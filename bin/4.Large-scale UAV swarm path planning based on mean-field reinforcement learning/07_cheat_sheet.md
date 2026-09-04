━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📄 PAPER CHEAT SHEET
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

TITLE:    Large-scale UAV Swarm Path Planning Based on
          Mean-Field Reinforcement Learning
AUTHORS:  Yaozhong ZHANG et al.,
          Northwestern Polytechnical University +
          Zhejiang Normal University
VENUE:    Chinese Journal of Aeronautics, 38(9): 103484
          YEAR: 2025   DOI: 10.1016/j.cja.2025.103484

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
THE CORE STORY (memorize this)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PROBLEM:    Standard MARL can't scale to 80+ drones —
            N-squared interactions collapse performance;
            existing mean-field methods ignore distance
            and use unrealistic global observability.

SOLUTION:   PO-WMFDDPG — mean-field DDPG where each
            drone averages only nearby neighbors
            (partial obs), weighted by multi-head
            attention (closer drones matter more).

KEY RESULT: 98% task success with 80 UAVs; >90% at
            120 UAVs; DDPG and MFDDPG both fail at
            100-120 drones. Stable to 36 NFZs.

SO WHAT:    80+ autonomous drones can coordinate,
            avoid threats, and reach targets without
            any central controller — scales where
            all competing methods break down.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
5 TERMS TO KNOW
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⭐ PO-WMFDDPG:      Partially Observable Weighted Mean
                    Field DDPG — this paper's algorithm

⭐ Mean Field:       Replace N-agent interactions with
                    one weighted average signal (ā)

⭐ Attention Weight: Learned weight — closer drones get
                    higher weight in the mean field

⭐ POMDP:           Each drone sees only neighbors within
                    communication range R_a (not all 80)

   CTDE:            Train centrally, execute locally —
                    deployed drones act independently

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
KEY NUMBERS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Environment:   500×500m battlefield, 2D horizontal
Drones:        80 (primary) → tested up to 120
NFZs:          20 (primary) → tested up to 36+
Training:      1,000 rounds, batch=128, γ=0.98, lr=0.005
Convergence:   ~700 rounds to 98% SR
State dim:     16  (4 self + 2 task + 10 threat)
Action dim:    2   (linear acc + angular acc)
Actor network: 16 → 64 → 128 → 32 → 2
Critic input:  20  (state 16 + action 2 + mean_field 2)
Attention:     4 heads, 32-dim keys/queries

SCALABILITY RESULTS (approx):
Drone Count | PO-WMFDDPG | MFDDPG  | DDPG
    80      |   ~98%     |  ~93%   | ~88%
   100      |   ~95%     |  ~88%   | ~75%
   120      |   ~91%     |  ~82%   | ~65%

NFZ ROBUSTNESS:
   20 NFZs  |   ~98%     |  ~94%   | ~90%
   36 NFZs  |   ~92%     |  ~79%   | ~62%

Moving NFZ test: 75/80 drones succeed (93.75%)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
INSTANT REWARD FORMULA
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

r_task = λ(1 − d_{t+1}/d_t) + η·cos(β_t)

d_t    = distance to target NOW
d_{t+1}= distance to target NEXT step
β_t    = angle between heading and target direction

→ Getting closer to target = positive term
→ Facing toward target = high cos(β) = positive term
→ Dense feedback at every step, not just on arrival

Also: r_goal (reach target), r_crash (hit NFZ/drone),
      r_bound (leave boundary)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
WHAT MAKES THIS PAPER UNIQUE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

• Extends mean-field RL to continuous action spaces
  (DDPG) — previous MF-RL was discrete-only

• Partial observability: mean field from neighbors
  within R_a only — realistic + computationally better

• Attention weighting: closer drones influence mean
  field more — fixes the equal-weight flaw of MFDDPG

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
QUICK Q&A
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

If asked about limitations:
→ "2D simulation only; static + pre-assigned targets;
   homogeneous drones; no hardware validation; ideal
   communication assumed."

If asked what you'd change:
→ "Compare against MAPPO or MADDPG as stronger baselines,
   and add an ablation isolating the attention contribution
   from the partial observability contribution separately."

If asked about future work:
→ "3D extension, heterogeneous swarms, communication-
   constrained testing, and hardware validation."

If asked why MFDDPG is worse than PO-WMFDDPG:
→ "MFDDPG uses global equal-weight mean field — a drone
   400m away influences the average as much as one 5m
   away. PO-WMFDDPG's attention mechanism weights nearby
   drones higher and only includes neighbors within
   communication range — a more accurate, relevant signal."

If asked how many drones fail at 80 agents:
→ "Approximately 2 out of 80 — the algorithm achieves
   ~98% success rate, meaning roughly 1-2 drones out of
   80 fail per mission on average."

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
