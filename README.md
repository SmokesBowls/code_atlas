# Code Atlas

Code Atlas is a local, static architecture scanner for Python repositories. It turns source structure into a report you can inspect as JSON, read as Markdown, hand to an AI assistant, or browse through the included web viewer.

It is built for repositories where the hard question is not "how many files are here?" but "what actually connects to what?"

Code Atlas maps:

- Python files, imports, entry points, and parse failures
- resolved local dependency edges and route chains
- subsystem candidates with confidence and structural-ambiguity evidence
- payload producers, consumers, unresolved routes, and handoffs
- consumer access modes such as required, defaulted, guarded, and implicit `None`
- field outcomes such as effective, stranded, dropped, and unclassified
- explicit output-construction influence without executing the target project

## Why Code Atlas exists

Large or recovered repositories tend to accumulate several versions of the truth: directory names, architecture notes, imports, launch scripts, generated artifacts, and remembered intent. A normal file tree cannot tell you which of those still agree.

Code Atlas provides a reproducible static evidence layer. Its reports are meant to support inspection and cleanup decisions, not make those decisions on their own.

The scanner is conservative around identity:

- local dependency resolution prefers exact paths, then unique suffix matches;
- ambiguous suffix matches remain unresolved;
- payload handoffs reuse reporter-resolved dependency targets;
- multiple possible providers are refused rather than selected by iteration order;
- unknown calls stop field-effect classification instead of being guessed through.

## Requirements

- Python 3.9 or newer (`ast.unparse` is required)
- A local checkout of the repository you want to inspect

Code Atlas currently uses the Python standard library. There is no package installation step.

## Quick start

From the repository root:

```bash
python3 code_atlas/scanner.py \
  --dir /path/to/python/project \
  --output artifacts/project.json
```

This creates:

```text
artifacts/project.json
artifacts/project.md
```

`artifacts/` is ignored by Git and is the right place for exploratory scans.

To open the report in the local viewer:

```bash
python3 -m code_atlas.viewer.server \
  --report artifacts/project.json \
  --port 8080
```

Then open:

```text
http://127.0.0.1:8080/
```

The viewer is read-only and serves the selected report plus its companion Markdown and AI export files when they exist.

## Interactive launcher

The launcher walks through target selection, report naming, optional AI exports, scanning, and viewer startup:

```bash
./start_atlas.sh
```

By default it writes reports under `artifacts/`. Existing names are not overwritten; the launcher adds `_s2`, `_s3`, and so on.

## Command-line reference

### Scanner

```text
python3 code_atlas/scanner.py [options]

--dir DIR
    Directory to scan. Defaults to the current directory.

--output PATH
    Main JSON report path. A Markdown report is written beside it.

--ai-output PATH
    Optional AI-oriented Markdown packet.

--ai-json-output PATH
    Optional AI-oriented JSON packet.

--ai-detail {compact,standard,full}
    AI packet detail level. Defaults to standard.
```

Example with both AI exports:

```bash
python3 code_atlas/scanner.py \
  --dir /path/to/project \
  --output artifacts/project.json \
  --ai-output artifacts/project.ai.md \
  --ai-json-output artifacts/project.ai.json \
  --ai-detail standard
```

AI exports are opt-in. The normal JSON and Markdown reports do not depend on them.

### Viewer

```text
python3 -m code_atlas.viewer.server [options]

--report PATH
    Code Atlas JSON report to load.

--port PORT
    Local HTTP port.
```

The viewer validates the report at startup and does not expose arbitrary filesystem paths or directory listings.

## What is in a report

The main JSON report contains these top-level sections:

```text
project_name
scanned_at
scan_roots
analysis_boundary
limitations
next_files_to_inspect
candidate_subsystem_groups
routes
files
local_dependencies
parse_errors
payload_handoffs
unresolved_payload_routes
```

### Files and roles

Each Python file records structural facts such as imports, functions, classes, entry-point signals, inbound references, and a primary role hint.

Role evidence is preserved separately from the selected role. A runnable file under `tools/`, for example, can retain both CLI and utility signals even though `role_hint` must choose one label.

### Local dependencies and routes

Imports are resolved against files inside the scan boundary. Exact root-relative matches have priority. A suffix match is accepted only when it identifies one file.

Resolved edges feed route construction and payload analysis. Unresolved and ambiguous imports remain visible in the report.

### Subsystem candidates

Code Atlas groups files into candidate subsystems and records why each group exists. Confidence is evidence-based, and groups can be marked structurally ambiguous.

Current bounded policies include:

- directory ownership as the default grouping basis;
- shared utility consolidation only when at least two utilities independently qualify;
- toolbox cohesion only with utility evidence and multiple external consumers;
- coordinator cohesion only for an explicitly named `*_control_center.py` that emits at least three outbound edges and accounts for at least two-thirds of its group's outbound traffic.

These are classification aids, not claims about runtime ownership or canon.

### Payload handoffs

Payload analysis separates four questions:

| Dimension | Question |
| --- | --- |
| Caller supply | Did the proven caller construct and offer the field? |
| Consumer access | Does the consumer require, default, guard, or implicitly null it? |
| Effect result | Does the consumed value reach a recognized sink? |
| Diagnosis | Which side or stage needs inspection? |

Access modes are extracted from hard syntax:

```text
payload["field"]              REQUIRED
payload.get("field", value)   DEFAULTED
payload.get("field")          OPTIONAL_IMPLICIT_NONE
"field" in payload            GUARDED
```

Field-effect verdicts are:

```text
EFFECTIVE
    The field reaches an authorized sink or explicit output construction.

STRANDED
    The field is accessed but remains local or reaches only a known
    non-terminal operation.

DROPPED
    The proven caller supplies the field, but the matched consumer does
    not access it.

UNCLASSIFIED_TERMINUS
    Static evidence reaches an unknown operation and stops there.
```

Recognized sink families currently include serializer file writes, bounded state mutation, and explicit build/output construction. Network emission and process-boundary sinks remain reserved contract categories rather than implemented allowlists.

## Static-analysis boundary

Code Atlas does not run the scanned project. It does not import target modules, start applications, execute tests, inspect runtime values, or infer behavior from dynamic dispatch.

Current limits include:

- Python source only;
- syntax errors are reported but not repaired;
- dynamic imports and monkey-patching can hide real edges;
- call targets assembled through reflection may remain unresolved;
- wrapper functions can hide returned field shapes;
- construction provenance is syntactic, not semantic;
- unknown operations terminate effect tracing;
- a subsystem candidate is evidence for inspection, not proof of architectural authority.

A missing edge means "not established by this static pass," not "impossible at runtime."

## Running the tests

```bash
python3 -m unittest discover -s code_atlas/tests -v
```

The suite covers parser behavior, import resolution, route construction, role evidence, subsystem grouping, payload parity, access modes, effect verdicts, AI exports, and viewer safety.

## Repository layout

```text
code_atlas/
  scanner.py             CLI entry point
  core/                  parsing, resolution, grouping, routing, payload analysis
  tests/                 unittest suite
  viewer/                local read-only report viewer

fixture8/                maintained scanner fixture
docs/contracts/          current analysis contracts
docs/planning/           planning and ticket history
docs/history/            original briefs and build history
evidence/                curated final proof runs
artifacts/               disposable local scan output; ignored by Git
start_atlas.sh            interactive scanner and viewer launcher
```

## Evidence policy

`evidence/` is deliberately curated. It is not the default scan destination.

A committed evidence set should be final, named for the behavior it proves, reproducible from a documented command, and accompanied by raw output or checksums when byte identity matters. Intermediate retries belong under `artifacts/`.

See [`evidence/README.md`](evidence/README.md) for the current proof index and admission rules.

## Troubleshooting

### Port 8080 is already in use

If the viewer reports:

```text
Error: Failed to bind server to port 8080.
[Errno 98] Address already in use
```

another process is already listening on that port.

Inspect it:

```bash
ss -ltnp 'sport = :8080'
```

Start the viewer on another port:

```bash
python3 -m code_atlas.viewer.server \
  --report artifacts/project.json \
  --port 8081
```

Then open:

```text
http://127.0.0.1:8081/
```

If the existing process is an old Code Atlas viewer, stop it from its original terminal with `Ctrl+C`.

You can also stop the process occupying port 8080:

```bash
fuser -k 8080/tcp
```

### `ModuleNotFoundError: No module named 'code_atlas'`

Run viewer commands from the Code Atlas repository root:

```bash
cd /path/to/code_atlas_rescue

python3 -m code_atlas.viewer.server \
  --report artifacts/project.json \
  --port 8080
```

### Report file not found

Confirm that the scan completed and that the path exists:

```bash
ls -lh artifacts/
```

Then pass the exact JSON path:

```bash
python3 -m code_atlas.viewer.server \
  --report artifacts/project.json
```

The viewer loads the main `.json` report, not the `.md` or `.ai.json` export.

### `Permission denied` when running the launcher

Make the launcher executable:

```bash
chmod +x start_atlas.sh
./start_atlas.sh
```

Alternatively:

```bash
bash start_atlas.sh
```

### The viewer rejects the report

The report may be incomplete, outdated, or not a normal Code Atlas JSON report.

Regenerate it:

```bash
python3 code_atlas/scanner.py \
  --dir /path/to/python/project \
  --output artifacts/project.json
```

Then restart the viewer with the newly generated file.

### The scan reports parse failures

Parse failures do not necessarily mean Code Atlas itself failed. They indicate that one or more scanned Python files could not be parsed.

Common causes include:

* incomplete or damaged source files;
* Python syntax unsupported by the active interpreter;
* generated files that are not valid Python;
* merge-conflict markers;
* files using a non-Python format despite a `.py` extension.

Inspect the `parse_errors` section of the JSON or Markdown report. Code Atlas reports these files but does not repair them.

### Expected dependency or payload edges are missing

A missing edge means the static pass did not establish it. Check for:

* dynamic imports;
* reflection or `getattr()` dispatch;
* wrapper functions hiding returned fields;
* multiple possible provider files;
* dynamically generated dictionary keys;
* calls crossing unsupported language boundaries.

Ambiguous targets are deliberately left unresolved rather than guessed.

### A field is marked `DROPPED`, `STRANDED`, or `UNCLASSIFIED_TERMINUS`

These verdicts describe different static conditions:

```text
DROPPED
The proven caller supplies the field, but the matched consumer does not
access it.

STRANDED
The consumer accesses the field, but the value does not reach a recognized
sink or returned construction.

UNCLASSIFIED_TERMINUS
The value reaches an operation Code Atlas cannot classify safely.
```

Inspect the claim’s caller supply, access mode, traced path, sink type, and reasons before deciding which file needs repair.

### Run the verification suite

After changing Code Atlas itself:

```bash
python3 -m unittest discover -s code_atlas/tests -v
git diff --check
bash -n start_atlas.sh
```

A scanner finding is not a test failure by itself. These commands verify the Code Atlas implementation and launcher.



## Design rule

Code Atlas reports observations, confidence, and refusal boundaries separately. When the scanner cannot prove a unique route or classify a terminal operation, the report should say so plainly. A smaller honest map is more useful than a complete-looking map built from guesses.
