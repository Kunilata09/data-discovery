## 1. Executive summary

**Overall verdict: not feasible for the production window today. The prototype can proceed on conditions.** The discovery output gives an overall verdict of `not_feasible`. Two must needs drive it: N3 (humidity) and N2 (traffic). N1 is met with conditions.

Facts that drive the verdict:

1. **Prototype (N1, N3) is usable with conditions.** `link.uci_360` covers 2004-03-10 to 2005-04-04 hourly, with NO2-type reference concentrations and relative humidity. It is one device in one unnamed city, uses a -200 missing code, and has a conflicting licence (CC BY 4.0 on the link, but "research purposes only" in the dataset notes). It is for prototype use only.
2. **Humidity gap in production.** No candidate gives relative humidity for 2024-2025. `api.open_meteo_archive` gives temperature only. The register does not configure humidity. The provider documentation was not read, so whether it offers humidity is unknown.
3. **Traffic (N2) is only partly met.** `internal.traffic.hourly_counts` is the only traffic source and covers the production window. Counter-to-station proximity is unverified and there is no key. The counting basis changed on 2024-03-18, which the catalog does not mention. Access is pending.
4. **City station data (N1, production) is conditional.** `internal.airq.station_readings` is open-ended and hourly, but access has not been granted. The wiki says VR-03 was switched off on 2024-06-30, which conflicts with the catalog's "active" status. No station coordinates exist, so there is no join key.
5. **Two sources are out.** The Chicago link is unreachable (DOMAIN_NOT_ALLOWLISTED), has no licence, and is outside IT. The Eurostat PM2.5 deaths series has no licence, covers about 24% of the prototype window and none of the production window. Patient-level records are out of scope and no such entry was among the candidates.

## 2. Need coverage

| need id | need | priority | status | best source(s) | gap |
|---|---|---|---|---|---|
| N1 | Hourly air-pollutant concentrations (NO2 / PM2.5) | must | met with conditions | link.uci_360 (prototype); internal.airq.station_readings (production) | uci_360 is one device, unnamed city, -200 missingness, licence conflict, prototype only. Station data needs access, confirmation of which stations report after 2024-06-30 (VR-03), and coordinates. Station data starts 2023-01-01, so it does not cover the prototype. |
| N2 | Hourly vehicle traffic near the monitoring stations | must | partially met | internal.traffic.hourly_counts | Proximity to stations unverified. No counter-to-station key. 2024-03-18 counting change needs adjustment. Time zone/DST undocumented. Access pending. |
| N3 | Hourly temperature and humidity | must | partially met | link.uci_360 (prototype, T and RH); api.open_meteo_archive (temperature, both windows) | No source gives relative humidity for 2024-2025. Open-Meteo has temperature only in the register. Open-Meteo location is unconfirmed. |
| N4 | Daily respiratory clinic visits by district | should | met with conditions | internal.clinic.resp_visits_daily | Purpose limit may not cover a live warning to patients. Access pending. Respiratory grouping, district code list, zero-count and suppression rules undocumented. No district key to places. |
| N5 | Patient-level clinic visit records | could | out of scope (unmet) | none | Out of scope by brief. Not searched for, opened or profiled. The aggregated clinic table does not substitute for it. |
| N6 | National yearly context: deaths linked to PM2.5 | could | unmet | link.europa_sdg_11_52_099aa6 (rated not feasible) | Licence unknown (blocker). About 24% of prototype window, no production coverage. Unit (rate) not stated. |

## 3. Source assessments

Order: sources with conditions first, then sources not feasible.

