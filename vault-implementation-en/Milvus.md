# Milvus

Vector database that stores the [[Agente na POC|agent]]'s episodic memory. Each tool call, decision, and session is embedded and stored. The agent queries Milvus to find similar past actions via [[mcp-memory-server]].

---

## Why Vectors

The [[Agente na POC|agent]] needs semantic memory, not textual. "When was the last time I searched for AWS Lambda documentation?" is not a text query -- it is a similarity query in the [[Embedding|embeddings]] space. Milvus performs nearest-neighbor search in high-dimensional spaces.

## Three Collections

Three simultaneous collections, each capturing a memory granularity:

**1. Tool Calls (~6KB each)**
Each tool invocation: which tool, parameters, result, timestamp, context. Finest granularity. It is L1 (Experience) of the HCC described in [[Acumulação Cognitiva]].

**2. Decisions (~6KB each)**
Each high-level decision: what objective, which options considered, which chosen, why. Medium granularity. It is L2 (Knowledge) of the HCC.

**3. Sessions (~6KB each)**
Summary of each complete session: objective, approach, result, lessons learned. Coarsest granularity. It is L3 (Wisdom) of the HCC.

## Embeddings

OpenAI embeddings (`text-embedding-3-small` or similar). Each record is embedded at ingestion time. Search by cosine similarity with configurable threshold.

The three simultaneously stored collections allow search at any level of abstraction: "tool calls similar to this", "decisions similar to this", "sessions similar to this".

## Parallel with HCC

The [[Ultra-Long-Horizon Agentic Science]] paper validates this architecture. The HCC (Hierarchical Cognitive Caching) uses exactly three memory layers -- L1 (experience), L2 (knowledge), L3 (wisdom). The ablation study shows that all three are necessary: without L1, medal rate drops to 22.7%; without L3, drops to 54.5%.

Our design maps directly:
- Tool calls -> L1 (Evolving Experience)
- Decisions -> L2 (Refined Knowledge)
- Sessions -> L3 (Prior Wisdom)

## Role in the Architecture

Milvus is the backend of [[mcp-memory-server]]. The agent:
- **Logs** every tool call, decision, and session automatically
- **Searches** for similar actions before acting ("have I done something like this before?")
- **Learns** from the past -- if an approach worked before, reuses it; if it failed, avoids it

It is the memory that makes the [[Loop de Auto-Melhoria]] possible.

---

Related to: [[mcp-memory-server]], [[Embedding]], [[Acumulação Cognitiva]], [[Loop de Auto-Melhoria]], [[Agente na POC]], [[MCP]]
