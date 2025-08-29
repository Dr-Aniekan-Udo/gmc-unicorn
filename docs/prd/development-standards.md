# Development Standards

## Coding Standards

**Python Code Standards (Backend Services)**
- **Python Version Compliance**: All backend services must use Python 3.12+ leveraging latest performance improvements and type hinting enhancements
- **Code Formatting**: Black formatting with 88-character line limit for consistent code style across microservices
- **Type Annotations**: Full type hinting required for all functions, classes, and methods using Python 3.12 enhanced typing features
- **Import Organization**: isort configuration for consistent import ordering and dependency management
- **Code Quality**: Pylint/flake8 compliance with project-specific rules for Flask microservices architecture
- **Dependency Management**: uv package manager for fast dependency resolution and secure package management across all Python services

**React/JavaScript Code Standards (Frontend)**
- **React Version Compliance**: React 18.2+ with strict TypeScript integration for component-based architecture
- **Component Standards**: Functional components with hooks, proper prop typing, and Tailwind CSS + Headless UI integration
- **Code Formatting**: Prettier with 2-space indentation and consistent JSX formatting
- **TypeScript Integration**: Strict TypeScript configuration for type safety across React components and API integrations
- **Build Tools**: Vite 5.0+ for fast development build system with hot module replacement and optimized bundling
- **Package Management**: npm 10.2+ for JavaScript/TypeScript dependency management supporting React ecosystem

**Database Schema Standards**
- **PostgreSQL Schema**: SQLAlchemy models with proper foreign key relationships and database-level constraints
- **Multi-Database Integration**: Consistent naming conventions across PostgreSQL, Neo4j, Weaviate, MongoDB, Redis, and ClickHouse
- **Migration Management**: Alembic-based database migrations with rollback strategies and data integrity validation
- **Security Standards**: Row-level security policies, encrypted field storage (AES-256-GCM), and institutional boundary enforcement

## Documentation Standards

**API Documentation**
- **OpenAPI Compliance**: All microservice endpoints documented using OpenAPI 3.0 specifications with comprehensive schema definitions
- **Interactive Documentation**: Swagger UI deployment for all services enabling real-time API testing and validation
- **Endpoint Specifications**: Complete request/response schemas, error codes, and authentication requirements
- **Version Documentation**: API versioning strategy documentation with backward compatibility guidelines

**Code Documentation**
- **Docstring Standards**: Python docstrings following Google style with parameter types, return values, and usage examples
- **Component Documentation**: React component documentation with PropTypes/TypeScript interfaces and usage examples
- **Architecture Documentation**: Comprehensive service interaction diagrams and data flow documentation
- **Database Documentation**: Entity relationship diagrams and schema documentation with constraint explanations

**Technical Documentation**
- **Setup Documentation**: SETUP.md, README.md, and INSTALL.md with comprehensive installation and configuration instructions
- **AI Infrastructure Guide**: Intelligence directory setup, API key configuration, and deployment scenario documentation
- **Deployment Documentation**: Kubernetes, Docker, and development environment setup with troubleshooting guides
- **Security Documentation**: FERPA compliance procedures, encryption standards, and security policy implementation

## Git Workflows

**Branch Management Strategy**
- **Main Branch Protection**: Protected main branch requiring pull request reviews and CI/CD validation
- **Feature Branch Naming**: Descriptive branch names following pattern: `feature/epic-X-story-Y-description`
- **Release Branch Strategy**: Release branches for version management and production deployment coordination
- **Hotfix Process**: Emergency fix workflow with direct main branch merge and backward compatibility validation

**Commit Standards**
- **Conventional Commits**: Standardized commit messages with type, scope, and description for automated changelog generation
- **Commit Atomicity**: Single-purpose commits with clear descriptions and appropriate scope
- **Pre-commit Hooks**: Automated code formatting, linting, and test execution before commit acceptance
- **Commit Signing**: GPG-signed commits for security and authorship verification

**Pull Request Process**
- **Code Review Requirements**: Minimum two approvals for main branch merges with architecture review for structural changes
- **Automated Testing**: CI/CD pipeline execution with comprehensive test suite validation
- **Documentation Updates**: Mandatory documentation updates for API changes, new features, and architectural modifications
- **Performance Validation**: Automated performance testing for calculation engine changes and optimization validation

## Quality Assurance Standards

**Testing Strategy Enhancement**
- **Unit Test Coverage**: Minimum 90% code coverage for calculation engines with mathematical accuracy validation
- **Integration Testing**: Cross-service communication testing with database transaction validation
- **End-to-End Testing**: Complete user workflow testing from file upload through analysis completion
- **Performance Testing**: Load testing for 50+ concurrent users with sub-2 second response time validation
- **Security Testing**: Penetration testing for API endpoints and encryption validation for user credentials
- **Mathematical Validation**: Excel equivalency testing with 100% accuracy requirements against reference datasets

**Continuous Integration Standards**
- **Automated Test Execution**: Full test suite execution on all pull requests with failure blocking merge
- **Build Validation**: Multi-environment build testing (development, staging, production) with container validation
- **Dependency Scanning**: Automated vulnerability scanning for Python (uv) and JavaScript (npm) dependencies
- **Code Quality Gates**: Automated code quality checks with configurable thresholds and improvement tracking

