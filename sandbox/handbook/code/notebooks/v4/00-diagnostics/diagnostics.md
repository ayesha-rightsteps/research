# Handbook — diagnostics.ipynb (v3 models asal mein kya kar rahe hain)

Asal files: `code/notebooks/v4/00-diagnostics/diagnostics.ipynb` aur uska `README.md`

## Yeh kya hai?

v4 ka pehla kaam. v3 ke trained models ko sirf **padh kar** chaar sawalon ka jawab: koi training nahi,
koi model badla nahi. Laptop pe ~4 minute.

## Chaar sawal aur unke jawab

### D1 — Drones kis se takraye?
**Lagbhag hamesha obstacles se.** Stage 2 mein ~99% collisions obstacle se, Stage 3 mein 94–100%.
Drone-drone takkar sirf tab aam hui jab Hungarian assignment hata diya (97 mein se 19).

### D2 — Training mein safety reward kitni baar ON tha?
**Bahut kam — har 60 se 500 drone-steps mein ek baar (0.19–1.71%), aur zyada tar obstacles ki wajah se.**
Drone-drone conflict (jo PAH dekh sakta hai) is se bhi kam: har 250 se 5000 drone-steps mein ek baar.

### D3 — α kitna badalta hai?
- B4 = hamesha 0.5
- H = lagbhag hamesha 0.9 (kyunki τ zyada tar max pe hota hai)
- M = 0.7 se 0.9 ke beech, aur yeh **target ki doori** se tay hota hai, khatre se nahi
  (target door → α ≈ 0.70, paas → α ≈ 0.89; correlation −0.92 Stage 3 mein)
- α lagbhag kabhi 0.5 se neeche nahi jata.

Matlab teeno methods asal mein teen **lagbhag fixed** weightings ki tarah behave karte hain.

### D4 — IGAT-MARL ki metrics
Drone-drone near-misses bahut kam (ek episode mein ek bhi poora pair-step nahi). M aur B4 mein koi farq
nahi. Hungarian hatane se near-misses ~4.7 guna aur edges ~15 guna — yani assignment hi drones ko door
rakhta hai.

## Iska matlab (simple mein)

1. **Drones obstacles se fail ho rahe hain, aur PAH obstacles ko dekh hi nahi sakta.** PAH ka τ input
   sirf drone-drone conflict graph se aata hai. Yeh code ki baat hai, andaza nahi.
2. **PAH ke paas arbitrate karne ko bahut kam tha.** Is liye M, H aur B4 ka tie samajh aata hai. Yeh
   hypothesis ko mazboot support karta hai, lekin pakka sabit nahi karta.
3. **Success badhane ka sab se bada raasta shayad obstacle sensing hai** — abhi drone sirf 4 seedhi
   directions ki doori dekhta hai, jabki base paper 35-beam LiDAR use karta hai.

Agle kadam (Phase 1) ka faisla Ayesha, Manish aur supervisor milkar karenge.

## Dhyan rakhne wali baatein

- Stage 3 aur training wale checks sirf ek seed (42) pe hain.
- Har checkpoint pe 50 episodes, is liye D2 ke graph mein lines upar-neeche hoti hain — asal finding
  level hai (~1% ya kam), har chhota utaar-chadhaav nahi.
- Notebook ka Cell 2 **gate check** hai: agar nayi copy v3 ke purane nateeje bilkul wahi na de, to
  notebook wahin ruk jata hai.
