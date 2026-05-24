"""
One Rep Max Utilities - 测试套件

测试覆盖所有公式、综合计算、反向计算、训练计划生成等功能。
"""

import sys
import os
import math
import unittest

# 路径设置
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from one_rep_max_utils.mod import (
    # 核心公式
    brzycki, epley, lander, lombardi, oconner, wathan, mayhew, baechle,
    # 综合计算
    calculate_1rm, calculate_all_formulas, average_1rm,
    # 反向计算
    calculate_weight_for_reps, calculate_percentage_weight,
    # 训练计划
    generate_rep_max_table, generate_percentage_table, estimate_reps_at_weight,
    # 进度追踪
    calculate_strength_level, calculate_wilks_score, compare_1rm,
    # 辅助功能
    round_to_plate, suggest_warmup_weights, validate_input,
    get_available_formulas, get_formula_description,
    # 类
    OneRepMaxCalculator,
    # 常量
    FORMULAS
)


class TestCoreFormulas(unittest.TestCase):
    """测试核心公式计算"""
    
    def test_brzycki_basic(self):
        """测试Brzycki公式基本计算"""
        # 100kg做5次
        result = brzycki(100, 5)
        expected = 100 * 36 / (37 - 5)  # = 116.13
        self.assertAlmostEqual(result, expected, places=2)
    
    def test_brzycki_1_rep(self):
        """测试Brzycki公式1次等于重量本身"""
        result = brzycki(100, 1)
        self.assertEqual(result, 100)
    
    def test_brzycki_high_reps(self):
        """测试Brzycki公式高次数"""
        result = brzycki(80, 10)
        self.assertAlmostEqual(result, 106.67, places=2)
    
    def test_epley_basic(self):
        """测试Epley公式基本计算"""
        result = epley(100, 5)
        expected = 100 * (1 + 5/30)  # = 116.67
        self.assertAlmostEqual(result, expected, places=2)
    
    def test_epley_1_rep(self):
        """测试Epley公式1次等于重量本身"""
        result = epley(100, 1)
        self.assertEqual(result, 100)
    
    def test_lander_basic(self):
        """测试Lander公式基本计算"""
        result = lander(100, 5)
        # Lander: 100*100/(101.3 - 2.67123*5) ≈ 113.71
        self.assertAlmostEqual(result, 113.71, places=2)
    
    def test_lander_1_rep(self):
        """测试Lander公式1次"""
        result = lander(100, 1)
        self.assertEqual(result, 100)
    
    def test_lombardi_basic(self):
        """测试Lombardi公式基本计算"""
        result = lombardi(100, 5)
        expected = 100 * (5 ** 0.10)
        self.assertAlmostEqual(result, expected, places=2)
    
    def test_lombardi_1_rep(self):
        """测试Lombardi公式1次"""
        result = lombardi(100, 1)
        self.assertEqual(result, 100)
    
    def test_oconner_basic(self):
        """测试O'Conner公式基本计算"""
        result = oconner(100, 5)
        expected = 100 * (1 + 5/40)  # = 112.5
        self.assertAlmostEqual(result, expected, places=2)
    
    def test_oconner_1_rep(self):
        """测试O'Conner公式1次"""
        result = oconner(100, 1)
        self.assertEqual(result, 100)
    
    def test_wathan_basic(self):
        """测试Wathan公式基本计算"""
        result = wathan(100, 5)
        # Wathan公式计算
        self.assertGreater(result, 110)
        self.assertLess(result, 120)
    
    def test_wathan_1_rep(self):
        """测试Wathan公式1次"""
        result = wathan(100, 1)
        self.assertEqual(result, 100)
    
    def test_mayhew_basic(self):
        """测试Mayhew公式基本计算"""
        result = mayhew(100, 5)
        # Mayhew公式计算
        self.assertGreater(result, 115)
        self.assertLess(result, 125)
    
    def test_mayhew_1_rep(self):
        """测试Mayhew公式1次"""
        result = mayhew(100, 1)
        self.assertEqual(result, 100)
    
    def test_baechle_equals_wathan(self):
        """测试Baechle公式等于Wathan"""
        result1 = baechle(100, 5)
        result2 = wathan(100, 5)
        self.assertEqual(result1, result2)
    
    def test_invalid_weight(self):
        """测试无效重量"""
        with self.assertRaises(ValueError):
            brzycki(0, 5)
        with self.assertRaises(ValueError):
            brzycki(-10, 5)
    
    def test_invalid_reps(self):
        """测试无效次数"""
        with self.assertRaises(ValueError):
            brzycki(100, 0)
        with self.assertRaises(ValueError):
            brzycki(100, -1)
    
    def test_all_formulas_consistency(self):
        """测试所有公式结果一致性（范围在合理偏差内）"""
        weight = 100
        reps = 5
        results = calculate_all_formulas(weight, reps)
        
        # 所有结果应该在110-120范围内
        for name, value in results.items():
            self.assertGreater(value, 110)
            self.assertLess(value, 120)


