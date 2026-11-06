#!/usr/bin/env python3
"""
Build structured data + an interactive viewer from the ASF inventory Markdown.

Reads:   APACHE_SOFTWARE_FOUNDATION_INVENTORY.md
Writes:  apache_inventory.json          (one record per project; canonical data)
         apache_inventory.html          (self-contained, filterable viewer)

The data is parsed straight from the Markdown so it cannot drift from the
document. Re-run after editing the inventory:

    python3 tools/build_inventory.py

No third-party dependencies (standard library only).
"""
from __future__ import annotations
import json
import re
import sys
import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MD = ROOT / "APACHE_SOFTWARE_FOUNDATION_INVENTORY.md"
JSON_OUT = ROOT / "apache_inventory.json"
HTML_OUT = ROOT / "apache_inventory.html"

STATUS_BY_EMOJI = {
    "\U0001F7E2": "active",        # 🟢
    "\U0001F95A": "incubating",    # 🥚
    "\U0001F5C4": "attic",         # 🗄️ (base codepoint; may be followed by VS16)
    "\U0001F7E1": "low-activity",  # 🟡
}

HEAD_RE = re.compile(r"^\*\*(?P<name>.+?)\*\*(?P<extra>.*?)\s+—\s+\*(?P<meta>.+?)\*\s*$")
CAT_RE = re.compile(r"^###\s+(\d+)\.\s+(.*\S)\s*$")
SUBCAT_RE = re.compile(r"^####\s+(\d+)\.(\d+)\s+(.*\S)\s*$")
PART_RE = re.compile(r"^##\s+Part\s+(\d+)")
# label:value segments on a bullet line, split on " · " between them
SEG_RE = re.compile(r"\*\*([A-Za-z][A-Za-z &/]*?):\*\*\s*(.*?)(?=\s+·\s+\*\*[A-Za-z][A-Za-z &/]*?:\*\*|$)")

FIELD_KEYS = {
    "description": "description",
    "function": "function",
    "function & modules": "function",
    "patterns": "patterns",
    "use cases": "use_cases",
    "interfaces": "interfaces",
    "needs": "needs",
    "pairs with": "pairs_with",
    "alternatives": "alternatives",
    "standards": "standards",
    "maturity": "maturity",
    "leverage note": "leverage_note",
}

LINK_RE = re.compile(r"\[([^\]]+)\]\([^)]+\)")


def clean(text: str) -> str:
    if not text:
        return ""
    text = LINK_RE.sub(r"\1", text)        # [label](url) -> label
    text = text.replace("**", "").replace("`", "")
    text = re.sub(r"(?<!\*)\*(?!\*)", "", text)  # stray single * (italics)
    text = text.replace("·", "·")
    return re.sub(r"\s+", " ", text).strip()


def parse_meta(meta: str):
    """meta like 'Java/Scala · 🟢 Active (TLP, 2026)' -> (languages, status, status_label)."""
    meta = meta.strip()
    if meta.startswith("(see") or meta.startswith("("):
        return ([], "pointer", clean(meta))
    parts = [p.strip() for p in meta.split("·")]
    languages, status, status_label = [], "", ""
    for part in parts:
        emoji_hit = next((s for e, s in STATUS_BY_EMOJI.items() if e in part), None)
        if emoji_hit:
            status = emoji_hit
            status_label = clean(re.sub(r"[\U0001F300-\U0001FAFF️]", "", part))
        elif not languages:
            langs = re.split(r"[/,+]| and ", part)
            languages = [l.strip() for l in langs if l.strip()]
    return (languages, status or "unknown", status_label or status)


