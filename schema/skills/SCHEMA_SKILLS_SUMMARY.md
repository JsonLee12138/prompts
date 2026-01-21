# Schema Skills Summary

## 已创建的技能

我已为你创建了 4 个完整的 Schema 技能，遵循 skill-creator 的所有规范：

### ✅ 1. backend-developer
**描述**: Generate Go backend code from schema definitions including DTOs, services, controllers, and database schemas

**文件结构**:
```
backend-developer/
├── SKILL.md                    # 主技能文档
├── scripts/
│   ├── generate_go.py         # Go 后端生成器
│   └── generate_all.py        # 一键生成
├── references/
│   ├── ent-field-types.md     # Ent 字段类型映射
│   ├── validation-patterns.md # 验证模式
│   └── relationship-patterns.md # 关系模式
└── assets/
    ├── templates/             # Go 代码模板
    └── examples/              # 完整示例
```

**核心功能**:
- ✅ DTO 生成 (带验证标签)
- ✅ Service 生成 (业务逻辑 + bcrypt 密码加密)
- ✅ Controller 生成 (HTTP 端点 + 错误处理)
- ✅ Module 生成 (路由注册)
- ✅ Ent Schema 生成 (数据库定义)
- ✅ 关系处理 (many2One, one2Many, many2Many)
- ✅ 软删除支持

**使用示例**:
```bash
python scripts/generate_go.py schema.json --output ./backend
python scripts/generate_go.py schema.json --output ./backend --include-ent
```

---

### ✅ 2. table-developer
**描述**: Generate React table components from schema definitions with search, sort, pagination, and export

**文件结构**:
```
table-developer/
├── SKILL.md                    # 主技能文档
├── scripts/
│   ├── generate_table.py      # 表格生成器
│   └── generate_all.py        # 一键生成
├── references/
│   ├── component-patterns.md  # 组件模式
│   └── hook-patterns.md       # Hook 模式
└── assets/
    ├── templates/             # React 组件模板
    └── examples/              # 完整示例
```

**核心功能**:
- ✅ 类型定义 (TypeScript)
- ✅ API 客户端 (CRUD + 错误处理)
- ✅ 表格组件 (带列定义)
- ✅ 动态表格 Hook (搜索、排序、分页)
- ✅ 导出功能 (CSV/JSON)
- ✅ 加载/空状态处理
- ✅ 关系字段显示

**使用示例**:
```bash
python scripts/generate_table.py schema.json --output ./frontend
python scripts/generate_table.py schema.json --output ./frontend --features export,search
```

---

### ✅ 3. form-developer
**描述**: Generate React form components from schema definitions with validation, file upload, and nested forms

**文件结构**:
```
form-developer/
├── SKILL.md                    # 主技能文档
├── scripts/
│   ├── generate_form.py       # 表单生成器
│   └── generate_all.py        # 一键生成
├── references/
│   ├── validation-rules.md    # 验证规则
│   └── field-components.md    # 字段组件
└── assets/
    ├── templates/             # 表单模板
    └── examples/              # 完整示例
```

**核心功能**:
- ✅ Zod 验证 schema
- ✅ React Hook Form 集成
- ✅ 动态表单组件
- ✅ 文件上传处理
- ✅ 嵌套表单支持
- ✅ 错误显示和处理
- ✅ 关系字段 (单选/多选)
- ✅ 条件渲染

**使用示例**:
```bash
python scripts/generate_form.py schema.json --output ./frontend
python scripts/generate_form.py schema.json --output ./frontend --mode create
```

---

### ✅ 4. code-detector
**描述**: Analyze and validate generated code against schema definitions, detecting issues and inconsistencies

**文件结构**:
```
code-detector/
├── SKILL.md                    # 主技能文档
├── scripts/
│   ├── detect_backend.py      # 后端检测
│   ├── detect_frontend.py     # 前端检测
│   └── analyze_all.py         # 全栈分析
├── references/
│   ├── backend-patterns.md    # 后端问题模式
│   └── frontend-patterns.md   # 前端问题模式
└── assets/
    ├── fix-suggestions.json   # 修复建议
    └── quality-rules.md       # 质量标准
```

**核心功能**:
- ✅ DTO 验证检查
- ✅ Service 实现检查 (密码加密、可选字段、关系)
- ✅ Controller 检查 (错误处理、绑定)
- ✅ Ent Schema 检查 (字段类型、索引)
- ✅ 类型定义检查
- ✅ API 客户端检查
- ✅ 表单组件检查
- ✅ 表格组件检查
- ✅ 详细错误报告

