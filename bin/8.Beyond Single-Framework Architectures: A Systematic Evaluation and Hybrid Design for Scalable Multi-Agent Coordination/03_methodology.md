# 03 — Methodology: What the Researchers Did, Step by Step

---

## Research Design

**Type of study:** This is an experimental comparative evaluation study combined with a system design paper. The researchers ran controlled experiments, then used those findings to design and validate a new system.

**Overall strategy:**
1. Take three real-world multi-agent frameworks (CrewAI, AutoGen, LangChain)
2. Build a standardized testing harness so all three compete on equal footing
3. Run all three on the same benchmark across the same conditions
4. Analyze results across 17 task levels and 7 behavioral dimensions
5. Identify each framework's strengths and weaknesses
6. Design a hybrid system that combines the best aspects of each
7. Validate the hybrid against all baselines

---

## The Data (Testing Environment)

**Benchmark Used:** CREW-WILDFIRE — a publicly available, procedurally generated multi-agent benchmark designed specifically for large-scale coordination research.

**What CREW-WILDFIRE provides:**
- **17 task levels** across five categories, each testing different coordination skills
- **Maps up to 1,000,000 cells** (1 million cell grids), making this far larger than any prior benchmark
- **100+ simultaneous agents** of four distinct types
- **Partial observability** — agents can only see a local portion of the map (represented as ASCII minimaps)
- **Stochastic dynamics** — fire spreads randomly, wind changes direction, civilians can be discovered in unexpected locations
- **Structured evaluation** using seven behavioral competency dimensions

**The 5 Task Categories (17 levels total):**

| Category | Levels | Primary Competency Tested |
|----------|--------|--------------------------|
| Cut Trees | 4 levels | Task Designation, Agent Capitalization |
| Scout Fire | 2 levels | Spatial Reasoning, Observation Sharing |
| Transport Firefighters | 2 levels | Real-time Coordination |
| Rescue Civilians | 4 levels | Plan Adaptation |
| Suppress Fire | 4 levels | All integrated competencies |

**The 4 Agent Types:**
- **Firefighters:** Can cut trees, spray water, rescue civilians — but have limited mobility
- **Bulldozers:** Specialized for rapid vegetation clearing (faster than firefighters at this)
- **Drones:** Aerial observation with wide-area reconnaissance — can't fight fire directly
- **Helicopters:** Transport agents and drop water — critical for logistics operations

**Why this data was appropriate:** CREW-WILDFIRE was chosen precisely because it addresses the gaps in existing benchmarks — it has agent heterogeneity (4 types), operates at large scale (100+ agents), includes partial observability and stochastic dynamics, uses natural language interfaces, and provides structured multi-dimensional evaluation. It is the closest available approximation to a real-world coordination challenge.

---

## Standardization Protocol

To ensure a fair comparison, the researchers built two standardized modules that all three frameworks used:

**PERCEPTION Module:**
- Converts raw agent observations (ASCII minimap grid representations) into natural language spatial descriptions
- Example output: "You are at position (45, 32). There is active fire to your north-east. A civilian is visible 3 cells to the south. Your bulldozer teammate is operating 7 cells west."
- This ensures every framework receives the same quality of information

**EXECUTION Module:**
- Takes the natural language action commands that an LLM generates ("move north, then spray water")
- Translates these into executable vector formats the simulation understands
- Handles multi-step action composition like pathfinding (breaking "go to location X" into individual movement steps)
- This ensures every framework's decisions are executed with equal fidelity

---

## The Three Framework Implementations

### Implementation 1: CrewAI

The researchers built a hierarchical crew with the following structure:

**Algorithm (Algorithm 1 from paper):**
```
1. Initialize one manager agent and multiple specialized worker agents
2. For each timestep:
   a. Collect observations from ALL agents
   b. Generate natural language perception for each agent
   c. Manager receives all perceptions and decomposes the mission into sub-tasks
   d. Manager delegates sub-tasks to specific worker agents based on capabilities
   e. Each worker translates its assignment into an executable action
   f. All agents execute their actions simultaneously
   g. Repeat
```

