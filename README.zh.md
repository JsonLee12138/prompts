# Claude Code 技能与规则库

[English Document](./README.md)

一个全面的 Claude Code 技能和规则集合，旨在增强不同领域的 AI 辅助开发工作流。

## 📚 概述

本仓库包含可重用的技能和规则，可加载到 Claude Code 中，为以下领域提供专业能力：

- **前端开发** - React/TypeScript 标准、ESLint 配置、组件开发
- **架构设计** - 设计原则、架构决策记录（ADR）、多语言示例
- **CMS 开发** - 编码标准、响应格式、Schema 驱动开发
- **Schema 开发** - 表格/表单生成、代码检测、后端开发
- **部署文档** - 部署文档和指南

## 🚀 快速开始

### 前置要求

- 已安装 Claude Code CLI
- 项目中有 `.claude/` 目录

### 安装方法

每个技能/规则都可以通过将相关目录复制到项目的 `.claude/` 文件夹来安装：

```bash
# 复制技能
cp -r <技能目录> /path/to/your-project/.claude/skills/

# 复制规则
cp -r <规则文件>.md /path/to/your-project/.claude/rules/
```

## 📦 可用技能

### 1. 前端开发 (`frontend/`)

**技能列表：**
- `frontend-standard` - 完整的前端开发标准
- `eslint-config` - 工作空间的 ESLint 配置
- `components` - 组件开发指南

**安装方法：**
```bash
# 安装主要前端技能
cp -r frontend /path/to/your-project/.claude/skills/

# 或者安装特定的子技能
cp -r frontend/skills/eslint-config /path/to/your-project/.claude/skills/
cp -r frontend/skills/components /path/to/your-project/.claude/skills/
```

**安装规则：**
```bash
cp frontend/RULES.md /path/to/your-project/.claude/rules/frontend-rules.md
```

**功能特性：**
- PascalCase/camelCase 命名规范
- @antfu/eslint-config 标准
- UnoCSS 和颜色预设
- Git 提交规范（Conventional Commits）
- 工作空间/Monorepo 设置指南

---

### 2. 架构设计 (`architecture/`)

**主要技能：** `architecture-assistant`

**安装方法：**
```bash
cp -r architecture /path/to/your-project/.claude/skills/
```

**安装规则：**
```bash
cp architecture/RULES.md /path/to/your-project/.claude/rules/architecture-rules.md
```

**功能特性：**
- 10 个核心设计原则（SoC、SRP、DRY、KISS 等）
- 多语言示例（TypeScript、Go、Rust、Python、Java）
- 架构决策记录（ADR）模板
- 代码审查检查清单
- 反模式检测

**包含的资源：**
- 原则参考文档
- 特定语言示例
- ADR 模板和示例

---

### 3. CMS 开发 (`cms/`)

**技能列表：**
- `cms-coding-standard` - CMS 编码标准
- `cms-response-format` - 统一响应格式
- `schema-driven-development` - Schema 优先的开发工作流

**安装方法：**
```bash
# 安装所有 CMS 技能
cp -r cms/skills/* /path/to/your-project/.claude/skills/

# 或者单独安装
cp -r cms/skills/cms-coding-standard /path/to/your-project/.claude/skills/
cp -r cms/skills/cms-response-format /path/to/your-project/.claude/skills/
cp -r cms/skills/schema-driven-development /path/to/your-project/.claude/skills/
```

**安装规则：**
```bash
cp cms/RULES.md /path/to/your-project/.claude/rules/cms-rules.md
```

**功能特性：**
- Go/TypeScript 编码标准
- 统一的 API 响应格式
- Schema 验证和生成
- 安全最佳实践
- 控制器/模块的代码模板

---

### 4. Schema 开发 (`schema/`)

**技能列表：**
- `table-developer` - 表格 Schema 开发
- `form-developer` - 表单 Schema 开发
- `code-detector` - 前端/后端模式检测
- `backend-developer` - 后端代码生成

