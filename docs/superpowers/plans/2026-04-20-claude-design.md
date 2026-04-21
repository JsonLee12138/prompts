# Claude Design Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Turn `skills/claude-design/` into a complete top-level skill that auto-routes natural-language design requests, keeps the seven reference prompts intact except for connector-link paths, and localizes connector behavior to Figma/Pencil with HTML confirmation fallback.

**Architecture:** Add a concise router-style `SKILL.md` at `skills/claude-design/`, add a skill-local `references/CONNECTORS.md`, and update the seven reference files to point at the local connector file. Validation is done with small file-content checks so the implementation can confirm routing rules, connector constraints, and path rewrites without touching the prompt bodies.

**Tech Stack:** Markdown skills, YAML frontmatter, Python 3 for file-content verification, git

---

### Task 1: Create the top-level claude-design router skill

**Files:**
- Create: `skills/claude-design/SKILL.md`
- Verify against: `docs/superpowers/specs/2026-04-20-claude-design-design.md`

- [ ] **Step 1: Write the failing verification for the missing top-level skill**

```python
from pathlib import Path

skill = Path("skills/claude-design/SKILL.md")
assert skill.exists(), "missing skills/claude-design/SKILL.md"
text = skill.read_text()
assert text.startswith("---\nname: claude-design\n"), "missing claude-design frontmatter"
assert "default to one best-matching reference" in text, "missing single-route rule"
assert "Only combine multiple references when the user request clearly spans multiple design stages." in text, "missing combination rule"
assert "There is no available design-tool connection right now. Do you want me to continue in HTML design mode?" in text, "missing HTML confirmation rule"
assert "When the user specifies Figma or Pencil, execute design operations through the Pencil MCP toolchain." in text, "missing Pencil MCP execution rule"
```

- [ ] **Step 2: Run the verification to confirm it fails**

Run:
```bash
python3 - <<'PY'
from pathlib import Path

skill = Path("/Users/jsonlee/Projects/prompts/skills/claude-design/SKILL.md")
assert skill.exists(), "missing skills/claude-design/SKILL.md"
text = skill.read_text()
assert text.startswith("---\nname: claude-design\n"), "missing claude-design frontmatter"
assert "default to one best-matching reference" in text, "missing single-route rule"
assert "Only combine multiple references when the user request clearly spans multiple design stages." in text, "missing combination rule"
assert "There is no available design-tool connection right now. Do you want me to continue in HTML design mode?" in text, "missing HTML confirmation rule"
assert "When the user specifies Figma or Pencil, execute design operations through the Pencil MCP toolchain." in text, "missing Pencil MCP execution rule"
PY
```
Expected: FAIL with `missing skills/claude-design/SKILL.md`

- [ ] **Step 3: Write the minimal top-level skill**

Create `skills/claude-design/SKILL.md` with exactly this content:

