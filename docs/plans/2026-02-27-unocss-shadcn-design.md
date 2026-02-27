# unocss-shadcn Design

**Date:** 2026-02-27
**Owner:** Codex
**Status:** Approved

## Goal
Create a new reusable skill named `unocss-shadcn` that configures UnoCSS plus `unocss-preset-shadcn` with a deterministic monorepo/single-project routing strategy.

## Scope
- Semi-automatic mode only: generate file edits and command suggestions, but do not auto-install dependencies.
- Framework-agnostic behavior.
- Strict monorepo detection only:
  - `pnpm-workspace.yaml` exists, or
  - root `package.json` has `workspaces`.
- Path policy:
  - Monorepo -> `packages/shadcn-ui`
  - Single project -> `src/components`

## Architecture
### Skill package layout
- `skills/unocss-shadcn/SKILL.md`
- `skills/unocss-shadcn/references/monorepo.md`
- `skills/unocss-shadcn/references/single-project.md`
- `skills/unocss-shadcn/references/checklist.md`

### Runtime workflow
1. Inspect project files (`package.json`, `pnpm-workspace.yaml`, `uno.config.*` or `unocss.config.*`, `components.json`).
2. Decide project type with strict rule.
3. Produce configuration edits and install commands (commands are suggested only).
4. Enforce dependency placement policy.
5. Output verification checklist and remediation hints.

## shadcn MCP integration (mandatory)
- Any action that uses or creates shadcn components must call shadcn MCP first.
- Minimum MCP chain:
  1. `get_project_registries`
  2. `search_items_in_registries` or `list_items_in_registries`
  3. `get_item_examples_from_registries`
  4. Optional: `get_add_command_for_items` as reference only
- Creation mode must be **manual** (no default Tailwind-oriented shadcn init flow).
- If MCP is unavailable, block the component step and return an explicit error.

## Error handling
1. Missing UnoCSS config: provide minimal config template.
2. Missing `package.json`: stop and request project initialization.
3. Directory-only monorepo signal (`packages/`) without strict signals: treat as single project and explain why.
4. Existing dependency conflicts: do not force-write; output conflict resolution instructions.
5. Existing directory structure conflicts: avoid destructive overwrite; output migration suggestions.

## Validation cases
- Case A: single project -> `src/components`
- Case B: monorepo by `pnpm-workspace.yaml` -> `packages/shadcn-ui` + `peerDependencies`
- Case C: monorepo by `package.json.workspaces` -> same as Case B
- Case D: only `packages/` exists -> still single project path

## Acceptance criteria
- Skill trigger description clearly covers UnoCSS + shadcn preset setup and MCP/manual constraints.
- Skill body stays concise and delegates branch details to references files.
- Monorepo/single-project instructions are deterministic and non-ambiguous.
- MCP requirement and manual-mode constraint are explicit and non-optional.
