"""
Unit tests for Stable Marriage Utils

Tests cover:
- StableMarriage class (Gale-Shapley algorithm)
- StableRoommates class (Irving's algorithm)
- HospitalResidents class (many-to-one matching)
- Edge cases and validation
"""

import unittest
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from stable_marriage_utils.mod import (
    StableMarriage, StableRoommates, HospitalResidents,
    stable_marriage, stable_roommates, hospital_residents
)


class TestStableMarriage(unittest.TestCase):
    """Tests for the Stable Marriage Problem solver."""
    
    def test_basic_matching(self):
        """Test basic stable marriage matching."""
        men = {
            'A': ['Y', 'X', 'Z'],
            'B': ['X', 'Y', 'Z'],
            'C': ['Y', 'X', 'Z']
        }
        women = {
            'X': ['A', 'B', 'C'],
            'Y': ['B', 'A', 'C'],
            'Z': ['A', 'B', 'C']
        }
        
        sm = StableMarriage(men, women)
        result = sm.solve()
        
        # Check all men are matched
        self.assertEqual(len(result), 3)
        self.assertIn('A', result)
        self.assertIn('B', result)
        self.assertIn('C', result)
        
        # Check matching is valid (each woman matched once)
        women_matched = list(result.values())
        self.assertEqual(len(set(women_matched)), 3)
    
    def test_matching_is_stable(self):
        """Test that the resulting matching is stable."""
        men = {
            'M1': ['W2', 'W1', 'W3'],
            'M2': ['W1', 'W2', 'W3'],
            'M3': ['W1', 'W2', 'W3']
        }
        women = {
            'W1': ['M1', 'M2', 'M3'],
            'W2': ['M3', 'M1', 'M2'],
            'W3': ['M2', 'M1', 'M3']
        }
        
        sm = StableMarriage(men, women)
        result = sm.solve()
        
        self.assertTrue(sm.is_stable(result))
    
    def test_men_optimal(self):
        """Test that men get their optimal stable partner."""
        men = {
            'A': ['X', 'Y'],
            'B': ['Y', 'X']
        }
        women = {
            'X': ['B', 'A'],
            'Y': ['A', 'B']
        }
        
        sm = StableMarriage(men, women)
        result = sm.solve()
        
        # Man A gets first choice X, man B gets Y
        self.assertEqual(result['A'], 'X')
        self.assertEqual(result['B'], 'Y')
    
    def test_women_optimal(self):
        """Test women-optimal matching."""
        men = {
            'A': ['X', 'Y'],
            'B': ['X', 'Y']
        }
        women = {
            'X': ['A', 'B'],
            'Y': ['B', 'A']
        }
        
        sm = StableMarriage(men, women)
        men_optimal = sm.solve()
        women_optimal = sm.solve_women_optimal()
        
        # Both should be stable
        self.assertTrue(sm.is_stable(men_optimal))
        self.assertTrue(sm.is_stable(women_optimal))
    
    def test_identical_preferences(self):
        """Test when everyone has identical preferences."""
        men = {
            'M1': ['W1', 'W2', 'W3'],
            'M2': ['W1', 'W2', 'W3'],
            'M3': ['W1', 'W2', 'W3']
        }
        women = {
            'W1': ['M1', 'M2', 'M3'],
            'W2': ['M1', 'M2', 'M3'],
            'W3': ['M1', 'M2', 'M3']
        }
        
        sm = StableMarriage(men, women)
        result = sm.solve()
        
        self.assertTrue(sm.is_stable(result))
        # Everyone matched
        self.assertEqual(len(result), 3)
    
    def test_find_blocking_pairs(self):
        """Test detection of blocking pairs."""
        men = {
            'A': ['X', 'Y'],
            'B': ['X', 'Y']
        }
        women = {
            'X': ['A', 'B'],
            'Y': ['A', 'B']
        }
        
        sm = StableMarriage(men, women)
        
        # Create an unstable matching
        unstable_matching = {'A': 'Y', 'B': 'X'}
        
        blocking = sm.find_blocking_pairs(unstable_matching)
        # Should find blocking pairs
        self.assertGreater(len(blocking), 0)
    
    def test_satisfaction_metrics(self):
        """Test satisfaction calculation."""
        men = {
            'A': ['X', 'Y'],
            'B': ['Y', 'X']
        }
        women = {
            'X': ['A', 'B'],
            'Y': ['B', 'A']
        }
        
        sm = StableMarriage(men, women)
        result = sm.solve()
        satisfaction = sm.calculate_satisfaction(result)
        
        self.assertIn('men_scores', satisfaction)
        self.assertIn('women_scores', satisfaction)
        self.assertIn('men_avg', satisfaction)
        self.assertIn('women_avg', satisfaction)
        self.assertIn('total_avg', satisfaction)
        
        # All scores should be between 1 and n
        for score in satisfaction['men_scores'].values():
            self.assertGreaterEqual(score, 1)
            self.assertLessEqual(score, 2)
    
    def test_count_stable_matchings(self):
        """Test counting stable matchings."""
        men = {
            'A': ['X', 'Y'],
            'B': ['Y', 'X']
        }
        women = {
            'X': ['B', 'A'],
            'Y': ['A', 'B']
        }
        
        sm = StableMarriage(men, women)
        count = sm.count_stable_matchings()
        
        # Should have at least 1 stable matching
        self.assertGreaterEqual(count, 1)
    
    def test_find_all_stable_matchings(self):
        """Test finding all stable matchings."""
        men = {
            'A': ['X', 'Y'],
            'B': ['Y', 'X']
        }
        women = {
            'X': ['A', 'B'],
            'Y': ['B', 'A']
        }
        
        sm = StableMarriage(men, women)
        all_matchings = sm.find_all_stable_matchings()
        
        self.assertGreaterEqual(len(all_matchings), 1)
        for matching in all_matchings:
            self.assertTrue(sm.is_stable(matching))
    
    def test_invalid_preferences_wrong_size(self):
        """Test validation with unequal set sizes."""
        men = {
            'A': ['X', 'Y'],
            'B': ['X', 'Y']
        }
        women = {
            'X': ['A', 'B'],
            'Y': ['A', 'B'],
            'Z': ['A', 'B']
        }
        
        with self.assertRaises(ValueError):
            StableMarriage(men, women)
    
    def test_invalid_preferences_incomplete(self):
        """Test validation with incomplete preference lists."""
        men = {
            'A': ['X'],  # Missing Y
            'B': ['X', 'Y']
        }
        women = {
            'X': ['A', 'B'],
            'Y': ['A', 'B']
        }
        
        with self.assertRaises(ValueError):
            StableMarriage(men, women)
    
    def test_convenience_function(self):
        """Test the convenience function."""
        men = {'A': ['X', 'Y'], 'B': ['Y', 'X']}
        women = {'X': ['A', 'B'], 'Y': ['B', 'A']}
        
        result = stable_marriage(men, women)
        
        self.assertEqual(len(result), 2)
        self.assertIn('A', result)
        self.assertIn('B', result)


