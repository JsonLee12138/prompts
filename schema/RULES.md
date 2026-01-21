# Schema Skills Rules

## Overview

This document defines the unified rules and conventions for all schema-based skills in this project. These skills work together to provide a complete Schema Driven Development (SDD) workflow.

## Skill Architecture

### Core Skills

```
schema/
├── skills/
│   ├── backend-developer/    # Go backend code generation
│   ├── table-developer/       # React table components
│   ├── form-developer/        # React form components
│   └── code-detector/         # Code quality analysis
```

### Workflow

```
1. Design Schema
   └─> schema-designer (optional)
       └─> entity_schema.json

2. Validate Schema
   └─> schema-validator (optional)
       └─> ✅ Valid

3. Generate Code
   └─> backend-developer
   └─> table-developer
   └─> form-developer

4. Detect Issues
   └─> code-detector
       └─> Fix issues

5. Customize & Test
   └─> Add business logic
   └─> Run tests
```

## Schema Specification

### Entity Schema Structure

```json
{
  "name": "EntityName",
  "description": "Description of the entity",
  "softDelete": false,
  "properties": {
    "fieldName": {
      "type": "string",
      "validate": {
        "required": true,
        "email": true,
        "minLength": 3,
        "maxLength": 100
      },
      "ui": {
        "widget": "input",
        "label": "Field Label",
        "hidden": false
      }
    },
    "category": {
      "$ref": "Category",
      "x-relation": {
        "type": "many2One",
        "labelField": "name"
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
    "export": true,
    "import": false,
    "search": true
  }
}
```

### Field Types

#### Basic Types
- `string` - Text input
- `text` - Textarea
- `integer` - Number input (integer)
- `number` - Number input (float)
- `boolean` - Checkbox
- `enum` - Select dropdown
- `datetime` - Date/time picker
- `password` - Password input
- `uid` - Unique identifier
- `version` - Version number

#### Complex Types
- `json` - JSON editor
- `array` - Array/list
- `object` - Nested object
- `media` - File upload

### Validation Rules

#### Backend (Go)
```go
// Required
validate:"required"

// Email
validate:"email"

// Min/Max length (strings)
validate:"min=3,max=50"

// Range (numbers)
validate:"min=0,max=150"

// Enum
validate:"oneof=admin editor viewer"

// Pattern
validate:"regex=^.+@.+$"

// Optional
// No validation, use omitempty in struct tag
```

#### Frontend (TypeScript/Zod)
```typescript
// Required
z.string()

// Email
z.string().email()

// Min/Max length (strings)
z.string().min(3).max(50)

// Range (numbers)
z.number().int().min(0).max(150)

// Enum
z.enum(["admin", "editor", "viewer"])

// Optional
z.string().optional()
```

### Relationships

#### many2One (Foreign Key)
```json
{
  "author": {
    "$ref": "User",
    "x-relation": { "type": "many2One", "labelField": "name" }
  }
}
```

**Backend:**
- DTO: `AuthorID string`
- Service: `SetAuthorID(dto.AuthorID)`
- Schema: `field.String("author_id")`

**Frontend:**
- Type: `authorId: string`
- Form: Single select dropdown
- Table: Link to author

#### one2Many (Reverse Relation)
```json
{
  "posts": {
    "$ref": "Post",
    "x-relation": { "type": "one2Many", "labelField": "title" }
  }
}
```

**Backend:**
- Service: `WithPosts()` for eager loading
- Controller: Optional preload

**Frontend:**
- Type: `posts: Post[]`
- Table: Expandable rows or sub-table

#### many2Many (Through Table)
```json
{
  "roles": {
    "$ref": "Role",
    "x-relation": { "type": "many2Many", "labelField": "name" }
  }
}
```

**Backend:**
- DTO: `RoleIDs []string`
- Service: `AddRoleIDs(dto.RoleIDs...)`
- Schema: Separate through table

**Frontend:**
- Type: `roleIds: string[]`
- Form: Multi-select or checkbox group
- Table: Tag list

#### one2One (Unique Relation)
```json
{
  "profile": {
    "$ref": "Profile",
    "x-relation": { "type": "one2One" }
  }
}
```

**Backend:**
- Service: `WithProfile()` for eager loading
- Schema: Unique edge

**Frontend:**
- Type: `profile: Profile`
- Form: Nested form

### UI Configuration

#### Widgets
- `input` - Text input
- `textarea` - Textarea
- `number` - Number input
- `select` - Dropdown
- `checkbox` - Checkbox
- `radio` - Radio buttons
- `date` - Date picker
- `datetime` - DateTime picker
- `file` - File upload
- `color` - Color picker
- `range` - Range slider

