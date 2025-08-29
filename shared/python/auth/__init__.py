"""
Shared Authentication and Authorization Components

Project context management, data isolation, and security utilities
for GMC Dashboard microservices.
"""

from .project_context import (
    ProjectContext,
    ProjectContextManager,
    require_project_context,
    project_scoped_query,
    ProjectIsolationMiddleware,
    project_manager,
)

__all__ = [
    "ProjectContext",
    "ProjectContextManager",
    "require_project_context",
    "project_scoped_query",
    "ProjectIsolationMiddleware",
    "project_manager",
]
