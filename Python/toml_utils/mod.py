"""
TOML Configuration File Parser and Generator
=============================================

A complete TOML 1.0.0 compatible parser and generator with zero external dependencies.
"""

import re
import datetime
from typing import Any, Dict, List, Tuple, Union


class TOMLError(Exception):
    """Base exception for TOML parsing errors."""
    pass


class TOMLSyntaxError(TOMLError):
    """Raised when TOML syntax is invalid."""
    def __init__(self, message: str, line: int = None):
        self.line = line
        if line is not None:
            message = f"Line {line}: {message}"
        super().__init__(message)


class TOMLValidationError(TOMLError):
    """Raised when TOML data fails validation."""
    pass


TOMLValue = Union[str, int, float, bool, datetime.datetime, datetime.date, datetime.time, list, dict]

# Constants for quote characters
DQUOTE = '"'
SQUOTE = "'"


class TOMLParser:
    """TOML parser implementing TOML 1.0.0 specification."""
    
    def __init__(self):
        self.lines: List[str] = []
        self.line_num: int = 0
        self.result: Dict[str, Any] = {}
        self.current_table_path: List[str] = []
    
    def parse(self, content: str) -> Dict[str, Any]:
        """Parse TOML content string into a dictionary."""
        self.lines = content.split('\n')
        self.line_num = 0
        self.result = {}
        self.current_table_path = []
        
        while self.line_num < len(self.lines):
            line = self.lines[self.line_num].strip()
            self._parse_line(line)
            self.line_num += 1
        
        return self.result
    
    def _parse_line(self, line: str):
        """Parse a single line."""
        if not line or line.startswith('#'):
            return
        
        if line.startswith('[['):
            self._parse_array_table(line)
        elif line.startswith('['):
            self._parse_table(line)
        else:
            self._parse_key_value(line)
    
    def _parse_table(self, line: str):
        """Parse table header [table.name]."""
        if not line.endswith(']'):
            raise TOMLSyntaxError(f"Invalid table header: {line}", self.line_num + 1)
        
        name = line[1:-1].strip()
        keys = self._parse_dotted_key(name)
        self.current_table_path = keys
        self._create_table(keys)
    
    def _parse_array_table(self, line: str):
        """Parse array of tables [[array.name]]."""
        if not line.endswith(']]'):
            raise TOMLSyntaxError(f"Invalid array table header: {line}", self.line_num + 1)
        
        name = line[2:-2].strip()
        keys = self._parse_dotted_key(name)
        self.current_table_path = keys
        self._create_array_table(keys)
    
    def _parse_dotted_key(self, key_str: str) -> List[str]:
        """Parse a dotted key like 'a.b.c' into ['a', 'b', 'c']."""
        keys = []
        parts = key_str.split('.')
        for part in parts:
            part = part.strip()
            if part.startswith(DQUOTE) and part.endswith(DQUOTE):
                keys.append(part[1:-1])
            elif part.startswith(SQUOTE) and part.endswith(SQUOTE):
                keys.append(part[1:-1])
            else:
                keys.append(part)
        return keys
    
    def _create_table(self, keys: List[str]):
        """Create nested table structure."""
        current = self.result
        for key in keys:
            if key not in current:
                current[key] = {}
            current = current[key]
    
    def _create_array_table(self, keys: List[str]):
        """Create array table structure."""
        current = self.result
        for key in keys[:-1]:
            if key not in current:
                current[key] = {}
            current = current[key]
        
        last_key = keys[-1]
        if last_key not in current:
            current[last_key] = []
        current[last_key].append({})
    
    def _parse_key_value(self, line: str):
        """Parse key = value line."""
        eq_pos = line.find('=')
        if eq_pos == -1:
            raise TOMLSyntaxError(f"Invalid key-value pair: {line}", self.line_num + 1)
        
        key_part = line[:eq_pos].strip()
        value_part = line[eq_pos + 1:].strip()
        
        keys = self._parse_dotted_key(key_part)
        value = self._parse_value(value_part)
        self._set_value(keys, value)
    
    def _set_value(self, keys: List[str], value: Any):
        """Set a value at the given key path."""
        if self.current_table_path:
            current = self._get_current_table()
        else:
            current = self.result
        
        for key in keys[:-1]:
            if key not in current:
                current[key] = {}
            current = current[key]
        
        current[keys[-1]] = value
    
    def _get_current_table(self) -> dict:
        """Get the current table for writing."""
        current = self.result
        for key in self.current_table_path:
            if isinstance(current.get(key), list):
                current = current[key][-1]
            else:
                current = current[key]
        return current
    
    def _parse_value(self, value_str: str) -> TOMLValue:
        """Parse a TOML value."""
        value_str = value_str.strip()
        
        # Remove trailing comment
        comment_pos = self._find_comment(value_str)
        if comment_pos != -1:
            value_str = value_str[:comment_pos].strip()
        
        if not value_str:
            raise TOMLSyntaxError("Missing value", self.line_num + 1)
        
        # Boolean
        if value_str == 'true':
            return True
        if value_str == 'false':
            return False
        
        # Special floats
        if value_str in ('inf', '+inf'):
            return float('inf')
        if value_str == '-inf':
            return float('-inf')
        if value_str in ('nan', '+nan', '-nan'):
            return float('nan')
        
        # Array
        if value_str.startswith('['):
            return self._parse_array(value_str)
        
        # Inline table
        if value_str.startswith('{'):
            return self._parse_inline_table(value_str)
        
        # Multiline basic string (triple double quotes)
        if value_str.startswith(DQUOTE * 3):
            return self._parse_multiline_basic_string(value_str)
        
        # Multiline literal string (triple single quotes)
        if value_str.startswith(SQUOTE * 3):
            return self._parse_multiline_literal_string(value_str)
        
        # Basic string
        if value_str.startswith(DQUOTE):
            return self._parse_basic_string(value_str)
        
        # Literal string
        if value_str.startswith(SQUOTE):
            return self._parse_literal_string(value_str)
        
        # Number or datetime
        return self._parse_number_or_datetime(value_str)
    
    def _find_comment(self, s: str) -> int:
        """Find the start of a comment, respecting strings."""
        in_string = False
        string_char = None
        for i, c in enumerate(s):
            if in_string:
                if c == string_char:
                    in_string = False
            else:
                if c == DQUOTE or c == SQUOTE:
                    in_string = True
                    string_char = c
                elif c == '#':
                    return i
        return -1
    
    def _parse_basic_string(self, s: str) -> str:
        """Parse a basic string."""
        if not s.startswith(DQUOTE) or len(s) < 2:
            raise TOMLSyntaxError("Invalid string", self.line_num + 1)
        
        result = []
        i = 1
        while i < len(s):
            c = s[i]
            if c == DQUOTE:
                return ''.join(result)
            elif c == '\\' and i + 1 < len(s):
                next_c = s[i + 1]
                escapes = {'b': '\b', 't': '\t', 'n': '\n', 'f': '\f', 'r': '\r', '"': '"', '\\': '\\'}
                if next_c in escapes:
                    result.append(escapes[next_c])
                    i += 2
                    continue
                elif next_c == 'u' and i + 5 < len(s):
                    hex_str = s[i+2:i+6]
                    try:
                        result.append(chr(int(hex_str, 16)))
                        i += 6
                        continue
                    except ValueError:
                        pass
                elif next_c == 'U' and i + 9 < len(s):
                    hex_str = s[i+2:i+10]
                    try:
                        result.append(chr(int(hex_str, 16)))
                        i += 10
                        continue
                    except ValueError:
                        pass
                raise TOMLSyntaxError("Invalid escape", self.line_num + 1)
            else:
                result.append(c)
            i += 1
        
        raise TOMLSyntaxError("Unterminated string", self.line_num + 1)
    
    def _parse_literal_string(self, s: str) -> str:
        """Parse a literal string."""
        if not s.startswith(SQUOTE):
            raise TOMLSyntaxError("Invalid literal string", self.line_num + 1)
        
        end_quote = s.rfind(SQUOTE)
        if end_quote <= 0:
            raise TOMLSyntaxError("Unterminated literal string", self.line_num + 1)
        
        return s[1:end_quote]
    
    def _parse_multiline_basic_string(self, s: str) -> str:
        """Parse multiline basic string."""
        marker = DQUOTE * 3
        if not s.startswith(marker):
            raise TOMLSyntaxError("Invalid multiline string", self.line_num + 1)
        
        end = s.find(marker, 3)
        if end == -1:
            raise TOMLSyntaxError("Unterminated multiline string", self.line_num + 1)
        
        content = s[3:end]
        if content.startswith('\n'):
            content = content[1:]
        elif content.startswith('\r\n'):
            content = content[2:]
        
        # Process escapes
        result = []
        i = 0
        while i < len(content):
            c = content[i]
            if c == '\\' and i + 1 < len(content):
                next_c = content[i + 1]
                escapes = {'b': '\b', 't': '\t', 'n': '\n', 'f': '\f', 'r': '\r', '"': '"', '\\': '\\'}
                if next_c in escapes:
                    result.append(escapes[next_c])
                    i += 2
                elif next_c in ' \t\n\r':
                    i += 2
                    while i < len(content) and content[i] in ' \t\r\n':
                        i += 1
                else:
                    result.append(c)
                    i += 1
            else:
                result.append(c)
                i += 1
        
        return ''.join(result)
    
    def _parse_multiline_literal_string(self, s: str) -> str:
        """Parse multiline literal string."""
        marker = SQUOTE * 3
        if not s.startswith(marker):
            raise TOMLSyntaxError("Invalid multiline literal string", self.line_num + 1)
        
        end = s.find(marker, 3)
        if end == -1:
            raise TOMLSyntaxError("Unterminated multiline literal string", self.line_num + 1)
        
        content = s[3:end]
        if content.startswith('\n'):
            content = content[1:]
        elif content.startswith('\r\n'):
            content = content[2:]
        
        return content
    
    def _parse_array(self, s: str) -> list:
        """Parse an array."""
        if not s.startswith('[') or not s.endswith(']'):
            raise TOMLSyntaxError("Invalid array", self.line_num + 1)
        
        content = s[1:-1].strip()
        if not content:
            return []
        
        items = self._split_array_items(content)
        result = []
        for item in items:
            item = item.strip()
            if item:
                result.append(self._parse_value(item))
        
        return result
    
    def _split_array_items(self, content: str) -> List[str]:
        """Split array items by comma, respecting nested structures."""
        items = []
        current = []
        depth = 0
        in_string = False
        string_char = None
        
        for c in content:
            if in_string:
                current.append(c)
                if c == string_char:
                    in_string = False
            elif c == DQUOTE or c == SQUOTE:
                in_string = True
                string_char = c
                current.append(c)
            elif c in '[{':
                depth += 1
                current.append(c)
            elif c in ']}':
                depth -= 1
                current.append(c)
            elif c == ',' and depth == 0:
                items.append(''.join(current))
                current = []
            else:
                current.append(c)
        
        if current:
            items.append(''.join(current))
        
        return items
    
    def _parse_inline_table(self, s: str) -> dict:
        """Parse an inline table."""
        if not s.startswith('{') or not s.endswith('}'):
            raise TOMLSyntaxError("Invalid inline table", self.line_num + 1)
        
        content = s[1:-1].strip()
        if not content:
            return {}
        
        items = self._split_inline_table_items(content)
        result = {}
        for item in items:
            item = item.strip()
            if item:
                eq_pos = item.find('=')
                if eq_pos == -1:
                    raise TOMLSyntaxError("Invalid inline table item", self.line_num + 1)
                
                key = item[:eq_pos].strip()
                value = item[eq_pos + 1:].strip()
                
                if key.startswith(DQUOTE) and key.endswith(DQUOTE):
                    key = key[1:-1]
                elif key.startswith(SQUOTE) and key.endswith(SQUOTE):
                    key = key[1:-1]
                
                result[key] = self._parse_value(value)
        
        return result
    
    def _split_inline_table_items(self, content: str) -> List[str]:
        """Split inline table items by comma."""
        items = []
        current = []
        depth = 0
        in_string = False
        string_char = None
        
        for c in content:
            if in_string:
                current.append(c)
                if c == string_char:
                    in_string = False
            elif c == DQUOTE or c == SQUOTE:
                in_string = True
                string_char = c
                current.append(c)
            elif c in '[{':
                depth += 1
                current.append(c)
            elif c in ']}':
                depth -= 1
                current.append(c)
            elif c == ',' and depth == 0:
                items.append(''.join(current))
                current = []
            else:
                current.append(c)
        
        if current:
            items.append(''.join(current))
        
        return items
    
    def _parse_number_or_datetime(self, s: str) -> TOMLValue:
        """Parse a number or datetime."""
        s = s.strip()
        
        # Date: YYYY-MM-DD
        date_match = re.match(r'^(\d{4})-(\d{2})-(\d{2})$', s)
        if date_match:
            return datetime.date(int(date_match.group(1)), int(date_match.group(2)), int(date_match.group(3)))
        
        # Time: HH:MM:SS or HH:MM:SS.mmm
        time_match = re.match(r'^(\d{2}):(\d{2}):(\d{2})(?:\.(\d+))?', s)
        if time_match:
            hour, minute, second = int(time_match.group(1)), int(time_match.group(2)), int(time_match.group(3))
            microsecond = 0
            if time_match.group(4):
                ms_str = time_match.group(4)
                microsecond = int(ms_str[:6].ljust(6, '0'))
            return datetime.time(hour, minute, second, microsecond)
        
        # Local datetime
        datetime_match = re.match(r'^(\d{4})-(\d{2})-(\d{2})[T ](\d{2}):(\d{2}):(\d{2})(?:\.(\d+))?', s)
        if datetime_match:
            year = int(datetime_match.group(1))
            month = int(datetime_match.group(2))
            day = int(datetime_match.group(3))
            hour = int(datetime_match.group(4))
            minute = int(datetime_match.group(5))
            second = int(datetime_match.group(6))
            microsecond = 0
            if datetime_match.group(7):
                ms_str = datetime_match.group(7)
                microsecond = int(ms_str[:6].ljust(6, '0'))
            return datetime.datetime(year, month, day, hour, minute, second, microsecond)
        
        # Offset datetime
        offset_match = re.match(r'^(\d{4})-(\d{2})-(\d{2})[T ](\d{2}):(\d{2}):(\d{2})(?:\.(\d+))?(Z|[+-]\d{2}:\d{2})$', s)
        if offset_match:
            year = int(offset_match.group(1))
            month = int(offset_match.group(2))
            day = int(offset_match.group(3))
            hour = int(offset_match.group(4))
            minute = int(offset_match.group(5))
            second = int(offset_match.group(6))
            microsecond = 0
            if offset_match.group(7):
                ms_str = offset_match.group(7)
                microsecond = int(ms_str[:6].ljust(6, '0'))
            offset_str = offset_match.group(8)
            if offset_str == 'Z':
                offset_str = '+00:00'
            from datetime import timezone, timedelta
            offset_hours = int(offset_str[1:3])
            offset_minutes = int(offset_str[4:6])
            if offset_str[0] == '-':
                tz = timezone(timedelta(hours=-offset_hours, minutes=-offset_minutes))
            else:
                tz = timezone(timedelta(hours=offset_hours, minutes=offset_minutes))
            return datetime.datetime(year, month, day, hour, minute, second, microsecond, tz)
        
        # Integer
        int_match = re.match(r'^([+-]?)(0x[0-9a-fA-F_]+|0o[0-7_]+|0b[01_]+|\d[\d_]*)$', s)
        if int_match:
            sign = int_match.group(1)
            num_str = int_match.group(2).replace('_', '')
            try:
                if num_str.startswith('0x'):
                    return int(sign + num_str, 16)
                elif num_str.startswith('0o'):
                    return int(sign + num_str, 8)
                elif num_str.startswith('0b'):
                    return int(sign + num_str, 2)
                else:
                    return int(sign + num_str)
            except ValueError:
                pass
        
        # Float
        float_match = re.match(r'^([+-]?\d[\d_]*\.?\d[\d_]*[eE][+-]?\d[\d_]*|[+-]?\d[\d_]*\.\d[\d_]*|[+-]?\.\d[\d_]+)$', s)
        if float_match:
            num_str = float_match.group(0).replace('_', '')
            try:
                return float(num_str)
            except ValueError:
                pass
        
        raise TOMLSyntaxError(f"Invalid value: {s}", self.line_num + 1)


