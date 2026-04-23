# Makefile Validation Rules

## Validate Command

运行方式：在目标项目目录下执行，对现有 Makefile 进行检查。

```
用户说: "validate Makefile" 或 "检查 Makefile" 或 "lint Makefile"
```

## 检查项

### 必须通过 (ERROR)

| ID | 规则 | 说明 |
|----|------|------|
| E01 | `.DEFAULT_GOAL := help` 存在 | 无参数 `make` 必须输出帮助 |
| E02 | `help` target 存在 | 必须有自文档化 help 目标 |
| E03 | `help` 使用 `##` 解析 | help 管线必须 grep `##` 注释 |
| E04 | 每个非文件 target 有 `##` 注释 | 所有 `.PHONY` target 必须有描述 |
| E05 | `##` 注释在同一行 | `##` 不能写在 target 上方 |
| E06 | `##` 后有空格 | 格式：`target: ## 描述` |
| E07 | `.PHONY` 声明完整 | 所有非生成文件的 target 必须在 `.PHONY` 中声明 |
| E08 | 缩进使用 Tab | recipe 行必须用 Tab 缩进，不能用空格 |

### 建议修复 (WARNING)

| ID | 规则 | 说明 |
|----|------|------|
| W01 | `SHELL := /bin/bash` 或 `/bin/sh` | 显式声明 shell 避免环境差异 |
| W02 | `clean` target 存在 | 项目应有清理构建产物的能力 |
| W03 | 变量使用 `:=` 而非 `=` | `:=` 为简单扩展，避免递归展开陷阱 |
| W04 | 多行命令用 `\` 换行 | 长命令应合理换行提高可读性 |
| W05 | `help` 管线包含 ANSI 高亮 | 终端输出应有颜色区分 |
| W06 | target 按功能分组并空行分隔 | 提高可读性 |

### 最佳实践 (INFO)

| ID | 规则 | 说明 |
|----|------|------|
| I01 | 常用 target 覆盖 | build, test, lint, clean 至少存在 |
| I02 | `VERSION` 从 git 获取 | 使用 `git describe --tags` |
| I03 | Docker target 命名一致 | `docker-build`, `docker-run` |
| I04 | 避免硬编码路径 | 使用变量而非绝对路径 |

## Validate 输出格式

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

## 验证逻辑

1. 读取 Makefile 内容
2. 解析所有 target 定义（匹配 `^[a-zA-Z_-]+:` 行）
3. 检查 `.DEFAULT_GOAL` 是否设置为 `help`
4. 检查 `help` target 是否存在且使用 `##` 解析
5. 检查每个 target 是否有 `##` 注释
6. 检查 `.PHONY` 声明是否完整
7. 检查缩进是否使用 Tab
8. 检查 WARNING 和 INFO 级别的最佳实践
9. 输出格式化报告

## 常见修复方式

### E01: 缺少 .DEFAULT_GOAL
```makefile
.DEFAULT_GOAL := help
```

### E04: target 缺少注释
```makefile
# 之前
deploy:
	./deploy.sh

# 之后
deploy: ## 部署到生产环境
	./deploy.sh
```

### E07: .PHONY 不完整
```makefile
.PHONY: help build test lint clean deploy
```

### W01: 缺少 SHELL 声明
```makefile
SHELL := /bin/bash
```
