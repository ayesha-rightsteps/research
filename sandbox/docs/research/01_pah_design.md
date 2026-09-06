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
