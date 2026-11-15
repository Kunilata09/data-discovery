"""Deterministic red-flag rules, run on every catalog record before the Risk Assessor agent.

Why rules and an agent? Rules are cheap, repeatable and testable, and they catch what can be
read from structured fields. The agent adds judgement flags (conflicts, consent gaps,
representativeness, ...) and may dismiss a rule flag only with a written reason, and the
orchestrator enforces that.

Each rule: (record, candidate, use_case, settings) -> list of {"code", "evidence"}.
"""
from __future__ import annotations

import re
from datetime import date

Flag = dict

GRAIN_ORDER = ["minute", "15min", "30min", "hourly", "daily", "weekly", "monthly", "quarterly", "annual"]
INACTIVE_STATUSES = {"deprecated", "archived", "frozen", "retired", "decommissioned", "superseded"}


def _flag(code: str, evidence: str) -> Flag:
    return {"code": code, "evidence": evidence}


def _d(value: str | None) -> date | None:
    if not value:
        return None
    try:
        return date.fromisoformat(value[:10])
    except ValueError:
        return None


def _overlap_days(a0: date, a1: date, b0: date, b1: date) -> int:
    """Inclusive number of days shared by [a0, a1] and [b0, b1]; 0 if they do not overlap."""
    lo, hi = max(a0, b0), min(a1, b1)
    return (hi - lo).days + 1 if hi >= lo else 0


def _years_before(d: date, years: int) -> date:
    try:
        return d.replace(year=d.year - years)
    except ValueError:  # 29 February in a non-leap target year
        return d.replace(year=d.year - years, day=28)


_NEGATED_MISSING_RE = re.compile(r"(?i)\b(?:no|not|without|free of|nor|zero)\b[^.;:]{0,40}?\b(?:missing|NaN)\b")
_MISSING_RE = re.compile(r"(?i)\bmissing\b|absence of (?:a )?value|(?<![\d.])-200(?![\d.])|\bNaN\b|[\"'`]\?[\"'`]")


def _declares_no(value) -> bool:
    return value is False or (isinstance(value, str) and value.strip().lower() in {"no", "false"})


# ---------------------------------------------------------------------------
# Provided rules (read these as worked examples)
# ---------------------------------------------------------------------------
def rule_licence(record: dict, candidate: dict, uc: dict, settings: dict) -> list[Flag]:
    if record["kind"] == "internal":
        return []
    lic = record.get("licence") or {}
    name = (lic.get("name") or "").strip()
    flags = []
    if not name or name.lower() in {"unknown", "none", "null", "not found", "n/a"}:
        flags.append(_flag("LIC-UNKNOWN", f"No licence established. Evidence field: {lic.get('evidence')!r}"))
    elif re.search(r"\bNC\b|non[- ]?commercial", name, re.I):
        flags.append(_flag("LIC-NONCOMMERCIAL", f"Licence {name!r} restricts commercial use"))
    elif re.search(r"\bBY\b|attribution|OGL|open government", name, re.I):
        flags.append(_flag("LIC-ATTRIBUTION", f"Licence {name!r} requires attribution"))
    if lic.get("mixed_sources"):
        flags.append(_flag("LIC-MIXED", "Record states that parts come from upstream providers with different terms"))
    return flags


def rule_agreement(record: dict, candidate: dict, uc: dict, settings: dict) -> list[Flag]:
    status = ((record.get("licence") or {}).get("agreement_status") or "").lower()
    if record["kind"] == "vendor_feed" and status not in {"active", "signed"}:
        return [_flag("LIC-AGREEMENT-NOT-ACTIVE", f"Vendor feed with agreement_status={status or 'unknown'!r}")]
    return []


