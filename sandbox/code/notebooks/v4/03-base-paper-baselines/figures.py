"""
figures.py -- v4 Phase 2 figures (white background, for the thesis and the supervisor), from the evaluation JSON
files and the training histories. Writes PNG (200 dpi) and SVG to output/figures/.

  fig1_success_all_methods : mission success of all 9 methods, Stage 2 and Stage 3 (bar = mean, line = 95% CI,
                             dots = the 10 seeds)
  fig2_pah_vs_each_method  : MAPPO + PAH minus each method, with 95% Welch CI (right of 0 = PAH better)
  fig3_gap_breakdown       : DA-MAPPO (2D) -> Plain MAPPO -> Fixed-weight MAPPO -> MAPPO + PAH, one change per step
  fig4_outcomes            : how episodes end (success / obstacle collision / drone collision / timeout), Stage 3
  fig5_learning_curves     : training-time success (20 episodes every 100, seed 999) -- NOT the final numbers
  fig6_ranking_vs_paper    : DA-MAPPO paper (Table V, ENV-3) next to ours (Stage 3), each sorted best first
  fig7_difficulty_vs_paper : how success falls as the task gets harder, paper (30/40/50 obstacles) and ours (Stage 2/3)
  fig8_gain_over_mappo     : each method minus MAPPO, paper and ours -- the comparison that survives the setup gap
Base-paper numbers: DA-MAPPO (IEEE Internet of Things Journal), Table V, dynamic multi-target, N = 3 drones, 3D
Gazebo; transcribed in docs/research/09_literature_comparison_report.md. The paper gives no seed spread, so its
bars carry no CI. Absolute numbers are not comparable (simulator, sensors, network, budget); rankings, trends and
differences to MAPPO are. IGAT-MARL reports a different task and metrics, so it has no numeric panel.

Numbers use summarize.py (same statistics, half-up rounding). RMAPPO is left out of the figures: it did not learn
under the shared settings (REPORT.md, "RMAPPO note"), so it is not a performance number.

Usage:  python figures.py
"""
import os, sys, json, glob
import numpy as np
from scipy import stats
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import summarize as S                                   # welch(), f1(), load(), NAMES

OUT = os.path.join(HERE, 'output', 'figures')
PHASE1B = os.path.join(HERE, '..', '02-redesign')
OURS = ['mappo-pah', 'fixed-weight-mappo', 'tau-rule-mappo', 'mappo-pah-no-hungarian', 'plain-mappo']
BASE = ['igat-style', 'da-mappo-2d', 'mappo', 'ippo']
SHORT = {'mappo-pah': 'MAPPO + PAH', 'fixed-weight-mappo': 'Fixed-weight MAPPO', 'tau-rule-mappo': 'Hand-coded τ-rule MAPPO',
         'mappo-pah-no-hungarian': 'MAPPO + PAH (no assignment)', 'plain-mappo': 'Plain MAPPO',
         'igat-style': 'IGAT-style MAPPO', 'da-mappo-2d': 'DA-MAPPO (2D)', 'mappo': 'MAPPO', 'ippo': 'IPPO'}

# colour by role: MAPPO + PAH is the one accent; our other methods a light step of the same hue; base-paper methods grey
ACCENT, ACCENT_LIGHT, GREY = '#2a78d6', '#9cc1ec', '#b4b3ad'
INK, MUTED, GRID = '#0b0b0b', '#52514e', '#e4e3df'
# categorical slots 1-5 of the validated reference palette (adjacent CVD dE >= 9.1, normal-vision >= 19.6);
# three slots are below 3:1 contrast, so every series is also labelled directly
CAT = ['#2a78d6', '#eb6834', '#1baf7a', '#eda100', '#e87ba4']

plt.rcParams.update({
    'figure.facecolor': 'white', 'axes.facecolor': 'white', 'savefig.facecolor': 'white',
    'font.family': 'DejaVu Sans', 'font.size': 10, 'axes.titlesize': 11, 'axes.titleweight': 'bold',
    'axes.labelsize': 10, 'axes.spines.top': False, 'axes.spines.right': False, 'axes.grid': True,
    'axes.axisbelow': True, 'grid.color': GRID, 'grid.linewidth': 0.8, 'axes.edgecolor': MUTED,
    'xtick.color': MUTED, 'ytick.color': INK, 'axes.labelcolor': INK, 'text.color': INK,
})

R = S.load('eval_raw')


