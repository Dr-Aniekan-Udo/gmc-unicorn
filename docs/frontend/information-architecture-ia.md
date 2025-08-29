# Information Architecture (IA)

## Adaptive Multi-Mode Interface Architecture

**Core Design Philosophy:** Optimize each device type for its strengths in analytical workflow rather than forcing feature parity

**Mode Options:**
1. **Excel Familiar Mode:** Sheet-based navigation with enhanced features
2. **Integrated Workspace Mode:** Single-screen efficiency for power users
3. **Guided Workflow Mode:** Step-by-step progression for beginners

## Site Map / Screen Inventory

**Primary Structure: Project-Based Multi-Project Management Architecture**

**0. Project Management Foundation** *(Entry point and project orchestration)*
- **Project Dashboard:** Overview of all user projects with status indicators, last accessed, and quick actions
- **Project Creation Interface:** New project wizard with template selection and initial configuration
- **Project Switching Navigation:** Global project context switcher available throughout application
- **Multi-Project Status Overview:** Health indicators and progress across all projects simultaneously
- **Project Settings & Configuration:** Per-project settings, team member management, and data isolation controls

**Within Each Project Context: Investment Performance-Optimized Approach**

**1. Strategy Optimization Workspace** *(Primary competitive analysis screen)*
- **Investment Performance Center:** Real-time ranking display with performance gap analysis and competitive positioning
- **Parameter Sensitivity Panel:** Interactive controls showing investment performance impact of each decision variable
- **Strategy Comparison View:** Side-by-side analysis of multiple optimization scenarios with performance forecasting
- **AI Optimization Assistant:** Smart recommendations panel with constraint-aware strategy suggestions
- **Competitive Intelligence Sidebar:** Anonymous benchmarking and successful strategy pattern insights

**2. Building Block Analysis Hub**
- **Formula Transparency Center:** User-friendly editing capabilities for calculation adjustments and formula optimization
- **Redundancy Detection Panel:** Intelligent identification of unused/redundant calculations with manual review workflow
- **Calculation Verification:** Real-time validation against Excel equivalence with modification impact analysis
- **Custom Logic Builder:** Simple interface for users to adjust business logic and decision interdependencies

**3. Performance Command Center** *(Strategic overview dashboard)*
- **Investment Performance Tracking:** Historical progression with trend analysis and competitive context
- **Strategy Effectiveness Metrics:** Analysis of which decision combinations drive highest ranking improvements  
- **Team Performance Coordination:** Multi-user optimization collaboration with individual contribution attribution
- **Competitive Market Intelligence:** Anonymous insights on successful strategies and performance distribution patterns

## Navigation Structure

**Global Navigation:** *Project-aware navigation system*
- **Project Selector** (Always visible) - Current project context with quick project switching
- **Global Dashboard** - Multi-project overview, project creation, and cross-project insights
- **Project Settings** - Current project configuration, team management, and data isolation

**Project-Scoped Primary Navigation:** *Investment Performance-Focused horizontal navigation within project context*
- **Strategy Center** (Home) - Investment performance optimization dashboard with competitive ranking and AI recommendations
- **Optimization** - Parameter sensitivity analysis, multi-scenario comparison, and strategy tuning tools
- **Performance Intel** - Competitive benchmarking, best practices insights, and market intelligence 
- **Building Blocks** - Formula transparency, calculation editing, and redundancy management tools
- **Team Strategy** - Collaborative optimization, role-based access, and shared decision-making workflows
- **Data & Insights** - File management, historical analysis, and performance attribution reporting
- **AI Coach** - Personal AI assistant, conversational interface, strategy learning, and coaching sessions
- **Faculty Dashboard** - Educational analytics, student progress tracking, competency assessment (Faculty Only)

### Route Definitions Table

**Complete URL Patterns and Access Control Matrix**

