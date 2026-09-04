# Research Direction — Final Submission
**To:** Supervisor
**From:** Ayesha Khalil (SP25-RCS-009/ATD)
**Program:** MS Computer Science — COMSATS University Islamabad, Abbottabad Campus
**Date:** June 2026
**Re:** Revised research direction and problem statement — addressing committee feedback and incorporating recent literature

---

## Executive Summary

The synopsis committee raised a valid concern: the original problem statement described integrating two existing methods (DA-MAPPO and IGAT-MARL), which constitutes an integration study rather than an original research contribution. This submission presents the revised direction, which proposes a genuinely novel mechanism — the Priority Arbitration Head — that does not exist in any of the thirteen reviewed papers including the four most recent publications from 2025 and 2026. The revised direction retains the foundational motivation of the original proposal while contributing a new, testable, and bounded mechanism.

---

## Background: Why The Committee Was Correct

The original problem statement proposed combining DA-MAPPO (target assignment) and IGAT-MARL (collision avoidance) and evaluating the combined system. This framing reduces to the following research activity:

1. Implement DA-MAPPO
2. Implement IGAT-MARL
3. Run them together
4. Observe performance

There is no new mechanism, no falsifiable hypothesis about a new contribution, and no answer to the question: "what did we learn that we could not have predicted beforehand?" The committee's characterization of this as a comparative study was accurate.

---

## The Fundamental Question The Committee's Feedback Revealed

When target assignment and collision avoidance are combined in a single policy, they generate conflicting navigation commands whenever a drone's assigned target lies in a direction that requires passing near another drone. Resolving this conflict requires assigning relative importance to each objective at each decision step.

**This is a design decision present in every paper that attempts to combine both objectives — and every existing paper resolves it the same way: by setting fixed, constant reward coefficients before training.**

The question no existing paper asks is: *Should this balance be fixed, or should it be learned as a function of the agent's current operational state?*

This is a legitimate research question with a binary, falsifiable answer — and it has not been addressed in any reviewed paper.

---

## Literature Evidence for the Gap

A systematic review of thirteen papers spanning 2023 to 2026 was conducted. The table below summarizes the key findings:

| Paper | Year | Approach | Assignment | Avoidance | Dynamic Objective Weighting |
|---|---|---|---|---|---|
| DA-MAPPO (Sheng et al.) | 2026 | MAPPO + min-cost allocation | ✅ | Penalty only | ❌ Fixed |
| IGAT-MARL (Rezaee et al.) | 2026 | MARL + Graph Attention | ❌ | ✅ | ❌ Fixed |
| HPER-D3QN (Shen et al.) | 2026 | D3QN + DTPA + HPER | ❌ | ✅ | ❌ Fixed |
| STAAC (Yan et al.) | 2025 | MADDPG + LSA + GTA | ❌ | ✅ | ❌ Fixed |
| Kong et al. | 2024 | TD3 + assignment net | ✅ | Basic | ❌ Fixed |
| Zhang et al. | 2025 | Mean Field DDPG | ❌ | Partial | ❌ Fixed |
| Tang et al. | 2024 | D3QN + PER | ❌ | Obstacle only | ❌ Fixed |
| Govinda et al. (Survey) | 2025 | Survey (IEEE TITS) | N/A | N/A | Identified as open problem |

In addition, two papers that appeared after the initial submission:
- Shen et al. (2026) — HPER-D3QN: introduces dynamic threat *scoring* within the avoidance objective using time-to-closest-approach (TCPA) and distance-at-closest-approach (DCPA), but the balance between navigation and avoidance remains fixed (C_goal = +2, C_collision = −1).
- Yan et al. (2025) — STAAC: introduces spatial-temporal attention for entity-aware fleet coordination, validated on hardware at 1.5ms inference, but the balance between flocking adherence and collision avoidance remains governed by fixed constants (P1, P2, w1, w2).

**Across all thirteen papers, no mechanism proposes a learned, state-conditioned function to determine the relative weight between competing objectives at runtime.**

---

## Why Researchers Have Not Combined Both Objectives

This is a natural question a committee would raise. The answer is revealing:

Researchers have deliberately bounded their contributions because:

1. **Assignment and avoidance are mathematically distinct problem types** — combinatorial optimization (who goes where) versus continuous reactive control (how to navigate safely). Solving both rigorously in one paper is high-risk for a bounded research scope.

