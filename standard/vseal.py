#!/usr/bin/env python3
"""V-Seal reference implementation — Sovereign AI Standard.

One tool generates every dot-field artwork so the geometry is single-sourced:

  python3 standard/vseal.py logo                      -> site/brand/medallion.svg, medallion-mono.svg, glyph*.svg, favicon.svg
  python3 standard/vseal.py encode-coin MASTER REG    -> sealed coin credential (scheme vseal-1)
  python3 standard/vseal.py encode-cert MASTER FINDING.json [--template]  -> sealed certificate (vseal-cert-1)
  python3 standard/vseal.py verify FILE.svg (MASTER | --seed HEX)
  python3 standard/vseal.py selftest

The seal: every dot in the field is nudged by ±DELTA in x and y, the signs taken from
SHA-256(key ‖ u32le(i)). The key is K = HMAC-SHA256(master, "SAS|" + registry) for a coin, and
Kf = HMAC-SHA256(K, content_hash) for a certificate, where content_hash = SHA-256(canonical(finding)).
The file carries SHA-256(key) as a public commitment and SHA-256 of the written coordinates as the
"state image" of the artwork. Verification re-derives the key, rebuilds the field and compares.
Standard library only.
"""
import sys, json, math, hmac, hashlib, re, struct

DELTA = 0.09          # px nudge
EPS = 0.03            # exact-offset tolerance on read-back
DECIMALS = 3
FINDING_ORDER = ["subject","version","operator","jurisdiction","registry","assessed","standard","assessor","method","anchor","result","overall"]
DIMS = ["S1","S2","S3","S4","S5","S6","S7"]
SILVER = '<linearGradient id="silver" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="{w}" y2="{h}"><stop offset="0" stop-color="#EEF2F6"/><stop offset=".24" stop-color="#9AA3AE"/><stop offset=".46" stop-color="#F3F6F9"/><stop offset=".62" stop-color="#828C98"/><stop offset=".82" stop-color="#CBD2DA"/><stop offset="1" stop-color="#7E8894"/></linearGradient>'

# ---------------------------------------------------------------- crypto
def seed_K(master: str, registry: str) -> bytes:
    return hmac.new(master.encode(), b"SAS|" + registry.encode(), hashlib.sha256).digest()
def canonical(finding: dict) -> str:
    return "|".join(str(finding[k]) for k in FINDING_ORDER) + "|" + "|".join(f"{d}:{finding['levels'][d]}" for d in DIMS)
def content_hash(finding: dict) -> str:
    return hashlib.sha256(canonical(finding).encode()).hexdigest()
def seed_Kf(K: bytes, chash: str) -> bytes:
    return hmac.new(K, chash.encode(), hashlib.sha256).digest()
def commit(key: bytes) -> str:
    return hashlib.sha256(key).hexdigest()
def offset(key: bytes, i: int):
    b = hashlib.sha256(key + struct.pack("<I", i)).digest()[0]
    return (DELTA if b & 1 else -DELTA, DELTA if b & 2 else -DELTA)
def device_params(key: bytes):
    g = hashlib.sha256(key + b"VGLYPH").digest()
    return {"apex_dy": round((g[0] / 255 - .5) * 2.0, 3), "span_dx": round((g[1] / 255 - .5) * 4.0, 3)}
def state_image(points) -> str:
    return hashlib.sha256("\n".join(f"{x:.{DECIMALS}f},{y:.{DECIMALS}f}" for x, y in points).encode()).hexdigest()

# ---------------------------------------------------------------- geometry
def star_poly(cx, cy, r, ri):
    pts = []
    for i in range(8):
        a = math.pi / 2 * (i / 2) - math.pi / 2
        rr = r if i % 2 == 0 else ri
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    return pts
def seg_dist(p, a, b):
    (px, py), (ax, ay), (bx, by) = p, a, b
    dx, dy = bx - ax, by - ay
    t = 0 if dx == dy == 0 else max(0, min(1, ((px - ax) * dx + (py - ay) * dy) / (dx * dx + dy * dy)))
    return math.hypot(px - (ax + t * dx), py - (ay + t * dy))
def in_poly(p, poly):
    x, y = p; inside = False; n = len(poly)
    for i in range(n):
        (x1, y1), (x2, y2) = poly[i], poly[(i + 1) % n]
        if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1) + x1: inside = not inside
    return inside
