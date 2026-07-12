# Code Atlas Component Relationship Report: conductor_building_blocks

**Scanned at:** 2026-07-12T12:42:50.008975Z

## 1. Project Overview
- **Total Files Scanned:** 106
- **Total Parse Errors (Gaps):** 23
- **Detected Entrypoints:** trixelworld/demo_bestiary_flora_sheet.py, trixelworld/demo_bestiary_fauna_sheet.py, trixelworld/demo_building_material_sheet.py, trixelworld/demo_beach_material_sheet.py, trixelworld/stress_scene_mr.py, trixelworld/trixel_demo_mr.py, trixelworld/trixel_recipes_mr.py, trixelworld/engine_debug_mr.py, trixelworld/surface_behavior_mr.py, trixelworld/trixel_brush_adapter.py, trixelworld/palette_mr.py, trixelworld/engine_mr.py, trixelworld/world_tree_mr.py, trixelworld/brushes/gbr_parser_mr.py, trixelworld/brushes/gfig_parser_mr.py, trixelworld/brushes/vbr_parser_mr.py, trixelworld/brushes/gtp_parser_mr.py, trixelworld/brushes/gpl_parser_mr.py, trixelworld/brushes/gih_parser_mr.py, trixelworld/brushes/gdyn_parser_mr.py, libresprite/gates/gate_libresprite_starter_set.py, libresprite/gates/gate_libra_conductor_roundtrip.py, libresprite/gates/gate_libra_snapshot_backend.py, libresprite/gates/gate_libra_snapshot_stress_set.py, libresprite/gates/gate_libra_snapshot_schema_contract.py, libresprite/gates/gate_libra_snapshot_exporter_contract.py, libresprite/gates/gate_libra_real_document_regression.py, libresprite/gates/gate_libra_full_suite.py, libresprite/gates/gate_libra_asset_provenance_manifest.py, trixelcomposer/enhanced_trixel_core.py, trixelcomposer/scene_server.py, trixelcomposer/terminal_trixel.py, trixelcomposer/trixel_render_bridge.py, trixelcomposer/atlas_composer.py, trixelcomposer/tile_server.py, trixelmap/trixelmap_build.py, trixelmap/debug_layout_svg.py, trixelmap/vault_spatial_parser.py, trixelmap/spatial_pattern_matcher.py, trixelmap/location_ranker.py, trixelmap/trixel_recipes_mr.py, trixelmap/docs/message_file_package (1)/spatial_authority_extractor.py, trixelmap/docs/message_file_package (1)/message_file_package/spatial_authority_extractor.py, terrain/world_field_nucleus.py, terrain/terrain_thresholds.py, terrain/terrain_control_center.py, terrain/trixel_world_adapter.py

### Status Distribution
- **Likely_active:** 70
- **Stubbed:** 5
- **Orphaned:** 14
- **Dormant:** 17
- **Unresolved:** 0
- **Active (Runtime Confirmed):** 0

## 2. Candidate Subsystem Groups
### Brushes Subsystem
- **Confidence:** Low
- **Claim Type:** inferred
- **Member Count:** 12
- **Structurally Ambiguous:** Yes
- **Grouping Basis:** seed: directory_structure, refined_by: dependency_cohesion
- **Evidence:**
  - Files share directory structure: 'trixelworld/brushes'
  - Internal cohesion: 0 internal dependency edges
  - Cross-group coupling: 6 external dependency edges
  - Weak internal cohesion relative to strong cross-group coupling; marked as structurally ambiguous
- **Member Files:**
  - `trixelworld/brushes/__init__.py`
  - `trixelworld/brushes/gbr_parser_mr.py`
  - `trixelworld/brushes/gdyn_parser_mr.py`
  - `trixelworld/brushes/gfig_parser_mr.py`
  - `trixelworld/brushes/gflare_parser_mr.py`
  - `trixelworld/brushes/ggr_parser_mr.py`
  - `trixelworld/brushes/gih_parser_mr.py`
  - `trixelworld/brushes/gimpressionist_parser_mr.py`
  - `trixelworld/brushes/gpl_parser_mr.py`
  - `trixelworld/brushes/gtp_parser_mr.py`
  - `trixelworld/brushes/lisp_parser_mr.py`
  - `trixelworld/brushes/vbr_parser_mr.py`
- **Inbound Interface Files (6):**
  - `trixelworld/brushes/test_lisp.py`
  - `trixelworld/engine_debug_mr.py`
  - `trixelworld/engine_mr.py`
  - `trixelworld/test_parse.py`
  - `trixelworld/trixel_brush_adapter.py`
  - `trixelworld/world_tree_mr.py`
- **Outbound Interface Files (0):**

### Gates Subsystem
- **Confidence:** Medium
- **Claim Type:** inferred
- **Member Count:** 17
- **Structurally Ambiguous:** Yes
- **Grouping Basis:** seed: directory_structure, refined_by: dependency_cohesion
- **Evidence:**
  - Files share directory structure: 'libresprite/gates, terrain/gates'
  - Internal cohesion: 1 internal dependency edges
  - Cross-group coupling: 5 external dependency edges
  - Weak internal cohesion relative to strong cross-group coupling; marked as structurally ambiguous
- **Member Files:**
  - `libresprite/gates/gate_libra_asset_provenance_manifest.py`
  - `libresprite/gates/gate_libra_conductor_roundtrip.py`
  - `libresprite/gates/gate_libra_full_suite.py`
  - `libresprite/gates/gate_libra_real_document_regression.py`
  - `libresprite/gates/gate_libra_snapshot_backend.py`
  - `libresprite/gates/gate_libra_snapshot_exporter_contract.py`
  - `libresprite/gates/gate_libra_snapshot_schema_contract.py`
  - `libresprite/gates/gate_libra_snapshot_stress_set.py`
  - `libresprite/gates/gate_libresprite_starter_set.py`
  - `terrain/gates/gate_adapter_boundary.py`
  - `terrain/gates/gate_dirty_chunk_or_delta_shape.py`
  - `terrain/gates/gate_imports.py`
  - `terrain/gates/gate_no_authority_overreach.py`
  - `terrain/gates/gate_terrain_adapter_rejection_proof.py`
  - `terrain/gates/gate_thresholds_exist.py`
  - `terrain/gates/gate_trixel_retro_surface_paint_document.py`
  - `terrain/gates/gate_world_field_boundary.py`
- **Inbound Interface Files (1):**
  - `terrain/terrain_control_center.py`
- **Outbound Interface Files (4):**
  - `terrain/terrain_thresholds.py`
  - `terrain/trixel_retro_surface_paint_document.py`
  - `terrain/trixel_world_adapter.py`
  - `terrain/world_field_nucleus.py`

### Libresprite Subsystem
- **Confidence:** High
- **Claim Type:** inferred
- **Member Count:** 10
- **Structurally Ambiguous:** No
- **Grouping Basis:** seed: directory_structure, refined_by: dependency_cohesion
- **Evidence:**
  - Files share directory structure: 'libresprite'
  - Internal cohesion: 12 internal dependency edges
  - Cross-group coupling: 0 external dependency edges
