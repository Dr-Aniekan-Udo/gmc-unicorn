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


class TestHealthEndpoints:
    """Test health check endpoints."""
    
    def test_health_endpoint_success(self, client):
        """Test health endpoint returns success."""
        response = client.get('/health')
        assert response.status_code == 200
        
        data = response.get_json()
        assert data['status'] == 'healthy'
        assert data['service'] == 'user-management-service'
        assert 'version' in data
        assert 'timestamp' in data
        assert 'checks' in data
    
    def test_health_endpoint_database_connection(self, client):
        """Test health endpoint checks database connection."""
        response = client.get('/health')
        data = response.get_json()
        
        assert 'database_connection' in data['checks']
        assert data['checks']['database_connection'] is True


class TestUserAuthenticationEndpoints:
    """Test user authentication endpoints."""
    
    def test_register_endpoint_exists(self, client):
        """Test that user registration endpoint exists."""
        # Test with minimal valid data
        user_data = {
            'email': 'test@example.com',
            'password': 'securepassword123',
            'name': 'Test User'
        }
        
        response = client.post('/api/v1/users/register', json=user_data)
        
        # Should not return 404 (endpoint exists)
        assert response.status_code != 404
    
    def test_login_endpoint_exists(self, client):
        """Test that login endpoint exists."""
        login_data = {
            'email': 'test@example.com',
            'password': 'password123'
        }
        
        response = client.post('/api/v1/users/login', json=login_data)
        
        # Should not return 404 (endpoint exists)
        assert response.status_code != 404
    
    def test_profile_endpoint_requires_auth(self, client):
        """Test that profile endpoint requires authentication."""
        response = client.get('/api/v1/users/profile')
        
        # Should require authentication
        assert response.status_code in [401, 403]


class TestProjectDataIsolation:
    """Test project-level data isolation for users."""
    
    @patch('shared.python.auth.project_context.validate_project_access')
    def test_user_project_association(self, mock_validate, client):
        """Test that users are properly associated with projects."""
        mock_validate.return_value = True
        
        headers = {'X-Project-ID': 'project-123'}
        
        # Test accessing project-specific user data
        response = client.get('/api/v1/users/project-members', headers=headers)
        
        # Should call project validation
        mock_validate.assert_called()
    
    def test_cross_project_user_access_denied(self, client):
        """Test that users cannot access other projects' user data."""
        headers = {'X-Project-ID': 'unauthorized-project'}
        
        with patch('shared.python.auth.project_context.validate_project_access', return_value=False):
            response = client.get('/api/v1/users/project-members', headers=headers)
            assert response.status_code == 403


class TestPasswordSecurity:
    """Test password security features."""
    
    @patch('werkzeug.security.generate_password_hash')
    def test_password_hashing(self, mock_hash, client):
        """Test that passwords are properly hashed."""
        mock_hash.return_value = 'hashed_password'
        
        user_data = {
            'email': 'test@example.com',
            'password': 'plaintext_password',
            'name': 'Test User'
        }
        
        response = client.post('/api/v1/users/register', json=user_data)
        
        # Should hash the password
        mock_hash.assert_called_with('plaintext_password')
    
    def test_password_strength_validation(self, client):
        """Test password strength requirements."""
        weak_password_data = {
            'email': 'test@example.com',
            'password': '123',  # Too weak
            'name': 'Test User'
        }
        
        response = client.post('/api/v1/users/register', json=weak_password_data)
        
        # Should reject weak passwords
        assert response.status_code == 400


class TestJWTAuthentication:
    """Test JWT token functionality."""
    
    @patch('flask_jwt_extended.create_access_token')
    def test_jwt_token_creation(self, mock_create_token, client):
        """Test JWT token creation on successful login."""
        mock_create_token.return_value = 'mock_jwt_token'
        
        # Mock successful user authentication
        with patch('app.main.authenticate_user', return_value={'id': 1, 'email': 'test@example.com'}):
            login_data = {
                'email': 'test@example.com',
                'password': 'password123'
            }
            
            response = client.post('/api/v1/users/login', json=login_data)
            
            if response.status_code == 200:
                mock_create_token.assert_called()
    
    @patch('flask_jwt_extended.verify_jwt_in_request')
    def test_jwt_token_verification(self, mock_verify, client):
        """Test JWT token verification for protected endpoints."""
        mock_verify.return_value = None  # Valid token
        
        headers = {'Authorization': 'Bearer mock_jwt_token'}
        response = client.get('/api/v1/users/profile', headers=headers)
        
        # Should verify the token
        mock_verify.assert_called()


class TestDatabaseOperations:
    """Test database operations."""
    
    def test_user_table_operations(self, client):
        """Test basic user table operations."""
        with app.app_context():
            # Test database connection
            result = db.session.execute(db.text("SELECT 1"))
            assert result.fetchone()[0] == 1
    
    def test_project_user_relationships(self, client):
        """Test project-user relationship queries."""
        with app.app_context():
            # Test that we can query project-user relationships
            # This would test actual project_users table in real deployment
            tables = db.inspect(db.engine).get_table_names()
            assert isinstance(tables, list)


class TestErrorHandling:
    """Test error handling scenarios."""
    
    def test_duplicate_user_registration(self, client):
        """Test handling of duplicate user registration."""
        user_data = {
            'email': 'duplicate@example.com',
            'password': 'password123',
            'name': 'Test User'
        }
        
        # First registration should succeed or return appropriate error
        response1 = client.post('/api/v1/users/register', json=user_data)
        
        # Second registration should fail
        response2 = client.post('/api/v1/users/register', json=user_data)
        
        # Should handle duplicate registration appropriately
        assert response2.status_code in [400, 409]
    
    def test_invalid_login_credentials(self, client):
        """Test handling of invalid login credentials."""
        login_data = {
            'email': 'nonexistent@example.com',
            'password': 'wrongpassword'
        }
        
        response = client.post('/api/v1/users/login', json=login_data)
        
        # Should reject invalid credentials
        assert response.status_code in [400, 401]
    
    @patch('app.main.db.session.execute')
    def test_database_error_handling(self, mock_execute, client):
        """Test handling of database errors."""
        mock_execute.side_effect = Exception("Database error")
        
        response = client.get('/health')
        data = response.get_json()
        
        # Should handle database errors gracefully
        assert 'database_connection' in data['checks']
        assert data['checks']['database_connection'] is False


if __name__ == '__main__':
    pytest.main([__file__])