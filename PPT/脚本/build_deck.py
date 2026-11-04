# -*- coding: utf-8 -*-
"""生成答辩 PPT：16 页正文 + 6 页问答备份。"""
import os
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE, "脚本"))

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

from theme import *          # noqa
import theme
from widgets import (arrow, chip, chip_row, bignum, stat_block, bar_chart,
                     seed_grid, legend_sq, note_card)

A = os.path.join(BASE, "素材", "整理")
IMG = lambda n: os.path.join(A, n)

prs = Presentation()
prs.slide_width = Inches(W)
prs.slide_height = Inches(H)

NAVY = RGBColor(0x00, 0x2E, 0x5E)
GOLD = RGBColor(0xC8, 0xA4, 0x4B)
PALE = RGBColor(0xB9, 0xCD, 0xE8)


def new(kicker=None, title=None, n=None, kicker_color=BLUE, title_size=27):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    bg(s)
    if kicker is not None:
        head(s, kicker, title, kicker_color=kicker_color, title_size=title_size)
    if n is not None:
        footer(s, n)
    return s


def notes(s, text):
    s.notes_slide.notes_text_frame.text = text


# ════════════════════════════════════════════ 01 封面
s = prs.slides.add_slide(prs.slide_layouts[6])
rect(s, 0, 0, W, H, fill=WHITE)
pic_cover(s, IMG("cover-bg.jpg"), 6.62, 0, W - 6.62, H, fx=0.97, fy=0.5)
rect(s, 0, 0, 6.62, H, fill=NAVY)
rect(s, 6.60, 0, 0.035, H, fill=GOLD)

pic_fit(s, IMG("gold-emblem.png"), 0.92, 0.62, 0.62, 0.56, align="left", valign="top")
pic_fit(s, IMG("gold-name.png"), 1.74, 0.80, 2.55, 0.62, align="left", valign="top")

T(s, 0.94, 1.72, 5.3, 0.30, "哈尔滨工业大学（威海）· 大一年度项目 · 结题答辩",
  size=11, color=PALE, bold=True, autofit=False)

T(s, 0.94, 2.10, 5.4, 1.72, "从两篇论文到一次\n可运行的复现", size=40, color=WHITE,
  bold=True, ls=1.20, autofit=False)

rect(s, 0.96, 4.00, 0.90, 0.05, fill=GOLD)

T(s, 0.94, 4.28, 5.55, 0.50,
  [("RoboTwin 2.0", True), (" 数据生成　×　", False), ("SmolVLA", True), (" 动作预测", False)],
  size=15.5, color=WHITE, autofit=False)

T(s, 0.94, 4.92, 5.3, 0.70,
  "两条线各跑通一段：仿真采集 8 条轨迹，离线推理 30 帧。\n闭环那一步，还没有接上。",
  size=11.5, color=PALE, ls=1.45)

hline(s, 0.96, 6.06, 4.9, RGBColor(0x3E, 0x64, 0x96), 0.9)

T(s, 0.94, 6.22, 5.4, 0.70,
  "汇报人：__________　　组员：____ ____ ____ ____ ____\n指导教师：________　　2026 年 11 月",
  size=9.5, color=RGBColor(0x92, 0xAB, 0xCC), ls=1.55)

T(s, 0.94, 7.02, 4.6, 0.26, "规格严格　功夫到家", size=9, color=RGBColor(0x6A, 0x86, 0xAE),
  autofit=False)

notes(s, "各位老师好。我们的大一年度项目做的是 RoboTwin 2.0 和 SmolVLA 两篇论文的小规模复现。"
         "标题里「可运行的复现」是这次的重点——不是读了论文，而是哪些环节真的跑起来了、哪些还没有。"
         "汇报 20 分钟，之后请老师提问。【约 30 秒】")

# ════════════════════════════════════════════ 02 问题
s = new("01 ｜ 问题", [("让机器人完成一次抓取，缺的从来不只是「一个模型」", True)], 2)

vline(s, 0.80, 1.62, 0.44, BLUE, 2.2)
T(s, 1.04, 1.62, 10.4, 0.44, "把粉色积木放进透明盒里 —— 这一句话里，藏着三个要分别解决的问题",
  size=13, color=INK2, ls=1.3)

stages = [
    ("01", "示范从哪来", "仿真能反复生成带标注、带动作的轨迹；真机采集慢、贵，而且难以复现。", "→ RoboTwin 2.0"),
    ("02", "看到怎么动", "把画面、关节状态和一句指令，变成本该接下来的一串连续动作。", "→ SmolVLA"),
    ("03", "怎么算完成", "物体到没到、夹爪开没开，必须由环境按规则判定，不能看图猜。", "→ 闭环评测"),
]
xw = 3.42
for i, (num, ttl, body, tail) in enumerate(stages):
    x = 0.78 + i * (xw + 0.72)
    hline(s, x, 2.30, xw, LINE, 1.2)
    T(s, x, 2.42, 0.6, 0.30, num, size=10.5, color=BLUE, bold=True, autofit=False)
    T(s, x, 2.74, xw, 0.40, ttl, size=19, color=INK, bold=True, autofit=False)
    T(s, x, 3.26, xw - 0.18, 0.92, body, size=12, color=INK2, ls=1.45)
    T(s, x, 4.24, xw, 0.28, tail, size=10, color=BLUE_L, bold=True, autofit=False)
    if i < 2:
        arrow(s, x + xw + 0.14, 2.94, x + xw + 0.54, 2.94, FAINT, 1.0)

rect(s, 0.78, 4.72, CW, 1.02, fill=BLUE_T)
T(s, 1.02, 4.86, 1.6, 0.26, "本项目", size=9.5, color=BLUE, bold=True, autofit=False)
T(s, 1.02, 5.14, CW - 0.5, 0.50,
  [("①② 各做了一段实证", True),
   ("　RoboTwin 侧完成两组仿真采集，SmolVLA 侧完成 30 帧离线推理。　", False),
   ("③ 闭环执行与成功率判定，本次没有做。", True)],
  size=12, color=INK2, ls=1.3)

T(s, 0.78, 5.98, CW, 0.60,
  "所以这份汇报的每一页，基本都在回答这条链上某一个具体问题：数据长什么样、怎么采、模型输出什么、还差哪一步。",
  size=11, color=MUTED, ls=1.35)

notes(s, "先从问题说起。机器人要完成「把积木放进盒子」，需要三样东西：足够多的示范、能从画面算动作的模型、"
         "以及一个能判定成功的环境。这三件事我们都碰到了，但只有前两件各自做完一段，第三件没有接起来。"
         "这一页先把话说明白。【约 1 分钟】")

# ════════════════════════════════════════════ 03 两篇论文
s = new("02 ｜ 论文", [("一篇负责「造出可执行的示范」，一篇负责「从画面直接算动作」", True)], 3)

lx, lw = 0.78, 5.62
T(s, lx, 1.72, lw, 0.26, "RoboTwin 2.0　｜　数据生成 + 基准", size=10, color=BLUE, bold=True, autofit=False)
pic_fit(s, IMG("rt-pipeline.png"), lx, 2.04, lw, 2.06)
T(s, lx, 4.20, lw, 0.26, "Chen 等，2025，图 2 · 论文原图", size=8.6, color=FAINT, autofit=False)
T(s, lx, 4.54, lw - 0.10, 0.95,
  "多模态模型写候选专家程序，在仿真里跑、看回渲染图找错误、再改代码；"
  "跑通后用五类随机化扩增场景，导出带动作的示范。",
  size=11, color=INK2, ls=1.42)

rx, rw = 6.95, 5.60
T(s, rx, 1.72, rw, 0.26, "SmolVLA　｜　视觉-语言-动作模型", size=10, color=BLUE, bold=True, autofit=False)
pic_fit(s, IMG("svla-arch.png"), rx, 2.04, rw, 2.06)
T(s, rx, 4.20, rw, 0.26, "Shukor 等，2025，图 1 · 论文原图", size=8.6, color=FAINT, autofit=False)
T(s, rx, 4.54, rw - 0.10, 0.95,
  "把 VLM 主干末端若干层剪掉，接上 Action Expert；用流匹配一次预测一段连续动作块，"
  "配合异步推理减少等待。",
  size=11, color=INK2, ls=1.42)

rect(s, 0.78, 5.62, CW, 1.16, fill=None, line=LINE2, lw=1.0)
cov = [("RoboTwin 侧", "公开数据核查\nColab 环境\n两组自采 8 条轨迹", BLUE),
       ("SmolVLA 侧", "单帧推理\n30 帧批量推理\n一次指令替换", BLUE),
       ("未覆盖", "把两者接起来的\n闭环执行与评测", RED)]
