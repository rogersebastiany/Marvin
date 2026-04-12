# ReAct in the POC

The Reason -> Act -> Observe loop implemented in practice by the [[Agent in POC]]. Each cycle enriches the [[Programmatic Context|context]], reduces the [[Sample Space]], and brings the system closer to [[Measurable Determinism|determinism]].

---

## The Loop

In the thesis, [[ReAct]] is:
1. **Reason:** navigate the [[Sample Space]] and project the plan
2. **Act:** call a [[Tool]] via [[MCP]]
3. **Observe:** incorporate the result as new [[Context]]

In the POC, each tool call from the 4 servers is an "Act." Each returned result is an "Observe." The agent decides the next step (Reason) based on accumulated results.

## Concrete Examples

**Search and research:**
```
Reason: "I need to know about authentication"
Act:    search_docs("authentication")
Observe: "Found 3 matches in architecture.md"
Reason: "I'll read the detail"
Act:    docs://architecture.md
Observe: [full file content]
Reason: "now I can respond based on the docs"
```

**Ontology expansion:**
```
Reason: "I didn't find docs about FastAPI"
Act:    crawl_docs("https://fastapi.tiangolo.com/tutorial/", max_pages=15)
Observe: "Crawled 15 pages, saved to docs/"
Reason: "now I have local docs, I'll search"
Act:    search_docs("dependency injection")
Observe: "Found 5 matches"
```

**Diagram generation:**
```
Reason: "I need to visualize the payment architecture"
Act:    generate_diagram("payment system with API gateway", type="c4container")
Observe: [prompt with syntax refs + guidelines]
Reason: "I'll generate the mermaid and then evaluate"
Act:    judge_diagram(mermaid_code)
Observe: "OVERALL: 6/10 -- missing database, labels unclear"
Reason: "score < 7, I'll improve"
```

## Context Accumulation

Each ReAct cycle adds information to the conversation context. The [[Agent in POC]] operates with:
- Initial context: user prompt + system prompt
- After 1 cycle: + `search_docs` result
- After 2 cycles: + `docs://file.md` content
- After 3 cycles: + `generate_diagram` result

It is [[Space Reduction in Practice|progressive reduction]] -- each observation eliminates possibilities and concentrates the [[Conditional Probability]] on the correct token.

## ReAct + [[Deterministic Feedback Loop]]

The short ReAct (within session) feeds the long feedback loop (across sessions). The `crawl_docs` executed in a ReAct cycle persists in `docs/`. The next session starts with a richer ontology -- [[Implicit RAG]] in action.

The [[Ultra-Long-Horizon Agentic Science]] paper describes this phenomenon: agents maintain strategic coherence in long cycles through accumulation. In the POC, accumulation is concrete: files in `docs/` and `diagrams/`.

---

Related to: [[ReAct]], [[Agent in POC]], [[Server Chain]], [[Programmatic Context]], [[Space Reduction in Practice]], [[Deterministic Feedback Loop]], [[Implicit RAG]], [[Measurable Determinism]], [[Ultra-Long-Horizon Agentic Science]]
