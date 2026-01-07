---
description: Systematically collect and organize evidence to answer research questions
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Purpose

Gather specific evidence from sources to answer each research question. Organize evidence for easy retrieval and citation.

## Prerequisites

- `research-question.md` must exist
- `data-sources.md` should have sources listed
- `literature-review.md` should be complete (recommended)

## Execution Flow

### 1. Load Context

Read:
- `research-question.md` - Questions to answer
- `methodology.md` - Evidence quality criteria
- `data-sources.md` - Sources to extract from
- `literature-review.md` - Themes identified

### 2. Create Evidence Directory

```
FEATURE_DIR/evidence/
├── Q1-[question-slug]/
│   ├── evidence-01.md
│   ├── evidence-02.md
│   └── summary.md
├── Q2-[question-slug]/
│   └── ...
└── cross-cutting/
    └── ...
```

### 3. Extract Evidence by Question

For each secondary question, systematically extract evidence:

**Evidence Extraction Template**:
```markdown
# Evidence: [Brief descriptor]

## Metadata
- **Source**: [Source ID from bibliography]
- **Question**: Q[#]
- **Type**: [Statistic/Quote/Finding/Example/Data]
- **Quality**: [A/B/C - inherited from source]

## Evidence Content

### Raw Evidence
> "[Exact quote or data point]"
> — Source: [citation]

### Context
[What was the context of this evidence? What question was the source addressing?]

### Interpretation
[What does this evidence suggest about our research question?]

## Reliability Assessment

- **Directness**: [Direct/Indirect evidence for our question]
- **Corroboration**: [Other sources supporting this? List IDs]
- **Limitations**: [Any caveats about this evidence]

## Tags
[keyword1], [keyword2], [question-number]
```

### 4. Evidence Types to Collect

**Quantitative Evidence**:
- Statistics and metrics
- Survey results
- Performance benchmarks
- Comparative data

**Qualitative Evidence**:
- Expert opinions
- Case study findings
- Theoretical arguments
- Observed patterns

**Mixed Evidence**:
- Research findings with both
- Industry reports
- Systematic reviews

### 5. Quality Control

For each piece of evidence, verify:

| Check | Pass | Notes |
|-------|------|-------|
| Source is in bibliography | [ ] | |
| Quote is accurate | [ ] | |
| Context preserved | [ ] | |
| Not cherry-picked | [ ] | |
| Limitations noted | [ ] | |

### 6. Track Evidence Coverage

Create `evidence/coverage.md`:

```markdown
# Evidence Coverage Matrix

## By Question

| Question | Evidence Count | A-rated | B-rated | Sufficient? |
|----------|---------------|---------|---------|-------------|
| Q1 | 8 | 3 | 4 | Yes |
| Q2 | 4 | 1 | 2 | Needs more |
| Q3 | 6 | 2 | 3 | Yes |

## By Theme

| Theme | Evidence Count | Sources | Notes |
|-------|---------------|---------|-------|
| [Theme 1] | 5 | S01, S03, S07 | Strong coverage |
| [Theme 2] | 3 | S02, S04 | Need corroboration |

## Gaps Identified
- [Gap 1]: No direct evidence for [aspect]
- [Gap 2]: Only single source for [claim]

## Contradictory Evidence
- [Topic]: E-01 vs E-05 (conflicting findings)
```

### 7. Create Question Summaries

For each question directory, create `summary.md`:

```markdown
# Evidence Summary: Q[#]

## Question
[Full secondary question]

## Evidence Overview
- Total pieces: [#]
- Quality distribution: [# A, # B, # C]
- Sources used: [list]

## Key Evidence

### Supporting [Answer direction]
1. **E-01**: [Brief summary] (Quality: A)
2. **E-03**: [Brief summary] (Quality: B)

### Contradicting/Complicating
1. **E-05**: [Brief summary] (Quality: B)

## Preliminary Answer
Based on evidence collected, [tentative answer to question]

## Confidence Level
[High/Medium/Low] - because [reasoning]

## Remaining Gaps
[What evidence is still needed?]
```

### 8. Cross-Reference Check

Ensure:
- All evidence traces back to bibliography
- No orphaned evidence (uncited sources)
- No unsupported claims (evidence for each assertion)

## Output

Report:
- Total evidence pieces collected
- Coverage by question
- Quality distribution
- Gaps identified
- Contradictions found
- Next step: `/spec-mix.synthesize` or `/spec-mix.findings`

## Evidence Collection Principles

- **Completeness**: Collect both supporting AND contradicting evidence
- **Accuracy**: Quote exactly, don't paraphrase inaccurately
- **Context**: Note the original context of evidence
- **Traceability**: Every piece links to bibliography
- **Honesty**: Don't ignore inconvenient evidence
