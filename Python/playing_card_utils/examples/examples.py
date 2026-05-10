"""
Playing Card Utils 示例

演示扑克牌工具的主要功能。
"""

import sys
import os
# 添加父目录到路径以便导入 mod
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    Card, Suit, Rank, Deck, HandEvaluator, HandRank,
    Blackjack, CardGame, create_deck, shuffle_deck,
    deal_hand, evaluate_poker_hand, compare_hands, get_best_poker_hand
)


def demo_basic_cards():
    """演示基本的牌操作"""
    print("=" * 50)
    print("基本牌操作")
    print("=" * 50)
    
    # 创建牌
    ace_spades = Card(Suit.SPADES, Rank.ACE)
    king_hearts = Card(Suit.HEARTS, Rank.KING)
    
    print(f"牌: {ace_spades}")
    print(f"显示名: {ace_spades.display}")
    print(f"花色: {ace_spades.suit.name_zh}")
    print(f"点数: {ace_spades.rank.symbol}")
    print(f"是人头牌: {ace_spades.is_face_card}")
    print(f"是A: {ace_spades.is_ace}")
    
    # 比较大小
    print(f"\n比较: {ace_spades} > {king_hearts} = {ace_spades > king_hearts}")
    
    # 从字符串创建
    card = Card.from_string("♦Q")
    print(f"从字符串创建: {card} -> {card.display}")
    print()


def demo_deck_operations():
    """演示牌组操作"""
    print("=" * 50)
    print("牌组操作")
    print("=" * 50)
    
    # 创建牌组
    deck = create_deck()
    print(f"创建牌组: {len(deck)} 张牌")
    
    # 洗牌
    deck.shuffle(seed=42)
    print("洗牌完成")
    
    # 发一手牌
    hand = deck.deal(5)
    print(f"发5张牌: {CardGame.cards_to_string(hand)}")
    
    # 重置
    deck.reset()
    print(f"重置牌组: {len(deck)} 张牌")
    
    # 发多手牌
    hands = deck.deal_hands(4, 5)  # 4玩家每人5张
    for i, h in enumerate(hands):
        print(f"玩家{i+1}: {CardGame.cards_to_string(h)}")
    print()


def demo_poker_hands():
    """演示扑克手牌评估"""
    print("=" * 50)
    print("扑克手牌评估")
    print("=" * 50)
    
    # 定义各种牌型
    hands = {
        "皇家同花顺": "♠A ♠K ♠Q ♠J ♠10",
        "同花顺": "♥9 ♥8 ♥7 ♥6 ♥5",
        "四条": "♠A ♥A ♦A ♣A ♠K",
        "葫芦": "♠K ♥K ♦K ♣Q ♠Q",
        "同花": "♦A ♦J ♦8 ♦4 ♦2",
        "顺子": "♠5 ♥4 ♦3 ♣2 ♠A",
        "三条": "♠7 ♥7 ♦7 ♣K ♠Q",
        "两对": "♠A ♥A ♦K ♣K ♠2",
        "一对": "♠Q ♥Q ♦8 ♣5 ♠3",
        "高牌": "♠A ♥K ♦8 ♣5 ♠2",
    }
    
    for name, cards_str in hands.items():
        hand = [Card.from_string(c) for c in cards_str.split()]
        result = evaluate_poker_hand(hand)
        print(f"{name}: {result.rank.name_zh} (分数: {result.score})")
    print()


def demo_hand_comparison():
    """演示手牌比较"""
    print("=" * 50)
    print("手牌比较")
    print("=" * 50)
    
    # 两对 vs 一对
    two_pair = [Card.from_string(c) for c in "♠A ♥A ♦K ♣K ♠2".split()]
    one_pair = [Card.from_string(c) for c in "♠A ♥A ♦5 ♣3 ♠2".split()]
    
    result = compare_hands(two_pair, one_pair)
    print(f"两对 vs 一对: {result} (1表示前者赢)")
    
    # 同花顺 vs 四条
    straight_flush = [Card.from_string(c) for c in "♠5 ♠4 ♠3 ♠2 ♠A".split()]
    four_kind = [Card.from_string(c) for c in "♠A ♥A ♦A ♣A ♠K".split()]
    
    result = compare_hands(straight_flush, four_kind)
    print(f"同花顺 vs 四条: {result}")
    
    # 平局
    pair1 = [Card.from_string(c) for c in "♠A ♥A ♦K ♣Q ♠J".split()]
    pair2 = [Card.from_string(c) for c in "♥A ♦A ♠K ♠Q ♠J".split()]
    
    result = compare_hands(pair1, pair2)
    print(f"相同牌型不同花色: {result} (0表示平局)")
    print()


