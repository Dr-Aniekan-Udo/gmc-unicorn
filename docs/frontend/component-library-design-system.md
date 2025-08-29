# Component Library / Design System

**Design System Approach:** Educational-Professional Hybrid Component Architecture built on HTML-first progressive enhancement principles

## Core Components

### 0. Project Management Foundation Components

#### 0.1 Multi-Project Dashboard Component
- **Base:** Grid view of all user projects with status cards, last accessed timestamps, and quick actions
- **Enhancement:** Project health indicators, cross-project analytics, bulk operations, and project templates
- **Mobile:** Condensed project list with swipe actions for common operations
- **Project Context:** Global overview transcending individual project boundaries

#### 0.2 Project Creation Wizard Component
- **Base:** Step-by-step project setup with template selection and initial configuration
- **Enhancement:** Smart defaults based on user history, template customization, and team invitation workflows
- **Mobile:** Simplified project creation with essential settings only
- **Strategy Focus:** Project purpose selection (competitive analysis, strategy experimentation, team collaboration)

#### 0.3 Project Context Switcher Component
- **Base:** Always-visible dropdown showing current project with quick switching capability
- **Enhancement:** Recent projects, favorite projects, project search, and context preview
- **Mobile:** Slide-out project selector with search and filtering
- **Isolation Assurance:** Clear visual indication of current project scope and data boundaries

#### 0.4 Project-Scoped Navigation Component
- **Base:** Navigation system that adapts to current project context and available features
- **Enhancement:** Breadcrumb integration, project-specific shortcuts, and context-aware menu organization
- **Mobile:** Collapsible navigation with project-specific quick actions
- **Microservice Integration:** Service-specific navigation states and loading patterns

### 1. Investment Performance Dashboard Component (Project-Scoped)
- **Base:** Large numerical display with competitive ranking and performance score visualization within project context
- **Enhancement:** Real-time performance updates (<1 second), competitive positioning overlay, trend analysis with project-specific forecasting
- **Mobile:** Condensed performance scorecard with swipeable competitive context within project
- **Strategy Focus:** Performance impact preview for parameter changes, optimization opportunity highlights
- **Project Isolation:** All performance data and calculations scoped to current project only

### 2. Parameter Sensitivity Slider Component
- **Base:** Interactive slider with immediate visual feedback and impact indication
- **Enhancement:** Investment performance gradient visualization (red→yellow→green zones), constraint-aware optimization suggestions, sensitivity analytics
- **Mobile:** Touch-optimized controls with haptic feedback for constraint boundaries
- **AI Integration:** Smart parameter recommendations with performance improvement forecasts
**Multi-Provider Support:** Visual indicators showing active LLM provider with capability-specific recommendations

### 3. Strategy Comparison Matrix Component
- **Base:** Side-by-side scenario comparison with key metrics and performance indicators
- **Enhancement:** Interactive scenario branching, drag-and-drop strategy elements, performance forecasting with confidence intervals
- **Mobile:** Swipeable scenario cards with condensed comparison metrics
- **Collaborative:** Team strategy sharing with individual contribution attribution

### 4. Competitive Intelligence Panel Component
- **Base:** Anonymous benchmarking display with performance distribution and ranking context
- **Enhancement:** Best practices insights, successful strategy pattern recognition, market trend analysis
- **Mobile:** Notification-style competitive alerts with performance gap indicators
- **Privacy-Balanced:** Complete anonymization with meaningful competitive context

### 5. Building Block Editor Component
- **Base:** Formula transparency interface with Excel equivalence validation
- **Enhancement:** Redundancy detection, user-friendly adjustment workflows, performance impact analysis of modifications
- **Mobile:** Simplified formula editing with guided optimization suggestions
- **Educational:** Formula explanation mode with business logic context and calculation transparency

### 6. AI Strategy Recommendation Engine Component
- **Base:** Smart suggestion panel with constraint-aware optimization recommendations
- **Enhancement:** Explainable AI with recommendation rationale, historical success pattern analysis, performance improvement forecasting
- **Mobile:** Contextual recommendation notifications with one-tap implementation
- **Learning Integration:** Continuous improvement based on strategy effectiveness and user feedback
**Provider Awareness:** Different AI providers offer specialized capabilities (conversation, analysis, recommendations) with transparent switching

### 7. Multi-Provider LLM Selection Component
- **Base:** Provider selection interface supporting OpenAI, Anthropic, Gemini, DeepSeek, OpenRouter, and Ollama
- **Enhancement:** Real-time budget tracking per provider, API key status indicators, capability comparison
- **Mobile:** Simplified provider switcher with budget alerts and usage notifications
- **Integration:** User credential management with AES-256-GCM encryption and automated budget enforcement
- **Usage Context:** Shows which provider is actively responding with provider-specific capabilities

**Component Interface Pattern:**
```typescript
interface LLMProviderSelectorProps {
  currentProvider: 'openai' | 'anthropic' | 'gemini' | 'deepseek' | 'openrouter' | 'ollama';
  onProviderChange: (provider: string) => void;
  userApiKeys: Record<string, boolean>; // Which providers user has configured
  budgetStatus: Record<string, BudgetInfo>; // Budget remaining per provider
}
```

