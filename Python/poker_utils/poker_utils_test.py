"""
扑克牌工具测试

测试内容:
- Card 类测试
- Deck 类测试
- Hand 类测试
- 牌型判断测试
- 手牌比较测试
- 工具函数测试
- 游戏辅助类测试
"""

import sys
import os
import unittest

# Add module directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mod import (
    Card, Deck, Hand, PokerGame,
    Suit, Rank, HandRank,
    create_deck, shuffle_deck, deal_hands,
    evaluate_hand, compare_hands, best_hand,
    hand_probability, hand_combinations_count,
    cards_to_string, string_to_cards,
    get_all_cards, card_count_by_rank, card_count_by_suit,
    HAND_RANK_NAMES
)


class TestCard(unittest.TestCase):
    """Card 类测试"""
    
    def test_card_creation(self):
        """测试创建牌"""
        card = Card(Suit.SPADES, Rank.ACE)
        self.assertEqual(card.suit, Suit.SPADES)
        self.assertEqual(card.rank, Rank.ACE)
    
    def test_card_repr(self):
        """测试牌的字符串表示"""
        card = Card(Suit.HEARTS, Rank.KING)
        self.assertEqual(repr(card), "K♥")
        self.assertEqual(str(card), "红心K")
    
    def test_card_equality(self):
        """测试牌的相等性"""
        card1 = Card(Suit.DIAMONDS, Rank.QUEEN)
        card2 = Card(Suit.DIAMONDS, Rank.QUEEN)
        card3 = Card(Suit.DIAMONDS, Rank.JACK)
        card4 = Card(Suit.CLUBS, Rank.QUEEN)
        
        self.assertEqual(card1, card2)
        self.assertNotEqual(card1, card3)
        self.assertNotEqual(card1, card4)
    
    def test_card_comparison(self):
        """测试牌的大小比较"""
        ace_spades = Card(Suit.SPADES, Rank.ACE)
        ace_hearts = Card(Suit.HEARTS, Rank.ACE)
        king_spades = Card(Suit.SPADES, Rank.KING)
        
        self.assertTrue(king_spades < ace_spades)
        self.assertTrue(ace_hearts < ace_spades)  # 同点数，黑桃最大
    
    def test_card_from_string(self):
        """测试从字符串解析牌"""
        card = Card.from_string("A♠")
        self.assertEqual(card.suit, Suit.SPADES)
        self.assertEqual(card.rank, Rank.ACE)
        
        card2 = Card.from_string("K♥")
        self.assertEqual(card2.suit, Suit.HEARTS)
        self.assertEqual(card2.rank, Rank.KING)
    
    def test_card_to_dict(self):
        """测试牌转字典"""
        card = Card(Suit.CLUBS, Rank.TEN)
        d = card.to_dict()
        
        self.assertEqual(d['suit'], 'CLUBS')
        self.assertEqual(d['rank'], 'TEN')
        self.assertEqual(d['symbol'], '10♣')


class TestDeck(unittest.TestCase):
    """Deck 类测试"""
    
    def test_deck_creation(self):
        """测试创建牌组"""
        deck = Deck()
        self.assertEqual(len(deck), 52)
    
    def test_deck_shuffle(self):
        """测试洗牌"""
        deck1 = Deck()
        deck2 = Deck()
        
        # 两副新牌组应该相同
        for c1, c2 in zip(deck1, deck2):
            self.assertEqual(c1, c2)
        
        # 洗牌后可能不同（概率极高）
        deck1.shuffle()
        same_order = all(c1 == c2 for c1, c2 in zip(deck1, deck2))
        self.assertFalse(same_order)  # 几乎不可能相同
    
    def test_deck_draw(self):
        """测试抽牌"""
        deck = Deck()
        cards = deck.draw(5)
        
        self.assertEqual(len(cards), 5)
        self.assertEqual(len(deck), 47)
    
    def test_deck_draw_one(self):
        """测试抽一张牌"""
        deck = Deck()
        card = deck.draw_one()
        
        self.assertIsInstance(card, Card)
        self.assertEqual(len(deck), 51)
    
    def test_deck_empty_error(self):
        """测试牌组空时抽牌报错"""
        deck = Deck(cards=[])
        
        with self.assertRaises(ValueError):
            deck.draw_one()
        
        with self.assertRaises(ValueError):
            deck.draw(1)
    
    def test_deck_reset(self):
        """测试重置牌组"""
        deck = Deck()
        deck.draw(20)
        
        self.assertEqual(len(deck), 32)
        
        deck.reset()
        self.assertEqual(len(deck), 52)
    
    def test_deck_add_card(self):
        """测试添加牌"""
        deck = Deck(cards=[])
        card = Card(Suit.SPADES, Rank.ACE)
        
        deck.add_card(card)
        self.assertEqual(len(deck), 1)
        self.assertEqual(deck.cards[0], card)


