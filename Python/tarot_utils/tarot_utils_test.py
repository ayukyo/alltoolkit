#!/usr/bin/env python3
"""
塔罗牌工具模块测试
Tests for Tarot Card Utilities Module
"""

import unittest
import sys
import os

# 添加模块路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    TarotDeck, TarotReading, TarotCard, Orientation, CardType, Suit,
    MAJOR_ARCANA, MINOR_ARCANA, FULL_DECK,
    draw_single_card, draw_three_cards, draw_celtic_cross,
    ask_yes_no, get_card_info, list_all_cards, list_major_arcana,
    list_minor_arcana, list_cards_by_suit
)


class TestTarotDeck(unittest.TestCase):
    """测试塔罗牌牌组类"""
    
    def test_deck_size(self):
        """测试牌组大小为78张"""
        deck = TarotDeck()
        self.assertEqual(deck.remaining_count(), 78)
    
    def test_major_arcana_count(self):
        """测试大阿卡纳数量为22张"""
        self.assertEqual(len(MAJOR_ARCANA), 22)
    
    def test_minor_arcana_count(self):
        """测试小阿卡纳数量为56张"""
        self.assertEqual(len(MINOR_ARCANA), 56)
    
    def test_full_deck_count(self):
        """测试完整牌组为78张"""
        self.assertEqual(len(FULL_DECK), 78)
    
    def test_draw_card_reduces_deck(self):
        """测试抽牌后牌组减少"""
        deck = TarotDeck()
        initial_count = deck.remaining_count()
        deck.draw_card()
        self.assertEqual(deck.remaining_count(), initial_count - 1)
    
    def test_draw_multiple_cards(self):
        """测试抽取多张牌"""
        deck = TarotDeck()
        cards = deck.draw_cards(5)
        self.assertEqual(len(cards), 5)
        self.assertEqual(deck.remaining_count(), 73)
    
    def test_shuffle_resets_deck(self):
        """测试洗牌后重置牌组"""
        deck = TarotDeck()
        deck.draw_cards(10)
        self.assertEqual(deck.remaining_count(), 68)
        deck.shuffle()
        self.assertEqual(deck.remaining_count(), 78)
    
    def test_seed_reproducibility(self):
        """测试种子可重复性"""
        deck1 = TarotDeck(seed=42)
        card1, _ = deck1.draw_card()
        
        deck2 = TarotDeck(seed=42)
        card2, _ = deck2.draw_card()
        
        self.assertEqual(card1.id, card2.id)
    
    def test_orientation_distribution(self):
        """测试正逆位分布（多次抽取后应有两种情况）"""
        deck = TarotDeck()
        orientations = set()
        for _ in range(100):
            deck.shuffle()
            _, orientation = deck.draw_card(orientation_random=True)
            orientations.add(orientation)
        
        self.assertIn(Orientation.UPRIGHT, orientations)
        self.assertIn(Orientation.REVERSED, orientations)
    
    def test_drawn_cards_tracking(self):
        """测试已抽取牌追踪"""
        deck = TarotDeck()
        deck.draw_cards(3)
        self.assertEqual(len(deck.get_drawn_cards()), 3)


