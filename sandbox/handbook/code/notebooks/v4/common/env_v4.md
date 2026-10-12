# Handbook — env_v4.py (v4 ka naya environment)

Asal file: `code/notebooks/v4/common/env_v4.py` · Tests: `test_env_v4.py`

## Yeh kya hai?

v3 ka environment, sirf **chaar badlav** ke saath (baaki sab bilkul v3 jaisa):

1. **Gol obstacles (discs)** — radius 12, points nahi. Drone ka centre disc ke centre se 12 + 3 = 15 se kam
   ho to takkar.
2. **LiDAR** — har drone 24 rays (har 15° pe) phenkta hai, har ray batati hai ke sab se nazdeek obstacle ya
   deewar kitni door hai (100 units tak). Pehle sirf 4 seedhi directions ki doori thi.
3. **PAH ka τ ab har khatre ka** — "kitne steps mein takraunga" = drone se ya obstacle se, jo pehle ho.
   PAH ke inputs wahi 3 rehte hain.
4. **Targets obstacles se takra kar mudte hain** — taaki koi target obstacle ke andar na baith jaye.

Observation ab 50 numbers ka hai (pehle 30): apni position, speed, target ki taraf, 24 rays, 4 padosi.

## Galti se bachne ke tests (13/13 pass)

- Rays ki doori haath se hisaab ki hui value se bilkul milti hai (seedha, tircha, deewar, miss).
- Takkar bilkul 15 units pe shuru hoti hai.
- Obstacle tak pahunchne ka time haath ke hisaab se milta hai.
- Targets kabhi obstacle ke andar nahi jaate; obstacles kabhi drone ya target ke upar nahi bante.
- Same seed → same episode.
- **Sab se zaroori:** obstacles zero hon to yeh environment **v3 jaisa hi** chalta hai — rewards, assignment,
  padosi, sab. Matlab jo "unchanged" hona chahiye tha woh sach mein unchanged hai.
