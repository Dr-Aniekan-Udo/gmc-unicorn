# Epic 2: Project-Scoped Decision Input System & Core Analysis Engine

**Epic Goal:** Implement project-scoped Decision Sheet interfaces with all GMC decision parameters and build core analysis calculations for Revenue, Cost of Production, and basic Investment Performance within individual project contexts, delivering functional analysis systems that process user decisions independently per project through complete calculation pipelines with project-specific constraint validation and meaningful financial outcomes.

## Story 2.1: Project-Scoped Decision Sheet Input Interface

**As a** GMC participant,  
**I want** an intuitive project-specific decision input interface matching the Excel Decision Sheet,  
**so that** I can efficiently input quarterly decisions for each project independently without workflow confusion or cross-project interference.

### Acceptance Criteria
1. Interactive dashboard replicates Decision Sheet layout with proper visual grouping and labeling
2. Input controls implemented for all decision categories: Advertising (E8:H10), Prices (E13:G15), Quantities (E18:G20), Quality (E23:G26), Operations (H13:P15), Personnel (H18:P20), Finance (H23:P26)
3. Slider controls provide immediate visual feedback with min/max constraints based on available resources
4. Year/Quarter display (Year 2016, Qtr 4 format) with proper context for decision timing
5. Input validation prevents impossible combinations and provides helpful error messages
6. Auto-save functionality preserves decision state every 30 seconds with visual confirmation

## Story 2.2: Revenue Calculation Engine

**As a** user,  
**I want** real-time revenue calculations based on my pricing and quantity decisions,  
**so that** I can immediately see financial impact of market strategies.

### Acceptance Criteria
1. Revenue matrix calculations (B17:D26) process pricing and quantity inputs for all Product×Market combinations
2. Scrap value processing (H23:J27) handles product rejection scenarios with proper valuation
3. Total revenue consolidation (E29:E30) provides accurate summation with validation against expected ranges
4. Real-time updates trigger within 500ms of parameter changes across all dependent calculations
5. Revenue calculations match Excel reference data with 100% mathematical accuracy
6. Visual indicators show revenue impact of decision changes with clear before/after comparisons

## Story 2.3: Production Cost Analysis System

**As a** user,  
**I want** comprehensive production cost analysis based on my operational decisions,  
**so that** I understand the full cost implications of production choices.

### Acceptance Criteria
1. Machine capacity calculations (L5:P11) process efficiency, availability, and wage parameters
2. Raw material cost matrix (T1:AR12) handles multi-shift material requirements with proper cost allocation
3. Machine running costs (T13:AR33) calculate detailed machine hour requirements by product and shift
4. Labor cost calculations include both machinist wages (T34:AR44) and assembly wages (T48:AR55) with shift differentials
5. Quality control costs (T56) and logistics costs (T57:AR62) integrate with operational parameters
6. Total cost consolidation (T63:AR67) provides accurate per-unit and total cost calculations by market/product

## Story 2.4: Constraint Validation System

**As a** user,  
**I want** real-time constraint validation that prevents impossible decisions,  
**so that** I avoid costly mistakes that would fail in the actual GMC simulation.

### Acceptance Criteria
1. Machine capacity constraints validate against available hours and efficiency parameters
2. Personnel constraints check assembly worker availability and training requirements
3. Material availability constraints verify sufficient inventory for production decisions
4. Financial constraints validate cash flow requirements for equipment purchases and loan capabilities
5. Three-tier validation system: warnings (yellow), cautions (orange), violations (red) with appropriate UI feedback
6. Constraint violations block decision submission with clear explanation of required corrections

## Story 2.5: Basic Investment Performance Calculation

**As a** user,  
**I want** preliminary investment performance calculation,  
**so that** I can evaluate the overall effectiveness of my decision combination.

### Acceptance Criteria
1. Share capital tracking (E3:E6) processes equity structure changes from finance decisions
2. Basic investment performance metric (I9) calculates preliminary performance indicator
3. Profitability calculations integrate revenue and cost analysis results
4. Cash flow impact analysis shows immediate financial position changes
5. Performance calculations update in real-time as decisions change across all input categories
6. Results display provides clear indication of positive/negative performance trends

## Story 2.6: Analysis Session Management

**As a** user,  
**I want** complete session management with save/load and history tracking,  
**so that** I can work on analysis across multiple sessions and compare different scenarios.

### Acceptance Criteria
1. Session state persistence saves all decision parameters and calculation results
2. Auto-recovery restores previous session state if browser crashes or connection lost
3. Analysis history tracks all parameter changes with timestamps for review
4. Scenario comparison allows side-by-side analysis of different decision combinations
5. Export functionality generates decision summary in GMC-compatible format
6. Session cleanup removes expired sessions while preserving important analysis history
