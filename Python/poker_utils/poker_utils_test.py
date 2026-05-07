"""
扑克牌工具模块测试
==================

全面测试 poker_utils 模块的所有功能。
"""

import unittest
from mod import (
    Card, Deck, Hand, HandRank, Suit, Rank,
    PokerEvaluator, TexasHoldem, HandAnalyzer,
    create_deck, parse_cards, cards_to_str,
    evaluate_hand, compare_hands, get_hand_rank_name,
    simulate_win_rate, is_pocket_pair, is_suited,
    is_connected, get_starting_hand_strength,
    SUIT_SYMBOLS, RANK_SYMBOLS, HAND_RANK_NAMES
)


class TestCard(unittest.TestCase):
    """测试 Card 类"""
    
    def test_card_creation(self):
        """测试创建扑克牌"""
        card = Card(rank=Rank.ACE, suit=Suit.SPADES)
        self.assertEqual(card.rank, Rank.ACE)
        self.assertEqual(card.suit, Suit.SPADES)
    
    def test_card_str(self):
        """测试扑克牌字符串表示"""
        card = Card(rank=Rank.ACE, suit=Suit.SPADES)
        self.assertEqual(str(card), "A♠")
        
        card2 = Card(rank=Rank.TEN, suit=Suit.HEARTS)
        self.assertEqual(str(card2), "T♥")
        
        card3 = Card(rank=Rank.TWO, suit=Suit.DIAMONDS)
        self.assertEqual(str(card3), "2♦")
    
    def test_card_comparison(self):
        """测试扑克牌比较"""
        ace_spades = Card(rank=Rank.ACE, suit=Suit.SPADES)
        king_spades = Card(rank=Rank.KING, suit=Suit.SPADES)
        ace_hearts = Card(rank=Rank.ACE, suit=Suit.HEARTS)
        
        self.assertTrue(king_spades < ace_spades)
        # 同点数时，按花色枚举值比较：SPADES=0 < HEARTS=1
        self.assertTrue(ace_spades < ace_hearts)
        self.assertFalse(ace_hearts < ace_spades)
    
    def test_card_equality(self):
        """测试扑克牌相等性"""
        card1 = Card(rank=Rank.ACE, suit=Suit.SPADES)
        card2 = Card(rank=Rank.ACE, suit=Suit.SPADES)
        card3 = Card(rank=Rank.KING, suit=Suit.SPADES)
        
        self.assertEqual(card1, card2)
        self.assertNotEqual(card1, card3)
    
    def test_card_from_str(self):
        """测试从字符串创建扑克牌"""
        card = Card.from_str("As")
        self.assertEqual(card.rank, Rank.ACE)
        self.assertEqual(card.suit, Suit.SPADES)
        
        card2 = Card.from_str("Th")
        self.assertEqual(card2.rank, Rank.TEN)
        self.assertEqual(card2.suit, Suit.HEARTS)
        
        card3 = Card.from_str("2d")
        self.assertEqual(card3.rank, Rank.TWO)
        self.assertEqual(card3.suit, Suit.DIAMONDS)
        
        card4 = Card.from_str("KC")
        self.assertEqual(card4.rank, Rank.KING)
        self.assertEqual(card4.suit, Suit.CLUBS)
    
    def test_card_hash(self):
        """测试扑克牌哈希值"""
        card1 = Card(rank=Rank.ACE, suit=Suit.SPADES)
        card2 = Card(rank=Rank.ACE, suit=Suit.SPADES)
        
        # 相同的牌应该有相同的哈希值
        self.assertEqual(hash(card1), hash(card2))
        
        # 可以放入集合
        cards_set = {card1, card2}
        self.assertEqual(len(cards_set), 1)