for i, (t_, b_, c_) in enumerate(cov):
    x = 1.02 + i * 3.86
    T(s, x, 5.76, 3.5, 0.24, t_, size=9.2, color=c_, bold=True, autofit=False)
    T(s, x, 6.02, 3.5, 0.68, b_, size=9.6, color=INK2, ls=1.30)

notes(s, "两篇论文分工很清楚。左边 RoboTwin 解决「示范从哪来」：让大模型写专家程序，在仿真里跑，"
         "看渲染图找错误，再改代码，跑通了就大量导出轨迹。右边 SmolVLA 解决「看到怎么动」："
         "用剪枝后的 VLM 当大脑、动作专家当手，一次输出一小段动作。我们只做了论文链路里的两个切片。"
         "【约 1.5 分钟】")

# ════════════════════════════════════════════ 04 工作概览
s = new("03 ｜ 工作概览", [("六个环节，前五个跑通，最后一个「接起来」没有做", True)], 4)

steps = [
    ("01", "读论文与代码", "读两篇论文，跑通官方入口，确认哪些部分我们能动", True),
    ("02", "搭 Colab 环境", "T4 单卡，独立 Python 环境，14.93 GB 官方资源", True),
    ("03", "分析公开数据", "读 27,500 段转换数据，核对帧数、维数、指令", True),
    ("04", "两组仿真采集", "交接任务，固定与随机场景各 5 个种子，导出 8 条", True),
    ("05", "30 帧离线推理", "3 条轨迹 × 10 帧，加一次同画面指令替换", True),
    ("06", "接口对齐 + 闭环", "6 维预测怎么驱动 14 维双臂，成功率怎么统计", False),
]
sw = (CW - 5 * 0.30) / 6
hline(s, 0.78, 2.34, CW, LINE, 1.0)
for i, (num, ttl, body, done) in enumerate(steps):
    x = 0.78 + i * (sw + 0.30)
    col = BLUE if done else RED
    rect(s, x, 2.26, 0.15, 0.15, fill=col, shape=MSO_SHAPE.OVAL)
    T(s, x, 2.56, sw, 0.24, num, size=9.5, color=col, bold=True, autofit=False)
    T(s, x, 2.84, sw - 0.06, 0.62, ttl, size=13, color=INK, bold=True, ls=1.25)
    T(s, x, 3.54, sw - 0.10, 1.05, body, size=9.6, color=MUTED, ls=1.42)
    T(s, x, 4.38, sw, 0.24, "已完成" if done else "未完成", size=9.2, color=col, bold=True, autofit=False)

rect(s, 0.78, 5.18, CW, 0.025, fill=LINE2)
facts = [("27,500", "段公开轨迹已核验"), ("8", "条团队自采轨迹（视频 + HDF5）"),
         ("30", "帧离线推理，另加 1 次指令替换")]
cx = 0.80
for num, lab in facts:
    cx += stat_block(s, cx, 5.52, num, lab, size=30) + 0.55

notes(s, "这是我们实际走过的路。前三步是打地基：读论文、把环境装到能用、把公开数据读明白。"
         "第四第五步是我们自己产出的两组数据。第六步接口对齐和闭环评测没做完，"
         "第 15 页会专门讲为什么没做完、下一步怎么补。【约 1 分钟】")

# ════════════════════════════════════════════ 05 数据结构
s = new("04 ｜ 数据结构", [("一条轨迹不只是一段视频：三路画面 + 14 维动作 + 一句指令", True)], 5)

pic_fit(s, IMG("rt-episode0.png"), 0.78, 1.84, 4.42, 3.32, align="left", valign="top")
T(s, 0.78, 5.22, 4.42, 0.28, "公开数据第 0 段 · 顶部相机 · 139 帧 ≈ 4.63 s", size=9, color=MUTED, autofit=False)

rx = 5.60
cx = rx
for v, k in [("27,500", "轨迹"), ("6,075,103", "帧"), ("30", "FPS"), ("165", "中位帧数")]:
    cx += stat_block(s, cx, 1.82, v, k, size=21, color=BLUE, gap=0.42)
hline(s, rx, 2.66, W - MX - rx, LINE2, 0.9)

T(s, rx, 2.80, 3.6, 0.24, "动作向量 = 14 维", size=10, color=INK, bold=True, autofit=False)
T(s, rx + 1.90, 2.80, 5.0, 0.24, "每一维 = 一个关节或夹爪的角度 / 开合", size=9, color=MUTED, autofit=False)

names = ["left_waist", "left_shoulder", "left_elbow", "left_forearm_roll",
         "left_wrist_angle", "left_wrist_rotate", "left_gripper",
         "right_waist", "right_shoulder", "right_elbow", "right_forearm_roll",
         "right_wrist_angle", "right_wrist_rotate", "right_gripper"]
cw_, gap = 0.415, 0.062
for i, nm in enumerate(names):
    x = rx + i * (cw_ + gap)
    fill = BLUE if i < 7 else TEAL
    rect(s, x, 3.12, cw_, 0.42, fill=fill)
    if nm.endswith("gripper"):
        rect(s, x, 3.12, cw_, 0.42, fill=None, line=WHITE, lw=1.5)
    T(s, x, 3.12, cw_, 0.42, str(i + 1), size=9.5, color=WHITE,
      align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, autofit=False)

rect(s, rx, 3.68, 0.115, 0.115, fill=BLUE)
T(s, rx + 0.20, 3.62, 3.4, 0.26, "左臂 6 关节 + 左夹爪（第 7 维）", size=8.8, color=BLUE, autofit=False)
rect(s, rx + 3.86, 3.68, 0.115, 0.115, fill=TEAL)
T(s, rx + 4.06, 3.62, 3.0, 0.26, "右臂 6 关节 + 右夹爪（第 14 维）", size=8.8, color=TEAL, autofit=False)

T(s, rx, 4.10, 4.2, 0.24, "观察 = 三路相机 + 状态 + 指令文本", size=10, color=INK, bold=True, autofit=False)
chip(s, rx, 4.42, "cam_high 顶部", size=9.2, h=0.30)
chip(s, rx + 1.40, 4.42, "cam_left_wrist 左腕", size=9.2, h=0.30)
chip(s, rx + 3.12, 4.42, "cam_right_wrist 右腕", size=9.2, h=0.30)

note_card(s, 0.78, 5.62, CW, 1.00, "一个必须先对齐的细节",
          "团队自采第一条：视频 289 帧，HDF5 里 288 条状态与动作记录。差 1 不是丢数据，"
          "而是「帧」与「状态转移」的计数口径不同 —— 不先对齐，后面比长度、比速度都会错。",
          accent=BLUE, fill=BLUE_T, title_size=10)

notes(s, "这一页回答「一条机器人轨迹里到底有什么」。左边是公开数据的一个真实画面，注意是 AGILE X 双臂。"
         "右边是数据结构：14 个数，左臂 6 个关节加一个夹爪，右臂 6 个关节加一个夹爪。"
         "最后那条提示很重要：我们自采的第一条，视频 289 帧、HDF5 里 288 条记录，这个 1 就是计数口径问题。"
         "【约 1.5 分钟】")

# ════════════════════════════════════════════ 06 环境排错
s = new("05 ｜ 环境", [("三个报错，一条顺序：先读报错 → 确认实际环境 → 最小测试", True)], 6)

rows = [
    ("01", "ERROR: Could not find a version that satisfies the requirement sapien==3.0.0b1",
     "官方 requirements 锁死这个版本，它只发布到 Python 3.10；Colab 默认 3.13 找不到对应 wheel。",
     "uv 建 3.10.22 独立解释器，在这个环境里装 —— 而不是去改整个 Colab 的 Python。"),
    ("02", "ModuleNotFoundError: No module named 'pkg_resources'",
     "SAPIEN 3.0.0b1 启动时 import pkg_resources，而 setuptools ≥ 81 已把它移除。",
     "固定 setuptools==80.10.2，最小相机测试返回 (64, 64, 4) 的 RGBA 数组，渲染通了。"),
    ("03", "PyTorch 2.4.1+cu121　vs　系统编译器 CUDA 13",
     "扩展编译要用 Torch 的 CUDA 版本，而不是系统那一套；CuRobo 还要指定目标架构。",
     "补 CUDA 12.8 工具链，把 CuRobo v0.7.8 的编译目标限定为 T4 的 sm_75。"),
]
y = 1.78
for num, err, why, fix in rows:
    T(s, 0.78, y + 0.06, 0.4, 0.28, num, size=9.8, color=FAINT, bold=True, autofit=False)
    rect(s, 1.26, y, 5.26, 0.66, fill=RGBColor(0xF3, 0xF4, 0xF6))
    rect(s, 1.26, y, 0.045, 0.66, fill=RED)
    T(s, 1.44, y + 0.08, 4.92, 0.50, err, size=9.0,
      color=RGBColor(0x8C, 0x2F, 0x24), ls=1.24)
    T(s, 6.84, y + 0.02, 5.9, 0.30, why, size=10.2, color=INK2, ls=1.3)
    T(s, 6.84, y + 0.38, 5.9, 0.34, [("→ ", True), (fix, False)], size=10.2, color=INK2, ls=1.3)
    y += 1.20

