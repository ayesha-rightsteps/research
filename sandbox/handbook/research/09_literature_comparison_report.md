# Handbook — 09_literature_comparison_report.md

Asal file: `docs/research/09_literature_comparison_report.md`

## Yeh cheez kya hai?

Hamare results ko do base papers ke saath rakh kar dekhne wali report:
- **DA-MAPPO** (`bin/91`) — target assignment + navigation; numbers seedhe compare ho sakte hain (same
  metrics: success, collision, timeout).
- **IGAT-MARL** (`bin/9`) — sirf drones ka aapas mein collision avoidance; metrics alag (reward,
  loss-of-separation), is liye number-to-number comparison nahi.

## File mein kya hai (upar se neeche)

1. **Corrections note** — pehle ki galtiyan jo theek ki gayin (jaise "α ka asar 500× chhota" galat tha;
   sahi: ~10× chhota).
2. **Final Evaluation** — sab se zaroori hissa. Sab methods ek hi tareeqe se test: deterministic policy,
   200 episodes, alag seed.
   - Stage 2 (5 drones, 5 obstacles): Fixed-weight MAPPO 89.2%, Hand-coded τ-rule MAPPO 87.5%,
     MAPPO + PAH 89.5% — teeno barabar.
   - Stage 3 (8 drones, 10 obstacles): Fixed-weight MAPPO 73.5%, MAPPO + PAH 72.0%, Hungarian off 51.5%.
3. **PAH kahan achha kaam karta hai** — PAH khatre mein α kam (safety-first) aur safe mein α zyada
   (mission-first) karta hai, 586/586 states mein sahi direction (fig9, fig9b).
4. **Generalization** — naye, mushkil conditions mein MAPPO + PAH thoda kam gira (fig10). Ek hi run,
   chhota farq — trend, jeet nahi.
5. **Base paper ke saath seedha comparison (fig11)** — 12 Oct ko teacher ke kehne pe badla: paper ko
   "90–99%" range ki tarah nahi, **har asli value** ke saath dikhaya. Paper ki values PDF se program ke
   zariye nikaali.
6. **Neeche purane sections** — training-log wale numbers pe bane thay, "superseded" likha hai. Jahan upar
   aur neeche mein farq ho, **upar wala cite karna hai**.

## Zaroori baatein

- Paper 3 drones / 30–50 obstacles pe hai, hum 5–8 drones / 5–10 obstacles pe — **seb aur santre**.
  Comparison pattern dikhata hai, yeh nahi ke kaun behtar hai.
- `fig8_comparison_curves` (bands wala) ab use nahi karna.
- Neeche ke purane sections mein abhi bhi "90–99%" likha hai — teacher ko dene se pehle unhe hatana pending
  hai.

## v4 diagnostics ke baad (12 Oct) — is report ko kaise padhein

`code/notebooks/v4/00-diagnostics/README.md` ne dikhaya ke (1) collisions lagbhag sab obstacles se hain,
(2) PAH obstacles ko dekh hi nahi sakta, aur (3) har method asal mein lagbhag plain MAPPO ki tarah seekhta
hai. Is liye is report ka "teeno methods barabar" wala nateeja sahi hai, aur uski wajah ab zyada saaf hai.
