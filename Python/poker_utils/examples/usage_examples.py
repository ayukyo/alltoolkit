"""
扑克牌工具使用示例
==================

本示例展示 poker_utils 模块的主要功能：
1. 创建和管理扑克牌组
2. 手牌评估和比较
3. 德州扑克相关计算
4. 胜率模拟
"""

import sys
sys.path.insert(0, '..')

from mod import (
    Card, Deck, Suit, Rank, HandRank,
    PokerEvaluator, TexasHoldem, HandAnalyzer,
    create_deck, parse_cards, cards_to_str,
    evaluate_hand, compare_hands, get_hand_rank_name,
    simulate_win_rate, is_pocket_pair, is_suited,
    is_connected, get_starting_hand_strength,
    SUIT_SYMBOLS, RANK_SYMBOLS, HAND_RANK_NAMES
)


def example_1_basic_operations():
    """示例1: 基本扑克牌操作"""
    print("=" * 60)
    print("示例1: 基本扑克牌操作")
    print("=" * 60)
    
    # 创建扑克牌
    ace_spades = Card(rank=Rank.ACE, suit=Suit.SPADES)
    king_hearts = Card(rank=Rank.KING, suit=Suit.HEARTS)
    
    print(f"创建扑克牌: {ace_spades}, {king_hearts}")
    
    # 从字符串解析
    card = Card.from_str("As")  # 黑桃A
    print(f"从字符串解析: 'As' -> {card}")
    
    # 创建牌组
    deck = create_deck(shuffled=True)
    print(f"\n牌组创建完成，共 {len(deck)} 张牌")
    
    # 发牌
    hand = deck.deal(5)
    print(f"发5张牌: {cards_to_str(hand)}")
    print(f"牌组剩余: {len(deck)} 张")
    
    print()


def example_2_hand_evaluation():
    """示例2: 牌型评估"""
    print("=" * 60)
    print("示例2: 牌型评估")
    print("=" * 60)
    
    # 各种牌型示例
    hands = {
        "皇家同花顺": "As Ks Qs Js Ts",
        "同花顺": "9s 8s 7s 6s 5s",
        "四条": "As Ah Ad Ac 2h",
        "葫芦": "As Ah Ad Ks Kh",
        "同花": "As 9s 7s 4s 2s",
        "顺子": "9s 8h 7d 6c 5s",
        "轮子(最小顺子)": "As 2h 3d 4c 5s",
        "三条": "As Ah Ad 9c 5s",
        "两对": "As Ah Kd Kc 5s",
        "一对": "As Ah 9d 7c 5s",
        "高牌": "As 9h 7d 5c 3s",
    }
    
    for name, cards_str in hands.items():
        cards = parse_cards(cards_str)
        hand = evaluate_hand(cards)
        description = PokerEvaluator.get_hand_description(hand)
        print(f"{name:15s}: {cards_str:20s} -> {description}")
    
    print()


def example_3_hand_comparison():
    """示例3: 牌型比较"""
    print("=" * 60)
    print("示例3: 牌型比较")
    print("=" * 60)
    
    # 比较不同的牌
    match-ups = [
        ("同花顺 vs 四条", "9s 8s 7s 6s 5s", "As Ah Ad Ac 2h"),
        ("四条A vs 四条K", "As Ah Ad Ac 2h", "Ks Kh Kd Kc Ah"),
        ("葫芦A-K vs 葫芦A-Q", "As Ah Ad Ks Kh", "Ac Ah Ad Qs Qh"),
        ("两对A-K vs 两对A-Q", "As Ah Ks Kh 9c", "Ac Ad Qs Qh 9c"),
        ("一对A-K vs 一对A-Q", "As Ah Kc 9d 5s", "Ac Ad Qc 9d 5s"),
    ]
    
    for name, cards1_str, cards2_str in match_ups:
        cards1 = parse_cards(cards1_str)
        cards2 = parse_cards(cards2_str)
        result = compare_hands(cards1, cards2)
        
        winner = "左边胜" if result > 0 else "右边胜" if result < 0 else "平局"
        hand1 = evaluate_hand(cards1)
        hand2 = evaluate_hand(cards2)
        
        print(f"{name}")
        print(f"  左: {get_hand_rank_name(hand1)} ({cards1_str})")
        print(f"  右: {get_hand_rank_name(hand2)} ({cards2_str})")
        print(f"  结果: {winner}")
        print()
    
    print()


def example_4_texas_holdem():
    """示例4: 德州扑克分析"""
    print("=" * 60)
    print("示例4: 德州扑克分析")
    print("=" * 60)
    
    # 底牌和公共牌
    hole_cards = parse_cards("As Ah")
    flop = parse_cards("Ad 9c 5s")
    
    print(f"底牌: {cards_to_str(hole_cards)}")
    print(f"翻牌: {cards_to_str(flop)}")
    
    # 评估当前牌型
    hand = TexasHoldem.evaluate_hand(hole_cards, flop)
    print(f"当前牌型: {PokerEvaluator.get_hand_description(hand)}")
    
    # 计算补牌（达到四条需要的牌）
    outs_count = TexasHoldem.calculate_outs_count(hole_cards, flop, HandRank.FOUR_OF_A_KIND)
    print(f"四条补牌数: {outs_count}")
    
    # 起手牌分析
    print("\n起手牌分析:")
    hole_pairs = [
        ("AA", "As Ah"),
        ("AK同花", "As Ks"),
        ("AK不同花", "As Kh"),
        ("JJ", "Js Jh"),
        ("口袋对2", "2s 2h"),
        ("AX同花", "As 8s"),
        ("垃圾牌", "9s 3h"),
    ]
    
    for name, cards_str in hole_pairs:
        cards = parse_cards(cards_str)
        strength = get_starting_hand_strength(cards)
        print(f"  {name:10s}: {strength}")
    
    print()


