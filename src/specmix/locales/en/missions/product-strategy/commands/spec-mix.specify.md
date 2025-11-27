---
description: Create a 6-Pager strategic document. Starting from a product idea, systematically complete the strategy document.
---

## User Input

```text
{ARGS}
```

You **MUST** consider the user input above if not empty.

## Overview

This command creates a 6-Pager strategic document from a Product Owner perspective. Following the Amazon-style 6-Pager format, it consists of 14 sections:

1. One-Line Summary
2. Background and Purpose
3. Goals & KPIs
4. Market Size (TAM/SAM/SOM)
5. Customer Understanding (Personas)
6. Competitive Analysis
7. Solution & USP
8. User Stories
9. Business Model
10. GTM Strategy
11. Product Principles
12. Milestones
13. Risks
14. Open Issues

---

## Workflow

### Step 1: Understand Product Idea

If user input is missing or insufficient, ask the following:

```
I'll help you create a 6-Pager strategic document.

Please provide the following information:

1. **Product Name**: Name of your product/service
2. **One-line Description**: What does this product do?
3. **Target Customer**: Who is this product for?
4. **Problem to Solve**: What problem does it solve?
5. **Existing Materials**: (if any) planning docs, research, idea notes, etc.
```

### Step 2: Analyze Existing Materials

Check if there are existing materials in the project:

```bash
# Check for existing strategy documents
ls -la specs/*/6pager.md 2>/dev/null
ls -la docs/*.md 2>/dev/null

# Check for research materials
ls -la specs/*/market-research.md 2>/dev/null
ls -la specs/*/competitor-analysis.md 2>/dev/null
```

If existing materials exist, read and incorporate their content.

### Step 3: Information Gathering Conversation

Collect necessary information for each section through conversation. Don't ask too many questions at once; proceed section by section.

#### 3.1 Background and Purpose Questions

```
## Background and Purpose

1. **Why now** - Why should we build this product now?
   - What market changes are happening?
   - What's become technologically possible?
   - How is customer behavior changing?

2. **What problem** are you trying to solve?
   - What pain points do customers currently experience?
   - What are the limitations of existing solutions?
```

#### 3.2 Goals & KPIs Questions

```
## Goals & KPIs

1. What is your **3-5 year vision**?
   - What does success look like for this product?

2. What are your **measurable goals**?
   - What metrics do you want to achieve in 1 year?
   - (e.g., 100K MAU, 5% conversion rate, NPS 50+)
```

#### 3.3 Market Size Questions

```
## Market Size

1. **What market** are you targeting?
   - How do you define the market scope?

2. Do you have **market size** information?
   - Total Addressable Market (TAM)
   - Serviceable Available Market (SAM)
   - Serviceable Obtainable Market (SOM)

3. What is the **market growth rate**?
```

#### 3.4 Customer Understanding Questions

```
## Customer Understanding

1. Who is your **core target customer**?
   - Age, occupation, characteristics
   - Do you have specific personas?

2. What are the customer's **pain points**?
   - How do they currently solve the problem?
   - What's inconvenient about that approach?

3. What do **customers want**? (JTBD)
   - Functional job to be done
   - Emotional job
   - Social job
```

#### 3.5 Competitive Analysis Questions

```
## Competitive Analysis

1. Who are your **direct competitors**?
   - Products/services solving the same problem

2. What about **indirect competitors or substitutes**?
   - Different approaches meeting the same need

3. What are your **strengths/weaknesses vs competitors**?
```

#### 3.6 Solution & USP Questions

```
## Solution & USP

1. What are the **3-5 core features**?
   - What value does each feature provide to customers?

2. What is your **differentiation point** (USP)?
   - Your unique strength that competitors can't easily copy

3. What is the **MVP scope**?
   - Features that must be in the first version
```

#### 3.7 Business Model Questions

```
## Business Model

1. What is your **revenue model**?
   - Subscription? Ads? Transaction fees? License?

2. What is your **pricing strategy**?
   - Plan structure (Free / Pro / Enterprise)
   - Price points for each plan

3. What are your **Unit Economics targets**?
   - CAC, LTV, LTV:CAC ratio
```

#### 3.8 GTM Strategy Questions

```
## GTM Strategy

1. What is your **launch strategy**?
   - Private Beta → Public Beta → GA plan

2. What is your **initial customer acquisition strategy**?
   - How will you acquire your first customers?

3. What is your **marketing channel** priority?
```

#### 3.9 Milestone Questions

```
## Milestones

1. What are your **key milestones**?
   - Goals and deadlines for each milestone

2. Do you have a **phase-by-phase plan**?
```

#### 3.10 Risk Questions

```
## Risks

1. What are the **biggest risks**?
   - Market, technical, competitive, operational, regulatory

2. What are the **mitigation strategies** for each risk?
```

### Step 4: Generate 6-Pager Document

Based on collected information, generate the 6-Pager document.

1. **Load Template**:
   ```
   .spec-mix/active-mission/templates/6pager-template.md
   ```

2. **Create Directory**:
   ```bash
   mkdir -p specs/strategy
   ```

3. **Write Document**: Fill in each section of the template.
   - Mark unconfirmed information as `[TBD]` or `[To be validated]`
   - Clearly mark assumptions as `[Assumption]`
   - Cite sources for numerical data

4. **Save File**:
   ```
   specs/strategy/6pager.md
   ```

### Step 5: Summarize Items Needing Validation

After writing, summarize and present to user:

```markdown
## Complete

`specs/strategy/6pager.md` has been created.

### Items Requiring Validation

The following items need additional research or validation:

| Section | Item | Validation Method |
|---------|------|-------------------|
| Market Size | TAM/SAM/SOM figures | Review market research reports |
| Competitors | Market share | Competitor analysis |
| Unit Economics | CAC/LTV projections | Benchmark similar services |

### Next Steps

1. `/spec-mix.analyze` - Deep dive market/competitor analysis
2. `/spec-mix.refine` - Improve document based on feedback
3. `/spec-mix.review` - Stakeholder review
```

---

## Writing Guidelines

### Characteristics of a Good 6-Pager

1. **Specific and Measurable**: Concrete numbers and examples instead of abstract statements
2. **Data-Driven**: Distinguish between assumptions and facts, cite sources
3. **Customer-Centric**: Describe from customer value perspective, not technology
4. **Actionable**: Clear action items for next steps
5. **Concise and Clear**: Exclude unnecessary content

### Things to Avoid

- Unfounded optimistic predictions
- Presenting unvalidated assumptions as facts
- Technology-centric descriptions (technology is just a means)
- Underestimating competitors
- Ignoring or avoiding risks

### When Information is Insufficient

- Mark as `[TBD]` and add to validation items
- State assumptions but clearly mark as `[Assumption]`
- Use uncertainty expressions like "estimated to be", "expected to be"
- Specify validation methods and owners

---

## Example: Writing One-Line Summary

**Bad Example**:
> An innovative AI-based platform that leads the industry.

**Good Example**:
> An AI budgeting app for dual-income couples aged 30-40 that automatically categorizes expenses through bank integration and helps achieve monthly savings goals.

**Good Example Characteristics**:
- Specific target customer (dual-income couples aged 30-40)
- Clear description of what it does (AI budgeting app)
- Clear core value (automatic categorization, savings goals)
