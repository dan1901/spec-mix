---
description: Create feature specification from natural language description
---

## User Input

```text
$ARGUMENTS
```

## Execution Flow

### 1. Generate Branch Name

From the feature description, create a 2–4 word short name:

- "Add user authentication" → `user-auth`
- "Fix payment timeout" → `fix-payment-timeout`

### 2. Create Feature Branch

```bash
git fetch --all --prune 2>/dev/null || true

# Determine the next feature number
# Check: local branches, remote branches, specs/ directories
EXISTING=$(
  { git branch --list '[0-9]*' 2>/dev/null;
    git branch -r --list 'origin/[0-9]*' 2>/dev/null | sed 's|origin/||';
    ls specs/ 2>/dev/null; } | grep -oE '^[0-9]+' | sort -n | tail -1
)
NEXT=$(printf "%03d" $(( ${EXISTING:-0} + 1 )))
BRANCH="${NEXT}-<short-name>"

git checkout -b "$BRANCH"
mkdir -p "specs/$BRANCH"
```

### 3. Load Context

- Read `.spec-simple/templates/spec-template.md` for structure
- Read `specs/constitution.md` if it exists (for project principles)

### 4. Write Specification

Create `specs/{BRANCH}/spec.md` by filling template sections:

- **Feature Info**: Name, branch, date
- **User Stories**: As a [user], I want... with P1/P2/P3 priorities
- **Functional Requirements**: FR-001, FR-002, ... (testable)
- **Success Criteria**: SC-001, SC-002, ... (measurable outcomes)

**Rules**:

- Focus on WHAT, not HOW
- No implementation details (languages, APIs, frameworks)
- Mark critical unknowns as `[NEEDS CLARIFICATION]` (max 3)

### 5. Completion

```text
✓ Specification created: specs/{BRANCH}/spec.md

Next: /spec-simple.plan
```
