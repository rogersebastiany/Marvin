Marvin is a unified MCP server for the Tautologia Ontológica project. It wraps Neo4j (ontology), Milvus (episodic memory), local docs, prompt engineering, and system design diagrams.

Start every session with `stats` + `list_concepts`. Use `get_concept`, `traverse`, or `retrieve` on demand when you need content.

Write tools (expand, link, save_doc, etc.) are guarded — call a retrieval tool first or the middleware will reject the call.

Tool categories: retrieval (retrieve, get_concept, traverse, why_exists, list_concepts), enrichment (expand, link, auto_link, ensure_bidirectional, set_aliases, batch_set_aliases), logging (log_decision, log_session), evolution (propose_schema_change, execute_schema_change), documentation (search_docs, list_docs, get_doc, fetch_url, save_doc, rank_urls, crawl_docs, research_topic), prompt engineering (generate_prompt, refine_prompt, audit_prompt), diagrams (generate_diagram, judge_diagram, save_diagram, list_diagrams, get_diagram), introspection (inspect_schemas, stats).