def get(st, m, k):
    return np.array([R[(st, m, s)][k] for s in sorted(s for (a, b, s) in R if a == st and b == m)], dtype=float)


def colour(m):
    return ACCENT if m == 'mappo-pah' else ACCENT_LIGHT if m in OURS else GREY


def half(x):
    return stats.t.ppf(0.975, len(x) - 1) * x.std(ddof=1) / np.sqrt(len(x))


def save(fig, name):
    os.makedirs(OUT, exist_ok=True)
    fig.savefig(os.path.join(OUT, name + '.png'), dpi=200, bbox_inches='tight')
    fig.savefig(os.path.join(OUT, name + '.svg'), bbox_inches='tight')
    plt.close(fig)


def role_legend(ax, loc='lower right'):
    from matplotlib.patches import Patch
    ax.legend(handles=[Patch(color=ACCENT, label='MAPPO + PAH (proposed)'), Patch(color=ACCENT_LIGHT, label='Our other methods'),
                       Patch(color=GREY, label='Base-paper methods')], loc=loc, fontsize=8.5, frameon=False)


# ---- fig 1: success of every method ----------------------------------------------------------------------
order = sorted(OURS + BASE, key=lambda m: get(3, m, 'success').mean())          # best at the top
fig, axes = plt.subplots(1, 2, figsize=(12.5, 5.6), sharey=True)
for ax, st in zip(axes, (2, 3)):
    y = np.arange(len(order))
    for i, m in enumerate(order):
        v = get(st, m, 'success') * 100
        ax.barh(y[i], v.mean(), 0.62, color=colour(m), edgecolor='white', linewidth=2, zorder=2)
        ax.errorbar(v.mean(), y[i], xerr=half(v), color=INK, lw=1.2, capsize=3, zorder=4)
        ax.scatter(v, y[i] + np.linspace(-0.18, 0.18, len(v)), s=9, color=INK, alpha=0.45, zorder=3, linewidths=0)
        ax.text(min(v.max(), 100) + 2, y[i], S.f1(v.mean()), va='center', fontsize=9,
                fontweight='bold' if m == 'mappo-pah' else 'normal')
    ax.set_yticks(y); ax.set_yticklabels([SHORT[m] for m in order])
    ax.set_xlim(0, 112); ax.grid(axis='y', visible=False)
    ax.set_xlabel('Mission success (%)')
    ax.set_title('Stage {} — {}'.format(st, {2: '5 drones, 10 obstacles', 3: '8 drones, 20 obstacles'}[st]), loc='left')
role_legend(axes[1])
fig.suptitle('Mission success of every method (bar = mean of 10 seeds, line = 95% CI, dots = seeds)',
             x=0.01, ha='left', fontsize=12, fontweight='bold')
fig.text(0.01, -0.01, 'Final evaluation: 200 deterministic episodes per model, evaluation seed 7001. Methods ordered by '
         'Stage 3 success. RMAPPO not shown (did not learn under the shared settings; see report).', fontsize=8.5, color=MUTED)
fig.tight_layout()
save(fig, 'fig1_success_all_methods')

# ---- fig 2: PAH minus each method -------------------------------------------------------------------------
others = [m for m in OURS[1:] + BASE]
others = sorted(others, key=lambda m: S.welch(get(3, 'mappo-pah', 'success') * 100, get(3, m, 'success') * 100)[0])
fig, axes = plt.subplots(1, 2, figsize=(12.5, 5.2), sharey=True)
for ax, st in zip(axes, (2, 3)):
    for i, m in enumerate(others):
        d, lo, hi = S.welch(get(st, 'mappo-pah', 'success') * 100, get(st, m, 'success') * 100)
        settled = lo > 0
        primary = st == 3 and m == 'fixed-weight-mappo'
        c = ACCENT if settled else MUTED
        ax.plot([lo, hi], [i, i], color=c, lw=2.2, solid_capstyle='round', zorder=3)
        ax.scatter(d, i, s=60 if primary else 42, color=c, zorder=4, edgecolors='white', linewidths=1.5,
                   marker='D' if primary else 'o')
        ax.text(hi + 1.5, i, '{} [{}, {}]{}'.format(S.f1(d, True), S.f1(lo, True), S.f1(hi, True),
                                                   ('  ← primary question' if primary else '') + ('' if settled else '  not settled')),
                va='center', fontsize=8.5, color=INK, fontweight='bold' if primary else 'normal')
    ax.axvline(0, color=INK, lw=1, zorder=2)
    ax.set_yticks(range(len(others))); ax.set_yticklabels(['vs ' + SHORT[m] for m in others])
    ax.set_xlim(-8, 105); ax.grid(axis='y', visible=False)
    ax.set_xlabel('MAPPO + PAH minus method (success points)')
    ax.set_title('Stage {}'.format(st), loc='left')
