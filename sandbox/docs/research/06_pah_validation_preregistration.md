# 06 — PAH Validation Pre-Registration (DRAFT — needs Ayesha + Manish sign-off)

**Status: proposal, not yet adopted.** Written 2026-09-18 after a session of
`prior_coef` tuning (0.15 → 0.30 → 0.45) and a two-head-critic attempt both
failed to reliably fix a seed-dependent bug in PAH's danger-close behavior
(full history: `sessions/2026-09-18.md`). Reframes the immediate PAH
validation question narrower and more defensibly, per outside review. This
document itself changes nothing in `code/` — it is the plan to agree on
*before* the next code/experiment changes, per `docs/plans/00_master_plan.md`
("No change to the PAH core idea without asking Ayesha and Manish").

---

## 1. Why this document exists

Across 2026-09-16 through 2026-09-18 we iterated on PAH's α-direction bug
(danger-close situations should push α low/safety-focused) through several
fixes — tau-informed prior, danger-weighted prior, `prior_coef` sweeps,
a two-head critic — each tested, several looking good on 1–3 seeds, none
holding up across the full 5-seed set. Two structural problems came out of
that:

1. **We were tuning `prior_coef` partly by looking at seed 45's result, then
   including seed 45 in the "final" 5-seed table.** That is tuning on the
   evaluation data — the 34%→38% "no real improvement" combined result
   (Section 14 of `sessions/2026-09-18.md`) is the honest number, but the
   process that got us to `prior_coef=0.45` was not clean.
2. **Our success criterion (danger → low α, "direction agreement") is a
   proxy we designed, not the outcome that matters.** If α is trained with
   a prior that pulls it toward a τ-formula, and we then judge success by
   how well α matches that formula, we cannot honestly claim PAH
   *discovered* safety-first behavior from experience — we may just be
   watching it approach the equation we wrote by hand.

This document fixes the *process* before we touch the *mechanism* again.

---

## 2. The exact claim we are testing

> **Does context-aware priority arbitration (a learned correction to a
> transparent τ-based safety rule) improve the collision/success trade-off
> beyond (a) a fixed weight and (b) the hand-designed safety rule alone —
> consistently across seeds and on scenarios not used for tuning?**

This is narrower than the original thesis claim ("PAH learns α from
situation, existing work uses fixed α"). It is still the same core idea,
but it separates "does *adaptive* weighting help at all" from "does the
*learned* part add anything beyond a rule we could have written down
directly" — which is exactly the distinction our results so far cannot make.

---

## 3. The three methods (all three needed — this is the point)

| ID | Method | α source | What it isolates |
|----|--------|----------|-------------------|
| **B4** | Fixed α = 0.5 | constant | Is *any* adaptive weighting useful at all? |
| **H** (new) | Hand-coded τ-rule | `α = alpha_min + (alpha_max−alpha_min)·τ_norm`, no learning, no network | Is the improvement just the known safety heuristic, with zero learning? |
| **M** (PAH) | **Prior + learned residual**: `α(s) = clip(α_H(τ) + Δα_φ(s), alpha_min, alpha_max)`, where `α_H(τ)` is exactly H's rule and `Δα_φ(s)` is a small learned correction from `(τ, d_target, n_conflict)`, regularized toward **zero** (not toward the formula) | Does learning add value *beyond* the heuristic? |

**Why H matters and is currently missing:** right now we only compare
B4 vs M. If M's α ends up closely tracking the τ-formula (which the
danger-weighted prior actively pulls it toward), M vs B4 cannot tell us
whether the win — if any — came from adaptivity in general (which H alone
could also deliver, with zero learning and zero training instability) or
from something PAH's learning genuinely discovered. **Without H, a positive
M result does not support the thesis's "learned" claim.**

**Why M is redefined as prior + residual, not a free-form learned α:**
this directly removes the race/lock-in bug diagnosed in
`sessions/2026-09-18.md` Section 15 — `α_H(τ)` is structurally always
present (not something that can be "lost" if the actor loss wins an early
race), so M can never behave worse than H on the τ-dimension; the residual
is regularized toward zero so it only earns a role in the loss if it
demonstrably lowers loss beyond what H already gets for free. **This is a
change to PAH's formulation (not just training procedure) and needs
Ayesha's explicit sign-off, not only Manish's**, per the master plan's
"no change to the PAH core idea without asking Ayesha and Manish" rule.

---

## 4. Seeds and held-out scenarios

- **Training seeds: 42, 43, 44, 45, 46** (unchanged — same 5 already used
  all session, kept for continuity with existing exploratory runs).
