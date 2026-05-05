"""
Blood Type Utilities 测试模块

Author: AllToolkit
Version: 1.0.0
"""

import unittest
from mod import (
    BloodTypeUtils, BloodType, ABOType, RhFactor, BloodTypeInfo,
    parse_blood_type, can_donate, get_compatible_donors, 
    get_compatible_recipients, child_blood_types, get_blood_type_info
)


class TestBloodTypeParsing(unittest.TestCase):
    """血型解析测试"""
    
    def test_parse_valid_blood_types(self):
        """测试有效血型解析"""
        self.assertEqual(parse_blood_type("A+"), BloodType.A_POSITIVE)
        self.assertEqual(parse_blood_type("A-"), BloodType.A_NEGATIVE)
        self.assertEqual(parse_blood_type("B+"), BloodType.B_POSITIVE)
        self.assertEqual(parse_blood_type("B-"), BloodType.B_NEGATIVE)
        self.assertEqual(parse_blood_type("AB+"), BloodType.AB_POSITIVE)
        self.assertEqual(parse_blood_type("AB-"), BloodType.AB_NEGATIVE)
        self.assertEqual(parse_blood_type("O+"), BloodType.O_POSITIVE)
        self.assertEqual(parse_blood_type("O-"), BloodType.O_NEGATIVE)
    
    def test_parse_case_insensitive(self):
        """测试大小写不敏感"""
        self.assertEqual(parse_blood_type("a+"), BloodType.A_POSITIVE)
        self.assertEqual(parse_blood_type("Ab-"), BloodType.AB_NEGATIVE)
        self.assertEqual(parse_blood_type("O+"), BloodType.O_POSITIVE)
        self.assertEqual(parse_blood_type(" o- "), BloodType.O_NEGATIVE)
    
    def test_parse_full_names(self):
        """测试全名解析"""
        self.assertEqual(parse_blood_type("A POSITIVE"), BloodType.A_POSITIVE)
        self.assertEqual(parse_blood_type("O NEGATIVE"), BloodType.O_NEGATIVE)
    
    def test_parse_invalid_blood_types(self):
        """测试无效血型解析"""
        self.assertIsNone(parse_blood_type("X+"))
        self.assertIsNone(parse_blood_type("ABCD"))
        self.assertIsNone(parse_blood_type(""))
        self.assertIsNone(parse_blood_type("C+"))
    
    def test_get_abo_type(self):
        """测试获取ABO血型"""
        self.assertEqual(BloodTypeUtils.get_abo_type(BloodType.A_POSITIVE), ABOType.A)
        self.assertEqual(BloodTypeUtils.get_abo_type(BloodType.B_NEGATIVE), ABOType.B)
        self.assertEqual(BloodTypeUtils.get_abo_type(BloodType.AB_POSITIVE), ABOType.AB)
        self.assertEqual(BloodTypeUtils.get_abo_type(BloodType.O_NEGATIVE), ABOType.O)
    
    def test_get_rh_factor(self):
        """测试获取Rh因子"""
        self.assertEqual(BloodTypeUtils.get_rh_factor(BloodType.A_POSITIVE), RhFactor.POSITIVE)
        self.assertEqual(BloodTypeUtils.get_rh_factor(BloodType.A_NEGATIVE), RhFactor.NEGATIVE)
        self.assertEqual(BloodTypeUtils.get_rh_factor(BloodType.O_POSITIVE), RhFactor.POSITIVE)
        self.assertEqual(BloodTypeUtils.get_rh_factor(BloodType.O_NEGATIVE), RhFactor.NEGATIVE)


