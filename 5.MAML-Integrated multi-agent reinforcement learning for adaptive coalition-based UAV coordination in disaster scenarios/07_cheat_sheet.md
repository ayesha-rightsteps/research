━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📄 PAPER CHEAT SHEET
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

TITLE:    MAML-Integrated Multi-Agent Reinforcement
          Learning for Adaptive Coalition-Based UAV
          Coordination in Disaster Scenarios
AUTHORS:  Sabitri Poudel, Sangman Moh
          Chosun University, South Korea
VENUE:    Internet of Things (Elsevier), Vol. 37
          Article 101930  |  YEAR: 2026
DOI:      10.1016/j.iot.2026.101930

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
THE CORE STORY (memorize this)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PROBLEM:    Coordinating heterogeneous UAV swarms in
            disaster response — drones differ in type,
            some fail mid-mission, communication is
            unreliable, and every disaster is new.

SOLUTION:   RCTP — combines MAML (fast adaptation to
            new scenarios) + MA-DDPG (continuous
            control) + coalition formation (team drones
            by capability, auto-reform on failure).

KEY RESULT: 30–40% faster mission completion;
            10–20% lower energy; robust to multiple
            drone failures; millisecond inference.

SO WHAT:    First framework to handle heterogeneous
            drones + failures + bad communication +
            unseen environments all together.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
5 TERMS TO KNOW
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⭐ MAML:          Train to learn fast — adapts to new
                  disaster in a few gradient steps

⭐ Coalition:      Small drone team matched to a task
                  by capability — auto-reforms on failure

⭐ RCTP:          The full framework: MAML + MA-DDPG +
                  coalition + energy-aware routing

⭐ Heterogeneous: Drones with different sensors/speeds —
                  first paper in this folder to handle this

   LoS/NLoS:     Line-of-sight vs. blocked communication
                  — explicitly modeled in this paper

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
KEY NUMBERS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

UAVs tested:        10 to 30 (heterogeneous)
Baselines beaten:   PPO, DQN, MA-DDPG (no MAML)
Speed improvement:  30–40% faster mission completion
Energy saving:      10–20% lower consumption
Inference time:     Millisecond-level per agent
Scale vs. Paper 4:  Paper 4 = 80–120 drones (larger)
                    This paper = 10–30 drones (smaller)

WHAT MAKES THIS UNIQUE vs. OTHER PAPERS:
• Only paper with heterogeneous drone types
• Only paper with drone failure + auto-recovery
• Only paper with LoS/NLoS communication modeling
• Only paper with energy consumption optimization
• Only paper using MAML for fast scenario adaptation
• Only paper with disaster response (not military)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
HOW MAML WORKS (quick version)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Training: Learn across many diverse disaster scenarios
          → get meta-parameters θ*
Deploy:   Load θ* → collect tiny data → K grad steps
          → adapted policy ready in seconds
Why:      Every disaster is different — can't
          pre-train on exact environment

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
QUICK Q&A
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

If asked about limitations:
→ "Only tested to 30 drones (vs. 80+ in Paper 4);
   simulation only; MAML still needs a few data
   points from the new scenario to adapt."

If asked what you'd change:
→ "Scale to 80+ drones and test with actual hardware
   — the millisecond inference suggests it could work."

If asked about future work:
→ "Scale to larger swarms, validate on real hardware,
   combine MAML with mean-field methods for 100+ drones."

If asked why it's better than MA-DDPG alone:
→ "MA-DDPG alone needs long retraining for each new
   scenario and treats all drones as identical.
   RCTP adds fast MAML adaptation + coalition
   formation that respects drone heterogeneity."

If asked how it handles drone failures:
→ "Suitability scores update continuously — when a
   drone fails, remaining drones recompute scores and
   reform coalitions automatically. No central
   controller needed."

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
