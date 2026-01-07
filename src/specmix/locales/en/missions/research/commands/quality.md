---
description: Generate and run research quality checklist for ongoing quality assurance
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Purpose

Create and evaluate quality checklists at any stage of research to ensure standards are met. Can be run multiple times throughout the research process.

## When to Use

- After defining research question
- After completing literature review
- After evidence collection
- Before finalizing findings
- As a final pre-completion check

## Execution Flow

### 1. Determine Research Stage

Check which artifacts exist:
- `research-question.md` → Question stage complete
- `methodology.md` → Methodology stage complete
- `data-sources.md` → Search stage complete
- `literature-review.md` → Literature stage complete
- `evidence/` → Collection stage complete
- `analysis.md` → Analysis stage complete
- `findings.md` → Documentation stage complete

### 2. Generate Stage-Appropriate Checklist

Create `FEATURE_DIR/checklists/quality-[stage].md`:

### For Question Stage:

```markdown
# Quality Checklist: Research Question

## Question Clarity
- [ ] Primary question is specific and focused
- [ ] Primary question is answerable with available resources
- [ ] Question is not leading or biased
- [ ] Secondary questions support primary question
- [ ] All secondary questions are distinct (no overlap)

## Scope Definition
- [ ] In-scope items clearly listed
- [ ] Out-of-scope items explicitly stated
- [ ] Scope is realistic for available time/resources

## Success Criteria
- [ ] Criteria are measurable
- [ ] Criteria are achievable
- [ ] Criteria cover all secondary questions

## Constraints
- [ ] Time constraints documented
- [ ] Resource limitations noted
- [ ] Access restrictions identified
```

### For Methodology Stage:

```markdown
# Quality Checklist: Methodology

## Research Design
- [ ] Approach matches question type
- [ ] Data sources appropriate for question
- [ ] Analysis method defined

## Search Strategy
- [ ] Keywords identified for each question
- [ ] Multiple source categories planned
- [ ] Quality criteria established

## Quality Standards
- [ ] Minimum source counts defined
- [ ] Quality rating system specified
- [ ] Evidence triangulation planned
```

### For Search/Literature Stage:

```markdown
# Quality Checklist: Sources

## Source Coverage
- [ ] Minimum sources per question met
- [ ] Multiple source categories used
- [ ] Recent and foundational sources included

## Source Quality
- [ ] ≥50% A or B rated sources
- [ ] No over-reliance on single source
- [ ] Diverse perspectives included

## Documentation
- [ ] All sources in bibliography
- [ ] Quality ratings assigned
- [ ] Relevance to questions noted
```

### For Collection Stage:

```markdown
# Quality Checklist: Evidence

## Coverage
- [ ] Evidence collected for all questions
- [ ] ≥3 evidence pieces per question
- [ ] A-rated evidence for key claims

## Quality
- [ ] All evidence traceable to sources
- [ ] Context preserved for quotes
- [ ] Contradicting evidence included

## Organization
- [ ] Evidence organized by question
- [ ] Summaries created for each question
- [ ] Coverage matrix complete
```

### For Analysis Stage:

```markdown
# Quality Checklist: Analysis

## Synthesis Quality
- [ ] All questions addressed
- [ ] Evidence integrated (not just listed)
- [ ] Patterns/themes identified
- [ ] Contradictions addressed

## Rigor
- [ ] Multiple sources support key claims
- [ ] Alternative interpretations considered
- [ ] Limitations acknowledged

## Logic
- [ ] Conclusions follow from evidence
- [ ] No logical fallacies
- [ ] Confidence levels appropriate
```

### For Findings Stage:

```markdown
# Quality Checklist: Findings

## Content Quality
- [ ] Executive summary is standalone
- [ ] Key findings clearly stated
- [ ] Evidence cited for all claims
- [ ] Confidence levels stated

## Completeness
- [ ] All research questions answered
- [ ] Methodology summarized
- [ ] Limitations documented
- [ ] References complete

## Credibility
- [ ] No unsupported claims
- [ ] Contradicting evidence addressed
- [ ] Biases acknowledged
```

### 3. Evaluate Checklist

For each item:
1. Check the relevant artifact
2. Determine pass/fail
3. Note specific issues if failed

### 4. Generate Quality Report

```markdown
# Quality Report: [Stage]

## Summary
- **Status**: [PASS / NEEDS ATTENTION / CRITICAL ISSUES]
- **Checks Passed**: [#]/[#]
- **Critical Issues**: [#]

## Detailed Results

### Passed Checks
- [x] [Check item 1]
- [x] [Check item 2]

### Failed Checks
- [ ] [Check item 3]
  - **Issue**: [Specific problem]
  - **Fix**: [Recommended action]

- [ ] [Check item 4]
  - **Issue**: [Specific problem]
  - **Fix**: [Recommended action]

## Recommended Actions
1. [Priority action 1]
2. [Priority action 2]

## Next Steps
[What should happen next based on results]
```

### 5. Comprehensive Final Check

If research is complete, run all checklists:

```markdown
# Final Quality Assessment

## Stage Summaries
| Stage | Status | Pass Rate | Critical Issues |
|-------|--------|-----------|-----------------|
| Question | Pass | 100% | 0 |
| Methodology | Pass | 90% | 0 |
| Sources | Attention | 80% | 0 |
| Evidence | Pass | 95% | 0 |
| Analysis | Pass | 100% | 0 |
| Findings | Attention | 85% | 1 |

## Overall Status
**[READY FOR COMPLETION / NEEDS REVISION]**

## Outstanding Issues
[List all unresolved issues across stages]

## Final Recommendations
[What must be done before research is complete]
```

## Output

Report:
- Current stage detected
- Checklist results
- Issues found
- Recommended actions
- Overall quality status
