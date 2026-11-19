"""Search the web through the gateway and print the answer with its citation URLs.

Usage:
    python scripts/web_search.py "<query>"

Standard library only. Configuration comes from the environment:
    ANTHROPIC_BASE_URL     gateway base URL, without /v1 (required)
    ANTHROPIC_AUTH_TOKEN   bearer token (required; never printed)
    WEB_SEARCH_MODEL       model id (optional, default gemini-3.8-flash)

Results are leads, not verified sources. Check each URL on its publisher's page.
"""
import json
import os
import sys
import urllib.error
import urllib.request

DEFAULT_MODEL = "gemini-3.8-flash"
TIMEOUT_S = 60


def fail(message: str, code: int = 1) -> None:
    print(message, file=sys.stderr)
    sys.exit(code)


def citation_urls(payload: dict) -> list[str]:
    """Collect citation URLs from the shapes gateways use: url_citation annotations, a top-level
    citations list, and search result lists. Duplicates are removed, order is kept."""
    found: list[str] = []

    def add(value):
        if isinstance(value, str) and value.startswith(("http://", "https://")):
            found.append(value)
        elif isinstance(value, dict):
            url = value.get("url") or value.get("uri") or value.get("link")
            if isinstance(url, str) and url.startswith(("http://", "https://")):
                found.append(url)

    for choice in payload.get("choices") or []:
        message = choice.get("message") or {}
        for ann in message.get("annotations") or []:
            if isinstance(ann, dict):
                add(ann.get("url_citation") or ann)
    for item in payload.get("citations") or []:
        add(item)
    for item in payload.get("search_results") or []:
        add(item)
    return list(dict.fromkeys(found))


def answer_text(payload: dict) -> str:
    choices = payload.get("choices") or []
    if not choices:
        return ""
    content = (choices[0].get("message") or {}).get("content")
    if isinstance(content, list):  # content parts
        return "".join(p.get("text", "") for p in content if isinstance(p, dict))
    return content or ""


def main() -> None:
    if len(sys.argv) != 2 or not sys.argv[1].strip():
        fail('usage: python scripts/web_search.py "<query>"', 2)
    query = sys.argv[1]

    base = os.environ.get("ANTHROPIC_BASE_URL", "").strip().rstrip("/")
    token = os.environ.get("ANTHROPIC_AUTH_TOKEN", "").strip()
    missing = [name for name, value in (("ANTHROPIC_BASE_URL", base), ("ANTHROPIC_AUTH_TOKEN", token)) if not value]
    if missing:
        fail(f"web_search: missing environment variable(s): {', '.join(missing)}. Export them in this shell.")
    if base.endswith("/v1"):
        fail("web_search: ANTHROPIC_BASE_URL must not end with /v1 (the script adds it).")
    model = os.environ.get("WEB_SEARCH_MODEL", "").strip() or DEFAULT_MODEL

    body = json.dumps({
        "model": model,
        "messages": [{"role": "user", "content": query}],
        "web_search_options": {},
    }).encode("utf-8")
    request = urllib.request.Request(
        f"{base}/v1/chat/completions",
        data=body,
        method="POST",
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT_S) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")[:300]
        fail(f"web_search: gateway returned HTTP {exc.code} for model {model!r}. Response starts: {detail}")
    except urllib.error.URLError as exc:
        fail(f"web_search: could not reach the gateway ({exc.reason}).")
    except TimeoutError:
        fail(f"web_search: no response within {TIMEOUT_S} seconds.")

    try:
        payload = json.loads(raw)
    except json.JSONDecodeError:
        fail("web_search: the gateway response was not JSON.")

    text = answer_text(payload).strip()
    urls = citation_urls(payload)
    if not text:
        fail("web_search: the response contained no answer text.")

    print(text)
    print()
    print("Citations:" if urls else "Citations: none returned (do not use this result as a source).")
    for url in urls:
        print(url)


if __name__ == "__main__":
    main()
