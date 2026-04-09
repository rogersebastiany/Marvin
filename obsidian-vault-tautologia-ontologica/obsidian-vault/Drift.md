# Drift

Fenômeno em que o output de um modelo de IA varia mesmo quando as condições aparentes são constantes — mesmo prompt, mesma temperatura, mesmo modelo. A IA "deriva" do resultado esperado.

---

## Definição Formal

O artigo [[LLM Output Drift]] define drift como a variação não-intencional de respostas de LLMs em workflows repetíveis, especialmente em contextos financeiros onde reprodutibilidade é crítica.

Drift ocorre por múltiplas causas: mudanças internas no modelo (atualizações silenciosas), diferenças de precisão numérica entre providers, variações de batching, e fundamentalmente — insuficiência de [[Contexto]].

## Relação Inversa com Contexto

Drift é inversamente proporcional à completude da [[Ontologia]]:

- [[Contexto]] pobre → espaço de decisão amplo → muitos tokens candidatos → alta variação → drift
- [[Contexto]] rico → espaço de decisão restrito → poucos candidatos → baixa variação → [[Determinismo]]

É a mesma relação que existe entre [[Divergência]] e [[Convergência]] na [[Rede Neural]]: quando a [[Loss Function]] diverge, o treinamento está "driftando" — o modelo se afasta do resultado ótimo em vez de se aproximar.

## Drift como Ausência de Tautologia

Na tese [[Tautologia Ontológica]], drift é o que acontece quando a [[Tautologia]] não se estabelece. Se o [[Contexto]] é incompleto, múltiplas respostas são "plausíveis" dentro do [[Espaço Amostral]] — o modelo escolhe uma, mas poderia ter escolhido outra. Não há necessidade lógica no resultado.

Drift é o sintoma. [[Ontologia]] incompleta é a causa.

## Três Tiers de Drift

O artigo [[LLM Output Drift]] classifica modelos por comportamento a T=0.0:

- **Tier 1** (7-8B): 100% consistência. Determinísticos mas pouco capazes.
- **Tier 2** (20-70B): Alta consistência, bom equilíbrio.
- **Tier 3** (100B+): 12.5% consistência. A [[Matriz M]] maior tem [[Espaço Amostral]] maior — mais vetores competindo.

Modelos maiores driftam mais. Mais parâmetros ≠ mais determinismo. Isso reforça que [[Determinismo]] vem do [[Contexto]], não do modelo.

## Sensibilidade por Tarefa

Tarefas [[RAG]] são as mais sensíveis a drift. Classificação é a mais robusta (espaço de saída discreto). Sumarização é intermediária.

## Mitigação

O mesmo artigo propõe mitigação em três camadas:
- Validação cross-provider (testar o mesmo prompt em múltiplos modelos)
- [[Contexto]] estruturado rígido (reduzir ambiguidade)
- Harness de determinismo ([[DFAH]])

Na prática da tese: [[Tool|tools]] via [[MCP]], specs, BDD, TDD, ADR, observabilidade. Cada camada adicionada é uma camada de mitigação de drift — redução do [[Espaço Amostral]].

---

Relaciona-se com: [[Determinismo]], [[Contexto]], [[Ontologia]], [[Divergência]], [[Convergência]], [[Espaço Amostral]], [[Alucinação]], [[LLM Output Drift]], [[DFAH]], [[Tautologia Ontológica]], [[Matriz M]], [[RAG]], [[MCP]]
