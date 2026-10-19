#!/usr/bin/env python3
"""Reliability analysis of LLM-rater runs against the published DREAD-S ratings.

Input : ../input/published_ratings.csv  (id,...,D,R,E,A,D2,S)
        ../ratings/ratings_all_runs.csv (id,model,run,D,R,E,A,D2,S)
Output: ../results/*.csv and ../results/summary.md
Usage : python3 analyze.py            (requires numpy, scipy)
Equation: DREAD-S = (sum_{x in D,R,E,A,D2} nu(x) + S)/6, nu(x)=1+4(x-1)/9.
Bands   : Minimal <=1.8, Low <=2.6, Medium <=3.4, High <=4.2, Critical >4.2.
"""
import csv, itertools, os, sys
import numpy as np
from scipy.stats import kendalltau

HERE = os.path.dirname(os.path.abspath(__file__))
DIMS = ['D', 'R', 'E', 'A', 'D2', 'S']
BANDS = ['Minimal', 'Low', 'Medium', 'High', 'Critical']
GOV = ('GOV-01', 'GOV-02', 'GOV-03')

pub_rows = list(csv.DictReader(open(os.path.join(HERE, '../input/published_ratings.csv'))))
ids = [r['id'] for r in pub_rows]
pub = np.array([[int(r[k]) for k in DIMS] for r in pub_rows], float)
raw = list(csv.DictReader(open(os.path.join(HERE, '../ratings/ratings_all_runs.csv'))))
models = list(dict.fromkeys(r['model'] for r in raw))
for _m in models:
    if len({r['run'] for r in raw if r['model'] == _m}) < 2: sys.exit(f'{_m}: at least 2 runs are needed for agreement statistics')
runs = {}
for m in models:
    rs = sorted({int(r['run']) for r in raw if r['model'] == m})
    runs[m] = np.array([[[float(next(x[k] for x in raw if x['id'] == i and x['model'] == m and int(x['run']) == n))
                          for k in DIMS] for i in ids] for n in rs])          # runs x entries x dims

nu = lambda x: 1 + 4 * (x - 1) / 9
ds = lambda a: (nu(a[:, :5]).sum(1) + a[:, 5]) / 6
band = lambda v: np.select([v <= 1.8, v <= 2.6, v <= 3.4, v <= 4.2], [0, 1, 2, 3], 4)
base = ds(pub); top7 = set(np.argsort(-base)[:7]); gov = {ids.index(g) for g in GOV}

def kalpha(M):                       # Krippendorff's alpha, interval scale, no missing values
    m, n = M.shape; vals = M.ravel(); do = 0.0
    for u in range(n):
        c = M[:, u]; do += ((c[:, None] - c[None, :]) ** 2).sum() / (m - 1)
    Do = do / (m * n); N = m * n
    De = ((vals[:, None] - vals[None, :]) ** 2).sum() / (N * (N - 1))
    return 1 - Do / De

def icc21(M):                        # ICC(2,1), raters x units
    k, n = M.shape; X = M.T; gm = X.mean()
    ssr = k * ((X.mean(1) - gm) ** 2).sum(); ssc = n * ((X.mean(0) - gm) ** 2).sum()
    sse = ((X - gm) ** 2).sum() - ssr - ssc
    msr, msc, mse = ssr / (n - 1), ssc / (k - 1), sse / ((n - 1) * (k - 1))
    return (msr - mse) / (msr + (k - 1) * mse + k * (msc - mse) / n)

def agreement(R):                    # R: runs x entries x dims -> list of rows
    out = []
    for j, nm in enumerate(DIMS):
        M = R[:, :, j]
        out.append([nm, kalpha(M), icc21(M), np.abs(M - pub[:, j]).mean(), (np.abs(M - pub[:, j]) <= 1).mean()])
    sc = np.array([ds(r) for r in R])
    out.append(['DREAD-S', kalpha(sc), icc21(sc), np.abs(sc - base).mean(),
                (np.array([band(s) for s in sc]) == band(base)).mean()])
    return out

