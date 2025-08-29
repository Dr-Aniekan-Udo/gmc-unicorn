# Implementation Standards & Practices

## Development Standards Framework

### Coding Standards

**Python Services (Flask Microservices)**
```python
# PEP 8 compliance with Black formatting
# Type annotations required for all functions
# Maximum line length: 88 characters

from typing import Dict, List, Optional, Union
import logging

logger = logging.getLogger(__name__)

class GMCCalculationService:
    """Handles GMC mathematical calculations with Excel equivalency."""
    
    def calculate_investment_performance(
        self, 
        project_id: str,
        parameters: Dict[str, Union[int, float]],
        user_id: str
    ) -> Dict[str, float]:
        """Calculate investment performance for project context.
        
        Args:
            project_id: UUID of the project for data isolation
            parameters: Decision parameters from user input
            user_id: User ID for audit trail
            
        Returns:
            Dict containing performance metrics and calculations
            
        Raises:
            ValidationError: If parameters violate GMC constraints
        """
        logger.info(f"Calculating performance for project {project_id}")
        # Implementation follows Excel formula equivalency
```

**React Frontend (TypeScript)**
```typescript
// ESLint + Prettier configuration
// Strict TypeScript mode enabled
// Component prop types required

interface ProjectContextProps {
  projectId: string;
  onProjectChange: (projectId: string) => void;
  userPermissions: UserPermissions;
}

export const ProjectContextSwitcher: React.FC<ProjectContextProps> = ({
  projectId,
  onProjectChange,
  userPermissions
}) => {
  // Component implementation with accessibility
  // WCAG 2.1 AA compliance patterns
  // Team Unicorn design system integration
  
  return (
    <div role="navigation" aria-label="Project Context">
      {/* Implementation */}
    </div>
  );
};
```

### Git Workflow Standards

**Branch Strategy**
```bash
# Main branches
main/                    # Production-ready code
develop/                 # Integration branch for features
release/v*              # Release preparation branches

# Feature branches
feature/epic-1-foundation       # Epic-based feature development
feature/epic-6a-ai-coaching    # AI service implementation
hotfix/calculation-accuracy    # Critical production fixes

# Conventional Commits
feat(calculation): add investment performance optimization
fix(api): resolve project isolation validation error
docs(architecture): add system architecture diagrams
test(frontend): add accessibility testing integration
```

**Code Review Requirements**
- All changes require pull request approval
- Minimum 2 reviewers for architecture changes
- Automated CI/CD pipeline validation required
- Test coverage minimum 90% for calculation engines
- Accessibility testing validation for frontend changes

## API Documentation Standards

**OpenAPI 3.0 Specifications**
```yaml
# Every microservice provides OpenAPI spec
# Deployed with Swagger UI for interactive testing
# Project context validation documented for all endpoints

paths:
  /projects/{projectId}/calculations:
    post:
      summary: "Execute GMC calculations for project"
      parameters:
        - name: projectId
          in: path
          required: true
          schema:
            type: string
            format: uuid
          description: "Project UUID for data isolation"
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/GMCParameters'
      responses:
        '200':
          description: "Calculation results with investment performance"
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/CalculationResults'
        '403':
          description: "Project access denied or isolation violation"
```

**Documentation Generation**
- Automated API documentation generation from code annotations
- Interactive testing environments with Swagger UI deployment
- Version-specific documentation with migration guides
- Cross-service API dependency mapping

## Quality Assurance Standards

**Testing Requirements**
```python
# Unit Testing (pytest)
# Minimum 90% coverage for calculation engines
# 100% mathematical equivalency with Excel validation

def test_investment_performance_calculation():
    """Validate investment performance against Excel reference."""
    # Test data from overview/gmc_history_sample/
    parameters = load_test_parameters("Y16Q4_sample.xlsx")
    expected = load_excel_results("Y16Q4_expected.xlsx")
    
    result = calculate_investment_performance(parameters)
    
    assert_excel_equivalency(result, expected, tolerance=0.001)
    assert result['performance_score'] > 0
    assert 'competitive_ranking' in result

# Integration Testing
def test_project_isolation():
    """Verify complete project data isolation."""
    project_1_data = create_test_project("uuid-1111")
    project_2_data = create_test_project("uuid-2222")
    
    # Verify no cross-contamination
    assert_no_data_leakage(project_1_data, project_2_data)
```

**Performance Validation**
- Sub-500ms response time validation for basic calculations
- Load testing for 50+ concurrent users per simulation group
- AI service response time monitoring (3-10 second targets)
- Memory usage validation (<200MB peak during analysis)
