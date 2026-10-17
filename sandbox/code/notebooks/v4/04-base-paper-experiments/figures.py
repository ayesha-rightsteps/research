"""
figures.py -- v4 Phase 3 figures (white background, same style as 03-base-paper-baselines/figures.py), from the
Phase 3 evaluation JSON via summarize.py. Writes PNG (200 dpi) and SVG to output/figures/.

  p3_fig1_density          : success vs number of obstacle discs, Stage 2 and Stage 3 (DA-MAPPO ENV-1/2/3 style)
  p3_fig2_pah_lead         : MAPPO + PAH minus Fixed-weight MAPPO in every Phase 3 setting, 95% Welch CI
                             (the main Phase 3 question: does the lead hold when the setting changes?)
  p3_fig3_static           : moving targets (trained) vs static targets, every method
  p3_fig4_assign50         : assignment every step (trained) vs every 50 steps
  p3_fig5_swarm            : success vs swarm size 3-10 (IGAT-MARL style)
  p3_fig6_swarm_los        : loss of separation per episode vs swarm size (IGAT-MARL metric)
  p3_fig7_noise            : success vs LiDAR noise, Stage 3
  p3_fig8_timing           : decision time per step vs swarm size

Colour: five fixed categorical slots (validated reference palette, as Phase 2) for the methods named in most
figures; the other methods are grey with their own marker and are in the legend. Lines = mean over 10 seeds,
band = 95% CI. Vertical dotted line = the setting the models were trained in.

Usage:  python figures.py
"""
import os, sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import summarize as S                                   # get(), half(), welch, paired, levels, NAMES

OUT = os.path.join(HERE, 'output', 'figures')
INK, MUTED, GRID, GREY = '#0b0b0b', '#52514e', '#e4e3df', '#9a9993'
CAT = ['#2a78d6', '#eb6834', '#1baf7a', '#eda100', '#e87ba4']
COLOR = {'mappo-pah': CAT[0], 'fixed-weight-mappo': CAT[1], 'tau-rule-mappo': CAT[2], 'igat-style': CAT[3],
         'da-mappo-2d': CAT[4]}
MARKER = {'mappo-pah': 'o', 'fixed-weight-mappo': 's', 'tau-rule-mappo': '^', 'igat-style': 'D', 'da-mappo-2d': 'v',
          'mappo-pah-no-hungarian': 'P', 'plain-mappo': 'X', 'mappo': '<', 'ippo': '>'}
NAMES = dict(S.NAMES, **{'mappo-pah-no-hungarian': 'MAPPO + PAH (Hungarian off)'})

plt.rcParams.update({
    'figure.facecolor': 'white', 'axes.facecolor': 'white', 'savefig.facecolor': 'white',
    'font.family': 'DejaVu Sans', 'font.size': 10, 'axes.titlesize': 11, 'axes.titleweight': 'bold',
    'axes.labelsize': 10, 'axes.spines.top': False, 'axes.spines.right': False, 'axes.grid': True,
    'axes.axisbelow': True, 'grid.color': GRID, 'grid.linewidth': 0.8, 'axes.edgecolor': MUTED,
    'xtick.color': MUTED, 'ytick.color': INK, 'axes.labelcolor': INK, 'text.color': INK,
})


def save(fig, name):
    os.makedirs(OUT, exist_ok=True)
    fig.savefig(os.path.join(OUT, name + '.png'), dpi=200, bbox_inches='tight')
    fig.savefig(os.path.join(OUT, name + '.svg'), bbox_inches='tight')
    plt.close(fig)


def style(m):
    """Coloured, thicker line for the five named methods; thin grey line for the others."""
    if m in COLOR:
        return dict(color=COLOR[m], lw=2.2 if m == 'mappo-pah' else 1.8, ms=6, zorder=4 if m == 'mappo-pah' else 3)
    return dict(color=GREY, lw=1.1, ms=5, zorder=2, ls='--')


def sweep(ax, levels, methods, st, field='success', band=True):
    """One line per method over the levels of an experiment (x = level value)."""
    x = [v for v, _ in levels]
    for m in methods:
        vals = [S.get(e, st, m, field) for _, e in levels]
        mu = np.array([v.mean() for v in vals])
        kw = style(m)
        ax.plot(x, mu, marker=MARKER[m], label=NAMES[m], markeredgecolor='white', markeredgewidth=0.8, **kw)
        if band and m in COLOR:
            h = np.array([S.half(v) for v in vals])
            ax.fill_between(x, mu - h, mu + h, color=kw['color'], alpha=0.12, lw=0, zorder=1)


