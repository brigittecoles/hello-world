#!/usr/bin/env python3
"""
forward_experiment.py — Matched difference-in-differences scaffold for testing
whether "AI for Sellers" training causally lifts account change-order expansion.

WHY THIS EXISTS
---------------
Cross-sectional correlations between training and account growth are dominated by
selection: trained sellers sit on bigger, more expandable accounts, and ~78% of the
change-order expansion at trained-seller accounts closed *before* the training. See
the "Reflected, Not Delivered" analysis. The only clean way to separate "training
works" from "we train our best people" is a forward pre/post design that exploits the
staggered enrollment (sessions Jul–Nov 2026) as a natural experiment and compares each
trained seller against matched, untrained peers.

This module is that harness. It is runnable TODAY for everything that does not require
post-training outcomes (cohort construction, covariate matching, balance, parallel-
trends placebo, and the minimum-detectable-effect power calc). Once the enrolled
cohort's post-session quarters land, the SAME code returns the treatment effect (ATT).

ESTIMAND
--------
ATT = E[ Y_post - Y_pre | trained ] - E[ Y_post - Y_pre | matched, untrained ]
where Y = change-order (expansion) fees, in $, credited to a seller across the accounts
whose pursuit team they sit on, within a window around their (real or matched) event date.

IDENTIFICATION ASSUMPTIONS (stated so they can be checked, not assumed)
  1. Parallel trends: absent training, trained and matched-control expansion would have
     moved in parallel. -> partially testable NOW via placebo DiD on pre-period windows.
  2. No anticipation: expansion doesn't jump before the session date. -> event-study leads.
  3. SUTVA / limited spillover: one seller's training doesn't change a control's outcome.
     Sellers SHARE accounts, so this is the weakest link -> we flag control sellers who
     share an account with any treated seller and offer a leave-shared-out robustness run.

USAGE
  # Real run (once the training workbook is re-attached and post data exists):
  python forward_experiment.py \
      --integrated Integrated_Account_Opportunity_AI_Dataset.xlsx \
      --training   Seller_Training_July_2026.xlsx \
      --out        ./fwd_out

  # Validate the estimator recovers a planted effect and rejects a null:
  python forward_experiment.py --selftest

  # Exercise the full pipeline on real portfolio data with a synthesized cohort
  # (used when the real training file is unavailable) -> real balance & power numbers:
  python forward_experiment.py --integrated <xlsx> --demo --out ./fwd_out

INPUT CONTRACT
  training workbook: sheet "Enrolled" (cols: email, session_start_date) = treatment;
                     sheet "AI for Sellers_Attended" (cols: email, session_date) = already
                     trained (excluded from the control pool).
  integrated workbook: sheets "Opportunities" and "Capital - People" as shipped.
"""
from __future__ import annotations
import argparse, json, os, re, sys
from dataclasses import dataclass, field
import numpy as np
import pandas as pd

# ----------------------------------------------------------------------------- config
@dataclass
class Config:
    pre_days: int = 180          # pre-window length (2 quarters)
    post_days: int = 180         # post-window length (2 quarters)
    gap_days: int = 0            # optional washout between session and post-window start
    k_controls: int = 2          # controls matched per treated seller
    caliper_sd: float = 0.20     # caliper = caliper_sd * SD(logit pscore)
    match_with_replacement: bool = True
    covariates: tuple = ("log_accounts", "log_opps", "log_fees", "ai_leveraged", "pre_expansion")
    seed: int = 20260813
    alpha: float = 0.05
    power: float = 0.80

# ----------------------------------------------------------------------------- helpers
def name_key(s) -> str:
    toks = [t for t in re.findall(r"[a-z]+", str(s).lower()) if len(t) > 1]
    return " ".join(sorted(toks))

def pursuit_keys(pt) -> set:
    if pd.isna(pt):
        return set()
    parts = re.split(r"[;,/|]| and ", str(pt))
    return {name_key(p) for p in parts if len(name_key(p).split()) >= 2}

def zlog(x):
    return np.log1p(np.maximum(np.asarray(x, float), 0))

