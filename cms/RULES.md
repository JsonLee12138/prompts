# CMS Skill Rules

## 📋 File Naming Standards

### General Rules
- **ALWAYS use English** for all file and directory names
- **NEVER use Chinese characters** in file names
- **Use kebab-case** for multi-word names
- **Keep names lowercase** with hyphens only

### Skill Files
- **kebab-case**: `cms-coding-standard`, `schema-driven-development`, `cms-response-format`
- **Directory names**: `skills/`, `docs/`, `references/`

### Documentation Files
- **UPPER_SNAKE_CASE**: `README.md`, `INDEX.md`
- **kebab-case**: `setup-guide.md`, `quick-start.md`

## 🎯 Skill Usage Rules

### When to Use These Skills

**Use @cms-coding-standard when:**
- Writing Go code for Headless CMS
- Reviewing code for NestJS-style patterns
- Checking Ent ORM usage
- Validating Chi framework conventions
- Ensuring API Key authentication
- Implementing multi-tenancy

**Use @schema-driven-development when:**
- Creating new CMS modules
- Designing data structures
- Building dynamic frontend components
- Synchronizing前后端开发
- Working with schema.json

**Use @cms-response-format when:**
- Building API clients
- Creating frontend components
- Implementing backend responses
- Handling errors
- Working with TypeScript interfaces

### Required Workflow

#### 1. Module Development
```bash
# Start with schema
@schema-driven-development Create a user module

# Then implement code
@cms-coding-standard Review this Go code
```

#### 2. API Development
```bash
# Design response format
@cms-response-format Create API response for user list

# Implement backend
@cms-coding-standard Check my Go implementation
```

#### 3. Code Review
```bash
# Before merging
@cms-coding-standard Review for:
- NestJS patterns
- Ent ORM usage
- Chi conventions
- Security compliance
```

## 📝 Quality Standards

### Required Elements
- ✅ **YAML frontmatter** with proper metadata
- ✅ **Imperative language** in descriptions
- ✅ **Clear usage scenarios**
- ✅ **Reference to bundled resources**
- ✅ **English names only**

### Validation Checklist
- [ ] Skill names use kebab-case
- [ ] Description starts with verb
- [ ] No angle brackets in description
- [ ] Directory structure follows conventions
- [ ] Scripts are executable (if present)
- [ ] References are properly formatted

## 🚫 Common Mistakes

### ❌ Don't Do This
```go
// Wrong naming
type user_service struct {}  // Should be UserService

// Wrong patterns
func getUser() {             // Should follow NestJS patterns
    // Direct DB access
}
```

### ✅ Do This Instead
```go
// Correct naming
type UserService struct {}

// Correct patterns (NestJS-style)
type UserService struct {
    userRepo UserRepository
}

func (s *UserService) GetUser(id string) (*User, error) {
    // Use repository pattern
    return s.userRepo.FindByID(id)
}
```

## 📚 Resources

### Skills
- **@cms-coding-standard**: Go coding standards
- **@schema-driven-development**: Schema-driven workflow
- **@cms-response-format**: API response format

### Reference Documents
- **CMS Documentation**: `cms/README.md`
- **Quick Index**: `cms/INDEX.md`
- **Detailed Docs**: `cms/docs/`

---

**Last Updated**: 2026-01-13
**Version**: 1.0
**Maintainer**: CMS Team