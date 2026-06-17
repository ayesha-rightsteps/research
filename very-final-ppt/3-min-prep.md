# 3-Minute Prep — Sabse Crunched Version

---

## YEH 1 LINE — 10 BAAR PADHO

> **"Saare existing frameworks mein reward coefficients fixed hain — koi seekhta nahi ke abhi assignment ko priority deni hai ya avoidance ko. Priority Arbitration Head pehla mechanism hai jo yeh decision dynamically, real-time state dekh ke, seekhta hai."**

---

## PROBLEM → GAP → SOLUTION (3 lines)

1. **Problem:** Target assignment aur collision avoidance coupled hain, lekin koi framework dono ko saath handle nahi karta.
2. **Gap:** DA-MAPPO aur IGAT-MARL — dono mein fixed weights hain, dono ne ek doosre ko apna future work kaha.
3. **Solution:** Priority Arbitration Head — learned α, MAPPO ke saath jointly trained.

---

## PAH — 1 LINE

Chhota neural network (2-layer, 64 neurons) jo τ_collision, d_target, n_conflict dekh ke α decide karta hai. Formula: `r_total = α × r_assignment + (1−α) × r_avoidance`

---

## EK HI NUMBER YAAD RAKHO

**0% → 90%**: DA-MAPPO mein bina assignment ke success 0%, assignment ke saath 90-99%. Matlab assignment zaroori hai — isliye ignore nahi kar sakte, balance karna padega.

---

## EK HI Q&A

**Q: "Sirf combine kar rahe ho dono papers?"**
**A:** "Nahi sir — naya mechanism (PAH) add kiya hai jo dono papers mein exist nahi karta. Ablation se prove hoga: learned α vs fixed α (0.3, 0.5, 0.7) — agar difference aaya, PAH ka contribution real hai."

Done. Jao confidently. 💙
