#!/usr/bin/env python3
"""Figures of the LLM-rater study (reproducible from ../ratings and ../input).

Writes ../figures/fig1_overview, fig2_where_models_disagree, fig3_models_vs_published (.pdf and .png)
and ../figures/data/*.csv (the numbers behind every panel, i.e. the table view of each chart).
Usage: python3 make_figures.py      (requires numpy, scipy, matplotlib)

Colour: categorical slots 1-6 of the validated reference palette (blue, orange, aqua, yellow, magenta, green)
identify the six LLMs in every panel; sequential = one blue ramp; diverging = blue <-> red around grey.
"""
import csv, itertools, os, sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager, colors as mcolors
from scipy.stats import kendalltau

HERE = os.path.dirname(os.path.abspath(__file__))
WITH_TITLES = '--titles' in sys.argv      # overall figure titles are off by default: in the paper the caption does that job
OUT = os.path.join(HERE, '../figures'); os.makedirs(os.path.join(OUT, 'data'), exist_ok=True)

# ---------------------------------------------------------------- data
DIMS = ['D', 'R', 'E', 'A', 'D2', 'S']
DIMN = {'D': 'Damage', 'R': 'Reproducibility', 'E': 'Exploitability', 'A': 'Affected assets', 'D2': 'Discoverability', 'S': 'Safety impact'}
BANDS = ['Minimal', 'Low', 'Medium', 'High', 'Critical']
pub_rows = list(csv.DictReader(open(os.path.join(HERE, '../input/published_ratings.csv'))))
ids = [r['id'] for r in pub_rows]; asset = {r['id']: r['asset'] for r in pub_rows}
pub = np.array([[int(r[k]) for k in DIMS] for r in pub_rows], float)
raw = list(csv.DictReader(open(os.path.join(HERE, '../ratings/ratings_all_runs.csv'))))
models = list(dict.fromkeys(r['model'] for r in raw))
short = [m.split(' (')[0] for m in models]                       # 'LLM A'
name = {s: m.split('(')[1].rstrip(')') for s, m in zip(short, models)}   # 'Claude Sonnet 5.5'
R = {}
for s, m in zip(short, models):
    rs = sorted({int(r['run']) for r in raw if r['model'] == m})
    R[s] = np.array([[[float(next(x[k] for x in raw if x['id'] == i and x['model'] == m and int(x['run']) == n)) for k in DIMS]
                      for i in ids] for n in rs])
P = np.concatenate([R[s] for s in short])
N = len(short); NR = len(P); NC = len([s for s in short if name[s].startswith('Claude')])   # models, runs, Claude models
CLAUDE = [s for s in short if name[s].startswith('Claude')]
K = R[short[0]].shape[0]
nu = lambda x: 1 + 4 * (x - 1) / 9
ds = lambda a: (nu(a[:, :5]).sum(1) + a[:, 5]) / 6
band = lambda v: np.select([v <= 1.8, v <= 2.6, v <= 3.4, v <= 4.2], [0, 1, 2, 3], 4)
base = ds(pub)

def kalpha(M):
    m, n = M.shape; vals = M.ravel(); do = 0.0
    for u in range(n):
        c = M[:, u]; do += ((c[:, None] - c[None, :]) ** 2).sum() / (m - 1)
    N = m * n; De = ((vals[:, None] - vals[None, :]) ** 2).sum() / (N * (N - 1)); return 1 - (do / (m * n)) / De

