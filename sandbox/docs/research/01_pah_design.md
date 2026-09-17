# 01 — Priority Arbitration Head (PAH) Design

This is the **novel contribution** of the thesis. This document works out how it is
actually built and trained, and flags the one real design risk.

---

## 1. What the synopsis says

> "A Priority Arbitration Head is introduced to dynamically balance the two objectives
> at each decision step by learning state-dependent objective weights, replacing static
> reward weighting."
>
> "It outputs a single dynamic weight α ∈ [0,1]. The arbitration head adds no
> parameters to the centralized critic and requires no separate training loop — its
> weights are updated jointly with the MAPPO actor at each gradient step."

Inputs (3 scalars, per drone, per step):

| Input | Meaning | How computed |
|-------|---------|--------------|
| `τ_collision` | time-to-collision with the nearest drone on a collision course | `t*` from the conflict-graph CPA computation (see `02`); `+∞` → clip to `H` if no conflict |
| `d_target` | distance to the assigned target | from the Hungarian assignment |
| `n_conflict` | number of conflict-graph neighbors | node degree in the adjacency matrix |

Output: `α ∈ [0,1]`. Reward: `r = α·r_mission + (1−α)·r_safety`.

Meaning: `α → 1` = "focus on the mission", `α → 0` = "focus on staying safe".

---

## 2. The architecture (fixed part)

```python
class PriorityArbitrationHead(nn.Module):
    """Maps (tau_collision, d_target, n_conflict) -> alpha in [0, 1].

    Input:  x  of shape [B, 3]  (already normalized, see Section 3)
    Output: alpha of shape [B, 1]
    """
    def __init__(self, hidden_dim: int = 32):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(3, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, 1),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:   # x: [B, 3]
        return torch.sigmoid(self.net(x))                 # [B, 1] in (0, 1)
```

**Fixes vs the guide's version** (`docs/plans/implementation_guide.md` §5):
- takes a **batched tensor** `[B, 3]`, not three python floats
- **no `torch.tensor(...)` inside `forward`** — that breaks batching and gradient flow
- inputs are **normalized before** they reach the module (Section 3)
- 2 linear layers, `sigmoid` on the output → `α ∈ (0, 1)`

Parameter count is tiny (~150), consistent with "lightweight" in the synopsis.

---

## 3. Input normalization (critical)

The three inputs are on wildly different scales — `τ_collision` in seconds (0–3),
`d_target` in distance units (0–140), `n_conflict` a small integer (0–`N−1`). Feeding
raw values into a small MLP gives terrible conditioning and the net effectively ignores
the small-scale inputs.

Normalize each to roughly `[0, 1]` or zero-mean/unit-scale:

| Input | Normalization |
|-------|---------------|
| `τ_collision` | `clip(τ, 0, H) / H` (so 1 = "no imminent collision", 0 = "colliding now") |
| `d_target` | `clip(d, 0, d_max) / d_max` with `d_max ≈ world diagonal` |
| `n_conflict` | `n / (N − 1)` |

Consider a running normalizer (like an observation normalizer) instead of fixed
constants — decide in P4 based on how the raw distributions look.

---

## 4. The design risk: agent-controlled reward weighting → reward hacking

`α` scales the **reward that the agent is optimizing**, and `α` is produced by the
agent's own network. The agent can raise its return without behaving better, just by
choosing `α` to up-weight whichever component is momentarily larger.

**Concrete degenerate case.** No drone is nearby, so `r_safety ≈ 0`. The mission term
this step is `r_mission = −0.5` (step penalty dominates before progress kicks in). The
combined reward is `α·(−0.5) + (1−α)·0`. The agent minimizes the penalty by pushing
`α → 0` — regardless of whether that is the right *behavioral* trade-off. Symmetrically,
when `r_safety` is a large negative near a conflict, the agent can push `α → 1` to
"hide" the safety penalty from its own return.

The centralized critic sees long-term value and *partly* counteracts this, but the
per-step reward manipulation still adds a shortcut and extra gradient variance. In the
worst case `α` collapses to a constant or to a degenerate "whatever makes this step
look best" function — and then PAH is no better than fixed-α, which kills the thesis
claim.

**This is the single most important thing to resolve with the supervisor before P4.**

---

## 5. Candidate formulations

### A. α weights the scalar reward, trained by policy gradient (synopsis, literal)

`r_t = α_t·r_mission,t + (1−α_t)·r_safety,t`, and `α_t` comes from PAH which sits on the
actor and is updated by the same PPO loss.

- **Pro:** exactly what the synopsis describes; simplest; "no extra critic, no extra
  loop" holds.
