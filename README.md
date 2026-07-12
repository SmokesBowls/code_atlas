# Code Atlas

Static repository analysis for entrypoints, dependencies, subsystem grouping, payload handoffs, access modes, and field-effect tracing.

## Repository layout

```text
code_atlas/   Application source and tests
fixture8/     Maintained scanner fixture
docs/         Contracts, planning notes, and historical design material
evidence/     Curated, named proof runs only
artifacts/    Disposable local scan output (Git-ignored)
```

## Run tests

```bash
python3 -m unittest discover -s code_atlas/tests -v
```

## Run a scan

Interactive launcher:

```bash
./start_atlas.sh
```

Direct scanner invocation:

```bash
python3 code_atlas/scanner.py --dir /path/to/project --output artifacts/project.json
```

The scanner writes the JSON report and a sibling Markdown report. AI exports are optional.

## Evidence policy

`evidence/` is not a general output directory. Add only final, reproducible proof sets that support a committed behavior or architectural decision. Intermediate scans belong under ignored `artifacts/` and should not be committed.
