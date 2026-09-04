# 01 — Full Paper Summary

---

## Paper Identity

**Full Title:** Scalable UAV Multi-Hop Networking via Multi-Agent Reinforcement Learning with Large Language Models

**Authors:** Yanggang Xu, Jirong Zha, Weijie Hong, Xiangmin Yi, Geng Chen, Jianfeng Zheng, Chen-Chun Hsia, Xinlei Chen

**Corresponding Author:** Xinlei Chen (Associate Professor, Tsinghua University Shenzhen)
**Equal Contribution:** Yanggang Xu and Jirong Zha

**Year:** 2026 (arXiv v2: March 18, 2026; originally submitted 2025)

**Venue:** Journal of LaTeX Class Files (IEEE journal format); also available on arXiv as arXiv:2505.08448

**Affiliation:** Shenzhen International Graduate School, Tsinghua University; Shenzhen Smartcity Communication; Jilin University

**Research Domain:** Multi-agent reinforcement learning (MARL) / UAV-assisted emergency communications / Wireless networking / AI for disaster response

---

## The Problem

Imagine a major earthquake flattens a city. Within minutes, the cellular towers and fiber-optic cables that millions of people depend on are gone. Rescue teams cannot coordinate. Families cannot call for help. Aid organizations cannot know where to go. This is not a hypothetical — in 2024 alone, 27 climate disasters in the United States caused $184.8 billion in damage and 568 deaths, and communication failure was a central challenge in each.

Unmanned Aerial Vehicles (UAVs, commonly called drones) offer a compelling solution: they can be deployed rapidly, fly above obstacles, and act as aerial relay stations. But organizing a **swarm** of drones to collectively form a working wireless network is a deeply hard problem. Each drone needs to fly to a position where it can relay signals between ground users and the surviving base stations, but the ideal position for each drone depends on where all the other drones go. The drones must form what is called a **multi-hop network** — a chain of relays where data hops from a user to Drone 1, to Drone 2, to Drone 3, and finally to a base station, potentially traveling kilometers across a disaster zone.

Two specific technical challenges make this extremely difficult. First, scaling: as the number of drones grows, the coordination required grows exponentially. Existing reinforcement learning methods struggle because the state space (all possible network configurations) and action space (all possible moves) become astronomically large. Second, exploration: in the early stages of training, drones make random moves and rarely stumble upon a valid, connected network configuration — so the algorithm has almost no useful feedback to learn from. Prior work either focused on small numbers of drones, assumed the backhaul network (the link to the core internet) was already working, or used traditional optimization methods that are too slow and inflexible for real-time dynamic environments.

---

## The Proposed Solution

The authors propose **MRLMN** — *Multi-agent Reinforcement learning with Large language model in Multi-hop Networking* — a framework that attacks both challenges simultaneously with three innovations working together.

**Innovation 1: Role-based grouping with reward decomposition.** Rather than treating all drones identically, MRLMN classifies drones into groups based on their distance to base stations. Drones close to base stations are assigned relay roles; drones close to users are assigned coverage roles. Each group receives a customized reward signal that reflects its specific responsibility. This breaks the impossibly complex global optimization problem into smaller, clearer sub-problems, allowing each drone to receive actionable, targeted feedback about whether it is doing its specific job well.

**Innovation 2: Behavioral constraints for critical drones.** The drones closest to base stations are the most fragile links in the chain — if they disconnect, the entire relay chain collapses. MRLMN applies a special training constraint to these "gateway" drones, guiding them toward actions that maintain their connection to base stations. This prevents the cascading network failures that plague purely unconstrained learning approaches.

**Innovation 3: LLM-guided knowledge distillation.** Before a drone has learned anything, its policy is essentially random. To solve this "cold-start" problem, MRLMN uses GPT-4o as an offline teacher. The environment is simplified into a grid, and the LLM analyzes the scenario using chain-of-thought reasoning to suggest smart initial drone deployment positions. These suggestions are then matched to actual drone positions using the **Hungarian algorithm** (an optimal assignment technique), and the drone policies are trained to mimic the LLM's strategic reasoning. Crucially, the LLM is only used during training — once deployed, drones operate entirely on their own learned policies without any LLM involvement.