class TestBloodTypeCompatibility(unittest.TestCase):
    """血型兼容性测试"""
    
    def test_universal_donor(self):
        """测试万能献血者（O-）"""
        # O- 可以献血给所有血型
        for recipient in BloodType:
            self.assertTrue(can_donate(BloodType.O_NEGATIVE, recipient),
                          f"O- 应该可以献血给 {recipient.value}")
    
    def test_universal_recipient(self):
        """测试万能受血者（AB+）"""
        # AB+ 可以接受所有血型
        for donor in BloodType:
            self.assertTrue(can_donate(donor, BloodType.AB_POSITIVE),
                          f"AB+ 应该可以接受 {donor.value}")
    
    def test_o_negative_restriction(self):
        """测试O-受血者的限制"""
        # O- 只能接受O-
        donors = get_compatible_donors(BloodType.O_NEGATIVE)
        self.assertEqual(len(donors), 1)
        self.assertIn(BloodType.O_NEGATIVE, donors)
    
    def test_ab_positive_donor_restriction(self):
        """测试AB+献血者的限制"""
        # AB+ 只能献血给AB+
        recipients = get_compatible_recipients(BloodType.AB_POSITIVE)
        self.assertEqual(len(recipients), 1)
        self.assertIn(BloodType.AB_POSITIVE, recipients)
    
    def test_a_positive_compatibility(self):
        """测试A+血型兼容性"""
        # A+ 可以献血给
        recipients = get_compatible_recipients(BloodType.A_POSITIVE)
        self.assertIn(BloodType.A_POSITIVE, recipients)
        self.assertIn(BloodType.AB_POSITIVE, recipients)
        
        # A+ 可以接受
        donors = get_compatible_donors(BloodType.A_POSITIVE)
        self.assertIn(BloodType.A_POSITIVE, donors)
        self.assertIn(BloodType.A_NEGATIVE, donors)
        self.assertIn(BloodType.O_POSITIVE, donors)
        self.assertIn(BloodType.O_NEGATIVE, donors)
    
    def test_b_negative_compatibility(self):
        """测试B-血型兼容性"""
        # B- 可以献血给
        recipients = get_compatible_recipients(BloodType.B_NEGATIVE)
        self.assertIn(BloodType.B_POSITIVE, recipients)
        self.assertIn(BloodType.B_NEGATIVE, recipients)
        self.assertIn(BloodType.AB_POSITIVE, recipients)
        self.assertIn(BloodType.AB_NEGATIVE, recipients)
        
        # B- 只能接受O-和B-
        donors = get_compatible_donors(BloodType.B_NEGATIVE)
        self.assertIn(BloodType.B_NEGATIVE, donors)
        self.assertIn(BloodType.O_NEGATIVE, donors)
        self.assertNotIn(BloodType.B_POSITIVE, donors)
        self.assertNotIn(BloodType.O_POSITIVE, donors)
    
    def test_rh_negative_donor_rule(self):
        """测试Rh阴性献血规则"""
        # Rh阴性不能给Rh阳性献血（除非ABO兼容）
        # 但实际上是：Rh阴性可以给Rh阳性献血
        # Rh阳性不能给Rh阴性献血
        self.assertTrue(can_donate(BloodType.A_NEGATIVE, BloodType.A_POSITIVE))
        self.assertFalse(can_donate(BloodType.A_POSITIVE, BloodType.A_NEGATIVE))
    
    def test_is_universal_donor(self):
        """测试万能献血者判断"""
        self.assertTrue(BloodTypeUtils.is_universal_donor(BloodType.O_NEGATIVE))
        self.assertFalse(BloodTypeUtils.is_universal_donor(BloodType.O_POSITIVE))
        self.assertFalse(BloodTypeUtils.is_universal_donor(BloodType.AB_NEGATIVE))
    
    def test_is_universal_recipient(self):
        """测试万能受血者判断"""
        self.assertTrue(BloodTypeUtils.is_universal_recipient(BloodType.AB_POSITIVE))
        self.assertFalse(BloodTypeUtils.is_universal_recipient(BloodType.AB_NEGATIVE))
        self.assertFalse(BloodTypeUtils.is_universal_recipient(BloodType.O_POSITIVE))