class TestCalculate1RM(unittest.TestCase):
    """测试综合计算函数"""
    
    def test_calculate_1rm_default(self):
        """测试默认公式（Brzycki）"""
        result = calculate_1rm(100, 5)
        expected = brzycki(100, 5)
        self.assertEqual(result, expected)
    
    def test_calculate_1rm_specified_formula(self):
        """测试指定公式"""
        result = calculate_1rm(100, 5, 'epley')
        expected = epley(100, 5)
        self.assertEqual(result, expected)
    
    def test_calculate_1rm_case_insensitive(self):
        """测试公式名称大小写不敏感"""
        result1 = calculate_1rm(100, 5, 'BRZYCKI')
        result2 = calculate_1rm(100, 5, 'Brzycki')
        result3 = calculate_1rm(100, 5, 'brzycki')
        self.assertEqual(result1, result2)
        self.assertEqual(result2, result3)
    
    def test_calculate_1rm_invalid_formula(self):
        """测试无效公式名称"""
        with self.assertRaises(ValueError):
            calculate_1rm(100, 5, 'unknown')
    
    def test_calculate_all_formulas(self):
        """测试所有公式计算"""
        results = calculate_all_formulas(100, 5)
        
        # 应该返回8个公式结果
        self.assertEqual(len(results), 8)
        
        # 检查所有公式名称
        expected_formulas = ['brzycki', 'epley', 'lander', 'lombardi', 
                            'oconner', 'wathan', 'mayhew', 'baechle']
        self.assertEqual(set(results.keys()), set(expected_formulas))
    
    def test_average_1rm_all_formulas(self):
        """测试使用所有公式的平均值"""
        result = average_1rm(100, 5)
        
        # 平均值应该在115-117范围内
        self.assertGreater(result, 115)
        self.assertLess(result, 117)
    
    def test_average_1rm_selected_formulas(self):
        """测试指定公式的平均值"""
        result = average_1rm(100, 5, ['brzycki', 'epley'])
        expected = (brzycki(100, 5) + epley(100, 5)) / 2
        self.assertEqual(result, expected)


class TestReverseCalculation(unittest.TestCase):
    """测试反向计算"""
    
    def test_calculate_weight_for_reps_brzycki(self):
        """测试Brzycki反向计算"""
        # 120kg 1RM，做5次应该用多少重量
        result = calculate_weight_for_reps(120, 5, 'brzycki')
        
        # 反向验证
        estimated_1rm = brzycki(result, 5)
        self.assertAlmostEqual(estimated_1rm, 120, places=2)
    
    def test_calculate_weight_for_reps_epley(self):
        """测试Epley反向计算"""
        result = calculate_weight_for_reps(120, 5, 'epley')
        
        # 反向验证
        estimated_1rm = epley(result, 5)
        self.assertAlmostEqual(estimated_1rm, 120, places=2)
    
    def test_calculate_weight_for_reps_1_rep(self):
        """测试1次等于1RM本身"""
        result = calculate_weight_for_reps(100, 1)
        self.assertEqual(result, 100)
    
    def test_calculate_weight_for_reps_numerical(self):
        """测试需要数值逼近的公式"""
        result = calculate_weight_for_reps(120, 5, 'wathan')
        
        # 反向验证
        estimated_1rm = wathan(result, 5)
        self.assertAlmostEqual(estimated_1rm, 120, places=1)
    
    def test_calculate_percentage_weight(self):
        """测试百分比重量计算"""
        result = calculate_percentage_weight(100, 80)
        self.assertEqual(result, 80)
        
        result = calculate_percentage_weight(100, 50)
        self.assertEqual(result, 50)
        
        result = calculate_percentage_weight(120, 75)
        self.assertEqual(result, 90)


