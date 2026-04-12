# RAG

Retrieval Augmented Generation. The system's long-term memory. Vectorizes metadata via [[Embedding]] and enables semantic search across the complete history.

---

## Definition

RAG is the technique of augmenting model generation with information retrieved from a vector knowledge base. Instead of relying solely on what the model learned during training ([[Matrix M]]), RAG searches for relevant information in real time and injects it into the [[Context]].

## The Problem It Solves

Without RAG, [[Context]] is limited to the model's window in that session. Previous conversations, past decisions, project history -- everything is lost.

With RAG vectorizing metadata (decisions, specs, test results, ADRs), the [[Agent]] queries the entire project history at O(1) via [[MCP]].

## What to Vectorize

You do not need to vectorize everything -- vectorize the metadata: which decision was made, when, why, what the result was. At query time, RAG retrieves the relevant metadata via [[Vector|vector]] similarity search ([[Embedding]]), and the agent knows where to look for the complete context.

## Deterministic Feedback Loop

RAG closes the cycle: each interaction of the [[Agent]] with the code is recorded -> vectorized -> searchable. The next interaction has more context -> more [[Determinism]]. The loop only improves over time.

It is the component that enables the accumulation of structured knowledge described in the paper [[Ultra-Long-Horizon Agentic Science]]. The "+" of the 89%+ comes from here -- increasing [[Determinism]] with increasing history.

---

Related to: [[Embedding]], [[MCP]], [[Context]], [[Vector]], [[Agent]], [[Determinism]], [[Ultra-Long-Horizon Agentic Science]], [[Ontology]]
