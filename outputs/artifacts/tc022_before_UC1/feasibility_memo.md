## 1. Executive summary

**Overall verdict: not_feasible.** The use case cannot go to production on the current evidence. The prototype window is closer to workable, but its sources still carry conditions.

Facts driving the verdict:

1. **N2 (hourly traffic near stations) is partially met.** The only traffic source, `internal.traffic.hourly_counts`, has no counter-to-station mapping and no proof that counters are near stations. Counting changed on 2024-03-18 (per-direction before, both directions combined after), and the catalog does not mention it. The production window straddles that change.
2. **N3 (hourly humidity) has no production source.** Open-Meteo is configured for temperature and radiation only. No candidate supplies relative humidity for 2024–2025. The discovery record states no other candidate can close this gap, and that it would remain even if all access, licence and mapping conditions were cleared.
3. **N1 (hourly pollutants) is met with conditions in both windows.** Production uses `internal.airq.station_readings`, which needs warehouse access and a resolved status for station VR-03. The catalog says VR-03 is active and open-ended; the wiki says it was switched off on 2024-06-30. Prototype uses `link.uci_360`, which needs -200 cleaning and a licence note resolved.
4. **Both must-level gaps have no candidate, so calibration rule 6 sets the verdict to not_feasible.** N4 (should) and N6 (could) do not change the verdict. N5 (could, out of scope) was not searched for or opened.

## 2. Need coverage

| need id | need | priority | status | best source(s) | gap |
|---|---|---|---|---|---|
| N1 | Hourly air-pollutant concentrations | must | met_with_conditions | `internal.airq.station_readings` (production); `link.uci_360` (prototype) | Production: warehouse access, VR-03 status, no station coordinates, no validity flag. Prototype: -200 cleaning, research-only licence note, one device at one location. The Chicago link is not usable. |
| N2 | Hourly vehicle traffic near monitoring stations | must | partially_met | `internal.traffic.hourly_counts` | No counter-to-station mapping or proximity evidence. No documented adjustment for the 2024-03-18 change. No other traffic candidate. |
| N3 | Hourly temperature and humidity | must | partially_met | `api.open_meteo_archive` (temperature, both windows); `link.uci_360` (temperature and RH, prototype) | No humidity source for production. Open-Meteo is not configured for humidity. Location is not yet set for Valdena. |
| N4 | Daily respiratory clinic visits by district | should | met_with_conditions | `internal.clinic.resp_visits_daily` | Access not granted. Zero-count convention, district code list, diagnosis grouping and suppression rule undocumented. District cannot be joined to station geography. |
| N5 | Patient-level clinic visit records | could | unmet (out of scope) | none | Out of scope by brief. Nothing was searched for, opened or profiled. The clinic table is described as having no patient identifiers, and no N5 flag was raised. |
| N6 | National yearly context: PM2.5 deaths | could | unmet | `link.europa_sdg_11_52_099aa6` (not_feasible) | Licence unknown. Covers 2005 only, which is about 24% of the prototype window. No production years. |

Reader's note: the prototype window has candidate sources for its must needs (N1 and N3) through `link.uci_360` and `api.open_meteo_archive`, both with conditions. This is my reading of the need table. The overall verdict in the record is not_feasible and I have not changed it.

## 3. Source assessments

Ordered: with conditions first, then not feasible. No source was rated plain feasible.

### api.open_meteo_archive
- **What it is:** Open-Meteo historical weather API (reanalysis). Hourly temperature and shortwave radiation, UTC, one point per query. Catalog licence CC BY 4.0. Owner not stated.
- **Verdict:** feasible_with_conditions. N3 temperature only.
- **Flags:**
  - LIC-MIXED (major): the licence page lists C3S-derived reanalysis, but the upstream licence is not named.
  - COV-GEO-MISMATCH (major, judgement): the probe used grid point 45.448154, 9.169279 for query 45.4642, 9.19 (Milan area). The brief gives no Valdena coordinates.
  - LIC-ATTRIBUTION (minor): attribution required next to displayed data.
