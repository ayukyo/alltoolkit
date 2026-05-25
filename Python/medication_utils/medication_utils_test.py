"""
Medication Utilities - 测试文件

测试药物剂量计算工具的各项功能。
"""

import unittest
import math
from mod import (
    MedicationCalculator,
    MedicationInfo,
    DoseRange,
    DoseUnit,
    WeightUnit,
    Route,
    InfusionCalculator,
    HalfLifeCalculator,
    DoseConverter,
    RenalDoseAdjuster,
    DrugInteractionChecker,
    COMMON_MEDICATIONS,
    get_medication,
    calculate_dose
)


class TestDoseRange(unittest.TestCase):
    """测试剂量范围"""
    
    def test_contains_valid_dose(self):
        """测试剂量在范围内"""
        dose_range = DoseRange(10, 20, DoseUnit.MG)
        self.assertTrue(dose_range.contains(15))
        self.assertTrue(dose_range.contains(10))
        self.assertTrue(dose_range.contains(20))
    
    def test_contains_invalid_dose(self):
        """测试剂量超出范围"""
        dose_range = DoseRange(10, 20, DoseUnit.MG)
        self.assertFalse(dose_range.contains(5))
        self.assertFalse(dose_range.contains(25))
    
    def test_is_too_low(self):
        """测试剂量过低"""
        dose_range = DoseRange(10, 20, DoseUnit.MG)
        self.assertTrue(dose_range.is_too_low(5))
        self.assertFalse(dose_range.is_too_low(10))
        self.assertFalse(dose_range.is_too_low(15))
    
    def test_is_too_high(self):
        """测试剂量过高"""
        dose_range = DoseRange(10, 20, DoseUnit.MG)
        self.assertTrue(dose_range.is_too_high(25))
        self.assertFalse(dose_range.is_too_high(20))
        self.assertFalse(dose_range.is_too_high(15))


class TestMedicationCalculator(unittest.TestCase):
    """测试药物剂量计算器"""
    
    def setUp(self):
        """设置测试数据"""
        self.med = MedicationInfo(
            name="Test Drug",
            standard_dose_per_kg=10,
            dose_unit=DoseUnit.MG,
            dose_range=DoseRange(5, 15, DoseUnit.MG),
            max_daily_dose=1000  # 1000mg 为每日最大剂量
        )
        self.calculator = MedicationCalculator(self.med)
    
    def test_calculate_weight_based_dose_kg(self):
        """测试按体重计算剂量（公斤）"""
        # 70kg × 10mg/kg = 700mg
        dose = self.calculator.calculate_weight_based_dose(70)
        self.assertEqual(dose, 700)
        
        # 50kg × 10mg/kg = 500mg
        dose = self.calculator.calculate_weight_based_dose(50)
        self.assertEqual(dose, 500)
    
    def test_calculate_weight_based_dose_lb(self):
        """测试按体重计算剂量（磅）"""
        # 154 lb ≈ 69.85 kg
        # 69.85 kg × 10 mg/kg ≈ 698.5 mg
        dose = self.calculator.calculate_weight_based_dose(154, WeightUnit.LB)
        self.assertAlmostEqual(dose, 698.5, places=1)
    
    def test_calculate_pediatric_dose_fried(self):
        """测试 Fried 规则计算儿童剂量"""
        # 12个月婴儿
        # 成人剂量 = 70 × 10 = 700mg
        # 儿童剂量 = 700 × (12/150) = 56mg
        dose = self.calculator.calculate_pediatric_dose_fried(12)
        self.assertEqual(dose, 56)
    
    def test_calculate_pediatric_dose_young(self):
        """测试 Young 规则计算儿童剂量"""
        # 6岁儿童
        # 成人剂量 = 70 × 10 = 700mg
        # 儿童剂量 = 700 × (6/(6+12)) = 700 × 0.333... ≈ 233.33mg
        dose = self.calculator.calculate_pediatric_dose_young(6)
        self.assertAlmostEqual(dose, 233.33, places=2)
    
    def test_calculate_pediatric_dose_clark(self):
        """测试 Clark 规则计算儿童剂量"""
        # 50磅儿童
        # 成人剂量 = 70 × 10 = 700mg
        # 儿童剂量 = 700 × (50/150) = 233.33mg
        dose = self.calculator.calculate_pediatric_dose_clark(50, WeightUnit.LB)
        self.assertAlmostEqual(dose, 233.33, places=2)
    
    def test_calculate_pediatric_dose_body_surface(self):
        """测试体表面积法计算儿童剂量"""
        # 20kg, 110cm 儿童
        # BSA = √(110 × 20 / 3600) ≈ 0.78 m²
        # 成人 BSA ≈ 1.73 m², 成人剂量 = 700mg
        # 儿童剂量 = 700 × (0.78/1.73) ≈ 315.6mg
        dose = self.calculator.calculate_pediatric_dose_body_surface(20, 110)
        self.assertAlmostEqual(dose, 316.3, places=1)
    
    def test_validate_dose_valid(self):
        """测试有效剂量验证"""
        # 验证70kg成人的700mg剂量（10mg/kg）
        result = self.calculator.validate_dose(700, weight=70)
        self.assertTrue(result["is_valid"])
        self.assertEqual(len(result["errors"]), 0)
    
    def test_validate_dose_too_low(self):
        """测试剂量过低验证"""
        # 3mg/70kg = 0.043mg/kg，远低于范围 5-15mg/kg
        result = self.calculator.validate_dose(3, weight=70)
        self.assertFalse(result["is_valid"])
        self.assertTrue(len(result["errors"]) > 0)
    
    def test_validate_dose_too_high(self):
        """测试剂量过高验证"""
        # 1500mg/70kg = 21.4mg/kg，超过范围 5-15mg/kg
        result = self.calculator.validate_dose(1500, weight=70)
        self.assertFalse(result["is_valid"])
        self.assertTrue(len(result["errors"]) > 0)
    
    def test_validate_dose_negative(self):
        """测试负剂量验证"""
        result = self.calculator.validate_dose(-10)
        self.assertFalse(result["is_valid"])
        self.assertTrue(len(result["errors"]) > 0)
        # 负数会先触发"正数"检查
        self.assertTrue("正数" in result["errors"][0] or "必须" in result["errors"][0])


