# Claude Code Rules - File Naming Conventions

## 📋 File Naming Standards

### General Rules
- **ALWAYS use English** for all file and directory names
- **NEVER use Chinese characters** in file names
- **Use kebab-case** for multi-word names: `quick-start.md`, `docker-compose.yaml`
- **Use snake_case** when kebab-case is not supported: `ecosystem.config.js`
- **Keep names lowercase** (except for acronyms in specific contexts)

### File Extensions
- Markdown files: `.md`
- YAML files: `.yaml` or `.yml`
- JavaScript files: `.js`
- Shell scripts: `.sh`
- Dockerfile: `Dockerfile` (no extension)
- Makefile: `Makefile` (no extension)

### Directory Structure
```
deployment-docs/
├── README.md                          # Main documentation
├── overview.md                        # Overview/summary
├── summary.md                         # Summary of changes
├── cleanup-old-docs.sh                # Cleanup script
│
├── docs/                              # Documentation directory
│   ├── quickstart.md                  # Quick start guide
│   └── file-list.md                   # File inventory
│
└── templates/                         # Template files
    ├── Makefile.template              # Generic Makefile
    ├── Dockerfile.go                  # Go project
    ├── Dockerfile.python              # Python project
    ├── Dockerfile.node-pm2            # Node.js with PM2
    ├── Dockerfile.nextjs-nginx        # Next.js with Nginx
    ├── Dockerfile.java                # Java Spring Boot
    ├── Dockerfile.rust                # Rust project
    ├── docker-compose.local.yaml.template
    ├── docker-compose.test.yaml.template
    ├── docker-compose.yaml.template
    ├── ecosystem.config.js            # PM2 config
    ├── nginx.conf.template            # Nginx config
    ├── nginx.entrypoint.sh            # Nginx entrypoint
    └── README.md                      # Template instructions
```

### Naming Patterns by File Type

#### Documentation Files
- `README.md` - Main documentation
- `quickstart.md` - Quick start guide
- `overview.md` - Overview document
- `summary.md` - Summary document
- `file-list.md` - File inventory

#### Template Files
- `Makefile.template` - Makefile template
- `Dockerfile.{stack}` - Stack-specific Dockerfile
- `docker-compose.{env}.yaml.template` - Environment-specific compose
- `{name}.config.js` - Configuration files
- `{name}.conf.template` - Config templates
- `{name}.entrypoint.sh` - Entrypoint scripts

#### Shell Scripts
- Use kebab-case: `cleanup-old-docs.sh`
- Make executable: `chmod +x script.sh`

### Examples

#### ✅ Correct
```
README.md
quickstart.md
docker-compose.yaml
Dockerfile.go
ecosystem.config.js
cleanup-old-docs.sh
```

#### ❌ Incorrect
```
快速开始.md          # Chinese characters
README-EN.md        # Unnecessary suffix
Dockerfile.Golang   # Wrong case
docker_compose.yaml # Wrong separator
清理脚本.sh          # Chinese characters
```

### Git Commit Messages
- Use English
- Use conventional commit format: `type: description`
- Examples:
  - `docs: update quickstart guide`
  - `feat: add Rust Dockerfile template`
  - `fix: correct Makefile port configuration`

### Why These Rules?
1. **Consistency** - All team members use same naming convention
2. **Compatibility** - Avoids issues with different operating systems
3. **Automation** - Scripts can reliably find files
4. **Professionalism** - English is standard in software development
5. **Searchability** - Easier to search and reference

### Quick Reference
```
# Documentation
README.md
quickstart.md
overview.md
summary.md

# Templates
Makefile.template
Dockerfile.{stack}
docker-compose.{env}.yaml.template

# Configs
ecosystem.config.js
nginx.conf.template

# Scripts
cleanup-old-docs.sh
```

---
**Last Updated**: 2026-01-12
**Version**: 1.0
**Author**: Claude Code Rules