**Key design choice:** The manager sees everything (centralized knowledge) and makes all high-level decisions. Workers execute instructions but can request reassignment if they encounter obstacles.

**Why this implementation:** Follows CrewAI's recommended best practices using its hierarchical process mode, with agents defined by their role, goals, backstory, and available tools.

---

### Implementation 2: AutoGen

The researchers built a GroupChat configuration:

**Algorithm (Algorithm 2 from paper):**
```
1. Initialize AssistantAgents for each agent type + GroupChatManager
2. For each timestep:
   a. Collect observations from all agents
   b. Generate perceptions for each agent
   c. Run multiple communication rounds (round-robin):
      - Each agent generates a message based on its perception and conversation history
      - Message is broadcast to all other agents in the GroupChat
   d. After communication rounds complete:
      - Each agent generates its action based on all messages received
      - All agents execute their actions
   e. Repeat
```

**Key design choice:** All agents participate in shared conversation. Information sharing happens organically through message exchange. There is no central authority — agents collectively arrive at coordinated decisions.

**Why this implementation:** Follows AutoGen's recommended GroupChat pattern, designed to capture AutoGen's strength in information sharing and collaborative decision-making.

---

### Implementation 3: LangChain

The researchers built a four-stage sequential chain pipeline:

**Algorithm (Algorithm 3 from paper):**
```
1. Initialize four chains: PerceptionChain, PlanningChain, CoordinationChain, ExecutionChain
2. For each timestep:
   a. PerceptionChain: Takes raw observations → produces structured descriptions
   b. PlanningChain: Takes structured descriptions + history → generates action proposals for each agent
   c. CoordinationChain: Takes all proposals + global state → resolves conflicts → finalizes coordinated actions
   d. ExecutionChain: Takes finalized actions → translates to executable vectors
   e. All agents execute their assigned actions
   f. Repeat
```

**Key design choice:** Information flows through the chain in sequence. Each chain receives the full output of the previous chain (including all agent states), which is what causes the expensive O(n²) token scaling.

**Why this implementation:** Follows LangChain's compositional pattern, designed to capture its strength in flexible, fine-grained coordination control.

---

## The Hybrid Architecture Implementation

The hybrid system has four components working together:

### Component 1: LangGraph State Machine (Orchestration Layer)
- Maintains a four-phase mission workflow: **Detect → Suppress → Search → Rescue**
- At each phase transition, evaluates mission complexity
- Does not generate actions directly — manages flow and tracks global state
- Provides full interpretability: every decision point is logged and traceable

### Component 2: Complexity Detection and Routing Module
Evaluates four factors at each transition:
- Number of active agents and their workload
- Degree of inter-agent dependency (do agents need to coordinate with each other?)
- Environmental uncertainty (fire spread rate, unexplored map area)
- Need for dynamic re-planning (have recent events changed the optimal plan?)

**Routing rule:**
```
If complexity(current_state) > threshold τ:
    Route to CrewAI coordination (LLM reasoning)
Else:
    Route to rule-based execution
```

Empirically, only 18.3% of decisions crossed the complexity threshold and required LLM reasoning.

### Component 3: Rule-Based Execution (Simple Phase)
Handles predictable, low-interdependency tasks:
- Systematic area scanning (divide map into grid sectors, assign one per agent)
- Predefined movement patterns (patrol routes, sweep patterns)
- Routine agent transport (helicopter follows fixed schedule)
- Basic environmental monitoring (drone maintains coverage pattern)
Cost: near-zero tokens, near-zero latency (~8ms)

