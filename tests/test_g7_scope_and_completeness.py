"""G7 follow-up: contract-driven exclusions, unmet-needs completeness, and out-of-scope candidates.

The expected values come from the use-case contract and the register, not from fixed answers.
"""
from __future__ import annotations

from discovery_agent.agent import validate
from discovery_agent.agents import planner_spec, scout_spec
from discovery_agent.config import load_register
from discovery_agent.guards import excluded_sources
from discovery_agent.tools import ToolContext, execute
from discovery_agent.trace import Trace

NAGER = "api.nager_public_holidays"
METEO = "api.open_meteo_archive"
PATIENT_ENTRY = "internal.clinic.patient_visits"
DAILY_ENTRY = "internal.clinic.resp_visits_daily"


def _ctx(uc, settings):
    return ToolContext(use_case=uc, settings=settings, http=None, trace=Trace(None), agent="test")


def _plan(uc, mapping=None):
    mapping = mapping or {}
    return {"use_case": uc["id"], "objective_summary": "x" * 60,
            "need_plans": [{"need_id": n["id"], "interpretation": n["name"], "internal_queries": ["q"],
                            "external_data_hints": [], "register_ids": mapping.get(n["id"], []),
                            "acceptance_criteria": ["covers the window"]} for n in uc["needs"]],
            "open_questions": []}


def _required(uc):
    return {(n["id"], w) for n in uc["needs"] for w in n["windows"]}


def _cand(sid, kind, need_ids, windows, title="t"):
    return {"source_id": sid, "kind": kind, "title": title, "need_ids": need_ids, "target_windows": windows,
            "why_relevant": "test", "found_via": "test"}


def _submit(cands, unmet, rejected=None):
    out = {"candidates": cands, "searches_run": ["q"], "unmet_needs": unmet}
    if rejected is not None:
        out["rejected_without_profiling"] = rejected
    return out


def _errors(payload, spec):
    return validate(payload, spec)


# -- 1. contract-driven exclusion of the UC1 holiday API ----------------------------------------
def test_uc1_contract_excludes_the_holiday_api(uc1):
    assert NAGER in excluded_sources(uc1)
    assert excluded_sources(uc1)[NAGER].strip()


def test_excluded_source_cannot_be_mapped_to_a_need(uc1, settings):
    errs = _errors(_plan(uc1, mapping={"N4": [NAGER]}), planner_spec(uc1, settings))
    assert any(NAGER in e and "excluded for UC1" in e and "Do not map it" in e for e in errs)


def test_scout_cannot_submit_an_excluded_source_as_a_candidate(uc1, settings):
    cand = _cand(NAGER, "public_api", ["N4"], ["production"], "Nager holidays")
    errs = _errors(_submit([cand], _full_unmet(uc1, {("N4", "production")})), scout_spec(uc1, settings, _plan(uc1)))
    assert any(NAGER in e and "excluded for UC1" in e and "Do not submit it" in e for e in errs)


def test_excluded_source_is_annotated_in_the_register_listing(uc1, settings):
    ok, res = execute("list_external_register", {}, _ctx(uc1, settings))
    by_id = {s["id"]: s for s in res["sources"]}
    assert ok and by_id[NAGER]["excluded_by_use_case"]
    assert "excluded_by_use_case" not in by_id[METEO]


def test_excluded_source_cannot_be_called(uc1, settings):
    ok, payload = execute("call_public_api", {"source_id": NAGER}, _ctx(uc1, settings))
    assert not ok and "excluded for UC1" in str(payload)


def test_holiday_api_stays_available_for_uc2(uc2, settings):
    assert excluded_sources(uc2) == {}
    need = uc2["needs"][0]
    assert NAGER in {s["id"] for s in load_register("UC2")}
    errs = _errors(_plan(uc2, mapping={need["id"]: [NAGER]}), planner_spec(uc2, settings))
    assert not any("excluded" in e for e in errs)
    cand = _cand(NAGER, "public_api", [need["id"]], [need["windows"][0]], "Nager holidays")
    # Completeness is not what this test checks: list every other required gap so only the exclusion rule can speak.
    unmet = [f"{n} {w}: no source" for n, w in sorted(_required(uc2) - {(need["id"], need["windows"][0])})]
    errs = _errors(_submit([cand], unmet), scout_spec(uc2, settings, _plan(uc2, mapping={need["id"]: [NAGER]})))
    assert not any("excluded" in e for e in errs)


# -- 2. unmet_needs completeness ------------------------------------------------------------------
def test_complete_unmet_list_passes(uc1, settings):
    weather = [_cand(METEO, "public_api", ["N3"], ["prototype", "production"], "Open-Meteo")]
    covered = {("N3", "prototype"), ("N3", "production")}
    unmet = [f"{n} {w}: no source for this window" for n, w in sorted(_required(uc1) - covered)]
    errs = _errors(_submit(weather, unmet, rejected=[]), scout_spec(uc1, settings, _plan(uc1)))
    assert not any("missing from unmet_needs" in e for e in errs)