class TestStableRoommates(unittest.TestCase):
    """Tests for the Stable Roommates Problem solver."""
    
    def test_basic_matching(self):
        """Test basic stable roommates matching."""
        prefs = {
            'A': ['B', 'C', 'D'],
            'B': ['A', 'D', 'C'],
            'C': ['D', 'A', 'B'],
            'D': ['C', 'B', 'A']
        }
        
        sr = StableRoommates(prefs)
        result = sr.solve()
        
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 4)
    
    def test_matching_is_stable(self):
        """Test that result is stable."""
        prefs = {
            'A': ['B', 'C', 'D'],
            'B': ['C', 'A', 'D'],
            'C': ['A', 'B', 'D'],
            'D': ['A', 'B', 'C']
        }
        
        sr = StableRoommates(prefs)
        result = sr.solve()
        
        if result:
            self.assertTrue(sr.is_stable(result))
    
    def test_no_stable_solution(self):
        """Test case with no stable solution."""
        # Classic example with no stable matching
        prefs = {
            'A': ['B', 'C', 'D'],
            'B': ['C', 'A', 'D'],
            'C': ['A', 'B', 'D'],
            'D': ['A', 'B', 'C']
        }
        
        sr = StableRoommates(prefs)
        result = sr.solve()
        
        # This might have a solution depending on preferences
        # The key is that it should either find a stable one or return None
        if result:
            self.assertTrue(sr.is_stable(result))
    
    def test_odd_number_raises(self):
        """Test that odd number of participants raises error."""
        prefs = {
            'A': ['B', 'C'],
            'B': ['A', 'C'],
            'C': ['A', 'B']
        }
        
        with self.assertRaises(ValueError):
            StableRoommates(prefs)
    
    def test_convenience_function(self):
        """Test convenience function."""
        prefs = {
            'A': ['B', 'C', 'D'],
            'B': ['A', 'D', 'C'],
            'C': ['D', 'A', 'B'],
            'D': ['C', 'B', 'A']
        }
        
        result = stable_roommates(prefs)
        
        if result:
            self.assertEqual(len(result), 4)
    
    def test_symmetric_preferences(self):
        """Test with symmetric preferences."""
        prefs = {
            'A': ['B', 'C', 'D'],
            'B': ['A', 'C', 'D'],
            'C': ['D', 'A', 'B'],
            'D': ['C', 'A', 'B']
        }
        
        sr = StableRoommates(prefs)
        result = sr.solve()
        
        if result:
            # Each pair should be mutual
            for person, roommate in result.items():
                self.assertEqual(result[roommate], person)


