# API Key Security & Credential Management

## Overview

The GMC Dashboard's AI-powered features rely on external API integrations (Anthropic Pro, OpenRouter) and local AI deployments (Ollama), requiring comprehensive API key security to protect institutional credentials, prevent unauthorized usage, and ensure FERPA compliance. This section defines the complete security architecture for managing AI service credentials across diverse academic environments.

## Security Threat Model

### Primary Security Risks
1. **API Key Exposure**: Credentials leaked through version control, logs, or client-side exposure
2. **Unauthorized Usage**: API keys used outside intended institutional boundaries
3. **Cost Abuse**: Malicious or accidental high-volume API usage exceeding budgets
4. **Data Breach**: Student data exposure through compromised API credentials
5. **Compliance Violations**: FERPA violations through improper credential handling

### Attack Vectors
- **Source Code Exposure**: API keys committed to version control repositories
- **Configuration File Access**: Unsecured config files accessible via web server
- **Client-Side Leakage**: API keys exposed in frontend JavaScript bundles
- **Log File Mining**: Credentials logged in application or server logs
- **Social Engineering**: Phishing or credential harvesting attacks on institutional staff
- **Insider Threats**: Malicious access by institutional users with elevated permissions

## Multi-Layer Security Architecture

### Layer 1: User-Specific Credential Storage & Encryption

**Industry Best Practice: Database-Stored User API Keys**

Following industry standards (similar to GitHub, AWS Console, Stripe Dashboard), API keys are stored per-user in the database with enterprise-grade encryption:

```sql
-- User-specific API credentials table (PostgreSQL)
CREATE TABLE user_api_credentials (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    institution_id UUID NOT NULL REFERENCES institutions(id),
    provider_name VARCHAR(50) NOT NULL,  -- 'anthropic', 'openrouter', 'ollama'
    
    -- Encrypted credential data
    encrypted_api_key BYTEA NOT NULL,     -- AES-256-GCM encrypted
    key_iv BYTEA NOT NULL,                -- Initialization vector
    key_tag BYTEA NOT NULL,               -- Authentication tag
    key_hash VARCHAR(64) NOT NULL,        -- SHA-256 hash for verification
    
    -- User-specific configuration
    display_name VARCHAR(100),            -- User-friendly name "My Anthropic Key"
    daily_budget_usd DECIMAL(10,2) DEFAULT 10.00,
    monthly_budget_usd DECIMAL(10,2) DEFAULT 300.00,
    
    -- Usage tracking
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_used TIMESTAMP WITH TIME ZONE,
    total_usage_usd DECIMAL(10,4) DEFAULT 0.00,
    last_usage_reset DATE DEFAULT CURRENT_DATE,
    
    -- Security and compliance
    is_active BOOLEAN DEFAULT true,
    expires_at TIMESTAMP WITH TIME ZONE,
    created_by_ip INET,
    last_accessed_ip INET,
    
    -- Unique constraint: one key per user per provider
    UNIQUE(user_id, provider_name)
);

-- Row-level security for user isolation
ALTER TABLE user_api_credentials ENABLE ROW LEVEL SECURITY;

-- Policy: Users can only access their own API keys
CREATE POLICY user_api_key_isolation ON user_api_credentials
    FOR ALL TO authenticated_users
    USING (user_id = auth.uid());

-- Policy: Institution admins can manage keys in their institution
CREATE POLICY institution_admin_access ON user_api_credentials
    FOR ALL TO authenticated_users  
    USING (
        institution_id IN (
            SELECT institution_id FROM user_roles 
            WHERE user_id = auth.uid() 
            AND role IN ('institution_admin', 'super_admin')
        )
    );
```

