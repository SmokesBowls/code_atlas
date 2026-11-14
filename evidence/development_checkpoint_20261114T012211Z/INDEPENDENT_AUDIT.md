# Code Atlas independent architecture and code-quality audit

Audit date: 2026-11-13/14 UTC
Repository: `/mnt/data-drive/code_atlas`
Audited branch: `atlas-profile-structure-slice`
Audited baseline HEAD: `cd96258747e638f75ce410142da1b0f039faf3c1`
Scope: current working tree, including 10 modified tracked files and 10 untracked development files

## Executive assessment

Code Atlas is a functional static architecture scanner for Python repositories. It parses targets without importing or executing them and produces evidence about files, imports, entrypoints, candidate subsystems, static routes, payload handoffs, field effects, declared system profiles, HTTP boundaries, system coupling, and blast radius.

The current working tree is substantially more capable than committed HEAD. The implementation is useful as an advisory inspection tool, but it is not yet a hardened or authoritative runtime architecture verifier. The most important risks are unsafe report rendering, silent payload-analysis failures, incomplete async analysis, identity/parameter guessing, a partially implemented EFFECT contract, shallow viewer validation, an unversioned report format, launcher `eval`, and the fact that the newest capability slice existed only in the dirty working tree at audit time.

## Architecture verified from source

- Scanner orchestration and CLI: `code_atlas/scanner.py:63-158`, `code_atlas/scanner.py:160-209`.
- Static AST parsing without importing the target: `code_atlas/core/parser.py:154-225`.
- Conservative import resolution and unresolved ambiguity reporting: `code_atlas/core/reporter.py:15-77`, `code_atlas/core/reporter.py:103-143`.
- Report assembly: `code_atlas/core/reporter.py:144-280`.
- Static dependency-route traversal: `code_atlas/core/router.py:24-135`.
- Payload extraction and effect observations: `code_atlas/core/payload_extractor.py:202-313`, `code_atlas/core/payload_extractor.py:315-558`.
- Payload handoff assembly: `code_atlas/core/payload_analyzer.py:190-530`, `code_atlas/core/payload_analyzer.py:571-695`.
- Working-tree-only capabilities: profile hierarchy (`code_atlas/core/profile.py`), HTTP inventory/matching (`http_boundaries.py`, `boundary_matcher.py`), system coupling (`system_coupling.py`), Mermaid export (`mermaid_exporter.py`), and blast radius (`blast_radius.py`).
- Viewer server and browser UI: `code_atlas/viewer/server.py`, `code_atlas/viewer/static/app.js`.

## Verified strengths

1. Exact and unique-suffix local-import resolution refuses ambiguous edges.
2. Static route output is correctly described as traversal rather than runtime order.
3. Fixture coverage is strong for import ambiguity, payload routing, effect refusal behavior, profile structure, HTTP matching, blast radius, system coupling, and viewer path safety.
4. Profile declarations remain distinct from discovered relationships.
5. Confirmed and possible blast-radius edges are kept separate.
6. HTTP analysis is emitted separately and includes coverage accounting.
7. The implementation uses the Python standard library; no runtime dependency manifest was found.

## High-priority findings

### 1. Stored DOM injection risk

Report-controlled values are interpolated into `innerHTML` without escaping in `code_atlas/viewer/static/app.js`, including metadata, parse errors, unresolved imports, rankings, subsystem cards, and payload cards (notably lines 46-50, 133-149, 169-179, 196-243, and 478-519 at audit time). A malicious scanned repository can influence filenames, names, and source-derived messages. Loopback binding reduces network exposure but does not neutralize local browser execution.

### 2. Payload extraction can fail silently

`extract_payload_candidates()` catches all visitor exceptions and returns partial accumulated state without recording an analysis gap (`code_atlas/core/payload_extractor.py:647-663`). This can publish incomplete evidence as if analysis completed normally.

### 3. Async functions are omitted from stateful payload analysis

The parser recognizes `ast.AsyncFunctionDef`, but the payload visitor implements only `visit_FunctionDef` (`code_atlas/core/parser.py:188-205`; `code_atlas/core/payload_extractor.py:315-558`). Async producer/consumer behavior is therefore not covered by the main function-analysis path.

### 4. Payload identity can escape proven dependencies

Function resolution falls back to raw-import suffixes and globally unique exported names (`code_atlas/core/payload_analyzer.py:45-79`). This can promote an unproven same-named function to a confirmed handoff.

### 5. Forwarded parameter binding can be guessed