def trained_line(ax, x):
    ax.axvline(x, color=MUTED, lw=1, ls=':', zorder=0)
    ax.annotate('trained', (x, 1.0), xycoords=('data', 'axes fraction'), xytext=(3, -4), textcoords='offset points',
                ha='left', va='top', fontsize=8, color=MUTED)


def legend_below(fig, ax, ncol=3):
    h, l = ax.get_legend_handles_labels()
    fig.legend(h, l, loc='lower center', ncol=ncol, frameon=False, fontsize=9, bbox_to_anchor=(0.5, -0.02))


def fig_density():
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.6), sharey=True)
    for ax, st in zip(axes, (2, 3)):
        sweep(ax, S.DENSITY[st], S.ALL, st)
        trained_line(ax, S.TRAINED_OBST[st])
        ax.set_title('Stage {} ({} drones)'.format(st, S.TRAINED_N[st]), loc='left')
        ax.set_xlabel('Obstacle discs in the test world')
        ax.set_xticks([10, 20, 30, 40, 50]); ax.set_ylim(0, 100)
    axes[0].set_ylabel('Mission success (%)')
    fig.suptitle('Success as obstacles get denser (models trained on 10 / 20 discs)', x=0.01, ha='left', fontweight='bold')
    fig.tight_layout(rect=(0, 0.13, 1, 1))
    legend_below(fig, axes[0])
    save(fig, 'p3_fig1_density')


def fig_lead():
    """PAH - Fixed-weight in every setting, one row each, both stages side by side."""
    rows = {2: [], 3: []}
    for st in (2, 3):
        rows[st].append(('Trained setting', None))
        rows[st] += [('{} discs'.format(n), e) for n, e in S.DENSITY[st] if e]
        rows[st] += [('Static targets', 'static'), ('Assignment every 50', 'assign50')]
        rows[st] += [('N = {} drones'.format(n), e) for n, e in S.SWARM[st] if e]
    rows[3] += [('LiDAR noise σ = {:g}'.format(s), e) for s, e in S.NOISE if e]
    fig, axes = plt.subplots(1, 2, figsize=(11, 7.2), sharex=True)
    for ax, st in zip(axes, (2, 3)):
        lab = [r[0] for r in rows[st]]
        y = np.arange(len(lab))[::-1]
        for yi, (_, e) in zip(y, rows[st]):
            d, lo, hi = S.welch(S.get(e, st, 'mappo-pah'), S.get(e, st, 'fixed-weight-mappo'))
            c = CAT[0] if lo > 0 else MUTED
            ax.plot([lo, hi], [yi, yi], color=c, lw=2, solid_capstyle='round')
            ax.plot(d, yi, 'o', color=c, ms=7, markeredgecolor='white', markeredgewidth=1, zorder=3)
            ax.annotate(S.f1(d, True), (hi, yi), xytext=(5, 0), textcoords='offset points', va='center', fontsize=8,
                        color=MUTED)
        ax.axvline(0, color=INK, lw=1)
        ax.set_yticks(y); ax.set_yticklabels(lab, fontsize=9); ax.grid(axis='y', visible=False)
        ax.set_title('Stage {}'.format(st), loc='left')
        ax.set_xlabel('MAPPO + PAH − Fixed-weight MAPPO (success points)')
        ax.set_xlim(-5, 28)
    fig.suptitle('Does MAPPO + PAH stay ahead of Fixed-weight MAPPO when the test setting changes?\n'
                 'dot = mean difference over 10 seeds, line = 95% Welch CI; blue = CI entirely above 0',
                 x=0.01, ha='left', fontweight='bold', fontsize=11)
    fig.tight_layout()
    save(fig, 'p3_fig2_pah_lead')


def dumbbell(ax, methods, st, exp, name):
    y = np.arange(len(methods))[::-1]
    for yi, m in zip(y, methods):
        a, b = S.get(None, st, m).mean(), S.get(exp, st, m).mean()
        ax.plot([a, b], [yi, yi], color=GRID, lw=3, zorder=1, solid_capstyle='round')
        ax.plot(a, yi, 'o', color=INK, ms=7, zorder=3, label='Trained setting' if yi == y[0] else None)
        ax.plot(b, yi, 'o', color=CAT[1], ms=7, zorder=3, markeredgecolor='white', label=name if yi == y[0] else None)
        d, lo, hi = S.paired(S.get(exp, st, m), S.get(None, st, m))
        ax.annotate('{} {}'.format(S.f1(d, True), S.mark(lo, hi)), (max(a, b), yi), xytext=(8, 0),
                    textcoords='offset points', va='center', fontsize=8, color=MUTED)
    ax.set_yticks(y); ax.set_yticklabels([NAMES[m] for m in methods], fontsize=9); ax.grid(axis='y', visible=False)
    ax.set_xlim(0, 105); ax.set_xlabel('Mission success (%)')
    ax.set_title('Stage {}'.format(st), loc='left')


