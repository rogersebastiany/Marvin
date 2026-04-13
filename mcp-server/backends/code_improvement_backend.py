"""
Code improvement backend — contrast code against Milvus knowledge.

Four tools:
  - improve_code: per-chunk Milvus matches (what the KB says about your code)
  - tdd: same vector walk but output shaped for test generation —
         includes signatures, docstrings, args, return types, imports.
         Output includes pytest-specific patterns (fixtures, parametrize, markers).
  - score_applicability: behavioral embedding of code flow → Milvus match →
         deterministic classification (ALREADY_APPLIED / APPLICABLE / REFERENCE_ONLY)
  - scan_owasp: AST-based OWASP Top 10 pattern detection + Milvus behavioral
         embedding against security knowledge. Severity-classified findings.

Pure Milvus — no Neo4j. Portable across any Marvin environment.
"""

import ast
import logging
from pathlib import Path

log = logging.getLogger(__name__)

from .memory import (
    _embed,
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

    log.info("tdd: %s → %d units, %d knowledge hits", module_name, len(testable_units), total)

    return {
        "file": str(path),
        "module_name": module_name,
        "imports": imports,
        "testable_units": testable_units,
        "total_knowledge_hits": total,
        "unique_sources": len(seen_keys),
        "pytest_patterns": {
            "fixtures": "Use @pytest.fixture for shared setup (db connections, temp dirs, mock objects). "
                        "Scope options: function (default), class, module, session.",
            "parametrize": "Use @pytest.mark.parametrize('input,expected', [...]) for data-driven tests. "
                          "Reduces test duplication for functions with multiple input/output pairs.",
            "markers": "Use @pytest.mark.slow for long tests, @pytest.mark.integration for external deps. "
                      "Run subsets with pytest -m 'not slow'.",
            "assertions": "Use plain assert with descriptive messages. pytest rewrites assert for rich diffs. "
                         "For exceptions: with pytest.raises(ValueError, match='pattern').",
            "tmp_path": "Use tmp_path fixture for temporary file operations — auto-cleaned after test.",
            "monkeypatch": "Use monkeypatch fixture to mock env vars, attributes, dict items without side effects.",
        },
    }


# ── Behavioral Description ──────────────────────────────────────────────
# Walk the AST and describe what the code DOES as a flow, not what it
# looks like. This produces a natural-language behavioral spec that
# embeds much better against knowledge concepts than raw code.


def _describe_calls(node: ast.AST) -> list[str]:
    """Extract all function/method calls from an AST subtree."""
    calls = []
    for child in ast.walk(node):
        if not isinstance(child, ast.Call):
            continue
        try:
            calls.append(ast.unparse(child.func))
        except Exception:
            pass
    return calls


def _describe_control_flow(node: ast.AST) -> list[str]:
    """Describe control flow patterns in an AST subtree."""
    patterns = []
    for child in ast.walk(node):
        if isinstance(child, ast.Try):
            handlers = []
            for h in child.handlers:
                if h.type:
                    try:
                        handlers.append(ast.unparse(h.type))
                    except Exception:
                        handlers.append("Exception")
                else:
                    handlers.append("Exception")
            patterns.append(f"handles errors: {', '.join(handlers)}")
            if child.finalbody:
                patterns.append("has cleanup in finally block")
        elif isinstance(child, ast.With) or isinstance(child, ast.AsyncWith):
            for item in child.items:
                try:
                    patterns.append(f"uses context manager: {ast.unparse(item.context_expr)}")
                except Exception:
                    patterns.append("uses context manager")
        elif isinstance(child, ast.For) or isinstance(child, ast.AsyncFor):
            try:
                patterns.append(f"iterates over: {ast.unparse(child.iter)}")
            except Exception:
                patterns.append("iterates over collection")
        elif isinstance(child, ast.While):
            patterns.append("loops with condition")
        elif isinstance(child, ast.If):
            try:
                test_str = ast.unparse(child.test)
                if len(test_str) < 80:
                    patterns.append(f"branches on: {test_str}")
            except Exception:
                pass
        elif isinstance(child, ast.Yield) or isinstance(child, ast.YieldFrom):
            patterns.append("yields values (generator)")
        elif isinstance(child, ast.Raise):
            if child.exc:
                try:
                    patterns.append(f"raises: {ast.unparse(child.exc)}")
                except Exception:
                    patterns.append("raises exception")
    return patterns


def _describe_data_flow(node: ast.AST) -> list[str]:
    """Describe data patterns: what is read, transformed, returned."""
    patterns = []
    for child in ast.walk(node):
        if isinstance(child, ast.Return) and child.value:
            try:
                ret = ast.unparse(child.value)
                if len(ret) < 100:
                    patterns.append(f"returns: {ret}")
            except Exception:
                pass
        elif isinstance(child, ast.DictComp):
            patterns.append("builds dictionary comprehension")
        elif isinstance(child, ast.ListComp):
            patterns.append("builds list comprehension")
        elif isinstance(child, ast.SetComp):
            patterns.append("builds set comprehension")
    return patterns


def _behavioral_description(chunk: dict, file_imports: list[str]) -> str:
    """Generate a behavioral description of a code chunk from its AST.

    Produces a natural-language flow description:
      "async function that receives X, validates Y, calls Z, handles E, returns W"

    This embeds against Milvus concepts much better than raw code because
    it captures WHAT the code does, not syntactic noise.
    """
    code = chunk["code"]
    name = chunk["name"]
    kind = chunk["kind"]

    try:
        tree = ast.parse(code)
    except SyntaxError:
        return f"{kind} {name}: {code[:200]}"

    # Get the top-level node
    top_nodes = [n for n in ast.iter_child_nodes(tree)
                 if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))]
    if not top_nodes:
        return f"{kind} {name}: {code[:200]}"

    node = top_nodes[0]
    parts = []

    # Identity
    if isinstance(node, ast.AsyncFunctionDef):
        parts.append(f"async function '{name}'")
    elif isinstance(node, ast.FunctionDef):
        parts.append(f"function '{name}'")
    elif isinstance(node, ast.ClassDef):
        bases = [ast.unparse(b) for b in node.bases] if node.bases else []
        if bases:
            parts.append(f"class '{name}' extending {', '.join(bases)}")
        else:
            parts.append(f"class '{name}'")

    # Docstring as intent
    docstring = ast.get_docstring(node)
    if docstring:
        first_line = docstring.strip().split("\n")[0]
        parts.append(f"purpose: {first_line}")

    # Parameters (what it receives)
    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
        sig = _extract_signature(node)
        param_descs = []
        for arg in sig["args"]:
            if arg["name"] == "self":
                continue
            desc = arg["name"]
            if arg["annotation"]:
                desc += f": {arg['annotation']}"
            param_descs.append(desc)
        if param_descs:
            parts.append(f"receives: {', '.join(param_descs)}")
        if sig["return_type"]:
            parts.append(f"return type: {sig['return_type']}")
        if sig["decorators"]:
            parts.append(f"decorated with: {', '.join(sig['decorators'])}")

    # What it calls
    calls = _describe_calls(node)
    if calls:
        unique_calls = list(dict.fromkeys(calls))[:15]
        parts.append(f"calls: {', '.join(unique_calls)}")

    # Control flow
    flow = _describe_control_flow(node)
    if flow:
        unique_flow = list(dict.fromkeys(flow))[:10]
        parts.append(f"flow: {'; '.join(unique_flow)}")

    # Data patterns
    data = _describe_data_flow(node)
    if data:
        unique_data = list(dict.fromkeys(data))[:5]
        parts.append(f"data: {'; '.join(unique_data)}")

    # Relevant imports (what libraries this code depends on)
    if file_imports:
        # Only include imports that are actually referenced in this chunk
        code_text = chunk["code"]
        relevant = [imp for imp in file_imports if any(
            token in code_text for token in imp.split()
            if token not in ("import", "from", "as", ".")
        )]
        if relevant:
            parts.append(f"imports: {'; '.join(relevant[:10])}")

    # For classes, describe methods as sub-behaviors
    if isinstance(node, ast.ClassDef):
        methods = chunk.get("methods", [])
        if methods:
            method_names = [m["name"] for m in methods if not m["name"].startswith("_")]
            if method_names:
                parts.append(f"public methods: {', '.join(method_names[:10])}")

    return ". ".join(parts)


