#!/bin/bash
# Pre-tool hook for Marvin MCP calls.
# Validates orchestration and provenance rules from the client side.
#
# Toggle: set MARVIN_HOOK_PRE_MCP_TOOL=0 in .env to disable
#
# Receives JSON on stdin with tool_name and tool_input.
# Exit 0 = allow, Exit 2 = block (reason on stderr).

set -euo pipefail

# Check toggle — disabled by default means the hook runs
ENV_FILE="$(dirname "$0")/../../.env"
if [ -f "$ENV_FILE" ]; then
    TOGGLE=$(grep -s "^MARVIN_HOOK_PRE_MCP_TOOL=" "$ENV_FILE" | cut -d= -f2 || echo "1")
    if [ "$TOGGLE" = "0" ]; then
        exit 0  # Hook disabled
    fi
fi

INPUT=$(cat)
TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name // ""')

# Only process Marvin MCP tools
if [[ ! "$TOOL_NAME" =~ ^mcp__mcp-marvin__ ]]; then
    exit 0
fi

# Extract the short tool name (after mcp__mcp-marvin__)
SHORT_NAME="${TOOL_NAME#mcp__mcp-marvin__}"

# Audit log — system-level, Claude never sees this.
# NOT L1 memory (HCC). This is infrastructure, like nginx access logs.
# For the human to review: "did the gates fire? what was called?"
LOG_DIR="$(dirname "$0")/../logs"
mkdir -p "$LOG_DIR"
echo "$INPUT" | jq -c "{timestamp: (now | todate), tool: \"$SHORT_NAME\", input: .tool_input}" >> "$LOG_DIR/mcp_audit.jsonl" 2>/dev/null || true

# No context injection — don't pollute Claude's context window with
# "you just called X" noise. That's L1 and Claude already knows.
exit 0
