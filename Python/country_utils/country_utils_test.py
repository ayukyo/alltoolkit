#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AllToolkit - Country Utilities Test Suite

Comprehensive tests for country_utils module.

Author: AllToolkit
License: MIT
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    Country,
    get_country,
    get_by_alpha2,
    get_by_alpha3,
    get_by_numeric,
    get_by_name,
    search_countries,
    get_all_countries,
    get_countries_by_continent,
    get_countries_by_region,
    validate_alpha2,
    validate_alpha3,
    validate_numeric,
    alpha2_to_alpha3,
    alpha3_to_alpha2,
    alpha2_to_numeric,
    numeric_to_alpha2,
    get_flag_emoji,
    get_calling_code,
    get_currency,
    get_continents,
    get_regions,
    find,
    all_countries,
)


def test_get_by_alpha2():
    """Test get_by_alpha2 function"""
    print("Testing get_by_alpha2...")
    
    # Valid alpha-2 codes
    us = get_by_alpha2("US")
    assert us is not None
    assert us.alpha2 == "US"
    assert us.alpha3 == "USA"
    assert us.numeric == "840"
    assert us.name_en == "United States"
    assert us.name_zh == "美国"
    assert us.continent == "North America"
    assert us.calling_code == "+1"
    assert us.currency == "USD"
    
    cn = get_by_alpha2("CN")
    assert cn is not None
    assert cn.alpha2 == "CN"
    assert cn.alpha3 == "CHN"
    assert cn.name_en == "China"
    assert cn.name_zh == "中国"
    
    # Case insensitive
    jp = get_by_alpha2("jp")
    assert jp is not None
    assert jp.alpha2 == "JP"
    
    # Invalid codes
    assert get_by_alpha2("XX") is None
    assert get_by_alpha2("") is None
    assert get_by_alpha2("USA") is None  # Too long
    
    print("  ✓ get_by_alpha2 passed")


def test_get_by_alpha3():
    """Test get_by_alpha3 function"""
    print("Testing get_by_alpha3...")
    
    # Valid alpha-3 codes
    usa = get_by_alpha3("USA")
    assert usa is not None
    assert usa.alpha2 == "US"
    assert usa.name_en == "United States"
    
    chn = get_by_alpha3("CHN")
    assert chn is not None
    assert chn.alpha2 == "CN"
    
    # Case insensitive
    jpn = get_by_alpha3("jpn")
    assert jpn is not None
    assert jpn.alpha2 == "JP"
    
    # Invalid codes
    assert get_by_alpha3("XXX") is None
    assert get_by_alpha3("") is None
    assert get_by_alpha3("US") is None  # Too short
    
    print("  ✓ get_by_alpha3 passed")


def test_get_by_numeric():
    """Test get_by_numeric function"""
    print("Testing get_by_numeric...")
    
    # Valid numeric codes
    us = get_by_numeric("840")
    assert us is not None
    assert us.alpha2 == "US"
    
    cn = get_by_numeric("156")
    assert cn is not None
    assert cn.alpha2 == "CN"
    
    jp = get_by_numeric("392")
    assert jp is not None
    assert jp.alpha2 == "JP"
    
    # Invalid codes
    assert get_by_numeric("000") is None
    assert get_by_numeric("") is None
    assert get_by_numeric("84") is None  # Too short
    
    print("  ✓ get_by_numeric passed")


def test_get_by_name():
    """Test get_by_name function"""
    print("Testing get_by_name...")
    
    # English names
    us = get_by_name("United States")
    assert us is not None
    assert us.alpha2 == "US"
    
    # Case insensitive English
    china = get_by_name("china")
    assert china is not None
    assert china.alpha2 == "CN"
    
    # Chinese names
    zh_cn = get_by_name("中国")
    assert zh_cn is not None
    assert zh_cn.alpha2 == "CN"
    
    zh_jp = get_by_name("日本")
    assert zh_jp is not None
    assert zh_jp.alpha2 == "JP"
    
    # Invalid names
    assert get_by_name("Unknown Country") is None
    assert get_by_name("") is None
    
    print("  ✓ get_by_name passed")


def test_get_country():
    """Test get_country function (multi-code lookup)"""
    print("Testing get_country...")
    
    # Alpha-2
    us1 = get_country("US")
    assert us1 is not None
    assert us1.alpha2 == "US"
    
    # Alpha-3
    us2 = get_country("USA")
    assert us2 is not None
    assert us2.alpha2 == "US"
    
    # Numeric
    us3 = get_country("840")
    assert us3 is not None
    assert us3.alpha2 == "US"
    
    # All should return the same country
    assert us1.alpha2 == us2.alpha2 == us3.alpha2
    
    # Invalid
    assert get_country("XX") is None
    assert get_country("") is None
    
    print("  ✓ get_country passed")