```markdown
---
name: claude-design
description: Unified design workflow router for critique, accessibility review, developer handoff, design system work, UX copy, user research, and research synthesis. Use when users ask naturally for design feedback, mockup review, a11y audit, handoff specs, UX writing, research planning, research synthesis, or mention Figma, Pencil, or HTML design workflows and should not need to invoke separate sub-skills manually.
---

# Claude Design

Use this skill as the single entry point for design-related requests.
Route the request to the most relevant reference prompt instead of asking the user to invoke separate design skills.
Keep the reference prompts as the source of detailed guidance; this file only decides which reference(s) to load and which tool path to lock.

## Tool selection rules

1. If the user explicitly chooses a tool, lock to that tool and do not fall back automatically.
2. If the user specifies Figma or Pencil, execute design operations through the Pencil MCP toolchain.
3. Treat Figma as a design source/context and Pencil MCP as the execution interface.
4. If the user explicitly chooses HTML, stay in HTML mode and do not switch back to a design-tool flow.
5. If no design-tool connection is available, ask the user before using HTML mode.

Use this exact confirmation when there is no available design-tool connection:

> There is no available design-tool connection right now. Do you want me to continue in HTML design mode?

Read `references/CONNECTORS.md` whenever you need to interpret `~~design tool` semantics for this skill.

## Routing rules

Default to one best-matching reference.
Only combine multiple references when the user request clearly spans multiple design stages.
If the request is ambiguous, ask one minimal clarifying question before loading references.
Do not expand scope implicitly.

### Route mapping

- Design review, critique, screen feedback, mockup feedback → `references/design-critique.md`
- Accessibility, a11y, WCAG, contrast, keyboard review → `references/accessibility-review.md`
- Developer handoff, implementation specs, tokens, responsive states → `references/design-handoff.md`
- Design system audit, documentation, or extension → `references/design-system.md`
- CTA copy, error messages, empty states, dialog wording, onboarding copy → `references/ux-copy.md`
- User interviews, research plans, survey design, usability-test planning → `references/user-research.md`
- Research synthesis, transcript synthesis, support-feedback synthesis, NPS analysis → `references/research-synthesis.md`

### Combination rules

Use these combinations only when the request clearly asks for multiple stages:
- Review + accessibility → `references/design-critique.md` + `references/accessibility-review.md`
- Review + handoff → `references/design-critique.md` + `references/design-handoff.md`
- Research synthesis + next-round planning → `references/research-synthesis.md` + `references/user-research.md`

When combining, keep this order:
1. Evaluate or synthesize first
2. Apply focused secondary review next
3. Produce the delivery artifact last
```

- [ ] **Step 4: Run the verification to confirm it passes**

Run:
```bash
python3 - <<'PY'
from pathlib import Path

skill = Path("/Users/jsonlee/Projects/prompts/skills/claude-design/SKILL.md")
assert skill.exists(), "missing skills/claude-design/SKILL.md"
text = skill.read_text()
assert text.startswith("---\nname: claude-design\n"), "missing claude-design frontmatter"
assert "Default to one best-matching reference." in text, "missing single-route rule"
assert "Only combine multiple references when the user request clearly spans multiple design stages." in text, "missing combination rule"
assert "There is no available design-tool connection right now. Do you want me to continue in HTML design mode?" in text, "missing HTML confirmation rule"
assert "If the user specifies Figma or Pencil, execute design operations through the Pencil MCP toolchain." in text, "missing Pencil MCP execution rule"
PY
```
Expected: PASS with no output

- [ ] **Step 5: Commit**

```bash
git -C "/Users/jsonlee/Projects/prompts" add "skills/claude-design/SKILL.md"
git -C "/Users/jsonlee/Projects/prompts" commit -m "$(cat <<'EOF'
feat(claude-design): add top-level routing skill
EOF
)"
```

### Task 2: Add the skill-local connectors reference

**Files:**
- Create: `skills/claude-design/references/CONNECTORS.md`
- Verify against: `docs/superpowers/specs/2026-04-20-claude-design-design.md`

- [ ] **Step 1: Write the failing verification for the local connector reference**

```python
from pathlib import Path

connectors = Path("skills/claude-design/references/CONNECTORS.md")
assert connectors.exists(), "missing local connectors reference"
text = connectors.read_text()
assert "`~~design tool` means only **Figma** or **Pencil** in this skill." in text, "missing design-tool restriction"
assert "Figma/Pencil requests are executed through Pencil MCP." in text, "missing Pencil MCP rule"
assert "HTML mode requires explicit user confirmation." in text, "missing HTML confirmation rule"
assert "Explicit user tool selection disables fallback to another tool path." in text, "missing no-fallback rule"
```

- [ ] **Step 2: Run the verification to confirm it fails**

