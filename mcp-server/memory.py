"""
Memory backend — Python library wrapping Milvus.

Not an MCP server. Used internally by mcp-marvin.
"""

import os
import uuid
from datetime import datetime, timezone

import openai
from dotenv import load_dotenv
from pymilvus import (
    Collection, CollectionSchema, DataType, FieldSchema,
    connections, utility,
)

load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

MILVUS_HOST = os.getenv("MILVUS_HOST", "localhost")
MILVUS_PORT = os.getenv("MILVUS_PORT", "19530")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")

_openai_client = None
_connected = False


def _ensure_connected():
    global _connected
    if not _connected:
        connections.connect("default", host=MILVUS_HOST, port=MILVUS_PORT)
        _connected = True


def _get_openai():
    global _openai_client
    if _openai_client is None:
        _openai_client = openai.OpenAI()
    return _openai_client


def _embed(text: str) -> list[float]:
    """Embed a single text using OpenAI."""
    client = _get_openai()
    response = client.embeddings.create(input=text, model=EMBEDDING_MODEL)
    return response.data[0].embedding


def _embed_batch(texts: list[str], batch_size: int = 100) -> list[list[float]]:
    """Embed multiple texts in batches. Returns vectors in same order."""
    client = _get_openai()
    all_vectors = []
    for i in range(0, len(texts), batch_size):
        batch = texts[i : i + batch_size]
        response = client.embeddings.create(input=batch, model=EMBEDDING_MODEL)
        all_vectors.extend([d.embedding for d in response.data])
    return all_vectors


def _search_collection(collection_name: str, query: str, limit: int, output_fields: list[str]) -> list[dict]:
    """Search a Milvus collection by semantic similarity."""
    _ensure_connected()
    col = Collection(collection_name)
    col.load()

    vector = _embed(query)
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
        for field in output_fields:
            entry[field] = hit.entity.get(field)
        hits.append(entry)
    return hits


# ── Search ───────────────────────────────────────────────────────────────────


def search_tool_calls(query: str, limit: int = 5) -> str:
    """Search past tool invocations by semantic similarity."""
    fields = ["tool_name", "parameters", "result_summary", "context", "timestamp", "success"]
    hits = _search_collection("tool_calls", query, limit, fields)
    if not hits:
        return "No similar tool calls found."
    lines = [f"Found {len(hits)} similar tool call(s):\n"]
    for h in hits:
        success = "ok" if h.get("success") else "fail"
        lines.append(
            f"- [{success}] {h.get('tool_name', '?')} (score={h['score']:.3f})\n"
            f"  params: {h.get('parameters', '')}\n"
            f"  result: {h.get('result_summary', '')}\n"
            f"  context: {h.get('context', '')}\n"
            f"  time: {h.get('timestamp', '')}"
        )
    return "\n".join(lines)


def search_decisions(query: str, limit: int = 5) -> str:
    """Search past decisions by semantic similarity."""
    fields = ["objective", "options_considered", "chosen_option", "reasoning", "outcome", "timestamp"]
    hits = _search_collection("decisions", query, limit, fields)
    if not hits:
        return "No similar decisions found."
    lines = [f"Found {len(hits)} similar decision(s):\n"]
    for h in hits:
        lines.append(
            f"- (score={h['score']:.3f}) {h.get('objective', '?')}\n"
            f"  options: {h.get('options_considered', '')}\n"
            f"  chosen: {h.get('chosen_option', '')}\n"
            f"  reasoning: {h.get('reasoning', '')}\n"
            f"  outcome: {h.get('outcome', '')}\n"
            f"  time: {h.get('timestamp', '')}"
        )
    return "\n".join(lines)


def search_sessions(query: str, limit: int = 5) -> str:
    """Search past sessions by semantic similarity."""
    fields = ["objective", "approach", "result", "lessons_learned", "tools_used",
              "decision_count", "tool_call_count", "timestamp"]
    hits = _search_collection("sessions", query, limit, fields)
    if not hits:
        return "No similar sessions found."
    lines = [f"Found {len(hits)} similar session(s):\n"]
    for h in hits:
        lines.append(
            f"- (score={h['score']:.3f}) {h.get('objective', '?')}\n"
            f"  approach: {h.get('approach', '')}\n"
            f"  result: {h.get('result', '')}\n"
            f"  lessons: {h.get('lessons_learned', '')}\n"
            f"  tools: {h.get('tools_used', '')} | "
            f"decisions: {h.get('decision_count', 0)} | "
            f"tool calls: {h.get('tool_call_count', 0)}\n"
            f"  time: {h.get('timestamp', '')}"
        )
    return "\n".join(lines)


