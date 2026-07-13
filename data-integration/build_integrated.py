"""Build integrated Account/Opportunity/AI-evidence dataset from three source files."""
import pandas as pd
import numpy as np
import re
import difflib

UP = '/root/.claude/uploads/94fd7f02-ada3-55ab-8e58-2936eee13e0f/'
OUT = '/tmp/claude-0/-home-user-hello-world/94fd7f02-ada3-55ab-8e58-2936eee13e0f/scratchpad/Integrated_Account_Opportunity_AI_Dataset.xlsx'


def norm(s):
    """Normalize a name for matching: lowercase, strip non-alphanumerics."""
    if pd.isna(s):
        return ''
    return re.sub(r'[^a-z0-9]', '', str(s).lower())


def norm_loose(s):
    """Looser normalization: also drop common corporate suffixes."""
    n = str(s).lower() if not pd.isna(s) else ''
    n = re.sub(r'\b(inc|llc|llp|lp|ltd|corp|corporation|company|co|group|holdings?|partners?|solutions?|technologies|technology)\b', '', n)
    return re.sub(r'[^a-z0-9]', '', n)


def opp_prefix(name):
    """Extract account mnemonic prefix, skipping change-order prefixes like 'CO 3 - '."""
    s = str(name)
    s = re.sub(r'^CO\s*\d+\s*-\s*', '', s)
    m = re.match(r'^([A-Z0-9]{2,8})\s*-\s', s)
    return m.group(1) if m else np.nan


# ---------------------------------------------------------------- load sources
won = pd.read_excel(UP + '064bad35-Won_Opps_202620260713164807.xlsx', header=11).dropna(axis=1, how='all')
won.columns = [c.strip() for c in won.columns]
won = won[won['Opportunity Name'].notna()]
won = won[~won['Opportunity Name'].astype(str).str.contains('Confidential|Copyright', na=False)].copy()
won['Est. Close Date'] = pd.to_datetime(won['Est. Close Date'], errors='coerce')
won['Start Date'] = pd.to_datetime(won['Start Date'], errors='coerce')

rev = pd.ExcelFile(UP + '3259d9ae-RevOps_Account__Opportunity_Database_June_9.xlsx')
master = rev.parse('Master Account Database')
pipe = rev.parse('!RevOps 6-Month Pipeline')
old_pipe = rev.parse('OLD PIPELINE DATA')

ai_xl = pd.ExcelFile(UP + '91b116a5-AI_Work_SOWs_and_RTBs.xlsx')
ai_sows = ai_xl.parse('AI_SOWs')
rtb = ai_xl.parse('RTB', header=3)
rtb = rtb[rtb['Opportunity Name'].notna()].copy()
rtb['Close Date'] = pd.to_datetime(rtb['Close Date'], errors='coerce')

# ------------------------------------------------------- 1. account dimension
# Dedupe: prefer active Client status and a real (non-integration-user) AD.
master = master[master['Account Name'].notna()].copy()
master['_pref'] = (
    (master['Client Status'].eq('Client')).astype(int) * 2
    + (~master['Account Director'].fillna('').str.contains('Integration User')).astype(int)
)
master = (master.sort_values('_pref', ascending=False)
                .drop_duplicates(subset='Account Name', keep='first')
                .drop(columns='_pref')
                .sort_values('Account Name')
                .reset_index(drop=True))
master.insert(0, 'Account Key', master['Account Name'].map(norm))

master_by_norm = dict(zip(master['Account Key'], master['Account Name']))
master_by_loose = {}
for a in master['Account Name']:
    master_by_loose.setdefault(norm_loose(a), a)

# ----------------------------------------------- 2. account alias resolution
# Manual aliases for names automated matching can't safely resolve.
# (Only entries whose target exists in the Master DB take effect.)
MANUAL_ALIASES = {
    'ConEd': 'Consolidated Edison Company (ConEd)',
    'Frito-Lay': 'Frito-Lay,Inc.',
}

