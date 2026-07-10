"""Payload observations extractor.

Extracts returned keys, assignments, nested calls, parameter utilization,
and file operations within a single Python file to produce payload candidates.
"""

import ast
import os

class PayloadCandidateASTVisitor(ast.NodeVisitor):
    def __init__(self):
        self.producers = []
        self.consumers = []
        self.dataflows = []
        self.current_function = None
        self.current_params = []
        self.accessed_params = {}  # param_name -> set of keys/attributes
        self.forwarded_params = {}  # param_name -> set of callee names
        self.structural_params = set()  # param_name that is structurally update()d or expanded
        self.global_assignments = {}
        self.local_assignments = {}

    def visit_Assign(self, node):
        if self.current_function is None:
            for target in node.targets:
                if isinstance(target, ast.Name):
                    self.global_assignments[target.id] = node.value
        self.generic_visit(node)

    def visit_Module(self, node):
        self._track_block_dataflows(node)
        self.generic_visit(node)

    def _track_block_dataflows(self, node):
        assignments = {}
        calls = []
        
        # Recursively yield all children within the local scope (skipping nested defs)
        def walk_local_scope(n):
            for child in ast.iter_child_nodes(n):
                if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                    continue
                yield child
                yield from walk_local_scope(child)
                
        for subnode in walk_local_scope(node):
            if isinstance(subnode, ast.Assign):
                if isinstance(subnode.value, ast.Call):
                    func_name = self._get_func_name(subnode.value.func)
                    if func_name:
                        for target in subnode.targets:
                            if isinstance(target, ast.Name):
                                assignments[target.id] = func_name
            elif isinstance(subnode, ast.Call):
                func_name = self._get_func_name(subnode.func)
                if func_name:
                    # Check nested call: consumer(producer())
                    for arg in subnode.args:
                        if isinstance(arg, ast.Call):
                            nested_func = self._get_func_name(arg.func)
                            if nested_func:
                                self.dataflows.append({
                                    "producer_function": nested_func,
                                    "consumer_function": func_name,
                                    "variable": None,
                                    "nested": True,
                                    "context_function": getattr(node, "name", "<module>")
                                })
                    
                    args = [arg for arg in subnode.args]
                    kws = [kw.value for kw in subnode.keywords]
                    calls.append((func_name, args, kws))

        for func_name, args, kws in calls:
            all_arg_names = []
            for arg in args:
                if isinstance(arg, ast.Name):
                    all_arg_names.append(arg.id)
                elif isinstance(arg, ast.Subscript):
                    slice_val = self._get_slice_val(arg.slice)
                    if slice_val and isinstance(arg.value, ast.Name):
                        var_name = arg.value.id
                        if var_name in assignments:
                            producer_func = assignments[var_name]
                            self.dataflows.append({
                                "producer_function": producer_func,
                                "consumer_function": func_name,
                                "variable": var_name,
                                "destructured_key": slice_val,
                                "context_function": getattr(node, "name", "<module>")
                            })
            for kw in kws:
                if isinstance(kw, ast.Name):
                    all_arg_names.append(kw.id)
                    
            for arg_name in all_arg_names:
                if arg_name in assignments:
                    producer_func = assignments[arg_name]
                    if producer_func != func_name:
                        self.dataflows.append({
                            "producer_function": producer_func,
                            "consumer_function": func_name,
                            "variable": arg_name,
                            "context_function": getattr(node, "name", "<module>")
                        })

    def _resolve_expression_keys(self, expr, assignments):
        if expr is None:
            return []
        if isinstance(expr, ast.Call) and self._get_func_name(expr.func) == 'dumps' and len(expr.args) >= 1:
            expr = expr.args[0]
            
        if isinstance(expr, ast.Name):
            var_name = expr.id
            if var_name in assignments:
                val_node = assignments[var_name]
                if isinstance(val_node, ast.Dict):
                    return [self._get_key_str(k) for k in val_node.keys if self._get_key_str(k)]
                elif isinstance(val_node, ast.Call):
                    return {"from_call": self._get_func_name(val_node.func)}
                    
        elif isinstance(expr, ast.Subscript):
            slice_val = self._get_slice_val(expr.slice)
            if slice_val and isinstance(expr.value, ast.Name):
                var_name = expr.value.id
                if var_name in assignments:
                    val_node = assignments[var_name]
                    if isinstance(val_node, ast.Call):
                        return {"from_call_key": (self._get_func_name(val_node.func), slice_val)}
                        
        elif isinstance(expr, ast.Dict):
            return [self._get_key_str(k) for k in expr.keys if self._get_key_str(k)]
            
        return []

    def visit_FunctionDef(self, node):
        old_function = self.current_function
        old_params = self.current_params
        old_accessed = self.accessed_params
        old_forwarded = self.forwarded_params
        old_structural = self.structural_params
        old_local = self.local_assignments
        
        self.current_function = node.name
        self.current_params = [arg.arg for arg in node.args.args]
        self.accessed_params = {p: set() for p in self.current_params}
        self.forwarded_params = {p: set() for p in self.current_params}
        self.structural_params = set()
        
        # Track local assignments inside the function
        self.local_assignments = {}
        for subnode in ast.walk(node):
            if isinstance(subnode, ast.Assign):
                for target in subnode.targets:
                    if isinstance(target, ast.Name):
                        self.local_assignments[target.id] = subnode.value
                        
        self._track_block_dataflows(node)
        self.generic_visit(node)
        
        # Check returned keys and shapes
        returned_keys = set()
        has_dict_return = False
        returned_type = None
        contract_identifiers = []
        returned_dict_structure = {}
        
        for subnode in ast.walk(node):
            if isinstance(subnode, ast.Return) and subnode.value:
                if isinstance(subnode.value, ast.Dict):
                    has_dict_return = True
                    for k, v in zip(subnode.value.keys, subnode.value.values):
                        key_str = self._get_key_str(k)
                        if key_str:
                            returned_keys.add(key_str)
                            if any(w in key_str.lower() for w in ("contract", "version", "schema", "type", "payload")):
                                val_str = self._get_constant_str(v)
                                if val_str:
                                    contract_identifiers.append(val_str)
                            
                            # Extract returned dict structure
                            if isinstance(v, ast.Name) and v.id in self.local_assignments:
                                local_val = self.local_assignments[v.id]
                                if isinstance(local_val, ast.Dict):
                                    returned_dict_structure[key_str] = [self._get_key_str(dk) for dk in local_val.keys if self._get_key_str(dk)]
                                    for dk, dv in zip(local_val.keys, local_val.values):
                                        dk_str = self._get_key_str(dk)
                                        if dk_str and any(w in dk_str.lower() for w in ("contract", "version", "schema", "type", "payload")):
                                            dv_str = self._get_constant_str(dv)
                                            if dv_str:
                                                contract_identifiers.append(dv_str)
                            elif isinstance(v, ast.Dict):
                                returned_dict_structure[key_str] = [self._get_key_str(dk) for dk in v.keys if self._get_key_str(dk)]
                                for dk, dv in zip(v.keys, v.values):
                                    dk_str = self._get_key_str(dk)
                                    if dk_str and any(w in dk_str.lower() for w in ("contract", "version", "schema", "type", "payload")):
                                        dv_str = self._get_constant_str(dv)
                                        if dv_str:
                                            contract_identifiers.append(dv_str)
                elif isinstance(subnode.value, ast.Call):
                    func_id = self._get_func_name(subnode.value.func)
                    if func_id == 'dict':
                        has_dict_return = True
                    elif func_id:
                        returned_type = func_id
                        
        func_name_lower = node.name.lower()
        producer_keywords = {'build', 'emit', 'export', 'generate', 'extract', 'solve', 'classify', 'authorize', 'render', 'write'}
        is_producer_name = any(kw in func_name_lower for kw in producer_keywords)
        
        file_writes = []
        file_writes_detailed = []
        file_reads = []
        
        for subnode in ast.walk(node):
            if isinstance(subnode, ast.Call):
                func_id = self._get_func_name(subnode.func)
                written_expr = None
                filename = None
                
                if func_id == 'open':
                    mode = 'r'
                    if len(subnode.args) >= 1:
                        filename = self._get_constant_str(subnode.args[0])
                    if len(subnode.args) >= 2:
                        mode = self._get_constant_str(subnode.args[1]) or 'r'
                    for kw in subnode.keywords:
                        if kw.arg == 'mode':
                            mode = self._get_constant_str(kw.value) or 'r'
                    if any(c in mode for c in ('w', 'a', 'x')):
                        if filename: file_writes.append(filename)
                    else:
                        if filename: file_reads.append(filename)
                elif isinstance(subnode.func, ast.Attribute) and subnode.func.attr in ('write_text', 'write_bytes', 'write'):
                    filename = self._extract_path_filename(subnode.func.value)
                    if len(subnode.args) >= 1:
                        written_expr = subnode.args[0]
                    if filename: file_writes.append(filename)
                elif isinstance(subnode.func, ast.Attribute) and subnode.func.attr in ('read_text', 'read_bytes', 'read'):
                    filename = self._extract_path_filename(subnode.func.value)
                    if filename: file_reads.append(filename)
                    
                if filename and written_expr:
                    keys_info = self._resolve_expression_keys(written_expr, self.local_assignments)
                    file_writes_detailed.append({
                        "filename": filename,
                        "keys_info": keys_info
                    })
                    
        # Extract all accessed keys inside the function
        all_accessed = set()
        for subnode in ast.walk(node):
            if isinstance(subnode, ast.Subscript):
                slice_val = self._get_slice_val(subnode.slice)
                if slice_val:
                    all_accessed.add(slice_val)
            elif isinstance(subnode, ast.Attribute):
                all_accessed.add(subnode.attr)
            elif isinstance(subnode, ast.Call) and isinstance(subnode.func, ast.Attribute) and subnode.func.attr == 'get':
                if len(subnode.args) >= 1:
                    key_str = self._get_constant_str(subnode.args[0])
                    if key_str:
                        all_accessed.add(key_str)
                        
        if is_producer_name or file_writes or has_dict_return or returned_type:
            is_internal_lookup = func_name_lower.startswith('_') and not file_writes and len(returned_keys) > 0 and all(isinstance(k, str) and k.startswith('_') for k in returned_keys)
            
            self.producers.append({
                "function": node.name,
                "file_writes": sorted(list(set(file_writes))),
                "file_writes_detailed": file_writes_detailed,
                "returned_keys": sorted(list(returned_keys)),
                "returned_dict_structure": returned_dict_structure,
                "returned_type": returned_type,
                "has_dict_return": has_dict_return,
                "is_producer_name": is_producer_name,
                "contract_identifiers": sorted(list(set(contract_identifiers))),
                "candidate_type": "payload_candidate" if not is_internal_lookup else "internal_lookup"
            })
            
        param_utilization = {}
        for p in self.current_params:
            param_utilization[p] = {
                "accessed_keys": sorted(list(self.accessed_params[p])),
                "forwarded_to": sorted(list(self.forwarded_params[p])),
                "structural_consumption": p in self.structural_params
            }
            
        self.consumers.append({
            "function": node.name,
            "file_reads": sorted(list(set(file_reads))),
            "param_utilization": param_utilization,
            "all_accessed_keys": sorted(list(all_accessed))
        })
        
        self.current_function = old_function
        self.current_params = old_params
        self.accessed_params = old_accessed
        self.forwarded_params = old_forwarded
        self.structural_params = old_structural
        self.local_assignments = old_local

    def visit_Subscript(self, node):
        if self.current_function and isinstance(node.value, ast.Name):
            var_name = node.value.id
            if var_name in self.accessed_params:
                slice_val = self._get_slice_val(node.slice)
                if slice_val:
                    self.accessed_params[var_name].add(slice_val)
        self.generic_visit(node)

    def visit_Attribute(self, node):
        if self.current_function and isinstance(node.value, ast.Name):
            var_name = node.value.id
            if var_name in self.accessed_params:
                self.accessed_params[var_name].add(node.attr)
        self.generic_visit(node)

    def visit_Call(self, node):
        if self.current_function:
            if isinstance(node.func, ast.Attribute) and node.func.attr == 'get':
                if isinstance(node.func.value, ast.Name):
                    var_name = node.func.value.id
                    if var_name in self.accessed_params:
                        if len(node.args) >= 1:
                            key_str = self._get_constant_str(node.args[0])
                            if key_str:
                                self.accessed_params[var_name].add(key_str)
            elif isinstance(node.func, ast.Attribute) and node.func.attr == 'update':
                if len(node.args) >= 1 and isinstance(node.args[0], ast.Name):
                    var_name = node.args[0].id
                    if var_name in self.accessed_params:
                        self.structural_params.add(var_name)
            callee = self._get_func_name(node.func)
            if callee:
                for arg in node.args:
                    if isinstance(arg, ast.Name) and arg.id in self.forwarded_params:
                        self.forwarded_params[arg.id].add(callee)
                for kw in node.keywords:
                    if isinstance(kw.value, ast.Name) and kw.value.id in self.forwarded_params:
                        self.forwarded_params[kw.value.id].add(callee)
                        
        self.generic_visit(node)

    def _get_func_name(self, node):
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            return node.attr
        return None

    def _get_slice_val(self, node):
        if isinstance(node, ast.Constant):
            return str(node.value)
        if hasattr(ast, 'Index') and isinstance(node, getattr(ast, 'Index')):
            val = node.value
            if isinstance(val, ast.Constant):
                return str(val.value)
            elif hasattr(ast, 'Str') and isinstance(val, getattr(ast, 'Str')):
                return str(val.s)
        elif hasattr(ast, 'Str') and isinstance(node, getattr(ast, 'Str')):
            return str(node.s)
        return None

    def _get_key_str(self, node):
        if isinstance(node, ast.Constant):
            return str(node.value)
        elif hasattr(ast, 'Str') and isinstance(node, getattr(ast, 'Str')):
            return str(node.s)
        return None

    def _get_constant_str(self, node):
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            return node.value
        elif hasattr(ast, 'Str') and isinstance(node, getattr(ast, 'Str')):
            return node.s
        return None

    def _extract_path_filename(self, node):
        if isinstance(node, ast.Name):
            if node.id in self.local_assignments:
                node = self.local_assignments[node.id]
            elif node.id in self.global_assignments:
                node = self.global_assignments[node.id]
        if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Div):
            return self._get_constant_str(node.right)
        return self._get_constant_str(node)


def extract_payload_candidates(filepath):
    """Parse a single Python file and extract raw payload candidates and flows."""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    tree = ast.parse(content, filename=filepath)
    visitor = PayloadCandidateASTVisitor()
    try:
        visitor.visit(tree)
    except Exception:
        pass
        
    return {
        "producers": visitor.producers,
        "consumers": visitor.consumers,
        "dataflows": visitor.dataflows
    }
