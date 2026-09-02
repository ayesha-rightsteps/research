# 06 — Presentation Guide: Script + Q&A

---

## Suggested Opening (word for word)

> "Good morning, sir. Today I'd like to present a paper titled 'Deep Reinforcement Learning-Based Adaptive Collision Avoidance Method for UAV in Joint Operational Airspace,' by Yan Shen, Xuejun Zhang, Yan Li, and Weidong Zhang, from Beihang University in Beijing. This was published in the journal Defence Technology in 2026.
>
> This paper addresses a critical problem in modern military aviation — how can a drone autonomously avoid collisions with other aircraft in a contested battlefield where communication is disrupted, different types of aircraft are sharing the airspace, and wind is constantly pushing everything off course? The authors propose a deep reinforcement learning algorithm called HPER-D3QN that teaches the drone to dodge threats intelligently by prioritizing the most dangerous ones first. Their results show a 96.28% success rate even in dense airspace with 25 aircraft — significantly outperforming existing methods."

---

## Main Points to Cover (in order)

### 1. THE PROBLEM

**Say:**
> "The setting is a joint operational airspace — imagine manned fighter jets and military drones flying in the same patch of sky, from different combat units, with no shared communication network. The drones cannot rely on ground systems to tell them where other aircraft are. They only have their own onboard sensors, which have limited range and noisy readings. On top of that, dynamic wind constantly pushes aircraft off their intended paths. Traditional methods — rule-based systems, optimization algorithms, even earlier deep learning approaches — all fail here because they assume either perfect information, homogeneous aircraft, or stable environments. None of those assumptions hold in a real battlefield."

---

### 2. WHY EXISTING SOLUTIONS WERE NOT ENOUGH

**Say:**
> "Previous DRL methods like DQN and Rainbow DQN showed promise, but they had three key limitations. First, they assumed all aircraft are the same type — all drones or all jets, never mixed. Second, they used simplified, unrealistic observation models. Third, their experience replay mechanisms sampled all past experiences with equal probability, wasting training time on boring 'nothing happened' moments instead of focusing on critical collision events. This paper specifically addresses all three gaps."

---

### 3. THE PROPOSED APPROACH

**Say:**
> "The authors propose HPER-D3QN — a deep reinforcement learning algorithm built on three main ideas. First, the drone's sensor range is divided into 8 sectors, and a new algorithm called DTPA identifies the most dangerous aircraft in each sector using three factors: how soon they will be closest, how close that will be, and what type of aircraft they are — because a fast manned jet is more dangerous than a slow drone at the same distance. Second, a mechanism called Hierarchical Prioritized Experience Replay sorts all training experiences into three priority layers — critical events like collisions and destination arrivals get sampled most often during training. Third, the neural network backbone is D3QN, which combines two proven improvements over basic DQN to give more accurate and stable Q-value estimates."

---

### 4. KEY METHODOLOGY

**Say:**
> "The UAV is trained in a simulated 30 kilometer by 30 kilometer battlefield airspace, containing up to 25 mixed manned and unmanned aircraft, all subject to periodic wind and individual speed and heading uncertainties. At each one-second time step, the UAV selects one of 9 possible maneuvers — combinations of three speed adjustments and three heading changes. The reward function gives strong positive rewards for reaching the destination, strong penalties for collisions and boundary violations, and smaller penalties for entering warning zones or being inefficient. After 30,000 training episodes on a TITAN RTX GPU, the trained model is tested under three conditions — varying aircraft density, varying uncertainty level, and varying ratios of manned to unmanned aircraft."

---

### 5. THE RESULTS

**Say:**
> "The results are clear and consistent across all conditions. In the hardest test — 25 aircraft in the airspace — HPER-D3QN achieves a 96.28% success rate, while the basic DQN baseline achieves only 91.84%. At the maximum uncertainty level with 25 aircraft, HPER-D3QN maintains 95.06% success while DQN drops to 86.93%. The ablation study shows that removing the HPER mechanism causes a 9.27% drop in success rate and an 87.26% surge in dangerous near-miss events — confirming it is the single most important innovation. Finally, the trained model was transferred to a high-fidelity 3D Unity engine simulation and successfully avoided two separate aircraft before reaching its mission target — demonstrating generalization beyond the training environment."

---

