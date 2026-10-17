# Handbook — 04-base-paper-experiments/figures.py (Phase 3 ke graphs)

Asal file: `code/notebooks/v4/04-base-paper-experiments/figures.py` (17 Oct 2026)
Graphs: `output/figures/` — PNG (slides) aur SVG (thesis). Dobara banane ke liye: `python figures.py`.

Rang: **neela = MAPPO + PAH**, narangi = Fixed-weight MAPPO, hara = Hand-coded τ-rule MAPPO, peela = IGAT-style MAPPO,
gulabi = DA-MAPPO (2D). Baaqi methods grey dashed lines (legend mein naam). Halka rang wala patta = 95% CI.
Dotted khadi line "trained" = jis setting pe model train hua tha.

| Graph | Kya dikhata hai | Ek line mein samjhayein |
|---|---|---|
| p3_fig1_density | Obstacles badhne pe success | "Sab girte hain, lekin tarteeb wahi rehti hai — PAH har density pe sab se upar" |
| p3_fig2_pah_lead | PAH − Fixed-weight, har Phase 3 setting mein | "31 mein se 31 settings mein CI 0 se upar — PAH ka faida ek setting tak mehdood nahi" |
| p3_fig3_static | Chalte vs ruke hue targets | "Ajeeb baat: ruke targets pe sab ka natija girta hai; PAH sab se kam girta hai" |
| p3_fig4_assign50 | Har step vs har 50 steps baad assignment | "Kam assignment se sab thoda (1–4 points) girte hain — real-time assignment ka thoda faida" |
| p3_fig5_swarm | 3 se 10 drones pe success | "PAH sab se kam girta hai (90 → 80), IGAT-style sab se zyada (77 → 33)" |
| p3_fig6_swarm_los | Drones badhne pe LoS | "IGAT-style ke drones bohat qareeb se guzarte hain; PAH aur Fixed-weight ka LoS takreeban barabar" |
| p3_fig7_noise | LiDAR mein shor (noise) | "Lines takreeban seedhi — koi bhi method noise se zyada pareshan nahi" |
| p3_fig8_timing | Ek faisle ka waqt | "PAH aur Fixed-weight barabar (0.05 ms); IGAT-style ~6 guna slow, phir bhi bohat tez" |

## Dhyaan rakhein
- Training wali setting ke ilawa har setting "generalisation test" hai — sab methods ka girna normal hai.
- LoS ka graph honestly dikhata hai ke PAH ka faida **success** mein hai, kam qareeb guzarne mein nahi.
- Timing laptop pe naapi hai; asal number machine pe depend karta hai, sirf rukh (trend) maayne rakhta hai.