#### Layout
```json
{
  "ui": {
    "widget": "input",
    "label": "Email Address",
    "placeholder": "user@example.com",
    "helpText": "Enter a valid email",
    "hidden": false,
    "readonly": false,
    "grid": {
      "colSpan": 6,
      "row": 1
    }
  }
}
```

### Indexes

#### Unique Index
```json
{
  "type": "unique",
  "columns": ["email"]
}
```

**Backend:** `index.Fields("email").Unique()`

#### Regular Index
```json
{
  "type": "index",
  "columns": ["created_at"]
}
```

**Backend:** `index.Fields("created_at")`

#### Composite Index
```json
{
  "type": "index",
  "columns": ["status", "created_at"]
}
```

**Backend:** `index.Fields("status", "created_at")`

### Features

```json
{
  "features": {
    "export": true,
    "import": false,
    "search": true,
    "filter": true,
    "sort": true,
    "pagination": true,
    "bulkActions": false
  }
}
```

## Generation Rules

### Backend (Go)

#### 1. DTO Generation
```go
type CreateDTO struct {
    // Required fields
    Email    string `json:"email" validate:"required,email,max=100"`
    Password string `json:"password" validate:"required,min=6,max=72"`
    Name     string `json:"name" validate:"required,max=50"`

    // Optional fields
    Phone    string `json:"phone,omitempty"`
    Age      int    `json:"age,omitempty" validate:"min=0,max=150"`

    // Relationships
    AuthorID string `json:"authorId,omitempty"`
    RoleIDs  []string `json:"roleIds,omitempty"`
}
```

#### 2. Service Generation
```go
func (s *Service) Create(ctx context.Context, dto *CreateDTO) (*_gen.User, error) {
    // Password hashing
    hashedPassword, err := bcrypt.GenerateFromPassword([]byte(dto.Password), bcrypt.DefaultCost)
    if err != nil {
        return nil, err
    }

    // Build entity
    builder := s.client.User.Create().
        SetEmail(dto.Email).
        SetPassword(string(hashedPassword)).
        SetName(dto.Name).
        SetRole(user.Role(dto.Role))

    // Optional fields
    if dto.Phone != "" {
        builder.SetPhone(dto.Phone)
    }

    // Relationships
    if dto.AuthorID != "" {
        builder.SetAuthorID(dto.AuthorID)
    }

    if len(dto.RoleIDs) > 0 {
        builder.AddRoleIDs(dto.RoleIDs...)
    }

    return builder.Save(ctx)
}
```

#### 3. Controller Generation
```go
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

    res.Write(http.StatusOK, responder.StrapiResponse{
        Data: map[string]any{
            "id":    user.ID,
            "email": user.Email,
            "name":  user.Name,
        },
    })
}
```

#### 4. Module Generation
```go
func (m *Module) Setup(r chi.Router) {
    r.Route("/users", func(r chi.Router) {
        r.Get("/", m.controller.List)
        r.Get("/{id}", m.controller.Get)
        r.Post("/", m.controller.Create)
        r.Put("/{id}", m.controller.Update)
        r.Delete("/{id}", m.controller.Delete)
    })
}
```

#### 5. Ent Schema Generation
```go
func (User) Fields() []ent.Field {
    return []ent.Field{
        field.String("email").Unique().NotEmpty(),
        field.String("password").Sensitive().NotEmpty(),
        field.String("name").NotEmpty().MaxLen(50),
        field.Int("age").Range(0, 150),
        field.Enum("role").Values("admin", "editor", "viewer"),
        field.String("phone").Optional(),
        field.Time("deleted_at").Optional().Nillable(),
    }
}

func (User) Indexes() []ent.Index {
    return []ent.Index{
        index.Fields("email").Unique(),
    }
}
```

### Frontend (TypeScript/React)

#### 1. Type Definitions
```typescript
export interface User {
  id: string;
  email: string;
  name: string;
  age?: number;
  role: 'admin' | 'editor' | 'viewer';
  phone?: string;
  authorId?: string;
  roleIds?: string[];
}

export interface CreateUser extends Omit<User, 'id'> {
  password: string;
}
```

#### 2. API Client
```typescript
export class UserAPI {
  async create(data: CreateUser): Promise<User> {
    const response = await fetch('/api/users', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.message || 'Failed to create user');
    }

    return response.json();
  }

  async list(params?: { page?: number; search?: string }): Promise<User[]> {
    const url = new URL('/api/users');
    if (params?.page) url.searchParams.set('page', params.page.toString());
    if (params?.search) url.searchParams.set('search', params.search);

    const response = await fetch(url);
    return response.json();
  }

  async get(id: string): Promise<User> {
    const response = await fetch(`/api/users/${id}`);
    return response.json();
  }

  async update(id: string, data: Partial<User>): Promise<User> {
    const response = await fetch(`/api/users/${id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    return response.json();
  }

  async delete(id: string): Promise<void> {
    const response = await fetch(`/api/users/${id}`, {
      method: 'DELETE',
    });
    if (!response.ok) throw new Error('Failed to delete');
  }
}