- **Con:** the reward-hacking path in Section 4.
- **Mitigations:**
  - a **prior/regularizer** on α: `+ λ·(α − 0.5)²` or a KL to a Beta(2,2) prior — pulls
    α toward neutral unless the state gives a real reason to move it
  - **entropy / smoothness** penalty on α across time (discourage bang-bang α)
  - **stop-gradient** on the α used inside the critic's target return (critic evaluates
    a fixed weighting), so only the actor path shapes α
  - clip α to `[0.1, 0.9]` so neither objective is ever fully ignored

### B. α weights the two advantages, with a two-head critic (recommended primary)

Keep **two value heads** `V_mission`, `V_safety` and two advantage estimates
`A_mission`, `A_safety` (GAE on each reward component separately). The actor gradient is

```
g = E[ ∇_θ log π(a|o) · ( α·A_mission + (1−α)·A_safety ) ]  −  entropy term
```

α still comes from PAH and is trained through this same gradient (plus the Section-5A
prior). The agent **cannot inflate its return by moving α**, because α now reweights
*which direction the policy improves in*, not the scalar it accumulates.

- **Pro:** principled (this is how multi-objective / multi-critic RL usually does it);
  removes the reward-hacking shortcut; gives clean per-objective learning curves and a
  nice diagnostic (`V_mission` vs `V_safety`).
- **Con:** the critic gets a **second output head** — a small, honest deviation from
  "adds no parameters to the centralized critic". One-line synopsis amendment; ask the
  supervisor (`04`, Q5). Slightly more code.

### C. α trained against an auxiliary target (supervised), not by policy gradient

α weights the scalar reward (as in A), but PAH is trained by a small regression loss
toward a hand-designed target `α*`, e.g. `α* = σ(β·(τ_collision − τ_0))` (low when a
collision is close). Policy gradient does **not** flow into PAH.

- **Pro:** no reward hacking (PAH can't be gamed if PG doesn't train it); interpretable.
- **Con:** α is only as good as the hand-designed `α*` — weakens the "*learned*"
  novelty claim. Better as an **ablation / sanity baseline** than the main method.

### D. α as an extra actor output dimension

PAH is just two more output units on the actor; the realized α enters the reward as in
A; standard entropy regularization on the whole action (incl. α) applies.

- **Pro:** minimal architectural change.
- **Con:** same reward-hacking path as A; less clean to analyze.

---

## 6. Recommendation

1. **Build A first** (matches the synopsis) with the α prior + clipping from 5A.
   Instrument heavily: log the α histogram, `α` vs `τ_collision`, and whether α
   collapses to a constant.
2. **Run the reward-hacking check** on Stage 1: does α actually degenerate? Does the
   full model beat fixed-α? If A works and α is well-behaved, we keep it — simplest and
   closest to the synopsis.
3. **If A shows reward hacking** (α collapses, or full model ≤ fixed-α despite α being
   non-constant), **switch to B** as the primary method and report A as a failed
   variant. B is the more defensible design anyway.
4. Keep **C** as an ablation ("learned α vs heuristic α*") — it is a good comparison
   point for the thesis regardless.

Honest note: we will not know which is needed until we run it. The plan is built so
that switching A → B is a contained change (add a value head, split the advantage),
not a rewrite.

---

## 7. Evaluating PAH itself (thesis figures)

Beyond mission success rate, the thesis needs to show α is doing something sensible:

- **α vs time-to-collision** scatter/curve — expect α to drop as `τ_collision` drops.
- **α vs n_conflict** — expect α to drop as the neighborhood gets crowded.
- **α over a single episode** timeline, overlaid on the drone's distance-to-target and
  nearest-neighbor distance — shows α switching priority at the right moments.
- **α distribution** across a test set — if it is a narrow spike, PAH ≈ fixed-α and we
  say so plainly.
- **"frozen-α" ablation** (§ `02_experiment_protocol.md`): retrain/evaluate with α
  fixed at its mean learned value. If that matches the full model, the *adaptivity*
  isn't what helps — an important, honest finding.

---

## 8. Open questions for the supervisor

Consolidated in `04_open_questions_for_supervisor.md` (Q4–Q6). In short:
- Is α on the scalar reward (A) or on the advantage combination (B) acceptable?
- Can we add a second critic head if A shows reward hacking?
- Is an α prior/regularizer acceptable, or does it undermine "purely learned"?

---

## 9. Decision (2026-09-14) — Option B implemented