# ---------------------------------------------------------------- style tokens (reference palette, light)
SURF, INK, INK2, MUTED, GRID, AXIS = '#ffffff', '#0b0b0b', '#52514e', '#898781', '#e1e0d9', '#c3c2b7'
CAT = dict(zip(short, ['#2a78d6', '#eb6834', '#1baf7a', '#eda100', '#e87ba4', '#008300']))
SEQ = ['#cde2fb', '#9ec5f4', '#6da7ec', '#3987e5', '#256abf', '#184f95', '#0d366b']
ORD = ['#86b6ef', '#5598e7', '#2a78d6', '#1c5cab', '#0d366b']            # ordinal ramp, step 250 -> 700
DIV_NEG, DIV_MID, DIV_POS = '#2a78d6', '#f0efec', '#e34948'
seq_cmap = mcolors.LinearSegmentedColormap.from_list('seq', SEQ)
div_cmap = mcolors.LinearSegmentedColormap.from_list('div', [DIV_NEG, '#9ec5f4', DIV_MID, '#f3a8a7', DIV_POS])
for f in font_manager.findSystemFonts():
    if 'Inter' in os.path.basename(f) and 'Display' not in os.path.basename(f): font_manager.fontManager.addfont(f)
plt.rcParams.update({'font.family': 'Inter', 'font.size': 7.2, 'axes.edgecolor': AXIS, 'axes.linewidth': 0.7, 'axes.labelcolor': INK2,
                     'xtick.color': MUTED, 'ytick.color': MUTED, 'text.color': INK, 'figure.facecolor': SURF, 'axes.facecolor': SURF,
                     'savefig.facecolor': SURF, 'pdf.fonttype': 42, 'axes.spines.top': False, 'axes.spines.right': False,
                     'xtick.major.width': 0.6, 'ytick.major.width': 0.6, 'xtick.major.size': 2.5, 'ytick.major.size': 2.5})

def lum_text(rgba): r, g, b = rgba[:3]; return '#ffffff' if 0.2126 * r + 0.7152 * g + 0.0722 * b < 0.45 else INK
def title(ax, letter, t, sub=None, top=False):
    """panel letter + takeaway title (+ subtitle), placed in points above the axes; `top` leaves room for tick labels drawn above"""
    d1, d2 = (30, 19) if top else (17, 6)
    kw = dict(xycoords='axes fraction', textcoords='offset points', ha='left', va='bottom', annotation_clip=False)
    ax.annotate(letter, (0, 1), xytext=(0, d1), fontsize=8.6, fontweight='bold', color=INK, **kw)
    ax.annotate(t, (0, 1), xytext=(10 if letter else 0, d1), fontsize=8.2, fontweight='semibold', color=INK, **kw)
    if sub: ax.annotate(sub, (0, 1), xytext=(0, d2), fontsize=6.5, color=INK2, **kw)
def model_labels(ax, rows, x=-0.015, fs=7):
    """row labels with a coloured dot (identity) and ink text"""
    ax.set_yticks(range(len(rows))); ax.set_yticklabels([''] * len(rows))
    for i, s in enumerate(rows):
        if s in CAT:
            ax.plot([-0.03], [i], 'o', ms=5.2, color=CAT[s], mec=SURF, mew=1.2, transform=ax.get_yaxis_transform(), clip_on=False)
            ax.text(-0.06, i, s, ha='right', va='center', fontsize=fs, color=INK, transform=ax.get_yaxis_transform())
        else:
            ax.text(-0.015, i, s, ha='right', va='center', fontsize=fs, color=INK, transform=ax.get_yaxis_transform())
def save(fig, nm):
    for ext in ('pdf', 'png'): fig.savefig(os.path.join(OUT, f'{nm}.{ext}'), dpi=300 if ext == 'png' else None, bbox_inches='tight', pad_inches=0.06)
    plt.close(fig)
def dump(nm, head, rows):
    with open(os.path.join(OUT, 'data', nm + '.csv'), 'w', newline='') as f: w = csv.writer(f); w.writerow(head); w.writerows(rows)

