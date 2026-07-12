# Code Atlas Component Relationship Report: trixelmap

**Scanned at:** 2026-07-10T14:15:08.649601Z

## 1. Project Overview
- **Total Files Scanned:** 16
- **Total Parse Errors (Gaps):** 2
- **Detected Entrypoints:** trixelmap_build.py, debug_layout_svg.py, vault_spatial_parser.py, spatial_pattern_matcher.py, location_ranker.py, trixel_recipes_mr.py, docs/message_file_package (1)/spatial_authority_extractor.py, docs/message_file_package (1)/message_file_package/spatial_authority_extractor.py

### Status Distribution
- **Likely_active:** 12
- **Stubbed:** 0
- **Orphaned:** 2
- **Dormant:** 2
- **Unresolved:** 0
- **Active (Runtime Confirmed):** 0

## 2. Candidate Subsystem Groups
### Message_file_package (1) Subsystem
- **Confidence:** High
- **Claim Type:** inferred
- **Member Count:** 1
- **Structurally Ambiguous:** No
- **Grouping Basis:** seed: directory_structure, refined_by: dependency_cohesion
- **Evidence:**
  - Files share directory structure: 'docs/message_file_package (1)'
  - Internal cohesion: 0 internal dependency edges
  - Cross-group coupling: 0 external dependency edges
- **Member Files:**
  - `docs/message_file_package (1)/spatial_authority_extractor.py`
- **Inbound Interface Files (0):**
- **Outbound Interface Files (0):**

### Message_file_package Subsystem
- **Confidence:** Low
- **Claim Type:** inferred
- **Member Count:** 2
- **Structurally Ambiguous:** Yes
- **Grouping Basis:** seed: directory_structure, refined_by: dependency_cohesion
- **Evidence:**
  - Files share directory structure: 'docs/message_file_package (1)/message_file_package'
  - Internal cohesion: 0 internal dependency edges
  - Cross-group coupling: 1 external dependency edges
  - Weak internal cohesion relative to strong cross-group coupling; marked as structurally ambiguous
- **Member Files:**
  - `docs/message_file_package (1)/message_file_package/spatial_authority_extractor.py`
  - `docs/message_file_package (1)/message_file_package/spatial_authority_extractor_2.py`
- **Inbound Interface Files (0):**
- **Outbound Interface Files (1):**
  - `spatial_pattern_matcher.py`

### Message_file_package3 Subsystem
- **Confidence:** Low
- **Claim Type:** inferred
- **Member Count:** 2
- **Structurally Ambiguous:** Yes
- **Grouping Basis:** seed: directory_structure, refined_by: dependency_cohesion
- **Evidence:**
  - Files share directory structure: 'docs/message_file_package3'
  - Internal cohesion: 0 internal dependency edges
  - Cross-group coupling: 1 external dependency edges
  - Weak internal cohesion relative to strong cross-group coupling; marked as structurally ambiguous
- **Member Files:**
  - `docs/message_file_package3/spatial_pattern_matcher.py`
  - `docs/message_file_package3/vault_spatial_parser.py`
- **Inbound Interface Files (0):**
- **Outbound Interface Files (1):**
  - `spatial_pattern_matcher.py`

### Root Components
- **Confidence:** High
- **Claim Type:** inferred
- **Member Count:** 10
- **Structurally Ambiguous:** No
- **Grouping Basis:** seed: directory_structure, refined_by: dependency_cohesion
- **Evidence:**
  - Files share directory structure: '.'
  - Internal cohesion: 6 internal dependency edges
  - Cross-group coupling: 2 external dependency edges
- **Member Files:**
  - `debug_layout_svg.py`
  - `location_ranker.py`
  - `spatial_authority_extractor.py`
  - `spatial_layout_solver.py`
  - `spatial_pattern_matcher.py`
  - `terrain_field_builder.py`
  - `trixel_recipe_writer.py`
  - `trixel_recipes_mr.py`
  - `trixelmap_build.py`
  - `vault_spatial_parser.py`
- **Inbound Interface Files (2):**
  - `docs/message_file_package (1)/message_file_package/spatial_authority_extractor_2.py`
  - `docs/message_file_package3/vault_spatial_parser.py`
- **Outbound Interface Files (0):**

### Unassigned Subsystem
- **Confidence:** High
- **Claim Type:** inferred
- **Member Count:** 1
- **Structurally Ambiguous:** No
- **Grouping Basis:** seed: directory_structure, refined_by: dependency_cohesion
- **Evidence:**
  - Files share directory structure: 'docs/message_file_package/unassigned'
  - Internal cohesion: 0 internal dependency edges
  - Cross-group coupling: 0 external dependency edges
- **Member Files:**
  - `docs/message_file_package/unassigned/extracted_block_001.py`
- **Inbound Interface Files (0):**
- **Outbound Interface Files (0):**

## 3. Top Ranked Next Files to Inspect (Top 10)
1. `docs/message_file_package3/unassigned/extracted_block_004.py` (Score: **100**)
   - **Reasons:** parse_error
   - **Evidence:**
     - parse_error: IndentationError: unexpected indent (extracted_block_004.py, line 1)

2. `docs/message_file_package3/vault_spatial_parser_2.py` (Score: **100**)
   - **Reasons:** parse_error
   - **Evidence:**
     - parse_error: IndentationError: unexpected indent (vault_spatial_parser_2.py, line 4)

