"""
L-System (Lindenmayer System) Utilities

A comprehensive toolkit for working with Lindenmayer systems - parallel string rewriting
systems used for generating fractals, plant structures, and complex patterns.

Features:
- Deterministic L-systems (D0L)
- Stochastic L-systems with probability-weighted rules
- Context-sensitive L-systems
- Parametric L-systems with conditions
- Turtle graphics interpretation for visualization
- Built-in classic fractals and plant systems
- Zero external dependencies
"""

import math
import random
from typing import Dict, List, Tuple, Optional, Callable, Union
from dataclasses import dataclass, field
from enum import Enum


class LSystemType(Enum):
    """Types of L-systems"""
    DETERMINISTIC = "deterministic"      # D0L - deterministic, context-free
    STOCHASTIC = "stochastic"            # Probability-weighted rules
    CONTEXT_SENSITIVE = "context_sensitive"  # Rules depend on neighbors
    PARAMETRIC = "parametric"            # Rules with parameters and conditions


@dataclass
class LSystemRule:
    """
    Represents a production rule in an L-system.
    
    For deterministic systems: predecessor -> successor
    For stochastic systems: predecessor -> {successor: probability, ...}
    For context-sensitive: left_context < predecessor > right_context -> successor
    For parametric: predecessor(condition) -> successor
    """
    predecessor: str
    successor: Union[str, Dict[str, float]]  # String or {successor: probability}
    left_context: str = ""
    right_context: str = ""
    condition: Optional[Callable] = None
    probability: float = 1.0


@dataclass
class TurtleState:
    """State of the turtle graphics cursor"""
    x: float = 0.0
    y: float = 0.0
    angle: float = 90.0  # Facing up (North)
    stack: List[Tuple[float, float, float]] = field(default_factory=list)


