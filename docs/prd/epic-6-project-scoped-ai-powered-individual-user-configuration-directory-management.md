# Epic 6: Project-Scoped AI-Powered Individual User Configuration & Directory Management

**Epic Goal:** Implement comprehensive individual user API key management with project-scoped AI coaching contexts, encrypted PostgreSQL storage, and standardized intelligence directory infrastructure that enables personalized AI-powered analysis capabilities per project while maintaining institutional security boundaries, budget controls, and FERPA compliance, delivering project-specific AI-enhanced GMC strategy optimization.

## Story 6.1: Individual User API Key Registration & Management

**As a** GMC participant,  
**I want** to securely register and manage my own AI service API keys,  
**so that** I can access personalized AI-powered analysis features while maintaining control over my credentials and usage costs.

### Acceptance Criteria
1. User interface for registering individual API keys for Anthropic Pro, OpenRouter, and Ollama services
2. AES-256-GCM encryption of all API credentials before database storage
3. PostgreSQL user_api_credentials table implementation with proper user_id and institution_id relationships
4. User-friendly key management interface with activation/deactivation, rotation, and deletion capabilities
5. API key validation and testing functionality to verify credential accuracy before storage
6. Display names and organizational features for managing multiple keys per service

## Story 6.2: Encrypted Database Schema & Security Implementation

**As a** system administrator,  
**I want** secure encrypted storage of user API credentials with institutional boundaries,  
**so that** individual user credentials remain protected while maintaining institutional compliance and audit capabilities.

### Acceptance Criteria
1. Complete user_api_credentials table with UUID relationships, encryption fields (encrypted_api_key, key_iv, key_tag)
2. Row-level security policies ensuring users can only access their own credentials
3. Institution admin access policies for institutional boundary management
4. Comprehensive audit logging for all API credential operations
5. Budget tracking fields (daily_budget_usd, monthly_budget_usd, total_usage_usd) with automated enforcement
6. Security metadata tracking (created_by_ip, last_accessed_ip, expires_at)
7. Multi-provider support for all 6 LLM providers (openai, anthropic, gemini, deepseek, openrouter, ollama)

### Database Schema
```sql
CREATE TABLE user_api_credentials (
    credential_id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    provider_name VARCHAR(50), -- 'openai', 'anthropic', 'gemini', 'deepseek', 'openrouter', 'ollama'
    encrypted_api_key TEXT,    -- AES-256-GCM encrypted
    key_iv TEXT,               -- Initialization vector for encryption
    key_tag TEXT,              -- Authentication tag for encryption
    daily_budget_usd DECIMAL DEFAULT 10.00,
    monthly_budget_usd DECIMAL DEFAULT 300.00,
    total_usage_usd DECIMAL DEFAULT 0.00,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW(),
    last_accessed_at TIMESTAMP,
    expires_at TIMESTAMP,
    created_by_ip INET,
    last_accessed_ip INET
);
```

## Story 6.3: intelligence Directory Structure Implementation & Management

**As a** developer,  
**I want** standardized intelligence directory infrastructure with proper configuration management,  
**so that** AI features have consistent deployment and configuration across all environments.

### Acceptance Criteria
1. Complete intelligence directory structure with all documented subdirectories: api-configs/, classical-ml-models/, llm-prompts/, deployment-configs/, training-data/, agent-configs/, prompts/, and models/
2. Configuration file templates (anthropic.yaml, openrouter.yaml, ollama.yaml) with database credential integration and proper validation
3. Automated README.md generation reflecting current directory structure and configuration
4. Debug logging infrastructure (debug-log.md) for AI development tracking  
5. Classical ML model storage organization with catboost-models/, xgboost-models/, and scikit-models/ subdirectories
6. LLM prompt template library with strategy-optimization/, formula-analysis/, and competitive-intel/ subdirectories
7. Multi-environment deployment configurations with local-ollama/, cloud-api/, and hybrid/ subdirectories
8. Training data management with gmc-historical-samples/, synthetic-scenarios/, and validation-datasets/ subdirectories
9. AI agent configuration files (strategy-tuning-agent.yaml, building-block-agent.yaml, competitive-intel-agent.yaml)
10. Legacy directory support for prompts/ and models/ during migration phases
11. Complete subdirectory structure implementation including all discovered organizational patterns from reference `intelligence` implementation
12. Integration validation ensuring `intelligence` directory placement within `gmc-dashboard/` application structure functions correctly with development and deployment processes
13. Documentation completeness validation ensuring all subdirectories and configuration files match architectural specifications and development requirements

