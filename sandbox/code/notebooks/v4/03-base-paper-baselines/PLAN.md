# Plan — v4 Phase 2: comparison with the base paper's methods

**Status (2026-10-14, ~02:00): Step 1 (code + tests) and Step 2 (smoke runs) done; Step 3 (main training) NOT
started — Ayesha runs it.** Written 2026-10-14 at Ayesha's request. Manish could not review in time; Ayesha:
"basic setup or jo chaheay woh kar lo jo verify karna hai toh kar lo honestly, baaqi run kal". So the §6 open
points were decided with the recommended options (fixed assignment = Hungarian at reset; one value head; IGAT
width 64, no dropout; success = every drone on its own target) — **Manish can still change them before Step 3**.
Implementation record: §7.

## 0. Why

Phase 1b answered the thesis question: MAPPO + PAH beats Fixed-weight MAPPO (Stage 3, +8.6 points [exact 8.55; half-up rounding, 2026-10-16], 95% CI
[+1.7, +15.4]; `02-redesign/README.md`). An examiner will also ask how MAPPO + PAH compares with **published
methods**. The base paper's numbers cannot be put next to ours (Gazebo, 3 drones, other obstacles, other
reward), so — as the base paper itself does — every method is trained and evaluated **in the same
environment**: ours.

## 1. What is compared (base paper main comparison + synopsis)

Sources: DA-MAPPO (`bin/91`) §V-A and Tables IV–V; the synopsis' four baselines; IGAT-MARL (`bin/9`) §3–4.

| # | Method | From | Target assignment | Teammate information | Critic | Reward |
|---|---|---|---|---|---|---|
| 1 | **IPPO** | DA-MAPPO Table V | fixed at reset | all teammates' relative positions | **local** V(oᵢ) (no shared critic) | combined 0.5 / 0.5 |
| 2 | **MAPPO** (standard) | DA-MAPPO Table V; synopsis "standard MAPPO" | fixed at reset | all teammates' relative positions | centralized | combined 0.5 / 0.5 |
| 3 | **RMAPPO** | DA-MAPPO Table V | fixed at reset | all teammates' relative positions | centralized, **recurrent (GRU)** actor and critic | combined 0.5 / 0.5 |
| 4 | **DA-MAPPO (2D)** | the base paper's own method; synopsis "DA-MAPPO ported to 2D" | **Hungarian every step** | all teammates' relative positions | centralized | combined 0.5 / 0.5 |
| 5 | **IGAT-style MAPPO** | synopsis "IGAT-MARL with a fixed assignment"; IGAT-MARL §3 | fixed at reset | **conflict graph + graph attention** (IGAT blocks) | centralized | combined 0.5 / 0.5 |