class TestBloodTypeInheritance(unittest.TestCase):
    """血型遗传测试"""
    
    def test_o_plus_o_equals_o(self):
        """测试 O + O = O"""
        children = child_blood_types(BloodType.O_POSITIVE, BloodType.O_POSITIVE)
        # 只能产生O型
        for bt in children:
            self.assertIn(BloodTypeUtils.get_abo_type(bt), [ABOType.O])
    
    def test_ab_plus_o(self):
        """测试 AB + O 组合"""
        children = child_blood_types(BloodType.AB_POSITIVE, BloodType.O_POSITIVE)
        # 只能产生A型或B型
        for bt in children:
            abo = BloodTypeUtils.get_abo_type(bt)
            self.assertIn(abo, [ABOType.A, ABOType.B])
    
    def test_a_plus_a(self):
        """测试 A + A 组合"""
        children = child_blood_types(BloodType.A_POSITIVE, BloodType.A_POSITIVE)
        # 可能产生A型或O型
        for bt in children:
            abo = BloodTypeUtils.get_abo_type(bt)
            self.assertIn(abo, [ABOType.A, ABOType.O])
    
    def test_ab_plus_ab(self):
        """测试 AB + AB 组合"""
        children = child_blood_types(BloodType.AB_POSITIVE, BloodType.AB_POSITIVE)
        # 可能产生A型、B型或AB型，不可能O型
        for bt in children:
            abo = BloodTypeUtils.get_abo_type(bt)
            self.assertIn(abo, [ABOType.A, ABOType.B, ABOType.AB])
    
    def test_a_plus_b(self):
        """测试 A + B 组合"""
        children = child_blood_types(BloodType.A_POSITIVE, BloodType.B_POSITIVE)
        # 可能产生所有ABO血型
        abo_types = set(BloodTypeUtils.get_abo_type(bt) for bt in children)
        # 应该包含多种血型
        self.assertGreater(len(abo_types), 1)
    
    def test_possible_blood_types_from_parents(self):
        """测试父母组合可能的血型"""
        possible = BloodTypeUtils.possible_blood_types_from_parents(
            BloodType.A_POSITIVE, BloodType.B_POSITIVE
        )
        self.assertIsInstance(possible, set)
        self.assertGreater(len(possible), 0)
    
    def test_can_be_parent(self):
        """测试父母判断"""
        # O型父母不能有AB型孩子
        self.assertFalse(BloodTypeUtils.can_be_parent(BloodType.O_POSITIVE, BloodType.AB_POSITIVE))
        # AB型父母不能有O型孩子
        self.assertFalse(BloodTypeUtils.can_be_parent(BloodType.AB_POSITIVE, BloodType.O_POSITIVE))
        # A型父母可以有O型孩子
        self.assertTrue(BloodTypeUtils.can_be_parent(BloodType.A_POSITIVE, BloodType.O_POSITIVE))
    
    def test_find_possible_parents(self):
        """测试查找可能的父母组合"""
        parents = BloodTypeUtils.find_possible_parents(BloodType.O_NEGATIVE)
        self.assertGreater(len(parents), 0)
        # 所有组合都应该是有效的
        for p1, p2 in parents:
            possible = BloodTypeUtils.possible_blood_types_from_parents(p1, p2)
            self.assertIn(BloodType.O_NEGATIVE, possible)


class TestBloodTypeDistribution(unittest.TestCase):
    """血型分布测试"""
    
    def test_global_distribution(self):
        """测试全球分布"""
        distribution = BloodTypeUtils.get_distribution_by_population("global")
        
        # 总和应该约为100%
        total = sum(distribution.values())
        self.assertAlmostEqual(total, 100.0, places=0)
        
        # O+ 应该是最常见的
        self.assertEqual(
            max(distribution, key=distribution.get),
            BloodType.O_POSITIVE
        )
    
    def test_china_distribution(self):
        """测试中国分布"""
        distribution = BloodTypeUtils.get_distribution_by_population("china")
        
        # 总和应该约为100%
        total = sum(distribution.values())
        self.assertAlmostEqual(total, 100.0, places=0)
    
    def test_usa_distribution(self):
        """测试美国分布"""
        distribution = BloodTypeUtils.get_distribution_by_population("usa")
        
        # 总和应该约为100%
        total = sum(distribution.values())
        self.assertAlmostEqual(total, 100.0, places=0)
    
    def test_get_population_percentage(self):
        """测试获取人群比例"""
        o_pos_global = BloodTypeUtils.get_population_percentage(BloodType.O_POSITIVE, "global")
        self.assertGreater(o_pos_global, 30)
        self.assertLess(o_pos_global, 50)
        
        ab_neg_global = BloodTypeUtils.get_population_percentage(BloodType.AB_NEGATIVE, "global")
        self.assertLess(ab_neg_global, 5)


