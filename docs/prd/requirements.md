# Requirements

## Functional Requirements

**FR1:** The system shall replicate the complete interdependent formula architecture from `gmc_analysis.xlsx` with exact calculation accuracy across Cost of Production, Payments & Payables, Receipts & Receivables, Decision Sheet, and Investment Performance sheets.

**FR2:** The system shall provide real-time cross-sheet calculation updates where changes in any parameter instantly propagate through all dependent formulas across sheets.

**FR3:** The system shall implement visual constraint validation with "battery indicator" displays showing remaining capacity for skilled workers, machine hours, and financial resources.

**FR4:** The system shall support GMC quarterly report import functionality that automatically populates baseline parameters across all interdependent analysis sheets.

**FR5:** The system shall provide interactive sliders and controls for all GMC decision variables with immediate visual feedback on constraint impacts.

**FR6:** The system shall calculate and display Investment Performance metrics in real-time as the ultimate winning condition across all decisions.

**FR7:** The system shall implement directed acyclic graph (DAG) calculation ordering to prevent circular dependencies and ensure proper formula execution sequence.

**FR8:** The system shall validate all constraint violations in real-time and prevent submission of impossible decisions (e.g., exceeding capacity limits).

**FR9:** The system shall provide toggleable "learning mode" that reveals calculation logic and formula explanations for educational transparency.

**FR10:** The system shall implement scenario comparison functionality allowing parallel analysis of multiple strategies without affecting main analysis.

**FR11:** The system shall provide one-click decision export functionality compatible with official GMC submission portal formats.

**FR12:** The system shall implement modular architecture with separate calculation engine, state management, and UI components.

**FR13:** The system shall implement granular undo/redo functionality allowing users to reverse individual parameter changes or batch related modifications without affecting unrelated analysis components.

**FR14:** The system shall provide automatic state management with snapshots every 30 seconds and before major parameter changes, maintaining analysis history for session duration.

**FR15:** The system shall implement three-tier constraint validation (warning/caution/violation) with appropriate UI feedback patterns and guided resolution steps for each severity level.

**FR16:** The system shall provide analysis history timeline with visual progression indicators, annotation capabilities, and one-click reversion to any previous state.

**FR17:** The system shall implement contextual help system with embedded GMC business logic explanations accessible through UI tooltips and help panels.

**FR18:** The system shall provide interactive popup/modal windows with intuitive manipulation capabilities including zoom controls (mouse wheel/pinch gestures), pan functionality (click and drag within content area), window repositioning (drag by title bar), and resize handles (corner/edge drag) for optimal multi-sheet analysis viewing.

**FR19:** The system shall support GMC file naming conventions and workflow management including:
- **History Files**: Recognition of "Hst" prefix followed by year (Y16, Y18, Y14, etc.) and quarter (Q1, Q2, Q3, Q4) format
- **Game Report Files**: Recognition of "W" prefix followed by 6-digit series numbers for gameplay reports
- **File Type Distinction**: Automatic categorization and processing based on file naming patterns
- **Chronological Organization**: Automatic sorting and timeline placement based on extracted date information

**FR20:** The system shall provide intuitive file management capabilities including:
- **Drag-and-Drop Reordering**: Users can reorganize history files and reports through intuitive drag-and-drop interface
- **Historical Timeline Management**: Visual timeline editor for adjusting chronological sequence of uploaded files
- **Flexible File Validation**: Support for variable history lengths (minimum 1 quarter, recommended 5 quarters) with appropriate baseline calculations
- **Progress Visualization**: Charts and graphs showing improvement and progress across available historical periods and gameplay reports

**FR21:** The system shall provide comprehensive trend analysis and data combination capabilities including:
- **Cross-Quarter Trend Analysis**: Combine similar metrics from different quarters to build performance trend charts
- **Historical-to-Current Integration**: Seamless data combination across history files and current gameplay reports  
- **Multi-Dimensional Trending**: Track performance evolution across financial, operational, and strategic dimensions
- **Comparative Analysis**: Side-by-side comparison of metrics between historical periods and current decisions
- **Pattern Recognition**: Identify recurring trends and anomalies across quarters for strategic insight generation

