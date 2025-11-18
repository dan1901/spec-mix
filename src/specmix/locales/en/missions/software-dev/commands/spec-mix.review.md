---
description: Review completed work and move approved tasks to done lane
---

## User Input

```text
$ARGUMENTS

```text
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
      - ✅ Follows project principles (if `specs/constitution.md` exists)?
      - ✅ Tests passing (if applicable)?
      - ✅ Documentation updated?
      - ✅ No obvious bugs or issues?

   c. **Decision**:
      - **APPROVE**: Task meets all criteria
      - **REQUEST CHANGES**: Issues found that need fixing

4. **For approved tasks**:
   ```bash
   .spec-mix/scripts/bash/move-task.sh WPxx for_review done specs/{feature}
   ```

   - Move work package from `for_review/` to `done/`
   - Update frontmatter: `lane: done`, `completed_at: <timestamp>`
   - Append to activity log

5. **For tasks needing changes**:
   ```bash
   .spec-mix/scripts/bash/move-task.sh WPxx for_review doing specs/{feature}
   ```

   - Move back to `doing/` lane
   - **IMPORTANT**: Append structured review feedback to the WP file's Activity Log
   - Use the format below to provide clear, actionable feedback

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

- [ ] **Constitution Compliance**: Follows project principles defined in `specs/constitution.md` (if exists)

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

- Run `/spec-mix.accept` when all tasks are in done lane

## Structured Review Feedback Format

When appending review feedback to a Work Package file's Activity Log, use this structured format for clarity and consistency:

### For APPROVED tasks:

```markdown
- {TIMESTAMP}: [REVIEW] APPROVED by {REVIEWER_NAME}
  - ✅ All acceptance criteria met
  - ✅ Code quality meets standards
  - ✅ Tests passing
  - ✅ Documentation updated
```

### For tasks NEEDING CHANGES:

```markdown
- {TIMESTAMP}: [REVIEW] CHANGES REQUESTED by {REVIEWER_NAME}
  - ❌ Issue 1: {Description of problem}
    - Location: {file:line or section}
    - Action: {What needs to be fixed}
  - ❌ Issue 2: {Description of problem}
    - Location: {file:line or section}
    - Action: {What needs to be fixed}
  - ✅ {What was done well}
  - Next steps: {Summary of required changes}
```

### Example - Approved:

```markdown
- 2025-11-18T10:30:00Z: [REVIEW] APPROVED by Claude
  - ✅ All acceptance criteria met
  - ✅ HttpMethod enum correctly implements GET, POST, PUT, DELETE, PATCH
  - ✅ Unit tests cover all methods with 100% coverage
  - ✅ Type hints and docstrings complete
  - ✅ Follows project code style guidelines
```

### Example - Changes Requested:

```markdown
- 2025-11-18T10:45:00Z: [REVIEW] CHANGES REQUESTED by Claude
  - ❌ Missing error handling in login function
    - Location: src/auth/login.py:45-60
    - Action: Add try-catch blocks for network errors and invalid credentials
  - ❌ Test coverage insufficient
    - Location: tests/test_auth.py
    - Action: Add tests for edge cases (empty password, special characters, SQL injection)
  - ❌ API documentation outdated
    - Location: docs/api.md
    - Action: Update authentication endpoint documentation with new error codes
  - ✅ Core authentication logic is solid and well-structured
  - ✅ Password hashing implementation follows best practices
  - Next steps: Address the 3 issues above, then move back to for_review
```

### Benefits of Structured Format:

- **Clarity**: Reviewer and implementer both understand what's needed
- **Actionable**: Specific locations and actions make fixes straightforward
- **Trackable**: Easy to verify all issues are addressed in next review
- **Positive**: Acknowledges what works well, not just problems
- **Audit Trail**: Creates permanent record in WP file's Activity Log
- **Dashboard-ready**: Structured format can be parsed and displayed in timeline

### How to Append to WP File:

After running `move-task.sh`, manually append the review feedback to the WP file:

```bash
# Example: Appending review feedback
echo "" >> specs/{feature}/tasks/doing/WP02.md
echo "- $(date -u +%Y-%m-%dT%H:%M:%SZ): [REVIEW] CHANGES REQUESTED by Claude" >> specs/{feature}/tasks/doing/WP02.md
echo "  - ❌ Missing error handling in login function" >> specs/{feature}/tasks/doing/WP02.md
echo "    - Location: src/auth/login.py:45-60" >> specs/{feature}/tasks/doing/WP02.md
echo "    - Action: Add try-catch blocks for network errors" >> specs/{feature}/tasks/doing/WP02.md
# ... etc
```

Or simply edit the WP file directly and add the structured feedback to the Activity Log section.

```text