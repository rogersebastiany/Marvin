# ReAct na POC

O loop Reason → Act → Observe implementado na prática pelo [[Agente na POC]]. Cada ciclo enriquece o [[Contexto Programático|contexto]], reduz o [[Espaço Amostral]], e aproxima o sistema do [[Determinismo Mensurável|determinismo]].

---

## O Loop

Na tese, [[ReAct]] é:
1. **Reason:** navega no [[Espaço Amostral]] e projeta o plano
2. **Act:** chama uma [[Tool]] via [[MCP]]
3. **Observe:** incorpora o resultado como novo [[Contexto]]

Na POC, cada tool call dos 4 servers é um "Act." Cada resultado retornado é um "Observe." O agente decide o próximo passo (Reason) baseado nos resultados acumulados.

## Exemplos Concretos

**Busca e pesquisa:**
```
Reason: "preciso saber sobre autenticação"
Act:    search_docs("authentication")
Observe: "Found 3 matches in architecture.md"
Reason: "vou ler o detalhe"
Act:    docs://architecture.md
Observe: [conteúdo completo do arquivo]
Reason: "agora posso responder com base nos docs"
```

**Expansão de ontologia:**
```
Reason: "não encontrei docs sobre FastAPI"
Act:    crawl_docs("https://fastapi.tiangolo.com/tutorial/", max_pages=15)
Observe: "Crawled 15 pages, saved to docs/"
Reason: "agora tenho docs locais, vou buscar"
Act:    search_docs("dependency injection")
Observe: "Found 5 matches"
```

**Geração de diagrama:**
```
Reason: "preciso visualizar a arquitetura de pagamento"
Act:    generate_diagram("payment system with API gateway", type="c4container")
Observe: [prompt com syntax refs + guidelines]
Reason: "vou gerar o mermaid e depois avaliar"
Act:    judge_diagram(mermaid_code)
Observe: "OVERALL: 6/10 — missing database, labels unclear"
Reason: "score < 7, vou melhorar"
```

## Acumulação de Contexto

Cada ciclo ReAct adiciona informação ao contexto da conversa. O [[Agente na POC]] opera com:
- Contexto inicial: prompt do usuário + system prompt
- Após 1 ciclo: + resultado de `search_docs`
- Após 2 ciclos: + conteúdo de `docs://arquivo.md`
- Após 3 ciclos: + resultado de `generate_diagram`

É [[Redução de Espaço na Prática|redução progressiva]] — cada observação elimina possibilidades e concentra a [[Probabilidade Condicional]] no token correto.

## ReAct + [[Feedback Loop Determinístico]]

O ReAct curto (dentro da sessão) alimenta o feedback loop longo (entre sessões). O `crawl_docs` executado num ciclo ReAct persiste em `docs/`. A próxima sessão já começa com ontologia mais rica — o [[RAG Implícito]] em ação.

O artigo [[Ultra-Long-Horizon Agentic Science]] descreve este fenômeno: agentes mantêm coerência estratégica em ciclos longos através de acumulação. Na POC, a acumulação é concreta: arquivos em `docs/` e `diagrams/`.

---

Relaciona-se com: [[ReAct]], [[Agente na POC]], [[Cadeia de Servers]], [[Contexto Programático]], [[Redução de Espaço na Prática]], [[Feedback Loop Determinístico]], [[RAG Implícito]], [[Determinismo Mensurável]], [[Ultra-Long-Horizon Agentic Science]]