def device_segments(apex_dy=0.0, span_dx=0.0):
    """The device in medallion space (200×200): compressor wedge, psi stem, base, apex star."""
    L, R = 72 - span_dx, 128 + span_dx
    segs = [((L, 86), (R, 86)), ((R, 86), (109, 132)), ((109, 132), (91, 132)), ((91, 132), (L, 86)),
            ((100, 66), (100, 144)), ((86, 144), (114, 144))]
    return segs, star_poly(100, 60 + apex_dy, 8, 2.9)
def on_device(p, segs, star, tol=3.4):
    return any(seg_dist(p, a, b) <= tol for a, b in segs) or in_poly(p, star) or math.hypot(p[0] - 100, p[1] - (star[0][1] + 8)) <= 6.5

def coin_grid(spacing=7, r_max=78, rim_r=92, rim_n=72):
    pts = []
    n = int(r_max // spacing)
    for j in range(-n, n + 1):
        for i in range(-n, n + 1):
            x, y = 100 + i * spacing, 100 + j * spacing
            if math.hypot(x - 100, y - 100) <= r_max: pts.append((x, y))
    for k in range(rim_n):
        a = 2 * math.pi * k / rim_n
        pts.append((100 + rim_r * math.cos(a), 100 + rim_r * math.sin(a)))
    return pts
def band_grid(x0=68, y0=672, nx=142, ny=6, spacing=7, ring=(1030, 690, 19, 36)):
    pts = [(x0 + i * spacing, y0 + j * spacing) for j in range(ny) for i in range(nx)]
    cx, cy, r, n = ring
    pts += [(cx + r * math.cos(2 * math.pi * k / n), cy + r * math.sin(2 * math.pi * k / n)) for k in range(n)]
    return pts
def to_medallion(p, vbase):
    return ((p[0] - vbase["cx"]) / vbase["scale"] + 100, (p[1] - vbase["cy"]) / vbase["scale"] + 100)

# ---------------------------------------------------------------- SVG writers
def dots_svg(points, device_idx, keyed, paint_dim, paint_hi, r_dot=1.15, r_dev=1.9, covert=False, cls=True):
    out = []
    for i, (x, y) in enumerate(points):
        dev = i in device_idx
        r = r_dot if (covert or not dev) else r_dev
        fill = paint_hi if (dev and not covert) else paint_dim
        c = ' class="d"' if cls else ''
        tag = ' data-dev="1"' if (dev and not covert) else ''
        out.append(f'<circle{c} cx="{x:.{DECIMALS}f}" cy="{y:.{DECIMALS}f}" r="{r}" fill="{fill}"{tag}/>')
    return "".join(out)

def logo_svg(mono=False):
    pts = coin_grid(); segs, star = device_segments()
    dev = {i for i, p in enumerate(pts) if on_device(p, segs, star)}
    if mono: dim, hi, defs, extra = "#9AA3AE", "#15171d", "", ' color="#15171d"'
    else:    dim, hi, defs, extra = "#6F7883", "url(#silver)", SILVER.format(w=200, h=200), ""
    body = dots_svg(pts, dev, False, dim, hi, cls=False)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="200" height="200" role="img" aria-label="Sovereign AI Standard medallion"{extra}>'
            f'<title>Sovereign AI Standard — the medallion</title><desc>A stigmergic dot field: the device, the Greek letter psi fused with the P&amp;ID compressor wedge, emerges from the grid. Three prongs for three levels; the apex star above.</desc>'
            f'<defs>{defs}</defs>{body}</svg>\n')

def glyph_svg(mono=False, tile=False):
    # the glyph is the device's reduction: a diamond of dots with a filled core
    pts = [(32 + dx, 32 + dy) for dx, dy in [(0,-24),(8,-16),(16,-8),(24,0),(16,8),(8,16),(0,24),(-8,16),(-16,8),(-24,0),(-16,-8),(-8,-16)]]
    core = [(32,32),(32,24),(40,32),(32,40),(24,32)]
    if mono: dim, hi, defs = "#15171d", "#15171d", ""
    else:    dim, hi, defs = "url(#silver)", "url(#silver)", SILVER.format(w=64, h=64)
    body = "".join(f'<circle cx="{x}" cy="{y}" r="2.6" fill="{dim}"/>' for x, y in pts) + "".join(f'<circle cx="{x}" cy="{y}" r="3.4" fill="{hi}"/>' for x, y in core)
    bg = '<rect width="64" height="64" rx="12" fill="#08090B"/>' if tile else ''
    colour = ' color="#15171d"' if mono else ''
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64" role="img" aria-label="Sovereign AI glyph"{colour}><defs>{defs}</defs>{bg}{body}</svg>\n'