def score_applicability(
    file_path: str,
    k_per_collection: int = 5,
    behavior_threshold: float = 0.40,
    code_threshold: float = 0.35,
) -> dict:
    """Behavioral embedding of code → Milvus → applicability classification.

    For each code chunk:
      1. Generate behavioral description from AST (what the code DOES)
      2. Embed the behavioral description → search Milvus (behavior matches)
      3. Embed the raw code → search Milvus (code matches, like improve_code)
      4. Cross-reference: concepts found by BOTH embeddings with high behavior
         score are APPLICABLE. Concepts found by code but not behavior are
         REFERENCE_ONLY. Concepts where code already shows implementation
         indicators are ALREADY_APPLIED.

    The behavioral embedding is the key insight: it matches against what
    the code DOES (its flow, its patterns, its responsibilities), not what
    it looks like syntactically. This makes the ontology actionable.

    Returns:
      {
        "file": str,
        "chunks": [
          {
            "name": str,
            "kind": str,
            "lineno": int,
            "behavioral_description": str,
            "applicable": [{"concept": str, "score": float, "reason": str}],
            "already_applied": [{"concept": str, "score": float, "indicator": str}],
            "reference_only": [{"concept": str, "score": float}],
          }
        ],
        "summary": {
          "total_applicable": int,
          "total_already_applied": int,
          "total_reference_only": int,
        }
      }
    """
    path = Path(file_path)
    if not path.is_file():
        return {"error": f"File not found: {file_path}"}

    source = path.read_text(encoding="utf-8", errors="replace")
    if not source.strip():
        return {"error": f"File is empty: {file_path}"}

    code_chunks = _chunk_code_by_ast(source, str(path))
    file_imports = _extract_imports(source)

    # Generate behavioral descriptions for each chunk
    behaviors = [_behavioral_description(c, file_imports) for c in code_chunks]

    # Embed both: behavioral descriptions AND raw code
    behavior_vecs = _embed_batch([b[:8000] for b in behaviors])
    code_vecs = _embed_batch([c["code"][:8000] for c in code_chunks])

    k = max(1, min(k_per_collection, 20))
    result_chunks = []
    totals = {"applicable": 0, "already_applied": 0, "reference_only": 0}

    for chunk, behavior, bvec, cvec in zip(code_chunks, behaviors, behavior_vecs, code_vecs):
        # Collect matches from both embeddings (concepts collection only for classification)
        behavior_hits = {}  # concept_name → {score, summary}
        code_hits = {}      # concept_name → {score, summary}

        concept_fields = _RESSALVA_COLLECTIONS["concepts"]

        # Behavior embedding matches
        for h in _search_by_vector("concepts", bvec, k, concept_fields):
            if h["score"] >= behavior_threshold:
                behavior_hits[h.get("name", "")] = {
                    "score": round(h["score"], 4),
                    "summary": h.get("summary", ""),
                }

        # Code embedding matches
        for h in _search_by_vector("concepts", cvec, k, concept_fields):
            if h["score"] >= code_threshold:
                code_hits[h.get("name", "")] = {
                    "score": round(h["score"], 4),
                    "summary": h.get("summary", ""),
                }

        # Also search doc_chunks and decisions with behavior embedding
        # These provide additional context for applicability
        doc_behavior_hits = []
        for col in ("doc_chunks", "decisions"):
            fields = _RESSALVA_COLLECTIONS[col]
            for h in _search_by_vector(col, bvec, k, fields):
                if h["score"] >= behavior_threshold:
                    doc_behavior_hits.append({
                        "collection": col,
                        "score": round(h["score"], 4),
                        "summary": _format_ressalva(col, h),
                    })

        # Classify each concept
        all_concepts = set(behavior_hits.keys()) | set(code_hits.keys())
        applicable = []
        already_applied = []
        reference_only = []

        code_text_lower = chunk["code"].lower()

        for concept_name in all_concepts:
            if not concept_name:
                continue

            in_behavior = concept_name in behavior_hits
            in_code = concept_name in code_hits
            b_score = behavior_hits.get(concept_name, {}).get("score", 0)
            c_score = code_hits.get(concept_name, {}).get("score", 0)
            summary = (behavior_hits.get(concept_name) or code_hits.get(concept_name, {})).get("summary", "")

            # Check if the concept name or key terms appear literally in the code
            # This is the "already applied" signal — the code references it directly
            concept_tokens = concept_name.lower().replace("-", " ").replace("_", " ").split()
            # A concept is considered present if its name tokens appear in the code
            # (handles: lru_cache matches "LRU Cache", retry matches "Retry Pattern")
            tokens_found = sum(1 for t in concept_tokens if t in code_text_lower and len(t) > 2)
            token_ratio = tokens_found / max(len(concept_tokens), 1)

            if token_ratio >= 0.5 and c_score > 0:
                # Code already references this concept — likely implemented
                already_applied.append({
                    "concept": concept_name,
                    "score": max(b_score, c_score),
                    "indicator": f"code contains {tokens_found}/{len(concept_tokens)} concept tokens",
                    "summary": summary,
                })
            elif in_behavior and b_score >= behavior_threshold:
                # Behavior matches — the code DOES something this concept addresses
                applicable.append({
                    "concept": concept_name,
                    "behavior_score": b_score,
                    "code_score": c_score,
                    "summary": summary,
                })
            else:
                # Only found by code embedding — syntactically close but not behaviorally
                reference_only.append({
                    "concept": concept_name,
                    "score": c_score or b_score,
                    "summary": summary,
                })

        # Sort by score descending
        applicable.sort(key=lambda x: x["behavior_score"], reverse=True)
        already_applied.sort(key=lambda x: x["score"], reverse=True)
        reference_only.sort(key=lambda x: x["score"], reverse=True)

        totals["applicable"] += len(applicable)
        totals["already_applied"] += len(already_applied)
        totals["reference_only"] += len(reference_only)

        result_chunks.append({
            "name": chunk["name"],
            "kind": chunk["kind"],
            "lineno": chunk["lineno"],
            "behavioral_description": behavior,
            "applicable": applicable,
            "already_applied": already_applied,
            "reference_only": reference_only,
            "supporting_knowledge": doc_behavior_hits[:5],
        })

    return {
        "file": str(path),
        "chunks": result_chunks,
        "summary": {
            "total_applicable": totals["applicable"],
            "total_already_applied": totals["already_applied"],
            "total_reference_only": totals["reference_only"],
        },
    }