### link.uci_360
- **What it is:** Hourly averaged readings from one road-level chemical multisensor device in an unnamed Italian city. Holds reference concentrations (CO, NMHC, benzene, NOx, NO2), five sensor responses, temperature, relative humidity and absolute humidity. Sampled whole: 9,357 rows, 2004-03-10 to 2005-04-04. No traffic or clinic data.
- **Verdict:** feasible with conditions, prototype use only.
- **Key flags:**
  - DQ-METADATA-CONTRADICTION (major): declared has_missing_values "no", but the documentation and sample show -200 as the missing tag.
  - DQ-SENTINEL-VALUES (major): -200 is the missing code in several columns. C6H6(GT) has a minimum of -200 and 366 negative values that were not counted as missing.
  - GOV-PURPOSE-LIMITATION (major): CC BY 4.0 on the link, but the dataset notes say research use only. commercial_use unknown.
  - INT-REPRESENTATIVENESS (major): one device, one location, no station id or coordinates. Not representative of 2024-2025.
  - DQ-UNDOCUMENTED-SCHEMA (minor): dates documented DD/MM/YYYY but parse month-first. Sensor columns typed categorical but numeric. Coverage note says to February 2005, file runs to 2005-04-04.
  - FRS-STALE (major, rule) was dismissed for this source because all target windows are the prototype window.
- **Conditions:** Legal confirms whether the research-only note applies. Treat -200 as missing and confirm date format at profiling. Do not use for production. State the single-device, unnamed-city limit in any output. Apply the attribution text.

### api.open_meteo_archive
- **What it is:** Hourly gridded reanalysis from the Open-Meteo archive API for one point per query. Register configures temperature_2m and shortwave_radiation in UTC. Probes returned data for 2004-03-10 to 2004-03-12 and 2024-01-01 to 2024-01-03 (HTTP 200). No relative humidity, no traffic.
- **Verdict:** feasible with conditions, for N3 temperature only.
- **Key flags:**
  - COV-GEO-MISMATCH (major, judgement): the register default is Milan, and no client location has been chosen. The brief says the default is Lisbon. The probed grid point is 45.448154, 9.169279. Sources disagree on the default; both are recorded.
  - LIC-MIXED (major, rule): the licence page cites Copernicus C3S as upstream, with no upstream licence link named.
  - LIC-ATTRIBUTION (minor, rule): CC BY 4.0, attribution required next to displayed data.
  - INT-REPRESENTATIVENESS (minor, judgement): modelled values, not established at street or station level.
- **Conditions:** Legal signs off the C3S licence before production use. Client coordinates are set and recorded. Full archive start/end and refresh lag confirmed (unknown beyond 3-day probes). Convert UTC to Europe/Rome before joining. Check provider documentation for humidity; if absent, N3 humidity stays unmet for production.

### internal.airq.station_readings
- **What it is:** Hourly NO2 and PM2.5 (ug/m3) from city monitoring stations, keyed by station_id and UTC hour start. About 4.2 million rows per catalog. Coverage from 2023-01-01, open-ended, hourly refresh (catalog last refreshed 2026-10-14). Owner: Environment Monitoring Unit. Access by warehouse request. No data sampled or delivered.
- **Verdict:** feasible with conditions, for N1 production.
- **Key flags:**
  - ACC-RESTRICTED (major, rule): auth required, internal classification, request not yet delivered.
  - GOV-CATALOG-WIKI-CONFLICT (major, judgement): catalog says "active" with open-ended coverage. Wiki station_network (last edited 2024-07-01) says VR-03 was switched off 2024-06-30. The catalog is newer, but this does not prove all stations report to the present.
  - INT-NO-JOIN-KEY (major, judgement): free-text station codes, no coordinates or ISO codes.
- **Conditions:** access granted and table tested as reachable. Environment Monitoring Unit confirms which stations report 2024-01-01 to 2025-12-31 and VR-03 status. Coordinates supplied. Sample profiling for negatives, sentinel codes and missing hours (validation status undocumented). UTC handling confirmed.

