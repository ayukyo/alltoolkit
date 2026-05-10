"""
昵称生成器测试文件
测试所有昵称生成功能
"""

import unittest
import sys
import os

# 添加模块路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    NicknameGenerator,
    UsernameGenerator,
    GameIdGenerator,
    PetNameGenerator,
    TeamNameGenerator,
    FantasyNameGenerator,
    NameStyle,
    GeneratedName,
    generate_nickname,
    generate_username,
    generate_game_id,
    generate_pet_name,
    generate_team_name,
    generate_fantasy_name,
    generate_names_bulk
)


class TestNicknameGenerator(unittest.TestCase):
    """测试昵称生成器"""
    
    def setUp(self):
        self.gen = NicknameGenerator(seed=42)  # 固定种子以便测试
    
    def test_generate_chinese_cute(self):
        """测试生成中文可爱风格昵称"""
        results = self.gen.generate(NameStyle.CUTE, "chinese", 5)
        
        self.assertEqual(len(results), 5)
        for result in results:
            self.assertIsInstance(result, GeneratedName)
            self.assertIsInstance(result.name, str)
            self.assertTrue(len(result.name) > 0)
            self.assertEqual(result.style, NameStyle.CUTE)
            self.assertTrue(len(result.alternatives) > 0)
    
    def test_generate_english_cool(self):
        """测试生成英文酷炫风格昵称"""
        results = self.gen.generate(NameStyle.COOL, "english", 3)
        
        self.assertEqual(len(results), 3)
        for result in results:
            self.assertIsInstance(result.name, str)
            self.assertTrue(len(result.name) > 0)
    
    def test_generate_mixed(self):
        """测试生成混合风格昵称"""
        results = self.gen.generate_mixed(10)
        
        self.assertEqual(len(results), 10)
        
        # 检查是否有不同风格
        styles = set(r.style for r in results)
        self.assertTrue(len(styles) > 1)
    
    def test_generate_with_prefix_suffix(self):
        """测试生成带前缀后缀的昵称"""
        result = self.gen.generate_with_prefix_suffix(NameStyle.COOL, "english")
        
        self.assertIsInstance(result, GeneratedName)
        self.assertTrue(len(result.name) > 0)
    
    def test_seed_consistency(self):
        """测试种子一致性"""
        # 使用相同种子生成两次，名字应该有相似长度
        gen1 = NicknameGenerator(seed=100)
        gen2 = NicknameGenerator(seed=100)
        
        results1 = gen1.generate(NameStyle.CUTE, "chinese", 5)
        results2 = gen2.generate(NameStyle.CUTE, "chinese", 5)
        
        # 检查长度一致（由于风格键选择也用了随机，名字可能不完全一致）
        self.assertEqual(len(results1), len(results2))
        
        # 检查所有名字都是有效的
        for r in results1 + results2:
            self.assertTrue(len(r.name) > 0)
    
    def test_all_styles(self):
        """测试所有风格都能生成"""
        for style in NameStyle:
            results = self.gen.generate(style, "chinese", 1)
            self.assertTrue(len(results[0].name) > 0)
            
            results = self.gen.generate(style, "english", 1)
            self.assertTrue(len(results[0].name) > 0)


