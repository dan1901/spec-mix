---
description: Interactive guided review process for tasks in for_review lane
---

## User Input

```text

$ARGUMENTS

```

Consider the user input **before** proceeding if it is not empty.

## Overview

This command provides an **interactive, guided review experience** for tasks in the `for_review` lane. Instead of manual review, the AI assistant walks you through each task systematically, helps you fill out structured review feedback, and automatically updates the task status.

## Key Differences from `/spec-mix.review`

| Feature | `/spec-mix.review` | `/spec-mix.review-interactive` |
|---------|-------------------|-------------------------------|
| Review Mode | Automated/manual | Guided interactive |
| Feedback Format | AI-generated or manual | Step-by-step structured form |
| User Interaction | Minimal | High (Q&A style) |
| Review Document | Optional | Always generated |
| Best For | Quick batch reviews | Detailed, thorough reviews |

## Execution Flow

### 1. Identify Feature Directory

```bash
# Detect current feature from branch or directory
FEATURE=$(bash .spec-mix/scripts/bash/common.sh get_current_branch)

# Or use user-provided feature
FEATURE="001-feature-name"
```

If no feature found, prompt user to specify.

### 2. Scan for Tasks in for_review

```bash
ls specs/{feature}/tasks/for_review/*.md
```

**If no tasks**:
- Inform user: "No tasks currently in for_review lane"
- Suggest checking `doing` lane or running `/spec-mix.implement`
- Exit

**If tasks found**:
- List all tasks with brief summary
- Ask user: "Which task would you like to review? (or type 'all' to review all tasks)"

### 3. For Each Selected Task

#### Step 3.1: Load Task Context

Read the Work Package file:

```bash
cat specs/{feature}/tasks/for_review/WPxx.md
```

Display to user:
- Task ID and title
- Acceptance criteria
- Git history (if available)
- Activity log summary

#### Step 3.2: Guide Review Questions

Ask the user the following questions **one by one**, gathering responses:

**Question 1: Acceptance Criteria**
```
Let's review the acceptance criteria. For each criterion, type:
- ✅ if met
- ❌ if not met
- ⚠️ if partially met

Criterion 1: [description]
Your assessment: _____

Criterion 2: [description]
Your assessment: _____

...
```

**Question 2: Code Quality**
```
On a scale of 1-5, how would you rate the code quality?
1 = Poor (needs major refactoring)
2 = Below average (multiple issues)
3 = Acceptable (minor improvements needed)
4 = Good (meets standards)
5 = Excellent (exemplary)

Rating: _____

What are the strengths of this implementation? (list 2-3 points)
1. _____
2. _____
3. _____
```

**Question 3: Issues Found**
```
Did you find any issues that need to be addressed? (yes/no)

If yes, for each issue:
  - Issue title: _____
  - Severity: [Critical/Major/Minor]
  - Location: [file:line or section]
  - Description: _____
  - Action required: _____

Type 'done' when finished listing issues.
```

**Question 4: Testing**
```
Are there adequate tests for this implementation? (yes/no/partial)

If no or partial, what tests are missing? _____
```

**Question 5: Documentation**
```
Is the documentation complete and up-to-date? (yes/no/partial)

If no or partial, what needs to be documented? _____
```

**Question 6: Security & Performance**
```
Did you notice any security vulnerabilities? (yes/no)
If yes, describe: _____

Did you notice any performance issues? (yes/no)
If yes, describe: _____
```

#### Step 3.3: Generate Review Decision

Based on the responses:

```
Based on your feedback, I recommend:

[X] APPROVED - All criteria met, minor or no issues
[ ] CHANGES REQUESTED - Critical/major issues found or multiple criteria not met

Do you agree with this recommendation? (yes/no)
If no, which decision would you prefer? _____
```

#### Step 3.4: Generate Review Feedback Document

Using the `review-feedback-template.md`, fill in all responses:

```bash
# Create review feedback document
cat specs/{feature}/tasks/for_review/review-feedback-template.md | \
    sed "s/\[TASK_ID\]/$TASK_ID/g" | \
    sed "s/\[REVIEWER_NAME\]/$USER_NAME/g" | \
    # ... fill in all template placeholders
    > specs/{feature}/tasks/for_review/WPxx-review-feedback.md
```

Show the generated document to the user:
```
I've generated the following review feedback document.
Please review and confirm if it looks correct.

[Display generated document]

Would you like to:
1. Approve and proceed
2. Edit the document manually
3. Cancel this review

Your choice: _____
```

#### Step 3.5: Update Work Package Activity Log

Append the structured review feedback to the WP file:

```bash
# Generate timestamp
TIMESTAMP=$(date -u +%Y-%m-%dT%H:%M:%SZ)

# Append review feedback
echo "" >> specs/{feature}/tasks/for_review/WPxx.md
echo "## Review Feedback" >> specs/{feature}/tasks/for_review/WPxx.md
echo "" >> specs/{feature}/tasks/for_review/WPxx.md

# For APPROVED
if [[ $DECISION == "APPROVED" ]]; then
    echo "- $TIMESTAMP: [REVIEW] APPROVED by $REVIEWER_NAME" >> ...
    echo "  - ✅ All acceptance criteria met ($CRITERIA_MET/$CRITERIA_TOTAL)" >> ...
    echo "  - ✅ Code quality rated $QUALITY_RATING/5" >> ...
    # ... add all positive points
fi

# For CHANGES REQUESTED
if [[ $DECISION == "CHANGES_REQUESTED" ]]; then
    echo "- $TIMESTAMP: [REVIEW] CHANGES REQUESTED by $REVIEWER_NAME" >> ...
    # ... add all issues
    # ... add positive points
    echo "  - Next steps: $NEXT_STEPS_SUMMARY" >> ...
fi
```

#### Step 3.6: Move Task to Appropriate Lane

**If APPROVED**:
```bash
.spec-mix/scripts/bash/move-task.sh WPxx for_review done specs/{feature}
```

**If CHANGES REQUESTED**:
```bash
.spec-mix/scripts/bash/move-task.sh WPxx for_review doing specs/{feature}
```

#### Step 3.7: Update tasks.md

If task is approved, mark it as completed in `tasks.md`:

```bash
# Update task status
sed -i "s/- \[ \] WPxx:/- [x] WPxx:/" specs/{feature}/tasks.md
```

#### Step 3.8: Ask About Next Task

```
Task WPxx review complete!

Decision: [APPROVED/CHANGES REQUESTED]
Moved to: [done/doing] lane

Would you like to review the next task? (yes/no)
```

### 4. Final Summary

After all reviews are complete:

```markdown
# Review Session Summary

**Feature**: {feature-name}
**Reviewer**: {reviewer-name}
**Date**: {date}

## Tasks Reviewed

### ✅ Approved (moved to done)
- WP01: Task title 1
- WP03: Task title 3

### 🔄 Changes Requested (moved back to doing)
- WP02: Task title 2 (Issues: testing coverage, documentation)
- WP04: Task title 4 (Issues: error handling)

## Progress
- Reviewed: 4 tasks
- Approved: 2 tasks (50%)
- Changes needed: 2 tasks (50%)
- Remaining in for_review: 0 tasks

## Next Steps
1. Address feedback for WP02 and WP04
2. Re-submit for review when ready
3. Once all tasks approved, run `/spec-mix.accept` for final acceptance
```

## User Experience Enhancements

### Progress Tracking

Show progress during multi-task reviews:

```
[Task 2 of 5] Reviewing WP02: User Authentication
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 40%

✅ WP01 - Approved
➡️  WP02 - In Progress
⏳ WP03 - Pending
⏳ WP04 - Pending
⏳ WP05 - Pending
```

### Smart Defaults

