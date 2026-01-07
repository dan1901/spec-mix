---
description: Document research findings in a clear, citable format
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Purpose

Create the final findings document that presents research results clearly, with proper citations and confidence levels. This is the primary output of the research project.

## Prerequisites

- `research-question.md` must exist
- `analysis.md` should be complete
- `bibliography.md` should be up to date

## Execution Flow

### 1. Load Context

Read:
- `research-question.md` - Original objectives
- `analysis.md` - Synthesized analysis
- `evidence/coverage.md` - Evidence quality overview
- `bibliography.md` - All citations

### 2. Structure Findings Document

Organize findings for maximum clarity and impact:

```markdown
# Research Findings: [TOPIC]

## Executive Summary
[3-5 paragraph overview for readers who won't read the full document]

## Key Findings
[Numbered list of main discoveries]

## Detailed Findings
[In-depth presentation with evidence]

## Methodology Summary
[Brief description of how research was conducted]

## Limitations
[Honest constraints and caveats]

## Conclusions
[Final answers to research questions]

## Recommendations
[Actionable insights if applicable]

## References
[Full bibliography]
```

### 3. Write Executive Summary

**Structure**:
- Paragraph 1: Research question and why it matters
- Paragraph 2: Approach taken
- Paragraph 3-4: Key findings
- Paragraph 5: Main conclusions and implications

**Guidelines**:
- Write for someone with 5 minutes
- No jargon without explanation
- Include the most important numbers/facts
- State confidence levels

### 4. Present Key Findings

Format each finding:

```markdown
## Key Findings

### Finding 1: [Title]

**Summary**: [One sentence statement]

**Evidence**:
- [Evidence point 1] (Source: [citation])
- [Evidence point 2] (Source: [citation])

**Confidence**: [High/Medium/Low]

**Implications**: [What this means]

---

### Finding 2: [Title]
...
```

**Finding Prioritization**:
1. Most important/impactful first
2. Findings that answer primary question
3. Unexpected or novel discoveries
4. Findings with highest confidence
5. Supporting/contextual findings

### 5. Write Detailed Findings

Expand each key finding with:

```markdown
## Detailed Findings

### 1. [Finding Title]

#### Context
[Background needed to understand this finding]

#### Evidence Analysis

**Primary Evidence**:
> "[Key quote or data]"
> — [Full citation]

[Analysis of what this evidence shows]

**Supporting Evidence**:
- [Additional evidence point 1]
- [Additional evidence point 2]

**Contradicting/Complicating Evidence**:
[If any, and how it was addressed]

#### Interpretation
[What this finding means in context of the research]

#### Confidence Assessment
- **Level**: [High/Medium/Low]
- **Basis**: [Why this confidence level]
- **Caveats**: [Important limitations]
```

### 6. Document Methodology Summary

Brief but sufficient for credibility:

```markdown
## Methodology Summary

### Research Approach
[Type of research conducted]

### Data Sources
- **Academic sources**: [#] papers/articles
- **Technical sources**: [#] documentation/blogs
- **Industry sources**: [#] reports/case studies
- Total sources: [#]

### Quality Assessment
- A-rated (peer-reviewed/authoritative): [#]
- B-rated (credible): [#]
- C-rated (informal): [#]

### Analysis Method
[How evidence was analyzed]

### Limitations
[Key methodological constraints]
```

### 7. State Limitations Clearly

Be honest about:

```markdown
## Limitations

### Scope Limitations
- [What was not investigated]
- [Boundaries of the research]

### Evidence Limitations
- [Gaps in available sources]
- [Quality constraints]

### Methodology Limitations
- [Approach constraints]
- [Time/resource limits]

### Generalizability
- [When/where these findings apply]
- [When/where they may not apply]
```

### 8. Write Conclusions

```markdown
## Conclusions

### Answer to Research Question
[Direct answer to primary question with confidence level]

### Key Takeaways
1. [Most important insight]
2. [Second most important]
3. [Third most important]

### What This Research Contributes
[Value added by this research]

### Remaining Questions
[What this research didn't answer]
```

### 9. Add Recommendations (if applicable)

```markdown
## Recommendations

### For [Audience 1]
1. [Actionable recommendation]
   - Based on: [Finding #]
   - Confidence: [Level]

### For [Audience 2]
1. [Actionable recommendation]

### For Future Research
1. [Research direction suggested]
```

### 10. Compile References

Pull from `bibliography.md`:

```markdown
## References

[1] Author, A. (Year). Title. Source. URL

[2] Author, B. (Year). Title. Source. URL

...
```

### 11. Write findings.md

Create `FEATURE_DIR/findings.md` using template from `.spec-mix/active-mission/templates/findings-template.md` and fill with all sections above.

## Output

Report:
- Findings document complete
- Number of key findings documented
- Total citations used
- Confidence levels stated
- Next step: `/spec-mix.validate`

## Quality Checklist

Before completing:
- [ ] Executive summary is standalone readable
- [ ] Every finding has evidence citations
- [ ] Confidence levels stated for each finding
- [ ] Limitations honestly documented
- [ ] All sources in bibliography
- [ ] No unsupported claims
