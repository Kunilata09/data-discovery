# UC2 independent reuse check report

Scope: README section 9 "Reuse check" and the skill's Steps 0 to 2b for UC2, run in a scratch copy. Step 3 onward (profiling, rules, assess, memo) was not run, because no dataset link was accepted (README: "If none survives your check, record 'none accepted' and stop").

**Scratch copy:** /tmp/uc2_reuse_scratch. Created with `tar` from the project, excluding `outputs/UC1`, `outputs/UC2`, `outputs/artifacts`, `.venv`, `.cache`, `.git`, `.env`, and the project's local `.claude` settings. Only `.claude/skills/data-discovery-agent/` was kept.

## Independence caveat (read first)

This check is **not a clean fresh-session test**. It was run by the same assistant that built the project, with these inputs in context:
- the project `CLAUDE.md`, which loads automatically;
- the full `README.md`, which contains draft answers to the reuse-check questions written from an earlier same-session run;
- the skill files.

The README's draft answers may have shaped what I looked for. The README's own test requires a session that has only the skill and the README. That test still needs to be run, by a session that has not seen the earlier draft answers. Treat this report as evidence that the steps are executable, not as the independent sign-off.

## Result

| Item | Result |
|---|---|
| Step 0 setup, tests and tool smoke | Passed (86 tests; 3 smoke tests returned JSON) |
| Step 1 use-case validation | Technically passed (`UC2: OK`). Not separately reviewed or confirmed by the learner. The learner confirmed the needs table (needs, priorities, grains, windows), and the contract was not changed |
| Step 2 plan and scout | Passed (exit 0) |
| Step 2 gate question (dataset links) | Learner: no links. `links.json` = `[]` |
| Step 2b search | Ran (2 queries, exit 0). Results unusable as publisher sources |
| Step 2b decisions | Learner rejected all N5 leads; no N2 source accepted |
| Steps 3 to 5 | Not run, because none accepted (as the README directs) |
| Overall independent check | **Not passed as an independent check.** Steps 0 to 2b ran, but the test is not independent (see caveat), and two instruction gaps were found (below) |

## Commands executed (scratch copy unless stated)

Read-only, original project:
- `ls -la`, `ls scripts/ outputs/ outputs/artifacts/ use_cases/ internal/ links/ config/`; `du`; `git status`; `git log`
- Env presence check: `python3 -c "...bool(os.environ.get(k))..."` (names only, values not printed)
- `find ... -newermt "2026-11-15 16:20"` (to confirm no original file changed)
- `grep` on `use_cases/UC2_ice_cream.md`; `diff` of the register against scratch

Scratch setup:
- `tar ... -cf - . | tar -xf - -C /tmp/uc2_reuse_scratch` with excludes; `cp -r` of the skill directory
- `python3 -m venv .venv`; `pip install -q -r requirements.txt` (anthropic 1.17.0, jsonschema 4.26.0, pytest 9.2.0)

Step 0:
- `python -m pytest tests/ -q` -> 86 passed
- Per file: `tests/test_tools_offline.py` 24 passed; `tests/test_agent_loop.py` 7 passed; `tests/test_learner_gaps.py` 21 passed; `tests/test_g7_regressions.py` 18 passed; `tests/test_g7_scope_and_completeness.py` 16 passed
- `python -m discovery_agent tool search_internal_catalog '{"query": "ice cream sales daily"}' --use-case UC2` (exit 0)
- `python -m discovery_agent tool inspect_dataset_link '{"url": "https://archive.ics.uci.edu/dataset/360/air+quality"}' --use-case UC2` (exit 0; this made one real GET to archive.ics.uci.edu, which the allowlist permitted)
- `python -m discovery_agent tool list_external_register '{}' --use-case UC2` (exit 0)

Step 1:
- `python -m discovery_agent validate-use-case UC2 > outputs/UC2/use_case_validation.txt` -> `UC2: OK`
- Read the UC2 contract needs and windows (python, read-only on the contract)

