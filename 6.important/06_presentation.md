# 06 — Presentation Guide: Script and Q&A

This file is your complete guide for the day you present. Read it the night before and again in the morning.

---

## Suggested Opening (Word for Word)

> "Good morning, sir. Today I'd like to present a paper titled 'Scalable UAV Multi-Hop Networking via Multi-Agent Reinforcement Learning with Large Language Models' by Yanggang Xu, Jirong Zha, and colleagues from Tsinghua University, published in 2025 and available on arXiv.
>
> This paper addresses the problem of restoring communication in disaster zones where ground infrastructure has been destroyed. The authors propose MRLMN — a framework that trains a swarm of drones to collectively form a wireless relay network, guided by a large language model during training. The results show up to 52% higher data rates and 27% more user coverage compared to the current best methods."

---

## Main Points to Cover (In Order)

---

**1. THE PROBLEM**

Say: "When disasters like earthquakes or floods strike, the first thing that goes down is the communication infrastructure — base stations, fiber-optic cables, everything. And without communication, rescue teams can't coordinate, and survivors can't call for help. In 2024 alone, 27 climate disasters in the US caused 184 billion dollars in losses — and communication failure was a major factor in each. Drones can be deployed quickly to act as relay stations, but organizing a swarm of 18 or more drones to collectively form a reliable multi-hop relay network — where each drone passes signals to the next — is an extremely hard coordination problem."

---

**2. WHY EXISTING SOLUTIONS WEREN'T ENOUGH**

Say: "Traditional optimization approaches are too slow for real-time dynamic environments. Existing reinforcement learning methods hit a scalability wall as drone count increases — the state space and action space explode exponentially. And another critical problem is the cold start issue: in early RL training, drones make random moves and almost never stumble onto a working network configuration, so they get almost no feedback to learn from. This makes training very slow and prone to getting stuck in bad local solutions."

---

**3. THE PROPOSED APPROACH**

Say: "The authors propose MRLMN, which stands for Multi-agent Reinforcement Learning with Large Language Model in Multi-hop Networking. The core idea is to train each drone using an independent reinforcement learning algorithm called IPPO, but to make three important additions. First, drones are grouped by their role — some act as relay nodes close to base stations, others serve users near the disaster area — and each group gets a customized reward signal tailored to its specific job. Second, a special training constraint keeps the gateway drones — the ones closest to base stations — from accidentally disconnecting, which would break the entire relay chain. Third, and most innovatively, GPT-4o is used as an offline teacher: it analyzes a simplified description of the disaster scenario and suggests smart deployment positions for the drones. These suggestions are then distilled into the drone policies through a mathematical loss function. Critically, once the drones are trained, they operate completely independently — no LLM is needed at runtime."

---

**4. KEY METHODOLOGY**

Say: "Let me walk through how the LLM distillation actually works, because this is the most novel part. The environment is simplified into a grid — for example, an 8-by-8 grid showing how many users are in each cell. This grid is described in natural language and given to GPT-4o along with instructions to reason through the deployment in three steps: first, identify where users are concentrated; second, check for connectivity gaps; third, finalize the deployment. The LLM then outputs suggested positions for all drones. A rule-based verifier checks that these positions form a valid connected network. Then, the Hungarian algorithm — an optimal assignment method — matches each LLM-suggested position to the nearest actual drone. This gives each drone an expected direction to move. A cross-entropy loss function then trains the drone's policy to be more likely to choose that direction. This is knowledge distillation — transferring the LLM's strategic reasoning into the drone's neural network policy."

---

**5. THE RESULTS**