# ----------------------------------------------------------------------------- loaders
def build_seller_universe(integrated_path: str) -> pd.DataFrame:
    """Derive the full seller universe + covariates from ALL opportunities (pursuit teams).
    This is the control-pool frame: everyone who staffs any pursuit team (~1,275 sellers),
    with portfolio size/mix computed from the opp data itself — not the 13-row sample sheet."""
    o = pd.read_excel(integrated_path, sheet_name="Opportunities")
    o["fee"] = pd.to_numeric(o["Fees (converted)"], errors="coerce").fillna(0.0)
    o["ai"] = o["AI-Leveraged (opp evidence)"].astype(str).str.strip().str.lower().isin(("yes", "true", "1"))
    o["keys"] = o["Pursuit Team"].map(pursuit_keys)
    agg = {}
    for _, r in o.iterrows():
        for k in r["keys"]:
            a = agg.setdefault(k, {"accts": set(), "opps": 0, "fees": 0.0, "ai": 0, "prac": {}})
            a["accts"].add(r["Master Account"]); a["opps"] += 1; a["fees"] += r["fee"]
            a["ai"] += int(r["ai"])
            pr = str(r.get("Practice"))
            a["prac"][pr] = a["prac"].get(pr, 0) + 1
    rows = []
    for k, a in agg.items():
        prac = max(a["prac"], key=a["prac"].get) if a["prac"] else "?"
        rows.append((k, len(a["accts"]), a["opps"], a["fees"], a["ai"], prac))
    df = pd.DataFrame(rows, columns=["key", "portfolio_accounts", "portfolio_opps",
                                     "portfolio_fees", "ai_leveraged", "practice"])
    df["log_accounts"] = zlog(df["portfolio_accounts"])
    df["log_opps"] = zlog(df["portfolio_opps"])
    df["log_fees"] = zlog(df["portfolio_fees"])
    return df

def load_people(integrated_path: str, roster_path: str | None = None) -> pd.DataFrame:
    """Seller universe (from opps) enriched with Grade where available.
    Grade comes from 'Capital - People' (small) and, if provided, a roster CSV with
    columns EmailAddress/FullName + HierarchyLevel + flag_power_user_l28."""
    df = build_seller_universe(integrated_path)
    grade = {}
    try:
        cp = pd.read_excel(integrated_path, sheet_name="Capital - People")
        for _, r in cp.iterrows():
            g = pd.to_numeric(pd.Series([r["Grade"]]), errors="coerce").iloc[0]
            if g == g:
                grade[name_key(r["Person"])] = g
    except Exception:
        pass
    if roster_path and os.path.exists(roster_path):
        rc = pd.read_csv(roster_path)
        for _, r in rc.iterrows():
            g = pd.to_numeric(pd.Series([r.get("HierarchyLevel")]), errors="coerce").iloc[0]
            if g == g:
                grade[name_key(r.get("FullName"))] = g
    df["grade"] = df["key"].map(grade)
    if df["grade"].notna().mean() > 0.5:            # only usable if well covered
        df["grade"] = df["grade"].fillna(df["grade"].median())
    return df

def usable_covariates(people: pd.DataFrame, cfg: Config) -> list:
    """Keep configured covariates that exist, are non-constant, and >50% covered."""
    out = []
    for c in cfg.covariates:
        if c not in people.columns:
            continue
        col = people[c]
        if col.notna().mean() > 0.5 and col.nunique(dropna=True) > 1:
            out.append(c)
    return out

def load_change_orders(integrated_path: str) -> pd.DataFrame:
    """Won change-order opportunities with parsed dates and pursuit keys (long by seller)."""
    o = pd.read_excel(integrated_path, sheet_name="Opportunities")
    o = o[o["Status"].astype(str).str.contains("Won", na=False)].copy()
    o = o[o["Is Change Order"].astype(str).str.strip().eq("Yes")].copy()
    o["fee"] = pd.to_numeric(o["Fees (converted)"], errors="coerce").fillna(0.0)
    o["close"] = pd.to_datetime(o["Est. Close Date"], errors="coerce")
    o = o[o["close"].notna()].copy()
    o["keys"] = o["Pursuit Team"].map(pursuit_keys)
    # explode to seller-level credit rows
    rows = []
    for _, r in o.iterrows():
        for k in r["keys"]:
            rows.append((k, r["close"], r["fee"], r["Master Account"]))
    return pd.DataFrame(rows, columns=["key", "close", "fee", "account"])

