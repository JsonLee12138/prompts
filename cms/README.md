# CMS (Headless Content Management System)

> 一套完整的 Headless CMS 开发框架，包含文档规范、API 标准和 Claude Skills

## 📁 目录结构

```
cms/
├── docs/                           # 原始文档
│   ├── CMS_CODING_STANDARD.md      # Go 后端编码规范 (59KB)
│   ├── CMS_RESPONSE.md             # HTTP 响应格式 (10KB)
│   └── SCHEMA_DRIVEN_DEVELOPMENT.md # Schema 驱动开发 (39KB)
│
├── skills/                         # Claude Skills (可直接使用)
│   ├── README.md                   # Skills 概览
│   ├── CLAUDE_USAGE.md            # 使用示例
│   ├── INSTALLATION.md            # 安装指南
│   ├── SUMMARY.md                 # 技能汇总
│   ├── validate-skills.sh         # 验证脚本
│   │
│   ├── cms-coding-standard/       # Skill 1: 后端标准
│   │   └── SKILL.md
│   ├── cms-response-format/       # Skill 2: 响应格式
│   │   └── SKILL.md
│   └── schema-driven-development/ # Skill 3: Schema 开发
│       └── SKILL.md
│
└── README.md                       # 本文件
```

## 📚 文档说明

### 原始文档 (docs/)
这些是详细的规范文档，适合深度阅读和参考：

| 文档 | 大小 | 用途 |
|------|------|------|
| **CMS_CODING_STANDARD.md** | 59KB | Go 后端完整编码规范 |
| **CMS_RESPONSE.md** | 10KB | HTTP 响应格式标准 |
| **SCHEMA_DRIVEN_DEVELOPMENT.md** | 39KB | Schema 驱动开发流程 |

### Claude Skills (skills/)
这些是优化后的技能文件，可直接在 Claude Code 中使用：

| Skill | 用途 | 使用方式 |
|-------|------|----------|
| **@cms/cms-coding-standard** | Go 后端开发标准 | `@cms/cms-coding-standard` |
| **@cms/cms-response-format** | API 响应格式 | `@cms/cms-response-format` |
| **@cms/schema-driven-development** | Schema 开发流程 | `@cms/schema-driven-development` |

## 🚀 快速开始

### 方式 1: 使用 Claude Skills (推荐)

在 Claude Code 中直接引用：

```bash
# 创建新模块
@cms/schema-driven-development 如何创建一个 "Product" 模块？

# 后端实现
@cms/cms-coding-standard 基于这个 schema，如何实现 4 个核心文件？

# 前端集成
@cms/cms-response-format 如何在 React 中调用 Product API？
```

### 方式 2: 阅读详细文档

```bash
# 先阅读概览
cd /Users/jsonlee/Projects/prompts/cms/docs
cat CMS_CODING_STANDARD.md | head -100

# 或者查看 Skills 使用指南
cd /Users/jsonlee/Projects/prompts/cms/skills
cat CLAUDE_USAGE.md
```

## 🎯 核心概念

### 1. Schema 驱动开发
```
Schema 定义 → 后端实现 → 前端生成
(唯一数据源)  (基于 Schema)  (自动适配)
```

### 2. 4-文件模块结构
```
module_name/
├── schema.json      # 数据定义 (唯一来源)
├── module.go        # 依赖注入 & 路由
├── controller.go    # HTTP 处理器
├── service.go       # 业务逻辑
└── dto.go           # 数据传输对象
```

### 3. 统一响应格式
```typescript
interface Response<T> {
  data: T | T[] | null;
  meta?: {
    pagination?: Pagination;
    traceId?: string;
    took?: number;
  };
}
```

## 📖 使用指南

### 对于后端开发者

1. **学习编码规范**
   ```bash
   @cms/cms-coding-standard 介绍项目的核心规范
   ```

2. **创建新模块**
   ```bash
   @cms/schema-driven-development 创建 User 模块的 schema
   @cms/cms-coding-standard 实现 User 模块的 4 个文件
   ```

3. **代码审查**
   ```bash
   @cms/cms-coding-standard 审查这段代码是否符合规范
   ```

### 对于前端开发者

1. **理解 API 格式**
   ```bash
   @cms/cms-response-format API 响应格式说明
   ```

