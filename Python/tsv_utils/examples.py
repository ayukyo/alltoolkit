"""
TSV Utilities - Usage Examples

This file demonstrates various use cases for the TSV utilities module.
"""

import os
import tempfile

from tsv_utils import (
    read_tsv,
    read_tsv_as_dicts,
    read_tsv_streaming,
    parse_tsv_string,
    write_tsv,
    write_tsv_from_dicts,
    to_tsv_string,
    dicts_to_tsv_string,
    validate_tsv,
    get_tsv_info,
    merge_tsv_files,
)


def example_basic_read_write():
    """Basic TSV file reading and writing."""
    print("=" * 60)
    print("Example 1: Basic TSV File Reading and Writing")
    print("=" * 60)
    
    # Create sample data
    headers = ['ID', 'Name', 'Email', 'Department']
    rows = [
        ['1', 'Alice Johnson', 'alice@example.com', 'Engineering'],
        ['2', 'Bob Smith', 'bob@example.com', 'Marketing'],
        ['3', 'Charlie Brown', 'charlie@example.com', 'Sales'],
    ]
    
    with tempfile.TemporaryDirectory() as tmpdir:
        filepath = os.path.join(tmpdir, 'employees.tsv')
        
        # Write TSV file
        print(f"\nWriting TSV file: {filepath}")
        rows_written = write_tsv(filepath, headers, rows)
        print(f"Wrote {rows_written} rows (including header)")
        
        # Read TSV file
        print("\nReading TSV file:")
        read_headers, read_rows = read_tsv(filepath)
        print(f"Headers: {read_headers}")
        print("Rows:")
        for row in read_rows:
            print(f"  {row}")


def example_dict_operations():
    """Working with dictionaries."""
    print("\n" + "=" * 60)
    print("Example 2: Dictionary Operations")
    print("=" * 60)
    
    # Create sample data
    employees = [
        {'id': 1, 'name': 'Alice', 'department': 'Engineering', 'salary': 95000},
        {'id': 2, 'name': 'Bob', 'department': 'Marketing', 'salary': 85000},
        {'id': 3, 'name': 'Charlie', 'department': 'Sales', 'salary': 75000},
    ]
    
    # Convert to TSV string
    print("\nConverting dictionaries to TSV string:")
    tsv_string = dicts_to_tsv_string(employees)
    print(tsv_string)
    
    # Write to file
    with tempfile.TemporaryDirectory() as tmpdir:
        filepath = os.path.join(tmpdir, 'employees.tsv')
        
        write_tsv_from_dicts(filepath, employees)
        print(f"\nWrote to file: {filepath}")
        
        # Read back as dictionaries
        print("\nReading back as dictionaries:")
        read_data = read_tsv_as_dicts(filepath)
        for emp in read_data:
            print(f"  {emp}")


def example_string_parsing():
    """Parsing TSV strings."""
    print("\n" + "=" * 60)
    print("Example 3: String Parsing")
    print("=" * 60)
    
    # Parse a TSV string
    tsv_data = """Product\tPrice\tStock\tCategory
Laptop\t999.99\t50\tElectronics
Mouse\t29.99\t200\tElectronics
Desk\t349.00\t15\tFurniture
Chair\t199.50\t30\tFurniture"""
    
    print("\nParsing TSV string:")
    print(tsv_data)
    print()
    
    headers, rows = parse_tsv_string(tsv_data)
    print(f"Parsed headers: {headers}")
    print(f"Parsed {len(rows)} rows:")
    for row in rows:
        print(f"  {row}")
    
    # Convert back to TSV with modifications
    print("\nModifying and converting back:")
    modified_rows = []
    for row in rows:
        # Add 10% markup to price
        price = float(row[1])
        new_price = price * 1.10
        modified_rows.append([row[0], f"{new_price:.2f}", row[2], row[3]])
    
    new_tsv = to_tsv_string(headers, modified_rows)
    print(new_tsv)


