# Code Atlas Component Relationship Report: EngAIn

**Scanned at:** 2026-07-12T14:09:42.750218Z

## 1. Project Overview
- **Total Files Scanned:** 400
- **Total Parse Errors (Gaps):** 2
- **Detected Entrypoints:** start_button.py, engainos_boot_kernel.py, tier1/mrlore/mrlore_control_center.py, tier1/mrlore/mrlore_scene_intake_runner.py, tier1/mrlore/mrlore_claim_extraction_runner.py, tier1/mrlore/mrlore_proposed_claim_shape_gate.py, tier1/mrlore/mrlore_proposed_claim_audit_summary.py, tier1/mrlore/mrlore_high_claim_scene_review_manifest.py, tier1/mrlore/mrlore_contradiction_candidate_grouper.py, tier1/mrlore/mrlore_contradiction_candidate_audit_summary.py, tier1/mrlore/mrlore_review_queue_builder.py, tier1/mrlore/mrlore_review_queue_noise_audit.py, tier1/mrlore/mrlore_review_queue_clean_view.py, tier1/mrlore/mrlore_review_rail_health_runner.py, tier1/mrlore/mrlore_manual_review_decision_schema.py, tier1/mrlore/mrlore_manual_review_decision_example_writer.py, tier1/mrlore/mrlore_entity_candidate_quality_gate.py, tier1/mrlore/mrlore_quality_aware_review_queue_builder.py, tier1/mrlore/mrlore_quality_aware_queue_summary.py, tier1/mrlore/mrlore_accepted_lore_packet_schema.py, tier1/mrlore/mrlore_preserve_entity_allowlist_registry_gate.py, tier1/mrlore/mrlore_temporal_claim_context_enrichment.py, tier1/mrlore/mrlore_temporal_collision_classification.py, tier1/mrlore/mrlore_temporal_aware_review_queue_builder.py, tier1/mrlore/mrlore_temporal_aware_queue_summary.py, tier1/mrlore/mrlore_temporal_aware_review_by_chapter_view.py, tier1/mrlore/mrlore_predicate_collision_policy_registry_gate.py, tier1/mrlore/mrlore_p3_sequential_entity_second_pass_quality_audit.py, tier1/mrlore/mrlore_coming_calendar_registry_gate.py, tier1/mrlore/mrlore_cosmic_year_context_enrichment.py, tier1/mrlore/mrlore_revision_breathing_map.py, tier1/mrlore/mrlore_revision_breathing_map_guidance_gate.py, tier1/mrlore/mrlore_major_event_internal_receipt_map.py, tier1/mrlore/evidence/proofs/phase_4/collect_delta.py, tier1/mrlore/archive/old_tools/mrlore_session.py, tier1/mrlore/archive/old_tools/lint_wiki.py, tier1/mrlore/archive/old_tools/write_changed_manifest.py, tier1/mrlore/archive/old_tools/propose_corrections.py, tier1/mrlore/archive/old_tools/continuity_audit.py, tier1/mrlore/archive/old_tools/mrlore_run_changed.py, tier1/mrlore/archive/old_tools/build_codex_candidates.py, tier1/mrlore/archive/old_tools/lint_codex_candidates.py, tier1/mrlore/archive/old_tools/promotion_eligibility_gate.py, tier1/mrlore/archive/old_tools/promote_candidate.py, tier1/mrlore/archive/old_tools/lint_relationship_schema.py, tier1/mrlore/archive/old_tools/populate_registry.py, tier1/mrlore/archive/old_tools/extract_member_of.py, tier1/mrlore/archive/old_tools/propose_rel_summaries.py, tier1/mrlore/archive/old_tools/propose_rel_source_stubs.py, tier1/mrlore/archive/old_tools/draft_rel_evidence_review.py, tier1/mrlore/archive/old_tools/stb_scanner.py, tier1/mrlore/archive/old_tools/build_registry.py, tier1/mrlore/archive/old_tools/stb_lint.py, tier1/mrlore/archive/old_tools/extract_candidates.py, tier1/mrlore/archive/old_tools/ollama_ingest_cockpit.py, tier1/mrlore/archive/old_tools/compile_entity_states.py, tier1/mrlore/archive/old_tools/chapter_ledger_extractor.py, tier1/mrlore/archive/old_tools/identity_signal_math.py, tier1/mrlore/archive/old_tools/provisional_identity_router.py, tier1/mrlore/archive/old_tools/identity_review_queue.py, tier1/mrlore/archive/old_tools/artifact_extractor.py, tier1/mrlore/archive/old_tools/pass2_math.py, tier1/mrlore/archive/old_tools/registry_builder.py, tier1/mrlore/archive/old_tools/identity_reviewer.py, tier1/mrlore/archive/old_tools/mrlore_query.py, tier1/mrlore/archive/old_tools/lint_scene_contract.py, tier1/mrlore/archive/old_tools/lint_entity_contract.py, tier1/mrlore/archive/old_tools/authority_score_calculator.py, tier1/mrlore/archive/old_tools/ingest_source_stub.py, tier1/mrlore/archive/old_tools/mrlore_rebuild_findings.py, tier1/mrlore/tools/mrlore_full_output_dump.py, tier1/engainos/engainos_server.py, tier1/engainos/launch_engine.py, tier1/engainos/engainos_control_center.py, tier1/engainos/gates/gate_ap_core_migration_authority.py, tier1/engainos/gates/gate_ap_core_behavior_parity.py, tier1/engainos/gates/gate_ap_core_signature_probe.py, tier1/engainos/gates/gate_ap_core_rule_activation.py, tier1/engainos/gates/gate_ap_engine_migration_authority.py, tier1/engainos/gates/gate_ap_engine_historical_probe.py, tier1/engainos/gates/gate_ap_engine_historical_source_map.py, tier1/engainos/gates/gate_ap_zw_engine_migration.py, tier1/engainos/gates/gate_ap_runtime_repair_readiness.py, tier1/engainos/gates/gate_ap_runtime_behavior_probe.py, tier1/engainos/gates/run_active_gates.py, tier1/engainos/gates/gate_ap_runtime_blocker_lane.py, tier1/engainos/gates/gate_server_runtime_preflight_lane.py, tier1/engainos/gates/gate_server_entrypoint_repair_lane.py, tier1/engainos/gates/gate_safe_server_wrapper_blueprint_lane.py, tier1/engainos/gates/gate_controlled_runtime_salvage_lane.py, tier1/engainos/gates/gate_vault_boot_side_effect_fence_lane.py, tier1/engainos/gates/gate_gamestate_draft_review_ready.py, tier1/engainos/gates/gate_ap_default_rules_registered.py, tier1/engainos/gates/gate_ap_zw_engine_timeline_fence.py, tier1/engainos/gates/gate_ap_zw_engine_canonical_claim.py, tier1/engainos/gates/gate_ap_runtime_relay_readiness.py, tier1/engainos/gates/gate_ap_runtime_relay_behavior.py, tier1/engainos/gates/gate_ap_runtime_relay_real_integration.py, tier1/engainos/gates/gate_governance_contract_board.py, tier1/engainos/gates/gate_gamestate_draft_review_contract.py, tier1/engainos/gates/gate_safe_server_wrapper_implementation_lane.py, tier1/engainos/gates/gate_safe_server_wrapper_behavior_lane.py, tier1/engainos/adapters/zonj_to_gamestate.py, tier1/engainos/core/no_godot_scene_proof.py, tier1/engainos/aproom/ap_engine.py, tier1/engainos/aproom/ap_quest_rules.py, tier1/engainos/aproom/ap_rule_loader.py, tier1/engainos/aproom/ap_world_rules.py, tier1/engainos/aproom/engine_summary.py, tier1/engainos/aproom/protocol_envelope.py, tier1/engainos/aproom/ap_zw_engine.py, tier1/engainos/aproom/ap_runtime.py, tier1/engainos/bridgeroom/godot_adapter.py, tier1/engainos/bridgeroom/scene_loader.py, tier1/engainos/bridgeroom/scene_server.py, tier1/engainos/bridgeroom/zon_to_game.py, tier1/engainos/bridgeroom/quest3d_integration.py, tier1/engainos/tools/vault_discovery.py, tier1/engainos/tools/chapter_discovery.py, tier1/engainos/tools/chapter_splitter/chapter_to_stage_packets.py, tier1/engainos/tools/chapter_splitter/promote_stage_draft.py, tier1/engainos/validators/runtime_stage_identity.py, tier1/engainos/validators/runtime_stage_manifest.py, tier1/paradox_machine/proofs/read_paradox_machine_gate_triad_result.py, tier1/paradox_machine/proofs/run_paradox_machine_gate_triad.py, tier1/paradox_machine/proofs/proof_008_spatiotemporal_gate_stub.py, tier1/paradox_machine/proofs/proof_007b_temporal_rejection.py, tier1/paradox_machine/proofs/proof_007_temporal_mvp.py, tier1/paradox_machine/proofs/export_gate_triad_result_zw.py, tier2/godotsim/scan_old_vault_paths.py, tier2/godotsim/scene_extractor.py, tier2/godotsim/trixel_composer.py, tier2/godotsim/vault_linker.py, tier2/godotsim/sim_runtime.py, tier2/godotsim/kernels/quest3d_mr.py, tier2/godotsim/kernels/navigation_mr.py, tier2/godotsim/kernels/perception_mr.py, tier2/godotsim/kernels/dialogue3d_mr.py, tier2/godotsim/kernels/inventory3d_mr.py, tier2/godotsim/adapters/navigation_adapter.py, tier2/godotsim/adapters/spatial3d_adapter.py, tier2/godotsim/adapters/combat3d_integration.py, tier2/godotsim/adapters/dialogue3d_integration.py, tier2/godotsim/adapters/inventory3d_integration.py, tier2/godotsim/gates/gate_piece3d_baseline.py, tier2/godotsim/gates/gate_floor_headless_parse_proof.py, tier2/godotsim/gates/gate_visible_floor_render_proof.py, tier2/godotsim/gates/gate_static_room_visible_proof.py, tier2/godotsim/gates/gate_player_body_visible_proof.py, tier2/godotsim/gates/gate_player_movement_proof.py, tier2/godotsim/gates/gate_player_movement_visible_observer_proof.py, tier2/godotsim/gates/gate_piece_recipe_pack_001_visible_proof.py, tier2/godotsim/gates/gate_piece_recipe_pack_002_door_proof.py, tier2/godotsim/gates/gate_ollama_diff_patcher_tests.py, tier2/godotsim/gates/gate_piece_recipe_pack_001.py, tier2/godotsim/gates/gate_trigger_zone_light_off_proof.py, tier2/godotsim/gates/gate_trigger_zone_multi_trigger_light_route_proof.py, tier2/engionality/engionality_control_center.py, tier2/engionality/controlroom/zon4d_kernel.py, tier2/engionality/controlroom/bootstrap.py, tier2/engionality/controlroom/performance_harness.py, tier2/topologist/classroom/run_topologist_classroom_probe.py, tier3/mettaext/engain_ingest.py, tier3/mettaext/narrative_to_game.py, tier3/mettaext/segmenter.py, tier3/mettaext/zwify_python.py, tier3/mettaext/zw_compiler.py, tier3/mettaext/pipeline_runner.py, tier3/mettaext/master_pipeline.py, tier3/mettaext/zw_world_rules_compiler.py, tier3/mettaext/run1time.py, tier3/mettaext/build_scene_index.py, tier3/mettaext/semantic_environment_extractor.py, tier3/mettaext/world_rules_loader.py, tier3/mettaext/stageroom_manifest.py, tier3/mettaext/passroom/pass2_event_builder.py, tier3/mettaext/passroom/pass4_zon_bridge.py, tier3/mettaext/passroom/pass5_game_bridge.py, tier3/mettaext/passroom/pass1_explicit.py, tier3/mettaext/passroom/pass2_enhanced.py, tier3/mettaext/passroom/pass3_merge.py, tier3/mettaext/passroom/pass1_spatial.py, tier3/mettaext/chapterroom/chapterroom_runner.py, tier3/mettaext/chapterroom/passA_chapter_intake.py, tier3/mettaext/chapterroom/passB_scene_boundary_provider.py, tier3/mettaext/chapterroom/passC_scene_packet_writer.py, tier3/mettaext/chapterroom/chapterroom_index_runner.py, tier3/mettaext/chapterroom/passB5_environment_detector.py, tier3/mettaext/vaultroom/vault_source_index.py, tools/ollama_diff_patcher.py, tools/gameproof/run_gameproof_001.py, tools/gameproof/run_gameproof_002.py, tools/gameproof/run_gameproof_003.py, tools/gameproof/run_gameproof_004.py, tools/gameproof/run_gameproof_005.py, tools/gameproof/run_gameproof_006.py, tools/passB_fix/passB_day_boundary_runner.py, tools/retired/ollama_patcher.py, scratch/gameproof_003/retired_cli_bridge/run_gameproof_003_cli.py, scratch/tier_relocation/trixel/legacy_payloads/harvest_legacy_trixel_payloads.py, gates/gate_engainos_bootstrap_preflight_v1.py, gates/gate_engainos_system_health_preflight_v1.py, gates/gate_boot_scene_authorization_request_v1.py, gates/gate_boot_scene_load_executor_request_v1.py, gates/gate_boot_shell_presentation_ready_v1.py, gates/gate_player_input_authorization_request_v1.py, gates/gate_player_input_listener_executor_request_v1.py, executors/boot_scene_load_executor_v1.py, executors/player_input_listener_executor_v1.py, interface/000_status.py, interface/010_show_protected_files.py, interface/020_show_ledger.py, interface/060_run_py_compile.py, interface/070_run_headless_gate.py, interface/080_stamp_result.py, interface/999_console.py, interface/030_create_task_packet.py, interface/040_show_next_command.py, interface/050_record_command_output.py, interface/090_recover_file_from_git.py, command_center/app.py

### Status Distribution
- **Likely_active:** 361
- **Stubbed:** 8
- **Orphaned:** 17
- **Dormant:** 14
- **Unresolved:** 0
- **Active (Runtime Confirmed):** 0

## 2. Candidate Subsystem Groups
### Adapters Subsystem
- **Confidence:** Low
- **Claim Type:** inferred
- **Member Count:** 10
- **Structurally Ambiguous:** Yes
- **Grouping Basis:** seed: directory_structure, refined_by: dependency_cohesion
- **Evidence:**
  - Files share directory structure: 'tier1/engainos/adapters, tier2/godotsim/adapters'
  - Internal cohesion: 0 internal dependency edges
  - Cross-group coupling: 6 external dependency edges
  - Weak internal cohesion relative to strong cross-group coupling; marked as structurally ambiguous
- **Member Files:**
  - `tier1/engainos/adapters/zonj_to_gamestate.py`
  - `tier2/godotsim/adapters/__init__.py`
  - `tier2/godotsim/adapters/behavior_adapter.py`
  - `tier2/godotsim/adapters/combat3d_adapter.py`
  - `tier2/godotsim/adapters/combat3d_integration.py`
  - `tier2/godotsim/adapters/dialogue3d_integration.py`
  - `tier2/godotsim/adapters/inventory3d_integration.py`
  - `tier2/godotsim/adapters/navigation_adapter.py`
  - `tier2/godotsim/adapters/perception_adapter.py`
  - `tier2/godotsim/adapters/spatial3d_adapter.py`
- **Inbound Interface Files (1):**
  - `tier2/godotsim/runtime_core.py`
- **Outbound Interface Files (5):**
  - `tier2/godotsim/__init__.py`
  - `tier2/godotsim/kernels/combat3d_mr.py`
  - `tier2/godotsim/slice_builders.py`
  - `tier2/godotsim/slice_types.py`
  - `tier2/godotsim/spatial3d.py`

### Aproom Subsystem
- **Confidence:** High
- **Claim Type:** inferred
- **Member Count:** 16
- **Structurally Ambiguous:** No
- **Grouping Basis:** seed: directory_structure, refined_by: dependency_cohesion
- **Evidence:**
  - Files share directory structure: 'tier1/engainos/aproom'
  - Internal cohesion: 4 internal dependency edges
  - Cross-group coupling: 4 external dependency edges
- **Member Files:**
  - `tier1/engainos/aproom/ap_complex_rules.py`
  - `tier1/engainos/aproom/ap_core.py`
  - `tier1/engainos/aproom/ap_engine.py`
  - `tier1/engainos/aproom/ap_quest_rules.py`
  - `tier1/engainos/aproom/ap_rule_evaluator.py`
  - `tier1/engainos/aproom/ap_rule_loader.py`
  - `tier1/engainos/aproom/ap_runtime.py`
  - `tier1/engainos/aproom/ap_world_rules.py`
  - `tier1/engainos/aproom/ap_zw_engine.py`
  - `tier1/engainos/aproom/authority_gate.py`
  - `tier1/engainos/aproom/authority_validator.py`
  - `tier1/engainos/aproom/canon.py`
  - `tier1/engainos/aproom/contract_validator.py`
  - `tier1/engainos/aproom/engine_summary.py`
  - `tier1/engainos/aproom/protocol_envelope.py`
  - `tier1/engainos/aproom/reality_mode.py`
- **Inbound Interface Files (4):**
  - `tier1/engainos/launch_engine.py`
  - `tier2/godotsim/http_handlers.py`
  - `tier2/godotsim/runtime_core.py`
  - `tier2/godotsim/runtime_gateway.py`
- **Outbound Interface Files (0):**

### Artifactroom Subsystem
- **Confidence:** High
- **Claim Type:** inferred
- **Member Count:** 3
- **Structurally Ambiguous:** No
- **Grouping Basis:** seed: directory_structure, refined_by: dependency_cohesion
- **Evidence:**
  - Files share directory structure: 'tier2/topologist/artifactroom'
  - Internal cohesion: 1 internal dependency edges
  - Cross-group coupling: 2 external dependency edges
- **Member Files:**
  - `tier2/topologist/artifactroom/__init__.py`
  - `tier2/topologist/artifactroom/passroom_signal_converter.py`
  - `tier2/topologist/artifactroom/topology_artifact.py`
- **Inbound Interface Files (2):**
  - `tier2/topologist/classroom/run_topologist_classroom_probe.py`
  - `tier2/topologist/reckoningroom/topology_validator.py`
- **Outbound Interface Files (0):**

### Bridgeroom Subsystem
- **Confidence:** High
- **Claim Type:** inferred
- **Member Count:** 12
- **Structurally Ambiguous:** No
- **Grouping Basis:** seed: directory_structure, refined_by: dependency_cohesion
- **Evidence:**
  - Files share directory structure: 'tier1/engainos/bridgeroom'
  - Internal cohesion: 9 internal dependency edges
  - Cross-group coupling: 4 external dependency edges
- **Member Files:**
  - `tier1/engainos/bridgeroom/godot_adapter.py`
  - `tier1/engainos/bridgeroom/mesh_intake.py`
  - `tier1/engainos/bridgeroom/mesh_manifest.py`
  - `tier1/engainos/bridgeroom/quest3d_integration.py`
  - `tier1/engainos/bridgeroom/scene_loader.py`
  - `tier1/engainos/bridgeroom/scene_server.py`
  - `tier1/engainos/bridgeroom/semantic_bridge.py`
  - `tier1/engainos/bridgeroom/spatial_reasoner.py`
  - `tier1/engainos/bridgeroom/spatial_skin_system.py`
  - `tier1/engainos/bridgeroom/zon_bridge.py`
  - `tier1/engainos/bridgeroom/zon_to_entities.py`
  - `tier1/engainos/bridgeroom/zon_to_game.py`