| Route Pattern | Component/Page | Access Level | Authentication Required | Deep Link Support |
|---------------|----------------|--------------|-------------------------|-------------------|
| **Global Routes** | | | | |
| `/` | Multi-Project Dashboard | All Users | Yes | N/A |
| `/projects/new` | Project Creation Wizard | All Users | Yes | No |
| `/projects/:projectId/switch` | Project Context Switcher | Project Members | Yes | No |
| `/settings/global` | Global User Settings | All Users | Yes | No |
| **Project-Scoped Routes (`:projectId` prefix)** | | | | |
| `/projects/:projectId` | Strategy Center (Home) | Project Members | Yes | Yes |
| `/projects/:projectId/strategy` | Investment Performance Dashboard | Project Members | Yes | Yes |
| `/projects/:projectId/optimization` | Parameter Sensitivity Analysis | Project Members | Yes | Yes |
| `/projects/:projectId/optimization/scenarios` | Multi-Scenario Comparison | Project Members | Yes | Yes |
| `/projects/:projectId/optimization/sensitivity/:parameterId` | Parameter Detail View | Project Members | Yes | Yes |
| `/projects/:projectId/performance-intel` | Competitive Intelligence Panel | Project Members | Yes | Yes |
| `/projects/:projectId/performance-intel/benchmarks` | Anonymous Benchmarking | Project Members | Yes | Yes |
| `/projects/:projectId/performance-intel/trends` | Market Intelligence | Project Members | Yes | Yes |
| `/projects/:projectId/building-blocks` | Formula Transparency Center | Project Members | Yes | Yes |
| `/projects/:projectId/building-blocks/editor` | Building Block Editor | Project Members | Yes | Yes |
| `/projects/:projectId/building-blocks/redundancy` | Redundancy Detection | Project Members | Yes | Yes |
| `/projects/:projectId/team` | Team Strategy Coordination | Project Members | Yes | Yes |
| `/projects/:projectId/team/permissions` | Role-Based Access Control | Project Owners | Yes | No |
| `/projects/:projectId/team/collaboration` | Real-Time Collaboration | Project Members | Yes | Yes |
| `/projects/:projectId/data` | File Management Timeline | Project Members | Yes | Yes |
| `/projects/:projectId/data/upload` | File Upload Interface | Project Members | Yes | No |
| `/projects/:projectId/data/reports/:reportId` | GMC Report Viewer | Project Members | Yes | Yes |
| `/projects/:projectId/insights` | Performance Attribution | Project Members | Yes | Yes |
| `/projects/:projectId/insights/history` | Analysis History Timeline | Project Members | Yes | Yes |
| `/projects/:projectId/ai-coach` | AI Coaching Interface | Project Members | Yes | Yes |
| `/projects/:projectId/ai-coach/conversation` | Conversational AI Chat | Project Members | Yes | Yes |
| `/projects/:projectId/ai-coach/knowledge` | Knowledge Search Panel | Project Members | Yes | Yes |
| `/projects/:projectId/ai-coach/recommendations` | ML Recommendations | Project Members | Yes | Yes |
| `/projects/:projectId/ai-coach/providers` | Multi-Provider Selection | Project Members | Yes | No |
| `/projects/:projectId/settings` | Project Configuration | Project Owners | Yes | No |
| **Faculty-Only Routes** | | | | |
| `/faculty` | Faculty Dashboard | Faculty | Yes | Yes |
| `/faculty/analytics` | Educational Analytics | Faculty | Yes | Yes |
| `/faculty/students/:studentId` | Individual Student Progress | Faculty | Yes | Yes |
| `/faculty/class/:classId` | Class Performance Overview | Faculty | Yes | Yes |
| `/faculty/interventions` | Intervention Alerts | Faculty | Yes | Yes |
| **API Key Management Routes** | | | | |
| `/api-keys` | Personal API Key Management | All Users | Yes | No |
| `/api-keys/providers/:providerId` | Provider Configuration | All Users | Yes | No |
| `/api-keys/usage` | Usage Analytics Dashboard | All Users | Yes | Yes |
| `/api-keys/budget` | Budget Monitoring | All Users | Yes | Yes |

**Route Protection Implementation:**
- **Authentication Layer:** API Gateway (Kong/Traefik) with JWT token validation
- **Project-Scoped Authorization:** Middleware validates project membership and role permissions
- **Deep Linking Support:** State restoration for shareable analysis URLs with project context
- **Route Guards:** React Router guards validate access levels and redirect to appropriate entry points

**URL Parameter Patterns:**
- **Project ID:** UUIDs for project identification (`550e8400-e29b-41d4-a716-446655440000`)
- **Parameter ID:** Semantic identifiers for GMC parameters (`product1-price`, `europe-advertising`)
- **Report ID:** Timestamped identifiers for uploaded files (`hst-y16q1`, `w122162-2024`)
- **Faculty Context:** Institution-scoped identifiers with role validation

**Secondary Navigation:** *Project-scoped context-sensitive left sidebar within each primary area*
- **In Analysis Areas:** Quick switcher between related sheets within current project (e.g., Production → Costs → Performance)  
- **In Data Management:** Project-specific file organization, company selection, and historical timeline
- **In Team Areas:** Project team member management, permissions, and project-scoped communication threads
- **Project Context Indicator:** Always-visible reminder of current project scope and isolation boundaries

**Breadcrumb Strategy:** *Dynamic breadcrumbs showing analysis depth*
- **Level 1:** Primary area (Analysis, Data, Team, Tools)
- **Level 2:** Specific component (Decision Studio, Production Analysis)  
- **Level 3:** Detail view (Parameter Controls, Machine Capacity)
- **Interactive breadcrumbs:** Click any level to return while preserving context
