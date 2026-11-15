# UC2 Feasibility Memo: Ice-cream sales, weather and holidays

**Client:** Valdena Gelato Shop (fictional, northern Italy)
**As-of date:** 2026-10-15
**Status:** Initial feasibility assessment, metadata-based. No pipeline built. Only end-point samples were taken from the weather API. No internal data was accessed.

## 1. Executive summary

Overall verdict: **not feasible as scoped.** The must need N2 (mapping of product codes across the 2024 code change) is not met by any candidate source. The verdict would move to feasible with conditions if Retail Operations supplies an old-to-new product code mapping.

Facts that drive the verdict:

1. **N2 is unmet.** The wiki page `product_codes_2024` (edited 2024-04-02) says codes ending in "L" were replaced from 2024-04-01, and that no mapping table exists. `sales.products` lists only current codes (about 64 rows), has no validity dates, and names are not unique. Name matching is therefore ambiguous.
2. **N1 (daily sales by product) and N3 (daily max temperature) are met with conditions.** `sales.daily_by_product` is a daily table with coverage from 2022-01-01, last refreshed 2026-10-14. The Open-Meteo archive returned hourly data at the probed end-points of both windows. Neither source has been sampled in full.
3. **The sales history has a known gap.** The wiki says there are no sales rows from 2024-02-05 to 2024-03-10. The catalog says "no gap". The wiki is treated as more specific. The gap must be treated as missing, not zero.
4. **Access is untested and restricted.** The sales table is confidential and needs a request to Retail Operations. The calendar needs analytics-role access. Reachability was not tested for either.
5. **N4 (public holidays) is only partly met and is not feasible as a source.** The Nager.Date API returns national holidays only. Its licence is unknown. Per the discovery rules, it is recorded as context. This does not change the overall verdict because N4 is a should need.

## 2. Need coverage

| Need ID | Need | Priority | Status | Best source(s) | Gap |
|---|---|---|---|---|---|
| N1 | Daily ice-cream sales by product | must | met with conditions | internal.sales.daily_by_product; internal.store.calendar | Access restricted and untested. Gap 2024-02-05 to 2024-03-10 must be treated as missing. Closed-day representation unverified. |
| N2 | Mapping of product codes before and after the 2024 code change | must | **partially met (unmet for the verdict)** | internal.sales.products (partial aid only) | No old-to-new mapping exists in any source. Names are not unique. Pre-2024 codes are absent. |
| N3 | Daily maximum temperature | must | met with conditions | api.open_meteo_archive | No daily max variable is in the register, so it must be derived from hourly data. Timezone day boundary undecided. Shop coordinate not chosen. Upstream C3S terms unread. |
| N4 | Public holidays in Italy | should | partially met | api.nager_public_holidays (not feasible, context) | National holidays only. No regional, patron-saint or bridge days. 2025 not probed. Licence unknown. |
| N5 | Shop opening days and local events | should | partially met | internal.store.calendar | event_name completeness and history unverified. No source for regional or local events in northern Italy. Row count inconsistent with coverage. |

## 3. Source assessments

### internal.sales.daily_by_product
- **What it is:** Till-system table of units sold and revenue in euros, per product code per day. Owned by Retail Operations. Status active. Catalog grain daily, coverage from 2022-01-01 with no end date, daily refresh, last refreshed 2026-10-14, about 310,000 rows.
- **Verdict:** Feasible with conditions. Core source for N1. It cannot close N2.
- **Key flags:**
  - ACC-RESTRICTED (major). Auth required. Classification confidential. Request via Retail Operations. Reachability not tested.
  - GOV-CATALOG-WIKI-CONFLICT (major). Catalog says no gap. Wiki says no rows from 2024-02-05 to 2024-03-10 (edited 2024-03-12). Wiki treated as more specific.
  - INT-JOIN-KEY-MISMATCH (major). Codes re-keyed from 2024-04-01. No mapping table.
- **Conditions:** Confirm access and the role used for warehouse_sql. Record the gap in the catalog. Obtain an old-to-new code mapping. Confirm refund/void treatment, timezone, day cut-off, closed-day representation and export completeness for 2025-06 to 2026-03. Run a value-level sample once access is granted.

