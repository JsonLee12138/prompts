#!/usr/bin/env python3
"""
Schema Validator - Validate entity schema files against entity_schema.json specification
"""

import json
import sys
import os
from typing import Dict, List, Tuple, Any, Optional


class SchemaValidator:
    """Validates schema.json files against the entity_schema.json specification"""

    # Valid field types
    VALID_TYPES = {
        "string", "text", "integer", "number", "boolean", "enum",
        "json", "media", "richText", "datetime", "password", "uid",
        "version", "array", "object"
    }

    # Valid relation types
    VALID_RELATION_TYPES = {"one2One", "many2One", "one2Many", "many2Many"}

    # Valid widget types
    VALID_WIDGETS = {
        "text", "textarea", "password", "email", "number", "decimal",
        "select", "radio", "checkbox", "switch", "date", "datetime",
        "file", "image", "video", "audio", "custom"
    }

    # Valid index types
    VALID_INDEX_TYPES = {"unique", "fulltext", "index"}

    # Valid delete actions
    VALID_DELETE_ACTIONS = {"cascade", "setNull", "restrict", "noAction", "setDefault"}

    # Valid media types
    VALID_MEDIA_TYPES = {"image", "video", "audio", "file"}

    # Valid layout directions
    VALID_DIRECTIONS = {"vertical", "horizontal"}

    # Valid component modes
    VALID_COMPONENT_MODES = {"flatten", "relation"}

    # Valid format types
    VALID_FORMATS = {"email", "url", "uuid", "phone", "datetime", "date", "time"}

    def __init__(self, schema_path: str):
        self.schema_path = schema_path
        self.errors: List[str] = []
        self.warnings: List[str] = []

    def validate(self) -> Tuple[bool, List[str], List[str]]:
        """Main validation method"""
        try:
            # Load schema file
            with open(self.schema_path, 'r', encoding='utf-8') as f:
                schema = json.load(f)

            # Run all validations
            self._validate_root_structure(schema)
            self._validate_properties(schema)
            self._validate_indexes(schema)
            self._validate_features(schema)

            return len(self.errors) == 0, self.errors, self.warnings

        except FileNotFoundError:
            self.errors.append(f"Schema file not found: {self.schema_path}")
            return False, self.errors, self.warnings
        except json.JSONDecodeError as e:
            self.errors.append(f"Invalid JSON: {e}")
            return False, self.errors, self.warnings
        except Exception as e:
            self.errors.append(f"Unexpected error: {e}")
            return False, self.errors, self.warnings

    def _validate_root_structure(self, schema: Dict):
        """Validate root-level structure"""
        # Required fields
        if "name" not in schema:
            self.errors.append("Missing required field: name")
        elif not isinstance(schema["name"], str):
            self.errors.append("Field 'name' must be a string")
        elif not schema["name"][0].isupper():
            self.warnings.append("Entity name should be PascalCase (start with uppercase)")

        if "properties" not in schema:
            self.errors.append("Missing required field: properties")
        elif not isinstance(schema["properties"], dict):
            self.errors.append("Field 'properties' must be an object")

        # Optional fields with type checking
        if "collectionName" in schema and not isinstance(schema["collectionName"], str):
            self.errors.append("Field 'collectionName' must be a string")

        if "description" in schema:
            desc = schema["description"]
            if not isinstance(desc, str) and not isinstance(desc, dict):
                self.errors.append("Field 'description' must be string or object (for i18n)")

        if "softDelete" in schema and not isinstance(schema["softDelete"], bool):
            self.errors.append("Field 'softDelete' must be a boolean")

        # Validate info section
        if "info" in schema:
            self._validate_info(schema["info"])

        # Validate root ui
        if "ui" in schema:
            self._validate_root_ui(schema["ui"])

    def _validate_info(self, info: Dict):
        """Validate info section"""
        if not isinstance(info, dict):
            self.errors.append("Field 'info' must be an object")
            return

        if "displayName" in info:
            val = info["displayName"]
            if not isinstance(val, str) and not isinstance(val, dict):
                self.errors.append("info.displayName must be string or object")

        if "description" in info:
            val = info["description"]
            if not isinstance(val, str) and not isinstance(val, dict):
                self.errors.append("info.description must be string or object")

        if "icon" in info and not isinstance(info["icon"], str):
            self.errors.append("info.icon must be a string")

        if "locale" in info and not isinstance(info["locale"], str):
            self.errors.append("info.locale must be a string")

    def _validate_root_ui(self, ui: Dict):
        """Validate root-level UI configuration"""
        if not isinstance(ui, dict):
            self.errors.append("Field 'ui' must be an object")
            return

        # Button texts
        if "submitText" in ui:
            val = ui["submitText"]
            if not isinstance(val, str) and not isinstance(val, dict):
                self.errors.append("ui.submitText must be string or object")

        if "resetText" in ui:
            val = ui["resetText"]
            if not isinstance(val, str) and not isinstance(val, dict):
                self.errors.append("ui.resetText must be string or object")

        if "showReset" in ui and not isinstance(ui["showReset"], bool):
            self.errors.append("ui.showReset must be a boolean")

        # Layout
        if "layout" in ui:
            layout = ui["layout"]
            if not isinstance(layout, dict):
                self.errors.append("ui.layout must be an object")
            else:
                if "direction" in layout:
                    if layout["direction"] not in self.VALID_DIRECTIONS:
                        self.errors.append(f"ui.layout.direction must be one of {self.VALID_DIRECTIONS}")

                if "gap" in layout and not isinstance(layout["gap"], (int, float)):
                    self.errors.append("ui.layout.gap must be a number")

                if "columns" in layout and not isinstance(layout["columns"], int):
                    self.errors.append("ui.layout.columns must be an integer")

    def _validate_properties(self, schema: Dict):
        """Validate properties section"""
        if "properties" not in schema:
            return

        properties = schema["properties"]
        if not isinstance(properties, dict):
            return

        for field_name, field_def in properties.items():
            if not isinstance(field_def, dict):
                self.errors.append(f"Property '{field_name}' must be an object")
                continue

            self._validate_property(field_name, field_def)

    def _validate_property(self, field_name: str, field_def: Dict):
        """Validate a single property"""
        # Check for relationship field ($ref)
        has_ref = "$ref" in field_def
        has_type = "type" in field_def

        if has_ref:
            # Relationship field
            ref_value = field_def["$ref"]
            if not isinstance(ref_value, str):
                self.errors.append(f"Property '{field_name}.$ref' must be a string")

            # Should not have type field
            if has_type:
                self.warnings.append(f"Property '{field_name}': Relationship fields should use $ref, not type")

            # Must have x-relation for relationships
            if "x-relation" not in field_def:
                self.errors.append(f"Property '{field_name}': Relationship fields must have x-relation")
            else:
                self._validate_relation(field_name, field_def["x-relation"])

        elif has_type:
            # Regular field
            field_type = field_def["type"]
            if field_type not in self.VALID_TYPES:
                self.errors.append(f"Property '{field_name}': Invalid type '{field_type}'. Expected one of {self.VALID_TYPES}")

            # Validate array items
            if field_type == "array" and "items" in field_def:
                self._validate_property(f"{field_name}[]", field_def["items"])

            # Validate object properties
            if field_type == "object" and "properties" in field_def:
                if not isinstance(field_def["properties"], dict):
                    self.errors.append(f"Property '{field_name}.properties' must be an object")
                else:
                    for nested_name, nested_def in field_def["properties"].items():
                        if isinstance(nested_def, dict):
                            self._validate_property(f"{field_name}.{nested_name}", nested_def)

        else:
            # Missing both $ref and type
            self.errors.append(f"Property '{field_name}': Must have either $ref or type")

        # Validate label
        if "label" in field_def:
            val = field_def["label"]
            if not isinstance(val, str) and not isinstance(val, dict):
                self.errors.append(f"Property '{field_name}.label' must be string or object")

        # Validate description
        if "description" in field_def:
            val = field_def["description"]
            if not isinstance(val, str) and not isinstance(val, dict):
                self.errors.append(f"Property '{field_name}.description' must be string or object")

        # Validate validate rules
        if "validate" in field_def:
            self._validate_validation_rules(field_name, field_def["validate"])

        # Validate UI
        if "ui" in field_def:
            self._validate_field_ui(field_name, field_def["ui"])

        # Validate other property fields
        self._validate_property_flags(field_name, field_def)

    def _validate_relation(self, field_name: str, relation: Any):
        """Validate x-relation configuration"""
        if not isinstance(relation, dict):
            self.errors.append(f"Property '{field_name}.x-relation' must be an object")
            return

        # Type is required
        if "type" not in relation:
            self.errors.append(f"Property '{field_name}.x-relation.type' is required")
        elif relation["type"] not in self.VALID_RELATION_TYPES:
            self.errors.append(f"Property '{field_name}.x-relation.type' must be one of {self.VALID_RELATION_TYPES}")

        # Optional fields
        if "inversedBy" in relation and not isinstance(relation["inversedBy"], str):
            self.errors.append(f"Property '{field_name}.x-relation.inversedBy' must be a string")

        if "mapBy" in relation and not isinstance(relation["mapBy"], str):
            self.errors.append(f"Property '{field_name}.x-relation.mapBy' must be a string")

        if "labelField" in relation and not isinstance(relation["labelField"], str):
            self.errors.append(f"Property '{field_name}.x-relation.labelField' must be a string")

        if "preload" in relation and not isinstance(relation["preload"], bool):
            self.errors.append(f"Property '{field_name}.x-relation.preload' must be a boolean")

        if "writable" in relation and not isinstance(relation["writable"], bool):
            self.errors.append(f"Property '{field_name}.x-relation.writable' must be a boolean")

        if "queryable" in relation and not isinstance(relation["queryable"], bool):
            self.errors.append(f"Property '{field_name}.x-relation.queryable' must be a boolean")

        if "onDelete" in relation:
            if relation["onDelete"] not in self.VALID_DELETE_ACTIONS:
                self.errors.append(f"Property '{field_name}.x-relation.onDelete' must be one of {self.VALID_DELETE_ACTIONS}")

    def _validate_validation_rules(self, field_name: str, validate: Any):
        """Validate validation rules"""
        if not isinstance(validate, dict):
            self.errors.append(f"Property '{field_name}.validate' must be an object")
            return

        # Boolean rules
        for rule in ["required", "nullable", "positive", "negative", "nonNegative", "integer"]:
            if rule in validate and not isinstance(validate[rule], bool):
                self.errors.append(f"Property '{field_name}.validate.{rule}' must be a boolean")

        # Numeric rules
        for rule in ["min", "max", "length"]:
            if rule in validate and not isinstance(validate[rule], (int, float)):
                self.errors.append(f"Property '{field_name}.validate.{rule}' must be a number")

        # String rules
        if "pattern" in validate and not isinstance(validate["pattern"], str):
            self.errors.append(f"Property '{field_name}.validate.pattern' must be a string")

        if "format" in validate:
            if validate["format"] not in self.VALID_FORMATS:
                self.errors.append(f"Property '{field_name}.validate.format' must be one of {self.VALID_FORMATS}")

        # Enum
        if "enum" in validate:
            if not isinstance(validate["enum"], list):
                self.errors.append(f"Property '{field_name}.validate.enum' must be an array")
            elif not all(isinstance(item, str) for item in validate["enum"]):
                self.errors.append(f"Property '{field_name}.validate.enum' must contain only strings")

        # Custom validation
        if "custom" in validate:
            custom = validate["custom"]
            if not isinstance(custom, list):
                self.errors.append(f"Property '{field_name}.validate.custom' must be an array")
            else:
                for i, item in enumerate(custom):
                    if not isinstance(item, dict):
                        self.errors.append(f"Property '{field_name}.validate.custom[{i}]' must be an object")
                    elif "code" not in item:
                        self.errors.append(f"Property '{field_name}.validate.custom[{i}]' must have 'code' field")

        # Error message
        if "errorMessage" in validate:
            val = validate["errorMessage"]
            if not isinstance(val, str) and not isinstance(val, dict):
                self.errors.append(f"Property '{field_name}.validate.errorMessage' must be string or object")

    def _validate_field_ui(self, field_name: str, ui: Any):
        """Validate field-level UI configuration"""
        if not isinstance(ui, dict):
            self.errors.append(f"Property '{field_name}.ui' must be an object")
            return

        # Widget
        if "widget" in ui:
            if ui["widget"] not in self.VALID_WIDGETS:
                self.errors.append(f"Property '{field_name}.ui.widget' must be one of {self.VALID_WIDGETS}")

        # Placeholder
        if "placeholder" in ui:
            val = ui["placeholder"]
            if not isinstance(val, str) and not isinstance(val, dict):
                self.errors.append(f"Property '{field_name}.ui.placeholder' must be string or object")

        # Boolean flags
        for flag in ["showInList", "showInForm", "readOnly", "writeOnly", "disabled", "hidden", "multiple", "searchable", "filterable", "sortable", "aggregatable", "exportable", "importable", "batchable", "editable", "queryable"]:
            if flag in ui and not isinstance(ui[flag], bool):
                self.errors.append(f"Property '{field_name}.ui.{flag}' must be a boolean")

        # Numeric values
        for field in ["span", "rows", "step", "precision", "maxLength", "minLength", "sort"]:
            if field in ui and not isinstance(ui[field], (int, float)):
                self.errors.append(f"Property '{field_name}.ui.{field}' must be a number")

        # String values
        for field in ["className", "icon", "prefix", "suffix"]:
            if field in ui and not isinstance(ui[field], str):
                self.errors.append(f"Property '{field_name}.ui.{field}' must be a string")

        # Size
        if "size" in ui and ui["size"] not in ["sm", "md", "lg"]:
            self.errors.append(f"Property '{field_name}.ui.size' must be 'sm', 'md', or 'lg'")

        # Style
        if "style" in ui and not isinstance(ui["style"], dict):
            self.errors.append(f"Property '{field_name}.ui.style' must be an object")

        # Options
        if "options" in ui:
            options = ui["options"]
            if not isinstance(options, list):
                self.errors.append(f"Property '{field_name}.ui.options' must be an array")
            else:
                for i, opt in enumerate(options):
                    if not isinstance(opt, dict):
                        self.errors.append(f"Property '{field_name}.ui.options[{i}]' must be an object")
                    else:
                        if "value" not in opt:
                            self.errors.append(f"Property '{field_name}.ui.options[{i}]' must have 'value'")
                        if "label" not in opt:
                            self.errors.append(f"Property '{field_name}.ui.options[{i}]' must have 'label'")
                        if "disabled" in opt and not isinstance(opt["disabled"], bool):
                            self.errors.append(f"Property '{field_name}.ui.options[{i}].disabled' must be a boolean")

    def _validate_property_flags(self, field_name: str, field_def: Dict):
        """Validate other property fields"""
        # Boolean flags
        for flag in ["unique", "primaryKey", "private", "writable", "queryable", "exportable", "importable"]:
            if flag in field_def and not isinstance(field_def[flag], bool):
                self.errors.append(f"Property '{field_name}.{flag}' must be a boolean")

        # Version
        if "version" in field_def:
            val = field_def["version"]
            if not isinstance(val, int) or val < 1:
                self.errors.append(f"Property '{field_name}.version' must be an integer >= 1")

        # Default value
        # No strict type checking for default as it can be any type

        # Component
        if "$component" in field_def and not isinstance(field_def["$component"], str):
            self.errors.append(f"Property '{field_name}.$component' must be a string")

        # Relation type (component mode)
        if "relation-type" in field_def:
            if field_def["relation-type"] not in self.VALID_COMPONENT_MODES:
                self.errors.append(f"Property '{field_name}.relation-type' must be one of {self.VALID_COMPONENT_MODES}")

        # Allowed types for media
        if "allowedTypes" in field_def:
            allowed = field_def["allowedTypes"]
            if not isinstance(allowed, list):
                self.errors.append(f"Property '{field_name}.allowedTypes' must be an array")
            else:
                for media_type in allowed:
                    if media_type not in self.VALID_MEDIA_TYPES:
                        self.errors.append(f"Property '{field_name}.allowedTypes' contains invalid type '{media_type}'")

    def _validate_indexes(self, schema: Dict):
        """Validate indexes section"""
        if "indexes" not in schema:
            return

        indexes = schema["indexes"]
        if not isinstance(indexes, list):
            self.errors.append("Field 'indexes' must be an array")
            return

        for i, index in enumerate(indexes):
            if not isinstance(index, dict):
                self.errors.append(f"indexes[{i}] must be an object")
                continue

            # Type
            if "type" in index:
                if index["type"] not in self.VALID_INDEX_TYPES:
                    self.errors.append(f"indexes[{i}].type must be one of {self.VALID_INDEX_TYPES}")
            else:
                self.warnings.append(f"indexes[{i}] missing type, defaulting to 'index'")

            # Name
            if "name" in index and not isinstance(index["name"], str):
                self.errors.append(f"indexes[{i}].name must be a string")

            # Columns (required)
            if "columns" not in index:
                self.errors.append(f"indexes[{i}] missing required 'columns' field")
            elif not isinstance(index["columns"], list):
                self.errors.append(f"indexes[{i}].columns must be an array")
            elif len(index["columns"]) == 0:
                self.errors.append(f"indexes[{i}].columns cannot be empty")
            else:
                for col in index["columns"]:
                    if not isinstance(col, str):
                        self.errors.append(f"indexes[{i}].columns must contain only strings")

            # Unique (legacy)
            if "unique" in index and not isinstance(index["unique"], bool):
                self.errors.append(f"indexes[{i}].unique must be a boolean")

    def _validate_features(self, schema: Dict):
        """Validate features section"""
        if "features" not in schema:
            return

        features = schema["features"]
        if not isinstance(features, dict):
            self.errors.append("Field 'features' must be an object")
            return

        for feature_name, value in features.items():
            if not isinstance(value, bool):
                self.errors.append(f"features.{feature_name} must be a boolean")


def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        print("Usage: python validate_schema.py <schema_path>")
        print("       python validate_schema.py <schema_path> --json")
        sys.exit(1)

    schema_path = sys.argv[1]
    json_output = "--json" in sys.argv

    validator = SchemaValidator(schema_path)
    is_valid, errors, warnings = validator.validate()

    if json_output:
        result = {
            "valid": is_valid,
            "schema": schema_path,
            "errors": errors,
            "warnings": warnings
        }
        print(json.dumps(result, indent=2))
    else:
        print(f"\nValidating: {schema_path}")
        print("-" * 60)

        if warnings:
            print("\n⚠️  Warnings:")
            for warning in warnings:
                print(f"  - {warning}")

        if errors:
            print("\n❌ Errors:")
            for error in errors:
                print(f"  - {error}")
            print(f"\nResult: FAILED with {len(errors)} error(s)")
        else:
            print("\n✅ Schema is valid!")

    sys.exit(0 if is_valid else 1)


if __name__ == "__main__":
    main()