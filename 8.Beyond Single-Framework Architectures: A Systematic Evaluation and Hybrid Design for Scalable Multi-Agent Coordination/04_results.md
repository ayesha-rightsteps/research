# 04 — Results: What They Found and Why It Matters

---

## Key Results

**Result 1: CrewAI is the best single framework overall**

CrewAI achieved a 52% normalized score and 68.5% success rate across all 17 task levels — the highest of the three individual frameworks. AutoGen reached 47% normalized score / 61.2% success, and LangChain achieved 49% / 64.8%. All three substantially outperformed the passive baseline (31% normalized score).

In practical terms: if you have to pick just one framework right now and need reliable task completion, CrewAI is the safest choice. Its hierarchical manager-worker pattern is particularly powerful when tasks have a clear structure and can be neatly divided.

Compared to prior work: All three frameworks beat the traditional baselines (CAMON: 0.35 BCS, COELA: 0.25 BCS), validating the value of LLM-based coordination over purely algorithmic approaches.

---

**Result 2: Each framework has a different behavioral specialty**

Looking at task-by-task scores reveals something aggregate metrics hide entirely:

| Task Category | Winner | Score | Runner-up |
|---------------|--------|-------|-----------|
| Cut Trees (Task Designation) | CrewAI | 0.78 | LangChain: 0.69 |
| Scout Fire (Spatial Reasoning) | LangChain | 0.35 | AutoGen: 0.31 |
| Transport Firefighters (Real-time) | CrewAI | 0.62 | LangChain: 0.56 |
| Rescue Civilians (Plan Adaptation) | AutoGen | 0.41 | LangChain: 0.36 |
| Suppress Fire (Integrated) | AutoGen | 0.28 | LangChain: 0.26 |

In practical terms: No single framework dominates everything. If you run a mission that is mostly structured delegation (tree cutting, transport), use CrewAI. If your mission involves dynamic uncertainty (civilian rescue, adaptive firefighting), use AutoGen. If you need complex spatial calculations, LangChain has an edge.

---

**Result 3: LangChain is dangerously expensive at scale** ⭐

LangChain's token scaling is quadratic — O(n²). Here is what that means in numbers:

| Agents | CrewAI Tokens | AutoGen Tokens | LangChain Tokens | Hybrid Tokens |
|--------|---------------|----------------|------------------|---------------|
| 3 | 8,200 | 10,500 | 11,800 | 3,100 |
| 10 | 26,800 | 38,700 | 51,400 | 10,800 |
| 20 | 56,700 | 87,300 | 142,800 | 24,100 |
| 30 | 89,400 | 138,900 | 315,600 | 38,900 |

At 30 agents, LangChain consumes 315,600 tokens per episode — 3.5× more than CrewAI and 8.1× more than the Hybrid. For an organization running 1,000 missions per year with 30 agents, LangChain would cost $12,653/year versus the Hybrid's $1,560/year.

This is the most critical practical finding of the comparison section. LangChain's architecture fundamentally lacks mechanisms to limit inter-agent communication growth, making it economically unviable for large-scale deployments.

---

**Result 4 (MOST IMPRESSIVE): The Hybrid achieves 96.1% success while cutting costs by 76.2%**

This is the headline result of the paper. Across 51 episodes (17 scenarios × 3 seeds), the hybrid system achieved:

| Metric | Hybrid | Pure CrewAI | Improvement |
|--------|--------|-------------|-------------|
| Success Rate | 96.1% (49/51) | 88.9% (45/51) | +7.2 percentage points |
| Avg Tokens/Episode | 750 | 3,150 | -76.2% (4.2× cheaper) |
| Avg Latency | 2,200ms | 32,000ms | 14.5× faster |
| Total Cost (51 episodes) | $0.38 | $1.58 | -76% |
| API Calls/Episode | 45 | 315 | 7× fewer |

The hybrid simultaneously achieved the highest performance AND the lowest cost — which should be impossible if you accept the premise that better performance requires more computation. The key insight is that this trade-off does not hold when you apply intelligence selectively rather than uniformly.

