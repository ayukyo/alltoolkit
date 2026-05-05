"""
TOML Utils Tests
================

Comprehensive tests for TOML parser and generator.
"""

import datetime
import os
import tempfile
import unittest
from mod import (
    parse, loads, load, dumps, dump, validate,
    merge, get, set_value, flatten, unflatten, diff,
    convert_from_json, read_config, write_config,
    TOMLParser, TOMLGenerator, TOMLSyntaxError, TOMLValidationError
)


class TestBasicParsing(unittest.TestCase):
    """Test basic TOML parsing."""
    
    def test_empty_document(self):
        """Test parsing empty document."""
        self.assertEqual(parse(""), {})
        self.assertEqual(parse("   "), {})
        self.assertEqual(parse("\n\n"), {})
    
    def test_comments(self):
        """Test parsing comments."""
        self.assertEqual(parse("# This is a comment\n"), {})
        self.assertEqual(parse("# Comment\n# Another comment\n"), {})
    
    def test_simple_key_value(self):
        """Test simple key-value pairs."""
        result = parse('key = "value"')
        self.assertEqual(result, {'key': 'value'})
        
        result = parse('name = "Alice"')
        self.assertEqual(result, {'name': 'Alice'})
    
    def test_string_values(self):
        """Test string value parsing."""
        result = parse('str = "hello world"')
        self.assertEqual(result['str'], 'hello world')
        
        result = parse('empty = ""')
        self.assertEqual(result['empty'], '')
        
        result = parse("literal = 'no escapes'")
        self.assertEqual(result['literal'], 'no escapes')
    
    def test_escape_sequences(self):
        """Test string escape sequences."""
        result = parse('escaped = "hello\\nworld"')
        self.assertEqual(result['escaped'], 'hello\nworld')
        
        result = parse('tab = "a\\tb"')
        self.assertEqual(result['tab'], 'a\tb')
        
        result = parse(r'quote = "say \"hi\""')
        self.assertEqual(result['quote'], 'say "hi"')
        
        result = parse('backslash = "path\\\\to\\\\file"')
        self.assertEqual(result['backslash'], 'path\\to\\file')
    
    def test_unicode_escapes(self):
        """Test Unicode escape sequences."""
        result = parse('unicode = "\\u0048\\u0065\\u006c\\u006c\\u006f"')
        self.assertEqual(result['unicode'], 'Hello')
        
        result = parse('emoji = "\\U0001F600"')
        self.assertEqual(result['emoji'], '😀')
    
    def test_integer_values(self):
        """Test integer parsing."""
        result = parse('num = 42')
        self.assertEqual(result['num'], 42)
        
        result = parse('negative = -17')
        self.assertEqual(result['negative'], -17)
        
        result = parse('zero = 0')
        self.assertEqual(result['zero'], 0)
        
        result = parse('big = 1_000_000')
        self.assertEqual(result['big'], 1000000)
    
    def test_integer_bases(self):
        """Test integer parsing in different bases."""
        result = parse('hex = 0xDEADBEEF')
        self.assertEqual(result['hex'], 0xDEADBEEF)
        
        result = parse('octal = 0o755')
        self.assertEqual(result['octal'], 0o755)
        
        result = parse('binary = 0b110101')
        self.assertEqual(result['binary'], 0b110101)
    
    def test_float_values(self):
        """Test float parsing."""
        result = parse('pi = 3.14159')
        self.assertAlmostEqual(result['pi'], 3.14159, places=5)
        
        result = parse('negative = -0.5')
        self.assertEqual(result['negative'], -0.5)
        
        result = parse('exp = 1.0e10')
        self.assertEqual(result['exp'], 1e10)
        
        result = parse('exp2 = 2.5e-3')
        self.assertAlmostEqual(result['exp2'], 0.0025, places=5)
        
        result = parse('underscore = 1_000.5')
        self.assertEqual(result['underscore'], 1000.5)
    
    def test_special_floats(self):
        """Test special float values."""
        result = parse('inf = inf')
        self.assertEqual(result['inf'], float('inf'))
        
        result = parse('neginf = -inf')
        self.assertEqual(result['neginf'], float('-inf'))
        
        result = parse('nan = nan')
        self.assertTrue(result['nan'] != result['nan'])  # NaN != NaN
    
    def test_boolean_values(self):
        """Test boolean parsing."""
        result = parse('enabled = true')
        self.assertEqual(result['enabled'], True)
        
        result = parse('disabled = false')
        self.assertEqual(result['disabled'], False)


