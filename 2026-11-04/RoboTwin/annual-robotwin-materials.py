"""Index observed seed trials and validate the resulting videos and HDF5 files."""
import csv
import json
from pathlib import Path
import re
import subprocess
import sys
import h5py

root = Path(sys.argv[1])
rows = []
for mode in ("clean", "randomized"):
    log = root / f"{mode}.log"
    if not log.exists():
        continue
    events = re.findall(r"simulate data episode (\d+) (success|fail)! \(seed = (\d+)\)", log.read_text())
    unique = {}
    task = root / "generated" / f"annual_b_{mode}" / "handover_block" / "aloha_agilex"
    for episode, outcome, seed in events:
        idx = int(seed)
        if idx in unique and unique[idx][1] != outcome:
            raise RuntimeError(f"Inconsistent results for {mode} seed {seed}; inspect log")
        unique[idx] = (int(episode), outcome)
    for seed, (episode, outcome) in sorted(unique.items()):
        item = dict(condition=mode, seed=seed, planning_and_task_check=outcome,
                    hdf5="", video="", frames="")
        if outcome == "success":
            matches = sorted(task.rglob(f"episode_{episode:07d}.hdf5"))
            if matches:
                with h5py.File(matches[0]) as h:
                    assert len(h.keys()) > 0
                item["hdf5"] = str(matches[0].relative_to(root))
            videos = [*task.rglob(f"episode_{episode:07d}.mp4"), *task.rglob(f"episode{episode}.mp4")]
            if videos:
                vid = videos[0]
                info = subprocess.check_output(
                    ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                     "stream=nb_frames", "-of", "json", str(vid)], text=True)
                item["frames"] = json.loads(info)["streams"][0].get("nb_frames", "")
                item["video"] = str(vid.relative_to(root))
                if not (root / f"{mode}-seed-{seed}.png").exists():
                    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(vid), "-frames:v", "1",
                                    str(root / f"{mode}-seed-{seed}.png")], check=True)
        rows.append(item)
fields = ["condition", "seed", "planning_and_task_check", "hdf5", "video", "frames"]
with (root / "seed-attempts.csv").open("w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fields)
    writer.writeheader()
    writer.writerows(rows)
print(json.dumps({mode: {"attempts": sum(r["condition"] == mode for r in rows),
                       "checked_success": sum(r["condition"] == mode and r["planning_and_task_check"] == "success" for r in rows),
                       "hdf5": sum(r["condition"] == mode and bool(r["hdf5"]) for r in rows),
                       "videos": sum(r["condition"] == mode and bool(r["video"]) for r in rows)}
                  for mode in ("clean", "randomized")}, indent=2))
