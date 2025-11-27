---
description: Improve the 6-Pager document by incorporating feedback.
---

## User Input

```text
{ARGS}
```

You **MUST** consider the user input above if not empty.

## Overview

This command improves the 6-Pager document by incorporating stakeholder feedback, analysis results, or new information.

---

## Workflow

### Step 1: Review Current Document

```bash
# Read 6-Pager document
cat specs/strategy/6pager.md

# Check for analysis documents
ls -la specs/strategy/*.md
```

### Step 2: Identify Feedback Type

Analyze user input to identify feedback type:

| Type | Example | Processing Method |
|------|---------|-------------------|
| **Section Update** | "Update market size" | Modify specific section |
| **Data Update** | "Change TAM to $10B" | Update figures |
| **Feedback Incorporation** | "Reviewer requested more competitor analysis" | Strengthen content |
| **Structure Change** | "Add another persona" | Expand structure |
| **Overall Improvement** | (empty input) | Review and suggest improvements |

### Step 3: Process Based on Feedback

#### A. Specific Section Update Request

1. Identify the relevant section
2. Apply requested changes
3. Present change summary

```markdown
## Changes Complete

### Modified Section: [Section Name]

**Before**:
[Previous content summary]

**After**:
[New content summary]

### Reason for Change
[Why this change was made]
```

#### B. Analysis Results Integration Request

Integrate analysis document content into 6-Pager:

```bash
# Read analysis results
cat specs/strategy/market-research.md 2>/dev/null
cat specs/strategy/competitor-analysis.md 2>/dev/null
cat specs/strategy/customer-analysis.md 2>/dev/null
```

After integration:

```markdown
## Analysis Results Incorporated

The following analysis results have been reflected in the 6-Pager:

### Market Analysis → Section 4 (Market Size)
- Updated TAM/SAM/SOM figures
- Added market growth rate data

### Competitor Analysis → Section 6 (Competitive Analysis)
- Enhanced competitor matrix
- Clarified differentiation points

### Customer Analysis → Section 5 (Customer Understanding)
- Incorporated validated persona content
- Adjusted pain point priorities
```

#### C. Overall Improvement (Empty Input)

Review entire document and suggest improvements:

```markdown
## 6-Pager Quality Review

### Current State Assessment

| Section | Completeness | Key Issues |
|---------|--------------|------------|
| 1. One-Line Summary | ⭐⭐⭐⭐⭐ | - |
| 2. Background & Purpose | ⭐⭐⭐⭐ | Needs stronger Why Now |
| 3. Goals & KPIs | ⭐⭐⭐ | KPIs need more specificity |
| ... | | |

### Improvement Recommendations

#### High Priority
1. **[Section Name]**: [Improvement content]
2. **[Section Name]**: [Improvement content]

#### Medium Priority
1. **[Section Name]**: [Improvement content]

#### Low Priority
1. **[Section Name]**: [Improvement content]

### Additional Information Needed

| Item | Why Needed | How to Obtain |
|------|------------|---------------|
| | | |

Would you like to proceed with improvements? (Y/N)
```

### Step 4: Record Change History

Update the "Change History" section at the bottom of the document:

```markdown
### C. Change History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| v1.0 | YYYY-MM-DD | Initial creation | [Name] |
| v1.1 | YYYY-MM-DD | [Change summary] | AI Assistant |
```

### Step 5: Present Results

```markdown
## Improvement Complete

### Change Summary

| Section | Change Type | Description |
|---------|-------------|-------------|
| | Modified | |
| | Added | |
| | Removed | |

### Next Steps

- [ ] Review changes
- [ ] Collect stakeholder feedback
- [ ] Proceed with formal review via `/spec-mix.review`
```

---

## Improvement Guidelines

### Principles of Good Improvement

1. **Maintain Consistency**: Preserve tone and style throughout document
2. **Track Changes**: Clearly record what changed and why
3. **Cite Sources**: Update sources when data changes
4. **Check Impact**: Review how changes to one section affect others

### Cautions

- Don't arbitrarily change approved content
- Update related calculations when changing numbers
- Remove assumption markers when assumptions are validated
- Clearly mark new assumptions when added

### Version Management

- Minor changes: v1.0 → v1.1
- Major changes: v1.1 → v2.0
- Post-review approval: Draft → v1.0

---

## Common Improvement Patterns

### Data Update

```
Input: "Change TAM from $50B to $75B, source is Gartner 2024"

Processing:
1. Update TAM value in Section 4
2. Add source to calculation basis
3. Review SAM/SOM ratios
4. Record in change history
```

### Feedback Incorporation

```
Input: "CFO requested more detailed CAC breakdown in Unit Economics"

Processing:
1. Expand CAC item in Section 9.3
2. Add channel-by-channel CAC breakdown
3. Note related assumptions
4. Record in change history
```

### Add Competitor

```
Input: "Add Competitor D"

Processing:
1. Request Competitor D information from user
2. Add to competitor matrix in Section 6
3. Update competitive advantage analysis
4. Record in change history
```