SHORT = {'GOV-01': 'Competent authority', 'GOV-02': 'Regulatory framework', 'GOV-03': 'Strategic planning', 'SVC-01': 'Registration & EID',
         'SVC-02': 'Tracking & monitoring', 'SVC-03': 'Flight authorization', 'SVC-04': 'API gateway (service)', 'SVC-05': 'Geo-awareness service',
         'DAT-01': 'Geo-awareness database', 'DAT-02': 'CIS / single source of truth', 'DAT-03': 'Traffic & weather data', 'DAT-04': 'Logs & audit trails',
         'DAT-05': 'Data-layer API gateway', 'DAT-06': 'Database server', 'INF-01': 'GNSS / navigation', 'INF-02': 'Communication networks',
         'INF-03': 'UAS hardware', 'INF-04': 'Power & infrastructure', 'INF-05': 'Sensors & ground stations', 'INF-06': 'Vertiports', 'INF-07': 'Supply chain'}
# ---------------------------------------------------------------- numbers
alpha = np.array([[kalpha(R[s][:, :, j]) for j in range(6)] + [kalpha(np.array([ds(r) for r in R[s]]))] for s in short])
bias = np.array([(R[s] - pub).mean((0, 1)) for s in short])
mad5 = np.array([np.abs(R[s][:, :, :5] - pub[:, :5]).mean() for s in short])
inband = np.array([(np.array([band(ds(r)) for r in R[s]]) == band(base)).mean() for s in short])
bandcnt = np.array([[np.mean([(band(ds(r)) == b).sum() for r in R[s]]) for b in range(5)] for s in short])
pubcnt = np.array([(band(base) == b).sum() for b in range(5)])
tau = {s: [kendalltau(base, ds(r))[0] for r in R[s]] for s in short}
inf02 = {s: [int(np.argsort(-ds(r)).tolist().index(ids.index('INF-02')) + 1) for r in R[s]] for s in short}
pub_inf02 = int(np.argsort(-base).tolist().index(ids.index('INF-02')) + 1)
conf = np.zeros((5, 5))
for s in short:
    for r in R[s]:
        for a, b in zip(pub[:, 5].astype(int), r[:, 5].astype(int)): conf[a - 1, b - 1] += 1
dump('fig1a_alpha', ['model'] + DIMS + ['DREAD-S'], [[s] + list(np.round(a, 3)) for s, a in zip(short, alpha)])
dump('fig1b_bias', ['model'] + DIMS, [[s] + list(np.round(b, 3)) for s, b in zip(short, bias)])
dump('fig1c_mad_and_band', ['model', 'MAD_five_dread', 'share_in_published_band'], [[s, round(m, 3), round(b, 3)] for s, m, b in zip(short, mad5, inband)])
dump('fig1d_band_counts', ['rater'] + BANDS, [['Published'] + list(pubcnt)] + [[s] + list(np.round(b, 2)) for s, b in zip(short, bandcnt)])
dump('fig1e_tau_runs', ['model', 'run', 'tau', 'inf02_rank'], [[s, k + 1, round(tau[s][k], 3), inf02[s][k]] for s in short for k in range(3)])
dump('fig1f_S_confusion_published_by_llm', ['published_S'] + [f'llm_S{k}' for k in range(1, 6)], [[i + 1] + list(map(int, conf[i])) for i in range(5)])

# ================================================================ FIGURE 1
fig = plt.figure(figsize=(6.5, 8.5))
gs = fig.add_gridspec(3, 6, hspace=0.62, wspace=1.9, left=0.10, right=0.985, top=0.885, bottom=0.05, height_ratios=[0.8, 1, 1.0])
if WITH_TITLES:
    fig.text(0.10, 0.985, f'How far {N} LLM raters reproduce the published DREAD-S ratings', fontsize=10.5, fontweight='bold', ha='left')
    fig.text(0.10, 0.964, f'21 catalogue entries, {K} runs per model ({NR} runs), same prompt; published ratings are the baseline', fontsize=7, color=INK2, ha='left')