**安装方法：**
```bash
cp -r schema/skills/* /path/to/your-project/.claude/skills/
```

**安装规则：**
```bash
cp schema/RULES.md /path/to/your-project/.claude/rules/schema-rules.md
```

**功能特性：**
- Schema 驱动的表格/表单生成
- 现有代码的模式检测
- 后端脚手架
- 验证脚本

---

### 5. 部署文档 (`deployment-docs/`)

**主要技能：** 部署文档和指南

**安装方法：**
```bash
cp -r deployment-docs /path/to/your-project/.claude/skills/
```

**安装规则：**
```bash
cp deployment-docs/RULES.md /path/to/your-project/.claude/rules/deployment-rules.md
```

---

## 🛠️ 技能管理工具

### 创建新技能

使用内置的技能创建器：

```bash
# 初始化新技能
python .claude/skills/skill-creator/scripts/init_skill.py <技能名称> --path <输出目录>

# 示例
python .claude/skills/skill-creator/scripts/init_skill.py my-custom-skill --path .claude/skills/
```

### 验证技能

```bash
# 验证技能结构
python .claude/skills/skill-creator/scripts/quick_validate.py <技能目录>

# 示例
python .claude/skills/skill-creator/scripts/quick_validate.py .claude/skills/my-skill
```

### 打包技能

```bash
# 打包技能用于分发
python .claude/skills/skill-creator/scripts/package_skill.py <技能目录>

# 使用自定义输出目录
python .claude/skills/skill-creator/scripts/package_skill.py <技能目录> ./dist
```

---

## 📖 使用示例

### 示例 1：前端项目设置

```bash
# 1. 复制前端技能和规则
cp -r frontend /path/to/frontend-project/.claude/skills/
cp frontend/RULES.md /path/to/frontend-project/.claude/rules/frontend-rules.md

# 2. 询问 Claude Code
# "为我的 React TypeScript 工作空间设置 ESLint"
# "根据前端标准审查这个组件"
```

### 示例 2：架构审查

```bash
# 1. 安装架构技能
cp -r architecture /path/to/project/.claude/skills/
cp architecture/RULES.md /path/to/project/.claude/rules/architecture-rules.md

# 2. 询问 Claude Code
# "根据架构原则审查这段代码"
# "为选择 PostgreSQL 而不是 MongoDB 创建一个 ADR"
```

### 示例 3：CMS 开发

```bash
# 1. 安装 CMS 技能
cp -r cms/skills/* /path/to/cms-project/.claude/skills/
cp cms/RULES.md /path/to/cms-project/.claude/rules/cms-rules.md

# 2. 询问 Claude Code
# "按照 CMS 标准生成一个用户模块"
# "为这个端点创建 API 响应类型"
```

### 示例 4：Schema 驱动开发

```bash
# 1. 安装 Schema 技能
cp -r schema/skills/* /path/to/project/.claude/skills/
cp schema/RULES.md /path/to/project/.claude/rules/schema-rules.md

# 2. 询问 Claude Code
# "为用户管理生成一个表格 Schema"
# "检测这个代码库中的前端模式"
```

---

## 📁 目录结构

```
.
├── README.md                          # 英文文档
├── README_ZH.md                       # 中文文档（本文件）
├── CLAUDE.md                          # 全局 Claude Code 规则
├── .claude/
│   ├── skills/
│   │   └── skill-creator/             # 技能创建工具
│   └── rules/
│       └── skill-creator-rules.md     # 技能创建器使用规则
├── frontend/                          # 前端开发技能
│   ├── SKILL.md                       # 主技能文件
│   ├── RULES.md                       # 前端规则
│   ├── skills/                        # 子技能
│   ├── references/                    # 参考文档
│   ├── assets/                        # 模板和配置
│   └── templates/                     # 代码模板
├── architecture/                      # 架构设计技能
│   ├── SKILL.md
│   ├── RULES.md
│   ├── references/                    # 原则和指南
│   ├── examples/                      # 语言示例
│   ├── adrs/                          # ADR 示例
│   └── assets/                        # 模板
├── cms/                               # CMS 开发技能
│   ├── RULES.md
│   └── skills/
│       ├── cms-coding-standard/
│       ├── cms-response-format/
│       └── schema-driven-development/
├── schema/                            # Schema 开发技能
│   ├── RULES.md
│   └── skills/
│       ├── table-developer/
│       ├── form-developer/
│       ├── code-detector/
│       └── backend-developer/
└── deployment-docs/                   # 部署文档技能
    ├── SKILL.md
    ├── RULES.md
    ├── references/
    └── assets/
```

