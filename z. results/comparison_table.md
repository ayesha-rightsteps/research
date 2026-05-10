# Cross-Paper Comparison: 4 UAV Path Planning Papers

---

## The Big Picture

All 4 papers solve **UAV path planning using Deep Reinforcement Learning**, but each targets a different piece of the same problem: one drone in a small space → one drone in a huge space → multiple drones with target assignment → a massive swarm of 80+ drones. Together, they form a progression from simple to large-scale.

---

## Side-by-Side Comparison Table

| | **Paper 1** | **Paper 2** | **Paper 3** | **Paper 4** |
|---|---|---|---|---|
| **Short Name** | Improved D3QN | TANet-TD3 | Dynamic Reward DQN | PO-WMFDDPG |
| **Full Title** | Dynamic Scene Path Planning of UAVs Based on Deep Reinforcement Learning | Multi-UAV Simultaneous Target Assignment and Path Planning | Dynamic Reward-Based DRL for UAV Path Planning in Large-Scale Environments | Large-scale UAV Swarm Path Planning Based on Mean-Field Reinforcement Learning |
| **Year** | 2024 | 2022 | 2025 | 2025 |
| **Venue** | *Drones* (MDPI) | *Frontiers in Neurorobotics* | Procedia Computer Science (KES 2025) | Chinese Journal of Aeronautics |
| **Algorithm** | Improved D3QN (Dueling Double DQN + PER + Heuristic Exploration) | TANet-TD3 (Target Assignment Network + TD3) | DQN with dynamic reward d3/(d1+d2) + 3D CNN | PO-WMFDDPG (Partial Obs. Weighted Mean Field DDPG) |
| **Action Space** | Discrete (8 directions) | Continuous (speed + heading) | Discrete (26 directions) | Continuous (linear acc + angular acc) |
| **# of UAVs** | 1 | 5 | 1 | 80 (tested up to 120) |
| **Environment** | 2D grid, dynamic moving obstacles | 2D, dynamic obstacles + moving targets | 3D grid, 6–40 static obstacles | 2D, 500×500m battlefield, 20 NFZs |
| **Environment Size** | Small grid | Medium | Large-scale (7–25 km) | 500×500m tactical |
| **Obstacles** | Moving (dynamic) threat zones | Moving obstacles + static targets | Static (6 to 40) | Static + moving NFZ test |
| **Observability** | Full (MDP) | Partial (POMDP, limited detection range) | Full (MDP) | Partial (POMDP, comm. range R_a) |
| **Key Innovation 1** | Heuristic action selection narrows exploration toward target | TD3 with TANet for simultaneous target assignment | Dynamic reward d3/(d1+d2) — dense feedback every step | Mean field approximation → N² interactions → N×1 |
| **Key Innovation 2** | Prioritized Experience Replay (PER) — learn from important mistakes more | Hungarian algorithm generates optimal assignment labels | 3D CNN processes spatial grid — no Q-table needed | Partial observability — only nearby neighbors in mean field |
| **Key Innovation 3** | Dueling network architecture (V + A streams) | State reordering by Q-value to keep assignment consistent | Input normalization for training stability | Multi-head attention weights closer drones higher |
| **Reward Design** | 5-component: target arrival, boundary, threat zone, time penalty, step penalty | Potential-based reward: arrival + boundary + threat avoidance + collision | Dynamic: R=d3/(d1+d2) each step; ±1 for goal/obstacle | r_task = λ(1−d_{t+1}/d_t) + η·cos(β_t) + long-term penalties |
| **Baselines** | DQN, DDQN, A*, RRT-GoalBias | DDPG, MADDPG, TD3 without TANet | Q-learning, GWO, PSO, SSA | DDPG, MFDDPG |
| **Primary Metric** | Path length, steps, planning time, success rate | Success rate, path efficiency | Success rate (SR), SLR, path length, compute time | Task success rate |
| **Best Result** | ~95% SR in dynamic scene; shorter paths than A* | Highest SR + simultaneous assignment, outperforms all baselines | 98% SR (Sc.1) → 85% SR (Sc.4 with 40 obstacles) | ~98% SR at 80 UAVs; >90% at 120 UAVs |
| **Compute Time** | Not the bottleneck (2D small grid) | Not specifically reported | 133–456 sec (slowest but most accurate) | Converges in ~700/1000 training rounds |
| **Hardware Validated** | No — simulation only | No — simulation only | No — simulation only | No — simulation only |
| **Obstacle Type** | Dynamic (moving) | Dynamic (moving) | Static only | Static (+ 1 dynamic test) |
| **Multi-Agent?** | No | Yes (5 UAVs) | No | Yes (80–120 UAVs) |
| **Target Assignment?** | No (target is fixed/given) | Yes — simultaneously assigns targets to UAVs | No (target is fixed/given) | No (pre-assigned targets) |
| **Publication Impact** | MDPI open-access journal | Frontiers (peer-reviewed) | Conference (KES 2025) | Chinese Journal of Aeronautics |

