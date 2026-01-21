# CMS 快速索引

## 🔍 快速查找

### 我想... 创建新模块
→ **使用**: `@cms/schema-driven-development`
→ **文档**: `docs/SCHEMA_DRIVEN_DEVELOPMENT.md`
→ **参考**: `skills/schema-driven-development/SKILL.md`

### 我想... 实现后端
→ **使用**: `@cms/cms-coding-standard`
→ **文档**: `docs/CMS_CODING_STANDARD.md`
→ **参考**: `skills/cms-coding-standard/SKILL.md`

### 我想... 处理 API 响应
→ **使用**: `@cms/cms-response-format`
→ **文档**: `docs/CMS_RESPONSE.md`
→ **参考**: `skills/cms-response-format/SKILL.md`

### 我想... 了解使用方法
→ **阅读**: `skills/CLAUDE_USAGE.md`
→ **安装**: `skills/INSTALLATION.md`

---

## 📋 按场景索引

### 场景 1: 第一次使用
```
1. 阅读: README.md (本文件)
2. 使用: @cms/schema-driven-development 了解工作流
3. 实践: 创建一个简单的 User 模块
```

### 场景 2: 创建完整模块
```
Step 1: @cms/schema-driven-development 定义 schema
Step 2: @cms/cms-coding-standard 实现后端
Step 3: @cms/cms-response-format 构建前端
```

### 场景 3: 代码审查
```
@cms/cms-coding-standard 请审查这段代码是否符合规范
```

### 场景 4: 调试 API
```
@cms/cms-response-format 如何使用 traceId 调试？
```

### 场景 5: 学习架构
```
@cms/schema-driven-development 介绍架构设计原则
```

---

## 📖 文档导航

### Skills (Claude Code 使用)
| Skill | 命令 | 用途 |
|-------|------|------|
| **后端标准** | `@cms/cms-coding-standard` | Go 代码规范 |
| **响应格式** | `@cms/cms-response-format` | API 格式 |
| **Schema 开发** | `@cms/schema-driven-development` | 开发流程 |

### 原始文档 (深度阅读)
| 文档 | 大小 | 重点 |
|------|------|------|
| **编码规范** | 59KB | 完整的 Go 后端规范 |
| **响应格式** | 10KB | API 响应标准 |
| **Schema 开发** | 39KB | 前后端同步开发 |

### 辅助文档
| 文件 | 用途 |
|------|------|
| `skills/README.md` | Skills 概览 |
| `skills/CLAUDE_USAGE.md` | 50+ 使用示例 |
| `skills/INSTALLATION.md` | 安装配置 |
| `skills/SUMMARY.md` | 项目汇总 |

---

## 🎯 按角色索引

### 后端开发者
**主要工具**: `@cms/cms-coding-standard`
**核心文档**: `docs/CMS_CODING_STANDARD.md`
**学习路径**:
1. 理解 4-文件模块结构
2. 掌握 Ent ORM 模式
3. 学习 API Key 认证

### 前端开发者
**主要工具**: `@cms/cms-response-format`
**核心文档**: `docs/CMS_RESPONSE.md`
**学习路径**:
1. 理解响应格式
2. 掌握 API 客户端
3. 学习动态组件生成

### 全栈开发者
**主要工具**: 所有 3 个 Skills
**核心文档**: 所有 3 个文档
**学习路径**:
1. Schema 驱动开发流程
2. 前后端同步实现
3. 完整模块开发

---

## 🔧 常用命令

### 验证 Skills
```bash
cd /Users/jsonlee/Projects/prompts/cms/skills
./validate-skills.sh
```

### 查看文件大小
```bash
wc -l /Users/jsonlee/Projects/prompts/cms/docs/*.md
wc -l /Users/jsonlee/Projects/prompts/cms/skills/*/SKILL.md
```

### 快速预览
```bash
# 查看 Skills 概览
cat /Users/jsonlee/Projects/prompts/cms/skills/README.md

# 查看使用示例
cat /Users/jsonlee/Projects/prompts/cms/skills/CLAUDE_USAGE.md | head -50
```

---

## 📊 统计信息

### 文档统计
- **原始文档**: 3 个文件，约 108KB
- **Skills**: 3 个技能，约 2.3KB 代码
- **辅助文档**: 4 个文件，约 24KB
- **总计**: 10 个文件

### 内容分类
- **规范文档**: 3 个
- **Skills**: 3 个
- **使用指南**: 3 个
- **索引/汇总**: 2 个

---

## 🚀 开始使用

### 最快路径
```bash
# 在 Claude Code 中
@cms/schema-driven-development 我该如何开始？
```

### 完整路径
```bash
# 1. 阅读概览
cat /Users/jsonlee/Projects/prompts/cms/README.md

# 2. 了解 Skills
cat /Users/jsonlee/Projects/prompts/cms/skills/README.md

# 3. 查看示例
cat /Users/jsonlee/Projects/prompts/cms/skills/CLAUDE_USAGE.md

# 4. 开始实践
@cms/schema-driven-development 创建一个 Product 模块
```

---

## 💡 提示

### 快速搜索
使用 `grep` 查找特定内容：
```bash
# 搜索 API Key 相关
grep -r "API Key" /Users/jsonlee/Projects/prompts/cms/

# 搜索 Schema 示例
grep -r "schema.json" /Users/jsonlee/Projects/prompts/cms/
```

### 版本控制
所有文件都在 `/Users/jsonlee/Projects/prompts/cms/` 目录下，便于 Git 管理。

---

**需要帮助？** → 查看 `skills/CLAUDE_USAGE.md`
**需要示例？** → 使用 `@cms/` 技能提问
**需要文档？** → 查看 `docs/` 目录

---

*索引最后更新: 2026-01-13*