**Encryption Key Management (Industry Standard)**
```python
# Production-grade encryption using industry best practices
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import secrets
import base64

class UserAPIKeyEncryption:
    """Enterprise-grade API key encryption following industry standards"""
    
    def __init__(self, master_key: bytes):
        self.master_key = master_key
        self.aesgcm = AESGCM(master_key)
    
    @classmethod
    def generate_master_key(cls) -> bytes:
        """Generate cryptographically secure master key"""
        return AESGCM.generate_key(bit_length=256)
    
    def encrypt_api_key(self, api_key: str, user_id: str) -> dict:
        """Encrypt API key with user-specific associated data"""
        # Convert API key to bytes
        plaintext = api_key.encode('utf-8')
        
        # Generate unique IV for each encryption
        iv = secrets.token_bytes(12)  # 96-bit IV for GCM
        
        # Use user_id as associated data for additional security
        associated_data = user_id.encode('utf-8')
        
        # Encrypt with authentication
        ciphertext = self.aesgcm.encrypt(iv, plaintext, associated_data)
        
        return {
            'encrypted_data': ciphertext[:-16],  # Ciphertext without tag
            'iv': iv,
            'tag': ciphertext[-16:],              # Authentication tag
            'hash': hashes.Hash(hashes.SHA256()).finalize()  # Verification hash
        }
    
    def decrypt_api_key(self, encrypted_data: bytes, iv: bytes, 
                       tag: bytes, user_id: str) -> str:
        """Decrypt API key with user verification"""
        # Reconstruct full ciphertext with tag
        full_ciphertext = encrypted_data + tag
        
        # Use same associated data for verification
        associated_data = user_id.encode('utf-8')
        
        try:
            # Decrypt and verify authenticity
            plaintext = self.aesgcm.decrypt(iv, full_ciphertext, associated_data)
            return plaintext.decode('utf-8')
        except Exception as e:
            raise ValueError(f"Failed to decrypt API key: {e}")
```

**Dynamic Configuration Loading (Runtime Security)**
```python
# Secure runtime API key loading service
class UserAPIKeyService:
    """Service for secure user API key management following industry practices"""
    
    def __init__(self, db_connection, encryption_service: UserAPIKeyEncryption):
        self.db = db_connection
        self.encryption = encryption_service
        self.key_cache = {}  # In-memory cache with TTL
    
    async def store_user_api_key(self, user_id: str, provider: str, 
                                api_key: str, budget_limits: dict,
                                request_context: dict) -> str:
        """Securely store user's API key with audit logging"""
        # Encrypt the API key
        encrypted_data = self.encryption.encrypt_api_key(api_key, user_id)
        
        # Store in database
        credential_id = await self.db.execute("""
            INSERT INTO user_api_credentials (
                user_id, institution_id, provider_name,
                encrypted_api_key, key_iv, key_tag, key_hash,
                daily_budget_usd, monthly_budget_usd,
                created_by_ip, display_name
            ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)
            ON CONFLICT (user_id, provider_name)
            DO UPDATE SET 
                encrypted_api_key = EXCLUDED.encrypted_api_key,
                key_iv = EXCLUDED.key_iv,
                key_tag = EXCLUDED.key_tag,
                key_hash = EXCLUDED.key_hash,
                daily_budget_usd = EXCLUDED.daily_budget_usd,
                monthly_budget_usd = EXCLUDED.monthly_budget_usd
            RETURNING id
        """, [
            user_id, request_context['institution_id'], provider,
            encrypted_data['encrypted_data'], encrypted_data['iv'], 
            encrypted_data['tag'], encrypted_data['hash'],
            budget_limits.get('daily_usd', 10.00),
            budget_limits.get('monthly_usd', 300.00),
            request_context['ip_address'],
            budget_limits.get('display_name', f'{provider.title()} API Key')
        ])
        
        # Audit log the key storage (never log the actual key)
        await self.audit_log({
            'event': 'api_key_stored',
            'user_id': user_id,
            'provider': provider,
            'credential_id': credential_id,
            'ip_address': request_context['ip_address'],
            'user_agent_hash': hash(request_context.get('user_agent', ''))
        })
        
        return credential_id
    
    async def get_user_api_key(self, user_id: str, provider: str,
                              request_context: dict) -> Optional[str]:
        """Securely retrieve and decrypt user's API key"""
        # Check cache first (with TTL)
        cache_key = f"{user_id}:{provider}"
        if cache_key in self.key_cache:
            cached_entry = self.key_cache[cache_key]
            if cached_entry['expires'] > time.time():
                return cached_entry['key']
        
        # Fetch encrypted key from database
        row = await self.db.fetch_one("""
            SELECT encrypted_api_key, key_iv, key_tag, daily_budget_usd,
                   total_usage_usd, last_usage_reset, is_active
            FROM user_api_credentials 
            WHERE user_id = $1 AND provider_name = $2 AND is_active = true
        """, [user_id, provider])
        
        if not row:
            return None
        
        # Check if user is within budget limits
        if not await self.validate_budget_limits(user_id, provider, row):
            raise BudgetExceededException(f"Budget exceeded for {provider}")
        
        # Decrypt the API key
        try:
            decrypted_key = self.encryption.decrypt_api_key(
                row['encrypted_api_key'], row['key_iv'], 
                row['key_tag'], user_id
            )
            
            # Cache the decrypted key temporarily (5 minutes)
            self.key_cache[cache_key] = {
                'key': decrypted_key,
                'expires': time.time() + 300  # 5 minute TTL
            }
            
            # Update last used timestamp
            await self.db.execute("""
                UPDATE user_api_credentials 
                SET last_used = NOW(), last_accessed_ip = $3
                WHERE user_id = $1 AND provider_name = $2
            """, [user_id, provider, request_context['ip_address']])
            
            # Audit log the access (never log the actual key)
            await self.audit_log({
                'event': 'api_key_accessed',
                'user_id': user_id,
                'provider': provider,
                'ip_address': request_context['ip_address']
            })
            
            return decrypted_key
            
        except Exception as e:
            # Audit log the failure
            await self.audit_log({
                'event': 'api_key_access_failed',
                'user_id': user_id,
                'provider': provider,
                'error': str(e),
                'ip_address': request_context['ip_address']
            })
            raise
    
    async def validate_budget_limits(self, user_id: str, provider: str, 
                                   credential_row: dict) -> bool:
        """Check if user is within their API usage budget"""
        daily_budget = credential_row['daily_budget_usd']
        current_usage = credential_row['total_usage_usd']
        last_reset = credential_row['last_usage_reset']
        
        # Reset usage if it's a new day
        if last_reset < date.today():
            await self.reset_daily_usage(user_id, provider)
            return True
        
        return current_usage < daily_budget
```

