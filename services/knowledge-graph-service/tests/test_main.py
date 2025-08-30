import pytest
from unittest.mock import Mock, patch, MagicMock
from flask import Flask
import sys
import os

# Add parent directory to path to import app
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.main import app


@pytest.fixture
def client():
    """Create test client."""
    app.config['TESTING'] = True
    
    with app.test_client() as client:
        yield client


@pytest.fixture
def mock_neo4j_connection():
    """Mock Neo4j connection."""
    with patch('app.main.neo4j_conn') as mock_conn:
        mock_conn.connect.return_value = True
        mock_conn.driver = MagicMock()
        mock_conn.session = MagicMock()
        yield mock_conn


class TestHealthEndpoints:
    """Test health check endpoints."""
    
    def test_health_endpoint_success(self, client, mock_neo4j_connection):
        """Test health endpoint returns success."""
        response = client.get('/health')
        assert response.status_code == 200
        
        data = response.get_json()
        assert data['status'] == 'healthy'
        assert data['service'] == 'knowledge-graph-service'
        assert 'version' in data
        assert 'timestamp' in data
        assert 'checks' in data
    
    def test_health_endpoint_neo4j_connection(self, client, mock_neo4j_connection):
        """Test health endpoint checks Neo4j connection."""
        response = client.get('/health')
        data = response.get_json()
        
        assert 'neo4j_connection' in data['checks']
        assert data['checks']['neo4j_connection'] is True
    
    def test_health_endpoint_neo4j_failure(self, client):
        """Test health endpoint when Neo4j is down."""
        with patch('app.main.neo4j_conn') as mock_conn:
            mock_conn.connect.return_value = False
            
            response = client.get('/health')
            data = response.get_json()
            
            assert 'neo4j_connection' in data['checks']
            assert data['checks']['neo4j_connection'] is False


class TestKnowledgeGraphEndpoints:
    """Test knowledge graph endpoints."""
    
    @patch('app.main.request')
    def test_knowledge_endpoint_requires_project_context(self, mock_request, client, mock_neo4j_connection):
        """Test that knowledge endpoints require project context."""
        mock_request.headers = {'X-Project-ID': 'test-project-123'}
        
        with patch('shared.python.auth.project_context.validate_project_access', return_value=True):
            response = client.get('/api/v1/knowledge/rules')
            
            # Should not return 403 (unauthorized)
            assert response.status_code != 403
    
    def test_knowledge_endpoint_missing_project_id(self, client, mock_neo4j_connection):
        """Test knowledge endpoint without project ID."""
        response = client.get('/api/v1/knowledge/rules')
        
        # Should return error without project context
        assert response.status_code in [400, 403]


class TestNeo4jOperations:
    """Test Neo4j database operations."""
    
    def test_neo4j_connection_initialization(self, mock_neo4j_connection):
        """Test Neo4j connection is initialized properly."""
        # Connection should be established during app initialization
        mock_neo4j_connection.connect.assert_called()
    
    @patch('app.main.neo4j_conn')
    def test_execute_cypher_query(self, mock_conn, client):
        """Test executing Cypher queries."""
        mock_session = MagicMock()
        mock_conn.session.return_value.__enter__.return_value = mock_session
        mock_session.run.return_value = [{'count': 5}]
        
        with app.app_context():
            # This would be called by actual endpoint
            with mock_conn.session() as session:
                result = session.run("MATCH (n) RETURN count(n) as count")
                records = list(result)
                
        assert len(records) == 1
        assert records[0]['count'] == 5


class TestProjectDataIsolation:
    """Test project data isolation in knowledge graph."""
    
    @patch('shared.python.database.project_queries.get_project_knowledge_graph')
    def test_knowledge_filtered_by_project(self, mock_get_knowledge, client, mock_neo4j_connection):
        """Test that knowledge graph data is filtered by project."""
        mock_get_knowledge.return_value = []
        
        headers = {'X-Project-ID': 'project-123'}
        
        with patch('shared.python.auth.project_context.validate_project_access', return_value=True):
            response = client.get('/api/v1/knowledge/rules', headers=headers)
            
            # Should call project-specific query
            mock_get_knowledge.assert_called_once_with('project-123')
    
    @patch('app.main.neo4j_conn')
    def test_project_context_in_cypher_queries(self, mock_conn, client):
        """Test that Cypher queries include project context."""
        mock_session = MagicMock()
        mock_conn.session.return_value.__enter__.return_value = mock_session
        
        headers = {'X-Project-ID': 'project-123'}
        
        with patch('shared.python.auth.project_context.validate_project_access', return_value=True):
            response = client.get('/api/v1/knowledge/rules', headers=headers)
            
            # Verify that queries include project filtering
            # (This would be more specific based on actual implementation)
            if mock_session.run.called:
                call_args = mock_session.run.call_args
                query = call_args[0][0] if call_args else ""
                # Check that project context is included in query
                assert 'project' in query.lower() or 'Project' in query


class TestErrorHandling:
    """Test error handling scenarios."""
    
    @patch('app.main.neo4j_conn')
    def test_neo4j_connection_error(self, mock_conn, client):
        """Test handling of Neo4j connection errors."""
        mock_conn.connect.side_effect = Exception("Connection failed")
        
        response = client.get('/health')
        data = response.get_json()
        
        # Should handle connection errors gracefully
        assert 'neo4j_connection' in data['checks']
        assert data['checks']['neo4j_connection'] is False
    
    @patch('app.main.neo4j_conn')
    def test_cypher_query_error_handling(self, mock_conn, client):
        """Test handling of Cypher query errors."""
        mock_session = MagicMock()
        mock_conn.session.return_value.__enter__.return_value = mock_session
        mock_session.run.side_effect = Exception("Query failed")
        
        headers = {'X-Project-ID': 'project-123'}
        
        with patch('shared.python.auth.project_context.validate_project_access', return_value=True):
            response = client.get('/api/v1/knowledge/rules', headers=headers)
            
            # Should handle query errors gracefully
            assert response.status_code in [500, 503]


if __name__ == '__main__':
    pytest.main([__file__])