# 通用项目部署文档

> 适用于任何技术栈的 Docker + Makefile 部署体系，支持 monorepo 和独立项目

---

## 📋 目录

- [项目类型适配](#项目类型适配)
- [快速开始](#快速开始-1)
- [Makefile 模板](#makefile-模板)
- [Dockerfile 模板](#dockerfile-模板)
- [Docker Compose 配置](#docker-compose-配置)
- [配置清单](#配置清单)
- [使用示例](#使用示例)

---

## 项目类型适配

### 场景 1: Monorepo 项目

```
my-monorepo/
├── apps/
│   ├── frontend/          # Next.js / React / Vue
│   │   ├── Dockerfile
│   │   ├── Makefile
│   │   ├── docker-compose.yaml
│   │   └── docker/        # Nginx 配置 (如果需要)
│   └── backend/           # Go / Python / Node / Java
│       ├── Dockerfile
│       ├── Makefile
│       ├── docker-compose.yaml
│       └── ecosystem.config.js  # PM2 配置 (Node.js)
├── packages/
└── turbo.json
```

**特点**:
- 每个应用独立配置
- 共享 packages
- 使用 turbo 构建

### 场景 2: 独立项目

```
my-project/
├── Dockerfile
├── Makefile
├── docker-compose.yaml
├── docker-compose.test.yaml
├── docker-compose.local.yaml
└── src/
```

**特点**:
- 项目根目录直接部署
- 无 monorepo 依赖
- 简单直接

---

## 快速开始

### 步骤 1: 选择技术栈 Dockerfile

根据你的项目技术栈，选择对应的 Dockerfile：

| 技术栈 | Dockerfile | 端口 | 启动方式 |
|--------|------------|------|----------|
| Go | `Dockerfile.go` | 8080 | `./app` |
| Python | `Dockerfile.python` | 8000 | `python main.py` |
| Node.js (后端) | `Dockerfile.node-pm2` | 3000 | `pm2-runtime ecosystem.config.js` |
| Next.js (前端) | `Dockerfile.nextjs-nginx` | 80 | `nginx` |
| Java/Spring | `Dockerfile.java` | 8080 | `java -jar app.jar` |
| Rust | `Dockerfile.rust` | 8080 | `./app` |

### 步骤 2: 复制模板文件

```bash
# 进入你的项目目录
cd your-project

# 复制基础文件
cp deployment-docs/templates/Makefile.template Makefile
cp deployment-docs/templates/Dockerfile.go Dockerfile  # 选择你的技术栈

# 复制 docker-compose 文件
cp deployment-docs/templates/docker-compose.local.yaml.template docker-compose.local.yaml
cp deployment-docs/templates/docker-compose.test.yaml.template docker-compose.test.yaml
cp deployment-docs/templates/docker-compose.yaml.template docker-compose.yaml

# 如果是 Node.js 后端，复制 PM2 配置
cp deployment-docs/templates/ecosystem.config.js ecosystem.config.js

# 如果是前端需要 Nginx，复制 Nginx 配置
mkdir -p docker/nginx
cp deployment-docs/templates/nginx.conf.template docker/nginx/
cp deployment-docs/templates/nginx.entrypoint.sh docker/nginx/
chmod +x docker/nginx/entrypoint.sh
```

### 步骤 3: 修改配置

**编辑 Makefile** (修改第 14-24 行):
```makefile
# 修改这些值
APP_NAME ?= your-app-name

# 修改环境配置
ifeq ($(ENV_MODE), test)
  REGISTRY_HOST = 192.168.1.100:5000
  REMOTE_USER = root
  REMOTE_HOST = test-server
  REMOTE_COMPOSE_PATH = /opt/docker-composes
else ifeq ($(ENV_MODE), prod)
  REGISTRY_HOST = registry.example.com:5000
  REMOTE_USER = deploy
  REMOTE_HOST = prod-server
  REMOTE_COMPOSE_PATH = ~/docker-composes
endif
```

**编辑 Dockerfile** (根据技术栈调整端口、启动命令等)

**编辑 docker-compose.yaml** (修改镜像名、容器名)

### 步骤 4: 测试部署

```bash
# 1. 本地测试
make test

# 2. 构建并推送镜像
make push

# 3. 部署到测试环境
make remote-deploy

# 4. 部署到生产环境
make ENV_MODE=prod remote-deploy
```

---

## Makefile 模板

### 完整 Makefile

```makefile
# ============================================
# 通用项目部署 Makefile
# ============================================

# --- 基础配置 ---
APP_NAME ?= $(shell basename $(CURDIR))
VERSION ?= latest
ENV_MODE ?= test  # local | test | prod
USE_SUDO ?= true

# --- 路径配置 ---
MONOREPO_ROOT ?= $(shell git rev-parse --show-toplevel 2>/dev/null || echo ".")
BUILD_CONTEXT ?= $(MONOREPO_ROOT)
DOCKERFILE ?= Dockerfile

# --- 环境配置 (根据实际修改) ---
ifeq ($(ENV_MODE), local)
  REGISTRY_HOST = localhost:5000
  REMOTE_USER = $(shell whoami)
  REMOTE_HOST = localhost
  REMOTE_PATH = .
  COMPOSE_FILE = docker-compose.local.yaml
else ifeq ($(ENV_MODE), test)
  REGISTRY_HOST = registry.example.com:5000
  REMOTE_USER = root
  REMOTE_HOST = test-server
  REMOTE_PATH = /opt/docker-composes
  COMPOSE_FILE = docker-compose.test.yaml
else ifeq ($(ENV_MODE), prod)
  REGISTRY_HOST = registry.example.com:5000
  REMOTE_USER = deploy
  REMOTE_HOST = prod-server
  REMOTE_PATH = ~/docker-composes
  COMPOSE_FILE = docker-compose.yaml
endif

FULL_IMAGE = $(REGISTRY_HOST)/$(APP_NAME):$(VERSION)
SUDO = $(if $(USE_SUDO),sudo,)

# --- 颜色定义 ---
GREEN = \033[0;32m
YELLOW = \033[1;33m
RED = \033[0;31m
NC = \033[0m

# ============================================
# 1. 本地开发测试
# ============================================

.PHONY: test local-dev

test: ## 本地 Docker 测试
	@echo "$(YELLOW)启动本地服务: $(APP_NAME)$(NC)"
	docker compose -f $(COMPOSE_FILE) up --build

local-dev: ## 本地开发 (不使用 Docker)
	@echo "$(YELLOW)启动本地开发$(NC)"
	@if [ -f "package.json" ]; then \
		pnpm dev || npm run dev; \
	elif [ -f "go.mod" ]; then \
		go run ./...; \
	elif [ -f "main.py" ]; then \
		python main.py; \
	else \
		echo "$(RED)无法自动启动，请手动执行启动命令$(NC)"; \
	fi

# ============================================
# 2. 镜像构建
# ============================================

.PHONY: build build-arm save tag

build-arm: ## ARM 架构构建 (M1/M2 Mac)
	@echo "$(YELLOW)构建 ARM 镜像: $(APP_NAME):$(VERSION)$(NC)"
	docker build -t $(APP_NAME):$(VERSION) -f $(DOCKERFILE) $(BUILD_CONTEXT)

build: ## AMD64 架构构建
	@echo "$(YELLOW)构建 AMD64 镜像: $(APP_NAME):$(VERSION)$(NC)"
	docker buildx build --platform linux/amd64 -t $(APP_NAME):$(VERSION) -f $(DOCKERFILE) $(BUILD_CONTEXT)

save: build ## 保存镜像到文件
	@echo "$(YELLOW)保存镜像到文件$(NC)"
	docker save $(APP_NAME):$(VERSION) -o ./$(APP_NAME)-$(VERSION).tar
	@echo "$(GREEN)已保存: $(APP_NAME)-$(VERSION).tar$(NC)"

tag: build ## 打标签
	@echo "$(YELLOW)打标签: $(FULL_IMAGE)$(NC)"
	docker tag $(APP_NAME):$(VERSION) $(FULL_IMAGE)

# ============================================
# 3. 镜像推送
# ============================================

.PHONY: push remote-pull

push: tag ## 推送到仓库
	@echo "$(YELLOW)推送: $(FULL_IMAGE)$(NC)"
	docker push $(FULL_IMAGE)

remote-pull: push ## 远程拉取
	@echo "$(YELLOW)远程拉取$(NC)"
	ssh $(REMOTE_USER)@$(REMOTE_HOST) "$(SUDO) docker pull $(FULL_IMAGE)"

# ============================================
# 4. 部署管理
# ============================================

.PHONY: push-compose remote-deploy remote-restart remote-logs remote-status

push-compose: push ## 推送 compose 文件
	@echo "$(YELLOW)推送 compose 文件$(NC)"
	ssh $(REMOTE_USER)@$(REMOTE_HOST) "mkdir -p $(REMOTE_PATH)"
	ssh $(REMOTE_USER)@$(REMOTE_HOST) "rm -f $(REMOTE_PATH)/$(APP_NAME).yaml"
	scp $(COMPOSE_FILE) $(REMOTE_USER)@$(REMOTE_HOST):$(REMOTE_PATH)/$(APP_NAME).yaml

remote-deploy: push local-clean push-compose-file ## 完整部署
	@echo "$(YELLOW)开始部署: $(APP_NAME)$(NC)"
	@echo "1. 停止旧服务..."
	ssh $(REMOTE_USER)@$(REMOTE_HOST) "cd $(REMOTE_PATH) && $(SUDO) docker compose -f $(APP_NAME).yaml down || true"
	@echo "2. 拉取镜像..."
	ssh $(REMOTE_USER)@$(REMOTE_HOST) "cd $(REMOTE_PATH) && $(SUDO) docker compose -f $(APP_NAME).yaml pull"
	@echo "3. 启动服务..."
	ssh $(REMOTE_USER)@$(REMOTE_HOST) "cd $(REMOTE_PATH) && $(SUDO) docker compose -f $(APP_NAME).yaml up -d"
	@echo "$(GREEN)部署完成!$(NC)"

remote-restart: ## 重启服务
	@echo "$(YELLOW)重启服务$(NC)"
	ssh $(REMOTE_USER)@$(REMOTE_HOST) "cd $(REMOTE_PATH) && $(SUDO) docker compose -f $(APP_NAME).yaml restart"

remote-logs: ## 查看日志
	@echo "$(YELLOW)查看日志$(NC)"
	ssh $(REMOTE_USER)@$(REMOTE_HOST) "docker logs -f --tail=100 $(APP_NAME)"

remote-status: ## 查看状态
	@echo "$(YELLOW)服务状态$(NC)"
	ssh $(REMOTE_USER)@$(REMOTE_HOST) "docker ps | grep $(APP_NAME) || echo '未运行'"

# ============================================
# 5. 清理维护
# ============================================

.PHONY: local-clean docker-clean

local-clean: ## 清理本地镜像
	@echo "$(YELLOW)清理本地镜像$(NC)"
	docker rmi $(APP_NAME):$(VERSION) 2>/dev/null || true
	docker rmi $(FULL_IMAGE) 2>/dev/null || true

docker-clean: ## 清理 Docker 缓存
	@echo "$(YELLOW)清理缓存$(NC)"
	docker system prune -f

# ============================================
# 6. 工具命令
# ============================================

.PHONY: help info

help: ## 显示帮助
	@printf "$(YELLOW)应用: $(GREEN)$(APP_NAME)$(NC) | 环境: $(GREEN)$(ENV_MODE)$(NC)\\n"
	@printf "\\n$(GREEN)可用命令:$(NC)\\n"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = \":.*?## \"}; {printf "  %-20s %s\\n", $$1, $$2}'

info: ## 显示配置
	@echo "============================================"
	@echo "应用: $(APP_NAME)"
	@echo "版本: $(VERSION)"
	@echo "环境: $(ENV_MODE)"
	@echo "仓库: $(REGISTRY_HOST)"
	@echo "远程: $(REMOTE_USER)@$(REMOTE_HOST)"
	@echo "镜像: $(FULL_IMAGE)"
	@echo "============================================"

# ============================================
# 使用示例
# ============================================
# 本地测试: make test
# 生产部署: make ENV_MODE=prod remote-deploy
# 指定版本: make VERSION=v1.2.3 push
# 查看日志: make remote-logs
# ============================================
```

---

## Dockerfile 模板

### 1. Go 项目

```dockerfile
# ============================================
# Go 项目 Dockerfile
# ============================================

# Stage 1: Builder
FROM golang:1.21-alpine AS builder

WORKDIR /app

# 安装依赖
COPY go.mod go.sum ./
RUN go mod download

# 复制源码
COPY . .

# 构建
RUN CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o app .

# Stage 2: Runner
FROM alpine:latest

RUN apk --no-cache add ca-certificates tzdata

WORKDIR /root/

# 复制二进制文件
COPY --from=builder /app/app .

# 创建非 root 用户
RUN addgroup -g 1000 appgroup && \
    adduser -D -u 1000 -G appgroup appuser

# 创建日志目录
RUN mkdir -p /app/logs && chown -R appuser:appgroup /app

USER appuser

EXPOSE 8080

# 健康检查
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:8080/health || exit 1

CMD ["./app"]
```

### 2. Python 项目

```dockerfile
# ============================================
# Python 项目 Dockerfile
# ============================================

# Stage 1: Builder
FROM python:3.11-slim AS builder

WORKDIR /app

# 安装依赖
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Runner
FROM python:3.11-slim

WORKDIR /app

# 复制依赖
COPY --from=builder /root/.local /root/.local

# 复制源码
COPY . .

# 创建非 root 用户
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app

USER appuser

# 环境变量
ENV PATH=/root/.local/bin:$PATH
ENV PYTHONUNBUFFERED=1

EXPOSE 8000

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

CMD ["python", "main.py"]
```

### 3. Node.js 项目 (PM2)

```dockerfile
# ============================================
# Node.js 项目 Dockerfile (PM2)
# ============================================

# Stage 1: Builder
FROM node:22-alpine AS builder

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .

# 如果有构建步骤，取消注释
# RUN npm run build

# Stage 2: Runner
FROM node:22-alpine

WORKDIR /app

# 安装 PM2
RUN npm install -g pm2

# 复制依赖
COPY --from=builder /app/node_modules ./node_modules

# 复制源码
COPY . .

# 创建非 root 用户
RUN addgroup -g 1000 nodejs && \
    adduser -D -u 1000 -G nodejs nodejs

# 创建日志目录
RUN mkdir -p logs && chown -R nodejs:nodejs /app

USER nodejs

ENV NODE_ENV=production
ENV PORT=3000
EXPOSE 3000

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
  CMD curl -f http://localhost:3000/health || exit 1

CMD ["pm2-runtime", "ecosystem.config.js"]
```

### 4. Next.js 项目 (Nginx)

```dockerfile
# ============================================
# Next.js 项目 Dockerfile (Nginx)
# ============================================

# Stage 1: Builder
FROM node:22-alpine AS builder

WORKDIR /app

COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Stage 2: Runner
FROM nginx:alpine

# 复制构建产物
COPY --from=builder /app/.next/static /usr/share/nginx/html/_next/static
COPY --from=builder /app/public /usr/share/nginx/html/public

# Nginx 配置
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
  CMD curl -f http://localhost:80/health || exit 1

CMD ["nginx", "-g", "daemon off;"]
```

### 5. Java/Spring Boot 项目

```dockerfile
# ============================================
# Java Spring Boot 项目 Dockerfile
# ============================================

# Stage 1: Builder
FROM maven:3.9-eclipse-temurin-17 AS builder

WORKDIR /app

COPY pom.xml .
RUN mvn dependency:go-offline
COPY src ./src
RUN mvn clean package -DskipTests

# Stage 2: Runner
FROM eclipse-temurin:17-jre-alpine

WORKDIR /app

# 复制 JAR
COPY --from=builder /app/target/*.jar app.jar

# 创建非 root 用户
RUN addgroup -g 1000 java && \
    adduser -D -u 1000 -G java javauser

USER javauser

EXPOSE 8080

# 健康检查 (需要 Spring Boot Actuator)
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:8080/actuator/health || exit 1

ENTRYPOINT ["java", "-jar", "app.jar"]
```

### 6. Rust 项目

```dockerfile
# ============================================
# Rust 项目 Dockerfile
# ============================================

# Stage 1: Builder
FROM rust:1.75-slim AS builder

WORKDIR /app

COPY . .

# 构建 release 版本
RUN cargo build --release

# Stage 2: Runner
FROM debian:bookworm-slim

WORKDIR /root/

# 复制构建好的二进制
COPY --from=builder /app/target/release/app .

# 创建非 root 用户
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app

USER appuser

EXPOSE 8080

# 健康检查
HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
  CMD curl -f http://localhost:8080/health || exit 1

CMD ["./app"]
```

---

## Docker Compose 配置

### 1. 本地开发 (docker-compose.local.yaml)

```yaml
services:
  app:
    build: .
    ports:
      - "8080:8080"  # 根据应用端口修改
    environment:
      - NODE_ENV=development
      - ENV=local
    volumes:
      - .:/app  # 源码热重载
      - /app/node_modules  # 保持 node_modules 独立
    networks:
      - dev-network

networks:
  dev-network:
    driver: bridge
```

### 2. 测试环境 (docker-compose.test.yaml)

```yaml
services:
  app:
    image: registry.example.com:5000/app:latest
    container_name: app-test
    environment:
      - NODE_ENV=production
      - ENV=test
      - DATABASE_URL=postgresql://user:pass@db-test:5432/testdb
      - REDIS_URL=redis://redis-test:6379
    ports:
      - "18080:8080"
    restart: unless-stopped
    networks:
      - test-network
    depends_on:
      - db-test
      - redis-test

  db-test:
    image: postgres:15-alpine
    container_name: db-test
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
      - POSTGRES_DB=testdb
    volumes:
      - pgdata-test:/var/lib/postgresql/data
    networks:
      - test-network

  redis-test:
    image: redis:7-alpine
    container_name: redis-test
    networks:
      - test-network

volumes:
  pgdata-test:

networks:
  test-network:
    driver: bridge
```

### 3. 生产环境 (docker-compose.yaml)

```yaml
services:
  app:
    image: registry.example.com:5000/app:latest
    container_name: app
    environment:
      - NODE_ENV=production
      - ENV=production
      - DATABASE_URL=postgresql://user:pass@db:5432/proddb
      - REDIS_URL=redis://redis:6379
    restart: unless-stopped
    deploy:
      resources:
        limits:
          cpus: "0.5"
          memory: "1024M"
    networks:
      - prod-network:
          ipv4_address: 172.20.0.10
    depends_on:
      - db
      - redis

  db:
    image: postgres:15-alpine
    container_name: db
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
      - POSTGRES_DB=proddb
    volumes:
      - pgdata:/var/lib/postgresql/data
    deploy:
      resources:
        limits:
          cpus: "0.5"
          memory: "2048M"
    networks:
      - prod-network:
          ipv4_address: 172.20.0.11

  redis:
    image: redis:7-alpine
    container_name: redis
    deploy:
      resources:
        limits:
          cpus: "0.2"
          memory: "512M"
    networks:
      - prod-network:
          ipv4_address: 172.20.0.12

volumes:
  pgdata:

networks:
  prod-network:
    external: true
    name: prod-network
```

---

## 配置清单

### Makefile 必须修改

```makefile
# 第 6 行: 应用名称
APP_NAME ?= your-app-name

# 第 14-24 行: 环境配置
REGISTRY_HOST = your-registry:5000
REMOTE_USER = your-user
REMOTE_HOST = your-host
```

### Dockerfile 必须修改

```dockerfile
# 根据技术栈调整
# - 端口号 (EXPOSE)
# - 启动命令 (CMD/ENTRYPOINT)
# - 环境变量
# - 健康检查
```

### docker-compose 必须修改

```yaml
# - 镜像名称
# - 端口映射
# - 环境变量
# - 依赖服务
```

---

## 使用示例

### 场景 1: Go 项目

```bash
# 1. 创建项目
mkdir my-go-app && cd my-go-app

# 2. 复制模板
cp deployment-docs/templates/Makefile.template Makefile
cp deployment-docs/templates/Dockerfile.go Dockerfile
cp deployment-docs/templates/docker-compose.*.yaml.template ./

# 3. 修改配置
# 编辑 Makefile, Dockerfile

# 4. 测试部署
make test
make remote-deploy
```

### 场景 2: Python 项目

```bash
# 1. 创建项目
mkdir my-python-app && cd my-python-app

# 2. 复制模板
cp deployment-docs/templates/Makefile.template Makefile
cp deployment-docs/templates/Dockerfile.python Dockerfile
cp deployment-docs/templates/docker-compose.*.yaml.template ./

# 3. 创建 requirements.txt
pip freeze > requirements.txt

# 4. 测试部署
make test
make remote-deploy
```

### 场景 3: Node.js 后端项目

```bash
# 1. 创建项目
mkdir my-node-app && cd my-node-app
npm init -y

# 2. 复制模板
cp deployment-docs/templates/Makefile.template Makefile
cp deployment-docs/templates/Dockerfile.node-pm2 Dockerfile
cp deployment-docs/templates/ecosystem.config.js ./
cp deployment-docs/templates/docker-compose.*.yaml.template ./

# 3. 修改配置
# 编辑 Makefile, Dockerfile, ecosystem.config.js

# 4. 测试部署
make test
make remote-deploy
```

### 场景 4: Next.js 前端项目

```bash
# 1. 创建项目
mkdir my-nextjs-app && cd my-nextjs-app

# 2. 复制模板
cp deployment-docs/templates/Makefile.template Makefile
cp deployment-docs/templates/Dockerfile.nextjs-nginx Dockerfile
cp deployment-docs/templates/docker-compose.*.yaml.template ./
mkdir -p docker/nginx
cp deployment-docs/templates/nginx.conf.template docker/nginx/
cp deployment-docs/templates/nginx.entrypoint.sh docker/nginx/
chmod +x docker/nginx/entrypoint.sh

# 3. 修改配置
# 编辑 Makefile, Dockerfile, docker/nginx/nginx.conf

# 4. 测试部署
make test
make remote-deploy
```

### 场景 5: Monorepo 项目

```bash
# 在每个应用目录下
cd apps/backend/api

# 复制模板
cp ../../deployment-docs/templates/Makefile.template Makefile
# 根据技术栈选择 Dockerfile
cp ../../deployment-docs/templates/Dockerfile.go Dockerfile  # 或其他

# 修改配置
# 编辑 Makefile 中的路径配置

# 测试部署
make test
make ENV_MODE=prod remote-deploy
```

---

## 常用命令速查

| 命令 | 说明 | 使用场景 |
|------|------|----------|
| `make test` | 本地 Docker 测试 | 开发调试 |
| `make local-dev` | 本地开发模式 | 不使用 Docker |
| `make build` | 构建镜像 | 生产环境 |
| `make build-arm` | ARM 架构构建 | M1/M2 Mac |
| `make push` | 推送镜像 | 部署前 |
| `make remote-deploy` | 完整部署 | 测试/生产 |
| `make remote-logs` | 查看日志 | 排查问题 |
| `make remote-status` | 查看状态 | 监控 |
| `make remote-restart` | 重启服务 | 维护 |
| `make rollback` | 回滚版本 | 故障恢复 |
| `make help` | 显示帮助 | 查看命令 |
| `make info` | 显示配置 | 查看当前配置 |

---

## 故障排查

### 镜像推送失败

```bash
# 检查登录
docker login registry.example.com:5000

# 检查网络
ping registry.example.com
```

### 部署后服务无法访问

```bash
# 查看日志
make remote-logs

# 检查容器状态
make remote-status

# 检查端口
ssh user@host "netstat -tlnp | grep 18080"
```

### 如何清理磁盘空间

```bash
# 本地清理
make local-clean
make docker-clean

# 远程清理
ssh user@host "docker system prune -f"
```

---

## 总结

这套部署系统的核心优势：

1. **完全通用** - 适用于任何技术栈（Go, Python, Node.js, Java, Rust 等）
2. **独立使用** - 不依赖 monorepo，也支持 monorepo
3. **灵活配置** - 易于修改和扩展
4. **保持功能** - Makefile 提供完整部署流程
5. **环境隔离** - 本地/测试/生产环境完全分离
6. **安全可靠** - 非 root 运行、健康检查、资源限制

**使用流程**：
1. 选择对应的技术栈 Dockerfile
2. 复制 Makefile 和 docker-compose 模板
3. 修改配置
4. 测试部署

所有模板都在 `templates/` 目录下，按需使用即可！

---

**文档版本**: v3.0
**最后更新**: 2026-01-12
**适用范围**: 所有项目（Monorepo 和独立项目）
