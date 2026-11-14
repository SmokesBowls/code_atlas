"""AI-oriented architectural exporter for Code Atlas reports.

Compreses and structures report data into token-conscious, deterministic JSON and Markdown packets.
"""

import json
import os

CONTRACT_HEADER = {
    "contract": "code_atlas.ai_architecture_packet",
    "contract_version": "1.1.0",
    "source_report_contract": "code_atlas.report",
    "source_report_contract_version": None
}

STATIC_REACHABILITY_WARNING = (
    "WARNING: Static dependency routes and reachability results are derived solely from import statements. "
    "They indicate potential compile-time or static dependencies and do not reflect runtime execution sequence, "
    "call order, or dynamic control flow."
)

def generate_ai_json(report_data, detail_level="standard"):
    """Compile the JSON AI-oriented architecture packet from the normal report."""
    if detail_level not in ("compact", "standard", "full"):
        raise ValueError(f"Invalid detail_level: {detail_level}")

    # Build Header
    result = dict(CONTRACT_HEADER)
    result["project_name"] = report_data.get("project_name", "Unknown")
    result["scanned_at"] = report_data.get("scanned_at", "Unknown")
    result["static_reachability_warning"] = STATIC_REACHABILITY_WARNING

    # 1. Limitations (deterministic sorting)
    raw_limitations = report_data.get("limitations", [])
    limitations = []
    for lim in raw_limitations:
        limitations.append({
            "reason": lim.get("reason", ""),
            "claim_type": lim.get("claim_type", "gap"),
            "confidence": lim.get("confidence", "medium")
        })
    limitations.sort(key=lambda x: x["reason"])
    result["limitations"] = limitations

    # 2. Candidate Subsystems (deterministic sorting)
    raw_groups = report_data.get("candidate_subsystem_groups", [])
    subsystems = []
    for g in raw_groups:
        subsystems.append({
            "name": g.get("name", ""),
            "claim_type": g.get("claim_type", "inferred"),
            "confidence": g.get("confidence", "medium"),
            "member_count": len(g.get("member_files", [])),
            "structurally_ambiguous": g.get("structurally_ambiguous", False),
            "grouping_basis": sorted(g.get("grouping_basis", []))
        })
    subsystems.sort(key=lambda x: x["name"])
    result["candidate_subsystems"] = subsystems

    # 3. Top Inspection Targets (deterministic sorting)
    raw_targets = report_data.get("next_files_to_inspect", [])
    # Sort: score descending, then filepath ascending
    sorted_raw_targets = sorted(raw_targets, key=lambda x: (-x.get("score", 0), x.get("filepath", "")))
    
    # Slice to top 20 for compact/standard, keep all for full
    target_slice_limit = 20 if detail_level in ("compact", "standard") else len(sorted_raw_targets)
    targets = []
    for item in sorted_raw_targets[:target_slice_limit]:
        targets.append({
            "filepath": item.get("filepath", ""),
            "score": item.get("score", 0),
            "reasons": sorted(item.get("reasons", [])),
            "claim_type": item.get("claim_type", "inferred")
        })
    result["top_inspection_targets"] = targets

    # 4. Parse Gaps and Unresolved Findings (deterministic sorting)
    raw_errors = report_data.get("parse_errors", [])
    gaps = []
    for pe in raw_errors:
        gaps.append({
            "filepath": pe.get("filepath", ""),
            "error": pe.get("error", ""),
            "kind": pe.get("kind", "source_defect"),
            "claim_type": pe.get("claim_type", "gap")
        })
    gaps.sort(key=lambda x: x["filepath"])
    result["parse_gaps"] = gaps
    # Scanner limitations, kept apart from source findings: possible dependencies only.
    result["unresolved_imports"] = [
        {"source": u["source"], "import": u["import"], "candidates": u["candidates"],
         "kind": u["kind"], "claim_type": u["claim_type"]}
        for u in report_data.get("unresolved_imports", [])
    ]

    if detail_level in ("standard", "full"):
        # 5. Boundary Crossings (deterministic sorting, duplicate prevention)
        raw_routes = report_data.get("routes", [])
        crossings_set = set()
        for r in raw_routes:
            for bc in r.get("boundary_crossings", []):
                # bc is {"from": ..., "to": ..., "file": ...}
                crossings_set.add((bc.get("from", ""), bc.get("to", ""), bc.get("file", ""), bc.get("claim_type", "inferred")))
                
        boundary_crossings = []
        for item in crossings_set:
            boundary_crossings.append({
                "from": item[0],
                "to": item[1],
                "file": item[2],
                "claim_type": item[3]
            })
        # Deterministic sorting
        boundary_crossings.sort(key=lambda x: (x["from"], x["to"], x["file"]))
        result["boundary_crossings"] = boundary_crossings

        # 6. Route Summaries (deduplicating one-file routes, summarizing multi-file routes)
        single_file_paths = []
        multi_file_routes = []
        
        for r in raw_routes:
            files_list = r.get("route_files", [])
            entry = r.get("entrypoint", "")
            if len(files_list) == 1:
                single_file_paths.append((entry, r.get("claim_type", "inferred")))
            else:
                multi_file_routes.append({
                    "entrypoint": entry,
                    "claim_type": r.get("claim_type", "inferred"),
                    "route_length": len(files_list),
                    "advisory_next_step": r.get("next_file_to_inspect_in_route", ""),
                    "boundary_crossings_count": len(r.get("boundary_crossings", []))
                })
                
        # Group single file routes by claim_type (do not mix claim types!)
        grouped_single_routes = {}
        for path, claim in single_file_paths:
            grouped_single_routes.setdefault(claim, []).append(path)
            
        route_warnings = []
        for claim, paths in sorted(grouped_single_routes.items()):
            sorted_paths = sorted(list(set(paths)))
            route_warnings.append({
                "warning_type": "single_file_static_route",
                "claim_type": claim,
                "count": len(sorted_paths),
                "affected_paths": sorted_paths
            })
            
        multi_file_routes.sort(key=lambda x: x["entrypoint"])
        
        result["route_summaries"] = {
            "grouped_warnings": route_warnings,
            "multi_file_routes": multi_file_routes
        }

    if detail_level == "full":
        # 7. File inventory (deterministic sorting)
        raw_files = report_data.get("files", {})
        files_inv = []
        for filepath, info in raw_files.items():
            status_val = info.get("status", {}).get("status", "unresolved")
            status_claim = info.get("status", {}).get("claim_type", "inferred")
            files_inv.append({
                "filepath": filepath,
                "language": info.get("language", ""),
                "role_hint": info.get("role_hint", "unknown"),
                "inbound_count": info.get("inbound_count", 0),
                "outbound_count": info.get("outbound_count", 0),
                "status": status_val,
                "status_claim_type": status_claim,
                "inspection_score": info.get("inspection_score", 0)
            })
        files_inv.sort(key=lambda x: x["filepath"])
        result["files"] = files_inv

        # 8. Local Dependencies (deterministic sorting)
        raw_deps = report_data.get("local_dependencies", [])
        dependencies = []
        for d in raw_deps:
            dependencies.append({
                "source": d.get("source", ""),
                "target": d.get("target", ""),
                "claim_type": d.get("claim_type", "inferred")
            })
        dependencies.sort(key=lambda x: (x["source"], x["target"]))
        result["local_dependencies"] = dependencies

    return result