export const userAPI = new UserAPI();
```

#### 3. Zod Schema
```typescript
import { z } from 'zod';

export const createUserSchema = z.object({
  email: z.string().email().max(100),
  password: z.string().min(6).max(72),
  name: z.string().max(50),
  age: z.number().int().min(0).max(150).optional(),
  role: z.enum(['admin', 'editor', 'viewer']),
  phone: z.string().optional(),
  authorId: z.string().optional(),
  roleIds: z.array(z.string()).optional(),
});

export const updateUserSchema = createUserSchema.partial();

export type CreateUser = z.infer<typeof createUserSchema>;
export type UpdateUser = z.infer<typeof updateUserSchema>;
```

#### 4. Form Component
```typescript
import { useForm, Controller } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { createUserSchema, CreateUser } from '../schemas/user';
import { userAPI } from '../lib/api/user';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { toast } from '@/hooks/use-toast';

export function UserForm({ user, onSuccess }: { user?: User; onSuccess?: () => void }) {
  const { register, control, handleSubmit, formState: { errors, isSubmitting } } = useForm<CreateUser>({
    resolver: zodResolver(createUserSchema),
    defaultValues: user,
  });

  const onSubmit = async (data: CreateUser) => {
    try {
      if (user) {
        await userAPI.update(user.id, data);
        toast.success('User updated');
      } else {
        await userAPI.create(data);
        toast.success('User created');
      }
      onSuccess?.();
    } catch (error) {
      toast.error(error.message);
    }
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
      <div>
        <label>Email</label>
        <Input
          type="email"
          {...register('email')}
          disabled={isSubmitting}
        />
        {errors.email && <span className="text-red-500">{errors.email.message}</span>}
      </div>

      {!user && (
        <div>
          <label>Password</label>
          <Input
            type="password"
            {...register('password')}
            disabled={isSubmitting}
          />
          {errors.password && <span className="text-red-500">{errors.password.message}</span>}
        </div>
      )}

      <div>
        <label>Name</label>
        <Input
          {...register('name')}
          disabled={isSubmitting}
        />
        {errors.name && <span className="text-red-500">{errors.name.message}</span>}
      </div>

      <div>
        <label>Role</label>
        <Controller
          name="role"
          control={control}
          render={({ field }) => (
            <select {...field} disabled={isSubmitting}>
              <option value="admin">Admin</option>
              <option value="editor">Editor</option>
              <option value="viewer">Viewer</option>
            </select>
          )}
        />
        {errors.role && <span className="text-red-500">{errors.role.message}</span>}
      </div>

      <Button type="submit" disabled={isSubmitting}>
        {isSubmitting ? 'Saving...' : user ? 'Update' : 'Create'}
      </Button>
    </form>
  );
}
```

#### 5. Table Component
```typescript
import { useState, useEffect } from 'react';
import { User } from '@/types/user';
import { userAPI } from '@/lib/api/user';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table';

