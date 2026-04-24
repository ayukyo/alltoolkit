"""
扑克牌工具使用示例

本示例展示 poker_utils 的主要功能：
1. 创建牌组和洗牌
2. 发牌和手牌评估
3. 各种牌型的判断
4. 手牌比较
5. 简单游戏模拟
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import mod
from mod import (
    Card, Deck, Hand, PokerGame,
    Suit, Rank, HandRank,
    create_deck, shuffle_deck, deal_hands,
    evaluate_hand, compare_hands, best_hand,
    hand_probability, hand_combinations_count,
    cards_to_string, string_to_cards,
    HAND_RANK_NAMES
)


def print_separator(title: str):
    """打印分隔线"""
    print(f"\n{'='*50}")
    print(f"  {title}")
    print('='*50)


def example_1_basic_operations():
    """示例1：基本操作"""
    print_separator("示例1：基本操作")
    
    # 创建牌组
    deck = create_deck()
    print(f"创建牌组: {deck}")
    print(f"牌组包含 {len(deck)} 张牌")
    
    # 洗牌
    shuffle_deck(deck)
    print("洗牌完成")
    
    # 抽牌
    cards = deck.draw(5)
    print(f"抽5张牌: {cards_to_string(cards)}")
    print(f"牌组剩余: {len(deck)} 张")
    
    # 从字符串解析
    card = Card.from_string("A♠")
    print(f"从字符串解析: {card} -> {str(card)}")


def example_2_hand_evaluation():
    """示例2：手牌评估"""
    print_separator("示例2：手牌评估")
    
    # 创建各种牌型
    hands = {
        "高牌": [
            Card(Suit.SPADES, Rank.ACE),
            Card(Suit.HEARTS, Rank.KING),
            Card(Suit.DIAMONDS, Rank.QUEEN),
            Card(Suit.CLUBS, Rank.JACK),
            Card(Suit.SPADES, Rank.NINE),
        ],
        "一对": [
            Card(Suit.SPADES, Rank.ACE),
            Card(Suit.HEARTS, Rank.ACE),
            Card(Suit.DIAMONDS, Rank.KING),
            Card(Suit.CLUBS, Rank.QUEEN),
            Card(Suit.SPADES, Rank.JACK),
        ],
        "两对": [
            Card(Suit.SPADES, Rank.ACE),
            Card(Suit.HEARTS, Rank.ACE),
            Card(Suit.DIAMONDS, Rank.KING),
            Card(Suit.CLUBS, Rank.KING),
            Card(Suit.SPADES, Rank.QUEEN),
        ],
        "三条": [
            Card(Suit.SPADES, Rank.ACE),
            Card(Suit.HEARTS, Rank.ACE),
            Card(Suit.DIAMONDS, Rank.ACE),
            Card(Suit.CLUBS, Rank.KING),
            Card(Suit.SPADES, Rank.QUEEN),
        ],
        "顺子": [
            Card(Suit.SPADES, Rank.TEN),
            Card(Suit.HEARTS, Rank.NINE),
            Card(Suit.DIAMONDS, Rank.EIGHT),
            Card(Suit.CLUBS, Rank.SEVEN),
            Card(Suit.SPADES, Rank.SIX),
        ],
        "同花": [
            Card(Suit.HEARTS, Rank.ACE),
            Card(Suit.HEARTS, Rank.KING),
            Card(Suit.HEARTS, Rank.QUEEN),
            Card(Suit.HEARTS, Rank.FIVE),
            Card(Suit.HEARTS, Rank.TWO),
        ],
        "葫芦": [
            Card(Suit.SPADES, Rank.ACE),
            Card(Suit.HEARTS, Rank.ACE),
            Card(Suit.DIAMONDS, Rank.ACE),
            Card(Suit.CLUBS, Rank.KING),
            Card(Suit.SPADES, Rank.KING),
        ],
        "四条": [
            Card(Suit.SPADES, Rank.ACE),
            Card(Suit.HEARTS, Rank.ACE),
            Card(Suit.DIAMONDS, Rank.ACE),
            Card(Suit.CLUBS, Rank.ACE),
            Card(Suit.SPADES, Rank.KING),
        ],
        "同花顺": [
            Card(Suit.SPADES, Rank.KING),
            Card(Suit.SPADES, Rank.QUEEN),
            Card(Suit.SPADES, Rank.JACK),
            Card(Suit.SPADES, Rank.TEN),
            Card(Suit.SPADES, Rank.NINE),
        ],
        "皇家同花顺": [
            Card(Suit.SPADES, Rank.ACE),
            Card(Suit.SPADES, Rank.KING),
            Card(Suit.SPADES, Rank.QUEEN),
            Card(Suit.SPADES, Rank.JACK),
            Card(Suit.SPADES, Rank.TEN),
        ],
    }
    
    for name, cards in hands.items():
        hand = Hand(cards)
        rank, values = hand.evaluate()
        print(f"{name}: {cards_to_string(cards)}")
        print(f"  -> 识别为: {hand.get_rank_name()} (等级{rank})")


def example_3_hand_comparison():
    """示例3：手牌比较"""
    print_separator("示例3：手牌比较")
    
    # 创建两手牌
    hand1 = Hand([
        Card(Suit.SPADES, Rank.ACE),
        Card(Suit.HEARTS, Rank.ACE),
        Card(Suit.DIAMONDS, Rank.KING),
        Card(Suit.CLUBS, Rank.QUEEN),
        Card(Suit.SPADES, Rank.JACK),
    ])
    
    hand2 = Hand([
        Card(Suit.SPADES, Rank.KING),
        Card(Suit.HEARTS, Rank.KING),
        Card(Suit.DIAMONDS, Rank.KING),
        Card(Suit.CLUBS, Rank.TEN),
        Card(Suit.SPADES, Rank.NINE),
    ])
    
    print(f"手牌1: {hand1} ({hand1.get_rank_name()})")
    print(f"手牌2: {hand2} ({hand2.get_rank_name()})")
    
    result = hand1.compare(hand2)
    if result > 0:
        print("结果: 手牌1 获胜!")
    elif result < 0:
        print("结果: 手牌2 获胜!")
    else:
        print("结果: 平局!")
    
    # 使用比较运算符
    print(f"\n使用运算符比较:")
    print(f"hand1 > hand2: {hand1 > hand2}")
    print(f"hand1 < hand2: {hand1 < hand2}")


def example_4_best_hand_selection():
    """示例4：从7张牌中选最佳组合（德州扑克）"""
    print_separator("示例4：最佳组合选择")
    
    # 模拟德州扑克：2张手牌 + 5张公共牌
    hole_cards = [
        Card(Suit.SPADES, Rank.ACE),
        Card(Suit.HEARTS, Rank.ACE),
    ]
    
    community_cards = [
        Card(Suit.DIAMONDS, Rank.ACE),
        Card(Suit.CLUBS, Rank.KING),
        Card(Suit.SPADES, Rank.KING),
        Card(Suit.HEARTS, Rank.TWO),
        Card(Suit.DIAMONDS, Rank.THREE),
    ]
    
    all_cards = hole_cards + community_cards
    
    print(f"手牌: {cards_to_string(hole_cards)}")
    print(f"公共牌: {cards_to_string(community_cards)}")
    
    best = best_hand(all_cards)
    print(f"最佳组合: {best}")
    print(f"牌型: {best.get_rank_name()}")


def example_5_probability_info():
    """示例5：牌型概率信息"""
    print_separator("示例5：牌型概率")
    
    print("各牌型在5张随机牌中出现的概率:")
    print("-" * 50)
    print(f"{'牌型':<12} {'概率':<12} {'组合数':<12}")
    print("-" * 50)
    
    for rank in HandRank:
        prob = hand_probability(rank)
        count = hand_combinations_count(rank)
        print(f"{HAND_RANK_NAMES[rank]:<12} {prob:>8.4f}% {count:>12,}")
    
    print("-" * 50)
    print(f"总组合数: {sum(hand_combinations_count(r) for r in HandRank):,}")


def example_6_game_simulation():
    """示例6：简单游戏模拟"""
    print_separator("示例6：游戏模拟")
    
    # 创建4人游戏
    game = PokerGame(num_players=4)
    game.new_round()
    
    print(f"开始新游戏，{game.num_players} 位玩家")
    
    # 发手牌
    game.deal_to_players(2)
    print("\n手牌已发放:")
    for i, hand in enumerate(game.hands):
        print(f"  玩家{i+1}: {cards_to_string(hand.cards)}")
    
    # 翻牌
    flop = game.flop()
    print(f"\n翻牌: {cards_to_string(flop)}")
    
    # 转牌
    turn = game.turn()
    print(f"转牌: {turn}")
    
    # 河牌
    river = game.river()
    print(f"河牌: {river}")
    
    print(f"\n公共牌: {cards_to_string(game.community_cards)}")
    
    # 判定胜负
    winner_idx, best_hands = game.get_winner()
    
    print("\n各玩家最佳手牌:")
    for i, hand in enumerate(best_hands):
        print(f"  玩家{i+1}: {hand} ({hand.get_rank_name()})")
    
    if winner_idx is not None:
        print(f"\n🏆 玩家{winner_idx + 1} 获胜!")
    else:
        print("\n平局!")


def example_7_card_utils():
    """示例7：牌工具函数"""
    print_separator("示例7：牌工具函数")
    
    # 创建一组牌
    cards = [
        Card(Suit.SPADES, Rank.ACE),
        Card(Suit.HEARTS, Rank.ACE),
        Card(Suit.DIAMONDS, Rank.ACE),
        Card(Suit.CLUBS, Rank.KING),
        Card(Suit.SPADES, Rank.KING),
    ]
    
    print(f"牌组: {cards_to_string(cards)}")
    
    # 统计牌面
    from mod import card_count_by_rank, card_count_by_suit
    rank_count = card_count_by_rank(cards)
    print(f"\n牌面统计: {dict((r.name, c) for r, c in rank_count.items())}")
    
    # 统计花色
    suit_count = card_count_by_suit(cards)
    print(f"花色统计: {dict((s.name, c) for s, c in suit_count.items())}")
    
    # 中英文显示
    print(f"\n英文显示: {cards_to_string(cards)}")
    print(f"中文显示: {cards_to_string(cards, chinese=True)}")


def example_8_wheel_straight():
    """示例8：轮子（A-2-3-4-5）顺子"""
    print_separator("示例8：特殊顺子 - 轮子")
    
    # A-2-3-4-5 顺子（轮子）
    wheel = Hand([
        Card(Suit.SPADES, Rank.ACE),
        Card(Suit.HEARTS, Rank.TWO),
        Card(Suit.DIAMONDS, Rank.THREE),
        Card(Suit.CLUBS, Rank.FOUR),
        Card(Suit.SPADES, Rank.FIVE),
    ])
    
    print(f"手牌: {cards_to_string(wheel.cards)}")
    print(f"牌型: {wheel.get_rank_name()}")
    
    rank, values = wheel.evaluate()
    print(f"最高牌: {Rank(values[0]).name} (A作为1使用)")
    
    # 与普通顺子比较
    normal_straight = Hand([
        Card(Suit.SPADES, Rank.SIX),
        Card(Suit.HEARTS, Rank.FIVE),
        Card(Suit.DIAMONDS, Rank.FOUR),
        Card(Suit.CLUBS, Rank.THREE),
        Card(Suit.SPADES, Rank.TWO),
    ])
    
    print(f"\n普通顺子: {cards_to_string(normal_straight.cards)}")
    
    # 比较结果
    if normal_straight > wheel:
        print("普通顺子(6高) > 轮子(5高)")


def main():
    """运行所有示例"""
    example_1_basic_operations()
    example_2_hand_evaluation()
    example_3_hand_comparison()
    example_4_best_hand_selection()
    example_5_probability_info()
    example_6_game_simulation()
    example_7_card_utils()
    example_8_wheel_straight()
    
    print("\n" + "="*50)
    print("  所有示例运行完成!")
    print("="*50)


if __name__ == "__main__":
    main()