class TestDeck(unittest.TestCase):
    """测试 Deck 类"""
    
    def test_deck_creation(self):
        """测试创建牌组"""
        deck = Deck()
        self.assertEqual(len(deck), 52)
    
    def test_deck_deal(self):
        """测试发牌"""
        deck = Deck()
        cards = deck.deal(5)
        self.assertEqual(len(cards), 5)
        self.assertEqual(len(deck), 47)
    
    def test_deck_deal_one(self):
        """测试发一张牌"""
        deck = Deck()
        card = deck.deal_one()
        self.assertIsInstance(card, Card)
        self.assertEqual(len(deck), 51)
    
    def test_deck_deal_too_many(self):
        """测试发牌数量超过牌组"""
        deck = Deck()
        deck.deal(50)
        with self.assertRaises(ValueError):
            deck.deal(3)  # 只剩2张
    
    def test_deck_deal_empty(self):
        """测试空牌组发牌"""
        deck = Deck()
        deck.deal(52)
        with self.assertRaises(ValueError):
            deck.deal_one()
    
    def test_deck_shuffle(self):
        """测试洗牌"""
        deck1 = Deck()
        deck2 = Deck()
        
        # 未洗牌时应该相同
        self.assertEqual(deck1._cards[0], deck2._cards[0])
        
        # 洗牌后可能不同（有极小概率相同，但测试目的）
        deck2.shuffle()
        # 注意：有很小概率洗牌后顺序相同，但这个测试主要是验证不会抛错
    
    def test_deck_reset(self):
        """测试重置牌组"""
        deck = Deck()
        deck.deal(10)
        self.assertEqual(len(deck), 42)
        
        deck.reset()
        self.assertEqual(len(deck), 52)
    
    def test_deck_remove(self):
        """测试从牌组移除牌"""
        deck = Deck()
        card = Card(rank=Rank.ACE, suit=Suit.SPADES)
        
        removed = deck.remove(card)
        self.assertTrue(removed)
        self.assertEqual(len(deck), 51)
        
        # 再次移除同一张牌应该失败
        removed = deck.remove(card)
        self.assertFalse(removed)
    
    def test_deck_remove_cards(self):
        """测试批量移除牌"""
        deck = Deck()
        cards = [
            Card(rank=Rank.ACE, suit=Suit.SPADES),
            Card(rank=Rank.ACE, suit=Suit.HEARTS),
            Card(rank=Rank.ACE, suit=Suit.DIAMONDS),
        ]
        
        removed = deck.remove_cards(cards)
        self.assertEqual(removed, 3)
        self.assertEqual(len(deck), 49)


