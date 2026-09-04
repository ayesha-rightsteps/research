# 04 — Results: What They Found and Why It Matters

---

## Key Results

### Result 1: RALLY Achieves the Best Overall Performance Among All Baselines

RALLY attains the highest mean reward and the narrowest variance distribution across 30 test episodes, outperforming all three baselines: CIHRL (state-of-the-art MARL), CoNavGPT (pure LLM planner), and DITTO (LLM with fixed roles).

**What this means in practice:** RALLY completes the DS-CEFC mission more consistently and more reliably than any prior approach. The narrow variance means its good performance is not a fluke — it performs well across all 30 test episodes, not just a lucky few.

**Compared to prior work:**
- CIHRL is stable but conservative — it learns a safe policy that avoids collisions but is timid about covering targets, resulting in modest rewards
- CoNavGPT achieves higher rewards than CIHRL, confirming LLMs are powerful reasoners, but its rewards are more variable because it can get stuck in local optima without any online learning
- DITTO slightly outperforms CIHRL by using LLM-based role self-cognition, but its greedy role choices and lack of reinforcement feedback lead to high variance and unstable consensus
- RALLY beats all of them because it combines the strengths of both: the semantic reasoning of LLMs and the adaptive exploration of MARL

---

### Result 2: RALLY Converges Faster and More Accurately Than VDN

In the RMIX ablation (Figure 7), both RMIX and VDN converge during training, but RMIX converges faster and yields more accurate cumulative return estimates.

**What this means in practice:** The more sophisticated RMIX mixing architecture (two-layer MLP with ReLU-constrained weights) is genuinely better than the simpler linear VDN aggregation for role credit assignment. The theoretical monotonicity guarantee in RMIX translates into a measurable training improvement.

---

### Result 3: RALLY Generalizes to Larger Swarm Sizes Without Retraining ⭐ (Most Impressive Result)

When swarm size increases from the training size of 8 drones to 9, 10, and 11 drones, RALLY preserves high scoring ability throughout. CIHRL, by contrast, degrades substantially with each additional drone.

**What this means in practice:** Without retraining, CIHRL's drones fall into "habitual grouping" patterns — they repeatedly form the clusters they learned during training and cannot adapt to cover additional targets when the swarm grows. RALLY avoids this by encoding the maximum permitted formation size into its LLM prompt, which dynamically adjusts the consensus-formation strategy for any swarm size.

**Why this is the most impressive result:** In real deployments, you rarely know exactly how many drones will be available. A system that handles variable fleet sizes without retraining is enormously more practical. This result demonstrates that RALLY's LLM-based reasoning provides genuine generalization capability — not just pattern matching on a fixed configuration.

**Compared to prior work:** CIHRL requires retraining for every new swarm size, which is computationally expensive and operationally impractical. RALLY generalizes zero-shot to unseen sizes.

---

### Result 4: RALLY Generalizes Across Different Target Area Configurations

Testing on a 3x3 grid (original training configuration), a 2x4 grid, and a 4x2 grid shows no significant difference in RALLY's reward performance across all three layouts (Figure 10).

**What this means in practice:** The spatial arrangement of mission targets does not degrade RALLY's performance. This is significant because real-world mission environments are highly variable — targets can be arranged in any configuration, not the one the system trained on.

---

### Result 5: Three-Role Architecture is Optimal — Adding More Roles Hurts

The ablation study of role configurations (Figure 12) shows:
- **1 role (Executor only):** Lowest performance, mean reward approximately -3,000 — severe limitation because no task decomposition occurs
- **2 roles (Commander + Executor):** Higher mean reward but greatly enlarged variance — overreliance on Commander decisions causes instability
- **3 roles (Commander + Coordinator + Executor):** Best combination of high mean reward and low variance
- **4 roles (Commander + Coordinator + Executor + Decoy):** Reduced average reward and inflated variance — too much coordination overhead