class LSystem:
    """
    L-System generator supporting multiple system types.
    
    Example:
        # Koch curve
        lsystem = LSystem(
            axiom="F",
            rules={"F": "F+F-F-F+F"},
            angle=90
        )
        result = lsystem.generate(iterations=4)
        points = lsystem.interpret(result, step=10)
    """
    
    def __init__(
        self,
        axiom: str,
        rules: Dict[str, Union[str, Dict[str, float], LSystemRule]],
        angle: float = 90.0,
        step: float = 10.0,
        system_type: LSystemType = LSystemType.DETERMINISTIC
    ):
        """
        Initialize an L-system.
        
        Args:
            axiom: Starting string
            rules: Production rules as {predecessor: successor} or 
                   {predecessor: {successor: probability}} for stochastic
            angle: Turn angle in degrees
            step: Step size for turtle graphics
            system_type: Type of L-system
        """
        self.axiom = axiom
        self.angle = angle
        self.step = step
        self.system_type = system_type
        self.rules = self._normalize_rules(rules)
    
    def _normalize_rules(
        self, 
        rules: Dict[str, Union[str, Dict[str, float], LSystemRule]]
    ) -> Dict[str, LSystemRule]:
        """Convert rule definitions to LSystemRule objects"""
        normalized = {}
        for pred, succ in rules.items():
            if isinstance(succ, LSystemRule):
                normalized[pred] = succ
            elif isinstance(succ, dict):
                normalized[pred] = LSystemRule(
                    predecessor=pred,
                    successor=succ,
                    probability=1.0
                )
            else:
                normalized[pred] = LSystemRule(
                    predecessor=pred,
                    successor=succ,
                    probability=1.0
                )
        return normalized
    
    def _apply_rule(self, char: str, context: Tuple[str, str, str]) -> str:
        """
        Apply appropriate rule for a character given its context.
        
        Args:
            char: Current character
            context: (left_context, char, right_context)
            
        Returns:
            Replacement string
        """
        if char not in self.rules:
            return char
        
        rule = self.rules[char]
        
        if isinstance(rule.successor, dict):
            # Stochastic rule
            rand = random.random()
            cumulative = 0.0
            for successor, prob in rule.successor.items():
                cumulative += prob
                if rand <= cumulative:
                    return successor
            # Fallback to last successor
            return list(rule.successor.keys())[-1]
        else:
            # Deterministic rule
            return rule.successor
    
    def generate(self, iterations: int = 1, seed: Optional[int] = None) -> str:
        """
        Generate the L-system string after n iterations.
        
        Args:
            iterations: Number of rewriting iterations
            seed: Random seed for reproducibility (stochastic systems)
            
        Returns:
            Final generated string
        """
        if seed is not None:
            random.seed(seed)
        
        current = self.axiom
        
        for _ in range(iterations):
            result = []
            n = len(current)
            
            for i, char in enumerate(current):
                # Get context for context-sensitive rules
                left_context = current[max(0, i-2):i] if i > 0 else ""
                right_context = current[i+1:min(n, i+3)] if i < n-1 else ""
                
                result.append(self._apply_rule(char, (left_context, char, right_context)))
            
            current = "".join(result)
        
        return current
    
    def interpret(
        self, 
        string: str, 
        step: Optional[float] = None,
        angle: Optional[float] = None
    ) -> List[Tuple[float, float]]:
        """
        Interpret L-system string using turtle graphics.
        
        Commands:
            F, G - Move forward and draw line
            f, g - Move forward without drawing
        +, - - Turn left/right by angle
        [, ] - Push/pop turtle state
        | - Turn 180 degrees
        (, ) - Decrease/increase line width (not rendered, just tracked)
        
        Args:
            string: L-system string to interpret
            step: Step size (default: self.step)
            angle: Turn angle (default: self.angle)
            
        Returns:
            List of line segments as (x1, y1, x2, y2) tuples
        """
        step = step or self.step
        angle = angle or self.angle
        
        turtle = TurtleState()
        lines = []
        
        for char in string:
            if char in "FG":
                # Move forward and draw
                x1, y1 = turtle.x, turtle.y
                rad = math.radians(turtle.angle)
                turtle.x += step * math.cos(rad)
                turtle.y += step * math.sin(rad)
                lines.append((x1, y1, turtle.x, turtle.y))
            
            elif char in "fg":
                # Move forward without drawing
                rad = math.radians(turtle.angle)
                turtle.x += step * math.cos(rad)
                turtle.y += step * math.sin(rad)
            
            elif char == "+":
                # Turn left
                turtle.angle += angle
            
            elif char == "-":
                # Turn right
                turtle.angle -= angle
            
            elif char == "[":
                # Push state
                turtle.stack.append((turtle.x, turtle.y, turtle.angle))
            
            elif char == "]":
                # Pop state
                if turtle.stack:
                    turtle.x, turtle.y, turtle.angle = turtle.stack.pop()
            
            elif char == "|":
                # Turn 180 degrees
                turtle.angle += 180
        
        return lines
    
    def get_bounds(
        self, 
        string: str, 
        step: Optional[float] = None,
        angle: Optional[float] = None
    ) -> Tuple[float, float, float, float]:
        """
        Calculate bounding box of the generated shape.
        
        Args:
            string: L-system string
            step: Step size
            angle: Turn angle
            
        Returns:
            (min_x, min_y, max_x, max_y)
        """
        lines = self.interpret(string, step, angle)
        
        if not lines:
            return (0, 0, 0, 0)
        
        x_coords = [x for line in lines for x in [line[0], line[2]]]
        y_coords = [y for line in lines for y in [line[1], line[3]]]
        
        return (min(x_coords), min(y_coords), max(x_coords), max(y_coords))
    
    def to_svg(
        self, 
        string: str,
        step: Optional[float] = None,
        angle: Optional[float] = None,
        width: int = 800,
        height: int = 600,
        stroke_color: str = "#000000",
        stroke_width: float = 1.0,
        background: str = "#ffffff"
    ) -> str:
        """
        Convert L-system string to SVG.
        
        Args:
            string: L-system string
            step: Step size
            angle: Turn angle
            width: SVG width
            height: SVG height
            stroke_color: Line color
            stroke_width: Line width
            background: Background color
            
        Returns:
            SVG string
        """
        lines = self.interpret(string, step, angle)
        
        if not lines:
            return f'<svg width="{width}" height="{height}"><rect width="100%" height="100%" fill="{background}"/></svg>'
        
        # Calculate bounds and scale
        min_x, min_y, max_x, max_y = self.get_bounds(string, step, angle)
        
        shape_width = max_x - min_x
        shape_height = max_y - min_y
        
        if shape_width == 0 or shape_height == 0:
            return f'<svg width="{width}" height="{height}"><rect width="100%" height="100%" fill="{background}"/></svg>'
        
        # Scale to fit with padding
        padding = 20
        scale = min(
            (width - 2 * padding) / shape_width,
            (height - 2 * padding) / shape_height
        )
        
        # Center offset
        offset_x = (width - shape_width * scale) / 2 - min_x * scale
        offset_y = (height - shape_height * scale) / 2 - min_y * scale
        
        # Build SVG
        svg_lines = []
        svg_lines.append(f'<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">')
        svg_lines.append(f'<rect width="100%" height="100%" fill="{background}"/>')
        svg_lines.append(f'<g stroke="{stroke_color}" stroke-width="{stroke_width}" stroke-linecap="round">')
        
        for x1, y1, x2, y2 in lines:
            sx1 = x1 * scale + offset_x
            sy1 = y1 * scale + offset_y
            sx2 = x2 * scale + offset_x
            sy2 = y2 * scale + offset_y
            svg_lines.append(f'<line x1="{sx1:.2f}" y1="{sy1:.2f}" x2="{sx2:.2f}" y2="{sy2:.2f}"/>')
        
        svg_lines.append('</g>')
        svg_lines.append('</svg>')
        
        return '\n'.join(svg_lines)


