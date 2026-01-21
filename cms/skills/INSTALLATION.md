# CMS Skills Installation Guide

This guide explains how to install and use the CMS Skills collection with Claude Code.

## 📦 What's Included

These skills are now part of the unified CMS directory:

```
cms/
├── docs/                              # Original documentation
│   ├── CMS_CODING_STANDARD.md         # Go backend standards (59KB)
│   ├── CMS_RESPONSE.md                # HTTP response format (10KB)
│   └── SCHEMA_DRIVEN_DEVELOPMENT.md   # Schema workflow (39KB)
│
├── skills/                            # Claude Skills (this directory)
│   ├── README.md                      # Skills overview
│   ├── CLAUDE_USAGE.md                # Usage examples & patterns
│   ├── INSTALLATION.md                # This file
│   ├── SUMMARY.md                     # Skills summary
│   ├── validate-skills.sh             # Validation script
│   │
│   ├── cms-coding-standard/
│   │   └── SKILL.md                   # Go backend standards
│   ├── cms-response-format/
│   │   └── SKILL.md                   # HTTP response patterns
│   └── schema-driven-development/
│       └── SKILL.md                   # Schema workflow
│
├── README.md                          # Main overview
└── INDEX.md                           # Quick reference
```

## 🎯 How to Use

### Option 1: Direct Reference (Recommended)

In Claude Code, simply reference the skills using `@cms/` prefix:

```bash
# Reference a specific skill
@cms/cms-coding-standard

# Ask questions
@cms/cms-coding-standard How do I create a new module?

# Combine skills
@cms/schema-driven-development @cms/cms-response-format
```

### Option 2: Copy to Claude Skills Directory

If you want to install these as global Claude skills:

```bash
# Find your Claude skills directory
# Usually: ~/.claude/skills/ or ~/.anthropic/skills/

# Copy the skills
cp -r /Users/jsonlee/Projects/prompts/cms-skills/cms-coding-standard ~/.claude/skills/
cp -r /Users/jsonlee/Projects/prompts/cms-skills/cms-response-format ~/.claude/skills/
cp -r /Users/jsonlee/Projects/prompts/cms-skills/schema-driven-development ~/.claude/skills/

# Then use without path
cms-coding-standard
```

## 🔍 Verify Installation

Run the validation script:

```bash
cd /Users/jsonlee/Projects/prompts/cms/skills
./validate-skills.sh
```

Expected output:
```
✅ All skills are valid!

Available skills:
  - @cms/cms-coding-standard: [description]
  - @cms/cms-response-format: [description]
  - @cms/schema-driven-development: [description]
```

## 🚀 Quick Test

Try these commands in Claude Code:

```bash
# Test 1: Module creation workflow
@cms/schema-driven-development Show me the complete workflow to create a "Product" module

# Test 2: Backend implementation
@cms/cms-coding-standard What are the 4 core files I need for a Product module?

# Test 3: Frontend integration
@cms/cms-response-format How do I fetch and display products in React?
```

## 📚 Documentation

- **README.md** - Overview and available skills
- **CLAUDE_USAGE.md** - Detailed usage examples and patterns
- **INSTALLATION.md** - This file

## 🎯 What Each Skill Does

### 1. cms-coding-standard
**Purpose**: Go backend development standards

**Includes**:
- NestJS-style module architecture
- Ent ORM best practices
- Chi framework patterns
- API Key & JWT authentication
- Multi-tenancy implementation
- Security guidelines
- Code review checklist

**Use for**:
- Creating new modules
- Code review
- Architecture decisions
- Backend troubleshooting

### 2. cms-response-format
**Purpose**: Standardized API responses

**Includes**:
- Strapi-style response structure
- TypeScript interfaces
- Go implementation
- Frontend integration patterns
- React hooks & components
- Error handling
- Debugging with TraceId

**Use for**:
- Building API clients
- Creating frontend components
- Implementing backend responses
- Debugging API issues

### 3. schema-driven-development
**Purpose**: Schema-based前后端同步开发

**Includes**:
- Schema as single source of truth
- Schema API endpoints
- Validation rules mapping
- Dynamic table generation
- Dynamic form generation
- Zod schema generation
- Complete workflow examples

**Use for**:
- Module creation
- Data modeling
- UI generation
- API design

## 🔧 Configuration

### For Local Development
The skills are already configured to work from `/Users/jsonlee/Projects/prompts/cms/skills/`

### For Team Sharing
1. Commit the `cms/` directory to your project
2. Team members can reference skills using relative paths
3. Or copy to their local Claude skills directory

### For Different Projects
You can have multiple skill collections:
```bash
project-a/
└── skills/
    └── cms/          # CMS-specific skills

project-b/
└── skills/
    └── api/          # API-specific skills
```

## 📝 Updating Skills

When you update the original documentation:

```bash
# 1. Update the original .md files in cms/docs/
vim /Users/jsonlee/Projects/prompts/cms/docs/CMS_CODING_STANDARD.md

# 2. Regenerate the SKILL.md files
# (Manual process - copy relevant sections to SKILL.md)

# 3. Update version numbers
vim /Users/jsonlee/Projects/prompts/cms/skills/*/SKILL.md

# 4. Validate
./validate-skills.sh
```

## 🎓 Learning Resources

### Start Here
1. Read `README.md` for overview
2. Check `CLAUDE_USAGE.md` for examples
3. Try the quick test commands

### Deep Dive
- **Backend**: `@cms/cms-coding-standard`
- **Frontend**: `@cms/cms-response-format`
- **Architecture**: `@cms/schema-driven-development`

### Common Workflows
- **New Module**: All three skills combined
- **Code Review**: `cms-coding-standard`
- **API Issues**: `cms-response-format`
- **Data Modeling**: `schema-driven-development`

## 🆘 Troubleshooting

### Skills not found?
```bash
# Check the skill files exist
ls -la /Users/jsonlee/Projects/prompts/cms/skills/*/SKILL.md

# Validate format
./validate-skills.sh
```

### Reference errors?
```bash
# Use exact path
@/Users/jsonlee/Projects/prompts/cms/skills/cms-coding-standard/SKILL.md

# Or use the @cms/ prefix (if configured)
@cms/cms-coding-standard
```

### Need to see all skills?
```bash
cat /Users/jsonlee/Projects/prompts/cms/skills/README.md
```

## ✅ Success Checklist

- [ ] Skills directory exists
- [ ] All SKILL.md files are valid
- [ ] Validation script passes
- [ ] Can reference skills in Claude Code
- [ ] Understand when to use each skill
- [ ] Know how to combine skills

## 🚀 Ready to Go!

You're all set! Start using the skills:

```bash
@cms/schema-driven-development What's the first step in creating a new module?
```

Happy coding! 🎉