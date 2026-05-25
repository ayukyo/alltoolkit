"""
AllToolkit - Abbreviation Utilities Tests
"""

import unittest
from mod import (
    AbbreviationUtils,
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
)


class TestExpand(unittest.TestCase):
    """Test abbreviation expansion."""
    
    def test_expand_organization_acronyms(self):
        """Test organization acronyms."""
        self.assertEqual(expand("NASA"), "National Aeronautics and Space Administration")
        self.assertEqual(expand("FBI"), "Federal Bureau of Investigation")
        self.assertEqual(expand("UN"), "United Nations")
        self.assertEqual(expand("WHO"), "World Health Organization")
    
    def test_expand_technology_acronyms(self):
        """Test technology acronyms."""
        self.assertEqual(expand("API"), "Application Programming Interface")
        self.assertEqual(expand("URL"), "Uniform Resource Locator")
        self.assertEqual(expand("CPU"), "Central Processing Unit")
        self.assertEqual(expand("RAM"), "Random Access Memory")
    
    def test_expand_business_acronyms(self):
        """Test business acronyms."""
        self.assertEqual(expand("CEO"), "Chief Executive Officer")
        self.assertEqual(expand("CFO"), "Chief Financial Officer")
        self.assertEqual(expand("HR"), "Human Resources")
        self.assertEqual(expand("ROI"), "Return on Investment")
    
    def test_expand_common_abbreviations(self):
        """Test common abbreviations."""
        self.assertEqual(expand("etc"), "et cetera")
        self.assertEqual(expand("e.g."), "exempli gratia")
        self.assertEqual(expand("i.e."), "id est")
    
    def test_expand_state_codes(self):
        """Test US state codes."""
        self.assertEqual(expand("CA"), "California")
        self.assertEqual(expand("NY"), "New York")
        self.assertEqual(expand("TX"), "Texas")
        self.assertEqual(expand("FL"), "Florida")
    
    def test_expand_country_codes(self):
        """Test country codes."""
        self.assertEqual(expand("US"), "United States")
        self.assertEqual(expand("CN"), "China")
        self.assertEqual(expand("JP"), "Japan")
        # Note: UK returns the expansion from COMMON_ACRONYMS or COUNTRY_CODES
        # The behavior depends on which database is checked first
    
    def test_expand_unknown(self):
        """Test unknown abbreviations."""
        self.assertIsNone(expand("UNKNOWN"))
        self.assertIsNone(expand("XYZ"))
        self.assertIsNone(expand(""))
    
    def test_expand_case_insensitive(self):
        """Test case insensitive expansion."""
        self.assertEqual(expand("nasa"), "National Aeronautics and Space Administration")
        self.assertEqual(expand("Nasa"), "National Aeronautics and Space Administration")
        self.assertEqual(expand("NASA"), "National Aeronautics and Space Administration")


class TestExpandText(unittest.TestCase):
    """Test text expansion."""
    
    def test_expand_single_abbreviation(self):
        """Test expanding single abbreviation in text."""
        text = "NASA launched a rocket."
        result = expand_text(text)
        self.assertEqual(result, "National Aeronautics and Space Administration launched a rocket.")
    
    def test_expand_multiple_abbreviations(self):
        """Test expanding multiple abbreviations."""
        text = "NASA and FBI work together."
        result = expand_text(text)
        self.assertEqual(result, "National Aeronautics and Space Administration and Federal Bureau of Investigation work together.")
    
    def test_expand_with_original(self):
        """Test keeping original abbreviation."""
        text = "NASA launched."
        result = expand_text(text, keep_original=True)
        self.assertEqual(result, "National Aeronautics and Space Administration (NASA) launched.")
    
    def test_expand_empty_text(self):
        """Test empty text."""
        self.assertEqual(expand_text(""), "")
    
    def test_expand_no_abbreviations(self):
        """Test text with no abbreviations."""
        text = "Hello world, this is a test."
        self.assertEqual(expand_text(text), text)