- **Member Files:**
  - `libresprite/__init__.py`
  - `libresprite/ls_asset_provenance_mr.py`
  - `libresprite/ls_cel_parser_mr.py`
  - `libresprite/ls_image_parser_mr.py`
  - `libresprite/ls_layer_parser_mr.py`
  - `libresprite/ls_palette_parser_mr.py`
  - `libresprite/ls_semantic_parser_mr.py`
  - `libresprite/ls_snapshot_backend_mr.py`
  - `libresprite/ls_snapshot_exporter_mr.py`
  - `libresprite/ls_sprite_parser_mr.py`
- **Inbound Interface Files (0):**
- **Outbound Interface Files (0):**

### Message_file_package (1) Subsystem
- **Confidence:** High
- **Claim Type:** inferred
- **Member Count:** 1
- **Structurally Ambiguous:** No
- **Grouping Basis:** seed: directory_structure, refined_by: dependency_cohesion
- **Evidence:**
  - Files share directory structure: 'trixelmap/docs/message_file_package (1)'
  - Internal cohesion: 0 internal dependency edges
  - Cross-group coupling: 0 external dependency edges
- **Member Files:**
  - `trixelmap/docs/message_file_package (1)/spatial_authority_extractor.py`
- **Inbound Interface Files (0):**
- **Outbound Interface Files (0):**

### Message_file_package Subsystem
- **Confidence:** High
- **Claim Type:** inferred
- **Member Count:** 2
- **Structurally Ambiguous:** No
- **Grouping Basis:** seed: directory_structure, refined_by: dependency_cohesion
- **Evidence:**
  - Files share directory structure: 'trixelmap/docs/message_file_package (1)/message_file_package'
  - Internal cohesion: 0 internal dependency edges
  - Cross-group coupling: 0 external dependency edges
- **Member Files:**
  - `trixelmap/docs/message_file_package (1)/message_file_package/spatial_authority_extractor.py`
  - `trixelmap/docs/message_file_package (1)/message_file_package/spatial_authority_extractor_2.py`
- **Inbound Interface Files (0):**
- **Outbound Interface Files (0):**

### Message_file_package3 Subsystem
- **Confidence:** High
- **Claim Type:** inferred
- **Member Count:** 2
- **Structurally Ambiguous:** No
- **Grouping Basis:** seed: directory_structure, refined_by: dependency_cohesion
- **Evidence:**
  - Files share directory structure: 'trixelmap/docs/message_file_package3'
  - Internal cohesion: 0 internal dependency edges
  - Cross-group coupling: 0 external dependency edges
- **Member Files:**
  - `trixelmap/docs/message_file_package3/spatial_pattern_matcher.py`
  - `trixelmap/docs/message_file_package3/vault_spatial_parser.py`
- **Inbound Interface Files (0):**
- **Outbound Interface Files (0):**

### Terrain Subsystem
- **Confidence:** Medium
- **Claim Type:** inferred
- **Member Count:** 16
- **Structurally Ambiguous:** No
- **Grouping Basis:** seed: directory_structure, refined_by: dependency_cohesion, refined_by: coordinator_outbound_concentration
- **Evidence:**
  - Files share directory structure: 'terrain'
  - Internal cohesion: 8 internal dependency edges
  - Cross-group coupling: 14 external dependency edges
  - Coordinator cohesion: explicitly named control center emits 8/8 outbound edges (100.0%); internal dependency edges are not required
- **Member Files:**
  - `terrain/__init__.py`
  - `terrain/godot_projection_consumer_contract.py`
  - `terrain/projection_execution_plan.py`
  - `terrain/surface_basis_resolver.py`
  - `terrain/terrain_control_center.py`
  - `terrain/terrain_material_mapping.py`
  - `terrain/terrain_studio_biome_material_adapter.py`
  - `terrain/terrain_studio_height_adapter.py`
  - `terrain/terrain_studio_import_contract.py`
  - `terrain/terrain_surface_basis_contract.py`
  - `terrain/terrain_thresholds.py`
  - `terrain/trixel_retro_surface_paint_document.py`
  - `terrain/trixel_surface_painter_selector.py`
  - `terrain/trixel_world_adapter.py`
  - `terrain/world_field_nucleus.py`
  - `terrain/worldfield_to_worldcell_projection.py`
- **Inbound Interface Files (6):**
  - `terrain/gates/gate_adapter_boundary.py`
  - `terrain/gates/gate_dirty_chunk_or_delta_shape.py`
  - `terrain/gates/gate_imports.py`
  - `terrain/gates/gate_thresholds_exist.py`
  - `terrain/gates/gate_trixel_retro_surface_paint_document.py`
  - `terrain/gates/gate_world_field_boundary.py`
- **Outbound Interface Files (8):**
  - `terrain/gates/gate_adapter_boundary.py`
  - `terrain/gates/gate_dirty_chunk_or_delta_shape.py`
  - `terrain/gates/gate_imports.py`
  - `terrain/gates/gate_no_authority_overreach.py`
  - `terrain/gates/gate_terrain_adapter_rejection_proof.py`
  - `terrain/gates/gate_thresholds_exist.py`
  - `terrain/gates/gate_trixel_retro_surface_paint_document.py`
  - `terrain/gates/gate_world_field_boundary.py`

### Testing Suite
- **Confidence:** High
- **Claim Type:** inferred
- **Member Count:** 3
- **Structurally Ambiguous:** No
- **Grouping Basis:** seed: test_role_hint, refined_by: role_consolidation
- **Evidence:**
  - Consolidated based on test role hints across directories
  - Internal cohesion: 0 internal dependency edges
  - Cross-group coupling: 3 external dependency edges
- **Member Files:**
  - `trixelworld/brushes/test_lisp.py`
  - `trixelworld/test_parse.py`
  - `trixelworld/test_spacing_ratio.py`
- **Inbound Interface Files (0):**
- **Outbound Interface Files (3):**
  - `trixelworld/brushes/gflare_parser_mr.py`
  - `trixelworld/brushes/lisp_parser_mr.py`
  - `trixelworld/trixel_brush_adapter.py`

### Trixelcomposer Subsystem
- **Confidence:** High
- **Claim Type:** inferred
- **Member Count:** 11
- **Structurally Ambiguous:** No
- **Grouping Basis:** seed: directory_structure, refined_by: dependency_cohesion
- **Evidence:**
  - Files share directory structure: 'trixelcomposer'
  - Internal cohesion: 9 internal dependency edges
  - Cross-group coupling: 0 external dependency edges
- **Member Files:**
  - `trixelcomposer/atlas_composer.py`
  - `trixelcomposer/composer_abi_adapter.py`
  - `trixelcomposer/demand_resolver.py`
  - `trixelcomposer/empire_bridge.py`
  - `trixelcomposer/enhanced_trixel_core.py`
  - `trixelcomposer/entity_layer.py`
  - `trixelcomposer/scene_server.py`
  - `trixelcomposer/terminal_trixel.py`
  - `trixelcomposer/tile_address.py`
  - `trixelcomposer/tile_server.py`
  - `trixelcomposer/trixel_render_bridge.py`
- **Inbound Interface Files (0):**
- **Outbound Interface Files (0):**

