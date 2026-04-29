"""
Comprehensive tests for L-System Utilities
"""

import unittest
import math
from mod import (
    LSystem, LSystemRule, LSystemType, TurtleState, ClassicLSystems,
    generate_lsystem, interpret_lsystem, lsystem_to_svg,
    count_characters, get_string_length, analyze_lsystem
)


class TestLSystemBasic(unittest.TestCase):
    """Basic L-system generation tests"""
    
    def test_simple_rule(self):
        """Test simple single rule"""
        lsystem = LSystem(axiom="F", rules={"F": "FF"})
        result = lsystem.generate(3)
        self.assertEqual(result, "FFFFFFFF")
    
    def test_multiple_rules(self):
        """Test multiple production rules"""
        lsystem = LSystem(
            axiom="AB",
            rules={"A": "AB", "B": "A"}
        )
        # AB -> ABA -> ABAAB -> ABAABABA
        self.assertEqual(lsystem.generate(0), "AB")
        self.assertEqual(lsystem.generate(1), "ABA")
        self.assertEqual(lsystem.generate(2), "ABAAB")
    
    def test_no_rule(self):
        """Test characters without rules remain unchanged"""
        lsystem = LSystem(axiom="F+F", rules={"F": "FF"})
        result = lsystem.generate(1)
        self.assertEqual(result, "FF+FF")
    
    def test_empty_axiom(self):
        """Test empty axiom"""
        lsystem = LSystem(axiom="", rules={"F": "FF"})
        result = lsystem.generate(5)
        self.assertEqual(result, "")
    
    def test_constant_rule(self):
        """Test rule that produces constant output"""
        lsystem = LSystem(axiom="F", rules={"F": "F"})
        result = lsystem.generate(10)
        self.assertEqual(result, "F")


class TestKochCurve(unittest.TestCase):
    """Test Koch curve generation"""
    
    def test_koch_iteration_0(self):
        """Test Koch curve at iteration 0"""
        koch = ClassicLSystems.koch_curve()
        result = koch.generate(0)
        self.assertEqual(result, "F")
    
    def test_koch_iteration_1(self):
        """Test Koch curve at iteration 1"""
        koch = ClassicLSystems.koch_curve()
        result = koch.generate(1)
        self.assertEqual(result, "F+F-F-F+F")
    
    def test_koch_iteration_2(self):
        """Test Koch curve at iteration 2"""
        koch = ClassicLSystems.koch_curve()
        result = koch.generate(2)
        # F -> F+F-F-F+F, each F expands to F+F-F-F+F
        expected = "F+F-F-F+F+F+F-F-F+F-F+F-F-F+F-F+F-F-F+F+F+F-F-F+F"
        self.assertEqual(result, expected)


class TestKochSnowflake(unittest.TestCase):
    """Test Koch snowflake generation"""
    
    def test_snowflake_iteration_0(self):
        """Test Koch snowflake at iteration 0"""
        snowflake = ClassicLSystems.koch_snowflake()
        result = snowflake.generate(0)
        self.assertEqual(result, "F--F--F")
    
    def test_snowflake_iteration_1(self):
        """Test Koch snowflake at iteration 1"""
        snowflake = ClassicLSystems.koch_snowflake()
        result = snowflake.generate(1)
        self.assertEqual(result, "F+F--F+F--F+F--F+F--F+F--F+F")


class TestSierpinskiTriangle(unittest.TestCase):
    """Test Sierpinski triangle generation"""
    
    def test_sierpinski_iteration_0(self):
        """Test Sierpinski triangle at iteration 0"""
        st = ClassicLSystems.sierpinski_triangle()
        result = st.generate(0)
        self.assertEqual(result, "F-G-G")
    
    def test_sierpinski_iteration_1(self):
        """Test Sierpinski triangle at iteration 1"""
        st = ClassicLSystems.sierpinski_triangle()
        result = st.generate(1)
        self.assertEqual(result, "F-G+F+G-F-GG-GG")