### 8. AI Coaching Conversational Interface Component (Project-Scoped)
- **Base:** Chat-style interface with natural language strategy communication within project context
- **Enhancement:** Project-scoped persistent learning, project-specific strategy preferences, contextual help integration
- **Mobile:** Voice input support, quick response buttons, project-aware coaching alerts
- **Educational Integration:** GMC Manual knowledge base, constraint explanations, formula transparency
- **Project Isolation:** Separate AI coaching instances per project with independent conversation memory and strategy learning
- **Multi-Service Integration:** Connects to conversation-service via coaching-orchestrator with provider transparency

**Component Interface Pattern:**
```typescript
interface ConversationInterfaceProps {
  projectId: string;
  conversationHistory: ConversationMessage[];
  onSendMessage: (message: string) => void;
  llmProvider: string; // Shows which LLM is responding
  isTyping: boolean;
}
```

### 9. Knowledge Search Component (AI-Powered)
- **Base:** Intelligent GMC knowledge retrieval with vector search capabilities
- **Enhancement:** Project-scoped search results, contextual knowledge recommendations, search result ranking
- **Mobile:** Voice search input, condensed knowledge cards, quick knowledge application
- **Integration:** Connects to vector-search-service via coaching-orchestrator for project-specific knowledge
- **Educational Context:** GMC Manual integration with formula explanations and best practices

**Component Interface Pattern:**
```typescript
interface KnowledgeSearchProps {
  projectId: string;
  searchQuery: string;
  onSearch: (query: string) => void;
  searchResults: GMCKnowledgeResult[];
  isSearching: boolean;
}
```

### 10. ML Recommendations Component (Strategy Intelligence)
- **Base:** Machine learning-powered parameter optimization suggestions with performance forecasting
- **Enhancement:** Explainable AI recommendations, confidence intervals, historical success pattern analysis
- **Mobile:** Recommendation cards with swipe actions, simplified recommendation application
- **Integration:** Connects to ml-recommendation-service via coaching-orchestrator for intelligent strategy suggestions
- **Strategy Focus:** Investment performance optimization with constraint-aware recommendations

**Component Interface Pattern:**
```typescript
interface MLRecommendationsProps {
  projectId: string;
  currentParameters: GMCParameters;
  recommendations: MLRecommendation[];
  onApplyRecommendation: (recommendation: MLRecommendation) => void;
  onRequestAnalysis: () => void;
}
```

### 11. Unified AI Coach Interface (Orchestrated)
- **Base:** Single interface combining conversation, knowledge search, and ML recommendations seamlessly
- **Enhancement:** Intelligent service coordination, contextual capability switching, unified user experience
- **Mobile:** Tabbed interface for different AI capabilities with contextual mode switching
- **Backend Integration:** Coaching-orchestrator provides unified interface while coordinating multiple AI services
- **User Experience:** One AI coach interface with transparent multi-service coordination

**Component Interface Pattern:**
```typescript
interface AICoachInterfaceProps {
  projectId: string;
  // Combines all AI capabilities in single interface
  // Backend: coaching-orchestrator coordinates all services
  // Frontend: Single component with multiple capability modes
}
```

### 12. Educational Analytics Dashboard Component (Faculty)
- **Base:** Class performance overview with individual student progress tracking
- **Enhancement:** Competency assessment visualization, intervention alerts, learning objective alignment
- **Mobile:** Key metrics dashboard, quick intervention tools, mobile-optimized faculty interface
- **Analytics Integration:** Student engagement tracking, performance correlation analysis, adaptive learning recommendations

### 13. Individual API Key Management Component
- **Base:** Secure credential storage interface with budget controls
- **Enhancement:** Usage monitoring, service selection, real-time budget tracking with automated enforcement
- **Mobile:** Quick budget checks, usage alerts, simplified key management interface
- **Security Integration:** AES-256-GCM encryption, institutional compliance, audit logging

### 14. Advanced File Management Timeline Component
- **Base:** Drag-and-drop file organization with GMC naming pattern recognition
- **Enhancement:** Cross-quarter trend analysis, historical data combination, progress visualization
- **Mobile:** Touch-optimized file reordering, simplified timeline view, quick file validation
- **Intelligence Integration:** Automatic chronological sorting, data quality assessment, trend pattern recognition

**AI-Enhanced Component Design Principles:**
- **Performance-First Optimization:** Every component optimized for investment performance analysis with intelligent AI assistance
- **Multi-Provider AI Integration:** Seamless coordination of multiple LLM providers with transparent service switching
- **Service Health Awareness:** Components gracefully handle individual AI service failures without disrupting user workflow
- **Intelligent AI Recommendations:** Smart suggestions discoverable through contextual interaction with provider-specific expertise
- **Competitive Intelligence Integration:** Anonymous benchmarking enhanced with AI pattern recognition and market analysis
- **Building Block Flexibility:** User-friendly editing with AI-powered redundancy detection and optimization suggestions
- **Real-Time AI-Assisted Collaboration:** Team coordination enhanced with intelligent decision support and consensus building
- **Transparent AI Operations:** Clear indication of which AI services are contributing to user experience at any moment