class TestTarotCard(unittest.TestCase):
    """测试塔罗牌数据类"""
    
    def test_major_arcana_structure(self):
        """测试大阿卡纳牌结构"""
        for card in MAJOR_ARCANA:
            self.assertIsInstance(card.id, int)
            self.assertIsInstance(card.name, str)
            self.assertIsInstance(card.english_name, str)
            self.assertEqual(card.card_type, CardType.MAJOR_ARCANA)
            self.assertIsNone(card.suit)
            self.assertIsNone(card.number)
            self.assertIsInstance(card.keywords_upright, list)
            self.assertIsInstance(card.keywords_reversed, list)
    
    def test_minor_arcana_structure(self):
        """测试小阿卡纳牌结构"""
        for card in MINOR_ARCANA:
            self.assertIsInstance(card.id, int)
            self.assertIsInstance(card.name, str)
            self.assertEqual(card.card_type, CardType.MINOR_ARCANA)
            self.assertIsNotNone(card.suit)
            self.assertIsInstance(card.number, int)
            self.assertGreaterEqual(card.number, 1)
            self.assertLessEqual(card.number, 14)
    
    def test_minor_arcana_suits(self):
        """测试小阿卡纳花色分布"""
        suits = {Suit.WANDS, Suit.CUPS, Suit.SWORDS, Suit.PENTACLES}
        found_suits = set()
        
        for card in MINOR_ARCANA:
            found_suits.add(card.suit)
        
        self.assertEqual(found_suits, suits)
    
    def test_minor_arcana_numbers(self):
        """测试小阿卡纳每个花色有14张牌"""
        suit_counts = {suit: 0 for suit in Suit}
        
        for card in MINOR_ARCANA:
            suit_counts[card.suit] += 1
        
        for suit, count in suit_counts.items():
            self.assertEqual(count, 14, f"{suit.value}应有14张牌，实际{count}张")
    
    def test_card_keywords_not_empty(self):
        """测试牌关键词不为空"""
        for card in FULL_DECK:
            self.assertGreater(len(card.keywords_upright), 0)
            self.assertGreater(len(card.keywords_reversed), 0)
    
    def test_card_meanings_not_empty(self):
        """测试牌含义不为空"""
        for card in FULL_DECK:
            self.assertGreater(len(card.meaning_upright), 0)
            self.assertGreater(len(card.meaning_reversed), 0)
    
    def test_fool_card(self):
        """测试愚者牌数据"""
        fool = MAJOR_ARCANA[0]
        self.assertEqual(fool.id, 0)
        self.assertEqual(fool.name, "愚者")
        self.assertEqual(fool.english_name, "The Fool")
        self.assertEqual(fool.element, "风")
    
    def test_world_card(self):
        """测试世界牌数据"""
        world = MAJOR_ARCANA[-1]
        self.assertEqual(world.id, 21)
        self.assertEqual(world.name, "世界")
        self.assertEqual(world.english_name, "The World")


class TestTarotReading(unittest.TestCase):
    """测试塔罗牌解读类"""
    
    def test_single_card_reading(self):
        """测试单牌解读"""
        reading = TarotReading(TarotDeck(seed=42))
        result = reading.single_card_reading("测试问题")
        
        self.assertEqual(result["spread_type"], "单牌牌阵")
        self.assertEqual(result["question"], "测试问题")
        self.assertEqual(len(result["cards"]), 1)
        self.assertIn("interpretation", result)
    
    def test_three_card_reading(self):
        """测试三牌牌阵解读"""
        reading = TarotReading(TarotDeck(seed=42))
        result = reading.three_card_reading("测试问题")
        
        self.assertEqual(result["spread_type"], "三牌牌阵")
        self.assertEqual(len(result["cards"]), 3)
        self.assertEqual(result["positions"], ["过去", "现在", "未来"])
        self.assertIn("interpretation", result)
    
    def test_three_card_custom_positions(self):
        """测试自定义三牌牌阵位置"""
        reading = TarotReading(TarotDeck(seed=42))
        result = reading.three_card_reading(
            positions=("情境", "行动", "结果")
        )
        
        self.assertEqual(result["positions"], ["情境", "行动", "结果"])
    
    def test_celtic_cross_reading(self):
        """测试凯尔特十字牌阵解读"""
        reading = TarotReading(TarotDeck(seed=42))
        result = reading.celtic_cross_reading("测试问题")
        
        self.assertEqual(result["spread_type"], "凯尔特十字牌阵")
        self.assertEqual(len(result["cards"]), 10)
        self.assertIn("interpretation", result)
        
        # 验证位置名称
        positions = [card["position"] for card in result["cards"]]
        self.assertEqual(positions[0], "现状")
        self.assertEqual(positions[-1], "最终结果")
    
    def test_yes_no_reading(self):
        """测试是非问题解读"""
        reading = TarotReading(TarotDeck(seed=42))
        result = reading.yes_no_reading("我应该接受这份工作吗？")
        
        self.assertEqual(result["spread_type"], "是非牌阵")
        self.assertIn(result["answer"], ["是的", "不是", "不确定"])
        self.assertIn(result["confidence"], ["高", "中", "低"])
        self.assertIn("card", result)
        self.assertIn("interpretation", result)


