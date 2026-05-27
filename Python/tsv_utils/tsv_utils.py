"""
TSV (Tab-Separated Values) Utilities

A comprehensive, zero-dependency library for reading, writing, and manipulating 
TSV (Tab-Separated Values) files and data.

Features:
- Read TSV files into lists or dictionaries
- Write data to TSV files
- Parse TSV strings
- Convert data to TSV format
- Handle BOM (Byte Order Mark)
- Support various line endings
- Streaming support for large files
- Type inference and conversion
- Header handling
"""

import io
from typing import (
    Any,
    Callable,
    Dict,
    Generator,
    Iterable,
    List,
    Optional,
    Tuple,
    Union,
)


class TSVError(Exception):
    """Base exception for TSV utilities."""
    pass


class TSVParseError(TSVError):
    """Raised when TSV parsing fails."""
    pass


class TSVWriteError(TSVError):
    """Raised when TSV writing fails."""
    pass


def _detect_bom(content: Union[str, bytes]) -> Tuple[str, bool]:
    """
    Detect and handle BOM (Byte Order Mark).
    
    Args:
        content: Input content (string or bytes)
        
    Returns:
        Tuple of (content_without_bom, had_bom)
    """
    if isinstance(content, bytes):
        # UTF-8 BOM
        if content.startswith(b'\xef\xbb\xbf'):
            return content[3:].decode('utf-8'), True
        # UTF-16 LE BOM
        if content.startswith(b'\xff\xfe'):
            return content[2:].decode('utf-16-le'), True
        # UTF-16 BE BOM
        if content.startswith(b'\xfe\xff'):
            return content[2:].decode('utf-16-be'), True
        # Try to decode as UTF-8
        try:
            return content.decode('utf-8'), False
        except UnicodeDecodeError:
            return content.decode('latin-1'), False
    else:
        # String with UTF-8 BOM character
        if content.startswith('\ufeff'):
            return content[1:], True
        return content, False


def _normalize_line_endings(content: str) -> str:
    """
    Normalize line endings to Unix style (\\n).
    
    Args:
        content: Input string
        
    Returns:
        String with normalized line endings
    """
    # Handle Windows line endings first, then old Mac
    return content.replace('\r\n', '\n').replace('\r', '\n')


def _parse_tsv_line(
    line: str,
    delimiter: str = '\t',
    quote_char: Optional[str] = None,
    escape_char: Optional[str] = None
) -> List[str]:
    """
    Parse a single TSV line.
    
    Args:
        line: The line to parse
        delimiter: Field delimiter (default: tab)
        quote_char: Character used for quoting fields
        escape_char: Character used for escaping
        
    Returns:
        List of field values
    """
    if not line:
        return ['']
    
    fields = []
    current_field = []
    in_quotes = False
    i = 0
    
    while i < len(line):
        char = line[i]
        
        if quote_char and char == quote_char:
            if in_quotes:
                # Check for escaped quote
                if i + 1 < len(line) and line[i + 1] == quote_char:
                    current_field.append(quote_char)
                    i += 2
                    continue
                else:
                    in_quotes = False
            else:
                in_quotes = True
            i += 1
        elif escape_char and char == escape_char and i + 1 < len(line):
            # Handle escape character
            current_field.append(line[i + 1])
            i += 2
        elif char == delimiter and not in_quotes:
            fields.append(''.join(current_field))
            current_field = []
            i += 1
        else:
            current_field.append(char)
            i += 1
    
    # Add the last field
    fields.append(''.join(current_field))
    
    return fields


def _serialize_field(
    value: Any,
    delimiter: str = '\t',
    quote_char: Optional[str] = '"',
    newline: str = '\n'
) -> str:
    """
    Serialize a single field value for TSV output.
    
    Args:
        value: The value to serialize
        delimiter: Field delimiter
        quote_char: Character for quoting fields
        newline: Newline character to escape
        
    Returns:
        Serialized field string
    """
    if value is None:
        return ''
    
    str_value = str(value)
    
    # Check if quoting is needed
    needs_quoting = (
        delimiter in str_value or
        newline in str_value or
        (quote_char and quote_char in str_value)
    )
    
    if needs_quoting and quote_char:
        # Escape quote characters by doubling them
        escaped = str_value.replace(quote_char, quote_char * 2)
        return f"{quote_char}{escaped}{quote_char}"
    
    return str_value


# ==================== Reading Functions ====================

