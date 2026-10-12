# Handbook — v4 (naya version, kyun aur kaise)

Asal file: `code/notebooks/v4/README.md`

## Yeh kya hai?

v4 hamare kaam ka naya version hai, jo 12 October 2026 ko shuru hua. v3 ke results ne kuch aise sawal
uthaye jinka jawab v3 ke setup se nahi mil sakta tha:
- hamare numbers base papers ke numbers se fair tareeqe se compare nahi ho sakte (problem alag hai),
- base papers ne jo experiments kiye, woh hum ne apne environment mein kabhi dohraye hi nahi,
- shayad PAH ke paas "arbitrate" karne ko kuch tha hi nahi.

## Sab se bada usool: sirf utna banao jitna abhi chahiye

v3 mein bahut cheezein pehle se bana li gayi thin (docs, folders) jo baad mein badal gayin. v4 mein:
- Abhi sirf **Phase 0** (diagnostics) bana hai.
- Aage ke phases sirf **list** hain, faisle nahi. Unke folders tab banenge jab un pe kaam shuru hoga.
- Har agla faisla pichhle phase ke results dekh kar Ayesha, Manish aur supervisor milkar karenge.

| Phase | Kya | Status |
|---|---|---|
| 0 | v3 ke trained models ki jaanch (sirf padhna, koi training nahi) | ho gaya |
| 1 | Environment mein badlav? (obstacle sensing, PAH ka input, conflicts zyada) | discuss karna hai |
| 2 | Base papers ke methods hamare environment mein | discuss karna hai |
| 3 | Base papers ke experiments (density sweep, drones sweep, waghera) | discuss karna hai |

## v3 se kya seekha (folder rules)

1. **Shared code ki sirf ek copy** — `common/` folder mein. Notebooks usko import karte hain, paste nahi.
   v3 mein environment har notebook mein alag paste hota tha; ek jagah badla, doosri jagah nahi, to pata hi
   nahi chalta tha.
2. **Har phase ka folder** = `00-naam/`, jismein `README.md` (sawal, tareeqa, nateeje), notebook, aur
   `output/`.
3. **Har notebook gate check se shuru hota hai** — pehle purana jaana-pehchana nateeja dobara nikaal kar
   milao, phir naya kuch.
4. **Evaluation ka ek hi tareeqa pehle din se** — deterministic policy, 200 episodes, alag seed. Aur
   collision ki type, near-misses, edges sab saath mein record.
5. v4 kabhi `v3/` mein kuch nahi likhta.
