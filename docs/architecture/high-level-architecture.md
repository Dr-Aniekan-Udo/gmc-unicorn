# High Level Architecture

Based on the comprehensive analysis and starter template evaluation, I'll now present the complete high-level architecture with all subsections integrated:

## Technical Summary

The GMC Dashboard employs a **Microservices Architecture with Project Management Foundation** enabling multiple independent GMC analysis projects with comprehensive data isolation and strategic experimentation capabilities. The system consists of 10 specialized Flask microservices with dedicated databases, React SPA frontend with project-aware navigation, and Kubernetes orchestration for scalable deployment.

**Core Architecture Pattern:** Database-per-service microservices with project-scoped data isolation, API Gateway routing, and Service Mesh communication. Each project maintains complete independence with dedicated AI coaching contexts, competitive intelligence analysis, and timeline management.

**Critical Integration Points:** Project-aware API routing, real-time collaboration within project boundaries, project-scoped offline capability, and multi-database coordination for AI/ML operations. Infrastructure supports complete project data isolation while enabling cross-project analytics and strategic experimentation.

The infrastructure deploys on **Kubernetes with Helm charts** providing automatic scaling, FERPA-compliant data handling, and sophisticated project isolation enforcement, enabling consistent user experience across multiple concurrent strategic analysis projects.

## Platform and Infrastructure Choice

**Microservices Architecture Deployment (PRD v6.0 Aligned)**
- **Architecture Pattern:** Database-per-service microservices with React frontend and API Gateway
- **Frontend:** React SPA with Dash integration for mathematical visualizations
- **API Gateway:** Kong/Traefik for service routing, authentication, and rate limiting
- **Service Mesh:** Istio for inter-service communication, observability, and security
- **Container Orchestration:** Kubernetes with Helm charts for deployment management

**Core Services:**
- **GMC Calculation Service:** Python Flask + PostgreSQL (GMC analysis, user sessions, Excel integration)
- **Knowledge Graph Service:** Python Flask + Neo4j (GMC rule relationships, strategy reasoning)
- **Content Management Service:** Python Flask + MongoDB (GMC Manual, document versioning)
- **User Management Service:** Python Flask + PostgreSQL (authentication, API keys, FERPA compliance)
- **Analytics Service:** Python Flask + PostgreSQL + ClickHouse (educational analytics, faculty dashboard)
- **Notification Service:** Python Flask + Redis (real-time updates, team collaboration)

**AI Coaching Ecosystem (Decomposed for AI Agent Implementation):**
- **Conversation Service:** Python Flask + Rasa + MongoDB (conversational AI, natural language processing, project-scoped chat history)
- **Vector Search Service:** Python Flask + Weaviate (semantic search over GMC Manual, knowledge retrieval, embeddings)
- **ML Recommendation Service:** Python Flask + CatBoost + XGBoost + MLflow (parameter optimization, classical ML predictions, experiment tracking)
- **Coaching Orchestrator:** Python Flask + Redis (AI service coordination, unified user experience, intelligent routing)

**Post-MVP API Extensions:**
- **API Layer:** Flask integration for external system integration
- **Automation:** N8n workflow engine for advanced automation scenarios
- **Authentication:** Campus SSO and institutional boundary management

## Comprehensive Deployment Orchestration Guide

### **Kubernetes Production Deployment**

**1. Namespace Organization**
```yaml
# namespace-configuration.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: gmc-dashboard-prod
  labels:
    environment: production
    project: gmc-dashboard
---
apiVersion: v1
kind: Namespace
metadata:
  name: gmc-dashboard-staging
  labels:
    environment: staging
    project: gmc-dashboard
```

**2. ConfigMap and Secret Management**
```yaml
# config-maps.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: gmc-dashboard-config
  namespace: gmc-dashboard-prod
data:
  # Service URLs (internal Kubernetes DNS)
  GMC_CALCULATION_SERVICE_URL: "http://gmc-calculation-service:5000"
  KNOWLEDGE_GRAPH_SERVICE_URL: "http://knowledge-graph-service:5001"
  AI_COACHING_SERVICE_URL: "http://ai-coaching-service:5002"
  USER_MANAGEMENT_SERVICE_URL: "http://user-management-service:5003"
  
  # Database configurations
  POSTGRES_CALC_HOST: "postgresql-calc-service"
  POSTGRES_USER_HOST: "postgresql-user-service"
  NEO4J_HOST: "neo4j-service"
  WEAVIATE_HOST: "weaviate-service"
  MONGODB_HOST: "mongodb-service"
  REDIS_HOST: "redis-service"
  
  # Performance configurations
  FLASK_ENV: "production"
  FLASK_DEBUG: "false"
  
  # Educational compliance
  FERPA_COMPLIANCE_MODE: "enabled"
  AUDIT_LOGGING_LEVEL: "detailed"

---
apiVersion: v1
kind: Secret
metadata:
  name: gmc-dashboard-secrets
  namespace: gmc-dashboard-prod
type: Opaque
stringData:
  # Service-to-service authentication
  SERVICE_SECRET_KEY: "your-service-secret-key-here"
  
  # Database credentials
  POSTGRES_CALC_PASSWORD: "calc-db-password"
  POSTGRES_USER_PASSWORD: "user-db-password"
  NEO4J_PASSWORD: "neo4j-password"
  MONGODB_PASSWORD: "mongodb-password"
  
  # External service keys (for system operations)
  SYSTEM_ANTHROPIC_API_KEY: "system-anthropic-key"
```

**3. Database Services Deployment**
```yaml
# postgresql-calc-service.yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: postgresql-calc
  namespace: gmc-dashboard-prod
spec:
  serviceName: postgresql-calc-service
  replicas: 1
  selector:
    matchLabels:
      app: postgresql-calc
  template:
    metadata:
      labels:
        app: postgresql-calc
    spec:
      containers:
      - name: postgresql
        image: postgres:15
        env:
        - name: POSTGRES_DB
          value: gmc_calculations
        - name: POSTGRES_USER
          value: gmc_calc_user
        - name: POSTGRES_PASSWORD
          valueFrom:
            secretKeyRef:
              name: gmc-dashboard-secrets
              key: POSTGRES_CALC_PASSWORD
        ports:
        - containerPort: 5432
        volumeMounts:
        - name: postgres-calc-storage
          mountPath: /var/lib/postgresql/data
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "2Gi"
            cpu: "1000m"
  volumeClaimTemplates:
  - metadata:
      name: postgres-calc-storage
    spec:
      accessModes: ["ReadWriteOnce"]
      resources:
        requests:
          storage: 10Gi

---
apiVersion: v1
kind: Service
metadata:
  name: postgresql-calc-service
  namespace: gmc-dashboard-prod
spec:
  selector:
    app: postgresql-calc
  ports:
  - port: 5432
    targetPort: 5432
  type: ClusterIP

---
# neo4j-service.yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: neo4j
  namespace: gmc-dashboard-prod
spec:
  serviceName: neo4j-service
  replicas: 1
  selector:
    matchLabels:
      app: neo4j
  template:
    metadata:
      labels:
        app: neo4j
    spec:
      containers:
      - name: neo4j
        image: neo4j:5.0-community
        env:
        - name: NEO4J_AUTH
          valueFrom:
            secretKeyRef:
              name: gmc-dashboard-secrets
              key: NEO4J_PASSWORD
        - name: NEO4J_dbms_memory_heap_initial__size
          value: "512m"
        - name: NEO4J_dbms_memory_heap_max__size
          value: "2G"
        ports:
        - containerPort: 7474  # HTTP
        - containerPort: 7687  # Bolt
        volumeMounts:
        - name: neo4j-data
          mountPath: /data
        resources:
          requests:
            memory: "1Gi"
            cpu: "500m"
          limits:
            memory: "4Gi"
            cpu: "2000m"
  volumeClaimTemplates:
  - metadata:
      name: neo4j-data
    spec:
      accessModes: ["ReadWriteOnce"]
      resources:
        requests:
          storage: 5Gi
```

**4. Microservice Deployment Templates**
```yaml
# gmc-calculation-service.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: gmc-calculation-service
  namespace: gmc-dashboard-prod
spec:
  replicas: 3  # Horizontal scaling for calculation-heavy workload
  selector:
    matchLabels:
      app: gmc-calculation-service
  template:
    metadata:
      labels:
        app: gmc-calculation-service
      annotations:
        prometheus.io/scrape: "true"
        prometheus.io/port: "5000"
        prometheus.io/path: "/metrics"
    spec:
      containers:
      - name: gmc-calculation-service
        image: gmc-dashboard/calculation-service:latest
        ports:
        - containerPort: 5000
        env:
        - name: SERVICE_NAME
          value: "gmc_calculation_service"
        - name: DATABASE_URL
          value: "postgresql://gmc_calc_user:$(POSTGRES_CALC_PASSWORD)@postgresql-calc-service:5432/gmc_calculations"
        envFrom:
        - configMapRef:
            name: gmc-dashboard-config
        - secretRef:
            name: gmc-dashboard-secrets
        resources:
          requests:
            memory: "256Mi"
            cpu: "100m"
          limits:
            memory: "1Gi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 5000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health/ready
            port: 5000
          initialDelaySeconds: 5
          periodSeconds: 5

---
apiVersion: v1
kind: Service
metadata:
  name: gmc-calculation-service
  namespace: gmc-dashboard-prod
spec:
  selector:
    app: gmc-calculation-service
  ports:
  - port: 5000
    targetPort: 5000
  type: ClusterIP

---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: gmc-calculation-service-hpa
  namespace: gmc-dashboard-prod
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: gmc-calculation-service
  minReplicas: 3
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

**5. API Gateway Configuration**
```yaml
# kong-gateway.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: kong-gateway
  namespace: gmc-dashboard-prod
spec:
  replicas: 2
  selector:
    matchLabels:
      app: kong-gateway
  template:
    metadata:
      labels:
        app: kong-gateway
    spec:
      containers:
      - name: kong
        image: kong:3.0
        env:
        - name: KONG_DATABASE
          value: "off"
        - name: KONG_DECLARATIVE_CONFIG
          value: "/kong/declarative/kong.yml"
        - name: KONG_PROXY_ACCESS_LOG
          value: "/dev/stdout"
        - name: KONG_ADMIN_ACCESS_LOG
          value: "/dev/stdout"
        - name: KONG_PROXY_ERROR_LOG
          value: "/dev/stderr"
        - name: KONG_ADMIN_ERROR_LOG
          value: "/dev/stderr"
        ports:
        - containerPort: 8000  # Proxy HTTP
        - containerPort: 8443  # Proxy HTTPS
        - containerPort: 8001  # Admin API HTTP
        volumeMounts:
        - name: kong-config
          mountPath: /kong/declarative
        resources:
          requests:
            memory: "256Mi"
            cpu: "100m"
          limits:
            memory: "512Mi"
            cpu: "300m"
      volumes:
      - name: kong-config
        configMap:
          name: kong-config

