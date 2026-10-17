#!/bin/sh
# v4 Phase 3: every experiment of PLAN.md Section 4, evaluation only (no training), 6 processes.
# Launch from v4/04-base-paper-experiments/:
#   nohup caffeinate -i -s ./run_phase3.sh > logs/run_phase3.out 2>&1 &
# Results: 02-redesign/output/phase3/<experiment>/ (our 5 methods) and 03-base-paper-baselines/output/phase3/<experiment>/
# (the 4 base-paper methods; RMAPPO excluded). The main setting (E5 metrics) is in .../phase3/main/ (run before, as part
# of the identity gate). Each model keeps its trained configuration except the one setting named in the folder.
cd "$(dirname "$0")/../02-redesign"
. ../../../../venv/bin/activate
LOG=../04-base-paper-experiments/logs/time_phase3.txt
OURS=plain-mappo,fixed-weight-mappo,tau-rule-mappo,mappo-pah,mappo-pah-no-hungarian
BASE=ippo,mappo,da-mappo-2d,igat-style
ev() { python3 evaluate.py --procs 6 "$@"; }
both() { ev --methods $OURS "$@"; ev --phase2 --methods $BASE "$@"; }
date '+start %Y-%m-%d %H:%M:%S' >> $LOG

# E1 obstacle density (S2 trained on 10 discs, S3 on 20; those settings are the main results)
for n in 20 30 40 50; do both --stages 2 --obstacles $n --raw-dir phase3/density_s2_n$n; done
for n in 10 30 40 50; do both --stages 3 --obstacles $n --raw-dir phase3/density_s3_n$n; done
date '+E1 done %H:%M:%S' >> $LOG

# E2 static targets (trained with target speed 1)
both --target-speed 0 --raw-dir phase3/static
date '+E2 done %H:%M:%S' >> $LOG

# E3 assignment every 50 steps (only methods trained with every-step assignment)
ev --methods plain-mappo,fixed-weight-mappo,tau-rule-mappo,mappo-pah --assign-every 50 --raw-dir phase3/assign50
ev --phase2 --methods da-mappo-2d --assign-every 50 --raw-dir phase3/assign50
date '+E3 done %H:%M:%S' >> $LOG

# E4 swarm size 3-10 (methods whose observation does not depend on the swarm size; trained sizes are the main results)
for n in 3 4 6 7 8 9 10; do
  ev --methods plain-mappo,fixed-weight-mappo,tau-rule-mappo,mappo-pah --stages 2 --drones $n --raw-dir phase3/swarm_s2_n$n
  ev --phase2 --methods igat-style --stages 2 --drones $n --raw-dir phase3/swarm_s2_n$n
done
for n in 3 4 5 6 7 9 10; do
  ev --methods plain-mappo,fixed-weight-mappo,tau-rule-mappo,mappo-pah --stages 3 --drones $n --raw-dir phase3/swarm_s3_n$n
  ev --phase2 --methods igat-style --stages 3 --drones $n --raw-dir phase3/swarm_s3_n$n
done
date '+E4 done %H:%M:%S' >> $LOG

# E6 LiDAR noise, Stage 3
for s in 0.02 0.05 0.1; do both --stages 3 --lidar-noise $s --raw-dir phase3/noise_s3_$s; done
date '+E6 done %H:%M:%S' >> $LOG

# E7 decision time, 1 process, 20 episodes, Stage 3 models (time per step for all drones together)
for n in 3 4 5 6 7 8 9 10; do
  python3 evaluate.py --procs 1 --episodes 20 --methods mappo-pah,fixed-weight-mappo --stages 3 --drones $n --raw-dir phase3/timing_n$n
  python3 evaluate.py --procs 1 --episodes 20 --phase2 --methods igat-style --stages 3 --drones $n --raw-dir phase3/timing_n$n
done
date '+end %Y-%m-%d %H:%M:%S' >> $LOG
