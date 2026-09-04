# What-and-What — Konsi Cheez Kahan Se Aayi
### Source: CUI_Synopsis_AYESHA_KHALIL-SP25-RCS-009_FIXED.docx

---

## QUICK MAP — Konsa Concept Kahan Se Aaya

| Concept | Konsa Paper / Source | Kya Proof Deta Hai |
|---|---|---|
| Target assignment (Hungarian) | DA-MAPPO (Sheng et al., 2026) | 90-99% success, ablation 0% without it |
| Conflict-aware collision avoidance | IGAT-MARL (Rezaee et al., 2026) | 44% fewer edges, 17% reward gain |
| Fixed weights gap | DA-MAPPO + IGAT-MARL both | Dono mein reward coefficients constant hain |
| "Each other's future work" evidence | DA-MAPPO + IGAT-MARL | Dono papers explicitly is baat ko likhte hain |
| Curriculum learning design | DA-MAPPO + IGAT-MARL | Dono ne staged training validate ki |
| MAPPO backbone choice | Yu et al., 2022 | Cooperative MARL mein effective hona proven |
| Priority Arbitration Head | NEW — yeh research | Kisi paper mein exist nahi karta |

---

## DA-MAPPO — DETAILS

**Full Title:** Dynamic Target Assignment and Cooperative Decision-Making for UAV Swarms Based on Multi-Agent Reinforcement Learning
**Authors:** Sheng et al., 2026
**Venue:** IEEE Internet of Things Journal

**Kya karta hai:** Real-time Hungarian-algorithm assignment ko observation vector mein encode karta hai, har step pe update.

**Numbers:**
- 90-99% mission success
- Ablation: assignment hatane se success 0%
- Collision avoidance: fixed penalty constant

**Iska role is research mein:** Primary baseline for assignment. Hum DA-MAPPO ke against compare karenge.

---

## IGAT-MARL — DETAILS

**Full Title:** Efficient Multi-Agent Deep Reinforcement Learning Algorithm for Multi-UAV Collision Avoidance
**Authors:** Rezaee et al., 2026
**Venue:** Applied Soft Computing

**Kya karta hai:** Graph Attention Network use karta hai sparse conflict graph pe — sirf collision-course pairs connect hote hain.

**Numbers:**
- 44% fewer interaction edges
- 17% higher cumulative reward vs baseline
- 10% fewer separation violations
- Fixed reward weights throughout

**Iska role is research mein:** Primary baseline for avoidance.

---

## KONSA SENTENCE KAHAN SE SUPPORT MILTA HAI

**"Assignment aur avoidance coupled hain"**
→ DA-MAPPO khud kehta hai: assignment ke baghair path planning "brittle" ho jaati hai

**"Dono papers ek doosre ko future work kehte hain"**
→ DA-MAPPO: collision avoidance future work
→ IGAT-MARL: target allocation future work

**"Fixed weights — no coordinated mechanism"**
→ DA-MAPPO: collision penalty = fixed constant
→ IGAT-MARL: P1, P2 = fixed constants
→ Dono ke numbers se proven, koi naya paper nahi chahiye

---

## ESSENTIAL — KYA NAYA HAI, KYA EXISTING SE AAYA

| Component | Source | Status |
|---|---|---|
| MAPPO backbone | Yu et al. 2022 + DA-MAPPO | Existing, adopted |
| Hungarian assignment | DA-MAPPO | Existing, adopted |
| Conflict graph | IGAT-MARL | Existing, adopted |
| 4-element observation vector | Combination of both | Existing, combined |
| **Priority Arbitration Head** | **This research** | **NEW — core contribution** |
| Learned α mechanism | This research | **NEW — core contribution** |
| Ablation: learned vs fixed α | This research | **NEW — research question** |

---

## EK LINE MEIN PURA PICTURE

> "DA-MAPPO ne assignment solve kiya, IGAT-MARL ne avoidance solve kiya — dono fixed weights ke saath. Main inhe combine nahi kar rahi, main ek naya mechanism add kar rahi hoon — Priority Arbitration Head — jo dono ke beech ka balance LEARN karta hai, instead of fixing it."
