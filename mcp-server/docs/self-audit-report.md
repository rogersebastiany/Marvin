# Marvin Self-Audit Report

Generated: 2026-04-10 18:40 UTC

## Summary

- **Code tools**: 35
- **Canonical MARVIN_TOOLS list**: 35
- **KG concepts**: 140
- **KG relations**: 2080
- **Backend modules**: 7

## Findings

No drift detected. Code and ontology are aligned.

## Code Structure

### Tools (35)

- `audit_prompt` [always-allowed]
- `auto_link` [guarded]
- `batch_set_aliases` [guarded]
- `crawl_docs` [guarded]
- `ensure_bidirectional` [guarded]
- `execute_schema_change` [guarded]
- `expand` [guarded]
- `fetch_url` [always-allowed]
- `generate_diagram` [guarded]
- `generate_prompt` [guarded]
- `get_concept` [retrieval]
- `get_diagram` [always-allowed]
- `get_doc` [retrieval]
- `get_memory` [retrieval]
- `inspect_schemas` [retrieval]
- `judge_diagram` [always-allowed]
- `link` [guarded]
- `list_concepts` [retrieval]
- `list_diagrams` [always-allowed]
- `list_docs` [retrieval]
- `log_decision` [always-allowed]
- `log_session` [always-allowed]
- `propose_schema_change` [always-allowed]
- `rank_urls` [always-allowed]
- `refine_prompt` [guarded]
- `research_topic` [guarded]
- `retrieve` [retrieval]
- `save_diagram` [guarded]
- `save_doc` [guarded]
- `search_docs` [retrieval]
- `self_description` [retrieval]
- `set_aliases` [guarded]
- `stats` [retrieval]
- `traverse` [retrieval]
- `why_exists` [retrieval]

### Backends (7)

- **docs_backend**: search_docs, list_docs, get_doc_summary, read_doc
- **marvin_server**: build_self_description, get_concept, traverse, why_exists, list_concepts, get_memory, set_aliases, batch_set_aliases, log_decision, log_session, expand, link, auto_link, ensure_bidirectional, propose_schema_change, execute_schema_change, search_docs, list_docs, get_doc, fetch_url, save_doc, rank_urls, generate_prompt, refine_prompt, audit_prompt, generate_diagram, judge_diagram, save_diagram, list_diagrams, get_diagram, inspect_schemas, stats, self_description
- **memory**: search_tool_calls, search_decisions, search_sessions, log_tool_call, log_decision, log_session, search_doc_chunks, search_concepts_semantic, index_docs, index_concepts, save_self_description, get_cached_self_description, ensure_collections, get_schema
- **ontology**: query, set_aliases, batch_set_aliases, get_concept, traverse, why_exists, expand, auto_link, ensure_bidirectional, run_cypher, get_vault_concepts, list_concepts, get_stats, get_schema
- **prompt_engineer_backend**: generate_prompt, refine_prompt, audit_prompt
- **system_design_backend**: generate_diagram, judge_diagram, save_diagram, list_diagrams, get_diagram
- **web_to_docs_backend**: rank_urls, convert_url, save_as_doc, batch_convert, crawl_docs, research_topic

### Middleware

- `RetrieveBeforeActMiddleware`

### Always-Allowed Tools (not in RETRIEVAL or GUARDED)

- `audit_prompt`
- `fetch_url`
- `get_diagram`
- `judge_diagram`
- `list_diagrams`
- `log_decision`
- `log_session`
- `propose_schema_change`
- `rank_urls`

## KG Claims

### Marvin Node
- Vault: implementation
- Summary: O servidor MCP unificado que implementa a Tautologia Ontológica na prática. Um único processo (`marvin_server.py`) que expõe 35 tools tautológicas ao Agente na POC via MCP.

### Marvin Relations (32)

- —[CONTRADICTS]→ Alucinação
- —[IMPLEMENTS]→ Agente
- —[IMPLEMENTS]→ Contexto
- —[IMPLEMENTS]→ Mermaid.js
- —[IMPLEMENTS]→ ReAct
- —[IMPLEMENTS]→ Tautologia
- —[IMPLEMENTS]→ Tool
- —[IMPLEMENTS]→ Transformer-Driven Prompt Architect
- —[IMPLEMENTS]→ milvus
- —[PROVES]→ Conjunto
- —[PROVES]→ Drift
- —[RELATES_TO]→ Agente na POC
- —[RELATES_TO]→ Anti-Alucinação
- —[RELATES_TO]→ Catálogo de Tools
- —[RELATES_TO]→ Contexto Programático
- —[RELATES_TO]→ Enforcement Arquitetural
- —[RELATES_TO]→ FastMCP
- —[RELATES_TO]→ Loop de Auto-Melhoria
- —[RELATES_TO]→ MCP
- —[RELATES_TO]→ Milvus
- —[RELATES_TO]→ Neo4j
- —[RELATES_TO]→ Ontologia
- —[RELATES_TO]→ Ontologia como Código
- —[RELATES_TO]→ ReAct na POC
- —[RELATES_TO]→ Tautologia Ontológica
- —[RELATES_TO]→ Teoria dos Conjuntos
- —[RELATES_TO]→ Tool Tautológica
- —[RELATES_TO]→ docs-server
- —[RELATES_TO]→ mcp-memory-server
- —[RELATES_TO]→ prompt-engineer
- —[RELATES_TO]→ system-design
- —[RELATES_TO]→ web-to-docs

---
*Self-audit script: `mcp-server/self_audit.py`*