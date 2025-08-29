"""
GMC Dashboard - Educational Analytics Platform for Strategic Business Analysis

A microservices-based platform for GMC analysis with project-scoped data isolation,
real-time collaboration, and AI-powered strategic optimization.
"""

__version__ = "0.1.0"
__author__ = "GMC Dashboard Team"
__email__ = "support@gmc-dashboard.com"

from typing import Dict, Any

# Project configuration constants
PROJECT_CONFIG: Dict[str, Any] = {
    "name": "gmc-app",
    "version": __version__,
    "description": "GMC Dashboard - Educational Analytics Platform",
    "python_requires": ">=3.12",
    "architecture": "microservices",
    "data_isolation": "project_scoped",
    "deployment": "kubernetes"
}

# Microservice configuration
MICROSERVICES: Dict[str, Dict[str, Any]] = {
    "gmc_calculation": {"port": 5000, "database": "postgresql"},
    "knowledge_graph": {"port": 5001, "database": "neo4j"}, 
    "user_management": {"port": 5003, "database": "postgresql"},
    "content_management": {"port": 5004, "database": "mongodb"},
    "analytics": {"port": 5005, "database": "postgresql+clickhouse"},
    "notification": {"port": 5006, "database": "redis"}
}

# AI Coaching Services
AI_SERVICES: Dict[str, Dict[str, Any]] = {
    "conversation": {"port": 5002, "database": "mongodb"},
    "vector_search": {"port": 5007, "database": "weaviate"},
    "ml_recommendation": {"port": 5008, "database": "mlflow"},
    "coaching_orchestrator": {"port": 5009, "database": "redis"}
}

__all__ = [
    "__version__",
    "__author__", 
    "__email__",
    "PROJECT_CONFIG",
    "MICROSERVICES",
    "AI_SERVICES"
]