# (a) consistency heatmap
ax = fig.add_subplot(gs[0, :3]); cols = ['D', 'R', 'E', 'A', 'D2', 'S', 'DREAD-S']
vmin, vmax = 0.7, 1.0
im = ax.imshow(alpha, cmap=seq_cmap, vmin=vmin, vmax=vmax, aspect='auto')
for (i, j), v in np.ndenumerate(alpha): ax.text(j, i, f'{v:.2f}', ha='center', va='center', fontsize=6.6, color=lum_text(seq_cmap((v - vmin) / (vmax - vmin))))
ax.set_xticks(range(7)); ax.set_xticklabels(cols, fontsize=6.8, color=INK2); ax.xaxis.tick_top(); ax.tick_params(length=0)
model_labels(ax, short); ax.spines[:].set_visible(False)
for k in range(1, 7): ax.axvline(k - 0.5, color=SURF, lw=1.6)
for k in range(1, N): ax.axhline(k - 0.5, color=SURF, lw=1.6)
ax.axvline(5.5, color=SURF, lw=3)
title(ax, 'a', 'Each model is consistent with itself', "Krippendorff's α across its 3 runs (darker = more consistent)", top=True)
ax.title.set_visible(False)

# (b) bias heatmap
ax = fig.add_subplot(gs[0, 3:]); lim = 2.0
ax.imshow(bias, cmap=div_cmap, vmin=-lim, vmax=lim, aspect='auto')
for (i, j), v in np.ndenumerate(bias): ax.text(j, i, f'{v:+.1f}', ha='center', va='center', fontsize=6.6, color=lum_text(div_cmap((v + lim) / (2 * lim))))
ax.set_xticks(range(6)); ax.set_xticklabels(DIMS, fontsize=6.8, color=INK2); ax.xaxis.tick_top(); ax.tick_params(length=0)
model_labels(ax, short); ax.spines[:].set_visible(False)
for k in range(1, 6): ax.axvline(k - 0.5, color=SURF, lw=1.6)
for k in range(1, N): ax.axhline(k - 0.5, color=SURF, lw=1.6)
title(ax, 'b', 'Claude rates likelihood lower, GPT-6 does not', 'Mean rating, LLM minus published (blue = LLM lower, red = higher)', top=True)
ax.title.set_visible(False)

for _a in fig.axes[:2]:                      # pull the first row closer to the second
    p = _a.get_position(); _a.set_position([p.x0, p.y0 - 0.05, p.width, p.height])
# (c) closest model
ax = fig.add_subplot(gs[1, :3]); order = np.argsort(mad5)
for pos, k in enumerate(order):
    s = short[k]; ax.barh(pos, mad5[k], height=0.55, color=CAT[s], zorder=3)
    ax.text(mad5[k] + 0.03, pos, f'{mad5[k]:.2f}', va='center', fontsize=7, color=INK, fontweight='semibold' if pos == 0 else 'normal')
    ax.text(0.02, pos, f'{s}  {name[s].replace("Claude ", "")}', va='center', ha='left', fontsize=6.4, color='#ffffff' if CAT[s] in ('#2a78d6', '#008300') else INK, zorder=4)
ax.set_yticks([]); ax.set_ylim(len(short) - 0.4, -0.6); ax.set_xlim(0, 2.1); ax.set_xticks([0, 0.5, 1, 1.5, 2])
ax.xaxis.grid(True, color=GRID, lw=0.6, zorder=0); ax.set_axisbelow(True); ax.spines['left'].set_visible(False)
ax.set_xlabel('Mean absolute deviation per DREAD rating (points)', fontsize=6.8)
title(ax, 'c', f'{name[short[order[0]]].replace("Claude ", "").replace("OpenAI ", "")} is closest; none is close', 'Deviation from the published ratings, five DREAD ratings, sorted')
ax.title.set_visible(False)

