#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Fuzzy Logic Utilities Test Module
================================================
Test cases for fuzzy logic utilities.

Author: AllToolkit Contributors
License: MIT
"""

import math
import unittest
from mod import (
    # Membership functions
    triangular_membership, trapezoidal_membership, gaussian_membership,
    gaussian2_membership, sigmoid_membership, bell_membership,
    s_shape_membership, z_shape_membership, pi_shape_membership,
    singleton_membership, rectangular_membership, linear_membership,
    linear_down_membership,
    
    # Fuzzy operations
    fuzzy_union, fuzzy_intersection, fuzzy_complement, fuzzy_difference,
    fuzzy_and, fuzzy_or, fuzzy_not, fuzzy_implies,
    
    # Hedges
    apply_hedge, hedge_function, HedgeType,
    
    # Enums
    FuzzyOperator, DefuzzificationMethod,
    
    # Classes
    FuzzySet, LinguisticVariable, FuzzyRule, FuzzyInferenceSystem,
    
    # Convenience functions
    create_triangular_set, create_trapezoidal_set, create_gaussian_set,
    create_sigmoid_set, create_bell_set,
    create_temperature_variable, create_speed_variable, create_age_variable,
    create_risk_variable, create_temperature_controller,
)


class TestMembershipFunctions(unittest.TestCase):
    """Test membership functions."""
    
    def test_triangular_membership(self):
        """Test triangular membership function."""
        # Peak value
        self.assertEqual(triangular_membership(5, 0, 5, 10), 1.0)
        
        # Left side
        self.assertEqual(triangular_membership(2.5, 0, 5, 10), 0.5)
        self.assertEqual(triangular_membership(0, 0, 5, 10), 0.0)
        
        # Right side
        self.assertEqual(triangular_membership(7.5, 0, 5, 10), 0.5)
        self.assertEqual(triangular_membership(10, 0, 5, 10), 0.0)
        
        # Outside range
        self.assertEqual(triangular_membership(-1, 0, 5, 10), 0.0)
        self.assertEqual(triangular_membership(11, 0, 5, 10), 0.0)
    
    def test_triangular_membership_invalid_params(self):
        """Test triangular membership with invalid parameters."""
        with self.assertRaises(ValueError):
            triangular_membership(5, 10, 5, 0)  # a >= b
    
    def test_trapezoidal_membership(self):
        """Test trapezoidal membership function."""
        # Peak region
        self.assertEqual(trapezoidal_membership(5, 0, 3, 7, 10), 1.0)
        self.assertEqual(trapezoidal_membership(3, 0, 3, 7, 10), 1.0)
        self.assertEqual(trapezoidal_membership(7, 0, 3, 7, 10), 1.0)
        
        # Left side
        self.assertEqual(trapezoidal_membership(1.5, 0, 3, 7, 10), 0.5)
        self.assertEqual(trapezoidal_membership(0, 0, 3, 7, 10), 0.0)
        
        # Right side
        self.assertEqual(trapezoidal_membership(8.5, 0, 3, 7, 10), 0.5)
        self.assertEqual(trapezoidal_membership(10, 0, 3, 7, 10), 0.0)
    
    def test_gaussian_membership(self):
        """Test Gaussian membership function."""
        # Peak value
        self.assertEqual(gaussian_membership(5, 5, 2), 1.0)
        
        # Symmetric values
        self.assertAlmostEqual(gaussian_membership(3, 5, 2), gaussian_membership(7, 5, 2), 10)
        
        # Values 2 sigma away from center (should be exp(-1) of peak at 1 sigma)
        # At x=7 (2 units away with sigma=2), the formula gives exp(-(7-5)^2/(2*2^2)) = exp(-0.5)
        self.assertAlmostEqual(gaussian_membership(7, 5, 2), math.exp(-0.5), 10)
        
        # Invalid sigma
        with self.assertRaises(ValueError):
            gaussian_membership(5, 5, 0)
    
    def test_gaussian2_membership(self):
        """Test two-sided Gaussian membership function."""
        # Peak region
        self.assertEqual(gaussian2_membership(5, 0, 2, 10, 2), 1.0)
        
        # Left side
        self.assertEqual(gaussian2_membership(0, 0, 2, 10, 2), 1.0)
        self.assertLess(gaussian2_membership(-1, 0, 2, 10, 2), 1.0)
        
        # Right side
        self.assertEqual(gaussian2_membership(10, 0, 2, 10, 2), 1.0)
        self.assertLess(gaussian2_membership(11, 0, 2, 10, 2), 1.0)
    
    def test_sigmoid_membership(self):
        """Test sigmoid membership function."""
        # Inflection point
        self.assertEqual(sigmoid_membership(5, 2, 5), 0.5)
        
        # Rising sigmoid
        self.assertGreater(sigmoid_membership(7, 2, 5), 0.5)
        self.assertLess(sigmoid_membership(3, 2, 5), 0.5)
        
        # Falling sigmoid (negative slope)
        self.assertLess(sigmoid_membership(7, -2, 5), 0.5)
        self.assertGreater(sigmoid_membership(3, -2, 5), 0.5)
    
    def test_bell_membership(self):
        """Test generalized bell membership function."""
        # Peak value
        self.assertEqual(bell_membership(5, 2, 4, 5), 1.0)
        
        # Symmetric values
        self.assertEqual(bell_membership(3, 2, 4, 5), bell_membership(7, 2, 4, 5))
        
        # Invalid parameter
        with self.assertRaises(ValueError):
            bell_membership(5, 0, 4, 5)
    
    def test_s_shape_membership(self):
        """Test S-shaped membership function."""
        # Start
        self.assertEqual(s_shape_membership(0, 0, 10), 0.0)
        
        # End
        self.assertEqual(s_shape_membership(10, 0, 10), 1.0)
        
        # Middle
        self.assertEqual(s_shape_membership(5, 0, 10), 0.5)
        
        # Below first quartile
        self.assertEqual(s_shape_membership(2.5, 0, 10), 0.125)
        
        # Above third quartile
        self.assertEqual(s_shape_membership(7.5, 0, 10), 0.875)
    
    def test_z_shape_membership(self):
        """Test Z-shaped membership function."""
        # Start
        self.assertEqual(z_shape_membership(0, 0, 10), 1.0)
        
        # End
        self.assertEqual(z_shape_membership(10, 0, 10), 0.0)
        
        # Middle
        self.assertEqual(z_shape_membership(5, 0, 10), 0.5)
    
    def test_pi_shape_membership(self):
        """Test Pi-shaped membership function."""
        # Peak region
        self.assertEqual(pi_shape_membership(5, 0, 3, 7, 10), 1.0)
        
        # Outside
        self.assertEqual(pi_shape_membership(-1, 0, 3, 7, 10), 0.0)
        self.assertEqual(pi_shape_membership(11, 0, 3, 7, 10), 0.0)
    
    def test_singleton_membership(self):
        """Test singleton membership function."""
        self.assertEqual(singleton_membership(5, 5), 1.0)
        self.assertEqual(singleton_membership(5, 4), 0.0)
        self.assertEqual(singleton_membership(5.0, 5.0), 1.0)
    
    def test_rectangular_membership(self):
        """Test rectangular membership function."""
        self.assertEqual(rectangular_membership(5, 0, 10), 1.0)
        self.assertEqual(rectangular_membership(0, 0, 10), 1.0)
        self.assertEqual(rectangular_membership(10, 0, 10), 1.0)
        self.assertEqual(rectangular_membership(11, 0, 10), 0.0)
        self.assertEqual(rectangular_membership(-1, 0, 10), 0.0)
    
    def test_linear_membership(self):
        """Test linear membership function."""
        self.assertEqual(linear_membership(0, 0, 10), 0.0)
        self.assertEqual(linear_membership(10, 0, 10), 1.0)
        self.assertEqual(linear_membership(5, 0, 10), 0.5)
    
    def test_linear_down_membership(self):
        """Test linear down membership function."""
        self.assertEqual(linear_down_membership(0, 0, 10), 1.0)
        self.assertEqual(linear_down_membership(10, 0, 10), 0.0)
        self.assertEqual(linear_down_membership(5, 0, 10), 0.5)


class TestFuzzyOperations(unittest.TestCase):
    """Test fuzzy logical operations."""
    
    def test_fuzzy_union_max(self):
        """Test fuzzy union (MAX)."""
        self.assertEqual(fuzzy_union(0.3, 0.7, FuzzyOperator.MAX), 0.7)
        self.assertEqual(fuzzy_union(0.5, 0.5, FuzzyOperator.MAX), 0.5)
        self.assertEqual(fuzzy_union(0.0, 0.9, FuzzyOperator.MAX), 0.9)
    
    def test_fuzzy_union_sum(self):
        """Test fuzzy union (SUM)."""
        self.assertEqual(fuzzy_union(0.3, 0.7, FuzzyOperator.SUM), 1.0)
        self.assertEqual(fuzzy_union(0.2, 0.3, FuzzyOperator.SUM), 0.5)
    
    def test_fuzzy_intersection_min(self):
        """Test fuzzy intersection (MIN)."""
        self.assertEqual(fuzzy_intersection(0.3, 0.7, FuzzyOperator.MIN), 0.3)
        self.assertEqual(fuzzy_intersection(0.5, 0.5, FuzzyOperator.MIN), 0.5)
    
    def test_fuzzy_intersection_product(self):
        """Test fuzzy intersection (PRODUCT)."""
        self.assertEqual(fuzzy_intersection(0.3, 0.7, FuzzyOperator.PRODUCT), 0.21)
        self.assertEqual(fuzzy_intersection(0.5, 0.5, FuzzyOperator.PRODUCT), 0.25)
    
    def test_fuzzy_complement(self):
        """Test fuzzy complement."""
        self.assertEqual(fuzzy_complement(0.3), 0.7)
        self.assertEqual(fuzzy_complement(0.5), 0.5)
        self.assertEqual(fuzzy_complement(0.0), 1.0)
        self.assertEqual(fuzzy_complement(1.0), 0.0)
    
    def test_fuzzy_difference(self):
        """Test fuzzy difference."""
        self.assertEqual(fuzzy_difference(0.5, 0.3), min(0.5, 1 - 0.3))
    
    def test_fuzzy_and(self):
        """Test fuzzy AND for multiple values."""
        self.assertEqual(fuzzy_and(0.3, 0.5, 0.7), 0.3)
        self.assertEqual(fuzzy_and(0.8, 0.8), 0.8)
    
    def test_fuzzy_or(self):
        """Test fuzzy OR for multiple values."""
        self.assertEqual(fuzzy_or(0.3, 0.5, 0.7), 0.7)
        self.assertEqual(fuzzy_or(0.2, 0.2), 0.2)
    
    def test_fuzzy_not(self):
        """Test fuzzy NOT."""
        self.assertEqual(fuzzy_not(0.3), 0.7)
    
    def test_fuzzy_implies_mamdani(self):
        """Test fuzzy implication (Mamdani)."""
        self.assertEqual(fuzzy_implies(0.5, 0.8, "mamdani"), 0.5)
        self.assertEqual(fuzzy_implies(0.8, 0.5, "mamdani"), 0.5)
    
    def test_fuzzy_implies_larsen(self):
        """Test fuzzy implication (Larsen)."""
        self.assertEqual(fuzzy_implies(0.5, 0.8, "larsen"), 0.4)


class TestHedges(unittest.TestCase):
    """Test fuzzy hedges."""
    
    def test_very_hedge(self):
        """Test very hedge."""
        self.assertEqual(apply_hedge(0.5, HedgeType.VERY), 0.25)
        self.assertAlmostEqual(apply_hedge(0.8, HedgeType.VERY), 0.64, 10)
    
    def test_extremely_hedge(self):
        """Test extremely hedge."""
        self.assertEqual(apply_hedge(0.5, HedgeType.EXTREMELY), 0.125)
        self.assertEqual(apply_hedge(1.0, HedgeType.EXTREMELY), 1.0)
    
    def test_slightly_hedge(self):
        """Test slightly hedge."""
        self.assertAlmostEqual(apply_hedge(0.5, HedgeType.SLIGHTLY), math.sqrt(0.5), 10)
        self.assertEqual(apply_hedge(1.0, HedgeType.SLIGHTLY), 1.0)
    
    def test_plus_hedge(self):
        """Test plus hedge."""
        self.assertAlmostEqual(apply_hedge(0.5, HedgeType.PLUS), 0.5 ** 1.25, 10)
    
    def test_minus_hedge(self):
        """Test minus hedge."""
        self.assertAlmostEqual(apply_hedge(0.5, HedgeType.MINUS), 0.5 ** 0.75, 10)
    
    def test_hedge_function(self):
        """Test hedge function creation."""
        very = hedge_function(HedgeType.VERY)
        self.assertEqual(very(0.5), 0.25)


class TestFuzzySet(unittest.TestCase):
    """Test FuzzySet class."""
    
    def test_fuzzy_set_creation(self):
        """Test fuzzy set creation."""
        fs = create_triangular_set("medium", 20, 50, 80)
        self.assertEqual(fs.name, "medium")
        self.assertEqual(fs.membership(50), 1.0)
        self.assertEqual(fs.membership(35), 0.5)
    
    def test_fuzzy_set_callable(self):
        """Test fuzzy set callable interface."""
        fs = create_triangular_set("medium", 20, 50, 80)
        self.assertEqual(fs(50), 1.0)
    
    def test_fuzzy_set_complement(self):
        """Test fuzzy set complement."""
        fs = create_triangular_set("medium", 20, 50, 80)
        comp = fs.complement()
        self.assertEqual(comp.membership(50), 0.0)
        self.assertEqual(comp.membership(35), 0.5)
    
    def test_fuzzy_set_union(self):
        """Test fuzzy set union."""
        fs1 = create_triangular_set("low", 0, 25, 50)
        fs2 = create_triangular_set("high", 50, 75, 100)
        union = fs1.union_with(fs2)
        
        self.assertEqual(union.membership(25), 1.0)
        self.assertEqual(union.membership(75), 1.0)
        # Union takes max of both, at 50 one set ends at 0 and other starts at 0
        # So the union at 50 should be 0 (both are at boundary)
        self.assertEqual(union.membership(50), 0.0)
    
    def test_fuzzy_set_intersection(self):
        """Test fuzzy set intersection."""
        fs1 = create_triangular_set("a", 0, 30, 60)
        fs2 = create_triangular_set("b", 30, 60, 90)
        intersection = fs1.intersect_with(fs2)
        
        # At x=45, both sets should have membership 0.5
        self.assertEqual(intersection.membership(45), 0.5)
    
    def test_fuzzy_set_apply_hedge(self):
        """Test applying hedge to fuzzy set."""
        fs = create_triangular_set("medium", 20, 50, 80)
        very_fs = fs.apply_hedge(HedgeType.VERY)
        
        self.assertEqual(very_fs.membership(50), 1.0)
        self.assertEqual(very_fs.membership(35), 0.25)  # 0.5^2
    
    def test_alpha_cut(self):
        """Test alpha-cut."""
        fs = create_triangular_set("medium", 0, 50, 100)
        cut = fs.get_alpha_cut(0.5)
        
        # Should return interval where membership >= 0.5
        self.assertGreater(len(cut), 0)


class TestLinguisticVariable(unittest.TestCase):
    """Test LinguisticVariable class."""
    
    def test_create_temperature_variable(self):
        """Test temperature variable creation."""
        temp = create_temperature_variable(0, 100)
        
        # Test peak values
        self.assertEqual(temp.get_membership(50, "comfortable"), 1.0)
        self.assertEqual(temp.get_membership(100, "hot"), 1.0)
        
        # Test middle value
        self.assertEqual(temp.get_membership(50, "comfortable"), 1.0)
    
    def test_get_all_memberships(self):
        """Test getting all memberships."""
        temp = create_temperature_variable(0, 100)
        memberships = temp.get_all_memberships(25)
        
        self.assertIn("cold", memberships)
        self.assertIn("cool", memberships)
        self.assertIn("comfortable", memberships)
        self.assertIn("warm", memberships)
        self.assertIn("hot", memberships)
    
    def test_get_active_sets(self):
        """Test getting active sets."""
        temp = create_temperature_variable(0, 100)
        active = temp.get_active_sets(25, threshold=0.1)
        
        # Should have at least one active set
        self.assertGreater(len(active), 0)
    
    def test_create_speed_variable(self):
        """Test speed variable creation."""
        speed = create_speed_variable(0, 100)
        
        self.assertEqual(speed.get_membership(50, "medium"), 1.0)
    
    def test_create_age_variable(self):
        """Test age variable creation."""
        age = create_age_variable(0, 100)
        
        self.assertEqual(age.get_membership(50, "middle_aged"), 1.0)
    
    def test_create_risk_variable(self):
        """Test risk variable creation."""
        risk = create_risk_variable(0, 1)
        
        self.assertEqual(risk.get_membership(0.5, "medium"), 1.0)


class TestFuzzyRule(unittest.TestCase):
    """Test FuzzyRule class."""
    
    def test_rule_creation(self):
        """Test rule creation."""
        temp = create_temperature_variable(0, 100)
        fan = create_speed_variable(0, 100)
        
        rule = FuzzyRule(
            antecedent={"temperature": "hot"},
            consequent={"speed": "fast"},
            weight=1.0
        )
        
        inputs = {"temperature": temp}
        values = {"temperature": 90}  # High temperature
        
        strength = rule.evaluate_antecedent(inputs, values)
        self.assertGreater(strength, 0.3)  # Should have some firing strength


class TestFuzzyInferenceSystem(unittest.TestCase):
    """Test FuzzyInferenceSystem class."""
    
    def test_temperature_controller(self):
        """Test temperature controller."""
        controller = create_temperature_controller()
        
        # Test different temperatures
        results = controller.evaluate({'temperature': 15})
        self.assertIn('fan_speed', results)
        
        # Hot temperature should result in higher fan speed
        hot_result = controller.evaluate({'temperature': 85})
        cold_result = controller.evaluate({'temperature': 15})
        
        self.assertGreater(hot_result['fan_speed'], cold_result['fan_speed'])
    
    def test_custom_inference_system(self):
        """Test custom inference system creation."""
        # Create input variable
        temp = create_temperature_variable(0, 100)
        
        # Create output variable
        action = LinguisticVariable("action", universe_min=0, universe_max=100)
        action.add_fuzzy_set("decrease", lambda x: triangular_membership(x, 0, 0, 30))
        action.add_fuzzy_set("maintain", lambda x: triangular_membership(x, 30, 50, 70))
        action.add_fuzzy_set("increase", lambda x: triangular_membership(x, 70, 100, 100))
        
        # Create system
        system = FuzzyInferenceSystem("custom_controller")
        system.add_input_variable(temp)
        system.add_output_variable(action)
        
        # Add rules
        system.add_rule({"temperature": "cold"}, {"action": "increase"})
        system.add_rule({"temperature": "hot"}, {"action": "decrease"})
        
        # Test
        result = system.evaluate({'temperature': 10})
        self.assertIn('action', result)


class TestDefuzzification(unittest.TestCase):
    """Test defuzzification methods."""
    
    def test_centroid_defuzzification(self):
        """Test centroid defuzzification."""
        controller = create_temperature_controller()
        controller.defuzzification = DefuzzificationMethod.CENTROID
        
        result = controller.evaluate({'temperature': 50})
        self.assertIn('fan_speed', result)
    
    def test_mom_defuzzification(self):
        """Test mean of maximum defuzzification."""
        controller = create_temperature_controller()
        controller.defuzzification = DefuzzificationMethod.MOM
        
        result = controller.evaluate({'temperature': 50})
        self.assertIn('fan_speed', result)
    
    def test_different_defuzzification_methods(self):
        """Test different defuzzification methods give reasonable results."""
        controller = create_temperature_controller()
        
        methods = [
            DefuzzificationMethod.CENTROID,
            DefuzzificationMethod.BISECTOR,
            DefuzzificationMethod.MOM,
            DefuzzificationMethod.SOM,
            DefuzzificationMethod.LOM
        ]
        
        for method in methods:
            controller.defuzzification = method
            result = controller.evaluate({'temperature': 50})
            self.assertGreater(result['fan_speed'], 0)
            self.assertLess(result['fan_speed'], 100)


class TestConvenienceFunctions(unittest.TestCase):
    """Test convenience functions."""
    
    def test_create_triangular_set(self):
        """Test create triangular set."""
        fs = create_triangular_set("test", 0, 50, 100)
        self.assertEqual(fs.membership(50), 1.0)
    
    def test_create_trapezoidal_set(self):
        """Test create trapezoidal set."""
        fs = create_trapezoidal_set("test", 0, 20, 80, 100)
        self.assertEqual(fs.membership(50), 1.0)
    
    def test_create_gaussian_set(self):
        """Test create Gaussian set."""
        fs = create_gaussian_set("test", 50, 10)
        self.assertEqual(fs.membership(50), 1.0)
    
    def test_create_sigmoid_set(self):
        """Test create sigmoid set."""
        fs = create_sigmoid_set("test", 1, 50)
        self.assertEqual(fs.membership(50), 0.5)
    
    def test_create_bell_set(self):
        """Test create bell set."""
        fs = create_bell_set("test", 10, 2, 50)
        self.assertEqual(fs.membership(50), 1.0)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases."""
    
    def test_membership_out_of_range(self):
        """Test membership values outside universe."""
        fs = create_triangular_set("test", 20, 50, 80, 0, 100)
        self.assertEqual(fs.membership(-10), 0.0)
        self.assertEqual(fs.membership(110), 0.0)
    
    def test_zero_firing_strength(self):
        """Test rule with zero firing strength."""
        controller = create_temperature_controller()
        result = controller.evaluate({'temperature': -10})  # Outside range
        # Should still return some result
        self.assertIn('fan_speed', result)
    
    def test_empty_rule_evaluation(self):
        """Test empty antecedent."""
        rule = FuzzyRule(antecedent={}, consequent={"speed": "fast"})
        strength = rule.evaluate_antecedent({}, {})
        self.assertEqual(strength, 0.0)
    
    def test_multiple_rules_same_consequent(self):
        """Test multiple rules with same consequent."""
        temp = create_temperature_variable(0, 100)
        fan = create_speed_variable(0, 100)
        
        system = FuzzyInferenceSystem("test")
        system.add_input_variable(temp)
        system.add_output_variable(fan)
        
        # Add multiple rules for same output
        system.add_rule({"temperature": "cold"}, {"speed": "slow"})
        system.add_rule({"temperature": "cool"}, {"speed": "slow"})
        
        result = system.evaluate({'temperature': 20})
        self.assertIn('speed', result)


def run_tests():
    """Run all tests."""
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(__import__(__name__))
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    exit(0 if success else 1)