### internal.sales.products
- **What it is:** Static reference list of current product codes, names and categories. Owned by Retail Operations. About 64 rows. Last metadata update 2025-03-31.
- **Verdict:** Feasible with conditions as a partial aid. It does not meet N2 on its own.
- **Key flags:**
  - INT-JOIN-KEY-MISMATCH (major). No pre-2024 codes, no validity dates, no mapping. The wiki states it is not a mapping table. Names are not unique.
- **Conditions:** Obtain an authoritative old-to-new mapping, or confirm that retired "L" codes are absent from this list. Verify the table has not changed since 2025-03-31. Check name uniqueness. Verify analytics-role access.

### internal.store.calendar
- **What it is:** One row per calendar day for the shop, with an is_open flag and an optional event_name. Owned by Store Operations. Catalog grain daily, coverage from 2022-01-01, about 1,500 rows, weekly refresh, last refreshed 2026-10-10.
- **Verdict:** Feasible with conditions. Supports N1 by separating closed days from zero sales. Supports N5 only in part.
- **Key flags:**
  - ACC-RESTRICTED (major). Auth required. Classification internal. Open to analytics roles. Not tested.
  - Row count inconsistent with coverage. Catalog says about 1,500 rows. About 1,745 calendar days from 2022-01-01 to 2026-10-14. Not verified; no sample taken. (Judgement from catalog figures.)
- **Conditions:** Confirm analytics-role access. Verify row completeness. Confirm is_open on the 2024 till-outage days, and whether closed days are holiday closures or shop decisions. Confirm whether event_name is a full historical record or planned events, and whether public holidays are flagged. Confirm refresh coverage to 2026-03-31.

### api.open_meteo_archive
- **What it is:** Open-Meteo historical weather archive. Hourly reanalysis for one latitude and longitude. Variables temperature_2m (°C) and shortwave_radiation (W/m²). Licence recorded as CC BY 4.0 for API data. Upstream reanalysis is from Copernicus C3S under a separate licence.
- **Verdict:** Feasible with conditions. Core source for N3.
- **Key flags:**
  - LIC-MIXED (major). The API licence is CC BY 4.0. The upstream C3S licence was not read. Commercial use is recorded as unknown.
  - DQ-SEMANTIC-ENCODING (major, judgement). Hourly time is UTC (utc_offset_seconds 0). Europe/Rome calendar days do not match UTC days. Daily max must be derived and the day boundary decided.
  - LIC-ATTRIBUTION (minor). Required citation: "Weather data by Open-Meteo.com"; Zippenfenig, P., 2023, Zenodo, doi 10.5281/ZENODO.7970649; C3S as upstream.
- **Evidence and gaps:** Probes at 2023-06-01 and 2026-03-31 returned HTTP 200 with 72 hourly values each. The grid cell returned was 45.448154N, 9.169279E (147 m), not the query point. Only end-points and 3-day samples were probed. Full-window completeness is unverified. The register default is Milan (45.4642, 9.1900). The shop's city is not named in any source.
- **Conditions:** Legal to read the upstream C3S licence and confirm commercial use. Retain attribution. Derive daily max from hourly temperature_2m and document the day boundary in decisions.md. Choose and justify the shop coordinate. Check completeness across 2023-06-01 to 2026-03-31.

### api.nager_public_holidays
- **What it is:** Nager.Date REST endpoint for Italian public holidays by year (PublicHolidays/{year}/IT). About 13 to 14 national records per year. Start 2023-01-01. Refresh cadence unknown.
- **Verdict:** Not feasible (as context). Serves only N4, a should need.
- **Key flags:**
  - LIC-UNKNOWN (blocker, rule). Register agreement_status is "not_required_open_data". The terms URL is the code repo. The MIT licence seen covers the code, and the discovery record says it is not established that it covers the holiday data. Licence name null. Commercial use unknown. This conflicts with the register status.
  - COV-GEO-MISMATCH (major, judgement). National only. Regional and patron-saint days are not returned. No bridge days.
  - COV-PARTIAL-WINDOW (major, judgement). 2023, 2024 and 2026 were probed. 2025 was not probed, though the history window and recent window both include 2025.
- **Conditions:** None carried. If N4 remains needed, a licence-confirmed holiday source would need to be assessed as a new candidate.

## 4. Red-flag register

