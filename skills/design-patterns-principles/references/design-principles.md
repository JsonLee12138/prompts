# Design Principles (Full)

> Scope: all languages and projects

This document summarizes core design principles, quality attributes, technical guidelines, a decision framework, anti-patterns, and implementation checklists to standardize team design and delivery.

## Core Principles

### 1. Separation of Concerns (SoC)
**Definition**: Split the system into parts with clear, minimally overlapping responsibilities.  
**Use Cases**:
- Layered architecture, MVC/MVVM
- Microservices/modular systems
**Pros**:
- Lower coupling, better maintainability
- Easier independent testing and collaboration
**Implementation Tips**:
- Separate business logic from infrastructure
- Separate UI/presentation from domain logic
- Separate data access from business rules

### 2. Single Responsibility Principle (SRP)
**Definition**: A class/module should have one and only one responsibility.  
**Use Cases**:
- Class design, module boundaries, API design
**Pros**:
- Easier to understand, maintain, and test
**Implementation Tips**:
- One reason to change
- Public methods serve a single goal

### 3. DRY (Don’t Repeat Yourself)
**Definition**: Avoid duplicated logic by abstracting shared behavior.  
**Use Cases**:
- Business logic, validation rules, data transformations
**Pros**:
- Lower maintenance cost, fewer inconsistencies
**Implementation Tips**:
- Extract shared functions/modules
- Use parameterization or configuration

### 4. KISS (Keep It Simple, Stupid)
**Definition**: Prefer the simplest workable solution.  
**Use Cases**:
- Architecture choices and implementation design
**Pros**:
- Lower complexity, fewer bugs
**Implementation Tips**:
- Avoid over-abstraction
- Don’t design for hypothetical future needs

### 5. Composition Over Inheritance
**Definition**: Prefer composition to inheritance for reuse.  
**Use Cases**:
- Behavior extension, plugin systems
**Pros**:
- More flexible, lower coupling
**Implementation Tips**:
- Prefer interfaces + dependency injection
- Use inheritance only for strict is-a relationships

### 6. High Cohesion, Low Coupling
**Definition**: Keep related responsibilities together and minimize dependencies between modules.  
**Use Cases**:
- Module design, service boundaries
**Pros**:
- Smaller change impact
**Implementation Tips**:
- Depend on interfaces
- Avoid cyclic dependencies

### 7. Explicit Dependencies
**Definition**: Declare all dependencies explicitly.  
**Use Cases**:
- Class design, function signatures, service composition
**Pros**:
- Easier testing, clearer dependencies
**Implementation Tips**:
- Constructor/parameter injection
- Avoid globals and hidden singletons

### 8. Fail Fast and Loud
**Definition**: Validate early at boundaries and surface errors clearly.  
**Use Cases**:
- API boundaries, data validation, external calls
**Pros**:
- Early detection, easier diagnosis
**Implementation Tips**:
- Use explicit error types
- Avoid silent failures

### 9. Immutability by Default
**Definition**: Prefer immutable data to reduce state mutation.  
**Use Cases**:
- Concurrency, state management
**Pros**:
- Predictable state, thread safety
**Implementation Tips**:
- Create new objects on updates
- Avoid shared mutable state

### 10. Testability First
**Definition**: Design with testability as a first-class concern.  
**Use Cases**:
- All core business logic
**Pros**:
- Safer refactoring, controlled quality
**Implementation Tips**:
- Dependency injection
- Small, focused functions

---

## Quality Attributes

### Performance
**Principle**: Measure before optimizing, optimize the common path.  
**Typical Targets**:
- API P50 < 100ms
- API P95 < 200ms
- API P99 < 500ms

**Strategies**:
- Caching and indexing
- Async processing for long tasks
- Avoid unnecessary recomputation

### Security
**Principle**: Least privilege, never trust input, defense in depth.  
**Checklist**:
- Input validation and sanitization
- SQL injection / XSS / CSRF protection
- Authentication, authorization, audit logs
- Sensitive data encryption and masking

### Scalability
**Principle**: Stateless design and horizontal scale.  
**Strategies**:
- Read/write separation
- Message queues for decoupling
- Multi-layer caching

### Maintainability
**Principle**: Consistency, clear structure, synchronized docs.  
**Strategies**:
- Unified naming and conventions
- Code reviews and regular refactoring
- Keep docs aligned with implementation

---

## Technical Guidelines

### API Design
**RESTful conventions**:
- GET /resources
- GET /resources/{id}
- POST /resources
- PUT /resources/{id}
- PATCH /resources/{id}
- DELETE /resources/{id}

**Status code guidance**:
- 200 OK
- 201 Created
- 204 No Content
- 400 Bad Request
- 401 Unauthorized
- 403 Forbidden
- 404 Not Found
- 500 Internal Server Error

### Database Design
**Principles**:
- Normalize to 3NF
- Index key fields
- Plan for soft delete and migrations

### Frontend Architecture
**Component principles**:
- Container vs presentational components
- Single responsibility
- Layered state management

**Performance optimizations**:
- Route-based lazy loading
- Code splitting
- Image compression and lazy loading

---

## Decision Framework

1. **Understand the problem**
- What is the goal?
- What constraints and success criteria exist?

2. **Collect options**
- At least 2–3 viable approaches
- Compare build vs buy vs open source

3. **Evaluate tradeoffs**
- Simplicity, cost, risk, performance, maintainability

4. **Record the decision**
- Use an ADR

5. **Review and approve**
- Peer review + tech lead approval

---

## Anti-Patterns (Common)

**God Object**  
Symptom: One class takes too many responsibilities  
Fix: Split responsibilities, return to SRP

**Circular Dependencies**  
Symptom: A depends on B, B depends on A  
Fix: Extract shared modules, apply dependency inversion

**Shotgun Surgery**  
Symptom: One change requires edits in many places  
Fix: Increase cohesion, extract shared modules

**Duplicate Code**  
Symptom: Same logic appears in multiple places  
Fix: Extract shared functions/modules

---

## Implementation Checklist

**Project Start**
- Architecture principles agreed
- Directory structure and conventions set
- Tech stack decisions recorded

**Design Phase**
- Module boundaries defined
- Dependencies mapped
- API and data models designed

**Implementation Phase**
- Unit tests on critical paths
- Logging and monitoring in place
- Error handling complete

**Code Review**
- Single responsibility
- Explicit dependencies
- No duplicate code
- Clear naming

**Pre-Deployment**
- Performance testing complete
- Security scans complete
- Documentation updated

---

## Appendix

### Glossary
- DRY: Don’t Repeat Yourself
- KISS: Keep It Simple, Stupid
- SoC: Separation of Concerns
- YAGNI: You Aren’t Gonna Need It
- ADR: Architecture Decision Record

### Recommended Reading
- Design Patterns (GoF)
- Refactoring (Martin Fowler)
- Clean Architecture (Robert C. Martin)
- Domain-Driven Design (Eric Evans)
