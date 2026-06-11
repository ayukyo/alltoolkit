#!/usr/bin/env python3
"""Conway's Game of Life Utils Tests"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import Rule, Pattern, GameOfLife, RULES


def test_rule_from_string():
    """Test Rule creation from string."""
    rule = Rule.from_string("B3/S23")
    assert rule.birth == {3}
    assert rule.survival == {2, 3}
    assert rule.name == "Custom"


def test_rule_from_string_conway():
    """Test Conway's Life rule."""
    rule = Rule.from_string("B3/S23", "Conway")
    assert rule.birth == {3}
    assert rule.survival == {2, 3}
    assert str(rule) == "B3/S23"


def test_rule_from_string_highlife():
    """Test HighLife rule (B36/S23)."""
    rule = Rule.from_string("B36/S23", "HighLife")
    assert rule.birth == {3, 6}
    assert rule.survival == {2, 3}


def test_rule_from_string_simplified():
    """Test simplified format (3/23)."""
    rule = Rule.from_string("3/23")
    assert rule.birth == {3}
    assert rule.survival == {2, 3}


def test_rule_str():
    """Test Rule string representation."""
    rule = Rule.from_string("B3/S23")
    assert str(rule) == "B3/S23"


def test_predefined_rules():
    """Test predefined rules exist."""
    assert "conway" in RULES
    assert "highlife" in RULES
    assert "seeds" in RULES
    assert "day_and_night" in RULES
    assert RULES["conway"].birth == {3}
    assert RULES["conway"].survival == {2, 3}


def test_pattern_block():
    """Test Block pattern."""
    block = Pattern.get("block")
    assert block == [(0, 0), (0, 1), (1, 0), (1, 1)]


def test_pattern_glider():
    """Test Glider pattern."""
    glider = Pattern.get("glider")
    assert (0, 1) in glider
    assert (2, 0) in glider
    assert (2, 1) in glider
    assert (2, 2) in glider


def test_pattern_beacon():
    """Test Beacon oscillator."""
    beacon = Pattern.get("beacon")
    assert len(beacon) == 8


def test_pattern_invalid():
    """Test invalid pattern name."""
    try:
        Pattern.get("invalid_pattern")
        assert False, "Should raise KeyError"
    except KeyError:
        pass


def test_gameoflife_init():
    """Test GameOfLife initialization."""
    gol = GameOfLife()
    assert gol.width == 100
    assert gol.height == 100
    assert gol.rule == RULES["conway"]


def test_gameoflife_init_custom_rule():
    """Test GameOfLife with custom rule."""
    rule = Rule.from_string("B36/S23")
    gol = GameOfLife(rule=rule, width=50, height=50)
    assert gol.width == 50
    assert gol.height == 50
    assert gol.rule == rule


def test_gameoflife_clear():
    """Test clear grid."""
    gol = GameOfLife(width=10, height=10)
    gol.set_cell(5, 5, True)
    assert gol.get_cell(5, 5)
    gol.clear()
    assert not gol.get_cell(5, 5)


def test_gameoflife_set_get_cell():
    """Test cell set and get."""
    gol = GameOfLife(width=20, height=20)
    gol.set_cell(10, 10, True)
    assert gol.get_cell(10, 10)
    gol.set_cell(10, 10, False)
    assert not gol.get_cell(10, 10)


def test_gameoflife_out_of_bounds():
    """Test out of bounds access."""
    gol = GameOfLife(width=10, height=10)
    assert not gol.get_cell(100, 100)
    gol.set_cell(100, 100, True)  # Should not raise


def test_toggle_cell():
    """Test cell toggling."""
    gol = GameOfLife(width=10, height=10)
    assert not gol.get_cell(5, 5)
    result = gol.toggle_cell(5, 5)
    assert result == True
    assert gol.get_cell(5, 5)
    result = gol.toggle_cell(5, 5)
    assert result == False
    assert not gol.get_cell(5, 5)


def test_blinker_evolution():
    """Test Blinker oscillator evolution."""
    gol = GameOfLife(width=10, height=10)
    # Place blinker vertically at (5,4), (5,5), (5,6)
    gol.set_cell(5, 4, True)
    gol.set_cell(5, 5, True)
    gol.set_cell(5, 6, True)
    
    # After one step, should be horizontal
    gol.step()
    assert gol.get_cell(4, 5)
    assert gol.get_cell(5, 5)
    assert gol.get_cell(6, 5)
    assert not gol.get_cell(5, 4)
    assert not gol.get_cell(5, 6)