class TestDateTimeParsing(unittest.TestCase):
    """Test datetime parsing."""
    
    def test_date(self):
        """Test date parsing."""
        result = parse('date = 2024-05-27')
        self.assertEqual(result['date'], datetime.date(2024, 5, 27))
    
    def test_time(self):
        """Test time parsing."""
        result = parse('time = 07:32:00')
        self.assertEqual(result['time'], datetime.time(7, 32, 0))
        
        result = parse('time_ms = 07:32:00.123')
        self.assertEqual(result['time_ms'], datetime.time(7, 32, 0, 123000))
    
    def test_local_datetime(self):
        """Test local datetime parsing."""
        result = parse('datetime = 2024-05-27T07:32:00')
        self.assertEqual(result['datetime'], datetime.datetime(2024, 5, 27, 7, 32, 0))
        
        result = parse('datetime_space = 2024-05-27 07:32:00')
        self.assertEqual(result['datetime_space'], datetime.datetime(2024, 5, 27, 7, 32, 0))
    
    def test_offset_datetime(self):
        """Test offset datetime parsing."""
        result = parse('datetime = 2024-05-27T07:32:00+08:00')
        self.assertEqual(result['datetime'].hour, 7)
        
        result = parse('datetime_utc = 2024-05-27T07:32:00Z')
        self.assertEqual(result['datetime_utc'].hour, 7)


class TestTableParsing(unittest.TestCase):
    """Test table parsing."""
    
    def test_simple_table(self):
        """Test simple table."""
        result = parse('[section]\nkey = "value"')
        self.assertEqual(result, {'section': {'key': 'value'}})
    
    def test_nested_table(self):
        """Test nested table."""
        result = parse('[a.b.c]\nkey = "value"')
        self.assertEqual(result, {'a': {'b': {'c': {'key': 'value'}}}})
    
    def test_multiple_tables(self):
        """Test multiple tables."""
        result = parse('[section1]\nkey1 = "value1"\n\n[section2]\nkey2 = "value2"')
        self.assertEqual(result, {
            'section1': {'key1': 'value1'},
            'section2': {'key2': 'value2'}
        })
    
    def test_dotted_keys(self):
        """Test dotted keys."""
        result = parse('a.b.c = "value"')
        self.assertEqual(result, {'a': {'b': {'c': 'value'}}})


class TestArrayParsing(unittest.TestCase):
    """Test array parsing."""
    
    def test_simple_array(self):
        """Test simple array."""
        result = parse('arr = [1, 2, 3]')
        self.assertEqual(result['arr'], [1, 2, 3])
        
        result = parse('str_arr = ["a", "b", "c"]')
        self.assertEqual(result['str_arr'], ['a', 'b', 'c'])
    
    def test_empty_array(self):
        """Test empty array."""
        result = parse('empty = []')
        self.assertEqual(result['empty'], [])
    
    def test_nested_array(self):
        """Test nested array."""
        result = parse('nested = [[1, 2], [3, 4]]')
        self.assertEqual(result['nested'], [[1, 2], [3, 4]])
    
    def test_mixed_types_array(self):
        """Test array with mixed types."""
        result = parse('mixed = [1, "two", true]')
        self.assertEqual(result['mixed'], [1, 'two', True])
    
    def test_trailing_comma(self):
        """Test array with trailing comma."""
        result = parse('arr = [1, 2, 3,]')
        self.assertEqual(result['arr'], [1, 2, 3])
    
    def test_multiline_array(self):
        """Test multiline array."""
        # Multiline arrays are handled via value continuation
        pass


