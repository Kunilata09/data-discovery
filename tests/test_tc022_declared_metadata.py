"""TC-022: declared_metadata flags must be stated by the source, not inferred from counts.

Regression for the Eurostat record: the profiler wrote declared_metadata.has_missing_values = "no"
from summarize_jsonstat's computed missing_cells = 0, and no tool result said so.
"""
from discovery_agent.agent import AgentSpec, collect_keys, validate
from discovery_agent.agents import declared_flags_are_stated

# The keys of the real summarize_jsonstat result for the Eurostat link (UC1). Publisher fields
# and computed counts sit side by side; none of them is a missing-value flag.
EUROSTAT_SUMMARY_KEYS_FIXTURE = {
    "url": "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sdg_11_52?format=JSON&lang=EN&geo=IT",
    "label": "Premature deaths due to exposure to fine particulate matter (PM2.5)",
    "updated": "2025-12-09T11:00:00+0100",
    "source": "ESTAT",
    "dimensions": [{"id": "geo", "size": 1, "labels": ["IT: Italy"]}],
    "time": {"first": "2005", "last": "2023", "values": ["2005", "2007"]},
    "geo_codes": ["IT"],
    "expected_cells": 36,
    "value_count": 36,
    "missing_cells": 0,
    "status_counts": {},
    "warnings": [],
}


def _payload(declared: dict) -> dict:
    return {"declared_metadata": declared}


def test_no_flag_without_evidence_is_rejected():
    errs = declared_flags_are_stated(_payload({"has_missing_values": "no"}), frozenset(EUROSTAT_SUMMARY_KEYS_FIXTURE))
    assert len(errs) == 1 and "has_missing_values" in errs[0]


def test_eurostat_style_counts_do_not_stand_in_for_the_flag():
    evidence = collect_keys(EUROSTAT_SUMMARY_KEYS_FIXTURE, set())
    assert "missing_cells" in evidence                 # the count exists ...
    assert "has_missing_values" not in evidence        # ... but the source states no flag
    assert declared_flags_are_stated(_payload({"has_missing_values": "no"}), frozenset(evidence))


def test_flag_is_accepted_when_a_tool_result_contains_it():
    # UCI metadata nests its flags under "declared"; the key still counts as stated.
    uci_result = {"metadata": {"declared": {"has_missing_values": "no", "missing_values_symbol": None}}}
    evidence = frozenset(collect_keys(uci_result, set()))
    assert declared_flags_are_stated(_payload({"has_missing_values": "no"}), evidence) == []


def test_null_is_always_acceptable():
    assert declared_flags_are_stated(_payload({"has_missing_values": None}), frozenset()) == []
    assert declared_flags_are_stated({}, frozenset()) == []


def test_collect_keys_walks_nested_lists_and_dicts():
    keys = collect_keys({"a": [{"b": {"c": 1}}, {"d": 2}], "e": "text"}, set())
    assert keys == {"a", "b", "c", "d", "e"}


def test_validate_runs_evidence_checks_with_the_run_evidence():
    spec = AgentSpec(name="t", system_prompt="", tool_names=[], submit_name="submit", submit_description="",
                     submit_schema={"type": "object"}, max_turns=1,
                     evidence_validators=[declared_flags_are_stated])
    payload = _payload({"has_missing_values": "no"})
    assert validate(payload, spec)                              # no evidence: rejected
    assert validate(payload, spec, frozenset({"has_missing_values"})) == []


def test_unsupported_contains_pii_is_rejected_like_has_missing_values():
    # UC2 Nager: the profiler wrote contains_pii "no" although no tool result states it.
    errs = declared_flags_are_stated(_payload({"contains_pii": "no"}), frozenset(EUROSTAT_SUMMARY_KEYS_FIXTURE))
    assert len(errs) == 1 and "contains_pii" in errs[0]


def test_contains_pii_is_accepted_when_stated_or_null():
    evidence = frozenset({"contains_pii"})   # internal catalog results carry this key
    assert declared_flags_are_stated(_payload({"contains_pii": False}), evidence) == []
    assert declared_flags_are_stated(_payload({"contains_pii": None}), frozenset()) == []