# (d) bands stacked
ax = fig.add_subplot(gs[1, 3:]); rows = ['Published'] + short; data = np.vstack([pubcnt, bandcnt])
for i, rw in enumerate(rows):
    left = 0
    for b in range(5):
        v = data[i, b]
        if v <= 0: continue
        ax.barh(i, v, left=left, height=0.62, color=ORD[b], edgecolor=SURF, linewidth=1.4, zorder=3)
        if v >= 1.8: ax.text(left + v / 2, i, f'{v:.0f}' if i == 0 else f'{v:.1f}'.rstrip('0').rstrip('.'), ha='center', va='center', fontsize=6.4, color=lum_text(mcolors.to_rgba(ORD[b])))
        left += v
    if i > 0: ax.text(21.6, i, f'{inband[i - 1]:.0%}', va='center', ha='left', fontsize=6.8, color=INK)
ax.text(21.6, -0.95, 'stay in\npublished band', fontsize=6, color=INK2, ha='left', va='center')
ax.set_xlim(0, 21); ax.set_ylim(N + 0.5, -0.5); ax.set_xticks([0, 7, 14, 21]); ax.set_yticks([]); ax.spines['left'].set_visible(False)
ax.spines['bottom'].set_color(AXIS); ax.set_xlabel('Entries per band (mean of 3 runs)', fontsize=6.8)
model_labels(ax, rows)
ax.set_xlim(0, 21)
for b in range(5): ax.barh(-5, 0, color=ORD[b], label=BANDS[b])
ax.legend(ncol=5, fontsize=6, frameon=False, loc='upper center', bbox_to_anchor=(0.45, -0.20), handlelength=0.9, handleheight=0.9, columnspacing=0.8, handletextpad=0.35)
title(ax, 'd', 'Claude shifts bands down; GPT-6 stays closer', 'Distribution of the 21 entries over the DREAD-S bands')
ax.title.set_visible(False)

# (e1) tau strip
ax = fig.add_subplot(gs[2, :2]); rng = np.random.default_rng(3)
for i, s in enumerate(short):
    xs = i + np.array([-0.16, 0, 0.16]); ax.plot(xs, tau[s], 'o', ms=5.2, color=CAT[s], mec=SURF, mew=1.2, zorder=4, ls='none')
    ax.plot([i - 0.28, i + 0.28], [np.mean(tau[s])] * 2, color=INK, lw=1.2, zorder=5)
ax.axhline(0.87, color=MUTED, lw=0.8, ls=(0, (4, 2))); ax.text(N - 0.55, 0.885, 'ratings ±1 (perturbation) 0.87', ha='right', va='bottom', fontsize=6, color=INK2)
ax.set_ylim(0.2, 1.0); ax.set_xlim(-0.6, N - 0.4); ax.set_xticks(range(N)); ax.set_xticklabels([s.split()[1] for s in short], color=INK2, fontsize=7)
ax.yaxis.grid(True, color=GRID, lw=0.6, zorder=0); ax.set_axisbelow(True); ax.set_ylabel("Kendall's τ with published ranking", fontsize=6.6)
title(ax, 'e', 'Ranking only partly kept', 'τ per run, bar = mean')
ax.title.set_visible(False)

# (e2) INF-02 rank
ax = fig.add_subplot(gs[2, 2:4])
for i, s in enumerate(short):
    ys = np.array(inf02[s]); xs = i + np.array([-0.16, 0, 0.16]); ax.plot(xs, ys, 'o', ms=5.2, color=CAT[s], mec=SURF, mew=1.2, zorder=4, ls='none')
ax.axhline(pub_inf02, color=INK, lw=0.9); ax.text(N - 0.5, pub_inf02 + 0.18, 'published: 1st', ha='right', va='top', fontsize=6, color=INK2)
ax.set_ylim(10.7, 0.5); ax.set_yticks([1, 2, 4, 6, 8, 10]); ax.set_xlim(-0.6, N - 0.4); ax.set_xticks(range(N)); ax.set_xticklabels([s.split()[1] for s in short], color=INK2, fontsize=7)
ax.yaxis.grid(True, color=GRID, lw=0.6, zorder=0); ax.set_axisbelow(True); ax.set_ylabel('Rank of comm. networks (INF-02)', fontsize=6.6)
title(ax, 'f', 'First place never reproduced', f'never 1st in any of {NR} runs')
ax.title.set_visible(False)

