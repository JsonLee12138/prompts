#!/usr/bin/env python3
"""
Go Code Generator - Generate Go backend code from schema
"""

import json
import sys
import os
from pathlib import Path
from typing import Dict, List, Any


class GoCodeGenerator:
    """Generate Go backend code from schema"""

    def __init__(self, schema_path: str, output_dir: str):
        self.schema_path = schema_path
        self.output_dir = Path(output_dir)
        self.schema = self._load_schema()

    def _load_schema(self) -> Dict:
        """Load schema from file"""
        with open(self.schema_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _get_entity_name(self) -> str:
        """Get entity name (lowercase for package)"""
        return self.schema.get('name', 'entity').lower()

    def _get_pascal_name(self) -> str:
        """Get entity name in PascalCase"""
        return self.schema.get('name', 'Entity')

    def _generate_validation_tag(self, validate: Dict) -> str:
        """Generate Go validation tag from validate rules"""
        tags = []

        if validate.get('required'):
            tags.append('required')

        if validate.get('format') == 'email':
            tags.append('email')

        if validate.get('format') == 'phone':
            tags.append('phone')

        if validate.get('min') is not None:
            tags.append(f'min={validate["min"]}')

        if validate.get('max') is not None:
            tags.append(f'max={validate["max"]}')

        if validate.get('length') is not None:
            tags.append(f'min={validate["length"]},max={validate["length"]}')

        if validate.get('pattern'):
            tags.append(f'regex={validate["pattern"]}')

        if validate.get('enum'):
            enum_values = ' '.join(validate['enum'])
            tags.append(f'oneof={enum_values}')

        if validate.get('positive'):
            tags.append('min=1')

        if validate.get('nonNegative'):
            tags.append('min=0')

        if validate.get('integer'):
            tags.append('number')

        return ','.join(tags) if tags else ''

    def _get_field_type(self, field_name: str, field_def: Dict) -> str:
        """Get Go type for field"""
        # Relationship field
        if '$ref' in field_def:
            relation_type = field_def['x-relation']['type']
            if relation_type in ['one2Many', 'many2Many']:
                return f'[]*{field_def["$ref"]}'
            else:
                return f'*{field_def["$ref"]}'

        # Regular field
        field_type = field_def.get('type', 'string')

        type_map = {
            'string': 'string',
            'text': 'string',
            'password': 'string',
            'email': 'string',
            'uid': 'string',
            'integer': 'int',
            'number': 'float64',
            'boolean': 'bool',
            'enum': 'string',
            'datetime': 'time.Time',
            'date': 'time.Time',
            'json': 'map[string]any',
            'media': 'string',
            'richText': 'string',
            'array': '[]any',
            'object': 'map[string]any',
        }

        return type_map.get(field_type, 'string')

    def _is_optional(self, field_def: Dict) -> bool:
        """Check if field is optional"""
        validate = field_def.get('validate', {})
        return not validate.get('required', False)

    def _is_private(self, field_def: Dict) -> bool:
        """Check if field is private"""
        return field_def.get('private', False)

    def _is_password(self, field_def: Dict) -> bool:
        """Check if field is password"""
        return field_def.get('type') == 'password'

    def _has_relationship(self) -> bool:
        """Check if schema has relationship fields"""
        properties = self.schema.get('properties', {})
        return any('$ref' in prop for prop in properties.values())

    def _get_relationship_fields(self) -> List[Dict[str, Any]]:
        """Get all relationship fields"""
        properties = self.schema.get('properties', {})
        rel_fields = []

        for name, prop in properties.items():
            if '$ref' in prop:
                rel_fields.append({
                    'name': name,
                    'ref': prop['$ref'],
                    'relation': prop.get('x-relation', {}),
                })

        return rel_fields

    def generate_dto(self) -> str:
        """Generate DTO file"""
        entity_name = self._get_pascal_name()
        properties = self.schema.get('properties', {})

        # Create DTO
        create_fields = []
        update_fields = []

        for field_name, field_def in properties.items():
            # Skip private fields
            if self._is_private(field_def):
                continue

            # Skip relationship fields in DTO (handled by Ent)
            if '$ref' in field_def:
                continue

            field_type = self._get_field_type(field_name, field_def)
            json_tag = field_name
            validate = field_def.get('validate', {})
            validation_tag = self._generate_validation_tag(validate)
            is_optional = self._is_optional(field_def)

            # Create field
            create_tags = [f'json:"{json_tag}"']
            if validation_tag:
                create_tags.append(f'validate:"{validation_tag}"')

            create_field = f'    {field_name.capitalize()} {field_type} `{" ".join(create_tags)}`'
            create_fields.append(create_field)

            # Update field (all optional)
            if not is_optional:
                update_tags = [f'json:"{json_tag},omitempty"']
                if validation_tag:
                    update_tags.append(f'validate:"{validation_tag}"')
                update_field = f'    {field_name.capitalize()} {field_type} `{" ".join(update_tags)}`'
                update_fields.append(update_field)

        dto_content = f"""package {entity_name.lower()}

import "github.com/go-playground/validator/v10"

// CreateDTO - Data transfer object for creating {entity_name}
type CreateDTO struct {{
{chr(10).join(create_fields)}
}}

// UpdateDTO - Data transfer object for updating {entity_name}
type UpdateDTO struct {{
{chr(10).join(update_fields) if update_fields else '    // Add update fields as needed'}
}}
"""
        return dto_content

    def generate_service(self) -> str:
        """Generate Service file"""
        entity_name = self._get_pascal_name()
        entity_lower = entity_name.lower()
        has_password = any(self._is_password(prop) for prop in self.schema.get('properties', {}).values())
        has_relationship = self._has_relationship()

        # Import section
        imports = [
            '"context"',
            f'"github.com/JsonLee12138/headless-cms/cms/_gen"',
        ]

        if has_password:
            imports.append('"golang.org/x/crypto/bcrypt"')

        if has_relationship:
            imports.append(f'"github.com/JsonLee12138/headless-cms/cms/_gen/{entity_lower}"')

        # Create method
        create_lines = []
        properties = self.schema.get('properties', {})

        if has_password:
            create_lines.append('    // Hash password')
            create_lines.append('    hashedPassword, err := bcrypt.GenerateFromPassword([]byte(dto.Password), bcrypt.DefaultCost)')
            create_lines.append('    if err != nil {')
            create_lines.append('        return nil, err')
            create_lines.append('    }')
            create_lines.append('')

        create_lines.append(f'    return s.client.{entity_name}.Create()')

        for field_name, field_def in properties.items():
            if self._is_private(field_def) or '$ref' in field_def:
                continue

            field_type = field_def.get('type')
            if field_type == 'password':
                create_lines.append(f'        Set{field_name.capitalize()}(string(hashedPassword))')
            elif field_type == 'enum':
                create_lines.append(f'        Set{field_name.capitalize()}({entity_lower}.{entity_name}("{field_def.get('validate', {}).get('enum', [''])[0]}"))')
            else:
                create_lines.append(f'        Set{field_name.capitalize()}(dto.{field_name.capitalize()})')

        create_lines.append('        Save(ctx)')

        service_content = f"""package {entity_lower}

import (
{chr(10).join(f'    {imp}' for imp in imports)}
)

type Service struct {{
    client *_gen.Client
}}

func NewService(client *_gen.Client) *Service {{
    return &Service{{client: client}}
}}

func (s *Service) Create(ctx context.Context, dto *CreateDTO) (*_gen.{entity_name}, error) {{
{chr(10).join(create_lines)}
}}

func (s *Service) Update(ctx context.Context, id string, dto *UpdateDTO) (*_gen.{entity_name}, error) {{
    builder := s.client.{entity_name}.UpdateOneID(id)

    // Set fields if provided
{chr(10).join([f'    if dto.{f.capitalize()} != {self._get_default_value(f, d)} {{ builder.Set{f.capitalize()}(dto.{f.capitalize()}) }}'
               for f, d in properties.items()
               if not self._is_private(d) and '$ref' not in d and not self._is_optional(d)])}

    return builder.Save(ctx)
}}

func (s *Service) Delete(ctx context.Context, id string) error {{
    return s.client.{entity_name}.DeleteOneID(id).Exec(ctx)
}}

func (s *Service) Get(ctx context.Context, id string) (*_gen.{entity_name}, error) {{
    return s.client.{entity_name}.Get(ctx, id)
}}

func (s *Service) List(ctx context.Context, page, pageSize int) ([]*_gen.{entity_name}, error) {{
    return s.client.{entity_name}.Query().
        Offset((page - 1) * pageSize).
        Limit(pageSize).
        All(ctx)
}}
"""
        return service_content

    def _get_default_value(self, field_name: str, field_def: Dict) -> str:
        """Get default value for type"""
        field_type = field_def.get('type', 'string')
        if field_type in ['integer', 'number']:
            return '0'
        elif field_type == 'boolean':
            return 'false'
        return '""'

    def generate_controller(self) -> str:
        """Generate Controller file"""
        entity_name = self._get_pascal_name()
        entity_lower = entity_name.lower()

        controller_content = f"""package {entity_lower}

import (
    "net/http"
    "github.com/go-chi/chi/v5"
    "github.com/JsonLee12138/headless-cms/core/http/binding"
    "github.com/JsonLee12138/headless-cms/core/http/responder"
)

type Controller struct {{
    service          *Service
    responderFactory *responder.ResponderFactory
}}

func NewController(service *Service, factory *responder.ResponderFactory) *Controller {{
    return &Controller{{service: service, responderFactory: factory}}
}}

func (c *Controller) Create(w http.ResponseWriter, r *http.Request) {{
    res := c.responderFactory.FromRequest(w, r)

    var dto CreateDTO
    if err := binding.JSON(r, &dto); err != nil {{
        res.WriteError(http.StatusBadRequest, responder.Error{{Message: err.Error()}})
        return
    }}

    entity, err := c.service.Create(r.Context(), &dto)
    if err != nil {{
        res.WriteError(http.StatusInternalServerError, responder.Error{{Message: err.Error()}})
        return
    }}

    res.Write(http.StatusOK, responder.StrapiResponse{{
        Data: map[string]any{{
            "id": entity.ID,
        }},
    }})
}}

func (c *Controller) Update(w http.ResponseWriter, r *http.Request) {{
    res := c.responderFactory.FromRequest(w, r)

    id := chi.URLParam(r, "id")
    if id == "" {{
        res.WriteError(http.StatusBadRequest, responder.Error{{Message: "ID is required"}})
        return
    }}

    var dto UpdateDTO
    if err := binding.JSON(r, &dto); err != nil {{
        res.WriteError(http.StatusBadRequest, responder.Error{{Message: err.Error()}})
        return
    }}

    entity, err := c.service.Update(r.Context(), id, &dto)
    if err != nil {{
        res.WriteError(http.StatusInternalServerError, responder.Error{{Message: err.Error()}})
        return
    }}

    res.Write(http.StatusOK, responder.StrapiResponse{{
        Data: map[string]any{{
            "id": entity.ID,
        }},
    }})
}}

func (c *Controller) Get(w http.ResponseWriter, r *http.Request) {{
    res := c.responderFactory.FromRequest(w, r)

    id := chi.URLParam(r, "id")
    if id == "" {{
        res.WriteError(http.StatusBadRequest, responder.Error{{Message: "ID is required"}})
        return
    }}

    entity, err := c.service.Get(r.Context(), id)
    if err != nil {{
        res.WriteError(http.StatusNotFound, responder.Error{{Message: "Not found"}})
        return
    }}

    res.Write(http.StatusOK, responder.StrapiResponse{{
        Data: entity,
    }})
}}

func (c *Controller) Delete(w http.ResponseWriter, r *http.Request) {{
    res := c.responderFactory.FromRequest(w, r)

    id := chi.URLParam(r, "id")
    if id == "" {{
        res.WriteError(http.StatusBadRequest, responder.Error{{Message: "ID is required"}})
        return
    }}

    if err := c.service.Delete(r.Context(), id); err != nil {{
        res.WriteError(http.StatusInternalServerError, responder.Error{{Message: err.Error()}})
        return
    }}

    res.Write(http.StatusOK, responder.StrapiResponse{{
        Data: map[string]any{{"success": true}},
    }})
}}

func (c *Controller) List(w http.ResponseWriter, r *http.Request) {{
    res := c.responderFactory.FromRequest(w, r)

    entities, err := c.service.List(r.Context(), 1, 20)
    if err != nil {{
        res.WriteError(http.StatusInternalServerError, responder.Error{{Message: err.Error()}})
        return
    }}

    res.Write(http.StatusOK, responder.StrapiResponse{{
        Data: entities,
    }})
}}
"""
        return controller_content

    def generate_module(self) -> str:
        """Generate Module file"""
        entity_name = self._get_pascal_name()
        entity_lower = entity_name.lower()

        module_content = f"""package {entity_lower}

import (
    "github.com/JsonLee12138/headless-cms/cms/_gen"
    "github.com/JsonLee12138/headless-cms/core/http/responder"
    "github.com/go-chi/chi/v5"
)

type Module struct {{
    controller *Controller
    service    *Service
}}

func NewModule(client *_gen.Client) *Module {{
    service := NewService(client)
    responderFactory := responder.NewResponderFactory(responder.DefaultPanicFn)
    controller := NewController(service, responderFactory)

    return &Module{{
        controller: controller,
        service:    service,
    }}
}}

func (m *Module) Setup(r chi.Router) {{
    r.Route("/{entity_lower}s", func(r chi.Router) {{
        r.Get("/", m.controller.List)
        r.Get("/{id}", m.controller.Get)
        r.Post("/", m.controller.Create)
        r.Put("/{id}", m.controller.Update)
        r.Delete("/{id}", m.controller.Delete)
    }})
}}
"""
        return module_content

    def generate_all(self) -> Dict[str, str]:
        """Generate all files"""
        return {
            'dto.go': self.generate_dto(),
            'service.go': self.generate_service(),
            'controller.go': self.generate_controller(),
            'module.go': self.generate_module(),
        }

    def write_files(self) -> None:
        """Write generated files to output directory"""
        entity_lower = self._get_entity_name()
        output_path = self.output_dir / entity_lower

        # Create directory
        output_path.mkdir(parents=True, exist_ok=True)

        # Generate and write files
        files = self.generate_all()

        for filename, content in files.items():
            file_path = output_path / filename
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Generated: {file_path}")

        print(f"\n🎉 Generation complete! Files written to: {output_path}")


def main():
    """Main entry point"""
    if len(sys.argv) < 3:
        print("Usage: python generate_go.py <schema_path> <output_dir>")
        sys.exit(1)

    schema_path = sys.argv[1]
    output_dir = sys.argv[2]

    if not os.path.exists(schema_path):
        print(f"Error: Schema file not found: {schema_path}")
        sys.exit(1)

    generator = GoCodeGenerator(schema_path, output_dir)
    generator.write_files()


if __name__ == "__main__":
    main()