---
description: Execute the implementation plan by processing and executing all tasks defined in tasks.md
scripts:
  sh: scripts/bash/check-prerequisites.sh --json --require-tasks --include-tasks
  ps: scripts/powershell/check-prerequisites.ps1 -Json -RequireTasks -IncludeTasks
---

## Mode Detection

**IMPORTANT**: First, check the project mode from `.spec-mix/config.json`:

```bash
cat .spec-mix/config.json 2>/dev/null | grep '"mode"' || echo "mode: pro"
```

- If `mode: "normal"` → Follow the **Normal Mode Workflow** section below
- If `mode: "pro"` or no config found → Follow the **Pro Mode Workflow** section below

---

# NORMAL MODE WORKFLOW

If the mode is `normal`, follow this phase-based implementation workflow with built-in walkthrough, review, and accept steps:

## Overview (Normal Mode)

Normal Mode executes implementation **phase by phase** with these key features:
1. Execute one phase at a time
2. Generate walkthrough after each phase completion
3. Present review summary to user
4. Offer Accept/Reject choice for each phase
5. Only proceed to next phase after acceptance

## Step 1: Load Phase Information

1. Run `{SCRIPT}` to get FEATURE_DIR and task information
2. Read `FEATURE_DIR/tasks.md` to identify phases
3. Determine current phase (first incomplete phase)
4. Display phase status:

```
Phase Progress:
├─ Phase 1: {name} - ✓ Complete
├─ Phase 2: {name} - ⏳ In Progress  ← Current
├─ Phase 3: {name} - ○ Pending
└─ Phase 4: {name} - ○ Pending
```

## Step 2: Execute Current Phase

For the current phase:

1. **Display Phase Details**:
   ```markdown
   ---
   ## Executing Phase {N}: {Phase Name}

   **Description**: {phase description}

   **Deliverables**:
   - {deliverable 1}
   - {deliverable 2}

   **Starting implementation...**
   ---
   ```

2. **Implement the Phase**:
   - Create/modify files as specified in deliverables
   - Follow the implementation plan and data model
   - Write tests if applicable
   - Commit changes with descriptive messages

3. **Mark Phase Complete in tasks.md**:
   - Update the phase section with completion status

## Step 3: Generate Walkthrough

After phase implementation, automatically generate a walkthrough document:

**Location**: `FEATURE_DIR/walkthrough-phase-{N}.md`

```markdown
# Walkthrough: Phase {N} - {Phase Name}

**Generated**: {timestamp}
**Feature**: {feature name}
**Branch**: {branch name}

## Summary
{Brief description of what was accomplished in this phase}

## Files Changed
```
{git diff --name-status for this phase}
```

## Key Changes

### {Component 1}
- **File**: {path}
- **Changes**: {description}
- **Why**: {rationale}

### {Component 2}
- **File**: {path}
- **Changes**: {description}
- **Why**: {rationale}

## Tests & Verification
- {Test results if applicable}
- {Manual verification steps}

## Commits
```
{git log --oneline for this phase}
```

## Notes
{Any important observations or decisions made}
```

## Step 4: Present Review

After generating walkthrough, present a review summary to the user:

```markdown
---
## Phase {N} Complete - Review

### Walkthrough Generated
📄 `FEATURE_DIR/walkthrough-phase-{N}.md`

### Summary
{2-3 sentence summary of what was implemented}

### Files Modified
- {file list with brief descriptions}

### Acceptance Criteria Status
- [x] {Criteria 1} - Met
- [x] {Criteria 2} - Met
- [ ] {Criteria 3} - Partially met (explain)

---

### Your Decision:

| Choice | Action |
|--------|--------|
| **ACCEPT** | Approve this phase and proceed to Phase {N+1} |
| **REJECT** | Request changes (explain what needs to be fixed) |

Type `ACCEPT` or `REJECT` with feedback:
---
```

## Step 5: Handle User Decision

