# AI Development Infrastructure: `intelligence` Directory

## Overview

The `intelligence` directory serves as the centralized hub for all AI-related development artifacts, configurations, and deployment resources in the GMC Dashboard project. This directory is **critical infrastructure** that enables the investment performance optimization, strategy tuning, and building block flexibility features.

**Core Purpose:** Provide a standardized, developer-friendly structure for managing external LLM API integrations (Anthropic Pro, OpenRouter), local AI deployments (Ollama), and classical ML models (CatBoost/XGBoost) while maintaining educational compliance and cost optimization.

## Complete Directory Structure

```
intelligence/
├── README.md                     # Comprehensive documentation (auto-generated)
├── debug-log.md                 # AI development tracking and performance logs
│
├── api-configs/                 # External API integration configurations
│   ├── anthropic.yaml           # Anthropic Pro API settings, prompt templates
│   ├── openrouter.yaml          # OpenRouter multi-model routing configuration
│   ├── ollama.yaml              # Local Ollama deployment and model settings
│   └── api-keys.env.example     # Environment variable template (NOT tracked in git)
│
├── classical-ml-models/         # Traditional ML model files and configurations
│   ├── catboost-models/         # Investment performance prediction models
│   │   ├── investment-performance.cbm
│   │   ├── parameter-sensitivity.cbm
│   │   └── model-config.yaml
│   ├── xgboost-models/          # Parameter optimization models
│   │   ├── constraint-optimization.json
│   │   └── sensitivity-analysis.json
│   └── scikit-models/           # Preprocessing and analysis models
│       ├── redundancy-detector.pkl
│       └── formula-classifier.pkl
│
├── llm-prompts/                 # LLM-specific prompts for external APIs
│   ├── strategy-optimization/   # Claude/GPT prompts for strategy analysis
│   │   ├── investment-performance-analysis.md
│   │   ├── competitive-strategy-recommendations.md
│   │   └── multi-scenario-comparison.md
│   ├── formula-analysis/        # LLM prompts for building block analysis
│   │   ├── excel-formula-explanation.md
│   │   ├── redundancy-detection.md
│   │   └── manual-adjustment-guidance.md
│   └── competitive-intel/       # LLM prompts for educational insights
│       ├── anonymous-benchmarking.md
│       └── success-pattern-analysis.md
│
├── deployment-configs/          # AI deployment configurations for different environments
│   ├── local-ollama/            # Privacy-first local deployment
│   │   ├── docker-compose.yml      # Ollama containerized deployment
│   │   ├── model-setup.sh          # Automated model installation
│   │   └── hardware-requirements.md # System requirements by model size
│   ├── cloud-api/               # External API deployment settings
│   │   ├── production.yaml         # Production API configuration
│   │   ├── staging.yaml            # Testing environment settings
│   │   └── cost-optimization.yaml  # Budget and usage controls
│   └── hybrid/                  # Mixed local/cloud deployment
│       ├── privacy-routing.yaml    # Data residency routing rules
│       └── fallback-strategy.yaml  # API failure handling
│
├── training-data/               # Sample data for classical ML training
│   ├── gmc-historical-samples/  # Anonymized historical GMC data
│   ├── synthetic-scenarios/     # Generated training scenarios
│   └── validation-datasets/     # Model testing and validation data
│
├── agent-configs/               # AI agent configurations and workflows
│   ├── strategy-tuning-agent.yaml
│   ├── building-block-agent.yaml
│   └── competitive-intel-agent.yaml
│
├── prompts/                     # Legacy prompt directory (being migrated to llm-prompts/)
│   └── strategy-optimization/   # Contains existing strategic documents
│       ├── architect-optimization-system-requirements-20250827.md
│       └── pm-strategic-clarification-alert-20250827.md
│
└── models/                      # Legacy model directory (deprecated, kept for reference)
```

## Core AI Integration Components

### 1. External API Integration (`api-configs/`)

