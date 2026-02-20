# Single Project Setup (Flat Config)

## Install
```bash
pnpm add -D eslint @antfu/eslint-config
```

## eslint.config.js
```javascript
import antfu from '@antfu/eslint-config'

export default antfu({
  typescript: true,
  react: true,
  formatters: true,
  stylistic: {
    indent: 2,
    quotes: 'single',
    semi: false,
  },
  rules: {
    'no-console': 'warn',
    '@typescript-eslint/no-explicit-any': 'off',
  },
  ignores: ['dist/', 'build/', 'node_modules/', 'coverage/'],
})
```

## package.json scripts
```json
{
  "scripts": {
    "lint": "eslint .",
    "lint:fix": "eslint . --fix"
  }
}
```

## Verify
```bash
pnpm lint
```