# ── Log ──────────────────────────────────────────────────────────────────────


def log_tool_call(
    tool_name: str,
    parameters: str,
    result_summary: str,
    success: bool,
    context: str = "",
    session_id: str = "",
) -> str:
    """Record a tool invocation (L1 Experience)."""
    _ensure_connected()
    col = Collection("tool_calls")

    now = datetime.now(timezone.utc).isoformat()
    record_id = str(uuid.uuid4())

    embed_text = f"{tool_name} {parameters} {context} {result_summary}"
    vector = _embed(embed_text)

    col.insert([
        [record_id], [tool_name], [parameters], [result_summary],
        [context], [session_id], [now], [success], [vector],
    ])
    col.flush()
    return f"Logged tool call: {tool_name} ({record_id})"


def log_decision(
    objective: str,
    options_considered: str,
    chosen_option: str,
    reasoning: str,
    outcome: str = "",
    session_id: str = "",
) -> str:
    """Record a decision (L2 Knowledge)."""
    _ensure_connected()
    col = Collection("decisions")

    now = datetime.now(timezone.utc).isoformat()
    record_id = str(uuid.uuid4())

    embed_text = f"{objective} {options_considered} {chosen_option} {reasoning}"
    vector = _embed(embed_text)

    col.insert([
        [record_id], [objective], [options_considered], [chosen_option],
        [reasoning], [outcome], [session_id], [now], [vector],
    ])
    col.flush()
    return f"Logged decision: {objective[:60]} ({record_id})"


def log_session(
    objective: str,
    approach: str,
    result: str,
    lessons_learned: str,
    tools_used: str = "",
    decision_count: int = 0,
    tool_call_count: int = 0,
) -> str:
    """Record a session summary (L3 Wisdom)."""
    _ensure_connected()
    col = Collection("sessions")

    now = datetime.now(timezone.utc).isoformat()
    record_id = str(uuid.uuid4())

    embed_text = f"{objective} {approach} {result} {lessons_learned}"
    vector = _embed(embed_text)

    col.insert([
        [record_id], [objective], [approach], [result],
        [lessons_learned], [tools_used], [decision_count],
        [tool_call_count], [now], [vector],
    ])
    col.flush()
    return f"Logged session: {objective[:60]} ({record_id})"


# ── Semantic Search (doc_chunks + concepts) ────────────────────────────────


def search_doc_chunks(query: str, limit: int = 5) -> list[dict]:
    """Semantic search over doc chunks. Returns list of {score, doc_name, heading, content}."""
    fields = ["doc_name", "heading", "content"]
    return _search_collection("doc_chunks", query, limit, fields)


def search_concepts_semantic(query: str, limit: int = 5) -> list[dict]:
    """Semantic search over concepts. Returns list of {score, name, vault, summary}."""
    fields = ["name", "vault", "summary"]
    return _search_collection("concepts", query, limit, fields)


# ── Indexing (called by load_vaults and rebuild scripts) ────────────────────


def _chunk_markdown(text: str, doc_name: str) -> list[dict]:
    """Split markdown by ## headers into chunks."""
    import re
    chunks = []
    # Split on ## but keep the heading
    parts = re.split(r"(?=^## )", text, flags=re.MULTILINE)

    for i, part in enumerate(parts):
        part = part.strip()
        if not part:
            continue

        # Extract heading
        lines = part.split("\n", 1)
        heading = lines[0].lstrip("#").strip() if lines[0].startswith("#") else doc_name
        content = lines[1].strip() if len(lines) > 1 else part

        # Skip tiny chunks (navigation fragments, empty sections)
        if len(content) < 50:
            continue

        chunks.append({
            "id": f"{doc_name}::{i}",
            "doc_name": doc_name,
            "chunk_index": i,
            "heading": heading[:500].encode("utf-8")[:500].decode("utf-8", errors="ignore"),
            "content": content[:8000].encode("utf-8")[:8000].decode("utf-8", errors="ignore"),
            "embed_text": f"{heading}\n{content}"[:8000],
        })

    return chunks


