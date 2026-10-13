"""
figures.py -- v4 Phase 1b, Step 5 figures from output/eval_raw/ (white background, base-paper style bars).

  fig1_success_collision : mean success and collision per method, Stage 2 and Stage 3, every seed as a dot
  fig2_time_path         : T_ave and L_ave (successful episodes only)
  fig3_alpha_by_tau      : alpha against the hazard tau -- Fixed-weight, tau-rule and the learned PAH
Method names are on the x-axis, so colour is not needed to tell methods apart: baselines are grey,
MAPPO + PAH is the one accent colour, its Hungarian-off ablation a lighter step of the same hue.
"""
import os, json, glob
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'output')
METHODS = ['plain-mappo', 'fixed-weight-mappo', 'tau-rule-mappo', 'mappo-pah', 'mappo-pah-no-hungarian']
LABELS = ['Plain\nMAPPO', 'Fixed-weight\nMAPPO', 'Hand-coded\nτ-rule MAPPO', 'MAPPO\n+ PAH', 'MAPPO + PAH\n(Hungarian off)']
GREY, ACCENT, ACCENT_LIGHT, INK, MUTED = '#9a9994', '#2a78d6', '#8fb8ea', '#0b0b0b', '#52514e'
COLOURS = [GREY, GREY, GREY, ACCENT, ACCENT_LIGHT]

plt.rcParams.update({
    'figure.facecolor': 'white', 'axes.facecolor': 'white', 'savefig.facecolor': 'white',
    'font.family': 'DejaVu Sans', 'font.size': 10, 'axes.titlesize': 11, 'axes.labelsize': 10,
    'axes.spines.top': False, 'axes.spines.right': False, 'axes.grid': True, 'axes.grid.axis': 'y', 'axes.axisbelow': True,
    'grid.alpha': 0.25, 'grid.linestyle': '-', 'axes.edgecolor': MUTED, 'xtick.color': INK, 'ytick.color': MUTED,
    'axes.labelcolor': INK, 'text.color': INK,
})

R = [json.load(open(f)) for f in glob.glob(os.path.join(OUT, 'eval_raw', '*.json'))]
get = lambda st, m, k: np.array([r[k] for r in sorted(R, key=lambda r: r['seed']) if r['stage'] == st and r['method'] == m])


def bars(ax, st, key, scale, ylabel, ylim, fmt):
    x = np.arange(len(METHODS))
    for i, m in enumerate(METHODS):
        v = get(st, m, key) * scale
        mean = np.nanmean(v)
        ax.bar(x[i], mean, 0.62, color=COLOURS[i], edgecolor='white', linewidth=2, zorder=2)
        jitter = np.linspace(-0.16, 0.16, len(v))
        ax.scatter(x[i] + jitter, v, s=12, color=INK, alpha=0.55, zorder=3, linewidths=0)
        ax.text(x[i], max(mean, np.nanmax(v)) + (ylim[1] - ylim[0]) * 0.02, fmt.format(mean),
                ha='center', va='bottom', fontsize=9, fontweight='bold' if m == 'mappo-pah' else 'normal')
    ax.set_xticks(x); ax.set_xticklabels(LABELS, fontsize=8.5)
    ax.set_ylabel(ylabel); ax.set_ylim(*ylim)


def save(fig, name):
    fig.savefig(os.path.join(OUT, name + '.png'), dpi=200, bbox_inches='tight')
    fig.savefig(os.path.join(OUT, name + '.svg'), bbox_inches='tight')
    plt.close(fig)


# ---- fig 1: success and collision ------------------------------------------------------------------------
fig, axes = plt.subplots(2, 2, figsize=(12, 8))
for j, st in enumerate((2, 3)):
    sub = {2: 'Stage 2 — 5 drones, 10 discs', 3: 'Stage 3 — 8 drones, 20 discs'}[st]
    bars(axes[0, j], st, 'success', 100, 'Mission success (%)', (0, 112), '{:.1f}')
    axes[0, j].set_title('({}) Success — {}'.format('ab'[j], sub))
    bars(axes[1, j], st, 'collision', 100, 'Collision (%)', (0, 75), '{:.1f}')
    axes[1, j].set_title('({}) Collision — {}'.format('cd'[j], sub))