| Source ID | Code | Severity | Evidence | Raised by |
|---|---|---|---|---|
| internal.sales.daily_by_product | ACC-RESTRICTED | major | Auth required; confidential; request to Retail Operations; reachability not tested | rule |
| internal.sales.daily_by_product | GOV-CATALOG-WIKI-CONFLICT | major | Catalog: no gap. Wiki (2024-03-12): no rows 2024-02-05 to 2024-03-10. Wiki treated as more specific. | judgement |
| internal.sales.daily_by_product | INT-JOIN-KEY-MISMATCH | major | Wiki (2024-04-02): codes ending "L" replaced from 2024-04-01; no mapping table | judgement |
| internal.sales.products | INT-JOIN-KEY-MISMATCH | major | Wiki: lists only current codes; names not unique; no mapping | judgement |
| internal.store.calendar | ACC-RESTRICTED | major | Auth required; internal; analytics roles; not tested | rule |
| internal.store.calendar | Row count vs coverage (not a registered code) | major (proposed) | About 1,500 rows in catalog vs about 1,745 calendar days; not sampled | judgement (this memo) |
| api.open_meteo_archive | LIC-MIXED | major | API CC BY 4.0; upstream C3S licence not read; commercial use unknown | rule |
| api.open_meteo_archive | DQ-SEMANTIC-ENCODING | major | Hourly UTC; Europe/Rome days do not align | judgement |
| api.open_meteo_archive | LIC-ATTRIBUTION | minor | Required citation and upstream attribution | rule |
| api.nager_public_holidays | LIC-UNKNOWN | blocker | Register "not_required_open_data"; licence name null; commercial use unknown; conflicts with code licence | rule |
| api.nager_public_holidays | COV-GEO-MISMATCH | major | National only; no regional or patron-saint days | judgement |
| api.nager_public_holidays | COV-PARTIAL-WINDOW | major | 2025 not probed | judgement |

Note: The row-count flag for internal.store.calendar is not in the discovery record. It is raised here from catalog figures. It is listed in the discovery record as an unverified item.

## 5. Conditions and owners

| Condition | Source(s) | Who can resolve | Blocking which need |
|---|---|---|---|
| Provide an authoritative old-to-new product code mapping, or confirm retired codes are absent | internal.sales.products; internal.sales.daily_by_product | Retail Operations | N2 (must); overall verdict |
| Confirm access and reachability for warehouse_sql (sales) | internal.sales.daily_by_product | Retail Operations | N1 (must) |
| Confirm analytics-role access (calendar) | internal.store.calendar | Store Operations / Retail Operations | N1 (partly), N5 |
| Record the 2024-02-05 to 2024-03-10 gap as missing in the catalog | internal.sales.daily_by_product | Retail Operations (catalog owner) | N1 (must) |
| Confirm refund/void, timezone, day cut-off, closed-day representation, export completeness 2025-06 to 2026-03 | internal.sales.daily_by_product | Retail Operations | N1 (must) |
| Verify calendar row completeness and is_open on the outage days | internal.store.calendar | Store Operations | N1 (partly), N5 |
| Confirm event_name semantics and whether public holidays are flagged | internal.store.calendar | Store Operations | N5 (should) |
| Read the upstream C3S licence; confirm commercial use | api.open_meteo_archive | Legal / data owner | N3 (must) |
| Choose and justify the shop coordinate | api.open_meteo_archive | Valdena management; analyst | N3 (must) |
| Decide the day boundary; derive daily max; document in decisions.md | api.open_meteo_archive | Analyst | N3 (must) |
| Check full-window completeness of the archive (2023-06-01 to 2026-03-31) | api.open_meteo_archive | Analyst | N3 (must) |
| Confirm holiday data licence, or source a licence-confirmed alternative | api.nager_public_holidays | Legal / Retail Operations | N4 (should) |
| Probe 2025 holidays; confirm regional coverage gap | api.nager_public_holidays | Analyst | N4 (should) |
| Source regional or local event data for northern Italy, if needed | none identified | Valdena management | N5 (should) |

## 6. Recommended next steps

