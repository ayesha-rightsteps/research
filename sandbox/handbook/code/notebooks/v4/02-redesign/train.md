# Handbook — 02-redesign/train.py (Phase 1b training)

Asal file: `code/notebooks/v4/02-redesign/train.py` · Plan: `PLAN.md`

Ek run = ek method + ek stage + ek seed. v3 ka training loop, chaar farq ke saath: naya environment aur
agent; warm start nahi (sab shuru se); training ke beech ka evaluation deterministic aur alag seed (999) pe;
aur training ke dauran saari diagnostics save hoti hain (collision ki type, safety kitni baar ON, τ obstacle
ne set kiya ya drone ne, near-misses, α khatre mein vs safe mein).

Stage 2 = 5 drones, 20 obstacles. Stage 3 = 8 drones, 40 obstacles.
`--curriculum` sirf tab jab sanity training na seekhe (pehle kam obstacles, phir dheere-dheere zyada).
