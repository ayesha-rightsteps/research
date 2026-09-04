# 03 — Methodology: Exactly What the Researchers Did

---

## Research Design

**Type of study:** Simulation-based experimental study combining meta-learning (MAML) with multi-agent deep reinforcement learning (MA-DDPG).

**Overall strategy:** The authors formulate the multi-UAV disaster coordination problem as a decentralized MARL problem with heterogeneous agents. The RCTP framework is built in two stages: (1) MAML meta-training across a distribution of disaster scenarios to produce a fast-adapting meta-policy, and (2) MA-DDPG fine-tuning and execution within specific disaster scenarios. Coalition formation is handled through resource-aware suitability scores computed and updated online.

**Note:** The full paper is behind a journal paywall — the following methodology is reconstructed from the abstract, keywords, and known properties of MAML and MA-DDPG. Where specific details are not confirmed by the paper, this is noted.

---

## The Environment

**Application domain:** Disaster response — search, rescue, and situational assessment missions.

**Simulation environment:** The paper does not specify exact map dimensions, but environments include dynamic obstacles (debris, collapsed structures), intermittent communication zones, and multiple tasks distributed across the disaster area.

**Agents:** 10–30 heterogeneous UAVs (tested across this range).

**Tasks:** Multiple simultaneous tasks including search, rescue, and situational assessment — each with different resource requirements that different drone types fulfill.

**Obstacles:** Dynamic — moving debris, uncertain terrain. This is different from static NFZ models in Papers 3 and 4.

**Communication model:** Explicit LoS/NLoS switching — drones can detect when they lose direct line-of-sight and adjust coordination behavior accordingly. This is the most realistic communication model in the folder.

**Failures:** UAV failures are explicitly simulated mid-mission — drones drop out and the system must recover.

---

## MAML Component — How Rapid Adaptation Works

MAML (Model-Agnostic Meta-Learning) was originally proposed by Finn et al. (2017). The paper integrates it into multi-agent UAV control as follows:

**Meta-Training Phase (happens before deployment):**

```
FOR each disaster scenario in training distribution:
    1. Initialize policy parameters θ (shared meta-parameters)
    2. Collect a small batch of experience in this scenario
    3. Compute task-specific gradient update:
       θ_i = θ - α · ∇_θ L_task_i(θ)
       (α = inner learning rate)
    4. Evaluate updated parameters θ_i on a new batch
    5. Compute meta-gradient across all tasks:
       θ ← θ - β · ∇_θ Σ L_task_i(θ_i)
       (β = outer/meta learning rate)
RESULT: Meta-parameters θ that are a good
        initialization for ANY new disaster scenario
```

**Deployment Phase (new disaster, never seen before):**
```
1. Load meta-trained parameters θ
2. Collect a very small amount of experience in the new disaster
3. Perform K gradient steps (K is small — 1 to 5 steps)
4. Deploy adapted policy — UAVs now perform near-optimally
   in the new scenario without extensive retraining
```

**Key insight:** The meta-parameters θ are specifically optimized so that a small number of gradient steps from θ will produce a good policy for any new disaster scenario. This is fundamentally different from just training a general model — the gradient structure of θ is explicitly shaped to enable fast adaptation.

---

## MA-DDPG Component — Multi-Agent Continuous Control

Each UAV runs a DDPG-style actor-critic architecture:

**Actor network:** Takes local observations as input → outputs continuous control actions (speed, heading, coalition decisions)

**Critic network:** During training, takes global state information from all agents → evaluates the quality of each agent's actions more accurately (centralized training)

**Execution:** Each UAV runs only its own actor with local observations (distributed execution — no central controller needed in deployment)

This is the standard CTDE (Centralized Training, Distributed Execution) framework — the same approach used in Paper 4 (PO-WMFDDPG).

**State space** (the paper does not specify exact dimensions, but likely includes):
- UAV own position, velocity, heading
- Battery/resource level (unique to this paper — heterogeneity representation)
- Task locations and requirements within sensor range
- Communication status (LoS/NLoS) with other drones
- Coalition membership status