When binding a forwarded payload to a multi-parameter callee, the analyzer can ultimately choose the first parameter (`code_atlas/core/payload_analyzer.py:101-128`). This risks attributing the wrong accesses/effects to the payload.

### 6. Launcher shell injection risk

`start_atlas.sh` builds a command string and executes it through `eval` (`start_atlas.sh:94-113`). User-entered paths containing shell metacharacters can escape argument boundaries.

## Medium-priority findings

1. Viewer validation is weaker than documented. The README claims startup validation and rejection of incomplete/outdated reports (`README.md:131`, `README.md:354-366`), while `code_atlas/viewer/server.py:163-186` only checks JSON parsing and an object root.
2. The main report has no contract/version identifier (`code_atlas/core/reporter.py:259-280`). The AI exporter leaves `source_report_contract_version` unset (`code_atlas/core/ai_exporter.py:9-14`).
3. The EFFECT contract promises network/process sinks, declared terminals, and module-level mutation that are not implemented (`docs/contracts/effect_trace_contract.md:18-40`; compare `code_atlas/core/payload_extractor.py:262-311`). Generic `.write` detection is also broader than a proven file-handle sink.
4. `ast.walk(function_node)` descends into nested definitions in several payload analyses, allowing nested-scope activity to contaminate outer-function evidence (`payload_extractor.py:331-395`, `424-493`, `524-542`).
5. Optional outputs are written after the main report, so later failure can leave a partial report family (`code_atlas/scanner.py:96-158`).
6. Profile root overlaps are rejected, but equal/overlapping component declarations are not explicitly rejected (`code_atlas/core/profile.py:103-130`, `209-249`).
7. HTTP wrapper matching can use name-based heuristics without proven import/type identity (`code_atlas/core/http_boundaries.py:342-390`, `504-519`).
8. Known roadmap cleanup remains open: route confidence and field utilization remain conflated, and `scan_boundary` still records a file path rather than the scan root (`docs/planning/TODO.md:45-48`, `84`; `code_atlas/core/payload_analyzer.py:381-413`).

## Documentation and development-state findings

- Current CLI options `--profile`, `--mermaid-dir`, and `--boundaries-output` are not documented in the main option list (`README.md:83-117`; `code_atlas/scanner.py:188-202`).
- New report sections for profiles, systems, externals, lifecycle, coupling, unresolved imports, and blast-radius scope are underdocumented.
- No packaging metadata, release tags, CI workflow, coverage configuration, or compatibility matrix was found.
- README claims Python 3.9+, but verification occurred only on Python 3.14. `http_boundaries.py` constructs an AST node with `type_params=[]`, which deserves minimum-version testing.
- Historical/planning documents contain useful provenance but also long conversational residue; they should not be treated as concise current architecture records.

## Verification performed during the audit

- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s code_atlas/tests -v`: 107 tests passed; one non-failing `ResourceWarning` occurred in the expected viewer 404 path.
- `git diff --check`: passed.
- `bash -n start_atlas.sh`: passed.
- `node --check code_atlas/viewer/static/app.js`: passed.
- Maintained fixture scan: completed over four Python files with one deliberate syntax defect and produced JSON/Markdown/AI outputs in a temporary external directory.

These results validate the audited working tree, not baseline commit `cd96258` alone.

## Git state at audit time

- Current branch, local `main`, and `origin/main` all pointed to `cd96258`.
- The development branch had no upstream and no committed divergence from `main`.
- Nothing was staged.
- Ten tracked files were modified (216 insertions, 40 deletions).
- Ten source/test files were untracked.
- The meaningful profile/HTTP/coupling/blast-radius feature state therefore existed only in the working tree.

## Prioritized recommendations

1. Preserve the 20-file working-tree feature slice before any cleanup or repair.
2. Replace report-controlled `innerHTML` and remove launcher `eval`.
3. Surface payload-analysis failures explicitly and add async coverage.
4. Remove global-name/first-parameter guessing from confirmed payload claims.
5. Add and validate a versioned report contract.
6. Reconcile the EFFECT contract with implemented sinks.
7. Separate route confidence, utilization, and effect dimensions; correct `scan_boundary`.
8. Make multi-output generation atomic and strengthen profile overlap validation.
9. Add CI, supported-Python testing, coverage reporting, and current CLI/report documentation.

## Audit boundary

This assessment was formed from repository source, documentation, tests, Git history, working-tree changes, ignored files, and selected supplied scratchpad artifacts. It did not rely on previous agent assessments. No repository or EngAIn files were modified during the audit itself.