def rank_row(label, s):
    o = np.argsort(-s)
    return [label, kendalltau(base, s)[0], int((band(s) != band(base)).sum()), int((band(s) > band(base)).sum()),
            len(top7 & set(o[:7])) / 7, ids[o[0]], o.tolist().index(ids.index('INF-02')) + 1,
            len(gov & set(np.argsort(s)[:5])) / 3, BANDS[band(s).max()]]

def fmt(x): return f'{x:.2f}' if isinstance(x, (float, np.floating)) else str(x)
def table(head, rows): return '| ' + ' | '.join(head) + ' |\n|' + '---|' * len(head) + '\n' + '\n'.join('| ' + ' | '.join(fmt(c) for c in r) + ' |' for r in rows) + '\n'

md = ['# LLM-rater study: computed results\n', f'Models: {", ".join(models)}\n',
      f'Published mean DREAD-S: {base.mean():.2f}\n']
os.makedirs(os.path.join(HERE, '../results'), exist_ok=True)
def save(name, head, rows):
    with open(os.path.join(HERE, '../results', name), 'w', newline='') as f:
        w = csv.writer(f); w.writerow(head); w.writerows([[fmt(c) for c in r] for r in rows])

allrows = []
for m in models:
    R = runs[m]; a = agreement(R)
    md += [f'\n## {m} (K={len(R)} runs)\n', table(['Dim', 'alpha', 'ICC(2,1)', 'MAD vs published', 'within +-1 (DREAD-S: same band)'], a)]
    allrows += [[m] + r for r in a]
    sc = np.array([ds(r) for r in R])
    inter = np.mean([np.abs(R[x][:, :5] - R[y][:, :5]).mean() for x, y in itertools.combinations(range(len(R)), 2)])
    md.append(f'\nRun-to-run MAD (5 DREAD ratings): {inter:.2f}; MAD vs published: five ratings '
              f'{np.abs(R[:, :, :5] - pub[:, :5]).mean():.2f}, S {np.abs(R[:, :, 5] - pub[:, 5]).mean():.2f}; '
              f'signed mean (LLM - published) D,R,E,A,D2,S = {np.round((R - pub).mean((0, 1)), 2).tolist()}; '
              f'mean DREAD-S {sc.mean():.2f}\n')
    rr = [rank_row(f'run {i + 1}', sc[i]) for i in range(len(R))] + [rank_row('median of runs', ds(np.median(R, 0)))]
    md += ['\n', table(['Rater', 'tau', 'bands changed', 'bands raised', 'top-7 overlap', 'first', 'INF-02 rank', 'gov in 5 lowest', 'highest band'], rr)]
    save(f'ranking_{m.split(" ")[1]}.csv', ['rater', 'tau', 'bands', 'raised', 'top7', 'first', 'inf02rank', 'gov', 'maxband'], rr)
save('agreement_per_model.csv', ['model', 'dim', 'alpha', 'icc', 'mad', 'within1'], allrows)

if len(models) > 1:
    P = np.concatenate([runs[m] for m in models]); a = agreement(P)
    md += [f'\n## All {len(P)} runs pooled\n', table(['Dim', 'alpha', 'ICC(2,1)', 'MAD vs published', 'within +-1'], a)]
    md += ['\n', table(['Rater', 'tau', 'bands changed', 'bands raised', 'top-7 overlap', 'first', 'INF-02 rank', 'gov in 5 lowest', 'highest band'],
                         [rank_row('median of all runs', ds(np.median(P, 0)))])]
    save('agreement_pooled.csv', ['dim', 'alpha', 'icc', 'mad', 'within1'], a)
    md.append('\n## Between-model agreement (means of each model\'s runs)\n')
    for x, y in itertools.combinations(models, 2):
        mx, my = runs[x].mean(0), runs[y].mean(0)
        rows = [[nm, np.corrcoef(mx[:, j], my[:, j])[0, 1], np.abs(mx[:, j] - my[:, j]).mean()] for j, nm in enumerate(DIMS)]
        rows.append(['DREAD-S tau', kendalltau(ds(mx), ds(my))[0], np.abs(ds(mx) - ds(my)).mean()])
        md += [f'\n{x} vs {y}\n', table(['Dim', 'Pearson r', 'MAD of run means'], rows)]
