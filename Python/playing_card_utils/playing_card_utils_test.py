"""
Playing Card Utilities 测试

Author: AllToolkit
"""

import unittest
from mod import (
    Suit, Rank, Card, Deck, HandRank, HandResult,
    HandEvaluator, Blackjack, CardGame,
    create_deck, shuffle_deck, deal_hand,
    evaluate_poker_hand, compare_hands, get_best_poker_hand
)


class TestCard(unittest.TestCase):
    """测试 Card 类"""
    
    def test_card_creation(self):
        """测试创建牌"""
        card = Card(Suit.SPADES, Rank.ACE)
        self.assertEqual(card.suit, Suit.SPADES)
        self.assertEqual(card.rank, Rank.ACE)
        self.assertEqual(str(card), "♠A")
    
    def test_card_comparison(self):
        """测试牌的大小比较"""
        ace = Card(Suit.SPADES, Rank.ACE)
        king = Card(Suit.HEARTS, Rank.KING)
        two = Card(Suit.CLUBS, Rank.TWO)
        
        self.assertTrue(ace > king)
        self.assertTrue(king > two)
        self.assertTrue(ace > two)
        
        # 同点数时按花色排序（用于排序，不代表游戏中的强度）
        # 枚举顺序: SPADES(0), HEARTS(1), DIAMONDS(2), CLUBS(3)
        ace_hearts = Card(Suit.HEARTS, Rank.ACE)
        ace_spades = Card(Suit.SPADES, Rank.ACE)
        # Spades 在枚举中排在前面，所以 (14, 0) < (14, 1)
        self.assertTrue(ace_spades < ace_hearts)
    
    def test_card_from_string(self):
        """测试从字符串创建牌"""
        card = Card.from_string("♠A")
        self.assertEqual(card.suit, Suit.SPADES)
        self.assertEqual(card.rank, Rank.ACE)
        
        card = Card.from_string("♥10")
        self.assertEqual(card.suit, Suit.HEARTS)
        self.assertEqual(card.rank, Rank.TEN)
        
        card = Card.from_string("♦K")
        self.assertEqual(card.suit, Suit.DIAMONDS)
        self.assertEqual(card.rank, Rank.KING)
    
    def test_card_properties(self):
        """测试牌的属性"""
        jack = Card(Suit.SPADES, Rank.JACK)
        self.assertTrue(jack.is_face_card)
        self.assertFalse(jack.is_ace)
        
        ace = Card(Suit.HEARTS, Rank.ACE)
        self.assertFalse(ace.is_face_card)
        self.assertTrue(ace.is_ace)
        
        # 花色属性
        self.assertEqual(Suit.HEARTS.color, "red")
        self.assertEqual(Suit.SPADES.color, "black")
        self.assertEqual(Suit.HEARTS.name_zh, "红心")
        self.assertEqual(Suit.CLUBS.name_zh, "梅花")


class TestDeck(unittest.TestCase):
    """测试 Deck 类"""
    
    def test_deck_creation(self):
        """测试创建牌组"""
        deck = Deck()
        self.assertEqual(len(deck), 52)
    
    def test_deck_shuffle(self):
        """测试洗牌"""
        deck1 = Deck()
        deck2 = Deck()
        
        # 未洗牌时顺序相同
        cards1 = [str(c) for c in deck1.cards]
        cards2 = [str(c) for c in deck2.cards]
        self.assertEqual(cards1, cards2)
        
        # 洗牌后大概率不同
        deck1.shuffle()
        cards1_shuffled = [str(c) for c in deck1.cards]
        self.assertNotEqual(cards1, cards1_shuffled)
    
    def test_deck_deal(self):
        """测试发牌"""
        deck = Deck()
        deck.shuffle()
        
        # 发一手牌
        hand = deck.deal(5)
        self.assertEqual(len(hand), 5)
        self.assertEqual(len(deck), 47)
        
        # 发多手牌
        deck.reset()
        deck.shuffle()
        hands = deck.deal_hands(4, 5)  # 4个玩家，每人5张
        self.assertEqual(len(hands), 4)
        for hand in hands:
            self.assertEqual(len(hand), 5)
    
    def test_deck_deal_all(self):
        """测试发完所有牌"""
        deck = Deck()
        deck.shuffle()
        all_cards = deck.deal(52)
        self.assertEqual(len(all_cards), 52)
        self.assertEqual(len(deck), 0)
    
    def test_deck_deal_too_many(self):
        """测试发牌超过牌组数量"""
        deck = Deck()
        with self.assertRaises(ValueError):
            deck.deal(53)
    
    def test_deck_reset(self):
        """测试重置牌组"""
        deck = Deck()
        deck.shuffle()
        deck.deal(10)
        self.assertEqual(len(deck), 42)
        
        deck.reset()
        self.assertEqual(len(deck), 52)