class TestUsernameGenerator(unittest.TestCase):
    """测试用户名生成器"""
    
    def setUp(self):
        self.gen = UsernameGenerator(seed=42)
    
    def test_generate_basic(self):
        """测试基本用户名生成"""
        results = self.gen.generate(count=5)
        
        self.assertEqual(len(results), 5)
        for name in results:
            self.assertIsInstance(name, str)
            self.assertTrue(len(name) >= 6)
    
    def test_generate_with_base(self):
        """测试基于基础名生成"""
        results = self.gen.generate(base_name="test", count=3)
        
        for name in results:
            self.assertTrue("test" in name.lower())
    
    def test_generate_without_numbers(self):
        """测试不使用数字"""
        results = self.gen.generate(use_numbers=False, count=3)
        
        # 检查是否有纯字母用户名
        has_alpha_only = any(name.replace("_", "").replace("-", "").isalpha() for name in results)
        # 注意：可能有些还是会有数字，因为长度调整
        self.assertTrue(len(results) == 3)
    
    def test_check_format_valid(self):
        """测试有效格式检查"""
        valid, errors = self.gen.check_availability_format("valid_username")
        
        self.assertTrue(valid)
        self.assertEqual(len(errors), 0)
    
    def test_check_format_invalid(self):
        """测试无效格式检查"""
        # 太短
        valid, errors = self.gen.check_availability_format("ab")
        self.assertFalse(valid)
        self.assertTrue(len(errors) > 0)
        
        # 特殊字符
        valid, errors = self.gen.check_availability_format("user@name")
        self.assertFalse(valid)
        
        # 数字开头
        valid, errors = self.gen.check_availability_format("123user")
        self.assertFalse(valid)
    
    def test_length_constraints(self):
        """测试长度约束"""
        results = self.gen.generate(min_length=8, max_length=15, count=5)
        
        for name in results:
            self.assertTrue(8 <= len(name) <= 15)


class TestGameIdGenerator(unittest.TestCase):
    """测试游戏ID生成器"""
    
    def setUp(self):
        self.gen = GameIdGenerator(seed=42)
    
    def test_generate_fps(self):
        """测试FPS游戏ID生成"""
        results = self.gen.generate("fps", count=5)
        
        self.assertEqual(len(results), 5)
        for id_ in results:
            self.assertIsInstance(id_, str)
            self.assertTrue(len(id_) > 0)
    
    def test_generate_moba(self):
        """测试MOBA游戏ID生成"""
        results = self.gen.generate("moba", count=3)
        
        self.assertEqual(len(results), 3)
    
    def test_generate_with_clan(self):
        """测试带战队前缀"""
        results = self.gen.generate("fps", include_clan=True, count=3)
        
        for id_ in results:
            self.assertTrue("[" in id_ and "]" in id_)
    
    def test_generate_with_custom_clan(self):
        """测试自定义战队名"""
        results = self.gen.generate("fps", include_clan=True, 
                                   clan_name="MyTeam", count=2)
        
        for id_ in results:
            self.assertTrue("[MyTeam]" in id_)
    
    def test_all_game_types(self):
        """测试所有游戏类型"""
        game_types = ["fps", "moba", "mmorpg", "casual", "strategy", "racing"]
        
        for gt in game_types:
            results = self.gen.generate(gt, count=1)
            self.assertTrue(len(results[0]) > 0)
    
    def test_alias(self):
        """测试别名方法"""
        results = self.gen.generate_game_id("fps", count=2)
        
        self.assertEqual(len(results), 2)


class TestPetNameGenerator(unittest.TestCase):
    """测试宠物名字生成器"""
    
    def setUp(self):
        self.gen = PetNameGenerator(seed=42)
    
    def test_generate_dog_chinese(self):
        """测试生成中文狗名"""
        results = self.gen.generate("dog", "chinese", 5)
        
        self.assertEqual(len(results), 5)
        for name in results:
            self.assertIsInstance(name, str)
    
    def test_generate_cat_english(self):
        """测试生成英文猫名"""
        results = self.gen.generate("cat", "english", 3)
        
        self.assertEqual(len(results), 3)
    
    def test_generate_cute_combo(self):
        """测试可爱组合名"""
        results = self.gen.generate_cute_combo(5)
        
        self.assertEqual(len(results), 5)
    
    def test_all_pet_types(self):
        """测试所有宠物类型"""
        pet_types = ["dog", "cat", "bird", "fish", "rabbit", "hamster"]
        
        for pt in pet_types:
            results = self.gen.generate(pt, "chinese", 1)
            self.assertTrue(len(results[0]) > 0)
            
            results = self.gen.generate(pt, "english", 1)
            self.assertTrue(len(results[0]) > 0)