rect(s, 0.78, 5.52, CW, 0.86, fill=None, line=LINE2, lw=1.0)
T(s, 1.02, 5.64, 2.4, 0.24, "最后的验证", size=9.5, color=BLUE, bold=True, autofit=False)
T(s, 1.02, 5.92, CW - 0.5, 0.40,
  [("14.93 GB 官方资源（机器人 / 物体 / 纹理）就位后，官方入口报告 ", False), ("Render Well", True),
   ("，进入双臂任务 —— 此后所有报错都只和任务有关。", False)],
  size=11, color=INK2, ls=1.3)

notes(s, "这一页只讲两个有代表性的困难。第一个是版本死锁：官方锁的 SAPIEN 只有 Python 3.10 的包，"
         "而 Colab 默认 3.13，正确做法是给项目单独建解释器。"
         "第二个更隐蔽：包装上了，但一 import 就缺 pkg_resources，因为 setuptools 81 把它删了。"
         "第三个是编译链不匹配。总结的顺序就是标题这句。【约 1 分钟】")

# ════════════════════════════════════════════ 07 实验设计
s = new("06 ｜ 实验设计", [("只改一处：同任务、同机器人、同种子编号，两组各试五次", True)], 7)

T(s, 0.78, 1.76, 6.0, 0.24, "A　控制住的条件（两组完全相同）", size=9.5, color=BLUE, bold=True, autofit=False)
chip_row(s, 0.78, 2.06, ["任务 handover_block", "机器人 ALOHA AgileX", "三路相机",
                         "30 FPS 采样", "语言由官方模板生成", "保存格式"],
         h=0.32, size=9.6, max_w=5.95)

T(s, 0.78, 3.02, 6.0, 0.24, "B　改变的条件（官方 demo_randomized）", size=9.5, color=RED, bold=True, autofit=False)
chip_row(s, 0.78, 3.32, ["桌面背景", "桌面杂物", "光照", "桌面高度"],
         h=0.32, size=9.6, color=RED, fill=RED_T)
T(s, 0.78, 3.78, 5.85, 0.28, "四项同时打开 —— 只能说「整体更难的场景」，不能归因到某一项。",
  size=9.4, color=MUTED, ls=1.25)

T(s, 0.78, 4.28, 6.0, 0.24, "C　计数规则（防止把失败从统计里删掉）", size=9.5, color=BLUE, bold=True, autofit=False)
rules = ["种子固定 0–4，失败也计入分母，报告「成功数 / 尝试数」",
         "回放数量 = 实际成功条数，不用补帧凑数",
         "单组最多尝试 5 次，避免无限搜索掩盖问题"]
for i, r in enumerate(rules):
    T(s, 0.80, 4.58 + i * 0.33, 5.9, 0.30, f"·　{r}", size=9.8, color=INK2, ls=1.2)

rx = 7.10
rect(s, rx, 1.74, 5.45, 1.90, fill=None, line=LINE2, lw=1.0)
T(s, rx + 0.24, 1.90, 4.9, 0.24, "成功判定由官方任务代码给出，不是我们自定的", size=9.2, color=BLUE, bold=True, autofit=False)
for i, (k, v) in enumerate([("平面两方向距离", "< 3 cm"), ("高度差", "< 1 cm"), ("右夹爪", "已打开")]):
    T(s, rx + 0.24, 2.24 + i * 0.42, 3.0, 0.30, k, size=10, color=INK2, autofit=False)
    T(s, rx + 3.30, 2.24 + i * 0.42, 1.9, 0.30, v, size=11.5, color=INK, bold=True, autofit=False)

T(s, rx, 3.92, 5.4, 0.24, "为什么这样设计", size=9.5, color=BLUE, bold=True, autofit=False)
why = [("可复现", "提交号、种子、配置都写进日志，任何人能重跑"),
       ("可对照", "两组差别只有一处，差异才能归因于它"),
       ("可承认", "失败原因写得出来，比成功率高更有说服力")]
for i, (k, v) in enumerate(why):
    T(s, rx, 4.24 + i * 0.60, 0.95, 0.28, k, size=9.8, color=BLUE, bold=True, autofit=False)
    T(s, rx + 1.02, 4.24 + i * 0.60, 4.3, 0.50, v, size=9.9, color=INK2, ls=1.25)

T(s, 0.78, 5.98, CW, 0.30,
  "一句话：这十次尝试的价值不在于「8 比 5」，而在于每一次都能说出为什么。",
  size=10, color=MUTED, autofit=False)

notes(s, "实验设计就一句话：只改一处。A 区条件两组完全一样，B 区是官方随机化打开的四项，C 区是我们自己加的计数规则。"
         "特别注意第一条：失败也算分母。右边是官方给的判定标准，不是我们定的。"
         "【约 1.5 分钟】")

# ════════════════════════════════════════════ 08 交接任务
s = new("07 ｜ 任务", [("抓起 → 交接 → 放置：一次交接要两只手都算准", True)], 8)

stages = [
    ("阶段 1", "左臂抓起", "左臂接近桌面上的红色长方体，闭合左夹爪把它提起。", "记录：左臂 6 关节 + 左夹爪"),
    ("阶段 2", "中间交接", "两条手臂在中间区域靠近，右夹爪接住，左夹爪松开。", "记录：双臂同时动作，易插手部碰撞"),
    ("阶段 3", "放到目标", "右臂移到目标位置，正对目标区，右夹爪打开放下。", "记录：判定看距离、高度、夹爪状态"),
]
sw2 = 3.55
for i, (tag_, ttl, body, rec) in enumerate(stages):
    x = 0.78 + i * (sw2 + 0.56)
    rect(s, x, 1.94, sw2, 2.06, fill=WHITE, line=LINE2, lw=1.0)
    T(s, x + 0.26, 2.12, sw2 - 0.4, 0.24, tag_, size=8.8, color=BLUE, bold=True, autofit=False)
    T(s, x + 0.26, 2.42, sw2 - 0.4, 0.36, ttl, size=16, color=INK, bold=True, autofit=False)
    T(s, x + 0.26, 2.86, sw2 - 0.50, 0.66, body, size=10.2, color=INK2, ls=1.38)
    T(s, x + 0.26, 3.62, sw2 - 0.46, 0.28, rec, size=8.4, color=FAINT, ls=1.2)
    if i < 2:
        arrow(s, x + sw2 + 0.10, 2.96, x + sw2 + 0.44, 2.96, FAINT, 1.0)

T(s, 0.78, 4.24, 6.0, 0.24, "一条成功轨迹的实际记录（固定场景 · 种子 0）", size=9.5, color=BLUE, bold=True, autofit=False)
cx = 0.78
for v, k in [("289", "视频帧"), ("30", "FPS"), ("9.63 s", "时长"), ("288", "状态/动作条"), ("320×240", "分辨率")]:
    cx += stat_block(s, cx, 4.56, v, k, size=21, color=INK, gap=0.62)

rect(s, 0.78, 5.42, CW, 0.025, fill=LINE2)
T(s, 0.78, 5.60, CW, 0.28,
  [("总计：两组共导出 ", False), ("8 条视频 + 8 份可打开的 HDF5", True),
   ("，合计约 151 MiB；每条都带关节、末端位姿、动作和语言指令。", False)],
  size=11, color=INK2, ls=1.3)
T(s, 0.78, 6.02, CW, 0.62,
  "要说清的一点：这一步是「专家程序能跑通并导出数据」，不等于「学出来的策略能完成任务」。"
  "前者由规划器保证，后者才需要训练和评测。",
  size=10.5, color=MUTED, ls=1.4)

notes(s, "这个任务叫 handover_block：左臂抓起红色方块，在中间交给右臂，右臂放到目标位置。"
         "分三个阶段是因为失败点不同：抓取段容易滑，交接段容易撞，放置段容易差几厘米。"
         "下面是种子 0 的真实记录。最重要的是最后一句——这是专家轨迹，不是学习策略的成绩。"
         "【约 1.5 分钟，可配合 10 秒录屏】")

