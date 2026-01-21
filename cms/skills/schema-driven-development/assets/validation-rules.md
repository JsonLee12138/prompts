# Schema Validation Rules Reference

> This document provides detailed validation rule mappings based on the `entity_schema.json` specification.

## 📚 Related Documents

- **`../references/entity_schema.json`** - Schema definition specification
- **`../references/schema-development.md`** - Complete development guide
- **`../SKILL.md`** - Skill usage guide
- **`../rules.md`** - Skill usage rules with @schema/ integration

## 🔗 Integration with @schema/ Skills

This validation reference is **based on and extends** the patterns from @schema/ skills:

| @schema/ Skill | Focus | CMS Integration |
|----------------|-------|-----------------|
| **backend-developer** | Go DTO/Service/Controller | Validation tags, password hashing, relations |
| **table-developer** | React table components | Column generation, search/sort/pagination |
| **form-developer** | React forms + Zod | Field rendering, validation schemas |
| **code-detector** | Code quality checks | Backend/frontend validation patterns |

**Key patterns adopted from @schema/:**
- ✅ `$ref` for relationships (not `type: "uid"` + `target`)
- ✅ `label` field priority for UI display
- ✅ `ui.placeholder` priority rules
- ✅ Backend validation layering (Controller/Service)
- ✅ Frontend dynamic generation from schema

---

## Field Types

| Type | Description | Go Type | TypeScript Type | Notes |
|------|-------------|---------|-----------------|-------|
| `string` | Text field | `string` | `string` | General text content |
| `text` | Long text | `string` | `string` | Multi-line text, textarea |
| `integer` | Integer number | `int` | `number` | Whole numbers |
| `number` | Decimal number | `float64` | `number` | Floating point |
| `boolean` | True/false | `bool` | `boolean` | Checkbox |
| `enum` | Enum values | `string` | `string` (union) | Single select |
| `password` | Password field | `string` | `string` | Masked input |
| `email` | Email address | `string` | `string` | Email format |
| `url` | URL | `string` | `string` | URL format |
| `date` | Date only | `time.Time` | `string` | YYYY-MM-DD |
| `datetime` | Date & time | `time.Time` | `string` | ISO 8601 |
| `timestamp` | Unix timestamp | `int64` | `number` | Seconds since epoch |
| `json` | JSON data | `datatypes.JSON` | `object` | JSON object |
| `array` | Array of items | `[]string` | `string[]` | Multiple values |
| `file` | File upload | `string` | `string` | File path/URL |
| `image` | Image upload | `string` | `string` | Image path/URL |
| `uid` | Unique ID | `string` | `string` | UUID/ObjectID |
| `uuid` | UUID | `string` | `string` | UUID format |

## Validation Rules

| Rule | Type | Description | Ent Mapping | Zod Mapping | Example |
|------|------|-------------|-------------|-------------|---------|
| `required` | boolean | Must have value | `.NotEmpty()` | `.nonempty()` | `true` |
| `nullable` | boolean | Can be null | `.Nillable()` | `.nullable()` | `true` |
| `min` | number | Minimum value (numbers only) | `.Min()` | `.min()` / `.gte()` | `0` |
| `max` | number | Maximum value (numbers only) | `.Max()` | `.max()` / `.lte()` | `100` |
| `minLength` | integer | Minimum length (strings/arrays) | `.MinLen()` | `.min()` | `3` |
| `maxLength` | integer | Maximum length (strings/arrays) | `.MaxLen()` | `.max()` | `50` |
| `pattern` | string | Regex pattern | `.Match(regexp)` | `.regex()` | `"^[A-Z]+$"` |
| `format` | string | Predefined format | Custom Validator | `.email()`, `.url()` | `"email"` |
| `positive` | boolean | Positive number | `.Positive()` | `.positive()` | `true` |
| `negative` | boolean | Negative number | `.Negative()` | `.negative()` | `true` |
| `nonNegative` | boolean | Non-negative | `.NonNegative()` | `.nonnegative()` | `true` |
| `nonPositive` | boolean | Non-positive | `.NonPositive()` | `.nonpositive()` | `true` |
| `integer` | boolean | Integer only | Integer type | `.int()` | `true` |
| `enum` | array | Enum values | `.Enum()` | `.enum()` | `["a","b"]` |
| `custom` | array | Custom validation | Custom code | Custom code | See below |
| `errorMessage` | string | Custom error message | - | `.refine()` | `"Invalid"` |
| `before` | string | Before date | `.Max()` | `.max()` | `"2025-01-01"` |
| `after` | string | After date | `.Min()` | `.min()` | `"2020-01-01"` |
| `unique` | boolean | Unique constraint | Database index | `.refine()` | `true` |
| `email` | boolean | Email format | Custom | `.email()` | `true` |
| `url` | boolean | URL format | Custom | `.url()` | `true` |
| `uuid` | boolean | UUID format | Custom | `.uuid()` | `true` |

