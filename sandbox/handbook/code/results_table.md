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
- MAPPO + PAH aur Hand-coded τ-rule MAPPO ka 2 point ka fark (p = 0.039) 3 comparisons ke baad pakka nahi hai — ise finding mat likhna.

## Base paper (DA-MAPPO) ke saath comparison — fig11 (Cell 15, 12 Oct 2026)

Teacher ne kaha tha: base paper ko graph mein kabhi "90–99%" jaisi **range** ki tarah nahi dikhate — paper
ki **asli values** plot karte hain. Isliye Cell 15 ne `fig11_actual_values_vs_paper.png` banaya:

- **Left:** DA-MAPPO ki Table V (moving targets, 3 drones) ki har asli value — 6 methods (IPPO, RMAPPO,
  MAPPO, NavRL, EGO-Planner v2, DA-MAPPO), har ek ke 3 bars (30 / 40 / 50 obstacles). Values paper ki PDF se
  program ke zariye (`pdftotext`) nikaali gayin, yaad se nahi likhi.
- **Right:** hamare methods (Fixed-weight MAPPO, Hand-coded τ-rule MAPPO, MAPPO + PAH, MAPPO + PAH
  Hungarian off), Stage 2 aur Stage 3 pe, har bar pe asli value.
- Upar success rate, neeche collision rate.

`output/table_comparison.md` mein yahi sab ek table mein hai.

**Dhyan rahe:** dono taraf ke environments alag hain (paper: 3 drones, 30–50 obstacles; hum: 5–8 drones,
5–10 obstacles). Graph pattern dikhata hai (obstacles / drones badhne pe success girti hai), "kaun jeeta"
nahi.

**Purana `fig8_comparison_curves`** paper ko 90–99% / 78–85% bands ki tarah dikhata tha — teacher ki baat
ke baad woh **superseded** hai, use mat dikhaiye.

## Hard words
- **Deterministic policy** — model hamesha apna sabse likely action leta hai, random nahi
- **Welch t-test** — do groups ke average mein fark asli hai ya sirf ittefaq, ye check karta hai
- **Wilson interval** — ek percentage ke aas-paas "kitna bharosa" ka range