def resolve_account(raw, source):
    """Return (master_name, method, score). Falls back to raw name unresolved."""
    if pd.isna(raw) or str(raw).strip() == '':
        return (np.nan, 'missing', np.nan)
    raw = str(raw).strip()
    n = norm(raw)
    if n in master_by_norm:
        return (master_by_norm[n], 'exact', 1.0)
    if raw in MANUAL_ALIASES and norm(MANUAL_ALIASES[raw]) in master_by_norm:
        return (MANUAL_ALIASES[raw], 'manual-alias', 1.0)
    nl = norm_loose(raw)
    if nl and nl in master_by_loose:
        return (master_by_loose[nl], 'suffix-normalized', 0.95)
    # containment (one name inside the other, min length guard)
    cands = [m for k, m in master_by_norm.items()
             if len(n) >= 6 and len(k) >= 6 and (n in k or k in n)]
    if len(cands) == 1:
        return (cands[0], 'containment', 0.9)
    close = difflib.get_close_matches(n, list(master_by_norm.keys()), n=1, cutoff=0.87)
    if close:
        return (master_by_norm[close[0]], 'fuzzy',
                round(difflib.SequenceMatcher(None, n, close[0]).ratio(), 3))
    return (np.nan, 'unresolved', np.nan)


alias_rows = []
def resolve_series(series, source):
    out = []
    for raw in series:
        m, method, score = resolve_account(raw, source)
        out.append(m)
        if method not in ('exact', 'missing'):
            alias_rows.append({'Source': source, 'Raw Account Name': raw,
                               'Resolved Master Account': m, 'Method': method, 'Score': score})
    return out

won['Master Account'] = resolve_series(won['Account Name: Account Name'], 'Won Opps 2026')
pipe['Master Account'] = resolve_series(pipe['Account Name'], 'RevOps Pipeline')
rtb['Master Account'] = resolve_series(rtb['Account / Client'], 'RTB tab')

# accounts not in the Master DB keep their raw name so nothing drops out of rollups;
# the dimension marks them as not present in the 6/9 Master DB
for df, raw_col in [(won, 'Account Name: Account Name'), (pipe, 'Account Name'), (rtb, 'Account / Client')]:
    df['Account In Master DB'] = np.where(df['Master Account'].notna(), 'Yes', 'No')
    df['Master Account'] = df['Master Account'].fillna(df[raw_col])

alias_df = (pd.DataFrame(alias_rows)
              .drop_duplicates(subset=['Source', 'Raw Account Name'])
              .sort_values(['Method', 'Source', 'Raw Account Name'])
              .reset_index(drop=True))

# ------------------------------------------- 3. RTB -> won opp match waterfall
won['_norm_name'] = won['Opportunity Name'].map(norm)
won['_norm_orig'] = won['Original Opp Name'].map(norm)
won['_prefix'] = won['Opportunity Name'].map(opp_prefix)

def match_rtb_row(row):
    """Waterfall: exact name -> prefix+account+date -> account+fuzzy. Returns (won_opp, method)."""
    n = norm(row['Opportunity Name'])
    hit = won[(won['_norm_name'] == n) | (won['_norm_orig'] == n)]
    if len(hit):
        return (hit.iloc[0]['Opportunity Name'], 'exact-name')
    # containment on names within same account
    acct = row['Master Account']
    if pd.notna(acct):
        sub = won[won['Master Account'] == acct]
        contain = sub[sub['_norm_name'].apply(lambda k: n in k or k in n)]
        if len(contain) == 1:
            return (contain.iloc[0]['Opportunity Name'], 'name-containment')
        # prefix + close date proximity
        pref = opp_prefix(row['Opportunity Name'])
        if pd.notna(pref) and pd.notna(row['Close Date']):
            cand = sub[sub['_prefix'] == pref].copy()
            if len(cand):
                cand['_dd'] = (cand['Est. Close Date'] - row['Close Date']).abs().dt.days
                cand = cand[cand['_dd'] <= 45]
                if len(cand):
                    return (cand.sort_values('_dd').iloc[0]['Opportunity Name'], 'prefix+close-date')
        # fuzzy within account
        if len(sub):
            best = difflib.get_close_matches(n, sub['_norm_name'].tolist(), n=1, cutoff=0.75)
            if best:
                return (sub[sub['_norm_name'] == best[0]].iloc[0]['Opportunity Name'], 'account+fuzzy-name')
    return (np.nan, 'no-match (likely FY2025 close, outside Won Opps 2026 export)')

rtb[['Matched Won Opp', 'Opp Match Method']] = rtb.apply(
    lambda r: pd.Series(match_rtb_row(r)), axis=1)

# --------------------------------------- 4. AI_SOWs -> account from doc titles
# Build helper indexes over ALL opportunity names (won + both pipeline snapshots).
from collections import Counter

