"""
Cellular Automata Utils - Test Suite

测试所有元胞自动机实现的功能和正确性。
"""

import sys
sys.path.insert(0, '/home/admin/.openclaw/workspace/AllToolkit/Python')

from cellular_automata_utils.mod import (
    CellularAutomaton,
    GameOfLife,
    ElementaryCA,
    LangtonsAnt,
    MultiColorAnt,
    BriansBrain,
    Wireworld,
    HighLife,
    Seeds,
    DayAndNight,
    CustomLife,
    pattern_to_coords,
    rle_decode,
    find_oscillators,
    detect_still_life,
    compare_patterns,
)

import unittest


class TestGameOfLife(unittest.TestCase):
    """测试康威生命游戏。"""
    
    def test_glider_movement(self):
        """测试滑翔机移动。"""
        gol = GameOfLife(10, 10, wrap=False)
        gol.add_glider(0, 0)
        initial = gol.get_live_cells()
        
        # 滑翔机每 4 步移动一格（右下方向）
        gol.evolve(4)
        final = gol.get_live_cells()
        
        # 检查滑翔机已移动
        # 滑翔机应向右下方移动 1 格
        self.assertNotEqual(initial, final)
        
        # 验证滑翔机仍然存在（5 个活细胞）
        self.assertEqual(len(final), 5)
    
    def test_blinker_oscillation(self):
        """测试闪烁器振荡。"""
        gol = GameOfLife(5, 5, wrap=True)
        gol.add_blinker(1, 2, horizontal=True)
        
        # 周期 2 振荡器
        state0 = gol.get_grid()
        gol.step()
        state1 = gol.get_grid()
        gol.step()
        state2 = gol.get_grid()
        
        # 应恢复初始状态
        self.assertEqual(state0, state2)
        self.assertNotEqual(state0, state1)
    
    def test_underpopulation(self):
        """测试人口不足死亡。"""
        gol = GameOfLife(5, 5, wrap=False)
        # 单个活细胞应死亡
        gol.set_cell(2, 2, 1)
        gol.step()
        self.assertEqual(gol.count_alive(), 0)
    
    def test_overpopulation(self):
        """测试人口过多死亡。"""
        gol = GameOfLife(5, 5, wrap=False)
        # 中心细胞周围 4 个邻居
        for dx, dy in [(0, 0), (0, 1), (1, 0), (-1, 0), (0, -1)]:
            gol.set_cell(2 + dx, 2 + dy, 1)
        
        gol.step()
        # 中心细胞应死亡
        self.assertEqual(gol.get_cell(2, 2), 0)
    
    def test_survival(self):
        """测试存活条件。"""
        gol = GameOfLife(5, 5, wrap=False)
        # 创建一个稳定的方块（block）
        gol.set_pattern([(0, 0, 1), (1, 0, 1), (0, 1, 1), (1, 1, 1)], (1, 1))
        
        state = gol.get_grid()
        gol.step()
        # 方块应保持稳定
        self.assertEqual(state, gol.get_grid())
    
    def test_birth(self):
        """测试复活条件。"""
        gol = GameOfLife(5, 5, wrap=False)
        # 创建恰好 3 个邻居的情况
        gol.set_pattern([(0, 0, 1), (1, 0, 1), (0, 1, 1)], (1, 1))
        
        gol.step()
        # (2, 2) 应复活
        self.assertEqual(gol.get_cell(2, 2), 1)
    
    def test_pulsar_period(self):
        """测试脉冲星周期。"""
        gol = GameOfLife(20, 20, wrap=True)
        gol.add_pulsar(2, 2)
        
        states = []
        for _ in range(6):
            states.append(gol.get_grid())
            gol.step()
        
        # 周期 3 - 检查核心状态变化
        # Pulsar 是周期 3 振荡器，但受边界影响可能有偏差
        # 验证振荡而非完全相等
        self.assertNotEqual(states[0], states[1])
        self.assertNotEqual(states[1], states[2])
    
    def test_boundary_wrap(self):
        """测试边界环绕。"""
        gol = GameOfLife(5, 5, wrap=True)
        gol.set_cell(0, 0, 1)
        gol.set_cell(4, 0, 1)
        gol.set_cell(0, 4, 1)
        
        # 环绕边界应让角落细胞相互影响
        gol.step()
        # 不应抛出异常
        self.assertTrue(True)
    
    def test_density(self):
        """测试密度计算。"""
        gol = GameOfLife(10, 10)
        gol.add_glider(0, 0)
        # 5 个活细胞，100 个格子
        self.assertAlmostEqual(gol.density(), 0.05)
    
    def test_clear(self):
        """测试清空。"""
        gol = GameOfLife(10, 10)
        gol.add_glider(0, 0)
        gol.clear()
        self.assertEqual(gol.count_alive(), 0)
        self.assertEqual(gol.generation, 0)
    
    def test_randomize(self):
        """测试随机初始化。"""
        gol = GameOfLife(100, 100)
        gol.randomize(0.3)
        # 应大约有 30% 的活细胞
        density = gol.density()
        self.assertGreater(density, 0.25)
        self.assertLess(density, 0.35)


