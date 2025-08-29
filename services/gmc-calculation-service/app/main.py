"""
GMC Calculation Service - Main Application

Core mathematical engine for GMC analysis with Excel compatibility,
real-time parameter processing, and project-scoped data isolation.
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
import logging
import os
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret-key")
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL", "postgresql://localhost/gmc_calculations"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY", "jwt-secret-key")

# Initialize extensions
cors = CORS(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Service configuration
SERVICE_INFO = {
    "name": "gmc-calculation-service",
    "version": "0.1.0",
    "port": 5000,
    "database": "postgresql",
    "description": "Core GMC mathematical calculation engine",
    "status": "active",
}


@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint for Kubernetes liveness probe."""
    try:
        # Test database connection
        db.session.execute("SELECT 1")
        db_status = "healthy"
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        db_status = "unhealthy"

    return jsonify(
        {
            "status": "healthy" if db_status == "healthy" else "unhealthy",
            "service": SERVICE_INFO["name"],
            "version": SERVICE_INFO["version"],
            "timestamp": datetime.utcnow().isoformat(),
            "database": db_status,
            "checks": {"database_connection": db_status == "healthy", "service_ready": True},
        }
    ), (200 if db_status == "healthy" else 503)


@app.route("/health/ready", methods=["GET"])
def readiness_check():
    """Readiness check endpoint for Kubernetes readiness probe."""
    try:
        # Test database connection and basic functionality
        db.session.execute("SELECT 1")
        ready = True
        message = "Service ready"
    except Exception as e:
        logger.error(f"Readiness check failed: {e}")
        ready = False
        message = f"Service not ready: {str(e)}"

    return jsonify(
        {
            "ready": ready,
            "service": SERVICE_INFO["name"],
            "message": message,
            "timestamp": datetime.utcnow().isoformat(),
        }
    ), (200 if ready else 503)


@app.route("/api/v1/info", methods=["GET"])
def service_info():
    """Service information endpoint."""
    return jsonify(
        {
            "service": SERVICE_INFO,
            "endpoints": [
                {"path": "/health", "method": "GET", "description": "Health check"},
                {"path": "/health/ready", "method": "GET", "description": "Readiness check"},
                {"path": "/api/v1/info", "method": "GET", "description": "Service information"},
                {"path": "/api/v1/projects", "method": "GET", "description": "List projects"},
                {
                    "path": "/api/v1/projects/{project_id}/sessions",
                    "method": "GET",
                    "description": "List project sessions",
                },
                {
                    "path": "/api/v1/projects/{project_id}/calculate",
                    "method": "POST",
                    "description": "Calculate GMC parameters",
                },
            ],
            "features": [
                "Project-scoped data isolation",
                "Excel-compatible calculations",
                "Real-time parameter processing",
                "Investment performance analysis",
            ],
        }
    )


@app.route("/api/v1/projects", methods=["GET"])
def list_projects():
    """List accessible projects for the current user."""
    # TODO: Implement JWT authentication and user context
    # TODO: Query projects table with user permissions
    return jsonify(
        {
            "projects": [],
            "message": "Project listing requires authentication - to be implemented in next story",
        }
    )


@app.route("/api/v1/projects/<project_id>/sessions", methods=["GET"])
def list_project_sessions(project_id: str):
    """List analysis sessions for a specific project."""
    # TODO: Implement project validation and session querying
    return jsonify(
        {
            "project_id": project_id,
            "sessions": [],
            "message": "Session listing requires database models - to be implemented in next story",
        }
    )


@app.route("/api/v1/projects/<project_id>/calculate", methods=["POST"])
def calculate_gmc_parameters(project_id: str):
    """Calculate GMC parameters for a project session."""
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    data = request.get_json()

    # Basic validation
    if not data or "parameters" not in data:
        return jsonify({"error": "Parameters required"}), 400

    # TODO: Implement actual GMC calculations with Excel compatibility
    # TODO: Add project validation and database persistence

    # Placeholder response
    return jsonify(
        {
            "project_id": project_id,
            "calculation_id": f"calc_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
            "parameters": data.get("parameters", {}),
            "results": {
                "investment_performance": 0.0,
                "message": "GMC calculation engine - placeholder response",
                "note": "Full calculation logic to be implemented in next story",
            },
            "timestamp": datetime.utcnow().isoformat(),
        }
    )


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return (
        jsonify(
            {
                "error": "Not Found",
                "message": "The requested resource was not found",
                "service": SERVICE_INFO["name"],
            }
        ),
        404,
    )


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    logger.error(f"Internal server error: {error}")
    return (
        jsonify(
            {
                "error": "Internal Server Error",
                "message": "An internal error occurred",
                "service": SERVICE_INFO["name"],
            }
        ),
        500,
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_ENV") == "development"

    logger.info(f"Starting {SERVICE_INFO['name']} on port {port}")
    logger.info(f"Debug mode: {debug}")

    app.run(host="0.0.0.0", port=port, debug=debug)
