class GradebookError(Exception):
    """Base error for gradebook operations."""


class ValidationError(GradebookError):
    """Raised when input validation fails."""


class NotFoundError(GradebookError):
    """Raised when a requested item is not found."""


class ConflictError(GradebookError):
    """Raised when an operation conflicts with existing data."""