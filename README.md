# Skills Installation
[中文文档](./README.zh.md)

This repository includes the following skills:

- `components`
- `design-patterns-principles`
- `eslint-config`

See the [skills documentation](https://github.com/vercel-labs/skills) for more usage details.

## Quick Install (interactive)

```bash
npx skills add JsonLee12138/prompts
```

## List Available Skills

```bash
npx skills add JsonLee12138/prompts --list
```

## Install All Skills

```bash
npx skills add JsonLee12138/prompts --all
```

## Install Specific Skills

```bash
npx skills add JsonLee12138/prompts \
  --skill components \
  --skill design-patterns-principles \
  --skill eslint-config
```

## Install From Local Directory

```bash
npx skills add .
```

## Common Options

- `-a, --agent <agents...>`: install only for specific agents (e.g. `claude-code`, `codex`)
- `-g, --global`: install to global directory
- `-y, --yes`: skip confirmation prompts
