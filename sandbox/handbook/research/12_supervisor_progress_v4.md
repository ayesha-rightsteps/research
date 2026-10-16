# Handbook — docs/research/12_supervisor_progress_v4.html (supervisor ke liye progress report)

Asal file: `docs/research/12_supervisor_progress_v4.html` · Online: https://claude.ai/artifact/Pxy15uSUF3q5XZkt8Vu7nd
(private — supervisor ko dikhane ke liye Share menu se share karna hoga, ya file khol kar dikhayein)

## Yeh kya hai?
12 Oct wali supervisor summary (`10_supervisor_summary_phase1.md`) ka agla hissa. English mein, taake seedha
Dr. Faisal Rehman ko dikha sakein. Is mein:
- 12 Oct ke 4 badlav kaise kiye (do value heads, PAH ke τ mein obstacles, 24-ray LiDAR, bade discs).
- Pehla PAH safety ke khilaf jhuka hua tha — wajah aur fix (ek hi baar badla, phir freeze).
- Tareeqa: same env, same settings, 10 seeds, 200 test episodes.
- **Asal natija:** Stage 3 pe MAPPO + PAH − Fixed-weight MAPPO = **+8.6 [+1.7, +15.4]**.
- Saare 9 methods ki table (RMAPPO alag, Limits mein), base paper ke saath tarteeb ka muqabla.
- Farq ke teen qadam (conflict graph +15.4, do heads +30.0, PAH +8.6).
- Checks: seed 42 hata kar bhi natija wahi; 186 evaluations dobara bilkul same; saare tests pass.
- Limits, agla plan, aur supervisor se 5 sawal.

## Dikhate waqt yaad rakhein
- Headline +8.6 hai, +53.9 nahi.
- Stage 2 pe PAH vs τ-rule abhi pakka nahi — yeh report mein saaf likha hai.