1. **Raise an access request to Retail Operations** for `sales.daily_by_product` and `sales.products`. Ask them to confirm reachability and the role for warehouse_sql.
2. **Ask Retail Operations for an old-to-new product code mapping** covering the 2024-04-01 change. This is the single item that moves the verdict. Ask them to say whether "L" codes are absent from the current list.
3. **Ask Retail Operations to record the 2024-02-05 to 2024-03-10 gap** in the catalog. The catalog and wiki currently disagree.
4. **Raise an access request to Store Operations** for `store.calendar`. Ask for row completeness, is_open semantics for the outage days, and event_name definitions.
5. **Ask Legal to read the upstream C3S licence** and confirm commercial use of the Open-Meteo reanalysis for this shop.
6. **Decide the shop coordinate** and record it in decisions.md. The current options are the register default (Milan) or the probed grid cell. Both are reanalysis grid points, not the shop.
7. **Decide the day boundary for daily max** (Europe/Rome vs UTC) and record it in decisions.md before any profiling.
8. **Decide whether N4 remains in scope.** If yes, find a licence-confirmed holiday source. Do not carry the Nager.Date API forward on its current licence status.
9. **Once the gates are passed, profile first:**
   - sales: the 2024 gap window, product-code counts before and after 2024-04-01, and refund/void and negative values;
   - calendar: row count against calendar days, and is_open on closed days;
   - weather: completeness and hourly-to-daily max derivation across both windows.

## 7. Open questions for the human reviewer

Numbered questions for people only. These are also returned in `open_questions_for_human`.

1. Does Retail Operations hold an old-to-new product code mapping for the 2024-04-01 change, or do the retired "L" codes not exist in any system? Until this is answered, the verdict stays not feasible.
2. Which city or exact address is the shop in? Is Milan the right default, or should the shop coordinate be set by management?
3. Can Legal confirm the commercial-use terms of the upstream Copernicus C3S reanalysis for a commercial shop?
4. Is the Nager.Date licence status ("not_required_open_data") correct? The register and the licence evidence disagree. Who can confirm the licence of the holiday data itself?
5. Is N4 (public holidays) still required if only national holidays are available? Does the owner accept national-only coverage?
6. Does Store Operations confirm that `event_name` is a full historical record, and that public holidays are flagged in the calendar?
7. Does the 2024-02-05 to 2024-03-10 gap reflect a till outage, or did the shop close? Were those days closed by decision or by holiday?
8. Is the calendar row count (about 1,500) consistent with the expected number of calendar days from 2022-01-01? The catalog suggests a gap or a sparse table.
9. The discovery record was generated on 2026-11-15, one month after the as-of date of 2026-10-15. Should the assessment be re-run against the as-of date, or is the later date acceptable?
10. Who is the analytics owner who will accept the access requests, and who signs off the decisions in decisions.md?

---

## Human review gate

Draft generated by the discovery agents for UC2 on 2026-11-15T15:07:09Z (model claude-haiku-5-5). It is a draft for review, not a decision.

Before any profiling or pipeline work, the reviewer confirms:

- [ ] Each verdict is supported by the evidence cited
- [ ] Every licence was read at its source, and the attribution text is recorded
- [ ] Access requests for the feasible-with-conditions sources are raised with the named owners
- [ ] Consent and purpose limits are understood, and the target population is filtered accordingly

**Open questions:**

1. Does Retail Operations hold an old-to-new product code mapping for the 2024-04-01 change, or do the retired 'L' codes not exist in any system? Until answered, the verdict stays not feasible.
2. Which city or exact address is the shop in? Is Milan the right default, or should management set the shop coordinate?
3. Can Legal confirm commercial-use terms for the upstream Copernicus C3S reanalysis used by Open-Meteo for a commercial shop?
4. The Nager.Date register status 'not_required_open_data' conflicts with the absence of a licence for the holiday data. Who can confirm the licence of the holiday data itself?
5. Is N4 (public holidays) still needed if only national holidays are available? Does the owner accept national-only coverage?
6. Does Store Operations confirm that event_name is a full historical record and that public holidays are flagged in the calendar?
7. Was the 2024-02-05 to 2024-03-10 gap a till outage, or did the shop close? Were those days closed by decision or by holiday?
8. Is the calendar row count (about 1,500) consistent with the expected number of calendar days from 2022-01-01? The catalog suggests a gap or a sparse table.
9. The discovery record was generated 2026-11-15, one month after the as-of date of 2026-10-15. Should the assessment be re-run against the as-of date, or is the later date acceptable?
10. Who is the analytics owner who will accept the access requests and sign off the decisions in decisions.md?

Reviewer: ____________________   Date: __________   Decision: proceed / proceed with conditions / stop