class TestTrainingPlan(unittest.TestCase):
    """测试训练计划生成"""
    
    def test_generate_rep_max_table(self):
        """测试nRM表生成"""
        table = generate_rep_max_table(100)
        
        # 1RM应该等于100
        self.assertEqual(table[1], 100)
        
        # 2RM应该略低于100
        self.assertLess(table[2], 100)
        self.assertGreater(table[2], 90)
        
        # 检查所有次数
        self.assertEqual(len(table), 12)
    
    def test_generate_rep_max_table_max_reps(self):
        """测试自定义最大次数"""
        table = generate_rep_max_table(100, max_reps=15)
        self.assertEqual(len(table), 15)
    
    def test_generate_percentage_table_default(self):
        """测试默认百分比表"""
        table = generate_percentage_table(100)
        
        # 检查默认百分比
        self.assertEqual(len(table), 10)
        self.assertEqual(table[95], 95)
        self.assertEqual(table[80], 80)
        self.assertEqual(table[50], 50)
    
    def test_generate_percentage_table_custom(self):
        """测试自定义百分比表"""
        table = generate_percentage_table(100, [100, 90, 80, 70])
        
        self.assertEqual(len(table), 4)
        self.assertEqual(table[100], 100)
        self.assertEqual(table[70], 70)
    
    def test_estimate_reps_at_weight(self):
        """测试估算次数"""
        # 100kg 1RM，80kg能做多少次
        reps = estimate_reps_at_weight(100, 80)
        
        # 应该在7-9次范围
        self.assertGreater(reps, 6)
        self.assertLess(reps, 10)
    
    def test_estimate_reps_at_weight_1rm(self):
        """测试重量等于1RM"""
        reps = estimate_reps_at_weight(100, 100)
        self.assertEqual(reps, 1)
    
    def test_estimate_reps_at_weight_very_light(self):
        """测试很轻重量"""
        reps = estimate_reps_at_weight(100, 50)
        self.assertGreater(reps, 15)


class TestProgressTracking(unittest.TestCase):
    """测试进度追踪功能"""
    
    def test_calculate_strength_level_bench_male(self):
        """测试男性卧推力量等级"""
        # Elite: >= 1.5倍体重
        level = calculate_strength_level(150, 100, 'male', 'bench_press')
        self.assertEqual(level, 'Elite')
        
        # Advanced: >= 1.2倍体重
        level = calculate_strength_level(130, 100, 'male', 'bench_press')
        self.assertEqual(level, 'Advanced')
        
        # Intermediate: >= 1.0倍体重
        level = calculate_strength_level(100, 100, 'male', 'bench_press')
        self.assertEqual(level, 'Intermediate')
        
        # Novice: >= 0.75倍体重
        level = calculate_strength_level(80, 100, 'male', 'bench_press')
        self.assertEqual(level, 'Novice')
        
        # Beginner: < 0.75倍体重
        level = calculate_strength_level(60, 100, 'male', 'bench_press')
        self.assertEqual(level, 'Beginner')
    
    def test_calculate_strength_level_bench_female(self):
        """测试女性卧推力量等级"""
        # Elite: >= 1.0倍体重
        level = calculate_strength_level(70, 70, 'female', 'bench_press')
        self.assertEqual(level, 'Elite')
        
        # Intermediate: >= 0.6倍体重
        level = calculate_strength_level(42, 70, 'female', 'bench_press')
        self.assertEqual(level, 'Intermediate')
    
    def test_calculate_strength_level_squat(self):
        """测试深蹲力量等级"""
        # Elite male: >= 2.0倍体重
        level = calculate_strength_level(200, 100, 'male', 'squat')
        self.assertEqual(level, 'Elite')
        
        # Intermediate male: >= 1.4倍体重
        level = calculate_strength_level(150, 100, 'male', 'squat')
        self.assertEqual(level, 'Intermediate')
    
    def test_calculate_strength_level_deadlift(self):
        """测试硬拉力量等级"""
        # Elite male: >= 2.5倍体重
        level = calculate_strength_level(250, 100, 'male', 'deadlift')
        self.assertEqual(level, 'Elite')
    
    def test_calculate_strength_level_unknown_exercise(self):
        """测试未知动作（使用默认）"""
        level = calculate_strength_level(100, 100, 'male', 'unknown')
        self.assertEqual(level, 'Intermediate')
    
    def test_calculate_wilks_score_male(self):
        """测试男性Wilks得分"""
        # 150kg举重，75kg体重（单次举重）
        score = calculate_wilks_score(150, 75, 'male')
        # Wilks得分应该是合理的正值（单次举重得分较低）
        self.assertGreater(score, 20)
        self.assertLess(score, 100)
    
    def test_calculate_wilks_score_female(self):
        """测试女性Wilks得分"""
        score = calculate_wilks_score(100, 60, 'female')
        self.assertGreater(score, 100)
    
    def test_calculate_wilks_score_lb_unit(self):
        """测试磅单位"""
        # 330lb（约150kg），165lb（约75kg）
        score_lb = calculate_wilks_score(330, 165, 'male', 'lb')
        score_kg = calculate_wilks_score(150, 75, 'male', 'kg')
        
        # 应该近似相等（允许10%误差）
        self.assertLess(abs(score_lb - score_kg) / score_kg, 0.1)
    
    def test_compare_1rm_improvement(self):
        """测试进步比较"""
        result = compare_1rm(100, 110)
        
        self.assertEqual(result['change'], 10)
        self.assertEqual(result['percentage'], 10)
        self.assertTrue(result['is_improvement'])
    
    def test_compare_1rm_decline(self):
        """测试退步比较"""
        result = compare_1rm(100, 90)
        
        self.assertEqual(result['change'], -10)
        self.assertEqual(result['percentage'], -10)
        self.assertFalse(result['is_improvement'])
    
    def test_compare_1rm_no_change(self):
        """测试无变化"""
        result = compare_1rm(100, 100)
        
        self.assertEqual(result['change'], 0)
        self.assertEqual(result['percentage'], 0)
        self.assertFalse(result['is_improvement'])