- **Inbound Interface Files (1):**
  - `tier1/engainos/launch_engine.py`
- **Outbound Interface Files (3):**
  - `tier2/godotsim/kernels/combat3d_mr.py`
  - `tier2/godotsim/kernels/quest3d_mr.py`
  - `tier3/mettaext/scene_identity.py`

### Builders Subsystem
- **Confidence:** Medium
- **Claim Type:** inferred
- **Member Count:** 1
- **Structurally Ambiguous:** Yes
- **Grouping Basis:** seed: directory_structure, refined_by: dependency_cohesion
- **Evidence:**
  - Files share directory structure: 'tier2/godotsim/builders'
  - Internal cohesion: 0 internal dependency edges
  - Cross-group coupling: 7 external dependency edges
  - Weak internal cohesion relative to strong cross-group coupling; marked as structurally ambiguous
- **Member Files:**
  - `tier2/godotsim/builders/godot_scene_piece_builder.py`
- **Inbound Interface Files (6):**
  - `tier2/godotsim/gates/gate_piece_recipe_pack_001_visible_proof.py`
  - `tier2/godotsim/gates/gate_piece_recipe_pack_002_door_proof.py`
  - `tier2/godotsim/gates/gate_player_body_visible_proof.py`
  - `tier2/godotsim/gates/gate_player_movement_proof.py`
  - `tier2/godotsim/gates/gate_player_movement_visible_observer_proof.py`
  - `tier2/godotsim/gates/gate_static_room_visible_proof.py`
- **Outbound Interface Files (1):**
  - `tier2/godotsim/kernels/piece3d_mr.py`

### Chapter_splitter Subsystem
- **Confidence:** High
- **Claim Type:** inferred
- **Member Count:** 2
- **Structurally Ambiguous:** No
- **Grouping Basis:** seed: directory_structure, refined_by: dependency_cohesion
- **Evidence:**
  - Files share directory structure: 'tier1/engainos/tools/chapter_splitter'
  - Internal cohesion: 0 internal dependency edges
  - Cross-group coupling: 0 external dependency edges
- **Member Files:**
  - `tier1/engainos/tools/chapter_splitter/chapter_to_stage_packets.py`
  - `tier1/engainos/tools/chapter_splitter/promote_stage_draft.py`
- **Inbound Interface Files (0):**
- **Outbound Interface Files (0):**

### Chapterroom Subsystem
- **Confidence:** High
- **Claim Type:** inferred
- **Member Count:** 8
- **Structurally Ambiguous:** No
- **Grouping Basis:** seed: directory_structure, refined_by: dependency_cohesion
- **Evidence:**
  - Files share directory structure: 'tier3/mettaext/chapterroom'
  - Internal cohesion: 7 internal dependency edges
  - Cross-group coupling: 1 external dependency edges
- **Member Files:**
  - `tier3/mettaext/chapterroom/__init__.py`
  - `tier3/mettaext/chapterroom/chapterroom_bridge.py`
  - `tier3/mettaext/chapterroom/chapterroom_index_runner.py`
  - `tier3/mettaext/chapterroom/chapterroom_runner.py`
  - `tier3/mettaext/chapterroom/passA_chapter_intake.py`
  - `tier3/mettaext/chapterroom/passB5_environment_detector.py`
  - `tier3/mettaext/chapterroom/passB_scene_boundary_provider.py`
  - `tier3/mettaext/chapterroom/passC_scene_packet_writer.py`
- **Inbound Interface Files (1):**
  - `tools/gameproof/run_gameproof_003.py`
- **Outbound Interface Files (0):**

### Classroom Subsystem
- **Confidence:** Medium
- **Claim Type:** inferred
- **Member Count:** 1
- **Structurally Ambiguous:** Yes
- **Grouping Basis:** seed: directory_structure, refined_by: dependency_cohesion
- **Evidence:**
  - Files share directory structure: 'tier2/topologist/classroom'
  - Internal cohesion: 0 internal dependency edges
  - Cross-group coupling: 2 external dependency edges
  - Weak internal cohesion relative to strong cross-group coupling; marked as structurally ambiguous
- **Member Files:**
  - `tier2/topologist/classroom/run_topologist_classroom_probe.py`
- **Inbound Interface Files (0):**
- **Outbound Interface Files (2):**
  - `tier2/topologist/artifactroom/topology_artifact.py`
  - `tier2/topologist/reckoningroom/topology_validator.py`

### Codecs Subsystem
- **Confidence:** High
- **Claim Type:** inferred
- **Member Count:** 1
- **Structurally Ambiguous:** No
- **Grouping Basis:** seed: directory_structure, refined_by: dependency_cohesion
- **Evidence:**
  - Files share directory structure: 'tier1/paradox_machine/codecs'
  - Internal cohesion: 0 internal dependency edges
  - Cross-group coupling: 0 external dependency edges
- **Member Files:**
  - `tier1/paradox_machine/codecs/__init__.py`
- **Inbound Interface Files (0):**
- **Outbound Interface Files (0):**

### Command_center Subsystem
- **Confidence:** High
- **Claim Type:** inferred
- **Member Count:** 1
- **Structurally Ambiguous:** No
- **Grouping Basis:** seed: directory_structure, refined_by: dependency_cohesion
- **Evidence:**
  - Files share directory structure: 'command_center'
  - Internal cohesion: 0 internal dependency edges
  - Cross-group coupling: 0 external dependency edges
- **Member Files:**
  - `command_center/app.py`
- **Inbound Interface Files (0):**
- **Outbound Interface Files (0):**

### Controlroom Subsystem
- **Confidence:** High
- **Claim Type:** inferred
- **Member Count:** 7
- **Structurally Ambiguous:** No
- **Grouping Basis:** seed: directory_structure, refined_by: dependency_cohesion
- **Evidence:**
  - Files share directory structure: 'tier2/engionality/controlroom'
  - Internal cohesion: 4 internal dependency edges
  - Cross-group coupling: 7 external dependency edges
- **Member Files:**
  - `tier2/engionality/controlroom/__init__.py`
  - `tier2/engionality/controlroom/bootstrap.py`
  - `tier2/engionality/controlroom/performance_harness.py`
  - `tier2/engionality/controlroom/runtime_loop.py`
  - `tier2/engionality/controlroom/task_system_merged.py`
  - `tier2/engionality/controlroom/task_types.py`
  - `tier2/engionality/controlroom/zon4d_kernel.py`
- **Inbound Interface Files (5):**
  - `tier2/engionality/showroom/animation_engine.py`
  - `tier2/engionality/showroom/audio_engine.py`
  - `tier2/engionality/showroom/dialogue_engine.py`
  - `tier2/engionality/showroom/performer_engine.py`
  - `tier2/engionality/showroom/scene_track.py`
- **Outbound Interface Files (2):**
  - `tier2/engionality/showroom/domain_views.py`
  - `tier2/engionality/showroom/performer_engine.py`

### Core Subsystem
- **Confidence:** High
- **Claim Type:** inferred
- **Member Count:** 10
- **Structurally Ambiguous:** No
- **Grouping Basis:** seed: directory_structure, refined_by: dependency_cohesion
- **Evidence:**
  - Files share directory structure: 'tier1/engainos/core'
  - Internal cohesion: 3 internal dependency edges
  - Cross-group coupling: 6 external dependency edges
- **Member Files:**
  - `tier1/engainos/core/__init__.py`
  - `tier1/engainos/core/agent_gateway.py`
  - `tier1/engainos/core/combat3d_mr.py`
  - `tier1/engainos/core/history_xeon.py`
  - `tier1/engainos/core/intent_shadow.py`
  - `tier1/engainos/core/no_godot_scene_proof.py`
  - `tier1/engainos/core/quest3d_mr.py`
  - `tier1/engainos/core/replay.py`
  - `tier1/engainos/core/trae_observer.py`
  - `tier1/engainos/core/zw_core.py`
- **Inbound Interface Files (4):**
  - `tier1/engainos/gates/gate_ap_default_rules_registered.py`
  - `tier1/engainos/gates/gate_ap_zw_engine_timeline_fence.py`
  - `tier2/godotsim/http_handlers.py`
  - `tier2/godotsim/runtime_gateway.py`
- **Outbound Interface Files (2):**
  - `tier2/godotsim/kernels/combat3d_mr.py`
  - `tier2/godotsim/kernels/quest3d_mr.py`

### Engainos Subsystem
- **Confidence:** Medium
- **Claim Type:** inferred
- **Member Count:** 5
- **Structurally Ambiguous:** No
- **Grouping Basis:** seed: directory_structure, refined_by: dependency_cohesion, refined_by: coordinator_outbound_concentration
- **Evidence:**
  - Files share directory structure: 'tier1/engainos'
  - Internal cohesion: 1 internal dependency edges
  - Cross-group coupling: 13 external dependency edges
  - Coordinator cohesion: explicitly named control center emits 9/13 outbound edges (69.2%); internal dependency edges are not required
- **Member Files:**
  - `tier1/engainos/__init__.py`
  - `tier1/engainos/engainos_control_center.py`
  - `tier1/engainos/engainos_server.py`
  - `tier1/engainos/launch_engine.py`
  - `tier1/engainos/runtime_client.py`
- **Inbound Interface Files (0):**
- **Outbound Interface Files (13):**
  - `tier1/engainos/aproom/ap_engine.py`
  - `tier1/engainos/aproom/ap_runtime.py`
  - `tier1/engainos/bridgeroom/godot_adapter.py`
  - `tier1/engainos/bridgeroom/scene_server.py`
  - `tier1/engainos/gates/gate_acceptance_rule.py`
  - `tier1/engainos/gates/gate_declared_truth_shape.py`
  - `tier1/engainos/gates/gate_governance_rejection_proof.py`
  - `tier1/engainos/gates/gate_no_asset_production.py`
  - `tier1/engainos/gates/gate_no_lane_theft_in_packet.py`
  - `tier1/engainos/gates/gate_no_presentation_authority.py`
  - `tier1/engainos/gates/gate_no_simulation_execution.py`
  - `tier1/engainos/gates/gate_packet_identity.py`
  - `tier1/engainos/gates/gate_validated_packets_shape.py`

### Engionality Subsystem
- **Confidence:** Medium
- **Claim Type:** inferred
- **Member Count:** 2
- **Structurally Ambiguous:** No
- **Grouping Basis:** seed: directory_structure, refined_by: dependency_cohesion, refined_by: coordinator_outbound_concentration
- **Evidence:**
  - Files share directory structure: 'tier2/engionality'
  - Internal cohesion: 0 internal dependency edges
  - Cross-group coupling: 6 external dependency edges
  - Coordinator cohesion: explicitly named control center emits 6/6 outbound edges (100.0%); internal dependency edges are not required
- **Member Files:**
  - `tier2/engionality/__init__.py`
  - `tier2/engionality/engionality_control_center.py`
- **Inbound Interface Files (0):**
- **Outbound Interface Files (6):**
  - `tier2/engionality/gates/gate_affect_state_valid.py`
  - `tier2/engionality/gates/gate_intensity_bounds.py`
  - `tier2/engionality/gates/gate_no_lane_theft_in_packet.py`
  - `tier2/engionality/gates/gate_relationship_deltas_valid_if_present.py`
  - `tier2/engionality/gates/gate_required_fields.py`
  - `tier2/engionality/gates/gate_scene_mood_valid_if_present.py`

### Executors Subsystem
- **Confidence:** High
- **Claim Type:** inferred
- **Member Count:** 2
- **Structurally Ambiguous:** No
- **Grouping Basis:** seed: directory_structure, refined_by: dependency_cohesion
- **Evidence:**
  - Files share directory structure: 'executors'
  - Internal cohesion: 0 internal dependency edges
  - Cross-group coupling: 0 external dependency edges
- **Member Files:**
  - `executors/boot_scene_load_executor_v1.py`
  - `executors/player_input_listener_executor_v1.py`
- **Inbound Interface Files (0):**
- **Outbound Interface Files (0):**

### Extraction Subsystem
- **Confidence:** Low
- **Claim Type:** inferred
- **Member Count:** 2
- **Structurally Ambiguous:** Yes
- **Grouping Basis:** seed: directory_structure, refined_by: dependency_cohesion
- **Evidence:**
  - Files share directory structure: 'tier1/paradox_machine/extraction'
  - Internal cohesion: 0 internal dependency edges
  - Cross-group coupling: 2 external dependency edges
  - Weak internal cohesion relative to strong cross-group coupling; marked as structurally ambiguous
- **Member Files:**
  - `tier1/paradox_machine/extraction/__init__.py`
  - `tier1/paradox_machine/extraction/naive_temporal_extractor.py`
- **Inbound Interface Files (1):**
  - `tier1/paradox_machine/proofs/proof_007_temporal_mvp.py`
- **Outbound Interface Files (1):**
  - `tier1/paradox_machine/schemas/temporal_artifact.py`

### Gameproof Subsystem
- **Confidence:** Low
- **Claim Type:** inferred
- **Member Count:** 6
- **Structurally Ambiguous:** Yes
- **Grouping Basis:** seed: directory_structure, refined_by: dependency_cohesion
- **Evidence:**
  - Files share directory structure: 'tools/gameproof'
  - Internal cohesion: 0 internal dependency edges
  - Cross-group coupling: 4 external dependency edges
  - Weak internal cohesion relative to strong cross-group coupling; marked as structurally ambiguous
- **Member Files:**
  - `tools/gameproof/run_gameproof_001.py`
  - `tools/gameproof/run_gameproof_002.py`
  - `tools/gameproof/run_gameproof_003.py`
  - `tools/gameproof/run_gameproof_004.py`
  - `tools/gameproof/run_gameproof_005.py`
  - `tools/gameproof/run_gameproof_006.py`
- **Inbound Interface Files (0):**
- **Outbound Interface Files (4):**
  - `tier2/topologist/gates/gate_accept_proposed_topology_artifact.py`
  - `tier3/mettaext/chapterroom/chapterroom_bridge.py`
  - `tier3/mettaext/passroom/pass1_spatial.py`
  - `tier3/mettaext/passroom/passroom_bridge.py`

### Gates Subsystem
- **Confidence:** High
- **Claim Type:** inferred
- **Member Count:** 81
- **Structurally Ambiguous:** No
- **Grouping Basis:** seed: directory_structure, refined_by: dependency_cohesion
- **Evidence:**
  - Files share directory structure: 'gates, tier1/engainos/gates, tier1/mrlore/gates, tier1/paradox_machine/gates, tier2/engionality/gates, tier2/godotsim/gates, tier2/topologist/gates'
  - Internal cohesion: 13 internal dependency edges
  - Cross-group coupling: 14 external dependency edges
- **Member Files:**
  - `gates/gate_boot_scene_authorization_request_v1.py`
  - `gates/gate_boot_scene_load_executor_request_v1.py`
  - `gates/gate_boot_shell_presentation_ready_v1.py`
  - `gates/gate_engainos_bootstrap_preflight_v1.py`
  - `gates/gate_engainos_system_health_preflight_v1.py`
  - `gates/gate_player_input_authorization_request_v1.py`
  - `gates/gate_player_input_listener_executor_request_v1.py`
  - `tier1/engainos/gates/__init__.py`
  - `tier1/engainos/gates/gate_acceptance_rule.py`
  - `tier1/engainos/gates/gate_ap_core_behavior_parity.py`
  - `tier1/engainos/gates/gate_ap_core_migration_authority.py`
  - `tier1/engainos/gates/gate_ap_core_rule_activation.py`
  - `tier1/engainos/gates/gate_ap_core_signature_probe.py`
  - `tier1/engainos/gates/gate_ap_default_rules_registered.py`
  - `tier1/engainos/gates/gate_ap_engine_historical_probe.py`
  - `tier1/engainos/gates/gate_ap_engine_historical_source_map.py`
  - `tier1/engainos/gates/gate_ap_engine_migration_authority.py`
  - `tier1/engainos/gates/gate_ap_runtime_behavior_probe.py`
  - `tier1/engainos/gates/gate_ap_runtime_blocker_lane.py`
  - `tier1/engainos/gates/gate_ap_runtime_relay_behavior.py`
  - `tier1/engainos/gates/gate_ap_runtime_relay_readiness.py`
  - `tier1/engainos/gates/gate_ap_runtime_relay_real_integration.py`
  - `tier1/engainos/gates/gate_ap_runtime_repair_readiness.py`
  - `tier1/engainos/gates/gate_ap_zw_engine_canonical_claim.py`
  - `tier1/engainos/gates/gate_ap_zw_engine_migration.py`
  - `tier1/engainos/gates/gate_ap_zw_engine_timeline_fence.py`
  - `tier1/engainos/gates/gate_controlled_runtime_salvage_lane.py`
  - `tier1/engainos/gates/gate_declared_truth_shape.py`
  - `tier1/engainos/gates/gate_gamestate_draft_review_contract.py`
  - `tier1/engainos/gates/gate_gamestate_draft_review_ready.py`
  - `tier1/engainos/gates/gate_governance_contract_board.py`
  - `tier1/engainos/gates/gate_governance_rejection_proof.py`
  - `tier1/engainos/gates/gate_no_asset_production.py`
  - `tier1/engainos/gates/gate_no_lane_theft_in_packet.py`
  - `tier1/engainos/gates/gate_no_presentation_authority.py`
  - `tier1/engainos/gates/gate_no_simulation_execution.py`
  - `tier1/engainos/gates/gate_packet_identity.py`
  - `tier1/engainos/gates/gate_safe_server_wrapper_behavior_lane.py`
  - `tier1/engainos/gates/gate_safe_server_wrapper_blueprint_lane.py`
  - `tier1/engainos/gates/gate_safe_server_wrapper_implementation_lane.py`
  - `tier1/engainos/gates/gate_server_entrypoint_repair_lane.py`
  - `tier1/engainos/gates/gate_server_runtime_preflight_lane.py`
  - `tier1/engainos/gates/gate_validated_packets_shape.py`
  - `tier1/engainos/gates/gate_vault_boot_side_effect_fence_lane.py`
  - `tier1/engainos/gates/run_active_gates.py`
  - `tier1/mrlore/gates/__init__.py`
  - `tier1/mrlore/gates/gate_claims_structure.py`
  - `tier1/mrlore/gates/gate_contradiction_stop_proof.py`
  - `tier1/mrlore/gates/gate_contradictions_valid_if_present.py`
  - `tier1/mrlore/gates/gate_enum_values_valid.py`
  - `tier1/mrlore/gates/gate_human_review_enforcement.py`
  - `tier1/mrlore/gates/gate_no_auto_resolve_attempt.py`
  - `tier1/mrlore/gates/gate_no_lane_theft_in_packet.py`
  - `tier1/mrlore/gates/gate_no_vault_path_dependency.py`
  - `tier1/mrlore/gates/gate_required_fields.py`
  - `tier1/paradox_machine/gates/__init__.py`
  - `tier1/paradox_machine/gates/temporal_gate.py`
  - `tier2/engionality/gates/gate_affect_packet_relationships.py`
  - `tier2/engionality/gates/gate_affect_state_valid.py`
  - `tier2/engionality/gates/gate_hard_rejects.py`
  - `tier2/engionality/gates/gate_intensity_bounds.py`
  - `tier2/engionality/gates/gate_no_lane_theft_in_packet.py`
  - `tier2/engionality/gates/gate_no_legacy_imports.py`
  - `tier2/engionality/gates/gate_relationship_deltas_valid_if_present.py`
  - `tier2/engionality/gates/gate_required_fields.py`
  - `tier2/engionality/gates/gate_scene_mood_valid_if_present.py`
  - `tier2/godotsim/gates/gate_floor_headless_parse_proof.py`
  - `tier2/godotsim/gates/gate_ollama_diff_patcher_tests.py`
  - `tier2/godotsim/gates/gate_piece3d_baseline.py`
  - `tier2/godotsim/gates/gate_piece_recipe_pack_001.py`
  - `tier2/godotsim/gates/gate_piece_recipe_pack_001_visible_proof.py`
  - `tier2/godotsim/gates/gate_piece_recipe_pack_002_door_proof.py`
  - `tier2/godotsim/gates/gate_player_body_visible_proof.py`
  - `tier2/godotsim/gates/gate_player_movement_proof.py`
  - `tier2/godotsim/gates/gate_player_movement_visible_observer_proof.py`
  - `tier2/godotsim/gates/gate_static_room_visible_proof.py`
  - `tier2/godotsim/gates/gate_trigger_zone_light_off_proof.py`
  - `tier2/godotsim/gates/gate_trigger_zone_multi_trigger_light_route_proof.py`
  - `tier2/godotsim/gates/gate_visible_floor_render_proof.py`
  - `tier2/topologist/gates/__init__.py`
  - `tier2/topologist/gates/gate_accept_proposed_topology_artifact.py`
