-- GMC Dashboard: Project-Scoped Database Schema
-- Core project management foundation with complete data isolation

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Main projects table - foundation for project-scoped data isolation
CREATE TABLE projects (
    project_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_name VARCHAR(255) NOT NULL,
    project_description TEXT,
    user_id VARCHAR(100) NOT NULL, -- Project owner
    team_members JSONB NOT NULL DEFAULT '[]'::jsonb, -- Array of user IDs
    project_type VARCHAR(50) NOT NULL CHECK (project_type IN ('individual', 'team_collaboration', 'competitive_intelligence')),
    project_template VARCHAR(50) NOT NULL CHECK (project_template IN ('blank', 'standard_gmc', 'advanced_multi_scenario')),
    data_isolation_boundary JSONB NOT NULL DEFAULT '{}'::jsonb,
    timeline_independence JSONB NOT NULL DEFAULT '{}'::jsonb,
    strategic_context JSONB NOT NULL DEFAULT '{}'::jsonb,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_accessed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Companies within project contexts
CREATE TABLE companies (
    company_id VARCHAR(50) NOT NULL,
    project_id UUID NOT NULL REFERENCES projects(project_id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    members JSONB NOT NULL DEFAULT '[]'::jsonb,
    current_quarter VARCHAR(20) NOT NULL,
    project_role_permissions JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (company_id, project_id),
    UNIQUE (company_id, project_id)
);

-- GMC Reports with project scoping
CREATE TABLE gmc_reports (
    report_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_id UUID NOT NULL REFERENCES projects(project_id) ON DELETE CASCADE,
    company_id VARCHAR(50) NOT NULL,
    report_type VARCHAR(20) NOT NULL CHECK (report_type IN ('history', 'game')),
    quarter_period VARCHAR(20) NOT NULL,
    filename VARCHAR(255) NOT NULL,
    data JSONB NOT NULL,
    is_valid BOOLEAN DEFAULT false,
    project_timeline_position INTEGER NOT NULL,
    cross_project_isolation_verified BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (company_id, project_id) REFERENCES companies(company_id, project_id)
);

-- Analysis sessions with project isolation
CREATE TABLE analysis_sessions (
    session_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_id UUID NOT NULL REFERENCES projects(project_id) ON DELETE CASCADE,
    company_id VARCHAR(50) NOT NULL,
    session_name VARCHAR(255) NOT NULL,
    base_report_id UUID REFERENCES gmc_reports(report_id),
    base_report_data JSONB NOT NULL,
    decision_parameters JSONB NOT NULL,
    calculated_results JSONB,
    investment_performance DECIMAL(10,2),
    project_analysis_context JSONB NOT NULL DEFAULT '{}'::jsonb,
    cross_session_isolation_boundary JSONB NOT NULL DEFAULT '{}'::jsonb,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (company_id, project_id) REFERENCES companies(company_id, project_id)
);

-- Parameter changes with project-scoped audit trail
CREATE TABLE parameter_changes (
    change_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_id UUID NOT NULL REFERENCES projects(project_id) ON DELETE CASCADE,
    session_id UUID NOT NULL REFERENCES analysis_sessions(session_id) ON DELETE CASCADE,
    parameter_path VARCHAR(255) NOT NULL,
    old_value JSONB,
    new_value JSONB NOT NULL,
    change_reason VARCHAR(500),
    user_id VARCHAR(100) NOT NULL,
    project_undo_redo_position INTEGER NOT NULL,
    cross_project_isolation_verified BOOLEAN DEFAULT true,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- PROJECT-SCOPED INDEXES for performance isolation
CREATE INDEX idx_projects_user_id ON projects(user_id);
CREATE INDEX idx_projects_active ON projects(is_active, last_accessed_at);
CREATE INDEX idx_companies_project_id ON companies(project_id);
CREATE INDEX idx_gmc_reports_project_id ON gmc_reports(project_id);
CREATE INDEX idx_analysis_sessions_project_id ON analysis_sessions(project_id);
CREATE INDEX idx_parameter_changes_project_id ON parameter_changes(project_id);
CREATE INDEX idx_parameter_changes_session ON parameter_changes(session_id, project_undo_redo_position);

-- PROJECT DATA ISOLATION TRIGGER FUNCTION
CREATE OR REPLACE FUNCTION verify_project_data_isolation() 
RETURNS TRIGGER AS $$
BEGIN
    -- Ensure all related data belongs to the same project
    IF TG_TABLE_NAME = 'analysis_sessions' THEN
        IF NOT EXISTS (SELECT 1 FROM companies WHERE company_id = NEW.company_id AND project_id = NEW.project_id) THEN
            RAISE EXCEPTION 'Cross-project data contamination prevented: company_id % does not belong to project_id %', NEW.company_id, NEW.project_id;
        END IF;
    ELSIF TG_TABLE_NAME = 'parameter_changes' THEN
        IF NOT EXISTS (SELECT 1 FROM analysis_sessions WHERE session_id = NEW.session_id AND project_id = NEW.project_id) THEN
            RAISE EXCEPTION 'Cross-project data contamination prevented: session_id % does not belong to project_id %', NEW.session_id, NEW.project_id;
        END IF;
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Apply project isolation triggers
CREATE TRIGGER trigger_project_isolation_analysis_sessions 
    BEFORE INSERT OR UPDATE ON analysis_sessions 
    FOR EACH ROW EXECUTE FUNCTION verify_project_data_isolation();

CREATE TRIGGER trigger_project_isolation_parameter_changes
    BEFORE INSERT OR UPDATE ON parameter_changes
    FOR EACH ROW EXECUTE FUNCTION verify_project_data_isolation();

-- Update timestamp trigger function
CREATE OR REPLACE FUNCTION update_modified_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Apply update timestamp triggers
CREATE TRIGGER update_projects_modtime BEFORE UPDATE ON projects FOR EACH ROW EXECUTE FUNCTION update_modified_column();
CREATE TRIGGER update_companies_modtime BEFORE UPDATE ON companies FOR EACH ROW EXECUTE FUNCTION update_modified_column();
CREATE TRIGGER update_gmc_reports_modtime BEFORE UPDATE ON gmc_reports FOR EACH ROW EXECUTE FUNCTION update_modified_column();
CREATE TRIGGER update_analysis_sessions_modtime BEFORE UPDATE ON analysis_sessions FOR EACH ROW EXECUTE FUNCTION update_modified_column();