fig.suptitle('How much better MAPPO + PAH is than each method (point = difference, line = 95% Welch CI)',
             x=0.01, ha='left', fontsize=12, fontweight='bold')
fig.text(0.01, -0.05, 'A line entirely right of 0 means MAPPO + PAH is better; a line crossing 0 is not settled. '
         'Blue = settled, grey = not settled. Only the Stage 3 comparison with Fixed-weight MAPPO is primary; the rest are '
         'secondary, without multiple-testing correction.', fontsize=8.5, color=MUTED, wrap=True)
fig.tight_layout()
save(fig, 'fig2_pah_vs_each_method')

# ---- fig 3: the gap to DA-MAPPO (2D), one change per step --------------------------------------------------
chain = [('da-mappo-2d', 'DA-MAPPO (2D)'), ('plain-mappo', '+ conflict-graph\nobservation'),
         ('fixed-weight-mappo', '+ separate mission and\nsafety value heads'), ('mappo-pah', "+ PAH's learned α")]
fig, axes = plt.subplots(1, 2, figsize=(12.5, 4.8), sharey=True)
for ax, st in zip(axes, (2, 3)):
    means = [get(st, m, 'success').mean() * 100 for m, _ in chain]
    for i, (m, lab) in enumerate(chain):
        if i == 0:
            ax.bar(i, means[0], 0.6, color=GREY, edgecolor='white', linewidth=2, zorder=2)
            ax.text(i, means[0] + 1.5, S.f1(means[0]), ha='center', fontsize=9)
            continue
        lo_, step = means[i - 1], means[i] - means[i - 1]
        d, lo, hi = S.welch(get(st, m, 'success') * 100, get(st, chain[i - 1][0], 'success') * 100)
        ax.bar(i, step, 0.6, bottom=lo_, color=ACCENT if m == 'mappo-pah' else ACCENT_LIGHT,
               edgecolor='white', linewidth=2, zorder=2)
        ax.plot([i - 1 + 0.3, i - 0.3], [lo_, lo_], color=MUTED, lw=0.8, ls=':', zorder=1)
        ax.text(i, means[i] + 1.5, '{}\n[{}, {}]'.format(S.f1(d, True), S.f1(lo, True), S.f1(hi, True)),
                ha='center', fontsize=8.5, fontweight='bold' if m == 'mappo-pah' else 'normal')
    ax.text(3, means[3] - 6, '= ' + S.f1(means[3]), ha='center', fontsize=9, color='white', fontweight='bold')
    ax.set_xticks(range(4)); ax.set_xticklabels([lab for _, lab in chain], fontsize=8.5)
    ax.set_ylim(0, 105); ax.grid(axis='x', visible=False)
    ax.set_title('Stage {}'.format(st), loc='left')
axes[0].set_ylabel('Mission success (%)')
fig.suptitle('Where the gap to DA-MAPPO (2D) comes from: each step changes one thing (95% Welch CI per step)',
             x=0.01, ha='left', fontsize=12, fontweight='bold')
fig.text(0.01, -0.02, "The steps are roughly additive. PAH's own contribution is the last step, not the whole gap.",
         fontsize=8.5, color=MUTED)
fig.tight_layout()
save(fig, 'fig3_gap_breakdown')

# ---- fig 4: how episodes end, Stage 3 ------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(12.5, 5.4))
parts = [('Success', CAT[0]), ('Collision with an obstacle', CAT[1]), ('Collision between drones', CAT[2]),
         ('Timeout', CAT[3])]
for i, m in enumerate(order):
    n = 200 * len(get(3, m, 'success'))
    succ = get(3, m, 'success').mean() * 100
    do = get(3, m, 'coll_drone_obstacle').sum() / n * 100
    dd = (get(3, m, 'coll_drone_drone').sum() + get(3, m, 'coll_both').sum()) / n * 100
    to = get(3, m, 'timeout').mean() * 100
    left = 0
    for (lab, c), v in zip(parts, (succ, do, dd, to)):
        ax.barh(i, v, 0.62, left=left, color=c, edgecolor='white', linewidth=2, zorder=2)
        if v >= 6:
            ax.text(left + v / 2, i, '{:.0f}'.format(v), ha='center', va='center', fontsize=8.5,
                    color='white' if c in (CAT[0], CAT[1]) else INK)
        left += v
