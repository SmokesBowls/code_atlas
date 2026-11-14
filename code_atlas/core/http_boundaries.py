"""HTTP boundary inventory: what each file sends and serves over HTTP, from source only.

This module is separate from the import scanner and never changes its results. It parses
Python files with the stdlib ast module (nothing is imported or executed) and records:

  outgoing   HTTP client calls: method, destination (resolved or not, and why), call site
  incoming   HTTP routes a server declares: method, path pattern, handler, declaring site
  bindings   servers bound to a port in source
  coverage   one entry per HTTP-looking call site, saying whether it was interpreted

Coverage is tracked per call site so an unsupported operation cannot hide inside a file
whose other calls were understood. Importing an HTTP library is not itself an operation.

Everything here is source-level evidence. A recorded call is not proof that it runs, and a
resolved destination is what the source says, which configuration may override.
"""

import ast
import os
import re

INVENTORY_FORMAT = "code_atlas.http_boundary_inventory"
INVENTORY_VERSION = 1
EVIDENCE_LEVEL = "source-level static analysis; not runtime confirmation"

HTTP_VERBS = ("get", "post", "put", "delete", "patch", "head", "options")
CLIENT_LIBS = ("requests", "httpx", "urllib.request", "http.client", "aiohttp", "urllib3")
# Receivers whose attribute calls are treated as HTTP sessions/clients by name.
SESSION_RECEIVERS = {"http", "session", "sess", "client", "http_client", "httpclient"}
# Attribute names that look like HTTP operations on a session-like receiver.
# Exact verbs only (optionally async_): `get_history()` on a `session` object is not an HTTP call.
OPERATION_NAME = re.compile(r"^(async_)?(get|post|put|delete|patch|head|options|request|stream|send|fetch|urlopen)$")
# Server-side registration calls this module has no adapter for; reported, never guessed.
UNSUPPORTED_REGISTRATIONS = {
    "add_url_rule", "add_api_route", "add_api_websocket_route", "include_router", "add_routes",
    "add_get", "add_post", "add_put", "add_delete", "add_patch", "add_head", "add_view",
}
SERVER_FRAMEWORKS = ("http.server", "fastapi", "flask", "starlette", "pyramid", "django", "aiohttp.web",
                     "tornado", "bottle", "falcon", "sanic", "socketserver")
LOCAL_HOSTS = {"127.0.0.1", "localhost", "0.0.0.0", "::1", ""}
MAX_WRAPPER_DEPTH = 3


# ---------------------------------------------------------------- value resolution

class Unknown:
    """A value that could not be resolved from source, with the reason."""

    def __init__(self, why):
        self.why = why


class Param:
    """A function parameter; resolved later at the function's call sites."""

    def __init__(self, name):
        self.name = name


def _join(parts):
    if any(isinstance(p, (Param, tuple)) for p in parts):
        return ("concat", parts)
    if all(isinstance(p, str) for p in parts):
        return "".join(parts)
    return Unknown("partly unresolved: " + "".join(p if isinstance(p, str) else "{?}" for p in parts))


def _is_template(v):
    return isinstance(v, (Param, tuple))


def _subst(value, bindings):
    if isinstance(value, Param):
        return bindings.get(value.name, value)
    if isinstance(value, tuple) and value[0] == "concat":
        return _join([_subst(p, bindings) for p in value[1]])
    if isinstance(value, tuple) and value[0] == "str_op":
        inner = _subst(value[2], bindings)
        if isinstance(inner, str):
            return getattr(inner, value[1])(*value[3])
        return inner if isinstance(inner, Unknown) else value
    return value


def _describe(v):
    if isinstance(v, Unknown):
        return v.why
    if isinstance(v, Param):
        return f"parameter {v.name!r} with no resolvable argument"
    if isinstance(v, tuple) and v[0] == "concat":
        return "built from unresolved parts: " + "".join(p if isinstance(p, str) else "{?}" for p in v[1])
    return "unresolved expression"


def _dotted(node):
    parts = []
    while isinstance(node, ast.Attribute):
        parts.append(node.attr)
        node = node.value
    if isinstance(node, ast.Name):
        parts.append(node.id)
        return ".".join(reversed(parts))
    return ""


def _kw(call, name):
    for k in call.keywords:
        if k.arg == name:
            return k.value
    return None


def _methods(cls):
    return {n.name: n for n in cls.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))}


def _params_with_defaults(fn):
    args = fn.args.args
    defaults = [None] * (len(args) - len(fn.args.defaults)) + list(fn.args.defaults)
    out = {a.arg: d for a, d in zip(args, defaults)}
    for a, d in zip(fn.args.kwonlyargs, fn.args.kw_defaults):
        out[a.arg] = d
    return out


def _local_assigns(fn):
    out = {}
    for node in ast.walk(fn):
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            out.setdefault(node.targets[0].id, []).append(node.value)
        elif isinstance(node, (ast.With, ast.AsyncWith)):
            for item in node.items:
                if isinstance(item.optional_vars, ast.Name):
                    out.setdefault(item.optional_vars.id, []).append(item.context_expr)
    return out