class TestPokerEvaluator(unittest.TestCase):
    """测试牌型评估器"""
    
    def test_royal_flush(self):
        """测试皇家同花顺"""
        cards = parse_cards("As Ks Qs Js Ts")
        hand = PokerEvaluator.evaluate(cards)
        self.assertEqual(hand.rank, HandRank.ROYAL_FLUSH)
    
    def test_straight_flush(self):
        """测试同花顺"""
        cards = parse_cards("9s 8s 7s 6s 5s")
        hand = PokerEvaluator.evaluate(cards)
        self.assertEqual(hand.rank, HandRank.STRAIGHT_FLUSH)
    
    def test_four_of_a_kind(self):
        """测试四条"""
        cards = parse_cards("As Ah Ad Ac 2h")
        hand = PokerEvaluator.evaluate(cards)
        self.assertEqual(hand.rank, HandRank.FOUR_OF_A_KIND)
    
    def test_full_house(self):
        """测试葫芦"""
        cards = parse_cards("As Ah Ad Ks Kh")
        hand = PokerEvaluator.evaluate(cards)
        self.assertEqual(hand.rank, HandRank.FULL_HOUSE)
    
    def test_flush(self):
        """测试同花"""
        cards = parse_cards("As 9s 7s 4s 2s")
        hand = PokerEvaluator.evaluate(cards)
        self.assertEqual(hand.rank, HandRank.FLUSH)
    
    def test_straight(self):
        """测试顺子"""
        cards = parse_cards("9s 8h 7d 6c 5s")
        hand = PokerEvaluator.evaluate(cards)
        self.assertEqual(hand.rank, HandRank.STRAIGHT)
    
    def test_wheel_straight(self):
        """测试轮子顺子(A-2-3-4-5)"""
        cards = parse_cards("As 2h 3d 4c 5s")
        hand = PokerEvaluator.evaluate(cards)
        self.assertEqual(hand.rank, HandRank.STRAIGHT)
    
    def test_three_of_a_kind(self):
        """测试三条"""
        cards = parse_cards("As Ah Ad 9c 5s")
        hand = PokerEvaluator.evaluate(cards)
        self.assertEqual(hand.rank, HandRank.THREE_OF_A_KIND)
    
    def test_two_pair(self):
        """测试两对"""
        cards = parse_cards("As Ah Kd Kc 5s")
        hand = PokerEvaluator.evaluate(cards)
        self.assertEqual(hand.rank, HandRank.TWO_PAIR)
    
    def test_one_pair(self):
        """测试一对"""
        cards = parse_cards("As Ah 9d 7c 5s")
        hand = PokerEvaluator.evaluate(cards)
        self.assertEqual(hand.rank, HandRank.ONE_PAIR)
    
    def test_high_card(self):
        """测试高牌"""
        cards = parse_cards("As 9h 7d 5c 3s")
        hand = PokerEvaluator.evaluate(cards)
        self.assertEqual(hand.rank, HandRank.HIGH_CARD)
    
    def test_compare_hands(self):
        """测试牌型比较"""
        # 同花顺 > 四条
        sf = parse_cards("9s 8s 7s 6s 5s")
        quads = parse_cards("As Ah Ad Ac 2h")
        
        sf_hand = PokerEvaluator.evaluate(sf)
        quads_hand = PokerEvaluator.evaluate(quads)
        
        self.assertTrue(sf_hand > quads_hand)
    
    def test_compare_same_rank(self):
        """测试同类型牌比较"""
        # 比较大的四条
        quads_a = parse_cards("As Ah Ad Ac 2h")
        quads_k = parse_cards("Ks Kh Kd Kc Ah")
        
        hand_a = PokerEvaluator.evaluate(quads_a)
        hand_k = PokerEvaluator.evaluate(quads_k)
        
        self.assertTrue(hand_a > hand_k)
    
    def test_evaluate_seven_cards(self):
        """测试7张牌评估"""
        cards = parse_cards("As Ah Kd Kc 5s 3h 2d")
        hand = PokerEvaluator.evaluate(cards)
        self.assertEqual(hand.rank, HandRank.TWO_PAIR)
    
    def test_evaluate_too_few_cards(self):
        """测试牌数不足"""
        cards = parse_cards("As Ah Kd")
        with self.assertRaises(ValueError):
            PokerEvaluator.evaluate(cards)
    
    def test_get_hand_description(self):
        """测试牌型描述"""
        cards = parse_cards("As Ah Ad Ac 2h")
        hand = PokerEvaluator.evaluate(cards)
        desc = PokerEvaluator.get_hand_description(hand)
        self.assertEqual(desc, "四条 (A)")


