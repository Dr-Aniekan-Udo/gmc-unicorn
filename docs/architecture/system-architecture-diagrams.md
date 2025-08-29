# System Architecture Diagrams

## 1. Microservices System Overview

```ascii
┌─────────────────────────────────────────────────────────────────────────────────┐
│                                GMC DASHBOARD                                     │
│                            MICROSERVICES ARCHITECTURE                           │
└─────────────────────────────────────────────────────────────────────────────────┘

                                ┌─────────────────┐
                                │  React Frontend │
                                │   (Vite 5.0+)   │
                                └─────────┬───────┘
                                          │
                                ┌─────────▼───────┐
                                │   API Gateway   │
                                │ (Kong/Traefik)  │
                                │ Authentication  │
                                │ Rate Limiting   │
                                └─────────┬───────┘
                                          │
                ┌─────────────────────────┼─────────────────────────┐
                │                         │                         │
    ┌───────────▼─────────────┐ ┌─────────▼─────────────┐ ┌─────────▼─────────────┐
    │    CORE SERVICES        │ │   AI COACHING         │ │   SHARED SERVICES     │
    │                         │ │                       │ │                       │
    │ ┌─────────────────────┐ │ │ ┌─────────────────┐   │ │ ┌─────────────────┐   │
    │ │gmc-calculation-svc  │ │ │ │conversation-svc │   │ │ │user-mgmt-svc   │   │
    │ │   PostgreSQL        │ │ │ │   MongoDB       │   │ │ │   PostgreSQL    │   │
    │ └─────────────────────┘ │ │ └─────────────────┘   │ │ └─────────────────┘   │
    │                         │ │                       │ │                       │
    │ ┌─────────────────────┐ │ │ ┌─────────────────┐   │ │ ┌─────────────────┐   │
    │ │knowledge-graph-svc  │ │ │ │vector-search    │   │ │ │analytics-svc    │   │
    │ │     Neo4j           │ │ │ │   Weaviate      │   │ │ │PostgreSQL+      │   │
    │ └─────────────────────┘ │ │ └─────────────────┘   │ │ │ClickHouse       │   │
    │                         │ │                       │ │ └─────────────────┘   │
    │ ┌─────────────────────┐ │ │ ┌─────────────────┐   │ │                       │
    │ │content-mgmt-svc     │ │ │ │ml-recommendation│   │ │ ┌─────────────────┐   │
    │ │    MongoDB          │ │ │ │MLflow+CatBoost  │   │ │ │notification-svc │   │
    │ └─────────────────────┘ │ │ └─────────────────┘   │ │ │     Redis       │   │
    │                         │ │                       │ │ └─────────────────┘   │
    │                         │ │ ┌─────────────────┐   │ │                       │
    │                         │ │ │coaching-        │   │ │                       │
    │                         │ │ │orchestrator     │   │ │                       │
    │                         │ │ └─────────────────┘   │ │                       │
    └─────────────────────────┘ └─────────────────────┘ └─────────────────────────┘

                            ┌─────────────────────────────────────┐
                            │           SERVICE MESH              │
                            │              (Istio)                │
                            │   • Inter-service Communication    │
                            │   • Circuit Breakers               │
                            │   • Observability & Monitoring     │
                            │   • Security Policies              │
                            └─────────────────────────────────────┘
```

## 2. Project-Scoped Data Flow Architecture

```ascii
┌─────────────────────────────────────────────────────────────────────────────────┐
│                          PROJECT-BASED DATA ISOLATION                          │
└─────────────────────────────────────────────────────────────────────────────────┘

    User Request: /projects/uuid-1234/analysis/parameters
                                    │
                          ┌─────────▼─────────┐
                          │   API Gateway     │
                          │ Project Context   │
                          │   Validation      │
                          └─────────┬─────────┘
                                    │ project_id: uuid-1234
                          ┌─────────▼─────────┐
                          │   GMC Calculation │
                          │     Service       │
                          │                   │
                          │ SELECT * FROM     │
                          │ sessions WHERE    │
                          │ project_id =      │
                          │ 'uuid-1234'       │
                          └─────────┬─────────┘
                                    │
              ┌─────────────────────┼─────────────────────┐
              │                     │                     │
    ┌─────────▼─────────┐ ┌─────────▼─────────┐ ┌─────────▼─────────┐
    │   AI Coaching     │ │   Analytics       │ │  Notifications    │
    │                   │ │                   │ │                   │
    │ Context isolated  │ │ Project metrics   │ │ Team updates for  │
    │ per project_id    │ │ only for this     │ │ this project only │
    │                   │ │ project           │ │                   │
    └───────────────────┘ └───────────────────┘ └───────────────────┘

COMPLETE PROJECT DATA ISOLATION:
• Database queries filtered by project_id
• AI coaching contexts completely separate
• No cross-project data contamination
• Team collaboration scoped to project only
```

## 3. AI Service Coordination Architecture

```ascii
┌─────────────────────────────────────────────────────────────────────────────────┐
│                       MULTI-PROVIDER AI ORCHESTRATION                          │
└─────────────────────────────────────────────────────────────────────────────────┘

                            Frontend Request:
                          "Optimize my strategy"
                                    │
                          ┌─────────▼─────────┐
                          │  Coaching         │
                          │  Orchestrator     │
                          │                   │
                          │ User API Keys:    │
                          │ • OpenAI ✓        │
                          │ • Anthropic ✓     │
                          │ • Ollama ✓        │
                          └─────────┬─────────┘
                                    │
              ┌─────────────────────┼─────────────────────┐
              │                     │                     │
    ┌─────────▼─────────┐ ┌─────────▼─────────┐ ┌─────────▼─────────┐
    │  Conversation     │ │  Vector Search    │ │  ML Recommendation│
    │                   │ │                   │ │                   │
    │ • Natural lang    │ │ • GMC Manual      │ │ • CatBoost        │
    │ • User prefs      │ │ • Semantic search │ │ • XGBoost         │
    │ • Project context │ │ • Knowledge graph │ │ • Pattern recog   │
    └─────────┬─────────┘ └─────────┬─────────┘ └─────────┬─────────┘
              │                     │                     │
              └─────────────────────┼─────────────────────┘
                                    │
                          ┌─────────▼─────────┐
                          │   Synthesized     │
                          │   Response        │
                          │                   │
                          │ "Increase Product │
                          │ 1 price to €125   │
                          │ for +23pts perf"  │
                          └───────────────────┘
```
