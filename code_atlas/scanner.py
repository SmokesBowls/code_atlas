#!/usr/bin/env python3
"""Main entry point CLI scanner for Code Atlas."""

import argparse
import json
import os
import sys

# Ensure parent directory of code_atlas is in sys.path so imports work when run as script
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from code_atlas.core.parser import parse_file
from code_atlas.core.reporter import generate_report, generate_markdown_report

def run_scan(target_dir, output_file):
    """Scan the target directory, parse Python files, and generate JSON and Markdown reports."""
    target_dir = os.path.abspath(target_dir)
    if not os.path.isdir(target_dir):
        print(f"Error: Target directory '{target_dir}' does not exist.", file=sys.stderr)
        sys.exit(1)

    files_data = {}
    parse_errors = []
    
    ignored_dirs = {'.git', '__pycache__', '.venv', 'venv', 'env', '.gemini', 'build', 'dist', 'node_modules'}

    print(f"Scanning directory: {target_dir}...")
    
    for root, dirs, files in os.walk(target_dir):
        # Filter directories in-place to avoid scanning ignored paths
        dirs[:] = [d for d in dirs if d not in ignored_dirs]
        
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                rel_path = os.path.relpath(filepath, target_dir)
                # Normalize relative path to forward slashes for cross-platform reports
                rel_path_key = rel_path.replace(os.sep, '/')
                
                try:
                    parsed_info = parse_file(filepath, target_dir)
                    files_data[rel_path_key] = parsed_info
                except Exception as e:
                    parse_errors.append({
                        "filepath": rel_path_key,
                        "error": f"{type(e).__name__}: {str(e)}"
                    })

    # Generate full report data
    report = generate_report(target_dir, files_data, parse_errors)

    # Save to output JSON file
    output_path = os.path.abspath(output_file)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2)

    # Resolve and save Markdown report path alongside JSON
    base_path, ext = os.path.splitext(output_path)
    if ext.lower() == '.json':
        md_output_path = base_path + '.md'
    else:
        md_output_path = output_path + '.md'
        
    md_content = generate_markdown_report(report)
    with open(md_output_path, 'w', encoding='utf-8') as f:
        f.write(md_content)

    print("\nScan completed successfully!")
    print(f"  Scanned Files: {len(files_data)}")
    print(f"  Parse Errors:  {len(parse_errors)}")
    print(f"  JSON Report saved to: {output_path}")
    print(f"  Markdown Report saved to: {md_output_path}")

def main():
    parser = argparse.ArgumentParser(description="Code Atlas Static Scanner")
    parser.add_argument(
        "--dir",
        default=".",
        help="Directory to scan (default: current directory)"
    )
    parser.add_argument(
        "--output",
        default="code_atlas_report.json",
        help="File to save the JSON report to (default: code_atlas_report.json)"
    )
    args = parser.parse_args()
    run_scan(args.dir, args.output)

if __name__ == "__main__":
    main()
