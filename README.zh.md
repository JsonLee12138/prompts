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

核心能力：
- 创建/删除角色 worktree（`team/<name>`）
- 打开角色会话（`claude`/`codex`/`opencode`）
- 派发任务并向会话发送消息（`assign`/`reply`）
- 查看状态、合并角色分支

### 依赖工具
- Git: https://git-scm.com/
- WezTerm（默认后端）: https://wezfurlong.org/wezterm/installation.html
- tmux（可选后端）: https://github.com/tmux/tmux/wiki/Installing
- Python 3: https://www.python.org/downloads/

### 提示词优先用法（推荐）
建议通过 AI 提示词触发 `solo-ops` 工作流，而不是手动运行 Python 命令。

示例提示词：
```text
请在当前仓库使用 `solo-ops` 协调 PR #142 的评审。
1. 创建 3 个角色：`sec-review`、`perf-review`、`test-review`。
2. 打开这 3 个角色会话（默认使用 claude）。
3. 分别派发任务：
   - sec-review：检查安全影响和高风险改动
   - perf-review：评估性能影响与潜在热点
   - test-review：核对测试覆盖率与缺失用例
4. 等待各角色回传结果后，汇总一份总报告，至少包含：
   - 严重问题
   - 中风险问题
   - 修复建议
5. 最后输出角色状态和 pending 任务数量。
```

```text
请使用 `solo-ops` 查看当前团队角色状态和待办任务数量。
```

```text
请使用 `solo-ops` 清理已合并完成的角色。
```

### 在提示词中指定 tmux 后端
```bash
# 可用自然语言直接指定：
# “请用 tmux 后端运行 solo-ops 并打开评审角色会话。”
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