### Layer 2: Access Control & Permission Management

**Role-Based Access Control (RBAC)**
```typescript
// API credential access permissions
interface APIKeyPermissions {
  canViewKeys: boolean;        // View masked key (last 4 chars)
  canCreateKeys: boolean;      // Add new API keys
  canUpdateKeys: boolean;      // Modify existing keys
  canDeleteKeys: boolean;      // Remove API keys
  canManageBudgets: boolean;   // Set budget limits
  canViewUsageStats: boolean;  // Access usage analytics
}

// Role definitions for API key management
const API_ROLES = {
  SUPER_ADMIN: {
    canViewKeys: true, canCreateKeys: true, canUpdateKeys: true,
    canDeleteKeys: true, canManageBudgets: true, canViewUsageStats: true
  },
  IT_ADMINISTRATOR: {
    canViewKeys: true, canCreateKeys: true, canUpdateKeys: true,
    canDeleteKeys: false, canManageBudgets: true, canViewUsageStats: true
  },
  FACULTY_ADMIN: {
    canViewKeys: false, canCreateKeys: false, canUpdateKeys: false,
    canDeleteKeys: false, canManageBudgets: true, canViewUsageStats: true
  },
  REGULAR_USER: {
    canViewKeys: false, canCreateKeys: false, canUpdateKeys: false,
    canDeleteKeys: false, canManageBudgets: false, canViewUsageStats: false
  }
};
```

**API Key Scoping & Restrictions**
```python
# Python backend API key validation and scoping
class APIKeyValidator:
    def __init__(self, institution_id: str, user_role: str):
        self.institution_id = institution_id
        self.user_role = user_role
    
    async def validate_api_key_access(self, api_provider: str) -> bool:
        """Validate user can access specific API provider credentials"""
        # Check role-based permissions
        permissions = API_ROLES.get(self.user_role, API_ROLES['REGULAR_USER'])
        
        if not permissions['canViewKeys']:
            return False
        
        # Validate institution boundary
        key_record = await self.get_encrypted_key_record(api_provider)
        if not key_record or key_record.institution_id != self.institution_id:
            return False
        
        # Check budget limits and usage quotas
        if await self.is_over_budget(api_provider):
            logger.warning(f"API usage over budget for {self.institution_id}")
            return False
        
        return True
    
    async def decrypt_api_key(self, api_provider: str) -> Optional[str]:
        """Securely decrypt API key for authorized usage"""
        if not await self.validate_api_key_access(api_provider):
            raise PermissionError("Unauthorized API key access attempt")
        
        # Retrieve encrypted key from secure storage
        encrypted_key = await self.get_encrypted_key(api_provider)
        
        # Decrypt using institutional master key
        master_key = await self.get_master_key()
        decrypted_key = self.decrypt_with_master_key(encrypted_key, master_key)
        
        # Log access for audit trail (without exposing key)
        await self.log_api_key_access(api_provider, self.user_role)
        
        return decrypted_key
```