# ── OWASP Top 10 Scanner ──────────────────────────────────────────────
# Static AST pattern detection + Milvus behavioral embedding against
# OWASP security knowledge. Designed to run as the final step in
# improvement chains (tdd_improve, full_improvement).

# Each rule: (id, owasp_category, severity, description, AST detector)
# Detectors receive an ast.AST node and return a match string or None.

_OWASP_RULES: list[dict] = []


def _register_rule(owasp_id: str, category: str, severity: str, description: str):
    """Decorator to register an OWASP detection rule."""
    def decorator(fn):
        _OWASP_RULES.append({
            "owasp_id": owasp_id,
            "category": category,
            "severity": severity,
            "description": description,
            "detector": fn,
        })
        return fn
    return decorator


@_register_rule("A03", "Injection", "CRITICAL",
                 "SQL injection via string formatting — use parameterized queries")
def _detect_sql_injection(node: ast.AST) -> str | None:
    """Detect SQL queries built with f-strings, format(), or concatenation."""
    if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Module)):
        return None

    for child in ast.walk(node):
        # f-string containing SQL keywords
        if isinstance(child, ast.JoinedStr):
            try:
                parts = [ast.unparse(v) for v in child.values if isinstance(v, ast.FormattedValue)]
                full = ast.unparse(child)
            except Exception:
                continue
            sql_kw = ("select ", "insert ", "update ", "delete ", "drop ", "where ", "from ")
            if any(kw in full.lower() for kw in sql_kw) and parts:
                return f"f-string with SQL keywords and interpolated values: {full[:120]}"

        # "SELECT ... " + variable or "SELECT ... ".format(...)
        if isinstance(child, ast.BinOp) and isinstance(child.op, ast.Add):
            try:
                left = ast.unparse(child.left).lower()
            except Exception:
                continue
            sql_kw = ("select ", "insert ", "update ", "delete ", "drop ", "where ")
            if any(kw in left for kw in sql_kw):
                return f"string concatenation in SQL query: {left[:120]}"

        if isinstance(child, ast.Call):
            try:
                func_str = ast.unparse(child.func)
            except Exception:
                continue
            if func_str.endswith(".format"):
                try:
                    obj = ast.unparse(child.func.value).lower() if hasattr(child.func, 'value') else ""
                except Exception:
                    obj = ""
                sql_kw = ("select ", "insert ", "update ", "delete ", "drop ", "where ")
                if any(kw in obj for kw in sql_kw):
                    return f".format() on SQL string: {obj[:120]}"

    return None


