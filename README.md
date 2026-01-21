# Claude Code Skills & Rules Library

[中文文档](./README.zh.md)

A comprehensive collection of skills and rules for Claude Code, designed to enhance AI-assisted development workflows across different domains.

## 📚 Overview

This repository contains reusable skills and rules that can be loaded into Claude Code to provide specialized capabilities for:

- **Frontend Development** - React/TypeScript standards, ESLint configs, component development
- **Architecture** - Design principles, ADRs, multi-language examples
- **CMS Development** - Coding standards, response formats, schema-driven development
- **Schema Development** - Table/Form generation, code detection, backend development
- **Deployment** - Deployment documentation and guidelines

## 🚀 Quick Start

### Prerequisites

- Claude Code CLI installed
- A project with `.claude/` directory

### Installation

Each skill/rule can be installed by copying the relevant directories to your project's `.claude/` folder:

```bash
# Copy skills
cp -r <skill-directory> /path/to/your-project/.claude/skills/

# Copy rules
cp -r <rule-file>.md /path/to/your-project/.claude/rules/
```

## 📦 Available Skills

### 1. Frontend Development (`frontend/`)

**Skills:**
- `frontend-standard` - Complete frontend development standards
- `eslint-config` - ESLint configuration for workspaces
- `components` - Component development guidelines

**Installation:**
```bash
# Install main frontend skill
cp -r frontend /path/to/your-project/.claude/skills/

# Or install specific sub-skills
cp -r frontend/skills/eslint-config /path/to/your-project/.claude/skills/
cp -r frontend/skills/components /path/to/your-project/.claude/skills/
```

**Rules:**
```bash
cp frontend/RULES.md /path/to/your-project/.claude/rules/frontend-rules.md
```

**Features:**
- PascalCase/camelCase naming conventions
- @antfu/eslint-config standards
- UnoCSS and color presets
- Git commit conventions (Conventional Commits)
- Workspace/Monorepo setup guides

---

### 2. Architecture (`architecture/`)

**Main Skill:** `architecture-assistant`

**Installation:**
```bash
cp -r architecture /path/to/your-project/.claude/skills/
```

**Rules:**
```bash
cp architecture/RULES.md /path/to/your-project/.claude/rules/architecture-rules.md
```

**Features:**
- 10 core design principles (SoC, SRP, DRY, KISS, etc.)
- Multi-language examples (TypeScript, Go, Rust, Python, Java)
- Architecture Decision Records (ADR) templates
- Code review checklists
- Anti-pattern detection

**Resources Included:**
- Principle references
- Language-specific examples
- ADR templates and examples

---

### 3. CMS Development (`cms/`)

**Skills:**
- `cms-coding-standard` - CMS coding standards
- `cms-response-format` - Unified response format
- `schema-driven-development` - Schema-first development workflow

**Installation:**
```bash
# Install all CMS skills
cp -r cms/skills/* /path/to/your-project/.claude/skills/

# Or install individually
cp -r cms/skills/cms-coding-standard /path/to/your-project/.claude/skills/
cp -r cms/skills/cms-response-format /path/to/your-project/.claude/skills/
cp -r cms/skills/schema-driven-development /path/to/your-project/.claude/skills/
```

**Rules:**
```bash
cp cms/RULES.md /path/to/your-project/.claude/rules/cms-rules.md
```

**Features:**
- Go/TypeScript coding standards
- Unified API response format
- Schema validation and generation
- Security best practices
- Code templates for controllers/modules

---

### 4. Schema Development (`schema/`)

**Skills:**
- `table-developer` - Table schema development
- `form-developer` - Form schema development
- `code-detector` - Frontend/Backend pattern detection
- `backend-developer` - Backend code generation

**Installation:**
```bash
cp -r schema/skills/* /path/to/your-project/.claude/skills/
```

**Rules:**
```bash
cp schema/RULES.md /path/to/your-project/.claude/rules/schema-rules.md
```

**Features:**
- Schema-driven table/form generation
- Pattern detection for existing code
- Backend scaffolding
- Validation scripts

---

### 5. Deployment Documentation (`deployment-docs/`)

**Main Skill:** Deployment documentation and guidelines

**Installation:**
```bash
cp -r deployment-docs /path/to/your-project/.claude/skills/
```

**Rules:**
```bash
cp deployment-docs/RULES.md /path/to/your-project/.claude/rules/deployment-rules.md
```

---

## 🛠️ Skill Management Tools

### Creating New Skills

Use the built-in skill creator:

```bash
# Initialize a new skill
python .claude/skills/skill-creator/scripts/init_skill.py <skill-name> --path <output-directory>

# Example
python .claude/skills/skill-creator/scripts/init_skill.py my-custom-skill --path .claude/skills/
```

### Validating Skills

```bash
# Validate skill structure
python .claude/skills/skill-creator/scripts/quick_validate.py <skill-directory>

# Example
python .claude/skills/skill-creator/scripts/quick_validate.py .claude/skills/my-skill
```

### Packaging Skills

```bash
# Package skill for distribution
python .claude/skills/skill-creator/scripts/package_skill.py <skill-directory>

# With custom output directory
python .claude/skills/skill-creator/scripts/package_skill.py <skill-directory> ./dist
```

---

## 📖 Usage Examples

### Example 1: Frontend Project Setup

```bash
# 1. Copy frontend skills and rules
cp -r frontend /path/to/frontend-project/.claude/skills/
cp frontend/RULES.md /path/to/frontend-project/.claude/rules/frontend-rules.md

# 2. Ask Claude Code
# "Set up ESLint for my React TypeScript workspace"
# "Review this component for frontend standards compliance"
```