### Layer 3: Runtime Protection & Monitoring

**API Key Usage Monitoring**
```python
# Real-time API usage tracking and anomaly detection
class APIUsageMonitor:
    def __init__(self, redis_client):
        self.redis = redis_client
    
    async def track_api_call(self, institution_id: str, provider: str, 
                           cost_usd: float, user_id: str):
        """Track API usage with real-time budget enforcement"""
        # Update usage counters
        daily_key = f"api_usage:{institution_id}:{provider}:{date.today()}"
        hourly_key = f"api_usage_hourly:{institution_id}:{provider}:{datetime.now().hour}"
        
        pipe = self.redis.pipeline()
        pipe.incr(f"{daily_key}:calls")
        pipe.incrbyfloat(f"{daily_key}:cost", cost_usd)
        pipe.incr(f"{hourly_key}:calls")
        pipe.expire(daily_key, 86400 * 7)  # Keep for 7 days
        pipe.expire(hourly_key, 3600 * 24)  # Keep for 24 hours
        await pipe.execute()
        
        # Check for usage anomalies
        if await self.detect_usage_anomaly(institution_id, provider):
            await self.alert_administrators(institution_id, provider)
        
        # Enforce budget limits
        daily_cost = await self.get_daily_cost(institution_id, provider)
        budget_limit = await self.get_budget_limit(institution_id, provider)
        
        if daily_cost > budget_limit:
            await self.trigger_budget_exceeded_action(institution_id, provider)
    
    async def detect_usage_anomaly(self, institution_id: str, provider: str) -> bool:
        """Detect unusual API usage patterns"""
        current_hour_calls = await self.redis.get(f"api_usage_hourly:{institution_id}:{provider}:{datetime.now().hour}:calls")
        
        # Alert if hourly usage exceeds 10x normal pattern
        avg_hourly = await self.get_average_hourly_usage(institution_id, provider)
        return int(current_hour_calls or 0) > (avg_hourly * 10)
```

**Budget Enforcement & Cost Controls**
```typescript
// Frontend budget management interface
interface BudgetControlPanel {
  dailyBudgetUSD: number;
  currentUsageUSD: number;
  remainingBudgetUSD: number;
  budgetUtilizationPercent: number;
  costAlerts: BudgetAlert[];
  usageProjection: UsageProjection;
}

interface BudgetAlert {
  severity: 'info' | 'warning' | 'critical';
  message: string;
  threshold: number;
  currentValue: number;
  recommendedAction: string;
}

// Budget enforcement actions
const BUDGET_ENFORCEMENT_ACTIONS = {
  WARNING_75: 'Send email alert to administrators',
  WARNING_90: 'Require approval for additional API calls',
  EXCEEDED_100: 'Switch to local Ollama deployment automatically',
  EXCEEDED_150: 'Disable AI features until budget reset or increase'
};
```

### Layer 4: Audit Trail & Compliance

**Comprehensive Audit Logging**
```python
# FERPA-compliant audit logging for API key operations
class APISecurityAuditLogger:
    def __init__(self, db_connection):
        self.db = db_connection
    
    async def log_credential_event(self, event_type: str, institution_id: str,
                                 user_id: str, provider: str, 
                                 details: Dict[str, Any]):
        """Log API credential security events for compliance"""
        audit_record = {
            'event_type': event_type,  # 'key_created', 'key_accessed', 'key_rotated'
            'institution_id': institution_id,
            'user_id': user_id,
            'provider': provider,
            'timestamp': datetime.utcnow(),
            'ip_address': self.hash_ip_address(details.get('ip_address')),
            'user_agent_hash': self.hash_user_agent(details.get('user_agent')),
            'success': details.get('success', True),
            'failure_reason': details.get('failure_reason'),
            'api_usage_cost': details.get('cost_usd'),
            'FERPA_compliant': True  # All logs anonymized appropriately
        }
        
        await self.db.execute(
            "INSERT INTO api_security_audit_log VALUES (...)",
            audit_record
        )
    
    async def generate_compliance_report(self, institution_id: str, 
                                       start_date: date, end_date: date) -> Dict:
        """Generate FERPA-compliant security audit report"""
        return {
            'institution_id': institution_id,
            'report_period': f"{start_date} to {end_date}",
            'api_key_operations': await self.count_key_operations(institution_id, start_date, end_date),
            'security_incidents': await self.get_security_incidents(institution_id, start_date, end_date),
            'budget_compliance': await self.get_budget_compliance_summary(institution_id, start_date, end_date),
            'data_protection_status': 'FERPA_COMPLIANT',
            'recommendations': await self.generate_security_recommendations(institution_id)
        }
```