- **Inbound Interface Files (7):**
  - `tier1/engainos/engainos_control_center.py`
  - `tier1/engainos/tests/test_gamestate_authority.py`
  - `tier1/mrlore/mrlore_control_center.py`
  - `tier1/paradox_machine/proofs/proof_007_temporal_mvp.py`
  - `tier1/paradox_machine/proofs/proof_007b_temporal_rejection.py`
  - `tier2/engionality/engionality_control_center.py`
  - `tools/gameproof/run_gameproof_006.py`
- **Outbound Interface Files (7):**
  - `tier1/engainos/core/__init__.py`
  - `tier1/engainos/relays/ap_runtime_relay.py`
  - `tier1/paradox_machine/reasoning/temporal_validator.py`
  - `tier1/paradox_machine/schemas/temporal_artifact.py`
  - `tier2/godotsim/builders/godot_scene_piece_builder.py`
  - `tier2/godotsim/kernels/piece3d_mr.py`
  - `tools/ollama_diff_patcher.py`

### Godotsim Subsystem
- **Confidence:** High
- **Claim Type:** inferred
- **Member Count:** 24
- **Structurally Ambiguous:** No
- **Grouping Basis:** seed: directory_structure, refined_by: dependency_cohesion
- **Evidence:**
  - Files share directory structure: 'tier2/godotsim'
  - Internal cohesion: 27 internal dependency edges
  - Cross-group coupling: 22 external dependency edges
- **Member Files:**
  - `tier2/godotsim/__init__.py`
  - `tier2/godotsim/blender_mcp_bridge.py`
  - `tier2/godotsim/bridge_integration.py`
  - `tier2/godotsim/combat3d_mr.py`
  - `tier2/godotsim/command_dispatcher.py`
  - `tier2/godotsim/embodiment_contract_builder.py`
  - `tier2/godotsim/engain_hooks.py`
  - `tier2/godotsim/environment_manager.py`
  - `tier2/godotsim/http_handlers.py`
  - `tier2/godotsim/protocol_envelope.py`
  - `tier2/godotsim/runtime_core.py`
  - `tier2/godotsim/runtime_gateway.py`
  - `tier2/godotsim/scan_old_vault_paths.py`
  - `tier2/godotsim/scene_extractor.py`
  - `tier2/godotsim/scene_manager.py`
  - `tier2/godotsim/semantic_bridge.py`
  - `tier2/godotsim/sim_runtime.py`
  - `tier2/godotsim/slice_builders.py`
  - `tier2/godotsim/slice_types.py`
  - `tier2/godotsim/spatial3d.py`
  - `tier2/godotsim/spatial_skin_system.py`
  - `tier2/godotsim/trixel_composer.py`
  - `tier2/godotsim/vault_linker.py`
  - `tier2/godotsim/vault_manager.py`
- **Inbound Interface Files (7):**
  - `tier2/godotsim/adapters/behavior_adapter.py`
  - `tier2/godotsim/adapters/dialogue3d_integration.py`
  - `tier2/godotsim/adapters/inventory3d_integration.py`
  - `tier2/godotsim/adapters/navigation_adapter.py`
  - `tier2/godotsim/adapters/perception_adapter.py`
  - `tier2/godotsim/adapters/spatial3d_adapter.py`
  - `tier2/godotsim/test_slice_builders.py`
- **Outbound Interface Files (15):**
  - `tier1/engainos/aproom/ap_complex_rules.py`
  - `tier1/engainos/aproom/authority_gate.py`
  - `tier1/engainos/aproom/canon.py`
  - `tier1/engainos/aproom/reality_mode.py`
  - `tier1/engainos/core/intent_shadow.py`
  - `tier2/godotsim/adapters/behavior_adapter.py`
  - `tier2/godotsim/adapters/combat3d_adapter.py`
  - `tier2/godotsim/adapters/dialogue3d_integration.py`
  - `tier2/godotsim/adapters/inventory3d_integration.py`
  - `tier2/godotsim/adapters/perception_adapter.py`
  - `tier2/godotsim/adapters/spatial3d_adapter.py`
  - `tier2/godotsim/kernels/behavior3d_mr.py`
  - `tier2/godotsim/kernels/perception_mr.py`
  - `tier2/godotsim/kernels/spatial3d_mr.py`
  - `tier3/mettaext/scene_identity.py`

### Interface Subsystem
- **Confidence:** High
- **Claim Type:** inferred
- **Member Count:** 12
- **Structurally Ambiguous:** No
- **Grouping Basis:** seed: directory_structure, refined_by: dependency_cohesion
- **Evidence:**
  - Files share directory structure: 'interface'
  - Internal cohesion: 10 internal dependency edges
  - Cross-group coupling: 0 external dependency edges
- **Member Files:**
  - `interface/000_status.py`
  - `interface/010_show_protected_files.py`
  - `interface/020_show_ledger.py`
  - `interface/030_create_task_packet.py`
  - `interface/040_show_next_command.py`
  - `interface/050_record_command_output.py`
  - `interface/060_run_py_compile.py`
  - `interface/070_run_headless_gate.py`
  - `interface/080_stamp_result.py`
  - `interface/090_recover_file_from_git.py`
  - `interface/999_console.py`
  - `interface/interface_common.py`
- **Inbound Interface Files (0):**
- **Outbound Interface Files (0):**

### Kernels Subsystem
- **Confidence:** Low
- **Claim Type:** inferred
- **Member Count:** 10
- **Structurally Ambiguous:** Yes
- **Grouping Basis:** seed: directory_structure, refined_by: dependency_cohesion
- **Evidence:**
  - Files share directory structure: 'tier2/godotsim/kernels'
  - Internal cohesion: 0 internal dependency edges
  - Cross-group coupling: 19 external dependency edges
  - Weak internal cohesion relative to strong cross-group coupling; marked as structurally ambiguous
- **Member Files:**
  - `tier2/godotsim/kernels/__init__.py`
  - `tier2/godotsim/kernels/behavior3d_mr.py`
  - `tier2/godotsim/kernels/combat3d_mr.py`
  - `tier2/godotsim/kernels/dialogue3d_mr.py`
  - `tier2/godotsim/kernels/inventory3d_mr.py`
  - `tier2/godotsim/kernels/navigation_mr.py`
  - `tier2/godotsim/kernels/perception_mr.py`
  - `tier2/godotsim/kernels/piece3d_mr.py`
  - `tier2/godotsim/kernels/quest3d_mr.py`
  - `tier2/godotsim/kernels/spatial3d_mr.py`
- **Inbound Interface Files (19):**
  - `tier1/engainos/bridgeroom/quest3d_integration.py`
  - `tier1/engainos/bridgeroom/zon_bridge.py`
  - `tier1/engainos/core/combat3d_mr.py`
  - `tier1/engainos/core/quest3d_mr.py`
  - `tier1/engainos/core/replay.py`
  - `tier2/godotsim/adapters/combat3d_adapter.py`
  - `tier2/godotsim/adapters/combat3d_integration.py`
  - `tier2/godotsim/builders/godot_scene_piece_builder.py`
  - `tier2/godotsim/gates/gate_floor_headless_parse_proof.py`
  - `tier2/godotsim/gates/gate_piece3d_baseline.py`
  - `tier2/godotsim/gates/gate_piece_recipe_pack_001.py`
  - `tier2/godotsim/gates/gate_piece_recipe_pack_001_visible_proof.py`
  - `tier2/godotsim/gates/gate_piece_recipe_pack_002_door_proof.py`
  - `tier2/godotsim/gates/gate_player_body_visible_proof.py`
  - `tier2/godotsim/gates/gate_player_movement_proof.py`
  - `tier2/godotsim/gates/gate_player_movement_visible_observer_proof.py`
  - `tier2/godotsim/gates/gate_static_room_visible_proof.py`
  - `tier2/godotsim/gates/gate_visible_floor_render_proof.py`
  - `tier2/godotsim/runtime_core.py`
- **Outbound Interface Files (0):**

### Legacy_payloads Subsystem
- **Confidence:** High
- **Claim Type:** inferred
- **Member Count:** 1
- **Structurally Ambiguous:** No
- **Grouping Basis:** seed: directory_structure, refined_by: dependency_cohesion
- **Evidence:**
  - Files share directory structure: 'scratch/tier_relocation/trixel/legacy_payloads'
  - Internal cohesion: 0 internal dependency edges
  - Cross-group coupling: 0 external dependency edges
- **Member Files:**
  - `scratch/tier_relocation/trixel/legacy_payloads/harvest_legacy_trixel_payloads.py`
- **Inbound Interface Files (0):**
- **Outbound Interface Files (0):**

### Mettaext Subsystem
- **Confidence:** Low
- **Claim Type:** inferred
- **Member Count:** 15
- **Structurally Ambiguous:** Yes
- **Grouping Basis:** seed: directory_structure, refined_by: dependency_cohesion
- **Evidence:**
  - Files share directory structure: 'tier3/mettaext'
  - Internal cohesion: 0 internal dependency edges
  - Cross-group coupling: 7 external dependency edges
  - Weak internal cohesion relative to strong cross-group coupling; marked as structurally ambiguous
- **Member Files:**
  - `tier3/mettaext/__init__.py`
  - `tier3/mettaext/build_scene_index.py`
  - `tier3/mettaext/engain_ingest.py`
  - `tier3/mettaext/master_pipeline.py`
  - `tier3/mettaext/narrative_to_game.py`
  - `tier3/mettaext/pipeline_runner.py`
  - `tier3/mettaext/run1time.py`
  - `tier3/mettaext/scene_identity.py`
  - `tier3/mettaext/segmenter.py`
  - `tier3/mettaext/semantic_environment_extractor.py`
  - `tier3/mettaext/stageroom_manifest.py`
  - `tier3/mettaext/world_rules_loader.py`
  - `tier3/mettaext/zw_compiler.py`
  - `tier3/mettaext/zw_world_rules_compiler.py`
  - `tier3/mettaext/zwify_python.py`
- **Inbound Interface Files (7):**
  - `tier1/engainos/bridgeroom/scene_loader.py`
  - `tier2/godotsim/http_handlers.py`
  - `tier2/godotsim/scene_manager.py`
  - `tier2/godotsim/sim_runtime.py`
  - `tier3/mettaext/passroom/pass2_entity_filter.py`
  - `tier3/mettaext/passroom/pass4_zon_bridge.py`
  - `tier3/mettaext/passroom/pass5_game_bridge.py`
- **Outbound Interface Files (0):**

### Mrlore Subsystem
- **Confidence:** Medium
- **Claim Type:** inferred
- **Member Count:** 32
- **Structurally Ambiguous:** No
- **Grouping Basis:** seed: directory_structure, refined_by: dependency_cohesion, refined_by: coordinator_outbound_concentration
- **Evidence:**
  - Files share directory structure: 'tier1/mrlore'
  - Internal cohesion: 20 internal dependency edges
  - Cross-group coupling: 37 external dependency edges
  - Coordinator cohesion: explicitly named control center emits 8/8 outbound edges (100.0%); internal dependency edges are not required
- **Member Files:**
  - `tier1/mrlore/__init__.py`
  - `tier1/mrlore/mrlore_accepted_lore_packet_schema.py`
  - `tier1/mrlore/mrlore_claim_extraction_runner.py`
  - `tier1/mrlore/mrlore_coming_calendar_registry_gate.py`
  - `tier1/mrlore/mrlore_contradiction_candidate_audit_summary.py`
  - `tier1/mrlore/mrlore_contradiction_candidate_grouper.py`
  - `tier1/mrlore/mrlore_control_center.py`
  - `tier1/mrlore/mrlore_cosmic_year_context_enrichment.py`
  - `tier1/mrlore/mrlore_entity_candidate_quality_gate.py`
  - `tier1/mrlore/mrlore_high_claim_scene_review_manifest.py`
  - `tier1/mrlore/mrlore_major_event_internal_receipt_map.py`
  - `tier1/mrlore/mrlore_manual_review_decision_example_writer.py`
  - `tier1/mrlore/mrlore_manual_review_decision_schema.py`
  - `tier1/mrlore/mrlore_p3_sequential_entity_second_pass_quality_audit.py`
  - `tier1/mrlore/mrlore_predicate_collision_policy_registry_gate.py`
  - `tier1/mrlore/mrlore_preserve_entity_allowlist_registry_gate.py`
  - `tier1/mrlore/mrlore_proposed_claim_audit_summary.py`
  - `tier1/mrlore/mrlore_proposed_claim_shape_gate.py`
  - `tier1/mrlore/mrlore_quality_aware_queue_summary.py`
  - `tier1/mrlore/mrlore_quality_aware_review_queue_builder.py`
  - `tier1/mrlore/mrlore_review_queue_builder.py`
  - `tier1/mrlore/mrlore_review_queue_clean_view.py`
  - `tier1/mrlore/mrlore_review_queue_noise_audit.py`
  - `tier1/mrlore/mrlore_review_rail_health_runner.py`
  - `tier1/mrlore/mrlore_revision_breathing_map.py`
  - `tier1/mrlore/mrlore_revision_breathing_map_guidance_gate.py`
  - `tier1/mrlore/mrlore_scene_intake_runner.py`
  - `tier1/mrlore/mrlore_temporal_aware_queue_summary.py`
  - `tier1/mrlore/mrlore_temporal_aware_review_by_chapter_view.py`
  - `tier1/mrlore/mrlore_temporal_aware_review_queue_builder.py`
  - `tier1/mrlore/mrlore_temporal_claim_context_enrichment.py`
  - `tier1/mrlore/mrlore_temporal_collision_classification.py`
- **Inbound Interface Files (29):**
  - `tier1/mrlore/tests/test_accepted_lore_packet_schema.py`
  - `tier1/mrlore/tests/test_claim_extraction_runner.py`
  - `tier1/mrlore/tests/test_coming_calendar_registry_gate.py`
  - `tier1/mrlore/tests/test_contradiction_candidate_audit_summary.py`
  - `tier1/mrlore/tests/test_contradiction_candidate_grouper.py`
  - `tier1/mrlore/tests/test_cosmic_year_context_enrichment.py`
  - `tier1/mrlore/tests/test_entity_candidate_quality_gate.py`
  - `tier1/mrlore/tests/test_high_claim_scene_review_manifest.py`
  - `tier1/mrlore/tests/test_major_event_internal_receipt_map.py`
  - `tier1/mrlore/tests/test_manual_review_decision_example_writer.py`
  - `tier1/mrlore/tests/test_manual_review_decision_schema.py`
  - `tier1/mrlore/tests/test_p3_sequential_entity_second_pass_quality_audit.py`
  - `tier1/mrlore/tests/test_predicate_collision_policy_registry_gate.py`
  - `tier1/mrlore/tests/test_preserve_entity_allowlist_registry_gate.py`
  - `tier1/mrlore/tests/test_proposed_claim_audit_summary.py`
  - `tier1/mrlore/tests/test_proposed_claim_shape_gate.py`
  - `tier1/mrlore/tests/test_quality_aware_queue_summary.py`
  - `tier1/mrlore/tests/test_quality_aware_review_queue_builder.py`
  - `tier1/mrlore/tests/test_review_queue_builder.py`
  - `tier1/mrlore/tests/test_review_queue_clean_view.py`
  - `tier1/mrlore/tests/test_review_queue_noise_audit.py`
  - `tier1/mrlore/tests/test_review_rail_health_runner.py`
  - `tier1/mrlore/tests/test_revision_breathing_map.py`
  - `tier1/mrlore/tests/test_revision_breathing_map_guidance_gate.py`
  - `tier1/mrlore/tests/test_temporal_aware_queue_summary.py`
  - `tier1/mrlore/tests/test_temporal_aware_review_by_chapter_view.py`
  - `tier1/mrlore/tests/test_temporal_aware_review_queue_builder.py`
  - `tier1/mrlore/tests/test_temporal_claim_context_enrichment.py`
  - `tier1/mrlore/tests/test_temporal_collision_classification.py`
- **Outbound Interface Files (8):**
  - `tier1/mrlore/gates/gate_claims_structure.py`
  - `tier1/mrlore/gates/gate_contradiction_stop_proof.py`
  - `tier1/mrlore/gates/gate_contradictions_valid_if_present.py`
  - `tier1/mrlore/gates/gate_enum_values_valid.py`
  - `tier1/mrlore/gates/gate_no_auto_resolve_attempt.py`
  - `tier1/mrlore/gates/gate_no_lane_theft_in_packet.py`
  - `tier1/mrlore/gates/gate_no_vault_path_dependency.py`
  - `tier1/mrlore/gates/gate_required_fields.py`

### Old_tools Subsystem
- **Confidence:** High
- **Claim Type:** inferred
- **Member Count:** 36
- **Structurally Ambiguous:** No
- **Grouping Basis:** seed: directory_structure, refined_by: dependency_cohesion
- **Evidence:**
  - Files share directory structure: 'tier1/mrlore/archive/old_tools'
  - Internal cohesion: 2 internal dependency edges
  - Cross-group coupling: 0 external dependency edges