def _self_attrs(cls):
    init = _methods(cls).get("__init__")
    out = {}
    if init is not None:
        for node in ast.walk(init):
            if isinstance(node, ast.Assign) and len(node.targets) == 1:
                t = node.targets[0]
                if isinstance(t, ast.Attribute) and isinstance(t.value, ast.Name) and t.value.id == "self":
                    out[t.attr] = node.value
    return out


class _Module:
    def __init__(self, rel, system, tree):
        self.rel, self.system, self.tree = rel, system, tree
        self.consts, self.funcs, self.classes = {}, {}, {}
        for node in tree.body:
            if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
                self.consts[node.targets[0].id] = node.value
            elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name) and node.value is not None:
                self.consts[node.target.id] = node.value
            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                self.funcs[node.name] = node
            elif isinstance(node, ast.ClassDef):
                self.classes[node.name] = node
        # local name -> fully qualified HTTP library name, e.g. {"r": "requests", "urlopen": "urllib.request.urlopen"}
        self.http_aliases = {}
        self.imports = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for a in node.names:
                    self.imports.add(a.name)
                    if _in_libs(a.name):
                        self.http_aliases[a.asname or a.name.split(".")[0]] = a.name if a.asname else a.name.split(".")[0]
            elif isinstance(node, ast.ImportFrom) and node.module:
                self.imports.add(node.module)
                for a in node.names:
                    full = f"{node.module}.{a.name}"
                    if _in_libs(node.module) or _in_libs(full):
                        self.http_aliases[a.asname or a.name] = full
        self.scopes = [(None, f) for f in self.funcs.values()]
        for c in self.classes.values():
            self.scopes += [(c, f) for f in _methods(c).values()]
        # Module-level statements (scripts) as a pseudo-function, so top-level calls are scanned too.
        top = [s for s in tree.body if not isinstance(s, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))]
        if top:
            pseudo = ast.FunctionDef(name="<module>", body=top, decorator_list=[], returns=None, type_params=[],
                                     args=ast.arguments(posonlyargs=[], args=[], kwonlyargs=[], kw_defaults=[], defaults=[]))
            pseudo.lineno = top[0].lineno
            self.scopes.append((None, pseudo))


def _in_libs(name):
    return any(name == lib or name.startswith(lib + ".") for lib in CLIENT_LIBS)


class _Evaluator:
    """Resolves URL and method expressions to str, Param, a template tuple, or Unknown."""

    def __init__(self, module, cls, fn, bindings=None, depth=0):
        self.m, self.cls, self.fn, self.depth = module, cls, fn, depth
        self.bindings = bindings or {}
        self.params = _params_with_defaults(fn) if fn is not None else {}
        self.locals = _local_assigns(fn) if fn is not None else {}
        self.notes = []

    def child(self, cls, fn, bindings=None):
        return _Evaluator(self.m, cls, fn, bindings, self.depth + 1)

    def absorb(self, other, value):
        self.notes.extend(other.notes)
        return value

    def ev(self, node):
        if node is None:
            return Unknown("missing")
        if isinstance(node, ast.Constant):
            if isinstance(node.value, str):
                return node.value
            if isinstance(node.value, int) and not isinstance(node.value, bool):
                return str(node.value)  # ports interpolated into URLs
            return Unknown(f"non-string constant {node.value!r}")
        if isinstance(node, ast.JoinedStr):
            return _join([self.ev(v.value) if isinstance(v, ast.FormattedValue) else v.value for v in node.values])
        if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
            return _join([self.ev(node.left), self.ev(node.right)])
        if isinstance(node, ast.Name):
            return self._name(node.id)
        if isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name) and node.value.id == "self" and self.cls is not None:
            return self._self_attr(node.attr)
        if isinstance(node, ast.BoolOp) and isinstance(node.op, ast.Or):
            # `arg or default`: take the last literal operand and say it can be overridden.
            for v in reversed(node.values):
                r = self.ev(v)
                if isinstance(r, str):
                    self.notes.append("fallback default; an argument may override it")
                    return r
            return Unknown("`or` expression with no literal operand")
        if isinstance(node, ast.Call):
            return self._call(node)
        return Unknown(f"{type(node).__name__} expression")

    def _name(self, name):
        if name in self.bindings:
            return self.bindings[name]
        if name in self.params:
            return Param(name)
        vals = self.locals.get(name)
        if vals:
            if len(vals) > 1:
                self.notes.append(f"local {name!r} is assigned {len(vals)} times; the first assignment was used")
            return self.ev(vals[0])
        if name in self.m.consts:
            sub = self.child(None, None)
            return self.absorb(sub, sub.ev(self.m.consts[name]))
        return Unknown(f"name {name!r} not resolvable in this module")

    def _self_attr(self, attr):
        attrs = _self_attrs(self.cls)
        if attr not in attrs:
            return Unknown(f"self.{attr} is not assigned in __init__")
        init = _methods(self.cls)["__init__"]
        sub = self.child(self.cls, init)
        val = sub.ev(attrs[attr])
        if isinstance(val, Param):
            default = sub.params.get(val.name)
            d = sub.ev(default) if default is not None else None
            self.notes.extend(sub.notes)
            if isinstance(d, str):
                self.notes.append(f"constructor default for {val.name!r}; a caller may pass another value")
                return d
            return Unknown(f"constructor argument {val.name!r} has no literal default")
        return self.absorb(sub, val)

    def _call(self, node):
        f = node.func
        dotted = _dotted(f)
        if dotted in ("os.environ.get", "os.getenv", "environ.get", "getenv"):
            var = self.ev(node.args[0]) if node.args else Unknown("environment variable name")
            if len(node.args) > 1:
                d = self.ev(node.args[1])
                if isinstance(d, str):
                    self.notes.append(f"environment variable {var} overrides the default {d}")
                    return d
            return Unknown(f"environment variable {var if isinstance(var, str) else '?'} with no literal default")
        if isinstance(f, ast.Attribute) and f.attr in ("rstrip", "strip", "lstrip", "upper", "lower"):
            inner = self.ev(f.value)
            args = [self.ev(a) for a in node.args]
            if not all(isinstance(a, str) for a in args):
                return Unknown(f"{f.attr}() with unresolved argument")
            if isinstance(inner, str):
                return getattr(inner, f.attr)(*args)
            if isinstance(inner, Param):
                return ("str_op", f.attr, inner, tuple(args))
            return inner
        if self.depth < 4 and isinstance(f, ast.Attribute) and isinstance(f.value, ast.Name) and f.value.id == "self" and self.cls is not None:
            target = _methods(self.cls).get(f.attr)
            if target is not None:
                return self._inline(target, node, self.cls)
        if self.depth < 4 and isinstance(f, ast.Name) and f.id in self.m.funcs:
            return self._inline(self.m.funcs[f.id], node, None)
        return Unknown(f"value returned by {dotted or 'a call'}()")

    def _inline(self, target, call, cls):
        returns = [n.value for n in ast.walk(target) if isinstance(n, ast.Return) and n.value is not None]
        if len(returns) != 1:
            return Unknown(f"{target.name}() has {len(returns)} return statements")
        sub = self.child(cls, target, _bind_args(target, call, self, skip_self=cls is not None))
        return self.absorb(sub, sub.ev(returns[0]))


