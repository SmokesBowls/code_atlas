# EFFECT_TRACE — code_atlas Contract v1

## Position in the pipeline

VOICE → HANDSHAKE → INTERPRETER → **EFFECT**

- **VOICE** — a function returns/emits a payload. *(existing)*
- **HANDSHAKE** — the payload reaches a consumer function. *(existing — `payload_handoffs`)*
- **INTERPRETER** — the consumer reads specific keys off the payload. *(existing — `utilized_keys` / `unutilized_keys`)*
- **EFFECT** *(this contract)* — of the keys INTERPRETER marks utilized, which ones go on to change something outside the process's own call graph, versus being read into a local and going nowhere.

**Non-goal, stated up front:** EFFECT does not confirm a write is ever read by anything downstream. If `trixelmap` writes `trixelcomposer_recipe.json`, that write is a complete effect on its own — trace ends there. Whether `trixelcomposer` actually opens that file is a separate, already-existing question (cross-boundary handoff / "consumer outside scan boundary"). Don't merge these two capabilities — they answer different questions, and conflating them would make EFFECT claims silently depend on a second scan succeeding.

## 1. Terminal sink taxonomy

Every sink gets a `sink_type`. Detection is framework-agnostic — no hardcoded Godot/Flask/etc. knowledge. Two tiers.

**Tier 1 — built-in, always on:**

| sink_type | Detected by |
|---|---|
| `FILE_WRITE` | value is an argument to `open(path,'w'\|'wb'\|'a').write(...)`, `json.dump`, `Path.write_text`, `Path.write_bytes`, `pickle.dump`, `yaml.dump`, `.to_csv` |
| `STATE_MUTATION` | value assigned to `self.<attr>`, a module-level name, or an index/attribute of an object that arrived as a function *parameter* (not locally constructed this call) |
| `NETWORK_EMIT` | value passed to `requests.*`, `socket.send*`, or `return`ed from a function decorated as a route/handler |
| `PROCESS_BOUNDARY` | value passed to `subprocess.run(..., input=...)`, assigned into `os.environ[...]` |

**Tier 2 — declared, per repo:**

Same spirit as the lifecycle-declaration rule that already rejects boards without labels: undeclared calls don't get guessed at, they get flagged, not silently trusted.

```json
{
  "declared_terminal_functions": [
    {"qualified_name": "trixelmap.recipe_writer.write_recipe_and_atlas", "sink_type": "FILE_WRITE"},
    {"qualified_name": "runtime.accept_for_runtime", "sink_type": "STATE_MUTATION"}
  ]
}
```

A repo with no such file still gets full Tier 1 coverage. Tier 2 exists for the terminal functions no generic pattern could ever guess — this is where "Runtime executes" plugs in. You define what Runtime means for a given repo; the tool doesn't infer it.

## 2. Known non-terminal set (built-in denylist)

Reads that resolve only to `logging.*`, `print`, `assert`, or an f-string/`.format()` passed only to one of those, do **not** count as EFFECT — even though INTERPRETER correctly marked them utilized. Otherwise every debug line makes everything look alive and this whole stage loses its point. Configurable, not hardcoded: some repos genuinely treat structured logs as a real sink (piped to something else that acts on them). Default is no; override the same way Tier 2 sinks get declared.

## 3. Field-level verdict taxonomy

| Verdict | Meaning |
|---|---|
| `EFFECTIVE` | traced path terminates in a Tier 1 or Tier 2 sink |
| `STRANDED` | utilized, but every path dead-ends in local scope or a known non-terminal call |
| `DROPPED` | never utilized at the first consumer — inherited straight from INTERPRETER, not re-derived |
| `UNCLASSIFIED_TERMINUS` | utilized, traced path reaches a call that is neither a known sink, a declared sink, nor the denylist |

`UNCLASSIFIED_TERMINUS` is the load-bearing one — `structurally_ambiguous`'s sibling. It's what keeps this honest instead of quietly rounding unknowns down into `STRANDED` (understates real effects) or up into `EFFECTIVE` (invents confidence that isn't there).

## 4. Claim schema

```json
{
  "claim_id": "effect_<file>_<field>_<n>",
  "field": "grid_size",
  "origin": {"file": "...", "function": "..."},
  "traced_path": [
    {"file": "...", "function": "...", "role": "PRODUCER"},
    {"file": "...", "function": "...", "role": "INTERPRETER", "utilized": true},
    {"file": "...", "function": "...", "role": "TERMINAL_SINK", "sink_type": "FILE_WRITE", "evidence": "json.dump(recipe, fp) — line 47"}
  ],
  "verdict": "EFFECTIVE",
  "confidence": "high",
  "claim_type": "structural",
  "reasons": ["utilized_key", "direct_arg_to_tier1_sink"]
}
```

`confidence` follows the existing scale. Tier 1/2 sink matches are `high`. `UNCLASSIFIED_TERMINUS` claims are `low` by construction — there is no honest version of "unknown" that deserves `high` confidence. Don't let a builder shortcut that later.

## 5. Hand-authored fixtures (required before any extraction testing)

**Fixture A — happy path, the case that triggered this:**

```python
# terrain_field_builder.py
def build_terrain_field(seed):
    return {
        "grid_size": compute_grid_size(seed),
        "tiles": generate_tiles(seed),
        "version": "1.0",
    }

# recipe_writer.py
def write_recipe_and_atlas(payload):
    size = payload["grid_size"]
    with open("trixelcomposer_recipe.json", "w") as fp:
        json.dump({"size": size}, fp)
```
Expected: `grid_size` → `EFFECTIVE` / `FILE_WRITE`. `tiles`, `version` → `DROPPED`.

**Fixture B — adversarial, utilized but stranded:**

```python
def write_recipe_and_atlas(payload):
    size = payload["grid_size"]
    tiles = payload["tiles"]
    logger.debug(f"tiles={len(tiles)}")
    with open("trixelcomposer_recipe.json", "w") as fp:
        json.dump({"size": size}, fp)
```
Expected: `tiles` → `STRANDED` (reaches only the denylist), **not** `DROPPED` — it was read, and that distinction has to survive in the output.

**Fixture C — adversarial, genuinely unknown:**

```python
def write_recipe_and_atlas(payload):
    size = payload["grid_size"]
    atlas_service.register(size)  # not Tier 1, not declared, not denylist
```
Expected: `size` → `UNCLASSIFIED_TERMINUS`. Not `EFFECTIVE`, not `STRANDED`. This is the fixture most likely to get quietly skipped — it's the one that actually proves the tool refuses to guess.

Antigravity's submission gets checked against all three, exactly, before it ever touches a real package.

## 6. What to expect running this against terrain first

Worth knowing before the report lands: terrain's imports are still unpathed. EFFECT tracing needs the same resolvable call graph HANDSHAKE and INTERPRETER need — so terrain will likely come back mostly `DROPPED` / `UNCLASSIFIED_TERMINUS`, for the same underlying reason it currently reads as orphaned. That result would confirm the path-repair diagnosis again, not overturn it. If terrain comes back looking healthy under EFFECT *before* the paths are fixed, treat that as a bug in the tool, not good news about terrain.

## 7. Open call — yours, not Antigravity's

Should a package's confidence score degrade under heavy `UNCLASSIFIED_TERMINUS` coverage, the way `parse_gaps` already forces a score down? Leaning yes — an untraceable effect is the same flavor of problem as unparseable code — but that's a scoring-policy decision, not an engineering one.