### Component 4: CrewAI Coordination (Complex Phase)
Activated when complexity threshold is crossed:
- **Fire Suppression Coordinator crew:** Manages firefighter/bulldozer teams for dynamic fire suppression
- **Rescue Mission Coordinator crew:** Handles civilian rescue, evacuation routing, helicopter dispatch
- Manager agent performs strategic task decomposition
- Worker agents coordinate through role-based delegation
- Fallback: If CrewAI generates an error or LLM fails, automatically switches to rule-based execution to ensure mission continuity

---

## Pipeline Diagram

```
[Raw Agent Observations (ASCII minimaps)]
          ↓
[PERCEPTION Module: Convert to Natural Language Descriptions]
          ↓
[LangGraph State Machine: Determine Current Mission Phase]
          ↓
[Complexity Detection & Routing Module]
    ↙ Low Complexity          ↘ High Complexity
[Rule-Based Execution]    [CrewAI Coordination]
 - Area scan               - Manager decomposes task
 - Patrol patterns         - Assigns to specialist workers
 - Routine transport       - Workers execute delegated tasks
 - Near-zero latency       - LLM reasoning invoked
          ↓                          ↓
    [EXECUTION Module: Translate to Action Vectors]
          ↓
[Agents Execute Actions in CREW-WILDFIRE Environment]
          ↓
[Next Timestep: Updated Observations]
```

---

## The Experiments

**Experiment 1: Framework Comparison**
- 3 frameworks × 17 task levels × 3 random seeds = 153 total evaluation episodes
- Each episode evaluated on: normalized task score, success rate, execution time, token usage, API calls, and 7 BCS dimensions
- All frameworks used GPT-4o at temperature=0

**Experiment 2: Hybrid Validation**
- 17 task scenarios × 3 random seeds = 51 total episodes
- Compared against: pure CrewAI, pure AutoGen, LangChain, rule-based baseline, and 4 existing CREW-WILDFIRE systems (CAMON, COELA, HMAS-2, Embodied)

**Experiment 3: Sensitivity Analysis**
- LLM model variations: GPT-4o, GPT-4-Turbo, GPT-4, GPT-3.5-Turbo
- Temperature sensitivity: 0.0, 0.3, 0.7, 1.0
- Extended seed testing: 10 seeds per scenario (170 episodes) vs. 3 seeds
- Environmental perturbations: fire spread rate ±30%, wind direction ±45°, agent count 4-8, map size 30×30 to 80×80, victim distribution variations, initial fire size 5-25 cells

**Baselines compared against:**
| System | Type |
|--------|------|
| CAMON | Traditional multi-agent (avg BCS 0.35) |
| COELA | Traditional multi-agent (avg BCS 0.25) |
| HMAS-2 | Traditional multi-agent (avg BCS 0.32) |
| Embodied | Traditional multi-agent (avg BCS 0.32) |
| Rule-Based | Pure deterministic (64.4% success, 0 tokens) |
| Pure CrewAI | Single LLM framework (88.9% success) |

**Evaluation Metrics:**
- **Raw score:** Task-specific achievement (trees cut, civilians rescued, fire damage score)
- **Normalized Score (NS):** Raw score adjusted to [0,1] range using baseline and target values
- **Success Rate:** Percentage of episodes reaching target performance threshold
- **BCS (7 dimensions):** TD, AC, SR, OS, RC, PA, OP — each normalized to [0,1]
- **Total Tokens:** Sum of input + output tokens per episode
- **API Calls:** Number of LLM requests per episode
- **Decision Latency:** Average time from observation to action (milliseconds)
- **Estimated Cost:** Based on GPT-4o pricing ($5/1M input, $15/1M output tokens)

**Hardware/Software:**
- Hardware: 16GB RAM, NVIDIA RTX 3060 GPU, 3.0 GHz CPU
- LLM: GPT-4o (OpenAI API)
- Random seeds: 43, 375, 483 (for 3-seed experiments)
- Frameworks: CrewAI, AutoGen (Microsoft), LangChain/LangGraph (all open-source)
