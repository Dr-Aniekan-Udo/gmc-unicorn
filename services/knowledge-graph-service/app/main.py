"""
Knowledge Graph Service - Main Application

Neo4j-based GMC rule relationships, strategic reasoning,
and constraint dependency management with project contexts.
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager
import logging
import os
from datetime import datetime
from typing import Dict, Any, Optional
from neo4j import GraphDatabase
import json

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'jwt-secret-key')

# Neo4j configuration
NEO4J_URI = os.environ.get('NEO4J_URI', 'bolt://localhost:7687')
NEO4J_USER = os.environ.get('NEO4J_USER', 'neo4j')
NEO4J_PASSWORD = os.environ.get('NEO4J_PASSWORD', 'password')

# Initialize extensions
cors = CORS(app)
jwt = JWTManager(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Service configuration
SERVICE_INFO = {
    "name": "knowledge-graph-service",
    "version": "0.1.0", 
    "port": 5001,
    "database": "neo4j",
    "description": "GMC business rule relationships and strategic reasoning",
    "status": "active"
}

class Neo4jConnection:
    """Neo4j database connection manager."""
    
    def __init__(self):
        self.driver = None
        
    def connect(self) -> bool:
        """Establish connection to Neo4j."""
        try:
            self.driver = GraphDatabase.driver(
                NEO4J_URI,
                auth=(NEO4J_USER, NEO4J_PASSWORD)
            )
            # Test connection
            with self.driver.session() as session:
                result = session.run("RETURN 1 AS test")
                test_value = result.single()["test"]
                return test_value == 1
        except Exception as e:
            logger.error(f"Neo4j connection failed: {e}")
            return False
    
    def close(self):
        """Close Neo4j connection."""
        if self.driver:
            self.driver.close()
    
    def is_healthy(self) -> bool:
        """Check if connection is healthy."""
        try:
            with self.driver.session() as session:
                result = session.run("RETURN 1 AS health")
                return result.single()["health"] == 1
        except Exception:
            return False

# Initialize Neo4j connection
neo4j_conn = Neo4jConnection()

@app.before_first_request
def initialize_database():
    """Initialize Neo4j connection on startup."""
    connected = neo4j_conn.connect()
    if connected:
        logger.info("Neo4j connection established")
    else:
        logger.error("Failed to establish Neo4j connection")

@app.teardown_appcontext
def close_database(error):
    """Close database connection on teardown."""
    pass  # Connection will be closed on app shutdown

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for Kubernetes liveness probe."""
    try:
        neo4j_healthy = neo4j_conn.is_healthy()
        db_status = "healthy" if neo4j_healthy else "unhealthy"
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        db_status = "unhealthy"
        
    return jsonify({
        "status": "healthy" if db_status == "healthy" else "unhealthy",
        "service": SERVICE_INFO["name"],
        "version": SERVICE_INFO["version"],
        "timestamp": datetime.utcnow().isoformat(),
        "database": db_status,
        "checks": {
            "neo4j_connection": db_status == "healthy",
            "service_ready": True
        }
    }), 200 if db_status == "healthy" else 503

@app.route('/health/ready', methods=['GET'])
def readiness_check():
    """Readiness check endpoint for Kubernetes readiness probe."""
    try:
        neo4j_ready = neo4j_conn.is_healthy()
        ready = neo4j_ready
        message = "Service ready" if ready else "Neo4j not ready"
    except Exception as e:
        logger.error(f"Readiness check failed: {e}")
        ready = False
        message = f"Service not ready: {str(e)}"
        
    return jsonify({
        "ready": ready,
        "service": SERVICE_INFO["name"],
        "message": message,
        "timestamp": datetime.utcnow().isoformat()
    }), 200 if ready else 503

@app.route('/api/v1/info', methods=['GET'])
def service_info():
    """Service information endpoint."""
    return jsonify({
        "service": SERVICE_INFO,
        "endpoints": [
            {"path": "/health", "method": "GET", "description": "Health check"},
            {"path": "/health/ready", "method": "GET", "description": "Readiness check"},
            {"path": "/api/v1/info", "method": "GET", "description": "Service information"},
            {"path": "/api/v1/projects/{project_id}/rules", "method": "GET", "description": "Get GMC rules for project"},
            {"path": "/api/v1/projects/{project_id}/relationships", "method": "GET", "description": "Get rule relationships"},
            {"path": "/api/v1/projects/{project_id}/strategy", "method": "POST", "description": "Analyze strategy implications"}
        ],
        "features": [
            "GMC business rule relationships",
            "Strategic reasoning and analysis",
            "Constraint dependency management",
            "Project-scoped knowledge contexts"
        ]
    })