class TestHand(unittest.TestCase):
    """Hand 类测试"""
    
    def test_high_card(self):
        """测试高牌"""
        hand = Hand([
            Card(Suit.SPADES, Rank.ACE),
            Card(Suit.HEARTS, Rank.KING),
            Card(Suit.DIAMONDS, Rank.QUEEN),
            Card(Suit.CLUBS, Rank.JACK),
            Card(Suit.SPADES, Rank.NINE),
        ])
        
        rank, values = hand.evaluate()
        self.assertEqual(rank, HandRank.HIGH_CARD)
        self.assertEqual(hand.get_rank_name(), "高牌")
    
    def test_one_pair(self):
        """测试一对"""
        hand = Hand([
            Card(Suit.SPADES, Rank.ACE),
            Card(Suit.HEARTS, Rank.ACE),
            Card(Suit.DIAMONDS, Rank.KING),
            Card(Suit.CLUBS, Rank.QUEEN),
            Card(Suit.SPADES, Rank.JACK),
        ])
        
        rank, values = hand.evaluate()
        self.assertEqual(rank, HandRank.ONE_PAIR)
        self.assertEqual(values[0], Rank.ACE)
    
    def test_two_pair(self):
        """测试两对"""
        hand = Hand([
            Card(Suit.SPADES, Rank.ACE),
            Card(Suit.HEARTS, Rank.ACE),
            Card(Suit.DIAMONDS, Rank.KING),
            Card(Suit.CLUBS, Rank.KING),
            Card(Suit.SPADES, Rank.QUEEN),
        ])
        
        rank, values = hand.evaluate()
        self.assertEqual(rank, HandRank.TWO_PAIR)
        self.assertEqual(values[0], Rank.ACE)
        self.assertEqual(values[1], Rank.KING)
    
    def test_three_of_a_kind(self):
        """测试三条"""
        hand = Hand([
            Card(Suit.SPADES, Rank.ACE),
            Card(Suit.HEARTS, Rank.ACE),
            Card(Suit.DIAMONDS, Rank.ACE),
            Card(Suit.CLUBS, Rank.KING),
            Card(Suit.SPADES, Rank.QUEEN),
        ])
        
        rank, values = hand.evaluate()
        self.assertEqual(rank, HandRank.THREE_OF_A_KIND)
        self.assertEqual(values[0], Rank.ACE)
    
    def test_straight(self):
        """测试顺子"""
        hand = Hand([
            Card(Suit.SPADES, Rank.FIVE),
            Card(Suit.HEARTS, Rank.FOUR),
            Card(Suit.DIAMONDS, Rank.THREE),
            Card(Suit.CLUBS, Rank.TWO),
            Card(Suit.SPADES, Rank.ACE),
        ])
        
        rank, values = hand.evaluate()
        self.assertEqual(rank, HandRank.STRAIGHT)
        self.assertEqual(values[0], Rank.FIVE)  # A-2-3-4-5 顺子最高为5
    
    def test_straight_normal(self):
        """测试普通顺子"""
        hand = Hand([
            Card(Suit.SPADES, Rank.TEN),
            Card(Suit.HEARTS, Rank.NINE),
            Card(Suit.DIAMONDS, Rank.EIGHT),
            Card(Suit.CLUBS, Rank.SEVEN),
            Card(Suit.SPADES, Rank.SIX),
        ])
        
        rank, values = hand.evaluate()
        self.assertEqual(rank, HandRank.STRAIGHT)
        self.assertEqual(values[0], Rank.TEN)
    
    def test_flush(self):
        """测试同花"""
        hand = Hand([
            Card(Suit.HEARTS, Rank.ACE),
            Card(Suit.HEARTS, Rank.KING),
            Card(Suit.HEARTS, Rank.QUEEN),
            Card(Suit.HEARTS, Rank.FIVE),
            Card(Suit.HEARTS, Rank.TWO),
        ])
        
        rank, values = hand.evaluate()
        self.assertEqual(rank, HandRank.FLUSH)
    
    def test_full_house(self):
        """测试葫芦"""
        hand = Hand([
            Card(Suit.SPADES, Rank.ACE),
            Card(Suit.HEARTS, Rank.ACE),
            Card(Suit.DIAMONDS, Rank.ACE),
            Card(Suit.CLUBS, Rank.KING),
            Card(Suit.SPADES, Rank.KING),
        ])
        
        rank, values = hand.evaluate()
        self.assertEqual(rank, HandRank.FULL_HOUSE)
        self.assertEqual(values[0], Rank.ACE)  # 三条的点数
        self.assertEqual(values[1], Rank.KING)  # 对子的点数
    
    def test_four_of_a_kind(self):
        """测试四条"""
        hand = Hand([
            Card(Suit.SPADES, Rank.ACE),
            Card(Suit.HEARTS, Rank.ACE),
            Card(Suit.DIAMONDS, Rank.ACE),
            Card(Suit.CLUBS, Rank.ACE),
            Card(Suit.SPADES, Rank.KING),
        ])
        
        rank, values = hand.evaluate()
        self.assertEqual(rank, HandRank.FOUR_OF_A_KIND)
        self.assertEqual(values[0], Rank.ACE)
    
    def test_straight_flush(self):
        """测试同花顺"""
        hand = Hand([
            Card(Suit.SPADES, Rank.KING),
            Card(Suit.SPADES, Rank.QUEEN),
            Card(Suit.SPADES, Rank.JACK),
            Card(Suit.SPADES, Rank.TEN),
            Card(Suit.SPADES, Rank.NINE),
        ])
        
        rank, values = hand.evaluate()
        self.assertEqual(rank, HandRank.STRAIGHT_FLUSH)
        self.assertEqual(values[0], Rank.KING)
    
    def test_royal_flush(self):
        """测试皇家同花顺"""
        hand = Hand([
            Card(Suit.SPADES, Rank.ACE),
            Card(Suit.SPADES, Rank.KING),
            Card(Suit.SPADES, Rank.QUEEN),
            Card(Suit.SPADES, Rank.JACK),
            Card(Suit.SPADES, Rank.TEN),
        ])
        
        rank, values = hand.evaluate()
        self.assertEqual(rank, HandRank.ROYAL_FLUSH)
    
    def test_hand_comparison(self):
        """测试手牌比较"""
        pair = Hand([
            Card(Suit.SPADES, Rank.ACE),
            Card(Suit.HEARTS, Rank.ACE),
            Card(Suit.DIAMONDS, Rank.KING),
            Card(Suit.CLUBS, Rank.QUEEN),
            Card(Suit.SPADES, Rank.JACK),
        ])
        
        two_pair = Hand([
            Card(Suit.SPADES, Rank.ACE),
            Card(Suit.HEARTS, Rank.ACE),
            Card(Suit.DIAMONDS, Rank.KING),
            Card(Suit.CLUBS, Rank.KING),
            Card(Suit.SPADES, Rank.QUEEN),
        ])
        
        self.assertTrue(two_pair > pair)
        self.assertTrue(pair < two_pair)
        
        # 测试同牌型比较
        pair_lower = Hand([
            Card(Suit.SPADES, Rank.KING),
            Card(Suit.HEARTS, Rank.KING),
            Card(Suit.DIAMONDS, Rank.QUEEN),
            Card(Suit.CLUBS, Rank.JACK),
            Card(Suit.SPADES, Rank.TEN),
        ])
        
        self.assertTrue(pair > pair_lower)  # AA对 > KK对
    
    def test_hand_equality(self):
        """测试手牌相等"""
        hand1 = Hand([
            Card(Suit.SPADES, Rank.ACE),
            Card(Suit.HEARTS, Rank.ACE),
            Card(Suit.DIAMONDS, Rank.KING),
            Card(Suit.CLUBS, Rank.QUEEN),
            Card(Suit.SPADES, Rank.JACK),
        ])
        
        hand2 = Hand([
            Card(Suit.DIAMONDS, Rank.ACE),
            Card(Suit.CLUBS, Rank.ACE),
            Card(Suit.SPADES, Rank.KING),
            Card(Suit.HEARTS, Rank.QUEEN),
            Card(Suit.DIAMONDS, Rank.JACK),
        ])
        
        # 牌型相同，点数相同，应视为相等
        self.assertTrue(hand1.compare(hand2) == 0)


