#!/bin/sh
# Phase 1b Step 4, part 2: the 40 runs of the FIXED (risk-learning) PAH, started automatically after the
# non-PAH queue (run_non_pah.sh) has finished. Same settings as every other method (PLAN.md Section 10).
cd "$(dirname "$0")/.."
. ../../../../venv/bin/activate
while pgrep -f "runs/run_non_pah.sh" > /dev/null; do sleep 60; done
date '+pah start %Y-%m-%d %H:%M:%S' >> runs/logs/time_pah.txt
cat runs/jobs_pah_fixed.txt | xargs -P 4 -L 1 sh -c 'm=$0; st=$1; sd=$2; d=$3; python3 -u train.py $m $st $sd --obstacles $d --danger 20 --collision-penalty 10 > runs/logs/$m-stage$st-seed$sd.log 2>&1'
date '+pah end %Y-%m-%d %H:%M:%S' >> runs/logs/time_pah.txt
