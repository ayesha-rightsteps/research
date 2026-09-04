# 08 — Flashcards

Use these to quiz yourself — or ask someone to read the question while you answer out loud. Cover the answer with your hand first!

---

**Q1: What does DRL stand for and what is it in one sentence?**

---
Deep Reinforcement Learning — an AI technique where a machine learns optimal decision-making by trial and error, receiving rewards or penalties, powered by deep neural networks.

---

**Q2: What are the four autonomous system domains covered in this survey?**

---
Autonomous Cars, Autonomous Robotics, Autonomous Drones, and Advanced Driver Assistance Systems (ADAS).

---

**Q3: Which journal published this paper, and when?**

---
IEEE Transactions on Intelligent Transportation Systems, Vol. 26, No. 7, July 2025.

---

**Q4: Who are the three authors?**

---
Shruti Govinda, Bouziane Brik (Senior Member, IEEE), and Saad Harous (Senior Member, IEEE). They are from the University of Sharjah, UAE.

---

**Q5: What is DDPG and why is it used most in this paper?**

---
Deep Deterministic Policy Gradient — an actor-critic DRL algorithm designed for continuous action spaces (like choosing a steering angle). It is the most frequently used algorithm in the survey because autonomous driving and drone control require smooth, continuous decisions rather than discrete choices like "turn left or right."

---

**Q6: What is the key difference between DQN and DDPG?**

---
DQN works for discrete actions (a fixed set of choices like "turn left, go straight, turn right"), while DDPG works for continuous actions (any value on a range, like steering 17.3 degrees). DQN is better for routing and braking events; DDPG is better for steering, speed control, and precise maneuvering.

---

**Q7: What impressive accuracy did the VILDS system achieve?**

---
98.2% lane detection accuracy and 96.5% lane departure warning accuracy — outperforming all traditional methods, even in adverse weather conditions like fog and rain.

---

**Q8: What does SIFRCNN stand for and what was its key result?**

---
Scale Invariant Faster Region-based Convolutional Neural Network. It achieved a 23% improvement in miss rate over other CNN-based pedestrian detectors, tested on the KAIST, CityPerson, and Caltech datasets for nighttime pedestrian detection.

---

**Q9: Which algorithm achieved a 100% safety rate in robotic trajectory planning, and in how many episodes?**

---
SAC (Soft Actor-Critic) achieved a 100% safety rate within 6,000 simulation episodes, outperforming DDPG in both safety and consistency for a Panda robot manipulator task.

---

**Q10: What is SAC and what makes it special?**

---
Soft Actor-Critic — a DRL algorithm that adds an entropy term to the reward function, encouraging the agent to explore diverse actions rather than locking in too early. This makes it more robust and better at finding safe, stable policies for safety-critical tasks like robot manipulation.

---

**Q11: What is the Sim-to-Real gap and why does it matter?**

---
The performance drop that occurs when a DRL system trained in a simulator is deployed in the real physical world. It matters because almost all DRL systems are trained in simulation (it's cheaper and safer), but the real world has sensor noise, physics variations, and unexpected edge cases that simulators can't perfectly replicate. It's identified as the field's most persistent unsolved challenge.

---

**Q12: What is PPO and where is it used in this paper?**

---
Proximal Policy Optimization — a DRL algorithm that clips policy updates to prevent large, destabilizing changes during training. In this paper, it's used for training multi-legged robotic swarms on flat and rough terrains, and for obstacle avoidance on the AWS DeepRacer platform.

---

**Q13: What is MARL and which application in this paper uses it?**

---
Multi-Agent Reinforcement Learning — a framework where multiple AI agents learn simultaneously in a shared environment. In this paper, it's used for coordinating a fleet of drones to characterize air pollution plumes, combined with Gaussian Processes and a Categorical DQN (DQN-C51).

---

**Q14: Name three real-world companies that use DRL for autonomous systems, as discussed in this paper.**

---
Any three of: Tesla (Autopilot for autonomous driving), Waymo (ChauffeurNet for self-driving taxis), Boston Dynamics (Atlas robot locomotion), Amazon Robotics/Kiva Systems (warehouse robot coordination), Amazon Prime Air (drone delivery), DJI (consumer drone intelligence), Mobileye (ADAS), Nvidia DRIVE Platform (autonomous vehicle AI).

---

**Q15: What is the survey's methodology called, and what databases were searched?**

---
Systematic Literature Review (SLR). Databases: IEEE Xplore, ACM Digital Library, Google Scholar, ProQuest, EBSCO, ScienceDirect, and MDPI. Papers published 2018–2024 were prioritized.

---

**Q16: What are the three main challenges the paper identifies for future work?**

---
(1) Scalability and generalization — DRL struggles in diverse, unstructured real-world environments. (2) Safety and robustness — systems must be certified safe for deployment in critical applications. (3) Sim-to-Real transfer — bridging the gap between simulation training and real-world performance.

---

**Q17: What does ADAS stand for? Give two examples.**

---
Advanced Driver Assistance Systems. Examples: lane departure warning (alerts driver when drifting out of lane), adaptive cruise control (automatically maintains safe following distance), and automatic emergency braking (brakes to avoid a collision).

---

**Q18: What is the D3QN and why is it better than standard DQN?**

---
Dueling Double Deep Q-Network — an enhanced version of DQN that uses two separate networks to avoid overestimating action values (Double DQN) and a dueling architecture that separately estimates state value and action advantage. It achieves superior performance in drone interception and obstacle avoidance compared to standard DQN.

---

**Q19: What is the one-sentence takeaway from this paper?**

---
DRL is already transforming autonomous systems in cars, robots, drones, and ADAS — but challenges in safety, scalability, and real-world deployment mean the technology's full potential is still ahead, and this survey maps exactly what needs to happen to get there.

---

**Q20: What future technology integration does the paper discuss as the next frontier?**

---
Large Language Models (LLMs) and transformer-based architectures (like Decision Transformers) — which could give autonomous systems more sophisticated reasoning, natural language understanding, and better sample efficiency. The paper also highlights multi-modal learning (combining vision, language, and sensor inputs) as a key direction.

---

*💡 Tip: Go through these twice — once reading, once covering the answers. 20 questions = ~15 minutes. You've got this!*
