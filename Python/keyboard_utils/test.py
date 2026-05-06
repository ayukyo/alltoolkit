"""
Keyboard Utils Tests - 键盘布局工具测试

测试覆盖：
- 布局初始化
- 按键位置查询
- 距离计算
- 打字分析
- 键盘模式检测
- 效率评分
- 布局转换
"""

import unittest
import sys
import os

# 添加模块路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    KeyboardUtils, KeyboardLayout, Finger, Hand, KeyPosition, TypingAnalysis,
    QWERTY_LAYOUT, DVORAK_LAYOUT, COLEMAK_LAYOUT, AZERTY_LAYOUT, QWERTZ_LAYOUT,
    distance, total_distance, analyze, get_key_position, get_coordinates,
    get_finger, get_hand, efficiency_score, get_keyboard_patterns,
    suggest_improvements, available_layouts, get_utils
)


class TestKeyboardLayout(unittest.TestCase):
    """测试键盘布局类"""
    
    def test_qwerty_layout_initialization(self):
        """测试 QWERTY 布局初始化"""
        layout = KeyboardLayout(QWERTY_LAYOUT)
        self.assertEqual(layout.name, "QWERTY")
        self.assertEqual(layout.variant, "US")
    
    def test_dvorak_layout_initialization(self):
        """测试 Dvorak 布局初始化"""
        layout = KeyboardLayout(DVORAK_LAYOUT)
        self.assertEqual(layout.name, "Dvorak")
        self.assertEqual(layout.variant, "US")
    
    def test_colemak_layout_initialization(self):
        """测试 Colemak 布局初始化"""
        layout = KeyboardLayout(COLEMAK_LAYOUT)
        self.assertEqual(layout.name, "Colemak")
    
    def test_azerty_layout_initialization(self):
        """测试 AZERTY 布局初始化"""
        layout = KeyboardLayout(AZERTY_LAYOUT)
        self.assertEqual(layout.name, "AZERTY")
        self.assertEqual(layout.variant, "French")
    
    def test_qwertz_layout_initialization(self):
        """测试 QWERTZ 布局初始化"""
        layout = KeyboardLayout(QWERTZ_LAYOUT)
        self.assertEqual(layout.name, "QWERTZ")
        self.assertEqual(layout.variant, "German")
    
    def test_get_key_position_lowercase(self):
        """测试获取小写字母位置"""
        layout = KeyboardLayout(QWERTY_LAYOUT)
        pos = layout.get_key_position('a')
        self.assertIsNotNone(pos)
        self.assertEqual(pos.row, 2)  # home row
        self.assertEqual(pos.finger, Finger.LEFT_PINKY)
        self.assertEqual(pos.hand, Hand.LEFT)
    
    def test_get_key_position_uppercase(self):
        """测试获取大写字母位置"""
        layout = KeyboardLayout(QWERTY_LAYOUT)
        pos = layout.get_key_position('A')
        self.assertIsNotNone(pos)
        self.assertEqual(pos.row, 2)
        self.assertEqual(pos.finger, Finger.LEFT_PINKY)
    
    def test_get_key_position_number(self):
        """测试获取数字位置"""
        layout = KeyboardLayout(QWERTY_LAYOUT)
        pos = layout.get_key_position('1')
        self.assertIsNotNone(pos)
        self.assertEqual(pos.row, 0)  # number row
        self.assertEqual(pos.finger, Finger.LEFT_PINKY)
    
    def test_get_key_position_special(self):
        """测试获取特殊字符位置"""
        layout = KeyboardLayout(QWERTY_LAYOUT)
        pos = layout.get_key_position('!')
        self.assertIsNotNone(pos)
        # ! 在 1 的 shift 位置
        self.assertEqual(pos.finger, Finger.LEFT_PINKY)
    
    def test_get_key_position_not_found(self):
        """测试未找到字符"""
        layout = KeyboardLayout(QWERTY_LAYOUT)
        pos = layout.get_key_position('中')
        self.assertIsNone(pos)
    
    def test_get_coordinates(self):
        """测试获取坐标"""
        layout = KeyboardLayout(QWERTY_LAYOUT)
        coords = layout.get_coordinates('a')
        self.assertIsNotNone(coords)
        x, y = coords
        self.assertEqual(y, 2)  # home row
        self.assertIsInstance(x, float)
        self.assertIsInstance(y, float)
    
    def test_get_finger(self):
        """测试获取手指"""
        layout = KeyboardLayout(QWERTY_LAYOUT)
        
        # 左手
        self.assertEqual(layout.get_finger('a'), Finger.LEFT_PINKY)
        self.assertEqual(layout.get_finger('s'), Finger.LEFT_RING)
        self.assertEqual(layout.get_finger('d'), Finger.LEFT_MIDDLE)
        self.assertEqual(layout.get_finger('f'), Finger.LEFT_INDEX)
        
        # 右手
        self.assertEqual(layout.get_finger('j'), Finger.RIGHT_INDEX)
        self.assertEqual(layout.get_finger('k'), Finger.RIGHT_MIDDLE)
        self.assertEqual(layout.get_finger('l'), Finger.RIGHT_RING)
        self.assertEqual(layout.get_finger(';'), Finger.RIGHT_PINKY)
    
    def test_get_hand(self):
        """测试获取手"""
        layout = KeyboardLayout(QWERTY_LAYOUT)
        
        self.assertEqual(layout.get_hand('a'), Hand.LEFT)
        self.assertEqual(layout.get_hand('s'), Hand.LEFT)
        self.assertEqual(layout.get_hand('j'), Hand.RIGHT)
        self.assertEqual(layout.get_hand('k'), Hand.RIGHT)


