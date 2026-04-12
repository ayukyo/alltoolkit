"""
AllToolkit - Python Configuration Utilities

A zero-dependency, production-ready configuration management module.
Supports key-value parsing, environment variable substitution, validation,
type coercion, nested configs, and multiple format support.

Author: AllToolkit
License: MIT
"""

import os
import re
import json
from typing import Optional, Any, Dict, List, Tuple, Union, Callable, TypeVar
from dataclasses import dataclass, field
from pathlib import Path
from enum import Enum


T = TypeVar('T')


class ConfigFormat(Enum):
    """Supported configuration formats."""
    KEY_VALUE = "key_value"
    JSON = "json"
    ENV = "env"
    INI = "ini"


class ConfigError(Exception):
    """Base exception for configuration errors."""
    pass


class ConfigValidationError(ConfigError):
    """Raised when configuration validation fails."""
    pass


class ConfigParseError(ConfigError):
    """Raised when configuration parsing fails."""
    pass


class ConfigFileError(ConfigError):
    """Raised when configuration file operations fail."""
    pass


@dataclass
class ConfigValue:
    """Represents a configuration value with metadata."""
    value: Any
    source: str = "default"
    is_env_substituted: bool = False
    
    def __repr__(self) -> str:
        return f"ConfigValue({self.value!r}, source={self.source!r})"


@dataclass
class SchemaField:
    """Defines a schema field for validation."""
    type: type = str
    required: bool = False
    default: Any = None
    min: Optional[Union[int, float]] = None
    max: Optional[Union[int, float]] = None
    choices: Optional[List[Any]] = None
    pattern: Optional[str] = None
    description: str = ""
    
    def validate(self, value: Any, key: str) -> Tuple[bool, Optional[str]]:
        """Validate a value against this field schema."""
        # Type check
        if not isinstance(value, self.type):
            try:
                value = self.type(value)
            except (ValueError, TypeError):
                return False, f"{key}: expected {self.type.__name__}, got {type(value).__name__}"
        
        # Range check
        if self.min is not None and value < self.min:
            return False, f"{key}: value {value} is less than minimum {self.min}"
        if self.max is not None and value > self.max:
            return False, f"{key}: value {value} is greater than maximum {self.max}"
        
        # Choices check
        if self.choices is not None and value not in self.choices:
            return False, f"{key}: value {value!r} not in allowed choices {self.choices}"
        
        # Pattern check (for strings)
        if self.pattern is not None and isinstance(value, str):
            if not re.match(self.pattern, value):
                return False, f"{key}: value '{value}' does not match pattern '{self.pattern}'"
        
        return True, None