---
apiVersion: v1
kind: ConfigMap
metadata:
  name: kong-config
  namespace: gmc-dashboard-prod
data:
  kong.yml: |
    _format_version: "3.0"
    
    services:
      - name: gmc-calculation-service
        url: http://gmc-calculation-service:5000
        routes:
          - name: calculation-routes
            paths:
              - /api/v1/calculations
              - /api/v1/sessions
        plugins:
          - name: rate-limiting
            config:
              minute: 100
              hour: 1000
          - name: jwt
            config:
              key_claim_name: iss
      
      - name: knowledge-graph-service
        url: http://knowledge-graph-service:5001
        routes:
          - name: knowledge-routes
            paths:
              - /api/v1/knowledge
              - /api/v1/rules
        plugins:
          - name: rate-limiting
            config:
              minute: 50
              hour: 500
          - name: jwt
            config:
              key_claim_name: iss
      
      - name: ai-coaching-service
        url: http://ai-coaching-service:5002
        routes:
          - name: coaching-routes
            paths:
              - /api/v1/coaching
              - /api/v1/recommendations
        plugins:
          - name: rate-limiting
            config:
              minute: 20  # Lower rate limit for AI services
              hour: 200
          - name: jwt
            config:
              key_claim_name: iss

---
apiVersion: v1
kind: Service
metadata:
  name: kong-gateway-service
  namespace: gmc-dashboard-prod
spec:
  selector:
    app: kong-gateway
  ports:
  - name: proxy
    port: 8000
    targetPort: 8000
  - name: proxy-ssl
    port: 8443
    targetPort: 8443
  type: LoadBalancer
```

### **Docker Compose Development Environment**

**1. Complete Development Stack**
```yaml
# docker-compose.yml
version: '3.8'

services:
  # Database Services
  postgres-calc:
    image: postgres:15
    environment:
      POSTGRES_DB: gmc_calculations
      POSTGRES_USER: gmc_calc_user
      POSTGRES_PASSWORD: calc_password
    ports:
      - "5432:5432"
    volumes:
      - postgres_calc_data:/var/lib/postgresql/data
    networks:
      - gmc-network

  postgres-user:
    image: postgres:15
    environment:
      POSTGRES_DB: gmc_users
      POSTGRES_USER: gmc_user_user
      POSTGRES_PASSWORD: user_password
    ports:
      - "5433:5432"
    volumes:
      - postgres_user_data:/var/lib/postgresql/data
    networks:
      - gmc-network

  neo4j:
    image: neo4j:5.0-community
    environment:
      NEO4J_AUTH: neo4j/knowledge_password
      NEO4J_dbms_memory_heap_initial__size: 512m
      NEO4J_dbms_memory_heap_max__size: 1G
    ports:
      - "7474:7474"  # HTTP
      - "7687:7687"  # Bolt
    volumes:
      - neo4j_data:/data
    networks:
      - gmc-network

  weaviate:
    image: semitechnologies/weaviate:latest
    ports:
      - "8080:8080"
    environment:
      QUERY_DEFAULTS_LIMIT: 25
      AUTHENTICATION_ANONYMOUS_ACCESS_ENABLED: 'true'
      PERSISTENCE_DATA_PATH: '/var/lib/weaviate'
      DEFAULT_VECTORIZER_MODULE: 'none'
    volumes:
      - weaviate_data:/var/lib/weaviate
    networks:
      - gmc-network

  mongodb:
    image: mongo:7.0
    environment:
      MONGO_INITDB_ROOT_USERNAME: gmc_admin
      MONGO_INITDB_ROOT_PASSWORD: mongo_password
    ports:
      - "27017:27017"
    volumes:
      - mongodb_data:/data/db
    networks:
      - gmc-network

  redis:
    image: redis:7.2
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    networks:
      - gmc-network

  clickhouse:
    image: yandex/clickhouse-server:latest
    ports:
      - "8123:8123"
      - "9000:9000"
    volumes:
      - clickhouse_data:/var/lib/clickhouse
    networks:
      - gmc-network

  # Application Services
  gmc-calculation-service:
    build:
      context: ./services/gmc-calculation-service
      dockerfile: Dockerfile
    environment:
      - SERVICE_NAME=gmc_calculation_service
      - DATABASE_URL=postgresql://gmc_calc_user:calc_password@postgres-calc:5432/gmc_calculations
      - REDIS_URL=redis://redis:6379/0
      - FLASK_ENV=development
    ports:
      - "5000:5000"
    depends_on:
      - postgres-calc
      - redis
    volumes:
      - ./services/gmc-calculation-service:/app
    networks:
      - gmc-network

  knowledge-graph-service:
    build:
      context: ./services/knowledge-graph-service
      dockerfile: Dockerfile
    environment:
      - SERVICE_NAME=knowledge_graph_service
      - NEO4J_URI=bolt://neo4j:7687
      - NEO4J_USER=neo4j
      - NEO4J_PASSWORD=knowledge_password
      - FLASK_ENV=development
    ports:
      - "5001:5001"
    depends_on:
      - neo4j
    volumes:
      - ./services/knowledge-graph-service:/app
    networks:
      - gmc-network

  ai-coaching-service:
    build:
      context: ./services/ai-coaching-service
      dockerfile: Dockerfile
    environment:
      - SERVICE_NAME=ai_coaching_service
      - WEAVIATE_URL=http://weaviate:8080
      - MONGODB_URL=mongodb://gmc_admin:mongo_password@mongodb:27017/gmc_coaching
      - REDIS_URL=redis://redis:6379/1
      - FLASK_ENV=development
    ports:
      - "5002:5002"
    depends_on:
      - weaviate
      - mongodb
      - redis
    volumes:
      - ./services/ai-coaching-service:/app
    networks:
      - gmc-network

  # Frontend
  react-frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile.dev
    environment:
      - REACT_APP_API_BASE_URL=http://localhost:8000
    ports:
      - "3000:3000"
    volumes:
      - ./frontend:/app
      - /app/node_modules
    networks:
      - gmc-network

  # API Gateway
  kong:
    image: kong:3.0
    environment:
      KONG_DATABASE: 'off'
      KONG_DECLARATIVE_CONFIG: /kong/declarative/kong.yml
      KONG_PROXY_ACCESS_LOG: /dev/stdout
      KONG_ADMIN_ACCESS_LOG: /dev/stdout
      KONG_PROXY_ERROR_LOG: /dev/stderr
      KONG_ADMIN_ERROR_LOG: /dev/stderr
    ports:
      - "8000:8000"  # Proxy HTTP
      - "8001:8001"  # Admin API
    volumes:
      - ./kong/kong.yml:/kong/declarative/kong.yml
    networks:
      - gmc-network

volumes:
  postgres_calc_data:
  postgres_user_data:
  neo4j_data:
  weaviate_data:
  mongodb_data:
  redis_data:
  clickhouse_data:

networks:
  gmc-network:
    driver: bridge
```

### **Deployment Environment Configurations**

**1. Development Environment**
```bash
# scripts/dev-setup.sh
#!/bin/bash

echo "Setting up GMC Dashboard Development Environment"

# Create necessary directories
mkdir -p ./services/{gmc-calculation-service,knowledge-graph-service,ai-coaching-service}
mkdir -p ./config/{development,staging,production}
mkdir -p ./database/migrations
mkdir -p ./kong

# Generate development configuration
cat > ./config/development/.env << EOF
# Development Configuration
FLASK_ENV=development
FLASK_DEBUG=true

# Service URLs (Docker Compose internal network)
GMC_CALCULATION_SERVICE_URL=http://gmc-calculation-service:5000
KNOWLEDGE_GRAPH_SERVICE_URL=http://knowledge-graph-service:5001
AI_COACHING_SERVICE_URL=http://ai-coaching-service:5002

# Database URLs
POSTGRES_CALC_URL=postgresql://gmc_calc_user:calc_password@postgres-calc:5432/gmc_calculations
POSTGRES_USER_URL=postgresql://gmc_user_user:user_password@postgres-user:5432/gmc_users
NEO4J_URI=bolt://neo4j:7687
MONGODB_URL=mongodb://gmc_admin:mongo_password@mongodb:27017
REDIS_URL=redis://redis:6379

# Development secrets (not for production)
SERVICE_SECRET_KEY=dev-secret-key-not-for-production
JWT_SECRET_KEY=dev-jwt-secret-not-for-production
EOF

# Start development environment
docker-compose up -d

echo "Development environment started. Services available at:"
echo "- Frontend: http://localhost:3000"
echo "- API Gateway: http://localhost:8000"
echo "- Neo4j Browser: http://localhost:7474"
echo "- Weaviate: http://localhost:8080"
```

**2. Production Deployment Script**
```bash
# scripts/production-deploy.sh
#!/bin/bash

set -e  # Exit on any error

NAMESPACE="gmc-dashboard-prod"
CLUSTER_NAME="gmc-production-cluster"

echo "Deploying GMC Dashboard to Production Kubernetes Cluster"

# Verify kubectl context
kubectl config current-context
read -p "Are you sure you want to deploy to production? (yes/no): " confirm
if [ "$confirm" != "yes" ]; then
    echo "Deployment cancelled"
    exit 1
fi

# Create namespace if it doesn't exist
kubectl create namespace $NAMESPACE --dry-run=client -o yaml | kubectl apply -f -

# Apply database services first (they take longer to start)
echo "Deploying database services..."
kubectl apply -f ./k8s/databases/ -n $NAMESPACE

# Wait for databases to be ready
echo "Waiting for databases to be ready..."
kubectl wait --for=condition=ready pod -l app=postgresql-calc -n $NAMESPACE --timeout=300s
kubectl wait --for=condition=ready pod -l app=neo4j -n $NAMESPACE --timeout=300s
kubectl wait --for=condition=ready pod -l app=mongodb -n $NAMESPACE --timeout=300s

# Apply application services
echo "Deploying application services..."
kubectl apply -f ./k8s/services/ -n $NAMESPACE

# Apply ingress and gateway
echo "Deploying API Gateway and Ingress..."
kubectl apply -f ./k8s/gateway/ -n $NAMESPACE

# Wait for all deployments to be ready
echo "Waiting for all services to be ready..."
kubectl rollout status deployment/gmc-calculation-service -n $NAMESPACE
kubectl rollout status deployment/knowledge-graph-service -n $NAMESPACE
kubectl rollout status deployment/ai-coaching-service -n $NAMESPACE

