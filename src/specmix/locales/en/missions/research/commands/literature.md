---
description: Conduct systematic literature review to understand existing knowledge
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Purpose

Review and synthesize existing literature to understand what is already known about the research topic, identify gaps, and establish the foundation for original analysis.

## Prerequisites

- `research-question.md` must exist
- `data-sources.md` should have sources collected

## Execution Flow

### 1. Load Context

Read:
- `research-question.md` - Questions guiding the review
- `methodology.md` - Analysis framework
- `data-sources.md` - Sources to review
- `bibliography.md` - Citation information

### 2. Prioritize Sources

Order sources for review:
1. **A-rated sources** first (most authoritative)
2. **Most relevant** to primary question
3. **Most recent** (current state of knowledge)
4. **Foundational** works (seminal papers)

### 3. Deep Read Each Source

For each source, use WebFetch if URL available, then extract:

**Content Analysis Template**:
```markdown
## [Source Title] (ID: S##)

### Main Arguments
- [Key argument 1]
- [Key argument 2]

### Evidence Presented
- [Evidence type]: [Summary]
- [Data/findings]: [Summary]

### Methodology (if applicable)
- Approach: [How did they investigate?]
- Limitations: [What constraints?]

### Key Findings
1. [Finding 1]
2. [Finding 2]

### Relevance to Research Questions
- Q1: [How it addresses Q1]
- Q2: [How it addresses Q2]

### Quotes for Citation
> "[Exact quote]" (section/page)

### Critical Notes
- Strengths: [What's convincing]
- Weaknesses: [What's questionable]
- Gaps: [What's not covered]
```

### 4. Identify Themes

As you review, track emerging themes:

```markdown
## Emerging Themes

### Theme 1: [Name]
- Description: [What this theme covers]
- Supporting sources: S01, S03, S07
- Key consensus: [What sources agree on]
- Debates: [Where sources disagree]

### Theme 2: [Name]
...
```

### 5. Map Knowledge Landscape

Create a knowledge map:

```markdown
## Knowledge Landscape

### Well-Established
[Areas with strong consensus and evidence]
- [Topic]: Supported by S01, S02, S05

### Emerging/Debated
[Areas with ongoing discussion]
- [Topic]: S03 argues X, S04 argues Y

### Gaps in Literature
[Areas with insufficient research]
- [Gap 1]: No sources address...
- [Gap 2]: Only C-rated sources cover...

### Contradictions
[Where sources conflict]
- S01 claims X, but S06 shows Y
- Resolution needed for: [topic]
```

### 6. Synthesize Findings

Don't just summarize - synthesize:

**Synthesis Questions**:
- What does the literature collectively tell us?
- Where is there agreement vs. disagreement?
- What methodologies are most common/effective?
- What are the major schools of thought?
- How has understanding evolved over time?

### 7. Write literature-review.md

Create `FEATURE_DIR/literature-review.md`:

```markdown
# Literature Review: [TOPIC]

## Overview
[2-3 paragraph summary of the literature landscape]

## Key Themes

### [Theme 1]
[Synthesis of sources on this theme]

**Sources**: S01, S03, S07
**Consensus**: [What's agreed]
**Debate**: [What's contested]

### [Theme 2]
...

## State of Knowledge

### What We Know
[Well-established findings with citations]

### What's Debated
[Areas of disagreement with different positions]

### What's Missing
[Gaps in the literature]

## Methodological Landscape
[How has this topic been studied? What approaches work?]

## Evolution of Understanding
[How has thinking on this topic changed over time?]

## Implications for This Research
[How does this literature inform our research questions?]

## Critical Assessment
[Overall quality and limitations of available literature]
```

### 8. Update Bibliography

Ensure all reviewed sources are properly cited in `bibliography.md` with "Used In" column updated.

## Output

Report:
- Number of sources reviewed
- Key themes identified
- Knowledge gaps found
- Contradictions noted
- Next step: `/spec-mix.collect` or `/spec-mix.synthesize`

## Literature Review Best Practices

- **Be objective**: Report what sources say, not what you want them to say
- **Note limitations**: Every source has constraints
- **Track disagreements**: Conflicting views are valuable data
- **Cite properly**: Every claim needs attribution
- **Synthesize, don't summarize**: Find connections between sources
