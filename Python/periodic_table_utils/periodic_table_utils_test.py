#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Periodic Table Utilities Test Suite
=================================================
Comprehensive tests for periodic_table_utils module.

Run with: python -m pytest periodic_table_utils_test.py -v
Or directly: python periodic_table_utils_test.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    # Enums
    ElementCategory,
    ElementState,
    
    # Data Classes
    Element,
    
    # Main functions
    get_element,
    get_elements_by_period,
    get_elements_by_group,
    get_elements_by_category,
    search_elements,
    calculate_molecular_weight,
    format_element_info,
    get_periodic_table_text,
    compare_elements,
    get_element_neighbors,
    get_common_compounds,
    
    # Constants
    ELEMENTS,
    SYMBOL_TO_NUMBER,
    NAME_TO_NUMBER,
)

import unittest


class TestGetElement(unittest.TestCase):
    """Test get_element function."""
    
    def test_by_atomic_number(self):
        """Test getting element by atomic number."""
        element = get_element(1)
        self.assertIsNotNone(element)
        self.assertEqual(element.symbol, 'H')
        self.assertEqual(element.name, '氢')
        
        element = get_element(79)
        self.assertEqual(element.symbol, 'Au')
        self.assertEqual(element.name, '金')
    
    def test_by_symbol(self):
        """Test getting element by symbol."""
        element = get_element('H')
        self.assertEqual(element.atomic_number, 1)
        
        element = get_element('Fe')
        self.assertEqual(element.atomic_number, 26)
        self.assertEqual(element.name, '铁')
        
        element = get_element('Au')
        self.assertEqual(element.atomic_number, 79)
    
    def test_by_name_chinese(self):
        """Test getting element by Chinese name."""
        element = get_element('氢')
        self.assertEqual(element.atomic_number, 1)
        
        element = get_element('铁')
        self.assertEqual(element.atomic_number, 26)
        
        element = get_element('金')
        self.assertEqual(element.atomic_number, 79)
    
    def test_by_name_english(self):
        """Test getting element by English name."""
        element = get_element('hydrogen')
        self.assertEqual(element.atomic_number, 1)
        
        element = get_element('iron')
        self.assertEqual(element.atomic_number, 26)
        
        element = get_element('gold')
        self.assertEqual(element.atomic_number, 79)
    
    def test_invalid_input(self):
        """Test getting element with invalid input."""
        # Invalid atomic number
        element = get_element(119)  # Beyond known elements
        self.assertIsNone(element)
        
        element = get_element(0)
        self.assertIsNone(element)
        
        # Invalid symbol
        element = get_element('Xx')
        self.assertIsNone(element)
        
        # Invalid name
        element = get_element('notanelement')
        self.assertIsNone(element)
    
    def test_all_elements_accessible(self):
        """Test that all 118 elements are accessible."""
        for i in range(1, 119):
            element = get_element(i)
            self.assertIsNotNone(element)
            self.assertEqual(element.atomic_number, i)


class TestElementData(unittest.TestCase):
    """Test Element dataclass."""
    
    def test_element_properties(self):
        """Test element properties."""
        h = get_element(1)
        
        self.assertEqual(h.atomic_number, 1)
        self.assertEqual(h.symbol, 'H')
        self.assertEqual(h.name, '氢')
        self.assertEqual(h.name_en, 'Hydrogen')
        self.assertEqual(h.atomic_mass, 1.008)
        self.assertEqual(h.category, ElementCategory.NONMETAL)
        self.assertEqual(h.period, 1)
        self.assertEqual(h.group, 1)
        self.assertEqual(h.state, ElementState.GAS)
    
    def test_element_masses(self):
        """Test atomic masses."""
        c = get_element(6)
        self.assertAlmostEqual(c.atomic_mass, 12.011, places=2)
        
        o = get_element(8)
        self.assertAlmostEqual(o.atomic_mass, 15.999, places=2)
        
        au = get_element(79)
        self.assertAlmostEqual(au.atomic_mass, 196.97, places=2)
    
    def test_element_categories(self):
        """Test element categories."""
        tests = [
            (1, ElementCategory.NONMETAL),        # H
            (3, ElementCategory.ALKALI_METAL),    # Li
            (4, ElementCategory.ALKALINE_EARTH_METAL),  # Be
            (26, ElementCategory.TRANSITION_METAL),  # Fe
            (5, ElementCategory.METALLOID),       # B
            (9, ElementCategory.HALOGEN),         # F
            (2, ElementCategory.NOBLE_GAS),       # He
            (57, ElementCategory.LANTHANIDE),     # La
            (92, ElementCategory.ACTINIDE),       # U
        ]
        
        for atomic_num, expected_category in tests:
            with self.subTest(atomic_num=atomic_num):
                element = get_element(atomic_num)
                self.assertEqual(element.category, expected_category)
    
    def test_element_states(self):
        """Test element states at room temperature."""
        tests = [
            (1, ElementState.GAS),      # H
            (2, ElementState.GAS),      # He
            (80, ElementState.LIQUID),  # Hg (mercury)
            (79, ElementState.SOLID),   # Au (gold)
            (35, ElementState.LIQUID),  # Br (bromine)
        ]
        
        for atomic_num, expected_state in tests:
            with self.subTest(atomic_num=atomic_num):
                element = get_element(atomic_num)
                self.assertEqual(element.state, expected_state)


