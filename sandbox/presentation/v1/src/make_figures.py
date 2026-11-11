"""Two figures that did not exist before deck v1.

  env_illustration.png   a real Stage 3 layout from env_v4 (8 drones, 20 discs): assignment lines + one LiDAR fan
  v3_alpha_tie.png       the v3 study with full method names (the old figure used the short names B4 / H / M)

Run (needs numpy, matplotlib, scipy, torch for the env import):
    python make_figures.py            # from presentation/v1/src
Numbers are parsed from the v3 result tables; nothing is typed by hand.
"""
import os, re, sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle

HERE = os.path.dirname(os.path.abspath(__file__))
SAND = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
V4 = os.path.join(SAND, 'code', 'notebooks', 'v4')
V3T = os.path.join(SAND, 'code', 'notebooks', 'v3', 'results-table', 'output')
OUT = os.path.join(HERE, '..', 'images')
sys.path.insert(0, os.path.join(V4, 'common'))

BLUE, LIGHT, GREY, ORANGE, INK = '#2A78D6', '#9DC0EC', '#B5B3AC', '#EC6A36', '#1F2A37'
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 13, 'axes.edgecolor': INK, 'text.color': INK})


def env_illustration():
    import env_v4 as E
    best = None
    for seed in range(1, 60):                                    # pick a layout with a lively LiDAR fan
        env = E.MultiUAVEnvV4(n_drones=8, n_obstacles=20, seed=seed)
        env.reset()
        for i in range(env.n):
            p = env.drone_pos[i].astype(np.float64)
            if not (120 < p[0] < 380 and 120 < p[1] < 380):
                continue
            d = E.ray_distances(p, env.obstacle_pos.astype(np.float64), env.obs_r, env.W)
            hits = int((d < E.RAY_RANGE - 1e-6).sum())
            if best is None or hits > best[0]:
                best = (hits, seed, i)
    hits, seed, k = best
    env = E.MultiUAVEnvV4(n_drones=8, n_obstacles=20, seed=seed)
    env.reset()
    fig, ax = plt.subplots(figsize=(7.2, 7.2), dpi=200)
    ax.add_patch(Rectangle((0, 0), env.W, env.W, fc='#F6F6F4', ec=INK, lw=1.4))
    for c in env.obstacle_pos:
        ax.add_patch(Circle(c, env.obs_r, fc='#8D8B84', ec='white', lw=0.8, zorder=2))
    p = env.drone_pos[k].astype(np.float64)
    d = E.ray_distances(p, env.obstacle_pos.astype(np.float64), env.obs_r, env.W)
    for ang, dist in zip(np.arange(E.N_RAYS) * 2 * np.pi / E.N_RAYS, d):
        end = p + dist * np.array([np.cos(ang), np.sin(ang)])
        ax.plot([p[0], end[0]], [p[1], end[1]], color=BLUE, lw=0.9, alpha=0.55, zorder=3)
        if dist < E.RAY_RANGE - 1e-6:
            ax.plot(*end, 'o', ms=3.2, color=ORANGE, zorder=4)
    ax.add_patch(Circle(p, E.RAY_RANGE, fc='none', ec=BLUE, lw=0.8, ls=(0, (4, 4)), alpha=0.6, zorder=3))
    for i in range(env.n):
        t = env.target_pos[env.assignment[i]]
        ax.plot([env.drone_pos[i][0], t[0]], [env.drone_pos[i][1], t[1]], color=INK, lw=0.9, ls=(0, (3, 3)),
                alpha=0.55, zorder=3)
        ax.plot(*t, 'D', ms=11, color=ORANGE, mec='white', mew=1.0, zorder=5)
        ax.text(t[0] + 15, t[1] + 1, str(i + 1), ha='left', va='center', fontsize=10.5, color=ORANGE,
                fontweight='bold', zorder=6)
        ax.plot(*env.drone_pos[i], 'o', ms=13, color=BLUE, mec='white', mew=1.2, zorder=6)
        ax.text(env.drone_pos[i][0], env.drone_pos[i][1], str(i + 1), ha='center', va='center', fontsize=8.5,
                color='white', fontweight='bold', zorder=7)
    ax.set_xlim(-8, env.W + 8); ax.set_ylim(-8, env.W + 8); ax.set_aspect('equal'); ax.axis('off')
    from matplotlib.lines import Line2D
    h = [Line2D([], [], marker='o', ls='', color=BLUE, mec='white', ms=10, label='drone'),
         Line2D([], [], marker='D', ls='', color=ORANGE, mec='white', ms=9, label='target of the drone with that number (moves)'),
         Line2D([], [], marker='o', ls='', color='#8D8B84', ms=10, label='obstacle disc'),
         Line2D([], [], color=BLUE, lw=1.2, alpha=0.7, label='24 LiDAR rays (drone %d)' % (k + 1)),
         Line2D([], [], color=INK, lw=1.0, ls=(0, (3, 3)), alpha=0.6, label='Hungarian assignment')]
    ax.legend(handles=h, loc='upper center', bbox_to_anchor=(0.5, -0.005), ncol=3, frameon=False, fontsize=10.5,
              handletextpad=0.4, columnspacing=1.2)
    fig.savefig(os.path.join(OUT, 'env_illustration.png'), bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print('env_illustration: seed', seed, 'drone', k + 1, 'rays hitting a disc:', hits)


def parse_pm(cell):
    m = re.findall(r'-?\d+\.\d+', cell)
    return [float(x) for x in m]


def v3_chart():
    rows2, rows3 = {}, {}
    for line in open(os.path.join(V3T, 'table_stage2.md')):
        if line.startswith('| ') and 'R_success' not in line and '---' not in line:
            c = [x.strip() for x in line.strip().strip('|').split('|')]
            rows2[c[0]] = parse_pm(c[1])                       # mean, std over 5 seeds
    for line in open(os.path.join(V3T, 'table_stage3.md')):
        if line.startswith('| ') and 'R_success' not in line and '---' not in line:
            c = [x.strip() for x in line.strip().strip('|').split('|')]
            rows3[c[0]] = parse_pm(c[1])                       # mean, lo, hi (95% CI)
    names2 = [('B4 (fixed alpha)', 'Fixed-weight\nMAPPO', LIGHT), ('H (tau-formula)', 'Hand-coded\nτ-rule MAPPO', LIGHT),
              ('M (PAH residual)', 'MAPPO + PAH\n(first version)', BLUE)]
    names3 = [('B4 (fixed alpha)', 'Fixed-weight\nMAPPO', LIGHT), ('M (PAH residual)', 'MAPPO + PAH\n(first version)', BLUE),
              ('M, no Hungarian', 'MAPPO + PAH,\nno assignment', ORANGE)]
    fig, axs = plt.subplots(1, 2, figsize=(13, 5.2), dpi=200, gridspec_kw={'wspace': 0.12})
    for ax, names, rows, title, ci in [(axs[0], names2, rows2, 'Stage 2: 5 drones, 5 obstacles', False),
                                       (axs[1], names3, rows3, 'Stage 3: 8 drones, 10 obstacles', True)]:
        for x, (key, lab, col) in enumerate(names):
            v = rows[key]
            ax.bar(x, v[0], width=0.62, color=col, zorder=2)
            err = ([[v[0] - v[1]], [v[2] - v[0]]] if ci else [[v[1]], [v[1]]])
            ax.errorbar(x, v[0], yerr=err, color=INK, capsize=5, lw=1.6, zorder=3)
            top = (v[2] if ci else v[0] + v[1])
            ax.text(x, top + 2.0, '%.1f' % v[0], ha='center', va='bottom', fontsize=15, fontweight='bold')
        ax.set_xticks(range(3)); ax.set_xticklabels([n[1] for n in names], fontsize=12)
        ax.set_ylim(0, 108); ax.set_title(title, loc='left', fontsize=14, fontweight='bold')
        ax.grid(axis='y', color='#E3E3E0', zorder=0); ax.set_axisbelow(True)
        for s in ('top', 'right'):
            ax.spines[s].set_visible(False)
    axs[0].set_ylabel('Mission success (%)', fontsize=13)
    axs[1].set_yticklabels([])
    fig.text(0.01, -0.02, 'Version 3 environment (point obstacles, four-direction sensing). Stage 2: mean ± std over 5 seeds. '
             'Stage 3: one seed, 95% CI over 200 test episodes.', fontsize=10.5, color='#555', ha='left')
    fig.savefig(os.path.join(OUT, 'v3_alpha_tie.png'), bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print('v3_alpha_tie:', rows2, rows3)


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    env_illustration()
    v3_chart()
