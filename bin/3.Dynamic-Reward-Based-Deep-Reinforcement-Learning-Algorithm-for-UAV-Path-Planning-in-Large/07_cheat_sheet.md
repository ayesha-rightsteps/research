━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📄 PAPER CHEAT SHEET
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

TITLE:    Dynamic Reward-Based Deep Reinforcement Learning
          Algorithm for UAV Path Planning in Large-Scale
          Environments
AUTHORS:  Raja Jarray*, Imen Zaghbani, Soufiene Bouallègue
VENUE:    Procedia Computer Science 270 (2025) 692–702
          KES 2025 Conference  |  YEAR: 2025
DOI:      10.1016/j.procs.2025.09.189

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
THE CORE STORY (memorize this)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PROBLEM:    Classic Q-learning can't scale to large 3D
            environments (state space explosion); metaheuristics
            get trapped in local optima and crash into obstacles.

SOLUTION:   DQN with 3D CNN + dynamic reward d3/(d1+d2) +
            input normalization — learns to navigate large
            spaces without a Q-table.

KEY RESULT: 85–98% success rate across 4 scenarios (vs.
            20–75% for metaheuristics); shortest paths and
            lowest STD in complex scenarios.

SO WHAT:    A single drone can reliably plan collision-free
            routes through large, obstacle-dense 3D environments
            without a pre-programmed map.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
5 TERMS TO KNOW
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⭐ DQN:           Neural network replaces Q-table to handle
                  large state spaces in reinforcement learning

⭐ Dynamic Reward: R = d3/(d1+d2) — rewards efficient progress
                  toward target at every step, not just on arrival

⭐ SLR:           Straightness Line Rate = actual path ÷ straight
                  distance; lower is more efficient (1.0 = perfect)

⭐ State Encoding: 3D grid representation of environment fed to
                  3D CNN instead of explicit Q-table lookup

   Dual Q-nets:   Evaluation net (learns) + Target net (frozen
                  reference) — prevents training instability

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
KEY NUMBERS TO REMEMBER
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Scenarios:  4 scenarios, 6→10→24→40 static obstacles
            7km → 14km → 20km → 25km environments

DQN Success Rate:    98% / 93% / 88% / 85%
Q-Learning SR:       95% / 85% / 80% / 70%
PSO (worst) SR:      60% / 40% / 35% / 20%

DQN Path (Sc.4):     44.466 km (mean)
Q-Learning (Sc.4):   64.195 km (31% longer!)
DQN STD (SLR Sc.4):  0.0054 vs Q-Learning 0.2054
DQN SLR (Sc.4):      1.0697 (closest to straight line)

Training:   2,000 episodes, 10,000 steps/ep, γ=0.8, ε=0.9
Network:    3D Conv (64 filters) → 3D Conv (32 filters)
            → FC(256) → FC(256) → Output(26 actions)
CT (DQN):   133–456 sec (slowest but best quality)
CT (GWO):   13–29 sec (fastest but fails in complex scenarios)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
THE DYNAMIC REWARD — HOW IT WORKS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

R = +1  → reached target
R = -1  → hit obstacle
R = d3/(d1+d2) → normal step

d1 = step size (current → next)
d2 = distance (next → target)
d3 = distance (current → target)

→ Move efficiently toward target = high reward
→ Move away from target = low reward
→ Dense feedback at every step (no sparse reward problem)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
WHAT MAKES THIS PAPER UNIQUE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

• Dynamic reward d3/(d1+d2) solves sparse reward
  problem — continuous guidance at every step

• 3D CNN processes spatial grid directly — no
  Q-table, scales to large environments

• DQN maintains >80% SR even at 40 obstacles;
  metaheuristics collapse to 20–25%

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
QUICK Q&A
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

If asked about limitations:
→ "Static obstacles only; single drone; no ablation
   study on the reward; simulation only; highest CT."

If asked what you'd change:
→ "Add an ablation testing DQN with sparse reward to
   isolate the dynamic reward's specific contribution."

If asked about future work:
→ "Parallelize DQN training to cut computational time;
   extend to multi-agent drone systems."

If asked why DQN is slow but still best:
→ "Path planning is offline pre-mission — 455 seconds
   of planning time is acceptable when alternatives
   fail 75–80% of the time."

If asked DQN vs Q-learning difference:
→ "Q-learning stores a table (impossible for large
   spaces); DQN uses a neural network to generalize
   Q-values from features — scales to any size."

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
