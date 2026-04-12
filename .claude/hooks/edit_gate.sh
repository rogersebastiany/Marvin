#!/bin/bash
# Edit/Write orchestration gate — P=0 enforcement on core source files.
#
# Thesis: "A prompt is a Bias — it shifts probability, it does not eliminate it."
#         "If the tool does not exist, the action is impossible by construction."
#
# This hook makes it IMPOSSIBLE to edit core Marvin files without first
# calling orchestrate. Not "please don't" — "cannot."
#
# Toggle: set MARVIN_HOOK_EDIT_GATE=0 in .env to disable
#
# Protected paths (core files):
#   mcp-server/backends/*.py
#   mcp-server/marvin_server.py
#
# Unprotected (always editable):
#   tests/, scripts/, docs/, diagrams/, .claude/, vaults/,
#   CLAUDE.md, README.md, .env, load-vaults/

set -euo pipefail

ENV_FILE="$(dirname "$0")/../../.env"
if [ -f "$ENV_FILE" ]; then
    TOGGLE=$(grep -s "^MARVIN_HOOK_EDIT_GATE=" "$ENV_FILE" | cut -d= -f2 || echo "1")
    if [ "$TOGGLE" = "0" ]; then
        exit 0  # Hook disabled
    fi
fi

INPUT=$(cat)
TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name // ""')

# Only gate Edit and Write tools
if [ "$TOOL_NAME" != "Edit" ] && [ "$TOOL_NAME" != "Write" ]; then
    exit 0
fi

# Extract the file path being edited
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // ""')

if [ -z "$FILE_PATH" ]; then
    exit 0  # No file path, let it through
fi

# Check if this is a protected core file
PROTECTED=false

# mcp-server/backends/*.py
if echo "$FILE_PATH" | grep -qE 'mcp-server/backends/[^/]+\.py$'; then
    PROTECTED=true
fi

# mcp-server/marvin_server.py
if echo "$FILE_PATH" | grep -qE 'mcp-server/marvin_server\.py$'; then
    PROTECTED=true
fi

# If not a protected file, allow
if [ "$PROTECTED" = "false" ]; then
    exit 0
fi

# Protected file — check if orchestrate was called this session
STATE_FILE="$(dirname "$0")/../state/orchestrated_session"

if [ -f "$STATE_FILE" ]; then
    # Orchestration plan exists — allow the edit
    exit 0
fi

# No orchestration plan — BLOCK (P=0)
echo "BLOCKED: Editing core file '$(basename "$FILE_PATH")' requires an orchestration plan." >&2
echo "Call 'orchestrate' first to establish a chain, then retry." >&2
echo "This is architectural enforcement (P=0), not a suggestion." >&2
echo "To disable: uv run python scripts/marvin_config.py --toggle MARVIN_HOOK_EDIT_GATE" >&2
exit 2
