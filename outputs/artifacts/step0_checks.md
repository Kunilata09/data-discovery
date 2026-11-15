# Step 0: tooling check (2026-11-15)

Scope: SKILL.md Step 0, run before any model-powered stage. No agent, Planner, Scout, Profiler or Assess run was started, and no LLM call was made. The only network request was the HTTPS GET in tool check 2, to an allowlisted host.

## 1. Environment

| Item | Result |
|---|---|
| Virtual environment | `.venv/` in the project root, activated for these checks |
| Python | 3.14.4 (`requirements.txt` asks for 3.10+) |
| anthropic | 1.17.0 |
| jsonschema | 4.26.0 |
| pytest | 9.2.0 |

## 2. Gateway variables (presence only, values not shown)

| Variable | Set |
|---|---|
| `ANTHROPIC_BASE_URL` | True |
| `ANTHROPIC_AUTH_TOKEN` | True |
| `ANTHROPIC_MODEL` | True |

Model in use: **claude-haiku-5-5**. It comes from `ANTHROPIC_MODEL`, because `DISCOVERY_MODEL` is not set (`discovery_agent/llm.py`, the resolution order is DISCOVERY_MODEL, then ANTHROPIC_MODEL, then the default).

Not verified here: that the gateway accepts this model and key. That is checked by the first model call, and no model call has been made in this step. Earlier runs (outputs/UC1/run_summary.json) recorded the same model with successful planner and scout calls.

## 3. Offline tests

Command: `python -m pytest tests/ -q`. Full output saved to `outputs/artifacts/pytest_after.txt`.

| File | Result |
|---|---|
| `tests/test_tools_offline.py` | 24 passed |
| `tests/test_agent_loop.py` | 7 passed |
| `tests/test_learner_gaps.py` | 21 passed |
| `tests/test_g7_regressions.py` | 18 passed |
| `tests/test_g7_scope_and_completeness.py` | 16 passed |
| **Total** | **86 passed, 0 failed** (exit code 0) |

The Step 0 instruction expected `test_learner_gaps.py` to fail until G1–G6 were implemented. All 21 pass now. The `tests/` tree has no failing tests.

Note: `pytest_after.txt` uses the `-q` format, so it lists no per-test names. The earlier baseline, `pytest_before.txt`, is in verbose format. Both are saved in `outputs/artifacts/`.

## 4. Tool smoke tests (no LLM)

Each command was run with `python -m discovery_agent tool … --use-case UC1`.

1. `search_internal_catalog` with the query "hourly air pollutant concentrations NO2 PM2.5": returned JSON with 3 hits (`airq.station_readings`, `traffic.hourly_counts`, `counter_replacement_2024`) and no refusal.
2. `inspect_dataset_link` on `https://archive.ics.uci.edu/dataset/360/air+quality`: returned JSON. `link_type` is `uci_dataset_page`, `page_status` 200, `canonical_ref` `uci:360`, and the licence is `CC BY 4.0`, found in a link. This was an HTTPS GET to an allowlisted host.
3. `list_external_register` for UC1: returned JSON with 4 sources (`policy.open_data_links`, `api.open_meteo_archive`, `api.nager_public_holidays`, `vendor.atmosdata_pro`). The holiday API is the only one excluded for UC1 by the contract, and it is still listed here as a register entry.

Side effect: check 2 created the HTTP cache directory `.cache/http/` (4 files). It is listed in `.gitignore`, so it is excluded from the repository and the ZIP.

## 5. Use-case validation

Command: `python -m discovery_agent validate-use-case UC1`. Output saved to `outputs/UC1/use_case_validation.txt`. Result: `UC1: OK`.

## 6. Files this step did not touch

`outputs/UC1/search_plan.json`, `candidates.json` and `trace.jsonl` were checked by hash before and after the checks and are unchanged. The only new file in `outputs/UC1/` is `use_case_validation.txt`.

## 7. Never recorded here

The value of `ANTHROPIC_AUTH_TOKEN` was not read or printed. A search for its value in the project found no matching file.
