# Deployment Architecture

Define deployment strategy supporting diverse academic institutional capabilities with cost optimization.

## Deployment Strategy

**Frontend Deployment:**
- **Platform:** Vercel Edge Functions with academic calendar-aware scaling
- **Build Command:** `npm run build:academic` with institutional configuration injection
- **Output Directory:** `dist/` optimized for academic bandwidth constraints and device diversity
- **CDN/Edge:** Global edge deployment with educational institution regional compliance (US-East for FERPA, EU-West for GDPR)

**Backend Deployment:**  
- **Platform:** Docker containers with academic institutional flexibility (self-hosted, cloud, or hybrid options)
- **Build Command:** `python -m build --academic-compliance` with institutional boundary configuration
- **Deployment Method:** Progressive deployment supporting basic static files to enterprise Kubernetes

**Academic Environment Optimization:**
- **AI Cost Management:** External API usage optimization with classical ML preprocessing, daily budget limits (<$10/day per institution), local Ollama fallback for cost-sensitive scenarios
- **Network Resilience:** Multi-region deployment with academic network compatibility testing, API fallback strategies for unreliable connections
- **Institutional Integration:** Campus authentication, LMS integration, academic calendar synchronization, and configurable local vs. cloud AI deployment
- **Regulatory Compliance:** Configurable data residency and privacy protection for international academic markets, local AI processing for FERPA-sensitive institutions

## Environments

| Environment | Frontend URL | Backend URL | Purpose | Academic Context | AI Configuration |
|-------------|--------------|-------------|---------|------------------|-------------------|
| **Development** | `localhost:3000` | `localhost:8000` | Developer testing and feature development | Synthetic academic data, full debugging | Local Ollama + OpenRouter (testing) |
| **Staging** | `staging.gmcdashboard.edu` | `api-staging.gmcdashboard.edu` | Faculty review and institutional pilot testing | Anonymous real academic data | Anthropic Pro + OpenRouter (limited) |
| **Production** | `app.gmcdashboard.edu` | `api.gmcdashboard.edu` | Live academic environment | Full FERPA compliance, audit logging | Anthropic Pro primary, Ollama fallback |
| **Institutional** | `gmc.{institution}.edu` | `gmc-api.{institution}.edu` | Self-hosted institutional deployment | Institution-controlled data residency | Local Ollama only (privacy-first) |

---
