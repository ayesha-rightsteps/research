━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PAPER CHEAT SHEET
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

TITLE:    Deep Reinforcement Learning-Based Adaptive Collision
          Avoidance Method for UAV in Joint Operational Airspace

AUTHORS:  Yan Shen, Xuejun Zhang, Yan Li, Weidong Zhang
          (Beihang University, Beijing, China)

VENUE:    Defence Technology (journal) | YEAR: 2026

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
THE CORE STORY (memorize this)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PROBLEM:    UAVs cannot avoid collisions in mixed manned/unmanned
            military airspace when communication is down and wind
            adds uncertainty — existing methods fail here.

SOLUTION:   HPER-D3QN: a deep reinforcement learning system using
            smart threat prioritization (DTPA) + hierarchical
            experience replay (HPER) + D3QN network backbone.

KEY RESULT: 96.28% success rate with 25 aircraft (vs 91.84% DQN);
            95.06% at max uncertainty (vs 86.93% DQN);
            Ablation: removing HPER drops success by 9.27%.

SO WHAT:    Military UAVs can autonomously dodge both manned jets
            and other drones in chaotic battle airspace without
            needing any communication link or human intervention.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
5 TERMS TO KNOW
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

* HPER:   Hierarchical Prioritized Experience Replay — sorts training
          memories into 3 layers; critical events sampled most often.

* DTPA:   Dynamic Threat Prioritization Assessment — scores each
          nearby aircraft using time, distance, and type to find
          the true biggest threat per sensor sector.

* D3QN:   Double-Dueling Deep Q-Network — neural network backbone
          combining two DQN improvements for stable Q-value learning.

  TCPA:   Time to Closest Point of Approach — seconds until two
          aircraft are nearest; small TCPA = imminent collision risk.

  FHP:    Frequency of Hazardous Proximity — near-miss rate per
          episode; HPER-D3QN keeps this lowest of all methods.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
WHAT MAKES THIS PAPER UNIQUE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

 - First to combine heterogeneous aircraft types (manned + UAV),
   partial observability, AND dynamic wind uncertainty all at once
   in a DRL collision avoidance system.

 - HPER is a novel experience replay design that outperforms both
   standard PER and uniform replay — proven by ablation (9.27% gap).

 - Validated on a high-fidelity Unity3D 3D battlefield platform,
   not just the training simulator — shows generalization capability.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
KEY NUMBERS TO REMEMBER
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  96.28% — HPER-D3QN success rate, 25 aircraft
  91.84% — DQN success rate, 25 aircraft (worst baseline)
  95.06% — HPER-D3QN success rate, max uncertainty (Level 5)
  86.93% — DQN success rate, max uncertainty (worst baseline)
   9.27% — success rate drop when HPER removed (ablation)
  87.26% — FHP increase when HPER removed (ablation)
  30,000 — training episodes
      45  — observation vector dimension (input to network)
       9  — discrete maneuver actions
       8  — detection sectors around the UAV

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DTPA THREAT SCORE FORMULA
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  S = 0.4 × TCPA_normalized + 0.4 × DCPA_normalized + 0.2 × κ

  κ = 0.75 for manned aircraft (more dangerous)
  κ = 0.25 for unmanned aircraft (less dangerous)
  Highest S in each sector = the "intruder" the UAV watches

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
HPER PRIORITY LAYERS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  HIGH priority (4,000 buffer): collision, arrival, boundary violation
  MEDIUM priority (6,000 buffer): entering warning zone
  LOW priority (10,000 buffer): safe cruise (no threats detected)

  Within each layer: sample by TD error (bigger error = more samples)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
REWARD FUNCTION VALUES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Reach destination:     +2.0  (strong positive)
  Collision:             -1.0  (strong penalty)
  Enter warning zone:    -0.5  (moderate penalty)
  Exit airspace:         -0.5  (moderate penalty)
  Each time step:        -0.005 (efficiency pressure)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
QUICK Q&A
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

If asked about limitations:
→ "All experiments are in 2D simulation — no real hardware tested
   yet, and other aircraft follow fixed plans rather than reacting
   intelligently to the UAV."

If asked what you'd change:
→ "I would extend to 3D space and model the other aircraft as
   reactive agents with their own decision-making systems."

If asked about future work:
→ "Hardware-in-the-loop semi-physical simulations and real flight
   tests under the Live-Virtual-Constructive (LVC) framework,
   focusing on the sim-to-real transfer mechanism."

If asked why HPER beats PER:
→ "PER uses only TD error for prioritization. HPER adds a
   hierarchical scenario classification layer on top — ensuring
   rare but critical events (collisions, arrivals) are sampled
   more frequently regardless of their TD error value."

If asked about the action space:
→ "9 discrete actions: 3 speed adjustments (decrease/maintain/
   increase by 5 m/s) times 3 heading rates (left 3 deg/s,
   straight, right 3 deg/s)."

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
IF YOU BLANK ON SOMETHING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Say: "The paper reports that specifically in the experimental
results — the key finding is that HPER-D3QN consistently
outperforms all baselines, with HPER being the most critical
component as shown by the ablation study."

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
