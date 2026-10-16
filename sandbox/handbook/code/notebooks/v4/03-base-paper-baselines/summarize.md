# Handbook — 03-base-paper-baselines/summarize.py (Phase 2 report ki tables)

Asal file: `code/notebooks/v4/03-base-paper-baselines/summarize.py` (nayi, 16 Oct 2026)

## Yeh kya hai?
`REPORT.md` ki saari tables ab **ek command** se JSON files se banti hain (pehle yeh hisaab temporary tareeqe se hua
tha). Yeh Phase 1b (hamare 5 methods) aur Phase 2 (base-paper ke 5 methods) dono ki JSON padhti hai.

Banati hai (`output/eval_summary.md`):
- Table 1: success ± range, collision, timeout (dono stages); kitne seeds chale (RMAPPO: Stage 3 pe 6, Stage 2 "not run").
- Table 2: T_ave, L_ave (sirf kamyab episodes), takkarein.
- Table 3: MAPPO + PAH minus har method, 95% Welch CI ke saath.
- Farq ka breakdown: DA-MAPPO (2D) → Plain MAPPO → Fixed-weight MAPPO → MAPPO + PAH, aur DA-MAPPO (2D) − MAPPO.

## Kaise chalayein
`python summarize.py` (ya `--raw-dir NAAM` kisi doosre folder ke liye). Rounding: half up (`02-redesign/summarize.md` dekhein).

## Mushkil lafz
- **± (half-width):** 10 seeds ke average ki 95% bharose ki range ka aadha hissa.
