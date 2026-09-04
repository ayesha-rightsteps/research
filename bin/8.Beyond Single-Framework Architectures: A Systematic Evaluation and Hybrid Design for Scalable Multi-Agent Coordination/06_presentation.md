# 06 — Presentation Guide: Your Complete Script and Q&A

---

## Suggested Opening (Word for Word)

> "Good morning / good afternoon, sir. Today I'd like to present a paper titled 'Beyond Single-Framework Architectures: A Systematic Evaluation and Hybrid Design for Scalable Multi-Agent Coordination,' by Muhammad Saleem Khan and colleagues from COMSATS University Islamabad, published in IEEE Access in 2026.
>
> This paper addresses the problem of how to choose and design coordination frameworks for large teams of AI agents working on complex real-world tasks. The authors systematically compare three major frameworks — CrewAI, AutoGen, and LangChain — and then propose a novel hybrid architecture that combines the best of these frameworks. Their hybrid system achieves a 96.1% task success rate while reducing computational costs by over 76% compared to any single framework alone."

---

## Main Points to Cover (in order)

**1. THE PROBLEM**

Say: "When building large-scale AI agent teams — for example, coordinating drones, firefighters, bulldozers, and helicopters to respond to a wildfire — engineers must choose a software framework to manage how agents communicate and coordinate. Three frameworks dominate: CrewAI, AutoGen, and LangChain. But no one had actually compared them systematically under identical, realistic conditions. People were picking frameworks based on familiarity or convenience, which led to unpredictable performance and unexpected costs. The paper calls this a significant gap in the field."

---

**2. WHY EXISTING SOLUTIONS WEREN'T ENOUGH**

Say: "Existing benchmarks for testing multi-agent systems were either too small — fewer than 10 agents — or too simple, lacking the agent diversity and unpredictability of real emergencies. Prior evaluations looked at individual frameworks in isolation, never side-by-side. And initial assessments on the CREW-WILDFIRE benchmark showed that even sophisticated multi-agent systems like COELA and HMAS-2 sometimes failed to outperform passive baselines on complex tasks, which tells you the field really needed better architectures and better analysis tools."

---

**3. THE PROPOSED APPROACH**

Say: "The authors did two things. First, they built a standardized testing setup — identical perception and execution modules for all frameworks — and ran all three head-to-head on CREW-WILDFIRE, a wildfire simulation with 17 task levels, 100-plus agents, and maps of up to one million cells. They measured performance across seven behavioral dimensions, not just a single score. Second, using what they learned from that comparison, they designed a hybrid architecture called LangGraph-CrewAI Hybrid. The key insight is simple: not every decision in a complex mission needs expensive AI reasoning. Simple tasks like systematic area scanning can be handled by fast rule-based logic, while only genuinely complex phases — like dynamic resource allocation when the fire spreads unexpectedly — invoke the LLM. This is what they call complexity-aware routing."

---

**4. KEY METHODOLOGY**

Say: "All experiments used GPT-4o at temperature zero for reproducibility. Each of the three frameworks was tested across 17 task levels with three random seeds per level — that's 51 episodes per framework. The testing environment, CREW-WILDFIRE, features four distinct agent types — firefighters, bulldozers, drones, and helicopters — and evaluates performance on seven behavioral competencies including task designation, spatial reasoning, plan adaptation, and real-time coordination. The hybrid system was then validated on the same 51 episodes, and additionally tested across variations in LLM model versions, temperature settings, and environmental parameters to confirm robustness."

---

**5. THE RESULTS**

Say: "The comparison revealed that CrewAI achieves the best overall performance at 52% normalized score and 68.5% success rate, excelling at structured tasks where hierarchical delegation shines. AutoGen is the most adaptive, scoring 28% better than CrewAI on plan adaptation, but at 27% higher token cost. LangChain offers the most flexibility but suffers from quadratic token scaling — at 30 agents, it consumes 315,000 tokens per episode compared to CrewAI's 89,000. The hybrid system then outperforms all of them: 96.1% success rate, 750 tokens per episode — that's 76.2% less than pure CrewAI — and decisions made in 2.2 seconds versus 32 seconds for CrewAI. The hybrid achieved perfect scores of 1.0 on both task designation and agent capitalization, and an average behavioral competency score of 0.87, which is 2.5 times better than the best traditional baseline."

