# Handbook — 03-base-paper-baselines/figures.py (Phase 2 ke graphs)

Asal file: `code/notebooks/v4/03-base-paper-baselines/figures.py` (16 Oct 2026)
Graphs: `code/notebooks/v4/03-base-paper-baselines/output/figures/` — har graph PNG (slides/Word ke liye) aur SVG
(thesis ke liye, zoom pe bhi saaf). Dobara banane ke liye: `python figures.py`.

Rang ka matlab: **neela gehra = MAPPO + PAH**, halka neela = hamare baaqi methods, grey = base-paper methods.
Base paper wale graphs (6–8) mein **ek method = ek rang dono taraf** (DA-MAPPO narangi, MAPPO hara, IPPO peela).

## Har graph kya dikhata hai — aur kaise samjhayein

| Graph | Kya dikhata hai | Ek line mein samjhayein |
|---|---|---|
| fig1_success_all_methods | 9 methods ki success, dono stages. Bar = average, kaali line = 95% CI, dots = 10 seeds | "PAH dono stages mein sab se upar, aur us ke dots ek jagah ikatthe — har training mein acha" |
| fig2_pah_vs_each_method | PAH minus har method, CI ke saath. 0 se daayein = PAH behtar | "Sirf do jagah pakka nahi (grey, Stage 2), baaqi har jagah PAH behtar; ← primary question" |
| fig3_gap_breakdown | DA-MAPPO (2D) se PAH tak teen qadam: conflict graph, do heads, PAH | "Farq teen cheezon se aata hai; PAH ka apna hissa aakhri neela tukda (+8.6)" |
| fig4_outcomes | Stage 3 episodes kaise khatam hue: kamyab / obstacle se takkar / drone se takkar / timeout | "Har method zyada tar obstacle se takra kar fail hota hai; PAH sab se kam" |
| fig5_learning_curves | Training ke dauran success (20 episodes har 100 pe) | "PAH Stage 3 pe sab se tez aur sab se upar seekhta hai" — yaad rahe: yeh training-time numbers hain, final nahi |
| fig6_ranking_vs_paper | DA-MAPPO paper (ENV-3) aur hamari Stage 3 ranking saath saath | "Paper mein unka method sab se upar, hamare mein PAH; MAPPO aur IPPO dono jagah neeche" |
| fig7_difficulty_vs_paper | Mushkil badhne pe success kaise girti hai: paper 30→50 obstacles, hamara Stage 2→3 | "Dono studies mein mushkil badhne se MAPPO/IPPO bahut girte hain, best method kam girta hai" |
| fig8_gain_over_mappo | Har method MAPPO se kitna aage: halki bars paper, gehri bars hamari (CI ke saath) | "Simulator alag hai to seedhe number nahi milate — MAPPO se farq milate hain; rukh dono jagah ek jaisa" |

## Dhyaan rakhein
- Paper ke numbers (3D Gazebo, 3 drones) aur hamare (2D, 8 drones) seedhe compare nahi hote — **tarteeb aur farq** compare hote hain. Har graph ke neeche yeh likha hai.
- RMAPPO graphs mein nahi hai (shared settings pe seekh nahi saka — report ka "RMAPPO note").
- IGAT-MARL ka paper alag task aur alag metrics use karta hai, is liye us ke saath number wala graph nahi bana.
- Rang colour-blind safe hain (validator se check kiye); halke rangon pe naam seedhe likhe hain.

## Mushkil lafz
- **95% CI:** average ki "bharose ki range". Line chhoti = natija pakka.
- **Seed:** training ka ek alag run (alag shuruaat). Har dot = ek seed.
- **Waterfall chart (fig3):** seedhiyon jaisa graph jo dikhata hai ke har qadam ne kitna joda.
