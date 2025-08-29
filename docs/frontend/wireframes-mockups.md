# Wireframes & Mockups

**Primary Design Files:** [Future Figma workspace to be created - recommend: "GMC Dashboard UI Design System"]

## Key Screen Layouts

### Multi-Project Dashboard (Application Entry Point)

**Purpose:** Primary entry point providing overview of all user projects, creation workflows, and cross-project navigation

**Key Elements:**
- **Project Grid/List View:**
```
┌─ GMC DASHBOARD - PROJECT MANAGEMENT ─────────────────────┐
│ [🏠 Dashboard] [➕ New Project] [👥 Team] [⚙️ Settings] │
├─ MY PROJECTS ────────────────────────────────────────────┤
│ ┌─ Project Alpha ─────┐ ┌─ Market Strategy ───┐ ┌─ Q4  ─┐ │
│ │ 🎯 Active Analysis  │ │ 📊 Competitive Intel│ │ 📁 Data│ │
│ │ Last: 2h ago        │ │ Last: 1d ago       │ │ Setup │ │
│ │ Performance: 847.3  │ │ Performance: 723.1 │ │ Ready │ │
│ │ [📊 Open] [⚙️ Set] │ │ [📊 Open] [⚙️ Set]│ │ [📊]  │ │
│ └─────────────────────┘ └────────────────────┘ └───────┘ │
├─ QUICK ACTIONS ──────────────────────────────────────────┤
│ 🚀 Start New Analysis  📋 Clone Existing  👥 Join Team   │
│ 📊 Cross-Project Intel 📈 Performance Summary            │
└───────────────────────────────────────────────────────────┘
```

**Interaction Notes:** Project cards with hover states, drag-and-drop reordering, quick actions menu, bulk operations

### Project Creation Wizard

**Purpose:** Guided setup for new GMC analysis projects with template selection and team configuration

**Key Elements:**
- **Step-by-Step Configuration:**
```
┌─ NEW PROJECT WIZARD ─────────────────────────────────────┐
│ Step 1 of 4: Project Setup                               │
├───────────────────────────────────────────────────────────┤
│ Project Name: [Market Expansion Strategy          ]      │
│ Description:  [Analyzing European market entry    ]      │
│                                                          │
│ Project Type: ○ Individual Analysis                      │
│               ● Team Collaboration (3-5 members)        │
│               ○ Competitive Intelligence                 │
│                                                          │
│ Template:     ○ Blank Project                           │
│               ● Standard GMC Analysis                    │
│               ○ Advanced Multi-Scenario                  │
├───────────────────────────────────────────────────────────┤
│                           [Cancel] [Back] [Next Step >]  │
└───────────────────────────────────────────────────────────┘
```

**Interaction Notes:** Progressive disclosure, smart defaults, template preview, validation feedback

### Project Context Switcher (Always Visible)

**Purpose:** Global navigation element maintaining project awareness throughout application

**Key Elements:**
- **Persistent Project Context Bar:**
```
┌─ PROJECT CONTEXT ─────────────────────────────────────────┐
│ 📋 [Market Expansion Strategy ▼] │ 🏠 Dashboard │ ⚙️ Settings│
├─────────────────────────────────────────────────────────────┤
│ Quick Switch: Alpha Analysis • Competitive Intel • Q4 Data │
└─────────────────────────────────────────────────────────────┘
```

**Interaction Notes:** Dropdown with search, recent projects, favorites, clear project isolation indicators

### Strategy Command Center (Project-Scoped Performance Home)

**Purpose:** Provide immediate investment performance overview with competitive intelligence and optimization opportunities within current project context

**Key Elements:**
- **Investment Performance Dashboard:** Large, prominent display of current ranking, performance score, and competitive position with trend indicators
- **Strategy Optimization Panel:** AI-powered recommendations with parameter sensitivity analysis and performance impact forecasting
- **Competitive Intelligence Summary:** Anonymous benchmarking showing performance gaps, successful strategy patterns, and market positioning
- **Quick Strategy Actions:** "Optimize Performance," "Compare Scenarios," "Analyze Competition," "Tune Parameters" with performance impact previews
- **Strategy Effectiveness Tracker:** Visual analysis showing which decision categories drive highest investment performance improvements
- **Team Strategy Coordination:** Real-time collaboration status with individual contribution attribution and shared optimization progress
- **Building Block Health Monitor:** Formula redundancy alerts and calculation optimization opportunities with manual adjustment workflows

