# 部署文档整理说明

## 📁 新目录结构

```
deployment-docs/
├── README.md                          # 主文档 - 完整部署指南
├── overview.md                        # 本文件 - 整理说明
│
├── docs/                              # 文档目录
│   ├── quickstart.md                    # 5分钟快速开始指南
│   └── file-list.md                    # 文件清单和配置说明
│
└── templates/                         # 模板文件目录
    ├── Makefile.template              # 通用部署 Makefile
    │
    ├── Dockerfile.go                  # Go 项目
    ├── Dockerfile.python              # Python 项目
    ├── Dockerfile.node-pm2            # Node.js (PM2)
    ├── Dockerfile.nextjs-nginx        # Next.js (Nginx)
    ├── Dockerfile.java                # Java Spring Boot
    ├── Dockerfile.rust                # Rust 项目
    ├── Dockerfile.frontend            # 前端 (旧版)
    ├── Dockerfile.backend             # 后端 (旧版)
    │
    ├── docker-compose.local.yaml.template   # 本地开发
    ├── docker-compose.test.yaml.template    # 测试环境
    ├── docker-compose.yaml.template         # 生产环境
    │
    ├── ecosystem.config.js            # PM2 配置
    ├── nginx.conf.template            # Nginx 配置
    ├── nginx.entrypoint.sh            # Nginx 入口脚本
    │
    └── README.md                      # 模板使用说明
```

---

## 🎯 核心特点

### 1. **完全通用**
- 适用于任何技术栈：Go, Python, Node.js, Java, Rust, Next.js
- 不绑定特定项目结构
- 支持 monorepo 和独立项目

### 2. **Makefile 自动化**
```bash
make test              # 本地测试
make build             # 构建镜像
make push              # 推送镜像
make remote-deploy     # 完整部署
make remote-logs       # 查看日志
make rollback          # 回滚版本
```

### 3. **多环境支持**
- **本地**: docker-compose.local.yaml (端口映射)
- **测试**: docker-compose.test.yaml (端口映射 + 数据库)
- **生产**: docker-compose.yaml (资源限制 + 外部网络)

### 4. **技术栈分离**
- **Node.js 后端**: PM2 进程管理（无需 Nginx）
- **Next.js 前端**: Nginx 静态服务
- **Go/Python/Java/Rust**: 直接运行二进制

---

## 📚 文档说明

### 主文档: `README.md`
- 完整的架构说明
- 所有技术栈的 Dockerfile 模板
- 所有环境的 docker-compose 配置
- 完整 Makefile
- 使用示例和故障排查

### 快速开始: `docs/quickstart.md`
- 5分钟快速搭建
- 按技术栈的场景化示例
- 常用命令速查表
- 常见问题解答

### 文件清单: `docs/file-list.md`
- 所有模板文件列表
- 配置修改清单
- 部署检查清单

---

## 🚀 使用流程

### 方式 1: 学习完整文档
```
README.md → quickstart.md → 实际操作
```

### 方式 2: 直接使用模板
```
1. 阅读 quickstart.md
2. 选择技术栈
3. 复制 templates/ 下的文件
4. 修改配置
5. 测试部署
```

---

## 🔧 配置清单

### 必须修改的配置

#### 1. Makefile (第 6, 14-24 行)
```makefile
APP_NAME ?= your-app-name
REGISTRY_HOST = your-registry:5000
REMOTE_USER = your-user
REMOTE_HOST = your-host
```

#### 2. Dockerfile (根据技术栈)
```dockerfile
# 端口号、启动命令、健康检查
```

#### 3. docker-compose.yaml
```yaml
# 镜像名称、容器名称、环境变量
```

---

## ✅ 部署流程

```bash
# 1. 复制模板
cd your-project
cp deployment-docs/templates/Makefile.template Makefile
cp deployment-docs/templates/Dockerfile.go Dockerfile  # 选择技术栈
cp deployment-docs/templates/docker-compose.*.yaml.template ./

# 2. 修改配置
# 编辑 Makefile, Dockerfile, docker-compose.yaml

# 3. 测试部署
make test
make remote-deploy
make ENV_MODE=prod remote-deploy
```

---

## 🗑️ 清理旧文档

如果需要清理原来的旧文档，可以删除以下文件：

```bash
# 删除旧的文档（如果不再需要）
rm PPBL_Monorepo_通用部署文档.md
rm Monorepo_通用部署指南.md
rm quickstart.md
rm file-list.md
rm 通用部署方案.md
rm font_end.md

# 保留 templates/ 目录（已复制到 deployment-docs/templates/）
# 保留 ARCHITECTURE.md（其他用途）
```

---

## 📝 版本信息

**文档版本**: v3.0
**最后更新**: 2026-01-12
**适用范围**: 所有项目（Go/Python/Node.js/Java/Rust/Next.js）
**支持模式**: Monorepo / 独立项目 / 多服务

---

## 🎯 下一步

1. **阅读主文档**: `deployment-docs/README.md`
2. **快速开始**: `deployment-docs/docs/quickstart.md`
3. **选择模板**: 根据技术栈选择 Dockerfile
4. **复制使用**: 复制 templates 到你的项目
5. **修改配置**: 按照清单修改
6. **测试部署**: 从本地测试开始

---

## 💡 提示

- 所有模板文件都已准备就绪
- 文档已完全脱离特定技术栈
- Makefile 保持统一，无需修改
- 只需根据项目类型选择对应的 Dockerfile
- 支持任意技术栈的扩展

---

**整理完成**: 2026-01-12