class TestGetElementsByPeriod(unittest.TestCase):
    """Test get_elements_by_period function."""
    
    def test_period_1(self):
        """Test period 1 elements."""
        elements = get_elements_by_period(1)
        
        self.assertEqual(len(elements), 2)
        symbols = [e.symbol for e in elements]
        self.assertIn('H', symbols)
        self.assertIn('He', symbols)
    
    def test_period_2(self):
        """Test period 2 elements."""
        elements = get_elements_by_period(2)
        
        self.assertEqual(len(elements), 8)
        symbols = [e.symbol for e in elements]
        self.assertIn('Li', symbols)
        self.assertIn('C', symbols)
        self.assertIn('O', symbols)
        self.assertIn('Ne', symbols)
    
    def test_period_6(self):
        """Test period 6 elements (includes lanthanides)."""
        elements = get_elements_by_period(6)
        
        # Period 6 has more elements due to lanthanides
        self.assertTrue(len(elements) > 30)
    
    def test_invalid_period(self):
        """Test invalid period."""
        elements = get_elements_by_period(0)
        self.assertEqual(len(elements), 0)
        
        elements = get_elements_by_period(8)
        self.assertEqual(len(elements), 0)


class TestGetElementsByGroup(unittest.TestCase):
    """Test get_elements_by_group function."""
    
    def test_group_1_alkali_metals(self):
        """Test group 1 (alkali metals)."""
        elements = get_elements_by_group(1)
        
        symbols = [e.symbol for e in elements]
        self.assertIn('Li', symbols)
        self.assertIn('Na', symbols)
        self.assertIn('K', symbols)
        self.assertIn('Rb', symbols)
        self.assertIn('Cs', symbols)
        self.assertIn('Fr', symbols)
    
    def test_group_18_noble_gases(self):
        """Test group 18 (noble gases)."""
        elements = get_elements_by_group(18)
        
        symbols = [e.symbol for e in elements]
        self.assertIn('He', symbols)
        self.assertIn('Ne', symbols)
        self.assertIn('Ar', symbols)
        self.assertIn('Kr', symbols)
        self.assertIn('Xe', symbols)
        self.assertIn('Rn', symbols)
        self.assertIn('Og', symbols)
    
    def test_group_0_lanthanides_actinides(self):
        """Test group 0 (lanthanides and actinides)."""
        elements = get_elements_by_group(0)
        
        # Should include all lanthanides and actinides
        symbols = [e.symbol for e in elements]
        self.assertIn('La', symbols)
        self.assertIn('U', symbols)
    
    def test_invalid_group(self):
        """Test invalid group."""
        elements = get_elements_by_group(19)
        self.assertEqual(len(elements), 0)


class TestGetElementsByCategory(unittest.TestCase):
    """Test get_elements_by_category function."""
    
    def test_noble_gases(self):
        """Test getting noble gases."""
        elements = get_elements_by_category(ElementCategory.NOBLE_GAS)
        
        self.assertEqual(len(elements), 7)  # He, Ne, Ar, Kr, Xe, Rn, Og
        symbols = [e.symbol for e in elements]
        self.assertIn('He', symbols)
        self.assertIn('Ne', symbols)
    
    def test_alkali_metals(self):
        """Test getting alkali metals."""
        elements = get_elements_by_category(ElementCategory.ALKALI_METAL)
        
        self.assertEqual(len(elements), 6)  # Li, Na, K, Rb, Cs, Fr
    
    def test_transition_metals(self):
        """Test getting transition metals."""
        elements = get_elements_by_category(ElementCategory.TRANSITION_METAL)
        
        # Many transition metals
        self.assertTrue(len(elements) > 30)
        symbols = [e.symbol for e in elements]
        self.assertIn('Fe', symbols)
        self.assertIn('Cu', symbols)
        self.assertIn('Au', symbols)
    
    def test_lanthanides(self):
        """Test getting lanthanides."""
        elements = get_elements_by_category(ElementCategory.LANTHANIDE)
        
        self.assertEqual(len(elements), 15)
    
    def test_actinides(self):
        """Test getting actinides."""
        elements = get_elements_by_category(ElementCategory.ACTINIDE)
        
        self.assertEqual(len(elements), 15)