class TestDragonCurve(unittest.TestCase):
    """Test Dragon curve generation"""
    
    def test_dragon_iteration_0(self):
        """Test Dragon curve at iteration 0"""
        dragon = ClassicLSystems.dragon_curve()
        result = dragon.generate(0)
        self.assertEqual(result, "FX")
    
    def test_dragon_iteration_1(self):
        """Test Dragon curve at iteration 1"""
        dragon = ClassicLSystems.dragon_curve()
        result = dragon.generate(1)
        self.assertEqual(result, "FX+YF+")
    
    def test_dragon_iteration_2(self):
        """Test Dragon curve at iteration 2"""
        dragon = ClassicLSystems.dragon_curve()
        result = dragon.generate(2)
        self.assertEqual(result, "FX+YF++-FX-YF+")


class TestHilbertCurve(unittest.TestCase):
    """Test Hilbert curve generation"""
    
    def test_hilbert_iteration_0(self):
        """Test Hilbert curve at iteration 0"""
        hilbert = ClassicLSystems.hilbert_curve()
        result = hilbert.generate(0)
        self.assertEqual(result, "A")
    
    def test_hilbert_iteration_1(self):
        """Test Hilbert curve at iteration 1"""
        hilbert = ClassicLSystems.hilbert_curve()
        result = hilbert.generate(1)
        self.assertEqual(result, "-BF+AFA+FB-")


class TestPlantSystems(unittest.TestCase):
    """Test plant L-systems"""
    
    def test_simple_plant(self):
        """Test simple plant generation"""
        plant = ClassicLSystems.plant_simple()
        result = plant.generate(0)
        self.assertEqual(result, "F")
        
        result = plant.generate(1)
        self.assertEqual(result, "F[+F]F[-F]F")
    
    def test_branching_plant(self):
        """Test branching plant"""
        plant = ClassicLSystems.plant_branching()
        result = plant.generate(0)
        self.assertEqual(result, "X")
        
        result = plant.generate(1)
        self.assertEqual(result, "F[+X]F[-X]+X")


class TestTurtleInterpretation(unittest.TestCase):
    """Test turtle graphics interpretation"""
    
    def test_forward(self):
        """Test forward movement"""
        lsystem = LSystem(axiom="", rules={}, step=10)
        lines = lsystem.interpret("F")
        self.assertEqual(len(lines), 1)
        # Should be a vertical line going up (angle=90)
        self.assertEqual(lines[0][0], 0)  # x1
        self.assertEqual(lines[0][1], 0)  # y1
        self.assertAlmostEqual(lines[0][2], 0, places=5)  # x2
        self.assertAlmostEqual(lines[0][3], 10, places=5)  # y2
    
    def test_turn_right(self):
        """Test right turn"""
        lsystem = LSystem(axiom="", rules={}, step=10, angle=90)
        lines = lsystem.interpret("F-F")
        self.assertEqual(len(lines), 2)
        # First line goes up
        self.assertAlmostEqual(lines[0][3], 10, places=5)
        # Second line goes right (after 90 degree right turn)
        self.assertAlmostEqual(lines[1][2], 10, places=5)
        self.assertAlmostEqual(lines[1][3], 10, places=5)
    
    def test_turn_left(self):
        """Test left turn"""
        lsystem = LSystem(axiom="", rules={}, step=10, angle=90)
        lines = lsystem.interpret("F+F")
        self.assertEqual(len(lines), 2)
        # First line goes up
        # Second line goes left (after 90 degree left turn)
        self.assertAlmostEqual(lines[1][2], -10, places=5)
        self.assertAlmostEqual(lines[1][3], 10, places=5)
    
    def test_push_pop(self):
        """Test state push/pop"""
        lsystem = LSystem(axiom="", rules={}, step=10, angle=90)
        lines = lsystem.interpret("F[+F]F")
        self.assertEqual(len(lines), 3)
    
    def test_square(self):
        """Test drawing a square"""
        lsystem = LSystem(axiom="", rules={}, step=10, angle=90)
        lines = lsystem.interpret("F+F+F+F")
        self.assertEqual(len(lines), 4)
        # All lines should have same length
        for line in lines:
            length = math.sqrt((line[2]-line[0])**2 + (line[3]-line[1])**2)
            self.assertAlmostEqual(length, 10, places=5)
    
    def test_move_without_draw(self):
        """Test move without drawing (f, g)"""
        lsystem = LSystem(axiom="", rules={}, step=10)
        lines = lsystem.interpret("FfF")
        self.assertEqual(len(lines), 2)  # Only F draws
    
    def test_180_turn(self):
        """Test 180 degree turn"""
        lsystem = LSystem(axiom="", rules={}, step=10)
        lines = lsystem.interpret("F|F")
        self.assertEqual(len(lines), 2)
        # Second line should go back down
        self.assertAlmostEqual(lines[1][3], 0, places=5)