Say: "The results are convincing across three key metrics: connected UE proportion — what percentage of survivors are connected; average data rate — how fast their connection is; and available UAV ratio — what fraction of drones are successfully relaying. Across all conditions tested, MRLMN outperforms five baselines including MAPPO, which is considered a strong multi-agent RL method. Specifically: 27% more users are connected on average as environment size increases; the average data rate is 52% higher as the drone count scales from 12 to 24; and the training reward stabilizes above 0.8 while all baselines plateau at 0.4 to 0.6. The ablation study confirmed that removing any single module — the reward decomposition, the LLM distillation, or the behavioral constraints — causes at least a 6% drop in coverage and a 10% drop in data rate."

---

**6. SIGNIFICANCE AND CONTRIBUTION**

Say: "This paper makes three practical contributions. First, it shows that large language models can be used as strategic teachers for multi-agent RL systems, even in highly technical domains like wireless networking — without requiring the LLM to be present at deployment time. Second, the role-based grouping strategy is a general approach to scalable multi-agent coordination that could apply beyond UAVs. Third, it demonstrates that combining these components produces an integrated system that is qualitatively better than any component alone. The directions for future work are clear and important: adding energy constraints, testing on physical hardware, and supporting dynamic environments where base stations might also fail."

---

## Anticipated Questions and Model Answers

| Question Sir Might Ask | What Ayesha Should Say |
|---|---|
| **What is the main contribution of this paper?** | "The main contribution is the MRLMN framework, which is the first to combine role-based multi-agent reinforcement learning with knowledge distillation from a large language model for UAV multi-hop networking. The LLM solves the cold-start problem in MARL training by providing strategic guidance from day one — something previous RL methods couldn't do. The result is 27% more user coverage and 52% higher data rates than existing methods like MAPPO and graph neural network approaches." |
| **What makes this approach different from previous work?** | "Previous MARL approaches for UAV networking either use a global reward signal that makes it hard for individual drones to understand their specific contribution, or they use graph neural networks that are computationally expensive. MRLMN's key differentiator is threefold: it decomposes the reward by role so each drone gets targeted feedback; it uses an LLM offline during training to guide exploration — which no prior work did for this specific problem; and it applies behavioral constraints asymmetrically — only to the critical gateway drones — rather than restricting all drones equally." |
| **What are the limitations of this work?** | "The biggest limitation I see is that everything is validated in simulation — there's no real hardware testing. Real drones face GPS errors, wind, and hardware variability that simulations cannot capture. A second limitation is that energy consumption is completely ignored in the reward function, which matters a lot in practice since drone batteries last only 20 to 40 minutes. The authors themselves acknowledge both of these and list them as future work. I'd also add that using GPT-4o as the teacher model raises reproducibility concerns since it's a paid, proprietary API." |
| **What evaluation metrics did they use? Are they appropriate?** | "They use three metrics: connected UE proportion, which measures what fraction of users are connected; average data rate per user in Mbps, which measures connection quality; and available UAV ratio, which measures network stability by tracking what fraction of drones remain connected to the relay chain. I think these are well-chosen and appropriate. The first two directly measure what matters for disaster survivors, and the third measures robustness, which is critical for a relay network where one drone dropping out can break all downstream connections." |
| **What dataset was used and why?** | "This paper doesn't use a traditional dataset — it uses a custom simulation environment. The environment is a 3.5 km by 3.5 km area with 150 users distributed following either a uniform pattern or a Gaussian mixture model, which simulates how people cluster in real disaster scenarios. The BSs are placed at three corners, specifically positioned so that no user can connect directly, forcing genuine multi-hop behavior. The communication parameters — 2.4 GHz frequency, 25 dB SNR threshold — are taken from standard UAV communication modeling literature, which gives the results real-world credibility." |
| **Could this approach be applied to other problems?** | "Yes, I think the core ideas generalize quite well. The LLM-guided knowledge distillation technique could be applied to any multi-agent RL problem where high-level strategic reasoning from an LLM could guide early exploration — for example, multi-robot warehouse coordination or traffic signal control with multiple intersections. The role-based grouping and reward decomposition approach applies to any heterogeneous multi-agent system where different agents have different responsibilities. The specific communication model and behavioral constraints are UAV-specific, but the framework's architecture is general." |
| **What would you change if you were the author?** | "I would add a real-world hardware experiment, even a small-scale one with three or four drones in a parking lot. I would also add UAV energy consumption to the reward function, since ignoring battery life makes the system impractical. And I would experiment with using an open-source LLM like LLaMA or Mistral as the teacher instead of GPT-4o, to test whether a freely available model provides comparable guidance quality — this would make the framework accessible to researchers without API budgets." |
| **What future work do the authors suggest?** | "The authors identify four directions. First, adding practical operational constraints including energy consumption, network load balancing, and UAV replacement when batteries die. Second, improving communication reliability through interference management and physical-layer optimization — since the paper currently assumes fixed bandwidth allocation with no interference. Third, deeper LLM integration — for example, replacing the conventional neural network policies with more expressive LLM-based decision models. Fourth, validation in real-world deployments, which would reveal practical feasibility and help close the gap between simulation and physical operation." |
| **Do you find the results convincing? Why?** | "Mostly yes. The results are convincing because they are tested across multiple conditions — five different environment sizes and five different UAV counts — and the advantage holds consistently. The ablation study is particularly convincing because it isolates each component's contribution, which rules out the possibility that only one module is doing all the work. What I find slightly less convincing is that the entire evaluation is simulation-only. The 52% data rate improvement is impressive, but I would want to see at least a small physical experiment before fully trusting that number in a real disaster deployment." |
| **How does MRLMN compare to MAPPO specifically?** | "MAPPO is a strong cooperative MARL baseline that uses a centralized value function during training. The key difference is that MAPPO gives all agents the same centralized value estimate, which doesn't distinguish individual contributions well. MRLMN, by contrast, gives each drone a role-specific reward that clearly tells it how well it is performing its specific job — relay or coverage. Additionally, MRLMN starts training with LLM guidance while MAPPO starts from random initialization. In the results, MAPPO stabilizes at a training reward of around 0.4 to 0.6 while MRLMN reaches above 0.8 — a gap of roughly 30 to 40 percentage points, which is substantial." |