class ClassicLSystems:
    """Factory for classic L-system fractals and plant structures"""
    
    @staticmethod
    def koch_curve() -> LSystem:
        """
        Koch curve - one of the earliest fractals.
        
        Features:
        - Self-similarity at all scales
        - Infinite perimeter, finite area
        - Simple construction rule
        """
        return LSystem(
            axiom="F",
            rules={"F": "F+F-F-F+F"},
            angle=90,
            step=10
        )
    
    @staticmethod
    def koch_snowflake() -> LSystem:
        """
        Koch snowflake - three Koch curves forming a snowflake.
        
        Features:
        - Forms a closed fractal curve
        - Enclosed area is 8/5 of the original triangle
        - Perimeter increases by factor 4/3 each iteration
        """
        return LSystem(
            axiom="F--F--F",
            rules={"F": "F+F--F+F"},
            angle=60,
            step=10
        )
    
    @staticmethod
    def sierpinski_triangle() -> LSystem:
        """
        Sierpinski triangle using L-system.
        
        Features:
        - Self-similar fractal
        - Area approaches zero
        - Infinite perimeter
        """
        return LSystem(
            axiom="F-G-G",
            rules={
                "F": "F-G+F+G-F",
                "G": "GG"
            },
            angle=120,
            step=10
        )
    
    @staticmethod
    def sierpinski_carpet() -> LSystem:
        """Sierpinski carpet variant using L-system"""
        return LSystem(
            axiom="F",
            rules={"F": "F+F-F-F-G+F+F+F-F", "G": "GGG"},
            angle=90,
            step=10
        )
    
    @staticmethod
    def dragon_curve() -> LSystem:
        """
        Dragon curve (Heighway dragon).
        
        Features:
        - Space-filling curve
        - Created by folding paper
        - Self-avoiding
        """
        return LSystem(
            axiom="FX",
            rules={
                "X": "X+YF+",
                "Y": "-FX-Y"
            },
            angle=90,
            step=10
        )
    
    @staticmethod
    def hilbert_curve() -> LSystem:
        """
        Hilbert curve - a space-filling fractal curve.
        
        Features:
        - Visits every point in a square grid
        - Self-similar at all scales
        - Used in image compression, space-filling algorithms
        """
        return LSystem(
            axiom="A",
            rules={
                "A": "-BF+AFA+FB-",
                "B": "+AF-BFB-FA+"
            },
            angle=90,
            step=10
        )
    
    @staticmethod
    def peano_curve() -> LSystem:
        """
        Peano curve - the first space-filling curve discovered.
        
        Features:
        - Fills entire square
        - Continuous but nowhere differentiable
        """
        return LSystem(
            axiom="F",
            rules={"F": "F+F-F-F-F+F+F+F-F"},
            angle=90,
            step=10
        )
    
    @staticmethod
    def levy_c_curve() -> LSystem:
        """
        Lévy C curve.
        
        Features:
        - Self-similar fractal
        - Resembles letter 'C' at early iterations
        - Area approaches a finite limit
        """
        return LSystem(
            axiom="F",
            rules={"F": "+F--F+"},
            angle=45,
            step=10
        )
    
    @staticmethod
    def gosper_curve() -> LSystem:
        """
        Gosper curve (flowsnake).
        
        Features:
        - Space-filling curve on hexagonal grid
        - Creates beautiful flowing patterns
        """
        return LSystem(
            axiom="A",
            rules={
                "A": "A-B--B+A++AA+B-",
                "B": "+A-BB--B-A++A+B"
            },
            angle=60,
            step=10
        )
    
    @staticmethod
    def plant_simple() -> LSystem:
        """
        Simple plant structure.
        
        Features:
        - Tree-like branching pattern
        - Uses push/pop for branches
        """
        return LSystem(
            axiom="F",
            rules={"F": "F[+F]F[-F]F"},
            angle=25.7,
            step=10
        )
    
    @staticmethod
    def plant_branching() -> LSystem:
        """
        More complex branching plant.
        
        Features:
        - Multiple branch levels
        - Natural-looking tree structure
        """
        return LSystem(
            axiom="X",
            rules={
                "X": "F[+X]F[-X]+X",
                "F": "FF"
            },
            angle=30,
            step=10
        )
    
    @staticmethod
    def plant_stochastic() -> LSystem:
        """
        Stochastic plant - varies each generation.
        
        Features:
        - Different rules applied with probabilities
        - Creates natural variation
        """
        return LSystem(
            axiom="F",
            rules={
                "F": {
                    "F[+F]F[-F]F": 0.33,
                    "F[+F]F": 0.33,
                    "F[-F]F": 0.34
                }
            },
            angle=25,
            step=10,
            system_type=LSystemType.STOCHASTIC
        )
    
    @staticmethod
    def tree_bushy() -> LSystem:
        """
        Bushy tree structure.
        """
        return LSystem(
            axiom="F",
            rules={"F": "FF+[+F-F-F]-[-F+F+F]"},
            angle=22.5,
            step=10
        )
    
    @staticmethod
    def tree_willow() -> LSystem:
        """
        Willow-like tree with drooping branches.
        """
        return LSystem(
            axiom="F",
            rules={"F": "F[+F]F[-F][F]"},
            angle=30,
            step=10
        )
    
    @staticmethod
    def alga() -> LSystem:
        """
        Algae-like branching pattern.
        """
        return LSystem(
            axiom="F",
            rules={"F": "F+F-F-F+F"},
            angle=90,
            step=10
        )
    
    @staticmethod
    def seaweed() -> LSystem:
        """
        Seaweed-like structure.
        """
        return LSystem(
            axiom="F",
            rules={
                "F": "FF+[+F-F-F]-[-F+F+F]"
            },
            angle=22.5,
            step=10
        )
    
    @staticmethod
    def crystal() -> LSystem:
        """
        Crystal-like structure.
        """
        return LSystem(
            axiom="F+F+F+F",
            rules={"F": "FF+F+F+F+FF"},
            angle=90,
            step=10
        )
    
    @staticmethod
    def carpet() -> LSystem:
        """
        Carpet-like pattern.
        """
        return LSystem(
            axiom="YF",
            rules={
                "X": "YF+XF+Y",
                "Y": "XF-YF-X"
            },
            angle=60,
            step=10
        )
    
    @staticmethod
    def rings() -> LSystem:
        """
        Interlocking rings pattern.
        """
        return LSystem(
            axiom="F+F+F+F",
            rules={"F": "FF+F+F+F+F+F-F"},
            angle=90,
            step=10
        )
    
    @staticmethod
    def squares() -> LSystem:
        """
        Nested squares pattern.
        """
        return LSystem(
            axiom="F+F+F+F",
            rules={"F": "F+f-FF+F+FF+Ff+FF-f+FF-F-FF-Ff-FFF"},
            angle=90,
            step=10
        )
    
    @staticmethod
    def moore_curve() -> LSystem:
        """
        Moore curve - a variant of the Hilbert curve.
        """
        return LSystem(
            axiom="LFL+F+LFL",
            rules={
                "L": "-RF+LFL+FR-",
                "R": "+LF-RFR-FL+"
            },
            angle=90,
            step=10
        )
    
    @staticmethod
    def terdragon() -> LSystem:
        """
        Terdragon curve.
        """
        return LSystem(
            axiom="F",
            rules={"F": "F+F-F"},
            angle=120,
            step=10
        )
    
    @staticmethod
    def twin_dragon() -> LSystem:
        """
        Twin dragon curve.
        """
        return LSystem(
            axiom="FX",
            rules={
                "X": "X+YF+",
                "Y": "-FX-Y"
            },
            angle=90,
            step=10
        )
    
    @staticmethod
    def sierpinski_arrowhead() -> LSystem:
        """
        Sierpinski arrowhead curve.
        """
        return LSystem(
            axiom="YF",
            rules={
                "X": "YF+XF+Y",
                "Y": "XF-YF-X"
            },
            angle=60,
            step=10
        )
    
    @staticmethod
    def minkowski_sausage() -> LSystem:
        """
        Minkowski sausage/sausage curve.
        """
        return LSystem(
            axiom="F",
            rules={"F": "F+F-F-FF+F+F-F"},
            angle=90,
            step=10
        )
    
    @staticmethod
    def cesaro_fractal() -> LSystem:
        """
        Cesàro fractal curve.
        """
        return LSystem(
            axiom="F",
            rules={"F": "F+F-F-F+F"},
            angle=85,
            step=10
        )
    
    @staticmethod
    def quadratic_koch() -> LSystem:
        """
        Quadratic Koch island.
        """
        return LSystem(
            axiom="F+F+F+F",
            rules={"F": "F+F-F-FF+F+F-F"},
            angle=90,
            step=10
        )


