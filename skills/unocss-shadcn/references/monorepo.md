# Monorepo Flow

## Detection
Treat the project as monorepo only if one of these is true:
- Root `pnpm-workspace.yaml` exists.
- Root `package.json` has `workspaces`.

If neither exists, do not use this branch.

## Destination
Use `packages/shadcn-ui` as the component package root.

Recommended structure:
- `packages/shadcn-ui/package.json`
- `packages/shadcn-ui/src/components/*`
- `packages/shadcn-ui/src/lib/*` (optional)

## Dependency Policy
Write shadcn-related runtime dependencies into `peerDependencies` of `packages/shadcn-ui/package.json`.

Example template:
```json
{
  "name": "@your-scope/shadcn-ui",
  "version": "0.0.0",
  "peerDependencies": {
    "react": "^18 || ^19",
    "react-dom": "^18 || ^19"
  }
}
```

Derive exact component dependencies from shadcn MCP outputs. Do not guess dependency names or versions.

## UnoCSS Preset Patch Template
Patch existing `uno.config.*` or `unocss.config.*` by adding preset import and registration.

Example:
```ts
import { defineConfig, presetWind3 } from 'unocss'
import presetShadcn from 'unocss-preset-shadcn'

export default defineConfig({
  presets: [
    presetWind3(),
    presetShadcn(),
  ],
})
```

Keep existing presets/rules/shortcuts intact. Add minimal diff only.

## Component Creation and Usage
1. Run shadcn MCP chain first.
2. Fetch example code from MCP.
3. Create or update component files manually under `packages/shadcn-ui/src/components`.
4. Avoid Tailwind-first auto init flows.

## Suggested Commands (Do Not Auto-Run)
Use project package manager placeholder `<pm>`.

- Add UnoCSS core:
`<pm> add -D unocss`

- Add shadcn preset:
`<pm> add -D unocss-preset-shadcn`

- Install peer dependencies in each consumer app:
`<pm> add react react-dom`

Adjust commands to workspace manager syntax (`pnpm -w`, `pnpm --filter`, etc.) as needed.