# ════════════════════════════════════════════ 09 随机化
s = new("08 ｜ 随机化", [("随机化改的是「桌子上的世界」，不是任务目标", True)], 9)

pic_fit(s, IMG("rt-randomization.png"), 0.78, 1.80, 6.42, 2.56, align="left", valign="top")
T(s, 0.78, 4.46, 6.42, 0.44,
  "Chen 等，2025，图 4：左列固定场景，中列杂物 / 光照 / 桌面高度 / 背景同时变化，右列 12k 纹理库（论文原图）",
  size=8.4, color=FAINT, ls=1.25)

rx = 7.55
T(s, rx, 1.78, 4.9, 0.24, "论文定义的五类变化", size=9.5, color=BLUE, bold=True, autofit=False)
items = [("桌面杂物", "本轮启用", True), ("光照", "本轮启用", True), ("桌面背景", "本轮启用", True),
         ("桌面高度", "本轮启用", True), ("语言指令", "官方模板，未做替换", False)]
for i, (k, v, on) in enumerate(items):
    y = 2.12 + i * 0.44
    rect(s, rx, y + 0.09, 0.13, 0.13, fill=BLUE if on else LINE, shape=MSO_SHAPE.OVAL)
    T(s, rx + 0.26, y + 0.02, 2.0, 0.28, k, size=10.5, color=INK, autofit=False)
    T(s, rx + 2.10, y + 0.03, 2.7, 0.26, v, size=9, color=BLUE if on else FAINT, autofit=False)

T(s, 0.78, 4.80, 6.35, 0.42,
  "变难在哪：杂物遮挡目标 · 光照改变颜色统计 · 背景干扰分割 · 桌高改变相机相对位姿",
  size=9.2, color=MUTED, ls=1.3)

T(s, rx, 4.38, 4.9, 0.85,
  "为什么研究它：训练时见过的桌子越少，真机换个桌面就越容易失效。随机化把「见过的世界」变宽，"
  "代价是采集更难。",
  size=10, color=INK2, ls=1.40)

note_card(s, 0.78, 5.56, CW, 1.10, "讲这一页时最容易说错的一句话",
          "「相同种子编号 = 相同初始位姿」并不成立。两套配置调用随机数的次数和顺序不同，"
          "即使都是 seed 0，物体位置也可能不一样 —— 所以配对图只能比「场景风格」，不能比「同一物体的两次尝试」。",
          accent=RED, fill=RED_T, title_size=10)

notes(s, "随机化是 RoboTwin 的核心卖点之一。左边是论文原图：同一个小碗、同一双鞋，"
         "左列是干净桌面，中列是杂物、光照、桌面高度、背景全变。右边是我们本轮实际启用的四项。"
         "这里有个容易被问倒的点，我先说：同一个种子编号在两套配置下不一定摆出同样的物体。"
         "【约 1.5 分钟】")

# ════════════════════════════════════════════ 10 结果
s = new("09 ｜ 结果", [("固定场景 5/5，随机场景 3/5；三次失败都留在统计里", True)], 10)

T(s, 0.78, 1.72, 3.9, 0.24, "专家轨迹生成结果", size=9.2, color=MUTED, autofit=False)
bar_chart(s, 0.86, 2.06, 3.30, 2.86,
          [("固定场景", 5, BLUE, "5 / 5"), ("随机场景", 3, RED, "3 / 5")], 5)

gx = 4.86
seed_grid(s, gx, 2.30, 0.56, 0.44, 0.16,
          [("固定", [True, True, True, True, True]),
           ("随机", [True, False, False, True, True])],
          header=["0", "1", "2", "3", "4"])
T(s, gx + 0.02, 2.02, 1.2, 0.24, "种子编号", size=8.8, color=FAINT, autofit=False)

nx = gx + 0.02
nx += legend_sq(s, nx, 3.86, BLUE, "通过", True)
legend_sq(s, nx, 3.86, RED, "未通过", False)
T(s, gx, 4.24, 4.0, 1.10,
  "随机组失败的是种子 1 和 2。同一个种子编号在两组里都算「一次尝试」，"
  "没有因为失败被剔除，也没有补跑。",
  size=9.8, color=INK2, ls=1.40)

lx2 = 9.30
rect(s, lx2, 1.86, 3.24, 3.50, fill=WHITE, line=LINE2, lw=1.0)
T(s, lx2 + 0.24, 2.02, 2.7, 0.24, "日志告诉我们什么", size=9.4, color=BLUE, bold=True, autofit=False)
T(s, lx2 + 0.24, 2.34, 2.7, 0.26, "种子 2 · 随机场景", size=8.8, color=MUTED, autofit=False)
T(s, lx2 + 0.24, 2.60, 2.70, 0.60, "「杂物酒杯不稳定」", size=12.5, color=RED, bold=True, ls=1.2)
T(s, lx2 + 0.24, 3.24, 2.70, 0.92,
  "失败发生在场景初始化：杂物里的酒杯没站稳，物理上先塌了。问题在场景，不在规划器。",
  size=9.6, color=INK2, ls=1.38)
hline(s, lx2 + 0.24, 4.14, 2.70, LINE2, 0.75)
T(s, lx2 + 0.24, 4.24, 2.70, 0.26, "种子 1 · 随机场景", size=8.8, color=MUTED, autofit=False)
T(s, lx2 + 0.24, 4.50, 2.70, 0.70, "日志信息不足，本轮没有定位到根因 —— 保留为待查。",
  size=9.6, color=INK2, ls=1.38)

rect(s, 0.78, 5.68, CW, 0.86, fill=BLUE_T)
T(s, 0.78, 5.82, CW, 0.24, "口径提醒", size=9.2, color=BLUE, bold=True,
  align=PP_ALIGN.CENTER, autofit=False)
T(s, 0.78, 6.08, CW, 0.34,
  "每格只有 5 次、没有重复实验，不能据此推断成功率；这是「专家轨迹能不能生成」，不是「学习策略能不能泛化」。",
  size=10, color=INK2, align=PP_ALIGN.CENTER, autofit=False)

notes(s, "结果很简单：固定场景五个种子全过，随机场景过了三个。这个图我特意把分母标出来，因为「5 比 3」本身没有统计意义，"
         "只有「5/5 对 3/5」才是可比较的。右边是种子格，失败的两个是种子 1 和 2，都没有删。"
         "种子 2 的日志给了很具体的线索：杂物里的酒杯不稳，是场景初始化阶段就塌了。种子 1 查不出来，就写「待查」。"
         "【约 1.5 分钟】")

# ════════════════════════════════════════════ 11 模型前向
s = new("10 ｜ 模型", [("输入是三样东西，输出是六个连续数", True)], 11)

T(s, 0.78, 1.72, 6.0, 0.24, "前向一次的计算路径（简化）", size=9.2, color=MUTED, autofit=False)
for x, t1, t2 in [(0.78, "图像 ×3", "side / up / up"),
                  (2.22, "状态", "SO-101 关节"),
                  (3.66, "指令", "一句英文")]:
    rect(s, x, 2.06, 1.22, 0.86, fill=BLUE_T)
    T(s, x, 2.16, 1.22, 0.26, t1, size=10, color=BLUE, bold=True, align=PP_ALIGN.CENTER, autofit=False)
    T(s, x, 2.44, 1.22, 0.26, t2, size=8.2, color=MUTED, align=PP_ALIGN.CENTER, autofit=False)

for x in (1.39, 2.83, 4.27):
    vline(s, x, 2.92, 0.30, LINE, 1.0)
hline(s, 1.39, 3.22, 2.88, LINE, 1.0)
vline(s, 2.83, 3.22, 0.22, BLUE_L, 1.2)

rect(s, 0.78, 3.46, 4.28, 0.60, fill=BLUE)
T(s, 0.78, 3.46, 4.28, 0.60, "VLM 主干（剪掉末端层）", size=10.5, color=WHITE, bold=True,
  align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, autofit=False)
arrow(s, 2.83, 4.06, 2.83, 4.22, BLUE_L, 1.2)

rect(s, 0.78, 4.24, 4.28, 0.60, fill=WHITE, line=BLUE, lw=1.2)
T(s, 0.78, 4.24, 4.28, 0.60, "Action Expert ＋ 流匹配去噪", size=10.5, color=BLUE, bold=True,
  align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, autofit=False)