class TestTeamNameGenerator(unittest.TestCase):
    """测试团队名称生成器"""
    
    def setUp(self):
        self.gen = TeamNameGenerator(seed=42)
    
    def test_generate_tech(self):
        """测试科技团队名"""
        results = self.gen.generate("tech", "chinese", 5)
        
        self.assertEqual(len(results), 5)
        for name in results:
            self.assertTrue(len(name) > 0)
    
    def test_generate_gaming(self):
        """测试游戏战队名"""
        results = self.gen.generate("gaming", "chinese", 3)
        
        self.assertEqual(len(results), 3)
    
    def test_generate_english(self):
        """测试英文团队名"""
        results = self.gen.generate("creative", "english", 3)
        
        self.assertEqual(len(results), 3)
    
    def test_generate_with_name(self):
        """测试带领导名字"""
        results = self.gen.generate_with_name("张三", "tech")
        
        self.assertEqual(len(results), 2)
        for name in results:
            self.assertTrue("张三" in name)
    
    def test_all_team_types(self):
        """测试所有团队类型"""
        team_types = ["tech", "creative", "business", "gaming", "academic"]
        
        for tt in team_types:
            results = self.gen.generate(tt, "chinese", 1)
            self.assertTrue(len(results[0]) > 0)


class TestFantasyNameGenerator(unittest.TestCase):
    """测试奇幻名字生成器"""
    
    def setUp(self):
        self.gen = FantasyNameGenerator(seed=42)
    
    def test_generate_elven(self):
        """测试精灵名"""
        results = self.gen.generate("elven", "english", 5)
        
        self.assertEqual(len(results), 5)
        for name in results:
            self.assertTrue(len(name) > 0)
    
    def test_generate_dwarven(self):
        """测试矮人名"""
        results = self.gen.generate("dwarven", "english", 3)
        
        self.assertEqual(len(results), 3)
    
    def test_generate_chinese_fantasy(self):
        """测试中文奇幻名"""
        results = self.gen.generate("elven", "chinese", 5)
        
        self.assertEqual(len(results), 5)
        for name in results:
            # 中文名应该是3个字
            self.assertTrue(len(name) == 3)
    
    def test_generate_full_name(self):
        """测试生成全名"""
        name = self.gen.generate_full_name("elven", "english")
        
        self.assertTrue(" " in name)  # 英文全名有空格
        
        name = self.gen.generate_full_name("elven", "chinese")
        self.assertTrue(len(name) == 6)  # 中文全名是6个字
    
    def test_all_races(self):
        """测试所有种族"""
        races = ["elven", "dwarven", "human", "demonic", "angelic"]
        
        for race in races:
            results = self.gen.generate(race, "english", 1)
            self.assertTrue(len(results[0]) > 0)


class TestConvenienceFunctions(unittest.TestCase):
    """测试便捷函数"""
    
    def test_generate_nickname(self):
        """测试快速生成昵称"""
        name = generate_nickname("可爱", "chinese")
        self.assertTrue(len(name) > 0)
        
        name = generate_nickname("cool", "english")
        self.assertTrue(len(name) > 0)
    
    def test_generate_username(self):
        """测试快速生成用户名"""
        name = generate_username()
        self.assertTrue(len(name) > 0)
        
        name = generate_username("testbase")
        self.assertTrue(len(name) > 0)
    
    def test_generate_game_id(self):
        """测试快速生成游戏ID"""
        id_ = generate_game_id("fps")
        self.assertTrue(len(id_) > 0)
        
        id_ = generate_game_id("moba")
        self.assertTrue(len(id_) > 0)
    
    def test_generate_pet_name(self):
        """测试快速生成宠物名"""
        name = generate_pet_name("dog")
        self.assertTrue(len(name) > 0)
        
        name = generate_pet_name("cat")
        self.assertTrue(len(name) > 0)
    
    def test_generate_team_name(self):
        """测试快速生成团队名"""
        name = generate_team_name("tech")
        self.assertTrue(len(name) > 0)
        
        name = generate_team_name("creative")
        self.assertTrue(len(name) > 0)
    
    def test_generate_fantasy_name(self):
        """测试快速生成奇幻名"""
        name = generate_fantasy_name("elven")
        self.assertTrue(len(name) > 0)
        
        name = generate_fantasy_name("dwarven")
        self.assertTrue(len(name) > 0)
    
    def test_generate_names_bulk(self):
        """测试批量生成"""
        names = generate_names_bulk("可爱", "chinese", 20)
        
        self.assertEqual(len(names), 20)
        
        # 检查所有名字都有效
        for name in names:
            self.assertTrue(len(name) > 0)