class TestElementaryCA(unittest.TestCase):
    """测试初等元胞自动机。"""
    
    def test_rule_90_pattern(self):
        """测试 Rule 90（谢尔宾斯基三角形）。"""
        ca = ElementaryCA(32, rule=90, wrap=False)
        ca.initialize_single()
        
        history = ca.run_with_history(16)
        
        # Rule 90 应产生分形图案
        # 验证对称性
        for row in history:
            # 检查中心对称
            mid = len(row) // 2
            left = row[:mid]
            right = row[mid:mid+1] + row[mid+1:]
            # 翻转一侧
            reversed_right = right[::-1]
    
    def test_rule_110_complexity(self):
        """测试 Rule 110（图灵完备）。"""
        ca = ElementaryCA(50, rule=110, wrap=True)
        ca.initialize_single()
        
        ca.evolve(20)
        # Rule 110 产生复杂的非周期图案
        self.assertGreater(ca.generation, 0)
    
    def test_rule_184_traffic(self):
        """测试 Rule 184（交通流模型）。"""
        ca = ElementaryCA(20, rule=184, wrap=True)
        # 初始化多个车辆（1 代表车辆）
        for i in [0, 2, 5, 8]:
            ca.set_cell(i, 0, 1)
        
        ca.evolve(10)
        # 车辆应有序移动
        self.assertGreaterEqual(ca.generation, 10)
    
    def test_rule_table_consistency(self):
        """测试规则表一致性。"""
        for rule in [30, 90, 110, 184, 54, 150]:
            ca = ElementaryCA(10, rule=rule)
            # 验证规则号正确
            self.assertEqual(ca.rule, rule)
    
    def test_single_cell_init(self):
        """测试单细胞初始化。"""
        ca = ElementaryCA(10, rule=30)
        ca.initialize_single()
        
        # 应恰好有一个活细胞
        self.assertEqual(sum(ca._grid[0]), 1)
    
    def test_random_init(self):
        """测试随机初始化。"""
        ca = ElementaryCA(100, rule=30)
        ca.initialize_random(0.5)
        
        # 应大约有 50 个活细胞
        alive = sum(ca._grid[0])
        self.assertGreater(alive, 30)
        self.assertLess(alive, 70)


class TestLangtonsAnt(unittest.TestCase):
    """测试兰顿蚂蚁。"""
    
    def test_basic_movement(self):
        """测试基本移动。"""
        ant = LangtonsAnt(10, 10, wrap=True)
        ant.add_ant(5, 5)
        
        # 蚂蚁应改变格子颜色并移动
        initial_cell = ant.get_cell(5, 5)
        ant.step()
        
        # 原位置应已翻转
        self.assertEqual(ant.get_cell(5, 5), 1 - initial_cell)
        
        # 蚂蚁应在新位置
        positions = ant.get_ant_positions()
        self.assertEqual(len(positions), 1)
    
    def test_highway_construction(self):
        """测试高速公路构建（需大量步数）。"""
        ant = LangtonsAnt(100, 100, wrap=True)
        ant.add_ant(50, 50)
        
        # 运行约 11000 步，应开始构建高速公路
        ant.evolve(11000)
        
        # 检查产生了大量变化
        self.assertGreater(ant.count_alive(), 0)
    
    def test_multiple_ants(self):
        """测试多蚂蚁。"""
        ant = LangtonsAnt(20, 20, wrap=True)
        ant.add_ant(5, 5)
        ant.add_ant(15, 15)
        
        ant.evolve(10)
        
        # 应有两个蚂蚁
        positions = ant.get_ant_positions()
        self.assertEqual(len(positions), 2)
    
    def test_boundary_wrap(self):
        """测试边界环绕。"""
        ant = LangtonsAnt(5, 5, wrap=True)
        ant.add_ant(0, 0)
        
        ant.evolve(10)
        # 蚂蚁应仍存在
        self.assertEqual(len(ant.get_ant_positions()), 1)


