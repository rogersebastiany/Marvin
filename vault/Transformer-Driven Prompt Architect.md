# Transformer-Driven Prompt Architect

Framework do [[prompt-engineer]] para gerar prompts estruturados. 6 seções mandatórias, cada uma atacando uma dimensão do [[Espaço Amostral]]. Baseado nos princípios matemáticos do Transformer: Constant Path Length da Attention, Multi-Head Attention, e Attention Masking.

---

## Princípios Matemáticos

**Constant Path Length O(1):** O mecanismo de attention do Transformer conecta quaisquer dois tokens com o mesmo custo computacional. O framework explora isso com cross-references explícitas — tags como `[RULE_1]` que ligam constraints a blocos de execução. O modelo não precisa "procurar" a conexão; ela está explícita.

É o mesmo princípio do [[MCP]]: endereçamento indireto O(1). No prompt, as cross-references são o MCP interno do texto.

**Multi-Head Attention:** Distribuir a tarefa por múltiplos "Expert Heads" — Security, Performance, Cost. Cada head opera num subspace diferente do attention. Na seção 1 (ROLE & PERSPECTIVES), múltiplos personas capturam subspaces diferentes do problema.

**Attention Masking (Constraints Negativos):** Definir "Forbidden Zones" que impedem o modelo de atender a padrões legados ou inseguros. Na seção 5 (ATTENTION MASK), o "DO NOT" list é um mask literal — bloqueia regiões do [[Espaço Amostral]].

## As 6 Seções Mandatórias

| Seção | O que define | Dimensão que reduz |
|---|---|---|
| 1. ROLE & PERSPECTIVES | Personas expert com "Attention Heads" | Quem responde |
| 2. KNOWLEDGE BEYOND WEIGHTS (MCP) | Instruções de quando/como usar [[Primitivas MCP\|tools]] | O que consultar |
| 3. THE GOLDEN PATTERNS (FEW-SHOTS) | Mínimo 2 exemplos Input → Reasoning → Output | Como se parece o correto |
| 4. EXECUTION PIPELINE (CoT) | Chain of Thought passo-a-passo | Como raciocinar |
| 5. ATTENTION MASK (CONSTRAINTS) | Lista de "DO NOT" | O que não fazer |
| 6. FINAL TASK | Trigger específico para iniciar | O que fazer agora |

Cada seção é uma operação de [[Redução de Espaço na Prática|redução]] no [[Espaço Amostral]]: seção 1 restringe o espaço de "quem", seção 2 de "com quê", seção 3 de "como se parece", seção 4 de "como pensar", seção 5 de "o que evitar", seção 6 de "o que fazer."

## Injeção do [[Catálogo de Tools]]

A seção 2 (KNOWLEDGE BEYOND WEIGHTS) é onde o catálogo auto-descoberto é injetado. O prompt gerado diz ao modelo: "estas tools existem no workspace, use-as na seção MCP do prompt que você está gerando." É meta-contexto — [[Contexto Programático|contexto]] sobre como dar contexto.

## Papel na Tese

O framework é uma formalização de como montar [[Contexto]] que maximiza [[Determinismo Mensurável|determinismo]]. Cada seção ataca uma fonte de [[Drift]]:
- Sem role → drift de persona (quem está respondendo?)
- Sem few-shots → drift de formato (como deveria ser a resposta?)
- Sem constraints → drift de escopo (o que é proibido?)

Com todas as 6 seções preenchidas, o prompt é a [[Ontologia]] da tarefa — completa o suficiente para que a resposta seja quase [[Tautologia|tautológica]].

---

Relaciona-se com: [[prompt-engineer]], [[Catálogo de Tools]], [[Contexto Programático]], [[Anti-Alucinação]], [[Redução de Espaço na Prática]], [[Determinismo Mensurável]], [[MCP]], [[Primitivas MCP]], [[Espaço Amostral]], [[Drift]]