class TestKeyboardUtils(unittest.TestCase):
    """测试键盘工具类"""
    
    def setUp(self):
        """设置测试"""
        self.ku = KeyboardUtils("qwerty")
    
    def test_initialization(self):
        """测试初始化"""
        self.assertEqual(self.ku.layout_name, "qwerty")
        self.assertIsInstance(self.ku.layout, KeyboardLayout)
    
    def test_invalid_layout(self):
        """测试无效布局"""
        with self.assertRaises(ValueError):
            KeyboardUtils("invalid_layout")
    
    def test_distance_same_key(self):
        """测试同一按键的距离"""
        dist = self.ku.distance('a', 'a')
        self.assertEqual(dist, 0.0)
    
    def test_distance_adjacent_keys(self):
        """测试相邻按键的距离"""
        dist = self.ku.distance('a', 's')
        self.assertLess(dist, 2.0)  # 相邻键
        self.assertGreater(dist, 0)
    
    def test_distance_far_keys(self):
        """测试远距离按键"""
        dist = self.ku.distance('a', 'p')
        self.assertGreater(dist, 5.0)  # 很远
    
    def test_distance_invalid_char(self):
        """测试无效字符的距离"""
        dist = self.ku.distance('a', '中')
        self.assertEqual(dist, float('inf'))
    
    def test_total_distance_empty(self):
        """测试空文本的总距离"""
        dist = self.ku.total_distance("")
        self.assertEqual(dist, 0.0)
    
    def test_total_distance_single(self):
        """测试单字符的总距离"""
        dist = self.ku.total_distance("a")
        self.assertEqual(dist, 0.0)
    
    def test_total_distance_word(self):
        """测试单词的总距离"""
        dist = self.ku.total_distance("hello")
        self.assertGreater(dist, 0)
    
    def test_analyze_empty(self):
        """测试空文本分析"""
        analysis = self.ku.analyze("")
        self.assertEqual(analysis.total_distance, 0.0)
        self.assertEqual(analysis.average_distance, 0.0)
        self.assertEqual(analysis.hand_alternations, 0)
        self.assertEqual(analysis.same_hand_sequences, 0)
    
    def test_analyze_single_char(self):
        """测试单字符分析"""
        analysis = self.ku.analyze("a")
        self.assertEqual(analysis.total_distance, 0.0)
        self.assertEqual(analysis.finger_usage[Finger.LEFT_PINKY], 1)
        self.assertEqual(analysis.hand_usage[Hand.LEFT], 1)
        self.assertEqual(analysis.home_row_usage, 1)
    
    def test_analyze_word(self):
        """测试单词分析"""
        analysis = self.ku.analyze("asdf")
        
        self.assertGreater(analysis.total_distance, 0)
        self.assertEqual(analysis.home_row_usage, 4)
        self.assertEqual(analysis.finger_usage[Finger.LEFT_PINKY], 1)  # a
        self.assertEqual(analysis.finger_usage[Finger.LEFT_RING], 1)   # s
        self.assertEqual(analysis.finger_usage[Finger.LEFT_MIDDLE], 1)  # d
        self.assertEqual(analysis.finger_usage[Finger.LEFT_INDEX], 1)  # f
    
    def test_analyze_hand_alternation(self):
        """测试手交替分析"""
        # "aj" - 左右手交替
        analysis = self.ku.analyze("aj")
        self.assertEqual(analysis.hand_alternations, 1)
        self.assertEqual(analysis.same_hand_sequences, 0)
        
        # "aa" - 同手连续
        analysis = self.ku.analyze("aa")
        self.assertEqual(analysis.hand_alternations, 0)
        self.assertEqual(analysis.same_hand_sequences, 1)
    
    def test_is_same_hand(self):
        """测试同手判断"""
        self.assertTrue(self.ku.is_same_hand('a', 's'))  # 左手
        self.assertTrue(self.ku.is_same_hand('j', 'k'))  # 右手
        self.assertFalse(self.ku.is_same_hand('a', 'j'))  # 不同手
    
    def test_is_same_finger(self):
        """测试同指判断"""
        self.assertTrue(self.ku.is_same_finger('a', 'q'))  # 左小指
        self.assertTrue(self.ku.is_same_finger('j', 'u'))  # 右食指
        self.assertFalse(self.ku.is_same_finger('a', 's'))  # 不同手指
    
    def test_is_adjacent_finger(self):
        """测试相邻手指判断"""
        self.assertTrue(self.ku.is_adjacent_finger('a', 's'))  # 小指-无名指
        self.assertTrue(self.ku.is_adjacent_finger('s', 'd'))  # 无名指-中指
        self.assertFalse(self.ku.is_adjacent_finger('a', 'd'))  # 小指-中指（不相邻）
    
    def test_is_home_row(self):
        """测试基准行判断"""
        self.assertTrue(self.ku.is_home_row('a'))
        self.assertTrue(self.ku.is_home_row('s'))
        self.assertTrue(self.ku.is_home_row('d'))
        self.assertTrue(self.ku.is_home_row('f'))
        self.assertFalse(self.ku.is_home_row('q'))
        self.assertFalse(self.ku.is_home_row('z'))
    
    def test_is_top_row(self):
        """测试上行判断"""
        self.assertTrue(self.ku.is_top_row('q'))
        self.assertTrue(self.ku.is_top_row('w'))
        self.assertTrue(self.ku.is_top_row('e'))
        self.assertFalse(self.ku.is_top_row('a'))
    
    def test_is_bottom_row(self):
        """测试下行判断"""
        self.assertTrue(self.ku.is_bottom_row('z'))
        self.assertTrue(self.ku.is_bottom_row('x'))
        self.assertTrue(self.ku.is_bottom_row('c'))
        self.assertFalse(self.ku.is_bottom_row('a'))
    
    def test_is_number_row(self):
        """测试数字行判断"""
        self.assertTrue(self.ku.is_number_row('1'))
        self.assertTrue(self.ku.is_number_row('2'))
        self.assertTrue(self.ku.is_number_row('0'))
        self.assertFalse(self.ku.is_number_row('a'))
    
    def test_is_consecutive(self):
        """测试相邻键判断"""
        self.assertTrue(self.ku.is_consecutive('a', 's'))
        self.assertTrue(self.ku.is_consecutive('s', 'a'))
        self.assertFalse(self.ku.is_consecutive('a', 'p'))
    
    def test_get_keyboard_patterns_empty(self):
        """测试空文本模式检测"""
        patterns = self.ku.get_keyboard_patterns("")
        self.assertEqual(patterns, [])
    
    def test_get_keyboard_patterns_single(self):
        """测试单字符模式检测"""
        patterns = self.ku.get_keyboard_patterns("a")
        self.assertEqual(patterns, [])
    
    def test_get_keyboard_patterns_consecutive(self):
        """测试连续键模式"""
        patterns = self.ku.get_keyboard_patterns("as")
        consecutive_patterns = [p for p in patterns if p["type"] == "consecutive"]
        self.assertGreater(len(consecutive_patterns), 0)
    
    def test_get_keyboard_patterns_same_finger(self):
        """测试同指模式"""
        patterns = self.ku.get_keyboard_patterns("aq")  # 都是左小指
        same_finger_patterns = [p for p in patterns if p["type"] == "same_finger"]
        self.assertGreater(len(same_finger_patterns), 0)
    
    def test_get_keyboard_patterns_straight_line(self):
        """测试直线模式"""
        patterns = self.ku.get_keyboard_patterns("asd")  # 水平直线
        line_patterns = [p for p in patterns if p["type"] == "straight_line"]
        self.assertGreater(len(line_patterns), 0)
    
    def test_efficiency_score_empty(self):
        """测试空文本效率分数"""
        score = self.ku.get_efficiency_score("")
        self.assertEqual(score, 100.0)
    
    def test_efficiency_score_home_row(self):
        """测试基准行文本效率"""
        score = self.ku.get_efficiency_score("asdfjkl;")
        self.assertGreater(score, 50)  # 高效
    
    def test_efficiency_score_poor(self):
        """测试低效文本"""
        score = self.ku.get_efficiency_score("qpz/")  # 跳跃大
        self.assertLess(score, 80)
    
    def test_suggest_alternatives_empty(self):
        """测试空文本建议"""
        suggestions = self.ku.suggest_alternatives("")
        self.assertEqual(suggestions, [])
    
    def test_suggest_alternatives_same_finger(self):
        """测试同指建议"""
        suggestions = self.ku.suggest_alternatives("aq")  # 都是左小指
        same_finger = [s for s in suggestions if s["type"] == "same_finger"]
        self.assertGreater(len(same_finger), 0)
    
    def test_suggest_alternatives_long_jump(self):
        """测试长距离跳跃建议"""
        suggestions = self.ku.suggest_alternatives("ap")  # a 到 p 距离远
        long_jump = [s for s in suggestions if s["type"] == "long_jump"]
        self.assertGreater(len(long_jump), 0)
    
    def test_suggest_alternatives_double_pinky(self):
        """测试双小指建议"""
        suggestions = self.ku.suggest_alternatives("qp")  # 都是右手小指附近
        # 注意：qp 可能不是同指，测试实际的小指序列
        suggestions = self.ku.suggest_alternatives("qz")  # 左小指 q，左小指 z
        double_pinky = [s for s in suggestions if s["type"] == "double_pinky"]
        self.assertGreater(len(double_pinky), 0)