fig.suptitle('Final evaluation: 200 deterministic episodes per model, 10 seeds per method (dots = seeds, bar = mean)',
             fontsize=11, y=1.0)
fig.tight_layout()
save(fig, 'fig1_success_collision')

# ---- fig 2: T_ave and L_ave -------------------------------------------------------------------------------
fig, axes = plt.subplots(2, 2, figsize=(12, 8))
for j, st in enumerate((2, 3)):
    sub = {2: 'Stage 2', 3: 'Stage 3'}[st]
    t = np.concatenate([get(s, m, 'T_ave') for s in (2, 3) for m in METHODS])
    l = np.concatenate([get(s, m, 'L_ave') for s in (2, 3) for m in METHODS])
    bars(axes[0, j], st, 'T_ave', 1, 'T_ave (steps)', (0, np.nanmax(t) * 1.15), '{:.1f}')
    axes[0, j].set_title('({}) Time to finish — {}'.format('ab'[j], sub))
    bars(axes[1, j], st, 'L_ave', 1, 'L_ave (world units per drone)', (0, np.nanmax(l) * 1.15), '{:.0f}')
    axes[1, j].set_title('({}) Path length — {}'.format('cd'[j], sub))
fig.suptitle('Time and path length, successful episodes only (lower is better)', fontsize=11, y=1.0)
fig.tight_layout()
save(fig, 'fig2_time_path')

# ---- fig 3: alpha against tau -----------------------------------------------------------------------------
fig, axes = plt.subplots(1, 2, figsize=(12, 4.2), sharey=True)
xt = ['τ < 1\n(danger)', '1 ≤ τ < 2', '2 ≤ τ < 3', 'τ = 3\n(nothing ahead)']
show = [('fixed-weight-mappo', 'Fixed-weight MAPPO', GREY, '--', 's'),
        ('tau-rule-mappo', 'Hand-coded τ-rule MAPPO', MUTED, ':', '^'),
        ('mappo-pah', 'MAPPO + PAH (learned)', ACCENT, '-', 'o')]
for j, st in enumerate((2, 3)):
    ax = axes[j]
    for m, name, c, ls, mk in show:
        b = np.array([r['alpha_tau_bins'] for r in R if r['stage'] == st and r['method'] == m])
        mean = np.nanmean(b, axis=0)
        ax.plot(range(4), mean, ls=ls, marker=mk, color=c, lw=2, ms=8, label=name, zorder=3)
        if m == 'mappo-pah':
            for k in range(4):
                ax.scatter([k] * len(b), b[:, k], s=10, color=c, alpha=0.35, zorder=2, linewidths=0)
        if m != 'fixed-weight-mappo':             # label the danger-end value; PAH below, rule above
            dy = -14 if m == 'mappo-pah' else 12
            ax.annotate('{:.2f}'.format(mean[0]), (0, mean[0]), textcoords='offset points', xytext=(-22, dy),
                        va='center', fontsize=8.5, color=c if m == 'mappo-pah' else INK)
    ax.set_xticks(range(4)); ax.set_xticklabels(xt, fontsize=8.5); ax.set_ylim(0, 1)
    ax.set_title('({}) Stage {}'.format('ab'[j], st)); ax.set_xlim(-0.5, 3.3)
axes[0].set_ylabel('α  (weight on the mission reward)')
axes[0].legend(loc='lower right', fontsize=8.5, frameon=False)
fig.suptitle('What α each method uses as the hazard gets closer (τ = steps to the nearest collision; '
             'faint dots = PAH, each seed)', fontsize=11, y=1.02)
fig.tight_layout()
save(fig, 'fig3_alpha_by_tau')
print('figures written to', OUT)