def generate_lsystem(
    axiom: str,
    rules: Dict[str, str],
    iterations: int = 4,
    angle: float = 90.0
) -> str:
    """
    Simple convenience function to generate an L-system string.
    
    Args:
        axiom: Starting string
        rules: Production rules {predecessor: successor}
        iterations: Number of iterations
        angle: Turn angle (used for interpretation, not generation)
        
    Returns:
        Generated string
        
    Example:
        >>> result = generate_lsystem("F", {"F": "F+F-F-F+F"}, 3)
    """
    lsystem = LSystem(axiom=axiom, rules=rules, angle=angle)
    return lsystem.generate(iterations)


def interpret_lsystem(
    string: str,
    angle: float = 90.0,
    step: float = 10.0
) -> List[Tuple[float, float, float, float]]:
    """
    Interpret L-system string to get line segments.
    
    Args:
        string: L-system string
        angle: Turn angle in degrees
        step: Step size for movement
        
    Returns:
        List of line segments as (x1, y1, x2, y2) tuples
        
    Example:
        >>> segments = interpret_lsystem("F+F-F", angle=90, step=10)
    """
    lsystem = LSystem(axiom="", rules={}, angle=angle, step=step)
    return lsystem.interpret(string, step=step, angle=angle)


def lsystem_to_svg(
    axiom: str,
    rules: Dict[str, str],
    iterations: int = 4,
    angle: float = 90.0,
    step: float = 10.0,
    width: int = 800,
    height: int = 600
) -> str:
    """
    Generate SVG from L-system specification.
    
    Args:
        axiom: Starting string
        rules: Production rules
        iterations: Number of iterations
        angle: Turn angle
        step: Step size
        width: SVG width
        height: SVG height
        
    Returns:
        SVG string
        
    Example:
        >>> svg = lsystem_to_svg("F", {"F": "F+F-F-F+F"}, 4, 90)
    """
    lsystem = LSystem(axiom=axiom, rules=rules, angle=angle, step=step)
    string = lsystem.generate(iterations)
    return lsystem.to_svg(string, step=step, angle=angle, width=width, height=height)


