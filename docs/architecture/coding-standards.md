# Coding Standards

Define **MINIMAL but CRITICAL** standards focused on academic compliance, educational transparency, and GMC accuracy. These standards prioritize automated enforcement over manual compliance to reduce burden on academic development teams.

## Essential Academic Compliance Standards (Automated Enforcement)

- **Student Data Protection:** All operations affecting student data must include institutional boundary validation and FERPA audit logging *(automated through middleware)*
- **Educational Transparency:** GMC business logic must include educational comments explaining optimization strategies and constraint reasoning *(enforced through templates)*
- **Academic Integrity Tracking:** Parameter changes, collaboration events, and calculation results must be auditable with team member attribution *(automated through service layers)*
- **Cross-Stack Type Safety:** Shared data structures between frontend/backend must use generated types from single source of truth *(automated through build pipeline)*
- **Constraint Validation Consistency:** All GMC constraint checks must provide educational explanations and optimization guidance *(enforced through validation framework)*

## JavaScript/TypeScript Standards

### Component Standards
```typescript
// Component structure: Props interface, main component, export
interface UserProfileProps {
  readonly userId: string;
  readonly academicContext: AcademicContext;
  readonly onProfileUpdate?: (profile: UserProfile) => void;
}

export const UserProfile: React.FC<UserProfileProps> = ({
  userId,
  academicContext,
  onProfileUpdate
}) => {
  // Hooks first
  const { data: profile, error } = useUserProfile(userId);
  const [isEditing, setIsEditing] = useState(false);
  
  // Early returns for loading/error states
  if (error) return <ErrorBoundary error={error} />;
  if (!profile) return <LoadingSpinner />;
  
  // Event handlers with academic audit integration
  const handleSave = useCallback(async (updatedProfile: UserProfile) => {
    await updateProfile(updatedProfile);
    onProfileUpdate?.(updatedProfile);
    setIsEditing(false);
  }, [onProfileUpdate]);
  
  return (
    <div className="user-profile">
      {/* Component JSX */}
    </div>
  );
};
```

### API Integration Standards
```typescript
// Use centralized API client with proper error handling
import { gmcApi } from '@/shared/api/gmcClient';
import { handleApiError } from '@/shared/utils/errorHandling';

export const useAnalysisSession = (sessionId: string) => {
  return useSWR(
    `sessions/${sessionId}`,
    () => gmcApi.sessions.getSession(sessionId),
    {
      onError: handleApiError,
      revalidateOnFocus: false, // Academic context - don't over-refresh
    }
  );
};
```

## Python Standards

### Service Class Standards
```python
from typing import Dict, List, Optional, Union
import asyncio
from flask import Blueprint, request, jsonify
from pydantic import BaseModel, validator

from app.core.config import settings
from app.models.academic import Company, AnalysisSession
from app.services.calculation import GMCCalculationEngine
from app.utils.academic_audit import log_academic_event

class GMCCalculationService:
    """
    GMC calculation service with Excel compatibility and academic audit trails.
    
    Provides mathematical processing equivalent to GMC Excel analysis
    with educational transparency and performance optimization.
    """
    
    def __init__(
        self, 
        excel_parser: ExcelParsingService,
        audit_logger: AcademicAuditLogger,
        cache_service: CacheService
    ) -> None:
        self.excel_parser = excel_parser
        self.audit_logger = audit_logger
        self.cache_service = cache_service
        
    async def calculate_investment_performance(
        self, 
        session_id: str, 
        parameters: DecisionParameters,
        academic_context: AcademicContext
    ) -> InvestmentPerformanceResult:
        """
        Calculate GMC investment performance with educational transparency.
        
        Args:
            session_id: Analysis session identifier
            parameters: Decision parameters for calculation
            academic_context: Educational context for audit and learning analytics
            
        Returns:
            Investment performance results with formula audit trail
            
        Raises:
            CalculationError: When mathematical processing fails
            ValidationError: When parameters violate GMC constraints
        """
        # Academic audit logging
        await self.audit_logger.log_calculation_start(
            session_id, academic_context.student_id, "investment_performance"
        )
        
        try:
            # Check calculation cache for performance
            cache_key = self._generate_cache_key(parameters)
            cached_result = await self.cache_service.get(cache_key)
            
            if cached_result:
                await self.audit_logger.log_cache_hit(session_id, cache_key)
                return cached_result
            
            # Perform calculation with formula transparency
            result = await self._perform_investment_calculation(parameters)
            
            # Cache result for future use
            await self.cache_service.set(cache_key, result, ttl=3600)
            
            # Academic audit completion
            await self.audit_logger.log_calculation_complete(
                session_id, result.performance_metrics, result.audit_trail
            )
            
            return result
            
        except Exception as e:
            await self.audit_logger.log_calculation_error(session_id, str(e))
            raise CalculationError(
                f"Investment performance calculation failed: {e}",
                educational_guidance="Review parameter constraints and try again"
            )
```

