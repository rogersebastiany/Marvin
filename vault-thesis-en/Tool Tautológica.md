# Tautological Tool

A [[Tool]] whose input/output contract is complete and unambiguous. Given a valid input, there exists exactly one correct output. The tool cannot return a wrong answer -- it either returns the correct answer or reports that it cannot answer.

---

## Definition

A tool is tautological when its specification (input types, output format, behavior in edge cases) leaves no room for ambiguity. The result is [[Determinismo|deterministic]] by construction -- true for all possible valuations of the inputs, like a logical [[Tautologia]].

Examples:
- `search_docs("lambda")` -> returns lines containing "lambda" or "No results found". There is no third option.
- `get_doc("architecture.md")` -> returns the file contents or "Document not found". It does not invent content.
- `save_diagram(code, filename)` -> saves the file or returns an error. It does not modify the code.

Counter-example: a tool `answer_question(query)` that generates free text is **not** tautological -- the output space is open.

## Why It Matters

The [[DFAH]] reveals that [[Determinismo]] and accuracy have a null correlation (r = -0.11) in agents with generic tools. A system can be perfectly deterministic and perfectly wrong -- small models (7-8B) prove this.

But this finding applies to tools whose output is ambiguous. When tools are tautological, [[Determinismo]] **implies** accuracy. If the tool can only return the correct answer or "I don't know," and the system is deterministic, the system is deterministically correct.

The null correlation from DFAH measures agents with generic tools. The [[Ontological Tautology]] thesis operates with tautological tools -- a universe where r = -0.11 does not apply.

## Criteria

A tool is tautological when:
1. **Typed input**: Parameters with explicit types, no ambiguity
2. **Finite output**: Output space is closed (enum of possibilities, not free text)
3. **Explicit failure**: When it cannot answer, it returns "not found" / error, never invents
4. **Idempotence**: Same input always produces same output
5. **Complete contract**: Docstring/spec covers all possible behaviors

## In the POC

The POC tools are mostly tautological:

| Tool | Tautological? | Why |
|---|---|---|
| `search_docs` | Yes | Substring search -- finds or does not find |
| `list_docs` | Yes | Lists files -- return is the filesystem |
| `get_doc` | Yes | Reads file -- returns content or "not found" |
| `crawl_docs` | Yes | Does HTTP + saves -- success or error |
| `save_diagram` | Yes | Writes file -- success or error |
| `generate_prompt` | **Partial** | Generates text via LLM -- open output, but 6-section framework constrains |
| `generate_diagram` | **Partial** | Generates Mermaid.js -- semi-open output, but syntax refs constrain |
| `judge_diagram` | **Partial** | Score 0-10 on 4 dimensions -- output is numeric, but judgment involves inference |

The partially tautological tools are those involving generation. The [[Transformer-Driven Prompt Architect]] and [[Scoring de Diagramas]] are mechanisms that approximate these tools toward tautology -- they constrain the output space without fully closing it.

## Complete Ontology = Total Coverage of Tautological Tools

A domain's [[Ontologia]] is complete when **every method/process of the domain has a corresponding tautological tool**. Verifiable: enumerate the methods, verify coverage, confirm that each tool is tautological.

If every tool is tautological and every action in the domain is covered by a tool, the system is tautological by construction -- not by probability.

---

Related to: [[Tool]], [[Tautologia]], [[Determinismo]], [[DFAH]], [[Ontologia]], [[Ontological Tautology]], [[MCP]], [[Contexto]], [[Espaço Amostral]]
