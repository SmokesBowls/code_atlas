"""AST parser module for extracting module structural metadata (imports, classes, methods, line ranges) and flags."""

import ast
import os

def get_module_path(filepath):
    """Convert a file path to a dot-separated module path relative to workspace."""
    base, _ = os.path.splitext(filepath)
    parts = base.split(os.sep)
    if parts[-1] == "__init__":
        parts.pop()
    return ".".join(parts)

def is_node_stub(body_nodes):
    """Check if a sequence of statements inside a function/class is a stub (only pass, docstrings, Ellipsis, or NotImplementedError)."""
    for node in body_nodes:
        if isinstance(node, ast.Pass):
            continue
        # Check for string constant (docstring)
        if isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
            continue
        if hasattr(ast, 'Str') and isinstance(node, ast.Expr) and isinstance(node.value, getattr(ast, 'Str')):
            continue
        # Check for Ellipsis (...)
        if isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant) and node.value.value is Ellipsis:
            continue
        if isinstance(node, ast.Raise):
            exc = node.exc
            if isinstance(exc, ast.Name) and exc.id == 'NotImplementedError':
                return True
            if isinstance(exc, ast.Call) and isinstance(exc.func, ast.Name) and exc.func.id == 'NotImplementedError':
                return True
        return False
    return True

def get_all_docstrings(tree):
    """Retrieve docstrings for the module, classes, and functions from the AST."""
    docstrings = []
    mod_doc = ast.get_docstring(tree)
    if mod_doc:
        docstrings.append(mod_doc)
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            doc = ast.get_docstring(node)
            if doc:
                docstrings.append(doc)
    return docstrings

def check_is_stub(tree, content, filename):
    """Check if the file is a stub (contains TODO/FIXME comments or docstrings, raises NotImplementedError, or contains only empty blocks)."""
    import re
    import tokenize
    import io
    
    # 1. Check for actual Python comments starting with # TODO or # FIXME using tokenize
    has_todo_comment = False
    try:
        tokens = tokenize.tokenize(io.BytesIO(content.encode('utf-8')).readline)
        for tok in tokens:
            if tok.type == tokenize.COMMENT:
                if re.match(r'^#\s*(TODO|FIXME)\b', tok.string, re.IGNORECASE):
                    has_todo_comment = True
                    break
    except Exception:
        pass
        
    if has_todo_comment:
        return True
        
    # 2. Check for TODO or FIXME lines inside actual docstrings
    has_todo_docstring = False
    try:
        for doc in get_all_docstrings(tree):
            for line in doc.splitlines():
                if re.match(r'^\s*(TODO|FIXME)\b', line, re.IGNORECASE):
                    has_todo_docstring = True
                    break
            if has_todo_docstring:
                break
    except Exception:
        pass
        
    if has_todo_docstring:
        return True
        
    # Check for NotImplementedError raise
    for node in ast.walk(tree):
        if isinstance(node, ast.Raise):
            exc = node.exc
            if isinstance(exc, ast.Name) and exc.id == 'NotImplementedError':
                return True
            if isinstance(exc, ast.Call) and isinstance(exc.func, ast.Name) and exc.func.id == 'NotImplementedError':
                return True
                
    if os.path.basename(filename) == '__init__.py':
        return False
        
    has_active_code = False
    for node in tree.body:
        if isinstance(node, (ast.Import, ast.ImportFrom, ast.Pass)):
            continue
        if isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
            continue
        if hasattr(ast, 'Str') and isinstance(node, ast.Expr) and isinstance(node.value, getattr(ast, 'Str')):
            continue
        if isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant) and node.value.value is Ellipsis:
            continue
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if not is_node_stub(node.body):
                has_active_code = True
            continue
        if isinstance(node, ast.ClassDef):
            for subnode in node.body:
                if isinstance(subnode, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    if not is_node_stub(subnode.body):
                        has_active_code = True
                elif isinstance(subnode, (ast.Pass, ast.Expr)):
                    continue
                else:
                    has_active_code = True
            continue
        has_active_code = True

    return not has_active_code

def check_has_main_block(tree):
    """Check if the file has an execution entrypoint (if __name__ == '__main__')."""
    for node in tree.body:
        if isinstance(node, ast.If):
            test = node.test
            if isinstance(test, ast.Compare):
                if isinstance(test.left, ast.Name) and test.left.id == '__name__':
                    if len(test.ops) == 1 and isinstance(test.ops[0], ast.Eq):
                        comparand = test.comparators[0]
                        if isinstance(comparand, ast.Constant) and comparand.value == '__main__':
                            return True
                        if hasattr(ast, 'Str') and isinstance(comparand, getattr(ast, 'Str')) and comparand.s == '__main__':
                            return True
    return False

def check_has_route_decorators(tree):
    """Check if any function in the module has routing decorators (e.g., Flask @app.route or FastAPI @app.get)."""
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            for decorator in node.decorator_list:
                if isinstance(decorator, ast.Call):
                    func = decorator.func
                    if isinstance(func, ast.Attribute) and func.attr in {'route', 'get', 'post', 'put', 'delete', 'patch'}:
                        return True
                elif isinstance(decorator, ast.Attribute) and decorator.attr in {'route', 'get', 'post', 'put', 'delete', 'patch'}:
                    return True
    return False

def parse_file(filepath, workspace_dir):
    """Read and parse a Python file to extract structural metadata and signals."""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    tree = ast.parse(content, filename=filepath)
    rel_path = os.path.relpath(filepath, workspace_dir)
    
    # 1. Imports extraction
    raw_imports = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for name in node.names:
                raw_imports.append(name.name)
        elif isinstance(node, ast.ImportFrom):
            module = node.module if node.module else ""
            if node.level > 0:
                dir_parts = os.path.dirname(rel_path).split(os.sep)
                if dir_parts == [''] or not dir_parts[0]:
                    dir_parts = []
                for _ in range(node.level - 1):
                    if dir_parts:
                        dir_parts.pop()
                prefix = ".".join(dir_parts)
                if prefix:
                    module = f"{prefix}.{module}" if module else prefix
            for name in node.names:
                import_name = f"{module}.{name.name}" if module else name.name
                raw_imports.append(import_name)

    # 2. Classes and methods extraction
    classes = []
    functions = []
    
    for node in tree.body:
        if isinstance(node, ast.ClassDef):
            methods = []
            for subnode in node.body:
                if isinstance(subnode, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    methods.append(subnode.name)
            classes.append({
                "name": node.name,
                "methods": methods,
                "start_line": node.lineno,
                "end_line": getattr(node, "end_lineno", node.lineno)
            })
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            functions.append({
                "name": node.name,
                "start_line": node.lineno,
                "end_line": getattr(node, "end_lineno", node.lineno)
            })

    lines_count = len(content.splitlines())

    return {
        "language": "python",
        "size_bytes": os.path.getsize(filepath),
        "claim_type": "confirmed",
        "confidence": "high",
        "evidence": [
            "Direct AST parsing of Python source code"
        ],
        "raw_imports": sorted(list(set(raw_imports))),
        "classes": classes,
        "functions": functions,
        
        # Internal temporary attributes used by classifiers
        "_has_main_block": check_has_main_block(tree),
        "_has_route_decorators": check_has_route_decorators(tree),
        "_is_stub": check_is_stub(tree, content, filepath)
    }