class TestUtilityFunctions(unittest.TestCase):
    """工具函数测试"""
    
    def test_create_deck(self):
        """测试创建牌组"""
        deck = create_deck()
        self.assertEqual(len(deck), 52)
    
    def test_shuffle_deck(self):
        """测试洗牌"""
        deck = create_deck()
        shuffled = shuffle_deck(deck)
        self.assertEqual(len(shuffled), 52)
    
    def test_deal_hands(self):
        """测试发牌"""
        deck = create_deck()
        shuffle_deck(deck)
        hands = deal_hands(deck, num_players=4, cards_per_hand=5)
        
        self.assertEqual(len(hands), 4)
        for hand in hands:
            self.assertEqual(len(hand.cards), 5)
    
    def test_evaluate_hand(self):
        """测试评估手牌"""
        cards = [
            Card(Suit.SPADES, Rank.ACE),
            Card(Suit.HEARTS, Rank.ACE),
            Card(Suit.DIAMONDS, Rank.KING),
            Card(Suit.CLUBS, Rank.KING),
            Card(Suit.SPADES, Rank.QUEEN),
        ]
        
        rank, values = evaluate_hand(cards)
        self.assertEqual(rank, HandRank.TWO_PAIR)
    
    def test_compare_hands(self):
        """测试比较手牌"""
        hand1 = [
            Card(Suit.SPADES, Rank.ACE),
            Card(Suit.HEARTS, Rank.ACE),
            Card(Suit.DIAMONDS, Rank.KING),
            Card(Suit.CLUBS, Rank.QUEEN),
            Card(Suit.SPADES, Rank.JACK),
        ]
        
        hand2 = [
            Card(Suit.SPADES, Rank.KING),
            Card(Suit.HEARTS, Rank.KING),
            Card(Suit.DIAMONDS, Rank.QUEEN),
            Card(Suit.CLUBS, Rank.JACK),
            Card(Suit.SPADES, Rank.TEN),
        ]
        
        self.assertTrue(compare_hands(hand1, hand2) > 0)
    
    def test_best_hand(self):
        """测试从7张牌中选最佳组合"""
        # 假设有公共牌和手牌
        seven_cards = [
            Card(Suit.SPADES, Rank.ACE),
            Card(Suit.HEARTS, Rank.ACE),  # 手牌
            Card(Suit.SPADES, Rank.KING),
            Card(Suit.HEARTS, Rank.KING),
            Card(Suit.DIAMONDS, Rank.KING),  # 公共牌
            Card(Suit.CLUBS, Rank.TWO),
            Card(Suit.SPADES, Rank.THREE),
        ]
        
        best = best_hand(seven_cards)
        rank, _ = best.evaluate()
        # 应该能选出三张K加一对A（葫芦）或两对
        self.assertIn(rank, [HandRank.FULL_HOUSE, HandRank.THREE_OF_A_KIND, HandRank.TWO_PAIR])
    
    def test_hand_probability(self):
        """测试牌型概率"""
        # 皇家同花顺概率应约为0.000154%
        prob = hand_probability(HandRank.ROYAL_FLUSH)
        self.assertAlmostEqual(prob, 0.000154, places=5)
        
        # 一对概率应约为42%
        prob = hand_probability(HandRank.ONE_PAIR)
        self.assertAlmostEqual(prob, 42.2569, places=2)
    
    def test_hand_combinations_count(self):
        """测试牌型组合数"""
        # 皇家同花顺只有4种
        self.assertEqual(hand_combinations_count(HandRank.ROYAL_FLUSH), 4)
        
        # 高牌最多
        self.assertEqual(hand_combinations_count(HandRank.HIGH_CARD), 1302540)
    
    def test_cards_to_string(self):
        """测试牌列表转字符串"""
        cards = [
            Card(Suit.SPADES, Rank.ACE),
            Card(Suit.HEARTS, Rank.KING),
        ]
        
        s = cards_to_string(cards)
        self.assertEqual(s, "A♠ K♥")
        
        s_chinese = cards_to_string(cards, chinese=True)
        self.assertEqual(s_chinese, "黑桃A 红心K")
    
    def test_string_to_cards(self):
        """测试字符串解析为牌"""
        # 简化测试
        cards = string_to_cards("A♠")
        self.assertEqual(len(cards), 1)
        self.assertEqual(cards[0].suit, Suit.SPADES)
        self.assertEqual(cards[0].rank, Rank.ACE)
    
    def test_get_all_cards(self):
        """测试获取所有牌"""
        all_cards = get_all_cards()
        self.assertEqual(len(all_cards), 52)
    
    def test_card_count_by_rank(self):
        """测试按牌面统计"""
        cards = [
            Card(Suit.SPADES, Rank.ACE),
            Card(Suit.HEARTS, Rank.ACE),
            Card(Suit.DIAMONDS, Rank.ACE),
            Card(Suit.CLUBS, Rank.KING),
        ]
        
        count = card_count_by_rank(cards)
        self.assertEqual(count[Rank.ACE], 3)
        self.assertEqual(count[Rank.KING], 1)
    
    def test_card_count_by_suit(self):
        """测试按花色统计"""
        cards = [
            Card(Suit.SPADES, Rank.ACE),
            Card(Suit.SPADES, Rank.KING),
            Card(Suit.HEARTS, Rank.QUEEN),
        ]
        
        count = card_count_by_suit(cards)
        self.assertEqual(count[Suit.SPADES], 2)
        self.assertEqual(count[Suit.HEARTS], 1)


