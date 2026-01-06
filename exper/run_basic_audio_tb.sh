#!/usr/bin/env bash
set -euo pipefail

runs=4

for i in $(seq 1 "${runs}"); do
  run_dir="logs/basic_audio_run_${i}"
  mkdir -p "${run_dir}"
  python3 examples/python/learning_stable_baselines3_notifications.py \
    --env VizdoomBasicAudio-v1 \
    --dir "${run_dir}" \
    --exp "BasicAudio" \
    --n-envs 1
done
