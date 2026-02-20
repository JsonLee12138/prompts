# Component Review Checklist (Condensed)

## Design
- Responsibilities are clear and narrow.
- Component type is appropriate (UI, business, container, page, layout).
- Props and dependencies are explicit.
- Data flow is clear and testable.

## Implementation
- File naming matches conventions.
- Props are fully typed (no `any`).
- Event handlers use `handleX` naming.
- Hooks dependencies are complete and correct.
- No inline styles; UnoCSS used.

## Quality
- No duplicated logic.
- Error and loading states handled.
- Performance optimizations applied where needed (`memo`, `useCallback`, `useMemo`).
- Code stays under reasonable size (~200 lines) or split.

## Pre-commit
- `pnpm lint` passes.
- `tsc --noEmit` passes.
- `pnpm build` passes.