**Purpose:** Manage external LLM API integrations with cost optimization, performance monitoring, and educational compliance.

**Key Configuration Files:**

**`anthropic.yaml`**: Anthropic Pro API configuration
- Primary model: Claude-3.5-Sonnet for complex strategy analysis
- Fallback model: Claude-3-Haiku for cost-sensitive operations
- Educational prompt templates optimized for business school contexts
- Cost management: <$0.10 per student per session
- FERPA compliance settings and data anonymization

**`openrouter.yaml`**: Multi-model routing for flexibility and cost optimization
- Intelligent model selection based on task complexity
- Cost-sensitive routing (Llama 3.1 8B for simple tasks, Claude for complex analysis)
- Budget controls and automatic fallback mechanisms
- Performance monitoring and model effectiveness tracking

**`ollama.yaml`**: Local deployment for privacy-sensitive institutions
- Hardware-optimized model selection (8B/13B/70B based on available resources)
- Complete data residency control for FERPA-sensitive institutions
- Docker containerization for easy deployment
- Academic calendar-aware maintenance scheduling

### 2. Classical ML Models (`classical-ml-models/`)

**Purpose:** Fast, reliable traditional ML for parameter sensitivity analysis and performance prediction.

**CatBoost Models** (`catboost-models/`):
- **Investment Performance Prediction**: Primary ranking calculation acceleration
- **Parameter Sensitivity Analysis**: <1 second impact analysis for all decision variables
- **Constraint Optimization**: Resource-aware recommendation generation

**XGBoost Models** (`xgboost-models/`):
- **Multi-Scenario Forecasting**: Strategy outcome prediction across different approaches
- **Competitive Intelligence**: Pattern recognition in successful strategies
- **Building Block Analysis**: Formula redundancy detection and optimization

**Scikit-Learn Models** (`scikit-models/`):
- **Data Preprocessing**: Feature engineering for GMC analysis parameters
- **Formula Classification**: Automated categorization of Excel formulas
- **Anomaly Detection**: Unusual parameter combinations and constraint violations

### 3. LLM Prompt Engineering (`llm-prompts/`)

**Purpose:** Optimized prompts for external LLM APIs with educational context and business accuracy.

**Strategy Optimization Prompts**:
- **Investment Performance Analysis**: Generate optimization recommendations with business rationale
- **Competitive Strategy Development**: Multi-scenario analysis with risk assessment
- **Educational Explanations**: Student-friendly optimization guidance with learning objectives

**Formula Analysis Prompts**:
- **Excel Formula Explanation**: Convert complex formulas to educational business explanations
- **Redundancy Detection**: Identify unused calculations with manual adjustment guidance
- **Building Block Optimization**: Suggest formula improvements while maintaining Excel equivalence

**Competitive Intelligence Prompts**:
- **Anonymous Benchmarking**: Generate insights without revealing team identities
- **Success Pattern Recognition**: Extract learnings from high-performing strategies
- **Market Analysis**: Provide competitive context with educational value

### 4. Deployment Configurations (`deployment-configs/`)

**Purpose:** Environment-specific AI deployment settings optimized for different institutional needs.

**Local Ollama Deployment** (`local-ollama/`):
- **Privacy-First**: Complete data residency control for FERPA compliance
- **Hardware Optimization**: Model selection based on available institutional resources
- **Cost Benefits**: Zero per-request costs after initial hardware investment
- **Academic Integration**: Campus network compatibility and authentication

**Cloud API Deployment** (`cloud-api/`):
- **Performance Optimization**: <2 second response times with global edge deployment
- **Cost Management**: Intelligent usage optimization and budget controls
- **Scalability**: Handle 50+ concurrent users during peak academic periods
- **Reliability**: 99.9% uptime with automatic failover mechanisms

