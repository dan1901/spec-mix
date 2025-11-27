---
description: Perform deep analysis on market, competitors, and customers.
---

## User Input

```text
{ARGS}
```

You **MUST** consider the user input above if not empty.

## Overview

This command performs deep analysis to improve the quality of the 6-Pager document. It analyzes three areas:

1. **Market Analysis** - Market size, trends, growth drivers
2. **Competitor Analysis** - Competitive landscape, strengths/weaknesses, positioning
3. **Customer Analysis** - Persona validation, deep needs analysis

---

## Analysis Types

Select analysis type based on user input:

| Input | Analysis Type |
|-------|---------------|
| `market` | Market analysis only |
| `competitor` | Competitor analysis only |
| `customer` | Customer analysis only |
| (empty) | Perform all analyses |

---

## 1. Market Analysis

### 1.1 Check Existing Information

```bash
# Check 6-Pager document
cat specs/strategy/6pager.md 2>/dev/null | head -200
```

### 1.2 Market Size Validation

Validate TAM/SAM/SOM figures in the current 6-Pager:

```markdown
## Market Size Analysis

### TAM (Total Addressable Market)
- **Definition**: [Market definition and scope]
- **Size**: $[amount]
- **Calculation Basis**:
  - Data source: [Research firm, report name]
  - Method: [Top-down / Bottom-up]
  - Calculation: [Specific calculation logic]

### SAM (Serviceable Available Market)
- **Target Market Definition**: [Accessible market scope]
- **Size**: $[amount]
- **Percentage of TAM**: [%]
- **Limiting Factors**: [Region, language, platform, etc.]

### SOM (Serviceable Obtainable Market)
- **Realistic Target Market**: [Market obtainable initially]
- **Size**: $[amount]
- **Percentage of SAM**: [%]
- **Acquisition Strategy**: [How to capture this market]
```

### 1.3 Market Trend Analysis

```markdown
## Market Trends

### Growth Drivers
1. **[Driver 1]**: [Description and impact]
2. **[Driver 2]**: [Description and impact]

### Restraints
1. **[Factor 1]**: [Description and impact]
2. **[Factor 2]**: [Description and impact]

### Opportunities
1. **[Opportunity 1]**: [Description]
2. **[Opportunity 2]**: [Description]

### Threats
1. **[Threat 1]**: [Description]
2. **[Threat 2]**: [Description]
```

### 1.4 Save Results

Save analysis results to a separate file:

```bash
mkdir -p specs/strategy
# Create specs/strategy/market-research.md
```

---

## 2. Competitor Analysis

### 2.1 Identify Competitors

```markdown
## Competitive Landscape

### Direct Competitors
Products/services solving the same problem in the same way

| Competitor | Product | Target Customer | Price Range | Strengths | Weaknesses |
|------------|---------|-----------------|-------------|-----------|------------|
| | | | | | |

### Indirect Competitors
Products/services solving the same problem differently

| Competitor | Product | Solution Method | Difference from Us |
|------------|---------|-----------------|-------------------|
| | | | |

### Substitutes
Ways to solve the problem differently or ignore it

| Substitute | Description | Why Customers Choose It |
|------------|-------------|------------------------|
| | | |
```

### 2.2 Deep Competitor Analysis

For each major competitor:

```markdown
## [Competitor Name] Analysis

### Basic Information
- **Company Name**:
- **Founded**:
- **Size**: (employees, revenue, funding)
- **Main Products**:

### Product Analysis
- **Core Features**:
- **Pricing Model**:
- **Target Customers**:
- **Tech Stack**: (if known)

### SWOT Analysis
| Strengths | Weaknesses |
|-----------|------------|
| | |

| Opportunities | Threats |
|---------------|---------|
| | |

### Market Position
- **Market Share**: [%] (estimated)
- **Brand Awareness**:
- **Customer Reviews**: (reviews, NPS, etc.)

### Recent Developments
- **New Features/Products**:
- **Strategic Moves**:
- **Funding/Acquisition News**:
```

### 2.3 Competitive Advantage Analysis

