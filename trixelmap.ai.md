# Code Atlas AI Architecture Report: trixelmap

- **Contract:** code_atlas.ai_architecture_packet (v1.0.0)
- **Scanned At:** 2026-07-10T05:09:09.756976Z

## Static Reachability Warning
> [!WARNING]
> WARNING: Static dependency routes and reachability results are derived solely from import statements. They indicate potential compile-time or static dependencies and do not reflect runtime execution sequence, call order, or dynamic control flow.

## Limitations
- Namespace packages without __init__.py are supported, but ambiguous resolutions (multiple candidates matching the same import) are recorded as gaps. (Claim: `gap`, Confidence: `high`)
- Reflection and dynamic attribute retrieval may hide runtime dependencies. (Claim: `gap`, Confidence: `high`)
- Static analysis cannot resolve dynamic imports (e.g. __import__, importlib, or dynamic string execution). (Claim: `gap`, Confidence: `high`)
- Static route paths are inferred from import syntax, not runtime-verified. (Claim: `gap`, Confidence: `medium`)

## Subsystem Summaries
- **Message_file_package (1) Subsystem**
  - Claim: `inferred`, Confidence: `high`, Member Count: 1
  - Grouping Basis: refined_by: dependency_cohesion, seed: directory_structure
- **Message_file_package Subsystem** [AMBIGUOUS]
  - Claim: `inferred`, Confidence: `low`, Member Count: 2
  - Grouping Basis: refined_by: dependency_cohesion, seed: directory_structure
- **Message_file_package3 Subsystem** [AMBIGUOUS]
  - Claim: `inferred`, Confidence: `low`, Member Count: 2
  - Grouping Basis: refined_by: dependency_cohesion, seed: directory_structure
- **Root Components**
  - Claim: `inferred`, Confidence: `high`, Member Count: 10
  - Grouping Basis: refined_by: dependency_cohesion, seed: directory_structure
- **Unassigned Subsystem**
  - Claim: `inferred`, Confidence: `high`, Member Count: 1
  - Grouping Basis: refined_by: dependency_cohesion, seed: directory_structure

## Top Inspection Targets (Detail: standard)
1. `docs/message_file_package3/unassigned/extracted_block_004.py` (Score: **100**)
   - Claim: `inferred`, Reasons: parse_error
2. `docs/message_file_package3/vault_spatial_parser_2.py` (Score: **100**)
   - Claim: `inferred`, Reasons: parse_error
3. `docs/message_file_package3/spatial_pattern_matcher.py` (Score: **70**)
   - Claim: `inferred`, Reasons: orphaned_with_code, structurally_ambiguous_subsystem
4. `docs/message_file_package (1)/message_file_package/spatial_authority_extractor_2.py` (Score: **52**)
   - Claim: `inferred`, Reasons: high_outbound_coupling, structurally_ambiguous_subsystem
5. `docs/message_file_package3/vault_spatial_parser.py` (Score: **52**)
   - Claim: `inferred`, Reasons: high_outbound_coupling, structurally_ambiguous_subsystem
6. `docs/message_file_package (1)/message_file_package/spatial_authority_extractor.py` (Score: **50**)
   - Claim: `inferred`, Reasons: structurally_ambiguous_subsystem
7. `docs/message_file_package/unassigned/extracted_block_001.py` (Score: **20**)
   - Claim: `inferred`, Reasons: orphaned_with_code
8. `spatial_pattern_matcher.py` (Score: **20**)
   - Claim: `inferred`, Reasons: high_inbound_coupling
9. `trixelmap_build.py` (Score: **8**)
   - Claim: `inferred`, Reasons: high_outbound_coupling
10. `spatial_authority_extractor.py` (Score: **7**)
   - Claim: `inferred`, Reasons: high_inbound_coupling, high_outbound_coupling
11. `debug_layout_svg.py` (Score: **5**)
   - Claim: `inferred`, Reasons: routine_inspection
12. `docs/message_file_package (1)/spatial_authority_extractor.py` (Score: **5**)
   - Claim: `inferred`, Reasons: routine_inspection
13. `location_ranker.py` (Score: **5**)
   - Claim: `inferred`, Reasons: routine_inspection
14. `spatial_layout_solver.py` (Score: **5**)
   - Claim: `inferred`, Reasons: high_inbound_coupling
15. `terrain_field_builder.py` (Score: **5**)
   - Claim: `inferred`, Reasons: high_inbound_coupling
16. `trixel_recipe_writer.py` (Score: **5**)
   - Claim: `inferred`, Reasons: high_inbound_coupling
17. `trixel_recipes_mr.py` (Score: **5**)
   - Claim: `inferred`, Reasons: routine_inspection
18. `vault_spatial_parser.py` (Score: **2**)
   - Claim: `inferred`, Reasons: high_outbound_coupling

## Unresolved Gaps & Parse Errors
- `docs/message_file_package3/unassigned/extracted_block_004.py`: IndentationError: unexpected indent (extracted_block_004.py, line 1) (Claim: `gap`)
- `docs/message_file_package3/vault_spatial_parser_2.py`: IndentationError: unexpected indent (vault_spatial_parser_2.py, line 4) (Claim: `gap`)

## Cross-Subsystem Boundaries
No boundaries crossed by static dependency paths.

## Route Summaries
### Grouped Single-File Routes
- Type: `single_file_static_route` (Claim: `inferred`, Count: 6)
  - `debug_layout_svg.py`
  - `docs/message_file_package (1)/message_file_package/spatial_authority_extractor.py`
  - `docs/message_file_package (1)/spatial_authority_extractor.py`
  - `location_ranker.py`
  - `spatial_pattern_matcher.py`
  - `trixel_recipes_mr.py`

### Multi-File Static Routes
- Entrypoint: `trixelmap_build.py` (Claim: `inferred`)
  - Length: 6, Advisory Next Step: `spatial_pattern_matcher.py`
  - Boundary Crossings Count: 0
- Entrypoint: `vault_spatial_parser.py` (Claim: `inferred`)
  - Length: 2, Advisory Next Step: `spatial_pattern_matcher.py`
  - Boundary Crossings Count: 0