### internal.clinic.resp_visits_daily
- **What it is:** Daily counts of respiratory clinic visits per district (visit_date, district, visit_count). Catalog says no patient identifiers. Owner: Clinical Analytics. Coverage from 2022-01-01, open-ended, daily refresh (last refresh 2026-10-14). The wiki clinic data policy names it as the only permitted clinic source for surveillance analysis.
- **Verdict:** feasible with conditions, for N4 (should, context).
- **Key flags:**
  - ACC-RESTRICTED (major, rule): auth required, request to Clinical Analytics.
  - GOV-PURPOSE-LIMITATION (major, judgement): the policy (owner Data Protection Office, last edited 2025-02-01) allows only daily district counts for "surveillance analysis". A live warning to clinic patients may be outside that purpose.
  - INT-NO-JOIN-KEY (major, judgement): district is free text, no code list, no district-to-station or grid key.
  - DQ-UNDOCUMENTED-SCHEMA (major, judgement): no respiratory diagnosis grouping, zero-count convention, district code list or small-count suppression rule.
- **Conditions:** Data Protection Office confirms in writing that a live warning is within the policy purpose. Clinical Analytics confirms aggregated daily counts only, grants access, and documents grouping, codes, zero counts and suppression. District-to-station or district-to-grid key agreed.

### internal.traffic.hourly_counts
- **What it is:** Hourly vehicle counts per road counter, described in the catalog as near the monitoring stations. About 15 million rows. Coverage from 2021-01-01, open-ended, hourly refresh (last refreshed 2026-10-12). Owner: Mobility Office (steward Luca Ferri per catalog). Access by warehouse SQL request. Data not accessed.
- **Verdict:** feasible with conditions per the source record, but N2 is only partly met until proximity is confirmed.
- **Key flags:**
  - ACC-RESTRICTED (major, rule): request status unknown.
  - GOV-CATALOG-WIKI-CONFLICT (major, judgement): wiki counter_replacement_2024 (last edited 2024-04-02) says counters were replaced 2024-03-18 and counting changed from per-direction to combined. It warns not to compare across the change without adjustment. The catalog shows coverage from 2021-01-01 with no break.
  - INT-NO-JOIN-KEY (major, judgement): no sensor location or distance field. The counter-to-station mapping is "not available". Proximity is unverified.
  - DQ-DST-ARTEFACTS (minor, judgement): ts_local is "local time (zone not stated)". DST handling not documented.
- **Conditions:** access granted. Counter locations and distances to each station confirmed. The 2024-03-18 adjustment factor or an overlap period provided, or the analysis adjusts for it. Time zone and DST confirmed. Missing-hour or outage rates per counter, if available.

### link.europa_sdg_11_52_099aa6
- **What it is:** Eurostat SDG 11.52 series: premature deaths attributed to PM2.5, Italy only, annual. JSON-stat API, 18 time points 2005-2023 with 36 cells. 2006 absent. No district, station or hourly grain.
- **Verdict:** not feasible (rule 7: a blocker on a context source means not feasible).
- **Key flags:**
  - LIC-UNKNOWN (blocker, rule): licence page redirected to EU Login with no licence text. Licence and commercial use unknown.
  - COV-PARTIAL-WINDOW (major, rule): record 2005-01-01 to 2023-12-31 covers about 24% of the prototype window. No production coverage.
  - DQ-UNDOCUMENTED-SCHEMA (major, judgement): unit RT (rate) not stated in the API summary. 2006 missing with no cause given.
- **Conditions:** none recorded. Not a must need; no effect on overall verdict.

### link.data_open_air_chicago_hour_aggre_d4970b
- **What it is:** Human-supplied data.gov link to "Open Air Chicago hour aggregations", described as hourly sensor data from a US city. Contents, period, licence, owner and formats unverified.
- **Verdict:** not feasible.
- **Key flags:**
  - ACC-UNREACHABLE (blocker, rule): catalog.data.gov returned DOMAIN_NOT_ALLOWLISTED. The platform owner would need to add the host. No other route should be used.
  - LIC-UNKNOWN (blocker, rule): no licence could be read.
  - COV-GEO-MISMATCH (major, judgement): US city, outside IT. Would not cover the client's stations or districts even if reachable.