### Example 2: Architecture Review

```bash
# 1. Install architecture skill
cp -r architecture /path/to/project/.claude/skills/
cp architecture/RULES.md /path/to/project/.claude/rules/architecture-rules.md

# 2. Ask Claude Code
# "Review this code against architecture principles"
# "Create an ADR for choosing PostgreSQL over MongoDB"
```

### Example 3: CMS Development

```bash
# 1. Install CMS skills
cp -r cms/skills/* /path/to/cms-project/.claude/skills/
cp cms/RULES.md /path/to/cms-project/.claude/rules/cms-rules.md

# 2. Ask Claude Code
# "Generate a user module following CMS standards"
# "Create API response types for this endpoint"
```

### Example 4: Schema-Driven Development

```bash
# 1. Install schema skills
cp -r schema/skills/* /path/to/project/.claude/skills/
cp schema/RULES.md /path/to/project/.claude/rules/schema-rules.md

# 2. Ask Claude Code
# "Generate a table schema for user management"
# "Detect frontend patterns in this codebase"
```

---

## 📁 Directory Structure

```
.
├── README.md                          # This file
├── CLAUDE.md                          # Global Claude Code rules
├── .claude/
│   ├── skills/
│   │   └── skill-creator/             # Skill creation tools
│   └── rules/
│       └── skill-creator-rules.md     # Skill creator usage rules
├── frontend/
│   ├── SKILL.md                       # Main skill file
│   ├── RULES.md                       # Frontend rules
│   ├── skills/                        # Sub-skills
│   ├── references/                    # Documentation
│   ├── assets/                        # Templates & configs
│   └── templates/                     # Code templates
├── architecture/
│   ├── SKILL.md
│   ├── RULES.md
│   ├── references/                    # Principles & guides
│   ├── examples/                      # Language examples
│   ├── adrs/                          # ADR examples
│   └── assets/                        # Templates
├── cms/
│   ├── RULES.md
│   └── skills/
│       ├── cms-coding-standard/
│       ├── cms-response-format/
│       └── schema-driven-development/
├── schema/
│   ├── RULES.md
│   └── skills/
│       ├── table-developer/
│       ├── form-developer/
│       ├── code-detector/
│       └── backend-developer/
└── deployment-docs/
    ├── SKILL.md
    ├── RULES.md
    ├── references/
    └── assets/
```

---

## 🎯 File Naming Standards

As per `CLAUDE.md`:

- **ALWAYS use English** for all file and directory names
- **NEVER use Chinese characters** in file names
- **Use PascalCase** for Frontend Components (Exception: index files use lowercase)
- **Use camelCase** for page files
- **Use UPPER_SNAKE_CASE** for README files

---

## 🔧 Skill Structure

Each skill follows this standard structure:

```
skill-name/
├── SKILL.md              # Required - main skill file with YAML frontmatter
├── RULES.md              # Optional - specific rules for this skill
├── scripts/              # Optional - executable Python/Bash scripts
│   └── *.py or *.sh
├── references/           # Optional - detailed documentation (loaded as needed)
│   └── *.md
└── assets/               # Optional - templates, configs, files
    └── * (any file type)
```

### SKILL.md Format

```markdown
---
name: skill-name
description: Brief description (20-120 chars, starts with verb)
---

# Skill Title

## Overview
[1-2 sentences explaining purpose]

## When to Use
[Specific use cases]

## Main Content
[Instructions, guidelines, examples]

## Resources
[Reference to scripts/references/assets]
```

---

## 💡 Best Practices

### Installation Tips

1. **Selective Installation**: Only install skills you need for your project
2. **Check Dependencies**: Some skills reference shared resources
3. **Rule Conflicts**: Avoid conflicting rules from different skills
4. **Regular Updates**: Pull latest changes from this repo

### Usage Tips

1. **Skill Triggers**: Skills activate when Claude detects relevant keywords
2. **Explicit Requests**: You can explicitly call skills: "Use the frontend-standard skill to review this"
3. **Combine Skills**: Multiple skills can work together in a project
4. **Customize**: Fork and modify skills for your team's needs

### Maintenance

1. **Validate After Changes**: Run validation scripts after modifying skills
2. **Document Changes**: Update SKILL.md when making modifications
3. **Version Control**: Track your `.claude/` directory in git
4. **Share With Team**: Package and distribute custom skills to your team

---

## 🤝 Contributing

### Creating New Skills

Follow the skill-creator guidelines:

```bash
# 1. Initialize
python .claude/skills/skill-creator/scripts/init_skill.py my-skill --path skills/

# 2. Edit SKILL.md and add resources

# 3. Validate
python .claude/skills/skill-creator/scripts/quick_validate.py skills/my-skill

# 4. Package
python .claude/skills/skill-creator/scripts/package_skill.py skills/my-skill
```

### Quality Standards

- ✅ YAML frontmatter with `name` and `description`
- ✅ Lowercase hyphen-case naming
- ✅ Clear "When to Use" section
- ✅ Imperative writing style
- ✅ Referenced resources documented

---

## 📝 License

[Your License Here]

---

## 🆘 Support

For questions or issues:

1. Check individual skill documentation
2. Review the skill-creator guides
3. Consult `.claude/rules/skill-creator-rules.md`
4. Open an issue in this repository

---

## 🔄 Version History

**Current Version**: 1.0.0
**Last Updated**: 2026-01-21

### Changelog

- **1.0.0** - Initial release with frontend, architecture, CMS, schema, and deployment skills

---

**Happy Coding with Claude! 🚀**