---

## 🎯 文件命名标准

根据 `CLAUDE.md` 规范：

- **始终使用英文** 命名所有文件和目录
- **禁止使用中文字符** 作为文件名
- **使用 PascalCase（大驼峰）** 命名前端组件（例外：index 文件使用小写）
- **使用 camelCase（小驼峰）** 命名页面文件
- **使用 UPPER_SNAKE_CASE** 命名 README 文件

---

## 🔧 技能结构

每个技能遵循以下标准结构：

```
skill-name/
├── SKILL.md              # 必需 - 带 YAML frontmatter 的主技能文件
├── RULES.md              # 可选 - 此技能的特定规则
├── scripts/              # 可选 - 可执行的 Python/Bash 脚本
│   └── *.py 或 *.sh
├── references/           # 可选 - 详细文档（按需加载）
│   └── *.md
└── assets/               # 可选 - 模板、配置、文件
    └── *（任何文件类型）
```

### SKILL.md 格式

```markdown
---
name: skill-name
description: 简短描述（20-120 字符，以动词开头）
---

# 技能标题

## 概述
[用 1-2 句话解释目的]

## 何时使用
[具体使用场景]

## 主要内容
[说明、指南、示例]

## 资源
[引用 scripts/references/assets]
```

---

## 💡 最佳实践

### 安装技巧

1. **选择性安装**：只安装项目需要的技能
2. **检查依赖**：某些技能引用共享资源
3. **规则冲突**：避免不同技能的规则冲突
4. **定期更新**：从此仓库拉取最新更改

### 使用技巧

1. **技能触发**：Claude 检测到相关关键词时会激活技能
2. **明确请求**：可以明确调用技能："使用 frontend-standard 技能审查这个"
3. **组合技能**：多个技能可以在一个项目中协同工作
4. **自定义**：Fork 并修改技能以适应团队需求

### 维护建议

1. **修改后验证**：修改技能后运行验证脚本
2. **记录更改**：修改时更新 SKILL.md
3. **版本控制**：在 git 中跟踪 `.claude/` 目录
4. **团队共享**：打包并分发自定义技能给团队

---

## 🤝 贡献指南

### 创建新技能

遵循 skill-creator 指南：

```bash
# 1. 初始化
python .claude/skills/skill-creator/scripts/init_skill.py my-skill --path skills/

# 2. 编辑 SKILL.md 并添加资源

# 3. 验证
python .claude/skills/skill-creator/scripts/quick_validate.py skills/my-skill

# 4. 打包
python .claude/skills/skill-creator/scripts/package_skill.py skills/my-skill
```

### 质量标准

- ✅ 带有 `name` 和 `description` 的 YAML frontmatter
- ✅ 小写连字符命名
- ✅ 清晰的"何时使用"部分
- ✅ 祈使句写作风格
- ✅ 记录引用的资源

---

## 📋 常见问题

### 如何选择需要的技能？

根据你的项目类型选择：
- **React/Vue 项目** → `frontend` + `architecture`
- **CMS 系统** → `cms` + `schema` + `architecture`
- **后端 API** → `architecture` + `schema/backend-developer`
- **全栈项目** → 组合多个技能

### 技能之间会冲突吗？

