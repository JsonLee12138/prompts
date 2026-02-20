---
name: eslint-config
description: Use when configuring ESLint with @antfu/eslint-config for a single project or a monorepo workspace, including flat config setup, shared config packages, or migrations from legacy ESLint configs.
---

# ESLint Config

## Overview
Set up ESLint using `@antfu/eslint-config` for either a single project or a workspace package.

## Decision
- **Single project**: Choose when you have one app/package.
- **Workspace package**: Choose when multiple apps need a shared ESLint config in a monorepo.

## Quick Workflow
1. Choose single vs workspace.
2. Install dependencies.
3. Create `eslint.config.js` (flat config).
4. Add `lint` scripts.
5. Run `pnpm lint` to verify.

## Common Mistakes
- Mixing Prettier with ESLint formatting rules (prefer ESLint-only).
- Using legacy `.eslintrc` instead of `eslint.config.js`.
- Forgetting to build/publish the shared workspace config.

## Resources
- `references/single-project.md`
- `references/workspace.md`
- `references/vscode-settings.md`
