# --- ECR Repository ---

resource "aws_ecr_repository" "mcp" {
  name                 = "${local.name_prefix}"
  image_tag_mutability = "MUTABLE"
  force_delete         = true

  image_scanning_configuration {
    scan_on_push = true
  }

  tags = { Name = "${local.name_prefix}-ecr" }
}

# --- ECS Cluster ---

resource "aws_ecs_cluster" "main" {
  name = "${local.name_prefix}-cluster"

  setting {
    name  = "containerInsights"
    value = "enabled"
  }

  tags = { Name = "${local.name_prefix}-cluster" }
}

# --- IAM Roles ---

data "aws_iam_policy_document" "ecs_assume" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["ecs-tasks.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "ecs_execution" {
  name               = "${local.name_prefix}-ecs-execution"
  assume_role_policy = data.aws_iam_policy_document.ecs_assume.json
}

resource "aws_iam_role_policy_attachment" "ecs_execution" {
  role       = aws_iam_role.ecs_execution.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

resource "aws_iam_role" "ecs_task" {
  name               = "${local.name_prefix}-ecs-task"
  assume_role_policy = data.aws_iam_policy_document.ecs_assume.json
}

data "aws_iam_policy_document" "ecs_task" {
  statement {
    sid = "S3Access"
    actions = [
      "s3:GetObject",
      "s3:PutObject",
      "s3:ListBucket",
      "s3:DeleteObject",
    ]
    resources = [
      aws_s3_bucket.docs.arn,
      "${aws_s3_bucket.docs.arn}/*",
    ]
  }

  statement {
    sid = "KMSAccess"
    actions = [
      "kms:Decrypt",
      "kms:Encrypt",
      "kms:GenerateDataKey",
    ]
    resources = [aws_kms_key.docs.arn]
  }

  statement {
    sid = "SecretsAccess"
    actions = [
      "secretsmanager:GetSecretValue",
    ]
    resources = [aws_secretsmanager_secret.mcp_config.arn]
  }

  statement {
    sid = "CloudWatchLogs"
    actions = [
      "logs:CreateLogStream",
      "logs:PutLogEvents",
    ]
    resources = ["*"]
  }
}

resource "aws_iam_role_policy" "ecs_task" {
  name   = "${local.name_prefix}-ecs-task-policy"
  role   = aws_iam_role.ecs_task.id
  policy = data.aws_iam_policy_document.ecs_task.json
}

# --- ECS Task Definitions ---

locals {
  server_entrypoints = {
    "docs-server"      = "server.py"
    "web-to-docs"      = "web_to_docs_server.py"
    "prompt-engineer"   = "prompt_engineer_server.py"
    "system-design"     = "system_design_server.py"
  }
}

resource "aws_ecs_task_definition" "mcp" {
  for_each = var.mcp_servers

  family                   = "${local.name_prefix}-${each.key}"
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = each.value.cpu
  memory                   = each.value.memory
  execution_role_arn       = aws_iam_role.ecs_execution.arn
  task_role_arn            = aws_iam_role.ecs_task.arn

  container_definitions = jsonencode([
    {
      name      = each.key
      image     = "${aws_ecr_repository.mcp.repository_url}:latest"
      essential = true

      environment = [
        { name = "MCP_SERVER", value = local.server_entrypoints[each.key] },
        { name = "AWS_DEFAULT_REGION", value = var.aws_region },
        { name = "S3_BUCKET", value = aws_s3_bucket.docs.id },
        { name = "SECRET_ARN", value = aws_secretsmanager_secret.mcp_config.arn },
      ]

      portMappings = [
        {
          containerPort = each.value.port
          protocol      = "tcp"
        }
      ]

      logConfiguration = {
        logDriver = "awslogs"
        options = {
          "awslogs-group"         = aws_cloudwatch_log_group.mcp[each.key].name
          "awslogs-region"        = var.aws_region
          "awslogs-stream-prefix" = each.key
        }
      }
    }
  ])

  tags = { Name = "${local.name_prefix}-${each.key}" }
}

# --- ECS Services ---

resource "aws_ecs_service" "mcp" {
  for_each = var.mcp_servers

  name            = each.key
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.mcp[each.key].arn
  desired_count   = 1
  launch_type     = "FARGATE"

  network_configuration {
    subnets          = aws_subnet.private[*].id
    security_groups  = [aws_security_group.ecs.id]
    assign_public_ip = false
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.mcp[each.key].arn
    container_name   = each.key
    container_port   = each.value.port
  }

  tags = { Name = "${local.name_prefix}-${each.key}" }
}
