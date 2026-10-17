# Handbook — 05-mechanism-check (advantage check, aasaan zabaan mein)

Asal files: `code/notebooks/v4/05-mechanism-check/advantage_check.py` aur `REPORT.md` (17 Oct 2026).

## Sawal kya tha
Training mein actor ko ek "signal" milta hai jo batata hai ke ye action acha tha ya bura. Two-head methods
(Fixed-weight, τ-rule, PAH) ye signal do hisson se banate hain: mission advantage aur safety advantage, α ke saath
mila kar. Sawal: kya ye signal Plain MAPPO ke signal se waqai alag hai? Plan mein likha tha "alag hona chahiye".

## Kya kiya
80 final models (4 methods × 2 stages × 10 seeds) se training jaisi 10 batches chalayi. Koi training nahi, 1.5 minute.

## Kya mila
1. **Mission aur safety advantage alag cheezein batate hain** (correlation sirf 0.13–0.28). Do heads ka faida hai.
2. **Lekin actor ka signal Plain MAPPO jaisa hi rehta hai** (correlation 0.92–0.99). Sirf 2.5–8.7% samples par disha
   ulti hoti hai, zyada tar un steps par jahan safety reward on hai. Plan ki ummeed ("alag hona chahiye") poori nahi hui.
3. **Ajeeb baat:** PAH ka signal Plain MAPPO se *zyada* milta hai (0.98) Fixed-weight (0.92) ke muqable mein, phir bhi
   PAH sab se acha hai. Matlab ye check nahi batata ke PAH kyun behtar hai.

## Thesis mein kya likhna hai
- "PAH ka faida actor ke signal mein bara badlaav laane se nahi aata" — ye data kehta hai.
- "PAH advantage ko reshape karke kaam karta hai" — ye NAHI likhna, data iske khilaf hai.
- Do heads se critic ka seekhna bhi badalta hai; ye ek mumkin wajah hai, lekin naapi nahi gayi.

## Mushkil lafz
- **Advantage:** "ye action average se kitna behtar tha" ka number.
- **Correlation:** do cheezein saath saath kitna upar neeche hoti hain (1 = bilkul saath, 0 = koi taalluq nahi).