def example_streaming_large_files():
    """Streaming large TSV files."""
    print("\n" + "=" * 60)
    print("Example 4: Streaming Large Files")
    print("=" * 60)
    
    # Create a large file
    with tempfile.TemporaryDirectory() as tmpdir:
        filepath = os.path.join(tmpdir, 'large.tsv')
        
        # Generate sample data
        print("\nGenerating large TSV file with 10,000 rows...")
        headers = ['id', 'name', 'value', 'timestamp']
        rows = []
        for i in range(10000):
            rows.append([
                str(i + 1),
                f'Item_{i + 1}',
                f'{(i + 1) * 1.5:.2f}',
                f'2026-01-{(i % 28) + 1:02d}'
            ])
        
        write_tsv(filepath, headers, rows)
        
        # Get file info
        info = get_tsv_info(filepath)
        print(f"\nFile info:")
        print(f"  Rows: {info['row_count']}")
        print(f"  Columns: {info['column_count']}")
        print(f"  Headers: {info['headers']}")
        print(f"  Size: {info['file_size_bytes']} bytes")
        
        # Stream read with chunks
        print("\nStreaming in chunks of 3000 rows:")
        chunk_num = 0
        total_rows = 0
        
        for chunk_headers, chunk_rows in read_tsv_streaming(filepath, chunk_size=3000):
            chunk_num += 1
            total_rows += len(chunk_rows)
            print(f"  Chunk {chunk_num}: {len(chunk_rows)} rows")
        
        print(f"\nTotal rows streamed: {total_rows}")


def example_type_inference():
    """Type inference when reading TSV."""
    print("\n" + "=" * 60)
    print("Example 5: Type Inference")
    print("=" * 60)
    
    tsv_data = """name\tage\tscore\tactive\tjoined
Alice\t30\t95.5\ttrue\t2020
Bob\t25\t87.3\tfalse\t2021
Charlie\t35\t92.1\ttrue\t2019"""
    
    with tempfile.TemporaryDirectory() as tmpdir:
        filepath = os.path.join(tmpdir, 'data.tsv')
        with open(filepath, 'w') as f:
            f.write(tsv_data)
        
        # Read without type inference
        print("\nWithout type inference:")
        headers, rows = read_tsv(filepath)
        for row in rows:
            print(f"  {row} (types: {[type(v).__name__ for v in row]})")
        
        # Read with type inference
        print("\nWith type inference:")
        headers, rows = read_tsv(filepath, type_inference=True)
        for row in rows:
            print(f"  {row} (types: {[type(v).__name__ for v in row]})")


def example_validation():
    """TSV validation."""
    print("\n" + "=" * 60)
    print("Example 6: TSV Validation")
    print("=" * 60)
    
    # Valid TSV
    valid_tsv = "name\tage\nAlice\t30\nBob\t25"
    
    # Invalid TSV (inconsistent columns)
    invalid_tsv = "name\tage\nAlice\t30\nBob"
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Test valid file
        valid_path = os.path.join(tmpdir, 'valid.tsv')
        with open(valid_path, 'w') as f:
            f.write(valid_tsv)
        
        is_valid, issues = validate_tsv(valid_path)
        print(f"\nValid file check:")
        print(f"  Is valid: {is_valid}")
        print(f"  Issues: {issues}")
        
        # Test invalid file
        invalid_path = os.path.join(tmpdir, 'invalid.tsv')
        with open(invalid_path, 'w') as f:
            f.write(invalid_tsv)
        
        is_valid, issues = validate_tsv(invalid_path)
        print(f"\nInvalid file check:")
        print(f"  Is valid: {is_valid}")
        print(f"  Issues: {issues}")