class TestSearchElements(unittest.TestCase):
    """Test search_elements function."""
    
    def test_search_by_symbol(self):
        """Test searching by symbol fragment."""
        results = search_elements('Fe')
        symbols = [e.symbol for e in results]
        self.assertIn('Fe', symbols)
    
    def test_search_by_name_chinese(self):
        """Test searching by Chinese name."""
        results = search_elements('氧')
        symbols = [e.symbol for e in results]
        self.assertIn('O', symbols)
    
    def test_search_by_name_english(self):
        """Test searching by English name fragment."""
        results = search_elements('gen')
        symbols = [e.symbol for e in results]
        self.assertIn('H', symbols)  # Hydrogen
        self.assertIn('O', symbols)  # Oxygen
        self.assertIn('N', symbols)  # Nitrogen
    
    def test_search_empty_results(self):
        """Test search with no matches."""
        results = search_elements('xyz')
        self.assertEqual(len(results), 0)


class TestCalculateMolecularWeight(unittest.TestCase):
    """Test calculate_molecular_weight function."""
    
    def test_water_h2o(self):
        """Test water molecular weight."""
        mass, composition = calculate_molecular_weight('H2O')
        
        # H: 1.008 * 2 = 2.016
        # O: 15.999 * 1 = 15.999
        # Total: ~18.015
        self.assertAlmostEqual(mass, 18.015, places=2)
        self.assertEqual(composition, {'H': 2, 'O': 1})
    
    def test_co2(self):
        """Test CO2 molecular weight."""
        mass, composition = calculate_molecular_weight('CO2')
        
        # C: 12.011, O: 15.999 * 2
        self.assertAlmostEqual(mass, 44.009, places=2)
        self.assertEqual(composition, {'C': 1, 'O': 2})
    
    def test_nacl(self):
        """Test NaCl molecular weight."""
        mass, composition = calculate_molecular_weight('NaCl')
        
        # Na: 22.990, Cl: 35.45
        self.assertAlmostEqual(mass, 58.44, places=2)
        self.assertEqual(composition, {'Na': 1, 'Cl': 1})
    
    def test_glucose_c6h12o6(self):
        """Test glucose molecular weight."""
        mass, composition = calculate_molecular_weight('C6H12O6')
        
        self.assertAlmostEqual(mass, 180.156, places=2)
        self.assertEqual(composition, {'C': 6, 'H': 12, 'O': 6})
    
    def test_sulfuric_acid_h2so4(self):
        """Test sulfuric acid molecular weight."""
        mass, composition = calculate_molecular_weight('H2SO4')
        
        # H: 1.008*2, S: 32.06, O: 15.999*4
        # Use approximate comparison
        self.assertAlmostEqual(mass, 98.07, places=1)
        self.assertEqual(composition, {'H': 2, 'S': 1, 'O': 4})
    
    def test_single_element(self):
        """Test single element."""
        mass, composition = calculate_molecular_weight('Fe')
        
        self.assertAlmostEqual(mass, 55.845, places=2)
        self.assertEqual(composition, {'Fe': 1})
    
    def test_complex_formula(self):
        """Test complex formula."""
        # Calcium carbonate: CaCO3
        mass, composition = calculate_molecular_weight('CaCO3')
        
        self.assertAlmostEqual(mass, 100.086, places=2)
        self.assertEqual(composition, {'Ca': 1, 'C': 1, 'O': 3})
    
    def test_invalid_formula(self):
        """Test invalid formula."""
        with self.assertRaises(ValueError):
            calculate_molecular_weight('H2Ox')  # Invalid element 'Ox'
        
        with self.assertRaises(ValueError):
            calculate_molecular_weight('123')  # Invalid
    
    def test_unknown_element(self):
        """Test formula with unknown element."""
        with self.assertRaises(ValueError):
            calculate_molecular_weight('Xx2')


