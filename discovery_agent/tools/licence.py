"""Licence and structured-metadata extraction from dataset landing pages."""
from __future__ import annotations

import json
import re
from html import unescape


def jsonld_datasets(html: str) -> list[dict]:
    """Return every schema.org Dataset object embedded as JSON-LD in a page.

    Many portals (Kaggle, Zenodo, data.gov, Hugging Face, Dataverse, CKAN sites) embed one.
    It is the most reliable machine-readable description of a dataset when it exists.
    """
    found = []
    for m in re.finditer(r"""(?is)<script[^>]*type=["']application/ld\+json["'][^>]*>(.*?)</script>""", html):
        try:
            data = json.loads(m.group(1).strip())
        except json.JSONDecodeError:
            continue
        items = data if isinstance(data, list) else data.get("@graph", [data]) if isinstance(data, dict) else []
        for item in items:
            if isinstance(item, dict) and "Dataset" in str(item.get("@type", "")):
                found.append(item)
    return found


def summarise_jsonld_dataset(d: dict) -> dict:
    """Keep the fields that matter for discovery, clipped for the model."""
    def name_of(v):
        if isinstance(v, list):
            return [name_of(x) for x in v][:5]
        if isinstance(v, dict):
            return v.get("name") or v.get("url") or v.get("@id")
        return v

    def clip(v, n=600):
        v = re.sub(r"<[^>]+>", " ", str(v)) if v is not None else None
        return None if v is None else (" ".join(v.split())[:n])

    dist = d.get("distribution") or []
    dist = dist if isinstance(dist, list) else [dist]
    return {
        "name": d.get("name"), "description": clip(d.get("description")),
        "license": d.get("license"), "creator": name_of(d.get("creator")), "publisher": name_of(d.get("publisher")),
        "datePublished": d.get("datePublished"), "dateModified": d.get("dateModified"),
        "temporalCoverage": d.get("temporalCoverage"), "spatialCoverage": name_of(d.get("spatialCoverage")),
        "isAccessibleForFree": d.get("isAccessibleForFree"), "keywords": clip(d.get("keywords"), 300),
        "variableMeasured": name_of(d.get("variableMeasured")),
        "distribution": [{k: x.get(k) for k in ("contentUrl", "encodingFormat", "fileFormat", "contentSize", "requiresSubscription", "name")
                          if isinstance(x, dict) and x.get(k) is not None} for x in dist[:10]],
    }


# ---------------------------------------------------------------------------
# LEARNER TODO (G1): find the licence of ANY dataset from its landing page
# ---------------------------------------------------------------------------
# Without this, every dataset link ends up LIC-UNKNOWN (a blocker) and verdicts are wrong.
#
# Contract (tests/test_learner_gaps.py::test_g1_* checks it):
#   extract_licence(html: str, jsonld: list[dict] | None = None) -> dict with EXACTLY these keys
#     licence_name : normalised name, one of e.g. "CC BY 4.0", "CC BY-SA 4.0", "CC BY-NC 4.0", "CC BY-NC-SA 4.0",
#                    "CC BY-ND 4.0", "CC0 1.0", "ODbL 1.0", "OGL v3.0", "MIT", "Apache-2.0"; None if not found
#                    or if the page says the licence is unknown/unspecified
#     licence_url  : the licence URL you found, or None
#     snippet      : the text or JSON-LD value you read it from (<= 400 chars), or None
#     found_in     : "json-ld" | "link" | "text" | None
#
# Order of evidence: JSON-LD "license" (string URL, or {"name", "url"}) first; then links to
# creativecommons.org / opendatacommons.org / nationalarchives.gov.uk (OGL) / choosealicense.com;
# then sentences such as "licensed under a Creative Commons Attribution 4.0 International (CC BY 4.0) license".
# jsonld defaults to jsonld_datasets(html) when None. Never guess: return None values when unsure.
# Closed table of Creative Commons suffixes. Anything outside it is unrecognised, never guessed.
_CC_NAMES = {
    "": "CC BY", "-sa": "CC BY-SA", "-nc": "CC BY-NC", "-nd": "CC BY-ND",
    "-nc-sa": "CC BY-NC-SA", "-nc-nd": "CC BY-NC-ND",
}
# The suffix group is greedy, so "BY-NC-SA" is read whole and can never be cut down to "BY" or "BY-NC".
# Plain "Attribution" wording is never used as evidence of a licence.
_CC_URL_RE = re.compile(r"creativecommons\.org/licenses/by((?:-(?:nc|sa|nd))*)/(\d\.\d)", re.I)
_CC_NAME_RE = re.compile(r"\bCC\s*BY((?:-(?:NC|SA|ND))*)\s*(\d\.\d)\b", re.I)
_CC0_RE = re.compile(r"\bCC0\s*1\.0\b", re.I)
_ODBL_RE = re.compile(r"\bODbL\s*1\.0\b", re.I)
_OGL_RE = re.compile(r"\bOpen Government Licen[cs]e\s*v?3\.0\b", re.I)
_UNKNOWN_WORDS = {"unknown", "unspecified", "not specified", "none", "n/a"}


