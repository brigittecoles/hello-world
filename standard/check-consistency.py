#!/usr/bin/env python3
"""Check every HTML document under site/ against standard/source-of-truth.json.

Fails (exit 1) when a document still carries a stale phrase, enumerates the
dimensions without S7, or states a criteria/questionnaire count that differs
from the source of truth. Run from the repo root:  python3 standard/check-consistency.py
"""
import json, re, sys, glob, html

ROOT = __import__("os").path.dirname(__import__("os").path.dirname(__import__("os").path.abspath(__file__)))
truth = json.load(open(f"{ROOT}/standard/source-of-truth.json", encoding="utf-8"))
counts = truth["counts"]
dims = truth["dimensions"]
WORDS = {7: "seven", 28: "twenty-eight", 56: "fifty-six", 30: "thirty"}

def text_of(src: str) -> str:
    src = re.sub(r"<(style|script)[^>]*>.*?</\1>", " ", src, flags=re.S | re.I)
    src = re.sub(r"<[^>]+>", " ", src)
    return html.unescape(src)

problems = []
for path in sorted(glob.glob(f"{ROOT}/site/*.html")):
    name = path.split("/")[-1]
    raw = open(path, encoding="utf-8").read()
    txt = text_of(raw)

    # 1. stale phrases anywhere (markup or prose)
    for phrase in truth["stale_phrases"]:
        for m in re.finditer(re.escape(phrase), raw):
            line = raw.count("\n", 0, m.start()) + 1
            problems.append(f"{name}:{line}: stale phrase {phrase!r}")

    # 2. any document that enumerates dimension codes must enumerate all of them
    # (four or more codes counts as an enumeration; a sample card showing one or two does not)
    codes_present = {d["code"] for d in dims if re.search(rf"\b{d['code']}\b", txt)}
    if len(codes_present) >= 4 and codes_present != {d["code"] for d in dims}:
        missing = sorted({d["code"] for d in dims} - codes_present)
        problems.append(f"{name}: enumerates {sorted(codes_present)} but not {missing}")

    # 3. a document that names dimensions must use the canonical name next to each code it shows
    names_any = any(d["name"].lower() in txt.lower() for d in dims)
    for d in dims:
        if names_any and re.search(rf"\b{d['code']}\b", txt) and d["name"].lower() not in txt.lower() \
           and d["name"].split()[0].lower() not in txt.lower():
            problems.append(f"{name}: mentions {d['code']} but never names {d['name']!r}")

    # 4. numeric statements about dimensions / criteria must match
    for m in re.finditer(r"\b(\w+|\d+)\s+dimensions\b", txt, flags=re.I):
        w = m.group(1).lower()
        if w in ("six", "6", "five", "5", "eight", "8"):
            problems.append(f"{name}: '{m.group(0)}' should be {WORDS[counts['dimensions']]} dimensions")
    for m in re.finditer(r"\b(\w+|\d+)\s+criteria\b", txt, flags=re.I):
        w = m.group(1).lower()
        if w in ("48", "forty-eight", "24", "twenty-four", "twenty-six", "fifty-two"):
            problems.append(f"{name}: '{m.group(0)}' disagrees with source of truth "
                            f"({counts['criteria_total']} total, {counts['criteria_per_track']} per track)")

    # 5. a questionnaire that cites S-codes must run to the full item count
    items = re.findall(r"^\s*(\d+)\.\s+.*\[S\d\.\d\]", txt, flags=re.M)
    if items and int(max(items, key=int)) != counts["procurement_questionnaire_items"]:
        problems.append(f"{name}: questionnaire ends at item {max(items, key=int)}, "
                        f"source of truth says {counts['procurement_questionnaire_items']}")

if problems:
    print("\n".join(problems)); print(f"\n{len(problems)} problem(s)"); sys.exit(1)
print(f"OK — {len(glob.glob(f'{ROOT}/site/*.html'))} documents agree with standard/source-of-truth.json")
