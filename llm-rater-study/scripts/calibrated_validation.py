#!/usr/bin/env python3
"""Calibrated robustness and convergent checks for the U-Space DREAD-S catalogue.

Inputs (relative to the repository root): ratings.csv, edges.csv,
llm-rater-study/raw_responses/llm_{a..g}_run{1..3}.json  (21 LLM runs).
Output: llm-rater-study/results/calibrated_validation.md (all numbers quoted in the paper).
Usage:  python3 llm-rater-study/scripts/calibrated_validation.py      (needs numpy scipy networkx)
All random draws use fixed seeds.
"""
import csv, glob, json, os, re, sys
import numpy as np, networkx as nx
from scipy.stats import kendalltau, spearmanr, rankdata, chi2

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
rows = list(csv.DictReader(open(os.path.join(ROOT, 'ratings.csv'))))
ids = [r['id'] for r in rows]; dims = ['D', 'R', 'E', 'A', 'D2', 'S']
pub = np.array([[int(r[k]) for k in dims] for r in rows], float)
raw = np.zeros((7, 3, 21, 6))
for f in glob.glob(os.path.join(ROOT, 'llm-rater-study', 'raw_responses', 'llm_*_run*.json')):
    m = re.search(r'llm_([a-g])_run(\d)', f)
    for e in json.load(open(f)):
        raw[ord(m.group(1)) - 97, int(m.group(2)) - 1, ids.index(e['id'])] = [e[d] for d in dims]
assert (raw > 0).all(), 'missing LLM ratings'
nu = lambda x: 1 + 4 * (np.asarray(x, float) - 1) / 9
ds = lambda a, w=1 / 6: (1 - w) / 5 * nu(a[..., :5]).sum(-1) + w * a[..., 5]
band = lambda v: np.select([v <= 1.8 + 1e-9, v <= 2.6 + 1e-9, v <= 3.4 + 1e-9, v <= 4.2 + 1e-9], [0, 1, 2, 3], 4)
base = ds(pub); bb = band(base); flat = raw.reshape(21, 21, 6); pool = np.concatenate([flat, pub[None]], 0)
top7 = set(np.argsort(-base)[:7]); i02 = ids.index('INF-02'); N = 20000
out = []
def P(s=''): print(s); out.append(s)

def summarize(draws):
    t, b, t7, gv, fi, t3 = [], [], [], [], [], []; rk = np.zeros((len(draws), 21)); bc = np.zeros((21, 5))
    for n, s in enumerate(draws):
        o = np.argsort(-s); t.append(kendalltau(base, s)[0]); b.append((band(s) != bb).sum())
        t7.append(len(top7 & set(o[:7])) / 7); gv.append(len({0, 1, 2} & set(np.argsort(s)[:5])) / 3)
        fi.append(o[0] == i02); t3.append(i02 in o[:3]); bc[np.arange(21), band(s)] += 1; rk[n] = np.argsort(np.argsort(-s)) + 1
    return dict(tau=np.mean(t), bands=np.mean(b), top7=np.mean(t7), gov=np.mean(gv), first=np.mean(fi), top3=np.mean(t3)), bc / len(draws), rk

P('# Calibrated validation results\n')
P('## 1. Rating perturbation: paper scheme vs disagreement observed between raters')
rng = np.random.default_rng(11)
d1 = [ds(np.column_stack([np.clip(pub[:, :5] + rng.choice([-1, 0, 1], size=(21, 5), p=[.25, .5, .25]), 1, 10), pub[:, 5]])) for _ in range(N)]
rng = np.random.default_rng(7)
ar = np.arange(21)
d2 = [ds(pool[rng.integers(0, 22, size=(21, 6)), ar[:, None], np.arange(6)[None, :]]) for _ in range(N)]
d3 = [ds(pool[rng.integers(0, 22)]) for _ in range(N)]
res = {}
for lbl, d in (('pm1', d1), ('pool_independent', d2), ('one_rater', d3)):
    res[lbl] = summarize(d); r = res[lbl][0]
    P(f"{lbl}: tau={r['tau']:.2f} bands_changed={r['bands']:.1f} top7={r['top7']:.2f} INF-02_first={r['first']:.2f} INF-02_top3={r['top3']:.2f} gov_in_lowest5={r['gov']:.2f}")