- **Probe result:** HTTP 200 for 2004-03-10 to 03-12 and 2024-01-01 to 01-03. Both windows are reachable.
- **Conditions:** Health Office to confirm Valdena coordinates and record them in `decisions.md`. Legal to sign off the C3S licence for production use. Convert UTC to Europe/Rome before joining. Not sufficient for humidity.

### internal.airq.station_readings
- **What it is:** Hourly NO2 and PM2.5 (µg/m³) from city monitoring stations, keyed by station_id and UTC hour. About 4.2 million rows. Coverage from 2023-01-01, open-ended, hourly refresh, last refreshed 2026-10-14. Owner: Environment Monitoring Unit. Internal licence.
- **Verdict:** feasible_with_conditions. Production N1 only.
- **Flags:**
  - ACC-RESTRICTED (major): auth required. Request pending ("not yet delivered per candidate brief").
  - GOV-CATALOG-WIKI-CONFLICT (major, judgement): catalog shows the network active with open-ended coverage. Wiki station_network (last edited 2024-07-01) says VR-03 was switched off on 2024-06-30.
  - INT-NO-JOIN-KEY (major, judgement): station codes are free text, with no coordinates or ISO codes.
- **Conditions:** warehouse access; VR-03 and other station status confirmed; station coordinates supplied; ts_utc and missing-hour convention confirmed; internal classification confirmed for use in the warning model.
- **Gap:** no 2004–2005 coverage, so prototype N1 depends on `link.uci_360`.

### internal.clinic.resp_visits_daily
- **What it is:** Daily respiratory visit counts by district, one row per day and district, with columns visit_date, district and visit_count. Coverage from 2022-01-01, open-ended, daily refresh, last refreshed 2026-10-14. Owner: Clinical Analytics. Internal licence. Wiki clinic_data_policy names it as the only permitted clinic source.
- **Verdict:** feasible_with_conditions. N4 (should), production window.
- **Flags:**
  - ACC-RESTRICTED (major): access request to Clinical Analytics. No data read.
  - DQ-UNDOCUMENTED-SCHEMA (major, judgement): no district code list, zero-count convention, diagnosis grouping or small-count suppression rule documented.
  - INT-NO-JOIN-KEY (major, judgement): district names are free text, not verified. Unclear whether "district" means residence or clinic location.
- **Conditions:** approval and delivery as aggregated daily district counts only, under the clinic policy. Schema, code list and suppression rule documented. Residence-versus-clinic meaning confirmed before any join.

### internal.traffic.hourly_counts
- **What it is:** Hourly vehicle counts per road counter, described in the catalog as near the monitoring stations. About 15 million rows. Coverage from 2021-01-01, open-ended, hourly refresh, last refreshed 2026-10-12. Owner: Mobility Office. Internal licence. Local time, zone not stated.
- **Verdict:** feasible_with_conditions. N2 (must), production window. The need is only partially met.
- **Flags:**
  - ACC-RESTRICTED (major): request to Mobility Office, status unknown.
  - GOV-CATALOG-WIKI-CONFLICT (major, judgement): wiki counter_replacement_2024 (last edited 2024-04-02) says counters were replaced on 2024-03-18 and counts are combined after that date. The catalog has no note on this.
  - DQ-SEMANTIC-ENCODING (major, judgement): per-direction before 2024-03-18, combined after. No direction field in the schema.
  - INT-NO-JOIN-KEY (major, judgement): no counter location field and no counter-to-station mapping.
- **Conditions:** access; counter locations or distances to stations; documented adjustment factor or overlap period; timezone confirmed and DST handled.

### link.uci_360
- **What it is:** UCI dataset 360, Air Quality. Hourly averages from one road-level chemical multisensor device in an unnamed Italian city, 2004-03-10 to 2005-04-04, 9,357 rows. Reference concentrations (CO, NMHC, benzene, NOx, NO2), five metal-oxide sensor responses, temperature, RH and absolute humidity. Licence CC BY 4.0 on the link. Owner not stated.
- **Verdict:** feasible_with_conditions. Prototype only. Provides N1 prototype and the only prototype RH.
- **Flags:**
  - DQ-METADATA-CONTRADICTION (major): declared has_missing_values "no", but documentation says -200 marks missing values. The sample confirms -200 in numeric columns.
  - DQ-SENTINEL-VALUES (major, judgement): -200 counts: CO 1,592; NOx 1,639; NO2 1,642; NMHC 8,443 of 9,357. The benzene minimum of -200 is not counted as missing.
  - INT-REPRESENTATIVENESS (major, judgement): one device, one road-level location, unnamed city. Not representative of 2024–2025.
  - INT-NO-JOIN-KEY (major, judgement): no station id, coordinates or district field.
  - GOV-PURPOSE-LIMITATION (major, judgement): metadata says research use only, commercial use excluded. This conflicts with CC BY 4.0. Commercial use is unknown.
  - FRS-STALE (major, rule): raised on data ending 2005-04-04, then dismissed by the rule because the target window ends at the same date.
  - LIC-ATTRIBUTION (minor): cite Vito and De Vito et al. 2008.
