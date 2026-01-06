#!/usr/bin/env bash
set -euo pipefail

base_log_dir="exper/random_logs"
base_img_dir="exper/images"
combined_log_dir="exper/random_logs_overlay"
scenarios=()

mapfile -t scenarios < <(
  python3 - <<'PY'
import random

import gymnasium
import vizdoom.gymnasium_wrapper  # noqa: F401

envs = sorted(
    env
    for env in gymnasium.envs.registry.keys()
    if "Vizdoom" in env and "MultiBinary" not in env
)
random.shuffle(envs)
for env in envs[:10]:
    print(env)
PY
)

for scenario in "${scenarios[@]}"; do
  log_dir="${base_log_dir}/${scenario}"
  images_dir="${base_img_dir}/${scenario}"
  python3 exper/random_scenarios_tensorboard.py \
    --env "${scenario}" \
    --log-dir "${log_dir}" \
    --images-dir "${images_dir}" \
    --episodes "10" \
    --combined-log-dir "${combined_log_dir}" \
    --tag-prefix "${scenario}"
done