大部分技能是互补的，但注意：
- 避免安装相同领域的重复技能
- 检查 RULES.md 是否有冲突的规则
- 优先级：项目特定规则 > 技能规则 > 全局规则

### 可以修改技能吗？

可以！建议的做法：
1. Fork 此仓库
2. 修改技能以适应团队需求
3. 使用验证工具确保格式正确
4. 在团队内部分发

### 如何更新已安装的技能？

```bash
# 1. 从仓库拉取最新版本
git pull origin main

# 2. 重新复制到项目
cp -r <技能目录> /path/to/your-project/.claude/skills/

# 3. 验证
python .claude/skills/skill-creator/scripts/quick_validate.py /path/to/your-project/.claude/skills/<技能名>
```

---

## 🎓 学习路径

### 初学者

1. **第一步**：安装 `frontend-standard` 或 `architecture-assistant`
2. **第二步**：熟悉技能触发机制
3. **第三步**：尝试使用技能审查代码

### 进阶用户

1. **组合技能**：在项目中使用多个技能
2. **自定义规则**：调整 RULES.md 适应团队
3. **创建技能**：为特定需求创建新技能

### 团队管理员

1. **标准化**：为团队选择统一的技能集
2. **分发**：打包并分发自定义技能
3. **培训**：教导团队成员使用技能
4. **维护**：定期更新和优化技能

---

## 🔍 技能详细说明

### Frontend Standard（前端标准）

**适用场景：**
- React/Vue/Angular 项目
- TypeScript 项目
- 需要统一代码风格的团队

**核心功能：**
- 命名规范（PascalCase、camelCase、UPPER_SNAKE_CASE）
- ESLint 配置（@antfu/eslint-config）
- UnoCSS 集成和颜色系统
- Git 提交规范（Conventional Commits）
- 工作空间配置

**快速开始：**
```bash
cp -r frontend /path/to/project/.claude/skills/
# 然后询问："设置 ESLint 并审查我的组件"
```

---

### Architecture Assistant（架构助手）

**适用场景：**
- 需要架构审查的项目
- 制定技术决策
- 多语言项目
- 需要文档化决策（ADR）

**核心功能：**
- 10 个设计原则检查
- 5 种语言的示例代码
- ADR 模板和生成
- 反模式识别
- 代码质量评估

**快速开始：**
```bash
cp -r architecture /path/to/project/.claude/skills/
# 然后询问："审查这段代码的架构质量"
```

---

### CMS Development（CMS 开发）

**适用场景：**
- Go/TypeScript CMS 项目
- 需要统一响应格式
- Schema 驱动的开发

**核心功能：**
- 编码标准和模板
- 统一 API 响应格式
- Schema 验证和生成
- 安全最佳实践

**快速开始：**
```bash
cp -r cms/skills/* /path/to/project/.claude/skills/
# 然后询问："生成一个符合标准的用户模块"
```

---

### Schema Development（Schema 开发）

**适用场景：**
- 数据驱动的应用
- 需要自动生成 CRUD
- 表单/表格密集型应用

**核心功能：**
- 表格 Schema 生成
- 表单 Schema 生成
- 前端/后端模式检测
- 代码自动生成

**快速开始：**
```bash
cp -r schema/skills/* /path/to/project/.claude/skills/
# 然后询问："为用户管理创建 Schema"
```

---

## 📊 技能对比表

| 技能 | 前端 | 后端 | 全栈 | 架构 | 文档 |
|------|------|------|------|------|------|
| frontend-standard | ✅ | ❌ | ✅ | ⚠️ | ⚠️ |
| architecture-assistant | ✅ | ✅ | ✅ | ✅ | ✅ |
| cms-coding-standard | ⚠️ | ✅ | ✅ | ⚠️ | ❌ |
| schema-driven-development | ✅ | ✅ | ✅ | ⚠️ | ❌ |
| deployment-docs | ❌ | ⚠️ | ⚠️ | ❌ | ✅ |

