// GMC Dashboard: Neo4j Knowledge Graph Schema
// GMC business rule relationships and strategic reasoning with project contexts

// Create constraints for unique identifiers
CREATE CONSTRAINT gmc_rule_id_unique IF NOT EXISTS FOR (r:GMCRule) REQUIRE r.id IS UNIQUE;
CREATE CONSTRAINT parameter_id_unique IF NOT EXISTS FOR (p:Parameter) REQUIRE p.id IS UNIQUE;
CREATE CONSTRAINT market_id_unique IF NOT EXISTS FOR (m:Market) REQUIRE m.id IS UNIQUE;
CREATE CONSTRAINT product_id_unique IF NOT EXISTS FOR (pr:Product) REQUIRE pr.id IS UNIQUE;
CREATE CONSTRAINT strategy_id_unique IF NOT EXISTS FOR (s:Strategy) REQUIRE s.id IS UNIQUE;
CREATE CONSTRAINT project_context_id_unique IF NOT EXISTS FOR (pc:ProjectContext) REQUIRE pc.project_id IS UNIQUE;

// Create indexes for performance
CREATE INDEX gmc_rule_type_index IF NOT EXISTS FOR (r:GMCRule) ON (r.type);
CREATE INDEX parameter_type_index IF NOT EXISTS FOR (p:Parameter) ON (p.type);
CREATE INDEX market_region_index IF NOT EXISTS FOR (m:Market) ON (m.region);
CREATE INDEX product_category_index IF NOT EXISTS FOR (pr:Product) ON (pr.category);
CREATE INDEX strategy_complexity_index IF NOT EXISTS FOR (s:Strategy) ON (s.complexity_level);

// Project context nodes for data isolation
CREATE INDEX project_context_active_index IF NOT EXISTS FOR (pc:ProjectContext) ON (pc.is_active);

// Core GMC Rules (Business Logic)
CREATE (capacity_rule:GMCRule {
    id: 'capacity_constraint',
    type: 'hard_constraint',
    description: 'Machine capacity cannot exceed available hours',
    formula: 'sum(machine_hours_per_product) <= total_machine_hours',
    priority: 'critical',
    educational_explanation: 'Production capacity represents the maximum output achievable with available resources'
});

CREATE (demand_rule:GMCRule {
    id: 'market_demand_constraint',
    type: 'market_constraint', 
    description: 'Sales cannot exceed market demand',
    formula: 'sales_volume <= market_demand * market_share',
    priority: 'high',
    educational_explanation: 'Market demand sets the upper limit for achievable sales in each region'
});

CREATE (cash_flow_rule:GMCRule {
    id: 'cash_flow_balance',
    type: 'financial_constraint',
    description: 'Cash outflows cannot exceed available cash plus credit',
    formula: 'total_expenses <= cash_balance + available_credit',
    priority: 'critical',
    educational_explanation: 'Financial liquidity ensures business operations can continue'
});

// Parameters (Decision Variables)
CREATE (machine_hours:Parameter {
    id: 'machine_hours_product_a',
    type: 'decision_variable',
    category: 'production',
    min_value: 0,
    max_value: 10000,
    unit: 'hours',
    description: 'Machine hours allocated to Product A production'
});

CREATE (price_product_a:Parameter {
    id: 'price_product_a',
    type: 'decision_variable', 
    category: 'pricing',
    min_value: 50,
    max_value: 200,
    unit: 'currency',
    description: 'Selling price for Product A'
});

CREATE (marketing_spend:Parameter {
    id: 'marketing_spend_europe',
    type: 'decision_variable',
    category: 'marketing',
    min_value: 0,
    max_value: 100000,
    unit: 'currency',
    description: 'Marketing expenditure in European market'
});

// Markets
CREATE (europe_market:Market {
    id: 'europe',
    name: 'European Market',
    region: 'Europe',
    demand_elasticity: 0.8,
    growth_rate: 0.03,
    competitive_intensity: 'high',
    description: 'Primary European market with high competition'
});

CREATE (asia_market:Market {
    id: 'asia',
    name: 'Asian Market', 
    region: 'Asia',
    demand_elasticity: 1.2,
    growth_rate: 0.07,
    competitive_intensity: 'medium',
    description: 'Emerging Asian market with growth potential'
});

