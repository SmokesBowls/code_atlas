"""Optional scan profile: user-declared system hierarchy and external systems.

A profile only labels files the scanner already found. It never creates
dependency or communication relationships, and every value it contributes is
reported with claim_type "declared" so it cannot be mistaken for scan evidence.
"""

import fnmatch
import hashlib
import json
import os

PROFILE_VERSION = 1

_TOP_LEVEL_KEYS = {"profile_version", "name", "systems", "externals", "lifecycle"}
# Declared lifecycle states; independent of system membership. Undeclared paths stay "undeclared".
LIFECYCLE_STATES = ("active", "retired", "archived")
_SYSTEM_KEYS = {"roots", "components", "description"}
_EXTERNAL_KEYS = {"description", "bridge_files"}

# Mechanisms the scanner currently examines, and the ones it does not.
# Absence of an edge is only meaningful for mechanisms marked scanned=True.
COVERAGE_MECHANISMS = {
    "python_import": {
        "scanned": True,
        "scope": "static import / from-import statements in .py files",
        "limits": [
            "dynamic imports (importlib, __import__) are not resolved",
            "ambiguous imports are recorded as gaps, not edges",
        ],
    },
    "function_return_to_argument": {
        "scanned": True,
        "scope": "function return value passed to another function's argument",
        "limits": [
            "method calls are matched by bare name and may collide with unrelated functions",
        ],
    },
    "file_write_to_file_read": {
        "scanned": True,
        "scope": "writer and reader of the same literal file path",
        "limits": [
            "computed or constant-built paths are only partly resolved",
        ],
    },
    "http": {"scanned": False, "scope": "HTTP routes and clients", "limits": []},
    "subprocess": {"scanned": False, "scope": "subprocess invocations", "limits": []},
    "external_repository": {"scanned": False, "scope": "code outside the scanned root", "limits": []},
    "non_python_sources": {"scanned": False, "scope": "GDScript, JSON contracts and other non-Python files", "limits": []},
}


class ProfileError(ValueError):
    """Raised when a profile file is missing, unreadable, or invalid."""


def _check_rel_path(value, where):
    if not isinstance(value, str) or not value.strip():
        raise ProfileError(f"{where}: expected a non-empty relative path string")
    norm = value.replace("\\", "/").strip("/")
    if value.startswith(("/", "\\")) or (len(value) > 1 and value[1] == ":"):
        raise ProfileError(f"{where}: path must be relative to the scanned root: {value!r}")
    if ".." in norm.split("/"):
        raise ProfileError(f"{where}: path must not contain '..': {value!r}")
    return norm


def _check_unknown_keys(obj, allowed, where):
    unknown = sorted(set(obj) - allowed)
    if unknown:
        raise ProfileError(f"{where}: unknown key(s) {unknown}; allowed: {sorted(allowed)}")


def _within(path, prefix):
    return path == prefix or path.startswith(prefix + "/")


