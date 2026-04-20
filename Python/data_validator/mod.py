"""
Data Validator - Pure Python data validation toolkit with zero external dependencies.

Features:
- Type validation (str, int, float, bool, list, dict, etc.)
- Schema-based validation
- Custom validators with error messages
- Nested data structure validation
- Optional fields and default values
- Validation rules (min/max, length, regex, choices)
"""

from typing import Any, Callable, Dict, List, Optional, Tuple, Union
from dataclasses import dataclass, field
import re
from datetime import datetime


@dataclass
class ValidationError:
    """Represents a single validation error."""
    field: str
    message: str
    value: Any = None
    rule: str = ""

    def __str__(self) -> str:
        return f"[{self.field}] {self.message}"
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "field": self.field,
            "message": self.message,
            "value": repr(self.value),
            "rule": self.rule
        }


@dataclass
class ValidationResult:
    """Result of validation with errors and data."""
    is_valid: bool
    errors: List[ValidationError] = field(default_factory=list)
    data: Dict[str, Any] = field(default_factory=dict)
    
    def add_error(self, field: str, message: str, value: Any = None, rule: str = ""):
        self.errors.append(ValidationError(field, message, value, rule))
        self.is_valid = False
    
    def merge(self, prefix: str, other: "ValidationResult"):
        """Merge another result with prefixed field names."""
        for error in other.errors:
            self.errors.append(ValidationError(
                field=f"{prefix}.{error.field}" if error.field else prefix,
                message=error.message,
                value=error.value,
                rule=error.rule
            ))
        if not other.is_valid:
            self.is_valid = False
    
    def error_messages(self) -> List[str]:
        return [str(e) for e in self.errors]
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "is_valid": self.is_valid,
            "errors": [e.to_dict() for e in self.errors],
            "data": self.data
        }


class Field:
    """Defines validation rules for a single field."""
    
    def __init__(
        self,
        field_type: type = None,
        required: bool = True,
        default: Any = None,
        min_value: Union[int, float] = None,
        max_value: Union[int, float] = None,
        min_length: int = None,
        max_length: int = None,
        pattern: str = None,
        choices: List[Any] = None,
        custom_validator: Callable[[Any], Tuple[bool, str]] = None,
        nested_schema: "Schema" = None,
        item_type: type = None,  # For list items
    ):
        self.field_type = field_type
        self.required = required
        self.default = default
        self.min_value = min_value
        self.max_value = max_value
        self.min_length = min_length
        self.max_length = max_length
        self.pattern = re.compile(pattern) if pattern else None
        self.choices = choices
        self.custom_validator = custom_validator
        self.nested_schema = nested_schema
        self.item_type = item_type
    
    def validate(self, value: Any, field_name: str) -> ValidationResult:
        """Validate a value against this field's rules."""
        result = ValidationResult(is_valid=True)
        
        # Check required
        if value is None:
            if self.required:
                result.add_error(field_name, "Field is required", value, "required")
            return result
        
        # Type check
        if self.field_type and not isinstance(value, self.field_type):
            # Allow int when expecting float
            if not (self.field_type == float and isinstance(value, int)):
                result.add_error(
                    field_name, 
                    f"Expected type {self.field_type.__name__}, got {type(value).__name__}",
                    value, "type"
                )
                return result
        
        # Numeric range checks
        if isinstance(value, (int, float)):
            if self.min_value is not None and value < self.min_value:
                result.add_error(field_name, f"Value must be >= {self.min_value}", value, "min_value")
            if self.max_value is not None and value > self.max_value:
                result.add_error(field_name, f"Value must be <= {self.max_value}", value, "max_value")
        
        # String/collection length checks
        if hasattr(value, "__len__"):
            length = len(value)
            if self.min_length is not None and length < self.min_length:
                result.add_error(field_name, f"Length must be >= {self.min_length}", value, "min_length")
            if self.max_length is not None and length > self.max_length:
                result.add_error(field_name, f"Length must be <= {self.max_length}", value, "max_length")
        
        # Regex pattern check
        if self.pattern and isinstance(value, str):
            if not self.pattern.match(value):
                result.add_error(field_name, f"Value does not match pattern {self.pattern.pattern}", value, "pattern")
        
        # Choices check
        if self.choices is not None:
            if value not in self.choices:
                result.add_error(field_name, f"Value must be one of {self.choices}", value, "choices")
        
        # Custom validator
        if self.custom_validator:
            try:
                is_valid, message = self.custom_validator(value)
                if not is_valid:
                    result.add_error(field_name, message, value, "custom")
            except Exception as e:
                result.add_error(field_name, f"Custom validator error: {str(e)}", value, "custom")
        
        # Nested schema for dict
        if self.nested_schema and isinstance(value, dict):
            nested_result = self.nested_schema.validate(value)
            result.merge(field_name, nested_result)
        
        # List item type validation
        if self.item_type and isinstance(value, list):
            for i, item in enumerate(value):
                if not isinstance(item, self.item_type):
                    result.add_error(
                        f"{field_name}[{i}]", 
                        f"Expected item type {self.item_type.__name__}, got {type(item).__name__}",
                        item, "item_type"
                    )
        
        return result