def coin_svg(master, registry):
    K = seed_K(master, registry); key = K
    base = coin_grid(); dp = device_params(key); segs, star = device_segments(**dp)
    dev = sorted(i for i, p in enumerate(base) if on_device(p, segs, star))
    pts = [(x + offset(key, i)[0], y + offset(key, i)[1]) for i, (x, y) in enumerate(base)]
    meta = {"scheme": "vseal-1", "registry": registry, "commit": commit(key), "dots": len(pts), "delta": DELTA,
            "grid": {"type": "coin", "spacing": 7, "r_max": 78, "rim_r": 92, "rim_n": 72}, "vbase": {"cx": 100, "cy": 100, "scale": 1},
            "device": dp, "state_image": state_image(pts)}
    body = dots_svg(pts, set(dev), True, "#8E97A3", "#8E97A3", covert=True)
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="200" height="200" role="img" aria-label="Sovereign AI credential coin {registry}">'
           f'<title>Sovereign AI credential · {registry}</title><metadata id="vseal">{json.dumps(meta, separators=(",", ":"))}</metadata>'
           f'<rect width="200" height="200" fill="#08090B"/>{body}'
           f'<text x="100" y="193" text-anchor="middle" font-family="IBM Plex Mono,monospace" font-size="6" letter-spacing="1.5" fill="#6A727D">SOVEREIGN AI · {registry}</text></svg>\n')
    return svg, {"K": K.hex(), "commit": meta["commit"], "dots": len(pts), "device_dots": len(dev), "state_image": meta["state_image"]}

