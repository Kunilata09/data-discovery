"""The five agents: what each may use, what each must return, and how its output is checked."""
from __future__ import annotations

import json
import re

from .agent import AgentSpec
from .config import load_prompt, load_red_flags, load_register, load_schema
from .guards import excluded_match, excluded_sources, out_of_scope_need_ids, register_name_in, register_name_tokens
from .tools.internal_catalog import _load_estate

SCOUT_TOOLS = ["search_internal_catalog", "get_catalog_entry", "read_wiki_page", "list_external_register"]
PROFILER_TOOLS = ["get_catalog_entry", "read_wiki_page", "search_internal_catalog", "list_external_register", "call_public_api",
                  "inspect_dataset_link", "sample_data_file", "probe_url", "summarize_datapackage", "summarize_jsonstat"]
RISK_TOOLS = ["read_wiki_page", "get_catalog_entry"]
# An unmet-needs entry must start with the need and window it reports, e.g. "N1 prototype: no source ...".
UNMET_ENTRY = re.compile(r"^\s*(N\d+)\s+([A-Za-z0-9_-]+)\s*:")


def _with_shared(name: str) -> str:
    """System prompt = shared operating rules + agent-specific prompt."""
    return load_prompt("_shared_rules") + "\n\n" + load_prompt(name)


def planner_spec(uc: dict, settings: dict) -> AgentSpec:
    need_ids = {n["id"] for n in uc["needs"]}
    register = load_register(uc["id"])
    kinds = {s["id"]: s["kind"] for s in register}
    data_ids = {i for i, k in kinds.items() if k in ("public_api", "vendor_feed")}
    names = register_name_tokens(register)
    excl = excluded_sources(uc)

    def covers_all_needs(p: dict) -> list[str]:
        got = {n["need_id"] for n in p["need_plans"]}
        return [f"need_plans is missing {sorted(need_ids - got)}"] if need_ids - got else []

    def register_ids_are_data_sources(p: dict) -> list[str]:
        return [f"{n['need_id']}: register_ids entry {rid!r} is not a public API or vendor feed tagged for {uc['id']}. "
                "Policy entries are not data sources; datasets come from links at the candidate gate."
                for n in p["need_plans"] for rid in n["register_ids"] if rid not in data_ids]

    def excluded_sources_are_not_mapped(p: dict) -> list[str]:
        return [f"{n['need_id']}: register_ids entry {rid!r} is excluded for {uc['id']} by the use-case contract "
                f"({excl[rid]}). Do not map it to any need."
                for n in p["need_plans"] for rid in n["register_ids"] if rid in excl]

    def vendor_feeds_are_mapped(p: dict) -> list[str]:
        mapped = {rid for n in p["need_plans"] for rid in n["register_ids"]}
        return [f"{sid}: vendor feed tagged for {uc['id']} must appear in register_ids of the need(s) it could serve, "
                "even when its agreement is expired. The Scout reports it as a finding; it is not left out."
                for sid, kind in kinds.items() if kind == "vendor_feed" and sid not in mapped and sid not in excl]

    def no_register_names_in_queries(p: dict) -> list[str]:
        errs = []
        for n in p["need_plans"]:
            for q in n["internal_queries"]:
                rid = register_name_in(q, names)
                if rid:
                    errs.append(f"{n['need_id']}: internal query {q!r} names the register source {rid!r}. Register sources "
                                "go in register_ids. internal_queries search the internal catalog and wiki only.")
        return errs

    return AgentSpec("planner", _with_shared("planner"), ["list_external_register"], "submit_search_plan",
                     "Submit the search plan. Call exactly once, when complete.", load_schema("search_plan"),
                     settings["agents"]["max_turns"]["planner"],
                     [covers_all_needs, register_ids_are_data_sources, excluded_sources_are_not_mapped,
                      vendor_feeds_are_mapped, no_register_names_in_queries])