### 6. SIGNIFICANCE AND CONTRIBUTION

**Say:**
> "This paper makes three contributions to the field. First, it establishes a realistic joint airspace simulation that handles both aircraft type heterogeneity and dynamic wind uncertainty together — something previous work had not done. Second, the DTPA algorithm gives the UAV smarter threat awareness by considering time, distance, and aircraft type together rather than just using Euclidean distance. Third, HPER makes the training process more efficient and effective by ensuring the agent spends more time learning from the rare but critical experiences. Together, these make a UAV that is more robust, more efficient, and more deployable in real joint military airspace than any previous approach."

---

## Anticipated Questions and Model Answers

| Question Sir Might Ask | What Ayesha Should Say |
|---|---|
| **What is the main contribution of this paper?** | "There are three main contributions. First, the paper builds a realistic joint airspace simulation that includes both manned aircraft and UAVs with dynamic wind and individual state uncertainty. Second, the DTPA algorithm identifies the most dangerous aircraft in each detection sector using three factors — time to closest approach, distance at closest approach, and aircraft type — rather than just Euclidean distance. Third, the HPER mechanism classifies training experiences into three hierarchical priority layers so the agent learns more efficiently from rare but critical events like collisions and successful arrivals. The resulting HPER-D3QN algorithm outperforms all baselines across every test condition." |
| **What makes this approach different from previous DRL work on collision avoidance?** | "Most previous DRL methods simplified the problem significantly — they assumed all aircraft are the same type, used ideal sensor coverage with no partial observability, and ignored wind effects. This paper addresses all three gaps simultaneously. It handles heterogeneous aircraft with different speeds, sizes, and warning zones. It uses a sector-based partial observation model that works with fixed-dimension inputs regardless of how many aircraft are present. And it introduces HPER, which no previous collision avoidance paper had used. The combination produces a much more robust system." |
| **What are the limitations of this work?** | "There are a few important limitations. First, all experiments are in 2D simulation — the paper does not test the vertical dimension, and no real hardware is involved. Second, the wind model uses a smooth sinusoidal function that is more regular than real atmospheric turbulence. Third, in the simulation, the other aircraft follow fixed predefined paths — they do not react to the UAV, which is unrealistic. In a real scenario, a manned pilot would also maneuver when they see a drone approaching. The authors themselves acknowledge these limitations and identify hardware-in-the-loop testing as the next step." |
| **What evaluation metrics did they use and are they appropriate?** | "The paper uses three metrics. Success rate measures whether the UAV avoids all collisions and reaches its destination — this is the primary metric. Task completion time measures efficiency. Frequency of Hazardous Proximity, or FHP, counts how many times per episode the UAV enters another aircraft's warning zone — this captures near-miss risk that success rate alone would miss. I think this combination is appropriate because success rate alone could hide a system that barely avoids collisions by constantly cutting through warning zones. Including FHP makes the evaluation more nuanced." |
| **What dataset was used?** | "No external dataset was used. All training and testing data was generated procedurally by a custom simulation environment built with Python's PyGame library. The airspace is 30 km by 30 km and supports up to 25 aircraft. During training, the number of aircraft, the manned-to-unmanned ratio, and uncertainty level were randomly varied each episode, giving the agent diverse training experience. Testing was done with 300 independent runs repeated 10 times for each scenario configuration." |
| **What is HPER and how does it work?** | "HPER stands for Hierarchical Prioritized Experience Replay. During training, the agent accumulates experiences — each experience is a tuple of the current observation, the action taken, the reward received, and the next observation. Standard experience replay samples these uniformly at random. HPER instead sorts each experience into one of three layers. The high-priority layer holds experiences from collision events, destination arrivals, and boundary violations — rare but critical. The medium-priority layer holds warning zone entry experiences. The low-priority layer holds routine safe-cruise experiences. Sampling is weighted so the high-priority layer is drawn from most often. Within each layer, individual experiences are further ranked by their Temporal-Difference error. This two-level prioritization makes the training much more efficient." |
| **What is DTPA?** | "DTPA is the Dynamic Threat Prioritization Assessment algorithm. Within each of the 8 detection sectors around the UAV, there may be multiple aircraft. DTPA scores each one using the formula: S = 0.4 times the normalized time to closest approach, plus 0.4 times the normalized distance at closest approach, plus 0.2 times a type coefficient — where the type coefficient is 0.75 for manned aircraft and 0.25 for drones. The aircraft with the highest score becomes the intruder for that sector. This is better than just picking the closest aircraft because a fast manned jet heading directly toward you 700 meters away is more dangerous than a slow drone 300 meters away that is flying past you." |
| **What future work do the authors suggest?** | "The authors plan to conduct hardware-in-the-loop semi-physical simulations and real flight tests under the Live-Virtual-Constructive framework, which combines real physical assets, simulated platforms, and computer-generated forces. The key challenge they want to address next is the simulation-to-reality transfer mechanism — making sure the policy trained in simulation works reliably on real hardware with real sensor noise and actuator limitations." |
| **Do you find the results convincing? Why or why not?** | "I find the results largely convincing for a simulation study. The experimental design is notably thorough — three independent evaluation axes, 300 runs with 10 repetitions, ablation studies, and comparison against established industry standards like NASA's DO-365C. The ablation study is particularly convincing because it shows exactly how much each component contributes to performance. However, I would want to see 3D extension and hardware-in-the-loop results before being fully convinced of real-world applicability. The sim-to-real gap for actual flying hardware is much larger than the paper's Unity3D transfer test demonstrates." |
| **How does HPER-D3QN compare to the NASA rule-based standard?** | "HPER-D3QN outperforms the NASA DO-365C rule-based standard across all metrics — higher success rate, shorter task completion time, and lower frequency of hazardous proximity events — especially in high-density scenarios. The rule-based approach struggles as aircraft count increases because its fixed rules cannot adapt to the complexity of 25 mixed aircraft. HPER-D3QN, having learned through trial and error, adapts better to varying conditions." |
| **Could this approach be applied to civilian air traffic management?** | "The paper does not explicitly address civilian application, but the underlying approach is applicable. Civilian UAV traffic management faces similar challenges of partial observability, mixed aircraft types, and dynamic environments. The main difference would be the reward structure and safety thresholds, which would need to be redesigned for civilian separation standards. The DTPA and HPER mechanisms themselves are general enough to transfer to that domain." |
| **What would you change if you were an author?** | "I would extend the environment to 3D to make the collision avoidance problem more realistic — all current experiments are in a 2D horizontal plane. I would also model the other aircraft as reactive agents rather than fixed-plan followers, so the algorithm is tested against intelligent opponents. And I would include a sensitivity analysis showing how HPER performance varies with different priority scaling factors, since those values are currently chosen without a principled justification." |