echo "Production deployment completed successfully!"
echo "API Gateway: https://gmc-dashboard.yourdomain.com"
```

**Regulatory Compliance Framework:**
- **Multi-Jurisdictional Support:** FERPA (US), GDPR (EU), PIPEDA (Canada), local privacy law compliance modules
- **Data Residency Configuration:** Configurable per-institution data location with cross-border collaboration limitations
- **Academic Calendar Integration:** Global academic calendar awareness preventing maintenance during critical analysis periods

**Platform:** Adaptive Resilient (Kubernetes microservices primary, Docker enterprise pathway, static fallback, hybrid international)
**Key Services:** Flask microservices with PostgreSQL/Neo4j/MongoDB, IndexedDB with quota management, WebAssembly precision modules, Redis for real-time collaboration
**Deployment Host and Regions:** Global with academic resilience (multi-region availability, calendar-aware maintenance, regulatory compliance)

## Repository Structure

**Structure:** Microservices monorepo with database-per-service architecture  
**Package Management:** 
- **Python Services:** uv for fast dependency resolution and secure package management
- **React Frontend:** npm for JavaScript/TypeScript ecosystem and build tools
- **Containerization:** Docker for consistent deployment across environments
**Organization:** Service-oriented modules with clear boundaries and shared libraries

```
gmc-dashboard/
├── intelligence/                    # AI infrastructure directory per FR26
│   ├── api-configs/        # Service-specific AI configuration files
│   ├── classical-ml-models/ # CatBoost/XGBoost/Scikit model storage
│   ├── llm-prompts/        # Structured prompt libraries for optimization
│   ├── deployment-configs/ # Multi-environment AI deployment configurations
│   ├── training-data/      # ML training and validation datasets
│   ├── agent-configs/      # AI agent YAML configurations
│   ├── prompts/           # Legacy prompt directory (backward compatibility)
│   ├── models/            # Legacy model directory (backward compatibility)
│   ├── debug-log.md       # AI development tracking and debugging
│   └── README.md          # AI infrastructure documentation
├── services/               # Microservices directory
│   ├── gmc-calculation-service/    # GMC mathematical engine service
│   │   ├── app/
│   │   │   ├── __init__.py
│   │   │   ├── main.py         # Flask application entry point
│   │   │   ├── models/         # PostgreSQL models (SQLAlchemy)
│   │   │   ├── routes/         # API endpoints and handlers
│   │   │   ├── services/       # Business logic and Excel integration
│   │   │   ├── utils/          # Mathematical utilities and validation
│   │   │   └── config.py       # Service configuration
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   ├── tests/
│   │   └── README.md
│   ├── knowledge-graph-service/    # Neo4j GMC rule relationships service
│   │   ├── app/
│   │   │   ├── __init__.py
│   │   │   ├── main.py         # Flask application entry point
│   │   │   ├── models/         # Neo4j graph models
│   │   │   ├── routes/         # Graph query API endpoints
│   │   │   ├── services/       # Graph reasoning and traversal
│   │   │   ├── cypher/         # Cypher query templates
│   │   │   └── config.py       # Neo4j connection configuration
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   ├── tests/
│   │   └── README.md
│   ├── ai-coaching/                 # AI Coaching Ecosystem (Decomposed Architecture)
│   │   ├── conversation-service/    # Natural language interaction service
│   │   │   ├── app/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── main.py         # Flask application entry point
│   │   │   │   ├── models/         # MongoDB conversation models
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── conversation.py      # Project-scoped conversations
│   │   │   │   │   ├── user_preferences.py # LLM provider preferences
│   │   │   │   │   └── project_context.py  # Project-specific AI context
│   │   │   │   ├── routes/         # Conversation API endpoints
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── chat.py             # POST /chat, GET /history endpoints
│   │   │   │   │   ├── llm_config.py       # PUT /llm-provider configuration
│   │   │   │   │   └── project_chat.py     # Project-scoped chat management
│   │   │   │   ├── services/       # Business logic and integrations
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── rasa_integration.py # Rasa chatbot integration
│   │   │   │   │   ├── llm_manager.py      # Multi-provider LLM management
│   │   │   │   │   │   # Supports: OpenAI, Anthropic, Gemini, DeepSeek, OpenRouter, Ollama
│   │   │   │   │   ├── project_context.py  # Project isolation logic
│   │   │   │   │   └── conversation_memory.py # Persistent conversation state
│   │   │   │   ├── llm_providers/  # LLM provider implementations
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── openai_client.py    # OpenAI GPT-4/GPT-3.5 integration
│   │   │   │   │   ├── anthropic_client.py # Claude-3/Claude-2 integration
│   │   │   │   │   ├── gemini_client.py    # Google Gemini Pro integration
│   │   │   │   │   ├── deepseek_client.py  # DeepSeek Coder integration
│   │   │   │   │   ├── openrouter_client.py # OpenRouter multi-model access
│   │   │   │   │   ├── ollama_client.py    # Local Ollama integration
│   │   │   │   │   └── provider_factory.py # LLM provider factory
│   │   │   │   └── config.py       # MongoDB + intelligence directory integration
│   │   │   ├── Dockerfile
│   │   │   ├── requirements.txt    # rasa + pymongo + openai + anthropic + google-generativeai + deepseek
│   │   │   ├── tests/
│   │   │   │   ├── test_chat.py
│   │   │   │   ├── test_llm_providers.py
│   │   │   │   └── test_project_isolation.py
│   │   │   └── README.md
│   │   ├── vector-search-service/   # Semantic search and knowledge retrieval service
│   │   │   ├── app/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── main.py         # Flask application entry point
│   │   │   │   ├── models/         # Weaviate schema definitions
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── gmc_manual_schema.py # GMC Manual knowledge structure
│   │   │   │   │   ├── project_embeddings.py # Project-scoped embeddings
│   │   │   │   │   └── search_results.py    # Search result models
│   │   │   │   ├── routes/         # Search API endpoints
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── semantic_search.py  # POST /search, GET /similar endpoints
│   │   │   │   │   ├── knowledge_base.py   # GET /knowledge, POST /index endpoints
│   │   │   │   │   └── project_search.py   # Project-aware search routing
│   │   │   │   ├── services/       # Search logic and processing
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── weaviate_client.py  # Weaviate database operations
│   │   │   │   │   ├── embedding_service.py # Text embedding generation
│   │   │   │   │   ├── gmc_parser.py       # GMC Manual content parsing
│   │   │   │   │   └── search_orchestrator.py # Search result coordination
│   │   │   │   ├── embeddings/     # Embedding generation utilities
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── text_processor.py   # Text preprocessing
│   │   │   │   │   ├── chunk_strategy.py   # Document chunking
│   │   │   │   │   └── vector_store.py     # Vector storage management
│   │   │   │   └── config.py       # Weaviate + intelligence directory integration
│   │   │   ├── Dockerfile
│   │   │   ├── requirements.txt    # weaviate-client + sentence-transformers + flask
│   │   │   ├── tests/
│   │   │   │   ├── test_search.py
│   │   │   │   ├── test_embeddings.py
│   │   │   │   └── test_gmc_parsing.py
│   │   │   └── README.md
│   │   ├── ml-recommendation-service/ # Classical ML predictions and optimization service
│   │   │   ├── app/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── main.py         # Flask application entry point
│   │   │   │   ├── models/         # ML model definitions and storage
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── catboost_models.py  # CatBoost model definitions
│   │   │   │   │   ├── xgboost_models.py   # XGBoost model definitions
│   │   │   │   │   ├── model_registry.py   # Model versioning and storage
│   │   │   │   │   └── prediction_schemas.py # Prediction result schemas
│   │   │   │   ├── routes/         # ML prediction API endpoints
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── predictions.py      # POST /predict, GET /model-info endpoints
│   │   │   │   │   ├── optimization.py     # POST /optimize, GET /sensitivity endpoints
│   │   │   │   │   └── training.py        # POST /train, GET /metrics endpoints
│   │   │   │   ├── services/       # ML pipeline and orchestration
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── prediction_engine.py # Core prediction logic
│   │   │   │   │   ├── optimization_engine.py # Parameter optimization
│   │   │   │   │   ├── model_trainer.py    # Model training pipelines
│   │   │   │   │   ├── feature_engineer.py # Feature engineering
│   │   │   │   │   └── mlflow_integration.py # Experiment tracking
│   │   │   │   ├── ml_pipeline/    # Machine learning pipeline components
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── data_preprocessor.py # Data cleaning and preparation
│   │   │   │   │   ├── feature_extractor.py # Feature extraction from GMC data
│   │   │   │   │   ├── model_selector.py   # Automated model selection
│   │   │   │   │   ├── hyperparameter_tuner.py # Hyperparameter optimization
│   │   │   │   │   └── performance_evaluator.py # Model performance evaluation
│   │   │   │   ├── classical_ml/   # Classical ML algorithm implementations
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── catboost_wrapper.py # CatBoost model wrapper
│   │   │   │   │   ├── xgboost_wrapper.py  # XGBoost model wrapper
│   │   │   │   │   ├── ensemble_methods.py # Model ensemble strategies
│   │   │   │   │   └── constraint_solver.py # GMC constraint validation
│   │   │   │   └── config.py       # MLflow + intelligence directory integration
│   │   │   ├── Dockerfile
│   │   │   ├── requirements.txt    # catboost + xgboost + mlflow + scikit-learn
│   │   │   ├── tests/
│   │   │   │   ├── test_predictions.py
│   │   │   │   ├── test_optimization.py
│   │   │   │   ├── test_model_training.py
│   │   │   │   └── test_constraint_validation.py
│   │   │   └── README.md
│   │   └── coaching-orchestrator/   # AI service coordination and unified user experience
│   │       ├── app/
│   │       │   ├── __init__.py
│   │       │   ├── main.py         # Flask application entry point
│   │       │   ├── models/         # Orchestration data models
│   │       │   │   ├── __init__.py
│   │       │   │   ├── coaching_session.py # User coaching session state
│   │       │   │   ├── service_health.py   # Service health monitoring
│   │       │   │   └── user_journey.py     # User interaction flow
│   │       │   ├── routes/         # Unified AI coaching API endpoints
│   │       │   │   ├── __init__.py
│   │       │   │   ├── ai_coach.py         # POST /ai-coach/chat unified interface
│   │       │   │   ├── recommendations.py  # GET /ai-coach/recommendations
│   │       │   │   ├── project_analysis.py # GET /ai-coach/analyze/{project_id}
│   │       │   │   └── health_check.py     # GET /health service monitoring
│   │       │   ├── services/       # Orchestration logic and service integration
│   │       │   │   ├── __init__.py
│   │       │   │   ├── service_coordinator.py # AI service coordination logic
│   │       │   │   ├── conversation_router.py # Route requests to conversation service
│   │       │   │   ├── knowledge_router.py    # Route requests to vector search
│   │       │   │   ├── ml_router.py          # Route requests to ML recommendations
│   │       │   │   ├── response_synthesizer.py # Combine multi-service responses
│   │       │   │   ├── project_context_manager.py # Project isolation enforcement
│   │       │   │   └── error_handler.py      # Graceful service failure handling
│   │       │   ├── orchestration/  # Service orchestration patterns
│   │       │   │   ├── __init__.py
│   │       │   │   ├── workflow_engine.py    # Multi-step AI workflow coordination
│   │       │   │   ├── service_registry.py   # Dynamic service discovery
│   │       │   │   ├── load_balancer.py      # AI service load balancing
│   │       │   │   ├── circuit_breaker.py    # Service failure protection
│   │       │   │   └── cache_manager.py      # Response caching and optimization
│   │       │   └── config.py       # Service URLs + Redis coordination configuration
│   │       ├── Dockerfile
│   │       ├── requirements.txt    # flask + redis + requests + circuit-breaker
│   │       ├── tests/
│   │       │   ├── test_orchestration.py
│   │       │   ├── test_service_coordination.py
│   │       │   ├── test_error_handling.py
│   │       │   └── test_project_isolation.py
│   │       └── README.md
│   ├── content-management-service/ # GMC Manual versioning with MongoDB
│   │   ├── app/
│   │   │   ├── __init__.py
│   │   │   ├── main.py         # Flask application entry point
│   │   │   ├── models/         # MongoDB document schemas
│   │   │   ├── routes/         # Content management APIs
│   │   │   ├── services/       # Document parsing and versioning
│   │   │   ├── parsers/        # GMC Manual content extraction
│   │   │   └── config.py       # MongoDB configuration
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   ├── tests/
│   │   └── README.md
│   ├── user-management-service/    # Authentication and API key management
│   │   ├── app/
│   │   │   ├── __init__.py
│   │   │   ├── main.py         # Flask application entry point
│   │   │   ├── models/         # PostgreSQL user and credential models
│   │   │   ├── routes/         # Authentication and user management APIs
│   │   │   ├── services/       # Encryption, FERPA compliance, audit trails
│   │   │   ├── security/       # AES-256-GCM encryption utilities
│   │   │   └── config.py       # Security and database configuration
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   ├── tests/
│   │   └── README.md
│   ├── analytics-service/          # Educational analytics with PostgreSQL + ClickHouse
│   │   ├── app/
│   │   │   ├── __init__.py
│   │   │   ├── main.py         # Flask application entry point
│   │   │   ├── models/         # PostgreSQL analytics models
│   │   │   ├── routes/         # Analytics and faculty dashboard APIs
│   │   │   ├── services/       # Competency tracking and reporting
│   │   │   ├── clickhouse/     # Time-series event processing
│   │   │   └── config.py       # Multi-database analytics configuration
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   ├── tests/
│   │   └── README.md
│   └── notification-service/       # Real-time collaboration with Redis
│       ├── app/
│       │   ├── __init__.py
│       │   ├── main.py         # Flask application entry point
│       │   ├── routes/         # WebSocket and notification APIs
│       │   ├── services/       # Real-time event broadcasting
│       │   ├── websocket/      # WebSocket connection management
│       │   └── config.py       # Redis and WebSocket configuration
│       ├── Dockerfile
│       ├── requirements.txt
│       ├── tests/
│       └── README.md
├── frontend/               # React SPA with Dash integration
│   ├── public/
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── pages/         # Page-level components
│   │   ├── services/      # API integration and service calls
│   │   ├── hooks/         # Custom React hooks
│   │   ├── utils/         # Frontend utilities
│   │   ├── dash/          # Dash Plotly integration components
│   │   └── assets/        # Static assets and Team Unicorn branding
│   ├── package.json
│   ├── Dockerfile
│   ├── Dockerfile.dev
│   └── README.md
├── shared/                 # Shared libraries and utilities
│   ├── python/            # Shared Python libraries
│   │   ├── auth/          # Service authentication utilities
│   │   ├── events/        # Event sourcing and messaging patterns
│   │   ├── monitoring/    # Health checks and metrics collection
│   │   ├── database/      # Database connection utilities
│   │   └── security/      # Encryption and security utilities
│   └── schemas/           # Shared data schemas and validation
│       ├── events/        # Event schemas for service communication
│       ├── api/           # API request/response schemas
│       └── database/      # Database schema definitions
├── infrastructure/        # Infrastructure as Code and deployment
│   ├── k8s/               # Kubernetes manifests
│   │   ├── databases/     # Database StatefulSets and Services
│   │   ├── services/      # Application service Deployments
│   │   ├── gateway/       # API Gateway and Ingress configurations
│   │   ├── monitoring/    # Prometheus, Grafana, Jaeger
│   │   └── secrets/       # Secret and ConfigMap templates
│   ├── docker-compose/    # Development environment compositions
│   │   ├── docker-compose.yml         # Full development stack
│   │   ├── docker-compose.minimal.yml # Minimal testing stack
│   │   └── docker-compose.prod.yml    # Production-like local testing
│   ├── helm/              # Helm charts for production deployment
│   │   ├── gmc-dashboard/ # Main application chart
│   │   └── dependencies/  # Database and infrastructure charts
│   ├── terraform/         # Cloud infrastructure provisioning
│   │   ├── aws/          # AWS-specific resources
│   │   ├── azure/        # Azure-specific resources
│   │   └── gcp/          # Google Cloud-specific resources
│   └── scripts/          # Deployment and maintenance scripts
│       ├── dev-setup.sh         # Development environment setup
│       ├── production-deploy.sh # Production deployment script
│       ├── database-migrations.sh # Database migration management
│       └── service-health-check.sh # Service health validation
├── tests/                  # Cross-service integration tests
│   ├── integration/       # Service-to-service integration tests
│   ├── e2e/              # End-to-end user workflow tests
│   ├── performance/      # Load testing and performance validation
│   ├── security/         # Security and penetration testing
│   └── fixtures/         # Test data and mock services
├── docs/                   # Technical documentation
│   ├── README.md           # Project overview and quick start
│   ├── INSTALL.md          # Installation and configuration guide
│   ├── SETUP.md            # AI infrastructure setup guide
│   ├── API.md              # API documentation and service contracts
│   ├── DEPLOYMENT.md       # Deployment guide for different environments
│   ├── MONITORING.md       # Monitoring and observability guide
│   ├── SECURITY.md         # Security architecture and compliance
│   └── TROUBLESHOOTING.md  # Common issues and resolution guide
├── config/                 # Environment-specific configurations
│   ├── development/       # Development environment config
│   ├── staging/           # Staging environment config
│   ├── production/        # Production environment config
│   └── local/             # Local development overrides
├── .github/                # CI/CD workflows and templates
│   ├── workflows/         # GitHub Actions workflows
│   ├── ISSUE_TEMPLATE/    # Issue templates
│   └── PULL_REQUEST_TEMPLATE.md
├── database/               # Database schemas and migrations
│   ├── migrations/        # Database migration scripts
│   │   ├── postgresql/    # PostgreSQL migrations for all services
│   │   ├── neo4j/         # Neo4j schema and constraint scripts
│   │   └── mongodb/       # MongoDB collection and index scripts
│   └── seeds/             # Seed data for development and testing
└── monitoring/             # Monitoring and observability configurations
    ├── prometheus/        # Prometheus configuration and rules
    ├── grafana/          # Grafana dashboards and data sources
    ├── jaeger/           # Distributed tracing configuration
    └── alerts/           # Alerting rules and notification configs
