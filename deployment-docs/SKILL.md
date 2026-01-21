---
name: universal-deployment
description: Provides complete deployment setup for any tech stack including Docker, Makefile, docker-compose, and CI/CD configurations
---

# 通用部署技能 (Universal Deployment Skill)

## 🎯 使用场景

当用户需要为任何技术栈的项目创建完整的部署体系时使用此技能：

- **部署应用** - "deploy application", "部署应用"
- **创建部署配置** - "create deployment", "创建部署"
- **Docker 配置** - "setup Docker", "configure Docker", "Docker 配置"
- **Makefile 自动化** - "configure Makefile", "add Makefile", "Makefile 配置"
- **Docker Compose** - "add docker-compose", "docker-compose 配置"
- **CI/CD 流程** - "setup CI/CD", "配置 CI/CD"
- **服务器部署** - "deploy to server", "部署到服务器"
- **Dockerfile 创建** - "create Dockerfile", "Dockerfile 配置"

## 📋 技能内容

### 支持的技术栈

此技能包含以下技术栈的完整部署模板：

| 技术栈 | Dockerfile | 端口 | 启动方式 |
|--------|------------|------|----------|
| Go | `Dockerfile.go` | 8080 | `./app` |
| Python | `Dockerfile.python` | 8000 | `python main.py` |
| Node.js (后端) | `Dockerfile.node-pm2` | 3000 | `pm2-runtime ecosystem.config.js` |
| Next.js (前端) | `Dockerfile.nextjs-nginx` | 80 | `nginx` |
| Java/Spring | `Dockerfile.java` | 8080 | `java -jar app.jar` |
| Rust | `Dockerfile.rust` | 8080 | `./app` |

### 环境配置

- **本地环境** (`docker-compose.local.yaml`) - 端口映射 + 热重载
- **测试环境** (`docker-compose.test.yaml`) - 端口映射 + 数据库 + Redis
- **生产环境** (`docker-compose.yaml`) - 资源限制 + 外部网络 + 健康检查

### Makefile 自动化

```bash
make test              # 本地 Docker 测试
make build             # 构建镜像 (AMD64)
make build-arm         # 构建镜像 (ARM/M1)
make push              # 推送镜像
make remote-deploy     # 完整部署
make remote-logs       # 查看日志
make remote-status     # 查看状态
make remote-restart    # 重启服务
make rollback          # 回滚版本
make help              # 显示帮助
```

## 🚀 快速开始

### 步骤 1: 使用自动化脚本（推荐）

```bash
# 运行自动化设置脚本
bash deployment-docs/scripts/setup-deployment.sh
```

脚本会自动检测你的项目类型并完成所有配置。

### 步骤 2: 或者手动复制模板

```bash
# 进入项目目录
cd your-project

# 复制 Makefile
cp deployment-docs/assets/Makefile.template Makefile

# 复制 Dockerfile (选择技术栈)
cp deployment-docs/assets/Dockerfile.go Dockerfile      # Go
cp deployment-docs/assets/Dockerfile.python Dockerfile  # Python
cp deployment-docs/assets/Dockerfile.node-pm2 Dockerfile  # Node.js
cp deployment-docs/assets/Dockerfile.nextjs-nginx Dockerfile  # Next.js

# 复制 docker-compose 文件
cp deployment-docs/assets/docker-compose.local.yaml.template docker-compose.local.yaml
cp deployment-docs/assets/docker-compose.test.yaml.template docker-compose.test.yaml
cp deployment-docs/assets/docker-compose.yaml.template docker-compose.yaml

# Node.js 后端需要 PM2 配置
cp deployment-docs/assets/ecosystem.config.js ecosystem.config.js

# 前端需要 Nginx 配置
mkdir -p docker/nginx
cp deployment-docs/assets/nginx.conf.template docker/nginx/
cp deployment-docs/assets/nginx.entrypoint.sh docker/nginx/
chmod +x docker/nginx/entrypoint.sh
```

### 步骤 2: 修改配置

#### 修改 Makefile (必须)

