# Skills Installation
[中文文档](./README.zh.md)

This repository includes the following skills (current `skills/` directory only):

- `components`
- `design-patterns-principles`
- `eslint-config`
- `solo-ops`

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
  --skill eslint-config \
  --skill solo-ops
```

## Install From Local Directory

```bash
npx skills add .
```

## Common Options

- `-a, --agent <agents...>`: install only for specific agents (e.g. `claude-code`, `codex`)
- `-g, --global`: install to global directory
- `-y, --yes`: skip confirmation prompts

## Skills Usage Index
- [components](#components)
- [design-patterns-principles](#design-patterns-principles)
- [eslint-config](#eslint-config)
- [solo-ops](#solo-ops)

## components
Use when designing, implementing, or reviewing React/TypeScript components with naming conventions, props typing, hooks usage, and UnoCSS styling standards.

Quick workflow:
1. Define component type and responsibility (UI/business/container/page/layout).
2. Define props and dependencies explicitly.
3. Implement with typed props and function components.
4. Apply UnoCSS classes and CSS variables.
5. Review against checklist.

References:
- `skills/components/references/standards.md`
- `skills/components/references/checklist.md`
- `skills/components/references/templates.md`

## design-patterns-principles
Use when a request asks for software design patterns or design principles, including explanations, comparisons, summaries, or quick reference grounded in local docs.

Quick workflow:
1. Identify scope: patterns, principles, or both.
2. Load references.
3. Respond in concise Chinese sections.
4. If user asks for depth/examples, ask one clarifying question and then expand.

References:
- `skills/design-patterns-principles/references/design-patterns.md`
- `skills/design-patterns-principles/references/design-principles.md`

## eslint-config
Use when configuring ESLint with `@antfu/eslint-config` for a single project or monorepo workspace, including flat config setup and optional commit quality hooks.

Quick workflow:
1. Choose single-project or workspace package mode.
2. Install dependencies.
3. Create `eslint.config.js`.
4. Add lint scripts.
5. Run lint verification.
6. Optionally add `commitlint + husky + lint-staged`.

References:
- `skills/eslint-config/references/single-project.md`
- `skills/eslint-config/references/workspace.md`
- `skills/eslint-config/references/vscode-settings.md`
- `skills/eslint-config/references/commit-quality.md`

## solo-ops
`solo-ops` manages multi-agent role workflows with git worktrees + terminal sessions.

Core features:
- Create roles and isolated worktrees (`team/<name>`)
- Open role sessions (`claude` / `codex` / `opencode`)
- Assign tasks to a role and send controller replies
- Check team status and pending tasks
- Merge completed role branches and delete finished roles

### Required tools
- Git: https://git-scm.com/
- WezTerm (default backend): https://wezfurlong.org/wezterm/installation.html
- tmux (supported backend): https://github.com/tmux/tmux/wiki/Installing
- Python 3: https://www.python.org/downloads/

### How to use
Use `/solo-ops` prompts directly in chat.  
You do not need to run `python` commands manually for normal usage.

### Simple example
```text
/solo-ops Create a review team for PR #142 with three roles:
- sec-review (security)
- perf-review (performance)
- test-review (test coverage)
Open the roles, assign one task to each role, and report final findings with role status.
```

If you cannot see the opened tmux session, it is usually detached by default. Switch/attach manually:
```bash
tmux list-sessions
tmux switch-client -t <session_name_or_id>   # inside tmux
tmux attach -t <session_name_or_id>          # from regular terminal
```

Related files:
- `skills/solo-ops/SKILL.md`
- `skills/solo-ops/scripts/solo_ops.py`
- `skills/solo-ops/scripts/solo_ops_tmux.py`
- `skills/solo-ops/references/details.md`
