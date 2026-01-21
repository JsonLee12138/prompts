# Schema-Driven Development Skill Usage Rules

> ⚠️ **IMPORTANT**: This file documents when and how to use the schema-driven-development skill.

## Overview

The `schema-driven-development` skill provides a complete toolkit for designing schemas, validating them, and generating production-ready code from schema.json as the single source of truth for Headless CMS.

### Integration with @schema/ Skills

This CMS skill integrates **four specialized @schema/ skills** into a unified toolkit:

```
┌─────────────────────────────────────────────────────────────────┐
│           CMS Schema-Driven Development Skill                   │
│         (Unified Toolkit for Headless CMS)                      │
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

**When to use each @schema/ skill directly:**
- **`@schema/backend-developer`**: Need detailed Go backend patterns
- **`@schema/table-developer`**: Need React table implementation details
- **`@schema/form-developer`**: Need React form implementation details
- **`@schema/code-detector`**: Need code quality validation rules

**When to use this CMS skill:**
- Complete end-to-end module development
- Schema-first workflow
- Integrated validation and generation
- CMS-specific patterns and examples

## When to Use This Skill

### Primary Triggers

**Use this skill when users mention:**
- "Create a new [entity] module"
- "Add a new field to [entity] schema"
- "I need a [entity] CRUD module"
- "Generate Go backend from schema"
- "Generate TypeScript frontend from schema"
- "Validate my schema"
- "Design a schema for [entity]"
- "Build a form/table from schema"
- "Create API endpoints for [entity]"
- "Scaffold a new module"

### Specific Scenarios

1. **New Module Creation**
   - User wants to create a complete module (backend + frontend)
   - User needs CRUD operations for a new entity
   - User is starting a new feature

2. **Schema Design**
   - User needs help designing entity structure
   - User wants interactive schema creation
   - User needs to plan data models

3. **Code Generation**
   - User has existing schema and wants generated code
   - User needs Go backend code (DTO, Service, Controller)
   - User needs TypeScript frontend code (Types, API, Components)

4. **Validation**
   - User wants to validate schema before coding
   - User modified schema and needs verification
   - User is doing code review

## How to Use This Skill

### Complete Workflow (Always Follow This Order)

```
1. Design Schema (if not exists)
   └─> Use scripts/designer/designer.py
   └─> Output: schema.json

2. Validate Schema (always before generation)
   └─> Use scripts/validator/validate_schema.py
   └─> Ensure: ✅ Schema is valid

3. Generate Backend Code
   └─> Use scripts/generator/generate_go.py
   └─> Output: backend/dto.go, service.go, controller.go, module.go

4. Generate Frontend Code
   └─> Use scripts/generator/generate_ts.py
   └─> Output: frontend/types/, lib/api/, components/

5. Customize & Test
   └─> Add business logic
   └─> Run tests
```

**⚠️ CRITICAL: Always validate before generating code!**

### Step-by-Step Instructions

#### Step 1: Design Schema (If Needed)

**When user says:** "I need a new User module"

**Action:**
```bash
cd /Users/jsonlee/Projects/prompts/cms/skills/schema-driven-development
python scripts/designer/designer.py
```

**Follow the interactive prompts:**
- Entity name (PascalCase): `User`
- Collection name: `users`
- Fields: `email`, `password`, `name`, `role`
- Relationships: Add as needed
- UI configuration: Submit/reset button texts

**Output:** `user-schema.json`

#### Step 2: Validate Schema

**Always validate before generation:**

```bash
python scripts/validator/validate_schema.py user-schema.json
```

**Expected output:**
```
✅ user-schema.json - Valid
```

**If errors appear:**
- Read the error messages
- Fix the schema according to validation-rules.md
- Re-validate until ✅

#### Step 3: Generate Backend (Go)

```bash
python scripts/generator/generate_go.py user-schema.json --output ./backend
```

**Generated files:**
```
backend/user/
├── dto.go          # CreateDTO, UpdateDTO with validation tags
├── service.go      # CRUD operations, password hashing, relations
├── controller.go   # HTTP handlers, error handling
└── module.go       # Route registration
```

**What to do next:**
- Review generated code
- Add business logic to `service.go`
- Add auth checks to `controller.go`
- Run `go test ./...`

#### Step 4: Generate Frontend (TypeScript)

```bash
python scripts/generator/generate_ts.py user-schema.json --output ./frontend
```

**Generated files:**
```
frontend/
├── types/user.ts           # Type definitions
├── lib/api/user.ts         # API client
├── components/UserForm.tsx # Form with Zod validation
└── components/UserTable.tsx # Table component
```

**What to do next:**
- Review generated components
- Customize UI in `UserForm.tsx`
- Add custom validation if needed
- Run `npm test`

#### Step 5: Customize

**Backend customization:**
```go
// In backend/user/service.custom.go
func (s *Service) CustomLogic(ctx context.Context, id string) error {
    // Add business logic here
    return nil
}
```

**Frontend customization:**
```typescript
// In frontend/components/UserForm.custom.tsx
export function CustomUserForm() {
  // Custom UI logic here
}
```

## Schema Format Reference

### Complete Example Schema

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
    "showReset": true
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
        "showInList": true
      }
    },
    "password": {
      "type": "password",
      "label": "密码",
      "validate": {
        "required": true,
        "minLength": 8
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

## Common Patterns

### Pattern 1: User Module
```json
{
  "name": "User",
  "properties": {
    "email": { "type": "string", "validate": { "required": true, "format": "email" } },
    "password": { "type": "password", "validate": { "required": true, "minLength": 8 } },
    "role": { "type": "enum", "enum": ["admin", "editor", "viewer"] }
  }
}
```

### Pattern 2: Product with Category
```json
{
  "name": "Product",
  "properties": {
    "name": { "type": "string", "validate": { "required": true } },
    "price": { "type": "number", "validate": { "min": 0 } },
    "category": { "$ref": "Category", "x-relation": { "type": "many2One" } }
  }
}
```

### Pattern 3: Blog with Relationships
```json
{
  "name": "Post",
  "properties": {
    "title": { "type": "string", "validate": { "required": true } },
    "author": { "$ref": "User", "x-relation": { "type": "many2One" } },
    "categories": { "$ref": "Category", "x-relation": { "type": "many2Many" } }
  }
}
```

## Validation Rules Summary

### Field Types
- `string`, `text`, `integer`, `number`, `boolean`, `enum`
- `password`, `email`, `url`, `datetime`, `date`
- `array`, `object`, `json`, `media`, `image`

### Validation Rules
- `required`: Must have value
- `min`/`max`: Minimum/maximum value (numbers only)
- `minLength`/`maxLength`: Minimum/maximum length (strings/arrays)
- `format`: email, url, uuid, etc.
- `pattern`: Regex pattern
- `unique`: Database unique constraint

### Relationship Types
- `many2One`: Many entities to one (e.g., posts → author)
- `one2Many`: One entity to many (e.g., author → posts)
- `many2Many`: Many to many (e.g., posts ↔ tags)
- `one2One`: One to one

### UI Widgets
- `input`, `textarea`, `number`, `select`, `checkbox`
- `date`, `datetime`, `password`, `email`, `url`
- `file`, `image`, `tags`, `switch`, `radio`

## Error Handling

### Common Validation Errors

**Missing required field:**
```
❌ Missing required field: name
→ Fix: Add "name" to properties
```

**Invalid type:**
```
❌ Invalid type: 'str' for field 'email'
→ Fix: Use proper type in schema
```

**Relationship error:**
```
❌ Invalid relationship: missing x-relation.type
→ Fix: Add x-relation with type
```

### Generation Errors

**Schema not valid:**
```
Error: Schema validation failed
→ Action: Run validation script first
```

**Output directory exists:**
```
Error: Output directory already exists
→ Action: Use --force or different directory
```

## Best Practices

### 1. Always Validate First
```bash
# ✅ Correct
python scripts/validator/validate_schema.py schema.json
python scripts/generator/generate_go.py schema.json --output ./backend

