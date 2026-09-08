# Handbook — rendering.py

## Yeh file kia hai?
Yeh **visualization** file hai — iska kaam sirf yeh hai ke environment ka ek episode
**animated window mein dikha sake**.

Research ke liye zarori hai kyunke:
- Dekh sako ke drones sahi kaam kar rahe hain ya nahi
- Training ke baad dekhein — kia drones samajhdar ho gaye?
- Supervisor ko dikhao kya bana hai

## Andar kia hai?

### `run_episode(env, policy, ...)` — Ek episode chalata aur dikhata hai
- `env` = aapka environment (MultiUAVEnv)
- `policy` = drone ka brain. **Agar None diya toh random actions** — koi AI nahi
- Animated matplotlib window khulti hai

### Window mein kia dikhta hai?
| Cheez | Shape | Matlab |
|-------|-------|--------|
| Rang wale circles | 🔵🩷🟢 | Drones |
| Stars | ⭐ | Targets |
| Grey circles | ⬛ | Obstacles |
| Dotted lines | - - - | Kaun sa drone kaun sa target ki taraf ja raha hai |
| Light trails | ~~~ | Drone ka pichla raasta |
| Top text | "Step: 45" | Abhi kitna aagay gaye |
| Result text | "SUCCESS!" | Episode kaise khatam hua |

### Colors
Har drone ka apna rang hai — aur uske target ka bhi same rang hai.
Toh easily dekh sako: blue drone → blue star ki taraf ja raha hai.

## Hard words
- **Animation:** pictures jaldi jaldi badal ke video jaisi lagti hai
- **FuncAnimation:** matplotlib ka function jo animation banata hai
- **Policy:** AI ka brain — observation dalo, action milta hai
- **Trail:** pichlay positions ka raasta — dikhaata hai drone kahan kahan se gaya

## Yeh file kab use hogi?
- Har baar jab visually dekhna ho ke environment sahi kaam kar raha hai
- Training ke baad — trained drone ko dekhne ke liye
- Thesis presentation mein GIF/video banane ke liye