**What this means in practice:** Role design is not "more is better." The Coordinator role is the critical addition — it mediates between the Commander's individual-focused strategy and the Executor's obedient execution, providing the right balance of exploration and consistency. Adding a fourth Decoy role creates more coordination overhead than it saves in evasion benefit.

---

### Result 6: Fine-Tuned Qwen2.5-1.5B Achieves Practical Deployment

After LoRA fine-tuning on the 8,231-sample filtered dataset:
- The base Qwen2.5-7B without fine-tuning performs markedly worse
- Direct GPT-4o API calls introduce significant latency and instability
- RALLY with fine-tuned Qwen2.5-7B achieves the best performance among fine-tuned models
- Qwen2.5-1.5B achieves a near-comparable balance of performance and efficiency

From Table 3:

| Model | Avg. Inference Time (s) | Memory Footprint (GB) | Runtime Overhead (GB) |
|---|---|---|---|
| Qwen2.5-7B | 15.39 | 15 | 15.7 |
| Qwen2.5-3B | 17.63 | 5.8 | 7.17 |
| Qwen2.5-1.5B | 14.48 | 2.9 | 4.13 |
| Qwen2.5-0.5B | 15.45 | 1.2 | 1.77 |

**What this means in practice:** The 1.5B model is the practical sweet spot — smaller than 3B and 7B but significantly more capable than 0.5B. At 2.9 GB memory and 14.48 seconds inference time, it can realistically run on modern onboard UAV compute hardware.

---

### Result 7: SITL Validation Confirms Real-World Viability

The SITL experiments (Figure 16) show RALLY successfully orchestrating a UAV swarm through four representative phases in one episode:
- **Step 17:** UAV #2 (closest to target, farthest from enemy) assumes Commander and leads the swarm to Target #2
- **Step 39:** Enemy approach forces dynamic reorganization — the swarm splits into two sub-formations (F3 and F5) with new Commander and Coordinator assignments
- **Step 43:** UAV #7 acts as Coordinator, deliberately positioning between enemy and cluster to divert pursuit, allowing peers to reorient
- **Step 62:** Both sub-clusters successfully evade the enemy and complete coverage

**What this means in practice:** RALLY's role-adaptive behavior emerges organically during the mission — drones do not follow a pre-programmed script but genuinely adapt to changing threats and opportunities.

---

## Tables and Figures Explained

### Figure 6: Overall Performance Comparison (Box Plot)
**What it shows:** Reward distributions (box plots) across 30 test episodes for RALLY and the three baselines (CIHRL, CoNavGPT, DITTO).
**Key takeaway:** RALLY's box is positioned highest (least negative reward) and has the narrowest spread, indicating both superior average performance and superior consistency.
**What to say to sir about it:** "Figure 6 shows RALLY achieves the highest mean reward and narrowest variance distribution among all compared methods. The narrow box indicates RALLY consistently completes the DS-CEFC task across episodes, while baselines like DITTO have wide variance, showing they work sometimes but fail unpredictably."

---

### Figure 7: RMIX vs. VDN Training Convergence
**What it shows:** Loss curves during RMIX-based role training, comparing the RMIX mixing network against the simpler VDN aggregation.
**Key takeaway:** RMIX converges faster and to a lower final loss than VDN, validating the design choice.
**What to say to sir about it:** "Figure 7 demonstrates that the RMIX mixing architecture converges faster and more accurately than VDN. This confirms that the monotonically constrained two-layer MLP provides better role credit assignment than simple linear value summation."

---

### Figure 8: Qwen2.5-7B Fine-Tuning Loss Curve
**What it shows:** The training and validation loss during LoRA fine-tuning of Qwen2.5-7B.
**Key takeaway:** Loss consistently decreases; validation convergence achieved around step 500, indicating successful knowledge transfer from GPT-4o.
**What to say to sir about it:** "Figure 8 shows the LoRA fine-tuning of Qwen2.5-7B converges successfully, with validation loss stabilizing around step 500. This confirms that GPT-4o's DS-CEFC reasoning capability can be effectively transferred to the smaller model."