class Schema:
    """Schema definition for data validation."""
    
    def __init__(self, fields: Dict[str, Field] = None):
        self.fields = fields or {}
    
    def add_field(self, name: str, field: Field) -> "Schema":
        """Add a field to the schema."""
        self.fields[name] = field
        return self
    
    def validate(self, data: Dict[str, Any]) -> ValidationResult:
        """Validate data against the schema."""
        result = ValidationResult(is_valid=True)
        
        for name, field_def in self.fields.items():
            value = data.get(name)
            field_result = field_def.validate(value, name)
            result.merge("", field_result)
            
            # Set default for missing optional fields
            if value is None and field_def.default is not None and not field_def.required:
                result.data[name] = field_def.default
            elif value is not None:
                result.data[name] = value
        
        return result
    
    def validate_partial(self, data: Dict[str, Any]) -> ValidationResult:
        """Validate only provided fields (required fields become optional)."""
        result = ValidationResult(is_valid=True)
        
        for name, field_def in self.fields.items():
            if name in data:
                value = data[name]
                field_result = field_def.validate(value, name)
                result.merge("", field_result)
                if field_result.is_valid:
                    result.data[name] = value
        
        return result


# Pre-built validators
class Validators:
    """Collection of reusable validator functions."""
    
    @staticmethod
    def email(value: str) -> Tuple[bool, str]:
        """Validate email format."""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if re.match(pattern, value):
            return True, ""
        return False, "Invalid email format"
    
    @staticmethod
    def url(value: str) -> Tuple[bool, str]:
        """Validate URL format."""
        pattern = r'^https?://[^\s/$.?#].[^\s]*$'
        if re.match(pattern, value, re.IGNORECASE):
            return True, ""
        return False, "Invalid URL format"
    
    @staticmethod
    def phone(value: str) -> Tuple[bool, str]:
        """Validate phone number (supports various formats)."""
        # Remove common separators
        cleaned = re.sub(r'[\s\-\(\)\+]', '', value)
        if cleaned.isdigit() and 7 <= len(cleaned) <= 15:
            return True, ""
        return False, "Invalid phone number format"
    
    @staticmethod
    def date_iso(value: str) -> Tuple[bool, str]:
        """Validate ISO date format (YYYY-MM-DD)."""
        try:
            datetime.strptime(value, "%Y-%m-%d")
            return True, ""
        except ValueError:
            return False, "Invalid ISO date format (expected YYYY-MM-DD)"
    
    @staticmethod
    def datetime_iso(value: str) -> Tuple[bool, str]:
        """Validate ISO datetime format."""
        patterns = [
            "%Y-%m-%dT%H:%M:%S",
            "%Y-%m-%dT%H:%M:%SZ",
            "%Y-%m-%dT%H:%M:%S%z",
            "%Y-%m-%d %H:%M:%S",
        ]
        for pattern in patterns:
            try:
                datetime.strptime(value.replace("+00:00", "+0000"), pattern)
                return True, ""
            except ValueError:
                continue
        return False, "Invalid ISO datetime format"
    
    @staticmethod
    def uuid(value: str) -> Tuple[bool, str]:
        """Validate UUID format."""
        pattern = r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
        if re.match(pattern, value, re.IGNORECASE):
            return True, ""
        return False, "Invalid UUID format"
    
    @staticmethod
    def hex_color(value: str) -> Tuple[bool, str]:
        """Validate hex color code."""
        pattern = r'^#([0-9a-fA-F]{3}|[0-9a-fA-F]{6})$'
        if re.match(pattern, value):
            return True, ""
        return False, "Invalid hex color format"
    
    @staticmethod
    def ipv4(value: str) -> Tuple[bool, str]:
        """Validate IPv4 address."""
        parts = value.split('.')
        if len(parts) != 4:
            return False, "Invalid IPv4 address"
        try:
            for part in parts:
                num = int(part)
                if not 0 <= num <= 255:
                    return False, "IPv4 octet must be 0-255"
            return True, ""
        except ValueError:
            return False, "Invalid IPv4 address"
    
    @staticmethod
    def port(value: int) -> Tuple[bool, str]:
        """Validate port number."""
        if 0 <= value <= 65535:
            return True, ""
        return False, "Port must be between 0 and 65535"
    
    @staticmethod
    def age(value: int) -> Tuple[bool, str]:
        """Validate age (reasonable range)."""
        if 0 <= value <= 150:
            return True, ""
        return False, "Age must be between 0 and 150"
    
    @staticmethod
    def password_strength(min_length: int = 8, require_upper: bool = True, 
                          require_lower: bool = True, require_digit: bool = True,
                          require_special: bool = False) -> Callable[[str], Tuple[bool, str]]:
        """Create a password strength validator."""
        def validator(value: str) -> Tuple[bool, str]:
            if len(value) < min_length:
                return False, f"Password must be at least {min_length} characters"
            if require_upper and not any(c.isupper() for c in value):
                return False, "Password must contain uppercase letter"
            if require_lower and not any(c.islower() for c in value):
                return False, "Password must contain lowercase letter"
            if require_digit and not any(c.isdigit() for c in value):
                return False, "Password must contain a digit"
            if require_special and not any(c in "!@#$%^&*()_+-=[]{}|;:',.<>?/" for c in value):
                return False, "Password must contain special character"
            return True, ""
        return validator
    
    @staticmethod
    def in_range(min_val: Union[int, float], max_val: Union[int, float]) -> Callable[[Union[int, float]], Tuple[bool, str]]:
        """Create a range validator."""
        def validator(value: Union[int, float]) -> Tuple[bool, str]:
            if min_val <= value <= max_val:
                return True, ""
            return False, f"Value must be between {min_val} and {max_val}"
        return validator
    
    @staticmethod
    def length(min_len: int = None, max_len: int = None) -> Callable[[str], Tuple[bool, str]]:
        """Create a length validator for strings/collections."""
        def validator(value: str) -> Tuple[bool, str]:
            length = len(value)
            if min_len is not None and length < min_len:
                return False, f"Length must be at least {min_len}"
            if max_len is not None and length > max_len:
                return False, f"Length must be at most {max_len}"
            return True, ""
        return validator


# Convenience functions
def validate(data: Dict[str, Any], schema: Schema) -> ValidationResult:
    """Validate data against a schema."""
    return schema.validate(data)


def validate_field(value: Any, field: Field, name: str = "field") -> ValidationResult:
    """Validate a single value against a field definition."""
    return field.validate(value, name)


# Quick validation helpers
def is_valid_email(value: str) -> bool:
    return Validators.email(value)[0]

def is_valid_url(value: str) -> bool:
    return Validators.url(value)[0]

def is_valid_phone(value: str) -> bool:
    return Validators.phone(value)[0]

def is_valid_uuid(value: str) -> bool:
    return Validators.uuid(value)[0]

def is_valid_ipv4(value: str) -> bool:
    return Validators.ipv4(value)[0]