# Code Atlas Pilot Phase Notes

This document summarizes findings from running Code Atlas on the `code_atlas` project itself (12 scanned files, 0 parse errors).

---

## 1. What Worked Well

- **Local Dependency Resolution**: Strip-matching resolved imports cleanly. E.g., `code_atlas.core.parser` was correctly mapped to the relative path `core/parser.py`.
- **Entrypoint Detection Heuristics**: The Entrypoint Audit effectively eliminated false positives. Only `scanner.py` (which contains `if __name__ == "__main__"` and imports `argparse`) and `tests/test_scanner.py` (a test root) were marked as entrypoints.
- **Candidate Subsystem Groupings**:
  - `Core Subsystem` (containing the files inside `core/`) was grouped with high confidence and cohesive dependency edge density.
  - `Testing Suite` correctly isolated the test script.
  - `Root Components` (containing the outer `scanner.py` orchestrator and `__init__.py`) was correctly identified as `structurally_ambiguous` due to low internal cohesion but high outbound coupling.
- **Static Traversal Routes**: Reconstructed full DFS dependency paths correctly from `scanner.py` and `test_scanner.py` through their downstreams, with accurate subsystem boundary crossings.

---

## 2. Pilot Corrections Pass

### 1. Tokenizer-Based Stub Detection Fix
- **Issue**: Previously, `core/parser.py` and `core/status_classifier.py` were incorrectly classified as `stubbed` because they contained docstrings and parser checks discussing TODOs.
- **Correction**: Replaced global substring matching with Python's native `tokenize` module. We now scan actual `tokenize.COMMENT` tokens matching `# TODO` or `# FIXME` patterns, and check docstrings lines specifically starting with `TODO` or `FIXME`.
- **Outcome**: The false-positive stub classifications have completely disappeared. Both core modules and test modules now resolve correctly as `likely_active`.

### 2. Namespace Package Handling (PEP 420)
- **Outcome**: Resolved clean namespace packages (no `__init__.py` files) successfully when a unique candidate module matches the relative path.
- **Outcome**: Ambiguous namespace import resolutions (multiple candidates matching the same module) are caught and reported as `AmbiguousImportError` gaps. Added the limitation to the report's limitations registry.

### 3. Verification
- **Automated Tests**: Added 4 regression tests verifying:
  - Global `"TODO"` string constants (as logic strings) do NOT trigger stub detection.
  - Genuine `# TODO` comments trigger stub detection.
  - `raise NotImplementedError` triggers stub detection.
  - Namespace packages resolve correctly, and duplicate imports trigger `AMBIGUOUS` resolution gaps.
- **Result**: Running `python3 -m unittest discover -s code_atlas/tests -p "*.py"` completes successfully with `16 tests - OK`.
- **No regressions** were discovered.
