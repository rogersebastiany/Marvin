# Determinismo Mensurável

O [[Determinismo]] que pode ser quantificado. O artigo [[DFAH]] demonstra 89-90%+ de determinismo de trajetória quando o [[Contexto]] é estruturado. A POC implementa as condições para esse determinismo.

---

## A Evidência

O [[DFAH]] (Determinism-Faithfulness Assurance Harness) de Raffi Khatchadourian prova empiricamente: agentes LLM com **schema-first architecture** — tools tipadas, parâmetros com tipos explícitos, retornos formatados — atingem 89-90% de determinismo de trajetória.

Três métricas formais:
- **ActDet**: As ações (tool calls) se repetem entre execuções?
- **SigDet**: As assinaturas (tool + parâmetros exatos) se repetem?
- **DecDet**: As decisões de alto nível se repetem?

89% (ActDet) significa: em 100 execuções com o mesmo input e contexto, 89 produzem a mesma sequência de ações. Os 11% restantes são gerenciáveis — detectáveis por testes, code review, observabilidade.

**Sobre r = -0.11**: o DFAH revela correlação nula entre determinismo e acurácia em agentes com tools genéricas. Mas a POC opera com [[Tool Tautológica|tools tautológicas]] — `search_docs` encontra ou retorna "not found", `get_doc` retorna conteúdo ou erro. Quando as tools são tautológicas, determinismo **implica** acurácia. O r = -0.11 não se aplica ao caso da POC.

## Como a POC Atinge Determinismo

A POC implementa exatamente a **schema-first architecture** que o DFAH identifica como produtora dos 89%+:

**Schema-first tools:** Cada [[Primitivas MCP|tool]] tem descrição precisa, parâmetros tipados via Python type hints, retornos formatados. `@mcp.tool()` do [[FastMCP]] com type hints é literalmente o padrão schema-first. O [[Agente na POC|agente]] não opera no vácuo — opera com [[Ontologia como Código|ontologia]] servida via contratos tipados.

**Tools definidas:** As 15+ tools dos 4 servers formam um [[Catálogo de Tools]] completo. O agente sabe o que pode e o que não pode fazer. Cada descrição de tool é um [[Tool como Bias|bias vetorial]] que restringe o [[Espaço Amostral]].

**Specs implícitas:** As docstrings de cada tool são specs de comportamento. `"Search across all documentation files for a keyword or phrase. Returns matching lines with surrounding context and filenames."` é uma spec. É o contrato do schema-first.

**Framework estruturado:** O [[Transformer-Driven Prompt Architect]] com 6 seções mandatórias garante que cada prompt gerado é estruturado, não ad-hoc.

**Métrica de avaliação:** Para domínios regulados, a métrica correta é **pass^k** (todas as tentativas devem ter sucesso), não pass@k (pelo menos uma). A distância entre pass@k e pass^k revela a variância real do sistema.

## O "+" do 89%+

O artigo [[Ultra-Long-Horizon Agentic Science]] mostra que determinismo cresce com [[Acumulação Cognitiva]] — não agregação linear de contexto, mas destilação progressiva em três camadas (L1 experiência → L2 conhecimento → L3 sabedoria). 56.44% medal rate no MLE-Bench, SOTA.

Na POC, o [[Feedback Loop Determinístico]] implementa essa acumulação: cada `crawl_docs` expande `docs/`, cada `save_diagram` expande `diagrams/`. O corpus cresce, o determinismo cresce.

O [[RAG Implícito]] fecha o ciclo: conhecimento persistido entre sessões → contexto mais rico na próxima sessão → determinismo maior.

## Complemento: O Artigo [[LLM Output Drift]]

O mesmo autor demonstra o inverso: sem contexto rígido, a IA varia respostas mesmo com temperatura zero. Modelos maiores (100B+, Tier 3) driftam mais — apenas 12.5% de consistência. Tarefas [[RAG Implícito|RAG]] são as mais sensíveis a drift. A busca em `docs/` é exatamente uma tarefa RAG — o que torna o contexto estruturado ainda mais crítico.

A POC ataca o drift pela raiz — não ajustando o modelo, mas enriquecendo o contexto via schema-first tools.

## Complemento: [[Deterministic Trajectory Optimization]]

O mesmo padrão em outro domínio: começa probabilístico, enriquece com informação estruturada, converge pro determinístico. Na POC: o agente começa sem docs, enriquece via crawl, converge para respostas determinísticas.

---

Relaciona-se com: [[Determinismo]], [[DFAH]], [[LLM Output Drift]], [[Ultra-Long-Horizon Agentic Science]], [[Deterministic Trajectory Optimization]], [[Feedback Loop Determinístico]], [[Catálogo de Tools]], [[Transformer-Driven Prompt Architect]], [[RAG Implícito]], [[Drift]], [[Acumulação Cognitiva]], [[FastMCP]], [[Tool como Bias]], [[Tool Tautológica]]