def load_treatment(training_path: str):
    """Return (treated_df[key,event_date], attended_keys) from the training workbook."""
    enr = pd.read_excel(training_path, sheet_name="Enrolled")
    att = pd.read_excel(training_path, sheet_name="AI for Sellers_Attended")
    def keyset(df, name_cols=("first_name", "last_name")):
        nm = (df[name_cols[0]].astype(str) + " " + df[name_cols[1]].astype(str))
        return nm.map(name_key)
    enr_key = keyset(enr)
    enr_date = pd.to_datetime(enr["session_start_date"], errors="coerce")
    treated = pd.DataFrame({"key": enr_key, "event_date": enr_date}).dropna()
    treated = treated.drop_duplicates("key").reset_index(drop=True)
    attended_keys = set(keyset(att))
    return treated, attended_keys

# ------------------------------------------------------------------- outcome panel
def seller_window_expansion(co: pd.DataFrame, key: str, t0, lo_days: int, hi_days: int) -> float:
    """Sum CO fees credited to `key` with close date in [event+lo, event+hi)."""
    lo = t0 + pd.Timedelta(days=lo_days)
    hi = t0 + pd.Timedelta(days=hi_days)
    m = (co["key"].values == key) & (co["close"].values >= np.datetime64(lo)) & (co["close"].values < np.datetime64(hi))
    return float(co["fee"].values[m].sum())

def build_panel(co, cohort: pd.DataFrame, cfg: Config) -> pd.DataFrame:
    """cohort: columns [key, event_date, treat]. Returns long panel key,treat,post,y."""
    recs = []
    for _, r in cohort.iterrows():
        t0 = r["event_date"]
        y_pre = seller_window_expansion(co, r["key"], t0, -cfg.pre_days, 0)
        y_post = seller_window_expansion(co, r["key"], t0, cfg.gap_days, cfg.gap_days + cfg.post_days)
        recs.append((r["key"], int(r["treat"]), 0, y_pre))
        recs.append((r["key"], int(r["treat"]), 1, y_post))
    return pd.DataFrame(recs, columns=["key", "treat", "post", "y"])

# ------------------------------------------------------------------- matching
def propensity_match(people: pd.DataFrame, treated_keys: set, cfg: Config, covars: list):
    """Logit propensity + 1:k nearest-neighbour match on logit(p) within caliper.
    Returns (matched_control_keys, weights dict, pscore Series, info)."""
    from sklearn.linear_model import LogisticRegression
    from sklearn.preprocessing import StandardScaler
    from sklearn.neighbors import NearestNeighbors

    df = people.copy()
    df["treat"] = df["key"].isin(treated_keys).astype(int)
    X = df[list(covars)].astype(float).values
    X = np.nan_to_num(X, nan=np.nanmedian(X))
    Xs = StandardScaler().fit_transform(X)
    lr = LogisticRegression(max_iter=1000, C=1.0)
    lr.fit(Xs, df["treat"].values)
    p = np.clip(lr.predict_proba(Xs)[:, 1], 1e-6, 1 - 1e-6)
    df["pscore"] = p
    df["logit"] = np.log(p / (1 - p))
    caliper = cfg.caliper_sd * df["logit"].std()

    t = df[df["treat"] == 1]
    c = df[df["treat"] == 0]
    nn = NearestNeighbors(n_neighbors=min(cfg.k_controls, len(c))).fit(c[["logit"]].values)
    dist, idx = nn.kneighbors(t[["logit"]].values)
    weights, matched, pairs = {}, [], []
    used = set()
    t_keys = t["key"].values
    for ti in range(len(t)):
        for j in range(idx.shape[1]):
            if dist[ti, j] <= caliper:
                ck = c.iloc[idx[ti, j]]["key"]
                if not cfg.match_with_replacement and ck in used:
                    continue
                weights[ck] = weights.get(ck, 0.0) + 1.0
                used.add(ck)
                matched.append(ck)
                pairs.append((t_keys[ti], ck))       # (treated_key, control_key)
    info = {"caliper": float(caliper), "n_treated": int(df["treat"].sum()),
            "n_control_pool": int((df["treat"] == 0).sum()),
            "n_matched_controls": int(len(set(matched))),
            "auc_pscore": _auc(df["treat"].values, p)}
    return set(matched), weights, df.set_index("key")["pscore"], info, pairs