export function UserTable() {
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');

  useEffect(() => {
    loadUsers();
  }, [search]);

  const loadUsers = async () => {
    setLoading(true);
    try {
      const data = await userAPI.list({ search });
      setUsers(data);
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id: string) => {
    if (!confirm('Are you sure?')) return;
    await userAPI.delete(id);
    loadUsers();
  };

  if (loading) return <div>Loading...</div>;
  if (users.length === 0) return <div>No users found</div>;

  return (
    <div className="space-y-4">
      <Input
        placeholder="Search users..."
        value={search}
        onChange={(e) => setSearch(e.target.value)}
      />

      <Table>
        <TableHeader>
          <TableRow>
            <TableHead>Email</TableHead>
            <TableHead>Name</TableHead>
            <TableHead>Role</TableHead>
            <TableHead>Actions</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {users.map(user => (
            <TableRow key={user.id}>
              <TableCell>{user.email}</TableCell>
              <TableCell>{user.name}</TableCell>
              <TableCell>{user.role}</TableCell>
              <TableCell>
                <Button variant="outline" size="sm">Edit</Button>
                <Button variant="destructive" size="sm" onClick={() => handleDelete(user.id)}>
                  Delete
                </Button>
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </div>
  );
}
```

## Quality Standards

### Backend Quality Checklist

- [ ] All required fields in DTO
- [ ] Validation tags match schema
- [ ] Password hashing implemented
- [ ] Optional fields checked
- [ ] Relationships handled correctly
- [ ] Soft delete implemented (if enabled)
- [ ] Unique constraints validated
- [ ] Error handling in controllers
- [ ] JSON binding validation
- [ ] Consistent response format
- [ ] Indexes defined
- [ ] Ent schema complete

### Frontend Quality Checklist

- [ ] Zod schema matches entity
- [ ] All fields in types
- [ ] API methods complete
- [ ] Form validation working
- [ ] Error messages displayed
- [ ] Loading states present
- [ ] Empty states handled
- [ ] Table columns complete
- [ ] Search/filter implemented
- [ ] Pagination working
- [ ] Export functionality (if enabled)
- [ ] Type safety maintained

### Code Detection Checklist

- [ ] Run detection after generation
- [ ] Fix all errors
- [ ] Review warnings
- [ ] Add custom business logic
- [ ] Write tests
- [ ] Update documentation

## Common Patterns

### User Management
```json
{
  "name": "User",
  "properties": {
    "email": { "type": "string", "validate": { "required": true, "email": true } },
    "password": { "type": "password", "validate": { "required": true, "minLength": 6 } },
    "name": { "type": "string", "validate": { "required": true, "maxLength": 50 } },
    "age": { "type": "integer", "validate": { "min": 0, "max": 150 } },
    "role": { "type": "enum", "validate": { "enum": ["admin", "editor", "viewer"] } }
  },
  "indexes": [{ "type": "unique", "columns": ["email"] }]
}
```

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

### E-commerce
```json
{
  "name": "Product",
  "properties": {
    "name": { "type": "string", "validate": { "required": true } },
    "price": { "type": "number", "validate": { "required": true, "min": 0 } },
    "stock": { "type": "integer", "validate": { "min": 0 } },
    "category": { "$ref": "Category", "x-relation": { "type": "many2One" } }
  },
  "features": { "export": true, "search": true, "filter": true }
}
```

## Integration

### CI/CD Pipeline
```yaml
# .github/workflows/schema-validation.yml
name: Schema Quality Check

on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Validate Schema
        run: |
          python skills/schema-validator/scripts/validate_schema.py schema.json

      - name: Generate Code
        run: |
          python skills/backend-developer/scripts/generate_go.py schema.json --output ./backend
          python skills/table-developer/scripts/generate_table.py schema.json --output ./frontend
          python skills/form-developer/scripts/generate_form.py schema.json --output ./frontend

      - name: Detect Issues
        run: |
          python skills/code-detector/scripts/analyze_all.py ./backend ./frontend --schema schema.json
```

### Pre-commit Hook
```bash
#!/bin/bash
# .git/hooks/pre-commit

# Validate schema
python skills/schema-validator/scripts/validate_schema.py schema.json
if [ $? -ne 0 ]; then exit 1; fi

# Detect code issues
python skills/code-detector/scripts/analyze_all.py ./backend ./frontend --schema schema.json
if [ $? -ne 0 ]; then exit 1; fi

echo "✅ All checks passed!"
```

## Troubleshooting

### Common Issues

#### 1. Generation Fails
**Solution:** Validate schema first
```bash
python skills/schema-validator/scripts/validate_schema.py schema.json
```

#### 2. Missing Fields
**Solution:** Check schema properties and regenerate

#### 3. Relationship Errors
**Solution:** Verify $ref and x-relation.type

#### 4. Validation Not Working
**Solution:** Check struct tags and Zod schemas match

#### 5. Code Quality Issues
**Solution:** Run code detector and fix reported issues

## Best Practices

### 1. Always Validate Schema First
```bash
python skills/schema-validator/scripts/validate_schema.py schema.json
```

### 2. Use Templates for Common Patterns
```bash
python skills/schema-designer/scripts/quick_design.py --template user --name User
```

### 3. Generate Then Detect
```bash
# Generate
python skills/backend-developer/scripts/generate_go.py schema.json --output ./backend

# Detect issues
python skills/code-detector/scripts/detect_backend.py ./backend --schema schema.json
```

### 4. Review Before Committing
- Check generated code
- Add business logic
- Write tests
- Update documentation

### 5. Keep Schemas in Version Control
```bash
git add schema.json
git commit -m "feat: update user schema"
```

## Related Resources

- [Entity Schema Specification](entity_schema.json)
- [Schema Driven Development](SCHEMA_DRIVEN_DEVELOPMENT.md)
- [Backend Developer Skill](skills/backend-developer/SKILL.md)
- [Table Developer Skill](skills/table-developer/SKILL.md)
- [Form Developer Skill](skills/form-developer/SKILL.md)
- [Code Detector Skill](skills/code-detector/SKILL.md)

---

**Last Updated:** 2026-01-14
**Version:** 2.0
