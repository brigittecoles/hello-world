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
def load_won_export(path):
    """Salesforce won-opps report export: headers at row 12, footer boilerplate rows."""
    df = pd.read_excel(path, header=11).dropna(axis=1, how='all')
    df.columns = [c.strip() for c in df.columns]
    df = df[df['Opportunity Name'].notna()]
    df = df[~df['Opportunity Name'].astype(str).str.contains('Confidential|Copyright', na=False)].copy()
    df['Est. Close Date'] = pd.to_datetime(df['Est. Close Date'], errors='coerce')
    df['Start Date'] = pd.to_datetime(df['Start Date'], errors='coerce')
    return df

won = load_won_export(UP + '064bad35-Won_Opps_202620260713164807.xlsx')      # FY2026 closes
won25 = load_won_export(UP + '88833b9a-Won_Opps_202620260713214830.xlsx')    # FY2025 closes

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
won25['Master Account'] = resolve_series(won25['Account Name: Account Name'], 'Won Opps 2025')
pipe['Master Account'] = resolve_series(pipe['Account Name'], 'RevOps Pipeline')
rtb['Master Account'] = resolve_series(rtb['Account / Client'], 'RTB tab')

# accounts not in the Master DB keep their raw name so nothing drops out of rollups;
# the dimension marks them as not present in the 6/9 Master DB
for df, raw_col in [(won, 'Account Name: Account Name'), (won25, 'Account Name: Account Name'),
                    (pipe, 'Account Name'), (rtb, 'Account / Client')]:
    df['Account In Master DB'] = np.where(df['Master Account'].notna(), 'Yes', 'No')
    df['Master Account'] = df['Master Account'].fillna(df[raw_col])

alias_df = (pd.DataFrame(alias_rows)
              .drop_duplicates(subset=['Source', 'Raw Account Name'])
              .sort_values(['Method', 'Source', 'Raw Account Name'])
              .reset_index(drop=True))

# ------------------------------------------- 3. RTB -> won opp match waterfall
won_all = pd.concat([won.assign(FY='2026'), won25.assign(FY='2025')], ignore_index=True)
won_all['_norm_name'] = won_all['Opportunity Name'].map(norm)
won_all['_norm_orig'] = won_all['Original Opp Name'].map(norm)
won_all['_prefix'] = won_all['Opportunity Name'].map(opp_prefix)

def match_rtb_row(row):
    """Waterfall over both FY exports: exact name -> containment -> prefix+date -> account+fuzzy.
    Returns (won_opp, fy, method)."""
    n = norm(row['Opportunity Name'])
    hit = won_all[(won_all['_norm_name'] == n) | (won_all['_norm_orig'] == n)]
    if len(hit):
        return (hit.iloc[0]['Opportunity Name'], hit.iloc[0]['FY'], 'exact-name')
    # containment on names within same account
    acct = row['Master Account']
    if pd.notna(acct):
        sub = won_all[won_all['Master Account'] == acct]
        contain = sub[sub['_norm_name'].apply(lambda k: n in k or k in n)]
        if len(contain) == 1:
            return (contain.iloc[0]['Opportunity Name'], contain.iloc[0]['FY'], 'name-containment')
        # prefix + close date proximity
        pref = opp_prefix(row['Opportunity Name'])
        if pd.notna(pref) and pd.notna(row['Close Date']):
            cand = sub[sub['_prefix'] == pref].copy()
            if len(cand):
                cand['_dd'] = (cand['Est. Close Date'] - row['Close Date']).abs().dt.days
                cand = cand[cand['_dd'] <= 45]
                if len(cand):
                    best = cand.sort_values('_dd').iloc[0]
                    return (best['Opportunity Name'], best['FY'], 'prefix+close-date')
        # fuzzy within account
        if len(sub):
            best = difflib.get_close_matches(n, sub['_norm_name'].tolist(), n=1, cutoff=0.75)
            if best:
                b = sub[sub['_norm_name'] == best[0]].iloc[0]
                return (b['Opportunity Name'], b['FY'], 'account+fuzzy-name')
    return (np.nan, np.nan, 'no-match in FY2025/FY2026 won exports')

rtb[['Matched Won Opp', 'Matched FY', 'Opp Match Method']] = rtb.apply(
    lambda r: pd.Series(match_rtb_row(r)), axis=1)

# --------------------------------------- 4. AI_SOWs -> account from doc titles
# Build helper indexes over ALL opportunity names (won + both pipeline snapshots).
from collections import Counter