**FR22:** The system shall provide robust error handling and data validation including:
- **File Format Resilience**: Graceful handling of corrupted Excel files, missing sheets, or unexpected data structures with specific error messages
- **Data Recovery Mechanisms**: Automatic backup and recovery strategies when calculations fail or sessions are interrupted
- **Version Compatibility**: Support for different GMC report format versions with automatic detection and appropriate processing
- **Validation Reporting**: Comprehensive error logs and data quality reports for troubleshooting file upload issues

**FR23:** The system shall support team collaboration workflows including:
- **Shared Session Management**: Multiple team members can access the same analysis session with real-time synchronization
- **Role-Based Access Control**: Configurable permissions for different team members to control specific analysis areas
- **Conflict Resolution**: Intelligent handling of simultaneous edits with merge strategies and change notification systems
- **Collaborative Decision Tracking**: Team annotation system with decision rationale capture and change attribution

**FR24:** The system shall provide individual user API key management where each user can securely store their own AI service credentials (Anthropic Pro, OpenRouter) in PostgreSQL with encrypted storage linked to user accounts using AES-256-GCM encryption and user_id relationships.

**FR25:** The system shall implement comprehensive user-specific API key workflows including:
- **Personal API Key Registration**: User interface for adding and validating individual AI service credentials
- **Encrypted Database Storage**: PostgreSQL user_api_credentials table with institution_id relationships and row-level security
- **Runtime Security Model**: API keys loaded directly from encrypted user profiles at runtime - no .env files or static configuration storage
- **Individual Budget Controls**: Per-user daily ($10) and monthly ($300) budget limits with usage tracking
- **Key Management Interface**: User-controlled API key rotation, activation/deactivation, and usage monitoring

**FR26:** The system shall implement comprehensive `intelligence` directory infrastructure within the `gmc-dashboard/` application directory providing centralized management of AI-related development artifacts including:
- **API Configurations** (`api-configs/`): Service-specific configuration files (anthropic.yaml, openrouter.yaml, ollama.yaml, security-integration-reference.yaml) with database-managed credential integration
- **Classical ML Models** (`classical-ml-models/`): Organized model storage with catboost-models/, xgboost-models/, and scikit-models/ subdirectories for investment performance prediction and parameter sensitivity analysis
- **LLM Prompt Templates** (`llm-prompts/`): Structured prompt libraries with strategy-optimization/, formula-analysis/, and competitive-intel/ subdirectories containing markdown-based prompt templates
- **Deployment Configurations** (`deployment-configs/`): Multi-environment deployment with local-ollama/, cloud-api/, hybrid/, and ui-configuration-interface.yaml for flexible institutional deployment
- **Training Data** (`training-data/`): Sample data management with gmc-historical-samples/, synthetic-scenarios/, and validation-datasets/ subdirectories for model training and evaluation
- **AI Agent Configurations** (`agent-configs/`): YAML configurations for strategy-tuning-agent, building-block-agent, and competitive-intel-agent with complete parameter specifications
- **Legacy Support**: Maintained prompts/ and models/ directories for backward compatibility during migration phases
- **Development Documentation**: README.md and debug-log.md providing AI development tracking and component documentation
- **Directory Structure**: Complete `intelligence/` infrastructure located at `gmc-dashboard/intelligence/` as integral part of application architecture enabling AI-powered analysis capabilities
- **Architectural Governance**: Core directory structure defined by architecture team with established patterns - developers may create subdirectories within defined patterns subject to code review validation, ensuring structural consistency while maintaining development velocity
- **Setup Responsibility**: AI infrastructure setup is handled during development phase by developers, with end users only required to provide API keys through user interface - local Ollama users require minimal setup configuration while cloud API users simply register their credentials

**FR27:** The system shall maintain comprehensive project structure synchronization requirements where all changes to core directory structure (including intelligence infrastructure) must be documented in architecture.md to ensure consistency across development teams and automated deployment processes, with architectural governance defining established patterns that developers follow when creating subdirectories, validated through code review processes, and any architectural pattern changes requiring corresponding PRD updates to maintain specification accuracy.

**FR28:** The system shall integrate GMC Manual content as AI knowledge base using NoSQL database storage for GMC-Manual.pdf and GMC-manual_summary.md, enabling AI systems to provide game-specific expertise, rule-compliant recommendations, and accurate constraint validation based on official simulation specifications.