open(os.path.join(HERE, '../results/summary.md'), 'w').write(''.join(md))
print(''.join(md))

# ---- the three LLM tables of Section 8.5 of the paper ----------------------------------------------------------
def rng(vals, f):
    lo, hi = min(vals), max(vals); return f(lo) if f(lo) == f(hi) else f(lo) + '--' + f(hi)
ordn = lambda n: {1: '1st', 2: '2nd', 3: '3rd'}.get(n, f'{n}th')
P = np.concatenate([runs[m] for m in models]); sets = [(m.split(' (')[0], runs[m]) for m in models]
tb = ['# Tables of Section 8.5 (computed)\n', '\n## Table: alpha per dimension (columns: ' + ', '.join(n for n, _ in sets) + ', All)\n',
      '| Dimension | ' + ' | '.join(n.split()[-1] for n, _ in sets) + ' | All |\n|' + '---|' * (len(sets) + 2) + '\n']
for j, nm in enumerate(DIMS + ['DREAD-S']):
    cells = []
    for _, R in sets + [('All', P)]:
        X = R[:, :, j] if j < 6 else np.array([ds(r) for r in R]); cells.append(f'{kalpha(X):.2f}')
    tb.append(f'| {nm} | ' + ' | '.join(cells) + ' |\n')
tb.append('\n## Table: deviation from the published ratings\n\n| Rater | Runs MAD | DREAD MAD | DREAD within 1 | S MAD | S within 1 | Mean DREAD-S |\n|---|---|---|---|---|---|---|\n')
for n, R in sets + [('All runs', P)]:
    k = len(R); inter = np.mean([np.abs(R[x][:, :5] - R[y][:, :5]).mean() for x in range(k) for y in range(x + 1, k)])
    tb.append(f'| {n} | {inter:.2f} | {np.abs(R[:, :, :5] - pub[:, :5]).mean():.2f} | {(np.abs(R[:, :, :5] - pub[:, :5]) <= 1).mean():.0%} | '
              f'{np.abs(R[:, :, 5] - pub[:, 5]).mean():.2f} | {(np.abs(R[:, :, 5] - pub[:, 5]) <= 1).mean():.0%} | {np.mean([ds(r).mean() for r in R]):.2f} |\n')
tb.append(f'| Published | - | - | - | - | - | {base.mean():.2f} |\n')
tb.append('\n## Table: ranking stability (range over the runs of each model)\n\n| Rater | tau | Bands | Top-7 | INF-02 rank | Gov. | Runs with a Critical entry |\n|---|---|---|---|---|---|---|\n')
for n, R in sets:
    rr = [rank_row('', ds(r)) for r in R]
    tb.append(f'| {n} | {rng([r[1] for r in rr], lambda x: f"{x:.2f}")} | {rng([r[2] for r in rr], str)} | {rng([r[4] for r in rr], lambda x: f"{x:.2f}")} | '
              f'{rng([r[6] for r in rr], ordn)} | {rng([r[7] for r in rr], lambda x: f"{x:.0%}")} | {sum(r[8] == "Critical" for r in rr)}/{len(rr)} |\n')
r = rank_row('', ds(np.median(P, 0)))
tb.append(f'| Median of all {len(P)} runs | {r[1]:.2f} | {r[2]} | {r[4]:.2f} | {ordn(r[6])} | {r[7]:.0%} | {r[8]} |\n')
open(os.path.join(HERE, '../results/paper_tables.md'), 'w').write(''.join(tb))

