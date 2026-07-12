# Code Atlas Component Relationship Report: fixture8

**Scanned at:** 2026-07-09T14:07:06.275195Z

## 1. Project Overview
- **Total Files Scanned:** 4
- **Total Parse Errors (Gaps):** 1
- **Detected Entrypoints:** main.py

### Status Distribution
- **Likely_active:** 4
- **Stubbed:** 0
- **Orphaned:** 0
- **Dormant:** 0
- **Unresolved:** 0
- **Active (Runtime Confirmed):** 0

## 2. Candidate Subsystem Groups
### Core Subsystem
- **Confidence:** Medium
- **Claim Type:** inferred
- **Member Count:** 1
- **Structurally Ambiguous:** Yes
- **Grouping Basis:** seed: directory_structure, refined_by: dependency_cohesion
- **Evidence:**
  - Files share directory structure: 'core'
  - Internal cohesion: 0 internal dependency edges
  - Cross-group coupling: 3 external dependency edges
  - Weak internal cohesion relative to strong cross-group coupling; marked as structurally ambiguous
- **Member Files:**
  - `core/helper.py`
- **Inbound Interface Files (1):**
  - `main.py`
- **Outbound Interface Files (2):**
  - `broken.py`
  - `utils/util_b.py`

### Root Components
- **Confidence:** Medium
- **Claim Type:** inferred
- **Member Count:** 1
- **Structurally Ambiguous:** Yes
- **Grouping Basis:** seed: directory_structure, refined_by: dependency_cohesion
- **Evidence:**
  - Files share directory structure: '.'
  - Internal cohesion: 0 internal dependency edges
  - Cross-group coupling: 2 external dependency edges
  - Weak internal cohesion relative to strong cross-group coupling; marked as structurally ambiguous
- **Member Files:**
  - `main.py`
- **Inbound Interface Files (0):**
- **Outbound Interface Files (2):**
  - `core/helper.py`
  - `utils/util_a.py`

### Utilities Subsystem
- **Confidence:** Low
- **Claim Type:** inferred
- **Member Count:** 2
- **Structurally Ambiguous:** Yes
- **Grouping Basis:** seed: directory_structure, refined_by: dependency_cohesion
- **Evidence:**
  - Files share directory structure: 'utils'
  - Internal cohesion: 0 internal dependency edges
  - Cross-group coupling: 2 external dependency edges
  - Weak internal cohesion relative to strong cross-group coupling; marked as structurally ambiguous
- **Member Files:**
  - `utils/util_a.py`
  - `utils/util_b.py`
- **Inbound Interface Files (2):**
  - `core/helper.py`
  - `main.py`
- **Outbound Interface Files (0):**

## 3. Top Ranked Next Files to Inspect (Top 10)
1. `broken.py` (Score: **100**)
   - **Reasons:** parse_error
   - **Evidence:**
     - parse_error: SyntaxError: expected ':' (broken.py, line 1)

2. `core/helper.py` (Score: **59**)
   - **Reasons:** structurally_ambiguous_subsystem, high_inbound_coupling, high_outbound_coupling
   - **Evidence:**
     - member_of: candidate_subsystem_groups.Core Subsystem
     - inbound_count: 1
     - outbound_count: 2

3. `utils/util_a.py` (Score: **55**)
   - **Reasons:** structurally_ambiguous_subsystem, high_inbound_coupling
   - **Evidence:**
     - member_of: candidate_subsystem_groups.Utilities Subsystem
     - inbound_count: 1

4. `utils/util_b.py` (Score: **55**)
   - **Reasons:** structurally_ambiguous_subsystem, high_inbound_coupling
   - **Evidence:**
     - member_of: candidate_subsystem_groups.Utilities Subsystem
     - inbound_count: 1

5. `main.py` (Score: **54**)
   - **Reasons:** structurally_ambiguous_subsystem, high_outbound_coupling
   - **Evidence:**
     - member_of: candidate_subsystem_groups.Root Components
     - outbound_count: 2

## 4. Path and Dependency Routes
These paths describe **static dependency routes** determined by import statements. The file order reflects the **dependency traversal order** (DFS) from the entrypoint, which is not a proven runtime execution call order. Suggested inspection order is **advisory only**.

### Static Route from entrypoint: `main.py`
- **Advisory Next File to Inspect in Route:** `broken.py`
- **Dependency Traversal Flow:**
  - `main.py`
  - `core/helper.py` ➔ **Inferred Boundary Crossing:** (Root Components ➔ Core Subsystem)
  - `broken.py` [PARSE ERROR, UNRESOLVED] ➔ **Inferred Boundary Crossing:** (Core Subsystem ➔ unknown)
  - `utils/util_b.py` ➔ **Inferred Boundary Crossing:** (Core Subsystem ➔ Utilities Subsystem)
  - `utils/util_a.py` ➔ **Inferred Boundary Crossing:** (Root Components ➔ Utilities Subsystem)
