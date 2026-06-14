# Research Update — Additional Literature Review
**To:** Supervisor
**From:** Ayesha Khalil (SP25-RCS-009/ATD)
**Program:** MS Computer Science — COMSATS University Islamabad, Abbottabad Campus
**Date:** June 2026
**Re:** Two additional papers reviewed following submission of revised problem statement

---

## Purpose

This memo documents the review of two additional papers identified following the submission of the revised problem statement on Priority Arbitration for Multi-UAV Coordination. Both papers are directly related to the proposed research. Their contributions are summarized below, along with an analysis of how they reinforce the identified research gap.

---

## Paper A: Shen et al. (2026) — HPER-D3QN

**Full Citation:**
Yan Shen, Xuejun Zhang, Yan Li, Weidong Zhang. "Deep reinforcement learning-based adaptive collision avoidance method for UAV in joint operational airspace." *Defence Technology*, Vol. 56, 2026, pp. 142–159. https://doi.org/10.1016/j.dt.2025.08.011

**Institution:** Beihang University, Beijing (State Key Laboratory of CNS/ATM)

**Setting:** Single UAV operating in joint operational airspace containing manned aircraft (commercial), unmanned aircraft (drones), and dynamic wind disturbances. Partial observability — UAV cannot access global airspace information and relies solely on onboard sensors within a detection radius of 4000 meters divided into 8 sectors.

---

### Contributions

**1. DTPA — Dynamic Threat Prioritization Assessment**

Previous approaches used Euclidean distance alone to determine which aircraft is most threatening. DTPA replaces this with a multi-dimensional threat score:

```
S = ωt × normalize(TCPA) + ωd × normalize(DCPA) + ωtype × κ
```

Where TCPA (Time to Closest Point of Approach) and DCPA (Distance at Closest Point of Approach) are computed from relative position and velocity vectors. Aircraft type factor κ is set to 0.75 for manned aircraft and 0.25 for unmanned aircraft, reflecting greater operational risk from larger aircraft. Weights are ωt = 0.4, ωd = 0.4, ωtype = 0.2.

DTPA identifies the highest-scoring aircraft in each detection sector as the "intruder" for that sector. This provides a more accurate threat assessment in heterogeneous airspace.

**2. HPER — Hierarchical Prioritized Experience Replay**

Standard experience replay samples uniformly from a buffer, which under-samples safety-critical events because they are rare. HPER partitions the replay buffer into three priority layers:

| Layer | Contents | Sampling Priority |
|---|---|---|
| Ehigh | Successful arrival ∪ Collision ∪ Boundary violation | Highest |
| Emedium | Warning zone entry | Intermediate |
| Elow | Normal safe flight (no threats detected) | Lowest |

Within each layer, sampling is further weighted by TD-error (Temporal-Difference error) of individual experiences. This combination ensures that critical events — which are rare but information-dense — are sampled disproportionately during training. The backbone algorithm is D3QN (Double Dueling Deep Q-Network).

**Algorithm:** HPER-D3QN trained on PyTorch with TITAN RTX GPU in a PyGame-based simulation environment of 30km × 30km.

---

### Results

At 25-aircraft density (most congested scenario): **96.28% task success rate** — highest among all compared methods (DQN, DDQN, Dueling DQN, D3QN, PER-D3QN).

Ablation study (highest-density environment, uncertainty level 5):
- Removing DTPA: success rate drops 8.98%, Frequency of Hazardous Proximity increases 92.54%
- Removing HPER: success rate drops 9.27%, FHP increases 87.26%

Generalization to high-fidelity Unity3D battlefield simulation validated successfully.

---

### Relevance to Proposed Research

The DTPA mechanism introduces state-dependent, context-sensitive prioritization *within* the collision avoidance objective — ranking threats dynamically at each timestep based on collision parameters.

This is conceptually consistent with the proposed Priority Arbitration Head, which introduces state-dependent prioritization *between* objectives (assignment vs. avoidance). DTPA validates the approach of using time-to-collision as a primary signal for priority decisions — the same signal is one of the three inputs proposed for the arbitration head.

**Critical observation:** The reward function in HPER-D3QN uses fixed coefficients (C_goal = +2, C_collision = −1, C_warning = −0.5, C_boundary = −0.5) that are set before training and remain constant regardless of operational state. The paper makes no attempt to dynamically adjust the relative importance of the navigation objective versus the avoidance objective at runtime. DTPA addresses priority *within* collision avoidance; the inter-objective priority remains unaddressed.

---

## Paper B: Yan et al. (2025) — STAAC

**Full Citation:**
Chao Yan, Chang Wang, Han Zhou, Xiaojia Xiang, Xiangke Wang, Lincheng Shen. "Multi-Agent Reinforcement Learning with Spatial-Temporal Attention for Flocking with Collision Avoidance of a Scalable Fixed-Wing UAV Fleet." *IEEE Transactions on Intelligent Transportation Systems*, Vol. 26, No. 2, February 2025, pp. 1769–1782. DOI: 10.1109/TITS.2024.3505929

**Institution:** Nanjing University of Aeronautics and Astronautics (NUAA) + National University of Defense Technology (NUDT)

**Setting:** Multi-agent leader-follower fixed-wing UAV fleet in a 2D environment (1200m × 800m), with a variable number of non-cooperative intruder drones. Formulated as a Dec-POMDP (Decentralized Partially Observable Markov Decision Process).

---

### Contributions

**1. Population-Invariant Network Architecture (STAN — Spatial-Temporal Attention Network)**

The key challenge is that fleet size and intruder count vary — a policy trained for 10 followers cannot easily generalize to 5 or 15 followers with standard architectures.