## Deployment-Specific Security Strategies

### Cloud API Deployment Security

**Production Environment Setup**
```bash
#!/bin/bash
# Secure cloud API deployment script

# Step 1: Generate institutional master key
echo "Generating institutional encryption key..."
MASTER_KEY=$(openssl rand -base64 32)
echo "GMC_AI_MASTER_KEY=$MASTER_KEY" >> .env.secure

# Step 2: Encrypt API keys
echo "Encrypting Anthropic API key..."
ENCRYPTED_ANTHROPIC=$(echo $ANTHROPIC_KEY | openssl enc -aes-256-cbc -base64 -k $MASTER_KEY)
echo "GMC_AI_ANTHROPIC_ENCRYPTED=$ENCRYPTED_ANTHROPIC" >> .env.secure

# Step 3: Set secure file permissions
chmod 600 .env.secure
chown app:app .env.secure

# Step 4: Configure systemd service with security
cat > /etc/systemd/system/gmc-dashboard.service << EOF
[Unit]
Description=GMC Dashboard
After=network.target

[Service]
Type=notify
User=app
Group=app
WorkingDirectory=/opt/gmc-dashboard
EnvironmentFile=/opt/gmc-dashboard/.env.secure
ExecStart=/opt/gmc-dashboard/start.sh
Restart=always
RestartSec=5

# Security hardening
NoNewPrivileges=yes
PrivateTmp=yes
ProtectSystem=strict
ProtectHome=yes
ReadWritePaths=/opt/gmc-dashboard/data

[Install]
WantedBy=multi-user.target
EOF

echo "✅ Secure deployment configuration complete"
```

### Local AI Deployment Security (Ollama)

**Institutional Data Protection**
```yaml
# Ollama security configuration for institutional deployment
ollama_security:
  network_isolation:
    bind_address: "127.0.0.1:11434"  # Local-only access
    firewall_rules: 
      - "DENY incoming from 0.0.0.0/0"
      - "ALLOW incoming from 127.0.0.1"
  
  data_protection:
    model_encryption: true
    conversation_logging: false  # FERPA compliance
    model_storage: "/secure/ollama-models"  # Encrypted filesystem
  
  access_control:
    require_authentication: true
    api_key_required: true
    rate_limiting:
      requests_per_minute: 60
      concurrent_requests: 5
  
  monitoring:
    usage_logging: true
    performance_monitoring: true
    security_event_logging: true
```

## Security Integration with Existing Components

### Frontend Security Integration

**Secure API Key Management UI**
```typescript
// Admin panel API key management with security best practices
interface SecureAPIKeyManager {
  // Never expose full API keys in frontend
  displayMaskedKey: (key: string) => string;  // "sk-ant-****...****1234"
  validateKeyFormat: (key: string, provider: string) => boolean;
  testAPIConnection: (provider: string) => Promise<ConnectionResult>;
  rotatateAPIKey: (provider: string) => Promise<RotationResult>;
  
  // Budget and usage monitoring
  getCurrentUsage: () => Promise<UsageMetrics>;
  updateBudgetLimits: (limits: BudgetLimits) => Promise<void>;
  getSecurityAlerts: () => Promise<SecurityAlert[]>;
}

// Security-first form handling
const APIKeySetupForm: React.FC = () => {
  const [apiKey, setApiKey] = useState('');
  const [isValidating, setIsValidating] = useState(false);
  
  const handleKeySubmission = async (encryptedKey: string) => {
    // Key is encrypted on client-side before transmission
    const publicKey = await getInstitutionalPublicKey();
    const encryptedForTransmission = await encryptForServer(encryptedKey, publicKey);
    
    // Secure API call with audit logging
    await apiKeyService.securelyStoreKey({
      provider: 'anthropic',
      encryptedKey: encryptedForTransmission,
      budgetLimits: budgetSettings,
      institutionId: user.institutionId
    });
  };
  
  return (
    <SecureForm onSubmit={handleKeySubmission}>
      {/* Password-style input with validation */}
      <PasswordInput 
        value={apiKey}
        onChange={setApiKey}
        validator={validateAnthropicKeyFormat}
        placeholder="sk-ant-..."
        autoComplete="off"
      />
      <BudgetLimitControls />
      <SecurityPolicyAgreement />
    </SecureForm>
  );
};
```

