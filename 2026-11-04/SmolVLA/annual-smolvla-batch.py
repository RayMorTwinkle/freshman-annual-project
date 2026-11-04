"""Evaluate 30 independent observations and one paired instruction intervention."""
import json
import os
import time
from pathlib import Path

import torch
from PIL import Image
from lerobot.datasets.lerobot_dataset import LeRobotDataset
from lerobot.policies.factory import make_pre_post_processors
from lerobot.policies.smolvla.modeling_smolvla import SmolVLAPolicy

MODEL = "lerobot/smolvla_base"
MODEL_REV = "5e8d12a6e2975b0e5e5fce7c8caf47c371d257b6"
DATA = "lerobot/svla_so101_pickplace"
DATA_REV = "f641879e22172be7e8161d5e6c1503c2d2feb657"
DRIVE = Path("/content/drive/MyDrive")
OUT = Path(os.environ.get("SMOL_OUTPUT", str(DRIVE / "大一年度项目复现/SmolVLA")))
assert not OUT.is_relative_to(DRIVE) or DRIVE.is_dir(), "Mount Drive before running"
OUT.mkdir(parents=True, exist_ok=True)
ds = LeRobotDataset(DATA, revision=DATA_REV, video_backend="pyav")
policy = SmolVLAPolicy.from_pretrained(MODEL, revision=MODEL_REV).to("cuda").eval()
pre, post = make_pre_post_processors(
    policy.config, MODEL, preprocessor_overrides={"device_processor": {"device": "cuda"}}
)
mapping = {"camera1": "side", "camera2": "up", "camera3": "up"}
snapshot = OUT / "observations.json"
rows = json.loads(snapshot.read_text()) if snapshot.exists() else []
done = {(r["frame"], r["condition"]) for r in rows}

def observe(index, episode, position, condition, instruction=None):
    if (index, condition) in done:
        return
    frame = dict(ds[index])
    for target, source in mapping.items():
        frame[f"observation.images.{target}"] = frame[f"observation.images.{source}"]
    if instruction:
        frame["task"] = instruction
    batch = pre(frame)
    policy.reset()
    torch.manual_seed(7)
    torch.cuda.synchronize()
    start = time.perf_counter()
    with torch.inference_mode():
        action = post(policy.select_action(batch)).flatten()
    torch.cuda.synchronize()
    seconds = time.perf_counter() - start
    assert action.isfinite().all()
    rows.append(dict(frame=index, episode=episode, position=position,
                     condition=condition, instruction=frame["task"],
                     predicted=action.cpu().tolist(), reference=frame["action"].flatten().tolist(),
                     seconds=seconds, model_revision=MODEL_REV, dataset_revision=DATA_REV))
    temp = snapshot.with_suffix(".tmp")
    temp.write_text(json.dumps(rows, indent=2, ensure_ascii=False))
    temp.replace(snapshot)
    if condition == "original" and position in (0, 4, 9):
        image = frame["observation.images.side"].permute(1, 2, 0).mul(255).clamp(0, 255)
        Image.fromarray(image.byte().cpu().numpy()).save(OUT / f"episode-{episode}-frame-{index}.png")

for episode in (0, 1, 2):
    meta = ds.meta.episodes[episode]
    first, end = int(meta["dataset_from_index"]), int(meta["dataset_to_index"])
    for position in range(10):
        index = first + round((end - first - 1) * position / 9)
        observe(index, episode, position, "original")
        if episode == 0 and position == 4:
            observe(index, episode, position, "changed_instruction",
                    "Leave the pink lego brick where it is.")
print("Saved", len(rows), "observations to Drive")
