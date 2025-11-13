---
description: Review completed work and move approved tasks to done lane
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Outline

This command helps you review work that has been completed and moved to the `for_review` lane. You'll examine each task, verify it meets acceptance criteria, and either approve it (moving to `done`) or request changes.

## Execution Flow

1. **Identify feature directory**:
   - Use current branch to find feature (e.g., `001-feature-name`)
   - Locate `specs/{feature}/tasks/for_review/` directory

2. **Scan for review tasks**:
   ```bash
   ls specs/{feature}/tasks/for_review/*.md
   ```
   - If no tasks found, inform user and exit
   - List all work packages awaiting review

3. **For each task in for_review**:

   a. **Read work package**:
      - Open `WPxx.md` file
      - Review the objective, acceptance criteria, implementation notes
      - Check activity log for context

   b. **Verify completion**:
      - ✅ All acceptance criteria met?
      - ✅ Code quality acceptable?
      - ✅ Tests passing (if applicable)?
      - ✅ Documentation updated?
      - ✅ No obvious bugs or issues?

   c. **Decision**:
      - **APPROVE**: Task meets all criteria
      - **REQUEST CHANGES**: Issues found that need fixing

4. **For approved tasks**:
   ```bash
   .specify/scripts/bash/move-task.sh WPxx for_review done specs/{feature}
   ```
   - Move work package from `for_review/` to `done/`
   - Update frontmatter: `lane: done`, `completed_at: <timestamp>`
   - Append to activity log

5. **For tasks needing changes**:
   ```bash
   .specify/scripts/bash/move-task.sh WPxx for_review doing specs/{feature}
   ```
   - Move back to `doing/` lane
   - Document specific issues in activity log
   - Provide clear feedback on what needs to change

6. **Update tasks.md**:
   - Mark completed tasks with `[x]`
   - Update status summary

7. **Report summary**:
   ```
   Review Summary:
   ✅ Approved: WP01, WP03, WP05
   🔄 Needs changes: WP02 (missing tests), WP04 (documentation incomplete)
   📊 Progress: 3/5 tasks complete (60%)
   ```

## Quality Checks

Before approving a task, verify:

- [ ] **Functionality**: Feature works as specified
- [ ] **Code Quality**: Readable, maintainable, follows conventions
- [ ] **Tests**: Appropriate test coverage
- [ ] **Documentation**: Code comments, README updates
- [ ] **No Regressions**: Existing functionality still works
- [ ] **Acceptance Criteria**: All criteria from WP file met

## Edge Cases

- **Empty for_review lane**: Inform user no tasks are ready for review
- **Partial completion**: If some criteria met but not all, provide specific feedback
- **Multiple reviewers**: Check if task has review metadata to avoid duplicate reviews

## Output Format

Present review results clearly:

```markdown
# Review Report: {feature-name}

## Reviewed: {date}

### ✅ Approved Tasks (moved to done)

#### WP01: User Authentication
- All acceptance criteria met
- Tests passing
- Documentation updated
- No issues found

### 🔄 Tasks Needing Changes (moved back to doing)

#### WP02: Password Reset
- ❌ Missing unit tests for edge cases
- ❌ Error messages not user-friendly
- ✅ Core functionality works

**Action needed**: Add tests and improve error handling

## Next Steps

- Address feedback for WP02
- Continue with remaining planned tasks
- Run `/speckit.accept` when all tasks are in done lane
```
