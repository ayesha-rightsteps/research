# 04 — Results: What They Found and Why It Matters

---

## Key Results (Numbered List)

---

### Result 1: MRLMN Converges Faster and to a Higher Reward Than All Baselines

MRLMN's training reward stabilizes above 0.8 after approximately 6–7 million training steps, while the best competing method (GVis) plateaus well below this level. MAPPO and GA2C stabilize in the range of 0.4 to 0.6. The two A2C-based methods (IA2C and MAA2C) converge the slowest and fluctuate around 0.4.

**What this means in practical terms:** A training reward above 0.8 indicates that approximately 80% or more of the joint objective (UE coverage + weighted data rate) is being achieved. Competing methods achieving only 0.4–0.6 means they are reaching at best 60% of what is theoretically possible — leaving a large fraction of survivors disconnected or underserved.

**Comparison with prior work:** This is a significant margin. In reinforcement learning research, achieving a gap of 20–40% in reward over strong baselines like MAPPO is considered highly competitive. The fact that MRLMN outperforms a heterogeneous graph neural network method (GVis) is particularly noteworthy because GNN-based methods are considered state-of-the-art for multi-agent networking.

---

### Result 2: 27% More UE Coverage Across Environment Sizes ⭐ MOST IMPRESSIVE RESULT

When the environment size is varied from 6.76 km² to 14.44 km² with 18 UAVs fixed, MRLMN achieves an average of approximately 27% higher connected UE proportion than the best baseline.

**Specific numbers from Figure 5(a):** At the standard 12.25 km² (3.5 km × 3.5 km) environment, MRLMN achieves approximately 70–75% UE connectivity while baselines achieve 50–60%. At the largest environment (14.44 km²), MRLMN still achieves around 46% connectivity while NR achieves only 40% — a 15% absolute gap that represents dozens more survivors connected.

**What this means in practical terms:** In a disaster scenario with 150 survivors, the difference between 46% and 40% connectivity is approximately 9 additional people who can make contact with rescue teams. At scale (thousands of survivors), this gap translates directly into lives.

**Why it is the most impressive result:** This result shows that MRLMN does not just learn faster — it learns a qualitatively better policy. Even as the environment grows larger and the problem becomes harder, MRLMN maintains its advantage, whereas competing methods degrade faster.

---

### Result 3: 52% Higher Data Rate as UAV Count Scales

When UAV count is varied from 12 to 24 (in a 3.5 km × 3.5 km area), MRLMN achieves on average 52% higher data rate per UE compared to all baseline methods combined.

**Specific numbers from Figure 5(d):** At 18 UAVs, MRLMN achieves approximately 7–8 Mbps average data rate per UE, while baselines achieve 4–6 Mbps. At 24 UAVs, MRLMN approaches 10+ Mbps while baselines remain below 8 Mbps.

**What this means in practical terms:** A data rate of 7+ Mbps is sufficient for real-time video communication, GPS location sharing, and medical data transmission. Below 4 Mbps, video calls become unstable. The 52% improvement could be the difference between a rescue team receiving a live video feed from a survivor's phone versus only a text message.

**Comparison with prior work:** None of the five baseline methods — including MAPPO, which is considered a strong MARL baseline — approach MRLMN's data rate performance, confirming that the combination of role-based grouping and LLM distillation provides genuine, substantial benefits.

---

### Result 4: 23% Higher UE Coverage and 19% Higher UAV Availability Across All UAV Counts

Across the full range of UAV counts (12 to 24), MRLMN consistently achieves:
- 23% higher UE coverage proportion
- 52% higher average data rate
- 19% higher UAV availability ratio (proportion of drones connected to the BS)

**What "19% higher UAV availability" means:** If a baseline method has 80% of drones connected to the relay chain, MRLMN achieves closer to 95%. In a 18-drone swarm, that is the difference between 14 and 17 drones being effective relay nodes — which directly determines how many users can be covered.

**Comparison:** In smaller environments (6.76 km²), MRLMN achieves nearly 100% UAV availability, while all methods perform reasonably well. The advantage becomes most pronounced in large environments (14.44 km²) where MRLMN outperforms the next-best method by approximately 17 percentage points in UAV availability.

---

### Result 5: Ablation Confirms Every Module is Necessary

Removing any single module from MRLMN causes a statistically significant performance decline:

| Configuration | Connected UE % (14.44 km²) | Data Rate (Mbps) | UAV Availability |
|---|---|---|---|
| Full MRLMN | 46% | 5.2 Mbps | 88% |
| No reward decomposition (NR) | 40% | 4.5 Mbps | 82% |
| No knowledge distillation (NL) | ~42% | ~4.7 Mbps | ~84% |
| No behavioral constraints (NC) | ~43% | ~4.8 Mbps | ~80% |

(NL and NC values are read from Figure 6 approximations)

