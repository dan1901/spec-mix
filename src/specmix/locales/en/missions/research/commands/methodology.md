---
description: Define research methodology and approach for systematic investigation
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Purpose

Establish a systematic approach to answer the research question. Define what data to collect, from where, and how to analyze it.

## Prerequisites

- `research-question.md` must exist and be complete

## Execution Flow

### 1. Load Context

Read:
- `research-question.md` - Primary and secondary questions
- `specs/constitution.md` - Research principles (if exists)

### 2. Select Research Approach

Choose based on question type:

| Question Type | Recommended Approach | Data Types |
|---------------|---------------------|------------|
| Exploratory | Literature review + Expert sources | Qualitative |
| Descriptive | Documentation analysis + Case studies | Mixed |
| Comparative | Systematic comparison framework | Quantitative + Qualitative |
| Causal | Evidence triangulation | Multiple sources |
| Evaluative | Criteria-based assessment | Metrics + Qualitative |

### 3. Define Data Collection Strategy

**Source Categories**:

1. **Academic Sources**
   - Peer-reviewed papers (arXiv, journals)
   - Conference proceedings
   - Dissertations/theses

2. **Technical Sources**
   - Official documentation
   - Technical blogs (reputable)
   - GitHub repositories
   - Stack Overflow (for patterns)

3. **Industry Sources**
   - Industry reports
   - Case studies
   - White papers
   - News articles (credible outlets)

4. **Expert Sources**
   - Interviews/podcasts
   - Conference talks
   - Expert blogs

**For each secondary question**, specify:
- Which source categories are most relevant
- Minimum number of sources required
- Quality threshold (A/B/C rating)

### 4. Establish Search Strategy

Define for each secondary question:
```markdown
## Q1: [Secondary Question]

**Keywords**: [primary], [secondary], [alternatives]
**Boolean Query**: "term1" AND ("term2" OR "term3") NOT "exclude"
**Sources**: [Academic, Technical, Industry]
**Date Range**: [If relevant]
**Language**: [en, or specify]
**Minimum Sources**: [Number]
```

### 5. Define Analysis Framework

**For Qualitative Data**:
- Thematic analysis (identify patterns)
- Content analysis (categorize information)
- Comparative analysis (contrast sources)

**For Quantitative Data**:
- Statistical comparison (if applicable)
- Trend analysis
- Benchmark comparison

**Evidence Triangulation**:
- Require 3+ independent sources for key claims
- Document conflicting evidence
- Note consensus vs. debate areas

### 6. Set Quality Criteria

**Source Quality Assessment**:
| Criterion | A (High) | B (Medium) | C (Low) |
|-----------|----------|------------|---------|
| Authority | Peer-reviewed, recognized expert | Known organization | Unknown/informal |
| Currency | < 2 years | 2-5 years | > 5 years |
| Relevance | Directly addresses question | Related topic | Tangential |
| Objectivity | Balanced, cited | Minor bias | Promotional/biased |

**Minimum Quality Requirements**:
- At least 50% of sources must be A or B rated
- No conclusion based solely on C-rated sources
- Conflicting claims require A-rated source resolution

### 7. Define Deliverables

| Phase | Deliverable | Description |
|-------|-------------|-------------|
| Search | `data-sources.md` | Curated list of sources |
| Literature | `literature-review.md` | Summary of existing knowledge |
| Collection | `evidence/*.md` | Organized evidence files |
| Synthesis | `findings.md` | Key findings with citations |
| Analysis | `analysis.md` | Cross-cutting analysis |

### 8. Write methodology.md

Create `FEATURE_DIR/methodology.md`:

```markdown
# Research Methodology: [TOPIC]

## Research Approach
[Selected approach and rationale]

## Data Collection Strategy

### Source Categories
[Which categories and why]

### Search Strategy by Question
[Detailed search plans]

## Analysis Framework
[How data will be analyzed]

## Quality Criteria
[Minimum standards]

## Deliverables and Timeline
[What will be produced]

## Limitations
[Known constraints on methodology]
```

## Output

Report:
- Research approach selected
- Number of source categories targeted
- Search strategies defined
- Quality criteria established
- Next step: `/spec-mix.search` or `/spec-mix.literature`
