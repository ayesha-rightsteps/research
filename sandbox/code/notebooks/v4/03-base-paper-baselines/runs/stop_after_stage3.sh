#!/bin/sh
# Ayesha 2026-10-14 17:25: abhi sirf Stage 3; Stage 2 baad mein (run_phase2_stage2.sh).
# Waits until the last Stage 3 job (da-mappo-2d seed 51) has started, then stops ONLY the xargs queue (pid given) so
# no Stage 2 job starts; running trainings are not touched. Keeps the Mac awake (run under caffeinate) until they end.
cd "$(dirname "$0")"
XARGS=$1
until [ -f logs/da-mappo-2d-stage3-seed51.log ]; do sleep 2; done
kill "$XARGS"
date '+queue stopped after last Stage 3 job started %Y-%m-%d %H:%M:%S' >> logs/time_without_rmappo.txt
while pgrep -f "train_baselines.py" > /dev/null; do sleep 30; done
date '+Stage 3 all finished %Y-%m-%d %H:%M:%S' >> logs/time_without_rmappo.txt
