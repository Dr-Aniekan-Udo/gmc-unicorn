"""
User Management Service

Authentication, authorization, API key management,
and FERPA-compliant user data handling.
"""

from typing import Dict, Any

SERVICE_CONFIG: Dict[str, Any] = {
    "name": "user-management-service",
    "version": "0.1.0", 
    "port": 5003,
    "database": "postgresql",
    "description": "Authentication and API key management"
}

__all__ = ["SERVICE_CONFIG"]