def rule_access(record: dict, candidate: dict, uc: dict, settings: dict) -> list[Flag]:
    acc = record.get("access") or {}
    flags = []
    if acc.get("auth_required") or (acc.get("classification") or "").lower() == "restricted":
        flags.append(_flag("ACC-RESTRICTED", f"auth_required={acc.get('auth_required')}, "
                                             f"classification={acc.get('classification')}, process={acc.get('request_process')!r}"))
    if (acc.get("method") or "").lower() in {"manual_export", "manual", "spreadsheet", "email"}:
        flags.append(_flag("ACC-MANUAL", f"Access method {acc.get('method')!r}"))
    if acc.get("reachable") is False:
        flags.append(_flag("ACC-UNREACHABLE", "Record states the source could not be reached or restored"))
    return flags


def rule_payload(record: dict, candidate: dict, uc: dict, settings: dict) -> list[Flag]:
    size = (record.get("access") or {}).get("approx_size_bytes")
    limit = settings["rules"]["large_payload_bytes"]
    if isinstance(size, int) and size > limit:
        return [_flag("OPS-LARGE-PAYLOAD", f"approx_size_bytes={size:,} > {limit:,}")]
    return []


def rule_pii(record: dict, candidate: dict, uc: dict, settings: dict) -> list[Flag]:
    pii_fields = [f["name"] for f in (record.get("schema") or {}).get("fields", []) if f.get("pii") is True]
    declared = (record.get("declared_metadata") or {}).get("contains_pii")
    if pii_fields or declared is True:
        return [_flag("GOV-PII", f"PII fields: {pii_fields or 'declared contains_pii=true'}")]
    return []


def rule_owner(record: dict, candidate: dict, uc: dict, settings: dict) -> list[Flag]:
    if record["kind"] == "internal" and not ((record.get("ownership") or {}).get("owner") or "").strip():
        return [_flag("GOV-OWNER-UNKNOWN", "Internal source with no recorded owner")]
    return []


def rule_status(record: dict, candidate: dict, uc: dict, settings: dict) -> list[Flag]:
    status = (record.get("status") or "").lower()
    if status in INACTIVE_STATUSES:
        return [_flag("GOV-DEPRECATED", f"status={status!r}")]
    return []


# ---------------------------------------------------------------------------
# LEARNER TODO (G4): three rules. tests/test_learner_gaps.py::test_g4_* checks them.
# ---------------------------------------------------------------------------
def rule_temporal_coverage(record: dict, candidate: dict, uc: dict, settings: dict) -> list[Flag]:
    """Coverage of the candidate's target windows, plus staleness.

    - Skip records whose temporal.grain is "static", or whose start is unknown.
    - Treat a null end as "still updating", i.e. covered up to uc["as_of"].
    - For each window id in candidate["target_windows"], compute the fraction of that window
      (uc["windows"], inclusive dates) covered by [start, end].
        all fractions == 0                                      -> COV-OUT-OF-WINDOW
        otherwise any fraction < settings["rules"]["partial_window_threshold"] -> COV-PARTIAL-WINDOW
    - FRS-STALE if end is not null and end is more than settings["rules"]["stale_after_years"]
      years before uc["as_of"].
    Evidence strings must name the window(s) and the dates you compared.
    """
    temporal = record.get("temporal") or {}
    if (temporal.get("grain") or "").lower() == "static":
        return []
    start = _d(temporal.get("start"))
    if start is None:
        return []
    as_of = _d(uc["as_of"])
    end_raw = _d(temporal.get("end"))
    end = end_raw or as_of  # a null end means "still updating": covered up to the as-of date
    open_label = "open (still updating)" if end_raw is None else str(end_raw)

    windows = {w["id"]: w for w in uc.get("windows", [])}
    fractions = {}  # window id -> (fraction covered, window start, window end, covered days)
    for wid in candidate.get("target_windows") or []:
        w = windows.get(wid)
        if w is None:
            continue
        w_start, w_end = _d(w["start"]), _d(w["end"])
        length = (w_end - w_start).days + 1
        covered = _overlap_days(start, end, w_start, w_end)
        fractions[wid] = (covered / length, w_start, w_end)
    if not fractions:
        return []

    flags = []
    threshold = settings["rules"]["partial_window_threshold"]
    ids = ", ".join(sorted(fractions))
    if all(frac == 0 for frac, _, _ in fractions.values()):
        flags.append(_flag("COV-OUT-OF-WINDOW",
                           f"record {start} to {open_label} does not overlap target window(s) {ids}"))
    else:
        short = [f"{wid} ({frac:.0%} of {w0} to {w1})" for wid, (frac, w0, w1) in sorted(fractions.items())
                 if frac < threshold]
        if short:
            flags.append(_flag("COV-PARTIAL-WINDOW",
                               f"record {start} to {open_label} covers less than {threshold:.0%} of: " + "; ".join(short)))
    if end_raw is not None and end_raw < _years_before(as_of, settings["rules"]["stale_after_years"]):
        flags.append(_flag("FRS-STALE",
                           f"data ends {end_raw}, more than {settings['rules']['stale_after_years']} years "
                           f"before as-of {as_of} (window(s) {ids})"))
    return flags


