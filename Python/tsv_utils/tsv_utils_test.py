"""
Test Suite for TSV Utilities

Comprehensive tests for all TSV utility functions.
"""

import os
import tempfile
import unittest

from tsv_utils import (
    TSVError,
    TSVParseError,
    TSVWriteError,
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
    _detect_bom,
    _normalize_line_endings,
    _parse_tsv_line,
    _serialize_field,
    _infer_type,
)


class TestHelperFunctions(unittest.TestCase):
    """Test helper functions."""
    
    def test_detect_bom_no_bom(self):
        """Test BOM detection with no BOM."""
        content = "hello world"
        result, had_bom = _detect_bom(content)
        self.assertEqual(result, "hello world")
        self.assertFalse(had_bom)
    
    def test_detect_bom_utf8_string(self):
        """Test BOM detection with UTF-8 BOM string."""
        content = "\ufeffhello world"
        result, had_bom = _detect_bom(content)
        self.assertEqual(result, "hello world")
        self.assertTrue(had_bom)
    
    def test_detect_bom_utf8_bytes(self):
        """Test BOM detection with UTF-8 BOM bytes."""
        content = b'\xef\xbb\xbfhello world'
        result, had_bom = _detect_bom(content)
        self.assertEqual(result, "hello world")
        self.assertTrue(had_bom)
    
    def test_normalize_line_endings_unix(self):
        """Test normalizing Unix line endings."""
        content = "line1\nline2\nline3"
        result = _normalize_line_endings(content)
        self.assertEqual(result, "line1\nline2\nline3")
    
    def test_normalize_line_endings_windows(self):
        """Test normalizing Windows line endings."""
        content = "line1\r\nline2\r\nline3"
        result = _normalize_line_endings(content)
        self.assertEqual(result, "line1\nline2\nline3")
    
    def test_normalize_line_endings_mac(self):
        """Test normalizing old Mac line endings."""
        content = "line1\rline2\rline3"
        result = _normalize_line_endings(content)
        self.assertEqual(result, "line1\nline2\nline3")
    
    def test_parse_tsv_line_simple(self):
        """Test parsing simple TSV line."""
        line = "a\tb\tc"
        result = _parse_tsv_line(line)
        self.assertEqual(result, ['a', 'b', 'c'])
    
    def test_parse_tsv_line_empty(self):
        """Test parsing empty TSV line."""
        result = _parse_tsv_line('')
        self.assertEqual(result, [''])
    
    def test_parse_tsv_line_with_quotes(self):
        """Test parsing TSV line with quoted fields."""
        line = 'a\t"b with tab\tinside"\tc'
        result = _parse_tsv_line(line, quote_char='"')
        self.assertEqual(result, ['a', 'b with tab\tinside', 'c'])
    
    def test_parse_tsv_line_escaped_quotes(self):
        """Test parsing TSV line with escaped quotes."""
        line = 'a\t"b with ""quotes"""\tc'
        result = _parse_tsv_line(line, quote_char='"')
        self.assertEqual(result, ['a', 'b with "quotes"', 'c'])
    
    def test_serialize_field_simple(self):
        """Test serializing simple field."""
        result = _serialize_field('hello')
        self.assertEqual(result, 'hello')
    
    def test_serialize_field_none(self):
        """Test serializing None field."""
        result = _serialize_field(None)
        self.assertEqual(result, '')
    
    def test_serialize_field_with_tab(self):
        """Test serializing field with tab."""
        result = _serialize_field('hello\tworld', quote_char='"')
        self.assertEqual(result, '"hello\tworld"')
    
    def test_serialize_field_with_newline(self):
        """Test serializing field with newline."""
        result = _serialize_field('hello\nworld', quote_char='"')
        self.assertEqual(result, '"hello\nworld"')
    
    def test_serialize_field_with_quotes(self):
        """Test serializing field with quotes."""
        result = _serialize_field('say "hi"', quote_char='"')
        self.assertEqual(result, '"say ""hi"""')
    
    def test_infer_type_int(self):
        """Test type inference for integer."""
        self.assertEqual(_infer_type('42'), 42)
        self.assertEqual(_infer_type('-42'), -42)
    
    def test_infer_type_float(self):
        """Test type inference for float."""
        self.assertEqual(_infer_type('3.14'), 3.14)
        self.assertEqual(_infer_type('-2.5e10'), -2.5e10)
    
    def test_infer_type_bool(self):
        """Test type inference for boolean."""
        self.assertIs(_infer_type('true'), True)
        self.assertIs(_infer_type('false'), False)
        self.assertIs(_infer_type('yes'), True)
        self.assertIs(_infer_type('no'), False)
    
    def test_infer_type_none(self):
        """Test type inference for None."""
        self.assertIsNone(_infer_type(''))
        self.assertIsNone(_infer_type('null'))
        self.assertIsNone(_infer_type('none'))
    
    def test_infer_type_string(self):
        """Test type inference for string."""
        self.assertEqual(_infer_type('hello'), 'hello')
        self.assertEqual(_infer_type('abc123'), 'abc123')