Step 2:
- `python -m discovery_agent run --use-case UC2 --stop-after scout --no-input` (exit 0; 8 LLM calls, 21 tool calls, 0 tool errors, 0 HTTP requests, 0 refusals)
- Inspection of `candidates.json`, `search_plan.json`, `trace.jsonl`, `run_summary.json` (python)

Step 2b:
- `python scripts/web_search.py "public dataset of local events calendar for Milan, daily, 2023-2026, open data licence"` (exit 0; 12 citation URLs)
- `python scripts/web_search.py "open dataset mapping of gelato or ice cream product codes before and after a 2024 product code change, Italy"` (exit 0; 7 citation URLs)
- No inspection of any suggestion, since all were rejected or not accepted

Writes (scratch only):
- `outputs/artifacts/step0_checks.md`, `outputs/artifacts/uc2_reuse_check_progress.md`, `outputs/artifacts/decisions.md`
- `outputs/UC2/links.json` = `[]`

Not run: `python -m discovery_agent check UC2` (Step 5, after profiling, so not applicable); any profile, assess or memo stage.

## Step 2 coverage (from `candidates.json`)

| Need | Candidates | Status |
|---|---|---|
| N1 daily sales by product | internal.sales.daily_by_product, internal.sales.products | covered internally |
| N2 product-code mapping (pre/post 2024) | internal.sales.products only | **unmet** (no mapping exists; `product_codes_2024` wiki page) |
| N3 daily max temperature | api.open_meteo_archive | one candidate; register configures hourly `temperature_2m`, not a daily max; coordinates are a placeholder |
| N4 public holidays | internal.store.calendar, api.nager_public_holidays | covered |
| N5 opening days and events | internal.store.calendar | one candidate; no local-events source; the hint was rejected by the learner |

Scout review: `product_codes_2024` and `till_migration_2024` were read. The calendar entry has no wiki backlinks. I did not verify whether any internal search returned nothing. My trace parser reported zero hits for every search, which is a parser artefact, not a finding.

## Step 2b decisions (learner)

- **N5, query 1:** reject all. Reason (learner, verbatim): "The search results only provided unverified redirect citations, and no publisher dataset pages, coverage or licences were verified. Do not add any of these sources to links.json."
- **N2, query 2:** no source accepted; N2 stays unresolved. Reason (learner, verbatim): "I agree that the ISTAT ATECO/PRODCOM results do not satisfy the requirement for the shop's old-to-new product-code mapping. No external source is accepted. Keep N2 unresolved."
- **Dataset links:** none for UC2. `links.json` = `[]`.
- **Weather city:** Milan as proxy; register coordinates unchanged (45.4642, 9.19). Reason (learner, verbatim): "I chose Milan as a practical proxy because the UC2 brief specifies Italy but does not identify the shop's city. The existing register coordinates are already in the Milan area. I understand that the weather results are illustrative and must be replaced with the actual shop location when it becomes available."

All of the above is recorded in `outputs/artifacts/decisions.md` in the scratch copy.

## Findings: what worked

- Steps 0 and 1 ran as written. The tests and smoke checks passed, and validation returned `UC2: OK`. That validation result is technical only: the learner confirmed the needs table, but did not separately review or confirm the validation output.
- Step 2 produced a usable candidate list, with a clear unmet-needs field and planner hints. The scout's wiki reads and the calendar's missing backlinks were visible in the output.
- The guardrails behaved correctly. No host was refused in the UC2 run, and no link was added without a decision.

## Findings: what failed or was unclear