def scout_spec(uc: dict, settings: dict, plan: dict | None = None) -> AgentSpec:
    est = _load_estate(str(uc["internal_path"]))
    register = load_register(uc["id"])
    register_ids = {s["id"] for s in register if s["kind"] in ("public_api", "vendor_feed")}
    vendor_ids = {s["id"] for s in register if s["kind"] == "vendor_feed"}
    planned_vendors = {rid for n in (plan or {}).get("need_plans", []) for rid in n["register_ids"] if rid in vendor_ids}
    windows = {w["id"] for w in uc["windows"]}
    needs = {n["id"] for n in uc["needs"]}
    needs_windows = {(n["id"], w) for n in uc["needs"] for w in n["windows"]}
    max_c = settings["agents"]["max_candidates"]

    def ids_exist(p: dict) -> list[str]:
        errs, seen = [], set()
        for c in p["candidates"]:
            sid = c["source_id"]
            if sid in seen:
                errs.append(f"duplicate candidate {sid}")
            seen.add(sid)
            if sid.startswith("internal.") and sid.removeprefix("internal.") not in est["entries"]:
                errs.append(f"{sid}: no such internal catalog entry (use the exact id from search_internal_catalog)")
            if sid.startswith(("api.", "vendor.")) and sid not in register_ids:
                errs.append(f"{sid}: not in the external register for {uc['id']}")
            if sid.startswith("link."):
                errs.append(f"{sid}: do not add dataset links yourself; the human supplies them at the candidate gate. "
                            "Describe what is missing in unmet_needs instead")
            kind_ok = {"internal.": "internal", "api.": "public_api", "vendor.": "vendor_feed"}
            for prefix, kind in kind_ok.items():
                if sid.startswith(prefix) and c["kind"] != kind:
                    errs.append(f"{sid}: kind must be {kind!r}")
            if set(c["target_windows"]) - windows:
                bad = sorted(set(c["target_windows"]) - windows)
                errs.append(f"{sid}: unknown target_windows {bad}; use {sorted(windows)}")
            if set(c["need_ids"]) - needs:
                errs.append(f"{sid}: unknown need_ids {sorted(set(c['need_ids']) - needs)}")
        if len(p["candidates"]) > max_c:
            errs.append(f"too many candidates ({len(p['candidates'])} > {max_c}). "
                        "Keep the strongest; list the rest in rejected_without_profiling")
        return errs

    def planned_vendors_accounted(p: dict) -> list[str]:
        accounted = {c["source_id"] for c in p["candidates"]} | {r["source_id"] for r in p.get("rejected_without_profiling") or []}
        return [f"{v}: the search plan maps this vendor feed to a need, so it must appear as a candidate (with its agreement "
                "status) or in rejected_without_profiling with a reason. It must not silently disappear."
                for v in sorted(planned_vendors - accounted)]

    def candidates_in_scope(p: dict) -> list[str]:
        """Excluded sources and out-of-scope needs or records never become candidates. Policy documents are not
        candidates, so they stay readable through read_wiki_page and the search."""
        errs = []
        for c in p["candidates"]:
            sid = c["source_id"]
            if sid in excluded_sources(uc):
                errs.append(f"{sid}: excluded for {uc['id']} by the use-case contract. Do not submit it; "
                            "it is not a candidate for any need.")
            out = sorted(set(c["need_ids"]) & out_of_scope_need_ids(uc))
            if out:
                errs.append(f"{sid}: serves {out}, which the use-case contract marks out_of_scope. Remove those need ids, "
                            "and record the scope restriction in unmet_needs.")
            if sid.startswith("internal."):
                entry = est["entries"].get(sid.removeprefix("internal."))
                need = excluded_match(json.dumps(entry), uc) if entry else None
                if need:
                    errs.append(f"{sid}: describes records excluded by the scope of {need}. Do not submit it. Record the "
                                "restriction in unmet_needs.")
        return errs

    def unmet_are_genuine_gaps(p: dict) -> list[str]:
        covered = {(nid, w) for c in p["candidates"] for nid in c["need_ids"] for w in c["target_windows"]}
        errs = []
        for u in p["unmet_needs"]:
            m = UNMET_ENTRY.match(u)
            if not m:
                errs.append(f"unmet_needs entry {u[:60]!r} must start with '<need id> <window id>:', e.g. 'N1 prototype: ...'")
                continue
            pair = (m.group(1), m.group(2))
            if pair not in needs_windows:
                errs.append(f"unmet_needs entry {pair[0]} {pair[1]}: that need is not required for that window "
                            "(see the need's windows in the spec). It is not a gap; remove it.")
            elif pair in covered:
                errs.append(f"unmet_needs entry {pair[0]} {pair[1]}: a candidate already covers it. Record the weakness "
                            "in suspected_issues, not in unmet_needs.")
        return errs

    def unmet_cover_every_gap(p: dict) -> list[str]:
        """Completeness: every required need-window that no candidate covers must be listed in unmet_needs."""
        covered = {(nid, w) for c in p["candidates"] for nid in c["need_ids"] for w in c["target_windows"]}
        listed = {(m.group(1), m.group(2)) for u in p["unmet_needs"] if (m := UNMET_ENTRY.match(u))}
        return [f"{nid} {w}: a required need-window with no candidate is missing from unmet_needs. "
                f"Add '{nid} {w}: <why no source covers it>'."
                for nid, w in sorted(needs_windows - covered - listed)]

    return AgentSpec("scout", _with_shared("scout"), SCOUT_TOOLS, "submit_candidates",
                     "Submit the candidate source list. Call exactly once, when your search is complete.",
                     load_schema("candidates"), settings["agents"]["max_turns"]["scout"],
                     [ids_exist, planned_vendors_accounted, candidates_in_scope, unmet_are_genuine_gaps, unmet_cover_every_gap])