CERT_VBASE = {"cx": 300, "cy": 690, "scale": 0.42}
def cert_face(finding, sealed_meta=None, field_dots="", template=False):
    MONO = "'IBM Plex Mono',ui-monospace,Menlo,monospace"
    INK, INK2, INK3, EDGE, PAPER = "#15171d", "#4F5A66", "#7A8591", "#C6CDD6", "#F4F5F7"
    f = finding
    def fld(x, y, label, w, val):
        return (f'<text x="{x}" y="{y}" font-family="{MONO}" font-size="8.5" letter-spacing="1.6" fill="{INK3}">{label}</text>'
                f'<line x1="{x}" y1="{y+30}" x2="{x+w}" y2="{y+30}" stroke="{EDGE}"/><text x="{x}" y="{y+23}" font-family="{MONO}" font-size="13" fill="{INK}">{val}</text>')
    lvl_name = {1: "Disclosed", 2: "Controlled", 3: "Sovereign"}
    overall = f["overall"]
    levels = "".join(f'<g transform="translate({64 + k*62} 0)"><text x="0" y="588" font-family="{MONO}" font-size="8" letter-spacing="1.4" fill="{INK3}">{d}</text>'
                     f'<text class="lv" data-dim="{d}" x="0" y="606" font-family="{MONO}" font-size="15" font-weight="700" fill="{INK}">{f["levels"][d]}</text></g>' for k, d in enumerate(DIMS))
    meta = f'<metadata id="vseal">{json.dumps(sealed_meta, separators=(",", ":"))}</metadata>' if sealed_meta else ''
    med = f'<image href="medallion-mono.svg" x="820" y="140" width="260" height="260"/>'
    badge = f'<image href="badge-level-{overall}-light.svg" x="800" y="430" width="260" height="48.5"/>'
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1123 794" width="1123" height="794" role="img" aria-label="Sovereign AI certificate {f['registry']}">
  <title>Sovereign AI Standard — certificate {f['registry']}</title>{meta}
  <rect width="1123" height="794" fill="{PAPER}"/>
  <rect x="24" y="24" width="1075" height="746" fill="none" stroke="{INK}" stroke-width="1.5"/><rect x="30" y="30" width="1063" height="734" fill="none" stroke="{EDGE}" stroke-width=".8"/>
  <g transform="translate(64 60)"><path d="M11 2 L20 11 L11 20 L2 11 Z" fill="none" stroke="{INK}" stroke-width="1.6"/><path d="M11 7 L15 11 L11 15 L7 11 Z" fill="{INK}"/></g>
  <text x="96" y="76" font-family="{MONO}" font-size="13" font-weight="700" letter-spacing="2.6" fill="{INK}">SOVEREIGN AI STANDARD</text>
  <text x="96" y="92" font-family="{MONO}" font-size="8.5" letter-spacing="2" fill="{INK3}">CERTIFICATE OF CERTIFICATION · ISSUED UNDER SOVEREIGN AI STANDARD {f['standard'].upper()}</text>
  <text x="1059" y="76" text-anchor="end" font-family="{MONO}" font-size="8.5" letter-spacing="1.6" fill="{INK3}">CERTIFICATE NO.</text>
  <text x="1059" y="92" text-anchor="end" font-family="{MONO}" font-size="13" fill="{INK}">{f['registry']}</text>
  <line x1="64" y1="112" x2="1059" y2="112" stroke="{INK}" stroke-width="1"/>
  <text x="64" y="172" font-family="{MONO}" font-size="30" font-weight="600" fill="{INK}">This certifies that</text>
  <text x="64" y="214" font-family="{MONO}" font-size="22" fill="{INK}">{f['subject']}</text>
  <text x="64" y="240" font-family="{MONO}" font-size="13" fill="{INK2}">of {f['operator']} · {f['jurisdiction']}</text>
  <text x="64" y="290" font-family="{MONO}" font-size="14" fill="{INK}">has been assessed by an accredited independent assessor and holds</text>
  <text x="64" y="326" font-family="{MONO}" font-size="21" font-weight="700" fill="{INK}">Sovereign AI Certified · Level <tspan class="lv" data-dim="overall">{overall}</tspan></text>
  <text x="64" y="352" font-family="{MONO}" font-size="15" font-weight="600" fill="{INK}">{lvl_name[overall] if not template else "[ Disclosed / Controlled / Sovereign ]"} · <tspan class="lv" data-dim="result">{f['result']}</tspan></text>
  <text x="64" y="374" font-family="{MONO}" font-size="11.5" fill="{INK2}">against Sovereign AI Standard {f['standard']}, Track {f['method']}, across all seven dimensions of AI control.</text>
  {fld(64,400,"ISSUED",200,f['assessed'])}{fld(300,400,"VALID TO",200,f.get('valid_to','[ ]'))}{fld(536,400,"STANDARD VERSION",200,f['standard'])}
  {fld(64,470,"ACCREDITED ASSESSOR",436,f['assessor'])}{fld(536,470,"ANCHOR",200,f['anchor'])}
  <text x="64" y="526" font-family="{MONO}" font-size="8.5" letter-spacing="1.6" fill="{INK3}">VERIFY AT</text>
  <text x="64" y="546" font-family="{MONO}" font-size="13" fill="{INK}">register.sovereignai.com/{f['registry']}</text>
  <text x="64" y="574" font-family="{MONO}" font-size="8.5" letter-spacing="1.6" fill="{INK3}">LEVEL ACHIEVED PER DIMENSION · S1 MODEL · S2 DATA · S3 PROVENANCE · S4 OPERATIONAL · S5 INFRASTRUCTURE · S6 EXIT · S7 EVALUATION</text>
  {levels}
  <text x="64" y="636" font-family="{MONO}" font-size="9" fill="{INK3}">Certification is product-scoped and evidences the published criteria at the level stated; it does not certify accuracy, safety, fairness or fitness for purpose.</text>
  <text x="64" y="650" font-family="{MONO}" font-size="9" fill="{INK3}">The certificate is the Standard's record; its status is live on the public register. The field below is the V-Seal: it binds this face to its seed and to these results.</text>
  {med}{badge}
  <text x="930" y="500" text-anchor="middle" font-family="{MONO}" font-size="8" letter-spacing="1.4" fill="{INK3}">{"REPLACE WITH THE BADGE FOR THE LEVEL HELD" if template else "LEVEL " + str(overall) + " · " + lvl_name[overall].upper()}</text>
  <line x1="800" y1="590" x2="1059" y2="590" stroke="{EDGE}"/><text x="800" y="606" font-family="{MONO}" font-size="8" letter-spacing="1.4" fill="{INK3}">SIGNED FOR THE ACCREDITED ASSESSOR</text><text x="800" y="620" font-family="{MONO}" font-size="8" letter-spacing="1.4" fill="{INK3}">NAME · ROLE · DATE</text>
  <rect x="64" y="664" width="995" height="52" fill="none" stroke="{EDGE}"/>
  <g id="field">{field_dots}</g>
  <text x="64" y="732" font-family="{MONO}" font-size="7.5" letter-spacing="1.4" fill="{INK3}">V-SEAL FIELD · vseal-cert-1 · {"UNSEALED TEMPLATE — THE ISSUING ASSESSOR SEALS IT" if template else "SEALED · COMMIT " + sealed_meta["commit"][:16] + "… · STATE IMAGE " + sealed_meta["state_image"][:16] + "…"}</text>
  <text x="64" y="756" font-family="{MONO}" font-size="8" letter-spacing="1.2" fill="{INK3}">SOVEREIGNAI IS A CERTIFICATION MARK OF SOVEREIGN TECHNOLOGY SYSTEMS CORPORATION · USPTO SERIAL NO. 99861987 · REGISTRATION PENDING</text>
