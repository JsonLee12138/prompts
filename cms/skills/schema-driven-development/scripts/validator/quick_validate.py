#!/usr/bin/env python3
"""
Quick Validation Script - Validates a schema directory quickly
"""

import sys
import os
from pathlib import Path
from validate_all import find_schema_files
from validate_schema import SchemaValidator


def main():
    """Quick validation entry point"""
    if len(sys.argv) < 2:
        print("Usage: python quick_validate.py <schema-directory>")
        sys.exit(1)

    directory = sys.argv[1]
    schema_files = find_schema_files(directory)

    if not schema_files:
        print(f"❌ No schema.json files found in {directory}")
        sys.exit(1)

    print(f"\n🔍 Validating {len(schema_files)} schema file(s)...\n")

    all_valid = True
    for schema_path in schema_files:
        validator = SchemaValidator(schema_path)
        is_valid, errors, warnings = validator.validate()

        rel_path = os.path.relpath(schema_path, directory)

        if is_valid:
            print(f"✅ {rel_path}")
        else:
            print(f"❌ {rel_path}")
            for error in errors:
                print(f"   - {error}")
            all_valid = False

    print()
    if all_valid:
        print("🎉 All schemas are valid!")
        sys.exit(0)
    else:
        print("❌ Some schemas have errors")
        sys.exit(1)


if __name__ == "__main__":
    main()