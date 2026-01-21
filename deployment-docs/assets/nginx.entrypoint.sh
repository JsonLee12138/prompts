#!/bin/sh
set -e

# ============================================
# Nginx + Node.js 入口脚本
# ============================================

# 1. 环境变量注入 (根据需要修改)
API_HOST="${API_HOST:-backend}"
API_PORT="${API_PORT:-3000}"
export API_HOST API_PORT

# 2. 生成 Nginx 配置 (使用 envsubst)
envsubst '${API_HOST} ${API_PORT}' \
  < /etc/nginx/templates/nginx.conf.template \
  > /etc/nginx/http.d/default.conf

# 3. 启动 Node.js 应用
node server.js &
NODE_PID=$!

# 4. 启动 Nginx
nginx -g 'daemon off;' &
NGINX_PID=$!

# 5. 信号处理与优雅退出
trap "kill -TERM $NODE_PID; kill -TERM $NGINX_PID" TERM INT

wait $NODE_PID
exit $?