all_opps = pd.concat([
    pd.DataFrame({'opp': won['Opportunity Name'], 'acct': won['Account Name: Account Name']}),
    pd.DataFrame({'opp': won25['Opportunity Name'], 'acct': won25['Account Name: Account Name']}),
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

# Curated manual mappings for rows the automated waterfall can't resolve.
# Keyed by row index with an evidence snippet as a guard against source reordering.
# basis = the opportunity-name evidence the mapping rests on.
MANUAL_SOW_MAP = [
    (1,  'Ian Smith AI Retainer', 'Audax Management Company',
         'CO 1 - ADX - AI Retainer (Change Order 01 aligns; Audax AI Retainer family)', 'Medium'),
    (3,  'OCFO_AI_Use_Case_Enablement', 'Gallagher Benefit Services',
         'GBN - OCFO AI Use Case Enablement (exact phrase)', 'High'),
    (4,  'AI in BEM', 'Southern California Edison',
         'SCE - AI in BEM Program Development - Phase I (exact phrase)', 'High'),
    (13, 'Intelligent Automation Strategy and Design', 'J.D. Power and Associates',
         'JDP - DataOps Intelligent Automation Strategy; RTB cites Intellio Agent POC', 'Medium'),
    (15, 'Cyber_Data_AI_SOW', 'Emory University',
         'EMORY - Cyber, Data, and AI Assessments and Roadmap', 'High'),
    (25, 'Fund Admin & Accounting Copilot Training', 'The Riverside Company',
         'RC - Copilot Training for Accounting & Fund Admin (exact phrase)', 'High'),
    (28, 'Intellio Policy', 'Walmart US',
         'WMTUS - Energy - Intellio Policy AI (RTB describes Intellio Policy build)', 'High'),
    (32, 'GenAI Advisory', 'Caresource',
         'CSRC - CareSource Data & Reporting GenAI Advisory CO 1-4 (report conversion matches)', 'Medium'),
    (37, 'AI Workshop', 'Mariani Landscape',
         'CO 2 - MARIL SSA - AI Workshop (only AI Workshop opp)', 'Medium'),
    (38, 'SOW title generic in connector output', 'Capital One',
         'CAPO - CO 1 - DFS - Payment Services CRM Analytics + AI Knowledgebase Assessment (offering matches exactly)', 'High'),
    (39, 'SOW title generic', 'Travis Credit Union',
         'TRVCU - AI Accelerated Process Mapping (only AI process-mapping opp)', 'Medium'),
    (41, 'Change_Order_to_AI_Program_Support', 'Kymanox LLC',
         'KYNOX - AI Program Support (this row is its change order)', 'Medium'),
    (44, 'Fraud Alerting & Data Science Enablement', 'ConnexPay',
         'CONX - Fraud Alerting Build & AI Finalization family', 'High'),
    (45, 'GenAI Advisory', 'Caresource',
         'CSRC - CareSource Data & Reporting GenAI Advisory CO 1-4', 'Medium'),
    (46, 'GenAI Advisory', 'Caresource',
         'CSRC - CareSource Data & Reporting GenAI Advisory CO 1-4', 'Medium'),
    (47, 'AISprint', 'Palo Alto Networks',
         'PANW/PALO quarterly AISprint pattern (other AISprint rows are Palo Alto)', 'Medium'),
    (55, 'GenAI Advisory', 'Caresource',
         'CSRC - CareSource Data & Reporting GenAI Advisory CO 1-4', 'Medium'),
    (61, 'Lakehouse Build Fraud Modeling CO2', 'ConnexPay',
         'CO 2 - CONX - Lakehouse Build (exact CO number and scope)', 'High'),
    # --- round 2: matches found in logged opps per user direction ("all already logged") ---
    (10, 'Insurance AI Assessment', 'Inflexion',
         'INFLX - AI Opportunity and Risk Diligence Assessment (only PE-portfolio AI-diligence opp); "Insurance" likely the WM practice or a portfolio co', 'Medium'),
    (11, 'Agentic Transformation SOW', 'Anaqua',
         'ANQU - Agentic Transformation (exact opp name); alt: CRC Insurance Services (TIHI - KV Agentic Transformation Strategy)', 'Medium'),
    (12, 'AI Advisory SOW', 'Vizient, Inc.',
         'VHA - AI Advisory (exact opp name)', 'High'),
    (14, 'AI Platform SOW', 'Knox Lane LP',
         'KNXL - AI Platform (exact opp name)', 'High'),
    (16, 'EDA Use Case Delivery', 'Consolidated Edison Company (ConEd)',
         'CNED - EDA (Enterprise Data & Analytics) program + GCP Platform Foundation & AI Use Case Delivery CO1', 'High'),
    (23, 'EDA AI Workstreams', 'Consolidated Edison Company (ConEd)',
         'CNED - EDA (Enterprise Data & Analytics) AI workstreams; EDA confirmed as a ConEd program code', 'High'),
    (26, '02139753', 'Exelon Business Services Company, LLC',
         'EXE - AI Governance Planning (generic file title; AI-governance offering); alt: ConEd Data & AI Governance Optimization', 'Low'),
    (29, '202510_CP_Signed', 'ABC Fitness Solutions',
         'Intellio Evolve used on ABCF Service Transformation; SOW signed Oct 2025; alt: Nextech/Surescripts/Aven Evolve pilots', 'Low'),
    (33, 'Nigel', "Shearer's",
         "SHEAS - Data Platform Build; RTB cites the 'Nigel' AI-SQL tool for Shearer's; alt: Arthur J. Gallagher", 'Medium'),
    (58, 'generic: sign.pdf', 'Health Care Service Corporation',
         'CO 1 - HCS - MA Contact Center - Driving Efficiency with Gen AI (offering "GenAI contact center / efficiency" matches verbatim)', 'High'),
]
for idx, snippet, acct, basis, conf in MANUAL_SOW_MAP:
    _guard = (str(ai_sows.iloc[idx]['SOW validation evidence']) + ' '
              + str(ai_sows.iloc[idx]['Relevant Ring the Bell evidence'])).lower()
    if snippet.lower() in _guard:
        ai_sows.iloc[idx, ai_sows.columns.get_loc('Account (inferred)')] = acct
        ai_sows.iloc[idx, ai_sows.columns.get_loc('Account Match Method')] = f'manual ({conf} confidence): {basis}'
    else:
        print(f'WARNING: manual map row {idx} snippet mismatch, skipped: {snippet}')

# All previously-ambiguous rows are now mapped above; none remain candidate-only.
SOW_CANDIDATES = {}

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
    'Matched FY': rtb['Matched FY'],
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
    'Matched FY': np.nan,
    'Match Method': ai_sows['Account Match Method'],
})
ai_evidence = pd.concat([rtb_ev, sow_ev], ignore_index=True)

ai_opps = set(ai_evidence['Matched Opportunity'].dropna())
ai_accounts = set(ai_evidence['Master Account'].dropna())

# -------------------------------------------------------- 6. opportunity fact
def won_to_fact(df, source_label):
    return pd.DataFrame({
        'Record Source': source_label,
        'Status': 'Won',
        'Opportunity Name': df['Opportunity Name'],
        'Original Opp Name': df['Original Opp Name'],
        'Is Change Order': df['Opportunity Name'].ne(df['Original Opp Name']).map({True: 'Yes', False: 'No'}),
        'Account (as given)': df['Account Name: Account Name'],
        'Master Account': df['Master Account'],
        'Fees (converted)': df['Estimated Fees (converted)'],
        'Est. Close Date': df['Est. Close Date'],
        'Start Date': df['Start Date'],
        'Stage': df['Stage'],
        'Pursuit Team': df['Pursuit Team'],
    })

