#!/usr/bin/env python3
"""
Generate tool documentation from marvin_server.py source of truth.

Reads MARVIN_TOOLS, tier classifications, docstrings, and backend modules,
then updates README.md, CLAUDE.md, and mcp-server/CLAUDE.md between markers.

Usage:
    cd mcp-server && uv run python generate_docs.py          # preview
    cd mcp-server && uv run python generate_docs.py --write  # update files
"""

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
import marvin_server

ROOT = Path(__file__).parent.parent.parent
MCP = Path(__file__).parent.parent

# ── Extract tool metadata ────────────────────────────────────────────────


def _get_tool_table() -> str:
    """Generate markdown table of all tools with descriptions and tiers."""
    tiers = {
        "Milvus (sets gate)": marvin_server.MILVUS_TOOLS,
        "Overview (ungated)": marvin_server.OVERVIEW_TOOLS,
        "Neo4j Read (gated)": marvin_server.NEO4J_READ_TOOLS,
        "Write (gated)": marvin_server.WRITE_TOOLS,
    }

    classified = set()
    for tools in tiers.values():
        classified |= tools

    always_allowed = set(marvin_server.MARVIN_TOOLS) - classified

    def _tier_of(name: str) -> str:
        for tier_name, tools in tiers.items():
            if name in tools:
                return tier_name
        return "Always Allowed"

    def _doc_of(name: str) -> str:
        func = getattr(marvin_server, name, None)
        if func and callable(func):
            raw = (func.__doc__ or "").strip()
            return raw.split("\n")[0].strip() if raw else "—"
        return "—"

    lines = [
        f"| Tool | Tier | Description |",
        f"|------|------|-------------|",
    ]
    for name in marvin_server.MARVIN_TOOLS:
        lines.append(f"| `{name}` | {_tier_of(name)} | {_doc_of(name)} |")

    return "\n".join(lines)


def _get_tier_summary() -> str:
    """Generate tier summary table."""
    lines = [
        "| Tier | Count | Tools |",
        "|------|-------|-------|",
    ]

    tier_data = [
        ("Milvus (sets gate)", marvin_server.MILVUS_TOOLS),
        ("Overview (ungated)", marvin_server.OVERVIEW_TOOLS),
        ("Neo4j Read (gated)", marvin_server.NEO4J_READ_TOOLS),
        ("Write (gated)", marvin_server.WRITE_TOOLS),
    ]

    classified = set()
    for _, tools in tier_data:
        classified |= tools
    always = set(marvin_server.MARVIN_TOOLS) - classified

    for tier_name, tools in tier_data:
        tool_list = ", ".join(f"`{t}`" for t in sorted(tools))
        lines.append(f"| **{tier_name}** | {len(tools)} | {tool_list} |")

    tool_list = ", ".join(f"`{t}`" for t in sorted(always))
    lines.append(f"| **Always Allowed** | {len(always)} | {tool_list} |")

    return "\n".join(lines)


def _get_backend_table(backends: list[tuple[str, str]]) -> str:
    """Generate backend module table."""
    lines = [
        "| Module | Description |",
        "|--------|-------------|",
    ]
    for name, doc in backends:
        lines.append(f"| `{name}.py` | {doc} |")

    return "\n".join(lines)


def _get_chain_table() -> str:
    """Generate orchestrator chain table."""
    from backends.orchestrator_backend import CHAINS

    lines = [
        "| Chain | Triggers | Steps | Description |",
        "|-------|----------|-------|-------------|",
    ]
    for name, chain in CHAINS.items():
        triggers = ", ".join(chain["triggers"][:3])
        lines.append(
            f"| `{name}` | {triggers} | {len(chain['steps'])} | {chain['description']} |"
        )

    return "\n".join(lines)


# ── Assemble full docs block ─────────────────────────────────────────────


def _get_backends() -> list[tuple[str, str]]:
    """Discover backend modules from imports in marvin_server.py."""
    import ast
    import importlib

    source = (MCP / "marvin_server.py").read_text()
    tree = ast.parse(source)

    backends = []
    for node in ast.iter_child_nodes(tree):
        if isinstance(node, ast.ImportFrom) and node.module == "backends":
            for alias in node.names:
                mod_path = MCP / "backends" / f"{alias.name}.py"
                if mod_path.exists():
                    mod = importlib.import_module(f"backends.{alias.name}")
                    doc = (mod.__doc__ or "").strip().split("\n")[0]
                    backends.append((alias.name, doc))
    return backends


def generate_block() -> str:
    """Generate the full auto-generated docs block."""
    total = len(marvin_server.MARVIN_TOOLS)
    backends = _get_backends()

    return f"""## Marvin's Tools ({total} total)

{_get_tool_table()}

### Tier Summary

{_get_tier_summary()}

### Backends ({len(backends)} modules)

{_get_backend_table(backends)}

### Orchestrator Chains

{_get_chain_table()}

### Milvus Gate Middleware

All Neo4j reads and write tools are **blocked** unless a Milvus tier tool was called first in the session. Architectural enforcement (P=0), not prompt bias."""


# ── File updater ─────────────────────────────────────────────────────────

START_MARKER = "<!-- AUTO:TOOLS:START -->"
END_MARKER = "<!-- AUTO:TOOLS:END -->"


def update_file(path: Path, block: str, dry_run: bool = True) -> bool:
    """Replace content between markers in a file. Returns True if changed."""
    if not path.exists():
        print(f"  SKIP {path} (not found)")
        return False

    content = path.read_text()

    if START_MARKER not in content:
        print(f"  SKIP {path} (no {START_MARKER} marker)")
        return False

    pattern = re.compile(
        re.escape(START_MARKER) + r".*?" + re.escape(END_MARKER),
        re.DOTALL,
    )

    replacement = f"{START_MARKER}\n{block}\n{END_MARKER}"
    new_content = pattern.sub(replacement, content)

    if new_content == content:
        print(f"  OK   {path} (no changes)")
        return False

    if dry_run:
        print(f"  WOULD UPDATE {path}")
    else:
        path.write_text(new_content)
        print(f"  UPDATED {path}")

    return True


def main():
    parser = argparse.ArgumentParser(description="Generate tool docs from marvin_server.py")
    parser.add_argument("--write", action="store_true", help="Actually write to files (default: preview)")
    args = parser.parse_args()

    block = generate_block()

    if not args.write:
        print("=== Preview (run with --write to update files) ===\n")
        print(block)
        print("\n=== Files to update ===")

    targets = [
        ROOT / "README.md",
        ROOT / "CLAUDE.md",
        MCP / "CLAUDE.md",
    ]

    for path in targets:
        update_file(path, block, dry_run=not args.write)


if __name__ == "__main__":
    main()