ax.set_yticks(range(len(order))); ax.set_yticklabels([SHORT[m] for m in order])
for t in ax.get_yticklabels():
    if t.get_text() == 'MAPPO + PAH':
        t.set_fontweight('bold')
ax.set_xlim(0, 100); ax.grid(axis='y', visible=False); ax.set_xlabel('Share of test episodes (%)')
ax.legend(handles=[plt.Rectangle((0, 0), 1, 1, color=c) for _, c in parts], labels=[l for l, _ in parts],
          loc='lower center', bbox_to_anchor=(0.5, 1.0), ncol=4, fontsize=9, frameon=False)
fig.suptitle('How Stage 3 episodes end (8 drones, 20 obstacles; 2,000 test episodes per method)',
             x=0.01, ha='left', fontsize=12, fontweight='bold', y=1.04)
fig.text(0.01, -0.02, 'Failures are mostly obstacle collisions. Collisions where a drone hits a drone and an obstacle '
         'at the same step are counted with drone collisions. Segments under 6% are not labelled.', fontsize=8.5, color=MUTED)
fig.tight_layout()
save(fig, 'fig4_outcomes')

# ---- fig 5: learning curves (training-time) --------------------------------------------------------------------
CURVES = [('mappo-pah', PHASE1B), ('fixed-weight-mappo', PHASE1B), ('plain-mappo', PHASE1B),
          ('igat-style', HERE), ('da-mappo-2d', HERE)]
grid = np.arange(100, 8001, 100)
fig, axes = plt.subplots(1, 2, figsize=(12.5, 4.8), sharey=True)
for ax, st in zip(axes, (2, 3)):
    ends = []
    for (m, root), c in zip(CURVES, CAT):
        runs = sorted(glob.glob(os.path.join(root, 'runs', 'stage{}'.format(st), m, 'seed-*', 'history.json')))
        ys = []
        for f in runs:
            h = json.load(open(f))
            ys.append(np.interp(grid, h['episode'], np.array(h['success']) * 100))
        ys = np.array(ys)
        k = 5                                               # running mean over 5 checkpoints (500 episodes)
        sm = np.array([np.convolve(y, np.ones(k) / k, mode='valid') for y in ys])
        g = grid[k - 1:]
        mean, hw = sm.mean(0), stats.t.ppf(0.975, len(sm) - 1) * sm.std(0, ddof=1) / np.sqrt(len(sm))
        ax.fill_between(g, mean - hw, mean + hw, color=c, alpha=0.15, linewidth=0, zorder=1)
        ax.plot(g, mean, color=c, lw=2, zorder=3, label=SHORT[m])
        ends.append([mean[-1], SHORT[m], c])
    ends.sort(key=lambda e: e[0])                           # direct end labels, nudged apart
    last = -99
    for e in ends:
        yl = max(e[0], last + 5.5); last = yl
        ax.text(grid[-1] + 120, yl, e[1], va='center', fontsize=8.5, color=INK)
        ax.plot([grid[-1], grid[-1] + 100], [e[0], yl], color=e[2], lw=1)
    ax.set_xlim(0, 10400); ax.set_ylim(0, 100); ax.set_xticks([0, 2000, 4000, 6000, 8000])
    ax.set_xlabel('Training episodes'); ax.grid(axis='x', visible=False)
    ax.set_title('Stage {}'.format(st), loc='left')
axes[0].set_ylabel('Training-time success (%)')
fig.suptitle('Learning curves: mean of 10 seeds with 95% band (running mean over 500 episodes)',
             x=0.01, ha='left', fontsize=12, fontweight='bold')
fig.text(0.01, -0.02, 'Training-time checks: 20 deterministic episodes every 100 training episodes, evaluation seed 999. '
         'These are not the final results (200 episodes, seed 7001) and are higher than them.', fontsize=8.5, color=MUTED)
fig.tight_layout()
save(fig, 'fig5_learning_curves')

# ---- base paper: DA-MAPPO Table V (success %, ENV-1 / ENV-2 / ENV-3 = 30 / 40 / 50 obstacles, N = 3) ------------
PAPER = {'DA-MAPPO': [99, 95, 90], 'RMAPPO': [85, 69, 67], 'MAPPO': [83, 70, 64], 'IPPO': [78, 57, 53],
         'NavRL': [63, 53, 32], 'EGO-Planner v2': [53, 51, 43]}
