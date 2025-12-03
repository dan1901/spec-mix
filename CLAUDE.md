# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Spec Kit** is an open-source toolkit for Spec-Driven Development (SDD), a structured approach where specifications become executable and drive implementation. The toolkit includes:

- **specify CLI**: Python-based CLI tool that bootstraps SDD projects for various AI assistants
- **Templates**: Specification, plan, and task templates for structured development
- **Scripts**: Bash/PowerShell automation scripts that manage feature branches and documentation
- **Slash Commands**: AI agent commands (`/spec-mix.*`) that guide the SDD workflow

## Development Commands

### Running the CLI Locally

```bash
# Install dependencies
uv sync

# Run the CLI
uv run specify --help
uv run specify init <project-name>
uv run specify check

# Install globally for development
uv tool install --editable .
```

### Testing Template Changes Locally

The normal `uv run specify init` pulls **released packages** from GitHub, which won't include your local changes. To test template/command changes:

```bash
# 1. Generate local release packages
./.github/workflows/scripts/create-release-packages.sh v1.0.0

# 2. Copy relevant package to test project
cp -r .genreleases/sdd-copilot-package-sh/. <path-to-test-project>/

# 3. Test in your AI agent
cd <path-to-test-project>
claude  # or your chosen AI agent
```

### Running Tests

```bash
# Run any Python tests (if applicable)
uv run pytest

# Test CLI functionality manually with sample projects
uv run specify init test-project --ai claude
cd test-project
# Verify slash commands work in your AI agent
```

## Repository Structure

```text
spec-kit/
├── src/specmix/
│   ├── __init__.py                # Main CLI implementation (Python)
│   ├── i18n.py                    # Internationalization core module
│   ├── lang_command.py            # Language management commands
│   ├── mission.py                 # Mission system core
│   ├── mission_command.py         # Mission management commands
│   ├── mode.py                    # Mode system core (Normal/Pro modes)
│   ├── mode_command.py            # Mode management commands
│   ├── dashboard.py               # Dashboard HTTP server
│   ├── dashboard_command.py       # Dashboard CLI commands
│   └── static/dashboard/          # Dashboard frontend files (NEW)
│       ├── index.html
│       ├── dashboard.css
│       └── dashboard.js
├── locales/                        # Multi-language support (NEW)
│   ├── config.json                # Language configuration
│   ├── en/                        # English (default)
│   │   ├── strings.json           # CLI messages
│   │   ├── commands/              # Command instructions
│   │   ├── templates/             # Document templates
│   │   └── missions/              # Mission-specific content (NEW)
│   │       ├── software-dev/      # Software development mission
│   │       │   ├── mission.yaml
│   │       │   ├── templates/
│   │       │   ├── commands/
│   │       │   └── constitution/
│   │       └── research/          # Research mission
│   │           ├── mission.yaml
│   │           ├── templates/
│   │           ├── commands/
│   │           └── constitution/
│   └── ko/                        # Korean (full translation)
│       ├── strings.json
│       ├── commands/
│       ├── templates/
│       └── missions/              # Localized missions
├── templates/                      # Legacy templates (links to locales/en)
│   ├── spec-template.md           # Feature specification template
│   ├── plan-template.md           # Implementation plan template
│   ├── tasks-template.md          # Task breakdown template
│   ├── checklist-template.md      # Quality checklist template
│   ├── commands/                  # Slash command definitions
│   │   ├── specify.md             # /spec-mix.specify workflow
│   │   ├── plan.md                # /spec-mix.plan workflow
│   │   ├── tasks.md               # /spec-mix.tasks workflow
│   │   ├── implement.md           # /spec-mix.implement workflow
│   │   ├── constitution.md        # /spec-mix.constitution workflow
│   │   ├── clarify.md             # /spec-mix.clarify workflow
│   │   ├── analyze.md             # /spec-mix.analyze workflow
│   │   ├── checklist.md           # /spec-mix.checklist workflow
│   │   ├── review.md              # /spec-mix.review workflow (NEW)
│   │   ├── accept.md              # /spec-mix.accept workflow (NEW)
│   │   ├── merge.md               # /spec-mix.merge workflow (NEW)
│   │   └── dashboard.md           # /spec-mix.dashboard workflow (NEW)
│   └── vscode-settings.json       # VS Code settings for projects
├── scripts/                        # Script templates (not directly executed)
│   ├── bash/                      # POSIX shell scripts
│   │   ├── common.sh              # Shared utilities (repo root, branch detection)
│   │   ├── create-new-feature.sh  # Feature branch creation
│   │   ├── setup-plan.sh          # Plan directory setup
│   │   ├── check-prerequisites.sh # Prerequisite validation
│   │   ├── update-agent-context.sh # Agent context file updates
│   │   ├── setup-worktree.sh      # Git worktree management (NEW)
│   │   ├── move-task.sh           # Task lane movement (NEW)
│   │   ├── merge-feature.sh       # Feature branch merging (NEW)
│   │   └── create-fix.sh          # Lightweight bug fix creation (NEW)
│   └── powershell/                # PowerShell equivalents
├── memory/                         # Project memory/constitution examples
├── docs/                           # Documentation site files
│   └── i18n.md                    # Internationalization guide
├── pyproject.toml                  # Python package configuration
└── README.md                       # Main documentation
```

