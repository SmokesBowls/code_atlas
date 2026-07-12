"""Report assembler module for resolving dependencies, formatting outputs, and integrating classification, grouping, routing, and limitations results."""

import os
import datetime
from code_atlas.core.status_classifier import classify_statuses
from code_atlas.core.capability_grouper import infer_subsystem_groups, get_role_hint
from code_atlas.core.ranking import calculate_inspection_rankings
from code_atlas.core.entrypoint_detector import detect_entrypoint
from code_atlas.core.router import calculate_dependency_routes

def _resolve_import_with_candidates(import_str, scanned_files, project_dir_name=None):
    """Return the resolution and candidate evidence for a local import."""
    scanned_files = set(scanned_files)

    def find_exact_candidates(parts):
        matches = set()
        for i in range(len(parts), 0, -1):
            candidate_path = "/".join(parts[:i])
            py_file = candidate_path + ".py"
            init_file = candidate_path + "/__init__.py"

            if py_file in scanned_files:
                matches.add(py_file)
            if init_file in scanned_files:
                matches.add(init_file)
            if matches:
                break
        return matches

    parts = import_str.split(".")
    exact_candidates = find_exact_candidates(parts)
    if project_dir_name and parts and parts[0] == project_dir_name:
        exact_candidates.update(find_exact_candidates(parts[1:]))

    if exact_candidates:
        candidates = exact_candidates
    else:
        candidates = set()
        for i in range(len(parts), 0, -1):
            module_path = "/".join(parts[:i])
            suffixes = [module_path + ".py"]
            if i == len(parts):
                suffixes.append(module_path + "/__init__.py")
            candidates = {
                filepath
                for filepath in scanned_files
                if any(
                    filepath == suffix or filepath.endswith("/" + suffix)
                    for suffix in suffixes
                )
            }
            if candidates:
                break

    ordered_candidates = sorted(candidates)
    if len(ordered_candidates) > 1:
        return "AMBIGUOUS", ordered_candidates
    if len(ordered_candidates) == 1:
        return ordered_candidates[0], ordered_candidates
    return None, []


def resolve_import_to_local_file(import_str, scanned_files, project_dir_name=None):
    """Resolve an import string to a local relative file path from scanned_files.

    Exact root-relative resolution has priority. If it fails, a complete-path
    suffix is accepted only when it identifies one scanned file. Ambiguous
    resolution returns ``AMBIGUOUS``.
    """
    resolved, _ = _resolve_import_with_candidates(
        import_str, scanned_files, project_dir_name
    )
    return resolved

