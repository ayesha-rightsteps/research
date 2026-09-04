# Research Revision Memo
**To:** Supervisor
**From:** Ayesha Khalil (SP25-RCS-009/ATD)
**Program:** MS Computer Science — COMSATS University Islamabad, Abbottabad Campus
**Date:** June 2026
**Re:** Revised Research Focus Following Synopsis Committee Feedback

---

## Background

The synopsis committee reviewed my proposed research and raised a concern: the original problem statement described combining two existing methods — DA-MAPPO (target assignment) and IGAT-MARL (collision avoidance) — in a single framework. The committee's position was that this constitutes integration/comparative study rather than original research contribution.

This memo presents the revised research direction that addresses that concern.

---

## Previous Problem Statement

> Existing approaches to multi-UAV coordination treat dynamic target assignment and collision avoidance as separate problems, each developed and validated independently in two-dimensional environments. When both mechanisms operate simultaneously in three-dimensional space, they generate competing navigation signals — the assignment directs each drone toward its target without awareness of active collision conflicts, while the collision avoidance module forces course corrections without awareness of current assignments, a tension that becomes structurally significant when vertical flight paths are introduced. The result is a fundamental tension in three-dimensional multi-UAV deployment: goal-directed navigation and inter-agent collision avoidance pull each drone in opposing directions, and whether a unified policy can hold both objectives in balance — or whether one systematically undermines the other — has not been established.

**What this statement did:** It correctly identified the tension between two objectives. However, the proposed solution — integrating the two methods and evaluating performance — did not introduce a new mechanism. The committee was correct that this framing reduces to a comparative/integration study.

---

## What Is Being Added

The revised research introduces one new component that does not exist in any prior paper:

**Priority Arbitration Head** — a trainable neural module that determines, at each decision step, the relative weight between the assignment objective and the avoidance objective, based on current operational state (collision imminence, target proximity, conflict neighborhood density).

In all existing work — including DA-MAPPO and IGAT-MARL — the relative weight between competing reward components is a fixed constant set before training. This constant does not change based on whether the drone is in open space or approaching a collision. The proposed arbitration module makes this weighting dynamic and learned.

This is not a combination of two existing methods. It is a new component whose behavior emerges from training and whose design is not present in any of the 11 papers reviewed.

---

## Revised Problem Statement

Multi-UAV systems pursuing dynamic targets in shared airspace must simultaneously optimize goal-directed navigation and inter-agent collision avoidance — two objectives that produce conflicting navigation commands within a single policy when collision risk and target assignment coincide at the same decision step.

Existing frameworks that address these objectives independently use fixed reward coefficients that assign constant relative weight to each objective regardless of operational context. A drone navigating open space and a drone seconds from a collision receive the same trade-off weighting. This forces the policy to learn a globally averaged balance that is suboptimal when either objective is clearly dominant.

No existing framework provides a mechanism to determine, at each step, which objective should take priority based on real-time state. This research proposes a learned priority arbitration module that continuously adjusts the relative weight between assignment and avoidance as a function of time-to-collision, target distance, and conflict neighborhood — and evaluates whether learned weighting outperforms the fixed-weight baselines used in all prior work.

---

## Key Changes from Original Proposal

| Item | Previous | Revised |
|---|---|---|
| Core contribution | Combining two methods in one policy | New arbitration module — not present in any prior work |
| Research question | Does combined framework work? | Does learned priority weighting outperform fixed weighting? |
| Environment | 3D | 2D (consistent with both baseline papers; cleaner evaluation) |
| Novel mechanism | None proposed | Priority Arbitration Head (learned, state-dependent) |
| Evaluation baseline | DA-MAPPO, IGAT-MARL | Same + fixed α=0.3, 0.5, 0.7 as ablation — isolates the contribution |

---

## Why This Qualifies as Original Research

1. The mechanism being proposed (dynamic, learned reward weighting) does not exist in any of the 11 reviewed papers.
2. The research question has a binary testable outcome: learned priority weighting either outperforms fixed weighting or it does not.
3. The contribution is a new component, not a new dataset, setting, or combination.
4. The ablation study directly tests the hypothesis by comparing learned α against fixed α values.

---

## Scope

Environment: 2D simulation, 5–8 drones, dynamic targets, static obstacles.
Training: MAPPO backbone with added arbitration module.
Baselines: Standard MAPPO, DA-MAPPO, IGAT-MARL, fixed-weight combined (α = 0.3, 0.5, 0.7).
Ablation: Arbitration module removed — replaces learned α with each fixed value.
Timeline: 12 months (unchanged from original proposal).

---

*For further discussion, I am available at the earliest convenience.*