- **Conditions:** -200 treated as null, including benzene. Legal to resolve the research-only note against CC BY 4.0 and confirm operational warning use. Date format (DD/MM or MM/DD) confirmed; the sample parses month-first. Prototype use only.

### link.data_open_air_chicago_hour_aggre_d4970b
- **What it is:** A data.gov landing page, "Open Air Chicago hour aggregations". Described as hourly sensor data from a US city. Contents, period, licence, owner and formats are unverified.
- **Verdict:** not_feasible.
- **Flags:**
  - ACC-UNREACHABLE (blocker): catalog.data.gov returned DOMAIN_NOT_ALLOWLISTED. The record says no other route should be used.
  - LIC-UNKNOWN (blocker): no licence could be read.
  - COV-GEO-MISMATCH (major, judgement): US city; primary geography is Italy.
- **Note:** even if the host were allowlisted, the stated geography does not cover Valdena or Italy. No one can clear the blocker within scope.

### link.europa_sdg_11_52_099aa6
- **What it is:** Eurostat sdg_11_52 (ESTAT), premature deaths attributed to PM2.5, Italy only, annual, counts and rates. Populated 2005–2023, 18 periods, 36 cells, no missing values. Metadata last updated 2025-12-09. National context only.
- **Verdict:** not_feasible. N6 is a could-level need.
- **Flags:**
  - LIC-UNKNOWN (blocker): licence null. The copyright page redirected to an EU Login page. Not in the external register.
  - COV-PARTIAL-WINDOW (major, rule): covers about 24% of the prototype window. No production years.
  - GOV-OWNER-UNKNOWN (major, judgement): owner and steward null. Publisher stated as Eurostat (ESTAT) only.
- **Note:** the publisher terms might clear the licence, but the record does not carry this as a condition.

## 4. Red-flag register

