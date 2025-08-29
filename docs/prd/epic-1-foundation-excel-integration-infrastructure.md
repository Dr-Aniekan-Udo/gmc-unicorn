# Epic 1: Foundation & Excel Integration Infrastructure

**Epic Goal:** Establish project-scoped foundational infrastructure with complete Excel integration capabilities, mathematical calculation engine, and formula validation system that provides the core architecture for all subsequent GMC analysis functionality within individual project contexts while delivering testable health-check endpoints for immediate deployment validation.

## Story 1.1: Project-Scoped Foundation Setup

**As a** developer,  
**I want** complete project scaffolding with proper architecture and dependencies supporting project-scoped data isolation,  
**so that** I have a solid foundation for implementing the GMC Dashboard system with multiple independent project contexts.

### Acceptance Criteria
1. Python 3.12 project initialized with **uv** for modern Python project management and dependency handling
2. **npm** project initialized for JavaScript/React component management with multilanguage build integration
3. Directory structure created following microservices architecture: `/services/`, `/frontend/`, `/intelligence/`, `/infrastructure/`, `/shared/`, `/tests/`, `/config/`, `/database/`, `/monitoring/`, `/docs/`, `/.github/`
4. Service dependencies installed via uv: Flask for all microservices, openpyxl for calculation service, pandas/numpy for mathematical processing, database drivers (PostgreSQL, Neo4j, Weaviate, MongoDB, Redis), Kubernetes/Docker for orchestration
5. React development environment configured for advanced UI components with proper npm build integration
6. Development environment configured with proper logging, debugging, and hot-reload capabilities for both Python and JavaScript components
7. All microservices launch successfully with individual health-check endpoints, API Gateway routing configured, React frontend connects to services through API Gateway with proper authentication
8. Git repository initialized with proper .gitignore covering both Python (uv) and JavaScript (npm) artifacts and initial commit structure
9. Database schemas designed with project_id foreign key relationships across all services for complete project data isolation
10. Microservices configured to handle project-scoped operations with proper project context validation and data boundaries

## Story 1.2: Excel Formula Extraction System

**As a** developer,  
**I want** automated formula extraction from the GMC analysis Excel file,  
**so that** I can replicate exact mathematical calculations in Python with perfect fidelity.

### Acceptance Criteria
1. openpyxl integration reads `gmc_analysis.xlsx` and extracts all formulas from documented cell ranges
2. Formula dependency mapper creates directed acyclic graph (DAG) of calculation order requirements  
3. Cell reference parser converts Excel formulas to Python-equivalent mathematical expressions
4. Formula extraction system handles all 12 analysis sheets with proper error handling for missing cells
5. Extracted formulas saved in structured format (JSON/YAML) for validation and testing
6. System validates extracted formulas against known test cases from `overview/gmc_history_sample/`

## Story 1.3: Database Architecture Implementation

**As a** system architect,  
**I want** complete database schema and state management infrastructure,  
**so that** the microservices can persist data, manage distributed sessions, and coordinate undo/redo functionality across service boundaries while maintaining state consistency.

### Acceptance Criteria
1. Multi-database architecture implemented: PostgreSQL for gmc-calculation-service and user-management-service, Neo4j for knowledge-graph-service, Weaviate for ai-coaching-service vector storage, MongoDB for content-management-service, Redis for notification-service, ClickHouse for analytics-service
2. SQLAlchemy models implemented for all GMC data structures matching report sheet formats
3. Distributed state management integration: user-management-service handles sessions and undo/redo coordination, notification-service manages real-time state synchronization with Redis, each service maintains data persistence while supporting cross-service undo/redo operations
4. Database migration system (Alembic) configured with initial schema migration
5. Connection pooling and transaction management implemented for concurrent user support
6. Data validation layer ensures referential integrity between GMC report data and analysis calculations

## Story 1.4: Core Mathematical Engine Foundation

**As a** product manager,  
**I want** the fundamental calculation engine that processes interdependent formulas,  
**so that** real-time updates propagate correctly across all analysis components.

