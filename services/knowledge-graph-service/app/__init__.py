"""
Knowledge Graph Service

Neo4j-based GMC rule relationships, strategic reasoning,
and constraint dependency management with project contexts.
"""

from typing import Dict, Any

SERVICE_CONFIG: Dict[str, Any] = {
    "name": "knowledge-graph-service", 
    "version": "0.1.0",
    "port": 5001,
    "database": "neo4j",
    "description": "GMC business rule relationships and strategic reasoning"
}

__all__ = ["SERVICE_CONFIG"]