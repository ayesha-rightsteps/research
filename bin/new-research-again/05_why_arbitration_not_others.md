# Why Priority Arbitration — Not Something Else
### Alternative mechanisms vs chosen approach

---

## The Question

Why Priority Arbitration specifically? What other mechanisms could solve the same problem — and why were they not chosen?

---

## Alternative 1: Hierarchical Policy

**What it would do:**
A high-level policy decides "assignment mode or avoidance mode" at each step. A low-level policy executes within that mode.

**Why it does not fit this problem:**
Assignment and avoidance happen simultaneously — a drone is moving toward its target and avoiding a collision at the same second. The concept of "switching modes" is fundamentally wrong here. There is no clean moment where only one objective is active. Additionally, hierarchical policies require separate training loops for each level, which increases implementation complexity and failure risk significantly for a 12-month MS timeline.

**Verdict:** Wrong assumption about the problem structure.

---

## Alternative 2: Constrained RL (CMDP)

**What it would do:**
Treat collision avoidance as a hard constraint. Maximize assignment reward subject to: collision probability < threshold. Uses Lagrangian methods to enforce the constraint during training.

**Why it does not fit this problem:**
This is theoretically the most rigorous alternative. The problem is practical: Lagrangian methods in multi-agent settings have well-documented convergence issues. The constraint becomes a moving target during training — the Lagrange multiplier oscillates, policy updates destabilize, and agents do not converge reliably. Published papers on constrained MARL acknowledge this. For a 12-month MS, if convergence fails at month 8, there is no time to recover.

**Verdict:** Theoretically valid. Practically risky for MS scope.

---

## Alternative 3: Multi-Objective RL (Pareto Front)

**What it would do:**
Train multiple policies, each representing a different trade-off between assignment and avoidance on the Pareto frontier. At deployment, select the policy that matches the current scenario preference.

**Why it does not fit this problem:**
This approach selects a policy before the flight begins — it cannot adapt mid-flight. If a drone has a collision incoming two seconds from now, the system cannot switch to a more avoidance-heavy policy in that moment. Our problem is specifically about adapting priority within a single flight, at each decision step. Pareto methods solve a different problem: choosing a policy across scenarios, not within one.

**Verdict:** Solves the wrong version of the problem.

---

## Alternative 4: Reward Decomposition / Separate Value Functions

**What it would do:**
Maintain a separate Q-function for each objective (assignment Q, avoidance Q). At inference, combine them with a weighting vector.

**Why it does not fit this problem:**
Conceptually this is a cousin of Priority Arbitration — but it operates at the value function level rather than the reward level. In multi-agent settings, maintaining two independent value functions per agent introduces training instability because each value function affects the other agents' learning. The ablation study also becomes harder to design cleanly: you cannot simply swap "learned vs fixed" — you have to retrain separate networks. Interpretability is lower.

**Verdict:** More complex than needed for the same goal. Ablation is not clean.

---

## Why Priority Arbitration

| Requirement | Arbitration | Hierarchical | CMDP | Pareto | Decomposed V |
|---|---|---|---|---|---|
| Adapts within a single flight | ✅ | ❌ | ✅ | ❌ | ✅ |
| No convergence risk in MARL | ✅ | ✅ | ❌ | ✅ | ⚠️ |
| Adds to MAPPO without changing architecture | ✅ | ❌ | ❌ | ❌ | ❌ |
| Clean ablation (learned vs fixed) | ✅ | ❌ | ❌ | ❌ | ❌ |
| Feasible in 12-month MS | ✅ | ⚠️ | ❌ | ✅ | ⚠️ |
| Directly targets the reward-conflict problem | ✅ | ❌ | ✅ | ⚠️ | ✅ |

Priority Arbitration is the only option that satisfies all six requirements simultaneously.

---

## If the Committee Asks

> *"Why not constrained RL — that seems more principled?"*

> "Sir, constrained RL is theoretically rigorous, and I did consider it. The issue is that Lagrangian methods in multi-agent settings have known convergence instability — this is documented in constrained MARL literature. For a 12-month timeline, a failed convergence at month 8 has no recovery path. Priority Arbitration addresses the same tension with a simpler formulation that has a guaranteed testable outcome."

> *"Why not a hierarchical policy?"*

> "Sir, hierarchical policies assume the two objectives can be separated into distinct modes. In our setting, a drone is simultaneously navigating toward a target and resolving a collision — there is no clean mode boundary. The arbitration mechanism is continuous and operates within a single policy, which matches the actual structure of the problem."

---

## Honest Summary

Constrained RL is also a legitimate choice given more time and a stable MARL convergence baseline.
Priority Arbitration was chosen because it addresses the same conflict, operates at the right level (reward, not architecture), is directly ablatable, and is implementable within MS scope.

