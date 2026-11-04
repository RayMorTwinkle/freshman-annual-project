"""Analyze the published RoboTwin conversion without starting a simulator."""
import json
import statistics
import urllib.request
from pathlib import Path

import pyarrow.parquet as pq

REVISION = "1287871839fae2296bc27b88a5457c3e1eba8e1f"
BASE = f"https://huggingface.co/datasets/lerobot/robotwin_unified/resolve/{REVISION}"
WORK = Path(__file__).resolve().parent

def fetch(remote_path, local_path):
    if not local_path.exists():
        urllib.request.urlretrieve(f"{BASE}/{remote_path}", local_path)
    return local_path

info = json.loads(fetch("meta/info.json", WORK / "robo-info.json").read_text())
with __import__("tempfile").TemporaryDirectory() as tmp:
    meta = fetch("meta/episodes/chunk-000/file-000.parquet", Path(tmp) / "episodes.parquet")
    table = pq.read_table(meta, columns=["episode_index", "length", "tasks"])
    lengths = table["length"].to_pylist()
    first = table.slice(0, 3).to_pylist()
    assert len(lengths) == info["total_episodes"]
    assert sum(lengths) == info["total_frames"]
result = {
    "revision": REVISION, "episodes": len(lengths), "frames": sum(lengths),
    "fps": info["fps"], "action_dimensions": info["features"]["action"]["shape"],
    "state_dimensions": info["features"]["observation.state"]["shape"],
    "camera_keys": [k for k in info["features"] if k.startswith("observation.images.")],
    "episode_length_frames": {
        "min": min(lengths), "median": statistics.median(lengths), "max": max(lengths)
    },
    "first_three_episodes": first,
}
(WORK / "robotwin-result.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
print(json.dumps(result, ensure_ascii=False, indent=2))