won_fact = won_to_fact(won, 'Won Opps 2026 (7/13 export)')
won25_fact = won_to_fact(won25, 'Won Opps 2025 (7/13 export)')
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
    won25_fact[col] = np.nan
    pipe_fact[col] = pipe[col].values

fact = pd.concat([won25_fact, won_fact, pipe_fact], ignore_index=True)

# flag pipeline opps that later appear as won (converted since the 6/9 snapshot)
_w26 = won_all[won_all['FY'] == '2026']
won_names_norm = set(_w26['_norm_name']) | set(_w26['_norm_orig'].dropna())
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
won25_by_acct = won25_fact.groupby('Master Account').agg(
    won_opps_2025=('Opportunity Name', 'count'),
    won_fees_2025=('Fees (converted)', 'sum')).reset_index()
ai_by_acct = (ai_evidence.dropna(subset=['Master Account'])
              .groupby('Master Account')
              .agg(ai_evidence_rows=('Evidence Source', 'count'),
                   ai_high_confidence_rows=('Confidence', lambda s: (s == 'High').sum()))
              .reset_index())
pipe_by_acct = pipe_fact.groupby('Master Account').agg(
    open_pipeline_opps=('Opportunity Name', 'count'),
    open_pipeline_fees=('Fees (converted)', 'sum')).reset_index()

# supplemental rows: accounts seen in won/pipeline/AI evidence but absent from the 6/9 Master DB
seen_accounts = (set(won['Master Account'].dropna()) | set(won25['Master Account'].dropna())
                 | set(pipe['Master Account'].dropna())
                 | set(ai_evidence['Master Account'].dropna()))
extra = sorted(seen_accounts - set(master['Account Name']))
master['In 6-9 Master DB'] = 'Yes'
extra_df = pd.DataFrame({'Account Key': [norm(a) for a in extra], 'Account Name': extra,
                         'In 6-9 Master DB': 'No'})
dim_base = pd.concat([master, extra_df], ignore_index=True)

dim = (dim_base
       .merge(won_by_acct, left_on='Account Name', right_on='Master Account', how='left').drop(columns='Master Account')
       .merge(won25_by_acct, left_on='Account Name', right_on='Master Account', how='left').drop(columns='Master Account')
       .merge(pipe_by_acct, left_on='Account Name', right_on='Master Account', how='left').drop(columns='Master Account')
       .merge(ai_by_acct, left_on='Account Name', right_on='Master Account', how='left').drop(columns='Master Account'))
for c in ['won_opps_2026', 'won_opps_2025', 'open_pipeline_opps', 'ai_evidence_rows', 'ai_high_confidence_rows']:
    dim[c] = dim[c].fillna(0).astype(int)
