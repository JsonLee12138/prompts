# Skills 安装
[English Document](./README.md)

本仓库当前 `skills/` 目录包含以下技能：

- `components`
- `design-patterns-principles`
- `eslint-config`
- `solo-ops`

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
  --skill eslint-config \
  --skill solo-ops
```

## 从本地当前目录安装

```bash
npx skills add .
```

## 常用选项

- `-a, --agent <agents...>`：仅安装到指定 agent（例如 `claude-code`、`codex`）
- `-g, --global`：安装到全局目录
- `-y, --yes`：跳过交互确认

## Skills 使用目录
- [components](#components)
- [design-patterns-principles](#design-patterns-principles)
- [eslint-config](#eslint-config)
- [solo-ops](#solo-ops)

## components
适用场景：设计、实现或评审 React/TypeScript 组件时，统一命名规范、Props 类型、Hooks 用法和 UnoCSS 风格。

快速流程：
1. 明确组件类型与职责（UI/业务/容器/页面/布局）。
2. 明确 props 与依赖。
3. 使用强类型函数组件实现。
4. 使用 UnoCSS 类与 CSS 变量。
5. 对照清单做评审。

参考文件：
- `skills/components/references/standards.md`
- `skills/components/references/checklist.md`
- `skills/components/references/templates.md`

## design-patterns-principles
适用场景：用户需要设计模式或设计原则的解释、对比、总结、速查。

快速流程：
1. 识别范围：仅模式、仅原则、或两者都要。
2. 加载对应参考文档。
3. 用简洁中文结构化输出。
4. 若用户要求更深入示例，先补一个澄清问题再展开。

参考文件：
- `skills/design-patterns-principles/references/design-patterns.md`
- `skills/design-patterns-principles/references/design-principles.md`

## eslint-config
适用场景：基于 `@antfu/eslint-config` 配置 ESLint（单项目或 Monorepo），以及可选的提交质量钩子。

快速流程：
1. 选择单项目模式或工作区共享配置模式。
2. 安装依赖。
3. 创建 `eslint.config.js`。
4. 配置 lint 脚本。
5. 运行 lint 验证。
6. 可选：接入 `commitlint + husky + lint-staged`。

参考文件：
- `skills/eslint-config/references/single-project.md`
- `skills/eslint-config/references/workspace.md`
- `skills/eslint-config/references/vscode-settings.md`
- `skills/eslint-config/references/commit-quality.md`

## solo-ops
`solo-ops` 用于多角色协作开发：基于 git worktree + 终端会话管理角色，并支持任务派发与回复。

核心功能：
- 创建角色与隔离 worktree（`team/<name>`）
- 打开角色会话（`claude` / `codex` / `opencode`）
- 给角色派发任务并发送主控回复
- 查看团队状态与待办任务数量
- 合并角色分支并删除已完成角色

### 依赖工具
- Git: https://git-scm.com/
- WezTerm（默认后端）: https://wezfurlong.org/wezterm/installation.html
- tmux（可选后端）: https://github.com/tmux/tmux/wiki/Installing
- Python 3: https://www.python.org/downloads/

### 使用方式
在对话中直接使用 `/solo-ops` 相关提示词即可。  
正常使用不需要手动运行 `python` 命令。

### 简单示例
```text
/solo-ops 请为 PR #142 创建评审小组，包含三个角色：
- sec-review（安全）
- perf-review（性能）
- test-review（测试覆盖）
请打开角色会话、分别派发任务，并在最后输出汇总结论和角色状态。
```

如果你没有看到新开的 tmux 会话，通常是因为默认以 detached 方式启动。可手动切换/附着：
```bash
tmux list-sessions
tmux switch-client -t <session_name_or_id>   # 在 tmux 内
tmux attach -t <session_name_or_id>          # 在普通终端
```

相关文件：
- `skills/solo-ops/SKILL.md`
- `skills/solo-ops/scripts/solo_ops.py`
- `skills/solo-ops/scripts/solo_ops_tmux.py`
- `skills/solo-ops/references/details.md`
