# unocss-shadcn Skill Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build a new `unocss-shadcn` skill that guides semi-automatic UnoCSS + shadcn preset setup with strict monorepo detection and mandatory shadcn MCP/manual workflow.

**Architecture:** Keep `SKILL.md` concise and route branch-specific behavior into `references/` files. Implement deterministic decision logic for monorepo vs single-project and enforce shadcn component operations through MCP only. Use no scripts for v1 to reduce complexity and rely on explicit command templates.

**Tech Stack:** Markdown skill package, Python init utility (`init_skill.py`), git

---

### Task 1: Initialize skill scaffold

**Files:**
- Create: `skills/unocss-shadcn/SKILL.md`
- Create: `skills/unocss-shadcn/references/`

**Step 1: Verify target directory does not exist**

Run: `test -d skills/unocss-shadcn && echo "exists" || echo "missing"`
Expected: `missing`

**Step 2: Create scaffold with init tool**

Run: `python3 /Users/jsonlee/.codex/skills/.system/skill-creator/scripts/init_skill.py unocss-shadcn --path /Users/jsonlee/Projects/prompts/skills --resources references`
Expected: new `skills/unocss-shadcn/` with template `SKILL.md` and `references/`

**Step 3: Verify scaffold exists**

Run: `ls -la skills/unocss-shadcn`
Expected: includes `SKILL.md` and `references/`

**Step 4: Commit scaffold**

```bash
git add skills/unocss-shadcn
git commit -m "feat: initialize unocss-shadcn skill scaffold"
```

### Task 2: Author core SKILL.md

**Files:**
- Modify: `skills/unocss-shadcn/SKILL.md`

**Step 1: Write frontmatter with trigger-rich description**

Include exact fields:
```yaml
---
name: unocss-shadcn
description: Configure UnoCSS with unocss-preset-shadcn and enforce shadcn MCP/manual component workflow. Use when setting up UnoCSS + shadcn integration, deciding monorepo vs single-project target paths, or generating non-automatic config/command changes.
---
```

**Step 2: Write concise workflow sections**

Include:
- strict monorepo detection rule
- semi-automatic mode rule (no auto install)
- path policy
- mandatory MCP chain
- manual mode constraint for component creation
- blocked behavior when MCP unavailable
- links to `references/*.md`

**Step 3: Validate markdown structure**

Run: `sed -n '1,220p' skills/unocss-shadcn/SKILL.md`
Expected: no TODO placeholders and no extra frontmatter fields

**Step 4: Commit SKILL.md**

```bash
git add skills/unocss-shadcn/SKILL.md
git commit -m "feat: define unocss-shadcn core workflow"
```

### Task 3: Add branch-specific references

**Files:**
- Create: `skills/unocss-shadcn/references/monorepo.md`
- Create: `skills/unocss-shadcn/references/single-project.md`
- Create: `skills/unocss-shadcn/references/checklist.md`

**Step 1: Write `monorepo.md`**

Must include:
- detection evidence examples
- `packages/shadcn-ui` destination
- `peerDependencies` policy
- UnoCSS preset patch template
- MCP-first component flow

**Step 2: Write `single-project.md`**

Must include:
- fallback detection result
- `src/components` destination
- dependency policy (`dependencies`)
- UnoCSS preset patch template
- MCP-first component flow

**Step 3: Write `checklist.md`**

Must include:
- preflight checks
- post-change validation checks
- failure/remediation matrix

**Step 4: Verify reference files**

Run: `rg -n "MCP|manual|peerDependencies|src/components|packages/shadcn-ui" skills/unocss-shadcn/references`
Expected: all required terms are present

**Step 5: Commit references**

```bash
git add skills/unocss-shadcn/references
git commit -m "feat: add unocss-shadcn branch references"
```

### Task 4: Validate package quality

**Files:**
- Modify if needed: `skills/unocss-shadcn/SKILL.md`
- Modify if needed: `skills/unocss-shadcn/references/*.md`

**Step 1: Run quick validation pass**

Run: `python3 /Users/jsonlee/.codex/skills/.system/skill-creator/scripts/quick_validate.py /Users/jsonlee/Projects/prompts/skills/unocss-shadcn`
Expected: no critical validation errors

**Step 2: Manual content review**

Run: `rg -n "Tailwind|init" skills/unocss-shadcn`
Expected: mentions are only constraints/warnings, not default recommended flow

**Step 3: Final commit**

```bash
git add skills/unocss-shadcn
git commit -m "feat: complete unocss-shadcn skill v1"
```