- **Conditions:** none can be cleared within the project. Superseded for N1 prototype by uci_360.

## 4. Red-flag register

| source_id | code | severity | evidence | raised by (rule or judgement) |
|---|---|---|---|---|
| link.uci_360 | DQ-METADATA-CONTRADICTION | major | has_missing_values "no" declared; documentation and sample show -200 | rule |
| link.uci_360 | DQ-SENTINEL-VALUES | major | -200 missing code in CO(GT) 83% non-missing, NOx(GT) 82.5%, NMHC(GT) 9.8% usable; C6H6(GT) min -200, 366 negatives | judgement |
| link.uci_360 | GOV-PURPOSE-LIMITATION | major | CC BY 4.0 vs "research purposes only" in dataset notes; commercial_use unknown | judgement |
| link.uci_360 | INT-REPRESENTATIVENESS | major | one device, one location, unnamed city; not representative of 2024-2025 | judgement |
| link.uci_360 | LIC-ATTRIBUTION | minor | CC BY 4.0; attribution required | rule |
| link.uci_360 | DQ-UNDOCUMENTED-SCHEMA | minor | DD/MM/YYYY documented, month-first parse; categorical sensor columns; coverage note mismatch | judgement |
| link.uci_360 | FRS-STALE | major | data ends 2005-04-04 (rule). Dismissed for prototype-only use per calibration rule 5 | rule (dismissed) |
| api.open_meteo_archive | COV-GEO-MISMATCH | major | register default Milan; brief says Lisbon; probed point 45.448154, 9.169279; no client location chosen | judgement |
| api.open_meteo_archive | LIC-MIXED | major | upstream Copernicus C3S, licence link not named | rule |
| api.open_meteo_archive | LIC-ATTRIBUTION | minor | CC BY 4.0; attribution next to displayed data | rule |
| api.open_meteo_archive | INT-REPRESENTATIVENESS | minor | modelled grid point; not established at station/street level | judgement |
| internal.airq.station_readings | ACC-RESTRICTED | major | auth required; request not yet delivered | rule |
| internal.airq.station_readings | GOV-CATALOG-WIKI-CONFLICT | major | catalog "active", open-ended; wiki says VR-03 off 2024-06-30 | judgement |
| internal.airq.station_readings | INT-NO-JOIN-KEY | major | free-text station codes; no coordinates | judgement |
| internal.clinic.resp_visits_daily | ACC-RESTRICTED | major | auth required; request to Clinical Analytics | rule |
| internal.clinic.resp_visits_daily | GOV-PURPOSE-LIMITATION | major | policy allows daily district counts for surveillance; live warning may fall outside | judgement |
| internal.clinic.resp_visits_daily | INT-NO-JOIN-KEY | major | district free text; no code list or key | judgement |
| internal.clinic.resp_visits_daily | DQ-UNDOCUMENTED-SCHEMA | major | no respiratory grouping, zero-count rule, code list or suppression rule | judgement |
| internal.traffic.hourly_counts | ACC-RESTRICTED | major | auth required; request status unknown | rule |
| internal.traffic.hourly_counts | GOV-CATALOG-WIKI-CONFLICT | major | counting basis changed 2024-03-18 (wiki); catalog silent | judgement |
| internal.traffic.hourly_counts | INT-NO-JOIN-KEY | major | no counter location or distance; counter-to-station mapping not available | judgement |
| internal.traffic.hourly_counts | DQ-DST-ARTEFACTS | minor | ts_local zone not stated; DST undocumented | judgement |
| link.europa_sdg_11_52_099aa6 | LIC-UNKNOWN | blocker | licence page redirects to EU Login; no licence text | rule |
| link.europa_sdg_11_52_099aa6 | COV-PARTIAL-WINDOW | major | 2005-01-01 to 2023-12-31; about 24% of prototype; no production | rule |
| link.europa_sdg_11_52_099aa6 | DQ-UNDOCUMENTED-SCHEMA | major | unit RT not stated; 2006 absent, no cause | judgement |
| link.data_open_air_chicago_hour_aggre_d4970b | ACC-UNREACHABLE | blocker | DOMAIN_NOT_ALLOWLISTED on catalog.data.gov | rule |
| link.data_open_air_chicago_hour_aggre_d4970b | LIC-UNKNOWN | blocker | no licence readable | rule |
| link.data_open_air_chicago_hour_aggre_d4970b | COV-GEO-MISMATCH | major | US city; outside IT | judgement |