arrow(s, 2.83, 4.84, 2.83, 5.00, INK, 1.2)

rect(s, 0.78, 5.02, 4.28, 0.60, fill=INK)
T(s, 0.78, 5.02, 4.28, 0.60, "动作：1 × 6", size=11.5, color=WHITE, bold=True,
  align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, autofit=False)

T(s, 0.78, 5.80, 4.30, 0.80, "加载后只做前向：不复训、不微调，用公开预训练权重直接算。",
  size=9.8, color=MUTED, ls=1.35)

rx = 5.72
T(s, rx, 1.72, 6.6, 0.24, "本轮真实输出（SO-101 第 0 帧，side + up 两路画面）", size=9.2, color=MUTED, autofit=False)
T(s, rx, 2.02, 5.9, 0.28,
  [("450,046,176", True), (" 参数　·　首次动作 ", False), ("1.76 s", True), ("（含后处理）", False)],
  size=10, color=INK2, autofit=False)

vals = [0.4353, -0.2852, -0.6141, 0.6141, 1.2733, -0.8516]
base_y, maxabs = 4.16, 1.30
for i, v in enumerate(vals):
    x = rx + 0.14 + i * 0.94
    hh = abs(v) / maxabs * 1.02
    if v >= 0:
        rect(s, x, base_y - hh, 0.56, hh, fill=BLUE)
        T(s, x - 0.10, base_y - hh - 0.32, 0.76, 0.26, f"{v:+.2f}", size=8.4, color=BLUE,
          align=PP_ALIGN.CENTER, autofit=False)
    else:
        rect(s, x, base_y, 0.56, hh, fill=RED)
        T(s, x - 0.10, base_y + hh + 0.05, 0.76, 0.26, f"{v:+.2f}", size=8.4, color=RED,
          align=PP_ALIGN.CENTER, autofit=False)
    T(s, x - 0.10, base_y + 0.98, 0.76, 0.22, f"a{i+1}", size=8.2, color=FAINT,
      align=PP_ALIGN.CENTER, autofit=False)
hline(s, rx, base_y, 5.72, INK, 1.0)

note_card(s, rx, 5.52, 6.83, 1.06, "这就是「接不上」的直接原因",
          "RoboTwin 的动作是 14 维（双臂各 6 关节 + 各 1 夹爪），这份权重输出 6 维。"
          "接起来至少要核对：机器人形态、关节顺序、单位、动作表示、归一化。",
          accent=RED, fill=RED_T, title_size=10)

notes(s, "模型这边，输入是两到三路图像、机器人状态和一句英文指令，先过 VLM 主干，"
         "再进动作专家，用流匹配去噪，一次吐出六个动作。右边这六个数是真的，来自第 0 帧。"
         "「这六个数是不是角度」—— 我们不能确认，记录里没有核对单位和缩放。"
         "最后的红卡是重点：输出 6 维，目标 14 维。【约 1.5 分钟】")

# ════════════════════════════════════════════ 12 计时
s = new("11 ｜ 测量", [("首条 1.95 秒，其余中位数 0.91 秒 —— 比数字更重要的是计时边界", True)], 12)

for i, (v, k, c) in enumerate([("1.954 s", "第 1 条（含初始化）", RED),
                              ("0.911 s", "其余 29 条中位数", BLUE),
                              ("1.140 s", "其余 29 条 P90", BLUE)]):
    x = 0.78 + i * 3.95
    T(s, x, 1.78, 3.6, 0.62, v, size=36, color=c, bold=True, autofit=False)
    T(s, x, 2.46, 3.6, 0.26, k, size=10, color=MUTED, autofit=False)

ax0, ax1, ay = 1.60, 12.30, 3.62
lo, hi = 0.80, 2.10
mx = lambda v: ax0 + (v - lo) / (hi - lo) * (ax1 - ax0)

# 集中区间底纹
rect(s, mx(0.911), ay + 0.02, mx(1.140) - mx(0.911), 0.16, fill=RGBColor(0xD7, 0xE2, 0xF1))

hline(s, ax0 - 0.15, ay, ax1 - ax0 + 0.30, LINE, 1.2)
for t in [0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0]:
    vline(s, mx(t), ay - 0.07, 0.14, LINE, 1.0)
    T(s, mx(t) - 0.30, ay + 0.24, 0.60, 0.22, f"{t:.1f}", size=8.2, color=FAINT,
      align=PP_ALIGN.CENTER, autofit=False)

for v, tag_, c in [(0.911, "中位数", BLUE), (1.140, "P90", BLUE), (1.954, "第 1 条", RED)]:
    x = mx(v)
    rect(s, x - 0.085, ay - 0.085, 0.17, 0.17, fill=c, shape=MSO_SHAPE.OVAL)
    T(s, x - 0.62, ay - 0.46, 1.24, 0.30, tag_, size=10, color=c, bold=True,
      align=PP_ALIGN.CENTER, autofit=False)

T(s, ax0 - 0.15, ay + 0.54, 8.6, 0.24,
  "单次离线推理耗时（秒）；浅色区间为其余 29 条的集中范围（中位数 → P90）",
  size=8.4, color=FAINT, autofit=False)

T(s, 0.78, 4.62, 5.6, 0.24, "实验怎么做的", size=9.4, color=BLUE, bold=True, autofit=False)
T(s, 0.78, 4.92, 5.55, 1.40,
  "三条录制轨迹各取 10 个等距时间点，共 30 个样本。每帧独立重置动作队列并固定随机种子，"
  "避免把上一帧队列里的动作误当成新预测。",
  size=10, color=INK2, ls=1.45)

T(s, 6.90, 4.62, 5.7, 0.24, "计时算了什么 / 没算什么", size=9.4, color=BLUE, bold=True, autofit=False)
T(s, 6.90, 4.92, 5.70, 1.40,
  [("计入：", True), ("GPU 同步后的预测 + 动作后处理。\n", False),
   ("排除：", True), ("模型加载、视频解码、输入预处理。\n", False),
   ("不能推广到：", True), ("稳定吞吐、端侧速度、任务成功率。", False)],
  size=9.8, color=INK2, ls=1.45)

rect(s, 0.78, 6.06, CW, 0.70, fill=BLUE_T)
T(s, 1.02, 6.18, 1.6, 0.24, "所以能说什么", size=9.2, color=BLUE, bold=True, autofit=False)
T(s, 1.02, 6.44, CW - 0.5, 0.28,
  "能说：在这批输入上，一次前向（含后处理）平均零点九秒左右，偶发到一点一秒。不能说：端侧能不能实时，任务成功率是多少。",
  size=10.2, color=INK2, autofit=False)

notes(s, "三十次推理，第一条 1.95 秒，后面中位数 0.91，P90 是 1.14。第一条高是因为有初始化和缓存预热。"
         "我画成一条数轴而不是三根柱子，因为三根柱子容易让人以为是三种条件。真正要讲的是边界："
         "不含模型加载和数据预处理，而且 30 个样本来自 3 条轨迹、帧间相关，不是 30 次独立实验。"
         "【约 1.5 分钟】")

# ════════════════════════════════════════════ 13 指令替换
s = new("12 ｜ 干预", [("只改一句话，六个分量全部改变，输出向量移动了 0.623", True)], 13)

rect(s, 0.78, 1.84, 6.05, 0.98, fill=WHITE, line=LINE2, lw=1.0)
T(s, 1.02, 1.96, 5.4, 0.24, "指令 A　原始（数据集自带）", size=8.8, color=MUTED, autofit=False)
T(s, 1.02, 2.24, 5.45, 0.58, "pink lego brick into the transparent box", size=13,
  color=INK, bold=True, ls=1.25)

rect(s, 0.78, 3.00, 6.05, 0.98, fill=BLUE_T, line=BLUE, lw=1.2)
T(s, 1.02, 3.12, 5.4, 0.24, "指令 B　替换", size=8.8, color=BLUE, bold=True, autofit=False)
T(s, 1.02, 3.40, 5.45, 0.56, "让粉色积木留在原地（keep the pink brick where it is）",
  size=12, color=INK, bold=True, ls=1.25)

rx = 7.20
T(s, rx, 1.84, 5.2, 0.24, "固定不变的三个条件", size=9.2, color=BLUE, bold=True, autofit=False)
for i, t_ in enumerate(["输入图像（同一帧）", "机器人状态（同一帧）", "随机种子"]):
    rect(s, rx, 2.20 + i * 0.34 + 0.06, 0.11, 0.11, fill=BLUE)
    T(s, rx + 0.22, 2.14 + i * 0.34, 4.8, 0.28, t_, size=10.2, color=INK2, autofit=False)

