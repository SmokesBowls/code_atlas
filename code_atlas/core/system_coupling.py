"""System-to-file coupling: which files account for the import edges between two declared systems.

Mechanism: resolved static Python imports only. An import edge is a code dependency, not
communication and not runtime use. Edges inside one system are left to the system-level view.
Possible edges (an unresolved import with a candidate in the other system) are reported apart
and never enter the counts or shares.
"""

from code_atlas.core.profile import lifecycle_of

OUTSIDE = "(outside declared systems)"
EVIDENCE = ("static import dependency between declared systems; "
            "not communication and not runtime use")


def _files_table(counter, total, lifecycle):
    rows = [{"file": f, "lifecycle": lifecycle_of(f, lifecycle), "edges": n, "share_percent": round(100 * n / total, 1)}
            for f, n in counter.items()]
    return sorted(rows, key=lambda r: (-r["edges"], r["file"]))


def build_system_coupling(report, systems, lifecycle):
    system_of = {f: s["name"] for s in systems for f in s["files"]}
    sys_of = lambda f: system_of.get(f, OUTSIDE)
    pairs = {}

    def pair(a, b):
        return pairs.setdefault((a, b), {"edges": [], "possible": []})

    for d in report.get("local_dependencies", []):
        a, b = sys_of(d["source"]), sys_of(d["target"])
        if a != b:
            pair(a, b)["edges"].append((d["source"], d["target"]))
    for u in report.get("unresolved_imports", []):
        a = sys_of(u["source"])
        for b in sorted({sys_of(c) for c in u["candidates"]} - {a}):
            pair(a, b)["possible"].append({"source": u["source"], "import": u["import"],
                                           "candidates": [c for c in u["candidates"] if sys_of(c) == b]})

    out = []
    for (a, b), p in pairs.items():
        n = len(p["edges"])
        src, tgt, by_life = {}, {}, {}
        for s, t in p["edges"]:
            src[s] = src.get(s, 0) + 1
            tgt[t] = tgt.get(t, 0) + 1
            key = lifecycle_of(s, lifecycle)
            by_life[key] = by_life.get(key, 0) + 1
        out.append({
            "from": a, "to": b, "mechanism": "python_import", "edges": n,
            "edges_by_source_lifecycle": dict(sorted(by_life.items())),
            "source_files": _files_table(src, n, lifecycle) if n else [],
            "target_files": _files_table(tgt, n, lifecycle) if n else [],
            "possible_edges": len(p["possible"]),
            "possible": p["possible"],
        })
    out.sort(key=lambda x: (-x["edges"], -x["possible_edges"], x["from"], x["to"]))
    return {"claim_type": "inferred", "mechanism": "python_import", "evidence_level": EVIDENCE,
            "lifecycle_source": "declared in profile; files with no declaration are 'undeclared'",
            "pairs": out}
