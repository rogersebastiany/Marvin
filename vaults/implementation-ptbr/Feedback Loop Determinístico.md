# Feedback Loop Determinístico

O ciclo em que cada interação do [[Agente na POC|agente]] com os [[Cadeia de Servers|servers]] adiciona [[Contexto Programático|contexto]] ao sistema, que por sua vez melhora as próximas interações. O loop só melhora com o tempo — [[Determinismo]] crescente com histórico crescente.

---

## O Loop na POC

```
1. Agente busca info → search_docs("lambda") → não encontrou
2. Agente busca na web → crawl_docs("https://docs.aws.amazon.com/lambda/...") → salva em docs/
3. Agora é buscável → search_docs("lambda") → encontra
4. Agente usa o resultado como contexto para a próxima decisão
```

Cada iteração do loop:
- **Expande a [[Ontologia como Código|ontologia]]**: mais arquivos em `docs/`
- **Reduz o [[Espaço Amostral]]**: mais [[Contexto Programático|contexto]] disponível para futuras buscas
- **Aumenta o [[Determinismo Mensurável|determinismo]]**: menos [[Drift]] porque o conhecimento está mapeado

## Os Dois Loops

**Loop curto (dentro de uma sessão):**
O [[Agente na POC]] opera via [[ReAct na POC|ReAct]] — reason, act (tool call), observe. Cada ciclo enriquece o contexto daquela sessão. `search_docs` → resultado → nova decisão → `generate_diagram` → resultado → decisão melhor.

**Loop longo (entre sessões):**
Documentos salvos por `crawl_docs` e `save_as_doc` persistem em `docs/`. Diagramas salvos por `save_diagram` persistem em `diagrams/`. A próxima sessão do agente já começa com ontologia mais rica. É o [[RAG Implícito]] em ação.

## Sustentação Científica

O artigo [[Ultra-Long-Horizon Agentic Science]] demonstra que agentes mantêm "coerência estratégica" via [[Acumulação Cognitiva]] — o framework HCC com três camadas de memória:

- **L1 (Experience)**: Traces raw de execução — na POC, o output de cada tool call.
- **L2 (Knowledge)**: Julgamentos e insights destilados — na POC, os docs salvos por `crawl_docs` e `save_as_doc`.
- **L3 (Wisdom)**: Estratégias transferíveis entre sessões — na POC, o corpus acumulado em `docs/` e `diagrams/`.

O "+" do 89%+ ([[DFAH]]) vem deste loop. [[Determinismo]] não é estático, cresce com acumulação. O HCC mostra que acumulação linear (concatenar tudo) satura a 200k+ tokens. Acumulação estruturada (destilação L1→L2→L3) mantém ~70k tokens efetivos.

Na POC, a acumulação é concreta: cada `crawl_docs` adiciona páginas, cada `save_diagram` adiciona diagramas. O corpus de [[Ontologia como Código|ontologia]] cresce monotonicamente. O [[Feedback Loop Determinístico]] é o mecanismo de **context promotion** da POC.

## Condição de [[Anti-Alucinação]]

O loop também é uma defesa contra [[Alucinação]]: se a informação não está mapeada, o agente pode buscá-la em vez de inventá-la. O caminho "não encontrou → buscou → salvou" transforma uma potencial alucinação em conhecimento verificado.

---

Relaciona-se com: [[Cadeia de Servers]], [[docs-server]], [[web-to-docs]], [[ReAct na POC]], [[RAG Implícito]], [[Ontologia como Código]], [[Determinismo Mensurável]], [[Anti-Alucinação]], [[Ultra-Long-Horizon Agentic Science]], [[DFAH]], [[Acumulação Cognitiva]]