- **Member Files:**
  - `tier1/mrlore/archive/old_tools/artifact_extractor.py`
  - `tier1/mrlore/archive/old_tools/authority_score_calculator.py`
  - `tier1/mrlore/archive/old_tools/build_codex_candidates.py`
  - `tier1/mrlore/archive/old_tools/build_registry.py`
  - `tier1/mrlore/archive/old_tools/chapter_ledger_extractor.py`
  - `tier1/mrlore/archive/old_tools/compile_entity_states.py`
  - `tier1/mrlore/archive/old_tools/continuity_audit.py`
  - `tier1/mrlore/archive/old_tools/draft_rel_evidence_review.py`
  - `tier1/mrlore/archive/old_tools/extract_candidates.py`
  - `tier1/mrlore/archive/old_tools/extract_member_of.py`
  - `tier1/mrlore/archive/old_tools/identity_review_queue.py`
  - `tier1/mrlore/archive/old_tools/identity_reviewer.py`
  - `tier1/mrlore/archive/old_tools/identity_signal_math.py`
  - `tier1/mrlore/archive/old_tools/ingest_source_stub.py`
  - `tier1/mrlore/archive/old_tools/lint_codex_candidates.py`
  - `tier1/mrlore/archive/old_tools/lint_entity_contract.py`
  - `tier1/mrlore/archive/old_tools/lint_relationship_schema.py`
  - `tier1/mrlore/archive/old_tools/lint_scene_contract.py`
  - `tier1/mrlore/archive/old_tools/lint_wiki.py`
  - `tier1/mrlore/archive/old_tools/mrlore_query.py`
  - `tier1/mrlore/archive/old_tools/mrlore_rebuild_findings.py`
  - `tier1/mrlore/archive/old_tools/mrlore_run_changed.py`
  - `tier1/mrlore/archive/old_tools/mrlore_session.py`
  - `tier1/mrlore/archive/old_tools/ollama_ingest_cockpit.py`
  - `tier1/mrlore/archive/old_tools/pass2_math.py`
  - `tier1/mrlore/archive/old_tools/populate_registry.py`
  - `tier1/mrlore/archive/old_tools/promote_candidate.py`
  - `tier1/mrlore/archive/old_tools/promotion_eligibility_gate.py`
  - `tier1/mrlore/archive/old_tools/propose_corrections.py`
  - `tier1/mrlore/archive/old_tools/propose_rel_source_stubs.py`
  - `tier1/mrlore/archive/old_tools/propose_rel_summaries.py`
  - `tier1/mrlore/archive/old_tools/provisional_identity_router.py`
  - `tier1/mrlore/archive/old_tools/registry_builder.py`
  - `tier1/mrlore/archive/old_tools/stb_lint.py`
  - `tier1/mrlore/archive/old_tools/stb_scanner.py`
  - `tier1/mrlore/archive/old_tools/write_changed_manifest.py`
- **Inbound Interface Files (0):**
- **Outbound Interface Files (0):**

### Paradoxroom Subsystem
- **Confidence:** High
- **Claim Type:** inferred
- **Member Count:** 2
- **Structurally Ambiguous:** No
- **Grouping Basis:** seed: directory_structure, refined_by: dependency_cohesion
- **Evidence:**
  - Files share directory structure: 'tier1/paradox_machine/paradoxroom'
  - Internal cohesion: 0 internal dependency edges
  - Cross-group coupling: 0 external dependency edges
- **Member Files:**
  - `tier1/paradox_machine/paradoxroom/__init__.py`
  - `tier1/paradox_machine/paradoxroom/potential_temporal_state_set.py`
- **Inbound Interface Files (0):**
- **Outbound Interface Files (0):**

### Passb_fix Subsystem
- **Confidence:** High
- **Claim Type:** inferred
- **Member Count:** 1
- **Structurally Ambiguous:** No
- **Grouping Basis:** seed: directory_structure, refined_by: dependency_cohesion
- **Evidence:**
  - Files share directory structure: 'tools/passB_fix'
  - Internal cohesion: 0 internal dependency edges
  - Cross-group coupling: 0 external dependency edges
- **Member Files:**
  - `tools/passB_fix/passB_day_boundary_runner.py`
- **Inbound Interface Files (0):**
- **Outbound Interface Files (0):**

### Passroom Subsystem
- **Confidence:** High
- **Claim Type:** inferred
- **Member Count:** 10
- **Structurally Ambiguous:** No
- **Grouping Basis:** seed: directory_structure, refined_by: dependency_cohesion
- **Evidence:**
  - Files share directory structure: 'tier3/mettaext/passroom'
  - Internal cohesion: 3 internal dependency edges
  - Cross-group coupling: 4 external dependency edges
- **Member Files:**
  - `tier3/mettaext/passroom/__init__.py`
  - `tier3/mettaext/passroom/pass1_explicit.py`
  - `tier3/mettaext/passroom/pass1_spatial.py`
  - `tier3/mettaext/passroom/pass2_enhanced.py`
  - `tier3/mettaext/passroom/pass2_entity_filter.py`
  - `tier3/mettaext/passroom/pass2_event_builder.py`
  - `tier3/mettaext/passroom/pass3_merge.py`
  - `tier3/mettaext/passroom/pass4_zon_bridge.py`
  - `tier3/mettaext/passroom/pass5_game_bridge.py`
  - `tier3/mettaext/passroom/passroom_bridge.py`
- **Inbound Interface Files (2):**
  - `tools/gameproof/run_gameproof_004.py`
  - `tools/gameproof/run_gameproof_005.py`
- **Outbound Interface Files (2):**
  - `tier3/mettaext/semantic_environment_extractor.py`
  - `tier3/mettaext/world_rules_loader.py`

### Phase_4 Subsystem
- **Confidence:** High
- **Claim Type:** inferred
- **Member Count:** 2
- **Structurally Ambiguous:** No
- **Grouping Basis:** seed: directory_structure, refined_by: dependency_cohesion
- **Evidence:**
  - Files share directory structure: 'tier1/mrlore/evidence/proofs/phase_4'
  - Internal cohesion: 0 internal dependency edges
  - Cross-group coupling: 0 external dependency edges
- **Member Files:**
  - `tier1/mrlore/evidence/proofs/phase_4/coco_flow.py`
  - `tier1/mrlore/evidence/proofs/phase_4/collect_delta.py`
- **Inbound Interface Files (0):**
- **Outbound Interface Files (0):**

### Proofs Subsystem
- **Confidence:** Low
- **Claim Type:** inferred
- **Member Count:** 7
- **Structurally Ambiguous:** Yes
- **Grouping Basis:** seed: directory_structure, refined_by: dependency_cohesion
- **Evidence:**
  - Files share directory structure: 'tier1/paradox_machine/proofs'
  - Internal cohesion: 0 internal dependency edges
  - Cross-group coupling: 5 external dependency edges
  - Weak internal cohesion relative to strong cross-group coupling; marked as structurally ambiguous
- **Member Files:**
  - `tier1/paradox_machine/proofs/__init__.py`
  - `tier1/paradox_machine/proofs/export_gate_triad_result_zw.py`
  - `tier1/paradox_machine/proofs/proof_007_temporal_mvp.py`
  - `tier1/paradox_machine/proofs/proof_007b_temporal_rejection.py`
  - `tier1/paradox_machine/proofs/proof_008_spatiotemporal_gate_stub.py`
  - `tier1/paradox_machine/proofs/read_paradox_machine_gate_triad_result.py`
  - `tier1/paradox_machine/proofs/run_paradox_machine_gate_triad.py`
- **Inbound Interface Files (0):**
- **Outbound Interface Files (5):**
  - `tier1/paradox_machine/extraction/naive_temporal_extractor.py`
  - `tier1/paradox_machine/gates/temporal_gate.py`
  - `tier1/paradox_machine/reasoning/temporal_validator.py`
  - `tier1/paradox_machine/schemas/temporal_artifact.py`
  - `tier1/paradox_machine/zwcodecs/json_to_zw.py`

### Reasoning Subsystem
- **Confidence:** Medium
- **Claim Type:** inferred
- **Member Count:** 4
- **Structurally Ambiguous:** Yes
- **Grouping Basis:** seed: directory_structure, refined_by: dependency_cohesion
- **Evidence:**
  - Files share directory structure: 'tier1/paradox_machine/reasoning'
  - Internal cohesion: 1 internal dependency edges
  - Cross-group coupling: 5 external dependency edges
  - Weak internal cohesion relative to strong cross-group coupling; marked as structurally ambiguous
- **Member Files:**
  - `tier1/paradox_machine/reasoning/__init__.py`
  - `tier1/paradox_machine/reasoning/allen_relations.py`
  - `tier1/paradox_machine/reasoning/stn.py`
  - `tier1/paradox_machine/reasoning/temporal_validator.py`
- **Inbound Interface Files (4):**
  - `scratch/test_temporal_contradiction.py`
  - `tier1/paradox_machine/gates/temporal_gate.py`
  - `tier1/paradox_machine/proofs/proof_007_temporal_mvp.py`
  - `tier1/paradox_machine/proofs/proof_007b_temporal_rejection.py`
- **Outbound Interface Files (1):**
  - `tier1/paradox_machine/schemas/temporal_artifact.py`

### Reckoningroom Subsystem
- **Confidence:** Low
- **Claim Type:** inferred
- **Member Count:** 2
- **Structurally Ambiguous:** Yes
- **Grouping Basis:** seed: directory_structure, refined_by: dependency_cohesion
- **Evidence:**
  - Files share directory structure: 'tier2/topologist/reckoningroom'
  - Internal cohesion: 0 internal dependency edges
  - Cross-group coupling: 2 external dependency edges
  - Weak internal cohesion relative to strong cross-group coupling; marked as structurally ambiguous
- **Member Files:**
  - `tier2/topologist/reckoningroom/__init__.py`
  - `tier2/topologist/reckoningroom/topology_validator.py`
- **Inbound Interface Files (1):**
  - `tier2/topologist/classroom/run_topologist_classroom_probe.py`
- **Outbound Interface Files (1):**
  - `tier2/topologist/artifactroom/topology_artifact.py`

### Relays Subsystem
- **Confidence:** Low
- **Claim Type:** inferred
- **Member Count:** 2
- **Structurally Ambiguous:** Yes
- **Grouping Basis:** seed: directory_structure, refined_by: dependency_cohesion
- **Evidence:**
  - Files share directory structure: 'tier1/engainos/relays'
  - Internal cohesion: 0 internal dependency edges
  - Cross-group coupling: 2 external dependency edges
  - Weak internal cohesion relative to strong cross-group coupling; marked as structurally ambiguous
- **Member Files:**
  - `tier1/engainos/relays/__init__.py`
  - `tier1/engainos/relays/ap_runtime_relay.py`
- **Inbound Interface Files (2):**
  - `tier1/engainos/gates/gate_ap_runtime_relay_behavior.py`
  - `tier1/engainos/gates/gate_ap_runtime_relay_real_integration.py`
- **Outbound Interface Files (0):**

### Retired Subsystem
- **Confidence:** High
- **Claim Type:** inferred
- **Member Count:** 1
- **Structurally Ambiguous:** No
- **Grouping Basis:** seed: directory_structure, refined_by: dependency_cohesion
- **Evidence:**
  - Files share directory structure: 'tools/retired'
  - Internal cohesion: 0 internal dependency edges
  - Cross-group coupling: 0 external dependency edges
- **Member Files:**
  - `tools/retired/ollama_patcher.py`
- **Inbound Interface Files (0):**
- **Outbound Interface Files (0):**

### Retired_cli_bridge Subsystem
- **Confidence:** High
- **Claim Type:** inferred
- **Member Count:** 1
- **Structurally Ambiguous:** No
- **Grouping Basis:** seed: directory_structure, refined_by: dependency_cohesion
- **Evidence:**
  - Files share directory structure: 'scratch/gameproof_003/retired_cli_bridge'
  - Internal cohesion: 0 internal dependency edges
  - Cross-group coupling: 0 external dependency edges
- **Member Files:**
  - `scratch/gameproof_003/retired_cli_bridge/run_gameproof_003_cli.py`
- **Inbound Interface Files (0):**
- **Outbound Interface Files (0):**

### Root Components
- **Confidence:** High
- **Claim Type:** inferred
- **Member Count:** 3
- **Structurally Ambiguous:** No
- **Grouping Basis:** seed: directory_structure, refined_by: dependency_cohesion
- **Evidence:**
  - Files share directory structure: '.'
  - Internal cohesion: 0 internal dependency edges
  - Cross-group coupling: 0 external dependency edges
- **Member Files:**
  - `engainos_boot_kernel.py`
  - `start_button.py`
  - `tmp_qwen35_proof.py`
- **Inbound Interface Files (0):**
- **Outbound Interface Files (0):**

### Schemas Subsystem
- **Confidence:** Low
- **Claim Type:** inferred
- **Member Count:** 4
- **Structurally Ambiguous:** Yes
- **Grouping Basis:** seed: directory_structure, refined_by: dependency_cohesion
- **Evidence:**
  - Files share directory structure: 'tier1/paradox_machine/schemas'
  - Internal cohesion: 0 internal dependency edges
  - Cross-group coupling: 5 external dependency edges
  - Weak internal cohesion relative to strong cross-group coupling; marked as structurally ambiguous
- **Member Files:**
  - `tier1/paradox_machine/schemas/__init__.py`
  - `tier1/paradox_machine/schemas/paradox_state.py`
  - `tier1/paradox_machine/schemas/temporal_artifact.py`
  - `tier1/paradox_machine/schemas/temporal_truth_packet.py`
- **Inbound Interface Files (5):**
  - `scratch/test_temporal_contradiction.py`
  - `tier1/paradox_machine/extraction/naive_temporal_extractor.py`
  - `tier1/paradox_machine/gates/temporal_gate.py`
  - `tier1/paradox_machine/proofs/proof_007b_temporal_rejection.py`
  - `tier1/paradox_machine/reasoning/temporal_validator.py`
- **Outbound Interface Files (0):**

### Server Subsystem
- **Confidence:** High
- **Claim Type:** inferred
- **Member Count:** 2
- **Structurally Ambiguous:** No
- **Grouping Basis:** seed: directory_structure, refined_by: dependency_cohesion
- **Evidence:**
  - Files share directory structure: 'tier1/engainos/server'
  - Internal cohesion: 1 internal dependency edges
  - Cross-group coupling: 0 external dependency edges
- **Member Files:**
  - `tier1/engainos/server/__init__.py`
  - `tier1/engainos/server/safe_runtime_server_entrypoint.py`
- **Inbound Interface Files (0):**
- **Outbound Interface Files (0):**

### Showroom Subsystem
- **Confidence:** High
- **Claim Type:** inferred
- **Member Count:** 7
- **Structurally Ambiguous:** No
- **Grouping Basis:** seed: directory_structure, refined_by: dependency_cohesion
- **Evidence:**
  - Files share directory structure: 'tier2/engionality/showroom'
  - Internal cohesion: 7 internal dependency edges
  - Cross-group coupling: 4 external dependency edges
- **Member Files:**
  - `tier2/engionality/showroom/__init__.py`
  - `tier2/engionality/showroom/animation_engine.py`
  - `tier2/engionality/showroom/audio_engine.py`
  - `tier2/engionality/showroom/dialogue_engine.py`
  - `tier2/engionality/showroom/domain_views.py`
  - `tier2/engionality/showroom/performer_engine.py`
  - `tier2/engionality/showroom/scene_track.py`
- **Inbound Interface Files (3):**
  - `tier2/engionality/controlroom/bootstrap.py`
  - `tier2/engionality/controlroom/performance_harness.py`
  - `tier2/engionality/controlroom/runtime_loop.py`
- **Outbound Interface Files (1):**
  - `tier2/engionality/controlroom/task_types.py`

### Testing Suite
- **Confidence:** High
- **Claim Type:** inferred
- **Member Count:** 36
- **Structurally Ambiguous:** No
- **Grouping Basis:** seed: test_role_hint, refined_by: role_consolidation
- **Evidence:**
  - Consolidated based on test role hints across directories
  - Internal cohesion: 0 internal dependency edges
  - Cross-group coupling: 34 external dependency edges
- **Member Files:**
  - `scratch/test_temporal_contradiction.py`
  - `tier1/engainos/tests/test_gamestate_authority.py`
  - `tier1/mrlore/tests/test_accepted_lore_packet_schema.py`
  - `tier1/mrlore/tests/test_claim_extraction_runner.py`
  - `tier1/mrlore/tests/test_coming_calendar_registry_gate.py`
  - `tier1/mrlore/tests/test_contradiction_candidate_audit_summary.py`
  - `tier1/mrlore/tests/test_contradiction_candidate_grouper.py`
  - `tier1/mrlore/tests/test_cosmic_year_context_enrichment.py`
  - `tier1/mrlore/tests/test_entity_candidate_quality_gate.py`
  - `tier1/mrlore/tests/test_high_claim_scene_review_manifest.py`
  - `tier1/mrlore/tests/test_major_event_internal_receipt_map.py`
  - `tier1/mrlore/tests/test_manual_review_decision_example_writer.py`
  - `tier1/mrlore/tests/test_manual_review_decision_schema.py`
  - `tier1/mrlore/tests/test_p3_sequential_entity_second_pass_quality_audit.py`
  - `tier1/mrlore/tests/test_predicate_collision_policy_registry_gate.py`
  - `tier1/mrlore/tests/test_preserve_entity_allowlist_registry_gate.py`
  - `tier1/mrlore/tests/test_proposed_claim_audit_summary.py`
  - `tier1/mrlore/tests/test_proposed_claim_shape_gate.py`
  - `tier1/mrlore/tests/test_quality_aware_queue_summary.py`
  - `tier1/mrlore/tests/test_quality_aware_review_queue_builder.py`
  - `tier1/mrlore/tests/test_review_queue_builder.py`
  - `tier1/mrlore/tests/test_review_queue_clean_view.py`
  - `tier1/mrlore/tests/test_review_queue_noise_audit.py`
  - `tier1/mrlore/tests/test_review_rail_health_runner.py`
  - `tier1/mrlore/tests/test_revision_breathing_map.py`
  - `tier1/mrlore/tests/test_revision_breathing_map_guidance_gate.py`
  - `tier1/mrlore/tests/test_temporal_aware_queue_summary.py`
  - `tier1/mrlore/tests/test_temporal_aware_review_by_chapter_view.py`
  - `tier1/mrlore/tests/test_temporal_aware_review_queue_builder.py`
  - `tier1/mrlore/tests/test_temporal_claim_context_enrichment.py`
  - `tier1/mrlore/tests/test_temporal_collision_classification.py`
  - `tier1/paradox_machine/tests/__init__.py`
  - `tier1/paradox_machine/tests/test_temporal_artifact.py`
  - `tier1/paradox_machine/tests/test_temporal_gate.py`
  - `tier1/paradox_machine/tests/test_temporal_validator.py`
  - `tier2/godotsim/test_slice_builders.py`
- **Inbound Interface Files (0):**
- **Outbound Interface Files (34):**
  - `tier1/engainos/gates/gate_gamestate_draft_review_ready.py`
  - `tier1/mrlore/mrlore_accepted_lore_packet_schema.py`
  - `tier1/mrlore/mrlore_claim_extraction_runner.py`
  - `tier1/mrlore/mrlore_coming_calendar_registry_gate.py`
  - `tier1/mrlore/mrlore_contradiction_candidate_audit_summary.py`
  - `tier1/mrlore/mrlore_contradiction_candidate_grouper.py`
  - `tier1/mrlore/mrlore_cosmic_year_context_enrichment.py`
  - `tier1/mrlore/mrlore_entity_candidate_quality_gate.py`
  - `tier1/mrlore/mrlore_high_claim_scene_review_manifest.py`
  - `tier1/mrlore/mrlore_major_event_internal_receipt_map.py`
  - `tier1/mrlore/mrlore_manual_review_decision_example_writer.py`
  - `tier1/mrlore/mrlore_manual_review_decision_schema.py`
  - `tier1/mrlore/mrlore_p3_sequential_entity_second_pass_quality_audit.py`
  - `tier1/mrlore/mrlore_predicate_collision_policy_registry_gate.py`
  - `tier1/mrlore/mrlore_preserve_entity_allowlist_registry_gate.py`
  - `tier1/mrlore/mrlore_proposed_claim_audit_summary.py`
  - `tier1/mrlore/mrlore_proposed_claim_shape_gate.py`
  - `tier1/mrlore/mrlore_quality_aware_queue_summary.py`
  - `tier1/mrlore/mrlore_quality_aware_review_queue_builder.py`
  - `tier1/mrlore/mrlore_review_queue_builder.py`
  - `tier1/mrlore/mrlore_review_queue_clean_view.py`
  - `tier1/mrlore/mrlore_review_queue_noise_audit.py`
  - `tier1/mrlore/mrlore_review_rail_health_runner.py`
  - `tier1/mrlore/mrlore_revision_breathing_map.py`
  - `tier1/mrlore/mrlore_revision_breathing_map_guidance_gate.py`
  - `tier1/mrlore/mrlore_temporal_aware_queue_summary.py`
  - `tier1/mrlore/mrlore_temporal_aware_review_by_chapter_view.py`
  - `tier1/mrlore/mrlore_temporal_aware_review_queue_builder.py`
  - `tier1/mrlore/mrlore_temporal_claim_context_enrichment.py`
  - `tier1/mrlore/mrlore_temporal_collision_classification.py`
  - `tier1/paradox_machine/reasoning/temporal_validator.py`
  - `tier1/paradox_machine/schemas/temporal_artifact.py`
  - `tier2/godotsim/slice_builders.py`
  - `tier2/godotsim/slice_types.py`