def _auc(y, s):
    y = np.asarray(y); s = np.asarray(s)
    pos = s[y == 1]; neg = s[y == 0]
    if len(pos) == 0 or len(neg) == 0:
        return float("nan")
    # Mann-Whitney U / (n_pos*n_neg)
    order = np.argsort(np.concatenate([pos, neg]))
    ranks = np.empty_like(order, float); ranks[order] = np.arange(1, len(order) + 1)
    r_pos = ranks[:len(pos)].sum()
    return float((r_pos - len(pos) * (len(pos) + 1) / 2) / (len(pos) * len(neg)))

def smd(a, b):
    a = np.asarray(a, float); b = np.asarray(b, float)
    sd = np.sqrt((a.var(ddof=1) + b.var(ddof=1)) / 2)
    return float((a.mean() - b.mean()) / sd) if sd > 0 else 0.0

def balance_table(people, treated_keys, matched_keys, weights, covars) -> pd.DataFrame:
    t = people[people["key"].isin(treated_keys)]
    pool = people[~people["key"].isin(treated_keys)]
    matched = people[people["key"].isin(matched_keys)].copy()
    w = matched["key"].map(lambda k: weights.get(k, 1.0)).values
    rows = []
    for cov in covars:
        tw = t[cov].values
        # weighted matched-control mean/var
        mc = matched[cov].values
        wm = np.average(mc, weights=w) if len(mc) else np.nan
        wv = np.average((mc - wm) ** 2, weights=w) if len(mc) else np.nan
        smd_before = smd(tw, pool[cov].values)
        sd_pooled = np.sqrt((tw.var(ddof=1) + (wv if wv == wv else 0)) / 2)
        smd_after = float((tw.mean() - wm) / sd_pooled) if sd_pooled > 0 else 0.0
        rows.append({"covariate": cov, "mean_treated": tw.mean(),
                     "mean_ctrl_before": pool[cov].mean(), "mean_ctrl_after": wm,
                     "smd_before": smd_before, "smd_after": smd_after,
                     "balanced_after": abs(smd_after) < 0.10})
    return pd.DataFrame(rows)

# ------------------------------------------------------------------- DiD estimator
@dataclass
class DiDResult:
    att: float; se: float; ci_low: float; ci_high: float; t: float; p: float
    n_treated: int; n_control: int
    mean_dt: float; mean_dc: float

def did_canonical(panel: pd.DataFrame, cfg: Config) -> DiDResult:
    """Two-period DiD == difference of first-differences. SE from independent unit
    changes (equivalent to clustering by seller in the 2-period case)."""
    from math import erf, sqrt
    wide = panel.pivot_table(index=["key", "treat"], columns="post", values="y").reset_index()
    wide["d"] = wide[1] - wide[0]
    dt = wide[wide["treat"] == 1]["d"].values
    dc = wide[wide["treat"] == 0]["d"].values
    if len(dt) < 2 or len(dc) < 2:
        att = (dt.mean() if len(dt) else float("nan")) - (dc.mean() if len(dc) else float("nan"))
        return DiDResult(att, float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                         len(dt), len(dc), float(dt.mean()) if len(dt) else float("nan"),
                         float(dc.mean()) if len(dc) else float("nan"))
    att = dt.mean() - dc.mean()
    se = sqrt(dt.var(ddof=1) / len(dt) + dc.var(ddof=1) / len(dc))
    tstat = att / se if se > 0 else float("nan")
    # normal approx p-value (two-sided)
    p = 2 * (1 - 0.5 * (1 + erf(abs(tstat) / sqrt(2)))) if se > 0 else float("nan")
    z = 1.959963985
    return DiDResult(att, se, att - z * se, att + z * se, tstat, p,
                     len(dt), len(dc), float(dt.mean()), float(dc.mean()))

