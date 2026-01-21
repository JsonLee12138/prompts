# Schema 驱动开发规范

> 本文档定义了基于 Schema 的前后端同步开发规范，通过统一的 Schema 定义和动态接口，确保前后端数据结构的一致性。

## 📋 规范来源

本规范基于以下核心文件定义：

- **实体 Schema 定义**: `entity_schema.json` (当前目录)
  - 定义了所有可用的字段类型、验证规则、UI 配置和关系配置
  - Schema.json 文件必须遵循此 JSON Schema 定义

- **Schema 驱动开发技能**: `../SKILL.md`
  - 完整的工作流程和使用指南
  - 包含代码生成工具和验证脚本
  - **整合了 @schema/ 所有技能**: backend-developer, table-developer, form-developer, code-detector

- **验证规则参考**: `../assets/validation-rules.md`
  - 详细的验证规则映射表
  - 前后端验证规则对照
  - **基于 @schema/RULES.md 更新**

- **技能使用规则**: `../rules.md`
  - 何时使用此 CMS 技能 vs @schema/ 独立技能
  - 集成模式说明

## 🎯 与 @schema/ 技能的关系

### 技能架构

```
┌─────────────────────────────────────────────────────────────────┐
│           CMS Schema-Driven Development Skill                   │
│         (Unified Toolkit for Headless CMS)                      │
│                                                                 │
│  集成以下 @schema/ 技能，提供完整端到端开发能力：               │
└─────────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ↓                     ↓                     ↓
┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│  @schema/    │    │  @schema/    │    │  @schema/    │    │  @schema/    │
│  backend-    │    │  table-      │    │  form-       │    │  code-       │
│  developer   │    │  developer   │    │  developer   │    │  detector    │
└──────────────┘    └──────────────┘    └──────────────┘    └──────────────┘
   Go Backend        React Tables       React Forms      Code Quality
   DTO/Service       Components         Components       Validation
```

### 核心差异

| 维度 | @schema/ 技能 (4个) | CMS 技能 (1个) |
|------|---------------------|----------------|
| **专注度** | 每个技能专注单一领域 | 统一集成所有能力 |
| **使用场景** | 特定技术栈深入开发 | 端到端模块开发 |
| **代码生成** | 专注生成特定层代码 | 完整前后端生成 |
| **验证** | 代码质量检测 | 完整工作流验证 |
| **适用性** | 技术细节参考 | 完整项目开发 |

### 使用建议

**使用 CMS 技能 (`schema-driven-development`) 当：**
- 需要创建完整模块（前后端一体）
- 遵循 Schema 优先开发流程
- 需要集成验证和生成工具
- CMS 项目开发

**使用 @schema/ 技能当：**
- 需要深入学习特定技术栈（如 Go 后端细节）
- 需要特定组件的实现参考
- 需要代码质量检测规则
- 技术研究和学习

## 📑 目录

