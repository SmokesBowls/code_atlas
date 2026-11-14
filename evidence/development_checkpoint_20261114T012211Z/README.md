# Code Atlas development checkpoint evidence

Checkpoint time: 2026-11-14T01:22:11Z
Development branch: `atlas-profile-structure-slice`
Baseline before checkpoint commits: `cd96258747e638f75ce410142da1b0f039faf3c1`

This evidence set preserves the independent audit and selected pre-repair benchmark/scratchpad witnesses. It does not claim that the audited findings have been repaired.

## Files in this evidence set

- `INDEPENDENT_AUDIT.md` — independent architecture and code-quality audit of the pre-repair working tree.
- `code_atlas_pre_repair_evidence.tar.gz` — compressed, path-normalized copies of selected original artifacts.
- `code_atlas_pre_repair_evidence.tar.gz.sha256` — checksum of the archive.
- `ARCHIVE_CONTENTS.sha256` — checksum manifest for every regular file inside the archive.

The archive contains:

1. The four ignored 2026-11-11 EngAIn report artifacts that were present in the Code Atlas worktree.
2. The final selected HTTP benchmark harness, expected fixtures, result summary, and full EngAIn/devpi HTTP inventory outputs.
3. The HTTP benchmark's EngAIn expected fixture and devpi live request/server-log witnesses.
4. The draft lifecycle/profile input used for profile analysis. Its own name states that it is a draft and not approved.
5. The latest selected system-coupling report family, including JSON, Markdown, and Mermaid containment output.
6. Two byte-identical blast-radius query results, retained together as determinism evidence, plus the boundary inventory used alongside that experiment.

## Exclusions

The following were reviewed and intentionally excluded:

- virtual environments and installed packages;
- Python bytecode and `__pycache__` directories;
- package/download caches;
- temporary databases and devpi server/client state;
- credentials/authentication state;
- profiler output;
- intermediate/retry report families when a later selected result existed;
- duplicate full blast report families where the compact query outputs were the relevant evidence;
- baseline source-code copies already recoverable from Git history.

Nothing was deleted from the original scratchpad or ignored worktree locations.

## Source provenance

Original Code Atlas repository:

- path: `/mnt/data-drive/code_atlas`
- baseline HEAD: `cd96258747e638f75ce410142da1b0f039faf3c1`
- remote: `git@github.com:SmokesBowls/code_atlas.git`

EngAIn benchmark target:

- path at capture: `/home/mytruelove/Desktop/burdens_of_a_forgotten_past/EngAIn`
- HEAD at preservation: `0cb58c6462bd76056e61826b82575a7f823339b9`
- working tree was dirty: 41 porcelain entries
- SHA-256 of `git status --porcelain=v1`: `f33ebc75092380fbe37323f2d2df8a76c896a47c0ba16450aed639c4f7629c26`

The EngAIn benchmark therefore is not fully reproducible from its commit alone. The preserved result is a witness over the then-current dirty EngAIn bytes. EngAIn was read but not modified during preservation.

devpi static target:

- source remote: `https://github.com/devpi/devpi.git`
- commit: `1914bd5996cfd815c2418257b01f3a80b90704e4`
- working tree status digest: SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` (empty/clean)

## Verify the preserved archive

From this directory:

```sh
sha256sum -c code_atlas_pre_repair_evidence.tar.gz.sha256
gzip -t code_atlas_pre_repair_evidence.tar.gz
mkdir -p /tmp/code-atlas-checkpoint-verify
tar -xzf code_atlas_pre_repair_evidence.tar.gz -C /tmp/code-atlas-checkpoint-verify
(
  cd /tmp/code-atlas-checkpoint-verify/code_atlas_pre_repair_evidence
  sha256sum -c SHA256SUMS
)
```

`ARCHIVE_CONTENTS.sha256` is a copy of the archive's internal `SHA256SUMS`, allowing review without extraction.

## Reproduce Code Atlas unit and syntax validation

From the Code Atlas repository at the checkpoint commit:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s code_atlas/tests -v
bash -n start_atlas.sh
node --check code_atlas/viewer/static/app.js
git diff --check
```

## Reproduce the HTTP benchmark

The original preserved harness is `scratchpad/http_bench/bench.py` inside the archive. It expects these paths relative to the extracted scratchpad layout:

- `scratchpad/http_proto/expected.json`
- `scratchpad/devpi_test/src/devpi`
- `scratchpad/devpi_live/client_requests.jsonl`
- `scratchpad/devpi_live/server.log`

It also contains the original absolute paths for Code Atlas and EngAIn. To rerun without changing the sealed harness:

1. Extract the archive.
2. Clone devpi at commit `1914bd5996cfd815c2418257b01f3a80b90704e4` into `scratchpad/devpi_test/src/devpi`.
3. Restore Code Atlas at the checkpoint commit to `/mnt/data-drive/code_atlas`, or run a modified copy of the harness pointing at another checkout.
4. Restore the benchmark EngAIn source bytes. Commit `0cb58c6` alone is insufficient because the original tree had 41 dirty entries; exact reproduction requires the original preserved working tree.
5. From `scratchpad/http_bench`, run:

```sh
python3 -I bench.py
```

The harness writes `bench_result.json`. Compare it with the sealed result using `sha256sum` or a structural JSON diff. A rerun against a clean or later EngAIn tree is a new benchmark, not byte-for-byte reproduction of this witness.

## Reproduce profile/coupling and blast-radius scans

The archive retains the exact draft profile and selected generated report/query outputs. The scanner CLI exposes the required current-tree options:

```sh
python3 code_atlas/scanner.py \
  --dir /path/to/EngAIn \
  --output /tmp/report.json \
  --profile /path/to/engain.profile.lifecycle-draft.json \
  --mermaid-dir /tmp/mermaid \
  --boundaries-output /tmp/boundaries.json

python3 -m code_atlas.core.blast_radius \
  --report /tmp/report.json \
  --file tier2/godotsim/runtime_core.py \
  --output /tmp/runtime_core_blast.json
```

Use `python3 code_atlas/scanner.py --help` and
`python3 -m code_atlas.core.blast_radius --help` if option names change in a
later revision. Direct execution of `code_atlas/core/blast_radius.py` from the
repository root failed at this checkpoint because package imports were not on
the script path; module execution passed. Exact byte comparison requires the
same Code Atlas checkpoint and the same target source bytes.

## Authority limits

- These are producer-side preservation witnesses, not an independent acceptance verdict.
- The draft profile is not an approved statement of EngAIn architecture.
- Static scan output is not proof of runtime behavior.
- Preserved generated reports record what the pre-repair implementation emitted; they may include the defects identified in `INDEPENDENT_AUDIT.md`.