**If user types ACCEPT:**
1. Mark phase as accepted in tasks.md
2. Update phase status to "Complete"
3. Check if more phases remain:
   - **If more phases**: Display "Phase {N+1} ready. Continue? (yes/no)"
   - **If last phase**: Proceed to Final Completion

**If user types REJECT:**
1. Parse user feedback
2. Display: "Understood. Please specify what needs to be changed."
3. After user provides details, make the requested changes
4. Re-run Step 3 (Generate Walkthrough) and Step 4 (Present Review)

## Step 6: Final Completion (After All Phases)

When all phases are accepted:

```markdown
---
## Implementation Complete

**All Phases Accepted**

| Phase | Status |
|-------|--------|
| Phase 1: {name} | ✓ Accepted |
| Phase 2: {name} | ✓ Accepted |
| Phase 3: {name} | ✓ Accepted |

### Generated Walkthroughs
- `walkthrough-phase-1.md`
- `walkthrough-phase-2.md`
- `walkthrough-phase-3.md`

### Final Step

Run `/spec-mix.merge` to merge your feature branch to main.

---
```

**END OF NORMAL MODE WORKFLOW**

---

# PRO MODE WORKFLOW

If the mode is `pro` or not specified, follow this workflow:

## User Input

```text
$ARGUMENTS

```text
You **MUST** consider the user input before proceeding (if not empty).

## MANDATORY LANE WORKFLOW ENFORCEMENT

**IMPORTANT**: The following lane workflow rules are STRICTLY ENFORCED:

