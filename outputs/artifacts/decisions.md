# Decisions log

## Source suggestions (Step 2b)
One row per suggestion you accepted, rejected or revised, with your reason. Use the page's own wording for the reason.

| Suggestion (publisher, URL) | Need, window | Decision | Reason |
|---|---|---|---|
Search evidence for UC1 N6 production: one `scripts/web_search.py` query ("Italy national annual premature deaths attributable to PM2.5 … 2024 and 2025 … Eurostat, ISTAT, ISS or EEA"). The saved output (`/tmp/step2b_n6.txt`) contains **four** cited redirect URLs. The log below previously recorded three. Row 4 was missing and is added here. Each redirect was resolved by reading its first HTTP redirect target (no further hops followed). Each destination was then fetched with a 300 KB cap and read as plain text. Nothing was executed. Verification date: 2026-11-15.

| # | Suggestion: redirect URL (as returned) | Resolved destination (verified) | Publisher, title, type (verified) | Coverage (what the page states) | Supports N6 production 2024–2025? | Assistant recommendation (not a decision) | Learner decision |
|---|---|---|---|---|---|---|---|
| 1 | `https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQE36GI_hS6KzkROj2emumvKD-PI1rD9CIDhwF33J-hHWU29A0V317gYFt-rwLem68ijpYX12niYiLqot2HdUJXXLn8FYhtLxetPAqUNELOeuhBIydVpd9ZH_IyJ18lJBjnvxQKx6FW7CpRMrKiwkjMMQd4HV4IZ` | https://www.explorationpub.com/Journals/eaa/Article/1009135 (HTTP 200) | Open Exploration, *Exploration of Asthma & Allergy*. "An expert position paper on environment, occupation and climate change effects on allergic respiratory diseases in Italy." Article, not a dataset. | No data series. Mentions PM2.5 and years 2000–2026 in its text, which are not a coverage period. No downloadable dataset found on the page. | No | Reject for N6: not a source of national mortality data. | **PENDING LEARNER DECISION.** An earlier version of this cell read "REJECTED (learner decision, final)". The learner could not confirm that; the claim is withdrawn (see clarification 2026-11-15). |
| 2 | `https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHNPE-Gqu82ZS9X14ANCBb7m1APTSPeJZ8l4xw1H3BA2wTS-fS6fr-eOjLuacIgcq94j2-5BnLRTJvSOg3KMT5ItL8--Wn2bz4Jt3MX1Bvy9g9kz_Ol6UaAVomZqx3NK0ur5E2Hx600DnGO3NNvIr1kz6czuWtSUNoNcktgata0nZBuN3VILQRPXnpJj10bIx3G05W_iEPPtNTTBnwgPtjblP0Md5JE8Ral3xmyCw==` | https://www.turkiyetoday.com/lifestyle/182000-deaths-in-europe-linked-to-air-pollution-in-2023-study-finds-3210692 (HTTP 200) | Türkiye Today (news). "182,000 deaths in Europe linked to air pollution in 2023, study finds." News article. | Europe-wide study summary for 2023. Not a dataset. Links only to the EEA 2025 briefing (row EEA-2025). | No | Reject as a source. Use the primary EEA page instead (see EEA-2025). | **PENDING LEARNER DECISION.** An earlier version of this cell read "REJECTED (learner decision, final)". The learner could not confirm that; the claim is withdrawn (see clarification 2026-11-15). |
| 3 | `https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHB4A_j6H49LeEhrqU_MfDpcWQ645EihjBx8y_FJypRT6bUry9KnMQg2wFSHhAgLxWyUKbsLWvybFrv9afrdpbTWLuC6_CeRXLtDrGqy3XtLB4PiSwTQHiapbZfykWQFSLZ4EIHtFdKiH59Ap-iG4NbhJk5CmB1LEy6PmIeHolIZlV_G3vUVl8A64BOySVvNYEXoabjOZ7eNU-3jlRnYXD_fMRBxIyleMZwJRY-hg4=` | https://oilprice.com/Energy/Energy-General/Europes-Air-Pollution-Crisis-Persists-Despite-Progress-on-Emissions.html (HTTP 200) | OilPrice.com (news). "Europe's Air Pollution Crisis Persists Despite Progress on Emissions." News article. | No dataset coverage. Its one dataset-like link points to a North Macedonia report PDF, which is unrelated to Italy. | No | Reject as a source. | **PENDING LEARNER DECISION.** An earlier version of this cell read "REJECTED (learner decision, final)". The learner could not confirm that; the claim is withdrawn (see clarification 2026-11-15). |
| 4 | `https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFwAnVYtmTtjeXJHnQwWk2RvKF5P7XFjSG202ADH74eZtWx08PCkIxoRHmi2YwAf19Gj2a5l2C9w55vViHAxOVOJcCvXu0TKm2024-9pi0drvYt2xXjXKwnALsoRP_Sxr2cAhJFDkX9ouuw_piL8Nek7OMgRefP_Nw9knCCkrGeMrRYPMeyN8R4TtjmGJKmAluWo6drW7jAo3YbrdeIXAetKmXhGD_C7w==` (not in the earlier log; added here) | https://www.egalite.org/en/pollution-eea-report/ (HTTP 200) | Égalité (secondary). "Air Pollution, Human Health and the Environment. EEA Report." Published 2025-01-25 per page metadata. | Secondary summary of EEA material. Points to EEA 2024 briefing (row EEA-2024). Not a dataset. | No | Reject as a source. Use the primary EEA pages instead. | **PENDING LEARNER DECISION.** An earlier version of this cell read "REJECTED (learner decision, final)". The learner could not confirm that; the claim is withdrawn (see clarification 2026-11-15). |

**Primary EEA pages (leads, not suggestions).** These were reached through links on the cited pages. They are not citations in the search output, so under the README rule they are **not eligible as Step 2b suggestions**. They are recorded so the learner knows what the primary source says.
- **EEA-2025:** EEA, "Harm to human health from air pollution in Europe: burden of disease status, 2025". https://www.eea.europa.eu/en/analysis/publications/harm-to-human-health-from-air-pollution-burden-of-disease-status-2025 (HTTP 200). Verified from the page: "based on data up to the year 2023"; covers 41 countries; reports a 57% fall in PM2.5 premature deaths in the EU from 2005 to 2023. No dataset download link found. Italy-specific figures were not verified. **Cannot support N6 production 2024–2025**, because its data ends in 2023. Possible use: annual national context for the prototype window only, after the learner reads it.
- **EEA-2024:** EEA, "Harm to human health from air pollution in Europe: burden of disease status, 2024". https://www.eea.europa.eu/en/analysis/publications/harm-to-human-health-from-air-pollution-2024 (HTTP 200). Verified from the page: data for 2022; 41 countries; PM2.5 premature deaths fell 45% from 2005 to 2022. No dataset download link found. **Cannot support N6 production 2024–2025.**
- The EEA pages also link to an EEA indicator, "Premature deaths due to exposure to fine particulate matter in Europe". It was **not opened** and is not verified.