### Tier2 Subsystem
- **Confidence:** High
- **Claim Type:** inferred
- **Member Count:** 1
- **Structurally Ambiguous:** No
- **Grouping Basis:** seed: directory_structure, refined_by: dependency_cohesion
- **Evidence:**
  - Files share directory structure: 'tier2'
  - Internal cohesion: 0 internal dependency edges
  - Cross-group coupling: 0 external dependency edges
- **Member Files:**
  - `tier2/__init__.py`
- **Inbound Interface Files (0):**
- **Outbound Interface Files (0):**

### Tier3 Subsystem
- **Confidence:** High
- **Claim Type:** inferred
- **Member Count:** 1
- **Structurally Ambiguous:** No
- **Grouping Basis:** seed: directory_structure, refined_by: dependency_cohesion
- **Evidence:**
  - Files share directory structure: 'tier3'
  - Internal cohesion: 0 internal dependency edges
  - Cross-group coupling: 0 external dependency edges
- **Member Files:**
  - `tier3/__init__.py`
- **Inbound Interface Files (0):**
- **Outbound Interface Files (0):**

### Tools Subsystem
- **Confidence:** Low
- **Claim Type:** inferred
- **Member Count:** 5
- **Structurally Ambiguous:** Yes
- **Grouping Basis:** seed: directory_structure, refined_by: dependency_cohesion
- **Evidence:**
  - Files share directory structure: 'tier1/engainos/tools, tier1/mrlore/tools, tools'
  - Internal cohesion: 0 internal dependency edges
  - Cross-group coupling: 1 external dependency edges
  - Weak internal cohesion relative to strong cross-group coupling; marked as structurally ambiguous
- **Member Files:**
  - `tier1/engainos/tools/chapter_discovery.py`
  - `tier1/engainos/tools/vault_discovery.py`
  - `tier1/mrlore/tools/__init__.py`
  - `tier1/mrlore/tools/mrlore_full_output_dump.py`
  - `tools/ollama_diff_patcher.py`
- **Inbound Interface Files (1):**
  - `tier2/godotsim/gates/gate_ollama_diff_patcher_tests.py`
- **Outbound Interface Files (0):**

### Topologist Subsystem
- **Confidence:** High
- **Claim Type:** inferred
- **Member Count:** 1
- **Structurally Ambiguous:** No
- **Grouping Basis:** seed: directory_structure, refined_by: dependency_cohesion
- **Evidence:**
  - Files share directory structure: 'tier2/topologist'
  - Internal cohesion: 0 internal dependency edges
  - Cross-group coupling: 0 external dependency edges
- **Member Files:**
  - `tier2/topologist/__init__.py`
- **Inbound Interface Files (0):**
- **Outbound Interface Files (0):**

### Unsorted Subsystem
- **Confidence:** High
- **Claim Type:** inferred
- **Member Count:** 1
- **Structurally Ambiguous:** No
- **Grouping Basis:** seed: directory_structure, refined_by: dependency_cohesion
- **Evidence:**
  - Files share directory structure: 'tier1/engainos/core/unsorted'
  - Internal cohesion: 0 internal dependency edges
  - Cross-group coupling: 0 external dependency edges
- **Member Files:**
  - `tier1/engainos/core/unsorted/__init__.py`
- **Inbound Interface Files (0):**
- **Outbound Interface Files (0):**

### Validators Subsystem
- **Confidence:** High
- **Claim Type:** inferred
- **Member Count:** 3
- **Structurally Ambiguous:** No
- **Grouping Basis:** seed: directory_structure, refined_by: dependency_cohesion
- **Evidence:**
  - Files share directory structure: 'tier1/engainos/validators'
  - Internal cohesion: 1 internal dependency edges
  - Cross-group coupling: 0 external dependency edges
- **Member Files:**
  - `tier1/engainos/validators/__init__.py`
  - `tier1/engainos/validators/runtime_stage_identity.py`
  - `tier1/engainos/validators/runtime_stage_manifest.py`
- **Inbound Interface Files (0):**
- **Outbound Interface Files (0):**

### Vaultroom Subsystem
- **Confidence:** High
- **Claim Type:** inferred
- **Member Count:** 2
- **Structurally Ambiguous:** No
- **Grouping Basis:** seed: directory_structure, refined_by: dependency_cohesion
- **Evidence:**
  - Files share directory structure: 'tier3/mettaext/vaultroom'
  - Internal cohesion: 0 internal dependency edges
  - Cross-group coupling: 0 external dependency edges
- **Member Files:**
  - `tier3/mettaext/vaultroom/__init__.py`
  - `tier3/mettaext/vaultroom/vault_source_index.py`
- **Inbound Interface Files (0):**
- **Outbound Interface Files (0):**

### Zwcodecs Subsystem
- **Confidence:** Low
- **Claim Type:** inferred
- **Member Count:** 2
- **Structurally Ambiguous:** Yes
- **Grouping Basis:** seed: directory_structure, refined_by: dependency_cohesion
- **Evidence:**
  - Files share directory structure: 'tier1/paradox_machine/zwcodecs'
  - Internal cohesion: 0 internal dependency edges
  - Cross-group coupling: 1 external dependency edges
  - Weak internal cohesion relative to strong cross-group coupling; marked as structurally ambiguous
- **Member Files:**
  - `tier1/paradox_machine/zwcodecs/__init__.py`
  - `tier1/paradox_machine/zwcodecs/json_to_zw.py`
- **Inbound Interface Files (1):**
  - `tier1/paradox_machine/proofs/export_gate_triad_result_zw.py`
- **Outbound Interface Files (0):**

## 3. Top Ranked Next Files to Inspect (Top 10)
1. `tier2/godotsim/bridge_integration.py` (Score: **100**)
   - **Reasons:** parse_error
   - **Evidence:**
     - parse_error: AmbiguousImportError: Import 'semantic_bridge.SemanticRegistry' resolved to multiple local candidates: ['tier1/engainos/bridgeroom/semantic_bridge.py', 'tier2/godotsim/semantic_bridge.py'].

2. `tier2/godotsim/bridge_integration.py` (Score: **100**)
   - **Reasons:** parse_error
   - **Evidence:**
     - parse_error: AmbiguousImportError: Import 'semantic_bridge.zon_to_entity3d' resolved to multiple local candidates: ['tier1/engainos/bridgeroom/semantic_bridge.py', 'tier2/godotsim/semantic_bridge.py'].

3. `tier1/paradox_machine/reasoning/stn.py` (Score: **80**)
   - **Reasons:** structurally_ambiguous_subsystem, stubbed_implementation
   - **Evidence:**
     - member_of: candidate_subsystem_groups.Reasoning Subsystem
     - status: stubbed

4. `tier1/paradox_machine/schemas/paradox_state.py` (Score: **80**)
   - **Reasons:** structurally_ambiguous_subsystem, stubbed_implementation
   - **Evidence:**
     - member_of: candidate_subsystem_groups.Schemas Subsystem
     - status: stubbed

5. `tier1/paradox_machine/schemas/temporal_truth_packet.py` (Score: **80**)
   - **Reasons:** structurally_ambiguous_subsystem, stubbed_implementation
   - **Evidence:**
     - member_of: candidate_subsystem_groups.Schemas Subsystem
     - status: stubbed

6. `tier2/godotsim/builders/godot_scene_piece_builder.py` (Score: **77**)
   - **Reasons:** structurally_ambiguous_subsystem, high_inbound_coupling, high_outbound_coupling
   - **Evidence:**
     - member_of: candidate_subsystem_groups.Builders Subsystem
     - inbound_count: 6
     - outbound_count: 1

7. `tier1/paradox_machine/schemas/temporal_artifact.py` (Score: **75**)
   - **Reasons:** structurally_ambiguous_subsystem, high_inbound_coupling
   - **Evidence:**
     - member_of: candidate_subsystem_groups.Schemas Subsystem
     - inbound_count: 5

8. `tier2/godotsim/kernels/combat3d_mr.py` (Score: **75**)
   - **Reasons:** structurally_ambiguous_subsystem, high_inbound_coupling
   - **Evidence:**
     - member_of: candidate_subsystem_groups.Kernels Subsystem
     - inbound_count: 5

9. `tier2/godotsim/kernels/piece3d_mr.py` (Score: **75**)
   - **Reasons:** structurally_ambiguous_subsystem, high_inbound_coupling
   - **Evidence:**
     - member_of: candidate_subsystem_groups.Kernels Subsystem
     - inbound_count: 11

10. `tier1/paradox_machine/reasoning/temporal_validator.py` (Score: **74**)
   - **Reasons:** structurally_ambiguous_subsystem, high_inbound_coupling, high_outbound_coupling
   - **Evidence:**
     - member_of: candidate_subsystem_groups.Reasoning Subsystem
     - inbound_count: 4
     - outbound_count: 2

## 4. Path and Dependency Routes
These paths describe **static dependency routes** determined by import statements. The file order reflects the **dependency traversal order** (DFS) from the entrypoint, which is not a proven runtime execution call order. Suggested inspection order is **advisory only**.

### Static Route from entrypoint: `command_center/app.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `command_center/app.py`

### Static Route from entrypoint: `engainos_boot_kernel.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `engainos_boot_kernel.py`

### Static Route from entrypoint: `executors/boot_scene_load_executor_v1.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `executors/boot_scene_load_executor_v1.py`

### Static Route from entrypoint: `executors/player_input_listener_executor_v1.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `executors/player_input_listener_executor_v1.py`

### Static Route from entrypoint: `gates/gate_boot_scene_authorization_request_v1.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `gates/gate_boot_scene_authorization_request_v1.py`

### Static Route from entrypoint: `gates/gate_boot_scene_load_executor_request_v1.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `gates/gate_boot_scene_load_executor_request_v1.py`

### Static Route from entrypoint: `gates/gate_boot_shell_presentation_ready_v1.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `gates/gate_boot_shell_presentation_ready_v1.py`

### Static Route from entrypoint: `gates/gate_engainos_bootstrap_preflight_v1.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `gates/gate_engainos_bootstrap_preflight_v1.py`

### Static Route from entrypoint: `gates/gate_engainos_system_health_preflight_v1.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `gates/gate_engainos_system_health_preflight_v1.py`

### Static Route from entrypoint: `gates/gate_player_input_authorization_request_v1.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `gates/gate_player_input_authorization_request_v1.py`

### Static Route from entrypoint: `gates/gate_player_input_listener_executor_request_v1.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `gates/gate_player_input_listener_executor_request_v1.py`

### Static Route from entrypoint: `interface/000_status.py`
- **Advisory Next File to Inspect in Route:** `interface/interface_common.py`
- **Dependency Traversal Flow:**
  - `interface/000_status.py`
  - `interface/interface_common.py`

### Static Route from entrypoint: `interface/010_show_protected_files.py`
- **Advisory Next File to Inspect in Route:** `interface/interface_common.py`
- **Dependency Traversal Flow:**
  - `interface/010_show_protected_files.py`
  - `interface/interface_common.py`

### Static Route from entrypoint: `interface/020_show_ledger.py`
- **Advisory Next File to Inspect in Route:** `interface/interface_common.py`
- **Dependency Traversal Flow:**
  - `interface/020_show_ledger.py`
  - `interface/interface_common.py`

### Static Route from entrypoint: `interface/030_create_task_packet.py`
- **Advisory Next File to Inspect in Route:** `interface/interface_common.py`
- **Dependency Traversal Flow:**
  - `interface/030_create_task_packet.py`
  - `interface/interface_common.py`

### Static Route from entrypoint: `interface/040_show_next_command.py`
- **Advisory Next File to Inspect in Route:** `interface/interface_common.py`
- **Dependency Traversal Flow:**
  - `interface/040_show_next_command.py`
  - `interface/interface_common.py`

### Static Route from entrypoint: `interface/050_record_command_output.py`
- **Advisory Next File to Inspect in Route:** `interface/interface_common.py`
- **Dependency Traversal Flow:**
  - `interface/050_record_command_output.py`
  - `interface/interface_common.py`

### Static Route from entrypoint: `interface/060_run_py_compile.py`
- **Advisory Next File to Inspect in Route:** `interface/interface_common.py`
- **Dependency Traversal Flow:**
  - `interface/060_run_py_compile.py`
  - `interface/interface_common.py`

### Static Route from entrypoint: `interface/070_run_headless_gate.py`
- **Advisory Next File to Inspect in Route:** `interface/interface_common.py`
- **Dependency Traversal Flow:**
  - `interface/070_run_headless_gate.py`
  - `interface/interface_common.py`

### Static Route from entrypoint: `interface/080_stamp_result.py`
- **Advisory Next File to Inspect in Route:** `interface/interface_common.py`
- **Dependency Traversal Flow:**
  - `interface/080_stamp_result.py`
  - `interface/interface_common.py`

### Static Route from entrypoint: `interface/090_recover_file_from_git.py`
- **Advisory Next File to Inspect in Route:** `interface/interface_common.py`
- **Dependency Traversal Flow:**
  - `interface/090_recover_file_from_git.py`
  - `interface/interface_common.py`

### Static Route from entrypoint: `interface/999_console.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `interface/999_console.py`

### Static Route from entrypoint: `scratch/gameproof_003/retired_cli_bridge/run_gameproof_003_cli.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `scratch/gameproof_003/retired_cli_bridge/run_gameproof_003_cli.py`

### Static Route from entrypoint: `scratch/tier_relocation/trixel/legacy_payloads/harvest_legacy_trixel_payloads.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `scratch/tier_relocation/trixel/legacy_payloads/harvest_legacy_trixel_payloads.py`

### Static Route from entrypoint: `start_button.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `start_button.py`

### Static Route from entrypoint: `tier1/engainos/adapters/zonj_to_gamestate.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `tier1/engainos/adapters/zonj_to_gamestate.py`

### Static Route from entrypoint: `tier1/engainos/aproom/ap_engine.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `tier1/engainos/aproom/ap_engine.py`

### Static Route from entrypoint: `tier1/engainos/aproom/ap_quest_rules.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `tier1/engainos/aproom/ap_quest_rules.py`

### Static Route from entrypoint: `tier1/engainos/aproom/ap_rule_loader.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `tier1/engainos/aproom/ap_rule_loader.py`

### Static Route from entrypoint: `tier1/engainos/aproom/ap_runtime.py`
- **Advisory Next File to Inspect in Route:** `tier1/engainos/aproom/ap_zw_engine.py`
- **Dependency Traversal Flow:**
  - `tier1/engainos/aproom/ap_runtime.py`
  - `tier1/engainos/aproom/ap_zw_engine.py`

### Static Route from entrypoint: `tier1/engainos/aproom/ap_world_rules.py`
- **Advisory Next File to Inspect in Route:** `tier1/engainos/aproom/engine_summary.py`
- **Dependency Traversal Flow:**
  - `tier1/engainos/aproom/ap_world_rules.py`
  - `tier1/engainos/aproom/engine_summary.py`

### Static Route from entrypoint: `tier1/engainos/aproom/ap_zw_engine.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `tier1/engainos/aproom/ap_zw_engine.py`

### Static Route from entrypoint: `tier1/engainos/aproom/engine_summary.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `tier1/engainos/aproom/engine_summary.py`

### Static Route from entrypoint: `tier1/engainos/aproom/protocol_envelope.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `tier1/engainos/aproom/protocol_envelope.py`

### Static Route from entrypoint: `tier1/engainos/bridgeroom/godot_adapter.py`
- **Advisory Next File to Inspect in Route:** `tier1/engainos/bridgeroom/spatial_skin_system.py`
- **Dependency Traversal Flow:**
  - `tier1/engainos/bridgeroom/godot_adapter.py`
  - `tier1/engainos/bridgeroom/spatial_skin_system.py`
  - `tier1/engainos/bridgeroom/zon_to_entities.py`
  - `tier1/engainos/bridgeroom/mesh_manifest.py`

### Static Route from entrypoint: `tier1/engainos/bridgeroom/quest3d_integration.py`
- **Advisory Next File to Inspect in Route:** `tier2/godotsim/kernels/quest3d_mr.py`
- **Dependency Traversal Flow:**
  - `tier1/engainos/bridgeroom/quest3d_integration.py`
  - `tier2/godotsim/kernels/quest3d_mr.py` ➔ **Inferred Boundary Crossing:** (Bridgeroom Subsystem ➔ Kernels Subsystem)

### Static Route from entrypoint: `tier1/engainos/bridgeroom/scene_loader.py`
- **Advisory Next File to Inspect in Route:** `tier3/mettaext/scene_identity.py`
- **Dependency Traversal Flow:**
  - `tier1/engainos/bridgeroom/scene_loader.py`
  - `tier1/engainos/bridgeroom/spatial_reasoner.py`
  - `tier1/engainos/bridgeroom/spatial_skin_system.py`
  - `tier3/mettaext/scene_identity.py` ➔ **Inferred Boundary Crossing:** (Bridgeroom Subsystem ➔ Mettaext Subsystem)

### Static Route from entrypoint: `tier1/engainos/bridgeroom/scene_server.py`
- **Advisory Next File to Inspect in Route:** `tier3/mettaext/scene_identity.py`
- **Dependency Traversal Flow:**
  - `tier1/engainos/bridgeroom/scene_server.py`
  - `tier1/engainos/bridgeroom/scene_loader.py`
  - `tier1/engainos/bridgeroom/spatial_reasoner.py`
  - `tier1/engainos/bridgeroom/spatial_skin_system.py`
  - `tier3/mettaext/scene_identity.py` ➔ **Inferred Boundary Crossing:** (Bridgeroom Subsystem ➔ Mettaext Subsystem)

### Static Route from entrypoint: `tier1/engainos/bridgeroom/zon_to_game.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `tier1/engainos/bridgeroom/zon_to_game.py`

### Static Route from entrypoint: `tier1/engainos/core/no_godot_scene_proof.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `tier1/engainos/core/no_godot_scene_proof.py`

### Static Route from entrypoint: `tier1/engainos/engainos_control_center.py`
- **Advisory Next File to Inspect in Route:** `tier1/engainos/gates/gate_acceptance_rule.py`
- **Dependency Traversal Flow:**
  - `tier1/engainos/engainos_control_center.py`
  - `tier1/engainos/gates/gate_acceptance_rule.py` ➔ **Inferred Boundary Crossing:** (Engainos Subsystem ➔ Gates Subsystem)
  - `tier1/engainos/gates/gate_declared_truth_shape.py` ➔ **Inferred Boundary Crossing:** (Engainos Subsystem ➔ Gates Subsystem)
  - `tier1/engainos/gates/gate_governance_rejection_proof.py` ➔ **Inferred Boundary Crossing:** (Engainos Subsystem ➔ Gates Subsystem)
  - `tier1/engainos/gates/gate_no_asset_production.py`
  - `tier1/engainos/gates/gate_no_presentation_authority.py`
  - `tier1/engainos/gates/gate_no_simulation_execution.py`
  - `tier1/engainos/gates/gate_no_lane_theft_in_packet.py` ➔ **Inferred Boundary Crossing:** (Engainos Subsystem ➔ Gates Subsystem)
  - `tier1/engainos/gates/gate_packet_identity.py` ➔ **Inferred Boundary Crossing:** (Engainos Subsystem ➔ Gates Subsystem)
  - `tier1/engainos/gates/gate_validated_packets_shape.py` ➔ **Inferred Boundary Crossing:** (Engainos Subsystem ➔ Gates Subsystem)

