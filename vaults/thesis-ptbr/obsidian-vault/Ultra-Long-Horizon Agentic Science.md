# Ultra-Long-Horizon Agentic Science

Artigo que apresenta ML-Master 2.0, um agente autônomo que mantém coerência estratégica em ciclos longos (24h+) através de [[Acumulação Cognitiva]] hierárquica. Introduz o framework HCC (Hierarchical Cognitive Caching).

---

## Referência

**Toward Ultra-Long-Horizon Agentic Science: Cognitive Accumulation for Machine Learning Engineering**
Xinyu Zhu, Yuzhu Cai, Zexi Liu et al. — Shanghai Jiao Tong University, DP Technology, Shanghai AI Laboratory
https://arxiv.org/abs/2601.10402

## Contribuição

O artigo redefine autonomia de longo horizonte não como expansão de contexto, mas como um processo evolutivo de [[Acumulação Cognitiva]]: experiência transiente → conhecimento validado → sabedoria reutilizável. Introduz o HCC como mecanismo concreto.

## Hierarchical Cognitive Caching (HCC)

Hierarquia de memória em três camadas, inspirada em cache de computador:

**L1 — Evolving Experience (memória de trabalho)**
Traces de execução raw: patches de código, output de terminal, plano de pesquisa atual. Alta fidelidade, curta duração. O scratchpad do [[Agente]].

**L2 — Refined Knowledge (memória estratégica de médio prazo)**
Julgamentos-chave ("feature X é prejudicial"), insights experimentais ("CV leakage sob split Y"), resumos de progresso. Destilado de L1 após cada fase. Permite planejamento de longo prazo sem carregar logs verbosos.

**L3 — Prior Wisdom (memória de longo prazo)**
Estratégias transferíveis, pipelines reutilizáveis, priors estáveis de hiperparâmetros. Persiste entre tarefas. Armazenado como pares ([[Embedding]], texto) e recuperado via similaridade de cosseno.

## Context Migration

Três operações movem informação entre camadas:

- **Prefetching**: Antes de iniciar uma tarefa, embeda o descritor da tarefa e recupera sabedoria similar de L3 via threshold δ de cosseno. O agente já começa informado.
- **Context Hit**: Política cache-like — busca em L1 se disponível, senão fallback para resumos de L2.
- **Context Promotion**: P1 comprime L1→L2 (sumarização por fase), P2 destila L2→L3 (extração de sabedoria por tarefa). Experiência cristaliza em conhecimento, que cristaliza em sabedoria.

## Resultados

- **56.44% medal rate** no MLE-Bench (75 tarefas Kaggle reais) — SOTA, superando todos proprietary e open-source.
- **92.7% melhoria** sobre ML-Master 1.0.
- HCC limita pico de contexto de **200k+ tokens para ~70k**, retendo coerência estratégica.
- Supera 50% dos participantes humanos em 63.1% das tarefas.

## Ablation — Cada Camada Importa

| Configuração | Valid Submission | Medal Rate |
|---|---|---|
| Sem L1 (Experience) | 54.5% | 22.7% |
| Sem L2 (Knowledge) | 95.5% | 59.1% |
| Sem L3 (Wisdom) | 95.5% | 54.5% |
| **Completo (L1+L2+L3)** | **95.5%** | **72.7%** |

L1 é a mais crítica — sem experiência raw, o agente não consegue iterar sobre seus erros. L3 é a que mais impacta qualidade — sem sabedoria prévia, o agente explora ineficientemente.

## O "+" do 89%+

Este artigo sustenta o "mais" do 89%+ demonstrado pelo [[DFAH]]. O [[Determinismo]] não é estático — ele cresce com o tempo quando o [[Contexto]] é cumulativo e estruturado em camadas.

Mecanismo: cada ciclo [[ReAct]] do [[Agente]] produz novo conhecimento → destilado em L2 → cristalizado em L3 → disponível no próximo ciclo → contexto mais rico → determinismo maior.

O insight central: **[[Acumulação Cognitiva]] ≠ agregação linear de contexto**. É experiência → conhecimento → sabedoria. Cada nível tem dinâmicas temporais e níveis de abstração diferentes.

---

Relaciona-se com: [[Determinismo]], [[RAG]], [[Agente]], [[ReAct]], [[DFAH]], [[Contexto]], [[Tautologia Ontológica]], [[Acumulação Cognitiva]], [[Embedding]]
