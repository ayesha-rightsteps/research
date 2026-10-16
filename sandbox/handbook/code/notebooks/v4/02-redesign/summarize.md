# Handbook — 02-redesign/summarize.py (Phase 1b ki tables)

Asal file: `code/notebooks/v4/02-redesign/summarize.py`

## Yeh kya hai?
`output/eval_raw/` ki JSON files se Phase 1b ki tables aur muqable (PLAN §5 ka rule: 95% Welch CI) banata hai.
Natija: `output/eval_summary.md` aur `output/eval_per_seed.csv`.

## Rounding ka rule (16 Oct 2026)
Har seed ka success 200 mein se hota hai, is liye 10 seeds ka average aksar bilkul **x.x5** pe aata hai (jaise 74.15).
Pehle computer ki choti float ghalti tay karti thi ke 74.1 aaye ya 74.2. Ab ek saaf rule hai: **half up** (school wala) —
74.15 → 74.2, 8.55 → 8.6. Data bilkul nahi badla, sirf aakhri decimal ka rule.

## Mushkil lafz
- **Welch CI:** do methods ke average ka farq aur us ki "bharose ki range" (95%).
- **Half up:** .5 ya us se upar ho to upar round karna.
