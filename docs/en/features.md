# Spec Mix Enhanced Features

Spec Mix extends the original Spec Kit with powerful features for multi-language development, mission-based workflows, and visual project management.

## Overview

This fork adds four major feature sets:

1. **Mode System** - Normal/Pro workflow modes
2. **Multi-Language Support (i18n)** - Full internationalization support
3. **Mission System** - Domain-specific workflow templates
4. **Web Dashboard** - Visual project management interface

## Mode System

Spec Mix offers two operational modes to match different user needs and experience levels.

### Normal Mode (Default)

Guided workflow with streamlined commands:

- **Auto-clarify**: `/spec-mix.specify` creates spec then automatically presents clarification questions
- **User choice**: Answer questions to refine spec OR skip to next step
- **Phase-based tasks**: `/spec-mix.plan` generates checklist + plan + phase-level tasks (not detailed sub-tasks)
- **Guided implementation**: `/spec-mix.implement` executes phase by phase with walkthrough and review
- **Accept workflow**: After each phase, user gets Accept/Reject choice (not a command)

**Normal Mode Workflow:**

```text
/spec-mix.specify "Feature description"
    ↓
Spec created → Auto-clarify questions
    ↓
[Answer questions] or [SKIP → Next Step]
    ↓
/spec-mix.plan
    ↓
Checklist + Plan + Phase-based Tasks
    ↓
/spec-mix.implement
    ↓
Phase 1 → Walkthrough → Review → [ACCEPT/REJECT]
    ↓
Phase 2 → Walkthrough → Review → [ACCEPT/REJECT]
    ↓
... all phases complete ...
    ↓
"Run /spec-mix.merge to finalize"
```

### Pro Mode

Full control with all individual commands:

- All commands available: constitution, specify, clarify, plan, tasks, implement, analyze, checklist, review, accept, merge, dashboard
- Fine-grained control over each workflow step
- Work Package based task management (kanban lanes)
- Recommended for experienced users

### Mode Commands

```bash
# List available modes
spec-mix mode list

# Check current mode
spec-mix mode current

# Switch mode
spec-mix mode set normal
spec-mix mode set pro

# View mode details
spec-mix mode info normal

# Initialize project with specific mode
spec-mix init my-project --mode pro
```

### Dashboard Mode Support

The dashboard adapts to the current mode:

- **Normal Mode**: Shows phase-based kanban board with phase progress
- **Pro Mode**: Shows traditional Work Package kanban with lane management
- Mode badges displayed on feature cards

## Multi-Language Support (i18n)

Full documentation available in [Multi-Language Guide](i18n.md)

### Key Features

- **Multiple language packs** - Currently supports English and Korean
- **Locale-specific commands** - Slash commands in your preferred language
- **Mission templates per language** - Localized workflow templates
- **CLI language switching** - Easy language management

### Quick Start

```bash
# List available languages
spec-mix lang list

# Set language
spec-mix lang set ko

# Initialize project with language
spec-mix init my-project --language ko
```

## Mission System

The mission system provides domain-specific workflow templates optimized for different types of projects.

### Available Missions

#### Software Development Mission

Optimized for building software applications with:

- Feature specification templates
- Implementation planning workflows
- Task breakdown structures
- Code review checklists
- Testing guidelines

```bash
spec-mix init my-app --mission software-dev
```

#### Product Strategy Mission

Designed for product planning and strategic documents with:

- Amazon-style 6-Pager templates
- Market size analysis (TAM/SAM/SOM)
- Competitor analysis frameworks
- Customer persona development
- Business model canvas
- GTM strategy planning
- **Automatic web research** with source citation

```bash
spec-mix init my-product --mission product-strategy
```

**Key Commands:**

- `/spec-mix.specify` - Create 6-Pager with guided conversation
- `/spec-mix.analyze` - Deep market/competitor/customer analysis
- `/spec-mix.refine` - Incorporate feedback and update
- `/spec-mix.review` - Stakeholder review preparation

See [6-Pager Guide](6pager.md) for detailed usage.

#### Research Mission

Designed for research projects with:

- Research question templates
- Analysis workflows
- Findings documentation
- Literature review structures
- Data analysis guidelines

```bash
spec-mix init my-research --mission research
```

### Mission Structure

Each mission includes:

```text
missions/[mission-name]/
├── commands/           # Mission-specific slash commands
│   ├── constitution.md
│   ├── specify.md
│   ├── plan.md
│   └── ...
├── templates/         # Document templates
│   ├── spec-template.md
│   ├── plan-template.md
│   └── ...
└── constitution/      # Mission guidelines
    └── constitution-template.md
```