**Interaction Notes:** Performance impact preview on hover, one-click access to optimization tools, real-time competitive ranking updates, contextual AI recommendations based on current strategy state

### Analysis Workspace (Primary Work Area)

**Purpose:** Unified workspace where 80% of analysis work happens - parameter adjustment with real-time constraint validation and impact visualization

**Key Elements:**
- **Left Panel - Decision Parameters:** 
  - Tabbed parameter groups (Production, Pricing, Marketing, Finance)
  - Interactive sliders and input controls with immediate validation feedback
  - Constraint optimization indicators showing available capacity
- **Center Panel - Impact Visualization:**
  - Real-time calculation results display
  - Performance impact charts and metrics
  - Revenue/cost/profit trend indicators
- **Right Panel - Constraint Monitor:**
  - Contextual constraint status with optimization direction
  - Detailed violation explanations with resolution guidance
  - Team member activity indicators (in team mode)
- **Bottom Panel - Analysis Tools:**
  - Undo/redo controls with operation history
  - Scenario comparison toggle
  - Excel sheet access for power users (collapsible)
- **AI Coach Sidebar:** (Expandable/collapsible) - **PROJECT-SCOPED**
  - Project-specific conversational interface with isolated chat history
  - Quick action buttons for project-aware coaching requests
  - Project-specific strategy preference settings and learning progress
  - Clear project context indicators in AI responses

**Interaction Notes:** Drag-to-resize panels, collapsible sections for focus mode, keyboard shortcuts (Ctrl+Z/Ctrl+Y), real-time updates across all panels when parameters change

### Enhanced Multi-Provider AI Coaching Interface

**Purpose:** Unified AI assistant combining multiple providers and services with transparent service coordination and health monitoring

**Key Elements:**
- **Multi-Provider AI Interface with Service Health:**
```
┌─ AI COACH - PROJECT: Market Expansion Strategy ───────────┐
│ 🔄 Provider: Anthropic Claude ✅ | Budget: $45/$300 🟢    │
│ 🟢 Conversation ✅ Knowledge 🟡 ML Analysis 🔴 Offline   │
├───────────────────────────────────────────────────────────┤
│ 💬 [Conversation] In this project, I've learned you      │
│     prefer aggressive market entry. For European strategy │
│ 🔍 [Knowledge] Based on GMC Manual Section 4.2, European │
│     markets respond well to premium pricing strategies    │
│ 📊 [ML Prediction] CatBoost model suggests Product 2     │
│     pricing at €135 for +22.3 performance improvement    │
├─ PROVIDER SELECTION ──────────────────────────────────────┤
│ [🧠 Anthropic] [🤖 OpenAI] [💎 Gemini] [⚡ DeepSeek]     │
│ [🌐 OpenRouter] [🏠 Ollama] | Switch: Maintains context  │
├─ AI SERVICE STATUS ────────────────────────────────────────┤
│ 💬 Conversation: ✅ Fast response (127ms avg)            │
│ 🔍 Knowledge Search: ✅ Vector search active             │
│ 📊 ML Recommendations: 🟡 High load (2.3s response)     │
│ 🎯 Orchestrator: ✅ All services coordinated             │
├─ USER INPUT WITH SERVICE INDICATORS ──────────────────────┤
│ [Compare pricing strategies across markets?        ] 📤   │
│ Quick Actions: 💡 Optimize 🔍 Search 📊 Analyze 🎯 All   │
└───────────────────────────────────────────────────────────┘
```

