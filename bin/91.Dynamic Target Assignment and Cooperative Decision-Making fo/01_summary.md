# 01 — Full Paper Summary

---

## Paper Identity

- **Full Title:** Dynamic Target Assignment and Cooperative Decision-Making for UAV Swarms Based on Multi-Agent Reinforcement Learning
- **Authors:** Yuanyuan Sheng, Xianan Xie, Huanyu Liu, Junbao Li (Harbin Institute of Technology, China)
- **Year:** 2026
- **Venue:** IEEE Internet of Things Journal (DOI: 10.1109/JIOT.2026.3686066) — accepted, pre-publication version
- **Research Domain:** Multi-Agent Reinforcement Learning (MARL), UAV Swarms, Autonomous Navigation, IoT-Edge Systems

---

## The Problem

Imagine you have a team of drones that need to fly through a cluttered space — full of obstacles — and each drone must reach a different target. Simple enough, right? Now imagine those targets keep moving. The drone that was heading toward Target A finds that Target A has shifted to a completely different location. Meanwhile, the drone must also avoid crashing into walls, buildings, and its own teammates.

This is the core challenge that UAV swarm systems face in the real world. The problem is especially hard for two reasons. First, no single drone knows everything — each only has limited local perception (via a LiDAR sensor) and can only talk to nearby neighbors. This is called **partial observability**. Second, the classic engineering approach was to solve "who goes where" and "how to fly there safely" as two completely separate problems using hand-designed rules. That works well when targets are fixed and the world is fully known, but the moment targets start moving, these rigid pipelines fall apart: the drone may be flying toward an old target location, collisions become more likely, and the whole team's coordination degrades.

Existing deep reinforcement learning (DRL) approaches tried to improve on this, but most still assumed targets don't move. Even those that handled task assignment treated it as a separate pre-processing step, not something updated in real time during flight. The result was a persistent gap: no method tightly coupled the "who chases what" decision with the real-time navigation behavior of each drone in truly dynamic, partially observable settings.

---

## The Proposed Solution

The authors propose **DA-MAPPO** — Dynamic Assignment-aware Multi-Agent Proximal Policy Optimization. The core idea is elegant: instead of treating target assignment and navigation as separate problems, embed the assignment outcome directly into what each drone "sees" and "thinks about" at every single decision step.

Here is what makes it different from everything before it:

1. **Online minimum-cost allocation:** At every decision step, the system solves a mathematical assignment problem (which drone should chase which target) based on current distances. The solution is updated continuously — not once at the start, not every 50 steps, but every single step.

2. **Assignment-augmented observations:** The result of the assignment is fed directly into each drone's local observation vector. So every drone always knows its current assigned target and can immediately react when that assignment changes.

3. **Hierarchical cooperative reward:** A carefully designed reward function simultaneously encourages each drone to make progress toward its target, avoid obstacles, avoid hitting teammates, stay in bounds, and contribute to the team's overall completion — all in one signal.

4. **CTDE paradigm:** Training uses a Centralized Critic (who can see everything) to guide the agents, but each drone executes its policy using only its own local information. This means the swarm can be deployed without needing a central controller in the real world.

---

## The Method (in one paragraph)

Each UAV is equipped with a 35-beam LiDAR sensor and communicates only with neighbors within a limited radius. At every decision step, the framework runs three stages: (1) Environmental Perception — each drone collects obstacle data, kinematic state, and neighboring drone positions; (2) Target Allocation — a Hungarian-algorithm-based minimum-cost assignment pairs each drone to the nearest unoccupied target; (3) Cooperative Decision-Making — each drone's full observation (obstacles + own state + assigned target + teammate positions) is fed into a shared neural network policy that outputs continuous velocity and angular velocity commands. The entire system is trained using MAPPO (Multi-Agent Proximal Policy Optimization) with a clipped surrogate loss and entropy bonus for exploration, and a Generalized Advantage Estimation (GAE) method for stable advantage computation. A progressive curriculum training strategy gradually increases obstacle density from 0–10 obstacles up to 35–40 obstacles over 3 million environment steps.

---

## The Key Results

1. **90%–99% mission success in dynamic multi-target environments.**
   In the easiest environment (30 obstacles), DA-MAPPO achieves 99% success even when targets are moving. In the hardest setting (50 obstacles), it still achieves 90%. This means it almost never fails.

2. **Up to 25 percentage points better than the best competing method.**
   The next-best baseline (RMAPPO) achieved only 67% success in the hardest dynamic environment. DA-MAPPO achieved 90% — a 23-point improvement. This is a very large margin in a field where 5% improvements are considered meaningful.

3. **Near-zero degradation when switching from static to dynamic targets.**
   DA-MAPPO in a static (fixed target) environment achieves 92% success in the hardest setting; in the dynamic version, it still gets 90% — only a 2% drop. Competing methods degraded by 20–30 percentage points under the same switch, confirming that DA-MAPPO truly handles dynamic environments rather than just tolerating them.

4. **Shorter trajectories and fewer steps — not just safer, but faster.**
   DA-MAPPO achieves the lowest average trajectory length (Lave) and lowest average time steps (Tave) in almost every dynamic scenario, meaning it is not just safe but also efficient. For example, in ENV-2 (40 obstacles, dynamic), DA-MAPPO's Tave is 38.32 steps versus MAPPO's 50.14 steps — a 24% speed improvement.

5. **Robust to real-world imperfections.**
   Even with 50% packet loss and 6-step communication delays, performance barely changes (94% vs. 95% baseline). With heavy sensor noise (sigma = 0.50), success still holds at 90%. The framework runs in 1.496 ms per step on a single agent and scales sub-linearly on edge hardware (NVIDIA Jetson Orin Nano).

---

## The Contribution

This paper demonstrates for the first time that tight real-time coupling of online target allocation with multi-agent reinforcement learning — through assignment-augmented observations and hierarchical cooperative rewards — achieves both safety and efficiency in truly dynamic UAV swarm missions under partial observability, making it practically deployable on IoT-edge platforms.

**One-sentence takeaway Ayesha can quote to sir:**
> "DA-MAPPO is the first framework to continuously embed real-time target reassignment directly into each drone's perception, enabling a swarm to adapt instantly to moving targets while maintaining collision-free coordination — and it works on actual edge hardware."