### Trixelmap Subsystem
- **Confidence:** High
- **Claim Type:** inferred
- **Member Count:** 10
- **Structurally Ambiguous:** No
- **Grouping Basis:** seed: directory_structure, refined_by: dependency_cohesion
- **Evidence:**
  - Files share directory structure: 'trixelmap'
  - Internal cohesion: 3 internal dependency edges
  - Cross-group coupling: 2 external dependency edges
- **Member Files:**
  - `trixelmap/debug_layout_svg.py`
  - `trixelmap/location_ranker.py`
  - `trixelmap/spatial_authority_extractor.py`
  - `trixelmap/spatial_layout_solver.py`
  - `trixelmap/spatial_pattern_matcher.py`
  - `trixelmap/terrain_field_builder.py`
  - `trixelmap/trixel_recipe_writer.py`
  - `trixelmap/trixel_recipes_mr.py`
  - `trixelmap/trixelmap_build.py`
  - `trixelmap/vault_spatial_parser.py`
- **Inbound Interface Files (0):**
- **Outbound Interface Files (2):**
  - `trixelworld/brush_models_mr.py`
  - `trixelworld/trixel_brush_adapter.py`

### Trixelworld Subsystem
- **Confidence:** High
- **Claim Type:** inferred
- **Member Count:** 21
- **Structurally Ambiguous:** No
- **Grouping Basis:** seed: directory_structure, refined_by: dependency_cohesion
- **Evidence:**
  - Files share directory structure: 'trixelworld'
  - Internal cohesion: 49 internal dependency edges
  - Cross-group coupling: 9 external dependency edges
- **Member Files:**
  - `trixelworld/__init__.py`
  - `trixelworld/atmosphere_mr.py`
  - `trixelworld/brush_models_mr.py`
  - `trixelworld/debugerrors.py`
  - `trixelworld/debugnames.py`
  - `trixelworld/demo_beach_material_sheet.py`
  - `trixelworld/demo_bestiary_fauna_sheet.py`
  - `trixelworld/demo_bestiary_flora_sheet.py`
  - `trixelworld/demo_building_material_sheet.py`
  - `trixelworld/engine_debug_mr.py`
  - `trixelworld/engine_mr.py`
  - `trixelworld/palette_mr.py`
  - `trixelworld/render_pictures.py`
  - `trixelworld/scene_models_mr.py`
  - `trixelworld/stress_scene_mr.py`
  - `trixelworld/surface_behavior_mr.py`
  - `trixelworld/testing_space.py`
  - `trixelworld/trixel_brush_adapter.py`
  - `trixelworld/trixel_demo_mr.py`
  - `trixelworld/trixel_recipes_mr.py`
  - `trixelworld/world_tree_mr.py`
- **Inbound Interface Files (2):**
  - `trixelmap/trixel_recipes_mr.py`
  - `trixelworld/test_spacing_ratio.py`
- **Outbound Interface Files (7):**
  - `trixelworld/brushes/gbr_parser_mr.py`
  - `trixelworld/brushes/gdyn_parser_mr.py`
  - `trixelworld/brushes/gfig_parser_mr.py`
  - `trixelworld/brushes/gih_parser_mr.py`
  - `trixelworld/brushes/gpl_parser_mr.py`
  - `trixelworld/brushes/gtp_parser_mr.py`
  - `trixelworld/brushes/vbr_parser_mr.py`

### Unassigned Subsystem
- **Confidence:** High
- **Claim Type:** inferred
- **Member Count:** 1
- **Structurally Ambiguous:** No
- **Grouping Basis:** seed: directory_structure, refined_by: dependency_cohesion
- **Evidence:**
  - Files share directory structure: 'trixelmap/docs/message_file_package/unassigned'
  - Internal cohesion: 0 internal dependency edges
  - Cross-group coupling: 0 external dependency edges
- **Member Files:**
  - `trixelmap/docs/message_file_package/unassigned/extracted_block_001.py`
- **Inbound Interface Files (0):**
- **Outbound Interface Files (0):**

## 3. Top Ranked Next Files to Inspect (Top 10)
1. `trixelmap/docs/message_file_package (1)/message_file_package/spatial_authority_extractor_2.py` (Score: **100**)
   - **Reasons:** parse_error
   - **Evidence:**
     - parse_error: AmbiguousImportError: Import 'spatial_pattern_matcher.extract_spatial_facts' resolved to multiple local candidates: ['trixelmap/docs/message_file_package3/spatial_pattern_matcher.py', 'trixelmap/spatial_pattern_matcher.py'].

2. `trixelmap/docs/message_file_package3/unassigned/extracted_block_004.py` (Score: **100**)
   - **Reasons:** parse_error
   - **Evidence:**
     - parse_error: IndentationError: unexpected indent (extracted_block_004.py, line 1)

3. `trixelmap/docs/message_file_package3/vault_spatial_parser.py` (Score: **100**)
   - **Reasons:** parse_error
   - **Evidence:**
     - parse_error: AmbiguousImportError: Import 'spatial_pattern_matcher.extract_location_mentions' resolved to multiple local candidates: ['trixelmap/docs/message_file_package3/spatial_pattern_matcher.py', 'trixelmap/spatial_pattern_matcher.py'].

4. `trixelmap/docs/message_file_package3/vault_spatial_parser.py` (Score: **100**)
   - **Reasons:** parse_error
   - **Evidence:**
     - parse_error: AmbiguousImportError: Import 'spatial_pattern_matcher.extract_spatial_facts' resolved to multiple local candidates: ['trixelmap/docs/message_file_package3/spatial_pattern_matcher.py', 'trixelmap/spatial_pattern_matcher.py'].

5. `trixelmap/docs/message_file_package3/vault_spatial_parser.py` (Score: **100**)
   - **Reasons:** parse_error
   - **Evidence:**
     - parse_error: AmbiguousImportError: Import 'spatial_pattern_matcher.normalize_id' resolved to multiple local candidates: ['trixelmap/docs/message_file_package3/spatial_pattern_matcher.py', 'trixelmap/spatial_pattern_matcher.py'].

6. `trixelmap/docs/message_file_package3/vault_spatial_parser_2.py` (Score: **100**)
   - **Reasons:** parse_error
   - **Evidence:**
     - parse_error: IndentationError: unexpected indent (vault_spatial_parser_2.py, line 4)

7. `trixelmap/spatial_authority_extractor.py` (Score: **100**)
   - **Reasons:** parse_error
   - **Evidence:**
     - parse_error: AmbiguousImportError: Import 'spatial_pattern_matcher.extract_spatial_facts' resolved to multiple local candidates: ['trixelmap/docs/message_file_package3/spatial_pattern_matcher.py', 'trixelmap/spatial_pattern_matcher.py'].

8. `trixelmap/trixelmap_build.py` (Score: **100**)
   - **Reasons:** parse_error
   - **Evidence:**
     - parse_error: AmbiguousImportError: Import 'spatial_authority_extractor.extract_from_scene_json' resolved to multiple local candidates: ['trixelmap/docs/message_file_package (1)/message_file_package/spatial_authority_extractor.py', 'trixelmap/docs/message_file_package (1)/spatial_authority_extractor.py', 'trixelmap/spatial_authority_extractor.py'].

