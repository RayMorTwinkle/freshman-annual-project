"""Export matched illustrative frames and gripper action traces after collection."""
import csv
from pathlib import Path
import subprocess
import sys

import h5py
import matplotlib.pyplot as plt
import numpy as np

root = Path(sys.argv[1])
rows = list(csv.DictReader((root / "seed-attempts.csv").open()))
by_mode = {mode: {r["seed"]: r for r in rows
                  if r["condition"] == mode and r["video"] and r["hdf5"]}
           for mode in ("clean", "randomized")}
seeds = set(by_mode["clean"]) & set(by_mode["randomized"])
if not seeds:
    print("No matching seed with verified exports in both conditions")
    raise SystemExit(0)
seed = min(seeds, key=int)
fig, axes = plt.subplots(2, 1, figsize=(10, 6), sharex=False)
for ax, (mode, items) in zip(axes, by_mode.items()):
    row = items[seed]
    with h5py.File(root / row["hdf5"]) as h:
        left = np.asarray(h["action/left_ee_joint_states"]).flatten()
        right = np.asarray(h["action/right_ee_joint_states"]).flatten()
    ax.plot(left, label="Left gripper")
    ax.plot(right, label="Right gripper")
    ax.set(title=f"{mode}, seed {seed}", xlabel="Recorded action index", ylabel="Action value")
    ax.legend()
    for label, fraction in [("start", 0.0), ("middle", .5), ("end", .95)]:
        frame = round((int(row["frames"]) - 1) * fraction)
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(root / row["video"]),
                        "-vf", f"select=eq(n\\,{frame})", "-frames:v", "1",
                        str(root / f"pair-seed-{seed}-{mode}-{label}.png")], check=True)
fig.suptitle("RoboTwin handover: recorded gripper actions")
fig.tight_layout()
fig.savefig(root / f"pair-seed-{seed}-gripper.png", dpi=180)
print("Illustrated matched seed", seed)
