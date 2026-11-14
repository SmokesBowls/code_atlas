"""Blast radius: which scanned files depend on a given file, directly or transitively.

Source-level impact estimate over static import edges only; not a prediction of runtime failure.
  confirmed  reached from the file through resolved import edges (reverse direction: importers)
  possible   reached only through at least one unresolved import whose candidates include a file
             on the path; never counted as a dependent
  gaps       why both counts may be incomplete (unparsed files, mechanisms Atlas does not trace)

Query: python3 -m code_atlas.core.blast_radius --report report.json --file path/to/x.py [--boundaries b.json] [--json]
"""

import argparse
import json
import sys
from collections import deque

from code_atlas.core.profile import lifecycle_of

SCOPE = ("source-level impact estimate over resolved static Python imports; "
         "not a prediction of runtime failure")
UNTRACED = [
    "dynamic imports (importlib, __import__, exec)",
    "duck-typed use of objects and attribute patching (setattr, monkey-patching)",
    "HTTP, subprocess and file-drop handoffs between processes",
    "callers outside the scanned root and non-Python callers (GDScript, shell, JSON contracts)",
]


def _reverse(edges):
    rev = {}
    for src, tgt in edges:
        rev.setdefault(tgt, set()).add(src)
    return rev


def _closure(start, rev):
    seen, queue = {start}, deque([start])
    while queue:
        for importer in sorted(rev.get(queue.popleft(), ())):
            if importer not in seen:
                seen.add(importer)
                queue.append(importer)
    seen.discard(start)
    return seen


def _graphs(report):
    resolved = [(d["source"], d["target"]) for d in report.get("local_dependencies", [])]
    candidate = [(u["source"], c) for u in report.get("unresolved_imports", []) for c in u["candidates"]]
    return _reverse(resolved), _reverse(resolved + candidate)


def blast_radius_counts(report):
    """{file: {"confirmed_direct", "confirmed", "possible"}} for every file in report["files"]."""
    rev, rev_all = _graphs(report)
    out = {}
    for f in report.get("files", {}):
        confirmed = _closure(f, rev)
        out[f] = {"confirmed_direct": len(rev.get(f, ())), "confirmed": len(confirmed),
                  "possible": len(_closure(f, rev_all) - confirmed)}
    return out


def blast_radius(report, target, boundaries=None):
    """Full detail for one file: dependent lists, how possible ones arise, and analysis gaps."""
    if target not in report.get("files", {}):
        raise KeyError(f"{target!r} is not a parsed file in this report")
    rev, rev_all = _graphs(report)
    confirmed = _closure(target, rev)
    possible = _closure(target, rev_all) - confirmed
    affected = {target} | confirmed | possible
    via = [u for u in report.get("unresolved_imports", []) if set(u["candidates"]) & affected
           and (u["source"] in possible)]
    gaps = []
    unparsed = sorted(pe["filepath"] for pe in report.get("parse_errors", []))
    if unparsed:
        gaps.append({"kind": "unparsed_files", "count": len(unparsed), "files": unparsed,
                     "why": "Atlas could not read these files' imports; any of them may depend on this file"})
    if via:
        gaps.append({"kind": "unresolved_imports", "count": len(via),
                     "why": "these imports may point at this file or one of its dependents; "
                            "the files that make them are listed as possible, not confirmed"})
    gaps.append({"kind": "untraced_mechanisms", "mechanisms": UNTRACED,
                 "why": "dependents that reach the file only through these are not counted"})
    if boundaries:
        inv = boundaries.get("inventory", boundaries)
        scope = {target} | confirmed
        servers = {}
        for r in inv.get("incoming", []):
            if r["file"] in scope:
                servers[r["file"]] = servers.get(r["file"], 0) + 1
        if servers:
            gaps.append({"kind": "http_boundary", "files": [f"{f} ({n} routes)" for f, n in sorted(servers.items())],
                         "why": "this file or a confirmed dependent serves HTTP routes; HTTP callers of those routes "
                                "are not import dependents and are not counted (see the boundary analysis)"})
    system_of = {f: s["name"] for s in report.get("systems", []) for f in s["files"]}
    declared = (report.get("lifecycle") or {}).get("declarations")
    group = lambda files: {f: {"system": system_of.get(f, "(outside declared systems)" if system_of else None),
                               "lifecycle": lifecycle_of(f, declared) if declared is not None else None}
                           for f in sorted(files)}
    by_life = {}
    for f in confirmed:
        key = lifecycle_of(f, declared) if declared is not None else "no lifecycle declared"
        by_life[key] = by_life.get(key, 0) + 1
    return {
        "file": target,
        "scope": SCOPE,
        "confirmed_direct": sorted(rev.get(target, ())),
        "confirmed": group(confirmed),
        "confirmed_by_lifecycle": dict(sorted(by_life.items())),
        "possible": group(possible),
        "possible_via": [{"source": u["source"], "import": u["import"], "candidates": u["candidates"]} for u in via],
        "gaps": gaps,
    }


def _text(r):
    lines = [f"Blast radius of {r['file']}", f"  ({r['scope']})", ""]
    headings = {"confirmed": f"Confirmed dependents: {len(r['confirmed'])} ({len(r['confirmed_direct'])} import it directly)",
                "possible": f"Possible dependents (through unresolved imports, not counted): {len(r['possible'])}"}
    for key in ("confirmed", "possible"):
        lines.append(headings[key])
        if key == "confirmed" and r["confirmed_by_lifecycle"]:
            lines.append("  by declared lifecycle: " + ", ".join(f"{k} {v}" for k, v in r["confirmed_by_lifecycle"].items()))
        by = {}
        for f, info in r[key].items():
            by.setdefault(info["system"], []).append(f)
        for s in sorted(by, key=lambda x: (x is None, x or "")):
            if s is not None:
                lines.append(f"  [{s}] {len(by[s])}")
            for f in by[s]:
                mark = " *direct" if key == "confirmed" and f in r["confirmed_direct"] else ""
                life = r[key][f]["lifecycle"]
                lines.append(f"    {f}{mark}" + (f"  ({life})" if life else ""))
    for u in r["possible_via"]:
        lines.append(f"  via {u['source']}: import {u['import']} -> {', '.join(u['candidates'])}")
    lines.append("Analysis gaps (the counts above may be incomplete):")
    for g in r["gaps"]:
        lines.append(f"  - {g['kind']}: {g['why']}")
        for x in g.get("files", []) + g.get("mechanisms", []):
            lines.append(f"      {x}")
    return "\n".join(lines)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Code Atlas blast radius for one file (source-level estimate)")
    ap.add_argument("--report", required=True, help="Code Atlas JSON report")
    ap.add_argument("--file", required=True, help="repository-relative path, as in the report")
    ap.add_argument("--boundaries", help="optional --boundaries-output JSON, to name HTTP gaps")
    ap.add_argument("--json", action="store_true", help="print JSON instead of text")
    a = ap.parse_args(argv)
    with open(a.report, encoding="utf-8") as fh:
        report = json.load(fh)
    boundaries = None
    if a.boundaries:
        with open(a.boundaries, encoding="utf-8") as fh:
            boundaries = json.load(fh)
    try:
        r = blast_radius(report, a.file, boundaries)
    except KeyError as e:
        print(f"Error: {e.args[0]}", file=sys.stderr)
        return 1
    print(json.dumps(r, indent=2) if a.json else _text(r))
    return 0


if __name__ == "__main__":
    sys.exit(main())
