# TanStack Router — Vite Configuration

## 1. Vite Plugin

In `vite.config.ts`, register `@tanstack/router-plugin/vite`:

```ts
import { tanstackRouter } from '@tanstack/router-plugin/vite';
import { join, resolve } from 'node:path';

const srcDir = resolve(__dirname, './src');

export default defineConfig({
  plugins: [
    tanstackRouter({
      target: 'react',
      autoCodeSplitting: true,
      routesDirectory: join(srcDir, './pages'),
      quoteStyle: 'single',
    }),
    // devtools plugin (see SKILL.md shared config)
    // react plugin must come AFTER tanstackRouter
  ],
});
```

**Key options:**
- `target`: `'react'` for React projects
- `autoCodeSplitting`: `true` enables automatic lazy loading per route
- `routesDirectory`: points to the file-based routes directory (e.g., `src/pages`)
- `quoteStyle`: `'single'` to match project style

**Plugin order matters:** `tanstackRouter` should be registered **before** `react()` plugin.

## 2. main.tsx Registration

```tsx
import { createRouter, RouterProvider } from '@tanstack/react-router';
import { routeTree } from './routeTree.gen';

// Create router instance
const router = createRouter({ routeTree });

// TypeScript module augmentation for type-safe routing
declare module '@tanstack/react-router' {
  interface Register {
    router: typeof router;
  }
}

// In render tree:
<RouterProvider router={router} />
```

**Notes:**
- `routeTree` is auto-generated from files in `routesDirectory` — never edit `routeTree.gen.ts` manually
- The `declare module` augmentation enables type-safe `useNavigate`, `useParams`, `Link`, etc.
- `RouterProvider` should be nested inside `QueryClientProvider` (if using query)

## 3. DevTools Panel

```tsx
import { TanStackRouterDevtoolsPanel } from '@tanstack/react-router-devtools';

// As a plugin in TanStackDevtools:
{
  name: 'Tanstack Router',
  render: <TanStackRouterDevtoolsPanel router={router} />,
}
```

**Note:** The `router` instance must be passed to the devtools panel.

## 4. VSCode Settings

Add to `.vscode/settings.json` to prevent editing and unnecessary indexing of the generated route tree:

```json
{
  "files.readonlyInclude": {
    "**/routeTree.gen.ts": true
  },
  "files.watcherExclude": {
    "**/routeTree.gen.ts": true
  },
  "search.exclude": {
    "**/routeTree.gen.ts": true
  }
}
```

## Compliance Checklist

- [ ] `tanstackRouter` plugin registered before `react()` in vite plugins array
- [ ] `routesDirectory` points to correct pages directory
- [ ] `autoCodeSplitting` enabled
- [ ] `quoteStyle` matches project convention
- [ ] `routeTree.gen.ts` imported (not manually created)
- [ ] `declare module '@tanstack/react-router'` type augmentation present
- [ ] `RouterProvider` receives `router` instance
- [ ] Router DevTools panel receives `router` prop
- [ ] VSCode settings configured for `routeTree.gen.ts` (readonly, watcher exclude, search exclude)