def validate_profile(data):
    """Validate a parsed profile and return a normalized copy. Raises ProfileError."""
    if not isinstance(data, dict):
        raise ProfileError("profile: top level must be a JSON object")
    _check_unknown_keys(data, _TOP_LEVEL_KEYS, "profile")
    if data.get("profile_version") != PROFILE_VERSION:
        raise ProfileError(f"profile: profile_version must be {PROFILE_VERSION}")

    name = data.get("name", "")
    if not isinstance(name, str):
        raise ProfileError("profile.name: expected a string")

    systems_in = data.get("systems", {})
    if not isinstance(systems_in, dict) or not systems_in:
        raise ProfileError("profile.systems: expected a non-empty object of system name -> definition")

    systems = []
    all_roots = []
    for sys_name, sdef in systems_in.items():
        where = f"systems.{sys_name}"
        if not sys_name.strip():
            raise ProfileError("profile.systems: system names must be non-empty")
        if not isinstance(sdef, dict):
            raise ProfileError(f"{where}: expected an object")
        _check_unknown_keys(sdef, _SYSTEM_KEYS, where)
        roots_in = sdef.get("roots")
        if not isinstance(roots_in, list) or not roots_in:
            raise ProfileError(f"{where}.roots: expected a non-empty list of paths")
        roots = [_check_rel_path(r, f"{where}.roots") for r in roots_in]
        for r in roots:
            for other_sys, other_root in all_roots:
                if _within(r, other_root) or _within(other_root, r):
                    raise ProfileError(
                        f"{where}.roots: {r!r} overlaps {other_root!r} of system {other_sys!r}; "
                        "each file may belong to only one system"
                    )
            all_roots.append((sys_name, r))

        comps_in = sdef.get("components", {})
        if not isinstance(comps_in, dict):
            raise ProfileError(f"{where}.components: expected an object of component name -> paths")
        components = []
        for comp_name, paths_in in comps_in.items():
            cwhere = f"{where}.components.{comp_name}"
            if not comp_name.strip():
                raise ProfileError(f"{where}.components: component names must be non-empty")
            if not isinstance(paths_in, list) or not paths_in:
                raise ProfileError(f"{cwhere}: expected a non-empty list of paths")
            paths = [_check_rel_path(p, cwhere) for p in paths_in]
            for p in paths:
                if not any(_within(p, r) for r in roots):
                    raise ProfileError(f"{cwhere}: {p!r} is outside the system roots {roots}")
            components.append({"name": comp_name, "paths": paths})

        description = sdef.get("description", "")
        if not isinstance(description, str):
            raise ProfileError(f"{where}.description: expected a string")
        systems.append({"name": sys_name, "description": description, "roots": roots, "components": components})

    externals_in = data.get("externals", {})
    if not isinstance(externals_in, dict):
        raise ProfileError("profile.externals: expected an object of external name -> definition")
    externals = []
    for ext_name, edef in externals_in.items():
        where = f"externals.{ext_name}"
        if not ext_name.strip():
            raise ProfileError("profile.externals: external names must be non-empty")
        if not isinstance(edef, dict):
            raise ProfileError(f"{where}: expected an object")
        _check_unknown_keys(edef, _EXTERNAL_KEYS, where)
        description = edef.get("description", "")
        if not isinstance(description, str):
            raise ProfileError(f"{where}.description: expected a string")
        patterns_in = edef.get("bridge_files", [])
        if not isinstance(patterns_in, list):
            raise ProfileError(f"{where}.bridge_files: expected a list of glob patterns")
        patterns = [_check_rel_path(p, f"{where}.bridge_files") for p in patterns_in]
        externals.append({"name": ext_name, "description": description, "bridge_patterns": patterns})

    names = [s["name"] for s in systems] + [e["name"] for e in externals]
    if len(set(names)) != len(names):
        raise ProfileError("profile: system and external names must be unique")

    lifecycle_in = data.get("lifecycle", {})
    if not isinstance(lifecycle_in, dict):
        raise ProfileError("profile.lifecycle: expected an object of state -> list of paths")
    _check_unknown_keys(lifecycle_in, set(LIFECYCLE_STATES), "lifecycle")
    lifecycle, seen = [], {}
    for state in LIFECYCLE_STATES:
        paths_in = lifecycle_in.get(state, [])
        if not isinstance(paths_in, list):
            raise ProfileError(f"lifecycle.{state}: expected a list of paths")
        for p in paths_in:
            norm = _check_rel_path(p, f"lifecycle.{state}")
            if norm in seen:
                raise ProfileError(f"lifecycle: {norm!r} is declared both {seen[norm]!r} and {state!r}")
            seen[norm] = state
            lifecycle.append({"state": state, "path": norm})

    return {"profile_version": PROFILE_VERSION, "name": name, "systems": systems, "externals": externals,
            "lifecycle": sorted(lifecycle, key=lambda x: x["path"])}


def lifecycle_of(path, lifecycle):
    """Declared state of path (longest declared prefix wins), or "undeclared"."""
    hit = _longest_match(path, [(x["state"], x["path"]) for x in lifecycle])
    return hit[0] if hit else "undeclared"


