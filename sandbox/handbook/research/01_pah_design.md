# Samjhein: docs/research/01_pah_design.md

## Yeh cheez kya hai
Thesis ka **naya kaam** — Priority Arbitration Head (PAH) — ka poora design. Aur ek badi
problem jo ismein chhupi hai.

## Iski zaroorat kyun
Yehi aapki original contribution hai. Iska design galat hua to poori thesis kamzor.
Isliye pehle ache se sochiye.

## Main baatein

- **PAH kya hai:** ek chhota network (bas 2 layers). Input 3 numbers:
  1. `τ_collision` — kitni der mein takkar (chhota = khatra kareeb)
  2. `d_target` — target kitna door
  3. `n_conflict` — kitne drones kareeb hain
  Output: `α` (0 se 1). α batata hai abhi kitna focus mission pe, kitna safety pe.

- **Purane papers mein α fixed hota hai** (jaise hamesha 0.5). PAH isko har step pe
  situation dekh ke badalta hai. **Yehi novelty hai.**

- **Code ki galtiyan jo guide mein thi, humne theek ki:**
  - Network ko ek saath poora batch (`[B, 3]`) dena, ek-ek number nahi
  - `forward()` ke andar naya tensor mat banayein (gradient toot jaata hai)
  - 3 inputs 3 alag scales pe hain (seconds, distance, count) — inhe **normalize** karein
    pehle, warna network chhote wale input ignore kar deta hai

- **BADI PROBLEM — "reward hacking":**
  α reward ko banata hai, aur α agent khud decide karta hai. To agent cheat kar sakta
  hai — apna reward badha le bina achha behave kiye, bas α ko us taraf jhuka ke jahan
  reward easy hai. Agar aisa hua to α ek constant ban jayega, aur PAH = fixed-α, aur
  thesis ka point khatam.

- **4 tareeqe (formulations) soche:**
  - **A** = α reward pe (jaisa synopsis kehta hai). Simple, par hacking ka risk. Bachav:
    α pe ek "0.5 ki taraf kheencho" wala regularizer, α ko 0.1-0.9 mein clip.
  - **B** = do critic heads rakhein, α **advantage** pe lagayein reward pe nahi. Hacking ka
    rasta band ho jaata hai. Thoda zyada code, critic mein ek extra head.
  - **C** = α ko haath se banaye "sahi jawab" ki taraf train karein (supervised).
    Hacking nahi, par "learned" wala novelty kamzor. Ablation ke liye achha.
  - **D** = α ko actor ka ek aur output bana do. A jaisa hi risk.

- **Plan:** pehle **A** banayein (synopsis se match), heavily instrument karein (α ka graph
  dekhein). Agar α degenerate hota hai ya PAH fixed-α se nahi jeetta → **B** pe switch.
  Ye switch chhota change hai, rewrite nahi.

- **Thesis ke figures:** α vs time-to-collision ka graph, α vs n_conflict, ek episode
  mein α kaise badalta hai. Ye dikhate hain ki α "sahi jagah" priority switch kar raha.

- **Update (2026-09-16) — ek real problem mili aur fix ki:** Option B ban gaya (do
  advantage streams, ek shared critic) — hacking ka seedha rasta band ho gaya. Lekin
  8000-episode run check karne pe pata chala ek dusri, chhoti problem hai: α ka sirf
  "0.5 ki taraf kheencho" wala regularizer tha, jo **direction** kuch nahi batata —
  sirf collapse rokta hai. Isliye jahan danger tha wahan bhi α kabhi-kabhi **ulti**
  taraf (mission-focus) ja raha tha, kyunki safety-advantage danger mein aksar zyada
  negative hoti hai aur loss ise "avoid" karne ki koshish karta hai. **Fix:** regularizer
  ab τ (time-to-collision) ke hisaab se target rakhta hai — danger mein α ko low ki
  taraf kheenchta hai, safe mein high ki taraf — na ki hamesha 0.5. Ye Option C nahi
  bana (jahan α sirf formula copy karta) — policy gradient abhi bhi α ko train karta
  hai, ye regularizer sirf ek soft nudge hai. Agla Kaggle run isko verify karega.

- **Update (2026-09-17) — pehla fix kaam nahi kiya, dusra kiya:** Pehla fix (upar)
  Kaggle pe test kiya — kaam nahi kiya, wahi ulti-direction problem (58%) waisi hi
  rahi. Wajah: naya regularizer bhi actor-loss se 10-20x kamzor tha, aur danger
  wale moments training data ka bahut chhota hissa hote hain — isliye average mein
  dab jaate the. **Dusra fix:** regularizer ab danger-close samples ko zyada
  "weight" deta hai (jitna zyada khatra, utna zyada zor), safe samples ko kam.
  Ye Kaggle pe test kiya — **is baar kaam kiya**: 14 mein se 14 danger-close
  samples mein α sahi direction mein gaya (pehle 11/19 ulta tha). Success bhi
  thoda behtar (91.2% vs 89.7%), collision thoda kam (8.8% vs 10.3%). **Abhi bhi
  single seed hai** — pakka verdict ke liye multi-seed chahiye, lekin ye pehli
  baar hai jab PAH ka core idea (danger mein safety ki taraf jhukna) genuinely
  kaam karta dikha, sirf hope nahi.

## Mushkil lafz
- **Reward hacking** = reward badhana bina actually achha kaam kiye (cheating)
- **Normalize** = alag-alag scale ke numbers ko ek jaise range (0-1) mein laana
- **Regularizer** = training mein ek extra "aise mat karein" wala push (yahan: α ko 0.5 ke paas rakhein)
- **Advantage** = "ye action average se kitna behtar tha" (number)
- **Critic head** = critic network ka output hissa; "two heads" = do alag values nikaalna
- **Degenerate** = solution jo technically kaam karta hai par bekaar/trivial hai
- **Instrument karna** = code mein jagah-jagah measurement/logging daalna
