"""Produce a numeric table, an offline action comparison, and latency summary."""
import csv
import json
from pathlib import Path
import sys

import matplotlib.pyplot as plt
import numpy as np

root = Path(sys.argv[1])
rows = json.loads((root / "observations.json").read_text())
baseline = [r for r in rows if r["condition"] == "original"]
assert len(baseline) == 30 and len({r["frame"] for r in baseline}) == 30
fields = ["episode", "frame", "position", "condition", "seconds", "instruction"]
fields += [f"{kind}_{j+1}" for kind in ("predicted", "reference") for j in range(6)]
with (root / "observations.csv").open("w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fields)
    writer.writeheader()
    for r in rows:
        row = {k: r[k] for k in fields if k in r}
        for kind in ("predicted", "reference"):
            row.update({f"{kind}_{j+1}": value for j, value in enumerate(r[kind])})
        writer.writerow(row)
seconds = np.array([r["seconds"] for r in baseline])
summary = {
    "observations": len(baseline), "first_seconds": float(seconds[0]),
    "post_first_median_seconds": float(np.median(seconds[1:])),
    "post_first_p90_seconds": float(np.percentile(seconds[1:], 90)),
    "action_units_validation": "Unverified equivalence between checkpoint and recorded controller; descriptive overlay only.",
}
changed = next((r for r in rows if r["condition"] == "changed_instruction"), None)
if changed:
    original = next(r for r in baseline if r["frame"] == changed["frame"])
    summary["paired_instruction_delta_l2"] = float(np.linalg.norm(
        np.array(changed["predicted"]) - np.array(original["predicted"])
    ))
(root / "summary.json").write_text(json.dumps(summary, indent=2))
fig, axes = plt.subplots(2, 3, figsize=(12, 6), sharex=True)
for joint, ax in enumerate(axes.flat):
    sample = [r for r in baseline if r["episode"] == 0]
    ax.plot([r["position"] for r in sample], [r["predicted"][joint] for r in sample], "o-", label="Predicted")
    ax.plot([r["position"] for r in sample], [r["reference"][joint] for r in sample], ".--", label="Recorded")
    ax.set_title(f"Action component {joint+1}")
    ax.grid(alpha=.25)
axes.flat[0].legend()
fig.supxlabel("Sample position in episode 0")
fig.suptitle("Offline action outputs and recorded values (units alignment unverified)")
fig.tight_layout()
fig.savefig(root / "action-overlay.png", dpi=170)
print(json.dumps(summary))