def load_profile(path):
    """Read, hash and validate a profile file. Returns (profile, provenance)."""
    abs_path = os.path.abspath(path)
    if not os.path.isfile(abs_path):
        raise ProfileError(f"profile file not found: {abs_path}")
    try:
        with open(abs_path, "rb") as f:
            raw = f.read()
        data = json.loads(raw.decode("utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as e:
        raise ProfileError(f"profile file could not be read as UTF-8 JSON: {abs_path}: {e}") from e
    profile = validate_profile(data)
    provenance = {
        "path": abs_path,
        "sha256": hashlib.sha256(raw).hexdigest(),
        "name": profile["name"],
        "profile_version": profile["profile_version"],
        "claim_type": "declared",
    }
    return profile, provenance


def _longest_match(path, candidates):
    """Return the candidate (name, prefix) with the longest prefix containing path, or None."""
    best = None
    for name, prefix in candidates:
        if _within(path, prefix) and (best is None or len(prefix) > len(best[1])):
            best = (name, prefix)
    return best


def build_profile_sections(report, profile, provenance, ignored_dirs):
    """Return the report sections a profile contributes: profile, systems, externals, coverage.

    Membership is assigned only to files present in report["files"]; nothing is added
    for paths the scanner did not see.
    """
    files = sorted(report.get("files", {}).keys())
    parse_error_files = sorted({pe["filepath"] for pe in report.get("parse_errors", [])})
    all_known = sorted(set(files) | set(parse_error_files))

    root_index = [(s["name"], r) for s in profile["systems"] for r in s["roots"]]
    system_members = {s["name"]: [] for s in profile["systems"]}
    outside = []
    for path in all_known:
        hit = _longest_match(path, root_index)
        if hit is None:
            outside.append(path)
        else:
            system_members[hit[0]].append(path)

    systems = []
    for s in profile["systems"]:
        members = system_members[s["name"]]
        comp_index = [(c["name"], p) for c in s["components"] for p in c["paths"]]
        comp_members = {c["name"]: [] for c in s["components"]}
        unassigned = []
        for path in members:
            hit = _longest_match(path, comp_index)
            if hit is None:
                unassigned.append(path)
            else:
                comp_members[hit[0]].append(path)
        systems.append({
            "name": s["name"],
            "description": s["description"],
            "claim_type": "declared",
            "source": "profile",
            "roots": s["roots"],
            "roots_without_scanned_files": [
                r for r in s["roots"] if not any(_within(p, r) for p in members)
            ],
            "file_count": len(members),
            "components": [
                {
                    "name": c["name"],
                    "paths": c["paths"],
                    "file_count": len(comp_members[c["name"]]),
                    "files": comp_members[c["name"]],
                }
                for c in s["components"]
            ],
            "unassigned_files": unassigned,
            "files": members,
        })

    externals = []
    for e in profile["externals"]:
        matched = [p for p in all_known if any(fnmatch.fnmatchcase(p, pat) for pat in e["bridge_patterns"])]
        externals.append({
            "name": e["name"],
            "description": e["description"],
            "claim_type": "declared",
            "source": "profile",
            "scanned": False,
            "bridge_patterns": e["bridge_patterns"],
            "bridge_files_in_scan": matched,
        })

    coverage = {
        "claim_type": "confirmed",
        "evidence_level": "source-level static analysis; no runtime confirmation",
        "scan_roots": report.get("scan_roots", []),
        "languages_scanned": ["python"],
        "ignored_dirs": sorted(ignored_dirs),
        "mechanisms": json.loads(json.dumps(COVERAGE_MECHANISMS)),
        "files_with_gaps": parse_error_files,
        "files_with_unresolved_imports": sorted({u["source"] for u in report.get("unresolved_imports", [])}),
        "files_outside_declared_systems": outside,
    }

    lifecycle = profile.get("lifecycle", [])
    files_by_state = {}
    for path in all_known:
        files_by_state.setdefault(lifecycle_of(path, lifecycle), []).append(path)
    lifecycle_section = {
        "claim_type": "declared",
        "source": "profile",
        "declarations": lifecycle,
        "file_counts": {st: len(files_by_state.get(st, [])) for st in LIFECYCLE_STATES + ("undeclared",)},
        "files": {st: files_by_state[st] for st in sorted(files_by_state)},
    }

    from code_atlas.core.system_coupling import build_system_coupling
    coupling = build_system_coupling(report, systems, lifecycle)
    return {"profile": provenance, "systems": systems, "externals": externals, "coverage": coverage,
            "lifecycle": lifecycle_section, "system_coupling": coupling}