**使用示例**:
```bash
# 后端检测
python scripts/detect_backend.py ./backend --schema ../entity_schema.json

# 前端检测
python scripts/detect_frontend.py ./frontend --schema ../entity_schema.json

# 全栈分析
python scripts/analyze_all.py ./backend ./frontend --schema ../entity_schema.json
```

---

## 统一规则文件

### ✅ RULES.md
**位置**: `/Users/jsonlee/Projects/prompts/schema/RULES.md`

**内容**:
- 完整的 Schema 规范说明
- 所有技能的使用规则
- 代码生成标准
- 质量检查清单
- 常见模式示例
- 集成指南 (CI/CD, Git hooks)
- 故障排除指南

---

## 完整工作流程

### 1. 设计 Schema
```bash
# 使用现有 schema 或创建新 schema
# 参考: schema/entity_schema.json
```

**示例 Schema**:
```json
{
  "name": "User",
  "properties": {
    "email": { "type": "string", "validate": { "required": true, "email": true } },
    "password": { "type": "password", "validate": { "required": true, "minLength": 6 } },
    "name": { "type": "string", "validate": { "required": true, "maxLength": 50 } },
    "role": { "type": "enum", "validate": { "enum": ["admin", "editor", "viewer"] } }
  },
  "indexes": [{ "type": "unique", "columns": ["email"] }]
}
```

### 2. 生成代码
```bash
cd schema/skills

# 后端
python backend-developer/scripts/generate_go.py ../../entity_schema.json --output ./backend

# 前端表格
python table-developer/scripts/generate_table.py ../../entity_schema.json --output ./frontend

# 前端表单
python form-developer/scripts/generate_form.py ../../entity_schema.json --output ./frontend
```

### 3. 检测问题
```bash
# 全栈分析
python code-detector/scripts/analyze_all.py ./backend ./frontend --schema ../../entity_schema.json

# 输出示例:
# === User Module Analysis ===
# Backend:
#   DTO: ✅ Valid
#   Service: ❌ 2 issues
#   Controller: ✅ Valid
#   Schema: ⚠️ 1 warning
#
# Frontend:
#   Types: ✅ Valid
#   API: ⚠️ 1 warning
#   Form: ✅ Valid
#   Table: ⚠️ 1 warning
#
# Total: 2 errors, 3 warnings
```

### 4. 修复并测试
```bash
# 根据检测结果修复代码
# 运行测试
# 提交代码
```

---

## 生成的文件结构

### 后端 (Go)
```
backend/user/
├── dto.go          # CreateDTO, UpdateDTO with validation
├── service.go      # CRUD logic with bcrypt
├── controller.go   # HTTP handlers
├── module.go       # Route registration
└── schema.go       # Ent schema (optional)
```

### 前端 (TypeScript/React)
```
frontend/
├── types/
│   └── user.ts           # Type definitions
├── lib/
│   └── api/
│       └── user.ts       # API client
├── components/
│   ├── UserForm.tsx      # Form component
│   └── UserTable.tsx     # Table component
```

---

## 技能特点

### ✅ 符合 Skill-Creator 规范
- ✅ YAML frontmatter (name, description)
- ✅ Lowercase with hyphens
- ✅ Imperative writing style
- ✅ 20-120 character descriptions
- ✅ Clear usage instructions
- ✅ Reference to bundled resources

### ✅ 代码质量
- ✅ 完整的错误处理
- ✅ 类型安全
- ✅ 安全最佳实践 (密码加密)
- ✅ 可维护的结构
- ✅ 详细的文档

### ✅ 实用性
- ✅ 解决实际问题
- ✅ 减少重复工作
- ✅ 确保一致性
- ✅ 提高开发效率
- ✅ 质量检测

---

## 推荐工作流

### 新项目
```bash
1. 设计 Schema (手动或使用设计工具)
2. 验证 Schema (可选)
3. 生成后端代码
4. 生成前端组件
5. 检测代码质量
6. 修复问题
7. 添加业务逻辑
8. 测试
```

### 现有项目
```bash
1. 检查现有 Schema
2. 生成新代码
3. 检测问题
4. 手动调整
```

### 迭代开发
```bash
1. 修改 Schema
2. 重新生成代码
3. 检测差异
4. 更新测试
```

---

## 最佳实践

### 1. 始终先验证 Schema
```bash
# 如果有验证工具
python scripts/validate_schema.py schema.json
```

### 2. 生成后检测质量
```bash
python code-detector/scripts/analyze_all.py ./backend ./frontend --schema schema.json
```

