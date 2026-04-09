# mcp-ontology-server

MCP server que expõe o knowledge graph [[Neo4j]] como tools para o [[Agente na POC|agente]]. Permite consultar, traversar, e enriquecer a [[Ontologia como Código|ontologia]].

---

## Tools

| Tool | Descrição |
|---|---|
| `query` | Busca conceitos por nome, tag, ou texto livre |
| `get_concept` | Retorna um conceito completo com suas relações |
| `traverse` | Caminha N hops a partir de um conceito, retornando a vizinhança |
| `why_exists` | Explica por que um conceito existe na ontologia — retorna o reasoning das arestas |
| `expand` | Adiciona novo conceito ou nova relação ao grafo |

## Diferença do docs-server

O [[docs-server]] busca texto em arquivos markdown. O mcp-ontology-server busca **conceitos e relações** num grafo. A diferença:

- `search_docs("determinismo")` → linhas de texto que contêm "determinismo"
- `query("Determinismo")` → o nó Determinismo com suas 11 relações, pesos, e reasoning

O grafo tem semântica que o texto não tem.

## Enriquecimento pelo Agente

O agente pode usar `expand` para adicionar conceitos e relações que descobre durante o trabalho. Se durante uma sessão o agente percebe que "FastMCP implements schema-first architecture", pode criar essa relação no grafo.

As arestas criadas pelo agente têm `discovered_by: "agent"` — distinguíveis das importadas dos vaults (`discovered_by: "vault_import"`).

## Na Cadeia de Servers

O mcp-ontology-server se integra à [[Cadeia de Servers]] existente:

```
Agente precisa entender um conceito → mcp-ontology-server (traverse)
    ↓ conceito tem ghost nodes
Agente preenche gaps → mcp-ontology-server (expand)
    ↓ precisa de docs detalhados
docs-server (search_docs)
    ↓ não encontrou
web-to-docs (crawl_docs) → salva → docs-server encontra
    ↓ atualiza o grafo
mcp-ontology-server (expand)
```

---

Relaciona-se com: [[Neo4j]], [[Ontologia como Código]], [[Cadeia de Servers]], [[docs-server]], [[Loop de Auto-Melhoria]], [[MCP]], [[FastMCP]]
