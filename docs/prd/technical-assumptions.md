# Technical Assumptions

## Repository Structure: Microservices Monorepo with Service-Oriented Architecture
Microservices monorepo containing containerized services with database-per-service pattern:
- `/services/`: Microservices directory
  - `/core/`: Core GMC services (6 services)
    - `/gmc-calculation-service/`: Flask-based GMC mathematical engine with PostgreSQL
    - `/knowledge-graph-service/`: Flask-based Neo4j relationships and GMC rule reasoning
    - `/content-management-service/`: Flask-based GMC Manual versioning with MongoDB
    - `/user-management-service/`: Flask-based authentication with PostgreSQL + API key encryption
    - `/analytics-service/`: Flask-based educational analytics with PostgreSQL + ClickHouse
    - `/notification-service/`: Flask-based real-time collaboration with Redis + WebSocket
  - `/ai-coaching/`: AI Coaching Ecosystem (4 services)
    - `/conversation-service/`: Rasa + MongoDB + Multi-LLM provider support
    - `/vector-search-service/`: Weaviate + GMC Manual semantic search
    - `/ml-recommendation-service/`: CatBoost + XGBoost + MLflow experimentation
    - `/coaching-orchestrator/`: Service coordination + unified API interface
- `/frontend/`: React SPA with Dash integration for mathematical visualizations
- `/intelligence/`: AI infrastructure directory with configurations, models, prompts, and deployment resources
- `/infrastructure/`: Deployment configurations
  - `/docker/`: Docker Compose configurations for development and production
  - `/kubernetes/`: Kubernetes manifests and Helm charts
  - `/terraform/`: Cloud infrastructure provisioning
- `/shared/`: Shared libraries and common utilities across services
- `/tests/`: Comprehensive test suites for formula validation and service integration
- `/config/`: Environment-specific configuration management
- `/database/`: Database schemas, migrations, and seed data
- `/monitoring/`: Prometheus, Grafana, and observability configurations  
- `/docs/`: Technical documentation and API specifications
- `/.github/`: CI/CD workflows and GitHub automation
- **Root Setup Documentation**: SETUP.md, README.md, and INSTALL.md providing comprehensive installation, configuration, AI infrastructure setup, troubleshooting instructions, and deployment scenarios for the entire GMC Dashboard project

**Architectural Control**: The core directory structure within the `gmc-dashboard/` project is defined by the architecture team with established organizational patterns. Developers may create subdirectories following these established patterns, validated through code review processes to prevent conflicts during coding and testing phases. Architectural pattern modifications require architect approval and corresponding documentation updates.

## Service Architecture: Microservices with Database-Per-Service Pattern
Python Flask-based microservices architecture with React frontend and specialized service boundaries. Ten microservices (6 core + 4 AI coaching) maintain dedicated databases for optimal performance and data isolation: gmc-calculation-service with PostgreSQL for mathematical processing, user-management-service with PostgreSQL for authentication and API keys, conversation-service with MongoDB for multi-provider LLM integration, vector-search-service with Weaviate for GMC Manual semantic search, ml-recommendation-service with MLflow for classical ML, coaching-orchestrator for AI service coordination, knowledge-graph-service with Neo4j for relationship reasoning, analytics-service with PostgreSQL + ClickHouse for educational insights, content-management-service with MongoDB for GMC Manual versioning, and notification-service with Redis for real-time collaboration. This microservices approach provides service isolation, independent scaling, and specialized data processing while maintaining Flask technology consistency.

**Deployment Complexity Acknowledgment**: The multi-database architecture requires institutional IT support for production deployment, with containerized development environments provided to simplify local setup. Educational institutions should plan for infrastructure support or consider cloud-hosted deployment options.

**Post-MVP API and Automation Architecture:**
- **RESTful API Layer**: FastAPI integration providing OpenAPI-compliant endpoints for external system integration
- **N8n Workflow Engine**: Containerized N8n instance for advanced automation scenarios and workflow orchestration
- **Webhook Infrastructure**: Event-driven notifications for analysis completion, constraint violations, and performance milestones
- **Authentication Layer**: API key management and rate limiting for secure third-party access