### Static Route from entrypoint: `tier1/engainos/engainos_server.py`
- **Advisory Next File to Inspect in Route:** `tier1/engainos/runtime_client.py`
- **Dependency Traversal Flow:**
  - `tier1/engainos/engainos_server.py`
  - `tier1/engainos/runtime_client.py`

### Static Route from entrypoint: `tier1/engainos/gates/gate_ap_core_behavior_parity.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `tier1/engainos/gates/gate_ap_core_behavior_parity.py`

### Static Route from entrypoint: `tier1/engainos/gates/gate_ap_core_migration_authority.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `tier1/engainos/gates/gate_ap_core_migration_authority.py`

### Static Route from entrypoint: `tier1/engainos/gates/gate_ap_core_rule_activation.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `tier1/engainos/gates/gate_ap_core_rule_activation.py`

### Static Route from entrypoint: `tier1/engainos/gates/gate_ap_core_signature_probe.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `tier1/engainos/gates/gate_ap_core_signature_probe.py`

### Static Route from entrypoint: `tier1/engainos/gates/gate_ap_default_rules_registered.py`
- **Advisory Next File to Inspect in Route:** `tier1/engainos/core/__init__.py`
- **Dependency Traversal Flow:**
  - `tier1/engainos/gates/gate_ap_default_rules_registered.py`
  - `tier1/engainos/core/__init__.py` ➔ **Inferred Boundary Crossing:** (Gates Subsystem ➔ Core Subsystem)

### Static Route from entrypoint: `tier1/engainos/gates/gate_ap_engine_historical_probe.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `tier1/engainos/gates/gate_ap_engine_historical_probe.py`

### Static Route from entrypoint: `tier1/engainos/gates/gate_ap_engine_historical_source_map.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `tier1/engainos/gates/gate_ap_engine_historical_source_map.py`

### Static Route from entrypoint: `tier1/engainos/gates/gate_ap_engine_migration_authority.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `tier1/engainos/gates/gate_ap_engine_migration_authority.py`

### Static Route from entrypoint: `tier1/engainos/gates/gate_ap_runtime_behavior_probe.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `tier1/engainos/gates/gate_ap_runtime_behavior_probe.py`

### Static Route from entrypoint: `tier1/engainos/gates/gate_ap_runtime_blocker_lane.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `tier1/engainos/gates/gate_ap_runtime_blocker_lane.py`

### Static Route from entrypoint: `tier1/engainos/gates/gate_ap_runtime_relay_behavior.py`
- **Advisory Next File to Inspect in Route:** `tier1/engainos/relays/ap_runtime_relay.py`
- **Dependency Traversal Flow:**
  - `tier1/engainos/gates/gate_ap_runtime_relay_behavior.py`
  - `tier1/engainos/relays/ap_runtime_relay.py` ➔ **Inferred Boundary Crossing:** (Gates Subsystem ➔ Relays Subsystem)

### Static Route from entrypoint: `tier1/engainos/gates/gate_ap_runtime_relay_readiness.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `tier1/engainos/gates/gate_ap_runtime_relay_readiness.py`

### Static Route from entrypoint: `tier1/engainos/gates/gate_ap_runtime_relay_real_integration.py`
- **Advisory Next File to Inspect in Route:** `tier1/engainos/relays/ap_runtime_relay.py`
- **Dependency Traversal Flow:**
  - `tier1/engainos/gates/gate_ap_runtime_relay_real_integration.py`
  - `tier1/engainos/relays/ap_runtime_relay.py` ➔ **Inferred Boundary Crossing:** (Gates Subsystem ➔ Relays Subsystem)

### Static Route from entrypoint: `tier1/engainos/gates/gate_ap_runtime_repair_readiness.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `tier1/engainos/gates/gate_ap_runtime_repair_readiness.py`

### Static Route from entrypoint: `tier1/engainos/gates/gate_ap_zw_engine_canonical_claim.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `tier1/engainos/gates/gate_ap_zw_engine_canonical_claim.py`

### Static Route from entrypoint: `tier1/engainos/gates/gate_ap_zw_engine_migration.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `tier1/engainos/gates/gate_ap_zw_engine_migration.py`

### Static Route from entrypoint: `tier1/engainos/gates/gate_ap_zw_engine_timeline_fence.py`
- **Advisory Next File to Inspect in Route:** `tier1/engainos/core/__init__.py`
- **Dependency Traversal Flow:**
  - `tier1/engainos/gates/gate_ap_zw_engine_timeline_fence.py`
  - `tier1/engainos/core/__init__.py` ➔ **Inferred Boundary Crossing:** (Gates Subsystem ➔ Core Subsystem)

### Static Route from entrypoint: `tier1/engainos/gates/gate_controlled_runtime_salvage_lane.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `tier1/engainos/gates/gate_controlled_runtime_salvage_lane.py`

### Static Route from entrypoint: `tier1/engainos/gates/gate_gamestate_draft_review_contract.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `tier1/engainos/gates/gate_gamestate_draft_review_contract.py`

### Static Route from entrypoint: `tier1/engainos/gates/gate_gamestate_draft_review_ready.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `tier1/engainos/gates/gate_gamestate_draft_review_ready.py`

### Static Route from entrypoint: `tier1/engainos/gates/gate_governance_contract_board.py`
- **Advisory Next File to Inspect in Route:** `tier1/engainos/gates/gate_acceptance_rule.py`
- **Dependency Traversal Flow:**
  - `tier1/engainos/gates/gate_governance_contract_board.py`
  - `tier1/engainos/gates/gate_acceptance_rule.py`
  - `tier1/engainos/gates/gate_declared_truth_shape.py`
  - `tier1/engainos/gates/gate_no_asset_production.py`
  - `tier1/engainos/gates/gate_no_lane_theft_in_packet.py`
  - `tier1/engainos/gates/gate_no_presentation_authority.py`
  - `tier1/engainos/gates/gate_no_simulation_execution.py`
  - `tier1/engainos/gates/gate_packet_identity.py`
  - `tier1/engainos/gates/gate_validated_packets_shape.py`

### Static Route from entrypoint: `tier1/engainos/gates/gate_safe_server_wrapper_behavior_lane.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `tier1/engainos/gates/gate_safe_server_wrapper_behavior_lane.py`

### Static Route from entrypoint: `tier1/engainos/gates/gate_safe_server_wrapper_blueprint_lane.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `tier1/engainos/gates/gate_safe_server_wrapper_blueprint_lane.py`

### Static Route from entrypoint: `tier1/engainos/gates/gate_safe_server_wrapper_implementation_lane.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `tier1/engainos/gates/gate_safe_server_wrapper_implementation_lane.py`

### Static Route from entrypoint: `tier1/engainos/gates/gate_server_entrypoint_repair_lane.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `tier1/engainos/gates/gate_server_entrypoint_repair_lane.py`

### Static Route from entrypoint: `tier1/engainos/gates/gate_server_runtime_preflight_lane.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `tier1/engainos/gates/gate_server_runtime_preflight_lane.py`

### Static Route from entrypoint: `tier1/engainos/gates/gate_vault_boot_side_effect_fence_lane.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `tier1/engainos/gates/gate_vault_boot_side_effect_fence_lane.py`

### Static Route from entrypoint: `tier1/engainos/gates/run_active_gates.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `tier1/engainos/gates/run_active_gates.py`

### Static Route from entrypoint: `tier1/engainos/launch_engine.py`
- **Advisory Next File to Inspect in Route:** `tier3/mettaext/scene_identity.py`
- **Dependency Traversal Flow:**
  - `tier1/engainos/launch_engine.py`
  - `tier1/engainos/aproom/ap_engine.py` ➔ **Inferred Boundary Crossing:** (Engainos Subsystem ➔ Aproom Subsystem)
  - `tier1/engainos/aproom/ap_runtime.py` ➔ **Inferred Boundary Crossing:** (Engainos Subsystem ➔ Aproom Subsystem)
  - `tier1/engainos/aproom/ap_zw_engine.py`
  - `tier1/engainos/bridgeroom/godot_adapter.py` ➔ **Inferred Boundary Crossing:** (Engainos Subsystem ➔ Bridgeroom Subsystem)
  - `tier1/engainos/bridgeroom/spatial_skin_system.py`
  - `tier1/engainos/bridgeroom/zon_to_entities.py`
  - `tier1/engainos/bridgeroom/mesh_manifest.py`
  - `tier1/engainos/bridgeroom/scene_server.py` ➔ **Inferred Boundary Crossing:** (Engainos Subsystem ➔ Bridgeroom Subsystem)
  - `tier1/engainos/bridgeroom/scene_loader.py`
  - `tier1/engainos/bridgeroom/spatial_reasoner.py`
  - `tier3/mettaext/scene_identity.py` ➔ **Inferred Boundary Crossing:** (Bridgeroom Subsystem ➔ Mettaext Subsystem)

### Static Route from entrypoint: `tier1/engainos/tools/chapter_discovery.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `tier1/engainos/tools/chapter_discovery.py`

### Static Route from entrypoint: `tier1/engainos/tools/chapter_splitter/chapter_to_stage_packets.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `tier1/engainos/tools/chapter_splitter/chapter_to_stage_packets.py`

### Static Route from entrypoint: `tier1/engainos/tools/chapter_splitter/promote_stage_draft.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `tier1/engainos/tools/chapter_splitter/promote_stage_draft.py`

### Static Route from entrypoint: `tier1/engainos/tools/vault_discovery.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `tier1/engainos/tools/vault_discovery.py`

### Static Route from entrypoint: `tier1/engainos/validators/runtime_stage_identity.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `tier1/engainos/validators/runtime_stage_identity.py`

### Static Route from entrypoint: `tier1/engainos/validators/runtime_stage_manifest.py`
- **Advisory Next File to Inspect in Route:** `tier1/engainos/validators/runtime_stage_identity.py`
- **Dependency Traversal Flow:**
  - `tier1/engainos/validators/runtime_stage_manifest.py`
  - `tier1/engainos/validators/runtime_stage_identity.py`

### Static Route from entrypoint: `tier1/mrlore/archive/old_tools/artifact_extractor.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `tier1/mrlore/archive/old_tools/artifact_extractor.py`

### Static Route from entrypoint: `tier1/mrlore/archive/old_tools/authority_score_calculator.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `tier1/mrlore/archive/old_tools/authority_score_calculator.py`

### Static Route from entrypoint: `tier1/mrlore/archive/old_tools/build_codex_candidates.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `tier1/mrlore/archive/old_tools/build_codex_candidates.py`

### Static Route from entrypoint: `tier1/mrlore/archive/old_tools/build_registry.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `tier1/mrlore/archive/old_tools/build_registry.py`

### Static Route from entrypoint: `tier1/mrlore/archive/old_tools/chapter_ledger_extractor.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `tier1/mrlore/archive/old_tools/chapter_ledger_extractor.py`

### Static Route from entrypoint: `tier1/mrlore/archive/old_tools/compile_entity_states.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `tier1/mrlore/archive/old_tools/compile_entity_states.py`

### Static Route from entrypoint: `tier1/mrlore/archive/old_tools/continuity_audit.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `tier1/mrlore/archive/old_tools/continuity_audit.py`

### Static Route from entrypoint: `tier1/mrlore/archive/old_tools/draft_rel_evidence_review.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `tier1/mrlore/archive/old_tools/draft_rel_evidence_review.py`

### Static Route from entrypoint: `tier1/mrlore/archive/old_tools/extract_candidates.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `tier1/mrlore/archive/old_tools/extract_candidates.py`

### Static Route from entrypoint: `tier1/mrlore/archive/old_tools/extract_member_of.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `tier1/mrlore/archive/old_tools/extract_member_of.py`

### Static Route from entrypoint: `tier1/mrlore/archive/old_tools/identity_review_queue.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `tier1/mrlore/archive/old_tools/identity_review_queue.py`

### Static Route from entrypoint: `tier1/mrlore/archive/old_tools/identity_reviewer.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `tier1/mrlore/archive/old_tools/identity_reviewer.py`

### Static Route from entrypoint: `tier1/mrlore/archive/old_tools/identity_signal_math.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `tier1/mrlore/archive/old_tools/identity_signal_math.py`

### Static Route from entrypoint: `tier1/mrlore/archive/old_tools/ingest_source_stub.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `tier1/mrlore/archive/old_tools/ingest_source_stub.py`

### Static Route from entrypoint: `tier1/mrlore/archive/old_tools/lint_codex_candidates.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `tier1/mrlore/archive/old_tools/lint_codex_candidates.py`

### Static Route from entrypoint: `tier1/mrlore/archive/old_tools/lint_entity_contract.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `tier1/mrlore/archive/old_tools/lint_entity_contract.py`

### Static Route from entrypoint: `tier1/mrlore/archive/old_tools/lint_relationship_schema.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `tier1/mrlore/archive/old_tools/lint_relationship_schema.py`

### Static Route from entrypoint: `tier1/mrlore/archive/old_tools/lint_scene_contract.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `tier1/mrlore/archive/old_tools/lint_scene_contract.py`

### Static Route from entrypoint: `tier1/mrlore/archive/old_tools/lint_wiki.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `tier1/mrlore/archive/old_tools/lint_wiki.py`

### Static Route from entrypoint: `tier1/mrlore/archive/old_tools/mrlore_query.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `tier1/mrlore/archive/old_tools/mrlore_query.py`

### Static Route from entrypoint: `tier1/mrlore/archive/old_tools/mrlore_rebuild_findings.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `tier1/mrlore/archive/old_tools/mrlore_rebuild_findings.py`

### Static Route from entrypoint: `tier1/mrlore/archive/old_tools/mrlore_run_changed.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `tier1/mrlore/archive/old_tools/mrlore_run_changed.py`

### Static Route from entrypoint: `tier1/mrlore/archive/old_tools/mrlore_session.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `tier1/mrlore/archive/old_tools/mrlore_session.py`

### Static Route from entrypoint: `tier1/mrlore/archive/old_tools/ollama_ingest_cockpit.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `tier1/mrlore/archive/old_tools/ollama_ingest_cockpit.py`

### Static Route from entrypoint: `tier1/mrlore/archive/old_tools/pass2_math.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `tier1/mrlore/archive/old_tools/pass2_math.py`

### Static Route from entrypoint: `tier1/mrlore/archive/old_tools/populate_registry.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `tier1/mrlore/archive/old_tools/populate_registry.py`

### Static Route from entrypoint: `tier1/mrlore/archive/old_tools/promote_candidate.py`
- **Advisory Next File to Inspect in Route:** `tier1/mrlore/archive/old_tools/authority_score_calculator.py`
- **Dependency Traversal Flow:**
  - `tier1/mrlore/archive/old_tools/promote_candidate.py`
  - `tier1/mrlore/archive/old_tools/authority_score_calculator.py`

### Static Route from entrypoint: `tier1/mrlore/archive/old_tools/promotion_eligibility_gate.py`
- **Advisory Next File to Inspect in Route:** `tier1/mrlore/archive/old_tools/authority_score_calculator.py`
- **Dependency Traversal Flow:**
  - `tier1/mrlore/archive/old_tools/promotion_eligibility_gate.py`
  - `tier1/mrlore/archive/old_tools/authority_score_calculator.py`

### Static Route from entrypoint: `tier1/mrlore/archive/old_tools/propose_corrections.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `tier1/mrlore/archive/old_tools/propose_corrections.py`

### Static Route from entrypoint: `tier1/mrlore/archive/old_tools/propose_rel_source_stubs.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `tier1/mrlore/archive/old_tools/propose_rel_source_stubs.py`

### Static Route from entrypoint: `tier1/mrlore/archive/old_tools/propose_rel_summaries.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `tier1/mrlore/archive/old_tools/propose_rel_summaries.py`

### Static Route from entrypoint: `tier1/mrlore/archive/old_tools/provisional_identity_router.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `tier1/mrlore/archive/old_tools/provisional_identity_router.py`

### Static Route from entrypoint: `tier1/mrlore/archive/old_tools/registry_builder.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `tier1/mrlore/archive/old_tools/registry_builder.py`

### Static Route from entrypoint: `tier1/mrlore/archive/old_tools/stb_lint.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `tier1/mrlore/archive/old_tools/stb_lint.py`

### Static Route from entrypoint: `tier1/mrlore/archive/old_tools/stb_scanner.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `tier1/mrlore/archive/old_tools/stb_scanner.py`

### Static Route from entrypoint: `tier1/mrlore/archive/old_tools/write_changed_manifest.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `tier1/mrlore/archive/old_tools/write_changed_manifest.py`

### Static Route from entrypoint: `tier1/mrlore/evidence/proofs/phase_4/collect_delta.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `tier1/mrlore/evidence/proofs/phase_4/collect_delta.py`

### Static Route from entrypoint: `tier1/mrlore/mrlore_accepted_lore_packet_schema.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `tier1/mrlore/mrlore_accepted_lore_packet_schema.py`

### Static Route from entrypoint: `tier1/mrlore/mrlore_claim_extraction_runner.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `tier1/mrlore/mrlore_claim_extraction_runner.py`

### Static Route from entrypoint: `tier1/mrlore/mrlore_coming_calendar_registry_gate.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `tier1/mrlore/mrlore_coming_calendar_registry_gate.py`

### Static Route from entrypoint: `tier1/mrlore/mrlore_contradiction_candidate_audit_summary.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `tier1/mrlore/mrlore_contradiction_candidate_audit_summary.py`

### Static Route from entrypoint: `tier1/mrlore/mrlore_contradiction_candidate_grouper.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `tier1/mrlore/mrlore_contradiction_candidate_grouper.py`

### Static Route from entrypoint: `tier1/mrlore/mrlore_control_center.py`
- **Advisory Next File to Inspect in Route:** `tier1/mrlore/gates/gate_contradictions_valid_if_present.py`
- **Dependency Traversal Flow:**
  - `tier1/mrlore/mrlore_control_center.py`
  - `tier1/mrlore/gates/gate_claims_structure.py` ➔ **Inferred Boundary Crossing:** (Mrlore Subsystem ➔ Gates Subsystem)
  - `tier1/mrlore/gates/gate_contradiction_stop_proof.py` ➔ **Inferred Boundary Crossing:** (Mrlore Subsystem ➔ Gates Subsystem)
  - `tier1/mrlore/gates/gate_contradictions_valid_if_present.py`
  - `tier1/mrlore/gates/gate_enum_values_valid.py` ➔ **Inferred Boundary Crossing:** (Mrlore Subsystem ➔ Gates Subsystem)
  - `tier1/mrlore/gates/gate_no_auto_resolve_attempt.py` ➔ **Inferred Boundary Crossing:** (Mrlore Subsystem ➔ Gates Subsystem)
  - `tier1/mrlore/gates/gate_no_lane_theft_in_packet.py` ➔ **Inferred Boundary Crossing:** (Mrlore Subsystem ➔ Gates Subsystem)
  - `tier1/mrlore/gates/gate_no_vault_path_dependency.py` ➔ **Inferred Boundary Crossing:** (Mrlore Subsystem ➔ Gates Subsystem)
  - `tier1/mrlore/gates/gate_required_fields.py` ➔ **Inferred Boundary Crossing:** (Mrlore Subsystem ➔ Gates Subsystem)

