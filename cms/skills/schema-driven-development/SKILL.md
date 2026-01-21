---
name: schema-driven-development
description: Complete schema-driven development toolkit - design, validate, and generate code from schema.json as single source of truth for Headless CMS
---

# Schema Driven Development Skill

Complete toolkit for schema-driven development workflow. Design schemas, validate them, and generate both backend (Go) and frontend (TypeScript/React) code automatically.

**This skill integrates all @schema/ skills:** `backend-developer`, `table-developer`, `form-developer`, and `code-detector` into a unified CMS-focused toolkit.

## 📋 Core Files

- **`references/entity_schema.json`** - Schema definition specification
  - Defines all available field types, validation rules, UI configurations
  - All schema.json files must follow this JSON Schema

- **`references/schema-development.md`** - Complete development guide
  - Detailed workflow and best practices
  - Backend/frontend integration patterns
  - **Based on @schema/RULES.md** - comprehensive schema specifications

- **`assets/validation-rules.md`** - Validation rules reference
  - Field type mappings
  - Ent/Zod validation mappings
  - **Updated with @schema/ skill patterns**

- **`assets/schema.template.json`** - Schema template
  - **Updated with latest features from @schema/ skills**

## 🎯 When to Use This Skill

### Primary Use Cases
- **Creating new modules** - Design schema first, then generate everything
- **Updating data models** - Modify schema, validate, regenerate code
- **Building dynamic UI** - Generate forms and tables from schema
- **API design** - Plan data structure before implementation
- **Code generation** - Auto-generate DTOs, services, controllers, types, API clients
- **Schema validation** - Verify schema correctness before development
- **Team collaboration** - Ensure前后端 data consistency

### Workflow Triggers
- "I need a new User module"
- "Add a new field to Product schema"
- "Validate my schema before coding"
- "Generate Go backend from schema"
- "Generate TypeScript frontend from schema"

## 📋 Core Principles

### 1. Schema as Single Source of Truth
```
Traditional Development:
Backend API → Frontend Manual Integration → Type Definitions
(Disjointed, error-prone, manual updates)

Schema-Driven Development:
Schema Definition → Auto-Generate Backend → Auto-Generate Frontend
(Synchronized, type-safe, zero duplication)
```

### 2. Development Order
```
1. Design Schema (Interactive or Manual)
   ↓
2. Validate Schema (Check for errors)
   ↓
3. Generate Backend Code (Go: DTO, Service, Controller, Module)
   ↓
4. Generate Frontend Code (TS: Types, API, Components)
   ↓
5. Customize & Test (Add business logic)
```

**Always: Design → Validate → Generate → Customize**

### 3. Three-Phase Approach

#### Phase 1: Design
- Interactive designer or manual schema creation
- Define entities, fields, relationships, validations, UI config

#### Phase 2: Validate
- Check schema against specification
- Verify types, relationships, rules
- Ensure consistency

#### Phase 3: Generate
- Backend: Go code (DTO, Service, Controller, Module)
- Frontend: TypeScript code (Types, API, Components)
- Ready to use with customization hooks

## 🛠️ Available Scripts

### 1. Schema Designer (Interactive)
**Location**: `scripts/designer/designer.py`

**Purpose**: Interactive tool for creating schemas through guided questions

**Usage**:
```bash
python scripts/designer/designer.py
```

**Features**:
- ✅ Interactive Q&A workflow
- ✅ Entity metadata (name, description, icon)
- ✅ Field design (types, labels, validation)
- ✅ Relationship design (one2One, many2One, one2Many, many2Many)
- ✅ Index design (unique, index, fulltext)
- ✅ UI configuration (widgets, layout, visibility)
- ✅ Features (soft delete, import/export)

**Example Flow**:
```
Entity name: User
Display name: 用户管理
Fields: email, password, name, age, role
Relationships: posts (one2Many), roles (many2Many)
Indexes: email (unique)
UI: Form layout, button texts
```

### 2. Schema Validator
**Location**: `scripts/validator/`

**Files**:
- `validate_schema.py` - Validate single schema
- `validate_all.py` - Validate all schemas in directory
- `quick_validate.py` - Quick validation with summary

**Usage**:
```bash
# Validate single
python scripts/validator/validate_schema.py schema.json

# Validate all
python scripts/validator/validate_all.py ./schemas/

# Quick validation
python scripts/validator/quick_validate.py ./schemas/
```

**Validation Checks**:
- ✅ JSON syntax
- ✅ Required fields (name, properties)
- ✅ Field types (string, integer, enum, etc.)
- ✅ Relationship fields ($ref, x-relation.type)
- ✅ Validation rules (min/max for values, minLength/maxLength for length, format, enum)
- ✅ UI configuration (widget types, layout)
- ✅ Indexes (type, columns)
- ✅ Features (boolean values)

