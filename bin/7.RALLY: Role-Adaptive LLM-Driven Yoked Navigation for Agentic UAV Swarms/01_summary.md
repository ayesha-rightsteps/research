# 01 — Full Paper Summary

---

## Paper Identity

- **Full Title:** RALLY: Role-Adaptive LLM-Driven Yoked Navigation for Agentic UAV Swarms
- **Authors:** Ziyao Wang, Rongpeng Li, Sizhao Li, Yuming Xiang, Haiping Wang, Zhifeng Zhao, and Honggang Zhang
- **Year:** 2025
- **Venue:** IEEE Open Journal of Vehicular Technology (OJVT), Volume 6, 2025
- **DOI:** 10.1109/OJVT.2025.3610852
- **Type:** Invited Paper
- **Research Domain:** Multi-agent systems, UAV swarm control, Large Language Models (LLMs), Multi-Agent Reinforcement Learning (MARL), Agentic AI

---

## The Problem

Imagine you need to send a fleet of eight drones into a disaster zone. They must cover multiple survivor areas, dodge obstacles, and continuously evade a pursuing adversarial drone — all without any single drone having the full picture of what is happening. Each drone can only see what is within its local observation range, can only talk to neighbors nearby, and must still coordinate with the whole swarm to be effective. This is the core challenge the paper addresses, formally called the **DS-CEFC task** (Dynamic Swarm coordination with Cooperative Evasion and Formation Coverage).

This problem affects researchers building autonomous systems for disaster response, military operations, surveillance, and exploration — essentially anywhere a group of robots must self-organize under uncertainty and adversarial pressure.

Existing solutions fall into two camps, both deeply flawed. **Traditional MARL approaches** (such as QMIX or MADDPG) teach drones to cooperate through trial-and-error reinforcement learning. They work reasonably well in controlled scenarios but communicate using raw numerical vectors that carry no meaning — the drones cannot explain their intentions, and their roles are rigidly fixed, meaning they cannot adapt when the situation changes. When you try to scale these methods up to more drones or new environments, performance collapses because the learned policy is too narrowly specialized. **LLM-based approaches** (like CoNavGPT) leverage the rich reasoning ability of large language models to plan drone missions using natural language. They generalize well to new scenarios because they draw on the LLM's vast world knowledge, but they rely entirely on pre-trained knowledge without any ability to improve from real-world experience. They get stuck in local optima, cannot explore effectively, and are computationally impractical for resource-limited onboard UAV hardware.

Neither approach alone is sufficient. What the field needs is a framework that combines the semantic reasoning and generalization power of LLMs with the adaptive, experience-driven learning of MARL — and that is precisely the gap RALLY fills.

---

## The Proposed Solution

RALLY (Role-Adaptive LLM-Driven Yoked Navigation) is a hybrid framework that integrates LLMs with MARL to give each drone both semantic intelligence and learned adaptability.

The core innovation is a **two-stage semantic consensus process** paired with a **dynamic role assignment mechanism**. In the first stage, each drone uses an LLM to reason about its local observations — the positions of teammates, the enemy, and target areas — and generates an initial navigation intention expressed in natural language. In the second stage, the drone communicates with nearby neighbors, and the LLM refines the initial intention into a collective consensus goal, taking each agent's dynamically assigned role into account.

What makes RALLY truly different from all prior work is the **Role-value Mixing Network (RMIX)** — a credit-assignment mechanism that learns which role (Commander, Coordinator, or Executor) each drone should play at each moment. Critically, RMIX is pre-seeded with offline data collected from GPT-4o's zero-shot role suggestions, meaning it starts already knowing something sensible rather than exploring blindly from scratch. It then continuously improves during online reinforcement learning.

RALLY is also designed for practical deployment: it distills GPT-4o's reasoning ability into a tiny local model (Qwen2.5-1.5B, compressed to under 5 GB) that can run directly on UAV onboard GPUs, eliminating dependence on cloud APIs in the field.

---

## The Method (in one paragraph)

RALLY operates as the high-level policy in a three-layer UAV control architecture. At the top level, each drone observes its local environment (its own position and velocity, the enemy's position and velocity, and the positions and urgency levels of target regions) and feeds this into a two-stage LLM-based reasoning process. In Stage 1 (intention generation), the LLM uses a structured task prompt, a Chain-of-Thought reasoning guide, and the drone's own observation to produce an initial target intention. Simultaneously, the RMIX-based role selection policy takes the drone's observation as input and assigns it one of three roles: Commander (maximizes individual reward, makes independent decisions), Coordinator (balances team and individual gains, defers to the Commander), or Executor (follows the Coordinator's guidance, reverts to own strategy if needed). In Stage 2 (consensus refinement), each drone broadcasts its intention and role to neighbors within communication range, receives their intentions and roles, and the LLM synthesizes all of this into a final consensus navigation goal. This consensus goal then guides the mid-level MARL policy that handles formation-keeping and obstacle avoidance, while the low-level PID controller handles actual flight dynamics. RMIX is trained through a hybrid offline-online approach: GPT-4o first seeds the replay buffer with sensible role assignments, and then RMIX continues learning from online interactions to improve credit assignment for cooperative multi-drone behavior.

---

## The Key Results

1. **RALLY achieves the highest mean reward and narrowest variance across all baselines.** In 30-episode evaluations on the DS-CEFC task in the Multi-Agent Particle Environment, RALLY consistently outperforms CIHRL (the state-of-the-art MARL baseline), CoNavGPT (a pure LLM planner), and DITTO (an LLM with fixed role assignment). This means RALLY completes missions more reliably and consistently than any prior approach.

2. **RALLY generalizes to unseen swarm sizes without retraining.** When tested with swarm sizes of 8, 9, 10, and 11 drones (having been trained on 8), RALLY maintains high performance. By contrast, the CIHRL baseline degrades substantially as the swarm grows beyond its training configuration — agents fall into habitual grouping patterns and fail to cover additional targets. This is one of the most practically significant results: real deployments often involve variable team sizes.

3. **RALLY generalizes across different target area configurations.** Tested on three different grid layouts (3x3, 2x4, and 4x2), RALLY shows no significant difference in reward performance, demonstrating robust adaptability to varying environmental conditions.

4. **The three-role architecture (Commander-Coordinator-Executor) is optimal.** An ablation study with 1, 2, 3, and 4 roles shows that the three-role configuration achieves the best combination of high mean reward and low variance. A single-role setup delivers the worst performance (~-3,000 mean reward). Adding a fourth "Decoy" role actually hurts performance by introducing too much coordination overhead.

5. **The fine-tuned Qwen2.5-1.5B model achieves practical on-device deployment.** With only 2.9 GB memory footprint and 14.48 seconds average inference time on an NVIDIA RTX 4090, the 1.5B parameter model strikes the best balance between decision quality and computational efficiency, making real-world UAV deployment feasible.

---

## The Contribution

RALLY demonstrates that the best path to intelligent UAV swarm control is to combine LLM reasoning (for interpretable, generalizable semantic planning) with MARL-driven role learning (for adaptive, experience-based coordination), showing that this hybrid consistently and significantly outperforms either approach alone.

**One-sentence takeaway for sir:** "RALLY is the first framework to dynamically assign heterogeneous roles to UAVs using a credit-based reinforcement learning mechanism seeded by LLM priors, enabling drone swarms to form consensus through natural language reasoning while remaining adaptable to new environments and swarm sizes."
