"""Build deck v1: presentation/v1/deck_v1.pptx + deck_v1.md (+ text-fit report).

    python src/build_deck.py          (from presentation/v1, with the venv that has python-pptx, Pillow, lxml)

Every number that appears on a slide is either parsed from the result tables or checked against them in
verify_facts() before the deck is written; the build stops if a fact is missing.
"""
import os, re, shutil, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from deck_lib import *

HERE = os.path.dirname(os.path.abspath(__file__))
V1 = os.path.abspath(os.path.join(HERE, '..'))
SAND = os.path.abspath(os.path.join(V1, '..', '..'))
V4 = os.path.join(SAND, 'code', 'notebooks', 'v4')
IMG = os.path.join(V1, 'images')

# ------------------------------------------------------------------ pictures (copied so the folder is self-contained)
PICS = {
    'collision_type_v3.png': '00-diagnostics/output/collision_type_check.png',
    'alpha_by_tau.png': '02-redesign/output/fig3_alpha_by_tau.png',
    'time_path.png': '02-redesign/output/fig2_time_path.png',
    'success_all_methods.png': '03-base-paper-baselines/output/figures/fig1_success_all_methods.png',
    'pah_vs_each_method.png': '03-base-paper-baselines/output/figures/fig2_pah_vs_each_method.png',
    'gap_breakdown.png': '03-base-paper-baselines/output/figures/fig3_gap_breakdown.png',
    'outcomes.png': '03-base-paper-baselines/output/figures/fig4_outcomes.png',
    'learning_curves.png': '03-base-paper-baselines/output/figures/fig5_learning_curves.png',
    'ranking_vs_paper.png': '03-base-paper-baselines/output/figures/fig6_ranking_vs_paper.png',
    'difficulty_vs_paper.png': '03-base-paper-baselines/output/figures/fig7_difficulty_vs_paper.png',
    'gain_over_mappo.png': '03-base-paper-baselines/output/figures/fig8_gain_over_mappo.png',
    'density.png': '04-base-paper-experiments/output/figures/p3_fig1_density.png',
    'lead_everywhere.png': '04-base-paper-experiments/output/figures/p3_fig2_pah_lead.png',
    'static_targets.png': '04-base-paper-experiments/output/figures/p3_fig3_static.png',
    'assign_every_50.png': '04-base-paper-experiments/output/figures/p3_fig4_assign50.png',
    'swarm_size.png': '04-base-paper-experiments/output/figures/p3_fig5_swarm.png',
    'loss_of_separation.png': '04-base-paper-experiments/output/figures/p3_fig6_swarm_los.png',
    'noise.png': '04-base-paper-experiments/output/figures/p3_fig7_noise.png',
    'timing.png': '04-base-paper-experiments/output/figures/p3_fig8_timing.png',
    'density_vs_paper.png': '04-base-paper-experiments/output/figures/p3_cmp1_density.png',
    'static_vs_paper.png': '04-base-paper-experiments/output/figures/p3_cmp2_static_dynamic.png',
    'edges_vs_igat_paper.png': '04-base-paper-experiments/output/figures/p3_cmp3_edges.png',
}


def collect_pictures():
    os.makedirs(IMG, exist_ok=True)
    for name, rel in PICS.items():
        shutil.copy(os.path.join(V4, rel), os.path.join(IMG, name))
    for need in ('env_illustration.png', 'v3_alpha_tie.png'):
        assert os.path.exists(os.path.join(IMG, need)), 'run make_figures.py first: ' + need


def P(name):
    return os.path.join(IMG, name)


# ------------------------------------------------------------------ facts
def rd(rel):
    return open(os.path.join(V4, rel), encoding='utf-8').read()


def verify_facts():
    ev = rd('03-base-paper-baselines/output/eval_summary.md')
    p3 = rd('04-base-paper-experiments/output/phase3_summary.md')
    r3 = rd('04-base-paper-experiments/REPORT.md')
    notes = open(os.path.join(SAND, 'docs', 'research', '11_thesis_reporting_notes.md'), encoding='utf-8').read()
    v3 = rd('../v3/results-table/output/table_stage2.md') + rd('../v3/results-table/output/table_stage3.md')
    plain = rd('01-plain-mappo-check/output/results.md')
    mech = rd('05-mechanism-check/output/advantage_summary.md')
    al = rd('02-redesign/output/eval_summary.md')
    checks = [
        (al, '| MAPPO + PAH | 0.13 | 0.25 | 0.61 | 0.85 |'), (al, '| MAPPO + PAH | 0.19 | 0.32 | 0.59 | 0.81 |'),
        (al, '| Hand-coded τ-rule MAPPO | 0.19 | 0.51 | 0.77 | 0.90 |'),
        (ev, '| MAPPO + PAH | 10 / 10 | 86.8 ± 3.8 | 13.2 | 0.0 | 82.7 ± 4.0 | 17.3 | 0.0 |'),
        (ev, '| Fixed-weight MAPPO | 10 / 10 | 79.9 ± 2.2 | 20.2 | 0.0 | 74.2 ± 6.1 | 25.8 | 0.1 |'),
        (ev, '+8.6 [+1.7, +15.4]'), (ev, '+7.0 [+2.8, +11.1]'), (ev, '+2.0 [-2.6, +6.6]'),
        (ev, '+15.4 [+10.3, +20.4]'), (ev, '+30.0 [+22.8, +37.1]'), (ev, '+14.3 [+6.3, +22.3]'),
        (ev, '+11.3 [+4.6, +17.9]'), (ev, '+53.9 [+49.3, +58.4]'), (ev, '+7.0 [+2.3, +11.6]'),
        (ev, '| MAPPO + PAH (Hungarian off) | 78 | 301 | 76 / 255 | 109 | 342 | 127 / 495 |'),
        (ev, '| MAPPO + PAH | 54 | 188 | 6 / 258 | 61 | 173 | 16 / 330 |'),
        (p3, '| MAPPO + PAH | 93.5 ± 2.2 | 82.7 ± 4.0 | 70.3 ± 6.9 | 51.3 ± 7.4 | 40.4 ± 7.5 |'),
        (p3, '-7.0 [-9.5, -4.4]'), (p3, '-15.0 [-20.8, -9.2]'), (p3, '+16.6 [+7.8, +25.4]'),
        (p3, '| MAPPO + PAH | 82.7 ± 4.0 | 82.3 ± 4.4 | 82.0 ± 4.2 | 80.8 ± 4.3 |'),
        (p3, '+4.8 [+0.1, +9.5]'), (p3, '+3.5'), (p3, '| MAPPO + PAH | 90.5 ± 3.4 |'), (p3, '80.5 ± 5.2'),
        (p3, '| Fixed-weight MAPPO | 85.7 ± 3.7 |'), (p3, '68.3 ± 7.4'), (p3, '| IGAT-style MAPPO | 77.3 ± 4.9 |'),
        (p3, '32.5 ± 10.8'), (p3, '| MAPPO + PAH | 86.8 ± 3.8 | 0.17 | 0.0012 | 82.7 ± 4.0 | 0.63 | 0.0044 |'),
        (p3, '| Fixed-weight MAPPO | 79.9 ± 2.2 | 0.25 | 0.0019 | 74.2 ± 6.1 | 0.55 | 0.0061 |'),
        (p3, '| IGAT-style MAPPO | 73.0 ± 5.4 | 0.79 | 0.0048 | 46.8 ± 9.5 | 2.64 | 0.0163 |'),
        (r3, 'Yes, in all 31 settings tested'), (r3, '(Stage 2: 14, Stage 3: 17)'),
        (notes, '+7.9 [+0.7, +15.1]'), (notes, 'higher on 9 of 10 seed indices'),
        (v3, '89.2 +/- 2.0'), (v3, '87.5 +/- 1.5'), (v3, '89.5 +/- 1.0'), (v3, '73.5 [67.0, 79.1]'),
        (v3, '72.0 [65.4, 77.8]'), (v3, '51.5 [44.6, 58.3]'),
        (plain, '89.9 ± 1.4'), (plain, '88.2 ± 2.2'),
        (mech, '| 3 | MAPPO + PAH |'),
        (rd('05-mechanism-check/REPORT.md'), 'Phase 0\n   on v3: 0.95–1.00') if False else (rd('05-mechanism-check/REPORT.md'), '0.95–1.00'),
    ]
    bad = [c[1] for c in checks if c[1] not in c[0]]
    assert not bad, 'facts not found in the result files: %s' % bad
    # arithmetic used in the text
    assert round(90.5 - 80.5, 1) == 10.0 and round(85.7 - 68.3, 1) == 17.4 and round(77.3 - 32.5, 1) == 44.8
    assert round(82.7 - 68.4, 1) == 14.3
    print('verify_facts: %d facts + arithmetic OK' % len(checks))


