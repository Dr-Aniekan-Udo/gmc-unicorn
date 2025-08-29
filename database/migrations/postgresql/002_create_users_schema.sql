-- GMC Dashboard: User Management Schema
-- Authentication, API key management, and FERPA compliance

-- Users table for authentication
CREATE TABLE users (
    user_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    institution_id VARCHAR(100) NOT NULL, -- FERPA compliance boundary
    user_role VARCHAR(50) NOT NULL DEFAULT 'student' CHECK (user_role IN ('student', 'instructor', 'admin')),
    is_active BOOLEAN DEFAULT true,
    email_verified BOOLEAN DEFAULT false,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login_at TIMESTAMP
);

-- Individual user API credentials (encrypted storage)
CREATE TABLE user_api_credentials (
    credential_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    institution_id VARCHAR(100) NOT NULL, -- Institutional boundary for compliance
    service_name VARCHAR(50) NOT NULL CHECK (service_name IN ('anthropic', 'openrouter', 'ollama')),
    encrypted_api_key TEXT NOT NULL, -- AES-256-GCM encrypted
    key_iv VARCHAR(255) NOT NULL, -- Initialization vector
    key_tag VARCHAR(255) NOT NULL, -- Authentication tag
    daily_budget_usd DECIMAL(10,2) NOT NULL DEFAULT 10.00,
    monthly_budget_usd DECIMAL(10,2) NOT NULL DEFAULT 300.00,
    total_usage_usd DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP,
    last_used_at TIMESTAMP,
    UNIQUE (user_id, service_name)
);

-- API usage tracking for budget enforcement
CREATE TABLE api_usage_logs (
    usage_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    credential_id UUID NOT NULL REFERENCES user_api_credentials(credential_id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    service_name VARCHAR(50) NOT NULL,
    endpoint VARCHAR(255) NOT NULL,
    tokens_used INTEGER,
    cost_usd DECIMAL(10,4) NOT NULL,
    project_id UUID, -- Optional project context
    usage_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    request_metadata JSONB -- Additional request context
);

-- Session management
CREATE TABLE user_sessions (
    session_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    session_token VARCHAR(255) UNIQUE NOT NULL,
    ip_address INET,
    user_agent TEXT,
    is_active BOOLEAN DEFAULT true,
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_activity_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Audit logs for FERPA compliance
CREATE TABLE audit_logs (
    audit_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(user_id) ON DELETE SET NULL,
    action VARCHAR(100) NOT NULL,
    resource_type VARCHAR(100) NOT NULL,
    resource_id VARCHAR(255),
    project_id UUID, -- Optional project context
    institution_id VARCHAR(100) NOT NULL,
    ip_address INET,
    user_agent TEXT,
    details JSONB,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX idx_users_institution_id ON users(institution_id);
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_username ON users(username);

CREATE INDEX idx_api_credentials_user_id ON user_api_credentials(user_id);
CREATE INDEX idx_api_credentials_service ON user_api_credentials(service_name, is_active);

CREATE INDEX idx_api_usage_logs_credential_id ON api_usage_logs(credential_id);
CREATE INDEX idx_api_usage_logs_timestamp ON api_usage_logs(usage_timestamp);
CREATE INDEX idx_api_usage_logs_cost ON api_usage_logs(cost_usd);

CREATE INDEX idx_user_sessions_user_id ON user_sessions(user_id);
CREATE INDEX idx_user_sessions_token ON user_sessions(session_token);
CREATE INDEX idx_user_sessions_expires ON user_sessions(expires_at);

CREATE INDEX idx_audit_logs_user_id ON audit_logs(user_id);
CREATE INDEX idx_audit_logs_timestamp ON audit_logs(timestamp);
CREATE INDEX idx_audit_logs_institution ON audit_logs(institution_id);

-- Budget enforcement trigger
CREATE OR REPLACE FUNCTION check_api_budget()
RETURNS TRIGGER AS $$
DECLARE
    daily_total DECIMAL(10,2);
    monthly_total DECIMAL(10,2);
    credential_record RECORD;
BEGIN
    -- Get credential information
    SELECT daily_budget_usd, monthly_budget_usd 
    INTO credential_record
    FROM user_api_credentials 
    WHERE credential_id = NEW.credential_id;

    -- Check daily budget
    SELECT COALESCE(SUM(cost_usd), 0) INTO daily_total
    FROM api_usage_logs 
    WHERE credential_id = NEW.credential_id 
    AND usage_timestamp >= CURRENT_DATE;

    IF (daily_total + NEW.cost_usd) > credential_record.daily_budget_usd THEN
        RAISE EXCEPTION 'Daily budget exceeded for API credential %', NEW.credential_id;
    END IF;

    -- Check monthly budget
    SELECT COALESCE(SUM(cost_usd), 0) INTO monthly_total
    FROM api_usage_logs 
    WHERE credential_id = NEW.credential_id 
    AND usage_timestamp >= DATE_TRUNC('month', CURRENT_DATE);

    IF (monthly_total + NEW.cost_usd) > credential_record.monthly_budget_usd THEN
        RAISE EXCEPTION 'Monthly budget exceeded for API credential %', NEW.credential_id;
    END IF;

    -- Update total usage
    UPDATE user_api_credentials 
    SET total_usage_usd = total_usage_usd + NEW.cost_usd,
        last_used_at = CURRENT_TIMESTAMP
    WHERE credential_id = NEW.credential_id;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_check_api_budget
    BEFORE INSERT ON api_usage_logs
    FOR EACH ROW EXECUTE FUNCTION check_api_budget();

-- Apply update timestamp triggers
CREATE TRIGGER update_users_modtime BEFORE UPDATE ON users FOR EACH ROW EXECUTE FUNCTION update_modified_column();
CREATE TRIGGER update_user_sessions_activity BEFORE UPDATE ON user_sessions FOR EACH ROW EXECUTE FUNCTION update_modified_column();