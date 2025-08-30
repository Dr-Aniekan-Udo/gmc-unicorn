# GitHub Branch Protection Rules Configuration

## Repository Settings

### Main Branch Protection
Configure these settings for the `main` branch:

#### General
- ✅ Require a pull request before merging
- ✅ Require approvals: 1
- ✅ Dismiss stale PR approvals when new commits are pushed
- ✅ Require review from code owners
- ✅ Restrict pushes that create files larger than 100 MB

#### Status Checks
- ✅ Require status checks to pass before merging
- ✅ Require branches to be up to date before merging

**Required Status Checks:**
- `backend-test`
- `frontend-test`
- `integration-test`
- `security`

#### Restrictions
- ✅ Restrict pushes to matching branches
- ✅ Allow force pushes: ❌ (disabled)
- ✅ Allow deletions: ❌ (disabled)

### Develop Branch Protection
Configure these settings for the `develop` branch:

#### General
- ✅ Require a pull request before merging
- ✅ Require approvals: 1
- ✅ Dismiss stale PR approvals when new commits are pushed

#### Status Checks
- ✅ Require status checks to pass before merging
- ✅ Require branches to be up to date before merging

**Required Status Checks:**
- `backend-test`
- `frontend-test`
- `integration-test`

## Repository Rules (Additional)

### File Restrictions
- Prevent commits to:
  - `*.env` files in root directory
  - `config/production/*.yml` files
  - `infrastructure/k8s/secrets/*.yml` files

### Commit Message Format
- Enforce conventional commits format:
  - `feat: add new feature`
  - `fix: resolve bug`
  - `docs: update documentation`
  - `test: add test cases`
  - `refactor: code restructuring`
  - `chore: maintenance tasks`

### Required Checks Before Merge
1. All CI/CD workflows must pass
2. No merge commits allowed (squash and merge only)
3. Branch must be up-to-date with target branch
4. All conversations must be resolved

## Secrets Configuration

### Required Repository Secrets
- `REGISTRY_URL`: Container registry URL
- `REGISTRY_USERNAME`: Container registry username  
- `REGISTRY_PASSWORD`: Container registry password
- `KUBECONFIG`: Base64 encoded Kubernetes config
- `PROD_BASE_URL`: Production application base URL

### Environment Secrets (Production)
- `DATABASE_URL`: Production database connection string
- `REDIS_URL`: Production Redis connection string
- `NEO4J_URI`: Production Neo4j connection string
- `SECRET_KEY`: Application secret key
- `JWT_SECRET_KEY`: JWT signing key

## Auto-merge Settings
- ✅ Enable auto-merge for dependabot PRs
- ✅ Require status checks for auto-merge
- ❌ Allow auto-merge without review (disabled for security)

## Instructions to Apply

1. Go to repository Settings > Branches
2. Add branch protection rule for `main`
3. Configure settings as specified above
4. Add branch protection rule for `develop`
5. Configure repository secrets in Settings > Secrets and variables > Actions
6. Enable dependabot security updates in Settings > Security & analysis