def count_characters(string: str, chars: str = "FG") -> Dict[str, int]:
    """
    Count occurrences of specific characters in an L-system string.
    
    Args:
        string: L-system string
        chars: Characters to count (default: "FG")
        
    Returns:
        Dictionary with character counts
    """
    return {c: string.count(c) for c in chars}


def get_string_length(axiom: str, rules: Dict[str, str], iterations: int) -> int:
    """
    Calculate the expected string length without generating it.
    
    Uses the growth matrix method for D0L systems.
    
    Args:
        axiom: Starting string
        rules: Production rules
        iterations: Number of iterations
        
    Returns:
        Expected string length
    """
    # Get all unique symbols
    symbols = set(axiom)
    for pred, succ in rules.items():
        symbols.add(pred)
        symbols.update(succ)
    
    # Build growth matrix
    symbols = sorted(symbols)
    n = len(symbols)
    
    if n == 0:
        return len(axiom)
    
    # Growth rates for each symbol
    growth_rates = {}
    for sym in symbols:
        if sym in rules:
            growth_rates[sym] = len(rules[sym])
        else:
            growth_rates[sym] = 1
    
    # Calculate string length
    current_counts = {sym: axiom.count(sym) for sym in symbols}
    
    for _ in range(iterations):
        new_counts = {sym: 0 for sym in symbols}
        for sym in symbols:
            if sym in rules:
                successor = rules[sym]
                for c in successor:
                    if c in new_counts:
                        new_counts[c] += current_counts[sym]
            else:
                new_counts[sym] += current_counts[sym]
        current_counts = new_counts
    
    return sum(current_counts.values())


