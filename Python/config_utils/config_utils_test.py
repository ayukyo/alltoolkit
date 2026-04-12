"""
AllToolkit - Python Configuration Utilities Test Suite

Comprehensive tests for the config_utils module.
"""

import os
import sys
import tempfile
from pathlib import Path

# Import the module under test
from mod import (
    Config,
    ConfigParser,
    ConfigSchema,
    SchemaField,
    ConfigFormat,
    ConfigError,
    ConfigValidationError,
    ConfigParseError,
    ConfigFileError,
    load_config,
    create_config,
    create_schema,
    parse_config,
    DATABASE_SCHEMA,
    SERVER_SCHEMA,
    LOGGING_SCHEMA,
)


class TestResult:
    """Simple test result tracker."""
    
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors = []
    
    def ok(self, test_name: str):
        self.passed += 1
        print(f"  ✓ {test_name}")
    
    def fail(self, test_name: str, message: str):
        self.failed += 1
        self.errors.append((test_name, message))
        print(f"  ✗ {test_name}: {message}")
    
    def summary(self):
        total = self.passed + self.failed
        print(f"\n{'='*60}")
        print(f"Results: {self.passed}/{total} tests passed")
        if self.failed > 0:
            print(f"\nFailed tests:")
            for name, msg in self.errors:
                print(f"  - {name}: {msg}")
        return self.failed == 0


result = TestResult()


def test_parser_key_value():
    """Test key-value format parsing."""
    parser = ConfigParser()
    
    content = """
# This is a comment
host=localhost
port=8080
name="My Application"
description='Single quoted value'
"""
    
    try:
        config = parser.parse_key_value(content)
        assert config['host'] == 'localhost', f"Expected 'localhost', got {config['host']}"
        assert config['port'] == '8080', f"Expected '8080', got {config['port']}"
        assert config['name'] == 'My Application', f"Expected 'My Application', got {config['name']}"
        assert config['description'] == 'Single quoted value', f"Expected 'Single quoted value', got {config['description']}"
        result.ok("Key-value parsing")
    except Exception as e:
        result.fail("Key-value parsing", str(e))


def test_parser_env_substitution():
    """Test environment variable substitution."""
    # Set up test environment variables
    os.environ['TEST_HOST'] = 'example.com'
    os.environ['TEST_PORT'] = '3000'
    
    parser = ConfigParser()
    
    content = """
host=${TEST_HOST}
port=$TEST_PORT
with_default=${NONEXISTENT:-fallback}
"""
    
    try:
        config = parser.parse_key_value(content)
        assert config['host'] == 'example.com', f"Expected 'example.com', got {config['host']}"
        assert config['port'] == '3000', f"Expected '3000', got {config['port']}"
        assert config['with_default'] == 'fallback', f"Expected 'fallback', got {config['with_default']}"
        result.ok("Environment variable substitution")
    except Exception as e:
        result.fail("Environment variable substitution", str(e))
    
    # Cleanup
    del os.environ['TEST_HOST']
    del os.environ['TEST_PORT']


def test_parser_json():
    """Test JSON format parsing."""
    parser = ConfigParser()
    
    content = """
{
    "host": "localhost",
    "port": 8080,
    "nested": {
        "key": "value"
    },
    "array": [1, 2, 3]
}
"""
    
    try:
        config = parser.parse_json(content)
        assert config['host'] == 'localhost', f"Expected 'localhost', got {config['host']}"
        assert config['port'] == 8080, f"Expected 8080, got {config['port']}"
        assert config['nested']['key'] == 'value', f"Expected nested value"
        assert config['array'] == [1, 2, 3], f"Expected array [1, 2, 3]"
        result.ok("JSON parsing")
    except Exception as e:
        result.fail("JSON parsing", str(e))


