# Handbook — v4 Phase 1a: Plain MAPPO check

Asal files: `code/notebooks/v4/01-plain-mappo-check/` (`PLAN.md`, `train_runner.py`, `evaluate.ipynb`, `README.md`)

## Sawal kya tha?

Phase 0 ne dikhaya tha ke teeno v3 methods (Fixed-weight MAPPO, Hand-coded τ-rule MAPPO, MAPPO + PAH)
asal mein lagbhag **plain MAPPO** ki tarah seekhte hain. To test kiya: agar mission/safety ka milana hata
dein aur seedha plain MAPPO train karein, to kya nateeja wahi aata hai?

## Kya chalaya (laptop pe, Stage 2 = 5 drones, 5 obstacles, 5 seeds)

| Run | Kya |
|---|---|
| Fixed-weight MAPPO (laptop) | v3 ka code bilkul waisa — laptop pe dobara, taaki dono ek hi machine pe compare hon |
| Plain MAPPO | sirf **ek line** badli: drone ko seedha normal combined advantage milta hai |
| Plain MAPPO, α = 0.9 reward | upar wala, lekin reward mein mission ka weight 0.9 |

`train_runner.py` v3 ke notebook ko bina chhede chalata hai — sirf zaroori jagah badlav (seed, method,
warm-start path, aur woh ek line), har badlav ke saath check ke asli text bilkul ek hi baar mila.

## Gate checks (teeno pass)

1. Base code purane Fixed-weight notebook jaisa hi hai.
2. Runs ke code mein farq sirf ek line ka.
3. Laptop pe Fixed-weight MAPPO 88.2% aaya, Kaggle pe 89.2% tha — laptop ki training bhi utni hi achhi.

## Nateeja

- Plain MAPPO: **89.9%**, Fixed-weight MAPPO (laptop): **88.2%**, Plain MAPPO α = 0.9: **89.4%**.
- Pehle se tay rule ke hisaab se: **inconclusive**. 5 seeds ke saath CI (−1.1 se +4.5) bahut chauda hai,
  "barabar" pakka nahi keh sakte. Rule baad mein badla nahi.
- **Jo pakka keh sakte hain:** milana hatane se MAPPO **kharab nahi** hua. Yani v3 ke mission/safety milane
  ka koi fayda nahi tha. Reward weight 0.5 ya 0.9 — koi farq nahi.
- **Speed:** ek poora Stage 2 run laptop pe 11–12 minute (8 ek saath); Kaggle pe ~44 minute (ek).

## Iska matlab

PAH ko asar daalne ka mauka dene ke liye design badalna padega (Phase 1b): mission aur safety ke alag value
heads, PAH ke time-to-collision mein obstacles bhi, LiDAR jaisi sensing, aur asli size ke ghane obstacles.

## Hard words
- **Plain MAPPO** — ek hi combined reward, ek hi normal advantage; mission/safety alag nahi kiye jaate.
- **95% CI (confidence interval)** — asli farq kis range mein hone ka 95% bharosa hai. Chauda CI = data kam.
