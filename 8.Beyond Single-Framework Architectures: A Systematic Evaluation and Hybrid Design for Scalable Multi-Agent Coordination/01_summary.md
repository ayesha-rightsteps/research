# 01 — Full Paper Summary

---

## Paper Identity

- **Full Title:** Beyond Single-Framework Architectures: A Systematic Evaluation and Hybrid Design for Scalable Multi-Agent Coordination
- **Authors:** Muhammad Saleem Khan, Muhammad Janas Khan, Muhammad Sharif, Sadaf Yasmin
- **Year:** 2026
- **Venue:** IEEE Access (Volume 14), DOI: 10.1109/ACCESS.2026.3683900
- **Research Domain:** Multi-Agent Systems, Large Language Model (LLM)-based AI Frameworks, Agentic AI, Scalable Coordination

---

## The Problem

Imagine you need to deploy dozens — or even hundreds — of AI agents to handle a complex real-world crisis, like a wildfire spreading across a million-cell map. Some agents are firefighters, some are drones doing surveillance, some are helicopters ferrying people to safety. They all need to coordinate instantly, adapt when things go wrong, and do it without burning through astronomical amounts of computational resources.

Several software frameworks exist to build exactly these kinds of multi-agent AI systems. The three most widely used are **CrewAI**, **AutoGen**, and **LangChain**. Organizations and researchers have been adopting these frameworks rapidly — but almost always based on convenience or habit, with little understanding of how they actually perform under pressure. No one had systematically compared all three under the same realistic, large-scale conditions. This gap is serious: choosing the wrong framework can result in agents that fail at critical moments, or systems so expensive to run they are economically infeasible.

Making matters worse, existing benchmarks for testing multi-agent AI were too small (fewer than 10 agents), too simple, or lacked the agent diversity and unpredictability of real emergencies. Developers were essentially flying blind when picking a framework.

---

## The Proposed Solution

The authors tackled this gap head-on with a two-part contribution. First, they conducted the **first comprehensive, fair, side-by-side comparison** of CrewAI, AutoGen, and LangChain under identical conditions across 17 task levels and 7 behavioral evaluation dimensions, using the CREW-WILDFIRE benchmark — a realistic, large-scale wildfire simulation with over 100 agents, four distinct agent types (firefighters, bulldozers, drones, helicopters), and partial observability (agents can't see everything at once).

Second — and this is the real innovation — they used what they learned from that comparison to design a **novel hybrid architecture** called **LangGraph-CrewAI Hybrid**. The key insight driving this design: not every coordination decision needs expensive AI reasoning. Simple, repetitive tasks (like scanning an area) can be handled by cheap, fast rule-based logic. Only genuinely complex decisions (like dynamic resource allocation during an unexpected fire spread) should invoke the powerful but costly LLM reasoning. By routing tasks intelligently between these two modes, the hybrid system achieves dramatically better performance at a fraction of the cost.

This is fundamentally different from existing hybrid approaches, which simply combine frameworks in a fixed, static way. The LangGraph-CrewAI hybrid uses **dynamic, complexity-aware routing** — it decides in real time whether a situation needs LLM intelligence or rule-based efficiency.

---

## The Method (in one paragraph)

The researchers implemented all three frameworks — CrewAI (hierarchical manager-worker delegation), AutoGen (group-chat-based conversational coordination), and LangChain (sequential chain-based pipelines) — with standardized perception modules (converting agent observations to natural language) and execution modules (translating LLM-generated instructions back into executable actions). They tested every framework on 17 task levels from CREW-WILDFIRE across 3 random seeds each (51 total episodes per framework) using GPT-4o as the underlying language model at temperature=0 for reproducibility. Performance was measured across task completion scores, success rates, token consumption, API calls, decision latency, and seven Behavioral Competency Scores (BCS). Informed by these results, they then built the hybrid LangGraph-CrewAI system — featuring a four-phase LangGraph state machine (detect, suppress, search, rescue), a complexity-detection router, rule-based execution for simple phases, and CrewAI coordination crews for complex phases — and validated it across 51 more episodes with the same protocol.

---

## The Key Results

1. **CrewAI achieved the best overall task performance (52% normalized score, 68.5% success rate)** among the three individual frameworks, excelling at structured tasks like cutting trees (score 0.78) and transporting firefighters (0.62) thanks to its hierarchical delegation model. In plain terms: when tasks are well-structured and predictable, CrewAI is your best bet.

2. **AutoGen was the most adaptable framework**, achieving 28% better plan adaptation (BCS 0.35) compared to CrewAI, because its conversational feedback loop allowed agents to raise concerns and trigger re-planning dynamically. The cost: 27% more tokens and slower decisions (138.7 average steps vs CrewAI's 145.3, though AutoGen was faster per step).

3. **LangChain was the most expensive framework**, incurring 42% higher token costs than CrewAI due to its chain-to-chain state passing, and showing quadratic O(n²) token scaling — meaning costs explode as the number of agents grows. At 30 agents, LangChain consumed 315,600 tokens per episode versus CrewAI's 89,400.

4. **The hybrid LangGraph-CrewAI system achieved a 96.1% success rate (49/51 episodes)** while consuming only 750 tokens per episode — a 76.2% reduction compared to CrewAI's 3,150 tokens/episode. Decisions were made in 2.2 seconds on average, 14.5 times faster than pure CrewAI (32 seconds). The hybrid also scored perfect 1.00 BCS on both Task Designation and Agent Capitalization, outperforming all baselines including CAMON, COELA, HMAS-2, and Embodied agents from the CREW-WILDFIRE leaderboard.

5. **The hybrid's cost savings are transformative at scale:** For 1,000 missions per year with 30 agents, the hybrid costs $1,560/year compared to LangChain's $12,653/year — a saving of over $11,000 per year for a single deployment, making large-scale agentic AI practically viable.

---

## The Contribution

This paper makes the first systematic, evidence-based comparison of the three dominant LLM multi-agent frameworks at realistic scale, and demonstrates that a complexity-aware hybrid architecture can simultaneously achieve higher performance, lower cost, and faster decisions than any single framework — providing both the research community and industry practitioners with a principled, data-driven basis for framework selection and system design.

**One-sentence takeaway Ayesha can quote to sir:**
"This paper proves that no single multi-agent framework is best at everything, and that a hybrid LangGraph-CrewAI design achieves a 96.1% success rate while cutting token costs by 76% — the best of all worlds."
