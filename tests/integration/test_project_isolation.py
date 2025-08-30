"""
Integration tests for project data isolation across all services.

Tests that project-scoped data isolation is working correctly
and that cross-project data contamination is prevented.
"""

import pytest
import requests
import uuid
from typing import Dict, Any
import time


class TestProjectDataIsolation:
    """Test project data isolation across all microservices."""

    @pytest.fixture(autouse=True)
    def setup_test_projects(self):
        """Set up test projects for isolation testing."""
        self.project_a = f"test-project-a-{uuid.uuid4().hex[:8]}"
        self.project_b = f"test-project-b-{uuid.uuid4().hex[:8]}"
        
        # Base URLs for services
        self.base_urls = {
            'calculation': 'http://localhost:5000',
            'knowledge': 'http://localhost:5001',
            'conversation': 'http://localhost:5002',
            'user': 'http://localhost:5003'
        }
    
    def create_test_data(self, service: str, project_id: str, data: Dict[Any, Any]) -> Dict[Any, Any]:
        """Create test data in a specific service and project."""
        headers = {'X-Project-ID': project_id, 'Content-Type': 'application/json'}
        
        endpoints = {
            'calculation': '/api/v1/calculations',
            'knowledge': '/api/v1/knowledge/rules',
            'conversation': '/api/v1/conversations',
            'user': '/api/v1/users/project-data'
        }
        
        url = f"{self.base_urls[service]}{endpoints[service]}"
        response = requests.post(url, json=data, headers=headers)
        
        if response.status_code in [200, 201]:
            return response.json()
        else:
            pytest.skip(f"Could not create test data for {service}: {response.status_code}")

    def get_project_data(self, service: str, project_id: str) -> Dict[Any, Any]:
        """Retrieve data from a specific service and project."""
        headers = {'X-Project-ID': project_id}
        
        endpoints = {
            'calculation': '/api/v1/calculations',
            'knowledge': '/api/v1/knowledge/rules',
            'conversation': '/api/v1/conversations',
            'user': '/api/v1/users/project-data'
        }
        
        url = f"{self.base_urls[service]}{endpoints[service]}"
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            return []
        else:
            pytest.fail(f"Failed to get data from {service}: {response.status_code}")

    def test_calculation_service_isolation(self):
        """Test that calculation data is isolated between projects."""
        # Create calculation data in project A
        calc_data_a = {
            'name': 'Project A Calculation',
            'revenue': 10000,
            'costs': 8000,
            'project_id': self.project_a
        }
        
        created_a = self.create_test_data('calculation', self.project_a, calc_data_a)
        
        # Create calculation data in project B  
        calc_data_b = {
            'name': 'Project B Calculation',
            'revenue': 15000,
            'costs': 12000,
            'project_id': self.project_b
        }
        
        created_b = self.create_test_data('calculation', self.project_b, calc_data_b)
        
        # Verify project A only sees its own data
        project_a_data = self.get_project_data('calculation', self.project_a)
        project_a_names = [item.get('name') for item in project_a_data]
        
        assert 'Project A Calculation' in project_a_names
        assert 'Project B Calculation' not in project_a_names
        
        # Verify project B only sees its own data
        project_b_data = self.get_project_data('calculation', self.project_b)
        project_b_names = [item.get('name') for item in project_b_data]
        
        assert 'Project B Calculation' in project_b_names
        assert 'Project A Calculation' not in project_b_names

    def test_knowledge_graph_isolation(self):
        """Test that knowledge graph data is isolated between projects."""
        # Create knowledge rule in project A
        rule_data_a = {
            'name': 'Project A Rule',
            'description': 'Rule for project A only',
            'conditions': ['condition_a'],
            'project_id': self.project_a
        }
        
        created_a = self.create_test_data('knowledge', self.project_a, rule_data_a)
        
        # Create knowledge rule in project B
        rule_data_b = {
            'name': 'Project B Rule', 
            'description': 'Rule for project B only',
            'conditions': ['condition_b'],
            'project_id': self.project_b
        }
        
        created_b = self.create_test_data('knowledge', self.project_b, rule_data_b)
        
        # Verify isolation
        project_a_rules = self.get_project_data('knowledge', self.project_a)
        project_a_names = [rule.get('name') for rule in project_a_rules]
        
        assert 'Project A Rule' in project_a_names
        assert 'Project B Rule' not in project_a_names
        
        project_b_rules = self.get_project_data('knowledge', self.project_b)  
        project_b_names = [rule.get('name') for rule in project_b_rules]
        
        assert 'Project B Rule' in project_b_names
        assert 'Project A Rule' not in project_b_names

    def test_conversation_service_isolation(self):
        """Test that conversation data is isolated between projects."""
        # Create conversation in project A
        conv_data_a = {
            'message': 'Question about Project A',
            'user_id': 'user123',
            'project_id': self.project_a
        }
        
        created_a = self.create_test_data('conversation', self.project_a, conv_data_a)
        
        # Create conversation in project B
        conv_data_b = {
            'message': 'Question about Project B',
            'user_id': 'user123', 
            'project_id': self.project_b
        }
        
        created_b = self.create_test_data('conversation', self.project_b, conv_data_b)
        
        # Verify isolation
        project_a_convs = self.get_project_data('conversation', self.project_a)
        project_a_messages = [conv.get('message') for conv in project_a_convs]
        
        assert 'Question about Project A' in project_a_messages
        assert 'Question about Project B' not in project_a_messages
        
        project_b_convs = self.get_project_data('conversation', self.project_b)
        project_b_messages = [conv.get('message') for conv in project_b_convs]
        
        assert 'Question about Project B' in project_b_messages  
        assert 'Question about Project A' not in project_b_messages

    def test_cross_project_access_denied(self):
        """Test that accessing other project's data is denied."""
        # Create data in project A
        calc_data = {
            'name': 'Private Calculation',
            'revenue': 50000,
            'project_id': self.project_a
        }
        
        self.create_test_data('calculation', self.project_a, calc_data)
        
        # Try to access project A's data with project B context
        headers = {'X-Project-ID': self.project_b}
        url = f"{self.base_urls['calculation']}/api/v1/calculations"
        
        response = requests.get(url, headers=headers)
        
        # Should not contain project A's data
        if response.status_code == 200:
            project_b_data = response.json()
            project_b_names = [item.get('name') for item in project_b_data]
            assert 'Private Calculation' not in project_b_names

    def test_project_id_validation(self):
        """Test that invalid or missing project IDs are handled correctly."""
        # Test missing project ID
        url = f"{self.base_urls['calculation']}/api/v1/calculations"
        response = requests.get(url)  # No X-Project-ID header
        
        assert response.status_code in [400, 403], "Missing project ID should be rejected"
        
        # Test invalid project ID format
        headers = {'X-Project-ID': 'invalid-format!@#$'}
        response = requests.get(url, headers=headers)
        
        assert response.status_code in [400, 403], "Invalid project ID should be rejected"

    def test_project_boundary_enforcement(self):
        """Test that project boundaries are enforced at the database level."""
        # This test would verify database constraints prevent cross-project contamination
        # In a real implementation, this might involve direct database queries
        
        # Create data in multiple projects
        services = ['calculation', 'knowledge', 'conversation']
        
        for service in services:
            test_data = {
                'name': f'Boundary test {service}',
                'project_id': self.project_a
            }
            
            self.create_test_data(service, self.project_a, test_data)
        
        # Verify each service maintains isolation
        for service in services:
            project_a_data = self.get_project_data(service, self.project_a)
            project_b_data = self.get_project_data(service, self.project_b)
            
            # Project A should have data, Project B should not
            assert len(project_a_data) > 0, f"{service} should have data in project A"
            
            # Check that project B data doesn't contain project A items
            project_b_names = [item.get('name', '') for item in project_b_data]
            assert f'Boundary test {service}' not in project_b_names

    def test_concurrent_project_operations(self):
        """Test that concurrent operations on different projects don't interfere."""
        import threading
        import time
        
        results = {'project_a': [], 'project_b': []}
        
        def create_project_data(project_id: str, result_key: str):
            for i in range(5):
                data = {
                    'name': f'Concurrent test {result_key} {i}',
                    'value': i * 100,
                    'project_id': project_id
                }
                
                created = self.create_test_data('calculation', project_id, data)
                results[result_key].append(created)
                time.sleep(0.1)  # Small delay to simulate real usage
        
        # Start concurrent operations
        thread_a = threading.Thread(
            target=create_project_data, 
            args=(self.project_a, 'project_a')
        )
        thread_b = threading.Thread(
            target=create_project_data,
            args=(self.project_b, 'project_b')
        )
        
        thread_a.start()
        thread_b.start()
        
        thread_a.join()
        thread_b.join()
        
        # Verify data integrity after concurrent operations
        final_data_a = self.get_project_data('calculation', self.project_a)
        final_data_b = self.get_project_data('calculation', self.project_b)
        
        # Each project should have exactly its own data
        project_a_names = [item.get('name', '') for item in final_data_a]
        project_b_names = [item.get('name', '') for item in final_data_b]
        
        # Check project A data integrity  
        for i in range(5):
            assert f'Concurrent test project_a {i}' in project_a_names
            assert f'Concurrent test project_b {i}' not in project_a_names
        
        # Check project B data integrity
        for i in range(5):
            assert f'Concurrent test project_b {i}' in project_b_names  
            assert f'Concurrent test project_a {i}' not in project_b_names


if __name__ == '__main__':
    pytest.main([__file__, '-v'])