**Search answer claim (checked, partly).** The model said that official 2024 and 2025 PM2.5 attributable-death figures for Italy have not been published by EEA, Eurostat, ISTAT or ISS, and that the latest year it cites is 2023. The EEA 2025 and 2024 pages support the 2023 and 2022 coverage they state. They do not show whether Eurostat, ISTAT or ISS have published 2024–2025 figures. That part remains **unresolved**.

**Status of UC1 N6 production.** Unresolved. None of the four cited links is a dataset with verified coverage for 2024–2025. No source is recommended for acceptance. **Learner decisions: all four UC1 N6 suggestions are PENDING LEARNER DECISION.** An earlier version of this paragraph said the learner had rejected all four as final. The learner could not confirm that, so the statement is withdrawn (see clarification 2026-11-15). No UC1 N6 suggestion has been accepted. N6 production remains **unresolved**; the absence of an accepted source does not establish that no 2024–2025 source exists.

**UC2 Step 2b for N2 history (run in the scratch copy only).**
- Step 2b was run in the scratch copy `/tmp/reuse_UC2`, not in this project. The scratch copy is a same-session rerun, not an independent fresh-session check.
- **UC2 N2 search (separate from the UC1 N6 suggestions above):** four cited redirect URLs were returned. None was verified and none was accepted. The details are in the scratch report, section 6.
- N2 history **remains unresolved**.
- The original UC2 pipeline outputs (`outputs/UC2/`) were **not changed** by this step. Their file hashes match the pre-check snapshot.

Inspected through the workflow (at least one accepted extra source): **not applicable yet.** No suggestion has been accepted. The UC1 N6 production gap is the only unmet need that Step 2b covers. UC2 has no unmet needs in its Scout output, so Step 2b has nothing to search for there.

## G1 and G3: one edge case in each function
*Assistant draft from the code and the tests. The learner must confirm or rewrite these in their own words.*
- **G1, `extract_licence`**: the edge case is a JSON-LD licence of "Unknown" (the Kaggle fixture). The code treats an explicit "Unknown" as a final answer: `licence_name` is null, `found_in` is `json-ld`, and the page's links and text are not searched. A later link or sentence cannot override it. So a dataset with an explicit unknown licence is recorded as `LIC-UNKNOWN`, not given a licence from elsewhere on the page.
- **G3, `jsonstat_summary`**: the edge case is a sparse `value` dict, where a position absent from the dict counts as a missing cell. The code counts non-null values and sets `missing_cells` to expected cells minus that count, so an absent or null cell is never read as zero. A non-ISO geo code such as Eurostat's `UK` or `EL` raises `NON_ISO_GEO_CODES`.

## G4–G5: feasible for one need or window, not another
*Assistant draft from UC1's calibrated run. The learner must confirm it.*
- Source and the rule or calibration decision: `link.uci_360` (UCI Air Quality). Rule 3 in the calibration section: a source that misses its proposed window but fully covers another required window stays `feasible_with_conditions` for that window only. The agent applied the same logic and scoped the source to prototype only.
- Feasible for (need, window), and why: N1 prototype. The UCI file holds hourly NO2 (the `NO2(GT)` column) and covers 2004-03-10 to 2005-04-04 (`records/link.uci_360.json`, `temporal.start` and `temporal.end`). Its verdict is `feasible_with_conditions`, with five conditions, including treating -200 as null.
- Not feasible for (need, window), and why: N1 production, and N3 production. The UCI file ends in 2005, so it cannot serve production. The agent scoped it to prototype with the condition "Use for prototype window only".
- Reason for each red flag you dismissed: none. `dismissed_rule_flags` is empty for every source in `outputs/UC1/discovery_results.json`. See the G5 section below for the one flag that rule 5 would have dismissed.

## G6: Allowlist changes
Exact hosts only. For each host: what it provides and why a broader domain is not needed.

| Host added | Needed for (source, page) | Why nothing broader | Date |
|---|---|---|---|
| `ec.europa.eu` | UC1 link N6, `https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sdg_11_52` (JSON-stat API, prototype and production windows). The same host serves the dataset response and the Eurostat copyright notice, which is the terms page. No separate file host is linked. | The exact host is the only one the link and its terms page need. The parent `europa.eu` is not added, because it would cover every Commission site. Subdomains of `ec.europa.eu` are not listed separately. | 2026-11-15 |

Hosts you chose **not** to add, and why:
- `catalog.data.gov`: the Chicago distractor's host. It is refused by design, and the refusal is the finding. Do not add it.
- `europa.eu`: a parent domain. It would allow every EU institution site, and the test forbids it.
- Any redirect target of the Eurostat API that is not `ec.europa.eu`: not added in advance. If a response redirects to another host, the guardrail refuses it and that refusal is recorded as a finding. (Not verified: no request was made in this step.)
- Note on matching: `host_allowed` also accepts any subdomain of a listed host. So `ec.europa.eu` admits `*.ec.europa.eu`, which is the existing matching rule and is not changed here.

## G5: Verdict calibration
- **Rules written** (`prompts/risk_assessor.md`, section "Verdict calibration", 8 numbered rules, all in the file): 1 clearable blocker gives `feasible_with_conditions` with a named resolver. 2 uncleared blocker gives `not_feasible`. 3 a window miss with coverage of another required window gives a window-scoped `feasible_with_conditions`. 4 partial coverage is conditional. 5 staleness is dismissed when every target window is historical. 6 only `must` gaps set the overall verdict. 7 a context source with a blocker gives `not_feasible`. 8 major flags cap a source at `feasible_with_conditions`, and minor flags never change the verdict. The reasoning is in the file itself.
- **Before / after status: NOT MEASURED.** No `--from-stage assess` run was made with the uncalibrated prompt, so no verdict change can be attributed to the calibration. The UC1 and UC2 runs used the calibrated prompt only. The "after" data in `outputs/UC1/` and `outputs/UC2/` is therefore a single calibrated result, not a before-and-after comparison.
- **Observations from the calibrated runs** (checked against the files, not changed):
  - *Rule 5 was not applied (superseded by the 2026-11-15 regeneration).* Pre-regeneration, `link.uci_360` kept the `FRS-STALE` flag (`outputs/UC1/discovery_results.json`). Its prototype window ends 2005-04-04, which is historical, so rule 5 says to dismiss it. `dismissed_rule_flags` is empty.
  - *Rule 7 was applied.* `link.europa_sdg_11_52_099aa6` is `not_feasible` because it is a context source with a blocker (`LIC-UNKNOWN`). The agent cites rule 7 for this. An earlier note in this session blamed rule 1 for the Eurostat verdict. That was wrong: rule 1 covers core sources and clearable blockers, and rule 7 covers context sources, which is the case here.
  - *Rule 7 also applied to UC2.* `api.nager_public_holidays` is `not_feasible` for the same reason.
  - *Rule 6 was applied.* UC1 and UC2 are both `not_feasible`, driven by must needs that are `partially_met` with no candidate closing the gap.