def _bind_args(target, call, caller, skip_self):
    names = [a.arg for a in target.args.args][1 if skip_self else 0:]
    bind = {}
    for name, arg in zip(names, call.args):
        bind[name] = caller.ev(arg)
    for kw in call.keywords:
        if kw.arg:
            bind[kw.arg] = caller.ev(kw.value)
    return bind


def split_url(url):
    """'http://h:p/path?q' -> (host, port, path); None if not an absolute http(s) URL."""
    if not isinstance(url, str):
        return None
    m = re.match(r"^(https?)://([^/:?#]*)(?::(\d+))?([^?#]*)", url)
    if not m:
        return None
    scheme, host, port, path = m.groups()
    return host, int(port) if port else (443 if scheme == "https" else 80), (path or "/").rstrip("/") or "/"


# ---------------------------------------------------------------- client side

def _is_http_constructor(node, module):
    """`httpx.AsyncClient()`, `requests.Session()`, `aiohttp.ClientSession()` and similar."""
    if not isinstance(node, ast.Call):
        return False
    dotted = _dotted(node.func)
    root = dotted.split(".")[0] if dotted else ""
    return root in module.http_aliases and dotted.split(".")[-1][:1].isupper()


def _session_names(module, cls, fn):
    """Receivers proven to hold an HTTP client object: locals / with-targets / self attributes."""
    names = {n for n, vals in _local_assigns(fn).items() if any(_is_http_constructor(v, module) for v in vals)}
    if cls is not None:
        names |= {"self." + a for a, v in _self_attrs(cls).items() if _is_http_constructor(v, module)}
    return names


def _receiver_kind(receiver, sessions):
    if receiver in sessions:
        return "HTTP client object"
    if receiver and receiver.split(".")[-1] in SESSION_RECEIVERS:
        return "session-like receiver name"
    return None