class TestDifferentLayouts(unittest.TestCase):
    """测试不同键盘布局"""
    
    def test_dvorak_home_row(self):
        """测试 Dvorak 基准行"""
        ku = KeyboardUtils("dvorak")
        # Dvorak 基准行：aoeuidhtns
        self.assertTrue(ku.is_home_row('a'))
        self.assertTrue(ku.is_home_row('o'))
        self.assertTrue(ku.is_home_row('e'))
        self.assertTrue(ku.is_home_row('u'))
        self.assertTrue(ku.is_home_row('i'))
    
    def test_colemak_home_row(self):
        """测试 Colemak 基准行"""
        ku = KeyboardUtils("colemak")
        # Colemak 基准行：arstdhneio
        self.assertTrue(ku.is_home_row('a'))
        self.assertTrue(ku.is_home_row('r'))
        self.assertTrue(ku.is_home_row('s'))
        self.assertTrue(ku.is_home_row('t'))
    
    def test_azerty_layout(self):
        """测试 AZERTY 布局"""
        ku = KeyboardUtils("azerty")
        # AZERTY 第一行是 aze...
        pos = ku.layout.get_key_position('a')
        self.assertIsNotNone(pos)
        self.assertEqual(pos.row, 1)  # 上行
    
    def test_qwertz_layout(self):
        """测试 QWERTZ 布局"""
        ku = KeyboardUtils("qwertz")
        # QWERTZ 有 z 和 y 互换
        pos_z = ku.layout.get_key_position('z')
        self.assertIsNotNone(pos_z)