## 5. Conditions and owners

| condition | source(s) | who can resolve it | blocking which need |
|---|---|---|---|
| Relative humidity source for 2024-2025 (check provider docs; add to register if available) | api.open_meteo_archive | discovery team (register owner) | N3 (production) |
| Legal sign-off on upstream C3S licence and attribution wording | api.open_meteo_archive | Valdena Health Office Legal | N3 (production) |
| Set and record client coordinates (replace Milan default; resolve Lisbon/Milan discrepancy) | api.open_meteo_archive | Valdena Health Office project lead | N3 (both windows) |
| Confirm research-only note and licence conflict for uci_360 | link.uci_360 | Valdena Health Office Legal | N1 (prototype) |
| Warehouse access to station readings | internal.airq.station_readings | Environment Monitoring Unit | N1 (production) |
| Confirm reporting stations 2024-2025 and VR-03 status after 2024-06-30 | internal.airq.station_readings | Environment Monitoring Unit | N1 (production) |
| Station coordinates for joins | internal.airq.station_readings | Environment Monitoring Unit | N1, N2, N3 joins |
| Access to traffic counts | internal.traffic.hourly_counts | Mobility Office | N2 |
| Counter locations and distance to each station | internal.traffic.hourly_counts | Mobility Office | N2 |
| 2024-03-18 adjustment factor or overlap period | internal.traffic.hourly_counts | Mobility Office | N2 |
| Time zone and DST handling for ts_local | internal.traffic.hourly_counts | Mobility Office | N2 joins |
| Written confirmation that a live warning is within clinic data policy purpose | internal.clinic.resp_visits_daily | Data Protection Office | N4 (live warning use) |
| Access and confirmation of aggregated-only delivery | internal.clinic.resp_visits_daily | Clinical Analytics | N4 |
| Respiratory grouping, district code list, zero-count and suppression rules | internal.clinic.resp_visits_daily | Clinical Analytics | N4 |
| District-to-station or district-to-grid key | internal.clinic.resp_visits_daily; internal.airq.station_readings; api.open_meteo_archive | Valdena Health Office project lead, with city | N4 join to N1/N3 |
| Pick UTC vs local-time conversion (Europe/Rome) for all joins | api.open_meteo_archive; internal.airq.station_readings; internal.traffic.hourly_counts | discovery team at profiling | N1, N2, N3 |
| Treat -200 as missing; confirm month-first date format | link.uci_360 | discovery team at profiling | N1 (prototype) |
| Upstream licence and unit for Eurostat series | link.europa_sdg_11_52_099aa6 | Eurostat / Valdena Legal | N6 (not feasible; no path without licence) |
| Platform allowlist for catalog.data.gov | link.data_open_air_chicago_hour_aggre_d4970b | platform owner | none (superseded by uci_360) |

## 6. Recommended next steps

