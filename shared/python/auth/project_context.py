"""
Project Context Management for Data Isolation

Middleware and decorators for enforcing project-scoped data isolation
across all GMC Dashboard microservices.
"""

from functools import wraps
from typing import Dict, Any, Optional, List
from flask import request, jsonify, g
import logging
from dataclasses import dataclass
import uuid

logger = logging.getLogger(__name__)


@dataclass
class ProjectContext:
    """Project context for data isolation."""

    project_id: str
    user_id: str
    user_role: str
    institution_id: str
    team_members: List[str]
    project_permissions: Dict[str, Any]
    is_active: bool = True


class ProjectContextManager:
    """Manages project context validation and data isolation."""

    def __init__(self):
        self.active_contexts: Dict[str, ProjectContext] = {}

    def validate_project_access(
        self, project_id: str, user_id: str, required_permission: Optional[str] = None
    ) -> bool:
        """
        Validate user access to project.

        Args:
            project_id: Project identifier
            user_id: User identifier
            required_permission: Optional specific permission required

        Returns:
            True if access is granted, False otherwise
        """
        try:
            # TODO: Implement actual database query for project access
            # For now, basic validation logic

            if not project_id or not user_id:
                return False

            # Validate UUID format
            try:
                uuid.UUID(project_id)
            except ValueError:
                logger.warning(f"Invalid project_id format: {project_id}")
                return False

            # TODO: Query database for actual project permissions
            # This is a placeholder implementation
            return True

        except Exception as e:
            logger.error(f"Project access validation failed: {e}")
            return False

    def get_project_context(self, project_id: str, user_id: str) -> Optional[ProjectContext]:
        """
        Get project context for user.

        Args:
            project_id: Project identifier
            user_id: User identifier

        Returns:
            ProjectContext if access granted, None otherwise
        """
        try:
            # TODO: Query database for project details
            # This is a placeholder implementation

            if self.validate_project_access(project_id, user_id):
                return ProjectContext(
                    project_id=project_id,
                    user_id=user_id,
                    user_role="student",  # TODO: Get from database
                    institution_id="demo_institution",  # TODO: Get from database
                    team_members=[user_id],  # TODO: Get from database
                    project_permissions={"can_read": True, "can_write": True, "can_manage": False},
                    is_active=True,
                )

            return None

        except Exception as e:
            logger.error(f"Failed to get project context: {e}")
            return None

    def enforce_data_isolation(
        self, project_id: str, query_params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Enforce data isolation by adding project_id filter to queries.

        Args:
            project_id: Project identifier
            query_params: Query parameters

        Returns:
            Updated query parameters with project isolation
        """
        # Add project_id filter to all queries
        query_params["project_id"] = project_id

        # Log data isolation enforcement
        logger.info(f"Data isolation enforced for project: {project_id}")

        return query_params


# Global project context manager instance
project_manager = ProjectContextManager()


def require_project_context(permission: Optional[str] = None):
    """
    Decorator to require valid project context for API endpoints.

    Args:
        permission: Optional specific permission required

    Usage:
        @app.route('/api/v1/projects/<project_id>/data')
        @require_project_context('can_read')
        def get_project_data(project_id):
            # Access g.project_context for validated context
            return jsonify({"data": "project data"})
    """

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                # Extract project_id from URL parameters or request body
                project_id = kwargs.get("project_id")
                if not project_id and request.is_json:
                    data = request.get_json()
                    project_id = data.get("project_id") if data else None

                if not project_id:
                    return (
                        jsonify(
                            {
                                "error": "Project ID required",
                                "message": "project_id must be provided in URL or request body",
                            }
                        ),
                        400,
                    )

                # TODO: Get user_id from JWT token
                user_id = getattr(g, "current_user_id", "demo_user")

                # Validate project access
                if not project_manager.validate_project_access(project_id, user_id, permission):
                    return (
                        jsonify(
                            {
                                "error": "Project access denied",
                                "message": (
                                    f"User {user_id} does not have access to project "
                                    f"{project_id}"
                                ),
                            }
                        ),
                        403,
                    )

                # Get and store project context
                project_context = project_manager.get_project_context(project_id, user_id)
                if not project_context:
                    return (
                        jsonify(
                            {
                                "error": "Invalid project context",
                                "message": "Could not establish project context",
                            }
                        ),
                        403,
                    )

                # Store context in Flask g for use in endpoint
                g.project_context = project_context
                g.project_id = project_id

                # Log successful project context validation
                logger.info(f"Project context validated: {project_id} for user: {user_id}")

                return f(*args, **kwargs)

            except Exception as e:
                logger.error(f"Project context validation error: {e}")
                return (
                    jsonify(
                        {
                            "error": "Project context validation failed",
                            "message": "Internal error during project validation",
                        }
                    ),
                    500,
                )

        return decorated_function

    return decorator


def project_scoped_query(base_query: str, table_alias: str = "") -> str:
    """
    Add project scoping to SQL queries for data isolation.

    Args:
        base_query: Base SQL query
        table_alias: Optional table alias

    Returns:
        Query with project scoping added
    """
    project_id = getattr(g, "project_id", None)
    if not project_id:
        raise ValueError("Project context not available for query scoping")

    alias_prefix = f"{table_alias}." if table_alias else ""
    project_filter = f" AND {alias_prefix}project_id = '{project_id}'"

    # Add project filter to WHERE clause or create new WHERE clause
    if " WHERE " in base_query.upper():
        return base_query + project_filter
    else:
        return base_query + " WHERE" + project_filter[5:]  # Remove " AND"


class ProjectIsolationMiddleware:
    """Flask middleware for project data isolation."""

    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """Initialize middleware with Flask app."""
        app.before_request(self.before_request)
        app.after_request(self.after_request)

    def before_request(self):
        """Process request before handling."""
        # Log all project-scoped requests
        if "projects/" in request.path:
            logger.info(f"Project-scoped request: {request.method} {request.path}")

    def after_request(self, response):
        """Process response after handling."""
        # Add project isolation headers
        if hasattr(g, "project_id"):
            response.headers["X-Project-ID"] = g.project_id
            response.headers["X-Data-Isolation"] = "enforced"

        return response