```

## Architectural Governance Model (FR27)

The GMC Dashboard implements comprehensive project structure synchronization requirements per FR27, ensuring consistency across development teams and automated deployment processes.

### Core Governance Principles

**1. Architectural Control:**
- **Core Directory Structure:** Defined by architecture team with established organizational patterns
- **Developer Flexibility:** Developers may create subdirectories following established patterns
- **Code Review Validation:** All subdirectory creation subject to code review to prevent conflicts
- **Pattern Consistency:** Architectural pattern changes require architect approval

**2. Documentation Synchronization:**
- **Mandatory Updates:** All changes to core directory structure must be documented in `architecture.md`
- **Specification Accuracy:** Architecture documentation must reflect actual implementation
- **Development Consistency:** Architectural governance ensures alignment across teams
- **Automated Validation:** CI/CD processes validate structure-documentation alignment

**3. intelligence Directory Governance:**
- **Infrastructure Standards:** Complete `intelligence` directory structure defined by architecture team
- **Developer Guidelines:** Established patterns for AI component organization
- **Validation Process:** Code review ensures `intelligence` modifications follow architectural standards
- **Documentation Requirements:** All `intelligence` changes require corresponding architecture updates

### Governance Workflow

**Development Phase Setup:**
1. **Pattern Definition:** Architecture team establishes core organizational patterns
2. **Developer Onboarding:** Team training on established patterns and approval processes
3. **Validation Integration:** Code review processes include architectural compliance checks
4. **Continuous Monitoring:** Regular audits ensure ongoing compliance and pattern adherence

**Change Management Process:**
1. **Pattern Modification Requests:** Developers propose changes through architecture review
2. **Impact Assessment:** Evaluation of proposed changes on overall system consistency
3. **Documentation Updates:** Required architecture.md updates for approved changes
4. **Implementation Coordination:** Synchronized rollout across development teams

**Quality Assurance:**
- **Structure Validation:** Automated checks for directory structure compliance
- **Documentation Sync:** CI/CD validation of architecture documentation accuracy
- **Pattern Enforcement:** Code review gates prevent non-compliant structural changes
- **Audit Processes:** Regular review of architectural governance effectiveness

## Architecture Diagram

```mermaid
graph TB
    subgraph "Client Layer"
        WEB[React SPA Frontend]
        MOBILE[Mobile App - Future]
    end
    
    subgraph "API Gateway & Load Balancer"
        GATEWAY[Kong API Gateway]
        LB[Load Balancer]
    end
    
    subgraph "Microservices Layer"
        subgraph "Core Business Services"
            CALC_SVC[GMC Calculation Service]
            KNOWLEDGE_SVC[Knowledge Graph Service]
            COACHING_SVC[AI Coaching Service]
            CONTENT_SVC[Content Management Service]
            USER_SVC[User Management Service]
            ANALYTICS_SVC[Analytics Service]
            NOTIFY_SVC[Notification Service]
        end
        
        subgraph "Supporting Services"
            AUTH_SVC[Authentication Service]
            FILE_SVC[File Processing Service]
            AUDIT_SVC[Audit & Compliance Service]
        end
    end
    
    subgraph "Database-per-Service"
        PG_CALC[(PostgreSQL - Calculations)]
        PG_USER[(PostgreSQL - Users)]
        PG_ANALYTICS[(PostgreSQL - Analytics)]
        NEO4J[(Neo4j - Knowledge Graph)]
        WEAVIATE[(Weaviate - Vector Search)]
        MONGODB[(MongoDB - Content)]
        REDIS[(Redis - Cache & Sessions)]
        CLICKHOUSE[(ClickHouse - Analytics)]
    end
    
    subgraph "External Services"
        ANTHROPIC[Anthropic API]
        OPENROUTER[OpenRouter API]
        OLLAMA[Local Ollama]
        EXCEL_FILES[Excel Files]
        GMC_MANUAL[GMC Manual Content]
    end
    
    subgraph "Infrastructure Services"
        MONITORING[Prometheus/Grafana]
        LOGGING[ELK Stack]
        TRACING[Jaeger]
        SERVICE_MESH[Istio Service Mesh]
    end
    
    subgraph "Orchestration"
        K8S[Kubernetes Cluster]
        HELM[Helm Charts]
        CICD[CI/CD Pipeline]
    end
    
    %% Client connections
    WEB --> GATEWAY
    MOBILE --> GATEWAY
    
    %% Gateway routing
    GATEWAY --> LB
    LB --> CALC_SVC
    LB --> KNOWLEDGE_SVC
    LB --> COACHING_SVC
    LB --> CONTENT_SVC
    LB --> USER_SVC
    LB --> ANALYTICS_SVC
    LB --> NOTIFY_SVC
    
    %% Service-to-Database mappings
    CALC_SVC --> PG_CALC
    USER_SVC --> PG_USER
    ANALYTICS_SVC --> PG_ANALYTICS
    ANALYTICS_SVC --> CLICKHOUSE
    KNOWLEDGE_SVC --> NEO4J
    COACHING_SVC --> WEAVIATE
    COACHING_SVC --> MONGODB
    CONTENT_SVC --> MONGODB
    NOTIFY_SVC --> REDIS
    
    %% Inter-service communication through service mesh
    CALC_SVC -.->|Service Mesh| KNOWLEDGE_SVC
    CALC_SVC -.->|Service Mesh| USER_SVC
    COACHING_SVC -.->|Service Mesh| KNOWLEDGE_SVC
    COACHING_SVC -.->|Service Mesh| USER_SVC
    ANALYTICS_SVC -.->|Service Mesh| CALC_SVC
    ANALYTICS_SVC -.->|Service Mesh| USER_SVC
    
    %% External service connections
    COACHING_SVC --> ANTHROPIC
    COACHING_SVC --> OPENROUTER
    COACHING_SVC --> OLLAMA
    CALC_SVC --> EXCEL_FILES
    CONTENT_SVC --> GMC_MANUAL
    
    %% Infrastructure monitoring
    SERVICE_MESH --> MONITORING
    SERVICE_MESH --> LOGGING
    SERVICE_MESH --> TRACING
    
    %% Orchestration
    K8S --> CALC_SVC
    K8S --> KNOWLEDGE_SVC
    K8S --> COACHING_SVC
    K8S --> CONTENT_SVC
    K8S --> USER_SVC
    K8S --> ANALYTICS_SVC
    K8S --> NOTIFY_SVC
