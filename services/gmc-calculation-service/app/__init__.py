"""
GMC Calculation Service

Core mathematical engine for GMC analysis with Excel compatibility,
real-time parameter processing, and project-scoped data isolation.
"""

from typing import Dict, Any

SERVICE_CONFIG: Dict[str, Any] = {
    "name": "gmc-calculation-service",
    "version": "0.1.0",
    "port": 5000,
    "database": "postgresql",
    "description": "Core GMC mathematical calculation engine"
}

__all__ = ["SERVICE_CONFIG"]