class TestInfusionCalculator(unittest.TestCase):
    """测试输液计算器"""
    
    def test_calculate_drip_rate(self):
        """测试输液滴速计算"""
        # 1000ml, 60分钟, 滴系数20
        # 滴速 = (1000 × 20) / 60 ≈ 333.33 滴/分钟
        rate = InfusionCalculator.calculate_drip_rate(1000, 60, 20)
        self.assertAlmostEqual(rate, 333.33, places=2)
    
    def test_calculate_drip_rate_different_drop_factor(self):
        """测试不同滴系数的滴速计算"""
        # 500ml, 30分钟, 滴系数60（小儿）
        # 滴速 = (500 × 60) / 30 = 1000 滴/分钟
        rate = InfusionCalculator.calculate_drip_rate(500, 30, 60)
        self.assertEqual(rate, 1000)
    
    def test_calculate_infusion_time(self):
        """测试输液时间计算"""
        # 500ml, 速度 100ml/h
        # 时间 = 500 / 100 = 5小时
        time = InfusionCalculator.calculate_infusion_time(500, 100)
        self.assertEqual(time, 5)
    
    def test_calculate_infusion_time_zero_rate(self):
        """测试零速度输液时间计算"""
        with self.assertRaises(ValueError):
            InfusionCalculator.calculate_infusion_time(500, 0)
    
    def test_calculate_volume(self):
        """测试液体体积计算"""
        # 剂量 200mg, 浓度 50mg/ml
        # 体积 = 200 / 50 = 4ml
        volume = InfusionCalculator.calculate_volume(200, 50)
        self.assertEqual(volume, 4)
    
    def test_calculate_volume_zero_concentration(self):
        """测试零浓度体积计算"""
        with self.assertRaises(ValueError):
            InfusionCalculator.calculate_volume(200, 0)


