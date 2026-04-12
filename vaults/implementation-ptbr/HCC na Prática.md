# HCC na Prática

Como o Hierarchical Cognitive Caching é implementado no [[Marvin]]. A decisão mais importante: L1 (Experience) NÃO é persistido. Vive apenas na context window e é descartado após destilação.

---

## Por que L1 Não É Persistido

O paper [[Ultra-Long-Horizon Agentic Science]] mostra que todas as 3 camadas são necessárias (ablation: sem L1 → 22.7%, sem L3 → 54.5%). Mas L1 é transiente por design — tool traces, patches, output de terminal. Persistir L1 causa saturação de contexto: 200k+ tokens, o modelo perde coerência.

HCC mantém ~70k tokens efetivos descartando L1 após destilação para L2. O agente não precisa lembrar cada `git diff` — precisa lembrar "commit X corrigiu bug Y por razão Z" (L2).

## Três Camadas

| Camada | O que armazena | Persistência | Tool |
|--------|---------------|-------------|------|
| **L1 Experience** | Tool traces, patches, terminal output | Context window apenas | Nenhum — vive no contexto |
| **L2 Knowledge** | Decisões, julgamentos, insights | Milvus `decisions` collection | `log_decision` |
| **L3 Wisdom** | Resumos de sessão, estratégias | Milvus `sessions` collection | `log_session` |

## Migração de Contexto

Três operações movem informação entre camadas:

1. **Context Prefetch** (L2/L3 → context): `retrieve` ou `get_memory` busca decisões e sessões similares antes de agir. Injeta L2/L3 como contexto para a ação atual.

2. **Context Hit** (context → L1): o agente age, observa o resultado. O resultado vira L1 na context window.

3. **Context Promotion** (L1 → L2, L2 → L3): o agente destila L1 em uma decisão (`log_decision`) ou sintetiza L2 em um resumo de sessão (`log_session`).

```
Prefetch: Milvus L2/L3 → context window
Hit:      tool result → context window (L1)
Promote:  L1 → log_decision → Milvus L2
          L2 → log_session → Milvus L3
```

## `log_decision` — Fire and Forget

`log_decision` é async fire-and-forget (daemon thread). O agente loga e continua sem esperar confirmação. Isso é crítico para não interromper o fluxo de trabalho. Se Milvus estiver offline, o log é silenciosamente descartado — preferível a bloquear o agente.

## `log_session` — Síntese

`log_session` é chamado no final de uma sessão. O agente sintetiza: objetivo, abordagem, resultado, lições aprendidas, tools usadas, decisões tomadas. É o L3 — sabedoria transferível para sessões futuras.

## Validação

O design mapeia diretamente para o HCC do paper:
- Tool calls → L1 (Evolving Experience)
- Decisions → L2 (Refined Knowledge)
- Sessions → L3 (Prior Wisdom)

A diferença: nosso L1 não é persistido em Milvus. O paper persiste L1, mas com um mecanismo de eviction. Nós simplificamos: L1 é a context window, ponto. Destila para L2 ou perde-se.

---

Relaciona-se com: [[Acumulação Cognitiva]], [[Milvus]], [[Marvin]], [[Loop de Auto-Melhoria]], [[Determinismo Mensurável]]