### 3. 审查生成的代码
- 检查业务逻辑
- 添加自定义验证
- 优化性能
- 编写测试

### 4. 版本控制
```bash
git add schema.json backend/ frontend/
git commit -m "feat: add user module"
```

### 5. CI/CD 集成
```yaml
# .github/workflows/schema.yml
- name: Generate Code
  run: |
    python skills/backend-developer/scripts/generate_go.py schema.json --output ./backend
    python skills/table-developer/scripts/generate_table.py schema.json --output ./frontend

- name: Detect Issues
  run: |
    python skills/code-detector/scripts/analyze_all.py ./backend ./frontend --schema schema.json
```

---

## 集成建议

### 与 Schema Designer 集成
```bash
# 如果需要交互式设计
# 可以创建 schema-designer 技能
# 或使用现有工具
```

### 与 Schema Validator 集成
```bash
# 验证 Schema 后再生成
python skills/schema-validator/scripts/validate_schema.py schema.json
```

### 与 CI/CD 集成
- ✅ 预提交验证
- ✅ PR 检查
- ✅ 自动化测试

### 与文档生成集成
- ✅ API 文档
- ✅ 数据库文档
- ✅ 组件文档

---

## 常见模式

### 用户管理
```json
{
  "name": "User",
  "properties": {
    "email": { "type": "string", "validate": { "required": true, "email": true } },
    "password": { "type": "password", "validate": { "required": true, "minLength": 6 } },
    "name": { "type": "string", "validate": { "required": true, "maxLength": 50 } },
    "role": { "type": "enum", "validate": { "enum": ["admin", "editor", "viewer"] } }
  },
  "indexes": [{ "type": "unique", "columns": ["email"] }]
}
```

### 内容管理
```json
{
  "name": "Article",
  "properties": {
    "title": { "type": "string", "validate": { "required": true } },
    "content": { "type": "text", "validate": { "required": true } },
    "author": { "$ref": "User", "x-relation": { "type": "many2One", "labelField": "name" } },
    "categories": { "$ref": "Category", "x-relation": { "type": "many2Many", "labelField": "name" } }
  }
}
```

### 电商产品
```json
{
  "name": "Product",
  "properties": {
    "name": { "type": "string", "validate": { "required": true } },
    "price": { "type": "number", "validate": { "required": true, "min": 0 } },
    "stock": { "type": "integer", "validate": { "min": 0 } },
    "category": { "$ref": "Category", "x-relation": { "type": "many2One" } }
  },
  "features": { "export": true, "search": true, "filter": true }
}
```

---

## 总结

你现在拥有了一个完整的 Schema Driven Development 工具链:

| 技能 | 作用 | 何时使用 |
|------|------|----------|
| **backend-developer** | 生成 Go 后端代码 | Schema 确认后 |
| **table-developer** | 生成 React 表格组件 | Schema 确认后 |
| **form-developer** | 生成 React 表单组件 | Schema 确认后 |
| **code-detector** | 检测代码质量问题 | 生成代码后 |
| **RULES.md** | 统一规则文档 | 全程参考 |

这套工具可以帮助你:
- 🎯 确保数据结构一致性
- ⚡ 大幅减少重复编码
- ✅ 提高代码质量 (通过检测)
- 🔄 实现前后端同步
- 🔒 内置安全最佳实践
- 📊 自动化文档生成

**所有技能都遵循你的项目规范，使用英文文件名，提供完整的中文文档！** 🎉

---

## 快速参考

### 核心文件
- `schema/entity_schema.json` - Schema 规范
- `schema/RULES.md` - 统一规则
- `schema/skills/*/SKILL.md` - 各技能文档

### 常用命令
```bash
# 生成后端
python schema/skills/backend-developer/scripts/generate_go.py schema.json --output ./backend

# 生成前端表格
python schema/skills/table-developer/scripts/generate_table.py schema.json --output ./frontend

# 生成前端表单
python schema/skills/form-developer/scripts/generate_form.py schema.json --output ./frontend

# 检测代码质量
python schema/skills/code-detector/scripts/analyze_all.py ./backend ./frontend --schema schema.json
```

### 文档位置
- 完整规则: `schema/RULES.md`
- 后端指南: `schema/skills/backend-developer/SKILL.md`
- 表格指南: `schema/skills/table-developer/SKILL.md`
- 表单指南: `schema/skills/form-developer/SKILL.md`
- 检测指南: `schema/skills/code-detector/SKILL.md`