def test_search_countries():
    """Test search_countries function"""
    print("Testing search_countries...")
    
    # Search by partial English name
    results = search_countries("United", limit=10)
    assert len(results) > 0
    # Should include United States and United Kingdom
    names = [c.name_en for c in results]
    assert any("United" in n for n in names)
    
    # Search by Chinese name
    zh_results = search_countries("韩")
    assert len(zh_results) > 0
    assert any(c.name_zh == "韩国" for c in zh_results)
    
    # Search by code
    code_results = search_countries("US")
    assert len(code_results) > 0
    
    # Limit works
    limited = search_countries("a", limit=5)
    assert len(limited) <= 5
    
    # No results for invalid query
    no_results = search_countries("XYZXYZ")
    assert len(no_results) == 0
    
    print("  ✓ search_countries passed")


def test_get_all_countries():
    """Test get_all_countries function"""
    print("Testing get_all_countries...")
    
    all_list = get_all_countries()
    assert len(all_list) > 100
    assert all(isinstance(c, Country) for c in all_list)
    
    # Should be sorted by alpha2
    alpha2_codes = [c.alpha2 for c in all_list]
    assert alpha2_codes == sorted(alpha2_codes)
    
    # Check some known countries exist
    alpha2_set = {c.alpha2 for c in all_list}
    assert "US" in alpha2_set
    assert "CN" in alpha2_set
    assert "JP" in alpha2_set
    
    print("  ✓ get_all_countries passed")


def test_get_countries_by_continent():
    """Test get_countries_by_continent function"""
    print("Testing get_countries_by_continent...")
    
    asia = get_countries_by_continent("Asia")
    assert len(asia) > 40
    assert all(c.continent == "Asia" for c in asia)
    
    europe = get_countries_by_continent("Europe")
    assert len(europe) > 40
    assert all(c.continent == "Europe" for c in europe)
    
    africa = get_countries_by_continent("Africa")
    assert len(africa) > 50
    assert all(c.continent == "Africa" for c in africa)
    
    # Check some Asian countries
    asia_alpha2 = {c.alpha2 for c in asia}
    assert "CN" in asia_alpha2
    assert "JP" in asia_alpha2
    
    print("  ✓ get_countries_by_continent passed")


def test_get_countries_by_region():
    """Test get_countries_by_region function"""
    print("Testing get_countries_by_region...")
    
    east_asia = get_countries_by_region("East Asia")
    assert len(east_asia) >= 7
    assert all(c.region == "East Asia" for c in east_asia)
    
    east_asia_alpha2 = {c.alpha2 for c in east_asia}
    assert "CN" in east_asia_alpha2
    assert "JP" in east_asia_alpha2
    assert "KR" in east_asia_alpha2
    
    southeast_asia = get_countries_by_region("Southeast Asia")
    assert len(southeast_asia) >= 10
    sea_alpha2 = {c.alpha2 for c in southeast_asia}
    assert "VN" in sea_alpha2
    assert "TH" in sea_alpha2
    assert "SG" in sea_alpha2
    
    print("  ✓ get_countries_by_region passed")


def test_validation():
    """Test validation functions"""
    print("Testing validation functions...")
    
    # Alpha-2 validation
    assert validate_alpha2("US") == True
    assert validate_alpha2("CN") == True
    assert validate_alpha2("JP") == True
    assert validate_alpha2("XX") == False
    assert validate_alpha2("USA") == False  # Too long
    assert validate_alpha2("") == False
    assert validate_alpha2("1") == False
    
    # Alpha-3 validation
    assert validate_alpha3("USA") == True
    assert validate_alpha3("CHN") == True
    assert validate_alpha3("JPN") == True
    assert validate_alpha3("XXX") == False
    assert validate_alpha3("US") == False  # Too short
    assert validate_alpha3("") == False
    
    # Numeric validation
    assert validate_numeric("840") == True
    assert validate_numeric("156") == True
    assert validate_numeric("392") == True
    assert validate_numeric("000") == False
    assert validate_numeric("84") == False  # Too short
    assert validate_numeric("") == False
    assert validate_numeric("abc") == False
    
    print("  ✓ validation functions passed")


def test_code_conversion():
    """Test code conversion functions"""
    print("Testing code conversion functions...")
    
    # Alpha-2 to Alpha-3
    assert alpha2_to_alpha3("US") == "USA"
    assert alpha2_to_alpha3("CN") == "CHN"
    assert alpha2_to_alpha3("JP") == "JPN"
    assert alpha2_to_alpha3("XX") is None
    
    # Alpha-3 to Alpha-2
    assert alpha3_to_alpha2("USA") == "US"
    assert alpha3_to_alpha2("CHN") == "CN"
    assert alpha3_to_alpha2("JPN") == "JP"
    assert alpha3_to_alpha2("XXX") is None
    
    # Alpha-2 to Numeric
    assert alpha2_to_numeric("US") == "840"
    assert alpha2_to_numeric("CN") == "156"
    assert alpha2_to_numeric("JP") == "392"
    assert alpha2_to_numeric("XX") is None
    
    # Numeric to Alpha-2
    assert numeric_to_alpha2("840") == "US"
    assert numeric_to_alpha2("156") == "CN"
    assert numeric_to_alpha2("392") == "JP"
    assert numeric_to_alpha2("000") is None
    
    print("  ✓ code conversion passed")