- **Status of these observations:** they are recorded only. No prompt change was made. Any change to the calibration rules would need a new before-and-after run, as G5 requires.

## G7: One agent failure, fixed at its cause

**Scope of this record.** There are three UC1 Scout runs. Each run has its own label and its own figures. Do not compare figures across labels without checking the label:
- **Run A, before the fix:** `outputs/artifacts/g7_before_UC1/`.
- **Run B, first fix:** `outputs/artifacts/g7_pre_hardening_UC1/`. These are the copied outputs from the run after the first fix. The figures below for Run B come from its files.
- **Run C, final hardening:** the current `outputs/UC1/`. Its events start at line 59 of `outputs/UC1/trace.jsonl`. Lines 1–58 belong to Runs A and B.

Checksums: `outputs/artifacts/g7_before_UC1/SHA256SUMS.txt` (verified). `outputs/artifacts/g7_pre_hardening_UC1/SHA256SUMS.txt` (its entry for itself hashes an empty file, because the shell created the file before the checksum ran; the other entries are valid).

- **Symptom:** The expired AtmosData Pro feed (`vendor.atmosdata_pro`) was missing from the Scout output: no candidate, no rejection and no unmet entry. The same run listed "N2 prototype: not required" as unmet, and the Planner put a register name into an internal query.
- **Evidence (Run A):** `trace.jsonl` line 13: the Scout's `list_external_register` returned the expired feed. Line 23: the Scout searched the internal catalog for "AtmosData weather feed" and got no hits. Line 11: the Scout searched "patient visit records event level". `search_plan.json`: N3 `register_ids` had only `api.open_meteo_archive`, while its `likely_pitfalls` said to record the expired feed as a finding. `candidates.json`: the vendor feed is absent from candidates and rejections, and `unmet_needs` has 7 entries, including "N2 prototype: not required by the spec" (`unmet_needs[1]`).
- **Root cause:** Four links. (1) The Planner had no check that a tagged vendor feed is mapped to a need. (2) Nothing stopped a register name from going into `internal_queries`. (3) The Scout's submit check did not require planned vendor feeds to be accounted for, and did not check that unmet entries are genuine gaps. (4) The tools had no guard for out-of-scope searches or for per-call variable changes.
- **Fix:**
  - New `discovery_agent/guards.py`: scope terms, variable locks, register-name detection, and per-use-case `excluded_sources`. All of it reads the use-case contract and the register.
  - `discovery_agent/agents.py`. Validators, with the pre-existing ones marked:
    - Planner: `covers_all_needs` (pre-existing), `register_ids_are_data_sources`, `vendor_feeds_are_mapped`, `no_register_names_in_queries` (first fix), `excluded_sources_are_not_mapped` (follow-up).
    - Scout: `ids_exist` (pre-existing), `planned_vendors_accounted`, `unmet_are_genuine_gaps` (first fix), `candidates_in_scope`, `unmet_cover_every_gap` (follow-up).
  - `discovery_agent/tools/internal_catalog.py`: out-of-scope searches are refused and excluded catalog entries are withheld. Policy wiki pages are not filtered.
  - `discovery_agent/tools/public_api.py`: per-call overrides of `hourly`, `daily`, `current` and `minutely_15` are refused, while dates and coordinates may still change. `list_external_register` marks excluded sources. `call_public_api` refuses an excluded source.
  - `discovery_agent/validation.py`: checks the `scope`, `excluded_terms` and `excluded_sources` fields.
  - `discovery_agent/orchestrator.py`: passes the plan to the Scout validator.
  - `use_cases/UC1_air_quality.json`: N5 gets `scope: out_of_scope` and its `excluded_terms`; its name is unchanged. The top-level `excluded_sources` entry for `api.nager_public_holidays` is new. UC2's contract is unchanged.
  - `discovery_agent/prompts/planner.md`, `scout.md` and `profiler.md`: the rules the validators enforce.
- **Tests and test-file changes:**
  - `tests/test_g7_regressions.py`: 18 tests (first fix).
  - `tests/test_g7_scope_and_completeness.py`: 16 tests (follow-up).
  - `tests/test_agent_loop.py`. First fix: fixtures only. `plan_payload` maps the tagged vendor feed to the first need, and the fake Scout's submission lists it in `rejected_without_profiling`. No assertion changed. Follow-up: the full-pipeline fixture changed, and one assertion's source identifier changed (see below).
  - `tests/test_g7_regressions.py`, `test_genuine_unmet_gaps_are_accepted`: the list was expanded from 4 to 7 entries. Its assertion is unchanged.
  - The follow-up changes to `tests/test_agent_loop.py` and `tests/test_g7_regressions.py` are explained below.
- **Changes to `tests/test_agent_loop.py` (follow-up), and why:**
  - The full-pipeline fixture's candidate changed from `internal.clinic.patient_visits` (N5) to `internal.clinic.resp_visits_daily` (N4), and the fake's catalog record was renamed to match.
  - The assertion that checks the PII flag now looks up `internal.clinic.resp_visits_daily`. This is the one changed assertion identifier. The check itself is unchanged: the candidate's record must carry `GOV-PII`.
  - The fake Scout's `unmet_needs` now lists the six required windows with no candidate.
  - **Why:** the out-of-scope rule rejects a candidate that serves N5 or matches the excluded phrases, so the fake Scout was rejected on every turn. The completeness rule requires the fake's `unmet_needs` to cover every required window with no candidate. The in-scope candidate keeps the PII-flag path under test. The source-set assertion and the link assertions are unchanged.