Run:
```bash
python3 - <<'PY'
from pathlib import Path

connectors = Path("/Users/jsonlee/Projects/prompts/skills/claude-design/references/CONNECTORS.md")
assert connectors.exists(), "missing local connectors reference"
text = connectors.read_text()
assert "`~~design tool` means only **Figma** or **Pencil** in this skill." in text, "missing design-tool restriction"
assert "Figma/Pencil requests are executed through Pencil MCP." in text, "missing Pencil MCP rule"
assert "HTML mode requires explicit user confirmation." in text, "missing HTML confirmation rule"
assert "Explicit user tool selection disables fallback to another tool path." in text, "missing no-fallback rule"
PY
```
Expected: FAIL with `missing local connectors reference`

- [ ] **Step 3: Write the minimal local connector reference**

Create `skills/claude-design/references/CONNECTORS.md` with exactly this content:

```markdown
# Connectors

## How tool references work in this skill

Plugin files use `~~design tool` as a placeholder for the design connector available to this skill.
In `claude-design`, `~~design tool` means only **Figma** or **Pencil**.

## Connector behavior for claude-design

- `~~design tool` means only **Figma** or **Pencil** in this skill.
- Figma/Pencil requests are executed through Pencil MCP.
- If there is no design-tool connection, HTML mode requires explicit user confirmation.
- Explicit user tool selection disables fallback to another tool path.

## Execution notes

- If the user explicitly chooses Figma, preserve that choice and use Pencil MCP as the execution interface.
- If the user explicitly chooses Pencil, preserve that choice and use Pencil MCP as the execution interface.
- If the user explicitly chooses HTML, stay in HTML mode.
- If no design-tool connection exists, ask before proceeding in HTML mode.
```

- [ ] **Step 4: Run the verification to confirm it passes**

Run:
```bash
python3 - <<'PY'
from pathlib import Path

connectors = Path("/Users/jsonlee/Projects/prompts/skills/claude-design/references/CONNECTORS.md")
assert connectors.exists(), "missing local connectors reference"
text = connectors.read_text()
assert "`~~design tool` means only **Figma** or **Pencil** in this skill." in text, "missing design-tool restriction"
assert "Figma/Pencil requests are executed through Pencil MCP." in text, "missing Pencil MCP rule"
assert "HTML mode requires explicit user confirmation." in text, "missing HTML confirmation rule"
assert "Explicit user tool selection disables fallback to another tool path." in text, "missing no-fallback rule"
PY
```
Expected: PASS with no output

- [ ] **Step 5: Commit**

```bash
git -C "/Users/jsonlee/Projects/prompts" add "skills/claude-design/references/CONNECTORS.md"
git -C "/Users/jsonlee/Projects/prompts" commit -m "$(cat <<'EOF'
feat(claude-design): add skill-local connectors reference
EOF
)"
```

### Task 3: Repoint all design references to the local connector file

**Files:**
- Modify: `skills/claude-design/references/accessibility-review.md:9`
- Modify: `skills/claude-design/references/design-critique.md:9`
- Modify: `skills/claude-design/references/design-handoff.md:9`
- Modify: `skills/claude-design/references/design-system.md:9`
- Modify: `skills/claude-design/references/research-synthesis.md:9`
- Modify: `skills/claude-design/references/user-research.md` (connector note if present; do not change any other body content)
- Modify: `skills/claude-design/references/ux-copy.md:9`

- [ ] **Step 1: Write the failing verification for connector link targets**

```python
from pathlib import Path

files = [
    Path("skills/claude-design/references/accessibility-review.md"),
    Path("skills/claude-design/references/design-critique.md"),
    Path("skills/claude-design/references/design-handoff.md"),
    Path("skills/claude-design/references/design-system.md"),
    Path("skills/claude-design/references/research-synthesis.md"),
    Path("skills/claude-design/references/ux-copy.md"),
]

for path in files:
    text = path.read_text()
    assert "[CONNECTORS.md](./CONNECTORS.md)" in text, f"{path} still points to the old connector path"
    assert "[CONNECTORS.md](../../CONNECTORS.md)" not in text, f"{path} still contains the old connector path"
```

- [ ] **Step 2: Run the verification to confirm it fails**