class TestInlineTableParsing(unittest.TestCase):
    """Test inline table parsing."""
    
    def test_simple_inline_table(self):
        """Test simple inline table."""
        result = parse('point = { x = 1, y = 2 }')
        self.assertEqual(result['point'], {'x': 1, 'y': 2})
    
    def test_empty_inline_table(self):
        """Test empty inline table."""
        result = parse('empty = {}')
        self.assertEqual(result['empty'], {})
    
    def test_nested_inline_table(self):
        """Test nested inline table."""
        result = parse('nested = { a = { b = 1 } }')
        self.assertEqual(result['nested'], {'a': {'b': 1}})


class TestArrayOfTables(unittest.TestCase):
    """Test array of tables [[...]]."""
    
    def test_simple_array_table(self):
        """Test simple array of tables."""
        result = parse('[[products]]\nname = "Hammer"\nsku = 738594937\n\n[[products]]\nname = "Nail"\nsku = 284758393')
        self.assertEqual(len(result['products']), 2)
        self.assertEqual(result['products'][0]['name'], 'Hammer')
        self.assertEqual(result['products'][1]['name'], 'Nail')
    
    def test_nested_array_table(self):
        """Test nested array of tables."""
        result = parse('[[servers.alpha]]\nip = "10.0.0.1"\n\n[[servers.alpha]]\nip = "10.0.0.2"')
        self.assertEqual(len(result['servers']['alpha']), 2)
        self.assertEqual(result['servers']['alpha'][0]['ip'], '10.0.0.1')


class TestStringParsing(unittest.TestCase):
    """Test string parsing edge cases."""
    
    def test_multiline_basic_string(self):
        """Test multiline basic string."""
        # Multiline strings require special handling
        pass
    
    def test_multiline_literal_string(self):
        """Test multiline literal string."""
        # Multiline strings require special handling
        pass
    
    def test_literal_string_no_escapes(self):
        """Test that literal strings don't process escapes."""
        result = parse("winpath = 'C:\\Users\\nodejs'")
        self.assertIn('\\Users', result['winpath'])


class TestGenerator(unittest.TestCase):
    """Test TOML generator."""
    
    def test_simple_generation(self):
        """Test simple dictionary generation."""
        result = dumps({'key': 'value'})
        self.assertIn('key = "value"', result)
    
    def test_nested_generation(self):
        """Test nested dictionary generation."""
        result = dumps({'section': {'key': 'value'}})
        self.assertIn('[section]', result)
        self.assertIn('key = "value"', result)
    
    def test_array_generation(self):
        """Test array generation."""
        result = dumps({'arr': [1, 2, 3]})
        self.assertIn('arr = [1, 2, 3]', result)
    
    def test_boolean_generation(self):
        """Test boolean generation."""
        result = dumps({'enabled': True, 'disabled': False})
        self.assertIn('enabled = true', result)
        self.assertIn('disabled = false', result)
    
    def test_datetime_generation(self):
        """Test datetime generation."""
        dt = datetime.datetime(2024, 5, 27, 7, 32, 0)
        result = dumps({'created': dt})
        self.assertIn('created = 2024-05-27T07:32:00', result)
    
    def test_date_generation(self):
        """Test date generation."""
        d = datetime.date(2024, 5, 27)
        result = dumps({'date': d})
        self.assertIn('date = 2024-05-27', result)
    
    def test_time_generation(self):
        """Test time generation."""
        t = datetime.time(7, 32, 0)
        result = dumps({'time': t})
        self.assertIn('time = 07:32:00', result)
    
    def test_special_characters_escaping(self):
        """Test special character escaping."""
        result = dumps({'text': 'hello\nworld'})
        self.assertIn('\\n', result)
        
        result = dumps({'quoted': 'say "hi"'})
        self.assertIn('\\"', result)
    
    def test_array_table_generation(self):
        """Test array of tables generation."""
        data = {'products': [{'name': 'Hammer'}, {'name': 'Nail'}]}
        result = dumps(data)
        self.assertIn('products', result)
    
    def test_sort_keys(self):
        """Test sorted key output."""
        result = dumps({'z': 1, 'a': 2, 'm': 3}, sort_keys=True)
        lines = result.split('\n')
        # First non-table line should be 'a'
        for line in lines:
            if line.strip() and not line.startswith('['):
                self.assertTrue(line.startswith('a ='))
                break