**Quality Metrics and Monitoring**
- **Performance Monitoring**: Real-time application performance monitoring with alert thresholds and optimization tracking
- **Error Tracking**: Comprehensive error logging and monitoring with user impact assessment and resolution tracking
- **Usage Analytics**: User behavior tracking for feature optimization and educational effectiveness measurement
- **Security Monitoring**: Continuous security monitoring with threat detection and compliance validation

## API Versioning Strategy

**Microservices API Versioning**
- **Semantic Versioning**: Major.Minor.Patch versioning for all microservice APIs with backward compatibility maintenance
- **API Gateway Integration**: Kong/Traefik routing configuration supporting multiple API versions simultaneously
- **Version Deprecation Policy**: 6-month deprecation notice for breaking changes with migration documentation and support
- **Client SDK Versioning**: Coordinated client library updates with server API versions for consistent integration

**Service-to-Service Communication**
- **Internal API Consistency**: Standardized request/response formats across all 10 microservices with consistent error handling
- **Service Discovery Integration**: Dynamic service endpoint resolution with health checking and failover capabilities
- **Circuit Breaker Implementation**: Resilience patterns for inter-service communication with graceful degradation
- **Message Format Standards**: JSON message schemas with validation and backward compatibility enforcement

**API Documentation Versioning**
- **Version-Specific Documentation**: Separate OpenAPI specifications for each major API version with migration guides
- **Interactive Testing**: Swagger UI environments for each API version enabling comprehensive testing and validation
- **Changelog Management**: Automated changelog generation from git commits with API change impact assessment
- **Developer Communication**: Proactive developer notification system for API changes and version updates

## Excel Integration Architecture:
**openpyxl Integration Strategy:**
- **Formula extraction**: Parse existing `gmc_analysis.xlsx` to extract exact formula definitions for replication validation
- **Report parsing**: Process uploaded GMC quarterly reports to populate dashboard with current period data
- **Structure analysis**: Extract cell dependencies and calculation order from Excel sheets to inform DAG implementation
- **Validation datasets**: Use extracted formulas from reference Excel files to validate Python calculation accuracy

**GMC File Processing Logic:**
```python
# File naming pattern recognition
HISTORY_FILE_PATTERN = r'^Hst(Y\d{2})(Q[1-4]).*\.xlsx?$'  # HstY16Q1.xlsx
GAME_REPORT_PATTERN = r'^W(\d{6}).*\.xlsx?$'               # W122162.xlsx

FILE_PROCESSING = {
    'history_files': {
        'pattern': 'Hst + Year + Quarter',
        'minimum_count': 1,   # Minimum 1 quarter required
        'recommended_count': 5,  # 5-quarter history recommended for optimal analysis
        'processing': 'adaptive_baseline_setup',  # Adapts to available history
        'timeline_position': 'historical_data'
    },
    'game_reports': {
        'pattern': 'W + 6-digit series',
        'processing': 'current_quarter_analysis',
        'timeline_position': 'current_gameplay'
    }
}

# Company/Team identification and data processing
COMPANY_MANAGEMENT = {
    'identification_pattern': 'Company [1-8]',  # Typical GMC group size 8-12 companies
    'data_extraction': {
        'group_information_sheet': 'Extract all company data for competitive context',
        'company_specific_data': 'Filter analysis data for selected company perspective',
        'competitive_benchmarking': 'Anonymous comparison against other companies'
    },
    'selection_workflow': {
        'step_1': 'Upload files and detect available companies in simulation group',
        'step_2': 'User selects their team company from available options',
        'step_3': 'System filters all data and analysis for selected company perspective',
        'step_4': 'Competitive context maintained while focusing on selected company'
    }
}

# Trend analysis data combination
TREND_ANALYSIS = {
    'cross_quarter_metrics': [
        'investment_performance',
        'revenue_trends', 
        'cost_optimization',
        'market_share_evolution',
        'operational_efficiency',
        'financial_ratios'
    ],
    'combination_strategies': {
        'historical_baseline': 'Average of available history quarters',
        'progressive_tracking': 'Quarter-over-quarter progression analysis', 
        'comparative_benchmarking': 'Current vs historical performance gaps',
        'trend_projection': 'Predictive analysis based on historical patterns'
    }
}
```

## GMC Manual Integration:
**Official GMC Manual Integration:**
- **Primary Reference**: `overview/GMC-Manual.pdf` - Complete official Global Management Challenge manual containing all simulation rules, formulas, and constraints
- **Quick Reference**: `overview/GMC-manual_summary.md` - Condensed summary of key GMC rules and validation criteria for rapid developer reference
- **Rule Validation**: All implemented formulas and constraints must align with official GMC Manual specifications to ensure simulation compliance
- **Dispute Resolution**: In cases of discrepancy between Excel implementation and manual specifications, GMC Manual takes precedence as authoritative source

## Testing Data Resources:
**Historical Reference Data (`overview/gmc_history_sample/`):**
- Pre-game historical data typically provided before simulation starts
- Baseline scenarios for formula validation and constraint testing

**Quarterly Report Data (`overview/gmc_report_sample/`):**
- Post-decision quarterly reports generated after each game round
- Real GMC data structures for upload functionality testing

**Visual Reference (`overview/screenshot_gmc_analysis_sheet/`, `overview/screenshot_gmc_report_sheet/`):**
- Excel layout screenshots for UI mirroring and design validation
- Visual confirmation of formula relationships and sheet interdependencies