## Field Property Reference

### Core Properties

| Property | Type | Description | Example |
|----------|------|-------------|---------|
| `type` | string | **Required**. Field type | `"string"` |
| `label` | string | Display label | `"用户名"` |
| `description` | string | Help text | `"用户登录名"` |
| `default` | any | Default value | `"admin"` |
| `validate` | object | Validation rules | `{ "required": true }` |
| `ui` | object | UI configuration | `{ "widget": "input" }` |

### Advanced Properties

| Property | Type | Description | Example |
|----------|------|-------------|---------|
| `unique` | boolean | Unique constraint | `true` |
| `private` | boolean | Exclude from API | `true` |
| `writable` | boolean | Allow write | `true` |
| `queryable` | boolean | Allow filter | `true` |
| `exportable` | boolean | Include in export | `true` |
| `importable` | boolean | Allow import | `true` |
| `version` | boolean | Enable versioning | `true` |
| `allowedTypes` | array | File type whitelist | `["jpg", "png"]` |
| `$ref` | string | Reference to entity | `"User"` |
| `x-relation` | object | Relationship config | See below |
| `items` | object | Array item schema | `{ "type": "string" }` |
| `properties` | object | Nested object fields | See below |

## Relationship Configuration

### Using `$ref` (Recommended)

```json
{
  "properties": {
    "author": {
      "$ref": "User",
      "label": "作者",
      "x-relation": {
        "type": "many2One",
        "labelField": "nickname",
        "displayFields": ["nickname", "email"]
      }
    }
  }
}
```

### Relationship Types

| Type | Description | Backend Type | Frontend Widget |
|------|-------------|--------------|-----------------|
| `many2One` | Many-to-One | `*User` | Select/AsyncSelect |
| `one2Many` | One-to-Many | `[]*Post` | Table/List |
| `many2Many` | Many-to-Many | `[]*Tag` | Multi-Select/Tags |

### Relationship Options

```json
{
  "x-relation": {
    "type": "many2One",
    "labelField": "name",        // Field to display in select
    "displayFields": ["name", "code"],  // Fields to show in table
    "filter": {"status": "active"},  // Pre-filter options
    "pageSize": 20,               // Pagination size
    "searchable": true,           // Enable search
    "preload": false              // Preload on page load
  }
}
```

## UI Configuration

### Widget Types

| Widget | Type | Use Case |
|--------|------|----------|
| `input` | string | Text input |
| `textarea` | text | Multi-line text |
| `number` | integer/number | Number input |
| `select` | enum | Single select |
| `checkbox` | boolean | Boolean toggle |
| `radio` | enum | Radio buttons |
| `date` | date | Date picker |
| `datetime` | datetime | DateTime picker |
| `password` | password | Password input |
| `email` | email | Email input |
| `url` | url | URL input |
| `file` | file | File upload |
| `image` | image | Image upload |
| `json` | json | JSON editor |
| `editor` | text | Rich text editor |
| `tags` | array | Tag input |
| `switch` | boolean | Switch toggle |

### UI Options

```json
{
  "ui": {
    "widget": "input",
    "placeholder": "Enter value",
    "help": "Helper text",
    "hidden": false,
    "readonly": false,
    "width": "full",  // full | half | third
    "group": "Basic",  // Group name in form
    "order": 1,        // Field order
    "showInTable": true,
    "sortable": true,
    "filterable": true
  }
}
```

## Validation Patterns

### Email Validation
```json
{
  "email": {
    "type": "string",
    "validate": {
      "required": true,
      "format": "email",
      "maxLength": 100
    }
  }
}
```