class TestConvenienceFunctions(unittest.TestCase):
    """测试便捷函数"""
    
    def test_distance_function(self):
        """测试 distance 函数"""
        dist = distance('a', 's')
        self.assertIsInstance(dist, float)
        self.assertGreater(dist, 0)
    
    def test_total_distance_function(self):
        """测试 total_distance 函数"""
        dist = total_distance("hello")
        self.assertIsInstance(dist, float)
        self.assertGreater(dist, 0)
    
    def test_analyze_function(self):
        """测试 analyze 函数"""
        analysis = analyze("test")
        self.assertIsInstance(analysis, TypingAnalysis)
    
    def test_get_key_position_function(self):
        """测试 get_key_position 函数"""
        pos = get_key_position('a')
        self.assertIsNotNone(pos)
        self.assertIsInstance(pos, KeyPosition)
    
    def test_get_coordinates_function(self):
        """测试 get_coordinates 函数"""
        coords = get_coordinates('a')
        self.assertIsNotNone(coords)
        self.assertIsInstance(coords, tuple)
        self.assertEqual(len(coords), 2)
    
    def test_get_finger_function(self):
        """测试 get_finger 函数"""
        finger = get_finger('a')
        self.assertIsNotNone(finger)
        self.assertIsInstance(finger, Finger)
    
    def test_get_hand_function(self):
        """测试 get_hand 函数"""
        hand = get_hand('a')
        self.assertIsNotNone(hand)
        self.assertIsInstance(hand, Hand)
    
    def test_efficiency_score_function(self):
        """测试 efficiency_score 函数"""
        score = efficiency_score("asdf")
        self.assertIsInstance(score, float)
        self.assertGreaterEqual(score, 0)
        self.assertLessEqual(score, 100)
    
    def test_get_keyboard_patterns_function(self):
        """测试 get_keyboard_patterns 函数"""
        patterns = get_keyboard_patterns("asd")
        self.assertIsInstance(patterns, list)
    
    def test_suggest_improvements_function(self):
        """测试 suggest_improvements 函数"""
        suggestions = suggest_improvements("aq")
        self.assertIsInstance(suggestions, list)
    
    def test_available_layouts_function(self):
        """测试 available_layouts 函数"""
        layouts = available_layouts()
        self.assertIsInstance(layouts, list)
        self.assertIn("qwerty", layouts)
        self.assertIn("dvorak", layouts)
        self.assertIn("colemak", layouts)
    
    def test_get_utils_caching(self):
        """测试 get_utils 缓存"""
        utils1 = get_utils("qwerty")
        utils2 = get_utils("qwerty")
        self.assertIs(utils1, utils2)
        
        utils3 = get_utils("dvorak")
        self.assertIsNot(utils1, utils3)