class TestTexasHoldem(unittest.TestCase):
    """测试德州扑克工具"""
    
    def test_evaluate_hand(self):
        """测试德州扑克手牌评估"""
        hole = parse_cards("As Ah")
        board = parse_cards("Ad 9c 5s 3h 2d")
        
        hand = TexasHoldem.evaluate_hand(hole, board)
        self.assertEqual(hand.rank, HandRank.THREE_OF_A_KIND)
    
    def test_evaluate_hand_with_flush(self):
        """测试德州扑克同花"""
        hole = parse_cards("As 2s")
        board = parse_cards("Ks 9s 5s 3h 2d")
        
        hand = TexasHoldem.evaluate_hand(hole, board)
        self.assertEqual(hand.rank, HandRank.FLUSH)
    
    def test_calculate_outs_count(self):
        """测试补牌计算"""
        hole = parse_cards("As Ah")
        board = parse_cards("Ad 9c 5s")
        
        outs = TexasHoldem.calculate_outs_count(hole, board, HandRank.FOUR_OF_A_KIND)
        # 只有一张 Ah 可以让四条
        self.assertEqual(outs, 1)
    
    def test_is_pocket_pair(self):
        """测试口袋对子判断"""
        hole = parse_cards("As Ah")
        self.assertTrue(is_pocket_pair(hole))
        
        hole2 = parse_cards("As Kh")
        self.assertFalse(is_pocket_pair(hole2))
    
    def test_is_suited(self):
        """测试同花底牌判断"""
        hole = parse_cards("As Ks")
        self.assertTrue(is_suited(hole))
        
        hole2 = parse_cards("As Kh")
        self.assertFalse(is_suited(hole2))
    
    def test_is_connected(self):
        """测试相连判断"""
        hole = parse_cards("As Kh")  # A-K
        self.assertTrue(is_connected(hole, gap=1))
        
        hole2 = parse_cards("As Qh")  # A-Q
        self.assertTrue(is_connected(hole2, gap=2))
        self.assertFalse(is_connected(hole2, gap=1))
    
    def test_starting_hand_strength(self):
        """测试起手牌强度评估"""
        # Premium hands
        aa = parse_cards("As Ah")
        self.assertEqual(get_starting_hand_strength(aa), 'premium')
        
        aks = parse_cards("As Ks")
        self.assertEqual(get_starting_hand_strength(aks), 'premium')
        
        # Strong hands
        jj = parse_cards("Js Jh")
        self.assertEqual(get_starting_hand_strength(jj), 'strong')
        
        ako = parse_cards("As Kh")
        self.assertEqual(get_starting_hand_strength(ako), 'strong')
        
        # Medium hands
        pocket_5 = parse_cards("5s 5h")
        self.assertEqual(get_starting_hand_strength(pocket_5), 'medium')
        
        aqo = parse_cards("As Qh")
        self.assertEqual(get_starting_hand_strength(aqo), 'medium')
        
        # Weak hands
        axs = parse_cards("As 9s")
        self.assertEqual(get_starting_hand_strength(axs), 'weak')
        
        # Trash hands
        hand = parse_cards("9s 3h")
        self.assertEqual(get_starting_hand_strength(hand), 'trash')


class TestHandAnalyzer(unittest.TestCase):
    """测试手牌分析器"""
    
    def test_get_possible_straights(self):
        """测试可能顺子分析"""
        cards = parse_cards("5s 6h 7d")
        possible = HandAnalyzer.get_possible_straights(cards)
        # 应该有多种顺子可能
        self.assertTrue(len(possible) > 0)
    
    def test_get_possible_flushes(self):
        """测试可能同花分析"""
        cards = parse_cards("As 5s 9s")
        possible = HandAnalyzer.get_possible_flushes(cards)
        # 应该有黑桃同花可能
        self.assertTrue(len(possible) > 0)
        self.assertTrue(any(suit == Suit.SPADES for suit, _ in possible))


