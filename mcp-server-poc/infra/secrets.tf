# --- Secrets Manager ---

resource "aws_secretsmanager_secret" "mcp_config" {
  name                    = "${local.name_prefix}/config"
  description             = "MCP server configuration and API keys"
  recovery_window_in_days = 0 # Immediate delete for local dev

  tags = { Name = "${local.name_prefix}-config" }
}

resource "aws_secretsmanager_secret_version" "mcp_config" {
  secret_id = aws_secretsmanager_secret.mcp_config.id
  secret_string = jsonencode({
    s3_bucket  = aws_s3_bucket.docs.id
    kms_key_id = aws_kms_key.docs.key_id
    # Add real API keys here for production
    api_key = "local-dev-key"
  })
}
