# Marvin

O servidor MCP unificado que implementa a [[Tautologia Ontológica]] na prática. Um único processo (`marvin_server.py`) que expõe 35 tools tautológicas ao [[Agente na POC|agente]] via [[MCP]].

---

## Arquitetura

Marvin unifica 6 módulos backend num único servidor [[FastMCP]]:

| Módulo | Backend | Função |
|---|---|---|
| `ontology.py` | [[Neo4j]] | Knowledge graph — conceitos, relações, traversal |
| `memory.py` | [[Milvus]] | Memória episódica — decisões, sessões |
| `docs_backend.py` | [[docs-server]] | Busca e leitura de docs locais |
| `web_to_docs_backend.py` | [[web-to-docs]] | Web → markdown → docs/ |
| `prompt_engineer_backend.py` | [[prompt-engineer]] | Framework Transformer-Driven Prompt Architect |
| `system_design_backend.py` | [[system-design]] | Diagramas Mermaid.js |

## Middleware

O `RetrieveBeforeActMiddleware` implementa [[Enforcement Arquitetural]]: bloqueia tools de escrita a menos que uma busca no [[Milvus]] tenha ocorrido primeiro. Não é "por favor busque antes" — é "não pode escrever sem buscar."

## Identidade Dinâmica

A identidade do Marvin não é um arquivo estático. É construída dinamicamente a partir do knowledge graph [[Neo4j]] via `self_description`:

1. Startup: verifica cache `self_description` no [[Milvus]]
2. Cache hit → usa prompt cacheado
3. Cache miss → constrói a partir do vault thesis + introspecção de código → cacheia no [[Milvus]]

## Self-Audit

O `self_audit.py` compara o AST do código contra o knowledge graph. Operações de [[Teoria dos Conjuntos]] puras — zero tokens de LLM. Detecta drift entre o que o código É e o que a [[Ontologia]] AFIRMA que ele é.

## [[Catálogo de Tools]]

35 tools em 8 categorias. Cada tool é uma [[Tool Tautológica]] — retorna dados verificados ou falha explicitamente. Nunca inventa.

---

Relaciona-se com: [[Neo4j]], [[Milvus]], [[docs-server]], [[web-to-docs]], [[prompt-engineer]], [[system-design]], [[Catálogo de Tools]], [[Tool Tautológica]], [[Enforcement Arquitetural]], [[Anti-Alucinação]], [[Loop de Auto-Melhoria]], [[Ontologia como Código]], [[Contexto Programático]], [[ReAct na POC]]
