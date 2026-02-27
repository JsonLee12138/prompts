# Validation Checklist

## Preflight
- Confirm `package.json` exists.
- Detect monorepo strictly:
- `pnpm-workspace.yaml` OR root `package.json.workspaces`.
- Confirm UnoCSS config file exists, or prepare minimal config template.
- Confirm shadcn MCP is available before component actions.

## Configuration Checks
- `unocss-preset-shadcn` is imported in UnoCSS config.
- `presetShadcn()` appears in `presets`.
- `presetWind4` is used by default. `presetWind3` or others only if user explicitly requested.
- Monorepo: UnoCSS config is in `apps/<app>/uno.config.*`, NOT at repo root.
- Existing UnoCSS config behavior is preserved (minimal diff).

## Path and Dependency Checks
- Monorepo branch:
- Components target `packages/shadcn-ui`.
- shadcn runtime deps are in `peerDependencies`.
- Single-project branch:
- Components target `src/components`.
- Runtime deps remain in `dependencies`.

## MCP and Manual-Mode Checks
- MCP chain was executed before component create/use.
- Component API and examples come from MCP output.
- Creation path is manual mode.
- If MCP was unavailable, component step was blocked with explicit error.

## Failure and Remediation Matrix
- Missing `package.json`:
- Stop and ask for project initialization.
- Missing UnoCSS config:
- Provide minimal config template; do not invent framework-specific boilerplate.
- Monorepo ambiguity (only `packages/` exists):
- Treat as single-project and explain strict rule.
- Dependency conflict in existing manifest:
- Report conflict and request explicit version decision.
- Existing target directory conflicts:
- Avoid destructive overwrite; propose migration steps.
