---
description: Validate research quality through systematic review and bias checking
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Purpose

Perform systematic validation of the research to ensure quality, identify biases, and verify that conclusions are properly supported by evidence.

## Prerequisites

- `findings.md` should be complete
- `analysis.md` should exist
- `bibliography.md` should be complete

## Execution Flow

### 1. Load All Artifacts

Read:
- `research-question.md`
- `methodology.md`
- `literature-review.md`
- `analysis.md`
- `findings.md`
- `bibliography.md`
- All `evidence/Q#/summary.md` files

### 2. Evidence Traceability Check

Verify every claim in findings.md traces to evidence:

```markdown
## Evidence Traceability Audit

| Finding | Claim | Evidence ID | Source | Verified |
|---------|-------|-------------|--------|----------|
| F1 | [claim text] | E-01, E-03 | S01, S04 | [Yes/No] |
| F1 | [claim text] | E-05 | S07 | [Yes/No] |
| F2 | [claim text] | E-02 | S02 | [Yes/No] |

### Unsupported Claims Found
- [List any claims without evidence]

### Evidence Not Used
- [List collected evidence not referenced]
```

### 3. Source Quality Audit

Review bibliography quality:

```markdown
## Source Quality Audit

### Quality Distribution
| Rating | Count | Percentage | Threshold | Status |
|--------|-------|------------|-----------|--------|
| A | [#] | [%] | ≥30% | [Pass/Fail] |
| B | [#] | [%] | ≥40% | [Pass/Fail] |
| C | [#] | [%] | ≤30% | [Pass/Fail] |

### Critical Findings Check
For each High-confidence finding, verify A-rated source support:

| Finding | Confidence | A-rated Sources | Status |
|---------|------------|-----------------|--------|
| F1 | High | S01, S05 | Pass |
| F2 | High | None | FAIL - downgrade |
```

### 4. Bias Detection

Check for common research biases:

```markdown
## Bias Assessment

### Confirmation Bias
- [ ] Contradicting evidence was actively sought
- [ ] Contradicting evidence is acknowledged in findings
- [ ] Alternative interpretations were considered

**Issues Found**: [None / List issues]

### Selection Bias
- [ ] Source selection criteria documented
- [ ] Sources represent diverse perspectives
- [ ] No systematic exclusion of viewpoints

**Issues Found**: [None / List issues]

### Recency Bias
- [ ] Foundational/older sources included
- [ ] Not over-relying on newest sources only

**Issues Found**: [None / List issues]

### Authority Bias
- [ ] Claims evaluated on evidence, not just source prestige
- [ ] Contradictions from lesser sources considered

**Issues Found**: [None / List issues]

### Availability Bias
- [ ] Effort made to find non-obvious sources
- [ ] Paywalled/restricted sources acknowledged if relevant

**Issues Found**: [None / List issues]
```

### 5. Logic Validation

Check reasoning quality:

```markdown
## Logic Validation

### Conclusion Support Check
For each conclusion, verify logical connection:

| Conclusion | Supporting Evidence | Logic Valid | Issues |
|------------|---------------------|-------------|--------|
| [C1] | E-01, E-03, E-05 | Yes | None |
| [C2] | E-02 | Weak | Single source |

### Logical Fallacies Check
- [ ] No false causation (correlation ≠ causation)
- [ ] No hasty generalization (small sample → broad claim)
- [ ] No appeal to authority without evidence
- [ ] No straw man (misrepresenting sources)
- [ ] No cherry-picking (selective evidence use)

**Fallacies Found**: [None / List with locations]
```

### 6. Completeness Check

Verify research question coverage:

```markdown
## Completeness Check

### Research Question Coverage
| Question | Addressed | Evidence | Confidence Stated | Status |
|----------|-----------|----------|-------------------|--------|
| Primary | Yes/No | [IDs] | Yes/No | [Pass/Fail] |
| Q1 | Yes/No | [IDs] | Yes/No | [Pass/Fail] |
| Q2 | Yes/No | [IDs] | Yes/No | [Pass/Fail] |

### Missing Elements
- [ ] All questions addressed
- [ ] All methodology steps completed
- [ ] All limitations documented
- [ ] All contradictions addressed
```

### 7. Confidence Calibration

Review confidence levels:

```markdown
## Confidence Calibration

| Finding | Stated Confidence | Evidence Quality | Source Count | Recommended |
|---------|-------------------|------------------|--------------|-------------|
| F1 | High | A: 2, B: 1 | 3 | High (correct) |
| F2 | High | A: 0, B: 2 | 2 | Medium (downgrade) |
| F3 | Medium | A: 1, B: 2 | 3 | Medium (correct) |

### Adjustments Needed
- [List any confidence levels that should change]
```

### 8. Generate Validation Report

Create `FEATURE_DIR/validation-report.md`:

```markdown
# Validation Report: [TOPIC]

## Overall Assessment
**Status**: [PASS / PASS WITH ISSUES / NEEDS REVISION]

## Summary Metrics
- Evidence traceability: [%] claims verified
- Source quality: [%] A+B rated
- Bias checks: [#]/[#] passed
- Logic validation: [#]/[#] passed
- Completeness: [#]/[#] questions addressed

## Issues Found

### Critical (Must Fix)
1. [Issue description]
   - Location: [Where in findings]
   - Fix: [Recommended action]

### Important (Should Fix)
1. [Issue description]

### Minor (Consider Fixing)
1. [Issue description]

## Confidence Adjustments
[List any recommended changes]

## Recommendations
1. [Action needed]
2. [Action needed]

## Validation Checklist
- [ ] All claims traceable to evidence
- [ ] Source quality meets threshold
- [ ] No major biases detected
- [ ] Logic is sound
- [ ] All questions addressed
- [ ] Confidence levels appropriate
- [ ] Limitations documented

## Validator Notes
[Any additional observations]
```

## Output

Report:
- Overall validation status
- Issues found by severity
- Confidence adjustments needed
- Actions required before finalization
- Next step: Address issues or finalize research

## Validation Standards

**PASS**: All critical checks pass, minor issues only
**PASS WITH ISSUES**: No critical issues, some important fixes needed
**NEEDS REVISION**: Critical issues found, cannot finalize