class TestUtilityFunctions(unittest.TestCase):
    """测试工具函数"""
    
    def test_create_deck(self):
        """测试创建牌组"""
        deck = create_deck()
        self.assertEqual(len(deck), 52)
    
    def test_create_deck_unshuffled(self):
        """测试创建未洗牌的牌组"""
        deck = create_deck(shuffled=False)
        # 未洗牌时第一张应该是黑桃2 (Suit.SPADES=0, Rank.TWO=2)
        first_card = deck._cards[0]
        self.assertEqual(first_card.rank, Rank.TWO)
        self.assertEqual(first_card.suit, Suit.SPADES)
    
    def test_parse_cards(self):
        """测试解析牌字符串"""
        cards = parse_cards("As Kh 2d")
        self.assertEqual(len(cards), 3)
        self.assertEqual(cards[0].rank, Rank.ACE)
        self.assertEqual(cards[0].suit, Suit.SPADES)
    
    def test_cards_to_str(self):
        """测试牌列表转字符串"""
        cards = [
            Card(rank=Rank.ACE, suit=Suit.SPADES),
            Card(rank=Rank.KING, suit=Suit.HEARTS)
        ]
        result = cards_to_str(cards)
        self.assertEqual(result, "A♠ K♥")
    
    def test_evaluate_hand_function(self):
        """测试快捷评估函数"""
        cards = parse_cards("As Ah Ad Ac 2h")
        hand = evaluate_hand(cards)
        self.assertEqual(hand.rank, HandRank.FOUR_OF_A_KIND)
    
    def test_compare_hands_function(self):
        """测试快捷比较函数"""
        cards1 = parse_cards("As Ah Ad Ac 2h")
        cards2 = parse_cards("Ks Kh Kd Kc Ah")
        
        result = compare_hands(cards1, cards2)
        self.assertEqual(result, 1)  # A四条 > K四条
    
    def test_get_hand_rank_name(self):
        """测试获取牌型名称"""
        cards = parse_cards("As Ah")
        hand = evaluate_hand(cards + parse_cards("Ad Ac 2h"))
        name = get_hand_rank_name(hand)
        self.assertEqual(name, "四条")
    
    def test_simulate_win_rate(self):
        """测试胜率模拟"""
        # AA vs 随机牌
        aa = parse_cards("As Ah")
        win_rate = simulate_win_rate(aa, simulations=100)
        
        # AA 应该有较高的胜率
        self.assertTrue(0.7 < win_rate < 1.0)


class TestEdgeCases(unittest.TestCase):
    """测试边缘情况"""
    
    def test_all_same_suit_rank_order(self):
        """测试同花色牌的顺序"""
        cards = [
            Card(rank=Rank.ACE, suit=Suit.SPADES),
            Card(rank=Rank.KING, suit=Suit.SPADES),
            Card(rank=Rank.QUEEN, suit=Suit.SPADES),
            Card(rank=Rank.JACK, suit=Suit.SPADES),
            Card(rank=Rank.TEN, suit=Suit.SPADES),
        ]
        hand = PokerEvaluator.evaluate(cards)
        self.assertEqual(hand.rank, HandRank.ROYAL_FLUSH)
    
    def test_different_suit_same_rank_order(self):
        """测试不同花色同一等级顺序"""
        cards = [
            Card(rank=Rank.ACE, suit=Suit.SPADES),
            Card(rank=Rank.KING, suit=Suit.HEARTS),
            Card(rank=Rank.QUEEN, suit=Suit.DIAMONDS),
            Card(rank=Rank.JACK, suit=Suit.CLUBS),
            Card(rank=Rank.TEN, suit=Suit.SPADES),
        ]
        hand = PokerEvaluator.evaluate(cards)
        self.assertEqual(hand.rank, HandRank.STRAIGHT)
    
    def test_compare_tie(self):
        """测试平局比较"""
        cards1 = parse_cards("As Ks Qs Js 9s")
        cards2 = parse_cards("Ah Kh Qh Jh 9h")
        
        result = compare_hands(cards1, cards2)
        self.assertEqual(result, 0)  # 同样大小的同花顺
    
    def test_full_house_comparison(self):
        """测试葫芦比较"""
        # A-K 葫芦 vs A-Q 葫芦
        fh1 = parse_cards("As Ah Ad Ks Kh")
        fh2 = parse_cards("Ac Ah Ad Qs Qh")
        
        result = compare_hands(fh1, fh2)
        self.assertEqual(result, 1)
    
    def test_two_pair_comparison(self):
        """测试两对比较"""
        # A-K 两对 vs A-Q 两对
        tp1 = parse_cards("As Ah Ks Kh 9c")
        tp2 = parse_cards("Ac Ah Qs Qh 9c")
        
        result = compare_hands(tp1, tp2)
        self.assertEqual(result, 1)
    
    def test_kicker_comparison(self):
        """测试kicker比较"""
        # 一对A，高kicker vs 低kicker
        p1 = parse_cards("As Ah Kc 9d 5s")
        p2 = parse_cards("Ac Ad Qc 9d 5s")
        
        result = compare_hands(p1, p2)
        self.assertEqual(result, 1)


if __name__ == '__main__':
    unittest.main()