class TestHalfLifeCalculator(unittest.TestCase):
    """测试药物半衰期计算器"""
    
    def test_calculate_remaining_dose(self):
        """测试剩余剂量计算"""
        # 初始 100mg, 半衰期 6小时, 经过 6小时
        # 剩余 = 100 × 0.5 = 50mg
        remaining = HalfLifeCalculator.calculate_remaining_dose(100, 6, 6)
        self.assertEqual(remaining, 50)
    
    def test_calculate_remaining_dose_multiple_half_lives(self):
        """测试多个半衰期后剩余剂量"""
        # 初始 100mg, 半衰期 6小时, 经过 12小时（2个半衰期）
        # 剩余 = 100 × 0.5² = 25mg
        remaining = HalfLifeCalculator.calculate_remaining_dose(100, 6, 12)
        self.assertEqual(remaining, 25)
    
    def test_calculate_remaining_dose_zero_time(self):
        """测试零时间剩余剂量"""
        remaining = HalfLifeCalculator.calculate_remaining_dose(100, 6, 0)
        self.assertEqual(remaining, 100)
    
    def test_calculate_time_to_eliminate(self):
        """测试消除时间计算"""
        # 初始 100mg, 半衰期 6小时, 目标 12.5mg
        # 时间 = 6 × log2(100/12.5) = 6 × 3 = 18小时
        time = HalfLifeCalculator.calculate_time_to_eliminate(100, 6, 12.5)
        self.assertAlmostEqual(time, 18, places=5)
    
    def test_calculate_time_to_eliminate_invalid_target(self):
        """测试无效目标剂量"""
        with self.assertRaises(ValueError):
            HalfLifeCalculator.calculate_time_to_eliminate(100, 6, 0)
        with self.assertRaises(ValueError):
            HalfLifeCalculator.calculate_time_to_eliminate(100, 6, -10)
    
    def test_estimate_steady_state_time(self):
        """测试稳态时间估算"""
        # 半衰期 6 小时
        # 稳态时间 = 6 × 5 = 30 小时
        time = HalfLifeCalculator.estimate_steady_state_time(6)
        self.assertEqual(time, 30)
    
    def test_calculate_dosing_interval(self):
        """测试给药间隔计算"""
        # 半衰期 6 小时, 峰谷比 0.5
        # 间隔 = 6 × log2(2) = 6 小时
        interval = HalfLifeCalculator.calculate_dosing_interval(6, 0.5)
        self.assertAlmostEqual(interval, 6, places=5)
    
    def test_calculate_dosing_interval_different_ratio(self):
        """测试不同峰谷比的给药间隔"""
        # 半衰期 6 小时, 峰谷比 0.25
        # 间隔 = 6 × log2(4) = 12 小时
        interval = HalfLifeCalculator.calculate_dosing_interval(6, 0.25)
        self.assertAlmostEqual(interval, 12, places=5)


class TestDoseConverter(unittest.TestCase):
    """测试剂量单位转换器"""
    
    def test_mg_to_g(self):
        """测试毫克转克"""
        self.assertEqual(DoseConverter.mg_to_g(1000), 1)
        self.assertEqual(DoseConverter.mg_to_g(500), 0.5)
    
    def test_g_to_mg(self):
        """测试克转毫克"""
        self.assertEqual(DoseConverter.g_to_mg(1), 1000)
        self.assertEqual(DoseConverter.g_to_mg(0.5), 500)
    
    def test_mg_to_mcg(self):
        """测试毫克转微克"""
        self.assertEqual(DoseConverter.mg_to_mcg(1), 1000)
        self.assertEqual(DoseConverter.mg_to_mcg(0.5), 500)
    
    def test_mcg_to_mg(self):
        """测试微克转毫克"""
        self.assertEqual(DoseConverter.mcg_to_mg(1000), 1)
        self.assertEqual(DoseConverter.mcg_to_mg(500), 0.5)
    
    def test_kg_to_lb(self):
        """测试公斤转磅"""
        self.assertAlmostEqual(DoseConverter.kg_to_lb(1), 2.20462, places=5)
        self.assertAlmostEqual(DoseConverter.kg_to_lb(70), 154.3234, places=4)
    
    def test_lb_to_kg(self):
        """测试磅转公斤"""
        self.assertAlmostEqual(DoseConverter.lb_to_kg(1), 0.453592, places=5)
        self.assertAlmostEqual(DoseConverter.lb_to_kg(154), 69.853168, places=5)
    
    def test_convert_dose_same_unit(self):
        """测试相同单位转换"""
        self.assertEqual(DoseConverter.convert_dose(100, DoseUnit.MG, DoseUnit.MG), 100)
    
    def test_convert_dose_different_units(self):
        """测试不同单位转换"""
        self.assertEqual(
            DoseConverter.convert_dose(1, DoseUnit.G, DoseUnit.MG),
            1000
        )
        self.assertEqual(
            DoseConverter.convert_dose(1000, DoseUnit.MG, DoseUnit.G),
            1
        )
        self.assertEqual(
            DoseConverter.convert_dose(1, DoseUnit.MG, DoseUnit.MCG),
            1000
        )
    
    def test_convert_dose_invalid_units(self):
        """测试无效单位转换"""
        with self.assertRaises(ValueError):
            DoseConverter.convert_dose(100, DoseUnit.MG, DoseUnit.ML)


