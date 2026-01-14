# Vibe coding

This folder tracks the commands used to run notification on/off comparisons and
plotting in this repo.

Training (background, survives logout):
```bash
nohup python examples/python/learning_stable_baselines3_notifications.py \
  --compare-notifications \
  --trials 4 \
  --n-envs 8 \
  --timesteps 2000000 \
  --dir ./logs_YYYY-MM-DD \
  --images-dir ./logs_YYYY-MM-DD/images \
  > ./logs_YYYY-MM-DD/run.log 2>&1 &
```

Plotting (EMA smoothing, all trials):
```bash
python examples/python/export_notification_plots.py \
  --log-dir ./logs_YYYY-MM-DD \
  --output-dir ./logs_YYYY-MM-DD/images \
  --image-format png \
  --exp Notif \
  --trials 4 \
  --smooth-alpha 0.96
```

Plotting (filter TensorBoard run directories ending with `_2`):
```bash
python examples/python/export_notification_plots.py \
  --log-dir ./logs_YYYY-MM-DD \
  --output-dir ./logs_YYYY-MM-DD/images \
  --image-format png \
  --exp Notif \
  --trials 4 \
  --smooth-alpha 0.96 \
  --run-suffix _2
```
