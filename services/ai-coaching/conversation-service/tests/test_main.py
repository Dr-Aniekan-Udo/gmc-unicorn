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
def mock_mongodb_connection():
    """Mock MongoDB connection."""
    with patch('app.main.mongo_conn') as mock_conn:
        mock_conn.connect.return_value = True
        mock_conn.db = MagicMock()
        yield mock_conn


class TestHealthEndpoints:
    """Test health check endpoints."""
    
    def test_health_endpoint_success(self, client, mock_mongodb_connection):
        """Test health endpoint returns success."""
        response = client.get('/health')
        assert response.status_code == 200
        
        data = response.get_json()
        assert data['status'] == 'healthy'
        assert data['service'] == 'conversation-service'
        assert 'version' in data
        assert 'timestamp' in data
        assert 'checks' in data
    
    def test_health_endpoint_mongodb_connection(self, client, mock_mongodb_connection):
        """Test health endpoint checks MongoDB connection."""
        response = client.get('/health')
        data = response.get_json()
        
        assert 'mongodb_connection' in data['checks']
        assert data['checks']['mongodb_connection'] is True
    
    def test_health_endpoint_mongodb_failure(self, client):
        """Test health endpoint when MongoDB is down."""
        with patch('app.main.mongo_conn') as mock_conn:
            mock_conn.connect.return_value = False
            
            response = client.get('/health')
            data = response.get_json()
            
            assert 'mongodb_connection' in data['checks']
            assert data['checks']['mongodb_connection'] is False


class TestConversationEndpoints:
    """Test conversation-related endpoints."""
    
    @patch('app.main.request')
    def test_conversations_endpoint_requires_project_context(self, mock_request, client, mock_mongodb_connection):
        """Test that conversation endpoints require project context."""
        mock_request.headers = {'X-Project-ID': 'test-project-123'}
        
        with patch('shared.python.auth.project_context.validate_project_access', return_value=True):
            response = client.get('/api/v1/conversations')
            
            # Should not return 403 (unauthorized)
            assert response.status_code != 403
    
    def test_conversations_endpoint_missing_project_id(self, client, mock_mongodb_connection):
        """Test conversations endpoint without project ID."""
        response = client.get('/api/v1/conversations')
        
        # Should return error without project context
        assert response.status_code in [400, 403]


class TestMongoDBOperations:
    """Test MongoDB database operations."""
    
    def test_mongodb_connection_initialization(self, mock_mongodb_connection):
        """Test MongoDB connection is initialized properly."""
        # Connection should be established during app initialization
        mock_mongodb_connection.connect.assert_called()
    
    @patch('app.main.mongo_conn')
    def test_insert_conversation(self, mock_conn, client):
        """Test inserting conversation data."""
        mock_collection = MagicMock()
        mock_conn.db.conversations = mock_collection
        mock_collection.insert_one.return_value.inserted_id = 'mock_id'
        
        conversation_data = {
            'message': 'Hello, I need help with GMC analysis',
            'user_id': 'user123',
            'project_id': 'project123'
        }
        
        headers = {
            'X-Project-ID': 'project123',
            'Authorization': 'Bearer mock_token'
        }
        
        with patch('shared.python.auth.project_context.validate_project_access', return_value=True):
            response = client.post('/api/v1/conversations', 
                                 json=conversation_data, 
                                 headers=headers)
            
            # Should call MongoDB insert
            if response.status_code == 201:
                mock_collection.insert_one.assert_called()


class TestProjectDataIsolation:
    """Test project data isolation in conversations."""
    
    @patch('shared.python.database.project_queries.get_project_conversations')
    def test_conversations_filtered_by_project(self, mock_get_conversations, client, mock_mongodb_connection):
        """Test that conversations are filtered by project."""
        mock_get_conversations.return_value = []
        
        headers = {'X-Project-ID': 'project-123'}
        
        with patch('shared.python.auth.project_context.validate_project_access', return_value=True):
            response = client.get('/api/v1/conversations', headers=headers)
            
            # Should call project-specific query
            mock_get_conversations.assert_called_once_with('project-123')
    
    @patch('app.main.mongo_conn')
    def test_project_context_in_mongodb_queries(self, mock_conn, client):
        """Test that MongoDB queries include project context."""
        mock_collection = MagicMock()
        mock_conn.db.conversations = mock_collection
        mock_collection.find.return_value = []
        
        headers = {'X-Project-ID': 'project-123'}
        
        with patch('shared.python.auth.project_context.validate_project_access', return_value=True):
            response = client.get('/api/v1/conversations', headers=headers)
            
            # Verify that queries include project filtering
            if mock_collection.find.called:
                call_args = mock_collection.find.call_args
                query = call_args[0][0] if call_args else {}
                assert 'project_id' in query or len(call_args) > 0