all_opps = pd.concat([
    pd.DataFrame({'opp': won['Opportunity Name'], 'acct': won['Account Name: Account Name']}),
    pd.DataFrame({'opp': pipe['Opportunity Name'], 'acct': pipe['Account Name']}),
    pd.DataFrame({'opp': old_pipe['Opportunity Name'], 'acct': old_pipe['Account Name']}),
]).dropna().drop_duplicates()
all_opps['_n'] = all_opps['opp'].map(norm)

# code -> account map from opp-name prefixes across all sources; drop ambiguous codes
code_counts = {}
for o, a in zip(all_opps['opp'], all_opps['acct']):
    c = opp_prefix(o)
    if c:
        code_counts.setdefault(c, Counter())[a] += 1
CODE_MAP = {c: cnt.most_common(1)[0][0] for c, cnt in code_counts.items() if len(cnt) == 1}
# curated code aliases for accounts whose opps predate all three files
CODE_MAP.update({'PALO': 'Palo Alto Networks', 'PANW': 'Palo Alto Networks'})
GENERIC_TOKENS = {'SOW', 'WMP', 'WM', 'LLC', 'PDF', 'DOCX', 'THE', 'AND', 'FOR', 'OUS',
                  'CO', 'PO', 'AI', 'ML', 'GENAI', 'CLEAN', 'FY', 'CFO', 'OCM', 'PMO', 'ERP', 'CRM'}

# distinctive-word -> account map over the full account universe (master + opp sources)
STOP_WORDS = {'group', 'holdings', 'holding', 'partners', 'partner', 'company', 'inc', 'llc', 'llp',
              'corp', 'corporation', 'solutions', 'services', 'service', 'capital', 'the', 'and',
              'north', 'america', 'american', 'technologies', 'technology', 'financial', 'global',
              'health', 'healthcare', 'management', 'international', 'systems', 'energy', 'bank',
              'insurance', 'media', 'software', 'west', 'monroe', 'enterprises', 'ventures',
              # generic business words that also appear in SOW-title language
              'advisory', 'advisors', 'accounting', 'transformation', 'workshop', 'consulting',
              'training', 'digital', 'strategy', 'platform', 'governance', 'support', 'enablement',
              'assessment', 'program', 'project', 'agent', 'build', 'building', 'intelligent',
              'automation', 'analytics', 'design', 'workforce', 'model', 'value', 'creation', 'plus'}
account_universe = pd.concat([master['Account Name'], all_opps['acct']]).dropna().unique()
tok_counts = {}
for a in account_universe:
    for w in set(re.findall(r'[a-z0-9]{4,}', str(a).lower())):
        if w not in STOP_WORDS:
            tok_counts.setdefault(w, set()).add(a)
TOKEN_MAP = {w: list(s)[0] for w, s in tok_counts.items() if len(s) == 1}

BOILERPLATE = {'attached', 'document', 'documents', 'title', 'titles', 'generic', 'connector',
               'output', 'metadata', 'references', 'reference', 'explicit', 'explicitly', 'mention',
               'executed', 'fully', 'signed', 'available', 'validation', 'captured', 'summary',
               'extract', 'file', 'excuted', 'sign', 'change', 'order'}

def extract_title_fragments(text):
    # greedy capture after the first 'title(s):', then split on ';' so multi-title rows keep all titles
    frags = re.findall(r'titles?\s*:?\s*(.+)', str(text), flags=re.I)
    out = []
    for f in frags:
        f = re.sub(r'\.(docx|pdf|xlsx)\b', '', f, flags=re.I).replace('_', ' ')
        for piece in re.split(r'[;]', f):
            piece = piece.strip()
            if piece:
                out.append(piece)
                # retry variant with version/date/vendor noise stripped (keep 4-digit years)
                stripped = re.sub(
                    r'\bv\d[\d\.]*\b|\b\d[\d_\-\.]{5,}\b|fully executed|signed|clean'
                    r'|west monroe|\bwmp?\b|\bsow\b|\bpartners\b',
                    '', piece, flags=re.I).strip(' -_')
                if stripped and stripped != piece:
                    out.append(stripped)
    return out