- **Changes to `tests/test_g7_regressions.py` (follow-up), and why:** the genuine-gaps list in `test_genuine_unmet_gaps_are_accepted` was expanded to cover every required window that the Open-Meteo candidate does not cover. The three added entries are N1 production, N4 production and N6 production. **Why:** the completeness rule reports each such window missing from `unmet_needs`, so the original list would fail. The assertion (no `unmet_needs` error) is unchanged.
- **Not demonstrated:** that the G7 regression tests fail against the pre-fix code. No revert run was done, so this record makes no claim about that.
- **Re-run:** `python -m discovery_agent run --use-case UC1 --stop-after scout --no-input`. Run B used the first-fix validators; Run C used the final validators.
- **Before / after, by run:**
  - *Run A (before the fix):* 6 model calls, 20 tool calls, 0 HTTP. Vendor feed absent. Unmet entries: 7, including "N2 prototype". N3 `register_ids`: open-meteo only.
  - *Run B (first fix; 70 tests at that time):* 9 model calls, 15 tool calls, 0 HTTP. The vendor feed is a candidate, `vendor.atmosdata_pro`, with `suspected_issues` beginning "BLOCKED: agreement_status expired". The Planner's first attempt put "AtmosData station weather feed" in an internal query, and the retry fixed it. Unmet entries: 4 (N1 prototype, N6 prototype, N6 production, N5 production). Humidity is recorded as a coverage gap.
  - *Run C (final hardening; 86 tests in the full suite, 34 in the focused G7 set):* 10 model calls, 16 tool calls, 0 HTTP. The vendor feed is not a candidate. It is in `rejected_without_profiling` with the reason "Expired agreement: contract AD-2021-114 ... Not usable for production; not profiled." The holiday API and the patient-level entry are also in `rejected_without_profiling`. Unmet entries: 4, the same four as Run B. The Planner was rejected once and then accepted. The Scout was rejected three times (7, 4 and 2 errors) and then accepted. No search used an excluded phrase, and no `call_public_api` call was made. Humidity is recorded as a coverage gap in the Open-Meteo candidate's suspected issues and in the N3 acceptance criteria.
- **Decision this failure could affect:** N3 production. The AtmosData feed is the only station-grade weather source in the register. It is not usable (expired agreement, key revoked), and the configured Open-Meteo query lacks humidity, so the production weather source for the live model is not established. The learner must decide whether a renewal, a signed agreement or a different source is needed.
- **Related source or test checked:**
  - `internal/UC1_valdena_health/wiki/clinic_data_policy.md`: the restriction on patient-level records.
  - `internal/UC1_valdena_health/wiki/station_network.md`: VR-03 stopped 2024-06-30. The catalog still lists the network as active. Run C's `airq.station_readings` candidate records this mismatch in its suspected issues.
  - `tests/test_g7_regressions.py` and `tests/test_g7_scope_and_completeness.py`.
- **Follow-up items, and their status in Run C:**
  - *Holiday API.* `api.nager_public_holidays` is excluded for UC1 by `excluded_sources` in the UC1 contract. The Planner rejects it in `register_ids`, the Scout rejects it as a candidate, and `call_public_api` refuses it for UC1. The register listing marks it `excluded_by_use_case`. Run C: not mapped, not a candidate, listed in `rejected_without_profiling`. UC2 has no exclusion, and its Nager entry is unchanged.
  - *Unmet-needs completeness.* Every required need-window that no candidate covers must appear in `unmet_needs`. Windows a need does not require are not demanded. Run C: the four uncovered windows are listed.
  - *Out-of-scope candidates.* A candidate that serves an out-of-scope need, or whose catalog entry matches the excluded phrases, is rejected. Policy documentation stays readable and searchable. Run C: no patient-level candidate.

## Other decisions

### UC1 assumptions and scope decisions (2026-11-15)
- **Weather location (assumption, not a claim).** Valdena is fictional. For the Open-Meteo weather call I use Milan, Italy, as a documented geographic proxy for northern Italy: latitude 45.4642, longitude 9.1900. This is **not** a claim that Valdena is Milan. Changed in `config/external_sources_register.json`, `api.open_meteo_archive`, `default_query`, latitude and longitude only, as the README allows. The same register entry is also used by UC2, so UC2 inherits this proxy unless it is changed again with its own note.
- **Weather window.** The register's default dates (2014-01-01 to 2014-01-03) are not the UC1 windows and are left unchanged. Probes must pass the prototype or production dates per call, through the `query` argument, not by editing the register.
- **N5 (patient-level records) is kept as a `could` need, out of scope by brief.** The brief's scope excludes individual patient records and `internal/UC1_valdena_health/wiki/clinic_data_policy.md` says they may not be used. The need name in `use_cases/UC1_air_quality.json` now says so, because the Scout only receives the spec, not the brief. Agents must not search for, open, download or profile patient-level records. An entry such as `clinic.patient_visits` is to be reported as a scope and privacy finding.
- **N3 humidity is a coverage gap if the configured query cannot supply it.** The register query requests `temperature_2m` and `shortwave_radiation` only. Humidity is not requested, and the README forbids changing the variables. N3 stays `hourly temperature and humidity` in the spec. If humidity is not available, the record shows a coverage gap for humidity and the need is not silently reduced to temperature.
- **Holidays are not matched to UC1.** `api.nager_public_holidays` stays tagged for UC1 in the register, but no UC1 need uses it, and no need was added for it.

### UC1 gate decisions (`outputs/UC1/gate_decisions.json`)
- **Decisions (learner):** UCI `uci:360` accept for N1 prototype. Eurostat `sdg_11_52` accept for N6 prototype only. Chicago `open-air-chicago-hour-aggregations` accept as an intentional distractor.
- **Reasons were transcribed by the assistant, word for word, from the learner's dictated decision statements. They were not written by the assistant:**
  - UCI: "I accept this dataset because it provides hourly NO2 measurements for an Italian city, making it relevant to the UC1 air-quality prototype. Its single-site coverage and missing-value limitations will be evaluated during profiling." This reason was dictated by the learner in the message that confirmed the gate decisions, and it was transcribed word for word. It replaces the earlier decision-only line, "ACCEPT for N1 prototype.", which the assistant had recorded because no separate reason had been given.
  - Eurostat: "Accept for N6 prototype only: it must not be mapped to production because its data ends in 2023."
  - Chicago: "Accept as an intentional distractor. It is not suitable for the Italian study area, and its domain must remain outside the allowlist so the pipeline records the refusal."
- **Change to `outputs/UC1/links.json`:** the Eurostat link's `target_windows` was narrowed from `["prototype", "production"]` to `["prototype"]`, and its note now says the data ends in 2023 and is not mapped to production. No other link changed.
- **Allowlist:** unchanged. `catalog.data.gov` is not on it, so the Chicago refusal will be recorded by the pipeline.

