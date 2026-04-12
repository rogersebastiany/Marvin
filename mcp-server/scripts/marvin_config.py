#!/usr/bin/env python3
"""
Marvin configuration toggle — manage middleware, provenance, and gate settings.

Reads/writes environment variables in the project .env file.
All toggles default to ENABLED (secure by default). Set to "1" to disable.

Usage:
    uv run python scripts/marvin_config.py              # show current config
    uv run python scripts/marvin_config.py --toggle <key>  # toggle a setting
    uv run python scripts/marvin_config.py --enable-all    # re-enable all gates
    uv run python scripts/marvin_config.py --disable-all   # disable all gates (dev mode)
"""

import argparse
import sys
from pathlib import Path

ENV_FILE = Path(__file__).parent.parent.parent / ".env"

# All configurable toggles — env var → description
TOGGLES = {
    "MARVIN_DISABLE_MILVUS_GATE": {
        "description": "Milvus Gate middleware — blocks Neo4j access without prior Milvus retrieval",
        "layer": "Middleware",
        "default": "0",  # enabled
    },
    "MARVIN_DISABLE_ORCHESTRATION_GATE": {
        "description": "Orchestration Gate middleware — blocks enrichment tools without orchestrate plan",
        "layer": "Middleware",
        "default": "0",  # enabled
    },
    "MARVIN_DISABLE_PROVENANCE": {
        "description": "Provenance enforcement — expand requires source_doc in densify/research chains",
        "layer": "Provenance",
        "default": "0",  # enabled
    },
    # Claude Code hooks — "1" means enabled (runs), "0" means disabled (skipped)
    # Note: hooks use opposite convention — "1" = ON, "0" = OFF
    "MARVIN_HOOK_PRE_MCP_TOOL": {
        "description": "Pre-tool hook — audit log + orchestration validation on MCP calls",
        "layer": "Hook",
        "default": "1",  # enabled
    },
    "MARVIN_HOOK_POST_MCP_TOOL": {
        "description": "Post-tool hook — result logging + provenance warnings on expand",
        "layer": "Hook",
        "default": "1",  # enabled
    },
    "MARVIN_HOOK_SESSION_START": {
        "description": "Session start hook — injects enforcement status into Claude context",
        "layer": "Hook",
        "default": "1",  # enabled
    },
}


def read_env() -> dict[str, str]:
    """Read .env file into a dict."""
    env = {}
    if ENV_FILE.exists():
        for line in ENV_FILE.read_text().splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                key, _, value = line.partition("=")
                env[key.strip()] = value.strip()
    return env


def write_env(env: dict[str, str]):
    """Write dict back to .env, preserving comments and blank lines."""
    lines = []
    if ENV_FILE.exists():
        existing_keys = set()
        for line in ENV_FILE.read_text().splitlines():
            stripped = line.strip()
            if stripped and not stripped.startswith("#") and "=" in stripped:
                key = stripped.split("=", 1)[0].strip()
                existing_keys.add(key)
                if key in env:
                    lines.append(f"{key}={env[key]}")
                else:
                    lines.append(line)
            else:
                lines.append(line)
        # Add new keys that weren't in the file
        for key, value in env.items():
            if key not in existing_keys:
                lines.append(f"{key}={value}")
    else:
        for key, value in env.items():
            lines.append(f"{key}={value}")

    ENV_FILE.write_text("\n".join(lines) + "\n")


def get_status(env: dict, key: str) -> tuple[str, str]:
    """Get current value and human-readable status.

    Middleware/Provenance: "1" = DISABLED, "0" = ENABLED (secure default)
    Hooks: "1" = ENABLED, "0" = DISABLED (hooks check for "0" to skip)
    """
    info = TOGGLES[key]
    value = env.get(key, info["default"])
    if info["layer"] == "Hook":
        # Hooks: "1" = ON, "0" = OFF
        return value, "ENABLED" if value != "0" else "DISABLED"
    else:
        # Middleware/Provenance: "1" = OFF, "0" = ON
        return value, "DISABLED" if value == "1" else "ENABLED"


def show_config():
    """Display current configuration."""
    env = read_env()

    print("=" * 70)
    print("  MARVIN ENFORCEMENT CONFIGURATION")
    print("  Set to '1' to disable, '0' (or absent) to enable")
    print("=" * 70)
    print()

    by_layer = {}
    for key, info in TOGGLES.items():
        by_layer.setdefault(info["layer"], []).append((key, info))

    for layer, items in by_layer.items():
        print(f"  [{layer}]")
        for key, info in items:
            value, status = get_status(env, key)
            marker = "ON" if status == "ENABLED" else "OFF"
            color = "\033[32m" if status == "ENABLED" else "\033[31m"
            reset = "\033[0m"
            print(f"    {color}[{marker}]{reset} {key}")
            print(f"         {info['description']}")
        print()

    print("-" * 70)
    print("  Toggle:      uv run python scripts/marvin_config.py --toggle <KEY>")
    print("  Enable all:  uv run python scripts/marvin_config.py --enable-all")
    print("  Disable all: uv run python scripts/marvin_config.py --disable-all")
    print("=" * 70)


def toggle_key(key: str):
    """Toggle a single setting."""
    if key not in TOGGLES:
        print(f"Unknown key: {key}")
        print(f"Available: {', '.join(TOGGLES.keys())}")
        sys.exit(1)

    env = read_env()
    info = TOGGLES[key]
    current = env.get(key, info["default"])
    new_value = "0" if current == "1" else "1"
    env[key] = new_value
    write_env(env)

    _, status = get_status(env, key)
    print(f"{key} → {status}")
    print(f"  {info['description']}")
    print()
    if info["layer"] == "Hook":
        print("Takes effect on next Claude Code session.")
    else:
        print("Restart Marvin server to apply.")


def set_all(value: str):
    """Set all toggles to enabled or disabled.

    Args:
        value: "enable" or "disable"
    """
    env = read_env()
    for key, info in TOGGLES.items():
        if value == "enable":
            # Middleware: "0" = enabled. Hooks: "1" = enabled.
            env[key] = "0" if info["layer"] != "Hook" else "1"
        else:
            # Middleware: "1" = disabled. Hooks: "0" = disabled.
            env[key] = "1" if info["layer"] != "Hook" else "0"
    write_env(env)

    label = "ENABLED" if value == "enable" else "DISABLED"
    print(f"All enforcement layers → {label}")
    for key, info in TOGGLES.items():
        _, status = get_status(env, key)
        marker = "ON" if status == "ENABLED" else "OFF"
        print(f"  [{marker}] {key} — {info['description']}")
    print()
    print("Restart Marvin server + start new Claude Code session to apply.")


def main():
    parser = argparse.ArgumentParser(description="Marvin enforcement configuration")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--toggle", metavar="KEY", help="Toggle a specific setting")
    group.add_argument("--enable-all", action="store_true", help="Enable all enforcement layers")
    group.add_argument("--disable-all", action="store_true", help="Disable all enforcement layers (dev mode)")
    args = parser.parse_args()

    if args.toggle:
        toggle_key(args.toggle)
    elif args.enable_all:
        set_all("enable")
    elif args.disable_all:
        set_all("disable")
    else:
        show_config()


if __name__ == "__main__":
    main()