### Switching Missions

You can switch missions in an existing project:

```bash
spec-mix mission list              # List available missions
spec-mix mission set research      # Switch to research mission
```

## Web Dashboard

The dashboard provides a visual interface for managing your Spec-Driven Development workflow.

### Features

- **Feature Overview** - Visual list of all features in `specs/`
- **Status Tracking** - See feature progress at a glance
- **Document Preview** - Read specifications, plans, and tasks
- **Markdown Rendering** - Beautiful formatted documentation
- **Real-time Updates** - Auto-refresh when files change

### Starting the Dashboard

```bash
# Start dashboard (default port 8080)
spec-mix dashboard

# Custom port
spec-mix dashboard --port 3000

# Custom host
spec-mix dashboard --host 0.0.0.0 --port 8080
```

### Dashboard Views

#### Features List

Shows all features with:

- Feature number and name
- Current status (from `spec.md`)
- Quick links to specification, plan, and tasks
- Color-coded status indicators

#### Document Viewer

View any specification document:

- Full markdown rendering
- Syntax highlighting for code blocks
- Table of contents navigation
- Responsive design

### Stopping the Dashboard

```bash
# Press Ctrl+C in the terminal
# Or use the shutdown command
spec-mix dashboard --shutdown
```

## Combining Features

All features work together seamlessly:

```bash
# Initialize a Korean research project with dashboard
spec-mix init my-korean-research \
  --language ko \
  --mission research

cd my-korean-research

# Start working with Korean commands
# (In your AI agent)
/spec-mix.specify 연구 질문: 딥러닝 모델의 설명가능성

# View progress in dashboard
spec-mix dashboard
```

## Configuration

### Language Configuration

Language settings are stored in `src/specmix/locales/config.json`:

```json
{
  "default_locale": "en",
  "supported_locales": [
    {
      "code": "en",
      "name": "English",
      "native_name": "English",
      "is_default": true
    },
    {
      "code": "ko",
      "name": "Korean",
      "native_name": "한국어"
    }
  ],
  "fallback_locale": "en"
}
```

### Mission Configuration

Missions are auto-detected from the `src/specmix/locales/[lang]/missions/` directory.

## Adding Your Own

### Adding a New Language

1. Create locale directory structure:

   ```bash
   mkdir -p src/specmix/locales/[lang-code]/missions/software-dev
   mkdir -p src/specmix/locales/[lang-code]/missions/research
   ```

2. Add locale to `config.json`

3. Translate command files and templates

4. Test with `spec-mix lang list`

See [Multi-Language Guide](i18n.md) for detailed instructions.

### Adding a New Mission

1. Create mission directory:

   ```bash
   mkdir -p src/specmix/locales/en/missions/[mission-name]
   ```

2. Add required structure:

   ```text
   [mission-name]/
   ├── commands/
   ├── templates/
   └── constitution/
   ```

3. Copy and customize templates from existing missions

4. Test with `spec-mix mission list`

## Best Practices

### Language Selection

- Choose your team's primary language for better collaboration
- English is recommended for open-source projects
- Use language-specific terminology appropriately

### Mission Selection

- **Software Development** - For apps, services, libraries, tools
- **Product Strategy** - For product planning, 6-Pagers, market analysis
- **Research** - For studies, analyses, experiments, papers
- Custom missions - For specialized workflows

### Dashboard Usage

- Keep it running during active development
- Use it for stakeholder demos
- Review feature status before standups
- Share the URL with team members (when using `--host 0.0.0.0`)

## Troubleshooting

### Language not appearing

```bash
# Check if locale files exist
ls src/specmix/locales/

# Verify config.json
cat src/specmix/locales/config.json
```

### Mission commands not working

```bash
# Check mission structure
ls src/specmix/locales/en/missions/[mission-name]/commands/

# Verify current mission
spec-mix mission list
```

### Dashboard not starting

```bash
# Check port availability
lsof -i :8080

# Try different port
spec-mix dashboard --port 8081

# Check for errors
spec-mix dashboard --verbose
```

## Next Steps

- [6-Pager Guide](6pager.md) - Create strategic documents with web research
- [Multi-Language Guide](i18n.md) - Deep dive into i18n features
- [Quick Start](quickstart.md) - Get started with Spec Mix
- [Installation](installation.md) - Installation options
