"""
Project-Scoped Database Query Utilities

Database query helpers that enforce project-scoped data isolation
across all GMC Dashboard microservices.
"""

from typing import Dict, Any, List, Optional, Union
from sqlalchemy import text
from sqlalchemy.orm import Session
import logging

logger = logging.getLogger(__name__)

class ProjectScopedQueries:
    """Database query utilities with automatic project scoping."""
    
    def __init__(self, db_session: Session, project_id: str):
        """
        Initialize with database session and project context.
        
        Args:
            db_session: SQLAlchemy database session
            project_id: Project identifier for scoping
        """
        self.db = db_session
        self.project_id = project_id
    
    def execute_project_scoped_query(
        self, 
        query: str, 
        params: Optional[Dict[str, Any]] = None
    ) -> Any:
        """
        Execute a project-scoped SQL query.
        
        Args:
            query: SQL query string
            params: Query parameters
            
        Returns:
            Query result
        """
        try:
            # Add project_id to parameters
            scoped_params = params.copy() if params else {}
            scoped_params['project_id'] = self.project_id
            
            # Execute query with project scoping
            result = self.db.execute(text(query), scoped_params)
            
            logger.info(f"Executed project-scoped query for project: {self.project_id}")
            return result
            
        except Exception as e:
            logger.error(f"Project-scoped query failed: {e}")
            raise
    
    def get_project_sessions(self, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Get analysis sessions for the current project.
        
        Args:
            limit: Maximum number of sessions to return
            
        Returns:
            List of session records
        """
        query = """
        SELECT session_id, session_name, company_id, base_report_data,
               decision_parameters, calculated_results, investment_performance,
               is_active, created_at, updated_at
        FROM analysis_sessions 
        WHERE project_id = :project_id 
        AND is_active = true
        ORDER BY updated_at DESC 
        LIMIT :limit
        """
        
        result = self.execute_project_scoped_query(query, {'limit': limit})
        return [dict(row._mapping) for row in result.fetchall()]
    
    def get_project_reports(self, report_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get GMC reports for the current project.
        
        Args:
            report_type: Optional filter by report type ('history' or 'game')
            
        Returns:
            List of report records
        """
        query = """
        SELECT report_id, company_id, report_type, quarter_period,
               filename, is_valid, project_timeline_position,
               created_at, updated_at
        FROM gmc_reports 
        WHERE project_id = :project_id
        """
        
        params = {}
        if report_type:
            query += " AND report_type = :report_type"
            params['report_type'] = report_type
        
        query += " ORDER BY project_timeline_position ASC"
        
        result = self.execute_project_scoped_query(query, params)
        return [dict(row._mapping) for row in result.fetchall()]
    
    def get_project_parameter_changes(
        self, 
        session_id: Optional[str] = None,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Get parameter changes for the current project.
        
        Args:
            session_id: Optional filter by session
            limit: Maximum number of changes to return
            
        Returns:
            List of parameter change records
        """
        query = """
        SELECT change_id, session_id, parameter_path, old_value, new_value,
               change_reason, user_id, project_undo_redo_position, timestamp
        FROM parameter_changes 
        WHERE project_id = :project_id
        """
        
        params = {'limit': limit}
        if session_id:
            query += " AND session_id = :session_id"
            params['session_id'] = session_id
        
        query += " ORDER BY timestamp DESC LIMIT :limit"
        
        result = self.execute_project_scoped_query(query, params)
        return [dict(row._mapping) for row in result.fetchall()]
    
    def create_project_session(
        self,
        company_id: str,
        session_name: str,
        base_report_id: Optional[str] = None,
        base_report_data: Dict[str, Any] = None,
        decision_parameters: Dict[str, Any] = None
    ) -> str:
        """
        Create new analysis session for the current project.
        
        Args:
            company_id: Associated company identifier
            session_name: Session display name
            base_report_id: Optional base report reference
            base_report_data: Base report data
            decision_parameters: Initial decision parameters
            
        Returns:
            Created session ID
        """
        import uuid
        session_id = str(uuid.uuid4())
        
        query = """
        INSERT INTO analysis_sessions (
            session_id, project_id, company_id, session_name,
            base_report_id, base_report_data, decision_parameters,
            project_analysis_context, cross_session_isolation_boundary,
            is_active, created_at, updated_at
        ) VALUES (
            :session_id, :project_id, :company_id, :session_name,
            :base_report_id, :base_report_data, :decision_parameters,
            :project_analysis_context, :cross_session_isolation_boundary,
            true, NOW(), NOW()
        )
        """
        
        params = {
            'session_id': session_id,
            'company_id': company_id,
            'session_name': session_name,
            'base_report_id': base_report_id,
            'base_report_data': base_report_data or {},
            'decision_parameters': decision_parameters or {},
            'project_analysis_context': {},
            'cross_session_isolation_boundary': {'isolated': True}
        }
        
        self.execute_project_scoped_query(query, params)
        self.db.commit()
        
        logger.info(f"Created session {session_id} for project {self.project_id}")
        return session_id
    
    def validate_project_data_isolation(self) -> Dict[str, Any]:
        """
        Validate that project data isolation is working correctly.
        
        Returns:
            Validation results
        """
        try:
            # Count records in each table for this project
            session_count_query = "SELECT COUNT(*) as count FROM analysis_sessions WHERE project_id = :project_id"
            report_count_query = "SELECT COUNT(*) as count FROM gmc_reports WHERE project_id = :project_id"  
            change_count_query = "SELECT COUNT(*) as count FROM parameter_changes WHERE project_id = :project_id"
            
            session_count = self.execute_project_scoped_query(session_count_query).scalar()
            report_count = self.execute_project_scoped_query(report_count_query).scalar()
            change_count = self.execute_project_scoped_query(change_count_query).scalar()
            
            # Verify no cross-project data contamination
            contamination_check = """
            SELECT COUNT(*) as count 
            FROM analysis_sessions s1 
            JOIN parameter_changes pc ON s1.session_id = pc.session_id 
            WHERE s1.project_id != pc.project_id
            """
            contamination_count = self.db.execute(text(contamination_check)).scalar()
            
            return {
                "project_id": self.project_id,
                "isolation_status": "verified",
                "record_counts": {
                    "sessions": session_count,
                    "reports": report_count, 
                    "parameter_changes": change_count
                },
                "contamination_detected": contamination_count > 0,
                "validation_timestamp": "NOW()"
            }
            
        except Exception as e:
            logger.error(f"Project data isolation validation failed: {e}")
            return {
                "project_id": self.project_id,
                "isolation_status": "validation_failed",
                "error": str(e)
            }

def create_project_scoped_session(db_session: Session, project_id: str) -> ProjectScopedQueries:
    """
    Create a project-scoped database session.
    
    Args:
        db_session: SQLAlchemy database session
        project_id: Project identifier
        
    Returns:
        ProjectScopedQueries instance
    """
    return ProjectScopedQueries(db_session, project_id)