class TOMLGenerator:
    """Generate TOML from Python dictionaries."""
    
    def __init__(self, indent: str = "  ", sort_keys: bool = False):
        self.indent = indent
        self.sort_keys = sort_keys
    
    def dumps(self, data: Dict[str, Any]) -> str:
        """Convert dictionary to TOML string."""
        lines = []
        self._generate(data, lines, [])
        return '\n'.join(lines)
    
    def _generate(self, data: Dict[str, Any], lines: List[str], prefix: List[str]):
        """Recursively generate TOML from data."""
        simple_items = []
        table_items = []
        array_table_items = []
        
        items = sorted(data.items()) if self.sort_keys else data.items()
        
        for key, value in items:
            if isinstance(value, dict):
                table_items.append((key, value))
            elif isinstance(value, list) and value and all(isinstance(v, dict) for v in value):
                array_table_items.append((key, value))
            else:
                simple_items.append((key, value))
        
        for key, value in simple_items:
            lines.append(self._format_key_value(key, value))
        
        if simple_items and (table_items or array_table_items):
            lines.append('')
        
        for key, value in table_items:
            table_path = prefix + [key]
            lines.append(f"[{'.'.join(table_path)}]")
            self._generate(value, lines, table_path)
        
        for key, value in array_table_items:
            table_path = prefix + [key]
            for item in value:
                lines.append(f"[[{'.'.join(table_path)}]]")
                self._generate(item, lines, table_path)
                lines.append('')
        
        if lines and lines[-1] == '':
            lines.pop()
    
    def _format_key_value(self, key: str, value: Any) -> str:
        """Format a key-value pair."""
        return f"{self._format_key(key)} = {self._format_value(value)}"
    
    def _format_key(self, key: str) -> str:
        """Format a key."""
        if re.match(r'^[a-zA-Z_][a-zA-Z0-9_-]*$', key):
            return key
        return f'{DQUOTE}{key}{DQUOTE}'
    
    def _format_value(self, value: Any) -> str:
        """Format a value."""
        if value is None:
            return DQUOTE * 2
        elif isinstance(value, bool):
            return 'true' if value else 'false'
        elif isinstance(value, int):
            return str(value)
        elif isinstance(value, float):
            if value != value:
                return 'nan'
            elif value == float('inf'):
                return 'inf'
            elif value == float('-inf'):
                return '-inf'
            return repr(value)
        elif isinstance(value, str):
            return self._format_string(value)
        elif isinstance(value, datetime.datetime):
            if value.tzinfo:
                return value.isoformat().replace('+00:00', 'Z')
            return value.isoformat()
        elif isinstance(value, datetime.date):
            return value.isoformat()
        elif isinstance(value, datetime.time):
            return value.isoformat()
        elif isinstance(value, list):
            return self._format_array(value)
        elif isinstance(value, dict):
            return self._format_inline_table(value)
        else:
            return self._format_string(str(value))
    
    def _format_string(self, s: str) -> str:
        """Format a string value."""
        if not s:
            return DQUOTE * 2
        
        if '\n' in s:
            if SQUOTE * 3 not in s and not any(ord(c) < 32 for c in s):
                return f'{SQUOTE * 3}{s}{SQUOTE * 3}'
            escaped = self._escape_string(s)
            return f'{DQUOTE * 3}{escaped}{DQUOTE * 3}'
        
        escaped = self._escape_string(s)
        return f'{DQUOTE}{escaped}{DQUOTE}'
    
    def _escape_string(self, s: str) -> str:
        """Escape special characters."""
        result = []
        for c in s:
            if c == DQUOTE:
                result.append('\\' + DQUOTE)
            elif c == '\\':
                result.append('\\\\')
            elif c == '\b':
                result.append('\\b')
            elif c == '\t':
                result.append('\\t')
            elif c == '\n':
                result.append('\\n')
            elif c == '\f':
                result.append('\\f')
            elif c == '\r':
                result.append('\\r')
            elif ord(c) < 32:
                result.append(f'\\u{ord(c):04x}')
            else:
                result.append(c)
        return ''.join(result)
    
    def _format_array(self, arr: list) -> str:
        """Format an array."""
        if not arr:
            return '[]'
        
        all_simple = all(not isinstance(v, (list, dict)) for v in arr)
        
        if all_simple and len(arr) <= 5:
            items = [self._format_value(v) for v in arr]
            return f"[{', '.join(items)}]"
        else:
            items = [f"  {self._format_value(v)}," for v in arr]
            return '[\n' + '\n'.join(items) + '\n]'
    
    def _format_inline_table(self, d: dict) -> str:
        """Format an inline table."""
        if not d:
            return '{}'
        
        items = [f"{self._format_key(k)} = {self._format_value(v)}" for k, v in d.items()]
        return '{ ' + ', '.join(items) + ' }'