---

**6. SIGNIFICANCE / CONTRIBUTION**

Say: "This paper contributes three things to the field. It gives us the first evidence-based decision guide for framework selection — telling practitioners exactly when to use each framework based on their specific needs. It introduces the first complexity-aware hybrid architecture with formal theoretical analysis showing O(n) rather than O(n-squared) scaling. And it demonstrates that intelligent hybrid designs can break the assumed trade-off between performance and cost: the hybrid is simultaneously the highest-performing and most cost-efficient system tested."

---

## Anticipated Questions and Model Answers

| Question Sir Might Ask | What Ayesha Should Say |
|---|---|
| **What is the main contribution of this paper?** | "The main contribution is actually two things working together. First, it's the first systematic comparison of CrewAI, AutoGen, and LangChain under identical large-scale conditions, using a 17-task benchmark with seven behavioral competency dimensions. Second, it proposes a hybrid LangGraph-CrewAI architecture with complexity-aware routing that achieves 96.1% success rate while reducing token costs by 76.2%. The theoretical contribution is showing that selective LLM invocation — only about 18.3% of decisions actually needed LLM reasoning — is sufficient to achieve top performance, which challenges the assumption that more AI reasoning always means better results." |
| **What makes this approach different from previous work?** | "Two things stand out. Previous framework comparisons evaluated systems in isolation on small-scale benchmarks with fewer than 10 agents. This paper tests all three on the same 100-plus agent wildfire benchmark with standardized interfaces — making the comparison genuinely fair for the first time. On the hybrid side, existing hybrid architectures statically combine frameworks in a fixed way. This paper's hybrid uses dynamic complexity-based routing — it decides in real time whether a situation needs LLM intelligence or rule-based efficiency. That's the architectural novelty that enables the dramatic efficiency gains." |
| **What are the limitations of this work?** | "I noticed a few limitations. The authors acknowledge that the benchmark only covers wildfire scenarios, so generalization to other domains like manufacturing or healthcare is unvalidated. All experiments used GPT-4o, so results with other LLM providers like Claude or Gemini are unknown. The hybrid was only tested with up to 6 agents experimentally, even though the paper claims O(n) scaling at 30-plus agents — that claim rests on theory, not direct measurement. And there's no formal ablation study isolating which specific component of the hybrid — LangGraph, CrewAI, or the routing mechanism — is actually responsible for the performance improvement." |
| **What evaluation metric did they use? Is it appropriate?** | "They used two main types of metrics. For performance, they used Behavioral Competency Scores — seven normalized dimensions including task designation, spatial reasoning, plan adaptation, and real-time coordination — plus overall success rate and task completion scores. For efficiency, they measured token consumption, API calls, decision latency, and estimated operational cost. I think this is actually one of the paper's strengths — using seven behavioral dimensions rather than a single aggregate score reveals much richer information. For example, CrewAI scores 0.59 on agent capitalization but only 0.27 on plan adaptation — two very different strengths invisible in a single number. The efficiency metrics are also unusually practical for an academic paper, giving direct cost projections in dollars per year." |
| **What dataset was used and why?** | "They used CREW-WILDFIRE, a publicly available benchmark specifically designed for large-scale multi-agent evaluation. It was chosen because it addresses the key gaps in existing benchmarks: it supports 100-plus agents and maps up to one million cells, includes four distinct agent types with different capabilities, features partial observability and stochastic fire spread that make it genuinely challenging, and provides a natural language interface compatible with LLM-based frameworks. It also includes the structured seven-competency evaluation framework. Essentially, it's the most realistic and demanding benchmark currently available for this type of research." |
| **Could this approach be applied to a related problem?** | "The paper suggests several domains where this hybrid design should transfer well — manufacturing assembly coordination, hospital patient care team management, and scientific research collaboration. The core principle of complexity-aware routing should apply anywhere you have a mix of routine, predictable operations and genuinely complex coordination decisions. That said, the complexity threshold τ and the rule-based logic would need to be redesigned for each new domain. The authors list cross-domain generalization as their top future work direction, so this is a recognized open question." |
| **What would you change if you were the author?** | "I would add a proper ablation study — specifically, testing versions of the hybrid with each component removed individually, to understand which piece actually drives the performance. Right now, we can't tell if the gains come from LangGraph's state machine, CrewAI's hierarchical coordination, or the routing mechanism itself. I would also be more explicit about the routing threshold τ — how it was chosen, how sensitive the system is to it, and whether it could be learned automatically rather than hand-tuned. And I would scale the experimental validation up to at least 30 agents to back up the theoretical scaling claims with real data." |
| **What future work do the authors suggest?** | "They suggest eight directions. The most important are: first, validating the hybrid across all 17 CREW-WILDFIRE tasks and extending to 100-plus agents to test real scalability. Second, implementing hierarchical manager structures for coordinating very large teams. Third, fine-tuning LLMs on successful coordination episodes so the system learns more efficient communication patterns over time. Fourth, adding attention-based selective communication to reduce unnecessary message passing. Fifth, integrating persistent vector databases so agents can access historical information instead of keeping full conversation histories in context. And sixth, evaluating across other domains to test generalizability." |
| **Do you find the results convincing? Why?** | "I find them largely convincing, yes. The experimental design is rigorous — standardized interfaces, identical conditions, multiple seeds, sensitivity analysis across models and environmental parameters. The finding that the hybrid achieves 95.8% success rate even when extended to 10 random seeds (versus 96.1% at 3 seeds) is a strong sign of genuine robustness. The mathematical formalization confirming the 76.2% token reduction is elegant and matches the empirical data. What I'm slightly cautious about is the scalability claim — the theory says O(n) scaling, but the hybrid was only tested with up to 6 agents. That's the one claim I'd want to see supported by larger-scale experiments before trusting it completely." |
| **How does this compare to traditional MARL approaches?** | "Traditional multi-agent reinforcement learning approaches like QMIX require extensive domain-specific engineering and struggle to generalize beyond their training environments. LLM-based frameworks like the ones in this paper coordinate through natural language, which means they can interpret novel instructions and handle situations they weren't explicitly trained for. The trade-off is cost and speed — LLMs are much more expensive per decision than trained policies. The hybrid system in this paper essentially tries to get the best of both worlds: LLM intelligence where it's needed, but fast deterministic execution where it isn't. The hybrid's 2.2-second latency is still much slower than traditional control systems, but for high-level strategic coordination rather than reactive control, it may be sufficient." |