// Products  
CREATE (product_a:Product {
    id: 'product_a',
    name: 'Product A',
    category: 'premium',
    production_complexity: 'medium',
    market_position: 'established',
    description: 'Premium product line with established market presence'
});

CREATE (product_b:Product {
    id: 'product_b',
    name: 'Product B',
    category: 'standard', 
    production_complexity: 'low',
    market_position: 'growing',
    description: 'Standard product line with growth potential'
});

// Strategies
CREATE (cost_leadership:Strategy {
    id: 'cost_leadership',
    name: 'Cost Leadership Strategy',
    description: 'Focus on minimizing costs to offer competitive pricing',
    complexity_level: 'medium',
    risk_level: 'low',
    optimization_focus: ['production_efficiency', 'cost_reduction']
});

CREATE (differentiation:Strategy {
    id: 'differentiation',
    name: 'Product Differentiation Strategy', 
    description: 'Focus on unique product features and premium positioning',
    complexity_level: 'high',
    risk_level: 'medium',
    optimization_focus: ['quality', 'innovation', 'brand_value']
});

// Project Context (for project-scoped isolation)
CREATE (default_project:ProjectContext {
    project_id: 'default',
    name: 'Default GMC Project',
    is_active: true,
    created_at: datetime(),
    description: 'Default project context for initial setup'
});

// Relationships: Parameter Dependencies
CREATE (machine_hours)-[:SUBJECT_TO]->(capacity_rule);
CREATE (machine_hours)-[:TARGETS]->(product_a);
CREATE (machine_hours)-[:AFFECTS_MARKET]->(europe_market);

CREATE (price_product_a)-[:SUBJECT_TO]->(demand_rule);
CREATE (price_product_a)-[:TARGETS]->(product_a);
CREATE (price_product_a)-[:AFFECTS_MARKET]->(europe_market);
CREATE (price_product_a)-[:AFFECTS_MARKET]->(asia_market);

CREATE (marketing_spend)-[:TARGETS]->(europe_market);
CREATE (marketing_spend)-[:SUPPORTS_STRATEGY]->(differentiation);

// Relationships: Business Logic Dependencies  
CREATE (capacity_rule)-[:DEPENDS_ON]->(machine_hours);
CREATE (demand_rule)-[:DEPENDS_ON]->(price_product_a);
CREATE (cash_flow_rule)-[:DEPENDS_ON]->(marketing_spend);

// Relationships: Strategic Alignments
CREATE (product_a)-[:SUITABLE_FOR_STRATEGY]->(differentiation);
CREATE (product_b)-[:SUITABLE_FOR_STRATEGY]->(cost_leadership);

CREATE (europe_market)-[:FAVORS_STRATEGY]->(differentiation);
CREATE (asia_market)-[:FAVORS_STRATEGY]->(cost_leadership);

// Relationships: Conflicts and Optimizations
CREATE (cost_leadership)-[:CONFLICTS_WITH]->(differentiation);
CREATE (machine_hours)-[:OPTIMIZES_FOR]->(cost_leadership);
CREATE (price_product_a)-[:OPTIMIZES_FOR]->(differentiation);

// Project Context Relationships (for isolation)
CREATE (default_project)-[:CONTAINS]->(capacity_rule);
CREATE (default_project)-[:CONTAINS]->(demand_rule);
CREATE (default_project)-[:CONTAINS]->(cash_flow_rule);
CREATE (default_project)-[:CONTAINS]->(machine_hours);
CREATE (default_project)-[:CONTAINS]->(price_product_a);
CREATE (default_project)-[:CONTAINS]->(marketing_spend);

// Educational relationships for GMC learning
CREATE (capacity_rule)-[:TEACHES_CONCEPT {
    concept: 'resource_constraints',
    learning_objective: 'Understanding production limitations',
    difficulty_level: 'intermediate'
}]->(machine_hours);

CREATE (demand_rule)-[:TEACHES_CONCEPT {
    concept: 'market_dynamics', 
    learning_objective: 'Understanding price-demand relationships',
    difficulty_level: 'intermediate'
}]->(price_product_a);

CREATE (differentiation)-[:TEACHES_CONCEPT {
    concept: 'strategic_positioning',
    learning_objective: 'Understanding competitive strategy options',
    difficulty_level: 'advanced'
}]->(product_a);