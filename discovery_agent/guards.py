"""Deterministic guards shared by the tools and the submit validators (G7).

Each guard answers a question that a prompt alone did not enforce:
- Is this search, catalog entry or query about a need that the brief put out of scope?
- Does a per-call API query try to change the variables the register fixes?
- Does a planner query name a register source instead of asking the catalog for it?

Everything here is driven by the use-case contract and the register, never by UC1 values.
"""
from __future__ import annotations

import re

# Variable-list parameters of the public APIs. The register fixes them; a per-call query may set dates and
# coordinates, but it may not add or change these. A missing variable is a coverage gap, not a silent change.
VARIABLE_PARAMS = ("hourly", "daily", "current", "minutely_15")


def out_of_scope_needs(uc: dict) -> list[dict]:
    return [n for n in uc.get("needs", []) if n.get("scope") == "out_of_scope"]


def out_of_scope_need_ids(uc: dict) -> set[str]:
    return {n["id"] for n in out_of_scope_needs(uc)}


def excluded_sources(uc: dict) -> dict[str, str]:
    """Register id -> reason, for sources this use case excludes in its own contract (`excluded_sources`).

    The exclusion is per use case: the same register entry may stay usable for another use case.
    """
    return {e["id"]: e.get("reason") or "" for e in uc.get("excluded_sources") or []}


def excluded_terms(uc: dict) -> dict[str, str]:
    """Lower-case excluded phrase -> id of the out-of-scope need that excludes it."""
    terms = {}
    for n in out_of_scope_needs(uc):
        for term in n.get("excluded_terms") or []:
            terms[term.lower().strip()] = n["id"]
    return {t: nid for t, nid in terms.items() if t}


def excluded_match(text: str, uc: dict) -> str | None:
    """The out-of-scope need id whose excluded phrase occurs in text, or None."""
    low = (text or "").lower()
    for term, need_id in excluded_terms(uc).items():
        if term in low:
            return need_id
    return None


def locked_variable_overrides(default_query: dict, query: dict) -> list[str]:
    """Variable parameters a per-call query sets to a value other than the configured one."""
    return sorted(k for k in VARIABLE_PARAMS if k in query and str(query[k]) != str(default_query.get(k)))


def register_name_tokens(entries: list[dict]) -> dict[str, str]:
    """Lower-case name -> register id, for the id itself and the first word of the title (5+ characters)."""
    names = {}
    for e in entries:
        names[e["id"].lower()] = e["id"]
        first = (e.get("title") or "").split()[0] if (e.get("title") or "").split() else ""
        if len(first) >= 5:
            names[first.lower()] = e["id"]
    return names


def register_name_in(query: str, names: dict[str, str]) -> str | None:
    """The register id whose name occurs as a whole word or phrase in a query, or None."""
    low = (query or "").lower()
    for name, rid in names.items():
        if re.search(r"(?<![a-z0-9])" + re.escape(name) + r"(?![a-z0-9])", low):
            return rid
    return None
