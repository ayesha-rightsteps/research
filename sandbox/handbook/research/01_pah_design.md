# Samjho: docs/research/01_pah_design.md

## Yeh cheez kya hai
Thesis ka **naya kaam** — Priority Arbitration Head (PAH) — ka poora design. Aur ek badi
problem jo ismein chhupi hai.

## Iski zaroorat kyun
Yehi tumhari original contribution hai. Iska design galat hua to poori thesis kamzor.
Isliye pehle ache se soch lo.

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
  - `forward()` ke andar naya tensor mat banao (gradient toot jaata hai)
  - 3 inputs 3 alag scales pe hain (seconds, distance, count) — inhe **normalize** karo
    pehle, warna network chhote wale input ignore kar deta hai

- **BADI PROBLEM — "reward hacking":**
  α reward ko banata hai, aur α agent khud decide karta hai. To agent cheat kar sakta
  hai — apna reward badha le bina achha behave kiye, bas α ko us taraf jhuka ke jahan
  reward easy hai. Agar aisa hua to α ek constant ban jayega, aur PAH = fixed-α, aur
  thesis ka point khatam.

- **4 tareeqe (formulations) soche:**
  - **A** = α reward pe (jaisa synopsis kehta hai). Simple, par hacking ka risk. Bachav:
    α pe ek "0.5 ki taraf kheencho" wala regularizer, α ko 0.1-0.9 mein clip.
  - **B** = do critic heads rakho, α **advantage** pe lagao reward pe nahi. Hacking ka
    rasta band ho jaata hai. Thoda zyada code, critic mein ek extra head.
  - **C** = α ko haath se banaye "sahi jawab" ki taraf train karo (supervised).
    Hacking nahi, par "learned" wala novelty kamzor. Ablation ke liye achha.
  - **D** = α ko actor ka ek aur output bana do. A jaisa hi risk.

- **Plan:** pehle **A** banao (synopsis se match), heavily instrument karo (α ka graph
  dekho). Agar α degenerate hota hai ya PAH fixed-α se nahi jeetta → **B** pe switch.
  Ye switch chhota change hai, rewrite nahi.

- **Thesis ke figures:** α vs time-to-collision ka graph, α vs n_conflict, ek episode
  mein α kaise badalta hai. Ye dikhate hain ki α "sahi jagah" priority switch kar raha.

## Mushkil lafz
- **Reward hacking** = reward badhana bina actually achha kaam kiye (cheating)
- **Normalize** = alag-alag scale ke numbers ko ek jaise range (0-1) mein laana
- **Regularizer** = training mein ek extra "aise mat karo" wala push (yahan: α ko 0.5 ke paas rakho)
- **Advantage** = "ye action average se kitna behtar tha" (number)
- **Critic head** = critic network ka output hissa; "two heads" = do alag values nikaalna
- **Degenerate** = solution jo technically kaam karta hai par bekaar/trivial hai
- **Instrument karna** = code mein jagah-jagah measurement/logging daalna
