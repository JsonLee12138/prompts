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
Default to a single reference. Combine multiple references when the user request clearly spans multiple design stages.

Examples:
- Review + accessibility → `references/design-critique.md` + `references/accessibility-review.md`
- Review + handoff → `references/design-critique.md` + `references/design-handoff.md`
- Research synthesis + next-round planning → `references/research-synthesis.md` + `references/user-research.md`

Other multi-stage pairings follow the same pattern when the request warrants it.

When combining, keep this order:
1. Evaluate or synthesize first
2. Apply focused secondary review next
3. Produce the delivery artifact last