class TestStochasticLSystem(unittest.TestCase):
    """Test stochastic L-systems"""
    
    def test_stochastic_different_outputs(self):
        """Test that stochastic L-systems can produce different outputs"""
        lsystem = ClassicLSystems.plant_stochastic()
        
        # Generate multiple times with different seeds
        results = set()
        for seed in range(100):
            result = lsystem.generate(3, seed=seed)
            results.add(result)
            if len(results) > 1:
                break
        
        # At least one pair should be different
        self.assertGreater(len(results), 1)
    
    def test_stochastic_reproducible(self):
        """Test that same seed produces same output"""
        lsystem = ClassicLSystems.plant_stochastic()
        
        result1 = lsystem.generate(3, seed=42)
        result2 = lsystem.generate(3, seed=42)
        
        self.assertEqual(result1, result2)


class TestBounds(unittest.TestCase):
    """Test bounding box calculation"""
    
    def test_single_point(self):
        """Test bounds of single point"""
        lsystem = LSystem(axiom="", rules={}, step=10)
        bounds = lsystem.get_bounds("F")
        min_x, min_y, max_x, max_y = bounds
        self.assertAlmostEqual(min_x, 0, places=5)
        self.assertAlmostEqual(min_y, 0, places=5)
        self.assertAlmostEqual(max_x, 0, places=5)
        self.assertAlmostEqual(max_y, 10, places=5)
    
    def test_square_bounds(self):
        """Test bounds of a square"""
        lsystem = LSystem(axiom="", rules={}, step=10, angle=90)
        bounds = lsystem.get_bounds("F+F+F+F")
        min_x, min_y, max_x, max_y = bounds
        # Square drawn with left turns: goes up, left, down, right
        # So bounds are (-10, 0) to (0, 10)
        self.assertAlmostEqual(min_x, -10, places=5)
        self.assertAlmostEqual(min_y, 0, places=5)
        self.assertAlmostEqual(max_x, 0, places=5)
        self.assertAlmostEqual(max_y, 10, places=5)
    
    def test_empty_string_bounds(self):
        """Test bounds of empty string"""
        lsystem = LSystem(axiom="", rules={}, step=10)
        bounds = lsystem.get_bounds("")
        self.assertEqual(bounds, (0, 0, 0, 0))


class TestSVGGeneration(unittest.TestCase):
    """Test SVG generation"""
    
    def test_svg_contains_elements(self):
        """Test that SVG contains expected elements"""
        lsystem = LSystem(axiom="F", rules={"F": "FF"}, step=10)
        string = lsystem.generate(2)
        svg = lsystem.to_svg(string)
        
        self.assertIn("<svg", svg)
        self.assertIn("</svg>", svg)
        self.assertIn("<line", svg)
    
    def test_svg_dimensions(self):
        """Test SVG dimensions"""
        lsystem = LSystem(axiom="", rules={}, step=10)
        svg = lsystem.to_svg("F", width=400, height=300)
        
        self.assertIn('width="400"', svg)
        self.assertIn('height="300"', svg)
    
    def test_svg_colors(self):
        """Test SVG color customization"""
        lsystem = LSystem(axiom="", rules={}, step=10)
        svg = lsystem.to_svg("F", stroke_color="#FF0000", background="#000000")
        
        self.assertIn("#FF0000", svg)
        self.assertIn("#000000", svg)
    
    def test_empty_svg(self):
        """Test SVG for empty string"""
        lsystem = LSystem(axiom="", rules={}, step=10)
        svg = lsystem.to_svg("")
        
        self.assertIn("<svg", svg)
        self.assertIn("</svg>", svg)


