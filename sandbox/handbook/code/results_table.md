# Handbook — results-table (paper jaisi table aur graphs)

## Yeh kya hai?

Teacher ne kaha tha ki comparison base paper (DA-MAPPO) ke style mein ho. Us paper mein results **tables**
mein hote hain (Table IV, V, VI), aur saaf white-background wale bar charts. Is folder mein wahi dono
hamare models se banate hain.

Folder: `code/notebooks/v3/results-table/` — notebook `paper_style_results.ipynb`.

## Kaise kaam karta hai (simple mein)

Pehle se trained models ko **dobara train nahi karte**. Bas har model ko 200 naye episodes pe test karte
hain (jinko model ne kabhi dekha nahi), aur har model ko **bilkul same 200 episodes** dete hain, taaki
comparison fair rahe. Sirf laptop pe ~80 second lagta hai, Kaggle nahi chahiye.

Table mein wahi columns hain jo DA-MAPPO ki Table V mein hain:
- **R_success** — kitne % episodes mein sab drones target tak pahunche bina takkar ke
- **R_collision** — kitne % episodes mein takkar hui
- **R_timeout** — kitne % mein time khatam ho gaya (hamare mein 0% hai)
- **T_ave** — successful episodes mein kitne steps lage
- **L_ave** — successful episodes mein har drone ne kitna rasta tay kiya

## Kya mila

- **Fixed α, formula α, aur PAH (M) — teeno lagbhag barabar** (Stage 2 mein 87.5% se 89.5%).
- **Assignment hataane se success 72% se 51.5% ho gaya** (Stage 3) — 20 points ka bada fark, aur jo
  episodes succeed hue unmein rasta bhi lagbhag double ho gaya.
- Yani bada asar assignment ka hai, α ka nahi.

## Zaroori caveats

- Ye numbers **training ke dauran dikhne wale numbers se alag** hain (wahan random actions the aur sirf
  20 episodes). Dono ko ek hi table mein mat milana.
- Stage 3 mein sirf **ek seed** hai, isliye wahan ke claims "ek seed pe" likhne hain.
- DA-MAPPO ne observation se *target ki jaankari hata di* thi; humne target ki jaankari rakhi aur sirf
  achhi assignment ko ek fixed jodi se badla. **Dono alag experiments hain**, ek hi asar nahi.
- M aur H ka 2 point ka fark (p = 0.039) 3 comparisons ke baad pakka nahi hai — ise finding mat likhna.

## Hard words
- **Deterministic policy** — model hamesha apna sabse likely action leta hai, random nahi
- **Welch t-test** — do groups ke average mein fark asli hai ya sirf ittefaq, ye check karta hai
- **Wilson interval** — ek percentage ke aas-paas "kitna bharosa" ka range