## Story 6.4: Individual Budget Controls & Usage Monitoring

**As a** GMC participant,  
**I want** personal budget controls and real-time usage monitoring for my AI service usage,  
**so that** I can manage costs and prevent unexpected charges while accessing AI features.

### Acceptance Criteria
1. User interface for setting personal daily and monthly budget limits per API service
2. Real-time usage tracking with cost calculations and remaining budget displays
3. Automated service suspension when budget limits are exceeded
4. Usage history and analytics dashboard showing API call patterns and costs
5. Budget reset functionality and usage period management
6. Email notifications for budget warnings (75%, 90%, 100% usage levels)

## Story 6.5: AI Service Integration & Configuration Management

**As a** GMC participant,  
**I want** seamless integration with my configured AI services for analysis enhancement,  
**so that** I can access AI-powered strategy optimization using my personal credentials and preferences.

### Acceptance Criteria
1. Dynamic API service selection based on user's configured credentials
2. Automatic fallback between cloud APIs and local Ollama deployment based on availability
3. Configuration management interface for service preferences and deployment options
4. Integration testing tools for validating API connectivity and functionality
5. Service health monitoring with status displays and error reporting
6. Performance optimization features including caching and request batching

## Story 6.6: GMC Manual AI Knowledge Base Integration

**As an** AI system,  
**I want** comprehensive GMC Manual content stored as searchable knowledge base,  
**so that** I can provide game-specific expertise, rule-compliant recommendations, and accurate constraint validation based on official simulation specifications.

### Acceptance Criteria
1. NoSQL database integration (MongoDB) for GMC Manual content storage with structured knowledge sections
2. Automated parsing of GMC-Manual.pdf and GMC-manual_summary.md into searchable knowledge base format
3. AI context injection system providing GMC-specific rules, constraints, and mechanics to all AI recommendations
4. Real-time validation of AI recommendations against GMC parameter limits and game rules
5. Version-controlled knowledge base with manual update workflow for simulation rule changes
6. Administrative interface for uploading new manual versions with automatic content parsing and AI knowledge updates

## Story 6.7: User-Replaceable Manual Management System

**As a** system administrator,  
**I want** to easily update GMC Manual content when simulation rules change,  
**so that** AI recommendations remain accurate and compliant with current game specifications.

### Acceptance Criteria
1. Administrative upload interface for GMC-Manual.pdf and GMC-manual_summary.md replacement
2. Automatic version control with manual history tracking and rollback capabilities
3. Content validation ensuring uploaded files meet GMC Manual format requirements
4. Automated parsing and knowledge base update workflow triggered by manual uploads
5. Impact assessment showing which AI prompts and recommendations will be affected by manual changes
6. Testing interface for validating AI knowledge accuracy after manual updates

## Story 6.8: Knowledge Graph + RAG System Implementation

**As an** AI system,  
**I want** knowledge graph and RAG architecture for understanding GMC rule relationships and strategic interdependencies,  
**so that** I can provide context-aware recommendations based on complex reasoning rather than simple document lookup.

### Acceptance Criteria
1. Vector database (Weaviate) integration for semantic search of GMC concepts and strategies
2. Graph database (Neo4j) implementation for relationship traversal and causal reasoning
3. Knowledge graph construction from GMC Manual content and platform data relationships
4. RAG pipeline combining vector similarity search with graph relationship reasoning
5. Context-aware query system understanding interdependencies between decisions, constraints, and outcomes
6. Performance benchmarking showing improved recommendation relevance through relationship understanding

## Story 6.9: Intelligent LLM Model Orchestration System

**As an** LLM,  
**I want** to intelligently coordinate classical models based on context analysis,  
**so that** I can provide comprehensive GMC optimization combining strategic reasoning with precise mathematical calculations.

### Acceptance Criteria
1. Context analysis system determining which classical models are needed for specific optimization scenarios
2. Model coordination framework enabling LLM to request CatBoost sensitivity analysis, XGBoost optimization, and financial projections
3. Results synthesis combining classical model outputs with strategic insights from knowledge graph traversal
4. Model performance monitoring and automatic selection of optimal models based on accuracy and context
5. Unified response generation combining quantitative results with qualitative strategic explanations
6. Feedback loop enabling LLM to learn from model coordination effectiveness

## Story 6.10: Unified AI Data Pipeline & Training Infrastructure

**As a** data scientist,  
**I want** unified data pipeline providing both LLM and classical models access to training and monitoring data,  
**so that** all AI components can learn from platform usage patterns and maintain optimal performance.

