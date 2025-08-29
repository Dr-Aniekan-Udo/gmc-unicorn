# Introduction

## Introduction

This architecture document defines the technical design for the GMC Dashboard application - an educational technology platform that transforms manual Excel-based Global Management Challenge analysis into an **investment performance optimization system** with AI-powered strategy assistance.

The design focuses on **MVP delivery with clear expansion pathways**, prioritizing core GMC functionality, mathematical accuracy, and essential AI features while maintaining the ability to scale to advanced capabilities. This approach ensures rapid time-to-market while building a solid foundation for the comprehensive features outlined in the PRD.

**MVP Focus Areas:**
- Complete GMC calculation engine with Excel equivalency
- Investment performance optimization dashboard
- Real-time constraint validation and team collaboration
- Basic AI strategy recommendations with user API key management
- Progressive web app with offline capability

**Post-MVP Expansion:**
- Advanced AI coaching with conversational interface
- Educational analytics dashboard for faculty
- Multi-institutional deployment modes
- Advanced competitive intelligence features

## Core Architectural Philosophy: MVP-First with Strategic Scaling

**MVP Foundation:** Cloud-native Progressive Web App focused on core GMC analysis with Excel equivalency, real-time collaboration, and basic AI recommendations. Built on microservices architecture with Flask backend services and React frontend for scalable deployment.

**Scaling Strategy:** Architecture designed for expansion to advanced AI coaching, multi-institutional deployment, and comprehensive educational analytics based on market validation and user feedback.

**Key Principles:**
- **Delivery Speed over Perfection:** Prioritize working core features over comprehensive edge-case handling
- **Strategic Simplification:** Single "golden path" for each technical decision to accelerate development
- **Expansion Readiness:** Clean architecture boundaries enable feature addition without refactoring

## Key Architectural Decisions & Rationale

**1. Epic 0: Revolutionary Project Management Foundation Architecture** ✅ **NEW FOUNDATIONAL DECISION**
- **Decision:** Multi-project system enabling multiple independent GMC analysis projects with complete data isolation, timeline independence, and strategic experimentation capabilities
- **Rationale:** Transforms single-session analysis into comprehensive project-based strategic experimentation platform. Enables users to compare different strategic approaches, maintain separate competitive intelligence contexts, and experiment with various risk tolerances across isolated projects.
- **Implementation:** 
  - **Project-Scoped Data Architecture:** All entities (sessions, reports, AI coaching) scoped by project_id with database-level isolation
  - **Timeline Independence:** Project-specific file management and historical data contexts
  - **Strategic Experimentation:** Project duplication, independent competitive intelligence, isolated AI coaching contexts
  - **Complete Isolation Enforcement:** Database triggers, API endpoint scoping, service communication context validation

**2. Investment Performance-First Architecture** ✅ **MAINTAINED**
- **Decision:** Investment performance optimization as core system objective with AI-powered strategy assistance within each project context
- **Rationale:** Each project can focus on different optimization strategies (aggressive growth, conservative risk management, competitive intelligence) while maintaining investment performance as the ultimate success metric
- **Implementation:** Project-scoped performance dashboards, parameter sensitivity analysis per project, AI recommendations based on project-specific strategy context

**3. Microservices Architecture with Database-per-Service Pattern** ✅ **UPDATED for PRD v6.0**
- **Decision:** Python Flask microservices with specialized databases, React frontend, and Kubernetes orchestration
- **Rationale:** Enables independent service scaling, specialized database optimization, and project-scoped data isolation across distributed architecture. Supports Epic 0's complex data isolation requirements.
- **Implementation:** 
  - **7 Core Microservices:** GMC Calculation, Knowledge Graph, AI Coaching, Content Management, User Management, Analytics, Notification
  - **Multi-Database Strategy:** PostgreSQL + Neo4j + Weaviate + MongoDB + Redis + ClickHouse for specialized data patterns
  - **Container Orchestration:** Kubernetes with Helm charts, API Gateway (Kong/Traefik), Service Mesh (Istio)
  - **Project Context Routing:** All service APIs enhanced with project_id validation and routing

**4. Progressive Web App with Project-Scoped Offline Capability** ✅ **ENHANCED**
- **Decision:** PWA with project-specific offline analysis and cross-project synchronization
- **Rationale:** Educational environments require offline capability, but multi-project architecture demands sophisticated sync strategies to prevent cross-project contamination
- **Implementation:** Service worker with project-scoped caching, offline calculation engine per project, intelligent sync with project isolation validation

