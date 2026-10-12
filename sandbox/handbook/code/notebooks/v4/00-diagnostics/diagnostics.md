# Handbook — diagnostics.ipynb (v3 models asal mein kya kar rahe hain)

Asal files: `code/notebooks/v4/00-diagnostics/diagnostics.ipynb` aur uska `README.md`

## Yeh kya hai?

v4 ka pehla kaam. v3 ke trained models ko sirf **padh kar** paanch sawalon ka jawab: koi training nahi,
koi model badla nahi. Laptop pe ~8 minute.

Methods ke naam (poore): **Fixed-weight MAPPO** (α hamesha 0.5), **Hand-coded τ-rule MAPPO** (α formula se,
kuch seekha nahi jata), **MAPPO + PAH** (hamara method), **MAPPO + PAH, Hungarian off** (ablation).
Stage 2 = 5 drones, 5 obstacles (5 seeds). Stage 3 = 8 drones, 10 obstacles (1 seed).

## Paanch checks aur unke jawab

### 1. Collision-type check — drones kis se takraye?
**Lagbhag hamesha obstacles se.** Stage 2 mein ~99%, Stage 3 mein 94–100%. Drone-drone takkar sirf tab aam
hui jab Hungarian assignment band kiya (97 mein se 19).

### 2. Safety-reward frequency check — safety reward kitni baar ON hota hai?
Bahut kam: har 60 se 600 drone-steps mein ek baar (0.17–1.71%), zyada tar obstacles ki wajah se.

*(Correction: pehle is se nateeja nikaala tha ke "α sirf itni hi baar matter karta hai". Woh galat tha —
safety ka **advantage** ek hi critic se banta hai aur lagbhag har step pe non-zero hota hai. Is liye
check 5 banaya.)*

### 3. α spread check — α kitna badalta hai?
- Fixed-weight MAPPO: hamesha 0.5
- Hand-coded τ-rule MAPPO: lagbhag hamesha 0.9 (kyunki khatra kam hi hota hai)
- MAPPO + PAH: 0.7–0.9, aur yeh **target ki doori** se tay hota hai, khatre se nahi (target door → α kam).
  Paanchon seeds mein yahi pattern (correlation −0.33 se −0.92).
- α lagbhag kabhi 0.5 se neeche nahi jata.

### 4. IGAT-MARL metrics check
Drones ke beech near-misses bahut kam. MAPPO + PAH aur Fixed-weight MAPPO mein koi farq nahi. Hungarian
band karne se near-misses ~4.7 guna aur conflict edges ~15 guna — yani assignment hi drones ko door rakhta
hai.

### 5. Advantage-correlation check — kya α drone ki seekhne ki direction badalta hai? (naya)
**Simple misaal:** drone ko seekhne ke liye ek "signal" milta hai — "yeh action achha tha, yeh bura".
v3 mein yeh signal do hisson (mission ka aur safety ka) ko α se mila kar banta hai.

Kya mila:
- Ek pakki math ki baat: agar normalize na karein, to `α × mission advantage + (1−α) × safety advantage`
  **bilkul wahi** hai jo plain MAPPO ka signal hota. Yani yeh milana apne aap kuch naya nahi karta.
- Asli data pe: **har method ka signal 95–100% plain MAPPO ke signal jaisa hai.** Matlab teeno methods
  asal mein lagbhag plain MAPPO ki tarah seekh rahe hain; farq sirf un kam steps pe hai jahan safety
  reward ON hota hai.
- Yeh teeno methods (Fixed-weight MAPPO, Hand-coded τ-rule MAPPO, MAPPO + PAH) ke barabar aane ki sab se saaf wajah lagti hai. Lekin yeh
  **hypothesis** hai: pakka karne ke liye plain MAPPO ko train karke compare karna padega (training = agla
  phase).

## Iska matlab (simple mein)

1. **Drones obstacles se fail ho rahe hain, aur PAH obstacles ko dekh hi nahi sakta.**
2. **α ke paas asar daalne ka raasta bahut kamzor hai** — jis tareeqe se α signal mein milaya jata hai, woh
   lagbhag plain MAPPO hi ban jata hai.
3. **Success badhane ka sab se bada raasta shayad obstacle sensing hai** (abhi 4 seedhi directions; base
   paper 35-beam LiDAR).

**Agle kadam ke raaste (faisla Ayesha, Manish, supervisor karenge):** mission aur safety ke liye do alag
value heads (taaki safety ka signal sach mein safety ka ho — Manish ka sawal, aur yeh nateeje usse support
karte hain); PAH ko obstacle ka khatra dena; LiDAR jaisi sensing; aisa setting jahan conflicts zyada hon.

## Dhyan rakhne wali baatein

- Stage 3 sirf ek seed (42) pe.
- "Training-like replay" asli training ka approximation hai (saved checkpoints ko naye seed pe dobara
  chalana).
- Notebook mein teen **gate checks** hain (purane nateeje dobara milao, collision dobara check karo, aur
  advantage ki math sahi hai ya nahi) — koi bhi fail ho to notebook ruk jata hai.
