# Handbook — 06_pah_validation_preregistration.md

## Yeh cheez kya hai?

Ek **proposal document** — abhi tak final nahi hai, aapke (Ayesha ke) review
ka wait kar raha hai. Isme likha hai ki PAH ko test karne ka **agla tareeqa**
kya hona chahiye, taaki jo result mile wo genuinely trust-karne-layak ho.

## Iski zaroorat kyun padi?

2026-09-18 ki poori raat `prior_coef` (α ko kitna zor se formula ki taraf
khींचna hai) ke alag-alag values try kiye gaye — 0.15, phir 0.30, phir 0.45.
Har baar kuch seeds theek hote, kuch bigad jaate. Aakhir mein do problems
pakde gaye:

1. **Humne jisse tune kiya, usi pe test bhi kiya.** Seed 45 ka result
   dekh-dekh ke coefficient badla, phir usi seed 45 ko final answer mein
   bhi gin liya — ye galat tareeqa hai, kyunki isse humara result biased
   ho jaata hai.
2. **Humne apna hi banaya hua rule check karne ke liye use kiya.** PAH ko
   ek formula (τ ke hisaab se α) ki taraf khींचte the, phir "PAH ne sahi
   seekha" ka proof usi formula se match karke dete the — ye circular hai,
   isse pata nahi chalta ki PAH ne genuinely **kuch seekha** ya sirf humara
   diya hua formula copy kar liya.

## Naya plan kya kehta hai

### Teen tareeke compare karenge, do nahi

| Naam | Kya hai |
|------|---------|
| **B4** | α hamesha 0.5 (fixed, koi adaptivity nahi) |
| **H (naya)** | α seedha formula se — `τ` kam toh α kam, koi learning nahi, bas ek seedha rule |
| **M (PAH)** | H ka formula **plus** ek chhota **learned correction** — jise "residual" kehte hain |

Pehle sirf B4 aur M compare kar rahe the. **H add karna zaroori hai** —
agar M sirf H jaisa dikhta hai, toh hum kabhi nahi bata sakte ki PAH ne
kuch nayi cheez seekhi ya sirf humara diya hua formula follow kar raha
tha.

### M ka naya formula (residual design)

```
α(s) = H ka formula(τ) + PAH ka chhota correction(s)
```

Pehle poora α PAH seekhta tha. Ab α ka base part **hamesha** safe formula
se aata hai (guaranteed), aur PAH sirf ek **chhota extra correction**
seekhta hai upar se. Isse woh purana bug (kabhi-kabhi α galat direction
mein "lock" ho jaana) khatam ho jaata hai — base part kabhi khoya nahi jaa
sakta.

**Yeh PAH ke design mein ek real change hai** — isliye ye sirf Manish ka
decision nahi hai, **aapka (Ayesha ka) sign-off zaroori hai** iske liye,
project ke rule ke mutabik ("PAH ka core idea nahi badalna bina dono ke
poochhe").

### Training aur testing alag seeds pe honge

Ab se jin seeds pe hum tune karenge, unhi pe final result nahi lenge — do
alag sets honge, taaki koi bias na aaye.

### Success kaise define karenge

Sabse pehle **success rate aur collision rate** dekhenge — "danger mein α
low tha ya nahi" ab sirf ek chhota sanity-check hai, asli decision nahi.

### Pehle se likh diya hai — kab hum maan lenge ki PAH kaam nahi kar raha

Result aane se pehle hi likh diya gaya hai ki kaunsa result PAH ko "reject"
karega — taaki result dekhne ke baad hum apni definition badal na sakein.

## Aapke liye kya decide karna hai

1. Kya ye naya residual design (`α = formula + chhota correction`) theek
   lagta hai PAH ke liye?
2. Kya ye narrower claim (jo section 2 mein hai, poore `docs/research/
   06_pah_validation_preregistration.md` mein) aapko theek lagta hai?

Koi code change nahi hui hai abhi — ye sirf ek plan hai, jab aap confirm
karengi tab hi implement hoga.