**Hybrid Deployment** (`hybrid/`):
- **Data Classification**: Sensitive data processed locally, general analysis via APIs
- **Cost Optimization**: Balance between performance, cost, and privacy requirements
- **Institutional Flexibility**: Configure based on specific academic compliance needs
- **Performance Balancing**: Optimize response times across different AI processing methods

## External Service Integration Architecture

### API Failure Handling Architecture

**Failover Strategy:** Six-tier OpenRouter-primary failover cascade
- **Tier 1:** OpenRouter API (primary multi-model service)
- **Tier 2:** Anthropic Pro API (reasoning excellence)  
- **Tier 3:** OpenAI API (mathematical analysis)
- **Tier 4:** Google Gemini API (multimodal knowledge)
- **Tier 5:** DeepSeek API (cost-effective technical analysis)
- **Tier 6:** Local Ollama deployment (offline privacy capability)

**Implementation:** Circuit breaker pattern with 3-second timeout, automatic service health checks, and intelligent model routing logic with cost optimization.

### API-Key-Only Authentication Architecture

**Rasa Integration:** Conversation management with API-key-only authentication patterns through configured actions and API connectors. No username storage required - only encrypted API keys with AES-256-GCM encryption.

**Provider Detection:** Automatic capability identification per API key with real-time service status validation and model availability checking.

**Security Model:** Complete API-key-only workflow ensuring institutional data privacy while supporting multi-provider AI access patterns.

### Mock Service Architecture

**Development Environment:** Complete mock service layer using fixtures directory with multi-provider simulation supporting all 6 AI providers (OpenRouter, Anthropic, OpenAI, Gemini, DeepSeek, Ollama).

**Testing Framework:** Automated mock responses with scenario-based AI coaching simulation for comprehensive provider failover testing and model switching validation.

**Data Management:** Seeded databases with comprehensive GMC analysis scenarios supporting provider failover testing, context preservation validation, and conversation continuity across model switches.

## Developer Integration Guide

### Quick Setup for Developers

```python
# Example: AI service integration
from gmc_dashboard.intelligence import AIStrategyService

# Initialize with configuration from intelligence/api-configs/
ai_service = AIStrategyService.from_config(
    config_path="intelligence/api-configs/anthropic.yaml",
    fallback_config="intelligence/api-configs/ollama.yaml"
)

# Generate investment performance optimization recommendations
recommendations = await ai_service.generate_strategy_recommendations(
    current_parameters=analysis_session.parameters,
    constraints=analysis_session.constraints,
    competitive_context=competitive_intelligence.get_anonymous_context(),
    educational_level="graduate_mba"  # Adjust explanation complexity
)

# Classical ML parameter sensitivity analysis
sensitivity_analysis = ai_service.analyze_parameter_sensitivity(
    parameters=current_parameters,
    model_path="intelligence/classical-ml-models/catboost-models/parameter-sensitivity.cbm"
)
```

### Configuration Loading Pattern

```python
# Automatic configuration detection and fallback
class AIConfigManager:
    def __init__(self):
        self.configs = self._load_ai_configs()
    
    def _load_ai_configs(self):
        """Load AI configurations with intelligent fallback"""
        return {
            'anthropic': self._load_yaml('intelligence/api-configs/anthropic.yaml'),
            'openrouter': self._load_yaml('intelligence/api-configs/openrouter.yaml'),
            'ollama': self._load_yaml('intelligence/api-configs/ollama.yaml')
        }
    
    def get_optimal_config(self, task_complexity='medium', privacy_level='standard'):
        """Select best AI configuration based on requirements"""
        if privacy_level == 'high':
            return self.configs['ollama']
        elif task_complexity == 'low':
            return self.configs['openrouter']  # Cost optimization
        else:
            return self.configs['anthropic']   # Performance optimization
```

## Non-Technical User Configuration

### UI-Based Configuration Interface

The GMC Dashboard provides a user-friendly configuration interface accessible via the admin panel:

**Navigation**: Admin → AI Configuration → Setup Wizard