2. **Combining them creates an immediate unresolved design question** — what coefficient should each objective receive? Every paper that attempted this (Kong et al., DA-MAPPO) resolved it by fixing the weight manually and leaving it unexamined. The question of whether this weight can and should be learned was never asked — because the question itself is the research contribution.

3. **The research community has reached a natural stopping point** — The most recent papers (2025–2026) have now produced sophisticated mechanisms for each objective independently. The next logical step — and the one not yet taken — is to propose a principled mechanism for balancing them dynamically.

---

## The Proposed Contribution: Priority Arbitration Head

**Mechanism:**
A small neural network (2–3 fully connected layers, approximately 32–64 units per layer) jointly trained with the MAPPO actor network. At each timestep t, given:
- τ_collision: estimated time-to-collision (derived from relative positions and velocities)
- d_target: distance to assigned target
- n_conflict: number of agents on conflict-course trajectories

The arbitration head outputs α ∈ [0, 1], which is applied as:

```
r_total = α × r_assignment + (1 − α) × r_avoidance
```

The parameter α is not fixed. It is learned end-to-end during MAPPO training through backpropagation of the policy gradient. No separate training loop is required. No architectural change to the critic network is necessary.

**Why these inputs:**
HPER-D3QN's DTPA mechanism uses TCPA and DCPA as the primary variables for threat assessment — validating that time-to-collision is an established, meaningful signal in this domain. STAAC's entity grouping validates that conflict neighborhood structure is a relevant state descriptor for collision-related decisions. These inputs were independently selected and subsequently confirmed by the most recent literature.

**Why this is not Multi-Objective RL (MORL):**
MORL methods (scalarization, Pareto-based, lexicographic) determine the preference vector at deployment time — before the agent begins operating. The preference remains constant during execution. The Priority Arbitration Head operates within a single execution episode, adjusting the weight at each timestep based on the agent's current physical state. This is not a preference selection; it is a real-time reactive decision made continuously during flight. Furthermore, multi-critic MORL approaches introduce training instability in cooperative MARL settings, as multiple value functions must converge simultaneously for all agents.

---

## Research Question

**Can a learned, state-conditioned priority arbitration module, jointly trained with a MAPPO backbone in a 2D multi-UAV environment requiring simultaneous dynamic target assignment and inter-agent collision avoidance, outperform fixed-weight reward baselines across mission success rate, collision frequency, and task completion time?**

This is falsifiable. A binary outcome is expected: learned arbitration either outperforms fixed-weight baselines or it does not. Both outcomes are publishable — the first confirms the hypothesis; the second contributes a negative result showing where fixed tuning is competitive and why.

---

## Evaluation Design

**Environment:** 2D simulation, 5–8 drones, dynamic targets, static obstacles. Directly comparable to both DA-MAPPO and IGAT-MARL baselines which also operate in 2D.

**Baselines and ablations:**
1. Standard MAPPO (no structured assignment or avoidance)
2. DA-MAPPO (assignment with fixed reward weights)
3. IGAT-MARL (avoidance with fixed reward weights)
4. Combined fixed α = 0.3
5. Combined fixed α = 0.5
6. Combined fixed α = 0.7
7. **Proposed: Learned α — Priority Arbitration Head**

**Metrics:** Mission success rate, inter-agent collision frequency, task completion time, α trajectory analysis (what does the learned mechanism actually do in critical situations).

**Timeline:** 12 months. Months 1–2: environment and baselines. Months 3–4: arbitration head implementation. Months 5–7: training and evaluation. Months 8–9: ablation study. Months 10–12: analysis and writing.

---

## Why This Qualifies as Original Research

1. The mechanism proposed — learned, state-conditioned objective weighting — does not exist in any of the thirteen reviewed papers, including the most recent publications.

2. The research question is falsifiable and binary — the answer advances the field's understanding regardless of direction.

3. The contribution is a new component, not a new dataset, environment, or combination of existing methods.

4. The ablation study is structurally clean: the single variable is whether α is learned or fixed. All other conditions remain constant.

5. The contribution is bounded and feasible within a 12-month MS timeline — a small MLP integrated into an existing MAPPO backbone.

---

*The revised problem statement is attached. I am available at the earliest convenience to discuss any aspects of this direction.*