### Review and sign-off decisions (2026-11-15)
- **UC1 review decisions (learner):** agree with overall `not_feasible`; agree with the UCI missing-value and single-site limits; the `FRS-STALE` dismissal for `link.uci_360` under G5 rule 5 is **assessor-generated, not a learner override**, and learner agreement is not recorded (historical prototype window; verdict unchanged); agree with the Eurostat licence uncertainty and partial window coverage. Sign-off recommendation: `proceed_with_conditions`, prototype only.
- **UC2 review decisions (learner):** agree with overall `not_feasible`; agree with the Open-Meteo conditions and the Nager licence and geography limits. Sign-off recommendation: `stop` until the blockers are resolved.
- *Superseded:* "The override is recorded, not applied. `outputs/UC1/discovery_results.json` is unchanged." The regenerated `discovery_results.json` now carries the dismissal. Correction (2026-11-15): the dismissal is assessor-generated under rule 5; the sign-off `overrides` list is empty; learner agreement is not recorded.
- **Reviewer identity and review time are placeholders** in both reviews and both sign-offs. The assistant did not supply them. The learner must replace them before submission. The self-check accepts any non-empty reviewer value, so it does not verify identity.
- **Step 2b status:** four redirect URLs for UC1 N6 production (see "Source suggestions"). All four are PENDING LEARNER DECISION. An earlier version said three; the count was wrong. The publisher pages were not verified: they are not reachable through the allowlist, and the redirect targets were not followed. UC2 has no unmet needs.
- **G5 calibration status:** unchanged from the earlier entry. No before-and-after run was made. The calibration observations are recorded and the rule 5 dismissal above is assessor-generated (see the 2026-11-15 correction), not a learner override and not a prompt change.

### Eurostat record findings (`link.europa_sdg_11_52_099aa6`, UC1 N6), 2026-11-15
These findings are recorded as they are. The profiler was not changed, and no model call was made to correct them.

1. **[SUPERSEDED 2026-11-15] Inferred missing-value flag (TC-022 fails).** Superseded by the TC-022 correction and regeneration (see the correction log below). The original text follows. `records/link.europa_sdg_11_52_099aa6.json` sets `declared_metadata.has_missing_values` to `"no"`. The source (the JSON-stat response) does not declare this flag. No tool result contains the string. It appears only in the profiler's own output (transcript `profiler__link.europa_sdg_11_52_099aa6.json`, the agent's submitted record). The value was inferred from `missing_cells: 0`. The field is labelled as declared metadata, so it breaks the "no inference" rule (`_shared_rules.md`, "Unknown stays unknown"). The memo repeats it: `outputs/UC1/feasibility_memo.md`, line 91, "36 cells, no missing values".
2. **Eurostat 2006 gap (preserved).** The time dimension lists 2005, then 2007 to 2023. Year 2006 is absent, so the series has 18 periods, not 19. Evidence: the `summarize_jsonstat` tool result in the same transcript (`"values": ["2005", "2007", …]`, `expected_cells` 36 = 2 units × 18 periods). The record's `quality_notes` state the gap. Its `unknowns` list it as "Whether the 2006 gap is a publication gap or a deliberate omission". Because the year is absent from the dimension, `missing_cells: 0` does not show it.
3. **Effect on the verdict.** None: the link is `not_feasible` for licence, coverage and context reasons, which do not depend on the 2006 gap or the inferred flag. The inferred flag would matter only if a rule relied on it. `DQ-METADATA-CONTRADICTION` was not raised for this source.
4. **[SUPERSEDED 2026-11-15] Rubric TC-022: Fail.** Superseded by the later correction and validation: the Eurostat record was regenerated without the inferred flag, the fix is covered by passing tests, and the UC1 check reports no problems. The rubric re-check itself is for the learner to record. The original text follows. The rubric's scale is Pass or Fail, so "Partial" is not available. The licence, owner and refresh cadence fields are correctly null and listed as unknowns, and the claims cite their tools. The inferred `has_missing_values` value fails the "no inference" requirement.
5. **Optional fix, not done.** A profiler rule that `declared_metadata` takes only values the source states (otherwise `null`), followed by a re-profile of this one link and a re-assess. This needs model calls and a new before-and-after record. It was not done, per the instruction.

---

## Correction log, 2026-11-15 (independent review items TC-018, TC-019, TC-021, TC-022, TC-025)

Entries above this line are unchanged. The corrections below supersede them where they conflict.

### TC-022: Eurostat `declared_metadata.has_missing_values` (UC1, `link.europa_sdg_11_52_099aa6`)

**Before (snapshot: `outputs/artifacts/tc022_before_UC1/`, checksums in `SHA256SUMS_before.txt`).** The record's `declared_metadata` was `{"has_missing_values": "no", "missing_cells": 0, "expected_cells": 36, "value_count": 36, "status_counts": {}, "warnings": [], "updated": "2025-12-09T11:00:00+0100"}`. The memo said "36 cells, no missing values" (2 occurrences). No tool result for this source contained a `has_missing_values` key.

**Root cause, traced.**
1. `summarize_jsonstat` (`discovery_agent/tools/formats.py`) returns publisher fields (`label`, `updated`, `source`) and its own computed counts (`expected_cells`, `value_count`, `missing_cells`, `status_counts`, `warnings`) in one flat dict. The G3 tests pin those key names, so they were not renamed.
2. The profiler prompt (`prompts/profiler.md`) had no rule for `declared_metadata`. The schema describes it as flags "exactly as the source declares them", but the prompt did not say so. The profiler copied the computed counts into it and added `has_missing_values: "no"`, inferred from `missing_cells: 0`. The transcript (`transcripts/profiler__link.europa_sdg_11_52_099aa6.json`) shows this in the accepted submission; the value appears nowhere in a tool result.
3. Nothing checked it. The profiler's validators checked only ids, kind and dates. `DQ-METADATA-CONTRADICTION` (`risk_rules.py`) reads a declared "no" as a publisher claim, so an inferred "no" can hide a real contradiction.

**Fix (at the source).**
- `discovery_agent/prompts/profiler.md`: new rule. `declared_metadata` holds only flags the source states. Computed counts go to `sample_findings` or `quality_notes`, and an unstated flag is null. A count never implies a flag.
- `discovery_agent/agent.py`: the agent loop now collects every key found in successful tool results during a run (`collect_keys`) and passes them to new `evidence_validators` (`validate(..., evidence)`). Existing validators are unchanged.
- `discovery_agent/agents.py`: `declared_flags_are_stated` (registered on the profiler spec). A non-null `has_missing_values` is rejected unless the key appears in a tool result for that source. `contains_pii` is **not** covered yet, because existing records set it without evidence. This is a known follow-up.
- `tests/test_tc022_declared_metadata.py`: 6 new tests. `tests/test_learner_gaps.py` was not edited.