---

## What NOT to Say

1. **Don't say "the LLM controls the drones in real time."** This is incorrect and a common misunderstanding. The LLM is only used during offline training. At deployment, drones run their learned MLP policies with zero LLM involvement. If sir asks about this, be specific.

2. **Don't say the results are from "real drones" or "real experiments."** Everything is simulation. The paper is clear about this. Claiming otherwise would be factually wrong.

3. **Don't say MRLMN "solves" the UAV networking problem.** It significantly outperforms existing baselines in simulation. Practical challenges — energy, hardware, real interference — remain unaddressed.

4. **Don't oversimplify the LLM role to "it just tells drones where to go."** The LLM suggests positions, which are matched to drones via the Hungarian algorithm, converted to soft probability distributions, and used as a training signal — not direct commands. The mechanism is subtle and that subtlety is part of the contribution.

5. **Don't confuse MRLMN with MAPPO.** MAPPO is one of the five baselines that MRLMN is compared against and outperforms. MRLMN's base algorithm is IPPO (Independent PPO), which is different.

---

## Closing Statement

> "In summary, MRLMN is a well-designed framework that addresses a real and urgent problem — emergency communication after disasters — with a novel combination of structured multi-agent learning and large language model guidance. The results are significant across multiple scales, and the ablation study validates each component. I believe the most impactful next step would be a real-world hardware demonstration. Thank you, sir — I'm happy to answer any further questions."

---

## If You Forget Something

If you blank on a specific number or detail, you can always say:

> "The paper specifies that number — let me recall the exact figure, but the key point is that MRLMN consistently outperformed all five baselines across every metric tested, with the most significant gains in data rate at around 52% improvement."

This is honest, confident, and shows you understand the paper even if you can't recall every specific digit under pressure.
