variable "localstack_endpoint" {
  description = "LocalStack endpoint URL"
  type        = string
  default     = "http://localhost:4566"
}

variable "cognito_callback_urls" {
  description = "OAuth2 callback URLs for Cognito"
  type        = list(string)
  default     = ["http://localhost/oauth2/idpresponse"]
}

variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "project" {
  description = "Project name used for resource naming"
  type        = string
  default     = "mcp-server"
}

variable "environment" {
  description = "Environment name"
  type        = string
  default     = "local"
}

variable "mcp_servers" {
  description = "Map of MCP server names to their config"
  type = map(object({
    cpu    = number
    memory = number
    port   = number
  }))
  default = {
    docs-server = {
      cpu    = 256
      memory = 512
      port   = 8001
    }
    web-to-docs = {
      cpu    = 256
      memory = 512
      port   = 8002
    }
    prompt-engineer = {
      cpu    = 256
      memory = 512
      port   = 8003
    }
    system-design = {
      cpu    = 256
      memory = 512
      port   = 8004
    }
  }
}

locals {
  name_prefix = "${var.project}-${var.environment}"
}
