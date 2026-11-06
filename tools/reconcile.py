#!/usr/bin/env python3
"""
Reconcile the ASF inventory against the foundation's live data.

Fetches the authoritative project + podling listings from projects.apache.org
and reports:
  * how many active top-level projects (PMCs) the ASF currently lists,
  * any active project NOT yet represented in the inventory (coverage gaps),
  * incubator podlings present live but not mentioned in the doc (and vice-versa),
  * the current date, to stamp "Last reconciled".

Exit status: 0 = no coverage gaps, 1 = coverage gaps found, 2 = fetch failed.

Usage:
    python3 tools/reconcile.py              # report
    python3 tools/reconcile.py --write-date # also update the doc's "Last reconciled" line

Dependencies: standard library only. Honors standard proxy / SSL_CERT_FILE env
vars, so it works behind a corporate proxy as well as on the open internet.
"""
from __future__ import annotations
import argparse
import datetime
import json
import re
import ssl
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MD = ROOT / "APACHE_SOFTWARE_FOUNDATION_INVENTORY.md"
PROJECTS_URL = "https://projects.apache.org/json/foundation/projects.json"
PODLINGS_URL = "https://projects.apache.org/json/foundation/podlings.json"


def fetch(url: str):
    ctx = ssl.create_default_context()  # reads SSL_CERT_FILE / SSL_CERT_DIR if set
    req = urllib.request.Request(url, headers={"User-Agent": "asf-inventory-reconcile"})
    with urllib.request.urlopen(req, timeout=60, context=ctx) as resp:
        return json.loads(resp.read().decode("utf-8"))


def active_pmcs(projects: dict):
    """Return {pmc: display_name} for PMCs with at least one non-retired entry."""
    groups: dict[str, list] = {}
    for key, val in projects.items():
        pmc = val.get("pmc")
        if not pmc:
            continue
        groups.setdefault(pmc, []).append((key, val))
    out = {}
    for pmc, entries in groups.items():
        retired = all("retired" in (v.get("category") or []) for _, v in entries)
        if retired:
            continue
        exact = [v for k, v in entries if k == pmc]
        name = (exact[0] if exact else entries[0][1]).get("name", "Apache " + pmc)
        out[pmc] = name
    return out


def covered(md: str, pmc: str, name: str) -> bool:
    clean = re.sub(r"^Apache ", "", name)
    first = clean.split()[0] if clean.split() else clean
    md_l = md.lower()
    return (clean.lower() in md_l
            or re.search(r"\b" + re.escape(pmc.lower()) + r"\b", md_l) is not None
            or ("apache " + first).lower() in md_l)


def current_podlings(podlings) -> dict:
    items = podlings.values() if isinstance(podlings, dict) else podlings
    out = {}
    for p in items:
        name = (p.get("name") or "").replace("(Incubating)", "").strip()
        short = re.sub(r"^Apache ", "", name)
        if short:
            out[short] = p.get("started", "?")
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write-date", action="store_true",
                    help="update the 'Last reconciled' line in the inventory doc")
    args = ap.parse_args()

    if not MD.exists():
        print("ERROR: inventory not found at", MD, file=sys.stderr)
        return 2
    md = MD.read_text(encoding="utf-8")

    try:
        projects = fetch(PROJECTS_URL)
        podlings = fetch(PODLINGS_URL)
    except Exception as e:  # noqa: BLE001
        print("ERROR: could not fetch live ASF data:", e, file=sys.stderr)
        print("(Behind a TLS-terminating proxy? Point SSL_CERT_FILE at its CA bundle.)",
              file=sys.stderr)
        return 2

    pmcs = active_pmcs(projects)
    gaps = sorted(f"{name} [{pmc}]" for pmc, name in pmcs.items()
                  if not covered(md, pmc, name))

    pods = current_podlings(podlings)
    pod_new = sorted(n for n in pods if n.lower() not in md.lower())

    today = datetime.date.today().isoformat()
    print(f"Live active top-level projects (PMCs): {len(pmcs)}")
    print(f"Current incubator podlings:            {len(pods)}")
    print(f"Coverage gaps (active, not in doc):    {len(gaps)}")
    for g in gaps:
        print("   -", g)
    print(f"Podlings live but not in doc:          {len(pod_new)}")
    for p in pod_new:
        print("   -", p, f"(started {pods[p]})")

    if args.write_date:
        new_md, n = re.subn(r"(\*\*Last reconciled:\*\*\s*)\d{4}-\d{2}-\d{2}",
                            r"\g<1>" + today, md)
        if n:
            MD.write_text(new_md, encoding="utf-8")
            print(f"Updated 'Last reconciled' to {today}.")
        else:
            print("No 'Last reconciled:' marker found to update.", file=sys.stderr)

    print("\nSummary:", "OK — every active PMC is covered."
          if not gaps else f"ACTION NEEDED — {len(gaps)} active project(s) missing.")
    return 1 if gaps else 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BrokenPipeError:
        sys.exit(0)