**Minimum impact per removed module:** At least 6% drop in UE coverage, 10% drop in data rate.

**Most critical module for UAV stability:** Behavioral constraints (NC shows the sharpest drop in UAV availability), confirming that gateway drone management is essential for preventing cascading failures.

**Most critical module for exploration efficiency:** Knowledge distillation (NL shows degraded convergence behavior, particularly in early training), confirming the cold-start problem is real and the LLM meaningfully accelerates learning.

---

### Result 6: Policy Diversity Trades Off Against Training Time

In the parameter-sharing experiment:
- 4 trained policies (maximum sharing) → 45% UE coverage, 5.1 Mbps data rate, ~93% UAV availability, 20 hours training
- 18 trained policies (no sharing) → 65% UE coverage, 7.4 Mbps data rate, ~98% UAV availability, 40 hours training

**Interpretation:** Sharing parameters across drones in the same group is a reasonable engineering trade-off (cut training time in half), but it costs about 20 percentage points of UE coverage. The paper recommends that practitioners choose a point on this trade-off curve based on their computational budget.

---

## Tables and Figures Explained

---

### Table I: Simulation Parameter Settings

**What it shows:** All fixed hyperparameters of the simulation environment, including frequency, bandwidth, power levels, path loss constants, SNR threshold, and training weights.

**Key takeaway:** The simulation is grounded in realistic wireless communication parameters. The 2.4 GHz frequency, 25 dB SNR threshold, and environmental constants (a=9.61, b=0.16) are standard values used in UAV communication research, giving the results practical credibility.

**What to say to sir about it:** "The simulation uses real-world communication parameters, including standard 2.4 GHz frequency and a 25 dB SNR threshold that reflects minimum acceptable link quality for reliable data transmission. This makes the results directly relevant to real emergency network deployments."

---

### Figure 1: Disaster Scenario Illustration

**What it shows:** A visual overview of the disaster scenario — a damaged base station in the center, working BSs at the edges, UAVs forming multi-hop relay chains from users to the working BSs.

**Key takeaway:** The scenario is realistic — a large urban area, scattered survivors (UEs), multiple UAVs flying as relay nodes, and surviving BS infrastructure at the periphery.

**What to say to sir about it:** "Figure 1 shows the exact scenario this paper targets — a communication dead zone created by a disaster, where UAVs must form a multi-hop chain from survivors back to working base stations at the edge of the affected area."

---

### Figure 2: MRLMN System Architecture

**What it shows:** The architecture of the MRLMN framework — UAVs grouped into roles (Groups 1, 2, 3), each running its own independent PPO policy and critic network, with information aggregation flowing between them and individualized reward components feeding back to each agent.

**Key takeaway:** Every drone is autonomous but informed. The architecture is decentralized (no central controller) but cooperative (shared aggregated observations).

**What to say to sir about it:** "Figure 2 shows that each UAV has its own independent policy network, but they share aggregated observations to coordinate. The reward components at the bottom show how each drone receives both team-level and role-specific feedback."

---

### Figure 3: LLM Knowledge Distillation Pipeline

**What it shows:** The full pipeline from environment simplification to LLM querying to bipartite matching to distillation loss. The left side shows the prompt and chain-of-thought reasoning process; the right side shows how LLM outputs connect to MARL through matching and distillation.

**Key takeaway:** The LLM is a completely offline component — it reads a simplified description of the scenario, reasons through it step by step, suggests deployment positions, and those suggestions are converted into soft training signals for the drones. The LLM never controls a drone directly.

**What to say to sir about it:** "Figure 3 illustrates the key design decision: the LLM acts as an offline teacher, not a real-time controller. It analyzes the scenario using structured reasoning, suggests smart drone positions, and its suggestions are then distilled into the drone policies through a matching and loss mechanism. At deployment time, the LLM is not involved at all."

---

### Figure 4: Training Curves (10 Million Steps)

**What it shows:** The team reward (y-axis) over 10 million training steps (x-axis) for MRLMN (labeled "Ours") versus all 5 baselines. Shaded regions show standard deviation (variability across runs).

**Key takeaway:** MRLMN rises steeply and stabilizes above 0.8 with low variance. GVis is the best baseline but plateaus much lower. MAPPO and GA2C stabilize between 0.4 and 0.6. IA2C and MAA2C are the weakest and most variable.

**What to say to sir about it:** "Figure 4 is the core training result. MRLMN not only achieves a higher final reward — above 0.8 versus 0.4 to 0.6 for competing methods — but also converges faster and with less variance. The rapid early rise is specifically due to the LLM distillation module providing a useful starting direction for exploration."

---

### Figure 5: Scaling Performance (6 subplots)

**What it shows:** Six plots comparing MRLMN vs. GVis, GA2C, MAPPO across: (a) connected UE proportion vs. area size, (b) connected UE proportion vs. UAV count, (c) data rate vs. area size, (d) data rate vs. UAV count, (e) UAV availability vs. area size, (f) UAV availability vs. UAV count.

