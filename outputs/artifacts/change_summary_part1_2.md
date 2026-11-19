# Change summary: Part 1 (FRS-STALE documentation) and Part 2 (UC2 Nager metadata), 2026-11-15

Scope: documentation corrections, one validator field, two regression tests, one targeted profile (5 model calls). No assessment or memo regenerated. learner decisions unchanged. README not touched. test_learner_gaps.py identical to the bundle copy.

Validation: full suite 94 passed (see pytest_part_final.txt); learner_gaps 21 passed; check UC1 and UC2 no problems; secret scan clean.

Nager targeted profile evidence: outputs/artifacts/nager_before_UC2/ (pre-run copy of outputs/UC2, hashes in SHA256SUMS_before.txt).

Open items: Nager temporal block changed (end 2026-12-26 unsupported, grain daily->static) - decision needed; Open-Meteo contains_pii 'no' known issue remains.

## outputs/UC1/signoff.json
```diff
--- /tmp/part_before/signoff.json	2026-11-15 17:30:43.135035304 +0000
+++ outputs/UC1/signoff.json	2026-11-15 17:31:07.976704249 +0000
@@ -46,12 +46,7 @@
       "reason": "Agree the N3 humidity gap: the configured variables are temperature and shortwave radiation only, and no candidate supplies humidity for production."
     }
   ],
-  "overrides": [
-    {
-      "source_id": "link.uci_360",
-      "reason": "Dismiss the FRS-STALE flag under calibration rule 5, because the prototype window (2004-03-10 to 2005-04-04) is historical. The verdict stays feasible_with_conditions. The agent kept the flag and recorded no dismissal, so this override is recorded here and not in discovery_results.json."
-    }
-  ],
+  "overrides": [],
   "traced_conclusion": {
     "source_id": "internal.airq.station_readings",
     "record_field": "temporal.start",
```

## outputs/artifacts/review_UC1.md
```diff
--- /tmp/part_before/review_UC1.md	2026-11-15 17:30:43.135336116 +0000
+++ outputs/artifacts/review_UC1.md	2026-11-15 17:31:07.978275982 +0000
@@ -4,7 +4,7 @@
 Review date: **15 November 2026**   
 Review time: **30 Mins**
 
-Decisions below are the learner's, as stated in the instruction that completed this review. The assistant only transcribed them and checked each claim against `outputs/UC1/discovery_results.json`, `risk_assessment.json`, `rule_flags.json`, `feasibility_memo.md` and the records.
+Decisions below are the learner's, as stated in the instruction that completed this review, except the FRS-STALE dismissal in 3.1 and section 4, which the assessor generated under calibration rule 5 (learner agreement not recorded). The assistant only transcribed them and checked each claim against `outputs/UC1/discovery_results.json`, `risk_assessment.json`, `rule_flags.json`, `feasibility_memo.md` and the records.
 
 ## 1. Overall verdict
 - **Agree: `not_feasible`.** Driver: must needs N2 (hourly traffic) and N3 (humidity) are `partially_met`, with no candidate closing the gap (calibration rule 6).
@@ -21,8 +21,8 @@
 ### 3.1 `link.uci_360`: UCI Air Quality, N1 prototype
 - **Agree:** the missing-value limitation. The metadata declares `has_missing_values: no`, but -200 is the documented missing marker. This is `DQ-METADATA-CONTRADICTION` and `DQ-SENTINEL-VALUES`.
 - **Agree:** the single-site limitation. It is one road-level device, `INT-REPRESENTATIVENESS`.
-- **Override (learner decision):** dismiss `FRS-STALE` for this source. The prototype window is historical (it ends 2005-04-04), so calibration rule 5 applies. The agent kept the flag and listed no dismissal.
-- **Effect:** the verdict stays `feasible_with_conditions` for N1 prototype only. The dismissal is recorded here and in the sign-off, and `discovery_results.json` is not edited.
+- **Dismissal (assessor-generated, calibration rule 5):** `FRS-STALE` is dismissed for this source in the regenerated assessment (`outputs/UC1/risk_assessment.json`, `discovery_results.json`). The prototype window is historical (it ends 2005-04-04) and is the only target window, so rule 5 applies. **Learner agreement: not recorded.**
+- **Effect:** the verdict stays `feasible_with_conditions` for N1 prototype only. The dismissal is recorded in the generated `risk_assessment.json` and `discovery_results.json`, not as a learner override.
 
 ### 3.2 `link.europa_sdg_11_52_099aa6`: Eurostat PM2.5 deaths, N6
 - **Agree:** the licence is unknown (`LIC-UNKNOWN`). The tool found no licence, so the reuse terms must be read at the source before any use.
@@ -40,7 +40,7 @@
 
 ## 4. Agreements and overrides (summary)
 - **Agreements:** overall `not_feasible`; UCI missing-value and single-site limits; Eurostat licence uncertainty and partial coverage; Chicago refusal; N2 and N3 production gaps.
-- **Override:** dismiss `FRS-STALE` for `link.uci_360` under calibration rule 5. Verdict unchanged.
+- **Assessor dismissal (not a learner override):** `FRS-STALE` for `link.uci_360`, under calibration rule 5. Verdict unchanged. **Learner agreement: not recorded.**
 
 ## 5. Sign-off recommendation
 - **`proceed_with_conditions`, for the prototype only.** Production is not supported by the evidence (N2 and N3 humidity gaps). The conditions are in `outputs/UC1/signoff.json`.
```

