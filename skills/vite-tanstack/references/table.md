# TanStack Table — Vite Configuration

## 1. Vite Plugin

TanStack Table does not require a dedicated Vite plugin. It is a headless UI library with no build-time configuration.

## 2. main.tsx Registration

TanStack Table does not require a global provider or any main.tsx registration. Tables are created per-component using `useReactTable` hook.

```tsx
import { useReactTable, getCoreRowModel } from '@tanstack/react-table';

// Usage is entirely per-component, no global setup needed
```

## 3. DevTools

TanStack Table does not currently have an official DevTools panel. Table state can be inspected through React DevTools or by logging `table.getState()`.

## Compliance Checklist

- [ ] `@tanstack/react-table` added to dependencies
- [ ] No unnecessary global providers added for table
