import json, time, importlib.metadata as md
import torch
from PIL import Image
from huggingface_hub import HfApi
from lerobot.datasets.lerobot_dataset import LeRobotDataset
from lerobot.policies.factory import make_pre_post_processors
from lerobot.policies.smolvla.modeling_smolvla import SmolVLAPolicy
model = "lerobot/smolvla_base"
data = "lerobot/svla_so101_pickplace"
api = HfApi()
model_rev, data_rev = api.model_info(model).sha, api.dataset_info(data).sha
print(model_rev, data_rev, flush=True)
ds = LeRobotDataset(data, revision=data_rev, video_backend="pyav")
frame = dict(ds[0])
keys = sorted(k for k in frame if k.startswith("observation.images."))
print(keys, flush=True)
p = SmolVLAPolicy.from_pretrained(model, revision=model_rev).to("cuda").eval()
pre, post = make_pre_post_processors(p.config, model, preprocessor_overrides={"device_processor":{"device":"cuda"}})
expected = sorted(k for k in p.config.input_features if k.startswith("observation.images."))
print(expected, flush=True)
mapping = {key:keys[min(i,len(keys)-1)] for i,key in enumerate(expected) if key not in frame}
for key, source in mapping.items():
    frame[key] = frame[source]
image = frame[keys[0]].permute(1,2,0).mul(255).clamp(0,255).byte().numpy()
Image.fromarray(image).save("/content/smol-observation.png")
batch = pre(frame)
torch.manual_seed(7)
torch.cuda.synchronize()
t = time.perf_counter()
with torch.inference_mode():
    action = post(p.select_action(batch))
torch.cuda.synchronize()
result = dict(model=model, model_revision=model_rev,dataset=data,dataset_revision=data_rev, frame_index=0,frames=len(ds), mapping=mapping, task=frame.get("task"),shape=list(action.shape),action=action.cpu().tolist(), finite=bool(action.isfinite().all()), first_action_seconds=time.perf_counter()-t,parameters=sum(x.numel() for x in p.parameters()),gpu=torch.cuda.get_device_name(), versions={x:md.version(x) for x in ("lerobot","torch","transformers")})
print(json.dumps(result), flush=True)
assert result["finite"]
open("/content/smol-result.json","w").write(json.dumps(result,indent=2))