def _client_call(node, module, sessions):
    """Recognize an HTTP client call. Returns (recognized_by, url_node, method) or None.

    method is a literal string, an AST node to evaluate, or None (urllib, resolved later)."""
    f = node.func
    dotted = _dotted(f)
    root = dotted.split(".")[0] if dotted else ""
    full = module.http_aliases.get(root)
    full_dotted = (full + dotted[len(root):]) if full else dotted
    if full_dotted.endswith("urlopen") and (full or dotted.endswith("urllib.request.urlopen")):
        return ("urllib.urlopen", node.args[0] if node.args else _kw(node, "url"), None)
    if not isinstance(f, ast.Attribute) and not (full and full_dotted.split(".")[-1] in HTTP_VERBS + ("request",)):
        return None
    attr = full_dotted.split(".")[-1]
    receiver = dotted.rsplit(".", 1)[0] if "." in dotted else ""
    is_lib = bool(full) and full_dotted.split(".")[0] in ("requests", "httpx", "aiohttp", "urllib3")
    kind = _receiver_kind(receiver, sessions)
    if attr == "request":
        m_node = node.args[0] if node.args else _kw(node, "method")
        u_node = node.args[1] if len(node.args) > 1 else _kw(node, "url")
        if m_node is not None and u_node is not None:
            return ("request(method, url)", u_node, m_node)
        return None
    if attr in HTTP_VERBS:
        u_node = node.args[0] if node.args else _kw(node, "url")
        if u_node is None:
            return None
        if is_lib:
            return ("library function", u_node, attr.upper())
        if kind == "HTTP client object":
            return (kind, u_node, attr.upper())
        if kind and not _non_url_literal(u_node):
            return (kind, u_node, attr.upper())
    return None


def _non_url_literal(node):
    """Name-only evidence guard: `self.client.get("key")` on a dict-like object is not HTTP."""
    return isinstance(node, ast.Constant) and isinstance(node.value, str) \
        and not node.value.startswith(("http://", "https://", "/"))


def _http_looking(node, module, sessions):
    """Does this call look like an HTTP operation, whether or not it can be interpreted?"""
    dotted = _dotted(node.func)
    if not dotted:
        return None
    root, attr = dotted.split(".")[0], dotted.split(".")[-1]
    full = module.http_aliases.get(root)
    if full:
        name = (full + dotted[len(root):]).split(".")[-1]
        if name[:1].islower() and OPERATION_NAME.match(name):
            return f"call into HTTP library {full}"
    if "." in dotted:
        receiver = dotted.rsplit(".", 1)[0]
        kind = _receiver_kind(receiver, sessions)
        first = node.args[0] if node.args else None
        if kind == "session-like receiver name" and _non_url_literal(first):
            return None
        if kind and OPERATION_NAME.match(attr):
            return f"operation-like call {attr}() on {kind} '{receiver}'"
    return None


def _request_parts(ev, node):
    url = ev.ev(node.args[0] if node.args else _kw(node, "url"))
    method_node = _kw(node, "method")
    data_given = len(node.args) > 1 or (
        _kw(node, "data") is not None and not (isinstance(_kw(node, "data"), ast.Constant) and _kw(node, "data").value is None))
    if method_node is not None:
        method = _method_value(ev, method_node)
    else:
        method = "POST" if data_given else "GET"
        ev.notes.append(f"method inferred as {method} from whether a request body is passed")
    return url, method


def _method_value(ev, method):
    if method is None or isinstance(method, str):
        return method
    v = ev.ev(method)
    if isinstance(v, str):
        return v.upper()
    if isinstance(v, Param):
        return ("str_op", "upper", v, ())
    if isinstance(v, tuple):
        return v
    return Unknown("method expression not resolvable")


def _extract_client_calls(module):
    calls, looking = [], []
    for cls, fn in module.scopes:
        sessions = _session_names(module, cls, fn)
        for node in ast.walk(fn):
            if not isinstance(node, ast.Call):
                continue
            hit = _client_call(node, module, sessions)
            if hit is None:
                why = _http_looking(node, module, sessions)
                if why:
                    looking.append((node, fn, cls, why))
                continue
            recognized_by, url_node, method = hit
            ev = _Evaluator(module, cls, fn)
            if recognized_by == "urllib.urlopen":
                target = url_node
                if isinstance(target, ast.Name) and len(ev.locals.get(target.id, [])) == 1:
                    target = ev.locals[target.id][0]
                if isinstance(target, ast.Call) and _dotted(target.func).split(".")[-1] == "Request":
                    url, method = _request_parts(ev, target)
                else:
                    url, method = ev.ev(target), "GET"
            else:
                url, method = ev.ev(url_node), _method_value(ev, method)
            calls.append({"node": node, "fn": fn, "cls": cls, "module": module, "recognized_by": recognized_by,
                          "url": url, "method": method, "notes": ev.notes, "via": [], "link_evidence": None})
    # A node can be both recognized and http-looking (e.g. requests.get); keep only true gaps.
    recognized_ids = {id(c["node"]) for c in calls}
    gaps = [g for g in looking if id(g[0]) not in recognized_ids]
    return calls, gaps


def _def_counts(modules):
    counts = {}
    for m in modules:
        for _, f in m.scopes:
            counts[f.name] = counts.get(f.name, 0) + 1
    return counts


def _call_index(modules):
    """All calls in scan order, keyed by called name: ({attr: [...]} for x.attr(), {name: [...]} for name())."""
    by_attr, by_name = {}, {}
    for m in modules:
        for scls, sfn in m.scopes:
            for node in ast.walk(sfn):
                if isinstance(node, ast.Call):
                    f = node.func
                    if isinstance(f, ast.Attribute):
                        by_attr.setdefault(f.attr, []).append((m, scls, sfn, node))
                    elif isinstance(f, ast.Name):
                        by_name.setdefault(f.id, []).append((m, scls, sfn, node))
    return by_attr, by_name