For common scenarios, offer smart defaults:

```
All acceptance criteria are met (✅), no issues found, and code quality is rated 4/5.

Would you like me to auto-approve this task? (yes/no)
If yes, I'll generate standard approval feedback.
If no, we'll continue with detailed review questions.
```

### Review Templates by Severity

Offer quick templates for common review outcomes:

```
I can help you speed up this review. Select a template:

1. Quick Approve - All good, standard approval
2. Minor Tweaks - Small issues, approve with suggestions
3. Major Rework - Significant issues, send back to doing
4. Custom Review - Full guided review (recommended for complex tasks)

Your choice: _____
```

## Integration with Dashboard

The dashboard will display:
- Review history timeline for each task
- Reviewer names and decisions
- Issue trends across tasks
- Review velocity metrics

See `/spec-mix.dashboard` for visualization.

## Best Practices

1. **Review Regularly**: Don't let tasks pile up in for_review
2. **Be Specific**: Provide exact file locations and clear action items
3. **Balance Criticism**: Always highlight positives alongside issues
4. **Track Patterns**: If multiple tasks have similar issues, consider updating the constitution or plan
5. **Use Dashboard**: Visualize review history and trends

## Example Session

```
User: /spec-mix.review-interactive

AI: I found 3 tasks in for_review lane for feature 001-user-authentication:
    - WP01: Implement login endpoint
    - WP02: Add password reset flow
    - WP03: Create user profile API

    Which task would you like to review? (1-3, or 'all')

User: all

AI: Great! Let's start with WP01: Implement login endpoint

    [Displays task details, acceptance criteria, git history]

    Let's review the acceptance criteria. For each criterion, type ✅ if met, ❌ if not met:

    1. POST /api/login endpoint accepts email and password
    Your assessment:

User: ✅

AI: 2. Returns JWT token on successful authentication
    Your assessment:

User: ✅

AI: 3. Returns 401 for invalid credentials
    Your assessment:

User: ✅

AI: Excellent! All 3 acceptance criteria are met.

    On a scale of 1-5, how would you rate the code quality?

User: 4

AI: Good rating! What are the strengths of this implementation? (list 2-3 points)

User:
1. Clean error handling with proper status codes
2. Well-documented API with OpenAPI spec
3. Secure password hashing with bcrypt

AI: Did you find any issues that need to be addressed? (yes/no)

User: yes

AI: Issue #1:
    Issue title:

User: Missing rate limiting

AI: Severity: [Critical/Major/Minor]

User: Major

AI: Location: [file:line or section]

User: src/api/auth.py:login route

AI: Description:

User: The login endpoint has no rate limiting, which makes it vulnerable to brute force attacks

AI: Action required:

User: Add Flask-Limiter with 5 attempts per minute per IP

AI: Got it. Any more issues? (yes to add another, no to continue)

User: no

AI: Based on your feedback:
    - 3/3 acceptance criteria met
    - Code quality: 4/5
    - 1 major issue found (rate limiting)

    I recommend: CHANGES REQUESTED

    Do you agree? (yes/no)

User: yes

AI: Perfect. I've generated the review feedback document.
    [Shows document]

    Would you like to:
    1. Approve and proceed
    2. Edit manually
    3. Cancel

User: 1

AI: ✅ Review complete for WP01!

    Decision: CHANGES REQUESTED
    Moved to: doing lane
    Feedback saved to: WP01-review-feedback.md

    [Progress: 1 of 3 tasks reviewed]

    Would you like to review the next task (WP02)? (yes/no)

User: yes

...
```

## Notes

- Review feedback documents are saved in `specs/{feature}/tasks/for_review/WPxx-review-feedback.md`
- Activity log entries are appended directly to the WP file
- The interactive review process typically takes 3-5 minutes per task
- For faster batch reviews, use `/spec-mix.review` instead

---

**Command Version**: 1.0
**Last Updated**: 2025-11-18