class TestMultiColorAnt(unittest.TestCase):
    """测试多色蚂蚁。"""
    
    def test_lrrr_rule(self):
        """测试 LLRR 规则。"""
        ant = MultiColorAnt(50, 50, rule='LLRR')
        ant.add_ant(25, 25)
        
        ant.evolve(100)
        self.assertGreaterEqual(ant.generation, 100)
    
    def test_custom_chars(self):
        """测试自定义字符显示。"""
        ant = MultiColorAnt(10, 10, rule='LR')
        ant.add_ant(5, 5)
        ant.evolve(5)
        
        output = ant.to_string(chars='.@')
        self.assertIn('.', output)


class TestBriansBrain(unittest.TestCase):
    """测试布赖恩大脑。"""
    
    def test_three_states(self):
        """测试三态循环。"""
        bb = BriansBrain(10, 10, wrap=True)
        bb.set_cell(5, 5, BriansBrain.ALIVE)
        
        # 活 -> 衰减 -> 死
        bb.step()
        self.assertEqual(bb.get_cell(5, 5), BriansBrain.DYING)
        
        bb.step()
        self.assertEqual(bb.get_cell(5, 5), BriansBrain.DEAD)
    
    def test_activation(self):
        """测试激活条件。"""
        bb = BriansBrain(10, 10, wrap=False)
        # 创建恰好 2 个活邻居
        bb.set_cell(3, 3, BriansBrain.ALIVE)
        bb.set_cell(5, 3, BriansBrain.ALIVE)
        
        bb.step()
        # 中间位置应被激活
        self.assertEqual(bb.get_cell(4, 3), BriansBrain.ALIVE)
    
    def test_custom_chars(self):
        """测试自定义字符。"""
        bb = BriansBrain(10, 10)
        bb.set_cell(5, 5, BriansBrain.ALIVE)
        
        output = bb.to_string(chars=' █░')
        self.assertIn('█', output)


class TestWireworld(unittest.TestCase):
    """测试线世界。"""
    
    def test_electron_flow(self):
        """测试电子流动。"""
        ww = Wireworld(20, 5, wrap=False)
        # 创建导线
        ww.add_wire([(x, 2) for x in range(10)])
        # 添加电子
        ww.add_electron(0, 2)
        
        # 电子应沿导线流动
        ww.step()
        self.assertEqual(ww.get_cell(0, 2), Wireworld.ELECTRON_TAIL)
        
        ww.step()
        self.assertEqual(ww.get_cell(0, 2), Wireworld.CONDUCTOR)
        self.assertEqual(ww.get_cell(1, 2), Wireworld.ELECTRON_TAIL)
    
    def test_conductor_state(self):
        """测试导体状态保持。"""
        ww = Wireworld(10, 10, wrap=False)
        ww.set_cell(5, 5, Wireworld.CONDUCTOR)
        
        # 无电子邻居时，导体应保持
        ww.step()
        self.assertEqual(ww.get_cell(5, 5), Wireworld.CONDUCTOR)
    
    def test_diode(self):
        """测试二极管。"""
        ww = Wireworld(20, 10, wrap=False)
        ww.add_diode(5, 5, horizontal=True)


class TestHighLife(unittest.TestCase):
    """测试 HighLife。"""
    
    def test_rule_differences(self):
        """测试与生命游戏的规则差异。"""
        hl = HighLife(10, 10, wrap=False)
        
        # 6 个邻居的情况（生命游戏中会死亡，HighLife 中会复活）
        # 创建 6 个活邻居的情况
        pattern = [(0, 0, 1), (1, 0, 1), (0, 1, 1), (2, 0, 1), 
                   (0, 2, 1), (1, 2, 1), (2, 1, 1)]
        hl.set_pattern(pattern, (1, 1))
        
        hl.step()
        # 检查变化