| source_id | code | severity | evidence | raised by (rule or judgement) |
|---|---|---|---|---|
| api.open_meteo_archive | LIC-MIXED | major | Mixed sources; upstream C3S licence not named | rule |
| api.open_meteo_archive | COV-GEO-MISMATCH | major | Probe at 45.448154, 9.169279 (Milan area); no Valdena coordinates in brief | judgement |
| api.open_meteo_archive | LIC-ATTRIBUTION | minor | CC BY 4.0, attribution required next to displayed data | rule |
| internal.airq.station_readings | ACC-RESTRICTED | major | Auth required; request pending | rule |
| internal.airq.station_readings | GOV-CATALOG-WIKI-CONFLICT | major | Catalog open-ended; wiki says VR-03 switched off 2024-06-30 | judgement |
| internal.airq.station_readings | INT-NO-JOIN-KEY | major | Free-text station codes; no coordinates | judgement |
| internal.clinic.resp_visits_daily | ACC-RESTRICTED | major | Auth required; request to Clinical Analytics; no data read | rule |
| internal.clinic.resp_visits_daily | DQ-UNDOCUMENTED-SCHEMA | major | No code list, zero-count convention, diagnosis grouping or suppression rule | judgement |
| internal.clinic.resp_visits_daily | INT-NO-JOIN-KEY | major | Free-text districts; residence vs clinic unclear | judgement |
| internal.traffic.hourly_counts | ACC-RESTRICTED | major | Auth required; request status unknown | rule |
| internal.traffic.hourly_counts | GOV-CATALOG-WIKI-CONFLICT | major | Catalog silent on 2024-03-18 counter change; wiki documents it | judgement |
| internal.traffic.hourly_counts | DQ-SEMANTIC-ENCODING | major | Per-direction before, combined after 2024-03-18; no direction field | judgement |
| internal.traffic.hourly_counts | INT-NO-JOIN-KEY | major | No counter location or station mapping | judgement |
| link.uci_360 | DQ-METADATA-CONTRADICTION | major | Declared no missing values; documentation says -200 is missing | rule |
| link.uci_360 | DQ-SENTINEL-VALUES | major | -200 in CO, NOx, NO2, NMHC; benzene minimum not counted | judgement |
| link.uci_360 | INT-REPRESENTATIVENESS | major | One device, one location, 2004–2005 | judgement |
| link.uci_360 | INT-NO-JOIN-KEY | major | No station id, coordinates or district | judgement |
| link.uci_360 | GOV-PURPOSE-LIMITATION | major | Research-only note conflicts with CC BY 4.0; commercial use unknown | judgement |
| link.uci_360 | FRS-STALE | major | Rule raised; dismissed because target window ends at the same date | rule (dismissed) |
| link.uci_360 | LIC-ATTRIBUTION | minor | Citation required | rule |
| link.data_open_air_chicago_hour_aggre_d4970b | ACC-UNREACHABLE | blocker | DOMAIN_NOT_ALLOWLISTED | rule |
| link.data_open_air_chicago_hour_aggre_d4970b | LIC-UNKNOWN | blocker | No licence readable | rule |
| link.data_open_air_chicago_hour_aggre_d4970b | COV-GEO-MISMATCH | major | US city; not Italy | judgement |
| link.europa_sdg_11_52_099aa6 | LIC-UNKNOWN | blocker | Licence null; copyright page redirected to login | rule |
| link.europa_sdg_11_52_099aa6 | COV-PARTIAL-WINDOW | major | 2005 only of prototype; no production years | rule |
| link.europa_sdg_11_52_099aa6 | GOV-OWNER-UNKNOWN | major | Owner and steward null | judgement |

Scope and privacy: no N5 flag was raised. No patient-level source was found or opened.

## 5. Conditions and owners

| condition | source(s) | who can resolve it | blocking which need |
|---|---|---|---|
| Set Valdena coordinates; record in `decisions.md` (Milan default is not a decision) | api.open_meteo_archive | Valdena Civic Health Office | N3 (temperature) |
| Legal sign-off on upstream C3S licence for production use | api.open_meteo_archive | Legal / platform data steward | N3 (temperature) |
| Warehouse access to station readings | internal.airq.station_readings | Environment Monitoring Unit | N1 (production) |
| Confirm VR-03 and other station status | internal.airq.station_readings | Environment Monitoring Unit | N1 (production) |
| Station coordinates; ts_utc and missing-hour convention | internal.airq.station_readings | Environment Monitoring Unit | N1 (production), N2 and N3 joins |
| Classification permits warning-model use | internal.airq.station_readings | Data Protection Office / Environment Monitoring Unit | N1 (production) |
| Access, aggregated daily district counts only | internal.clinic.resp_visits_daily | Clinical Analytics; Data Protection Office (policy) | N4 |
| Document code list, zero-count rule, diagnosis grouping, suppression rule | internal.clinic.resp_visits_daily | Clinical Analytics | N4 |
| Confirm residence vs clinic location | internal.clinic.resp_visits_daily | Clinical Analytics | N4 join to stations |
| Access request | internal.traffic.hourly_counts | Mobility Office | N2 |
| Counter locations and counter-to-station mapping | internal.traffic.hourly_counts | Mobility Office | N2 (must; gap remains) |
| Documented adjustment for 2024-03-18 change | internal.traffic.hourly_counts | Mobility Office | N2 (production comparability) |
| Timezone of ts_local confirmed | internal.traffic.hourly_counts | Mobility Office; analytics team | N2 joins |
| Research-only note vs CC BY 4.0; operational use | link.uci_360 | Legal | N1 (prototype), N3 (prototype RH) |
| -200 treated as null; date format confirmed | link.uci_360 | analytics team; UCI documentation | N1 (prototype), N3 (prototype RH) |
| Humidity source for 2024–2025 | none | No candidate identified | N3 (production) |

