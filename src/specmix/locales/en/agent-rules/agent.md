# agent.md

This file provides guidance to AI coding assistants when working with code in this repository.

## Project Configuration

This project uses Spec-Driven Development (SDD) with the spec-mix toolkit.

## Walkthrough Memory Loading

**CRITICAL**: At the start of each session, you MUST check for and load existing walkthrough documents to maintain context:

```bash
# Check for walkthrough documents
find specs -name "walkthrough.md" -type f
```

### Loading Priority

1. **Immediate action**: Search for `walkthrough.md` files in `specs/` directory
2. **Context loading**: Read all walkthroughs to understand previous work
3. **Decision continuity**: Apply same patterns and decisions from previous sessions

### Information in Walkthroughs

Each walkthrough contains critical session memory:

- Implementation summary
- Modified files with explanations
- Technical decisions and rationale
- Test results and verification status
- Outstanding issues and future work
- Git commit history

## Spec-Driven Development Workflow

Follow this structured approach for all features:

1. **Setup Phase**:
   - `/spec-mix.constitution` - Define project principles
   - `/spec-mix.specify` - Create feature specification

2. **Planning Phase**:
   - `/spec-mix.clarify` - Resolve ambiguities
   - `/spec-mix.plan` - Technical implementation plan
   - `/spec-mix.tasks` - Detailed task breakdown

3. **Implementation Phase**:
   - `/spec-mix.analyze` - Cross-check artifacts
   - `/spec-mix.implement` - Execute tasks (auto-creates walkthrough)

4. **Review Phase**:
   - `/spec-mix.review` - Review completed work
   - `/spec-mix.accept` - Acceptance verification
   - `/spec-mix.merge` - Integration to main

## Essential Practices

### Session Start Protocol

1. Search for existing walkthroughs: `ls specs/*/walkthrough.md`
2. Load and review previous decisions
3. Check task lane status: `ls specs/*/tasks/*/`
4. Continue from last known state

### During Implementation

- Tasks must be in `doing` lane before work starts
- Include Work Package ID in commits: `[WP01] Description`
- Move tasks through lanes: planned → doing → for_review → done
- Walkthrough automatically generated after implementation

### Session Continuity

- Walkthroughs preserve context between sessions
- Technical decisions should be consistent
- Architecture patterns should be maintained
- Test strategies should be continued

## Project Structure

```text
project/
├── specs/                      # Feature specifications
│   └── {feature}/
│       ├── spec.md            # Feature specification
│       ├── plan.md            # Technical plan
│       ├── tasks.md           # Task breakdown
│       ├── walkthrough.md     # AUTO-GENERATED session record
│       └── tasks/             # Task lane management
│           ├── planned/
│           ├── doing/
│           ├── for_review/
│           └── done/
├── .spec-mix/                 # Toolkit files
│   └── scripts/               # Automation scripts
└── .github/                   # GitHub-specific (Copilot)
    └── commands/              # Slash commands

```

## Command Reference

- Initialize: `specify init <project-name>`
- Check environment: `specify check`
- Language settings: `specify lang`
- Mission management: `specify mission`
- Web dashboard: `specify dashboard`

## Critical Reminders

⚠️ **ALWAYS** check for walkthroughs at session start
⚠️ **NEVER** skip the lane workflow
⚠️ **ALWAYS** reference Work Package IDs in commits
⚠️ Walkthroughs are auto-generated - do not create manually

## Integration Notes

- This file works with GitHub Copilot, Codex CLI, and similar agents
- Commands may vary slightly based on your AI assistant
- Core workflow remains consistent across all agents