9. `trixelmap/trixelmap_build.py` (Score: **100**)
   - **Reasons:** parse_error
   - **Evidence:**
     - parse_error: AmbiguousImportError: Import 'spatial_authority_extractor.extract_from_vault_md' resolved to multiple local candidates: ['trixelmap/docs/message_file_package (1)/message_file_package/spatial_authority_extractor.py', 'trixelmap/docs/message_file_package (1)/spatial_authority_extractor.py', 'trixelmap/spatial_authority_extractor.py'].

10. `trixelmap/trixelmap_build.py` (Score: **100**)
   - **Reasons:** parse_error
   - **Evidence:**
     - parse_error: AmbiguousImportError: Import 'spatial_authority_extractor.extract_from_zonj' resolved to multiple local candidates: ['trixelmap/docs/message_file_package (1)/message_file_package/spatial_authority_extractor.py', 'trixelmap/docs/message_file_package (1)/spatial_authority_extractor.py', 'trixelmap/spatial_authority_extractor.py'].

## 4. Path and Dependency Routes
These paths describe **static dependency routes** determined by import statements. The file order reflects the **dependency traversal order** (DFS) from the entrypoint, which is not a proven runtime execution call order. Suggested inspection order is **advisory only**.

### Static Route from entrypoint: `libresprite/gates/gate_libra_asset_provenance_manifest.py`
- **Advisory Next File to Inspect in Route:** `libresprite/gates/gate_libra_asset_provenance_manifest.py`
- **Dependency Traversal Flow:**
  - `libresprite/gates/gate_libra_asset_provenance_manifest.py`

### Static Route from entrypoint: `libresprite/gates/gate_libra_conductor_roundtrip.py`
- **Advisory Next File to Inspect in Route:** `libresprite/gates/gate_libra_conductor_roundtrip.py`
- **Dependency Traversal Flow:**
  - `libresprite/gates/gate_libra_conductor_roundtrip.py`

### Static Route from entrypoint: `libresprite/gates/gate_libra_full_suite.py`
- **Advisory Next File to Inspect in Route:** `libresprite/gates/gate_libra_full_suite.py`
- **Dependency Traversal Flow:**
  - `libresprite/gates/gate_libra_full_suite.py`

### Static Route from entrypoint: `libresprite/gates/gate_libra_real_document_regression.py`
- **Advisory Next File to Inspect in Route:** `libresprite/gates/gate_libra_real_document_regression.py`
- **Dependency Traversal Flow:**
  - `libresprite/gates/gate_libra_real_document_regression.py`

### Static Route from entrypoint: `libresprite/gates/gate_libra_snapshot_backend.py`
- **Advisory Next File to Inspect in Route:** `libresprite/gates/gate_libra_snapshot_backend.py`
- **Dependency Traversal Flow:**
  - `libresprite/gates/gate_libra_snapshot_backend.py`

### Static Route from entrypoint: `libresprite/gates/gate_libra_snapshot_exporter_contract.py`
- **Advisory Next File to Inspect in Route:** `libresprite/gates/gate_libra_snapshot_exporter_contract.py`
- **Dependency Traversal Flow:**
  - `libresprite/gates/gate_libra_snapshot_exporter_contract.py`

### Static Route from entrypoint: `libresprite/gates/gate_libra_snapshot_schema_contract.py`
- **Advisory Next File to Inspect in Route:** `libresprite/gates/gate_libra_snapshot_schema_contract.py`
- **Dependency Traversal Flow:**
  - `libresprite/gates/gate_libra_snapshot_schema_contract.py`

### Static Route from entrypoint: `libresprite/gates/gate_libra_snapshot_stress_set.py`
- **Advisory Next File to Inspect in Route:** `libresprite/gates/gate_libra_snapshot_stress_set.py`
- **Dependency Traversal Flow:**
  - `libresprite/gates/gate_libra_snapshot_stress_set.py`

### Static Route from entrypoint: `libresprite/gates/gate_libresprite_starter_set.py`
- **Advisory Next File to Inspect in Route:** `libresprite/gates/gate_libresprite_starter_set.py`
- **Dependency Traversal Flow:**
  - `libresprite/gates/gate_libresprite_starter_set.py`

### Static Route from entrypoint: `terrain/terrain_control_center.py`
- **Advisory Next File to Inspect in Route:** `terrain/gates/gate_imports.py`
- **Dependency Traversal Flow:**
  - `terrain/terrain_control_center.py`
  - `terrain/gates/gate_adapter_boundary.py` ➔ **Inferred Boundary Crossing:** (Terrain Subsystem ➔ Gates Subsystem)
  - `terrain/trixel_world_adapter.py` ➔ **Inferred Boundary Crossing:** (Gates Subsystem ➔ Terrain Subsystem)
  - `terrain/terrain_thresholds.py`
  - `terrain/world_field_nucleus.py`
  - `terrain/gates/gate_dirty_chunk_or_delta_shape.py` ➔ **Inferred Boundary Crossing:** (Terrain Subsystem ➔ Gates Subsystem)
  - `terrain/gates/gate_imports.py` ➔ **Inferred Boundary Crossing:** (Terrain Subsystem ➔ Gates Subsystem)
  - `terrain/gates/gate_no_authority_overreach.py` ➔ **Inferred Boundary Crossing:** (Terrain Subsystem ➔ Gates Subsystem)
  - `terrain/gates/gate_terrain_adapter_rejection_proof.py` ➔ **Inferred Boundary Crossing:** (Terrain Subsystem ➔ Gates Subsystem)
  - `terrain/gates/gate_thresholds_exist.py` ➔ **Inferred Boundary Crossing:** (Terrain Subsystem ➔ Gates Subsystem)
  - `terrain/gates/gate_trixel_retro_surface_paint_document.py` ➔ **Inferred Boundary Crossing:** (Terrain Subsystem ➔ Gates Subsystem)
  - `terrain/trixel_retro_surface_paint_document.py` ➔ **Inferred Boundary Crossing:** (Gates Subsystem ➔ Terrain Subsystem)
  - `terrain/gates/gate_world_field_boundary.py` ➔ **Inferred Boundary Crossing:** (Terrain Subsystem ➔ Gates Subsystem)

### Static Route from entrypoint: `terrain/terrain_thresholds.py`
- **Advisory Next File to Inspect in Route:** `terrain/terrain_thresholds.py`
- **Dependency Traversal Flow:**
  - `terrain/terrain_thresholds.py`

### Static Route from entrypoint: `terrain/trixel_world_adapter.py`
- **Advisory Next File to Inspect in Route:** `terrain/terrain_thresholds.py`
- **Dependency Traversal Flow:**
  - `terrain/trixel_world_adapter.py`
  - `terrain/terrain_thresholds.py`
  - `terrain/world_field_nucleus.py`

### Static Route from entrypoint: `terrain/world_field_nucleus.py`
- **Advisory Next File to Inspect in Route:** `terrain/world_field_nucleus.py`
- **Dependency Traversal Flow:**
  - `terrain/world_field_nucleus.py`

