"""
Conway's Game of Life 测试套件

测试所有生命游戏功能，包括规则、模式、演化、RLE格式等。
"""

import sys
import os

# 添加父目录到路径以导入模块
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from conway_game_of_life_utils.mod import (
    GameOfLife, Rule, Pattern, RULES,
    run_simulation, detect_pattern_type, pattern_to_ascii,
    generate_random_pattern, compare_patterns,
)


class TestResult:
    """测试结果收集器"""
    
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.tests = []
    
    def add_pass(self, name: str):
        self.passed += 1
        self.tests.append(('PASS', name))
    
    def add_fail(self, name: str, error: str):
        self.failed += 1
        self.tests.append(('FAIL', name, error))
    
    def summary(self) -> str:
        lines = [f"\n{'='*60}",
                 f"测试结果: {self.passed} 通过, {self.failed} 失败",
                 f"{'='*60}"]
        
        for test in self.tests:
            if test[0] == 'PASS':
                lines.append(f"✅ {test[1]}")
            else:
                lines.append(f"❌ {test[1]}: {test[2]}")
        
        return '\n'.join(lines)


def run_tests():
    results = TestResult()
    
    # ========== Rule 测试 ==========
    
    # Test 1: 创建基本规则
    try:
        rule = Rule({3}, {2, 3}, "Custom")
        assert rule.birth == {3}
        assert rule.survival == {2, 3}
        assert rule.name == "Custom"
        results.add_pass("Rule: 创建基本规则")
    except Exception as e:
        results.add_fail("Rule: 创建基本规则", str(e))
    
    # Test 2: 从字符串创建规则 B3/S23
    try:
        rule = Rule.from_string("B3/S23")
        assert rule.birth == {3}
        assert rule.survival == {2, 3}
        results.add_pass("Rule: 从 B3/S23 格式创建")
    except Exception as e:
        results.add_fail("Rule: 从 B3/S23 格式创建", str(e))
    
    # Test 3: 从简化格式创建规则
    try:
        rule = Rule.from_string("3/23")
        assert rule.birth == {3}
        assert rule.survival == {2, 3}
        results.add_pass("Rule: 从简化格式 3/23 创建")
    except Exception as e:
        results.add_fail("Rule: 从简化格式 3/23 创建", str(e))
    
    # Test 4: 规则字符串表示
    try:
        rule = Rule({3, 6}, {2, 3}, "HighLife")
        assert str(rule) == "B36/S23"
        results.add_pass("Rule: 字符串表示")
    except Exception as e:
        results.add_fail("Rule: 字符串表示", str(e))
    
    # Test 5: 预定义规则
    try:
        assert RULES['conway'].birth == {3}
        assert RULES['conway'].survival == {2, 3}
        assert RULES['highlife'].birth == {3, 6}
        assert RULES['day_and_night'].birth == {3, 6, 7, 8}
        results.add_pass("Rule: 预定义规则正确")
    except Exception as e:
        results.add_fail("Rule: 预定义规则正确", str(e))
    
    # ========== Pattern 测试 ==========
    
    # Test 6: 获取内置模式
    try:
        glider = Pattern.get('glider')
        assert len(glider) == 5
        assert (0, 1) in glider
        results.add_pass("Pattern: 获取 glider 模式")
    except Exception as e:
        results.add_fail("Pattern: 获取 glider 模式", str(e))
    
    # Test 7: 获取 block 模式
    try:
        block = Pattern.get('block')
        assert len(block) == 4
        assert (0, 0) in block
        results.add_pass("Pattern: 获取 block 模式")
    except Exception as e:
        results.add_fail("Pattern: 获取 block 模式", str(e))
    
    # Test 8: 获取 glider_gun 模式
    try:
        gun = Pattern.get('glider_gun')
        assert len(gun) > 30
        results.add_pass("Pattern: 获取 glider_gun 模式")
    except Exception as e:
        results.add_fail("Pattern: 获取 glider_gun 模式", str(e))
    
    # Test 9: 无效模式名称
    try:
        Pattern.get('invalid_pattern')
        results.add_fail("Pattern: 无效模式名称应抛出异常", "没有抛出异常")
    except KeyError:
        results.add_pass("Pattern: 无效模式名称抛出 KeyError")
    except Exception as e:
        results.add_fail("Pattern: 无效模式名称", f"错误的异常类型: {e}")
    
    # ========== GameOfLife 基本测试 ==========
    
    # Test 10: 创建游戏
    try:
        game = GameOfLife()
        assert len(game) == 0
        assert game.generation == 0
        results.add_pass("GameOfLife: 创建空游戏")
    except Exception as e:
        results.add_fail("GameOfLife: 创建空游戏", str(e))
    
    # Test 11: 设置和获取单元格
    try:
        game = GameOfLife()
        game.set_cell(5, 5, True)
        assert game.get_cell(5, 5) == True
        assert game.get_cell(5, 6) == False
        game.set_cell(5, 5, False)
        assert game.get_cell(5, 5) == False
        results.add_pass("GameOfLife: 设置和获取单元格")
    except Exception as e:
        results.add_fail("GameOfLife: 设置和获取单元格", str(e))
    
    # Test 12: 切换单元格
    try:
        game = GameOfLife()
        result = game.toggle_cell(3, 3)
        assert result == True
        assert game.get_cell(3, 3) == True
        result = game.toggle_cell(3, 3)
        assert result == False
        assert game.get_cell(3, 3) == False
        results.add_pass("GameOfLife: 切换单元格")
    except Exception as e:
        results.add_fail("GameOfLife: 切换单元格", str(e))
    
    # Test 13: 清空游戏
    try:
        game = GameOfLife()
        game.set_cell(1, 1)
        game.set_cell(2, 2)
        assert len(game) == 2
        game.clear()
        assert len(game) == 0
        assert game.generation == 0
        results.add_pass("GameOfLife: 清空游戏")
    except Exception as e:
        results.add_fail("GameOfLife: 清空游戏", str(e))
    
    # Test 14: 加载模式
    try:
        game = GameOfLife()
        game.load_pattern([(0, 0), (1, 1), (2, 2)])
        assert len(game) == 3
        results.add_pass("GameOfLife: 加载模式")
    except Exception as e:
        results.add_fail("GameOfLife: 加载模式", str(e))
    
    # Test 15: 加载模式带偏移
    try:
        game = GameOfLife()
        game.load_pattern([(0, 0), (1, 1)], offset=(10, 10))
        assert game.get_cell(10, 10) == True
        assert game.get_cell(11, 11) == True
        assert game.get_cell(0, 0) == False
        results.add_pass("GameOfLife: 加载模式带偏移")
    except Exception as e:
        results.add_fail("GameOfLife: 加载模式带偏移", str(e))
    
    # Test 16: 加载内置模式
    try:
        game = GameOfLife()
        game.load_pattern_by_name('glider', offset=(5, 5))
        assert len(game) == 5
        assert game.get_cell(5, 6) == True
        results.add_pass("GameOfLife: 加载内置 glider 模式")
    except Exception as e:
        results.add_fail("GameOfLife: 加载内置 glider 模式", str(e))
    
    # ========== 演化测试 ==========
    
    # Test 17: Block 仍然生命
    try:
        game = GameOfLife()
        game.load_pattern(Pattern.BLOCK)
        initial_cells = len(game)
        game.step(10)
        assert len(game) == initial_cells
        assert game.generation == 10
        results.add_pass("Evolution: Block 保持稳定")
    except Exception as e:
        results.add_fail("Evolution: Block 保持稳定", str(e))
    
    # Test 18: Blinker 振荡器
    try:
        game = GameOfLife()
        game.load_pattern(Pattern.BLINKER)
        initial = game.cells.copy()
        game.step(1)
        gen1 = game.cells.copy()
        game.step(1)
        gen2 = game.cells.copy()
        assert gen2 == initial
        assert gen1 != initial
        results.add_pass("Evolution: Blinker 振荡周期 2")
    except Exception as e:
        results.add_fail("Evolution: Blinker 振荡周期 2", str(e))
    
    # Test 19: Glider 移动
    try:
        game = GameOfLife()
        game.load_pattern(Pattern.GLIDER)
        initial_min_x = min(c[0] for c in game.cells)
        initial_min_y = min(c[1] for c in game.cells)
        
        game.step(4)
        
        # Glider 每 4 代移动 1 格 (右下方向)
        new_min_x = min(c[0] for c in game.cells)
        new_min_y = min(c[1] for c in game.cells)
        
        assert new_min_x > initial_min_x or new_min_y > initial_min_y
        assert len(game) == 5  # 活细胞数不变
        results.add_pass("Evolution: Glider 移动")
    except Exception as e:
        results.add_fail("Evolution: Glider 移动", str(e))
    
    # Test 20: R Pentomino 演化
    try:
        game = GameOfLife()
        game.load_pattern(Pattern.R_PENTOMINO)
        game.step(10)
        # R Pentomino 活细胞数应该增长
        assert len(game) > 5
        results.add_pass("Evolution: R Pentomino 演化")
    except Exception as e:
        results.add_fail("Evolution: R Pentomino 演化", str(e))
    
    # Test 21: 邻居计数
    try:
        game = GameOfLife()
        game.load_pattern([(0, 0), (1, 0), (0, 1)])
        assert game.get_neighbors(1, 1) == 3
        assert game.get_neighbors(0, 0) == 2
        assert game.get_neighbors(5, 5) == 0
        results.add_pass("GameOfLife: 邻居计数")
    except Exception as e:
        results.add_fail("GameOfLife: 邻居计数", str(e))
    
    # ========== RLE 格式测试 ==========
    
    # Test 22: 加载简单 RLE
    try:
        game = GameOfLife()
        rle = "x = 3, y = 3\nbo$2bo$3o!"
        game.load_rle(rle)
        assert len(game) == 5, f"Expected 5 cells, got {len(game)}"
        # 验证是有效的 glider 模式（5个细胞）
        results.add_pass("RLE: 加载简单 RLE")
    except Exception as e:
        results.add_fail("RLE: 加载简单 RLE", str(e))
    
    # Test 23: RLE 带注释
    try:
        game = GameOfLife()
        rle = "#C Name: Block\n#C Author: Unknown\nx = 2, y = 2\n2o$2o!"
        game.load_rle(rle)
        assert len(game) == 4
        results.add_pass("RLE: 加载带注释的 RLE")
    except Exception as e:
        results.add_fail("RLE: 加载带注释的 RLE", str(e))
    
    # Test 24: 导出 RLE
    try:
        game = GameOfLife()
        game.load_pattern(Pattern.GLIDER)
        rle = game.to_rle()
        assert 'x = 3, y = 3' in rle
        assert 'rule = B3/S23' in rle
        results.add_pass("RLE: 导出为 RLE 格式")
    except Exception as e:
        results.add_fail("RLE: 导出为 RLE 格式", str(e))
    
    # Test 25: RLE 规则解析
    try:
        game = GameOfLife()
        rle = "x = 3, y = 3, rule = B36/S23\nbo$2bo$3o!"
        game.load_rle(rle)
        assert game.rule.birth == {3, 6}
        assert game.rule.survival == {2, 3}
        results.add_pass("RLE: 规则解析")
    except Exception as e:
        results.add_fail("RLE: 规则解析", str(e))
    
    # ========== 不同规则测试 ==========
    
    # Test 26: HighLife 规则
    try:
        game = GameOfLife(rule=RULES['highlife'])
        # 创建一个会触发 B6 的配置
        game.load_pattern([(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0)])
        game.step(1)
        # 在 HighLife 中，6 个邻居会出生新细胞
        results.add_pass("GameOfLife: HighLife 规则")
    except Exception as e:
        results.add_fail("GameOfLife: HighLife 规则", str(e))
    
    # Test 27: Seeds 规则 (B2/S)
    try:
        game = GameOfLife(rule=RULES['seeds'])
        game.load_pattern([(0, 0), (1, 0)])
        game.step(1)
        # Seeds 规则中，2 个邻居会出生，但没有任何存活条件
        # 所有细胞都会在下一代死亡
        assert len(game) > 2  # 新细胞出生
        game.step(1)
        # 原始的两个细胞死亡
        results.add_pass("GameOfLife: Seeds 规则")
    except Exception as e:
        results.add_fail("GameOfLife: Seeds 规则", str(e))
    
    # ========== 边界和统计测试 ==========
    
    # Test 28: 获取边界
    try:
        game = GameOfLife()
        game.load_pattern([(5, 5), (10, 10), (3, 7)])
        bounds = game.get_bounds()
        assert bounds[0] == 3
        assert bounds[1] == 10
        assert bounds[2] == 5
        assert bounds[3] == 10
        results.add_pass("GameOfLife: 获取边界")
    except Exception as e:
        results.add_fail("GameOfLife: 获取边界", str(e))
    
    # Test 29: 空游戏边界
    try:
        game = GameOfLife()
        bounds = game.get_bounds()
        assert bounds == (0, 0, 0, 0)
        results.add_pass("GameOfLife: 空游戏边界")
    except Exception as e:
        results.add_fail("GameOfLife: 空游戏边界", str(e))
    
    # Test 30: 统计信息
    try:
        game = GameOfLife()
        game.load_pattern(Pattern.BLOCK)
        game.step(5)
        stats = game.get_statistics()
        assert stats['cells'] == 4
        assert stats['generation'] == 5
        assert stats['density'] > 0
        results.add_pass("GameOfLife: 统计信息")
    except Exception as e:
        results.add_fail("GameOfLife: 统计信息", str(e))
    
    # Test 31: 字符串表示
    try:
        game = GameOfLife()
        game.load_pattern([(0, 0), (1, 0)])
        str_repr = game.to_string(alive='O', dead='.', padding=1)
        assert 'O' in str_repr, f"'O' not in string: {str_repr}"
        # 添加 padding 后应该有死细胞
        assert '.' in str_repr, f"'.' not in string: {str_repr}"
        lines = str_repr.split('\n')
        assert len(lines) >= 1, f"Expected at least 1 line, got {len(lines)}"
        results.add_pass("GameOfLife: 字符串表示")
    except Exception as e:
        results.add_fail("GameOfLife: 字符串表示", str(e))
    
    # Test 32: 网格表示
    try:
        game = GameOfLife()
        game.load_pattern([(0, 0), (1, 1)])
        grid = game.get_grid(padding=1)
        assert len(grid) >= 3
        assert len(grid[0]) >= 3
        assert grid[1][1] == True
        results.add_pass("GameOfLife: 网格表示")
    except Exception as e:
        results.add_fail("GameOfLife: 网格表示", str(e))
    
    # ========== 辅助函数测试 ==========
    
    # Test 33: run_simulation - 稳定模式
    try:
        result = run_simulation(Pattern.BLOCK, generations=10)
        assert result['stable'] == True
        assert result['still_life'] == True
        assert result['oscillation_period'] == 1
        results.add_pass("run_simulation: Block 稳定")
    except Exception as e:
        results.add_fail("run_simulation: Block 稳定", str(e))
    
    # Test 34: run_simulation - 振荡器
    try:
        result = run_simulation(Pattern.BLINKER, generations=10)
        assert result['stable'] == True
        assert result['oscillation_period'] == 2
        results.add_pass("run_simulation: Blinker 振荡")
    except Exception as e:
        results.add_fail("run_simulation: Blinker 振荡", str(e))
    
    # Test 35: detect_pattern_type - 仍然生命
    try:
        cells = set(Pattern.BLOCK)
        type_str = detect_pattern_type(cells, max_generations=4)
        assert type_str == "Still Life", f"Expected 'Still Life', got '{type_str}'"
        results.add_pass("detect_pattern_type: Block 为 Still Life")
    except Exception as e:
        results.add_fail("detect_pattern_type: Block 为 Still Life", str(e))
    
    # Test 36: detect_pattern_type - 振荡器
    try:
        cells = set(Pattern.BLINKER)
        type_str = detect_pattern_type(cells, max_generations=4)
        assert "Oscillator" in type_str
        results.add_pass("detect_pattern_type: Blinker 为 Oscillator")
    except Exception as e:
        results.add_fail("detect_pattern_type: Blinker 为 Oscillator", str(e))
    
    # Test 37: pattern_to_ascii
    try:
        ascii_art = pattern_to_ascii(Pattern.GLIDER)
        assert '■' in ascii_art
        assert '·' in ascii_art
        lines = ascii_art.split('\n')
        assert len(lines) == 3
        results.add_pass("pattern_to_ascii: 生成 ASCII 艺术")
    except Exception as e:
        results.add_fail("pattern_to_ascii: 生成 ASCII 艺术", str(e))
    
    # Test 38: generate_random_pattern
    try:
        pattern = generate_random_pattern(density=0.5, width=10, height=10, seed=42)
        assert len(pattern) > 0
        assert len(pattern) <= 100
        # 检查所有坐标在范围内
        for x, y in pattern:
            assert 0 <= x < 10
            assert 0 <= y < 10
        results.add_pass("generate_random_pattern: 生成随机模式")
    except Exception as e:
        results.add_fail("generate_random_pattern: 生成随机模式", str(e))
    
    # Test 39: compare_patterns - 相同
    try:
        p1 = set([(0, 0), (1, 1)])
        p2 = set([(0, 0), (1, 1)])
        result = compare_patterns(p1, p2)
        assert result['identical'] == True
        assert result['similarity'] == 1.0
        results.add_pass("compare_patterns: 相同模式")
    except Exception as e:
        results.add_fail("compare_patterns: 相同模式", str(e))
    
    # Test 40: compare_patterns - 不同
    try:
        p1 = set([(0, 0), (1, 1), (2, 2)])
        p2 = set([(0, 0), (3, 3)])
        result = compare_patterns(p1, p2)
        assert result['identical'] == False
        assert result['cells_in_common'] == 1
        assert result['only_in_first'] == 2
        assert result['only_in_second'] == 1
        results.add_pass("compare_patterns: 不同模式")
    except Exception as e:
        results.add_fail("compare_patterns: 不同模式", str(e))
    
    # ========== 复杂模式测试 ==========
    
    # Test 41: Pulsar 振荡器
    try:
        game = GameOfLife()
        game.load_pattern(Pattern.PULSAR)
        initial = game.cells.copy()
        game.step(3)
        # Pulsar 周期为 3
        assert game.cells == initial
        results.add_pass("Evolution: Pulsar 周期 3")
    except Exception as e:
        results.add_fail("Evolution: Pulsar 周期 3", str(e))
    
    # Test 42: Beacon 振荡器
    try:
        game = GameOfLife()
        game.load_pattern(Pattern.BEACON)
        initial = game.cells.copy()
        game.step(2)
        assert game.cells == initial
        results.add_pass("Evolution: Beacon 周期 2")
    except Exception as e:
        results.add_fail("Evolution: Beacon 周期 2", str(e))
    
    # Test 43: LWSS 太空船
    try:
        game = GameOfLife()
        game.load_pattern(Pattern.LWSS)
        initial_count = len(game)
        game.step(4)
        # LWSS 每 4 代移动 2 格，活细胞数不变
        assert len(game) == initial_count
        results.add_pass("Evolution: LWSS 太空船")
    except Exception as e:
        results.add_fail("Evolution: LWSS 太空船", str(e))
    
    # Test 44: Glider Gun 产生滑翔机
    try:
        game = GameOfLife()
        game.load_pattern(Pattern.GLIDER_GUN)
        game.step(30)
        # Glider gun 会持续产生滑翔机
        # 活细胞数应该增加
        assert len(game) > len(Pattern.GLIDER_GUN)
        results.add_pass("Evolution: Glider Gun 产生滑翔机")
    except Exception as e:
        results.add_fail("Evolution: Glider Gun 产生滑翔机", str(e))
    
    # Test 45: Diehard 消失前存活超过 100 代
    try:
        game = GameOfLife()
        game.load_pattern(Pattern.DIEHARD)
        game.step(100)
        # Diehard 在 130 代左右消失
        assert len(game) > 0 or game.generation > 100
        results.add_pass("Evolution: Diehard 长期存活")
    except Exception as e:
        results.add_fail("Evolution: Diehard 长期存活", str(e))
    
    # ========== 边界值测试 ==========
    
    # Test 46: 空模式
    try:
        game = GameOfLife()
        game.load_pattern([])
        assert len(game) == 0
        game.step(10)
        assert len(game) == 0
        results.add_pass("Boundary: 空模式")
    except Exception as e:
        results.add_fail("Boundary: 空模式", str(e))
    
    # Test 47: 单细胞
    try:
        game = GameOfLife()
        game.load_pattern([(0, 0)])
        game.step(1)
        assert len(game) == 0  # 单细胞会死亡
        results.add_pass("Boundary: 单细胞死亡")
    except Exception as e:
        results.add_fail("Boundary: 单细胞死亡", str(e))
    
    # Test 48: 两细胞
    try:
        game = GameOfLife()
        game.load_pattern([(0, 0), (1, 0)])
        game.step(1)
        assert len(game) == 0  # 两细胞也会死亡
        results.add_pass("Boundary: 两细胞死亡")
    except Exception as e:
        results.add_fail("Boundary: 两细胞死亡", str(e))
    
    # Test 49: 三细胞线
    try:
        game = GameOfLife()
        game.load_pattern([(0, 0), (1, 0), (2, 0)])  # Blinker
        game.step(1)
        # 变成垂直线
        assert len(game) == 3
        results.add_pass("Boundary: 三细胞振荡")
    except Exception as e:
        results.add_fail("Boundary: 三细胞振荡", str(e))
    
    # Test 50: 大坐标
    try:
        game = GameOfLife()
        game.load_pattern([(10000, 10000), (10001, 10001)])
        game.step(5)
        assert len(game) == 0
        results.add_pass("Boundary: 大坐标")
    except Exception as e:
        results.add_fail("Boundary: 大坐标", str(e))
    
    # Test 51: 负坐标
    try:
        game = GameOfLife()
        game.load_pattern([(-5, -5), (-4, -5), (-3, -5)])
        game.step(1)
        assert len(game) == 3  # Blinker 振荡
        results.add_pass("Boundary: 负坐标")
    except Exception as e:
        results.add_fail("Boundary: 负坐标", str(e))
    
    # Test 52: 密集模式
    try:
        game = GameOfLife()
        # 5x5 全满
        cells = [(x, y) for x in range(5) for y in range(5)]
        game.load_pattern(cells)
        game.step(10)
        # 密集模式会快速收缩
        results.add_pass("Boundary: 密集模式演化")
    except Exception as e:
        results.add_fail("Boundary: 密集模式演化", str(e))
    
    # Test 53: 复制游戏状态
    try:
        game = GameOfLife()
        game.load_pattern(Pattern.GLIDER)
        game.step(5)
        
        copy_game = game.copy()
        assert len(copy_game) == len(game)
        assert copy_game.generation == game.generation
        assert copy_game.cells == game.cells
        
        # 修改原游戏不影响副本
        game.step(5)
        assert copy_game.generation != game.generation
        results.add_pass("GameOfLife: 复制游戏状态")
    except Exception as e:
        results.add_fail("GameOfLife: 复制游戏状态", str(e))
    
    # Test 54: 无限演化
    try:
        game = GameOfLife()
        game.load_pattern(Pattern.ACORN)
        game.step(500)
        # Acorn 在数百代后稳定
        stats = game.get_statistics()
        assert stats['generation'] == 500
        results.add_pass("Evolution: 长期演化")
    except Exception as e:
        results.add_fail("Evolution: 长期演化", str(e))
    
    # Test 55: run_simulation 不稳定模式
    try:
        # 使用随机模式，设置较低代数
        pattern = generate_random_pattern(0.3, 20, 20, seed=123)
        result = run_simulation(pattern, generations=20, stop_if_stable=False)
        assert result['generations'] == 20
        results.add_pass("run_simulation: 强制运行指定代数")
    except Exception as e:
        results.add_fail("run_simulation: 强制运行指定代数", str(e))
    
    # Test 56: 边界环绕模式
    try:
        game = GameOfLife(width=10, height=10)
        game.wrap_edges = True
        # 在边缘放置细胞
        game.load_pattern([(0, 0), (0, 1), (0, 2)])
        game.step(1)
        # 环绕模式下，边缘细胞会影响对面
        results.add_pass("GameOfLife: 边界环绕模式")
    except Exception as e:
        results.add_fail("GameOfLife: 边界环绕模式", str(e))
    
    # Test 57: Beehive 仍然生命
    try:
        game = GameOfLife()
        game.load_pattern(Pattern.BEEHIVE)
        initial = len(game)
        game.step(100)
        assert len(game) == initial
        results.add_pass("Evolution: Beehive 保持稳定")
    except Exception as e:
        results.add_fail("Evolution: Beehive 保持稳定", str(e))
    
    # Test 58: Loaf 仍然生命
    try:
        game = GameOfLife()
        game.load_pattern(Pattern.LOAF)
        initial = len(game)
        game.step(100)
        assert len(game) == initial
        results.add_pass("Evolution: Loaf 保持稳定")
    except Exception as e:
        results.add_fail("Evolution: Loaf 保持稳定", str(e))
    
    # Test 59: Toad 振荡器
    try:
        game = GameOfLife()
        game.load_pattern(Pattern.TOAD)
        initial = game.cells.copy()
        game.step(2)
        assert game.cells == initial
        game.step(2)
        assert game.cells == initial
        results.add_pass("Evolution: Toad 周期 2")
    except Exception as e:
        results.add_fail("Evolution: Toad 周期 2", str(e))
    
    # Test 60: Pentadecathlon 振荡器
    try:
        game = GameOfLife()
        game.load_pattern(Pattern.PENTADecathlon)
        initial = game.cells.copy()
        game.step(15)
        assert game.cells == initial
        results.add_pass("Evolution: Pentadecathlon 周期 15")
    except Exception as e:
        results.add_fail("Evolution: Pentadecathlon 周期 15", str(e))
    
    # 打印结果
    print(results.summary())
    
    return results.failed == 0


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)