1. **Gate the prototype now.** Ask Valdena Health Office Legal to review the uci_360 research-only note and licence conflict, and to set the attribution. Once cleared, profile uci_360 for the prototype, treating -200 as missing and confirming the date format.
2. **Record the location assumption.** Set and record client coordinates in `decisions.md`, and reconcile the Milan register default with the Lisbon default cited in the brief. Use these coordinates in the Open-Meteo call.
3. **Raise access requests** to Environment Monitoring Unit (station readings), Mobility Office (traffic counts), Clinical Analytics (clinic daily counts) and Data Protection Office (purpose confirmation). Track the traffic request status, which is unknown.
4. **Resolve the humidity gap.** Check the Open-Meteo provider documentation for relative humidity. If it is not available, record N3 humidity for production as unmet. Decide whether to find another source or accept the gap. Do not assume a source exists.
5. **Ask the Mobility Office** for counter locations, distances to stations, the 2024-03-18 adjustment, and the time zone/DST behaviour. Without these, N2 stays partly met.
6. **Ask the Environment Monitoring Unit** which stations reported in 2024-2025, the status of VR-03, and station coordinates.
7. **Once access is passed, profile first:** (a) the station readings sample for negatives, sentinel codes and missing hours; (b) the traffic counts around 2024-03-18 to size the discontinuity; (c) the clinic daily counts for zero-count and suppression behaviour. Check time zones on all three before any join.
8. **Do not pursue** the Chicago link (host refused, no licence) or the Eurostat series (no licence, no production coverage) without a new decision. Do not search for or open patient-level records.
9. **Holiday API.** The brief tags a holiday API for this use case, but no record for it was in the discovery results. Assess it separately if it is needed.

## 7. Open questions for the human reviewer

1. Which location should the Open-Meteo call use? The register default is Milan (45.4642, 9.19) per the source summary, the discovery flag cites a probed point of 45.448154, 9.169279, and the brief says the register default is Lisbon. Which is the client's city, and which default is correct?
2. Does the Health Office accept that a live warning to clinic patients is within the clinic data policy's "surveillance analysis" purpose, or does the Data Protection Office need to rule on it?
3. Does Legal accept the uci_360 research-only note for a method-building prototype, or must the prototype use another public source?
4. Is there a source for relative humidity covering 2024-2025? If not, is the N3 humidity gap acceptable for the production model, or should the production scope change?
5. Is VR-03 still operating after 2024-06-30, and are any other stations still reporting? Only the Environment Monitoring Unit can answer.
6. Were the traffic counters near the monitoring stations? Only the Mobility Office can confirm.
7. Was the traffic request status ever recorded? Has the request been submitted, and by whom?
8. Should the holiday API tagged in the register be assessed for this use case?
9. Is a national PM2.5 context series (N6) needed at all, given that the only candidate has no licence?

---

## Human review gate

Draft generated by the discovery agents for UC1 on 2026-11-15T17:05:30Z (model claude-haiku-5-5). It is a draft for review, not a decision.

Before any profiling or pipeline work, the reviewer confirms:

- [ ] Each verdict is supported by the evidence cited
- [ ] Every licence was read at its source, and the attribution text is recorded
- [ ] Access requests for the feasible-with-conditions sources are raised with the named owners
- [ ] Consent and purpose limits are understood, and the target population is filtered accordingly

**Open questions:**

1. Which location should the Open-Meteo call use? The register default is Milan (45.4642, 9.19) per the source summary, the discovery flag cites a probed point of 45.448154, 9.169279, and the brief says the register default is Lisbon. Which is the client's city, and which default is correct?
2. Does the Health Office accept that a live warning to clinic patients is within the clinic data policy's 'surveillance analysis' purpose, or does the Data Protection Office need to rule on it?
3. Does Legal accept the uci_360 research-only note for a method-building prototype, or must the prototype use another public source?
4. Is there a source for relative humidity covering 2024-2025? If not, is the N3 humidity gap acceptable for the production model, or should the production scope change?
5. Is VR-03 still operating after 2024-06-30, and are any other stations still reporting? Only the Environment Monitoring Unit can answer.
6. Were the traffic counters near the monitoring stations? Only the Mobility Office can confirm.
7. Has the traffic data access request been submitted, and by whom? Its status is recorded as unknown.
8. Should the holiday API tagged in the register for this use case be assessed? No record for it appeared in the discovery results.
9. Is a national PM2.5 context series (N6) needed at all, given that the only candidate has no licence?

Reviewer: ____________________   Date: __________   Decision: proceed / proceed with conditions / stop