### Static Route from entrypoint: `trixelcomposer/atlas_composer.py`
- **Advisory Next File to Inspect in Route:** `trixelcomposer/terminal_trixel.py`
- **Dependency Traversal Flow:**
  - `trixelcomposer/atlas_composer.py`
  - `trixelcomposer/scene_server.py`
  - `trixelcomposer/terminal_trixel.py`
  - `trixelcomposer/entity_layer.py`

### Static Route from entrypoint: `trixelcomposer/enhanced_trixel_core.py`
- **Advisory Next File to Inspect in Route:** `trixelcomposer/enhanced_trixel_core.py`
- **Dependency Traversal Flow:**
  - `trixelcomposer/enhanced_trixel_core.py`

### Static Route from entrypoint: `trixelcomposer/scene_server.py`
- **Advisory Next File to Inspect in Route:** `trixelcomposer/scene_server.py`
- **Dependency Traversal Flow:**
  - `trixelcomposer/scene_server.py`

### Static Route from entrypoint: `trixelcomposer/terminal_trixel.py`
- **Advisory Next File to Inspect in Route:** `trixelcomposer/entity_layer.py`
- **Dependency Traversal Flow:**
  - `trixelcomposer/terminal_trixel.py`
  - `trixelcomposer/entity_layer.py`

### Static Route from entrypoint: `trixelcomposer/tile_server.py`
- **Advisory Next File to Inspect in Route:** `trixelcomposer/terminal_trixel.py`
- **Dependency Traversal Flow:**
  - `trixelcomposer/tile_server.py`
  - `trixelcomposer/atlas_composer.py`
  - `trixelcomposer/scene_server.py`
  - `trixelcomposer/terminal_trixel.py`
  - `trixelcomposer/entity_layer.py`
  - `trixelcomposer/trixel_render_bridge.py`

### Static Route from entrypoint: `trixelcomposer/trixel_render_bridge.py`
- **Advisory Next File to Inspect in Route:** `trixelcomposer/terminal_trixel.py`
- **Dependency Traversal Flow:**
  - `trixelcomposer/trixel_render_bridge.py`
  - `trixelcomposer/scene_server.py`
  - `trixelcomposer/terminal_trixel.py`
  - `trixelcomposer/entity_layer.py`

### Static Route from entrypoint: `trixelmap/debug_layout_svg.py`
- **Advisory Next File to Inspect in Route:** `trixelmap/debug_layout_svg.py`
- **Dependency Traversal Flow:**
  - `trixelmap/debug_layout_svg.py`

### Static Route from entrypoint: `trixelmap/docs/message_file_package (1)/message_file_package/spatial_authority_extractor.py`
- **Advisory Next File to Inspect in Route:** `trixelmap/docs/message_file_package (1)/message_file_package/spatial_authority_extractor.py`
- **Dependency Traversal Flow:**
  - `trixelmap/docs/message_file_package (1)/message_file_package/spatial_authority_extractor.py`

### Static Route from entrypoint: `trixelmap/docs/message_file_package (1)/spatial_authority_extractor.py`
- **Advisory Next File to Inspect in Route:** `trixelmap/docs/message_file_package (1)/spatial_authority_extractor.py`
- **Dependency Traversal Flow:**
  - `trixelmap/docs/message_file_package (1)/spatial_authority_extractor.py`

### Static Route from entrypoint: `trixelmap/location_ranker.py`
- **Advisory Next File to Inspect in Route:** `trixelmap/location_ranker.py`
- **Dependency Traversal Flow:**
  - `trixelmap/location_ranker.py`

### Static Route from entrypoint: `trixelmap/spatial_pattern_matcher.py`
- **Advisory Next File to Inspect in Route:** `trixelmap/spatial_pattern_matcher.py`
- **Dependency Traversal Flow:**
  - `trixelmap/spatial_pattern_matcher.py`

### Static Route from entrypoint: `trixelmap/trixel_recipes_mr.py`
- **Advisory Next File to Inspect in Route:** `trixelworld/brushes/gbr_parser_mr.py`
- **Dependency Traversal Flow:**
  - `trixelmap/trixel_recipes_mr.py`
  - `trixelworld/brush_models_mr.py` ➔ **Inferred Boundary Crossing:** (Trixelmap Subsystem ➔ Trixelworld Subsystem)
  - `trixelworld/trixel_brush_adapter.py` ➔ **Inferred Boundary Crossing:** (Trixelmap Subsystem ➔ Trixelworld Subsystem)
  - `trixelworld/brushes/gbr_parser_mr.py` ➔ **Inferred Boundary Crossing:** (Trixelworld Subsystem ➔ Brushes Subsystem)
  - `trixelworld/brushes/gdyn_parser_mr.py` ➔ **Inferred Boundary Crossing:** (Trixelworld Subsystem ➔ Brushes Subsystem)
  - `trixelworld/brushes/gih_parser_mr.py` ➔ **Inferred Boundary Crossing:** (Trixelworld Subsystem ➔ Brushes Subsystem)
  - `trixelworld/brushes/gpl_parser_mr.py` ➔ **Inferred Boundary Crossing:** (Trixelworld Subsystem ➔ Brushes Subsystem)
  - `trixelworld/brushes/gtp_parser_mr.py` ➔ **Inferred Boundary Crossing:** (Trixelworld Subsystem ➔ Brushes Subsystem)
  - `trixelworld/brushes/vbr_parser_mr.py` ➔ **Inferred Boundary Crossing:** (Trixelworld Subsystem ➔ Brushes Subsystem)

### Static Route from entrypoint: `trixelmap/trixelmap_build.py`
- **Advisory Next File to Inspect in Route:** `trixelmap/spatial_layout_solver.py`
- **Dependency Traversal Flow:**
  - `trixelmap/trixelmap_build.py` [PARSE ERROR]
  - `trixelmap/spatial_layout_solver.py`
  - `trixelmap/terrain_field_builder.py`
  - `trixelmap/trixel_recipe_writer.py`

### Static Route from entrypoint: `trixelmap/vault_spatial_parser.py`
- **Advisory Next File to Inspect in Route:** `trixelmap/vault_spatial_parser.py`
- **Dependency Traversal Flow:**
  - `trixelmap/vault_spatial_parser.py` [PARSE ERROR]

### Static Route from entrypoint: `trixelworld/brushes/gbr_parser_mr.py`
- **Advisory Next File to Inspect in Route:** `trixelworld/brushes/gbr_parser_mr.py`
- **Dependency Traversal Flow:**
  - `trixelworld/brushes/gbr_parser_mr.py`

### Static Route from entrypoint: `trixelworld/brushes/gdyn_parser_mr.py`
- **Advisory Next File to Inspect in Route:** `trixelworld/brushes/gdyn_parser_mr.py`
- **Dependency Traversal Flow:**
  - `trixelworld/brushes/gdyn_parser_mr.py`

### Static Route from entrypoint: `trixelworld/brushes/gfig_parser_mr.py`
- **Advisory Next File to Inspect in Route:** `trixelworld/brushes/gfig_parser_mr.py`
- **Dependency Traversal Flow:**
  - `trixelworld/brushes/gfig_parser_mr.py`

