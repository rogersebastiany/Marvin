# Tautological Tool

A tool whose input/output contract is complete and unambiguous -- given valid input, there is exactly one correct output. The tool returns the right answer or reports that it cannot answer. There is no third option.

---

## In the POC

| Tool | Tautological? | Contract |
|---|---|---|
| `search_docs(query)` | **Yes** | Substring search -> finds or "No results found" |
| `list_docs()` | **Yes** | Lists filesystem -> return is the actual state |
| `get_doc(filename)` | **Yes** | Reads file -> content or "not found" |
| `save_as_doc(url, filename)` | **Yes** | HTTP + save -> success or error |
| `crawl_docs(url, max_pages)` | **Yes** | Crawl + save -> success or error |
| `batch_convert(urls)` | **Yes** | Multiple HTTP + save -> partial or total success |
| `save_diagram(code, filename)` | **Yes** | Writes file -> success or error |
| `get_diagram(filename)` | **Yes** | Reads file -> content or "not found" |
| `list_diagrams()` | **Yes** | Lists filesystem -> return is the actual state |
| `generate_prompt(...)` | **Partial** | 6-section framework constrains, but output is generated |
| `generate_diagram(...)` | **Partial** | Syntax refs constrain, but output is generated |
| `judge_diagram(...)` | **Partial** | Numeric score, but judgment involves inference |
| `refine_prompt(...)` | **Partial** | Framework constrains, but refinement is generated |

## Pattern: Read Is Tautological, Write Is Partial

Tools that **read** existing data (search, list, get) are tautological by nature -- the output is the actual data or "does not exist". Tools that **generate** content (generate, refine, judge) are partially tautological -- frameworks constrain the output space but do not close it completely.

The [[Transformer-Driven Prompt Architect]] (6 mandatory sections) and [[Diagram Scoring]] (4 numeric dimensions) are mechanisms that **approximate** partial tools to tautology. The more constrained the framework, the more tautological the tool.

## Why It Matters

The [[DFAH]] shows null correlation (r = -0.11) between [[Determinism]] and accuracy in agents with generic tools. But with tautological tools, determinism **implies** accuracy -- the tool can only return truth or "I don't know".

This is the thesis defense against the DFAH's most provocative finding. The r = -0.11 measures the general case. The [[Ontological Tautology]] operates in the case where tools are tautological and the [[Ontology as Code|ontology]] is complete.

## Completeness = Coverage

The [[Ontology as Code|ontology]] is complete when every method in the domain has a corresponding tautological tool. Verifiable:
1. Enumerate the domain's methods/processes
2. Does each have a tool? -> coverage
3. Is each tool tautological? -> quality

If yes for all -> [[Tautology]] by construction.

---

Related to: [[Tool as Bias]], [[DFAH]], [[Measurable Determinism]], [[Anti-Hallucination]], [[Ontology as Code]], [[Transformer-Driven Prompt Architect]], [[Diagram Scoring]], [[Ontological Tautology — Thesis and Proof]], [[Tool Catalog]]