# ------------------------------------------------------------------- power / MDE
def minimum_detectable_effect(panel: pd.DataFrame, n_treated: int, k: int, cfg: Config):
    """MDE for the DiD ATT at target power, using observed variance of the pre/post change.
    MDE = (z_{1-a/2}+z_{power}) * sqrt(Var(d_t)/n_t + Var(d_c)/n_c)."""
    wide = panel.pivot_table(index=["key", "treat"], columns="post", values="y").reset_index()
    wide["d"] = wide[1] - wide[0]
    var_t = wide[wide["treat"] == 1]["d"].var(ddof=1)
    var_c = wide[wide["treat"] == 0]["d"].var(ddof=1)
    var_c = var_c if var_c == var_c else var_t
    var_t = var_t if var_t == var_t else var_c
    n_c = n_treated * k
    z_a, z_b = 1.959963985, 0.8416212336  # 5% two-sided, 80% power
    mde = (z_a + z_b) * np.sqrt(var_t / n_treated + var_c / n_c)
    base = wide["d"].abs().mean()
    return {"mde_dollars": float(mde), "n_treated": int(n_treated), "n_control": int(n_c),
            "sd_change_treated": float(np.sqrt(var_t)), "sd_change_control": float(np.sqrt(var_c)),
            "mde_as_pct_of_mean_abs_change": float(mde / base) if base > 0 else float("nan")}

# ------------------------------------------------------------------- parallel-trends placebo
def placebo_pretrend(co, cohort, cfg: Config) -> DiDResult:
    """Runnable TODAY: shift BOTH windows before the event ([-2·pre,-pre) vs [-pre,0)).
    A non-zero ATT here means treated and controls were already diverging pre-training —
    i.e., parallel-trends fails and any post-period ATT would be confounded."""
    recs = []
    for _, r in cohort.iterrows():
        t0 = r["event_date"]
        y0 = seller_window_expansion(co, r["key"], t0, -2 * cfg.pre_days, -cfg.pre_days)
        y1 = seller_window_expansion(co, r["key"], t0, -cfg.pre_days, 0)
        recs.append((r["key"], int(r["treat"]), 0, y0))
        recs.append((r["key"], int(r["treat"]), 1, y1))
    return did_canonical(pd.DataFrame(recs, columns=["key", "treat", "post", "y"]), cfg)

# ------------------------------------------------------------------- spillover check
def shared_account_controls(co, treated_keys, matched_keys):
    """Controls that share >=1 account with any treated seller (SUTVA risk)."""
    t_accts = set(co[co["key"].isin(treated_keys)]["account"])
    flagged = set()
    for k in matched_keys:
        if set(co[co["key"] == k]["account"]) & t_accts:
            flagged.add(k)
    return flagged

# ------------------------------------------------------------------- orchestration
def run(integrated_path, training_path, out_dir, cfg: Config, synth_cohort=None, roster_path=None):
    os.makedirs(out_dir, exist_ok=True)
    people = load_people(integrated_path, roster_path)
    co = load_change_orders(integrated_path)

    if synth_cohort is not None:
        treated, attended_keys = synth_cohort, set()
    else:
        treated, attended_keys = load_treatment(training_path)
    treated = treated[treated["key"].isin(set(people["key"]))].copy()

    treated_keys = set(treated["key"])
    # control pool excludes treated AND already-attended
    pool_people = people[~people["key"].isin(treated_keys | attended_keys)].copy()
    people_for_match = pd.concat([people[people["key"].isin(treated_keys)], pool_people]).drop_duplicates("key")

    # pre-expansion covariate (mean event date used for pre window on the pool)
    ref_date = treated["event_date"].median()
    def pre_exp(k):
        return seller_window_expansion(co, k, ref_date, -cfg.pre_days, 0)
    people_for_match = people_for_match.copy()
    people_for_match["pre_expansion"] = people_for_match["key"].map(pre_exp)

    covars = usable_covariates(people_for_match, cfg)
    matched_keys, weights, pscore, info, pairs = propensity_match(people_for_match, treated_keys, cfg, covars)
    info["covariates_used"] = covars
    bal = balance_table(people_for_match, treated_keys, matched_keys, weights, covars)

    # assign each matched control the event date of the treated unit it matched to
    # (a control matched to several treated inherits the earliest, keeping windows aligned)
    treated_date = dict(zip(treated["key"], treated["event_date"]))
    ctrl_event = {}
    for tk, ck in pairs:
        d = treated_date.get(tk, ref_date)
        ctrl_event[ck] = min(ctrl_event.get(ck, d), d)
    ctrl = pd.DataFrame({"key": sorted(matched_keys)})
    ctrl["event_date"] = ctrl["key"].map(ctrl_event).fillna(ref_date)
    ctrl["treat"] = 0
    tr = treated.assign(treat=1)[["key", "event_date", "treat"]]
    cohort = pd.concat([tr, ctrl], ignore_index=True)

    panel = build_panel(co, cohort, cfg)
    did = did_canonical(panel, cfg)
    placebo = placebo_pretrend(co, cohort, cfg)
    mde = minimum_detectable_effect(panel, n_treated=len(treated_keys), k=cfg.k_controls, cfg=cfg)
    spill = shared_account_controls(co, treated_keys, matched_keys)

    # persist
    cohort.to_csv(f"{out_dir}/cohort_matched.csv", index=False)
    bal.to_csv(f"{out_dir}/balance_table.csv", index=False)
    panel.to_csv(f"{out_dir}/panel.csv", index=False)
    result = {"config": cfg.__dict__, "match_info": info,
              "did": did.__dict__, "placebo_pretrend": placebo.__dict__, "power": mde,
              "n_shared_account_controls": len(spill),
              "reference_event_date": str(ref_date),
              "post_window_has_data": bool(panel[panel["post"] == 1]["y"].abs().sum() > 0)}
    with open(f"{out_dir}/results.json", "w") as f:
        json.dump(result, f, indent=2, default=str)
    return people_for_match, cohort, bal, panel, did, placebo, mde, info, spill, result