class TestParseTSVString(unittest.TestCase):
    """Test TSV string parsing."""
    
    def test_parse_simple(self):
        """Test parsing simple TSV."""
        content = "name\tage\nAlice\t30\nBob\t25"
        headers, rows = parse_tsv_string(content)
        self.assertEqual(headers, ['name', 'age'])
        self.assertEqual(rows, [['Alice', '30'], ['Bob', '25']])
    
    def test_parse_no_header(self):
        """Test parsing TSV without header."""
        content = "Alice\t30\nBob\t25"
        headers, rows = parse_tsv_string(content, has_header=False)
        self.assertEqual(headers, [])
        self.assertEqual(rows, [['Alice', '30'], ['Bob', '25']])
    
    def test_parse_empty(self):
        """Test parsing empty TSV."""
        headers, rows = parse_tsv_string('')
        self.assertEqual(headers, [])
        self.assertEqual(rows, [])
    
    def test_parse_single_column(self):
        """Test parsing single column TSV."""
        content = "name\nAlice\nBob"
        headers, rows = parse_tsv_string(content)
        self.assertEqual(headers, ['name'])
        self.assertEqual(rows, [['Alice'], ['Bob']])
    
    def test_parse_strip_whitespace(self):
        """Test parsing with whitespace stripping."""
        content = "name\t age \n Alice \t 30  \n  Bob \t25"
        headers, rows = parse_tsv_string(content, strip_whitespace=True)
        self.assertEqual(headers, ['name', 'age'])
        self.assertEqual(rows, [['Alice', '30'], ['Bob', '25']])
    
    def test_parse_skip_empty_lines(self):
        """Test parsing with empty line skipping."""
        content = "name\tage\n\nAlice\t30\n\nBob\t25\n"
        headers, rows = parse_tsv_string(content, skip_empty_lines=True)
        self.assertEqual(rows, [['Alice', '30'], ['Bob', '25']])
    
    def test_parse_with_bom(self):
        """Test parsing TSV with BOM."""
        content = "\ufeffname\tage\nAlice\t30"
        headers, rows = parse_tsv_string(content)
        self.assertEqual(headers, ['name', 'age'])
        self.assertEqual(rows, [['Alice', '30']])
    
    def test_parse_custom_delimiter(self):
        """Test parsing with custom delimiter."""
        content = "name,age\nAlice,30\nBob,25"
        headers, rows = parse_tsv_string(content, delimiter=',')
        self.assertEqual(headers, ['name', 'age'])
        self.assertEqual(rows, [['Alice', '30'], ['Bob', '25']])