@app.route('/api/v1/projects/<project_id>/rules', methods=['GET'])
def get_project_rules(project_id: str):
    """Get GMC rules for a specific project."""
    if not neo4j_conn.is_healthy():
        return jsonify({"error": "Knowledge graph service unavailable"}), 503
    
    try:
        with neo4j_conn.driver.session() as session:
            # Query project-specific rules
            query = """
            MATCH (pc:ProjectContext {project_id: $project_id})-[:CONTAINS]->(rule:GMCRule)
            RETURN rule.id as id, rule.type as type, rule.description as description,
                   rule.formula as formula, rule.priority as priority,
                   rule.educational_explanation as explanation
            ORDER BY rule.priority DESC
            """
            result = session.run(query, project_id=project_id)
            
            rules = [dict(record) for record in result]
            
            return jsonify({
                "project_id": project_id,
                "rules": rules,
                "count": len(rules),
                "timestamp": datetime.utcnow().isoformat()
            })
            
    except Exception as e:
        logger.error(f"Error querying project rules: {e}")
        return jsonify({
            "error": "Failed to retrieve project rules",
            "message": str(e)
        }), 500

@app.route('/api/v1/projects/<project_id>/relationships', methods=['GET'])
def get_rule_relationships(project_id: str):
    """Get rule relationships for strategic analysis."""
    if not neo4j_conn.is_healthy():
        return jsonify({"error": "Knowledge graph service unavailable"}), 503
    
    try:
        with neo4j_conn.driver.session() as session:
            # Query rule relationships within project context
            query = """
            MATCH (pc:ProjectContext {project_id: $project_id})-[:CONTAINS]->(rule:GMCRule)
            OPTIONAL MATCH (rule)-[r]-(related)
            WHERE (pc)-[:CONTAINS]->(related) OR related:Parameter OR related:Strategy
            RETURN rule.id as source, type(r) as relationship, 
                   CASE 
                     WHEN related:GMCRule THEN related.id
                     WHEN related:Parameter THEN related.id
                     WHEN related:Strategy THEN related.id
                     ELSE 'unknown'
                   END as target,
                   labels(related) as target_type
            """
            result = session.run(query, project_id=project_id)
            
            relationships = []
            for record in result:
                if record["relationship"]:  # Only include records with relationships
                    relationships.append({
                        "source": record["source"],
                        "relationship": record["relationship"],
                        "target": record["target"],
                        "target_type": record["target_type"]
                    })
            
            return jsonify({
                "project_id": project_id,
                "relationships": relationships,
                "count": len(relationships),
                "timestamp": datetime.utcnow().isoformat()
            })
            
    except Exception as e:
        logger.error(f"Error querying rule relationships: {e}")
        return jsonify({
            "error": "Failed to retrieve rule relationships",
            "message": str(e)
        }), 500

@app.route('/api/v1/projects/<project_id>/strategy', methods=['POST'])
def analyze_strategy_implications(project_id: str):
    """Analyze strategy implications using knowledge graph."""
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400
        
    data = request.get_json()
    strategy_name = data.get('strategy')
    
    if not strategy_name:
        return jsonify({"error": "Strategy name required"}), 400
    
    # TODO: Implement full strategy analysis logic
    # Placeholder response
    return jsonify({
        "project_id": project_id,
        "strategy": strategy_name,
        "implications": {
            "message": "Strategy analysis - placeholder response",
            "note": "Full knowledge graph reasoning to be implemented in next story"
        },
        "timestamp": datetime.utcnow().isoformat()
    })

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({
        "error": "Not Found",
        "message": "The requested resource was not found",
        "service": SERVICE_INFO["name"]
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    logger.error(f"Internal server error: {error}")
    return jsonify({
        "error": "Internal Server Error",
        "message": "An internal error occurred",
        "service": SERVICE_INFO["name"]
    }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    logger.info(f"Starting {SERVICE_INFO['name']} on port {port}")
    logger.info(f"Debug mode: {debug}")
    logger.info(f"Neo4j URI: {NEO4J_URI}")
    
    app.run(host='0.0.0.0', port=port, debug=debug)