@_register_rule("A03", "Injection", "CRITICAL",
                 "Command injection via subprocess/os with shell=True or os.system")
def _detect_command_injection(node: ast.AST) -> str | None:
    """Detect shell=True in subprocess calls or os.system usage."""
    for child in ast.walk(node):
        if not isinstance(child, ast.Call):
            continue
        try:
            func_str = ast.unparse(child.func)
        except Exception:
            continue

        # os.system(...)
        if func_str in ("os.system", "os.popen"):
            return f"{func_str}() call — use subprocess with shell=False"

        # subprocess.*(... shell=True ...)
        if func_str.startswith("subprocess."):
            for kw in child.keywords:
                if kw.arg == "shell":
                    try:
                        if isinstance(kw.value, ast.Constant) and kw.value.value is True:
                            return f"{func_str}(shell=True) — avoid shell=True with user input"
                    except Exception:
                        pass
    return None


@_register_rule("A01", "Broken Access Control", "HIGH",
                 "Path traversal — user input in file paths without sanitization")
def _detect_path_traversal(node: ast.AST) -> str | None:
    """Detect open()/Path() with unsanitized variables that could allow ../."""
    for child in ast.walk(node):
        if not isinstance(child, ast.Call):
            continue
        try:
            func_str = ast.unparse(child.func)
        except Exception:
            continue

        if func_str in ("open", "Path", "pathlib.Path"):
            if child.args:
                arg = child.args[0]
                # f-string or format call in file path argument
                if isinstance(arg, ast.JoinedStr):
                    return f"f-string in {func_str}() path — validate/sanitize path components"
                if isinstance(arg, ast.BinOp) and isinstance(arg.op, ast.Add):
                    return f"concatenation in {func_str}() path — validate/sanitize path components"
    return None


