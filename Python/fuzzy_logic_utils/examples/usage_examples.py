#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Fuzzy Logic Utilities Examples
=============================================
Usage examples for fuzzy logic utilities.

Author: AllToolkit Contributors
License: MIT
"""

import sys
sys.path.insert(0, '..')
from mod import (
    # Membership functions
    triangular_membership, trapezoidal_membership, gaussian_membership,
    sigmoid_membership, bell_membership,
    s_shape_membership, z_shape_membership,
    
    # Fuzzy operations
    fuzzy_union, fuzzy_intersection, fuzzy_complement,
    fuzzy_and, fuzzy_or, fuzzy_not,
    
    # Hedges
    apply_hedge, HedgeType,
    
    # Classes
    FuzzySet, LinguisticVariable, FuzzyRule, FuzzyInferenceSystem,
    
    # Enums
    FuzzyOperator, DefuzzificationMethod,
    
    # Convenience functions
    create_triangular_set, create_gaussian_set,
    create_temperature_variable, create_speed_variable,
    create_age_variable, create_risk_variable,
    create_temperature_controller,
)


def example_membership_functions():
    """
    Example 1: Basic membership functions.
    
    Demonstrates various membership functions and their shapes.
    """
    print("=" * 60)
    print("Example 1: Membership Functions")
    print("=" * 60)
    
    print("\n1.1 Triangular Membership Function:")
    print("    Triangular(0, 50, 100) - Peak at 50")
    for x in [0, 25, 50, 75, 100]:
        mu = triangular_membership(x, 0, 50, 100)
        print(f"    μ({x}) = {mu:.4f}")
    
    print("\n1.2 Trapezoidal Membership Function:")
    print("    Trapezoidal(0, 20, 80, 100) - Flat region [20, 80]")
    for x in [0, 10, 20, 50, 80, 90, 100]:
        mu = trapezoidal_membership(x, 0, 20, 80, 100)
        print(f"    μ({x}) = {mu:.4f}")
    
    print("\n1.3 Gaussian Membership Function:")
    print("    Gaussian(center=50, sigma=15)")
    for x in [20, 35, 50, 65, 80]:
        mu = gaussian_membership(x, 50, 15)
        print(f"    μ({x}) = {mu:.4f}")
    
    print("\n1.4 Sigmoid Membership Function:")
    print("    Sigmoid(a=0.5, c=50) - Rising")
    for x in [30, 40, 50, 60, 70]:
        mu = sigmoid_membership(x, 0.5, 50)
        print(f"    μ({x}) = {mu:.4f}")
    
    print("\n1.5 Bell Membership Function:")
    print("    Bell(a=20, b=2, c=50)")
    for x in [10, 30, 50, 70, 90]:
        mu = bell_membership(x, 20, 2, 50)
        print(f"    μ({x}) = {mu:.4f}")
    
    print("\n1.6 S-Shaped and Z-Shaped Functions:")
    print("    S-Shape(0, 100) - Rising")
    for x in [0, 25, 50, 75, 100]:
        mu = s_shape_membership(x, 0, 100)
        print(f"    μ({x}) = {mu:.4f}")
    
    print("\n    Z-Shape(0, 100) - Falling")
    for x in [0, 25, 50, 75, 100]:
        mu = z_shape_membership(x, 0, 100)
        print(f"    μ({x}) = {mu:.4f}")


def example_fuzzy_operations():
    """
    Example 2: Fuzzy logical operations.
    
    Demonstrates fuzzy AND, OR, NOT operations.
    """
    print("\n" + "=" * 60)
    print("Example 2: Fuzzy Logical Operations")
    print("=" * 60)
    
    print("\n2.1 Basic Operations:")
    a = 0.3
    b = 0.7
    
    print(f"    a = {a}, b = {b}")
    print(f"    AND (min): {fuzzy_intersection(a, b):.4f}")
    print(f"    OR  (max): {fuzzy_union(a, b):.4f}")
    print(f"    NOT a:     {fuzzy_complement(a):.4f}")
    print(f"    NOT b:     {fuzzy_complement(b):.4f}")
    
    print("\n2.2 Alternative Operators:")
    print("    Intersection:")
    print(f"      MIN:       {fuzzy_intersection(a, b, FuzzyOperator.MIN):.4f}")
    print(f"      PRODUCT:   {fuzzy_intersection(a, b, FuzzyOperator.PRODUCT):.4f}")
    print(f"      BOUND_DIFF: {fuzzy_intersection(a, b, FuzzyOperator.BOUND_DIFF):.4f}")
    
    print("\n    Union:")
    print(f"      MAX:       {fuzzy_union(a, b, FuzzyOperator.MAX):.4f}")
    print(f"      SUM:       {fuzzy_union(a, b, FuzzyOperator.SUM):.4f}")
    
    print("\n2.3 Multiple Values:")
    values = [0.2, 0.5, 0.8, 0.9]
    print(f"    Values: {values}")
    print(f"    AND all: {fuzzy_and(*values):.4f}")
    print(f"    OR  all: {fuzzy_or(*values):.4f}")


def example_hedges():
    """
    Example 3: Fuzzy hedges (modifiers).
    
    Demonstrates how hedges modify membership values.
    """
    print("\n" + "=" * 60)
    print("Example 3: Fuzzy Hedges (Modifiers)")
    print("=" * 60)
    
    print("\n3.1 Applying Hedges to Membership Values:")
    original = 0.5
    
    print(f"    Original membership: {original}")
    print(f"    VERY:      {apply_hedge(original, HedgeType.VERY):.4f}   (μ²)")
    print(f"    EXTREMELY: {apply_hedge(original, HedgeType.EXTREMELY):.4f} (μ³)")
    print(f"    SLIGHTLY:  {apply_hedge(original, HedgeType.SLIGHTLY):.4f} (√μ)")
    print(f"    PLUS:      {apply_hedge(original, HedgeType.PLUS):.4f}  (μ^1.25)")
    print(f"    MINUS:     {apply_hedge(original, HedgeType.MINUS):.4f} (μ^0.75)")
    
    print("\n3.2 Real-world Usage:")
    print("    Linguistic interpretation:")
    print(f"      'Temperature is 50% warm'")
    print(f"      'Temperature is very warm'     → {apply_hedge(0.5, HedgeType.VERY):.2%}")
    print(f"      'Temperature is extremely warm' → {apply_hedge(0.5, HedgeType.EXTREMELY):.2%}")
    print(f"      'Temperature is slightly warm'  → {apply_hedge(0.5, HedgeType.SLIGHTLY):.2%}")


def example_fuzzy_sets():
    """
    Example 4: Fuzzy sets.
    
    Demonstrates creating and manipulating fuzzy sets.
    """
    print("\n" + "=" * 60)
    print("Example 4: Fuzzy Sets")
    print("=" * 60)
    
    print("\n4.1 Creating Fuzzy Sets:")
    
    # Create fuzzy sets
    low = create_triangular_set("low", 0, 0, 50)
    medium = create_triangular_set("medium", 20, 50, 80)
    high = create_triangular_set("high", 50, 100, 100)
    
    print(f"    Created: {low.name}, {medium.name}, {high.name}")
    
    print("\n4.2 Membership Values:")
    for x in [0, 25, 50, 75, 100]:
        low_mu = low.membership(x)
        med_mu = medium.membership(x)
        high_mu = high.membership(x)
        print(f"    x={x}: low={low_mu:.2f}, medium={med_mu:.2f}, high={high_mu:.2f}")
    
    print("\n4.3 Fuzzy Set Operations:")
    
    # Complement
    not_high = high.complement()
    print(f"    NOT high at x=50: {not_high.membership(50):.4f}")
    
    # Union
    low_or_high = low.union_with(high)
    print(f"    low OR high at x=0:  {low_or_high.membership(0):.4f}")
    print(f"    low OR high at x=50: {low_or_high.membership(50):.4f}")
    print(f"    low OR high at x=100: {low_or_high.membership(100):.4f}")
    
    # Intersection
    low_and_medium = low.intersect_with(medium)
    print(f"    low AND medium at x=35: {low_and_medium.membership(35):.4f}")
    
    # Apply hedge
    very_medium = medium.apply_hedge(HedgeType.VERY)
    print(f"    very medium at x=35: {very_medium.membership(35):.4f} (vs {medium.membership(35):.4f})")


def example_linguistic_variables():
    """
    Example 5: Linguistic variables.
    
    Demonstrates creating linguistic variables with multiple fuzzy sets.
    """
    print("\n" + "=" * 60)
    print("Example 5: Linguistic Variables")
    print("=" * 60)
    
    print("\n5.1 Temperature Variable:")
    temp = create_temperature_variable(0, 100)
    
    print(f"    Variable: {temp.name}")
    print(f"    Universe: [{temp.universe_min}, {temp.universe_max}]")
    print(f"    Fuzzy sets: {list(temp.fuzzy_sets.keys())}")
    
    print("\n5.2 Membership Values for Different Temperatures:")
    for temp_val in [10, 25, 50, 75, 90]:
        memberships = temp.get_all_memberships(temp_val)
        print(f"    {temp_val}°C: cold={memberships['cold']:.2f}, "
              f"cool={memberships['cool']:.2f}, "
              f"comfortable={memberships['comfortable']:.2f}, "
              f"warm={memberships['warm']:.2f}, "
              f"hot={memberships['hot']:.2f}")
    
    print("\n5.3 Active Sets (membership > 0.1):")
    for temp_val in [20, 40, 60, 80]:
        active = temp.get_active_sets(temp_val, threshold=0.1)
        print(f"    {temp_val}°C: Active sets = {list(active.keys())}")
    
    print("\n5.4 Other Pre-built Variables:")
    
    speed = create_speed_variable(0, 120)
    print(f"    Speed variable: {list(speed.fuzzy_sets.keys())}")
    print(f"    Speed 60: {speed.get_all_memberships(60)}")
    
    age = create_age_variable(0, 100)
    print(f"    Age variable: {list(age.fuzzy_sets.keys())}")
    print(f"    Age 50: {age.get_all_memberships(50)}")
    
    risk = create_risk_variable(0, 1)
    print(f"    Risk variable: {list(risk.fuzzy_sets.keys())}")
    print(f"    Risk 0.5: {risk.get_all_memberships(0.5)}")


def example_fuzzy_controller():
    """
    Example 6: Fuzzy inference system (temperature controller).
    
    Demonstrates a complete fuzzy control system.
    """
    print("\n" + "=" * 60)
    print("Example 6: Fuzzy Temperature Controller")
    print("=" * 60)
    
    print("\n6.1 Controller Setup:")
    controller = create_temperature_controller()
    print(f"    Name: {controller.name}")
    print(f"    Input variables: {list(controller.input_vars.keys())}")
    print(f"    Output variables: {list(controller.output_vars.keys())}")
    print(f"    Number of rules: {len(controller.rules)}")
    print(f"    Defuzzification: {controller.defuzzification.value}")
    
    print("\n6.2 Rules:")
    for i, rule in enumerate(controller.rules):
        ant = ', '.join([f"{v} IS {s}" for v, s in rule.antecedent.items()])
        cons = ', '.join([f"{v} IS {s}" for v, s in rule.consequent.items()])
        print(f"    Rule {i+1}: IF {ant} THEN {cons}")
    
    print("\n6.3 Control Results:")
    print("    Temperature → Fan Speed")
    for temp in [5, 15, 30, 50, 70, 85, 95]:
        result = controller.evaluate({'temperature': temp})
        print(f"    {temp}°C → {result['fan_speed']:.1f}%")
    
    print("\n6.4 Different Defuzzification Methods:")
    methods = [
        DefuzzificationMethod.CENTROID,
        DefuzzificationMethod.BISECTOR,
        DefuzzificationMethod.MOM,
        DefuzzificationMethod.SOM,
        DefuzzificationMethod.LOM
    ]
    
    print("    Temperature=50°C with different methods:")
    for method in methods:
        controller.defuzzification = method
        result = controller.evaluate({'temperature': 50})
        print(f"      {method.value}: {result['fan_speed']:.1f}%")
    
    # Reset to default
    controller.defuzzification = DefuzzificationMethod.CENTROID


def example_custom_inference_system():
    """
    Example 7: Custom fuzzy inference system.
    
    Demonstrates creating a custom fuzzy decision system.
    """
    print("\n" + "=" * 60)
    print("Example 7: Custom Fuzzy Inference System")
    print("=" * 60)
    
    print("\n7.1 Risk Assessment System:")
    
    # Create input variables
    severity = LinguisticVariable("severity", universe_min=0, universe_max=10)
    severity.add_fuzzy_set("low", lambda x: triangular_membership(x, 0, 0, 4))
    severity.add_fuzzy_set("medium", lambda x: triangular_membership(x, 2, 5, 8))
    severity.add_fuzzy_set("high", lambda x: triangular_membership(x, 6, 10, 10))
    
    probability = LinguisticVariable("probability", universe_min=0, universe_max=1)
    probability.add_fuzzy_set("rare", lambda x: triangular_membership(x, 0, 0, 0.3))
    probability.add_fuzzy_set("occasional", lambda x: triangular_membership(x, 0.2, 0.5, 0.8))
    probability.add_fuzzy_set("frequent", lambda x: triangular_membership(x, 0.7, 1, 1))
    
    # Create output variable
    risk_level = create_risk_variable(0, 100)
    
    # Create system
    system = FuzzyInferenceSystem("risk_assessment")
    system.add_input_variable(severity)
    system.add_input_variable(probability)
    system.add_output_variable(risk_level)
    
    # Add rules
    system.add_rule({"severity": "low", "probability": "rare"}, {"risk": "low"})
    system.add_rule({"severity": "low", "probability": "occasional"}, {"risk": "low"})
    system.add_rule({"severity": "medium", "probability": "rare"}, {"risk": "medium"})
    system.add_rule({"severity": "medium", "probability": "occasional"}, {"risk": "medium"})
    system.add_rule({"severity": "high", "probability": "occasional"}, {"risk": "high"})
    system.add_rule({"severity": "medium", "probability": "frequent"}, {"risk": "high"})
    system.add_rule({"severity": "high", "probability": "frequent"}, {"risk": "critical"})
    
    print(f"    System: {system.name}")
    print(f"    Inputs: severity, probability")
    print(f"    Output: risk")
    
    print("\n7.2 Risk Assessment Results:")
    print("    Severity × Probability → Risk Level")
    
    test_cases = [
        (2, 0.1),   # Low severity, rare
        (5, 0.5),   # Medium severity, occasional
        (8, 0.9),   # High severity, frequent
        (3, 0.6),   # Low-medium severity, occasional
        (7, 0.3),   # High severity, rare
    ]
    
    for sev, prob in test_cases:
        result = system.evaluate({'severity': sev, 'probability': prob})
        print(f"    Severity={sev}, Probability={prob} → Risk={result['risk']:.1f}")


def example_air_conditioning_controller():
    """
    Example 8: Air conditioning fuzzy controller.
    
    Demonstrates a multi-input, multi-output fuzzy controller.
    """
    print("\n" + "=" * 60)
    print("Example 8: Air Conditioning Controller")
    print("=" * 60)
    
    print("\n8.1 Controller Design:")
    
    # Temperature input
    temperature = create_temperature_variable(10, 40)
    
    # Humidity input
    humidity = LinguisticVariable("humidity", universe_min=0, universe_max=100)
    humidity.add_fuzzy_set("dry", lambda x: triangular_membership(x, 0, 0, 40))
    humidity.add_fuzzy_set("normal", lambda x: triangular_membership(x, 20, 50, 80))
    humidity.add_fuzzy_set("humid", lambda x: triangular_membership(x, 60, 100, 100))
    
    # Fan speed output
    fan = LinguisticVariable("fan_speed", universe_min=0, universe_max=5)
    fan.add_fuzzy_set("low", lambda x: triangular_membership(x, 0, 0, 2))
    fan.add_fuzzy_set("medium", lambda x: triangular_membership(x, 1, 2.5, 4))
    fan.add_fuzzy_set("high", lambda x: triangular_membership(x, 3, 5, 5))
    
    # Cooling level output
    cooling = LinguisticVariable("cooling", universe_min=0, universe_max=100)
    cooling.add_fuzzy_set("minimal", lambda x: triangular_membership(x, 0, 0, 30))
    cooling.add_fuzzy_set("moderate", lambda x: triangular_membership(x, 20, 50, 80))
    cooling.add_fuzzy_set("strong", lambda x: triangular_membership(x, 70, 100, 100))
    
    # Create system
    ac_system = FuzzyInferenceSystem("air_conditioning")
    ac_system.add_input_variable(temperature)
    ac_system.add_input_variable(humidity)
    ac_system.add_output_variable(fan)
    ac_system.add_output_variable(cooling)
    
    # Add rules
    ac_system.add_rule({"temperature": "cold", "humidity": "dry"}, {"fan_speed": "low", "cooling": "minimal"})
    ac_system.add_rule({"temperature": "cool", "humidity": "normal"}, {"fan_speed": "low", "cooling": "minimal"})
    ac_system.add_rule({"temperature": "comfortable", "humidity": "normal"}, {"fan_speed": "medium", "cooling": "moderate"})
    ac_system.add_rule({"temperature": "warm", "humidity": "normal"}, {"fan_speed": "medium", "cooling": "moderate"})
    ac_system.add_rule({"temperature": "hot", "humidity": "dry"}, {"fan_speed": "high", "cooling": "strong"})
    ac_system.add_rule({"temperature": "hot", "humidity": "normal"}, {"fan_speed": "high", "cooling": "strong"})
    ac_system.add_rule({"temperature": "warm", "humidity": "humid"}, {"fan_speed": "high", "cooling": "strong"})
    ac_system.add_rule({"temperature": "hot", "humidity": "humid"}, {"fan_speed": "high", "cooling": "strong"})
    
    print(f"    System: {ac_system.name}")
    print(f"    Inputs: temperature, humidity")
    print(f"    Outputs: fan_speed, cooling")
    
    print("\n8.2 Controller Results:")
    print("    Temperature × Humidity → Fan Speed, Cooling")
    
    test_cases = [
        (15, 30),   # Cool, dry
        (25, 50),   # Comfortable, normal
        (32, 40),   # Hot, dry
        (30, 80),   # Warm, humid
        (35, 90),   # Hot, humid
    ]
    
    for temp, hum in test_cases:
        result = ac_system.evaluate({'temperature': temp, 'humidity': hum})
        print(f"    {temp}°C, {hum}% humidity → "
              f"Fan={result['fan_speed']:.1f}, Cooling={result['cooling']:.1f}")


def example_alpha_cut():
    """
    Example 9: Alpha-cut.
    
    Demonstrates finding regions where membership exceeds a threshold.
    """
    print("\n" + "=" * 60)
    print("Example 9: Alpha-Cut")
    print("=" * 60)
    
    print("\n9.1 Alpha-cut of Triangular Fuzzy Set:")
    fs = create_triangular_set("medium", 0, 50, 100)
    
    print(f"    Fuzzy set: {fs.name}")
    print(f"    Parameters: a=0, b=50, c=100")
    
    for alpha in [0.2, 0.5, 0.8]:
        cut = fs.get_alpha_cut(alpha)
        print(f"    α-cut at {alpha}: {cut}")
    
    print("\n9.2 Alpha-cut Application:")
    print("    Use alpha-cut to define crisp boundaries for fuzzy concepts")
    print("    Example: 'High quality' products (μ >= 0.7)")


def main():
    """Run all examples."""
    print("\n" + "=" * 60)
    print("AllToolkit - Fuzzy Logic Utilities Examples")
    print("=" * 60)
    
    example_membership_functions()
    example_fuzzy_operations()
    example_hedges()
    example_fuzzy_sets()
    example_linguistic_variables()
    example_fuzzy_controller()
    example_custom_inference_system()
    example_air_conditioning_controller()
    example_alpha_cut()
    
    print("\n" + "=" * 60)
    print("All examples completed!")
    print("=" * 60)
    print("\nFor full documentation, see mod.py")
    print("For test cases, see fuzzy_logic_utils_test.py")


if __name__ == '__main__':
    main()