def _call_sites(index, fn, cls, home, name_unique):
    """Calls to wrapper fn: same-class/same-module calls, or by unique name from elsewhere."""
    by_attr, by_name = index
    if cls is not None:
        for m, scls, sfn, node in by_attr.get(fn.name, ()):
            f = node.func
            if isinstance(f.value, ast.Name) and f.value.id == "self" and scls is cls:
                yield m, scls, sfn, node, "same-class call"
            elif name_unique:
                yield m, scls, sfn, node, "method name unique in scan (receiver type not checked)"
    else:
        for m, scls, sfn, node in by_name.get(fn.name, ()):
            if m is home:
                yield m, scls, sfn, node, "same-module call"
            elif name_unique:
                yield m, scls, sfn, node, "function name unique in scan (import not checked)"


def _expand_wrappers(modules, calls):
    """Replace calls whose URL or method depends on parameters with one call per call site."""
    counts = _def_counts(modules)
    index = _call_index(modules)
    out, wrappers = [], []
    pending = [(c, 0) for c in calls]
    while pending:
        c, depth = pending.pop()
        if not (_is_template(c["url"]) or _is_template(c["method"])):
            out.append(c)
            continue
        fn, cls = c["fn"], c["cls"]
        unique = counts.get(fn.name, 0) == 1
        sites = list(_call_sites(index, fn, cls, c["module"], unique)) if depth < MAX_WRAPPER_DEPTH else []
        wrappers.append({"file": c["module"].rel, "line": c["node"].lineno, "function": fn.name,
                         "class": cls.name if cls else None, "call_sites": len(sites), "name_unique": unique})
        if not sites:
            reason = "wrapper with no call site in scan" if depth < MAX_WRAPPER_DEPTH else "wrapper chain deeper than limit"
            out.append({**c, "notes": c["notes"] + [reason]})
            continue
        for m, scls, sfn, node, evidence in sites:
            ev = _Evaluator(m, scls, sfn)
            bind = _bind_args(fn, node, ev, skip_self=cls is not None)
            pending.append(({
                **c, "node": node, "fn": sfn, "cls": scls, "module": m,
                "url": _subst(c["url"], bind), "method": _subst(c["method"], bind),
                "via": c["via"] + [f"{c['module'].rel}:{c['node'].lineno} {fn.name}()"],
                "link_evidence": evidence, "notes": c["notes"] + ev.notes,
            }, depth + 1))
    return out, wrappers


def _outgoing_record(c, path_role):
    url, method = c["url"], c["method"]
    parts = split_url(url) if isinstance(url, str) else None
    if parts:
        resolution = "default" if any("default" in n or "override" in n for n in c["notes"]) else "literal"
        destination = {"url": url, "host": parts[0], "port": parts[1], "path": parts[2], "resolution": resolution}
    else:
        destination = {"url": url if isinstance(url, str) else None, "host": None, "port": None, "path": None,
                       "resolution": "unresolved",
                       "unresolved_reason": "not an absolute http URL" if isinstance(url, str) else _describe(url)}
    m = c["module"]
    return {
        "system": m.system, "file": m.rel, "line": c["node"].lineno, "function": c["fn"].name,
        "class": c["cls"].name if c["cls"] else None, "path_role": path_role(m.rel),
        "mechanism": "http", "direction": "outgoing", "recognized_by": c["recognized_by"],
        "method": method.upper() if isinstance(method, str) else None,
        "method_unresolved_reason": None if isinstance(method, str) else _describe(method),
        "destination": destination, "via": c["via"], "link_evidence": c["link_evidence"],
        "notes": sorted(set(c["notes"])),
    }


# ---------------------------------------------------------------- server side

def _str_list(node):
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return [node.value.upper()]
    if isinstance(node, (ast.Tuple, ast.List)):
        vals = [e.value.upper() for e in node.elts if isinstance(e, ast.Constant) and isinstance(e.value, str)]
        return vals if len(vals) == len(node.elts) else None
    return None


def _path_names(fn):
    names = {"path"}
    for node in ast.walk(fn):
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            if any(isinstance(n, ast.Attribute) and n.attr == "path" for n in ast.walk(node.value)):
                names.add(node.targets[0].id)
    return names


