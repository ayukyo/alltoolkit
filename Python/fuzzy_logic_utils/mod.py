#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Fuzzy Logic Utilities Module
==========================================
A comprehensive fuzzy logic system utility module for Python with zero external dependencies.

Features:
    - Fuzzy set operations (union, intersection, complement)
    - Membership functions (triangular, trapezoidal, Gaussian, sigmoid, etc.)
    - Fuzzy inference systems (Mamdani-style)
    - Fuzzy rule evaluation
    - Defuzzification methods (centroid, bisector, MOM, SOM, LOM)
    - Linguistic variable support
    - Hedges (modifiers like "very", "slightly", "extremely")
    - Fuzzy controllers and decision systems

Applications:
    - Control systems (temperature, speed, etc.)
    - Decision making systems
    - Expert systems
    - Pattern recognition
    - Risk assessment

Author: AllToolkit Contributors
License: MIT
"""

import math
from typing import Any, Callable, Dict, List, Optional, Tuple, Union
from dataclasses import dataclass, field
from enum import Enum


# ============================================================================
# Type Aliases
# ============================================================================

Number = Union[int, float]
MembershipValue = float  # Membership degree [0, 1]
MembershipFunction = Callable[[float], float]


# ============================================================================
# Enums
# ============================================================================

class FuzzyOperator(Enum):
    """Fuzzy logical operators"""
    MIN = "min"          # Standard intersection (Zadeh)
    MAX = "max"          # Standard union (Zadeh)
    PRODUCT = "product"  # Probabilistic intersection
    SUM = "sum"          # Probabilistic union (bounded)
    BOUND_SUM = "bounded_sum"  # Bounded sum union
    BOUND_DIFF = "bounded_diff"  # Bounded difference intersection
    DRASTIC_PRODUCT = "drastic_product"
    DRASTIC_SUM = "drastic_sum"
    HAMACHER_PRODUCT = "hamacher_product"
    HAMACHER_SUM = "hamacher_sum"
    EINSTEIN_PRODUCT = "einstein_product"
    EINSTEIN_SUM = "einstein_sum"


class DefuzzificationMethod(Enum):
    """Defuzzification methods"""
    CENTROID = "centroid"       # Center of gravity
    BISECTOR = "bisector"       # Bisector of area
    MOM = "mom"                 # Mean of maximum
    SOM = "som"                 # Smallest of maximum
    LOM = "lom"                 # Largest of maximum
    WEIGHTED_AVERAGE = "weighted_average"


class HedgeType(Enum):
    """Fuzzy hedges (modifiers)"""
    VERY = "very"               # Concentration (μ²)
    EXTREMELY = "extremely"     # Strong concentration (μ³)
    SLIGHTLY = "slightly"       # Dilution (√μ)
    SOMEWHAT = "somewhat"       # Moderate dilution (√μ)
    MORE_OR_LESS = "more_or_less"  # Dilution (√μ)
    INTENSELY = "intensely"     # Concentration (μ²)
    PLUS = "plus"               # Slight concentration (μ^1.25)
    MINUS = "minus"             # Slight dilution (μ^0.75)


# ============================================================================
# Membership Functions
# ============================================================================

def triangular_membership(x: Number, a: Number, b: Number, c: Number) -> MembershipValue:
    """
    Triangular membership function.
    
    Args:
        x: Input value
        a: Left boundary (membership = 0)
        b: Peak (membership = 1)
        c: Right boundary (membership = 0)
    
    Returns:
        Membership degree [0, 1]
    
    Example:
        >>> triangular_membership(5, 0, 5, 10)
        1.0
        >>> triangular_membership(2.5, 0, 5, 10)
        0.5
        >>> triangular_membership(7.5, 0, 5, 10)
        0.5
    """
    x = float(x)
    a, b, c = float(a), float(b), float(c)
    
    if a > c:
        raise ValueError("Invalid triangular parameters: a <= c required")
    
    # Handle edge cases where a == b or b == c
    if a == b == c:
        return 1.0 if x == a else 0.0
    
    if x <= a:
        # When a == b, membership is 1 at a
        if a == b:
            return 1.0
        return 0.0
    elif x >= c:
        # When b == c, membership is 1 at c
        if b == c:
            return 1.0
        return 0.0
    elif x <= b:
        if a == b:
            return 1.0
        return (x - a) / (b - a)
    elif x > b:
        if b == c:
            return 1.0
        return (c - x) / (c - b)
    else:  # x == b
        return 1.0


def trapezoidal_membership(x: Number, a: Number, b: Number, c: Number, d: Number) -> MembershipValue:
    """
    Trapezoidal membership function.
    
    Args:
        x: Input value
        a: Left boundary (membership = 0)
        b: Left peak (membership = 1)
        c: Right peak (membership = 1)
        d: Right boundary (membership = 0)
    
    Returns:
        Membership degree [0, 1]
    
    Example:
        >>> trapezoidal_membership(5, 0, 3, 7, 10)
        1.0
        >>> trapezoidal_membership(1.5, 0, 3, 7, 10)
        0.5
    """
    x = float(x)
    a, b, c, d = float(a), float(b), float(c), float(d)
    
    if a > b or b > c or c > d:
        raise ValueError("Invalid trapezoidal parameters: a <= b <= c <= d required")
    
    if x <= a or x >= d:
        return 0.0
    elif a < x < b:
        return (x - a) / (b - a)
    elif b <= x <= c:
        return 1.0
    elif c < x < d:
        return (d - x) / (d - c)
    else:
        return 0.0


def gaussian_membership(x: Number, center: Number, sigma: Number) -> MembershipValue:
    """
    Gaussian membership function.
    
    Args:
        x: Input value
        center: Center of the Gaussian (peak)
        sigma: Standard deviation (width)
    
    Returns:
        Membership degree [0, 1]
    
    Example:
        >>> gaussian_membership(5, 5, 2)
        1.0
        >>> round(gaussian_membership(7, 5, 2), 4)
        0.6065
    """
    x = float(x)
    center = float(center)
    sigma = float(sigma)
    
    if sigma <= 0:
        raise ValueError("Sigma must be positive")
    
    return math.exp(-((x - center) ** 2) / (2 * sigma ** 2))


def gaussian2_membership(x: Number, center1: Number, sigma1: Number, 
                         center2: Number, sigma2: Number) -> MembershipValue:
    """
    Two-sided Gaussian membership function (composite).
    
    Args:
        x: Input value
        center1: Left center
        sigma1: Left standard deviation
        center2: Right center
        sigma2: Right standard deviation
    
    Returns:
        Membership degree [0, 1]
    
    Example:
        >>> gaussian2_membership(5, 0, 2, 10, 2)
        1.0
    """
    x = float(x)
    c1, s1 = float(center1), float(sigma1)
    c2, s2 = float(center2), float(sigma2)
    
    if s1 <= 0 or s2 <= 0:
        raise ValueError("Sigma values must be positive")
    
    # Left Gaussian for x <= c1
    # Right Gaussian for x >= c2
    # Use minimum of both for middle region
    if x < c1:
        return math.exp(-((x - c1) ** 2) / (2 * s1 ** 2))
    elif x > c2:
        return math.exp(-((x - c2) ** 2) / (2 * s2 ** 2))
    else:
        return 1.0


def sigmoid_membership(x: Number, a: Number, c: Number) -> MembershipValue:
    """
    Sigmoid membership function.
    
    Formula: μ(x) = 1 / (1 + exp(-a(x - c)))
    
    Args:
        x: Input value
        a: Slope (positive = rising, negative = falling)
        c: Inflection point
    
    Returns:
        Membership degree [0, 1]
    
    Example:
        >>> round(sigmoid_membership(5, 2, 5), 4)
        0.5
        >>> round(sigmoid_membership(7, 2, 5), 4)
        0.8808
    """
    x = float(x)
    a = float(a)
    c = float(c)
    
    return 1.0 / (1.0 + math.exp(-a * (x - c)))


def bell_membership(x: Number, a: Number, b: Number, c: Number) -> MembershipValue:
    """
    Generalized bell membership function.
    
    Formula: μ(x) = 1 / (1 + |((x - c) / a)|^(2b))
    
    Args:
        x: Input value
        a: Width parameter
        b: Shape parameter (controls smoothness)
        c: Center
    
    Returns:
        Membership degree [0, 1]
    
    Example:
        >>> bell_membership(5, 2, 4, 5)
        1.0
    """
    x = float(x)
    a, b, c = float(a), float(b), float(c)
    
    if a <= 0:
        raise ValueError("Parameter a must be positive")
    
    return 1.0 / (1.0 + abs((x - c) / a) ** (2 * b))


def s_shape_membership(x: Number, a: Number, b: Number) -> MembershipValue:
    """
    S-shaped membership function (smooth step-up).
    
    Args:
        x: Input value
        a: Left boundary (membership = 0)
        b: Right boundary (membership = 1)
    
    Returns:
        Membership degree [0, 1]
    
    Example:
        >>> s_shape_membership(5, 0, 10)
        0.5
        >>> s_shape_membership(15, 0, 10)
        1.0
    """
    x = float(x)
    a, b = float(a), float(b)
    
    if a >= b:
        raise ValueError("Invalid S-shape parameters: a < b required")
    
    if x <= a:
        return 0.0
    elif x >= b:
        return 1.0
    elif a < x <= (a + b) / 2:
        return 2 * ((x - a) / (b - a)) ** 2
    else:  # (a + b) / 2 < x < b
        return 1 - 2 * ((b - x) / (b - a)) ** 2


def z_shape_membership(x: Number, a: Number, b: Number) -> MembershipValue:
    """
    Z-shaped membership function (smooth step-down).
    
    Args:
        x: Input value
        a: Left boundary (membership = 1)
        b: Right boundary (membership = 0)
    
    Returns:
        Membership degree [0, 1]
    
    Example:
        >>> z_shape_membership(5, 0, 10)
        0.5
        >>> z_shape_membership(-5, 0, 10)
        1.0
    """
    x = float(x)
    a, b = float(a), float(b)
    
    if a >= b:
        raise ValueError("Invalid Z-shape parameters: a < b required")
    
    if x <= a:
        return 1.0
    elif x >= b:
        return 0.0
    elif a < x <= (a + b) / 2:
        return 1 - 2 * ((x - a) / (b - a)) ** 2
    else:  # (a + b) / 2 < x < b
        return 2 * ((b - x) / (b - a)) ** 2


def pi_shape_membership(x: Number, a: Number, b: Number, c: Number, d: Number) -> MembershipValue:
    """
    Pi-shaped membership function (combination of S and Z).
    
    Args:
        x: Input value
        a: Left boundary (membership = 0)
        b: Left rise point
        c: Right fall point
        d: Right boundary (membership = 0)
    
    Returns:
        Membership degree [0, 1]
    
    Example:
        >>> pi_shape_membership(5, 0, 3, 7, 10)
        1.0
    """
    x = float(x)
    a, b, c, d = float(a), float(b), float(c), float(d)
    
    if a > b or b > c or c > d:
        raise ValueError("Invalid Pi-shape parameters: a <= b <= c <= d required")
    
    if x <= a or x >= d:
        return 0.0
    elif a < x < b:
        return s_shape_membership(x, a, b)
    elif b <= x <= c:
        return 1.0
    else:  # c < x < d
        return z_shape_membership(x, c, d)


def singleton_membership(x: Number, value: Number) -> MembershipValue:
    """
    Singleton membership function.
    
    Args:
        x: Input value
        value: Point where membership = 1
    
    Returns:
        Membership degree (0 or 1)
    
    Example:
        >>> singleton_membership(5, 5)
        1.0
        >>> singleton_membership(5, 4)
        0.0
    """
    return 1.0 if float(x) == float(value) else 0.0


def rectangular_membership(x: Number, a: Number, b: Number) -> MembershipValue:
    """
    Rectangular (crisp) membership function.
    
    Args:
        x: Input value
        a: Left boundary
        b: Right boundary
    
    Returns:
        Membership degree (0 or 1)
    
    Example:
        >>> rectangular_membership(5, 0, 10)
        1.0
        >>> rectangular_membership(15, 0, 10)
        0.0
    """
    x = float(x)
    a, b = float(a), float(b)
    return 1.0 if a <= x <= b else 0.0


def linear_membership(x: Number, a: Number, b: Number) -> MembershipValue:
    """
    Linear membership function (rising).
    
    Args:
        x: Input value
        a: Point where membership = 0
        b: Point where membership = 1
    
    Returns:
        Membership degree [0, 1]
    
    Example:
        >>> linear_membership(5, 0, 10)
        0.5
    """
    x = float(x)
    a, b = float(a), float(b)
    
    if a == b:
        return 1.0 if x == a else 0.0
    
    if x <= a:
        return 0.0
    elif x >= b:
        return 1.0
    else:
        return (x - a) / (b - a)


def linear_down_membership(x: Number, a: Number, b: Number) -> MembershipValue:
    """
    Linear membership function (falling).
    
    Args:
        x: Input value
        a: Point where membership = 1
        b: Point where membership = 0
    
    Returns:
        Membership degree [0, 1]
    
    Example:
        >>> linear_down_membership(5, 0, 10)
        0.5
    """
    x = float(x)
    a, b = float(a), float(b)
    
    if a == b:
        return 1.0 if x == a else 0.0
    
    if x <= a:
        return 1.0
    elif x >= b:
        return 0.0
    else:
        return (b - x) / (b - a)


# ============================================================================
# Fuzzy Set Operations
# ============================================================================

def fuzzy_union(a: MembershipValue, b: MembershipValue, 
                operator: FuzzyOperator = FuzzyOperator.MAX) -> MembershipValue:
    """
    Fuzzy union (OR operation).
    
    Args:
        a: First membership degree
        b: Second membership degree
        operator: Union operator type
    
    Returns:
        Union membership degree
    
    Example:
        >>> fuzzy_union(0.3, 0.7)
        0.7
        >>> fuzzy_union(0.3, 0.7, FuzzyOperator.SUM)
        1.0
    """
    a, b = float(a), float(b)
    
    if operator == FuzzyOperator.MAX:
        return max(a, b)
    elif operator == FuzzyOperator.SUM:
        return min(a + b, 1.0)
    elif operator == FuzzyOperator.BOUND_SUM:
        return min(a + b, 1.0)
    elif operator == FuzzyOperator.DRASTIC_SUM:
        if a == 0:
            return b
        elif b == 0:
            return a
        else:
            return 1.0
    elif operator == FuzzyOperator.HAMACHER_SUM:
        return (a + b - a * b) / (1 - a * b) if a * b != 1 else 1.0
    elif operator == FuzzyOperator.EINSTEIN_SUM:
        return (a + b) / (1 + a * b)
    else:
        return max(a, b)


def fuzzy_intersection(a: MembershipValue, b: MembershipValue,
                       operator: FuzzyOperator = FuzzyOperator.MIN) -> MembershipValue:
    """
    Fuzzy intersection (AND operation).
    
    Args:
        a: First membership degree
        b: Second membership degree
        operator: Intersection operator type
    
    Returns:
        Intersection membership degree
    
    Example:
        >>> fuzzy_intersection(0.3, 0.7)
        0.3
        >>> fuzzy_intersection(0.3, 0.7, FuzzyOperator.PRODUCT)
        0.21
    """
    a, b = float(a), float(b)
    
    if operator == FuzzyOperator.MIN:
        return min(a, b)
    elif operator == FuzzyOperator.PRODUCT:
        return a * b
    elif operator == FuzzyOperator.BOUND_DIFF:
        return max(a + b - 1, 0.0)
    elif operator == FuzzyOperator.DRASTIC_PRODUCT:
        if a == 1:
            return b
        elif b == 1:
            return a
        else:
            return 0.0
    elif operator == FuzzyOperator.HAMACHER_PRODUCT:
        return (a * b) / (a + b - a * b) if (a + b - a * b) != 0 else 0.0
    elif operator == FuzzyOperator.EINSTEIN_PRODUCT:
        return (a * b) / (2 - a - b + a * b) if (2 - a - b + a * b) != 0 else 0.0
    else:
        return min(a, b)


def fuzzy_complement(a: MembershipValue, complement_type: str = "standard") -> MembershipValue:
    """
    Fuzzy complement (NOT operation).
    
    Args:
        a: Membership degree
        complement_type: Type of complement ("standard", "sugeno", "yager")
    
    Returns:
        Complement membership degree
    
    Example:
        >>> fuzzy_complement(0.3)
        0.7
    """
    a = float(a)
    
    if complement_type == "standard":
        return 1.0 - a
    elif complement_type == "sugeno":
        # Sugeno complement: (1 - a) / (1 + lambda * a), lambda > -1
        lambda_val = 1.0  # Default lambda
        return (1.0 - a) / (1.0 + lambda_val * a)
    elif complement_type == "yager":
        # Yager complement: (1 - a^w)^(1/w), w > 0
        w = 2.0  # Default w
        return (1.0 - a ** w) ** (1.0 / w)
    else:
        return 1.0 - a


def fuzzy_difference(a: MembershipValue, b: MembershipValue) -> MembershipValue:
    """
    Fuzzy difference (A AND NOT B).
    
    Args:
        a: First membership degree
        b: Second membership degree
    
    Returns:
        Difference membership degree
    
    Example:
        >>> fuzzy_difference(0.5, 0.3)
        0.5
    """
    return fuzzy_intersection(a, fuzzy_complement(b))


# ============================================================================
# Fuzzy Hedges (Modifiers)
# ============================================================================

def apply_hedge(membership: MembershipValue, hedge: HedgeType) -> MembershipValue:
    """
    Apply a fuzzy hedge (modifier) to a membership value.
    
    Args:
        membership: Original membership degree
        hedge: Type of hedge to apply
    
    Returns:
        Modified membership degree
    
    Example:
        >>> apply_hedge(0.5, HedgeType.VERY)
        0.25
        >>> apply_hedge(0.5, HedgeType.SLIGHTLY)
        0.7071067811865476
    """
    mu = float(membership)
    
    if hedge == HedgeType.VERY or hedge == HedgeType.INTENSELY:
        return mu ** 2
    elif hedge == HedgeType.EXTREMELY:
        return mu ** 3
    elif hedge in (HedgeType.SLIGHTLY, HedgeType.SOMEWHAT, HedgeType.MORE_OR_LESS):
        return math.sqrt(mu)
    elif hedge == HedgeType.PLUS:
        return mu ** 1.25
    elif hedge == HedgeType.MINUS:
        return mu ** 0.75
    else:
        return mu


def hedge_function(hedge: HedgeType) -> Callable[[MembershipValue], MembershipValue]:
    """
    Create a hedge function for applying to membership values.
    
    Args:
        hedge: Type of hedge
    
    Returns:
        Function that applies the hedge
    
    Example:
        >>> very = hedge_function(HedgeType.VERY)
        >>> very(0.5)
        0.25
    """
    return lambda mu: apply_hedge(mu, hedge)


# ============================================================================
# Fuzzy Set Class
# ============================================================================

@dataclass
class FuzzySet:
    """
    Fuzzy set representation with a membership function.
    
    Attributes:
        name: Name of the fuzzy set
        membership_func: Membership function
        universe_min: Minimum value of the universe
        universe_max: Maximum value of the universe
    """
    name: str
    membership_func: Callable[[float], float]
    universe_min: float = 0.0
    universe_max: float = 100.0
    description: str = ""
    
    def membership(self, x: Number) -> MembershipValue:
        """Get membership degree for value x."""
        return self.membership_func(float(x))
    
    def __call__(self, x: Number) -> MembershipValue:
        """Callable interface for membership."""
        return self.membership(x)
    
    def complement(self) -> 'FuzzySet':
        """Create complement fuzzy set."""
        return FuzzySet(
            name=f"NOT_{self.name}",
            membership_func=lambda x: fuzzy_complement(self.membership(x)),
            universe_min=self.universe_min,
            universe_max=self.universe_max
        )
    
    def apply_hedge(self, hedge: HedgeType) -> 'FuzzySet':
        """Apply hedge to create new fuzzy set."""
        return FuzzySet(
            name=f"{hedge.value}_{self.name}",
            membership_func=lambda x: apply_hedge(self.membership(x), hedge),
            universe_min=self.universe_min,
            universe_max=self.universe_max
        )
    
    def union_with(self, other: 'FuzzySet', 
                   operator: FuzzyOperator = FuzzyOperator.MAX) -> 'FuzzySet':
        """Union with another fuzzy set."""
        return FuzzySet(
            name=f"{self.name}_OR_{other.name}",
            membership_func=lambda x: fuzzy_union(
                self.membership(x), other.membership(x), operator
            ),
            universe_min=min(self.universe_min, other.universe_min),
            universe_max=max(self.universe_max, other.universe_max)
        )
    
    def intersect_with(self, other: 'FuzzySet',
                       operator: FuzzyOperator = FuzzyOperator.MIN) -> 'FuzzySet':
        """Intersection with another fuzzy set."""
        return FuzzySet(
            name=f"{self.name}_AND_{other.name}",
            membership_func=lambda x: fuzzy_intersection(
                self.membership(x), other.membership(x), operator
            ),
            universe_min=min(self.universe_min, other.universe_min),
            universe_max=max(self.universe_max, other.universe_max)
        )
    
    def get_alpha_cut(self, alpha: float) -> List[Tuple[float, float]]:
        """
        Get alpha-cut (values where membership >= alpha).
        
        Args:
            alpha: Threshold value
        
        Returns:
            List of (x, membership) pairs
        """
        # Sample the universe to find alpha-cut region
        steps = 1000
        dx = (self.universe_max - self.universe_min) / steps
        cut_points = []
        
        in_cut = False
        start_x = None
        
        for i in range(steps + 1):
            x = self.universe_min + i * dx
            mu = self.membership(x)
            
            if mu >= alpha and not in_cut:
                in_cut = True
                start_x = x
            elif mu < alpha and in_cut:
                in_cut = False
                cut_points.append((start_x, x))
                start_x = None
        
        if in_cut:
            cut_points.append((start_x, self.universe_max))
        
        return cut_points


# ============================================================================
# Linguistic Variable
# ============================================================================

@dataclass
class LinguisticVariable:
    """
    Linguistic variable with multiple fuzzy sets.
    
    Attributes:
        name: Name of the linguistic variable
        fuzzy_sets: Dictionary of fuzzy sets by name
        universe_min: Minimum value of the universe
        universe_max: Maximum value of the universe
    """
    name: str
    fuzzy_sets: Dict[str, FuzzySet] = field(default_factory=dict)
    universe_min: float = 0.0
    universe_max: float = 100.0
    
    def add_fuzzy_set(self, name: str, membership_func: Callable[[float], float],
                      description: str = "") -> None:
        """Add a fuzzy set to the linguistic variable."""
        self.fuzzy_sets[name] = FuzzySet(
            name=name,
            membership_func=membership_func,
            universe_min=self.universe_min,
            universe_max=self.universe_max,
            description=description
        )
    
    def get_membership(self, value: Number, set_name: str) -> MembershipValue:
        """Get membership degree for a specific fuzzy set."""
        if set_name not in self.fuzzy_sets:
            raise ValueError(f"Fuzzy set '{set_name}' not found")
        return self.fuzzy_sets[set_name].membership(float(value))
    
    def get_all_memberships(self, value: Number) -> Dict[str, MembershipValue]:
        """Get membership degrees for all fuzzy sets."""
        return {name: fs.membership(float(value)) for name, fs in self.fuzzy_sets.items()}
    
    def get_active_sets(self, value: Number, threshold: float = 0.0) -> Dict[str, MembershipValue]:
        """Get fuzzy sets with membership > threshold."""
        memberships = self.get_all_memberships(value)
        return {name: mu for name, mu in memberships.items() if mu > threshold}


# ============================================================================
# Fuzzy Rule
# ============================================================================

@dataclass
class FuzzyRule:
    """
    Fuzzy rule: IF antecedent THEN consequent.
    
    Attributes:
        antecedent: Antecedent conditions (dict of variable -> set name)
        consequent: Consequent (dict of variable -> set name)
        weight: Rule weight [0, 1]
        operator: Logical operator for combining antecedents
    """
    antecedent: Dict[str, str]  # {variable_name: fuzzy_set_name}
    consequent: Dict[str, str]  # {variable_name: fuzzy_set_name}
    weight: float = 1.0
    operator: FuzzyOperator = FuzzyOperator.MIN
    description: str = ""
    
    def evaluate_antecedent(self, inputs: Dict[str, LinguisticVariable],
                            values: Dict[str, Number]) -> MembershipValue:
        """
        Evaluate the antecedent strength.
        
        Args:
            inputs: Dictionary of linguistic variables
            values: Dictionary of input values
        
        Returns:
            Antecedent strength (firing strength)
        """
        memberships = []
        
        for var_name, set_name in self.antecedent.items():
            if var_name not in inputs:
                raise ValueError(f"Variable '{var_name}' not found in inputs")
            if set_name not in inputs[var_name].fuzzy_sets:
                raise ValueError(f"Fuzzy set '{set_name}' not found in '{var_name}'")
            
            value = values.get(var_name, 0)
            mu = inputs[var_name].fuzzy_sets[set_name].membership(float(value))
            memberships.append(mu)
        
        # Combine memberships using operator
        if len(memberships) == 0:
            return 0.0
        elif len(memberships) == 1:
            return memberships[0] * self.weight
        
        result = memberships[0]
        for mu in memberships[1:]:
            if self.operator == FuzzyOperator.MIN:
                result = min(result, mu)
            elif self.operator == FuzzyOperator.PRODUCT:
                result = result * mu
            else:
                result = min(result, mu)
        
        return result * self.weight


# ============================================================================
# Fuzzy Inference System
# ============================================================================

@dataclass
class FuzzyInferenceSystem:
    """
    Mamdani-style fuzzy inference system.
    
    Attributes:
        name: System name
        input_vars: Dictionary of input linguistic variables
        output_vars: Dictionary of output linguistic variables
        rules: List of fuzzy rules
        defuzzification: Defuzzification method
    """
    name: str
    input_vars: Dict[str, LinguisticVariable] = field(default_factory=dict)
    output_vars: Dict[str, LinguisticVariable] = field(default_factory=dict)
    rules: List[FuzzyRule] = field(default_factory=list)
    defuzzification: DefuzzificationMethod = DefuzzificationMethod.CENTROID
    
    def add_input_variable(self, var: LinguisticVariable) -> None:
        """Add an input linguistic variable."""
        self.input_vars[var.name] = var
    
    def add_output_variable(self, var: LinguisticVariable) -> None:
        """Add an output linguistic variable."""
        self.output_vars[var.name] = var
    
    def add_rule(self, antecedent: Dict[str, str], consequent: Dict[str, str],
                 weight: float = 1.0, operator: FuzzyOperator = FuzzyOperator.MIN,
                 description: str = "") -> None:
        """Add a fuzzy rule."""
        rule = FuzzyRule(
            antecedent=antecedent,
            consequent=consequent,
            weight=weight,
            operator=operator,
            description=description
        )
        self.rules.append(rule)
    
    def evaluate(self, inputs: Dict[str, Number]) -> Dict[str, float]:
        """
        Evaluate the fuzzy system with given inputs.
        
        Args:
            inputs: Dictionary of input values
        
        Returns:
            Dictionary of output values after defuzzification
        """
        # Evaluate all rules
        rule_outputs = {}
        
        for rule in self.rules:
            firing_strength = rule.evaluate_antecedent(self.input_vars, inputs)
            
            # Apply firing strength to consequent fuzzy sets
            for var_name, set_name in rule.consequent.items():
                if var_name not in self.output_vars:
                    continue
                
                if var_name not in rule_outputs:
                    rule_outputs[var_name] = []
                
                rule_outputs[var_name].append((firing_strength, set_name))
        
        # Defuzzify each output variable
        results = {}
        
        for var_name, outputs in rule_outputs.items():
            output_var = self.output_vars[var_name]
            aggregated_membership = self._aggregate_outputs(output_var, outputs)
            
            results[var_name] = self._defuzzify(
                aggregated_membership, 
                output_var.universe_min,
                output_var.universe_max
            )
        
        return results
    
    def _aggregate_outputs(self, output_var: LinguisticVariable,
                           outputs: List[Tuple[float, str]]) -> Callable[[float], float]:
        """
        Aggregate output fuzzy sets using max operation.
        
        Args:
            output_var: Output linguistic variable
            outputs: List of (firing_strength, set_name) tuples
        
        Returns:
            Aggregated membership function
        """
        def aggregated_membership(x: float) -> float:
            max_mu = 0.0
            for firing_strength, set_name in outputs:
                if set_name in output_var.fuzzy_sets:
                    original_mu = output_var.fuzzy_sets[set_name].membership(x)
                    clipped_mu = min(original_mu, firing_strength)
                    max_mu = max(max_mu, clipped_mu)
            return max_mu
        
        return aggregated_membership
    
    def _defuzzify(self, membership_func: Callable[[float], float],
                   min_val: float, max_val: float) -> float:
        """
        Defuzzify the aggregated membership function.
        
        Args:
            membership_func: Membership function to defuzzify
            min_val: Minimum value of universe
            max_val: Maximum value of universe
        
        Returns:
            Defuzzified crisp value
        """
        if self.defuzzification == DefuzzificationMethod.CENTROID:
            return self._defuzzify_centroid(membership_func, min_val, max_val)
        elif self.defuzzification == DefuzzificationMethod.BISECTOR:
            return self._defuzzify_bisector(membership_func, min_val, max_val)
        elif self.defuzzification == DefuzzificationMethod.MOM:
            return self._defuzzify_mom(membership_func, min_val, max_val)
        elif self.defuzzification == DefuzzificationMethod.SOM:
            return self._defuzzify_som(membership_func, min_val, max_val)
        elif self.defuzzification == DefuzzificationMethod.LOM:
            return self._defuzzify_lom(membership_func, min_val, max_val)
        else:
            return self._defuzzify_centroid(membership_func, min_val, max_val)
    
    def _defuzzify_centroid(self, membership_func: Callable[[float], float],
                            min_val: float, max_val: float, steps: int = 100) -> float:
        """Centroid (center of gravity) defuzzification."""
        dx = (max_val - min_val) / steps
        
        total_area = 0.0
        weighted_sum = 0.0
        
        for i in range(steps):
            x = min_val + i * dx
            mu = membership_func(x)
            total_area += mu * dx
            weighted_sum += x * mu * dx
        
        if total_area == 0:
            return (min_val + max_val) / 2
        
        return weighted_sum / total_area
    
    def _defuzzify_bisector(self, membership_func: Callable[[float], float],
                            min_val: float, max_val: float, steps: int = 100) -> float:
        """Bisector of area defuzzification."""
        dx = (max_val - min_val) / steps
        
        # Calculate total area
        total_area = 0.0
        for i in range(steps):
            x = min_val + i * dx
            mu = membership_func(x)
            total_area += mu * dx
        
        if total_area == 0:
            return (min_val + max_val) / 2
        
        # Find bisector
        half_area = total_area / 2
        accumulated_area = 0.0
        
        for i in range(steps):
            x = min_val + i * dx
            mu = membership_func(x)
            accumulated_area += mu * dx
            if accumulated_area >= half_area:
                return x
        
        return max_val
    
    def _defuzzify_mom(self, membership_func: Callable[[float], float],
                       min_val: float, max_val: float, steps: int = 100) -> float:
        """Mean of maximum defuzzification."""
        dx = (max_val - min_val) / steps
        
        # Find maximum membership
        max_mu = 0.0
        max_points = []
        
        for i in range(steps):
            x = min_val + i * dx
            mu = membership_func(x)
            if mu > max_mu:
                max_mu = mu
                max_points = [x]
            elif mu == max_mu:
                max_points.append(x)
        
        if len(max_points) == 0:
            return (min_val + max_val) / 2
        
        return sum(max_points) / len(max_points)
    
    def _defuzzify_som(self, membership_func: Callable[[float], float],
                       min_val: float, max_val: float, steps: int = 100) -> float:
        """Smallest of maximum defuzzification."""
        dx = (max_val - min_val) / steps
        
        max_mu = 0.0
        first_max_point = max_val
        
        for i in range(steps):
            x = min_val + i * dx
            mu = membership_func(x)
            if mu > max_mu:
                max_mu = mu
                first_max_point = x
        
        return first_max_point
    
    def _defuzzify_lom(self, membership_func: Callable[[float], float],
                       min_val: float, max_val: float, steps: int = 100) -> float:
        """Largest of maximum defuzzification."""
        dx = (max_val - min_val) / steps
        
        max_mu = 0.0
        last_max_point = min_val
        
        for i in range(steps):
            x = min_val + i * dx
            mu = membership_func(x)
            if mu >= max_mu:
                max_mu = mu
                last_max_point = x
        
        return last_max_point


# ============================================================================
# Convenience Functions for Creating Fuzzy Sets
# ============================================================================

def create_triangular_set(name: str, a: Number, b: Number, c: Number,
                          universe_min: Number = None, universe_max: Number = None) -> FuzzySet:
    """Create a triangular fuzzy set."""
    a, b, c = float(a), float(b), float(c)
    umin = float(universe_min) if universe_min is not None else a
    umax = float(universe_max) if universe_max is not None else c
    return FuzzySet(name, lambda x: triangular_membership(x, a, b, c), umin, umax)


def create_trapezoidal_set(name: str, a: Number, b: Number, c: Number, d: Number,
                           universe_min: Number = None, universe_max: Number = None) -> FuzzySet:
    """Create a trapezoidal fuzzy set."""
    a, b, c, d = float(a), float(b), float(c), float(d)
    umin = float(universe_min) if universe_min is not None else a
    umax = float(universe_max) if universe_max is not None else d
    return FuzzySet(name, lambda x: trapezoidal_membership(x, a, b, c, d), umin, umax)


def create_gaussian_set(name: str, center: Number, sigma: Number,
                        universe_min: Number = None, universe_max: Number = None) -> FuzzySet:
    """Create a Gaussian fuzzy set."""
    center, sigma = float(center), float(sigma)
    umin = float(universe_min) if universe_min is not None else center - 4 * sigma
    umax = float(universe_max) if universe_max is not None else center + 4 * sigma
    return FuzzySet(name, lambda x: gaussian_membership(x, center, sigma), umin, umax)


def create_sigmoid_set(name: str, a: Number, c: Number,
                       universe_min: Number = None, universe_max: Number = None) -> FuzzySet:
    """Create a sigmoid fuzzy set."""
    a, c = float(a), float(c)
    umin = float(universe_min) if universe_min is not None else c - 10 / abs(a)
    umax = float(universe_max) if universe_max is not None else c + 10 / abs(a)
    return FuzzySet(name, lambda x: sigmoid_membership(x, a, c), umin, umax)


def create_bell_set(name: str, a: Number, b: Number, c: Number,
                    universe_min: Number = None, universe_max: Number = None) -> FuzzySet:
    """Create a generalized bell fuzzy set."""
    a, b, c = float(a), float(b), float(c)
    umin = float(universe_min) if universe_min is not None else c - 3 * a
    umax = float(universe_max) if universe_max is not None else c + 3 * a
    return FuzzySet(name, lambda x: bell_membership(x, a, b, c), umin, umax)


# ============================================================================
# Pre-built Linguistic Variables
# ============================================================================

def create_temperature_variable(universe_min: float = 0.0, universe_max: float = 100.0) -> LinguisticVariable:
    """
    Create a standard temperature linguistic variable.
    
    Sets: cold, cool, comfortable, warm, hot
    
    Example:
        >>> temp = create_temperature_variable(0, 100)
        >>> temp.get_membership(25, 'cool')
        0.5
    """
    var = LinguisticVariable("temperature", universe_min=universe_min, universe_max=universe_max)
    
    # Cold: triangular (0, 0, 30)
    var.add_fuzzy_set("cold", lambda x: triangular_membership(x, 0, 0, 30))
    
    # Cool: triangular (10, 30, 50)
    var.add_fuzzy_set("cool", lambda x: triangular_membership(x, 10, 30, 50))
    
    # Comfortable: triangular (30, 50, 70)
    var.add_fuzzy_set("comfortable", lambda x: triangular_membership(x, 30, 50, 70))
    
    # Warm: triangular (50, 70, 90)
    var.add_fuzzy_set("warm", lambda x: triangular_membership(x, 50, 70, 90))
    
    # Hot: triangular (70, 100, 100)
    var.add_fuzzy_set("hot", lambda x: triangular_membership(x, 70, 100, 100))
    
    return var


def create_speed_variable(universe_min: float = 0.0, universe_max: float = 100.0) -> LinguisticVariable:
    """
    Create a standard speed linguistic variable.
    
    Sets: slow, medium, fast, very_fast
    
    Example:
        >>> speed = create_speed_variable(0, 120)
        >>> speed.get_membership(60, 'medium')
        1.0
    """
    var = LinguisticVariable("speed", universe_min=universe_min, universe_max=universe_max)
    
    # Slow: trapezoidal (0, 0, 20, 40)
    var.add_fuzzy_set("slow", lambda x: trapezoidal_membership(x, 0, 0, 20, 40))
    
    # Medium: triangular (20, 50, 80)
    var.add_fuzzy_set("medium", lambda x: triangular_membership(x, 20, 50, 80))
    
    # Fast: triangular (50, 80, 100)
    var.add_fuzzy_set("fast", lambda x: triangular_membership(x, 50, 80, 100))
    
    # Very Fast: trapezoidal (80, 100, 100, 100)
    var.add_fuzzy_set("very_fast", lambda x: trapezoidal_membership(x, 80, 100, 100, 100))
    
    return var


def create_age_variable(universe_min: float = 0.0, universe_max: float = 100.0) -> LinguisticVariable:
    """
    Create a standard age linguistic variable.
    
    Sets: young, middle_aged, old, very_old
    
    Example:
        >>> age = create_age_variable(0, 100)
        >>> age.get_membership(30, 'young')
        0.5
    """
    var = LinguisticVariable("age", universe_min=universe_min, universe_max=universe_max)
    
    # Young: trapezoidal (0, 0, 20, 40)
    var.add_fuzzy_set("young", lambda x: trapezoidal_membership(x, 0, 0, 20, 40))
    
    # Middle-aged: triangular (30, 50, 70)
    var.add_fuzzy_set("middle_aged", lambda x: triangular_membership(x, 30, 50, 70))
    
    # Old: triangular (50, 70, 90)
    var.add_fuzzy_set("old", lambda x: triangular_membership(x, 50, 70, 90))
    
    # Very Old: trapezoidal (80, 100, 100, 100)
    var.add_fuzzy_set("very_old", lambda x: trapezoidal_membership(x, 80, 100, 100, 100))
    
    return var


def create_risk_variable(universe_min: float = 0.0, universe_max: float = 1.0) -> LinguisticVariable:
    """
    Create a standard risk linguistic variable.
    
    Sets: low, medium, high, critical
    
    Example:
        >>> risk = create_risk_variable(0, 1)
        >>> risk.get_membership(0.5, 'medium')
        1.0
    """
    var = LinguisticVariable("risk", universe_min=universe_min, universe_max=universe_max)
    
    # Low: triangular (0, 0, 0.3)
    var.add_fuzzy_set("low", lambda x: triangular_membership(x, 0, 0, 0.3))
    
    # Medium: triangular (0.2, 0.5, 0.8)
    var.add_fuzzy_set("medium", lambda x: triangular_membership(x, 0.2, 0.5, 0.8))
    
    # High: triangular (0.5, 0.7, 0.9)
    var.add_fuzzy_set("high", lambda x: triangular_membership(x, 0.5, 0.7, 0.9))
    
    # Critical: triangular (0.8, 1, 1)
    var.add_fuzzy_set("critical", lambda x: triangular_membership(x, 0.8, 1, 1))
    
    return var


# ============================================================================
# Fuzzy Controller Example
# ============================================================================

def create_temperature_controller() -> FuzzyInferenceSystem:
    """
    Create a fuzzy temperature controller.
    
    Input: temperature (0-100)
    Output: fan_speed (0-100)
    
    Rules:
        - IF temp IS cold THEN fan IS off
        - IF temp IS cool THEN fan IS slow
        - IF temp IS comfortable THEN fan IS medium
        - IF temp IS warm THEN fan IS fast
        - IF temp IS hot THEN fan IS very_fast
    
    Example:
        >>> controller = create_temperature_controller()
        >>> controller.evaluate({'temperature': 75})
        {'fan_speed': 75.0}
    """
    # Create input variable
    temp = create_temperature_variable(0, 100)
    
    # Create output variable
    fan = LinguisticVariable("fan_speed", universe_min=0, universe_max=100)
    fan.add_fuzzy_set("off", lambda x: triangular_membership(x, 0, 0, 20))
    fan.add_fuzzy_set("slow", lambda x: triangular_membership(x, 5, 25, 45))
    fan.add_fuzzy_set("medium", lambda x: triangular_membership(x, 30, 50, 70))
    fan.add_fuzzy_set("fast", lambda x: triangular_membership(x, 55, 75, 95))
    fan.add_fuzzy_set("very_fast", lambda x: triangular_membership(x, 80, 100, 100))
    
    # Create system
    system = FuzzyInferenceSystem("temperature_controller")
    system.add_input_variable(temp)
    system.add_output_variable(fan)
    
    # Add rules
    system.add_rule({"temperature": "cold"}, {"fan_speed": "off"})
    system.add_rule({"temperature": "cool"}, {"fan_speed": "slow"})
    system.add_rule({"temperature": "comfortable"}, {"fan_speed": "medium"})
    system.add_rule({"temperature": "warm"}, {"fan_speed": "fast"})
    system.add_rule({"temperature": "hot"}, {"fan_speed": "very_fast"})
    
    return system


# ============================================================================
# Utility Functions
# ============================================================================

def fuzzy_and(*values: MembershipValue, operator: FuzzyOperator = FuzzyOperator.MIN) -> MembershipValue:
    """Fuzzy AND for multiple values."""
    if len(values) == 0:
        return 0.0
    result = float(values[0])
    for v in values[1:]:
        result = fuzzy_intersection(result, float(v), operator)
    return result


def fuzzy_or(*values: MembershipValue, operator: FuzzyOperator = FuzzyOperator.MAX) -> MembershipValue:
    """Fuzzy OR for multiple values."""
    if len(values) == 0:
        return 0.0
    result = float(values[0])
    for v in values[1:]:
        result = fuzzy_union(result, float(v), operator)
    return result


def fuzzy_not(value: MembershipValue) -> MembershipValue:
    """Fuzzy NOT."""
    return fuzzy_complement(float(value))


def fuzzy_implies(a: MembershipValue, b: MembershipValue, implication_type: str = "mamdani") -> MembershipValue:
    """
    Fuzzy implication.
    
    Args:
        a: Antecedent membership
        b: Consequent membership
        implication_type: "mamdani" (min) or "larsen" (product)
    
    Returns:
        Implication result
    """
    a, b = float(a), float(b)
    
    if implication_type == "mamdani":
        return min(a, b)
    elif implication_type == "larsen":
        return a * b
    else:
        return min(a, b)


# ============================================================================
# Module Exports
# ============================================================================

__all__ = [
    # Enums
    'FuzzyOperator', 'DefuzzificationMethod', 'HedgeType',
    
    # Type aliases
    'Number', 'MembershipValue', 'MembershipFunction',
    
    # Membership functions
    'triangular_membership', 'trapezoidal_membership', 'gaussian_membership',
    'gaussian2_membership', 'sigmoid_membership', 'bell_membership',
    's_shape_membership', 'z_shape_membership', 'pi_shape_membership',
    'singleton_membership', 'rectangular_membership', 'linear_membership',
    'linear_down_membership',
    
    # Fuzzy operations
    'fuzzy_union', 'fuzzy_intersection', 'fuzzy_complement', 'fuzzy_difference',
    'fuzzy_and', 'fuzzy_or', 'fuzzy_not', 'fuzzy_implies',
    
    # Hedges
    'apply_hedge', 'hedge_function',
    
    # Classes
    'FuzzySet', 'LinguisticVariable', 'FuzzyRule', 'FuzzyInferenceSystem',
    
    # Convenience functions
    'create_triangular_set', 'create_trapezoidal_set', 'create_gaussian_set',
    'create_sigmoid_set', 'create_bell_set',
    
    # Pre-built variables
    'create_temperature_variable', 'create_speed_variable',
    'create_age_variable', 'create_risk_variable',
    
    # Controllers
    'create_temperature_controller',
]


if __name__ == '__main__':
    print("AllToolkit - Fuzzy Logic Utilities Demo")
    print("=" * 50)
    
    # Basic membership functions
    print("\nMembership Functions:")
    print(f"  Triangular(5, 0, 5, 10): {triangular_membership(5, 0, 5, 10)}")
    print(f"  Trapezoidal(5, 0, 3, 7, 10): {trapezoidal_membership(5, 0, 3, 7, 10)}")
    print(f"  Gaussian(5, 5, 2): {gaussian_membership(5, 5, 2):.4f}")
    print(f"  Sigmoid(5, 2, 5): {sigmoid_membership(5, 2, 5):.4f}")
    
    # Fuzzy operations
    print("\nFuzzy Operations:")
    print(f"  Union(0.3, 0.7): {fuzzy_union(0.3, 0.7)}")
    print(f"  Intersection(0.3, 0.7): {fuzzy_intersection(0.3, 0.7)}")
    print(f"  Complement(0.3): {fuzzy_complement(0.3)}")
    
    # Hedges
    print("\nHedges:")
    print(f"  Very(0.5): {apply_hedge(0.5, HedgeType.VERY)}")
    print(f"  Slightly(0.5): {apply_hedge(0.5, HedgeType.SLIGHTLY):.4f}")
    
    # Linguistic variable
    print("\nLinguistic Variable (Temperature):")
    temp = create_temperature_variable(0, 100)
    print(f"  25°C -> {temp.get_all_memberships(25)}")
    print(f"  50°C -> {temp.get_all_memberships(50)}")
    print(f"  75°C -> {temp.get_all_memberships(75)}")
    
    # Fuzzy controller
    print("\nFuzzy Temperature Controller:")
    controller = create_temperature_controller()
    for temp_val in [15, 30, 50, 70, 85]:
        result = controller.evaluate({'temperature': temp_val})
        print(f"  Temperature {temp_val}°C -> Fan speed: {result['fan_speed']:.2f}")
    
    print("\nFor full documentation, see README.md")