class TestRareBloodType(unittest.TestCase):
    """稀有血型测试"""
    
    def test_is_rare_blood_type_global(self):
        """测试全球稀有血型"""
        # AB-是全球稀有血型
        self.assertTrue(BloodTypeUtils.is_rare_blood_type(BloodType.AB_NEGATIVE, "global"))
        # B-也是稀有
        self.assertTrue(BloodTypeUtils.is_rare_blood_type(BloodType.B_NEGATIVE, "global"))
        # O+不是稀有
        self.assertFalse(BloodTypeUtils.is_rare_blood_type(BloodType.O_POSITIVE, "global"))
    
    def test_is_rare_blood_type_china(self):
        """测试中国稀有血型"""
        # 在中国，所有Rh阴性都是稀有
        for bt in [BloodType.A_NEGATIVE, BloodType.B_NEGATIVE, 
                   BloodType.O_NEGATIVE, BloodType.AB_NEGATIVE]:
            self.assertTrue(BloodTypeUtils.is_rare_blood_type(bt, "china", threshold=1))
    
    def test_get_rare_blood_types(self):
        """测试获取稀有血型列表"""
        rare_global = BloodTypeUtils.get_rare_blood_types("global")
        self.assertIn(BloodType.AB_NEGATIVE, rare_global)
        
        rare_china = BloodTypeUtils.get_rare_blood_types("china", threshold=1)
        # 在中国，Rh阴性血型更稀少
        for bt in rare_china:
            rh = BloodTypeUtils.get_rh_factor(bt)
            self.assertEqual(rh, RhFactor.NEGATIVE)


class TestBloodTypeFormatting(unittest.TestCase):
    """血型格式化测试"""
    
    def test_short_format(self):
        """测试简短格式"""
        self.assertEqual(
            BloodTypeUtils.format_blood_type(BloodType.A_POSITIVE, "short"),
            "A+"
        )
        self.assertEqual(
            BloodTypeUtils.format_blood_type(BloodType.O_NEGATIVE, "short"),
            "O-"
        )
    
    def test_full_format(self):
        """测试完整格式"""
        self.assertEqual(
            BloodTypeUtils.format_blood_type(BloodType.A_POSITIVE, "full"),
            "A型阳性"
        )
        self.assertEqual(
            BloodTypeUtils.format_blood_type(BloodType.O_NEGATIVE, "full"),
            "O型阴性"
        )
        self.assertEqual(
            BloodTypeUtils.format_blood_type(BloodType.AB_POSITIVE, "full"),
            "AB型阳性"
        )
    
    def test_chinese_format(self):
        """测试中文格式"""
        self.assertEqual(
            BloodTypeUtils.format_blood_type(BloodType.B_POSITIVE, "chinese"),
            "B型血"
        )
    
    def test_invalid_format(self):
        """测试无效格式返回简短格式"""
        self.assertEqual(
            BloodTypeUtils.format_blood_type(BloodType.A_POSITIVE, "invalid"),
            "A+"
        )