class TestPokerGame(unittest.TestCase):
    """PokerGame 类测试"""
    
    def test_game_creation(self):
        """测试创建游戏"""
        game = PokerGame(num_players=4)
        self.assertEqual(game.num_players, 4)
    
    def test_game_deal(self):
        """测试发牌"""
        game = PokerGame(num_players=4)
        game.new_round()
        game.deal_to_players(2)
        
        self.assertEqual(len(game.hands), 4)
        for hand in game.hands:
            self.assertEqual(len(hand.cards), 2)
    
    def test_game_community_cards(self):
        """测试公共牌"""
        game = PokerGame(num_players=2)
        game.new_round()
        game.deal_to_players(2)
        
        flop = game.flop()
        self.assertEqual(len(flop), 3)
        self.assertEqual(len(game.community_cards), 3)
        
        turn = game.turn()
        self.assertEqual(len(game.community_cards), 4)
        
        river = game.river()
        self.assertEqual(len(game.community_cards), 5)
    
    def test_game_get_winner(self):
        """测试获取赢家"""
        game = PokerGame(num_players=2)
        game.new_round()
        
        # 手动设置牌组，确保有明确的赢家
        # 玩家1：四条A
        # 玩家2：一对K
        game.deck = Deck(cards=[
            Card(Suit.SPADES, Rank.ACE),
            Card(Suit.HEARTS, Rank.ACE),   # 玩家1手牌
            Card(Suit.DIAMONDS, Rank.KING),
            Card(Suit.CLUBS, Rank.KING),    # 玩家2手牌
            # 公共牌
            Card(Suit.DIAMONDS, Rank.ACE),
            Card(Suit.CLUBS, Rank.ACE),
            Card(Suit.SPADES, Rank.TWO),
            Card(Suit.HEARTS, Rank.THREE),
            Card(Suit.SPADES, Rank.FOUR),
        ])
        
        game.deal_to_players(2)
        game.flop()
        game.turn()
        game.river()
        
        winner_idx, best_hands = game.get_winner()
        
        # 玩家1应该赢（四条A）
        self.assertEqual(winner_idx, 0)
        self.assertEqual(best_hands[0].get_rank_name(), "四条")