def read_tsv(
    filepath: str,
    delimiter: str = '\t',
    has_header: bool = True,
    encoding: str = 'utf-8',
    skip_empty_lines: bool = True,
    strip_whitespace: bool = True,
    type_inference: bool = False,
    quote_char: Optional[str] = None
) -> Tuple[List[str], List[List[Any]]]:
    """
    Read a TSV file and return headers and rows.
    
    Args:
        filepath: Path to the TSV file
        delimiter: Field delimiter (default: tab)
        has_header: Whether the file has a header row
        encoding: File encoding
        skip_empty_lines: Skip empty lines
        strip_whitespace: Strip whitespace from fields
        type_inference: Attempt to infer and convert types
        quote_char: Character used for quoting fields
        
    Returns:
        Tuple of (headers, rows)
        
    Raises:
        TSVParseError: If parsing fails
        FileNotFoundError: If file doesn't exist
    """
    try:
        with open(filepath, 'rb') as f:
            content = f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {filepath}")
    except Exception as e:
        raise TSVParseError(f"Error reading file: {e}")
    
    # Handle BOM and decode
    content_str, _ = _detect_bom(content)
    content_str = _normalize_line_endings(content_str)
    
    lines = content_str.split('\n')
    
    # Remove trailing empty line if present
    if lines and lines[-1] == '':
        lines = lines[:-1]
    
    # Filter empty lines if requested
    if skip_empty_lines:
        lines = [line for line in lines if line.strip()]
    
    if not lines:
        return [], []
    
    # Parse first line for headers
    if has_header:
        headers = _parse_tsv_line(lines[0], delimiter, quote_char)
        if strip_whitespace:
            headers = [h.strip() for h in headers]
        data_lines = lines[1:]
    else:
        headers = []
        data_lines = lines
    
    # Parse data rows
    rows = []
    for i, line in enumerate(data_lines):
        try:
            fields = _parse_tsv_line(line, delimiter, quote_char)
            
            if strip_whitespace:
                fields = [f.strip() for f in fields]
            
            if type_inference:
                fields = [_infer_type(f) for f in fields]
            
            rows.append(fields)
        except Exception as e:
            raise TSVParseError(f"Error parsing line {i + 2}: {e}")
    
    return headers, rows