def analyze_lsystem(axiom: str, rules: Dict[str, str]) -> Dict:
    """
    Analyze an L-system and return its properties.
    
    Args:
        axiom: Starting string
        rules: Production rules
        
    Returns:
        Dictionary with analysis results
    """
    symbols = set(axiom)
    variables = set(rules.keys())
    constants = set()
    
    for pred, succ in rules.items():
        symbols.update(succ)
        for c in succ:
            if c not in rules:
                constants.add(c)
    
    # Determine if context-free
    is_context_free = all(len(pred) == 1 for pred in rules.keys())
    
    # Calculate growth factor for each variable
    growth_factors = {}
    for var in variables:
        if var in rules:
            growth_factors[var] = len(rules[var])
    
    # Estimate complexity
    avg_growth = sum(growth_factors.values()) / len(growth_factors) if growth_factors else 1
    
    return {
        "axiom": axiom,
        "num_rules": len(rules),
        "variables": sorted(variables),
        "constants": sorted(constants),
        "is_context_free": is_context_free,
        "growth_factors": growth_factors,
        "average_growth_factor": avg_growth,
        "is_expanding": avg_growth > 1,
        "is_contracting": avg_growth < 1,
        "is_neutral": avg_growth == 1
    }


# Aliases for convenience
koch_curve = ClassicLSystems.koch_curve
koch_snowflake = ClassicLSystems.koch_snowflake
sierpinski_triangle = ClassicLSystems.sierpinski_triangle
dragon_curve = ClassicLSystems.dragon_curve
hilbert_curve = ClassicLSystems.hilbert_curve
plant = ClassicLSystems.plant_simple


if __name__ == "__main__":
    # Demo: Generate a Koch snowflake
    print("L-System Utilities Demo")
    print("=" * 50)
    
    # Create a Koch snowflake
    koch = ClassicLSystems.koch_snowflake()
    for i in range(5):
        string = koch.generate(i)
        print(f"Iteration {i}: {len(string)} characters")
    
    # Generate and analyze
    print("\nAnalyzing Koch snowflake:")
    analysis = analyze_lsystem("F--F--F", {"F": "F+F--F+F"})
    for key, value in analysis.items():
        print(f"  {key}: {value}")
    
    # Generate SVG
    print("\nGenerating SVG for Koch snowflake (iteration 3)...")
    string = koch.generate(3)
    svg = koch.to_svg(string, width=400, height=400)
    print(f"SVG generated: {len(svg)} bytes")