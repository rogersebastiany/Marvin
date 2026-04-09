terraform {
  required_version = ">= 1.5"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region                      = var.aws_region
  access_key                  = "test"
  secret_key                  = "test"
  skip_credentials_validation = true
  skip_metadata_api_check     = true
  skip_requesting_account_id  = true

  endpoints {
    s3             = var.localstack_endpoint
    kms            = var.localstack_endpoint
    secretsmanager = var.localstack_endpoint
    cloudwatchlogs = var.localstack_endpoint
    ecr            = var.localstack_endpoint
    ecs            = var.localstack_endpoint
    elbv2          = var.localstack_endpoint
    ec2            = var.localstack_endpoint
    iam            = var.localstack_endpoint
    sts            = var.localstack_endpoint
    wafv2          = var.localstack_endpoint
    cognitoidp     = var.localstack_endpoint
  }
}
