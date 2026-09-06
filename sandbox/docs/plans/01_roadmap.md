# 01 — Roadmap (detailed)

Phase-by-phase task breakdown with dependencies and done-criteria. Paced against the
approved synopsis 12-month Gantt.

---

## Synopsis Gantt (approved) vs our phases

| Synopsis task | Months | Our phases |
|---------------|--------|-----------|
| Task-I: 2D env setup + DA-MAPPO replication baseline | 1–2 | P0 + P1 + start of P2 |
| Task-II: Assignment-augmented obs + conflict graph integration | 3–4 | P2 + P3 |
| Task-III: Curriculum training 3→5→8 drones | 5–7 | P4 |
| Task-IV: Systematic evaluation vs 4 baselines (3 swarm sizes × 3 obstacle densities) | 8–9 | P5 |
| Task-V: Ablation experiments + failure-case analysis | 10–11 | P5 |
| Task-VI: Thesis writing | 12 | P6 |

**Reality check on Task-I:** "2D env + DA-MAPPO replication in 2 months" is tight if
Python/PyTorch are still being learned. The honest split: env with tests ≈ 3–5 weeks,
minimal MAPPO ≈ 3–4 weeks, getting Stage-1 to actually converge ≈ 2–4 weeks of
debugging. Budget Task-I as "env + MAPPO core running", push full DA-MAPPO replication
into month 3. Tell the supervisor this early.

---

## P0 — Formalization (weeks 1–3)

| Task | Depends on | Done when |
|------|-----------|-----------|
| Write `docs/research/00_problem_formalization.md` (MDP, obs, action, reward) | synopsis, DA-MAPPO/IGAT notes | reward terms have formulas; parameter table filled with proposed values |
| Write `docs/research/01_pah_design.md` (formulations + reward-hacking analysis) | 00 | ≥ 3 candidate PAH training rules with pros/cons + a recommendation |
| Write `docs/research/02_assignment_and_conflict.md` (Hungarian + TTC math) | 00 | closed-form TTC written; anti-thrashing options listed |
| Fill `docs/research/03_baseline_specs.md` parameter tables from the PDFs | DA-MAPPO + IGAT PDFs in `bin/` | every row verified against a page number in the PDF |
| Send `docs/research/04_open_questions_for_supervisor.md` to the supervisor | 00–03 | written answers / sign-off received |

**Output:** reviewed design docs. **Risk:** supervisor slow to respond → start P1 in
parallel (env work does not depend on the PAH answer).

---

## P1 — Environment (weeks 2–7, overlaps P0)

| Task | Done when |
|------|-----------|
| `code/environment/multi_uav_env.py` — reset, step, obs, reward, termination | runs end-to-end with random actions, no crashes |
| Point-mass 2D kinematics, speed clamp, world bounds | position update + clamp unit-tested |
| Obstacle field (static), collision detection (drone–drone, drone–obstacle, boundary) | collision unit tests pass for hand-built cases |
| Target generation + assignment hook (calls `hungarian.py`) | assigned-target field appears in obs, updates when positions change |
| Reward implementation (mission + safety terms) | sign of each term unit-tested (progress → +, collision → −) |
| Vectorized wrapper (run B env copies with batched numpy) | 32 envs step in parallel, output shapes correct |
| `code/environment/rendering.py` — matplotlib episode viewer | can watch a scripted agent reach its target |
| Determinism: same seed → same episode | byte-identical trajectory unit test |
| Scripted-policy sanity: "head straight to assigned target, ignore others" | high success with 1–3 drones, no obstacles |

**Output:** trusted env + `code/tests/test_env.py`. **This phase is the foundation —
do not rush it.**

---

## P2 — MAPPO core (weeks 6–10)

| Task | Done when |
|------|-----------|
| `code/algorithms/mappo.py` — shared actor, centralized critic, rollout buffer, GAE, PPO clipped loss, entropy bonus | code reviewed, ~300–400 lines, readable |
| Config system (`code/configs/*.yaml`) wired in | no hyperparameter hardcoded |
| Logging (TensorBoard) — return, episode length, losses, entropy, KL | curves visible during training |
| Checkpoint save/resume | training resumes from checkpoint with matching curve |
| Sanity 1: MAPPO on a 1-drone go-to-target task | converges to near-100% success |
| Sanity 2: MAPPO on a standard Gym task (e.g. a simple continuous-control env) | reaches known reference return |
| **Standard-MAPPO baseline** on Stage-1 env (3 drones, static targets, no obstacles) | trains stably; a meaningful success rate (not necessarily high yet) |

**Output:** working MAPPO + baseline 1 of 4. **Risk:** MAPPO instability → the sanity
tasks isolate whether it is the algorithm or the env.