rk = res['pool_independent'][2]; bc = res['pool_independent'][1]; p11 = (rk <= 11).mean(0)
P('\nTier membership (independent rater-pool draws): P(asset in top 11 of 21)')
for i in np.argsort(-p11): P(f"  {ids[i]} published {base[i]:.2f} rank {int((base > base[i]).sum() + 1)}  P(top11)={p11[i]:.2f}  P(keeps published band)={bc[i, bb[i]]:.2f}")
hi = [ids[i] for i in np.argsort(-p11) if p11[i] >= .8]; lo = [ids[i] for i in np.argsort(p11) if p11[i] <= .2]; mid = [ids[i] for i in range(21) if .2 < p11[i] < .8]
P(f'stable upper tier (>=0.8): {len(hi)} {hi}\nstable lower tier (<=0.2): {len(lo)} {lo}\nuncertain: {len(mid)} {mid}')
pub_top11 = set(ids[i] for i in np.argsort(-base)[:11]); P('published top 11: ' + str(sorted(pub_top11)))
agree = [ids[i] for i in range(21) if (ids[i] in pub_top11 and p11[i] >= .8) or (ids[i] not in pub_top11 and p11[i] <= .2)]
contra = [ids[i] for i in range(21) if (ids[i] in pub_top11 and p11[i] <= .2) or (ids[i] not in pub_top11 and p11[i] >= .8)]
unc = [ids[i] for i in range(21) if ids[i] not in agree and ids[i] not in contra]
P(f'published side of the top-11 cut reproduced in >=80% of draws: {len(agree)} {agree}\ncontradicted in >=80% of draws: {len(contra)} {contra}\nuncertain: {len(unc)} {unc}')
tc = np.mean([sum(1 for i in range(21) if (rk[n, i] <= 11) == (ids[i] in pub_top11)) / 21 for n in range(0, N, 10)]); P(f'mean share of assets on the same side of the top-11 cut as the published ranking: {tc:.2f}')

P('\n## 2. Agreement of the published ratings with the LLM panel')
mm = raw.mean(1); cons = mm.mean(0); dc = ds(cons)
P(f"consensus (mean of 7 models) vs published: tau={kendalltau(base, dc)[0]:.2f} rho={spearmanr(base, dc)[0]:.2f}  top11 overlap={len(set(np.argsort(-base)[:11]) & set(np.argsort(-dc)[:11])) / 11:.2f}")
raters = [base] + [ds(mm[m]) for m in range(7)]
loo = []
for i in range(8): loo.append(kendalltau(raters[i], np.mean([raters[j] for j in range(8) if j != i], 0))[0])
P('leave-one-out tau with the mean of the other raters: published %.2f; LLM models %.2f-%.2f' % (loo[0], min(loo[1:]), max(loo[1:])))
P('per-dimension Spearman rho, published vs consensus: ' + ', '.join(f'{d} {spearmanr(pub[:, j], cons[:, j])[0]:.2f}' for j, d in enumerate(dims)))
def kalpha(Mx):
    m, n = Mx.shape; do = sum(((Mx[:, u][:, None] - Mx[:, u][None, :]) ** 2).sum() / (m - 1) for u in range(n)) / (m * n)
    v = Mx.flatten(); Nn = m * n; return 1 - do / (((v[:, None] - v[None, :]) ** 2).sum() / (Nn * (Nn - 1)))
P('Krippendorff alpha with published as 8th rater (model means): ' + ', '.join(f'{d} {kalpha(np.vstack([mm[:, :, j], pub[:, j]])):.2f}' for j, d in enumerate(dims)))
def agg_drop(a, j): v = np.concatenate([nu(a[:, :5]), a[:, 5:6]], 1); return np.delete(v, j, 1).sum(1)
P('dropping D2: tau(published, consensus) %.2f -> %.2f' % (kendalltau(base, dc)[0], kendalltau(agg_drop(pub, 4), agg_drop(cons, 4))[0]))


def kendall_w(Sc):
    """Kendall's W (tie-corrected) for raters x items scores, and its chi-square p-value."""
    m, n = Sc.shape; Rk = np.array([rankdata(r) for r in Sc]); Rj = Rk.sum(0); ss = ((Rj - Rj.mean()) ** 2).sum()
    T = sum(((c ** 3 - c).sum()) for c in (np.unique(r, return_counts=True)[1] for r in Sc))
    w = 12 * ss / (m ** 2 * (n ** 3 - n) - m * T); return w, chi2.sf(m * (n - 1) * w, n - 1)
scr = ds(raw)
w7, p7 = kendall_w(ds(raw.mean(1))); w21, p21 = kendall_w(scr.reshape(21, 21)); w8, _ = kendall_w(np.vstack([base, ds(raw.mean(1))]))
P(f"Kendall's W of the DREAD-S rankings: 7 models (mean of runs) {w7:.2f} (p={p7:.1e}); all 21 runs {w21:.2f} (p={p21:.1e}); 7 models plus published as 8th rater {w8:.2f}")
P("Kendall's W per model over its 3 runs: " + ', '.join(f"{'ABCDEFG'[m]} {kendall_w(scr[m])[0]:.2f}" for m in range(7)))


