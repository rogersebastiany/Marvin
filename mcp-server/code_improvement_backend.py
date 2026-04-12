"""
Code improvement backend — contrast code against Milvus knowledge.

Two tools:
  - improve_code: per-chunk Milvus matches (what the KB says about your code)
  - tdd: same vector walk but output shaped for test generation —
         includes signatures, docstrings, args, return types, imports

Pure Milvus — no Neo4j. Portable across any Marvin environment.
"""

import ast
from pathlib import Path

from memory import (
    _embed_batch,
    _format_ressalva,
    _RESSALVA_COLLECTIONS,
    _search_by_vector,
)


def _unparse_annotation(node) -> str | None:
    """Best-effort unparse of a type annotation AST node."""
    if node is None:
        return None
    try:
        return ast.unparse(node)
    except Exception:
        return None


def _extract_signature(node: ast.FunctionDef | ast.AsyncFunctionDef) -> dict:
    """Extract function signature metadata from an AST node."""
    args = []
    for arg in node.args.args:
        args.append({
            "name": arg.arg,
            "annotation": _unparse_annotation(arg.annotation),
        })

    defaults_offset = len(node.args.args) - len(node.args.defaults)
    for i, default in enumerate(node.args.defaults):
        try:
            args[defaults_offset + i]["default"] = ast.unparse(default)
        except Exception:
            pass

    return {
        "args": args,
        "return_type": _unparse_annotation(node.returns),
        "is_async": isinstance(node, ast.AsyncFunctionDef),
        "decorators": [ast.unparse(d) for d in node.decorator_list],
    }


def _extract_class_methods(node: ast.ClassDef, lines: list[str]) -> list[dict]:
    """Extract method metadata from a class node."""
    methods = []
    for child in ast.iter_child_nodes(node):
        if not isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        start = child.lineno - 1
        end = child.end_lineno if child.end_lineno else start + 1
        methods.append({
            "name": child.name,
            "signature": _extract_signature(child),
            "docstring": ast.get_docstring(child),
            "lineno": child.lineno,
            "code": "".join(lines[start:end]),
        })
    return methods


