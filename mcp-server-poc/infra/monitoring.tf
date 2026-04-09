# --- CloudWatch Log Groups (container logs only) ---
# Audit logging is handled by Milvus episodic memory (log_tool_call, log_decision, log_session).
# CloudWatch is only for Fargate container stdout/stderr (ops, not compliance).

resource "aws_cloudwatch_log_group" "mcp" {
  for_each = var.mcp_servers

  name              = "/ecs/${local.name_prefix}/${each.key}"
  retention_in_days = 30

  tags = { Name = "${local.name_prefix}-${each.key}-logs" }
}