# Public API functions

def parse(content: str) -> Dict[str, Any]:
    """Parse a TOML string into a Python dictionary."""
    parser = TOMLParser()
    return parser.parse(content)


def loads(s: str) -> Dict[str, Any]:
    """Alias for parse()."""
    return parse(s)


def load(filepath: str, encoding: str = 'utf-8') -> Dict[str, Any]:
    """Load and parse a TOML file."""
    with open(filepath, 'r', encoding=encoding) as f:
        return parse(f.read())


def dumps(data: Dict[str, Any], indent: str = "  ", sort_keys: bool = False) -> str:
    """Serialize a dictionary to a TOML string."""
    generator = TOMLGenerator(indent=indent, sort_keys=sort_keys)
    return generator.dumps(data)


def dump(data: Dict[str, Any], filepath: str, encoding: str = 'utf-8', indent: str = "  ", sort_keys: bool = False):
    """Write a dictionary to a TOML file."""
    with open(filepath, 'w', encoding=encoding) as f:
        f.write(dumps(data, indent=indent, sort_keys=sort_keys))


def validate(data: Dict[str, Any]) -> bool:
    """Validate that data can be serialized to TOML."""
    def _check(value: Any, path: str = ''):
        if isinstance(value, dict):
            for k, v in value.items():
                _check(v, f"{path}.{k}" if path else k)
        elif isinstance(value, list):
            for i, v in enumerate(value):
                _check(v, f"{path}[{i}]")
        elif not isinstance(value, (str, int, float, bool, datetime.datetime,
                                     datetime.date, datetime.time, type(None))):
            raise TOMLValidationError(f"Invalid type at {path}: {type(value).__name__}")
    
    _check(data)
    return True


