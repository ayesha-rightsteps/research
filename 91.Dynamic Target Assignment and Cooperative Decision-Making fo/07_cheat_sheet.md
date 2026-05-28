# PAPER CHEAT SHEET
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

TITLE:    Dynamic Target Assignment and Cooperative
          Decision-Making for UAV Swarms Based on
          Multi-Agent Reinforcement Learning

AUTHORS:  Yuanyuan Sheng, Xianan Xie, Huanyu Liu, Junbao Li

VENUE:    IEEE Internet of Things Journal  |  YEAR: 2026

DOI:      10.1109/JIOT.2026.3686066

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
THE CORE STORY (memorize this)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PROBLEM:    UAV swarms fail to coordinate when targets move
            because existing methods decouple assignment
            from navigation and can't update in real time.

SOLUTION:   DA-MAPPO — solve target assignment at EVERY
            decision step using a Hungarian algorithm and
            embed the result into each drone's observation,
            so the navigation policy is always conditioned
            on its current assigned target.

KEY RESULT: 90–99% mission success in dynamic environments
            with up to 50 obstacles; only ~2% drop vs. static
            targets; baselines degrade by 20–34 percentage
            points under the same conditions.

SO WHAT:    Drone swarms can now adapt to moving targets in
            real time, on edge hardware, with no central
            controller — a critical step toward practical
            IoT-edge swarm deployment.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
5 TERMS TO KNOW
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⭐ DA-MAPPO:     Dynamic-assignment MAPPO — the proposed framework
⭐ Dec-POMDP:    Multi-agent model with partial observability
⭐ Augmented     Assignment result (distance + bearing to assigned
   State:        target) embedded into each drone's observation
⭐ CTDE:         Train centrally; deploy each agent independently
⭐ Hungarian     Classical algorithm that finds minimum-cost
   Algorithm:    one-to-one pairing (drone to target)

   MAPPO:        Multi-agent PPO with centralized critic (baseline)
   LiDAR:        35-beam laser distance sensor on each drone
   GAE:          Generalized Advantage Estimation for stable training

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
WHAT MAKES THIS PAPER UNIQUE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

• First framework to update target assignment at EVERY step
  and feed it directly into the policy observation — not
  decoupled, not periodic, not offline.

• Ablation proof: removing augmented state = 0% success.
  This is unusually strong evidence for a core design choice.

• Near-zero static-to-dynamic degradation (2% in densest
  setting vs. 20–34% for all baselines) — proves the method
  truly solves dynamic environments, not just tolerates them.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
NUMBERS TO REMEMBER
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Dynamic ENV-3 (50 obstacles, hardest):
  DA-MAPPO:  90% success  |  10% collision  |  L=19.35
  RMAPPO:    67% success  |  33% collision  |  L=24.71
  NavRL:     32% success  |  65% collision  |  L=20.91
  EGO-Plan:  43% success  |  57% collision  |  L=19.73

Ablation (w/o augmented state): 0% success — system fails
Communication test (50% loss):  94% success — barely changes
Sensor noise (sigma=0.50):      90% success — graceful drop
Target at 3 m/s (6x UAV speed): 95% success — no change!

Training: 3 million steps, 3-layer MLP (256 dim), LR=1e-5
Inference on Jetson Orin Nano (5 agents): 10.531 ms/step

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
THE 3-STAGE LOOP (what happens every step)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. PERCEIVE:   LiDAR + velocity + teammate positions
2. ALLOCATE:   Hungarian algorithm → who chases which target
3. DECIDE:     Augmented obs → neural network → fly

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
REWARD TIERS (4-tier hierarchical reward)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Tier 1 — Team:       Penalize sum of all drone-target distances
Tier 2 — Individual: Progress toward goal + arrival bonus + hover
Tier 3 — Safety:     -100 crash, -25/-10 near obstacle, -100 inter-UAV
Tier 4 — Auxiliary:  Smoothness + time step penalty + boundary

All divided by 50 for normalization.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
QUICK Q&A
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

If asked about limitations:
→ "Only tested with 3 drones; O(N^3) complexity may limit
   scaling; no real flights yet — sim-to-real is future work."

If asked what you'd change:
→ "Test with larger swarms and compare against other dynamic
   assignment MARL methods, like attention or GNN-based ones."

If asked about future work:
→ "Authors plan real-world UAV deployment for sim-to-real
   validation and communication-efficient coordination under
   stricter bandwidth constraints."

If asked why 0% without augmented state:
→ "The policy network learned to depend on the target
   information as a mandatory input — without it, agents
   have no way to know where they are supposed to go."

If asked about the Hungarian algorithm:
→ "It is a classical combinatorial algorithm, not a neural
   network. It finds the minimum-cost one-to-one matching
   between drones and targets in O(N^3) time and runs
   fresh every single decision step."

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
