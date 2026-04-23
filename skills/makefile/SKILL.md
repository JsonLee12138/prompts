---
name: makefile
description: "Use when creating, editing, or validating Makefiles. Provides templates for Go, Node, Python, Docker, and Monorepo projects with self-documenting help targets. Also validates existing Makefiles against conventions. Triggers on: Makefile, makefile, make help, validate makefile, lint makefile."
---

# Makefile Skill

## Overview

Makefile 模板生成与验证工具。支持两种模式：

1. **Generate** — 根据项目类型生成标准化 Makefile 模板
2. **Validate** — 检查现有 Makefile 是否符合规范

核心原则：**注释即文档，`make` 即入口。**

## Mode Selection

```
用户说 "创建/生成 Makefile" → Generate 模式
用户说 "validate/检查/lint Makefile" → Validate 模式
用户未明确 → 询问选择
```

---

## Generate 模式

### Template Selection

根据项目类型选择模板。如果用户未指定，通过以下方式自动检测：

1. 检查 `go.mod` → Go 模板
2. 检查 `package.json` → Node 模板
3. 检查 `pyproject.toml` 或 `setup.py` → Python 模板
4. 检查 `docker-compose.yml` → Docker 模板
5. 检查 `pnpm-workspace.yaml` 或 `lerna.json` → Monorepo 模板
6. 无法检测 → 询问用户选择

### Available Templates

| 模板 | 文件 | 适用场景 |
|------|------|----------|
| Go | `assets/Makefile.go.tmpl` | Go 项目，含 build/test/lint/docker |
| Node | `assets/Makefile.node.tmpl` | Node.js/TypeScript，自动检测包管理器 |
| Python | `assets/Makefile.python.tmpl` | Python 项目，含 venv/pytest/ruff |
| Docker | `assets/Makefile.docker.tmpl` | Docker Compose 项目，含 up/down/logs |
| Monorepo | `assets/Makefile.monorepo.tmpl` | 多包仓库，支持 filter 单包操作 |

### Generate Workflow

1. 检测或询问项目类型
2. 读取对应模板 `assets/Makefile.<type>.tmpl`
3. 根据项目实际情况调整变量（APP_NAME、端口等）
4. 写入 `Makefile`
5. 提示用户运行 `make` 验证 help 输出

### Convention

`## 描述` 写在 target 同一行，`make`（无参数）自动输出所有 target 及说明。

```makefile
.DEFAULT_GOAL := help

help: ## 显示帮助信息
	@grep -E '^[a-zA-Z_-]+:.*?## ' $(MAKEFILE_LIST) | sed 's/:.*##/:/' | awk -F: '{gsub(/^ /, "", $$2); printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

build: ## 编译项目
	go build ./...
```

### Rules

1. `.DEFAULT_GOAL := help` — 无参数 `make` 等同 `make help`
2. `.PHONY` 声明所有非文件 target
3. `##` 注释必须与 target 在同一行，格式：`target: deps ## 描述`
4. 描述用中文或英文，保持项目内一致
5. `help` 的 grep/awk 管线不要随意改动
6. 带依赖的 target：`setup-db: create-network ## 启动数据库`

---

## Validate 模式

### Trigger

```
用户说: "validate Makefile" / "检查 Makefile" / "lint Makefile"
```

### Workflow

1. 读取目标 Makefile（默认当前目录，或用户指定路径）
2. 按 `references/validation-rules.md` 中的规则逐项检查
3. 输出格式化报告

### Validation Rules Summary

**ERROR (必须修复)：**
- E01: `.DEFAULT_GOAL := help` 存在
- E02: `help` target 存在
- E03: `help` 使用 `##` 解析
- E04: 每个非文件 target 有 `##` 注释
- E05: `##` 注释在同一行
- E06: `##` 后有空格
- E07: `.PHONY` 声明完整
- E08: 缩进使用 Tab

**WARNING (建议修复)：**
- W01: 显式声明 `SHELL`
- W02: `clean` target 存在
- W03: 变量使用 `:=`
- W04: 长命令合理换行
- W05: `help` 管线包含 ANSI 高亮
- W06: target 按功能分组

**INFO (最佳实践)：**
- I01: 常用 target 覆盖 (build/test/lint/clean)
- I02: VERSION 从 git 获取
- I03: Docker target 命名一致
- I04: 避免硬编码路径

### Output Format

```
Makefile Validation Report
══════════════════════════

ERROR (2)
  E01  .DEFAULT_GOAL := help 未设置
  E04  target 'deploy' 缺少 ## 注释

WARNING (1)
  W01  未声明 SHELL 变量

INFO (1)
  I01  建议添加 lint target

Result: FAIL (2 errors, 1 warning, 1 info)
```

### Validate Completion

Validate 完成后：
1. 展示报告
2. 如果有 ERROR，询问用户是否自动修复
3. 自动修复后重新 validate 确认通过

---

## Common Mistakes

| 错误 | 正确 |
|------|------|
| `##` 注释在 target 上方单独一行 | `##` 写在 target 同一行 |
| 缺少 `.DEFAULT_GOAL := help` | 必须设置 |
| `##` 后无空格 | `## 描述`，`##` 后必须有空格 |
| help 管线用 awk `-F:` 切 3 段 | 用 `sed 's/:.*##/:/'` 先归一化 |
| recipe 用空格缩进 | 必须用 Tab |
| `.PHONY` 遗漏 target | 所有非文件 target 都要声明 |