## Architecture

### CLI Tool (`src/specmix/__init__.py`)

The CLI is a single-file Python application using:

- **typer**: CLI framework
- **rich**: Terminal UI (progress bars, panels, trees)
- **httpx**: HTTP client for GitHub API
- **readchar**: Cross-platform keyboard input

**Key workflows:**

1. `specify init`: Downloads latest release template from GitHub, extracts to project directory
2. `specify check`: Validates installed tools (git, AI agents)

**Template Download Flow:**

- Fetches latest release via GitHub API (`/repos/github/spec-kit/releases/latest`)
- Selects appropriate ZIP asset based on AI agent (`claude`, `copilot`, etc.) and script type (`sh`, `ps`)
- Extracts to target directory with special handling for:
  - `.vscode/settings.json`: Deep merge instead of overwrite
  - Nested directory flattening
  - Execute permissions on `.sh` scripts (Unix only)

### Script Architecture (`scripts/bash/`)

Scripts are **templates** deployed to user projects under `.spec-mix/scripts/`. They are executed by AI agents during the SDD workflow.

**Common Functions (`common.sh`):**

- `get_repo_root()`: Find repository root (supports non-Git repos)
- `get_current_branch()`: Get current branch with fallback to `SPECIFY_FEATURE` env var or latest feature directory
- `check_feature_branch()`: Validate feature branch naming (`001-feature-name`)
- `find_feature_dir_by_prefix()`: Find spec directory by numeric prefix

**Feature Branch Workflow (`create-new-feature.sh`):**

- Checks all sources (local branches, remote branches, spec directories) for existing numbering
- Generates next available branch number
- Creates branch and spec directory
- Supports `--short-name` and `--number` overrides

**Important Git Fallbacks:**

- All scripts support non-Git repositories
- Use `SPECIFY_FEATURE` environment variable to manually specify feature directory
- Fall back to detecting latest numbered directory in `specs/`

### Slash Command System

Slash commands are markdown files in `templates/commands/` that contain detailed instructions for AI agents. When users run `/spec-mix.specify`, the AI agent:

1. Reads the command file
2. Executes embedded bash scripts (e.g., `create-new-feature.sh`)
3. Follows the structured workflow to generate specifications

**Command Dependencies:**

1. `/spec-mix.constitution` → Establish project principles (optional but recommended)
2. `/spec-mix.specify` → Create feature specification
3. `/spec-mix.clarify` → Clarify ambiguities (optional, before plan)
4. `/spec-mix.plan` → Create technical plan
5. `/spec-mix.tasks` → Generate task breakdown
6. `/spec-mix.analyze` → Cross-artifact analysis (optional, before implement)
7. `/spec-mix.implement` → Execute implementation

**Standalone Commands:**

- `/spec-mix.fix` → Create lightweight bug fix (can be run anytime from feature branch or main)

## Key Design Principles

### Template System

- Templates use placeholder patterns like `[FEATURE NAME]`, `[###-feature-name]`
- AI agents fill in placeholders during workflow execution
- Templates enforce structure while allowing flexibility

### Branch Numbering

- Feature branches: `001-feature-name`, `002-another-feature`
- Multiple branches can share same number (e.g., `004-fix-bug`, `004-add-feature`)
- Numbering checked across local branches, remote branches, AND spec directories
- Prevents numbering conflicts in collaborative environments

### Agent Agnosticism

Supports 8 AI assistants:

| Agent | Key | Folder | Type |
|-------|-----|--------|------|
| Claude Code | `claude` | `.claude/` | CLI |
| GitHub Copilot | `copilot` | `.github/` | IDE |
| Gemini CLI | `gemini` | `.gemini/` | CLI |
| Cursor | `cursor-agent` | `.cursor/` | IDE |
| Kiro | `kiro` | `.kiro/` | IDE |
| Windsurf | `windsurf` | `.windsurf/` | IDE |
| Google Antigravity | `antigravity` | `.agent/` | CLI |
| Codex CLI | `codex` | `.codex/` | CLI |

- Each agent has specific folder and script type (sh/ps)
- CLI checks for agent availability but can skip with `--ignore-agent-tools`

### Non-Git Repository Support

- All critical functionality works without Git
- Use `SPECIFY_FEATURE` environment variable for feature selection
- Scripts fall back to directory-based feature detection

### Multi-Language Support (i18n)

- **Hybrid architecture**: English bundled, additional languages installable
- **Automatic detection**: Uses system locale or `SPECIFY_LANG` environment variable
- **Complete translation**: CLI messages, commands, and templates all localized
- **Graceful fallback**: Missing translations fall back to English automatically

**Supported Languages:**

- English (`en`): Default, always available
- Korean (`ko`): Full translation (CLI + commands + templates)

**Language Management:**

```bash
specify lang list     # List available languages
specify lang current  # Show current language
specify lang set ko   # Set default language
```

**For detailed i18n documentation, see `docs/i18n.md`**

### Task Lane System and Worktree Management (NEW)

The project now includes advanced workflow management features integrated from spec-kitty:

**Task Lanes (Kanban-style workflow):**

- Tasks are organized in `specs/{feature}/tasks/` with four lanes:
  - `planned/`: Tasks waiting to be started
  - `doing/`: Tasks currently in progress
  - `for_review/`: Tasks completed and awaiting review
  - `done/`: Tasks reviewed and approved
- Each task is a Work Package file (WPxx.md) with frontmatter metadata
- Use `scripts/bash/move-task.sh` to move tasks between lanes

**Git Worktree Support:**

- Feature isolation without branch switching using git worktrees
- Worktrees created in `.worktrees/{feature-name}/`
- Use `scripts/bash/setup-worktree.sh` to create/cleanup worktrees
- Allows working on multiple features simultaneously

**Workflow Commands:**

- `/spec-mix.review`: Review completed tasks in `for_review` lane
- `/spec-mix.accept`: Final acceptance check before merge (generates acceptance.md)
- `/spec-mix.merge`: Merge feature to main with multiple strategies (merge/squash/ff-only)

**Script Reference:**

```bash
# Create worktree
scripts/bash/setup-worktree.sh --feature 001-user-auth

# Move task between lanes
scripts/bash/move-task.sh WP01 planned doing specs/001-user-auth

# Merge with options
scripts/bash/merge-feature.sh --feature 001-user-auth --strategy squash --push

# Create lightweight bug fix
scripts/bash/create-fix.sh --json "bug description here"
```

### Mode System (Normal/Pro)

Two operational modes for different user needs:

**Normal Mode** (default):

- Guided workflow with auto-clarify
- `/spec-mix.specify`: Creates spec → auto-runs clarify questions → user chooses Answer or SKIP
- `/spec-mix.plan`: Generates checklist + plan + phase-based tasks
- `/spec-mix.implement`: Phase-by-phase execution with walkthrough/review/accept
- Simplified for beginners and streamlined workflows

**Pro Mode**:

- Full control with individual commands
- All commands available: constitution, specify, clarify, plan, tasks, implement, analyze, checklist, review, accept, merge, dashboard
- Advanced features for experienced users

**Mode Management:**

```bash
# List available modes
specify mode list

# Show current mode
specify mode current

# Switch mode
specify mode set normal
specify mode set pro

# View mode details
specify mode info normal
```

**Dashboard Mode Support:**

- Displays mode badge on feature cards (Normal/Pro)
- Phase-based kanban board for Normal mode
- Walkthrough file badges for phase completions

### Mission System and Dashboard

This fork includes advanced features from spec-kitty integration:

**Mission System:**

- Domain-specific workflows (software-dev, research)
- Mission-specific templates, commands, and validation
- Multilingual mission support
- Configuration via `mission.yaml`

```bash
# List missions
specify mission list

# Switch mission
specify mission switch research

# View mission details
specify mission info software-dev
```

**Web Dashboard:**

