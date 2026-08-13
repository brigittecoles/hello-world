# Forward pre/post scaffold — does AI-for-Sellers training cause account expansion?

`forward_experiment.py` is a **matched difference-in-differences (DiD)** harness that tests
whether the *AI for Sellers* training causally lifts **change-order expansion**, rather than
just marking sellers who already sit on big, expandable accounts.

## Why
Cross-sectional correlation is dominated by selection: on the raw number, trained sellers
lead — but control for account size and the effect collapses to ≈0, and **78% of the
change-order expansion at trained-seller accounts closed *before* the training** (see the
"Reflected, Not Delivered" analysis). The only clean separation of *"training works"* from
*"we train our best people"* is a forward design that exploits the **staggered enrollment
(sessions Jul–Nov 2026)** as a natural experiment and compares each trained seller against
**matched, untrained peers**.

## Estimand
```
ATT = E[ ΔY | trained ] − E[ ΔY | matched, untrained ],   ΔY = Y_post − Y_pre
```
`Y` = change-order (expansion) fees in $, credited to a seller across the accounts whose
pursuit team they sit on, in a window around their (real or matched) session date.

## Identification assumptions (checked, not assumed)
1. **Parallel trends** — absent training, trained & controls move together. *Partly testable
   now* via the pre-only placebo DiD (`placebo_pretrend`).
2. **No anticipation** — expansion doesn't jump before the session date.
3. **SUTVA / limited spillover** — one seller's training doesn't move a control's outcome.
   Sellers share accounts, so this is the weak link; the harness **flags controls that share
   an account** with any treated seller for a leave-shared-out robustness run.

## Pipeline
`build_seller_universe` (≈1,275 pursuit-team sellers, covariates from the opp data) →
`propensity_match` (logit p-score, 1:k nearest-neighbour on logit(p) within a caliper) →
`balance_table` (standardized mean differences before/after) →
`build_panel` (pre/post expansion per seller; controls inherit their matched treated unit's
event date) → `did_canonical` (two-period DiD = difference of first-differences, SE from
independent unit changes = clustering by seller) → `placebo_pretrend` + `minimum_detectable_effect`.

No `statsmodels` dependency — the 2-period DiD and its SE are computed in closed form.

## Run
```bash
# Real run — once the training workbook is re-attached and post quarters have closed:
python forward_experiment.py \
    --integrated Integrated_Account_Opportunity_AI_Dataset.xlsx \
    --training   Seller_Training_July_2026.xlsx \
    --roster     roster_with_hierarchy.csv \   # optional: adds Grade/seniority covariate
    --out        ./fwd_out

# Validate the estimator (recovers a planted $12k effect, rejects a null):
python forward_experiment.py --selftest

# Exercise the whole pipeline on real portfolio data with a synthesized cohort
# (used while the real training file is unavailable) → real balance & power numbers:
python forward_experiment.py --integrated <xlsx> --demo --out ./fwd_out
```
Key knobs: `--pre-days` / `--post-days` (default 180 each), `--k` controls per treated (2).

## Outputs (`fwd_out/`)
| file | contents |
|---|---|
| `cohort_matched.csv` | treated + matched controls, event dates, weights |
| `balance_table.csv` | SMD before/after matching per covariate |
| `panel.csv` | long pre/post expansion panel |
| `results.json` | config, match diagnostics, DiD, placebo, power/MDE, spillover count |

## Status
- **Self-test:** passes — recovers a planted ATT and a null.
- **Demo (random cohort, real data):** full pipeline runs; placebo/ATT land non-significant
  (no manufactured effect); MDE ≈ **$260k per seller** at 182 treated / 364 controls.
- **Treatment effect:** not yet estimable — the enrolled cohort's post-windows are in the
  future. Re-run after those quarters close. The harness is ready.

## What to collect when the post period lands
1. Re-attach `Seller_Training_July_2026.xlsx` (Enrolled + Attended sheets).
2. Refresh the opportunity export so change orders closing **after** each session are present.
3. (Optional) supply a roster CSV with `HierarchyLevel` to add seniority to the match.
4. `python forward_experiment.py --integrated … --training … --out ./fwd_out` and read
   `results.json` → `did` (with the placebo passing and balance within |SMD|<0.10).
