---
description: Execute phase-based implementation with walkthrough and review (Normal Mode)
---

## Overview

Normal Mode executes implementation **phase by phase**:
1. Execute one phase at a time
2. Generate walkthrough after completion
3. Present review → User accepts/rejects
4. Proceed to next phase after acceptance

## Step 1: Load Phase Info

```bash
# Get feature directory
FEATURE_DIR=$(cat .spec-mix/config.json | grep -o '"feature_dir"[^,]*' | cut -d'"' -f4)
```

Read `$FEATURE_DIR/tasks.md` and display:
```
Phase Progress:
├─ Phase 1: {name} - ✓ Complete
├─ Phase 2: {name} - ⏳ Current
└─ Phase 3: {name} - ○ Pending
```

## Step 2: Execute Current Phase

1. Display phase name and deliverables
2. Implement all deliverables
3. Write tests if applicable
4. Commit with descriptive messages
5. Mark phase complete in tasks.md

## Step 3: Generate Walkthrough

Create `$FEATURE_DIR/walkthrough-phase-{N}.md`:

```markdown
# Walkthrough: Phase {N} - {Name}

**Generated**: {timestamp}

## Summary
{What was accomplished}

## Files Changed
{git diff --name-status}

## Key Changes
- **File**: {path} - {description}

## Commits
{git log --oneline}
```

## Step 4: Present Review

```markdown
## Phase {N} Complete - Review

📄 Walkthrough: `walkthrough-phase-{N}.md`

### Summary
{2-3 sentences}

### Files Modified
- {file list}

---
| Choice | Action |
|--------|--------|
| **ACCEPT** | Proceed to next phase |
| **REJECT** | Request changes |

Type ACCEPT or REJECT:
```

## Step 5: Handle Decision

**ACCEPT**: Mark accepted, proceed to next phase (or final completion)
**REJECT**: Get feedback, make changes, re-generate walkthrough

## Step 6: Final Completion

When all phases accepted:
```markdown
## Implementation Complete

All phases accepted. Run `/spec-mix.merge` to finalize.
```