- [1. 核心理念](#1-核心理念)
- [2. Schema 文件规范](#2-schema-文件规范)
- [3. 字段定义详解](#3-字段定义详解)
- [4. 验证规则说明](#4-验证规则说明)
- [5. UI 配置说明](#5-ui-配置说明)
- [6. 关系配置详解](#6-关系配置详解)
- [7. 模块目录结构](#7-模块目录结构)
- [8. Schema API 接口](#8-schema-api-接口)
- [9. 后端开发规范](#9-后端开发规范)
- [10. 前端集成方案](#10-前端集成方案)
- [11. 工作流程](#11-工作流程)
- [12. 完整示例](#12-完整示例)
- [13. 默认值规则汇总](#13-默认值规则汇总)
- [14. 检查清单](#14-检查清单)

---

## 1. 核心理念

### 1.1 为什么需要 Schema 驱动？

```
传统开发流程：
后端定义 API → 前端手动调用 → 手动写类型 → 容易不一致

Schema 驱动流程：
Schema 定义 → 后端接口开发 → 前端表单/表格开发 → 统一数据源 → 前后端同步
```

### 1.2 核心原则

**Schema 是唯一数据源（Single Source of Truth）**

- 后端接口：根据 Schema 定义字段和验证规则
- 前端表格：根据 Schema 生成列定义和筛选条件
- 前端表单：根据 Schema 生成字段和验证规则
- API 文档：Schema 即文档

### 1.3 优势

- ✅ **统一数据源**：Schema 是前后端的唯一数据定义
- ✅ **减少重复**：避免在前后端重复定义字段和验证规则
- ✅ **快速开发**：修改 Schema 即可同步更新前后端
- ✅ **类型安全**：前后端都基于同一 Schema 开发
- ✅ **易于维护**：数据结构变更只需修改一处

---

## 2. Schema 文件规范

### 2.1 文件位置

每个业务模块**必须**在模块目录下包含 `schema.json` 文件：

```
cms/api/v1/
├── user/
│   ├── module.go
│   ├── controller.go
│   ├── service.go
│   ├── dto.go
│   └── schema.json          # ✅ 必须存在
│
├── article/
│   ├── module.go
│   ├── controller.go
│   ├── service.go
│   ├── dto.go
│   └── schema.json          # ✅ 必须存在
```

### 2.2 Schema 完整结构

`schema.json` 必须遵循 `entity_schema.json` 的定义：

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "name": "User",
  "collectionName": "users",
  "description": "用户实体",
  "softDelete": false,
  "info": {
    "displayName": "用户管理",
    "description": "系统用户",
    "icon": "User",
    "locale": "zh-CN"
  },
  "ui": {
    "submitText": "提交用户",
    "resetText": "重置",
    "showReset": true,
    "layout": {
      "direction": "vertical",
      "gap": 16,
      "columns": 2
    }
  },
  "properties": {
    "email": {
      "type": "string",
      "label": "邮箱地址",
      "description": "用户登录邮箱",
      "validate": {
        "required": true,
        "format": "email",
        "maxLength": 100
      },
      "unique": true,
      "private": false,
      "default": "",
      "version": 1,
      "writable": true,
      "queryable": true,
      "exportable": true,
      "importable": true,
      "ui": {
        "widget": "email",
        "placeholder": "user@example.com",
        "showInList": true,
        "showInForm": true,
        "span": 12,
        "readOnly": false,
        "disabled": false
      }
    },
    "author": {
      "$ref": "User",
      "label": "作者",
      "x-relation": {
        "type": "many2One",
        "inversedBy": "articles",
        "labelField": "nickname",
        "preload": true,
        "writable": true,
        "queryable": true,
        "onDelete": "cascade"
      },
      "ui": {
        "widget": "select",
        "showInList": true,
        "showInForm": true
      }
    }
  },
  "indexes": [
    {
      "type": "unique",
      "name": "idx_email",
      "columns": ["email"],
      "unique": true
    },
    {
      "type": "index",
      "name": "idx_created_at",
      "columns": ["createdAt"]
    }
  ],
  "features": {
    "softDelete": true,
    "export": true,
    "import": true,
    "batch": true
  }
}
```

### 2.3 根级字段说明

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `$schema` | string | ✅ | JSON Schema 引用 |
| `name` | string | ✅ | 实体名称 (PascalCase: User, Article) |
| `collectionName` | string | ❌ | 数据库表名（默认 name 的小写复数） |
| `description` | string/object | ❌ | 实体描述（支持多语言） |
| `softDelete` | boolean | ❌ | 软删除支持（默认 false） |
| `info` | object | ❌ | 实体元信息 |
| `ui` | object | ❌ | 表单/页面级别的 UI 配置 |
| `properties` | object | ✅ | 字段定义 |
| `indexes` | array | ❌ | 索引定义 |
| `features` | object | ❌ | 功能开关 |

---

## 3. 字段定义详解

### 3.1 字段基础属性

每个字段支持以下属性：

```json
{
  "properties": {
    "fieldName": {
      "$ref": "EntityName",        // 关系引用（关系字段专用）
      "type": "string",            // 字段类型（普通字段）
      "label": "字段标签",          // UI 显示标签
      "description": "字段描述",    // 详细描述
      "validate": { ... },         // 验证规则
      "unique": true,              // 唯一索引
      "primaryKey": false,         // 主键
      "private": false,            // 私有字段（不返回前端）
      "default": "",               // 默认值
      "version": 1,                // 版本控制
      "writable": true,            // 是否可写
      "queryable": true,           // 是否可查询
      "exportable": true,          // 是否可导出
      "importable": true,          // 是否可导入
      "allowedTypes": ["image"],   // 媒体类型限制
      "x-relation": { ... },       // 关系配置
      "ui": { ... },               // UI 配置
      "items": { ... },            // 数组元素类型（type 为 array 时）
      "properties": { ... }        // 对象属性（type 为 object 时）
    }
  }
}
```

### 3.2 字段类型 (Type)

| 类型 | Go 类型 | TS 类型 | 说明 |
|------|---------|---------|------|
| `string` | `string` | `string` | 短文本 |
| `text` | `string` | `string` | 长文本 |
| `integer` | `int` | `number` | 整数 |
| `number` | `float64` | `number` | 小数 |
| `boolean` | `bool` | `boolean` | 布尔值 |
| `enum` | `string` | `string` (union) | 枚举值 |
| `json` | `map[string]any` | `object` | JSON 对象 |
| `media` | `string` | `string` | 媒体文件 |
| `richText` | `string` | `string` | 富文本 |
| `datetime` | `time.Time` | `string` | 日期时间 |
| `password` | `string` | `string` | 密码（加密） |
| `uid` | `string` | `string` | 唯一标识 |
| `version` | `int` | `number` | 版本号 |
| `array` | `[]any` | `any[]` | 数组 |
| `object` | `map[string]any` | `object` | 对象 |

### 3.3 字段标签 (label)

**新增字段：`label`** - 用于定义字段在 UI 中显示的标签文本

```json
{
  "properties": {
    "username": {
      "type": "string",
      "label": "用户名",  // 简单字符串
      "validate": { "required": true }
    },
    "status": {
      "type": "enum",
      "label": {          // 多语言支持
        "zh-CN": "状态",
        "en-US": "Status"
      },
      "validate": {
        "required": true,
        "enum": ["active", "inactive"]
      }
    }
  }
}
```

**使用场景：**
- 表单字段的显示标签
- 表格列标题
- 验证错误消息中的字段名
- API 文档中的字段描述

**默认值规则：**
- 如果未提供 `label`，使用 `description` 作为备选
- 如果 `description` 也未提供，使用字段名（key）作为标签

### 3.4 数组和对象字段

#### 数组字段
```json
{
  "properties": {
    "tags": {
      "type": "array",
      "label": "标签",
      "items": {
        "type": "string"
      },
      "ui": {
        "widget": "tag-input"
      }
    },
    "images": {
      "type": "array",
      "label": "图片列表",
      "items": {
        "type": "media",
        "allowedTypes": ["image"]
      },
      "ui": {
        "widget": "image",
        "multiple": true
      }
    }
  }
}
```

#### 对象字段
```json
{
  "properties": {
    "address": {
      "type": "object",
      "label": "地址",
      "properties": {
        "province": {
          "type": "string",
          "label": "省份"
        },
        "city": {
          "type": "string",
          "label": "城市"
        },
        "detail": {
          "type": "string",
          "label": "详细地址"
        }
      }
    }
  }
}
```

---

## 4. 验证规则说明

`validate` 字段支持以下规则：

| 规则 | 类型 | 说明 | Ent 映射 | Zod 映射 |
|------|------|------|----------|----------|
| `required` | boolean | 必填 | `.NotEmpty()` | `.nonempty()` |
| `nullable` | boolean | 可为 null | `.Nillable()` | `.nullable()` |
| `min` | number | 最小值（仅数字） | `.Min()` | `.min()` / `.gte()` |
| `max` | number | 最大值（仅数字） | `.Max()` | `.max()` / `.lte()` |
| `minLength` | integer | 最小长度（字符串/数组） | `.MinLen()` | `.min()` |
| `maxLength` | integer | 最大长度（字符串/数组） | `.MaxLen()` | `.max()` |
| `pattern` | string | 正则 | `.Match(regexp)` | `.regex()` |
| `format` | string | 预定义格式 | 自定义 Validator | `.email()` 等 |
| `positive` | boolean | 正数 | `.Positive()` | `.positive()` |
| `negative` | boolean | 负数 | `.Negative()` | `.negative()` |
| `nonNegative` | boolean | 非负 | `.NonNegative()` | `.nonnegative()` |
| `integer` | boolean | 整数 | Integer 类型 | `.int()` |
| `enum` | array | 枚举值 | `.Enum()` | `.enum()` |
| `custom` | array | 自定义 | 自定义代码 | 自定义代码 |
| `errorMessage` | string | 错误消息 | - | `.refine()` |

**format 支持的预定义格式：**
- `email` - 邮箱格式
- `url` - URL 格式
- `uuid` - UUID 格式
- `phone` - 手机号格式
- `datetime` - 日期时间格式
- `date` - 日期格式
- `time` - 时间格式

---

## 5. UI 配置说明

### 5.1 根级 UI 配置 (RootUI)

```json
{
  "ui": {
    "submitText": "提交用户",     // 提交按钮文本
    "resetText": "重置",          // 重置按钮文本
    "showReset": true,           // 是否显示重置按钮
    "layout": {
      "direction": "vertical",   // 布局方向：vertical/horizontal
      "gap": 16,                 // 间距
      "columns": 2               // 栅格列数（24等分）
    }
  }
}
```

### 5.2 字段级 UI 配置 (Property UI)

```json
{
  "properties": {
    "email": {
      "type": "string",
      "label": "邮箱地址",
      "ui": {
        "widget": "email",           // 组件类型
        "placeholder": "请输入邮箱",   // 占位符
        "showInList": true,          // 在列表中显示
        "showInForm": true,          // 在表单中显示
        "span": 12,                  // 栅格占用（24等分）
        "readOnly": false,           // 只读
        "disabled": false,           // 禁用
        "size": "md",                // 组件大小：sm/md/lg
        "className": "custom-class", // 自定义 CSS 类
        "style": {                   // 内联样式
          "color": "red"
        },
        "icon": "Mail",              // 图标
        "prefix": "邮箱：",           // 前缀文本
        "suffix": "@example.com",    // 后缀文本
        "step": 1,                   // 步长（数字）
        "precision": 2,              // 小数精度
        "rows": 4,                   // Textarea 行数
        "hidden": false,             // 是否隐藏
        "options": [                 // 选项列表（select/radio/checkbox）
          { "value": "admin", "label": "管理员" },
          { "value": "editor", "label": "编辑" }
        ],
        "multiple": false            // 多选
      }
    }
  }
}
```

**常用 widget 类型：**
- `text`, `textarea`, `password`, `email`
- `number`, `decimal`
- `select`, `radio`, `checkbox`, `switch`
- `date`, `datetime`
- `file`, `image`, `video`, `audio`
- `tag-input` - 标签输入
- `custom` - 自定义组件

---

## 6. 关系配置详解

### 6.1 $ref 字段（核心概念）

**核心概念：使用 `$ref` 替代 `type: "uid"` + `target` 模式**

#### 旧模式（已废弃）
```json
{
  "properties": {
    "authorId": {
      "type": "uid",
      "label": "作者ID",
      "x-relation": {
        "type": "many2One",
        "target": "User",  // 重复指定目标
        "labelField": "username"
      }
    }
  }
}
```

**问题：**
- 字段名是 `authorId`，但实际需要的是 `author` 对象
- 需要同时指定 `type: "uid"` 和 `target: "User"`，信息重复
- 不够直观，不符合自然语义

#### 新模式（推荐）
```json
{
  "properties": {
    "author": {
      "$ref": "User",  // 直接引用目标实体
      "label": "作者",
      "x-relation": {
        "type": "many2One",
        "labelField": "username"
      }
    }
  }
}
```

**优势：**
- **语义清晰**：字段名 `author` 直接表达业务含义
- **信息精简**：`$ref` 同时指明类型和目标，无需重复
- **代码简洁**：减少冗余字段

### 6.2 关系类型 (Relation Type)

| 类型 | 说明 | 示例 | 字段值类型 |
|------|------|------|------------|
| `one2One` | 一对一 | 用户 ↔ 个人资料 | 单个对象 |
| `many2One` | 多对一 | 文章 ↔ 作者 | 单个对象 |
| `one2Many` | 一对多 | 用户 ↔ 文章列表 | 数组 |
| `many2Many` | 多对多 | 用户 ↔ 角色列表 | 数组 |

### 6.3 关系配置字段 (x-relation)

```json
{
  "properties": {
    "author": {
      "$ref": "User",
      "label": "作者",
      "x-relation": {
        "type": "many2One",           // 关系类型
        "inversedBy": "articles",     // 反向字段（双向关系）
        "mapBy": "mappingField",      // 映射字段（中间表）
        "labelField": "nickname",     // 显示字段（UI）
        "preload": true,              // 是否预加载
        "writable": true,             // 是否可写
        "queryable": true,            // 是否可查询
        "onDelete": "cascade"         // 删除动作
      }
    }
  }
}
```

**onDelete 支持的动作：**
- `cascade` - 级联删除
- `setNull` - 设置为 null
- `restrict` - 禁止删除（有依赖时）
- `noAction` - 无动作
- `setDefault` - 设置为默认值

### 6.4 使用规则

**重要规则：使用 `$ref` 时，不需要 `type` 字段**
- `$ref` 本身已经表明这是一个关系字段
- 前端通过 `x-relation.type` 判断是单个还是数组关系
  - `one2One`, `many2One` → 单个对象
  - `one2Many`, `many2Many` → 数组
- 不需要显式声明 `type: "array"` 或 `type: "uid"`

**示例：**
```json
{
  "properties": {
    // 单个关系
    "category": {
      "$ref": "Category",
      "label": "分类",
      "x-relation": {
        "type": "many2One",
        "labelField": "name"
      }
    },

    // 数组关系
    "roles": {
      "$ref": "Role",
      "label": "角色",
      "x-relation": {
        "type": "many2Many",
        "labelField": "name"
      }
    }
  }
}
```

### 6.5 labelField 优先级

**labelField 用于关系中显示的字段名：**

1. `labelField` 字段（如果存在）
2. 目标实体的 `label` 或 `description`
3. 目标实体的主键字段

**使用场景：**
- 下拉选择框中显示的文本
- 关系列表中的显示值
- 外键关联的友好显示

---

## 7. 模块目录结构

### 7.1 完整模块示例

```
cms/api/v1/user/
├── schema.json              # Schema 定义（单一数据源）
├── module.go                # 模块注册
├── controller.go            # HTTP 处理器
├── service.go               # 业务逻辑
├── dto.go                   # 数据传输对象
└── schema_gen.go            # ⚠️ 自动生成（可选）
```

### 7.2 Schema 优先开发流程

```go
// 1. 先定义 schema.json（数据驱动 - 唯一数据源）
// 2. 后端实现 Service（使用 Schema 验证）
// 3. 后端实现 Controller（基于 Schema 定义字段）
// 4. 前端通过 Schema API 获取定义
// 5. 前端基于 Schema 开发表格和表单
```

**开发顺序：Schema → 后端 → 前端**

---

## 8. Schema API 接口

### 8.1 核心接口设计

#### 8.1.1 获取所有模块的 Schema 列表

```go
// GET /api/schemas
// 返回所有可用模块的 Schema 摘要

// 响应
{
  "data": [
    {
      "name": "user",
      "displayName": "用户管理",
      "version": 1,
      "schemaUrl": "/api/schemas/user",
      "updatedAt": "2024-01-12T10:00:00Z"
    }
  ],
  "meta": {}
}
```

#### 8.1.2 获取单个模块的完整 Schema

```go
// GET /api/schemas/:moduleName
// 返回完整 Schema 定义

// 响应
{
  "data": {
    "name": "User",
    "collectionName": "users",
    "description": "用户实体",
    "info": { ... },
    "ui": { ... },
    "properties": { ... },
    "indexes": [...],
    "features": { ... }
  },
  "meta": { "version": 1, "updatedAt": "..." }
}
```

#### 8.1.3 批量获取多个 Schema

```go
// GET /api/schemas/batch?modules=user,article,product
// 响应: { "data": { "user": { ... }, "article": { ... } } }
```

#### 8.1.4 Schema 验证接口

```go
// POST /api/schemas/:moduleName/validate
// 请求: { "data": { "email": "invalid", "age": 200 } }
// 响应: { "valid": false, "errors": [{ "field": "email", "message": "..." }] }
```

---

## 9. 后端开发规范

### 9.1 开发原则

**必须先写 Schema，再写后端代码**

1. **Schema 优先**：所有业务模块必须先定义 `schema.json`
2. **字段一致性**：后端 DTO、Service、Controller 必须与 Schema 字段保持一致
3. **验证统一**：后端验证逻辑必须基于 Schema 的 `validate` 规则
4. **响应规范**：API 响应字段必须包含 Schema 定义的所有字段

### 9.2 后端开发流程

```go
// 步骤 1: 定义 Schema (cms/api/v1/user/schema.json)
{
  "name": "User",
  "properties": {
    "email": { "type": "string", "validate": { "required": true, "format": "email" } },
    "name": { "type": "string", "validate": { "required": true, "maxLength": 50 } }
  }
}

// 步骤 2: 定义 DTO (cms/api/v1/user/dto.go)
package user

import "github.com/go-playground/validator/v10"

type CreateDTO struct {
    Email string `json:"email" validate:"required,email,max=100"`
    Name  string `json:"name" validate:"required,max=50"`
    Age   int    `json:"age" validate:"min=0,max=150"`
    Role  string `json:"role" validate:"required,oneof=admin editor viewer"`
}

// 步骤 3: 绑定并验证 (在 Controller 中)
// 使用封装好的 binding 工具，自动根据 Schema 验证

// 步骤 4: 实现 Service (cms/api/v1/user/service.go)
func (s *Service) Create(ctx context.Context, dto *CreateDTO) (*_gen.User, error) {
    // Service 只处理业务逻辑，不负责验证
    // 验证已在 binding 层完成

    // 密码加密
    hashedPassword, err := bcrypt.GenerateFromPassword([]byte(dto.Password), bcrypt.DefaultCost)
    if err != nil {
        return nil, err
    }

    return s.client.User.Create().
        SetEmail(dto.Email).
        SetPassword(string(hashedPassword)).
        SetName(dto.Name).
        SetAge(dto.Age).
        SetRole(user.Role(dto.Role)).
        Save(ctx)
}

// 步骤 5: 实现 Controller (cms/api/v1/user/controller.go)
func (c *Controller) Create(w http.ResponseWriter, r *http.Request) {
    res := c.responderFactory.FromRequest(w, r)

    var dto CreateDTO
    if err := binding.JSON(r, &dto); err != nil {
        res.WriteError(http.StatusBadRequest, responder.Error{Message: err.Error()})
        return
    }

    user, err := c.service.Create(r.Context(), &dto)
    if err != nil {
        res.WriteError(http.StatusInternalServerError, responder.Error{Message: err.Error()})
        return
    }

    // 响应必须包含 Schema 定义的字段
    res.Write(http.StatusOK, responder.StrapiResponse{
        Data: map[string]any{
            "email": user.Email,
            "name":  user.Name,
            "age":   user.Age,
            "role":  user.Role,
        },
    })
}
```

### 9.3 后端开发检查清单

在开发后端接口时，必须确认：

- [ ] `schema.json` 已定义且格式正确
- [ ] **关系字段使用 `$ref` 而非 `type: "uid"` + `target`**
- [ ] 字段包含 `label` 用于 UI 显示
- [ ] 包含 `ui` 配置定义表单/页面行为
- [ ] DTO 结构体字段与 Schema `properties` 一一对应
- [ ] DTO 字段标签包含 `validate` 标签（基于 Schema 的 validate 规则）
- [ ] Controller 使用封装的 binding 工具自动验证
- [ ] Service 只处理业务逻辑，不负责验证
- [ ] Controller 响应包含 Schema 定义的所有字段
- [ ] API 路径与模块名称一致
- [ ] 错误消息清晰且与验证规则对应

### 9.4 验证层设计

**分层验证原则**：

```
┌─────────────────────────────────────┐
│  Controller (HTTP 层)                │
│  - binding.JSON 自动验证             │
│  - 验证失败直接返回 400              │
└─────────────────────────────────────┘
           ↓ 数据合法
┌─────────────────────────────────────┐
│  Service (业务逻辑层)                │
│  - 处理业务逻辑                      │
│  - 数据库操作                        │
│  - 不负责验证                        │
└─────────────────────────────────────┘
```

---

## 10. 前端集成方案

### 10.1 前端开发原则

**基于 Schema API 开发，不硬编码字段定义**

- 表格列定义：从 Schema 获取字段名、描述、类型
- 表单字段：从 Schema 获取字段名、验证规则、占位符
- 筛选条件：从 Schema 获取字段类型和验证规则
- 表单验证：使用 Schema 的 `validate` 规则

### 10.2 前端 API 客���端

```typescript
// frontend/lib/api/schema.ts
import { z } from 'zod';

const schemaCache = new Map<string, any>();

// 获取 Schema 列表
export async function getSchemaList() {
  const response = await fetch('/api/schemas');
  const { data } = await response.json();
  return data;
}

// 获取单个 Schema
export async function getSchema(name: string) {
  if (schemaCache.has(name)) {
    return schemaCache.get(name);
  }
  const response = await fetch(`/api/schemas/${name}`);
  const { data } = await response.json();
  schemaCache.set(name, data);
  return data;
}

// 批量获取 Schema
export async function getBatchSchemas(modules: string[]) {
  const response = await fetch('/api/schemas/batch', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ modules }),
  });
  const { data } = await response.json();
  return data;
}

// 验证数据
export async function validateData(moduleName: string, data: any) {
  const response = await fetch(`/api/schemas/${moduleName}/validate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ data }),
  });
  const { data: result } = await response.json();
  return result;
}

// 生成表单验证器
export async function getZodSchema(moduleName: string) {
  const schema = await getSchema(moduleName);
  const zodFields: Record<string, any> = {};

  for (const [fieldName, fieldDef] of Object.entries(schema.properties)) {
    const field = fieldDef as any;
    let zodType: any;

    // 基础类型映射
    switch (field.type) {
      case 'string':
      case 'text':
      case 'password':
        zodType = z.string();
        break;
      case 'integer':
      case 'number':
        zodType = z.number();
        break;
      case 'boolean':
        zodType = z.boolean();
        break;
      default:
        zodType = z.any();
    }

    // 应用验证规则
    const validate = field.validate;
    if (validate) {
      if (validate.required) {
        zodType = zodType.nonempty();
      }
      if (validate.min !== undefined) {
        zodType = zodType.min(validate.min);
      }
      if (validate.max !== undefined) {
        zodType = zodType.max(validate.max);
      }
      if (validate.format === 'email') {
        zodType = zodType.email();
      }
      if (validate.format === 'url') {
        zodType = zodType.url();
      }
    }

    if (!validate?.required) {
      zodType = zodType.optional();
    }

    zodFields[fieldName] = zodType;
  }

  return z.object(zodFields);
}
```

### 10.3 基于 Schema 的表格开发

```typescript
// frontend/components/UserTable.tsx
import { useEffect, useState } from 'react';
import { getSchema } from '@/lib/api/schema';

export function UserTable() {
  const [columns, setColumns] = useState<any[]>([]);
  const [data, setData] = useState<any[]>([]);

  useEffect(() => {
    loadSchemaAndData();
  }, []);

  const loadSchemaAndData = async () => {
    const schema = await getSchema('user');

    const tableColumns = Object.entries(schema.properties).map(([key, prop]: [string, any]) => ({
      key: key,
      title: prop.label || prop.description || key,  // 优先使用 label
      dataIndex: key,
      render: (value: any) => {
        if (prop.type === 'password') return '••••••';
        return value;
      },
      // 根据 showInList 过滤
      showInList: prop.ui?.showInList !== false,
    })).filter(col => col.showInList);

    setColumns(tableColumns);

    const response = await fetch('/api/users');
    const { data } = await response.json();
    setData(data);
  };

  return (
    <table>
      <thead>
        <tr>
          {columns.map(col => (
            <th key={col.key}>{col.title}</th>
          ))}
        </tr>
      </thead>
      <tbody>
        {data.map((row, idx) => (
          <tr key={idx}>
            {columns.map(col => (
              <td key={col.key}>{col.render ? col.render(row[col.key]) : row[col.key]}</td>
            ))}
          </tr>
        ))}
      </tbody>
    </table>
  );
}
```

### 10.4 基于 Schema 的表单开发

```typescript
// frontend/hooks/useSchemaForm.ts
import { useEffect, useState } from 'react';
import { useForm, UseFormReturn } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { getZodSchema, getSchema, validateData } from '@/lib/api/schema';

export function useSchemaForm<T extends Record<string, any>>(
  moduleName: string
): {
  form: UseFormReturn<T>;
  schema: any;
  fields: any[];
  loading: boolean;
  validate: (data: T) => Promise<boolean>;
} {
  const [schema, setSchema] = useState<any>(null);
  const [fields, setFields] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  const form = useForm<T>({
    resolver: async (data, context, options) => {
      if (!schema) {
        return { values: data, errors: {} };
      }
      const zodSchema = await getZodSchema(moduleName);
      return zodResolver(zodSchema)(data, context, options);
    },
  });

  useEffect(() => {
    loadSchema();
  }, [moduleName]);

  const loadSchema = async () => {
    setLoading(true);
    try {
      const loadedSchema = await getSchema(moduleName);
      setSchema(loadedSchema);

      // 从 Schema 生成表单字段配置
      const formFields = Object.entries(loadedSchema.properties).map(([key, prop]: [string, any]) => ({
        name: key,
        label: prop.label || prop.description || key,  // 优先使用 label
        type: prop.type,
        required: prop.validate?.required || false,
        placeholder: prop.ui?.placeholder || prop.label || prop.description || key,
        validate: prop.validate,
        ui: prop.ui,
      }));

      setFields(formFields);
    } catch (error) {
      console.error('Failed to load schema:', error);
    } finally {
      setLoading(false);
    }
  };

  const validate = async (data: T): Promise<boolean> => {
    const result = await validateData(moduleName, data);
    if (!result.valid) {
      result.errors.forEach((error: any) => {
        form.setError(error.field as any, {
          message: error.message,
        });
      });
      return false;
    }
    return true;
  };

  return { form, schema, fields, loading, validate };
}

// 使用示例：动态表单
export function DynamicForm({ moduleName }: { moduleName: string }) {
  const { form, fields, loading, validate } = useSchemaForm(moduleName);

  if (loading) return <div>Loading...</div>;

  const onSubmit = async (data: any) => {
    const isValid = await validate(data);
    if (!isValid) return;

    await fetch(`/api/${moduleName}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
  };

  return (
    <form onSubmit={form.handleSubmit(onSubmit)}>
      {fields.map(field => (
        <div key={field.name} style={{ marginBottom: 16 }}>
          <label>
            {field.label}
            {field.required && ' *'}
          </label>

          {field.type === 'enum' ? (
            <select {...form.register(field.name)}>
              {field.validate?.enum?.map((opt: string) => (
                <option key={opt} value={opt}>{opt}</option>
              ))}
            </select>
          ) : field.type === 'boolean' ? (
            <input type="checkbox" {...form.register(field.name)} />
          ) : field.type === 'integer' || field.type === 'number' ? (
            <input
              type="number"
              {...form.register(field.name, { valueAsNumber: true })}
              placeholder={field.placeholder}
            />
          ) : field.type === 'password' ? (
            <input
              type="password"
              {...form.register(field.name)}
              placeholder={field.placeholder}
            />
          ) : (
            <input
              type="text"
              {...form.register(field.name)}
              placeholder={field.placeholder}
            />
          )}

          {form.formState.errors[field.name] && (
            <div style={{ color: 'red' }}>
              {form.formState.errors[field.name]?.message}
            </div>
          )}
        </div>
      ))}

      <button type="submit">提交</button>
    </form>
  );
}
```

### 10.5 前端开发检查清单

在开发前端功能时，必须确认：

- [ ] 通过 Schema API 获取字段定义，不硬编码
- [ ] 表格列基于 Schema properties 生成
- [ ] 表单字段基于 Schema properties 生成
- [ ] 表单验证使用 Schema 的 validate 规则
- [ ] 字段标签优先使用 Schema 的 `label`，其次 `description`，最后字段名
- [ ] 根据 Schema 的 type 选择合适的输入组件
- [ ] 处理 Schema 中的枚举值
- [ ] 根据 `ui.showInList` 过滤表格列
- [ ] 根据 `ui.showInForm` 过滤表单字段

---

## 11. 工作流程

### 11.1 开发流程图

```
1. 定义 Schema (schema.json)
   ↓
2. 提交到版本控制
   ↓
3. 后端开发
   ├─ 实现 DTO
   ├─ 实现 Service (基于 Schema 验证)
   └─ 实现 Controller (基于 Schema 响应)
   ↓
4. 启动后端服务
   ↓
5. 前端调用 Schema API
   ↓
6. 前端开发表格 (基于 Schema 列定义)
   ↓
7. 前端开发表单 (基于 Schema 字段和验证)
   ↓
8. 测试前后端集成
```

### 11.2 更新流程

```
1. 修改 schema.json
   ↓
2. 后端更新验证逻辑（如果需要）
   ↓
3. 后端更新 DTO 和 Controller
   ↓
4. 前端重新获取 Schema
   ↓
5. 前端表格/表单自动适配
   ↓
6. 编译期发现不兼容问题
   ↓
7. 修复问题并提交
```

---

## 12. 完整示例

### 12.1 完整的用户模块示例

#### Schema 文件 (`cms/api/v1/user/schema.json`)

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "name": "User",
  "collectionName": "users",
  "description": "系统用户",
  "softDelete": true,
  "info": {
    "displayName": "用户管理",
    "description": "管理系统的用户账户",
    "icon": "User",
    "locale": "zh-CN"
  },
  "ui": {
    "submitText": "创建用户",
    "resetText": "重置",
    "showReset": true,
    "layout": {
      "direction": "vertical",
      "gap": 16,
      "columns": 2
    }
  },
  "properties": {
    "email": {
      "type": "string",
      "label": "邮箱地址",
      "description": "用户登录邮箱",
      "validate": {
        "required": true,
        "format": "email",
        "maxLength": 100
      },
      "unique": true,
      "ui": {
        "widget": "email",
        "placeholder": "user@example.com",
        "showInList": true,
        "showInForm": true,
        "span": 12
      }
    },
    "password": {
      "type": "password",
      "label": "登录密码",
      "description": "密码（加密存储）",
      "validate": {
        "required": true,
        "minLength": 8
      },
      "private": true,
      "ui": {
        "widget": "password",
        "writeOnly": true,
        "showInList": false,
        "showInForm": true
      }
    },
    "name": {
      "type": "string",
      "label": "用户姓名",
      "validate": {
        "required": true,
        "maxLength": 50
      },
      "ui": {
        "widget": "text",
        "placeholder": "请输入姓名",
        "showInList": true,
        "showInForm": true,
        "span": 12
      }
    },
    "age": {
      "type": "integer",
      "label": "年龄",
      "validate": {
        "min": 0,
        "max": 150,
        "nonNegative": true
      },
      "ui": {
        "widget": "number",
        "showInList": true,
        "showInForm": true,
        "span": 6
      }
    },
    "role": {
      "type": "enum",
      "label": "用户角色",
      "description": "系统权限角色",
      "validate": {
        "required": true,
        "enum": ["admin", "editor", "viewer"]
      },
      "ui": {
        "widget": "select",
        "options": [
          { "value": "admin", "label": "管理员" },
          { "value": "editor", "label": "编辑" },
          { "value": "viewer", "label": "查看者" }
        ],
        "showInList": true,
        "showInForm": true,
        "span": 6
      }
    },
    "phone": {
      "type": "string",
      "label": "手机号",
      "validate": {
        "format": "phone",
        "pattern": "^[0-9]+$"
      },
      "ui": {
        "widget": "text",
        "placeholder": "13800138000",
        "showInList": false,
        "showInForm": true,
        "span": 12
      }
    },
    "posts": {
      "$ref": "Post",
      "label": "文章列表",
      "x-relation": {
        "type": "one2Many",
        "inversedBy": "author",
        "labelField": "title",
        "preload": false,
        "writable": false,
        "queryable": true
      },
      "ui": {
        "showInList": false,
        "showInForm": false
      }
    },
    "roles": {
      "$ref": "Role",
      "label": "角色",
      "x-relation": {
        "type": "many2Many",
        "inversedBy": "users",
        "labelField": "name",
        "preload": true,
        "writable": true,
        "queryable": true
      },
      "ui": {
        "widget": "select",
        "multiple": true,
        "showInList": false,
        "showInForm": true
      }
    }
  },
  "indexes": [
    {
      "type": "unique",
      "name": "idx_email",
      "columns": ["email"]
    }
  ],
  "features": {
    "softDelete": true,
    "export": true,
    "import": true,
    "batch": true
  }
}
```

#### 后端 Service (`cms/api/v1/user/service.go`)

```go
package user

import (
    "context"
    "github.com/JsonLee12138/headless-cms/cms/_gen"
    "github.com/JsonLee12138/headless-cms/cms/_gen/user"
    "golang.org/x/crypto/bcrypt"
)

type Service struct {
    client *_gen.Client
}

func NewService(client *_gen.Client) *Service {
    return &Service{client: client}
}

func (s *Service) Create(ctx context.Context, dto *CreateDTO) (*_gen.User, error) {
    // 密码加密
    hashedPassword, err := bcrypt.GenerateFromPassword([]byte(dto.Password), bcrypt.DefaultCost)
    if err != nil {
        return nil, err
    }

    return s.client.User.Create().
        SetEmail(dto.Email).
        SetPassword(string(hashedPassword)).
        SetName(dto.Name).
        SetAge(dto.Age).
        SetRole(user.Role(dto.Role)).
        SetPhone(dto.Phone).
        Save(ctx)
}

func (s *Service) Update(ctx context.Context, id string, dto *UpdateDTO) (*_gen.User, error) {
    builder := s.client.User.UpdateOneID(id)

    if dto.Name != "" {
        builder.SetName(dto.Name)
    }
    if dto.Age != 0 {
        builder.SetAge(dto.Age)
    }
    if dto.Role != "" {
        builder.SetRole(user.Role(dto.Role))
    }

    return builder.Save(ctx)
}
```

#### 前端使用示例

```typescript
// frontend/pages/users/create.tsx
import { useSchemaForm } from '@/hooks/useSchemaForm';
import { CreateUserDTO } from '@/types/user';

export default function CreateUser() {
  const { form, loading, validate } = useSchemaForm<CreateUserDTO>('user');

  if (loading) return <div>Loading...</div>;

  const onSubmit = async (data: CreateUserDTO) => {
    const isValid = await validate(data);
    if (!isValid) return;

    await fetch('/api/users', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
  };

  return (
    <form onSubmit={form.handleSubmit(onSubmit)}>
      <div>
        <label>邮箱地址 *</label>
        <input {...form.register('email')} placeholder="user@example.com" />
        {form.formState.errors.email && <span>{form.formState.errors.email.message}</span>}
      </div>

      <div>
        <label>登录密码 *</label>
        <input type="password" {...form.register('password')} placeholder="••••••••" />
        {form.formState.errors.password && <span>{form.formState.errors.password.message}</span>}
      </div>

      <div>
        <label>用户姓名 *</label>
        <input {...form.register('name')} placeholder="请输入姓名" />
        {form.formState.errors.name && <span>{form.formState.errors.name.message}</span>}
      </div>

      <div>
        <label>年龄</label>
        <input type="number" {...form.register('age', { valueAsNumber: true })} placeholder="0-150" />
        {form.formState.errors.age && <span>{form.formState.errors.age.message}</span>}
      </div>

      <div>
        <label>用户角色 *</label>
        <select {...form.register('role')}>
          <option value="admin">管理员</option>
          <option value="editor">编辑</option>
          <option value="viewer">查看者</option>
        </select>
        {form.formState.errors.role && <span>{form.formState.errors.role.message}</span>}
      </div>

      <div>
        <label>手机号</label>
        <input {...form.register('phone')} placeholder="13800138000" />
        {form.formState.errors.phone && <span>{form.formState.errors.phone.message}</span>}
      </div>

      <button type="submit">创建用户</button>
    </form>
  );
}
```

---

## 13. 默认值规则汇总

### 13.1 UI 配置默认值

#### 根级 UI (RootUI)
| 字段 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `submitText` | string/object | `"提交"` | 提交按钮文本 |
| `resetText` | string/object | `"重置"` | 重置按钮文本 |
| `showReset` | boolean | `false` | 是否显示重置按钮 |
| `layout.direction` | string | `"vertical"` | 布局方向 |
| `layout.gap` | number | `16` | 间距 |
| `layout.columns` | number | `1` | 栅格列数 |

#### 字段级 UI (Property UI)
| 字段 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `showInList` | boolean | `true` | 在列表中显示 |
| `showInForm` | boolean | `true` | 在表单中显示 |
| `span` | number | `24` | 栅格占用（24等分） |
| `readOnly` | boolean | `false` | 只读 |
| `disabled` | boolean | `false` | 禁用 |

### 13.2 标签显示优先级

**字段标签 (label) 优先级：**
1. `label` 字段（如果存在）
2. `description` 字段（如果存在）
3. 字段名（key）作为最后备选

**示例：**
```json
{
  "properties": {
    "email": {
      "type": "string",
      "label": "邮箱地址",        // 优先级 1
      "description": "用户邮箱",   // 优先级 2
      // 如果都没有，显示 "email"   // 优先级 3
    }
  }
}
```

### 13.3 占位符优先级

**placeholder 优先级：**
1. `ui.placeholder` 字段（如果存在）
2. `label` 字段（如果存在）
3. `description` 字段（如果存在）
4. 字段名（key）作为最后备选

---

## 14. 检查清单

在开发每个模块时，请确认：

### Schema 定义
- [ ] 模块目录下存在 `schema.json` 文件
- [ ] Schema 遵循 `entity_schema.json` 的定义规范
- [ ] **关系字段使用 `$ref` 而非 `type: "uid"` + `target`**
- [ ] 字段包含 `label` 用于 UI 显示
- [ ] 包含 `ui` 配置定义表单/页面行为
- [ ] Schema 包含 `validate` 字段定义验证规则
- [ ] Schema 包含 `indexes` 定义索引
- [ ] Schema 包含 `features` 定义功能开关

### 后端开发
- [ ] 后端 Service 使用 Schema 定义的验证规则
- [ ] 后端 Controller 响应包含 Schema 定义的所有字段
- [ ] DTO 结构体字段与 Schema `properties` 一一对应
- [ ] DTO 字段标签包含 `validate` 标签
- [ ] Controller 使用封装的 binding 工具自动验证
- [ ] Service 只处理业务逻辑，不负责验证
- [ ] 密码字段使用 bcrypt 加密
- [ ] 关系字段正确处理（使用 `$ref`）

### 前端开发
- [ ] Schema API 接口可正常访问
- [ ] 前端通过 Schema API 获取定义，不硬编码字段
- [ ] 表格列基于 Schema 生成，优先使用 `label`
- [ ] 表单字段基于 Schema 生成，优先使用 `label`
- [ ] 表单验证使用 Schema 的 `validate` 规则
- [ ] 根据 `ui.showInList` 过滤表格列
- [ ] 根据 `ui.showInForm` 过滤表单字段
- [ ] 处理 Schema 中的枚举值
- [ ] 关系字段使用 `labelField` 显示友好文本

### 整体
- [ ] 修改 Schema 后前后端都能感知变化
- [ ] 所有字段标签使用优先级规则正确显示
- [ ] 所有占位符使用优先级规则正确显示

---

## 15. @schema/ 技能核心模式参考

本节总结了从 @schema/ 技能中提取的关键模式，这些模式已在 CMS 技能中集成。

### 15.1 关系字段模式

**推荐模式：使用 `$ref` (来自 @schema/backend-developer)**

```json
// ✅ 正确：使用 $ref
{
  "properties": {
    "author": {
      "$ref": "User",
      "label": "作者",
      "x-relation": {
        "type": "many2One",
        "labelField": "name"
      }
    }
  }
}

// ❌ 错误：旧模式
{
  "properties": {
    "authorId": {
      "type": "uid",
      "x-relation": {
        "type": "many2One",
        "target": "User"  // 重复指定
      }
    }
  }
}
```

**优势：**
- 语义清晰：字段名直接表达业务含义
- 信息精简：`$ref` 同时指明类型和目标
- 代码简洁：减少冗余字段

### 15.2 标签和占位符优先级

**标签优先级 (来自 @schema/table-developer & @schema/form-developer):**

```json
// 优先级顺序：label → description → 字段名
{
  "properties": {
    "email": {
      "type": "string",
      "label": "邮箱地址",        // ✅ 优先级 1
      "description": "用户邮箱",   // ✅ 优先级 2
      // 如果都没有，显示 "email"   // ✅ 优先级 3
    }
  }
}
```

**占位符优先级:**

```json
// 优先级顺序：ui.placeholder → label → description → 字段名
{
  "properties": {
    "email": {
      "type": "string",
      "label": "邮箱地址",
      "ui": {
        "placeholder": "user@example.com"  // 优先级 1
      }
      // 如果没有 placeholder，使用 label (优先级 2)
    }
  }
}
```

### 15.3 后端验证层 (来自 @schema/backend-developer)

**三层验证架构：**

```
┌─────────────────────────────────────┐
│  Controller (HTTP 层)                │
│  - binding.JSON 自动验证             │
│  - 验证失败直接返回 400              │
└─────────────────────────────────────┘
         ↓ 数据合法
┌─────────────────────────────────────┐
│  Service (业务逻辑层)                │
│  - 处理业务逻辑                      │
│  - 密码加密 (bcrypt)                 │
│  - 关系处理                          │
│  - 不负责基础验证                    │
└─────────────────────────────────────┘
         ↓
┌─────────────────────────────────────┐
│  Ent Schema (数据库层)               │
│  - 类型约束                          │
│  - 唯一索引                          │
│  - Not null                          │
└─────────────────────────────────────┘
```

**Go 代码示例：**

```go
// DTO (Controller 层验证)
type CreateDTO struct {
    Email    string `json:"email" validate:"required,email,max=100"`
    Password string `json:"password" validate:"required,min=6,max=72"`
}

// Service (业务逻辑)
func (s *Service) Create(ctx context.Context, dto *CreateDTO) (*_gen.User, error) {
    // 密码加密
    hashedPassword, _ := bcrypt.GenerateFromPassword([]byte(dto.Password), bcrypt.DefaultCost)

    return s.client.User.Create().
        SetEmail(dto.Email).
        SetPassword(string(hashedPassword)).
        Save(ctx)
}
```

### 15.4 前端动态生成 (来自 @schema/form-developer & @schema/table-developer)

**表单动态生成：**

```typescript
// 从 Schema 生成表单字段
const formFields = Object.entries(schema.properties).map(([key, prop]) => ({
  name: key,
  label: prop.label || prop.description || key,  // 优先级规则
  type: prop.type,
  required: prop.validate?.required || false,
  placeholder: prop.ui?.placeholder || prop.label || key,
  validate: prop.validate,
  ui: prop.ui,
}));
```

**表格动态生成：**

```typescript
// 从 Schema 生成表格列
const columns = Object.entries(schema.properties)
  .filter(([_, prop]) => prop.ui?.showInList !== false)
  .map(([key, prop]) => ({
    key: key,
    title: prop.label || prop.description || key,
    dataIndex: key,
    sortable: prop.ui?.sortable || false,
    filterable: prop.ui?.filterable || false,
  }));
```

### 15.5 代码质量检测 (来自 @schema/code-detector)

**Backend 检测要点：**
- ✅ DTO 验证标签完整性
- ✅ Service 密码哈希处理
- ✅ Controller 错误处理
- ✅ 关系字段正确配置

**Frontend 检测要点：**
- ✅ TypeScript 类型完整性
- ✅ Zod 验证 schema 匹配
- ✅ API 客户端方法完整
- ✅ 表单/表格字段覆盖

### 15.6 常见陷阱和解决方案

| 问题 | 错误做法 | 正确做法 |
|------|----------|----------|
| 关系字段 | `type: "uid"` + `target` | `$ref` + `x-relation` |
| 标签显示 | 使用 `description` | 使用 `label` |
| 可选字段 | 总是设置值 | 检查后再设置 |
| 密码存储 | 明文存储 | bcrypt 哈希 |
| 验证位置 | Service 中验证 | Controller 层验证 |

---

## 📚 相关文档

### 核心规范文件
- **`entity_schema.json`** (当前目录) - Schema 定义规范
  - 定义了所有可用的字段类型、验证规则、UI 配置
  - 所有 schema.json 必须遵循此定义

### 技能和工具
- **`../SKILL.md`** - Schema 驱动开发技能完整指南
  - 工作流程、代码生成、验证工具
  - **整合了 @schema/ 所有技能**
  - 设计器、验证器、代码生成器

- **`../rules.md`** - 技能使用规则
  - CMS 技能 vs @schema/ 技能的选择指南
  - 集成模式说明

### 参考文档
- **`../assets/validation-rules.md`** - 验证规则详细参考
  - 字段类型映射表
  - 验证规则 Ent/Zod 映射
  - **基于 @schema/RULES.md 更新**
  - 完整示例

### 模板和示例
- **`../assets/schema.template.json`** - Schema 模板文件
  - **包含 @schema/ 最新模式示例**
- **`../assets/example-user.json`** - 用户模块完整示例

### @schema/ 技能参考 (深入学习)
当需要特定技术栈的详细实现时，参考以下技能：

| 技能 | 路径 | 用途 |
|------|------|------|
| **backend-developer** | `../../schema/skills/backend-developer/SKILL.md` | Go 后端详细实现 |
| **table-developer** | `../../schema/skills/table-developer/SKILL.md` | React 表格组件 |
| **form-developer** | `../../schema/skills/form-developer/SKILL.md` | React 表单组件 |
| **code-detector** | `../../schema/skills/code-detector/SKILL.md` | 代码质量检测 |
| **核心规则** | `../../schema/RULES.md` | 完整 Schema 规范 |

### 其他
- [CMS 编码规范](./CMS_CODING_STANDARD.md) - 完整的编码规范
- [Schema Go 结构](../schema/schema.go) - Go 类型定义

---

**遵循 Schema 驱动开发，确保前后端数据同步！** 🚀