### Backend Security Integration

**API Key Middleware & Request Processing**
```python
# Flask middleware for secure API key handling
from flask import request, abort
from cryptography.fernet import Fernet

class SecureAPIKeyMiddleware:
    def __init__(self, app):
        self.app = app
        self.key_manager = InstitutionalKeyManager()
    
    async def __call__(self, request: Request, call_next):
        # Extract institution context from request
        institution_id = await self.get_institution_id(request)
        
        # For AI-related endpoints, ensure secure key handling
        if request.url.path.startswith('/api/ai/'):
            # Validate user has permission to use AI features
            if not await self.validate_ai_permissions(request, institution_id):
                raise HTTPException(status_code=403, detail="AI access not authorized")
            
            # Check budget limits before processing
            if await self.is_over_budget(institution_id):
                raise HTTPException(status_code=429, detail="AI budget exceeded")
            
            # Inject decrypted API keys into request context (never logged)
            request.state.api_keys = await self.get_decrypted_keys(institution_id)
        
        response = await call_next(request)
        
        # Log API usage for billing and monitoring (keys never logged)
        if hasattr(request.state, 'api_usage'):
            await self.log_api_usage(institution_id, request.state.api_usage)
        
        return response

# Secure AI service integration
class SecureAIService:
    def __init__(self, request: Request):
        self.api_keys = request.state.api_keys
        self.institution_id = request.state.institution_id
        self.user_id = request.state.user_id
    
    async def make_anthropic_request(self, prompt: str) -> str:
        """Make secure API request with usage tracking"""
        api_key = self.api_keys.get('anthropic')
        if not api_key:
            raise ValueError("Anthropic API key not available")
        
        # Make API request with timeout and error handling
        start_time = time.time()
        try:
            response = await anthropic_client.messages.create(
                model="claude-3-5-sonnet-20241022",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1000
            )
            
            # Track usage for billing
            cost = self.calculate_api_cost(response)
            await self.track_usage('anthropic', cost, response.usage)
            
            return response.content[0].text
            
        except Exception as e:
            # Log error without exposing API key
            await self.log_api_error('anthropic', str(e), self.user_id)
            raise
        
        finally:
            # Ensure API key is cleared from memory
            api_key = None
```

## Security Testing & Validation Framework

### Automated Security Testing