def _chunk_code_by_ast(source: str, file_path: str) -> list[dict]:
    """Split Python source into chunks by top-level functions and classes.

    Falls back to whole-file if AST parsing fails or for non-Python files.
    Returns rich chunks with signature/docstring metadata for tdd.
    """
    if not file_path.endswith(".py"):
        return [{"name": file_path, "kind": "file", "code": source, "lineno": 1}]

    try:
        tree = ast.parse(source)
    except SyntaxError:
        return [{"name": file_path, "kind": "file", "code": source, "lineno": 1}]

    lines = source.splitlines(keepends=True)
    chunks = []

    for node in ast.iter_child_nodes(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            kind = "function"
        elif isinstance(node, ast.ClassDef):
            kind = "class"
        else:
            continue

        start = node.lineno - 1
        end = node.end_lineno if node.end_lineno else start + 1
        code = "".join(lines[start:end])

        chunk = {
            "name": node.name,
            "kind": kind,
            "code": code,
            "lineno": node.lineno,
            "docstring": ast.get_docstring(node),
        }

        if kind == "function":
            chunk["signature"] = _extract_signature(node)
        elif kind == "class":
            chunk["bases"] = [ast.unparse(b) for b in node.bases],
            chunk["methods"] = _extract_class_methods(node, lines)

        chunks.append(chunk)

    if not chunks:
        return [{"name": file_path, "kind": "file", "code": source, "lineno": 1}]

    return chunks


def _extract_imports(source: str) -> list[str]:
    """Extract all import statements from source."""
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return []

    imports = []
    for node in ast.iter_child_nodes(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            imports.append(ast.unparse(node))
    return imports


def improve_code(
    file_path: str,
    k_per_collection: int = 5,
    score_threshold: float = 0.35,
) -> dict:
    """Read a file, chunk by AST, embed each chunk, search all Milvus collections.

    Returns per-chunk matches from concepts, decisions, sessions, doc_chunks, plans.

    Returns:
      {
        "file": str,
        "chunks": [
          {
            "name": str,
            "kind": str,
            "lineno": int,
            "matches": [{"collection": str, "score": float, "summary": str, ...}, ...]
          },
          ...
        ],
        "total_matches": int,
        "unique_sources": int,
      }
    """
    path = Path(file_path)
    if not path.is_file():
        return {"error": f"File not found: {file_path}"}

    source = path.read_text(encoding="utf-8", errors="replace")
    if not source.strip():
        return {"error": f"File is empty: {file_path}"}

    code_chunks = _chunk_code_by_ast(source, str(path))

    texts_to_embed = [c["code"][:8000] for c in code_chunks]
    vectors = _embed_batch(texts_to_embed)

    k_per_collection = max(1, min(k_per_collection, 20))
    seen_keys: set[tuple] = set()
    result_chunks = []

    for chunk, vec in zip(code_chunks, vectors):
        chunk_matches = []

        for col_name, fields in _RESSALVA_COLLECTIONS.items():
            hits = _search_by_vector(col_name, vec, k_per_collection, fields)
            for h in hits:
                if h["score"] < score_threshold:
                    continue
                summary = _format_ressalva(col_name, h)
                chunk_matches.append({
                    "collection": col_name,
                    "score": round(h["score"], 4),
                    "summary": summary,
                    **{k: h.get(k) for k in fields},
                })
                key_field = (
                    h.get("name") or h.get("objective")
                    or h.get("doc_name") or h.get("title") or ""
                )
                seen_keys.add((col_name, key_field))

        result_chunks.append({
            "name": chunk["name"],
            "kind": chunk["kind"],
            "lineno": chunk["lineno"],
            "matches": chunk_matches,
        })

    total = sum(len(c["matches"]) for c in result_chunks)
    return {
        "file": str(path),
        "chunks": result_chunks,
        "total_matches": total,
        "unique_sources": len(seen_keys),
    }


def tdd(
    file_path: str,
    k_per_collection: int = 5,
    score_threshold: float = 0.35,
) -> dict:
    """Code + Milvus knowledge → structured context for test generation.

    Same vector walk as improve_code, but output is shaped for writing tests:
    - Function signatures, args, return types, decorators
    - Class methods with their own signatures
    - Docstrings (the contract the test should verify)
    - Imports (so the agent knows what to import in the test file)
    - Per-chunk Milvus matches grouped as "behavioral expectations" —
      what the knowledge base says this code should do

    The tool does the tautological retrieval. The agent writes the tests.

    Returns:
      {
        "file": str,
        "module_name": str,
        "imports": [str],
        "testable_units": [
          {
            "name": str,
            "kind": "function" | "class",
            "lineno": int,
            "signature": {...} | None,
            "docstring": str | None,
            "methods": [...] | None,  # for classes
            "knowledge": [
              {"collection": str, "score": float, "summary": str, ...}
            ],
          }
        ],
        "total_knowledge_hits": int,
        "unique_sources": int,
      }
    """
    path = Path(file_path)
    if not path.is_file():
        return {"error": f"File not found: {file_path}"}

    source = path.read_text(encoding="utf-8", errors="replace")
    if not source.strip():
        return {"error": f"File is empty: {file_path}"}

    code_chunks = _chunk_code_by_ast(source, str(path))
    imports = _extract_imports(source)

    # Embed all chunks in one batch
    texts_to_embed = [c["code"][:8000] for c in code_chunks]
    vectors = _embed_batch(texts_to_embed)

    k_per_collection = max(1, min(k_per_collection, 20))
    seen_keys: set[tuple] = set()
    testable_units = []

    for chunk, vec in zip(code_chunks, vectors):
        knowledge = []

        for col_name, fields in _RESSALVA_COLLECTIONS.items():
            hits = _search_by_vector(col_name, vec, k_per_collection, fields)
            for h in hits:
                if h["score"] < score_threshold:
                    continue
                summary = _format_ressalva(col_name, h)
                knowledge.append({
                    "collection": col_name,
                    "score": round(h["score"], 4),
                    "summary": summary,
                    **{k: h.get(k) for k in fields},
                })
                key_field = (
                    h.get("name") or h.get("objective")
                    or h.get("doc_name") or h.get("title") or ""
                )
                seen_keys.add((col_name, key_field))

        unit = {
            "name": chunk["name"],
            "kind": chunk["kind"],
            "lineno": chunk["lineno"],
            "docstring": chunk.get("docstring"),
            "signature": chunk.get("signature"),
            "methods": chunk.get("methods"),
            "knowledge": knowledge,
        }
        testable_units.append(unit)

    total = sum(len(u["knowledge"]) for u in testable_units)

    # Module name for import in test file
    module_name = path.stem

    return {
        "file": str(path),
        "module_name": module_name,
        "imports": imports,
        "testable_units": testable_units,
        "total_knowledge_hits": total,
        "unique_sources": len(seen_keys),
    }
