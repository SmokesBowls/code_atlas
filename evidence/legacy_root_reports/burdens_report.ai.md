# Code Atlas AI Architecture Report: conductor_building_blocks

- **Contract:** code_atlas.ai_architecture_packet (v1.0.0)
- **Scanned At:** 2026-07-10T03:14:28.160629Z

## Static Reachability Warning
> [!WARNING]
> WARNING: Static dependency routes and reachability results are derived solely from import statements. They indicate potential compile-time or static dependencies and do not reflect runtime execution sequence, call order, or dynamic control flow.

## Limitations
- Namespace packages without __init__.py are supported, but ambiguous resolutions (multiple candidates matching the same import) are recorded as gaps. (Claim: `gap`, Confidence: `high`)
- Reflection and dynamic attribute retrieval may hide runtime dependencies. (Claim: `gap`, Confidence: `high`)
- Static analysis cannot resolve dynamic imports (e.g. __import__, importlib, or dynamic string execution). (Claim: `gap`, Confidence: `high`)
- Static route paths are inferred from import syntax, not runtime-verified. (Claim: `gap`, Confidence: `medium`)

## Subsystem Summaries
- **Brushes Subsystem**
  - Claim: `inferred`, Confidence: `high`, Member Count: 12
  - Grouping Basis: refined_by: dependency_cohesion, seed: directory_structure
- **Gates Subsystem** [AMBIGUOUS]
  - Claim: `inferred`, Confidence: `medium`, Member Count: 17
  - Grouping Basis: refined_by: dependency_cohesion, seed: directory_structure
- **Libresprite Subsystem**
  - Claim: `inferred`, Confidence: `high`, Member Count: 10
  - Grouping Basis: refined_by: dependency_cohesion, seed: directory_structure
- **Message_file_package (1) Subsystem**
  - Claim: `inferred`, Confidence: `high`, Member Count: 1
  - Grouping Basis: refined_by: dependency_cohesion, seed: directory_structure
- **Message_file_package Subsystem**
  - Claim: `inferred`, Confidence: `high`, Member Count: 2
  - Grouping Basis: refined_by: dependency_cohesion, seed: directory_structure
- **Message_file_package3 Subsystem**
  - Claim: `inferred`, Confidence: `high`, Member Count: 2
  - Grouping Basis: refined_by: dependency_cohesion, seed: directory_structure
- **Terrain Subsystem**
  - Claim: `inferred`, Confidence: `high`, Member Count: 16
  - Grouping Basis: refined_by: dependency_cohesion, seed: directory_structure
- **Testing Suite**
  - Claim: `inferred`, Confidence: `high`, Member Count: 3
  - Grouping Basis: refined_by: role_consolidation, seed: test_role_hint
- **Trixelcomposer Subsystem**
  - Claim: `inferred`, Confidence: `high`, Member Count: 11
  - Grouping Basis: refined_by: dependency_cohesion, seed: directory_structure
- **Trixelmap Subsystem**
  - Claim: `inferred`, Confidence: `high`, Member Count: 10
  - Grouping Basis: refined_by: dependency_cohesion, seed: directory_structure
- **Trixelworld Subsystem**
  - Claim: `inferred`, Confidence: `high`, Member Count: 21
  - Grouping Basis: refined_by: dependency_cohesion, seed: directory_structure
- **Unassigned Subsystem**
  - Claim: `inferred`, Confidence: `high`, Member Count: 1
  - Grouping Basis: refined_by: dependency_cohesion, seed: directory_structure

## Top Inspection Targets (Detail: standard)
1. `trixelmap/docs/message_file_package3/unassigned/extracted_block_004.py` (Score: **100**)
   - Claim: `inferred`, Reasons: parse_error
2. `trixelmap/docs/message_file_package3/vault_spatial_parser_2.py` (Score: **100**)
   - Claim: `inferred`, Reasons: parse_error
3. `terrain/gates/gate_imports.py` (Score: **61**)
   - Claim: `inferred`, Reasons: high_inbound_coupling, high_outbound_coupling, structurally_ambiguous_subsystem
4. `terrain/gates/gate_no_authority_overreach.py` (Score: **60**)
   - Claim: `inferred`, Reasons: high_inbound_coupling, structurally_ambiguous_subsystem