**Tests.** Full suite before the regeneration: 92 passed (86 existing + 6 new). Saved after the regeneration in `outputs/artifacts/pytest_tc022_after.txt`: full suite 92 passed; `test_learner_gaps.py` 21 passed; the new file 6 passed. `pytest_before.txt` and `pytest_after.txt` were not changed (checked by sha256).

**Regeneration (commands).**
```
.venv/bin/python -m discovery_agent run --use-case UC1 --from-stage profile --stop-after profile --only link.europa_sdg_11_52_099aa6 --links-file outputs/UC1/links.json --no-input   # 3 LLM calls, exit 0
.venv/bin/python -m discovery_agent run --use-case UC1 --from-stage assess --no-input                                                                                          # 2 LLM calls, exit 0
.venv/bin/python -m discovery_agent check UC1    # printed only; outputs/artifacts/check_UC1.json was NOT overwritten. problems: []
```

**After.** `declared_metadata` is `{}`. `sample_findings` now says: "expected_cells 36, value_count 36, missing_cells 0 (tool-computed, not a source flag)". The 2006 gap is still recorded in `quality_notes` and `unknowns`.
- Verdicts unchanged for all 8 sources; overall verdict still `not_feasible`.
- Red-flag codes unchanged for all sources. The only evidence text that changed is the Eurostat `LIC-UNKNOWN` evidence, which now quotes the new record.
- The memo was regenerated as a whole, not patched. It has 0 occurrences of "no missing values" (was 2). About 297 diff lines overall, including wording changes in sections unrelated to Eurostat (for example the `link.uci_360` section). Verdicts and flag codes did not change. Please read the new memo before relying on any wording.

**Not verified or still open.**
- The live rejection path of the new validator was not exercised: the profiler complied on the first attempt. Only the unit tests cover the rejection.
- `review_UC1.md` (open item on the Eurostat record finding, "memo line 91") and `DRAFT_*`/`signoff.json` refer to the old text. They were not edited. The learner must reconcile them.
- Other records use profiler-inferred flags, for example UC2 `api.nager_public_holidays` `has_missing_values: "unknown"`. They are not re-profiled and are not changed by this fix. The validator would reject them on re-profile.

### TC-018: gate validation (scratch copy `/tmp/tc018_scratch`; the real project was not used)
Both runs used the real credentials path, so the gate code (not the credentials check) stopped them. Command: `python -m discovery_agent run --use-case UC1 --from-stage profile --links-file outputs/UC1/links.json --no-input`.

| Case | Setup | Result | LLM calls | Trace lines |
|---|---|---|---|---|
| A | `gate_decisions.json` absent | exit 1: "Missing .../gate_decisions.json. Record accept or reject ..." | 0 (`llm_call` events 57 before, 57 after) | 172 before, 172 after |
| B | decisions for the UCI link only (1 of 3) | exit 1: "No decision for https://ec.europa.eu/... in .../gate_decisions.json" | 0 (57 before, 57 after) | 172 before, 172 after |

Logs: `outputs/artifacts/tc018_gate_validation/`. Note: the gate code reports the first missing link only, so case B does not list the Chicago link too. The scratch `run_history.jsonl` got one line per attempt, with `llm_calls: 0`. A test sanity note: the first attempt of this check ran without credentials and stopped at the credentials check, so it did not test the gate. It was discarded and rerun.

### TC-019: Step 2b suggestions (UC1 N6 production)
- **Count mismatch.** The "Source suggestions" table has **four** rows, not three. Its "Learner decision" column said **REJECTED (learner decision, final)** for all four. That reading is withdrawn; see clarification 2026-11-15. Another section (`Review and sign-off decisions`, the "Step 2b status" bullet, written earlier) says "three unresolved Google redirect URLs ... None is decided." These two statements conflict. Which is current is for you to state. I have not changed either one.
- **Re-check (2026-11-15, `outputs/artifacts/tc019_step2b_recheck.txt`).** Each redirect was resolved by a plain GET. Three resolve to the same pages the log records: Open Exploration (asthma position paper, `explorationpub.com`), Türkiye Today (news, `turkiyetoday.com`), OilPrice (news, `oilprice.com`). **The fourth does not match.** The log's fourth redirect (row 4, `AUZIYQFwAnVY...`) now resolves to `soldionline.it`, an Italian article on packaged gelato sales, not to `egalite.org`. The log's `egalite.org` page does exist (HTTP 200), so the mapping in the log is wrong or the redirect is not stable. I cannot tell which.
- **Coverage on the pages (as the pages state it).** None is a dataset or a statistics table. None states 2024 or 2025 PM2.5 mortality for Italy from Eurostat, ISTAT or ISS. The news and secondary pages cite the EEA 2025 report, which covers data to 2023 (EU 182,000 deaths in 2023; Italy 43,083). Access and licence: no page states a data licence, because none is a data source. The Égalité page is a secondary summary of an EEA 2024 briefing.
- **Decisions.** None made here. The four UC1 N6 suggestions are PENDING LEARNER DECISION. The earlier "rejected" record is not confirmed (see clarification 2026-11-15).

### TC-021: reviewer placeholders
Field locations (exact, current files):
- `outputs/UC1/signoff.json` line 2: `"reviewer": "KUNILATA MUDULI"`
- `outputs/UC2/signoff.json` line 2: `"reviewer": "KUNILATA MUDULI"`
- `outputs/artifacts/review_UC1.md` lines 3 and 5: `Reviewer: KUNILATA MUDULI`, `Review time: 30 Mins`
- `outputs/artifacts/review_UC2.md` lines 3 and 5: the same two values.

What is wrong. The template (`_TEMPLATE_signoff.json`) says `"reviewer": "Your name"`. The check (`validation.py` line 130) accepts any non-empty value, so it does not verify identity. The earlier decision log (section "Review and sign-off decisions") says the reviewer identity and review time are placeholders that the learner must replace. I cannot confirm whether `KUNILATA MUDULI` is the learner's name, so it is not verified here. The "30 Mins" review time is not measured here.

Also drafted, not confirmed: the UC1 sign-off conditions. Owners "Valdena Civic Health Office", "Legal" (twice), "analytics team" and "Environment Monitoring Unit", and due dates `2026-12-15` and `2026-12-31` (`outputs/UC1/signoff.json` lines 7–28). These are drafted values. The learner must confirm the owners and dates, or replace them.