**Advanced Service Health Dashboard:**
```
┌─ AI SERVICES HEALTH MONITOR ──────────────────────────────┐
│ Overall AI Health: 🟢 Excellent (3/4 services optimal)   │
├─ SERVICE BREAKDOWN ────────────────────────────────────────┤
│ 💬 Conversation Service    ✅ Active   127ms avg response │
│ 🔍 Vector Search Service   ✅ Active   2.1GB knowledge    │
│ 📊 ML Recommendation      🟡 Slow     2.3s avg response  │
│ 🎯 Coaching Orchestrator  ✅ Active   All services coord │
├─ DEGRADED SERVICE HANDLING ───────────────────────────────┤
│ ⚠️  ML Service experiencing high load. Using cached       │
│     recommendations. Full service restored in ~5 mins.    │
│ 🔄 Alternative: Switch to knowledge-based recommendations │
├─ PROVIDER BUDGET STATUS ──────────────────────────────────┤
│ Anthropic: $45/$300 monthly 🟢 | Daily: $2.1/$10 🟢      │
│ OpenAI: Not configured ⚪ | Gemini: $12/$100 🟢          │
└───────────────────────────────────────────────────────────┘
```

**Interaction Notes:** Multi-provider switching with context preservation, real-time service health monitoring, graceful degradation messaging, transparent AI service coordination

### Multi-Project Status Management Interface

**Purpose:** Advanced interface for users managing multiple concurrent projects with cross-project insights

**Key Elements:**
- **Cross-Project Performance Comparison:**
```
┌─ MULTI-PROJECT ANALYTICS ──────────────────────────────────┐
│ 📊 Performance Across Projects                             │
├─ PROJECT COMPARISON ───────────────────────────────────────┤
│ Market Expansion    ████████████░░ 892.1  🟢 Excellent    │
│ Alpha Analysis      ██████████░░░░ 847.3  🟡 Good         │
│ Q4 Conservative     ██████░░░░░░░░ 723.1  🟠 Improving    │
├─ STRATEGY INSIGHTS ────────────────────────────────────────┤
│ • Aggressive strategies performing +18% better across all  │
│ • European focus drives highest investment performance     │
│ • Conservative approach optimal for risk management       │
├─ PROJECT MANAGEMENT ───────────────────────────────────────┤
│ 🎯 Active Projects: 3    ⏰ Total Time Saved: 4.2 hours  │
│ 🤖 AI Usage: 47 sessions 💰 Budget Used: $23.50/$300     │
└─────────────────────────────────────────────────────────────┘
```

### Faculty Educational Analytics Dashboard

**Purpose:** Comprehensive instructor interface for monitoring class performance and student competency development across projects

**Key Elements:**
- **Class Performance Overview:**
```
┌─ FACULTY DASHBOARD - CLASS ANALYTICS ─────────────────────┐
│ 📈 Class Performance Overview      📊 Individual Progress  │
│ ├─ Average Investment Performance: 847.2                  │
│ ├─ Constraint Violation Rate: ↓23% (Target: 90% reduction)│
│ ├─ Analysis Time: 67min avg (Target: 45min)              │
│ └─ Strategic Thinking: 78% improvement                    │
├─ COMPETENCY TRACKING ─────────────────────────────────────┤
│ Financial Analysis    ████████████░░ 85% class mastery   │
│ Market Strategy      ███████░░░░░░░ 65% class mastery    │
│ Risk Management      ██████████░░░░ 75% class mastery     │
├─ INTERVENTION ALERTS ─────────────────────────────────────┤
│ ⚠️  3 students struggling with constraint understanding   │
│ 💡 2 students ready for advanced optimization challenges  │
└────────────────────────────────────────────────────────────┘
```

**Interaction Notes:** Drill-down to individual students, project-specific intervention tools, cross-project competency assessment

### Enhanced Multi-Provider API Key Management Interface

**Purpose:** Comprehensive AI provider credential management with real-time health monitoring and intelligent service selection

