"""
AI Conversation Service

Natural language interaction service with multi-provider LLM support,
project-scoped conversation memory, and educational context awareness.
"""

from typing import Dict, Any

SERVICE_CONFIG: Dict[str, Any] = {
    "name": "conversation-service",
    "version": "0.1.0",
    "port": 5002,
    "database": "mongodb", 
    "description": "Conversational AI with project-scoped memory"
}

__all__ = ["SERVICE_CONFIG"]