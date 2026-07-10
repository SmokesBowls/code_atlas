"""Module for inferring candidate subsystem groups based on directory layout, role hints, and dependency coupling."""

import os

def get_role_hint(filepath, info):
    """Assign a role hint to a file based on naming and structural heuristics."""
    filename = os.path.basename(filepath)
    if filename == "__init__.py":
        return "package_init"

    filepath_lower = filepath.lower()
    filename_lower = filename.lower()

    # Test file check
    if (
        filename_lower.startswith("test_") or 
        filename_lower.endswith("_test.py") or 
        "tests/" in filepath_lower or 
        "tests\\" in filepath_lower or
        "/tests" in filepath_lower or
        "\\tests" in filepath_lower
    ):
        return "test"

    # CLI check
    raw_imports = info.get("raw_imports", [])
    if (
        "argparse" in raw_imports or 
        info.get("_has_main_block") or
        any(x in filename_lower for x in ["cli", "scanner", "command"])
    ):
        return "cli"

    # Config check
    if any(x in filepath_lower for x in ["config", "settings", "setup", "env"]):
        return "config"

    # Model check
    if any(x in filepath_lower for x in ["model", "schema", "db", "database"]):
        return "model"

    # Utility check
    if any(x in filepath_lower for x in ["util", "helper", "tool", "common"]):
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
            "role_hint": get_role_hint(filepath, info),
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

    # Distribute files to groups
    for dir_seed, filepaths in dir_seeds.items():
        for filepath in filepaths:
            role = enriched_files[filepath]["role_hint"]
            
            if role == "test":
                groups["Testing Suite"].add(filepath)
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
        
        for dep in local_dependencies:
            src = dep["source"]
            tgt = dep["target"]
            
            if src in member_set and tgt in member_set:
                internal_edges += 1
            elif src in member_set and tgt not in member_set:
                # Outbound dependency to an external file
                external_outbound.add(tgt)
            elif src not in member_set and tgt in member_set:
                # Inbound dependency from an external file
                external_inbound.add(src)

        external_edges = len(external_outbound) + len(external_inbound)

        # Heuristic rules for Structural Ambiguity & Confidence
        structurally_ambiguous = False
        confidence = "high"
        
        if gname == "Shared Utility Subsystem":
            # Junk drawer trap rule: require at least 2 internal edges
            if internal_edges < 2:
                structurally_ambiguous = True
                confidence = "low"
        elif gname != "Testing Suite":
            if len(members) > 1 and internal_edges == 0 and external_edges > 0:
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
            if structurally_ambiguous:
                evidence.append("Junk drawer trap: shared utility group contains low internal cohesion (< 2 internal edges)")
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

        if structurally_ambiguous and gname != "Shared Utility Subsystem":
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
