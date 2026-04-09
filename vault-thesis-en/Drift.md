# Drift

A phenomenon where the output of an AI model varies even when the apparent conditions are constant -- same prompt, same temperature, same model. The AI "drifts" from the expected result.

---

## Formal Definition

The paper [[LLM Output Drift]] defines drift as the unintentional variation of LLM responses in repeatable workflows, especially in financial contexts where reproducibility is critical.

Drift occurs due to multiple causes: internal model changes (silent updates), numerical precision differences between providers, batching variations, and fundamentally -- insufficient [[Contexto]].

## Inverse Relationship with Context

Drift is inversely proportional to the completeness of the [[Ontologia]]:

- Poor [[Contexto]] -> broad decision space -> many candidate tokens -> high variation -> drift
- Rich [[Contexto]] -> narrow decision space -> few candidates -> low variation -> [[Determinismo]]

It is the same relationship that exists between [[Divergência]] and [[Convergência]] in a [[Rede Neural]]: when the [[Loss Function]] diverges, training is "drifting" -- the model moves away from the optimal result instead of approaching it.

## Drift as Absence of Tautology

In the [[Ontological Tautology]] thesis, drift is what happens when [[Tautologia]] is not established. If [[Contexto]] is incomplete, multiple responses are "plausible" within the [[Espaço Amostral]] -- the model chooses one, but could have chosen another. There is no logical necessity in the result.

Drift is the symptom. Incomplete [[Ontologia]] is the cause.

## Three Tiers of Drift

The paper [[LLM Output Drift]] classifies models by behavior at T=0.0:

- **Tier 1** (7-8B): 100% consistency. Deterministic but not very capable.
- **Tier 2** (20-70B): High consistency, good balance.
- **Tier 3** (100B+): 12.5% consistency. The larger [[Matriz M]] has a larger [[Espaço Amostral]] -- more vectors competing.

Larger models drift more. More parameters does not equal more determinism. This reinforces that [[Determinismo]] comes from [[Contexto]], not from the model.

## Sensitivity by Task

[[RAG]] tasks are the most sensitive to drift. Classification is the most robust (discrete output space). Summarization is intermediate.

## Mitigation

The same paper proposes mitigation in three layers:
- Cross-provider validation (test the same prompt across multiple models)
- Rigid structured [[Contexto]] (reduce ambiguity)
- Determinism harness ([[DFAH]])

In the thesis practice: [[Tool|tools]] via [[MCP]], specs, BDD, TDD, ADR, observability. Each layer added is a layer of drift mitigation -- reduction of the [[Espaço Amostral]].

---

Related to: [[Determinismo]], [[Contexto]], [[Ontologia]], [[Divergência]], [[Convergência]], [[Espaço Amostral]], [[Alucinação]], [[LLM Output Drift]], [[DFAH]], [[Ontological Tautology]], [[Matriz M]], [[RAG]], [[MCP]]
