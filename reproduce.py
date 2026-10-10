#!/usr/bin/env python3
"""Recompute the quantitative results of the accompanying U-Space threat-model paper.

Inputs : ratings.csv (21 catalogue entries: raw ratings D,R,E,A,D2, Safety Impact S)
         edges.csv   (45 propagation edges with mechanism, basis, resolution rule)
Outputs: printed results (scores, bands, graph structure, chains, cuts, sensitivity)
         and self-checks against the values reported in the paper.
Requires: Python 3.9+, numpy, scipy, networkx.   Usage: python3 reproduce.py
"""
import csv, sys
from collections import Counter
import numpy as np, networkx as nx
from scipy.stats import kendalltau

SYSTEMIC = {"GOV-02", "INF-07"}           # declare reach into all layers; not graph nodes
CATASTROPHIC = ["SVC-03", "DAT-02"]       # S = 5 assets inside the graph
BANDS = [(1.8, "Minimal"), (2.6, "Low"), (3.4, "Medium"), (4.2, "High")]

def nu(x): return 1 + 4 * (np.asarray(x, float) - 1) / 9          # rescale 1-10 -> 1-5
def dreads(d, s, w_s=1 / 6):                                      # Eq. 1 (w_s = 1/6)
    return (1 - w_s) / 5 * nu(d).sum(-1) + w_s * s
def band(v):
    return next((b for t, b in BANDS if v <= t), "Critical")
def band_idx(v):
    return np.select([v <= t for t, _ in BANDS], range(4), 4)

rows = list(csv.DictReader(open("ratings.csv")))
ids = [r["id"] for r in rows]
D = np.array([[r[k] for k in ("D", "R", "E", "A", "D2")] for r in rows], float)
S = np.array([r["S"] for r in rows], float)
base = dreads(D, S)
S_of = dict(zip(ids, S))
edges = [(r["source"], r["target"], r["mechanism"]) for r in csv.DictReader(open("edges.csv"))]

check = []
def ck(name, got, want):
    ok = got == want; check.append(ok)
    print(f"  [{'ok' if ok else 'MISMATCH'}] {name}: {got}" + ("" if ok else f" (paper: {want})"))

print("== Scoring (Eq. 1) ==")
b = Counter(band(v) for v in base)
for i, v in sorted(zip(ids, base), key=lambda x: -x[1]): print(f"  {i}  {v:.2f}  {band(v)}")
ck("bands", dict(b), {"Critical": 2, "High": 14, "Medium": 5})

print("== Propagation graph ==")
G = nx.DiGraph(); G.add_nodes_from(i for i in ids if i not in SYSTEMIC)
G.add_edges_from((s, t) for s, t, _ in edges)
ck("nodes / edges", (G.number_of_nodes(), G.number_of_edges()), (19, 45))
core = max(nx.strongly_connected_components(G), key=len)
ck("core size", len(core), 8); print("  core:", sorted(core))
d5 = {}; s1 = {}; reach = {}
for u in G:
    dist = nx.single_source_shortest_path_length(G, u)
    d5[u] = min([h for v, h in dist.items() if v in CATASTROPHIC and v != u] + [99])
    s1[u] = max([S_of[u]] + [S_of[v] for v, h in dist.items() if h == 1])
    reach[u] = len(dist) - 1
ck("max hops to a catastrophic asset", max(d5.values()), 2)
ck("assets one hop away", sum(h == 1 for h in d5.values()), 13)
ck("reach min/max", (min(reach.values()), max(reach.values())), (7, 10))
adj = {u: dreads(D[ids.index(u)], s1[u]) for u in G}
chg = sorted(u for u in G if band(adj[u]) != band(base[ids.index(u)]))
ck("assets changing band under DREAD-S1", len(chg), 5); print("  ", chg)

print("== Chains and gates ==")
entries = [u for u in G if u.startswith("INF")]
def chains(src, dst, maxh=4):
    out = []
    def dfs(p):
        if len(p) - 1 > maxh: return
        if p[-1] == dst and len(p) > 1: out.append(p[:]); return
        for n in G[p[-1]]:
            if n not in p: p.append(n); dfs(p); p.pop()
    dfs([src]); return out
allc = [p for u in entries for t in CATASTROPHIC for p in chains(u, t)]
ck("chains from infrastructure entries", len(allc), 43)
ck("chains through the SSOT (DAT-02)", sum("DAT-02" in p for p in allc), 36)
H = G.copy(); H.add_node("SRC"); H.add_edges_from(("SRC", u) for u in entries)
ck("vertex cut to SVC-03", sorted(nx.minimum_node_cut(H, "SRC", "SVC-03")), ["DAT-02", "INF-01", "INF-02", "SVC-04"])
ck("writers of DAT-02", sorted(G.predecessors("DAT-02")), ["INF-02", "INF-03", "INF-05", "SVC-01", "SVC-02", "SVC-03"])
keep = 0
for s, t, _ in edges:
    X = G.copy(); X.remove_edge(s, t)
    keep += len(max(nx.strongly_connected_components(X), key=len)) == len(core)
ck("single-edge removals that keep the core", keep, 40)
named = nx.DiGraph(); named.add_nodes_from(G)
rule = {(r["source"], r["target"]): r["basis"] for r in csv.DictReader(open("edges.csv"))}
named.add_edges_from(e for e, b_ in rule.items() if b_ != "Mapped by rule")
ck("edges without rule resolution", named.number_of_edges(), 12)
ck("core exists without rules", len(max(nx.strongly_connected_components(named), key=len)) > 1, False)

print("== Sensitivity (Section 8.4; 20,000 draws, fixed seeds) ==")
N = 20000; bb = band_idx(base); top7 = set(np.argsort(-base)[:7]); gov = {0, 1, 2}
for name, noise_s, seed in (("ratings +-1", False, 11), ("ratings +-1, S +-1", True, 11)):
    rng = np.random.default_rng(seed); tau = []; bc = []; ov = []; first = 0; gb = []
    for _ in range(N):
        d = np.clip(D + rng.choice([-1, 0, 1], size=D.shape, p=[.25, .5, .25]), 1, 10)
        s = np.clip(S + rng.choice([-1, 0, 1], size=21, p=[.2, .6, .2]), 1, 5) if noise_s else S
        sc = dreads(d, s); o = np.argsort(-sc)
        tau.append(kendalltau(base, sc)[0]); bc.append((band_idx(sc) != bb).sum())
        ov.append(len(top7 & set(o[:7])) / 7); first += ids[o[0]] == "INF-02"
        gb.append(len(gov & set(np.argsort(sc)[:5])) / 3)
    print(f"  {name}: tau={np.mean(tau):.2f} bands={np.mean(bc):.1f} top7={np.mean(ov):.2f} "
          f"INF-02 first={first / N:.0%} gov in bottom5={np.mean(gb):.0%}")
for w in (1 / 12, 1 / 4, 1 / 3, 1 / 2):
    sc = dreads(D, S, w); o = np.argsort(-sc)
    print(f"  w_S={w:.3f}: tau={kendalltau(base, sc)[0]:.2f} bands={(band_idx(sc) != bb).sum()} "
          f"top7={len(top7 & set(o[:7])) / 7:.2f} INF-02 first={ids[o[0]] == 'INF-02'}")

print(f"\n{sum(check)}/{len(check)} self-checks passed")
sys.exit(0 if all(check) else 1)