1. **Before ANY code writing**: You MUST have a task in the `doing` lane
2. **Every commit**: MUST reference a Work Package ID [WP##]
3. **After completion**: Task MUST be moved to `for_review` lane

## Outline

1. Run `{SCRIPT}` from repo root and parse FEATURE_DIR and AVAILABLE_DOCS list. All paths must be absolute. For single quotes in args like "I'm Groot", use escape syntax: e.g 'I'\''m Groot' (or double-quote if possible: "I'm Groot").

2. **MANDATORY: Lane State Validation and Task Selection**:

   a. **Check current lane state**:
      ```bash
      # Check if tasks directory exists
      if [ ! -d "FEATURE_DIR/tasks" ]; then
          echo "ERROR: No tasks directory found. Run /spec-mix.tasks first"
          exit 1
      fi

      # Check for tasks in each lane
      PLANNED_COUNT=$(find FEATURE_DIR/tasks/planned -name "WP*.md" 2>/dev/null | wc -l)
      DOING_COUNT=$(find FEATURE_DIR/tasks/doing -name "WP*.md" 2>/dev/null | wc -l)
      REVIEW_COUNT=$(find FEATURE_DIR/tasks/for_review -name "WP*.md" 2>/dev/null | wc -l)
      DONE_COUNT=$(find FEATURE_DIR/tasks/done -name "WP*.md" 2>/dev/null | wc -l)
      ```

   b. **Display lane status**:
      ```
      Task Lane Status:
      ├─ planned:     [X tasks]
      ├─ doing:       [X tasks]
      ├─ for_review:  [X tasks]
      └─ done:        [X tasks]
      ```

   c. **ENFORCE: Select task to work on**:
      - If DOING_COUNT > 0:
        - List tasks currently in doing
        - Ask: "Continue with existing task or select a new one?"
      - If DOING_COUNT = 0:
        - List all tasks in planned lane
        - **REQUIRE** user to select a task: "Which task will you work on? (WP##)"
        - **BLOCK** if no selection made

   d. **Move selected task to doing**:
      ```bash
      bash .spec-mix/scripts/move-task.sh WP## planned doing FEATURE_DIR
      ```
      - Record task movement in activity log
      - Display: "✓ WP## moved to 'doing' lane - work can begin"

3. **Check checklists status** (if FEATURE_DIR/checklists/ exists):
   - Scan all checklist files in the checklists/ directory
   - For each checklist, count:
     - Total items: All lines matching `- [ ]` or `- [X]` or `- [x]`
     - Completed items: Lines matching `- [X]` or `- [x]`
     - Incomplete items: Lines matching `- [ ]`
   - Create a status table:

     ```text
     | Checklist | Total | Completed | Incomplete | Status |
     |-----------|-------|-----------|------------|--------|
     | ux.md     | 12    | 12        | 0          | ✓ PASS |
     | test.md   | 8     | 5         | 3          | ✗ FAIL |
     | security.md | 6   | 6         | 0          | ✓ PASS |
     ```

   - Calculate overall status:
     - **PASS**: All checklists have 0 incomplete items
     - **FAIL**: One or more checklists have incomplete items

   - **If any checklist is incomplete**:
     - Display the table with incomplete item counts
     - **STOP** and ask: "Some checklists are incomplete. Do you want to proceed with implementation anyway? (yes/no)"
     - Wait for user response before continuing
     - If user says "no" or "wait" or "stop", halt execution
     - If user says "yes" or "proceed" or "continue", proceed to step 3

   - **If all checklists are complete**:
     - Display the table showing all checklists passed
     - Automatically proceed to step 3

3. Load and analyze the implementation context:
   - **REQUIRED**: Read tasks.md for the complete task list and execution plan
   - **REQUIRED**: Read plan.md for tech stack, architecture, and file structure
   - **CONSTITUTION**: If `specs/constitution.md` exists, read it to ensure implementation follows project principles (code quality, testing standards, architectural constraints)
   - **IF EXISTS**: Read data-model.md for entities and relationships
   - **IF EXISTS**: Read contracts/ for API specifications and test requirements
   - **IF EXISTS**: Read research.md for technical decisions and constraints
   - **IF EXISTS**: Read quickstart.md for integration scenarios

4. **Project Setup Verification**:
   - **REQUIRED**: Create/verify ignore files based on actual project setup:

   **Detection & Creation Logic**:
   - Check if the following command succeeds to determine if the repository is a git repo (create/verify .gitignore if so):

     ```sh
     git rev-parse --git-dir 2>/dev/null
     ```

   - Check if Dockerfile* exists or Docker in plan.md → create/verify .dockerignore
   - Check if .eslintrc*or eslint.config.* exists → create/verify .eslintignore
   - Check if .prettierrc* exists → create/verify .prettierignore
   - Check if .npmrc or package.json exists → create/verify .npmignore (if publishing)
   - Check if terraform files (*.tf) exist → create/verify .terraformignore
   - Check if .helmignore needed (helm charts present) → create/verify .helmignore

   **If ignore file already exists**: Verify it contains essential patterns, append missing critical patterns only
   **If ignore file missing**: Create with full pattern set for detected technology

   **Common Patterns by Technology** (from plan.md tech stack):
   - **Node.js/JavaScript/TypeScript**: `node_modules/`, `dist/`, `build/`, `*.log`, `.env*`
   - **Python**: `__pycache__/`, `*.pyc`, `.venv/`, `venv/`, `dist/`, `*.egg-info/`
   - **Java**: `target/`, `*.class`, `*.jar`, `.gradle/`, `build/`
   - **C#/.NET**: `bin/`, `obj/`, `*.user`, `*.suo`, `packages/`
   - **Go**: `*.exe`, `*.test`, `vendor/`, `*.out`
   - **Ruby**: `.bundle/`, `log/`, `tmp/`, `*.gem`, `vendor/bundle/`
   - **PHP**: `vendor/`, `*.log`, `*.cache`, `*.env`
   - **Rust**: `target/`, `debug/`, `release/`, `*.rs.bk`, `*.rlib`, `*.prof*`, `.idea/`, `*.log`, `.env*`
   - **Kotlin**: `build/`, `out/`, `.gradle/`, `.idea/`, `*.class`, `*.jar`, `*.iml`, `*.log`, `.env*`
   - **C++**: `build/`, `bin/`, `obj/`, `out/`, `*.o`, `*.so`, `*.a`, `*.exe`, `*.dll`, `.idea/`, `*.log`, `.env*`
   - **C**: `build/`, `bin/`, `obj/`, `out/`, `*.o`, `*.a`, `*.so`, `*.exe`, `Makefile`, `config.log`, `.idea/`, `*.log`, `.env*`
   - **Swift**: `.build/`, `DerivedData/`, `*.swiftpm/`, `Packages/`
   - **R**: `.Rproj.user/`, `.Rhistory`, `.RData`, `.Ruserdata`, `*.Rproj`, `packrat/`, `renv/`
   - **Universal**: `.DS_Store`, `Thumbs.db`, `*.tmp`, `*.swp`, `.vscode/`, `.idea/`

   **Tool-Specific Patterns**:
   - **Docker**: `node_modules/`, `.git/`, `Dockerfile*`, `.dockerignore`, `*.log*`, `.env*`, `coverage/`
   - **ESLint**: `node_modules/`, `dist/`, `build/`, `coverage/`, `*.min.js`
   - **Prettier**: `node_modules/`, `dist/`, `build/`, `coverage/`, `package-lock.json`, `yarn.lock`, `pnpm-lock.yaml`
   - **Terraform**: `.terraform/`, `*.tfstate*`, `*.tfvars`, `.terraform.lock.hcl`
   - **Kubernetes/k8s**: `*.secret.yaml`, `secrets/`, `.kube/`, `kubeconfig*`, `*.key`, `*.crt`

5. Parse tasks.md structure and extract:
   - **Task phases**: Setup, Tests, Core, Integration, Polish
   - **Task dependencies**: Sequential vs parallel execution rules
   - **Task details**: ID, description, file paths, parallel markers [P]
   - **Execution flow**: Order and dependency requirements

6. **MANDATORY WORKFLOW: Execute implementation with strict lane enforcement**:

   **BEFORE ANY CODE WRITING**:
   - **STOP**: Check that selected task (from step 2) is in `doing` lane
   - **BLOCK**: If no task in `doing`, display:
     ```
     ❌ ERROR: No task in 'doing' lane
     You MUST select and move a task to 'doing' before writing code.
     Run: bash .spec-mix/scripts/move-task.sh WP## planned doing FEATURE_DIR
     ```
   - **PROCEED**: Only when task is confirmed in `doing` lane

   **DURING IMPLEMENTATION**:
   - **Phase-by-phase execution**: Complete each phase before moving to the next
   - **Respect dependencies**: Run sequential tasks in order, parallel tasks [P] can run together
   - **Follow TDD approach**: Execute test tasks before their corresponding implementation tasks
   - **File-based coordination**: Tasks affecting the same files must run sequentially
   - **Validation checkpoints**: Verify each phase completion before proceeding

7. Implementation execution rules:
   - **Setup first**: Initialize project structure, dependencies, configuration
   - **Tests before code**: If you need to write tests for contracts, entities, and integration scenarios
   - **Core development**: Implement models, services, CLI commands, endpoints
   - **Integration work**: Database connections, middleware, logging, external services
   - **Polish and validation**: Unit tests, performance optimization, documentation

8. Progress tracking and error handling:
   - Report progress after each completed task
   - Halt execution if any non-parallel task fails
   - For parallel tasks [P], continue with successful tasks, report failed ones
   - Provide clear error messages with context for debugging
   - Suggest next steps if implementation cannot proceed
   - **IMPORTANT: Task Status Management (Hybrid Approach)**:

     **Auto-Detection**: The system automatically selects the appropriate method based on project structure:

     **Option 1 - Work Package File System (Most Recommended, uses move-task.sh)**:
     - **Detection**: When `FEATURE_DIR/tasks/` directory contains `planned/`, `doing/`, `for_review/`, `done/` subdirectories with WPxx.md files
     - **Usage**:
       1. **Before starting a task**:
          ```bash
          bash scripts/bash/move-task.sh WP01 planned doing "$FEATURE_DIR"
          ```
       2. **After completing a task** (needs review):
          ```bash
          bash scripts/bash/move-task.sh WP01 doing for_review "$FEATURE_DIR"
          ```
       3. **After review is complete**:
          ```bash
          bash scripts/bash/move-task.sh WP01 for_review done "$FEATURE_DIR"
          ```
     - **Benefits**:
       - Automatically updates Work Package file frontmatter (lane, started_at, completed_at)
       - Automatically appends activity logs
       - Perfect integration with the dashboard
       - Each task managed as independent file, reducing merge conflicts
     - **Note**: FEATURE_DIR is obtained from check-prerequisites.sh output

     **Option 2 - tasks.md Section-based (When Work Package files don't exist)**:
     - **Detection**: When tasks.md contains status sections (## Planned, ## Doing, ## For Review, ## Done)
     - **Usage**:
       1. **Before starting a task**: Move task from `## Planned` to `## Doing` section
       2. **After completing a task**: Move task from `## Doing` to `## Done` section
       3. **If task needs review**: Move task from `## Doing` to `## For Review` section
     - Format: Cut the entire task entry (### WP-XXX: Title + description) and paste into target section
     - This makes task status visible in the dashboard kanban board

     **Option 3 - Checkbox-based (Simplest, when sections don't exist)**:
     - **Detection**: When tasks.md uses checkbox format only without sections
     - **Usage**:
       1. **Before starting**: Change `- [ ] TXXX` to `- [ ] TXXX (In Progress)`
       2. **After completing**: Change `- [ ] TXXX` to `- [x] TXXX`

     **Creating Sections (if you want Option 2 but sections are missing)**:
     - If tasks.md doesn't have status sections but you want dashboard support, add them:
       ```markdown
       ## Planned
       [Move upcoming tasks here]

       ## Doing
       [Move tasks you're currently working on here]

       ## For Review
       [Move tasks awaiting review here]

       ## Done
       [Move completed tasks here]
       ```
     - Then move all task headers (### WP-XXX or ### TXXX) into appropriate sections

   - **MANDATORY Git Commit Rules**:

     **ENFORCEMENT**: ALL commits MUST follow these rules - NO EXCEPTIONS:

     1. **BEFORE COMMITTING - Verify task in doing**:
        ```bash
        # Check task is in doing lane
        ls FEATURE_DIR/tasks/doing/WP*.md
        # If empty: STOP - Move task to doing first
        ```

     2. **COMMIT MESSAGE FORMAT - REQUIRED**:
        ```bash
        git commit -m "[WP##] Brief description of changes

        - Detailed change 1
        - Detailed change 2

        Task: WP## - [Task Title]
        Lane: doing -> for_review (after this commit)"
        ```

     3. **VALIDATION BEFORE COMMIT**:
        - **CHECK**: Task WP## exists in `doing/` lane
        - **CHECK**: Commit message includes [WP##]
        - **BLOCK**: If either check fails:
          ```
          ❌ COMMIT BLOCKED: Missing requirements
          - Task must be in 'doing' lane
          - Commit message must include [WP##]
          ```

     4. **AFTER COMMIT - Auto-move to review**:
        ```bash
        # After successful commit, IMMEDIATELY move task
        bash .spec-mix/scripts/move-task.sh WP## doing for_review FEATURE_DIR
        echo "✓ Task WP## moved to review - ready for /spec-mix.review"
        ```

     **Examples**:
     ```bash
     # Good commit messages (task ID in brackets)
     git commit -m "[WP01.1] Add HttpMethod enum to models

     - Created src/models/enums.py with HttpMethod class
     - Added GET, POST, PUT, DELETE, PATCH methods
     - Included docstrings and type hints"

     git commit -m "[WP02.3] Implement user authentication middleware

     - Added JWT token validation
     - Created auth middleware in src/middleware/auth.py
     - Integrated with existing user model"

     git commit -m "[T005] Fix bug in login validation

     - Fixed null pointer in email validation
     - Added error handling for malformed emails"
     ```

     **Why this matters**:
     - The `move-task.sh` script automatically detects commits matching `[TASK_ID]` pattern
     - Commits are appended to the Work Package Activity Log
     - Dashboard displays git history per task
     - Creates automatic audit trail of code changes

     **What gets tracked automatically**:
     - Commit hash, message, timestamp, and author
     - List of files modified in each commit
     - Timeline of changes for each task

     **Best practices**:
     - Make frequent, small commits (easier to review and revert)
     - Always include task ID at the start: `[WP01]`, `[WP01.1]`, `[T005]`
     - Write clear, descriptive commit messages
     - Commit after completing each logical unit of work
     - Group related changes in a single commit

9. **MANDATORY Task Completion Workflow**:

   **ENFORCEMENT**: Task completion MUST follow this workflow:

   a. **Verify task completion**:
      - All code changes committed with [WP##] reference
      - Tests written and passing
      - Documentation updated

   b. **REQUIRED: Move task to review**:
      ```bash
      # MUST move completed task to review
      bash .spec-mix/scripts/move-task.sh WP## doing for_review FEATURE_DIR
      ```
      - **BLOCK** further work if task not moved
      - Display: "✓ WP## ready for review - use /spec-mix.review"

   c. **Lane status after completion**:
      ```
      Final Lane Status:
      ├─ planned:     [remaining tasks]
      ├─ doing:       [should be 0 - all moved to review]
      ├─ for_review:  [completed tasks awaiting review]
      └─ done:        [reviewed and approved tasks]
      ```

   d. **Next steps reminder**:
      ```
      ✓ Implementation phase complete for WP##

      REQUIRED NEXT STEPS:
      1. Run /spec-mix.review to review completed work
      2. After review, run /spec-mix.accept for acceptance
      3. Tasks will move to 'done' after acceptance

      ⚠️ DO NOT start new tasks until review is complete
      ```

10. **Workflow Summary**:

    The ENFORCED workflow for EVERY task:
    ```
    planned → doing → for_review → done
      ↓         ↓         ↓          ↓
    SELECT   IMPLEMENT  REVIEW    ACCEPTED
    ```

    **NO SHORTCUTS ALLOWED**:
    - Cannot skip lanes
    - Cannot commit without task in doing
    - Cannot leave completed tasks in doing
    - Must follow the complete workflow

Note: This command ENFORCES the complete lane workflow. Tasks MUST be in 'doing' before implementation and MUST be moved to 'for_review' after completion.

## Walkthrough Generation (Automatic)

After completing implementation tasks, automatically generate a walkthrough document that serves as both a work proof and session memory:

### Create Walkthrough Document

**Location**: `specs/{feature}/walkthrough.md`

Generate a comprehensive walkthrough using the following structure:

```markdown
# Implementation Walkthrough: {feature}

**Generated**: {timestamp}
**Session ID**: {unique-session-id}

## Summary

Brief overview of what was implemented in this session.

## Work Completed

### Tasks Implemented
- WP## - {task description}: {status}
- List all tasks worked on during this session

### Files Modified
```
{output of git diff --name-status}
```

### Key Changes

#### {Component/Module Name}
- **File**: {file path}
- **Changes**: {description of changes}
- **Rationale**: {why this approach was chosen}

{Repeat for each major component modified}

## Testing & Verification

### Tests Run
```bash
{test command and output}
```

### Manual Verification
- [ ] Feature tested in development environment
- [ ] Edge cases handled
- [ ] Error scenarios tested

## Architecture Decisions

Document any important technical decisions made:
- Why certain patterns were chosen
- Trade-offs considered
- Alternative approaches rejected and why

## Known Issues & TODOs

- [ ] Any remaining issues discovered during implementation
- [ ] Future improvements identified
- [ ] Technical debt incurred

## Commit History

```bash
git log --oneline --graph --decorate --since="{session-start}"
```

## Next Steps

What should be done next:
1. Review tasks in for_review lane
2. Any follow-up work identified
3. Documentation updates needed

---
*This walkthrough serves as a record of work completed and decisions made during this implementation session.*
```

### Auto-save and Reference

After generating the walkthrough:
1. Save to `specs/{feature}/walkthrough.md`
2. Display message: "✓ Walkthrough generated: specs/{feature}/walkthrough.md"
3. This file will be automatically loaded by AI agents on next session (via agent configuration)