def test_missing_required_need_window_is_reported(uc1, settings):
    weather = [_cand(METEO, "public_api", ["N3"], ["prototype", "production"], "Open-Meteo")]
    covered = {("N3", "prototype"), ("N3", "production")}
    unmet = [f"{n} {w}: no source" for n, w in sorted(_required(uc1) - covered) if (n, w) != ("N4", "production")]
    errs = _errors(_submit(weather, unmet, rejected=[]), scout_spec(uc1, settings, _plan(uc1)))
    assert any("N4 production" in e and "missing from unmet_needs" in e for e in errs)


def test_out_of_scope_need_window_must_still_be_listed(uc1, settings):
    weather = [_cand(METEO, "public_api", ["N3"], ["prototype", "production"], "Open-Meteo")]
    covered = {("N3", "prototype"), ("N3", "production")}
    unmet = [f"{n} {w}: no source" for n, w in sorted(_required(uc1) - covered) if (n, w) != ("N5", "production")]
    errs = _errors(_submit(weather, unmet, rejected=[]), scout_spec(uc1, settings, _plan(uc1)))
    assert any("N5 production" in e and "missing from unmet_needs" in e for e in errs)


def test_window_the_need_does_not_require_is_never_demanded(uc1, settings):
    weather = [_cand(METEO, "public_api", ["N3"], ["prototype", "production"], "Open-Meteo")]
    assert ("N2", "prototype") not in _required(uc1)  # the contract says N2 is production-only
    covered = {("N3", "prototype"), ("N3", "production")}
    unmet = [f"{n} {w}: no source" for n, w in sorted(_required(uc1) - covered)]
    errs = _errors(_submit(weather, unmet, rejected=[]), scout_spec(uc1, settings, _plan(uc1)))
    assert not any("N2 prototype" in e for e in errs)


def test_candidate_covered_window_is_not_demanded(uc1, settings):
    weather = [_cand(METEO, "public_api", ["N3"], ["prototype", "production"], "Open-Meteo")]
    unmet = [f"{n} {w}: no source" for n, w in sorted(_required(uc1) - {("N3", "prototype"), ("N3", "production")})]
    errs = _errors(_submit(weather, unmet, rejected=[]), scout_spec(uc1, settings, _plan(uc1)))
    assert not any(e.startswith("N3 ") for e in errs)


def test_incorrect_entry_for_an_unrequired_window_is_still_rejected(uc1, settings):
    weather = [_cand(METEO, "public_api", ["N3"], ["prototype", "production"], "Open-Meteo")]
    covered = {("N3", "prototype"), ("N3", "production")}
    unmet = [f"{n} {w}: no source" for n, w in sorted(_required(uc1) - covered)] + ["N2 prototype: not required"]
    errs = _errors(_submit(weather, unmet, rejected=[]), scout_spec(uc1, settings, _plan(uc1)))
    assert any("N2 prototype" in e and "not required for that window" in e for e in errs)


# -- 3. out-of-scope candidates ---------------------------------------------------------------------
def _full_unmet(uc, covered):
    return [f"{n} {w}: no source" for n, w in sorted(_required(uc) - covered)]


def test_candidate_serving_an_out_of_scope_need_is_rejected(uc1, settings):
    cand = _cand(DAILY_ENTRY, "internal", ["N4", "N5"], ["production"], "daily counts")
    errs = _errors(_submit([cand], _full_unmet(uc1, {("N4", "production")})), scout_spec(uc1, settings, _plan(uc1)))
    assert any(DAILY_ENTRY in e and "out_of_scope" in e and "['N5']" in e for e in errs)


def test_out_of_scope_record_is_rejected_even_under_an_in_scope_need(uc1, settings):
    cand = _cand(PATIENT_ENTRY, "internal", ["N4"], ["production"], "patient visits")
    errs = _errors(_submit([cand], _full_unmet(uc1, {("N4", "production")})), scout_spec(uc1, settings, _plan(uc1)))
    assert any(PATIENT_ENTRY in e and "describes records excluded" in e for e in errs)


def test_in_scope_daily_counts_candidate_is_accepted(uc1, settings):
    cand = _cand(DAILY_ENTRY, "internal", ["N4"], ["production"], "daily counts")
    errs = _errors(_submit([cand], _full_unmet(uc1, {("N4", "production")})), scout_spec(uc1, settings, _plan(uc1)))
    assert not any(DAILY_ENTRY in e for e in errs)


def test_policy_documentation_stays_readable_and_searchable(uc1, settings):
    ok, page = execute("read_wiki_page", {"page_id": "clinic_data_policy"}, _ctx(uc1, settings))
    assert ok and "may not be used for this analysis" in page["body"]
    ok, res = execute("search_internal_catalog", {"query": "clinic data policy"}, _ctx(uc1, settings))
    assert ok and any(h.get("id") == "clinic_data_policy" for h in res["hits"])
