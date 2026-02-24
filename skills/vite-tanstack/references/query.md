# TanStack Query — Vite Configuration

## 1. Vite Plugin

TanStack Query does not require a dedicated Vite plugin. It uses the shared `@tanstack/devtools-vite` plugin (see SKILL.md shared config).

## 2. main.tsx Registration

```tsx
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

// Create QueryClient instance
const queryClient = new QueryClient();

// In render tree (wraps Router and DevTools):
<QueryClientProvider client={queryClient}>
  <TanStackDevtools plugins={[...]} />
  <RouterProvider router={router} />
</QueryClientProvider>
```

**Nesting order:** `QueryClientProvider` is the **outermost** TanStack provider, wrapping both `TanStackDevtools` and `RouterProvider`.

**QueryClient options** (optional, for custom defaults):

```tsx
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60 * 5, // 5 minutes
      retry: 1,
      refetchOnWindowFocus: false,
    },
  },
});
```

## 3. DevTools Panel

```tsx
import { ReactQueryDevtoolsPanel } from '@tanstack/react-query-devtools';

// As a plugin in TanStackDevtools:
{
  name: 'TanStack Query',
  render: <ReactQueryDevtoolsPanel />,
  defaultOpen: true,
}
```

**Note:** `defaultOpen: true` makes the Query panel the default active tab in DevTools.

## Compliance Checklist

- [ ] `QueryClient` instantiated at module level (not inside component)
- [ ] `QueryClientProvider` wraps the entire app (outermost TanStack provider)
- [ ] Query DevTools panel registered in `TanStackDevtools` plugins
