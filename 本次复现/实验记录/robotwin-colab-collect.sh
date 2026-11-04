#!/usr/bin/env bash
set -euo pipefail
cd /content/robotwin
export PATH=/content/robo-env/bin:$PATH
export CUDA_VISIBLE_DEVICES=0
export PYTHONUNBUFFERED=1
python scripts/update_embodiment_config_path.py
python - <<'PY'
from pathlib import Path
import yaml
folder = Path("env_cfg/task_config")
for name in ("demo_clean", "demo_randomized"):
    config = yaml.safe_load((folder / f"{name}.yml").read_text())
    config["episode_num"] = 1
    (folder / f"annual_{name}.yml").write_text(yaml.safe_dump(config, sort_keys=False))
PY
for mode in clean randomized; do
  rc=0
  timeout 540 python scripts/collect_data.py handover_block "annual_demo_$mode" >"/content/annual-$mode.log" 2>&1 || rc=$?
  echo "$mode exit $rc"
done
find data -type f | head -60
