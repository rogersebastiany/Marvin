#!/usr/bin/env python3
"""
marvin-ops — Local CLI for Marvin operations.

Thin wrapper around ops_backend.py — same logic used by MCP tools.

Subcommands:
    sync      Cognify vaults → Neo4j + LanceDB → Milvus
    audit     Self-audit: compare code AST against knowledge graph
    improve   Deterministic self-improvement: audit → fix drift → log
    all       Run sync → audit → improve sequentially

Usage:
    uv run python marvin_ops.py sync --skip-cognify
    uv run python marvin_ops.py audit
    uv run python marvin_ops.py improve
    uv run python marvin_ops.py all

Exit codes:
    0  Clean (no drift, or all fixed)
    1  Drift found (audit) or errors
"""

import argparse
import json
import sys
from pathlib import Path

from dotenv import load_dotenv

# ── Paths ───────────────────────────────────────────────────────────────────

ROOT = Path(__file__).parent
load_dotenv(ROOT / ".env")

sys.path.insert(0, str(ROOT / "mcp-server"))
sys.path.insert(0, str(ROOT / "load-vaults"))

import ops_backend


# ── CLI ─────────────────────────────────────────────────────────────────────


def _print_result(label: str, result: dict, fmt: str):
    if fmt == "json":
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"\n[{label}]")
        for k, v in result.items():
            if isinstance(v, list):
                print(f"  {k}:")
                for item in v:
                    print(f"    - {item}")
            else:
                print(f"  {k}: {v}")


def cmd_sync(args) -> bool:
    result = ops_backend.sync(
        skip_cognify=args.skip_cognify,
        changed_files=args.changed_files,
    )
    _print_result("sync", result, args.format)
    return True


def cmd_audit(args) -> bool:
    result = ops_backend.audit()
    _print_result("audit", result, args.format)
    return result["drift_points"] <= args.threshold


def cmd_improve(args) -> bool:
    result = ops_backend.self_improve()
    _print_result("improve", result, args.format)
    return True


def cmd_all(args) -> bool:
    sync_result = ops_backend.sync(skip_cognify=args.skip_cognify)
    _print_result("sync", sync_result, args.format)

    audit_result = ops_backend.audit()
    _print_result("audit", audit_result, args.format)

    if audit_result["drift_points"] > args.threshold:
        improve_result = ops_backend.self_improve()
        _print_result("improve", improve_result, args.format)

    return True


def main():
    parser = argparse.ArgumentParser(
        prog="marvin-ops",
        description="Local CLI for Marvin operations (wraps ops_backend.py)",
    )

    shared = argparse.ArgumentParser(add_help=False)
    shared.add_argument("--format", choices=["text", "json"], default="text")
    shared.add_argument("--threshold", type=int, default=0)
    shared.add_argument("--skip-cognify", action="store_true")
    shared.add_argument("--changed-files", nargs="*", default=None)

    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("sync", parents=[shared], help="Cognify + LanceDB → Milvus")
    sub.add_parser("audit", parents=[shared], help="Code AST vs KG drift")
    sub.add_parser("improve", parents=[shared], help="Auto-fix drift + log")
    sub.add_parser("all", parents=[shared], help="sync → audit → improve")

    args = parser.parse_args()

    try:
        ok = {"sync": cmd_sync, "audit": cmd_audit, "improve": cmd_improve, "all": cmd_all}[args.command](args)
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        ok = False

    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