# ❌ Wrong
python scripts/generator/generate_go.py schema.json --output ./backend
# (without validation)
```

### 2. Keep Schema in Version Control
```bash
git add schemas/user.json
git commit -m "feat: add user schema"
```

### 3. Use Custom Files for Business Logic
- Never edit generated files directly
- Use `.custom.go` and `.custom.tsx` files
- Regenerate when schema changes

### 4. Test After Generation
```bash
# Backend
cd backend && go test ./...

# Frontend
cd frontend && npm test
```

### 5. Document Business Rules
Add comments in custom files explaining why customizations were made.

## Quick Reference Commands

```bash
# Complete workflow
cd /Users/jsonlee/Projects/prompts/cms/skills/schema-driven-development

# 1. Design
python scripts/designer/designer.py

# 2. Validate
python scripts/validator/validate_schema.py schema.json

# 3. Generate backend
python scripts/generator/generate_go.py schema.json --output ./backend

# 4. Generate frontend
python scripts/generator/generate_ts.py schema.json --output ./frontend

# 5. Validate all schemas in directory
python scripts/validator/validate_all.py ./schemas/

# 6. Quick validation
python scripts/validator/quick_validate.py ./schemas/
```

## Integration Points

### CI/CD Pipeline
```yaml
# .github/workflows/validate.yml
- name: Validate Schemas
  run: |
    python cms/skills/schema-driven-development/scripts/validator/validate_all.py ./schemas/
```

### Pre-commit Hook
```bash
# .git/hooks/pre-commit
python cms/skills/schema-driven-development/scripts/validator/validate_all.py schemas/
```

### Documentation Generation
```bash
# Generate API docs from schemas
python scripts/generate_docs.py schemas/
```

## Troubleshooting

### Issue: "Schema not found"
**Solution:** Check file path and extension

### Issue: "Validation errors"
**Solution:** Read validation-rules.md, fix schema, re-validate

### Issue: "Generation fails"
**Solution:** Ensure schema is valid before generation

### Issue: "Relationship not working"
**Solution:** Verify $ref and x-relation.type are correct

### Issue: "Missing fields in generated code"
**Solution:** Check if fields are marked as private or have incorrect types

## Resources

### Scripts
- `scripts/designer/designer.py` - Interactive schema designer
- `scripts/validator/validate_schema.py` - Single schema validation
- `scripts/validator/validate_all.py` - Batch validation
- `scripts/generator/generate_go.py` - Go backend generator
- `scripts/generator/generate_ts.py` - TypeScript frontend generator

### References
- `assets/validation-rules.md` - Complete validation rules
- `references/schema-development.md` - Detailed development guide

### Templates
- `assets/schema.template.json` - Blank template
- `assets/example-user.json` - Working example

## Summary Checklist

Before using this skill, verify:
- [ ] User wants to create/design/validate/generate from schema
- [ ] Schema exists OR user needs help designing one
- [ ] Follow the workflow: Design → Validate → Generate → Customize
- [ ] Always validate before generation
- [ ] Use custom files for business logic
- [ ] Test after generation

---

**Remember: Schema as Single Source of Truth!** 🚀