"""Mermaid structure diagrams built from a finished Code Atlas report.

Structure diagrams show containment only: which declared system and component a
scanned file belongs to. They never contain edges, so placement in the
hierarchy cannot be read as dependency or communication.
"""

import hashlib

SOURCE_LEVEL_LABEL = (
    "Source-level architectural map: static evidence, not runtime confirmation."
)
STRUCTURE_NOTE = (
    "Structure diagram: containment only. No arrows are drawn; placement does not "
    "imply dependency or communication."
)


class MermaidExportError(ValueError):
    """Raised when a report lacks the sections a diagram needs."""


def _node_id(prefix, name):
    return f"{prefix}_{hashlib.sha1(name.encode('utf-8')).hexdigest()[:12]}"


def _label(text):
    # Mermaid quoted labels: escape characters that would end or break the label.
    return (
        text.replace("&", "#amp;")
        .replace('"', "#quot;")
        .replace("<", "#lt;")
        .replace(">", "#gt;")
        .replace("\n", " ")
    )


def _plural(n, word):
    return f"{n} {word}" if n == 1 else f"{n} {word}s"


def generate_repository_structure_mmd(report):
    """Return the Mermaid source for the repository-level structure diagram."""
    if "systems" not in report or "externals" not in report:
        raise MermaidExportError(
            "structure diagram requires a profile-defined hierarchy (scan with --profile)"
        )

    project = report.get("project_name", "repository")
    lines = [
        f"%% {SOURCE_LEVEL_LABEL}",
        f"%% {STRUCTURE_NOTE}",
        "flowchart TB",
    ]
    repo_id = _node_id("r", project)
    lines.append(f'  subgraph {repo_id}["{_label(project)} · scanned repository"]')
    lines.append("    direction LR")

    for system in report["systems"]:
        sid = _node_id("s", system["name"])
        lines.append(
            f'    subgraph {sid}["{_label(system["name"])} · system · {_plural(system["file_count"], "file")}"]'
        )
        lines.append("      direction TB")
        for comp in system["components"]:
            cid = _node_id("c", system["name"] + "/" + comp["name"])
            lines.append(f'      {cid}["{_label(comp["name"])} · {_plural(comp["file_count"], "file")}"]')
        if system["unassigned_files"]:
            uid = _node_id("u", system["name"])
            lines.append(
                f'      {uid}["not in a declared component · {_plural(len(system["unassigned_files"]), "file")}"]'
            )
        if not system["components"] and not system["unassigned_files"]:
            eid = _node_id("e", system["name"])
            lines.append(f'      {eid}["no scanned files under declared roots"]')
        lines.append("    end")

    outside = report.get("coverage", {}).get("files_outside_declared_systems", [])
    if outside:
        lines.append(
            f'    {_node_id("o", project)}["outside declared systems · {_plural(len(outside), "file")}"]'
        )
    lines.append("  end")

    for ext in report["externals"]:
        xid = _node_id("x", ext["name"])
        bridge = len(ext["bridge_files_in_scan"])
        lines.append(
            f'  {xid}["{_label(ext["name"])} · external · not scanned · '
            f'{_plural(bridge, "declared bridge file")} in repository"]'
        )

    lines.append("  classDef system fill:#eef4ff,stroke:#4a6fa5")
    lines.append("  classDef external fill:#f4f4f4,stroke:#888888")
    lines.append("  classDef gap fill:#fff8e6,stroke:#b08a2e")
    for system in report["systems"]:
        lines.append(f"  class {_node_id('s', system['name'])} system")
    for ext in report["externals"]:
        lines.append(f"  class {_node_id('x', ext['name'])} external")
    if outside:
        lines.append(f"  class {_node_id('o', project)} gap")
    return "\n".join(lines) + "\n"


def generate_repository_structure_page(report, mmd_source):
    """Return a Markdown page wrapping the diagram with its legend and provenance."""
    prov = report.get("profile", {})
    cov = report.get("coverage", {})
    out = [
        f"# Repository structure: {report.get('project_name', 'repository')}",
        "",
        f"> {SOURCE_LEVEL_LABEL}",
        f"> {STRUCTURE_NOTE}",
        "",
        f"- Scanned at: {report.get('scanned_at', 'unknown')}",
        f"- Profile: `{prov.get('path', 'unknown')}` (sha256 `{prov.get('sha256', 'unknown')}`)",
        "- Systems, components and externals are **declared** by the profile; file counts are from the scan.",
        "",
        "```mermaid",
        mmd_source.rstrip("\n"),
        "```",
        "",
        "## Declared systems",
        "",
        "| System | Roots | Files | Components | Not in a component |",
        "|---|---|---|---|---|",
    ]
    for s in report["systems"]:
        comps = ", ".join(f"{c['name']} ({c['file_count']})" for c in s["components"]) or "none declared"
        roots = ", ".join(f"`{r}`" for r in s["roots"])
        out.append(f"| {s['name']} | {roots} | {s['file_count']} | {comps} | {len(s['unassigned_files'])} |")
        if s["roots_without_scanned_files"]:
            missing = ", ".join(f"`{r}`" for r in s["roots_without_scanned_files"])
            out.append(f"|  | no scanned files under: {missing} | | | |")

    out += ["", "## Declared externals", "", "| External | Scanned | Bridge patterns | Bridge files found in repository |", "|---|---|---|---|"]
    for e in report["externals"]:
        pats = ", ".join(f"`{p}`" for p in e["bridge_patterns"]) or "none"
        out.append(f"| {e['name']} | no | {pats} | {len(e['bridge_files_in_scan'])} |")

    life = report.get("lifecycle")
    if life:
        out += ["", "## Declared lifecycle", "",
                "Declared by the profile, separately from system membership. Paths with no declaration are `undeclared`.", "",
                "| State | Files |", "|---|---|"]
        out += [f"| {st} | {n} |" for st, n in life["file_counts"].items()]
    coupling = report.get("system_coupling")
    if coupling:
        out += ["", "## Import coupling between declared systems", "",
                f"> {coupling['evidence_level']}. Shares are of the pair's resolved edges; possible edges "
                "(unresolved imports) are listed apart and not counted.", "",
                "| From | To | Edges | By source lifecycle | Main source files (share) | Possible edges |",
                "|---|---|---|---|---|---|"]
        for p in coupling["pairs"]:
            life_str = ", ".join(f"{k} {v}" for k, v in p["edges_by_source_lifecycle"].items()) or "-"
            top = "<br>".join(f"`{r['file']}` {r['share_percent']}%" for r in p["source_files"][:3]) or "-"
            out.append(f"| {p['from']} | {p['to']} | {p['edges']} | {life_str} | {top} | {p['possible_edges']} |")
    out += ["", "## Scan coverage", "", "| Mechanism | Scanned | Scope |", "|---|---|---|"]
    for mech, info in cov.get("mechanisms", {}).items():
        out.append(f"| {mech} | {'yes' if info['scanned'] else 'no'} | {info['scope']} |")
    out += [
        "",
        f"- Files outside declared systems: {len(cov.get('files_outside_declared_systems', []))}",
        f"- Files with parse gaps: {len(cov.get('files_with_gaps', []))}",
        f"- Files with unresolved imports (possible dependencies not drawn): {len(cov.get('files_with_unresolved_imports', []))}",
        "",
    ]
    return "\n".join(out)