## 6. Recommended next steps

1. **Decide the Valdena location first.** The Health Office confirms coordinates for Open-Meteo and for the station and traffic joins. Record the decision in `decisions.md`. The brief says the register default is Lisbon; the record says Milan. Neither is a client decision.
2. **Raise access requests now:**
   - Environment Monitoring Unit: station readings, with VR-03 status and station coordinates.
   - Clinical Analytics: aggregated daily district counts, with the schema items listed in section 5.
   - Mobility Office: traffic counts, with counter locations, a station mapping and the 2024-03-18 adjustment.
3. **Route the licence questions to Legal:** C3S upstream licence (Open-Meteo); research-only note against CC BY 4.0 (UCI 360).
4. **Decide the N3 humidity gap.** No production humidity source exists. The decision is whether the production model proceeds without humidity, or a new source is sourced outside this discovery. This decision is needed before profiling of production.
5. **Decide the N2 gap.** Traffic cannot be linked to stations or adjusted for the 2024 change on current evidence. Decide whether N2 is kept as a must need or re-scoped.
6. **Once the gate is passed, profile in this order:**
   - Station readings: check VR-03 and the missing-hour convention first.
   - Traffic: check the 2024-03-18 break and the timezone second.
   - UCI 360: apply the -200 rule and confirm date parsing before any other check.
   - Open-Meteo: confirm UTC-to-Rome conversion once coordinates are set.
7. **Do not pursue** the Chicago link (guardrail: host refused; the stated geography is outside Italy) or Eurostat as a must-need source. Do not search for N5 patient-level records.

## 7. Open questions for the human reviewer

1. Which city or coordinates is Valdena? The brief gives none. Does the Health Office accept the Milan-area probe in the meantime, or should coordinates be set first?
2. The brief says the register default is Lisbon, but the discovery record says Milan. Which is correct, and does it matter for the record?
3. Which station status is true for VR-03: active per the catalog, or switched off on 2024-06-30 per the wiki?
4. Has the Mobility Office request been raised? Its status is unknown.
5. Does Legal accept the Open-Meteo mixed C3S licence for production, and does the UCI research-only note permit warning use?
6. Is there a production humidity source the record does not mention? The record states none exists. Could the Open-Meteo register configuration be extended to relative humidity? The inputs do not say.
7. Is a prototype-only path acceptable to the client if the production gaps (N2, N3 humidity) are not closed?
8. Does the clinic "district" mean residence or clinic location?
9. The brief references `decisions.md`, which was not among the inputs. Has it been written?

---

## Human review gate

Draft generated by the discovery agents for UC1 on 2026-11-15T15:02:50Z (model claude-haiku-5-5). It is a draft for review, not a decision.

Before any profiling or pipeline work, the reviewer confirms:

- [ ] Each verdict is supported by the evidence cited
- [ ] Every licence was read at its source, and the attribution text is recorded
- [ ] Access requests for the feasible-with-conditions sources are raised with the named owners
- [ ] Consent and purpose limits are understood, and the target population is filtered accordingly

**Open questions:**

1. Which city or coordinates is Valdena? The brief gives none. Does the Health Office accept the Milan-area probe in the meantime, or should coordinates be set first?
2. The brief says the register default is Lisbon, but the discovery record says Milan. Which is correct?
3. Which station status is true for VR-03: active per the catalog, or switched off on 2024-06-30 per the wiki?
4. Has the Mobility Office request been raised? Its status is unknown in the record.
5. Does Legal accept the Open-Meteo mixed C3S licence for production use?
6. Does Legal accept that the UCI 360 research-only note permits operational warning use, given CC BY 4.0 on the link?
7. Is there a production relative humidity source the record does not mention? The record says none exists. The inputs do not say whether the Open-Meteo configuration could be extended to humidity.
8. Is a prototype-only path acceptable to the client if the production gaps (N2 and N3 humidity) are not closed?
9. Does the clinic 'district' field mean district of residence or clinic location?
10. The brief references decisions.md, which was not among the inputs. Has the location assumption been recorded there?

Reviewer: ____________________   Date: __________   Decision: proceed / proceed with conditions / stop