**5. Comprehensive AI Integration with Project-Scoped Coaching** ✅ **ENHANCED per PRD v6.0 + Epic 0**
- **Decision:** Individual user API key management with project-isolated AI coaching contexts, knowledge graph reasoning, and conversational AI
- **Rationale:** Delivers personalized AI coaching that learns user strategy preferences independently per project while maintaining educational compliance, budget controls, and complete context separation between strategic experiments
- **Implementation:** 
  - **Project-Scoped AI Coaching:** MongoDB collections and Weaviate embeddings isolated by project_id
  - **Individual API Keys:** AES-256-GCM encryption with per-user budget enforcement (FR25)
  - **Knowledge Graph + RAG:** Neo4j relationships + Weaviate semantic search with project context awareness (FR30)
  - **Conversational AI:** Rasa-based coaching with project-specific conversation memory and strategy learning isolation (FR33-36)
  - **Classical ML Integration:** CatBoost/XGBoost orchestration with project-aware recommendation contexts (FR31)

**6. Excel Mathematical Fidelity with Project-Scoped Validation**
- **Decision:** Multi-library Excel parsing with project-isolated validation layers and comprehensive fallback strategies
- **Rationale:** GMC analysis demands 100% mathematical accuracy across all project contexts. Each project must maintain independent Excel equivalence validation without cross-project formula contamination.
- **Implementation:** 
  - **Project-Scoped Parsing:** openpyxl integration with project_id context validation
  - **Independent Formula Validation:** Project-specific test suites ensuring Excel equivalence per project
  - **Cross-Project Isolation:** Formula extraction and validation completely separated between projects

**7. Strategy Tuning & Building Block Flexibility with Project Context**
- **Decision:** AI-powered strategy optimization with project-aware formula customization capabilities and competitive intelligence integration
- **Rationale:** Different projects may require different strategic approaches. Excel formulas may contain redundant elements, but optimization suggestions must be contextualized to the specific project's strategic goals and competitive focus.
- **Implementation:** 
  - **Project-Aware ML Recommendations:** CatBoost/XGBoost models trained with project-specific context
  - **Building Block Intelligence per Project:** Redundancy detection isolated within project boundaries
  - **Formula Transparency Interface:** Project-scoped manual adjustment workflows with strategy context
  - **Competitive Intelligence Integration:** Building block suggestions informed by project-specific competitive analysis

**8. Progressive Complexity Management with Multi-Project UI Architecture** 
- **Decision:** HTML-first components with project-aware capability enhancement and multi-project navigation patterns
- **Rationale:** Educational users need seamless project switching and context awareness. Different projects may require different UI complexity levels based on strategic experimentation goals.
- **Implementation:** 
  - **Project-Scoped UI Components:** Interface complexity adapts based on project type and user competency within project context
  - **Multi-Project Navigation:** Semantic HTML foundation with project context preservation
  - **Progressive Project Enhancement:** Advanced features unlock based on demonstrated competency across multiple projects
  - **Context-Aware Help System:** Project-specific guidance and educational content

## Educational Environment Optimization

**Academic Constraints Addressed:**
- **FERPA Compliance:** Built-in data protection with configurable data residency options
- **Simple Deployment:** Container-based deployment with optional static file fallback  
- **Predictable Costs:** Local-first architecture minimizes ongoing cloud expenses
- **IT Resource Constraints:** Minimal administrative overhead with automated updates and monitoring
- **Network Limitations:** Graceful degradation for limited bandwidth and intermittent connectivity

**Pedagogical Requirements Supported:**
- **Mathematical Transparency:** Complete formula audit trails with Excel equivalence validation
- **Learning Analytics:** Faculty dashboard with student competency tracking and intervention triggers
- **Academic Integrity:** Comprehensive change attribution and decision rationale capture
- **Collaborative Learning:** Real-time team coordination without sacrificing individual analytical development

## Risk Mitigation Strategy

**Technical Risk Management:**
- **Multi-Layer Fallback Architecture:** Modern PWA → Reduced features → Static HTML → Excel export
- **Calculation Validation:** Excel compatibility test suite, multiple parsing libraries, formula verification layers
- **Performance Monitoring:** Built-in metrics tracking against 45-minute analysis target and 50+ concurrent user requirements

