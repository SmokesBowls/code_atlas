"""Module for classifying the execution status of project files based on reachability and AST hints."""

import os
from code_atlas.core.entrypoint_detector import detect_entrypoint

def classify_statuses(files_data, local_dependencies):
    """Analyze the file registry and dependency graph to assign execution statuses.
    
    Statuses:
        - likely_active: Static entrypoint or reachable from static entrypoint.
        - stubbed: Indicated by TODO/pass/NotImplementedError.
        - dormant: Isolated subgraphs (not imported, but imports others) or unreachable loops.
        - orphaned: Standalone isolated files.
        - unresolved: Default fallback.
    """
    statuses = {}
    
    # Build graph mappings
    adj_list = {f: set() for f in files_data}
    inbound_list = {f: set() for f in files_data}
    for dep in local_dependencies:
        src = dep["source"]
        tgt = dep["target"]
        if src in adj_list and tgt in adj_list:
            adj_list[src].add(tgt)
            inbound_list[tgt].add(src)
            
    # Step 0: Identify stubbed files first so reachability doesn't override them
    for filepath, info in files_data.items():
        if info.get("_is_stub"):
            statuses[filepath] = {
                "status": "stubbed",
                "claim_type": "confirmed",
                "confidence": "high",
                "evidence": [
                    "File contains TODO/FIXME annotations, raises NotImplementedError, or contains only empty structures"
                ]
            }
            
    # Step 1: Identify static entrypoints and test files (likely_active roots)
    active_roots = set()
    for filepath, info in files_data.items():
        if filepath in statuses:
            continue
            
        is_entry, entry_evidence = detect_entrypoint(filepath, info)
        
        # Check if test file based on name and directory
        filename = os.path.basename(filepath)
        is_test = (
            filename.startswith("test_") or 
            filename.endswith("_test.py") or 
            "tests/" in filepath or 
            "/tests" in filepath
        )
        
        if is_entry:
            active_roots.add(filepath)
            statuses[filepath] = {
                "status": "likely_active",
                "claim_type": "confirmed",
                "confidence": "high",
                "evidence": entry_evidence
            }
        elif is_test:
            active_roots.add(filepath)
            statuses[filepath] = {
                "status": "likely_active",
                "claim_type": "inferred",
                "confidence": "high",
                "evidence": ["Test file detected by name/path pattern"]
            }

    # Step 2: Reachability traversal (BFS) to identify other likely_active files
    queue = sorted(active_roots)  # sorted: set order varies with PYTHONHASHSEED
    visited = set(active_roots)
    imported_by = {}
    
    while queue:
        current = queue.pop(0)
        for neighbor in sorted(adj_list[current]):
            if neighbor not in visited:
                visited.add(neighbor)
                imported_by[neighbor] = current
                queue.append(neighbor)
                
    for filepath in visited:
        if filepath not in active_roots:
            # Stubs retain their stubbed status
            if filepath in statuses:
                continue
            parent = imported_by[filepath]
            statuses[filepath] = {
                "status": "likely_active",
                "claim_type": "inferred",
                "confidence": "high",
                "evidence": [
                    f"Imported by likely_active file: '{parent}'"
                ]
            }

    # Step 3: Classify remaining unreachable files
    for filepath, info in files_data.items():
        if filepath in statuses:
            continue
            
        # Sibling resolution for package __init__.py files
        if os.path.basename(filepath) == "__init__.py":
            dir_path = os.path.dirname(filepath)
            siblings_active = False
            active_sibling = None
            for other_file in files_data:
                if other_file != filepath and other_file.startswith(dir_path):
                    if other_file in visited:
                        siblings_active = True
                        active_sibling = other_file
                        break
            if siblings_active:
                statuses[filepath] = {
                    "status": "likely_active",
                    "claim_type": "inferred",
                    "confidence": "medium",
                    "evidence": [
                        f"Package initialization file for directory containing likely_active file: '{active_sibling}'"
                    ]
                }
                continue

        # Inbound and outbound checks for dormant vs orphaned
        inbound_count = len(inbound_list[filepath])
        outbound_count = len(adj_list[filepath])
        
        if inbound_count == 0:
            if outbound_count > 0:
                statuses[filepath] = {
                    "status": "dormant",
                    "claim_type": "inferred",
                    "confidence": "medium",
                    "evidence": [
                        "No inbound local imports found, but file imports other local modules (unused subsystem entrypoint)"
                    ]
                }
            else:
                statuses[filepath] = {
                    "status": "orphaned",
                    "claim_type": "inferred",
                    "confidence": "high",
                    "evidence": [
                        "Isolated standalone file with no inbound or outbound local dependencies in the project"
                    ]
                }
        else:
            statuses[filepath] = {
                "status": "dormant",
                "claim_type": "inferred",
                "confidence": "high",
                "evidence": [
                    f"File has local inbound imports ({inbound_count}) but is not reachable from any likely_active entrypoint"
                ]
            }
            
    # Fallback default
    for filepath in files_data:
        if filepath not in statuses:
            statuses[filepath] = {
                "status": "unresolved",
                "claim_type": "gap",
                "confidence": "low",
                "evidence": [
                    "Scanner could not determine the execution status based on static analysis heuristics"
                ]
            }
            
    return statuses
