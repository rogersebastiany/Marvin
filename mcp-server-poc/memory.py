"""
Memory backend — Python library wrapping Milvus.

Not an MCP server. Used internally by mcp-marvin.
"""

import os
import uuid
from datetime import datetime, timezone

import openai
from dotenv import load_dotenv
from pymilvus import Collection, connections, utility

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
    """Embed text using OpenAI."""
    client = _get_openai()
    response = client.embeddings.create(input=text, model=EMBEDDING_MODEL)
    return response.data[0].embedding


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


def get_schema() -> str:
    """Return current Milvus schema (collections, fields, indexes)."""
    _ensure_connected()
    lines = ["# Milvus Schema\n"]
    for name in ["tool_calls", "decisions", "sessions"]:
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
