# Handbook — 07_literature_comparison.md

## Yeh cheez kya hai?

Humne apne results (Stage 2, Stage 3) ko do published papers ke results
se compare kiya hai — taaki pata chale humare numbers reasonable hain ya
kahi kuch galat hai.

## Do papers kaunse hain

- **`bin/91` — DA-MAPPO** — humare jaisa hi problem (multi-drone target
  assignment + collision avoidance), same metric (success%/collision%).
  Sabse zyada directly-comparable paper hai.
- **`bin/9` — IGAT-MARL** — alag metric use karta hai (reward, time,
  connections ki count), alag task bhi (discrete actions). Direct number
  se compare nahi ho sakta, lekin design lessons zaroor useful hain.

## Sabse zaroori baat — environment size alag hai

Unka test bahut zyada obstacles ke saath hota hai (30-50), aur sirf 3
drones. Humara test kam obstacles ke saath (5-10), lekin zyada drones
(5-8). Isliye **number-to-number seedha compare karna theek nahi** — sirf
context/sanity-check ke liye hai.

## Kya mila

### Stage 2 (91%) — theek dikh raha hai
DA-MAPPO ka range 90-99% hai (unke teen environments mein) — humara Stage
2 usi range ke andar hai. Reasonable hai.

### Stage 3 (74.7-74.8%) — DA-MAPPO ke sabse mushkil environment se bhi kam
Ye dhyan dene wali baat hai. Kam obstacles hone ke bawajood, humara number
unse kam hai. **Sambhavit wajah:** humare paas kam obstacles hain lekin
zyada drones — matlab shayad drone-drone takkar zyada bada issue hai,
drone-obstacle takkar nahi. Ye abhi verify nahi hua, agla check hai.

### Sabse zaroori sabak — DA-MAPPO ka apna experiment
Unhone check kiya ki agar assignment (kaunsa drone kaunsa target pakde)
hata den, success rate **seedha 0% ho jaata hai**. Ye bahut bada fark hai.
Humare α (mission vs safety balance) ka fark sirf 0.2% tha. **Matlab
assignment/conflict-graph components mein bada fark ho sakta hai, α mein
nahi** — yehi wajah hai B1/B2/B3 baselines banana ab pehle se bhi zyada
zaroori lagta hai.

## Agla kaam jo ye comparison suggest karta hai

1. Check karo Stage 3 ka collision drone-drone hai ya drone-obstacle
2. B1/B2/B3 baselines banao (already plan mein tha, ab aur zaroori lagta hai)
3. Stage 3 ke aur seeds chalao (abhi sirf ek seed hai)
