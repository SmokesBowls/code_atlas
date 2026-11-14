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

def write_boundaries(target_dir, report, boundaries_output):
    """Separate analysis: HTTP boundary inventory + matching over the files the scan found.

    Reads the finished report only for its file list and (optional) profile systems; the
    report itself is not modified."""
    from code_atlas.core.http_boundaries import build_http_inventory
    from code_atlas.core.boundary_matcher import match_boundaries
    owner = {f: s["name"] for s in report.get("systems", []) for f in s["files"]}
    default_system = report.get("project_name", os.path.basename(target_dir))
    inventory = build_http_inventory(target_dir, sorted(report["files"]),
                                     lambda rel: owner.get(rel, default_system))
    data = {"scanned_at": report.get("scanned_at"), "root": target_dir,
            "profile": report.get("profile"), "inventory": inventory,
            "matching": match_boundaries([inventory])}
    path = os.path.abspath(boundaries_output)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
    cs = inventory["coverage_summary"]["sites_by_status"]
    print(f"  HTTP boundaries saved to: {path}")
    print(f"    outgoing calls: {len(inventory['outgoing'])}, routes: {len(inventory['incoming'])}, "
          f"call sites not interpreted: {cs.get('not-interpreted', 0)}")


def run_scan(target_dir, output_file, ai_output=None, ai_json_output=None, ai_detail="standard",
             profile_path=None, mermaid_dir=None, boundaries_output=None):
    """Scan the target directory, parse Python files, and generate JSON and Markdown reports."""
    target_dir = os.path.abspath(target_dir)
    if not os.path.isdir(target_dir):
        print(f"Error: Target directory '{target_dir}' does not exist.", file=sys.stderr)
        sys.exit(1)

    # Validate the optional profile before scanning so a bad profile never yields partial output.
    profile = profile_provenance = None
    if mermaid_dir is not None and profile_path is None:
        print("Error: --mermaid-dir requires --profile (diagrams follow the declared system hierarchy).", file=sys.stderr)
        sys.exit(1)
    if profile_path is not None:
        from code_atlas.core.profile import load_profile, ProfileError
        try:
            profile, profile_provenance = load_profile(profile_path)
        except ProfileError as e:
            print(f"Error: invalid profile: {e}", file=sys.stderr)
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
    if profile is not None:
        from code_atlas.core.profile import build_profile_sections
        report.update(build_profile_sections(report, profile, profile_provenance, ignored_dirs))

    # Save to output JSON file
    output_path = os.path.abspath(output_file)
    if os.path.isdir(output_path) or output_file.endswith('/') or output_file.endswith('\\'):
        output_path = os.path.join(output_path, "code_atlas_report.json")
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

    if mermaid_dir is not None:
        from code_atlas.core.mermaid_exporter import (
            generate_repository_structure_mmd, generate_repository_structure_page)
        mermaid_path = os.path.abspath(mermaid_dir)
        os.makedirs(mermaid_path, exist_ok=True)
        mmd = generate_repository_structure_mmd(report)
        with open(os.path.join(mermaid_path, "repository_structure.mmd"), 'w', encoding='utf-8') as f:
            f.write(mmd)
        with open(os.path.join(mermaid_path, "repository_structure.md"), 'w', encoding='utf-8') as f:
            f.write(generate_repository_structure_page(report, mmd))
        print(f"  Mermaid structure diagram saved to: {mermaid_path}")

    if boundaries_output is not None:
        write_boundaries(target_dir, report, boundaries_output)

    # Conditionally execute the AI architecture packet exporter (opt-in)
    if ai_output is not None or ai_json_output is not None:
        from code_atlas.core.ai_exporter import generate_ai_json, generate_ai_markdown
        ai_json_data = generate_ai_json(report, ai_detail)
        
        if ai_json_output is not None:
            ai_json_path = os.path.abspath(ai_json_output)
            if os.path.isdir(ai_json_path) or ai_json_output.endswith('/') or ai_json_output.endswith('\\'):
                ai_json_path = os.path.join(ai_json_path, "code_atlas_report.ai.json")
            os.makedirs(os.path.dirname(ai_json_path), exist_ok=True)
            with open(ai_json_path, 'w', encoding='utf-8') as f:
                json.dump(ai_json_data, f, indent=2)
            print(f"  AI JSON Report saved to: {ai_json_path}")
            
        if ai_output is not None:
            ai_md_path = os.path.abspath(ai_output)
            if os.path.isdir(ai_md_path) or ai_output.endswith('/') or ai_output.endswith('\\'):
                ai_md_path = os.path.join(ai_md_path, "code_atlas_report.ai.md")
            os.makedirs(os.path.dirname(ai_md_path), exist_ok=True)
            ai_md_content = generate_ai_markdown(ai_json_data, ai_detail)
            with open(ai_md_path, 'w', encoding='utf-8') as f:
                f.write(ai_md_content)
            print(f"  AI Markdown Report saved to: {ai_md_path}")

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
    parser.add_argument(
        "--ai-output",
        default=None,
        help="Path to save the AI-oriented Markdown report (opt-in)"
    )
    parser.add_argument(
        "--ai-json-output",
        default=None,
        help="Path to save the AI-oriented JSON report (opt-in)"
    )
    parser.add_argument(
        "--ai-detail",
        default="standard",
        choices=["compact", "standard", "full"],
        help="Detail level for the AI export: compact, standard, or full (default: standard)"
    )
    parser.add_argument(
        "--profile",
        default=None,
        help="Optional JSON profile declaring systems, components and external systems"
    )
    parser.add_argument(
        "--mermaid-dir",
        default=None,
        help="Directory for Mermaid structure diagrams (requires --profile)"
    )
    parser.add_argument(
        "--boundaries-output",
        default=None,
        help="Optional JSON file for the HTTP boundary inventory and matches (separate analysis)"
    )
    args = parser.parse_args()
    run_scan(args.dir, args.output, args.ai_output, args.ai_json_output, args.ai_detail,
             profile_path=args.profile, mermaid_dir=args.mermaid_dir,
             boundaries_output=args.boundaries_output)

if __name__ == "__main__":
    main()
