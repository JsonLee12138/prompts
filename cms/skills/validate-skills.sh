#!/bin/bash

# CMS Skills Validation Script
# Validates that all skills follow the proper format

echo "🔍 Validating CMS Skills..."
echo ""

SKILLS_DIR="/Users/jsonlee/Projects/prompts/cms/skills"
VALID=true

# Check each skill directory
for skill_dir in "$SKILLS_DIR"/*/; do
    if [ -d "$skill_dir" ]; then
        skill_name=$(basename "$skill_dir")

        # Skip if not a skill directory (e.g., root files like README.md, INSTALLATION.md, etc.)
        if [[ "$skill_name" == *"."* ]] || [ "$skill_name" = "skills" ]; then
            continue
        fi

        echo "📋 Checking: $skill_name"

        # Check for SKILL.md
        if [ ! -f "$skill_dir/SKILL.md" ]; then
            echo "  ❌ Missing SKILL.md"
            VALID=false
            continue
        fi

        # Check for required YAML frontmatter
        if ! grep -q "^---$" "$skill_dir/SKILL.md"; then
            echo "  ❌ Missing YAML frontmatter"
            VALID=false
            continue
        fi

        # Check for name field
        if ! grep -q "^name:" "$skill_dir/SKILL.md"; then
            echo "  ❌ Missing name field in frontmatter"
            VALID=false
            continue
        fi

        # Check for description field
        if ! grep -q "^description:" "$skill_dir/SKILL.md"; then
            echo "  ❌ Missing description field in frontmatter"
            VALID=false
            continue
        fi

        # Check for markdown content after frontmatter
        if ! grep -q "^#" "$skill_dir/SKILL.md"; then
            echo "  ❌ Missing markdown content (headers)"
            VALID=false
            continue
        fi

        echo "  ✅ Valid"
    fi
done

echo ""

if [ "$VALID" = true ]; then
    echo "✅ All skills are valid!"
    echo ""
    echo "Available skills:"
    for skill_dir in "$SKILLS_DIR"/*/; do
        if [ -d "$skill_dir" ] && [ -f "$skill_dir/SKILL.md" ]; then
            skill_name=$(basename "$skill_dir")
            if [[ "$skill_name" != *"."* ]] && [ "$skill_name" != "skills" ]; then
                # Extract description from frontmatter
                desc=$(grep "^description:" "$skill_dir/SKILL.md" | cut -d' ' -f2-)
                echo "  - @cms/$skill_name: $desc"
            fi
        fi
    done
    exit 0
else
    echo "❌ Some skills are invalid. Please fix the issues above."
    exit 1
fi