class TestEdgeCases(unittest.TestCase):
    """测试边界情况"""
    
    def test_special_characters(self):
        """测试特殊字符"""
        ku = KeyboardUtils("qwerty")
        
        # 测试特殊字符能获取位置
        pos = ku.layout.get_key_position('!')
        self.assertIsNotNone(pos)
        
        pos = ku.layout.get_key_position('@')
        self.assertIsNotNone(pos)
        
        pos = ku.layout.get_key_position(' ')
        self.assertIsNotNone(pos)  # 空格
    
    def test_unicode_characters(self):
        """测试 Unicode 字符"""
        ku = KeyboardUtils("qwerty")
        
        # Unicode 字符不在标准键盘上
        pos = ku.layout.get_key_position('中')
        self.assertIsNone(pos)
        
        pos = ku.layout.get_key_position('😀')
        self.assertIsNone(pos)
    
    def test_mixed_text(self):
        """测试混合文本"""
        ku = KeyboardUtils("qwerty")
        
        # 混合英文和中文
        analysis = ku.analyze("hello世界")
        self.assertGreater(analysis.total_distance, 0)
        
        # 中文字符不计入距离，但英文部分计入
        self.assertEqual(analysis.finger_usage[Finger.LEFT_PINKY], 0)  # h 不是小指
    
    def test_long_text(self):
        """测试长文本"""
        ku = KeyboardUtils("qwerty")
        
        long_text = "the quick brown fox jumps over the lazy dog " * 10
        analysis = ku.analyze(long_text)
        
        self.assertGreater(analysis.total_distance, 0)
        self.assertGreater(analysis.hand_alternations, 0)
    
    def test_case_insensitivity(self):
        """测试大小写不敏感"""
        ku = KeyboardUtils("qwerty")
        
        # 小写和大写应该返回相同的位置
        pos_lower = ku.layout.get_key_position('a')
        pos_upper = ku.layout.get_key_position('A')
        
        self.assertEqual(pos_lower.row, pos_upper.row)
        self.assertEqual(pos_lower.col, pos_upper.col)
        self.assertEqual(pos_lower.finger, pos_upper.finger)
    
    def test_space_key(self):
        """测试空格键"""
        ku = KeyboardUtils("qwerty")
        
        pos = ku.layout.get_key_position(' ')
        self.assertIsNotNone(pos)
        # 空格用拇指
        self.assertIn(pos.finger, [Finger.LEFT_THUMB, Finger.RIGHT_THUMB])


