# 6-Pager Strategic Document Guide

The Product Strategy mission helps you create Amazon-style 6-Pager strategic documents with AI assistance, including automatic web research and source citation.

## What is a 6-Pager?

A 6-Pager is a structured strategic document format popularized by Amazon. It forces clear thinking by requiring comprehensive analysis in a concise format. Our implementation includes 14 sections covering all aspects of product strategy.

## Quick Start

```bash
# Initialize project with product-strategy mission
spec-mix init my-product --mission product-strategy --ai claude

cd my-product

# Create 6-Pager document
/spec-mix.specify AI-powered budgeting app for millennials
```

## Document Structure

The 6-Pager template includes 14 sections:

| # | Section | Purpose |
|---|---------|---------|
| 1 | One-Line Summary | Elevator pitch in one sentence |
| 2 | Background & Purpose | Why now? What problem? |
| 3 | Goals & KPIs | Vision and measurable targets |
| 4 | Market Size | TAM/SAM/SOM analysis |
| 5 | Customer Understanding | Personas and JTBD |
| 6 | Competitive Analysis | Competitor matrix and positioning |
| 7 | Solution & USP | Core features and differentiation |
| 8 | User Stories | Epics and user stories |
| 9 | Business Model | Revenue model and unit economics |
| 10 | GTM Strategy | Launch and marketing plan |
| 11 | Product Principles | Decision-making guidelines |
| 12 | Milestones | Roadmap and key deliverables |
| 13 | Risks | Risk matrix and mitigation |
| 14 | Open Issues | Decisions needed |

## Available Commands

### `/spec-mix.specify`

Creates the 6-Pager document through guided conversation with automatic web research.

**Usage:**

```bash
# Basic usage
/spec-mix.specify

# With product description
/spec-mix.specify B2B SaaS for project management targeting remote teams
```

**Workflow:**

1. **Gather Information** - AI asks questions about your product
2. **Web Research** - Automatic search for market data, competitors, trends
3. **Generate Document** - Creates 6-Pager with cited sources
4. **Identify Gaps** - Lists items needing validation

### `/spec-mix.analyze`

Deep dive analysis for specific areas.

**Usage:**

```bash
# Full analysis
/spec-mix.analyze

# Market analysis only
/spec-mix.analyze market

# Competitor analysis only
/spec-mix.analyze competitor

# Customer analysis only
/spec-mix.analyze customer
```

**Output:**

- `specs/strategy/market-research.md`
- `specs/strategy/competitor-analysis.md`
- `specs/strategy/customer-analysis.md`

### `/spec-mix.refine`

Improve document based on feedback.

**Usage:**

```bash
# General improvement
/spec-mix.refine

# Specific update
/spec-mix.refine Update TAM to $75B based on Gartner 2024 report

# Incorporate feedback
/spec-mix.refine CFO requested more detailed CAC breakdown
```

### `/spec-mix.review`

Prepare for stakeholder review.

**Usage:**

```bash
# Self quality review
/spec-mix.review self

# Peer review preparation
/spec-mix.review peer

# Stakeholder review preparation
/spec-mix.review stakeholder
```

## Web Research Feature

The AI automatically searches the web to gather data for your 6-Pager.

### What Gets Searched

| Category | Search Examples |
|----------|-----------------|
| Market Data | "[industry] market size 2024", "TAM SAM SOM" |
| Competitors | "[company] funding", "pricing plans", "G2 reviews" |
| Trends | "[industry] trends 2024", "customer behavior" |

### Priority Sources

**Market Data:**

- Statista, Gartner, IDC
- Grand View Research, MarketsandMarkets
- Government statistics

**Competitor Info:**

- Crunchbase (funding, company info)
- G2, Capterra (reviews, ratings)
- Official websites (pricing, features)
- LinkedIn (company size, growth)

### Source Reliability

All data is tagged with reliability indicators:

| Indicator | Meaning | Examples |
|-----------|---------|----------|
| 🟢 Verified | Official, authoritative | Government stats, IR materials, academic papers |
| 🟡 Reference | Credible but unofficial | News articles, industry blogs, analyst opinions |
| 🔴 Estimated | Calculated or assumed | Self-calculations, extrapolations |

### Source Citation Format

