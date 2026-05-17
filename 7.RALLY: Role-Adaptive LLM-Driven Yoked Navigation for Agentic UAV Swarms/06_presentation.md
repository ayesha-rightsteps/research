# 06 — Presentation Guide: Your Complete Script and Q&A Prep

This is the most important file. Read it out loud at least once before you present.

---

## Suggested Opening (Word for Word)

> "Good morning, sir. Today I'd like to present a paper titled 'RALLY: Role-Adaptive LLM-Driven Yoked Navigation for Agentic UAV Swarms,' by Ziyao Wang, Rongpeng Li, Sizhao Li, Yuming Xiang, Haiping Wang, Zhifeng Zhao, and Honggang Zhang, published in the IEEE Open Journal of Vehicular Technology in 2025.
>
> This paper addresses the problem of controlling a swarm of drones that must cover multiple target areas while evading an adversary and avoiding obstacles — without any centralized controller. The authors propose RALLY, a hybrid framework that combines Large Language Model reasoning with Multi-Agent Reinforcement Learning, giving each drone the ability to reason in natural language and dynamically adapt its role within the team. Their experiments show that RALLY outperforms all existing approaches on task coverage, convergence speed, and generalization to new environments."

---

## Main Points to Cover (in order)

### 1. THE PROBLEM

**Say:**
"The specific task this paper addresses is called DS-CEFC — Dynamic Swarm coordination with Cooperative Evasion and Formation Coverage. Imagine eight drones that must fly to multiple target areas in formations of at least three, while simultaneously evading a pursuer drone that actively chases them and avoiding static obstacles in the environment. Crucially, each drone can only see what is within three meters of itself — there is no global map and no central commander. The challenge is getting the swarm to coordinate effectively under these constraints."

---

### 2. WHY EXISTING SOLUTIONS WERE NOT ENOUGH

**Say:**
"Two main families of approaches have been tried. Traditional Multi-Agent Reinforcement Learning methods — like QMIX and MADDPG — learn coordination through experience but communicate using raw numerical vectors that carry no semantic meaning. Their roles are rigidly fixed, so they fail badly when the team size or environment changes. On the other hand, LLM-based planners like CoNavGPT reason very well using prior knowledge, but they cannot learn from the actual deployment environment, so they get stuck in local optima and cannot adapt to the specific dynamics of the scenario. What is needed is a system that has both — semantic reasoning and real-world adaptation."

---

### 3. THE PROPOSED APPROACH

**Say:**
"RALLY addresses this by combining two core modules. The first is a two-stage LLM-based semantic consensus process. In Stage 1, each drone independently uses an LLM to reason about its local situation in natural language and generates an initial navigation intention — essentially choosing which target to fly toward. In Stage 2, after communicating with nearby drones, the LLM refines that intention using neighbors' goals and roles to reach a collective consensus. The second module is RMIX — a Role-value Mixing Network — which dynamically assigns each drone one of three roles: Commander, Coordinator, or Executor. These roles define how the drone weighs its own interests versus the team's, and they change every 50 timesteps as the situation evolves."

---

### 4. KEY METHODOLOGY

**Say:**
"What makes RMIX special is how it is trained. A direct exploration of all possible role combinations would be impractical — with 8 drones and 3 roles each, that is over six thousand combinations. So the authors use a clever two-phase approach. First, they call GPT-4o via API to suggest roles for each drone across many simulated episodes and store these suggestions as offline training data — this seeds the learning with sensible starting knowledge. Then, the RMIX network trains online using reinforcement learning, continuously refining role assignments based on real environment feedback. For deployment, GPT-4o is replaced by a smaller fine-tuned Qwen2.5-1.5B model — compressed to under 3 gigabytes — that runs locally on onboard UAV hardware without needing internet access."

---

### 5. THE RESULTS

