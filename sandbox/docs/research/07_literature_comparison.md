# 07 — Literature Comparison: Our Results vs Two Base Papers

**Presentation version:** a visual, chart-based version of this doc exists
as a private Artifact — https://claude.ai/artifact/GQTD3VBaacCbfNuvEh3cB6
("Multi-UAV Literature Comparison"). Built 2026-09-30 for Manish to show
his supervisor. Contains the same content as this file, plus two SVG bar
charts (all-methods-sorted comparison, and a two-panel effect-size chart
contrasting DA-MAPPO's 99-point ablation swing against our 0.2-point
α-source spread) and a ready-to-read presentation script. Same numbers as
below — nothing in the artifact was computed separately or differs from
what's in this file. Private (owner-only) unless shared from its page.

**Status: initial comparison, 2026-09-30.** Compares our Stage 2/Stage 3
results (B4, H, M — `sessions/2026-09-18.md` Section 24, `sessions/
2026-09-19.md` Section 11) against two of the project's base papers:

- **`bin/91`** — *Dynamic Target Assignment and Cooperative Decision-Making
  for...* (DA-MAPPO). Same problem family as ours (multi-UAV target
  assignment + collision avoidance, MAPPO-based), same primary metric
  (success rate / collision rate) — the most directly comparable paper.
- **`bin/9`** — *Efficient multi-agent deep reinforcement learning
  algorithm for multi UAV collision avoidance* (IGAT-MARL). Conflict-graph
  attention + DQN, different metric family (cumulative reward,
  loss-of-separation time, edge count) — conceptually related to our
  conflict-graph component, but not directly number-comparable.

**Important caveat up front, read before any number below:** neither
paper's environment matches ours in scale. DA-MAPPO tests **N=3 drones**
against **30–50 static/dynamic obstacles**. IGAT-MARL tests **N=3–10**
against a fixed-wing airspace-conflict setup, not obstacle-dense
navigation. Our Stage 2 is **5 drones, 5 obstacles**; Stage 3 is **8
drones, 10 obstacles**. Fewer obstacles per drone, different geometry —
**a lower success rate or a higher one than these papers does not, by
itself, mean our method is worse or better.** This comparison is for
context and sanity-checking, not a head-to-head claim.

---

## 1. Comparison vs DA-MAPPO (`bin/91`)

### Their numbers (Table V, dynamic targets — their main result)

| Method | ENV-1 (30 obs) | ENV-2 (40 obs) | ENV-3 (50 obs) |
|---|---|---|---|
| IPPO | 78% | — | 53% |
| MAPPO | 83% | — | 64% |
| RMAPPO | 85% | — | 67% |
| NavRL | 63% | — | 32% |
| EGO-Planner v2 | 53% | — | 43% |
| **DA-MAPPO** | **99%** | **95%** | **90%** |

(Collision rate = 100% − success%, since their episodes only end in
success or collision within the time limit, same as ours.)

### Our numbers

| Stage | Config | B4 (fixed α=0.5) | H (τ-formula) | M (PAH residual) |
|---|---|---|---|---|
| Stage 2 | 5 drones, 5 obstacles | 91.0% / 9.0% | 90.8% / 9.2% | 90.9% / 9.1% |
| Stage 3 (seed 42 only) | 8 drones, 10 obstacles | 74.7% / 25.3% | *(not run yet)* | 74.8% / 25.2% |

### Reading this honestly

- **Stage 2 (91%) sits inside DA-MAPPO's range** (90–99% across their three
  densities) — reasonable, given our Stage 2 (5 obstacles) is far less
  cluttered than even their easiest environment (30 obstacles). Not
  surprising it's on the easier end of their range rather than beating
  their best number — we have far fewer obstacles to navigate, but also
  more drones (5 vs their 3) sharing that same space, so it isn't a clean
  "we have it easier" comparison either.
