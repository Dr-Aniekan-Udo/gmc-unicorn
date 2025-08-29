"""
AI Conversation Service - Main Application

Natural language interaction service with multi-provider LLM support,
project-scoped conversation memory, and educational context awareness.
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
import logging
import os
from datetime import datetime
from typing import Dict, Any, Optional

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'jwt-secret-key')

# MongoDB configuration
MONGODB_URL = os.environ.get('MONGODB_URL', 'mongodb://localhost:27017/gmc_coaching')

# Initialize extensions
cors = CORS(app)
jwt = JWTManager(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Service configuration
SERVICE_INFO = {
    "name": "conversation-service",
    "version": "0.1.0",
    "port": 5002,
    "database": "mongodb",
    "description": "Conversational AI with project-scoped memory",
    "status": "active"
}

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for Kubernetes liveness probe."""
    # TODO: Test MongoDB connection
    db_status = "healthy"  # Placeholder
        
    return jsonify({
        "status": "healthy",
        "service": SERVICE_INFO["name"],
        "version": SERVICE_INFO["version"],
        "timestamp": datetime.utcnow().isoformat(),
        "database": db_status,
        "checks": {
            "mongodb_connection": True,  # Placeholder
            "service_ready": True
        }
    })

@app.route('/health/ready', methods=['GET'])
def readiness_check():
    """Readiness check endpoint for Kubernetes readiness probe."""
    # TODO: Test MongoDB and AI provider connectivity
    ready = True
    message = "Service ready"
        
    return jsonify({
        "ready": ready,
        "service": SERVICE_INFO["name"],
        "message": message,
        "timestamp": datetime.utcnow().isoformat()
    })

@app.route('/api/v1/info', methods=['GET'])
def service_info():
    """Service information endpoint."""
    return jsonify({
        "service": SERVICE_INFO,
        "endpoints": [
            {"path": "/health", "method": "GET", "description": "Health check"},
            {"path": "/health/ready", "method": "GET", "description": "Readiness check"},
            {"path": "/api/v1/info", "method": "GET", "description": "Service information"},
            {"path": "/api/v1/projects/{project_id}/chat", "method": "POST", "description": "Send chat message"},
            {"path": "/api/v1/projects/{project_id}/history", "method": "GET", "description": "Get conversation history"},
            {"path": "/api/v1/llm-config", "method": "PUT", "description": "Configure LLM provider"}
        ],
        "features": [
            "Multi-provider LLM support",
            "Project-scoped conversation memory",
            "Educational context awareness",
            "Individual user API key management",
            "Budget controls and usage tracking"
        ]
    })

@app.route('/api/v1/projects/<project_id>/chat', methods=['POST'])
@jwt_required()
def send_chat_message(project_id: str):
    """Send chat message to AI coach."""
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400
        
    current_user = get_jwt_identity()
    data = request.get_json()
    message = data.get('message')
    
    if not message:
        return jsonify({"error": "Message required"}), 400
    
    # TODO: Implement actual AI conversation logic
    # TODO: Load project-scoped context
    # TODO: Query user's preferred LLM provider
    # TODO: Generate AI response with educational context
    
    # Placeholder response
    return jsonify({
        "project_id": project_id,
        "user": current_user,
        "user_message": message,
        "ai_response": "AI coaching response - placeholder",
        "conversation_id": f"conv_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
        "provider": "placeholder",
        "timestamp": datetime.utcnow().isoformat(),
        "note": "Full AI conversation to be implemented in next story"
    })

@app.route('/api/v1/projects/<project_id>/history', methods=['GET'])
@jwt_required()
def get_conversation_history(project_id: str):
    """Get conversation history for project."""
    current_user = get_jwt_identity()
    
    # TODO: Query MongoDB for project-scoped conversation history
    # TODO: Apply user permissions and data isolation
    
    return jsonify({
        "project_id": project_id,
        "user": current_user,
        "conversations": [],
        "message": "Conversation history - placeholder response",
        "note": "Full conversation storage to be implemented in next story"
    })

@app.route('/api/v1/llm-config', methods=['PUT'])
@jwt_required()
def configure_llm_provider():
    """Configure user's LLM provider preferences."""
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400
        
    current_user = get_jwt_identity()
    data = request.get_json()
    
    provider = data.get('provider')
    if provider not in ['openai', 'anthropic', 'gemini', 'ollama']:
        return jsonify({"error": "Invalid provider"}), 400
    
    # TODO: Update user's LLM provider configuration
    # TODO: Validate API keys and budget settings
    
    return jsonify({
        "user": current_user,
        "provider": provider,
        "message": "LLM configuration - placeholder response", 
        "note": "Full provider configuration to be implemented in next story"
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5002))
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    logger.info(f"Starting {SERVICE_INFO['name']} on port {port}")
    logger.info(f"Debug mode: {debug}")
    
    app.run(host='0.0.0.0', port=port, debug=debug)