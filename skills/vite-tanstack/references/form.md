# TanStack Form — Vite Configuration

## 1. Vite Plugin

TanStack Form does not require a dedicated Vite plugin. It uses the shared `@tanstack/devtools-vite` plugin (see SKILL.md shared config).

## 2. main.tsx Registration

TanStack Form does not require a global provider. Forms are created per-component using `useForm` hook. No registration in `main.tsx` is needed.

## 3. DevTools Panel

```tsx
import { FormDevtoolsPanel } from '@tanstack/react-form-devtools';

// As a plugin in TanStackDevtools:
{
  name: 'Tanstack Form',
  render: <FormDevtoolsPanel />,
}
```

## Compliance Checklist

- [ ] Form DevTools panel registered in `TanStackDevtools` plugins