```markdown
## Our Competitive Advantage

### Differentiation Matrix

| Factor | Us | Competitor A | Competitor B | Importance |
|--------|-----|--------------|--------------|------------|
| | | | | High |
| | | | | Medium |
| | | | | Low |

### Sustainable Competitive Advantages
Strengths that competitors cannot easily replicate:

1. **[Advantage 1]**:
   - Basis:
   - Sustainability:

2. **[Advantage 2]**:
   - Basis:
   - Sustainability:

### Vulnerable Areas
Areas where competitors have the upper hand:

1. **[Area 1]**:
   - Response strategy:

2. **[Area 2]**:
   - Response strategy:
```

### 2.4 Save Results

```bash
# Create specs/strategy/competitor-analysis.md
```

---

## 3. Customer Analysis

### 3.1 Persona Validation

Deep analysis of 6-Pager personas:

```markdown
## Deep Persona Analysis

### Persona A: [Name]

#### Demographics
- **Age**:
- **Occupation**:
- **Income Level**:
- **Location**:
- **Family Structure**:

#### Psychographics
- **Values**:
- **Lifestyle**:
- **Tech Savviness**:
- **Purchase Decision Factors**:

#### Behavioral Patterns
- **Information Search Channels**:
- **Decision-Making Process**:
- **Purchase Frequency/Amount**:
- **Brand Loyalty**:

#### Deep Pain Point Analysis
| Pain Point | Severity | Frequency | Current Solution | Dissatisfaction Reason |
|------------|----------|-----------|------------------|----------------------|
| | High | Daily | | |
| | Medium | Weekly | | |

#### Jobs to be Done
- **Core Job**:
- **Related Jobs**:
- **Emotional Jobs**:
- **Social Jobs**:

#### Customer Journey
| Stage | Behavior | Emotion | Pain Point | Opportunity |
|-------|----------|---------|------------|-------------|
| Awareness | | | | |
| Consideration | | | | |
| Purchase | | | | |
| Usage | | | | |
| Advocacy | | | | |
```

### 3.2 Segment Analysis

```markdown
## Customer Segment Analysis

### Segment Matrix

| Segment | Size | Growth | Accessibility | Profitability | Priority |
|---------|------|--------|---------------|---------------|----------|
| | | | | | |

### Target Segment Selection Rationale

1. **[Selected Segment]**
   - Selection reason:
   - Expected size:
   - Approach strategy:
```

### 3.3 Save Results

```bash
# Create specs/strategy/customer-analysis.md
```

---

## 4. Integrate Analysis Results

When all analyses are complete, suggest 6-Pager updates:

```markdown
## Analysis Complete

The following analysis documents have been created:
- `specs/strategy/market-research.md`
- `specs/strategy/competitor-analysis.md`
- `specs/strategy/customer-analysis.md`

### Suggested 6-Pager Updates

Based on analysis results, recommend updates to these sections:

| Section | Current State | Update Content |
|---------|---------------|----------------|
| Market Size | [Existing content] | [New data] |
| Competitor Analysis | [Existing content] | [Additional insights] |
| Personas | [Existing content] | [Validated content] |

### Key Insights

1. **Market Opportunity**:
2. **Competitive Advantage**:
3. **Target Customer**:

### Next Steps

1. `/spec-mix.refine` - Reflect analysis results in 6-Pager
2. Review list of assumptions needing validation
```

---

## Analysis Tips

### Finding Market Data

- **Official Statistics**: Government agencies, industry association reports
- **Research Firms**: Gartner, Statista, IDC, Forrester
- **Public Sources**: Competitor IR materials, press coverage, academic papers

### Finding Competitor Information

- **Official Channels**: Website, blog, social media
- **Review Sites**: G2, Capterra, App Store reviews
- **News/Press**: TechCrunch, industry media
- **Job Postings**: Tech stack, business direction insights

### Finding Customer Insights

- **Direct Interviews**: 5-10 potential customers
- **Surveys**: 100+ quantitative research
- **Communities**: Reddit, relevant forums, industry communities
- **Review Analysis**: Extract pain points from competitor product reviews