**Educational Risk Management:**  
- **Faculty Adoption Support:** Extensive transparency features, comprehensive training materials, academic integrity assurances
- **Student Learning Curve:** Progressive complexity disclosure, contextual help system, competency-based feature unlocking
- **Institutional Variation:** Configurable deployment modes, cultural adaptation framework, multi-language support planning

## Performance Requirements (NFR1 - Tiered Architecture)

The architecture implements tiered performance response requirements based on operation complexity per NFR1:

**Tier 1 - Basic Calculations (Sub-500ms):**
- **Direct Parameter Changes:** Excel formula calculations and basic input validation
- **Real-time Input Feedback:** Parameter constraints and validation state changes  
- **UI State Updates:** Interface responsiveness and visual feedback
- **Implementation:** Redis caching + optimized calculation engine

**Tier 2 - Cross-Sheet Updates (Sub-2 seconds):**
- **Interdependent Calculations:** Changes propagating across all GMC sheets
- **Investment Performance Updates:** Real-time ranking and competitive position
- **Constraint Validation:** Complex multi-parameter constraint checking
- **Implementation:** AsyncIO processing + database optimization

**Tier 3 - AI Analysis (3-10 seconds):**
- **Classical Model Processing:** CatBoost/XGBoost parameter optimization
- **Basic AI Recommendations:** Strategy suggestions and constraint guidance
- **Sensitivity Analysis:** Parameter impact assessment across scenarios
- **Implementation:** ML model coordination + intelligent caching

**Tier 4 - Advanced AI Processing (10-30 seconds):**
- **Complex Knowledge Graph Analysis:** Neo4j relationship traversal and reasoning
- **Comprehensive Strategy Optimization:** Multi-scenario competitive analysis
- **Conversational AI Coaching:** Contextual strategy guidance with full history
- **Implementation:** Multi-database coordination + LLM orchestration

## MVP Success Metrics 

The tiered architecture directly supports core PRD objectives:
- **85% Time Reduction:** Tiered response times optimize for most common operations (Tier 1-2)
- **90% Constraint Violation Reduction:** Real-time validation prevents impossible decisions
- **Mathematical Accuracy:** Excel equivalence through comprehensive validation layers
- **AI-Enhanced Analysis:** Intelligent recommendations within educational time constraints
- **Performance Reliability:** 99.9% uptime with graceful degradation across tiers

## **🚀 Epic 0 Project Management Foundation: Architectural Implementation Summary**

**Revolutionary Multi-Project Capability:** Complete architectural transformation enabling multiple independent GMC analysis projects with comprehensive data isolation, timeline independence, and strategic experimentation capabilities.

### **Core Project Management Architecture Features:**

1. **Complete Data Isolation:** 
   - Project-scoped database schemas with cascading foreign keys
   - Database-level triggers preventing cross-project data contamination
   - All entities (sessions, reports, AI coaching) scoped by project_id

2. **Timeline Independence:** 
   - Project-specific file management and chronological ordering
   - Independent historical data contexts per project
   - Cross-project timeline contamination prevention

3. **Strategic Experimentation Capabilities:**
   - Project duplication for strategy comparison
   - Independent competitive intelligence per project
   - Project-specific AI coaching contexts with isolated learning

4. **AI Coaching Context Separation:**
   - MongoDB collections scoped by project_id
   - Weaviate vector embeddings include project isolation
   - Conversation history and strategy learning completely separated

5. **Microservice Project Scoping:**
   - All service APIs enhanced with project_id routing
   - Service-to-service communication includes project context
   - Real-time collaboration scoped within project boundaries

### **Epic 0 Technical Validation:**

✅ **Project Entity Architecture** - Complete project management data model
✅ **Database Schema Updates** - All tables enhanced with project_id scoping
✅ **AI Coaching Isolation** - Project-specific coaching contexts in MongoDB/Weaviate
✅ **API Endpoint Enhancement** - All endpoints support project-scoped operations
✅ **Data Isolation Enforcement** - Database triggers prevent cross-project contamination
✅ **Timeline Independence** - Project-specific file organization and historical data
✅ **Strategic Context Support** - Project-specific competitive intelligence and experimentation

**Architecture Status:** **FULLY SUPPORTS EPIC 0 REVOLUTIONARY PROJECT MANAGEMENT FOUNDATION**
