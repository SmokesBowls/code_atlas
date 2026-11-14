"""Match outgoing HTTP calls to incoming routes across one or more boundary inventories.

Outcomes, all source-level (a match never proves the call runs):
  matched     destination port is bound by a scanned server and its route list has the method+path
  candidate   method+path agree with a route whose server port is not known from source
  unmatched   the server on that port was scanned, its route list is complete, and nothing fits
  unknown     no scanned server on that port, or its route list is incomplete
  unresolved  the destination (or method) could not be resolved from source
  external    a non-local host
Runtime traces may later add evidence for unresolved calls; they are not recorded as static matches.
"""

import re

from code_atlas.core.http_boundaries import LOCAL_HOSTS

MATCH_FORMAT = "code_atlas.http_boundary_matches"
MATCH_VERSION = 1


def _path_ok(route, path):
    return bool(re.fullmatch(route["regex"], path) or re.fullmatch(route["regex"], path + "/"))


def _method_ok(route, method):
    return route["method"] in ("ANY", method)


def _ref(r):
    return {k: r.get(k) for k in ("system", "file", "line", "handler", "method", "path", "route_name")}


def match_boundaries(inventories):
    """inventories: list of inventory dicts (one per scanned repository)."""
    incoming = [r for inv in inventories for r in inv["incoming"]]
    handlers = {(h["file"], h["handler"]): h for inv in inventories for h in inv["handlers"]}
    ports_by_handler = {}
    for inv in inventories:
        for b in inv["bindings"]:
            if b["handler"] and b["port"]:  # port 0 = ephemeral (tests); never a fixed address
                ports_by_handler.setdefault(b["handler"], set()).add(b["port"])

    served = {}
    portless = []
    for r in incoming:
        ports = sorted(ports_by_handler.get(r.get("handler") or "", set())) if r["recognized_by"] == "http.server handler" else []
        if ports:
            for p in ports:
                served.setdefault(p, []).append(r)
        elif r["path_role"] == "production" and r["match"] != "prefix":
            # A prefix route (`path.startswith("/ap")`) is too weak to propose a connection
            # without a known port; it only counts once its server's port is bound in source.
            portless.append(r)

    results = []
    for inv in inventories:
        for c in inv["outgoing"]:
            d = c["destination"]
            row = {"call": {k: c[k] for k in ("system", "file", "line", "function", "method", "path_role", "recognized_by")},
                   "destination": d}
            if d["resolution"] == "unresolved" or c["method"] is None:
                row["outcome"] = "unresolved"
                row["reason"] = d.get("unresolved_reason") or c.get("method_unresolved_reason")
            elif d["host"] not in LOCAL_HOSTS:
                row["outcome"], row["reason"] = "external", f"non-local host {d['host']}"
            elif d["port"] in served:
                on_port = served[d["port"]]
                hits = [r for r in on_port if _method_ok(r, c["method"]) and _path_ok(r, d["path"])]
                if hits:
                    row["outcome"], row["servers"] = "matched", [_ref(h) for h in hits]
                    if d["resolution"] == "default":
                        row["caveat"] = "destination is a default that configuration may override"
                elif all(handlers.get((r["file"], r.get("handler")), {}).get("route_list_complete", False) for r in on_port):
                    row["outcome"] = "unmatched"
                    row["reason"] = f"server(s) on port {d['port']} were scanned; no {c['method']} {d['path']} route"
                else:
                    row["outcome"] = "unknown"
                    row["reason"] = f"route list of the server on port {d['port']} is not complete"
            else:
                hits = [r for r in portless if _method_ok(r, c["method"]) and _path_ok(r, d["path"])]
                if hits:
                    row["outcome"], row["servers"] = "candidate", [_ref(h) for h in hits]
                    row["reason"] = f"method and path agree; no scanned server is bound to port {d['port']} in source"
                else:
                    row["outcome"] = "unknown"
                    row["reason"] = f"no scanned server is bound to port {d['port']}"
            results.append(row)

    summary = {}
    for r in results:
        key = f"{r['call']['path_role']}:{r['outcome']}"
        summary[key] = summary.get(key, 0) + 1
    return {"format": MATCH_FORMAT, "version": MATCH_VERSION,
            "evidence_level": "source-level; a match is not runtime confirmation",
            "summary": dict(sorted(summary.items())), "results": results}
