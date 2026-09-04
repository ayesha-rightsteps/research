━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PAPER CHEAT SHEET
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

TITLE:    Beyond Single-Framework Architectures: A Systematic
          Evaluation and Hybrid Design for Scalable Multi-Agent
          Coordination
AUTHORS:  Muhammad Saleem Khan, Muhammad Janas Khan,
          Muhammad Sharif, Sadaf Yasmin
VENUE:    IEEE Access  |  YEAR: 2026  |  DOI: 10.1109/ACCESS.2026.3683900

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
THE CORE STORY (memorize this)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PROBLEM:    No one had ever systematically compared CrewAI, AutoGen,
            and LangChain at realistic large scale — people chose
            frameworks by gut feeling with unpredictable results.

SOLUTION:   First fair head-to-head comparison on CREW-WILDFIRE
            (17 task levels, 100+ agents, 7 behavioral dimensions),
            then a novel hybrid LangGraph-CrewAI architecture with
            complexity-aware routing.

KEY RESULT: Hybrid achieves 96.1% success rate (49/51 episodes)
            with only 750 tokens/episode — 76.2% fewer than pure
            CrewAI (3,150 tokens), and 14.5x faster decisions
            (2.2s vs 32s). Perfect BCS scores (1.00) on Task
            Designation and Agent Capitalization.

SO WHAT:    Large-scale AI agent coordination is now cost-viable.
            For 30 agents, 1,000 missions/year: Hybrid costs $1,560
            vs LangChain's $12,653. Savings of $11,000+ per year
            makes real-world deployment practical.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
5 TERMS TO KNOW
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⭐ BCS (Behavioral Competency Score): 7-dimensional rating of agent
   coordination quality — TD, AC, SR, OS, RC, PA, OP

⭐ Complexity-Aware Routing: Deciding in real time whether a task
   needs expensive LLM reasoning or cheap rule-based logic

⭐ CrewAI: Hierarchical manager-worker framework — best for
   structured tasks (52% score, 68.5% success rate)

⭐ CREW-WILDFIRE: Large-scale wildfire simulation benchmark —
   17 tasks, 100+ agents, 4 agent types, 7 competency dimensions

⭐ Token Scaling: O(n) = cost grows linearly; O(n²) = cost
   explodes quadratically — LangChain is O(n²), Hybrid is O(n)

   AutoGen: Conversational multi-agent framework — best for
   adaptive tasks (0.35 Plan Adaptation BCS, best of 3 frameworks)

   LangChain: Chain-based flexible framework — best spatial
   reasoning (0.38 SR), but 42% more expensive than CrewAI

   LangGraph: State machine orchestrator — backbone of the
   hybrid, manages 4 mission phases (Detect, Suppress, Search, Rescue)

   Partial Observability: Each agent sees only local map area,
   making information sharing critical for coordination

   GPT-4o: The LLM used in all experiments, temperature=0
   for deterministic reproducible results

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
FRAMEWORK COMPARISON SNAPSHOT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

              CrewAI    AutoGen   LangChain   Hybrid
Norm. Score:   0.52      0.47      0.49        ---
Success Rate:  68.5%     61.2%     64.8%     96.1%
Tokens/ep:     3.2M      4.1M      4.6M      ~750
Avg Latency:   145s     138.7s    152.6s     2.2s
Est. Cost($):  24.50     31.20     35.80     0.38
Avg BCS:       0.67      0.34      0.37      0.87

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
EACH FRAMEWORK'S SUPERPOWER
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CrewAI  → Task Designation (0.48 BCS) + Agent Capitalization (0.59)
           Best for: structured tasks, clear delegation, budget tight
AutoGen → Plan Adaptation (0.35 BCS) + Observation Sharing (0.24)
           Best for: dynamic environments, human-in-the-loop needed
LangChain→ Spatial Reasoning (0.38 BCS) + flexible tool integration
           Best for: custom workflows, complex spatial calculations
Hybrid  → Everything: 0.87 avg BCS, perfect on TD+AC, 0.78 realtime

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
WHAT MAKES THIS PAPER UNIQUE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

• First fair, systematic comparison of 3 major LLM frameworks
  under identical conditions at 100+ agent scale

• Behavioral competency profiling (7 dimensions) reveals
  framework-specific strengths invisible in aggregate metrics

• Novel hybrid with complexity-aware routing achieves O(n) scaling
  versus O(n²) for LangChain — proven mathematically AND empirically

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
KEY NUMBERS TO REMEMBER
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

96.1% — Hybrid success rate (49/51 episodes)
76.2% — Token reduction vs. pure CrewAI
14.5× — Decision speed improvement vs. CrewAI (2.2s vs 32s)
0.87  — Hybrid average BCS (vs 0.67 CrewAI, 0.35 best traditional)
1.00  — Hybrid perfect BCS on Task Designation AND Agent Capitalization
18.3% — Fraction of decisions that needed LLM reasoning in hybrid
7×    — Fewer API calls (45 vs 315 per episode vs. CrewAI)
2.5×  — Better than best traditional baseline (CAMON: 0.35 BCS)
17    — Task levels in CREW-WILDFIRE benchmark
51    — Episodes in hybrid validation (17 scenarios × 3 seeds)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
QUICK Q&A
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

If asked about limitations:
→ "The hybrid was only tested with up to 6 agents experimentally,
   the scalability claims beyond that rely on theoretical analysis.
   Also, all tests used GPT-4o — generalization to other LLMs is
   not validated. And the benchmark only covers wildfire scenarios."

If asked what you'd change:
→ "I would add a formal ablation study removing each hybrid
   component individually, to isolate which piece — LangGraph,
   CrewAI, or the routing mechanism — actually drives the gains."

If asked about future work:
→ "The authors plan to validate the hybrid at 100+ agent scale,
   test cross-domain generalization in manufacturing and healthcare,
   and explore learned routing thresholds using reinforcement learning."

If asked why not just use CrewAI:
→ "CrewAI achieves only 68.5% success rate vs hybrid's 96.1%,
   and its decisions take 32 seconds vs hybrid's 2.2 seconds.
   The hybrid preserves CrewAI's strengths while fixing its
   adaptability and latency weaknesses."

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
