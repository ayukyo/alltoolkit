#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DOI Utils - Basic Usage Example
================================
Demonstrates common DOI utility operations.
"""

import sys
sys.path.insert(0, '..')

from mod import (
    validate, validate_strict, parse, to_url, from_url,
    extract_from_text, extract_from_html, get_doi_type,
    format_doi, is_short_doi, short_doi_to_url,
    encode_base62, decode_base62
)


def main():
    print("=" * 60)
    print("DOI Utils - Basic Usage Examples")
    print("=" * 60)
    print()
    
    # 1. Basic Validation
    print("1. Basic Validation")
    print("-" * 40)
    test_dois = [
        '10.1000/182',
        '10.1038/nphys1170',
        '10.1126/science.169.3946.635',
        'invalid-doi',
    ]
    for doi in test_dois:
        print(f"  {doi}: {validate(doi)}")
    print()
    
    # 2. Strict Validation
    print("2. Strict Validation (with details)")
    print("-" * 40)
    result = validate_strict('10.1038/nphys1170')
    print(f"  DOI: {result['doi']}")
    print(f"  Prefix: {result['prefix']}")
    print(f"  Suffix: {result['suffix']}")
    print(f"  URL: {result['url']}")
    print()
    
    # 3. Parsing DOI from URL
    print("3. Parsing DOI from URL")
    print("-" * 40)
    url = 'https://doi.org/10.1038/nphys1170'
    result = parse(url)
    print(f"  Input: {url}")
    print(f"  Parsed DOI: {result.doi}")
    print(f"  Clean URL: {result.url}")
    print()
    
    # 4. URL Conversion
    print("4. URL Conversion")
    print("-" * 40)
    doi = '10.1000/182'
    print(f"  DOI: {doi}")
    print(f"  URL: {to_url(doi)}")
    print(f"  Legacy URL: {to_url(doi, use_legacy=True)}")
    print()
    
    # 5. Text Extraction
    print("5. Extracting DOIs from Text")
    print("-" * 40)
    text = """
    This paper (doi:10.1038/nphys1170) discusses quantum physics.
    Related work: https://doi.org/10.1126/science.169.3946.635
    Dataset available at 10.5281/zenodo.12345.
    """
    dois = extract_from_text(text)
    print(f"  Found {len(dois)} DOIs:")
    for doi in dois:
        print(f"    - {doi}")
    print()
    
    # 6. HTML Extraction
    print("6. Extracting DOIs from HTML")
    print("-" * 40)
    html = '''
    <div class="references">
        <a href="https://doi.org/10.1000/182">Paper 1</a>
        <a href="doi:10.1038/nphys1170">Paper 2</a>
    </div>
    '''
    dois = extract_from_html(html)
    print(f"  Found {len(dois)} DOIs:")
    for doi in dois:
        print(f"    - {doi}")
    print()
    
    # 7. Type Inference
    print("7. DOI Type Inference")
    print("-" * 40)
    type_examples = [
        ('10.1038/nphys1170', 'Nature journal'),
        ('10.5281/zenodo.12345', 'Zenodo dataset'),
        ('10.1101/2020.03.15', 'bioRxiv preprint'),
        ('10.5072/thesis123', 'University thesis'),
    ]
    for doi, desc in type_examples:
        type_ = get_doi_type(doi)
        print(f"  {doi} ({desc}): {type_ or 'unknown'}")
    print()
    
    # 8. Formatting Styles
    print("8. DOI Formatting Styles")
    print("-" * 40)
    doi = '10.1000/182'
    print(f"  Standard: {format_doi(doi, 'standard')}")
    print(f"  URL: {format_doi(doi, 'url')}")
    print(f"  doi: prefix: {format_doi(doi, 'doi_prefix')}")
    print()
    
    # 9. Short DOI
    print("9. Short DOI Utilities")
    print("-" * 40)
    short_codes = ['abc', 'd7c', '10kg']
    for code in short_codes:
        if is_short_doi(code):
            print(f"  {code} -> {short_doi_to_url(code)}")
    print()
    
    # 10. Base62 Encoding
    print("10. Base62 Encoding/Decoding")
    print("-" * 40)
    numbers = [0, 10, 100, 1000, 12345]
    for num in numbers:
        encoded = encode_base62(num)
        decoded = decode_base62(encoded)
        print(f"  {num} -> {encoded} -> {decoded}")
    print()
    
    print("=" * 60)
    print("All examples completed!")
    print("=" * 60)


if __name__ == '__main__':
    main()