5. `terrain/gates/gate_adapter_boundary.py` (Score: **57**)
   - Claim: `inferred`, Reasons: high_inbound_coupling, high_outbound_coupling, structurally_ambiguous_subsystem
6. `terrain/gates/gate_dirty_chunk_or_delta_shape.py` (Score: **57**)
   - Claim: `inferred`, Reasons: high_inbound_coupling, high_outbound_coupling, structurally_ambiguous_subsystem
7. `terrain/gates/gate_terrain_adapter_rejection_proof.py` (Score: **57**)
   - Claim: `inferred`, Reasons: high_inbound_coupling, high_outbound_coupling, structurally_ambiguous_subsystem
8. `terrain/gates/gate_thresholds_exist.py` (Score: **57**)
   - Claim: `inferred`, Reasons: high_inbound_coupling, high_outbound_coupling, structurally_ambiguous_subsystem
9. `terrain/gates/gate_trixel_retro_surface_paint_document.py` (Score: **57**)
   - Claim: `inferred`, Reasons: high_inbound_coupling, high_outbound_coupling, structurally_ambiguous_subsystem
10. `terrain/gates/gate_world_field_boundary.py` (Score: **57**)
   - Claim: `inferred`, Reasons: high_inbound_coupling, high_outbound_coupling, structurally_ambiguous_subsystem
11. `libresprite/gates/gate_libra_asset_provenance_manifest.py` (Score: **50**)
   - Claim: `inferred`, Reasons: structurally_ambiguous_subsystem
12. `libresprite/gates/gate_libra_conductor_roundtrip.py` (Score: **50**)
   - Claim: `inferred`, Reasons: structurally_ambiguous_subsystem
13. `libresprite/gates/gate_libra_full_suite.py` (Score: **50**)
   - Claim: `inferred`, Reasons: structurally_ambiguous_subsystem
14. `libresprite/gates/gate_libra_real_document_regression.py` (Score: **50**)
   - Claim: `inferred`, Reasons: structurally_ambiguous_subsystem
15. `libresprite/gates/gate_libra_snapshot_backend.py` (Score: **50**)
   - Claim: `inferred`, Reasons: structurally_ambiguous_subsystem
16. `libresprite/gates/gate_libra_snapshot_exporter_contract.py` (Score: **50**)
   - Claim: `inferred`, Reasons: structurally_ambiguous_subsystem
17. `libresprite/gates/gate_libra_snapshot_schema_contract.py` (Score: **50**)
   - Claim: `inferred`, Reasons: structurally_ambiguous_subsystem
18. `libresprite/gates/gate_libra_snapshot_stress_set.py` (Score: **50**)
   - Claim: `inferred`, Reasons: structurally_ambiguous_subsystem
19. `libresprite/gates/gate_libresprite_starter_set.py` (Score: **50**)
   - Claim: `inferred`, Reasons: structurally_ambiguous_subsystem
20. `libresprite/ls_cel_parser_mr.py` (Score: **40**)
   - Claim: `inferred`, Reasons: high_inbound_coupling, stubbed_implementation

## Unresolved Gaps & Parse Errors
- `trixelmap/docs/message_file_package3/unassigned/extracted_block_004.py`: IndentationError: unexpected indent (extracted_block_004.py, line 1) (Claim: `gap`)
- `trixelmap/docs/message_file_package3/vault_spatial_parser_2.py`: IndentationError: unexpected indent (vault_spatial_parser_2.py, line 4) (Claim: `gap`)

