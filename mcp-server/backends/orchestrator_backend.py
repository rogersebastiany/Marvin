"""
Orchestrator backend — goal-driven tool chain planner.

Takes a prompt, matches it against known tool chains, and returns
a structured execution plan that any MCP client can follow.

LLM-agnostic: Claude Code, Cursor, Windsurf, brain.py — they all
get the same plan, same gates, same step dependencies.
"""

from .memory import _embed, _search_by_vector, _RESSALVA_COLLECTIONS, _format_ressalva


# ── Tool Chain Definitions ───────────────────────────────────────────────
# Each chain: triggers (keywords that activate it), steps, and description.

CHAINS = {
    "tdd_improve": {
        "description": "TDD-guarded code improvement: lock behavior with tests, improve code, verify tests still pass",
        "triggers": ["improve", "refactor", "tdd", "test", "safe change", "improve code"],
        "requires": ["file_path"],
        "steps": [
            {
                "id": 1,
                "tool": "tdd",
                "args_template": {"file_path": "{file_path}"},
                "description": "Analyze code against Milvus knowledge — get signatures, docstrings, and behavioral expectations for test generation",
            },
            {
                "id": 2,
                "action": "write_tests",
                "input_from": 1,
                "description": "Write pytest tests based on tdd output: one test per function/class, covering the behavioral expectations from Milvus knowledge",
                "instruction": "Write tests to a file named test_{module_name}.py. Tests must verify CURRENT behavior — they are a safety net, not aspirational.",
            },
            {
                "id": 3,
                "action": "run_tests",
                "gate": "tests_pass",
                "description": "Run pytest on the generated test file. ALL tests must pass before proceeding. If any fail, fix the tests (not the code) — they must reflect current behavior.",
                "command_template": "pytest {test_file} -v",
            },
            {
                "id": 4,
                "tool": "improve_code",
                "args_template": {"file_path": "{file_path}"},
                "description": "Get Milvus knowledge matches per code chunk — what the KB says about each function/class",
            },
            {
                "id": 5,
                "action": "apply_improvements",
                "input_from": 4,
                "description": "Apply code improvements based on improve_code knowledge matches. Change implementation, not contracts. Do not change function signatures or behavior that tests verify.",
            },
            {
                "id": 6,
                "action": "run_tests",
                "gate": "tests_pass",
                "description": "Run the SAME tests again. If any fail, the improvement broke behavior — revert or fix the improvement, not the tests.",
                "command_template": "pytest {test_file} -v",
            },
            {
                "id": 7,
                "action": "create_issue",
                "input_from": [4, 6],
                "description": "Create a GitHub issue with the improvement summary: what was changed, which KB knowledge motivated each change, and test results. Use `gh issue create`.",
            },
        ],
    },
    "research": {
        "description": "Knowledge-enriched research: rank URLs, fetch, consolidate, extract keywords, fill knowledge gaps, sync",
        "triggers": ["research", "docs", "documentation", "fetch", "learn about"],
        "requires": ["urls", "topic"],
        "steps": [
            {
                "id": 1,
                "tool": "rank_urls",
                "args_template": {"urls": "{urls}"},
                "description": "Probe URLs and score documentation quality. Only URLs scoring 60+ are worth fetching.",
            },
            {
                "id": 2,
                "action": "filter_urls",
                "input_from": 1,
                "gate": "score_above_60",
                "description": "Filter rank_urls output — keep only URLs with score >= 60. If none pass, report to user and stop.",
            },
            {
                "id": 3,
                "tool": "research_topic",
                "args_template": {"urls": "{filtered_urls}", "topic": "{topic}"},
                "description": "Fetch filtered URLs, merge into a single consolidated doc with bibliography.",
            },
            {
                "id": 4,
                "tool": "extract_keywords",
                "args_template": {"doc_path": "{saved_doc_filename}"},
                "description": "Extract keyword candidates from the new doc — underlying concepts, technologies, abstractions.",
            },
            {
                "id": 5,
                "tool": "classify_keywords",
                "args_template": {"keywords_json": "{step_4_keywords}", "semantic_threshold": 0.45},
                "description": (
                    "Three-tier classification against Milvus:\n"
                    "  (a) EXACT MATCH (name exists in graph) → skip, concept already known.\n"
                    "  (b) SEMANTIC MATCH (score >= 0.45, no exact name) → enrich: the matched concepts "
                    "are CLOSE but incomplete. `link` the new keyword to the matched concept, or `expand` "
                    "the matched concept's description to incorporate the finding. These near-misses reveal "
                    "which generalist concepts should absorb the new knowledge.\n"
                    "  (c) TRUE GAP (score < 0.45) → collect for step 6: this concept needs proper research."
                ),
            },
            {
                "id": 6,
                "action": "enrich_semantic_matches",
                "input_from": [4, 5],
                "description": (
                    "For each SEMANTIC MATCH from step 5b: `link` the keyword to the matched concept. "
                    "Use `source_doc` (from step 3 saved doc) and `source_chunk_idx` (from step 4) "
                    "for provenance. NEVER pass LLM-written content to expand — always use source_chunk_idx "
                    "so the backend extracts real text from the doc."
                ),
            },
            {
                "id": 7,
                "action": "research_gaps",
                "input_from": 5,
                "description": (
                    "For each TRUE GAP keyword from step 5c:\n"
                    "  1. `rank_urls` → find quality sources.\n"
                    "  2. `research_topic` → fetch and consolidate into docs/.\n"
                    "  3. `expand` with source_doc + source_chunk_idx — content extracted by backend.\n"
                    "  4. `link` to related concepts with typed edges.\n"
                    "  NEVER pass LLM-written content to expand. All concept descriptions must come "
                    "from actual doc chunks via source_chunk_idx."
                ),
            },
            {
                "id": 8,
                "tool": "sync_vaults",
                "args_template": {"skip_cognify": False},
                "description": "Cognify all new content and sync to Milvus. New concepts from gap research get proper Cognee edges.",
            },
        ],
    },
    "prompt_lifecycle": {
        "description": "Generate, audit, and refine a prompt using the Prompt Architect framework",
        "triggers": ["prompt", "generate prompt", "write prompt", "prompt engineer"],
        "requires": ["task_description"],
        "steps": [
            {
                "id": 1,
                "tool": "generate_prompt",
                "args_template": {"task_description": "{task_description}"},
                "description": "Generate a structured prompt using the Prompt Architect framework (6 mandatory sections)",
            },
            {
                "id": 2,
                "tool": "audit_prompt",
                "args_template": {"prompt_to_audit": "{step_1_output}"},
                "description": "Audit the generated prompt — scores each section as PRESENT/MISSING/WEAK, gives overall score 1-10",
            },
            {
                "id": 3,
                "action": "check_score",
                "input_from": 2,
                "gate": "score_below_7_triggers_refine",
                "description": "If audit score >= 7, the prompt is good — deliver it. If < 7, proceed to refine.",
            },
            {
                "id": 4,
                "tool": "refine_prompt",
                "args_template": {"original_prompt": "{step_1_output}", "feedback": "{step_2_audit_feedback}"},
                "description": "Refine the prompt based on audit feedback. Only runs if audit score < 7.",
                "conditional": True,
            },
        ],
    },
    "code_to_knowledge": {
        "description": "Review code against KB, then enrich the ontology with missing concepts",
        "triggers": ["enrich", "knowledge gap", "missing concept", "ontology", "sync knowledge"],
        "requires": ["file_path"],
        "steps": [
            {
                "id": 1,
                "tool": "improve_code",
                "args_template": {"file_path": "{file_path}"},
                "description": "Contrast code against Milvus — find what the KB says about each chunk",
            },
            {
                "id": 2,
                "action": "identify_gaps",
                "input_from": 1,
                "description": "Review improve_code output. Identify code chunks with few or no knowledge matches — these are concepts the KB doesn't know about yet.",
            },
            {
                "id": 3,
                "tool": "retrieve",
                "args_template": {"query": "{identified_concept}"},
                "description": "Search Milvus to confirm the concept is truly missing (not just low-scoring). If retrieve finds nothing relevant, proceed to expand.",
            },
            {
                "id": 4,
                "tool": "expand",
                "args_template": {"concept_name": "{concept_name}", "content": "{concept_content}"},
                "description": "Add the missing concept to the ontology. Include what the code does, why it exists, and how it relates to existing concepts.",
                "conditional": True,
            },
        ],
    },
    "full_improvement": {
        "description": "Full file improvement cycle: TDD guard → improve → verify → check for new knowledge",
        "triggers": ["full improve", "full cycle", "complete improvement", "deep improve"],
        "requires": ["file_path"],
        "steps": [
            {
                "id": 1,
                "tool": "tdd",
                "args_template": {"file_path": "{file_path}"},
                "description": "Phase 1 — Analyze code for test generation context",
            },
            {
                "id": 2,
                "action": "write_tests",
                "input_from": 1,
                "description": "Write pytest tests that lock current behavior",
            },
            {
                "id": 3,
                "action": "run_tests",
                "gate": "tests_pass",
                "command_template": "pytest {test_file} -v",
                "description": "Green baseline — all tests must pass",
            },
            {
                "id": 4,
                "tool": "improve_code",
                "args_template": {"file_path": "{file_path}"},
                "description": "Phase 2 — Get KB knowledge for each code chunk",
            },
            {
                "id": 5,
                "action": "apply_improvements",
                "input_from": 4,
                "description": "Apply improvements based on KB matches. Preserve contracts.",
            },
            {
                "id": 6,
                "action": "run_tests",
                "gate": "tests_pass",
                "command_template": "pytest {test_file} -v",
                "description": "Verify improvements didn't break behavior",
            },
            {
                "id": 7,
                "tool": "tdd",
                "args_template": {"file_path": "{file_path}"},
                "description": "Phase 3 — Re-analyze improved code. Compare with step 1: did new knowledge surface? Are there new testable behaviors?",
            },
            {
                "id": 8,
                "action": "compare_and_report",
                "input_from": [1, 7],
                "description": "Diff tdd outputs: step 1 vs step 7. Report new knowledge hits, changed scores, new testable units. This is the improvement delta.",
            },
            {
                "id": 9,
                "action": "create_issue",
                "input_from": [4, 6, 8],
                "description": "Create a GitHub issue with the full improvement report: changes applied, KB knowledge that motivated them, test results, and the before/after tdd delta.",
            },
        ],
    },
    "sync_and_audit": {
        "description": "Sync all vaults to Milvus, then audit code vs KG for drift",
        "triggers": ["sync", "vault", "audit", "drift", "check"],
        "requires": [],
        "steps": [
            {
                "id": 1,
                "tool": "sync_vaults",
                "args_template": {"skip_cognify": True},
                "description": "Sync LanceDB vectors → Milvus (skip cognify for speed). Use skip_cognify=False if vaults changed.",
            },
            {
                "id": 2,
                "tool": "audit_code",
                "args_template": {},
                "description": "Compare code AST against KG claims. Returns drift points and findings.",
            },
            {
                "id": 3,
                "action": "review_drift",
                "input_from": 2,
                "gate": "drift_zero_or_acceptable",
                "description": "If drift_points > 0, review findings. Decide whether to run self_improve or fix manually.",
            },
            {
                "id": 4,
                "tool": "self_improve",
                "args_template": {},
                "description": "Auto-fix drift: update tool counts, add missing concept relations, re-sync, log to Milvus.",
                "conditional": True,
            },
        ],
    },
    "densify": {
        "description": "Knowledge graph densification: extract keywords from docs, classify against Milvus, enrich matches, research gaps, sync",
        "triggers": ["densify", "densification", "keywords", "extract keywords", "knowledge gaps", "bridge", "connect docs"],
        "requires": ["doc_path"],
        "steps": [
            {
                "id": 1,
                "tool": "extract_keywords",
                "args_template": {"doc_path": "{doc_path}"},
                "description": "Extract keyword candidates from the doc — underlying concepts, technologies, abstractions.",
            },
            {
                "id": 2,
                "tool": "classify_keywords",
                "args_template": {"keywords_json": "{step_1_keywords}", "semantic_threshold": 0.45},
                "description": (
                    "Three-tier classification against Milvus:\n"
                    "  (a) EXACT → skip.\n"
                    "  (b) SEMANTIC (>= 0.45) → enrich matched concepts in step 3.\n"
                    "  (c) GAP (< 0.45) → research in step 4."
                ),
            },
            {
                "id": 3,
                "action": "enrich_semantic_matches",
                "input_from": [1, 2],
                "description": (
                    "For each SEMANTIC MATCH: `link` the keyword to the matched concept. "
                    "Use `source_doc` and `source_chunk_idx` from step 1 for provenance. "
                    "If the keyword is a generalist hub, `expand` it with source_doc + source_chunk_idx "
                    "so the content comes from the actual doc chunk, not LLM generation. "
                    "NEVER pass LLM-written content to expand — always use source_chunk_idx."
                ),
            },
            {
                "id": 4,
                "action": "research_gaps",
                "input_from": 2,
                "description": (
                    "For each TRUE GAP: research properly through Marvin's tools.\n"
                    "  1. `rank_urls` → find quality sources.\n"
                    "  2. `research_topic` → fetch and consolidate into a doc in docs/.\n"
                    "  3. `expand` with source_doc pointing to the new doc and source_chunk_idx "
                    "to extract real content. NEVER pass LLM-written content.\n"
                    "  4. `link` to related concepts with typed edges.\n"
                    "  5. Create generalist hub nodes (e.g., 'Database', 'Vector Search') "
                    "that connect all specific instances — always with source_doc provenance."
                ),
            },
            {
                "id": 5,
                "tool": "sync_vaults",
                "args_template": {"skip_cognify": False},
                "description": "Cognify new content → Neo4j + LanceDB → Milvus. Cognee creates typed cross-doc edges.",
            },
        ],
    },
}