def match_ai_sow_row(text):
    """Waterfall: title<->opp-name containment -> code map -> distinctive token.
    Matching runs on extracted title fragments only, never boilerplate.
    Returns (master-or-raw account, matched opp or NaN, method)."""
    frags = extract_title_fragments(text)
    frag_text = ' ; '.join(frags)
    # (a) bidirectional containment between title fragments and opportunity names
    for frag in frags:
        fn = norm(frag)
        if len(fn) < 10:
            continue
        hits = all_opps[all_opps['_n'].apply(lambda k: (len(k) >= 10) and (fn in k or k in fn))]
        if len(hits) and hits['acct'].nunique() == 1:
            return (hits.iloc[0]['acct'], hits.iloc[0]['opp'], 'doc-title matches opportunity name')
    # (b) account-code prefix found in title fragments
    tokens = set(re.findall(r'\b[A-Z0-9]{2,8}\b', frag_text)) - GENERIC_TOKENS
    code_hits = {CODE_MAP[t] for t in tokens if t in CODE_MAP}
    if len(code_hits) == 1:
        return (code_hits.pop(), np.nan, 'account-code prefix in doc title')
    # (c) distinctive account-name word in title fragments
    words = set(re.findall(r'[a-z0-9]{4,}', frag_text.lower())) - BOILERPLATE
    tok_hits = {TOKEN_MAP[w] for w in words if w in TOKEN_MAP}
    if len(tok_hits) == 1:
        return (tok_hits.pop(), np.nan, 'account-name word in doc title')
    hint = ', '.join(sorted(tokens)[:5]) if tokens else 'none'
    return (np.nan, np.nan, f'unmatched — needs manual review (token hints: {hint})')

# titles live only in the SOW-evidence field; RTB prose would pollute fragment extraction
_res = ai_sows.apply(lambda r: pd.Series(match_ai_sow_row(str(r['SOW validation evidence']))), axis=1)
ai_sows[['Account (inferred)', 'Matched Opp Name', 'Account Match Method']] = _res

# resolve inferred accounts to master
ai_sows['Guessed Master Account'] = [resolve_account(a, 'AI_SOWs')[0] if pd.notna(a) else np.nan
                                     for a in ai_sows['Account (inferred)']]
# where not resolvable to master, keep the raw account universe name
ai_sows['Guessed Master Account'] = ai_sows['Guessed Master Account'].fillna(ai_sows['Account (inferred)'])

# ------------------------------------------------------ 5. AI evidence (union)
rtb_ev = pd.DataFrame({
    'Evidence Source': 'RTB tab',
    'Opportunity Name (as given)': rtb['Opportunity Name'],
    'Account (as given)': rtb['Account / Client'],
    'Master Account': rtb['Master Account'],
    'Close Date': rtb['Close Date'],
    'AI Offering / Capability': rtb['AI-related Offering, Service, or Capability'],
    'RTB Evidence': rtb['Relevant Ring the Bell evidence'],
    'SOW Evidence': rtb['SOW validation evidence'],
    'Confidence': rtb['Confidence level'],
    'Explanation': rtb['Brief explanation of why this should or should not count as AI-leveraged work'],
    'Matched Opportunity': rtb['Matched Won Opp'],
    'Match Method': rtb['Opp Match Method'],
})
sow_ev = pd.DataFrame({
    'Evidence Source': 'AI_SOWs tab',
    'Opportunity Name (as given)': np.nan,
    'Account (as given)': np.nan,
    'Master Account': ai_sows['Guessed Master Account'],
    'Close Date': pd.NaT,
    'AI Offering / Capability': ai_sows['AI-related Offering, Service, or Capability'],
    'RTB Evidence': ai_sows['Relevant Ring the Bell evidence'],
    'SOW Evidence': ai_sows['SOW validation evidence'],
    'Confidence': ai_sows['Confidence level'],
    'Explanation': ai_sows['Brief explanation of why this should or should not count as AI-leveraged work'],
    'Matched Opportunity': ai_sows['Matched Opp Name'],
    'Match Method': ai_sows['Account Match Method'],
})
ai_evidence = pd.concat([rtb_ev, sow_ev], ignore_index=True)

ai_opps = set(ai_evidence['Matched Opportunity'].dropna())
ai_accounts = set(ai_evidence['Master Account'].dropna())