```
    
    AC --> PWA
    AUTH --> API
    LMS --> API
    COMPLIANCE --> API
    
    U1 --> PWA
    U2 --> PWA
    U3 --> PWA
    U4 --> PWA
    
    PWA --> UI
    PWA --> DASH
    PWA --> LOCAL
    PWA --> WASM
    PWA --> OFFLINE
    
    UI --> API
    DASH --> API
    LOCAL --> API
    WASM --> ENGINE
    
    API --> ENGINE
    API --> INVESTPERF
    API --> STRATAI
    API --> BUILDBLOCK
    API --> COMPINTEL
    API --> PARSER
    API --> COLLAB
    API --> VALID
    
    INVESTPERF --> ENGINE
    STRATAI --> INVESTPERF
    BUILDBLOCK --> ENGINE
    COMPINTEL --> INVESTPERF
    
    ENGINE --> PG
    ENGINE --> CACHE
    INVESTPERF --> PG
    INVESTPERF --> CACHE
    STRATAI --> PG
    STRATAI --> CACHE
    BUILDBLOCK --> FILES
    COMPINTEL --> PG
    PARSER --> FILES
    COLLAB --> PG
    VALID --> CACHE
    
    EXCEL --> PARSER
    CLOUD --> BACKUP
    MONITOR --> ANALYTICS
    BACKUP --> FILES
```

## MVP Architectural Patterns

**Cloud-Native Progressive Web App:** React frontend with service worker for basic offline functionality, Kubernetes deployment with Flask microservices backend. *Rationale: Scalable microservices architecture with professional reliability and service isolation.*

**Excel Compatibility with Single Library:** openpyxl for Excel parsing with comprehensive validation. *Rationale: Proven library with extensive GMC testing, eliminates multi-library complexity.*

**Real-time Collaboration:** Flask-SocketIO with Redis for live updates during team analysis. *Rationale: Essential for team coordination, built-in conflict resolution, integrates with microservices architecture.*

**Basic AI Integration:** User-managed API keys for personalized AI recommendations. *Rationale: Delivers AI value without complex infrastructure.*

**FERPA Compliance:** PostgreSQL row-level security with audit trails. *Rationale: Educational compliance with manageable complexity.*