def index_docs(docs_dir: str) -> str:
    """Index all markdown docs into Milvus doc_chunks collection.

    Drops and recreates all entries. Call after docs change.
    """
    from pathlib import Path
    _ensure_connected()

    docs_path = Path(docs_dir)
    if not docs_path.exists():
        return f"Docs directory not found: {docs_dir}"

    # Collect all chunks
    all_chunks = []
    for md_file in sorted(docs_path.glob("*.md")):
        text = md_file.read_text()
        if len(text) < 200:
            continue
        chunks = _chunk_markdown(text, md_file.stem)
        all_chunks.extend(chunks)

    if not all_chunks:
        return "No chunks to index."

    # Batch embed
    embed_texts = [c["embed_text"] for c in all_chunks]
    vectors = _embed_batch(embed_texts)

    # Clear existing entries
    col = Collection("doc_chunks")
    col.load()
    # Delete all existing — use expression on doc_name
    if col.num_entities > 0:
        col.delete(expr='doc_name != ""')
        col.flush()

    # Insert in batches
    batch_size = 200
    for i in range(0, len(all_chunks), batch_size):
        batch = all_chunks[i : i + batch_size]
        batch_vectors = vectors[i : i + batch_size]
        col.insert([
            [c["id"] for c in batch],
            [c["doc_name"] for c in batch],
            [c["chunk_index"] for c in batch],
            [c["heading"] for c in batch],
            [c["content"] for c in batch],
            batch_vectors,
        ])
    col.flush()

    return f"Indexed {len(all_chunks)} chunks from {len(list(docs_path.glob('*.md')))} docs."


def index_concepts(concepts: list[dict]) -> str:
    """Index concepts into Milvus concepts collection.

    Args:
        concepts: list of dicts with keys: name, vault, summary, content
    """
    _ensure_connected()

    if not concepts:
        return "No concepts to index."

    # Build embed text: name + summary + first N chars of content
    entries = []
    for c in concepts:
        content_preview = (c.get("content") or "")[:2000]
        embed_text = f"{c['name']}\n{c.get('summary', '')}\n{content_preview}"
        entries.append({
            "id": f"concept::{c['name']}",
            "name": c["name"][:250],
            "vault": (c.get("vault") or "")[:60],
            "summary": (c.get("summary") or "")[:1000].encode("utf-8")[:1000].decode("utf-8", errors="ignore"),
            "content": content_preview[:8000].encode("utf-8")[:8000].decode("utf-8", errors="ignore"),
            "embed_text": embed_text[:8000],
        })

    # Batch embed
    vectors = _embed_batch([e["embed_text"] for e in entries])

    # Clear existing
    col = Collection("concepts")
    col.load()
    if col.num_entities > 0:
        col.delete(expr='name != ""')
        col.flush()

    # Insert in batches
    batch_size = 200
    for i in range(0, len(entries), batch_size):
        batch = entries[i : i + batch_size]
        batch_vectors = vectors[i : i + batch_size]
        col.insert([
            [e["id"] for e in batch],
            [e["name"] for e in batch],
            [e["vault"] for e in batch],
            [e["summary"] for e in batch],
            [e["content"] for e in batch],
            batch_vectors,
        ])
    col.flush()

    return f"Indexed {len(entries)} concepts."


# ── Schema ──────────────────────────────────────────────────────────────────


ALL_COLLECTIONS = ["tool_calls", "decisions", "sessions", "doc_chunks", "concepts"]

EMBEDDING_DIM = 1536  # text-embedding-3-small

