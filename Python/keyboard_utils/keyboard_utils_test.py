#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Keyboard Utils Test Suite
Tests for keyboard layout utilities
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from keyboard_utils.mod import (
    Finger, Hand, KeyPosition, TypingAnalysis,
    KeyboardLayout, KeyboardUtils,
    QWERTY_LAYOUT, DVORAK_LAYOUT, COLEMAK_LAYOUT, AZERTY_LAYOUT, QWERTZ_LAYOUT,
    distance, total_distance, analyze, get_key_position, get_coordinates,
    get_finger, get_hand, efficiency_score, get_keyboard_patterns,
    suggest_improvements, available_layouts, get_utils
)


class TestResultCollector:
    """Collects test results"""
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.tests = []
    
    def add_result(self, name, passed, message=""):
        self.tests.append((name, passed, message))
        if passed:
            self.passed += 1
        else:
            self.failed += 1
    
    def summary(self):
        total = self.passed + self.failed
        print(f"\n{'='*60}")
        print(f"Keyboard Utils Test Results: {self.passed}/{total} passed")
        print(f"{'='*60}")
        if self.failed > 0:
            print("Failed tests:")
            for name, passed, msg in self.tests:
                if not passed:
                    print(f"  - {name}: {msg}")
        return self.failed == 0


results = TestResultCollector()


def test_enums():
    """Test Finger and Hand enums"""
    try:
        assert Finger.LEFT_PINKY.value == "left_pinky"
        assert Finger.RIGHT_INDEX.value == "right_index"
        assert Hand.LEFT.value == "left"
        assert Hand.RIGHT.value == "right"
        assert Hand.BOTH.value == "both"
        results.add_result("enums", True)
    except Exception as e:
        results.add_result("enums", False, str(e))


def test_key_position_dataclass():
    """Test KeyPosition dataclass"""
    try:
        pos = KeyPosition(
            key="a",
            row=2,
            col=1,
            finger=Finger.LEFT_PINKY,
            hand=Hand.LEFT,
            shift_key="A"
        )
        assert pos.key == "a"
        assert pos.row == 2
        assert pos.finger == Finger.LEFT_PINKY
        results.add_result("key_position_dataclass", True)
    except Exception as e:
        results.add_result("key_position_dataclass", False, str(e))


def test_typing_analysis_dataclass():
    """Test TypingAnalysis dataclass"""
    try:
        analysis = TypingAnalysis(
            total_distance=10.0,
            average_distance=1.0,
            hand_alternations=5,
            same_hand_sequences=3,
            finger_usage={Finger.LEFT_PINKY: 2},
            hand_usage={Hand.LEFT: 5},
            rolling_sequences=2,
            home_row_usage=3,
            top_row_usage=2,
            bottom_row_usage=1,
            number_row_usage=0
        )
        assert analysis.total_distance == 10.0
        assert analysis.hand_alternations == 5
        results.add_result("typing_analysis_dataclass", True)
    except Exception as e:
        results.add_result("typing_analysis_dataclass", False, str(e))


def test_keyboard_layout():
    """Test KeyboardLayout class"""
    try:
        layout = KeyboardLayout(QWERTY_LAYOUT)
        assert layout.name == "QWERTY"
        
        # Get key position
        pos = layout.get_key_position("a")
        assert pos is not None
        assert pos.key.lower() == "a"
        
        # Get coordinates
        coord = layout.get_coordinates("a")
        assert coord is not None
        assert len(coord) == 2
        
        # Get finger
        finger = layout.get_finger("a")
        assert finger is not None
        
        # Get hand
        hand = layout.get_hand("a")
        assert hand is not None
        
        # Unknown character
        assert layout.get_key_position("unknown") is None
        results.add_result("keyboard_layout", True)
    except Exception as e:
        results.add_result("keyboard_layout", False, str(e))


def test_keyboard_utils_init():
    """Test KeyboardUtils initialization"""
    try:
        utils = KeyboardUtils("qwerty")
        assert utils.layout_name == "qwerty"
        
        # Invalid layout
        try:
            KeyboardUtils("invalid")
            results.add_result("keyboard_utils_init", False, "Should raise for invalid layout")
        except ValueError:
            pass
        results.add_result("keyboard_utils_init", True)
    except Exception as e:
        results.add_result("keyboard_utils_init", False, str(e))


def test_distance():
    """Test distance calculation"""
    try:
        utils = KeyboardUtils("qwerty")
        
        # Same key
        assert utils.distance("a", "a") == 0.0
        
        # Adjacent keys
        dist = utils.distance("a", "s")
        assert dist > 0 and dist < 2
        
        # Far keys
        dist_far = utils.distance("a", "p")
        assert dist_far > dist
        
        # Unknown characters
        assert utils.distance("a", "unknown") == float('inf')
        results.add_result("distance", True)
    except Exception as e:
        results.add_result("distance", False, str(e))