def _match_chains(prompt: str) -> list[dict]:
    """Match a prompt against known chains by trigger keywords. Returns scored matches."""
    prompt_lower = prompt.lower()
    matches = []
    for chain_name, chain in CHAINS.items():
        score = sum(1 for t in chain["triggers"] if t in prompt_lower)
        if score > 0:
            matches.append({
                "chain": chain_name,
                "score": score,
                "description": chain["description"],
                "requires": chain["requires"],
            })
    matches.sort(key=lambda m: m["score"], reverse=True)
    return matches


def _extract_file_path(prompt: str) -> str | None:
    """Try to extract a file path from the prompt."""
    import re
    exts = r'\.(?:py|js|ts|go|rs|java|kt|yaml|yml|json|toml|md)'
    # Match absolute paths — greedy through spaces until file extension
    match = re.search(rf'(/(?:[^\s]|\s(?!/)).*?{exts})\b', prompt)
    if match:
        return match.group(1)
    # Match relative paths
    match = re.search(rf'(?:^|\s)([\w./-]+{exts})', prompt)
    if match:
        return match.group(1)
    return None


def orchestrate(prompt: str, k_per_collection: int = 3) -> dict:
    """Take a goal prompt and return a structured execution plan.

    1. Match prompt against known tool chains (keyword triggers)
    2. Embed prompt → search Milvus for additional context
    3. Extract parameters (file paths, URLs) from prompt
    4. Return the execution plan with steps, gates, and dependencies

    Returns:
      {
        "goal": str,
        "chain": str,
        "chain_description": str,
        "parameters": {"file_path": str, ...},
        "steps": [...],
        "milvus_context": [...],  # relevant knowledge for the executor
        "alternative_chains": [...],  # other chains that partially matched
      }
    """
    # 1. Match chains
    matches = _match_chains(prompt)
    if not matches:
        return {
            "error": "No matching tool chain found for this goal",
            "available_chains": [
                {"name": name, "description": chain["description"], "triggers": chain["triggers"]}
                for name, chain in CHAINS.items()
            ],
        }

    best = matches[0]
    chain = CHAINS[best["chain"]]

    # 2. Extract parameters from prompt
    params = {}
    file_path = _extract_file_path(prompt)
    if file_path:
        params["file_path"] = file_path

    # 3. Search Milvus for context relevant to the goal
    prompt_vec = _embed(prompt[:8000])
    milvus_context = []
    for col_name, fields in _RESSALVA_COLLECTIONS.items():
        hits = _search_by_vector(col_name, prompt_vec, k_per_collection, fields)
        for h in hits:
            if h["score"] < 0.35:
                continue
            milvus_context.append({
                "collection": col_name,
                "score": round(h["score"], 4),
                "summary": _format_ressalva(col_name, h),
            })

    # 4. Build the plan
    missing_params = [r for r in chain["requires"] if r not in params]

    return {
        "goal": prompt,
        "chain": best["chain"],
        "chain_description": chain["description"],
        "parameters": params,
        "missing_parameters": missing_params,
        "steps": chain["steps"],
        "milvus_context": milvus_context,
        "alternative_chains": [
            {"chain": m["chain"], "description": m["description"], "score": m["score"]}
            for m in matches[1:]
        ],
    }
