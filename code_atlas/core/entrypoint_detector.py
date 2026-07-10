"""Module for detecting if a Python file is a likely application entrypoint."""

def detect_entrypoint(filepath, info):
    """Analyze parsed AST info to determine if a file is an entrypoint by requiring explicit signals.
    
    Returns:
        (is_entrypoint, evidence_list)
    """
    is_entry = False
    evidence = []
    
    # 1. AST check: Contains if __name__ == "__main__"
    if info.get("_has_main_block"):
        is_entry = True
        evidence.append("Contains 'if __name__ == \"__main__\"' execution block")
        
    # 2. AST check: Contains route decorators
    if info.get("_has_route_decorators"):
        is_entry = True
        evidence.append("Contains routing or API handler decorators (Flask/FastAPI style)")
        
    # 3. CLI Library Imports check: argparse, click
    raw_imports = info.get("raw_imports", [])
    cli_libs = {"argparse", "click"}
    for lib in cli_libs:
        if lib in raw_imports or any(imp.startswith(f"{lib}.") for imp in raw_imports):
            is_entry = True
            evidence.append(f"Imports the '{lib}' CLI library")

    return is_entry, evidence
