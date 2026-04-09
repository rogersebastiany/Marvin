# Nexus Platform Architecture

## Overview

Nexus is a microservices platform built for internal developer tooling. It provides a unified API gateway, shared infrastructure, and standardized service templates.

## System Components

### API Gateway
- **Technology**: Envoy proxy with custom Lua filters
- **Endpoint**: `https://api.nexus.internal`
- **Responsibilities**: routing, rate limiting, authentication verification, request logging
- All external traffic enters through the gateway; direct service-to-service calls use gRPC

### Service Mesh
- **Technology**: Istio on Kubernetes
- **Features**: mutual TLS, circuit breaking, retry policies
- Services communicate via service mesh without managing their own TLS certificates

### Database Layer
- **Primary**: PostgreSQL 16 cluster (managed by CloudNativePG)
- **Cache**: Redis 7 cluster for session data and rate limiting
- **Search**: Elasticsearch 8 for full-text search and log aggregation
- Each service gets a dedicated database schema; cross-schema queries are prohibited

### Message Queue
- **Technology**: Apache Kafka
- **Topics**: service events, audit logs, deployment notifications
- All inter-service async communication goes through Kafka; direct HTTP callbacks are not allowed

### Observability Stack
- **Metrics**: Prometheus + Grafana dashboards
- **Tracing**: Jaeger with OpenTelemetry SDK
- **Logging**: Structured JSON logs → Fluentd → Elasticsearch
- **Alerting**: PagerDuty integration via Alertmanager

## Deployment Pipeline

```
Code Push → GitHub Actions → Build Container → Push to Registry →
ArgoCD Sync → Kubernetes Rolling Update → Health Check → Traffic Shift
```

### Environments
| Environment | Cluster       | Auto-deploy | Approval Required |
|-------------|---------------|-------------|-------------------|
| Development | dev-cluster   | Yes (PR)    | No                |
| Staging     | stage-cluster | Yes (main)  | No                |
| Production  | prod-cluster  | No          | Yes (2 reviewers) |

## Security Model

- **Authentication**: OAuth 2.0 / OIDC via internal IdP
- **Authorization**: RBAC with service-level policies defined in OPA (Open Policy Agent)
- **Secrets**: HashiCorp Vault; services fetch secrets at startup via sidecar
- **Network**: zero-trust model; all inter-service traffic is encrypted via mTLS

## Data Flow Example

A typical API request flows through:

1. Client sends HTTPS request to `api.nexus.internal`
2. Envoy gateway verifies JWT token, applies rate limits
3. Request routed to target service via Istio mesh
4. Service processes request, queries PostgreSQL
5. Response returned through gateway with tracing headers
6. Audit event published to Kafka topic `nexus.audit.requests`