dim = dim.rename(columns={
    'won_opps_2026': 'Won Opps 2026 (count)', 'won_fees_2026': 'Won Fees 2026 (integrated)',
    'won_opps_2025': 'Won Opps 2025 (count)', 'won_fees_2025': 'Won Fees 2025 (integrated)',
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
    review.append({'Issue Type': 'RTB opp not matched to a won opp', 'Source': 'RTB tab',
                   'Item': r['Opportunity Name'],
                   'Current Resolution': f"Account-level link only ({r['Master Account'] if pd.notna(r['Master Account']) else 'no account link'})",
                   'Action Needed': 'Closed ' + (r['Close Date'].strftime('%Y-%m-%d') if pd.notna(r['Close Date']) else '?')
                                    + ' — not found in either FY export; verify name/record type'})
for _, r in rtb[rtb['Opp Match Method'].isin(['account+fuzzy-name', 'prefix+close-date', 'name-containment'])].iterrows():
    review.append({'Issue Type': 'RTB opp matched non-exactly', 'Source': 'RTB tab',
                   'Item': r['Opportunity Name'],
                   'Current Resolution': f"→ {r['Matched Won Opp']} ({r['Opp Match Method']})",
                   'Action Needed': 'Confirm the opportunity match'})
for idx, r in ai_sows[ai_sows['Guessed Master Account'].isna()].iterrows():
    review.append({'Issue Type': 'AI_SOWs row has no account link', 'Source': 'AI_SOWs tab',
                   'Item': str(r['SOW validation evidence'])[:120],
                   'Current Resolution': 'NOT LINKED',
                   'Action Needed': SOW_CANDIDATES.get(idx,
                       'Identify client from SOW title / regenerate extract with Opportunity ID')})
for _, r in ai_sows[ai_sows['Guessed Master Account'].notna()].iterrows():
    review.append({'Issue Type': 'AI_SOWs account inferred from doc title', 'Source': 'AI_SOWs tab',
                   'Item': str(r['SOW validation evidence'])[:120],
                   'Current Resolution': f"→ {r['Guessed Master Account']} ({r['Account Match Method']})",
                   'Action Needed': 'Confirm the inferred account (AI_SOWs has no key column, all links are inferred)'})
review_df = pd.DataFrame(review)

# ------------------------------------------------------ 8b. crosswalk sheet
# One row per review-queue theme, enriched with people and ranked account candidates.
from collections import Counter as _Counter

ad_by_acct = dict(zip(master['Account Name'], master['Account Director'].fillna('')))
am_by_acct = dict(zip(master['Account Name'], master['Account Manager'].fillna('')))

def acct_people(acct):
    bits = []
    if ad_by_acct.get(acct):
        bits.append(f"AD: {ad_by_acct[acct]}")
    if am_by_acct.get(acct):
        bits.append(f"AM: {am_by_acct[acct]}")
    return '; '.join(bits)

def top_people(series_of_lists, n=4):
    """Most frequent names from ';'-separated people fields."""
    c = _Counter()
    for v in series_of_lists.dropna():
        for name in str(v).split(';'):
            name = name.strip()
            if name and name != '-' and 'INVALID' not in name:
                c[name] += 1
    return '; '.join(f'{k}' for k, _ in c.most_common(n))

def candidate_accounts(raw, n=3):
    """Ranked master-account suggestions below the auto-match threshold."""
    nn = norm(raw)
    out, seen = [], set()
    for k, m in master_by_norm.items():
        if len(nn) >= 5 and len(k) >= 5 and (nn in k or k in nn) and m not in seen:
            out.append(f'{m} (containment)'); seen.add(m)
    for c in difflib.get_close_matches(nn, list(master_by_norm.keys()), n=n, cutoff=0.55):
        m = master_by_norm[c]
        if m not in seen:
            score = difflib.SequenceMatcher(None, nn, c).ratio()
            out.append(f'{m} ({score:.2f})'); seen.add(m)
    return '; '.join(out[:n]) if out else 'none close — likely new/absent from 6/9 Master DB'

cross = []
# --- unresolved account names, enriched per source
for _, a in alias_df[alias_df['Method'] == 'unresolved'].iterrows():
    raw, src = a['Raw Account Name'], a['Source']
    fees, people, extra = 0.0, '', ''
    if src in ('Won Opps 2026', 'Won Opps 2025'):
        d = (won if src == 'Won Opps 2026' else won25)
        sub = d[d['Account Name: Account Name'] == raw]
        fees = sub['Estimated Fees (converted)'].sum()
        people = top_people(sub['Pursuit Team'])
        dates = pd.to_datetime(sub['Est. Close Date'])
        extra = f"{len(sub)} won opp(s), closes {dates.min():%b %Y}–{dates.max():%b %Y}"
    elif src == 'RevOps Pipeline':
        sub = pipe[pipe['Account Name'] == raw]
        fees = sub['Estimated Fees (converted).amount'].sum()
        ppl = pd.concat([sub['Managed By'], sub['Business Developer'], sub['Pursuit Team']])
        people = top_people(ppl)
        extra = f"{len(sub)} open pipeline opp(s)"
    elif src == 'RTB tab':
        sub = rtb[rtb['Account / Client'] == raw]
        extra = f"{len(sub)} AI evidence row(s)"
    cross.append({
        'Item': raw, 'Issue Type': 'Account not in 6/9 Master DB', 'Source': src,
        'Summary': extra, 'Fees Involved': round(fees) if fees else None,
        'People': people, 'Likely Account Candidates': candidate_accounts(raw),
        'Suggested Action': 'Confirm whether this is a new account or an alias of a Master DB account'})

# --- non-exact account resolutions to confirm
for _, a in alias_df[alias_df['Method'].isin(['fuzzy', 'containment', 'suffix-normalized'])].iterrows():
    res = a['Resolved Master Account']
    cross.append({
        'Item': a['Raw Account Name'], 'Issue Type': 'Account mapping to confirm', 'Source': a['Source'],
        'Summary': f"Auto-resolved by {a['Method']} (score {a['Score']})", 'Fees Involved': None,
        'People': acct_people(res), 'Likely Account Candidates': res,
        'Suggested Action': 'Confirm or correct this mapping'})

# --- RTB opp matches made non-exactly
for _, r in rtb[~rtb['Opp Match Method'].isin(['exact-name'])].iterrows():
    if pd.isna(r['Matched Won Opp']):
        continue
    acct = r['Master Account']
    sub = won_all[won_all['Opportunity Name'] == r['Matched Won Opp']]
    cross.append({
        'Item': r['Opportunity Name'], 'Issue Type': 'RTB opp match to confirm', 'Source': 'RTB tab',
        'Summary': f"Matched to '{r['Matched Won Opp']}' (FY{r['Matched FY']}) via {r['Opp Match Method']}",
        'Fees Involved': round(sub['Estimated Fees (converted)'].sum()) if len(sub) else None,
        'People': '; '.join(filter(None, [acct_people(acct), top_people(sub['Pursuit Team'], 3)])),
        'Likely Account Candidates': acct,
        'Suggested Action': 'Confirm the opportunity match'})

# --- AI_SOWs rows: unresolved get candidates; inferred/manual get a confirm row
for idx, r in ai_sows.iterrows():
    title = str(r['SOW validation evidence']).replace('Attached document title: ', '')[:90]
    offering = str(r['AI-related Offering, Service, or Capability'])[:70]
    acct = r['Guessed Master Account']
    if pd.isna(acct):
        cross.append({
            'Item': title, 'Issue Type': 'AI SOW unmapped', 'Source': 'AI_SOWs tab',
            'Summary': f"Offering: {offering} · Confidence: {r['Confidence level']}", 'Fees Involved': None,
            'People': '',
            'Likely Account Candidates': SOW_CANDIDATES.get(idx, 'no candidates identified'),
            'Suggested Action': 'Identify client from the SOW document or a regenerated extract with Opportunity ID'})
    else:
        method = str(r['Account Match Method'])
        cross.append({
            'Item': title, 'Issue Type': 'AI SOW mapping to confirm', 'Source': 'AI_SOWs tab',
            'Summary': f"Offering: {offering} · via {method[:90]}", 'Fees Involved': None,
            'People': acct_people(acct), 'Likely Account Candidates': acct,
            'Suggested Action': 'Confirm the inferred account'})

crosswalk_df = pd.DataFrame(cross)
_order = {'AI SOW unmapped': 0, 'AI SOW mapping to confirm': 1, 'RTB opp match to confirm': 2,
          'Account mapping to confirm': 3, 'Account not in 6/9 Master DB': 4}
crosswalk_df['_o'] = crosswalk_df['Issue Type'].map(_order)
crosswalk_df = (crosswalk_df.sort_values(['_o', 'Fees Involved'], ascending=[True, False])
                            .drop(columns='_o').reset_index(drop=True))
crosswalk_df.insert(1, 'Confirmed Account Name (fill in)', '')
CROSSWALK_OUT = OUT.replace('Integrated_Account_Opportunity_AI_Dataset.xlsx', 'Review_Queue_Crosswalk.xlsx')
with pd.ExcelWriter(CROSSWALK_OUT, engine='openpyxl') as cw:
    crosswalk_df.to_excel(cw, sheet_name='Crosswalk', index=False)
    ws = cw.sheets['Crosswalk']
    widths = {'A': 44, 'B': 30, 'C': 26, 'D': 16, 'E': 52, 'F': 14, 'G': 40, 'H': 52, 'I': 40}
    for col, w in widths.items():
        ws.column_dimensions[col].width = w
    ws.freeze_panes = 'A2'

# ------------------------------------------------------------------ 9. README
readme = pd.DataFrame({'Integrated Account / Opportunity / AI Dataset': [
     'Built 2026-07-13 from: Won Opps FY2026 + FY2025 (Salesforce exports 7/13), RevOps Account & Opportunity Database (6/9 snapshot), AI_Work_SOWs_and_RTBs.',
    '',
    'SHEETS',
    'Accounts — one row per account. Base: Master Account Database (deduped: duplicate names removed, preferring active-Client rows with a real Account Director), plus supplemental rows (In 6-9 Master DB = No) for accounts seen only in won opps / pipeline / AI evidence. Adds rollups: FY2026 won fees/opps, open pipeline (6/9), AI-evidence counts, Has AI-Leveraged Work flag.',
    'Opportunities — union fact table: won opps (FY2025 + FY2026, 7/13 exports) + open pipeline opps (6/9 snapshot). Linked to Accounts via Master Account. Includes Is Change Order, Converted Since Snapshot (pipeline opp later appears as won), and AI flags.',
    'AI Evidence — all 95 AI rows (33 RTB + 62 AI_SOWs) with account links and, where possible, the matched opportunity. Match Method records how each link was made; treat non-exact methods as provisional until confirmed via the Review Queue.',
    'Alias Map — every non-exact account-name resolution (method + score). Exact matches are not listed.',
    'Review Queue — items needing a human decision: unresolved accounts, fuzzy/inferred matches to confirm, unlinked AI_SOWs rows.',
    'Capital - People / Opportunity / Account / Practice — the production-function capital term K = labor + tokens, priced (labor = rate x utilization x 40h; tokens = credits x $0.05) and attributed. APPROXIMATE mode: a person\'s weekly capital is spread across the opportunities they staff (Pursuit Team -> roster join), fee-weighted. Flips to EXACT when the token feed carries a charge_code/project_id (set env WM_TOKEN_FEED to the full Codex export). Token layer today is the top-5-per-week leaderboard from four exec summaries (5/24-6/20/2026) — treat person-level dollars as illustrative; practice AI census is the full roster.',
    'Rate Card Ref — grade (roster HierarchyLevel) -> $/hr mapping used to price labor (from the WM rate card; practice does not change the rate in the card, so grade is the sole per-person key).',
    '',
    'MATCHING WATERFALL (accounts): exact normalized name → manual alias → suffix-stripped name → containment → fuzzy (cutoff 0.87). Unresolved names are kept as-is and flagged In 6-9 Master DB = No.',
    'MATCHING WATERFALL (RTB opp → won opp, searched across FY2025+FY2026 exports): exact name → name containment within account → account-code prefix + close date (±45d) → fuzzy within account.',
    'MATCHING WATERFALL (AI_SOWs, which has no key column): SOW doc title ↔ opportunity-name containment → account-code prefix in title (e.g. GALLO, PALO) → distinctive account-name word in title. PALO/PANW were manually mapped to Palo Alto Networks.',
    '',
    'KNOWN LIMITATIONS',
    '- RTB opp matching now covers both FY2025 and FY2026 won exports.',
    '- AI_SOWs tab has no key column; account links were inferred from SOW document titles and are marked with their method. Regenerating that extract with Salesforce Opportunity ID is the durable fix.',
    '- RevOps pipeline is a June 9 snapshot vs a July 13 won export; treat pipeline-vs-won comparisons as ~5 weeks apart.',
    '- Fees are as-exported ("converted" currency fields); no restatement applied.',
]})

# ================================================= 9b. capital attribution (K)
# Prices the production-function capital term  K = labor + tokens  and attributes
# it to people, opportunities, accounts, and practices.
#
#   labor $ = rate(grade) x utilization x weekly_capacity_hours   (util x capacity
#             is the hours proxy, per direction — replace with hours actuals later)
#   token $ = credits x credit_price
#
# ATTRIBUTION runs in APPROXIMATE mode today: a person's weekly capital is spread
# across the opportunities they staff (via Pursuit Team -> roster join), fee-weighted.
# It flips to EXACT automatically when the token feed carries a charge_code / project_id
# that joins straight to an opportunity (see load_token_feed()).
import os

CREDIT_PRICE = 0.05     # $/credit, blended from the four exec-summary overage figures
CAPACITY_HRS = 40       # standard weekly billable capacity; labor hours = util x capacity
DEFAULT_UTIL = 1.0      # assumed when a token-feed row lacks utilization
DEFAULT_RATE = 250      # used when grade is unknown (e.g. contractors)
# grade (roster HierarchyLevel) -> $/hr, from the WM rate card IC/Manager ladder
# (Junior 174 / Base 205 / Senior 257 / Expert 325 / Principal 405; Mgr & MD bands to 493).
# Practice does not change the rate in the provided card, so grade is the sole per-person key.
GRADE_TO_RATE = {0: 174, 1: 174, 2: 205, 3: 257, 4: 325, 5: 405, 6: 405, 7: 436, 8: 436, 9: 493, 10: 493}

ROSTER_CSV = os.environ.get('WM_ROSTER_CSV',
    '/tmp/claude-0/-home-user-hello-world/94fd7f02-ada3-55ab-8e58-2936eee13e0f/scratchpad/'
    'poweruser/All people with power user status - monthly/Power Users - July 12.csv')
TOKEN_FEED_CSV = os.environ.get('WM_TOKEN_FEED', '')   # full Codex export; blank -> sample below

# Top-5-per-week leaderboard from the four exec summaries (5/24-6/20/2026).
# Replace by pointing WM_TOKEN_FEED at the full export (all users x credits x utilization,
# ideally + charge_code). Columns beyond name/credits/utilization are optional.
TOKEN_FEED_SAMPLE = [
    {'name': 'Mark Davisson',       'credits': 209500, 'utilization': 0.00},
    {'name': 'Andy Reising',        'credits':  90100, 'utilization': 1.88},
    {'name': 'Ryan MacCarthy',      'credits':  54700, 'utilization': 1.02},
    {'name': 'Aaron Blanchard',     'credits':  52600, 'utilization': 1.06},
    {'name': 'Nate Lipp',           'credits':  43100, 'utilization': 1.00},
    {'name': 'Sam Atkinson',        'credits':  60000, 'utilization': None},
    {'name': 'Kevin Dolan',         'credits':  50000, 'utilization': None},
    {'name': 'Nate Bunnyfield',     'credits':  33000, 'utilization': None},
    {'name': 'Taimoor Qureshi',     'credits':  29000, 'utilization': None},
    {'name': 'Chris Webb',          'credits':  43000, 'utilization': None},
    {'name': 'Yeh-Sun Lee',         'credits':  50000, 'utilization': None},
    {'name': 'Herve Jean-Baptiste', 'credits':  33000, 'utilization': None},
    {'name': 'Jonnathan Carpentier','credits':  56000, 'utilization': None},
]

def _name_key(s):
    """Order-independent person key: sorted alpha tokens (handles 'Last, First')."""
    toks = [t for t in re.findall(r'[a-z]+', str(s).lower()) if len(t) > 1]
    return ' '.join(sorted(toks))

def rate_for_grade(g):
    try:
        return GRADE_TO_RATE.get(int(float(g)), DEFAULT_RATE)
    except (ValueError, TypeError):
        return DEFAULT_RATE

def load_token_feed():
    """Return (DataFrame, mode). mode='exact' when a per-opportunity key is present."""
    if TOKEN_FEED_CSV and os.path.exists(TOKEN_FEED_CSV):
        tf = pd.read_csv(TOKEN_FEED_CSV)
        keycols = {'charge_code', 'project_id', 'opportunity_id', 'opp_id'}
        mode = 'exact' if {c.lower() for c in tf.columns} & keycols else 'approx'
        return tf, mode
    return pd.DataFrame(TOKEN_FEED_SAMPLE), 'approx'

def load_roster(path):
    try:
        r = pd.read_csv(path)
    except Exception as e:                       # roster is optional; base build still runs
        print(f'NOTE: roster not loaded ({e}); capital practice rollup skipped.')
        return pd.DataFrame()
    r['_key'] = r['FullName'].map(_name_key)
    for c in ['total_interactions', 'total_hours_saved']:
        if c in r.columns:
            r[c] = pd.to_numeric(r[c], errors='coerce').fillna(0)
    return r

token_feed, ATTR_MODE = load_token_feed()
roster = load_roster(ROSTER_CSV)
roster_by_key = {}
for _, rr in roster.iterrows():
    roster_by_key.setdefault(rr['_key'], rr)
_rkeys = list(roster_by_key)

# person keys present on each opportunity's pursuit team
def _pt_keys(pt):
    keys = set()
    if pd.notna(pt):
        for part in re.split(r'[;,/|]| and ', str(pt)):
            k = _name_key(part)
            if len(k.split()) >= 2:
                keys.add(k)
    return keys
fact['_pt'] = fact['Pursuit Team'].map(_pt_keys)
_all_pt = set().union(*fact['_pt']) if len(fact) else set()

def match_pt_key(k):
    """Resolve a token-feed person to a pursuit-team key (exact then fuzzy)."""
    if k in _all_pt:
        return k
    m = difflib.get_close_matches(k, list(_all_pt), n=1, cutoff=0.90)
    return m[0] if m else None

def match_roster(k):
    if k in roster_by_key:
        return roster_by_key[k]
    m = difflib.get_close_matches(k, _rkeys, n=1, cutoff=0.90)
    return roster_by_key[m[0]] if m else None

# --- per-person capital + portfolio (grain: token-feed person) -----------------
_fees = pd.to_numeric(fact['Fees (converted)'], errors='coerce').fillna(0)
people_rows, opp_alloc = [], {}     # opp_alloc: fact index -> [labor$, token$]
for row in token_feed.to_dict('records'):
    name = row.get('name') or row.get('FullName') or row.get('email') or ''
    credits = float(row.get('credits') or row.get('total_credits') or 0)
    util = row.get('utilization')
    util = DEFAULT_UTIL if util is None or (isinstance(util, float) and pd.isna(util)) else float(util)
    k = _name_key(name)
    rinfo = match_roster(k)
    grade = rinfo['HierarchyLevel'] if rinfo is not None else None
    practice = rinfo['PracticeName_Clean'] if rinfo is not None else None
    rate = rate_for_grade(grade)
    labor = rate * util * CAPACITY_HRS
    token = credits * CREDIT_PRICE
    total = labor + token
    # portfolio via pursuit team
    pk = match_pt_key(k)
    port_mask = fact['_pt'].map(lambda s: pk in s) if pk else pd.Series(False, index=fact.index)
    port = fact[port_mask]
    port_fees = _fees[port_mask]
    n_opp = int(len(port))
    mode = 'formation' if (n_opp == 0 or util == 0) else 'deployment'
    # spread this week's capital across the portfolio, fee-weighted (equal if no fees)
    if ATTR_MODE == 'exact' and row.get('charge_code'):
        hit = fact.index[fact['Opportunity Name'].map(norm) == norm(row.get('charge_code'))]
        for i in hit:
            a = opp_alloc.setdefault(i, [0.0, 0.0]); a[0] += labor; a[1] += token
    elif n_opp:
        w = port_fees / port_fees.sum() if port_fees.sum() > 0 else pd.Series(1 / n_opp, index=port.index)
        for i in port.index:
            a = opp_alloc.setdefault(i, [0.0, 0.0]); a[0] += labor * w[i]; a[1] += token * w[i]
    people_rows.append({
        'Person': name, 'Grade': grade, 'Practice': practice, 'Rate ($/hr)': rate,
        'Weekly Credits': int(credits), 'Utilization': util,
        'Labor Capital ($/wk)': round(labor), 'Token Capital ($/wk)': round(token),
        'Total Capital ($/wk)': round(total), 'Token Share': round(token / total, 3) if total else None,
        'Mode': mode, 'Portfolio Opps': n_opp, 'Portfolio Accounts': int(port['Master Account'].nunique()),
        'Portfolio Fees': round(port_fees.sum()),
        'AI-Leveraged Opps': int((port['AI-Leveraged (opp evidence)'] == 'Yes').sum()),
        'GTM $ per Capital $': round(port_fees.sum() / total, 1) if total else None})
cap_people = pd.DataFrame(people_rows).sort_values('Total Capital ($/wk)', ascending=False).reset_index(drop=True)

# --- per-opportunity allocated capital (portfolio-spread) ----------------------
if opp_alloc:
    ao = pd.DataFrame([{'_i': i, 'Allocated Labor ($/wk)': round(v[0]),
                        'Allocated Token ($/wk)': round(v[1]),
                        'Allocated Capital ($/wk)': round(v[0] + v[1])} for i, v in opp_alloc.items()])
    cap_opp = (fact.loc[ao['_i'], ['Opportunity Name', 'Master Account', 'Status', 'Practice',
                                   'Fees (converted)', 'AI-Leveraged (opp evidence)']]
               .reset_index(drop=True).join(ao.drop(columns='_i').reset_index(drop=True)))
    cap_opp['Attribution Mode'] = ATTR_MODE
    cap_opp = cap_opp.sort_values('Allocated Capital ($/wk)', ascending=False).reset_index(drop=True)
else:
    cap_opp = pd.DataFrame()

# --- per-account allocated capital vs growth -----------------------------------
if opp_alloc:
    tmp = fact.loc[list(opp_alloc), ['Master Account']].copy()
    tmp['cap'] = [opp_alloc[i][0] + opp_alloc[i][1] for i in tmp.index]
    acct_cap = tmp.groupby('Master Account', as_index=False)['cap'].sum().rename(
        columns={'cap': 'Allocated Capital ($/wk)'})
    g = master[['Account Name', '2026 YTD Net Gen Revenue', '2025 Net Gen Fees',
                'Total 2026 Open Pipeline']].copy()
    for c in g.columns[1:]:
        g[c] = pd.to_numeric(g[c], errors='coerce')
    g['Net-Gen Growth ($)'] = g['2026 YTD Net Gen Revenue'].fillna(0) - g['2025 Net Gen Fees'].fillna(0)
    cap_account = (acct_cap.merge(g, left_on='Master Account', right_on='Account Name', how='left')
                   .drop(columns='Account Name'))
    cap_account['Capital / 2026 Pipeline'] = (cap_account['Allocated Capital ($/wk)']
                                              / cap_account['Total 2026 Open Pipeline']).round(5)
    cap_account['Allocated Capital ($/wk)'] = cap_account['Allocated Capital ($/wk)'].round()
    cap_account = cap_account.sort_values('Allocated Capital ($/wk)', ascending=False).reset_index(drop=True)
else:
    cap_account = pd.DataFrame()

# --- per-practice: AI census + capital vs pipeline GTM -------------------------
if len(roster):
    pv = roster.copy()
    pv['_rate'] = pv['HierarchyLevel'].map(rate_for_grade)
    pv['_labcap'] = pv['_rate'] * CAPACITY_HRS      # full-week labor-capacity proxy
    grp = pv.groupby('PracticeName_Clean').agg(
        power_users=('_key', 'count'),
        interactions=('total_interactions', 'sum') if 'total_interactions' in pv else ('_key', 'size'),
        hours_saved=('total_hours_saved', 'sum') if 'total_hours_saved' in pv else ('_key', 'size'),
        labor_capacity_wk=('_labcap', 'sum')).reset_index()
    # token capital placed into each practice (from the token feed, via roster practice)
    tok_by_prac = (cap_people.dropna(subset=['Practice'])
                   .groupby('Practice')['Token Capital ($/wk)'].sum().rename('token_capital_wk'))
    # pipeline GTM by practice (only pipeline opps carry Practice today)
    _pf = pipe_fact.copy()
    _pf['_f'] = pd.to_numeric(_pf['Fees (converted)'], errors='coerce').fillna(0)
    pipe_by_prac = _pf.groupby('Practice')['_f'].sum().rename('pipeline_gtm')
    cap_practice = (grp.merge(tok_by_prac, left_on='PracticeName_Clean', right_index=True, how='left')
                       .merge(pipe_by_prac, left_on='PracticeName_Clean', right_index=True, how='left'))
    cap_practice[['token_capital_wk', 'pipeline_gtm']] = cap_practice[['token_capital_wk', 'pipeline_gtm']].fillna(0)
    cap_practice['pipeline_per_power_user'] = (cap_practice['pipeline_gtm']
                                               / cap_practice['power_users'].replace(0, np.nan)).round()
    cap_practice['pipeline_per_labor_$'] = (cap_practice['pipeline_gtm']
                                            / cap_practice['labor_capacity_wk'].replace(0, np.nan)).round(2)
    for c in ['interactions', 'hours_saved', 'labor_capacity_wk', 'token_capital_wk', 'pipeline_gtm']:
        cap_practice[c] = cap_practice[c].round().astype('Int64')
    cap_practice = cap_practice.rename(columns={
        'PracticeName_Clean': 'Practice', 'power_users': 'AI Power Users', 'interactions': 'Interactions',
        'hours_saved': 'Hours Saved', 'labor_capacity_wk': 'Labor Capacity ($/wk)',
        'token_capital_wk': 'Token Capital ($/wk)', 'pipeline_gtm': 'Pipeline GTM ($)',
        'pipeline_per_power_user': 'Pipeline $ / Power User', 'pipeline_per_labor_$': 'Pipeline $ / Labor $'
    }).sort_values('AI Power Users', ascending=False).reset_index(drop=True)
else:
    cap_practice = pd.DataFrame()

rate_card_ref = pd.DataFrame({
    'Grade (HierarchyLevel)': list(GRADE_TO_RATE), 'Rate ($/hr)': list(GRADE_TO_RATE.values()),
    'Rate-card band': ['Junior', 'Junior', 'Base', 'Senior', 'Expert', 'Principal/Mgr', 'Principal',
                       'Mgr/MD', 'Mgr/MD', 'MD', 'MD']})

# ------------------------------------------------------------------ 10. write
fact_out = fact.drop(columns='_pt')            # drop internal pursuit-key helper
with pd.ExcelWriter(OUT, engine='openpyxl') as xw:
    readme.to_excel(xw, sheet_name='README', index=False)
    dim.to_excel(xw, sheet_name='Accounts', index=False)
    fact_out.to_excel(xw, sheet_name='Opportunities', index=False)
    ai_evidence.to_excel(xw, sheet_name='AI Evidence', index=False)
    alias_df.to_excel(xw, sheet_name='Alias Map', index=False)
    review_df.to_excel(xw, sheet_name='Review Queue', index=False)
    # capital attribution sheets (skip any that are empty for lack of input data)
    for df_cap, sheet in [(cap_people, 'Capital - People'), (cap_opp, 'Capital - Opportunity'),
                          (cap_account, 'Capital - Account'), (cap_practice, 'Capital - Practice'),
                          (rate_card_ref, 'Rate Card Ref')]:
        if len(df_cap):
            df_cap.to_excel(xw, sheet_name=sheet, index=False)

# ------------------------------------------------------------------ summary
print('=== BUILD SUMMARY ===')
print(f'Accounts: {len(dim)} (deduped from {1054})')
print(f'Opportunities: {len(fact)} = {len(won25_fact)} won-2025 + {len(won_fact)} won-2026 + {len(pipe_fact)} pipeline')
print(f'  Won opps linked to master account: {won_fact["Master Account"].notna().sum()}/{len(won_fact)}')
print(f'  Pipeline opps linked: {pipe_fact["Master Account"].notna().sum()}/{len(pipe_fact)}')
print(f'  Converted since snapshot: {(fact["Converted Since Snapshot"]=="Yes").sum()}')
print(f'AI evidence rows: {len(ai_evidence)}')
print(f'  RTB with account link: {rtb["Master Account"].notna().sum()}/{len(rtb)}')
print(f'  RTB matched to a won opp: {rtb["Matched Won Opp"].notna().sum()}/{len(rtb)} (FY split: {rtb["Matched FY"].value_counts().to_dict()})')
print('  RTB match methods:', rtb['Opp Match Method'].value_counts().to_dict())
print(f'  AI_SOWs with account guess: {ai_sows["Guessed Master Account"].notna().sum()}/{len(ai_sows)}')
print(f'Alias map rows: {len(alias_df)} | methods: {alias_df["Method"].value_counts().to_dict()}')
print(f'Review queue: {len(review_df)} | Crosswalk rows: {len(crosswalk_df)}')
print(f'Accounts flagged AI-leveraged: {(dim["Has AI-Leveraged Work"]=="Yes").sum()}')
won_ai_fees = fact.loc[(fact['Status']=='Won') & (fact['AI-Leveraged (opp evidence)']=='Yes'), 'Fees (converted)'].sum()
won_acct_ai_fees = fact.loc[(fact['Status']=='Won') & (fact['Account Has AI Evidence']=='Yes'), 'Fees (converted)'].sum()
print(f'FY2026 won fees on AI-matched opps: ${won_ai_fees:,.0f}')
print(f'FY2026 won fees at accounts with AI evidence: ${won_acct_ai_fees:,.0f} of ${fact.loc[fact["Status"]=="Won","Fees (converted)"].sum():,.0f}')
print('--- capital attribution ---')
print(f'Attribution mode: {ATTR_MODE.upper()} (token feed: '
      f'{"full export "+TOKEN_FEED_CSV if TOKEN_FEED_CSV else "leaderboard sample, "+str(len(token_feed))+" people"})')
if len(cap_people):
    _dep = cap_people[cap_people['Mode'] == 'deployment']['Total Capital ($/wk)'].sum()
    _form = cap_people[cap_people['Mode'] == 'formation']['Total Capital ($/wk)'].sum()
    _tot = _dep + _form
    print(f'  People priced: {len(cap_people)} | roster-matched grade: '
          f'{cap_people["Grade"].notna().sum()}/{len(cap_people)}')
    print(f'  Capital split: formation ${_form:,.0f}/wk ({_form/_tot*100:.0f}%) vs '
          f'deployment ${_dep:,.0f}/wk | token share {cap_people["Token Capital ($/wk)"].sum()/_tot*100:.0f}%')
    print(f'  People mapped to >=1 opp: {(cap_people["Portfolio Opps"]>0).sum()}/{len(cap_people)}')
print(f'  Opportunities allocated capital: {len(cap_opp)} | accounts: {len(cap_account)} | '
      f'practices rolled up: {len(cap_practice)}')