**Team Unicorn Branding Integration:** Professional co-branding with Team Unicorn purple (#8B5CF6) accents and sophisticated animations for optimization achievements. *Rationale: Front-end spec requirement for educational technology excellence.*

# MVP Tech Stack

Simplified technology selection focused on rapid MVP delivery with clear expansion pathways.

## Core Technologies

| Category | Technology | Version | Purpose | Rationale |
|----------|------------|---------|---------|-------------------|
| **Frontend Language** | TypeScript | 5.3+ | Type-safe development | IDE support, fewer runtime errors |
| **Primary UI Framework** | React.js | 18.2+ | Modern reactive UI development | Component-based architecture, rich ecosystem |
| **Mathematical Visualization** | Dash Plotly | 2.16+ | Real-time mathematical charts and GMC analysis dashboards | Excel-equivalent mathematical precision, purpose-built for analytical applications |
| **Graph Integration** | Dash Components in React | 2.16+ | Embedded Dash graphs within React components | Seamless integration of Python-generated plots in React frontend |
| **Frontend Graph Rendering** | Plotly.js | 2.26+ | Interactive graph rendering in browser | Client-side graph interactivity, zoom, pan, hover effects |
| **UI Components** | Tailwind CSS + Headless UI | 3.4+ / 1.7+ | Styling and accessible components | WCAG 2.1 AA compliance, Team Unicorn branding |
| **Typography** | Inter + JetBrains Mono + Outfit | Latest | Font families per front-end spec | Inter (primary), JetBrains Mono (performance), Outfit (Team Unicorn) |
| **State Management** | Zustand + React Query | 4.4+ / 5.0+ | Client state and server synchronization | Simple state, built-in caching |
| **Build Tools** | Vite | 5.0+ | Fast development build system | Hot module replacement, optimized bundling |
| **Frontend Package Manager** | npm | 10.2+ | JavaScript/TypeScript dependency management | React ecosystem, frontend build tools |
| **Backend Language** | Python | 3.12+ | Mathematical calculations and microservices | Excel integration, AI/ML ecosystem |
| **Microservices Framework** | Flask | 2.3+ | Lightweight web framework for services | Microservices architecture, educational applications |
| **Graph Generation Backend** | Dash Plotly (Backend) | 2.16+ | Server-side graph generation and mathematical visualization | Python-based plotting for GMC calculations, integrates with React frontend |
| **Python Package Manager** | uv | 0.1+ | Modern Python dependency management | Fast dependency resolution, secure package management |

## **Database Technologies (Database-per-Service Pattern)**

| Category | Technology | Version | Purpose | Rationale |
|----------|------------|---------|---------|-------------------|
| **Transactional Database** | PostgreSQL | 15+ | ACID transactions for calculations and users | Complex GMC data relationships, JSON support, row-level security |
| **Knowledge Graph** | Neo4j Community Edition | 5.x | GMC rule relationships and causal reasoning | Complex interdependency traversal and strategy logic |
| **Vector Database** | Weaviate | 1.2x | Semantic search over GMC Manual and strategies | Context-aware query and similarity matching |
| **Document Storage** | MongoDB | 7.x | GMC Manual knowledge base and AI profiles | Version-controlled content, flexible schemas |
| **Analytics Database** | ClickHouse | 23.x+ | Time-series educational analytics | High-performance analytical queries, event data |
| **Cache & Message Queue** | Redis | 7.2+ | Session state, real-time collaboration, events | Sub-second performance, pub/sub messaging |
| **ORM & Database Tools** | SQLAlchemy + Alembic | 2.0+ / 1.13+ | Data modeling, migrations, relationships | Multi-database coordination, schema evolution |

## **AI & Machine Learning Stack**

| Category | Technology | Version | Purpose | Rationale |
|----------|------------|---------|---------|-------------------|
| **LLM APIs** | OpenAI + Anthropic + Gemini + DeepSeek + OpenRouter + Ollama | GPT-4+ / Claude-3+ / Gemini-Pro+ / DeepSeek-Coder+ | Individual user API key management with multi-provider support and budget controls | Per-user encrypted credential storage per FR25 with provider selection |
| **Local AI** | Ollama | Latest | Privacy-focused local AI deployment | Complete data privacy, no external API costs |
| **Conversational AI** | Rasa | 3.x | Persistent AI Coach chatbot interface per FR34 | Natural language strategy communication with memory |
| **Classical ML** | CatBoost + XGBoost + Scikit-learn | 1.x / 2.x / 1.4+ | Parameter optimization and sensitivity analysis | Investment performance prediction with LLM orchestration |
| **Mathematical Processing** | NumPy + Pandas | 1.26+ / 2.1+ | Precise financial calculations | Excel-equivalent mathematical accuracy |
| **NLP Processing** | spaCy | 3.x | Text processing and entity extraction | GMC Manual parsing and conversational analysis |
| **Graph Analysis** | NetworkX | 3.x | Knowledge graph building and manipulation | Python-based graph analysis for AI reasoning |
| **ML Orchestration** | MLflow + Airflow | 2.x / 2.x | Model lifecycle and AI pipeline automation | Experiment tracking and intelligent model coordination |

## **Infrastructure & Deployment Stack**

| Category | Technology | Version | Purpose | Rationale |
|----------|------------|---------|---------|-------------------|
| **Container Runtime** | Docker + Docker Compose | 24+ / 2.23+ | Microservices containerization | Consistent deployment across environments |
| **Container Orchestration** | Kubernetes + Helm | 1.28+ / 3.12+ | Production container management | Auto-scaling, service discovery, resource management |
| **API Gateway** | Kong | 3.0+ | Service routing, authentication, rate limiting | Microservices ingress, JWT authentication, API versioning |
| **Service Mesh** | Istio | 1.19+ | Service-to-service communication and observability | Traffic management, security, distributed tracing |
| **Infrastructure as Code** | Terraform | 1.6+ | Cloud infrastructure provisioning | Multi-cloud deployment, infrastructure versioning |
| **CI/CD Pipeline** | GitHub Actions | Latest | Automated testing and deployment | Free for educational use, excellent ecosystem integration |

## **Monitoring & Observability Stack**

| Category | Technology | Version | Purpose | Rationale |
|----------|------------|---------|---------|-------------------|
| **Metrics Collection** | Prometheus + Grafana | 2.45+ / 10.0+ | Metrics monitoring and visualization | Industry standard, rich ecosystem |
| **Distributed Tracing** | Jaeger | 1.49+ | Request tracing across microservices | Performance debugging, service dependency visualization |
| **Log Aggregation** | ELK Stack (Elasticsearch, Logstash, Kibana) | 8.x | Centralized logging and search | Structured logging, compliance audit trails |
| **Error Tracking** | Sentry | 7.80+ | Error monitoring and alerting | Educational privacy protection, performance optimization |
| **APM** | Prometheus + Custom Metrics | 2.45+ | Application performance monitoring | Custom educational metrics, FERPA-compliant analytics |

## **Security & Compliance Stack**

| Category | Technology | Version | Purpose | Rationale |
|----------|------------|---------|---------|-------------------|
| **Authentication** | JWT + OAuth 2.0 | Latest | User and service authentication | Stateless authentication, service-to-service security |
| **Encryption** | AES-256-GCM | Latest | Data encryption at rest and transit | FERPA compliance, API key protection |
| **Secret Management** | Kubernetes Secrets + External Secrets Operator | 1.28+ / 0.9+ | Secure configuration management | Encrypted secret storage, external vault integration |
| **Network Security** | TLS 1.3 + mTLS | Latest | Secure communication | End-to-end encryption, service mesh security |

## **Excel Integration Stack**

| Category | Technology | Version | Purpose | Rationale |
|----------|------------|---------|---------|-------------------|
| **Primary Excel Parser** | openpyxl | 3.1+ | Excel file parsing and manipulation | Proven library, GMC compatibility, pure Python |
| **Advanced Excel Integration** | xlwings | 0.31+ | Complex Excel features and COM automation | Advanced formulas, chart integration, Windows compatibility |
| **Formula Processing** | Custom Python Engine | Latest | Excel formula translation to Python | 100% mathematical accuracy, validation framework |

## **Development & Testing Stack**

| Category | Technology | Version | Purpose | Rationale |
|----------|------------|---------|---------|-------------------|
| **Frontend Testing** | Vitest + React Testing Library | 1.0+ / 13.4+ | Component and unit testing | Fast testing, React-specific utilities |
| **Backend Testing** | pytest + Coverage.py | 7.4+ / 7.3+ | Python service testing | Comprehensive test framework, coverage reporting |
| **E2E Testing** | Playwright | 1.40+ | Cross-browser end-to-end testing | Multi-browser support, academic environment testing |
| **Load Testing** | Locust + K6 | 2.17+ / 0.47+ | Performance and load testing | Educational concurrency testing, API stress testing |
| **API Testing** | HTTPx + Postman Collections | 0.25+ | API contract and integration testing | Async HTTP client, automated API validation |

## Post-MVP Expansion Technologies

- **Advanced AI:** Local Ollama deployment, vector databases
- **Analytics:** Educational analytics dashboard for faculty
- **Multi-tenant:** Institution management and SSO integration
- **Mobile:** React Native app for enhanced mobile experience
| **Local Storage** | IndexedDB + Dexie.js | - / 3.2+ | Offline-first local persistence with quota management | Browser-native offline storage, Dexie provides SQL-like queries, automatic quota management for academic constraints |
| **File Storage** | MinIO + PostgreSQL | - | Multi-region file storage with academic compliance | FERPA-compliant file handling, automatic backup, supports international data residency requirements |
| **Authentication** | Flask-Login + SAML | 0.6+ | Campus SSO integration with guest access support | Educational SSO compatibility, LDAP integration, supports diverse campus authentication systems |
| **Real-time Collaboration** | Flask-SocketIO + Y.js | - / 13.6+ | CRDT-based collaborative editing with conflict resolution | Essential for team-based GMC analysis; includes polling fallback for restricted academic networks; abstraction layer enables future self-hosted migration |
| **Frontend Testing** | Vitest + React Testing Library | 1.0+ / 13.4+ | Fast testing optimized for educational component patterns | Vite-native testing, educational accessibility testing support, component behavior validation |
| **Backend Testing** | pytest + Flask-Testing | 7.4+ / 1.0+ | Comprehensive API testing with Excel calculation validation | Mathematical accuracy testing, Flask app testing, educational compliance validation |
| **E2E Testing** | Playwright | 1.40+ | Cross-browser testing for diverse academic environments | Academic browser compatibility, accessibility testing, real user workflow validation |
| **Package Manager** | npm + uv | 10.2+ / 0.1.0+ | Hybrid JavaScript/Python dependency management | npm for frontend ecosystem, uv for modern Python packaging, monorepo workspace support |
| **Bundler** | Vite + Rollup | 5.0+ / 4.0+ | Optimized bundling with academic performance targets | Tree shaking for smaller bundles, code splitting for academic bandwidth, educational-friendly error handling |
| **Container Runtime** | Docker + Docker Compose | 24+ / 2.23+ | Consistent deployment across diverse academic infrastructure | Academic IT compatibility, simple deployment for resource-constrained institutions |
| **IaC Tool** | Docker Compose + Terraform | 2.23+ / 1.6+ | Infrastructure as code with academic deployment flexibility | Simple Docker Compose for basic deployment, Terraform for advanced institutional integration |
| **CI/CD** | GitHub Actions | - | Automated testing and deployment with educational validation cycles | Free for educational use, excellent ecosystem integration, academic compliance checking |
| **Monitoring** | Prometheus + Grafana + Sentry | - / 7.80+ | Performance monitoring with educational privacy protection | Academic-appropriate analytics, error tracking with student privacy protection, microservices observability |
| **Logging** | Winston + Structured Logs | 3.11+ | Educational audit trails with compliance export | Academic audit requirements, structured logging for compliance reporting, FERPA-compliant log management |
| **Progressive Web App** | Workbox | 7.0+ | Offline-first service worker with academic resilience | Critical for academic network reliability; extensive academic environment testing required; graceful degradation for limited browsers |

## Critical Implementation Notes

**Academic Network Resilience:**
- **Network Fallback Strategy:** WebSocket with intelligent polling fallback for restrictive campus firewalls
- **Browser Compatibility Matrix:** Tested compatibility with academic computer lab constraints (Chrome 90+, Firefox 88+, Safari 14+)
- **Connection Recovery:** Automatic reconnection with exponential backoff optimized for academic network patterns

**Vendor Dependency Management:**
- **Abstraction Layers:** Clean separation between microservices and core application logic enabling scalable deployment paths
- **Self-Hosted Alternatives:** Docker-based deployment option using PostgreSQL + PostgREST + self-managed auth
- **Migration Documentation:** Clear paths from cloud services to institutional self-hosting

**Technology Decision Confidence Level:**
- **High Confidence (>95%):** Python for calculations and Excel integration (unique strengths outweigh complexity)
- **Validated Approach:** Hybrid stack complexity is industry-acceptable for data applications
- **Future Flexibility:** Architecture designed for potential TypeScript migration without fundamental redesign

# AI Development Infrastructure: `intelligence` Directory

## Overview

The `intelligence` directory provides standardized infrastructure for AI-powered features including individual user API key management, classical ML models, LLM prompt engineering, and multi-deployment AI configurations. This structure supports Epic 6 requirements for personalized AI-enhanced GMC strategy optimization.

## Complete Directory Structure

```
intelligence/
├── api-configs/                 # AI service configuration files
│   ├── openai.yaml             # OpenAI GPT-4/GPT-3.5 API configuration and templates
│   ├── anthropic.yaml          # Anthropic Claude-3/Claude-2 API configuration and templates
│   ├── gemini.yaml             # Google Gemini Pro API configuration and templates
│   ├── deepseek.yaml           # DeepSeek Coder API configuration and templates
│   ├── openrouter.yaml         # OpenRouter multi-model routing configuration
│   ├── ollama.yaml             # Local Ollama deployment settings and model management
│   ├── provider-mapping.yaml   # LLM provider capability mapping and fallback strategies
│   └── provider-defaults.yaml  # Default provider settings and fallback configurations
│   # NOTE: User API keys stored in PostgreSQL with AES-256-GCM encryption per FR25
├── classical-ml-models/         # Traditional ML model storage
│   ├── catboost-models/        # Gradient boosting for investment performance
│   ├── xgboost-models/         # Parameter sensitivity analysis models
│   └── scikit-models/          # Supporting ML algorithms
├── llm-prompts/                 # Structured prompt libraries
│   ├── strategy-optimization/   # Investment performance optimization prompts
│   ├── formula-analysis/        # GMC calculation explanation prompts
│   └── competitive-intel/       # Anonymous benchmarking analysis prompts
├── deployment-configs/          # Multi-environment AI deployment
│   ├── local-ollama/           # Local privacy-preserving deployment
│   ├── cloud-api/              # Cloud-based API integration
│   └── hybrid/                 # Mixed local/cloud deployment
├── training-data/               # ML training and validation datasets
│   ├── gmc-historical-samples/ # Historical GMC performance data
│   ├── synthetic-scenarios/     # Generated training scenarios
│   └── validation-datasets/     # Model accuracy validation data
├── agent-configs/               # AI agent configuration files
│   ├── strategy-tuning-agent.yaml      # Investment optimization agent
│   ├── building-block-agent.yaml       # Formula transparency agent
│   └── competitive-intel-agent.yaml    # Benchmarking analysis agent
├── prompts/                     # Legacy prompt directory (backward compatibility)
├── models/                      # Legacy model directory (backward compatibility)
├── debug-log.md                # AI development debugging and tracking
└── SETUP_GUIDE.md              # Comprehensive installation and configuration guide
```

## AI Integration Components

### Individual User API Key Management
- **Encrypted Storage:** PostgreSQL with AES-256-GCM encryption
- **Budget Controls:** Daily ($10) and monthly ($300) limits per user
- **Service Support:** Anthropic Pro, OpenRouter, local Ollama fallback
- **FERPA Compliance:** Institution-level data boundaries with audit trails

### Knowledge Graph + RAG Architecture
- **Vector Database:** Weaviate for semantic search over GMC Manual content
- **Graph Database:** Neo4j for relationship reasoning between GMC concepts
- **LLM Orchestration:** Intelligent coordination of classical models with strategic reasoning
- **GMC Manual Integration:** Automated parsing and knowledge base updates

### Conversational AI Coach System
- **Framework:** Rasa for natural language strategy communication
- **Persistent Learning:** User-specific strategy profiles and decision pattern analysis
- **Task Delegation:** AI assistant capabilities for strategic analysis automation
- **Educational Integration:** GMC rule explanations and constraint guidance

## Documentation Synchronization

All `intelligence` directory changes must be documented in `architecture.md` to ensure consistency across development teams and automated deployment processes (FR27 compliance).

# Testing Strategy

## Comprehensive Testing Framework (PRD-Required)

**Unit Tests:** Individual formula calculations validated against Excel reference data
- Mathematical accuracy testing for all GMC calculation engines
- Investment performance calculation validation
- Parameter sensitivity analysis verification

**Integration Tests:** Cross-sheet dependency validation ensuring proper calculation propagation
- Real-time collaboration testing with Redis state management
- Database integrity testing with SQLAlchemy models
- AI integration testing with external API services

**Validation Tests:** Complete GMC scenarios tested against reference datasets
- Excel equivalence validation using `/overview/gmc_history_sample/` data
- Historical baseline calculations accuracy verification
- Constraint validation and error handling testing

**Performance Tests:** Load testing for academic environment requirements
- 50+ concurrent users performance validation
- Sub-2 second response time verification
- Parameter sensitivity analysis <1 second response testing
- AI recommendation generation <2 seconds validation

**UI Tests:** Educational interface and workflow validation
- Constraint validation and error recovery workflows
- Team Unicorn branding integration testing
- Accessibility compliance (WCAG 2.1 AA) validation
- Multi-device responsive design testing

# Data Models

Simplified data models focused on core MVP functionality with expansion capabilities.

# **Epic 0: Project Management Foundation Architecture** 🚀

**Revolutionary Multi-Project System:** Complete architectural transformation enabling multiple independent GMC analysis projects with comprehensive data isolation, timeline independence, and strategic experimentation capabilities.

## Project Entity (Primary Architecture Foundation)

**Purpose:** Core entity enabling multiple independent GMC analysis projects with complete data isolation

**Key Attributes:**
- `project_id`: string - Unique project identifier (UUID)
- `project_name`: string - User-defined project name (duplicates allowed for strategy experimentation)
- `project_description`: string - Optional project description for organization
- `user_id`: string - Project owner (creator)
- `team_members`: string[] - Collaborating user IDs with project access
- `project_type`: 'individual' | 'team_collaboration' | 'competitive_intelligence' - Project analysis mode
- `project_template`: 'blank' | 'standard_gmc' | 'advanced_multi_scenario' - Initial setup template
- `data_isolation_boundary`: object - Complete boundary configuration for project data separation
- `timeline_independence`: object - Project-specific timeline and historical data management
- `strategic_context`: object - Project-specific strategy goals and experimentation parameters
- `is_active`: boolean - Project status
- `created_at`: Date - Project creation timestamp
- `updated_at`: Date - Last project modification
- `last_accessed_at`: Date - Most recent project access for organization

### TypeScript Interface
```typescript
interface Project {
  project_id: string;
  project_name: string;
  project_description?: string;
  user_id: string;
  team_members: string[];
  project_type: 'individual' | 'team_collaboration' | 'competitive_intelligence';
  project_template: 'blank' | 'standard_gmc' | 'advanced_multi_scenario';
  data_isolation_boundary: DataIsolationConfig;
  timeline_independence: TimelineConfig;
  strategic_context: StrategicContext;
  is_active: boolean;
  created_at: Date;
  updated_at: Date;
  last_accessed_at: Date;
}

interface DataIsolationConfig {
  ai_coaching_context_id: string;     // Separate AI coaching per project
  competitive_intel_scope_id: string; // Independent competitive analysis
  file_management_scope_id: string;   // Project-specific file organization
  calculation_namespace: string;      // Isolated calculation contexts
}

interface TimelineConfig {
  independent_file_timeline: boolean;
  project_specific_quarters: string[];
  historical_data_isolation: boolean;
  cross_project_contamination_prevention: boolean;
}

interface StrategicContext {
  strategy_experimentation_goals: string[];
  competitive_analysis_focus: string[];
  risk_tolerance_override?: 'conservative' | 'moderate' | 'aggressive';
  optimization_priorities: string[];
}
```

## Company/Team Entity (Enhanced for Multi-Project)

**Purpose:** Represents a GMC simulation team within specific project contexts

**Key Attributes:**
- `company_id`: string - Team identifier (Company 1, Company 2, etc.)
- `project_id`: string - **PROJECT SCOPING** - Associated project context
- `name`: string - Team display name within project
- `members`: string[] - Team member user IDs
- `current_quarter`: string - Active analysis period (Y16Q1, etc.)
- `project_role_permissions`: object - Project-specific team member permissions
- `created_at`: Date - Creation timestamp
- `updated_at`: Date - Last modification

### TypeScript Interface
```typescript
interface Company {
  company_id: string;
  project_id: string; // **PROJECT SCOPING KEY**
  name: string;
  members: string[];
  current_quarter: string;
  project_role_permissions: ProjectRolePermissions;
  created_at: Date;
  updated_at: Date;
}

interface ProjectRolePermissions {
  [user_id: string]: {
    can_edit_parameters: boolean;
    can_manage_files: boolean;
    can_access_ai_coaching: boolean;
    can_view_competitive_intel: boolean;
  };
}
```

## GMC Report Entity (Enhanced for Project-Scoped File Management)

**Purpose:** Represents uploaded GMC quarterly reports with project-scoped data isolation and timeline independence

**Key Attributes:**
- `report_id`: string - Unique identifier
- `project_id`: string - **PROJECT SCOPING** - Associated project for complete data isolation
- `company_id`: string - Associated team within project context
- `report_type`: 'history' | 'game' - File type recognition
- `quarter_period`: string - Quarter identifier (Y16Q1, etc.)
- `filename`: string - Original uploaded filename
- `data`: object - Parsed Excel data (isolated per project)
- `is_valid`: boolean - Basic validation status
- `project_timeline_position`: number - Position in project-specific timeline
- `cross_project_isolation_verified`: boolean - Ensures no data leakage between projects
- `created_at`: Date - Upload timestamp
- `updated_at`: Date - Last modification timestamp

### TypeScript Interface
```typescript
interface GMCReport {
  report_id: string;
  project_id: string; // **PROJECT SCOPING KEY**
  company_id: string;
  report_type: 'history' | 'game';
  quarter_period: string;
  filename: string;
  data: any;
  is_valid: boolean;
  project_timeline_position: number;
  cross_project_isolation_verified: boolean;
  created_at: Date;
  updated_at: Date;
}
```

## Analysis Session Entity (Enhanced for Project-Scoped Analysis Context)

**Purpose:** Represents active GMC analysis workspace with project-scoped collaboration and state isolation

**Key Attributes:**
- `session_id`: string - Unique session identifier
- `project_id`: string - **PROJECT SCOPING** - Parent project context for complete isolation
- `company_id`: string - Associated team within project
- `session_name`: string - User-defined name
- `base_report_id`: string - Source GMC report (project-scoped)
- `decision_parameters`: object - Current GMC parameter values (project-isolated)
- `calculated_results`: object - Real-time calculated metrics (project-isolated)
- `project_analysis_context`: object - Project-specific analysis state and preferences
- `cross_session_isolation_boundary`: object - Prevents contamination between project sessions
- `is_active`: boolean - Session status
- `created_at`: Date - Creation timestamp
- `updated_at`: Date - Last modification

### TypeScript Interface
```typescript
interface AnalysisSession {
  session_id: string;
  project_id: string; // **PROJECT SCOPING KEY**
  company_id: string;
  session_name: string;
  base_report_id: string;
  decision_parameters: any;
  calculated_results: any;
  project_analysis_context: ProjectAnalysisContext;
  cross_session_isolation_boundary: SessionIsolationConfig;
  is_active: boolean;
  created_at: Date;
  updated_at: Date;
}

interface ProjectAnalysisContext {
  strategy_experimentation_mode: boolean;
  competitive_focus_areas: string[];
  ai_coaching_preferences: object;
  calculation_namespace: string;
}

interface SessionIsolationConfig {
  isolated_calculation_state: boolean;
  project_scoped_undo_redo: boolean;
  cross_project_contamination_prevention: boolean;
}
  is_calculation_dirty: boolean;
  // Academic workflow fields
  submission_status: 'draft' | 'submitted' | 'graded';
  instructor_feedback?: string;
}

interface AcademicContext {
  assignment_id?: string;
  due_date?: Date;
  learning_objectives: string[];
  assessment_criteria: AssessmentCriteria[];
  grade_weight: number;
  academic_integrity_hash: string; // For plagiarism detection
}
```

## Parameter Change Entity (Academic Integrity & Performance Optimized)

**Purpose:** Complete audit trail of decision parameter modifications with academic integrity attribution, undo/redo functionality, and learning analytics integration

**Key Attributes (Enhanced Academic Focus):**
- `change_id`: string - Unique change identifier for precise undo/redo and academic attribution
- `parameter_path`: string - Exact parameter location with hierarchical addressing (e.g., "pricing.product_a.market_1")
- `old_value`: ParameterValue - Previous value with comprehensive type and constraint preservation
## Parameter Change Entity (Enhanced for Project-Scoped Audit Trail)

**Purpose:** Tracks individual parameter modifications with project-scoped undo/redo and complete audit isolation

**Key Attributes:**
- `change_id`: string - Unique change identifier
- `project_id`: string - **PROJECT SCOPING** - Associated project context for audit trail isolation
- `session_id`: string - Associated analysis session within project
- `parameter_name`: string - Parameter that was changed
- `old_value`: any - Previous value
- `new_value`: any - New value
- `user_id`: string - Who made the change
- `project_undo_redo_position`: number - Position in project-specific undo/redo stack
- `cross_project_isolation_verified`: boolean - Ensures change isolation between projects
- `timestamp`: Date - When the change occurred

### TypeScript Interface
```typescript
interface ParameterChange {
  change_id: string;
  project_id: string; // **PROJECT SCOPING KEY**
  session_id: string;
  parameter_name: string;
  old_value: any;
  new_value: any;
  user_id: string;
  project_undo_redo_position: number;
  cross_project_isolation_verified: boolean;
  timestamp: Date;
}
```

## Individual User API Key Management Entity (FR25)

**Purpose:** Secure storage of individual user AI service credentials with budget controls

**Key Attributes:**
- `credential_id`: string - Unique credential identifier
- `user_id`: string - Associated user account
- `institution_id`: string - Institutional boundary for compliance
- `service_name`: 'anthropic' | 'openrouter' | 'ollama' - AI service provider
- `encrypted_api_key`: string - AES-256-GCM encrypted credential
- `key_iv`: string - Initialization vector for encryption
- `key_tag`: string - Authentication tag for encryption integrity
- `daily_budget_usd`: number - Daily spending limit (default: $10)
- `monthly_budget_usd`: number - Monthly spending limit (default: $300)
- `total_usage_usd`: number - Cumulative usage tracking
- `is_active`: boolean - Key activation status
- `created_at`: Date - Credential creation timestamp
- `expires_at`: Date - Optional credential expiration
- `last_used_at`: Date - Last API usage timestamp

### TypeScript Interface
```typescript
interface UserAPICredential {
  credential_id: string;
  user_id: string;
  institution_id: string;
  service_name: 'anthropic' | 'openrouter' | 'ollama';
  encrypted_api_key: string;
  key_iv: string;
  key_tag: string;
  daily_budget_usd: number;
  monthly_budget_usd: number;
  total_usage_usd: number;
  is_active: boolean;
  created_at: Date;
  expires_at?: Date;
  last_used_at?: Date;
}
```

## AI Coaching Session Entity (Enhanced for Project-Scoped AI Contexts)

**Purpose:** Persistent user-specific AI coaching with project-scoped conversation memory, strategy learning isolation, and competitive intelligence separation

**Key Attributes:**
- `coaching_session_id`: string - Unique coaching session identifier
- `project_id`: string - **PROJECT SCOPING** - Associated project for AI coaching context isolation
- `user_id`: string - Associated user for personalized coaching
- `conversation_history`: object[] - Chat messages and AI responses (project-scoped)
- `strategy_preferences`: object - Learned user strategy patterns within this project context
- `decision_patterns`: object - Historical decision-making analysis isolated per project
- `risk_tolerance`: 'conservative' | 'moderate' | 'aggressive' - User risk profile for this project
- `learning_progress`: object - Competency development tracking per project
- `coaching_effectiveness`: number - AI recommendation success rate within project
- `project_competitive_intel_context`: object - Project-specific competitive intelligence and strategy insights
- `cross_project_coaching_isolation`: object - Ensures AI coaching contexts don't contaminate between projects
- `last_interaction`: Date - Most recent coaching interaction
- `total_interactions`: number - Conversation volume tracking per project

### TypeScript Interface
```typescript
interface AICoachingSession {
  coaching_session_id: string;
  project_id: string; // **PROJECT SCOPING KEY**
  user_id: string;
  conversation_history: ProjectScopedConversation[];
  strategy_preferences: ProjectStrategyPreferences;
  decision_patterns: ProjectDecisionPatterns;
  risk_tolerance: 'conservative' | 'moderate' | 'aggressive';
  learning_progress: ProjectLearningProgress;
  coaching_effectiveness: number;
  project_competitive_intel_context: ProjectCompetitiveContext;
  cross_project_coaching_isolation: CoachingIsolationConfig;
  last_interaction: Date;
  total_interactions: number;
}

interface ProjectScopedConversation {
  message_id: string;
  timestamp: Date;
  user_message: string;
  ai_response: string;
  project_context_tags: string[];
  strategy_learning_impact: object;
}

interface ProjectStrategyPreferences {
  optimization_priorities: string[];
  risk_management_approach: string;
  competitive_focus_areas: string[];
  parameter_adjustment_patterns: object;
  project_specific_insights: object;
}

interface CoachingIsolationConfig {
  isolated_conversation_memory: boolean;
  project_scoped_strategy_learning: boolean;
  competitive_intel_separation: boolean;
  cross_project_contamination_prevention: boolean;
}
  coaching_session_id: string;
  user_id: string;
  conversation_history: ConversationMessage[];
  strategy_preferences: StrategyProfile;
  decision_patterns: DecisionPattern[];
  risk_tolerance: 'conservative' | 'moderate' | 'aggressive';
  learning_progress: CompetencyTracker;
  coaching_effectiveness: number;
  last_interaction: Date;
  total_interactions: number;
}

interface ConversationMessage {
  message_id: string;
  sender: 'user' | 'ai';
  content: string;
  context: any;
  timestamp: Date;
}
```

## Microservices Data Architecture (Database-per-Service Pattern)

### **1. GMC Calculation Service → PostgreSQL**
**Responsibility:** Core GMC mathematical engine, Excel integration, parameter analysis
**Database Ownership:**
- **Tables:** `analysis_sessions`, `parameter_changes`, `calculated_results`, `constraint_validations`, `excel_imports`
- **Data Patterns:** Transactional ACID compliance for financial calculations
- **Performance:** Read replicas for calculation-heavy operations, write-master for real-time updates
- **Integration:** Publishes calculation events via message queue, exposes calculation APIs

```sql
-- **EPIC 0 ENHANCED:** Project-Scoped GMC Calculation Service Schema
CREATE TABLE projects (
    project_id UUID PRIMARY KEY,
    project_name VARCHAR(255) NOT NULL,
    project_description TEXT,
    user_id VARCHAR(100) NOT NULL, -- Project owner
    team_members JSONB NOT NULL DEFAULT '[]'::jsonb, -- Array of user IDs
    project_type VARCHAR(50) NOT NULL CHECK (project_type IN ('individual', 'team_collaboration', 'competitive_intelligence')),
    project_template VARCHAR(50) NOT NULL CHECK (project_template IN ('blank', 'standard_gmc', 'advanced_multi_scenario')),
    data_isolation_boundary JSONB NOT NULL,
    timeline_independence JSONB NOT NULL,
    strategic_context JSONB NOT NULL,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_accessed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE companies (
    company_id VARCHAR(50) NOT NULL,
    project_id UUID NOT NULL REFERENCES projects(project_id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    members JSONB NOT NULL DEFAULT '[]'::jsonb,
    current_quarter VARCHAR(20) NOT NULL,
    project_role_permissions JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (company_id, project_id),
    UNIQUE (company_id, project_id)
);

CREATE TABLE gmc_reports (
    report_id UUID PRIMARY KEY,
    project_id UUID NOT NULL REFERENCES projects(project_id) ON DELETE CASCADE,
    company_id VARCHAR(50) NOT NULL,
    report_type VARCHAR(20) NOT NULL CHECK (report_type IN ('history', 'game')),
    quarter_period VARCHAR(20) NOT NULL,
    filename VARCHAR(255) NOT NULL,
    data JSONB NOT NULL,
    is_valid BOOLEAN DEFAULT false,
    project_timeline_position INTEGER NOT NULL,
    cross_project_isolation_verified BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (company_id, project_id) REFERENCES companies(company_id, project_id)
);

CREATE TABLE analysis_sessions (
    session_id UUID PRIMARY KEY,
    project_id UUID NOT NULL REFERENCES projects(project_id) ON DELETE CASCADE,
    company_id VARCHAR(50) NOT NULL,
    session_name VARCHAR(255) NOT NULL,
    base_report_id UUID REFERENCES gmc_reports(report_id),
    base_report_data JSONB NOT NULL,
    decision_parameters JSONB NOT NULL,
    calculated_results JSONB,
    investment_performance DECIMAL(10,2),
    project_analysis_context JSONB NOT NULL DEFAULT '{}'::jsonb,
    cross_session_isolation_boundary JSONB NOT NULL DEFAULT '{}'::jsonb,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (company_id, project_id) REFERENCES companies(company_id, project_id)
);

CREATE TABLE parameter_changes (
    change_id UUID PRIMARY KEY,
    project_id UUID NOT NULL REFERENCES projects(project_id) ON DELETE CASCADE,
    session_id UUID NOT NULL REFERENCES analysis_sessions(session_id) ON DELETE CASCADE,
    parameter_path VARCHAR(255) NOT NULL,
    old_value JSONB,
    new_value JSONB NOT NULL,
    change_reason VARCHAR(500),
    user_id VARCHAR(100) NOT NULL,
    project_undo_redo_position INTEGER NOT NULL,
    cross_project_isolation_verified BOOLEAN DEFAULT true,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- **PROJECT-SCOPED INDEXES** for performance isolation
CREATE INDEX idx_projects_user_id ON projects(user_id);
CREATE INDEX idx_projects_active ON projects(is_active, last_accessed_at);
CREATE INDEX idx_companies_project_id ON companies(project_id);
CREATE INDEX idx_gmc_reports_project_id ON gmc_reports(project_id);
CREATE INDEX idx_analysis_sessions_project_id ON analysis_sessions(project_id);
CREATE INDEX idx_parameter_changes_project_id ON parameter_changes(project_id);

-- **PROJECT DATA ISOLATION CONSTRAINTS**
CREATE OR REPLACE FUNCTION verify_project_data_isolation() 
RETURNS TRIGGER AS $$
BEGIN
    -- Ensure all related data belongs to the same project
    IF TG_TABLE_NAME = 'analysis_sessions' THEN
        IF NOT EXISTS (SELECT 1 FROM companies WHERE company_id = NEW.company_id AND project_id = NEW.project_id) THEN
            RAISE EXCEPTION 'Cross-project data contamination prevented: company_id % does not belong to project_id %', NEW.company_id, NEW.project_id;
        END IF;
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_project_isolation_analysis_sessions 
    BEFORE INSERT OR UPDATE ON analysis_sessions 
    FOR EACH ROW EXECUTE FUNCTION verify_project_data_isolation();
```

### **2. Knowledge Graph Service → Neo4j**
**Responsibility:** GMC business rule relationships, strategic reasoning, constraint dependencies
**Database Ownership:**
- **Nodes:** GMC Rules, Parameters, Markets, Products, Constraints, Strategies
- **Relationships:** DEPENDS_ON, CONFLICTS_WITH, OPTIMIZES_FOR, IMPACTS
- **Graph Patterns:** Rule traversal, impact analysis, optimization pathways
- **Integration:** Subscribes to calculation events, provides reasoning APIs

```cypher
// Example Neo4j schema for Knowledge Graph Service
CREATE (rule:GMCRule {id: 'capacity_constraint', type: 'hard_constraint', description: 'Machine capacity cannot exceed available hours'})
CREATE (param:Parameter {id: 'machine_hours_product_a', type: 'decision_variable', min_value: 0})
CREATE (market:Market {id: 'europe', name: 'European Market', demand_elasticity: 0.8})

CREATE (param)-[:SUBJECT_TO]->(rule)
CREATE (param)-[:TARGETS]->(market)
```

### **3. AI Coaching Service → Weaviate + MongoDB**
**Responsibility:** Conversational AI, user preference learning, strategy recommendations
**Database Ownership:**
- **Weaviate:** Semantic search vectors, conversation context, strategy similarity
- **MongoDB:** User coaching profiles, conversation history, AI model parameters
- **Integration:** Consumes calculation results, publishes coaching insights

```python