def merge(*configs: Dict[str, Any]) -> Dict[str, Any]:
    """Merge multiple TOML configurations."""
    def _deep_merge(a: dict, b: dict) -> dict:
        result = a.copy()
        for key, value in b.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = _deep_merge(result[key], value)
            else:
                result[key] = value
        return result
    
    result = {}
    for config in configs:
        if config:
            result = _deep_merge(result, config)
    return result


def get(data: Dict[str, Any], path: str, default: Any = None) -> Any:
    """Get a value using dot notation path."""
    keys = path.split('.')
    current = data
    
    for key in keys:
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            return default
    
    return current


def set_value(data: Dict[str, Any], path: str, value: Any) -> Dict[str, Any]:
    """Set a value using dot notation path."""
    keys = path.split('.')
    current = data
    
    for key in keys[:-1]:
        if key not in current:
            current[key] = {}
        current = current[key]
    
    current[keys[-1]] = value
    return data


def flatten(data: Dict[str, Any], separator: str = '.') -> Dict[str, Any]:
    """Flatten nested TOML data."""
    def _flatten(d: dict, prefix: str = '') -> dict:
        result = {}
        for key, value in d.items():
            new_key = f"{prefix}{separator}{key}" if prefix else key
            if isinstance(value, dict):
                result.update(_flatten(value, new_key))
            else:
                result[new_key] = value
        return result
    
    return _flatten(data)


