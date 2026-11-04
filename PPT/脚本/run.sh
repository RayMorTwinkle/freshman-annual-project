#!/bin/bash
# 一键重新生成 PPT 与预览图
set -e
cd "$(dirname "$0")/.."

PY="./.venv/bin/python"
if [ ! -x "$PY" ]; then
  echo "未找到虚拟环境，正在创建..."
  python3 -m venv .venv
  ./.venv/bin/python -m pip install -q --upgrade pip
  ./.venv/bin/python -m pip install -q python-pptx pillow matplotlib numpy
fi

"$PY" 脚本/build_deck.py
"$PY" 脚本/preview.py "输出/RoboTwin×SmolVLA_大一年度项目结题答辩.pptx" "输出/preview"
echo "完成：输出/RoboTwin×SmolVLA_大一年度项目结题答辩.pptx"
