---
description: Review the 6-Pager document and organize feedback.
---

## User Input

```text
{ARGS}
```

You **MUST** consider the user input above if not empty.

## Overview

This command helps systematically review 6-Pager documents and collect/organize stakeholder feedback.

---

## Workflow

### Step 1: Load Document

```bash
# Read 6-Pager document
cat specs/strategy/6pager.md

# Check for analysis documents
ls -la specs/strategy/*.md
```

### Step 2: Select Review Type

Determine review type based on user input:

| Input | Review Type |
|-------|-------------|
| `self` | Self quality review |
| `peer` | Peer review support |
| `stakeholder` | Stakeholder review support |
| (empty) | Comprehensive review |

---

## Review Type Procedures

### A. Self Quality Review (`self`)

Check document completeness and quality:

```markdown
## Self Quality Review Checklist

### 1. Structure Completeness

| Section | Complete | Notes |
|---------|----------|-------|
| 1. One-Line Summary | ✅/❌ | |
| 2. Background & Purpose | ✅/❌ | |
| 3. Goals & KPIs | ✅/❌ | |
| 4. Market Size | ✅/❌ | |
| 5. Customer Understanding | ✅/❌ | |
| 6. Competitive Analysis | ✅/❌ | |
| 7. Solution & USP | ✅/❌ | |
| 8. User Stories | ✅/❌ | |
| 9. Business Model | ✅/❌ | |
| 10. GTM Strategy | ✅/❌ | |
| 11. Product Principles | ✅/❌ | |
| 12. Milestones | ✅/❌ | |
| 13. Risks | ✅/❌ | |
| 14. Open Issues | ✅/❌ | |

### 2. Quality Criteria Check

#### Clarity
- [ ] Are technical terms properly defined?
- [ ] Are sentences clear and easy to understand?
- [ ] Is the logical flow natural?

#### Specificity
- [ ] Are there specific numbers instead of abstract statements?
- [ ] Are sufficient examples provided?
- [ ] Is the target customer clearly defined?

#### Data Quality
- [ ] Are sources cited for all figures?
- [ ] Are assumptions and facts clearly distinguished?
- [ ] Is the data current?

#### Actionability
- [ ] Are next steps clear?
- [ ] Are owners and deadlines assigned?
- [ ] Are there mitigation plans for risks?

### 3. Items Needing Improvement

| Priority | Item | Current State | Improvement Direction |
|----------|------|---------------|----------------------|
| High | | | |
| Medium | | | |
| Low | | | |
```

### B. Peer Review Support (`peer`)

Generate checklist and questions for peer PM review:

```markdown
## Peer Review Guide

### Questions for Reviewers

#### Strategic Alignment
1. Is the case for why this product is needed now sufficiently compelling?
2. Do goals and KPIs align with the vision?
3. Is target customer selection appropriate?

#### Market Analysis
1. Is the TAM/SAM/SOM calculation basis valid?
2. Is competitive landscape analysis sufficient?
3. Is the differentiation point sustainable?

#### Execution Plan
1. Are milestones realistic?
2. Are risks sufficiently considered?
3. Is the GTM strategy appropriate for target customers?

#### Business Model
1. Are Unit Economics assumptions reasonable?
2. Is the pricing strategy appropriate for market and customers?
3. Is the revenue model scalable?

### Feedback Template

```
### Feedback: [Section Name]

**Current State**:
[Summary of relevant document section]

**Concerns**:
[What the problem is]

**Suggestions**:
[How to improve]

**References**:
[Related data or examples]
```
```

### C. Stakeholder Review Support (`stakeholder`)

Prepare customized review materials by stakeholder:

```markdown
## Stakeholder Review Preparation

### Focus by Stakeholder

| Stakeholder | Key Interests | Review Sections |
|-------------|---------------|-----------------|
| CEO/Executives | Strategy alignment, ROI | 1, 2, 3, 12 |
| CFO/Finance | Unit Economics, budget | 4, 9, 12 |
| CTO/Development | Technical feasibility | 7, 8, 12, 13 |
| Marketing | GTM, positioning | 5, 6, 10 |
| Sales | Pricing, competition | 6, 7, 9 |
| Legal | Regulations, risks | 13, 14 |

### Executive Briefing Summary

```
## Executive Summary

**One-Line Summary**:
[One-line summary from 6-Pager]

**Key Opportunities**:
- [Opportunity 1]
- [Opportunity 2]

**Required Investment**:
- [Resource 1]
- [Resource 2]

**Key Risks**:
- [Risk 1]
- [Risk 2]

**Request**:
- [Items needing approval/decision]
```

### Review Meeting Agenda

1. **Introduction** (5 min)
   - Product overview
   - Review purpose

2. **Key Content Presentation** (15 min)
   - Problem definition
   - Solution overview
   - Market opportunity

3. **Q&A and Feedback** (20 min)
   - Department questions
   - Discuss concerns

4. **Next Steps** (5 min)
   - Feedback incorporation plan
   - Approval timeline
```

### D. Comprehensive Review (Empty Input)

Review document from all perspectives:

```markdown
## Comprehensive Review Results

### Overall Assessment

| Area | Score | Evaluation |
|------|-------|------------|
| Strategic Alignment | /10 | |
| Market Analysis | /10 | |
| Customer Understanding | /10 | |
| Competitive Analysis | /10 | |
| Execution Plan | /10 | |
| **Total** | /50 | |

### Strengths

1. **[Strength 1]**: [Description]
2. **[Strength 2]**: [Description]

### Needs Improvement

1. **[Improvement 1]**: [Description] (Priority: High)
2. **[Improvement 2]**: [Description] (Priority: Medium)

### Assumptions to Validate

| Assumption | Importance | Validation Method | Owner |
|------------|------------|-------------------|-------|
| | High | | |
| | Medium | | |

### Review Readiness

- [ ] Self quality review completed
- [ ] Peer review completed
- [ ] Data sources verified
- [ ] Open issues organized

### Recommended Next Steps

1. [Next step 1]
2. [Next step 2]
```

---

## Feedback Integration

Organize feedback received after review:

```markdown
## Feedback Integration

### Received Feedback Summary

| Reviewer | Section | Feedback | Action | Reason |
|----------|---------|----------|--------|--------|
| | | | Will incorporate | |
| | | | Will incorporate | |
| | | | Won't incorporate | [Reason] |

### Incorporation Plan

| Item | Priority | Owner | Due Date |
|------|----------|-------|----------|
| | High | | |
| | Medium | | |

### Next Steps

1. `/spec-mix.refine` - Incorporate feedback
2. Additional review meeting (if needed)
3. Request final approval
```