class TestConvenienceFunctions(unittest.TestCase):
    """测试便捷函数"""
    
    def test_draw_single_card(self):
        """测试单牌抽取函数"""
        result = draw_single_card("测试问题", seed=42)
        
        self.assertIn("spread_type", result)
        self.assertEqual(len(result["cards"]), 1)
    
    def test_draw_three_cards(self):
        """测试三牌抽取函数"""
        result = draw_three_cards(seed=42)
        
        self.assertEqual(len(result["cards"]), 3)
    
    def test_draw_celtic_cross(self):
        """测试凯尔特十字抽取函数"""
        result = draw_celtic_cross(seed=42)
        
        self.assertEqual(len(result["cards"]), 10)
    
    def test_ask_yes_no(self):
        """测试是非问题函数"""
        result = ask_yes_no("这是一个好主意吗？", seed=42)
        
        self.assertIn("answer", result)
        self.assertIn("confidence", result)
    
    def test_get_card_info(self):
        """测试获取牌信息"""
        # 测试中文名
        info = get_card_info("愚者")
        self.assertIsNotNone(info)
        self.assertEqual(info["name"], "愚者")
        
        # 测试英文名
        info = get_card_info("The Fool")
        self.assertIsNotNone(info)
        self.assertEqual(info["english_name"], "The Fool")
        
        # 测试小阿卡纳
        info = get_card_info("权杖A")
        self.assertIsNotNone(info)
        self.assertEqual(info["suit"], "权杖")
        
        # 测试不存在的牌
        info = get_card_info("不存在的牌")
        self.assertIsNone(info)
    
    def test_list_all_cards(self):
        """测试列出所有牌"""
        cards = list_all_cards()
        self.assertEqual(len(cards), 78)
        self.assertIn("愚者", cards)
        self.assertIn("世界", cards)
    
    def test_list_major_arcana(self):
        """测试列出大阿卡纳"""
        cards = list_major_arcana()
        self.assertEqual(len(cards), 22)
    
    def test_list_minor_arcana(self):
        """测试列出小阿卡纳"""
        cards = list_minor_arcana()
        self.assertEqual(len(cards), 56)
    
    def test_list_cards_by_suit(self):
        """测试按花色列出牌"""
        for suit in Suit:
            cards = list_cards_by_suit(suit)
            self.assertEqual(len(cards), 14)
            
            # 验证所有牌都属于该花色
            for card_name in cards:
                self.assertIn(suit.value, card_name)


class TestCardMeanings(unittest.TestCase):
    """测试牌义完整性"""
    
    def test_all_cards_have_elements(self):
        """测试所有牌都有元素"""
        # 大阿卡纳有元素
        for card in MAJOR_ARCANA:
            self.assertIsNotNone(card.element, f"{card.name}缺少元素")
        
        # 小阿卡纳也有元素
        for card in MINOR_ARCANA:
            self.assertIsNotNone(card.element)
    
    def test_major_arcana_have_zodiac_or_planet(self):
        """测试大阿卡纳有星座或行星对应"""
        for card in MAJOR_ARCANA:
            has_correspondence = card.zodiac is not None or card.planet is not None
            self.assertTrue(has_correspondence, f"{card.name}缺少星座或行星对应")


class TestOrientation(unittest.TestCase):
    """测试牌的朝向"""
    
    def test_orientation_values(self):
        """测试朝向枚举值"""
        self.assertEqual(Orientation.UPRIGHT.value, "正位")
        self.assertEqual(Orientation.REVERSED.value, "逆位")
    
    def test_card_orientation_in_reading(self):
        """测试解读中的牌朝向"""
        reading = TarotReading(TarotDeck(seed=123))
        result = reading.single_card_reading()
        
        orientation = result["cards"][0]["orientation"]
        self.assertIn(orientation, ["正位", "逆位"])


def run_tests():
    """运行所有测试"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    suite.addTests(loader.loadTestsFromTestCase(TestTarotDeck))
    suite.addTests(loader.loadTestsFromTestCase(TestTarotCard))
    suite.addTests(loader.loadTestsFromTestCase(TestTarotReading))
    suite.addTests(loader.loadTestsFromTestCase(TestConvenienceFunctions))
    suite.addTests(loader.loadTestsFromTestCase(TestCardMeanings))
    suite.addTests(loader.loadTestsFromTestCase(TestOrientation))
    
    runner = unittest.TextTestRunner(verbosity=2)
    return runner.run(suite)


if __name__ == "__main__":
    result = run_tests()
    sys.exit(0 if result.wasSuccessful() else 1)