class TestToTSVString(unittest.TestCase):
    """Test TSV string generation."""
    
    def test_to_tsv_simple(self):
        """Test simple TSV generation."""
        headers = ['name', 'age']
        rows = [['Alice', '30'], ['Bob', '25']]
        result = to_tsv_string(headers, rows)
        self.assertEqual(result, "name\tage\nAlice\t30\nBob\t25")
    
    def test_to_tsv_no_header(self):
        """Test TSV generation without header."""
        rows = [['Alice', '30'], ['Bob', '25']]
        result = to_tsv_string(rows=rows)
        self.assertEqual(result, "Alice\t30\nBob\t25")
    
    def test_to_tsv_empty(self):
        """Test TSV generation with empty data."""
        result = to_tsv_string()
        self.assertEqual(result, "")
    
    def test_to_tsv_special_chars(self):
        """Test TSV generation with special characters."""
        headers = ['name', 'description']
        rows = [['Test', 'Line1\nLine2'], ['Quote', 'Say "hello"']]
        result = to_tsv_string(headers, rows)
        self.assertIn('"Line1\nLine2"', result)
        self.assertIn('"Say ""hello"""', result)
    
    def test_to_tsv_custom_delimiter(self):
        """Test TSV generation with custom delimiter."""
        headers = ['name', 'age']
        rows = [['Alice', '30']]
        result = to_tsv_string(headers, rows, delimiter=',')
        self.assertEqual(result, "name,age\nAlice,30")
    
    def test_dicts_to_tsv_string(self):
        """Test dict list to TSV conversion."""
        data = [
            {'name': 'Alice', 'age': '30'},
            {'name': 'Bob', 'age': '25'},
        ]
        result = dicts_to_tsv_string(data)
        self.assertIn('name\tage', result)
        self.assertIn('Alice\t30', result)
        self.assertIn('Bob\t25', result)
    
    def test_dicts_to_tsv_string_no_header(self):
        """Test dict list to TSV without header."""
        data = [{'name': 'Alice', 'age': '30'}]
        result = dicts_to_tsv_string(data, include_header=False)
        self.assertEqual(result, "Alice\t30")


class TestFileOperations(unittest.TestCase):
    """Test file read/write operations."""
    
    def test_write_and_read_tsv(self):
        """Test writing and reading TSV file."""
        headers = ['name', 'age', 'city']
        rows = [
            ['Alice', '30', 'NYC'],
            ['Bob', '25', 'LA'],
            ['Charlie', '35', 'SF'],
        ]
        
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, 'test.tsv')
            
            # Write
            rows_written = write_tsv(filepath, headers, rows)
            self.assertEqual(rows_written, 4)  # 1 header + 3 data rows
            
            # Read
            read_headers, read_rows = read_tsv(filepath)
            self.assertEqual(read_headers, headers)
            self.assertEqual(read_rows, rows)
    
    def test_write_tsv_with_bom(self):
        """Test writing TSV with BOM."""
        headers = ['name']
        rows = [['Alice']]
        
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, 'test.tsv')
            write_tsv(filepath, headers, rows, include_bom=True)
            
            with open(filepath, 'rb') as f:
                content = f.read()
            
            self.assertTrue(content.startswith(b'\xef\xbb\xbf'))
    
    def test_write_tsv_from_dicts(self):
        """Test writing TSV from dictionaries."""
        data = [
            {'name': 'Alice', 'age': '30'},
            {'name': 'Bob', 'age': '25'},
        ]
        
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, 'test.tsv')
            rows_written = write_tsv_from_dicts(filepath, data)
            self.assertEqual(rows_written, 3)  # 1 header + 2 data
            
            # Verify content
            read_data = read_tsv_as_dicts(filepath)
            self.assertEqual(read_data, data)
    
    def test_read_tsv_as_dicts(self):
        """Test reading TSV as dictionaries."""
        content = "name\tage\tcity\nAlice\t30\tNYC\nBob\t25\tLA"
        
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, 'test.tsv')
            with open(filepath, 'w') as f:
                f.write(content)
            
            result = read_tsv_as_dicts(filepath)
            
            self.assertEqual(len(result), 2)
            self.assertEqual(result[0], {'name': 'Alice', 'age': '30', 'city': 'NYC'})
            self.assertEqual(result[1], {'name': 'Bob', 'age': '25', 'city': 'LA'})
    
    def test_read_tsv_type_inference(self):
        """Test reading TSV with type inference."""
        content = "name\tage\tscore\nAlice\t30\t95.5\nBob\t25\t87.3"
        
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, 'test.tsv')
            with open(filepath, 'w') as f:
                f.write(content)
            
            headers, rows = read_tsv(filepath, type_inference=True)
            
            self.assertEqual(rows[0][1], 30)  # int
            self.assertEqual(rows[0][2], 95.5)  # float
            self.assertEqual(rows[1][1], 25)  # int
            self.assertEqual(rows[1][2], 87.3)  # float
    
    def test_read_tsv_streaming(self):
        """Test streaming TSV read."""
        content = "name\tage\n" + "\n".join([f"Person{i}\t{i+20}" for i in range(100)])
        
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, 'test.tsv')
            with open(filepath, 'w') as f:
                f.write(content)
            
            total_rows = 0
            for headers, chunk in read_tsv_streaming(filepath, chunk_size=30):
                if headers:
                    self.assertEqual(headers, ['name', 'age'])
                total_rows += len(chunk)
            
            self.assertEqual(total_rows, 100)
    
    def test_read_nonexistent_file(self):
        """Test reading non-existent file."""
        with self.assertRaises(FileNotFoundError):
            read_tsv('/nonexistent/path.tsv')
    
    def test_read_tsv_as_dicts_no_header(self):
        """Test reading TSV as dicts without header uses first row as headers."""
        content = "Alice\t30\nBob\t25"
        
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, 'test.tsv')
            with open(filepath, 'w') as f:
                f.write(content)
            
            # read_tsv_as_dicts always assumes has_header=True,
            # so first row becomes the header
            result = read_tsv_as_dicts(filepath)
            # First row 'Alice', '30' becomes headers
            # Second row 'Bob', '25' becomes the only data row
            self.assertEqual(len(result), 1)
            self.assertEqual(result[0], {'Alice': 'Bob', '30': '25'})