### Static Route from entrypoint: `trixelworld/brushes/gih_parser_mr.py`
- **Advisory Next File to Inspect in Route:** `trixelworld/brushes/gih_parser_mr.py`
- **Dependency Traversal Flow:**
  - `trixelworld/brushes/gih_parser_mr.py`

### Static Route from entrypoint: `trixelworld/brushes/gpl_parser_mr.py`
- **Advisory Next File to Inspect in Route:** `trixelworld/brushes/gpl_parser_mr.py`
- **Dependency Traversal Flow:**
  - `trixelworld/brushes/gpl_parser_mr.py`

### Static Route from entrypoint: `trixelworld/brushes/gtp_parser_mr.py`
- **Advisory Next File to Inspect in Route:** `trixelworld/brushes/gtp_parser_mr.py`
- **Dependency Traversal Flow:**
  - `trixelworld/brushes/gtp_parser_mr.py`

### Static Route from entrypoint: `trixelworld/brushes/vbr_parser_mr.py`
- **Advisory Next File to Inspect in Route:** `trixelworld/brushes/vbr_parser_mr.py`
- **Dependency Traversal Flow:**
  - `trixelworld/brushes/vbr_parser_mr.py`

### Static Route from entrypoint: `trixelworld/demo_beach_material_sheet.py`
- **Advisory Next File to Inspect in Route:** `trixelworld/world_tree_mr.py`
- **Dependency Traversal Flow:**
  - `trixelworld/demo_beach_material_sheet.py` [PARSE ERROR]
  - `trixelworld/brush_models_mr.py`
  - `trixelworld/engine_debug_mr.py`
  - `trixelworld/brushes/gbr_parser_mr.py` ➔ **Inferred Boundary Crossing:** (Trixelworld Subsystem ➔ Brushes Subsystem)
  - `trixelworld/engine_mr.py`
  - `trixelworld/brushes/gih_parser_mr.py` ➔ **Inferred Boundary Crossing:** (Trixelworld Subsystem ➔ Brushes Subsystem)
  - `trixelworld/trixel_brush_adapter.py`
  - `trixelworld/brushes/gdyn_parser_mr.py` ➔ **Inferred Boundary Crossing:** (Trixelworld Subsystem ➔ Brushes Subsystem)
  - `trixelworld/brushes/gpl_parser_mr.py` ➔ **Inferred Boundary Crossing:** (Trixelworld Subsystem ➔ Brushes Subsystem)
  - `trixelworld/brushes/gtp_parser_mr.py` ➔ **Inferred Boundary Crossing:** (Trixelworld Subsystem ➔ Brushes Subsystem)
  - `trixelworld/brushes/vbr_parser_mr.py` ➔ **Inferred Boundary Crossing:** (Trixelworld Subsystem ➔ Brushes Subsystem)
  - `trixelworld/world_tree_mr.py` [PARSE ERROR]
  - `trixelworld/brushes/gfig_parser_mr.py` ➔ **Inferred Boundary Crossing:** (Trixelworld Subsystem ➔ Brushes Subsystem)
  - `trixelworld/surface_behavior_mr.py`

### Static Route from entrypoint: `trixelworld/demo_bestiary_fauna_sheet.py`
- **Advisory Next File to Inspect in Route:** `trixelworld/world_tree_mr.py`
- **Dependency Traversal Flow:**
  - `trixelworld/demo_bestiary_fauna_sheet.py` [PARSE ERROR]
  - `trixelworld/engine_debug_mr.py`
  - `trixelworld/brush_models_mr.py`
  - `trixelworld/brushes/gbr_parser_mr.py` ➔ **Inferred Boundary Crossing:** (Trixelworld Subsystem ➔ Brushes Subsystem)
  - `trixelworld/engine_mr.py`
  - `trixelworld/brushes/gih_parser_mr.py` ➔ **Inferred Boundary Crossing:** (Trixelworld Subsystem ➔ Brushes Subsystem)
  - `trixelworld/trixel_brush_adapter.py`
  - `trixelworld/brushes/gdyn_parser_mr.py` ➔ **Inferred Boundary Crossing:** (Trixelworld Subsystem ➔ Brushes Subsystem)
  - `trixelworld/brushes/gpl_parser_mr.py` ➔ **Inferred Boundary Crossing:** (Trixelworld Subsystem ➔ Brushes Subsystem)
  - `trixelworld/brushes/gtp_parser_mr.py` ➔ **Inferred Boundary Crossing:** (Trixelworld Subsystem ➔ Brushes Subsystem)
  - `trixelworld/brushes/vbr_parser_mr.py` ➔ **Inferred Boundary Crossing:** (Trixelworld Subsystem ➔ Brushes Subsystem)
  - `trixelworld/world_tree_mr.py` [PARSE ERROR]
  - `trixelworld/brushes/gfig_parser_mr.py` ➔ **Inferred Boundary Crossing:** (Trixelworld Subsystem ➔ Brushes Subsystem)
  - `trixelworld/surface_behavior_mr.py`

### Static Route from entrypoint: `trixelworld/demo_bestiary_flora_sheet.py`
- **Advisory Next File to Inspect in Route:** `trixelworld/world_tree_mr.py`
- **Dependency Traversal Flow:**
  - `trixelworld/demo_bestiary_flora_sheet.py`
  - `trixelworld/engine_debug_mr.py`
  - `trixelworld/brush_models_mr.py`
  - `trixelworld/brushes/gbr_parser_mr.py` ➔ **Inferred Boundary Crossing:** (Trixelworld Subsystem ➔ Brushes Subsystem)
  - `trixelworld/engine_mr.py`
  - `trixelworld/brushes/gih_parser_mr.py` ➔ **Inferred Boundary Crossing:** (Trixelworld Subsystem ➔ Brushes Subsystem)
  - `trixelworld/trixel_brush_adapter.py`
  - `trixelworld/brushes/gdyn_parser_mr.py` ➔ **Inferred Boundary Crossing:** (Trixelworld Subsystem ➔ Brushes Subsystem)
  - `trixelworld/brushes/gpl_parser_mr.py` ➔ **Inferred Boundary Crossing:** (Trixelworld Subsystem ➔ Brushes Subsystem)
  - `trixelworld/brushes/gtp_parser_mr.py` ➔ **Inferred Boundary Crossing:** (Trixelworld Subsystem ➔ Brushes Subsystem)
  - `trixelworld/brushes/vbr_parser_mr.py` ➔ **Inferred Boundary Crossing:** (Trixelworld Subsystem ➔ Brushes Subsystem)
  - `trixelworld/world_tree_mr.py` [PARSE ERROR]
  - `trixelworld/brushes/gfig_parser_mr.py` ➔ **Inferred Boundary Crossing:** (Trixelworld Subsystem ➔ Brushes Subsystem)
  - `trixelworld/surface_behavior_mr.py`