class TestFormatElementInfo(unittest.TestCase):
    """Test format_element_info function."""
    
    def test_format_hydrogen(self):
        """Test formatting hydrogen."""
        h = get_element(1)
        info = format_element_info(h)
        
        self.assertIn('氢', info)
        self.assertIn('H', info)
        self.assertIn('原子序数', info)
        self.assertIn('1', info)
    
    def test_format_gold(self):
        """Test formatting gold."""
        au = get_element(79)
        info = format_element_info(au)
        
        self.assertIn('金', info)
        self.assertIn('Au', info)
        self.assertIn('79', info)
        self.assertIn('过渡金属', info)
    
    def test_format_helium(self):
        """Test formatting helium."""
        he = get_element(2)
        info = format_element_info(he)
        
        self.assertIn('氦', info)
        self.assertIn('He', info)
        self.assertIn('稀有气体', info)


class TestCompareElements(unittest.TestCase):
    """Test compare_elements function."""
    
    def test_compare_fe_cu(self):
        """Test comparing iron and copper."""
        result = compare_elements('Fe', 'Cu')
        
        self.assertEqual(result['元素1'], '铁 (Fe)')
        self.assertEqual(result['元素2'], '铜 (Cu)')
        
        # Atomic number difference
        self.assertEqual(result['原子序数差异'], 3)  # 29 - 26
        
        # Both are transition metals
        self.assertTrue(result['同类'])
        
        # Same period (period 4)
        self.assertTrue(result['同周期'])
        
        # Different groups (8 vs 11)
        self.assertFalse(result['同族'])
    
    def test_compare_li_na(self):
        """Test comparing lithium and sodium."""
        result = compare_elements('Li', 'Na')
        
        # Both are alkali metals
        self.assertTrue(result['同类'])
        
        # Same group (group 1)
        self.assertTrue(result['同族'])
        
        # Different periods
        self.assertFalse(result['同周期'])
    
    def test_compare_h_he(self):
        """Test comparing hydrogen and helium."""
        result = compare_elements('H', 'He')
        
        # Same period (period 1)
        self.assertTrue(result['同周期'])
        
        # Different groups and categories
        self.assertFalse(result['同族'])
        self.assertFalse(result['同类'])
    
    def test_compare_invalid_element(self):
        """Test comparing with invalid element."""
        with self.assertRaises(ValueError):
            compare_elements('Fe', 'Xx')


class TestGetElementNeighbors(unittest.TestCase):
    """Test get_element_neighbors function."""
    
    def test_carbon_neighbors(self):
        """Test carbon neighbors."""
        neighbors = get_element_neighbors('C')
        
        self.assertIsNotNone(neighbors['left'])
        self.assertEqual(neighbors['left'].symbol, 'B')
        
        self.assertIsNotNone(neighbors['right'])
        self.assertEqual(neighbors['right'].symbol, 'N')
        
        # Period 2 elements have no above
        self.assertIsNone(neighbors['above'])
        
        self.assertIsNotNone(neighbors['below'])
        self.assertEqual(neighbors['below'].symbol, 'Si')
    
    def test_iron_neighbors(self):
        """Test iron neighbors."""
        neighbors = get_element_neighbors('Fe')
        
        self.assertIsNotNone(neighbors['left'])
        self.assertEqual(neighbors['left'].symbol, 'Mn')
        
        self.assertIsNotNone(neighbors['right'])
        self.assertEqual(neighbors['right'].symbol, 'Co')
        
        # Period 4 elements - check below (period 5)
        self.assertIsNotNone(neighbors['below'])
        self.assertEqual(neighbors['below'].symbol, 'Ru')
    
    def test_first_element(self):
        """Test hydrogen (first element) neighbors."""
        neighbors = get_element_neighbors('H')
        
        # No left, no above
        self.assertIsNone(neighbors['left'])
        self.assertIsNone(neighbors['above'])
        
        # Has right (He in same period, but different group structure)
        # Has below (Li in group 1, period 2)
        self.assertIsNotNone(neighbors['below'])
        self.assertEqual(neighbors['below'].symbol, 'Li')
    
    def test_invalid_element(self):
        """Test invalid element neighbors."""
        with self.assertRaises(ValueError):
            get_element_neighbors('Xx')


class TestGetCommonCompounds(unittest.TestCase):
    """Test get_common_compounds function."""
    
    def test_hydrogen_compounds(self):
        """Test hydrogen compounds."""
        compounds = get_common_compounds('H')
        
        self.assertIn('H2O', compounds)
        self.assertIn('H2', compounds)
        self.assertIn('HCl', compounds)
    
    def test_iron_compounds(self):
        """Test iron compounds."""
        compounds = get_common_compounds('Fe')
        
        self.assertIn('Fe2O3', compounds)
        self.assertIn('Fe3O4', compounds)
        self.assertIn('FeSO4', compounds)
    
    def test_carbon_compounds(self):
        """Test carbon compounds."""
        compounds = get_common_compounds('C')
        
        self.assertIn('CO2', compounds)
        self.assertIn('CH4', compounds)
        self.assertIn('C6H12O6', compounds)
    
    def test_element_without_compounds(self):
        """Test element without common compound data."""
        compounds = get_common_compounds('Og')  # Oganesson
        
        # Might be empty for very new elements
        self.assertIsInstance(compounds, list)
    
    def test_invalid_element(self):
        """Test invalid element."""
        compounds = get_common_compounds('Xx')
        
        self.assertEqual(len(compounds), 0)


