# Samjhein: docs/research/concept.md

Poore project ko zero se, aaram se — koi jargon nahi. Sabse pehle yehi padhein.

---

## 1. Asli duniya ka problem

Socho ek earthquake aaya. Ek building gir gayi. 5 drones bheje jaate hain malbe
ke upar — har drone ko ek alag jagah pahunchna hai (jahan koi phansa ho sakta hai).

Har drone ko do cheezein ek saath karni hain:
- **Apni jagah pahunchna** (mission)
- **Kisi aur drone se ya deewar se na takrana** (safety)

## 2. Yeh dono aapas mein ladte hain

Do drone ek dusre ki taraf aa rahe hain:
- Drone sirf manzil sochta hai → seedha jaata hai → **takkar**
- Drone sirf bachne ki sochta hai → raasta chhod deta hai → **manzil door, mission fail**

To har second drone ko decide karna hai: **"abhi zyada zaroori kya — pahunchna ya bachna?"**

## 3. Abhi log kaise solve karte hain

Ek fixed number set kar dete hain. Jaise:
> "hamesha 70% dhyan manzil pe, 30% bachne pe"

Is number ka naam hai **α (alpha)**.

Problem: yeh number **kabhi badalta nahi**. Raasta khali ho tab bhi 30% bachne pe
waste. Takkar hone wali ho tab bhi sirf 30% — bahut kam. Ek hi setting har
situation ke liye — kisi ke liye bhi theek nahi baithti.

## 4. Ayesha ka idea (yehi thesis hai)

> α ko fix mat rakho. Ek chhota "dimaag" lagao jo har second khud decide kare α
> kitna ho — situation dekh ke.

Is chhote dimaag ka naam: **PAH (Priority Arbitration Head)**. Yeh 3 cheezein dekhta hai:
1. Takkar hone mein kitna time bacha hai
2. Manzil kitni door hai
3. Aas-paas kitne drone hain

Aur α upar-neeche karta rehta hai:
- Raasta khali → α ≈ 0.9 (manzil pe focus)
- Takkar kareeb → α ≈ 0.2 (bachne pe focus)
- Khatra tal gaya → wapas α ≈ 0.9

Bas yehi poora naya kaam hai — ek **knob jo apne aap ghumta hai**, ek haath se
fix kiye knob ki jagah.

## 5. "Seekhna" ka matlab kya

Drone ko koi rulebook nahi diya jaata. Wo ek video-game version hazaron baar khelta hai:
- Achha kiya (pahuncha, nahi takraya) → **+points**
- Bura kiya (takraya) → **−points**

Hazaron games ke baad wo khud pattern samajh jaata hai. Ise **reinforcement
learning** kehte hain — jaise bachcha cycle chalana seekhta hai, gir gir ke. PAH
bhi isi tarah seekhta hai ki α kab high, kab low.

## 6. Pata kaise chalega ki idea kaam karta hai

Do versions banao, same simulation mein race karao:
- **Version A:** fixed α (purana tareeqa)
- **Version B:** PAH wala self-adjusting α (naya)

Dono 200 baar chalao. Gino: kitni baar *saare* drone *bina takrae* pahunche.
- B > A → thesis ka claim sahi ✓
- B ≈ A ya kam → claim galat; honestly likho kyun (yeh bhi valid thesis hai)

## 7. Scope — yeh kya hai aur kya nahi

- Yeh ek **2D simulation** hai: flat grid pe dots. Drones = points — koi size,
  weight, hawa nahi.
- 3 se 8 drones. Jaan-boojh ke chhota.
- Koi real drone nahi, koi deployment nahi, koi user nahi. Output = ek **thesis**
  (aur shayad ek paper).
- Yeh ek chhota, well-scoped research hai — ek existing method pe ek chhota sudhaar.
  MS thesis exactly aisi hi honi chahiye.

## 8. Abhi code mein ek cheez galat hai

PAH ban gaya hai, par usko *sikhाया* kaise ja raha hai — wahan bug hai.

Abhi code PAH ko keh raha hai: *"har second dekho abhi ka reward zyada kis se
milega, α ko usi taraf ghuma do."* Yeh ek shortcut hai — drone actual mein behtar
nahi ho raha, wo bas apna score number ke saath khel ke bada raha hai.

Nateeja: α ek jagah atak jata hai (~0.1), aur PAH ek **bura fixed knob** ban jata
hai — yaani naye idea ko fair test hi nahi milta.

Fix: PAH ko "abhi ka reward" se nahi, **"poore game ke end mein kitna achha hua"**
se sikhाना. Yehi supervisor ke liye open question hai
(`04_open_questions_for_supervisor.md`, Q4–Q5) — PAH experiments se pehle ise
settle karna hai.

## Mushkil lafz

- **α (alpha)** = mission vs safety ka balance number (0 se 1)
- **PAH** = wo chhota network jo α khud set karta hai — thesis ka naya kaam
- **Reinforcement learning** = trial-and-error se seekhna (+points / −points)
- **Episode** = ek poora "game" — shuru se lekar (sab pahunch gaye YA koi takraya YA time khatam) tak
- **Baseline** = comparison ke liye rakha purana/simple version
- Baaki `handbook/glossary.md` mein
