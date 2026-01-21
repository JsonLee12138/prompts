#!/usr/bin/env python3
"""
Schema Designer - Interactive tool for creating entity schemas
"""

import json
import sys
from typing import Dict, List, Any


class SchemaDesigner:
    """Interactive schema designer"""

    def __init__(self):
        self.schema = {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "name": "",
            "collectionName": "",
            "description": "",
            "softDelete": False,
            "info": {},
            "ui": {},
            "properties": {},
            "indexes": [],
            "features": {}
        }

    def ask(self, question: str, default: str = "", required: bool = False) -> str:
        """Ask user a question"""
        prompt = question
        if default:
            prompt += f" [{default}]"
        prompt += ": "

        answer = input(prompt).strip()

        if required and not answer:
            print("⚠️  This field is required!")
            return self.ask(question, default, required)

        return answer or default

    def ask_yes_no(self, question: str, default: bool = False) -> bool:
        """Ask yes/no question"""
        default_str = "Y/n" if default else "y/N"
        answer = input(f"{question} ({default_str}): ").strip().lower()

        if not answer:
            return default

        return answer in ["y", "yes"]

    def ask_list(self, question: str) -> List[str]:
        """Ask for comma-separated list"""
        answer = input(f"{question} (comma-separated): ").strip()
        if not answer:
            return []
        return [item.strip() for item in answer.split(",") if item.strip()]

    def design_entity(self):
        """Design entity metadata"""
        print("\n=== Entity Design ===")

        name = self.ask("Entity name (PascalCase)", required=True)
        self.schema["name"] = name

        # Collection name
        collection = self.ask("Collection name (plural, snake_case)", f"{name.lower()}s")
        self.schema["collectionName"] = collection

        # Description
        desc = self.ask("Entity description")
        self.schema["description"] = desc

        # Soft delete
        soft_delete = self.ask_yes_no("Enable soft delete?", False)
        self.schema["softDelete"] = soft_delete

        # Info section
        display_name = self.ask("Display name (for UI)", name)
        info_desc = self.ask("Info description", desc)
        icon = self.ask("Icon name", "Database")

        self.schema["info"] = {
            "displayName": display_name,
            "description": info_desc,
            "icon": icon
        }

    def design_fields(self):
        """Design fields interactively"""
        print("\n=== Field Design ===")
        print("Enter field details. Leave blank to finish.")

        while True:
            print("\n--- New Field ---")
            field_name = self.ask("Field name (camelCase)")
            if not field_name:
                break

            # Field type
            print("Available types: string, text, integer, number, boolean, enum, datetime, password, uid, array, object, media")
            field_type = self.ask("Field type", "string")

            # Label and description
            label = self.ask("Label (for UI)", field_name)
            description = self.ask("Description")

            # Validation
            print("\nValidation Rules:")
            required = self.ask_yes_no("  Required?", False)
            min_val = self.ask("  Min value/length")
            max_val = self.ask("  Max value/length")
            format_type = self.ask("  Format (email/url/phone/uuid)")
            enum_values = []
            if field_type == "enum":
                enum_values = self.ask_list("  Enum values")

            # UI configuration
            print("\nUI Configuration:")
            widget = self.ask("  Widget type (input/textarea/select/checkbox/etc.)", "input")
            show_in_list = self.ask_yes_no("  Show in list?", True)
            show_in_form = self.ask_yes_no("  Show in form?", True)
            placeholder = self.ask("  Placeholder")

            # Build field definition
            field_def = {
                "type": field_type,
                "label": label
            }

            if description:
                field_def["description"] = description

            # Validation rules
            validate = {}
            if required:
                validate["required"] = True
            if min_val:
                validate["min"] = int(min_val) if min_val.isdigit() else min_val
            if max_val:
                validate["max"] = int(max_val) if max_val.isdigit() else max_val
            if format_type:
                validate["format"] = format_type
            if enum_values:
                validate["enum"] = enum_values

            if validate:
                field_def["validate"] = validate

            # UI config
            ui = {}
            if widget:
                ui["widget"] = widget
            if show_in_list is not None:
                ui["showInList"] = show_in_list
            if show_in_form is not None:
                ui["showInForm"] = show_in_form
            if placeholder:
                ui["placeholder"] = placeholder

            if ui:
                field_def["ui"] = ui

            self.schema["properties"][field_name] = field_def

            print(f"✅ Added field: {field_name}")

    def design_relationships(self):
        """Design relationship fields"""
        print("\n=== Relationship Design ===")
        print("Define relationships to other entities")

        while self.ask_yes_no("Add relationship?", False):
            field_name = self.ask("Field name (camelCase)", required=True)
            target = self.ask("Target entity name (PascalCase)", required=True)

            print("Relationship types:")
            print("  1. one2One - One to one")
            print("  2. many2One - Many to one (e.g., many posts belong to one author)")
            print("  3. one2Many - One to many (e.g., one author has many posts)")
            print("  4. many2Many - Many to many")

            rel_type_num = self.ask("Type (1-4)")
            rel_types = ["one2One", "many2One", "one2Many", "many2Many"]
            rel_type = rel_types[int(rel_type_num) - 1] if rel_type_num.isdigit() and 1 <= int(rel_type_num) <= 4 else "many2One"

            label = self.ask("Label", field_name)
            label_field = self.ask("Label field (for display)", "name")
            preload = self.ask_yes_no("Preload?", False)

            field_def = {
                "$ref": target,
                "label": label,
                "x-relation": {
                    "type": rel_type,
                    "labelField": label_field,
                    "preload": preload
                }
            }

            self.schema["properties"][field_name] = field_def
            print(f"✅ Added relationship: {field_name} -> {target} ({rel_type})")

    def design_indexes(self):
        """Design indexes"""
        print("\n=== Index Design ===")

        while self.ask_yes_no("Add index?", False):
            index_type = self.ask("Type (unique/index/fulltext)", "index")
            columns = self.ask_list("Columns")
            name = self.ask("Index name", f"idx_{'_'.join(columns)}")

            index_def = {
                "type": index_type,
                "name": name,
                "columns": columns
            }

            self.schema["indexes"].append(index_def)
            print(f"✅ Added index: {name}")

    def design_ui(self):
        """Design UI configuration"""
        print("\n=== UI Configuration ===")

        # Root UI
        submit_text = self.ask("Submit button text", "提交")
        reset_text = self.ask("Reset button text", "重置")
        show_reset = self.ask_yes_no("Show reset button?", False)

        self.schema["ui"] = {
            "submitText": submit_text,
            "resetText": reset_text,
            "showReset": show_reset
        }

        # Features
        print("\nFeatures:")
        soft_delete = self.ask_yes_no("  Enable soft delete?", False)
        export = self.ask_yes_no("  Enable export?", True)
        import_ = self.ask_yes_no("  Enable import?", False)
        batch = self.ask_yes_no("  Enable batch operations?", True)

        self.schema["features"] = {
            "softDelete": soft_delete,
            "export": export,
            "import": import_,
            "batch": batch
        }

    def run(self):
        """Run interactive designer"""
        print("🎯 Schema Designer - Interactive Tool")
        print("=" * 50)

        self.design_entity()
        self.design_fields()
        self.design_relationships()
        self.design_indexes()
        self.design_ui()

        # Output
        print("\n" + "=" * 50)
        print("Generated Schema:")
        print(json.dumps(self.schema, indent=2, ensure_ascii=False))

        return self.schema


def main():
    """Main entry point"""
    designer = SchemaDesigner()
    schema = designer.run()

    # Save to file
    output_file = f"{schema['name'].lower()}-schema.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(schema, f, indent=2, ensure_ascii=False)

    print(f"\n✅ Schema saved to: {output_file}")


if __name__ == "__main__":
    main()