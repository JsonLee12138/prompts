# Component Standards (React/TypeScript)

## Naming
- **Component files**: PascalCase (e.g., `UserCard.tsx`).
- **Page files**: camelCase (e.g., `userSettings.tsx`).
- **Hooks**: camelCase with `use` prefix (e.g., `useModal.ts`).
- **Props interface**: `ComponentNameProps`.
- **Handlers**: `handleX` (e.g., `handleClick`).
- **State**: camelCase (e.g., `isOpen`, `userData`).
- **Constants**: UPPER_SNAKE_CASE.

## Component Types & Responsibilities
- **UI components**: presentation only (Button, Card).
- **Business components**: UI + local business logic (UserProfile).
- **Container components**: data fetching/state orchestration.
- **Page components**: route-level composition.
- **Layout components**: page structure only.

## Structure
- Use function components with typed props.
- Prefer named exports.
- Set `displayName` for memoized components.
- Keep components focused (SRP, SoC).

## Hooks
- Avoid hooks in loops/conditions.
- Use `useCallback` for event handlers.
- Use `useMemo` for expensive computations.
- Keep dependency arrays accurate.

## Styling (UnoCSS)
- Use UnoCSS utility classes and shortcuts.
- Prefer CSS variables for theming.
- Avoid inline styles unless necessary.
- Support dark mode where applicable.

## Quality & Architecture Principles
- Keep responsibilities narrow (SRP).
- Separate UI, logic, and data (SoC).
- Avoid duplication (DRY).
- Keep it simple (KISS).
- Prefer composition over inheritance.