3. `docs/message_file_package3/spatial_pattern_matcher.py` (Score: **70**)
   - **Reasons:** structurally_ambiguous_subsystem, orphaned_with_code
   - **Evidence:**
     - member_of: candidate_subsystem_groups.Message_file_package3 Subsystem
     - status: orphaned, contains 0 classes and 1 functions

4. `docs/message_file_package (1)/message_file_package/spatial_authority_extractor_2.py` (Score: **52**)
   - **Reasons:** structurally_ambiguous_subsystem, high_outbound_coupling
   - **Evidence:**
     - member_of: candidate_subsystem_groups.Message_file_package Subsystem
     - outbound_count: 1

5. `docs/message_file_package3/vault_spatial_parser.py` (Score: **52**)
   - **Reasons:** structurally_ambiguous_subsystem, high_outbound_coupling
   - **Evidence:**
     - member_of: candidate_subsystem_groups.Message_file_package3 Subsystem
     - outbound_count: 1

6. `docs/message_file_package (1)/message_file_package/spatial_authority_extractor.py` (Score: **50**)
   - **Reasons:** structurally_ambiguous_subsystem
   - **Evidence:**
     - member_of: candidate_subsystem_groups.Message_file_package Subsystem

7. `docs/message_file_package/unassigned/extracted_block_001.py` (Score: **20**)
   - **Reasons:** orphaned_with_code
   - **Evidence:**
     - status: orphaned, contains 1 classes and 1 functions

8. `spatial_pattern_matcher.py` (Score: **20**)
   - **Reasons:** high_inbound_coupling
   - **Evidence:**
     - inbound_count: 4

9. `trixelmap_build.py` (Score: **8**)
   - **Reasons:** high_outbound_coupling
   - **Evidence:**
     - outbound_count: 4

10. `spatial_authority_extractor.py` (Score: **7**)
   - **Reasons:** high_inbound_coupling, high_outbound_coupling
   - **Evidence:**
     - inbound_count: 1
     - outbound_count: 1

## 4. Path and Dependency Routes
These paths describe **static dependency routes** determined by import statements. The file order reflects the **dependency traversal order** (DFS) from the entrypoint, which is not a proven runtime execution call order. Suggested inspection order is **advisory only**.

### Static Route from entrypoint: `debug_layout_svg.py`
- **Advisory Next File to Inspect in Route:** `debug_layout_svg.py`
- **Dependency Traversal Flow:**
  - `debug_layout_svg.py`

### Static Route from entrypoint: `docs/message_file_package (1)/message_file_package/spatial_authority_extractor.py`
- **Advisory Next File to Inspect in Route:** `docs/message_file_package (1)/message_file_package/spatial_authority_extractor.py`
- **Dependency Traversal Flow:**
  - `docs/message_file_package (1)/message_file_package/spatial_authority_extractor.py`

### Static Route from entrypoint: `docs/message_file_package (1)/spatial_authority_extractor.py`
- **Advisory Next File to Inspect in Route:** `docs/message_file_package (1)/spatial_authority_extractor.py`
- **Dependency Traversal Flow:**
  - `docs/message_file_package (1)/spatial_authority_extractor.py`

### Static Route from entrypoint: `location_ranker.py`
- **Advisory Next File to Inspect in Route:** `location_ranker.py`
- **Dependency Traversal Flow:**
  - `location_ranker.py`

### Static Route from entrypoint: `spatial_pattern_matcher.py`
- **Advisory Next File to Inspect in Route:** `spatial_pattern_matcher.py`
- **Dependency Traversal Flow:**
  - `spatial_pattern_matcher.py`

### Static Route from entrypoint: `trixel_recipes_mr.py`
- **Advisory Next File to Inspect in Route:** `trixel_recipes_mr.py`
- **Dependency Traversal Flow:**
  - `trixel_recipes_mr.py`

### Static Route from entrypoint: `trixelmap_build.py`
- **Advisory Next File to Inspect in Route:** `spatial_pattern_matcher.py`
- **Dependency Traversal Flow:**
  - `trixelmap_build.py`
  - `spatial_authority_extractor.py`
  - `spatial_pattern_matcher.py`
  - `spatial_layout_solver.py`
  - `terrain_field_builder.py`
  - `trixel_recipe_writer.py`

### Static Route from entrypoint: `vault_spatial_parser.py`
- **Advisory Next File to Inspect in Route:** `spatial_pattern_matcher.py`
- **Dependency Traversal Flow:**
  - `vault_spatial_parser.py`
  - `spatial_pattern_matcher.py`

## 5. Limitations
- **Static analysis cannot resolve dynamic imports (e.g. __import__, importlib, or dynamic string execution).**
  - **Claim Type:** gap
  - **Confidence:** High

- **Reflection and dynamic attribute retrieval may hide runtime dependencies.**
  - **Claim Type:** gap
  - **Confidence:** High

- **Static route paths are inferred from import syntax, not runtime-verified.**
  - **Claim Type:** gap
  - **Confidence:** Medium

- **Namespace packages without __init__.py are supported, but ambiguous resolutions (multiple candidates matching the same import) are recorded as gaps.**
  - **Claim Type:** gap
  - **Confidence:** High
