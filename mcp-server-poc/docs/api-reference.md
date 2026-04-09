# Nexus API Reference

Base URL: `https://api.nexus.internal/v1`

All endpoints require a valid `Authorization: Bearer <NEXUS_TOKEN>` header.

## Services API

### List Services
```
GET /services
```
Returns all services the authenticated user has access to.

**Response:**
```json
{
  "services": [
    {
      "id": "svc-abc123",
      "name": "user-service",
      "owner": "team-platform",
      "status": "healthy",
      "environment": "production"
    }
  ]
}
```

### Get Service Details
```
GET /services/{service_id}
```

**Response:**
```json
{
  "id": "svc-abc123",
  "name": "user-service",
  "owner": "team-platform",
  "status": "healthy",
  "replicas": 3,
  "version": "2.4.1",
  "endpoints": {
    "health": "/health",
    "metrics": "/metrics"
  },
  "last_deployed": "2025-01-15T10:30:00Z"
}
```

### Deploy Service
```
POST /services/{service_id}/deploy
```

**Request Body:**
```json
{
  "version": "2.5.0",
  "environment": "staging",
  "strategy": "rolling"
}
```

**Response:**
```json
{
  "deployment_id": "dep-xyz789",
  "status": "in_progress",
  "started_at": "2025-01-15T11:00:00Z"
}
```

Deployment strategies: `rolling` (default), `blue-green`, `canary`.

## Deployments API

### Get Deployment Status
```
GET /deployments/{deployment_id}
```

**Response:**
```json
{
  "deployment_id": "dep-xyz789",
  "service_id": "svc-abc123",
  "status": "completed",
  "strategy": "rolling",
  "started_at": "2025-01-15T11:00:00Z",
  "completed_at": "2025-01-15T11:05:30Z",
  "rollback_available": true
}
```

### Rollback Deployment
```
POST /deployments/{deployment_id}/rollback
```

Rolls back to the previous healthy version. Only available within 24 hours of deployment.

## Configuration API

### Get Service Config
```
GET /services/{service_id}/config
```

Returns the current configuration for a service (non-secret values only).

### Update Service Config
```
PATCH /services/{service_id}/config
```

**Request Body:**
```json
{
  "LOG_LEVEL": "debug",
  "MAX_CONNECTIONS": "50"
}
```

Config changes trigger a rolling restart of the service.

## Error Responses

All errors follow this format:
```json
{
  "error": {
    "code": "NOT_FOUND",
    "message": "Service svc-abc123 not found",
    "request_id": "req-def456"
  }
}
```

Common error codes:
| Code           | HTTP Status | Description                          |
|----------------|-------------|--------------------------------------|
| UNAUTHORIZED   | 401         | Missing or invalid token             |
| FORBIDDEN      | 403         | Insufficient permissions             |
| NOT_FOUND      | 404         | Resource does not exist              |
| RATE_LIMITED   | 429         | Too many requests (limit: 100/min)   |
| INTERNAL_ERROR | 500         | Unexpected server error              |

## Rate Limits

- **Standard**: 100 requests per minute per token
- **Deploy endpoints**: 10 requests per minute per service
- Rate limit headers: `X-RateLimit-Remaining`, `X-RateLimit-Reset`