class TestTypingAnalysis(unittest.TestCase):
    """测试打字分析结果"""
    
    def test_analysis_dataclass(self):
        """测试分析结果数据类"""
        analysis = TypingAnalysis(
            total_distance=10.5,
            average_distance=1.05,
            hand_alternations=5,
            same_hand_sequences=3,
            finger_usage={f: 0 for f in Finger},
            hand_usage={h: 0 for h in Hand},
            rolling_sequences=2,
            home_row_usage=5,
            top_row_usage=3,
            bottom_row_usage=2,
            number_row_usage=0
        )
        
        self.assertEqual(analysis.total_distance, 10.5)
        self.assertEqual(analysis.average_distance, 1.05)
        self.assertEqual(analysis.hand_alternations, 5)
        self.assertEqual(analysis.same_hand_sequences, 3)
        self.assertEqual(analysis.rolling_sequences, 2)
        self.assertEqual(analysis.home_row_usage, 5)
    
    def test_finger_usage_complete(self):
        """测试手指使用统计完整性"""
        ku = KeyboardUtils("qwerty")
        analysis = ku.analyze("asdfjkl;")
        
        # 所有手指都应该在统计中
        for finger in Finger:
            self.assertIn(finger, analysis.finger_usage)
    
    def test_hand_usage_complete(self):
        """测试手使用统计完整性"""
        ku = KeyboardUtils("qwerty")
        analysis = ku.analyze("asdfjkl;")
        
        # 所有手都应该在统计中
        for hand in Hand:
            self.assertIn(hand, analysis.hand_usage)


class TestFingerAndHandEnums(unittest.TestCase):
    """测试手指和手枚举"""
    
    def test_finger_enum_values(self):
        """测试手指枚举值"""
        self.assertEqual(Finger.LEFT_PINKY.value, "left_pinky")
        self.assertEqual(Finger.LEFT_RING.value, "left_ring")
        self.assertEqual(Finger.LEFT_MIDDLE.value, "left_middle")
        self.assertEqual(Finger.LEFT_INDEX.value, "left_index")
        self.assertEqual(Finger.RIGHT_INDEX.value, "right_index")
        self.assertEqual(Finger.RIGHT_MIDDLE.value, "right_middle")
        self.assertEqual(Finger.RIGHT_RING.value, "right_ring")
        self.assertEqual(Finger.RIGHT_PINKY.value, "right_pinky")
    
    def test_hand_enum_values(self):
        """测试手枚举值"""
        self.assertEqual(Hand.LEFT.value, "left")
        self.assertEqual(Hand.RIGHT.value, "right")
        self.assertEqual(Hand.BOTH.value, "both")


if __name__ == "__main__":
    unittest.main(verbosity=2)