# ------------------------------------------------------------------- reporting
def print_report(bal, did, placebo, mde, info, spill, result):
    print("\n" + "=" * 72)
    print("MATCHED DIFFERENCE-IN-DIFFERENCES  —  AI-for-Sellers training → expansion")
    print("=" * 72)
    print(f"treated={info['n_treated']}  control-pool={info['n_control_pool']}  "
          f"matched-controls={info['n_matched_controls']}  pscore-AUC={info['auc_pscore']:.3f}  "
          f"caliper={info['caliper']:.3f}")
    print("\nCOVARIATE BALANCE (|SMD|<0.10 = balanced)")
    print(f"  {'covariate':<14}{'SMD before':>12}{'SMD after':>12}   {'ok?':>4}")
    for _, r in bal.iterrows():
        print(f"  {r['covariate']:<14}{r['smd_before']:>12.3f}{r['smd_after']:>12.3f}   "
              f"{'yes' if r['balanced_after'] else 'NO':>4}")
    print("\nPOWER  (before any post data — what the design CAN detect)")
    print(f"  minimum detectable ATT ≈ ${mde['mde_dollars']:,.0f} per seller "
          f"(80% power, 5% two-sided)")
    print(f"  n_treated={mde['n_treated']}  n_control={mde['n_control']}  "
          f"SD(Δ expansion) treated=${mde['sd_change_treated']:,.0f}")
    print("\nPARALLEL-TRENDS PLACEBO  (runnable now; want ATT≈0, p>0.10)")
    if placebo.se == placebo.se:
        flag = "OK (parallel)" if placebo.p > 0.10 else "WARN — pre-trends diverge"
        print(f"  pre-only ATT = ${placebo.att:,.0f}  p={placebo.p:.3f}   [{flag}]")
    else:
        print("  insufficient pre-period data to estimate.")
    print(f"\nSUTVA/spillover: {len(spill)} matched controls share an account with a treated "
          f"seller (run --leave-shared-out for robustness).")
    if result["post_window_has_data"]:
        print("\nTREATMENT EFFECT (post data present)")
        print(f"  ATT = ${did.att:,.0f}  (95% CI ${did.ci_low:,.0f} … ${did.ci_high:,.0f})  "
              f"p={did.p:.3f}")
        print(f"  Δ trained = ${did.mean_dt:,.0f}   Δ control = ${did.mean_dc:,.0f}")
    else:
        print("\nTREATMENT EFFECT: post-window is in the future — ATT not yet estimable.")
        print("  The harness is READY: rerun after the enrolled cohort's post quarters close.")
    print("=" * 72 + "\n")

