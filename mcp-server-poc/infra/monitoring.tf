# --- CloudWatch Log Groups ---

resource "aws_cloudwatch_log_group" "mcp" {
  for_each = var.mcp_servers

  name              = "/ecs/${local.name_prefix}/${each.key}"
  retention_in_days = 30

  tags = { Name = "${local.name_prefix}-${each.key}-logs" }
}

resource "aws_cloudwatch_log_group" "audit" {
  name              = "/mcp/${local.name_prefix}/audit"
  retention_in_days = 365

  tags = { Name = "${local.name_prefix}-audit-logs" }
}
