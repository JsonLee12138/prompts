---
name: @frontend/components
description: Provides component design guidance, code review, and best practices for frontend development while following both @frontend/ and @architecture/ standards
---

# @frontend/components

This skill should be used when developing React/TypeScript components. It provides component design guidance, code review, and best practices while following both frontend standards and architecture principles.

## Core Capabilities

This skill provides:

1. **Component Design Guidance** - Provides component architecture设计方案
2. **Code Review** - Checks components against both frontend and architecture standards
3. **Best Practices** - Provides component development best practices
4. **Problem Diagnosis** - Identifies component design issues and provides improvement solutions
5. **Template Generation** - Generates compliant component templates

## When to Use This Skill

Use this skill when:

- Creating new frontend components
- Reviewing component code quality
- Designing component architecture
- Diagnosing component issues
- Seeking component development best practices
- Need to follow both @frontend/ and @architecture/ standards

## How to Use This Skill

### Example 1: Create a New Component

To create a Button component with multiple variants and sizes:

```
@frontend/components Create a Button component

Requirements:
- Support multiple variants (primary, secondary, danger)
- Support different sizes (sm, md, lg)
- Support loading state
- Support disabled state
- Use TypeScript
- Use UnoCSS styles
```

This skill will provide:
- Component file structure
- TypeScript type definitions
- Props interface design
- Component implementation code
- Style configuration
- Usage examples

### Example 2: Code Review

To review a component for compliance:

```
@frontend/components Review this component:

```typescript
[Your component code]
```

Please check:
- Naming conventions
- TypeScript types completeness
- 10 design principles compliance
- UnoCSS usage
- Performance optimization suggestions
```

This skill will provide:
- Issue list (by severity)
- Specific modification suggestions
- Improved code examples
- Architecture principle applications

### Example 3: Architecture Design Guidance

To design a user list component:

```
@frontend/components Help me design a user list component

Requirements:
- Display user list
- Support search
- Support pagination
- Support delete operation
- Need loading and error handling
```

This skill will provide:
- Component hierarchy design
- Responsibility division
- Data flow design
- Component communication方案
- Code examples

### Example 4: Problem Diagnosis

To diagnose component issues:

```
@frontend/components What are the problems with this component?

```typescript
[Problematic component code]
```

Please analyze:
- Which design principles are violated
- How to improve
- Performance issues
- Testability issues
```

This skill will provide:
- Problem analysis
- Violated principles list
- Improvement solutions
- Refactoring suggestions

### Example 5: Best Practice Consultation

To optimize component performance:

```
@frontend/components How to optimize this component's performance?

```typescript
[Component code]
```

Please provide:
- Performance optimization suggestions
- Code improvement方案
- Best practice examples
```

This skill will provide:
- Performance analysis
- Optimization solutions
- Code examples
- Best practices

## Key Workflows

### Workflow 1: Component Development

1. **Design Phase** - Call `@architecture-assistant` for component design
2. **Get Standards** - Call this skill for frontend规范
3. **Implementation** - Use templates from `TEMPLATES.md`
4. **Code Review** - Call both `@architecture-assistant` and this skill
5. **Testing** - Run type checks and builds
6. **Documentation** - Create ADR if needed

### Workflow 2: Code Review

1. **Self-Check** - Use `CHECKLIST.md` for self-review
2. **Architecture Review** - Call `@architecture-assistant`
3. **Frontend Review** - Call this skill
4. **Fix Issues** - Address problems found
5. **Re-Review** - Verify fixes

### Workflow 3: Problem Diagnosis

1. **Identify Issues** - Analyze component problems
2. **Call Skill** - Use this skill for diagnosis
3. **Analyze Results** - Review skill output
4. **Implement Fixes** - Apply recommended solutions
5. **Verify** - Check that issues are resolved

## Bundled Resources

This skill provides the following bundled resources:

### References

- `CHECKLIST.md` - Component development checklist
- `RULES.md` - Complete component development rules
- `TEMPLATES.md` - Component code templates
- `README.md` - Documentation and usage guide

### How to Access References

To access reference documentation:

```bash
# View component rules
cat frontend/skills/components/RULES.md

# View checklist
cat frontend/skills/components/CHECKLIST.md

# View templates
cat frontend/skills/components/TEMPLATES.md

# View documentation
cat frontend/skills/components/README.md
```