def rule_grain(record: dict, candidate: dict, uc: dict, settings: dict) -> list[Flag]:
    """COV-GRAIN-MISMATCH if the record's grain is coarser than min_grain of any need the
    candidate serves (candidate["need_ids"] -> uc["needs"]). Only grains in GRAIN_ORDER are
    comparable; "event", "static" and "unknown" on either side never raise the flag."""
    grain = ((record.get("temporal") or {}).get("grain") or "").lower()
    if grain not in GRAIN_ORDER:
        return []
    needs = {n["id"]: n for n in uc.get("needs", [])}
    too_coarse = []
    for nid in candidate.get("need_ids") or []:
        min_grain = (needs.get(nid) or {}).get("min_grain")
        if min_grain in GRAIN_ORDER and GRAIN_ORDER.index(grain) > GRAIN_ORDER.index(min_grain):
            too_coarse.append(f"{nid} needs {min_grain}")
    if not too_coarse:
        return []
    return [_flag("COV-GRAIN-MISMATCH", f"source grain {grain!r} is coarser than: {', '.join(too_coarse)}")]


def rule_metadata_contradiction(record: dict, candidate: dict, uc: dict, settings: dict) -> list[Flag]:
    """DQ-METADATA-CONTRADICTION when record["declared_metadata"]["has_missing_values"] is a
    'no' (False, "no", "false") but documentation_excerpts or quality_notes describe missing
    values (e.g. "missing values", "absence of value", "-200", "?" used as missing, "NaN").
    Careful: "Data set has no missing values" is NOT a contradiction. Strip negated phrases
    before matching."""
    declared = (record.get("declared_metadata") or {}).get("has_missing_values")
    if not _declares_no(declared):
        return []
    sources = [("documentation_excerpts", record.get("documentation_excerpts") or []),
               ("quality_notes", record.get("quality_notes") or [])]
    for source, texts in sources:
        for text in texts:
            if not isinstance(text, str):
                continue
            # Negated phrases ("has no missing values") are removed before the search, so they never match.
            if _MISSING_RE.search(_NEGATED_MISSING_RE.sub(" ", text)):
                return [_flag("DQ-METADATA-CONTRADICTION",
                              f"declared has_missing_values={declared!r}, but {source} says: {text.strip()[:200]!r}")]
    return []


RULES = [rule_licence, rule_agreement, rule_access, rule_payload, rule_pii, rule_owner, rule_status,
         rule_temporal_coverage, rule_grain, rule_metadata_contradiction]


def evaluate(record: dict, candidate: dict, uc: dict, settings: dict) -> tuple[list[Flag], list[str]]:
    """Run every rule. Returns (flags, warnings). A rule that is not implemented yet is skipped with a warning."""
    flags: list[Flag] = []
    warnings: list[str] = []
    for rule in RULES:
        try:
            for f in rule(record, candidate, uc, settings):
                flags.append({**f, "raised_by": f"rule:{rule.__name__}"})
        except NotImplementedError as exc:
            warnings.append(f"{rule.__name__} skipped: {exc}")
    seen, unique = set(), []
    for f in flags:
        if f["code"] not in seen:
            seen.add(f["code"])
            unique.append(f)
    return unique, warnings