- **`prior_coef` (or any other hyperparameter) is chosen using training-seed
  behavior only, then frozen. It is never adjusted after looking at eval
  results.** This is the rule we broke this session (Section 1 above) —
  writing it down here so it cannot happen quietly again.
- **Evaluation uses a separate, disjoint set of seeds/episode layouts** not
  used anywhere during training or tuning — per `docs/plans/
  02_experiment_protocol.md`'s existing eval procedure (N_eval=200,
  fixed/disjoint eval seeds, deterministic policy, no gradient updates).
  We have **not** been doing this cleanly for the PAH-direction checks this
  session (the `eval_alpha_low_tau`/`high_tau` diagnostic ran on the same
  seed being trained) — this must change for any claim that counts.
- **Held-out scenario suite** (stretch goal, do after the core 3-method
  comparison, not before): low-conflict/open-space, sudden near-collision,
  dense obstacle corridor, mission-urgency-vs-safety conflict, and a
  drones/obstacle-density variation. Purpose: the ~90% average success rate
  we have seen everywhere this session may be hiding the actual effect —
  these scenarios are chosen to separate the methods, not to make PAH look
  good.

---

## 5. Primary measure — what decides whether PAH (M) helps

**Primary:** Mission Success Rate and collision rate (both — not one traded
for the other), per `docs/plans/02_experiment_protocol.md`'s existing MSR
definition, compared M vs H vs B4, mean ± std over the 5 training seeds,
evaluated on the held-out eval seeds.

**Decision rule (Welch's t-test or bootstrap CI, per existing protocol
Section "Decision rule"):**

- **M beats B4** if MSR(M) ≥ MSR(B4) with non-overlapping 95% CIs, and
  collision rate of M ≤ B4's. (Tests: does adaptivity help at all.)
- **M beats H** if MSR(M) ≥ MSR(H) with non-overlapping 95% CIs, and
  collision rate of M ≤ H's, **and** the learned residual `Δα_φ` is
  non-trivial (not collapsed to ~0 everywhere). (Tests: does *learning*
  add value beyond the rule.)

**α-direction agreement (danger → low α) is demoted to a secondary
sanity check, not the primary criterion** — per the outside review this
session: it is a proxy for "did training behave as expected," not proof of
outcome quality. A case where α "disagrees" with the naive danger-low rule
but produces a good outcome (e.g. geometry legitimately favors holding
mission priority) is not automatically a failure.

---

## 6. What result makes us abandon the "learned PAH is better" claim

Written in advance, per the outside review's recommendation, so we cannot
move the goalposts after seeing results:

- **If M does not beat B4:** adaptive weighting itself does not help in
  this setup — report that fixed-α is sufficient, a negative-but-honest
  result (`docs/plans/02_experiment_protocol.md` already commits us to
  reporting negative results honestly).
- **If M beats B4 but does not beat H (residual `Δα_φ` stays ~0, or beats H
  only within noise):** report the simpler, interpretable H (hand-coded
  τ-rule) as the finding — "adaptive, transparent arbitration beats fixed
  weighting; a learned correction on top of it does not add measurable
  value in this setup." This is still a legitimate, defensible thesis
  contribution, just a narrower one than originally hoped.
- **If M is unreliable across seeds even with the residual reframe** (repeat
  of this session's seed-dependence, now on the *residual's* behavior
  rather than the whole α): report the instability itself as a finding,
  and narrow the thesis claim accordingly rather than continuing to chase
  a clean result with more tuning.

---

## 7. What this document does NOT decide

- Whether to actually build the residual-PAH architecture and the canonical
  `code/`-based runner (vs. notebooks) — that is an implementation decision
  for a separate work session, once this document is agreed.
- The full held-out scenario suite's exact parameters — sketched in
  Section 4, to be filled in when we get there.
- Anything about Stage 3 (8 drones) — this document is scoped to finishing
  Stage 2 validation cleanly first, per the master plan's phase ordering.

---

## 8. Open items for Ayesha

- Sign-off on the residual reframing (`α = clip(α_H(τ) + Δα_φ(s), ...)`)
  as PAH's formulation going forward — this is a change to the core idea
  and needs her agreement, not just Manish's (`docs/plans/00_master_plan.md`).
  See `docs/research/04_open_questions_for_supervisor.md` — this may also
  be worth flagging to the supervisor given it is a deviation from the
  originally-described "α weights the reward" formulation.
- Agreement on the narrowed claim in Section 2 — it is honest and
  defensible, but it is a smaller claim than "PAH learns α from the
  situation" as originally pitched in the synopsis language.
