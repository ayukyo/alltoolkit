/**
 * Poker Utils 使用示例
 * 
 * 本文件展示扑克牌工具的各种使用场景
 */

package poker_utils

fun main() {
    println("=" .repeat(60))
    println("扑克牌工具 - Poker Utils 示例")
    println("=".repeat(60))
    println()
    
    // ========== 示例1: 创建和洗牌 ==========
    println("【示例1】创建和洗牌")
    println("-".repeat(40))
    
    val deck = createDeck()
    println("标准牌组: ${deck.size}张牌")
    println("原始顺序: ${deck.take(5).joinToString(" ")} ...")
    
    val shuffled = shuffleDeck(deck, seed = 42)
    println("洗牌后: ${shuffled.take(5).joinToString(" ")} ...")
    println()
    
    // ========== 示例2: 发牌 ==========
    println("【示例2】德州扑克发牌")
    println("-".repeat(40))
    
    val gameDeck = shuffleDeck(createDeck(), seed = 12345)
    val (hands, remaining) = dealTexasHoldem(gameDeck, numPlayers = 4)
    
    hands.forEachIndexed { i, hand ->
        println("玩家${i + 1}: ${hand.joinToString(" ")}")
    }
    println("剩余: ${remaining.size}张")
    println()
    
    // ========== 示例3: 牌型评估 ==========
    println("【示例3】牌型评估")
    println("-".repeat(40))
    
    val testHands = mapOf(
        "高牌" to parseCards("♠A ♥K ♦Q ♣J ♠9"),
        "一对" to parseCards("♠A ♥A ♦K ♣Q ♠J"),
        "两对" to parseCards("♠A ♥A ♦K ♣K ♠Q"),
        "三条" to parseCards("♠K ♥K ♦K ♣Q ♠J"),
        "顺子" to parseCards("♠5 ♥6 ♦7 ♣8 ♠9"),
        "同花" to parseCards("♠A ♠K ♠Q ♠J ♠9"),
        "葫芦" to parseCards("♠A ♥A ♦A ♣K ♠K"),
        "四条" to parseCards("♠8 ♥8 ♦8 ♣8 ♠K"),
        "同花顺" to parseCards("♠5 ♠6 ♠7 ♠8 ♠9"),
        "皇家同花顺" to parseCards("♠10 ♠J ♠Q ♠K ♠A")
    )
    
    testHands.forEach { (name, cards) ->
        val eval = evaluateHand(cards)
        println("$name: ${cards.joinToString(" ")} → ${eval.describe()}")
    }
    println()
    
    // ========== 示例4: 手牌比较 ==========
    println("【示例4】手牌比较")
    println("-".repeat(40))
    
    val playerHands = mapOf(
        "Alice" to parseCards("♠A ♥A ♦K ♣Q ♠J"),
        "Bob" to parseCards("♠K ♥K ♦K ♣Q ♠J"),
        "Charlie" to parseCards("♠A ♥A ♦A ♣Q ♠J")
    )
    
    playerHands.forEach { (name, cards) ->
        val eval = evaluateHand(cards)
        println("$name: ${cards.joinToString(" ")} → ${eval.describe()}")
    }
    
    val winners = findWinners(playerHands)
    println("\n获胜者: ${winners.joinToString(", ") { "${it.first} (${it.second.describe()})" }}")
    println()
    
    // ========== 示例5: 德州扑克模拟 ==========
    println("【示例5】德州扑克完整局模拟")
    println("-".repeat(40))
    
    val result = simulateTexasHoldem(numPlayers = 4, seed = 98765)
    println(result.describe())
    
    // 计算每个玩家的最佳牌型
    println("最终牌型评估:")
    result.hands.forEachIndexed { i, hand ->
        val allCards = hand + result.communityCards
        val eval = evaluateHand(allCards)
        println("  玩家${i + 1}: ${eval.describe()}")
    }
    println()
    
    // ========== 示例6: 概率计算 ==========
    println("【示例6】德州扑克概率计算")
    println("-".repeat(40))
    
    // 同花听牌场景
    println("场景: 同花听牌")
    println("  已知牌: 2张同花底牌 + 2张同花公共牌")
    println("  剩余同花牌: 9张")
    println()
    
    val outs = 9
    val prob = calculateOutsProbability(outs)
    println("  出牌数: $outs 张")
    println("  成功概率: ${(prob * 100).format(1)}%")
    println()
    
    // 底池赔率计算
    val potSize = 100.0
    val callAmount = 20.0
    val potOdds = calculatePotOdds(potSize, callAmount)
    println("底池赔率计算:")
    println("  底池: \$$potSize")
    println("  跟注: \$$callAmount")
    println("  底池赔率: ${potOdds}:1")
    println("  是否值得跟注: ${if (shouldCall(outs, potOdds)) "是" else "否"}")
    println()
    
    // ========== 示例7: 牌组操作 ==========
    println("【示例7】牌组操作工具")
    println("-".repeat(40))
    
    // 解析牌
    val parsedCards = parseCards("♠A ♥K ♦Q ♣J ♠10")
    println("解析字符串: \"♠A ♥K ♦Q ♣J ♠10\"")
    println("结果: ${parsedCards.joinToString(" ")}")
    
    // 牌组哈希
    val cards1 = parseCards("♠A ♥K ♦Q")
    val cards2 = parseCards("♦Q ♠A ♥K")  // 不同顺序
    println("\n牌组哈希测试:")
    println("  牌组1: ${cards1.joinToString(" ")}")
    println("  牌组2: ${cards2.joinToString(" ")}")
    println("  哈希相同: ${cardsHash(cards1) == cardsHash(cards2)}")
    
    // 牌信息
    val card = Card(Suit.SPADES, Rank.ACE)
    println("\n牌信息:")
    println("  简写: ${card}")  // ♠A
    println("  全名: ${card.toFullString()}")  // 黑桃尖
    println("  花色: ${card.suit.name_zh} (${card.suit.name})")
    println("  点数: ${card.rank.name_zh} (值: ${card.rank.value})")
    println()
    
    // ========== 示例8: 发牌游戏变体 ==========
    println("【示例8】不同扑克变体发牌")
    println("-".repeat(40))
    
    // Omaha 发牌（每人4张）
    val omahaDeck = shuffleDeck(createDeck(), seed = 11111)
    val (omahaHands, omahaRemaining) = dealCards(omahaDeck, numHands = 4, cardsPerHand = 4)
    println("Omaha 发牌（每人4张）:")
    omahaHands.forEachIndexed { i, hand ->
        println("  玩家${i + 1}: ${hand.joinToString(" ")}")
    }
    println("  剩余: ${omahaRemaining.size}张")
    println()
    
    // 5 Card Draw 发牌（每人5张）
    val drawDeck = shuffleDeck(createDeck(), seed = 22222)
    val (drawHands, drawRemaining) = dealCards(drawDeck, numHands = 4, cardsPerHand = 5)
    println("5 Card Draw 发牌（每人5张）:")
    drawHands.forEachIndexed { i, hand ->
        val eval = evaluateHand(hand)
        println("  玩家${i + 1}: ${hand.joinToString(" ")} → ${eval.describe()}")
    }
    println("  剩余: ${drawRemaining.size}张")
    println()
    
    // ========== 示例9: 花色和点数枚举 ==========
    println("【示例9】花色和点数枚举")
    println("-".repeat(40))
    
    println("花色:")
    Suit.values().forEach { suit ->
        println("  ${suit.symbol} ${suit.name_zh} (${suit.name})")
    }
    
    println("\n点数:")
    Rank.values().forEach { rank ->
        println("  ${rank.symbol} ${rank.name_zh} (值: ${rank.value})")
    }
    println()
    
    // ========== 示例10: 牌型优先级 ==========
    println("【示例10】牌型优先级（从小到大）")
    println("-".repeat(40))
    
    HandRank.values().forEachIndexed { i, rank ->
        println("  ${i + 1}. ${rank.name_zh} (${rank.name_en})")
    }
    println()
    
    println("=" .repeat(60))
    println("示例完成!")
    println("=".repeat(60))
}

/**
 * 格式化浮点数
 */
fun Double.format(decimals: Int): String {
    var multiplier = 1.0
    repeat(decimals) { multiplier *= 10 }
    return ((this * multiplier).toInt() / multiplier).toString()
}