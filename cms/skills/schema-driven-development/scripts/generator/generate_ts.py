#!/usr/bin/env python3
"""
TypeScript Code Generator - Generate frontend code from schema
"""

import json
import sys
import os
from pathlib import Path
from typing import Dict, List, Any


class TSCodeGenerator:
    """Generate TypeScript/React code from schema"""

    def __init__(self, schema_path: str, output_dir: str):
        self.schema_path = schema_path
        self.output_dir = Path(output_dir)
        self.schema = self._load_schema()

    def _load_schema(self) -> Dict:
        """Load schema from file"""
        with open(self.schema_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _get_entity_name(self) -> str:
        """Get entity name"""
        return self.schema.get('name', 'Entity')

    def _get_field_type(self, field_def: Dict) -> str:
        """Get TypeScript type for field"""
        if '$ref' in field_def:
            # Relationship
            rel_type = field_def['x-relation']['type']
            if rel_type in ['one2Many', 'many2Many']:
                return f'{field_def["$ref"]}[]'
            else:
                return field_def["$ref"]

        field_type = field_def.get('type', 'string')

        type_map = {
            'string': 'string',
            'text': 'string',
            'password': 'string',
            'email': 'string',
            'uid': 'string',
            'integer': 'number',
            'number': 'number',
            'boolean': 'boolean',
            'enum': 'string',
            'datetime': 'string',
            'date': 'string',
            'json': 'any',
            'media': 'string',
            'richText': 'string',
            'array': 'any[]',
            'object': 'Record<string, any>',
        }

        return type_map.get(field_type, 'string')

    def _is_optional(self, field_def: Dict) -> bool:
        """Check if field is optional"""
        validate = field_def.get('validate', {})
        return not validate.get('required', False)

    def _is_private(self, field_def: Dict) -> bool:
        """Check if field is private"""
        return field_def.get('private', False)

    def generate_types(self) -> str:
        """Generate TypeScript types"""
        entity_name = self._get_entity_name()
        properties = self.schema.get('properties', {})

        # Main interface
        lines = [f"// Types for {entity_name}", "", f"export interface {entity_name} {{"]

        for field_name, field_def in properties.items():
            if self._is_private(field_def):
                continue

            field_type = self._get_field_type(field_def)
            optional = "?" if self._is_optional(field_def) else ""
            lines.append(f"  {field_name}{optional}: {field_type};")

        lines.append("}")
        lines.append("")

        # Create DTO
        lines.append(f"export interface Create{entity_name}DTO {{")

        for field_name, field_def in properties.items():
            if self._is_private(field_def) or '$ref' in field_def:
                continue

            field_type = self._get_field_type(field_def)
            validate = field_def.get('validate', {})
            required = validate.get('required', False)

            if not required:
                lines.append(f"  {field_name}?: {field_type};")
            else:
                lines.append(f"  {field_name}: {field_type};")

        lines.append("}")
        lines.append("")

        # Update DTO
        lines.append(f"export interface Update{entity_name}DTO {{")

        for field_name, field_def in properties.items():
            if self._is_private(field_def) or '$ref' in field_def:
                continue

            field_type = self._get_field_type(field_def)
            lines.append(f"  {field_name}?: {field_type};")

        lines.append("}")

        return "\n".join(lines)

    def generate_api(self) -> str:
        """Generate API client"""
        entity_name = self._get_entity_name()
        entity_lower = entity_name.lower()

        api_content = f"""import {{ {entity_name}, Create{entity_name}DTO, Update{entity_name}DTO }} from '@/types/{entity_lower}';

export class {entity_name}API {{
  private baseURL = '/api/{entity_lower}s';

  async list(params?: {{ page?: number; pageSize?: number }}): Promise<{entity_name}[]> {{
    const url = new URL(this.baseURL);
    if (params?.page) url.searchParams.set('page', params.page.toString());
    if (params?.pageSize) url.searchParams.set('pageSize', params.pageSize.toString());

    const response = await fetch(url.toString());
    if (!response.ok) throw new Error('Failed to fetch');
    const {{ data }} = await response.json();
    return data;
  }}

  async get(id: string): Promise<{entity_name}> {{
    const response = await fetch(`${{this.baseURL}}/${{id}}`);
    if (!response.ok) throw new Error('Not found');
    const {{ data }} = await response.json();
    return data;
  }}

  async create(dto: Create{entity_name}DTO): Promise<{entity_name}> {{
    const response = await fetch(this.baseURL, {{
      method: 'POST',
      headers: {{ 'Content-Type': 'application/json' }},
      body: JSON.stringify(dto),
    }});
    if (!response.ok) throw new Error('Create failed');
    const {{ data }} = await response.json();
    return data;
  }}

  async update(id: string, dto: Update{entity_name}DTO): Promise<{entity_name}> {{
    const response = await fetch(`${{this.baseURL}}/${{id}}`, {{
      method: 'PUT',
      headers: {{ 'Content-Type': 'application/json' }},
      body: JSON.stringify(dto),
    }});
    if (!response.ok) throw new Error('Update failed');
    const {{ data }} = await response.json();
    return data;
  }}

  async delete(id: string): Promise<void> {{
    const response = await fetch(`${{this.baseURL}}/${{id}}`, {{ method: 'DELETE' }});
    if (!response.ok) throw new Error('Delete failed');
  }}
}}

export const {entity_lower}API = new {entity_name}API();
"""
        return api_content

    def generate_form(self) -> str:
        """Generate form component"""
        entity_name = self._get_entity_name()
        entity_lower = entity_name.lower()
        properties = self.schema.get('properties', {})

        # Build Zod schema
        zod_lines = [f"const schema = z.object({{"]

        for field_name, field_def in properties.items():
            if self._is_private(field_def) or '$ref' in field_def:
                continue

            validate = field_def.get('validate', {})
            field_type = field_def.get('type', 'string')

            # Build Zod chain
            zod_chain = []

            if field_type in ['string', 'text', 'password', 'email']:
                zod_chain.append('z.string()')
                if validate.get('format') == 'email':
                    zod_chain.append('.email("Invalid email")')
                if validate.get('min'):
                    zod_chain.append(f'.min({validate["min"]})')
                if validate.get('max'):
                    zod_chain.append(f'.max({validate["max"]})')
                if validate.get('pattern'):
                    zod_chain.append(f'.regex(/{validate["pattern"]}/)')
            elif field_type in ['integer', 'number']:
                zod_chain.append('z.number()')
                if validate.get('min') is not None:
                    zod_chain.append(f'.min({validate["min"]})')
                if validate.get('max') is not None:
                    zod_chain.append(f'.max({validate["max"]})')
            elif field_type == 'boolean':
                zod_chain.append('z.boolean()')
            elif field_type == 'enum':
                enum_values = validate.get('enum', [])
                enum_str = ', '.join([f'"{v}"' for v in enum_values])
                zod_chain.append(f'z.enum([{enum_str}])')
            else:
                zod_chain.append('z.any()')

            if not validate.get('required', False):
                zod_chain.append('.optional()')

            zod_lines.append(f"  {field_name}: {"".join(zod_chain)},")

        zod_lines.append("});")
        zod_lines.append("")
        zod_lines.append(f"type FormData = z.infer<typeof schema>;")

        # Build form component
        form_lines = [
            f"import {{ useForm }} from 'react-hook-form';",
            f"import {{ zodResolver }} from '@hookform/resolvers/zod';",
            f"import {{ z }} from 'zod';",
            f"import {{ {entity_lower}API }} from '@/lib/api/{entity_lower}';",
            f"",
            f"{"".join(zod_lines)}",
            f"",
            f"export function {entity_name}Form() {{",
            f"  const {{ register, handleSubmit, formState: {{ errors, isSubmitting }} }} = useForm<FormData>({{",
            f"    resolver: zodResolver(schema),",
            f"  }});",
            f"",
            f"  const onSubmit = async (data: FormData) => {{",
            f"    try {{",
            f"      await {entity_lower}API.create(data as any);",
            f"      alert('Created successfully!');",
            f"    }} catch (error) {{",
            f"      console.error('Failed:', error);",
            f"    }}",
            f"  }};",
            f"",
            f"  return (",
            f"    <form onSubmit={{handleSubmit(onSubmit)}}>",
        ]

        # Add form fields
        for field_name, field_def in properties.items():
            if self._is_private(field_def) or '$ref' in field_def:
                continue

            field_type = field_def.get('type', 'string')
            label = field_def.get('label', field_name)
            validate = field_def.get('validate', {})
            ui = field_def.get('ui', {})
            placeholder = ui.get('placeholder', '')

            form_lines.append(f"      <div>")
            form_lines.append(f"        <label>{label}{{{' *' if validate.get('required') else ''}}}</label>")

            if field_type == 'enum':
                enum_values = validate.get('enum', [])
                form_lines.append(f"        <select {{...register('{field_name}')}}>")
                for val in enum_values:
                    form_lines.append(f"          <option value=\"{val}\">{val}</option>")
                form_lines.append(f"        </select>")
            elif field_type == 'boolean':
                form_lines.append(f"        <input type=\"checkbox\" {{...register('{field_name}')}} />")
            elif field_type in ['integer', 'number']:
                form_lines.append(f"        <input type=\"number\" {{...register('{field_name}', {{ valueAsNumber: true }})}} placeholder=\"{placeholder}\" />")
            elif field_type == 'password':
                form_lines.append(f"        <input type=\"password\" {{...register('{field_name}')}} placeholder=\"{placeholder}\" />")
            else:
                form_lines.append(f"        <input type=\"text\" {{...register('{field_name}')}} placeholder=\"{placeholder}\" />")

            form_lines.append(f"        {{errors.{field_name} && <span>{{{{errors.{field_name}?.message}}}}</span>}}")
            form_lines.append(f"      </div>")

        form_lines.append(f"      <button type=\"submit\" disabled={{isSubmitting}}>")
        form_lines.append(f"        {{isSubmitting ? 'Submitting...' : 'Submit'}}")
        form_lines.append(f"      </button>")
        form_lines.append(f"    </form>")
        form_lines.append(f"  );")
        form_lines.append(f"}}")

        return "\n".join(form_lines)

    def generate_table(self) -> str:
        """Generate table component"""
        entity_name = self._get_entity_name()
        entity_lower = entity_name.lower()
        properties = self.schema.get('properties', {})

        # Filter visible fields
        visible_fields = []
        for field_name, field_def in properties.items():
            if self._is_private(field_def):
                continue
            if field_def.get('ui', {}).get('showInList', True):
                visible_fields.append((field_name, field_def))

        table_content = f"""import {{ useEffect, useState }} from 'react';
import {{ {entity_name} }} from '@/types/{entity_lower}';
import {{ {entity_lower}API }} from '@/lib/api/{entity_lower}';

export function {entity_name}Table() {{
  const [data, setData] = useState<{entity_name}[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {{
    loadData();
  }}, []);

  const loadData = async () => {{
    setLoading(true);
    try {{
      const items = await {entity_lower}API.list();
      setData(items);
    }} catch (error) {{
      console.error('Failed to load:', error);
    }} finally {{
      setLoading(false);
    }}
  }};

  const handleDelete = async (id: string) => {{
    if (!confirm('Are you sure?')) return;
    await {entity_lower}API.delete(id);
    loadData();
  }};

  if (loading) return <div>Loading...</div>;

  return (
    <div>
      <table>
        <thead>
          <tr>
"""

        # Table headers
        for field_name, field_def in visible_fields:
            label = field_def.get('label', field_name)
            table_content += f"            <th>{label}</th>\n"

        table_content += """            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {data.map(item => (
            <tr key={item.id}>
"""

        # Table cells
        for field_name, field_def in visible_fields:
            field_type = field_def.get('type', 'string')
            if field_type == 'password':
                table_content += f"              <td>••••••</td>\n"
            elif field_type == 'boolean':
                table_content += f"              <td>{{{{item.{field_name} ? '✓' : '✗'}}}}</td>\n"
            else:
                table_content += f"              <td>{{{{item.{field_name}}}}}</td>\n"

        table_content += f"""              <td>
                <button onClick={() => handleDelete(item.id)}>Delete</button>
              </td>
            </tr>
          ))}}
        </tbody>
      </table>
    </div>
  );
}}
"""
        return table_content

    def write_files(self) -> None:
        """Write generated files"""
        entity_name = self._get_entity_name()
        entity_lower = entity_name.lower()

        # Create directories
        types_dir = self.output_dir / "types"
        api_dir = self.output_dir / "lib" / "api"
        components_dir = self.output_dir / "components"

        for d in [types_dir, api_dir, components_dir]:
            d.mkdir(parents=True, exist_ok=True)

        # Write files
        files = {
            types_dir / f"{entity_lower}.ts": self.generate_types(),
            api_dir / f"{entity_lower}.ts": self.generate_api(),
            components_dir / f"{entity_name}Form.tsx": self.generate_form(),
            components_dir / f"{entity_name}Table.tsx": self.generate_table(),
        }

        for file_path, content in files.items():
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Generated: {file_path}")

        print(f"\n🎉 Generation complete! Files written to: {self.output_dir}")


def main():
    """Main entry point"""
    if len(sys.argv) < 3:
        print("Usage: python generate_ts.py <schema_path> <output_dir>")
        sys.exit(1)

    schema_path = sys.argv[1]
    output_dir = sys.argv[2]

    if not os.path.exists(schema_path):
        print(f"Error: Schema file not found: {schema_path}")
        sys.exit(1)

    generator = TSCodeGenerator(schema_path, output_dir)
    generator.write_files()


if __name__ == "__main__":
    main()