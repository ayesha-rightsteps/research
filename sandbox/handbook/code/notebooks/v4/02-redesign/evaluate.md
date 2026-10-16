# Handbook — 02-redesign/evaluate.py (aakhri imtehan / final evaluation)

Asal file: `code/notebooks/v4/02-redesign/evaluate.py`

## Yeh kya hai?
Har trained model ka **aakhri imtehan**. Har model ko 200 episodes chalaya jata hai, hamesha ek hi tarah
(deterministic actions, evaluation seed 7001). Is liye har method ko bilkul wahi 200 shuruaati naqshe milte hain.
Natija har model ke liye ek JSON file mein jata hai (`output/eval_raw/`).

## Kaise chalayein
- `python evaluate.py` — Phase 1b ke 100 models (hamare 5 methods).
- `python evaluate.py --phase2` — Phase 2 ke base-paper methods (IPPO, MAPPO, RMAPPO, DA-MAPPO (2D), IGAT-style MAPPO).
- **Naye options (16 Oct 2026):**
  - `--methods rmappo` — sirf yeh method(s), comma se alag.
  - `--stages 3` — sirf yeh stage(s).
  - `--raw-dir NAAM` — natije `output/NAAM/` mein, taake purane natije overwrite na hon (jaise dobara chala kar milana).
  - `--procs 6` — kitne kaam ek saath (default 4).
  - Misaal: `python evaluate.py --phase2 --methods rmappo --stages 3`

Pehle Phase 2 ki evaluation ek temporary script (scratchpad) se chali thi. Ab woh kaam isi file ke options se hota
hai, is liye "natije kis script se bane" ka jawab repo mein hai.

## Pakka kiya (16 Oct 2026)
Saare 186 models (Phase 1b 100 + Phase 2 86) dobara chalaye, alag folder mein: **186 / 186 JSON files byte-by-byte
bilkul same.** Yaani natije dobara banaye ja sakte hain.

## Mushkil lafz
- **Deterministic:** policy ka "best guess" action, bina random hilne ke — har baar same natija.
- **Evaluation seed:** woh number jo 200 shuruaati naqshe tay karta hai; training seeds se alag.