2. **构建 API 客户端**
   ```bash
   @cms/cms-response-format 如何创建通用的 API 客户端？
   ```

3. **动态表单/表格**
   ```bash
   @cms/schema-driven-development 如何基于 schema 生成表单？
   ```

### 对于全栈开发者

```bash
# 完整的模块开发流程
@cms/schema-driven-development @cms/cms-coding-standard @cms/cms-response-format
帮我创建一个完整的 "Article" 模块，包含：
1. Schema 定义 (标题、内容、状态、作者)
2. 后端实现 (CRUD + 验证)
3. 前端组件 (表格 + 表单)
```

## 🔧 工具和脚本

### 验证 Skills
```bash
cd /Users/jsonlee/Projects/prompts/cms/skills
./validate-skills.sh
```

### 查看 Skills 概览
```bash
cat /Users/jsonlee/Projects/prompts/cms/skills/README.md
```

### 查看使用示例
```bash
cat /Users/jsonlee/Projects/prompts/cms/skills/CLAUDE_USAGE.md
```

## 📊 技术栈

| 层级 | 技术 |
|------|------|
| **后端** | Go, Ent ORM, Chi, Casbin, JWT |
| **前端** | TypeScript, React, Zod, React Hook Form |
| **API** | RESTful, Strapi-style responses |
| **架构** | Schema-driven, NestJS-style modules |

## 🎓 学习路径

### 初学者
1. 阅读 `docs/CMS_RESPONSE.md` 理解响应格式
2. 使用 `@cms/schema-driven-development` 创建第一个模块
3. 实践 `@cms/cms-coding-standard` 的 4-文件模式

### 中级开发者
1. 掌握 Schema API 的使用
2. 理解多租户和权限系统
3. 学习错误处理和调试技巧

### 高级开发者
1. 自定义中间件开发
2. 插件架构设计
3. 性能优化策略

## 🔗 相关资源

### Skills 文档
- [Skills 概览](./skills/README.md)
- [使用示例](./skills/CLAUDE_USAGE.md)
- [安装指南](./skills/INSTALLATION.md)
- [技能汇总](./skills/SUMMARY.md)

### 原始文档
- [编码规范](./docs/CMS_CODING_STANDARD.md)
- [响应格式](./docs/CMS_RESPONSE.md)
- [Schema 开发](./docs/SCHEMA_DRIVEN_DEVELOPMENT.md)

## ✅ 最佳实践

### 1. 开发新模块
```bash
# Step 1: 定义 Schema
@cms/schema-driven-development 定义 [模块名] 的 schema

# Step 2: 后端实现
@cms/cms-coding-standard 实现 4 个核心文件

# Step 3: 前端开发
@cms/cms-response-format 创建前端组件
```

### 2. 代码质量
- 始终以 Schema 为唯一数据源
- 遵循 4-文件模块结构
- 使用统一的响应格式
- 启用 API Key 认证

### 3. 团队协作
- 共享 Schema 定义
- 统一编码规范
- 一致的 API 设计

## 🤝 贡献指南

### 更新文档
1. 修改 `docs/` 中的原始文档
2. 同步更新 `skills/` 中的 SKILL.md
3. 验证格式：`./skills/validate-skills.sh`

### 添加新技能
1. 创建 `skills/new-skill/SKILL.md`
2. 遵循 YAML frontmatter 格式
3. 更新 `skills/README.md` 索引

## 📞 支持

### 遇到问题？
1. 查看 `skills/CLAUDE_USAGE.md` 获取示例
2. 使用 `@cms/` 技能提问
3. 检查原始文档的详细说明

### 需要帮助？
```bash
# 快速开始
@cms/schema-driven-development 我是新手，从哪里开始？

# 具体问题
@cms/cms-coding-standard 如何实现 API Key 认证？

# 组合使用
@cms/schema-driven-development @cms/cms-response-format
创建一个完整的用户注册流程
```

---

## 🎉 开始使用

```bash
# 方式 1: 使用 Skills (推荐)
@cms/cms-coding-standard 项目介绍

# 方式 2: 阅读文档
cat /Users/jsonlee/Projects/prompts/cms/docs/CMS_CODING_STANDARD.md | head -50
```

**祝你开发愉快！** 🚀

---

*最后更新: 2026-01-13*
*版本: 1.0.0*
*包含: 3 个 Skills + 3 个原始文档*