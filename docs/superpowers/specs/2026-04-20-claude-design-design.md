# Claude Design Skill Redesign

## Overview
Replace the current reference-only `skills/claude-design/` layout with a complete top-level skill that automatically routes natural-language design requests to the correct reference prompt. Preserve the seven existing reference prompts as-is except for their `CONNECTORS.md` link target. Move connector guidance into `skills/claude-design/references/CONNECTORS.md` and restrict design tool semantics in this skill to Figma and Pencil only.

## Goals
- Keep the seven existing reference prompts intact except for connector link paths.
- Add a top-level `skills/claude-design/SKILL.md` that acts as the single entry point and router.
- Allow automatic triggering from natural-language design requests without requiring users to invoke sub-skills manually.
- Support mixed routing: default to one best-matching reference, combine multiple references only for clearly multi-stage requests.
- Enforce tool-locking rules so explicit user tool choices never fall back automatically.
- When no design connection is available, require explicit user confirmation before switching to HTML-based design mode.

## Final Directory Structure
```text
skills/claude-design/
├── SKILL.md
└── references/
    ├── CONNECTORS.md
    ├── accessibility-review.md
    ├── design-critique.md
    ├── design-handoff.md
    ├── design-system.md
    ├── research-synthesis.md
    ├── user-research.md
    └── ux-copy.md
```

## Scope of Changes
### Files to add
- `skills/claude-design/SKILL.md`
- `skills/claude-design/references/CONNECTORS.md`

### Files to update
- `skills/claude-design/references/accessibility-review.md`
- `skills/claude-design/references/design-critique.md`
- `skills/claude-design/references/design-handoff.md`
- `skills/claude-design/references/design-system.md`
- `skills/claude-design/references/research-synthesis.md`
- `skills/claude-design/references/user-research.md`
- `skills/claude-design/references/ux-copy.md`

### Out of scope
- Rewriting the main body content of the seven reference prompts
- Changing their output templates, principles, or overall prompt structure
- Keeping or depending on the repository-level `skills/CONNECTORS.md` for this skill’s runtime behavior

## Top-Level Skill Responsibilities
The new `skills/claude-design/SKILL.md` should do four things:

1. Define trigger coverage for natural-language requests involving:
   - design review / critique
   - accessibility / a11y audit
   - design handoff
   - design system audit, documentation, or extension
   - UX copy
   - user research planning
   - research synthesis
   - Figma, Pencil, and HTML-based design workflows

2. Route requests to the right reference prompt(s) without duplicating the detailed content of those references.

3. Enforce tool-selection rules before any design execution starts.

4. Load one or more references only when needed, keeping the top-level skill concise.

## Routing Model
### Default behavior
Use a single best-matching reference by default.

### Combination behavior
Only combine references when the user request clearly spans multiple design stages.

### Route mapping
| User intent | Reference to load |
|---|---|
| Design review, critique, mockup feedback, screen review | `references/design-critique.md` |
| Accessibility, a11y, WCAG, contrast, keyboard review | `references/accessibility-review.md` |
| Developer handoff, implementation spec, tokens, states, responsive spec | `references/design-handoff.md` |
| Design system audit, documentation, extension | `references/design-system.md` |
| CTA, error copy, empty state, dialog wording, onboarding copy | `references/ux-copy.md` |
| User interviews, research plan, survey design, usability test planning | `references/user-research.md` |
| Research synthesis, transcript synthesis, support-feedback synthesis, NPS analysis | `references/research-synthesis.md` |

### Combination rules
Use fixed combinations only when clearly requested:
- Review + accessibility → `design-critique` + `accessibility-review`
- Review + handoff → `design-critique` + `design-handoff`
- Research synthesis + next-round planning → `research-synthesis` + `user-research`

### Combination order
When combining, use this order:
1. Evaluate or synthesize first
2. Apply focused secondary review next
3. Produce delivery artifact last

Examples:
- critique → accessibility → handoff
- synthesis → next research plan

### Ambiguity handling
If the request is too vague to route confidently, ask one minimal clarifying question before loading references.

## Tool Selection and Fallback Rules
### Explicit tool selection locks the tool
If the user explicitly chooses a tool, the skill must lock to that tool and never fall back automatically.

Examples:
- “Use Figma” → lock to Figma semantics
- “Use Pencil” → lock to Pencil semantics
- “Use HTML” → lock to HTML mode

### Figma and Pencil execution path
When the user specifies Figma or Pencil, actual design reading, handling, and orchestration should be performed through the Pencil MCP toolchain.

Interpretation:
- Figma can be the design source/context.
- Pencil MCP is the execution interface for design operations.

### No automatic fallback from explicit choices
Once a tool is locked:
- Figma does not fall back to HTML.
- Pencil does not fall back to HTML.
- HTML does not switch to Figma or Pencil.
- Explicit tool intent must be preserved through the whole response.

### No connection available
If no usable design connection is available:
- Do not silently fall back to Figma or Pencil.
- Ask the user for confirmation before using HTML mode.

Required confirmation pattern:
> There is no available design-tool connection right now. Do you want me to continue in HTML design mode?

Only proceed in HTML mode after the user confirms.

## Connector Model
The skill-specific connector file should live at:
- `skills/claude-design/references/CONNECTORS.md`

It should define connector semantics for this skill only.

### Required connector constraints
- `~~design tool` means only **Figma** or **Pencil** in this skill.
- Figma/Pencil requests are executed through Pencil MCP.
- If there is no design-tool connection, HTML mode requires explicit user confirmation.
- Explicit user tool selection disables fallback to another tool path.

## Reference File Updates
Each existing reference file should only change its connector help link.

### Required path change
Replace:
- `[CONNECTORS.md](../../CONNECTORS.md)`

With:
- `[CONNECTORS.md](./CONNECTORS.md)`

No other prompt-body changes should be made.

## Acceptance Criteria
The redesign is complete only if all of the following are true:
- `skills/claude-design/` becomes a complete skill with a top-level `SKILL.md`.
- Users can describe design tasks naturally without invoking separate sub-skills.
- The skill chooses one reference by default and combines references only for clearly multi-stage requests.
- Figma and Pencil requests are handled through Pencil MCP semantics.
- When no design connection exists, the skill asks for user confirmation before switching to HTML mode.
- Once the user explicitly chooses Figma, Pencil, or HTML, the skill does not fall back to another tool path.
- The seven reference prompts remain unchanged except for connector-link path updates.
- Connector guidance is localized to `skills/claude-design/references/CONNECTORS.md`.