def derive_form(interfaces: str, needs: str) -> str:
    t = (interfaces + " " + needs).lower()
    checks = [
        ("both", "both ("),
        ("both", "server + embeddable"),
        ("both", "embeddable server"),
        ("library", "embeddable library"),
        ("library", "embeddable runtime/library"),
        ("service", "cluster service"),
        ("service", "standalone service"),
        ("service", "gateway service"),
        ("service", "broker service"),
        ("format", "file format"),
        ("format", "table format"),
        ("tool", "build tool"),
        ("tool", "tooling"),
        ("tool", " tool."),
        ("platform", "platform"),
        ("framework", "framework"),
        ("runtime", "runtime"),
        ("language", "language"),
        ("firmware", "firmware/os"),
        ("library", "library"),
        ("service", "service"),
    ]
    for form, needle in checks:
        if needle in t:
            return form
    return ""


def split_list(value: str):
    if not value:
        return []
    value = re.sub(r"\.$", "", value.strip())
    items = re.split(r"[;,]| · ", value)
    return [i.strip() for i in items if i.strip()]


def normalize_name(s: str) -> str:
    s = re.sub(r"^Apache ", "", s)
    s = re.sub(r"\([^)]*\)", "", s)
    return re.sub(r"\s+", " ", s).strip().lower()


AVOID_ROW = re.compile(r"^\|\s*\*\*(.+?)\*\*\s*\|(.+?)\|(.+?)\|\s*$")


def parse_avoid_when(md: str) -> dict:
    """Map normalized project name -> 'avoid … → prefer …' from the §6.6 table."""
    out = {}
    in66 = False
    for line in md.split("\n"):
        if re.match(r"^###\s+6\.6\b", line):
            in66 = True
            continue
        if in66 and re.match(r"^(##\s|###\s)", line):
            break
        if in66:
            m = AVOID_ROW.match(line)
            if m and "Avoid it when" not in line:
                name = normalize_name(clean(m.group(1)))
                avoid = clean(m.group(2))
                prefer = clean(m.group(3))
                if name and avoid:
                    out[name] = f"{avoid} → prefer {prefer}"
    return out


def finalize(rec: dict) -> dict:
    rec.setdefault("avoid_when", "")
    rec["form"] = derive_form(rec.get("interfaces", ""), rec.get("needs", ""))
    for k in ("pairs_with", "alternatives", "standards", "languages"):
        if k == "languages":
            continue
        rec[k + "_list"] = split_list(rec.get(k, ""))
    blob = " ".join(
        str(rec.get(k, ""))
        for k in ("name", "category", "subgroup", "description", "function", "patterns",
                  "use_cases", "interfaces", "needs", "pairs_with", "alternatives",
                  "standards", "maturity", "leverage_note")
    ) + " " + " ".join(rec.get("languages", []))
    rec["search"] = blob.lower()
    return rec


