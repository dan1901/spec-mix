---
description: Synthesize collected evidence into coherent analysis and insights
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Purpose

Analyze and synthesize all collected evidence to draw meaningful conclusions, identify patterns, and answer the research questions with supported arguments.

## Prerequisites

- `research-question.md` must exist
- `evidence/` directory should have collected evidence
- `literature-review.md` should be complete

## Execution Flow

### 1. Load All Context

Read:
- `research-question.md` - Questions to answer
- `methodology.md` - Analysis framework
- `literature-review.md` - Existing knowledge themes
- `evidence/coverage.md` - What evidence we have
- All `evidence/Q#/summary.md` files

### 2. Verify Evidence Sufficiency

Before synthesizing, confirm:

```markdown
## Pre-Synthesis Check

| Question | Min Evidence | Actual | A-rated Required | Actual | Status |
|----------|-------------|--------|------------------|--------|--------|
| Q1 | 3 | 8 | 1 | 3 | Ready |
| Q2 | 3 | 4 | 1 | 1 | Ready |
| Q3 | 3 | 2 | 1 | 0 | Need more |
```

If not sufficient, recommend running `/spec-mix.search` or `/spec-mix.collect` again.

### 3. Answer Each Secondary Question

For each question, synthesize evidence into an answer:

```markdown
## Q[#]: [Question]

### Short Answer
[1-2 sentence direct answer]

### Evidence Synthesis

**Key Supporting Evidence**:
1. [Evidence summary] → [What it tells us]
   - Source: [citation]
   - Strength: [Why this is convincing]

2. [Evidence summary] → [What it tells us]
   - Source: [citation]

**Complicating Evidence**:
1. [Evidence that adds nuance or contradicts]
   - Source: [citation]
   - Implication: [How this affects the answer]

### Analysis
[Deeper analysis integrating multiple pieces of evidence]

### Confidence Assessment
- **Level**: [High/Medium/Low]
- **Reasoning**: [Why this confidence level]
- **What would increase confidence**: [Additional evidence needed]
```

### 4. Identify Cross-Cutting Themes

Look for patterns across questions:

```markdown
## Cross-Cutting Themes

### Theme 1: [Name]

**Pattern Observed**:
[What pattern appears across multiple questions/sources]

**Supporting Evidence**:
- From Q1: [Evidence ID]
- From Q2: [Evidence ID]
- From Q3: [Evidence ID]

**Significance**:
[Why this pattern matters]

### Theme 2: [Name]
...
```

### 5. Analyze Contradictions

Address conflicting evidence:

```markdown
## Contradiction Analysis

### Contradiction 1: [Topic]

**Position A**: [Claim]
- Evidence: [IDs]
- Sources: [citations]

**Position B**: [Counter-claim]
- Evidence: [IDs]
- Sources: [citations]

**Analysis**:
[Why the contradiction exists - methodology differences? Context? Time period?]

**Resolution/Stance**:
[Which position is better supported, or if unresolved, why]
```

### 6. Answer Primary Question

Synthesize secondary answers into primary:

```markdown
## Primary Question Answer

### Question
[Full primary research question]

### Synthesized Answer
[Comprehensive answer drawing on all secondary question findings]

### Key Supporting Points
1. [Point from Q1 findings]
2. [Point from Q2 findings]
3. [Point from Q3 findings]

### Important Caveats
- [Limitation 1]
- [Limitation 2]

### Confidence Level
[Overall confidence and reasoning]
```

### 7. Identify Implications

```markdown
## Implications

### Theoretical Implications
[What does this mean for understanding the topic?]

### Practical Implications
[What actions or decisions does this inform?]

### Limitations of This Analysis
- [Scope limitations]
- [Evidence limitations]
- [Methodology limitations]
```

### 8. Write analysis.md

Create `FEATURE_DIR/analysis.md`:

```markdown
# Analysis: [TOPIC]

## Research Question Revisited

**Question**: [Primary question]
**Answer**: [Synthesized answer]

## Secondary Question Findings

### Q1: [Question]
[Synthesized answer with evidence]

### Q2: [Question]
[Synthesized answer with evidence]

...

## Cross-Cutting Themes

### [Theme 1]
[Analysis]

### [Theme 2]
[Analysis]

## Contradiction Resolution
[How conflicting evidence was handled]

## Synthesis
[Integration of all findings]

## Confidence Assessment
[Overall confidence and reasoning]

## Implications
[What this means]

## Limitations
[Honest assessment of constraints]

## Future Research Directions
[What questions remain]
```

## Output

Report:
- Questions answered (count)
- Confidence levels by question
- Cross-cutting themes identified
- Contradictions addressed
- Overall synthesis complete
- Next step: `/spec-mix.findings` or `/spec-mix.validate`

## Synthesis Principles

- **Evidence-based**: Every claim traces to evidence
- **Balanced**: Consider all evidence, not just supporting
- **Honest**: Acknowledge limitations and uncertainties
- **Nuanced**: Avoid oversimplification
- **Connected**: Link findings across questions