rect(s, rx, 3.28, 5.16, 1.58, fill=INK)
T(s, rx + 0.28, 3.42, 4.6, 0.24, "输出向量的 L2 距离", size=8.8, color=RGBColor(0x9F, 0xB2, 0xC9), autofit=False)
T(s, rx + 0.28, 3.64, 4.6, 0.80, "0.623", size=44, color=WHITE, bold=True, autofit=False)
T(s, rx + 0.28, 4.44, 4.6, 0.26, "6 个分量全部改变", size=9.6, color=RGBColor(0xC8, 0xD6, 0xE8), autofit=False)

T(s, 0.78, 4.14, 6.0, 0.24, "为什么要做这个对照", size=9.2, color=BLUE, bold=True, autofit=False)
T(s, 0.78, 4.42, 5.95, 1.05,
  "如果模型真的「读」指令，那么换一句话、画面和状态都不动，输出就应该变；"
  "如果输出一点不变，说明模型很可能只在看图像。这是一次最小干预。",
  size=10.2, color=INK2, ls=1.45)

note_card(s, rx, 5.14, 5.16, 1.42, "但它只能说明这么多",
          "输出变了 = 模型对指令有响应。输出是否符合新指令、是否会导致「留在原地」的行为，"
          "必须把动作交回环境执行。另外，单位、缩放和控制器映射本轮都没逐项核对。",
          accent=RED, fill=RED_T, title_size=9.5)

rect(s, 0.78, 5.66, 2.98, 0.90, fill=BLUE_T)
T(s, 1.00, 5.76, 2.6, 0.24, "可以说", size=9, color=BLUE, bold=True, autofit=False)
T(s, 1.00, 6.00, 2.60, 0.48, "输出对这句话有响应，不是复制原输出。", size=9.2, color=INK2, ls=1.3)

rect(s, 3.92, 5.66, 2.98, 0.90, fill=RED_T)
T(s, 4.14, 5.76, 2.6, 0.24, "不能说", size=9, color=RED, bold=True, autofit=False)
T(s, 4.14, 6.00, 2.60, 0.48, "模型听懂了，或换词后行为会跟着变。", size=9.2, color=INK2, ls=1.3)

notes(s, "这是本次唯一一个干预实验。画面不变、状态不变、随机种子不变，只把指令从「放进透明盒」换成「让积木留在原地」。"
         "结果六个分量全都变了，向量移动了 0.623。能得出什么？只能得出「模型对指令有响应」，"
         "不能得出「模型听懂了」——听懂要靠在环境里执行后看行为对不对。【约 1 分钟】")

# ════════════════════════════════════════════ 14 收获
s = new("13 ｜ 收获", [("三个认识，每一个都能指着一份证据说清楚", True)], 14)

learn = [
    ("01", "数据是有结构的", "「一段机器人视频」其实是三路相机、14 维关节与夹爪、一句指令在时间轴上对齐的结果。",
     "289 帧视频 / 288 条记录；14 个字段名逐个核对", BLUE),
    ("02", "对照必须说清控制了什么", "同任务、同机器人、同种子编号，只改场景；失败也计入分母，结论才有边界。",
     "两组各 5 次 → 5/5 与 3/5；失败日志原文保留", BLUE),
    ("03", "「模型动了」不等于「任务成了」", "输出变化、符合指令、完成任务，是三个不同层次的验证，需要三种不同证据。",
     "6 维输出 → L2 0.623 → 闭环成功率：最后一格还空着", RED),
]
T(s, 8.10, 1.52, 4.4, 0.22, "对应的证据", size=8.6, color=FAINT, autofit=False)
y0 = 1.76
for i, (num, ttl, body, ev, c) in enumerate(learn):
    y = y0 + i * 1.66
    vline(s, 0.86, y + 0.04, 1.30, c, 2.0)
    T(s, 1.10, y + 0.00, 0.7, 0.26, num, size=10.5, color=c, bold=True, autofit=False)
    T(s, 1.10, y + 0.30, 6.2, 0.36, ttl, size=16, color=INK, bold=True, autofit=False)
    T(s, 1.10, y + 0.72, 6.4, 0.62, body, size=10.5, color=INK2, ls=1.40)
    vline(s, 7.86, y + 0.08, 1.34, LINE2, 0.9)
    T(s, 8.10, y + 0.34, 4.45, 0.80, ev, size=9.6, color=MUTED, ls=1.42)

notes(s, "这一页不讲「提高了团队协作能力」这种空话。三个认识，每个后面都挂着一份具体证据。"
         "第一个是数据结构：原以为是一段视频，打开 HDF5 才发现是 14 个字段加三路相机加一句话在对齐。"
         "第二个是实验方法：对照要说清控制了什么，失败不能删。第三个最重要：输出变了、动作符合指令、"
         "任务完成了是三件事，我们做完前两件。【约 1.5 分钟】")

# ════════════════════════════════════════════ 15 局限
s = new("14 ｜ 局限", [("三条边界，三步补法", True)], 15)

for x, w_, t_ in [(0.78, 3.40, "现在的证据"), (4.42, 4.20, "还缺什么"), (8.68, 3.87, "下一步怎么做")]:
    T(s, x, 1.76, w_, 0.26, t_, size=9.2, color=BLUE, bold=True, autofit=False)
hline(s, 0.78, 2.06, CW, INK, 1.2)

rows = [
    ("10 次尝试（5/5、3/5）\n8 条专家轨迹",
     "次数太少，不能推断成功率；随机化四项一起改，无法归因",
     "每组 ≥ 20 次；拆分单一随机化因素做消融；报告「成功数 / 尝试数」"),
    ("30 帧离线推理\n1 次指令替换",
     "没有闭环任务成功率 —— 输出动作从未真正执行过",
     "先把 6 维对齐到 14 维，在 RoboTwin 内执行并按官方条件判定"),
    ("6 维输出　vs　14 维动作",
     "关节顺序、单位、缩放、归一化、控制模式都还没逐项核验",
     "单关节动作回放测试 → 单任务闭环 → 多场景批量评测"),
]
y = 2.22
for i, (a, b, c) in enumerate(rows):
    T(s, 0.78, y + 0.02, 0.42, 0.28, f"0{i+1}", size=9.5, color=FAINT, bold=True, autofit=False)
    T(s, 1.26, y, 3.00, 0.95, a, size=10.8, color=INK, bold=True, ls=1.55)
    T(s, 4.42, y, 4.10, 0.95, b, size=10.0, color=INK2, ls=1.45)
    T(s, 8.68, y, 3.85, 0.95, c, size=10.0, color=BLUE, ls=1.45)
    if i < 2:
        hline(s, 0.78, y + 1.20, CW, LINE2, 0.75)
    y += 1.34

rect(s, 0.78, 5.72, CW, 0.80, fill=BLUE_T)
T(s, 1.02, 5.86, 1.5, 0.24, "先做哪一步", size=9.2, color=BLUE, bold=True, autofit=False)
T(s, 1.02, 6.12, CW - 0.5, 0.30,
  "接口对齐：先让一个模型输出驱动一个关节，把关节顺序、单位、方向核对清楚，再谈闭环。",
  size=10.5, color=INK2, autofit=False)

notes(s, "局限列了三条，每条配一个补法。第一条是样本量：每组五次不够，下一步做到二十次以上，并把随机化拆开做消融。"
         "第二条是没有闭环，这是最硬的边界。第三条是接口：6 维怎么驱动 14 维，"
         "先做单关节回放测试，确认一个动作发下去机器人确实那样动。【约 1 分钟】")

# ════════════════════════════════════════════ 16 总结
s = new("15 ｜ 总结", [("三句话交代这个项目", True)], 16)

summary = [
    ("做完了", "公开数据 27,500 段核验 · Colab 环境从零搭起 · 两组自采 8 条轨迹 · 30 帧离线推理", BLUE),
    ("学到了", "数据是有结构的；对照必须说清控制了什么；验证分「输出变化 / 符合指令 / 完成任务」三层", BLUE),
    ("没做完", "6 维预测还没接到 14 维双臂上跑闭环 —— 所以这份报告只谈生成与推理，不谈成功率", RED),
]
y = 1.92
for i, (k, v, c) in enumerate(summary):
    T(s, 0.80, y + 0.02, 1.10, 0.32, k, size=10.5, color=c, bold=True, autofit=False)
    T(s, 2.06, y - 0.08, 6.90, 1.00, v, size=13, color=INK, ls=1.5)
    if i < 2:
        hline(s, 0.80, y + 1.00, 7.85, LINE2, 0.75)
    y += 1.32