def parse(md: str):
    lines = md.split("\n")
    records = []
    cat_num, cat_title, subgroup = 0, "", ""
    part = 0
    i = 0
    n = len(lines)
    while i < n:
        line = lines[i]
        mp = PART_RE.match(line)
        if mp:
            part = int(mp.group(1))
        msc = SUBCAT_RE.match(line)
        if msc:
            subgroup = clean(msc.group(3))
        mc = CAT_RE.match(line)
        if mc:
            cat_num = int(mc.group(1))
            cat_title = clean(mc.group(2))
            subgroup = ""
        mh = HEAD_RE.match(line) if line.startswith("**") else None
        if mh:
            raw_name = mh.group("name") + (mh.group("extra") or "")
            name = clean(raw_name.replace("** & **", " & ").replace("** / **", " / "))
            languages, status, status_label = parse_meta(mh.group("meta"))
            rec = {
                "name": name, "category": cat_title, "category_num": cat_num,
                "subgroup": subgroup, "languages": languages, "status": status,
                "status_label": status_label, "description": "", "function": "",
                "patterns": "", "use_cases": "", "interfaces": "", "needs": "",
                "pairs_with": "", "alternatives": "", "standards": "", "maturity": "",
                "leverage_note": "", "source": "card",
            }
            j = i + 1
            first_plain = ""
            while j < n and lines[j].lstrip().startswith("-"):
                bullet = lines[j].strip().lstrip("-").strip()
                segs = SEG_RE.findall(bullet)
                for label, value in segs:
                    key = FIELD_KEYS.get(label.strip().lower())
                    if key and not rec.get(key):
                        rec[key] = clean(value)
                if not segs and not first_plain and bullet:
                    first_plain = clean(bullet)
                j += 1
            if not rec["description"] and first_plain:
                rec["description"] = first_plain
            records.append(finalize(rec))
            i = j
            continue
        # Commons component table (section 24)
        if cat_num == 24 and line.startswith("| **Commons"):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) >= 2 and "Component" not in cells[0]:
                name = clean(cells[0]).replace("Commons ", "Apache Commons ", 1)
                rec = {
                    "name": name, "category": cat_title, "category_num": 24,
                    "subgroup": "", "languages": ["Java"], "status": "active",
                    "status_label": "Active", "description": clean(cells[1]),
                    "function": "", "patterns": "", "use_cases": "",
                    "interfaces": "Java library (Maven: org.apache.commons / commons-*). Embeddable library.",
                    "needs": "JVM", "pairs_with": "virtually every JVM project",
                    "alternatives": "Google Guava, Eclipse Collections (ext)",
                    "standards": "", "maturity": "Among the most-depended-on JVM libraries. Apache-2.0.",
                    "leverage_note": "", "source": "commons-table",
                }
                records.append(finalize(rec))
            i += 1
            continue
        # Incubator podling table (Part 3)
        if part == 3 and line.startswith("| **") and "|" in line:
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) >= 3 and cells[0].startswith("**") and "Podling" not in cells[0]:
                raw = clean(cells[0])
                names = [p.strip() for p in raw.split("/")] if "/" in raw else [raw]
                for nm in names:
                    rec = {
                        "name": "Apache " + nm if not nm.startswith("Apache") else nm,
                        "category": "Incubator podling", "category_num": 300,
                        "subgroup": clean(cells[1]), "languages": [], "status": "incubating",
                        "status_label": "Incubating", "description": clean(cells[2]),
                        "function": "", "patterns": "", "use_cases": "",
                        "interfaces": "", "needs": "", "pairs_with": "", "alternatives": "",
                        "standards": "", "maturity": "Incubating — pre-graduation; APIs and governance still stabilizing.",
                        "leverage_note": "", "source": "podling-table",
                    }
                    records.append(finalize(rec))
            i += 1
            continue
        i += 1

    # de-duplicate by name, preferring richer (card) records
    by_name = {}
    for r in records:
        key = r["name"].lower()
        if key not in by_name or len(r.get("description", "")) > len(by_name[key].get("description", "")):
            by_name[key] = r
    return list(by_name.values())


# ---------------------------------------------------------------------------
HTML_TEMPLATE = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Apache Project Finder</title>
<style>
/* Layout: sticky search/filter rail over a responsive card grid.
   Palette grounded in the Apache feather's brick red against warm neutrals. */
:root{
  --bg:#faf8f5; --surface:#ffffff; --surface-2:#f3efe9; --fg:#1c1a18; --muted:#6b6460;
  --line:#e7e1da; --accent:#b5231f; --accent-weak:#f5e2e0;
  --ok:#2f7d4f; --warn:#9a6a12; --idle:#8a8178; --info:#2f6f9f;
  --radius:10px; --mono:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;
  --sans:system-ui,-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;
  color-scheme:light;
}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){
  --bg:#161412; --surface:#201d1a; --surface-2:#2a2621; --fg:#ece7e1; --muted:#a69e96;
  --line:#322d28; --accent:#e4635d; --accent-weak:#3a2420;
  --ok:#5bbd83; --warn:#d6a24a; --idle:#9c938a; --info:#6aa6cf; color-scheme:dark;
}}
:root[data-theme="dark"]{
  --bg:#161412; --surface:#201d1a; --surface-2:#2a2621; --fg:#ece7e1; --muted:#a69e96;
  --line:#322d28; --accent:#e4635d; --accent-weak:#3a2420;
  --ok:#5bbd83; --warn:#d6a24a; --idle:#9c938a; --info:#6aa6cf; color-scheme:dark;
}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--fg);font-family:var(--sans);line-height:1.5;
  font-size:15px;-webkit-text-size-adjust:100%}
