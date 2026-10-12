# Handbook — v3_registry.py (saare v3 models kahan hain)

Asal file: `code/notebooks/v4/common/v3_registry.py`

## Yeh kya hai?

v3 ke saare 18 trained models ki list — kaunsa stage, kaunsa method, kaunsa seed, aur uska folder kahan
hai — ek jagah.

- Stage 2: B4, H, M × 5 seeds (42–46) = 15 models
- Stage 3: B4, M, M without Hungarian × seed 42 = 3 models

## Kyun zaroori thi?

v3 ke folders ke naam bikhre huye thay: kahin `output`, kahin `output-seed42`, kahin `seed-43/output`.
Har baar paths dhoondhne padte thay. Ab v4 mein jo bhi v3 ka model padhta hai, isi file se padhta hai.

## Kaam ke functions

| Function | Kya karta hai |
|---|---|
| `find(stage, method, seed)` | ek model ki entry dhoondhta hai, jaise `find(3, 'M', 42)` |
| `final_model(entry)` | us model ki aakhri file (`final_model.pt`) ka path |
| `checkpoints(entry)` | training ke beech mein save hui files (har ~500 episode pe, ~15 files) |
| `check_all()` | check karta hai ke saare 18 models maujood hain; koi missing ho to wahin rok deta hai |
