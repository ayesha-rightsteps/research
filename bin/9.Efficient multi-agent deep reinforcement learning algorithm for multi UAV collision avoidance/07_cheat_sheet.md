```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PAPER CHEAT SHEET
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

TITLE:    Efficient Multi-Agent Deep Reinforcement Learning
          Algorithm for Multi UAV Collision Avoidance

AUTHORS:  Mohammad Reza Rezaee, Nor Asilah Wati Abdul Hamid,
          Masnida Hussin, Zuriati Ahmad Zukarnain

VENUE:    Applied Soft Computing, Vol. 197, Article 115145 (Elsevier)
YEAR:     2026

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
THE CORE STORY (memorize this)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PROBLEM:    Existing multi-UAV collision avoidance systems
            use dense interaction graphs that become noisy
            and unscalable as swarm size increases.

SOLUTION:   IGAT-MARL — build interaction edges only between
            drones currently on a collision course, then use
            a stacked graph attention network (IGAT) plus
            curriculum + transfer learning to train safely.

KEY RESULT: 17.56% higher reward, 10.52% fewer dangerous
            near-miss time steps, 43.93% fewer interaction
            edges vs. the DGN benchmark (N=5 UAVs,
            last 2000 of 10,000 training episodes).

SO WHAT:    Drones can share dense airspace safely with less
            communication — smarter attention beats more
            communication every time.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
5 TERMS TO KNOW
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

* IGAT-MARL: The full proposed algorithm — conflict graph +
             improved graph attention + curriculum learning.

* Loss of Separation (LoS): When two UAVs come closer than
             the minimum safe distance (RPZ). IGAT cuts this
             by 10.52% vs. benchmark.

* Dynamic Conflict Graph: Interaction edges built only from
             active conflict pairs (predicted collisions),
             rebuilt every decision step.

* Curriculum Learning: Train on 3 UAVs first, then
             progressively increase to 10, transferring
             weights between stages.

* Action Bias: Over-preference for one maneuver; DGN picks
             "do nothing" 48.6% of time; IGAT distributes
             actions evenly (~0.30/0.35/0.35).

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
WHAT MAKES THIS PAPER UNIQUE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

* Conflict-driven graph (not distance-threshold): edges appear
  only when a real collision course is detected, keeping
  interaction structure sparse at any swarm size.

* "Double attention" IGAT architecture: 2 GAT layers per block,
  2 blocks stacked = 4 attention passes with residual
  connections + LayerNorm for stable training on time-varying
  graphs.

* Conflict-gated execution: heading commands only sent to UAVs
  currently in a conflict — free-flying drones are not disturbed.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
KEY NUMBERS (N=5 UAVs)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

IGAT reward:      -1418 ± 48.8
DGN reward:       -1719 ± 50.5   (+17.56% for IGAT)

IGAT t_loss:       461.6 ± 5.7
DGN t_loss:        515.8 ± 4.57  (+10.52% for IGAT)

IGAT edges:        0.5245 ± 0.035
DGN edges:         0.9355 ± 0.046 (+43.93% fewer for IGAT)

At N=10: IGAT -9561 vs DGN -10385 vs MGAT -11599

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
QUICK Q&A
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

If asked about limitations:
-> "Only fixed-wing UAVs in simulation; action space limited
   to 3 heading commands; no real-world validation; no
   sensor uncertainty or communication delays modeled."

If asked what you would change:
-> "Expand the action space to include altitude and speed
   changes, and validate on real hardware with noisy sensors."

If asked about future work:
-> "The authors plan to add altitude/speed actions, include
   static/dynamic obstacles, and extend to quadrotor UAVs."

If asked how it differs from DGN:
-> "DGN does single-pass dot-product attention; IGAT uses
   four-pass GAT-style pairwise energy attention with
   residual connections and LayerNorm — more selective,
   more stable, better safety results."

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SIMULATOR + HARDWARE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Simulator:   BlueSky (open-source ATC simulator)
Aircraft:    BADA dataset from EuroControl (fixed-wing UAVs)
Hardware:    Ubuntu + NVIDIA A40 GPU
Training:    10,000 episodes, N = 3 to 10 UAVs
Actions:     3 discrete heading offsets: 0 deg, +15, -15
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```