Run:
```bash
python3 - <<'PY'
from pathlib import Path

files = [
    Path("/Users/jsonlee/Projects/prompts/skills/claude-design/references/accessibility-review.md"),
    Path("/Users/jsonlee/Projects/prompts/skills/claude-design/references/design-critique.md"),
    Path("/Users/jsonlee/Projects/prompts/skills/claude-design/references/design-handoff.md"),
    Path("/Users/jsonlee/Projects/prompts/skills/claude-design/references/design-system.md"),
    Path("/Users/jsonlee/Projects/prompts/skills/claude-design/references/research-synthesis.md"),
    Path("/Users/jsonlee/Projects/prompts/skills/claude-design/references/ux-copy.md"),
]

for path in files:
    text = path.read_text()
    assert "[CONNECTORS.md](./CONNECTORS.md)" in text, f"{path} still points to the old connector path"
    assert "[CONNECTORS.md](../../CONNECTORS.md)" not in text, f"{path} still contains the old connector path"
PY
```
Expected: FAIL on the first file with `still points to the old connector path`

- [ ] **Step 3: Update the connector help links only**

Apply this exact replacement in each file that currently contains the shared connector note:

```markdown
> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](../../CONNECTORS.md).
```

Replace it with:

```markdown
> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](./CONNECTORS.md).
```

Update these files and do not change any other lines:
- `skills/claude-design/references/accessibility-review.md`
- `skills/claude-design/references/design-critique.md`
- `skills/claude-design/references/design-handoff.md`
- `skills/claude-design/references/design-system.md`
- `skills/claude-design/references/research-synthesis.md`
- `skills/claude-design/references/ux-copy.md`

Leave `skills/claude-design/references/user-research.md` untouched unless a connector note is added later; this plan does not rewrite its body.

- [ ] **Step 4: Run the verification to confirm it passes**

Run:
```bash
python3 - <<'PY'
from pathlib import Path

files = [
    Path("/Users/jsonlee/Projects/prompts/skills/claude-design/references/accessibility-review.md"),
    Path("/Users/jsonlee/Projects/prompts/skills/claude-design/references/design-critique.md"),
    Path("/Users/jsonlee/Projects/prompts/skills/claude-design/references/design-handoff.md"),
    Path("/Users/jsonlee/Projects/prompts/skills/claude-design/references/design-system.md"),
    Path("/Users/jsonlee/Projects/prompts/skills/claude-design/references/research-synthesis.md"),
    Path("/Users/jsonlee/Projects/prompts/skills/claude-design/references/ux-copy.md"),
]

for path in files:
    text = path.read_text()
    assert "[CONNECTORS.md](./CONNECTORS.md)" in text, f"{path} still points to the old connector path"
    assert "[CONNECTORS.md](../../CONNECTORS.md)" not in text, f"{path} still contains the old connector path"
PY
```
Expected: PASS with no output

- [ ] **Step 5: Commit**

```bash
git -C "/Users/jsonlee/Projects/prompts" add \
  "skills/claude-design/references/accessibility-review.md" \
  "skills/claude-design/references/design-critique.md" \
  "skills/claude-design/references/design-handoff.md" \
  "skills/claude-design/references/design-system.md" \
  "skills/claude-design/references/research-synthesis.md" \
  "skills/claude-design/references/ux-copy.md"
git -C "/Users/jsonlee/Projects/prompts" commit -m "$(cat <<'EOF'
chore(claude-design): localize connector links
EOF
)"
```

### Task 4: Run end-to-end content checks for the redesigned skill

**Files:**
- Verify: `skills/claude-design/SKILL.md`
- Verify: `skills/claude-design/references/CONNECTORS.md`
- Verify: `skills/claude-design/references/*.md`

- [ ] **Step 1: Write the failing end-to-end verification**

