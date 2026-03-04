---
description: Generate implementation plan from feature specification
---

## User Input

```text
$ARGUMENTS
```

## Execution Flow

### 1. Detect Feature

Identify the current feature from the git branch name:

```bash
BRANCH=$(git branch --show-current 2>/dev/null)
# Extract feature directory: specs/{NNN-feature-name}/
SPEC_DIR="specs/$BRANCH"
```

If not on a feature branch, check `specs/` for the most recent feature directory.

### 2. Load Context

- Read `$SPEC_DIR/spec.md` (required — abort if missing)
- Read `.spec-simple/templates/plan-template.md` for structure
- Read `specs/constitution.md` if it exists

### 3. Write Plan

Create `$SPEC_DIR/plan.md` by filling the plan template:

**Summary**: Extract primary requirement + proposed technical approach.

**Technical Context**: Fill in:

- Language/Version
- Primary Dependencies
- Storage (if applicable)
- Testing framework
- Target Platform

Mark unknowns as `[NEEDS CLARIFICATION]`.

**Project Structure**: Describe where new/modified files will live.

**Implementation Phases**: Break implementation into phases (max 5).

Each phase must include:

- **Name**: Short descriptive name
- **Deliverables**: Concrete files or changes
- **Acceptance Criteria**: How to verify the phase is complete

### 4. Completion

```text
✓ Plan created: $SPEC_DIR/plan.md

Phases:
  1. {Phase 1 name}
  2. {Phase 2 name}
  ...

Next: /spec-simple.implement
```
