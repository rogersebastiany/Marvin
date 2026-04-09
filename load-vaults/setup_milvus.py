"""
Set up Milvus collections for episodic memory.

Three collections mapping to HCC layers:
  - tool_calls  (L1 Experience) — individual tool invocations
  - decisions   (L2 Knowledge)  — high-level decision records
  - sessions    (L3 Wisdom)     — session summaries and lessons

Each collection stores text metadata + a vector embedding (1536-dim,
matching OpenAI text-embedding-3-small).

Usage:
    uv run python setup_milvus.py          # create collections
    uv run python setup_milvus.py --drop   # drop and recreate
    uv run python setup_milvus.py --status # show collection stats
"""

import sys
from pymilvus import (
    connections,
    utility,
    Collection,
    CollectionSchema,
    FieldSchema,
    DataType,
)

MILVUS_HOST = "localhost"
MILVUS_PORT = "19530"
EMBEDDING_DIM = 1536  # OpenAI text-embedding-3-small


def connect():
    connections.connect("default", host=MILVUS_HOST, port=MILVUS_PORT)


def create_tool_calls():
    """L1 Experience — every tool invocation."""
    fields = [
        FieldSchema(name="id", dtype=DataType.VARCHAR, is_primary=True, max_length=64),
        FieldSchema(name="tool_name", dtype=DataType.VARCHAR, max_length=128),
        FieldSchema(name="parameters", dtype=DataType.VARCHAR, max_length=4096),
        FieldSchema(name="result_summary", dtype=DataType.VARCHAR, max_length=4096),
        FieldSchema(name="context", dtype=DataType.VARCHAR, max_length=2048),
        FieldSchema(name="session_id", dtype=DataType.VARCHAR, max_length=64),
        FieldSchema(name="timestamp", dtype=DataType.VARCHAR, max_length=32),
        FieldSchema(name="success", dtype=DataType.BOOL),
        FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=EMBEDDING_DIM),
    ]
    schema = CollectionSchema(fields, description="L1 Experience — tool call episodic memory")
    col = Collection("tool_calls", schema)
    col.create_index(
        field_name="embedding",
        index_params={
            "metric_type": "COSINE",
            "index_type": "IVF_FLAT",
            "params": {"nlist": 128},
        },
    )
    print("  Created tool_calls (L1 Experience)")
    return col


def create_decisions():
    """L2 Knowledge — high-level decisions."""
    fields = [
        FieldSchema(name="id", dtype=DataType.VARCHAR, is_primary=True, max_length=64),
        FieldSchema(name="objective", dtype=DataType.VARCHAR, max_length=2048),
        FieldSchema(name="options_considered", dtype=DataType.VARCHAR, max_length=4096),
        FieldSchema(name="chosen_option", dtype=DataType.VARCHAR, max_length=2048),
        FieldSchema(name="reasoning", dtype=DataType.VARCHAR, max_length=4096),
        FieldSchema(name="outcome", dtype=DataType.VARCHAR, max_length=2048),
        FieldSchema(name="session_id", dtype=DataType.VARCHAR, max_length=64),
        FieldSchema(name="timestamp", dtype=DataType.VARCHAR, max_length=32),
        FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=EMBEDDING_DIM),
    ]
    schema = CollectionSchema(fields, description="L2 Knowledge — decision episodic memory")
    col = Collection("decisions", schema)
    col.create_index(
        field_name="embedding",
        index_params={
            "metric_type": "COSINE",
            "index_type": "IVF_FLAT",
            "params": {"nlist": 128},
        },
    )
    print("  Created decisions (L2 Knowledge)")
    return col


def create_sessions():
    """L3 Wisdom — session summaries."""
    fields = [
        FieldSchema(name="id", dtype=DataType.VARCHAR, is_primary=True, max_length=64),
        FieldSchema(name="objective", dtype=DataType.VARCHAR, max_length=2048),
        FieldSchema(name="approach", dtype=DataType.VARCHAR, max_length=4096),
        FieldSchema(name="result", dtype=DataType.VARCHAR, max_length=4096),
        FieldSchema(name="lessons_learned", dtype=DataType.VARCHAR, max_length=4096),
        FieldSchema(name="tools_used", dtype=DataType.VARCHAR, max_length=2048),
        FieldSchema(name="decision_count", dtype=DataType.INT64),
        FieldSchema(name="tool_call_count", dtype=DataType.INT64),
        FieldSchema(name="timestamp", dtype=DataType.VARCHAR, max_length=32),
        FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=EMBEDDING_DIM),
    ]
    schema = CollectionSchema(fields, description="L3 Wisdom — session episodic memory")
    col = Collection("sessions", schema)
    col.create_index(
        field_name="embedding",
        index_params={
            "metric_type": "COSINE",
            "index_type": "IVF_FLAT",
            "params": {"nlist": 128},
        },
    )
    print("  Created sessions (L3 Wisdom)")
    return col


def drop_all():
    for name in ["tool_calls", "decisions", "sessions"]:
        if utility.has_collection(name):
            utility.drop_collection(name)
            print(f"  Dropped {name}")


def status():
    for name in ["tool_calls", "decisions", "sessions"]:
        if utility.has_collection(name):
            col = Collection(name)
            col.load()
            print(f"  {name}: {col.num_entities} entities, description='{col.description}'")
            # Show index info
            for idx in col.indexes:
                print(f"    index: {idx.params}")
        else:
            print(f"  {name}: NOT FOUND")


def main():
    connect()
    args = sys.argv[1:]

    if "--status" in args:
        print("Milvus collection status:")
        status()
        return

    if "--drop" in args:
        print("Dropping existing collections...")
        drop_all()

    print("Creating Milvus collections...")
    existing = []
    for name in ["tool_calls", "decisions", "sessions"]:
        if utility.has_collection(name):
            existing.append(name)

    if existing:
        print(f"  Already exist: {', '.join(existing)}")
        print(f"  Use --drop to recreate.")
        # Only create missing ones
        if "tool_calls" not in existing:
            create_tool_calls()
        if "decisions" not in existing:
            create_decisions()
        if "sessions" not in existing:
            create_sessions()
    else:
        create_tool_calls()
        create_decisions()
        create_sessions()

    print("\nVerifying...")
    status()
    print("\nDone.")


if __name__ == "__main__":
    main()