def generate_ai_markdown(ai_json, detail_level="standard"):
    """Format the compiled JSON AI packet into token-conscious, structured Markdown."""
    lines = []
    lines.append(f"# Code Atlas AI Architecture Report: {ai_json.get('project_name')}")
    lines.append("")
    lines.append(f"- **Contract:** {ai_json.get('contract')} (v{ai_json.get('contract_version')})")
    lines.append(f"- **Scanned At:** {ai_json.get('scanned_at')}")
    lines.append("")
    
    # Warning
    lines.append("## Static Reachability Warning")
    lines.append(f"> [!WARNING]")
    lines.append(f"> {ai_json.get('static_reachability_warning')}")
    lines.append("")

    # Limitations
    lines.append("## Limitations")
    for lim in ai_json.get("limitations", []):
        lines.append(f"- {lim['reason']} (Claim: `{lim['claim_type']}`, Confidence: `{lim['confidence']}`)")
    lines.append("")

    # Subsystems
    lines.append("## Subsystem Summaries")
    for g in ai_json.get("candidate_subsystems", []):
        ambig_str = " [AMBIGUOUS]" if g["structurally_ambiguous"] else ""
        basis_str = ", ".join(g["grouping_basis"])
        lines.append(f"- **{g['name']}**{ambig_str}")
        lines.append(f"  - Claim: `{g['claim_type']}`, Confidence: `{g['confidence']}`, Member Count: {g['member_count']}")
        lines.append(f"  - Grouping Basis: {basis_str}")
    lines.append("")

    # Top Inspection Targets
    lines.append(f"## Top Inspection Targets (Detail: {detail_level})")
    for idx, t in enumerate(ai_json.get("top_inspection_targets", []), 1):
        reasons_str = ", ".join(t["reasons"])
        lines.append(f"{idx}. `{t['filepath']}` (Score: **{t['score']}**)")
        lines.append(f"   - Claim: `{t['claim_type']}`, Reasons: {reasons_str}")
    lines.append("")

    # Gaps: source defects and scanner limitations are listed separately
    gaps = ai_json.get("parse_gaps", [])
    for title, kind in (("Source Defects (Python parser rejected the file)", "source_defect"),
                        ("Analysis Limitations: Files Atlas Could Not Read", "analysis_limitation")):
        lines.append(f"## {title}")
        rows = [g for g in gaps if g.get("kind", "source_defect") == kind]
        lines.extend([f"- `{g['filepath']}`: {g['error']}" for g in rows] or ["None."])
        lines.append("")
    lines.append("## Analysis Limitations: Unresolved Imports (possible dependencies, not counted)")
    lines.extend([f"- `{u['source']}` imports `{u['import']}`: candidates {', '.join(f'`{c}`' for c in u['candidates'])}"
                  for u in ai_json.get("unresolved_imports", [])] or ["None."])
    lines.append("")

    if detail_level in ("standard", "full"):
        # Boundary crossings
        lines.append("## Cross-Subsystem Boundaries")
        boundaries = ai_json.get("boundary_crossings", [])
        if not boundaries:
            lines.append("No boundaries crossed by static dependency paths.")
        else:
            for bc in boundaries:
                lines.append(f"- `{bc['file']}`: Boundary `{bc['from']}` ➔ `{bc['to']}` (Claim: `{bc['claim_type']}`)")
        lines.append("")

        # Route Summaries
        lines.append("## Route Summaries")
        rs = ai_json.get("route_summaries", {})
        
        lines.append("### Grouped Single-File Routes")
        grouped = rs.get("grouped_warnings", [])
        if not grouped:
            lines.append("None.")
        else:
            for group in grouped:
                lines.append(f"- Type: `{group['warning_type']}` (Claim: `{group['claim_type']}`, Count: {group['count']})")
                for path in group["affected_paths"]:
                    lines.append(f"  - `{path}`")
                    
        lines.append("")
        lines.append("### Multi-File Static Routes")
        multi = rs.get("multi_file_routes", [])
        if not multi:
            lines.append("None.")
        else:
            for route in multi:
                lines.append(f"- Entrypoint: `{route['entrypoint']}` (Claim: `{route['claim_type']}`)")
                lines.append(f"  - Length: {route['route_length']}, Advisory Next Step: `{route['advisory_next_step']}`")
                lines.append(f"  - Boundary Crossings Count: {route['boundary_crossings_count']}")
        lines.append("")

    if detail_level == "full":
        # Full Inventory
        lines.append("## Complete File Inventory")
        for f in ai_json.get("files", []):
            lines.append(f"- `{f['filepath']}`: status: `{f['status']}` (Claim: `{f['status_claim_type']}`), role: `{f['role_hint']}`, score: {f['inspection_score']}, in/out links: {f['inbound_count']}/{f['outbound_count']}")
        lines.append("")

        # Dependencies
        lines.append("## Dependency Links")
        for dep in ai_json.get("local_dependencies", []):
            lines.append(f"- `{dep['source']}` ➔ `{dep['target']}` (Claim: `{dep['claim_type']}`)")
        lines.append("")

    return "\n".join(lines)
