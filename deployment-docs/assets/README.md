# 通用项目部署模板文件

这些模板文件可以帮助你快速搭建任何项目的部署体系（Go/Python/Node.js/Java/Rust/Next.js）。

## 📁 文件说明

### Makefile
- **Makefile.template**: 通用部署脚本，支持本地/测试/生产环境

### Docker Compose 配置
- **docker-compose.local.yaml.template**: 本地开发环境
- **docker-compose.test.yaml.template**: 测试环境
- **docker-compose.yaml.template**: 生产环境

### Dockerfile
- **Dockerfile.go**: Go 项目
- **Dockerfile.python**: Python 项目
- **Dockerfile.node-pm2**: Node.js 项目 (PM2)
- **Dockerfile.nextjs-nginx**: Next.js 项目 (Nginx)
- **Dockerfile.java**: Java Spring Boot 项目
- **Dockerfile.rust**: Rust 项目

### 配置文件
- **nginx.conf.template**: Nginx 配置模板
- **nginx.entrypoint.sh**: Nginx 入口脚本
- **ecosystem.config.js**: PM2 配置文件

---

## 🚀 快速开始

### 步骤 1: 复制模板到你的项目目录

```bash
# 假设你的项目在 my-project
cd my-project

# 复制 Makefile
cp deployment-docs/templates/Makefile.template Makefile

# 复制 Dockerfile (选择你的技术栈)
cp deployment-docs/templates/Dockerfile.go Dockerfile  # Go
# 或
cp deployment-docs/templates/Dockerfile.python Dockerfile  # Python
# 或
cp deployment-docs/templates/Dockerfile.node-pm2 Dockerfile  # Node.js
# 或其他

# 复制 Docker Compose 文件
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

### 步骤 2: 修改配置

#### 修改 Makefile

```makefile
# 修改这些变量
APP_NAME ?= your-app-name  # 你的应用名称

# 修改环境配置
ifeq ($(ENV_MODE), test)
  REGISTRY_HOST = 192.168.1.100:5000  # 你的测试仓库
  REMOTE_USER = root
  REMOTE_HOST = test-server
else ifeq ($(ENV_MODE), prod)
  REGISTRY_HOST = registry.example.com:5000  # 你的生产仓库
  REMOTE_USER = deploy
  REMOTE_HOST = prod-server
endif
```

#### 修改 Dockerfile

```dockerfile
# 根据技术栈调整
# - 端口号
# - 启动命令
# - 环境变量
# - 健康检查
```

#### 修改 Docker Compose

```yaml
services:
  app:  # 修改服务名
    image: registry.example.com:5000/your-app-name:latest  # 修改镜像名
    container_name: your-app-name  # 修改容器名
```

### 步骤 3: 测试部署

```bash
# 1. 本地测试
make test

# 2. 构建镜像
make build

# 3. 推送到仓库
make push

# 4. 部署到测试环境
make remote-deploy

# 5. 部署到生产环境
make ENV_MODE=prod remote-deploy
```

---

## 📝 使用示例

### Go 项目

```bash
cd my-go-app

# 本地开发
make test

# 部署
make remote-deploy
make ENV_MODE=prod remote-deploy
```

### Python 项目

```bash
cd my-python-app

# 本地开发
make test

# 部署
make remote-deploy
make ENV_MODE=prod remote-deploy
```

### Node.js 项目 (PM2)

```bash
cd my-node-app

# 本地开发
make test

# 部署
make remote-deploy
make ENV_MODE=prod remote-deploy
```

### Next.js 项目 (Nginx)

```bash
cd my-nextjs-app

# 本地开发
make test

# 部署
make remote-deploy
make ENV_MODE=prod remote-deploy
```

---

## 🔧 环境配置

### 本地环境
- Registry: localhost:5000
- 服务器: localhost
- 端口映射: 有

### 测试环境
- Registry: registry.example.com:5000
- 服务器: test-server
- 端口映射: 有 (18080+)

### 生产环境
- Registry: registry.example.com:5000
- 服务器: prod-server
- 端口映射: 无

---

## 📖 常用命令

```bash
# 查看帮助
make help

# 查看配置
make info

# 本地测试
make test

# 构建镜像
make build

# 推送镜像
make push

# 完整部署
make remote-deploy

# 查看日志
make remote-logs

# 查看状态
make remote-status

# 重启服务
make remote-restart

# 回滚版本
make rollback

# 清理
make local-clean
make docker-clean
```

---

## ⚙️ 环境变量

在 Docker Compose 文件中配置：

```yaml
environment:
  - NODE_ENV=production
  - PORT=3000
  - API_HOST=api
  - API_PORT=3000
  - DATABASE_URL=postgresql://user:pass@db:5432/mydb
  - REDIS_URL=redis://redis:6379
  - JWT_SECRET=your-secret-key
```

---

## 🐛 故障排查

### 问题: 镜像推送失败
```bash
# 检查登录
docker login registry.example.com:5000

# 检查网络
ping registry.example.com
```

### 问题: 部署失败
```bash
# 查看日志
make remote-logs

# 手动检查
ssh user@host "docker ps"
ssh user@host "docker logs container-name"
```

### 问题: 依赖服务未启动
```yaml
# 在 docker-compose.yaml 中添加
depends_on:
  db:
    condition: service_healthy
```

---

## 📚 参考文档

- 完整文档: [README.md](../README.md)
- 快速开始: [docs/quickstart.md](../docs/quickstart.md)
- 文件清单: [docs/file-list.md](../docs/file-list.md)

---

## 🎯 最佳实践

1. ✅ 使用版本控制 (Git)
2. ✅ 使用健康检查
3. ✅ 配置资源限制
4. ✅ 日志持久化
5. ✅ 数据卷备份
6. ✅ 定期清理无用镜像
7. ✅ 使用环境变量管理配置
8. ✅ 测试环境与生产环境隔离

---

## 📞 支持

如有问题，请参考完整文档或联系团队维护者。

---

**文档版本**: v3.0
**最后更新**: 2026-01-12
**适用范围**: 所有项目（Go/Python/Node.js/Java/Rust/Next.js）