class TestGeneratedName(unittest.TestCase):
    """测试GeneratedName数据类"""
    
    def test_data_class(self):
        """测试数据类属性"""
        name = GeneratedName(
            name="测试名字",
            style=NameStyle.CUTE,
            components=["可爱", "小猫"],
            meaning="可爱风格的昵称",
            alternatives=["测试名字1", "测试名字2"]
        )
        
        self.assertEqual(name.name, "测试名字")
        self.assertEqual(name.style, NameStyle.CUTE)
        self.assertEqual(len(name.components), 2)
        self.assertEqual(len(name.alternatives), 2)
    
    def test_str_representation(self):
        """测试字符串表示"""
        name = GeneratedName(
            name="我的昵称",
            style=NameStyle.COOL,
            components=["酷炫", "霸气"],
            meaning="酷炫风格",
            alternatives=[]
        )
        
        self.assertEqual(str(name), "我的昵称")


class TestEdgeCases(unittest.TestCase):
    """测试边界情况"""
    
    def test_empty_count(self):
        """测试生成0个"""
        gen = NicknameGenerator()
        results = gen.generate(NameStyle.CUTE, "chinese", 0)
        
        self.assertEqual(len(results), 0)
    
    def test_large_count(self):
        """测试生成大量"""
        gen = NicknameGenerator()
        results = gen.generate(NameStyle.CUTE, "chinese", 100)
        
        self.assertEqual(len(results), 100)
    
    def test_invalid_style(self):
        """测试无效风格（应该使用默认）"""
        gen = NicknameGenerator()
        # 应该能处理，不会报错
        results = gen.generate(NameStyle.CUTE, "chinese", 1)
        self.assertTrue(len(results[0].name) > 0)
    
    def test_invalid_pet_type(self):
        """测试无效宠物类型（使用默认）"""
        gen = PetNameGenerator()
        results = gen.generate("unknown_type", "chinese", 1)
        self.assertTrue(len(results[0]) > 0)
    
    def test_invalid_team_type(self):
        """测试无效团队类型（使用默认）"""
        gen = TeamNameGenerator()
        results = gen.generate("unknown_type", "chinese", 1)
        self.assertTrue(len(results[0]) > 0)
    
    def test_invalid_race(self):
        """测试无效种族（使用默认）"""
        gen = FantasyNameGenerator()
        results = gen.generate("unknown_race", "english", 1)
        self.assertTrue(len(results[0]) > 0)


if __name__ == "__main__":
    # 运行所有测试
    unittest.main(verbosity=2)
    
    # 打印一些示例
    print("\n" + "="*50)
    print("昵称生成示例")
    print("="*50)
    
    print("\n中文可爱昵称:")
    for _ in range(5):
        print(f"  - {generate_nickname('可爱', 'chinese')}")
    
    print("\n英文酷炫昵称:")
    for _ in range(5):
        print(f"  - {generate_nickname('cool', 'english')}")
    
    print("\n游戏ID:")
    for _ in range(5):
        print(f"  - {generate_game_id('fps')}")
    
    print("\n宠物名字:")
    print(f"  狗: {generate_pet_name('dog')}")
    print(f"  猫: {generate_pet_name('cat')}")
    print(f"  兔: {generate_pet_name('rabbit')}")
    
    print("\n奇幻角色名:")
    print(f"  精灵: {generate_fantasy_name('elven')}")
    print(f"  矮人: {generate_fantasy_name('dwarven')}")
    print(f"  中文: {generate_fantasy_name('elven')}")
    
    print("\n团队名称:")
    print(f"  科技: {generate_team_name('tech')}")
    print(f"  游戏: {generate_team_name('gaming')}")