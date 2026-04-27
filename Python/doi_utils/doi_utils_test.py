#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - DOI Utilities Test Module
========================================
Unit tests for DOI validation, parsing, and manipulation utilities.

Author: AllToolkit
License: MIT
"""

import unittest
from mod import (
    clean, validate, validate_strict, parse, normalize,
    to_url, from_url, extract_from_text, extract_from_html,
    is_short_doi, short_doi_to_url, encode_base62, decode_base62,
    get_doi_type, format_doi, validate_batch, extract_unique_dois,
    DOIError, InvalidDOIError, DOIResult
)


class TestDOIClean(unittest.TestCase):
    """Test DOI cleaning functions."""
    
    def test_clean_url_prefix(self):
        """Test removing URL prefixes."""
        self.assertEqual(clean('https://doi.org/10.1000/182'), '10.1000/182')
        self.assertEqual(clean('http://doi.org/10.1000/182'), '10.1000/182')
        self.assertEqual(clean('https://dx.doi.org/10.1000/182'), '10.1000/182')
        self.assertEqual(clean('http://dx.doi.org/10.1000/182'), '10.1000/182')
    
    def test_clean_doi_prefix(self):
        """Test removing doi: prefix."""
        self.assertEqual(clean('doi:10.1000/182'), '10.1000/182')
        self.assertEqual(clean('DOI:10.1000/182'), '10.1000/182')
        self.assertEqual(clean('doi: 10.1000/182'), '10.1000/182')
    
    def test_clean_whitespace(self):
        """Test whitespace handling."""
        self.assertEqual(clean('  10.1000/182  '), '10.1000/182')
        self.assertEqual(clean('\t10.1000/182\n'), '10.1000/182')
    
    def test_clean_empty(self):
        """Test empty input."""
        self.assertEqual(clean(''), '')
        self.assertEqual(clean(None), '')  # Should handle None gracefully
    
    def test_clean_plain_doi(self):
        """Test plain DOI (no changes needed)."""
        self.assertEqual(clean('10.1000/182'), '10.1000/182')


class TestDOIValidate(unittest.TestCase):
    """Test DOI validation functions."""
    
    def test_validate_valid_dois(self):
        """Test validation of valid DOIs."""
        self.assertTrue(validate('10.1000/182'))
        self.assertTrue(validate('10.1038/nphys1170'))
        self.assertTrue(validate('10.1126/science.169.3946.635'))
        self.assertTrue(validate('10.1101/2020.03.15.200333'))
        self.assertTrue(validate('https://doi.org/10.1000/182'))
        self.assertTrue(validate('doi:10.1000/182'))
    
    def test_validate_invalid_dois(self):
        """Test validation of invalid DOIs."""
        self.assertFalse(validate('invalid'))
        self.assertFalse(validate('10./suffix'))
        self.assertFalse(validate('10.123/suffix'))  # Too short prefix
        self.assertFalse(validate(''))
        self.assertFalse(validate('11.1000/182'))  # Wrong start
    
    def test_validate_strict_valid(self):
        """Test strict validation returns details."""
        result = validate_strict('10.1000/182')
        self.assertTrue(result['valid'])
        self.assertEqual(result['doi'], '10.1000/182')
        self.assertEqual(result['prefix'], '10.1000')
        self.assertEqual(result['suffix'], '/182')
        self.assertEqual(result['url'], 'https://doi.org/10.1000/182')
    
    def test_validate_strict_invalid(self):
        """Test strict validation raises exception."""
        with self.assertRaises(InvalidDOIError):
            validate_strict('invalid-doi')
        with self.assertRaises(InvalidDOIError):
            validate_strict('10.123/short')


class TestDOIParse(unittest.TestCase):
    """Test DOI parsing functions."""
    
    def test_parse_valid(self):
        """Test parsing valid DOI."""
        result = parse('https://doi.org/10.1000/182')
        self.assertTrue(result.valid)
        self.assertEqual(result.doi, '10.1000/182')
        self.assertEqual(result.prefix, '10.1000')
        self.assertEqual(result.suffix, '/182')
        self.assertEqual(result.url, 'https://doi.org/10.1000/182')
    
    def test_parse_invalid(self):
        """Test parsing invalid DOI returns invalid result."""
        result = parse('invalid')
        self.assertFalse(result.valid)
        self.assertEqual(result.prefix, '')
        self.assertEqual(result.suffix, '')
    
    def test_parse_complex_suffix(self):
        """Test parsing DOI with complex suffix."""
        result = parse('10.1126/science.169.3946.635')
        self.assertTrue(result.valid)
        self.assertEqual(result.suffix, '/science.169.3946.635')


class TestDOIURLConversion(unittest.TestCase):
    """Test DOI URL conversion functions."""
    
    def test_to_url_standard(self):
        """Test standard URL conversion."""
        self.assertEqual(to_url('10.1000/182'), 'https://doi.org/10.1000/182')
        self.assertEqual(to_url('doi:10.1000/182'), 'https://doi.org/10.1000/182')
    
    def test_to_url_legacy(self):
        """Test legacy URL conversion."""
        self.assertEqual(to_url('10.1000/182', use_legacy=True), 
                         'https://dx.doi.org/10.1000/182')
    
    def test_from_url(self):
        """Test extracting DOI from URL."""
        self.assertEqual(from_url('https://doi.org/10.1000/182'), '10.1000/182')
        self.assertEqual(from_url('https://dx.doi.org/10.1000/182'), '10.1000/182')
    
    def test_from_url_non_doi(self):
        """Test non-DOI URL returns None."""
        self.assertIsNone(from_url('https://example.com/page'))


class TestDOIExtraction(unittest.TestCase):
    """Test DOI extraction functions."""
    
    def test_extract_from_text_single(self):
        """Test extracting single DOI."""
        text = "This paper (doi:10.1000/182) is interesting."
        dois = extract_from_text(text)
        self.assertEqual(dois, ['10.1000/182'])
    
    def test_extract_from_text_multiple(self):
        """Test extracting multiple DOIs."""
        text = "See doi:10.1000/182 and https://doi.org/10.1038/nphys1170"
        dois = extract_from_text(text)
        self.assertIn('10.1000/182', dois)
        self.assertIn('10.1038/nphys1170', dois)
    
    def test_extract_from_text_none(self):
        """Test text without DOIs."""
        text = "This text has no DOI references."
        dois = extract_from_text(text)
        self.assertEqual(dois, [])
    
    def test_extract_from_html(self):
        """Test extracting DOI from HTML."""
        html = '<a href="https://doi.org/10.1000/182">Link</a>'
        dois = extract_from_html(html)
        self.assertEqual(dois, ['10.1000/182'])
    
    def test_extract_unique(self):
        """Test extracting unique DOIs."""
        text = "doi:10.1000/182 doi:10.1000/182 https://doi.org/10.1000/182"
        dois = extract_unique_dois(text)
        self.assertEqual(dois, ['10.1000/182'])


class TestShortDOI(unittest.TestCase):
    """Test short DOI functions."""
    
    def test_is_short_doi(self):
        """Test short DOI pattern matching."""
        self.assertTrue(is_short_doi('abc'))
        self.assertTrue(is_short_doi('d7c'))
        self.assertTrue(is_short_doi('10kg'))
        self.assertFalse(is_short_doi('a'))  # Too short
        self.assertFalse(is_short_doi('abcdefghijk'))  # Too long
    
    def test_short_doi_to_url(self):
        """Test short DOI URL generation."""
        self.assertEqual(short_doi_to_url('abc'), 'https://shortdoi.org/abc')
    
    def test_base62_encode(self):
        """Test base62 encoding."""
        self.assertEqual(encode_base62(0), '0')
        self.assertEqual(encode_base62(10), 'a')
        self.assertEqual(encode_base62(35), 'z')
        self.assertEqual(encode_base62(36), 'A')
        self.assertEqual(encode_base62(61), 'Z')
    
    def test_base62_decode(self):
        """Test base62 decoding."""
        self.assertEqual(decode_base62('0'), 0)
        self.assertEqual(decode_base62('a'), 10)
        self.assertEqual(decode_base62('z'), 35)
        self.assertEqual(decode_base62('A'), 36)
        self.assertEqual(decode_base62('Z'), 61)
        self.assertEqual(decode_base62('10'), 62)  # 1*62 + 0
    
    def test_base62_roundtrip(self):
        """Test base62 encode/decode roundtrip."""
        for num in [0, 10, 35, 36, 61, 100, 1000, 10000, 100000]:
            encoded = encode_base62(num)
            decoded = decode_base62(encoded)
            self.assertEqual(decoded, num, f"Roundtrip failed for {num}: {encoded}")


class TestDOIType(unittest.TestCase):
    """Test DOI type inference."""
    
    def test_journal_type(self):
        """Test journal DOI type."""
        self.assertEqual(get_doi_type('10.1038/nphys1170'), 'journal')
    
    def test_dataset_type(self):
        """Test dataset DOI type."""
        self.assertEqual(get_doi_type('10.5281/zenodo.12345'), 'dataset')
        self.assertEqual(get_doi_type('10.5252/figshare.123'), 'dataset')
    
    def test_preprint_type(self):
        """Test preprint DOI type."""
        self.assertEqual(get_doi_type('10.1101/abc123'), 'preprint')
    
    def test_invalid_doi_type(self):
        """Test invalid DOI returns None."""
        self.assertIsNone(get_doi_type('invalid'))


class TestDOIFormat(unittest.TestCase):
    """Test DOI formatting functions."""
    
    def test_format_standard(self):
        """Test standard format."""
        self.assertEqual(format_doi('10.1000/182', 'standard'), '10.1000/182')
    
    def test_format_url(self):
        """Test URL format."""
        self.assertEqual(format_doi('10.1000/182', 'url'), 
                         'https://doi.org/10.1000/182')
    
    def test_format_doi_prefix(self):
        """Test doi: prefix format."""
        self.assertEqual(format_doi('10.1000/182', 'doi_prefix'), 
                         'doi:10.1000/182')


class TestBatchOperations(unittest.TestCase):
    """Test batch operations."""
    
    def test_validate_batch_valid(self):
        """Test batch validation of valid DOIs."""
        results = validate_batch(['10.1000/182', '10.1038/nphys1170'])
        self.assertEqual(len(results), 2)
        for r in results:
            self.assertTrue(r['valid'])
    
    def test_validate_batch_mixed(self):
        """Test batch validation with invalid DOI."""
        results = validate_batch(['10.1000/182', 'invalid'])
        self.assertEqual(len(results), 2)
        self.assertTrue(results[0]['valid'])
        self.assertFalse(results[1]['valid'])


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and special scenarios."""
    
    def test_special_characters_in_suffix(self):
        """Test DOI with special characters in suffix."""
        doi = '10.1000/test-(1)-[2]-{3}'
        self.assertTrue(validate(doi))
    
    def test_long_registrant(self):
        """Test DOI with long registrant number."""
        doi = '10.123456789/test'
        self.assertTrue(validate(doi))
    
    def test_unicode_in_suffix(self):
        """Test DOI with unicode characters might be handled."""
        # DOI suffix can technically contain unicode
        doi = '10.1000/测试'
        cleaned = clean(doi)
        self.assertEqual(cleaned, '10.1000/测试')
    
    def test_normalized(self):
        """Test normalization."""
        self.assertEqual(normalize('DOI:10.1000/182'), '10.1000/182')
        self.assertEqual(normalize('https://doi.org/10.1000/182'), '10.1000/182')


if __name__ == '__main__':
    unittest.main(verbosity=2)