### TC-025: transcript submissions vs outputs
Command and full output: `outputs/artifacts/tc025_transcript_compare.txt` (script `outputs/artifacts/tc025_transcript_compare.py`).
- **Profile records (UC1 7, UC2 5): identical** to the accepted `submit_catalog_record` payload in each transcript (accepted = the submission whose tool result was `accepted`).
- **Risk assessment (UC1, UC2): identical** to the accepted `submit_risk_assessment` payload.
- **Planner and scout (search plan, candidates): identical** to the accepted payloads.
- **Memo (UC1, UC2):** each `feasibility_memo.md` begins with the exact submitted markdown. The added text is a footer that `orchestrator.human_gate` generates (the "Human review gate" section, with the generation timestamp and model name). The footer is code, not a manual edit (UC1 2055 chars, UC2 2148 chars).
- **Pre-fix UC1 snapshot:** the same checks pass (records, risk assessment, memo prefix).
- **Not covered.** `discovery_results.json` is built by code from the records and rules, not submitted by an agent, so it is not part of this comparison. The transcripts themselves are written by the code and have no independent hash from generation time, so this check shows that outputs match the transcripts, not that the transcripts are untouched.
- Evidence of manual editing: none found in these files.

### TC-022 addendum (2026-11-15): correction to the regeneration entry above
- The regenerated assessment (`outputs/UC1/risk_assessment.json`, `discovery_results.json`) records a dismissal of `FRS-STALE` for `link.uci_360`, with the assessor's own reason ("Every target window ... is the prototype window ... Recorded per calibration rule 5."). The pre-fix assessment had no dismissal (`outputs/artifacts/tc022_before_UC1/risk_assessment.json`, `dismissed_rule_flags` absent).
- The statement "red-flag codes unchanged" above is true for codes that are raised, but it omitted this dismissal. The dismissal arose from re-running the assessor, not from the TC-022 fix.
- `signoff.json` and `review_UC1.md` say the agent kept the flag and that the learner's override is the only dismissal. Both now conflict with the regenerated record. Not edited here: the learner decides which statement stands. *Resolved 2026-11-15 (Part 1):* both files now describe the dismissal as assessor-generated, with learner agreement not recorded.

### Clarification 2026-11-15: UC1 N6 Step 2b suggestions (TC-019)

- **Withdrawn statement.** Earlier entries recorded that the learner had made final rejection decisions on all four UC1 N6 suggestions: the "Learner decision" column of the Source suggestions table, the status paragraph under that table, and the "Step 2b status" bullet in "Review and sign-off decisions". Those entries were written by the assistant. The learner has said they cannot confidently confirm making final rejection decisions for all four, and I cannot find direct evidence of an explicit decision for each in the project files. The rejection claim is therefore withdrawn.
- **Current status, UC1 N6 (four suggestions, rows 1–4 of the table):** **PENDING LEARNER DECISION** for all four. None has been accepted. None has been entered as a dataset link or inspected through the pipeline.
- **Count.** The UC1 N6 set is four. The first log recorded three, and row 4 was added later. Statements that said "three" were wrong.
- **Separate set, UC2 N2.** The four redirect URLs from the UC2 N2 search (scratch copy only, `/tmp/reuse_UC2`) are a different set, with a different need and a different run. They are not counted above and carry no decision.
- **Not changed.** The redirect resolution details, the 2026-11-15 re-check (`outputs/artifacts/tc019_step2b_recheck.txt`), and the assistant's recommendation column. The recommendations are labelled as recommendations, not decisions.
- **Needed from the learner.** For each UC1 N6 suggestion, either an accept, reject or revise decision with a reason in the learner's own words, or a statement that it remains undecided. Until then, UC1 N6 production stays unresolved.
- **TC-019 status: NOT PASSED (pending learner decisions).** The rubric's TC-019 entry ("Not done (learner)") is still accurate.

### Part 1 and Part 2 corrections, 2026-11-15 (FRS-STALE documentation; UC2 Nager metadata)

**Part 1: FRS-STALE, `link.uci_360`.** The dismissal is assessor-generated under calibration rule 5. Its only target window is the prototype window (2004-03-10 to 2005-04-04), and it is in the regenerated `risk_assessment.json` and `discovery_results.json`. It is not a learner override. Changes: `outputs/UC1/signoff.json` `overrides` is now `[]` (the four agreements are unchanged); `outputs/artifacts/review_UC1.md` sections 3.1 and 4 describe the dismissal as assessor-generated, with "Learner agreement: not recorded"; the statements "rule 5 was not applied" and "override recorded, not applied" are marked superseded in this file. No assessment or memo was regenerated for this correction.

**Part 2: UC2 Nager (`api.nager_public_holidays`).**
- Before: `declared_metadata` = `{"has_missing_values": "unknown", "contains_pii": "no", ...}`. Neither value appears in any tool result for this source (checked against `outputs/artifacts/nager_before_UC2/transcripts/`).
- Fix: `contains_pii` added to `PUBLISHER_FLAGS_NEEDING_EVIDENCE` in `discovery_agent/agents.py`; two regression tests added to `tests/test_tc022_declared_metadata.py`.
- Targeted command run: `.venv/bin/python -m discovery_agent run --use-case UC2 --from-stage profile --stop-after profile --only api.nager_public_holidays --no-input` (5 model calls, exit 0).
- After: `declared_metadata` = `{"has_missing_values": null, "contains_pii": null}`. Files that changed in `outputs/UC2/`: the Nager record, its profiler transcript, `run_history.jsonl`, `run_summary.json`, `trace.jsonl`. No other file changed. Rule flags were recomputed offline with `discovery_agent.risk_rules.evaluate`: before and after both give `LIC-UNKNOWN` only, so the flags are unchanged. No assess or memo run was made.
- **Open issue, not resolved by this change.** The targeted profile also rewrote other parts of the Nager record, and the new `temporal` block is not supported by any provenance entry. `temporal.end` is now `2026-12-26`, a date after the as-of date (2026-10-15). It is the last holiday date in the probed responses, not a documented coverage end. `temporal.grain` changed from `daily` to `static`. The UC2 N4 need has `min_grain: daily`, so the grain change needs review if the rules are re-run. Decision needed: accept, restore the pre-run record from `outputs/artifacts/nager_before_UC2/` (which keeps the unsupported `has_missing_values` and `contains_pii` values), or re-profile with a validator rule for temporal coverage. No decision has been made here.
- **Known unsupported metadata, unchanged records.** `contains_pii: "no"` remains in `outputs/UC1/records/api.open_meteo_archive.json` and `outputs/UC2/records/api.open_meteo_archive.json`. These records were not re-profiled. `contains_pii` drives no flag (`GOV-PII` fires only on `true`). The new validator rule would reject these values on re-profile.

### Human-reviewed correction: UC2 Nager temporal fields, 2026-11-15