def _cc(suffix: str, version: str) -> str | None:
    name = _CC_NAMES.get(suffix.lower())
    return f"{name} {version}" if name else None


def _canonical_url(url: str) -> str | None:
    m = _CC_URL_RE.search(url)
    if m:
        return _cc(m.group(1), m.group(2))
    if re.search(r"creativecommons\.org/publicdomain/zero/1\.0|choosealicense\.com/licenses/cc0-1\.0", url, re.I):
        return "CC0 1.0"
    if re.search(r"opendatacommons\.org/licenses/odbl/1\.0", url, re.I):
        return "ODbL 1.0"
    if re.search(r"nationalarchives\.gov\.uk/doc/open-government-licence/version/3", url, re.I):
        return "OGL v3.0"
    return None


def _canonical_name(name: str) -> str | None:
    m = _CC_NAME_RE.search(name)
    if m:
        return _cc(m.group(1), m.group(2))
    if _CC0_RE.search(name):
        return "CC0 1.0"
    if _ODBL_RE.search(name):
        return "ODbL 1.0"
    if _OGL_RE.search(name):
        return "OGL v3.0"
    return None


def _result(name, url, snippet, found_in) -> dict:
    return {"licence_name": name, "licence_url": url or None,
            "snippet": snippet[:400] if snippet else None, "found_in": found_in}


def _from_jsonld(datasets: list[dict]) -> dict | None:
    """The first Dataset that has a 'license' key decides. Returns None to fall through to links and text."""
    for d in datasets:
        if "license" not in d:
            continue
        value = d["license"]
        if isinstance(value, list):
            value = value[0] if value else None
        if isinstance(value, str):
            text = value.strip()
            name, url = (None, text) if text.startswith("http") else (text or None, None)
        elif isinstance(value, dict):
            name = str(value.get("name") or "").strip() or None
            url = str(value.get("url") or "").strip() or None
        else:
            return None
        if not name and not url:
            return None
        snippet = json.dumps(value, ensure_ascii=False)
        from_url = _canonical_url(url) if url else None
        if from_url:  # the URL is authoritative when it names a known licence
            return _result(from_url, url, snippet, "json-ld")
        if name and name.lower().strip(" .") in _UNKNOWN_WORDS:  # explicit "Unknown" is a final answer
            return _result(None, url, snippet, "json-ld")
        from_name = _canonical_name(name) if name else None
        if from_name:
            return _result(from_name, url, snippet, "json-ld")
        return None  # unrecognised: fall through to links and text
    return None


def _from_links(html: str) -> dict | None:
    for m in re.finditer(r"(?is)<a\b[^>]*?\bhref\s*=\s*[\"']([^\"']+)[\"'][^>]*>(.*?)</a>", html):
        href = unescape(m.group(1)).strip()
        name = _canonical_url(href)
        if name:
            text = " ".join(unescape(re.sub(r"<[^>]+>", " ", m.group(2))).split())
            return _result(name, href, text or href, "link")
    return None


def _from_text(html: str) -> dict | None:
    body = re.sub(r"(?is)<(script|style)\b.*?</\1\s*>", " ", html)
    text = " ".join(unescape(re.sub(r"<[^>]+>", " ", body)).split())
    resolvers = (
        (_CC_NAME_RE, lambda m: _cc(m.group(1), m.group(2))),
        (_CC0_RE, lambda m: "CC0 1.0"),
        (_ODBL_RE, lambda m: "ODbL 1.0"),
        (_OGL_RE, lambda m: "OGL v3.0"),
    )
    for rx, resolve in resolvers:
        m = rx.search(text)
        name = resolve(m) if m else None
        if name:
            window = text[max(0, m.start() - 150): m.end() + 150]
            return _result(name, None, window, "text")
    return None


def extract_licence(html: str, jsonld: list[dict] | None = None) -> dict:
    """Licence of a dataset landing page. Order: JSON-LD, then licence links, then text.

    jsonld=None reads the page's own JSON-LD; jsonld=[] means "no JSON-LD". Unknown or unrecognised
    values are never turned into a licence name."""
    datasets = jsonld_datasets(html) if jsonld is None else jsonld
    for step in (lambda: _from_jsonld(datasets), lambda: _from_links(html), lambda: _from_text(html)):
        found = step()
        if found is not None:
            return found
    return _result(None, None, None, None)