**Output**:
```
✅ schema.json - Valid
❌ user.json - Errors:
   - Missing required field: name
   - Invalid type: 'str' for field 'email'
```

### 3. Code Generator (Go Backend)
**Location**: `scripts/generator/generate_go.py`

**Purpose**: Generate Go backend code from schema

**Usage**:
```bash
python scripts/generator/generate_go.py schema.json --output ./backend
```

**Generated Files**:
```
backend/user/
├── dto.go          # CreateDTO, UpdateDTO with validation tags
├── service.go      # CRUD operations, password hashing, relations
├── controller.go   # HTTP handlers, error handling
└── module.go       # Route registration
```

**Features**:
- ✅ Automatic validation tags (validate:"required,email,max=100")
- ✅ Password hashing (bcrypt)
- ✅ Relationship handling (Ent integration)
- ✅ Soft delete support
- ✅ Error handling
- ✅ Consistent response format

**Example Output**:
```go
// dto.go
type CreateDTO struct {
    Email    string `json:"email" validate:"required,email,max=100"`
    Password string `json:"password" validate:"required,min=8"`
    Name     string `json:"name" validate:"required,max=50"`
}

// service.go
func (s *Service) Create(ctx context.Context, dto *CreateDTO) (*_gen.User, error) {
    hashedPassword, _ := bcrypt.GenerateFromPassword([]byte(dto.Password), bcrypt.DefaultCost)
    return s.client.User.Create().
        SetEmail(dto.Email).
        SetPassword(string(hashedPassword)).
        SetName(dto.Name).
        Save(ctx)
}
```

### 4. Code Generator (TypeScript Frontend)
**Location**: `scripts/generator/generate_ts.py`

**Purpose**: Generate TypeScript/React frontend code from schema

**Usage**:
```bash
python scripts/generator/generate_ts.py schema.json --output ./frontend
```

**Generated Files**:
```
frontend/
├── types/user.ts           # Type definitions
├── lib/api/user.ts         # API client
├── components/UserForm.tsx # Form with Zod validation
└── components/UserTable.tsx # Table component
```

**Features**:
- ✅ Type-safe interfaces
- ✅ Zod validation schema
- ✅ React Hook Form integration
- ✅ API client with error handling
- ✅ Auto-generated form fields
- ✅ Table with columns from schema
- ✅ Relationship support

**Example Output**:
```typescript
// types/user.ts
export interface User {
  id: string;
  email: string;
  name: string;
  age: number;
  role: 'admin' | 'editor' | 'viewer';
}

// lib/api/user.ts
export class UserAPI {
  async create(dto: CreateUserDTO): Promise<User> {
    const response = await fetch('/api/users', {
      method: 'POST',
      body: JSON.stringify(dto),
    });
    return response.json();
  }
}

// components/UserForm.tsx
const schema = z.object({
  email: z.string().email().max(100),
  password: z.string().min(8),
  name: z.string().max(50),
});
```

## 📁 Complete Module Structure

### Standard Module Layout
```
cms/api/v1/user/
├── schema.json              # ✅ Single source of truth
│
├── backend/                 # Generated Go code
│   ├── dto.go              # Data transfer objects
│   ├── service.go          # Business logic
│   ├── controller.go       # HTTP handlers
│   └── module.go           # Route registration
│
├── frontend/                # Generated TypeScript code
│   ├── types/user.ts       # Type definitions
│   ├── lib/api/user.ts     # API client
│   ├── components/
│   │   ├── UserForm.tsx    # Form component
│   │   └── UserTable.tsx   # Table component
│
└── custom/                  # Your customizations
    ├── service.custom.go   # Business logic additions
    └── form.custom.tsx     # UI customizations
```

## 🎨 Schema File Format