rect(s, 9.35, 1.86, 3.42, 3.12, fill=BLUE)
T(s, 9.58, 2.06, 3.0, 0.24, "如果要继续做一年", size=8.8, color=RGBColor(0xAF, 0xC8, 0xE8), autofit=False)
for i, t_ in enumerate(["对齐 14 维接口", "单任务闭环跑通", "多场景成功率评测"]):
    T(s, 9.58, 2.44 + i * 0.50, 3.0, 0.30, f"{i+1}　{t_}", size=11.5, color=WHITE, bold=True, autofit=False)
hline(s, 9.58, 3.96, 2.90, RGBColor(0x5E, 0x86, 0xBE), 0.9)
T(s, 9.58, 4.12, 2.95, 0.80, "目标：拿到第一个可比较的闭环成功率", size=9.2,
  color=RGBColor(0xC8, 0xDA, 0xF0), ls=1.38)

T(s, 0.80, 5.92, 8.0, 0.40, "谢谢各位老师，请提问。", size=14, color=INK, bold=True, autofit=False)
T(s, 0.80, 6.42, 8.0, 0.28, "规格严格，功夫到家", size=10, color=BLUE, autofit=False)

notes(s, "最后三句话收：做完了什么、学到了什么、没做完什么。第三句要主动说，因为老师一定会看到我们没做闭环，"
         "与其被问，不如先讲清楚为什么没做、接下来怎么做。谢谢。【约 30 秒】")

# ════════════════════════════════════════════ 附录 A 接口
s = new("附录 A ｜ 接口", [("14 维动作怎么拆，6 维输出怎么对", True)], 17, kicker_color=MUTED)

T(s, 0.78, 1.76, 5.2, 0.24, "RoboTwin / ALOHA：state 与 action 各 14 维", size=9.2, color=BLUE, bold=True, autofit=False)
for i, nm in enumerate(names):
    col, row = (0 if i < 7 else 1), i % 7
    x = 0.78 + col * 3.10
    y = 2.10 + row * 0.46
    T(s, x, y, 0.42, 0.28, f"{i+1:02d}", size=8.8, color=FAINT, autofit=False)
    T(s, x + 0.44, y, 2.55, 0.28, nm, size=9.8, color=INK, autofit=False)

T(s, 7.10, 1.76, 5.4, 0.24, "对齐清单（按顺序做，每步都要有可检查的输出）", size=9.2, color=BLUE, bold=True, autofit=False)
checks = ["机器人形态：ALOHA AgileX 与 SO-101 的自由度、连杆长度不同",
          "关节顺序：左右臂、夹爪在第几维，必须逐位对上",
          "单位与缩放：弧度 / 归一化区间，需与训练时一致",
          "相机映射：三路输入怎么对应顶部、左腕、右腕",
          "控制模式：位置、速度还是增量，决定动作怎么下发",
          "闭环验证：执行后按官方条件判定，统计成功数 / 尝试数"]
for i, c in enumerate(checks):
    T(s, 7.10, 2.10 + i * 0.56, 5.30, 0.52, f"{i+1}.　{c}", size=9.6, color=INK2, ls=1.32)

note_card(s, 0.78, 5.56, 6.0, 1.10, "为什么这一步绕不过去",
          "两套系统对「动作」的定义不同：一边是双臂 14 个电机的目标值，一边是单臂 6 维末端增量。"
          "不先对上，模型输出再合理也无法驱动机器人。",
          accent=BLUE, fill=BLUE_T, title_size=9.5)

notes(s, "备用页。如果老师问「差在哪」，翻到这里：左边是 14 个字段的真实名字，右边是要逐项核对的六件事。")

# ════════════════════════════════════════════ 附录 B 环境
s = new("附录 B ｜ 环境", [("完整环境参数与成功判定", True)], 18, kicker_color=MUTED)

T(s, 0.78, 1.76, 5.4, 0.24, "RoboTwin 侧", size=9.2, color=BLUE, bold=True, autofit=False)
env1 = [("GPU", "Tesla T4 · 15,360 MiB · 驱动 580.82.07"),
        ("仓库提交", "ea8b21121ebb3cd201ff5b3fe361944ac94eda3f"),
        ("Python", "3.10.22（uv 独立环境；Colab 默认 3.13）"),
        ("SAPIEN", "3.0.0b1（requirements 锁定）"),
        ("PyTorch", "2.4.1+cu121，另装 CUDA 12.8 工具链"),
        ("CuRobo", "v0.7.8，编译目标 sm_75"),
        ("官方资源", "机器人 / 物体 / 纹理三个 ZIP，合计 14.93 GB")]
for i, (k, v) in enumerate(env1):
    T(s, 0.78, 2.08 + i * 0.46, 1.15, 0.28, k, size=8.8, color=MUTED, autofit=False)
    T(s, 1.98, 2.08 + i * 0.46, 4.30, 0.40, v, size=9.2, color=INK, ls=1.2)

T(s, 6.70, 1.76, 5.7, 0.24, "SmolVLA 侧", size=9.2, color=BLUE, bold=True, autofit=False)
env2 = [("模型", "lerobot/smolvla_base @ 5e8d12a6…"),
        ("数据", "lerobot/svla_so101_pickplace @ f641879e…"),
        ("环境", "LeRobot 0.6.1 · torch 2.11.0+cu130 · transformers 5.5.4"),
        ("参数", "450,046,176"),
        ("相机映射", "side→camera1, up→camera2, up→camera3（第 3 槽复用）"),
        ("输入量", "11,939 帧可读取；实际推理 1 + 30 帧")]
for i, (k, v) in enumerate(env2):
    T(s, 6.70, 2.08 + i * 0.46, 1.25, 0.28, k, size=8.8, color=MUTED, autofit=False)
    T(s, 8.02, 2.08 + i * 0.46, 4.40, 0.40, v, size=9.2, color=INK, ls=1.2)

T(s, 0.78, 5.40, 5.4, 0.24, "handover_block 成功判定（官方代码）", size=9.2, color=BLUE, bold=True, autofit=False)
for i, (k, v) in enumerate([("物体到目标 · 平面两方向", "均 < 3 cm"),
                            ("物体与目标", "高度差 < 1 cm"),
                            ("右夹爪", "已打开")]):
    T(s, 0.78, 5.70 + i * 0.34, 4.4, 0.28, k, size=9.4, color=INK2, autofit=False)
    T(s, 5.10, 5.70 + i * 0.34, 2.2, 0.28, v, size=9.4, color=INK, bold=True, autofit=False)

T(s, 7.90, 5.40, 4.6, 0.24, "已知差异", size=9.2, color=RED, bold=True, autofit=False)
T(s, 7.90, 5.68, 4.55, 1.00,
  "两套是两个独立的 Python 环境，torch 版本分别是 2.11.0+cu130 和 2.4.1+cu121，不能混用。",
  size=9.2, color=INK2, ls=1.35)

notes(s, "备用页。环境参数老师可能追问版本细节，这里是完整记录。最后一条：两套环境不是同一个 Python 环境。")

# ════════════════════════════════════════════ 附录 C 明细
s = new("附录 C ｜ 明细", [("逐次结果与产物清单", True)], 19, kicker_color=MUTED)

T(s, 0.78, 1.76, 6.0, 0.24, "十个种子的逐次结果", size=9.2, color=BLUE, bold=True, autofit=False)
hdr = ["种子", "固定场景", "视频帧", "随机场景", "视频帧"]
xs = [0.86, 1.90, 3.40, 4.60, 6.30]
for i, h in enumerate(hdr):
    T(s, xs[i], 2.10, 1.6, 0.26, h, size=8.6, color=MUTED, bold=True, autofit=False)
hline(s, 0.78, 2.40, 6.10, LINE, 0.9)

fixed = [289, 280, 288, 279, 290]
rnd = {0: 286, 3: 287, 4: 285}
y = 2.52
for i in range(5):
    T(s, xs[0], y, 0.8, 0.28, f"{i}", size=9.6, color=INK, autofit=False)
    T(s, xs[1], y, 1.4, 0.28, "通过", size=9.6, color=BLUE, bold=True, autofit=False)
    T(s, xs[2], y, 1.0, 0.28, str(fixed[i]), size=9.6, color=INK2, autofit=False)
    if i in rnd:
        T(s, xs[3], y, 1.5, 0.28, "通过", size=9.6, color=BLUE, bold=True, autofit=False)
        T(s, xs[4], y, 1.0, 0.28, str(rnd[i]), size=9.6, color=INK2, autofit=False)
    else:
        T(s, xs[3], y, 1.5, 0.28, "未通过", size=9.6, color=RED, bold=True, autofit=False)
        T(s, xs[4], y, 1.0, 0.28, "—", size=9.6, color=FAINT, autofit=False)
    y += 0.44
