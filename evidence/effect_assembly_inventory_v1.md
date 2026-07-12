# EFFECT implementation inventory — current tree

## Preconditions

Fixture A command:

```text
python3 -m unittest code_atlas.tests.test_payload_analyzer.TestPayloadAnalyzerRestructured.test_i_json_dump_sink_value_provenance -v
```

Raw result:

```text
test_i_json_dump_sink_value_provenance ... ok
Ran 1 test in 0.002s
OK
```

## Specification mapping

| Requirement | Surviving implementation | Status |
|---|---|---|
| Serializer sink-value provenance | `PayloadCandidateASTVisitor._resolve_parameter_origin_keys`; `terminal_writes[].origin_keys`; artifact-path join | partially implemented |
| FILE_WRITE sink taxonomy | allowlisted `json`, `pickle`, `yaml`.dump with literal write handles | partially implemented |
| STATE_MUTATION | none | specification only |
| NETWORK_EMIT | none | specification only |
| PROCESS_BOUNDARY | none | specification only |
| EFFECTIVE | none | specification only |
| STRANDED | none | specification only |
| DROPPED | only `unutilized_keys`, not an effect verdict | partially implemented |
| UNCLASSIFIED_TERMINUS | none | specification only |
| Claim schema / traced path | none | specification only |
| Known non-terminal denylist | none | specification only |
| Access modes | accessed key set only | specification only |
| BUILD_INFLUENCE | none | specification only |
| Reporter-resolved route qualification | `local_dependencies` passed to `analyze_payload_handoffs`; unique defining target required | implemented |

## Missing named document

`sink_provenance_ticket.md` is absent under that filename. Its serializer-provenance prerequisite survives in code and the runnable Fixture A regression above.

## Focused target identity

The only discovered `world_field_nucleus.py` is:

`/home/mytruelove/Desktop/burdens_of_a_forgotten_past/conductor/conductor_building_blocks/terrain/world_field_nucleus.py`

It does not contain `elevation_center`, `cell_width`, `cell_depth`, `_smooth`, or `np.pad`. The known validation targets are in:

- `trixelmap/trixel_recipe_writer.py`
- `trixelmap/terrain_field_builder.py`

The focused run must not attribute those findings to `world_field_nucleus.py`.
