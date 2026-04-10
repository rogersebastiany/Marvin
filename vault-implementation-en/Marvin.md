# Marvin

The unified MCP server that implements [[Ontological Tautology]] in practice. A single process (`marvin_server.py`) exposing 35 tautological tools to the [[Agent in POC|agent]] via [[MCP]].

---

## Architecture

Marvin unifies 6 backend modules into a single [[FastMCP]] server:

| Module | Backend | Purpose |
|---|---|---|
| `ontology.py` | [[Neo4j]] | Knowledge graph — concepts, relations, traversal |
| `memory.py` | [[Milvus]] | Episodic memory — decisions, sessions |
| `docs_backend.py` | [[docs-server]] | Local docs search and reading |
| `web_to_docs_backend.py` | [[web-to-docs]] | Web → markdown → docs/ |
| `prompt_engineer_backend.py` | [[prompt-engineer]] | Transformer-Driven Prompt Architect framework |
| `system_design_backend.py` | [[system-design]] | Mermaid.js diagrams |

## Middleware

The `RetrieveBeforeActMiddleware` implements [[Architectural Enforcement]]: blocks write tools unless a [[Milvus]] search happened first. It's not "please search first" — it's "cannot write without searching."

## Dynamic Identity

Marvin's identity is not a static file. It's built dynamically from the [[Neo4j]] knowledge graph via `self_description`:

1. Startup: check `self_description` cache in [[Milvus]]
2. Cache hit → use cached prompt
3. Cache miss → build from thesis vault + code introspection → cache in [[Milvus]]

## Self-Audit

`self_audit.py` compares code AST against the knowledge graph. Pure [[Set Theory]] operations — zero LLM tokens. Detects drift between what the code IS and what the [[Ontology]] CLAIMS it is.

## [[Tool Catalog]]

35 tools across 8 categories. Each tool is a [[Tautological Tool]] — returns verified data or fails explicitly. Never invents.

---

Relates to: [[Neo4j]], [[Milvus]], [[docs-server]], [[web-to-docs]], [[prompt-engineer]], [[system-design]], [[Tool Catalog]], [[Tautological Tool]], [[Architectural Enforcement]], [[Anti-Hallucination]], [[Self-Improvement Loop]], [[Ontology as Code]], [[Programmatic Context]], [[ReAct in POC]]
