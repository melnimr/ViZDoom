#!/usr/bin/env bash
set -euo pipefail

base_dir="exper/images"
scenarios=(
  "VizdoomBasic-v1"
  "VizdoomDeadlyCorridor-v1"
  "VizdoomDefendCenter-v1"
  "VizdoomHealthGathering-v1"
)

frames_per_scenario=200

for scenario in "${scenarios[@]}"; do
  out_dir="${base_dir}/${scenario}"
  mkdir -p "${out_dir}"
  SCENARIO="${scenario}" OUT_DIR="${out_dir}" FRAMES="${frames_per_scenario}" python3 - <<'PY'
import os

import cv2
import gymnasium
import numpy as np

import vizdoom.gymnasium_wrapper  # noqa: F401

env_id = os.environ["SCENARIO"]
out_dir = os.environ["OUT_DIR"]
max_frames = int(os.environ["FRAMES"])

env = gymnasium.make(env_id)
obs, _ = env.reset()

frames_written = 0
episode = 0

while frames_written < max_frames:
    if obs is None:
        break
    if isinstance(obs, dict) and "screen" in obs:
        frame = obs["screen"]
        if frame is not None:
            if frame.dtype != np.uint8:
                frame = frame.astype(np.uint8)
            frame_bgr = frame[..., ::-1]
            out_path = os.path.join(out_dir, f"frame_{frames_written:05d}.png")
            cv2.imwrite(out_path, frame_bgr)
            frames_written += 1

    action = env.action_space.sample()
    obs, _, terminated, truncated, _ = env.step(action)
    if terminated or truncated:
        episode += 1
        obs, _ = env.reset()

env.close()
print(f"{env_id}: wrote {frames_written} frames across {episode + 1} episode(s) to {out_dir}")
PY
done
