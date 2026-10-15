# Handbook — 03-base-paper-baselines/REPORT.md (Phase 2 ka natija)

Asal file: `code/notebooks/v4/03-base-paper-baselines/REPORT.md` · Online: https://claude.ai/artifact/4bu8Wa31ccoxmtztcwWfAz

## Yeh kya hai?
Phase 2 ki report. Is mein hamara MAPPO + PAH base paper (DA-MAPPO) ke methods ke muqable mein dikhaya gaya hai,
dono stages par. Report English mein hai taake Manish aur supervisor ko seedha dikha sakein.

## Sab se ahem baatein
- **MAPPO + PAH dono stages mein pehle number par hai:** Stage 2 mein 86.8% aur Stage 3 mein 82.7%.
- **Asal muqabla (DA-MAPPO (2D) se):** Stage 2 mein +26.9 aur Stage 3 mein +53.8 points. Dono mein PAH pakka behtar hai.
- **Base paper jaisa pattern:** wahan DA-MAPPO apne baselines se upar tha, yahan MAPPO + PAH sab se upar hai. IPPO
  dono jagah sab se kamzor hai.
- **Farq kahan se aata hai (Stage 3):** conflict graph +15.4, do value heads +30.0, aur PAH ka apna hissa +8.5.
  Teeno hamare idea hain aur teeno ka faida dikhta hai.
- **Hadood:** sirf 2D environment hai, sab methods ki settings same rakhi gayin, Stage 2 mein τ-rule se farq pakka
  nahi, aur RMAPPO abhi baqi hai.

## Tables kaise parhein
- **Success ± number:** ± wala number batata hai ke 10 seeds mein kitna utaar chadhaao tha.
- **[a, b] wali range (CI):** agar poori range zero se upar ho to PAH pakka behtar hai. Agar range mein zero aata
  ho to abhi kuch pakka nahi keh sakte.
- **T_ave:** kitne kadmon mein sab drones apne targets tak pohanche. Kam number behtar.
- **L_ave:** har drone ne kitna raasta tay kiya. Kam number behtar.
- **D–D / D–O:** drone ki drone se takkar / drone ki obstacle se takkar.

## Mushkil lafz
- **Base paper:** wo research paper jis ke saath ham apna kaam compare kar rahe hain (DA-MAPPO).
- **Welch CI:** do methods ke average ka farq aur us ki "bharose ki range", jab dono ke seeds ka phailao alag ho.
