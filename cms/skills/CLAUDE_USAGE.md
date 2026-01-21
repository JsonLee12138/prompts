# Using CMS Skills with Claude Code

This guide shows you how to effectively use the CMS skills in Claude Code for your Headless CMS development.

## 🎯 Quick Reference

### Available Skills
```bash
@cms/cms-coding-standard      # Go backend standards
@cms/cms-response-format       # HTTP response patterns
@cms/schema-driven-development # Schema-based workflow
```

## 📝 Usage Examples

### 1. Creating a New Module

**Step 1: Define the Schema**
```bash
@cms/schema-driven-development I need to create a new "Article" module. Show me how to define the schema.json file with fields: title (required string), content (required text), status (enum: draft/published), and author_id (UUID).
```

**Step 2: Implement Backend**
```bash
@cms/cms-coding-standard Based on this Article schema, show me how to implement the 4 core files (module.go, controller.go, service.go, dto.go) following the NestJS-style pattern.
```

**Step 3: Build Frontend**
```bash
@cms/cms-response-format I have an Article API. Show me how to create a React component that fetches and displays articles with pagination using the Strapi response format.
```

### 2. Code Review

```bash
@cms/cms-coding-standard Review this Go code for compliance with CMS standards:

[Paste your code here]
```

### 3. Debugging API Issues

```bash
@cms/cms-response-format My API is returning errors. How do I use traceId to debug, and what's the correct error response format for validation errors?
```

### 4. Schema Updates

```bash
@cms/schema-driven-development I need to add a "phone" field to my User schema. Show me the complete workflow from updating schema.json to frontend integration.
```

### 5. Multi-Tenancy Implementation

```bash
@cms/cms-coding-standard How do I implement multi-tenancy in my Service layer? Show me how to filter queries by tenant_id from context.
```

### 6. API Key Authentication

```bash
@cms/cms-coding-standard I need to protect my data APIs with API Key authentication. Show me the complete implementation including the middleware and API Key management module.
```

## 🔄 Combining Multiple Skills

### Full Stack Development
```bash
@cms/schema-driven-development @cms/cms-coding-standard @cms/cms-response-format
Create a complete "Product" module with:
1. Schema with fields: name, price, category, in_stock
2. Backend implementation with proper validation
3. Frontend table and form components
```

### Backend Focus
```bash
@cms/cms-coding-standard @cms/cms-response-format
Help me implement a secure CRUD API for comments including:
- API Key authentication
- Input validation
- Strapi-style responses
- Error handling
```

### Frontend Focus
```bash
@cms/schema-driven-development @cms/cms-response-format
Generate a complete React form for user registration that:
- Fetches schema from API
- Creates dynamic form fields
- Handles validation
- Submits to backend
```

## 📋 Common Patterns

### Pattern 1: CRUD Operations
```bash
@cms/cms-coding-standard Show me the complete CRUD implementation for a Post module including:
- Service methods (Create, Get, List, Update, Delete)
- Controller handlers
- DTO definitions
- Error handling
```

### Pattern 2: Pagination
```bash
@cms/cms-response-format How do I implement pagination in both Go backend and React frontend?
```

### Pattern 3: Validation
```bash
@cms/schema-driven-development Show me how validation works across the stack:
- Schema validate rules
- Go binding and validation
- Frontend Zod schema generation
```

### Pattern 4: Permissions
```bash
@cms/cms-coding-standard How do I implement role-based access control using Casbin for my User module?
```

## 💡 Pro Tips

### 1. Always Start with Schema
```bash
# Before writing any code, define your schema
@cms/schema-driven-development Define a schema for [your entity]
```

### 2. Use TraceId for Debugging
```bash
@cms/cms-response-format How do I use traceId to debug API issues in development?
```

### 3. Follow the 4-File Pattern
```bash
@cms/cms-coding-standard What are the 4 core files every module needs?
```

### 4. Check Response Format
```bash
@cms/cms-response-format What's the correct response format for [success/error/pagination]?
```

### 5. Security First
```bash
@cms/cms-coding-standard What security checks do I need for a new API endpoint?
```

## 🎓 Learning Path

### Beginner
1. Start with `@cms/schema-driven-development` to understand the workflow
2. Learn `@cms/cms-response-format` for API patterns
3. Study `@cms/cms-coding-standard` for backend implementation

### Intermediate
1. Combine all three skills for full module creation
2. Learn authentication patterns
3. Understand multi-tenancy

### Advanced
1. Custom middleware development
2. Plugin architecture
3. Performance optimization

## 🔧 Troubleshooting

### Issue: "Schema not found"
```bash
@cms/schema-driven-development Where should I place schema.json files?
```

### Issue: "Validation errors not showing"
```bash
@cms/cms-response-format How do I handle validation errors in the frontend?
```

### Issue: "Permission denied"
```bash
@cms/cms-coding-standard How does Casbin permission checking work?
```

### Issue: "Multi-tenant data leakage"
```bash
@cms/cms-coding-standard How do I ensure proper tenant isolation?
```

## 📚 Reference Commands

```bash
# Module creation
@cms/schema-driven-development Create schema for [entity]
@cms/cms-coding-standard Implement 4 files for [entity]
@cms/cms-response-format Frontend for [entity] API

# Code quality
@cms/cms-coding-standard Review this code: [code]
@cms/cms-coding-standard What's the best practice for [pattern]?

# API design
@cms/cms-response-format Correct response format for [scenario]
@cms/schema-driven-development Schema validation rules for [field type]

# Security
@cms/cms-coding-standard API Key authentication implementation
@cms/cms-coding-standard JWT vs API Key when to use each

# Testing
@cms/cms-coding-standard How to test [component]?
@cms/cms-response-format Mock API responses for testing
```

## ✅ Checklist Before Committing

Ask `@cms/cms-coding-standard`:
- [ ] Does my module follow the 4-file pattern?
- [ ] Are all fields from schema included in responses?
- [ ] Is API Key auth enabled for data APIs?
- [ ] Is multi-tenancy properly implemented?
- [ ] Are errors handled correctly?

Ask `@cms/schema-driven-development`:
- [ ] Does schema.json exist?
- [ ] Are validate rules correct?
- [ ] Does frontend use Schema API?
- [ ] Are tables/forms generated from schema?

Ask `@cms/cms-response-format`:
- [ ] Is response format consistent?
- [ ] Are pagination fields correct?
- [ ] Is error format standard?
- [ ] Does frontend handle responses properly?

---

## 🚀 Start Now

```bash
# Pick your first task and start with the appropriate skill
@cms/schema-driven-development I'm starting a new CMS project. What's the first step?
```

Remember: **Schema first, then backend, then frontend!** 📋 → 🔧 → 🎨