class TestRenalDoseAdjuster(unittest.TestCase):
    """测试肾功能剂量调整器"""
    
    def test_calculate_creatinine_clearance_male(self):
        """测试男性肌酐清除率计算"""
        # 男性, 50岁, 70kg, 肌酐 1.0 mg/dL
        # Ccr = ((140-50) × 70) / (72 × 1.0) = 87.5 mL/min
        ccr = RenalDoseAdjuster.calculate_creatinine_clearance(50, 70, 1.0, False)
        self.assertAlmostEqual(ccr, 87.5, places=1)
    
    def test_calculate_creatinine_clearance_female(self):
        """测试女性肌酐清除率计算"""
        # 女性, 50岁, 60kg, 肌酐 1.0 mg/dL
        # Ccr = ((140-50) × 60) / (72 × 1.0) × 0.85 = 63.75 mL/min
        ccr = RenalDoseAdjuster.calculate_creatinine_clearance(50, 60, 1.0, True)
        self.assertAlmostEqual(ccr, 63.75, places=1)
    
    def test_adjust_dose_for_renal_normal(self):
        """测试正常肾功能剂量调整"""
        dose, msg = RenalDoseAdjuster.adjust_dose_for_renal(100, 95)
        self.assertEqual(dose, 100)
        self.assertIn("正常", msg)
    
    def test_adjust_dose_for_renal_mild(self):
        """测试轻度肾功能不全剂量调整"""
        dose, msg = RenalDoseAdjuster.adjust_dose_for_renal(100, 70)
        self.assertEqual(dose, 90)
        self.assertIn("轻度", msg)
    
    def test_adjust_dose_for_renal_moderate(self):
        """测试中度肾功能不全剂量调整"""
        dose, msg = RenalDoseAdjuster.adjust_dose_for_renal(100, 45)
        self.assertEqual(dose, 75)
        self.assertIn("中度", msg)
    
    def test_adjust_dose_for_renal_severe(self):
        """测试重度肾功能不全剂量调整"""
        dose, msg = RenalDoseAdjuster.adjust_dose_for_renal(100, 25)
        self.assertEqual(dose, 50)
        self.assertIn("重度", msg)
    
    def test_adjust_dose_for_renal_esrd(self):
        """测试终末期肾病剂量调整"""
        dose, msg = RenalDoseAdjuster.adjust_dose_for_renal(100, 10)
        self.assertEqual(dose, 25)
        self.assertIn("终末期", msg)


class TestDrugInteractionChecker(unittest.TestCase):
    """测试药物相互作用检查器"""
    
    def test_check_known_interaction(self):
        """测试已知药物相互作用"""
        interaction = DrugInteractionChecker.check_interaction("warfarin", "aspirin")
        self.assertIsNotNone(interaction)
        self.assertEqual(interaction["severity"], "high")
        self.assertIn("出血", interaction["description"])
    
    def test_check_interaction_reverse_order(self):
        """测试反向顺序药物相互作用"""
        interaction = DrugInteractionChecker.check_interaction("aspirin", "warfarin")
        self.assertIsNotNone(interaction)
        self.assertEqual(interaction["severity"], "high")
    
    def test_check_no_interaction(self):
        """测试无相互作用的药物"""
        interaction = DrugInteractionChecker.check_interaction("paracetamol", "vitamin_c")
        self.assertIsNone(interaction)
    
    def test_check_critical_interaction(self):
        """测试严重药物相互作用"""
        interaction = DrugInteractionChecker.check_interaction("ssri", "maoi")
        self.assertIsNotNone(interaction)
        self.assertEqual(interaction["severity"], "critical")
    
    def test_check_multiple_interactions(self):
        """测试多种药物相互作用"""
        drugs = ["warfarin", "aspirin", "vitamin_k"]
        interactions = DrugInteractionChecker.check_multiple_interactions(drugs)
        self.assertTrue(len(interactions) >= 2)
        
        drug_pairs = [(i["drug1"], i["drug2"]) for i in interactions]
        self.assertTrue(
            ("warfarin", "aspirin") in drug_pairs or ("aspirin", "warfarin") in drug_pairs
        )


class TestCommonMedications(unittest.TestCase):
    """测试常用药物数据库"""
    
    def test_get_paracetamol(self):
        """测试获取对乙酰氨基酚信息"""
        med = get_medication("paracetamol")
        self.assertIsNotNone(med)
        self.assertEqual(med.name, "Paracetamol (Acetaminophen)")
        self.assertEqual(med.standard_dose_per_kg, 10)
    
    def test_get_ibuprofen(self):
        """测试获取布洛芬信息"""
        med = get_medication("ibuprofen")
        self.assertIsNotNone(med)
        self.assertEqual(med.dose_unit, DoseUnit.MG)
    
    def test_get_unknown_medication(self):
        """测试获取未知药物"""
        med = get_medication("unknown_drug")
        self.assertIsNone(med)
    
    def test_get_medication_with_spaces(self):
        """测试带空格的药物名称"""
        med = get_medication("Paracetamol Acetaminophen")
        self.assertIsNone(med)  # 不应找到