@_register_rule("A07", "Security Misconfiguration", "HIGH",
                 "Hardcoded secrets — credentials, keys, tokens in source code")
def _detect_hardcoded_secrets(node: ast.AST) -> str | None:
    """Detect assignments of string literals to variables with secret-like names."""
    secret_patterns = ("password", "secret", "api_key", "apikey", "token", "private_key",
                       "auth_token", "access_key", "secret_key", "db_pass")

    for child in ast.walk(node):
        if not isinstance(child, ast.Assign):
            continue
        for target in child.targets:
            if not isinstance(target, ast.Name):
                continue
            name_lower = target.id.lower()
            if any(pat in name_lower for pat in secret_patterns):
                if isinstance(child.value, ast.Constant) and isinstance(child.value.value, str):
                    val = child.value.value
                    if len(val) >= 4 and val not in ("", "None", "null", "TODO", "CHANGEME"):
                        return f"hardcoded string in '{target.id}' — use environment variables"
    return None


@_register_rule("A02", "Cryptographic Failures", "HIGH",
                 "Weak hashing — MD5/SHA1 for security purposes")
def _detect_weak_hashing(node: ast.AST) -> str | None:
    """Detect use of MD5 or SHA1 which are cryptographically broken."""
    for child in ast.walk(node):
        if not isinstance(child, ast.Call):
            continue
        try:
            func_str = ast.unparse(child.func)
        except Exception:
            continue

        if func_str in ("hashlib.md5", "hashlib.sha1"):
            return f"{func_str}() — use SHA-256+ for security-sensitive hashing"
        if func_str == "hashlib.new" and child.args:
            try:
                algo = ast.unparse(child.args[0]).strip("'\"").lower()
                if algo in ("md5", "sha1"):
                    return f"hashlib.new('{algo}') — use SHA-256+ for security-sensitive hashing"
            except Exception:
                pass
    return None