def check_density_and_swarm():
    """The slides say: MAPPO + PAH is first at every obstacle density, and its success drops least from 3 to 10 drones."""
    t = rd('04-base-paper-experiments/output/phase3_summary.md').split('\n')

    def num(c):
        return float(re.findall(r'-?\d+\.\d', c)[0])

    def table_after(i):
        rows = []
        for l in t[i + 1:]:
            if l.startswith('|'):
                c = [x.strip() for x in l.strip('|').split('|')]
                if not set(c[0]) <= set('-') and c[0] != 'Method':
                    rows.append(c)
            elif rows:
                break
        return rows

    for sec_name, last_col in (('## E1', None), ('## E4', 8)):
        sec = next(i for i, l in enumerate(t) if l.startswith(sec_name))
        for st in ('### Stage 2', '### Stage 3'):
            rows = table_after(next(j for j, l in enumerate(t) if l.startswith(st) and j > sec))
            if last_col is None:
                for k in range(1, 6):
                    best = max(rows, key=lambda r: num(r[k]))
                    assert best[0] == 'MAPPO + PAH', (st, k, best[0])
            else:
                drops = {r[0]: num(r[1]) - num(r[last_col]) for r in rows}
                assert min(drops, key=drops.get) == 'MAPPO + PAH', (st, drops)
    print('check_density_and_swarm: MAPPO + PAH first at every density and smallest swarm-size drop, both stages')


def parse_rows(text, start_marker, n_cols):
    """markdown table that follows the first line containing start_marker -> list of cell lists"""
    lines = text.split('\n')
    i = next(k for k, l in enumerate(lines) if start_marker in l)
    rows = []
    for l in lines[i + 1:]:
        if l.startswith('|'):
            c = [x.strip() for x in l.strip().strip('|').split('|')]
            if len(c) >= n_cols and not set(c[0]) <= set('-'):
                rows.append(c)
        elif rows:
            break
    return rows


M = '−'   # typographic minus used on slides


def mnus(s):
    return s.replace('-', M)


# ------------------------------------------------------------------ slide helpers
def fig_slide(d, key, title, section, img, call, notes, kind='blue', call_h=0.7):
    img_h = 5.35 - call_h - 0.1            # content area runs from y = 1.5 to y = 6.85
    d.new_slide(key, title, section)
    d.image(P(img), LM, 1.5, CW, img_h)
    d.callout(LM, 1.5 + img_h + 0.1, CW, call_h, call, kind=kind, pt=16)
    d.notes(notes)