def fig_two_setting(exp, methods, name, title, fname):
    fig, axes = plt.subplots(1, 2, figsize=(11, 0.45 * len(methods) + 2.2), sharey=True)
    for ax, st in zip(axes, (2, 3)):
        dumbbell(ax, methods, st, exp, name)
    fig.suptitle(title + '\nnumber = paired change over the 10 seeds; ▼ / ▲ CI below / above 0, · not settled',
                 x=0.01, ha='left', fontweight='bold', fontsize=11)
    fig.tight_layout(rect=(0, 0.06, 1, 1))
    h, l = axes[0].get_legend_handles_labels()
    fig.legend(h, l, loc='lower center', ncol=2, frameon=False, fontsize=9)
    save(fig, fname)


def fig_swarm(field, ylabel, title, fname, ylim=None):
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.4), sharey=True)
    for ax, st in zip(axes, (2, 3)):
        sweep(ax, S.SWARM[st], S.E4_METHODS, st, field, band=(field == 'success'))
        trained_line(ax, S.TRAINED_N[st])
        ax.set_title('Stage {} models (trained on {} drones, {} discs)'.format(st, S.TRAINED_N[st], S.TRAINED_OBST[st]),
                     loc='left')
        ax.set_xlabel('Drones in the test world (N)'); ax.set_xticks(range(3, 11))
        if ylim:
            ax.set_ylim(*ylim)
    axes[0].set_ylabel(ylabel)
    fig.suptitle(title, x=0.01, ha='left', fontweight='bold')
    fig.tight_layout(rect=(0, 0.09, 1, 1))
    legend_below(fig, axes[0], ncol=5)
    save(fig, fname)


def fig_noise():
    fig, ax = plt.subplots(figsize=(7.5, 5))
    sweep(ax, S.NOISE, S.ALL, 3)
    ax.set_xticks([s for s, _ in S.NOISE]); ax.set_xticklabels(['0 (trained)', '0.02', '0.05', '0.1'])
    ax.set_xlabel('LiDAR noise σ (fraction of the ray range)'); ax.set_ylabel('Mission success (%)'); ax.set_ylim(0, 100)
    ax.set_title('Stage 3: success with noisy LiDAR (trained without noise)', loc='left')
    fig.tight_layout(rect=(0, 0.17, 1, 1))
    legend_below(fig, ax)
    save(fig, 'p3_fig7_noise')


def fig_timing():
    fig, ax = plt.subplots(figsize=(7.5, 4.4))
    sweep(ax, S.TIMING, S.TIMING_METHODS, 3, 'decision_ms')
    ax.set_xlabel('Drones (N)'); ax.set_xticks(range(3, 11)); ax.set_ylabel('ms per decision step (whole swarm)')
    ax.set_ylim(0, None)
    ax.set_title('Decision time per step (actor only, 1 CPU thread, laptop)', loc='left')
    ax.legend(frameon=False, fontsize=9, loc='center right')
    fig.tight_layout()
    save(fig, 'p3_fig8_timing')


def main():
    fig_density()
    fig_lead()
    fig_two_setting('static', S.ALL, 'Static targets', 'Moving targets (trained) vs static targets', 'p3_fig3_static')
    fig_two_setting('assign50', S.E3_METHODS, 'Assignment every 50 steps',
                    'Assignment every step (trained) vs every 50 steps', 'p3_fig4_assign50')
    fig_swarm('success', 'Mission success (%)', 'Success as the swarm size changes (models used as trained)',
              'p3_fig5_swarm', (0, 100))
    fig_swarm('los_per_episode', 'Loss of separation per episode',
              'Loss of separation vs swarm size (IGAT-MARL metric; lower is safer)', 'p3_fig6_swarm_los')
    fig_noise()
    fig_timing()
    print('figures ->', OUT)


if __name__ == '__main__':
    main()
