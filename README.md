# Skills Installation
[中文文档](./README.zh.md)

This repository includes the following skills (current `skills/` directory only):

- `actions-npm`
- `brainstorming`
- `components`
- `design-patterns-principles`
- `eslint-config`
- `makefile`
- `solo-ops`
- `unocss-shadcn`
- `vite-tanstack`

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
  --skill actions-npm \
  --skill brainstorming \
  --skill components \
  --skill design-patterns-principles \
  --skill eslint-config \
  --skill makefile \
  --skill solo-ops \
  --skill unocss-shadcn \
  --skill vite-tanstack
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
- [actions-npm](#actions-npm)
- [brainstorming](#brainstorming)
- [components](#components)
- [design-patterns-principles](#design-patterns-principles)
- [eslint-config](#eslint-config)
- [makefile](#makefile)
- [solo-ops](#solo-ops)
- [unocss-shadcn](#unocss-shadcn)
- [vite-tanstack](#vite-tanstack)

## actions-npm
Use when creating GitHub Actions workflows for npm package publishing with OIDC provenance, especially tag-triggered release pipelines that avoid `NPM_TOKEN`.

Quick workflow:
1. Copy `assets/release-npm.yml` into `.github/workflows/`.
2. Ensure workflow permissions include `id-token: write`.
3. Explicitly set `NODE_AUTH_TOKEN: ""`.
4. Upgrade npm to v11+ before publish.
5. Ensure `package.json.repository` matches `github.com/<owner>/<repo>`.
6. Publish with provenance enabled and without `NPM_TOKEN`.

Related files:
- `skills/actions-npm/SKILL.md`
- `skills/actions-npm/assets/release-npm.yml`

## brainstorming
Use this before any creative work (features/components/behavior changes) to turn rough ideas into approved brainstorming/design docs through one-question-at-a-time dialogue.

Quick workflow:
1. Explore project context (files/docs/recent commits).
2. Ask one clarifying question at a time.
3. Propose 2-3 approaches with trade-offs and recommendation.
4. Present design sections and get approval.
5. Ask where to save before writing:
6. Default: `docs/brainstorming/`
7. Or user-provided custom directory.
8. Write and deliver the brainstorming doc, then stop (no implementation planning step).

Related files:
- `skills/brainstorming/SKILL.md`
- `skills/brainstorming/agents/openai.yaml`

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

## makefile
Use when creating or editing Makefiles that need an auto-generated help target. Covers inline `## comment` convention for self-documenting Makefiles.

Quick workflow:
1. Set `.DEFAULT_GOAL := help`.
2. Declare all non-file targets in `.PHONY`.
3. Write `## 描述` on the same line as each target.
4. Include the standard `help` target with grep/sed/awk pipeline.

Related files:
- `skills/makefile/SKILL.md`

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

## unocss-shadcn
Configure UnoCSS with `unocss-preset-shadcn` in a semi-automatic, framework-agnostic workflow.

Quick workflow:
1. Detect project shape strictly (`pnpm-workspace.yaml` or root `package.json.workspaces`).
2. Patch `uno.config.*` / `unocss.config.*` to include `unocss-preset-shadcn`.
3. Route components by project type:
4. Monorepo -> `packages/shadcn-ui` with `peerDependencies`.
5. Single project -> `src/components`.
6. Use shadcn MCP chain before component usage/creation.
7. Create components in manual mode (no default Tailwind-oriented init flow).
8. If MCP is unavailable, block component operations and report error.

References:
- `skills/unocss-shadcn/SKILL.md`
- `skills/unocss-shadcn/references/monorepo.md`
- `skills/unocss-shadcn/references/single-project.md`
- `skills/unocss-shadcn/references/checklist.md`

## vite-tanstack
TanStack (Router/Query/Form/Table) configuration guide for Vite + React projects. Use when setting up or reviewing TanStack config in a Vite project.

Quick workflow:
1. Specify modules needed: `router`, `query`, `form`, `table` (or `all`).
2. Register `@tanstack/devtools-vite` plugin in `vite.config.ts`.
3. Set up `TanStackDevtools` component in `main.tsx`.
4. Configure each module's provider in correct nesting order.
5. Verify against compliance checklist.

Usage examples:
- `/vite-tanstack router query` — load Router + Query references
- `/vite-tanstack all` — load all four module references
- `/vite-tanstack` — interactively choose modules

References:
- `skills/vite-tanstack/SKILL.md`
- `skills/vite-tanstack/references/router.md`
- `skills/vite-tanstack/references/query.md`
- `skills/vite-tanstack/references/form.md`
- `skills/vite-tanstack/references/table.md`