---

## What NOT to Say

1. **Do not say "the frameworks were tested on real wildfires."** The CREW-WILDFIRE benchmark is a simulation, not a real-world deployment. Always say "simulation" or "benchmark."

2. **Do not overstate the scalability.** The hybrid was validated with up to 6 agents, not 100+. If asked about large-scale performance, say the theoretical analysis shows O(n) scaling but empirical validation at large scales is listed as future work.

3. **Do not say "the hybrid is always better than any single framework."** LangChain has better spatial reasoning performance (0.38 BCS) than CrewAI (0.32 BCS) among individual frameworks. For some specific applications, a single framework may still be the right choice.

4. **Do not confuse LangGraph with LangChain.** They are related but different. LangChain is the full framework tested in the comparison. LangGraph is a workflow orchestration extension of LangChain that forms the backbone of the hybrid's orchestration layer. The hybrid uses LangGraph — not LangChain — for coordination.

5. **Do not say the paper "proves" the hybrid will work in production.** The authors themselves list production deployment studies as future work. Say "demonstrates" or "shows strong preliminary evidence" instead.

---

## Closing Statement

> "In summary, this paper demonstrates that the choice of multi-agent framework is not a universal decision — each framework has distinct behavioral strengths and economic trade-offs that should match the specific task requirements. More importantly, it shows that a carefully designed hybrid architecture can surpass individual frameworks on both performance and cost efficiency simultaneously. The evidence-based selection guidelines and the hybrid's 96.1% success rate with 76.2% token reduction represent a practical step toward deploying LLM-based multi-agent systems at real-world scale. I'm happy to take any questions."

---

## If You Forget Something

If you blank on a detail, say:
> "The paper mentions that — let me make sure I give you the exact figure, but the key point is..."

For example:
- Forget the success rate? Say "the hybrid achieved the highest success rate across all frameworks — I believe it was in the mid-90s percent range."
- Forget the token reduction? Say "the hybrid reduced token consumption by over 75% compared to pure CrewAI."
- Forget a BCS number? Say "the hybrid scored highest on that dimension — the exact number is in the detailed results table."