## Testing Requirements: Unit + Integration
Comprehensive testing strategy essential for mathematical accuracy:
- **Unit Tests**: Individual formula calculations validated against Excel reference data
- **Integration Tests**: Cross-sheet dependency validation ensuring proper calculation propagation
- **Validation Tests**: Complete GMC scenarios tested against both `overview/gmc_history_sample/` and `overview/gmc_report_sample/` datasets for comprehensive historical and quarterly report validation
- **Performance Tests**: Load testing for 50+ concurrent users and sub-2 second response requirements
- **UI Tests**: Constraint validation and error recovery workflows

## Frontend Technology Stack Enhanced:
- **Primary UI Framework**: React.js (18.2+) for modern reactive UI development with component-based architecture
- **Mathematical Visualization**: Dash Plotly (2.16+) for real-time mathematical charts and GMC analysis dashboards with Excel-equivalent mathematical precision
- **Graph Integration**: Dash Components in React (2.16+) for embedded Dash graphs within React components, enabling seamless integration of Python-generated plots in React frontend
- **Frontend Graph Rendering**: Plotly.js (2.26+) for interactive graph rendering in browser with client-side graph interactivity, zoom, pan, hover effects
- **Build Tools**: Vite (5.0+) for fast development build system with hot module replacement and optimized bundling
- **JavaScript Project Manager**: npm (10.2+) for JavaScript/TypeScript dependency management supporting React ecosystem and frontend build tools
- **UI Components**: Tailwind CSS + Headless UI (3.4+ / 1.7+) for styling and accessible components with WCAG 2.1 AA compliance
- **Typography**: Inter + JetBrains Mono + Outfit (Latest) - Inter (primary), JetBrains Mono (performance metrics), Outfit (Team Unicorn branding)
- **State Management**: Zustand + React Query (4.4+ / 5.0+) for client state and server synchronization with simple state management and built-in caching
- **Advanced UI Components**: React.js integration for complex UI patterns including:
  - **Interactive Popup/Modal Windows**: Multi-sheet analysis views with full zoom and pan capabilities, drag-to-reposition functionality, and resize handles
  - **Advanced Drag & Drop**: Parameter manipulation interfaces for complex constraint scenarios  
  - **Dynamic Layouts**: Resizable panels and customizable dashboard arrangements
  - **Real-time Collaboration**: Advanced UI patterns for team-based analysis features
- **Component Library Foundation**: Educational-Professional Hybrid Component Architecture with Team Unicorn brand integration and WCAG 2.1 AA compliance

## Backend Technology Stack:
- **Microservices Architecture**: Flask-based microservices with database-per-service pattern and container orchestration
- **Core Language**: Python (3.12+) as primary development language leveraging latest performance improvements and type hinting enhancements
- **Package Management**: uv for fast dependency resolution and secure package management across all Python services
- **Web Framework**: Flask as microservice framework foundation across all backend services
- **Excel Integration**: openpyxl for precise Excel file parsing and formula extraction from GMC reports
- **Mathematical Processing**: Pandas/NumPy for mathematical calculations and data manipulation across calculation services
- **Database Architecture**: Multi-database architecture with specialized data storage:
  - **PostgreSQL**: Primary transactional database for GMC calculations, user management, and analytics
  - **Neo4j**: Graph database for GMC rule relationships and knowledge reasoning
  - **Weaviate**: Vector database for semantic search and RAG capabilities  
  - **MongoDB**: Document database for GMC Manual content management and AI coaching profiles
  - **Redis**: In-memory database for session management, caching, and real-time collaboration
  - **ClickHouse**: Time-series database for educational analytics and performance tracking
