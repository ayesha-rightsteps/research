# 5-Minute Prep — Presentation Se Pehle Yeh Padho

---

## TERI RESEARCH — EK PARAGRAPH

Multi-UAV missions mein har drone ko ek target assign hota hai aur saath mein collision bhi avoid karni hoti hai. Yeh dono kaam ek doosre ko affect karte hain — agar drone collision avoid karne ke liye raasta badalta hai, toh uska target reach karna mushkil ho sakta hai. Aaj tak kisi bhi framework ne yeh dono cheezein ek learned policy mein saath solve nahi ki. Maine ek naya mechanism propose kiya hai — **Priority Arbitration Head (PAH)** — jo har second decide karta hai ke abhi target ki taraf jaana zyada zaroori hai ya collision se bachna, based on real-time situation. Yeh decision **seekha jaata hai**, manually fix nahi kiya jaata — yahi sabse bada difference hai existing kaam se.

---

## 3 SENTENCES JO SAB KUCH COVER KARTE HAIN

1. **Problem:** Assignment aur avoidance coupled hain — ek dusre ko affect karte hain, lekin koi unhe saath handle nahi karta.
2. **Gap:** DA-MAPPO aur IGAT-MARL dono mein reward weights FIXED hain — koi seekhta nahi kab kya priority deni hai.
3. **Solution:** Priority Arbitration Head — chhota neural network, MAPPO ke saath jointly trained, jo α (weight) ko dynamically learn karta hai.

---

## OPENING LINE (BOLO YEH)

> "Sir, mera research address karta hai ek structural gap — target assignment aur collision avoidance multi-UAV systems mein aaj tak kisi single learned policy mein saath solve nahi hue. Main propose kar rahi hoon Priority Arbitration Head, jo dynamically decide karta hai dono ke beech balance kaise rakha jaaye."

---

## 5 NUMBERS JO BOLNE HAIN

| Number | Matlab |
|---|---|
| 90–99% | DA-MAPPO ka mission success — strong baseline |
| 0% | DA-MAPPO bina assignment ke — assignment zaroori hai |
| 44% | IGAT-MARL ka edge reduction — sparse graph effective |
| 0.3, 0.5, 0.7 | Fixed α baselines jinse PAH compare hoga |
| 3, 5, 8 | Drones jinpe test hoga |

---

## AGAR EK HI SAWAAL POOCHA JAYE

**"Tumhari research ka contribution kya hai?"**

> "Sir, mera contribution Priority Arbitration Head hai — pehla learned mechanism multi-UAV coordination mein jo dynamically decide karta hai target assignment aur collision avoidance ke beech kya priority honi chahiye, instead of fixed constants jo har existing framework use karta hai."

---

## CONFIDENCE LINE

Teri research mein clear gap hai (proven from existing papers themselves), specific naya mechanism hai (PAH), aur falsifiable question hai. Confidently jao. 💙