class TestAbbreviate(unittest.TestCase):
    """Test abbreviation creation."""
    
    def test_abbreviate_acronym_style(self):
        """Test acronym style."""
        self.assertEqual(abbreviate("International Business Machines", style="acronym"), "IBM")
        self.assertEqual(abbreviate("Department of Motor Vehicles", style="acronym"), "DMV")
        self.assertEqual(abbreviate("Information Technology", style="acronym"), "IT")
    
    def test_abbreviate_skip_connectors(self):
        """Test skipping connector words."""
        self.assertEqual(abbreviate("North Atlantic Treaty Organization", style="acronym"), "NATO")
        self.assertEqual(abbreviate("National Aeronautics and Space Administration", style="acronym"), "NASA")
    
    def test_abbreviate_max_length(self):
        """Test max length."""
        self.assertEqual(abbreviate("International Business Machines", max_length=3, style="acronym"), "IBM")
        self.assertEqual(abbreviate("Very Long Organization Name Here", max_length=4, style="acronym"), "VLON")
    
    def test_abbreviate_truncation_style(self):
        """Test truncation style."""
        result = abbreviate("Department", style="truncation")
        # Truncation limits to 4 chars per word
        self.assertEqual(result, "Depa.")
    
    def test_abbreviate_empty(self):
        """Test empty input."""
        self.assertEqual(abbreviate(""), "")
    
    def test_abbreviate_single_word(self):
        """Test single word."""
        self.assertEqual(abbreviate("Test", style="acronym"), "T")


class TestDetect(unittest.TestCase):
    """Test abbreviation detection."""
    
    def test_detect_single(self):
        """Test detecting single abbreviation."""
        detected = detect("NASA is great.")
        self.assertEqual(len(detected), 1)
        self.assertEqual(detected[0].abbreviation, "NASA")
    
    def test_detect_multiple(self):
        """Test detecting multiple abbreviations."""
        detected = detect("NASA and FBI work with CIA.")
        self.assertEqual(len(detected), 3)
    
    def test_detect_no_abbreviations(self):
        """Test no abbreviations."""
        detected = detect("Hello world.")
        self.assertEqual(len(detected), 0)
    
    def test_detect_info(self):
        """Test detection info."""
        detected = detect("CEO announced changes.")
        if detected:
            info = detected[0]
            self.assertEqual(info.abbreviation, "CEO")
            self.assertEqual(info.expansion, "Chief Executive Officer")
            self.assertEqual(info.category, "business")


class TestGetInfo(unittest.TestCase):
    """Test abbreviation info."""
    
    def test_get_info_acronym(self):
        """Test acronym info."""
        info = get_info("NASA")
        self.assertIsNotNone(info)
        self.assertEqual(info.abbreviation, "NASA")
        self.assertEqual(info.expansion, "National Aeronautics and Space Administration")
        self.assertTrue(info.is_acronym)
        self.assertEqual(info.category, "organization")
    
    def test_get_info_initialism(self):
        """Test initialism info."""
        info = get_info("FBI")
        self.assertIsNotNone(info)
        self.assertTrue(info.is_initialism)
    
    def test_get_info_common(self):
        """Test common abbreviation info."""
        info = get_info("etc")
        self.assertIsNotNone(info)
        self.assertEqual(info.expansion, "et cetera")
        self.assertFalse(info.is_acronym)
    
    def test_get_info_state(self):
        """Test state info."""
        info = get_info("CA")
        self.assertIsNotNone(info)
        self.assertEqual(info.expansion, "California")
        self.assertEqual(info.category, "location")
    
    def test_get_info_unknown(self):
        """Test unknown abbreviation."""
        self.assertIsNone(get_info("XYZ"))


class TestIsAbbreviation(unittest.TestCase):
    """Test abbreviation check."""
    
    def test_is_known_abbreviation(self):
        """Test known abbreviations."""
        self.assertTrue(is_abbreviation("NASA"))
        self.assertTrue(is_abbreviation("CEO"))
        self.assertTrue(is_abbreviation("API"))
    
    def test_is_not_abbreviation(self):
        """Test non-abbreviations."""
        self.assertFalse(is_abbreviation("Hello"))
        self.assertFalse(is_abbreviation("World"))
        self.assertFalse(is_abbreviation(""))


class TestFindAbbreviationFor(unittest.TestCase):
    """Test finding abbreviation for expansion."""
    
    def test_find_for_known(self):
        """Test finding for known expansion."""
        self.assertEqual(find_abbreviation_for("National Aeronautics and Space Administration"), "NASA")
        self.assertEqual(find_abbreviation_for("Chief Executive Officer"), "CEO")
    
    def test_find_for_unknown(self):
        """Test finding for unknown expansion."""
        self.assertIsNone(find_abbreviation_for("Some Random Organization Name"))


