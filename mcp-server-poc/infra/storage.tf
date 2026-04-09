# --- KMS Key (encryption at rest) ---

resource "aws_kms_key" "docs" {
  description             = "Encryption key for MCP docs and diagrams"
  deletion_window_in_days = 7
  enable_key_rotation     = true

  tags = { Name = "${local.name_prefix}-docs-key" }
}

resource "aws_kms_alias" "docs" {
  name          = "alias/${local.name_prefix}-docs"
  target_key_id = aws_kms_key.docs.key_id
}

# --- S3 Bucket (docs + diagrams storage) ---

resource "aws_s3_bucket" "docs" {
  bucket        = "${local.name_prefix}-docs"
  force_destroy = true

  tags = { Name = "${local.name_prefix}-docs" }
}

resource "aws_s3_bucket_versioning" "docs" {
  bucket = aws_s3_bucket.docs.id

  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "docs" {
  bucket = aws_s3_bucket.docs.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm     = "aws:kms"
      kms_master_key_id = aws_kms_key.docs.arn
    }
    bucket_key_enabled = true
  }
}

resource "aws_s3_bucket_public_access_block" "docs" {
  bucket = aws_s3_bucket.docs.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# --- Seed initial docs and diagrams into S3 ---

resource "aws_s3_object" "docs" {
  for_each = fileset("${path.module}/../docs", "*.md")

  bucket = aws_s3_bucket.docs.id
  key    = "docs/${each.value}"
  source = "${path.module}/../docs/${each.value}"
  etag   = filemd5("${path.module}/../docs/${each.value}")
}

resource "aws_s3_object" "diagrams" {
  for_each = fileset("${path.module}/../diagrams", "*.mmd")

  bucket = aws_s3_bucket.docs.id
  key    = "diagrams/${each.value}"
  source = "${path.module}/../diagrams/${each.value}"
  etag   = filemd5("${path.module}/../diagrams/${each.value}")
}
