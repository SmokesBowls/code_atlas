# Evidence index

This directory contains curated proof artifacts, not routine scanner output.

## Current proof sets

- `unique_suffix_local_import_resolution_v1_final_20260712T011901Z/` — final unique-suffix import-resolution run, log, and checksums.
- `payload_resolution_path_parity_v1_20260712T014913Z/` — payload resolution parity characterization.
- `role_signals_exact_cli_20260712T031004Z/` — exact role-signal and CLI-token measurements.
- `coordinator_singleton_policy_20260712T031419Z/` — coordinator concentration and singleton utility policy scan.
- `effect_trixel_validation_20260712T124653Z/` — final route-qualified EFFECT/Trixel validation scan.
- `effect_assembly_inventory_v1.md` — contract-to-implementation inventory for EFFECT assembly.
- `legacy_root_reports/` — preserved reports that predate the evidence naming policy; retained for historical comparison, not current authority.

## Admission rule

A new evidence set should be:

1. final rather than an intermediate retry;
2. named for the contract or decision it proves;
3. reproducible from a documented command;
4. accompanied by checksums or raw test output when the proof depends on byte identity;
5. superseded explicitly when a later run replaces it.

Routine and exploratory scans belong in `artifacts/`, which is ignored by Git.