### Complete Example
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
    "icon": "User"
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
      "validate": {
        "required": true,
        "format": "email",
        "maxLength": 100
      },
      "ui": {
        "widget": "email",
        "placeholder": "user@example.com",
        "showInList": true,
        "span": 12
      }
    },
    "password": {
      "type": "password",
      "label": "密码",
      "validate": {
        "required": true,
        "minLength": 8
      },
      "ui": {
        "widget": "password",
        "writeOnly": true
      }
    },
    "author": {
      "$ref": "Author",
      "label": "作者",
      "x-relation": {
        "type": "many2One",
        "labelField": "name",
        "preload": true
      }
    },
    "posts": {
      "$ref": "Post",
      "label": "文章",
      "x-relation": {
        "type": "one2Many",
        "labelField": "title"
      }
    }
  },

  "indexes": [
    {
      "type": "unique",
      "columns": ["email"]
    }
  ],

  "features": {
    "softDelete": true,
    "export": true,
    "import": false,
    "batch": true
  }
}
```

## 🔗 Related @schema/ Skills

This CMS skill integrates the following specialized skills from @schema/:

### 1. Backend Developer (`@schema/backend-developer`)
**Focus**: Go backend code generation
- DTO generation with validation tags
- Service layer with bcrypt password hashing
- Controller with HTTP endpoints
- Ent schema generation
- Relationship handling (many2One, one2Many, many2Many)

**Use when**: Generating Go backend code from schema

### 2. Table Developer (`@schema/table-developer`)
**Focus**: React table components
- Type definitions
- API client generation
- Table components with search/sort/pagination
- Dynamic column generation
- Export functionality

**Use when**: Building data tables from schema

### 3. Form Developer (`@schema/form-developer`)
**Focus**: React form components
- Zod validation schema generation
- React Hook Form integration
- Dynamic field rendering
- File upload handling
- Nested form support

**Use when**: Building forms from schema

### 4. Code Detector (`@schema/code-detector`)
**Focus**: Code quality validation
- Backend analysis (Go validation tags, password hashing, relations)
- Frontend analysis (TypeScript types, Zod schemas, API clients)
- Detect missing fields, type mismatches, validation errors
- Relationship handling verification

**Use when**: Validating generated code against schema

### Integration Pattern
```
CMS Skill (Unified Toolkit)
    ├── References @schema/backend-developer
    ├── References @schema/table-developer
    ├── References @schema/form-developer
    └── References @schema/code-detector
```

## 📚 Resources

### Reference Documents
- **Complete Guide**: `references/schema-development.md` (43KB)
  - Based on @schema/RULES.md with CMS-specific examples
- **Validation Rules**: `assets/validation-rules.md` (15KB)
  - Updated with @schema/ skill patterns

### Templates & Examples
- **Schema Template**: `assets/schema.template.json`
  - Latest structure with all @schema/ features
- **Example User**: `assets/example-user.json`

### Scripts Reference
- **Designer**: `scripts/designer/designer.py`
- **Validator**: `scripts/validator/validate_schema.py`
- **Go Generator**: `scripts/generator/generate_go.py`
- **TS Generator**: `scripts/generator/generate_ts.py`

### @schema/ Skill References
- **Backend Skills**: `../../schema/skills/backend-developer/SKILL.md`
- **Table Skills**: `../../schema/skills/table-developer/SKILL.md`
- **Form Skills**: `../../schema/skills/form-developer/SKILL.md`
- **Detection Skills**: `../../schema/skills/code-detector/SKILL.md`
- **Core Rules**: `../../schema/RULES.md`

## 🚀 Quick Start

### Complete Workflow Example

```bash
# 1. Design schema (interactive)
cd cms/skills/schema-driven-development
python scripts/designer/designer.py
# Output: user-schema.json

# 2. Validate schema
python scripts/validator/validate_schema.py user-schema.json
# Output: ✅ Schema is valid!

# 3. Generate backend
python scripts/generator/generate_go.py user-schema.json --output ./backend
# Output: Generated 4 files

# 4. Generate frontend
python scripts/generator/generate_ts.py user-schema.json --output ./frontend
# Output: Generated 4 files

# 5. Review and customize
# Add business logic to service.go
# Customize UI in form components
```

### Using Existing Schema
```bash
# Validate existing schema
python scripts/validator/validate_schema.py /path/to/schema.json

# Generate all code
python scripts/generator/generate_go.py schema.json --output ./backend
python scripts/generator/generate_ts.py schema.json --output ./frontend
```

## 🔧 Customization

### After Generation
1. **Backend**: Add business logic to `service.go`
2. **Frontend**: Customize UI in components
3. **Validation**: Add custom rules in `dto.go` or Zod schema
4. **Security**: Add auth checks in controller

### Best Practices
- ✅ Keep schema in version control
- ✅ Validate before committing
- ✅ Regenerate after schema changes
- ✅ Add custom logic in separate files
- ✅ Document business rules

## ⚡ Benefits

### Time Savings
- ⏱️ 80% less boilerplate code
- ⏱️ Instant CRUD operations
- ⏱️ Automatic validation
- ⏱️ Type-safe everywhere

### Quality
- ✅ Consistent patterns
- ✅ Zero type errors
- ✅ Secure by default
- ✅ Easy to maintain

### Collaboration
- 📄 Single source of truth
- 🔄 Automatic synchronization
- 🎯 Clear data contracts
- 📊 Self-documenting

---

**Schema-Driven Development: Design once, generate everywhere!** 🚀