class TestHelperFunctions(unittest.TestCase):
    """测试辅助功能"""
    
    def test_round_to_plate_kg(self):
        """测试公斤杠铃片四舍五入"""
        # 默认公斤杠铃片：1.25最小，两倍=2.5最小增量
        result = round_to_plate(87.3)
        self.assertEqual(result, 87.5)
        
        result = round_to_plate(86.2)
        self.assertEqual(result, 85.0)
    
    def test_round_to_plate_lb(self):
        """测试磅杠铃片四舍五入"""
        # 默认磅杠铃片：2.5最小，两倍=5最小增量
        result = round_to_plate(187.3, unit='lb')
        self.assertEqual(result, 185.0)
    
    def test_round_to_plate_custom(self):
        """测试自定义杠铃片"""
        result = round_to_plate(87.3, plate_sizes=[5, 10, 20])
        self.assertEqual(result, 90.0)
    
    def test_suggest_warmup_weights(self):
        """测试热身组建议"""
        warmup = suggest_warmup_weights(100, 80)
        
        # 应该有几组热身
        self.assertGreater(len(warmup), 0)
        
        # 第一组应该是最轻的
        first_weight = warmup[0][0]
        self.assertLess(first_weight, 80)
        
        # 最后一组应该接近工作组
        last_weight = warmup[-1][0]
        self.assertLessEqual(last_weight, 80)
    
    def test_suggest_warmup_weights_all_below_working(self):
        """所有热身重量低于工作组"""
        warmup = suggest_warmup_weights(100, 90)
        for weight, reps in warmup:
            self.assertLess(weight, 90)
    
    def test_validate_input_valid(self):
        """测试有效输入"""
        valid, msg = validate_input(100, 5)
        self.assertTrue(valid)
        self.assertEqual(msg, '')
    
    def test_validate_input_zero_weight(self):
        """测试零重量"""
        valid, msg = validate_input(0, 5)
        self.assertFalse(valid)
        self.assertIn('positive', msg)
    
    def test_validate_input_negative_weight(self):
        """测试负重量"""
        valid, msg = validate_input(-10, 5)
        self.assertFalse(valid)
    
    def test_validate_input_zero_reps(self):
        """测试零次数"""
        valid, msg = validate_input(100, 0)
        self.assertFalse(valid)
    
    def test_validate_input_high_reps(self):
        """测试高次数"""
        valid, msg = validate_input(100, 35)
        self.assertFalse(valid)
        self.assertIn('30', msg)
    
    def test_get_available_formulas(self):
        """测试获取可用公式"""
        formulas = get_available_formulas()
        
        self.assertEqual(len(formulas), 8)
        self.assertIn('brzycki', formulas)
        self.assertIn('epley', formulas)
    
    def test_get_formula_description(self):
        """测试获取公式描述"""
        desc = get_formula_description('brzycki')
        self.assertIn('Brzycki', desc)
        
        desc = get_formula_description('unknown')
        self.assertEqual(desc, 'Unknown formula')