def example_merge_files():
    """Merging multiple TSV files."""
    print("\n" + "=" * 60)
    print("Example 7: Merging TSV Files")
    print("=" * 60)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create multiple files
        file1 = os.path.join(tmpdir, 'part1.tsv')
        file2 = os.path.join(tmpdir, 'part2.tsv')
        file3 = os.path.join(tmpdir, 'part3.tsv')
        output = os.path.join(tmpdir, 'merged.tsv')
        
        data1 = "name\tage\nAlice\t30\nBob\t25"
        data2 = "name\tage\nCharlie\t35\nDiana\t28"
        data3 = "name\tage\nEve\t22\nFrank\t40"
        
        with open(file1, 'w') as f:
            f.write(data1)
        with open(file2, 'w') as f:
            f.write(data2)
        with open(file3, 'w') as f:
            f.write(data3)
        
        print("\nMerging 3 TSV files...")
        
        # Merge files
        rows_written = merge_tsv_files(output, [file1, file2, file3])
        print(f"Wrote {rows_written} rows to merged file")
        
        # Read merged file
        headers, rows = read_tsv(output)
        print(f"\nMerged content:")
        print(f"Headers: {headers}")
        print("All rows:")
        for row in rows:
            print(f"  {row}")


def example_custom_delimiter():
    """Using custom delimiters."""
    print("\n" + "=" * 60)
    print("Example 8: Custom Delimiters (CSV-style)")
    print("=" * 60)
    
    # Note: While designed for TSV, the module supports other delimiters
    csv_data = "name,age,city\nAlice,30,NYC\nBob,25,LA\nCharlie,35,SF"
    
    print("\nParsing CSV with comma delimiter:")
    headers, rows = parse_tsv_string(csv_data, delimiter=',')
    print(f"Headers: {headers}")
    for row in rows:
        print(f"  {row}")
    
    # Output with custom delimiter
    print("\nOutput with pipe delimiter:")
    pipe_tsv = to_tsv_string(headers, rows, delimiter='|')
    print(pipe_tsv)


def example_special_characters():
    """Handling special characters."""
    print("\n" + "=" * 60)
    print("Example 9: Special Characters")
    print("=" * 60)
    
    headers = ['name', 'description', 'notes']
    rows = [
        ['Product A', 'Line 1\nLine 2', 'Has "quotes" inside'],
        ['Product B', 'Tab\there', 'Normal text'],
        ['Product C', 'Multiple\nNewlines\nHere', ''],
    ]
    
    print("\nData with special characters:")
    for row in rows:
        print(f"  {row}")
    
    # Convert to TSV
    tsv_string = to_tsv_string(headers, rows)
    print("\nTSV output (quoted fields):")
    print(tsv_string)
    
    # Parse back
    print("\nParsed back:")
    parsed_headers, parsed_rows = parse_tsv_string(tsv_string)
    for row in parsed_rows:
        print(f"  {row}")


def example_unicode():
    """Unicode and internationalization support."""
    print("\n" + "=" * 60)
    print("Example 10: Unicode Support")
    print("=" * 60)
    
    headers = ['language', 'hello', 'goodbye']
    rows = [
        ['English', 'Hello', 'Goodbye'],
        ['日本語', 'こんにちは', 'さようなら'],
        ['中文', '你好', '再见'],
        ['العربية', 'مرحبا', 'مع السلامة'],
        ['한국어', '안녕하세요', '안녕히 가세요'],
        ['עברית', 'שלום', 'להתראות'],
        ['Español', '¡Hola!', '¡Adiós!'],
        ['Français', 'Bonjour', 'Au revoir'],
        ['Русский', 'Привет', 'До свидания'],
    ]
    
    print("\nMultilingual greeting data:")
    tsv_string = to_tsv_string(headers, rows)
    print(tsv_string)
    
    # Parse back
    parsed_headers, parsed_rows = parse_tsv_string(tsv_string)
    print(f"\nSuccessfully parsed {len(parsed_rows)} rows with Unicode content")


def main():
    """Run all examples."""
    print("\n" + "#" * 60)
    print("# TSV Utilities - Complete Examples")
    print("#" * 60)
    
    example_basic_read_write()
    example_dict_operations()
    example_string_parsing()
    example_streaming_large_files()
    example_type_inference()
    example_validation()
    example_merge_files()
    example_custom_delimiter()
    example_special_characters()
    example_unicode()
    
    print("\n" + "=" * 60)
    print("All examples completed successfully!")
    print("=" * 60)


if __name__ == '__main__':
    main()