def _handler_routes(fn):
    """Literal paths compared against the request path inside a do_<METHOD> handler."""
    names = _path_names(fn)

    def is_path(n):
        return (isinstance(n, ast.Name) and n.id in names) or (isinstance(n, ast.Attribute) and n.attr in names)

    exact, prefix, table_lines = set(), set(), []
    for node in ast.walk(fn):
        if isinstance(node, ast.Compare) and is_path(node.left) and len(node.ops) == 1:
            comp = node.comparators[0]
            if isinstance(node.ops[0], ast.Eq) and isinstance(comp, ast.Constant) and isinstance(comp.value, str):
                exact.add(comp.value)
            elif isinstance(node.ops[0], ast.In) and isinstance(comp, (ast.Tuple, ast.List, ast.Set)):
                exact.update(e.value for e in comp.elts if isinstance(e, ast.Constant) and isinstance(e.value, str))
        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            if node.func.attr == "startswith" and is_path(node.func.value) and node.args and isinstance(node.args[0], ast.Constant):
                prefix.add(node.args[0].value)
            elif node.func.attr == "get" and node.args and is_path(node.args[0]):
                table_lines.append(node.lineno)
        elif isinstance(node, ast.Subscript) and is_path(node.slice):
            table_lines.append(node.lineno)
    return exact, prefix, table_lines


def pattern_regex(pattern):
    """Path pattern with {name} / {name:regex} / *rest segments -> regex."""
    out, i = "", 0
    while i < len(pattern):
        ch = pattern[i]
        if ch == "{":
            depth, j = 1, i + 1
            while j < len(pattern) and depth:
                depth += {"{": 1, "}": -1}.get(pattern[j], 0)
                j += 1
            body = pattern[i + 1:j - 1]
            out += "(" + body.split(":", 1)[1] + ")" if ":" in body else "([^/]+)"
            i = j
        elif ch == "*":
            return out + ".*"
        else:
            out += re.escape(ch)
            i += 1
    return out


def _extract_server(module, path_role):
    routes, handlers, coverage, bindings = [], [], [], []
    pyramid_decl, pyramid_views = [], []
    role = path_role(module.rel)

    def cov(line, status, detail):
        coverage.append({"system": module.system, "file": module.rel, "line": line, "path_role": role,
                         "side": "server", "status": status, "detail": detail})

    # Decorator routes: @app.get("/x"), @router.post("/x"), @app.route("/x", methods=[...]).
    # Every function definition is checked, including ones nested in app factories.
    owner = {id(f): c for c, f in module.scopes if c is not None}
    all_fns = [n for n in ast.walk(module.tree) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]
    for fn in all_fns:
        cls = owner.get(id(fn))
        for dec in fn.decorator_list:
            if not (isinstance(dec, ast.Call) and isinstance(dec.func, ast.Attribute)):
                continue
            attr = dec.func.attr
            if attr == "view_config":
                continue
            if attr not in HTTP_VERBS + ("route", "api_route", "websocket"):
                continue
            p = dec.args[0] if dec.args else _kw(dec, "path")
            if isinstance(p, ast.Constant) and isinstance(p.value, str) and p.value.startswith("/"):
                methods = [attr.upper()] if attr in HTTP_VERBS else (_str_list(_kw(dec, "methods")) or ["GET"])
                for meth in methods:
                    routes.append({"file": module.rel, "line": dec.lineno, "recognized_by": "route decorator",
                                   "app": _dotted(dec.func.value), "handler": fn.name, "method": meth,
                                   "path": p.value, "match": "regex", "regex": pattern_regex(p.value.rstrip("/") or "/")})
                cov(dec.lineno, "interpreted", f"@{_dotted(dec.func)} route")
            elif p is not None:
                cov(dec.lineno, "not-interpreted", f"@{_dotted(dec.func)} with a non-literal path")
        # Pyramid view_config: route_name links to add_route declarations.
        for dec in fn.decorator_list:
            if isinstance(dec, ast.Call) and _dotted(dec.func).split(".")[-1] == "view_config":
                rn, rm = _kw(dec, "route_name"), _kw(dec, "request_method")
                pyramid_views.append({"file": module.rel, "line": dec.lineno,
                                      "route_name": rn.value if isinstance(rn, ast.Constant) else None,
                                      "methods": _str_list(rm) if rm is not None else None,
                                      "handler": f"{cls.name + '.' if cls else ''}{fn.name}",
                                      "predicates": sorted(k.arg for k in dec.keywords if k.arg not in ("route_name", "request_method"))})

    # http.server handler classes.
    for cls in module.classes.values():
        dos = {k: v for k, v in _methods(cls).items() if k.startswith("do_") and k[3:].lower() in HTTP_VERBS}
        if not dos:
            continue
        table = []
        for name, fn in sorted(dos.items()):
            exact, prefix, table_lines = _handler_routes(fn)
            table += table_lines
            for p in sorted(exact):
                path = p.rstrip("/") or "/"
                routes.append({"file": module.rel, "line": fn.lineno, "recognized_by": "http.server handler",
                               "handler": cls.name, "method": name[3:], "path": path, "match": "regex",
                               "regex": re.escape(path)})
            for p in sorted(prefix):
                routes.append({"file": module.rel, "line": fn.lineno, "recognized_by": "http.server handler",
                               "handler": cls.name, "method": name[3:], "path": p + "*", "match": "prefix",
                               "regex": re.escape(p) + ".*"})
            cov(fn.lineno, "interpreted" if (exact or prefix) else "not-interpreted",
                f"{cls.name}.{name}: {len(exact) + len(prefix)} literal route comparisons")
            for line in table_lines:
                cov(line, "not-interpreted", f"{cls.name}.{name}: route lookup through a table is not followed")
        handlers.append({"file": module.rel, "handler": cls.name, "methods": sorted(k[3:] for k in dos),
                         "route_list_complete": not table,
                         "completeness_basis": "literal comparisons inside do_* methods only; helpers they call are not followed"})

    for node in ast.walk(module.tree):
        if not isinstance(node, ast.Call):
            continue
        dotted = _dotted(node.func)
        attr = dotted.split(".")[-1]
        if attr == "add_route" and isinstance(node.func, ast.Attribute):
            name = node.args[0] if node.args else _kw(node, "name")
            pattern = node.args[1] if len(node.args) > 1 else _kw(node, "pattern")
            if isinstance(name, ast.Constant) and isinstance(pattern, ast.Constant) and isinstance(pattern.value, str):
                rm = _kw(node, "request_method")
                pyramid_decl.append({"file": module.rel, "line": node.lineno, "name": name.value, "pattern": pattern.value,
                                     "methods": _str_list(rm) if rm is not None else None})
                cov(node.lineno, "interpreted", "add_route declaration")
            else:
                cov(node.lineno, "not-interpreted", "add_route with a non-literal name or pattern")
        elif attr in UNSUPPORTED_REGISTRATIONS and isinstance(node.func, ast.Attribute):
            cov(node.lineno, "not-interpreted", f"{attr}() route registration (no adapter)")
        elif attr.endswith("HTTPServer") and len(node.args) >= 2:
            addr, handler = node.args[0], node.args[1]
            port = None
            if isinstance(addr, ast.Tuple) and len(addr.elts) == 2:
                p = addr.elts[1]
                if isinstance(p, ast.Constant) and isinstance(p.value, int):
                    port = p.value
                elif isinstance(p, ast.Name) and isinstance(module.consts.get(p.id), ast.Constant) and isinstance(module.consts[p.id].value, int):
                    port = module.consts[p.id].value
            bindings.append({"system": module.system, "file": module.rel, "line": node.lineno, "path_role": role,
                             "handler": (_dotted(handler) or "").split(".")[-1] or None, "port": port})
            cov(node.lineno, "interpreted" if port is not None else "interpreted-unresolved",
                "server bound to port " + (str(port) if port is not None else "computed at runtime"))
    return routes, handlers, coverage, bindings, pyramid_decl, pyramid_views