### Acceptance Criteria
1. Calculation engine processes formulas in DAG-determined order preventing circular dependencies
2. Event-driven architecture broadcasts parameter changes to all dependent calculations
3. Formula validation system ensures Python calculations match Excel results within 0.001% tolerance
4. Caching layer stores intermediate calculations to optimize performance for repeated operations
5. Error handling gracefully manages calculation failures without corrupting session state
6. Performance benchmarks demonstrate sub-500ms calculation updates for typical parameter changes

## Story 1.5: Project-Scoped GMC File Management and Import System

**As a** user,  
**I want** intelligent project-specific file management for GMC history and gameplay reports with complete independence between projects,  
**so that** I can maintain separate timelines for different strategic experiments and track progress within each project context.

### Acceptance Criteria
1. **Project-Scoped File Upload**: File upload interface isolates files within current project context, recognizing GMC naming conventions with complete independence from other projects
2. **Project-Specific Timeline Management**: Each project maintains independent file categorization and chronological sorting without cross-project interference
3. **Independent Timeline Visualization**: Visual timeline interface operates per project with drag-and-drop reordering affecting only the current project's sequence
4. **Project-Scoped Validation**: Flexible validation system analyzes historical data completeness within project boundaries, providing project-specific recommendations
5. **Project-Specific Progress Charts**: Visualization adapts to each project's available historical periods, showing improvement trends within project context
6. **Isolated Recalculation Triggers**: File management operations trigger recalculation only within the current project scope, maintaining complete isolation from other project analyses

## Story 1.6: Project-Scoped Company Selection and Group Information Integration

**As a** team member,  
**I want** to select company identity independently for each project,  
**so that** different projects can analyze different company perspectives or strategies while maintaining project-specific competitive context.

### Acceptance Criteria
1. **Project-Specific Company Detection**: System detects available companies from each project's uploaded files independently
2. **Independent Company Selection**: Each project allows separate company selection without affecting other projects
3. **Project-Scoped Analysis Perspective**: All analysis data, calculations, and visualizations reflect the chosen company within the current project context only
4. **Project-Specific Competitive Context**: Competitive benchmarking operates within project boundaries using project-specific group data
5. **Project-Persistent Selection**: Company selection persists within each project scope and integrates with project-specific team collaboration
6. **Project-Scoped Validation**: Data validation checks company completeness within project boundaries and provides project-specific warnings

## Story 1.7: Project-Scoped GMC Report Data Import System

**As a** user,  
**I want** automated import of quarterly GMC reports with project-specific data extraction and integration,  
**so that** each project's analysis system populates independently with relevant simulation data without cross-project interference.

### Acceptance Criteria
1. openpyxl parser extracts data from all 8 report sheet components with proper validation for both history and game report formats
2. Data transformation converts report formats to analysis sheet input parameters while maintaining historical context
3. Import validation ensures data completeness and flags missing or invalid values with specific error messages
4. System handles multiple report formats (history vs current quarter) with appropriate processing workflows
5. Historical data integration provides baseline calculations and trend analysis capabilities
6. Import process populates database with session data ready for analysis sheet calculations and progress tracking
7. **Project-Specific Gameplay Cycle Integration**: When new quarterly GMC reports are received, they are integrated into the specific project's historical timeline only when explicitly assigned, maintaining project-independent gameplay sequences and analysis continuity

## Story 1.8: Basic Health Check and Validation Framework

**As a** stakeholder,  
**I want** deployable system with comprehensive validation capabilities,  
**so that** I can verify the foundation works correctly before building advanced features.

### Acceptance Criteria
1. Health check endpoint returns system status including database connectivity and Redis availability
2. Formula validation suite runs complete test battery against reference Excel calculations
3. Performance monitoring tracks calculation speeds and identifies bottlenecks
4. Error logging captures and reports system issues with appropriate detail for debugging
5. Basic web interface displays system status and validation results for stakeholder review
6. Deployment scripts enable easy setup in development and staging environments
