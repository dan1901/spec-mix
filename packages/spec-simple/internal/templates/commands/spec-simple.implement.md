---
description: Execute implementation based on plan phases
---

## Execution Flow

### 1. Detect Feature

```bash
BRANCH=$(git branch --show-current 2>/dev/null)
SPEC_DIR="specs/$BRANCH"
```

If not on a feature branch, check `specs/` for the most recent feature directory.

### 2. Load Context

- Read `$SPEC_DIR/spec.md` (required)
- Read `$SPEC_DIR/plan.md` (required — abort if missing)
- Read `specs/constitution.md` if it exists

### 3. Identify Current Phase

Parse the **Implementation Phases** section of `plan.md`.

Check `$SPEC_DIR/` for existing walkthrough files (`walkthrough-phase-N.md`) to determine which phases are already completed.

Select the first incomplete phase.

### 4. Execute Phase

For the current phase:

1. **Implement**: Write code according to the phase deliverables
2. **Test**: Run relevant tests if a testing framework is configured
3. **Commit**: Commit changes with message `[Phase N] {phase name}`

### 5. Generate Walkthrough

Create `$SPEC_DIR/walkthrough-phase-{N}.md`:

```markdown
# Phase {N} Walkthrough: {Phase Name}

## Changes Made
- {file}: {what changed and why}

## How to Verify
- {step-by-step verification instructions}

## Status: PENDING REVIEW
```

### 6. Review

Present the walkthrough and ask:

```text
Phase {N} complete. Review the walkthrough above.

| Choice | Action |
|--------|--------|
| ACCEPT | Mark phase done, proceed to next |
| REJECT | Describe what needs fixing |
```

- **ACCEPT**: Update walkthrough status to `ACCEPTED`, proceed to next phase
- **REJECT**: Fix issues based on feedback, regenerate walkthrough, re-review

### 7. Repeat or Finish

If more phases remain, go to step 3.

When all phases are complete:

```text
✓ All phases implemented and accepted.

Summary:
  Phase 1: {name} ✓
  Phase 2: {name} ✓
  ...

Next steps:
  - Review all changes: git log --oneline main..HEAD
  - Merge to main: git checkout main && git merge {BRANCH}
```
