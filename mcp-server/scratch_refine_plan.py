"""
Dogfood: manually execute the refine_plan algorithm against our Milvus.

Input draft = the spec I proposed for the refine_plan + save_plan tools themselves.
Run 2 Hadamard iterations across 5 collections, print ressalvas, decide.

This is NOT a tool. It's a throwaway validator. Delete after decision.
"""
from __future__ import annotations
import math
import textwrap
from pymilvus import connections, Collection

import memory  # local module — uses its _embed()

# ── The draft being refined: the spec for the tools themselves ─────────────
DRAFT = """
refine_plan + save_plan — two new MCP tools for Marvin.

## refine_plan(draft: str, iterations: int = 2, k_per_collection: int = 5) -> dict
Non-LLM, tautological plan refinement via Hadamard product vector walk.

Algorithm:
1. current_vector = L2_normalize(embed(draft))
2. For i in range(iterations):
   a. For each collection in [concepts, decisions, sessions, doc_chunks, plans]:
      - hits = milvus.search(data=[current_vector], limit=k_per_collection)
      - collect top-k as ressalvas (score + text snippet + source)
   b. ressalva_text = concat of all ressalva snippets this iteration
   c. ressalva_vector = L2_normalize(embed(ressalva_text))
   d. current_vector = L2_normalize(current_vector ⊙ ressalva_vector)  # Hadamard
3. Return {
     per_iteration: [[ressalvas_i1], [ressalvas_i2]],
     enhanced_draft: draft + inline annotations,
     total_ressalvas: int,
     final_vector: list[float],
   }

The intuition: each iteration bends the draft's vector toward whatever Milvus
already knows is related, surfacing concerns/prior-art/contradictions that the
draft doesn't yet address. After N iterations the walk converges on the
neighborhood of the draft's true semantic position.

## save_plan(name, title, status, summary, content) -> str
Embed + upsert into the plans collection in Milvus.

- name: slug, regex ^[\\w\\-]+$, max 100 chars
- title: max 200 chars
- status: enum draft|approved|in_progress|done|archived
- summary: max 1000 chars
- content: max 50000 chars (full plan markdown)

## Middleware classification
- refine_plan → MILVUS_TOOLS (retrieval, sets the gate)
- save_plan → WRITE_TOOLS (gated — requires prior retrieval)

## Structural changes in memory.py
- Register plans in _COLLECTION_DEFS (was created manually)
- Add helpers: _hadamard_normalize(), _search_by_vector(), _format_ressalva(),
  refine_plan_vector_walk(), save_plan(), search_plans()
- Extend get_memory(collection="plans") dispatch

## Why this matters
Planning currently happens in markdown files and gets lost. Plans should live
in Milvus so future sessions can retrieve_before_act on prior planning work.
And refinement should be deterministic (vectors, not LLM), consistent with
Tautologia Ontologica.
""".strip()


def l2_normalize(v: list[float]) -> list[float]:
    norm = math.sqrt(sum(x * x for x in v))
    if norm == 0:
        return v
    return [x / norm for x in v]


def hadamard(a: list[float], b: list[float]) -> list[float]:
    return [x * y for x, y in zip(a, b)]


def search_by_vector(collection_name: str, vector: list[float], limit: int, output_fields: list[str]) -> list[dict]:
    col = Collection(collection_name)
    col.load()
    results = col.search(
        data=[vector],
        anns_field="embedding",
        param={"metric_type": "COSINE", "params": {"nprobe": 16}},
        limit=limit,
        output_fields=output_fields,
    )
    hits = []
    for hit in results[0]:
        entry = {"score": hit.score}
        for f in output_fields:
            entry[f] = hit.entity.get(f)
        hits.append(entry)
    return hits


COLLECTION_CONFIG = {
    "concepts": (["name", "vault", "summary"], lambda h: f"[{h.get('vault','?')}] {h.get('name','?')} — {(h.get('summary') or '')[:180]}"),
    "decisions": (["objective", "chosen_option", "reasoning"], lambda h: f"{h.get('objective','?')[:80]} → {(h.get('chosen_option') or '')[:80]} ({(h.get('reasoning') or '')[:120]})"),
    "sessions": (["objective", "lessons_learned"], lambda h: f"{h.get('objective','?')[:80]} — lessons: {(h.get('lessons_learned') or '')[:180]}"),
    "doc_chunks": (["doc_name", "heading", "content"], lambda h: f"{h.get('doc_name','?')}#{h.get('heading','?')[:40]} — {(h.get('content') or '')[:160]}"),
    "plans": (["name", "title", "status", "summary"], lambda h: f"[{h.get('status','?')}] {h.get('name','?')}: {h.get('title','?')[:60]} — {(h.get('summary') or '')[:120]}"),
}


def run():
    connections.connect("default", host="localhost", port="19530")
    print("=" * 80)
    print("DOGFOOD: refine_plan vector walk on its own spec")
    print("=" * 80)
    print()

    # Step 1: embed draft
    print("[step 1] Embedding draft...")
    v0 = memory._embed(DRAFT)
    current = l2_normalize(v0)
    print(f"  draft length: {len(DRAFT)} chars, vector dim: {len(current)}")
    print()

    all_ressalvas: list[list[dict]] = []

    for it in range(2):
        print("=" * 80)
        print(f"ITERATION {it + 1}")
        print("=" * 80)

        iter_hits: list[dict] = []
        ressalva_text_parts: list[str] = []

        for col_name, (fields, fmt) in COLLECTION_CONFIG.items():
            hits = search_by_vector(col_name, current, limit=5, output_fields=fields)
            print(f"\n-- {col_name} (top {len(hits)}) --")
            for h in hits:
                line = fmt(h)
                print(f"  [{h['score']:.3f}] {line}")
                ressalva_text_parts.append(line)
                iter_hits.append({"collection": col_name, **h})

        all_ressalvas.append(iter_hits)

        # Build ressalva text, embed, Hadamard
        ressalva_text = "\n".join(ressalva_text_parts)
        rv = memory._embed(ressalva_text)
        rv_n = l2_normalize(rv)
        new_current = l2_normalize(hadamard(current, rv_n))

        # Compute drift (cosine) from previous vector
        drift = sum(a * b for a, b in zip(current, new_current))
        print(f"\n[iter {it+1}] ressalva_text: {len(ressalva_text)} chars")
        print(f"[iter {it+1}] cosine(prev, new) = {drift:.4f}  (1.0 = no movement)")

        current = new_current

    # Summary
    print()
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    total = sum(len(r) for r in all_ressalvas)
    print(f"Total ressalvas surfaced: {total}")
    print(f"Iterations: {len(all_ressalvas)}")

    # Unique sources across iterations
    seen = set()
    for r in all_ressalvas:
        for h in r:
            key = (h["collection"], h.get("name") or h.get("objective") or h.get("doc_name") or h.get("title") or "")
            seen.add(key)
    print(f"Unique sources: {len(seen)}")

    # New sources in iteration 2 that weren't in iteration 1
    iter1_keys = set()
    for h in all_ressalvas[0]:
        iter1_keys.add((h["collection"], h.get("name") or h.get("objective") or h.get("doc_name") or h.get("title") or ""))
    iter2_new = []
    for h in all_ressalvas[1]:
        k = (h["collection"], h.get("name") or h.get("objective") or h.get("doc_name") or h.get("title") or "")
        if k not in iter1_keys:
            iter2_new.append(k)
    print(f"New sources in iter2 (not in iter1): {len(iter2_new)}")
    for k in iter2_new:
        print(f"  - {k[0]}: {k[1]}")


if __name__ == "__main__":
    run()