After review by Manish (see `sessions/2026-09-14.md`, Part 2), **Option B ("α weights
advantages") was selected as the primary implementation.** Reason: a previous
implementation accidentally shipped Option C (supervised regression to a hand-crafted
`α_target = f(τ, n)`), which breaks the "learned α" thesis claim — PAH was just copying a
formula, not learning from experience.

**What is now in the code (`code/algorithms/mappo.py`, `update()`):**

1. `RolloutBuffer.compute_gae_components()` computes separate GAE trajectories for
   `r_mission` and `r_safety`, using the shared critic value `V` as the baseline for
   both. This is "Option B lite" — one critic, two advantage streams.

2. The actor loss is:
   ```
   w_adv  = α · A_mission + (1-α) · A_safety      # α from PAH
   a_loss = -E[ min(ratio·w_adv, clip(ratio)·w_adv) ]
   ```
   PAH gradient flows through `α` naturally. No hand-crafted `α_target`. No regression
   loss. `d_target` (PAH's third input) now has a real signal path — it influences
   `A_mission` which flows back through `α`.

3. The only PAH-specific loss is `compute_prior_loss(α)` — a mild pull toward 0.5 to
   prevent constant-α collapse.

**Why not two critic heads:** adding a second head (`V_safety`) is the full Option B
from Section 5B. We use a shared baseline for both advantage streams. This is a known
simplification; if `V` cannot simultaneously fit both components well, the advantages
will be noisier. This is acceptable for the thesis scope; if training is unstable, the
two-head extension is the natural next step.

**Option C becomes ablation:** train a PAH variant with supervised regression to
`α* = α_min + (α_max−α_min)·τ_norm·(1−0.3·n_norm)`, compare it to Option B in
evaluation. This is a valid thesis figure ("learned PAH vs heuristic PAH").

---

## 9.2 Fix (2026-09-16) — flat 0.5 prior let α drift the wrong way near danger

**Empirical finding.** The `stage2-pah/var-alpha` 8000-episode Kaggle run (Section 12/13
of `sessions/2026-09-16.md`) showed α was *not* collapsing to a constant (0.640–0.871
across training — the Section 9 prior was doing its one job), but its *direction* was
often wrong. Checking `eval_alpha_low_tau` (danger-close) against `eval_alpha_high_tau`
(safe) at the 17 eval points with enough danger-close samples to compare: **10 of 17 had
α higher near danger than when safe** — the opposite of the intended "α → 0 near danger"
behavior — and from ~episode 4800 onward α repeatedly saturated at `alpha_max` (0.9)
exactly in the danger-close bucket, a pattern that strengthened over training rather than
fading.

**Root cause.** `compute_prior_loss` (Section 9, item 3) only pulled α toward a flat 0.5.
That made it directionally neutral — it discourages collapse but says nothing about which
way α should move near danger. The *only* signal that did say something about direction
was the advantage-mixing actor loss (Section 9, item 2): that loss is minimized by moving
α toward whichever of `A_mission`/`A_safety` is currently larger at a given state. Near a
collision, `A_safety` is routinely more negative than `A_mission` — the collision penalty
is the sharpest negative term in the reward, and the agent is often still making mission
progress right up to the moment of impact. So the loss's gradient pushed α *up* (toward
`A_mission`, away from weighting the large negative `A_safety`) exactly in the states
where it should have pushed down. This is a subtler cousin of the Section 4 reward-hacking
risk: Option B closes the path where α inflates the *reward the agent accumulates*, but it
does not by itself stop α from drifting toward whichever advantage term is locally more
favorable to the *surrogate loss being maximized* — which is a related but distinct
failure mode, and the flat prior did nothing to counter it.

**Fix.** `compute_prior_loss` now takes `tau_norm` and pulls α toward
`alpha_target = alpha_min + (alpha_max - alpha_min) · tau_norm` — low near danger
(`tau_norm → 0`), high when safe (`tau_norm → 1`) — instead of a flat 0.5. `prior_coef`
raised `0.01 → 0.05` (the old value was tuned against an uninformative target and is not
assumed strong enough here; re-check against the next run, it is a reasoned starting
point, not a swept value).

**Why this is still Option B, not a reversion to Option C.** Option C (Section 5C, and
the ablation above) trains α *only* by regression to a hand-crafted `α*`, with no policy
gradient into PAH at all — α just copies a formula. Here, the advantage-mixing actor loss
(Section 9, item 2) still flows gradient into PAH every step, using all three inputs
(`τ`, `d_target`, `n_conflict`); the τ-informed term is a *regularizer added to that same
loss*, not a replacement training signal, and it only sees `τ`, not `d_target` or
`n_conflict` — those two still shape α purely through the learned pathway, unconstrained
by this prior. This is exactly the mitigation Section 5A already anticipated ("a
prior/regularizer on α... pulls α toward neutral unless the state gives a real reason to
move it") — the only change is that the prior's target is now informed by τ instead of
being a constant, which is necessary because a constant target cannot express "there is a
real reason to move it based on danger."

**Status: tested, FAILED.** A full 8000-episode Kaggle run with this fix (see
`sessions/2026-09-17.md`) showed **no improvement** — 11 of 19 danger-close eval
samples still had α higher than the matched safe-sample α (58%, statistically the same
rate as the 10/17 = 59% before this fix), still repeatedly saturating at `alpha_max`.
See Section 9.3 for the root cause and the fix that actually worked.

---

## 9.3 Fix (2026-09-17) — weight the prior toward danger-close samples

**Why 9.2 didn't work.** Comparing logged loss magnitudes from the 9.2 run:
`actor_loss` ranged -0.10 to 0.02, `pah_loss` (the 9.2 prior, coef 0.05) ranged only
0.001 to 0.007 — 10-20x smaller. Danger-close states are also a small fraction of any
training batch (only 19/76 eval checkpoints had *any* valid danger-close sample at
all). The 9.2 prior averaged `(α − α_target)²` uniformly over the whole batch, so the
rare danger-close samples' error got diluted by the much larger volume of safe
samples — the correction barely reached the exact samples it was meant to fix.

**Fix.** `compute_prior_loss` now weights each sample's squared error by how
dangerous it is, instead of averaging all samples equally:

```
alpha_target = alpha_min + (alpha_max − alpha_min) · tau_norm
weight        = 0.1 + 0.9 · (1 − tau_norm)     # 1.0 at danger, 0.1 when safe
loss          = prior_coef · mean(weight · (α − α_target)²)
```

`prior_coef` raised `0.05 → 0.15`. Same Option-B-not-C reasoning as 9.2 applies
unchanged — this is still a regularizer added to the same gradient-trained loss, not
a replacement for it.

**Status: tested on seed=42, initially looked like SUCCESS — 5-seed follow-up shows
PARTIAL / seed-dependent.** First run (8000-episode Kaggle, same warm-start, seed=42,
`sessions/2026-09-17.md`):

| | 9.2 (unweighted, coef 0.05) | 9.3 (weighted, coef 0.15), seed=42 |
|---|---|---|
| Danger-close samples with wrong direction | 11/19 (58%) | **0/14 (0%)** |
| Avg success | 89.7% | **91.2%** |
| Avg collision | 10.3% | **8.8%** |

All 14 valid danger-close eval points on seed=42 showed α correctly *lower* than the
matched safe-sample α. This looked like a clean fix — but it was a single seed, and
the master plan's own rule (≥5 seeds before any result counts) turned out to matter
here specifically:

**5-seed follow-up (seeds 42–46, `sessions/2026-09-17.md` Sections 10–14):**

| Seed | Direction wrong | Avg success | Avg collision |
|---|---|---|---|
| 42 | 0/14 (0%) | 91.2% | 8.8% |
| 43 | 0/14 (0%) | 91.2% | 8.8% |
| 44 | 0/16 (0%) | 90.2% | 9.8% |
| 45 | 11/17 (65%) | 92.6% | 7.4% |
| 46 | 16/18 (89%) | 90.1% | 9.9% |
| **Combined** | **27/79 (34%)** | 91.1% avg | 8.9% avg |

**Success/collision are consistently good across all 5 seeds (90–93% range) — that
part of the fix is solid.** But the direction check — the actual mechanism the fix
was meant to repair — fails badly in 2 of 5 seeds, and in both failing seeds the
wrong cases repeatedly saturate at exactly `alpha_max` (0.9), the same clip-ceiling
pattern from the original bug. `prior_coef=0.15` is evidently not uniformly strong
enough to win the tug-of-war against the advantage-mixing actor loss (Section 9.2's
root-cause explanation) — it wins most of the time, not reliably.

**This is not "PAH jeeta," and it is not a clean "PAH haara" either — it's an
open reliability problem in the current fix.** Next escalation path (already
anticipated in Section 9.2's closing note): a full two-head critic, so `A_safety`
gets its own value baseline instead of sharing one with `A_mission` — the shared
baseline may be why `A_safety`'s signal is unreliable enough, in some seeds, for the
actor loss to win that tug-of-war. This has not been implemented yet; it requires
re-running the full seed grid once done, and is a synopsis deviation worth flagging
to the supervisor before starting (`04_open_questions_for_supervisor.md` Q5).