# (f) S confusion
ax = fig.add_subplot(gs[2, 4:]); cm = mcolors.LinearSegmentedColormap.from_list('c', ['#ffffff'] + SEQ[1:])
mx = conf.max(); ax.imshow(conf, cmap=cm, vmin=0, vmax=mx, aspect='auto')
for (i, j), v in np.ndenumerate(conf):
    if v > 0: ax.text(j, i, f'{int(v)}', ha='center', va='center', fontsize=6.6, color=lum_text(cm(v / mx)))
for k in range(1, 5): ax.axvline(k - 0.5, color=GRID, lw=0.5); ax.axhline(k - 0.5, color=GRID, lw=0.5)
ax.add_patch(plt.Rectangle((-0.5, -0.5), 5, 5, fill=False, ec=AXIS, lw=0.7))
ax.set_xticks(range(5)); ax.set_xticklabels(range(1, 6), color=INK2); ax.set_yticks(range(5)); ax.set_yticklabels(range(1, 6), color=INK2)
ax.set_xlabel('LLM Safety impact S', fontsize=6.8); ax.set_ylabel('Published S', fontsize=6.8); ax.spines[:].set_visible(False); ax.tick_params(length=0)
w1 = (np.abs(P[:, :, 5] - pub[:, 5]) <= 1).mean()
title(ax, 'g', 'Safety impact transfers well', f'{w1:.0%} of {NR * 21} ratings within one level')
ax.title.set_visible(False)
save(fig, 'fig1_overview')

# ================================================================ FIGURE 2: where models disagree
meanall = P.mean(0); dev = meanall - pub
modmean = {s: R[s].mean(0) for s in short}
order_ids = list(range(21))
fig = plt.figure(figsize=(6.5, 5.4))
gs = fig.add_gridspec(1, 2, width_ratios=[1.0, 1.28], wspace=0.62, left=0.215, right=0.985, top=0.815, bottom=0.07)
if WITH_TITLES:
    fig.text(0.02, 0.975, 'Where the models disagree with the published ratings', fontsize=10.5, fontweight='bold', ha='left')
    fig.text(0.02, 0.948, f'Mean of {NR} runs against the published rating, per entry and rating', fontsize=7, color=INK2, ha='left')
ax = fig.add_subplot(gs[0, 0]); lim = 4.0
ax.imshow(dev, cmap=div_cmap, vmin=-lim, vmax=lim, aspect='auto')
for (i, j), v in np.ndenumerate(dev):
    if abs(v) >= 2.0: ax.text(j, i, f'{v:+.0f}', ha='center', va='center', fontsize=6.2, color=lum_text(div_cmap((v + lim) / (2 * lim))))
ax.set_xticks(range(6)); ax.set_xticklabels(DIMS, fontsize=6.8, color=INK2); ax.xaxis.tick_top(); ax.tick_params(length=0)
ax.set_yticks(range(21)); ax.set_yticklabels([f'{i}  {SHORT[i]}' for i in ids], fontsize=6.0, color=INK)
for k in range(1, 6): ax.axvline(k - 0.5, color=SURF, lw=1.4)
for k in range(1, 21): ax.axhline(k - 0.5, color=SURF, lw=1.4)
for k in (3, 8, 14): ax.axhline(k - 0.5, color=INK2, lw=0.7)
ax.spines[:].set_visible(False)
title(ax, 'a', 'Every entry, every rating', 'LLM mean minus published; labels where |difference| ≥ 2', top=True)
cax = fig.add_axes([0.02 + 0.0, 0.025, 0.10, 0.011]); cb = matplotlib.colorbar.ColorbarBase(cax, cmap=div_cmap, norm=mcolors.Normalize(-lim, lim), orientation='horizontal')
cb.set_ticks([-4, 0, 4]); cb.ax.tick_params(labelsize=6, length=2); cb.outline.set_visible(False); cb.ax.set_title('LLM lower  ←  →  LLM higher', fontsize=5.8, color=INK2, pad=2)