# -------------------------------------------------------- 6. opportunity fact
won_fact = pd.DataFrame({
    'Record Source': 'Won Opps 2026 (7/13 export)',
    'Status': 'Won',
    'Opportunity Name': won['Opportunity Name'],
    'Original Opp Name': won['Original Opp Name'],
    'Is Change Order': won['Opportunity Name'].ne(won['Original Opp Name']).map({True: 'Yes', False: 'No'}),
    'Account (as given)': won['Account Name: Account Name'],
    'Master Account': won['Master Account'],
    'Fees (converted)': won['Estimated Fees (converted)'],
    'Est. Close Date': won['Est. Close Date'],
    'Start Date': won['Start Date'],
    'Stage': won['Stage'],
    'Pursuit Team': won['Pursuit Team'],
})
pipe_fact = pd.DataFrame({
    'Record Source': 'RevOps Pipeline (6/9 snapshot)',
    'Status': 'Open Pipeline',
    'Opportunity Name': pipe['Opportunity Name'],
    'Original Opp Name': np.nan,
    'Is Change Order': np.nan,
    'Account (as given)': pipe['Account Name'],
    'Master Account': pipe['Master Account'],
    'Fees (converted)': pipe['Estimated Fees (converted).amount'],
    'Est. Close Date': pipe['Est. Close Date'],
    'Start Date': pd.NaT,
    'Stage': pipe['Stage'],
    'Pursuit Team': pipe['Pursuit Team'],
})
# carry useful pipeline-only fields
for col in ['Probability (%)', 'Practice', 'Offering', 'Capabilities / Services', 'Managed By', 'Business Developer']:
    won_fact[col] = np.nan
    pipe_fact[col] = pipe[col].values

fact = pd.concat([won_fact, pipe_fact], ignore_index=True)

# flag pipeline opps that later appear as won (converted since the 6/9 snapshot)
won_names_norm = set(won['_norm_name']) | set(won['_norm_orig'].dropna())
fact['_n'] = fact['Opportunity Name'].map(norm)
fact['Converted Since Snapshot'] = np.where(
    (fact['Status'] == 'Open Pipeline') & fact['_n'].isin(won_names_norm), 'Yes', '')

# AI flags
fact['AI-Leveraged (opp evidence)'] = np.where(fact['Opportunity Name'].isin(ai_opps), 'Yes', '')
fact['Account Has AI Evidence'] = np.where(fact['Master Account'].isin(ai_accounts), 'Yes', '')
fact = fact.drop(columns='_n')

# enrich with key account attributes
acct_attrs = master[['Account Name', 'Account Segment Category', 'Account Segment',
                     'Account Industry', 'Account Director', 'Client Size', 'Client Status', 'Parent Account']]
fact = fact.merge(acct_attrs, left_on='Master Account', right_on='Account Name', how='left').drop(columns='Account Name')

# --------------------------------------------- 7. account dimension AI rollups
won_by_acct = won_fact.groupby('Master Account').agg(
    won_opps_2026=('Opportunity Name', 'count'),
    won_fees_2026=('Fees (converted)', 'sum')).reset_index()
ai_by_acct = (ai_evidence.dropna(subset=['Master Account'])
              .groupby('Master Account')
              .agg(ai_evidence_rows=('Evidence Source', 'count'),
                   ai_high_confidence_rows=('Confidence', lambda s: (s == 'High').sum()))
              .reset_index())
pipe_by_acct = pipe_fact.groupby('Master Account').agg(
    open_pipeline_opps=('Opportunity Name', 'count'),
    open_pipeline_fees=('Fees (converted)', 'sum')).reset_index()

# supplemental rows: accounts seen in won/pipeline/AI evidence but absent from the 6/9 Master DB
seen_accounts = (set(won['Master Account'].dropna()) | set(pipe['Master Account'].dropna())
                 | set(ai_evidence['Master Account'].dropna()))
extra = sorted(seen_accounts - set(master['Account Name']))
master['In 6-9 Master DB'] = 'Yes'
extra_df = pd.DataFrame({'Account Key': [norm(a) for a in extra], 'Account Name': extra,
                         'In 6-9 Master DB': 'No'})
dim_base = pd.concat([master, extra_df], ignore_index=True)

dim = (dim_base
       .merge(won_by_acct, left_on='Account Name', right_on='Master Account', how='left').drop(columns='Master Account')
       .merge(pipe_by_acct, left_on='Account Name', right_on='Master Account', how='left').drop(columns='Master Account')
       .merge(ai_by_acct, left_on='Account Name', right_on='Master Account', how='left').drop(columns='Master Account'))