## discovery_agent/agents.py
```diff
--- /tmp/part_before/agents.py	2026-11-15 17:30:43.136043973 +0000
+++ discovery_agent/agents.py	2026-11-15 17:31:22.124861386 +0000
@@ -164,9 +164,10 @@
                      [ids_exist, planned_vendors_accounted, candidates_in_scope, unmet_are_genuine_gaps, unmet_cover_every_gap])
 
 
-#: declared_metadata flags that the risk rules read as a publisher's own claim. A non-null value
-#: must come from a tool result that actually contains the key (TC-022).
-PUBLISHER_FLAGS_NEEDING_EVIDENCE = ("has_missing_values",)
+#: declared_metadata flags that the risk rules read as a publisher's own claim (GOV-PII reads contains_pii;
+#: DQ-METADATA-CONTRADICTION reads has_missing_values). A non-null value must come from a tool result that
+#: actually contains the key (TC-022; contains_pii added after the UC2 Nager record was found unsupported).
+PUBLISHER_FLAGS_NEEDING_EVIDENCE = ("has_missing_values", "contains_pii")
 
 
 def declared_flags_are_stated(payload: dict, evidence: frozenset) -> list[str]:
```

## tests/test_tc022_declared_metadata.py
```diff
--- /tmp/part_before/test_tc022_declared_metadata.py	2026-11-15 17:30:43.136369412 +0000
+++ tests/test_tc022_declared_metadata.py	2026-11-15 17:31:22.143521793 +0000
@@ -64,3 +64,15 @@
     payload = _payload({"has_missing_values": "no"})
     assert validate(payload, spec)                              # no evidence: rejected
     assert validate(payload, spec, frozenset({"has_missing_values"})) == []
+
+
+def test_unsupported_contains_pii_is_rejected_like_has_missing_values():
+    # UC2 Nager: the profiler wrote contains_pii "no" although no tool result states it.
+    errs = declared_flags_are_stated(_payload({"contains_pii": "no"}), frozenset(EUROSTAT_SUMMARY_KEYS_FIXTURE))
+    assert len(errs) == 1 and "contains_pii" in errs[0]
+
+
+def test_contains_pii_is_accepted_when_stated_or_null():
+    evidence = frozenset({"contains_pii"})   # internal catalog results carry this key
+    assert declared_flags_are_stated(_payload({"contains_pii": False}), evidence) == []
+    assert declared_flags_are_stated(_payload({"contains_pii": None}), frozenset()) == []
```