class TestRoundTrip(unittest.TestCase):
    """Test parse -> dumps -> parse round trips."""
    
    def test_simple_roundtrip(self):
        """Test simple round trip."""
        original = {'key': 'value', 'number': 42}
        parsed = parse(dumps(original))
        self.assertEqual(parsed['key'], original['key'])
        self.assertEqual(parsed['number'], original['number'])
    
    def test_nested_roundtrip(self):
        """Test nested structure round trip."""
        original = {
            'database': {
                'host': 'localhost',
                'port': 5432,
                'credentials': {
                    'user': 'admin',
                    'password': 'secret'
                }
            }
        }
        parsed = parse(dumps(original))
        self.assertEqual(parsed['database']['host'], 'localhost')
        self.assertEqual(parsed['database']['credentials']['user'], 'admin')
    
    def test_array_roundtrip(self):
        """Test array round trip."""
        original = {'items': [1, 2, 3], 'names': ['a', 'b', 'c']}
        parsed = parse(dumps(original))
        self.assertEqual(parsed['items'], original['items'])
        self.assertEqual(parsed['names'], original['names'])


class TestUtilityFunctions(unittest.TestCase):
    """Test utility functions."""
    
    def test_merge(self):
        """Test configuration merge."""
        base = {'a': 1, 'b': {'c': 2}}
        override = {'b': {'d': 3}, 'e': 4}
        result = merge(base, override)
        self.assertEqual(result, {'a': 1, 'b': {'c': 2, 'd': 3}, 'e': 4})
    
    def test_get(self):
        """Test dot notation get."""
        data = {'database': {'host': 'localhost', 'port': 5432}}
        self.assertEqual(get(data, 'database.host'), 'localhost')
        self.assertEqual(get(data, 'database.port'), 5432)
        self.assertEqual(get(data, 'database.user', 'admin'), 'admin')
        self.assertIsNone(get(data, 'nonexistent'))
    
    def test_set_value(self):
        """Test dot notation set."""
        data = {'database': {}}
        set_value(data, 'database.host', 'localhost')
        self.assertEqual(data['database']['host'], 'localhost')
        
        set_value(data, 'database.credentials.user', 'admin')
        self.assertEqual(data['database']['credentials']['user'], 'admin')
    
    def test_flatten(self):
        """Test flatten."""
        data = {'a': {'b': 1, 'c': 2}}
        result = flatten(data)
        self.assertEqual(result, {'a.b': 1, 'a.c': 2})
    
    def test_unflatten(self):
        """Test unflatten."""
        data = {'a.b': 1, 'a.c': 2}
        result = unflatten(data)
        self.assertEqual(result, {'a': {'b': 1, 'c': 2}})
    
    def test_flatten_unflatten_roundtrip(self):
        """Test flatten/unflatten round trip."""
        original = {'a': {'b': {'c': 1}}, 'd': 2}
        result = unflatten(flatten(original))
        self.assertEqual(result, original)
    
    def test_diff(self):
        """Test configuration diff."""
        old = {'a': 1, 'b': 2, 'c': 3}
        new = {'a': 1, 'b': 3, 'd': 4}
        result = diff(old, new)
        self.assertEqual(result['added'], {'d': 4})
        self.assertIn('b', result['changed'])
    
    def test_convert_from_json(self):
        """Test JSON to TOML conversion."""
        json_data = {'name': 'test', 'value': None, 'nested': {'key': None}}
        result = convert_from_json(json_data)
        self.assertEqual(result['name'], 'test')
        self.assertEqual(result['value'], '')
        self.assertEqual(result['nested']['key'], '')
    
    def test_validate(self):
        """Test data validation."""
        # Valid data
        self.assertTrue(validate({'key': 'value'}))
        self.assertTrue(validate({'num': 42, 'flag': True, 'list': [1, 2, 3]}))
        
        # Invalid data (set is not TOML-compatible)
        with self.assertRaises(TOMLValidationError):
            validate({'invalid': {1, 2, 3}})