hline(s, 0.78, y - 0.02, 6.10, LINE2, 0.75)
T(s, 0.86, y + 0.08, 6.0, 0.30, "合计　固定 5/5　·　随机 3/5　·　生成 8 条轨迹",
  size=9.4, color=INK, bold=True, autofit=False)

T(s, 7.20, 1.76, 5.4, 0.24, "产物清单（Drive「大一年度项目复现」）", size=9.2, color=BLUE, bold=True, autofit=False)
files = [("RoboTwin/generated/", "8 条自采视频 + 8 份 HDF5 + 语言文件，约 151 MiB"),
         ("seed-attempts.csv", "两组十次尝试的逐次结果"),
         ("clean.log / randomized.log", "成功、失败、不稳定物体的原始记录"),
         ("SmolVLA/observations.csv", "30 条原指令预测 + 1 条指令对照"),
         ("SmolVLA/summary.json", "计时汇总（首条、中位数、P90）"),
         ("robotwin-result.json", "27,500 段轨迹统计，含断言")]
for i, (k, v) in enumerate(files):
    T(s, 7.20, 2.10 + i * 0.50, 2.45, 0.28, k, size=8.6, color=INK, bold=True, autofit=False)
    T(s, 9.72, 2.10 + i * 0.50, 2.80, 0.44, v, size=8.4, color=MUTED, ls=1.28)

T(s, 7.20, 5.34, 5.3, 0.70,
  "脚本、配置和提交号一并保存：拿到这个目录 + 一个 Colab 实例，就能重跑出同样的结果。",
  size=9.2, color=INK2, ls=1.38)

notes(s, "备用页。如果被问「具体哪几个种子失败的」，翻到这里，逐次的帧数都有。")

# ════════════════════════════════════════════ 附录 D 计时
s = new("附录 D ｜ 测量", [("计时方法：从哪里开始，在哪里结束", True)], 20, kicker_color=MUTED)

T(s, 0.78, 1.82, 11.6, 0.28, "一次样本的时间线上，我们只量中间那一段", size=10, color=MUTED, autofit=False)

seg = [("模型加载", 1.10, 1.30, RGBColor(0xDD, 0xE2, 0xE9), MUTED, "排除"),
       ("视频解码", 2.70, 1.10, RGBColor(0xDD, 0xE2, 0xE9), MUTED, "排除"),
       ("输入预处理", 4.10, 1.30, RGBColor(0xDD, 0xE2, 0xE9), MUTED, "排除"),
       ("前向 + 后处理", 5.70, 3.40, BLUE, WHITE, "计入"),
       ("写结果", 9.40, 1.10, RGBColor(0xDD, 0xE2, 0xE9), MUTED, "排除")]
for name, x, w_, fill, tc, note in seg:
    rect(s, x, 2.42, w_, 0.92, fill=fill)
    T(s, x, 2.52, w_, 0.30, name, size=9.6, color=tc, bold=True, align=PP_ALIGN.CENTER, autofit=False)
    T(s, x, 2.94, w_, 0.26, note, size=8.6, color=tc, align=PP_ALIGN.CENTER, autofit=False)

T(s, 5.70, 3.42, 3.4, 0.24, "▲ GPU 同步后开始 　▲ 后处理结束", size=7.8, color=FAINT, autofit=False)

bullets = [("为什么排除加载", "模型加载要数秒且只发生一次，计进去会污染「单次推理」的含义"),
           ("为什么先同步", "CUDA 是异步的，不同步会量到「提交时间」而不是「算完时间」"),
           ("为什么重置队列", "SmolVLA 输出动作块；不重置会读到上一帧残留动作，输入输出对不上"),
           ("为什么不能拿 30 去除", "30 个样本来自 3 条轨迹、帧间相关，不是 30 次独立试验")]
for i, (k, v) in enumerate(bullets):
    y = 4.30 + i * 0.66
    T(s, 0.78, y, 2.45, 0.28, k, size=9.6, color=BLUE, bold=True, autofit=False)
    T(s, 3.35, y, 9.2, 0.55, v, size=9.6, color=INK2, ls=1.32)

notes(s, "备用页。如果被问「这个 0.91 秒到底量了什么」，就讲这条时间线：只量前向加后处理，"
         "而且必须 GPU 同步之后才开始计时。")

# ════════════════════════════════════════════ 附录 E 口径
s = new("附录 E ｜ 口径", [("论文做到了什么，我们做到了什么", True)], 21, kicker_color=MUTED)

for i, h in enumerate(["", "论文", "本项目"]):
    T(s, [0.78, 3.10, 8.10][i], 1.78, 4.6, 0.28, h, size=9.2, color=BLUE, bold=True, autofit=False)
hline(s, 0.78, 2.10, CW, INK, 1.1)

tab = [("任务数量", "50 项双臂任务", "1 项（handover_block）"),
       ("轨迹规模", "10 万+ 专家轨迹", "8 条自采 + 27,500 段公开数据分析"),
       ("随机化", "五类变化 + 12k 纹理库，做泛化评测", "启用四项，整体对照，未拆单因素"),
       ("策略评测", "训练后闭环任务成功率 / Sim2Real", "未做闭环；只做离线前向推理"),
       ("模型训练", "从头预训练 + 多数据集混合", "只用预训练权重推理，不训练"),
       ("耗时测量", "同步 vs 异步推理的端到端效率", "T4 单样本离线耗时，30 个样本")]
y = 2.22
for i, (a, b, c) in enumerate(tab):
    T(s, 0.78, y, 2.15, 0.50, a, size=9.6, color=INK, bold=True, autofit=False)
    T(s, 3.10, y, 4.80, 0.50, b, size=9.4, color=INK2, ls=1.3)
    T(s, 8.10, y, 4.55, 0.50, c, size=9.4, color=BLUE, ls=1.3)
    if i < 5:
        hline(s, 0.78, y + 0.62, CW, LINE2, 0.75)
    y += 0.72

T(s, 0.78, 6.62, CW, 0.28,
  "一句话：论文证明的是「这套方法可行」，我们证明的是「这条链路在我们手里能跑通一段」——量级不同。",
  size=9.6, color=MUTED, autofit=False)

notes(s, "备用页，也是最需要准备的防守页。老师最可能问「你们和论文的差距在哪」，这张表逐项对照。")

# ════════════════════════════════════════════ 附录 F 来源
s = new("附录 F ｜ 来源", [("论文、数据与代码来源", True)], 22, kicker_color=MUTED)

refs = [("RoboTwin 2.0", "Chen 等，2025。A Scalable Data Generator and Benchmark with Strong Domain "
        "Randomization for Robust Bimanual Robotic Manipulation. arXiv:2506.18088"),
        ("SmolVLA", "Shukor 等，2025。A Vision-Language-Action Model for Affordable and Efficient Robotics. "
         "arXiv:2506.01844"),
        ("公开数据", "lerobot/robotwin_unified @ 1287871…（27,500 段，ALOHA 转换子集）"),
        ("预训练权重", "lerobot/smolvla_base @ 5e8d12a6…（450,046,176 参数）"),
        ("推理数据", "lerobot/svla_so101_pickplace @ f641879e…（11,939 帧）"),
        ("代码与环境", "RoboTwin @ ea8b2112…；LeRobot 0.6.1；实验脚本与日志随项目交付")]
y = 1.84
for k, v in refs:
    T(s, 0.78, y, 1.65, 0.28, k, size=9.2, color=BLUE, bold=True, autofit=False)
    T(s, 2.52, y, 7.30, 0.62, v, size=9.2, color=INK2, ls=1.36)
    y += 0.74

pic_fit(s, IMG("rt-overview.png"), 10.05, 2.60, 2.50, 3.60)
T(s, 10.05, 6.30, 2.50, 0.26, "RoboTwin 论文图 1", size=7.8, color=FAINT, autofit=False)

T(s, 0.78, 6.62, 9.0, 0.28,
  "论文原图仅用于说明方法，图注已标注来源；团队实测图与论文图分开标注。",
  size=8.4, color=FAINT, autofit=False)

notes(s, "备用页，列全部来源，方便老师核查。")

out = os.path.join(BASE, "输出", "RoboTwin×SmolVLA_大一年度项目结题答辩.pptx")
prs.save(out)
print("saved:", out, len(prs.slides._sldIdLst), "slides")
