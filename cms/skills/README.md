# CMS Skills Collection

A comprehensive collection of Claude Skills for Headless CMS development. These skills provide specialized expertise for building Go-based CMS systems with modern architecture patterns.

## 📚 Available Skills

### 1. **@cms/cms-coding-standard**
Comprehensive Go coding standards and architectural patterns for Headless CMS development.

**Key Features:**
- NestJS-style module structure (4 core files)
- Ent ORM best practices
- Chi framework conventions
- API Key & JWT authentication
- Multi-tenancy patterns
- Security guidelines
- Code review checklist

**Use When:**
- Creating new CMS modules
- Reviewing Go code
- Establishing project conventions

---

### 2. **@cms/cms-response-format**
Standardized HTTP response format using Strapi-style structure.

**Key Features:**
- Unified response interfaces (TypeScript & Go)
- Pagination patterns
- Error handling standards
- Frontend integration examples
- React hooks & components
- Debugging with TraceId

**Use When:**
- Building API clients
- Creating frontend components
- Implementing backend responses
- Debugging API issues

---

### 3. **@cms/schema-driven-development**
Schema-driven development workflow with前后端同步开发.

**Key Features:**
- Schema as single source of truth
- Schema API endpoints
- Validation rules mapping
- Dynamic table generation
- Dynamic form generation
- Zod schema generation

**Use When:**
- Creating new modules
- Updating data structures
- Building dynamic UI components
- API design

---

## 🚀 Quick Start

### Using Skills in Claude Code

```bash
# Reference a specific skill
@cms/cms-coding-standard

# Ask questions about the skill
@cms/cms-coding-standard How do I create a new module?

# Combine multiple skills
@cms/schema-driven-development @cms/cms-response-format
```

### Example Workflows

#### 1. Create a New Module
```bash
# Step 1: Define schema
@cms/schema-driven-development Show me how to define a schema for a Post module

# Step 2: Implement backend
@cms/cms-coding-standard How do I implement the 4 core files for the Post module?

# Step 3: Build frontend
@cms/cms-response-format How do I create a frontend component for the Post API?
```

#### 2. Code Review
```bash
@cms/cms-coding-standard Review this code for compliance with standards
```

#### 3. Debug API Issues
```bash
@cms/cms-response-format How do I debug API responses with traceId?
```

---

## 📁 Directory Structure

```
cms-skills/
├── README.md                          # This file
├── cms-coding-standard/
│   └── SKILL.md                       # Go standards & patterns
├── cms-response-format/
│   └── SKILL.md                       # HTTP response standards
└── schema-driven-development/
    └── SKILL.md                       # Schema-based workflow
```

---

## 🎯 Skill Usage Guidelines

### When to Use Each Skill

| Skill | Primary Use Cases |
|-------|------------------|
| **cms-coding-standard** | Backend development, code review, architecture decisions |
| **cms-response-format** | API design, frontend integration, debugging |
| **schema-driven-development** | Module creation, data modeling, UI generation |

### Skill Combinations

```bash
# Full module development
@cms/schema-driven-development @cms/cms-coding-standard @cms/cms-response-format

# Backend-focused
@cms/cms-coding-standard @cms/cms-response-format

# Frontend-focused
@cms/schema-driven-development @cms/cms-response-format
```

---

## 🔧 Technology Stack

- **Backend**: Go, Ent ORM, Chi, Casbin, JWT
- **Frontend**: TypeScript, React, Zod, React Hook Form
- **API**: RESTful, Strapi-style responses
- **Architecture**: Schema-driven, NestJS-style modules

---

## 📋 Development Principles

### 1. Schema as Single Source of Truth
- All data structures defined in `schema.json`
- Backend implements based on Schema
- Frontend generates from Schema API
- Changes sync automatically

### 2. Consistent Architecture
- 4 core files per module
- Clear separation of concerns
- Dependency injection
- Context-based multi-tenancy

### 3. Security First
- API Key authentication for all data APIs
- Casbin-based permission system
- JWT for management interfaces
- Input validation at all layers

### 4. Type Safety
- TypeScript types from Schema
- Go structs from Schema
- Compile-time validation
- Runtime validation

---

## 📚 Related Documentation

- [Original CMS Documentation](../cms/)
  - [CMS Coding Standard](../cms/CMS_CODING_STANDARD.md)
  - [CMS Response Format](../cms/CMS_RESPONSE.md)
  - [Schema Driven Development](../cms/SCHEMA_DRIVEN_DEVELOPMENT.md)

---

## 🤝 Contributing

These skills are generated from the original CMS documentation. To update:

1. Modify the original `.md` files in `cms/`
2. Regenerate the SKILL.md files
3. Update version numbers
4. Test with Claude Code

---

## 📝 Version History

- **v1.0.0** (2026-01-13): Initial release
  - cms-coding-standard
  - cms-response-format
  - schema-driven-development

---

**Built with ❤️ for Headless CMS Development** 🚀