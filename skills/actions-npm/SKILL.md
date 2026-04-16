---
name: actions-npm
description: "GitHub Actions workflow for npm package publishing with OIDC provenance (no NPM_TOKEN). Use when creating CI/CD workflows that publish npm packages, setting up tag-triggered releases, or configuring npm publish with provenance attestation. Triggers on release workflow, npm publish, provenance, actions-npm, .github/workflows."
---

# Actions NPM Publish (OIDC Provenance)

## Workflow Template

See [assets/release-npm.yml](assets/release-npm.yml) — 可直接复制到 `.github/workflows/` 使用。

## How It Works

npm v11+ 在 `NODE_AUTH_TOKEN` 为空时自动使用 GitHub OIDC 认证：

1. `id-token: write` 权限让 GitHub Actions 提供 OIDC token
2. npm v11+ 检测到空 token，向 GitHub 请求 OIDC token
3. npm 用 OIDC token 向 registry 换取发布凭证
4. provenance 证明被签名并发布到透明日志

**不需要 NPM_TOKEN secret。**

## Key Points

- `NODE_AUTH_TOKEN: ""` 必须显式设置（覆盖 setup-node 可能注入的值）
- `package.json` 必须有 `repository` 字段，URL 必须匹配 `github.com/<owner>/<repo>`
- Node 22 自带 npm v10，必须升级到 v11+（模板中的 Upgrade step 处理了 runner 上 npm 损坏的 fallback）
