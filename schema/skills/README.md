# Schema Skills Collection

This directory contains a complete set of skills for Schema Driven Development (SDD).

## Skills Overview

### 1. Backend Developer (`backend-developer`)
**Purpose**: Generate Go backend code from schema definitions including DTOs, services, controllers, and database schemas

**Key Features**:
- ✅ DTO generation with validation tags
- ✅ Service layer with business logic
- ✅ Controller with HTTP endpoints
- ✅ Module for route registration
- ✅ Ent database schemas
- ✅ Password hashing (bcrypt)
- ✅ Relationship handling

**Usage**:
```bash
python scripts/generate_go.py schema.json --output ./backend
python scripts/generate_go.py schema.json --output ./backend --include-ent
```

---

### 2. Table Developer (`table-developer`)
**Purpose**: Generate React table components from schema definitions

**Key Features**:
- ✅ TypeScript type definitions
- ✅ API client (CRUD operations)
- ✅ Table component with columns
- ✅ Dynamic hooks (search, sort, pagination)
- ✅ Export functionality
- ✅ Loading/empty states
- ✅ Relationship display

**Usage**:
```bash
python scripts/generate_table.py schema.json --output ./frontend
python scripts/generate_table.py schema.json --output ./frontend --features export,search
```

---

### 3. Form Developer (`form-developer`)
**Purpose**: Generate React form components from schema definitions

**Key Features**:
- ✅ Zod validation schemas
- ✅ React Hook Form integration
- ✅ Dynamic form components
- ✅ File upload handling
- ✅ Nested forms
- ✅ Error display
- ✅ Relationship fields (single/multi select)

**Usage**:
```bash
python scripts/generate_form.py schema.json --output ./frontend
python scripts/generate_form.py schema.json --output ./frontend --mode create
```

---

### 4. Code Detector (`code-detector`)
**Purpose**: Analyze and validate generated code against schema definitions

**Key Features**:
- ✅ Backend code analysis (DTO, Service, Controller, Schema)
- ✅ Frontend code analysis (Types, API, Forms, Tables)
- ✅ Detect missing fields and validation issues
- ✅ Check security practices
- ✅ Detailed error reports

**Usage**:
```bash
# Backend analysis
python scripts/detect_backend.py ./backend --schema ../entity_schema.json

# Frontend analysis
python scripts/detect_frontend.py ./frontend --schema ../entity_schema.json

# Full-stack analysis
python scripts/analyze_all.py ./backend ./frontend --schema ../entity_schema.json
```

---

## Complete Workflow

### 1. Design Schema
```bash
# Create or use existing schema
# Reference: ../entity_schema.json
```

**Example Schema**:
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

### 2. Generate Code
```bash
# Backend
python backend-developer/scripts/generate_go.py ../entity_schema.json --output ./backend

# Frontend Table
python table-developer/scripts/generate_table.py ../entity_schema.json --output ./frontend

# Frontend Form
python form-developer/scripts/generate_form.py ../entity_schema.json --output ./frontend
```

### 3. Detect Issues
```bash
# Full-stack analysis
python code-detector/scripts/analyze_all.py ./backend ./frontend --schema ../entity_schema.json
```

### 4. Fix & Test
```bash
# Fix issues based on detection results
# Run tests
# Commit code
```

---

## Generated File Structure

### Backend (Go)
```
backend/user/
├── dto.go          # CreateDTO, UpdateDTO with validation
├── service.go      # CRUD logic with bcrypt
├── controller.go   # HTTP handlers
├── module.go       # Route registration
└── schema.go       # Ent schema (optional)
```

### Frontend (TypeScript/React)
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

## Common Patterns

### User Management
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

**Generated**:
- ✅ Create/Update/Get/Delete/List endpoints
- ✅ Form with validation
- ✅ Table with columns
- ✅ Type definitions
- ✅ Password hashing

### Content Management
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

**Generated**:
- ✅ Relationship handling in service
- ✅ Preload configuration
- ✅ Label field display
- ✅ Multi-select UI

### Soft Delete
```json
{
  "name": "Order",
  "softDelete": true,
  "properties": {
    "orderNo": { "type": "string", "validate": { "required": true } },
    "status": { "type": "enum", "validate": { "enum": ["pending", "paid", "shipped"] } }
  }
}
```

**Generated**:
- ✅ deleted_at field
- ✅ Update instead of delete
- ✅ Filter in queries
- ✅ Restore functionality

---

## Best Practices

### 1. Always Validate Schema First
```bash
# If you have a validator
python scripts/validate_schema.py schema.json
```

### 2. Generate Then Detect
```bash
# Generate
python backend-developer/scripts/generate_go.py schema.json --output ./backend

# Detect issues
python code-detector/scripts/detect_backend.py ./backend --schema schema.json
```

### 3. Review Generated Code
- Check business logic needs
- Add custom validations
- Modify as needed
- Write tests

### 4. Keep Schemas in Version Control
```bash
git add schema.json
git commit -m "feat: add user schema"
```

### 5. Test After Generation
```bash
# Backend tests
cd backend && go test ./...

# Frontend tests
cd frontend && npm test
```

---

## Integration

### With CI/CD
```yaml
# .github/workflows/schema.yml
name: Schema Code Generation

on: [push, pull_request]

jobs:
  generate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Generate Backend
        run: |
          python skills/backend-developer/scripts/generate_go.py schema.json --output ./backend

      - name: Generate Frontend
        run: |
          python skills/table-developer/scripts/generate_table.py schema.json --output ./frontend
          python skills/form-developer/scripts/generate_form.py schema.json --output ./frontend

      - name: Detect Issues
        run: |
          python skills/code-detector/scripts/analyze_all.py ./backend ./frontend --schema schema.json
```

### With Pre-commit Hooks
```bash
# .git/hooks/pre-commit
python skills/code-detector/scripts/analyze_all.py ./backend ./frontend --schema schema.json
if [ $? -ne 0 ]; then
  echo "Code quality checks failed"
  exit 1
fi
```

---

## Troubleshooting

### Issue: Generation Fails
**Solution**: Ensure schema is valid before generation

### Issue: Missing Fields in Generated Code
**Solution**: Check if fields are in schema properties

### Issue: Relationship Not Working
**Solution**: Verify $ref and x-relation.type are correct

### Issue: Code Quality Issues
**Solution**: Run code detector and fix reported issues

---

## Related Resources

- [Unified Rules](../RULES.md) - Complete guidelines
- [Entity Schema Specification](../entity_schema.json)
- [Schema Driven Development](../SCHEMA_DRIVEN_DEVELOPMENT.md)
- [Skills Summary](SCHEMA_SKILLS_SUMMARY.md)

---

## Quick Reference

### Core Files
- `../entity_schema.json` - Schema specification
- `../RULES.md` - Unified rules
- `*/SKILL.md` - Individual skill docs

### Common Commands
```bash
# Backend
python skills/backend-developer/scripts/generate_go.py schema.json --output ./backend

# Frontend Table
python skills/table-developer/scripts/generate_table.py schema.json --output ./frontend

# Frontend Form
python skills/form-developer/scripts/generate_form.py schema.json --output ./frontend

# Code Detection
python skills/code-detector/scripts/analyze_all.py ./backend ./frontend --schema schema.json
```

---

**Happy Schema Driven Development!** 🚀