**FR29:** The system shall provide user-replaceable GMC Manual management allowing administrators to upload updated versions of GMC-Manual.pdf and GMC-manual_summary.md with automatic versioning, content parsing, and AI knowledge base updates to ensure recommendations remain current with simulation rule changes.

**FR30:** The system shall implement knowledge graph + RAG architecture using vector database (Weaviate) for semantic search and graph database (Neo4j) for relationship reasoning, enabling LLM to understand complex interdependencies between GMC rules, market dynamics, and strategic decisions rather than simple document lookup.

**FR31:** The system shall provide intelligent LLM orchestration of classical models where the LLM analyzes context, determines required calculations, coordinates CatBoost/XGBoost models for parameter optimization, and synthesizes results with GMC-specific strategic recommendations based on graph traversal insights.

**FR32:** The system shall implement unified data pipeline providing both LLM and classical models access to training data, evaluation metrics, and real-time monitoring capabilities through centralized data lake with version control and academic compliance tracking.

**FR33:** The system shall provide persistent user-specific AI coaching instances as an optional analysis method where each user can choose to activate a dedicated AI coach that learns their strategic preferences, decision patterns, and optimization goals, maintaining personalized strategy profiles that evolve with continued usage and user feedback while preserving access to manual analysis workflows.

**FR34:** The system shall implement conversational chatbot interface using open source Rasa framework enabling users to communicate strategies, request analysis tasks, receive explanations, and refine AI understanding through natural language dialogue with conversation memory and context retention.

**FR35:** The system shall provide AI assistant capabilities allowing users to delegate strategic analysis tasks such as "find best parameters for conservative strategy," "analyze competitor scenarios," or "optimize for my risk preferences," with AI coordinating appropriate classical models and knowledge graph analysis to deliver personalized results.

**FR36:** The system shall ensure user-specific AI instances have comprehensive access to all user's historical game data, decision patterns, model performance metrics, and strategy evolution to provide increasingly accurate and personalized recommendations that align with individual user goals and preferences.

**FR37:** The system shall provide competitive benchmarking and performance context including:
- **Anonymous Benchmarking**: Performance comparison against simulation group averages without revealing individual team identities
- **Relative Performance Indicators**: Clear visualization of team ranking and performance gaps within competitive context
- **Best Practice Insights**: Pattern recognition from successful strategies across simulation groups (instructor-approved sharing)
- **Performance Distribution Analytics**: Understanding of team performance relative to class distribution and historical benchmarks

**FR38:** The system shall provide team/company identification and selection functionality including:
- **Company Selection Interface**: Users can select their team identity (Company 1, Company 2, etc.) from available companies in their simulation group
- **Group Information Integration**: Team selection integrates with group information data showing all companies in the simulation group
- **Multi-Company Data Processing**: System processes uploaded files and displays data specific to the selected company while showing competitive context
- **Company-Specific Analysis**: All analysis and calculations reflect the selected company's perspective and data while maintaining competitive benchmarking capabilities

**FR39 (Post-MVP):** The system shall provide automation and integration capabilities including:
- **N8n Integration**: Workflow automation support for advanced users requiring automated analysis tasks, report generation, and decision pipeline processing
- **OpenAPI Compatibility**: RESTful API endpoints following OpenAPI specifications for third-party integrations and custom automation workflows  
- **Webhook Support**: Event-driven notifications and data exchange capabilities for external system integration
- **Automation Templates**: Pre-built N8n workflow templates for common GMC analysis automation scenarios

**FR40:** The system shall provide comprehensive educational analytics including student competency tracking, optimization pattern recognition, constraint understanding measurement, and team collaboration effectiveness monitoring.

**FR41:** The system shall implement faculty dashboard with class performance overviews, individual student progress tracking, learning objective achievement metrics, and intervention alert systems for academic support.

**FR42:** The system shall support adaptive learning features with personalized difficulty scaling, targeted learning resource recommendations, peer learning opportunity identification, and early warning systems for struggling students.

## Non-Functional Requirements