def unflatten(data: Dict[str, Any], separator: str = '.') -> Dict[str, Any]:
    """Unflatten dot-notation keys."""
    result = {}
    for key, value in data.items():
        keys = key.split(separator)
        current = result
        for k in keys[:-1]:
            if k not in current:
                current[k] = {}
            current = current[k]
        current[keys[-1]] = value
    return result


def diff(old: Dict[str, Any], new: Dict[str, Any]) -> Dict[str, Any]:
    """Compare two TOML configurations."""
    old_flat = flatten(old)
    new_flat = flatten(new)
    
    old_keys = set(old_flat.keys())
    new_keys = set(new_flat.keys())
    
    added = {k: new_flat[k] for k in new_keys - old_keys}
    removed = {k: old_flat[k] for k in old_keys - new_keys}
    changed = {}
    
    for k in old_keys & new_keys:
        if old_flat[k] != new_flat[k]:
            changed[k] = {'old': old_flat[k], 'new': new_flat[k]}
    
    return {'added': added, 'removed': removed, 'changed': changed}


def convert_from_json(json_data: Dict[str, Any]) -> Dict[str, Any]:
    """Convert JSON data to TOML-compatible format."""
    def _convert(value: Any) -> Any:
        if value is None:
            return ""
        elif isinstance(value, dict):
            return {k: _convert(v) for k, v in value.items()}
        elif isinstance(value, list):
            return [_convert(v) for v in value]
        else:
            return value
    
    return _convert(json_data)


def read_config(filepath: str, defaults: Dict[str, Any] = None) -> Dict[str, Any]:
    """Read a configuration file with optional defaults."""
    try:
        config = load(filepath)
    except FileNotFoundError:
        config = {}
    
    if defaults:
        return merge(defaults, config)
    return config


def write_config(filepath: str, data: Dict[str, Any], backup: bool = True):
    """Write configuration to a TOML file with optional backup."""
    import os
    
    if backup and os.path.exists(filepath):
        backup_path = f"{filepath}.bak"
        os.replace(filepath, backup_path)
    
    dump(data, filepath)