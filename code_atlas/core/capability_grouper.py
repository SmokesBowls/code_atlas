"""Module for inferring candidate subsystem groups based on directory layout, role hints, and dependency coupling."""

import os
import re


def get_role_signals(filepath, info):
    """Return the observable signals used by role classification."""
    filename = os.path.basename(filepath)
    filepath_lower = filepath.lower()
    filename_lower = filename.lower()
    filename_tokens = set(
        token for token in re.split(r"[^a-z0-9]+", os.path.splitext(filename_lower)[0])
        if token
    )
    raw_imports = info.get("raw_imports", [])

    return {
        "package_init": filename == "__init__.py",
        "test_path": (
            filename_lower.startswith("test_")
            or filename_lower.endswith("_test.py")
            or "tests/" in filepath_lower
            or "tests\\" in filepath_lower
            or "/tests" in filepath_lower
            or "\\tests" in filepath_lower
        ),
        "argparse_import": "argparse" in raw_imports,
        "main_block": bool(info.get("_has_main_block")),
        "cli_filename_tokens": sorted(
            filename_tokens & {"cli", "scanner", "command"}
        ),
        "config_path_terms": sorted(
            term for term in ("config", "settings", "setup", "env")
            if term in filepath_lower
        ),
        "model_path_terms": sorted(
            term for term in ("model", "schema", "db", "database")
            if term in filepath_lower
        ),
        "utility_path_terms": sorted(
            term for term in ("util", "helper", "tool", "common")
            if term in filepath_lower
        ),
    }


def get_role_hint(filepath, info):
    """Assign a role hint to a file based on naming and structural heuristics."""
    signals = get_role_signals(filepath, info)
    if signals["package_init"]:
        return "package_init"
    if signals["test_path"]:
        return "test"
    if (
        signals["argparse_import"]
        or signals["main_block"]
        or signals["cli_filename_tokens"]
    ):
        return "cli"
    if signals["config_path_terms"]:
        return "config"
    if signals["model_path_terms"]:
        return "model"
    if signals["utility_path_terms"]:
        return "utility"
    return "unknown"

def get_group_name(dir_seed):
    """Generate a readable subsystem name from a directory path seed."""
    if not dir_seed or dir_seed == ".":
        return "Root Components"
    
    parts = dir_seed.split(os.sep)
    # Use the last directory name for naming
    name = parts[-1]
    if name.lower() in ("tests", "test"):
        return "Testing Suite"
    if name.lower() in ("utils", "helpers"):
        return "Utilities Subsystem"
        
    return f"{name.capitalize()} Subsystem"

