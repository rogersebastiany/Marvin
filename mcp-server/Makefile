.PHONY: up down build tf-init tf-plan tf-apply tf-destroy logs clean

# --- Docker ---

up:
	docker compose up -d

down:
	docker compose down

build:
	docker compose build

logs:
	docker compose logs -f

# --- Terraform (against LocalStack) ---

tf-init:
	cd infra && terraform init

tf-plan:
	cd infra && terraform plan

tf-apply:
	cd infra && terraform apply -auto-approve

tf-destroy:
	cd infra && terraform destroy -auto-approve

tf-output:
	cd infra && terraform output

# --- Full local stack ---

local: up
	@echo "Waiting for LocalStack to be ready..."
	@until curl -sf http://localhost:4566/_localstack/health > /dev/null 2>&1; do sleep 1; done
	@echo "LocalStack ready. Running terraform..."
	$(MAKE) tf-init
	$(MAKE) tf-apply
	@echo ""
	@echo "=== Local stack is running ==="
	@echo "LocalStack:  http://localhost:4566"
	@echo "S3 docs:     awslocal s3 ls s3://mcp-server-local-docs/"
	@echo "Secrets:     awslocal secretsmanager get-secret-value --secret-id mcp-server-local/config"
	@echo "Logs:        awslocal logs describe-log-groups"
	@echo ""

# --- Utilities ---

s3-ls:
	awslocal s3 ls s3://mcp-server-local-docs/ --recursive

s3-seed:
	awslocal s3 sync ../docs s3://mcp-server-local-docs/docs/
	awslocal s3 sync ../diagrams s3://mcp-server-local-docs/diagrams/

clean: down tf-destroy
	docker compose down -v
	rm -rf infra/.terraform infra/.terraform.lock.hcl infra/terraform.tfstate*