def example_5_win_rate_simulation():
    """示例5: 胜率模拟"""
    print("=" * 60)
    print("示例5: 胜率模拟 (蒙特卡洛)")
    print("=" * 60)
    
    scenarios = [
        ("AA", "As Ah"),
        ("KK", "Ks Kh"),
        ("AK同花", "As Ks"),
        ("AK不同花", "As Kh"),
        ("口袋对中等", "8s 8h"),
        ("AX同花", "As 9s"),
        ("垃圾牌", "7s 2h"),
    ]
    
    print("底牌 vs 随机牌 (模拟1000次)")
    print("-" * 40)
    
    for name, cards_str in scenarios:
        cards = parse_cards(cards_str)
        win_rate = simulate_win_rate(cards, simulations=1000)
        print(f"{name:12s}: {win_rate:.1%} 胜率")
    
    print()


def example_6_hand_analysis():
    """示例6: 手牌分析"""
    print("=" * 60)
    print("示例6: 手牌分析")
    print("=" * 60)
    
    # 分析可能的顺子
    cards = parse_cards("5s 6h 7d")
    possible_straights = HandAnalyzer.get_possible_straights(cards)
    
    print(f"手牌: {cards_to_str(cards)}")
    print("可能的顺子补牌:")
    rank_names = {
        Rank.TWO: '2', Rank.THREE: '3', Rank.FOUR: '4', Rank.FIVE: '5',
        Rank.SIX: '6', Rank.SEVEN: '7', Rank.EIGHT: '8', Rank.NINE: '9',
        Rank.TEN: 'T', Rank.JACK: 'J', Rank.QUEEN: 'Q', Rank.KING: 'K', Rank.ACE: 'A'
    }
    for missing in possible_straights[:5]:
        missing_str = ', '.join(rank_names.get(r, str(r)) for r in missing)
        print(f"  缺: {missing_str}")
    
    # 分析可能的同花
    print("\n可能的同花补牌:")
    cards = parse_cards("As 5s 9s")
    print(f"手牌: {cards_to_str(cards)}")
    possible_flushes = HandAnalyzer.get_possible_flushes(cards)
    
    suit_names = {Suit.SPADES: '黑桃', Suit.HEARTS: '红心', Suit.DIAMONDS: '方块', Suit.CLUBS: '梅花'}
    for suit, needed in possible_flushes:
        print(f"  {suit_names[suit]}: 还需要 {needed} 张")
    
    print()


def example_7_full_game_simulation():
    """示例7: 完整游戏模拟"""
    print("=" * 60)
    print("示例7: 德州扑克游戏模拟")
    print("=" * 60)
    
    # 创建牌组并洗牌
    deck = create_deck(shuffled=True)
    
    # 发给4个玩家
    num_players = 4
    players = []
    for i in range(num_players):
        hole = deck.deal(2)
        players.append(hole)
        print(f"玩家{i+1}: {cards_to_str(hole)}")
    
    print("\n公共牌:")
    # 翻牌 (3张)
    flop = deck.deal(3)
    print(f"翻牌: {cards_to_str(flop)}")
    
    # 转牌 (1张)
    turn = deck.deal(1)
    print(f"转牌: {cards_to_str(turn)}")
    
    # 河牌 (1张)
    river = deck.deal(1)
    print(f"河牌: {cards_to_str(river)}")
    
    # 公共牌
    board = flop + turn + river
    
    # 评估每个玩家
    print("\n最终牌型:")
    results = []
    for i, hole in enumerate(players):
        hand = TexasHoldem.evaluate_hand(hole, board)
        desc = PokerEvaluator.get_hand_description(hand)
        print(f"玩家{i+1}: {desc}")
        results.append((i + 1, hand))
    
    # 找出赢家
    results.sort(key=lambda x: x[1], reverse=True)
    winner = results[0]
    print(f"\n赢家: 玩家{winner[0]} ({PokerEvaluator.get_hand_description(winner[1])})")
    
    print()


def example_8_odds_and_ends():
    """示例8: 杂项功能"""
    print("=" * 60)
    print("示例8: 杂项功能")
    print("=" * 60)
    
    # 花色和点数符号
    print("花色符号:")
    for suit, symbol in SUIT_SYMBOLS.items():
        print(f"  {suit.name}: {symbol}")
    
    print("\n点数符号:")
    for rank, symbol in RANK_SYMBOLS.items():
        print(f"  {rank.name}: {symbol}")
    
    # 牌型判断工具
    print("\n底牌判断:")
    hands = [
        ("As Ah", "口袋对?"),
        ("As Ks", "同花?"),
        ("As Kh", "相连?"),
    ]
    
    for cards_str, question in hands:
        cards = parse_cards(cards_str)
        if "口袋" in question:
            result = is_pocket_pair(cards)
        elif "同花" in question:
            result = is_suited(cards)
        else:
            result = is_connected(cards, gap=1)
        print(f"  {cards_str}: {question} {result}")
    
    print()


def main():
    """运行所有示例"""
    example_1_basic_operations()
    example_2_hand_evaluation()
    example_3_hand_comparison()
    example_4_texas_holdem()
    example_5_win_rate_simulation()
    example_6_hand_analysis()
    example_7_full_game_simulation()
    example_8_odds_and_end()


if __name__ == '__main__':
    main()