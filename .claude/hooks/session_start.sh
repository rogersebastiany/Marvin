#!/bin/bash
# Session start hook — inject Marvin enforcement status into context.
#
# Toggle: set MARVIN_HOOK_SESSION_START=0 in .env to disable

set -euo pipefail

ENV_FILE="$(dirname "$0")/../../.env"

if [ -f "$ENV_FILE" ]; then
    TOGGLE=$(grep -s "^MARVIN_HOOK_SESSION_START=" "$ENV_FILE" | cut -d= -f2 || echo "1")
    if [ "$TOGGLE" = "0" ]; then
        exit 0
    fi
fi

# Read current enforcement status
MILVUS_GATE="ENABLED"
ORCH_GATE="ENABLED"
PROVENANCE="ENABLED"

if [ -f "$ENV_FILE" ]; then
    [ "$(grep -s "^MARVIN_DISABLE_MILVUS_GATE=" "$ENV_FILE" | cut -d= -f2)" = "1" ] && MILVUS_GATE="DISABLED"
    [ "$(grep -s "^MARVIN_DISABLE_ORCHESTRATION_GATE=" "$ENV_FILE" | cut -d= -f2)" = "1" ] && ORCH_GATE="DISABLED"
    [ "$(grep -s "^MARVIN_DISABLE_PROVENANCE=" "$ENV_FILE" | cut -d= -f2)" = "1" ] && PROVENANCE="DISABLED"
fi

cat <<EOF
[Marvin Enforcement Status]
  Milvus Gate:        $MILVUS_GATE (retrieve before Neo4j access)
  Orchestration Gate: $ORCH_GATE (orchestrate before enrichment)
  Provenance:         $PROVENANCE (source_doc on expand in densify/research)

Remember: call orchestrate before any enrichment. Use source_doc + source_chunk_idx on expand.
EOF