### Password Validation
```json
{
  "password": {
    "type": "password",
    "validate": {
      "required": true,
      "minLength": 8,
      "pattern": "^(?=.*[a-z])(?=.*[A-Z])(?=.*\\d).+$"
    }
  }
}
```

### Age Validation
```json
{
  "age": {
    "type": "integer",
    "validate": {
      "min": 0,
      "max": 150,
      "nonNegative": true
    }
  }
}
```

### Enum Validation
```json
{
  "role": {
    "type": "enum",
    "enum": ["admin", "editor", "viewer"],
    "validate": {
      "required": true
    }
  }
}
```

### Date Range Validation
```json
{
  "startDate": {
    "type": "date",
    "validate": {
      "required": true,
      "after": "2020-01-01"
    }
  },
  "endDate": {
    "type": "date",
    "validate": {
      "required": true,
      "before": "2030-12-31"
    }
  }
}
```

### Array Validation
```json
{
  "tags": {
    "type": "array",
    "items": {
      "type": "string",
      "validate": {
        "minLength": 2,
        "maxLength": 20
      }
    },
    "validate": {
      "min": 1,
      "max": 10
    }
  }
}
```

### Nested Object Validation
```json
{
  "address": {
    "type": "object",
    "properties": {
      "street": {
        "type": "string",
        "validate": { "required": true }
      },
      "city": {
        "type": "string",
        "validate": { "required": true }
      },
      "zipCode": {
        "type": "string",
        "validate": {
          "pattern": "^\\d{6}$",
          "errorMessage": "Zip code must be 6 digits"
        }
      }
    }
  }
}
```

## Custom Validation

### Backend (Go/Ent)
```go
// In schema.go
func (User) Fields() []ent.Field {
    return []ent.Field{
        field.String("email").
            Validate(func(s string) error {
                if !strings.Contains(s, "@") {
                    return fmt.Errorf("invalid email format")
                }
                return nil
            }),
    }
}
```

### Frontend (Zod)
```typescript
// Auto-generated from schema
const userSchema = z.object({
  email: z.string()
    .email("Invalid email format")
    .max(100, "Email too long")
    .refine((val) => val.endsWith("@company.com"), "Must use company email")
});
```

## Common Patterns

### User Module
```json
{
  "properties": {
    "username": {
      "type": "string",
      "validate": {
        "required": true,
        "minLength": 3,
        "maxLength": 20,
        "pattern": "^[a-zA-Z0-9_]+$"
      }
    },
    "email": {
      "type": "email",
      "validate": {
        "required": true,
        "format": "email",
        "unique": true
      }
    },
    "password": {
      "type": "password",
      "validate": {
        "required": true,
        "minLength": 8
      }
    },
    "status": {
      "type": "enum",
      "enum": ["active", "inactive", "suspended"],
      "default": "active"
    }
  }
}
```

### Product Module
```json
{
  "properties": {
    "name": {
      "type": "string",
      "validate": { "required": true, "maxLength": 100 }
    },
    "price": {
      "type": "number",
      "validate": { "required": true, "min": 0, "nonNegative": true }
    },
    "stock": {
      "type": "integer",
      "validate": { "min": 0, "nonNegative": true }
    },
    "images": {
      "type": "array",
      "items": { "type": "image" },
      "validate": { "max": 5 }
    }
  }
}
```

## Validation Priority

### Backend Validation Layers

1. **Database Level** (Ent Schema)
   - Type constraints
   - Unique indexes
   - Not null

2. **Service Level** (Business Logic)
   - Complex rules
   - Cross-field validation
   - Business invariants

3. **Controller Level** (API Layer)
   - Input sanitization
   - Format validation
   - Permission checks

### Frontend Validation Layers

1. **Field Level** (Zod Schema)
   - Required fields
   - Format validation
   - Length constraints

2. **Form Level** (Form Logic)
   - Cross-field dependencies
   - Conditional validation
   - Async validation

3. **API Level** (Error Handling)
   - Server-side errors
   - Conflict resolution
   - User feedback

## Error Messages

### Default Messages