**NFR1:** The system shall provide tiered performance response based on operation complexity:
- **Tier 1 - Basic Calculations**: Sub-500ms for direct parameter changes and Excel formula calculations
- **Tier 2 - Cross-Sheet Updates**: Sub-2 seconds for interdependent calculations across all GMC sheets  
- **Tier 3 - AI Analysis**: 3-10 seconds for classical model processing and basic AI recommendations
- **Tier 4 - Advanced AI Processing**: 10-30 seconds for complex knowledge graph analysis and comprehensive strategy optimization

**NFR2:** The system shall support 50+ concurrent users per simulation group without performance degradation.

**NFR3:** The system shall maintain 100% mathematical equivalence validated against official GMC test cases.

**NFR4:** The system shall be accessible via modern browsers (Chrome, Firefox, Safari, Edge) with responsive design for desktop and tablet usage.

**NFR5:** The system shall implement modular architecture enabling expansion from production analysis to full GMC strategic planning without code refactoring.

**NFR6:** The system shall implement comprehensive educational security compliance including:
- **FERPA-Compliant Data Protection**: Row-level security with institutional boundaries and student data isolation
- **User API Credential Security**: AES-256-GCM encryption for individual user AI service credentials with PostgreSQL storage
- **Institution-Level Security**: Complete data isolation between institutions with comprehensive audit trails
- **Budget Protection Controls**: Automated enforcement of per-user API usage limits with real-time monitoring and cost prevention
- **Multi-Database Backup Strategy**: Comprehensive encrypted backup and recovery strategy across all six database types (PostgreSQL, Neo4j, Weaviate, MongoDB, Redis, ClickHouse) with automated failover capabilities, point-in-time recovery for transactional systems, and FERPA-compliant data archiving with institutional boundary preservation. Backup encryption uses AES-256 with separate key management for each database type, ensuring complete data protection during backup operations, transport, and long-term storage while maintaining the ability to restore individual institutional contexts without cross-contamination.

**NFR7:** The system shall achieve intuitive UI design standards with minimal learning curve for Excel users.

**NFR8:** The system shall maintain a complete audit trail for academic integrity verification, logging all parameter changes, strategic decisions, and AI usage analytics to provide a comprehensive record of the user's decision-making process.

**NFR9:** The system shall support offline-capable analysis for classroom environments with unreliable internet connectivity.

**NFR10:** The system shall achieve 85% reduction in analysis time (from 240 minutes to 45 minutes) as primary success metric.

**NFR11:** The system shall maintain undo/redo state history with minimal memory overhead, supporting minimum 50 operations per analysis session.

**NFR12:** The system shall provide immediate visual feedback (sub-500ms) for all constraint validation state changes with clear indication of validation level, including progress indicators for longer-running AI analysis operations with estimated completion times and cancellation options.

**NFR13:** The system shall implement keyboard accessibility with standard shortcuts (Ctrl+Z/Ctrl+Y) and complete tab navigation through all interactive elements.

**NFR14:** The system shall provide data persistence and archiving capabilities including analysis session retention during active simulation periods, automatic cleanup of expired sessions, and optional long-term storage for institutional learning purposes.

**NFR15:** The system shall support offline-capable operation with local data storage, automatic synchronization when connectivity is restored, and graceful degradation of features requiring real-time collaboration during network interruptions.

**NFR16:** The system shall maintain data isolation between different simulation groups and academic periods while enabling instructor-controlled cross-group analytics and best practice sharing capabilities.

**NFR17:** The system shall implement progressive enhancement architecture with HTML-first components that provide universal functionality and enhance based on device capabilities.

**NFR18:** The system shall achieve comprehensive WCAG 2.1 AA accessibility compliance with enhanced educational features including contextual audio descriptions and keyboard-optimized analytical workflows.

**NFR19:** The system shall provide educational analytics framework with faculty dashboard capabilities for competency assessment, learning progress tracking, and intervention triggers.

**NFR20:** The system shall support device role specialization with mobile optimized for coordination and status monitoring, tablet for collaborative review and presentation, and desktop for full analytical workflows.

**NFR21:** The system shall implement Team Unicorn brand standards with sophisticated animations (200-400ms duration), professional color palette, and polished interaction patterns that maintain educational focus.