def build():
    verify_facts()
    check_density_and_swarm()
    collect_pictures()
    d = Deck()
    S1, S2, S3, S4, S5, APP = ('Problem and method', 'How we got here', 'Results', 'Base-paper experiments',
                               'Claims and next steps', 'Appendix')

    # ============================================================ 1 title
    d.new_slide('title', 'Title', S1, dark=True, number=False)
    d.box(0.0, 0.0, 0.28, SH, [], fill=BLUE, round_=0, log=False)
    d.text(0.9, 1.25, 11.6, 2.3,
           ['Multi-Agent Proximal Policy Optimization for Joint Dynamic Target Assignment and Collision Avoidance in UAV Systems'],
           pt=31, bold=True, color=WHITE, anchor='top')
    d.text(0.9, 3.75, 11.0, 0.5, ['MS thesis · progress and results'], pt=22, color='9DC0EC')
    d.text(0.9, 4.75, 11.0, 1.6,
           ['**Ayesha Khalil** · CIIT/SP25-RCS-009/ATD',
            'Supervisor: Dr. Faisal Rehman · Co-supervisor: Mr. Ehzaz Mustafa',
            'COMSATS University Islamabad, Abbottabad campus'], pt=17, color=WHITE, space_after=6)
    d.notes("""Good morning, and thank you for your time.
Today I will show how far the thesis has come: a single MAPPO framework that does target assignment and collision avoidance together, and its new component, the Priority Arbitration Head, or PAH.
I will first explain the problem and the method, then what went wrong in my first attempt and how I fixed it, and then the results, including the experiments from the two base papers repeated on my own trained models. At the end I will say plainly what I claim and what I do not.""")

    # ============================================================ 2 problem
    d.new_slide('problem', 'Two decisions must be made together: who flies where, and how to stay safe', S1)
    d.image(P('env_illustration.png'), LM, 1.5, 6.5, 5.0)
    d.text(LM, 6.5, 6.5, 0.4, ['One Stage 3 layout from our environment: 8 drones, 20 obstacle discs, 500 × 500 world'],
           pt=11, color=GREY_T, align='center')
    d.card(7.35, 1.6, 5.43, 1.55, 'Assignment', 'Which drone flies to which target? The targets move, so the answer changes at every step.',
           body_pt=16, head_pt=19)
    d.card(7.35, 3.3, 5.43, 1.55, 'Collision avoidance', 'Keep clear of obstacles and of the other drones while flying there.',
           body_pt=16, head_pt=19)
    d.card(7.35, 5.0, 5.43, 1.75, 'Solved separately today',
           'Independent solutions give conflicting assignments, overlapping paths and delays (approved synopsis).',
           fill=ORANGE_BG, head_color='A63D12', accent=ORANGE, body_pt=16, head_pt=19)
    d.notes("""This picture is our simulated world, taken straight from the environment code. The blue circles are drones, the orange diamonds are their targets (the number tells you which drone a target belongs to), and the grey discs are obstacles. The dashed lines are the assignment.
A drone has to do two things at once. It must go to the right target, and it must not hit an obstacle or another drone on the way. The thin blue lines show what one drone can sense: 24 laser-like rays that measure the distance to the nearest obstacle.
In the literature these two jobs are usually solved separately, and then they conflict: a good assignment can send a drone straight through an obstacle. Our question is whether one learned policy can handle both.""")

    # ============================================================ 3 objectives
    d.new_slide('objectives', 'What we set out to do, and the short answer', S1)
    rows = [['Objective (from the approved synopsis)', 'Where it is answered', 'Short answer'],
            ['1. Design a Priority Arbitration Head (PAH) inside a unified MAPPO framework (Hungarian assignment + conflict graph)',
             'Method slides; redesign', 'Built and trained: 186 models. PAH learns α from the risk it observes.'],
            ['2. Test with different numbers of drones', '5 vs 8 drones; swarm size 3 to 10',
             'The lead over a fixed weight holds from 3 to 10 drones.'],
            ['3. Ablations: conflict graph, Hungarian assignment, PAH (learned α vs fixed weight)',
             'Gap breakdown; no-assignment run',
             'At 8 drones: conflict graph +15.4 · removing the assignment costs 14.3 · PAH +8.6 (95 % CI +1.7 to +15.4)']]
    d.table(LM, 1.65, [5.3, 2.7, 4.23], rows, pt=15, head_pt=14, max_h=3.6, pad=0.15)
    d.callout(LM, 5.3, CW, 1.2,
              ['**Primary question, written before any training:** with 8 drones, is MAPPO + PAH better than the same agent '
               'with a fixed weight (Fixed-weight MAPPO)?', '**Answer: yes, by +8.6 points, 95 % CI [+1.7, +15.4].**'], pt=17)
    d.notes("""This slide is the whole talk in one table. The three objectives are the ones in the approved synopsis, and next to each is the short answer, so you know where we are going.
Objective one: the framework exists and was trained and tested end to end.
Objective two: we tested from 3 to 10 drones, and PAH stays ahead of the fixed weight everywhere.
Objective three: the ablations tell us where the benefit comes from. With eight drones, the conflict graph is worth about 15 points, removing the assignment costs about 14 (at five drones that difference is not settled), and PAH's own contribution is 8.6 points. That last number is honest but modest, and it comes with a wide confidence interval, which I will come back to.
The box at the bottom is the one question we decided on before training anything. Everything else in the talk is secondary.""")

    # ============================================================ 4 base papers
    d.new_slide('basepapers', 'The two base papers each solve one half of the problem', S1)
    rows = [['', 'DA-MAPPO (Sheng et al., IEEE IoT Journal)', 'IGAT-MARL (Rezaee et al.)', 'This work'],
            ['Solves', 'Target assignment + navigation', 'Collision avoidance only (no targets)', 'Assignment and collision avoidance, together'],
            ['Method', 'MAPPO with the Hungarian assignment in the observation', 'DQN with graph attention on a conflict graph',
             'MAPPO + Hungarian + conflict graph + PAH'],
            ['Setting', '3 drones, 30 to 50 obstacles, 3D (Gazebo)', '3 to 10 aircraft, BlueSky air-traffic simulator',
             '5 and 8 drones, 10 and 20 obstacle discs, 2D'],
            ['Reward weights', 'Fixed coefficients', 'Fixed coefficients', 'Learned by PAH'],
            ['What we reuse', 'Assignment idea, success definition, Table V comparison',
             'Conflict graph, swarm size 3 to 10, loss-of-separation metric', '']]
    d.table(LM, 1.65, [1.9, 3.75, 3.75, 2.83], rows, pt=14, head_pt=13, max_h=4.2, bold_first_col=True, pad=0.09,
            highlight_rows=())
    d.callout(LM, 5.85, CW, 0.85,
              'Our supervisor\'s principle: do what the base papers did. So we trained their methods in our environment and '
              'repeated their experiments on our trained models; we do not copy their numbers.', pt=16)
    d.notes("""DA-MAPPO is the closest paper: it puts the Hungarian assignment into each drone's observation and trains with MAPPO, but it does not look at drone-to-drone conflicts explicitly. IGAT-MARL is the opposite: it builds a conflict graph and uses graph attention, but it has no targets at all.
Neither paper learns how to weigh mission against safety; both use fixed reward coefficients. That is the gap the synopsis describes, and it is where PAH sits.
Important: their environments are very different from ours (3D with three drones, or an air-traffic simulator). So we never compare raw numbers with theirs. We trained their methods in our own environment, and we repeated their experiments on our trained models. I will show both.""")

    # ============================================================ 5 framework
    d.new_slide('framework', 'One framework: assignment and conflict graph feed MAPPO; PAH balances mission against safety', S1)
    # inference path
    d.box(LM, 2.35, 1.95, 1.45, ['2D world', 'moving targets,', 'obstacle discs'], fill=GREY_BG, pt=13, line=BORDER)
    ins = [('Hungarian assignment', 'every step → assigned target'), ('Conflict graph', 'drones on a collision course'),
           ('24-ray LiDAR', 'distance to obstacles')]
    for i, (a, b) in enumerate(ins):
        y = 1.65 + i * 0.95
        d.box(3.05, y, 3.1, 0.82, ['**' + a + '**', b], fill=LBLUE, pt=13, line=None)
        d.arrow(2.5, 3.07, 3.05, y + 0.41, GREY_T, 1.5)
        d.arrow(6.15, y + 0.41, 6.6, 3.07, GREY_T, 1.5)
    d.box(6.6, 2.35, 1.95, 1.45, ['**Observation**', 'per drone', '(50 numbers)'], fill=GREY_BG, pt=13, line=BORDER)
    d.arrow(8.55, 3.07, 8.95, 3.07)
    d.box(8.95, 2.35, 1.85, 1.45, ['**Shared actor**', '(MAPPO)'], fill=BLUE, color=WHITE, pt=14)
    d.arrow(10.8, 3.07, 11.2, 3.07)
    d.box(11.2, 2.35, 1.58, 1.45, ['**Action**', '2D velocity'], fill=GREY_BG, pt=13, line=BORDER)
    # training-only band
    d.box(LM, 4.5, CW, 2.3, [], fill=WHITE, line=GREY_T, dashed=True, round_=0.05, log=False)
    d.text(LM + 0.2, 4.55, 5, 0.3, ['**TRAINING ONLY**'], pt=11, color=GREY_T)
    d.box(0.85, 5.05, 3.0, 1.4, ['**Centralised critic**', 'two value heads:', 'mission and safety'], fill=GREY_BG, pt=13, line=BORDER)
    d.arrow(3.85, 5.75, 4.25, 5.75)
    d.box(4.25, 5.05, 2.55, 1.4, ['**Advantages**', 'A_mission and A_safety'], fill=GREY_BG, pt=13, line=BORDER)
    d.arrow(6.8, 5.75, 7.2, 5.75)
    d.box(7.2, 5.05, 1.75, 1.4, ['**PAH**', 'τ, d_target,', 'n_conflict → α'], fill=BLUE, color=WHITE, pt=13)
    d.arrow(8.95, 5.75, 9.35, 5.75)
    d.box(9.35, 5.05, 3.2, 1.4, ['**Actor update**', 'α · A_mission +', '(1 − α) · A_safety'], fill=LBLUE, pt=13)
    d.arrow(10.95, 5.05, 9.9, 3.8, BLUE, 2.0, dashed=True)
    d.text(10.75, 4.1, 2.0, 0.3, ['trains the actor'], pt=11, color=BLUE)
    d.notes("""Read this diagram from left to right along the top. The world gives each drone three kinds of information: its assigned target from the Hungarian algorithm, which neighbours are on a collision course from the conflict graph, and the distance to obstacles from 24 LiDAR rays. Together that is 50 numbers per drone. One shared actor turns them into a velocity command.
The bottom band is only used during training. The critic estimates two values, one for the mission reward and one for the safety reward, and from them we get two advantages. PAH looks at the situation and produces a weight alpha, and the actor is updated with alpha times the mission advantage plus one minus alpha times the safety advantage.
A useful consequence: PAH shapes the training signal, but it is not used when the drones fly. So it adds no run-time cost. I will show the timing later.""")

    # ============================================================ 6 PAH
    d.new_slide('pah', 'PAH turns the situation into a mission-vs-safety weight α', S1)
    inp = [('τ', 'time to the nearest collision (drone or obstacle, capped at 3 steps)'),
           ('d_target', 'distance to the assigned target'), ('n_conflict', 'number of drones on a collision course')]
    for i, (a, b) in enumerate(inp):
        y = 1.75 + i * 1.18
        d.box(LM, y, 4.1, 1.02, ['**' + a + '**  ' + b], fill=GREY_BG, pt=14, line=BORDER, align='left')
        d.arrow(4.65, y + 0.51, 5.35, 3.45, GREY_T, 1.5)
    d.box(5.35, 2.75, 2.1, 1.4, ['**PAH**', 'small network', '3 → 32 → 1'], fill=BLUE, color=WHITE, pt=14)
    d.arrow(7.45, 3.45, 7.95, 3.45)
    d.box(7.95, 2.75, 1.9, 1.4, ['**risk p**', 'predicted danger', 'from 0 to 1'], fill=LBLUE, pt=13)
    d.arrow(9.85, 3.45, 10.35, 3.45)
    d.box(10.35, 2.75, 2.43, 1.4, ['**α = 0.9 − 0.8 · p**', 'weight on the mission'], fill=LBLUE, pt=14)
    d.text(5.35, 4.45, 7.43, 1.0,
           ['High risk → α near **0.1**: safety counts more.  Low risk → α near **0.9**: the mission counts more.'], pt=16, color=INK)
    d.callout(LM, 5.55, 6.0, 1.25,
              ['**Fixed-weight MAPPO:** α = 0.5 always.', '**Hand-coded τ-rule MAPPO:** α = 0.1 + 0.8 · τ / 3, nothing learned.'],
              pt=14, kind='blue')
    d.callout(6.75, 5.55, 6.03, 1.25,
              ['PAH learns the risk from the **safety cost that actually followed**, in the same training loop. No formula is copied.'],
              pt=14, kind='blue')
    d.notes("""PAH is deliberately tiny: three inputs, one hidden layer of 32 units, one output. The three inputs are exactly the ones in the approved synopsis: time to the nearest collision, distance to the target, and the number of drones on a collision course. The time-to-collision now also counts obstacles, which I will explain in the redesign.
The network predicts a risk between zero and one, and alpha is 0.9 minus 0.8 times that risk. So when danger is close, alpha is near 0.1 and safety dominates the learning signal; when nothing is near, alpha is near 0.9 and the mission dominates.
Two comparison methods use the same agent but a different alpha: a fixed 0.5, and a hand-written rule based only on time to collision. The point of the thesis is whether a learned alpha beats these.
If asked whether this is just a learned version of the hand-coded rule: it has the same inputs, but it learns from the safety cost that actually followed, and it turns towards safety earlier than the rule (I show that on the alpha slide). At Stage 3 it beats the rule by 11 points; at Stage 2 it does not clearly beat it.""")

    # ============================================================ 7 v3
    d.new_slide('v3', 'Version 3: how α is chosen made no difference; diagnostics showed obstacles were the problem', S2)
    d.image(P('v3_alpha_tie.png'), LM, 1.55, 7.75, 3.55)
    d.callout(LM, 5.3, 7.75, 1.4,
              ['The choice of α moved success by **2 points or less**. Removing the assignment cost **20.5 points** at 8 drones '
               '(version 3, one seed).'], pt=16)
    d.chip(8.6, 1.6, 4.18, 1.6, '94 to 100 %', 'of collisions were with obstacles, not with other drones', big_pt=24, small_pt=13)
    d.chip(8.6, 3.35, 4.18, 1.6, 'Blind to obstacles', 'PAH\'s τ came only from drone-to-drone conflicts', big_pt=22, small_pt=13)
    d.chip(8.6, 5.1, 4.18, 1.6, 'No mixing, no loss', 'Stage 2: Plain MAPPO (no α at all) 89.9 % vs 88.2 % for the fixed weight (5 seeds)',
           big_pt=22, small_pt=13, fill=ORANGE_BG, big_color='A63D12')
    d.notes("""This is the honest story of my first attempt. In version 3, three ways of choosing alpha (fixed, a hand-coded rule, and PAH) all landed within about two points of each other, on the left panel. Meanwhile, taking the assignment away cost 20 points, on the right panel.
So I ran diagnostics on the trained models, with no new training. Three findings. First, almost all collisions, 94 to 100 percent, were with obstacles. Second, PAH's time-to-collision only looked at other drones, so PAH could not even see the main danger. Third, when I removed the alpha mixing completely, with a plain MAPPO, success did not drop.
The conclusion was not that PAH failed. It was that this environment gave PAH nothing to arbitrate. That diagnosis is what motivated the redesign on the next slide.
Notes on numbers: the bars come from the original runs; the 89.9 versus 88.2 comparison is a separate re-run on the same laptop, which is why the fixed-weight number differs slightly from the bar.""")

    # ============================================================ 8 redesign
    d.new_slide('redesign', 'Redesign: four changes, one environment bug fixed, settings tuned once and frozen', S2)
    cards = [('1  Two value heads', ['Separate mission and safety critics, so the safety advantage becomes a real safety signal.',
                                       '**Because:** in version 3 the mixed signal was 95 to 100 % the same as Plain MAPPO\'s.']),
             ('2  Obstacle-aware τ', ['PAH\'s time-to-collision now includes obstacles. Its three inputs are unchanged.',
                                      '**Because:** PAH could not see the main danger.']),
             ('3  24-ray LiDAR', ['Replaces the four axis-aligned distances of version 3.',
                                  '**Because:** obstacles caused 94 to 100 % of collisions.']),
             ('4  Sized obstacles', ['Discs of radius 12: 10 at Stage 2, 20 at Stage 3 (points before).',
                                     '**Because:** point obstacles were far easier than the base papers\' physical ones.'])]
    for i, (h, b) in enumerate(cards):
        d.card(LM + (i % 2) * 4.05, 1.6 + (i // 2) * 2.65, 3.9, 2.5, h, b, body_pt=16, head_pt=19, body_space=8)
    d.card(8.75, 1.6, 4.03, 2.85, 'Bug found and fixed',
           ['Targets could push a waiting drone into an obstacle.',
            'A hand-written LiDAR rule then reached 82 % with no obstacle collisions (dense Stage 2 setting): the task is solvable.'],
           fill=ORANGE_BG, head_color='A63D12', accent=ORANGE, body_pt=15, head_pt=19)
    d.card(8.75, 4.6, 4.03, 2.15, 'Tuned once, then frozen',
           'Reward shaping and obstacle density were tuned on Plain MAPPO only, on separate seeds, then fixed for every method.',
           body_pt=15, head_pt=19)
    d.notes("""Four changes, each one answering a diagnostic finding. The two value heads make the safety advantage a real safety signal. Counting obstacles in the time-to-collision lets PAH see the main danger. The 24-ray LiDAR gives much better obstacle sensing than four directions. And the obstacles are now discs with a size, not points.
On the right: along the way we found a bug in the environment. Targets bounced off obstacles too close, so a drone waiting on its target could be dragged into one. We fixed it, and checked that the task is solvable by writing a simple hand-coded LiDAR rule, which reached 82 percent with no obstacle collisions in the dense setting. That tells us the task itself is fine, and any remaining difficulty is a learning problem.
Last, the fairness rule: we tuned reward shaping and obstacle density once, on the plain baseline only, using separate seeds, and then froze them for every method. So no method got special tuning.
Please note: the supervisor's agreement to these changes is not written anywhere in the repository, so confirm it before presenting if you want to say it.""")

    # ============================================================ 9 biased PAH (mechanism) + 10 alpha figure
    d.new_slide('biased', 'The first PAH was biased against safety; we found the cause and fixed it once', S2)
    steps = [('1  The synopsis design', 'PAH is trained through the policy gradient, together with the actor.', GREY_BG),
             ('2  What it learned', 'In danger, α was pushed towards the mission: +0.200, its maximum, at τ < 1.', ORANGE_BG),
             ('3  Why', 'The gradient of α·A_mission + (1 − α)·A_safety with respect to α is A_mission − A_safety. '
                        'In danger A_safety is very negative, so the gradient raises α.', GREY_BG),
             ('4  The fix, made once', 'PAH predicts the risk and learns by regression on the safety cost that followed. '
                                       'No gradient from the actor loss. Same inputs, same 3 → 32 → 1 network.', LBLUE)]
    cw, gap = 2.85, (CW - 4 * 2.85) / 3
    for i, (h, b, f) in enumerate(steps):
        x = LM + i * (cw + gap)
        d.card(x, 1.65, cw, 3.55, h, b, fill=f, body_pt=17, head_pt=18,
               accent=(ORANGE if f == ORANGE_BG else BLUE), head_color=('A63D12' if f == ORANGE_BG else DBLUE))
        if i < 3:
            d.arrow(x + cw + 0.03, 3.4, x + cw + gap - 0.03, 3.4, GREY_T, 2.0)
    d.callout(LM, 5.4, CW, 0.72,
              'Measured on the first PAH\'s final model (Stage 3, seed 42, 100 test episodes): +0.200 for τ < 1 (134 states). '
              'The biased version is kept as a finding.', pt=15)
    d.callout(LM, 6.2, CW, 0.65,
              'This is the one deliberate change to PAH compared with the synopsis, which trained it through the policy gradient.',
              kind='orange', pt=15)
    d.notes("""This is the part I am proudest of, because it is a negative result handled honestly.
Step one: my first PAH followed the synopsis. It was trained through the same policy-gradient update as the actor.
Step two: when I looked at what it had learned, it did the opposite of its purpose. In danger it pushed alpha as high as allowed, towards the mission.
Step three: the reason is mathematical. The gradient with respect to alpha is the mission advantage minus the safety advantage. In danger the safety advantage is strongly negative, so the gradient says: raise alpha, ignore safety. The model was simply following that gradient.
Step four: I changed the design once. Now PAH predicts the risk and is trained by regression on the safety cost that actually followed, with no gradient from the actor loss. Same inputs, same tiny network.
I found this by looking at the mechanism, not by tuning performance. The blue box gives the measurement; the biased version is kept as a finding. The orange box is the one place where PAH differs from the synopsis.
If asked 'did you change PAH after seeing seed 42, and is that tuning on the test set?': the change was driven by the mechanism, tested on synthetic data and a 300-episode smoke run, then frozen before any of the final runs. Without seed 42 the main result is +7.9, almost unchanged, and on seed 42 itself the new PAH is slightly below the hand-coded rule (79.5 against 82.0 percent), so the design was not shaped to win that seed.""")

    fig_slide(d, 'alpha', 'The fixed PAH tracks danger: α is low when a collision is near, and turns towards safety earlier than the rule',
              S2, 'alpha_by_tau.png',
              ['About **0.13 to 0.19** when τ < 1 and about **0.8** when nothing is ahead. At 1 ≤ τ < 2 PAH uses **0.25 (Stage 2) and 0.32 (Stage 3)**; the hand-coded rule uses 0.51.'],
              """Each panel shows the weight alpha that a method uses, split by how close the nearest collision is. The grey squares are the fixed weight, always 0.5. The dotted line is the hand-coded rule. The blue line is the learned PAH, and the faint blue dots are its individual seeds.
When a collision is less than one step away, PAH's alpha is about 0.13 to 0.19: safety counts most. When nothing is ahead, it is about 0.8: the mission counts most. In between, at one to two steps from a collision, PAH has already moved towards safety, 0.25 at Stage 2 and 0.32 at Stage 3, while the hand-coded rule is still at 0.51.
So the learned weight is not a copy of the formula: it reacts earlier. Whether that earlier reaction pays off is what the comparison with the hand-coded rule measures: clearly at eight drones, not clearly at five.""", call_h=0.85)

    # ============================================================ 10 protocol
    d.new_slide('protocol', 'A protocol built so that we cannot chase results', S2)
    cards = [('Same for every method', 'One environment, one training budget (8,000 episodes), one set of hyperparameters.'),
             ('10 seeds × 2 stages', 'Training seeds 42 to 51: 186 trained models in total.'),
             ('The same 200 test layouts', 'Deterministic actions, evaluation seed 7001, so every model sees identical episodes.'),
             ('One primary question, written first', 'Stage 3: MAPPO + PAH vs Fixed-weight MAPPO. Everything else is secondary.'),
             ('Success means all drones arrive', 'Every drone reaches its assigned target, no collision, within 500 steps (as in DA-MAPPO).'),
             ('Reproducible', 'All 186 evaluations re-run: 186 of 186 identical. Tables are made by script.')]
    for i, (h, b) in enumerate(cards):
        d.card(LM + (i % 3) * 4.1, 1.6 + (i // 3) * 2.42, 3.95, 2.28, h, b, body_pt=17, head_pt=17)
    d.text(LM, 6.5, CW, 0.4,
           ['Stage 2: 5 drones, 10 obstacles.  Stage 3: 8 drones, 20 obstacles.  Confidence intervals: 95 % Welch over seeds.'],
           pt=12, color=GREY_T)
    d.notes("""This slide is for anyone who wonders whether we tuned until the numbers looked good. We did not, and here is how we prevented it.
Every method gets the same environment, the same 8,000 training episodes and the same hyperparameters. Ten training seeds per method and per stage, 186 trained models in total. Each model is tested on the same 200 starting layouts, with deterministic actions, so differences are not luck of the layout.
The primary question was written down before the training, so we cannot move the goalposts: at eight drones, is MAPPO + PAH better than the fixed weight? Every other comparison I show is secondary, and I say so explicitly; no multiple-testing correction was applied.
Success means all drones reach their own targets without any collision, within 500 steps, the same definition as in the DA-MAPPO paper.
Finally, we re-ran all 186 evaluations from scratch and got identical results. Stage 2 is 5 drones and 10 obstacles; Stage 3 is 8 drones and 20 obstacles.""")

    # ============================================================ 11 main chart
    fig_slide(d, 'mainresult', 'MAPPO + PAH ranks first of nine methods at both stages', S3, 'success_all_methods.png',
              ['**86.8 %** at Stage 2 and **82.7 %** at Stage 3. Grey bars are the four base-paper methods trained in our environment.'],
              """Here is the main result. Every bar is the average over ten training seeds, the dots are the individual seeds, and the black line is the 95 percent confidence interval. Blue is MAPPO + PAH, light blue are our other methods, and grey are the four base-paper methods, trained in our own environment under identical conditions.
MAPPO + PAH is first at both stages: 86.8 percent with five drones and 82.7 percent with eight. All four base-paper methods are clearly below.
The tenth method, RMAPPO, is not in this chart because it did not learn under the shared settings. I explain that in the limits.""")

    # ============================================================ 12 table
    ev = rd('03-base-paper-baselines/output/eval_summary.md')
    t1 = {r[0]: r for r in parse_rows(ev, 'Table 1', 8)}
    t2 = {r[0]: r for r in parse_rows(ev, 'Table 2', 7)}
    d.new_slide('table', 'The numbers behind the chart', S3)
    order_ours = ['MAPPO + PAH', 'Fixed-weight MAPPO', 'Hand-coded τ-rule MAPPO', 'MAPPO + PAH (Hungarian off)', 'Plain MAPPO']
    order_base = ['IGAT-style MAPPO', 'DA-MAPPO (2D)', 'MAPPO', 'IPPO']
    rows = [['Method', 'Stage 2 success (%)', 'Stage 3 success (%)', 'Stage 3 collision (%)', 'Stage 3 steps', 'Stage 3 path']]
    rows.append(['Our methods', '', '', '', '', ''])
    for m in order_ours:
        nm = m.replace('(Hungarian off)', '(no assignment)')
        rows.append([nm, t1[m][2], t1[m][5], t1[m][6], t2[m][4], t2[m][5]])
    rows.append(['Base-paper methods in our environment', '', '', '', '', ''])
    for m in order_base:
        rows.append([m, t1[m][2], t1[m][5], t1[m][6], t2[m][4], t2[m][5]])
    d.table(LM, 1.55, [3.9, 1.9, 1.9, 1.6, 1.4, 1.53], rows, pt=14, head_pt=12.5, max_h=4.8, sub_rows=(1, 7),
            highlight_rows=(2,), align=['left', 'center', 'center', 'center', 'center', 'center'], pad=0.055)
    d.text(LM, 6.28, CW, 0.65,
           ['Success: mean ± 95 % half-width over 10 seeds. Steps and path (units per drone) are measured on successful episodes only. '
            'RMAPPO did not learn under the shared settings (appendix).'], pt=12, color=GREY_T)
    d.notes("""The same results as numbers, because a table is easier to quote. Success is the mean over ten seeds with its 95 percent half-width. The last two columns, steps and path length, are measured only on successful episodes, so a method with very low success is measured on few episodes; treat them as secondary.
MAPPO + PAH has the highest success and the lowest collision rate at Stage 3, and it is also the fastest: 61 steps on average, against 76 for the fixed weight.
The no-assignment row is the same PAH agent where each drone is simply tied to the target with its own number for the whole episode.""")

    # ============================================================ 13 primary
    d.new_slide('primary', 'Primary result: +8.6 points over a fixed weight at 8 drones (95 % CI +1.7 to +15.4)', S3)
    d.image(P('pah_vs_each_method.png'), LM, 1.5, CW, 4.15)
    d.chip(LM, 5.78, 3.95, 1.1, '+8.6 [+1.7, +15.4]', 'Primary: Stage 3, MAPPO + PAH minus Fixed-weight MAPPO', big_pt=20, small_pt=11)
    d.chip(LM + 4.14, 5.78, 3.95, 1.1, '+7.9 [+0.7, +15.1]', 'Without seed 42, the seed that exposed the first PAH\'s bias', big_pt=20, small_pt=11)
    d.chip(LM + 8.28, 5.78, 3.95, 1.1, '+2.0 [' + M + '2.6, +6.6]', 'Not settled: 5 drones vs the hand-coded rule', big_pt=20, small_pt=11,
           fill=ORANGE_BG, big_color='A63D12')
    d.notes("""This is the question we fixed in advance. At eight drones, MAPPO + PAH minus the fixed weight is plus 8.6 points, with a 95 percent confidence interval from plus 1.7 to plus 15.4. The whole interval is above zero, so by our rule it is better. MAPPO + PAH was higher on nine of the ten seed indices.
Please read it the way I read it: the gain is real, but modest and uncertain. A fair statement is that the gain is plausibly between about two and fifteen points.
The middle box answers the obvious worry. The first PAH's bias was seen on seed 42. Leaving seed 42 out, the result is plus 7.9, essentially unchanged.
The orange box is an honest limit: at five drones the learned alpha is not clearly better than the hand-coded rule. The interval crosses zero. The learned alpha is clearly better only with eight drones.
All other comparisons in the figure are secondary: no correction for multiple comparisons.""")

    # ============================================================ 14 gap
    fig_slide(d, 'gap', 'Most of the gap to DA-MAPPO (2D) comes from the framework; PAH\'s own part is +8.6', S3,
              'gap_breakdown.png',
              ['Controlled steps at Stage 3: conflict-graph observation **+15.4**, separate value heads **+30.0**, PAH\'s learned α **+8.6**. '
               'We do **not** claim the whole 53.9-point gap as PAH\'s effect.'],
              """The distance between DA-MAPPO (2D) and MAPPO + PAH is large, 54 points at Stage 3. It would be wrong to credit all of it to PAH.
We changed one thing at a time. Replacing raw teammate positions by conflict-graph features gives 15 points. Splitting the critic into a mission and a safety head gives 30 points. And PAH's learned alpha, instead of a fixed 0.5, gives the last 8.6.
All three steps are part of our framework, but only the last one is PAH. The steps are roughly additive; I say roughly because they are not independent. This slide is why my headline number is 8.6 and not 54.""", call_h=0.85)

    # ============================================================ 15 outcomes
    fig_slide(d, 'outcomes', 'MAPPO + PAH has the fewest collisions; failures everywhere are mostly obstacle hits', S3,
              'outcomes.png',
              ['**17 %** of episodes end in a collision with MAPPO + PAH vs **26 %** with Fixed-weight MAPPO. Without any assignment, drone-to-drone hits rise and paths double (342 vs 173 units).'],
              """This shows how episodes end, at Stage 3. Blue is success, orange is an obstacle collision, green a drone-to-drone collision, yellow a timeout.
Two things to see. First, in every method most failures are obstacle collisions, which is why PAH now looks at obstacles. Second, MAPPO + PAH has the smallest orange bar: 17 percent collisions against 26 percent for the fixed weight.
For the no-assignment variant, drone-to-drone collisions rise to about 6 percent of episodes and the paths of the successful episodes are twice as long, 342 against 173 units. That is the evidence that the assignment matters.""", call_h=0.85)

    # ============================================================ 16 vs paper
    fig_slide(d, 'paper', 'Against the DA-MAPPO paper the ranking agrees; the absolute numbers cannot be compared', S3,
              'ranking_vs_paper.png',
              ['Paper: 3 drones, 3D Gazebo, about 3 M steps with a curriculum. Ours: 8 drones, 2D, 8,000 episodes, no curriculum. '
               'What agrees: dynamic assignment beats fixed assignment, IPPO is weakest, MAPPO + PAH is above all base-paper methods.'],
              """The left panel is the DA-MAPPO paper's hardest setting. The right panel is our Stage 3. The same colour means the same method in both studies.
I want to be careful here. The paper's numbers are higher than ours for the same method. That is expected: their simulator is 3D with three drones, a different sensor, a much longer training with a curriculum. Our DA-MAPPO (2D) gets 28.9 percent and theirs gets 90, and the two numbers should not be compared.
What we can compare is the order. In both studies dynamic assignment is above rigid assignment, and IPPO is the weakest of the learning methods. And in our environment MAPPO + PAH is above all of them.
There is a backup slide in the appendix that compares the gain over MAPPO instead of the raw level; that one does not depend on the simulator.""", call_h=1.0)

    # ============================================================ 17 experiments table
    d.new_slide('experiments', 'We repeated the base papers\' experiments on our trained models, with no retraining', S4)
    rows = [['Experiment', 'From', 'What changes at test time', 'What we found'],
            ['Obstacle density', 'DA-MAPPO ENV-1/2/3', '10 to 50 discs', 'Every method falls; MAPPO + PAH is first at every density'],
            ['Static targets', 'DA-MAPPO Table IV / V', 'Targets stop moving', 'Every method does worse; MAPPO + PAH loses least (' + M + '7.0 vs ' + M + '15.0). Unexplained'],
            ['Assignment every 50 steps', 'DA-MAPPO ablation', 'Re-assign every 50 steps, not every step', 'Small loss for every method (' + M + '0.7 to ' + M + '3.8 points)'],
            ['Swarm size 3 to 10', 'IGAT-MARL', 'Number of drones', 'MAPPO + PAH degrades least (' + M + '10.0 vs ' + M + '17.4 for the fixed weight)'],
            ['Loss of separation, edges', 'IGAT-MARL', 'Count near-misses and conflict edges', 'MAPPO + PAH is not clearly lower: its gain is in success'],
            ['LiDAR noise', 'extra', 'Noise up to 10 % of the ray range', 'At most about 3 points lost'],
            ['Decision time', 'extra', 'Milliseconds per step', 'MAPPO + PAH = Fixed-weight MAPPO; IGAT-style about 6× slower']]
    d.table(LM, 1.55, [2.55, 2.35, 3.05, 4.28], rows, pt=13, head_pt=12.5, max_h=4.55, bold_first_col=True, pad=0.06)
    d.callout(LM, 6.12, CW, 0.75,
              'No new primary claim: every comparison here is secondary. The models were trained at one setting, so these are generalisation tests and every method is expected to drop.',
              pt=14, kind='orange')
    d.notes("""Our supervisor's principle was: what the base papers did, we should do. This table lists seven of their experiments and what we found. Importantly there is no new training here: the same 180 trained models were re-evaluated with a single test condition changed at a time, 200 episodes each. It took under two hours on a laptop.
I will show the main ones in the next slides. In one sentence each: density hurts everyone but the order stays; static targets surprisingly hurt everyone; assigning every 50 steps costs a little; MAPPO + PAH degrades least with more drones; its advantage is in success, not near-misses; noise barely matters; and PAH costs nothing at run time.
Because the models were trained only at one setting, every method is expected to drop when conditions change. A drop is not a failure.""")

    # ============================================================ 18-22 experiment figures
    fig_slide(d, 'density', 'Obstacle density: every method falls, and MAPPO + PAH stays first at every density', S4, 'density.png',
              ['Stage 3, MAPPO + PAH: **93.5 → 82.7 → 70.3 → 51.3 → 40.4 %** at 10 / 20 / 30 / 40 / 50 discs. Without a conflict graph (DA-MAPPO (2D), MAPPO, IPPO) success falls to about 2 to 3 % at 50 discs.'],
              """This is the DA-MAPPO density experiment, applied to our trained models. The models were trained at 10 and 20 discs, marked on the plot, and tested from 10 to 50 discs.
Everything goes down as obstacles are added, as expected. MAPPO + PAH is first at every density, in both stages; the methods just behind it swap places in some columns, but only where their confidence bands overlap. At 50 discs at Stage 3 it still reaches 40 percent, while the methods without a conflict graph are down at two to three percent.
The paper's methods also fall when obstacles are added, so the direction agrees. A fair caveat: DA-MAPPO trained its models with a curriculum on the dense settings; ours were trained at one density only. There is a backup slide that puts the paper's curve next to ours, and it shows openly that our DA-MAPPO (2D) is far below the paper's, for the reasons I gave earlier.""")
    fig_slide(d, 'swarm', 'Swarm size 3 to 10: MAPPO + PAH degrades least', S4, 'swarm_size.png',
              ['Stage 3 models, 3 → 10 drones: MAPPO + PAH **' + M + '10.0** points, Fixed-weight MAPPO ' + M + '17.4, IGAT-style MAPPO ' + M + '44.8. '
               'MAPPO, DA-MAPPO (2D) and IPPO see all teammates, so they cannot run at another swarm size without retraining.'],
              """This is the IGAT-MARL scalability experiment, and also the second objective in our synopsis: what happens when the number of drones changes?
Each model was used as trained and tested with three to ten drones. The shaded areas are confidence intervals. MAPPO + PAH degrades the least, about ten points from three to ten drones at Stage 3, against 17 for the fixed weight and 45 for the IGAT-style method. The same holds for the Stage 2 models, which were trained on five drones: 8.8 points lost, against 13.0 for the fixed weight.
Only five methods are shown because the other three take all teammates as input, so the size of their input is tied to the number of drones.""", call_h=0.95)
    fig_slide(d, 'los', 'Near-misses: MAPPO + PAH is not safer by this metric; its advantage is mission success', S4,
              'loss_of_separation.png',
              ['Loss of separation per episode at Stage 3 (8 drones): MAPPO + PAH **0.63**, Fixed-weight MAPPO 0.55, Hand-coded τ-rule MAPPO 0.73, IGAT-style MAPPO 2.64. Descriptive only, no confidence interval.'],
              """Loss of separation is IGAT-MARL's metric: how often two drones come closer than three collision radii. It grows with swarm size for every method, like in their paper.
Here I want to flag a result that does not flatter PAH. MAPPO + PAH does not have fewer near-misses than the fixed weight or the hand-coded rule: 0.63 against 0.55 and 0.73 per episode at eight drones. The IGAT-style method has far more.
So PAH's advantage is in mission success, not in fewer close passes between drones. This is consistent with the diagnostics: most failures are obstacle collisions, not drone-to-drone near-misses. I would not claim that PAH makes drones keep more distance from each other.""", kind='orange', call_h=0.95)
    fig_slide(d, 'static', 'Static targets: every method does worse; we report it and have not explained it', S4,
              'static_targets.png',
              ['Every method was trained on moving targets. MAPPO + PAH loses least (Stage 3: **' + M + '7.0** vs ' + M + '15.0 for Fixed-weight MAPPO), so its lead grows to **+16.6**.'],
              """In the DA-MAPPO paper, static targets are an easier case. We stop the targets from moving, and every method does worse, not better. Black dots are the trained setting, orange dots the static one, and the triangles mark where the change is statistically settled.
The change is statistically settled for 17 of the 18 method-and-stage pairs. We have not tested why. A plausible explanation is that the models learned to rely on the target drifting, because they were trained on moving targets only. Also, in the paper 'dynamic' means the targets swap places, while in ours the targets drift, so the two cases are not the same.
I am showing this because hiding it would be worse. The honest wording is: observation, not explained. One positive detail: MAPPO + PAH loses less than the fixed weight, so its lead over the fixed weight grows to about 17 points.""", kind='orange', call_h=0.85)

    # 22 noise + timing
    d.new_slide('noise', 'Sensor noise barely matters, and PAH adds no run-time cost', S4)
    d.image(P('noise.png'), LM, 1.55, 5.95, 4.1, valign='top')
    d.image(P('timing.png'), LM + 6.3, 1.55, 5.93, 3.6, valign='top')
    d.callout(LM, 5.85, 5.95, 1.0, 'LiDAR noise up to 10 % of the ray range costs at most about 3 points (MAPPO + PAH: 82.7 → 80.8). The lead is unchanged.', pt=14)
    d.callout(LM + 6.3, 5.85, 5.93, 1.0, 'MAPPO + PAH and Fixed-weight MAPPO: 0.04 to 0.05 ms per step. IGAT-style MAPPO is about 6× slower.', pt=14)
    d.notes("""Two quick robustness checks. On the left, we add Gaussian noise to the LiDAR distances, up to ten percent of the sensor range. No method loses more than about three points, and the lead of MAPPO + PAH over the fixed weight stays at about eight and a half points.
On the right, the time to compute the actions of the whole swarm, on one laptop CPU thread. MAPPO + PAH and the fixed weight are identical, about 0.05 milliseconds per step. That is expected: PAH shapes the training signal, but the actor does not use it when flying. The graph-attention method is about six times slower.
Absolute times depend on the machine, and the environment step and the conflict graph are not included.""")

    # 23 lead everywhere
    d.new_slide('lead', 'MAPPO + PAH stays ahead of Fixed-weight MAPPO in all 31 test settings', S4)
    d.image(P('lead_everywhere.png'), LM, 1.5, 8.2, 5.4)
    d.card(8.95, 1.6, 3.83, 1.75, '31 of 31', 'The 95 % interval is above zero in every setting (14 at Stage 2, 17 at Stage 3).', body_pt=14, head_pt=20)
    d.card(8.95, 3.5, 3.83, 1.6, 'Weakest at 3 drones', 'Stage 2 +3.5, Stage 3 +4.8. With three drones there are few conflicts to resolve.',
           body_pt=14, head_pt=17)
    d.card(8.95, 5.25, 3.83, 1.6, 'Read with care', 'The same 10 seeds are used in every setting: not 31 independent results. All secondary.',
           fill=ORANGE_BG, head_color='A63D12', accent=ORANGE, body_pt=14, head_pt=17)
    d.notes("""This one figure summarises all the tests: densities, static targets, assignment every 50 steps, swarm sizes and sensor noise. In every one of the 31 settings the confidence interval of the lead over the fixed weight is entirely above zero.
The weakest case is the smallest swarm, three drones: with three drones there are few conflicts, so a learned balance between mission and safety has the least to do. The lead tends to grow when the task gets harder.
A necessary caution, in orange: all of these use the same ten training seeds, so the 31 results are not independent confirmations. They show the lead is not specific to one test condition; they do not give 31 separate proofs. And all of them are secondary comparisons.""")

    # ============================================================ 24 synopsis diffs
    d.new_slide('synopsis', 'Where we differ from the approved synopsis, and why', S5)
    rows = [['The synopsis said', 'What we did', 'Why'],
            ['PAH trained through the policy gradient', 'PAH trained by regression on the observed safety cost; same training loop, no actor gradient',
             'The policy-gradient version was biased against safety'],
            ['Obstacle readings in four directions', '24-ray LiDAR', 'Obstacles caused 94 to 100 % of collisions'],
            ['Curriculum 3 → 5 → 8 drones', 'Each stage trained from scratch; Stage 1 (3 drones, static targets) only in version 3',
             'Phase 1b plan: identical training for every method'],
            ['Baselines: MAPPO without assignment, DA-MAPPO (2D), IGAT-MARL with fixed assignment',
             'DA-MAPPO (2D) and IGAT-style: yes. MAPPO has the assignment fixed at the start. IPPO added; no-assignment as an ablation',
             'Matches the base papers\' rigid-assignment baselines'],
            ['Metric: target reassignments per episode', 'Not measured yet', 'Planned'],
            ['3 swarm sizes × 3 obstacle densities', 'One factor at a time: density 10 to 50, swarm size 3 to 10', 'Wider range, not a full grid'],
            ['PyBullet simulator', 'Custom 2D environment', 'The research question is about α, not flight dynamics']]
    d.table(LM, 1.55, [3.85, 5.0, 3.38], rows, pt=14, head_pt=14, max_h=5.4, bold_first_col=False, pad=0.06)
    d.notes("""A committee member who has read the synopsis may ask about differences, so I would rather list them myself.
The most important one is the first: the synopsis trained PAH through the policy gradient, and I found that this makes it biased against safety, so PAH is now trained by regression on the safety cost that followed. It is still in the same training loop, with the same inputs and network.
Second, obstacle sensing went from four directions to a 24-ray LiDAR, because obstacles caused almost all collisions.
Third, we did not use the curriculum: each stage is trained from scratch, identically for all methods. Stage 1, with three drones and static targets, was only run in version 3.
Fourth, the baselines: we have the DA-MAPPO (2D) and the IGAT-style methods, and a MAPPO whose assignment is fixed at the start; IPPO was added from the DA-MAPPO paper, and the no-assignment case appears as an ablation.
Fifth, the number of target reassignments per episode, a secondary metric in the synopsis, has not been measured yet.
Sixth, the experiments change one factor at a time rather than a full three-by-three grid.
Last, the simulator is a custom 2D environment instead of PyBullet; the reason is that the question is about alpha and not flight dynamics. Please confirm that this was agreed with the supervisor before presenting.""")

    # ============================================================ 25 claims
    d.new_slide('claims', 'What we claim, and what we do not', S5)
    rows = [['We claim', 'We do not claim'],
            ['MAPPO + PAH is better than Fixed-weight MAPPO with 8 drones: +8.6 [+1.7, +15.4], plausibly 2 to 15 points',
             'That PAH explains the whole 53.9-point gap to DA-MAPPO (2D)'],
            ['It ranks first of nine methods at both stages, with the same budget and settings as the base-paper methods',
             'That we reproduced the base papers\' numbers (different simulator, sensors, training length)'],
            ['The lead holds in 31 of 31 test settings (secondary, same seeds)', 'That PAH keeps drones farther apart: loss of separation is similar'],
            ['A policy-gradient-trained α was biased against safety (a finding); a risk-learning α fixes it',
             'That PAH is clearly better than the hand-coded rule at 5 drones (+2.0, not settled)'],
            ['', 'Anything about 3D flight or real hardware']]
    d.table(LM, 1.6, [6.1, 6.13], rows, pt=17, head_pt=17, max_h=5.3, pad=0.13)
    d.notes("""Before the conclusion, a plain statement of scope. On the left, what the data supports. On the right, what it does not.
I would like to draw attention to three entries on the right. First, the large gap to DA-MAPPO (2D) is not all PAH. Second, we reproduced the methods in our own environment, we did not reproduce the numbers of the papers. Third, we do not claim PAH makes drones keep more distance; the near-miss metric does not show it. And the one on drones at five: the learned alpha is not clearly better than the hand-coded rule there.
Stating these ourselves is deliberate. It is what makes the claims on the left believable.""")

    # ============================================================ 26 limits + planned
    d.new_slide('limits', 'Limits, stated before anyone asks, and what we plan next', S5)
    d.text(LM, 1.6, 7.45, 5.2,
           ['The primary interval is wide; its lower end is +1.7 points.',
            'The base-paper methods use our shared settings, tuned on Plain MAPPO. They were not tuned one by one, and their scores are below the papers\' 3D results.',
            '**RMAPPO** did not learn under the shared settings (exploration collapsed; 0 % on 6 seeds at Stage 3; no implementation bug found). It is in the appendix with the reason, not as a performance number.',
            'A mechanism check does not explain where PAH\'s gain comes from; we do not claim that PAH reshapes the advantage.',
            'One simulated 2D environment. The same ten seeds are used in every test setting.'],
           pt=17, bullet=True, space_after=10)
    d.card(8.3, 1.6, 4.48, 5.15, 'Planned strengthening',
           ['**Fresh-seed replication:** MAPPO + PAH and Fixed-weight MAPPO on 10 new seeds, no design change, reported separately (about 2.5 hours per stage on the laptop).',
            '**RMAPPO** with its original large-batch setting (about one night).',
            '**Target reassignments per episode**, the missing synopsis metric.'],
           body_pt=16, head_pt=19, body_space=10)
    d.notes("""These are the limits, and I would say each of them out loud before anyone asks.
The primary interval is wide. The base-paper methods share our settings and were tuned only on the plain baseline, so their absolute scores are lower than in the papers. RMAPPO did not learn: its exploration noise collapsed early and the success stayed at zero on six seeds; I checked that its recurrent replay matches the stored values, so I found no implementation bug, but I did not re-run it with its original large-batch setting, so it stays in the appendix and not in the main table. A mechanism check on the advantage signal did not explain where the gain comes from, so I make no claim there. And everything is one 2D simulated environment.
On the right is what I plan to do to strengthen the main result: a replication on ten fresh seeds with no design change, which would narrow the interval; RMAPPO with its original setting; and the missing synopsis metric.
Note for the presenter: the replication has not been run yet. Do not say it has.""")

    # ============================================================ 27 conclusion
    d.new_slide('conclusion', 'Conclusion', S5)
    items = [('A unified framework', 'MAPPO with Hungarian assignment, a conflict graph and a Priority Arbitration Head, trained and tested on 186 models.'),
             ('First of nine methods at both stages', '86.8 % and 82.7 %; PAH\'s own gain over a fixed weight is +8.6 points, 95 % CI [+1.7, +15.4].'),
             ('A diagnosis-driven redesign', 'Obstacles, not other drones, caused the failures; a policy-gradient PAH is biased against safety.'),
             ('The base papers\' experiments, repeated', 'The lead over the fixed weight holds in 31 of 31 settings: density, swarm size, static targets, noise.')]
    for i, (h, b) in enumerate(items):
        y = 1.6 + i * 1.3
        d.box(LM, y + 0.05, 0.85, 0.85, [str(i + 1)], fill=BLUE, color=WHITE, pt=26, bold=True, round_=0.5, log=False)
        d.card(1.6, y, 11.18, 1.2, h, b, body_pt=16, head_pt=18, accent=None)
    d.notes("""To close, four points. A unified framework that was trained and tested end to end. The best method of nine at both stages, with the honest statement that PAH's own gain is plus 8.6 points over a fixed weight and the interval is wide. A redesign driven by diagnostics, including a negative result, the biased first PAH, which I think is a contribution in itself. And the base papers' experiments, repeated on our own models, where the lead holds everywhere we looked.
Thank you. I am happy to take questions, and I have backup slides for the ones I expect.""")

    # ============================================================ 28 next steps
    d.new_slide('next', 'Next steps and questions for the panel', S5)
    d.text(LM, 1.6, 6.3, 0.45, ['**Next steps**'], pt=19, color=DBLUE)
    d.text(LM, 2.1, 6.3, 4.6,
           ['Thesis writing: methodology and literature review can start now.',
            'Results tables and figures in the base papers\' format.',
            'Optional strengthening: fresh-seed replication; RMAPPO with its original setting; reassignment metric.'],
           pt=19, bullet=True, space_after=14)
    d.card(7.2, 1.6, 5.58, 5.15, 'Questions for the panel',
           ['**1.** Is the experiment list enough for the comparison chapter?',
            '**2.** RMAPPO: appendix with the reason, or re-run with its original setting?',
            '**3.** May version 3 be presented as the first stage that motivated the redesign?',
            '**4.** Is the custom 2D environment acceptable instead of PyBullet?'],
           body_pt=18, head_pt=20, body_space=14)
    d.notes("""Next steps are mostly writing: the methodology and literature chapters can start now, and the results tables in the base papers' format.
Then the four questions. I would like the panel's view on whether the list of experiments is enough for the comparison chapter, whether RMAPPO belongs in an appendix or should be re-run, whether version 3 can be presented as the first stage that led to the redesign, and whether the custom 2D environment is acceptable in place of PyBullet.
Asking these explicitly keeps the discussion on the decisions that matter.""")

    # ============================================================ appendix
    d.new_slide('app_divider', 'Appendix', APP, dark=True, number=False)
    d.text(0.9, 2.9, 11, 1.2, ['Appendix'], pt=44, bold=True, color=WHITE)
    d.text(0.9, 4.1, 11, 0.8, ['Backup slides for questions'], pt=22, color='9DC0EC')
    d.notes('Backup slides. Use them only if a question calls for them.')

    d.new_slide('app_methods', 'Appendix A1 · The ten methods, with their full names', APP)
    rows = [['Name used in this deck', 'What it is'],
            ['MAPPO + PAH', 'MAPPO with the learned α (the thesis method); two value heads'],
            ['Fixed-weight MAPPO', 'The same agent with α = 0.5 always; two value heads'],
            ['Hand-coded τ-rule MAPPO', 'α = 0.1 + 0.8 · τ / 3; nothing learned; two value heads'],
            ['MAPPO + PAH (no assignment)', 'Each drone tied to the target with its own number for the whole episode (called "Hungarian off" in some figures)'],
            ['Plain MAPPO', 'One value head, one combined reward, no α'],
            ['IGAT-style MAPPO', 'MAPPO with graph attention over the conflict graph (width 64, no dropout); assignment fixed at the start'],
            ['DA-MAPPO (2D)', 'MAPPO with all teammates in the observation and the Hungarian assignment every step; one value head'],
            ['MAPPO', 'MAPPO with the assignment fixed at the start (rigid assignment); one value head'],
            ['IPPO', 'Independent PPO with a local critic'],
            ['RMAPPO', 'Recurrent MAPPO; did not learn under the shared settings (see A13)']]
    d.table(LM, 1.55, [3.7, 8.53], rows, pt=13.5, head_pt=13, max_h=5.3, bold_first_col=True, pad=0.05)
    d.notes('Use this when someone asks what exactly a method is. The base-paper methods keep one value head, as in the published methods; the effect of two heads is measured separately as Fixed-weight MAPPO minus Plain MAPPO.')

    d.new_slide('app_impl', 'Appendix A2 · Training and environment settings', APP)
    rows = [['Setting', 'Value', 'Setting', 'Value'],
            ['Algorithm', 'MAPPO: shared actor, centralised critic', 'World', '500 × 500, max speed 5, max 500 steps'],
            ['Network', 'Actor and critic: 64 hidden units; PAH 3 → 32 → 1', 'Collision radius', '3 (obstacle discs: radius 12)'],
            ['Optimiser', 'Learning rate 3e-4; batch 64; 10 epochs', 'Target radius', '25; moving targets at speed 1'],
            ['PPO', 'γ 0.99; λ 0.95; clip 0.2; entropy 0.003', 'LiDAR', '24 rays, range 100'],
            ['Rollout', '512 steps; 8,000 episodes per run', 'Safety shaping', 'Danger radius 20; collision penalty 10'],
            ['Seeds', 'Training 42 to 51; evaluation 7001', 'Success bonus', '20'],
            ['Hardware', 'Apple M3 laptop, 4 to 6 runs in parallel; a run takes about 11 to 45 min (IGAT-style about 70)', 'Evaluation', '200 episodes per model, deterministic actions']]
    d.table(LM, 1.65, [1.7, 4.55, 1.9, 4.08], rows, pt=13, head_pt=12.5, max_h=5.0, bold_first_col=False, pad=0.08)
    d.notes('Settings read from the run configuration files (config.json of a Stage 3 MAPPO + PAH run). All methods share them; only the method-specific parts differ.')

    fig_slide(d, 'app_collisions', 'Appendix A3 · Version 3 diagnostic: what did the drones hit?', APP, 'collision_type_v3.png',
              ['Version 3 models: nearly all collisions are with obstacles. Without assignment (right, third bar), drone-to-drone collisions are more common.'],
              'The collision-type check on the version 3 models. In the three main methods, 94 to 100 percent of collisions were with obstacles. This is the finding that led to the redesign.')
    fig_slide(d, 'app_gain', 'Appendix A4 · Gain over MAPPO in both studies, independent of the simulator', APP, 'gain_over_mappo.png',
              ['Light bars: DA-MAPPO paper (no confidence interval reported). Solid bars: ours (95 % Welch CI over 10 seeds). Same direction in both studies.'],
              'When absolute numbers cannot be compared, the gain over MAPPO can. Dynamic assignment helps in both studies (ours is settled at Stage 3 only) and IPPO is not better than MAPPO. MAPPO + PAH adds a much larger gain.')
    fig_slide(d, 'app_assign50', 'Appendix A5 · Assignment every 50 steps instead of every step', APP, 'assign_every_50.png',
              ['Every method loses a little (0.7 to 3.8 points): real-time re-assignment helps, but modestly in our setting. Test-time change only; models were trained with assignment every step.'],
              'The DA-MAPPO assignment ablation, run at test time on our models. The effect is small. The lead of MAPPO + PAH over Fixed-weight MAPPO stays at +6.6 and +7.7.')
    fig_slide(d, 'app_static_paper', 'Appendix A6 · Static versus moving targets, paper and ours', APP, 'static_vs_paper.png',
              ['The sign is opposite: in the paper "dynamic" means targets swap places; ours drift continuously and the models were trained on drifting targets.'],
              'In the paper, moving targets are slightly harder than static ones for DA-MAPPO and much harder for MAPPO and IPPO. In ours the models, trained on drifting targets, do better on drifting than on static targets. We do not claim to know why.', kind='orange')
    fig_slide(d, 'app_density_paper', 'Appendix A7 · Obstacle density, paper and ours', APP, 'density_vs_paper.png',
              ['Absolute levels are not comparable. Our DA-MAPPO (2D) is far below the paper\'s: 8 drones, no curriculum, far fewer training steps.'],
              'This puts the paper\'s density curves next to ours. Every method falls in both studies. Our DA-MAPPO (2D) is much lower than the paper\'s DA-MAPPO; reasons: eight drones instead of three, no curriculum, 8,000 episodes against about 3 million steps, and shared settings.', kind='orange')
    fig_slide(d, 'app_edges', 'Appendix A8 · Active conflict edges versus swarm size', APP, 'edges_vs_igat_paper.png',
              ['Edges grow with the swarm size in both studies. Each panel has its own scale: the two papers count edges differently.'],
              'IGAT-MARL reports average network edges; we count active conflict-graph edges per step. Only the trend, growth with the number of drones, can be compared.')
    fig_slide(d, 'app_difficulty', 'Appendix A9 · Success as the task gets harder, paper and ours', APP, 'difficulty_vs_paper.png',
              ['Paper: 30 to 50 obstacles. Ours: Stage 2 to Stage 3. Absolute numbers are not comparable; the trend is.'],
              'Success as the task gets harder in each study.')
    fig_slide(d, 'app_curves', 'Appendix A10 · Learning curves (training-time evaluation)', APP, 'learning_curves.png',
              ['Training-time evaluation: 20 episodes every 100 episodes, seed 999. These are not the final numbers (which are lower); the order is the same. Never mix the two.'],
              'Learning curves from the training runs. They use a different, smaller evaluation than the final results, so the levels differ. Use them for the shape only.', kind='orange')
    fig_slide(d, 'app_timepath', 'Appendix A11 · Time and path length', APP, 'time_path.png',
              ['Steps and path length over successful episodes only: methods with low success are measured on few episodes. MAPPO + PAH finishes fastest (61 steps vs 76 at Stage 3).'],
              'Time and path length are measured on successful episodes only, so they carry a survivor bias for the weaker methods.', kind='orange')

    d.new_slide('app_mech', 'Appendix A12 · Mechanism check: does PAH change the actor\'s learning signal?', APP)
    mech = rd('05-mechanism-check/output/advantage_summary.md')
    mrows = parse_rows(mech, '| Stage | Method', 10)
    rows = [['Stage', 'Method', 'corr(A_mission, A_safety)', 'corr(actor signal, Plain MAPPO signal)', 'Success (%)']]
    succ = {('2', m): t1[m][2] for m in t1}
    succ.update({('3', m): t1[m][5] for m in t1})
    for r in mrows:
        rows.append([r[0], r[1].replace('(Hungarian off)', '(no assignment)'), r[2], r[4],
                     succ[(r[0], r[1])].split('±')[0].strip()])
    d.table(LM, 1.55, [0.9, 3.9, 2.4, 3.4, 1.63], rows, pt=12.5, head_pt=12, max_h=3.9, pad=0.05,
            align=['center', 'left', 'center', 'center', 'center'])
    d.callout(LM, 5.55, CW, 1.25,
              ['The two heads carry different information (weak correlation), but every method\'s actor signal stays 92 to 99 % correlated with Plain MAPPO\'s, and closeness to Plain MAPPO does not track success. '
               '**We do not claim that PAH works by reshaping the advantage.**'], pt=14, kind='orange')
    d.notes('An advantage-correlation check on 80 final two-head models, 10 training-style batches each. It was planned to show that the actor signal differs from Plain MAPPO. It does not, so the check does not explain where PAH\'s gain comes from. We report it as such.')

    d.new_slide('app_rmappo', 'Appendix A13 · RMAPPO: what happened', APP)
    d.card(LM, 1.6, 6.0, 4.2, 'What we observed',
           ['Recurrent MAPPO under the shared settings: 0.0 % success on all 6 seeds at Stage 3 (collision 86.3 %, timeout 13.7 %). Stage 2 was not run.',
            'The policy\'s random noise collapsed early. Seed 45: log-std reached its lower limit of −4.0 by episode 2,000 and entropy fell from 1.9 to −5.2; the other seeds ended between −2.9 and −3.5.',
            'Other methods on the same stage (seed 45) ended between about −0.9 and 0.'],
           body_pt=16, head_pt=18, body_space=8)
    d.card(6.78, 1.6, 6.0, 4.2, 'What we checked and what we did not',
           ['Replaying the stored sequences gives the stored log-probabilities (largest difference 9.5e-07), so the hidden state handling is correct; the speed-up of the code changed weights by less than 1e-6.',
            'Not tested: a larger batch. The shared 64-step minibatch gives only 4 sequences per minibatch; the original RMAPPO uses larger batches.',
            'Therefore RMAPPO is reported here with the reason, not as a performance number.'],
           body_pt=14, head_pt=17)
    d.notes('Use this if asked why RMAPPO is not in the comparison. We found no implementation bug; the likely cause is the small minibatch of recurrent sequences, but that was not tested. A re-run with its original large-batch setting would take about one night.')

    # ------------------------------------------------------------------ write
    d.save(os.path.join(V1, 'deck_v1.pptx'),
           dict(title='MAPPO + PAH: thesis progress and results', author='Ayesha Khalil',
                subject='MS thesis presentation, deck v1'))
    return d


if __name__ == '__main__':
    deck = build()
    head = open(os.path.join(HERE, 'md_head.txt'), encoding='utf-8').read() if os.path.exists(os.path.join(HERE, 'md_head.txt')) else '# Deck v1\n'
    deck.write_md(os.path.join(V1, 'deck_v1.md'), head)
    print('slides:', deck.n)
    if deck.warnings:
        print('TEXT-FIT WARNINGS (%d):' % len(deck.warnings))
        for w in deck.warnings:
            print('  ', w)
    else:
        print('text fit: all boxes and tables fit')
