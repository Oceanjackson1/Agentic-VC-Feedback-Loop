#!/bin/bash
# 投资人对话总结 Agent - 本地启动脚本

cd "$(dirname "$0")/backend"

if [ -z "$DEEPSEEK_API_KEY" ] && [ -f "../.env" ]; then
  export $(grep -v '^#' ../.env | xargs)
fi

if [ -z "$DEEPSEEK_API_KEY" ]; then
  echo "请设置 DEEPSEEK_API_KEY 环境变量或创建 .env 文件"
  echo "示例: export DEEPSEEK_API_KEY=sk-xxx"
  exit 1
fi

echo "正在启动服务..."
python3 -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