.wrap{max-width:1180px;margin:0 auto;padding-left:max(16px,env(safe-area-inset-left,0px));
  padding-right:max(16px,env(safe-area-inset-right,0px))}
header.top{padding-block:22px 6px}
h1{font-size:1.5rem;margin:0;letter-spacing:-.01em;text-wrap:balance}
.sub{color:var(--muted);margin:4px 0 0;font-size:.92rem}
a{color:var(--accent)}
.controls{position:sticky;top:env(safe-area-inset-top,0px);z-index:5;background:var(--bg);
  padding-block:12px;border-bottom:1px solid var(--line)}
.row{display:flex;flex-wrap:wrap;gap:8px;align-items:center}
input[type=search],select{font:inherit;color:var(--fg);background:var(--surface);
  border:1px solid var(--line);border-radius:8px;padding:8px 10px;min-width:0}
input[type=search]{flex:1 1 240px}
select{flex:0 0 auto}
label.f{display:flex;flex-direction:column;gap:3px;font-size:.72rem;color:var(--muted);
  text-transform:uppercase;letter-spacing:.06em;font-family:var(--mono)}
.chips{display:flex;flex-wrap:wrap;gap:6px;margin-top:8px}
.chip{font:inherit;font-size:.8rem;cursor:pointer;border:1px solid var(--line);
  background:var(--surface);color:var(--fg);border-radius:999px;padding:4px 11px}
.chip[aria-pressed=true]{background:var(--accent);border-color:var(--accent);color:#fff}
button.link{background:none;border:none;color:var(--accent);cursor:pointer;font:inherit;padding:4px}
.meta-row{display:flex;flex-wrap:wrap;gap:10px;align-items:baseline;margin:10px 0 4px}
.count{font-family:var(--mono);font-variant-numeric:tabular-nums;color:var(--muted);font-size:.85rem}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(310px,1fr));gap:14px;
  padding-block:14px 40px;align-items:start}
.card{background:var(--surface);border:1px solid var(--line);border-radius:var(--radius);
  padding:14px 15px;min-width:0}
.card h2{font-size:1.02rem;margin:0;display:flex;gap:8px;align-items:baseline;flex-wrap:wrap}
.pill{font-family:var(--mono);font-size:.66rem;text-transform:uppercase;letter-spacing:.05em;
  padding:2px 7px;border-radius:999px;border:1px solid;white-space:nowrap}
.st-active{color:var(--ok);border-color:var(--ok)}
.st-incubating{color:var(--warn);border-color:var(--warn)}
.st-attic{color:var(--idle);border-color:var(--idle)}
.st-low-activity{color:var(--info);border-color:var(--info)}
.st-unknown,.st-pointer{color:var(--muted);border-color:var(--line)}
.cardmeta{font-family:var(--mono);font-size:.72rem;color:var(--muted);margin:7px 0 0;
  display:flex;flex-wrap:wrap;gap:4px 10px}
.desc{margin:9px 0 0}
details{margin-top:9px;border-top:1px solid var(--line);padding-top:8px}
details summary{cursor:pointer;color:var(--accent);font-size:.82rem;font-family:var(--mono)}
dl{margin:9px 0 0;display:grid;grid-template-columns:auto 1fr;gap:4px 10px;font-size:.88rem}
dt{font-family:var(--mono);font-size:.68rem;text-transform:uppercase;letter-spacing:.05em;
  color:var(--muted);padding-top:2px}