def _join_pyramid(decls, views, system_of_file, path_role):
    by_name = {}
    for d in decls:
        by_name.setdefault(d["name"], []).append(d)
    routes, coverage, used = [], [], set()
    for v in views:
        targets = by_name.get(v["route_name"], [])
        if not targets:
            coverage.append({"system": system_of_file(v["file"]), "file": v["file"], "line": v["line"],
                             "path_role": path_role(v["file"]), "side": "server", "status": "not-interpreted",
                             "detail": f"view_config route_name {v['route_name']!r} has no add_route in scan"})
            continue
        coverage.append({"system": system_of_file(v["file"]), "file": v["file"], "line": v["line"],
                         "path_role": path_role(v["file"]), "side": "server", "status": "interpreted",
                         "detail": f"view_config for route {v['route_name']!r}"})
        for t in targets:
            used.add((t["file"], t["line"]))
            for meth in (v["methods"] or t["methods"] or ["ANY"]):
                routes.append({"file": v["file"], "line": v["line"], "recognized_by": "pyramid view_config + add_route",
                               "handler": v["handler"], "method": meth, "path": t["pattern"], "match": "regex",
                               "regex": pattern_regex(t["pattern"]), "route_name": t["name"],
                               "route_declared_at": f"{t['file']}:{t['line']}", "predicates": v["predicates"]})
    for t in decls:
        if (t["file"], t["line"]) not in used:
            routes.append({"file": t["file"], "line": t["line"], "recognized_by": "pyramid add_route",
                           "handler": None, "method": "ANY", "path": t["pattern"], "match": "regex",
                           "regex": pattern_regex(t["pattern"]), "route_name": t["name"],
                           "notes": ["route declared; no view_config for it found in scan"]})
    return routes, coverage


# ---------------------------------------------------------------- inventory

def default_path_role(rel):
    """Heuristic from the path only: 'test' for test files, else 'production'."""
    parts = rel.split("/")
    if "tests" in parts or "test" in parts[:-1] or parts[-1].startswith("test_") or parts[-1].endswith("_test.py") \
            or parts[-1] == "conftest.py" or any(p.startswith("test_") for p in parts[:-1]):
        return "test"
    return "production"


