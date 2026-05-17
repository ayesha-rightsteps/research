━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PAPER CHEAT SHEET
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

TITLE:    RALLY: Role-Adaptive LLM-Driven Yoked Navigation
          for Agentic UAV Swarms
AUTHORS:  Ziyao Wang, Rongpeng Li, Sizhao Li, Yuming Xiang,
          Haiping Wang, Zhifeng Zhao, Honggang Zhang
VENUE:    IEEE Open Journal of Vehicular Technology (OJVT)
YEAR:     2025   |   DOI: 10.1109/OJVT.2025.3610852

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
THE CORE STORY (memorize this)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PROBLEM:    A drone swarm must cover target areas in formations
            while evading an adversary and avoiding obstacles,
            with each drone seeing only its local neighborhood.

SOLUTION:   RALLY — combines LLM natural language reasoning
            for goal consensus with RMIX reinforcement learning
            for dynamic Commander/Coordinator/Executor role
            assignment, seeded by offline GPT-4o data.

KEY RESULT: RALLY achieves the highest mean reward and narrowest
            variance vs. all baselines, and generalizes to swarm
            sizes 9-11 without retraining (CIHRL collapses).

SO WHAT:    Drone swarms can now adapt roles in real time,
            reason interpretably, and deploy on onboard hardware
            via a fine-tuned 1.5B model (2.9 GB memory).

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
5 TERMS TO KNOW
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

* DS-CEFC:  Drone task — cover targets in formations while
            evading adversary and avoiding obstacles.

* RMIX:     Neural network that credits each drone's role choice
            for its contribution to team performance.

* RALLY:    The proposed hybrid LLM + MARL framework for
            drone swarm coordination with dynamic roles.

* Two-Stage Consensus: Stage 1 = individual LLM intention;
            Stage 2 = refine after neighbor communication.

* LoRA:     Fine-tunes a big model cheaply by adding tiny
            trainable layers, keeping original weights frozen.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
THREE ROLES (know these cold)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Commander:   Independent decisions, maximizes own reward.
Coordinator: Balances team and self, defers to Commander.
Executor:    Follows Coordinator's guidance, reliable.

→ 3 roles is optimal (ablation study proves this).
  Adding a 4th "Decoy" role HURTS performance.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
KEY NUMBERS TO REMEMBER
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

8 drones trained on  →  generalizes to 9, 10, 11 (CIHRL fails)
8,231 fine-tuning samples (filtered from GPT-4o data)
1.5B model  →  2.9 GB memory, 14.48s inference on RTX 4090
3^8 = 6,561 joint role combinations  →  why offline seeding needed
3 target grids tested (3x3, 2x4, 4x2)  →  all perform equally

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
WHAT MAKES THIS PAPER UNIQUE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

* First to use a credit-based mixing network (RMIX) for
  dynamic role assignment seeded by LLM offline priors —
  combining LLM knowledge with RL adaptation.

* Two-stage consensus proven mathematically superior to
  one-stage (Theorem 1 with formal proof).

* Full deployment pipeline: GPT-4o → filter 8,231 samples
  → LoRA fine-tune → 1.5B model on UAV onboard GPU.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
QUICK Q&A
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

If asked about limitations:
→ "14-second LLM inference latency, no historical memory
   in reasoning, and only qualitative SITL validation —
   no quantitative comparison vs. baselines in SITL."

If asked what you'd change:
→ "Add quantitative SITL experiments comparing RALLY vs.
   baselines in the high-fidelity simulator, and test with
   multiple adversaries to evaluate robustness."

If asked about future work:
→ "Faster inference for lightweight LLM, diversified CoT
   reasoning to avoid local optima, multimodal sensor
   fusion, and theoretical guarantees for larger swarms."

If asked how RALLY beats CoNavGPT:
→ "CoNavGPT has no online learning — RALLY adds RMIX
   role learning that adapts to the actual environment,
   giving higher mean reward and lower variance."

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
BASELINES AT A GLANCE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CIHRL:     Best MARL baseline. No roles. Stable but modest.
           Collapses on bigger swarms.
CoNavGPT:  Pure LLM planner. No training. Good reasoning
           but gets stuck in local optima.
DITTO:     LLM + fixed roles. Better than CIHRL but high
           variance due to greedy role choices.
RALLY:     LLM + dynamic roles via RMIX. Best on all metrics.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