class TestValidateTSV(unittest.TestCase):
    """Test TSV validation."""
    
    def test_validate_valid_tsv(self):
        """Test validating valid TSV."""
        content = "name\tage\nAlice\t30\nBob\t25"
        
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, 'test.tsv')
            with open(filepath, 'w') as f:
                f.write(content)
            
            is_valid, issues = validate_tsv(filepath)
            self.assertTrue(is_valid)
            self.assertEqual(issues, [])
    
    def test_validate_inconsistent_columns(self):
        """Test validating TSV with inconsistent columns."""
        content = "name\tage\nAlice\t30\nBob"
        
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, 'test.tsv')
            with open(filepath, 'w') as f:
                f.write(content)
            
            is_valid, issues = validate_tsv(filepath)
            self.assertFalse(is_valid)
            self.assertTrue(any('Inconsistent' in issue for issue in issues))
    
    def test_validate_empty_file(self):
        """Test validating empty file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, 'empty.tsv')
            with open(filepath, 'w') as f:
                f.write('')
            
            is_valid, issues = validate_tsv(filepath)
            self.assertFalse(is_valid)
            self.assertTrue(any('empty' in issue.lower() for issue in issues))


class TestGetTSVInfo(unittest.TestCase):
    """Test TSV info retrieval."""
    
    def test_get_tsv_info(self):
        """Test getting TSV file info."""
        content = "name\tage\tcity\nAlice\t30\tNYC\nBob\t25\tLA"
        
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, 'test.tsv')
            with open(filepath, 'w') as f:
                f.write(content)
            
            info = get_tsv_info(filepath)
            
            self.assertEqual(info['row_count'], 2)
            self.assertEqual(info['column_count'], 3)
            self.assertEqual(info['headers'], ['name', 'age', 'city'])
            self.assertTrue(info['has_header'])
            self.assertTrue(info['file_size_bytes'] > 0)


class TestMergeTSVFiles(unittest.TestCase):
    """Test TSV file merging."""
    
    def test_merge_two_files(self):
        """Test merging two TSV files."""
        content1 = "name\tage\nAlice\t30\nBob\t25"
        content2 = "name\tage\nCharlie\t35\nDiana\t28"
        
        with tempfile.TemporaryDirectory() as tmpdir:
            file1 = os.path.join(tmpdir, 'file1.tsv')
            file2 = os.path.join(tmpdir, 'file2.tsv')
            output = os.path.join(tmpdir, 'merged.tsv')
            
            with open(file1, 'w') as f:
                f.write(content1)
            with open(file2, 'w') as f:
                f.write(content2)
            
            rows_written = merge_tsv_files(output, [file1, file2])
            self.assertEqual(rows_written, 5)  # header + 4 data rows
            
            headers, rows = read_tsv(output)
            self.assertEqual(headers, ['name', 'age'])
            self.assertEqual(len(rows), 4)


class TestRoundTrip(unittest.TestCase):
    """Test round-trip conversion."""
    
    def test_roundtrip_string(self):
        """Test string round-trip conversion."""
        headers = ['name', 'age', 'city', 'score']
        rows = [
            ['Alice', '30', 'New York', '95.5'],
            ['Bob', '25', 'London', '87.3'],
            ['Charlie', '35', 'Paris', '92.1'],
        ]
        
        tsv_string = to_tsv_string(headers, rows)
        parsed_headers, parsed_rows = parse_tsv_string(tsv_string)
        
        self.assertEqual(parsed_headers, headers)
        self.assertEqual(parsed_rows, rows)
    
    def test_roundtrip_dict(self):
        """Test dictionary round-trip conversion."""
        data = [
            {'name': 'Alice', 'age': '30', 'city': 'NYC'},
            {'name': 'Bob', 'age': '25', 'city': 'LA'},
        ]
        
        tsv_string = dicts_to_tsv_string(data)
        
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, 'test.tsv')
            with open(filepath, 'w') as f:
                f.write(tsv_string)
            
            read_data = read_tsv_as_dicts(filepath)
            self.assertEqual(read_data, data)
    
    def test_roundtrip_file(self):
        """Test file round-trip conversion."""
        headers = ['col1', 'col2', 'col3']
        rows = [
            ['a', 'b', 'c'],
            ['d', 'e', 'f'],
            ['g', 'h', 'i'],
        ]
        
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, 'roundtrip.tsv')
            
            write_tsv(filepath, headers, rows)
            read_headers, read_rows = read_tsv(filepath)
            
            self.assertEqual(read_headers, headers)
            self.assertEqual(read_rows, rows)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and special scenarios."""
    
    def test_empty_fields(self):
        """Test handling empty fields."""
        content = "a\t\tc\n1\t\t3"
        headers, rows = parse_tsv_string(content)
        
        self.assertEqual(headers, ['a', '', 'c'])
        self.assertEqual(rows, [['1', '', '3']])
    
    def test_unicode_content(self):
        """Test handling Unicode content."""
        content = "name\tcity\n日本語\t東京\n中文\t北京\nالعربية\tالقاهرة"
        headers, rows = parse_tsv_string(content)
        
        self.assertEqual(headers, ['name', 'city'])
        self.assertEqual(rows, [['日本語', '東京'], ['中文', '北京'], ['العربية', 'القاهرة']])
    
    def test_very_long_line(self):
        """Test handling very long line."""
        # Create a line with 1000 fields
        fields = [f'field{i}' for i in range(1000)]
        content = '\t'.join(fields)
        
        headers, rows = parse_tsv_string(content, has_header=False)
        
        self.assertEqual(len(rows[0]), 1000)
    
    def test_many_rows(self):
        """Test handling many rows."""
        rows = [[f'val{i}a', f'val{i}b'] for i in range(10000)]
        tsv_string = to_tsv_string(rows=rows)
        
        _, parsed_rows = parse_tsv_string(tsv_string, has_header=False)
        
        self.assertEqual(len(parsed_rows), 10000)
    
    def test_none_values(self):
        """Test handling None values."""
        headers = ['a', 'b', 'c']
        rows = [['x', None, 'z'], [None, 'y', None]]
        
        tsv_string = to_tsv_string(headers, rows)
        
        self.assertIn('x\t\tz', tsv_string)
        self.assertIn('\ty\t', tsv_string)
    
    def test_numeric_values(self):
        """Test handling numeric values."""
        headers = ['int', 'float', 'bool']
        rows = [[42, 3.14, True], [-10, -2.5, False]]
        
        tsv_string = to_tsv_string(headers, rows)
        
        self.assertIn('42', tsv_string)
        self.assertIn('3.14', tsv_string)
        self.assertIn('True', tsv_string)


if __name__ == '__main__':
    unittest.main(verbosity=2)