---

### Figure 9: Generalization to Varying Swarm Sizes
**What it shows:** Box plots comparing RALLY and CIHRL performance as swarm size increases from 8 to 11 drones.
**Key takeaway:** RALLY maintains consistent performance across all sizes; CIHRL degrades significantly at 9, 10, and 11 drones.
**What to say to sir about it:** "Figure 9 is perhaps the most practically significant result — RALLY generalizes to unseen swarm sizes zero-shot while CIHRL's performance collapses beyond its training configuration. RALLY achieves this by encoding formation constraints in its LLM prompts, allowing dynamic consensus adjustment without retraining."

---

### Figure 10: Generalization to Varying Target Configurations
**What it shows:** RALLY's reward distributions across three different target area layouts: 2x4 grid, the original 3x3 grid, and 4x2 grid.
**Key takeaway:** No significant difference in performance across configurations, demonstrating spatial robustness.
**What to say to sir about it:** "Figure 10 shows RALLY maintains consistent performance regardless of how target regions are spatially arranged — 2x4 and 4x2 layouts perform comparably to the training 3x3 configuration. This validates that RALLY's LLM-based reasoning adapts to different mission geometries."

---

### Figure 11: Two-Phase Decision-Making by Agent #6
**What it shows:** A side-by-side comparison of Agent #6's Stage 1 (intention) reasoning and Stage 2 (consensus) reasoning text, demonstrating how the Coordinator role changes the agent's decision.
**Key takeaway:** In Stage 1, Agent #6 greedily chose the Commander role and target (-8,8) based purely on personal scoring. After RMIX overrode the role to Coordinator and Stage 2 consensus incorporated neighbor information, the agent maintained the same target but with a more team-oriented justification — demonstrating role correction without losing the good initial target.
**What to say to sir about it:** "Figure 11 provides a transparent window into RALLY's reasoning. It shows how RMIX corrects the LLM's tendency to greedily self-assign the Commander role, and how Stage 2 consensus integrates neighbor information to produce more coordinated decisions while preserving the LLM's strong initial target selection."

---

### Figure 12: Impact of Role Number (Ablation)
**What it shows:** Box plots of reward distributions for RALLY with 1, 2, 3, and 4 role configurations.
**Key takeaway:** Three roles (Commander-Coordinator-Executor) achieves the best combination of high mean reward and low variance. Four roles hurts performance.
**What to say to sir about it:** "Figure 12 shows a non-monotonic relationship between role count and performance — more roles do not automatically mean better performance. The three-role configuration is optimal because the Coordinator role mediates between individual optimization and team coordination, while adding a Decoy role introduces coordination overhead that outweighs its evasion benefit."

---

### Figure 13: Model Fine-Tuning Performance Comparison
**What it shows:** Reward curves over training epochs for three approaches: non-fine-tuned Qwen2.5-7B base model, direct API-GPT-4o calls, and RALLY with fine-tuned Qwen2.5-7B.
**Key takeaway:** The non-fine-tuned base model performs poorly; direct GPT-4o API suffers from latency instability; fine-tuned RALLY achieves the best reward.
**What to say to sir about it:** "Figure 13 validates the necessity of fine-tuning. Without fine-tuning, the smaller model lacks the task-specific reasoning needed for DS-CEFC navigation. With fine-tuning, RALLY achieves performance comparable to the much larger GPT-4o while being deployable locally on onboard hardware."

---

### Figure 14: Impact of Model Parameter Scale
**What it shows:** Performance after fine-tuning Qwen2.5 models of different sizes (0.5B, 1.5B, 3B, 7B) on the DS-CEFC task.
**Key takeaway:** All fine-tuned models show substantial performance gains over their base counterparts. The 1.5B and 7B models strike the best balance; 0.5B is too small for high-quality reasoning.
**What to say to sir about it:** "Figure 14 demonstrates that even very small models (1.5B parameters) can achieve strong performance after fine-tuning on domain-specific data — supporting RALLY's claim of practical edge deployment."