@_register_rule("A08", "Software and Data Integrity Failures", "MEDIUM",
                 "Unsafe deserialization — pickle/yaml.load without safe loader")
def _detect_unsafe_deserialization(node: ast.AST) -> str | None:
    """Detect pickle.load/loads and yaml.load without SafeLoader."""
    for child in ast.walk(node):
        if not isinstance(child, ast.Call):
            continue
        try:
            func_str = ast.unparse(child.func)
        except Exception:
            continue

        if func_str in ("pickle.load", "pickle.loads"):
            return f"{func_str}() — pickle is unsafe with untrusted data"

        if func_str == "yaml.load":
            has_safe_loader = False
            for kw in child.keywords:
                if kw.arg == "Loader":
                    try:
                        loader = ast.unparse(kw.value)
                        if "Safe" in loader:
                            has_safe_loader = True
                    except Exception:
                        pass
            if not has_safe_loader:
                return "yaml.load() without SafeLoader — use yaml.safe_load()"
    return None


@_register_rule("A05", "Security Misconfiguration", "MEDIUM",
                 "Debug mode enabled — Flask/Django debug=True in production code")
def _detect_debug_mode(node: ast.AST) -> str | None:
    """Detect debug=True in web framework calls."""
    for child in ast.walk(node):
        if not isinstance(child, ast.Call):
            continue
        try:
            func_str = ast.unparse(child.func)
        except Exception:
            continue

        if func_str in ("app.run", "Flask.run", "uvicorn.run"):
            for kw in child.keywords:
                if kw.arg == "debug":
                    if isinstance(kw.value, ast.Constant) and kw.value.value is True:
                        return f"{func_str}(debug=True) — disable debug mode in production"
    return None


@_register_rule("A09", "Security Logging and Monitoring Failures", "MEDIUM",
                 "Sensitive data in logs — logging passwords, tokens, or keys")