---

## The Method (in one paragraph)

The UAV networking task is modeled as a **stochastic game** — a mathematical framework for multi-agent decision-making under uncertainty. Each drone observes its local environment (positions of all nodes, signal quality of all links, connectivity status) plus an aggregated view shared across the swarm. Drones are partitioned into groups based on their initial distance to base stations, and each group's reward is a weighted sum of the global team reward plus individual components measuring direct UE coverage and relay contribution. An Independent PPO (IPPO) algorithm trains each drone's policy network independently. During training, GPT-4o is queried periodically to suggest a full drone deployment; the Hungarian algorithm matches each LLM-suggested position to the nearest actual drone, deriving an expected movement direction for each drone; a cross-entropy distillation loss then nudges the drone's policy toward that direction. Simultaneously, a behavioral constraint loss penalizes gateway drones that drift away from base station connectivity. At deployment time, each drone runs only its lightweight MLP policy network — no LLM, no central controller, fully decentralized.

---

## The Key Results

**Result 1: MRLMN significantly outperforms all five baseline methods in training reward.**
MRLMN's training curve stabilizes above a reward of 0.8, while the best competing method (GVis) plateaus significantly lower. MAPPO and GA2C stabilize between 0.4 and 0.6. This means MRLMN learns a substantially better policy — more connected users, higher data rates — within the same number of training steps.

**Result 2: 27% improvement in UE coverage across different environment sizes.**
When the environment area was varied from 6.76 km² to 14.44 km² with 18 UAVs, MRLMN achieved an average of 27% more connected user equipment (UE) than the best baseline. In practical terms: where a competing method might connect 50 out of 150 users, MRLMN connects approximately 64.

**Result 3: 52% higher data rate and 23% more UE coverage as swarm size increases.**
As the number of UAVs was varied from 12 to 24 (with a fixed 3.5 km × 3.5 km area), MRLMN achieved on average 23% higher UE coverage, 52% higher average data rate per user, and 19% higher UAV availability ratio (proportion of drones maintaining network connectivity) compared to all baseline methods combined.

**Result 4: Every module contributes — removing any one causes measurable decline.**
The ablation study showed that removing reward decomposition (NR) dropped connected UE proportion from 46% to 40% and data rate from 5.2 to 4.5 Mbps in the largest environment. Removing knowledge distillation (NL) caused similar degradation, and removing behavioral constraints (NC) caused the most pronounced drop in UAV availability. Removing any single module causes at least a 6% drop in UE coverage and 10% drop in data rate.

**Result 5: Policy diversity matters — more trained policies means better performance.**
In a controlled experiment on parameter sharing, allowing each of 18 drones to train its own independent policy (18 policies) versus all sharing one policy (4 policies) improved UE coverage from 45% to 65% and data rate from 5.1 Mbps to 7.4 Mbps. The trade-off is training time (20 hours for full sharing vs. 40 hours for full independence).

---

## The Contribution

This paper makes four distinct contributions to the research community: (1) it formulates large-scale multi-hop UAV networking as a stochastic game for the first time in a way that explicitly handles multi-hop connectivity constraints; (2) it introduces role-based agent grouping with decomposed rewards for scalable MARL coordination; (3) it designs a novel LLM-to-MARL knowledge distillation pipeline using Hungarian matching to solve the cold-start problem without requiring online LLM inference; and (4) it validates all claims with extensive simulation across multiple scales, UAV counts, and ablation configurations.

**One-sentence takeaway you can quote to sir:** "MRLMN is the first framework to combine multi-agent reinforcement learning with large language model knowledge distillation for scalable UAV multi-hop networking, achieving up to 52% higher data rates than state-of-the-art baselines while remaining fully decentralized at deployment time."