Not included: **NavRL** and **EGO-Planner v2** (DA-MAPPO's two non-MARL baselines). Both are 3D navigation
stacks (a safety-shielded RL navigator and a trajectory optimizer); a faithful 2D port is a project of its own.
The thesis states this. (Can be revisited if the supervisor asks.)

**Already trained in Phase 1b and evaluated with the same protocol** (no retraining; they go in the same
final table): Plain MAPPO, Fixed-weight MAPPO, Hand-coded τ-rule MAPPO, MAPPO + PAH, MAPPO + PAH (Hungarian off).

How the methods relate (one switch at a time):

```
MAPPO (fixed assignment, teammates)  --Hungarian every step-->  DA-MAPPO (2D)
DA-MAPPO (2D)  --conflict-graph neighbours instead of all teammates-->  Plain MAPPO (Phase 1b)
Plain MAPPO  --mission + safety value heads, α = 0.5-->  Fixed-weight MAPPO  --learned α (PAH)-->  MAPPO + PAH
MAPPO  --no centralized critic-->  IPPO          MAPPO  --GRU memory-->  RMAPPO
MAPPO  --graph attention over the conflict graph instead of all teammates-->  IGAT-style MAPPO
```

## 2. Design details (what the papers say, and what we decide where they are silent)

**2.1 Fixed assignment ("rigid assignment").** DA-MAPPO: the baselines "without dynamic reallocation incur
longer paths due to the pursuit of outdated targets … rigid assignments force UAVs to pursue suboptimal goals".
The paper does **not** say how the rigid assignment is chosen. **Decision: Hungarian once at reset, then
fixed** — the best possible start for the baselines, so their weakness is only the missing reallocation, not a
bad pairing. (Our Phase 1b ablation "Hungarian off" used an arbitrary pairing; it stays as it is — a different
question.) → **Manish: please confirm.**

**2.2 Teammate information without a conflict graph.** DA-MAPPO's observation has a "swarm topology" part:
the relative positions (Δx, Δy) of **all** teammates, concatenated. Our methods 1–4 get exactly that in place of
our 4 conflict-neighbour slots: 2(N−1) values (8 at Stage 2, 14 at Stage 3), ordered by drone index, scaled by
the world size like our other position features. Everything else in the observation is unchanged (own position,
velocity, target offset, 24 LiDAR rays).

**2.3 Reward and critic.** DA-MAPPO uses one reward and one critic. All five baselines therefore use **one value
head and our reward combined with fixed weights 0.5 / 0.5** — the same reward Plain MAPPO used in Phase 1b.
We use our reward, not DA-MAPPO's (team / progress / LiDAR / acceleration terms): the environment and its reward
must be the same for every method; only the algorithm changes.

**2.4 IPPO.** "Fully decentralized PPO in which each agent learns independently without shared critic
information" (DA-MAPPO §V-A). Critic input = the drone's own observation (dim = obs dim), not the joint state.
Actor and critic parameters shared across drones (standard practice; the paper does not say otherwise).

**2.5 RMAPPO.** MAPPO with a GRU (hidden 64) after the first layer of actor and critic. Rollouts store the GRU
hidden state; the PPO update runs on chunks of 16 consecutive steps starting from the stored hidden state; the
hidden state is reset at episode start. (DA-MAPPO cites the original MAPPO paper for RMAPPO; this is the chunked
recurrent update used there.)

**2.6 IGAT-style MAPPO.** From IGAT-MARL §3: conflict-graph adjacency (our DCPA/TCPA graph, horizon 3);
graph attention with masked neighbours, 4 heads, **2 IGAT blocks × 2 GAT layers**, residual + LayerNorm after each
layer. Node input = each drone's own observation (position, velocity, target offset, LiDAR); each drone attends
only to itself and its current conflict neighbours. Differences from IGAT-MARL, stated in the thesis: PPO instead
of DQN, continuous instead of 3 discrete heading actions, width 64 (not 128) and no dropout (same size as every
other method; dropout is not standard in PPO), and it has target assignment (fixed) because our task has targets.

**2.7 Same for every method (fairness, as in Phase 1b §3).** Environment and settings of PLAN 02 §10 (Stage 2:
5 drones / 10 discs; Stage 3: 8 drones / 20 discs; danger 20; collision −10), PPO settings (lr 3e-4, entropy
0.003, hidden 64, 10 epochs, batch 64, 512-step rollouts), 8000 episodes, seeds 42–51, from scratch, **no tuning
for any method**. DA-MAPPO also trains every algorithm with "identical network architectures and hyperparameter
settings" (§V-A).

## 3. Questions and reading rule (fixed now, before any run)

- **Primary (Phase 2):** Stage 3, **MAPPO + PAH vs DA-MAPPO (2D)** — our method vs the base paper's method — success.
- **Secondary:** MAPPO + PAH vs each of IPPO, MAPPO, RMAPPO, IGAT-style MAPPO; the same at Stage 2;
  DA-MAPPO (2D) vs MAPPO (does per-step reassignment help in our environment, as the base paper reports?).
- **Reading rule:** as PLAN 02 §5 — difference in mean success over 10 vs 10 seeds, 95% Welch CI; above 0 →
  better, below 0 → worse, inside ±3 and containing 0 → equivalent, otherwise inconclusive. Reported as it comes out.
- **Table:** the base paper's Table V format (success / collision / timeout / T_ave / L_ave), all 10 methods.

## 4. Steps and gates

**Step 1 — code (`v4/common/`).**
- `env_v4.py`: two switches, default off so Phase 1b behaviour is unchanged — `assignment='every-step' |
  'fixed-at-reset' | 'fixed-arbitrary'` (the last = Phase 1b "Hungarian off") and `teammates='conflict' | 'all'`.
- `mappo_v4.py`: IPPO critic option, GRU actor/critic (RMAPPO), IGAT encoder.
- *Gates (unit tests):* existing 13 env + 7 agent tests still pass unchanged (Phase 1b behaviour intact);
  fixed-at-reset equals Hungarian at step 0 and never changes; all-teammates block equals hand-computed relative
  positions; IPPO critic sees only the drone's own observation; RMAPPO: re-evaluating a stored chunk before the
  first update gives log-probabilities equal to those at collection time (ratio = 1), and the hidden state is reset
  at episode start; IGAT: changing a drone that is **not** a conflict neighbour of drone i leaves drone i's action
  unchanged, while changing a neighbour does change it.

**Step 2 — smoke runs.** Each new method, Stage 3, 300 episodes, sanity seed 101: no errors, success rises
above a random policy, speed measured. Not used for any decision about settings.

**Step 3 — main training.** 5 methods × 10 seeds × 2 stages = **100 runs**, laptop, 4 in parallel, overnight
(`caffeinate`, charger). Check every run's `config.json` right after launch.

**Step 4 — evaluation.** `02-redesign/evaluate.py` unchanged (200 episodes, seed 7001, each model from its own
config) + `summarize.py` extended with the new methods; one final table with all 10 methods.

## 5. Time estimate

| Step | Time |
|---|---|
| Manish's review of this plan | his time |
| Step 1: code + tests (IGAT and RMAPPO are the largest parts) | 2–3 days |
| Step 2: smoke runs | ~1 hour |
| Step 3: 100 runs (RMAPPO and IGAT-style are slower; estimate from Step 2) | ~3 nights |
| Step 4: evaluation, tables, figures, write-up | ~half a day |
| **Total** | **~1 week** |

## 6. Open points for Manish

1. §2.1 — fixed assignment = Hungarian at reset (recommended) or an arbitrary pairing?
2. §2.3 — baselines on one value head with our combined reward (recommended; faithful to the papers), or also
   give them two heads? (Two heads would make them new methods, not the published ones.)
3. §2.6 — IGAT-style width 64 / no dropout (recommended, fairness) vs IGAT's 128 / dropout 0.6.
4. Success definition with a fixed assignment: every drone must reach **its own** assigned target (as in DA-MAPPO:
   "all UAVs successfully reach their assigned targets"). A drone on another drone's target does not count.

## 7. Implementation record (2026-10-14)

- `common/env_v4.py`: switches `assignment` and `teammates` (defaults = Phase 1b). Phase 1b tests 13/13 pass;
  Phase 1b final evaluation reproduced **identically** on 3 models after the change (outcomes, T, L, α).
- `common/baselines_v4.py`: IPPO, RMAPPO, IGAT-style agents + method table. MAPPO and DA-MAPPO (2D) reuse the
  Phase 1b Plain MAPPO agent (no new agent code).
- `common/test_baselines_v4.py`: 7/7 pass; Phase 1b agent tests 7/7 still pass. Three tests were checked
  against deliberately broken code (hidden state not reset; no graph masking; fixed assignment re-solved) —
  each break is caught.
- `train_baselines.py` (this folder): the 02 `train.py` loop with the method's agent and environment switches.
- `02-redesign/evaluate.py`: `--phase2` mode; builds Phase 2 models from their config.
- **Smoke runs** (Stage 3, 300 episodes, seed 101; `smoke/`): all five run without errors; configs checked.
- **Speed:** IPPO / MAPPO / DA-MAPPO / IGAT-style ≈ Plain MAPPO (2.5–4 min per 300 episodes with 5 in parallel).
  **RMAPPO is ~8–10× slower per update** (backprop through 16-step chunks, 640 minibatches per update with the
  common batch size of 64): estimated ~2–2.5 h per Stage 3 run and ~1.3 h per Stage 2 run at 4 in parallel.
  Kept the common batch size (fairness, §2.7) rather than RMAPPO's usual full-batch update.
- **Main training estimate:** ~60 slot-hours → **~15 h at 4 in parallel** (~10 h at 6). Launcher:
  `runs/run_phase2.sh` (jobs longest-first: `runs/jobs.txt`). Not launched.
- **Learning check** (Stage 2, 2000 episodes, sanity seed 101; `smoke/learn2-*`; training-time success, last 5
  evaluations): IPPO 74%, MAPPO 57%, DA-MAPPO (2D) 70%, IGAT-style 73% — Phase 1b Plain MAPPO at the same point
  (seed 42) 63%, Fixed-weight MAPPO 68%. All four learn. **RMAPPO was only smoke-tested** (300 episodes in 14.5 min
  alone, no errors); its learning was not checked — a 2000-episode check would take ~45–60 min.
