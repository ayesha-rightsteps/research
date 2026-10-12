# Handbook — v3_registry.py (saare v3 models kahan hain)

Asal file: `code/notebooks/v4/common/v3_registry.py`

## Yeh kya hai?

v3 ke saare 18 trained models ki list — kaunsa stage, kaunsa method, kaunsa seed, aur uska folder kahan
hai — ek jagah.

- Stage 2 (5 drones, 5 obstacles): Fixed-weight MAPPO, Hand-coded τ-rule MAPPO, MAPPO + PAH × 5 seeds (42–46) = 15 models
- Stage 3 (8 drones, 10 obstacles): Fixed-weight MAPPO, MAPPO + PAH, MAPPO + PAH Hungarian off × seed 42 = 3 models

(Code ke andar inki keys abhi bhi `B4`, `H`, `M`, `M-noHungarian` hain, kyunki v3 ke data mein yahi naam hain — lekin likhte waqt hamesha poore naam.)

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
