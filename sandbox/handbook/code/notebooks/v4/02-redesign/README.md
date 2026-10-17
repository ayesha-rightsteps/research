# Handbook — 02-redesign/README.md (Phase 1b ke final results)

Asal file: `code/notebooks/v4/02-redesign/README.md` · Scripts: `evaluate.py`, `summarize.py`, `figures.py`

## Yeh kya hai?
Phase 1b ka nateeja. 100 trained models (5 methods × 10 seeds × 2 stages) ka **final exam**: har model ko 200 naye
episodes pe chalaya, bina randomness ke (drone wahi karta hai jo us ka "best guess" hai).

## Teen scripts, teen kaam
| Script | Kaam |
|---|---|
| `evaluate.py` | Har model ko us ki apni training settings (config.json) ke saath load karta hai aur 200 episodes chalata hai. Har model ko **bilkul same 200 shuruaati halaat** milte hain (evaluation seed 7001) — is liye muqabla barabar ka hai. Har episode ka nateeja, waqt, raaste ki lambai, aur α save karta hai. |
| `summarize.py` | Tables banata hai (base paper jaise: success, collision, timeout, T_ave, L_ave) aur methods ka farq 95% confidence ke saath nikalta hai. |
| `figures.py` | Teen graphs: success/collision, waqt/raasta, aur α vs τ. |

`evaluate.py` ko pehle training wale evaluator se match karke check kiya — 4 models pe bilkul same nateeja.

## Nateeja (Stage 3 — 8 drones, 20 obstacles, asal muqabla)
| Method | Success |
|---|---|
| Plain MAPPO | 44.2% |
| Fixed-weight MAPPO | 74.2% |
| Hand-coded τ-rule MAPPO | 71.5% |
| **MAPPO + PAH** | **82.7%** |
| MAPPO + PAH (Hungarian off) | 68.4% |

- **Asal sawal ka jawab: haan.** MAPPO + PAH, Fixed-weight MAPPO se +8.6 points aage, aur 95% confidence ke
  hisaab se yeh farq 0 se upar hai (kam se kam +1.7). Stage 2 pe bhi aage (+7.0).
- **Seekha hua α, formula se behtar** (Stage 3 pe +11.3). Stage 2 pe dono barabar.
- **PAH sab se jaldi bhi pahunchta hai** — safety ke saath waqt zaya nahi hota.
- **PAH ne kya seekha:** khatre mein α ~0.13–0.19 (safety pehle), kuch na ho to ~0.81–0.85 (mission pehle), aur
  formula se **pehle** safety ki taraf mudta hai (1–2 steps door khatre pe bhi α kam).
- **Hungarian zaroori hai** ("Hungarian off" = drone i hamesha target i, koi assignment nahi): band karne se raasta ~2 guna lamba, drones aapas mein zyada takrate hain.

## Imandari wali baatein (thesis mein likhni hain)
- PAH ka fix pehle wale PAH ki ek seed ka nateeja dekh kar aaya tha. Fix ek naapi hui galti (bias) ko hatata hai —
  results dekh kar settings tune nahi ki gayin. Pehle wala flawed PAH bhi finding ke taur pe report hoga.
- Stage 3 pe seeds ka phailao bara hai, is liye confidence interval chaura hai.
- Training ke dauran wale numbers in final numbers se thode zyada the; ranking same hai. Official numbers yahi hain.

## Mushkil lafz
- **Deterministic:** drone har dafa wahi action leta hai jo network ka best guess hai — koi random tukka nahi.
- **95% Welch CI:** "asal farq kahan tak ho sakta hai" ki range. Agar poori range 0 se upar hai, to farq pakka hai.
- **T_ave / L_ave:** kamyab episodes mein pahunchne ka waqt (steps) / har drone ka chala hua raasta.