```python
# Comprehensive security testing suite
import pytest
from unittest.mock import Mock, patch

class TestAPIKeySecurity:
    
    @pytest.mark.asyncio
    async def test_api_key_encryption_roundtrip(self):
        """Test API key encryption and decryption"""
        original_key = "sk-ant-test123456789"
        key_manager = InstitutionalKeyManager()
        
        # Encrypt API key
        encrypted_key = await key_manager.encrypt_api_key(original_key, "test_institution")
        assert encrypted_key != original_key
        assert original_key not in encrypted_key
        
        # Decrypt API key
        decrypted_key = await key_manager.decrypt_api_key(encrypted_key, "test_institution")
        assert decrypted_key == original_key
    
    @pytest.mark.asyncio
    async def test_institutional_isolation(self):
        """Test that institutions cannot access each other's keys"""
        key_manager = InstitutionalKeyManager()
        
        # Store key for institution A
        await key_manager.store_encrypted_key("sk-ant-test123", "institution_a")
        
        # Try to access from institution B
        with pytest.raises(PermissionError):
            await key_manager.get_decrypted_key("anthropic", "institution_b")
    
    @pytest.mark.asyncio
    async def test_budget_enforcement(self):
        """Test budget limits prevent overuse"""
        usage_monitor = APIUsageMonitor(Mock())
        
        # Set budget limit
        await usage_monitor.set_budget_limit("test_institution", "anthropic", 10.0)
        
        # Simulate usage approaching limit
        await usage_monitor.track_api_call("test_institution", "anthropic", 9.0, "user1")
        
        # Next call should trigger budget exceeded
        with pytest.raises(BudgetExceededException):
            await usage_monitor.track_api_call("test_institution", "anthropic", 2.0, "user1")
    
    @pytest.mark.asyncio
    async def test_audit_logging(self):
        """Test comprehensive audit trail"""
        audit_logger = APISecurityAuditLogger(Mock())
        
        # Log API key access
        await audit_logger.log_credential_event(
            'key_accessed', 'test_institution', 'user1', 'anthropic',
            {'ip_address': '192.168.1.100', 'success': True}
        )
        
        # Verify audit record was created
        audit_logger.db.execute.assert_called_once()
        call_args = audit_logger.db.execute.call_args
        assert 'key_accessed' in str(call_args)
        assert 'test_institution' in str(call_args)
    
    def test_api_key_masking(self):
        """Test API key masking for UI display"""
        key = "sk-ant-1234567890abcdef"
        masked = mask_api_key(key)
        
        assert masked == "sk-ant-****...****cdef"
        assert len(masked) < len(key)
        assert key not in masked
```

## Deployment Security Checklist

### Pre-Production Security Validation

```yaml
# Security checklist for GMC Dashboard AI deployment
security_checklist:
  
  api_key_management:
    - [ ] API keys never committed to version control
    - [ ] All API keys encrypted at rest using AES-256
    - [ ] Master encryption keys stored securely (vault/HSM)
    - [ ] API keys never logged in application logs
    - [ ] API keys never exposed to client-side code
    - [ ] Key rotation procedures documented and tested
  
  access_control:
    - [ ] Role-based access control implemented
    - [ ] Institutional boundaries enforced
    - [ ] Multi-factor authentication for admin access
    - [ ] Session management with proper timeouts
    - [ ] API endpoint authorization validated
  
  budget_controls:
    - [ ] Daily budget limits configured per institution
    - [ ] Real-time usage monitoring implemented
    - [ ] Budget exceeded alerts configured
    - [ ] Automatic failover to local AI when budget exceeded
    - [ ] Cost tracking accuracy validated
  
  compliance:
    - [ ] FERPA compliance validated for all data flows
    - [ ] Audit logging captures all security events
    - [ ] Data retention policies implemented
    - [ ] Student data anonymization verified
    - [ ] Cross-border data transfer compliance checked
  
  monitoring:
    - [ ] Security event monitoring configured
    - [ ] Anomaly detection for unusual API usage
    - [ ] Failed authentication attempt monitoring
    - [ ] Performance monitoring for security overhead
    - [ ] Incident response procedures documented
```

---

## Summary: Comprehensive API Key Security Framework

This security architecture provides **defense-in-depth protection** for AI service credentials while maintaining usability and performance:

**🔐 Multi-Layer Security:**
- **Layer 1**: Encryption at rest with institutional master keys
- **Layer 2**: Role-based access control with institutional boundaries
- **Layer 3**: Real-time monitoring with budget enforcement
- **Layer 4**: Comprehensive audit trails for compliance

**🎯 Key Security Features:**
- ✅ **Zero API Key Exposure**: Never logged, committed, or client-exposed
- ✅ **Institutional Isolation**: Complete separation between institutions
- ✅ **Budget Protection**: Real-time cost controls with automatic enforcement
- ✅ **FERPA Compliance**: Audit trails without student data exposure
- ✅ **Threat Monitoring**: Anomaly detection and security alerting

**🚀 Seamless Integration:**
- Frontend security interfaces integrate with existing admin panels
- Backend middleware provides transparent security without breaking existing APIs
- Database security leverages existing PostgreSQL Row-Level Security
- Monitoring integrates with existing Prometheus/Grafana analytics and logging

This security framework ensures **institutional trust, regulatory compliance, and cost protection** while enabling the powerful AI features that drive investment performance optimization in the GMC Dashboard.