**Key takeaway:** MRLMN consistently leads on all three metrics across all conditions tested. The advantage is most pronounced in larger environments and with fewer UAVs — precisely the hardest conditions where scalability matters most.

**What to say to sir about it:** "Figure 5 is the scalability validation. It shows that MRLMN's advantage is not specific to one environment size or one drone count — it maintains leadership across the full range tested. This is important evidence that the method genuinely scales, rather than just being optimized for one configuration."

---

### Figure 6: Ablation Study (6 subplots)

**What it shows:** Same six-metric format as Figure 5, but comparing full MRLMN versus three ablated versions (NC, NL, NR) across area sizes and UAV counts.

**Key takeaway:** Every module contributes. The NR version (no reward decomposition) suffers the most on UE coverage and data rate. The NC version (no behavioral constraints) suffers the most on UAV availability. The NL version (no distillation) degrades consistently across all metrics.

**What to say to sir about it:** "Figure 6 is the ablation study that validates each component individually. Every module contributes to performance, and removing any single one causes a drop of at least 6% in UE coverage and 10% in data rate, proving that the three innovations work together as an integrated system."

---

### Figure 7: Policy Sharing Trade-off

**What it shows:** Three scatter plots where each point represents one training run. X-axis is training time in hours, Y-axis is performance (UE coverage, data rate, UAV availability), and point size reflects standard deviation. The number of trained policies is encoded in the point cluster.

**Key takeaway:** More policies = better performance but longer training. The relationship is consistent and monotonic across all three metrics.

**What to say to sir about it:** "Figure 7 shows that allowing each drone to maintain an independent policy (18 policies) produces the best results — 65% UE coverage versus 45% for full sharing — but requires twice the training time. This gives practitioners a clear trade-off to navigate based on their available compute budget."

---

### Figure 8: Simulation Snapshots (4 panels)

**What it shows:** Network topology at four time steps within one episode — t=1 (chaotic initial random positions), t=100 (chains beginning to form), t=200 (increasingly stable coverage), t=400 (robust multi-hop network with high UE connectivity). Evaluation metrics are shown under each panel.

**Key takeaway:** The network evolves organically as drones learn where to position themselves. At t=1, connected UE proportion is ~41%. By t=400, it reaches approximately 82–100%, with data rate improving from 4.48 Mbps to 10.14 Mbps.

**What to say to sir about it:** "Figure 8 shows the algorithm in action during a single episode. You can see the UAVs progressively organizing into a multi-hop relay chain — from chaotic initial positions to a stable, well-connected network that covers the majority of users by the end of the episode."

---

## Comparison with Prior Work

**Prior best results (baseline methods):**
- MAPPO: stabilizes at 0.4–0.6 reward; achieves approximately 50–60% UE coverage in standard environment
- GVis (best baseline): performs closest to MRLMN but still falls 20–30% short on UE coverage
- GA2C: comparable to GVis on some metrics, worse on others; both rely on GNN-based coordination
- IA2C and MAA2C: weakest baselines; non-cooperative or weakly cooperative approaches

**Where MRLMN wins:**
- All conditions tested — environment size, UAV count, all three metrics
- Most dramatically in large environments (14.44 km²) where the coordination challenge is hardest
- Particularly in data rate — 52% average improvement suggests MRLMN not only connects more users but positions drones in better relay positions for higher-quality links

**Where MRLMN falls short:**
- Training time: using GPT-4o during training and training 18 independent policies takes 40 hours. Baselines train faster.
- The paper does not compare against methods that use online LLM control (since it deliberately avoids this), so the comparison to the theoretical upper bound of "LLM-controlled drones at every step" is not shown.

---

## Real-World Meaning

If MRLMN were actually deployed in a disaster scenario:

**For rescue coordination:** Emergency teams would be able to deploy a drone swarm from a vehicle or aircraft, have the swarm self-organize within the first 100 time steps (roughly a few minutes at 30m/slot movement speed), and then maintain a stable communication network for the duration of the rescue operation without any human operator managing drone positions.

**For survivors:** Instead of being completely cut off, a survivor in the communication dead zone could send their GPS location, communicate with family, and receive instructions from rescue coordinators — all through the relay network the drones have collectively built.

**For scalability:** Because MRLMN is fully decentralized at deployment time (each drone runs only its lightweight MLP policy, no LLM needed), additional drones can be added to an ongoing operation without redesigning the system. This is a critical operational advantage in fast-evolving disaster scenarios where additional resources arrive incrementally.

**The broader impact:** The methods developed here — role-based multi-agent grouping, reward decomposition, and LLM-guided exploration — are general enough to apply to other multi-robot coordination problems beyond UAV networking, including warehouse robot coordination, autonomous vehicle platooning, and distributed sensor network management.