## Quality Standards

### Excellent Components

- Follow 9-10 core principles
- Pass both architecture and frontend reviews
- Have clear ADR (if needed)
- Easy to test and maintain
- Clean and readable code

###合格 Components

- Follow 7-8 core principles
- No serious anti-patterns
- Basic testability
- Pass basic review

###不合格 Components

- Violate 3+ core principles
- Have God Objects
- Serious coupling or circular dependencies
- Not reviewed by skills

## Common Issues and Solutions

### Issue 1: Violating Single Responsibility Principle

**Symptoms**:
- Component exceeds 200 lines
- More than 5 props
- Mixed UI, data, and business logic

**Solution**: Split into multiple components

### Issue 2: Violating Separation of Concerns

**Symptoms**:
- UI and logic mixed together
- Data fetching inside component
- Complex state management

**Solution**: Separate into UI and container components

### Issue 3: Missing Type Safety

**Symptoms**:
- Using `any` type
- Incomplete Props types
- Missing type annotations

**Solution**: Add complete TypeScript types

### Issue 4: Style System Chaos

**Symptoms**:
- Using inline styles
- Mixed style solutions
- Not using CSS variables

**Solution**: Use UnoCSS and CSS variables consistently

### Issue 5: Performance Issues

**Symptoms**:
- Unnecessary re-renders
- Missing memo/useCallback
- Incorrect dependency arrays

**Solution**: Add performance optimizations

## Learning Path

### For Beginners (1-3 months)

1. **Week 1** - Read `RULES.md` naming section
2. **Weeks 2-4** - Create basic components using `TEMPLATES.md`
3. **Months 1-3** - Apply architecture principles

### For Intermediate Developers (3-12 months)

1. **Architecture Design** - Learn component patterns
2. **Performance Optimization** - Master performance techniques
3. **Team Collaboration** - Share knowledge and review code

### For Advanced Developers (1+ years)

1. **Architecture Decisions** - Design large component systems
2. **Team Building** - Train team members
3. **Process Improvement** - Enhance team standards

## Best Practices

### 1. Component Development

- Use imperative language in instructions
- Follow naming conventions strictly
- Apply 10 design principles
- Use TypeScript strictly
- Optimize performance with memo/useCallback

### 2. Code Review

- Check both frontend and architecture standards
- Use checklists for systematic review
- Provide specific, actionable feedback
- Include code examples for improvements

### 3. Documentation

- Keep SKILL.md lean and focused
- Move detailed examples to references
- Use progressive disclosure
- Update based on real usage

## Tips for Effective Use

### When to Call This Skill

- ✅ Creating new components
- ✅ Reviewing component code
- ✅ Designing component architecture
- ✅ Diagnosing component issues
- ✅ Seeking best practices

### When NOT to Call This Skill

- ❌ Simple file operations
- ❌ Single-line fixes
- ❌ Trivial questions answerable from code

### Getting the Best Results

1. **Be Specific** - Provide clear requirements
2. **Include Context** - Share relevant code
3. **Ask Follow-ups** - Clarify as needed
4. **Provide Feedback** - Help improve the skill

## Integration with Other Skills

This skill works well with:

- **@architecture-assistant** - For architecture design and review
- **@frontend-standard** - For general frontend standards
- **@frontend/ui-ux-engineer** - For visual/UI components

## Common Commands

```bash
# Create a component
@frontend/components Create a [ComponentName] component

# Review code
@frontend/components Review this component:
[component code]

# Diagnose issues
@frontend/components What are the problems with this component?
[component code]

# Get best practices
@frontend/components How to optimize this component?
[component code]
```

## Troubleshooting

### Skill Not Triggering

- Check if the skill is properly installed
- Verify the skill name is correct
- Ensure the request matches the skill's description

### Incomplete Responses

- Provide more context in your request
- Ask follow-up questions for clarification
- Check the reference documents for more details

### Unexpected Results

- Review the skill's guidelines
- Check if requirements are clear
- Provide specific examples of expected behavior

---

**Last Updated**: 2026-01-19
**Version**: 1.0
**Maintainer**: Frontend Team
