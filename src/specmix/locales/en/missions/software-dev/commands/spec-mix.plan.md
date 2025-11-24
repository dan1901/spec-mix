---
description: Execute the implementation planning workflow using the plan template to generate design artifacts.
scripts:
  sh: scripts/bash/setup-plan.sh --json
  ps: scripts/powershell/setup-plan.ps1 -Json
agent_scripts:
  sh: scripts/bash/update-agent-context.sh __AGENT__
  ps: scripts/powershell/update-agent-context.ps1 -AgentType __AGENT__
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

If the mode is `normal`, follow this integrated planning workflow that combines checklist, plan, and phase-based tasks:

## Step 1: Setup (Same as Pro Mode)

Run `{SCRIPT}` from repo root and parse JSON for FEATURE_SPEC, IMPL_PLAN, SPECS_DIR, BRANCH.

## Step 2: Generate Quality Checklist

Before planning, create a quality checklist at `FEATURE_DIR/checklists/requirements.md`:

1. Analyze the specification for quality validation
2. Generate checklist items covering:
   - Content Quality (no implementation details, user-focused)
   - Requirement Completeness (testable, measurable)
   - Feature Readiness (acceptance criteria defined)
   - Constitution Compliance (if exists)

3. Save the checklist file

## Step 3: Create Implementation Plan

Execute the standard planning workflow:
1. Fill Technical Context
2. Generate research.md (Phase 0)
3. Generate data-model.md, contracts/ (Phase 1)
4. Update agent context

## Step 4: Generate Phase-Based Tasks (Normal Mode)

**IMPORTANT**: In Normal Mode, tasks are generated at PHASE LEVEL only, not detailed sub-tasks.

Create `FEATURE_DIR/tasks.md` with this structure:

```markdown
# Tasks: {Feature Name}

## Overview
- **Total Phases**: {count}
- **Mode**: Normal (Phase-based execution)

## Phase 1: {Phase Name}
### Description
{What this phase accomplishes}

### Deliverables
- {List of files/components to be created}

### Acceptance Criteria
- [ ] {Criteria 1}
- [ ] {Criteria 2}

---

## Phase 2: {Phase Name}
### Description
{What this phase accomplishes}

### Deliverables
- {List of files/components to be created}

### Acceptance Criteria
- [ ] {Criteria 1}
- [ ] {Criteria 2}

---

{Continue for all phases}
```

**Phase Generation Rules:**
- Maximum 5 phases per feature
- Each phase should be completable in one session
- Phases are sequential (Phase N depends on Phase N-1)
- Focus on deliverables, not implementation details

## Step 5: Completion Message (Normal Mode)

```markdown
---
## Planning Complete (Normal Mode)

**Generated Artifacts:**
- Checklist: `{FEATURE_DIR}/checklists/requirements.md`
- Plan: `{IMPL_PLAN}`
- Tasks: `{FEATURE_DIR}/tasks.md` ({N} phases)

### Next Step:

Run `/spec-mix.implement` to:
1. Execute each phase sequentially
2. Generate walkthrough after each phase
3. Review and accept completed work
4. Proceed to next phase or finish

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

## Outline

1. **Setup**: Run `{SCRIPT}` from repo root and parse JSON for FEATURE_SPEC, IMPL_PLAN, SPECS_DIR, BRANCH. For single quotes in args like "I'm Groot", use escape syntax: e.g 'I'\''m Groot' (or double-quote if possible: "I'm Groot").

2. **Load context**: Read FEATURE_SPEC and `specs/constitution.md`. Load IMPL_PLAN template (already copied).

3. **Execute plan workflow**: Follow the structure in IMPL_PLAN template to:
   - Fill Technical Context (mark unknowns as "NEEDS CLARIFICATION")
   - Fill Constitution Check section from constitution
   - Evaluate gates (ERROR if violations unjustified)
   - Phase 0: Generate research.md (resolve all NEEDS CLARIFICATION)
   - Phase 1: Generate data-model.md, contracts/, quickstart.md
   - Phase 1: Update agent context by running the agent script
   - Re-evaluate Constitution Check post-design

4. **Stop and report**: Command ends after Phase 2 planning. Report branch, IMPL_PLAN path, and generated artifacts.

## Phases

### Phase 0: Outline & Research

1. **Extract unknowns from Technical Context** above:
   - For each NEEDS CLARIFICATION → research task
   - For each dependency → best practices task
   - For each integration → patterns task

2. **Generate and dispatch research agents**:

   ```text
   For each unknown in Technical Context:
     Task: "Research {unknown} for {feature context}"
   For each technology choice:
     Task: "Find best practices for {tech} in {domain}"
   ```

3. **Consolidate findings** in `research.md` using format:
   - Decision: [what was chosen]
   - Rationale: [why chosen]
   - Alternatives considered: [what else evaluated]

**Output**: research.md with all NEEDS CLARIFICATION resolved

### Phase 1: Design & Contracts

**Prerequisites:** `research.md` complete

1. **Extract entities from feature spec** → `data-model.md`:
   - Entity name, fields, relationships
   - Validation rules from requirements
   - State transitions if applicable

2. **Generate API contracts** from functional requirements:
   - For each user action → endpoint
   - Use standard REST/GraphQL patterns
   - Output OpenAPI/GraphQL schema to `/contracts/`

3. **Agent context update**:
   - Run `{AGENT_SCRIPT}`
   - These scripts detect which AI agent is in use
   - Update the appropriate agent-specific context file
   - Add only new technology from current plan
   - Preserve manual additions between markers

**Output**: data-model.md, /contracts/*, quickstart.md, agent-specific file

## Key rules

- Use absolute paths

- ERROR on gate failures or unresolved clarifications
