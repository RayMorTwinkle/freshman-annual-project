"""Extract report-ready scientific figures from existing Drive artifacts on CPU."""
import csv
import importlib.util
import json
from pathlib import Path
import re
import urllib.request

import cv2
import h5py
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path("/content/drive/MyDrive/大一年度项目复现")
OUT = ROOT / "补充素材"
assert ROOT.is_dir()
OUT.mkdir(exist_ok=True)
codec_path = Path("/content/robotwin_image_codec.py")
urllib.request.urlretrieve(
    "https://raw.githubusercontent.com/RoboTwin-Platform/RoboTwin/"
    "ea8b21121ebb3cd201ff5b3fe361944ac94eda3f/data/decode_image_bit.py", codec_path)
spec = importlib.util.spec_from_file_location("robotwin_image_codec", codec_path)
codec = importlib.util.module_from_spec(spec)
spec.loader.exec_module(codec)
entries = []
def register(name, category, source, note):
    entries.append(dict(file=name, category=category, source=source, note=note))
def save(fig, name, category, source, note):
    fig.savefig(OUT / name, dpi=190, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    register(name,category,source,note)
def image_at(h5, camera, fraction):
    group = h5[f"vision/{camera}/colors"]
    index = round((len(group)-1)*fraction)
    return codec.decode_image_bit(group[index]),index
rows = list(csv.DictReader((ROOT/"RoboTwin/seed-attempts.csv").open()))
valid = [r for r in rows if r["hdf5"]]
by_mode = {m:{int(r["seed"]):r for r in valid if r["condition"]==m} for m in ("clean","randomized")}
struct=[]
for row in valid:
    mode, seed = row["condition"], int(row["seed"])
    with h5py.File(ROOT/"RoboTwin"/row["hdf5"],"r") as h:
        fig, axes=plt.subplots(2,3,figsize=(12,7))
        for ax, fraction in zip(axes.flat,np.linspace(0,1,6)):
            image,index=image_at(h,"cam_head",float(fraction))
            ax.imshow(image)
            ax.set_title(f"Observation {index} / {len(h['vision/cam_head/colors'])-1}",fontsize=11)
            ax.axis("off")
        fig.suptitle(f"Self-collected handover | {mode}, seed {seed}",fontsize=16)
        save(fig,f"R1-storyboard-{mode}-seed{seed}.png","轨迹分镜",row["hdf5"],
             "Six equally spaced observations. Temporal positions are not hand-labelled action phases.")
        framecount=len(h["vision/cam_head/colors"])
        left=np.asarray(h["action/left_arm_joint_states"])
        right=np.asarray(h["action/right_arm_joint_states"])
        lg=np.asarray(h["action/left_ee_joint_states"]).flatten()
        rg=np.asarray(h["action/right_ee_joint_states"]).flatten()
        struct.append(dict(condition=mode,seed=seed,observation_rows=framecount,
                           action_rows=len(left),video_frames=int(row["frames"]),
                           left_arm_components=left.shape[1],right_arm_components=right.shape[1],
                           camera_count=len(h["vision"]),finite_joint_actions=bool(np.isfinite(left).all() and np.isfinite(right).all())))
        if seed==0:
            fig,axes=plt.subplots(3,1,figsize=(11,8),sharex=True)
            for j in range(6):
                axes[0].plot(left[:,j],label=f"Joint {j+1}",lw=1)
                axes[1].plot(right[:,j],label=f"Joint {j+1}",lw=1)
            axes[0].set_title("Left arm")
            axes[1].set_title("Right arm")
            axes[0].legend(ncol=6,fontsize=8)
            axes[2].plot(lg,label="Left gripper")
            axes[2].plot(rg,label="Right gripper")
            axes[2].legend()
            for ax in axes: ax.grid(alpha=.2); ax.set_ylabel("Recorded action value")
            axes[2].set_xlabel("Recorded action index")
            fig.suptitle(f"14 action components | {mode}, seed 0",fontsize=16)
            fig.tight_layout(rect=(0,0,1,.96))
            save(fig,f"R2-action-components-{mode}.png","动作结构",row["hdf5"],
                 "Raw recorded values; do not compare across different controllers before checking units.")
            fig,axes=plt.subplots(3,3,figsize=(12,9))
            cams=["cam_head","cam_left_wrist","cam_right_wrist"]
            for col,cam in enumerate(cams):
                for ri,fraction in enumerate((0,.5,1)):
                    image,index=image_at(h,cam,fraction)
                    axes[ri,col].imshow(image)
                    axes[ri,col].set_title(f"{cam} | sample {index}",fontsize=10)
                    axes[ri,col].axis("off")
            fig.suptitle(f"Three synchronized cameras | {mode}, seed 0",fontsize=16)
            save(fig,f"R3-three-cameras-{mode}.png","多视角",row["hdf5"],
                 "Rows are beginning/middle/end sampled by index; columns are head/left wrist/right wrist.")
with (OUT/"R4-data-structure.csv").open("w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=list(struct[0]));w.writeheader();w.writerows(struct)
register("R4-data-structure.csv","数据结构表","Eight self-collected HDF5 files","Observation/action and video counts use separate definitions.")
fig,axes=plt.subplots(2,5,figsize=(15,6))
for ri,mode in enumerate(("clean","randomized")):
    for seed in range(5):
        ax=axes[ri,seed]
        row=by_mode[mode].get(seed)
        if row:
            with h5py.File(ROOT/"RoboTwin"/row["hdf5"],"r") as h:
                image,index=image_at(h,"cam_head",0)
            ax.imshow(image)
            ax.set_title(f"{mode} | seed {seed}",fontsize=10)
        else:
            ax.text(.5,.5,"No completed export\nSee attempt log",ha="center",va="center",transform=ax.transAxes,fontsize=11)
            ax.set_title(f"{mode} | seed {seed}",fontsize=10)
        ax.axis("off")
fig.suptitle("Five seed attempts per configuration",fontsize=16)
save(fig,"R5-seed-overview.png","跨种子对照","seed-attempts.csv and HDF5",
     "Blank cells identify failed trials; no replacement success was sampled.")
for seed in sorted(set(by_mode["clean"]) & set(by_mode["randomized"])):
    fig,axes=plt.subplots(2,3,figsize=(12,7))
    for ri,mode in enumerate(("clean","randomized")):
        row=by_mode[mode][seed]
        with h5py.File(ROOT/"RoboTwin"/row["hdf5"],"r") as h:
            for ax,frac in zip(axes[ri],(0,.5,1)):
                image,index=image_at(h,"cam_head",frac)
                ax.imshow(image)
                ax.set_title(f"{mode} | observation {index}",fontsize=11)
                ax.axis("off")
    fig.suptitle(f"Matched seed number {seed} | clean and randomized",fontsize=16)
    save(fig,f"R6-paired-seed{seed}.png","场景对照","Clean/randomized HDF5",
         "Same seed number does not guarantee identical sampled object poses when configurations draw different random variables.")
fig,ax=plt.subplots(figsize=(8,4))
ax.bar(["Clean","Randomized"],[5,3],color=["#287b6a","#ce8d42"],width=.55)
ax.set(ylim=(0,5.7),ylabel="Successful expert generations out of 5",
       title="Observed expert generation outcomes")
for i,n in enumerate((5,3)): ax.text(i,n+.1,f"{n}/5",ha="center",fontsize=13)
save(fig,"R7-generation-outcomes.png","结果统计","seed-attempts.csv",
     "Small-sample generation outcomes; not learned-policy robustness.")
for mode in ("clean","randomized"):
    text=(ROOT/f"RoboTwin/{mode}.log").read_text()
    text=re.sub(r"\x1b\[[0-9;]*m","",text).replace("\r","\n")
    selected=[line for line in text.splitlines() if any(s in line for s in (
        "simulate data episode","unstable objects","Complete simulation","exit code"))]
    (OUT/f"R8-{mode}-log-excerpt.txt").write_text("\n".join(selected)+"\n")
    register(f"R8-{mode}-log-excerpt.txt","原始证据摘录",f"RoboTwin/{mode}.log",
             "Exact lines with ANSI color codes removed.")
fig,ax=plt.subplots(figsize=(9,4))
for mode,marker in (("clean","o"),("randomized","s")):
    subset=[r for r in rows if r["condition"]==mode and r["frames"]]
    ax.plot([int(r["seed"]) for r in subset],[int(r["frames"])/30 for r in subset],marker+"-",label=mode)
ax.set(xlabel="Seed number",ylabel="Exported video duration (s)",title="Successful trajectory durations")
ax.set_xticks(range(5)); ax.legend(); ax.grid(alpha=.2)
save(fig,"R9-duration-by-seed.png","轨迹时长","Verified video frame counts at 30 FPS",
     "Duration variation is descriptive; only successful exports are included.")

smol=json.loads((ROOT/"SmolVLA/observations.json").read_text())
original=[r for r in smol if r["condition"]=="original"]
for ep in (0,1,2):
    screenshots=sorted((ROOT/"SmolVLA").glob(f"episode-{ep}-frame-*.png"),
                       key=lambda p:int(re.search(r"frame-(\d+)",p.name)[1]))
    fig,axes=plt.subplots(1,3,figsize=(12,4))
    for ax,p in zip(axes,screenshots):
        ax.imshow(plt.imread(p));ax.set_title(p.stem.replace(f"episode-{ep}-",""),fontsize=11);ax.axis("off")
    fig.suptitle(f"Recorded SO-101 observations | episode {ep}",fontsize=16)
    save(fig,f"S1-input-episode{ep}.png","SmolVLA 输入","SO-101 dataset screenshots",
         "Recorded observations; predicted actions were evaluated offline.")
per_episode=[]
for ep in (0,1,2):
    rs=[r for r in original if r["episode"]==ep]
    times=np.array([r["seconds"] for r in rs])
    per_episode.append(dict(episode=ep,count=len(rs),median_seconds=float(np.median(times)),
                            minimum_seconds=float(times.min()),maximum_seconds=float(times.max())))
with (OUT/"S2-latency-by-episode.csv").open("w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=list(per_episode[0]));w.writeheader();w.writerows(per_episode)
register("S2-latency-by-episode.csv","计时表","SmolVLA/observations.json",
         "Episode 0 includes the first call; other episodes do not.")
fig,ax=plt.subplots(figsize=(8,4))
for ep in (0,1,2):
    r=[r for r in original if r["episode"]==ep]
    ax.scatter([ep]*len(r),[x["seconds"] for x in r],alpha=.7,s=32)
ax.set(xticks=[0,1,2],xlabel="Episode",ylabel="Prediction and postprocessing (s)",title="All 30 offline inference timings")
ax.grid(axis="y",alpha=.2)
save(fig,"S3-latency-distribution.png","计时分布","SmolVLA/observations.json",
     "Thirty calls from three recorded trajectories; temporal samples are correlated.")
alt=next(r for r in smol if r["condition"]=="changed_instruction")
orig=next(r for r in original if r["frame"]==alt["frame"])
with (OUT/"S4-instruction-components.csv").open("w",newline="") as f:
    w=csv.writer(f);w.writerow(["component","original_output","replacement_output","difference"])
    w.writerows((i+1,a,b,b-a) for i,(a,b) in enumerate(zip(orig["predicted"],alt["predicted"])))
register("S4-instruction-components.csv","指令对照表","SmolVLA/observations.json",
         "Single matched observation, state and RNG seed; no action execution.")
(OUT/"manifest.json").write_text(json.dumps(entries,ensure_ascii=False,indent=2))
print(json.dumps({"new_png":len(list(OUT.glob("*.png"))),
                  "new_csv":len(list(OUT.glob("*.csv"))),
                  "log_excerpts":len(list(OUT.glob("*-log-excerpt.txt"))),
                  "indexed_materials":len(entries),"output":str(OUT)},ensure_ascii=False))