- **Stage 3 (74.7–74.8%) is meaningfully below their whole range**, including
  their hardest environment (ENV-3, 90%). This is worth sitting with
  honestly: even though Stage 3 has fewer obstacles (10) than any of their
  environments (30–50), our success rate is lower than their worst case.
  The most likely explanation, in order of plausibility:
  1. **More drones, same relative space** — 8 drones in a fixed 500×500
     world is a much higher drone-density-per-obstacle-free-area situation
     than their 3-drone setup, even with fewer obstacles. Drone-drone
     conflict, not drone-obstacle conflict, may be the dominant failure
     mode in our Stage 3 (worth checking directly — see Section 3 below).
  2. **Fresh-critic warm-start growing pains** — Stage 3's freeze-first
     critic warm-start (`sessions/2026-09-19.md` Section 9) showed
     `critic_loss` still oscillating around the unfreeze point in the
     one seed run so far — the policy may not be fully converged yet.
     DA-MAPPO's numbers come from fully-converged, dedicated per-environment
     training runs.
  3. Only **one Stage 3 seed** exists so far — this number could move with
     more seeds or a longer/adjusted freeze schedule.
- **DA-MAPPO's baselines (MAPPO 83%/64%, RMAPPO 85%/67%) are closer to our
  Stage 2 numbers than DA-MAPPO's own headline result is** — meaning our
  B4 (plain fixed-weight MAPPO-style baseline) is roughly in the same
  ballpark as other papers' plain MAPPO/RMAPPO baselines at comparable
  difficulty, which is a reasonable sanity check that our environment/
  training pipeline isn't badly broken.

### What DA-MAPPO's ablation (Table VI) suggests for us

Their most telling result: **removing the assignment-augmented observation
drops their success rate to 0%.** This is a much stronger effect than
anything we have seen from varying `α` (adaptive vs fixed vs formula) — our
three methods differ by ~0.2 percentage points, nowhere near a 0%-vs-90%
gap. This lines up with `docs/plans/02_experiment_protocol.md`'s B1/B2/B3
plan: **the Hungarian-assignment and conflict-graph components are likely
where the large effect sizes are, not the α-arbitration mechanism** — which
is exactly what the Stage 2/3 null result (Section 24) already suggested,
and now has independent support from a paper doing the equivalent ablation
on the assignment piece specifically.

---

## 2. Comparison vs IGAT-MARL (`bin/9`)

**Not directly number-comparable** — different metrics (cumulative reward,
loss-of-separation time steps, interaction-edge count vs our success%/
collision%), different task framing (discrete 3-action airspace conflict
resolution vs our continuous 2D navigation + assignment). No attempt is
made here to convert one metric family into the other — that would produce
a misleading precision that doesn't exist.

**What is comparable — the design lesson, not the numbers:**

- IGAT-MARL's Table 7 (architecture ablation) shows every reduction in
  attention depth **monotonically degrades all three of their metrics**
  (reward, LoS, edges) — a clean, large, consistent effect from a
  structural design choice (how much of the graph-attention stack is kept).
- Their action-distribution result (Table 5) is conceptually close to our
  own α-direction diagnostic: they found their DGN benchmark baseline was
  biased toward "do nothing" ~49% of the time, while IGAT distributed
  actions near-uniformly, and they read this as evidence of genuinely
  situation-aware decisions. **Our own PAH (M) direction-check was
  perfect (0% wrong, Sections 19/24 across both stages) but the *outcome*
  metrics still tied with B4/H** — i.e., we had IGAT's kind of clean,
  situationally-correct signal (their Table 5's story), but unlike them,
  it didn't translate into an outcome advantage. This is a useful contrast
  to have on record: "the mechanism behaved correctly" and "the mechanism
  changed the outcome" are two different claims, and IGAT-MARL's paper
  is a case where a paper had both; ours currently only has the first.

---

## 3. Follow-up this comparison motivates (not yet done)

- **Check whether Stage 3's higher collision rate (25%) is drone-drone or
  drone-obstacle.** `MultiUAVEnv` should already distinguish these
  internally (or can be added cheaply) — if it's dominated by drone-drone
  conflict, that supports explanation (1) above (drone density, not
  obstacle density, is the bottleneck at Stage 3) and would be a concrete,
  useful thing to say in the thesis about *why* Stage 3 is harder than
  Stage 2, independent of the α-arbitration question.
- **B1/B2/B3 baselines** (already planned, `sessions/2026-09-19.md` Section
  12, Option A) — DA-MAPPO's ablation result (Section 1 above) makes this
  more clearly worth doing, not less: the assignment/conflict-graph
  components look like where a comparably large effect could actually show
  up, based on what a directly-comparable paper found.
- **More Stage 3 seeds**, once the `freeze_episodes` question
  (`sessions/2026-09-19.md` Section 9) is resolved — right now Stage 3's
  number is from a single seed with a critic that may not be fully
  converged (Section 1, explanation 2 above).
