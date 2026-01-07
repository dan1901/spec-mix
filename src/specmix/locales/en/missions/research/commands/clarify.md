---
description: Identify underspecified areas in the research question and refine scope through targeted clarification questions
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Purpose

Detect and reduce ambiguity in the research question, scope, or methodology. Ensure the research is focused and achievable before proceeding with data collection.

## Prerequisites

- `research-question.md` must exist

## Execution Flow

### 1. Load Research Question

Read:
- `research-question.md` - Primary and secondary questions
- `methodology.md` - If exists, check alignment

### 2. Ambiguity Scan

Analyze the research question for these categories:

**Question Clarity**:
- Is the primary question specific enough?
- Are secondary questions distinct and non-overlapping?
- Are there hidden assumptions in the questions?

**Scope Definition**:
- Are in-scope boundaries clear?
- Are out-of-scope items explicitly stated?
- Is the scope achievable with available resources?

**Success Criteria**:
- Are success criteria measurable?
- Can success be objectively verified?
- Are there unstated expectations?

**Methodology Alignment** (if methodology.md exists):
- Does the approach match the question type?
- Are data sources appropriate?
- Is the analysis framework suitable?

**Constraints & Feasibility**:
- Are time constraints realistic?
- Are resource limitations acknowledged?
- Are access restrictions considered?

**Terminology**:
- Are key terms defined?
- Are there ambiguous phrases?
- Is domain jargon explained?

For each category, mark status: **Clear / Partial / Missing**

### 3. Generate Clarification Questions

Create prioritized questions (maximum 5):

**Question Criteria**:
- Must materially impact research direction, scope, or quality
- Should be answerable with short answer or multiple choice
- Should reduce ambiguity, not add complexity

**Priority Order**:
1. Questions affecting primary research question
2. Questions affecting scope boundaries
3. Questions affecting methodology
4. Questions affecting success criteria
5. Questions affecting terminology

### 4. Interactive Clarification

Present ONE question at a time:

**For Multiple Choice Questions**:
```markdown
**Question [#]**: [Question text]

**Recommended**: Option [X] - [reasoning why this is best for research quality]

| Option | Description |
|--------|-------------|
| A | [Option A] |
| B | [Option B] |
| C | [Option C] |

Reply with option letter, "recommended", or provide your own answer (<=5 words).
```

**For Short Answer Questions**:
```markdown
**Question [#]**: [Question text]

**Suggested**: [Your suggested answer] - [brief reasoning]

Reply with "suggested" to accept, or provide your own answer (<=5 words).
```

**After Each Answer**:
1. Record the clarification
2. Update `research-question.md` immediately
3. Move to next question

**Stop When**:
- All critical ambiguities resolved
- User signals completion ("done", "proceed")
- 5 questions asked

### 5. Integration

Update `research-question.md` after each answer:

**Add Clarifications Section** (if not exists):
```markdown
## Clarifications

### Session YYYY-MM-DD
- Q: [question] → A: [answer]
```

**Apply to Relevant Sections**:
- Question clarity → Update primary/secondary questions
- Scope changes → Update In Scope / Out of Scope
- Success criteria → Update Success Criteria section
- Terminology → Add to glossary or clarify in context
- Constraints → Update Constraints section

### 6. Validation

After each update, verify:
- [ ] No contradictory statements remain
- [ ] Clarification is integrated into appropriate section
- [ ] Research question remains coherent
- [ ] Scope is still achievable

### 7. Report Completion

```markdown
## Clarification Summary

**Questions Asked**: [#]
**Sections Updated**: [list]

### Coverage Status
| Category | Status | Notes |
|----------|--------|-------|
| Question Clarity | Clear/Partial/Missing | |
| Scope Definition | Clear/Partial/Missing | |
| Success Criteria | Clear/Partial/Missing | |
| Methodology | Clear/Partial/Missing | |
| Constraints | Clear/Partial/Missing | |
| Terminology | Clear/Partial/Missing | |

### Outstanding Items
[Any remaining ambiguities]

### Recommended Next Step
[/spec-mix.methodology or /spec-mix.search]
```

## Behavior Rules

- If no meaningful ambiguities found: "Research question is well-defined. Ready to proceed with methodology or search."
- If `research-question.md` missing: Direct user to run `/spec-mix.question` first
- Never exceed 5 questions
- Respect user early termination ("done", "proceed", "stop")
- Focus on research quality, not perfectionism

## Example Clarification Questions

**Scope**:
- "Should this research include historical analysis (pre-2020) or focus only on current state?"
- "Is this research limited to academic sources or should industry reports be included?"

**Question Refinement**:
- "The phrase '[vague term]' could mean X or Y. Which interpretation should we use?"
- "Should we compare [topic] across different [dimensions] or focus on a single [dimension]?"

**Methodology**:
- "Given the question type, should we prioritize quantitative data or qualitative analysis?"
- "What is the acceptable confidence level for conclusions: high-confidence-only or include medium-confidence findings?"

**Feasibility**:
- "Given time constraints, should we limit sources to [#] or accept partial coverage of some areas?"
