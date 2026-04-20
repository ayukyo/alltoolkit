"""Data Validator - Pure Python data validation toolkit."""

from .mod import (
    Field,
    Schema,
    ValidationError,
    ValidationResult,
    Validators,
    validate,
    validate_field,
    is_valid_email,
    is_valid_url,
    is_valid_phone,
    is_valid_uuid,
    is_valid_ipv4,
)

__version__ = "1.0.0"
__all__ = [
    "Field",
    "Schema",
    "ValidationError",
    "ValidationResult",
    "Validators",
    "validate",
    "validate_field",
    "is_valid_email",
    "is_valid_url",
    "is_valid_phone",
    "is_valid_uuid",
    "is_valid_ipv4",
]