for c in ['won_opps_2026', 'open_pipeline_opps', 'ai_evidence_rows', 'ai_high_confidence_rows']:
    dim[c] = dim[c].fillna(0).astype(int)
dim = dim.rename(columns={
    'won_opps_2026': 'Won Opps 2026 (count)', 'won_fees_2026': 'Won Fees 2026 (integrated)',
    'open_pipeline_opps': 'Open Pipeline Opps (6/9)', 'open_pipeline_fees': 'Open Pipeline Fees (6/9)',
    'ai_evidence_rows': 'AI Evidence Rows', 'ai_high_confidence_rows': 'AI Evidence Rows (High Confidence)'})
dim['Has AI-Leveraged Work'] = np.where(dim['AI Evidence Rows'] > 0, 'Yes', '')

# ------------------------------------------------------------ 8. review queue
review = []
for _, r in alias_df[alias_df['Method'].isin(['unresolved', 'fuzzy', 'containment'])].iterrows():
    review.append({'Issue Type': f"Account match: {r['Method']}", 'Source': r['Source'],
                   'Item': r['Raw Account Name'],
                   'Current Resolution': r['Resolved Master Account'] if pd.notna(r['Resolved Master Account']) else 'NOT LINKED',
                   'Action Needed': 'Confirm or correct the account mapping'})
for _, r in rtb[rtb['Matched Won Opp'].isna()].iterrows():
    review.append({'Issue Type': 'RTB opp not in Won Opps 2026 export', 'Source': 'RTB tab',
                   'Item': r['Opportunity Name'],
                   'Current Resolution': f"Account-level link only ({r['Master Account'] if pd.notna(r['Master Account']) else 'no account link'})",
                   'Action Needed': 'Closed ' + (r['Close Date'].strftime('%Y-%m-%d') if pd.notna(r['Close Date']) else '?')
                                    + ' — pull a 2025 won-opps export to link at opp level'})
for _, r in rtb[rtb['Opp Match Method'].isin(['account+fuzzy-name', 'prefix+close-date', 'name-containment'])].iterrows():
    review.append({'Issue Type': 'RTB opp matched non-exactly', 'Source': 'RTB tab',
                   'Item': r['Opportunity Name'],
                   'Current Resolution': f"→ {r['Matched Won Opp']} ({r['Opp Match Method']})",
                   'Action Needed': 'Confirm the opportunity match'})
for _, r in ai_sows[ai_sows['Guessed Master Account'].isna()].iterrows():
    review.append({'Issue Type': 'AI_SOWs row has no account link', 'Source': 'AI_SOWs tab',
                   'Item': str(r['SOW validation evidence'])[:120],
                   'Current Resolution': 'NOT LINKED',
                   'Action Needed': 'Identify client from SOW title / regenerate extract with Opportunity ID'})
for _, r in ai_sows[ai_sows['Guessed Master Account'].notna()].iterrows():
    review.append({'Issue Type': 'AI_SOWs account inferred from doc title', 'Source': 'AI_SOWs tab',
                   'Item': str(r['SOW validation evidence'])[:120],
                   'Current Resolution': f"→ {r['Guessed Master Account']} ({r['Account Match Method']})",
                   'Action Needed': 'Confirm the inferred account (AI_SOWs has no key column, all links are inferred)'})
review_df = pd.DataFrame(review)

