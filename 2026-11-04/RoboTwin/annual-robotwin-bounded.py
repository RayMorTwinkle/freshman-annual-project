"""Run the official collector with an equal cap of five attempts per condition."""
import os
from pathlib import Path
import subprocess
import sys

import yaml

ROOT = Path("/content/robotwin")
DRIVE = Path("/content/drive/MyDrive")
DEST = Path(os.environ.get("ROBO_OUTPUT", str(DRIVE / "大一年度项目复现/RoboTwin")))
assert not DEST.is_relative_to(DRIVE) or DRIVE.is_dir(), "Mount Drive before running"
DEST.mkdir(parents=True, exist_ok=True)
os.chdir(ROOT)
source = Path("scripts/collect_data.py")
code = source.read_text()
old = 'while suc_num < args["episode_num"]:'
new = old[:-1] + ' and epid < 5:'
if old in code:
    code = code.replace(old, new, 1)
    marker = '    # =========== Collect Data ==========='
    assert code.count(marker) == 1
    code = code.replace(marker, '    args["episode_num"] = min(args["episode_num"], len(seed_list))\n\n' + marker)
    source.write_text(code)
assert new in source.read_text()
configs = Path("env_cfg/task_config")
for mode in ("clean", "randomized"):
    name = f"annual_b_{mode}"
    config = yaml.safe_load((configs / f"demo_{mode}.yml").read_text())
    config.update(episode_num=5, save_path=str(DEST / "generated"))
    config_path = configs / f"{name}.yml"
    config_path.write_text(yaml.safe_dump(config, sort_keys=False))
    (DEST / config_path.name).write_text(config_path.read_text())
    with (DEST / f"{mode}.log").open("a", buffering=1) as log:
        result = subprocess.run(
            ["timeout", "1200", sys.executable, "-u", str(source), "handover_block", name],
            stdout=log, stderr=subprocess.STDOUT,
        )
        print(mode, "exit code", result.returncode, file=log, flush=True)
