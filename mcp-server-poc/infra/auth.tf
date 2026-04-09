# --- Cognito User Pool ---

resource "aws_cognito_user_pool" "main" {
  name = "${local.name_prefix}-users"

  username_attributes      = ["email"]
  auto_verified_attributes = ["email"]

  password_policy {
    minimum_length    = 12
    require_lowercase = true
    require_uppercase = true
    require_numbers   = true
    require_symbols   = true
  }

  mfa_configuration = "OPTIONAL"

  software_token_mfa_configuration {
    enabled = true
  }

  account_recovery_setting {
    recovery_mechanism {
      name     = "verified_email"
      priority = 1
    }
  }

  schema {
    name                = "email"
    attribute_data_type = "String"
    required            = true
    mutable             = true

    string_attribute_constraints {
      min_length = 1
      max_length = 256
    }
  }

  schema {
    name                = "tenant_id"
    attribute_data_type = "String"
    required            = false
    mutable             = true

    string_attribute_constraints {
      min_length = 1
      max_length = 64
    }
  }

  tags = { Name = "${local.name_prefix}-user-pool" }
}

# --- Cognito User Pool Domain (for hosted UI / token endpoint) ---

resource "aws_cognito_user_pool_domain" "main" {
  domain       = local.name_prefix
  user_pool_id = aws_cognito_user_pool.main.id
}

# --- Cognito App Client (for ALB integration) ---

resource "aws_cognito_user_pool_client" "alb" {
  name         = "${local.name_prefix}-alb-client"
  user_pool_id = aws_cognito_user_pool.main.id

  generate_secret                      = true
  allowed_oauth_flows_user_pool_client = true
  allowed_oauth_flows                  = ["code"]
  allowed_oauth_scopes                 = ["openid", "email", "profile"]
  supported_identity_providers         = ["COGNITO"]

  callback_urls = [
    "http://localhost/oauth2/idpresponse",
    "https://${local.name_prefix}.example.com/oauth2/idpresponse",
  ]

  logout_urls = [
    "http://localhost/",
  ]

  explicit_auth_flows = [
    "ALLOW_USER_SRP_AUTH",
    "ALLOW_REFRESH_TOKEN_AUTH",
  ]
}

# --- Cognito Resource Server (API scopes for MCP) ---

resource "aws_cognito_resource_server" "mcp_api" {
  identifier   = "mcp-api"
  name         = "MCP Server API"
  user_pool_id = aws_cognito_user_pool.main.id

  scope {
    scope_name        = "read"
    scope_description = "Read access to docs and diagrams"
  }

  scope {
    scope_name        = "write"
    scope_description = "Write access (save docs, generate diagrams)"
  }

  scope {
    scope_name        = "admin"
    scope_description = "Admin access (crawl, audit)"
  }
}

# --- Cognito User Groups (RBAC) ---

resource "aws_cognito_user_group" "developers" {
  name         = "developers"
  user_pool_id = aws_cognito_user_pool.main.id
  description  = "Developers - read/write access to MCP servers"
}

resource "aws_cognito_user_group" "admins" {
  name         = "admins"
  user_pool_id = aws_cognito_user_pool.main.id
  description  = "Admins - full access including crawl and audit"
}
