---
name: cms-response-format
description: Standardizes HTTP response format for CMS APIs using Strapi-style structure with TypeScript interfaces, Go implementations, and frontend integration examples
---

# CMS Response Format Skill

This skill provides standardized HTTP response formats for CMS APIs using Strapi-style structure.

## 🎯 When to Use This Skill

- **Building API clients** - Need consistent response format
- **Creating frontend components** - Expecting standardized data structure
- **Implementing backend responses** - Following established patterns
- **API documentation** - Reference standard response format
- **Error handling** - Consistent error response structure

## 📋 Response Format

### Success Response (Strapi Style)
```json
{
  "data": {
    "id": 1,
    "attributes": {
      "title": "Example",
      "content": "Content here",
      "createdAt": "2024-01-13T10:00:00.000Z",
      "updatedAt": "2024-01-13T10:00:00.000Z"
    }
  },
  "meta": {}
}
```

### List Response
```json
{
  "data": [
    { "id": 1, "attributes": { ... } },
    { "id": 2, "attributes": { ... } }
  ],
  "meta": {
    "pagination": {
      "page": 1,
      "pageSize": 25,
      "pageCount": 1,
      "total": 2
    }
  }
}
```

### Error Response
```json
{
  "error": {
    "status": 400,
    "name": "BadRequestError",
    "message": "Invalid input",
    "details": {
      "field": "email",
      "message": "Must be a valid email"
    }
  }
}
```

## 📚 Resources

### Reference Documents
- **Response Format**: `references/response-format.md`

### Templates
- **Response Builder**: `assets/response-builder.go`
- **TypeScript Types**: `assets/response-types.ts`

---

**Standardized responses for better API consistency!** 📊