**Say:**
"RALLY achieves the highest mean reward and narrowest variance across all baselines in 30 test episodes in the Multi-Agent Particle Environment. More impressively, when the swarm size is increased from 8 to 9, 10, and 11 drones — without any retraining — RALLY maintains high performance while the best MARL baseline, CIHRL, degrades substantially. RALLY also generalizes across three different target area configurations without performance drops. An ablation study confirms that the three-role design is optimal — both fewer roles and more roles reduce performance. And the full system was validated in a high-fidelity Gazebo-ROS-PX4 simulation with real autopilot firmware, where RALLY successfully orchestrated dynamic formation splitting, role switching, and enemy evasion across a complete mission episode."

---

### 6. SIGNIFICANCE AND CONTRIBUTION

**Say:**
"The core contribution of RALLY is demonstrating that dynamic role heterogeneity — where each drone's role adapts in real time based on learned credit assignment — fundamentally improves swarm coordination over both static-role LLM systems and role-free MARL systems. The framework is also practically significant because it provides a full deployment pipeline: from GPT-4o quality data generation, through LoRA fine-tuning, down to an onboard-deployable 1.5-billion-parameter model. This makes RALLY one of the few LLM-based UAV swarm systems that is genuinely closer to real-world deployment than just a simulation proof-of-concept."

---

## Anticipated Questions and Model Answers

| Question Sir Might Ask | What Ayesha Should Say |
|---|---|
| **What is the main contribution of this paper?** | "The main contribution is RALLY itself — a hybrid framework that is the first to use a Role-value Mixing Network trained with offline LLM priors to dynamically assign heterogeneous roles to drones. Combined with a two-stage LLM consensus process, this enables the swarm to reason semantically and adapt its coordination strategy in real time. The result is that RALLY outperforms all baselines on task coverage, convergence, and generalization — especially to larger swarm sizes that MARL alone cannot handle without retraining." |
| **What makes this approach different from previous work?** | "There are three key differences. First, roles are dynamic — unlike DITTO or other LLM systems with fixed role definitions, RALLY's RMIX reassigns roles every decision step based on the current situation. Second, the role learning is seeded with LLM offline data — this is more sample-efficient than random exploration in a 6,561-dimensional joint role space. Third, RALLY provides a full deployment path — the LLM is compressed to a 1.5B model that runs locally on UAV hardware, unlike prior work that depends on cloud API calls." |
| **What are the limitations of this work?** | "The authors acknowledge three main limitations: LLM inference latency of about 14 seconds per decision is a concern for fast-moving scenarios; the LLM has no historical memory and reasons from scratch each step; and CoT reasoning can converge to local optima. I would also add that the SITL validation is only qualitative — there is no controlled comparison of RALLY versus baselines in the high-fidelity simulator. And all experiments use only one adversary, so robustness against multiple adversaries is untested." |
| **What evaluation metric did they use? Is it appropriate?** | "The primary metric is average reward per episode, averaged over 30 test episodes. The reward is a weighted sum of five components: formation quality, navigation progress, mission completion, interference penalty, and collision penalty — with weights of 15, 4, 10, minus 100, and minus 100 respectively. The metric is appropriate because it captures the multi-objective nature of DS-CEFC — covering targets, maintaining formations, and avoiding collisions all matter simultaneously. The large negative weights on penalties mean rewards are typically negative, so better performance means less-negative values." |
| **What dataset was used and why?** | "There is no real-world dataset. The paper uses two simulation environments. The Multi-Agent Particle Environment is a standard 2D particle simulator used for controlled experiments. For the fine-tuning of the local LLM, the authors call GPT-4o via API to generate 8,231 high-quality navigation decisions in the DS-CEFC scenario, filtered for output validity and reward quality. This approach is justified because DS-CEFC is a novel task with no existing real-world dataset, and using GPT-4o as a high-quality data generator is a principled form of knowledge distillation." |
| **Could this approach be applied to a related problem?** | "Yes, RALLY's framework is general enough for any multi-robot task where agents need to coordinate on goals under partial observability. Search-and-rescue operations, where robots need to cover an area while avoiding hazards, are a natural extension. Autonomous vehicle platooning is another — vehicles could use LLM reasoning to negotiate lane positions and following distances while RMIX assigns lead or follower roles. The main requirements are that natural language can describe the agents' observations meaningfully and that roles can be defined to encode different coordination priorities." |
| **What would you change if you were the author?** | "I would add quantitative SITL experiments comparing RALLY against baselines in the high-fidelity simulator, not just a qualitative demonstration. The current paper shows RALLY works in SITL but doesn't show it's better than baselines in that setting. I would also test with multiple adversaries to evaluate robustness, and I'd include a communication failure ablation — showing how RALLY degrades when the neighborhood communication required by Stage 2 is disrupted — since real deployments will have unreliable links." |
| **What future work do the authors suggest?** | "The authors identify four future directions. First, optimizing the lightweight LLM for faster inference and lower communication latency. Second, addressing local optima in CoT reasoning through test-time training and diversifying reasoning paths. Third, investigating multimodal fusion — incorporating visual or sensor data beyond positional observations. Fourth, developing theoretical guarantees for rapid semantic consensus in larger UAV swarms. I think the most impactful of these would be real hardware validation, which the authors do not explicitly mention but is the natural next step after SITL." |
| **Do you find the results convincing? Why?** | "Mostly yes. The performance comparison in MPE is statistically rigorous — 30 test episodes with box plots showing variance. The generalization results are particularly convincing because the swarm size experiments test a concrete, practically important property: does the system work without retraining? And RALLY passes while CIHRL fails. What I find less convincing is the SITL validation being only qualitative. A boxplot of RALLY versus CIHRL rewards in SITL would significantly strengthen the claim of real-world readiness. The results are compelling enough to take seriously, but would benefit from a hardware experiment." |
| **How does this compare to CoNavGPT?** | "CoNavGPT uses an LLM as a global planner — it reasons about the entire scene and outputs navigation goals without any training. It performs better than pure MARL like CIHRL, confirming LLMs are powerful planners. But CoNavGPT has no online learning, so it can get stuck in suboptimal solutions and has no mechanism to improve from experience in the actual deployment environment. RALLY adds two things CoNavGPT lacks: RMIX-based role learning that adapts to the specific environment dynamics, and the two-stage consensus that incorporates neighborhood communication. The result is that RALLY achieves both higher mean reward and lower variance than CoNavGPT in experiments." |

