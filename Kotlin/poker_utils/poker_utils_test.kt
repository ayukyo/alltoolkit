/**
 * Poker Utils 测试套件
 * 纯 Kotlin 标准库实现，零外部依赖
 */

package poker_utils

/**
 * 运行所有测试
 */
fun runTests() {
    println("=== Poker Utils 测试套件 ===\n")
    
    var passed = 0
    var failed = 0
    val results = mutableListOf<String>()
    
    // ==================== 牌组测试 ====================
    
    runCatching {
        // testCreateDeck
        val deck = createDeck()
        assert(deck.size == 52) { "标准牌组应有52张牌" }
        assert(deck.toSet().size == 52) { "所有牌应唯一" }
        Suit.values().forEach { suit ->
            assert(deck.count { it.suit == suit } == 13) { "${suit.name_zh}应有13张牌" }
        }
        results.add("✓ testCreateDeck")
        passed++
    }.onFailure {
        results.add("✗ testCreateDeck: ${it.message}")
        failed++
    }
    
    runCatching {
        // testShuffleDeck
        val deck = createDeck()
        val shuffled = shuffleDeck(deck)
        assert(shuffled.size == 52) { "洗牌后牌数不变" }
        assert(deck.toSet() == shuffled.toSet()) { "洗牌后牌的内容相同" }
        results.add("✓ testShuffleDeck")
        passed++
    }.onFailure {
        results.add("✗ testShuffleDeck: ${it.message}")
        failed++
    }
    
    runCatching {
        // testShuffleDeckWithSeed
        val deck = createDeck()
        val shuffled1 = shuffleDeck(deck, seed = 12345)
        val shuffled2 = shuffleDeck(deck, seed = 12345)
        assert(shuffled1 == shuffled2) { "相同种子应产生相同洗牌结果" }
        results.add("✓ testShuffleDeckWithSeed")
        passed++
    }.onFailure {
        results.add("✗ testShuffleDeckWithSeed: ${it.message}")
        failed++
    }
    
    runCatching {
        // testDealCards
        val deck = shuffleDeck(createDeck(), seed = 42)
        val (hands, remaining) = dealCards(deck, numHands = 4, cardsPerHand = 5)
        assert(hands.size == 4) { "应发4手牌" }
        hands.forEach { hand ->
            assert(hand.size == 5) { "每手牌应有5张" }
        }
        assert(remaining.size == 32) { "应剩32张牌" }
        results.add("✓ testDealCards")
        passed++
    }.onFailure {
        results.add("✗ testDealCards: ${it.message}")
        failed++
    }
    
    runCatching {
        // testDealTexasHoldem
        val deck = shuffleDeck(createDeck(), seed = 42)
        val (hands, remaining) = dealTexasHoldem(deck, numPlayers = 6)
        assert(hands.size == 6) { "应有6位玩家" }
        hands.forEach { hand ->
            assert(hand.size == 2) { "德州扑克每人2张底牌" }
        }
        assert(remaining.size == 40) { "应剩40张牌" }
        results.add("✓ testDealTexasHoldem")
        passed++
    }.onFailure {
        results.add("✗ testDealTexasHoldem: ${it.message}")
        failed++
    }
    
    // ==================== 牌型评估测试 ====================
    
    runCatching {
        // testEvaluateHighCard
        val cards = parseCards("♠A ♥K ♦Q ♣J ♠9")
        val eval = evaluateHand(cards)
        assert(eval.rank == HandRank.HIGH_CARD) { "应为高牌" }
        results.add("✓ testEvaluateHighCard")
        passed++
    }.onFailure {
        results.add("✗ testEvaluateHighCard: ${it.message}")
        failed++
    }
    
    runCatching {
        // testEvaluateOnePair
        val cards = parseCards("♠A ♥A ♦K ♣Q ♠J")
        val eval = evaluateHand(cards)
        assert(eval.rank == HandRank.ONE_PAIR) { "应为一对" }
        results.add("✓ testEvaluateOnePair")
        passed++
    }.onFailure {
        results.add("✗ testEvaluateOnePair: ${it.message}")
        failed++
    }
    
    runCatching {
        // testEvaluateTwoPair
        val cards = parseCards("♠A ♥A ♦K ♣K ♠Q")
        val eval = evaluateHand(cards)
        assert(eval.rank == HandRank.TWO_PAIR) { "应为两对" }
        results.add("✓ testEvaluateTwoPair")
        passed++
    }.onFailure {
        results.add("✗ testEvaluateTwoPair: ${it.message}")
        failed++
    }
    
    runCatching {
        // testEvaluateThreeOfAKind
        val cards = parseCards("♠A ♥A ♦A ♣K ♠Q")
        val eval = evaluateHand(cards)
        assert(eval.rank == HandRank.THREE_OF_A_KIND) { "应为三条" }
        results.add("✓ testEvaluateThreeOfAKind")
        passed++
    }.onFailure {
        results.add("✗ testEvaluateThreeOfAKind: ${it.message}")
        failed++
    }
    
    runCatching {
        // testEvaluateStraight
        val cards = parseCards("♠5 ♥6 ♦7 ♣8 ♠9")
        val eval = evaluateHand(cards)
        assert(eval.rank == HandRank.STRAIGHT) { "应为顺子" }
        results.add("✓ testEvaluateStraight")
        passed++
    }.onFailure {
        results.add("✗ testEvaluateStraight: ${it.message}")
        failed++
    }
    
    runCatching {
        // testEvaluateStraightWithWheel (A-2-3-4-5)
        val cards = parseCards("♠A ♥2 ♦3 ♣4 ♠5")
        val eval = evaluateHand(cards)
        assert(eval.rank == HandRank.STRAIGHT) { "应为顺子" }
        assert(eval.kickers[0] == 5) { "轮子的高牌应为5" }
        results.add("✓ testEvaluateStraightWithWheel")
        passed++
    }.onFailure {
        results.add("✗ testEvaluateStraightWithWheel: ${it.message}")
        failed++
    }
    
    runCatching {
        // testEvaluateFlush
        val cards = parseCards("♠A ♠K ♠Q ♠J ♠9")
        val eval = evaluateHand(cards)
        assert(eval.rank == HandRank.FLUSH) { "应为同花" }
        results.add("✓ testEvaluateFlush")
        passed++
    }.onFailure {
        results.add("✗ testEvaluateFlush: ${it.message}")
        failed++
    }
    
    runCatching {
        // testEvaluateFullHouse
        val cards = parseCards("♠A ♥A ♦A ♣K ♠K")
        val eval = evaluateHand(cards)
        assert(eval.rank == HandRank.FULL_HOUSE) { "应为葫芦" }
        results.add("✓ testEvaluateFullHouse")
        passed++
    }.onFailure {
        results.add("✗ testEvaluateFullHouse: ${it.message}")
        failed++
    }
    
    runCatching {
        // testEvaluateFourOfAKind
        val cards = parseCards("♠A ♥A ♦A ♣A ♠K")
        val eval = evaluateHand(cards)
        assert(eval.rank == HandRank.FOUR_OF_A_KIND) { "应为四条" }
        results.add("✓ testEvaluateFourOfAKind")
        passed++
    }.onFailure {
        results.add("✗ testEvaluateFourOfAKind: ${it.message}")
        failed++
    }
    
    runCatching {
        // testEvaluateStraightFlush
        val cards = parseCards("♠5 ♠6 ♠7 ♠8 ♠9")
        val eval = evaluateHand(cards)
        assert(eval.rank == HandRank.STRAIGHT_FLUSH) { "应为同花顺" }
        results.add("✓ testEvaluateStraightFlush")
        passed++
    }.onFailure {
        results.add("✗ testEvaluateStraightFlush: ${it.message}")
        failed++
    }
    
    runCatching {
        // testEvaluateRoyalFlush
        val cards = parseCards("♠10 ♠J ♠Q ♠K ♠A")
        val eval = evaluateHand(cards)
        assert(eval.rank == HandRank.ROYAL_FLUSH) { "应为皇家同花顺" }
        results.add("✓ testEvaluateRoyalFlush")
        passed++
    }.onFailure {
        results.add("✗ testEvaluateRoyalFlush: ${it.message}")
        failed++
    }
    
    // ==================== 手牌比较测试 ====================
    
    runCatching {
        // testCompareHandsWithDifferentRanks
        val pairHand = parseCards("♠A ♥A ♦K ♣Q ♠J")
        val twoPairHand = parseCards("♠A ♥A ♦K ♣K ♠J")
        assert(compareHands(pairHand, twoPairHand) == -1) { "两对应胜过一对" }
        results.add("✓ testCompareHandsWithDifferentRanks")
        passed++
    }.onFailure {
        results.add("✗ testCompareHandsWithDifferentRanks: ${it.message}")
        failed++
    }
    
    runCatching {
        // testCompareHandsWithSameRank
        val higherPair = parseCards("♠K ♥K ♦Q ♣J ♠9")
        val lowerPair = parseCards("♠J ♥J ♦A ♣K ♠Q")
        assert(compareHands(higherPair, lowerPair) == 1) { "对K应胜过对J" }
        results.add("✓ testCompareHandsWithSameRank")
        passed++
    }.onFailure {
        results.add("✗ testCompareHandsWithSameRank: ${it.message}")
        failed++
    }
    
    runCatching {
        // testCompareEqualHands
        val hand1 = parseCards("♠A ♥K ♦Q ♣J ♠9")
        val hand2 = parseCards("♥A ♦K ♣Q ♠J ♦9")
        assert(compareHands(hand1, hand2) == 0) { "相同牌型应平局" }
        results.add("✓ testCompareEqualHands")
        passed++
    }.onFailure {
        results.add("✗ testCompareEqualHands: ${it.message}")
        failed++
    }
    
    runCatching {
        // testFindWinners
        val hands = mapOf(
            "Player1" to parseCards("♠A ♥A ♦K ♣Q ♠J"),
            "Player2" to parseCards("♠K ♥K ♦K ♣Q ♠J"),
            "Player3" to parseCards("♠A ♥A ♦A ♣Q ♠J")
        )
        val winners = findWinners(hands)
        assert(winners.size == 1) { "应只有1个获胜者" }
        assert(winners[0].first == "Player3") { "获胜者应为Player3" }
        assert(winners[0].second.rank == HandRank.THREE_OF_A_KIND) { "应为三条" }
        results.add("✓ testFindWinners")
        passed++
    }.onFailure {
        results.add("✗ testFindWinners: ${it.message}")
        failed++
    }
    
    // ==================== 多牌评估测试 ====================
    
    runCatching {
        // testEvaluateMoreThanFiveCards
        val holeCards = parseCards("♠A ♥K")
        val communityCards = parseCards("♦A ♣K ♠Q ♦J ♣10")
        val allCards = holeCards + communityCards
        val eval = evaluateHand(allCards)
        assert(eval.rank == HandRank.TWO_PAIR) { "应为两对" }
        results.add("✓ testEvaluateMoreThanFiveCards")
        passed++
    }.onFailure {
        results.add("✗ testEvaluateMoreThanFiveCards: ${it.message}")
        failed++
    }
    
    runCatching {
        // testBestHandSelection
        val cards = parseCards("♠A ♥A ♦A ♣K ♠K ♥Q")
        val eval = evaluateHand(cards)
        assert(eval.rank == HandRank.FULL_HOUSE) { "应为葫芦（最佳组合）" }
        results.add("✓ testBestHandSelection")
        passed++
    }.onFailure {
        results.add("✗ testBestHandSelection: ${it.message}")
        failed++
    }
    
    // ==================== 概率计算测试 ====================
    
    runCatching {
        // testCalculateOutsProbability
        val prob = calculateOutsProbability(9, 47)
        assert(prob in 0.3..0.4) { "9出牌概率应在30%-40%之间" }
        results.add("✓ testCalculateOutsProbability")
        passed++
    }.onFailure {
        results.add("✗ testCalculateOutsProbability: ${it.message}")
        failed++
    }
    
    runCatching {
        // testCalculatePotOdds
        val odds = calculatePotOdds(100.0, 20.0)
        assert(odds == 5.0) { "底池赔率应为5:1" }
        results.add("✓ testCalculatePotOdds")
        passed++
    }.onFailure {
        results.add("✗ testCalculatePotOdds: ${it.message}")
        failed++
    }
    
    runCatching {
        // testShouldCall
        assert(shouldCall(9, 5.0)) { "9出牌应跟注" }
        assert(!shouldCall(2, 5.0)) { "2出牌不应跟注" }
        results.add("✓ testShouldCall")
        passed++
    }.onFailure {
        results.add("✗ testShouldCall: ${it.message}")
        failed++
    }
    
    // ==================== 解析测试 ====================
    
    runCatching {
        // testParseCard
        assert(parseCard("♠A") == Card(Suit.SPADES, Rank.ACE))
        assert(parseCard("♥K") == Card(Suit.HEARTS, Rank.KING))
        assert(parseCard("♦Q") == Card(Suit.DIAMONDS, Rank.QUEEN))
        assert(parseCard("♣J") == Card(Suit.CLUBS, Rank.JACK))
        assert(parseCard("黑桃A") == Card(Suit.SPADES, Rank.ACE))
        assert(parseCard("红心K") == Card(Suit.HEARTS, Rank.KING))
        results.add("✓ testParseCard")
        passed++
    }.onFailure {
        results.add("✗ testParseCard: ${it.message}")
        failed++
    }
    
    runCatching {
        // testParseCards
        val cards = parseCards("♠A ♥K ♦Q ♣J ♠10")
        assert(cards.size == 5)
        assert(cards[0].rank == Rank.ACE)
        assert(cards[1].rank == Rank.KING)
        assert(cards[2].rank == Rank.QUEEN)
        results.add("✓ testParseCards")
        passed++
    }.onFailure {
        results.add("✗ testParseCards: ${it.message}")
        failed++
    }
    
    // ==================== 游戏模拟测试 ====================
    
    runCatching {
        // testSimulateTexasHoldem
        val result = simulateTexasHoldem(numPlayers = 4, seed = 42)
        assert(result.hands.size == 4)
        assert(result.flop.size == 3)
        assert(result.communityCards.size == 5)
        results.add("✓ testSimulateTexasHoldem")
        passed++
    }.onFailure {
        results.add("✗ testSimulateTexasHoldem: ${it.message}")
        failed++
    }
    
    // ==================== 辅助工具测试 ====================
    
    runCatching {
        // testCardsHash
        val cards1 = parseCards("♠A ♥K ♦Q")
        val cards2 = parseCards("♦Q ♠A ♥K")
        assert(cardsHash(cards1) == cardsHash(cards2)) { "相同牌组应有相同哈希" }
        results.add("✓ testCardsHash")
        passed++
    }.onFailure {
        results.add("✗ testCardsHash: ${it.message}")
        failed++
    }
    
    runCatching {
        // testCardToString
        val card = Card(Suit.SPADES, Rank.ACE)
        assert(card.toString() == "♠A")
        assert(card.toFullString() == "黑桃尖")
        results.add("✓ testCardToString")
        passed++
    }.onFailure {
        results.add("✗ testCardToString: ${it.message}")
        failed++
    }
    
    runCatching {
        // testSuitFromSymbol
        assert(Suit.fromSymbol("♠") == Suit.SPADES)
        assert(Suit.fromSymbol("♥") == Suit.HEARTS)
        assert(Suit.fromSymbol("♦") == Suit.DIAMONDS)
        assert(Suit.fromSymbol("♣") == Suit.CLUBS)
        assert(Suit.fromSymbol("X") == null)
        results.add("✓ testSuitFromSymbol")
        passed++
    }.onFailure {
        results.add("✗ testSuitFromSymbol: ${it.message}")
        failed++
    }
    
    runCatching {
        // testRankFromValue
        assert(Rank.fromValue(2) == Rank.TWO)
        assert(Rank.fromValue(14) == Rank.ACE)
        assert(Rank.fromValue(11) == Rank.JACK)
        assert(Rank.fromValue(15) == null)
        results.add("✓ testRankFromValue")
        passed++
    }.onFailure {
        results.add("✗ testRankFromValue: ${it.message}")
        failed++
    }
    
    // 输出结果
    results.forEach { println(it) }
    
    println("\n=== 测试结果 ===")
    println("通过: $passed")
    println("失败: $failed")
    println("总计: ${passed + failed}")
    
    if (failed == 0) {
        println("\n✅ 所有测试通过！")
    } else {
        println("\n❌ 有 $failed 个测试失败")
    }
}

fun main() {
    runTests()
}