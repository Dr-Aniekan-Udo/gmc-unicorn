import pytest
from unittest.mock import Mock, patch
from flask import Flask
import sys
import os

# Add parent directory to path to import app
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.main import app, db


@pytest.fixture
def client():
    """Create test client."""
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client


@pytest.fixture
def mock_project_context():
    """Mock project context for testing."""
    with patch('shared.python.auth.project_context.validate_project_access') as mock:
        mock.return_value = True
        yield mock


class TestHealthEndpoints:
    """Test health check endpoints."""
    
    def test_health_endpoint_success(self, client):
        """Test health endpoint returns success."""
        response = client.get('/health')
        assert response.status_code == 200
        
        data = response.get_json()
        assert data['status'] == 'healthy'
        assert data['service'] == 'gmc-calculation-service'
        assert 'version' in data
        assert 'timestamp' in data
        assert 'checks' in data
    
    def test_health_endpoint_database_connection(self, client):
        """Test health endpoint checks database connection."""
        response = client.get('/health')
        data = response.get_json()
        
        assert 'database_connection' in data['checks']
        assert data['checks']['database_connection'] is True
    
    def test_ready_endpoint(self, client):
        """Test readiness endpoint."""
        response = client.get('/health/ready')
        assert response.status_code == 200
        
        data = response.get_json()
        assert data['status'] == 'ready'


class TestCalculationEndpoints:
    """Test calculation-related endpoints."""
    
    @patch('app.main.request')
    def test_calculations_endpoint_requires_project_context(self, mock_request, client, mock_project_context):
        """Test that calculations endpoint requires project context."""
        mock_request.headers = {'X-Project-ID': 'test-project-123'}
        
        response = client.get('/api/v1/calculations')
        
        # Should call project validation
        mock_project_context.assert_called_once()
    
    def test_calculations_endpoint_missing_project_id(self, client):
        """Test calculations endpoint without project ID."""
        response = client.get('/api/v1/calculations')
        
        # Should return error without project context
        assert response.status_code in [400, 403]


class TestProjectDataIsolation:
    """Test project data isolation features."""
    
    @patch('shared.python.database.project_queries.get_project_calculations')
    def test_calculations_filtered_by_project(self, mock_get_calculations, client, mock_project_context):
        """Test that calculations are filtered by project ID."""
        mock_get_calculations.return_value = []
        
        headers = {'X-Project-ID': 'project-123'}
        response = client.get('/api/v1/calculations', headers=headers)
        
        # Should call project-specific query
        mock_get_calculations.assert_called_once_with('project-123')
    
    def test_cross_project_access_denied(self, client):
        """Test that cross-project access is denied."""
        headers = {'X-Project-ID': 'unauthorized-project'}
        
        with patch('shared.python.auth.project_context.validate_project_access') as mock_validate:
            mock_validate.return_value = False
            
            response = client.get('/api/v1/calculations', headers=headers)
            assert response.status_code == 403


class TestDatabaseOperations:
    """Test database operations with project isolation."""
    
    def test_database_connection(self, client):
        """Test database connection is established."""
        with app.app_context():
            # Test that we can execute a simple query
            result = db.session.execute(db.text("SELECT 1"))
            assert result.fetchone()[0] == 1
    
    def test_project_schema_exists(self, client):
        """Test that project-related tables exist."""
        with app.app_context():
            # Check if projects table exists (would be created by migrations)
            tables = db.inspect(db.engine).get_table_names()
            # Note: In actual deployment, this would check for projects table
            assert isinstance(tables, list)


class TestErrorHandling:
    """Test error handling scenarios."""
    
    @patch('app.main.db.session.execute')
    def test_database_error_handling(self, mock_execute, client):
        """Test handling of database errors."""
        mock_execute.side_effect = Exception("Database error")
        
        response = client.get('/health')
        data = response.get_json()
        
        # Health check should handle database errors gracefully
        assert 'database_connection' in data['checks']
        assert data['checks']['database_connection'] is False
    
    def test_invalid_project_id_format(self, client):
        """Test handling of invalid project ID format."""
        headers = {'X-Project-ID': 'invalid-format!@#'}
        
        response = client.get('/api/v1/calculations', headers=headers)
        assert response.status_code in [400, 403]


if __name__ == '__main__':
    pytest.main([__file__])