```markdown
| Data | Value | Source | Reliability | Access Date |
|------|-------|--------|-------------|-------------|
| Global SaaS Market | $197B | [Statista](https://...) | 🟢 Verified | 2024-01-15 |
| Competitor A ARR | $10M | [Crunchbase](https://...) | 🟡 Reference | 2024-01-15 |
```

## Workflow Examples

### Example 1: New Product Launch

```bash
# Initialize
spec-mix init fintech-app --mission product-strategy

# Create 6-Pager
/spec-mix.specify Personal finance app for Gen Z with AI-powered savings recommendations

# Deep analysis
/spec-mix.analyze market
/spec-mix.analyze competitor

# Incorporate findings
/spec-mix.refine

# Prepare for board presentation
/spec-mix.review stakeholder
```

### Example 2: Feature Expansion

```bash
# Create strategy for new feature
/spec-mix.specify Add cryptocurrency portfolio tracking to existing investment app

# Focus on competitive landscape
/spec-mix.analyze competitor

# Update based on team feedback
/spec-mix.refine Engineering says crypto APIs have 500ms latency - add to risks
```

### Example 3: Market Entry

```bash
# Analyze new market opportunity
/spec-mix.specify Expand project management SaaS to Japanese market

# Deep market analysis
/spec-mix.analyze market
/spec-mix.analyze customer

# Review readiness
/spec-mix.review self
```

## Best Practices

### Writing Good 6-Pagers

**Do:**

- Be specific with numbers and examples
- Cite sources for all data
- Focus on customer value, not technology
- Identify and address risks honestly
- Keep it concise but complete

**Don't:**

- Make unfounded optimistic projections
- Present assumptions as facts
- Underestimate competitors
- Ignore or hide risks
- Write technology-centric descriptions

### Handling Missing Information

When data is unavailable:

1. Mark as `[TBD]` or `[To be validated]`
2. Add to Open Issues section
3. Specify validation method
4. Assign owner and deadline

```markdown
### Open Issues

| ID | Issue | Validation Method | Owner | Deadline |
|----|-------|-------------------|-------|----------|
| OI-001 | Exact TAM for APAC region | Commission market research | PM | Q1 2024 |
```

### Review Process

1. **Self Review** - Check completeness and consistency
2. **Peer Review** - Get feedback from colleagues
3. **Stakeholder Review** - Present to decision makers
4. **Iterate** - Refine based on feedback

## Output Files

After running commands, you'll find:

```text
specs/
└── strategy/
    ├── 6pager.md              # Main strategic document
    ├── market-research.md     # Detailed market analysis
    ├── competitor-analysis.md # Competitor deep dive
    └── customer-analysis.md   # Persona and JTBD analysis
```

## Tips for Effective Use

### 1. Prepare Context

Before starting, gather:

- Product vision and goals
- Known competitors
- Target customer description
- Any existing research

### 2. Be Specific in Prompts

```bash
# ❌ Too vague
/spec-mix.specify mobile app

# ✅ Specific
/spec-mix.specify Mobile app for freelance designers to manage client projects, invoices, and contracts. Target: US-based freelancers earning $50K-150K annually.
```

### 3. Iterate Frequently

Don't try to perfect everything in one pass:

1. Create initial draft
2. Run analysis
3. Refine based on findings
4. Review and iterate

### 4. Validate Key Assumptions

After AI generates the document:

- Verify market size numbers
- Cross-check competitor information
- Validate pricing assumptions
- Test customer personas

## Troubleshooting

### Web Search Not Working

- Check internet connectivity
- Try more specific search terms
- Use `/spec-mix.analyze` for focused research

### Sources Not Found

- Industry may be too niche
- Try broader search terms
- Mark as `[TBD]` and note manual research needed

### Document Too Long

- Focus on key sections first
- Use `/spec-mix.refine` to trim
- Move details to appendix

## Next Steps

After completing your 6-Pager:

1. **Share for Review** - Get stakeholder feedback
2. **Create Action Plan** - Break down into tasks
3. **Switch to Software-Dev** - If building software, switch mission:

   ```bash
   spec-mix mission switch software-dev
   /spec-mix.specify [based on 6-pager user stories]
   ```

## Related Documentation

- [Mission System Overview](missions.md)
- [Multi-Language Support](i18n.md)
- [Quick Start Guide](quickstart.md)
