# Code Atlas - Future Roadmap & TODOs

This file tracks the outstanding architectural opportunities, discovered codebase gaps, and analyzer enhancements identified during the Connectivity Layer implementation.

---

## 1. Discovered Codebase Gaps (To Investigate)

- [ ] **Address Orphaned `trixelcomposer_atlas_plan.json`**:
  - *Context*: Code Atlas statically identified that `trixelmap/trixelmap_build.py` emits the atlas plan, but nothing in `trixelcomposer` reads it.
  - *Action*: Determine if the composer is missing layout information, or if the atlas plan generation is deprecated and can be safely removed.
- [ ] **Review `trixelcomposer_recipe.json` Unutilized Keys**:
  - *Context*: The recipe file contains `grid_size`, `landmarks`, `transitions`, `type`, and `version` fields, but `scene_server.py` only utilizes the `regions` list.
  - *Action*: Investigate if `scene_server.py` should be verifying the `version`/`type` contracts or if the unused fields can be cleaned up from the pipeline output.

---

## 2. Static Analyzer Enhancements

- [ ] **Alias Mutation Tracking**:
  - *Enhancement*: Implement basic local dataflow alias tracking to follow dictionary mutations (e.g., `x = payload; x["new_key"] = ...`) when assigned to intermediate variable names.
- [ ] **Class Attribute State Tracking**:
  - *Enhancement*: Trace state across class properties and methods (e.g., `self.payload = data` followed by a read from `self.payload` in a different method).
- [ ] **Expanded Import & Module Resolution**:
  - *Enhancement*: Enhance import analysis to handle wildcard imports (`from module import *`) and absolute module aliases (`import sys as system`).

---

## 3. Connectivity Layer & Contract Features

- [ ] **Dynamic/Runtime Verification (Hybrid Scanner)**:
  - *Enhancement*: Implement a lightweight runtime decorator or hook that captures actual payload shapes at boundary crossings, validating `likely_connected` files or remote API handoffs.
- [ ] **Format/Schema Parser Integrations**:
  - *Enhancement*: Add parser support for YAML, INI, and environment-based configuration handoffs.
- [ ] **External API/Network Handoff Support**:
  - *Enhancement*: Track HTTP requests/gRPC calls as boundary connections to map microservices external to the local directory.


///////////////////
claude


Here's a clean pull of open items from this session, split by what's actually actionable vs. what's just worth remembering:

**Payload Handoff Diagnostics — code_atlas (open before calling it fully done)**
- [ ] Split `route_status` into two independent fields: `path_confidence` (connected/likely_connected/ambiguous_consumer/producer_only) and `utilization_status` (full/partial/unused) — current single enum loses info when a route is both shaky-connected *and* barely-utilized (e.g. `trixelcomposer_recipe.json` is `likely_connected` but only 1 of 6 keys read)
- [ ] Fix evidence wording on `likely_connected` routes — "Confirmed exact path string match" overstates certainty next to `claim_type: inferred` / `confidence: medium`; should read as basename-only, no shared path constant traced
- [ ] Once the above lands, worth a full re-scan of `conductor_building_blocks` to see if other routes were mislabeled the same way before this was caught

**Findings from this session worth tracking separately (not code_atlas bugs — real TrixelMap/TrixelComposer issues the tool surfaced)**
- [ ] `trixelcomposer_atlas_plan.json` has **zero confirmed consumers** anywhere in `conductor_building_blocks` — worth raising with whoever owns TrixelComposer/TrixelWorld, especially since it may be dead weight once the pixel-art output path replaces it
- [ ] Even where `trixelcomposer_recipe.json` connects, `scene_server.py` only reads `regions` — `type`, `version`, `transitions`, `landmarks`, `grid_size` are written and never consumed on the current evidence
- [ ] Duplicate biome-name mapping: `terrain_field_builder.py`'s `biome_map` and `trixel_recipe_writer.py`'s `_biome_name_to_id()` are two independent copies of the same table — separate bug from anything payload-diagnostics touches, still open

**Already-tracked TrixelMap bugs (unchanged, just resurfacing so they don't get lost under this thread)**
- [ ] `elevation_center` set to `centroid.x` instead of real elevation
- [ ] `_smooth()` stub doesn't actually blur (uses `np.pad`)
- [ ] `RELATION_VECTORS` missing ~5 relation strings from reference YAML
- [ ] Terrain class name mismatch causing fallback-to-default in `biome_map`
- [ ] `NameError` on missing `Any` import (may already be fixed — worth a quick check)

Want this exported as an actual file, or is a plain list enough to paste into your own todo.me?

/////////////////////////////////////

gpt

Yes. Add one concise section to `todo.md` so tomorrow starts cleanly:

```markdown
## NEXT SESSION — Payload Diagnostics Contract Cleanup

Do not add new features until this cleanup passes.

- [ ] Replace generic `connected` with deterministic route statuses:
  - `connected_full` = 100% of observed keys consumed
  - `connected_partial` = at least 1 but fewer than 100%
  - `connected_unused` = 0 observed keys consumed

- [ ] Correct known verdicts:
  - `build_terrain_field -> write_recipe_and_atlas` = `connected_partial`
  - `trixelcomposer_recipe.json -> trixelcomposer/scene_server.py` = `connected_partial`

- [ ] Fix `scan_boundary` so it records the actual scanned root or roots, not the producer filename.

- [ ] Split `run_pipeline` outputs into independent artifact routes:
  - `resolved_layout.json`
  - `spatial_authority.json`
  - `terrain_field.json`
  - `trixelcomposer_atlas_plan.json`
  - `trixelcomposer_recipe.json`

- [ ] In wide scans, connect only artifacts with a proven reader. Leave sibling artifacts independently unresolved.

- [ ] Extract literal contract identity values from fields such as `type` and `version` when statically visible. Do not treat field names alone as contract identifiers.

- [ ] Add `payload_diagnostics_summary` counts for every route status.

- [ ] Add regression tests for:
  - full, partial, and unused field consumption
  - one route record per emitted artifact
  - scan-root boundary accuracy
  - only the proven artifact connecting in the wider scan

- [ ] Repeat narrow `trixelmap` scan and wide `conductor_building_blocks` scan.

- [ ] Confirm no files inside the scanned projects were modified.

## Proven Findings — Preserve

- TrixelMap narrow scan correctly stops at the project boundary.
- Wide scan proves:
  `trixelmap/trixelmap_build.py::run_pipeline`
  writes `trixelcomposer_recipe.json`
  consumed by
  `trixelcomposer/scene_server.py::_load_region_authority`.
- The recipe consumer currently accesses only `regions`.
- `grid_size`, `landmarks`, `transitions`, `type`, and `version` are emitted but not accessed by that consumer.
- This is diagnostic evidence only; unused fields are not automatically defects.
```

That preserves both the remaining cleanup and the first important engine diagnosis. After those boxes pass, Payload Handoff Diagnostics can be treated as complete.
