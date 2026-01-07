---
description: Execute systematic search and source discovery using web search and databases
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Purpose

Systematically search for and collect relevant sources to answer the research question. Uses AI web search capabilities to find credible information.

## Prerequisites

- `research-question.md` must exist
- `methodology.md` should exist (recommended)

## Execution Flow

### 1. Load Context

Read:
- `research-question.md` - Questions to answer
- `methodology.md` - Search strategy (if exists)
- `bibliography.md` - Already collected sources

### 2. Prepare Search Queries

For each secondary question, prepare:

**Query Formulation**:
```
Primary: "[main concept] [specific aspect]"
Variations:
- Synonyms: "[alternative term] [aspect]"
- Broader: "[general topic] overview"
- Narrower: "[specific subtopic] [detail]"
```

**Search Operators**:
- Use quotes for exact phrases
- Add site:domain for specific sources
- Add filetype:pdf for papers
- Add year range for currency

### 3. Execute Web Searches

**IMPORTANT**: Use the WebSearch tool for each query.

**Search Sequence**:
1. Start with primary query
2. Review results, note gaps
3. Execute variation queries
4. Search specific domains:
   - `site:arxiv.org` - Academic papers
   - `site:github.com` - Code/implementations
   - `site:medium.com OR site:dev.to` - Technical blogs
   - `site:stackoverflow.com` - Community knowledge

**For Each Search**:
- Execute query via WebSearch
- Review top 10-15 results
- Evaluate relevance and quality
- Record promising sources

### 4. Evaluate Sources

**Quick Assessment Checklist**:
- [ ] Relevant to research question?
- [ ] Author/organization credible?
- [ ] Date acceptable (per methodology)?
- [ ] Evidence-based (not just opinion)?
- [ ] Accessible (not paywalled)?

**Quality Rating**:
- **A**: Peer-reviewed, authoritative source
- **B**: Credible organization, well-cited
- **C**: Informal but informative

### 5. Record Sources

For each valuable source, add to `data-sources.md`:

```markdown
## Source: [Title]

**URL**: [link]
**Type**: [Paper/Article/Documentation/Blog/Report]
**Author**: [name/organization]
**Date**: [publication date]
**Accessed**: [today's date]
**Quality**: [A/B/C]

**Relevance**:
- Addresses: [Q1, Q2, etc.]
- Key topics: [topics covered]

**Summary**:
[2-3 sentence summary of content]

**Key Quotes** (for later citation):
> "[Important quote 1]" (section/page)
> "[Important quote 2]" (section/page)

**Notes**:
[Any observations, limitations, biases noted]
```

### 6. Update Bibliography

Add each source to `bibliography.md`:

```markdown
| ID | Citation | Type | Accessed | Quality | Used In |
|----|----------|------|----------|---------|---------|
| S01 | Author (Year). Title. Source. URL | Paper | 2025-01-07 | A | Q1, Q3 |
```

### 7. Track Coverage

Create coverage matrix:

```markdown
## Search Coverage

| Question | Sources Found | A-rated | B-rated | Gaps |
|----------|---------------|---------|---------|------|
| Q1 | 5 | 2 | 3 | None |
| Q2 | 3 | 1 | 1 | Need more primary sources |
| Q3 | 2 | 0 | 2 | No A-rated sources yet |
```

### 8. Iterate if Needed

**If gaps exist**:
- Refine search queries
- Try alternative terms
- Search different source categories
- Consider expanding scope slightly

**Minimum Requirements**:
- At least 3 sources per secondary question
- At least 1 A-rated source per primary topic
- No question with only C-rated sources

## Output

Report:
- Total sources collected
- Coverage by question
- Quality distribution (A/B/C)
- Identified gaps
- Next step: `/spec-mix.literature` or `/spec-mix.collect`

## Search Tips

**Academic Sources**:
- "systematic review" + topic
- "meta-analysis" + topic
- "[topic] survey paper"

**Technical Sources**:
- "[technology] documentation"
- "[tool] best practices"
- "[framework] architecture"

**Recent Developments**:
- "[topic] 2024" or "[topic] 2025"
- "[topic] latest research"
- "[topic] state of the art"