---

## What Problem is Common Across ALL 4 Papers?

These are the problems every single paper is fighting:

### 1. Collision Avoidance
Every paper deals with a UAV that must not enter restricted/dangerous areas. Whether it's a moving threat zone (Paper 1), a dynamic obstacle (Paper 2), a static obstacle cluster (Paper 3), or a no-fly zone in a swarm (Paper 4) — the core challenge is always: **how does the UAV learn to avoid things that will get it killed?**

### 2. Sparse Reward Problem
All papers struggle with the fact that a drone flying through an empty environment gets no feedback until it reaches the goal or crashes — which makes learning extremely slow. Each paper solves this differently:
- Paper 1: Multi-component reward with step penalty and boundary penalty
- Paper 2: Potential-based reward with continuous progress signal
- Paper 3: Dynamic formula d3/(d1+d2) giving a score at every single step
- Paper 4: Instant reward r_task combining distance progress + heading alignment

### 3. Scalability of Classical Methods Fails
All 4 papers reject classical algorithms (A*, RRT, Q-learning, PSO, GWO) as insufficient:
- A*/RRT: Can't handle dynamic environments
- Q-learning: State space explosion in large or complex environments
- PSO/GWO: Local optima, fail at high obstacle density
- Standard MARL: Collapses beyond ~10 agents

### 4. Simulation Only — No Real Hardware
All 4 papers are simulation-only. None validates on physical drones. This is the single weakest point shared across the entire set of papers.

### 5. Training Stability
Every paper had to address training instability in deep RL — the tendency for networks to diverge or oscillate. Each solves it differently:
- Paper 1: DDQN to prevent Q-value overestimation
- Paper 2: TD3's clipped double-Q, delayed policy update, target smoothing
- Paper 3: Dual Q-networks (evaluation + target), input normalization
- Paper 4: Soft update of target networks, mean-field stabilization

---

## How Each Paper Extends the Previous

```
Paper 1: Improved D3QN
→ 1 drone, 2D, dynamic scene
→ Contribution: Better DRL training (PER + heuristic exploration + dueling)

        ↓ adds: multi-drone + target assignment

Paper 2: TANet-TD3
→ 5 drones, 2D, dynamic scene
→ Contribution: Simultaneous target assignment while navigating
                (TD3 + Hungarian Algorithm)

        ↓ adds: large 3D environment + scale of problem

Paper 3: Dynamic Reward DQN
→ 1 drone, 3D, large-scale (25km), static obstacles
→ Contribution: Novel reward design for large environments
                (3D CNN + dynamic reward formula)

        ↓ adds: large swarm + massive scale + coordination

Paper 4: PO-WMFDDPG
→ 80 drones, 2D, swarm coordination
→ Contribution: Mean-field approximation for scalable MARL
                (partial obs + attention weighting)
```

---

## The Gap Nobody Has Solved Yet

Reading all 4 papers together, the obvious next step — which **none of them addresses** — is:

> **"80+ drones, 3D environment, dynamic moving obstacles, with partial observability and real-time replanning."**

- Paper 3 handles 3D but only 1 drone and static obstacles
- Paper 4 handles 80 drones but only 2D and mostly static obstacles
- Paper 2 handles dynamic obstacles but only 5 drones
- Paper 1 handles dynamic obstacles but only 1 drone

No paper combines large-scale + 3D + dynamic + multi-agent. That is the open research problem.

---

## Quick Reference: Which Paper to Cite for What

| If the question is about... | Cite |
|---|---|
| Dynamic/moving obstacles | Paper 1 (or Paper 2) |
| Reward function design | Paper 3 (d3/(d1+d2) is the clearest example) |
| Large-scale 3D environments | Paper 3 |
| Multi-UAV coordination | Paper 2 (small scale) or Paper 4 (large scale) |
| Target assignment | Paper 2 |
| Swarm scalability | Paper 4 |
| Mean field theory in UAV RL | Paper 4 |
| Training stability techniques | Any — each has a different technique |
| Why classical algorithms fail | Paper 3 is the most explicit about PSO/GWO collapse |
| Partial observability | Paper 2 or Paper 4 |