```makefile
# 第 6 行: 应用名称
APP_NAME ?= your-app-name

# 第 14-24 行: 环境配置
REGISTRY_HOST = your-registry:5000
REMOTE_USER = your-user
REMOTE_HOST = your-host
```

#### 修改 Dockerfile (根据技术栈调整)

- 端口号 (EXPOSE)
- 启动命令 (CMD/ENTRYPOINT)
- 健康检查

#### 修改 docker-compose.yaml (必须)

```yaml
services:
  app:
    image: registry.example.com:5000/your-app-name:latest
    container_name: your-app-name
```

### 步骤 3: 测试部署

```bash
# 1. 本地测试
make test

# 2. 构建并推送
make push

# 3. 部署到测试环境
make remote-deploy

# 4. 部署到生产环境
make ENV_MODE=prod remote-deploy
```

## 📚 使用示例

### Go 项目

```bash
cd my-go-app
bash deployment-docs/scripts/setup-deployment.sh
# 或者手动：
cp deployment-docs/assets/Makefile.template Makefile
cp deployment-docs/assets/Dockerfile.go Dockerfile
cp deployment-docs/assets/docker-compose.*.yaml.template ./

make test
make remote-deploy
```

### Python 项目

```bash
cd my-python-app
bash deployment-docs/scripts/setup-deployment.sh
# 或者手动：
cp deployment-docs/assets/Makefile.template Makefile
cp deployment-docs/assets/Dockerfile.python Dockerfile
cp deployment-docs/assets/docker-compose.*.yaml.template ./

make test
make remote-deploy
```

### Node.js 后端 (PM2)

```bash
cd my-node-app
bash deployment-docs/scripts/setup-deployment.sh
# 或者手动：
cp deployment-docs/assets/Makefile.template Makefile
cp deployment-docs/assets/Dockerfile.node-pm2 Dockerfile
cp deployment-docs/assets/ecosystem.config.js ./
cp deployment-docs/assets/docker-compose.*.yaml.template ./

make test
make remote-deploy
```

### Next.js 前端 (Nginx)

```bash
cd my-nextjs-app
bash deployment-docs/scripts/setup-deployment.sh
# 或者手动：
cp deployment-docs/assets/Makefile.template Makefile
cp deployment-docs/assets/Dockerfile.nextjs-nginx Dockerfile
cp deployment-docs/assets/docker-compose.*.yaml.template ./
mkdir -p docker/nginx
cp deployment-docs/assets/nginx.conf.template docker/nginx/
cp deployment-docs/assets/nginx.entrypoint.sh docker/nginx/
chmod +x docker/nginx/entrypoint.sh

make test
make remote-deploy
```

## 🔧 故障排查

### 镜像推送失败

```bash
# 检查登录
docker login registry.example.com:5000

# 检查网络
ping registry.example.com
```

### 部署失败

```bash
# 查看日志
make remote-logs

# 手动检查
ssh user@host "docker ps"
ssh user@host "docker logs container-name"
```

### 依赖服务未启动

在 docker-compose.yaml 中添加健康检查：
```yaml
depends_on:
  db:
    condition: service_healthy
```

## 📖 参考文档

- **完整文档**: `deployment-docs/README.md`
- **快速开始**: `deployment-docs/references/quickstart.md`
- **概览说明**: `deployment-docs/references/overview.md`
- **自动化脚本**: `deployment-docs/scripts/setup-deployment.sh`

## 🎯 最佳实践

1. ✅ 使用版本控制 (Git)
2. ✅ 配置健康检查
3. ✅ 设置资源限制
4. ✅ 日志持久化
5. ✅ 数据卷备份
6. ✅ 定期清理无用镜像
7. ✅ 使用环境变量管理配置
8. ✅ 测试环境与生产环境隔离

## 📝 版本信息

**技能版本**: v1.0.0
**文档版本**: v3.0
**最后更新**: 2026-01-12
**适用范围**: 所有项目（Go/Python/Node.js/Java/Rust/Next.js）
**支持模式**: Monorepo / 独立项目 / 多服务