### Static Route from entrypoint: `tier1/mrlore/mrlore_cosmic_year_context_enrichment.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `tier1/mrlore/mrlore_cosmic_year_context_enrichment.py`

### Static Route from entrypoint: `tier1/mrlore/mrlore_entity_candidate_quality_gate.py`
- **Advisory Next File to Inspect in Route:** `tier1/mrlore/mrlore_preserve_entity_allowlist_registry_gate.py`
- **Dependency Traversal Flow:**
  - `tier1/mrlore/mrlore_entity_candidate_quality_gate.py`
  - `tier1/mrlore/mrlore_preserve_entity_allowlist_registry_gate.py`

### Static Route from entrypoint: `tier1/mrlore/mrlore_high_claim_scene_review_manifest.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `tier1/mrlore/mrlore_high_claim_scene_review_manifest.py`

### Static Route from entrypoint: `tier1/mrlore/mrlore_major_event_internal_receipt_map.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `tier1/mrlore/mrlore_major_event_internal_receipt_map.py`

### Static Route from entrypoint: `tier1/mrlore/mrlore_manual_review_decision_example_writer.py`
- **Advisory Next File to Inspect in Route:** `tier1/mrlore/mrlore_manual_review_decision_schema.py`
- **Dependency Traversal Flow:**
  - `tier1/mrlore/mrlore_manual_review_decision_example_writer.py`
  - `tier1/mrlore/mrlore_manual_review_decision_schema.py`

### Static Route from entrypoint: `tier1/mrlore/mrlore_manual_review_decision_schema.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `tier1/mrlore/mrlore_manual_review_decision_schema.py`

### Static Route from entrypoint: `tier1/mrlore/mrlore_p3_sequential_entity_second_pass_quality_audit.py`
- **Advisory Next File to Inspect in Route:** `tier1/mrlore/mrlore_preserve_entity_allowlist_registry_gate.py`
- **Dependency Traversal Flow:**
  - `tier1/mrlore/mrlore_p3_sequential_entity_second_pass_quality_audit.py`
  - `tier1/mrlore/mrlore_preserve_entity_allowlist_registry_gate.py`

### Static Route from entrypoint: `tier1/mrlore/mrlore_predicate_collision_policy_registry_gate.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `tier1/mrlore/mrlore_predicate_collision_policy_registry_gate.py`

### Static Route from entrypoint: `tier1/mrlore/mrlore_preserve_entity_allowlist_registry_gate.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `tier1/mrlore/mrlore_preserve_entity_allowlist_registry_gate.py`

### Static Route from entrypoint: `tier1/mrlore/mrlore_proposed_claim_audit_summary.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `tier1/mrlore/mrlore_proposed_claim_audit_summary.py`

### Static Route from entrypoint: `tier1/mrlore/mrlore_proposed_claim_shape_gate.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `tier1/mrlore/mrlore_proposed_claim_shape_gate.py`

### Static Route from entrypoint: `tier1/mrlore/mrlore_quality_aware_queue_summary.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `tier1/mrlore/mrlore_quality_aware_queue_summary.py`

### Static Route from entrypoint: `tier1/mrlore/mrlore_quality_aware_review_queue_builder.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `tier1/mrlore/mrlore_quality_aware_review_queue_builder.py`

### Static Route from entrypoint: `tier1/mrlore/mrlore_review_queue_builder.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `tier1/mrlore/mrlore_review_queue_builder.py`

### Static Route from entrypoint: `tier1/mrlore/mrlore_review_queue_clean_view.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `tier1/mrlore/mrlore_review_queue_clean_view.py`

### Static Route from entrypoint: `tier1/mrlore/mrlore_review_queue_noise_audit.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `tier1/mrlore/mrlore_review_queue_noise_audit.py`

### Static Route from entrypoint: `tier1/mrlore/mrlore_review_rail_health_runner.py`
- **Advisory Next File to Inspect in Route:** `tier1/mrlore/mrlore_preserve_entity_allowlist_registry_gate.py`
- **Dependency Traversal Flow:**
  - `tier1/mrlore/mrlore_review_rail_health_runner.py`
  - `tier1/mrlore/mrlore_claim_extraction_runner.py`
  - `tier1/mrlore/mrlore_contradiction_candidate_audit_summary.py`
  - `tier1/mrlore/mrlore_contradiction_candidate_grouper.py`
  - `tier1/mrlore/mrlore_entity_candidate_quality_gate.py`
  - `tier1/mrlore/mrlore_preserve_entity_allowlist_registry_gate.py`
  - `tier1/mrlore/mrlore_high_claim_scene_review_manifest.py`
  - `tier1/mrlore/mrlore_manual_review_decision_example_writer.py`
  - `tier1/mrlore/mrlore_manual_review_decision_schema.py`
  - `tier1/mrlore/mrlore_proposed_claim_audit_summary.py`
  - `tier1/mrlore/mrlore_proposed_claim_shape_gate.py`
  - `tier1/mrlore/mrlore_quality_aware_queue_summary.py`
  - `tier1/mrlore/mrlore_quality_aware_review_queue_builder.py`
  - `tier1/mrlore/mrlore_review_queue_builder.py`
  - `tier1/mrlore/mrlore_review_queue_clean_view.py`
  - `tier1/mrlore/mrlore_review_queue_noise_audit.py`
  - `tier1/mrlore/mrlore_revision_breathing_map.py`
  - `tier1/mrlore/mrlore_revision_breathing_map_guidance_gate.py`

### Static Route from entrypoint: `tier1/mrlore/mrlore_revision_breathing_map.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `tier1/mrlore/mrlore_revision_breathing_map.py`

### Static Route from entrypoint: `tier1/mrlore/mrlore_revision_breathing_map_guidance_gate.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `tier1/mrlore/mrlore_revision_breathing_map_guidance_gate.py`

### Static Route from entrypoint: `tier1/mrlore/mrlore_scene_intake_runner.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `tier1/mrlore/mrlore_scene_intake_runner.py`

### Static Route from entrypoint: `tier1/mrlore/mrlore_temporal_aware_queue_summary.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `tier1/mrlore/mrlore_temporal_aware_queue_summary.py`

### Static Route from entrypoint: `tier1/mrlore/mrlore_temporal_aware_review_by_chapter_view.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `tier1/mrlore/mrlore_temporal_aware_review_by_chapter_view.py`

### Static Route from entrypoint: `tier1/mrlore/mrlore_temporal_aware_review_queue_builder.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `tier1/mrlore/mrlore_temporal_aware_review_queue_builder.py`

### Static Route from entrypoint: `tier1/mrlore/mrlore_temporal_claim_context_enrichment.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `tier1/mrlore/mrlore_temporal_claim_context_enrichment.py`

### Static Route from entrypoint: `tier1/mrlore/mrlore_temporal_collision_classification.py`
- **Advisory Next File to Inspect in Route:** `tier1/mrlore/mrlore_predicate_collision_policy_registry_gate.py`
- **Dependency Traversal Flow:**
  - `tier1/mrlore/mrlore_temporal_collision_classification.py`
  - `tier1/mrlore/mrlore_predicate_collision_policy_registry_gate.py`

### Static Route from entrypoint: `tier1/mrlore/tools/mrlore_full_output_dump.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `tier1/mrlore/tools/mrlore_full_output_dump.py`

### Static Route from entrypoint: `tier1/paradox_machine/proofs/export_gate_triad_result_zw.py`
- **Advisory Next File to Inspect in Route:** `tier1/paradox_machine/zwcodecs/json_to_zw.py`
- **Dependency Traversal Flow:**
  - `tier1/paradox_machine/proofs/export_gate_triad_result_zw.py`
  - `tier1/paradox_machine/zwcodecs/json_to_zw.py` ➔ **Inferred Boundary Crossing:** (Proofs Subsystem ➔ Zwcodecs Subsystem)

### Static Route from entrypoint: `tier1/paradox_machine/proofs/proof_007_temporal_mvp.py`
- **Advisory Next File to Inspect in Route:** `tier1/paradox_machine/schemas/temporal_artifact.py`
- **Dependency Traversal Flow:**
  - `tier1/paradox_machine/proofs/proof_007_temporal_mvp.py`
  - `tier1/paradox_machine/extraction/naive_temporal_extractor.py` ➔ **Inferred Boundary Crossing:** (Proofs Subsystem ➔ Extraction Subsystem)
  - `tier1/paradox_machine/schemas/temporal_artifact.py` ➔ **Inferred Boundary Crossing:** (Extraction Subsystem ➔ Schemas Subsystem)
  - `tier1/paradox_machine/gates/temporal_gate.py` ➔ **Inferred Boundary Crossing:** (Proofs Subsystem ➔ Gates Subsystem)
  - `tier1/paradox_machine/reasoning/temporal_validator.py` ➔ **Inferred Boundary Crossing:** (Gates Subsystem ➔ Reasoning Subsystem)
  - `tier1/paradox_machine/reasoning/allen_relations.py`

### Static Route from entrypoint: `tier1/paradox_machine/proofs/proof_007b_temporal_rejection.py`
- **Advisory Next File to Inspect in Route:** `tier1/paradox_machine/schemas/temporal_artifact.py`
- **Dependency Traversal Flow:**
  - `tier1/paradox_machine/proofs/proof_007b_temporal_rejection.py`
  - `tier1/paradox_machine/gates/temporal_gate.py` ➔ **Inferred Boundary Crossing:** (Proofs Subsystem ➔ Gates Subsystem)
  - `tier1/paradox_machine/reasoning/temporal_validator.py` ➔ **Inferred Boundary Crossing:** (Gates Subsystem ➔ Reasoning Subsystem)
  - `tier1/paradox_machine/reasoning/allen_relations.py`
  - `tier1/paradox_machine/schemas/temporal_artifact.py` ➔ **Inferred Boundary Crossing:** (Reasoning Subsystem ➔ Schemas Subsystem)

### Static Route from entrypoint: `tier1/paradox_machine/proofs/proof_008_spatiotemporal_gate_stub.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `tier1/paradox_machine/proofs/proof_008_spatiotemporal_gate_stub.py`

### Static Route from entrypoint: `tier1/paradox_machine/proofs/read_paradox_machine_gate_triad_result.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `tier1/paradox_machine/proofs/read_paradox_machine_gate_triad_result.py`

### Static Route from entrypoint: `tier1/paradox_machine/proofs/run_paradox_machine_gate_triad.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `tier1/paradox_machine/proofs/run_paradox_machine_gate_triad.py`

### Static Route from entrypoint: `tier2/engionality/controlroom/bootstrap.py`
- **Advisory Next File to Inspect in Route:** `tier2/engionality/controlroom/task_types.py`
- **Dependency Traversal Flow:**
  - `tier2/engionality/controlroom/bootstrap.py`
  - `tier2/engionality/controlroom/runtime_loop.py`
  - `tier2/engionality/controlroom/task_types.py`
  - `tier2/engionality/showroom/domain_views.py` ➔ **Inferred Boundary Crossing:** (Controlroom Subsystem ➔ Showroom Subsystem)
  - `tier2/engionality/showroom/performer_engine.py` ➔ **Inferred Boundary Crossing:** (Controlroom Subsystem ➔ Showroom Subsystem)
  - `tier2/engionality/showroom/animation_engine.py`
  - `tier2/engionality/showroom/scene_track.py`
  - `tier2/engionality/showroom/audio_engine.py`
  - `tier2/engionality/showroom/dialogue_engine.py`
  - `tier2/engionality/controlroom/zon4d_kernel.py`

### Static Route from entrypoint: `tier2/engionality/controlroom/performance_harness.py`
- **Advisory Next File to Inspect in Route:** `tier2/engionality/controlroom/task_types.py`
- **Dependency Traversal Flow:**
  - `tier2/engionality/controlroom/performance_harness.py`
  - `tier2/engionality/showroom/performer_engine.py` ➔ **Inferred Boundary Crossing:** (Controlroom Subsystem ➔ Showroom Subsystem)
  - `tier2/engionality/controlroom/task_types.py` ➔ **Inferred Boundary Crossing:** (Showroom Subsystem ➔ Controlroom Subsystem)
  - `tier2/engionality/showroom/animation_engine.py`
  - `tier2/engionality/showroom/scene_track.py`
  - `tier2/engionality/showroom/audio_engine.py`
  - `tier2/engionality/showroom/dialogue_engine.py`

### Static Route from entrypoint: `tier2/engionality/controlroom/zon4d_kernel.py`
- **Advisory Next File to Inspect in Route:** `tier2/engionality/controlroom/task_types.py`
- **Dependency Traversal Flow:**
  - `tier2/engionality/controlroom/zon4d_kernel.py`
  - `tier2/engionality/controlroom/runtime_loop.py`
  - `tier2/engionality/controlroom/task_types.py`
  - `tier2/engionality/showroom/domain_views.py` ➔ **Inferred Boundary Crossing:** (Controlroom Subsystem ➔ Showroom Subsystem)
  - `tier2/engionality/showroom/performer_engine.py` ➔ **Inferred Boundary Crossing:** (Controlroom Subsystem ➔ Showroom Subsystem)
  - `tier2/engionality/showroom/animation_engine.py`
  - `tier2/engionality/showroom/scene_track.py`
  - `tier2/engionality/showroom/audio_engine.py`
  - `tier2/engionality/showroom/dialogue_engine.py`

### Static Route from entrypoint: `tier2/engionality/engionality_control_center.py`
- **Advisory Next File to Inspect in Route:** `tier2/engionality/gates/gate_affect_state_valid.py`
- **Dependency Traversal Flow:**
  - `tier2/engionality/engionality_control_center.py`
  - `tier2/engionality/gates/gate_affect_state_valid.py` ➔ **Inferred Boundary Crossing:** (Engionality Subsystem ➔ Gates Subsystem)
  - `tier2/engionality/gates/gate_intensity_bounds.py` ➔ **Inferred Boundary Crossing:** (Engionality Subsystem ➔ Gates Subsystem)
  - `tier2/engionality/gates/gate_no_lane_theft_in_packet.py` ➔ **Inferred Boundary Crossing:** (Engionality Subsystem ➔ Gates Subsystem)
  - `tier2/engionality/gates/gate_relationship_deltas_valid_if_present.py` ➔ **Inferred Boundary Crossing:** (Engionality Subsystem ➔ Gates Subsystem)
  - `tier2/engionality/gates/gate_required_fields.py` ➔ **Inferred Boundary Crossing:** (Engionality Subsystem ➔ Gates Subsystem)
  - `tier2/engionality/gates/gate_scene_mood_valid_if_present.py` ➔ **Inferred Boundary Crossing:** (Engionality Subsystem ➔ Gates Subsystem)

### Static Route from entrypoint: `tier2/godotsim/adapters/combat3d_integration.py`
- **Advisory Next File to Inspect in Route:** `tier2/godotsim/kernels/combat3d_mr.py`
- **Dependency Traversal Flow:**
  - `tier2/godotsim/adapters/combat3d_integration.py`
  - `tier2/godotsim/kernels/combat3d_mr.py` ➔ **Inferred Boundary Crossing:** (Adapters Subsystem ➔ Kernels Subsystem)

### Static Route from entrypoint: `tier2/godotsim/adapters/dialogue3d_integration.py`
- **Advisory Next File to Inspect in Route:** `tier2/godotsim/__init__.py`
- **Dependency Traversal Flow:**
  - `tier2/godotsim/adapters/dialogue3d_integration.py`
  - `tier2/godotsim/__init__.py` ➔ **Inferred Boundary Crossing:** (Adapters Subsystem ➔ Godotsim Subsystem)

### Static Route from entrypoint: `tier2/godotsim/adapters/inventory3d_integration.py`
- **Advisory Next File to Inspect in Route:** `tier2/godotsim/__init__.py`
- **Dependency Traversal Flow:**
  - `tier2/godotsim/adapters/inventory3d_integration.py`
  - `tier2/godotsim/__init__.py` ➔ **Inferred Boundary Crossing:** (Adapters Subsystem ➔ Godotsim Subsystem)

### Static Route from entrypoint: `tier2/godotsim/adapters/navigation_adapter.py`
- **Advisory Next File to Inspect in Route:** `tier2/godotsim/slice_builders.py`
- **Dependency Traversal Flow:**
  - `tier2/godotsim/adapters/navigation_adapter.py`
  - `tier2/godotsim/slice_builders.py` ➔ **Inferred Boundary Crossing:** (Adapters Subsystem ➔ Godotsim Subsystem)
  - `tier2/godotsim/slice_types.py`

### Static Route from entrypoint: `tier2/godotsim/adapters/spatial3d_adapter.py`
- **Advisory Next File to Inspect in Route:** `tier2/godotsim/__init__.py`
- **Dependency Traversal Flow:**
  - `tier2/godotsim/adapters/spatial3d_adapter.py`
  - `tier2/godotsim/__init__.py` ➔ **Inferred Boundary Crossing:** (Adapters Subsystem ➔ Godotsim Subsystem)
  - `tier2/godotsim/spatial3d.py` ➔ **Inferred Boundary Crossing:** (Adapters Subsystem ➔ Godotsim Subsystem)

### Static Route from entrypoint: `tier2/godotsim/gates/gate_floor_headless_parse_proof.py`
- **Advisory Next File to Inspect in Route:** `tier2/godotsim/kernels/piece3d_mr.py`
- **Dependency Traversal Flow:**
  - `tier2/godotsim/gates/gate_floor_headless_parse_proof.py`
  - `tier2/godotsim/kernels/piece3d_mr.py` ➔ **Inferred Boundary Crossing:** (Gates Subsystem ➔ Kernels Subsystem)

### Static Route from entrypoint: `tier2/godotsim/gates/gate_ollama_diff_patcher_tests.py`
- **Advisory Next File to Inspect in Route:** `tools/ollama_diff_patcher.py`
- **Dependency Traversal Flow:**
  - `tier2/godotsim/gates/gate_ollama_diff_patcher_tests.py`
  - `tools/ollama_diff_patcher.py` ➔ **Inferred Boundary Crossing:** (Gates Subsystem ➔ Tools Subsystem)

### Static Route from entrypoint: `tier2/godotsim/gates/gate_piece3d_baseline.py`
- **Advisory Next File to Inspect in Route:** `tier2/godotsim/kernels/piece3d_mr.py`
- **Dependency Traversal Flow:**
  - `tier2/godotsim/gates/gate_piece3d_baseline.py`
  - `tier2/godotsim/kernels/piece3d_mr.py` ➔ **Inferred Boundary Crossing:** (Gates Subsystem ➔ Kernels Subsystem)

### Static Route from entrypoint: `tier2/godotsim/gates/gate_piece_recipe_pack_001.py`
- **Advisory Next File to Inspect in Route:** `tier2/godotsim/kernels/piece3d_mr.py`
- **Dependency Traversal Flow:**
  - `tier2/godotsim/gates/gate_piece_recipe_pack_001.py`
  - `tier2/godotsim/kernels/piece3d_mr.py` ➔ **Inferred Boundary Crossing:** (Gates Subsystem ➔ Kernels Subsystem)

