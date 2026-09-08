# Handbook — test_env.py

## Yeh file kia hai?
Environment ke **unit tests** — yeh prove karte hain ke environment sahi kaam karta hai.
AI training se pehle yeh sab pass hone chahiye.

## Tests kyun likhte hain?
Sochiye tumne ghar banaya lekin check nahi kiya ke deewarein seedhi hain, darwaza khulta hai ya nahi. Phir furniture rakh di — aur pata chala ke zameen hi tilted thi.

RL mein yahi hota hai. Agar environment mein koi bug ho aur pehle check na karein, toh MAPPO training fail hogi aur pata nahi chalega kyun. Tests yeh guarantee karte hain ke **zameen seedhi hai**.

## Kia kia test kiya?

| Test | Kia check kiya |
|------|---------------|
| `test_obs_shape` | Observation 3×10 shape mein aati hai |
| `test_reset_gives_valid_positions` | Drones aur targets world ke andar hain |
| `test_step_returns_correct_shapes` | Step ke baad sahi data milta hai |
| `test_determinism` | Same seed = same episode, hamesha |
| `test_drone_stays_inside_world` | Drone kabhi world se bahar nahi jaata |
| `test_drone_drone_collision_detected` | Do drones ek jagah hoon toh collision detect ho |
| `test_no_false_collision` | Door drones mein collision NA aaye |
| `test_obstacle_collision_detected` | Drone obstacle pe ho toh collision detect ho |
| `test_collision_gives_negative_reward` | Collision pe reward negative aaye |
| `test_closer_to_target_less_negative_reward` | Paas wale drone ko zyada reward mile |
| `test_target_reached_when_close` | Target ke paas ho toh "reached" ho |
| `test_target_not_reached_when_far` | Door ho toh "reached" na ho |
| `test_hungarian_assigns_all_drones` | Har drone ko ek unique target mile |
| `test_hungarian_obvious_case` | Simple case mein assignment obvious ho |
| `test_timeout_truncates_episode` | Max steps ke baad episode band ho |

## Result
**15/15 pass** ✅ — environment sahi kaam kar raha hai, training shuru ho sakti hai.

## Hard words
- **Unit test:** ek chota check — sirf ek kaam test karein, aur dekhein sahi hua ya nahi
- **pytest:** Python ka testing tool — tests run karta hai aur batata hai kaun pass/fail
- **Determinism:** same input = same output, hamesha — experiments repeat karne ke liye zaroori
- **assert:** "yeh sach hona chahiye" — agar nahi hua toh test fail
