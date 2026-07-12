"""Payload Handoff Diagnostics Analyzer.

Links payload candidates across files, validates connectivity, enforces scan boundaries,
and structures output according to the strict Milestone 9 contract.
"""

import os

def analyze_payload_handoffs(
    files_data,
    candidates_by_file,
    workspace_dir,
    local_dependencies=None,
):
    """Link payload candidates across scanned files and classify connections or boundary gaps."""
    workspace_dir = os.path.abspath(workspace_dir)
    scan_roots = [workspace_dir]
    analysis_boundary = f"Files under {workspace_dir}"
    local_dependencies = local_dependencies or []
    dependency_targets = {}
    for dependency in local_dependencies:
        dependency_targets.setdefault(dependency["source"], set()).add(
            dependency["target"]
        )
    
    # Map exported functions to their defining files
    exported_functions = {}
    for rel_path, cands in candidates_by_file.items():
        for prod in cands.get("producers", []):
            if prod.get("candidate_type") == "payload_candidate":
                exported_functions.setdefault(prod["function"], []).append(rel_path)
                
    # Helper to resolve defining modules
    def file_defines_function(file_path, func_name):
        file_data = files_data.get(file_path, {})
        if any(func.get("name") == func_name for func in file_data.get("functions", [])):
            return True
        file_candidates = candidates_by_file.get(file_path, {})
        return any(
            candidate.get("function") == func_name
            for category in ("producers", "consumers")
            for candidate in file_candidates.get(category, [])
        )

    def resolve_defining_file(func_name, caller_rel_path):
        caller_data = files_data.get(caller_rel_path, {})
        local_funcs = [f["name"] for f in caller_data.get("functions", [])]
        if func_name in local_funcs:
            return caller_rel_path

        resolved_targets = sorted(
            target
            for target in dependency_targets.get(caller_rel_path, set())
            if file_defines_function(target, func_name)
        )
        if len(resolved_targets) == 1:
            return resolved_targets[0]
        if len(resolved_targets) > 1:
            return None

        imports = caller_data.get("raw_imports", [])
        for imp in imports:
            parts = imp.split('.')
            if parts[-1] == func_name:
                module_name = ".".join(parts[:-1])
                for p in files_data.keys():
                    if p.replace('.py', '').replace('/', '.').replace('\\', '.').endswith(module_name):
                        return p
            elif len(parts) == 1 and parts[0] == func_name:
                for p in files_data.keys():
                    if p.replace('.py', '').replace('/', '.').replace('\\', '.').endswith(func_name):
                        return p
                        
        candidates = exported_functions.get(func_name, [])
        if len(candidates) == 1:
            return candidates[0]
        elif len(candidates) > 1:
            return None
        return None

    # Recursive utilization tracer
    def trace_param_utilization(file_path, func_name, param_name, visited=None):
        if visited is None:
            visited = set()
        state_key = (file_path, func_name, param_name)
        if state_key in visited:
            return set(), set(), False
        visited.add(state_key)
        
        cands = candidates_by_file.get(file_path, {})
        consumers = cands.get("consumers", [])
        cons = next((c for c in consumers if c["function"] == func_name), None)
        if not cons:
            return set(), set(), False
            
        util = cons.get("param_utilization", {}).get(param_name, {})
        accessed = set(util.get("accessed_keys", []))
        forwarded = set(util.get("forwarded_to", []))
        is_structural = util.get("structural_consumption", False)
        
        for callee in list(forwarded):
            callee_file = resolve_defining_file(callee, file_path)
            if callee_file:
                callee_cands = candidates_by_file.get(callee_file, {})
                callee_consumers = callee_cands.get("consumers", [])
                callee_cons = next((c for c in callee_consumers if c["function"] == callee), None)
                if callee_cons:
                    params = list(callee_cons.get("param_utilization", {}).keys())
                    target_param = None
                    if param_name in params:
                        target_param = param_name
                    elif len(params) == 1:
                        target_param = params[0]
                    elif len(params) > 1:
                        for p in params:
                            if p in param_name or param_name in p:
                                target_param = p
                                break
                        if not target_param:
                            target_param = params[0]
                            
                    if target_param:
                        sub_accessed, sub_forwarded, sub_struct = trace_param_utilization(
                            callee_file, callee, target_param, visited
                        )
                        accessed.update(sub_accessed)
                        forwarded.update(sub_forwarded)
                        is_structural = is_structural or sub_struct
                        
        return accessed, forwarded, is_structural

    def resolve_written_keys_and_contracts(prod, w_file, path_key):
        writes_detailed = prod.get("file_writes_detailed", [])
        write_info = None
        for w in writes_detailed:
            if w["filename"] == path_key or os.path.basename(w["filename"]) == os.path.basename(path_key):
                write_info = w
                break
        if not write_info:
            return [], []
            
        keys_info = write_info.get("keys_info", [])
        if isinstance(keys_info, list):
            return keys_info, prod.get("contract_identifiers", [])
            
        if isinstance(keys_info, dict):
            if "from_call" in keys_info:
                callee = keys_info["from_call"]
                callee_file = resolve_defining_file(callee, w_file)
                if callee_file:
                    callee_cands = candidates_by_file.get(callee_file, {})
                    callee_prod = next((p for p in callee_cands.get("producers", []) if p["function"] == callee), None)
                    if callee_prod:
                        return callee_prod.get("returned_keys", []), callee_prod.get("contract_identifiers", [])
            elif "from_call_key" in keys_info:
                callee, key_name = keys_info["from_call_key"]
                callee_file = resolve_defining_file(callee, w_file)
                if callee_file:
                    callee_cands = candidates_by_file.get(callee_file, {})
                    callee_prod = next((p for p in callee_cands.get("producers", []) if p["function"] == callee), None)
                    if callee_prod:
                        struct = callee_prod.get("returned_dict_structure", {})
                        all_cid = callee_prod.get("contract_identifiers", [])
                        resolved_cid = []
                        for cid in all_cid:
                            if key_name in cid or cid in key_name:
                                resolved_cid.append(cid)
                        if not resolved_cid:
                            resolved_cid = all_cid
                        if key_name in struct:
                            return struct[key_name], resolved_cid
        return [], []

    handoffs = []
    unresolved_routes = []
    
    matched_producers = set()
    matched_consumers = set()
    matched_file_writes = set()
    matched_file_reads = set()

    # Generic limitations block for static diagnostic entries
    standard_limitations = [
        "Alias mutation is not tracked statically",
        "Container insertion/retrieval is not traced",
        "State tracking across class attributes is omitted",
        "Callback triggers and reflection are unsupported"
    ]

    # 1. Match Function-level connections (Assignments and Nested Calls)
    for rel_path, cands in candidates_by_file.items():
        dataflows = cands.get("dataflows", [])
        for flow in dataflows:
            prod_func = flow["producer_function"]
            cons_func = flow["consumer_function"]
            destructured_key = flow.get("destructured_key")
            
            prod_file = resolve_defining_file(prod_func, rel_path)
            cons_file = resolve_defining_file(cons_func, rel_path)
            
            # If function define file isn't in scanned path, it's not resolved in boundary
            if not prod_file or not cons_file:
                continue
                
            prod_cands = candidates_by_file[prod_file]
            producer = next((p for p in prod_cands.get("producers", []) if p["function"] == prod_func), None)
            
            # Verify candidate type (utility dictionaries or configuration tables are ignored)
            if not producer or producer.get("candidate_type") != "payload_candidate":
                continue
                
            cons_cands = candidates_by_file[cons_file]
            consumer = next((c for c in cons_cands.get("consumers", []) if c["function"] == cons_func), None)
            if not consumer:
                continue
                
            # Connect
            params_util = consumer.get("param_utilization", {})
            matched_param = None
            
            best_score = -1
            returned_keys_set = set(producer.get("returned_keys", []))
            
            for param_name, util in params_util.items():
                score = 0
                if param_name in prod_func or prod_func in param_name:
                    score += 5
                param_accessed = set(util.get("accessed_keys", []))
                shared_keys = returned_keys_set & param_accessed
                score += len(shared_keys) * 2
                
                if score > best_score:
                    best_score = score
                    matched_param = param_name
                    
            if not matched_param and params_util:
                matched_param = list(params_util.keys())[0]
                
            status = "connected"
            unutilized_keys = []
            utilized_keys = set()
            
            if matched_param:
                accessed, _, is_struct = trace_param_utilization(cons_file, cons_func, matched_param)
                if destructured_key:
                    accessed.add(destructured_key)
                    
                if is_struct:
                    status = "connected"
                    utilized_keys = returned_keys_set
                else:
                    if returned_keys_set:
                        utilized_keys = returned_keys_set & accessed
                        if len(utilized_keys) == len(returned_keys_set):
                            status = "connected"
                        elif len(utilized_keys) >= 1:
                            status = "connected_partial"
                            unutilized_keys = sorted(list(returned_keys_set - utilized_keys))
                        else:
                            status = "connected_unused"
                            unutilized_keys = sorted(list(returned_keys_set))
                            
            prod_pkg = prod_file.split('/')[0]
            cons_pkg = cons_file.split('/')[0]
            cross_boundary = prod_pkg != cons_pkg
            
            evidence = [
                f"Dataflow assignment in {rel_path}" if not flow.get("nested") else f"Nested call consumer(producer()) in {rel_path}",
                f"Local variables matched in context: {flow.get('context_function')}"
            ]
            if destructured_key:
                evidence.append(f"Call-site destructuring utilized key: {destructured_key}")
            if unutilized_keys:
                evidence.append(f"Unutilized fields: {', '.join(unutilized_keys)}")

            artifact_paths = []
            for terminal_write in consumer.get("terminal_writes", []):
                sink_keys = set(terminal_write.get("origin_keys", []))
                if sink_keys & utilized_keys:
                    sink_path = terminal_write["filename"]
                    artifact_paths.append(sink_path)
                    evidence.append(
                        f"Utilized field reaches {terminal_write['sink']} FILE_WRITE sink: {sink_path}"
                    )
                    matched_file_writes.add((cons_file, cons_func, sink_path))
            artifact_paths = sorted(set(artifact_paths))
                
            handoffs.append({
                "payload_candidate_id": f"flow_{prod_func}_to_{cons_func}",
                "observed_name": producer.get("returned_type") or "inferred_dictionary",
                "producer": {
                    "component": prod_pkg,
                    "file": prod_file,
                    "function": prod_func
                },
                "consumers": [{
                    "component": cons_pkg,
                    "file": cons_file,
                    "function": cons_func,
                    "matched_parameter": matched_param,
                    "evidence": f"Passed as argument to parameter {matched_param}"
                }],
                "handoff_method": "function_return_to_argument",
                "route_status": status,
                "observed_shape": {
                    "keys": producer.get("returned_keys", []),
                    "utilized_keys": sorted(list(utilized_keys)),
                    "unutilized_keys": unutilized_keys
                },
                "contract_identifiers": producer.get("contract_identifiers", []),
                "artifact_paths": artifact_paths,
                "scan_boundary": rel_path,
                "claim_type": "confirmed",
                "confidence": "high",
                "evidence": evidence,
                "limitations": standard_limitations
            })
            matched_producers.add((prod_file, prod_func))
            matched_consumers.add((cons_file, cons_func))

    # 2. Match File Handoffs (File Writes to Reads)
    file_writers = {}
    for rel_path, cands in candidates_by_file.items():
        for prod in cands.get("producers", []):
            if prod.get("candidate_type") == "payload_candidate":
                for filename in prod.get("file_writes", []):
                    file_writers.setdefault(filename, []).append((rel_path, prod))
                    basename = os.path.basename(filename)
                    if basename != filename:
                        file_writers.setdefault(basename, []).append((rel_path, prod))
                        
    file_readers = {}
    for rel_path, cands in candidates_by_file.items():
        for cons in cands.get("consumers", []):
            for filename in cons.get("file_reads", []):
                file_readers.setdefault(filename, []).append((rel_path, cons))
                basename = os.path.basename(filename)
                if basename != filename:
                    file_readers.setdefault(basename, []).append((rel_path, cons))

    # Connect matched file writers to readers
    for path_key, writers in file_writers.items():
        readers = file_readers.get(path_key, [])
        if not readers:
            continue
            
        for w_file, prod in writers:
            for r_file, cons in readers:
                is_exact = os.path.dirname(w_file) == os.path.dirname(r_file)
                
                prod_pkg = w_file.split('/')[0]
                cons_pkg = r_file.split('/')[0]
                cross_boundary = prod_pkg != cons_pkg
                
                # Resolve key-level shapes and contracts
                resolved_keys, resolved_cid = resolve_written_keys_and_contracts(prod, w_file, path_key)
                accessed = set(cons.get("all_accessed_keys", []))
                utilized_keys = set(resolved_keys) & accessed
                
                if not resolved_keys:
                    resolved_keys = prod.get("returned_keys", [])
                    utilized_keys = set(resolved_keys) & accessed
                    resolved_cid = prod.get("contract_identifiers", [])
                    
                observed_keys = sorted(list(resolved_keys))
                observed_utilized = sorted(list(utilized_keys))
                observed_unutilized = sorted(list(set(resolved_keys) - utilized_keys))
                
                # Apply three-tier status mapping based on exactness & utilization
                if is_exact:
                    if len(observed_utilized) == len(observed_keys) and len(observed_keys) > 0:
                        status = "connected"
                    elif len(observed_utilized) >= 1:
                        status = "connected_partial"
                    else:
                        status = "connected_unused"
                else:
                    # Basename-only match cannot verify identity beyond basename (likely_connected)
                    status = "likely_connected"
                
                # Add path-matching evidence
                path_matching_details = ""
                if path_key in prod.get("file_writes", []) and path_key in cons.get("file_reads", []):
                    path_matching_details = f"Path Match Basis: Confirmed exact path string match: '{path_key}'"
                elif os.path.basename(path_key) == path_key:
                    path_matching_details = f"Path Match Basis: Inferred filename basename match: '{path_key}'"
                else:
                    path_matching_details = f"Path Match Basis: Inferred path components match: '{path_key}'"

                handoffs.append({
                    "payload_candidate_id": f"file_{path_key}",
                    "observed_name": prod.get("returned_type") or path_key,
                    "producer": {
                        "component": prod_pkg,
                        "file": w_file,
                        "function": prod["function"]
                    },
                    "consumers": [{
                        "component": cons_pkg,
                        "file": r_file,
                        "function": cons["function"],
                        "evidence": f"Reads file {path_key}"
                    }],
                    "handoff_method": "file_write_to_file_read",
                    "route_status": status,
                    "observed_shape": {
                        "keys": observed_keys,
                        "utilized_keys": observed_utilized,
                        "unutilized_keys": observed_unutilized
                    },
                    "contract_identifiers": sorted(list(set(resolved_cid))),
                    "artifact_paths": [path_key],
                    "scan_boundary": w_file,
                    "claim_type": "confirmed" if is_exact else "inferred",
                    "confidence": "high" if is_exact else "medium",
                    "evidence": [
                        f"Writer: {w_file} ({prod['function']}) writes to {path_key}",
                        f"Reader: {r_file} ({cons['function']}) reads from {path_key}",
                        path_matching_details
                    ],
                    "limitations": standard_limitations
                })
                
                # Mark detailed file routes as matched
                for w_fn in prod.get("file_writes", []):
                    if w_fn == path_key or os.path.basename(w_fn) == os.path.basename(path_key):
                        matched_file_writes.add((w_file, prod["function"], w_fn))
                for r_fn in cons.get("file_reads", []):
                    if r_fn == path_key or os.path.basename(r_fn) == os.path.basename(path_key):
                        matched_file_reads.add((r_file, cons["function"], r_fn))
                        
                matched_consumers.add((r_file, cons["function"]))
            matched_producers.add((w_file, prod["function"]))

    # 3. Detect Ambiguous Consumers
    # If a file basename is matched to multiple readers
    for path_key, writers in file_writers.items():
        readers = file_readers.get(path_key, [])
        if len(readers) > 1:
            for w_file, prod in writers:
                prod_pkg = w_file.split('/')[0]
                handoffs.append({
                    "payload_candidate_id": f"ambiguous_file_{path_key}",
                    "observed_name": prod.get("returned_type") or path_key,
                    "producer": {
                        "component": prod_pkg,
                        "file": w_file,
                        "function": prod["function"]
                    },
                    "consumers": [{
                        "component": r_file.split('/')[0],
                        "file": r_file,
                        "function": cons["function"],
                        "evidence": f"Potential ambiguous read of {path_key}"
                    } for r_file, cons in readers],
                    "handoff_method": "file_write_to_file_read",
                    "route_status": "ambiguous_consumer",
                    "observed_shape": {
                        "keys": prod.get("returned_keys", []),
                        "utilized_keys": [],
                        "unutilized_keys": prod.get("returned_keys", [])
                    },
                    "contract_identifiers": prod.get("contract_identifiers", []),
                    "artifact_paths": [path_key],
                    "scan_boundary": w_file,
                    "claim_type": "inferred",
                    "confidence": "medium",
                    "evidence": [
                        f"Multiple candidate readers in scope for file path key {path_key}."
                    ],
                    "limitations": standard_limitations
                })

    # 4. Generate Unresolved Payload Routes (respecting scan boundary)
    for rel_path, cands in candidates_by_file.items():
        producers = cands.get("producers", [])
        for prod in producers:
            if prod.get("candidate_type") == "payload_candidate":
                file_writes = prod.get("file_writes", [])
                
                if file_writes:
                    for filename in file_writes:
                        if (rel_path, prod["function"], filename) not in matched_file_writes:
                            base = os.path.basename(filename)
                            is_boundary_intended = base in ("trixelcomposer_recipe.json", "trixelcomposer_atlas_plan.json")
                            
                            pkg = rel_path.split('/')[0]
                            if is_boundary_intended:
                                reason = "consumer outside scan boundary"
                                claim = "gap"
                                evidence = [
                                    "Consumer not visible within scanned boundary.",
                                    f"File written: {filename} is intended for cross-boundary consumption."
                                ]
                            else:
                                reason = "returned object not subsequently observed"
                                claim = "inferred"
                                evidence = [
                                    f"Emitted artifact: {filename} has no matching readers inside the scanned boundary."
                                ]
                                
                            unresolved_routes.append({
                                "payload_candidate_id": f"unresolved_prod_{rel_path}_{prod['function']}_{base}",
                                "observed_name": prod.get("returned_type") or "unknown",
                                "status": "producer_only",
                                "reason": reason,
                                "producer": {
                                    "component": pkg,
                                    "file": rel_path,
                                    "function": prod["function"]
                                },
                                "artifact_paths": [filename],
                                "scan_boundary": rel_path,
                                "claim_type": claim,
                                "confidence": "high",
                                "evidence": evidence
                            })
                else:
                    # Return object that has no file writes
                    if (rel_path, prod["function"]) not in matched_producers:
                        pkg = rel_path.split('/')[0]
                        unresolved_routes.append({
                            "payload_candidate_id": f"unresolved_prod_{rel_path}_{prod['function']}",
                            "observed_name": prod.get("returned_type") or "unknown",
                            "status": "producer_only",
                            "reason": "returned object not subsequently observed",
                            "producer": {
                                "component": pkg,
                                "file": rel_path,
                                "function": prod["function"]
                            },
                            "artifact_paths": [],
                            "scan_boundary": rel_path,
                            "claim_type": "inferred",
                            "confidence": "high",
                            "evidence": [
                                "Producer candidate defined but no consumer matched in current workspace."
                            ]
                        })

    for rel_path, cands in candidates_by_file.items():
        consumers = cands.get("consumers", [])
        for cons in consumers:
            file_reads = cons.get("file_reads", [])
            if file_reads:
                for filename in file_reads:
                    if (rel_path, cons["function"], filename) not in matched_file_reads:
                        pkg = rel_path.split('/')[0]
                        unresolved_routes.append({
                            "payload_candidate_id": f"unresolved_cons_{rel_path}_{cons['function']}_{os.path.basename(filename)}",
                            "observed_name": "unknown",
                            "status": "consumer_only",
                            "reason": "consumer input without visible producer",
                            "consumer": {
                                "component": pkg,
                                "file": rel_path,
                                "function": cons["function"]
                            },
                            "scan_boundary": rel_path,
                            "claim_type": "gap",
                            "confidence": "high",
                            "evidence": [
                                "Consumer function defined but no matching producer found.",
                                f"File read: {filename}"
                            ]
                        })
            else:
                if (rel_path, cons["function"]) not in matched_consumers:
                    if cons.get("param_utilization"):
                        pkg = rel_path.split('/')[0]
                        unresolved_routes.append({
                            "payload_candidate_id": f"unresolved_cons_{rel_path}_{cons['function']}",
                            "observed_name": "unknown",
                            "status": "consumer_only",
                            "reason": "consumer input without visible producer",
                            "consumer": {
                                "component": pkg,
                                "file": rel_path,
                                "function": cons["function"]
                            },
                            "scan_boundary": rel_path,
                            "claim_type": "gap",
                            "confidence": "high",
                            "evidence": [
                                "Consumer function defined but no matching producer found."
                            ]
                        })

    handoffs.sort(key=lambda x: x["payload_candidate_id"])
    unresolved_routes.sort(key=lambda x: x["payload_candidate_id"])

    return {
        "scan_roots": scan_roots,
        "analysis_boundary": analysis_boundary,
        "payload_handoffs": handoffs,
        "unresolved_payload_routes": unresolved_routes
    }
