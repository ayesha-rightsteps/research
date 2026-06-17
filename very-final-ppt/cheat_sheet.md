━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📄 ONE-PAGE CHEAT SHEET — Presentation Ke Dauran Khulla Rakho
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

TITLE: Joint Target Assignment and Conflict-Aware Collision
       Avoidance in Multi-UAV Coordination Using MAPPO with
       Priority Arbitration
STUDENT: Ayesha Khalil | CIIT/SP25-RCS-009/ATD

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CORE STORY (yeh bhool mat)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PROBLEM:  Assignment aur avoidance coupled hain — koi framework
          dono ko saath handle nahi karta.
GAP:      DA-MAPPO + IGAT-MARL dono mein reward weights FIXED
          hain — koi seekhta nahi kab kya priority deni hai.
SOLUTION: Priority Arbitration Head (PAH) — chhota neural
          network jo α ko LEARN karta hai, fix nahi karta.
FORMULA:  r_total = α × r_assignment + (1−α) × r_avoidance

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
5 NUMBERS — BOLNE KE LIYE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

90–99%   → DA-MAPPO mission success
0%       → DA-MAPPO bina assignment ke (ablation)
44%      → IGAT-MARL edge reduction
0.3/0.5/0.7 → Fixed α baselines (PAH inse compare hoga)
3,5,8    → Drones jinpe test hoga

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PAH — TECHNICAL SPEC
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Architecture: 2-layer MLP, 64 neurons
Inputs:  τ_collision (time-to-collision)
         d_target (distance to target)
         n_conflict (conflict neighbor count)
Output:  α ∈ [0,1]
Training: MAPPO actor ke saath jointly — no separate loop
Critic:  No change, zero extra parameters

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
4 RESEARCH OBJECTIVES (one-liner each)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. PAH design + implement (core mechanism)
2. Test on 3/5/8 drones (scalability)
3. Ablation: learned α vs fixed α 0.3/0.5/0.7
4. Find failure boundary (swarm size × obstacles × speed)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
IF ASKED...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Novelty?       → "Fixed weights → learned weights. PAH pehla
                  mechanism jo yeh dynamically decide karta hai."
Comparative study? → "Nahi — naya mechanism add kiya hai jo
                  kisi paper mein exist nahi karta."
Why 2D?        → "Contribution environment nahi, PAH hai.
                  DA-MAPPO/IGAT-MARL bhi 2D — fair comparison."
Falsifiable?   → "Haan — agar fixed α jeet jaaye, woh bhi valid
                  result hai."
Baselines?     → "Standard MAPPO, DA-MAPPO-2D, IGAT-MARL-fixed,
                  Unified+fixed-α (0.3/0.5/0.7)"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
WHAT NOT TO SAY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

❌ "Maine dono papers combine kiye"
✅ "Maine ek naya mechanism add kiya jo gap fill karta hai"

❌ "3D mein kar rahi hoon" (ab 2D hai — consistent raho)

❌ "Mujhe nahi pata" — kabhi mat bolo
✅ "Specific number abhi yaad nahi, lekin core concept yeh hai..."

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CLOSING LINE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

"Sir, yeh research pehli baar test karti hai ke ek learned
dynamic weighting mechanism fixed-coefficient approaches se
better hai ya nahi multi-UAV coordination mein. Thank you, sir."

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