def test_flag_emoji():
    """Test get_flag_emoji function"""
    print("Testing get_flag_emoji...")
    
    # Known flag emojis
    assert get_flag_emoji("US") == "🇺🇸"
    assert get_flag_emoji("CN") == "🇨🇳"
    assert get_flag_emoji("JP") == "🇯🇵"
    assert get_flag_emoji("KR") == "🇰🇷"
    assert get_flag_emoji("GB") == "🇬🇧"
    assert get_flag_emoji("DE") == "🇩🇪"
    assert get_flag_emoji("FR") == "🇫🇷"
    
    # Works with alpha-3 too
    assert get_flag_emoji("USA") == "🇺🇸"
    assert get_flag_emoji("CHN") == "🇨🇳"
    
    # Works with numeric
    assert get_flag_emoji("840") == "🇺🇸"
    
    # Invalid returns empty
    assert get_flag_emoji("XX") == ""
    assert get_flag_emoji("") == ""
    
    print("  ✓ get_flag_emoji passed")


def test_calling_code():
    """Test get_calling_code function"""
    print("Testing get_calling_code...")
    
    assert get_calling_code("US") == "+1"
    assert get_calling_code("CN") == "+86"
    assert get_calling_code("JP") == "+81"
    assert get_calling_code("KR") == "+82"
    assert get_calling_code("GB") == "+44"
    assert get_calling_code("DE") == "+49"
    
    # Invalid returns None
    assert get_calling_code("XX") is None
    assert get_calling_code("") is None
    
    print("  ✓ get_calling_code passed")


def test_get_currency():
    """Test get_currency function"""
    print("Testing get_currency...")
    
    assert get_currency("US") == "USD"
    assert get_currency("CN") == "CNY"
    assert get_currency("JP") == "JPY"
    assert get_currency("KR") == "KRW"
    assert get_currency("GB") == "GBP"
    assert get_currency("DE") == "EUR"
    assert get_currency("FR") == "EUR"
    
    # Invalid returns None
    assert get_currency("XX") is None
    assert get_currency("") is None
    
    print("  ✓ get_currency passed")


def test_get_continents():
    """Test get_continents function"""
    print("Testing get_continents...")
    
    continents = get_continents()
    expected = {"Asia", "Europe", "Africa", "North America", "South America", "Oceania"}
    assert continents == expected
    
    print("  ✓ get_continents passed")


def test_get_regions():
    """Test get_regions function"""
    print("Testing get_regions...")
    
    regions = get_regions()
    assert "East Asia" in regions
    assert "Southeast Asia" in regions
    assert "Western Europe" in regions
    assert "Northern Africa" in regions
    
    print("  ✓ get_regions passed")


def test_country_dataclass():
    """Test Country dataclass"""
    print("Testing Country dataclass...")
    
    us = get_by_alpha2("US")
    
    # Test repr
    assert repr(us) == "Country(US, United States)"
    
    # Test to_dict
    us_dict = us.to_dict()
    assert us_dict["alpha2"] == "US"
    assert us_dict["alpha3"] == "USA"
    assert us_dict["numeric"] == "840"
    assert us_dict["name_en"] == "United States"
    assert us_dict["name_zh"] == "美国"
    assert us_dict["continent"] == "North America"
    assert us_dict["calling_code"] == "+1"
    assert us_dict["currency"] == "USD"
    assert us_dict["flag_emoji"] == "🇺🇸"
    
    print("  ✓ Country dataclass passed")


def test_aliases():
    """Test convenience aliases"""
    print("Testing aliases...")
    
    # find alias
    us = find("US")
    assert us is not None
    assert us.alpha2 == "US"
    
    # all_countries alias
    all_list = all_countries()
    assert len(all_list) > 100
    
    print("  ✓ aliases passed")


def run_all_tests():
    """Run all tests"""
    print("=" * 50)
    print("Country Utils Test Suite")
    print("=" * 50)
    print()
    
    test_get_by_alpha2()
    test_get_by_alpha3()
    test_get_by_numeric()
    test_get_by_name()
    test_get_country()
    test_search_countries()
    test_get_all_countries()
    test_get_countries_by_continent()
    test_get_countries_by_region()
    test_validation()
    test_code_conversion()
    test_flag_emoji()
    test_calling_code()
    test_get_currency()
    test_get_continents()
    test_get_regions()
    test_country_dataclass()
    test_aliases()
    
    print()
    print("=" * 50)
    print("✅ All tests passed!")
    print("=" * 50)


if __name__ == "__main__":
    run_all_tests()