**Configuration Steps**:
1. **Choose Deployment Mode**:
   - 🌍 **Cloud APIs** (Anthropic Pro + OpenRouter) - Best performance, requires API keys
   - 🏠 **Local AI** (Ollama) - Complete privacy, requires hardware
   - 🔄 **Hybrid** - Balance of performance and privacy

2. **API Key Configuration** (if using cloud APIs):
   - Anthropic Pro API key (primary recommendations)
   - OpenRouter API key (cost optimization)
   - Budget limits and usage alerts

3. **Local Deployment Setup** (if using Ollama):
   - Hardware assessment (automatic)
   - Model recommendation (8B/13B/70B based on resources)
   - Installation guidance (automated scripts)

4. **Performance Optimization**:
   - Response time preferences
   - Cost vs. performance trade-offs
   - Educational explanation verbosity

5. **Privacy & Compliance**:
   - Data residency requirements
   - FERPA compliance level
   - Audit logging preferences

### Automated Setup Scripts

For technical users, automated setup is available:

```bash
# Quick setup for cloud APIs
./scripts/setup-ai-cloud.sh --anthropic-key=your_key --openrouter-key=your_key

# Local Ollama deployment
./scripts/setup-ai-local.sh --model-size=8b --privacy-mode=high

# Hybrid deployment
./scripts/setup-ai-hybrid.sh --config=privacy-balanced
```

## Cost Management and Optimization

### Budget Control Framework

**Daily Budget Limits**:
- **Small Institution** (<500 students): $5-10/day
- **Medium Institution** (500-2000 students): $15-30/day  
- **Large Institution** (2000+ students): $50-100/day

**Cost Optimization Strategies**:
1. **Classical ML Preprocessing**: Reduce LLM API calls by 70%
2. **Intelligent Caching**: 24-hour result caching for similar scenarios
3. **Model Routing**: Use cheaper models for simple tasks
4. **Batch Processing**: Group similar requests for efficiency
5. **Local Fallback**: Automatic switch to Ollama when budgets are exceeded

**Cost Monitoring Dashboard** (Admin Interface):
- Real-time usage tracking
- Per-student cost analysis
- Budget alerts and notifications
- ROI analysis (time saved vs. AI costs)
- Comparative analysis (cloud vs. local deployment costs)

## Privacy and Compliance Framework

### FERPA Compliance Levels

**Level 1 - Standard**: External APIs with data anonymization
- Student IDs replaced with anonymous tokens
- No personally identifiable information in API calls
- Audit trail maintained for all AI interactions

**Level 2 - Enhanced**: Hybrid processing with sensitive data routing
- Personal data processed locally only
- General strategy analysis via external APIs
- Institutional boundary enforcement

**Level 3 - Maximum**: Local-only AI processing
- Complete data residency control
- No external API calls for student data
- Full institutional sovereignty over AI processing

### Data Protection Measures

**External API Calls**:
- Automatic data anonymization
- Request/response logging (optional)
- Encryption in transit and at rest
- Geographic data residency controls

**Local Processing**:
- No data leaves institutional boundaries
- Local model fine-tuning on institutional data
- Complete audit trail control
- Academic calendar-aware processing

## Performance Monitoring and Optimization

### Key Performance Indicators

**Response Time Metrics**:
- Classical ML Analysis: <1 second (target)
- External LLM APIs: <2 seconds (target)
- Local Ollama: <10 seconds (target)
- End-to-end optimization: <3 seconds (target)

**Quality Metrics**:
- Recommendation acceptance rate: >70%
- Investment performance improvement: >15%
- User satisfaction score: >4.5/5
- Educational value rating: >4.0/5

**Cost Efficiency Metrics**:
- Cost per student per session: <$0.10
- API usage optimization: >50% reduction via ML preprocessing
- Budget adherence: >95% within limits
- ROI measurement: Time saved vs. AI costs

