# 01 — Paper Summary

---

## Paper Identity

**Full Title:** Deep reinforcement learning-based adaptive collision avoidance method for UAV in joint operational airspace

**Authors:** Yan Shen, Xuejun Zhang (corresponding author), Yan Li, Weidong Zhang

**Institution:** Beihang University, Beijing, China (School of Electronic and Information Engineering; State Key Laboratory of CNS/ATM; School of Cyber Science and Technology)

**Year:** 2026 (received May 2025, accepted August 2025, published online September 2025)

**Venue:** *Defence Technology*, Volume 56, Pages 142–159. Published by Elsevier B.V. on behalf of KeAi Communications Co. Ltd.

**Research Domain:** Deep reinforcement learning applied to autonomous UAV collision avoidance in military joint operational airspace

---

## The Problem

Imagine a battlefield where manned fighter jets and unmanned drones are flying in the same patch of sky, each following their own mission, and none of them can talk to each other through a shared command system. Communication links may be jammed or broken. The GPS or data network that normally feeds an aircraft its situational awareness picture is unavailable. Wind is blowing unpredictably. In this environment, a UAV must still somehow figure out in real time which aircraft around it are dangerous, how dangerous they are, and what maneuver to make — all within fractions of a second.

This is the joint operational airspace collision avoidance problem, and it is not trivial. The aircraft involved are heterogeneous: manned jets fly faster (80–160 m/s), respond differently to wind, and have larger safety buffers than drones (60–110 m/s). The UAV cannot see everything — its sensors only cover a limited range, and even within that range the information is incomplete and noisy due to wind disturbances and sensor errors. Traditional methods fail here. Geometry-based approaches (like Dubins paths) are too rigid for dynamic, multi-aircraft environments. Optimization methods like genetic algorithms and particle swarm optimization converge too slowly or get stuck in local solutions. Model Predictive Control requires knowing the system dynamics accurately, which is impossible when the environment is uncertain.

Existing deep reinforcement learning methods took a step in the right direction but still fell short. Most assumed all aircraft in the environment were the same type (homogeneous), did not account for dynamic wind fields, and used oversimplified observation models that would not work in a real battlefield. The gap this paper fills is the combination of heterogeneous aircraft types, partial observability, realistic wind uncertainty, and intelligent experience replay — all at once, in one coherent system.

---

## The Proposed Solution

The authors propose the **HPER-D3QN** algorithm — a deep reinforcement learning method that trains a UAV to avoid collisions autonomously through three interlocking innovations:

1. **A sector-based partial observation model combined with Dynamic Threat Prioritization Assessment (DTPA):** Instead of trying to track all aircraft globally (which is computationally impossible in real time), the UAV divides its sensing range into K sectors (8 sectors in the experiments). Within each sector, the DTPA algorithm calculates a threat score for every detected aircraft based on three factors: time to closest approach (TCPA), distance at closest approach (DCPA), and the aircraft's type (manned aircraft scores higher because it is more dangerous to collide with). The aircraft with the highest threat score in each sector becomes the "intruder" — the one the UAV monitors.

2. **A Hierarchical Prioritized Experience Replay (HPER) mechanism:** During training, not all learning experiences are equally valuable. Experiences involving a collision, reaching the destination, or violating airspace boundaries are rare but critical. The standard approach of sampling all experiences equally wastes most training time on boring "nothing happened" situations. HPER solves this by sorting all experiences into three priority layers — high (collisions, arrivals, boundary violations), medium (entering warning zones), and low (safe cruise flight) — and sampling more heavily from the high-priority layers, while also using Temporal-Difference error to rank individual experiences within each layer.

3. **The D3QN network backbone:** The underlying neural network is a Double-Dueling Deep Q-Network (D3QN), which combines two improvements over basic DQN: Double Q-learning (to prevent overestimating action values) and a dueling architecture (which separately estimates how good a state is versus the advantage of each action), giving more accurate and stable learning.

---

## The Method (in one paragraph)

The UAV operates in a simulated 30 km × 30 km joint airspace containing up to 25 mixed manned and unmanned aircraft, all subject to a dynamic periodic wind field and individual state uncertainties (heading and speed errors). At each one-second time step, the UAV's onboard sensors scan a 4,000-meter detection radius divided into 8 sectors. The DTPA algorithm evaluates every detected aircraft and identifies one "intruder" per sector based on a weighted threat score combining TCPA, DCPA, and aircraft type. This produces a compact observation vector (the UAV's own speed, heading to destination, wind state, and one intruder observation per sector) that feeds into the D3QN neural network (architecture: 45 × 128 × 64 × 32 × 9 neurons across 5 layers). The network outputs Q-values for 9 discrete maneuver actions (combinations of speed change and heading change), and the UAV selects the best action using an epsilon-greedy exploration policy. The resulting experience tuple is classified by the HPER mechanism and stored in the appropriate priority layer. During training, HPER samples mini-batches weighted by both layer priority and individual TD error, updating the prediction network's weights via the DDQN target formula. The model was trained for up to 30,000 episodes on a TITAN RTX GPU and then transferred to a high-fidelity Unity3D-based battlefield simulation platform to validate real-world applicability.

---

## Key Results

1. **HPER-D3QN achieves 96.28% success rate in crowded airspace (25 aircraft), compared to 91.84% for basic DQN — a gap of over 4 percentage points.**
   In plain terms: in a battlefield with 25 aircraft all moving unpredictably, the proposed method successfully avoids collisions and reaches its target destination more than 9 times out of 10, while older methods fail noticeably more often.

2. **Under maximum environmental uncertainty (wind, heading errors, speed errors at Level 5), HPER-D3QN maintains 95.06% success rate while basic DQN drops to 86.93%.**
   This means the new method stays robust under the most challenging real-world-like conditions, whereas the older method's performance degrades significantly with increasing chaos.

3. **HPER-D3QN's task completion time increases by only 42.91 seconds when going from sparse (3 aircraft) to crowded (25 aircraft) airspace; DQN's time increases by 65.95 seconds.**
   The new method stays efficient even in dense traffic — it finds smarter, shorter paths to its destination rather than taking excessive detours to avoid threats.

4. **Ablation experiments show that removing HPER causes a 9.27% drop in success rate and an 87.26% surge in Frequency of Hazardous Proximity (FHP).**
   This confirms that HPER is the single most important innovation in the paper — without it, the system degrades dramatically.

5. **The trained model transferred successfully to a high-fidelity Unity3D simulation platform, autonomously avoiding a manned aircraft at t=125s, another UAV at t=216s, and reaching its destination at t=295s.**
   This validates that the algorithm is not just a simulation artifact — it generalizes to a realistic battlefield-quality virtual environment.

---

## The Contribution

This paper demonstrates that a UAV can learn to autonomously avoid collisions with both manned and unmanned aircraft in a realistically uncertain, partially observable joint battlefield airspace — by combining intelligent threat prioritization (DTPA), hierarchical experience management (HPER), and a stable deep Q-learning backbone (D3QN) — achieving state-of-the-art performance that conventional and prior DRL methods cannot match.