def test_total_distance():
    """Test total distance calculation"""
    try:
        utils = KeyboardUtils("qwerty")
        
        # Empty text
        assert utils.total_distance("") == 0.0
        
        # Single character
        assert utils.total_distance("a") == 0.0
        
        # Multiple characters
        total = utils.total_distance("asdf")
        assert total > 0
        
        # Convenience function
        total2 = total_distance("asdf", layout="qwerty")
        assert total2 == total
        results.add_result("total_distance", True)
    except Exception as e:
        results.add_result("total_distance", False, str(e))


def test_analyze():
    """Test typing analysis"""
    try:
        utils = KeyboardUtils("qwerty")
        
        # Empty text
        analysis = utils.analyze("")
        assert analysis.total_distance == 0.0
        assert analysis.hand_alternations == 0
        
        # Simple text
        analysis = utils.analyze("asdf")
        assert analysis.total_distance > 0
        assert len(analysis.finger_usage) > 0
        
        # Convenience function
        analysis2 = analyze("asdf", layout="qwerty")
        assert analysis2.total_distance == analysis.total_distance
        results.add_result("analyze", True)
    except Exception as e:
        results.add_result("analyze", False, str(e))


def test_same_hand_finger():
    """Test same hand/finger detection"""
    try:
        utils = KeyboardUtils("qwerty")
        
        # Same hand (left hand keys)
        assert utils.is_same_hand("a", "s") == True
        
        # Different hands
        assert utils.is_same_hand("a", "j") == False
        
        # Same finger (a and a)
        assert utils.is_same_finger("a", "a") == True
        
        # Different fingers
        assert utils.is_same_finger("a", "s") == False
        
        # Adjacent finger
        result = utils.is_adjacent_finger("a", "s")
        # Check result is boolean
        assert isinstance(result, bool)
        results.add_result("same_hand_finger", True)
    except Exception as e:
        results.add_result("same_hand_finger", False, str(e))


def test_row_detection():
    """Test row detection"""
    try:
        utils = KeyboardUtils("qwerty")
        
        # Home row keys
        assert utils.is_home_row("a") == True
        assert utils.is_home_row("s") == True
        
        # Top row keys
        assert utils.is_top_row("q") == True
        assert utils.is_top_row("w") == True
        
        # Bottom row keys
        assert utils.is_bottom_row("z") == True
        assert utils.is_bottom_row("x") == True
        
        # Number row
        assert utils.is_number_row("1") == True
        assert utils.is_number_row("2") == True
        
        # Non-row character
        assert utils.is_home_row("unknown") == False
        results.add_result("row_detection", True)
    except Exception as e:
        results.add_result("row_detection", False, str(e))


def test_consecutive_keys():
    """Test consecutive key detection"""
    try:
        utils = KeyboardUtils("qwerty")
        
        # Adjacent keys
        assert utils.is_consecutive("a", "s") == True
        
        # Far keys
        assert utils.is_consecutive("a", "p") == False
        
        # Same key
        assert utils.is_consecutive("a", "a") == True
        results.add_result("consecutive_keys", True)
    except Exception as e:
        results.add_result("consecutive_keys", False, str(e))


def test_keyboard_patterns():
    """Test keyboard pattern detection"""
    try:
        utils = KeyboardUtils("qwerty")
        
        # Empty text
        patterns = utils.get_keyboard_patterns("")
        assert len(patterns) == 0
        
        # Short text
        patterns = utils.get_keyboard_patterns("a")
        assert len(patterns) == 0
        
        # Text with consecutive keys
        patterns = utils.get_keyboard_patterns("asdf")
        assert len(patterns) >= 0  # May or may not have patterns
        
        # Convenience function
        patterns2 = get_keyboard_patterns("asdf", layout="qwerty")
        assert len(patterns2) == len(patterns)
        results.add_result("keyboard_patterns", True)
    except Exception as e:
        results.add_result("keyboard_patterns", False, str(e))


def test_efficiency_score():
    """Test efficiency score calculation"""
    try:
        utils = KeyboardUtils("qwerty")
        
        # Empty text
        score = utils.get_efficiency_score("")
        assert score == 100.0
        
        # Simple text
        score = utils.get_efficiency_score("asdf")
        assert 0 <= score <= 100
        
        # Convenience function
        score2 = efficiency_score("asdf", layout="qwerty")
        assert score2 == score
        results.add_result("efficiency_score", True)
    except Exception as e:
        results.add_result("efficiency_score", False, str(e))


def test_suggest_improvements():
    """Test improvement suggestions"""
    try:
        utils = KeyboardUtils("qwerty")
        
        # Empty text
        suggestions = utils.suggest_alternatives("")
        assert len(suggestions) == 0
        
        # Short text
        suggestions = utils.suggest_alternatives("a")
        assert len(suggestions) == 0
        
        # Text with potential issues
        suggestions = utils.suggest_alternatives("aaaa")
        assert len(suggestions) >= 1  # Same finger repeated
        
        # Convenience function
        suggestions2 = suggest_improvements("aaaa", layout="qwerty")
        assert len(suggestions2) == len(suggestions)
        results.add_result("suggest_improvements", True)
    except Exception as e:
        results.add_result("suggest_improvements", False, str(e))