def _detect_sensitive_logging(node: ast.AST) -> str | None:
    """Detect logging calls that may include sensitive variable names."""
    sensitive = ("password", "secret", "token", "api_key", "private_key", "credential")

    for child in ast.walk(node):
        if not isinstance(child, ast.Call):
            continue
        try:
            func_str = ast.unparse(child.func)
        except Exception:
            continue

        if not any(func_str.endswith(f".{level}") for level in
                   ("debug", "info", "warning", "error", "critical", "exception")):
            continue
        if not func_str.startswith(("log.", "logger.", "logging.")):
            continue

        # Check if any argument references sensitive names
        for arg in child.args:
            try:
                arg_str = ast.unparse(arg).lower()
                for s in sensitive:
                    if s in arg_str:
                        return f"logging potentially sensitive data '{s}' via {func_str}"
            except Exception:
                pass
    return None


@_register_rule("A06", "Vulnerable and Outdated Components", "LOW",
                 "eval()/exec() usage — arbitrary code execution risk")
def _detect_eval_exec(node: ast.AST) -> str | None:
    """Detect eval() and exec() calls."""
    for child in ast.walk(node):
        if not isinstance(child, ast.Call):
            continue
        try:
            func_str = ast.unparse(child.func)
        except Exception:
            continue

        if func_str in ("eval", "exec"):
            return f"{func_str}() call — avoid with untrusted input, use ast.literal_eval() if needed"
    return None


