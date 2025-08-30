# GMC Dashboard API Documentation

**Version**: 0.1.0  
**Last Updated**: 2025-08-30  
**Base URL**: `http://localhost:8000` (via API Gateway) or individual service ports  

## Service Overview

The GMC Dashboard consists of 4 microservices, each with specific responsibilities:

| Service | Port | Database | Purpose |
|---------|------|----------|---------|
| **gmc-calculation-service** | 5000 | PostgreSQL | Core mathematical calculations |
| **knowledge-graph-service** | 5001 | Neo4j | Business rules & relationships |
| **conversation-service** | 5002 | MongoDB | AI coaching & conversations |
| **user-management-service** | 5003 | PostgreSQL | Authentication & API keys |

## Common Headers

All API requests should include:
```
Content-Type: application/json
X-Project-ID: {project_id}  # Required for project-scoped endpoints
Authorization: Bearer {jwt_token}  # Required for protected endpoints
```

---

# 1. GMC Calculation Service (`localhost:5000`)

**Purpose**: Core mathematical engine for GMC analysis with Excel compatibility

## Health Endpoints

### GET `/health`
**Description**: Health check for Kubernetes liveness probe  
**Response**:
```json
{
  "status": "healthy",
  "service": "gmc-calculation-service", 
  "version": "0.1.0",
  "timestamp": "2025-08-30T10:54:43.885907",
  "database": "healthy",
  "checks": {
    "database_connection": true,
    "service_ready": true
  }
}
```

### GET `/health/ready`
**Description**: Readiness check for Kubernetes deployment

## Service Information

### GET `/api/v1/info`
**Description**: Service capabilities and endpoint documentation  
**Response**:
```json
{
  "service": {
    "name": "gmc-calculation-service",
    "version": "0.1.0",
    "port": 5000,
    "database": "postgresql",
    "description": "Core GMC mathematical calculation engine",
    "status": "active"
  },
  "features": [
    "Project-scoped data isolation",
    "Excel-compatible calculations", 
    "Real-time parameter processing",
    "Investment performance analysis"
  ],
  "endpoints": [...]
}
```

## Project Management

### GET `/api/v1/projects`
**Description**: List projects accessible to current user  
**Headers**: `Authorization: Bearer {token}`

### GET `/api/v1/projects/{project_id}/sessions` 
**Description**: List calculation sessions for project  
**Headers**: `X-Project-ID: {project_id}`, `Authorization: Bearer {token}`

## Calculations

### POST `/api/v1/projects/{project_id}/calculate`
**Description**: Execute GMC parameter calculations  
**Headers**: `X-Project-ID: {project_id}`, `Authorization: Bearer {token}`  
**Request Body**:
```json
{
  "parameters": {
    "revenue": 100000,
    "costs": 80000,
    "timeframe": "12_months"
  },
  "calculation_type": "gmc_analysis"
}
```

---

# 2. Knowledge Graph Service (`localhost:5001`)

**Purpose**: GMC business rule relationships and strategic reasoning

## Service Information

### GET `/api/v1/info`
**Features**:
- GMC business rule relationships
- Strategic reasoning and analysis  
- Constraint dependency management
- Project-scoped knowledge contexts

## Knowledge Rules

### GET `/api/v1/projects/{project_id}/rules`
**Description**: Get GMC rules for specific project  
**Headers**: `X-Project-ID: {project_id}`

### GET `/api/v1/projects/{project_id}/relationships`
**Description**: Get rule relationships and dependencies  
**Headers**: `X-Project-ID: {project_id}`

## Strategic Analysis

### POST `/api/v1/projects/{project_id}/strategy`
**Description**: Analyze strategy implications using knowledge graph  
**Headers**: `X-Project-ID: {project_id}`, `Authorization: Bearer {token}`  
**Request Body**:
```json
{
  "strategy": "increase_revenue",
  "parameters": {...},
  "constraints": [...]
}
```

---

# 3. Conversation Service (`localhost:5002`)

**Purpose**: Conversational AI with project-scoped memory

## Service Information  

### GET `/api/v1/info`
**Features**:
- Multi-provider LLM support
- Project-scoped conversation memory
- Educational context awareness
- Individual user API key management
- Budget controls and usage tracking

