# Mission System

The Mission System provides domain-specific workflow templates and commands optimized for different types of projects.

## What are Missions?

Missions are pre-configured workflow templates that adapt Spec-Driven Development to specific domains. Each mission includes:

- **Custom slash commands** - Tailored to the domain
- **Document templates** - Pre-structured specifications and plans
- **Workflow guidelines** - Best practices for the domain
- **Constitution templates** - Domain-specific principles

## Available Missions

### Software Development

**Best for:** Web apps, mobile apps, APIs, libraries, CLI tools, services

**Features:**

- Feature-based specification structure
- Implementation planning with technical details
- Task breakdown for development workflows
- Code review and testing checklists
- Architecture decision templates

**Templates:**

- `spec-template.md` - Feature specifications
- `plan-template.md` - Technical implementation plans
- `tasks-template.md` - Development task lists
- `checklist-template.md` - Quality assurance checklists

**Example Use Case:**

```bash
spec-mix init my-web-app --mission software-dev

# Use software development commands
/spec-mix.specify Add user authentication with OAuth
/spec-mix.plan Use PostgreSQL and JWT tokens
/spec-mix.tasks Break down into backend and frontend work
```

### Product Strategy

**Best for:** Product planning, 6-Pager documents, market analysis, business cases

**Features:**

- Amazon-style 6-Pager strategic documents
- Market size analysis (TAM/SAM/SOM)
- Customer persona development
- Competitive analysis frameworks
- Business model canvas
- GTM strategy planning

**Templates:**

- `6pager-template.md` - 14-section strategic document
- `constitution-template.md` - Product strategy principles

**Commands:**

- `/spec-mix.specify` - Create 6-Pager through guided conversation
- `/spec-mix.analyze` - Deep market/competitor/customer analysis
- `/spec-mix.refine` - Improve document based on feedback
- `/spec-mix.review` - Stakeholder review checklists

**Example Use Case:**

```bash
spec-mix init my-product --mission product-strategy

# Use product strategy commands
/spec-mix.specify AI-powered budgeting app for millennials
/spec-mix.analyze market
/spec-mix.analyze competitor
/spec-mix.refine Update TAM to $10B based on Gartner report
/spec-mix.review stakeholder
```

### Research

**Best for:** Academic research, data analysis, experiments, studies, papers

**Features:**

- Research question formulation
- Literature review structure
- Methodology documentation
- Data analysis workflows
- Findings and conclusions templates

**Templates:**

- `research-question-template.md` - Research question formulation
- `analysis-template.md` - Data analysis documentation
- `findings-template.md` - Results and conclusions

**Example Use Case:**

```bash
spec-mix init ml-explainability-study --mission research

# Use research commands
/spec-mix.specify Research Question: How do attention mechanisms improve model interpretability?
/spec-mix.plan Design controlled experiment with baseline models
/spec-mix.tasks Set up data collection and analysis pipeline
```

## Mission Structure

Each mission is organized in the locales directory:

```text
src/specmix/locales/
└── [language]/
    └── missions/
        └── [mission-name]/
            ├── commands/          # Slash commands
            │   ├── constitution.md
            │   ├── specify.md
            │   ├── plan.md
            │   ├── tasks.md
            │   ├── implement.md
            │   ├── review.md
            │   ├── accept.md
            │   ├── merge.md
            │   ├── clarify.md
            │   ├── analyze.md
            │   ├── checklist.md
            │   └── dashboard.md
            ├── templates/         # Document templates
            │   ├── spec-template.md
            │   ├── plan-template.md
            │   ├── tasks-template.md
            │   └── ...
            └── constitution/      # Guidelines
                └── constitution-template.md
```

## Using Missions

### During Initialization

Specify the mission when creating a new project:

```bash
# Software development (default)
spec-mix init my-app

# Explicitly specify software-dev
spec-mix init my-app --mission software-dev

# Research project
spec-mix init my-study --mission research

# Combine with language
spec-mix init my-korean-research --mission research --language ko
```

### Switching Missions

You can change the mission of an existing project:

```bash
# List available missions
spec-mix mission list

# Switch to a different mission
spec-mix mission set research

# Verify current mission
spec-mix mission current
```