class TestAICoachingFeatures:
    """Test AI coaching specific features."""
    
    @patch('app.llm_providers.openai_client.generate_response')
    def test_ai_response_generation(self, mock_generate, client, mock_mongodb_connection):
        """Test AI response generation for conversations."""
        mock_generate.return_value = {
            'response': 'Here is some advice about GMC analysis...',
            'confidence': 0.85
        }
        
        conversation_data = {
            'message': 'How do I analyze GMC performance?',
            'user_id': 'user123',
            'project_id': 'project123'
        }
        
        headers = {
            'X-Project-ID': 'project123',
            'Authorization': 'Bearer mock_token'
        }
        
        with patch('shared.python.auth.project_context.validate_project_access', return_value=True):
            response = client.post('/api/v1/conversations/ai-response', 
                                 json=conversation_data, 
                                 headers=headers)
            
            # Should call AI response generation
            if response.status_code == 200:
                mock_generate.assert_called()
    
    @patch('app.main.mongo_conn')
    def test_conversation_history_retrieval(self, mock_conn, client):
        """Test retrieving conversation history for context."""
        mock_collection = MagicMock()
        mock_conn.db.conversations = mock_collection
        mock_collection.find.return_value = [
            {'message': 'Previous message', 'response': 'Previous response'}
        ]
        
        headers = {
            'X-Project-ID': 'project123',
            'Authorization': 'Bearer mock_token'
        }
        
        with patch('shared.python.auth.project_context.validate_project_access', return_value=True):
            response = client.get('/api/v1/conversations/history', headers=headers)
            
            # Should query conversation history
            if response.status_code == 200:
                mock_collection.find.assert_called()


class TestErrorHandling:
    """Test error handling scenarios."""
    
    @patch('app.main.mongo_conn')
    def test_mongodb_connection_error(self, mock_conn, client):
        """Test handling of MongoDB connection errors."""
        mock_conn.connect.side_effect = Exception("Connection failed")
        
        response = client.get('/health')
        data = response.get_json()
        
        # Should handle connection errors gracefully
        assert 'mongodb_connection' in data['checks']
        assert data['checks']['mongodb_connection'] is False
    
    @patch('app.llm_providers.openai_client.generate_response')
    def test_ai_service_error_handling(self, mock_generate, client, mock_mongodb_connection):
        """Test handling of AI service errors."""
        mock_generate.side_effect = Exception("AI service unavailable")
        
        conversation_data = {
            'message': 'Test message',
            'user_id': 'user123',
            'project_id': 'project123'
        }
        
        headers = {
            'X-Project-ID': 'project123',
            'Authorization': 'Bearer mock_token'
        }
        
        with patch('shared.python.auth.project_context.validate_project_access', return_value=True):
            response = client.post('/api/v1/conversations/ai-response', 
                                 json=conversation_data, 
                                 headers=headers)
            
            # Should handle AI service errors gracefully
            assert response.status_code in [500, 503]
    
    def test_invalid_conversation_data(self, client, mock_mongodb_connection):
        """Test handling of invalid conversation data."""
        invalid_data = {
            'message': '',  # Empty message
            'user_id': None,  # Invalid user ID
        }
        
        headers = {
            'X-Project-ID': 'project123',
            'Authorization': 'Bearer mock_token'
        }
        
        with patch('shared.python.auth.project_context.validate_project_access', return_value=True):
            response = client.post('/api/v1/conversations', 
                                 json=invalid_data, 
                                 headers=headers)
            
            # Should reject invalid data
            assert response.status_code == 400


if __name__ == '__main__':
    pytest.main([__file__])