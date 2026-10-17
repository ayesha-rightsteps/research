# Handbook — 04-base-paper-experiments/summarize.py (Phase 3 ki tables)

Asal file: `code/notebooks/v4/04-base-paper-experiments/summarize.py` (17 Oct 2026)
Chalane ka tareeqa: `python summarize.py` → `output/phase3_summary.md` (saari tables) aur `output/phase3_per_seed.csv`
(har model ka har setting ka ek row).

## Ye kya karta hai
Phase 3 ke run ne 2,390 JSON files banayi thi (har model × har test setting). Ye script un sab ko parh kar har
experiment ki table banata hai:
- **E5:** training wali setting pe IGAT-MARL ke metrics (LoS, edges) — sab 9 methods
- **E1:** obstacles 10/20/30/40/50 pe success, dono stages
- **E2:** chalte targets vs ruke hue targets
- **E3:** har step pe assignment vs har 50 steps baad
- **E4:** 3 se 10 drones, success + LoS + edges
- **E6:** LiDAR noise σ = 0, 0.02, 0.05, 0.1
- **E7:** ek faisle (decision step) mein kitne millisecond lagte hain

Har table ke neeche "MAPPO + PAH minus har method" ki table bhi hai, CI ke saath.

## Nishan ka matlab
- **▲** = CI poori 0 se upar → PAH behtar (pakka)
- **▼** = CI poori 0 se neeche → kam (pakka)
- **·** = CI 0 ko chhooti hai → faisla nahi hua

## Do qism ke CI — kyun?
- **Do alag methods ka farq** (PAH vs Fixed-weight): Welch CI, bilkul pehle jaisa.
- **Ek hi method, setting badalne se farq** (maslan PAH static vs moving): *paired* CI. Kyunke wahi 10 models
  dono settings mein test hue hain, to har seed ka apna farq nikal kar us ka average lete hain. Ye zyada sahih
  tareeqa hai jab cheez wahi ho aur sirf halaat badlein.

## Mushkil lafz
- **LoS (loss of separation):** do drones 3 collision-radius se zyada qareeb aa gaye — "bohat qareeb se guzarna".
  Ye takkar nahi hai, sirf khatre ki nishani hai.
- **Active edges:** conflict graph mein kitne drone-jodon ke darmiyan khatre ki line bani hui hai, har step pe.