def _run_static_rules(source: str, file_path: str) -> list[dict]:
    """Run all registered OWASP rules against the source AST.

    Returns a list of findings, each with owasp_id, category, severity,
    location (function/class name + line), and detail.
    """
    try:
        tree = ast.parse(source, filename=file_path)
    except SyntaxError:
        return [{"owasp_id": "N/A", "category": "Parse Error", "severity": "LOW",
                 "location": file_path, "detail": "Could not parse file — SyntaxError"}]

    findings = []

    # Run rules against each top-level function/class
    for node in ast.iter_child_nodes(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            scope_name = f"{node.name}() line {node.lineno}"
        elif isinstance(node, ast.ClassDef):
            scope_name = f"class {node.name} line {node.lineno}"
        else:
            continue

        for rule in _OWASP_RULES:
            detail = rule["detector"](node)
            if detail:
                findings.append({
                    "owasp_id": rule["owasp_id"],
                    "category": rule["category"],
                    "severity": rule["severity"],
                    "description": rule["description"],
                    "location": scope_name,
                    "detail": detail,
                })

    # Also run rules at module level (for top-level assignments like hardcoded secrets)
    for rule in _OWASP_RULES:
        detail = rule["detector"](tree)
        if detail:
            # Avoid duplicating findings already caught at function scope
            if not any(f["detail"] == detail for f in findings):
                findings.append({
                    "owasp_id": rule["owasp_id"],
                    "category": rule["category"],
                    "severity": rule["severity"],
                    "description": rule["description"],
                    "location": "module level",
                    "detail": detail,
                })

    return findings


def scan_owasp(
    file_path: str,
    k_per_collection: int = 5,
    behavior_threshold: float = 0.40,
) -> dict:
    """OWASP Top 10 vulnerability scanner — static patterns + Milvus security knowledge.

    Two-layer analysis:
      1. Static AST rules — detect known dangerous patterns (SQL injection,
         command injection, path traversal, hardcoded secrets, weak crypto,
         unsafe deserialization, debug mode, sensitive logging, eval/exec).
      2. Behavioral embedding — embed each code chunk's security-relevant
         behavior against Milvus OWASP/security knowledge for deeper matches
         that static rules can't catch.

    Severity classification: CRITICAL, HIGH, MEDIUM, LOW.

    Designed to run as the final step in tdd_improve and full_improvement
    chains — after code is improved and tests pass, scan for security debt.

    Returns:
      {
        "file": str,
        "static_findings": [...],
        "behavioral_findings": [...],
        "summary": {
          "total_findings": int,
          "by_severity": {"CRITICAL": int, "HIGH": int, "MEDIUM": int, "LOW": int},
          "by_category": {"Injection": int, ...},
          "risk_level": "CLEAN" | "LOW" | "MEDIUM" | "HIGH" | "CRITICAL",
        },
      }
    """
    path = Path(file_path)
    if not path.is_file():
        return {"error": f"File not found: {file_path}"}

    source = path.read_text(encoding="utf-8", errors="replace")
    if not source.strip():
        return {"error": f"File is empty: {file_path}"}

    # Layer 1: Static AST pattern detection
    static_findings = _run_static_rules(source, str(path))

    # Layer 2: Behavioral embedding against Milvus security knowledge
    code_chunks = _chunk_code_by_ast(source, str(path))
    file_imports = _extract_imports(source)

    # Build security-focused behavioral descriptions
    security_prefix = "security analysis of "
    behaviors = [security_prefix + _behavioral_description(c, file_imports) for c in code_chunks]
    behavior_vecs = _embed_batch([b[:8000] for b in behaviors])

    k = max(1, min(k_per_collection, 20))
    behavioral_findings = []

    # Security-relevant keywords to filter Milvus matches
    security_terms = frozenset({
        "owasp", "security", "injection", "authentication", "authorization",
        "access control", "cryptograph", "encrypt", "hash", "session",
        "xss", "csrf", "vulnerability", "exploit", "sanitiz", "validat",
        "credential", "password", "token", "secret", "certificate",
        "tls", "ssl", "cors", "cwe", "attack", "threat", "risk",
        "firewall", "audit", "compliance", "identity", "proofing",
    })

    for chunk, bvec in zip(code_chunks, behavior_vecs):
        for col_name, fields in _RESSALVA_COLLECTIONS.items():
            hits = _search_by_vector(col_name, bvec, k, fields)
            for h in hits:
                if h["score"] < behavior_threshold:
                    continue
                summary = _format_ressalva(col_name, h)
                summary_lower = summary.lower()
                # Only include security-relevant matches
                if any(term in summary_lower for term in security_terms):
                    behavioral_findings.append({
                        "collection": col_name,
                        "score": round(h["score"], 4),
                        "summary": summary,
                        "code_location": f"{chunk['name']} line {chunk['lineno']}",
                    })

    # Deduplicate behavioral findings by summary
    seen_summaries: set[str] = set()
    unique_behavioral = []
    for bf in behavioral_findings:
        if bf["summary"] not in seen_summaries:
            seen_summaries.add(bf["summary"])
            unique_behavioral.append(bf)
    behavioral_findings = unique_behavioral

    # Build summary
    all_findings = static_findings + [
        {"severity": "MEDIUM", "category": "Knowledge-Based", **bf}
        for bf in behavioral_findings
    ]

    by_severity = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0}
    by_category: dict[str, int] = {}
    for f in static_findings:
        by_severity[f["severity"]] = by_severity.get(f["severity"], 0) + 1
        by_category[f["category"]] = by_category.get(f["category"], 0) + 1
    for _ in behavioral_findings:
        by_severity["MEDIUM"] += 1
        by_category["Knowledge-Based"] = by_category.get("Knowledge-Based", 0) + 1

    # Risk level: highest severity found
    if by_severity["CRITICAL"] > 0:
        risk_level = "CRITICAL"
    elif by_severity["HIGH"] > 0:
        risk_level = "HIGH"
    elif by_severity["MEDIUM"] > 0:
        risk_level = "MEDIUM"
    elif by_severity["LOW"] > 0:
        risk_level = "LOW"
    else:
        risk_level = "CLEAN"

    total = len(static_findings) + len(behavioral_findings)

    log.info("scan_owasp: %s → %d static, %d behavioral, risk=%s",
             path.name, len(static_findings), len(behavioral_findings), risk_level)

    return {
        "file": str(path),
        "static_findings": static_findings,
        "behavioral_findings": behavioral_findings,
        "summary": {
            "total_findings": total,
            "by_severity": by_severity,
            "by_category": by_category,
            "risk_level": risk_level,
        },
    }
