---
description: Define research question and objectives for a new research project
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Purpose

Define a clear, focused research question that guides the entire research process. This is the foundation of your research project.

## Execution Flow

### 1. Create Research Directory

Create directory structure:
```
specs/[###-research-topic]/
├── research-question.md    # This output
├── methodology.md          # Created by /spec-mix.methodology
├── literature-review.md    # Created by /spec-mix.literature
├── data-sources.md         # Created by /spec-mix.search
├── evidence/               # Created by /spec-mix.collect
├── findings.md             # Created by /spec-mix.findings
├── analysis.md             # Created by /spec-mix.synthesize
└── bibliography.md         # Managed throughout
```

### 2. Parse User Input

Extract from the user's research topic:
- **Core topic**: What subject area?
- **Angle**: What specific aspect?
- **Purpose**: Why does this matter?
- **Constraints**: Time, resources, access limitations

### 3. Formulate Research Question

**Primary Question Requirements**:
- Specific (not too broad)
- Answerable (with available resources)
- Relevant (meaningful impact)
- Objective (not leading to predetermined answer)

**Question Types**:
| Type | Template | Example |
|------|----------|---------|
| Exploratory | "What are the key factors in...?" | "What are the key factors in AI adoption?" |
| Descriptive | "How does X work/function?" | "How does transformer architecture work?" |
| Comparative | "How does X compare to Y?" | "How does RAG compare to fine-tuning?" |
| Causal | "What is the impact of X on Y?" | "What is the impact of context length on accuracy?" |
| Evaluative | "How effective is X for Y?" | "How effective is prompt engineering for code generation?" |

### 4. Define Secondary Questions

Break down the primary question into 3-5 supporting questions:
- Each should be independently researchable
- Together they should comprehensively address the primary question
- Order them logically (foundational → advanced)

### 5. Establish Scope

**In Scope** - Explicitly include:
- Specific aspects to investigate
- Time period (if relevant)
- Geographic/domain boundaries
- Types of sources to consider

**Out of Scope** - Explicitly exclude:
- Related but tangential topics
- Areas requiring resources you don't have
- Questions for future research

### 6. Define Success Criteria

Research will be successful when:
- [ ] Primary question answered with evidence from 5+ credible sources
- [ ] All secondary questions addressed
- [ ] Findings are documented with proper citations
- [ ] Limitations and uncertainties acknowledged
- [ ] Conclusions supported by evidence (not assumptions)

### 7. Identify Constraints

Document:
- **Time**: Available research duration
- **Resources**: Tools, databases, access available
- **Expertise**: Domain knowledge limitations
- **Access**: Paywalls, language barriers, etc.

### 8. Write research-question.md

Use template from `.spec-mix/active-mission/templates/research-question-template.md`

Fill all sections with concrete details from above analysis.

### 9. Initialize Bibliography

Create empty `bibliography.md`:
```markdown
# Bibliography: [TOPIC]

## Citation Format
[Specify: APA/MLA/Chicago/IEEE]

## Sources

### Primary Sources
| ID | Citation | Type | Accessed | Quality | Used In |
|----|----------|------|----------|---------|---------|

### Secondary Sources
| ID | Citation | Type | Accessed | Quality | Used In |
|----|----------|------|----------|---------|---------|

## Notes
- Quality ratings: A (peer-reviewed), B (credible source), C (informal/limited)
```

## Output

Report:
- Created directory path
- Research question summary
- Number of secondary questions
- Defined scope boundaries
- Next step: `/spec-mix.methodology` or `/spec-mix.search`

## Quality Checklist

Before completing, verify:
- [ ] Question is specific and answerable
- [ ] Question is not leading or biased
- [ ] Scope is clearly bounded
- [ ] Success criteria are measurable
- [ ] Constraints are realistic