# one colour per method that appears in both studies (same hue on both sides); everything else grey
IDENT = {'MAPPO + PAH': CAT[0], 'DA-MAPPO': CAT[1], 'DA-MAPPO (2D)': CAT[1], 'MAPPO': CAT[2], 'IPPO': CAT[3],
         'RMAPPO': CAT[4]}
PAPER_NOTE = ('DA-MAPPO paper: 3D Gazebo, 3 drones, LiDAR, ~3M steps with curriculum, no seed spread reported. Ours: 2D, '
              '8 drones, 8,000 episodes, 10 seeds. Absolute numbers are not comparable; the order of methods is.')

# ---- fig 6: ranking side by side --------------------------------------------------------------------------
fig, axes = plt.subplots(1, 2, figsize=(12.5, 5.2))
left = sorted(PAPER, key=lambda k: PAPER[k][2])
ours6 = sorted(OURS + BASE, key=lambda m: get(3, m, 'success').mean())
for ax, names, vals, title in (
        (axes[0], left, [PAPER[k][2] for k in left], 'DA-MAPPO paper, Table V, ENV-3 (50 obstacles)'),
        (axes[1], [SHORT[m] for m in ours6], [get(3, m, 'success').mean() * 100 for m in ours6],
         'Ours, Stage 3 (8 drones, 20 obstacles)')):
    for i, (n, v) in enumerate(zip(names, vals)):
        ax.barh(i, v, 0.62, color=IDENT.get(n, GREY), edgecolor='white', linewidth=2, zorder=2)
        ax.text(v + 1.5, i, S.f1(v) if isinstance(v, float) else str(v), va='center', fontsize=9,
                fontweight='bold' if n in ('DA-MAPPO', 'MAPPO + PAH') else 'normal')
    ax.set_yticks(range(len(names))); ax.set_yticklabels(names)
    for t in ax.get_yticklabels():
        if t.get_text() in ('DA-MAPPO', 'MAPPO + PAH'):
            t.set_fontweight('bold')
    ax.set_xlim(0, 108); ax.grid(axis='y', visible=False); ax.set_xlabel('Mission success (%)')
    ax.set_title(title, loc='left')
fig.suptitle('Ranking of methods: base paper and ours (same colour = same method in both studies)',
             x=0.01, ha='left', fontsize=12, fontweight='bold')
fig.text(0.01, -0.03, PAPER_NOTE + ' Grey: method in one study only. RMAPPO is not on our side (did not learn under '
         'the shared settings).', fontsize=8.5, color=MUTED, wrap=True)
fig.tight_layout()
save(fig, 'fig6_ranking_vs_paper')

# ---- fig 7: success as the task gets harder ----------------------------------------------------------------
fig, axes = plt.subplots(1, 2, figsize=(12.5, 4.8), sharey=True)
ax = axes[0]
last = -99
for k in ('IPPO', 'MAPPO', 'RMAPPO', 'DA-MAPPO'):                    # bottom to top, labels nudged apart
    ax.plot([30, 40, 50], PAPER[k], color=IDENT[k], lw=2, marker='o', ms=7, zorder=3)
    yl = max(PAPER[k][2], last + 5); last = yl
    ax.text(51.2, yl, '{}  {}'.format(k, PAPER[k][2]), va='center', fontsize=8.5)
ax.set_xticks([30, 40, 50]); ax.set_xticklabels(['ENV-1\n30 obstacles', 'ENV-2\n40 obstacles', 'ENV-3\n50 obstacles'])
ax.set_xlim(27, 60); ax.set_title('DA-MAPPO paper (3 drones)', loc='left'); ax.set_ylabel('Mission success (%)')
ax = axes[1]
ends = []
for m in ('mappo-pah', 'da-mappo-2d', 'mappo', 'ippo'):
    mean = [get(st, m, 'success').mean() * 100 for st in (2, 3)]
    hw = [half(get(st, m, 'success') * 100) for st in (2, 3)]
    ax.errorbar([0, 1], mean, yerr=hw, color=IDENT[SHORT[m]], lw=2, marker='o', ms=7, capsize=3, zorder=3)
    ends.append([mean[1], '{}  {}'.format(SHORT[m], S.f1(mean[1]))])
ends.sort(key=lambda e: e[0]); last = -99
for e in ends:
    yl = max(e[0], last + 5); last = yl
    ax.text(1.06, yl, e[1], va='center', fontsize=8.5)
