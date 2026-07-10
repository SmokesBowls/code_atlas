"""Module for tracing static dependency routes from entrypoints and mapping subsystem boundary crossings."""

def calculate_dependency_routes(files_data, parse_errors, local_dependencies, candidate_groups):
    """Trace ordered static dependency paths from each entrypoint and analyze their properties.
    
    Returns:
        A list of route dictionaries matching the strict M6 schema:
        [
            {
                "entrypoint": "main.py",
                "claim_type": "inferred",
                "confidence": "high",
                "evidence": [...],
                "route_files": [...],
                "boundary_crossings": [{"from": "...", "to": "...", "file": "..."}],
                "stubbed_files": [...],
                "unresolved_files": [...],
                "parse_error_files": [...],
                "next_file_to_inspect_in_route": "..."
            }
        ]
    """
    # 1. Identify entrypoints
    entrypoints = [f for f, info in files_data.items() if info.get("is_entrypoint")]
    
    # 2. Build adjacency list of dependencies (source -> list of targets)
    adj = {f: [] for f in files_data}
    parse_errors_dict = {pe["filepath"]: pe["error"] for pe in parse_errors}
    
    # Also initialize key in adjacency list for broken files
    for filepath in parse_errors_dict:
        adj[filepath] = []
        
    for dep in local_dependencies:
        src = dep["source"]
        tgt = dep["target"]
        if src in adj:
            adj[src].append(tgt)

    # 3. Map each file to its candidate group
    file_to_group = {}
    for group in candidate_groups:
        gname = group["name"]
        for f in group["member_files"]:
            file_to_group[f] = gname

    routes = []
    
    for entrypoint in sorted(entrypoints):
        visited_steps = []
        visited_set = set()
        
        # DFS traversal to trace ordered imports
        def dfs(node, parent_node):
            if node in visited_set:
                return
            visited_set.add(node)
            
            gname = file_to_group.get(node, "unknown")
            parent_gname = file_to_group.get(parent_node) if parent_node else None
            
            boundary_crossing = None
            if parent_gname and parent_gname != gname:
                boundary_crossing = {
                    "from": parent_gname,
                    "to": gname,
                    "file": node
                }
                
            file_info = files_data.get(node, {})
            status_info = file_info.get("status", {})
            status = status_info.get("status", "unresolved")
            
            is_stub = (status == "stubbed")
            is_unresolved = (status == "unresolved")
            has_parse_error = (node in parse_errors_dict)
            
            score = file_info.get("inspection_score", 0)
            if has_parse_error:
                score = 100
                
            visited_steps.append({
                "filepath": node,
                "score": score,
                "boundary_crossing": boundary_crossing,
                "is_stub": is_stub,
                "is_unresolved": is_unresolved,
                "has_parse_error": has_parse_error
            })
            
            # Recurse for dependencies (neighbors), sorted alphabetically for determinism
            for neighbor in sorted(adj.get(node, [])):
                dfs(neighbor, node)
                
        dfs(entrypoint, None)
        
        # Build lists matching the requested M6 schema
        route_files = [s["filepath"] for s in visited_steps]
        boundary_crossings = [s["boundary_crossing"] for s in visited_steps if s["boundary_crossing"] is not None]
        stubbed_files = [s["filepath"] for s in visited_steps if s["is_stub"]]
        unresolved_files = [s["filepath"] for s in visited_steps if s["is_unresolved"]]
        parse_error_files = [s["filepath"] for s in visited_steps if s["has_parse_error"]]
        
        # Find next file to inspect inside this specific route (excluding entrypoint if possible)
        inspectable_files = [s for s in visited_steps if s["filepath"] != entrypoint]
        if not inspectable_files and visited_steps:
            inspectable_files = visited_steps
            
        if inspectable_files:
            # Sort descending by inspection score, then alphabetically by path
            inspectable_files.sort(key=lambda s: (-s["score"], s["filepath"]))
            next_file = inspectable_files[0]["filepath"]
        else:
            next_file = None
            
        routes.append({
            "entrypoint": entrypoint,
            "claim_type": "inferred",
            "confidence": "high",
            "evidence": [
                "DFS traversal from entrypoint",
                "reachable via import chain"
            ],
            "route_files": route_files,
            "boundary_crossings": boundary_crossings,
            "stubbed_files": stubbed_files,
            "unresolved_files": unresolved_files,
            "parse_error_files": parse_error_files,
            "next_file_to_inspect_in_route": next_file
        })
        
    return routes