def generate_report(project_dir, files_data, parse_errors):
    """Processes parsed files data to resolve dependencies, run status checks, grouping, and build report."""
    project_name = os.path.basename(os.path.abspath(project_dir))
    
    # Include both parsed files and files with parse errors in local dependency mapping
    scanned_files = set(files_data.keys()).union({pe["filepath"] for pe in parse_errors})

    local_dependencies = []
    
    # Track counts
    inbound_counts = {f: 0 for f in scanned_files}
    outbound_counts = {f: 0 for f in scanned_files}
    
    # 1. Resolve local dependencies and calculate counts
    for rel_path, info in files_data.items():
        raw_imports = info.get("raw_imports", [])
        resolved_for_file = set()
        
        for imp in raw_imports:
            resolved_file, resolution_candidates = _resolve_import_with_candidates(
                imp, scanned_files, project_name
            )
            if resolved_file == "AMBIGUOUS":
                parse_errors.append({
                    "filepath": rel_path,
                    "error": (
                        f"AmbiguousImportError: Import '{imp}' resolved to multiple "
                        f"local candidates: {resolution_candidates}."
                    )
                })
            elif resolved_file and resolved_file != rel_path:
                resolved_for_file.add(resolved_file)
        
        for target in sorted(list(resolved_for_file)):
            local_dependencies.append({
                "source": rel_path,
                "target": target,
                "type": "import",
                "claim_type": "inferred",
                "confidence": "high",
                "evidence": [
                    f"Import statement found in source code of {rel_path}",
                    f"Resolved import string to local path {target}"
                ]
            })
            inbound_counts[target] = inbound_counts.get(target, 0) + 1
            outbound_counts[rel_path] = outbound_counts.get(rel_path, 0) + 1

    # 2. Classify execution status for all scanned files
    statuses = classify_statuses(files_data, local_dependencies)

    # 3. Add status, role hints, inbound/outbound counts, entrypoint flags, and clean up temporary keys
    cleaned_files_data = {}
    for rel_path, info in files_data.items():
        file_info = dict(info)
        
        # Determine entrypoint using explicit heuristics
        is_entry, entry_evidence = detect_entrypoint(rel_path, file_info)
        file_info["is_entrypoint"] = is_entry
        
        file_info["role_hint"] = get_role_hint(rel_path, file_info)
        file_info["inbound_count"] = inbound_counts.get(rel_path, 0)
        file_info["outbound_count"] = outbound_counts.get(rel_path, 0)
        
        file_info["status"] = statuses.get(rel_path, {
            "status": "unresolved",
            "claim_type": "gap",
            "confidence": "low",
            "evidence": ["No status computed"]
        })
        
        # Remove internal parser attributes
        for k in ["_has_main_block", "_has_route_decorators", "_is_stub"]:
            if k in file_info:
                del file_info[k]
                
        cleaned_files_data[rel_path] = file_info

    # 4. Infer logical candidate subsystem groups (Milestone 3)
    candidate_subsystem_groups = infer_subsystem_groups(cleaned_files_data, local_dependencies)

    # 5. Generate next_files_to_inspect using new v2 multi-factor ranker (Milestone 4)
    inspect_list = calculate_inspection_rankings(cleaned_files_data, parse_errors, candidate_subsystem_groups)
    
    # Store computed scores back into cleaned_files_data so the router can access them
    score_map = {nf["filepath"]: nf["score"] for nf in inspect_list}
    for filepath, file_info in cleaned_files_data.items():
        file_info["inspection_score"] = score_map.get(filepath, 0)

    # 6. Trace dependency paths and group boundary crossings from entrypoints (Milestone 6)
    routes = calculate_dependency_routes(cleaned_files_data, parse_errors, local_dependencies, candidate_subsystem_groups)

    # 7. Format parse errors as gaps
    formatted_errors = []
    for pe in parse_errors:
        formatted_errors.append({
            "filepath": pe["filepath"],
            "error": pe["error"],
            "claim_type": "gap",
            "confidence": "high",
            "evidence": [
                "AST parser or dependency resolver flagged a structural gap"
            ]
        })

    # Sort local dependencies for deterministic outputs
    local_dependencies.sort(key=lambda d: (d["source"], d["target"]))

    # Extract payload candidates per file
    from code_atlas.core.payload_extractor import extract_payload_candidates
    candidates_by_file = {}
    for filepath in cleaned_files_data.keys():
        full_path = os.path.join(project_dir, filepath)
        if os.path.exists(full_path):
            candidates_by_file[filepath] = extract_payload_candidates(full_path)
        else:
            candidates_by_file[filepath] = {"producers": [], "consumers": [], "dataflows": []}

    # Call payload handoff diagnostics
    from code_atlas.core.payload_analyzer import analyze_payload_handoffs
    handoffs_data = analyze_payload_handoffs(
        cleaned_files_data,
        candidates_by_file,
        project_dir,
        local_dependencies=local_dependencies,
    )

    # Limitations definitions (claim_type: gap, confidence: high/medium, reason: string)
    limitations = [
        {
            "claim_type": "gap",
            "confidence": "high",
            "reason": "Static analysis cannot resolve dynamic imports (e.g. __import__, importlib, or dynamic string execution)."
        },
        {
            "claim_type": "gap",
            "confidence": "high",
            "reason": "Reflection and dynamic attribute retrieval may hide runtime dependencies."
        },
        {
            "claim_type": "gap",
            "confidence": "medium",
            "reason": "Static route paths are inferred from import syntax, not runtime-verified."
        },
        {
            "claim_type": "gap",
            "confidence": "high",
            "reason": "Namespace packages without __init__.py are supported, but ambiguous resolutions (multiple candidates matching the same import) are recorded as gaps."
        }
    ]

    report = {
        "project_name": project_name,
        "scanned_at": datetime.datetime.now(datetime.timezone.utc).isoformat().replace("+00:00", "Z"),
        "scan_roots": handoffs_data.get("scan_roots", []),
        "analysis_boundary": handoffs_data.get("analysis_boundary", ""),
        "limitations": limitations,
        "next_files_to_inspect": inspect_list,
        "candidate_subsystem_groups": candidate_subsystem_groups,
        "routes": routes,
        "files": cleaned_files_data,
        "local_dependencies": local_dependencies,
        "parse_errors": formatted_errors,
        "payload_handoffs": handoffs_data.get("payload_handoffs", []),
        "unresolved_payload_routes": handoffs_data.get("unresolved_payload_routes", [])
    }

    return report