dd{margin:0;min-width:0}
mark{background:var(--accent-weak);color:inherit;border-radius:3px;padding:0 1px}
.empty{padding:40px 0;color:var(--muted);text-align:center}
footer{border-top:1px solid var(--line);padding-block:16px 30px;color:var(--muted);font-size:.8rem}
.toggle{margin-left:auto}
@media (max-width:520px){.toggle{margin-left:0}}
:focus-visible{outline:2px solid var(--accent);outline-offset:2px;border-radius:4px}
</style>
</head>
<body>
<div class="wrap">
  <header class="top">
    <div class="row">
      <div>
        <h1>Apache Project Finder</h1>
        <p class="sub">Filter the Apache Software Foundation inventory by what it is, what it needs, and what it speaks.</p>
      </div>
      <button class="chip toggle" id="theme" aria-pressed="false" title="Toggle dark / light">Theme</button>
    </div>
  </header>

  <div class="controls">
    <div class="row">
      <input type="search" id="q" placeholder="Search name, description, interfaces, standards…" aria-label="Search">
      <label class="f">Category<select id="fcat"></select></label>
      <label class="f">Status<select id="fstatus"></select></label>
      <label class="f">Language<select id="flang"></select></label>
      <label class="f">Form<select id="fform"></select></label>
      <label class="f">Sort<select id="fsort">
        <option value="name">Name</option><option value="cat">Category</option>
        <option value="status">Status</option></select></label>
    </div>
    <div class="chips" id="quick" role="group" aria-label="Quick filters">
      <button class="chip" data-tech="JDBC">speaks JDBC</button>
      <button class="chip" data-tech="S3">speaks S3</button>
      <button class="chip" data-tech="Kafka protocol">Kafka protocol</button>
      <button class="chip" data-tech="MQTT">MQTT</button>
      <button class="chip" data-need="ZooKeeper">needs ZooKeeper</button>
      <button class="chip" data-need="HDFS">needs HDFS</button>
      <button class="chip" data-form="library">embeddable</button>
      <button class="chip" data-mat="managed">has managed service</button>
    </div>
  </div>

  <div class="meta-row">
    <span class="count" id="count"></span>
    <button class="link" id="reset" type="button">Reset filters</button>
  </div>

  <div class="grid" id="grid"></div>
  <div class="empty" id="empty" hidden>No projects match these filters.</div>

  <footer class="wrap">
    Generated from <code>APACHE_SOFTWARE_FOUNDATION_INVENTORY.md</code> on __GENERATED__ ·
    __COUNT__ records · reconciled against projects.apache.org on 2026-11-06.
    Status is the most volatile field — re-run <code>tools/build_inventory.py</code> after updating the doc.
  </footer>
</div>

<script id="data" type="application/json">__DATA__</script>
<script>
"use strict";
var DATA = JSON.parse(document.getElementById("data").textContent);
var $ = function(s){return document.querySelector(s)};
var state = {q:"",cat:"",status:"",lang:"",form:"",sort:"name",tech:"",need:"",mat:""};

function store(){try{localStorage.setItem("asf-finder",JSON.stringify(state))}catch(e){}}
function restore(){try{var s=localStorage.getItem("asf-finder");if(s)Object.assign(state,JSON.parse(s))}catch(e){}}

function uniq(key){
  var set={};
  DATA.forEach(function(r){
    var v=r[key];
    if(Array.isArray(v)){v.forEach(function(x){if(x)set[x]=1})}
    else if(v)set[v]=1;
  });
  return Object.keys(set).sort(function(a,b){return a.localeCompare(b)});
}
function fillSelect(el,items,label){
  el.innerHTML="<option value=''>"+label+"</option>"+
    items.map(function(i){return "<option>"+i+"</option>"}).join("");
}
function esc(s){return (s||"").replace(/[&<>"]/g,function(c){
  return {"&":"&amp;","<":"&lt;",">":"&gt;","\"":"&quot;"}[c]})}
function hi(s,terms){
  s=esc(s); if(!terms.length)return s;
  terms.forEach(function(t){
    if(t.length<2)return;
    var re=new RegExp("("+t.replace(/[.*+?^${}()|[\]\\]/g,"\\$&")+")","ig");
    s=s.replace(re,"<mark>$1</mark>");
  });
  return s;
}

