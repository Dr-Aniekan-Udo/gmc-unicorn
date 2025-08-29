# Database Architecture Enhancements

## Multi-Database Backup Strategy

### Backup Procedures by Database Type

**PostgreSQL (Core Services)**
```bash
# Automated encrypted backups with point-in-time recovery
# AES-256 encryption with separate key management

# gmc-calculation-service database
pg_dump --host=calc-db --username=gmc_calc \
  --verbose --clean --no-owner --no-acl \
  --format=custom gmc_calculations | \
  gpg --symmetric --cipher-algo AES256 \
  --output backup_calc_$(date +%Y%m%d_%H%M%S).pgdump.gpg

# user-management-service database  
pg_dump --host=user-db --username=gmc_users \
  --exclude-table=user_sessions \
  --verbose --clean --no-owner --no-acl \
  --format=custom gmc_users | \
  gpg --symmetric --cipher-algo AES256 \
  --output backup_users_$(date +%Y%m%d_%H%M%S).pgdump.gpg

# Automated restoration with project isolation validation
psql --host=restore-db --username=restore_user \
  --command="SET row_security = on;" \
  --dbname=gmc_calculations_restore < backup_calc.pgdump
```

**Neo4j (Knowledge Graph)**
```bash
# Graph database backup with relationship preservation
# GMC Manual knowledge graph and rule relationships

neo4j-admin backup --from=bolt://knowledge-graph:7687 \
  --backup-dir=/backups/neo4j/$(date +%Y%m%d_%H%M%S) \
  --database=neo4j \
  --verbose

# Encrypt backup directory
tar -czf - /backups/neo4j/latest | \
  gpg --symmetric --cipher-algo AES256 \
  --output neo4j_backup_$(date +%Y%m%d_%H%M%S).tar.gz.gpg
```

**Weaviate (Vector Database)**
```bash
# Vector embeddings backup with schema preservation
# GMC Manual semantic search and user query embeddings

curl -X GET "http://weaviate:8080/v1/objects" \
  -H "Content-Type: application/json" | \
  jq '.' > weaviate_objects_$(date +%Y%m%d_%H%M%S).json

# Schema backup
curl -X GET "http://weaviate:8080/v1/schema" \
  -H "Content-Type: application/json" | \
  jq '.' > weaviate_schema_$(date +%Y%m%d_%H%M%S).json

# Encrypt vector data
tar -czf - weaviate_*.json | \
  gpg --symmetric --cipher-algo AES256 \
  --output weaviate_backup_$(date +%Y%m%d_%H%M%S).tar.gz.gpg
```

**MongoDB (Content Management)**
```bash
# Document database backup with FERPA compliance
# GMC Manual content and AI coaching profiles

mongodump --host=content-db:27017 \
  --db=gmc_content \
  --collection=gmc_manual_content \
  --out=/backups/mongodb/$(date +%Y%m%d_%H%M%S)

mongodump --host=content-db:27017 \
  --db=ai_coaching \
  --collection=user_coaching_profiles \
  --out=/backups/mongodb/$(date +%Y%m%d_%H%M%S)

# Encrypt with institutional boundary preservation
tar -czf - /backups/mongodb/latest | \
  gpg --symmetric --cipher-algo AES256 \
  --output mongodb_backup_$(date +%Y%m%d_%H%M%S).tar.gz.gpg
```

**Redis (Session Management)**
```bash
# In-memory database backup with session preservation
# Real-time collaboration and notification state

redis-cli --rdb /backups/redis/dump_$(date +%Y%m%d_%H%M%S).rdb \
  BGSAVE

# Encrypt session data with user privacy protection
gpg --symmetric --cipher-algo AES256 \
  --output redis_backup_$(date +%Y%m%d_%H%M%S).rdb.gpg \
  /backups/redis/dump_latest.rdb
```

**ClickHouse (Analytics)**
```bash
# Time-series analytics backup with educational compliance
# Student performance metrics and faculty dashboard data

clickhouse-client --query="BACKUP DATABASE analytics \
  TO Disk('backups', 'analytics_$(date +%Y%m%d_%H%M%S).zip')"

# Encrypt analytics data with FERPA compliance
gpg --symmetric --cipher-algo AES256 \
  --output analytics_backup_$(date +%Y%m%d_%H%M%S).zip.gpg \
  analytics_latest.zip
```

## Migration Coordination Strategy

**Cross-Database Migration Orchestration**
```python
# Database migration coordinator with dependency management
# Ensures consistent schema updates across all 6 database types

class DatabaseMigrationOrchestrator:
    """Coordinates migrations across multiple database services."""
    
    async def execute_migration_batch(self, version: str) -> MigrationResult:
        """Execute coordinated migration across all databases."""
        
        # Phase 1: Core service databases (order matters)
        await self.migrate_postgresql_services([
            "user-management-service",
            "gmc-calculation-service", 
            "analytics-service"
        ])
        
        # Phase 2: Specialized databases (parallel execution)
        await asyncio.gather(
            self.migrate_neo4j_knowledge_graph(),
            self.migrate_weaviate_vectors(),
            self.migrate_mongodb_content(),
            self.migrate_clickhouse_analytics()
        )
        
        # Phase 3: Cache invalidation and session management
        await self.migrate_redis_sessions()
        
        # Validation: Test data consistency across services
        await self.validate_cross_database_integrity()
```
