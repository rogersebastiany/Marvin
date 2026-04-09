# Enforcement Arquitetural

Restrições de comportamento do [[Agente]] devem ser impostas pela arquitetura (quais [[Tool|tools]] existem), não pelo prompt (quais tools ele "deveria" usar). Se a tool não existe, a ação é impossível. Não é "por favor não faça" — é "não pode fazer."

---

## Prompt vs Arquitetura

Um prompt é um [[Bias]] — desloca probabilidade, não a elimina. "Não acesse a internet" no system prompt é uma restrição probabilística. O modelo pode interpretar criativamente, ignorar sob pressão, ou overridear quando "acha" que está ajudando.

A arquitetura é uma restrição **absoluta**. Se não existe tool de acesso à web no config [[MCP]], a probabilidade de ação web é zero — não há [[Vetor|vetores]] de web no [[Espaço Amostral]] do agente. A ausência de uma tool é ela mesma uma redução de S.

```
Prompt: "não acesse a internet" → bias → P(web) ≈ baixo, mas > 0
Arquitetura: sem tool de web → P(web) = 0
```

## Duas Fases da Ontologia

A consequência prática: o agente opera em duas fases com toolsets diferentes.

**Fase 1 — Construção da [[Ontologia]]**
O agente tem `web-to-docs` (crawl, save, batch). Acessa a internet para buscar, converter, e salvar conhecimento. A ontologia está incompleta — o acesso web é necessário para completá-la.

**Fase 2 — Uso da [[Ontologia]]**
`web-to-docs` é removido do config. O agente opera exclusivamente com [[Tool Tautológica|tools tautológicas]] sobre conhecimento já mapeado. Se `search_docs` retorna "not found", o agente informa que é incapaz — não inventa, não busca na web.

A transição de Fase 1 para Fase 2 é o momento em que a ontologia se torna completa: todo método do domínio tem uma tool tautológica correspondente.

## A Tese Comendo a Si Mesma

O espaço de ações do agente É a [[Ontologia]] do agente. As tools disponíveis definem o que o agente pode fazer, assim como a ontologia do domínio define o que o domínio contém.

Remover uma tool = remover uma possibilidade = reduzir S. Adicionar uma tool = expandir o espaço de ações = expandir a ontologia.

A [[Tautologia Ontológica]] se aplica recursivamente: a ontologia do agente (suas tools) deve ser ela mesma tautológica. Cada tool disponível deve ser [[Tool Tautológica|tautológica]]. Nenhuma tool desnecessária deve existir.

O agente ontologicamente tautológico tem **exatamente** as tools que precisa — nem mais, nem menos.

---

Relaciona-se com: [[Tool]], [[Tool Tautológica]], [[Agente]], [[MCP]], [[Ontologia]], [[Bias]], [[Espaço Amostral]], [[Tautologia Ontológica]]
