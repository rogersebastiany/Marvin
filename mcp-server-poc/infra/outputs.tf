output "alb_dns" {
  description = "ALB DNS name"
  value       = aws_lb.main.dns_name
}

output "s3_bucket" {
  description = "S3 bucket for docs and diagrams"
  value       = aws_s3_bucket.docs.id
}

output "ecr_repository_url" {
  description = "ECR repository URL for MCP server image"
  value       = aws_ecr_repository.mcp.repository_url
}

output "ecs_cluster" {
  description = "ECS cluster name"
  value       = aws_ecs_cluster.main.name
}

output "kms_key_id" {
  description = "KMS key ID for docs encryption"
  value       = aws_kms_key.docs.key_id
}

output "secret_arn" {
  description = "Secrets Manager ARN"
  value       = aws_secretsmanager_secret.mcp_config.arn
}

output "log_groups" {
  description = "CloudWatch log group names"
  value       = { for k, v in aws_cloudwatch_log_group.mcp : k => v.name }
}

output "vpc_id" {
  description = "VPC ID"
  value       = aws_vpc.main.id
}

output "cognito_user_pool_id" {
  description = "Cognito User Pool ID"
  value       = aws_cognito_user_pool.main.id
}

output "cognito_client_id" {
  description = "Cognito App Client ID (for auth flows)"
  value       = aws_cognito_user_pool_client.alb.id
}

output "cognito_domain" {
  description = "Cognito hosted UI domain"
  value       = aws_cognito_user_pool_domain.main.domain
}
