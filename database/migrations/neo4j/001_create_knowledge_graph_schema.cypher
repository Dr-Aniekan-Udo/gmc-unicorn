// GMC Knowledge Graph Schema - Project-Scoped
// Initial schema for knowledge graph service with project isolation

// Create project isolation constraint
CREATE CONSTRAINT project_isolation IF NOT EXISTS FOR (p:Project) REQUIRE p.project_id IS UNIQUE;

// Create core GMC rule nodes with project scoping
CREATE CONSTRAINT gmc_rule_constraint IF NOT EXISTS FOR (r:GMCRule) REQUIRE (r.id, r.project_id) IS UNIQUE;
CREATE CONSTRAINT parameter_constraint IF NOT EXISTS FOR (p:Parameter) REQUIRE (p.id, p.project_id) IS UNIQUE;
CREATE CONSTRAINT market_constraint IF NOT EXISTS FOR (m:Market) REQUIRE (m.id, r.project_id) IS UNIQUE;

// Example project-scoped GMC rules
CREATE (project:Project {project_id: 'default', name: 'Default GMC Project', created_at: datetime()});

// GMC business rules with project scoping
CREATE (capacity_rule:GMCRule {
    id: 'capacity_constraint', 
    project_id: 'default',
    type: 'hard_constraint', 
    description: 'Machine capacity cannot exceed available hours',
    formula: 'sum(machine_hours) <= available_capacity'
});

CREATE (demand_rule:GMCRule {
    id: 'demand_constraint',
    project_id: 'default', 
    type: 'market_constraint',
    description: 'Production must meet minimum demand requirements',
    formula: 'production_quantity >= min_demand * market_share'
});

// Parameters with project isolation
CREATE (machine_hours:Parameter {
    id: 'machine_hours_product_a',
    project_id: 'default',
    type: 'decision_variable', 
    min_value: 0,
    unit: 'hours'
});

CREATE (revenue:Parameter {
    id: 'revenue_per_unit',
    project_id: 'default',
    type: 'constant',
    value: 100.0,
    unit: 'currency'
});

// Market data with project context
CREATE (europe_market:Market {
    id: 'europe',
    project_id: 'default',
    name: 'European Market', 
    demand_elasticity: 0.8,
    market_size: 1000000
});

// Relationships between rules and parameters (project-scoped)
CREATE (capacity_rule)-[:CONSTRAINS {project_id: 'default'}]->(machine_hours);
CREATE (demand_rule)-[:AFFECTS {project_id: 'default'}]->(europe_market);
CREATE (machine_hours)-[:GENERATES {project_id: 'default', coefficient: 100.0}]->(revenue);

// Indexes for performance
CREATE INDEX rule_project_idx IF NOT EXISTS FOR (r:GMCRule) ON (r.project_id);
CREATE INDEX param_project_idx IF NOT EXISTS FOR (p:Parameter) ON (p.project_id);
CREATE INDEX market_project_idx IF NOT EXISTS FOR (m:Market) ON (m.project_id);