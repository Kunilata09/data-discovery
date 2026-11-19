# Memo review: UC1 (air quality and traffic)

Reviewer: **KUNILATA MUDULI** (PENDING: learner to confirm; not verified)    
Review date: **15 November 2026** (PENDING: learner to confirm)   
Review time: **30 Mins** (PENDING: not measured; learner to measure or correct)

Decisions below are the learner's, as stated in the instruction that completed this review, except the FRS-STALE dismissal in 3.1 and section 4, which the assessor generated under calibration rule 5 (learner agreement not recorded). The assistant only transcribed them and checked each claim against `outputs/UC1/discovery_results.json`, `risk_assessment.json`, `rule_flags.json`, `feasibility_memo.md` and the records.

## 1. Overall verdict
- **Agree: `not_feasible`.** Driver: must needs N2 (hourly traffic) and N3 (humidity) are `partially_met`, with no candidate closing the gap (calibration rule 6).

## 2. Gate decisions (learner, `outputs/UC1/gate_decisions.json`)
| Link | Gate decision | Agent verdict | Review decision |
|---|---|---|---|
| `link.uci_360` (UCI Air Quality) | accept, N1 prototype | `feasible_with_conditions` | Agree with the verdict, with the override in section 3.1 |
| `link.europa_sdg_11_52_099aa6` (Eurostat PM2.5 deaths) | accept, N6 prototype only | `not_feasible` | Agree with the verdict; see 3.2 |
| `link.data_open_air_chicago_hour_aggre_d4970b` (Chicago) | accept, deliberate distractor | `not_feasible` (`ACC-UNREACHABLE`) | Agree: the refusal is the finding |

## 3. Per-source decisions

### 3.1 `link.uci_360`: UCI Air Quality, N1 prototype
- **Agree:** the missing-value limitation. The metadata declares `has_missing_values: no`, but -200 is the documented missing marker. This is `DQ-METADATA-CONTRADICTION` and `DQ-SENTINEL-VALUES`.
- **Agree:** the single-site limitation. It is one road-level device, `INT-REPRESENTATIVENESS`.
- **Dismissal (assessor-generated, calibration rule 5):** `FRS-STALE` is dismissed for this source in the regenerated assessment (`outputs/UC1/risk_assessment.json`, `discovery_results.json`). The prototype window is historical (it ends 2005-04-04) and is the only target window, so rule 5 applies. **Learner agreement: not recorded.**
- **Effect:** the verdict stays `feasible_with_conditions` for N1 prototype only. The dismissal is recorded in the generated `risk_assessment.json` and `discovery_results.json`, not as a learner override.

### 3.2 `link.europa_sdg_11_52_099aa6`: Eurostat PM2.5 deaths, N6
- **Agree:** the licence is unknown (`LIC-UNKNOWN`). The tool found no licence, so the reuse terms must be read at the source before any use.
- **Agree:** the window coverage is partial. The series runs 2005 to 2023 (annual), so it overlaps the prototype window only in 2005 and does not cover production (2024–2025). This is `COV-PARTIAL-WINDOW`.
- **Agree:** the verdict is `not_feasible` under calibration rule 7 (context source with a blocker). The learner accepted the link for prototype only, and that remains the only permitted use.

### 3.3 `link.data_open_air_chicago_hour_aggre_d4970b`: Chicago (distractor)
- **Agree:** `not_feasible`. The host is not allowlisted and was refused. The US geography does not fit the Italian study area.

### 3.4 Internal and register sources (N1 production, N2, N3, N4)
- **Agree:** N1 production is `feasible_with_conditions` (station readings), subject to access and the VR-03 status conflict (catalog active, wiki switched off on 2024-06-30).
- **Agree:** N2 is `partially_met`. There is no counter-to-station mapping, and the 2024-03-18 counting change is unadjusted. The traffic source cannot be used for production as it stands.
- **Agree:** N3 humidity has no production source. Open-Meteo is configured for temperature and shortwave radiation only, and the variables cannot be changed per call.
- **Agree:** N4 (`internal.clinic.resp_visits_daily`) is `feasible_with_conditions` for daily district counts only, under the clinic data policy.

## 4. Agreements and overrides (summary)
- **Agreements:** overall `not_feasible`; UCI missing-value and single-site limits; Eurostat licence uncertainty and partial coverage; Chicago refusal; N2 and N3 production gaps.
- **Assessor dismissal (not a learner override):** `FRS-STALE` for `link.uci_360`, under calibration rule 5. Verdict unchanged. **Learner agreement: not recorded.**

## 5. Sign-off recommendation
- **`proceed_with_conditions`, for the prototype only.** Production is not supported by the evidence (N2 and N3 humidity gaps). The conditions are in `outputs/UC1/signoff.json`.

## 6. Open items for the learner
- Confirm the VR-03 status with the Environment Monitoring Unit.
- Legal to resolve the UCI research-only note against CC BY 4.0, and the upstream Copernicus licence of the Open-Meteo data.
- Confirm the Valdena coordinates, as the Milan proxy is an assumption (`decisions.md`).
- Read the Eurostat reuse terms at the source.
- **Eurostat record finding (SUPERSEDED 2026-11-15).** The original finding, as recorded when the memo was first generated, was that the record's `has_missing_values: "no"` was inferred by the profiler, not declared by the source, and the memo repeated it (memo line 91). The TC-022 correction fixed the record (`declared_metadata` is now `{}`), and the regenerated memo no longer contains that sentence. Verdict unaffected. The history is in `decisions.md`, "Eurostat record findings" and the TC-022 correction entries.
- **Eurostat 2006 gap (preserved):** the series has no 2006 value (18 periods, 2005 and 2007–2023). The source is annual and the zero missing-cell count does not show this. Confirm whether the gap is a publication gap or a deliberate omission.
- **Holiday-API statements in the generated memo (documentation only, 2026-11-15).** `outputs/UC1/feasibility_memo.md` lines 164, 175 and 200 say the brief tags a holiday API for UC1. The learner's UC1 contract excludes it (`use_cases/UC1_air_quality.json`, `excluded_sources`, reason "Learner decision (2026-11-15): no UC1 need uses public holidays"). **The contract exclusion governs UC1.** The memo predates the exclusion, because the memo writer does not receive `excluded_sources`. **The generated memo has NOT been corrected or regenerated**; those three statements are outdated and must be read with the exclusion.
- **Pending learner inputs (not filled):** reviewer name, review date and review time on this page; the reviewer and the owner and due-date fields in `outputs/UC1/signoff.json`. Each is marked PENDING above or in `decisions.md`.