def demo_best_hand():
    """演示从7张牌中找最佳组合"""
    print("=" * 50)
    print("德州扑克最佳组合")
    print("=" * 50)
    
    # 玩家手牌 + 公共牌
    hole_cards = [Card.from_string(c) for c in "♠A ♠K".split()]
    community = [Card.from_string(c) for c in "♠Q ♠J ♠10 ♥5 ♦2".split()]
    
    all_cards = hole_cards + community
    print(f"所有牌: {CardGame.cards_to_string(all_cards)}")
    
    best = get_best_poker_hand(all_cards)
    print(f"最佳组合: {best.rank.name_zh}")
    print(f"最佳5张: {CardGame.cards_to_string(best.cards)}")
    print()


def demo_blackjack():
    """演示21点功能"""
    print("=" * 50)
    print("21点游戏")
    print("=" * 50)
    
    # Blackjack
    bj_hand = [Card.from_string(c) for c in "♠A ♠K".split()]
    print(f"牌: {CardGame.cards_to_string(bj_hand)}")
    print(f"点数: {Blackjack.calculate_hand_value(bj_hand)}")
    print(f"是否Blackjack: {Blackjack.is_blackjack(bj_hand)}")
    
    # 普通牌
    hand = [Card.from_string(c) for c in "♠K ♥5 ♦3".split()]
    print(f"\n牌: {CardGame.cards_to_string(hand)}")
    print(f"点数: {Blackjack.calculate_hand_value(hand)}")
    
    # 爆牌
    bust_hand = [Card.from_string(c) for c in "♠K ♥Q ♦5".split()]
    print(f"\n牌: {CardGame.cards_to_string(bust_hand)}")
    print(f"点数: {Blackjack.calculate_hand_value(bust_hand)}")
    print(f"是否爆牌: {Blackjack.is_bust(bust_hand)}")
    
    # 策略建议
    print("\n策略建议:")
    player_hand = [Card.from_string(c) for c in "♠6 ♥6".split()]
    dealer_up = Card.from_string("♣10")
    hit = Blackjack.should_hit(player_hand, dealer_up)
    print(f"玩家: {CardGame.cards_to_string(player_hand)} (点数: {Blackjack.calculate_hand_value(player_hand)})")
    print(f"庄家明牌: {dealer_up}")
    print(f"建议: {'要牌' if hit else '停牌'}")
    print()


def demo_war_game():
    """演示战争牌游戏"""
    print("=" * 50)
    print("战争牌游戏模拟")
    print("=" * 50)
    
    deck = create_deck()
    deck.shuffle()
    
    # 发牌
    player1 = deck.deal(26)
    player2 = deck.deal(26)
    
    print(f"玩家1: {len(player1)} 张牌")
    print(f"玩家2: {len(player2)} 张牌")
    
    # 模拟10回合
    print("\n前10回合:")
    for round_num in range(1, 11):
        if not player1 or not player2:
            break
        
        card1 = player1.pop(0)
        card2 = player2.pop(0)
        
        result = CardGame.war_compare(card1, card2)
        
        if result > 0:
            player1.extend([card1, card2])
            outcome = "玩家1赢"
        elif result < 0:
            player2.extend([card1, card2])
            outcome = "玩家2赢"
        else:
            outcome = "平局"
        
        print(f"回合{round_num}: {card1} vs {card2} -> {outcome}")
    
    print(f"\n最终: 玩家1 {len(player1)} 张, 玩家2 {len(player2)} 张")
    print()


def demo_texas_holdem():
    """演示德州扑克模拟"""
    print("=" * 50)
    print("德州扑克模拟")
    print("=" * 50)
    
    deck = create_deck()
    deck.shuffle()
    
    # 发手牌给4个玩家
    hands = deck.deal_hands(4, 2)
    for i, hand in enumerate(hands):
        print(f"玩家{i+1}手牌: {CardGame.cards_to_string(hand)}")
    
    # 发公共牌
    flop = deck.deal(3)
    turn = deck.deal(1)
    river = deck.deal(1)
    community = flop + turn + river
    
    print(f"\n翻牌: {CardGame.cards_to_string(flop)}")
    print(f"转牌: {CardGame.cards_to_string(turn)}")
    print(f"河牌: {CardGame.cards_to_string(river)}")
    print(f"公共牌: {CardGame.cards_to_string(community)}")
    
    # 评估每个玩家的最佳手牌
    print("\n评估结果:")
    results = []
    for i, hand in enumerate(hands):
        all_cards = hand + community
        best = get_best_poker_hand(all_cards)
        results.append((i + 1, hand, best))
        print(f"玩家{i+1}: {best.rank.name_zh}")
    
    # 找出赢家
    results.sort(key=lambda x: x[2].score, reverse=True)
    winner = results[0]
    print(f"\n🏆 赢家: 玩家{winner[0]} ({winner[2].rank.name_zh})")
    print()


if __name__ == "__main__":
    demo_basic_cards()
    demo_deck_operations()
    demo_poker_hands()
    demo_hand_comparison()
    demo_best_hand()
    demo_blackjack()
    demo_war_game()
    demo_texas_holdem()