## Chat & Conversations

### POST `/api/v1/projects/{project_id}/chat`
**Description**: Send chat message to AI coach  
**Headers**: `X-Project-ID: {project_id}`, `Authorization: Bearer {token}`  
**Request Body**:
```json
{
  "message": "How do I optimize my GMC analysis?",
  "context": "financial_analysis",
  "user_preferences": {...}
}
```

### GET `/api/v1/projects/{project_id}/history`
**Description**: Get conversation history for project  
**Headers**: `X-Project-ID: {project_id}`, `Authorization: Bearer {token}`

## LLM Configuration

### PUT `/api/v1/llm-config`
**Description**: Configure LLM provider settings  
**Headers**: `Authorization: Bearer {token}`  
**Request Body**:
```json
{
  "provider": "openai",
  "model": "gpt-4",
  "api_key": "encrypted_key",
  "budget_limit": 100.0
}
```

---

# 4. User Management Service (`localhost:5003`)

**Purpose**: Authentication and API key management

## Service Information

### GET `/api/v1/info`
**Features**:
- JWT-based authentication
- FERPA-compliant user management
- Encrypted API key storage
- Budget controls for AI services  
- Institutional boundaries

## Authentication

### POST `/api/v1/auth/register`
**Description**: Register new user account  
**Request Body**:
```json
{
  "email": "user@example.com",
  "password": "secure_password",
  "name": "John Doe",
  "institution": "University of Example"
}
```

### POST `/api/v1/auth/login`
**Description**: Authenticate user and get JWT token  
**Request Body**:
```json
{
  "email": "user@example.com", 
  "password": "secure_password"
}
```
**Response**:
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "user": {
    "id": "user_123",
    "email": "user@example.com",
    "name": "John Doe"
  }
}
```

### GET `/api/v1/auth/profile`
**Description**: Get current user profile  
**Headers**: `Authorization: Bearer {token}`

## API Key Management

### GET `/api/v1/api-keys`
**Description**: List user's API keys  
**Headers**: `Authorization: Bearer {token}`

### POST `/api/v1/api-keys`
**Description**: Create new API key  
**Headers**: `Authorization: Bearer {token}`  
**Request Body**:
```json
{
  "name": "Production API Key",
  "service": "openai",
  "budget_limit": 50.0,
  "expires_at": "2025-12-31T23:59:59Z"
}
```

---

# Project Data Isolation

All services implement **project-scoped data isolation**:

1. **Required Header**: `X-Project-ID: {project_id}` for all project-scoped endpoints
2. **Database Constraints**: All tables include `project_id` foreign keys
3. **Query Filtering**: All database queries automatically filter by project context
4. **Cross-Project Prevention**: Services prevent access to other projects' data

## Error Responses

### 400 Bad Request
```json
{
  "error": "Bad Request",
  "message": "Missing required X-Project-ID header",
  "service": "service-name"
}
```

### 401 Unauthorized  
```json
{
  "error": "Unauthorized",
  "message": "Invalid or expired JWT token",
  "service": "service-name"
}
```

### 403 Forbidden
```json
{
  "error": "Forbidden", 
  "message": "Access denied to project resources",
  "service": "service-name"
}
```

### 404 Not Found
```json
{
  "error": "Not Found",
  "message": "The requested resource was not found", 
  "service": "service-name"
}
```

## Testing Examples

### Test Service Health
```bash
curl -X GET http://localhost:5000/health
curl -X GET http://localhost:5001/health  
curl -X GET http://localhost:5002/health
curl -X GET http://localhost:5003/health
```

### Test Service Information
```bash
curl -X GET http://localhost:5000/api/v1/info
curl -X GET http://localhost:5001/api/v1/info
curl -X GET http://localhost:5002/api/v1/info  
curl -X GET http://localhost:5003/api/v1/info
```

### Test Authentication Flow
```bash
# Register user
curl -X POST http://localhost:5003/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123","name":"Test User"}'

# Login and get token  
curl -X POST http://localhost:5003/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}'
```

---

**Status**: All 4 services are **healthy and operational** with full API documentation complete.