def test_convert_to_layout():
    """Test layout conversion"""
    try:
        utils = KeyboardUtils("qwerty")
        
        # Convert to same layout
        converted = utils.convert_to_layout("asdf", "qwerty")
        assert converted == "asdf"
        
        # Convert to different layout
        converted = utils.convert_to_layout("asdf", "dvorak")
        # Check conversion happened
        assert len(converted) == 4
        
        # Invalid target layout
        try:
            utils.convert_to_layout("asdf", "invalid")
            results.add_result("convert_to_layout", False, "Should raise for invalid layout")
        except ValueError:
            pass
        results.add_result("convert_to_layout", True)
    except Exception as e:
        results.add_result("convert_to_layout", False, str(e))


def test_available_layouts():
    """Test available layouts"""
    try:
        layouts = available_layouts()
        assert "qwerty" in layouts
        assert "dvorak" in layouts
        assert "colemak" in layouts
        assert "azerty" in layouts
        assert "qwertz" in layouts
        results.add_result("available_layouts", True)
    except Exception as e:
        results.add_result("available_layouts", False, str(e))


def test_get_utils():
    """Test get_utils convenience function"""
    try:
        utils = get_utils("qwerty")
        assert utils.layout_name == "qwerty"
        
        # Different layout
        utils2 = get_utils("dvorak")
        assert utils2.layout_name == "dvorak"
        results.add_result("get_utils", True)
    except Exception as e:
        results.add_result("get_utils", False, str(e))


def test_convenience_functions():
    """Test all convenience functions"""
    try:
        # distance
        dist = distance("a", "s", layout="qwerty")
        assert dist > 0
        
        # get_key_position
        pos = get_key_position("a", layout="qwerty")
        assert pos is not None
        
        # get_coordinates
        coord = get_coordinates("a", layout="qwerty")
        assert coord is not None
        
        # get_finger
        finger = get_finger("a", layout="qwerty")
        assert finger is not None
        
        # get_hand
        hand = get_hand("a", layout="qwerty")
        assert hand is not None
        results.add_result("convenience_functions", True)
    except Exception as e:
        results.add_result("convenience_functions", False, str(e))


def test_different_layouts():
    """Test different keyboard layouts"""
    try:
        # QWERTY
        qwerty = KeyboardUtils("qwerty")
        qwerty_dist = qwerty.distance("t", "h")
        
        # Dvorak - t and h positions differ
        dvorak = KeyboardUtils("dvorak")
        dvorak_dist = dvorak.distance("t", "h")
        
        # Colemak
        colemak = KeyboardUtils("colemak")
        colemak_dist = colemak.distance("t", "h")
        
        # Different layouts may have different distances
        # Just verify they all return valid numbers
        assert qwerty_dist >= 0
        assert dvorak_dist >= 0
        assert colemak_dist >= 0
        results.add_result("different_layouts", True)
    except Exception as e:
        results.add_result("different_layouts", False, str(e))


def test_layout_definitions():
    """Test layout definitions"""
    try:
        # All layouts should have name and rows
        assert QWERTY_LAYOUT["name"] == "QWERTY"
        assert len(QWERTY_LAYOUT["rows"]) == 5
        
        assert DVORAK_LAYOUT["name"] == "Dvorak"
        assert len(DVORAK_LAYOUT["rows"]) == 5
        
        assert COLEMAK_LAYOUT["name"] == "Colemak"
        assert len(COLEMAK_LAYOUT["rows"]) == 5
        
        assert AZERTY_LAYOUT["name"] == "AZERTY"
        assert len(AZERTY_LAYOUT["rows"]) == 5
        
        assert QWERTZ_LAYOUT["name"] == "QWERTZ"
        assert len(QWERTZ_LAYOUT["rows"]) == 5
        results.add_result("layout_definitions", True)
    except Exception as e:
        results.add_result("layout_definitions", False, str(e))


def test_edge_cases():
    """Test edge cases"""
    try:
        utils = KeyboardUtils("qwerty")
        
        # Empty and None
        assert utils.analyze("").total_distance == 0
        assert utils.total_distance("") == 0
        
        # Very long text
        long_text = "a" * 1000
        analysis = utils.analyze(long_text)
        assert analysis.total_distance == 0  # Same key
        
        # Mixed known/unknown characters
        dist = utils.distance("a", "🚀")  # Emoji
        assert dist == float('inf')
        
        # Numbers and symbols
        assert utils.layout.get_key_position("1") is not None
        # Note: ! is shift+1, not a direct key
        results.add_result("edge_cases", True)
    except Exception as e:
        results.add_result("edge_cases", False, str(e))


# Run all tests
def run_tests():
    """Run all test functions"""
    test_enums()
    test_key_position_dataclass()
    test_typing_analysis_dataclass()
    test_keyboard_layout()
    test_keyboard_utils_init()
    test_distance()
    test_total_distance()
    test_analyze()
    test_same_hand_finger()
    test_row_detection()
    test_consecutive_keys()
    test_keyboard_patterns()
    test_efficiency_score()
    test_suggest_improvements()
    test_convert_to_layout()
    test_available_layouts()
    test_get_utils()
    test_convenience_functions()
    test_different_layouts()
    test_layout_definitions()
    test_edge_cases()
    
    return results.summary()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)