function matches(r){
  if(state.cat && r.category!==state.cat)return false;
  if(state.status && r.status!==state.status)return false;
  if(state.form && r.form!==state.form)return false;
  if(state.lang && (r.languages||[]).indexOf(state.lang)<0)return false;
  if(state.need && (r.needs||"").toLowerCase().indexOf(state.need.toLowerCase())<0)return false;
  if(state.mat && (r.maturity||"").toLowerCase().indexOf(state.mat.toLowerCase())<0)return false;
  if(state.tech){
    var t=state.tech.toLowerCase();
    var hay=((r.interfaces||"")+" "+(r.standards||"")+" "+(r.needs||"")+" "+(r.pairs_with||"")).toLowerCase();
    if(hay.indexOf(t)<0)return false;
  }
  if(state.q){
    var terms=state.q.toLowerCase().split(/\s+/).filter(Boolean);
    for(var i=0;i<terms.length;i++){if(r.search.indexOf(terms[i])<0)return false}
  }
  return true;
}

var STATUS_ORDER={active:0,"low-activity":1,incubating:2,attic:3,unknown:4,pointer:5};
function sortRecs(a,b){
  if(state.sort==="cat"){
    if(a.category_num!==b.category_num)return a.category_num-b.category_num;
    return a.name.localeCompare(b.name);
  }
  if(state.sort==="status"){
    var d=(STATUS_ORDER[a.status]||9)-(STATUS_ORDER[b.status]||9);
    if(d)return d; return a.name.localeCompare(b.name);
  }
  return a.name.localeCompare(b.name);
}

var FIELDS=[["function","Function"],["patterns","Patterns"],["use_cases","Use cases"],
  ["interfaces","Interfaces"],["needs","Needs"],["pairs_with","Pairs with"],
  ["alternatives","Alternatives"],["standards","Standards"],["maturity","Maturity"],
  ["avoid_when","Avoid when"],["leverage_note","Leverage note"]];

function card(r,terms){
  var pills='<span class="pill st-'+r.status+'">'+esc(r.status_label||r.status)+'</span>';
  var metabits=[r.category];
  if(r.subgroup)metabits.push(r.subgroup);
  if((r.languages||[]).length)metabits.push(r.languages.join(" / "));
  if(r.form)metabits.push(r.form);
  var dl=FIELDS.map(function(f){
    var v=r[f[0]]; if(!v)return "";
    return "<dt>"+f[1]+"</dt><dd>"+hi(v,terms)+"</dd>";
  }).join("");
  var details=dl?('<details><summary>Details</summary><dl>'+dl+'</dl></details>'):"";
  return '<article class="card"><h2>'+hi(r.name,terms)+' '+pills+'</h2>'+
    '<div class="cardmeta">'+metabits.map(function(m){return "<span>"+esc(m)+"</span>"}).join("")+'</div>'+
    (r.description?'<p class="desc">'+hi(r.description,terms)+'</p>':"")+details+'</article>';
}

function render(){
  var terms=state.q?state.q.toLowerCase().split(/\s+/).filter(Boolean):[];
  var rows=DATA.filter(matches).sort(sortRecs);
  $("#grid").innerHTML=rows.map(function(r){return card(r,terms)}).join("");
  $("#empty").hidden=rows.length>0;
  $("#count").textContent=rows.length+" of "+DATA.length+" projects";
  store();
}

function syncControls(){
  $("#q").value=state.q; $("#fcat").value=state.cat; $("#fstatus").value=state.status;
  $("#flang").value=state.lang; $("#fform").value=state.form; $("#fsort").value=state.sort;
  document.querySelectorAll("#quick .chip").forEach(function(c){
    var on=(c.dataset.tech&&c.dataset.tech===state.tech)||
           (c.dataset.need&&c.dataset.need===state.need)||
           (c.dataset.form&&c.dataset.form===state.form)||
           (c.dataset.mat&&c.dataset.mat===state.mat);
    c.setAttribute("aria-pressed",on?"true":"false");
  });
}

