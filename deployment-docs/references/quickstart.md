# 快速开始指南

> 5 分钟快速搭建你的部署体系

---

## 🎯 目标

为你的项目（Go/Python/Node.js/Java/Rust/Next.js）搭建完整的 Docker 部署流程，支持：
- ✅ 本地开发测试
- ✅ 测试环境部署
- ✅ 生产环境部署
- ✅ 一键式命令

---

## 📋 准备工作

### 1. 环境要求

```bash
# 本地环境
✓ Docker
✓ Docker Compose
✓ Make
✓ SSH (远程部署)

# 远程服务器
✓ Docker
✓ Docker Compose
✓ SSH 访问权限
```

### 2. 仓库配置

```bash
# 登录镜像仓库
docker login registry.example.com:5000

# 配置 SSH 免密登录 (可选但推荐)
ssh-keygen -t rsa
ssh-copy-id user@remote-host
```

---

## 🚀 5分钟快速开始

### 场景 1: Go 项目

#### 第1步：创建项目结构

```bash
mkdir my-go-app && cd my-go-app
```

#### 第2步：复制模板文件

```bash
cp deployment-docs/templates/Makefile.template Makefile
cp deployment-docs/templates/Dockerfile.go Dockerfile
cp deployment-docs/templates/docker-compose.local.yaml.template docker-compose.local.yaml
cp deployment-docs/templates/docker-compose.test.yaml.template docker-compose.test.yaml
cp deployment-docs/templates/docker-compose.yaml.template docker-compose.yaml
```

#### 第3步：修改配置

**编辑 Makefile** (修改第 14-24 行):

```makefile
# 修改这些值
APP_NAME ?= go-app  # 你的应用名称

# 修改环境配置
ifeq ($(ENV_MODE), test)
  REGISTRY_HOST = 192.168.1.100:5000  # 你的测试仓库地址
  REMOTE_USER = root
  REMOTE_HOST = test-server
  REMOTE_COMPOSE_PATH = /opt/docker-composes
else ifeq ($(ENV_MODE), prod)
  REGISTRY_HOST = registry.example.com:5000  # 你的生产仓库地址
  REMOTE_USER = deploy
  REMOTE_HOST = prod-server
  REMOTE_COMPOSE_PATH = ~/docker-composes
endif
```

**编辑 Dockerfile** (修改端口和健康检查):
```dockerfile
EXPOSE 8080  # 根据你的应用端口修改

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:8080/health || exit 1
```

**编辑 docker-compose.yaml** (修改镜像名):
```yaml
services:
  app:
    image: registry.example.com:5000/go-app:latest  # 修改为你的镜像名
    container_name: go-app
```

#### 第4步：测试部署

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

### 场景 2: Python 项目

#### 第1步：创建项目

```bash
mkdir my-python-app && cd my-python-app
```

#### 第2步：复制模板

```bash
cp deployment-docs/templates/Makefile.template Makefile
cp deployment-docs/templates/Dockerfile.python Dockerfile
cp deployment-docs/templates/docker-compose.*.yaml.template ./
```

#### 第3步：创建依赖文件

```bash
# 创建 requirements.txt
pip freeze > requirements.txt

# 创建 main.py (示例)
cat > main.py << 'EOF'
from flask import Flask
import os

app = Flask(__name__)

@app.route('/health')
def health():
    return 'healthy\n'

@app.route('/')
def hello():
    return 'Hello from Python!\n'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
EOF

# 添加到 requirements.txt
echo "flask==3.0.0" >> requirements.txt
```

#### 第4步：修改配置并部署

```bash
# 修改 Makefile 中的配置
# 然后测试部署
make test
make remote-deploy
```

---

### 场景 3: Node.js 后端项目

#### 第1步：创建项目

```bash
mkdir my-node-app && cd my-node-app
npm init -y
```

#### 第2步：复制模板

```bash
cp deployment-docs/templates/Makefile.template Makefile
cp deployment-docs/templates/Dockerfile.node-pm2 Dockerfile
cp deployment-docs/templates/ecosystem.config.js ./
cp deployment-docs/templates/docker-compose.*.yaml.template ./
```

#### 第3步：修改配置

**编辑 ecosystem.config.js**:
```javascript
module.exports = {
  apps: [{
    name: 'node-app',      // 修改为你的应用名
    script: './server.js', // 修改为你的入口文件
    // ...
  }]
}
```

**创建示例 server.js**:
```javascript
const http = require('http');

const server = http.createServer((req, res) => {
  if (req.url === '/health') {
    res.writeHead(200, { 'Content-Type': 'text/plain' });
    res.end('healthy\n');
  } else {
    res.writeHead(200, { 'Content-Type': 'text/plain' });
    res.end('Hello from Node.js!\n');
  }
});

server.listen(3000, '0.0.0.0', () => {
  console.log('Server running on port 3000');
});
```

#### 第4步：测试部署

```bash
make test
make remote-deploy
```

---

### 场景 4: Next.js 前端项目

#### 第1步：创建项目

