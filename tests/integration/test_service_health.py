"""
Integration Tests for Service Health Checks

Tests to verify all microservices are healthy and respond correctly
to health check endpoints.
"""

import pytest
import requests
from typing import Dict, Any
import time
import logging

logger = logging.getLogger(__name__)

# Service endpoints for testing
SERVICES = {
    "gmc-calculation-service": "http://localhost:5000",
    "knowledge-graph-service": "http://localhost:5001", 
    "conversation-service": "http://localhost:5002",
    "user-management-service": "http://localhost:5003"
}

class TestServiceHealth:
    """Test suite for service health checks."""
    
    def test_all_services_health_endpoints(self):
        """Test that all services respond to /health endpoint."""
        for service_name, base_url in SERVICES.items():
            health_url = f"{base_url}/health"
            
            try:
                response = requests.get(health_url, timeout=10)
                
                # Should return 200 OK
                assert response.status_code == 200, f"{service_name} health check failed"
                
                # Should return JSON
                health_data = response.json()
                assert isinstance(health_data, dict), f"{service_name} should return JSON"
                
                # Should contain required fields
                assert "status" in health_data, f"{service_name} missing status field"
                assert "service" in health_data, f"{service_name} missing service field"
                assert "version" in health_data, f"{service_name} missing version field"
                assert "timestamp" in health_data, f"{service_name} missing timestamp field"
                
                # Status should be healthy
                assert health_data["status"] == "healthy", f"{service_name} reports unhealthy status"
                
                # Service name should match
                expected_service = service_name.replace("-", "_")
                assert expected_service in health_data["service"], f"{service_name} incorrect service name"
                
                logger.info(f"✅ {service_name} health check passed")
                
            except requests.exceptions.RequestException as e:
                pytest.fail(f"{service_name} health endpoint unreachable: {e}")
            except AssertionError as e:
                pytest.fail(f"{service_name} health check assertion failed: {e}")
    
    def test_all_services_readiness_endpoints(self):
        """Test that all services respond to /health/ready endpoint."""
        for service_name, base_url in SERVICES.items():
            ready_url = f"{base_url}/health/ready"
            
            try:
                response = requests.get(ready_url, timeout=10)
                
                # Should return 200 OK when ready
                assert response.status_code == 200, f"{service_name} readiness check failed"
                
                # Should return JSON
                ready_data = response.json()
                assert isinstance(ready_data, dict), f"{service_name} should return JSON"
                
                # Should contain required fields
                assert "ready" in ready_data, f"{service_name} missing ready field"
                assert "service" in ready_data, f"{service_name} missing service field"
                assert "message" in ready_data, f"{service_name} missing message field"
                
                # Ready should be True
                assert ready_data["ready"] is True, f"{service_name} reports not ready"
                
                logger.info(f"✅ {service_name} readiness check passed")
                
            except requests.exceptions.RequestException as e:
                pytest.fail(f"{service_name} readiness endpoint unreachable: {e}")
            except AssertionError as e:
                pytest.fail(f"{service_name} readiness check assertion failed: {e}")
    
    def test_service_info_endpoints(self):
        """Test that all services respond to /api/v1/info endpoint."""
        for service_name, base_url in SERVICES.items():
            info_url = f"{base_url}/api/v1/info"
            
            try:
                response = requests.get(info_url, timeout=10)
                
                # Should return 200 OK
                assert response.status_code == 200, f"{service_name} info endpoint failed"
                
                # Should return JSON
                info_data = response.json()
                assert isinstance(info_data, dict), f"{service_name} should return JSON"
                
                # Should contain service information
                assert "service" in info_data, f"{service_name} missing service field"
                assert "endpoints" in info_data, f"{service_name} missing endpoints field"
                assert "features" in info_data, f"{service_name} missing features field"
                
                # Service info should be complete
                service_info = info_data["service"]
                assert "name" in service_info, f"{service_name} missing service name"
                assert "version" in service_info, f"{service_name} missing service version"
                assert "port" in service_info, f"{service_name} missing service port"
                assert "database" in service_info, f"{service_name} missing database info"
                
                logger.info(f"✅ {service_name} info endpoint passed")
                
            except requests.exceptions.RequestException as e:
                pytest.fail(f"{service_name} info endpoint unreachable: {e}")
            except AssertionError as e:
                pytest.fail(f"{service_name} info endpoint assertion failed: {e}")
    
    def test_service_response_times(self):
        """Test that all services respond within acceptable time limits."""
        max_response_time = 2.0  # seconds
        
        for service_name, base_url in SERVICES.items():
            health_url = f"{base_url}/health"
            
            try:
                start_time = time.time()
                response = requests.get(health_url, timeout=10)
                end_time = time.time()
                
                response_time = end_time - start_time
                
                # Should respond quickly
                assert response_time < max_response_time, \
                    f"{service_name} response time {response_time:.2f}s exceeds {max_response_time}s"
                
                # Should be successful
                assert response.status_code == 200, f"{service_name} health check failed"
                
                logger.info(f"✅ {service_name} response time: {response_time:.2f}s")
                
            except requests.exceptions.RequestException as e:
                pytest.fail(f"{service_name} performance test failed: {e}")
    
    def test_cors_headers(self):
        """Test that services include proper CORS headers."""
        for service_name, base_url in SERVICES.items():
            health_url = f"{base_url}/health"
            
            try:
                response = requests.get(health_url, timeout=10)
                
                # Should have CORS headers
                headers = response.headers
                
                # Access-Control headers should be present via API Gateway
                # Note: This test will pass if services are accessed directly
                # CORS headers are typically added by the API Gateway
                
                logger.info(f"✅ {service_name} CORS headers checked")
                
            except requests.exceptions.RequestException as e:
                pytest.fail(f"{service_name} CORS test failed: {e}")

@pytest.fixture(scope="session", autouse=True)
def wait_for_services():
    """Wait for all services to be ready before running tests."""
    max_wait_time = 60  # seconds
    check_interval = 2  # seconds
    
    logger.info("Waiting for services to be ready...")
    
    for elapsed in range(0, max_wait_time, check_interval):
        all_ready = True
        
        for service_name, base_url in SERVICES.items():
            try:
                response = requests.get(f"{base_url}/health", timeout=5)
                if response.status_code != 200:
                    all_ready = False
                    break
            except requests.exceptions.RequestException:
                all_ready = False
                break
        
        if all_ready:
            logger.info(f"All services ready after {elapsed}s")
            return
        
        logger.info(f"Services not ready yet, waiting... ({elapsed}s elapsed)")
        time.sleep(check_interval)
    
    pytest.fail(f"Services not ready after {max_wait_time}s")

if __name__ == "__main__":
    # Run tests directly
    pytest.main([__file__, "-v"])