- Real-time feature monitoring
- Interactive kanban boards
- Artifact viewer with markdown rendering
- Auto-refresh (2s intervals)
- Multilingual UI

```bash
# Start dashboard
specify dashboard

# On custom port
specify dashboard start --port 9000

# Stop dashboard
specify dashboard stop
```

**Dashboard Architecture:**

- Backend: Python built-in `http.server` (`src/specmix/dashboard.py`)
- Frontend: Vanilla JS + marked.js (`src/specmix/static/dashboard/`)
- Default port: 9237
- Access: localhost only (security)
- State files: `.spec-mix/dashboard.{pid,port,token}`

## Common Development Patterns

### Adding a New AI Agent

1. Update `AGENT_CONFIG` in `src/specmix/__init__.py`:

```python
"newagent": {
    "name": "New Agent Name",
    "folder": ".newagent/",
    "install_url": "https://example.com/install",
    "requires_cli": True,  # or False for IDE-based
}
```

1. Create agent-specific templates (if needed) under `templates/`

2. Test with `uv run specify init test-project --ai newagent`

### Modifying Templates

Templates are in `templates/`. Changes affect **future releases** only unless you test locally (see Testing Template Changes above).

**Template Types:**

- `spec-template.md`: User stories, requirements, success criteria
- `plan-template.md`: Technical context, architecture, implementation phases
- `tasks-template.md`: Detailed task breakdown with dependencies
- `commands/*.md`: AI agent workflow instructions

### Working with Scripts

Scripts in `scripts/bash/` and `scripts/powershell/` are **source templates**. They get copied to user projects during `specify init`.

**Testing Script Changes:**

1. Edit script in `scripts/bash/`
2. Generate local release package (see Testing Template Changes)
3. Copy to test project
4. Execute in AI agent environment

### Adding or Modifying Translations

All translations are in `locales/`. Each language has the same structure:

```text
locales/{lang_code}/
├── strings.json      # CLI messages
├── commands/         # Command instructions (8 files)
└── templates/        # Document templates (5 files)
```

**To add a new language:**

1. Create `locales/{lang_code}/` directory
2. Add language entry to `locales/config.json`
3. Copy and translate `strings.json` from `locales/en/`
4. Copy and translate all files in `commands/` and `templates/`
5. Test with `SPECIFY_LANG={lang_code} uv run specify init test-project`

**To update existing translations:**

1. Edit files in `locales/{lang_code}/`
2. Ensure placeholder syntax (`[PLACEHOLDER]`, `{variable}`) is preserved
3. Test the full workflow in that language

**Translation Guidelines:**

- Preserve all markdown formatting
- Keep placeholder tokens unchanged (e.g., `[FEATURE NAME]`, `{ARGS}`)
- Maintain technical terms in English when appropriate
- Test with actual workflow execution

See `docs/i18n.md` for complete translation guide.

### Release Process

Releases are automated via GitHub Actions (`.github/workflows/release.yml`):

1. Creates ZIP packages for each AI agent + script type combination
2. Publishes to GitHub Releases
3. CLI downloads these ZIPs during `specify init`

## Important Notes

### JSON Merging for `.vscode/settings.json`

When initializing in existing directories (`--here` flag), the CLI performs **deep merge** of `.vscode/settings.json` instead of overwriting. This preserves user settings while adding Spec Kit recommendations.

### Script Permissions

On Unix systems, the CLI automatically sets execute permissions (`chmod +x`) on all `.sh` files under `.spec-mix/scripts/` recursively after extraction.

### Git Credential Management

Users on Linux may need Git Credential Manager. See troubleshooting section in README.md.

### Security Notice

Agent folders (`.claude/`, `.github/`, etc.) may contain credentials. Users should add them to `.gitignore` to prevent leakage.

## Testing Checklist

Before submitting PRs:

- [ ] Test CLI commands with `uv run specify init` and `uv run specify check`
- [ ] Verify template changes by generating local release package
- [ ] Test with at least one AI agent (Claude Code recommended)
- [ ] Ensure bash scripts work on Unix and PowerShell scripts work on Windows
- [ ] Run through full SDD workflow: constitution → specify → plan → tasks → implement
- [ ] Check non-Git repository support if modifying scripts
- [ ] Update README.md or spec-driven.md if user-facing changes
- [ ] **If modifying i18n**: Test with `SPECIFY_LANG=ko` and verify translations display correctly
- [ ] **If adding new language**: Verify all CLI messages, commands, and templates are translated