class TestConvenienceFunctions(unittest.TestCase):
    """Test convenience functions"""
    
    def test_generate_lsystem(self):
        """Test generate_lsystem function"""
        result = generate_lsystem("F", {"F": "FF"}, 3)
        self.assertEqual(result, "FFFFFFFF")
    
    def test_interpret_lsystem(self):
        """Test interpret_lsystem function"""
        lines = interpret_lsystem("F+F", angle=90, step=10)
        self.assertEqual(len(lines), 2)
    
    def test_lsystem_to_svg(self):
        """Test lsystem_to_svg function"""
        svg = lsystem_to_svg("F", {"F": "FF"}, 2, 90, 10)
        self.assertIn("<svg", svg)
    
    def test_count_characters(self):
        """Test character counting"""
        counts = count_characters("FF+FF-FF", "FG+-")
        self.assertEqual(counts["F"], 6)
        self.assertEqual(counts["+"], 1)
        self.assertEqual(counts["-"], 1)
        self.assertEqual(counts["G"], 0)


class TestStringLengthPrediction(unittest.TestCase):
    """Test string length prediction"""
    
    def test_constant_length(self):
        """Test prediction for constant length"""
        length = get_string_length("F", {"F": "F"}, 10)
        self.assertEqual(length, 1)
    
    def test_doubling(self):
        """Test prediction for doubling"""
        length = get_string_length("F", {"F": "FF"}, 3)
        self.assertEqual(length, 8)  # 2^3
    
    def test_complex_rules(self):
        """Test prediction for complex rules"""
        # Fibonacci-like growth
        length = get_string_length("A", {"A": "AB", "B": "A"}, 0)
        self.assertEqual(length, 1)
        
        length = get_string_length("A", {"A": "AB", "B": "A"}, 1)
        self.assertEqual(length, 2)  # AB


class TestLSystemAnalysis(unittest.TestCase):
    """Test L-system analysis"""
    
    def test_analyze_simple(self):
        """Test analysis of simple L-system"""
        analysis = analyze_lsystem("F", {"F": "FF"})
        
        self.assertEqual(analysis["axiom"], "F")
        self.assertEqual(analysis["num_rules"], 1)
        self.assertEqual(analysis["variables"], ["F"])
        self.assertTrue(analysis["is_context_free"])
        self.assertTrue(analysis["is_expanding"])
    
    def test_analyze_koch(self):
        """Test analysis of Koch curve"""
        analysis = analyze_lsystem("F", {"F": "F+F-F-F+F"})
        
        self.assertEqual(analysis["num_rules"], 1)
        self.assertEqual(analysis["variables"], ["F"])
        self.assertEqual(analysis["constants"], ["+", "-"])
        self.assertTrue(analysis["is_expanding"])
    
    def test_analyze_dragon(self):
        """Test analysis of Dragon curve"""
        analysis = analyze_lsystem("FX", {"X": "X+YF+", "Y": "-FX-Y"})
        
        self.assertEqual(analysis["num_rules"], 2)
        self.assertIn("X", analysis["variables"])
        self.assertIn("Y", analysis["variables"])
        self.assertIn("F", analysis["constants"])


