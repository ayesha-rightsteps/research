# PAH fix — plan (2026-10-13)

**Status:** plan + implementation + unit tests; **PAH training waits for Ayesha's go-ahead.** Plain MAPPO,
Fixed-weight MAPPO and Hand-coded τ-rule MAPPO keep training meanwhile (they contain no PAH).

## 1. The problem (measured)

Phase 1b, Stage 3, seed 42, final MAPPO + PAH model, 100 deterministic episodes: PAH's learned correction δ is
**+0.200 — the maximum — whenever τ < 1** (danger), +0.198 for 1 ≤ τ < 3, and −0.080 when safe. PAH pushes α as far as
it can **towards the mission exactly in danger**, the opposite of its purpose; it ends below its own prior
(Hand-coded τ-rule MAPPO: 86.5% vs MAPPO + PAH: 56.0% on this seed). Evidence kept in `runs_pah_v1_flawed/`.

**Cause:** PAH is trained through the actor's PPO objective. The gradient of α·A_mission + (1−α)·A_safety with respect
to α is A_mission − A_safety; in danger A_safety is strongly negative, so the gradient raises α — PAH learns to
discount safety where safety matters most. This was already seen in v3 (`docs/research/01_pah_design.md` §9.2); the
residual design only bounded it (±0.2). With separate value heads the safety advantage is a real signal, so the bias
is now fully visible.

## 2. The fix: PAH learns how much danger is ahead

| | Before (v3 residual PAH) | After (risk-learning PAH) |
|---|---|---|
| Inputs | τ, d_target, n_conflict | **same** |
| Network | 3 → 32 → 1 (ReLU) | **same** |
| Output | α = clip(α_safe(τ) + δ, 0.1, 0.9) | α = 0.9 − 0.8·p, where p ∈ (0,1) is the predicted risk |
| How it learns | gradient of the actor's PPO loss (biased, see §1) | **regression of p onto the observed safety cost-to-go** of that drone-step |
| Gradient from the actor loss | yes | **none** (α is detached in the actor loss) |

**Risk target** for each drone-step: risk = clip(−R_safety / 10, 0, 1), where R_safety is that drone's λ-return of the
safety reward (computed from the safety value head, exactly the return the safety head is trained on), and 10 is the
collision penalty — so a step that leads into a collision has risk ≈ 1, a step far from any hazard has risk ≈ 0.
PAH loss = mean squared error between p and the risk target, added to the update.

**Why this keeps the thesis claim:** PAH is still a small 2-layer network trained jointly with MAPPO that maps the
situation (τ, d_target, n_conflict) to α, and it **learns from experience** — its targets are the safety costs that
actually followed, not a hand formula (unlike the rejected "Option C", which regressed onto a formula). It can no
longer profit from ignoring safety, because its only job is to predict danger correctly.

**Unchanged:** environment, reward, two value heads, PPO settings, all other methods. The τ-rule baseline stays as
it is (it is the formula PAH used to be anchored to).

## 3. Gates (before any PAH training)

1. The actor loss sends **zero gradient** into PAH's parameters.
2. On a synthetic batch where risk falls with τ, the trained PAH's p rises as τ falls, and α is lower in danger
   than when safe.
3. Agent tests still pass (5/5), including the exact v3-compat test.
4. Smoke run of the new PAH (Stage 3, 300 episodes) with no errors; α danger < α safe.

## 4. Then

MAPPO + PAH and MAPPO + PAH (Hungarian off): 2 × 10 seeds × 2 stages = 40 runs on the laptop (4 at a time,
~3 h), same settings as every other method (PLAN.md §10). The evaluation (Step 5) reports the new PAH and keeps the
flawed v1 result as a documented finding ("a learned α trained through the policy objective is biased against safety").