def test_parser_ini():
    """Test INI format parsing."""
    parser = ConfigParser()
    
    content = """
[database]
host=localhost
port=5432

[server]
host=0.0.0.0
port=8080
"""
    
    try:
        config = parser.parse_ini(content)
        assert 'database' in config, "Expected 'database' section"
        assert config['database']['host'] == 'localhost', f"Expected 'localhost'"
        assert config['database']['port'] == '5432', f"Expected '5432'"
        assert config['server']['port'] == '8080', f"Expected '8080'"
        result.ok("INI parsing")
    except Exception as e:
        result.fail("INI parsing", str(e))


def test_parser_invalid_format():
    """Test parsing invalid format."""
    parser = ConfigParser()
    
    content = "invalid line without equals"
    
    try:
        parser.parse_key_value(content)
        result.fail("Invalid format detection", "Should have raised ConfigParseError")
    except ConfigParseError:
        result.ok("Invalid format detection")
    except Exception as e:
        result.fail("Invalid format detection", f"Wrong exception: {e}")


def test_config_basic():
    """Test basic Config operations."""
    config = Config({
        'host': 'localhost',
        'port': 8080,
        'debug': True,
    })
    
    try:
        assert config.get('host') == 'localhost', f"Expected 'localhost'"
        assert config.get('port') == 8080, f"Expected 8080"
        assert config.get('debug') == True, f"Expected True"
        assert config.get('missing', 'default') == 'default', f"Expected default value"
        result.ok("Basic Config operations")
    except Exception as e:
        result.fail("Basic Config operations", str(e))


def test_config_nested():
    """Test nested configuration access."""
    config = Config({
        'database': {
            'host': 'localhost',
            'port': 5432,
            'credentials': {
                'user': 'admin',
                'password': 'secret',
            }
        }
    })
    
    try:
        assert config.get('database.host') == 'localhost', f"Expected 'localhost'"
        assert config.get('database.port') == 5432, f"Expected 5432"
        assert config.get('database.credentials.user') == 'admin', f"Expected 'admin'"
        assert config.get('database.credentials.password') == 'secret', f"Expected 'secret'"
        result.ok("Nested configuration access")
    except Exception as e:
        result.fail("Nested configuration access", str(e))


def test_config_typed_getters():
    """Test typed getter methods."""
    config = Config({
        'count': '42',
        'ratio': '3.14',
        'enabled': 'true',
        'tags': 'a,b,c',
        'metadata': '{"key": "value"}',
    })
    
    try:
        assert config.get_int('count') == 42, f"Expected 42, got {config.get_int('count')}"
        assert config.get_float('ratio') == 3.14, f"Expected 3.14, got {config.get_float('ratio')}"
        assert config.get_bool('enabled') == True, f"Expected True, got {config.get_bool('enabled')}"
        assert config.get_list('tags') == ['a', 'b', 'c'], f"Expected ['a', 'b', 'c']"
        assert config.get_dict('metadata') == {'key': 'value'}, f"Expected dict"
        result.ok("Typed getter methods")
    except Exception as e:
        result.fail("Typed getter methods", str(e))


def test_config_set_and_update():
    """Test setting and updating configuration."""
    config = Config()
    
    try:
        config.set('host', 'localhost')
        config.set('server.port', 8080)
        config.update({'debug': True, 'name': 'Test'})
        
        assert config.get('host') == 'localhost', f"Expected 'localhost'"
        assert config.get('server.port') == 8080, f"Expected 8080"
        assert config.get('debug') == True, f"Expected True"
        assert config.get('name') == 'Test', f"Expected 'Test'"
        result.ok("Setting and updating configuration")
    except Exception as e:
        result.fail("Setting and updating configuration", str(e))


def test_config_immutable():
    """Test immutable configuration."""
    config = Config({'host': 'localhost'}).make_immutable()
    
    try:
        config.set('port', 8080)
        result.fail("Immutable config", "Should have raised ConfigError")
    except ConfigError:
        result.ok("Immutable configuration")
    except Exception as e:
        result.fail("Immutable config", f"Wrong exception: {e}")


