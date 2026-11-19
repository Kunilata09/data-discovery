"""G7 regression tests. Each one reproduces a failure seen in the UC1 Scout run before the fix.

1. An expired vendor feed silently dropped: the plan must map it, the Scout must account for it.
2. A register name placed in internal_queries: the planner validator must reject it.
3. A patient-level (out-of-scope) search: the search tool must refuse it and withhold excluded entries.
4. An unmet-needs entry for a window the need does not require (N2 prototype): the Scout validator must reject it.
5. A per-call change to the weather variables (humidity): the API tool must refuse it; dates may still change.

The checks are generic: they read the use-case contract and the register, not fixed answers.
"""
from __future__ import annotations

import pytest

from discovery_agent.agent import validate
from discovery_agent.agents import planner_spec, scout_spec
from discovery_agent.config import load_register
from discovery_agent.guards import excluded_match, locked_variable_overrides, register_name_in, register_name_tokens
from discovery_agent.tools import ToolContext, execute
from discovery_agent.trace import Trace

VENDOR = "vendor.atmosdata_pro"  # UC1 register entry, agreement expired
METEO = "api.open_meteo_archive"  # UC1 register entry, the configured weather query


def _ctx(uc, settings):
    return ToolContext(use_case=uc, settings=settings, http=None, trace=Trace(None), agent="test")


def _plan(uc, mapping=None, queries=None):
    mapping, queries = mapping or {}, queries or {}
    return {"use_case": uc["id"], "objective_summary": "x" * 60,
            "need_plans": [{"need_id": n["id"], "interpretation": n["name"],
                            "internal_queries": queries.get(n["id"], [n["name"]]), "external_data_hints": [],
                            "register_ids": mapping.get(n["id"], []), "acceptance_criteria": ["covers the window"]}
                           for n in uc["needs"]],
            "open_questions": []}


def _candidates(extra_rejected=None, unmet=None, candidates=None):
    cands = candidates if candidates is not None else [{
        "source_id": METEO, "kind": "public_api", "title": "Open-Meteo", "need_ids": ["N3"],
        "target_windows": ["prototype", "production"], "why_relevant": "temperature and humidity", "found_via": "register"}]
    out = {"candidates": cands, "searches_run": ["q"], "unmet_needs": unmet or []}
    if extra_rejected is not None:
        out["rejected_without_profiling"] = extra_rejected
    return out


def _errors(payload, spec):
    return validate(payload, spec)


# -- 1. the expired vendor feed must not disappear ---------------------------------------
def test_planner_must_map_the_vendor_feed_to_a_need(uc1, settings):
    spec = planner_spec(uc1, settings)
    assert any(VENDOR in e and "register_ids" in e for e in _errors(_plan(uc1), spec))
    assert _errors(_plan(uc1, mapping={"N3": [VENDOR]}), spec) == []


def test_scout_must_account_for_every_planned_vendor_feed(uc1, settings):
    plan = _plan(uc1, mapping={"N1": [VENDOR]})
    spec = scout_spec(uc1, settings, plan)
    missing = _errors(_candidates(), spec)
    assert any(VENDOR in e and "must not silently disappear" in e for e in missing)
    # Accounted for as a rejection with a reason ...
    assert not any(VENDOR in e for e in _errors(_candidates(extra_rejected=[{"source_id": VENDOR, "reason": "agreement expired"}]), spec))
    # ... or as a candidate that carries its status. Either way it is not silently dropped.
    as_candidate = _candidates(candidates=[{
        "source_id": VENDOR, "kind": "vendor_feed", "title": "AtmosData", "need_ids": ["N1"], "target_windows": ["production"],
        "why_relevant": "station-grade feed", "found_via": "register", "suspected_issues": ["agreement expired"]}])
    assert not any(VENDOR in e for e in _errors(as_candidate, spec))


def test_unplanned_vendor_feed_is_not_demanded_by_the_scout(uc1, settings):
    spec = scout_spec(uc1, settings, _plan(uc1))  # no need maps the vendor feed
    assert not any(VENDOR in e for e in _errors(_candidates(), spec))


# -- 2. register names must not be placed in internal_queries ------------------------------
def test_register_name_in_internal_query_is_rejected(uc1, settings):
    spec = planner_spec(uc1, settings)
    bad = _plan(uc1, mapping={"N3": [VENDOR]}, queries={"N3": ["AtmosData weather feed", "hourly temperature"]})
    errs = _errors(bad, spec)
    assert any("internal query 'AtmosData weather feed'" in e and "register_ids" in e for e in errs)
    good = _plan(uc1, mapping={"N3": [VENDOR]}, queries={"N3": ["hourly temperature weather station"]})
    assert _errors(good, spec) == []


def test_policy_entry_cannot_be_a_register_id(uc1, settings):
    spec = planner_spec(uc1, settings)
    errs = _errors(_plan(uc1, mapping={"N1": [VENDOR, "policy.open_data_links"]}), spec)
    assert any("policy.open_data_links" in e and "not a public API or vendor feed" in e for e in errs)


def test_register_name_detection_is_generic(uc1):
    names = register_name_tokens(load_register("UC1"))
    assert register_name_in("AtmosData weather feed", names) == VENDOR
    assert register_name_in("Open-Meteo archive weather", names) == METEO
    assert register_name_in("hourly temperature and humidity", names) is None