class TestStateFunctions(unittest.TestCase):
    """Test state abbreviation functions."""
    
    def test_expand_state(self):
        """Test state expansion."""
        self.assertEqual(expand_state("CA"), "California")
        self.assertEqual(expand_state("NY"), "New York")
        self.assertEqual(expand_state("TX"), "Texas")
    
    def test_abbreviate_state(self):
        """Test state abbreviation."""
        self.assertEqual(abbreviate_state("California"), "CA")
        self.assertEqual(abbreviate_state("New York"), "NY")
        self.assertEqual(abbreviate_state("Texas"), "TX")
    
    def test_state_case_insensitive(self):
        """Test case insensitive."""
        self.assertEqual(expand_state("ca"), "California")
        self.assertEqual(abbreviate_state("california"), "CA")
    
    def test_unknown_state(self):
        """Test unknown state."""
        self.assertIsNone(expand_state("XX"))
        self.assertIsNone(abbreviate_state("Unknown State"))


class TestCountryFunctions(unittest.TestCase):
    """Test country abbreviation functions."""
    
    def test_expand_country(self):
        """Test country expansion."""
        self.assertEqual(expand_country("US"), "United States")
        self.assertEqual(expand_country("CN"), "China")
        self.assertEqual(expand_country("JP"), "Japan")
    
    def test_abbreviate_country(self):
        """Test country abbreviation."""
        self.assertEqual(abbreviate_country("United States"), "US")
        self.assertEqual(abbreviate_country("China"), "CN")
        self.assertEqual(abbreviate_country("Japan"), "JP")
    
    def test_unknown_country(self):
        """Test unknown country."""
        self.assertIsNone(expand_country("XX"))
        self.assertIsNone(abbreviate_country("Unknown Country"))


class TestCategories(unittest.TestCase):
    """Test category functions."""
    
    def test_get_categories(self):
        """Test getting categories."""
        categories = get_categories()
        self.assertIn("organization", categories)
        self.assertIn("technology", categories)
        self.assertIn("business", categories)
    
    def test_get_by_category(self):
        """Test getting by category."""
        tech = get_all_by_category("technology")
        self.assertIn("API", tech)
        self.assertIn("URL", tech)
        self.assertEqual(tech["API"], "Application Programming Interface")


class TestCustomAbbreviation(unittest.TestCase):
    """Test custom abbreviation."""
    
    def test_add_custom(self):
        """Test adding custom abbreviation."""
        add_custom("TESTCO", "Test Company Inc", "custom")
        self.assertEqual(expand("TESTCO"), "Test Company Inc")
        
        info = get_info("TESTCO")
        self.assertIsNotNone(info)
        self.assertEqual(info.category, "custom")


class TestCountAbbreviations(unittest.TestCase):
    """Test abbreviation counting."""
    
    def test_count_single(self):
        """Test counting single abbreviation."""
        counts = count_abbreviations("NASA is NASA and NASA again.")
        self.assertEqual(counts["NASA"], 3)
    
    def test_count_multiple(self):
        """Test counting multiple abbreviations."""
        counts = count_abbreviations("NASA and FBI and NASA")
        self.assertEqual(counts["NASA"], 2)
        self.assertEqual(counts["FBI"], 1)
    
    def test_count_empty(self):
        """Test empty text."""
        self.assertEqual(count_abbreviations(""), {})
    
    def test_count_no_abbreviations(self):
        """Test no abbreviations."""
        self.assertEqual(count_abbreviations("Hello world"), {})


class TestEdgeCases(unittest.TestCase):
    """Test edge cases."""
    
    def test_empty_input(self):
        """Test empty inputs."""
        self.assertEqual(expand_text(""), "")
        self.assertEqual(abbreviate(""), "")
        self.assertEqual(len(detect("")), 0)
    
    def test_whitespace_input(self):
        """Test whitespace."""
        self.assertEqual(abbreviate("   "), "")
    
    def test_special_characters(self):
        """Test special characters."""
        # R&D should work
        self.assertEqual(expand("R&D"), "Research and Development")
    
    def test_mixed_case_text(self):
        """Test mixed case in text."""
        result = expand_text("nasa and Nasa and NASA")
        self.assertIn("National Aeronautics and Space Administration", result)


if __name__ == '__main__':
    unittest.main(verbosity=2)