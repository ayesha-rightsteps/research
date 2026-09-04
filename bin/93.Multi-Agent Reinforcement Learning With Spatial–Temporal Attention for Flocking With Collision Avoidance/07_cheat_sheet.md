━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PAPER CHEAT SHEET
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

TITLE:    Multi-Agent Reinforcement Learning With Spatial-Temporal
          Attention for Flocking With Collision Avoidance of a
          Scalable Fixed-Wing UAV Fleet

AUTHORS:  Chao Yan, Chang Wang, Han Zhou, Xiaojia Xiang,
          Xiangke Wang, Lincheng Shen

VENUE:    IEEE Transactions on Intelligent Transportation Systems
YEAR:     2025 (published December 2024)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
THE CORE STORY (memorize this)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PROBLEM:    Fixed-wing drone fleets have no scalable RL method
            for flocking + collision avoidance with dynamic,
            variable-number non-cooperative intruders.

SOLUTION:   STAAC algorithm — uses local spatial attention to
            handle variable neighbor counts + global temporal
            attention over 4-frame history — all in a
            population-invariant network that works for any
            fleet size without retraining.

KEY RESULT: In the hardest tested scenario (10 drones, 20
            intruders), STAAC's collision rate was 0.34% —
            22.73 percentage points lower than the next-best
            method — and inference takes only 1.5 ms per drone.

SO WHAT:    Drone swarms can now be deployed with variable team
            sizes and still safely avoid dynamic threats using a
            single trained policy, enabling practical real-world
            fixed-wing UAV fleet operations.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
5 TERMS TO KNOW
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

★ STAAC: The paper's RL algorithm combining spatial + temporal
         attention for scalable UAV flocking.

★ Population-Invariant: Network that handles any number of
         agents/intruders — input size never changes.

★ Local Spatial Attention (LSA): Assigns importance weights to
         nearby entities; collapses variable count to fixed vector.

★ Global Temporal Attention (GTA): LSTM + attention over 4
         history frames; weights which past moment matters most.

★ Dec-POMDP: Math framework — agents act independently with
         only local sensor views, no global knowledge.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
KEY NUMBERS TO REMEMBER
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Sensing range R_c     = 100 m  (how far each drone can see)
Safety radius R_s     = 15 m   (collision threshold)
Alert radius R_a      = 50 m   (warning zone start)
Training: 10 followers + 15 intruders, 1200m x 800m area
Test scenarios: n5m15, n10m15, n10m20 (zero-shot)
HITL: 5 followers + 3 intruders, 100 seconds, zero collisions
Inference time: ~1.5 ms per drone on embedded hardware
Training time: ~4 hours on RTX 3080 GPU, 5000 episodes

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
WHAT MAKES THIS PAPER UNIQUE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

• FIRST RL method for scalable fixed-wing UAV flocking with
  dynamic, variable-number non-cooperative intruders

• Population-invariant architecture: same policy works for
  any fleet size — zero-shot, no retraining needed

• Dual attention: spatial (WHO matters now) + temporal
  (WHEN in the past matters) — both validated by ablation

• Validated on real flight hardware (HITL) with Pixhawk +
  X-plane 10 — near zero-shot sim-to-real transfer

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
BASELINES COMPARED AGAINST (7 methods + 2 classical)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

MADDPG      — standard multi-agent actor-critic (no attention)
MATD3       — twin-delayed MADDPG (no attention)
HAMA        — hierarchical graph attention (STAAC beats by 22.73% F)
API-MADDPG  — authors' prior work (no intruders, no entity cluster)
BCDDPG      — RL collision avoidance method
LSTM-DDQN   — discrete-action RL with LSTM
APF         — classical potential field method
ORCA        — classical reciprocal collision avoidance

STAAC WINS on all three metrics (G, F, rho-bar) in all scenarios.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ABLATION COMPONENTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

TAAC = GTA only (no LSA) -> WORST performance
SAAC = LSA only (no GTA) -> Good but STAAC beats by 29% on F
STAAC = LSA + GTA        -> BEST on all metrics

Takeaway: Spatial attention matters MORE; temporal also matters.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
QUICK Q&A
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

If asked about limitations:
→ "2D only, perfect sensing assumed, HITL only tested with 5
  followers, generalization only tested up to training fleet
  size — real outdoor flights not done."

If asked what you'd change:
→ "Test with MORE drones than trained (e.g., 20 followers),
  add sensor noise experiments, and run a full-scale HITL
  with 10 followers."

If asked about future work:
→ "Authors plan to extend to 3D environments with altitude
  control and dynamic obstacles in three dimensions."

If asked about Dec-POMDP:
→ "Each drone acts independently, sees only 100m around it —
  the Dec-POMDP formalism captures this partial observability
  and justifies the centralized-training decentralized-execution
  approach."

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ONE-SENTENCE SUMMARY TO OPEN OR CLOSE WITH
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

"STAAC uses spatial-temporal attention to give fixed-wing drone
 swarms a single scalable policy for safe formation flying
 around dynamic intruders — validated on real flight hardware
 with 22.73% better collision avoidance than the next-best
 method in the hardest tested scenario."

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