def test_config_has_and_delete():
    """Test has() and delete() methods."""
    config = Config({'host': 'localhost', 'port': 8080})
    
    try:
        assert config.has('host') == True, "Expected host to exist"
        assert config.has('missing') == False, "Expected missing to not exist"
        
        assert config.delete('host') == True, "Expected delete to return True"
        assert config.has('host') == False, "Expected host to be deleted"
        assert config.delete('missing') == False, "Expected delete to return False"
        result.ok("has() and delete() methods")
    except Exception as e:
        result.fail("has() and delete() methods", str(e))


def test_config_bracket_notation():
    """Test bracket notation access."""
    config = Config({'host': 'localhost', 'port': 8080})
    
    try:
        assert config['host'] == 'localhost', f"Expected 'localhost'"
        
        config['new_key'] = 'new_value'
        assert config['new_key'] == 'new_value', f"Expected 'new_value'"
        
        assert 'port' in config, "Expected 'port' to be in config"
        assert 'missing' not in config, "Expected 'missing' to not be in config"
        result.ok("Bracket notation access")
    except Exception as e:
        result.fail("Bracket notation access", str(e))


def test_schema_validation_basic():
    """Test basic schema validation."""
    schema = create_schema(
        host=dict(type=str, required=True),
        port=dict(type=int, required=True, min=1, max=65535),
        debug=dict(type=bool, default=False),
    )
    
    try:
        # Valid config
        config = Config({'host': 'localhost', 'port': 8080}, schema)
        is_valid, errors = config.validate()
        assert is_valid == True, f"Expected valid config, got errors: {errors}"
        
        # Invalid config - missing required
        config2 = Config({'host': 'localhost'}, schema)
        is_valid, errors = config2.validate()
        assert is_valid == False, "Expected invalid config"
        assert any('port' in e for e in errors), f"Expected port error in {errors}"
        
        # Invalid config - out of range
        config3 = Config({'host': 'localhost', 'port': 100000}, schema)
        is_valid, errors = config3.validate()
        assert is_valid == False, "Expected invalid config"
        assert any('maximum' in e for e in errors), f"Expected range error in {errors}"
        
        result.ok("Basic schema validation")
    except Exception as e:
        result.fail("Basic schema validation", str(e))


def test_schema_choices():
    """Test schema with choices."""
    schema = create_schema(
        level=dict(type=str, choices=['DEBUG', 'INFO', 'WARNING', 'ERROR']),
    )
    
    try:
        config = Config({'level': 'INFO'}, schema)
        is_valid, errors = config.validate()
        assert is_valid == True, f"Expected valid, got: {errors}"
        
        config2 = Config({'level': 'INVALID'}, schema)
        is_valid, errors = config2.validate()
        assert is_valid == False, "Expected invalid"
        assert any('choices' in e for e in errors), f"Expected choices error in {errors}"
        
        result.ok("Schema with choices")
    except Exception as e:
        result.fail("Schema with choices", str(e))