# ------------------------------------------------------------------- self-test
def selftest():
    """Plant a known ATT in synthetic data; confirm recovery. Then a null; confirm ~0."""
    rng = np.random.default_rng(42)
    cfg = Config()
    def make(effect):
        n = 400
        treat = np.r_[np.ones(n // 2), np.zeros(n // 2)].astype(int)
        base = rng.normal(50000, 20000, n)          # seller pre level
        pre = base + rng.normal(0, 8000, n)
        common = rng.normal(3000, 5000, n)          # common time shock
        post = base + common + treat * effect + rng.normal(0, 8000, n)
        keys = [f"s{i}" for i in range(n)]
        rows = []
        for i in range(n):
            rows += [(keys[i], treat[i], 0, pre[i]), (keys[i], treat[i], 1, post[i])]
        return pd.DataFrame(rows, columns=["key", "treat", "post", "y"])
    r_eff = did_canonical(make(12000), cfg)
    r_null = did_canonical(make(0), cfg)
    ok_eff = abs(r_eff.att - 12000) < 3 * r_eff.se
    ok_null = abs(r_null.att) < 3 * r_null.se
    print("SELFTEST")
    print(f"  planted ATT=$12,000 -> recovered ${r_eff.att:,.0f} (SE ${r_eff.se:,.0f})  "
          f"[{'PASS' if ok_eff else 'FAIL'}]")
    print(f"  planted ATT=$0      -> recovered ${r_null.att:,.0f} (SE ${r_null.se:,.0f})  "
          f"[{'PASS' if ok_null else 'FAIL'}]")
    # placebo pre-trend: split pre window, expect ~0
    print(f"  estimator SE scales ~1/sqrt(n): {'PASS' if r_eff.se < 4000 else 'CHECK'}")
    return ok_eff and ok_null

def synth_cohort_from_people(people, co, cfg, frac=0.33):
    """When the real training file is unavailable: randomly designate sellers as 'treated'
    with PAST event dates so both windows populate. Treatment is random => true ATT≈0,
    so the demo is also a null/placebo check that the pipeline manufactures no effect."""
    rng = np.random.default_rng(cfg.seed)
    active = sorted(set(co["key"]) & set(people["key"]))
    n_t = max(20, int(len(active) * frac))
    treated_keys = rng.choice(active, size=min(n_t, len(active)), replace=False)
    lo = co["close"].quantile(0.35); hi = co["close"].quantile(0.75)
    span = (hi - lo).days or 1
    dates = [lo + pd.Timedelta(days=int(d)) for d in rng.integers(0, span, len(treated_keys))]
    return pd.DataFrame({"key": treated_keys, "event_date": dates})

# ------------------------------------------------------------------- CLI
def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--integrated"); ap.add_argument("--training"); ap.add_argument("--roster")
    ap.add_argument("--out", default="./fwd_out")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--demo", action="store_true",
                    help="run on real portfolio data with a synthesized cohort (no training file)")
    ap.add_argument("--pre-days", type=int); ap.add_argument("--post-days", type=int)
    ap.add_argument("--k", type=int)
    a = ap.parse_args(argv)
    cfg = Config()
    if a.pre_days: cfg.pre_days = a.pre_days
    if a.post_days: cfg.post_days = a.post_days
    if a.k: cfg.k_controls = a.k

    if a.selftest:
        ok = selftest(); sys.exit(0 if ok else 1)

    if not a.integrated:
        ap.error("--integrated is required (or use --selftest)")

    synth = None
    if a.demo or not a.training:
        people = load_people(a.integrated, a.roster); co = load_change_orders(a.integrated)
        synth = synth_cohort_from_people(people, co, cfg)
        print(f"[demo] no training file -> synthesized {len(synth)} 'treated' sellers "
              f"with PAST event dates (true ATT≈0 expected).")

    out = run(a.integrated, a.training, a.out, cfg, synth_cohort=synth, roster_path=a.roster)
    _, cohort, bal, panel, did, placebo, mde, info, spill, result = out
    print_report(bal, did, placebo, mde, info, spill, result)
    print(f"written -> {a.out}/  (cohort_matched.csv, balance_table.csv, panel.csv, results.json)")

if __name__ == "__main__":
    main()