#: declared_metadata flags that the risk rules read as a publisher's own claim (GOV-PII reads contains_pii;
#: DQ-METADATA-CONTRADICTION reads has_missing_values). A non-null value must come from a tool result that
#: actually contains the key (TC-022; contains_pii added after the UC2 Nager record was found unsupported).
PUBLISHER_FLAGS_NEEDING_EVIDENCE = ("has_missing_values", "contains_pii")


def declared_flags_are_stated(payload: dict, evidence: frozenset) -> list[str]:
    """A declared flag is the source's claim, so the source's own tool results must contain it.
    `missing_cells: 0` in a count does not show that the source says it has no missing values."""
    declared = payload.get("declared_metadata") or {}
    errs = []
    for key in PUBLISHER_FLAGS_NEEDING_EVIDENCE:
        value = declared.get(key)
        if value is not None and key not in evidence:
            errs.append(f"declared_metadata.{key} is {value!r}, but no tool result for this source "
                        f"contains a {key!r} field. Set it to null, and put what the sample or counts "
                        "show in sample_findings or quality_notes.")
    return errs


def profiler_spec(uc: dict, settings: dict, candidate: dict) -> AgentSpec:
    def matches_candidate(r: dict) -> list[str]:
        errs = []
        if r["source_id"] != candidate["source_id"]:
            errs.append(f"source_id must be {candidate['source_id']!r}")
        if r["kind"] != candidate["kind"]:
            errs.append(f"kind must be {candidate['kind']!r}")
        t = r["temporal"]
        if t.get("start") and t.get("end") and t["start"] > t["end"]:
            errs.append("temporal.start is after temporal.end")
        return errs

    return AgentSpec("profiler", _with_shared("profiler"), PROFILER_TOOLS, "submit_catalog_record",
                     "Submit the catalog record for this one source. Call exactly once.",
                     load_schema("catalog_record"), settings["agents"]["max_turns"]["profiler"], [matches_candidate],
                     evidence_validators=[declared_flags_are_stated])


def risk_spec(uc: dict, settings: dict, records: list[dict], rule_flags: dict[str, list[dict]]) -> AgentSpec:
    valid_codes = set(load_red_flags())
    expected = {r["source_id"] for r in records}
    needs = {n["id"] for n in uc["needs"]}

    def complete_and_consistent(p: dict) -> list[str]:
        errs = []
        got = [a["source_id"] for a in p["assessments"]]
        if set(got) != expected or len(got) != len(set(got)):
            errs.append(f"assess every source exactly once. Missing: {sorted(expected - set(got))}; "
                        f"unexpected: {sorted(set(got) - expected)}")
        for a in p["assessments"]:
            raised = {f["code"] for f in a["red_flags"]}
            for code in raised | {d["code"] for d in a.get("dismissed_rule_flags", [])}:
                if code not in valid_codes:
                    errs.append(f"{a['source_id']}: invalid red-flag code {code!r}")
            dismissed = {d["code"] for d in a.get("dismissed_rule_flags", [])}
            for rf in rule_flags.get(a["source_id"], []):
                if rf["code"] not in raised and rf["code"] not in dismissed:
                    errs.append(f"{a['source_id']}: rule flag {rf['code']} must be kept in red_flags or listed in "
                                "dismissed_rule_flags with a reason")
            if a["verdict"] == "feasible_with_conditions" and not a["conditions"]:
                errs.append(f"{a['source_id']}: feasible_with_conditions needs at least one condition")
        cov = {c["need_id"] for c in p["need_coverage"]}
        if needs - cov:
            errs.append(f"need_coverage is missing {sorted(needs - cov)}")
        return errs

    return AgentSpec("risk_assessor", _with_shared("risk_assessor"), RISK_TOOLS, "submit_risk_assessment",
                     "Submit verdicts, red flags and need coverage for ALL sources. Call exactly once.",
                     load_schema("risk_assessment"), settings["agents"]["max_turns"]["risk_assessor"],
                     [complete_and_consistent])


REQUIRED_MEMO_HEADINGS = ["## 1. Executive summary", "## 2. Need coverage", "## 3. Source assessments",
                          "## 4. Red-flag register", "## 5. Conditions and owners", "## 6. Recommended next steps",
                          "## 7. Open questions for the human reviewer"]


def memo_spec(uc: dict, settings: dict, source_ids: list[str]) -> AgentSpec:
    def has_structure(p: dict) -> list[str]:
        md = p["markdown"]
        errs = [f"missing heading {h!r}" for h in REQUIRED_MEMO_HEADINGS if h not in md]
        missing = [s for s in source_ids if s not in md]
        if missing:
            errs.append(f"memo must mention every assessed source id; missing {missing}")
        return errs

    return AgentSpec("memo_writer", _with_shared("memo_writer"), [], "submit_memo",
                     "Submit the feasibility memo as Markdown. Call exactly once.", load_schema("memo"),
                     settings["agents"]["max_turns"]["memo_writer"], [has_structure])