class TestClassicLSystems(unittest.TestCase):
    """Test all classic L-systems"""
    
    def test_all_classics_generate(self):
        """Test that all classic L-systems can generate strings"""
        classics = [
            ClassicLSystems.koch_curve,
            ClassicLSystems.koch_snowflake,
            ClassicLSystems.sierpinski_triangle,
            ClassicLSystems.sierpinski_carpet,
            ClassicLSystems.dragon_curve,
            ClassicLSystems.hilbert_curve,
            ClassicLSystems.peano_curve,
            ClassicLSystems.levy_c_curve,
            ClassicLSystems.gosper_curve,
            ClassicLSystems.plant_simple,
            ClassicLSystems.plant_branching,
            ClassicLSystems.plant_stochastic,
            ClassicLSystems.tree_bushy,
            ClassicLSystems.tree_willow,
            ClassicLSystems.alga,
            ClassicLSystems.seaweed,
            ClassicLSystems.crystal,
            ClassicLSystems.carpet,
            ClassicLSystems.rings,
            ClassicLSystems.squares,
            ClassicLSystems.moore_curve,
            ClassicLSystems.terdragon,
            ClassicLSystems.twin_dragon,
            ClassicLSystems.sierpinski_arrowhead,
            ClassicLSystems.minkowski_sausage,
            ClassicLSystems.cesaro_fractal,
            ClassicLSystems.quadratic_koch,
        ]
        
        for factory in classics:
            with self.subTest(factory=factory):
                lsystem = factory()
                result = lsystem.generate(3)
                self.assertIsInstance(result, str)
                self.assertGreater(len(result), 0)
    
    def test_all_classics_interpret(self):
        """Test that all classic L-systems can be interpreted"""
        classics = [
            ClassicLSystems.koch_curve,
            ClassicLSystems.koch_snowflake,
            ClassicLSystems.dragon_curve,
            ClassicLSystems.hilbert_curve,
        ]
        
        for factory in classics:
            with self.subTest(factory=factory):
                lsystem = factory()
                string = lsystem.generate(3)
                lines = lsystem.interpret(string)
                self.assertIsInstance(lines, list)
                self.assertGreater(len(lines), 0)


class TestTurtleState(unittest.TestCase):
    """Test TurtleState class"""
    
    def test_default_state(self):
        """Test default turtle state"""
        state = TurtleState()
        self.assertEqual(state.x, 0)
        self.assertEqual(state.y, 0)
        self.assertEqual(state.angle, 90)
        self.assertEqual(len(state.stack), 0)
    
    def test_custom_state(self):
        """Test custom turtle state"""
        state = TurtleState(x=10, y=20, angle=45)
        self.assertEqual(state.x, 10)
        self.assertEqual(state.y, 20)
        self.assertEqual(state.angle, 45)


class TestLSystemRule(unittest.TestCase):
    """Test LSystemRule class"""
    
    def test_deterministic_rule(self):
        """Test deterministic rule creation"""
        rule = LSystemRule(predecessor="F", successor="FF")
        self.assertEqual(rule.predecessor, "F")
        self.assertEqual(rule.successor, "FF")
        self.assertEqual(rule.probability, 1.0)
    
    def test_stochastic_rule(self):
        """Test stochastic rule creation"""
        rule = LSystemRule(
            predecessor="F",
            successor={"FF": 0.5, "F+F": 0.5}
        )
        self.assertIsInstance(rule.successor, dict)
        self.assertEqual(rule.successor["FF"], 0.5)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and error handling"""
    
    def test_deep_recursion(self):
        """Test deep recursion doesn't cause issues"""
        lsystem = LSystem(axiom="F", rules={"F": "FF"})
        # 15 iterations = 32768 F's
        result = lsystem.generate(15)
        self.assertEqual(len(result), 32768)
    
    def test_angle_0(self):
        """Test with zero angle"""
        lsystem = LSystem(axiom="", rules={}, angle=0, step=10)
        lines = lsystem.interpret("F+F+F")
        # All lines should be in same direction
        self.assertEqual(len(lines), 3)
    
    def test_negative_angle(self):
        """Test with negative angle"""
        lsystem = LSystem(axiom="", rules={}, angle=-90, step=10)
        lines = lsystem.interpret("F+F")
        self.assertEqual(len(lines), 2)
    
    def test_negative_step(self):
        """Test with negative step"""
        lsystem = LSystem(axiom="", rules={}, step=-10)
        lines = lsystem.interpret("F")
        self.assertEqual(len(lines), 1)
        # y should be negative
        self.assertAlmostEqual(lines[0][3], -10, places=5)
    
    def test_unbalanced_brackets(self):
        """Test with unbalanced brackets"""
        lsystem = LSystem(axiom="", rules={}, step=10)
        # Should handle gracefully
        lines = lsystem.interpret("F[[[F")
        self.assertGreater(len(lines), 0)
        
        lines = lsystem.interpret("F]]]F")
        self.assertGreater(len(lines), 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)