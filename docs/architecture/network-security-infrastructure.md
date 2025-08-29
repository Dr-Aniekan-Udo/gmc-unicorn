# Network Security & Infrastructure

## Production Network Security Rules

**Kubernetes Security Policies**
```yaml
# Network policies for microservices isolation
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: gmc-microservices-isolation
  namespace: gmc-dashboard
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          name: gmc-dashboard
    - podSelector:
        matchLabels:
          app: api-gateway
    ports:
    - protocol: TCP
      port: 8080
  egress:
  - to:
    - namespaceSelector:
        matchLabels:
          name: gmc-dashboard
    ports:
    - protocol: TCP
      port: 5432  # PostgreSQL
    - protocol: TCP  
      port: 7687  # Neo4j
    - protocol: TCP
      port: 8080  # Weaviate
    - protocol: TCP
      port: 27017 # MongoDB
    - protocol: TCP
      port: 6379  # Redis
    - protocol: TCP
      port: 9000  # ClickHouse
```

**Firewall Configurations**
```bash
# Educational institution firewall rules
# Allow HTTPS traffic to API Gateway only
iptables -A INPUT -p tcp --dport 443 -j ACCEPT
iptables -A INPUT -p tcp --dport 80 -j ACCEPT

# Block direct database access from external networks
iptables -A INPUT -p tcp --dport 5432 -s 10.0.0.0/8 -j ACCEPT
iptables -A INPUT -p tcp --dport 5432 -j DROP

# Allow internal service communication only
iptables -A INPUT -p tcp -s 172.16.0.0/16 --dport 8080 -j ACCEPT
iptables -A INPUT -p tcp -s 172.16.0.0/16 --dport 7687 -j ACCEPT

# Educational network integration
iptables -A INPUT -p tcp -s 192.168.0.0/16 --dport 443 -j ACCEPT
```

## Security Monitoring & Incident Response

**Prometheus Security Metrics**
```yaml
# Custom security metrics for educational compliance
groups:
- name: gmc_security_alerts
  rules:
  - alert: UnauthorizedDatabaseAccess
    expr: postgresql_connections{database="gmc_calculations"} > 100
    for: 5m
    labels:
      severity: critical
    annotations:
      summary: "Unusual database connection count detected"
      
  - alert: ProjectIsolationViolation  
    expr: increase(project_isolation_violations_total[5m]) > 0
    for: 1m
    labels:
      severity: critical
    annotations:
      summary: "Project data isolation boundary crossed"
      
  - alert: APIKeyBudgetExceeded
    expr: user_api_budget_usage_dollars > user_api_budget_limit_dollars
    for: 1m  
    labels:
      severity: warning
    annotations:
      summary: "User exceeded AI service budget limits"
```

**Incident Response Procedures**
```python
# Automated incident response for educational environment
class SecurityIncidentHandler:
    """Handles security incidents with FERPA compliance."""
    
    async def handle_project_isolation_violation(self, incident: SecurityIncident):
        """Respond to project data contamination attempt."""
        
        # Immediate containment
        await self.suspend_user_session(incident.user_id)
        await self.audit_project_access(incident.project_ids)
        
        # FERPA-compliant logging
        await self.log_privacy_incident(
            user_id=incident.user_id,
            affected_projects=incident.project_ids,
            timestamp=incident.timestamp,
            anonymize_student_data=True
        )
        
        # Educational context notification
        await self.notify_faculty_if_academic_integrity_concern(incident)
        
        # Recovery validation
        await self.validate_data_isolation_restoration()
```