```bash
mkdir my-nextjs-app && cd my-nextjs-app
npx create-next-app .  # 或使用你的项目
```

#### 第2步：复制模板

```bash
cp deployment-docs/templates/Makefile.template Makefile
cp deployment-docs/templates/Dockerfile.nextjs-nginx Dockerfile
cp deployment-docs/templates/docker-compose.*.yaml.template ./
mkdir -p docker/nginx
cp deployment-docs/templates/nginx.conf.template docker/nginx/
cp deployment-docs/templates/nginx.entrypoint.sh docker/nginx/
chmod +x docker/nginx/entrypoint.sh
```

#### 第3步：修改配置

**编辑 Makefile**:
```makefile
APP_NAME ?= web
# ... 其他配置
```

**编辑 docker-compose.yaml**:
```yaml
services:
  web:
    image: registry.example.com:5000/web:latest
    container_name: web
    # ...
```

#### 第4步：测试部署

```bash
make test
make ENV_MODE=prod remote-deploy
```

---

### 场景 5: Monorepo 项目

#### 第1步：在每个应用目录下

```bash
cd apps/backend/api  # 或 apps/frontend/web
```

#### 第2步：复制模板

```bash
# 根据技术栈选择 Dockerfile
cp deployment-docs/templates/Makefile.template Makefile
cp deployment-docs/templates/Dockerfile.go Dockerfile  # Go 示例
cp deployment-docs/templates/docker-compose.*.yaml.template ./
```

#### 第3步：修改配置

**编辑 Makefile** (如果需要 monorepo 支持):
```makefile
# 添加 monorepo 根目录检测
MONOREPO_ROOT ?= $(shell git rev-parse --show-toplevel 2>/dev/null || cd ../.. && pwd)
BUILD_CONTEXT ?= $(MONOREPO_ROOT)
```

#### 第4步：测试部署

```bash
make test
make ENV_MODE=prod remote-deploy
```

---

## 📖 常用命令速查

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

---

## 🔧 环境配置示例

### 本地环境 (docker-compose.local.yaml)

```yaml
services:
  app:
    ports:
      - "8080:8080"  # 本地端口映射
    environment:
      - NODE_ENV=development
```

### 测试环境 (docker-compose.test.yaml)

```yaml
services:
  app:
    ports:
      - "18080:8080"  # 测试端口映射
    environment:
      - NODE_ENV=production
```

### 生产环境 (docker-compose.yaml)

```yaml
services:
  app:
    # 无端口映射，使用外部网络
    deploy:
      resources:
        limits:
          cpus: "0.5"
          memory: "1024M"
```

---

## 🎓 进阶用法

### 1. 多应用部署

```bash
# 部署后端
cd apps/backend/api
make ENV_MODE=prod remote-deploy

# 部署前端
cd apps/frontend/web
make ENV_MODE=prod remote-deploy
```

### 2. 指定版本部署

```bash
make VERSION=v1.2.3 ENV_MODE=prod remote-deploy
```

### 3. 使用 Git SHA 作为版本

```bash
make VERSION=$(git rev-parse --short HEAD) push
```

### 4. 查看完整栈状态

```bash
# 在远程服务器上
ssh user@host "docker ps"
ssh user@host "docker compose -f /opt/docker-composes/app.yaml ps"
```

---

## 🐛 常见问题

### Q: make test 报错 "file not found"

**A**: 检查当前目录是否正确，确保 Dockerfile 和 docker-compose.local.yaml 存在

### Q: 镜像推送失败

**A**:
```bash
# 检查登录
docker login registry.example.com:5000

# 检查网络
ping registry.example.com
```

### Q: 部署后服务无法访问

**A**:
```bash
# 查看日志
make remote-logs

# 检查容器状态
make remote-status

# 检查端口
ssh user@host "netstat -tlnp | grep 18080"
```

### Q: 如何清理磁盘空间

```bash
# 本地清理
make local-clean
make docker-clean

# 远程清理
ssh user@host "docker system prune -f"
```

---

## ✅ 检查清单

部署前检查：

- [ ] Dockerfile 中的应用名称已修改
- [ ] Makefile 中的仓库地址已配置
- [ ] Makefile 中的远程服务器已配置
- [ ] docker-compose.yaml 中的镜像名已修改
- [ ] Docker 仓库登录成功
- [ ] SSH 连接正常
- [ ] 本地测试通过

---

## 🎉 开始使用

选择你的项目类型：

- **Go 项目**: 参考 [场景 1](#场景-1-go-项目)
- **Python 项目**: 参考 [场景 2](#场景-2-python-项目)
- **Node.js 项目**: 参考 [场景 3](#场景-3-nodejs-后端项目)
- **Next.js 项目**: 参考 [场景 4](#场景-4-nextjs-前端项目)
- **Monorepo**: 参考 [场景 5](#场景-5-monorepo-项目)

如果遇到问题，请查看完整文档或联系团队支持。

---

**文档版本**: v3.0
**最后更新**: 2026-01-12