**Note:** Switching missions will update the command files in `.claude/commands/` (or your agent's directory) but won't modify existing specifications.

## Command Differences by Mission

### Software Development Commands

Commands focus on building features:

- **`/spec-mix.specify`** - Describe a feature to build
- **`/spec-mix.plan`** - Create technical implementation plan
- **`/spec-mix.tasks`** - Break down into development tasks
- **`/spec-mix.implement`** - Execute implementation
- **`/spec-mix.review`** - Code review checklist
- **`/spec-mix.accept`** - Acceptance criteria verification

### Product Strategy Commands

Commands focus on strategic planning:

- **`/spec-mix.specify`** - Create 6-Pager strategic document
- **`/spec-mix.analyze`** - Market/competitor/customer analysis
- **`/spec-mix.refine`** - Incorporate feedback and update document
- **`/spec-mix.review`** - Stakeholder review and approval

### Research Commands

Commands focus on research workflow:

- **`/spec-mix.specify`** - Formulate research question
- **`/spec-mix.plan`** - Design methodology
- **`/spec-mix.tasks`** - Plan research activities
- **`/spec-mix.implement`** - Execute research plan
- **`/spec-mix.review`** - Peer review checklist
- **`/spec-mix.accept`** - Validate findings

## Creating Custom Missions

You can create your own missions for specialized workflows.

### Step 1: Create Mission Directory

```bash
# For English
mkdir -p src/specmix/locales/en/missions/my-mission/commands
mkdir -p src/specmix/locales/en/missions/my-mission/templates
mkdir -p src/specmix/locales/en/missions/my-mission/constitution
```

### Step 2: Copy Base Templates

Start with an existing mission as a template:

```bash
# Copy from software-dev as base
cp -r src/specmix/locales/en/missions/software-dev/* \
      src/specmix/locales/en/missions/my-mission/
```

### Step 3: Customize Commands

Edit each command file to match your domain:

```markdown
---
description: Your custom command description
scripts:
  sh: scripts/bash/your-script.sh
  ps: scripts/powershell/your-script.ps1
---

## Your Command Instructions

Customize the workflow for your domain...
```

### Step 4: Update Templates

Modify templates to include domain-specific sections:

- Add relevant sections
- Remove irrelevant sections
- Update examples and guidance
- Adjust terminology

### Step 5: Test Your Mission

```bash
spec-mix mission list           # Should show your mission
spec-mix init test --mission my-mission
```

## Mission Best Practices

### Choosing a Mission

**Use Software Development when:**

- Building applications, services, or tools
- Need feature-based specifications
- Focus on implementation details
- Require code quality checks

**Use Product Strategy when:**

- Creating product planning documents
- Need market/competitor analysis
- Developing business cases
- Preparing stakeholder presentations
- Writing 6-Pager strategic documents

**Use Research when:**

- Conducting studies or experiments
- Need research question focus
- Document methodology and findings
- Focus on analysis and conclusions

**Create Custom Mission when:**

- Specialized domain requirements
- Unique workflow needs
- Team-specific processes
- Hybrid approaches needed

### Organizing Projects

```bash
# Group by mission type
projects/
├── software/
│   ├── web-app/
│   ├── mobile-app/
│   └── api-service/
└── research/
    ├── ml-study/
    ├── user-research/
    └── performance-analysis/
```

### Mission Switching Guidelines

**Good times to switch:**

- Project scope changes significantly
- Moving from prototype to production
- Pivoting from research to implementation

**Avoid switching when:**

- In the middle of active development
- Existing specs would become inconsistent
- Team is familiar with current workflow

## Multi-Language Missions

Missions work with any supported language:

```bash
# Korean software development
spec-mix init 내-앱 --mission software-dev --language ko

# Korean research
spec-mix init 내-연구 --mission research --language ko
```

Each language can have different mission implementations:

```text
locales/
├── en/missions/
│   ├── software-dev/
│   └── research/
└── ko/missions/
    ├── software-dev/  # Korean version
    └── research/      # Korean version
```

## Examples

### Software Development Workflow

```bash
# Initialize
spec-mix init todo-app --mission software-dev

cd todo-app

# Define feature
/spec-mix.specify Create task management with categories

# Plan implementation
/spec-mix.plan Use React frontend, Node.js backend, PostgreSQL

# Break down tasks
/spec-mix.tasks

# Implement
/spec-mix.implement

# Review and accept
/spec-mix.review
/spec-mix.accept
```

### Product Strategy Workflow

```bash
# Initialize
spec-mix init my-saas --mission product-strategy

cd my-saas

# Create 6-Pager (guided conversation)
/spec-mix.specify B2B SaaS for project management

# Deep analysis
/spec-mix.analyze market       # TAM/SAM/SOM analysis
/spec-mix.analyze competitor   # Competitive landscape
/spec-mix.analyze customer     # Persona development

# Incorporate feedback
/spec-mix.refine CFO requested more detailed unit economics

# Stakeholder review
/spec-mix.review stakeholder
```

### Research Workflow

```bash
# Initialize
spec-mix init attention-study --mission research

cd attention-study

# Formulate question
/spec-mix.specify Research Question: Do attention visualizations improve model trust?

# Design study
/spec-mix.plan Mixed-methods study with surveys and metrics

# Plan activities
/spec-mix.tasks

# Execute research
/spec-mix.implement

# Document findings
/spec-mix.review
/spec-mix.accept
```

## Troubleshooting

### Mission not found

```bash
# List available missions
spec-mix mission list

# Check mission files exist
ls src/specmix/locales/en/missions/
```

### Commands not updating

```bash
# Verify mission is set
spec-mix mission current

# Force update commands
spec-mix mission set [mission-name] --force
```

### Custom mission not appearing

1. Verify directory structure matches expected format
2. Check command files have proper frontmatter
3. Ensure mission name doesn't conflict with existing
4. Restart your AI agent to reload commands

## Advanced Topics

### Mission Inheritance

You can create missions that extend others:

```bash
# Base mission
missions/software-dev/

# Extended mission
missions/mobile-dev/  # Extends software-dev with mobile-specific templates
```

### Mission Plugins

Future feature: Install missions as plugins:

```bash
# Future capability
spec-mix mission install game-dev
spec-mix mission install devops
```

## Next Steps

- [Enhanced Features Overview](features.md)
- [Multi-Language Guide](i18n.md)
- [Quick Start](quickstart.md)