def build_http_inventory(root_dir, rel_paths, system_of, path_role=default_path_role):
    """Build the HTTP boundary inventory for the given files under root_dir.

    rel_paths: forward-slash paths relative to root_dir (normally report["files"] keys).
    system_of: callable rel_path -> system name.
    """
    modules, parse_gaps = [], []
    for rel in sorted(rel_paths):
        path = os.path.join(root_dir, *rel.split("/"))
        try:
            with open(path, "rb") as fh:
                tree = ast.parse(fh.read(), filename=rel)
        except (OSError, SyntaxError, ValueError) as e:
            parse_gaps.append({"file": rel, "error": f"{type(e).__name__}: {e}"})
            continue
        modules.append(_Module(rel, system_of(rel), tree))

    raw_calls, gap_sites = [], []
    incoming, handlers, coverage, bindings, decls, views = [], [], [], [], [], []
    for m in modules:
        calls, gaps = _extract_client_calls(m)
        raw_calls += calls
        gap_sites += [(m, g) for g in gaps]
        r, h, cv, b, d, v = _extract_server(m, path_role)
        for x in r:
            x["system"], x["path_role"] = m.system, path_role(m.rel)
        for x in h:
            x["system"], x["path_role"] = m.system, path_role(m.rel)
        incoming += r
        handlers += h
        coverage += cv
        bindings += b
        decls += d
        views += v
    pr, pcov = _join_pyramid(decls, views, system_of, path_role)
    for x in pr:
        x["system"], x["path_role"] = system_of(x["file"]), path_role(x["file"])
    incoming += pr
    coverage += pcov

    # Client coverage is recorded at the direct call site, before wrapper expansion.
    for c in raw_calls:
        resolved = isinstance(c["url"], str) and split_url(c["url"]) and isinstance(c["method"], str)
        coverage.append({"system": c["module"].system, "file": c["module"].rel, "line": c["node"].lineno,
                         "path_role": path_role(c["module"].rel), "side": "client",
                         "status": "interpreted" if resolved else (
                             "interpreted-wrapper" if (_is_template(c["url"]) or _is_template(c["method"])) else "interpreted-unresolved"),
                         "detail": c["recognized_by"]})
    for m, (node, fn, cls, why) in gap_sites:
        coverage.append({"system": m.system, "file": m.rel, "line": node.lineno, "path_role": path_role(m.rel),
                         "side": "client", "status": "not-interpreted", "detail": why})

    expanded, wrappers = _expand_wrappers(modules, raw_calls)
    outgoing = [_outgoing_record(c, path_role) for c in expanded]
    # Call sites reached through a wrapper are HTTP operations too; record their coverage,
    # including intermediate levels (a call inside a wrapper that is itself wrapped).
    covered = {(c["file"], c["line"]) for c in coverage if c["side"] == "client"}
    for w in wrappers:
        if (w["file"], w["line"]) not in covered:
            covered.add((w["file"], w["line"]))
            coverage.append({"system": system_of(w["file"]), "file": w["file"], "line": w["line"],
                             "path_role": path_role(w["file"]), "side": "client", "status": "interpreted-wrapper",
                             "detail": f"inside wrapper {w['function']}() ({w['call_sites']} call sites)"})
    for o in outgoing:
        if o["via"]:
            coverage.append({"system": o["system"], "file": o["file"], "line": o["line"], "path_role": o["path_role"],
                             "side": "client",
                             "status": "interpreted" if o["destination"]["resolution"] != "unresolved" and o["method"] else "interpreted-unresolved",
                             "detail": f"call through wrapper {o['via'][0].split(' ', 1)[1]}"})

    key = lambda x: (x["file"], x["line"], x.get("method") or "", str(x.get("path") or x.get("destination", {}).get("url")))
    outgoing.sort(key=key)
    incoming.sort(key=key)
    coverage.sort(key=lambda x: (x["file"], x["line"], x["side"], x["detail"]))
    # Informational only: importing an HTTP library or framework is not an operation.
    with_sites = {c["file"] for c in coverage}
    imports_only = sorted(m.rel for m in modules if m.rel not in with_sites and (
        m.http_aliases or any(i == fw or i.startswith(fw + ".") for i in m.imports for fw in SERVER_FRAMEWORKS)))
    return {
        "format": INVENTORY_FORMAT,
        "version": INVENTORY_VERSION,
        "mechanism": "http",
        "evidence_level": EVIDENCE_LEVEL,
        "files_scanned": len(modules),
        "outgoing": outgoing,
        "incoming": incoming,
        "bindings": sorted(bindings, key=lambda x: (x["file"], x["line"])),
        "handlers": sorted(handlers, key=lambda x: (x["file"], x["handler"])),
        "wrappers": sorted(wrappers, key=lambda x: (x["file"], x["line"])),
        "coverage": coverage,
        "coverage_summary": _coverage_summary(coverage),
        "files_importing_http_without_operations": imports_only,
        "parse_gaps": parse_gaps,
    }


def _coverage_summary(coverage):
    by_status = {}
    for c in coverage:
        by_status[c["status"]] = by_status.get(c["status"], 0) + 1
    gaps = sorted({(c["file"], c["line"], c["detail"]) for c in coverage if c["status"] == "not-interpreted"})
    return {"sites_by_status": dict(sorted(by_status.items())),
            "not_interpreted": [{"file": f, "line": l, "detail": d} for f, l, d in gaps]}