## Academic-Specific Naming Conventions

| Element | Frontend (TypeScript) | Backend (Python) | Academic Context | Example |
|---------|----------------------|------------------|---------|---------|
| **Student Components** | `Student*` prefix | N/A | Always require academic context | `StudentDashboard.tsx` |
| **GMC Business Logic** | `GMC*` or `*Analysis` | `gmc_*` or `*_analysis` | Educational comments required | `GMCParameterInput.tsx`, `gmc_calculation_service.py` |
| **Academic Services** | `*Academic*` | `academic_*` | FERPA compliance required | `AcademicAuditLogger.ts`, `academic_auth_service.py` |
| **Collaboration Features** | `Collab*` or `Team*` | `collab_*` or `team_*` | Attribution tracking required | `CollabWorkspace.tsx`, `team_session_manager.py` |
| **Database Tables** | N/A | `snake_case` | Institution isolation required | `student_analysis_sessions`, `academic_audit_events` |

## Error Handling Patterns

```typescript
// Frontend academic error handling
export const handleAcademicError = (
  error: ApiError, 
  context: AcademicContext
): AcademicErrorResult => {
  return {
    studentMessage: generateStudentFriendlyMessage(error),
    educationalGuidance: {
      concept: getGMCConcept(error.code),
      explanation: getOptimizationExplanation(error),
      nextSteps: getSuggestedActions(error, context),
      resources: getEducationalResources(error.code)
    },
    facultyAlert: requiresFacultyNotification(error, context),
    recoveryOptions: generateRecoveryOptions(error, context)
  };
};
```

```python
# Backend academic exception handling
class GMCValidationError(HTTPException):
    """Academic-focused validation error with educational context."""
    
    def __init__(
        self, 
        message: str, 
        educational_guidance: str,
        student_message: Optional[str] = None,
        faculty_context: Optional[str] = None
    ):
        super().__init__(
            status_code=400, 
            detail={
                "error_type": "gmc_validation_error",
                "message": message,
                "student_message": student_message or message,
                "educational_guidance": educational_guidance,
                "faculty_context": faculty_context,
                "timestamp": datetime.utcnow().isoformat()
            }
        )
```

## Academic Compliance Automation Strategy

**Tier 1 - Essential Automation (All Teams):**
- Academic context injection through templates
- FERPA compliance through middleware  
- Educational error formatting through decorators
- Audit logging through service layer integration

**Tier 2 - Advanced Automation (Experienced Teams):**
- AI agent code generation with academic templates
- Automated GMC formula validation against Excel references
- Learning analytics integration through instrumentation
- Faculty dashboard data collection through event streams

**Tier 3 - Enterprise Academic (Large Institutions):**
- Custom academic compliance rule engines
- Institution-specific integration patterns
- Advanced learning analytics and intervention systems
- Multi-language academic development frameworks