class TestHandEvaluator(unittest.TestCase):
    """测试扑克手牌评估"""
    
    def _make_hand(self, cards_str: str) -> list:
        """辅助函数：从字符串创建手牌"""
        return [Card.from_string(c) for c in cards_str.split()]
    
    def test_high_card(self):
        """测试高牌"""
        hand = self._make_hand("♠A ♥8 ♦5 ♣3 ♠2")
        result = HandEvaluator.evaluate(hand)
        self.assertEqual(result.rank, HandRank.HIGH_CARD)
    
    def test_one_pair(self):
        """测试一对"""
        hand = self._make_hand("♠A ♥A ♦5 ♣3 ♠2")
        result = HandEvaluator.evaluate(hand)
        self.assertEqual(result.rank, HandRank.ONE_PAIR)
    
    def test_two_pair(self):
        """测试两对"""
        hand = self._make_hand("♠A ♥A ♦K ♣K ♠2")
        result = HandEvaluator.evaluate(hand)
        self.assertEqual(result.rank, HandRank.TWO_PAIR)
    
    def test_three_of_a_kind(self):
        """测试三条"""
        hand = self._make_hand("♠A ♥A ♦A ♣3 ♠2")
        result = HandEvaluator.evaluate(hand)
        self.assertEqual(result.rank, HandRank.THREE_OF_A_KIND)
    
    def test_straight(self):
        """测试顺子"""
        hand = self._make_hand("♠5 ♥4 ♦3 ♣2 ♠A")  # A-2-3-4-5 最小顺子
        result = HandEvaluator.evaluate(hand)
        self.assertEqual(result.rank, HandRank.STRAIGHT)
        
        hand2 = self._make_hand("♠A ♥K ♦Q ♣J ♠10")  # 10-J-Q-K-A 最大顺子
        result2 = HandEvaluator.evaluate(hand2)
        self.assertEqual(result2.rank, HandRank.STRAIGHT)
    
    def test_flush(self):
        """测试同花"""
        hand = self._make_hand("♠A ♠K ♠8 ♠3 ♠2")
        result = HandEvaluator.evaluate(hand)
        self.assertEqual(result.rank, HandRank.FLUSH)
    
    def test_full_house(self):
        """测试葫芦"""
        hand = self._make_hand("♠A ♥A ♦A ♣K ♠K")
        result = HandEvaluator.evaluate(hand)
        self.assertEqual(result.rank, HandRank.FULL_HOUSE)
    
    def test_four_of_a_kind(self):
        """测试四条"""
        hand = self._make_hand("♠A ♥A ♦A ♣A ♠2")
        result = HandEvaluator.evaluate(hand)
        self.assertEqual(result.rank, HandRank.FOUR_OF_A_KIND)
    
    def test_straight_flush(self):
        """测试同花顺"""
        hand = self._make_hand("♠5 ♠4 ♠3 ♠2 ♠A")  # A-2-3-4-5 同花顺
        result = HandEvaluator.evaluate(hand)
        self.assertEqual(result.rank, HandRank.STRAIGHT_FLUSH)
        
        hand2 = self._make_hand("♠9 ♠8 ♠7 ♠6 ♠5")
        result2 = HandEvaluator.evaluate(hand2)
        self.assertEqual(result2.rank, HandRank.STRAIGHT_FLUSH)
    
    def test_royal_flush(self):
        """测试皇家同花顺"""
        hand = self._make_hand("♠A ♠K ♠Q ♠J ♠10")
        result = HandEvaluator.evaluate(hand)
        self.assertEqual(result.rank, HandRank.ROYAL_FLUSH)
    
    def test_hand_comparison(self):
        """测试手牌比较"""
        # 同花顺 > 四条
        straight_flush = self._make_hand("♠5 ♠4 ♠3 ♠2 ♠A")
        four_kind = self._make_hand("♠A ♥A ♦A ♣A ♠2")
        self.assertEqual(compare_hands(straight_flush, four_kind), 1)
        
        # 葫芦 > 同花
        full_house = self._make_hand("♠A ♥A ♦A ♣K ♠K")
        flush = self._make_hand("♠A ♠K ♠8 ♠3 ♠2")
        self.assertEqual(compare_hands(full_house, flush), 1)
        
        # 两对 > 一对
        two_pair = self._make_hand("♠A ♥A ♦K ♣K ♠2")
        one_pair = self._make_hand("♠A ♥A ♦5 ♣3 ♠2")
        self.assertEqual(compare_hands(two_pair, one_pair), 1)
    
    def test_best_hand_from_seven(self):
        """测试从7张牌中找最佳组合"""
        # 7张牌包含同花顺
        cards = self._make_hand("♠A ♠K ♠Q ♠J ♠10 ♥5 ♦3")
        result = get_best_poker_hand(cards)
        self.assertEqual(result.rank, HandRank.ROYAL_FLUSH)


