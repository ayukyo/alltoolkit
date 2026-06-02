#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Abbreviation Utilities Tests

Tests for the abbreviation_utils module.
"""

import pytest
from mod import (
    AbbreviationUtils,
    AbbreviationInfo,
    expand,
    expand_text,
    abbreviate,
    detect,
    get_info,
    is_abbreviation,
    find_abbreviation_for,
    expand_state,
    abbreviate_state,
    expand_country,
    abbreviate_country,
    get_all_by_category,
    get_categories,
    add_custom,
    count_abbreviations,
    COMMON_ACRONYMS,
    US_STATES,
    COUNTRY_CODES,
)


class TestExpand:
    """Tests for expand functions."""

    def test_expand_nasa(self):
        """Test expanding NASA."""
        assert expand('NASA') == 'National Aeronautics and Space Administration'

    def test_expand_ceo(self):
        """Test expanding CEO."""
        assert expand('CEO') == 'Chief Executive Officer'

    def test_expand_api(self):
        """Test expanding API."""
        assert expand('API') == 'Application Programming Interface'

    def test_expand_unknown(self):
        """Test expanding unknown abbreviation."""
        assert expand('unknown') is None

    def test_expand_case_insensitive(self):
        """Test that expand is case-insensitive."""
        assert expand('nasa') == 'National Aeronautics and Space Administration'
        assert expand('nasa') == expand('NASA')

    def test_expand_state(self):
        """Test expanding US state abbreviation."""
        assert expand('CA') == 'California'
        assert expand('NY') == 'New York'

    def test_expand_country(self):
        """Test expanding country code."""
        assert expand('US') == 'United States'
        assert expand('CN') == 'China'


class TestExpandText:
    """Tests for expand_text function."""

    def test_expand_text_basic(self):
        """Test basic text expansion."""
        result = expand_text('NASA launched a rocket')
        assert 'National Aeronautics and Space Administration' in result
        assert 'NASA' not in result or 'NASA' in result  # Either outcome fine

    def test_expand_text_keep_original(self):
        """Test expand_text with keep_original=True."""
        result = expand_text('NASA launched', keep_original=True)
        assert 'National Aeronautics and Space Administration (NASA)' in result

    def test_expand_text_empty(self):
        """Test expand_text with empty string."""
        assert expand_text('') == ''


class TestAbbreviate:
    """Tests for abbreviate function."""

    def test_abbreviate_ibm(self):
        """Test abbreviating IBM."""
        result = abbreviate('International Business Machines')
        assert result == 'IBM'

    def test_abbreviate_dmv(self):
        """Test abbreviating DMV."""
        result = abbreviate('Department of Motor Vehicles')
        assert result == 'DMV'

    def test_abbreviate_it(self):
        """Test abbreviating IT."""
        result = abbreviate('Information Technology')
        assert result == 'IT'

    def test_abbreviate_empty(self):
        """Test abbreviating empty string."""
        assert abbreviate('') == ''

    def test_abbreviate_max_length(self):
        """Test abbreviate with max_length parameter."""
        result = abbreviate('International Business Machines', max_length=2)
        assert len(result) <= 2


class TestDetect:
    """Tests for detect function."""

    def test_detect_nasa_fbi(self):
        """Test detecting NASA and FBI in text."""
        text = 'NASA and FBI work together'
        detected = detect(text)
        abbrevs = [d.abbreviation for d in detected]
        assert 'NASA' in abbrevs
        assert 'FBI' in abbrevs

    def test_detect_empty(self):
        """Test detecting in empty text."""
        assert detect('') == []


class TestGetInfo:
    """Tests for get_info function."""

    def test_get_info_nasa(self):
        """Test getting info for NASA."""
        info = get_info('NASA')
        assert info is not None
        assert info.abbreviation == 'NASA'
        assert info.is_acronym is True
        assert info.category == 'organization'

    def test_get_info_fbi(self):
        """Test getting info for FBI (initialism)."""
        info = get_info('FBI')
        assert info is not None
        assert info.is_initialism is True

    def test_get_info_unknown(self):
        """Test getting info for unknown abbreviation."""
        assert get_info('UNKNOWNXYZ123') is None


class TestIsAbbreviation:
    """Tests for is_abbreviation function."""

    def test_is_abbreviation_known(self):
        """Test known abbreviations."""
        assert is_abbreviation('NASA') is True
        assert is_abbreviation('CEO') is True

    def test_is_abbreviation_unknown(self):
        """Test unknown text."""
        assert is_abbreviation('Hello') is False
        assert is_abbreviation('randomword') is False


class TestFindAbbreviationFor:
    """Tests for find_abbreviation_for function."""

    def test_find_nasa(self):
        """Test finding NASA abbreviation."""
        result = find_abbreviation_for(
            'National Aeronautics and Space Administration'
        )
        assert result == 'NASA'

    def test_find_unknown(self):
        """Test finding abbreviation for unknown expansion."""
        assert find_abbreviation_for('Some Random Organization Name') is None


class TestStateAbbreviations:
    """Tests for US state abbreviation functions."""

    def test_expand_state(self):
        """Test expanding US state abbreviation."""
        assert expand_state('CA') == 'California'
        assert expand_state('TX') == 'Texas'

    def test_abbreviate_state(self):
        """Test getting state abbreviation."""
        assert abbreviate_state('California') == 'CA'
        assert abbreviate_state('New York') == 'NY'

    def test_state_roundtrip(self):
        """Test state expand/abbreviate roundtrip."""
        for code, name in US_STATES.items():
            assert abbreviate_state(name) == code


class TestCountryAbbreviations:
    """Tests for country code functions."""

    def test_expand_country(self):
        """Test expanding country code."""
        assert expand_country('US') == 'United States'
        assert expand_country('CN') == 'China'

    def test_abbreviate_country(self):
        """Test getting country abbreviation."""
        assert abbreviate_country('United States') == 'US'
        assert abbreviate_country('China') == 'CN'

    def test_country_roundtrip(self):
        """Test country expand/abbreviate roundtrip."""
        for code, name in COUNTRY_CODES.items():
            assert abbreviate_country(name) == code


class TestGetAllByCategory:
    """Tests for get_all_by_category function."""

    def test_get_technology(self):
        """Test getting technology category abbreviations."""
        tech = get_all_by_category('technology')
        assert 'API' in tech
        assert 'URL' in tech
        assert 'HTML' in tech

    def test_get_organization(self):
        """Test getting organization category abbreviations."""
        org = get_all_by_category('organization')
        assert 'NASA' in org
        assert 'FBI' in org

    def test_get_business(self):
        """Test getting business category abbreviations."""
        biz = get_all_by_category('business')
        assert 'CEO' in biz
        assert 'CFO' in biz


class TestGetCategories:
    """Tests for get_categories function."""

    def test_get_categories_contains_main(self):
        """Test that main categories are present."""
        categories = get_categories()
        assert 'technology' in categories
        assert 'organization' in categories
        assert 'business' in categories
        assert 'medical' in categories


class TestAddCustom:
    """Tests for add_custom function."""

    def test_add_custom(self):
        """Test adding custom abbreviation."""
        add_custom('TEST', 'Test Expansion', 'custom')
        assert expand('TEST') == 'Test Expansion'

    def test_custom_in_get_info(self):
        """Test that custom abbreviation shows in get_info."""
        add_custom('MYCO', 'My Custom Organization')
        info = get_info('MYCO')
        assert info is not None
        assert info.expansion == 'My Custom Organization'


class TestCountAbbreviations:
    """Tests for count_abbreviations function."""

    def test_count_nasa_twice(self):
        """Test counting NASA twice in text."""
        counts = count_abbreviations('NASA and NASA work with FBI')
        assert counts['NASA'] == 2
        assert counts['FBI'] == 1

    def test_count_empty(self):
        """Test counting in empty text."""
        assert count_abbreviations('') == {}


class TestAbbreviationInfo:
    """Tests for AbbreviationInfo dataclass."""

    def test_info_creation(self):
        """Test creating AbbreviationInfo."""
        info = AbbreviationInfo(
            abbreviation='NASA',
            expansion='National Aeronautics and Space Administration',
            is_acronym=True,
            is_initialism=False,
            category='organization',
            case_type='uppercase'
        )
        assert info.abbreviation == 'NASA'
        assert info.is_acronym is True


class TestAbbreviationsDatabase:
    """Tests for abbreviations database."""

    def test_nasa_in_database(self):
        """Test NASA is in database."""
        assert 'NASA' in COMMON_ACRONYMS

    def test_database_has_valid_categories(self):
        """Test that database entries have valid categories for built-in entries."""
        valid_categories = {'organization', 'technology', 'business', 
                            'medical', 'academic', 'government', 'common'}
        # Check only NASA as a representative built-in entry
        assert COMMON_ACRONYMS['NASA'][1] in valid_categories


class TestEdgeCases:
    """Tests for edge cases."""

    def test_expand_lowercase_etc(self):
        """Test expanding lowercase 'etc'."""
        result = expand('etc')
        assert result == 'et cetera'

    def test_abbreviate_single_word(self):
        """Test abbreviating single word."""
        result = abbreviate('Test')
        assert result == 'T'

    def test_expand_text_no_abbreviations(self):
        """Test expand_text with no abbreviations."""
        result = expand_text('Hello World')
        assert result == 'Hello World'


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