# ------------------------------------------------------------------ 9. README
readme = pd.DataFrame({'Integrated Account / Opportunity / AI Dataset': [
    'Built 2026-07-13 from: Won_Opps_2026 (Salesforce export 7/13), RevOps Account & Opportunity Database (6/9 snapshot), AI_Work_SOWs_and_RTBs.',
    '',
    'SHEETS',
    'Accounts — one row per account. Base: Master Account Database (deduped: duplicate names removed, preferring active-Client rows with a real Account Director), plus supplemental rows (In 6-9 Master DB = No) for accounts seen only in won opps / pipeline / AI evidence. Adds rollups: FY2026 won fees/opps, open pipeline (6/9), AI-evidence counts, Has AI-Leveraged Work flag.',
    'Opportunities — union fact table: won opps (FY2026, 7/13 export) + open pipeline opps (6/9 snapshot). Linked to Accounts via Master Account. Includes Is Change Order, Converted Since Snapshot (pipeline opp later appears as won), and AI flags.',
    'AI Evidence — all 95 AI rows (33 RTB + 62 AI_SOWs) with account links and, where possible, the matched opportunity. Match Method records how each link was made; treat non-exact methods as provisional until confirmed via the Review Queue.',
    'Alias Map — every non-exact account-name resolution (method + score). Exact matches are not listed.',
    'Review Queue — items needing a human decision: unresolved accounts, fuzzy/inferred matches to confirm, RTB opps outside the FY2026 export, unlinked AI_SOWs rows.',
    '',
    'MATCHING WATERFALL (accounts): exact normalized name → manual alias → suffix-stripped name → containment → fuzzy (cutoff 0.87). Unresolved names are kept as-is and flagged In 6-9 Master DB = No.',
    'MATCHING WATERFALL (RTB opp → won opp): exact name → name containment within account → account-code prefix + close date (±45d) → fuzzy within account.',
    'MATCHING WATERFALL (AI_SOWs, which has no key column): SOW doc title ↔ opportunity-name containment → account-code prefix in title (e.g. GALLO, PALO) → distinctive account-name word in title. PALO/PANW were manually mapped to Palo Alto Networks.',
    '',
    'KNOWN LIMITATIONS',
    '- Most RTB rows closed in FY2025 and cannot link to the FY2026-only won export; they carry account-level links only. Pull a 2025 won-opps export to complete them.',
    '- AI_SOWs tab has no key column; account links were inferred from SOW document titles and are marked with their method. Regenerating that extract with Salesforce Opportunity ID is the durable fix.',
    '- RevOps pipeline is a June 9 snapshot vs a July 13 won export; treat pipeline-vs-won comparisons as ~5 weeks apart.',
    '- Fees are as-exported ("converted" currency fields); no restatement applied.',
]})

# ------------------------------------------------------------------ 10. write
with pd.ExcelWriter(OUT, engine='openpyxl') as xw:
    readme.to_excel(xw, sheet_name='README', index=False)
    dim.to_excel(xw, sheet_name='Accounts', index=False)
    fact.to_excel(xw, sheet_name='Opportunities', index=False)
    ai_evidence.to_excel(xw, sheet_name='AI Evidence', index=False)
    alias_df.to_excel(xw, sheet_name='Alias Map', index=False)
    review_df.to_excel(xw, sheet_name='Review Queue', index=False)

# ------------------------------------------------------------------ summary
print('=== BUILD SUMMARY ===')
print(f'Accounts: {len(dim)} (deduped from {1054})')
print(f'Opportunities: {len(fact)} = {len(won_fact)} won + {len(pipe_fact)} pipeline')
print(f'  Won opps linked to master account: {won_fact["Master Account"].notna().sum()}/{len(won_fact)}')
print(f'  Pipeline opps linked: {pipe_fact["Master Account"].notna().sum()}/{len(pipe_fact)}')
print(f'  Converted since snapshot: {(fact["Converted Since Snapshot"]=="Yes").sum()}')
print(f'AI evidence rows: {len(ai_evidence)}')
print(f'  RTB with account link: {rtb["Master Account"].notna().sum()}/{len(rtb)}')
print(f'  RTB matched to a FY2026 won opp: {rtb["Matched Won Opp"].notna().sum()}/{len(rtb)}')
print('  RTB match methods:', rtb['Opp Match Method'].value_counts().to_dict())
print(f'  AI_SOWs with account guess: {ai_sows["Guessed Master Account"].notna().sum()}/{len(ai_sows)}')
print(f'Alias map rows: {len(alias_df)} | methods: {alias_df["Method"].value_counts().to_dict()}')
print(f'Review queue: {len(review_df)}')
print(f'Accounts flagged AI-leveraged: {(dim["Has AI-Leveraged Work"]=="Yes").sum()}')
won_ai_fees = fact.loc[(fact['Status']=='Won') & (fact['AI-Leveraged (opp evidence)']=='Yes'), 'Fees (converted)'].sum()
won_acct_ai_fees = fact.loc[(fact['Status']=='Won') & (fact['Account Has AI Evidence']=='Yes'), 'Fees (converted)'].sum()
print(f'FY2026 won fees on AI-matched opps: ${won_ai_fees:,.0f}')
print(f'FY2026 won fees at accounts with AI evidence: ${won_acct_ai_fees:,.0f} of ${fact.loc[fact["Status"]=="Won","Fees (converted)"].sum():,.0f}')