class TestBlackjack(unittest.TestCase):
    """测试21点工具"""
    
    def _make_hand(self, cards_str: str) -> list:
        """辅助函数：从字符串创建手牌"""
        return [Card.from_string(c) for c in cards_str.split()]
    
    def test_hand_value(self):
        """测试计算手牌点数"""
        hand = self._make_hand("♠A ♠K")
        self.assertEqual(Blackjack.calculate_hand_value(hand), 21)
        
        hand = self._make_hand("♠5 ♥3")
        self.assertEqual(Blackjack.calculate_hand_value(hand), 8)
        
        # A可以是1或11
        hand = self._make_hand("♠A ♥5")
        self.assertEqual(Blackjack.calculate_hand_value(hand), 16)
        
        # 两个A
        hand = self._make_hand("♠A ♥A")
        self.assertEqual(Blackjack.calculate_hand_value(hand), 12)
        
        # 爆牌时A变为1
        hand = self._make_hand("♠A ♥K ♦5")
        self.assertEqual(Blackjack.calculate_hand_value(hand), 16)
    
    def test_blackjack_detection(self):
        """测试Blackjack检测"""
        hand = self._make_hand("♠A ♠K")
        self.assertTrue(Blackjack.is_blackjack(hand))
        
        hand = self._make_hand("♠10 ♥A")
        self.assertTrue(Blackjack.is_blackjack(hand))
        
        hand = self._make_hand("♠A ♠K ♠Q")
        self.assertFalse(Blackjack.is_blackjack(hand))
    
    def test_bust_detection(self):
        """测试爆牌检测"""
        hand = self._make_hand("♠K ♥Q ♦5")
        self.assertTrue(Blackjack.is_bust(hand))
        
        hand = self._make_hand("♠A ♥K ♦5")
        self.assertFalse(Blackjack.is_bust(hand))
    
    def test_hit_strategy(self):
        """测试基础策略建议"""
        # 12点，庄家6，建议停牌
        hand = self._make_hand("♠6 ♥6")
        dealer = Card(Suit.CLUBS, Rank.SIX)
        self.assertFalse(Blackjack.should_hit(hand, dealer))
        
        # 12点，庄家A，建议要牌
        hand = self._make_hand("♠6 ♥6")
        dealer = Card(Suit.CLUBS, Rank.ACE)
        self.assertTrue(Blackjack.should_hit(hand, dealer))
        
        # 17点，建议停牌
        hand = self._make_hand("♠K ♥7")
        dealer = Card(Suit.CLUBS, Rank.ACE)
        self.assertFalse(Blackjack.should_hit(hand, dealer))


class TestCardGame(unittest.TestCase):
    """测试卡牌游戏工具"""
    
    def test_war_compare(self):
        """测试战争牌比较"""
        ace = Card(Suit.SPADES, Rank.ACE)
        king = Card(Suit.HEARTS, Rank.KING)
        two = Card(Suit.CLUBS, Rank.TWO)
        another_two = Card(Suit.DIAMONDS, Rank.TWO)
        
        self.assertEqual(CardGame.war_compare(ace, king), 1)
        self.assertEqual(CardGame.war_compare(two, king), -1)
        self.assertEqual(CardGame.war_compare(two, another_two), 0)
    
    def test_hand_from_string(self):
        """测试从字符串创建手牌"""
        hand = CardGame.create_hand_from_string("♠A ♥K ♦Q")
        self.assertEqual(len(hand), 3)
        self.assertEqual(hand[0].suit, Suit.SPADES)
        self.assertEqual(hand[0].rank, Rank.ACE)
    
    def test_cards_to_string(self):
        """测试手牌转字符串"""
        hand = [Card(Suit.SPADES, Rank.ACE), Card(Suit.HEARTS, Rank.KING)]
        result = CardGame.cards_to_string(hand)
        self.assertEqual(result, "♠A ♥K")
    
    def test_card_name(self):
        """测试牌的完整中文名称"""
        card = Card(Suit.SPADES, Rank.ACE)
        self.assertEqual(CardGame.get_card_name(card), "黑桃王牌")


class TestConvenienceFunctions(unittest.TestCase):
    """测试便捷函数"""
    
    def test_create_deck(self):
        """测试创建牌组"""
        deck = create_deck()
        self.assertEqual(len(deck), 52)
    
    def test_shuffle_deck(self):
        """测试洗牌函数"""
        deck = shuffle_deck(seed=42)
        self.assertEqual(len(deck), 52)
        
        # 相同种子产生相同顺序
        deck2 = shuffle_deck(seed=42)
        cards1 = [str(c) for c in deck.cards]
        cards2 = [str(c) for c in deck2.cards]
        self.assertEqual(cards1, cards2)
    
    def test_deal_hand(self):
        """测试发手牌"""
        hand = deal_hand(5)
        self.assertEqual(len(hand), 5)
        # 每张牌都是唯一的
        self.assertEqual(len(set(str(c) for c in hand)), 5)
    
    def test_evaluate_poker_hand(self):
        """测试便捷评估函数"""
        hand = [Card.from_string(c) for c in "♠A ♠K ♠Q ♠J ♠10".split()]
        result = evaluate_poker_hand(hand)
        self.assertEqual(result.rank, HandRank.ROYAL_FLUSH)


if __name__ == "__main__":
    unittest.main(verbosity=2)