**Key Elements:**
- **Enhanced Multi-Provider Configuration:**
```
┌─ PERSONAL AI CONFIGURATION ────────────────────────────────┐
│ 🔐 Your AI Service Credentials - 6 Providers Supported    │
├─ PROVIDER STATUS & CAPABILITIES ──────────────────────────┤
│ ✅ Anthropic Claude    Budget: $45/$300 🟢 Conversation++│
│ ✅ OpenAI GPT-4       Budget: $23/$200 🟢 Analysis++     │
│ ✅ Google Gemini      Budget: $12/$100 🟢 Knowledge++    │
│ ⚪ DeepSeek (Not Set) Budget: $0/$150  ⚪ Cost Effective │
│ ❌ OpenRouter (Error) Budget: $5/$100  🔴 Service Down   │
│ ✅ Local Ollama       Status: Connected 🟢 Privacy++     │
├─ INTELLIGENT SERVICE SELECTION ───────────────────────────┤
│ 🎯 Auto-Select Best Provider:                             │
│ • Conversation: Anthropic (Best reasoning)               │
│ • Knowledge Search: Gemini (Vector search optimized)     │
│ • ML Analysis: OpenAI (Mathematical reasoning)           │
│ • Budget Conscious: DeepSeek (Cost effective)            │
├─ REAL-TIME MONITORING ────────────────────────────────────┤
│ Active Sessions: 3 providers | Total Today: $4.20/$30    │
│ Anthropic: 45 msgs, $2.10 | OpenAI: 12 msgs, $1.85      │
│ Gemini: 8 searches, $0.25  | Auto-failover: 2 instances │
├─ ADVANCED MANAGEMENT ─────────────────────────────────────┤
│ [🚀 Smart Setup Wizard] [🔄 Provider Health Check]       │
│ [📊 Usage Analytics]    [⚡ Auto Budget Optimizer]       │
│ [🛡️ Security Audit]     [🌐 Service Comparison]         │
└────────────────────────────────────────────────────────────┘
```

**Service Health Integration:**
```
┌─ PROVIDER HEALTH & PERFORMANCE MONITORING ────────────────┐
│ Real-time Status: 5/6 providers optimal                   │
├─ PERFORMANCE METRICS ──────────────────────────────────────┤
│ Response Times: Anthropic 127ms, OpenAI 89ms, Gemini 156ms│
│ Success Rate: All providers >99.5% uptime this month      │
│ Cost Efficiency: DeepSeek 50% cheaper, Ollama free local  │
├─ AUTOMATIC FAILOVER LOG ───────────────────────────────────┤
│ 14:23 OpenRouter→Anthropic (timeout)     ✅ Seamless     │
│ 12:15 OpenAI→Gemini (quota exceeded)     ✅ User notified │
└────────────────────────────────────────────────────────────┘
```

**Interaction Notes:** Multi-provider health monitoring, intelligent service selection, automatic failover with user notification, comprehensive usage analytics

### Advanced File Management Timeline

**Purpose:** Intelligent file organization with GMC naming pattern recognition and cross-quarter analysis

**Key Elements:**
- **Interactive Timeline Interface:**
```
┌─ GMC FILE TIMELINE - INTELLIGENT ORGANIZATION ────────────┐
│ 📁 Drag & Drop Files | 🏷️ Auto-Recognition | 📈 Trends    │
├─ TIMELINE VIEW ────────────────────────────────────────────┤
│ Y16Q1 ──── Y16Q2 ──── Y16Q3 ──── Y16Q4 ──── Current      │
│ [Hst]     [Hst]     [Hst]     [Hst]     [W122162]        │
│  ✅        ✅        ⚠️        ✅        📤              │
├─ TREND ANALYSIS ───────────────────────────────────────────┤
│ Performance Trend: ↗️ +12% improvement across quarters    │
│ Strategy Evolution: Pricing focus → Market diversification │
│ Key Insights: Europe market shows consistent growth       │
├─ FILE ACTIONS ─────────────────────────────────────────────┤
│ 🔄 Reorder Timeline  📊 Generate Trends  ⚠️ Validate Data  │
│ 🗑️ Remove Files    📥 Import Batch     📤 Export Analysis │
└────────────────────────────────────────────────────────────┘
```

**Interaction Notes:** Drag-and-drop reordering, automatic chronological sorting, trend visualization, data quality validation

### Contextual Information System

**Enhanced Tooltip Components:**
- **Rich Content Tooltips:** Formatted text, charts, and interactive elements
- **Formula Explanations:** Step-by-step calculation breakdown with Excel equivalents
- **Historical Context:** Multi-quarter trend data and benchmark comparisons
- **Team Activity Information:** Real-time collaboration information and change attribution

**Slide-Out Detail Panels:**
- **Right Sidebar:** Detailed constraint analysis and formula transparency
- **Left Sidebar:** Historical comparisons and team activity
- **Bottom Drawer:** Scenario comparison when needed