def test_block_stable():
    """Test Block pattern is stable."""
    gol = GameOfLife(width=10, height=10)
    # Place block
    for dx, dy in Pattern.BLOCK:
        gol.set_cell(5 + dx, 5 + dy, True)
    
    initial_state = gol.get_cell(5, 5)
    gol.step()
    # Block should remain unchanged
    assert gol.get_cell(5, 5) == initial_state
    assert gol.get_cell(5, 6) == initial_state
    assert gol.get_cell(6, 5) == initial_state
    assert gol.get_cell(6, 6) == initial_state


def test_glider_movement():
    """Test Glider moves correctly."""
    gol = GameOfLife(width=10, height=10)
    # Place glider at origin
    for dx, dy in Pattern.GLIDER:
        gol.set_cell(dx, dy, True)
    
    # Record initial position
    initial_live = len(gol.cells)
    
    # Step a few times
    for _ in range(4):
        gol.step()
    
    # Glider should still be alive and moving
    assert len(gol.cells) == initial_live


def test_get_neighbors():
    """Test neighbor counting."""
    gol = GameOfLife(width=5, height=5)
    # Place center cell
    gol.set_cell(2, 2, True)
    # Place 8 neighbors
    gol.set_cell(1, 1, True)
    gol.set_cell(1, 2, True)
    gol.set_cell(1, 3, True)
    gol.set_cell(2, 1, True)
    gol.set_cell(2, 3, True)
    gol.set_cell(3, 1, True)
    gol.set_cell(3, 2, True)
    gol.set_cell(3, 3, True)
    
    # Center cell should have 8 neighbors
    assert gol.get_neighbors(2, 2) == 8


def test_live_cells_count():
    """Test live cell counting."""
    gol = GameOfLife(width=10, height=10)
    assert len(gol.cells) == 0
    
    gol.set_cell(1, 1, True)
    gol.set_cell(2, 2, True)
    gol.set_cell(3, 3, True)
    assert len(gol.cells) == 3


def test_load_pattern():
    """Test loading a pattern."""
    gol = GameOfLife(width=20, height=20)
    blinker = [(0, 0), (0, 1), (0, 2)]
    gol.load_pattern(blinker, (10, 10))
    
    # Check cells are set correctly
    assert gol.get_cell(10, 10)
    assert gol.get_cell(10, 11)
    assert gol.get_cell(10, 12)


def test_load_pattern_by_name():
    """Test loading pattern by name."""
    gol = GameOfLife(width=20, height=20)
    gol.load_pattern_by_name("blinker", (10, 10))
    assert gol.get_cell(10, 10)
    assert gol.get_cell(10, 11)
    assert gol.get_cell(10, 12)


def test_step_generations():
    """Test multiple generations."""
    gol = GameOfLife(width=10, height=10)
    blinker = [(0, 0), (0, 1), (0, 2)]
    gol.load_pattern(blinker, (5, 5))
    
    gen0 = gol.generation
    gol.step()
    assert gol.generation == gen0 + 1
    
    gol.step()
    assert gol.generation == gen0 + 2


def test_to_rle():
    """Test RLE export."""
    gol = GameOfLife(width=10, height=10)
    gol.set_cell(0, 0, True)
    gol.set_cell(0, 1, True)
    rle = gol.to_rle()
    assert "x =" in rle
    assert "y =" in rle
    assert "rule =" in rle


def test_get_bounds():
    """Test bounds calculation."""
    gol = GameOfLife(width=100, height=100)
    assert gol.get_bounds() == (0, 0, 0, 0)
    
    gol.set_cell(5, 3, True)
    gol.set_cell(10, 7, True)
    bounds = gol.get_bounds()
    assert bounds == (5, 10, 3, 7)


def test_get_grid():
    """Test grid representation."""
    gol = GameOfLife(width=5, height=5)
    gol.set_cell(1, 1, True)
    grid = gol.get_grid()
    assert len(grid) > 0
    assert len(grid[0]) > 0


if __name__ == "__main__":
    import subprocess
    result = subprocess.run(["python3", "-m", "pytest", __file__, "-v"], cwd=os.path.dirname(os.path.abspath(__file__)))
    sys.exit(result.returncode)
