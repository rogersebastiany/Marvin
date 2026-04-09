# Getting Started with Nexus Platform

Welcome to the Nexus internal developer platform. This guide walks you through setting up your development environment and deploying your first service.

## Prerequisites

- Access to the Nexus GitHub organization
- VPN connection to the internal network
- Docker Desktop installed (v24+)
- Node.js 20 LTS or Python 3.12+

## Authentication

All Nexus services use SSO via our internal identity provider. To authenticate:

1. Visit `https://auth.nexus.internal/login`
2. Sign in with your corporate credentials
3. Generate an API token at `https://auth.nexus.internal/tokens`
4. Export the token: `export NEXUS_TOKEN=<your-token>`

The token is valid for 90 days and grants access to all services your role permits.

## Creating Your First Service

Use the Nexus CLI to scaffold a new service:

```bash
nexus init my-service --template=python-fastapi
cd my-service
nexus dev
```

This creates a FastAPI service with:
- Health check endpoint at `/health`
- OpenTelemetry tracing pre-configured
- Connection to the shared PostgreSQL cluster
- CI/CD pipeline via GitHub Actions

## Deploying to Staging

Push to the `main` branch to trigger an automatic deployment to the staging environment:

```bash
git push origin main
```

Monitor the deployment at `https://deploy.nexus.internal/status`.

## Common Issues

### "Connection refused" when running locally
Make sure the VPN is active and Docker Desktop is running. The service needs access to internal dependencies.

### Authentication token expired
Regenerate your token at the auth portal. Tokens expire after 90 days of inactivity.

### Database migrations failing
Run `nexus db migrate` before starting the service. If migrations are out of sync, use `nexus db reset` (staging only — never in production).
