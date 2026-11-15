# Walkthrough (draft)

> **STATUS: ASSISTANT DRAFT, LEARNER MUST REWRITE IN OWN WORDS.** The assistant wrote this from the project files so that every claim points to a real file and field. The learner's walkthrough must be in the learner's own words, and the learner must be able to explain each item in the 15-minute session. Do not submit this text as it stands.

## 1. One rule I wrote or accepted: calibration rule 7 (context source with a blocker)
- Where: `discovery_agent/prompts/risk_assessor.md`, section "Verdict calibration", rule 7. It reads: a context source with a blocker gives `not_feasible`, because conditions are not worth carrying for it.
- What it did in the UC1 run: `link.europa_sdg_11_52_099aa6` (Eurostat PM2.5 deaths, N6, national context) has the blocker `LIC-UNKNOWN`. The agent gave `not_feasible` and cited rule 7 (`outputs/UC1/discovery_results.json`, the source's `rationale`).
- Why it matters: the overall verdict is not affected, because N6 is a could need. The learner accepted this link for the prototype only at the gate (`outputs/UC1/gate_decisions.json`).

## 2. One claim in `signoff.json`, traced to its record field
- Source: `internal.airq.station_readings` (the UC1 station network).
- Record field: `temporal.start` in `outputs/UC1/records/internal.airq.station_readings.json`. Its value is `2023-01-01`.
- Claim: the station readings cannot serve the N1 prototype window (2004-03-10 to 2005-04-04), so the prototype N1 must come from the UCI link.
- What could change it: station readings for the prototype window are supplied (recorded in `DRAFT_signoff_UC1.json`, `traced_conclusion.could_change_if`).

## 3. One rejected source and why
- `link.data_open_air_chicago_hour_aggre_d4970b` (Chicago), accepted at the gate as a deliberate distractor.
- The host `catalog.data.gov` is not on `config/allowlist.json`. The guardrail refused it (`DOMAIN_NOT_ALLOWLISTED`, recorded in `outputs/UC1/trace.jsonl`), so the pipeline recorded it as `ACC-UNREACHABLE` and `not_feasible` (`outputs/UC1/discovery_results.json`).
- The refusal is the finding. The host was not added to the allowlist.

## 4. One memo conclusion
- From `outputs/UC1/feasibility_memo.md`, section 1, fact 2: "N3 (hourly humidity) has no production source. Open-Meteo is configured for temperature and radiation only."
- Source: `api.open_meteo_archive`. Its configured variables are `temperature_2m` and `shortwave_radiation`, in `config/external_sources_register.json`.
- The variable lock (`discovery_agent/tools/public_api.py`) stops a per-call change to these variables, so the gap cannot be closed from inside the pipeline.
- Effect: N3 is `partially_met`, a must need, and the overall UC1 verdict is `not_feasible` (calibration rule 6).

## Learner check before submission
- [ ] Rewrite sections 1–4 in own words.
- [ ] Confirm each file path and field exists.
- [ ] Remove the STATUS banner.
