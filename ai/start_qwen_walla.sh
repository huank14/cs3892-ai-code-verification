#!/usr/bin/env bash
# Explicit, separate process; never stops other users' inference jobs.
set -euo pipefail
cd /home/jiahao/cs3892-ai-pilot
mkdir -p logs
model_path=/home/jiahao/.cache/huggingface/hub/models--Qwen--Qwen3.8-27B-FP8/snapshots/c3a462cc3d38cf351f3b26cbd763469eeb74ef81
if curl -sf --max-time 3 http://127.0.0.1:18392/v1/models > /dev/null; then
    echo 'Port 18392 already serves a model; verify identity before using it.'
    exit 1
fi
CUDA_VISIBLE_DEVICES=0 HF_HUB_OFFLINE=1 nohup \
  /home/jiahao/abstention-claude-prelim/.venv-vllm/bin/python \
  -m vllm.entrypoints.openai.api_server \
  --model "$model_path" --served-model-name Qwen/Qwen3.8-27B-FP8 \
  --host 127.0.0.1 --port 18392 --max-model-len 8192 --max-num-seqs 1 \
  --gpu-memory-utilization 0.72 --enforce-eager --language-model-only \
  > logs/server.log 2>&1 < /dev/null &
echo $! > logs/server.pid
