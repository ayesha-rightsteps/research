# Handbook — 03-base-paper-baselines/PLAN.md (Phase 2 ka plan)

Asal file: `code/notebooks/v4/03-base-paper-baselines/PLAN.md` · Abhi sirf plan hai, kuch chala nahi.

## Yeh kyun?
Phase 1b mein PAH ne Fixed-weight MAPPO ko hara diya. Ab examiner poochega: "published methods se kaisa hai?"
Base paper ke numbers seedhe compare nahi ho sakte (un ka simulator, drones, reward sab alag). Is liye
**un ke methods ko apne environment mein train karenge** — bilkul jaise base paper ne khud kiya.

## Kaun se 5 methods?
| Method | Aasaan matlab |
|---|---|
| **IPPO** | Har drone akela seekhta hai — koi "team wala critic" nahi |
| **MAPPO** | Team wala critic hai, lekin target shuru mein ek dafa assign hota hai, phir kabhi nahi badalta |
| **RMAPPO** | MAPPO + yaad-dasht (GRU) — pichle steps yaad rakhta hai |
| **DA-MAPPO (2D)** | Base paper ka apna method — har step pe Hungarian se naya assignment |
| **IGAT-style MAPPO** | Drones conflict graph pe "attention" se dekhte hain ke kaun sa padosi zyada khatarnak hai |

Pehle 4 methods ko sab teammates ki position milti hai (base paper jaise). Hamare methods ko sirf conflict
graph wale padosi milte hain.

Base paper ke do aur baselines (NavRL, EGO-Planner v2) chhod rahe hain — woh 3D ke bade systems hain, 2D mein
banana alag project jitna kaam hai. Thesis mein wajah likhenge.

## Barabari ke qaide
Sab ka environment, reward, settings, seeds (42–51), episodes (8000) same. Kisi ki alag tuning nahi.

## Asal sawal
Stage 3 pe **MAPPO + PAH vs DA-MAPPO (2D)** — hamara method vs base paper ka method. Faisla pehle wale
qaide se (95% confidence range 0 se upar → behtar).

## Waqt
Code + tests 2–3 din, training ~3 raatein, evaluation aadha din → **~1 hafta**. Pehle Manish verify karenge.

## Mushkil lafz
- **Rigid / fixed assignment:** target shuru mein ek dafa diya, phir nahi badla.
- **GRU:** neural network ka chhota hissa jo pichli baatein yaad rakhta hai.
- **Graph attention:** har drone apne padosiyon ko alag "ahmiyat" deta hai — zyada khatarnak padosi pe zyada dhyan.