- **Record:** `outputs/UC2/records/api.nager_public_holidays.json`.
- **What the profiler produced.** The targeted profile (see the Part 2 entry above) set `temporal.end` to `2026-12-26` and `temporal.grain` to `static`. The end date is the last holiday date in the 2026 probe, not a documented coverage end, and it is after the as-of date (2026-10-15). The change to `static` was not supported by the evidence. The profiler produced both values, and no provenance entry supports either.
- **Human-reviewed correction.** Both fields are restored to their pre-run values from `outputs/artifacts/nager_before_UC2/records/api.nager_public_holidays.json`: `temporal.end` = `null`, `temporal.grain` = `daily`. This was a human review decision, and the reason is the one above.
- **Retained.** `declared_metadata` = `{"has_missing_values": null, "contains_pii": null}`, the corrected values from Part 2. The old unsupported values (`"unknown"`, `"no"`) are not restored.
- **Not changed.** Other text fields that the targeted profile rewrote (`summary`, `schema`, `licence` evidence, `provenance`, `quality_notes`, `unknowns`, `title`, `spatial`, `status`, `access`, `documentation_excerpts`) are left as the profiler produced them. Two of them still conflict with the restored grain: the `summary` calls the source "a static calendar lookup", and the `provenance` probe note cites the 2026-12-26 maximum as an observation (that note is accurate as an observation). They were not in scope for this correction and are recorded here as remaining profiler text.
- **Historical evidence preserved.** The profiler transcript `outputs/UC2/transcripts/profiler__api.nager_public_holidays.json` is unchanged. It still holds the accepted submission with `temporal.end` = `2026-12-26` and `grain` = `static`. The corrected record is not the model's submission.
- **Assessment and memo.** Not regenerated. Neither `outputs/UC2/risk_assessment.json`, `discovery_results.json` nor `feasibility_memo.md` cites the Nager temporal values, so the correction does not change them. Rule flags for this source were unchanged by the targeted profile (`LIC-UNKNOWN` only).

### TC-025 status note (2026-11-15), Nager record

- The Nager record was generated by the profiler, and the accepted submission is in its transcript. The comparison script now reports `identical_to_record=False`, `differing_keys=['temporal']`. That difference is the documented human correction above (`end` `null`, `grain` `daily`). The `declared_metadata` values match the submission.
- Status: the record is profiler-generated, with a documented human correction to two temporal fields. It is not an unexplained hand edit. TC-025's "outputs match transcripts" result holds for every other record. For this record it holds except for `temporal`.

### Documentation corrections, 2026-11-15 (final submission cleanup)

1. **Human wording correction, UC2 Nager record.** In `outputs/UC2/records/api.nager_public_holidays.json`, the `summary` phrase "static calendar lookup with no daily values" was changed to "calendar lookup of holiday dates, with no daily measurements". Reason: the profiler's word "static" conflicted with the restored `temporal.grain` = `daily`, and the new wording describes the content without a grain term. This is a human wording correction. Every other field is unchanged. The record was not regenerated.
2. **Outdated holiday-API statements in the UC1 generated memo (not corrected).** `outputs/UC1/feasibility_memo.md` lines 164, 175 and 200 say the brief tags a holiday API for UC1. The learner's UC1 contract excludes it (`use_cases/UC1_air_quality.json`, `excluded_sources`, 2026-11-15). **The contract exclusion governs UC1.** The memo predates the exclusion, because the memo writer does not receive `excluded_sources`. The generated memo has **not** been edited or regenerated. Mentioned in `review_UC1.md`, section 6.
3. **Pending inputs, not filled.** These are marked PENDING in `review_UC1.md` and `review_UC2.md`: the reviewer name, the review date and the review time. The reviewer and the owner and due-date fields in `outputs/UC1/signoff.json` and `outputs/UC2/signoff.json` are unchanged and not confirmed by the learner: owners "Valdena Civic Health Office", "Legal" (twice), "analytics team" and "Environment Monitoring Unit", and due dates 2026-12-15 and 2026-12-31. The learner must confirm or replace each.
4. **Walkthrough deliverable.** `outputs/artifacts/walkthrough.md` is the deliverable. A note added to the README Submission notes section says so. The assistant draft is not submitted as the learner's walkthrough. The learner writes the content.
5. **TC-019 unchanged.** The four UC1 N6 suggestions remain PENDING LEARNER DECISION.

### Punctuation and superseded-label corrections, 2026-11-15 (documentation only)
1. **Punctuation, UC2 Nager summary.** "and" was added before "covers national holidays only" in `outputs/UC2/records/api.nager_public_holidays.json`. Wording and all other fields are unchanged.
2. **Superseded labels.** The earlier "TC-022 fails" entry and the "Rubric TC-022: Fail" item above are marked SUPERSEDED. They are kept as history.
3. **Draft sign-offs.** `outputs/artifacts/DRAFT_signoff_UC1.json` and `DRAFT_signoff_UC2.json` have a non-submission label in their `_status` field. No other field was changed, and the files were not deleted.

### Punctuation/grammar correction, UC2 Nager summary (2026-11-15)
- In `outputs/UC2/records/api.nager_public_holidays.json`, the summary fragment "with no daily measurements, and covers national holidays only, and was probed successfully" was replaced with "with no daily measurements; it covers national holidays only and was probed successfully." This removes the doubled "and" from the previous punctuation correction. Wording is otherwise unchanged and all other fields are preserved.
- **Issue from this correction, now CORRECTED (2026-11-15):** the replacement had ended the sentence at "successfully.", so the text read "…was probed successfully. for 2023, 2024 and 2026; 2025 was not probed." On learner approval, "successfully. for 2023" was replaced with "successfully for 2023", preserving the original continuation. The sentence now reads "…was probed successfully for 2023, 2024 and 2026; 2025 was not probed." No other content changed.

### Human correction: Open-Meteo `contains_pii` (UC1 and UC2), 2026-11-15
- **Records changed:** `outputs/UC1/records/api.open_meteo_archive.json` and `outputs/UC2/records/api.open_meteo_archive.json`. In each, `declared_metadata.contains_pii` changed from `"no"` to `null`. Nothing else in either record changed.
- **Reason.** No source states personal-data or PII status for this API. The register entry has no such field, the profiler's tool results contain no PII key or personal-data wording, and the records' documentation, unknowns and provenance mention none. The value `"no"` was therefore a profiler inference, which the TC-022 rule (`declared_metadata` holds only stated flags) does not allow. It is recorded as unknown (`null`).
- **Effect.** `GOV-PII` fires only when `contains_pii` is `true`, so the change does not alter any rule flag. Assessments and memos were not regenerated.
- **Scope.** This is a human-approved correction. It is not a learner sign-off decision.