STAN resolves this by:

**(a) Entity Clustering with Local Spatial Attention (LSA):**
Each follower classifies observed entities into four groups: self, leader, neighbor-followers, neighbor-intruders. A separate attention mechanism computes a spatial embedding for each group:

```
efol_i = Σj αij × FC(ξfol_j)    where αij = softmax(βij)
βij = (ξself)ᵀ Wfol FC(ξfol_j) / √d
```

The spatial embedding dimension is invariant to group size, enabling the architecture to handle varying numbers of entities.

**(b) Global Temporal Attention (GTA):**
Four historical observation frames are processed through LSTM networks per group:
```
hlea_τ = LSTM(elea_τ, hlea_τ-1),   τ ∈ [t-3, t]
```
A temporal attention mechanism then identifies which time slot is most relevant for the current decision:
```
αglo_τ = softmax(FC(hglo_τ))
vi = Σ αglo_τ × hglo_τ
```

**2. Learning Algorithm**

STAAC uses parameter sharing (single shared policy across all homogeneous followers) and clipped double Q-learning (two critics; minimum Q-value is used to reduce overestimation bias). Training paradigm: centralized training, decentralized execution.

---

### Results

**Generalization (zero-shot, no retraining across fleet sizes):**

| Scenario | STAAC Collision Rate | Next Best (HAMA) |
|---|---|---|
| n5m15 | Best | 4.76% higher |
| n10m15 | Best | 7.69% higher |
| n10m20 | **0.34%** | 22.73% higher |

STAAC outperforms MADDPG, MATD3, HAMA, API-MADDPG, BCDDPG, LSTM-DDQN, APF, and ORCA across all evaluated scenarios.

**Ablation study (n10m20):**
- Removing LSA (→TAAC): largest performance drop — entity grouping is the primary driver
- Removing GTA (→SAAC): 29.17% higher collision rate than STAAC — temporal context also critical

**Hardware-in-the-Loop (HITL):** 5 followers + 3 intruders, 100 time steps on real hardware (X-plane 10 + Pixhawk + PX4). Zero collisions. **Average inference time: 1.5ms per UAV.**

---

### Relevance to Proposed Research

STAAC addresses the same domain — multi-agent UAV coordination with simultaneous navigation and collision avoidance objectives — making it directly related work.

The population-invariant architecture demonstrates that per-agent mechanisms with parameter sharing can scale effectively across fleet sizes. The proposed Priority Arbitration Head operates per-agent (each drone computes its own α independently), and parameter sharing can similarly be applied — the computational approach is consistent.

The HITL result of 1.5ms inference per UAV for the full STAN architecture (which includes LSTM + attention mechanisms) establishes that computationally lightweight add-ons to MARL actors are real-time feasible. The Priority Arbitration Head, being a simpler 2-3 layer MLP, would require less computation than STAN.

**Critical observation:** The reward function in STAAC is:
```
r_i = r_leader_following + Σ r_UAV-UAV + Σ r_UAV-intruder
```
The coefficients (P1, P2, w1, w2) are described as "tuning parameters" — they are fixed before training. When formation adherence (r_leader_following, coefficient P1) and intruder avoidance (r_UAV-intruder, coefficient P1) produce conflicting navigation commands, both terms carry identical fixed coefficients. The policy must learn a globally averaged balance. There is no mechanism in STAAC to determine — based on current proximity to intruder, distance to formation position, or number of active threats — whether flocking or avoidance should take priority at a given timestep.

---

## Consolidated Gap Statement

Both papers represent strong, recent contributions to UAV coordination and collision avoidance. Both introduce context-sensitive mechanisms within their respective objectives. Neither paper addresses the following:

**How should the relative weight between competing objectives — navigation/assignment and collision avoidance — be determined at each decision step based on the agent's current operational state?**

In HPER-D3QN, DTPA dynamically prioritizes which aircraft is most threatening (within avoidance). The balance between navigation and avoidance is fixed. In STAAC, LSA dynamically prioritizes which entities matter spatially, and GTA dynamically prioritizes which historical frames matter temporally. The balance between flocking and avoidance is fixed.

Across all thirteen papers reviewed — DA-MAPPO, IGAT-MARL, HPER-D3QN, STAAC, and nine additional papers spanning 2023–2026 — no mechanism proposes a learned, state-conditioned function to determine this balance at runtime. This is the gap that the proposed Priority Arbitration Head addresses.

---

## How These Papers Will Appear in the Final Thesis

**Related Work section:** Both papers will be reviewed alongside DA-MAPPO and IGAT-MARL as the four most directly relevant recent contributions. Their mechanisms will be described accurately, and the gap will be derived from the comparison — not stated as an assumption.

**Motivation for input design:** DTPA's use of TCPA (time to closest approach) confirms that time-to-collision is an established, meaningful signal for collision risk assessment. STAAC's entity grouping confirms that conflict neighborhood structure is a meaningful state descriptor. Both validate the three inputs chosen for the arbitration head: time-to-collision, distance to target, and conflict neighbor count.

**Baseline evaluation:** HPER-D3QN and STAAC address different task configurations (single-agent collision avoidance and multi-agent flocking, respectively) and thus are not direct baselines for evaluation. DA-MAPPO and IGAT-MARL, which address the same joint assignment-avoidance problem, remain the primary baselines. The four fixed-weight ablations (α = 0.3, 0.5, 0.7, 0.9) complete the evaluation design.

---

*These two papers strengthen the literature foundation for the revised problem statement and will be incorporated into the full synopsis.*