class TestOneRepMaxCalculator(unittest.TestCase):
    """测试计算器类"""
    
    def test_init_default_formula(self):
        """测试默认公式初始化"""
        calc = OneRepMaxCalculator()
        self.assertEqual(calc.formula, 'brzycki')
    
    def test_init_custom_formula(self):
        """测试自定义公式初始化"""
        calc = OneRepMaxCalculator('epley')
        self.assertEqual(calc.formula, 'epley')
    
    def test_init_invalid_formula(self):
        """测试无效公式初始化"""
        with self.assertRaises(ValueError):
            OneRepMaxCalculator('unknown')
    
    def test_calculate(self):
        """测试计算方法"""
        calc = OneRepMaxCalculator('brzycki')
        result = calc.calculate(100, 5)
        
        expected = brzycki(100, 5)
        self.assertEqual(result, expected)
    
    def test_calculate_all(self):
        """测试计算所有公式"""
        calc = OneRepMaxCalculator()
        results = calc.calculate_all(100, 5)
        
        self.assertEqual(len(results), 8)
    
    def test_calculate_average(self):
        """测试计算平均值"""
        calc = OneRepMaxCalculator()
        avg = calc.calculate_average(100, 5)
        
        self.assertGreater(avg, 115)
        self.assertLess(avg, 117)
    
    def test_calculate_weight_for_reps(self):
        """测试反向计算"""
        calc = OneRepMaxCalculator('brzycki')
        weight = calc.calculate_weight_for_reps(120, 5)
        
        # 验证
        estimated = calc.calculate(weight, 5)
        self.assertAlmostEqual(estimated, 120, places=2)
    
    def test_generate_table(self):
        """测试生成nRM表"""
        calc = OneRepMaxCalculator()
        table = calc.generate_table(100)
        
        self.assertEqual(table[1], 100)
        self.assertEqual(len(table), 12)
    
    def test_estimate_reps(self):
        """测试估算次数"""
        calc = OneRepMaxCalculator()
        reps = calc.estimate_reps(100, 80)
        
        self.assertGreater(reps, 6)
        self.assertLess(reps, 10)
    
    def test_suggest_warmup(self):
        """测试热身建议"""
        calc = OneRepMaxCalculator()
        warmup = calc.suggest_warmup(100, 80)
        
        self.assertGreater(len(warmup), 0)
    
    def test_compare(self):
        """测试进步比较"""
        calc = OneRepMaxCalculator()
        result = calc.compare(100, 110)
        
        self.assertEqual(result['change'], 10)
        self.assertTrue(result['is_improvement'])


class TestBoundaryCases(unittest.TestCase):
    """测试边界情况"""
    
    def test_very_light_weight(self):
        """测试极轻重量"""
        result = brzycki(1, 5)
        self.assertGreater(result, 1)
    
    def test_very_heavy_weight(self):
        """测试极重重量"""
        result = brzycki(500, 3)
        self.assertGreater(result, 500)
    
    def test_min_reps(self):
        """测试最小次数（1次）"""
        for formula in FORMULAS.values():
            result = formula(100, 1)
            self.assertEqual(result, 100)
    
    def test_max_valid_reps(self):
        """测试最大有效次数（30次）"""
        result = brzycki(50, 30)
        # 验证输入
        valid, _ = validate_input(50, 30)
        self.assertTrue(valid)
    
    def test_float_weight(self):
        """测试浮点重量"""
        result = brzycki(87.5, 5)
        self.assertGreater(result, 87.5)
    
    def test_float_result_precision(self):
        """测试浮点结果精度"""
        result = brzycki(100, 7)
        # 应该是精确的浮点数
        self.assertIsInstance(result, float)
        self.assertAlmostEqual(result, 100 * 36 / 30, places=10)
    
    def test_consistency_1_rep_all_formulas(self):
        """测试所有公式在1次时的一致性"""
        weight = 100
        for name, formula in FORMULAS.items():
            result = formula(weight, 1)
            self.assertEqual(result, weight)