### Acceptance Criteria
1. Centralized data lake with versioned access to GMC historical data, student interaction patterns, and performance outcomes
2. Training data pipeline supporting both classical model training and knowledge graph enrichment
3. Real-time monitoring dashboard tracking LLM reasoning quality and classical model accuracy
4. Automated model retraining triggered by performance degradation or new data availability
5. Academic compliance layer ensuring FERPA protection while enabling AI improvement
6. A/B testing framework comparing traditional recommendations vs knowledge graph-enhanced recommendations

## Story 6.11: Project-Scoped Persistent User-Specific AI Coaching System

**As a** GMC participant,  
**I want** persistent AI coaches that learn my strategic preferences independently for each project,  
**so that** I receive increasingly personalized GMC optimization advice that aligns with different strategic approaches and risk tolerances per project while maintaining isolation between experimental strategies.

### Acceptance Criteria
1. **Project-Scoped AI Instances**: Persistent AI coaching context per project with dedicated strategy profile storage and conversation memory isolated between projects
2. **Project-Specific Strategy Learning**: AI analyzes user communications and decision patterns independently within each project to build personalized optimization models per strategic approach
3. User preference tracking for risk tolerance, market focus, optimization style, and decision-making patterns
4. Performance tracking showing how AI recommendations improve in accuracy as it learns user preferences
5. Strategy evolution monitoring tracking how user approaches change over time with AI guidance
6. Cross-session continuity ensuring AI remembers previous conversations and strategic discussions

## Story 6.12: Conversational Chatbot Interface for Strategy Communication

**As a** GMC participant,  
**I want** to communicate with my AI coach through natural conversation to explain my strategies and request specific analysis,  
**so that** I can easily train my AI to understand my approach and delegate strategic analysis tasks.

### Acceptance Criteria
1. Rasa-based conversational interface with natural language understanding for strategic concepts
2. Strategy communication capabilities allowing users to explain preferences like "I prefer conservative cash management"
3. Task delegation interface enabling requests like "find best parameters for my risk-averse approach"
4. Conversation memory maintaining context across multiple interactions and sessions
5. Explanation capabilities where AI can justify recommendations and answer strategy questions
6. Strategy refinement through dialogue allowing users to correct AI understanding and provide feedback

## Story 6.13: AI Assistant Task Delegation & Execution

**As a** GMC participant,  
**I want** to delegate strategic analysis tasks to my AI coach and receive personalized results,  
**so that** I can efficiently explore optimization options that align with my strategic preferences without manual analysis.

### Acceptance Criteria
1. Task delegation framework supporting requests like "find optimal pricing strategy," "analyze market timing," "optimize resource allocation"
2. Intelligent model coordination where AI selects appropriate classical models based on task type and user strategy profile
3. Personalized results synthesis combining quantitative analysis with user's strategic context and preferences
4. Progress tracking for long-running analysis tasks with status updates and intermediate results
5. Results explanation showing how recommendations align with user's stated strategic preferences
6. Task history tracking enabling users to revisit previous analysis requests and results

## Story 6.14: Comprehensive User Data Integration for Personalized AI

**As an** AI coaching system,  
**I want** complete access to user's historical game data, decision patterns, and performance metrics,  
**so that** I can provide increasingly accurate personalized recommendations that learn from user's actual GMC gameplay and outcomes.

### Acceptance Criteria
1. Historical game data access including all user sessions, decisions, and outcomes for pattern analysis
2. Decision pattern recognition identifying user's typical strategic approaches and optimization priorities
3. Performance correlation analysis linking user decisions to outcomes to improve future recommendations
4. Model effectiveness tracking showing how well AI recommendations perform for specific user's style
5. Strategy evolution analysis tracking how user approaches change and improve over time
6. Privacy-compliant data usage ensuring user data serves only their personal AI instance with appropriate security controls

## Story 6.15: Architecture Documentation Synchronization

**As a** development team member,  
**I want** automated synchronization between intelligence directory implementation and architecture documentation,  
**so that** all AI infrastructure changes are properly documented and maintained consistently.

### Acceptance Criteria
1. Validation system ensuring intelligence directory structure matches architecture.md documentation
2. Automated detection of configuration changes requiring documentation updates
3. Development workflow integration requiring architecture updates for intelligence modifications
4. Compliance reporting for documentation synchronization status
5. Version control hooks preventing intelligence changes without corresponding documentation
6. Regular audit processes validating implementation-documentation alignment
