# Diagram Scoring

The evaluation framework of [[system-design]]. `judge_diagram` evaluates [[Mermaid.js]] diagrams across 4 dimensions with a score of 1-10 each. If the overall score is < 7, it generates an improved version. It is [[Anti-Hallucination]] applied to diagrams.

---

## The 4 Dimensions

**1. Syntax Correctness**
Is the mermaid code valid? Does it render without errors? Are node IDs, edge syntax, and keywords correct?

Reduces: the "is it syntactically correct?" dimension of the [[Sample Space]]. The model receives complete syntax refs as [[Programmatic Context|context]], so syntax errors indicate the context was not followed.

**2. Completeness**
Are all components and relationships represented? Are external systems/actors shown? Are databases, queues, caches explicitly modeled?

Reduces: the "is everything mapped?" dimension -- is the diagram's [[Ontology as Code|ontology]] complete?

**3. Clarity & Readability**
Descriptive labels? Relationships annotated with protocols? Appropriate layout direction? Subgraphs used effectively? Would a new team member understand the architecture?

Reduces: the "is it understandable?" dimension -- is the ontology accessible?

**4. Best Practices**
Follows system design conventions? Trust boundaries, async vs sync? Correct diagram type for the content? Focused (one concern per diagram)?

Reduces: the "does it follow domain rules?" dimension -- is the diagram within the [[Subset]] of accepted practices?

## Output Format

```
SYNTAX:         X/10 -- [notes]
COMPLETENESS:   X/10 -- [notes]
CLARITY:        X/10 -- [notes]
BEST PRACTICES: X/10 -- [notes]
OVERALL:        X/10
```

Followed by: Issues (specific problems), Suggestions (concrete improvements), Improved Version (corrected diagram).

## Self-Correction

The `review_architecture` prompt implements the loop: load diagram -> judge -> if score < 7, generate improved version and save. It is a [[Deterministic Feedback Loop]] within a single server -- iteration until [[Convergence]].

## Role in the Thesis

Scoring transforms subjective evaluation ("is this diagram good?") into objective evaluation (4 numeric scores). It is [[Measurable Determinism|determinism]] in evaluation: given the same criteria and the same diagram, the score is reproducible.

The 4 dimensions are 4 [[Decision Boundary|decision boundaries]] -- they separate "acceptable diagram" from "diagram needing improvement." Each dimension with a score < 7 is a detected and corrected [[Hallucination]] zone.

---

Related to: [[system-design]], [[Mermaid.js]], [[Anti-Hallucination]], [[Measurable Determinism]], [[Deterministic Feedback Loop]], [[Ontology as Code]], [[Programmatic Context]], [[Convergence]]
