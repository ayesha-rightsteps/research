"""
compare_papers.py -- v4 Phase 3: our Phase 3 results next to the numbers the base papers report for the same kind of
experiment. Writes PNG (200 dpi) and SVG to output/figures/.

  p3_cmp1_density        : success vs obstacles, DA-MAPPO paper Table V (dynamic targets, ENV-1/2/3 = 30/40/50
                           obstacles, N = 3) next to ours (Stage 3, 8 drones, 30/40/50 discs)
  p3_cmp2_static_dynamic : success with moving targets minus success with static targets, paper (Table V minus
                           Table IV, mean of ENV-1/2/3) and ours (trained setting minus static, Stage 3)
  p3_cmp3_edges          : active edges vs swarm size, IGAT-MARL paper Table 1 next to ours (Stage 3)
  p3_cmp4_noise          : success change under sensor noise, DA-MAPPO paper Table IX next to ours (E6)

Paper numbers were read from the PDFs (bin/91 DA-MAPPO, IEEE IoT Journal 2026; bin/9 IGAT-MARL, Applied Soft
Computing 197 (2026) 115145) and are typed below exactly as printed. The papers give no seed spread, so their marks
carry no CI. Simulator, sensors, swarm size and training differ, so absolute values are not comparable; the shapes
(trends, order of methods, sign of a change) are what these figures compare.

Usage:  python compare_papers.py
"""
import os, sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import summarize as S
from figures import save, INK, MUTED, GRID, GREY, CAT        # same style as the Phase 3 figures (sets rcParams)

# DA-MAPPO paper, success % (Table IV static, Table V dynamic), ENV-1/2/3 = 30/40/50 obstacles, N = 3
PAPER_STATIC = {'DA-MAPPO': [99, 95, 92], 'MAPPO': [98, 92, 89], 'IPPO': [94, 91, 87]}
PAPER_DYNAMIC = {'DA-MAPPO': [99, 95, 90], 'MAPPO': [83, 70, 64], 'IPPO': [78, 57, 53]}
# DA-MAPPO paper Table IX (sensor noise on velocity / angular velocity, test time): baseline 95, then three levels
PAPER_NOISE = [95, 94, 94, 90]
# IGAT-MARL paper Table 1, average number of network edges, N = 3..10
IGAT_N = list(range(3, 11))
IGAT_EDGES = {'IGAT (paper)': [0.145, 2.114, 0.540, 0.711, 1.084, 1.461, 2.123, 2.422],
              'DGN benchmark (paper)': [0.183, 2.138, 1.654, 1.474, 2.742, 3.573, 3.892, 4.671]}

LINE = {'DA-MAPPO': dict(color=CAT[4], marker='v'), 'DA-MAPPO (2D)': dict(color=CAT[4], marker='v'),
        'MAPPO': dict(color=GREY, marker='<', ls='--'), 'IPPO': dict(color=GREY, marker='>', ls=':'),
        'MAPPO + PAH': dict(color=CAT[0], marker='o', lw=2.4)}


def end_label(ax, x, y, text, color):
    ax.annotate(text, (x, y), xytext=(6, 0), textcoords='offset points', va='center', fontsize=8.5, color=INK)


def cmp_density():
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.4), sharey=True)
    x = [30, 40, 50]
    ax = axes[0]
    for m, v in PAPER_DYNAMIC.items():
        ax.plot(x, v, lw=LINE[m].get('lw', 1.8), ms=7, markeredgecolor='white', **{k: w for k, w in LINE[m].items() if k != 'lw'})
        end_label(ax, 50, v[-1], m, LINE[m]['color'])
    ax.set_title('DA-MAPPO paper (Table V): 3 drones, 3D Gazebo', loc='left')
    ours = {'MAPPO + PAH': 'mappo-pah', 'DA-MAPPO (2D)': 'da-mappo-2d', 'MAPPO': 'mappo', 'IPPO': 'ippo'}
    ax = axes[1]
    for name, m in ours.items():
        lv = [(n, e) for n, e in S.DENSITY[3] if n in x]
        mu = [S.get(e, 3, m).mean() for _, e in lv]
        h = [S.half(S.get(e, 3, m)) for _, e in lv]
        st = LINE[name]
        ax.errorbar(x, mu, yerr=h, lw=st.get('lw', 1.8), ms=7, capsize=0, elinewidth=1, markeredgecolor='white',
                    **{k: w for k, w in st.items() if k != 'lw'})
    ax.legend(list(ours), frameon=False, fontsize=8.5, loc='upper right')
    ax.set_title('Ours (Stage 3): 8 drones, 2D, mean ± 95% CI', loc='left')
    for ax in axes:
        ax.set_xticks(x); ax.set_xticklabels(['30\n(ENV-1)', '40\n(ENV-2)', '50\n(ENV-3)'])
        ax.set_xlim(27, 58); ax.set_ylim(0, 100); ax.set_xlabel('Obstacles')
    axes[0].set_ylabel('Mission success (%)')
    fig.suptitle('Denser obstacles: every method falls in both studies (absolute levels are not comparable)',
                 x=0.01, ha='left', fontweight='bold')
    fig.tight_layout()
    save(fig, 'p3_cmp1_density')