### Static Route from entrypoint: `trixelworld/demo_building_material_sheet.py`
- **Advisory Next File to Inspect in Route:** `trixelworld/world_tree_mr.py`
- **Dependency Traversal Flow:**
  - `trixelworld/demo_building_material_sheet.py` [PARSE ERROR]
  - `trixelworld/brush_models_mr.py`
  - `trixelworld/engine_debug_mr.py`
  - `trixelworld/brushes/gbr_parser_mr.py` ➔ **Inferred Boundary Crossing:** (Trixelworld Subsystem ➔ Brushes Subsystem)
  - `trixelworld/engine_mr.py`
  - `trixelworld/brushes/gih_parser_mr.py` ➔ **Inferred Boundary Crossing:** (Trixelworld Subsystem ➔ Brushes Subsystem)
  - `trixelworld/trixel_brush_adapter.py`
  - `trixelworld/brushes/gdyn_parser_mr.py` ➔ **Inferred Boundary Crossing:** (Trixelworld Subsystem ➔ Brushes Subsystem)
  - `trixelworld/brushes/gpl_parser_mr.py` ➔ **Inferred Boundary Crossing:** (Trixelworld Subsystem ➔ Brushes Subsystem)
  - `trixelworld/brushes/gtp_parser_mr.py` ➔ **Inferred Boundary Crossing:** (Trixelworld Subsystem ➔ Brushes Subsystem)
  - `trixelworld/brushes/vbr_parser_mr.py` ➔ **Inferred Boundary Crossing:** (Trixelworld Subsystem ➔ Brushes Subsystem)
  - `trixelworld/world_tree_mr.py` [PARSE ERROR]
  - `trixelworld/brushes/gfig_parser_mr.py` ➔ **Inferred Boundary Crossing:** (Trixelworld Subsystem ➔ Brushes Subsystem)
  - `trixelworld/surface_behavior_mr.py`

### Static Route from entrypoint: `trixelworld/engine_debug_mr.py`
- **Advisory Next File to Inspect in Route:** `trixelworld/brushes/gbr_parser_mr.py`
- **Dependency Traversal Flow:**
  - `trixelworld/engine_debug_mr.py`
  - `trixelworld/brush_models_mr.py`
  - `trixelworld/brushes/gbr_parser_mr.py` ➔ **Inferred Boundary Crossing:** (Trixelworld Subsystem ➔ Brushes Subsystem)
  - `trixelworld/engine_mr.py`
  - `trixelworld/brushes/gih_parser_mr.py` ➔ **Inferred Boundary Crossing:** (Trixelworld Subsystem ➔ Brushes Subsystem)
  - `trixelworld/trixel_brush_adapter.py`
  - `trixelworld/brushes/gdyn_parser_mr.py` ➔ **Inferred Boundary Crossing:** (Trixelworld Subsystem ➔ Brushes Subsystem)
  - `trixelworld/brushes/gpl_parser_mr.py` ➔ **Inferred Boundary Crossing:** (Trixelworld Subsystem ➔ Brushes Subsystem)
  - `trixelworld/brushes/gtp_parser_mr.py` ➔ **Inferred Boundary Crossing:** (Trixelworld Subsystem ➔ Brushes Subsystem)
  - `trixelworld/brushes/vbr_parser_mr.py` ➔ **Inferred Boundary Crossing:** (Trixelworld Subsystem ➔ Brushes Subsystem)

### Static Route from entrypoint: `trixelworld/engine_mr.py`
- **Advisory Next File to Inspect in Route:** `trixelworld/brushes/gbr_parser_mr.py`
- **Dependency Traversal Flow:**
  - `trixelworld/engine_mr.py`
  - `trixelworld/brush_models_mr.py`
  - `trixelworld/brushes/gbr_parser_mr.py` ➔ **Inferred Boundary Crossing:** (Trixelworld Subsystem ➔ Brushes Subsystem)
  - `trixelworld/brushes/gih_parser_mr.py` ➔ **Inferred Boundary Crossing:** (Trixelworld Subsystem ➔ Brushes Subsystem)
  - `trixelworld/trixel_brush_adapter.py`
  - `trixelworld/brushes/gdyn_parser_mr.py` ➔ **Inferred Boundary Crossing:** (Trixelworld Subsystem ➔ Brushes Subsystem)
  - `trixelworld/brushes/gpl_parser_mr.py` ➔ **Inferred Boundary Crossing:** (Trixelworld Subsystem ➔ Brushes Subsystem)
  - `trixelworld/brushes/gtp_parser_mr.py` ➔ **Inferred Boundary Crossing:** (Trixelworld Subsystem ➔ Brushes Subsystem)
  - `trixelworld/brushes/vbr_parser_mr.py` ➔ **Inferred Boundary Crossing:** (Trixelworld Subsystem ➔ Brushes Subsystem)

### Static Route from entrypoint: `trixelworld/palette_mr.py`
- **Advisory Next File to Inspect in Route:** `trixelworld/brushes/gbr_parser_mr.py`
- **Dependency Traversal Flow:**
  - `trixelworld/palette_mr.py`
  - `trixelworld/brush_models_mr.py`
  - `trixelworld/trixel_brush_adapter.py`
  - `trixelworld/brushes/gbr_parser_mr.py` ➔ **Inferred Boundary Crossing:** (Trixelworld Subsystem ➔ Brushes Subsystem)
  - `trixelworld/brushes/gdyn_parser_mr.py` ➔ **Inferred Boundary Crossing:** (Trixelworld Subsystem ➔ Brushes Subsystem)
  - `trixelworld/brushes/gih_parser_mr.py` ➔ **Inferred Boundary Crossing:** (Trixelworld Subsystem ➔ Brushes Subsystem)
  - `trixelworld/brushes/gpl_parser_mr.py` ➔ **Inferred Boundary Crossing:** (Trixelworld Subsystem ➔ Brushes Subsystem)
  - `trixelworld/brushes/gtp_parser_mr.py` ➔ **Inferred Boundary Crossing:** (Trixelworld Subsystem ➔ Brushes Subsystem)
  - `trixelworld/brushes/vbr_parser_mr.py` ➔ **Inferred Boundary Crossing:** (Trixelworld Subsystem ➔ Brushes Subsystem)

### Static Route from entrypoint: `trixelworld/stress_scene_mr.py`
- **Advisory Next File to Inspect in Route:** `trixelworld/world_tree_mr.py`
- **Dependency Traversal Flow:**
  - `trixelworld/stress_scene_mr.py` [PARSE ERROR]
  - `trixelworld/brush_models_mr.py`
  - `trixelworld/engine_debug_mr.py`
  - `trixelworld/brushes/gbr_parser_mr.py` ➔ **Inferred Boundary Crossing:** (Trixelworld Subsystem ➔ Brushes Subsystem)
  - `trixelworld/engine_mr.py`
  - `trixelworld/brushes/gih_parser_mr.py` ➔ **Inferred Boundary Crossing:** (Trixelworld Subsystem ➔ Brushes Subsystem)
  - `trixelworld/trixel_brush_adapter.py`
  - `trixelworld/brushes/gdyn_parser_mr.py` ➔ **Inferred Boundary Crossing:** (Trixelworld Subsystem ➔ Brushes Subsystem)
  - `trixelworld/brushes/gpl_parser_mr.py` ➔ **Inferred Boundary Crossing:** (Trixelworld Subsystem ➔ Brushes Subsystem)
  - `trixelworld/brushes/gtp_parser_mr.py` ➔ **Inferred Boundary Crossing:** (Trixelworld Subsystem ➔ Brushes Subsystem)
  - `trixelworld/brushes/vbr_parser_mr.py` ➔ **Inferred Boundary Crossing:** (Trixelworld Subsystem ➔ Brushes Subsystem)
  - `trixelworld/palette_mr.py`
  - `trixelworld/world_tree_mr.py` [PARSE ERROR]
  - `trixelworld/brushes/gfig_parser_mr.py` ➔ **Inferred Boundary Crossing:** (Trixelworld Subsystem ➔ Brushes Subsystem)
  - `trixelworld/surface_behavior_mr.py`