### Static Route from entrypoint: `tier2/godotsim/gates/gate_piece_recipe_pack_001_visible_proof.py`
- **Advisory Next File to Inspect in Route:** `tier2/godotsim/builders/godot_scene_piece_builder.py`
- **Dependency Traversal Flow:**
  - `tier2/godotsim/gates/gate_piece_recipe_pack_001_visible_proof.py`
  - `tier2/godotsim/builders/godot_scene_piece_builder.py` ➔ **Inferred Boundary Crossing:** (Gates Subsystem ➔ Builders Subsystem)
  - `tier2/godotsim/kernels/piece3d_mr.py` ➔ **Inferred Boundary Crossing:** (Builders Subsystem ➔ Kernels Subsystem)

### Static Route from entrypoint: `tier2/godotsim/gates/gate_piece_recipe_pack_002_door_proof.py`
- **Advisory Next File to Inspect in Route:** `tier2/godotsim/builders/godot_scene_piece_builder.py`
- **Dependency Traversal Flow:**
  - `tier2/godotsim/gates/gate_piece_recipe_pack_002_door_proof.py`
  - `tier2/godotsim/builders/godot_scene_piece_builder.py` ➔ **Inferred Boundary Crossing:** (Gates Subsystem ➔ Builders Subsystem)
  - `tier2/godotsim/kernels/piece3d_mr.py` ➔ **Inferred Boundary Crossing:** (Builders Subsystem ➔ Kernels Subsystem)

### Static Route from entrypoint: `tier2/godotsim/gates/gate_player_body_visible_proof.py`
- **Advisory Next File to Inspect in Route:** `tier2/godotsim/builders/godot_scene_piece_builder.py`
- **Dependency Traversal Flow:**
  - `tier2/godotsim/gates/gate_player_body_visible_proof.py`
  - `tier2/godotsim/builders/godot_scene_piece_builder.py` ➔ **Inferred Boundary Crossing:** (Gates Subsystem ➔ Builders Subsystem)
  - `tier2/godotsim/kernels/piece3d_mr.py` ➔ **Inferred Boundary Crossing:** (Builders Subsystem ➔ Kernels Subsystem)

### Static Route from entrypoint: `tier2/godotsim/gates/gate_player_movement_proof.py`
- **Advisory Next File to Inspect in Route:** `tier2/godotsim/builders/godot_scene_piece_builder.py`
- **Dependency Traversal Flow:**
  - `tier2/godotsim/gates/gate_player_movement_proof.py`
  - `tier2/godotsim/builders/godot_scene_piece_builder.py` ➔ **Inferred Boundary Crossing:** (Gates Subsystem ➔ Builders Subsystem)
  - `tier2/godotsim/kernels/piece3d_mr.py` ➔ **Inferred Boundary Crossing:** (Builders Subsystem ➔ Kernels Subsystem)

### Static Route from entrypoint: `tier2/godotsim/gates/gate_player_movement_visible_observer_proof.py`
- **Advisory Next File to Inspect in Route:** `tier2/godotsim/builders/godot_scene_piece_builder.py`
- **Dependency Traversal Flow:**
  - `tier2/godotsim/gates/gate_player_movement_visible_observer_proof.py`
  - `tier2/godotsim/builders/godot_scene_piece_builder.py` ➔ **Inferred Boundary Crossing:** (Gates Subsystem ➔ Builders Subsystem)
  - `tier2/godotsim/kernels/piece3d_mr.py` ➔ **Inferred Boundary Crossing:** (Builders Subsystem ➔ Kernels Subsystem)

### Static Route from entrypoint: `tier2/godotsim/gates/gate_static_room_visible_proof.py`
- **Advisory Next File to Inspect in Route:** `tier2/godotsim/builders/godot_scene_piece_builder.py`
- **Dependency Traversal Flow:**
  - `tier2/godotsim/gates/gate_static_room_visible_proof.py`
  - `tier2/godotsim/builders/godot_scene_piece_builder.py` ➔ **Inferred Boundary Crossing:** (Gates Subsystem ➔ Builders Subsystem)
  - `tier2/godotsim/kernels/piece3d_mr.py` ➔ **Inferred Boundary Crossing:** (Builders Subsystem ➔ Kernels Subsystem)

### Static Route from entrypoint: `tier2/godotsim/gates/gate_trigger_zone_light_off_proof.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `tier2/godotsim/gates/gate_trigger_zone_light_off_proof.py`

### Static Route from entrypoint: `tier2/godotsim/gates/gate_trigger_zone_multi_trigger_light_route_proof.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `tier2/godotsim/gates/gate_trigger_zone_multi_trigger_light_route_proof.py`

### Static Route from entrypoint: `tier2/godotsim/gates/gate_visible_floor_render_proof.py`
- **Advisory Next File to Inspect in Route:** `tier2/godotsim/kernels/piece3d_mr.py`
- **Dependency Traversal Flow:**
  - `tier2/godotsim/gates/gate_visible_floor_render_proof.py`
  - `tier2/godotsim/kernels/piece3d_mr.py` ➔ **Inferred Boundary Crossing:** (Gates Subsystem ➔ Kernels Subsystem)

### Static Route from entrypoint: `tier2/godotsim/kernels/dialogue3d_mr.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `tier2/godotsim/kernels/dialogue3d_mr.py`

### Static Route from entrypoint: `tier2/godotsim/kernels/inventory3d_mr.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `tier2/godotsim/kernels/inventory3d_mr.py`

### Static Route from entrypoint: `tier2/godotsim/kernels/navigation_mr.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `tier2/godotsim/kernels/navigation_mr.py`

### Static Route from entrypoint: `tier2/godotsim/kernels/perception_mr.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `tier2/godotsim/kernels/perception_mr.py`

### Static Route from entrypoint: `tier2/godotsim/kernels/quest3d_mr.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `tier2/godotsim/kernels/quest3d_mr.py`

### Static Route from entrypoint: `tier2/godotsim/scan_old_vault_paths.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `tier2/godotsim/scan_old_vault_paths.py`

### Static Route from entrypoint: `tier2/godotsim/scene_extractor.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `tier2/godotsim/scene_extractor.py`

### Static Route from entrypoint: `tier2/godotsim/sim_runtime.py`
- **Advisory Next File to Inspect in Route:** `tier2/godotsim/bridge_integration.py`
- **Dependency Traversal Flow:**
  - `tier2/godotsim/sim_runtime.py`
  - `tier2/godotsim/bridge_integration.py` [PARSE ERROR]
  - `tier2/godotsim/environment_manager.py`
  - `tier2/godotsim/http_handlers.py`
  - `tier1/engainos/aproom/canon.py` ➔ **Inferred Boundary Crossing:** (Godotsim Subsystem ➔ Aproom Subsystem)
  - `tier1/engainos/core/intent_shadow.py` ➔ **Inferred Boundary Crossing:** (Godotsim Subsystem ➔ Core Subsystem)
  - `tier2/godotsim/command_dispatcher.py`
  - `tier2/godotsim/runtime_core.py`
  - `tier1/engainos/aproom/reality_mode.py` ➔ **Inferred Boundary Crossing:** (Godotsim Subsystem ➔ Aproom Subsystem)
  - `tier2/godotsim/adapters/behavior_adapter.py` ➔ **Inferred Boundary Crossing:** (Godotsim Subsystem ➔ Adapters Subsystem)
  - `tier2/godotsim/__init__.py` ➔ **Inferred Boundary Crossing:** (Adapters Subsystem ➔ Godotsim Subsystem)
  - `tier2/godotsim/adapters/combat3d_adapter.py` ➔ **Inferred Boundary Crossing:** (Godotsim Subsystem ➔ Adapters Subsystem)
  - `tier2/godotsim/kernels/combat3d_mr.py` ➔ **Inferred Boundary Crossing:** (Adapters Subsystem ➔ Kernels Subsystem)
  - `tier2/godotsim/adapters/dialogue3d_integration.py` ➔ **Inferred Boundary Crossing:** (Godotsim Subsystem ➔ Adapters Subsystem)
  - `tier2/godotsim/adapters/inventory3d_integration.py` ➔ **Inferred Boundary Crossing:** (Godotsim Subsystem ➔ Adapters Subsystem)
  - `tier2/godotsim/adapters/perception_adapter.py` ➔ **Inferred Boundary Crossing:** (Godotsim Subsystem ➔ Adapters Subsystem)
  - `tier2/godotsim/adapters/spatial3d_adapter.py` ➔ **Inferred Boundary Crossing:** (Godotsim Subsystem ➔ Adapters Subsystem)
  - `tier2/godotsim/spatial3d.py` ➔ **Inferred Boundary Crossing:** (Adapters Subsystem ➔ Godotsim Subsystem)
  - `tier2/godotsim/engain_hooks.py`
  - `tier2/godotsim/kernels/behavior3d_mr.py` ➔ **Inferred Boundary Crossing:** (Godotsim Subsystem ➔ Kernels Subsystem)
  - `tier2/godotsim/kernels/perception_mr.py` ➔ **Inferred Boundary Crossing:** (Godotsim Subsystem ➔ Kernels Subsystem)
  - `tier2/godotsim/kernels/spatial3d_mr.py` ➔ **Inferred Boundary Crossing:** (Godotsim Subsystem ➔ Kernels Subsystem)
  - `tier2/godotsim/protocol_envelope.py`
  - `tier2/godotsim/scene_manager.py`
  - `tier2/godotsim/scene_extractor.py`
  - `tier3/mettaext/scene_identity.py` ➔ **Inferred Boundary Crossing:** (Godotsim Subsystem ➔ Mettaext Subsystem)
  - `tier2/godotsim/slice_builders.py`
  - `tier2/godotsim/slice_types.py`
  - `tier2/godotsim/vault_linker.py`
  - `tier2/godotsim/vault_manager.py`
  - `tier2/godotsim/runtime_gateway.py`
  - `tier1/engainos/aproom/ap_complex_rules.py` ➔ **Inferred Boundary Crossing:** (Godotsim Subsystem ➔ Aproom Subsystem)
  - `tier1/engainos/aproom/ap_core.py`
  - `tier1/engainos/aproom/authority_gate.py` [STUB] ➔ **Inferred Boundary Crossing:** (Godotsim Subsystem ➔ Aproom Subsystem)

### Static Route from entrypoint: `tier2/godotsim/trixel_composer.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `tier2/godotsim/trixel_composer.py`

### Static Route from entrypoint: `tier2/godotsim/vault_linker.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `tier2/godotsim/vault_linker.py`

### Static Route from entrypoint: `tier2/topologist/classroom/run_topologist_classroom_probe.py`
- **Advisory Next File to Inspect in Route:** `tier2/topologist/reckoningroom/topology_validator.py`
- **Dependency Traversal Flow:**
  - `tier2/topologist/classroom/run_topologist_classroom_probe.py`
  - `tier2/topologist/artifactroom/topology_artifact.py` ➔ **Inferred Boundary Crossing:** (Classroom Subsystem ➔ Artifactroom Subsystem)
  - `tier2/topologist/reckoningroom/topology_validator.py` ➔ **Inferred Boundary Crossing:** (Classroom Subsystem ➔ Reckoningroom Subsystem)

### Static Route from entrypoint: `tier3/mettaext/build_scene_index.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `tier3/mettaext/build_scene_index.py`

### Static Route from entrypoint: `tier3/mettaext/chapterroom/chapterroom_index_runner.py`
- **Advisory Next File to Inspect in Route:** `tier3/mettaext/chapterroom/passA_chapter_intake.py`
- **Dependency Traversal Flow:**
  - `tier3/mettaext/chapterroom/chapterroom_index_runner.py`
  - `tier3/mettaext/chapterroom/passA_chapter_intake.py`
  - `tier3/mettaext/chapterroom/passB5_environment_detector.py`
  - `tier3/mettaext/chapterroom/passB_scene_boundary_provider.py`
  - `tier3/mettaext/chapterroom/passC_scene_packet_writer.py`

### Static Route from entrypoint: `tier3/mettaext/chapterroom/chapterroom_runner.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `tier3/mettaext/chapterroom/chapterroom_runner.py`

### Static Route from entrypoint: `tier3/mettaext/chapterroom/passA_chapter_intake.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `tier3/mettaext/chapterroom/passA_chapter_intake.py`

### Static Route from entrypoint: `tier3/mettaext/chapterroom/passB5_environment_detector.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `tier3/mettaext/chapterroom/passB5_environment_detector.py`

### Static Route from entrypoint: `tier3/mettaext/chapterroom/passB_scene_boundary_provider.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `tier3/mettaext/chapterroom/passB_scene_boundary_provider.py`

### Static Route from entrypoint: `tier3/mettaext/chapterroom/passC_scene_packet_writer.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `tier3/mettaext/chapterroom/passC_scene_packet_writer.py`

### Static Route from entrypoint: `tier3/mettaext/engain_ingest.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `tier3/mettaext/engain_ingest.py`

### Static Route from entrypoint: `tier3/mettaext/master_pipeline.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `tier3/mettaext/master_pipeline.py`

### Static Route from entrypoint: `tier3/mettaext/narrative_to_game.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `tier3/mettaext/narrative_to_game.py`

### Static Route from entrypoint: `tier3/mettaext/passroom/pass1_explicit.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `tier3/mettaext/passroom/pass1_explicit.py`

### Static Route from entrypoint: `tier3/mettaext/passroom/pass1_spatial.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `tier3/mettaext/passroom/pass1_spatial.py`

### Static Route from entrypoint: `tier3/mettaext/passroom/pass2_enhanced.py`
- **Advisory Next File to Inspect in Route:** `tier3/mettaext/world_rules_loader.py`
- **Dependency Traversal Flow:**
  - `tier3/mettaext/passroom/pass2_enhanced.py`
  - `tier3/mettaext/passroom/pass2_entity_filter.py`
  - `tier3/mettaext/world_rules_loader.py` ➔ **Inferred Boundary Crossing:** (Passroom Subsystem ➔ Mettaext Subsystem)

### Static Route from entrypoint: `tier3/mettaext/passroom/pass2_event_builder.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `tier3/mettaext/passroom/pass2_event_builder.py`

### Static Route from entrypoint: `tier3/mettaext/passroom/pass3_merge.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `tier3/mettaext/passroom/pass3_merge.py`

### Static Route from entrypoint: `tier3/mettaext/passroom/pass4_zon_bridge.py`
- **Advisory Next File to Inspect in Route:** `tier3/mettaext/semantic_environment_extractor.py`
- **Dependency Traversal Flow:**
  - `tier3/mettaext/passroom/pass4_zon_bridge.py`
  - `tier3/mettaext/semantic_environment_extractor.py` ➔ **Inferred Boundary Crossing:** (Passroom Subsystem ➔ Mettaext Subsystem)

### Static Route from entrypoint: `tier3/mettaext/passroom/pass5_game_bridge.py`
- **Advisory Next File to Inspect in Route:** `tier3/mettaext/semantic_environment_extractor.py`
- **Dependency Traversal Flow:**
  - `tier3/mettaext/passroom/pass5_game_bridge.py`
  - `tier3/mettaext/semantic_environment_extractor.py` ➔ **Inferred Boundary Crossing:** (Passroom Subsystem ➔ Mettaext Subsystem)

### Static Route from entrypoint: `tier3/mettaext/pipeline_runner.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `tier3/mettaext/pipeline_runner.py`

### Static Route from entrypoint: `tier3/mettaext/run1time.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `tier3/mettaext/run1time.py`

### Static Route from entrypoint: `tier3/mettaext/segmenter.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `tier3/mettaext/segmenter.py`

### Static Route from entrypoint: `tier3/mettaext/semantic_environment_extractor.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `tier3/mettaext/semantic_environment_extractor.py`

### Static Route from entrypoint: `tier3/mettaext/stageroom_manifest.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `tier3/mettaext/stageroom_manifest.py`

### Static Route from entrypoint: `tier3/mettaext/vaultroom/vault_source_index.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `tier3/mettaext/vaultroom/vault_source_index.py`

### Static Route from entrypoint: `tier3/mettaext/world_rules_loader.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `tier3/mettaext/world_rules_loader.py`

### Static Route from entrypoint: `tier3/mettaext/zw_compiler.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `tier3/mettaext/zw_compiler.py`

### Static Route from entrypoint: `tier3/mettaext/zw_world_rules_compiler.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `tier3/mettaext/zw_world_rules_compiler.py`

### Static Route from entrypoint: `tier3/mettaext/zwify_python.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `tier3/mettaext/zwify_python.py`

### Static Route from entrypoint: `tools/gameproof/run_gameproof_001.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `tools/gameproof/run_gameproof_001.py`

### Static Route from entrypoint: `tools/gameproof/run_gameproof_002.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `tools/gameproof/run_gameproof_002.py`

### Static Route from entrypoint: `tools/gameproof/run_gameproof_003.py`
- **Advisory Next File to Inspect in Route:** `tier3/mettaext/chapterroom/chapterroom_bridge.py`
- **Dependency Traversal Flow:**
  - `tools/gameproof/run_gameproof_003.py`
  - `tier3/mettaext/chapterroom/chapterroom_bridge.py` ➔ **Inferred Boundary Crossing:** (Gameproof Subsystem ➔ Chapterroom Subsystem)
  - `tier3/mettaext/chapterroom/passA_chapter_intake.py`
  - `tier3/mettaext/chapterroom/passB_scene_boundary_provider.py`
  - `tier3/mettaext/chapterroom/passC_scene_packet_writer.py`

### Static Route from entrypoint: `tools/gameproof/run_gameproof_004.py`
- **Advisory Next File to Inspect in Route:** `tier3/mettaext/passroom/passroom_bridge.py`
- **Dependency Traversal Flow:**
  - `tools/gameproof/run_gameproof_004.py`
  - `tier3/mettaext/passroom/passroom_bridge.py` ➔ **Inferred Boundary Crossing:** (Gameproof Subsystem ➔ Passroom Subsystem)
  - `tier3/mettaext/passroom/pass1_explicit.py`

### Static Route from entrypoint: `tools/gameproof/run_gameproof_005.py`
- **Advisory Next File to Inspect in Route:** `tier3/mettaext/passroom/passroom_bridge.py`
- **Dependency Traversal Flow:**
  - `tools/gameproof/run_gameproof_005.py`
  - `tier3/mettaext/passroom/pass1_spatial.py` ➔ **Inferred Boundary Crossing:** (Gameproof Subsystem ➔ Passroom Subsystem)
  - `tier3/mettaext/passroom/passroom_bridge.py` ➔ **Inferred Boundary Crossing:** (Gameproof Subsystem ➔ Passroom Subsystem)
  - `tier3/mettaext/passroom/pass1_explicit.py`

### Static Route from entrypoint: `tools/gameproof/run_gameproof_006.py`
- **Advisory Next File to Inspect in Route:** `tier2/topologist/gates/gate_accept_proposed_topology_artifact.py`
- **Dependency Traversal Flow:**
  - `tools/gameproof/run_gameproof_006.py`
  - `tier2/topologist/gates/gate_accept_proposed_topology_artifact.py` ➔ **Inferred Boundary Crossing:** (Gameproof Subsystem ➔ Gates Subsystem)

### Static Route from entrypoint: `tools/ollama_diff_patcher.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `tools/ollama_diff_patcher.py`

### Static Route from entrypoint: `tools/passB_fix/passB_day_boundary_runner.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `tools/passB_fix/passB_day_boundary_runner.py`

### Static Route from entrypoint: `tools/retired/ollama_patcher.py`
- **Advisory Next File to Inspect in Route:** `None`
- **Dependency Traversal Flow:**
  - `tools/retired/ollama_patcher.py`

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