1. **Step 2b cannot produce a publisher page from the script's output.** The citations are Google grounding redirect URLs (`vertexaisearch.cloud.google.com/grounding-api-redirect/...`), not publisher pages. The skill requires an exact dataset URL and a coverage quote, but gives no way to get one without following the redirect. Following it was not done, since the redirect target is not on the allowlist. **Gap:** the skill needs a defined resolution step (for example, the learner opens the citation and supplies the publisher URL), or the script needs to return publisher URLs.
2. **Step 0 item 3 is stale for this project state.** It says `tests/test_learner_gaps.py` is "expected to fail" until G1–G6 are done. In this copy it passes (21 of 21). A fresh session would see a mismatch and not know whether to report a failure. **Gap:** the instruction should say "expected to fail before G1–G6; must pass after".
3. **Step 0 item 4 example is UC1-specific.** The smoke test for `inspect_dataset_link` uses the UCI air-quality link, which is a UC1 link. For UC2 I used it anyway, because the step lists it. This made one real HTTP request. **Gap:** the example should be use-case neutral, or UC2 should have its own smoke link.
4. **Step 1 "pause" is ambiguous.** It says "Pause (for a human learner in an interactive session; in a non-interactive run, write the table and stop)". In a session with the learner present, it is unclear whether to wait for confirmation or proceed. I waited. **Gap:** the instruction should say which applies when the learner is in the session.
5. **The contract does not contain "acceptance criteria" or "required variables".** The planner produces per-need acceptance criteria, and they look reasonable, but they are not in the contract, so they are not checked against any input. A new session could mistake them for the learner's requirements. **Gap:** the skill should say that planner criteria are proposals to review, not contract data.
6. **The N2 need cannot be met from the register or the public web for this client.** This is a finding, not a skill defect: the old-to-new product-code mapping is the shop's internal knowledge. The skill's Step 2b assumes external search can fill unmet needs. It should say that a need which depends on internal knowledge may stay unresolved.

## What the README's reuse-check questions look like from this run

These are the learner's to confirm. I have not written the learner-only answers.

- *Steps that could not be followed as written:* Step 2b (no publisher URL from the citations; see finding 1), and Step 0 item 3 (stale expectation; finding 2).
- *Inputs a data scientist would replace:* the use-case contract, the brief, the internal catalog and wiki, the register coordinates for the shop's city, and the dataset links. The run also showed that the register's Open-Meteo coordinates are a placeholder that must be replaced by the actual shop location.
- *Hard-coded values:* **not established.** No code-level audit was performed, so the absence of hard-coded UC2 values in `discovery_agent/` is not confirmed. This run's outputs showed none, but that does not check the code. The Open-Meteo coordinates are in the register file, not in code; this was observed in the register, and no code search was done.

## Unresolved items

1. **N2 unresolved.** No external source; the internal product-code mapping is not in the catalog or wiki.
2. **N3 weather coordinates are a proxy.** The shop's actual city is not known. The weather results are illustrative until replaced.
3. **N3 daily-max variable not configured.** The register configures hourly `temperature_2m`; a daily maximum must be derived. Not done (no profiling run).
4. **N5 events unresolved.** All local-events leads were rejected; no event source exists.
5. **Step 3 to 5 not run.** No link was accepted, so profiling, rules, assess, memo and `check UC2` were not run for this check.
6. **Independent fresh-session run still needed.** See the caveat above.
7. **Learner-only README answers** (ownership, review time, reuse-check answers) are not written here.

## Files created or modified

Scratch copy only (`/tmp/uc2_reuse_scratch`):
- Created: `.venv/`, `outputs/UC2/use_case_validation.txt`, `outputs/UC2/candidates.json`, `outputs/UC2/search_plan.json`, `outputs/UC2/trace.jsonl`, `outputs/UC2/transcripts/`, `outputs/UC2/run_summary.json`, `outputs/UC2/run_history.jsonl`, `outputs/UC2/links.json` (`[]`), `outputs/artifacts/step0_checks.md`, `outputs/artifacts/uc2_reuse_check_progress.md`, `outputs/artifacts/decisions.md`, `outputs/artifacts/uc2_independent_reuse_check_report.md` (this report)
- Temporary, outside the scratch copy: `/tmp/uc2_smoke_*.txt`, `/tmp/uc2_websearch_*.txt`, `/tmp/uc2_step2_run.log`

Original project: this report is the only file to be copied in. Nothing else was created or changed. I checked for modifications with `find -newermt "2026-11-15 16:20"` and found none.

Not touched: `outputs/UC1/`, `outputs/UC2/`, `outputs/artifacts/g7_*`, existing reviews, check files, signoffs, the project's `decisions.md`, `walkthrough.md`, and `config/` (the register is identical to the original).

No ZIP, commit, push or PR was created.