# (b) dumbbells for the 12 largest gaps
cells = [(i, j) for i in range(21) for j in range(6)]
top = sorted(cells, key=lambda c: -abs(dev[c]))[:12]
ax = fig.add_subplot(gs[0, 1])
for pos, (i, j) in enumerate(top):
    vals = [modmean[s][i, j] for s in short]
    ax.plot([min(vals + [pub[i, j]]), max(vals + [pub[i, j]])], [pos, pos], color=AXIS, lw=1.2, zorder=1, solid_capstyle='round')
    for s, v in zip(short, vals): ax.plot(v, pos, 'o', ms=5.6, color=CAT[s], mec=SURF, mew=1.2, zorder=3)
    ax.plot(pub[i, j], pos, 'D', ms=6, color=INK, mec=SURF, mew=1.2, zorder=4)
ax.set_yticks(range(12)); ax.set_yticklabels([f'{ids[i]}  {DIMN[DIMS[j]]}' for i, j in top], fontsize=6.8, color=INK)
ax.set_ylim(11.6, -0.6); ax.set_xlim(1, 10); ax.set_xticks(range(1, 11)); ax.xaxis.grid(True, color=GRID, lw=0.6, zorder=0); ax.set_axisbelow(True)
ax.spines['left'].set_visible(False); ax.tick_params(axis='y', length=0)
ax.set_xlabel('Rating (1–10; Safety impact 1–5)', fontsize=6.8)
title(ax, 'b', 'The twelve largest gaps', '◆ published rating, ● mean of each model’s 3 runs', top=True)
handles = [plt.Line2D([], [], marker='D', ls='none', ms=5.5, color=INK, mec=SURF, label='Published')] + [plt.Line2D([], [], marker='o', ls='none', ms=5.5, color=CAT[s], mec=SURF, label=f'{s}  {name[s].replace("Claude ", "")}') for s in short]
ax.legend(handles=handles, ncol=4, fontsize=6.2, frameon=False, loc='upper center', bbox_to_anchor=(0.45, -0.075), columnspacing=1.0, handletextpad=0.2)
dump('fig2a_signed_deviation_mean_all_runs', ['id'] + DIMS, [[i] + list(np.round(d, 2)) for i, d in zip(ids, dev)])
dump('fig2b_top12_gaps', ['entry', 'rating', 'published'] + short, [[ids[i], DIMN[DIMS[j]], pub[i, j]] + [round(modmean[s][i, j], 2) for s in short] for i, j in top])
save(fig, 'fig2_where_models_disagree')

# ================================================================ FIGURE 3: models vs you
labs = short + ['Published']; NL = N + 1; mm = [R[s].mean(0) for s in short] + [pub]
tm = np.array([[kendalltau(ds(a), ds(b))[0] for b in mm] for a in mm])
mad_m = np.array([[np.abs(a[:, :5] - b[:, :5]).mean() for b in mm] for a in mm])
fig = plt.figure(figsize=(6.5, 3.6))
gs = fig.add_gridspec(1, 2, width_ratios=[1, 1.12], wspace=0.42, left=0.085, right=0.985, top=0.74, bottom=0.17)
if WITH_TITLES: fig.text(0.02, 0.96, f'The {N} models agree with each other more than with the published ratings', fontsize=10.5, fontweight='bold', ha='left')
ax = fig.add_subplot(gs[0, 0]); mask = np.triu(np.ones((NL, N), bool), 0)
cm2 = mcolors.LinearSegmentedColormap.from_list('t', SEQ[:6]); lo, hi = 0.5, 1.0
ax.imshow(np.where(mask, np.nan, np.clip(tm[:, :N], lo, hi)), cmap=cm2, vmin=lo, vmax=hi, aspect='equal')
for i in range(NL):
    for j in range(i):
        ax.text(j, i, f'{tm[i, j]:.2f}', ha='center', va='center', fontsize=6.6, color=lum_text(cm2((np.clip(tm[i, j], lo, hi) - lo) / (hi - lo))))
    if i == j: pass
