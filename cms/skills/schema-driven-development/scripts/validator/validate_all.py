#!/usr/bin/env python3
"""
Batch Schema Validator - Validate all schema.json files in a directory
"""

import sys
import os
import json
from pathlib import Path
from validate_schema import SchemaValidator


def find_schema_files(directory: str) -> list:
    """Find all schema.json files in directory"""
    schema_files = []
    dir_path = Path(directory)

    if not dir_path.exists():
        print(f"Error: Directory not found: {directory}")
        return []

    # Recursively find all schema.json files
    for schema_file in dir_path.rglob("schema.json"):
        schema_files.append(str(schema_file))

    return sorted(schema_files)


def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        print("Usage: python validate_all.py <directory>")
        print("       python validate_all.py <directory> --json")
        sys.exit(1)

    directory = sys.argv[1]
    json_output = "--json" in sys.argv

    schema_files = find_schema_files(directory)

    if not schema_files:
        print(f"No schema.json files found in {directory}")
        sys.exit(0)

    results = []
    total_valid = 0
    total_invalid = 0

    print(f"\nFound {len(schema_files)} schema file(s) to validate")
    print("=" * 70)

    for schema_path in schema_files:
        validator = SchemaValidator(schema_path)
        is_valid, errors, warnings = validator.validate()

        if is_valid:
            total_valid += 1
            status = "✅ Valid"
        else:
            total_invalid += 1
            status = "❌ Invalid"

        if json_output:
            results.append({
                "schema": schema_path,
                "valid": is_valid,
                "errors": errors,
                "warnings": warnings
            })
        else:
            print(f"\n{status} {schema_path}")

            if warnings:
                print("  ⚠️  Warnings:")
                for warning in warnings:
                    print(f"    - {warning}")

            if errors:
                print("  ❌ Errors:")
                for error in errors:
                    print(f"    - {error}")

    if json_output:
        print(json.dumps({
            "summary": {
                "total": len(schema_files),
                "valid": total_valid,
                "invalid": total_invalid
            },
            "results": results
        }, indent=2))
    else:
        print("\n" + "=" * 70)
        print(f"Summary: {total_valid} valid, {total_invalid} invalid out of {len(schema_files)} total")

    sys.exit(0 if total_invalid == 0 else 1)


if __name__ == "__main__":
    main()