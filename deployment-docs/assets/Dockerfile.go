# ============================================
# Go 项目 Dockerfile
# ============================================

# Stage 1: Builder - 构建阶段
FROM golang:1.21-alpine AS builder

WORKDIR /app

# 复制依赖文件
COPY go.mod go.sum ./

# 下载依赖（缓存层）
RUN go mod download

# 复制所有源码
COPY . .

# 构建二进制文件
# CGO_ENABLED=0: 禁用 CGO，生成静态链接二进制
# -a: 强制重新编译
# -installsuffix cgo: 安装后缀
# -o app: 输出文件名
RUN CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o app .

# Stage 2: Runner - 运行阶段
FROM alpine:latest

# 安装基础工具和时区
RUN apk --no-cache add ca-certificates tzdata

WORKDIR /root/

# 复制构建好的二进制文件
COPY --from=builder /app/app .

# 创建非 root 用户（安全最佳实践）
RUN addgroup -g 1000 appgroup && \
    adduser -D -u 1000 -G appgroup appuser

# 创建日志目录并授权
RUN mkdir -p /app/logs && chown -R appuser:appgroup /app

# 切换到非 root 用户
USER appuser

# 暴露端口（根据你的应用修改）
EXPOSE 8080

# 健康检查
# --interval: 检查间隔
# --timeout: 超时时间
# --start-period: 启动等待时间
# --retries: 重试次数
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:8080/health || exit 1

# 启动命令
CMD ["./app"]