### Monitoring Dashboard

The AI system provides comprehensive monitoring accessible via:
**Admin Interface → AI Analytics → Performance Dashboard**

**Real-time Monitoring**:
- API response times and success rates
- Model performance and accuracy metrics
- Cost tracking and budget utilization
- User engagement and satisfaction metrics

**Historical Analysis**:
- Performance trends over academic periods
- Seasonal usage patterns and optimization opportunities
- Model effectiveness evolution
- Cost-benefit analysis and ROI tracking

## Troubleshooting and Support

### Common Issues and Solutions

**API Connection Issues**:
- Automatic fallback to secondary providers
- Local Ollama deployment as ultimate fallback
- Network connectivity diagnostics and retry mechanisms

**Performance Issues**:
- Model optimization and caching strategies
- Hardware resource monitoring and scaling recommendations
- Request batching and queue management

**Cost Overruns**:
- Automatic budget enforcement and alerts
- Usage pattern analysis and optimization recommendations
- Migration guidance to more cost-effective deployment modes

**Privacy Concerns**:
- Data audit trails and compliance reporting
- Migration to local-only processing
- Institutional data residency verification

### Support Resources

**Developer Documentation**: `/docs/ai-integration/`
- API integration examples
- Classical ML model training guides
- Prompt engineering best practices
- Deployment and scaling recommendations

**User Guides**: `/docs/user-guides/ai-setup/`
- Non-technical setup instructions
- Configuration best practices
- Troubleshooting common issues
- Performance optimization tips

**Video Tutorials**: Available in admin interface
- Step-by-step setup walkthroughs
- Feature demonstration and use cases
- Best practices for educational contexts
- Cost optimization strategies

---

## Summary: `intelligence` Directory as Critical Infrastructure

The `intelligence` directory represents the **backbone of intelligent features** in the GMC Dashboard, providing:

✅ **Developer Productivity**: Standardized structure and configuration management  
✅ **Non-Technical Accessibility**: UI-based setup and automated deployment options  
✅ **Cost Optimization**: Intelligent usage patterns and budget controls  
✅ **Privacy Flexibility**: From cloud APIs to complete local processing  
✅ **Educational Compliance**: FERPA-aware configurations and audit capabilities  
✅ **Performance Reliability**: Sub-second classical ML + <2 second LLM recommendations  

This infrastructure enables the **investment performance optimization**, **AI strategy tuning**, and **building block flexibility** that transforms GMC Dashboard from a simple Excel replacement into an intelligent educational technology platform.

## 📋 **CRITICAL: Documentation Synchronization Requirement**

**Mandatory Process**: All changes to the `intelligence` directory structure, configurations, or functionality **MUST** be documented in this architecture.md file to ensure consistency across development teams and AI agents.

**Synchronization Requirements**:
- ✅ **New Files/Directories**: Update directory structure documentation
- ✅ **Configuration Changes**: Update corresponding configuration sections
- ✅ **API Integration Changes**: Update technology stack and component descriptions
- ✅ **Setup Process Changes**: Update setup and deployment instructions
- ✅ **Performance Requirements**: Update monitoring and performance sections
- ✅ **Prompt Template Changes**: Update AI integration examples and documentation

**Implementation Process**:
1. **Before intelligence Changes**: Review current architecture documentation
2. **During intelligence Changes**: Document design decisions in `intelligence/debug-log.md`
3. **After intelligence Changes**: Update corresponding sections in `architecture.md`
4. **Validation**: Ensure architecture accurately reflects actual `intelligence` implementation

**Responsibility**: All developers, architects, and AI agents modifying the `intelligence` directory must maintain documentation synchronization.

**Compliance Check**: Regular audits will verify `intelligence` implementation matches architecture documentation.

**Next Phase**: Implementation teams should begin with the automated setup scripts and UI configuration interface to ensure seamless adoption across diverse institutional environments.