def test_schema_pattern():
    """Test schema with pattern validation."""
    schema = create_schema(
        email=dict(type=str, pattern=r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'),
    )
    
    try:
        config = Config({'email': 'test@example.com'}, schema)
        is_valid, errors = config.validate()
        assert is_valid == True, f"Expected valid, got: {errors}"
        
        config2 = Config({'email': 'invalid-email'}, schema)
        is_valid, errors = config2.validate()
        assert is_valid == False, "Expected invalid"
        assert any('pattern' in e for e in errors), f"Expected pattern error in {errors}"
        
        result.ok("Schema with pattern validation")
    except Exception as e:
        result.fail("Schema with pattern validation", str(e))


def test_schema_strict_mode():
    """Test strict schema mode."""
    schema = ConfigSchema(
        fields={'host': SchemaField(type=str)},
        strict=True
    )
    
    try:
        config = Config({'host': 'localhost', 'unknown': 'value'}, schema)
        is_valid, errors = config.validate()
        assert is_valid == False, "Expected invalid in strict mode"
        assert any('Unknown' in e for e in errors), f"Expected unknown key error in {errors}"
        
        result.ok("Strict schema mode")
    except Exception as e:
        result.fail("Strict schema mode", str(e))


def test_prebuilt_schemas():
    """Test pre-built schemas."""
    try:
        # DATABASE_SCHEMA
        db_config = Config({
            'host': 'localhost',
            'name': 'mydb',
            'user': 'admin',
            'password': 'secret',
        }, DATABASE_SCHEMA)
        is_valid, errors = db_config.validate()
        assert is_valid == True, f"Expected valid DB config, got: {errors}"
        
        # SERVER_SCHEMA
        server_config = Config({
            'port': 8080,
            'workers': 4,
        }, SERVER_SCHEMA)
        is_valid, errors = server_config.validate()
        assert is_valid == True, f"Expected valid server config, got: {errors}"
        
        # LOGGING_SCHEMA
        log_config = Config({
            'level': 'DEBUG',
            'max_size': 10485760,
        }, LOGGING_SCHEMA)
        is_valid, errors = log_config.validate()
        assert is_valid == True, f"Expected valid logging config, got: {errors}"
        
        result.ok("Pre-built schemas")
    except Exception as e:
        result.fail("Pre-built schemas", str(e))


def test_load_config_from_file():
    """Test loading configuration from file."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.conf', delete=False) as f:
        f.write("""
# Test configuration
host=localhost
port=8080
debug=true
""")
        temp_path = f.name
    
    try:
        config = load_config(temp_path)
        assert config.get('host') == 'localhost', f"Expected 'localhost'"
        assert config.get('port') == '8080', f"Expected '8080'"
        assert config.get('debug') == 'true', f"Expected 'true'"
        result.ok("Load configuration from file")
    except Exception as e:
        result.fail("Load configuration from file", str(e))
    finally:
        os.unlink(temp_path)


def test_load_json_file():
    """Test loading JSON configuration from file."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        f.write('{"host": "localhost", "port": 8080}')
        temp_path = f.name
    
    try:
        config = load_config(temp_path)
        assert config.get('host') == 'localhost', f"Expected 'localhost'"
        assert config.get('port') == 8080, f"Expected 8080"
        result.ok("Load JSON configuration from file")
    except Exception as e:
        result.fail("Load JSON configuration from file", str(e))
    finally:
        os.unlink(temp_path)


def test_file_not_found():
    """Test file not found error."""
    try:
        load_config('/nonexistent/path/config.conf')
        result.fail("File not found", "Should have raised ConfigFileError")
    except ConfigFileError:
        result.ok("File not found error")
    except Exception as e:
        result.fail("File not found", f"Wrong exception: {e}")


def test_parse_config_function():
    """Test parse_config convenience function."""
    content = "host=localhost\nport=8080"
    
    try:
        config = parse_config(content)
        assert config['host'] == 'localhost', f"Expected 'localhost'"
        assert config['port'] == '8080', f"Expected '8080'"
        result.ok("parse_config function")
    except Exception as e:
        result.fail("parse_config function", str(e))


def test_create_config_function():
    """Test create_config convenience function."""
    try:
        config = create_config({'host': 'localhost', 'port': 8080})
        assert config.get('host') == 'localhost', f"Expected 'localhost'"
        assert config.get('port') == 8080, f"Expected 8080"
        result.ok("create_config function")
    except Exception as e:
        result.fail("create_config function", str(e))


def test_env_prefix():
    """Test environment variable prefix."""
    os.environ['APP_HOST'] = 'prefixed.example.com'
    
    parser = ConfigParser(env_prefix='APP_')
    
    try:
        content = "host=${HOST}"
        config = parser.parse_key_value(content)
        assert config['host'] == 'prefixed.example.com', f"Expected prefixed value, got {config['host']}"
        result.ok("Environment variable prefix")
    except Exception as e:
        result.fail("Environment variable prefix", str(e))
    finally:
        del os.environ['APP_HOST']


def test_config_repr():
    """Test Config string representation."""
    config = Config({'host': 'localhost', 'port': 8080})
    
    try:
        repr_str = repr(config)
        assert 'Config' in repr_str, f"Expected 'Config' in repr"
        assert 'localhost' in repr_str, f"Expected 'localhost' in repr"
        result.ok("Config string representation")
    except Exception as e:
        result.fail("Config string representation", str(e))


def test_config_len():
    """Test Config length."""
    config = Config({'host': 'localhost', 'port': 8080, 'debug': True})
    
    try:
        assert len(config) == 3, f"Expected length 3, got {len(config)}"
        result.ok("Config length")
    except Exception as e:
        result.fail("Config length", str(e))


def test_config_keys():
    """Test Config keys method."""
    config = Config({'host': 'localhost', 'port': 8080, 'debug': True})
    
    try:
        keys = config.keys()
        assert 'host' in keys, "Expected 'host' in keys"
        assert 'port' in keys, "Expected 'port' in keys"
        assert 'debug' in keys, "Expected 'debug' in keys"
        result.ok("Config keys method")
    except Exception as e:
        result.fail("Config keys method", str(e))


def test_validate_strict():
    """Test validate_strict method."""
    schema = create_schema(
        host=dict(type=str, required=True),
    )
    
    config = Config({}, schema)
    
    try:
        config.validate_strict()
        result.fail("validate_strict", "Should have raised ConfigValidationError")
    except ConfigValidationError:
        result.ok("validate_strict method")
    except Exception as e:
        result.fail("validate_strict", f"Wrong exception: {e}")


def test_complex_env_substitution():
    """Test complex environment variable substitution scenarios."""
    os.environ['DB_HOST'] = 'db.example.com'
    os.environ['DB_PORT'] = '5432'
    os.environ['APP_NAME'] = 'MyApp'
    
    config = Config({
        'database_url': 'postgresql://${DB_HOST}:${DB_PORT}/mydb',
        'app_name': '${APP_NAME}',
        'fallback': '${MISSING:-default_value}',
    }, env_substitute=True)
    
    try:
        assert config.get('database_url') == 'postgresql://db.example.com:5432/mydb', \
            f"Expected substituted URL, got {config.get('database_url')}"
        assert config.get('app_name') == 'MyApp', f"Expected 'MyApp', got {config.get('app_name')}"
        assert config.get('fallback') == 'default_value', f"Expected 'default_value', got {config.get('fallback')}"
        result.ok("Complex environment variable substitution")
    except Exception as e:
        result.fail("Complex environment variable substitution", str(e))
    finally:
        del os.environ['DB_HOST']
        del os.environ['DB_PORT']
        del os.environ['APP_NAME']


def run_all_tests():
    """Run all tests."""
    print("=" * 60)
    print("AllToolkit - Configuration Utilities Test Suite")
    print("=" * 60)
    
    print("\n[Parser Tests]")
    test_parser_key_value()
    test_parser_env_substitution()
    test_parser_json()
    test_parser_ini()
    test_parser_invalid_format()
    
    print("\n[Config Tests]")
    test_config_basic()
    test_config_nested()
    test_config_typed_getters()
    test_config_set_and_update()
    test_config_immutable()
    test_config_has_and_delete()
    test_config_bracket_notation()
    test_config_repr()
    test_config_len()
    test_config_keys()
    
    print("\n[Schema Tests]")
    test_schema_validation_basic()
    test_schema_choices()
    test_schema_pattern()
    test_schema_strict_mode()
    test_prebuilt_schemas()
    test_validate_strict()
    
    print("\n[File I/O Tests]")
    test_load_config_from_file()
    test_load_json_file()
    test_file_not_found()
    
    print("\n[Convenience Functions]")
    test_parse_config_function()
    test_create_config_function()
    
    print("\n[Advanced Features]")
    test_env_prefix()
    test_complex_env_substitution()
    
    return result.summary()


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
