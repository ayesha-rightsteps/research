#!/bin/sh
# Phase 2, part 2: RMAPPO x 10 seeds x Stage 2/3 = 20 runs (slowest method, run last), 6 at a time (Ayesha, 2026-10-15).
# Stage 3 before Stage 2. Restarted 2026-10-15 ~23:00 with the faster RMAPPO update (baselines_v4._chunk_eval).
# Launch from v4/03-base-paper-baselines/:
#   nohup caffeinate -i -s ./runs/run_phase2_rmappo.sh > runs/logs/launcher_rmappo.out 2>&1 &
# Then check one runs/stage*/<method>/seed-*/config.json of every method.
cd "$(dirname "$0")/.."
. ../../../../venv/bin/activate
date '+start %Y-%m-%d %H:%M:%S' >> runs/logs/time_rmappo.txt
cat runs/jobs_rmappo.txt | xargs -P 6 -L 1 sh -c 'm=$0; st=$1; sd=$2; python3 -u train_baselines.py $m $st $sd > runs/logs/$m-stage$st-seed$sd.log 2>&1'
date '+end %Y-%m-%d %H:%M:%S' >> runs/logs/time_rmappo.txt