class TestConstants(unittest.TestCase):
    """Test constants and mappings."""
    
    def test_elements_dict(self):
        """Test ELEMENTS dictionary."""
        self.assertEqual(len(ELEMENTS), 118)
        
        # Check first element
        self.assertEqual(ELEMENTS[1].symbol, 'H')
        
        # Check last element
        self.assertEqual(ELEMENTS[118].symbol, 'Og')
    
    def test_symbol_to_number(self):
        """Test SYMBOL_TO_NUMBER mapping."""
        self.assertEqual(SYMBOL_TO_NUMBER['H'], 1)
        self.assertEqual(SYMBOL_TO_NUMBER['C'], 6)
        self.assertEqual(SYMBOL_TO_NUMBER['Au'], 79)
        
        self.assertEqual(len(SYMBOL_TO_NUMBER), 118)
    
    def test_name_to_number(self):
        """Test NAME_TO_NUMBER mapping."""
        # Chinese names
        self.assertEqual(NAME_TO_NUMBER['氢'], 1)
        self.assertEqual(NAME_TO_NUMBER['铁'], 26)
        
        # English names
        self.assertEqual(NAME_TO_NUMBER['hydrogen'], 1)
        self.assertEqual(NAME_TO_NUMBER['iron'], 26)


class TestGetPeriodicTableText(unittest.TestCase):
    """Test get_periodic_table_text function."""
    
    def test_compact_format(self):
        """Test compact periodic table format."""
        table = get_periodic_table_text(compact=True)
        
        self.assertIn('H', table)
        self.assertIn('He', table)
        self.assertIn('Li', table)
        self.assertIn('Fe', table)
        self.assertIn('Au', table)


class TestElementPhysicalProperties(unittest.TestCase):
    """Test element physical properties."""
    
    def test_melting_points(self):
        """Test melting points."""
        h = get_element(1)
        self.assertAlmostEqual(h.melting_point, 14.01, places=2)
        
        au = get_element(79)
        self.assertAlmostEqual(au.melting_point, 1337.33, places=2)
    
    def test_boiling_points(self):
        """Test boiling points."""
        h = get_element(1)
        self.assertAlmostEqual(h.boiling_point, 20.28, places=2)
    
    def test_densities(self):
        """Test densities."""
        au = get_element(79)
        self.assertAlmostEqual(au.density, 19.282, places=2)
        
        # Gold is very dense
        self.assertTrue(au.density > 10)
    
    def test_discovery_year(self):
        """Test discovery years."""
        h = get_element(1)
        self.assertEqual(h.discovery_year, 1766)
        
        # Ancient elements have no discovery year
        au = get_element(79)
        self.assertIsNone(au.discovery_year)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases."""
    
    def test_first_element(self):
        """Test first element (hydrogen)."""
        h = get_element(1)
        
        self.assertEqual(h.atomic_number, 1)
        self.assertEqual(h.period, 1)
        self.assertEqual(h.group, 1)
    
    def test_last_element(self):
        """Test last known element (oganesson)."""
        og = get_element(118)
        
        self.assertEqual(og.atomic_number, 118)
        self.assertEqual(og.symbol, 'Og')
        self.assertEqual(og.category, ElementCategory.NOBLE_GAS)
    
    def test_case_insensitivity(self):
        """Test case insensitive lookups."""
        # Name lookups are case insensitive
        self.assertEqual(get_element('IRON').atomic_number, 26)
        self.assertEqual(get_element('iron').atomic_number, 26)
        self.assertEqual(get_element('Iron').atomic_number, 26)
        
        # Symbol lookups require proper case
        self.assertEqual(get_element('Fe').atomic_number, 26)
        
        # Chinese names work directly
        self.assertEqual(get_element('铁').atomic_number, 26)
    
    def test_spaces_in_name(self):
        """Test names with spaces."""
        # Should work without spaces
        element = get_element('noblegas')
        # This should return None since there's no element named "noblegas"
        self.assertIsNone(element)


if __name__ == '__main__':
    unittest.main(verbosity=2)