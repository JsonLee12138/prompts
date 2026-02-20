# Workspace (Monorepo) Setup

## 1. Create shared config package
```
packages/eslint-config/
  package.json
  src/index.ts
  eslint.config.js
  tsdown.config.ts
```

## 2. package.json (shared config)
```json
{
  "name": "@your-scope/eslint-config",
  "version": "1.0.0",
  "type": "module",
  "main": "./dist/cjs/index.cjs",
  "module": "./dist/es/index.mjs",
  "exports": {
    ".": "./dist/cjs/index.cjs",
    "./es": "./dist/es/index.mjs",
    "./cjs": "./dist/cjs/index.cjs"
  },
  "scripts": {
    "build": "tsdown",
    "dev": "tsdown --watch"
  },
  "dependencies": {
    "@antfu/eslint-config": "^6.0.0",
    "eslint-plugin-format": "^1.0.2"
  },
  "devDependencies": {
    "eslint": "^9.37.0",
    "tsdown": "^0.15.9"
  }
}
```

## 3. src/index.ts
```typescript
import antfu from '@antfu/eslint-config'

type Options = Parameters<typeof antfu>[0]

export default (options: Options = {}) => {
  const stylisticConfig = {
    indent: 2,
    quotes: 'single',
    endOfLine: 'lf',
    trailingComma: 'all',
    semi: false,
  } as any

  if (typeof options.stylistic === 'object') {
    Object.assign(stylisticConfig, options.stylistic)
    delete options.stylistic
  }

  return antfu({
    formatters: true,
    stylistic: stylisticConfig,
    typescript: true,
    react: true,
    ...options,
  })
}
```

## 4. eslint.config.js (package)
```javascript
import config from './src/index.js'
export default config
```

## 5. Build
```bash
pnpm install
pnpm build
```

## 6. Use in an app
```javascript
// apps/my-app/eslint.config.js
import config from '@your-scope/eslint-config'

export default config({
  typescript: true,
  react: true,
})
```

## Optional: Commit Quality Guardrails (repo root)
For monorepos, keep commit hooks and staged-file linting at repository root:
- `.commitlintrc.cjs`
- `.husky/commit-msg`
- `.husky/pre-commit`
- `.lintstagedrc`

Reference:
- `references/commit-quality.md`