function init(){
  restore();
  fillSelect($("#fcat"),uniq("category"),"All categories");
  fillSelect($("#fstatus"),uniq("status"),"Any status");
  fillSelect($("#flang"),uniq("languages"),"Any language");
  fillSelect($("#fform"),uniq("form").filter(Boolean),"Any form");
  syncControls();
  var t;
  $("#q").addEventListener("input",function(e){state.q=e.target.value;clearTimeout(t);t=setTimeout(render,120)});
  $("#fcat").addEventListener("change",function(e){state.cat=e.target.value;render()});
  $("#fstatus").addEventListener("change",function(e){state.status=e.target.value;render()});
  $("#flang").addEventListener("change",function(e){state.lang=e.target.value;render()});
  $("#fform").addEventListener("change",function(e){state.form=e.target.value;render()});
  $("#fsort").addEventListener("change",function(e){state.sort=e.target.value;render()});
  document.querySelectorAll("#quick .chip").forEach(function(c){
    c.addEventListener("click",function(){
      if(c.dataset.tech)state.tech=state.tech===c.dataset.tech?"":c.dataset.tech;
      if(c.dataset.need)state.need=state.need===c.dataset.need?"":c.dataset.need;
      if(c.dataset.form){state.form=state.form===c.dataset.form?"":c.dataset.form;$("#fform").value=state.form}
      if(c.dataset.mat)state.mat=state.mat===c.dataset.mat?"":c.dataset.mat;
      syncControls();render();
    });
  });
  $("#reset").addEventListener("click",function(){
    state={q:"",cat:"",status:"",lang:"",form:"",sort:"name",tech:"",need:"",mat:""};
    syncControls();render();
  });
  var themeBtn=$("#theme");
  themeBtn.addEventListener("click",function(){
    var cur=document.documentElement.getAttribute("data-theme");
    var next=cur==="dark"?"light":"dark";
    document.documentElement.setAttribute("data-theme",next);
    themeBtn.setAttribute("aria-pressed",next==="dark"?"true":"false");
    try{localStorage.setItem("asf-finder-theme",next)}catch(e){}
  });
  try{var th=localStorage.getItem("asf-finder-theme");if(th)document.documentElement.setAttribute("data-theme",th)}catch(e){}
  render();
}
init();
</script>
</body>
</html>
"""


def build_html(records, generated):
    data = json.dumps(records, ensure_ascii=False, separators=(",", ":"))
    html = (HTML_TEMPLATE
            .replace("__DATA__", data)
            .replace("__GENERATED__", generated)
            .replace("__COUNT__", str(len(records))))
    return html


def main():
    if not MD.exists():
        print("ERROR: inventory markdown not found at", MD, file=sys.stderr)
        return 1
    md = MD.read_text(encoding="utf-8")
    records = parse(md)
    amap = parse_avoid_when(md)
    for r in records:
        key = normalize_name(r["name"])
        if key in amap:
            r["avoid_when"] = amap[key]
            r["search"] += " " + amap[key].lower()
    records.sort(key=lambda r: (r["category_num"], r["name"].lower()))
    JSON_OUT.write_text(json.dumps(records, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    generated = datetime.date.today().isoformat()
    HTML_OUT.write_text(build_html(records, generated), encoding="utf-8")

    # summary
    from collections import Counter
    st = Counter(r["status"] for r in records)
    src = Counter(r["source"] for r in records)
    print("records:", len(records))
    print("by status:", dict(st))
    print("by source:", dict(src))
    missing = [r["name"] for r in records if r["source"] == "card" and not r["description"]]
    print("cards missing description:", len(missing), missing[:12])
    nofields = [r["name"] for r in records if r["source"] == "card"
                and not r["interfaces"] and not r["leverage_note"]]
    print("cards missing interfaces & leverage note:", len(nofields), nofields[:20])
    print("wrote", JSON_OUT.name, "and", HTML_OUT.name)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BrokenPipeError:
        sys.exit(0)
