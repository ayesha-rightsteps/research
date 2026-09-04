# Ayesha — Naya Research Direction
### Kya badla, kyun badla, aur ab kya hai

---

## Ek line mein

**Pehle:** "DA-MAPPO aur IGAT-MARL ko combine karo aur check karo."
**Ab:** "Jab dono methods ek hi drone ko alag direction mein kheenchtey hain, toh uss tension ko resolve karne ka ek **naya mechanism** propose karo jisko khud seekhna hoga."

---

## Committee ne kya issue kiya

Committee ne kaha: **"Yeh comparative study hai."**

Woh galat nahi the. Original proposal essentially yeh tha:
- Method A (DA-MAPPO) ko lo — target assignment ke liye
- Method B (IGAT-MARL) ko lo — collision avoidance ke liye
- Dono ko combine karo
- 3D mein test karo

Yeh nayi discovery nahi hai. Yeh sirf do existing methods ko naye setting mein chalana hai. MS research ke liye ek **nayi cheez** chahiye — ek aise mechanism ya idea ka, jo pehle kisi ne propose nahi kiya.

---

## Asli problem kahan thi

Apna purana problem statement dekho — isme yeh line thi:

> *"the assignment directs each drone toward its target... while the collision avoidance module forces course corrections without awareness of current assignments"*

Yeh line ek real problem point kar rahi thi. Lekin proposed solution sirf "dono ko saath daalo" tha — jis se yeh tension resolve nahi hoti, sirf ek hi jagah aa jaati hai.

**Actual research question jo koi nahi poochha:**
> Jab assignment aur avoidance ek drone ko same waqt alag direction mein kheenchhein, toh policy kaise decide karegi kaunsa objective abhi zyada important hai — aur kya yeh decision **seekha** ja sakta hai?

Kisi bhi paper mein — DA-MAPPO mein, IGAT-MARL mein, kisi mein bhi — yeh mechanism nahi hai.

---

## Naya mechanism — Priority Arbitration

**Naam:** Learned Priority Arbitration Head

**Simple explanation:**

Abhi existing papers reward likhte hain aise:

```
Total Reward = 0.5 × (assignment reward) + 0.5 × (avoidance reward)
```

Yeh weight (0.5 / 0.5) **hamesha fixed rehta hai** — chahe drone target ke qareeb ho ya collision hone waali ho. Yeh logical nahi hai.

**Naya proposal:**

```
Total Reward = α × (assignment reward) + (1 - α) × (avoidance reward)
```

Jahaan **α** fixed nahi hai. α ek chhota neural network hai jo har second decide karta hai:
- Agar collision bilkul qareeb hai → α chhota hoga → avoidance ko zyada weight milega
- Agar raasta clear hai aur target door hai → α bada hoga → assignment ko zyada weight milega

Yeh α training mein **seekha jaata hai** — hand-tune nahi kiya jaata.

**Kya chahiye isko:**
- Time-to-collision (kitne waqt mein crash ho sakta hai)
- Distance to target (target kitna door hai)
- Number of conflict neighbors (kitne drones collision course pe hain)

---

## Naya Research Direction

**Title:**
> *"Learned Priority Arbitration for Joint Target Assignment and Collision Avoidance in Multi-UAV Coordination using MARL"*

**Environment:** 2D (3D nahi — yeh change important hai, neechey explain kiya)

**Novel contribution:** Priority Arbitration Head — ek naya neural module jo reactive priority weighting karta hai, jo kisi bhi existing paper mein nahi hai.

---

## 3D se 2D kyun

- DA-MAPPO 2D mein hai. IGAT-MARL 2D mein hai. Agar 2D mein test karein toh results directly comparable hain.
- Dimensionality badlana contribution nahi hai — mechanism badlana contribution hai.
- 2D mein ablation study simple aur clean hogi.
- Sir directly pehle ke papers se compare kar sakenge.

---

## Naya Problem Statement

> Multi-UAV systems pursuing dynamic targets in shared airspace must simultaneously optimize goal-directed navigation and inter-agent collision avoidance — two objectives that generate conflicting navigation commands within a single policy when collision risk and target proximity coincide at the same decision step.

> Existing frameworks that integrate these objectives rely on fixed reward coefficients that assign constant relative weight to each objective regardless of the operational context — whether a drone is navigating open space or approaching an imminent collision. This fixed weighting forces the policy to learn a globally averaged trade-off that cannot adapt to the changing priority of each objective across different moments of flight.

> No existing framework provides a mechanism to dynamically determine, at each decision step, which objective should take priority based on real-time operational state. This work proposes a learned priority arbitration module that continuously adjusts the relative weight between assignment and avoidance rewards as a function of collision imminence, target proximity, and neighborhood conflict density.

---

## Sir se kaise baat karni hai

Agar sir poochhe "kya badla":

> *"Sir, the committee said combining two methods is comparative study — and they were right. What I am now proposing is not a combination. I am proposing a new mechanism called Priority Arbitration — a small module that decides at every decision step whether the drone should currently prioritize reaching its target or avoiding a collision. This weight is not fixed. It is learned during training. No paper in this area — not DA-MAPPO, not IGAT-MARL, not any of the 11 papers I reviewed — has this mechanism. That is the contribution."*

Agar sir poochhe "yeh novel kyun hai":

> *"Sir, all existing papers use fixed reward weights. The question no one has asked is: can this weight be learned? Should a drone approaching another drone at close range be treated the same as a drone flying alone? Our mechanism says no — and proposes a trainable component to reflect that."*

---

## Ek line summary

Contribution = ek naya module (Priority Arbitration Head) jo existing papers mein nahi hai, jo competing objectives ko real-time mein balance karta hai, jiska behavior khud seekha jaata hai.

