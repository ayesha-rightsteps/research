# Handbook — 04-base-paper-experiments/PLAN.md (Phase 3 ka plan)

Asal file: `code/notebooks/v4/04-base-paper-experiments/PLAN.md` (17 Oct 2026) — **sirf plan, kuch chala nahi. Manish ki haan ka intezar.**

## Yeh kya hai?
Base papers jo experiments dikhate hain, wohi hamare **pehle se trained models** pe — nayi training nahi.
Sirf test ki setting badlegi, models wahi rahenge.

| # | Experiment | Kya badlega | Kis paper se |
|---|---|---|---|
| E1 | Obstacles zyada | 10, 20, 30, 40, 50 discs | DA-MAPPO (30/40/50) |
| E2 | Targets ruke hue | target ki speed 0 | DA-MAPPO |
| E3 | Assignment har 50 steps pe | har step ki jagah har 50 steps | DA-MAPPO ablation |
| E4 | Drones ki tadaad | 3 se 10 drones | IGAT-MARL |
| E5 | IGAT ke metrics | loss-of-separation, active edges | IGAT-MARL |
| E6 | Sensor mein shor (noise) | LiDAR mein thodi ghalti | robustness |
| E7 | Kitna tez | har decision ka time, 3–10 drones | — |

## Ahem baatein
- **Koi naya "asal natija" nahi** — sab secondary; jo aaye woh likhna, chahe PAH aage ho ya na ho.
- **E4 mein MAPPO, DA-MAPPO (2D), IPPO nahi** — yeh saare teammates dekhte hain, is liye doosri tadaad pe bina dobara
  training ke nahi chal sakte.
- Chhote code badlav chahiye (jaise test ke waqt critic na chalana, "har K steps" assignment, LiDAR noise) —
  default pe purane natije **bilkul same** aane chahiye (186 evaluations dobara milayenge).
- Laptop: ~3–4 ghante (sirf evaluation, darmiyana bojh). Code ~3–4 ghante.

## Mushkil lafz
- **Generalization test:** model ko us setting pe chalana jis pe woh train nahi hua — sab methods ka girna normal hai.
- **Robustness:** ghalat/shor wale input ke bawajood kitna theek kaam karta hai.