</svg>
'''

def cert_svg(master, finding, template=False):
    base = band_grid()
    if template:
        body = dots_svg(base, set(), False, "#B8C0CA", "#B8C0CA", r_dot=1.0, covert=True, cls=False)
        return cert_face(finding, None, body, template=True), {}
    K = seed_K(master, finding["registry"]); ch = content_hash(finding); Kf = seed_Kf(K, ch); key = Kf
    dp = device_params(key); segs, star = device_segments(**dp)
    dev = sorted(i for i, p in enumerate(base) if on_device(to_medallion(p, CERT_VBASE), segs, star, tol=3.4))
    pts = [(x + offset(key, i)[0], y + offset(key, i)[1]) for i, (x, y) in enumerate(base)]
    meta = {"scheme": "vseal-cert-1", "registry": finding["registry"], "content_hash": ch, "commit": commit(key), "dots": len(pts), "delta": DELTA,
            "grid": {"type": "band", "x0": 68, "y0": 672, "nx": 142, "ny": 6, "spacing": 7, "ring": [1030, 690, 19, 36]}, "vbase": CERT_VBASE,
            "device": dp, "state_image": state_image(pts), "finding": finding}
    body = dots_svg(pts, set(dev), True, "#7A8591", "#7A8591", r_dot=1.0, covert=True)
    return cert_face(finding, meta, body), {"K": K.hex(), "Kf": Kf.hex(), "commit": meta["commit"], "content_hash": ch, "dots": len(pts), "device_dots": len(dev), "state_image": meta["state_image"]}

# ---------------------------------------------------------------- verifier
def parse(svg_text):
    m = re.search(r'<metadata id="vseal">(.*?)</metadata>', svg_text, re.S)
    meta = json.loads(m.group(1)) if m else None
    pts = [(float(a), float(b)) for a, b in re.findall(r'<circle class="d" cx="([-\d.]+)" cy="([-\d.]+)"', svg_text)]
    printed = dict(re.findall(r'class="lv" data-dim="([A-Za-z0-9]+)"[^>]*>([^<]*)<', svg_text))
    return meta, pts, printed
def rebuild_base(meta):
    g = meta["grid"]
    if g["type"] == "coin": return coin_grid(g["spacing"], g["r_max"], g["rim_r"], g["rim_n"])
    return band_grid(g["x0"], g["y0"], g["nx"], g["ny"], g["spacing"], tuple(g["ring"]))
def verify(svg_text, master=None, seed_hex=None):
    meta, pts, printed = parse(svg_text)
    if not meta: return {"ok": False, "error": "no vseal metadata"}
    cert = meta["scheme"] == "vseal-cert-1"
    if seed_hex: key = bytes.fromhex(seed_hex)
    else:
        K = seed_K(master, meta["registry"])
        key = seed_Kf(K, content_hash(meta["finding"])) if cert else K
    base = rebuild_base(meta)
    ok_field = 0; desync = []
    for i, (bx, by) in enumerate(base):
        if i >= len(pts): desync.append(i); continue
        dx, dy = offset(key, i)
        if abs(pts[i][0] - (bx + dx)) <= EPS and abs(pts[i][1] - (by + dy)) <= EPS: ok_field += 1
        else: desync.append(i)
    r = {"scheme": meta["scheme"], "registry": meta["registry"], "field": f"{ok_field} / {len(base)}", "field_ok": ok_field == len(base) == len(pts),
         "commit_ok": commit(key) == meta["commit"], "state_image_ok": state_image(pts) == meta["state_image"], "desync": desync[:12]}
    if cert:
        f = meta["finding"]; exp = {d: str(f["levels"][d]) for d in DIMS}; exp["overall"] = str(f["overall"]); exp["result"] = str(f["result"])
        bad = [k for k, v in exp.items() if printed.get(k) != v]
        r["content_ok"] = content_hash(f) == meta["content_hash"] and not bad; r["printed_mismatch"] = bad
    dp = device_params(key); segs, star = device_segments(**dp)
    vb = meta["vbase"]
    r["device_dots"] = [i for i, p in enumerate(base) if on_device(to_medallion(p, vb), segs, star)]
    r["ok"] = r["field_ok"] and r["commit_ok"] and r["state_image_ok"] and r.get("content_ok", True)
    return r

DEMO_FINDING = {"subject": "Claims Copilot", "version": "4.2", "operator": "Northwind Analytics", "jurisdiction": "EU · Ireland", "registry": "SAS-2026-0007",
                "assessed": "2026-08-14", "valid_to": "2028-08-14", "standard": "v1.0", "assessor": "Tensor (founding accredited assessor)", "method": "A",
                "anchor": "register.sovereignai.com", "result": "PASS", "overall": 2, "levels": {"S1": 3, "S2": 2, "S3": 2, "S4": 3, "S5": 2, "S6": 2, "S7": 3}}

def selftest(master="SAS-master-demo"):
    rows = []
    svg, info = coin_svg(master, "SAS-2026-0007")
    rows.append(("coin · authentic", verify(svg, master)))
    rows.append(("coin · one dot moved", verify(svg.replace('class="d" cx="100.090"', 'class="d" cx="100.190"', 1), master)))
    rows.append(("coin · wrong seed", verify(svg, "not-the-master")))
    csvg, cinfo = cert_svg(master, DEMO_FINDING)
    rows.append(("cert · authentic", verify(csvg, master)))
    rows.append(("cert · printed score edited", verify(re.sub(r'(data-dim="S5"[^>]*>)2<', r'\g<1>3<', csvg, 1), master)))
    alt = csvg.replace('"S5":2', '"S5":3', 1)
    rows.append(("cert · sealed finding altered", verify(alt, master)))
    rows.append(("cert · wrong seed", verify(csvg, "not-the-master")))
    print(f"{'scenario':<30} {'field':>12}  commit  state  content  verdict")
    for name, r in rows:
        print(f"{name:<30} {r['field']:>12}  {'✓' if r['commit_ok'] else '✗':^6}  {'✓' if r['state_image_ok'] else '✗':^5}  {('✓' if r.get('content_ok') else '✗') if 'content_ok' in r else '–':^7}  {'PASS' if r['ok'] else 'FAIL'}")
    return all(r["ok"] for n, r in rows if "authentic" in n) and not any(r["ok"] for n, r in rows if "authentic" not in n)

def main(argv):
    if not argv or argv[0] in ("-h", "--help"): print(__doc__); return 0
    cmd = argv[0]
    if cmd == "logo":
        open("site/brand/medallion.svg", "w").write(logo_svg()); open("site/brand/medallion-mono.svg", "w").write(logo_svg(mono=True))
        open("site/brand/glyph.svg", "w").write(glyph_svg()); open("site/brand/glyph-mono.svg", "w").write(glyph_svg(mono=True)); open("site/brand/favicon.svg", "w").write(glyph_svg(tile=True))
        print("logo written"); return 0
    if cmd == "encode-coin":
        svg, info = coin_svg(argv[1], argv[2]); out = argv[3] if len(argv) > 3 else f"site/brand/coin-{argv[2]}.svg"
        open(out, "w").write(svg); print(json.dumps(info, indent=1)); print("->", out); return 0
    if cmd == "encode-cert":
        finding = DEMO_FINDING if argv[2] == "demo" else json.load(open(argv[2]))
        template = "--template" in argv
        svg, info = cert_svg(argv[1], finding, template=template)
        out = next((a for a in argv[3:] if not a.startswith("--")), "site/brand/certificate-template.svg" if template else f"site/brand/certificate-{finding['registry']}.svg")
        open(out, "w").write(svg); print(json.dumps(info, indent=1)); print("->", out); return 0
    if cmd == "verify":
        text = open(argv[1]).read()
        r = verify(text, seed_hex=argv[3]) if len(argv) > 3 and argv[2] == "--seed" else verify(text, master=argv[2])
        print(json.dumps({k: v for k, v in r.items() if k != "device_dots"}, indent=1)); return 0 if r["ok"] else 1
    if cmd == "selftest": return 0 if selftest() else 1
    print("unknown command"); return 2
if __name__ == "__main__": sys.exit(main(sys.argv[1:]))