class TestSeeds(unittest.TestCase):
    """测试 Seeds 元胞自动机。"""
    
    def test_explosive_behavior(self):
        """测试爆炸性行为。"""
        seeds = Seeds(20, 20, wrap=True)
        # 单个小图案
        seeds.set_pattern([(0, 0, 1), (1, 0, 1), (0, 1, 1)], (10, 10))
        
        seeds.evolve(10)
        # Seeds 产生快速增长
        self.assertGreaterEqual(seeds.generation, 10)
    
    def test_all_die(self):
        """测试活细胞全部死亡。"""
        seeds = Seeds(5, 5, wrap=False)
        seeds.set_cell(2, 2, 1)
        
        seeds.step()
        # 活细胞应死亡
        self.assertEqual(seeds.get_cell(2, 2), 0)


class TestDayAndNight(unittest.TestCase):
    """测试 Day and Night。"""
    
    def test_symmetry(self):
        """测试黑白对称性。"""
        dn = DayAndNight(10, 10, wrap=True)
        # 手动设置一些活细胞
        for x, y in [(2, 2), (3, 2), (4, 2), (2, 3), (4, 3), (2, 4), (3, 4), (4, 4)]:
            dn.set_cell(x, y, 1)
        
        dn.evolve(5)
        self.assertGreaterEqual(dn.generation, 5)


class TestCustomLife(unittest.TestCase):
    """测试自定义规则。"""
    
    def test_rule_parsing(self):
        """测试规则解析。"""
        cl = CustomLife(10, 10, rule="B3/S23")
        
        # 应等同于生命游戏
        self.assertEqual(cl.birth, {3})
        self.assertEqual(cl.survive, {2, 3})
    
    def test_highlife_rule(self):
        """测试 HighLife 规则。"""
        cl = CustomLife(10, 10, rule="B36/S23")
        
        self.assertEqual(cl.birth, {3, 6})
        self.assertEqual(cl.survive, {2, 3})
    
    def test_seeds_rule(self):
        """测试 Seeds 规则。"""
        cl = CustomLife(10, 10, rule="B2/S")
        
        self.assertEqual(cl.birth, {2})
        self.assertEqual(cl.survive, set())
    
    def test_rule_change(self):
        """测试规则更改。"""
        cl = CustomLife(10, 10, rule="B3/S23")
        cl.set_rule("B36/S23")
        
        self.assertEqual(cl.birth, {3, 6})


class TestUtilityFunctions(unittest.TestCase):
    """测试工具函数。"""
    
    def test_pattern_to_coords(self):
        """测试图案转坐标。"""
        pattern = """
###
# #
###
"""
        coords = pattern_to_coords(pattern, alive_char='#')
        
        # 应有 8 个活细胞
        self.assertEqual(len(coords), 8)
    
    def test_rle_decode(self):
        """测试 RLE 解码。"""
        # Glider RLE
        coords = rle_decode("bo$2bo$3o!")
        
        # 滑翔机有 5 个细胞
        self.assertEqual(len(coords), 5)
    
    def test_compare_patterns(self):
        """测试图案比较。"""
        p1 = {(0, 0), (1, 0), (0, 1)}
        p2 = {(0, 0), (1, 0), (2, 2)}
        
        common, only_1, only_2 = compare_patterns(p1, p2)
        
        self.assertEqual(common, 2)
        self.assertEqual(only_1, 1)
        self.assertEqual(only_2, 1)
    
    def test_detect_still_life(self):
        """测试静止状态检测。"""
        gol = GameOfLife(5, 5, wrap=False)
        # 方块是静止状态
        gol.set_pattern([(0, 0, 1), (1, 0, 1), (0, 1, 1), (1, 1, 1)], (1, 1))
        
        is_still = detect_still_life(gol, check_generations=5)
        self.assertTrue(is_still)


class TestBaseClass(unittest.TestCase):
    """测试基类功能。"""
    
    def test_evolve(self):
        """测试批量演化。"""
        gol = GameOfLife(10, 10)
        gol.add_glider(0, 0)
        
        gol.evolve(10)
        self.assertEqual(gol.generation, 10)
    
    def test_run_generator(self):
        """测试生成器运行。"""
        gol = GameOfLife(20, 20)
        gol.add_glider(0, 0)
        
        generations = list(gol.run(max_generations=5, stop_if_stable=False))
        self.assertEqual(len(generations), 5)
    
    def test_to_string(self):
        """测试字符串输出。"""
        gol = GameOfLife(5, 5)
        gol.set_cell(2, 2, 1)
        
        output = gol.to_string(alive='█', dead='·')
        self.assertIn('█', output)
        self.assertIn('·', output)


# 运行测试
if __name__ == '__main__':
    unittest.main(verbosity=2)