ax.set_xticks([0, 1]); ax.set_xticklabels(['Stage 2\n5 drones, 10 obstacles', 'Stage 3\n8 drones, 20 obstacles'])
ax.set_xlim(-0.25, 1.75); ax.set_ylim(0, 105); ax.set_title('Ours (mean of 10 seeds, 95% CI)', loc='left')
for a in axes:
    a.grid(axis='x', visible=False)
fig.suptitle('How success falls as the task gets harder: the gap to MAPPO and IPPO widens in both studies',
             x=0.01, ha='left', fontsize=12, fontweight='bold')
fig.text(0.01, -0.03, PAPER_NOTE, fontsize=8.5, color=MUTED, wrap=True)
fig.tight_layout()
save(fig, 'fig7_difficulty_vs_paper')

# ---- fig 8: each method minus MAPPO --------------------------------------------------------------------------
def gain_rows(hardest):
    """(label, difference, ci or None, colour, is ours) -- one bar per row, paper and ours on separate rows."""
    envs = [2] if hardest else [0, 1]
    st = 3 if hardest else 2
    out = []
    for pk, om, name_p, name_o in (('DA-MAPPO', 'da-mappo-2d', 'DA-MAPPO', 'DA-MAPPO (2D)'), ('IPPO', 'ippo', 'IPPO', 'IPPO')):
        for e in envs:
            out.append(('{} − MAPPO   · paper ENV-{}'.format(name_p, e + 1), PAPER[pk][e] - PAPER['MAPPO'][e], None, IDENT[pk], False))
        d, lo, hi = S.welch(get(st, om, 'success') * 100, get(st, 'mappo', 'success') * 100)
        out.append(('{} − MAPPO   · ours Stage {}'.format(name_o, st), d, (lo, hi), IDENT[pk], True))
    d, lo, hi = S.welch(get(st, 'mappo-pah', 'success') * 100, get(st, 'mappo', 'success') * 100)
    out.append(('MAPPO + PAH − MAPPO   · ours Stage {}'.format(st), d, (lo, hi), ACCENT, True))
    return out


fig, axes = plt.subplots(1, 2, figsize=(13.5, 5.0), gridspec_kw=dict(width_ratios=[7, 5]))
for ax, hardest in zip(axes, (False, True)):
    rows8 = gain_rows(hardest)
    for i, (lab, d, ci, c, ours) in enumerate(rows8):
        ax.barh(i, d, 0.62, color=c, alpha=1.0 if ours else 0.4, edgecolor='white', linewidth=2, zorder=2)
        right = d
        if ci:
            ax.errorbar(d, i, xerr=[[d - ci[0]], [ci[1] - d]], color=INK, lw=1.1, capsize=3, zorder=4)
            right = ci[1]
        txt = '{:+d}'.format(int(d)) if ci is None else '{} [{}, {}]'.format(S.f1(d, True), S.f1(ci[0], True), S.f1(ci[1], True))
        ax.text(max(right, 0) + 2, i, txt, va='center', fontsize=8.5, fontweight='bold' if c == ACCENT else 'normal')
    ax.axvline(0, color=INK, lw=1, zorder=3)
    ax.set_yticks(range(len(rows8))); ax.set_yticklabels([r[0] for r in rows8], fontsize=8.5)
    ax.invert_yaxis(); ax.set_xlim(-20, 100); ax.grid(axis='y', visible=False)
    ax.set_xlabel('Success points above MAPPO (fixed assignment)')
    ax.set_title('Hardest setting: paper ENV-3 · ours Stage 3' if hardest else 'Easier settings: paper ENV-1, ENV-2 · ours Stage 2',
                 loc='left')
fig.suptitle('Gain over MAPPO in each study: the comparison that does not depend on the simulator',
             x=0.01, ha='left', fontsize=12, fontweight='bold')
fig.text(0.01, -0.04, 'Light bars: DA-MAPPO paper, Table V (no CI reported). Solid bars: ours, 95% Welch CI over 10 vs 10 seeds. '
         'Same direction in both studies: dynamic assignment above MAPPO (ours settled at Stage 3 only), IPPO not better than MAPPO; '
         'MAPPO + PAH adds a much larger gain.',
         fontsize=8.5, color=MUTED, wrap=True)
fig.tight_layout()
save(fig, 'fig8_gain_over_mappo')
print('figures written to', OUT)
