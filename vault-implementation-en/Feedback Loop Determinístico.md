# Deterministic Feedback Loop

The cycle in which each interaction of the [[Agente na POC|agent]] with the [[Cadeia de Servers|servers]] adds [[Contexto Programático|context]] to the system, which in turn improves subsequent interactions. The loop only improves over time -- [[Determinismo]] growing with growing history.

---

## The Loop in the POC

```
1. Agent searches for info -> search_docs("lambda") -> not found
2. Agent searches the web -> crawl_docs("https://docs.aws.amazon.com/lambda/...") -> saves to docs/
3. Now searchable -> search_docs("lambda") -> found
4. Agent uses the result as context for the next decision
```

Each iteration of the loop:
- **Expands the [[Ontologia como Código|ontology]]**: more files in `docs/`
- **Reduces the [[Espaço Amostral]]**: more [[Contexto Programático|context]] available for future searches
- **Increases [[Determinismo Mensurável|determinism]]**: less [[Drift]] because knowledge is mapped

## The Two Loops

**Short loop (within a session):**
The [[Agente na POC]] operates via [[ReAct na POC|ReAct]] -- reason, act (tool call), observe. Each cycle enriches the context of that session. `search_docs` -> result -> new decision -> `generate_diagram` -> result -> better decision.

**Long loop (across sessions):**
Documents saved by `crawl_docs` and `save_as_doc` persist in `docs/`. Diagrams saved by `save_diagram` persist in `diagrams/`. The next agent session starts with a richer ontology. It is [[RAG Implícito]] in action.

## Scientific Foundation

The [[Ultra-Long-Horizon Agentic Science]] paper demonstrates that agents maintain "strategic coherence" via [[Acumulação Cognitiva]] -- the HCC framework with three memory layers:

- **L1 (Experience)**: Raw execution traces -- in the POC, the output of each tool call.
- **L2 (Knowledge)**: Distilled judgments and insights -- in the POC, the docs saved by `crawl_docs` and `save_as_doc`.
- **L3 (Wisdom)**: Strategies transferable across sessions -- in the POC, the accumulated corpus in `docs/` and `diagrams/`.

The "+" of 89%+ ([[DFAH]]) comes from this loop. [[Determinismo]] is not static, it grows with accumulation. The HCC shows that linear accumulation (concatenating everything) saturates at 200k+ tokens. Structured accumulation (distillation L1->L2->L3) maintains ~70k effective tokens.

In the POC, accumulation is concrete: each `crawl_docs` adds pages, each `save_diagram` adds diagrams. The [[Ontologia como Código|ontology]] corpus grows monotonically. The [[Feedback Loop Determinístico]] is the POC's **context promotion** mechanism.

## [[Anti-Alucinação]] Condition

The loop is also a defense against [[Alucinação]]: if the information is not mapped, the agent can fetch it instead of inventing it. The path "not found -> fetched -> saved" transforms a potential hallucination into verified knowledge.

---

Related to: [[Cadeia de Servers]], [[docs-server]], [[web-to-docs]], [[ReAct na POC]], [[RAG Implícito]], [[Ontologia como Código]], [[Determinismo Mensurável]], [[Anti-Alucinação]], [[Ultra-Long-Horizon Agentic Science]], [[DFAH]], [[Acumulação Cognitiva]]