## Cross-Subsystem Boundaries
- `terrain/trixel_retro_surface_paint_document.py`: Boundary `Gates Subsystem` ➔ `Terrain Subsystem` (Claim: `inferred`)
- `terrain/trixel_world_adapter.py`: Boundary `Gates Subsystem` ➔ `Terrain Subsystem` (Claim: `inferred`)
- `terrain/gates/gate_adapter_boundary.py`: Boundary `Terrain Subsystem` ➔ `Gates Subsystem` (Claim: `inferred`)
- `terrain/gates/gate_dirty_chunk_or_delta_shape.py`: Boundary `Terrain Subsystem` ➔ `Gates Subsystem` (Claim: `inferred`)
- `terrain/gates/gate_imports.py`: Boundary `Terrain Subsystem` ➔ `Gates Subsystem` (Claim: `inferred`)
- `terrain/gates/gate_no_authority_overreach.py`: Boundary `Terrain Subsystem` ➔ `Gates Subsystem` (Claim: `inferred`)
- `terrain/gates/gate_terrain_adapter_rejection_proof.py`: Boundary `Terrain Subsystem` ➔ `Gates Subsystem` (Claim: `inferred`)
- `terrain/gates/gate_thresholds_exist.py`: Boundary `Terrain Subsystem` ➔ `Gates Subsystem` (Claim: `inferred`)
- `terrain/gates/gate_trixel_retro_surface_paint_document.py`: Boundary `Terrain Subsystem` ➔ `Gates Subsystem` (Claim: `inferred`)
- `terrain/gates/gate_world_field_boundary.py`: Boundary `Terrain Subsystem` ➔ `Gates Subsystem` (Claim: `inferred`)

## Route Summaries
### Grouped Single-File Routes
- Type: `single_file_static_route` (Claim: `inferred`, Count: 45)
  - `libresprite/gates/gate_libra_asset_provenance_manifest.py`
  - `libresprite/gates/gate_libra_conductor_roundtrip.py`
  - `libresprite/gates/gate_libra_full_suite.py`
  - `libresprite/gates/gate_libra_real_document_regression.py`
  - `libresprite/gates/gate_libra_snapshot_backend.py`
  - `libresprite/gates/gate_libra_snapshot_exporter_contract.py`
  - `libresprite/gates/gate_libra_snapshot_schema_contract.py`
  - `libresprite/gates/gate_libra_snapshot_stress_set.py`
  - `libresprite/gates/gate_libresprite_starter_set.py`
  - `terrain/terrain_thresholds.py`
  - `terrain/world_field_nucleus.py`
  - `trixelcomposer/atlas_composer.py`
  - `trixelcomposer/enhanced_trixel_core.py`
  - `trixelcomposer/scene_server.py`
  - `trixelcomposer/terminal_trixel.py`
  - `trixelcomposer/tile_server.py`
  - `trixelcomposer/trixel_render_bridge.py`
  - `trixelmap/debug_layout_svg.py`
  - `trixelmap/docs/message_file_package (1)/message_file_package/spatial_authority_extractor.py`
  - `trixelmap/docs/message_file_package (1)/spatial_authority_extractor.py`
  - `trixelmap/location_ranker.py`
  - `trixelmap/spatial_pattern_matcher.py`
  - `trixelmap/trixel_recipes_mr.py`
  - `trixelmap/trixelmap_build.py`
  - `trixelmap/vault_spatial_parser.py`
  - `trixelworld/brushes/gbr_parser_mr.py`
  - `trixelworld/brushes/gdyn_parser_mr.py`
  - `trixelworld/brushes/gfig_parser_mr.py`
  - `trixelworld/brushes/gih_parser_mr.py`
  - `trixelworld/brushes/gpl_parser_mr.py`
  - `trixelworld/brushes/gtp_parser_mr.py`
  - `trixelworld/brushes/vbr_parser_mr.py`
  - `trixelworld/demo_beach_material_sheet.py`
  - `trixelworld/demo_bestiary_fauna_sheet.py`
  - `trixelworld/demo_bestiary_flora_sheet.py`
  - `trixelworld/demo_building_material_sheet.py`
  - `trixelworld/engine_debug_mr.py`
  - `trixelworld/engine_mr.py`
  - `trixelworld/palette_mr.py`
  - `trixelworld/stress_scene_mr.py`
  - `trixelworld/surface_behavior_mr.py`
  - `trixelworld/trixel_brush_adapter.py`
  - `trixelworld/trixel_demo_mr.py`
  - `trixelworld/trixel_recipes_mr.py`
  - `trixelworld/world_tree_mr.py`

### Multi-File Static Routes
- Entrypoint: `terrain/terrain_control_center.py` (Claim: `inferred`)
  - Length: 13, Advisory Next Step: `terrain/gates/gate_imports.py`
  - Boundary Crossings Count: 10
- Entrypoint: `terrain/trixel_world_adapter.py` (Claim: `inferred`)
  - Length: 3, Advisory Next Step: `terrain/terrain_thresholds.py`
  - Boundary Crossings Count: 0
