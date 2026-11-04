#!/usr/bin/env bash
# Run in a Colab T4 Ubuntu 24.04 runtime. Assets stay on the VM.
set -euo pipefail
repo=/content/robotwin
venv=/content/robo-env
cd /content
if [[ ! -d "$repo/.git" ]]; then
  git clone https://github.com/RoboTwin-Platform/RoboTwin.git "$repo"
fi
cd "$repo"
git checkout ea8b21121ebb3cd201ff5b3fe361944ac94eda3f
(
  cd assets
  for name in embodiments objects background_texture; do
    [[ -f ".$name.complete" ]] && continue
    curl -fL --retry 3 --connect-timeout 30 -sS \
      "https://huggingface.co/datasets/TianxingChen/RoboTwin2.0/resolve/main/$name.zip" -o "$name.zip"
    unzip -oq "$name.zip"
    rm "$name.zip"
    touch ".$name.complete"
  done
) &
assets_pid=$!
[[ -x "$venv/bin/python" ]] || uv venv --python 3.10 "$venv"
uv pip install --python "$venv/bin/python" -r scripts/requirements.txt 'setuptools<81' pip
git submodule update --init XPolicyLab
uv pip install --python "$venv/bin/python" -e ./XPolicyLab --no-deps
if [[ ! -d envs/curobo/.git ]]; then
  git clone --branch v0.7.8 --depth 1 https://github.com/NVlabs/curobo.git envs/curobo
fi
export CUDA_HOME=/usr/local/cuda-12.8
if [[ ! -x "$CUDA_HOME/bin/nvcc" ]]; then
  apt-get update -qq
  apt-get install -y --no-install-recommends cuda-nvcc-12-8 cuda-cudart-dev-12-8 cuda-cccl-12-8
fi
export PATH="$venv/bin:$CUDA_HOME/bin:$PATH"
export TORCH_CUDA_ARCH_LIST=7.5 MAX_JOBS=2 PYTHONPATH="$repo"
uv pip install --python "$venv/bin/python" 'warp-lang==1.12.0' wheel ninja toppra
python -m pip install --no-build-isolation -e envs/curobo
wait "$assets_pid"
python scripts/update_embodiment_config_path.py
python -c 'from envs.robot.planner import CuroboPlanner; print("CuRobo import passed")'
