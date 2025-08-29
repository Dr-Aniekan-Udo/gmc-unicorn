# Introduction

This document defines the user experience goals, information architecture, user flows, and visual design specifications for GMC Dashboard's user interface. It serves as the foundation for visual design and frontend development, ensuring a cohesive and user-centered experience.

## Overall UX Goals & Principles

### Target User Personas

**Primary: "Strategic Sarah" - The Analytical Team Lead**
- Graduate MBA student (26-28), team captain experience
- **Goals:** Optimize investment performance, guide team decisions, ensure GMC compliance
- **Pain Points:** Excel crashes under complexity, time pressure (240→45min target), teaching teammates
- **Behavior:** Detail-oriented, risk-averse about constraint violations, collaborative leadership style

**Secondary: "Efficient Erik" - The Executive Decision Maker**
- Executive MBA (30-35), experienced professional with limited time
- **Goals:** Fast strategic analysis, focus on insights not spreadsheet mechanics  
- **Pain Points:** Impatient with learning curves, wants advanced features immediately
- **Behavior:** Values automation, shortcuts, and direct access to key metrics

**Tertiary: "Learning Lisa" - The First-Time GMC Participant**
- Undergraduate business major (20-22), first simulation experience
- **Goals:** Understand GMC rules, avoid major mistakes, learn through safe experimentation
- **Pain Points:** Overwhelmed by complexity, fears making wrong decisions
- **Behavior:** Needs contextual guidance, benefits from explanations, learns through hands-on exploration

### Usability Goals

**Primary Success Metrics:**
- **Investment Performance Optimization:** Enable teams to achieve competitive ranking improvements through strategic parameter tuning
- **Strategy Analysis Speed:** Parameter sensitivity analysis <1 second, optimization recommendations <2 seconds
- **Analysis Time Reduction:** 240 minutes → 45 minutes (85% reduction) with increased strategic focus
- **Competitive Intelligence:** Anonymous benchmarking and performance gap identification
- **Constraint-Aware Optimization:** 90% reduction in constraint violations while maximizing performance potential
- **Team Strategy Coordination:** Real-time collaborative optimization with individual contribution tracking

**Experience Quality Targets:**
- **Immediate Feedback:** Sub-500ms visual response to all parameter changes
- **Calculation Transparency:** Real-time updates with visible calculation progress
- **Error Recovery:** One-click reversion to any previous analysis state
- **Academic Integrity:** Complete formula audit trail with Excel-equivalent verification

### Design Principles

**1. Investment Performance-Centered Design**  
*Every interface element optimizes for competitive ranking improvement*
- **Performance Impact Visualization**: Real-time display of how parameter changes affect investment performance ranking
- **Strategy Optimization Dashboard**: Primary interface focused on parameter sensitivity and competitive positioning
- **Constraint-Aware Recommendations**: Visual guides suggest optimal parameter combinations within resource limits
- **Competitive Context Integration**: Anonymous benchmarking shows performance gaps and optimization opportunities

**2. Strategy Tuning-First Architecture with Progressive Optimization**
*Start with performance impact, progress to detailed parameter tuning, maintain competitive context*
- **Strategy Command Center**: Investment performance dashboard with real-time ranking and optimization opportunities
- **Progressive Strategy Disclosure**: Parameter sensitivity analysis → AI recommendations → multi-scenario comparison
- **Contextual Optimization**: Beginners see guided optimization paths, experts access advanced strategy comparison tools
- **Building Block Flexibility**: Simple editing capabilities for formula adjustments and calculation modifications

**3. Excel-Familiar with Modern Enhancement**
*Leverage familiar patterns while eliminating frustrations*
- Maintain Excel visual metaphors and keyboard shortcuts (Ctrl+Z/Ctrl+Y)
- Provide "Show Formulas" transparency mode for verification needs
- Enhance Excel limitations: real-time collaboration, visual constraints, guided workflows

**4. Intelligent Strategy Analysis Philosophy**
*Trust through explainable optimization and transparent competitive intelligence*
- **Strategy Transparency Mode**: Reveals why certain parameters impact investment performance most significantly
- **AI Recommendation Explanations**: Clear rationale for optimization suggestions based on successful patterns
- **Performance Attribution Analysis**: Shows which decision categories contribute most to competitive ranking changes
- **Building Block Intelligence**: System detects formula redundancies and inconsistencies with user-friendly adjustment workflows

**5. Social Collaboration Design**
*Team presence with conflict prevention*
- Visual ownership indicators show who's editing which analysis areas
- Real-time teammate cursor visibility and change attribution
- Smart conflict resolution with merge capabilities and change notifications

**6. Educational Excellence & AI-Enhanced Learning**
*Personalized learning with faculty oversight and AI coaching*
- Individual user API key management for personalized AI assistance
- Educational analytics dashboard for faculty competency tracking
- Conversational AI coaching with persistent user-specific learning
- Adaptive difficulty scaling based on demonstrated competency

### Change Log

| Date | Version | Description | Author |
|------|---------|-------------|--------|
| 2025-08-26 | 1.0 | Initial UX Goals established from comprehensive user research and competitive analysis | Sally (UX Expert) |
| 2025-08-27 | 1.1 | **STRATEGIC UPDATE**: Investment performance optimization as primary focus, strategy tuning system integration, competitive ranking emphasis | Sally (UX Expert) |
| 2025-08-28 | 2.0 | **MAJOR UPDATE**: Added Educational Analytics & Faculty Tools, AI Coaching System, Individual API Key Management, Advanced File Management | Sally (UX Expert) |
| 2025-08-28 | 3.0 | **CRITICAL ARCHITECTURE UPDATE**: Complete project-based microservice architecture integration - Added Epic 0 Project Management Foundation, project-scoped AI coaching contexts, microservice-aware UI patterns, project data isolation across all components, distributed state management, and comprehensive project-based wireframes | Sally (UX Expert) |