---

## P3 — Assignment + conflict graph (weeks 10–14)

| Task | Done when |
|------|-----------|
| `code/algorithms/hungarian.py` — cost matrix + `linear_sum_assignment` wrapper | unit-tested against hand-solved 3×3 cases |
| Assignment-augmented observation (distance + bearing to assigned target) | matches `docs/research/00` spec |
| `code/algorithms/conflict_graph.py` — DCPA/TCPA, adjacency, degree, neighbor list | TTC unit-tested against analytic cases |
| Conflict-neighbor slots in obs (fixed K, sorted by TTC, zero-padded + mask) | shape fixed regardless of actual neighbor count |
| **DA-MAPPO-2D baseline** (assignment ON, conflict graph OFF) | trains; success clearly above Standard-MAPPO on Stage 1 |
| **Assignment ablation check** — remove assignment aug from a trained-style config | success collapses (DA-MAPPO Table VI reports → 0%); if it does not, investigate |
| **IGAT-style baseline** (conflict graph ON, real-time assignment OFF) | trains; documented as a MAPPO adaptation, not a DQN reproduction |
| "Target reassignments per episode" metric logged | visible; if thrashing appears, add switching-cost term (see `02`) |

**Output:** baselines 2 and 3 of 4; the key ablation result.

---

## P4 — Priority Arbitration Head (weeks 14–20)

| Task | Done when |
|------|-----------|
| `code/algorithms/pah.py` — batched MLP, input normalization, `α ∈ [0,1]` output | forward pass works on `[B, 3]` tensors; gradients flow |
| PAH inputs computed in env/wrapper: `τ_collision`, `d_target`, `n_conflict` | each normalized per `docs/research/01` |
| Chosen PAH training rule integrated into MAPPO update | per the supervisor-approved formulation in `01` |
| α regularizer / prior (if used) | configurable; off by default, sweepable |
| **Full model** (assignment + conflict graph + PAH) on Stage 1 | trains stably; α does not collapse to a constant |
| **Fixed-α baseline sweep** — α ∈ {0.3, 0.5, 0.7} (values TBD), full model otherwise | all runs complete, ≥ 5 seeds each |
| Curriculum: Stage 1 → 2 → 3 with weight transfer | each stage converges; transfer helps early reward (IGAT reports ~34% at N=4) |
| α-vs-context diagnostic plot (α vs τ_collision, α vs n_conflict) | produced; this is a core thesis figure |

**Output:** the novel contribution, running; the fixed-α comparison data.

---

## P5 — Evaluation + ablation (weeks 20–28)

| Task | Done when |
|------|-----------|
| `code/evaluation/evaluate.py` — fixed eval seeds, N_eval episodes, all metrics | see `02_experiment_protocol.md` |
| Full grid: {3, 5, 8} drones × {low, med, high} obstacle density × {all baselines + full model} | every cell has ≥ 5 seeds |
| Stage 4: unseen swarm sizes (generalization) | full model + best baseline evaluated on sizes not trained on |
| Ablation matrix (drop conflict graph / drop assignment / fixed-α / no regularizer) | table complete |
| `code/evaluation/make_results_table.py` — CSV → thesis tables | tables regenerate from raw logs with one command |
| Plots: learning curves, success-rate bars with CI, α diagnostics, trajectory renders | all in `code/results/plots/` |
| Failure-case analysis — watch failed episodes, categorize | short write-up in `docs/research/` |
| **The verdict:** does PAH beat the best fixed-α? | stated with numbers + CIs per the protocol's decision rule |

**Output:** all results. **If PAH does not beat fixed-α:** that is still a thesis —
report it honestly, analyze why, this is a valid negative result.

---

## P6 — Writing (weeks 28–34)

Chapters map to the docs: intro/related work (synopsis + `bin/` handbooks), method
(`docs/research/00`–`02`), experiments (`02_experiment_protocol.md`), results
(`code/results/`), discussion (failure analysis + `05_critical_analysis` style).

---

## Standing risks (see also `00_master_plan.md`)

| Risk | Mitigation |
|------|-----------|
| PAH reward-hacking (agent games its own reward weight) | analyzed up front in `docs/research/01`; fallback formulation ready |
| Assignment thrashing | metric logged from P3; switching-cost term on standby |
| Variable-length neighbor obs | fixed-K padding + mask decided in P0 |
| MAPPO won't converge | sanity tasks in P2 isolate algorithm vs env |
| Compute / time overrun | vectorized env (CPU), free Kaggle GPU, checkpoint often |
| Supervisor unavailable for P0 sign-off | P1 runs in parallel; escalate deviations in writing early |
| Scale of coding vs skill level | pair on it, keep code simple, lean on the session log for continuity |
