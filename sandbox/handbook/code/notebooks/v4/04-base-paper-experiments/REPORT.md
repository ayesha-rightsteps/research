# Handbook — 04-base-paper-experiments/REPORT.md (Phase 3 ki report, aasaan zabaan mein)

Asal file: `code/notebooks/v4/04-base-paper-experiments/REPORT.md` (17 Oct 2026)

## Kya kiya
Koi nayi training nahi. Pehle se train hue 180 models (9 methods × 2 stages × 10 seeds) ko **badli hui test
settings** mein dobara test kiya — wahi experiments jo base papers (DA-MAPPO, IGAT-MARL) ne kiye thay. Ek waqt
mein sirf ek cheez badli. Run 17 Oct raat 21:12–22:53, koi error nahi.

## Sab se ahem natija
**MAPPO + PAH ne Fixed-weight MAPPO ko 31 ki 31 settings mein pakke taur pe hara diya** (CI har jagah 0 se upar).
Matlab PAH ka faida sirf ek khaas setting ka kamaal nahi — obstacles zyada hon, targets ruke hon, drones 3 hon ya
10, sensor mein shor ho — faida rehta hai. Sab se kamzor faida 3 drones pe hai (kam drones = kam takraav = PAH ke
paas karne ko kam).

## Baaqi baatein
1. **Obstacles badhne pe** sab girte hain, tarteeb wahi. 50 obstacles pe PAH 40%, DA-MAPPO (2D) 3%.
2. **Ruke hue targets** pe sab ka natija *gira* — ye ulta lagta hai. Hamare paas iski test ki hui wajah nahi; thesis
   mein isay "observation" likhna hai, wajah ghadni nahi.
3. **Har 50 steps baad assignment:** sab 1–4 points girte hain. Real-time assignment ka faida hai, lekin chhota.
4. **Drones ki tadaad:** PAH sab se kam girta hai, IGAT-style sab se zyada.
5. **LoS (qareeb se guzarna):** PAH ka LoS Fixed-weight jitna hi hai — kam nahi. Imaandari se: PAH ka faida
   mission poora karne mein hai.
6. **Sensor noise:** kisi method pe khaas asar nahi.
7. **Waqt:** PAH faisla karne mein Fixed-weight jitna hi tez (PAH sirf training reward ke liye hai).

## Kya NAHI kehna
- Ye koi naya primary claim nahi — sab secondary hai (pehle se tay tha).
- "PAH takkar ke qareeb jaana kam karta hai" — data ye nahi kehta.
- Assignment ablation sirf test pe hai, training pe nahi.