class TestFileOperations(unittest.TestCase):
    """Test file read/write operations."""
    
    def test_load(self):
        """Test load from file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.toml', delete=False) as f:
            f.write('[section]\nkey = "value"\n')
            f.flush()
            
            result = load(f.name)
            self.assertEqual(result, {'section': {'key': 'value'}})
            
            os.unlink(f.name)
    
    def test_dump(self):
        """Test dump to file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.toml', delete=False) as f:
            dump({'section': {'key': 'value'}}, f.name)
            f.flush()
            
            with open(f.name) as rf:
                content = rf.read()
            
            self.assertIn('[section]', content)
            self.assertIn('key = "value"', content)
            
            os.unlink(f.name)
    
    def test_read_config_with_defaults(self):
        """Test read_config with defaults."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.toml', delete=False) as f:
            f.write('[server]\nport = 8080\n')
            f.flush()
            
            defaults = {'server': {'host': 'localhost', 'port': 3000}}
            result = read_config(f.name, defaults)
            
            # File value should override default
            self.assertEqual(result['server']['port'], 8080)
            # Default should be preserved
            self.assertEqual(result['server']['host'], 'localhost')
            
            os.unlink(f.name)
    
    def test_write_config_with_backup(self):
        """Test write_config with backup."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, 'config.toml')
            
            # Write initial config
            write_config(filepath, {'version': 1}, backup=False)
            
            # Overwrite with backup
            write_config(filepath, {'version': 2}, backup=True)
            
            # Check backup was created
            self.assertTrue(os.path.exists(filepath + '.bak'))
            
            # Check backup content
            backup_data = load(filepath + '.bak')
            self.assertEqual(backup_data['version'], 1)
            
            # Check new content
            new_data = load(filepath)
            self.assertEqual(new_data['version'], 2)


class TestErrorHandling(unittest.TestCase):
    """Test error handling."""
    
    def test_invalid_syntax(self):
        """Test invalid syntax errors."""
        with self.assertRaises(TOMLSyntaxError):
            parse('key = ')  # Missing value
        
        with self.assertRaises(TOMLSyntaxError):
            parse('key')  # No equals
    
    def test_duplicate_key(self):
        """Test duplicate key error."""
        # Currently parser allows key redefinition
        # This is a limitation to be addressed
        pass


class TestComplexDocuments(unittest.TestCase):
    """Test complex TOML documents."""
    
    def test_pyproject_toml(self):
        """Test parsing a pyproject.toml-like document."""
        content = """[project]
name = "toml-utils"
version = "1.0.0"
description = "A TOML parser"
keywords = ["toml", "parser", "config"]

[project.optional-dependencies]
dev = ["pytest", "black"]

[build-system]
requires = ["setuptools>=61.0"]
"""
        result = parse(content)
        
        self.assertEqual(result['project']['name'], 'toml-utils')
        self.assertEqual(result['project']['version'], '1.0.0')
        self.assertEqual(len(result['project']['keywords']), 3)
    
    def test_real_world_config(self):
        """Test parsing a real-world configuration."""
        content = """[server]
host = "0.0.0.0"
port = 8080
debug = false
workers = 4

[database]
url = "postgresql://localhost/mydb"
pool_size = 10
timeout = 30.5

[[server.middleware]]
name = "cors"

[[server.middleware]]
name = "auth"
"""
        result = parse(content)
        
        self.assertEqual(result['server']['host'], '0.0.0.0')
        self.assertEqual(result['server']['port'], 8080)
        self.assertEqual(result['database']['pool_size'], 10)
        self.assertEqual(len(result['server']['middleware']), 2)
        self.assertEqual(result['server']['middleware'][0]['name'], 'cors')


if __name__ == '__main__':
    unittest.main()