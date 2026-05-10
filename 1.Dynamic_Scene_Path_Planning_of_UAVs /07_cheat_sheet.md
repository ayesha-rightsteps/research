```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📄 PAPER CHEAT SHEET
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

TITLE:    Dynamic Scene Path Planning of UAVs Based on
          Deep Reinforcement Learning
AUTHORS:  Jin Tang, Yangang Liang, Kebo Li
VENUE:    Drones (MDPI Open Access Journal)  |  YEAR: 2024

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
THE CORE STORY (memorize this)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PROBLEM:    Classical UAV path planners fail in dynamic environments
            where threat zones (radar/SAM systems) are moving.

SOLUTION:   Improved D3QN = Double DQN + Dueling Network +
            Prioritized Experience Replay + Heuristic Exploration Policy

KEY RESULT: 51 steps (vs. 53 for DQN/DDQN) in static scene;
            ~95% success rate in dynamic scene after 20,000 training rounds.

SO WHAT:    UAVs can now learn to navigate moving threat zones
            autonomously — something no classical algorithm can do.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
5 TERMS TO KNOW
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⭐ D3QN:        Dueling Double DQN — core algorithm combining 3 DRL improvements
⭐ MDP:         Math framework: State (x,y), Action (8 dirs), Reward (+200/-50/-0.5)
⭐ PER:         Prioritized Experience Replay — trains more on worst mistakes
⭐ Heuristic:   Narrows random exploration to 5 directions biased toward target
   Dueling Net: Splits Q-value into V(state value) + A(action advantage)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
WHAT MAKES THIS PAPER UNIQUE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

• Tackles MOVING obstacle zones — not just static ones (the hard real-world case)
• Combines 4 improvements into one algorithm (DDQN + Dueling + PER + Heuristic)
• Introduces visualized action field — a new way to see what the policy learned
• Uses transfer learning: trains static first, then fine-tunes for dynamic

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
KEY NUMBERS TO REMEMBER
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Mission area: 60×60 km | Target at: (52, 52)
3 obstacle zones: radii 6 km, 10 km, 8 km
Static training: 10,000 rounds | Dynamic training: 20,000 rounds
D3QN path: 51 steps, reward 175.0
DQN path:  53 steps, reward 174.0
Dynamic success rate: ~95% (after ~12,000 rounds)
Network: Input(2) → FC(100) → FC(80) → Dueling → 8 outputs

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
QUICK Q&A
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

If asked about limitations:
→ "The environment is 2D only, obstacles move on fixed paths (not randomly),
   and there's no ablation study to isolate each improvement's contribution."

If asked what you'd change:
→ "I'd add obstacle positions to the state so the agent can reason about
   where threats are, not just react when it gets too close."

If asked about future work:
→ "Extend to 3D with altitude, test with randomly moving obstacles, and
   scale to multi-UAV coordination scenarios."

If asked why D3QN beats A*:
→ "A* replans a fixed map — it cannot handle moving obstacles. D3QN learns
   a policy that works for any state, adapting to dynamic environments."

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
REWARD FUNCTION (quick ref)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

r1 = obstacle zone penalty (−10·Ts to −50, based on danger level)
r2 = reach target → +200
r3 = exit boundary → −50
r4 = exceed 500 steps → −50
r5 = normal flight → −0.5 per step (pushes toward shorter paths)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```
