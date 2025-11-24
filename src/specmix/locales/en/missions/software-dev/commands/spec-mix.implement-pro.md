---
description: Execute implementation with Work Package lane workflow (Pro Mode)
scripts:
  sh: scripts/bash/check-prerequisites.sh --json --require-tasks --include-tasks
  ps: scripts/powershell/check-prerequisites.ps1 -Json -RequireTasks -IncludeTasks
---

## User Input

```text
$ARGUMENTS
```

## Lane Workflow (MANDATORY)

```
planned → doing → for_review → done
```

**Rules**:
- Task MUST be in `doing` before coding
- Commits MUST include `[WP##]`
- Completed tasks MUST move to `for_review`

## Execution Flow

### 1. Run Prerequisites Script

```bash
{SCRIPT}
```
Parse FEATURE_DIR from output.

### 2. Check Lane Status

```bash
ls $FEATURE_DIR/tasks/{planned,doing,for_review,done}/*.md 2>/dev/null | wc -l
```

Display:
```
Lane Status:
├─ planned:    X tasks
├─ doing:      X tasks
├─ for_review: X tasks
└─ done:       X tasks
```

### 3. Select Task

- If task in `doing`: Continue or select new
- If no task in `doing`: Select from `planned`

Move task:
```bash
bash .spec-mix/scripts/bash/move-task.sh WP## planned doing $FEATURE_DIR
```

### 4. Load Context

Read (in order):
1. `tasks.md` - task list
2. `plan.md` - architecture
3. `constitution.md` - principles (if exists)
4. `data-model.md` (if exists)

### 5. Implement

**Before coding**: Verify task in `doing`

Execute by phase:
- Setup → Tests → Core → Integration → Polish
- Respect dependencies
- Follow TDD when applicable

### 6. Commit

Format:
```bash
git commit -m "[WP##] Brief description

- Change 1
- Change 2"
```

### 7. Complete Task

Move to review:
```bash
bash .spec-mix/scripts/bash/move-task.sh WP## doing for_review $FEATURE_DIR
```

### 8. Generate Walkthrough

Create `$FEATURE_DIR/walkthrough.md`:

```markdown
# Implementation Walkthrough

**Generated**: {timestamp}

## Tasks Completed
- WP## - {description}

## Files Modified
{git diff --name-status}

## Key Changes
- **{file}**: {change description}

## Next Steps
1. Run /spec-mix.review
2. After review, run /spec-mix.accept
```

## Next Steps

```
✓ Implementation complete for WP##

Next:
1. /spec-mix.review - Review completed work
2. /spec-mix.accept - Acceptance check
3. /spec-mix.merge - Merge to main
```