---

### Table 1: Notation Table
**What it shows:** All mathematical symbols used in the paper with their descriptions.
**What to say to sir about it:** "Table 1 is the paper's notation reference, defining key variables like oi^t for local observation, ki^t for role assignment, and gt^i for consensus goal, which appear throughout the algorithm formulations."

---

### Table 2: Environmental and Reward Parameter Configurations
**What it shows:** The specific numerical values used in all experiments — number of UAVs (8-11), velocity ranges, reward weights, training hyperparameters.
**What to say to sir about it:** "Table 2 provides full experimental reproducibility — all environment parameters, reward weights (formation:15, navigation:4, completion:10, interference:-100, collision:-100), and training hyperparameters are specified. This transparency is important for scientific rigor."

---

### Table 3: LLM Running Performance on NVIDIA RTX 4090
**What it shows:** Average Inference Time, Memory Footprint, and Runtime Overhead for Qwen2.5 models at four parameter scales.
**What to say to sir about it:** "Table 3 makes a practical case for the 1.5B model — at 2.9 GB memory and 14.48 seconds inference time, it is the only model that realistically fits on modern onboard UAV GPUs while still delivering adequate reasoning quality, validated by the performance results in Figure 14."

---

### Figure 15: Gazebo SITL Task Overview
**What it shows:** The architecture of the SITL simulation platform — RALLY module, ROS communication nodes, PX4 autopilot, Gazebo physics simulator, and their interconnections.
**What to say to sir about it:** "Figure 15 shows the complete software architecture of the SITL validation setup. Each UAV runs an independent Python controller that interfaces with RALLY via ROS, sends navigation commands to PX4, and receives physics simulation feedback from Gazebo — creating a closed-loop system that mirrors real UAV operation."

---

### Figure 16: Four SITL Cooperation Scenarios
**What it shows:** Four snapshots of the SITL simulation at decision steps 17, 39, 43, and 62, showing UAV trajectories, role assignments, and formation evolution.
**What to say to sir about it:** "Figure 16 provides visual confirmation that RALLY's dynamic role adaptation works in a realistic simulation. At step 39, the approaching enemy triggers an autonomous swarm split into two sub-formations with new Commander assignments — behavior that emerges from RALLY's reasoning without any pre-programmed split rule."

---

## Comparison with Prior Work

| Method | Type | Role Assignment | Online Learning | Generalization to New Sizes |
|---|---|---|---|---|
| CIHRL [2] | Pure MARL | None (homogeneous) | Yes | Poor |
| CoNavGPT [30] | Pure LLM | None | No | Good but local optima |
| DITTO [51] | LLM + fixed roles | Fixed, self-assigned | No | Moderate |
| **RALLY** | LLM + MARL | Dynamic (RMIX) | Yes | Excellent |

RALLY beats CIHRL on task completion and generalization; beats CoNavGPT on stability and adaptive exploration; beats DITTO on variance and consistent consensus.

---

## Real-World Meaning

If RALLY were deployed in real operations:

- **Disaster response:** A fleet of search drones sent to an earthquake zone could autonomously assign Commanders to lead formation coverage of survivor areas, Coordinators to balance team coverage efficiency, and Executors to reliably execute search patterns — all while evading debris or hostile interference — without any human dispatching roles manually.

- **Variable team sizes:** If two drones are damaged and drop out of the mission, the remaining drones could automatically reorganize into smaller formations and continue covering targets at an adjusted scale. No human reprogramming needed.

- **Edge deployment:** With the 1.5B model running on onboard GPUs, the drones do not need internet connectivity or cloud inference during the mission — critical for denied-communication environments like urban warfare or remote disaster zones.

- **Interpretability:** Unlike black-box MARL, a human operator can actually read the drones' LLM reasoning to understand why they made each decision, enabling human oversight and trust in autonomous systems.