```python
from pathlib import Path

skill = Path("skills/claude-design/SKILL.md")
connectors = Path("skills/claude-design/references/CONNECTORS.md")
reference_dir = Path("skills/claude-design/references")

assert skill.exists(), "top-level skill missing"
assert connectors.exists(), "local connectors missing"

skill_text = skill.read_text()
connectors_text = connectors.read_text()

assert "Read `references/CONNECTORS.md` whenever you need to interpret `~~design tool` semantics for this skill." in skill_text, "skill missing connector handoff"
assert "If no design-tool connection is available, ask the user before using HTML mode." in skill_text, "skill missing HTML gating"
assert "Figma/Pencil requests are executed through Pencil MCP." in connectors_text, "connectors missing Pencil MCP rule"

for ref in [
    reference_dir / "accessibility-review.md",
    reference_dir / "design-critique.md",
    reference_dir / "design-handoff.md",
    reference_dir / "design-system.md",
    reference_dir / "research-synthesis.md",
    reference_dir / "ux-copy.md",
]:
    text = ref.read_text()
    assert "[CONNECTORS.md](./CONNECTORS.md)" in text, f"{ref.name} missing local connector link"
```

- [ ] **Step 2: Run the verification to confirm it passes once Tasks 1-3 are done**

Run:
```bash
python3 - <<'PY'
from pathlib import Path

skill = Path("/Users/jsonlee/Projects/prompts/skills/claude-design/SKILL.md")
connectors = Path("/Users/jsonlee/Projects/prompts/skills/claude-design/references/CONNECTORS.md")
reference_dir = Path("/Users/jsonlee/Projects/prompts/skills/claude-design/references")

assert skill.exists(), "top-level skill missing"
assert connectors.exists(), "local connectors missing"

skill_text = skill.read_text()
connectors_text = connectors.read_text()

assert "Read `references/CONNECTORS.md` whenever you need to interpret `~~design tool` semantics for this skill." in skill_text, "skill missing connector handoff"
assert "If no design-tool connection is available, ask the user before using HTML mode." in skill_text, "skill missing HTML gating"
assert "Figma/Pencil requests are executed through Pencil MCP." in connectors_text, "connectors missing Pencil MCP rule"

for ref in [
    reference_dir / "accessibility-review.md",
    reference_dir / "design-critique.md",
    reference_dir / "design-handoff.md",
    reference_dir / "design-system.md",
    reference_dir / "research-synthesis.md",
    reference_dir / "ux-copy.md",
]:
    text = ref.read_text()
    assert "[CONNECTORS.md](./CONNECTORS.md)" in text, f"{ref.name} missing local connector link"
PY
```
Expected: PASS with no output

- [ ] **Step 3: Review `git diff` to confirm the reference bodies were not rewritten**

Run:
```bash
git -C "/Users/jsonlee/Projects/prompts" diff -- \
  "skills/claude-design/SKILL.md" \
  "skills/claude-design/references/CONNECTORS.md" \
  "skills/claude-design/references/accessibility-review.md" \
  "skills/claude-design/references/design-critique.md" \
  "skills/claude-design/references/design-handoff.md" \
  "skills/claude-design/references/design-system.md" \
  "skills/claude-design/references/research-synthesis.md" \
  "skills/claude-design/references/ux-copy.md"
```
Expected: diff shows one new top-level skill, one new local connectors file, and connector-link-only edits in the existing reference prompts

- [ ] **Step 4: Commit**

```bash
git -C "/Users/jsonlee/Projects/prompts" add \
  "skills/claude-design/SKILL.md" \
  "skills/claude-design/references/CONNECTORS.md" \
  "skills/claude-design/references/accessibility-review.md" \
  "skills/claude-design/references/design-critique.md" \
  "skills/claude-design/references/design-handoff.md" \
  "skills/claude-design/references/design-system.md" \
  "skills/claude-design/references/research-synthesis.md" \
  "skills/claude-design/references/ux-copy.md"
git -C "/Users/jsonlee/Projects/prompts" commit -m "$(cat <<'EOF'
feat(claude-design): add routed design skill entrypoint
EOF
)"
```
