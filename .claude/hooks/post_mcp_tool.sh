#!/bin/bash
# Post-tool hook for Marvin MCP calls.
# Logs results and validates provenance on expand output.
#
# Toggle: set MARVIN_HOOK_POST_MCP_TOOL=0 in .env to disable

set -euo pipefail

ENV_FILE="$(dirname "$0")/../../.env"
if [ -f "$ENV_FILE" ]; then
    TOGGLE=$(grep -s "^MARVIN_HOOK_POST_MCP_TOOL=" "$ENV_FILE" | cut -d= -f2 || echo "1")
    if [ "$TOGGLE" = "0" ]; then
        exit 0
    fi
fi

INPUT=$(cat)
TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name // ""')

if [[ ! "$TOOL_NAME" =~ ^mcp__mcp-marvin__ ]]; then
    exit 0
fi

SHORT_NAME="${TOOL_NAME#mcp__mcp-marvin__}"

# Audit log — system-level only, not injected into Claude's context.
LOG_DIR="$(dirname "$0")/../logs"
mkdir -p "$LOG_DIR"
RESULT_PREVIEW=$(echo "$INPUT" | jq -r '.tool_output // "" | tostring | .[0:200]' 2>/dev/null || echo "")
echo "{\"timestamp\": \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\", \"tool\": \"$SHORT_NAME\", \"result_preview\": \"$RESULT_PREVIEW\"}" >> "$LOG_DIR/mcp_audit.jsonl" 2>/dev/null || true

# Provenance enforcement — this IS worth injecting into context.
# Not L1 noise: it's corrective feedback, like a failing test.
# Tells Claude "your approach was wrong, fix it."
if [ "$SHORT_NAME" = "expand" ]; then
    OUTPUT=$(echo "$INPUT" | jq -r '.tool_output // ""')
    if echo "$OUTPUT" | grep -q "^BLOCKED:"; then
        echo "{\"hookSpecificOutput\": {\"hookEventName\": \"PostToolUse\", \"additionalContext\": \"[PROVENANCE] expand was blocked. You MUST provide source_doc and source_chunk_idx.\"}}"
        exit 0
    fi
fi

exit 0