---

## What NOT to Say

1. **Do not say "RALLY is perfect"** — it has real limitations (14-second inference latency, no historical memory, only qualitative SITL validation). Acknowledging these will impress your professor far more than overselling the paper.

2. **Do not say "the LLM understands the environment"** — more precisely, the LLM uses its pre-trained language understanding to reason about structured natural language descriptions of the environment. It does not "perceive" the environment directly.

3. **Do not confuse RMIX with QMIX** — RMIX is inspired by QMIX but specifically adapted for role selection (choosing among Commander/Coordinator/Executor), not for general action selection as in QMIX.

4. **Do not say "the results prove RALLY works in the real world"** — the SITL validation is encouraging but SITL is still a simulator. No actual physical hardware flight tests are reported.

5. **Do not say the reward values are "scores out of some maximum"** — the rewards are negative numbers (typically between -1000 and -6000) because large collision and interference penalties dominate. Better performance = less negative reward, not a positive score.

---

## Closing Statement

> "In summary, RALLY makes a meaningful advance in intelligent UAV swarm control by showing that dynamic LLM-driven role assignment, grounded by reinforcement learning credit mechanisms, produces a system that is more capable, more generalizable, and more deployable than either LLMs or reinforcement learning alone. Thank you, sir."

---

## If You Forget Something

If you blank on a specific number or detail, you can say:

> "The paper reports specific figures on this — the key point is that RALLY outperforms all baselines on this metric, and I can confirm the exact numbers from the paper if needed."

For any equation or algorithm detail:

> "The precise formulation uses a monotonically constrained mixing network, but the intuition is that it ensures each drone's role improvement cannot hurt the team — which is the key mathematical guarantee that makes the whole credit-assignment mechanism work."
