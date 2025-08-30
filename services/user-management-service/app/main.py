"""
User Management Service - Main Application

Authentication, authorization, API key management,
and FERPA-compliant user data handling.
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import text
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import logging
import os
from datetime import datetime, timedelta
import uuid

# Initialize Flask app
app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret-key")
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "USER_DATABASE_URL", "postgresql://localhost/gmc_users"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY", "jwt-secret-key")
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=24)

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
    "name": "user-management-service",
    "version": "0.1.0",
    "port": 5003,
    "database": "postgresql",
    "description": "Authentication and API key management",
    "status": "active",
}


# Placeholder models - will be enhanced in next story
class User(db.Model):
    """Basic user model for authentication."""

    __tablename__ = "users"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(255), nullable=False)
    institution_id = db.Column(db.String(100), nullable=False)
    user_role = db.Column(db.String(50), default="student", nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint for Kubernetes liveness probe."""
    try:
        # Test database connection
        db.session.execute(text("SELECT 1"))
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
        # Test database connection and user table
        db.session.execute(text("SELECT 1"))
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
                {
                    "path": "/api/v1/auth/login",
                    "method": "POST",
                    "description": "User authentication",
                },
                {
                    "path": "/api/v1/auth/register",
                    "method": "POST",
                    "description": "User registration",
                },
                {
                    "path": "/api/v1/auth/profile",
                    "method": "GET",
                    "description": "Get user profile",
                },
                {"path": "/api/v1/api-keys", "method": "GET", "description": "List user API keys"},
                {"path": "/api/v1/api-keys", "method": "POST", "description": "Create API key"},
            ],
            "features": [
                "JWT-based authentication",
                "FERPA-compliant user management",
                "Encrypted API key storage",
                "Budget controls for AI services",
                "Institutional boundaries",
            ],
        }
    )


@app.route("/api/v1/auth/register", methods=["POST"])
def register_user():
    """Register a new user."""
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    data = request.get_json()

    # Basic validation
    required_fields = ["username", "email", "password", "full_name", "institution_id"]
    for field in required_fields:
        if not data.get(field):
            return jsonify({"error": f"{field} is required"}), 400

    # TODO: Implement full user registration with validation
    # TODO: Add password strength validation
    # TODO: Add email verification

    # Placeholder response
    return (
        jsonify(
            {
                "message": "User registration - placeholder response",
                "user_id": f"user_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
                "username": data.get("username"),
                "note": "Full user registration to be implemented in next story",
            }
        ),
        201,
    )


@app.route("/api/v1/auth/login", methods=["POST"])
def login_user():
    """Authenticate user and return JWT token."""
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400

    # TODO: Implement actual user authentication
    # TODO: Add password verification
    # TODO: Create proper JWT token

    # Placeholder response with demo JWT
    access_token = create_access_token(
        identity=username,
        additional_claims={"user_role": "student", "institution_id": "demo_institution"},
    )

    return jsonify(
        {
            "access_token": access_token,
            "user": {"username": username, "role": "student", "institution_id": "demo_institution"},
            "message": "Authentication - placeholder response",
            "note": "Full authentication to be implemented in next story",
        }
    )


@app.route("/api/v1/auth/profile", methods=["GET"])
@jwt_required()
def get_user_profile():
    """Get current user profile."""
    current_user = get_jwt_identity()

    # TODO: Implement actual user profile retrieval
    # TODO: Query user database

    return jsonify(
        {
            "user": {
                "username": current_user,
                "message": "User profile - placeholder response",
                "note": "Full profile management to be implemented in next story",
            }
        }
    )


@app.route("/api/v1/api-keys", methods=["GET"])
@jwt_required()
def list_api_keys():
    """List user's API keys."""
    current_user = get_jwt_identity()

    # TODO: Implement API key listing
    # TODO: Query user_api_credentials table

    return jsonify(
        {
            "api_keys": [],
            "user": current_user,
            "message": "API key management - placeholder response",
            "note": "Full API key management to be implemented in next story",
        }
    )


@app.route("/api/v1/api-keys", methods=["POST"])
@jwt_required()
def create_api_key():
    """Create new API key for user."""
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    current_user = get_jwt_identity()
    data = request.get_json()

    service_name = data.get("service_name")
    if service_name not in ["anthropic", "openrouter", "ollama"]:
        return jsonify({"error": "Invalid service name"}), 400

    # TODO: Implement API key encryption and storage
    # TODO: Add budget controls

    return jsonify(
        {
            "credential_id": f"cred_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
            "service_name": service_name,
            "user": current_user,
            "message": "API key creation - placeholder response",
            "note": "Full encrypted API key storage to be implemented in next story",
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
    port = int(os.environ.get("PORT", 5003))
    debug = os.environ.get("FLASK_ENV") == "development"

    logger.info(f"Starting {SERVICE_INFO['name']} on port {port}")
    logger.info(f"Debug mode: {debug}")

    app.run(host="0.0.0.0", port=port, debug=debug)