- **Data Modeling**: SQLAlchemy for PostgreSQL models, Neo4j driver for graph operations, Weaviate client for vector operations
- **Container Orchestration**: Kubernetes with Helm charts for production deployment and service management
- **API Gateway**: Kong/Traefik for service routing, authentication, rate limiting, and external API management
- **Service Mesh**: Istio for inter-service communication, observability, and security policies
- **Service Communication**: RESTful APIs between services with JSON message format and service discovery
- **Background Processing**: Celery with Redis for asynchronous task processing and model training workflows

## AI Technology Stack:
- **Individual API Key Management**: AES-256-GCM encryption system for secure user-specific AI service credentials with PostgreSQL storage and runtime security model
- **Multi-Provider LLM Integration**: Comprehensive support for 6 LLM providers enabling user choice and optimization:
  - **OpenAI**: GPT-4, GPT-3.5-turbo integration with advanced reasoning capabilities
  - **Anthropic**: Claude-3, Claude-2 integration with safety-focused analysis
  - **Google**: Gemini Pro integration with multimodal capabilities
  - **DeepSeek**: DeepSeek Coder integration optimized for technical analysis
  - **OpenRouter**: Multi-model routing and access with cost optimization
  - **Ollama**: Local privacy-preserving AI deployment for institutional control
- **Provider Selection Architecture**: Individual user API key management across all providers with automatic fallback strategies, cost optimization, and budget controls per provider
- **Knowledge Graph + RAG Architecture**: 
    - **Graph Database**: Neo4j (5.x Community Edition) for GMC rule relationships and strategic reasoning
    - **Vector Database**: Weaviate (1.2x) for semantic search over GMC manual and user strategies with embeddings
    - **Graph Construction**: NetworkX (3.x) for building and manipulating knowledge graphs in Python
- **Conversational AI Framework**: 
    - **Chatbot Engine**: Rasa (3.x) for building persistent AI Coach interface with conversation memory and context retention
    - **Natural Language Processing**: spaCy (3.x) for text processing and entity extraction from GMC Manual and user interactions
- **Classical Machine Learning Integration**:
    - **Gradient Boosting Models**: CatBoost (1.x), XGBoost (2.x) for investment performance prediction and parameter sensitivity analysis
    - **LLM Orchestration**: Intelligent coordination where LLM analyzes context, determines required calculations, coordinates classical models, and synthesizes results with GMC-specific strategic recommendations
- **AI Infrastructure Management**:
    - **Experiment Tracking**: MLflow (2.x) for managing classical model lifecycle, performance metrics, and A/B testing
    - **Workflow Automation**: Apache Airflow (2.x) for scheduling data pipelines, model training, and evaluation workflows
    - **Model Serving**: Dedicated AI coaching microservice with Weaviate + MongoDB + Rasa integration
- **AI Service Architecture**:
    - **AI Coaching Service**: Flask microservice managing conversational AI, user profiles, and personalized strategy learning
    - **Knowledge Graph Service**: Flask microservice for Neo4j relationships and GMC rule reasoning
    - **Unified Data Pipeline**: Centralized data lake providing both LLM and classical models access to training data, evaluation metrics, and real-time monitoring with academic compliance tracking
- **User Experience Integration**:
    - **Per-User Budget Controls**: Daily ($10) and monthly ($300) limits with real-time usage tracking
    - **API Key Management Interface**: User-controlled credential rotation, activation/deactivation, and usage monitoring
    - **Persistent Coaching**: User-specific AI instances that learn strategic preferences, decision patterns, and optimization goals with conversation history

## Database Choice Rationale: PostgreSQL
- **Complex relational data**: GMC analysis involves interconnected financial data across quarters with historical relationships
- **ACID compliance**: Financial calculations require transaction consistency
- **JSON support**: GMC reports contain nested data structures that PostgreSQL's JSON columns can efficiently store
- **Academic environment compatibility**: Most universities already run PostgreSQL
- **Formula audit trails**: Complex queries needed for tracking parameter changes across time periods
- **Concurrent user support**: MVCC essential for 50+ concurrent users analyzing shared GMC data