class TestRealWorldScenarios(unittest.TestCase):
    """测试真实场景"""
    
    def test_typical_bench_press_scenario(self):
        """测试典型卧推场景"""
        # 卧推80kg做8次，估算1RM
        one_rm = calculate_1rm(80, 8)
        self.assertGreater(one_rm, 95)
        self.assertLess(one_rm, 110)
    
    def test_typical_squat_scenario(self):
        """测试典型深蹲场景"""
        # 深蹲120kg做5次
        one_rm = calculate_1rm(120, 5)
        self.assertGreater(one_rm, 130)
        self.assertLess(one_rm, 150)
    
    def test_progressive_overload_tracking(self):
        """测试渐进负荷追踪"""
        # 第一周：80kg 5次
        week1 = calculate_1rm(80, 5)
        
        # 第二周：85kg 5次（进步）
        week2 = calculate_1rm(85, 5)
        
        # 比较进步
        progress = compare_1rm(week1, week2)
        self.assertTrue(progress['is_improvement'])
    
    def test_warmup_before_heavy_lift(self):
        """测试大重量前的热身"""
        # 目标：硬拉180kg
        one_rm = 180
        
        # 工作组150kg
        warmup = suggest_warmup_weights(one_rm, 150)
        
        # 应有渐进热身
        weights = [w[0] for w in warmup]
        self.assertTrue(all(weights[i] < weights[i+1] for i in range(len(weights)-1)))
    
    def test_deload_calculation(self):
        """测试减载计算"""
        # 1RM 100kg，减载到70%
        deload_weight = calculate_percentage_weight(100, 70)
        self.assertEqual(deload_weight, 70)
    
    def test_strength_level_assessment(self):
        """测试力量等级评估"""
        # 卧推100kg，体重80kg的男性
        level = calculate_strength_level(100, 80, 'male', 'bench_press')
        
        # 100/80 = 1.25，应该是Advanced
        self.assertEqual(level, 'Advanced')


class TestEdgeCases(unittest.TestCase):
    """测试极端情况"""
    
    def test_reps_approaching_formula_limit(self):
        """测试接近公式限制的次数"""
        # Brzycki公式在reps接近37时有问题
        # 但我们限制输入在30次以内
        result = brzycki(50, 10)
        self.assertGreater(result, 50)
    
    def test_percentage_weight_zero_percent(self):
        """测试零百分比"""
        result = calculate_percentage_weight(100, 0)
        self.assertEqual(result, 0)
    
    def test_percentage_weight_100_percent(self):
        """测试100%百分比"""
        result = calculate_percentage_weight(100, 100)
        self.assertEqual(result, 100)
    
    def test_compare_with_zero_old_1rm(self):
        """测试旧1RM为零的比较"""
        result = compare_1rm(0, 100)
        self.assertEqual(result['percentage'], 0)  # 无法计算百分比
    
    def test_strength_level_very_strong(self):
        """测试非常强的力量等级"""
        # 深拉300kg，体重80kg
        level = calculate_strength_level(300, 80, 'male', 'deadlift')
        # 300/80 = 3.75，应该是Elite
        self.assertEqual(level, 'Elite')
    
    def test_strength_level_very_weak(self):
        """测试很弱的力量等级"""
        level = calculate_strength_level(20, 80, 'male', 'bench_press')
        self.assertEqual(level, 'Beginner')


def run_tests():
    """运行所有测试"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # 添加所有测试类
    suite.addTests(loader.loadTestsFromTestCase(TestCoreFormulas))
    suite.addTests(loader.loadTestsFromTestCase(TestCalculate1RM))
    suite.addTests(loader.loadTestsFromTestCase(TestReverseCalculation))
    suite.addTests(loader.loadTestsFromTestCase(TestTrainingPlan))
    suite.addTests(loader.loadTestsFromTestCase(TestProgressTracking))
    suite.addTests(loader.loadTestsFromTestCase(TestHelperFunctions))
    suite.addTests(loader.loadTestsFromTestCase(TestOneRepMaxCalculator))
    suite.addTests(loader.loadTestsFromTestCase(TestBoundaryCases))
    suite.addTests(loader.loadTestsFromTestCase(TestRealWorldScenarios))
    suite.addTests(loader.loadTestsFromTestCase(TestEdgeCases))
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result


if __name__ == '__main__':
    result = run_tests()
    
    # 输出摘要
    print("\n" + "="*60)
    print("测试摘要")
    print("="*60)
    print(f"总测试数: {result.testsRun}")
    print(f"成功: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"失败: {len(result.failures)}")
    print(f"错误: {len(result.errors)}")
    print("="*60)
    
    sys.exit(0 if result.wasSuccessful() else 1)