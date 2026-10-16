# Handbook — docs/research/11_thesis_reporting_notes.md (thesis mein natije kaise likhne hain)

Asal file: `docs/research/11_thesis_reporting_notes.md` (16 Oct 2026)

## Yeh kya hai?
Ek "likhne ka rulebook": har natija thesis mein kin alfaaz mein likhna hai, taake hum data se zyada dawa na karein.
Manish ke review aur hamare fact-check se bana.

## Sab se ahem baatein
- **Asal natija:** Stage 3 pe MAPPO + PAH, Fixed-weight MAPPO se **+8.6 [+1.7, +15.4]** behtar. Hamesha range ke saath
  likhna. "Faida shayad ~2 se ~15 points ke beech" — "bahut behtar" nahi.
- **Baaki muqable "secondary" hain** (sirf upar wala pehle se tay tha). Stage 2 pe PAH vs τ-rule: abhi pakka nahi.
- **Seed 42 ka sawal:** PAH ek hi baar badla, wajah mechanism thi (performance nahi). Seed 42 hata kar bhi natija
  wahi (+7.9 [+0.7, +15.1]). Seed 42 pe to naya PAH τ-rule se neeche hai.
- **Pehla PAH (v1):** ek "finding" — policy ke gradient se seekha α safety ke khilaf jhukta hai. Us ka number sirf 1 seed.
- **Hungarian off:** matlab assignment ka koi tareeqa hi nahi (drone i → target i). Har-step re-assignment ka asar
  alag se: DA-MAPPO (2D) − MAPPO.
- **Base-paper methods:** "same environment, same budget, same settings" likhna; paper ke numbers dohraane ka dawa nahi.
- **Headline +8.6 hai, +53.9 nahi.** Farq teen qadmon mein: conflict graph +15.4, do heads +30.0, PAH +8.6.
- **RMAPPO:** main table se bahar, appendix mein wajah ke saath. 0.0 ko natija ki tarah nahi dikhana.
- **T_ave/L_ave:** sirf kamyab episodes pe — table ke neeche note zaroor.
- **Rounding:** half up (8.55 → 8.6).

## Mushkil lafz
- **Pre-registered:** run se pehle likha hua sawal aur padhne ka rule.
- **Multiple comparisons:** bahut saare muqable karne se ittefaq se "jeet" milne ka chance badhta hai; is liye sirf ek
  ko asal natija maana.
- **Ablation:** ek hissa hata kar dekhna ke us ka kitna asar tha.
