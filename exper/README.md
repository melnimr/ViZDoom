# Vibe coding

This folder tracks the commands used to run notification on/off comparisons and
plotting in this repo.

Training (background, survives logout, 2026-01-07):
```bash
nohup python examples/python/learning_stable_baselines3_notifications.py \
  --compare-notifications \
  --trials 4 \
  --n-envs 8 \
  --timesteps 2000000 \
  --dir ./logs_2026-01-07 \
  --images-dir ./logs_2026-01-07/images \
  > ./logs_2026-01-07/run.log 2>&1 &
```

Training (background, 2026-01-07, n_envs=4, 500k steps):
```bash
nohup python examples/python/learning_stable_baselines3_notifications.py \
  --compare-notifications \
  --trials 4 \
  --n-envs 4 \
  --timesteps 500000 \
  --dir ./logs_2026-01-07 \
  --images-dir ./logs_2026-01-07/images \
  > ./logs_2026-01-07/run.log 2>&1 &
```

Plotting (EMA smoothing, all trials, 2026-01-07):
```bash
python examples/python/export_notification_plots.py \
  --log-dir ./logs_2026-01-07 \
  --output-dir ./logs_2026-01-07/images \
  --image-format png \
  --exp Notif \
  --trials 4 \
  --smooth-alpha 0.96
```

Plotting (filter TensorBoard run directories ending with `_2`, 2026-01-07):
```bash
python examples/python/export_notification_plots.py \
  --log-dir ./logs_2026-01-07 \
  --output-dir ./logs_2026-01-07/images \
  --image-format png \
  --exp Notif \
  --trials 4 \
  --smooth-alpha 0.96 \
  --run-suffix _2
```