class TestEdgeCases(unittest.TestCase):
    """边界情况测试"""
    
    def test_wheel_straight(self):
        """测试A-2-3-4-5顺子（轮子）"""
        hand = Hand([
            Card(Suit.SPADES, Rank.ACE),
            Card(Suit.HEARTS, Rank.TWO),
            Card(Suit.DIAMONDS, Rank.THREE),
            Card(Suit.CLUBS, Rank.FOUR),
            Card(Suit.SPADES, Rank.FIVE),
        ])
        
        rank, values = hand.evaluate()
        self.assertEqual(rank, HandRank.STRAIGHT)
        self.assertEqual(values[0], Rank.FIVE)  # 轮子最高牌是5
    
    def test_hand_with_wrong_card_count(self):
        """测试非5张牌时评估报错"""
        hand = Hand([
            Card(Suit.SPADES, Rank.ACE),
            Card(Suit.HEARTS, Rank.KING),
        ])
        
        with self.assertRaises(ValueError):
            hand.evaluate()
    
    def test_best_hand_with_minimum_cards(self):
        """测试用最少的牌（5张）选最佳"""
        cards = [
            Card(Suit.SPADES, Rank.ACE),
            Card(Suit.HEARTS, Rank.ACE),
            Card(Suit.DIAMONDS, Rank.ACE),
            Card(Suit.CLUBS, Rank.ACE),
            Card(Suit.SPADES, Rank.KING),
        ]
        
        best = best_hand(cards)
        rank, _ = best.evaluate()
        self.assertEqual(rank, HandRank.FOUR_OF_A_KIND)


if __name__ == "__main__":
    unittest.main(verbosity=2)