**图例：**
- ✅ 强烈推荐
- ⚠️ 部分适用
- ❌ 不适用

---

## 🚀 实战案例

### 案例 1：React + TypeScript 项目

**项目需求：**
- React 18 + TypeScript
- 团队 5 人
- 需要统一代码风格

**推荐技能：**
```bash
cp -r frontend /path/to/project/.claude/skills/
cp -r architecture /path/to/project/.claude/skills/
cp frontend/RULES.md /path/to/project/.claude/rules/frontend-rules.md
cp architecture/RULES.md /path/to/project/.claude/rules/architecture-rules.md
```

**使用场景：**
- "设置 ESLint 和 Prettier"
- "审查这个组件的代码质量"
- "这个设计符合架构原则吗？"

---

### 案例 2：Go + React 全栈项目

**项目需求：**
- Go 后端 + React 前端
- RESTful API
- 需要统一响应格式

**推荐技能：**
```bash
cp -r frontend /path/to/project/.claude/skills/
cp -r cms/skills/cms-coding-standard /path/to/project/.claude/skills/
cp -r cms/skills/cms-response-format /path/to/project/.claude/skills/
cp -r architecture /path/to/project/.claude/skills/
```

**使用场景：**
- "生成一个符合标准的 Go 控制器"
- "创建统一的 API 响应格式"
- "审查前后端的架构设计"

---

### 案例 3：数据密集型应用

**项目需求：**
- 大量表单和表格
- 需要自动生成 CRUD
- Schema 驱动

**推荐技能：**
```bash
cp -r schema/skills/* /path/to/project/.claude/skills/
cp -r cms/skills/schema-driven-development /path/to/project/.claude/skills/
cp -r architecture /path/to/project/.claude/skills/
```

**使用场景：**
- "从这个 Schema 生成表格和表单"
- "检测现有代码中的数据模式"
- "生成完整的 CRUD 后端"

---

## 📞 获取帮助

### 遇到问题？

1. **查看技能文档**：每个技能的 SKILL.md 包含详细说明
2. **检查 RULES.md**：了解技能的规则和约束
3. **运行验证工具**：确保技能安装正确
4. **查看示例**：references/ 目录包含详细示例

### 常见错误

**错误 1：技能没有触发**
- 原因：技能名称或路径不正确
- 解决：检查 `.claude/skills/` 目录结构

**错误 2：规则冲突**
- 原因：多个技能有冲突的规则
- 解决：查看 RULES.md 并调整优先级

**错误 3：验证失败**
- 原因：SKILL.md 格式不正确
- 解决：参考模板修正 frontmatter

---

## 📝 许可证

[您的许可证]

---

## 🔄 版本历史

**当前版本**：1.0.0
**最后更新**：2026-01-21

### 更新日志

- **1.0.0** - 初始版本，包含前端、架构、CMS、Schema 和部署技能

---

## 🌟 快速参考卡

### 安装命令速查

```bash
# 前端项目
cp -r frontend /path/to/project/.claude/skills/

# 架构审查
cp -r architecture /path/to/project/.claude/skills/

# CMS 开发
cp -r cms/skills/* /path/to/project/.claude/skills/

# Schema 开发
cp -r schema/skills/* /path/to/project/.claude/skills/

# 验证技能
python .claude/skills/skill-creator/scripts/quick_validate.py <技能目录>

# 打包技能
python .claude/skills/skill-creator/scripts/package_skill.py <技能目录>
```

### 常用询问示例

```
# 前端
"使用前端标准审查这个组件"
"为我的 React 项目设置 ESLint"

# 架构
"审查这段代码的架构质量"
"为选择 Redis 创建 ADR"

# CMS
"生成符合 CMS 标准的用户模块"
"创建统一的 API 响应格式"

# Schema
"从 Schema 生成表格和表单"
"检测代码中的数据模式"
```

---

**使用 Claude 愉快编码！🚀**