class TestBloodTypeInfo(unittest.TestCase):
    """血型详细信息测试"""
    
    def test_get_blood_type_info(self):
        """测试获取血型信息"""
        info = get_blood_type_info("O-")
        
        self.assertIsInstance(info, BloodTypeInfo)
        self.assertEqual(info.blood_type, BloodType.O_NEGATIVE)
        self.assertEqual(info.abo_type, ABOType.O)
        self.assertEqual(info.rh_factor, RhFactor.NEGATIVE)
        self.assertTrue(info.is_universal_donor)
        self.assertFalse(info.is_universal_recipient)
    
    def test_ab_positive_info(self):
        """测试AB+血型信息"""
        info = BloodTypeUtils.get_blood_type_info(BloodType.AB_POSITIVE)
        
        self.assertFalse(info.is_universal_donor)
        self.assertTrue(info.is_universal_recipient)
        self.assertEqual(info.abo_type, ABOType.AB)
        self.assertEqual(info.rh_factor, RhFactor.POSITIVE)
    
    def test_antigens_and_antibodies(self):
        """测试抗原和抗体"""
        # O型有抗A和抗B抗体
        o_pos_info = BloodTypeUtils.get_blood_type_info(BloodType.O_POSITIVE)
        self.assertIn("Anti-A", o_pos_info.antibodies)
        self.assertIn("Anti-B", o_pos_info.antibodies)
        
        # AB型没有抗体
        ab_pos_info = BloodTypeUtils.get_blood_type_info(BloodType.AB_POSITIVE)
        self.assertEqual(len(ab_pos_info.antibodies), 0)
        
        # AB型有A和B抗原
        self.assertIn("A", ab_pos_info.antigens)
        self.assertIn("B", ab_pos_info.antigens)
    
    def test_possible_genotypes(self):
        """测试可能基因型"""
        a_info = BloodTypeUtils.get_blood_type_info(BloodType.A_POSITIVE)
        self.assertIn("AA", a_info.possible_genotypes)
        self.assertIn("AO", a_info.possible_genotypes)
        
        o_info = BloodTypeUtils.get_blood_type_info(BloodType.O_POSITIVE)
        self.assertEqual(o_info.possible_genotypes, ["OO"])
        
        ab_info = BloodTypeUtils.get_blood_type_info(BloodType.AB_POSITIVE)
        self.assertEqual(ab_info.possible_genotypes, ["AB"])


class TestUtilityFunctions(unittest.TestCase):
    """便捷函数测试"""
    
    def test_parse_blood_type_function(self):
        """测试便捷解析函数"""
        self.assertEqual(parse_blood_type("A+"), BloodType.A_POSITIVE)
        self.assertEqual(parse_blood_type("O-"), BloodType.O_NEGATIVE)
    
    def test_can_donate_function(self):
        """测试便捷献血函数"""
        self.assertTrue(can_donate("O-", "A+"))
        self.assertTrue(can_donate("A+", "AB+"))
        self.assertFalse(can_donate("A+", "O-"))
    
    def test_get_compatible_donors_function(self):
        """测试便捷获取献血者函数"""
        donors = get_compatible_donors("AB+")
        self.assertEqual(len(donors), 8)  # 所有血型
    
    def test_get_compatible_recipients_function(self):
        """测试便捷获取受血者函数"""
        recipients = get_compatible_recipients("O-")
        self.assertEqual(len(recipients), 8)  # 所有血型
    
    def test_child_blood_types_function(self):
        """测试便捷遗传计算函数"""
        children = child_blood_types("A+", "B+")
        self.assertIsInstance(children, dict)
        self.assertGreater(len(children), 0)
    
    def test_invalid_string_input(self):
        """测试无效字符串输入"""
        self.assertIsNone(parse_blood_type("invalid"))
        self.assertFalse(can_donate("X+", "Y-"))
        self.assertEqual(get_compatible_donors("invalid"), [])
        self.assertEqual(get_compatible_recipients("invalid"), [])
        self.assertEqual(child_blood_types("X+", "Y-"), {})
        self.assertIsNone(get_blood_type_info("invalid"))


class TestAllBloodTypes(unittest.TestCase):
    """所有血型完整性测试"""
    
    def test_all_blood_types_count(self):
        """测试血型数量"""
        all_types = BloodTypeUtils.get_all_blood_types()
        self.assertEqual(len(all_types), 8)
    
    def test_all_types_have_info(self):
        """测试所有血型都有信息"""
        for bt in BloodType:
            info = BloodTypeUtils.get_blood_type_info(bt)
            self.assertIsNotNone(info)
            self.assertEqual(info.blood_type, bt)
    
    def test_all_types_have_distribution(self):
        """测试所有血型都有分布数据"""
        for bt in BloodType:
            pct = BloodTypeUtils.get_population_percentage(bt, "global")
            self.assertGreater(pct, 0)
    
    def test_all_types_compatibility_complete(self):
        """测试所有血型兼容性完整"""
        for donor in BloodType:
            recipients = BloodTypeUtils.get_compatible_recipients(donor)
            self.assertGreater(len(recipients), 0)
            
            for recipient in recipients:
                self.assertTrue(can_donate(donor, recipient))


if __name__ == "__main__":
    unittest.main()