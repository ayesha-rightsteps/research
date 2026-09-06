# Samjho: docs/research/04_open_questions_for_supervisor.md

## Yeh cheez kya hai
14 sawaal jo supervisor (Dr. Faisal Rehman) se poochhne hain — likhit jawab ke saath —
serious coding shuru karne se pehle.

## Iski zaroorat kyun
Approved synopsis se hum kuch cheezein change kar rahe hain. Ye chupke se nahi karna —
warna thesis defense mein "aapne synopsis mein PyBullet likha tha, use kyun nahi kiya?"
wala sawaal aayega. Abhi email pe OK le lo.

## Main baatein — sawaalon ke groups

- **A. Synopsis se deviation (written OK chahiye):**
  - Q1: PyBullet ki jagah custom 2D env — theek hai?
  - Q2: action `(vx, vy)` (DA-MAPPO ka `(speed, turn-rate)` nahi) — theek hai?
  - Q3: LiDAR ki jagah 4 direction ki doori — theek hai?

- **B. PAH ka design (sabse important):**
  - Q4: α reward pe lagao (Option A) ya advantage pe (Option B)? Hacking ka risk
    explain kiya hai.
  - Q5: Agar A fail hua to critic mein ek extra head daal sakte hain? (synopsis kehta
    hai "no extra critic params")
  - Q6: α pe regularizer (0.5 ki taraf push) daalna theek hai, ya wo "purely learned"
    ke against hai?

- **C. Assignment:** Q7 per-step vs har 50 step. Q8 doori ka square vs plain.

- **D. Conflict graph:** Q9 look-ahead time (3 sec?) aur danger distance ke values.

- **E. Evaluation:**
  - Q10: 5 seeds kaafi hai committee ke liye?
  - Q11: Stage 1 ka "DA-MAPPO replication" — kya qualitative match (mechanism helps +
    ablation collapses) kaafi hai, kyunki hamara env alag hai?
  - Q12: B3 baseline — IGAT ka idea MAPPO mein daalein, ya poora IGAT (DQN) banayein?

- **F. Scope:** Q13 moving targets — position swap ya continuous drift? Q14 curriculum
  aur max 8 drones confirm.

- **Timeline note:** synopsis "2 mahine mein env + replication" kehta hai; realistically
  month 3. Supervisor ko abhi bata do.

## Mushkil lafz
- **Deviation** = approved plan se hatna/badalna
- **Sign-off** = officially "haan theek hai" mil jaana
- **Regularizer** = training mein "aise mat karo" wala extra push
- **Qualitative match** = exact number match nahi, par "same pattern/behaviour" dikhna
- **Curriculum** = aasaan se mushkil ki taraf training stages