### Static Route from entrypoint: `trixelworld/surface_behavior_mr.py`
- **Advisory Next File to Inspect in Route:** `trixelworld/surface_behavior_mr.py`
- **Dependency Traversal Flow:**
  - `trixelworld/surface_behavior_mr.py`

### Static Route from entrypoint: `trixelworld/trixel_brush_adapter.py`
- **Advisory Next File to Inspect in Route:** `trixelworld/brushes/gbr_parser_mr.py`
- **Dependency Traversal Flow:**
  - `trixelworld/trixel_brush_adapter.py`
  - `trixelworld/brush_models_mr.py`
  - `trixelworld/brushes/gbr_parser_mr.py` ➔ **Inferred Boundary Crossing:** (Trixelworld Subsystem ➔ Brushes Subsystem)
  - `trixelworld/brushes/gdyn_parser_mr.py` ➔ **Inferred Boundary Crossing:** (Trixelworld Subsystem ➔ Brushes Subsystem)
  - `trixelworld/brushes/gih_parser_mr.py` ➔ **Inferred Boundary Crossing:** (Trixelworld Subsystem ➔ Brushes Subsystem)
  - `trixelworld/brushes/gpl_parser_mr.py` ➔ **Inferred Boundary Crossing:** (Trixelworld Subsystem ➔ Brushes Subsystem)
  - `trixelworld/brushes/gtp_parser_mr.py` ➔ **Inferred Boundary Crossing:** (Trixelworld Subsystem ➔ Brushes Subsystem)
  - `trixelworld/brushes/vbr_parser_mr.py` ➔ **Inferred Boundary Crossing:** (Trixelworld Subsystem ➔ Brushes Subsystem)

### Static Route from entrypoint: `trixelworld/trixel_demo_mr.py`
- **Advisory Next File to Inspect in Route:** `trixelworld/brushes/gbr_parser_mr.py`
- **Dependency Traversal Flow:**
  - `trixelworld/trixel_demo_mr.py` [PARSE ERROR]
  - `trixelworld/engine_debug_mr.py`
  - `trixelworld/brush_models_mr.py`
  - `trixelworld/brushes/gbr_parser_mr.py` ➔ **Inferred Boundary Crossing:** (Trixelworld Subsystem ➔ Brushes Subsystem)
  - `trixelworld/engine_mr.py`
  - `trixelworld/brushes/gih_parser_mr.py` ➔ **Inferred Boundary Crossing:** (Trixelworld Subsystem ➔ Brushes Subsystem)
  - `trixelworld/trixel_brush_adapter.py`
  - `trixelworld/brushes/gdyn_parser_mr.py` ➔ **Inferred Boundary Crossing:** (Trixelworld Subsystem ➔ Brushes Subsystem)
  - `trixelworld/brushes/gpl_parser_mr.py` ➔ **Inferred Boundary Crossing:** (Trixelworld Subsystem ➔ Brushes Subsystem)
  - `trixelworld/brushes/gtp_parser_mr.py` ➔ **Inferred Boundary Crossing:** (Trixelworld Subsystem ➔ Brushes Subsystem)
  - `trixelworld/brushes/vbr_parser_mr.py` ➔ **Inferred Boundary Crossing:** (Trixelworld Subsystem ➔ Brushes Subsystem)
  - `trixelworld/palette_mr.py`

### Static Route from entrypoint: `trixelworld/trixel_recipes_mr.py`
- **Advisory Next File to Inspect in Route:** `trixelworld/brushes/gbr_parser_mr.py`
- **Dependency Traversal Flow:**
  - `trixelworld/trixel_recipes_mr.py`
  - `trixelworld/brush_models_mr.py`
  - `trixelworld/trixel_brush_adapter.py`
  - `trixelworld/brushes/gbr_parser_mr.py` ➔ **Inferred Boundary Crossing:** (Trixelworld Subsystem ➔ Brushes Subsystem)
  - `trixelworld/brushes/gdyn_parser_mr.py` ➔ **Inferred Boundary Crossing:** (Trixelworld Subsystem ➔ Brushes Subsystem)
  - `trixelworld/brushes/gih_parser_mr.py` ➔ **Inferred Boundary Crossing:** (Trixelworld Subsystem ➔ Brushes Subsystem)
  - `trixelworld/brushes/gpl_parser_mr.py` ➔ **Inferred Boundary Crossing:** (Trixelworld Subsystem ➔ Brushes Subsystem)
  - `trixelworld/brushes/gtp_parser_mr.py` ➔ **Inferred Boundary Crossing:** (Trixelworld Subsystem ➔ Brushes Subsystem)
  - `trixelworld/brushes/vbr_parser_mr.py` ➔ **Inferred Boundary Crossing:** (Trixelworld Subsystem ➔ Brushes Subsystem)

### Static Route from entrypoint: `trixelworld/world_tree_mr.py`
- **Advisory Next File to Inspect in Route:** `trixelworld/brushes/gbr_parser_mr.py`
- **Dependency Traversal Flow:**
  - `trixelworld/world_tree_mr.py` [PARSE ERROR]
  - `trixelworld/brushes/gfig_parser_mr.py` ➔ **Inferred Boundary Crossing:** (Trixelworld Subsystem ➔ Brushes Subsystem)
  - `trixelworld/engine_debug_mr.py`
  - `trixelworld/brush_models_mr.py`
  - `trixelworld/brushes/gbr_parser_mr.py` ➔ **Inferred Boundary Crossing:** (Trixelworld Subsystem ➔ Brushes Subsystem)
  - `trixelworld/engine_mr.py`
  - `trixelworld/brushes/gih_parser_mr.py` ➔ **Inferred Boundary Crossing:** (Trixelworld Subsystem ➔ Brushes Subsystem)
  - `trixelworld/trixel_brush_adapter.py`
  - `trixelworld/brushes/gdyn_parser_mr.py` ➔ **Inferred Boundary Crossing:** (Trixelworld Subsystem ➔ Brushes Subsystem)
  - `trixelworld/brushes/gpl_parser_mr.py` ➔ **Inferred Boundary Crossing:** (Trixelworld Subsystem ➔ Brushes Subsystem)
  - `trixelworld/brushes/gtp_parser_mr.py` ➔ **Inferred Boundary Crossing:** (Trixelworld Subsystem ➔ Brushes Subsystem)
  - `trixelworld/brushes/vbr_parser_mr.py` ➔ **Inferred Boundary Crossing:** (Trixelworld Subsystem ➔ Brushes Subsystem)
  - `trixelworld/surface_behavior_mr.py`

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