P('\nKrippendorff alpha vs Kendall W, same raters (DREAD-S, then Exploitability and Discoverability):')
def cases(f, pubv):
    mmv = f(raw.mean(1)); sc = f(raw); allr = sc.reshape(21, 21)
    w = [(kalpha(sc[m]), kendall_w(sc[m])[0]) for m in range(7)]
    return {'within a model (range over 7)': (f"{min(x[0] for x in w):.2f}-{max(x[0] for x in w):.2f}", f"{min(x[1] for x in w):.2f}-{max(x[1] for x in w):.2f}"),
            '7 models': (f'{kalpha(mmv):.2f}', f'{kendall_w(mmv)[0]:.2f}'), 'all 21 runs': (f'{kalpha(allr):.2f}', f'{kendall_w(allr)[0]:.2f}'),
            '7 models + published': (f'{kalpha(np.vstack([mmv, pubv])):.2f}', f'{kendall_w(np.vstack([mmv, pubv]))[0]:.2f}')}
for lbl, f, pv in (('DREAD-S', ds, base), ('E', lambda a: a[..., 2], pub[:, 2]), ('D2', lambda a: a[..., 4], pub[:, 4])):
    for k, (a, w) in cases(f, pv).items(): P(f'  {lbl:8s} {k:30s} alpha {a:10s} W {w}')

P('\n## 3. Alternative aggregation schemes on the published ratings (vs Eq. 1)')
S = pub[:, 5]; L = nu(pub[:, :5]).mean(1); Lk = nu(pub[:, [1, 2, 4]]).mean(1); Im = (nu(pub[:, [0, 3]]).mean(1) + S) / 2
z = lambda a: (a - a.mean(0)) / a.std(0); u, s_, vt = np.linalg.svd(z(pub), full_matrices=False); pc = u[:, 0] * s_[0]; pc = pc if np.corrcoef(pc, base)[0, 1] > 0 else -pc
lv = np.clip(np.rint(pub[:, :5].mean(1) / 2), 1, 5)
schemes = {'S only': S, 'mean of five nu (no S)': L, 'L x I (L=R,E,D2; I=D,A,S)': Lk * Im, 'mean five nu x S': L * S, 'max': np.maximum(nu(pub[:, :5]).max(1), S * 0.9 * 2),
           'ordinal 5x5 matrix': lv * S, 'z-score mean': z(pub).mean(1), 'PC1': pc}
for k, v in schemes.items(): P(f"  {k:28s} tau={kendalltau(base, v)[0]:.2f} rho={spearmanr(base, v)[0]:.2f} top7={len(top7 & set(np.argsort(-v)[:7])) / 7:.2f}")
P('  PC1 explains %.0f%% of variance' % (100 * s_[0] ** 2 / (s_ ** 2).sum()))

P('\n## 4. Propagation graph: structure vs score, and edge noise')
ed = [(e['source'], e['target']) for e in csv.DictReader(open(os.path.join(ROOT, 'edges.csv')))]
nodes = sorted({x for e in ed for x in e}); cat = [n for n in nodes if pub[ids.index(n), 5] >= 5]
G0 = nx.DiGraph(); G0.add_nodes_from(ids); G0.add_edges_from(ed); reach = np.array([len(nx.descendants(G0, n)) for n in ids]); outd = np.array([G0.out_degree(n) for n in ids])
P('Spearman rho of DREAD-S with downstream reach %.2f, with out-degree %.2f' % (spearmanr(base, reach)[0], spearmanr(base, outd)[0]))
def met(edges):
    G = nx.DiGraph(); G.add_nodes_from(nodes); G.add_edges_from(edges); sc = sorted([c for c in nx.strongly_connected_components(G) if len(c) > 1], key=len, reverse=True); core = sc[0] if sc else set()
    two = sum(1 for n in nodes if n not in cat and any(c in nx.single_source_shortest_path_length(G, n, cutoff=2) for c in cat)); return core, two
core0 = met(ed)[0]; P('baseline core %d, within two hops of a catastrophic asset: %d of %d' % (len(core0), met(ed)[1], len(nodes) - len(cat)))
non = [(a, c) for a in nodes for c in nodes if a != c and (a, c) not in set(ed)]; rng = np.random.default_rng(3); M = 5000
for p in (0.1, 0.2, 0.3):
    for rew in (False, True):
        cs, both, tw, kept = [], [], [], []
        for _ in range(M):
            keep = [e for e in ed if rng.random() > p]
            if rew: keep += [non[i] for i in rng.choice(len(non), len(ed) - len(keep), replace=False)]
            core, two = met(keep); cs.append(len(core)); both.append({'SVC-03', 'DAT-02'} <= core); tw.append(two); kept.append(len(core & core0) / 8)
        P(f"  p={p} {'rewire' if rew else 'delete'}: core size mean {np.mean(cs):.1f}, P(core>=6)={np.mean(np.array(cs) >= 6):.2f}, core members kept {np.mean(kept):.2f}, SVC-03 and DAT-02 both in core {np.mean(both):.2f}, mean assets within 2 hops {np.mean(tw):.1f} of {len(nodes) - len(cat)}")
open(os.path.join(ROOT, 'llm-rater-study', 'results', 'calibrated_validation.md'), 'w').write('\n'.join(out) + '\n')