class TestCalculateDoseFunction(unittest.TestCase):
    """测试便捷计算函数"""
    
    def test_calculate_dose_success(self):
        """测试成功计算剂量"""
        result = calculate_dose("paracetamol", 70)
        self.assertTrue(result["success"])
        self.assertEqual(result["calculated_dose"], 700)
        self.assertEqual(result["weight_kg"], 70)
    
    def test_calculate_dose_with_lb(self):
        """测试使用磅计算剂量"""
        result = calculate_dose("paracetamol", 154, WeightUnit.LB)
        self.assertTrue(result["success"])
        self.assertAlmostEqual(result["weight_kg"], 69.85, places=2)
        self.assertAlmostEqual(result["calculated_dose"], 698.5, places=1)
    
    def test_calculate_dose_unknown_medication(self):
        """测试未知药物计算"""
        result = calculate_dose("unknown", 70)
        self.assertFalse(result["success"])
        self.assertIn("error", result)
    
    def test_calculate_dose_child(self):
        """测试儿童剂量计算"""
        # 使用对乙酰氨基酚，20kg儿童
        result = calculate_dose("paracetamol", 20)
        self.assertTrue(result["success"])
        self.assertEqual(result["calculated_dose"], 200)  # 20kg × 10mg/kg


class TestEdgeCases(unittest.TestCase):
    """测试边界情况"""
    
    def test_zero_weight(self):
        """测试零体重"""
        med = COMMON_MEDICATIONS["paracetamol"]
        calculator = MedicationCalculator(med)
        dose = calculator.calculate_weight_based_dose(0)
        self.assertEqual(dose, 0)
    
    def test_very_small_weight(self):
        """测试极小体重"""
        med = COMMON_MEDICATIONS["paracetamol"]
        calculator = MedicationCalculator(med)
        dose = calculator.calculate_weight_based_dose(0.5)  # 新生儿
        self.assertEqual(dose, 5)  # 0.5kg × 10mg/kg
    
    def test_very_large_weight(self):
        """测试极大体重"""
        med = COMMON_MEDICATIONS["paracetamol"]
        calculator = MedicationCalculator(med)
        dose = calculator.calculate_weight_based_dose(200)
        self.assertEqual(dose, 2000)  # 200kg × 10mg/kg
    
    def test_boundary_dose_validation(self):
        """测试边界剂量验证"""
        med = MedicationInfo(
            name="Test",
            standard_dose_per_kg=10,
            dose_unit=DoseUnit.MG,
            dose_range=DoseRange(10, 20, DoseUnit.MG)
        )
        calculator = MedicationCalculator(med)
        
        # 使用1kg体重测试边界值
        # 刚好等于最小值: 10mg/1kg = 10mg/kg
        result = calculator.validate_dose(10, weight=1)
        self.assertTrue(result["is_valid"])
        
        # 刚好等于最大值: 20mg/1kg = 20mg/kg
        result = calculator.validate_dose(20, weight=1)
        self.assertTrue(result["is_valid"])
        
        # 刚好小于最小值: 9.99mg/1kg = 9.99mg/kg < 10mg/kg
        result = calculator.validate_dose(9.99, weight=1)
        self.assertFalse(result["is_valid"])


class TestInsulinDosing(unittest.TestCase):
    """测试胰岛素剂量计算"""
    
    def test_insulin_dose_calculation(self):
        """测试胰岛素剂量计算"""
        med = COMMON_MEDICATIONS["insulin_regular"]
        calculator = MedicationCalculator(med)
        
        # 70kg 成人
        dose = calculator.calculate_weight_based_dose(70)
        self.assertEqual(dose, 7)  # 70kg × 0.1 units/kg


class TestAmoxicillinDosing(unittest.TestCase):
    """测试阿莫西林剂量计算"""
    
    def test_amoxicillin_dose_calculation(self):
        """测试阿莫西林剂量计算"""
        med = COMMON_MEDICATIONS["amoxicillin"]
        calculator = MedicationCalculator(med)
        
        # 20kg 儿童
        dose = calculator.calculate_weight_based_dose(20)
        self.assertEqual(dose, 500)  # 20kg × 25mg/kg
        
        # 验证是否在安全范围内（需要提供体重）
        validation = calculator.validate_dose(dose, weight=20)
        self.assertTrue(validation["is_valid"])


if __name__ == "__main__":
    unittest.main(verbosity=2)