## outputs/artifacts/decisions.md
```diff
--- /tmp/part_before/decisions.md	2026-11-15 17:30:43.135612673 +0000
+++ outputs/artifacts/decisions.md	2026-11-15 17:33:44.152785267 +0000
@@ -60,7 +60,7 @@
 - **Rules written** (`prompts/risk_assessor.md`, section "Verdict calibration", 8 numbered rules, all in the file): 1 clearable blocker gives `feasible_with_conditions` with a named resolver. 2 uncleared blocker gives `not_feasible`. 3 a window miss with coverage of another required window gives a window-scoped `feasible_with_conditions`. 4 partial coverage is conditional. 5 staleness is dismissed when every target window is historical. 6 only `must` gaps set the overall verdict. 7 a context source with a blocker gives `not_feasible`. 8 major flags cap a source at `feasible_with_conditions`, and minor flags never change the verdict. The reasoning is in the file itself.
 - **Before / after status: NOT MEASURED.** No `--from-stage assess` run was made with the uncalibrated prompt, so no verdict change can be attributed to the calibration. The UC1 and UC2 runs used the calibrated prompt only. The "after" data in `outputs/UC1/` and `outputs/UC2/` is therefore a single calibrated result, not a before-and-after comparison.
 - **Observations from the calibrated runs** (checked against the files, not changed):
-  - *Rule 5 was not applied.* `link.uci_360` keeps the `FRS-STALE` flag (`outputs/UC1/discovery_results.json`). Its prototype window ends 2005-04-04, which is historical, so rule 5 says to dismiss it. `dismissed_rule_flags` is empty.
+  - *Rule 5 was not applied (superseded by the 2026-11-15 regeneration).* Pre-regeneration, `link.uci_360` kept the `FRS-STALE` flag (`outputs/UC1/discovery_results.json`). Its prototype window ends 2005-04-04, which is historical, so rule 5 says to dismiss it. `dismissed_rule_flags` is empty.
   - *Rule 7 was applied.* `link.europa_sdg_11_52_099aa6` is `not_feasible` because it is a context source with a blocker (`LIC-UNKNOWN`). The agent cites rule 7 for this. An earlier note in this session blamed rule 1 for the Eurostat verdict. That was wrong: rule 1 covers core sources and clearable blockers, and rule 7 covers context sources, which is the case here.
   - *Rule 7 also applied to UC2.* `api.nager_public_holidays` is `not_feasible` for the same reason.
   - *Rule 6 was applied.* UC1 and UC2 are both `not_feasible`, driven by must needs that are `partially_met` with no candidate closing the gap.
@@ -136,12 +136,12 @@
 - **Allowlist:** unchanged. `catalog.data.gov` is not on it, so the Chicago refusal will be recorded by the pipeline.
 
 ### Review and sign-off decisions (2026-11-15)
-- **UC1 review decisions (learner):** agree with overall `not_feasible`; agree with the UCI missing-value and single-site limits; **override: dismiss `FRS-STALE` for `link.uci_360` under G5 rule 5** (historical prototype window; verdict unchanged); agree with the Eurostat licence uncertainty and partial window coverage. Sign-off recommendation: `proceed_with_conditions`, prototype only.
+- **UC1 review decisions (learner):** agree with overall `not_feasible`; agree with the UCI missing-value and single-site limits; the `FRS-STALE` dismissal for `link.uci_360` under G5 rule 5 is **assessor-generated, not a learner override**, and learner agreement is not recorded (historical prototype window; verdict unchanged); agree with the Eurostat licence uncertainty and partial window coverage. Sign-off recommendation: `proceed_with_conditions`, prototype only.
 - **UC2 review decisions (learner):** agree with overall `not_feasible`; agree with the Open-Meteo conditions and the Nager licence and geography limits. Sign-off recommendation: `stop` until the blockers are resolved.
-- **The override is recorded, not applied.** `outputs/UC1/discovery_results.json` is unchanged. The dismissal appears in `outputs/UC1/signoff.json` and `outputs/artifacts/review_UC1.md`.
+- *Superseded:* "The override is recorded, not applied. `outputs/UC1/discovery_results.json` is unchanged." The regenerated `discovery_results.json` now carries the dismissal. Correction (2026-11-15): the dismissal is assessor-generated under rule 5; the sign-off `overrides` list is empty; learner agreement is not recorded.
 - **Reviewer identity and review time are placeholders** in both reviews and both sign-offs. The assistant did not supply them. The learner must replace them before submission. The self-check accepts any non-empty reviewer value, so it does not verify identity.
 - **Step 2b status:** four redirect URLs for UC1 N6 production (see "Source suggestions"). All four are PENDING LEARNER DECISION. An earlier version said three; the count was wrong. The publisher pages were not verified: they are not reachable through the allowlist, and the redirect targets were not followed. UC2 has no unmet needs.
-- **G5 calibration status:** unchanged from the earlier entry. No before-and-after run was made. The calibration observations are recorded and the rule 5 dismissal above is the learner's override, not a prompt change.
+- **G5 calibration status:** unchanged from the earlier entry. No before-and-after run was made. The calibration observations are recorded and the rule 5 dismissal above is assessor-generated (see the 2026-11-15 correction), not a learner override and not a prompt change.
 
 ### Eurostat record findings (`link.europa_sdg_11_52_099aa6`, UC1 N6), 2026-11-15
 These findings are recorded as they are. The profiler was not changed, and no model call was made to correct them.
@@ -232,7 +232,7 @@
 ### TC-022 addendum (2026-11-15): correction to the regeneration entry above
 - The regenerated assessment (`outputs/UC1/risk_assessment.json`, `discovery_results.json`) records a dismissal of `FRS-STALE` for `link.uci_360`, with the assessor's own reason ("Every target window ... is the prototype window ... Recorded per calibration rule 5."). The pre-fix assessment had no dismissal (`outputs/artifacts/tc022_before_UC1/risk_assessment.json`, `dismissed_rule_flags` absent).
 - The statement "red-flag codes unchanged" above is true for codes that are raised, but it omitted this dismissal. The dismissal arose from re-running the assessor, not from the TC-022 fix.
-- `signoff.json` and `review_UC1.md` say the agent kept the flag and that the learner's override is the only dismissal. Both now conflict with the regenerated record. Not edited here: the learner decides which statement stands.
+- `signoff.json` and `review_UC1.md` say the agent kept the flag and that the learner's override is the only dismissal. Both now conflict with the regenerated record. Not edited here: the learner decides which statement stands. *Resolved 2026-11-15 (Part 1):* both files now describe the dismissal as assessor-generated, with learner agreement not recorded.
 
 ### Clarification 2026-11-15: UC1 N6 Step 2b suggestions (TC-019)
 
@@ -243,3 +243,15 @@
 - **Not changed.** The redirect resolution details, the 2026-11-15 re-check (`outputs/artifacts/tc019_step2b_recheck.txt`), and the assistant's recommendation column. The recommendations are labelled as recommendations, not decisions.
 - **Needed from the learner.** For each UC1 N6 suggestion, either an accept, reject or revise decision with a reason in the learner's own words, or a statement that it remains undecided. Until then, UC1 N6 production stays unresolved.
 - **TC-019 status: NOT PASSED (pending learner decisions).** The rubric's TC-019 entry ("Not done (learner)") is still accurate.
+
+### Part 1 and Part 2 corrections, 2026-11-15 (FRS-STALE documentation; UC2 Nager metadata)
+
+**Part 1: FRS-STALE, `link.uci_360`.** The dismissal is assessor-generated under calibration rule 5. Its only target window is the prototype window (2004-03-10 to 2005-04-04), and it is in the regenerated `risk_assessment.json` and `discovery_results.json`. It is not a learner override. Changes: `outputs/UC1/signoff.json` `overrides` is now `[]` (the four agreements are unchanged); `outputs/artifacts/review_UC1.md` sections 3.1 and 4 describe the dismissal as assessor-generated, with "Learner agreement: not recorded"; the statements "rule 5 was not applied" and "override recorded, not applied" are marked superseded in this file. No assessment or memo was regenerated for this correction.
+
+**Part 2: UC2 Nager (`api.nager_public_holidays`).**
+- Before: `declared_metadata` = `{"has_missing_values": "unknown", "contains_pii": "no", ...}`. Neither value appears in any tool result for this source (checked against `outputs/artifacts/nager_before_UC2/transcripts/`).
+- Fix: `contains_pii` added to `PUBLISHER_FLAGS_NEEDING_EVIDENCE` in `discovery_agent/agents.py`; two regression tests added to `tests/test_tc022_declared_metadata.py`.
+- Targeted command run: `.venv/bin/python -m discovery_agent run --use-case UC2 --from-stage profile --stop-after profile --only api.nager_public_holidays --no-input` (5 model calls, exit 0).
+- After: `declared_metadata` = `{"has_missing_values": null, "contains_pii": null}`. Files that changed in `outputs/UC2/`: the Nager record, its profiler transcript, `run_history.jsonl`, `run_summary.json`, `trace.jsonl`. No other file changed. Rule flags were recomputed offline with `discovery_agent.risk_rules.evaluate`: before and after both give `LIC-UNKNOWN` only, so the flags are unchanged. No assess or memo run was made.
+- **Open issue, not resolved by this change.** The targeted profile also rewrote other parts of the Nager record, and the new `temporal` block is not supported by any provenance entry. `temporal.end` is now `2026-12-26`, a date after the as-of date (2026-10-15). It is the last holiday date in the probed responses, not a documented coverage end. `temporal.grain` changed from `daily` to `static`. The UC2 N4 need has `min_grain: daily`, so the grain change needs review if the rules are re-run. Decision needed: accept, restore the pre-run record from `outputs/artifacts/nager_before_UC2/` (which keeps the unsupported `has_missing_values` and `contains_pii` values), or re-profile with a validator rule for temporal coverage. No decision has been made here.
+- **Known unsupported metadata, unchanged records.** `contains_pii: "no"` remains in `outputs/UC1/records/api.open_meteo_archive.json` and `outputs/UC2/records/api.open_meteo_archive.json`. These records were not re-profiled. `contains_pii` drives no flag (`GOV-PII` fires only on `true`). The new validator rule would reject these values on re-profile.
```