ax.set_xticks(range(N)); ax.set_xticklabels([l.replace('LLM ', '') for l in labs[:N]], fontsize=7, color=INK2)
ax.set_yticks(range(NL)); ax.set_yticklabels([l.replace('LLM ', '') for l in labs], fontsize=7, color=INK2)
ax.xaxis.tick_top(); ax.tick_params(length=0); ax.spines[:].set_visible(False)
ax.add_patch(plt.Rectangle((-0.5, N - 0.5), N, 1, fill=False, ec=INK, lw=1.0))
title(ax, 'a', 'Models rank the entries more alike', "Kendall's τ between DREAD-S rankings; outlined row: published", top=True)
# (b) strip: pairwise MAD in three groups (Claude-Claude, Claude-GPT-6, model vs published)
ax = fig.add_subplot(gs[0, 1])
ci = [i for i, s in enumerate(short) if s in CLAUDE]; oi = [i for i in range(N) if i not in ci]
g1 = [(a, b) for a, b in itertools.combinations(ci, 2)]                      # same provider
g2 = [(a, b) for a in ci for b in oi]                                       # across providers
g3 = [(a, N) for a in range(N)]                                             # model vs published
groups = [g1, g2, g3]; gx = [0, 1, 2]
for x, g in zip(gx, groups):
    y = [mad_m[a, b] for a, b in g]
    if x < 2: ax.plot(np.zeros(len(y)) + x + np.linspace(-0.14, 0.14, len(y)), y, 'o', ms=5.2, color=MUTED, mec=SURF, mew=1.1, zorder=3)
    else:
        for k, (a, b) in enumerate(g): ax.plot(x + (k - (len(g) - 1) / 2) * 0.10, y[k], 'o', ms=5.6, color=CAT[short[a]], mec=SURF, mew=1.2, zorder=3)
    ax.plot([x - 0.3, x + 0.3], [np.mean(y)] * 2, color=INK, lw=1.2, zorder=4)
    ax.text(x + 0.34, np.mean(y), f'{np.mean(y):.2f}', va='center', fontsize=7, fontweight='semibold')
ax.set_xlim(-0.6, 2.75); ax.set_ylim(0, 1.9); ax.set_xticks(gx)
ax.set_xticklabels([f'Claude–Claude\n{len(g1)} pairs', f'Claude–GPT-6\n{len(g2)} pairs', f'Model–published\n{N} models'], fontsize=6.4, color=INK2)
ax.yaxis.grid(True, color=GRID, lw=0.6, zorder=0); ax.set_axisbelow(True); ax.set_ylabel('Mean absolute deviation, five DREAD\nratings (mean of 3 runs per model)', fontsize=6.6)
title(ax, 'b', 'Same-provider models are closest', 'Each dot is one pair; coloured: model vs published', top=True)
for k, (a, b) in enumerate(g3): ax.text(2 + (k - (len(g3) - 1) / 2) * 0.10, mad_m[a, b] + 0.09, short[a].split()[1], ha='center', fontsize=5.8, color=INK2)
dump('fig3a_tau_between', ['rater'] + labs, [[l] + list(np.round(r, 3)) for l, r in zip(labs, tm)])
dump('fig3b_mad_pairs', ['pair', 'MAD_five_dread'], [[f'{short[a]} vs {short[b]}', round(mad_m[a, b], 3)] for a, b in g1 + g2] + [[f'{short[a]} vs published', round(mad_m[a, N], 3)] for a in range(N)])
save(fig, 'fig3_models_vs_published')
print('figures written to', os.path.abspath(OUT))