def generate_markdown_report(report):
    """Generate a clean, human-readable Markdown summary from the JSON report dictionary."""
    lines = []
    lines.append(f"# Code Atlas Component Relationship Report: {report['project_name']}")
    lines.append("")
    lines.append(f"**Scanned at:** {report['scanned_at']}")
    lines.append("")
    
    # 1. Project Overview
    files = report["files"]
    errors = report["parse_errors"]
    
    # Entrypoints (boolean checked)
    entrypoints = [f for f, info in files.items() if info.get("is_entrypoint")]
                
    lines.append("## 1. Project Overview")
    lines.append(f"- **Total Files Scanned:** {len(files)}")
    lines.append(f"- **Total Parse Errors (Gaps):** {len(errors)}")
    lines.append(f"- **Detected Entrypoints:** {', '.join(entrypoints) if entrypoints else 'None'}")
    lines.append("")
    
    # Status distribution
    status_counts = {}
    for info in files.values():
        stat = info.get("status", {}).get("status", "unresolved")
        status_counts[stat] = status_counts.get(stat, 0) + 1
        
    lines.append("### Status Distribution")
    for stat in ["likely_active", "stubbed", "orphaned", "dormant", "unresolved"]:
        count = status_counts.get(stat, 0)
        lines.append(f"- **{stat.capitalize()}:** {count}")
    lines.append("- **Active (Runtime Confirmed):** 0")
    lines.append("")
    
    # 2. Candidate Subsystem Groups
    lines.append("## 2. Candidate Subsystem Groups")
    groups = report.get("candidate_subsystem_groups", [])
    if not groups:
        lines.append("No candidate subsystem groups detected.")
    else:
        for g in groups:
            ambig_str = "Yes" if g.get("structurally_ambiguous") else "No"
            lines.append(f"### {g['name']}")
            lines.append(f"- **Confidence:** {g['confidence'].capitalize()}")
            lines.append(f"- **Claim Type:** {g['claim_type']}")
            lines.append(f"- **Member Count:** {len(g['member_files'])}")
            lines.append(f"- **Structurally Ambiguous:** {ambig_str}")
            basis = ", ".join(g.get("grouping_basis", []))
            lines.append(f"- **Grouping Basis:** {basis}")
            lines.append("- **Evidence:**")
            for ev in g.get("evidence", []):
                lines.append(f"  - {ev}")
            lines.append("- **Member Files:**")
            for f in g.get("member_files", []):
                lines.append(f"  - `{f}`")
                
            inbound_files = g.get("inbound_interface_files", [])
            outbound_files = g.get("outbound_interface_files", [])
            
            lines.append(f"- **Inbound Interface Files ({len(inbound_files)}):**")
            for f in inbound_files:
                lines.append(f"  - `{f}`")
            lines.append(f"- **Outbound Interface Files ({len(outbound_files)}):**")
            for f in outbound_files:
                lines.append(f"  - `{f}`")
            lines.append("")
            
    # 3. Top Ranked Next Files to Inspect
    lines.append("## 3. Top Ranked Next Files to Inspect (Top 10)")
    next_files = report.get("next_files_to_inspect", [])[:10]
    if not next_files:
        lines.append("No inspection priorities computed.")
    else:
        for idx, nf in enumerate(next_files, 1):
            reasons = ", ".join(nf.get("reasons", []))
            lines.append(f"{idx}. `{nf['filepath']}` (Score: **{nf['score']}**)")
            lines.append(f"   - **Reasons:** {reasons}")
            lines.append("   - **Evidence:**")
            for ev in nf.get("evidence", []):
                lines.append(f"     - {ev}")
            lines.append("")
                
    # 4. Path and Dependency Routes
    lines.append("## 4. Path and Dependency Routes")
    lines.append("These paths describe **static dependency routes** determined by import statements. The file order reflects the **dependency traversal order** (DFS) from the entrypoint, which is not a proven runtime execution call order. Suggested inspection order is **advisory only**.")
    lines.append("")
    routes = report.get("routes", [])
    if not routes:
        lines.append("No static dependency routes computed.")
    else:
        for r in routes:
            lines.append(f"### Static Route from entrypoint: `{r['entrypoint']}`")
            lines.append(f"- **Advisory Next File to Inspect in Route:** `{r['next_file_to_inspect_in_route']}`")
            lines.append("- **Dependency Traversal Flow:**")
            for file in r["route_files"]:
                flag_str = ""
                flags = []
                if file in r["parse_error_files"]:
                    flags.append("PARSE ERROR")
                if file in r["stubbed_files"]:
                    flags.append("STUB")
                if file in r["unresolved_files"]:
                    flags.append("UNRESOLVED")
                if flags:
                    flag_str = f" [{', '.join(flags)}]"
                
                # Check if this file has a boundary crossing associated with it
                crossing_str = ""
                for bc in r["boundary_crossings"]:
                    if bc["file"] == file:
                        crossing_str = f" ➔ **Inferred Boundary Crossing:** ({bc['from']} ➔ {bc['to']})"
                        break
                        
                lines.append(f"  - `{file}`{flag_str}{crossing_str}")
            lines.append("")

    # 5. Limitations
    lines.append("## 5. Limitations")
    for lim in report.get("limitations", []):
        lines.append(f"- **{lim['reason']}**")
        lines.append(f"  - **Claim Type:** {lim['claim_type']}")
        lines.append(f"  - **Confidence:** {lim['confidence'].capitalize()}")
        lines.append("")

    return "\n".join(lines)