@dataclass
class ConfigSchema:
    """Defines a configuration schema for validation."""
    fields: Dict[str, SchemaField] = field(default_factory=dict)
    strict: bool = False  # If True, reject unknown keys
    
    def add_field(self, key: str, **kwargs) -> 'ConfigSchema':
        """Add a field to the schema."""
        self.fields[key] = SchemaField(**kwargs)
        return self
    
    def validate(self, config: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """Validate a configuration against this schema."""
        errors = []
        
        # Check for unknown keys in strict mode
        if self.strict:
            unknown_keys = set(config.keys()) - set(self.fields.keys())
            for key in unknown_keys:
                errors.append(f"Unknown configuration key: {key}")
        
        # Validate each field
        for key, field_schema in self.fields.items():
            if key not in config:
                if field_schema.required:
                    errors.append(f"Missing required configuration: {key}")
                continue
            
            value = config[key]
            is_valid, error = field_schema.validate(value, key)
            if not is_valid:
                errors.append(error)
        
        return len(errors) == 0, errors


class ConfigParser:
    """
    A zero-dependency configuration parser supporting multiple formats.
    
    Features:
    - Key-value format (key=value)
    - JSON format
    - Environment file format (.env)
    - INI format (sections)
    - Environment variable substitution (${VAR} or $VAR)
    - Type coercion
    - Nested configuration support
    """
    
    # Environment variable pattern: ${VAR} or $VAR
    ENV_PATTERN = re.compile(r'\$\{([^}]+)\}|\$([A-Za-z_][A-Za-z0-9_]*)')
    
    def __init__(self, env_prefix: str = ""):
        """
        Initialize the parser.
        
        Args:
            env_prefix: Prefix for environment variable lookups
        """
        self.env_prefix = env_prefix
        self._env_cache: Dict[str, str] = {}
    
    def _get_env(self, var_name: str) -> Optional[str]:
        """Get environment variable with optional prefix and caching."""
        full_name = f"{self.env_prefix}{var_name}" if self.env_prefix else var_name
        
        if full_name not in self._env_cache:
            self._env_cache[full_name] = os.environ.get(full_name, "")
        
        return self._env_cache[full_name] or os.environ.get(var_name, "")
    
    def substitute_env(self, text: str) -> str:
        """
        Substitute environment variables in text.
        
        Supports:
        - ${VAR_NAME} - named variable
        - $VAR_NAME - named variable (no braces)
        - ${VAR_NAME:-default} - with default value
        - ${VAR_NAME:+alternate} - alternate if set
        
        Args:
            text: Text containing environment variable references
            
        Returns:
            Text with environment variables substituted
        """
        def replace(match):
            var_expr = match.group(1) or match.group(2)
            
            # Check for default value syntax ${VAR:-default}
            if ':-' in var_expr:
                var_name, default = var_expr.split(':-', 1)
                value = self._get_env(var_name)
                return value if value else default
            
            # Check for alternate value syntax ${VAR:+alternate}
            if ':+' in var_expr:
                var_name, alternate = var_expr(':+', 1)
                value = self._get_env(var_name)
                return alternate if value else ""
            
            # Simple variable substitution
            return self._get_env(var_expr)
        
        return self.ENV_PATTERN.sub(replace, text)
    
    def parse_key_value(self, content: str) -> Dict[str, str]:
        """
        Parse key-value format content.
        
        Format:
        ```
        key=value
        key2=value with spaces
        # comment
        ```
        
        Args:
            content: Raw content string
            
        Returns:
            Dictionary of key-value pairs
        """
        result = {}
        
        for line_num, line in enumerate(content.splitlines(), 1):
            line = line.strip()
            
            # Skip empty lines and comments
            if not line or line.startswith('#') or line.startswith(';'):
                continue
            
            # Find the first '=' sign
            if '=' not in line:
                raise ConfigParseError(f"Line {line_num}: Missing '=' in key-value pair")
            
            key, _, value = line.partition('=')
            key = key.strip()
            value = value.strip()
            
            # Remove quotes if present
            if (value.startswith('"') and value.endswith('"')) or \
               (value.startswith("'") and value.endswith("'")):
                value = value[1:-1]
            
            # Substitute environment variables
            value = self.substitute_env(value)
            
            if not key:
                raise ConfigParseError(f"Line {line_num}: Empty key")
            
            result[key] = value
        
        return result
    
    def parse_env(self, content: str) -> Dict[str, str]:
        """
        Parse .env file format content.
        
        Similar to key-value but with .env conventions.
        
        Args:
            content: Raw content string
            
        Returns:
            Dictionary of key-value pairs
        """
        return self.parse_key_value(content)
    
    def parse_ini(self, content: str) -> Dict[str, Dict[str, str]]:
        """
        Parse INI format content.
        
        Format:
        ```
        [section]
        key=value
        ```
        
        Args:
            content: Raw content string
            
        Returns:
            Nested dictionary: {section: {key: value}}
        """
        result: Dict[str, Dict[str, str]] = {}
        current_section = "DEFAULT"
        result[current_section] = {}
        
        for line_num, line in enumerate(content.splitlines(), 1):
            line = line.strip()
            
            # Skip empty lines and comments
            if not line or line.startswith('#') or line.startswith(';'):
                continue
            
            # Section header
            if line.startswith('[') and line.endswith(']'):
                current_section = line[1:-1].strip()
                if current_section not in result:
                    result[current_section] = {}
                continue
            
            # Key-value pair
            if '=' not in line:
                raise ConfigParseError(f"Line {line_num}: Missing '=' in INI file")
            
            key, _, value = line.partition('=')
            key = key.strip()
            value = value.strip()
            
            # Remove quotes
            if (value.startswith('"') and value.endswith('"')) or \
               (value.startswith("'") and value.endswith("'")):
                value = value[1:-1]
            
            # Substitute environment variables
            value = self.substitute_env(value)
            
            result[current_section][key] = value
        
        # Remove DEFAULT section if empty
        if not result.get("DEFAULT"):
            del result["DEFAULT"]
        
        return result
    
    def parse_json(self, content: str) -> Dict[str, Any]:
        """
        Parse JSON format content.
        
        Args:
            content: Raw JSON string
            
        Returns:
            Parsed dictionary
        """
        try:
            return json.loads(content)
        except json.JSONDecodeError as e:
            raise ConfigParseError(f"Invalid JSON: {e}")
    
    def parse(self, content: str, format: ConfigFormat = ConfigFormat.KEY_VALUE) -> Dict[str, Any]:
        """
        Parse configuration content in the specified format.
        
        Args:
            content: Raw content string
            format: Configuration format
            
        Returns:
            Parsed configuration dictionary
        """
        if format == ConfigFormat.KEY_VALUE:
            return self.parse_key_value(content)
        elif format == ConfigFormat.ENV:
            return self.parse_env(content)
        elif format == ConfigFormat.INI:
            return self.parse_ini(content)
        elif format == ConfigFormat.JSON:
            return self.parse_json(content)
        else:
            raise ConfigParseError(f"Unsupported format: {format}")
    
    def parse_file(self, path: Union[str, Path], format: Optional[ConfigFormat] = None) -> Dict[str, Any]:
        """
        Parse a configuration file.
        
        Args:
            path: Path to the configuration file
            format: Configuration format (auto-detected if None)
            
        Returns:
            Parsed configuration dictionary
        """
        path = Path(path)
        
        if not path.exists():
            raise ConfigFileError(f"Configuration file not found: {path}")
        
        # Auto-detect format from extension
        if format is None:
            ext = path.suffix.lower()
            format_map = {
                '.json': ConfigFormat.JSON,
                '.ini': ConfigFormat.INI,
                '.env': ConfigFormat.ENV,
                '.conf': ConfigFormat.KEY_VALUE,
                '.cfg': ConfigFormat.KEY_VALUE,
            }
            format = format_map.get(ext, ConfigFormat.KEY_VALUE)
        
        try:
            content = path.read_text(encoding='utf-8')
        except IOError as e:
            raise ConfigFileError(f"Failed to read configuration file: {e}")
        
        return self.parse(content, format)


class Config:
    """
    Configuration manager with validation, type coercion, and environment support.
    
    Features:
    - Load from files or dictionaries
    - Environment variable substitution
    - Schema validation
    - Type coercion
    - Nested configuration access
    - Default values
    - Immutable after validation (optional)
    """
    
    def __init__(
        self,
        data: Optional[Dict[str, Any]] = None,
        schema: Optional[ConfigSchema] = None,
        env_substitute: bool = True,
        env_prefix: str = "",
        immutable: bool = False
    ):
        """
        Initialize configuration.
        
        Args:
            data: Initial configuration data
            schema: Schema for validation
            env_substitute: Enable environment variable substitution
            env_prefix: Prefix for environment variable lookups
            immutable: Make configuration immutable after initialization
        """
        self._data: Dict[str, Any] = {}
        self._schema = schema
        self._immutable = immutable
        self._parser = ConfigParser(env_prefix)
        self._env_substitute = env_substitute
        
        if data:
            self.update(data)
        
        if schema:
            self.validate()
    
    def _coerce_type(self, value: Any, target_type: type) -> Any:
        """Coerce a value to the target type."""
        if isinstance(value, target_type):
            return value
        
        try:
            if target_type == bool:
                if isinstance(value, str):
                    return value.lower() in ('true', 'yes', '1', 'on')
                return bool(value)
            elif target_type == list:
                if isinstance(value, str):
                    return [v.strip() for v in value.split(',')]
                return list(value)
            elif target_type == dict:
                if isinstance(value, str):
                    return json.loads(value)
                return dict(value)
            else:
                return target_type(value)
        except (ValueError, TypeError, json.JSONDecodeError):
            return value
    
    def _process_value(self, value: Any) -> Any:
        """Process a value (env substitution, type coercion)."""
        if not self._env_substitute:
            return value
        
        if isinstance(value, str):
            value = self._parser.substitute_env(value)
        elif isinstance(value, dict):
            value = {k: self._process_value(v) for k, v in value.items()}
        elif isinstance(value, list):
            value = [self._process_value(v) for v in value]
        
        return value
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration value.
        
        Supports dot notation for nested access: "database.host"
        
        Args:
            key: Configuration key (supports dot notation)
            default: Default value if key doesn't exist
            
        Returns:
            Configuration value or default
        """
        keys = key.split('.')
        value = self._data
        
        try:
            for k in keys:
                if isinstance(value, dict):
                    value = value[k]
                else:
                    return default
        except (KeyError, TypeError):
            return default
        
        return value
    
    def get_typed(self, key: str, type_: type, default: Any = None) -> Any:
        """
        Get a configuration value with type coercion.
        
        Args:
            key: Configuration key
            type_: Target type
            default: Default value
            
        Returns:
            Typed configuration value
        """
        value = self.get(key, default)
        return self._coerce_type(value, type_)
    
    def get_int(self, key: str, default: int = 0) -> int:
        """Get an integer configuration value."""
        return self.get_typed(key, int, default)
    
    def get_float(self, key: str, default: float = 0.0) -> float:
        """Get a float configuration value."""
        return self.get_typed(key, float, default)
    
    def get_bool(self, key: str, default: bool = False) -> bool:
        """Get a boolean configuration value."""
        return self.get_typed(key, bool, default)
    
    def get_list(self, key: str, default: Optional[List] = None) -> List:
        """Get a list configuration value."""
        return self.get_typed(key, list, default or [])
    
    def get_dict(self, key: str, default: Optional[Dict] = None) -> Dict:
        """Get a dictionary configuration value."""
        return self.get_typed(key, dict, default or {})
    
    def set(self, key: str, value: Any) -> 'Config':
        """
        Set a configuration value.
        
        Args:
            key: Configuration key (supports dot notation)
            value: Configuration value
            
        Returns:
            Self for chaining
            
        Raises:
            ConfigError: If configuration is immutable
        """
        if self._immutable:
            raise ConfigError("Cannot modify immutable configuration")
        
        keys = key.split('.')
        current = self._data
        
        # Navigate to the parent
        for k in keys[:-1]:
            if k not in current:
                current[k] = {}
            current = current[k]
        
        # Process and set the value
        current[keys[-1]] = self._process_value(value)
        
        return self
    
    def update(self, data: Dict[str, Any]) -> 'Config':
        """
        Update configuration with new data.
        
        Args:
            data: New configuration data
            
        Returns:
            Self for chaining
        """
        for key, value in data.items():
            self.set(key, value)
        
        return self
    
    def delete(self, key: str) -> bool:
        """
        Delete a configuration key.
        
        Args:
            key: Configuration key
            
        Returns:
            True if key was deleted, False if it didn't exist
        """
        if self._immutable:
            raise ConfigError("Cannot modify immutable configuration")
        
        keys = key.split('.')
        current = self._data
        
        try:
            for k in keys[:-1]:
                current = current[k]
            del current[keys[-1]]
            return True
        except (KeyError, TypeError):
            return False
    
    def has(self, key: str) -> bool:
        """
        Check if a configuration key exists.
        
        Args:
            key: Configuration key
            
        Returns:
            True if key exists
        """
        return self.get(key, _SENTINEL) is not _SENTINEL
    
    def keys(self) -> List[str]:
        """Get all top-level configuration keys."""
        return list(self._data.keys())
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary."""
        return dict(self._data)
    
    def validate(self, schema: Optional[ConfigSchema] = None) -> Tuple[bool, List[str]]:
        """
        Validate configuration against a schema.
        
        Args:
            schema: Schema to validate against (uses instance schema if None)
            
        Returns:
            Tuple of (is_valid, list of errors)
        """
        schema = schema or self._schema
        
        if not schema:
            return True, []
        
        return schema.validate(self._data)
    
    def validate_strict(self, schema: Optional[ConfigSchema] = None) -> None:
        """
        Validate configuration strictly, raising on errors.
        
        Args:
            schema: Schema to validate against
            
        Raises:
            ConfigValidationError: If validation fails
        """
        is_valid, errors = self.validate(schema)
        
        if not is_valid:
            raise ConfigValidationError("Configuration validation failed:\n" + "\n".join(errors))
    
    def make_immutable(self) -> 'Config':
        """Make this configuration immutable."""
        self._immutable = True
        return self
    
    def freeze(self) -> 'Config':
        """Alias for make_immutable."""
        return self.make_immutable()
    
    def __getitem__(self, key: str) -> Any:
        """Get item using bracket notation."""
        value = self.get(key, _SENTINEL)
        if value is _SENTINEL:
            raise KeyError(key)
        return value
    
    def __setitem__(self, key: str, value: Any) -> None:
        """Set item using bracket notation."""
        self.set(key, value)
    
    def __contains__(self, key: str) -> bool:
        """Check if key exists using 'in' operator."""
        return self.has(key)
    
    def __repr__(self) -> str:
        return f"Config({self._data!r})"
    
    def __len__(self) -> int:
        return len(self._data)


# Sentinel object for default detection
_SENTINEL = object()


# Convenience functions

def load_config(
    path: Union[str, Path],
    format: Optional[ConfigFormat] = None,
    schema: Optional[ConfigSchema] = None,
    env_substitute: bool = True,
    env_prefix: str = ""
) -> Config:
    """
    Load configuration from a file.
    
    Args:
        path: Path to configuration file
        format: Configuration format (auto-detected if None)
        schema: Schema for validation
        env_substitute: Enable environment variable substitution
        env_prefix: Prefix for environment variable lookups
        
    Returns:
        Config object
    """
    parser = ConfigParser(env_prefix)
    data = parser.parse_file(path, format)
    return Config(data, schema, env_substitute, env_prefix)


def create_config(
    data: Optional[Dict[str, Any]] = None,
    schema: Optional[ConfigSchema] = None,
    env_substitute: bool = True,
    env_prefix: str = ""
) -> Config:
    """
    Create a new configuration.
    
    Args:
        data: Initial configuration data
        schema: Schema for validation
        env_substitute: Enable environment variable substitution
        env_prefix: Prefix for environment variable lookups
        
    Returns:
        Config object
    """
    return Config(data, schema, env_substitute, env_prefix)


def create_schema(**fields) -> ConfigSchema:
    """
    Create a configuration schema.
    
    Args:
        **fields: Field definitions as keyword arguments
        
    Returns:
        ConfigSchema object
        
    Example:
        schema = create_schema(
            host=dict(type=str, required=True),
            port=dict(type=int, required=True, min=1, max=65535),
            debug=dict(type=bool, default=False),
            log_level=dict(type=str, choices=['DEBUG', 'INFO', 'WARNING', 'ERROR']),
        )
    """
    schema = ConfigSchema()
    
    for key, kwargs in fields.items():
        schema.add_field(key, **kwargs)
    
    return schema


def parse_config(
    content: str,
    format: ConfigFormat = ConfigFormat.KEY_VALUE,
    env_prefix: str = ""
) -> Dict[str, Any]:
    """
    Parse configuration content.
    
    Args:
        content: Raw configuration content
        format: Configuration format
        env_prefix: Prefix for environment variable lookups
        
    Returns:
        Parsed configuration dictionary
    """
    parser = ConfigParser(env_prefix)
    return parser.parse(content, format)


# Pre-built schemas for common configurations

DATABASE_SCHEMA = create_schema(
    host=dict(type=str, required=True, description="Database host"),
    port=dict(type=int, default=5432, min=1, max=65535, description="Database port"),
    name=dict(type=str, required=True, description="Database name"),
    user=dict(type=str, required=True, description="Database user"),
    password=dict(type=str, required=True, description="Database password"),
    ssl=dict(type=bool, default=False, description="Use SSL connection"),
)

SERVER_SCHEMA = create_schema(
    host=dict(type=str, default="0.0.0.0", description="Server host"),
    port=dict(type=int, required=True, min=1, max=65535, description="Server port"),
    debug=dict(type=bool, default=False, description="Debug mode"),
    workers=dict(type=int, default=4, min=1, max=64, description="Number of workers"),
)

LOGGING_SCHEMA = create_schema(
    level=dict(type=str, default="INFO", choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']),
    format=dict(type=str, default="%(asctime)s - %(name)s - %(levelname)s - %(message)s"),
    file=dict(type=str, default=None),
    max_size=dict(type=int, default=10485760, description="Max log file size in bytes"),
    backup_count=dict(type=int, default=5, description="Number of backup files"),
)