---

**Result 5: The Hybrid's Behavioral Competency Scores are in a different league**

Comparing average BCS across all evaluated systems:

| System | Avg BCS | Relative to Hybrid |
|--------|---------|-------------------|
| Hybrid | **0.87** | — |
| CrewAI | 0.67 | 30% below Hybrid |
| CAMON (best traditional) | 0.35 | 2.5× below Hybrid |
| COELA | 0.25 | 3.5× below Hybrid |
| HMAS-2 | 0.32 | 2.7× below Hybrid |
| Embodied | 0.32 | 2.7× below Hybrid |

Individual BCS highlights for the Hybrid:
- Task Designation: **1.00** (perfect — matches CrewAI's strength)
- Agent Capitalization: **1.00** (perfect — exceeds CrewAI's 0.67)
- Spatial Reasoning: **0.85** (outperforms all systems, 2.9× better than traditional baselines)
- Observation Sharing: **0.92** (strong, just below CrewAI's 1.00)
- Realtime Coordination: **0.78** (while pure LLM frameworks like CrewAI and LangGraph scored 0.00 here)
- Plan Adaptation: **0.65** (2.9× better than traditional baselines)

---

## Tables and Figures Explained

### Table 1: Framework Architectural Comparison
**What it shows:** A side-by-side comparison of CrewAI, AutoGen, and LangChain across 8 dimensions: Abstraction Level, Setup Complexity, Communication style, Task Structure, Human-in-loop capability, Tool Integration, Flexibility, and Learning Curve.
**Key takeaway:** CrewAI is easy to set up (Low complexity) but medium flexibility; LangChain is highly flexible but steep learning curve; AutoGen is the middle ground.
**What to say to sir:** "This table shows that the three frameworks represent fundamentally different design philosophies — CrewAI prioritizes ease of use, LangChain prioritizes flexibility, and AutoGen balances both with a focus on conversational coordination."

---

### Table 2: Overall Framework Performance Comparison
**What it shows:** Aggregate performance of CrewAI, AutoGen, LangChain, and a passive baseline across five metrics: Average Normalized Score, Success Rate, Average Steps, Total Tokens, and Estimated Cost.
**Key takeaway:** CrewAI leads on performance and cost; AutoGen is fastest in steps; LangChain is most expensive. All beat the baseline.
**What to say to sir:** "This table confirms that CrewAI achieves the best balance of performance (52% score, 68.5% success) and cost ($24.50 total) among the three frameworks, while LangChain's $35.80 cost reflects its 42% higher token overhead."

---

### Table 3: Behavioral Competency Scores by Framework
**What it shows:** Scores for each of the 7 behavioral dimensions (TD, AC, SR, OS, RC, PA, OP) for CrewAI, AutoGen, and LangChain, plus their average BCS.
**Key takeaway:** Each framework excels in different dimensions — there is no single best framework across all competencies.
**What to say to sir:** "This table is one of the most important in the paper. It shows that aggregate metrics hide critical differences: CrewAI leads in Task Designation (0.48) and Agent Capitalization (0.59), AutoGen leads in Plan Adaptation (0.35) and Observation Sharing (0.24), and LangChain leads in Spatial Reasoning (0.38). This directly motivates the hybrid design."

---

### Figure 1: Normalized Scores by Task Category
**What it shows:** A bar chart showing each framework's normalized score across the 5 task categories (Cut Trees, Scout Fire, Transport FF, Rescue Civilians, Suppress Fire).
**Key takeaway:** CrewAI dominates structured tasks; AutoGen excels in adaptive tasks; LangChain is most balanced across categories.
**What to say to sir:** "This figure visually confirms that framework performance is task-dependent, not universal. CrewAI's score of 0.78 on Cut Trees drops to 0.32 on Rescue Civilians, while AutoGen's strength grows from 0.64 to 0.41 in adaptive scenarios."

---

### Figure 2: Token Consumption Scaling with Agent Count
**What it shows:** A line graph of token usage from 3 to 30 agents for all four systems (CrewAI, AutoGen, LangChain, Hybrid).
**Key takeaway:** LangChain's line curves upward dramatically (quadratic growth), while Hybrid's line stays nearly flat relative to the others.
**What to say to sir:** "This figure is the clearest visualization of why LangChain cannot scale. At 10 agents it uses 51,400 tokens — manageable. At 30 agents, it uses 315,600 tokens. The Hybrid by contrast reaches only 38,900 tokens at 30 agents, demonstrating that the complexity-aware routing keeps scaling under control."

---

### Figure 3: Hybrid System Architecture Diagram
**What it shows:** A flowchart showing the hybrid's four components: LangGraph Workflow Controller at top → Complexity Detection and Routing → two branches: Rule-Based Logic (Simple) and CrewAI Coordinator (Complex).
**Key takeaway:** The hybrid is not a random combination of tools — it has a clear, principled architecture where components have distinct responsibilities.
**What to say to sir:** "This architecture diagram shows the hybrid's key innovation — the complexity-detection layer. Everything flows through LangGraph, but only genuinely complex phases escalate to CrewAI. Simple tasks go through rule-based logic, which is why the system is both fast and efficient."

---

### Table 4: Hybrid Routing Decisions
**What it shows:** For each of the five mission phases, whether the hybrid routes to Simple (rule-based) or Complex (CrewAI), and the rationale.
**Key takeaway:** Fire Detection and Civilian Search are simple (pattern-based); Fire Suppression and Rescue Operations are complex (require LLM coordination); Agent Transport is medium complexity (LangGraph handles directly).
**What to say to sir:** "This table makes the routing logic concrete. Not all parts of a mission are equally complex. Detecting fire patterns is algorithmic; deciding how to allocate firefighters when the wind shifts and civilians are discovered in new locations requires genuine intelligence."

---

### Figure 4: Resource Efficiency Comparison (Hybrid vs. Pure CrewAI)
**What it shows:** A bar chart comparing Hybrid vs. CrewAI on three metrics: Average Tokens per Episode, Average Latency (ms), and API Calls per Episode.
**Key takeaway:** On every resource metric, the Hybrid dramatically outperforms pure CrewAI.
**What to say to sir:** "This figure visually captures the 76.2% token reduction, 14.5× latency improvement, and 7× fewer API calls that the hybrid achieves over pure CrewAI — making the efficiency gains immediately obvious without needing to read tables."

---

### Figure 5: Success Rate Comparison
**What it shows:** A bar chart of success rates for CrewAI versus the Hybrid system.
**Key takeaway:** Hybrid achieves 96.1% (shown as ~95.6% in the figure caption, with 96.1% in Table 5) vs. CrewAI's ~89% — demonstrating that the hybrid is not just cheaper but also more reliable.
**What to say to sir:** "This chart shows that the hybrid does not trade performance for efficiency — it achieves both simultaneously. The 96.1% success rate of the hybrid versus 88.9% for pure CrewAI means the hybrid is both cheaper and more reliable."

---

### Figure 6: Behavioral Competency Score Comparison (Hybrid vs. CrewAI)
**What it shows:** A bar chart comparing BCS scores on Task Designation and Agent Capitalization for CrewAI vs. the Hybrid.
**Key takeaway:** Hybrid achieves perfect scores (1.00) on both dimensions, while CrewAI scores 1.00 on TD but only 0.67 on AC.
**What to say to sir:** "On the two behavioral competencies fully measured in the hybrid validation, the hybrid achieves perfect scores. The fact that Agent Capitalization jumps from 0.67 (CrewAI) to 1.00 (Hybrid) shows that the hybrid makes better use of each specialized agent type than the original framework it incorporates."

---

### Table 5: Comprehensive Hybrid Validation Results
**What it shows:** Success rate, episodes completed, average tokens, and average latency for Hybrid, CrewAI, AutoGen, LangChain, and Rule-Based baseline.
**Key takeaway:** Hybrid leads on success rate while having dramatically lower resource consumption than all LLM-based approaches. Rule-based is fastest (8ms) and cheapest (0 tokens) but achieves only 64.4% success.
**What to say to sir:** "This table is the paper's main result table. The Hybrid achieves the highest success rate (96.1%) at the lowest LLM cost (750 tokens, $0.38). The Rule-Based system is technically faster and cheaper, but its 64.4% success rate confirms that intelligence is needed — the hybrid provides it selectively."

---

### Table 6: Behavioral Competency Scores — Hybrid vs. State-of-the-Art Baselines
**What it shows:** Full BCS comparison across all 7 dimensions for CAMON, COELA, Embodied, HMAS-2, CrewAI, LangGraph, and Hybrid.
**Key takeaway:** Hybrid achieves highest scores in almost every dimension, with an average BCS of 0.87 versus the next best (CrewAI at 0.67).
**What to say to sir:** "This is the most comprehensive performance table in the paper. The Hybrid's 0.87 average BCS represents a 2.5× improvement over the best traditional system (CAMON: 0.35) and a 30% improvement over pure CrewAI (0.67), demonstrating the hybrid's superiority across all behavioral dimensions."

---

### Table 9: Detailed Performance by Task Level
**What it shows:** For every one of the 17 task levels, mean score ± standard deviation for each of the five systems, compared against the target value.
**Key takeaway:** The Hybrid achieves target scores or near-target scores in most tasks, with consistently lower standard deviations (0.6-2.5) than competing frameworks (0.9-6.2), indicating more reliable and predictable behavior.
**What to say to sir:** "The lower standard deviations are as important as the mean scores. Hybrid's consistency — particularly the 0.00 standard deviation on Scout Fire tasks — shows that its rule-based coordination for reconnaissance phases eliminates the variability inherent in pure LLM approaches."

---

## Comparison with Prior Work

**Previous best results on CREW-WILDFIRE:** CAMON achieved the highest average BCS among the four traditional baselines at 0.35. The original CREW-WILDFIRE paper found that frameworks like COELA and HMAS-2 sometimes failed to outperform passive baselines on complex tasks.

**This paper's results in comparison:**
- The hybrid (0.87 BCS) represents a **2.5× improvement** over CAMON (0.35 BCS)
- Even pure CrewAI (0.67 BCS) outperforms CAMON by 91%
- The hybrid's 96.1% success rate versus the best traditional baseline's 73.3% (fire suppression tasks) represents a 22.8 percentage point improvement

**Where the hybrid wins:** Virtually every dimension, especially in Task Designation (1.00 vs 0.39), Agent Capitalization (1.00 vs 0.50), and Realtime Coordination (0.78 vs 0.49).

**Where there are still gaps:** Plan Adaptation remains the weakest dimension even for the hybrid (0.65), far below human-level performance (1.0). This is acknowledged as a fundamental challenge for all current AI systems.

---

## Real-World Meaning

If the hybrid LangGraph-CrewAI system were deployed in an actual wildfire emergency response coordination center:

- **Faster decisions:** At 2.2 seconds per decision cycle (versus 32 seconds for pure CrewAI), field commanders would receive coordinated action plans in near-real-time, potentially saving lives in rapidly evolving fire situations.

- **Lower cost:** An operation center running 10,000 missions annually (think continuous monitoring of large national parks or industrial fire-prone regions) would spend $15,600/year on the hybrid versus $126,530/year on LangChain — a saving of over $110,000 annually that could fund additional human operators or physical resources.

- **Higher reliability:** A 96.1% success rate means only about 4 missions in 100 fail to meet their objective. For emergency response, that reliability gap between 64% (rule-based) and 96% (hybrid) translates directly to more civilians rescued and more property saved.

- **Broader applicability:** The paper demonstrates consistent high performance across fire suppression (97.8%), rescue operations (91.7%), and transport coordination (94.4%) — showing the hybrid is not a specialist tool for one task type but a general coordination architecture.