def infer_subsystem_groups(files_data, local_dependencies):
    """Analyze files and dependencies statically to infer logical candidate subsystem groups.
    
    Returns:
        A list of candidate subsystem group dictionaries.
    """
    # 1. Enrich files with role hints for analysis
    enriched_files = {}
    for filepath, info in files_data.items():
        enriched_files[filepath] = {
            "role_hint": info.get("role_hint") or get_role_hint(filepath, info),
            "raw_imports": info.get("raw_imports", [])
        }

    # 2. Map files to initial directory seeds
    dir_seeds = {}
    for filepath in files_data:
        dir_name = os.path.dirname(filepath)
        # Normalize directory path
        dir_name = dir_name.replace(os.sep, '/')
        if not dir_name:
            dir_name = "."
        if dir_name not in dir_seeds:
            dir_seeds[dir_name] = []
        dir_seeds[dir_name].append(filepath)

    # 3. Track final groups as: group_name -> set of file paths
    groups = {}
    
    # Pre-populate specific refined groups
    groups["Testing Suite"] = set()
    groups["Shared Utility Subsystem"] = set()

    # Determine cross-cutting utilities
    utility_inbound_seeds = {}
    for dep in local_dependencies:
        src = dep["source"]
        tgt = dep["target"]
        if enriched_files.get(tgt, {}).get("role_hint") == "utility":
            src_dir = os.path.dirname(src).replace(os.sep, '/') or "."
            if tgt not in utility_inbound_seeds:
                utility_inbound_seeds[tgt] = set()
            utility_inbound_seeds[tgt].add(src_dir)

    shared_utilities = set()
    for tgt, seeds in utility_inbound_seeds.items():
        if len(seeds) >= 2:
            shared_utilities.add(tgt)
    if len(shared_utilities) < 2:
        shared_utilities.clear()

    # Preserve a directory toolbox before cross-boundary utility consolidation.
    # Package initializers are neutral, and consumers are distinct source files.
    toolbox_dir_seeds = set()
    for dir_seed, filepaths in dir_seeds.items():
        eligible_members = [
            filepath for filepath in filepaths
            if enriched_files[filepath]["role_hint"] != "package_init"
        ]
        utility_members = [
            filepath for filepath in eligible_members
            if enriched_files[filepath]["role_hint"] == "utility"
        ]
        external_consumers = {
            dep["source"] for dep in local_dependencies
            if dep["target"] in filepaths and dep["source"] not in filepaths
        }
        utility_ratio = (
            len(utility_members) / len(eligible_members)
            if eligible_members else 0.0
        )
        if (
            len(utility_members) >= 2
            and utility_ratio >= (2 / 3)
            and len(external_consumers) >= 2
        ):
            toolbox_dir_seeds.add(dir_seed)

    # Distribute files to groups
    for dir_seed, filepaths in dir_seeds.items():
        for filepath in filepaths:
            role = enriched_files[filepath]["role_hint"]
            
            if role == "test":
                groups["Testing Suite"].add(filepath)
            elif dir_seed in toolbox_dir_seeds:
                gname = get_group_name(dir_seed)
                if gname not in groups:
                    groups[gname] = set()
                groups[gname].add(filepath)
            elif filepath in shared_utilities:
                groups["Shared Utility Subsystem"].add(filepath)
            else:
                # Keep in directory seed group
                gname = get_group_name(dir_seed)
                if gname not in groups:
                    groups[gname] = set()
                groups[gname].add(filepath)

    # Clean up empty groups
    groups = {name: sorted(list(members)) for name, members in groups.items() if members}

    # 4. Analyze cohesion, coupling, and build group objects
    candidate_groups = []
    
    for gname, members in groups.items():
        member_set = set(members)
        
        # Calculate edge counts
        internal_edges = 0
        external_inbound = set()
        external_outbound = set()
        external_outbound_by_source = {}
        
        for dep in local_dependencies:
            src = dep["source"]
            tgt = dep["target"]
            
            if src in member_set and tgt in member_set:
                internal_edges += 1
            elif src in member_set and tgt not in member_set:
                # Outbound dependency to an external file
                external_outbound.add(tgt)
                external_outbound_by_source.setdefault(src, set()).add(tgt)
            elif src not in member_set and tgt in member_set:
                # Inbound dependency from an external file
                external_inbound.add(src)

        external_edges = len(external_outbound) + len(external_inbound)

        # Toolbox cohesion is expressed by serving multiple external consumers,
        # not by utilities importing one another. Package initializers are neutral.
        eligible_members = [
            filepath for filepath in members
            if enriched_files.get(filepath, {}).get("role_hint") != "package_init"
        ]
        utility_members = [
            filepath for filepath in eligible_members
            if enriched_files.get(filepath, {}).get("role_hint") == "utility"
        ]
        utility_ratio = (
            len(utility_members) / len(eligible_members)
            if eligible_members else 0.0
        )
        toolbox_exempt = utility_ratio >= (2 / 3) and len(external_inbound) >= 2

        coordinator_members = [
            filepath
            for filepath in members
            if os.path.splitext(os.path.basename(filepath))[0].endswith("_control_center")
            or os.path.splitext(os.path.basename(filepath))[0] == "control_center"
        ]
        coordinator_outbound_count = sum(
            len(external_outbound_by_source.get(filepath, set()))
            for filepath in coordinator_members
        )
        total_outbound_count = sum(
            len(targets) for targets in external_outbound_by_source.values()
        )
        coordinator_outbound_ratio = (
            coordinator_outbound_count / total_outbound_count
            if total_outbound_count else 0.0
        )
        coordinator_exempt = (
            coordinator_outbound_count >= 3
            and coordinator_outbound_ratio >= (2 / 3)
        )

        # Heuristic rules for Structural Ambiguity & Confidence
        structurally_ambiguous = False
        confidence = "high"
        
        if gname != "Testing Suite":
            if toolbox_exempt:
                confidence = "medium"
            elif coordinator_exempt:
                confidence = "medium"
            elif len(members) > 1 and internal_edges == 0 and external_edges > 0:
                structurally_ambiguous = True
                confidence = "low"
            elif external_edges > 2 * internal_edges and internal_edges <= 1:
                structurally_ambiguous = True
                confidence = "medium"

        # Evidence generation
        evidence = []
        grouping_basis = []
        
        if gname == "Testing Suite":
            evidence.append("Consolidated based on test role hints across directories")
            grouping_basis = ["seed: test_role_hint", "refined_by: role_consolidation"]
        elif gname == "Shared Utility Subsystem":
            evidence.append("Consolidated utility files imported by multiple directory seeds")
            grouping_basis = ["seed: utility_role_hint", "refined_by: cross_boundary_consolidation"]
        else:
            seed_dirs = {os.path.dirname(f).replace(os.sep, '/') or "." for f in members}
            dir_str = ", ".join(sorted(list(seed_dirs)))
            evidence.append(f"Files share directory structure: '{dir_str}'")
            grouping_basis = [
                "seed: directory_structure",
                "refined_by: dependency_cohesion"
            ]

        evidence.append(f"Internal cohesion: {internal_edges} internal dependency edges")
        evidence.append(f"Cross-group coupling: {external_edges} external dependency edges")

        if toolbox_exempt:
            evidence.append(
                "Toolbox cohesion: utility-dominated group "
                f"({len(utility_members)}/{len(eligible_members)} eligible members) "
                f"serves {len(external_inbound)} distinct external consumers; "
                "internal dependency edges are not required"
            )
            grouping_basis.append("refined_by: toolbox_external_consumers")

        if coordinator_exempt:
            evidence.append(
                "Coordinator cohesion: explicitly named control center emits "
                f"{coordinator_outbound_count}/{total_outbound_count} outbound edges "
                f"({coordinator_outbound_ratio:.1%}); internal dependency edges are not required"
            )
            grouping_basis.append("refined_by: coordinator_outbound_concentration")

        if structurally_ambiguous:
            evidence.append("Weak internal cohesion relative to strong cross-group coupling; marked as structurally ambiguous")

        candidate_groups.append({
            "name": gname,
            "confidence": confidence,
            "claim_type": "inferred",
            "evidence": evidence,
            "member_files": members,
            "inbound_interface_files": sorted(list(external_inbound)),
            "outbound_interface_files": sorted(list(external_outbound)),
            "structurally_ambiguous": structurally_ambiguous,
            "internal_edge_count": internal_edges,
            "external_edge_count": external_edges,
            "grouping_basis": grouping_basis
        })

    # Sort groups alphabetically by name
    candidate_groups.sort(key=lambda g: g["name"])
    
    return candidate_groups