---

## What NOT to Say

1. **Do not say "the paper trains the UAV in the real world."** All experiments are in simulation. The Unity3D test is still a simulation — just a more realistic one.

2. **Do not confuse DTPA with HPER.** DTPA identifies which aircraft are the biggest threats. HPER manages how training experiences are stored and sampled. They are separate mechanisms that work together.

3. **Do not say "the 9 actions cover all possible maneuvers."** The 9 discrete actions are an approximation — they cover only 3 speed levels and 3 heading rates. It is a simplification for computational tractability, not a complete control specification.

4. **Do not overstate the transfer experiment.** The Unity3D test is encouraging but it is still a simulation transfer, not real-world flight. Avoid saying it "proves" the system works in the real world.

5. **Do not say the method works for "any" collision avoidance problem.** It was designed specifically for the joint operational airspace context. Generalizing beyond that setting would require new training and validation.

---

## Closing Statement

> "In summary, this paper makes a meaningful contribution to autonomous UAV collision avoidance in complex joint battlefield airspace. By combining intelligent threat assessment through DTPA, hierarchical experience management through HPER, and a stable D3QN backbone, the proposed algorithm achieves state-of-the-art performance that conventional and prior DRL methods cannot match. The experimental results are thorough and the ablation study provides rigorous evidence for each design choice. The primary limitation is that it remains a simulation study — which the authors acknowledge — and the next milestone is hardware validation. Thank you."

---

## If You Forget Something

> "If you blank on a specific number or detail, you can always say: 'The paper reports this in the experimental results — the key finding is that HPER-D3QN consistently outperforms all baselines across every condition tested, with the HPER mechanism being the most critical component according to the ablation study.' This covers you while you collect your thoughts."
