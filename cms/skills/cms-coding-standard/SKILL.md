---
name: cms-coding-standard
description: Provides Go coding standards and architectural patterns for Headless CMS development with NestJS-style structure, Ent ORM, Chi framework, and security guidelines
---

# CMS Coding Standard Skill

This skill provides comprehensive coding standards and architectural patterns for Headless CMS development using Go.

## 🎯 When to Use This Skill

- **Creating new CMS modules** - Need to follow proper structure and conventions
- **Code review** - Verify adherence to project standards
- **Refactoring existing code** - Ensure changes follow established patterns
- **Onboarding new developers** - Provide clear development guidelines
- **Troubleshooting** - Understand expected patterns and best practices

## 📋 Core Principles

### 1. Project Structure
```
cms/
├── cmd/server/          # Server entry point
├── api/v1/              # Business modules
│   └── module_name/     # Each module has 4 core files
│       ├── schema.json  # Single source of truth
│       ├── module.go    # Dependency injection & routing
│       ├── controller.go # HTTP handlers
│       ├── service.go   # Business logic
│       └── dto.go       # Data transfer objects
├── _gen/                # Ent generated code
├── core/                # Shared utilities
└── config/              # Configuration
```

### 2. Module Architecture (NestJS Style)
Every business module **must** contain 4 core files:
- `module.go` - Dependency injection & routing
- `controller.go` - HTTP handlers
- `service.go` - Business logic
- `dto.go` - Data transfer objects

## 📚 Resources

### Reference Documents
- **Complete Standards**: `references/coding-standards.md`
- **Security Guidelines**: `references/security.md`

### Templates
- **Module Template**: `assets/module.template.go`
- **Controller Template**: `assets/controller.template.go`

---

**Follow these standards for consistent, maintainable code!** 🚀
