from typing import Optional, Dict, Any


class APIException(Exception):
    """Base API Exception"""
    
    def __init__(
        self,
        status_code: int = 500,
        error_code: str = "INTERNAL_ERROR",
        message: str = "An error occurred",
        details: Optional[Dict[str, Any]] = None
    ):
        self.status_code = status_code
        self.error_code = error_code
        self.message = message
        self.details = details
        super().__init__(self.message)


class NotFoundError(APIException):
    """Resource not found"""
    
    def __init__(self, resource: str, resource_id: str):
        super().__init__(
            status_code=404,
            error_code="NOT_FOUND",
            message=f"{resource} not found",
            details={"resource": resource, "id": resource_id}
        )


class ValidationError(APIException):
    """Validation error"""
    
    def __init__(self, message: str, details: Optional[Dict] = None):
        super().__init__(
            status_code=400,
            error_code="VALIDATION_ERROR",
            message=message,
            details=details
        )


class RateLimitError(APIException):
    """Rate limit exceeded"""
    
    def __init__(self, retry_after: int = 60):
        super().__init__(
            status_code=429,
            error_code="RATE_LIMIT_EXCEEDED",
            message="Too many requests",
            details={"retry_after": retry_after}
        )


class ExternalAPIError(APIException):
    """External API error"""
    
    def __init__(self, service: str, message: str):
        super().__init__(
            status_code=502,
            error_code="EXTERNAL_API_ERROR",
            message=f"Error from {service}: {message}",
            details={"service": service}
        )
