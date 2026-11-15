import json, glob, os, sys
ROOT = sys.argv[1]  # directory containing UC1/ and UC2/ (outputs or a snapshot)

def accepted_submission(t):
    """Return (tool_name, input) of the submission whose tool_result was 'accepted'."""
    uses = {}
    accepted = None
    for m in t["messages"]:
        c = m.get("content")
        if not isinstance(c, list):
            continue
        for b in c:
            if b.get("type") == "tool_use" and b.get("name", "").startswith("submit"):
                uses[b["id"]] = (b["name"], b["input"])
            if b.get("type") == "tool_result" and b.get("tool_use_id") in uses:
                if b.get("content") == "accepted" and not b.get("is_error"):
                    accepted = uses[b["tool_use_id"]]
    return accepted

def diff_keys(a, b):
    out = []
    for k in sorted(set(a) | set(b)):
        if a.get(k) != b.get(k):
            out.append(k)
    return out

for uc in ("UC1", "UC2"):
    d = os.path.join(ROOT, uc)
    if not os.path.isdir(os.path.join(d, "transcripts")):
        continue
    for f in sorted(glob.glob(os.path.join(d, "transcripts", "*.json"))):
        name = os.path.basename(f)
        acc = accepted_submission(json.load(open(f)))
        if acc is None:
            print(f"{uc} {name}: NO accepted submission"); continue
        tool, payload = acc
        if name.startswith("profiler__"):
            sid = payload.get("source_id")
            out_path = os.path.join(d, "records", f"{sid}.json")
            if not os.path.exists(out_path):
                print(f"{uc} {name}: output missing {out_path}"); continue
            out = json.load(open(out_path))
            same = payload == out
            print(f"{uc} {name}: tool={tool} source={sid} identical_to_record={same}" + ("" if same else f" differing_keys={diff_keys(payload, out)}"))
        elif name == "risk_assessor.json":
            out = json.load(open(os.path.join(d, "risk_assessment.json")))
            same = payload == out
            print(f"{uc} {name}: tool={tool} identical_to_risk_assessment={same}" + ("" if same else f" differing_keys={diff_keys(payload, out)}"))
        elif name == "memo_writer.json":
            memo_path = os.path.join(d, "feasibility_memo.md")
            text = open(memo_path, encoding="utf-8").read()
            keys = [k for k, v in payload.items() if isinstance(v, str) and len(v) > 200]
            matches = {k: (payload[k] == text) for k in keys}
            print(f"{uc} {name}: tool={tool} submitted_keys={list(payload.keys())} long_text_fields_equal_to_memo={matches}")
            if keys and not matches[keys[0]]:
                a, b = payload[keys[0]], text
                i = next((j for j in range(min(len(a), len(b))) if a[j] != b[j]), min(len(a), len(b)))
                print(f"   first difference at char {i}: submitted={a[i:i+120]!r} | file={b[i:i+120]!r} | len submitted={len(a)} file={len(b)}")
        elif name == "scout.json":
            out = json.load(open(os.path.join(d, "candidates.json")))
            same = payload == out
            print(f"{uc} {name}: tool={tool} identical_to_candidates={same}" + ("" if same else f" differing_keys={diff_keys(payload, out)}"))
        elif name == "planner.json":
            out = json.load(open(os.path.join(d, "search_plan.json")))
            same = payload == out
            print(f"{uc} {name}: tool={tool} identical_to_search_plan={same}" + ("" if same else f" differing_keys={diff_keys(payload, out)}"))
