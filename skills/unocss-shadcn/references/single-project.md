# Single-Project Flow

## Detection
Use this branch when strict monorepo signals are absent:
- No root `pnpm-workspace.yaml`
- Root `package.json` has no `workspaces`

Even if `packages/` exists, keep this branch unless strict signals exist.

## Destination
Use `src/components` for shadcn component files.

Recommended structure:
- `src/components/ui/*`
- `src/lib/*` (optional)

## Dependency Policy
Keep project runtime dependencies in normal `dependencies` (not `peerDependencies`).

Example template:
```json
{
  "dependencies": {
    "react": "^18 || ^19",
    "react-dom": "^18 || ^19"
  },
  "devDependencies": {
    "unocss": "<version>",
    "unocss-preset-shadcn": "<version>"
  }
}
```

Use shadcn MCP outputs to decide additional component-specific dependencies.

## UnoCSS Preset Patch Template
Patch existing `uno.config.*` or `unocss.config.*` by adding preset import and registration.

Default to `presetWind4`. Only use `presetWind3` or other versions if the user explicitly requests it.

Example:
```ts
import { defineConfig, presetWind4 } from 'unocss'
import presetShadcn from 'unocss-preset-shadcn'

export default defineConfig({
  presets: [
    presetWind4(),
    presetShadcn(),
  ],
})
```

Preserve existing config and append minimal changes only.

## Component Creation and Usage
1. Run shadcn MCP chain first.
2. Fetch example code from MCP.
3. Create or update component files manually under `src/components`.
4. Do not use default Tailwind-oriented auto init as the primary path.

## Suggested Commands (Do Not Auto-Run)
Use project package manager placeholder `<pm>`.

- Add UnoCSS core:
`<pm> add -D unocss`

- Add shadcn preset:
`<pm> add -D unocss-preset-shadcn`