def read_tsv_as_dicts(
    filepath: str,
    delimiter: str = '\t',
    encoding: str = 'utf-8',
    skip_empty_lines: bool = True,
    strip_whitespace: bool = True,
    type_inference: bool = False,
    quote_char: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Read a TSV file and return a list of dictionaries.
    
    Args:
        filepath: Path to the TSV file
        delimiter: Field delimiter (default: tab)
        encoding: File encoding
        skip_empty_lines: Skip empty lines
        strip_whitespace: Strip whitespace from fields
        type_inference: Attempt to infer and convert types
        quote_char: Character used for quoting fields
        
    Returns:
        List of dictionaries, one per row
        
    Raises:
        TSVParseError: If parsing fails or file has no header
    """
    headers, rows = read_tsv(
        filepath,
        delimiter=delimiter,
        has_header=True,
        encoding=encoding,
        skip_empty_lines=skip_empty_lines,
        strip_whitespace=strip_whitespace,
        type_inference=type_inference,
        quote_char=quote_char
    )
    
    if not headers:
        raise TSVParseError("TSV file must have a header row for dict conversion")
    
    result = []
    for row in rows:
        # Handle rows with fewer fields than headers
        row_dict = {}
        for i, header in enumerate(headers):
            if i < len(row):
                row_dict[header] = row[i]
            else:
                row_dict[header] = None
        result.append(row_dict)
    
    return result


def read_tsv_streaming(
    filepath: str,
    delimiter: str = '\t',
    has_header: bool = True,
    encoding: str = 'utf-8',
    skip_empty_lines: bool = True,
    strip_whitespace: bool = True,
    chunk_size: int = 1000
) -> Generator[Tuple[List[str], List[List[Any]]], None, None]:
    """
    Stream read a TSV file in chunks for large files.
    
    Args:
        filepath: Path to the TSV file
        delimiter: Field delimiter
        has_header: Whether the file has a header row
        encoding: File encoding
        skip_empty_lines: Skip empty lines
        strip_whitespace: Strip whitespace from fields
        chunk_size: Number of rows per chunk
        
    Yields:
        Tuple of (headers, chunk_rows) for each chunk
    """
    with open(filepath, 'r', encoding=encoding) as f:
        headers = []
        
        if has_header:
            header_line = f.readline()
            if header_line:
                headers = _parse_tsv_line(
                    _normalize_line_endings(header_line).rstrip('\n'),
                    delimiter
                )
                if strip_whitespace:
                    headers = [h.strip() for h in headers]
        
        chunk = []
        for line in f:
            line = _normalize_line_endings(line).rstrip('\n')
            
            if skip_empty_lines and not line.strip():
                continue
            
            fields = _parse_tsv_line(line, delimiter)
            
            if strip_whitespace:
                fields = [f.strip() for f in fields]
            
            chunk.append(fields)
            
            if len(chunk) >= chunk_size:
                yield headers, chunk
                chunk = []
        
        if chunk:
            yield headers, chunk


def parse_tsv_string(
    content: str,
    delimiter: str = '\t',
    has_header: bool = True,
    skip_empty_lines: bool = True,
    strip_whitespace: bool = True,
    quote_char: Optional[str] = None
) -> Tuple[List[str], List[List[str]]]:
    """
    Parse a TSV string.
    
    Args:
        content: TSV string content
        delimiter: Field delimiter
        has_header: Whether content has a header row
        skip_empty_lines: Skip empty lines
        strip_whitespace: Strip whitespace from fields
        quote_char: Character used for quoting fields
        
    Returns:
        Tuple of (headers, rows)
    """
    content, _ = _detect_bom(content)
    content = _normalize_line_endings(content)
    
    lines = content.split('\n')
    
    if lines and lines[-1] == '':
        lines = lines[:-1]
    
    if skip_empty_lines:
        lines = [line for line in lines if line.strip()]
    
    if not lines:
        return [], []
    
    if has_header:
        headers = _parse_tsv_line(lines[0], delimiter, quote_char)
        if strip_whitespace:
            headers = [h.strip() for h in headers]
        data_lines = lines[1:]
    else:
        headers = []
        data_lines = lines
    
    rows = []
    for line in data_lines:
        fields = _parse_tsv_line(line, delimiter, quote_char)
        if strip_whitespace:
            fields = [f.strip() for f in fields]
        rows.append(fields)
    
    return headers, rows


# ==================== Writing Functions ====================

def write_tsv(
    filepath: str,
    headers: Optional[List[str]] = None,
    rows: Optional[List[List[Any]]] = None,
    delimiter: str = '\t',
    encoding: str = 'utf-8',
    newline: str = '\n',
    quote_char: Optional[str] = '"',
    include_bom: bool = False
) -> int:
    """
    Write data to a TSV file.
    
    Args:
        filepath: Output file path
        headers: Optional header row
        rows: Data rows
        delimiter: Field delimiter
        encoding: File encoding
        newline: Newline character
        quote_char: Character for quoting fields
        include_bom: Whether to include UTF-8 BOM
        
    Returns:
        Number of rows written (including header)
        
    Raises:
        TSVWriteError: If writing fails
    """
    if rows is None:
        rows = []
    
    try:
        with open(filepath, 'w', encoding=encoding, newline='') as f:
            if include_bom:
                f.write('\ufeff')
            
            row_count = 0
            
            # Write header
            if headers:
                header_line = delimiter.join(
                    _serialize_field(h, delimiter, quote_char, newline)
                    for h in headers
                )
                f.write(header_line + newline)
                row_count += 1
            
            # Write data rows
            for row in rows:
                row_line = delimiter.join(
                    _serialize_field(field, delimiter, quote_char, newline)
                    for field in row
                )
                f.write(row_line + newline)
                row_count += 1
            
            return row_count
    except Exception as e:
        raise TSVWriteError(f"Error writing TSV file: {e}")


def write_tsv_from_dicts(
    filepath: str,
    data: List[Dict[str, Any]],
    fieldnames: Optional[List[str]] = None,
    delimiter: str = '\t',
    encoding: str = 'utf-8',
    newline: str = '\n',
    quote_char: Optional[str] = '"',
    include_bom: bool = False,
    include_header: bool = True
) -> int:
    """
    Write a list of dictionaries to a TSV file.
    
    Args:
        filepath: Output file path
        data: List of dictionaries
        fieldnames: Optional field order (uses first dict keys if not provided)
        delimiter: Field delimiter
        encoding: File encoding
        newline: Newline character
        quote_char: Character for quoting fields
        include_bom: Whether to include UTF-8 BOM
        include_header: Whether to include header row
        
    Returns:
        Number of rows written
    """
    if not data:
        return write_tsv(
            filepath,
            headers=fieldnames if include_header else None,
            rows=[],
            delimiter=delimiter,
            encoding=encoding,
            newline=newline,
            quote_char=quote_char,
            include_bom=include_bom
        )
    
    # Determine fieldnames
    if fieldnames is None:
        fieldnames = list(data[0].keys())
    
    # Convert dicts to rows
    rows = []
    for item in data:
        row = [item.get(field) for field in fieldnames]
        rows.append(row)
    
    headers = fieldnames if include_header else None
    
    return write_tsv(
        filepath,
        headers=headers,
        rows=rows,
        delimiter=delimiter,
        encoding=encoding,
        newline=newline,
        quote_char=quote_char,
        include_bom=include_bom
    )


def to_tsv_string(
    headers: Optional[List[str]] = None,
    rows: Optional[List[List[Any]]] = None,
    delimiter: str = '\t',
    newline: str = '\n',
    quote_char: Optional[str] = '"'
) -> str:
    """
    Convert data to a TSV string.
    
    Args:
        headers: Optional header row
        rows: Data rows
        delimiter: Field delimiter
        newline: Newline character
        quote_char: Character for quoting fields
        
    Returns:
        TSV formatted string
    """
    if rows is None:
        rows = []
    
    lines = []
    
    if headers:
        header_line = delimiter.join(
            _serialize_field(h, delimiter, quote_char, newline)
            for h in headers
        )
        lines.append(header_line)
    
    for row in rows:
        row_line = delimiter.join(
            _serialize_field(field, delimiter, quote_char, newline)
            for field in row
        )
        lines.append(row_line)
    
    return newline.join(lines)


def dicts_to_tsv_string(
    data: List[Dict[str, Any]],
    fieldnames: Optional[List[str]] = None,
    delimiter: str = '\t',
    newline: str = '\n',
    quote_char: Optional[str] = '"',
    include_header: bool = True
) -> str:
    """
    Convert a list of dictionaries to a TSV string.
    
    Args:
        data: List of dictionaries
        fieldnames: Optional field order
        delimiter: Field delimiter
        newline: Newline character
        quote_char: Character for quoting fields
        include_header: Whether to include header row
        
    Returns:
        TSV formatted string
    """
    if not data:
        return ''
    
    if fieldnames is None:
        fieldnames = list(data[0].keys())
    
    rows = [[item.get(field) for field in fieldnames] for item in data]
    headers = fieldnames if include_header else None
    
    return to_tsv_string(
        headers=headers,
        rows=rows,
        delimiter=delimiter,
        newline=newline,
        quote_char=quote_char
    )


# ==================== Utility Functions ====================

def _infer_type(value: str) -> Any:
    """
    Infer and convert a string value to its appropriate type.
    
    Args:
        value: String value to convert
        
    Returns:
        Converted value (int, float, bool, None, or original string)
    """
    if not value:
        return None
    
    # Check for None/null
    if value.lower() in ('null', 'none', 'nil', '~'):
        return None
    
    # Check for boolean
    if value.lower() in ('true', 'yes', 'on', '1'):
        return True
    if value.lower() in ('false', 'no', 'off', '0'):
        return False
    
    # Try integer
    try:
        if '.' not in value and 'e' not in value.lower():
            return int(value)
    except ValueError:
        pass
    
    # Try float
    try:
        return float(value)
    except ValueError:
        pass
    
    return value


def validate_tsv(
    filepath: str,
    delimiter: str = '\t',
    encoding: str = 'utf-8'
) -> Tuple[bool, List[str]]:
    """
    Validate a TSV file for common issues.
    
    Args:
        filepath: Path to the TSV file
        delimiter: Field delimiter
        encoding: File encoding
        
    Returns:
        Tuple of (is_valid, list_of_issues)
    """
    issues = []
    
    try:
        with open(filepath, 'r', encoding=encoding) as f:
            lines = f.readlines()
    except Exception as e:
        return False, [f"Cannot read file: {e}"]
    
    if not lines:
        return False, ["File is empty"]
    
    # Normalize line endings
    lines = [_normalize_line_endings(line) for line in lines]
    
    # Count fields in each line
    field_counts = set()
    for i, line in enumerate(lines):
        if line.strip():
            fields = _parse_tsv_line(line.rstrip('\n'), delimiter)
            field_counts.add(len(fields))
    
    # Check for consistent field counts
    if len(field_counts) > 1:
        issues.append(f"Inconsistent field counts: {sorted(field_counts)}")
    
    # Check for potential issues
    for i, line in enumerate(lines):
        line = line.rstrip('\n')
        
        # Check for raw newlines in fields
        if delimiter == '\t' and '\n' in line:
            issues.append(f"Line {i + 1}: Contains newline in field")
    
    return len(issues) == 0, issues


def get_tsv_info(
    filepath: str,
    delimiter: str = '\t',
    encoding: str = 'utf-8'
) -> Dict[str, Any]:
    """
    Get information about a TSV file.
    
    Args:
        filepath: Path to the TSV file
        delimiter: Field delimiter
        encoding: File encoding
        
    Returns:
        Dictionary with file information
    """
    headers, rows = read_tsv(filepath, delimiter=delimiter, encoding=encoding)
    
    info = {
        'filepath': filepath,
        'row_count': len(rows),
        'column_count': len(headers) if headers else (len(rows[0]) if rows else 0),
        'headers': headers,
        'has_header': bool(headers),
        'file_size_bytes': 0,
        'delimiter': delimiter,
    }
    
    try:
        import os
        info['file_size_bytes'] = os.path.getsize(filepath)
    except Exception:
        pass
    
    return info


def merge_tsv_files(
    output_filepath: str,
    input_filepaths: List[str],
    delimiter: str = '\t',
    encoding: str = 'utf-8',
    has_header: bool = True,
    keep_all_headers: bool = False
) -> int:
    """
    Merge multiple TSV files into one.
    
    Args:
        output_filepath: Output file path
        input_filepaths: List of input file paths
        delimiter: Field delimiter
        encoding: File encoding
        has_header: Whether files have headers
        keep_all_headers: Keep headers from all files (not just first)
        
    Returns:
        Total number of rows written
    """
    if not input_filepaths:
        return 0
    
    all_rows = []
    headers = None
    
    for filepath in input_filepaths:
        file_headers, file_rows = read_tsv(
            filepath,
            delimiter=delimiter,
            has_header=has_header,
            encoding=encoding
        )
        
        if headers is None:
            headers = file_headers
        
        if keep_all_headers or not has_header:
            all_rows.extend(file_rows)
        else:
            all_rows.extend(file_rows)
    
    return write_tsv(
        output_filepath,
        headers=headers,
        rows=all_rows,
        delimiter=delimiter,
        encoding=encoding
    )


if __name__ == '__main__':
    # Demo usage
    print("TSV Utils Demo")
    print("=" * 50)
    
    # Create sample data
    headers = ['Name', 'Age', 'City', 'Score']
    rows = [
        ['Alice', '30', 'New York', '95.5'],
        ['Bob', '25', 'London', '87.3'],
        ['Charlie', '35', 'Paris', '92.1'],
        ['Diana', '28', 'Tokyo', '88.9'],
    ]
    
    # Convert to TSV string
    print("\n1. To TSV String:")
    tsv_string = to_tsv_string(headers, rows)
    print(tsv_string)
    
    # Parse TSV string
    print("\n2. Parse TSV String:")
    parsed_headers, parsed_rows = parse_tsv_string(tsv_string)
    print(f"Headers: {parsed_headers}")
    print(f"Rows: {parsed_rows}")
    
    # Dict conversion
    print("\n3. Dict conversion:")
    data = [
        {'name': 'Eve', 'age': 29, 'city': 'Berlin'},
        {'name': 'Frank', 'age': 32, 'city': 'Sydney'},
    ]
    dict_tsv = dicts_to_tsv_string(data)
    print(dict_tsv)
    
    # File operations demo
    print("\n4. File operations:")
    import tempfile
    import os
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Write TSV file
        filepath = os.path.join(tmpdir, 'test.tsv')
        rows_written = write_tsv(filepath, headers, rows)
        print(f"Wrote {rows_written} rows to {filepath}")
        
        # Read TSV file
        read_headers, read_rows = read_tsv(filepath)
        print(f"Read headers: {read_headers}")
        print(f"Read {len(read_rows)} rows")
        
        # Read as dicts
        dicts = read_tsv_as_dicts(filepath)
        print(f"First dict: {dicts[0]}")
        
        # Get file info
        info = get_tsv_info(filepath)
        print(f"File info: {info}")
        
        # Validate
        is_valid, issues = validate_tsv(filepath)
        print(f"Valid: {is_valid}, Issues: {issues}")
    
    print("\n" + "=" * 50)
    print("TSV Utils Demo Complete")