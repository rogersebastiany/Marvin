# DFAH

Determinism-Faithfulness Assurance Harness. Artigo de Raffi Khatchadourian (City University of New York) que mede [[Determinismo]] e fidelidade de agentes LLM com ferramentas, revelando que determinismo e acurácia são dimensões independentes.

---

## Referência

**Replayable Financial Agents: A Determinism-Faithfulness Assurance Harness for Tool-Using LLM Agents**
Raffi Khatchadourian — City University of New York
https://arxiv.org/abs/2601.15322

## Contribuição

O artigo introduz um harness "replayable" — grava trajetórias de agentes (sequências de tool calls) e re-executa para medir divergência. Com [[Contexto]] estruturado (schemas tipados, specs, ferramentas definidas), o determinismo de trajetória sobe para 89-90%+.

É a prova empírica central da tese [[Tautologia Ontológica]]: [[Ontologia]] (contexto estruturado) → [[Tautologia]] (resultado previsível) → [[Determinismo]] (89%+).

## Três Métricas Formais

O artigo define três níveis de determinismo, cada um medindo uma granularidade diferente:

- **ActDet** (Action Determinism): As ações (tool calls) são as mesmas entre execuções?
- **SigDet** (Signature Determinism): As assinaturas (qual tool + quais parâmetros) são as mesmas?
- **DecDet** (Decision Determinism): As decisões de alto nível são as mesmas?

SigDet é o mais estrito — exige parâmetros idênticos. DecDet é o mais relaxado — permite variação de implementação desde que a estratégia seja a mesma. Os 89%+ referem-se a ActDet em condições de schema-first.

## pass^k vs pass@k

Duas métricas de avaliação com implicações opostas:

- **pass@k** (otimista): pelo menos 1 de k tentativas tem sucesso. Útil para exploração.
- **pass^k** (conservador): todas as k tentativas têm sucesso. Exigido para reprodutibilidade.

A distância entre pass@k e pass^k revela a variância real. Um sistema com pass@5 = 95% mas pass^5 = 40% parece bom mas é instável. Para domínios regulados (finanças, saúde, direito), pass^k é a métrica que importa.

## O Achado Provocativo: Determinismo ≠ Acurácia

A correlação entre determinismo e acurácia é **nula (r = -0.11)**. Modelos pequenos (7-20B parâmetros) atingem 100% de determinismo a T=0.0, mas acurácia baixa. Modelos frontier mostram determinismo moderado com acurácia variável.

**Porém**: essa correlação nula se aplica a agentes com tools genéricas — tools cujo output é ambíguo ou aberto. Quando as tools são [[Tool Tautológica|tautológicas]] (contrato I/O completo, output finito, falha explícita), determinismo **implica** acurácia. Se a tool só pode retornar a resposta certa ou "não sei", um sistema determinístico é deterministicamente correto.

A tese [[Tautologia Ontológica]] opera nesse universo restrito: tools tautológicas servidas via [[MCP]]. O r = -0.11 mede o caso geral; a tese opera no caso específico onde a correlação é positiva por construção.

## Arquitetura Schema-First

O que produz o 89%+ é especificamente **schema-first architecture**: definições de tools tipadas, parâmetros com tipos explícitos, retornos formatados. Não é "contexto" genérico. É [[Contexto]] estruturado com contratos.

Na prática: `@mcp.tool()` com type hints do [[FastMCP]] é literalmente este padrão. Cada tool da POC com parâmetros tipados e docstrings precisas implementa schema-first.

## Modos de Falha

Stress tests revelam que o determinismo **degrada** sob:
- Falhas de tools (timeout, erro de API)
- Schemas ambíguos (descrições vagas, parâmetros sem tipo)
- Contexto sobrecarregado (muitas tools, informação contraditória)

Os 89% não são incondicionais — exigem manutenção da qualidade do schema e do [[Contexto]].

## Implicação

89-90% de determinismo significa que 11% de indeterminismo é gerenciável. Num contexto de engenharia de software, isso é aceitável — erros podem ser detectados por testes, code review, e observabilidade.

O artigo [[Ultra-Long-Horizon Agentic Science]] mostra que o número pode crescer com [[Acumulação Cognitiva]] — sustentando o "+".

---

Relaciona-se com: [[Determinismo]], [[Ontologia]], [[Tautologia]], [[LLM Output Drift]], [[Ultra-Long-Horizon Agentic Science]], [[Contexto]], [[Tautologia Ontológica]], [[Acumulação Cognitiva]], [[FastMCP]], [[Tool Tautológica]]