| Rule | Default Message |
|------|-----------------|
| `required` | "This field is required" |
| `min` | "Must be at least {min}" |
| `max` | "Must be at most {max}" |
| `minLength` | "Must be at least {min} characters" |
| `maxLength` | "Must be at most {max} characters" |
| `pattern` | "Invalid format" |
| `format` | "Invalid {format} format" |
| `unique` | "Already exists" |

### Custom Error Messages

```json
{
  "email": {
    "type": "string",
    "validate": {
      "required": true,
      "format": "email",
      "errorMessage": "Please enter a valid email address"
    }
  },
  "password": {
    "type": "password",
    "validate": {
      "minLength": 8,
      "pattern": "^(?=.*[a-z])(?=.*[A-Z])(?=.*\\d).+$",
      "errorMessage": "Password must contain uppercase, lowercase, and number"
    }
  }
}
```

## Best Practices

### 1. Always Use `label` for Display
```json
// ✅ Good
{ "email": { "type": "string", "label": "邮箱地址" } }

// ❌ Bad
{ "email": { "type": "string", "description": "邮箱地址" } }
```

### 2. Use `description` for Help Text
```json
{
  "email": {
    "type": "string",
    "label": "邮箱地址",
    "description": "We'll send confirmation to this address"
  }
}
```

### 3. Combine `required` with Other Rules
```json
// ✅ Good
{ "validate": { "required": true, "minLength": 8 } }

// ❌ Bad (redundant if required)
{ "validate": { "minLength": 8 } }
```

### 4. Use `unique` for Identifiers
```json
{
  "username": {
    "type": "string",
    "validate": { "required": true, "unique": true }
  }
}
```

### 5. Set Appropriate Defaults
```json
{
  "status": {
    "type": "enum",
    "enum": ["active", "inactive"],
    "default": "active"
  }
}
```

## Complete Example

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "name": "Product",
  "collectionName": "products",
  "description": "Product entity for e-commerce",
  "properties": {
    "name": {
      "type": "string",
      "label": "Product Name",
      "description": "Display name of the product",
      "validate": {
        "required": true,
        "minLength": 2,
        "maxLength": 100
      },
      "ui": {
        "widget": "input",
        "placeholder": "Enter product name",
        "width": "full",
        "showInTable": true,
        "sortable": true
      }
    },
    "price": {
      "type": "number",
      "label": "Price",
      "validate": {
        "required": true,
        "min": 0,
        "nonNegative": true
      },
      "ui": {
        "widget": "number",
        "placeholder": "0.00",
        "width": "half"
      }
    },
    "category": {
      "$ref": "Category",
      "label": "Category",
      "x-relation": {
        "type": "many2One",
        "labelField": "name",
        "searchable": true
      },
      "validate": {
        "required": true
      }
    },
    "tags": {
      "type": "array",
      "label": "Tags",
      "items": {
        "type": "string",
        "validate": {
          "minLength": 2,
          "maxLength": 20
        }
      },
      "validate": {
        "max": 5
      },
      "ui": {
        "widget": "tags"
      }
    },
    "status": {
      "type": "enum",
      "label": "Status",
      "enum": ["draft", "published", "archived"],
      "default": "draft",
      "ui": {
        "widget": "select"
      }
    }
  },
  "indexes": [
    {
      "type": "unique",
      "columns": ["name"]
    }
  ]
}
```

## Quick Reference

### Common Validation Combinations

```json
// Email (required, format, max length)
{ "validate": { "required": true, "format": "email", "maxLength": 100 } }

// Password (required, min length, pattern)
{ "validate": { "required": true, "minLength": 8, "pattern": "^(?=.*[a-z])(?=.*[A-Z])(?=.*\\d).+$" } }

// Username (required, min/max length, pattern, unique)
{ "validate": { "required": true, "minLength": 3, "maxLength": 20, "pattern": "^[a-zA-Z0-9_]+$", "unique": true } }

// Age (integer, range)
{ "validate": { "min": 0, "max": 150, "nonNegative": true } }

// Price (number, positive)
{ "validate": { "required": true, "min": 0, "nonNegative": true } }

// Date range
{ "validate": { "required": true, "after": "2020-01-01", "before": "2030-12-31" } }

// Array (min/max items, item constraints)
{ "validate": { "min": 1, "max": 10 }, "items": { "validate": { "minLength": 2 } } }
```