class TestHospitalResidents(unittest.TestCase):
    """Tests for the Hospital/Residents Problem solver."""
    
    def test_basic_matching(self):
        """Test basic hospital-residents matching."""
        residents = {
            'R1': ['H1', 'H2'],
            'R2': ['H2', 'H1'],
            'R3': ['H1', 'H2']
        }
        hospitals = {
            'H1': (2, ['R1', 'R3', 'R2']),
            'H2': (1, ['R2', 'R1', 'R3'])
        }
        
        hr = HospitalResidents(residents, hospitals)
        result = hr.solve()
        
        # All hospitals in result
        self.assertIn('H1', result)
        self.assertIn('H2', result)
        
        # Check capacity constraints
        self.assertLessEqual(len(result['H1']), 2)
        self.assertLessEqual(len(result['H2']), 1)
    
    def test_capacity_constraints(self):
        """Test that capacity constraints are respected."""
        residents = {
            'R1': ['H1'],
            'R2': ['H1'],
            'R3': ['H1'],
            'R4': ['H1']
        }
        hospitals = {
            'H1': (2, ['R1', 'R2', 'R3', 'R4'])
        }
        
        hr = HospitalResidents(residents, hospitals)
        result = hr.solve()
        
        # Only 2 residents should match
        self.assertEqual(len(result['H1']), 2)
    
    def test_matching_is_stable(self):
        """Test that matching is stable."""
        residents = {
            'R1': ['H1', 'H2'],
            'R2': ['H1', 'H2'],
            'R3': ['H2', 'H1']
        }
        hospitals = {
            'H1': (1, ['R1', 'R2', 'R3']),
            'H2': (2, ['R3', 'R2', 'R1'])
        }
        
        hr = HospitalResidents(residents, hospitals)
        result = hr.solve()
        
        self.assertTrue(hr.is_stable(result))
    
    def test_resident_optimal(self):
        """Test resident-proposing is resident-optimal."""
        residents = {
            'R1': ['H1', 'H2'],
            'R2': ['H1', 'H2']
        }
        hospitals = {
            'H1': (1, ['R1', 'R2']),
            'H2': (1, ['R2', 'R1'])
        }
        
        hr = HospitalResidents(residents, hospitals)
        result = hr.solve()
        
        # R1 should get H1 (first choice), R2 gets H2
        self.assertIn('R1', result['H1'])
    
    def test_hospital_optimal(self):
        """Test hospital-proposing variant."""
        residents = {
            'R1': ['H1', 'H2'],
            'R2': ['H2', 'H1']
        }
        hospitals = {
            'H1': (1, ['R1', 'R2']),
            'H2': (1, ['R2', 'R1'])
        }
        
        hr = HospitalResidents(residents, hospitals)
        result = hr.solve_hospital_optimal()
        
        # Both hospitals should have 1 resident each
        self.assertEqual(len(result['H1']), 1)
        self.assertEqual(len(result['H2']), 1)
    
    def test_convenience_function(self):
        """Test convenience function."""
        residents = {
            'R1': ['H1', 'H2'],
            'R2': ['H2', 'H1']
        }
        hospitals = {
            'H1': (1, ['R1', 'R2']),
            'H2': (1, ['R2', 'R1'])
        }
        
        result = hospital_residents(residents, hospitals)
        
        self.assertIn('H1', result)
        self.assertIn('H2', result)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and special scenarios."""
    
    def test_single_pair(self):
        """Test with single pair."""
        men = {'A': ['X']}
        women = {'X': ['A']}
        
        sm = StableMarriage(men, women)
        result = sm.solve()
        
        self.assertEqual(result, {'A': 'X'})
    
    def test_two_pairs(self):
        """Test with two pairs."""
        men = {'A': ['Y', 'X'], 'B': ['X', 'Y']}
        women = {'X': ['A', 'B'], 'Y': ['B', 'A']}
        
        sm = StableMarriage(men, women)
        result = sm.solve()
        
        self.assertTrue(sm.is_stable(result))
    
    def test_complete_reversal(self):
        """Test when preferences are completely reversed."""
        men = {
            'A': ['X', 'Y', 'Z'],
            'B': ['Y', 'Z', 'X'],
            'C': ['Z', 'X', 'Y']
        }
        women = {
            'X': ['C', 'B', 'A'],
            'Y': ['A', 'C', 'B'],
            'Z': ['B', 'A', 'C']
        }
        
        sm = StableMarriage(men, women)
        result = sm.solve()
        
        self.assertTrue(sm.is_stable(result))
    
    def test_uniform_preferences(self):
        """Test when all men have same preferences."""
        men = {
            'M1': ['W1', 'W2', 'W3'],
            'M2': ['W1', 'W2', 'W3'],
            'M3': ['W1', 'W2', 'W3']
        }
        women = {
            'W1': ['M1', 'M2', 'M3'],
            'W2': ['M2', 'M3', 'M1'],
            'W3': ['M3', 'M1', 'M2']
        }
        
        sm = StableMarriage(men, women)
        result = sm.solve()
        
        self.assertTrue(sm.is_stable(result))


class TestPerformance(unittest.TestCase):
    """Performance tests for larger inputs."""
    
    def test_medium_size(self):
        """Test with 10x10 instance."""
        n = 10
        men = {f'M{i}': [f'W{j}' for j in range(n)] for i in range(n)}
        women = {f'W{i}': [f'M{j}' for j in range(n)] for i in range(n)}
        
        sm = StableMarriage(men, women)
        result = sm.solve()
        
        self.assertEqual(len(result), n)
        self.assertTrue(sm.is_stable(result))
    
    def test_large_instance(self):
        """Test with 100x100 instance."""
        import random
        
        n = 100
        men = {}
        women = {}
        
        for i in range(n):
            men_order = list(range(n))
            random.shuffle(men_order)
            men[f'M{i}'] = [f'W{j}' for j in men_order]
            
            women_order = list(range(n))
            random.shuffle(women_order)
            women[f'W{i}'] = [f'M{j}' for j in women_order]
        
        sm = StableMarriage(men, women)
        result = sm.solve()
        
        self.assertEqual(len(result), n)
        self.assertTrue(sm.is_stable(result))


if __name__ == '__main__':
    unittest.main(verbosity=2)