# -- 3. the out-of-scope need is not searched -----------------------------------------------
def test_out_of_scope_search_is_refused_before_any_catalog_hit(uc1, settings):
    ok, res = execute("search_internal_catalog", {"query": "patient visit records event level"}, _ctx(uc1, settings))
    assert ok and res["hits"] == [] and "N5" in res["refused"] and "scope" in res["refused"]


def test_out_of_scope_catalog_entry_is_not_opened(uc1, settings):
    assert excluded_match("one row per patient visit", uc1) == "N5"
    ok, payload = execute("get_catalog_entry", {"entry_id": "clinic.patient_visits"}, _ctx(uc1, settings))
    assert not ok and "out of scope" in str(payload) and "not opened" in str(payload)


def test_out_of_scope_entry_is_withheld_from_search_hits(uc1, settings):
    ok, res = execute("search_internal_catalog", {"query": "clinic visits patient district", "top_k": 10}, _ctx(uc1, settings))
    # The catalog entry is never shown. The wiki policy page may still be listed: it is the restriction itself.
    assert ok and "internal.clinic.patient_visits" not in [h.get("source_id") for h in res["hits"]]
    assert res["withheld_out_of_scope"] == 1  # the excluded entry scored in the top results and was counted, not shown
    assert any(h.get("source_id") == "internal.clinic.resp_visits_daily" for h in res["hits"])  # in-scope hits still shown


def test_in_scope_search_and_entry_still_work(uc1, settings):
    ok, res = execute("search_internal_catalog", {"query": "respiratory clinic visits daily counts district"}, _ctx(uc1, settings))
    assert ok and "refused" not in res and any(h.get("id") == "clinic.resp_visits_daily" for h in res["hits"])
    ok, entry = execute("get_catalog_entry", {"entry_id": "clinic.resp_visits_daily"}, _ctx(uc1, settings))
    assert ok and entry["source_id"] == "internal.clinic.resp_visits_daily"


# -- 4. unmet_needs holds only genuine gaps ----------------------------------------------------
WEATHER = [{"source_id": METEO, "kind": "public_api", "title": "Open-Meteo", "need_ids": ["N3"],
            "target_windows": ["prototype", "production"], "why_relevant": "temperature", "found_via": "register"}]


def test_unmet_entry_for_a_window_the_need_does_not_require_is_rejected(uc1, settings):
    spec = scout_spec(uc1, settings, _plan(uc1))
    errs = _errors(_candidates(unmet=["N2 prototype: not required by the spec"], candidates=WEATHER), spec)
    assert any("N2 prototype" in e and "not required for that window" in e for e in errs)


def test_unmet_entry_for_a_covered_need_window_is_rejected(uc1, settings):
    spec = scout_spec(uc1, settings, _plan(uc1))
    errs = _errors(_candidates(unmet=["N3 production: no fallback"], candidates=WEATHER), spec)
    assert any("N3 production" in e and "already covers it" in e for e in errs)


def test_unmet_entry_must_name_need_and_window(uc1, settings):
    spec = scout_spec(uc1, settings, _plan(uc1))
    errs = _errors(_candidates(unmet=["N6 national PM2.5 deaths, no source"], candidates=WEATHER), spec)
    assert any("must start with '<need id> <window id>:'" in e for e in errs)


def test_genuine_unmet_gaps_are_accepted(uc1, settings):
    spec = scout_spec(uc1, settings, _plan(uc1))
    # Complete for this candidate set: every required window the Open-Meteo candidate does not cover is listed.
    genuine = ["N1 prototype: no internal or register source; a public dataset must be supplied as a link",
               "N1 production: no internal or register source at the required grain for the production window",
               "N2 production: no traffic source in the register",
               "N4 production: no candidate survived the scope and grain checks",
               "N5 production: out of scope by the brief; patient-level records are not searched",
               "N6 prototype: no internal or register source",
               "N6 production: no internal or register source"]
    errs = _errors(_candidates(unmet=genuine, candidates=WEATHER), spec)
    assert not [e for e in errs if "unmet_needs" in e]


# -- 5. the weather variables are not changed per call -----------------------------------------
def test_per_call_variable_override_is_refused(uc1, settings):
    ok, payload = execute("call_public_api", {"source_id": METEO,
                                              "query": {"hourly": "temperature_2m,relative_humidity_2m"}}, _ctx(uc1, settings))
    assert not ok and "fixed by the register" in str(payload) and "['hourly']" in str(payload)


def test_dates_and_coordinates_may_still_be_overridden():
    default = next(s for s in load_register("UC1") if s["id"] == METEO)["default_query"]
    assert locked_variable_overrides(default, {"start_date": "2004-03-10", "end_date": "2005-04-04",
                                               "latitude": "45.4642"}) == []
    assert locked_variable_overrides(default, {"hourly": default["hourly"]}) == []  # same value is not a change
    assert locked_variable_overrides(default, {"hourly": "temperature_2m,relative_humidity_2m"}) == ["hourly"]


@pytest.mark.parametrize("bad", [{"daily": "temperature_2m_max"}, {"current": "relative_humidity_2m"}])
def test_other_variable_lists_are_locked_too(bad):
    default = {"hourly": "temperature_2m,shortwave_radiation"}
    assert locked_variable_overrides(default, bad) == [next(iter(bad))]