def cmp_static_dynamic():
    names = ['DA-MAPPO', 'MAPPO', 'IPPO']
    paper = [np.mean(np.array(PAPER_DYNAMIC[m]) - np.array(PAPER_STATIC[m])) for m in names]
    keys = ['da-mappo-2d', 'mappo', 'ippo']
    ours = [S.paired(S.get(None, 3, k), S.get('static', 3, k)) for k in keys]
    fig, axes = plt.subplots(1, 2, figsize=(11, 3.8), sharey=True)
    y = np.arange(3)[::-1]
    ends = [None, [o[2] for o in ours]]
    for ax, vals, title, end in ((axes[0], paper, 'DA-MAPPO paper\n(Table V − Table IV, mean of ENV-1/2/3)', paper),
                                 (axes[1], [o[0] for o in ours], 'Ours, Stage 3\n(moving − static, line = paired 95% CI)',
                                  [o[2] for o in ours])):
        ax.barh(y, vals, height=0.5, color=[CAT[4], GREY, GREY], edgecolor='white')
        for yi, v, e in zip(y, vals, end):
            ax.annotate(S.f1(v, True), (e, yi), xytext=(-6 if v < 0 else 6, 0), textcoords='offset points',
                        va='center', ha='right' if v < 0 else 'left', fontsize=9, color=INK)
        ax.axvline(0, color=INK, lw=1); ax.set_xlim(-34, 16)
        ax.set_title(title, loc='left', fontsize=10); ax.grid(axis='y', visible=False)
        ax.set_xlabel('Success points (moving − static)')
    for yi, (d, lo, hi) in zip(y, ours):
        axes[1].plot([lo, hi], [yi, yi], color=INK, lw=1.2)
    axes[0].set_yticks(y); axes[0].set_yticklabels(['DA-MAPPO / DA-MAPPO (2D)', 'MAPPO', 'IPPO'])
    fig.suptitle('Static vs moving targets: the sign is opposite in the two studies\n'
                 'paper: targets swap places mid-mission; ours: targets drift continuously and the models were trained '
                 'on moving targets', x=0.01, ha='left', fontweight='bold', fontsize=11)
    fig.tight_layout()
    save(fig, 'p3_cmp2_static_dynamic')


def cmp_edges():
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.2))
    ax = axes[0]
    for (name, v), c, mk in zip(IGAT_EDGES.items(), (CAT[3], GREY), ('D', 's')):
        ax.plot(IGAT_N, v, color=c, marker=mk, lw=1.8, ms=6, markeredgecolor='white', label=name)
    ax.set_title('IGAT-MARL paper (Table 1): BlueSky air traffic', loc='left')
    ax.set_ylabel('Average network edges')
    ax = axes[1]
    for m, c, mk, name in (('igat-style', CAT[3], 'D', 'IGAT-style MAPPO (ours)'),
                           ('fixed-weight-mappo', CAT[1], 's', 'Fixed-weight MAPPO (ours)'),
                           ('mappo-pah', CAT[0], 'o', 'MAPPO + PAH (ours)')):
        v = [S.get(e, 3, m, 'active_edges_per_step').mean() for _, e in S.SWARM[3]]
        ax.plot(IGAT_N, v, color=c, marker=mk, lw=1.8, ms=6, markeredgecolor='white', label=name)
    ax.set_title('Ours (Stage 3 models): conflict-graph edges', loc='left')
    ax.set_ylabel('Active edges per step')
    for ax in axes:
        ax.set_xticks(IGAT_N); ax.set_xlabel('Drones (N)'); ax.set_ylim(0, None)
        ax.legend(frameon=False, fontsize=8.5, loc='upper left')
    fig.suptitle('Edges grow with swarm size in both studies (each panel has its own scale: the two papers count '
                 'edges differently)', x=0.01, ha='left', fontweight='bold', fontsize=11)
    fig.tight_layout()
    save(fig, 'p3_cmp3_edges')


def cmp_noise():
    fig, axes = plt.subplots(1, 2, figsize=(11, 3.9), sharey=True)
    lv = ['none', 'low', 'medium', 'high']
    ax = axes[0]
    d = np.array(PAPER_NOISE) - PAPER_NOISE[0]
    ax.plot(range(4), d, color=CAT[4], marker='v', lw=1.8, ms=7, markeredgecolor='white')
    end_label(ax, 3, d[-1], 'DA-MAPPO', CAT[4])
    ax.set_title('DA-MAPPO paper (Table IX): noise on velocity', loc='left')
    ax.set_xticklabels([])
    ax.set_xticks(range(4)); ax.set_xticklabels(['none\n(95%)', 'σv 0.2\nσω 0.05', 'σv 0.3\nσω 0.10', 'σv 0.5\nσω 0.15'])
    ax = axes[1]
    for name, m in (('MAPPO + PAH', 'mappo-pah'), ('DA-MAPPO (2D)', 'da-mappo-2d'), ('MAPPO', 'mappo'), ('IPPO', 'ippo')):
        base = S.get(None, 3, m)
        v = [S.get(e, 3, m).mean() - base.mean() for _, e in S.NOISE]
        st = LINE[name]
        ax.plot(range(4), v, lw=st.get('lw', 1.8), ms=7, markeredgecolor='white', **{k: w for k, w in st.items() if k != 'lw'})
    ax.legend(['MAPPO + PAH', 'DA-MAPPO (2D)', 'MAPPO', 'IPPO'], frameon=False, fontsize=8.5, loc='lower left')
    ax.set_xticks(range(4)); ax.set_xticklabels(['none', 'σ 0.02', 'σ 0.05', 'σ 0.1'])
    ax.set_title('Ours (Stage 3): noise on LiDAR distances', loc='left')
    for ax in axes:
        ax.axhline(0, color=INK, lw=1); ax.set_ylim(-8, 3); ax.set_xlim(-0.3, 3.8)
    axes[0].set_ylabel('Success change from no noise (points)')
    fig.suptitle('Sensor noise: small drops in both studies', x=0.01, ha='left', fontweight='bold')
    fig.tight_layout()
    save(fig, 'p3_cmp4_noise')


if __name__ == '__main__':
    cmp_density(); cmp_static_dynamic(); cmp_edges(); cmp_noise()
    print('comparison figures ->', os.path.join(HERE, 'output', 'figures'))