_COLLECTION_DEFS = {
    "tool_calls": {
        "description": "L1 Experience — tool call episodic memory",
        "fields": [
            FieldSchema("id", DataType.VARCHAR, is_primary=True, max_length=64),
            FieldSchema("tool_name", DataType.VARCHAR, max_length=100),
            FieldSchema("parameters", DataType.VARCHAR, max_length=8000),
            FieldSchema("result_summary", DataType.VARCHAR, max_length=8000),
            FieldSchema("context", DataType.VARCHAR, max_length=8000),
            FieldSchema("session_id", DataType.VARCHAR, max_length=64),
            FieldSchema("timestamp", DataType.VARCHAR, max_length=64),
            FieldSchema("success", DataType.BOOL),
            FieldSchema("embedding", DataType.FLOAT_VECTOR, dim=EMBEDDING_DIM),
        ],
    },
    "decisions": {
        "description": "L2 Knowledge — decision episodic memory",
        "fields": [
            FieldSchema("id", DataType.VARCHAR, is_primary=True, max_length=64),
            FieldSchema("objective", DataType.VARCHAR, max_length=8000),
            FieldSchema("options_considered", DataType.VARCHAR, max_length=8000),
            FieldSchema("chosen_option", DataType.VARCHAR, max_length=8000),
            FieldSchema("reasoning", DataType.VARCHAR, max_length=8000),
            FieldSchema("outcome", DataType.VARCHAR, max_length=8000),
            FieldSchema("session_id", DataType.VARCHAR, max_length=64),
            FieldSchema("timestamp", DataType.VARCHAR, max_length=64),
            FieldSchema("embedding", DataType.FLOAT_VECTOR, dim=EMBEDDING_DIM),
        ],
    },
    "sessions": {
        "description": "L3 Wisdom — session episodic memory",
        "fields": [
            FieldSchema("id", DataType.VARCHAR, is_primary=True, max_length=64),
            FieldSchema("objective", DataType.VARCHAR, max_length=8000),
            FieldSchema("approach", DataType.VARCHAR, max_length=8000),
            FieldSchema("result", DataType.VARCHAR, max_length=8000),
            FieldSchema("lessons_learned", DataType.VARCHAR, max_length=8000),
            FieldSchema("tools_used", DataType.VARCHAR, max_length=2000),
            FieldSchema("decision_count", DataType.INT64),
            FieldSchema("tool_call_count", DataType.INT64),
            FieldSchema("timestamp", DataType.VARCHAR, max_length=64),
            FieldSchema("embedding", DataType.FLOAT_VECTOR, dim=EMBEDDING_DIM),
        ],
    },
    "doc_chunks": {
        "description": "Semantic index — doc chunks",
        "fields": [
            FieldSchema("id", DataType.VARCHAR, is_primary=True, max_length=256),
            FieldSchema("doc_name", DataType.VARCHAR, max_length=256),
            FieldSchema("chunk_index", DataType.INT64),
            FieldSchema("heading", DataType.VARCHAR, max_length=500),
            FieldSchema("content", DataType.VARCHAR, max_length=8000),
            FieldSchema("embedding", DataType.FLOAT_VECTOR, dim=EMBEDDING_DIM),
        ],
    },
    "concepts": {
        "description": "Semantic index — KG concepts",
        "fields": [
            FieldSchema("id", DataType.VARCHAR, is_primary=True, max_length=256),
            FieldSchema("name", DataType.VARCHAR, max_length=250),
            FieldSchema("vault", DataType.VARCHAR, max_length=60),
            FieldSchema("summary", DataType.VARCHAR, max_length=1000),
            FieldSchema("content", DataType.VARCHAR, max_length=8000),
            FieldSchema("embedding", DataType.FLOAT_VECTOR, dim=EMBEDDING_DIM),
        ],
    },
}


def ensure_collections():
    """Create all Milvus collections if they don't exist. Idempotent."""
    _ensure_connected()
    created = []
    for name, defn in _COLLECTION_DEFS.items():
        if utility.has_collection(name):
            continue
        schema = CollectionSchema(fields=defn["fields"], description=defn["description"])
        col = Collection(name, schema=schema)
        col.create_index(
            "embedding",
            {"metric_type": "COSINE", "index_type": "IVF_FLAT", "params": {"nlist": 128}},
        )
        created.append(name)
    return created


def get_schema() -> str:
    """Return current Milvus schema (collections, fields, indexes)."""
    _ensure_connected()
    lines = ["# Milvus Schema\n"]
    for name in ALL_COLLECTIONS:
        if not utility.has_collection(name):
            lines.append(f"## {name}: NOT FOUND")
            continue
        col = Collection(name)
        lines.append(f"## {name}")
        lines.append(f"  Description: {col.description}")
        lines.append(f"  Entities: {col.num_entities}")
        lines.append(f"  Fields:")
        for field in col.schema.fields:
            lines.append(f"    - {field.name}: {field.dtype.name} (pk={field.is_primary})")
        for idx in col.indexes:
            lines.append(f"  Index: {idx.params}")
        lines.append("")
    return "\n".join(lines)