**Action space** (continuous):
- Movement: linear and angular acceleration
- Coalition actions: decisions about which coalition to join or leave (the paper does not specify exact encoding)

---

## Resource-Aware Suitability Score Mechanism

This is a key novel component unique to this paper:

```
For each drone i and each task j:
    suitability_score(i, j) = f(capabilities_i, requirements_j, battery_i, distance_i_to_j)
```

Where:
- capabilities_i = drone i's sensor type, speed class, payload capacity
- requirements_j = task j's sensor needs, urgency, required resources
- battery_i = current battery level of drone i
- distance_i_to_j = current distance from drone i to task j

The score is updated **online** — continuously recalculated as the mission progresses and drone states change.

**Coalition formation algorithm:**
1. Compute suitability scores for all drone-task pairs
2. Assign drones to coalitions that maximize total suitability (optimization step)
3. When a drone fails: remove it from scores, recompute, reform affected coalitions
4. Winning coalition for each task = drones with highest combined suitability for that task's requirements

---

## Training Setup

**Meta-training:** MAML trains across a distribution of diverse disaster scenarios (varied layouts, obstacle densities, task types). The paper does not specify the exact number of training scenarios, but MAML typically uses dozens to hundreds of diverse tasks.

**Fine-tuning per scenario:** K gradient steps (small number) after observing the new scenario.

**Baselines compared:**
- PPO (Proximal Policy Optimization) — same environment, no MAML, no coalitions
- DQN — same environment, discrete actions
- MA-DDPG — same multi-agent setup but without the MAML meta-training layer

**Evaluation scenarios:** 10–30 UAVs; with and without drone failures; varying levels of communication degradation (LoS vs. NLoS switching rates); noisy sensor conditions.

---

## Pipeline Diagram

```
PRE-DEPLOYMENT: META-TRAINING
┌─────────────────────────────────────────────┐
│   Distribution of Disaster Scenarios        │
│   (Scenario A, B, C, ... N)                 │
└──────────────────────┬──────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────┐
│            MAML META-TRAINING               │
│  Inner loop: adapt policy to each scenario  │
│  Outer loop: optimize for fast adaptation   │
│  Output: Meta-parameters θ*                 │
└──────────────────────┬──────────────────────┘
                       │
═══════════ DEPLOYMENT TIME ═════════════════
                       │
                       ▼
┌─────────────────────────────────────────────┐
│        NEW DISASTER SCENARIO                │
│  (Never seen before — flood, earthquake..)  │
└──────────────────────┬──────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────┐
│     FEW-SHOT ADAPTATION (K steps)           │
│  Load θ* → collect small experience →       │
│  K gradient updates → adapted policy θ_new  │
└──────────────────────┬──────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────┐
│      PARTIAL OBSERVATION PER UAV            │
│  Own state + nearby tasks + comm status     │
│  (LoS/NLoS) + battery level                 │
└──────────────────────┬──────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────┐
│   RESOURCE-AWARE SUITABILITY SCORING        │
│  For each drone-task pair → score           │
│  Group drones into coalitions               │
└──────────────────────┬──────────────────────┘
                       │
              ┌────────┴────────┐
              ▼                 ▼
┌─────────────────┐    ┌─────────────────────┐
│  ACTOR NETWORK  │    │  CRITIC (training)   │
│  Local obs →    │    │  Global info →       │
│  Continuous     │    │  Q-value estimate    │
│  actions        │    │                      │
└────────┬────────┘    └─────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────┐
│      UAV EXECUTES ACTION                    │
│  Move + path plan + coalition update        │
│  Energy-aware routing considered            │
└──────────────────────┬──────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────┐
│       DRONE FAILURE DETECTION               │
│  If failure detected:                       │
│  → Recompute suitability scores             │
│  → Reform coalitions with remaining drones  │
│  → Reassign failed drone's tasks            │
└──────────────────────┬──────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────┐
│      MISSION COMPLETE                       │
│  30-40% faster than baselines               │
│  10-20% less energy                         │
│  Robust to drone failures                   │
└─────────────────────────────────────────────┘
```
