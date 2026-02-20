# Skills 安装
[English Document](./README.md)

本仓库包含以下 skills：

- `components`
- `design-patterns-principles`
- `eslint-config`

更多用法参考 [skills 文档](https://github.com/vercel-labs/skills)。

## 快速安装（交互）

```bash
npx skills add JsonLee12138/prompts
```

## 列出可安装技能

```bash
npx skills add JsonLee12138/prompts --list
```

## 安装全部技能

```bash
npx skills add JsonLee12138/prompts --all
```

## 安装指定技能

```bash
npx skills add JsonLee12138/prompts \
  --skill components \
  --skill design-patterns-principles \
  --skill eslint-config
```

## 从本地当前目录安装

```bash
npx skills add .
```

## 常用选项

- `-a, --agent <agents...>`：仅安装到指定 agent（例如 `claude-code`、`codex`）
- `-g, --global`：安装到全局目录
- `-y, --yes`：跳过交互确认
