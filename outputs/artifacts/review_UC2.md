# Memo review: UC2 (ice-cream sales, weather and holidays)

Reviewer: **KUNILATA MUDULI** (PENDING: learner to confirm; not verified)    
Review date: **15 November 2026** (PENDING: learner to confirm)   
Review time: **30 Mins** (PENDING: not measured; learner to measure or correct)

Decisions below are the learner's, as stated in the instruction that completed this review. The assistant checked each claim against `outputs/UC2/discovery_results.json`, `risk_assessment.json`, `rule_flags.json`, `feasibility_memo.md` and the records.

## 1. Overall verdict
- **Agree: `not_feasible`.** Driver: must need N2 (product sales across the 2024-04-01 code change) is `partially_met`. No source provides the old-to-new product code mapping (rule 6).

## 2. Source decisions

### 2.1 `internal.sales.products`: N2 product mapping
- **Agree:** this table cannot close N2 on its own. It has current codes only, no validity dates, and names that are not unique (its record has `quality_notes` stating this).
- **Blocker for N2:** an authoritative old-to-new product code mapping from Retail Operations.

### 2.2 `internal.sales.daily_by_product` and `internal.store.calendar`
- **Agree:** `feasible_with_conditions`, with access requests to Retail Operations and Store Operations (`ACC-RESTRICTED`) and the data gaps listed in their conditions. The 2024-02-05 to 2024-03-10 gap is treated as missing, not zero.

### 2.3 `api.open_meteo_archive`: N3 (temperature)
- **Agree:** `feasible_with_conditions`, with the conditions the agent listed. These are the upstream Copernicus C3S licence review for commercial use, attribution, deriving the daily maximum from hourly temperature, the shop coordinate, and a completeness check.
- **Agree:** the Milan coordinate is a proxy, and the shop coordinate must be set and justified.

### 2.4 `api.nager_public_holidays`: N4 (context)
- **Agree:** the licence is unknown (`LIC-UNKNOWN`) and the coverage is national only (`COV-GEO-MISMATCH`, `COV-PARTIAL-WINDOW`). Under calibration rule 7 the verdict is `not_feasible`. It is a should need, so the overall verdict does not depend on it.

## 3. Agreements and overrides (summary)
- **Agreements:** overall `not_feasible` driven by N2; Open-Meteo conditions; Nager licence and geography limits.
- **Overrides:** none.

## 4. Sign-off recommendation
- **`stop`, until the blockers are resolved.** Blockers: (1) the product code mapping for N2; (2) access to the sales and calendar tables; (3) the licence review of the upstream reanalysis for a commercial use. The sign-off records these in its traced conclusion and its agreements.

## 5. Open items for the learner
- Retail Operations: does an old-to-new product code mapping exist?
- Legal: commercial-use terms of the upstream Copernicus C3S reanalysis.
- The shop location and coordinate, to be set by management.
- Whether national-only holidays are acceptable for N4.
