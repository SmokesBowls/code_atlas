"""Module for computing multi-factor prioritization scores for project files to guide inspection."""

def calculate_inspection_rankings(files_data, parse_errors, candidate_groups):
    """Calculate inspection scores (0 to 100) for all files based on architectural features.
    
    Ranking Factors:
        1. parse error that is a source defect -> score = 100 (analysis limitations are not scored)
        2. structurally_ambiguous: true -> score += 50
        3. inbound_count > 0 -> score += min(25, inbound_count * 5)
        4. status == "stubbed" -> score += 30
        5. status == "orphaned" with classes/functions -> score += 20
        6. outbound_count > 0 -> score += min(10, outbound_count * 2)
        
    Parsed files are capped at score 99 to ensure broken files (100) always sort first.
    """
    file_to_group_info = {}
    for group in candidate_groups:
        gname = group["name"]
        is_ambig = group["structurally_ambiguous"]
        for f in group["member_files"]:
            file_to_group_info[f] = (gname, is_ambig)

    rankings = []

    # 1. Source defects (highest priority). Files Atlas failed to read for other reasons
    #    ("analysis_limitation") are scanner gaps, not EngAIn findings, and are not scored.
    for pe in parse_errors:
        if pe.get("kind", "source_defect") != "source_defect":
            continue
        rankings.append({
            "filepath": pe["filepath"],
            "score": 100,
            "reasons": ["parse_error"],
            "claim_type": "inferred",
            "confidence": "high",
            "evidence": [f"parse_error: {pe['error']}"]
        })

    # 2. Successfully parsed files
    for filepath, info in files_data.items():
        score = 0
        reasons = []
        evidence = []

        # Ambiguity check
        gname, is_ambig = file_to_group_info.get(filepath, (None, False))
        if is_ambig:
            score += 50
            reasons.append("structurally_ambiguous_subsystem")
            evidence.append(f"member_of: candidate_subsystem_groups.{gname}")

        # Inbound count coupling check
        inbound = info.get("inbound_count", 0)
        if inbound > 0:
            coupling_score = min(25, inbound * 5)
            score += coupling_score
            reasons.append("high_inbound_coupling")
            evidence.append(f"inbound_count: {inbound}")

        # Stubbed implementation check
        status_info = info.get("status", {})
        status = status_info.get("status")
        if status == "stubbed":
            score += 30
            reasons.append("stubbed_implementation")
            evidence.append("status: stubbed")

        # Orphaned with code check
        classes_count = len(info.get("classes", []))
        funcs_count = len(info.get("functions", []))
        if status == "orphaned" and (classes_count > 0 or funcs_count > 0):
            score += 20
            reasons.append("orphaned_with_code")
            evidence.append(f"status: orphaned, contains {classes_count} classes and {funcs_count} functions")

        # Outbound count coupling check
        outbound = info.get("outbound_count", 0)
        if outbound > 0:
            outbound_score = min(10, outbound * 2)
            score += outbound_score
            reasons.append("high_outbound_coupling")
            evidence.append(f"outbound_count: {outbound}")

        # Cap parsed files at 99 so broken files always rank first
        score = min(99, score)

        # Fallback for files with no specific issues
        if not reasons:
            score = 5
            reasons.append("routine_inspection")
            evidence.append("No critical issues or high coupling detected")

        rankings.append({
            "filepath": filepath,
            "score": score,
            "reasons": reasons,
            "claim_type": "inferred",
            "confidence": "high",
            "evidence": evidence
        })

    # Sort rankings: score descending, then filepath alphabetically
    rankings.sort(key=lambda r: (-r["score"], r["filepath"]))
    return rankings
