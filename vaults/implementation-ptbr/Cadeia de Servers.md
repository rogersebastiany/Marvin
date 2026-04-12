# Cadeia de Servers

Os 4 MCP servers da POC se complementam numa cadeia de [[Contexto Programático|contexto]] acumulativo. Cada server resolve uma lacuna que o anterior não cobre, e o resultado de um alimenta o próximo.

---

## A Cadeia

```
docs-server ← "o que sabemos?"
     ↕
web-to-docs ← "o que podemos saber?"
     ↓
prompt-engineer ← "como perguntar bem?"
     ↓
system-design ← "como visualizar?"
```

## Fluxo Típico

1. [[Agente na POC]] precisa de informação → chama [[docs-server]] `search_docs("lambda")`
2. Não encontrou → chama [[web-to-docs]] `crawl_docs("https://docs.aws.amazon.com/lambda/...")`
3. web-to-docs salva páginas em `docs/` → agora são pesquisáveis pelo docs-server
4. Agente busca de novo → `search_docs("lambda")` → encontra
5. Agente precisa de um prompt otimizado → [[prompt-engineer]] `generate_prompt("Lambda expert", "cloud")`
6. prompt-engineer injeta o [[Catálogo de Tools]] completo no prompt gerado
7. Agente precisa de diagrama → [[system-design]] `generate_diagram("Lambda with API Gateway")`
8. system-design injeta syntax refs de `docs/mermaid-*.md` no contexto

## Acoplamentos

**docs-server ↔ web-to-docs:** Compartilham `docs/`. web-to-docs escreve, docs-server lê. O diretório `docs/` é o ponto de integração.

**prompt-engineer → todos os 3:** Importa os 3 servers irmãos no startup para construir o [[Catálogo de Tools]]. Acoplamento forte — os 3 devem ser importáveis.

**system-design → docs-server:** Lê `docs/mermaid-*.md` no startup como referência de sintaxe. Depende dos docs existirem.

## Na Tese

A cadeia implementa a redução progressiva do [[Espaço Amostral]]:

1. docs-server: restringe ao que está documentado (A ⊂ S)
2. web-to-docs: expande A e depois restringe com conteúdo verificado
3. prompt-engineer: restringe a forma de perguntar (elimina ambiguidade)
4. system-design: restringe a representação visual (elimina interpretações)

Cada elo é uma operação de interseção na [[Teoria dos Conjuntos]]: A ∩ T₁ ∩ T₂ ∩ T₃ → [[Subconjunto]] preciso → [[Determinismo Mensurável|determinismo]].

É a [[Redução de Espaço na Prática]] materializada em arquitetura de software.

## Evolução: 6 Servers

A cadeia original (4 servers) opera sobre ontologia estática em `docs/`. Dois novos servers adicionam ontologia viva e memória:

```
docs-server ← "o que sabemos?" (texto)
     ↕
web-to-docs ← "o que podemos saber?"
     ↓
prompt-engineer ← "como perguntar bem?"
     ↓
system-design ← "como visualizar?"
     ↕
mcp-ontology-server ← "o que sabemos?" (grafo semântico)
     ↕
mcp-memory-server ← "o que já fizemos?"
```

O [[mcp-ontology-server]] consulta [[Neo4j]] — conceitos e relações como grafo. O [[mcp-memory-server]] consulta [[Milvus]] — tool calls, decisões, e sessões como vetores.

Os dois novos servers habilitam o [[Loop de Auto-Melhoria]]: o agente consulta → age → loga → descobre → enriquece → próximo ciclo mais rico.

---

Relaciona-se com: [[docs-server]], [[web-to-docs]], [[prompt-engineer]], [[system-design]], [[mcp-ontology-server]], [[mcp-memory-server]], [[Feedback Loop Determinístico]], [[Redução de Espaço na Prática]], [[Catálogo de Tools]], [[Agente na POC]], [[Contexto Programático]], [[Loop de Auto-Melhoria]]
