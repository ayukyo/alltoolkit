/**
 * Poker Utils - 扑克牌工具模块
 * 
 * 功能：
 * - 创建和管理标准扑克牌组（52张）
 * - 洗牌和发牌
 * - 牌型评估（高牌到皇家同花顺）
 * - 手牌比较
 * - 扑克概率计算
 * 
 * 零外部依赖，纯 Kotlin 标准库实现
 */

package poker_utils

// ==================== 数据定义 ====================

/**
 * 花色枚举
 */
enum class Suit(val symbol: String, val name_zh: String) {
    SPADES("♠", "黑桃"),
    HEARTS("♥", "红心"),
    DIAMONDS("♦", "方块"),
    CLUBS("♣", "梅花");
    
    companion object {
        fun fromSymbol(symbol: String): Suit? = values().find { it.symbol == symbol }
    }
}

/**
 * 点数枚举（2-10, J, Q, K, A）
 */
enum class Rank(val value: Int, val symbol: String, val name_zh: String) {
    TWO(2, "2", "二"),
    THREE(3, "3", "三"),
    FOUR(4, "4", "四"),
    FIVE(5, "5", "五"),
    SIX(6, "6", "六"),
    SEVEN(7, "7", "七"),
    EIGHT(8, "8", "八"),
    NINE(9, "9", "九"),
    TEN(10, "10", "十"),
    JACK(11, "J", "钩"),
    QUEEN(12, "Q", "圈"),
    KING(13, "K", "凯"),
    ACE(14, "A", "尖");
    
    companion object {
        fun fromValue(value: Int): Rank? = values().find { it.value == value }
        fun fromSymbol(symbol: String): Rank? = values().find { it.symbol == symbol }
    }
}

/**
 * 扑克牌数据类
 */
data class Card(val suit: Suit, val rank: Rank) : Comparable<Card> {
    override fun toString(): String = "${suit.symbol}${rank.symbol}"
    
    override fun compareTo(other: Card): Int = this.rank.value.compareTo(other.rank.value)
    
    fun toFullString(): String = "${suit.name_zh}${rank.name_zh}"
}

/**
 * 牌型枚举（从小到大）
 */
enum class HandRank(val value: Int, val name_zh: String, val name_en: String) {
    HIGH_CARD(1, "高牌", "High Card"),
    ONE_PAIR(2, "一对", "One Pair"),
    TWO_PAIR(3, "两对", "Two Pair"),
    THREE_OF_A_KIND(4, "三条", "Three of a Kind"),
    STRAIGHT(5, "顺子", "Straight"),
    FLUSH(6, "同花", "Flush"),
    FULL_HOUSE(7, "葫芦", "Full House"),
    FOUR_OF_A_KIND(8, "四条", "Four of a Kind"),
    STRAIGHT_FLUSH(9, "同花顺", "Straight Flush"),
    ROYAL_FLUSH(10, "皇家同花顺", "Royal Flush");
}

/**
 * 手牌评估结果
 */
data class HandEvaluation(
    val rank: HandRank,
    val kickers: List<Int>,  // 用于比较的附加牌值
    val cards: List<Card>
) : Comparable<HandEvaluation> {
    
    override fun compareTo(other: HandEvaluation): Int {
        // 先比较牌型
        val rankCompare = this.rank.value.compareTo(other.rank.value)
        if (rankCompare != 0) return rankCompare
        
        // 牌型相同，比较踢脚牌
        for (i in 0 until minOf(kickers.size, other.kickers.size)) {
            val kickerCompare = this.kickers[i].compareTo(other.kickers[i])
            if (kickerCompare != 0) return kickerCompare
        }
        
        return 0
    }
    
    fun describe(): String {
        return "${rank.name_zh} (${rank.name_en})"
    }
}

// ==================== 牌组操作 ====================

/**
 * 创建标准52张牌组
 */
fun createDeck(): List<Card> {
    return Suit.values().flatMap { suit ->
        Rank.values().map { rank -> Card(suit, rank) }
    }
}

/**
 * 洗牌（Fisher-Yates 算法）
 */
fun shuffleDeck(deck: List<Card>, seed: Long? = null): List<Card> {
    val result = deck.toMutableList()
    val random = if (seed != null) java.util.Random(seed) else java.util.Random()
    
    for (i in result.size - 1 downTo 1) {
        val j = random.nextInt(i + 1)
        result[i] = result[j].also { result[j] = result[i] }
    }
    
    return result
}

/**
 * 发牌
 * @param deck 牌组
 * @param numHands 手牌数量
 * @param cardsPerHand 每手牌数量
 * @return Pair(手牌列表, 剩余牌)
 */
fun dealCards(deck: List<Card>, numHands: Int, cardsPerHand: Int): Pair<List<List<Card>>, List<Card>> {
    val hands = MutableList(numHands) { mutableListOf<Card>() }
    var cardIndex = 0
    
    for (round in 0 until cardsPerHand) {
        for (hand in 0 until numHands) {
            if (cardIndex < deck.size) {
                hands[hand].add(deck[cardIndex++])
            }
        }
    }
    
    return Pair(hands.map { it.toList() }, deck.drop(cardIndex))
}

/**
 * 发德州扑克手牌（每人2张）
 */
fun dealTexasHoldem(deck: List<Card>, numPlayers: Int): Pair<List<List<Card>>, List<Card>> {
    return dealCards(deck, numPlayers, 2)
}

// ==================== 牌型评估 ====================

/**
 * 评估一手牌（5张以上）
 * 支持 Texas Hold'em、Omaha 等变体
 */
fun evaluateHand(cards: List<Card>): HandEvaluation {
    if (cards.size < 5) {
        throw IllegalArgumentException("至少需要5张牌进行评估")
    }
    
    // 对于超过5张牌，找出最佳组合
    if (cards.size > 5) {
        return findBestHand(cards)
    }
    
    return evaluateFiveCards(cards)
}

/**
 * 从多于5张的牌中找出最佳手牌
 */
private fun findBestHand(cards: List<Card>): HandEvaluation {
    val combinations = generateCombinations(cards, 5)
    return combinations.map { evaluateFiveCards(it) }.maxOrNull()!!
}

/**
 * 生成组合
 */
private fun generateCombinations(cards: List<Card>, size: Int): List<List<Card>> {
    if (size == 0) return listOf(emptyList())
    if (cards.size < size) return emptyList()
    
    val result = mutableListOf<List<Card>>()
    
    for (i in cards.indices) {
        val rest = cards.drop(i + 1)
        for (combo in generateCombinations(rest, size - 1)) {
            result.add(listOf(cards[i]) + combo)
        }
    }
    
    return result
}

/**
 * 评估恰好5张牌
 */
private fun evaluateFiveCards(cards: List<Card>): HandEvaluation {
    val sortedCards = cards.sortedByDescending { it.rank.value }
    val suits = cards.map { it.suit }
    val ranks = cards.map { it.rank.value }
    
    val isFlush = suits.distinct().size == 1
    val sortedRanks = ranks.sorted()
    
    // 检查顺子（包括 A-2-3-4-5 特殊情况）
    val isStraight = when {
        sortedRanks == listOf(2, 3, 4, 5, 14) -> true  // A-2-3-4-5（轮子）
        sortedRanks.zipWithNext().all { (a, b) -> b - a == 1 } -> true
        else -> false
    }
    
    // 统计点数出现次数
    val rankCounts = ranks.groupingBy { it }.eachCount().values.sortedDescending()
    
    // 判断牌型
    return when {
        isFlush && isStraight && sortedRanks == listOf(10, 11, 12, 13, 14) -> 
            HandEvaluation(HandRank.ROYAL_FLUSH, listOf(14), sortedCards)
        
        isFlush && isStraight -> {
            val highCard = if (sortedRanks == listOf(2, 3, 4, 5, 14)) 5 else sortedRanks.max()!!
            HandEvaluation(HandRank.STRAIGHT_FLUSH, listOf(highCard), sortedCards)
        }
        
        rankCounts == listOf(4, 1) -> {
            val quadRank = ranks.groupBy { it }.entries.find { it.value.size == 4 }!!.key
            val kicker = ranks.find { it != quadRank }!!
            HandEvaluation(HandRank.FOUR_OF_A_KIND, listOf(quadRank, kicker), sortedCards)
        }
        
        rankCounts == listOf(3, 2) -> {
            val tripRank = ranks.groupBy { it }.entries.find { it.value.size == 3 }!!.key
            val pairRank = ranks.groupBy { it }.entries.find { it.value.size == 2 }!!.key
            HandEvaluation(HandRank.FULL_HOUSE, listOf(tripRank, pairRank), sortedCards)
        }
        
        isFlush -> HandEvaluation(HandRank.FLUSH, sortedRanks.sortedDescending(), sortedCards)
        
        isStraight -> {
            val highCard = if (sortedRanks == listOf(2, 3, 4, 5, 14)) 5 else sortedRanks.max()!!
            HandEvaluation(HandRank.STRAIGHT, listOf(highCard), sortedCards)
        }
        
        rankCounts == listOf(3, 1, 1) -> {
            val tripRank = ranks.groupBy { it }.entries.find { it.value.size == 3 }!!.key
            val kickers = ranks.filter { it != tripRank }.sortedDescending()
            HandEvaluation(HandRank.THREE_OF_A_KIND, listOf(tripRank) + kickers, sortedCards)
        }
        
        rankCounts == listOf(2, 2, 1) -> {
            val pairRanks = ranks.groupBy { it }.entries.filter { it.value.size == 2 }.map { it.key }.sortedDescending()
            val kicker = ranks.find { it !in pairRanks }!!
            HandEvaluation(HandRank.TWO_PAIR, pairRanks + listOf(kicker), sortedCards)
        }
        
        rankCounts == listOf(2, 1, 1, 1) -> {
            val pairRank = ranks.groupBy { it }.entries.find { it.value.size == 2 }!!.key
            val kickers = ranks.filter { it != pairRank }.sortedDescending()
            HandEvaluation(HandRank.ONE_PAIR, listOf(pairRank) + kickers, sortedCards)
        }
        
        else -> HandEvaluation(HandRank.HIGH_CARD, sortedRanks.sortedDescending(), sortedCards)
    }
}

// ==================== 手牌比较 ====================

/**
 * 比较两手牌
 * @return 1表示hand1赢，-1表示hand2赢，0表示平局
 */
fun compareHands(hand1: List<Card>, hand2: List<Card>): Int {
    val eval1 = evaluateHand(hand1)
    val eval2 = evaluateHand(hand2)
    return eval1.compareTo(eval2)
}

/**
 * 从多手牌中找出赢家
 */
fun findWinners(hands: Map<String, List<Card>>): List<Pair<String, HandEvaluation>> {
    val evaluations = hands.map { (name, cards) -> name to evaluateHand(cards) }
    val maxEval = evaluations.maxByOrNull { it.second }!!.second
    
    return evaluations.filter { it.second == maxEval }
}

// ==================== 概率计算 ====================

/**
 * 计算德州扑克出牌概率（简化版）
 * @param outs 出牌数（能让你赢的牌数）
 * @param remainingCards 剩余牌数（默认47张，翻牌后）
 * @return 成功概率（0.0-1.0）
 */
fun calculateOutsProbability(outs: Int, remainingCards: Int = 47): Double {
    return 1.0 - Math.pow((remainingCards - outs).toDouble() / remainingCards, 2.0)
}

/**
 * 计算德州扑克底池赔率
 * @param potSize 底池大小
 * @param callAmount 跟注金额
 * @return 底池赔率（如 3.0 表示 3:1）
 */
fun calculatePotOdds(potSize: Double, callAmount: Double): Double {
    return potSize / callAmount
}

/**
 * 判断是否值得跟注
 * @param outs 出牌数
 * @param potOdds 底池赔率
 * @return 是否值得跟注
 */
fun shouldCall(outs: Int, potOdds: Double): Boolean {
    val winProbability = calculateOutsProbability(outs)
    val requiredProbability = 1.0 / (potOdds + 1.0)
    return winProbability > requiredProbability
}

// ==================== 辅助工具 ====================

/**
 * 解析扑克牌字符串
 * 支持格式: "♠A", "♥K", "♦Q", "♣J", "黑桃A", "红心K" 等
 */
fun parseCard(str: String): Card? {
    if (str.length < 2) return null
    
    return when {
        str.startsWith("黑桃") -> Suit.SPADES to str.substring(2)
        str.startsWith("红心") -> Suit.HEARTS to str.substring(2)
        str.startsWith("方块") -> Suit.DIAMONDS to str.substring(2)
        str.startsWith("梅花") -> Suit.CLUBS to str.substring(2)
        else -> {
            val suit = Suit.fromSymbol(str.substring(0, 1)) ?: return null
            suit to str.substring(1)
        }
    }.let { (suit, rankStr) ->
        val rank = Rank.fromSymbol(rankStr) ?: return null
        Card(suit, rank)
    }
}

/**
 * 解析多张扑克牌
 */
fun parseCards(str: String): List<Card> {
    return str.split(Regex("[,\\s]+"))
        .filter { it.isNotBlank() }
        .mapNotNull { parseCard(it.trim()) }
}

/**
 * 牌组转字符串
 */
fun deckToString(cards: List<Card>): String {
    return cards.joinToString(" ")
}

/**
 * 计算牌组哈希（用于去重）
 */
fun cardsHash(cards: List<Card>): String {
    return cards.sortedBy { it.suit.ordinal * 100 + it.rank.value }
        .joinToString("-") { "${it.suit.ordinal}${it.rank.value}" }
}

// ==================== 游戏辅助 ====================

/**
 * 生成德州扑克公共牌（翻牌、转牌、河牌）
 */
fun dealCommunityCards(deck: List<Card>, count: Int): Pair<List<Card>, List<Card>> {
    return Pair(deck.take(count), deck.drop(count))
}

/**
 * 模拟德州扑克一局
 * @param numPlayers 玩家数量
 * @return 游戏结果（各玩家手牌、公共牌）
 */
fun simulateTexasHoldem(numPlayers: Int, seed: Long? = null): GameResult {
    require(numPlayers in 2..10) { "玩家数量必须在2-10之间" }
    
    val deck = shuffleDeck(createDeck(), seed)
    val (hands, remaining) = dealTexasHoldem(deck, numPlayers)
    val (flop, afterFlop) = dealCommunityCards(remaining.drop(1), 3)  // 烧一张牌，发翻牌
    val (turn, afterTurn) = dealCommunityCards(afterFlop.drop(1), 1)  // 烧一张牌，发转牌
    val (river, _) = dealCommunityCards(afterTurn.drop(1), 1)        // 烧一张牌，发河牌
    
    val communityCards = flop + turn + river
    
    return GameResult(
        hands = hands,
        flop = flop,
        turn = turn.single(),
        river = river.single(),
        communityCards = communityCards
    )
}

/**
 * 游戏结果
 */
data class GameResult(
    val hands: List<List<Card>>,
    val flop: List<Card>,
    val turn: Card,
    val river: Card,
    val communityCards: List<Card>
) {
    fun describe(): String {
        val sb = StringBuilder()
        sb.appendLine("翻牌: ${flop.joinToString(" ")}")
        sb.appendLine("转牌: $turn")
        sb.appendLine("河牌: $river")
        sb.appendLine("公共牌: ${communityCards.joinToString(" ")}")
        sb.appendLine()
        hands.forEachIndexed { i, hand ->
            sb.appendLine("玩家${i + 1}: ${hand.joinToString(" ")}")
            val allCards = hand + communityCards
            val eval = evaluateHand(allCards)
            sb.appendLine("  最佳牌型: ${eval.describe()}")
        }
        return sb.toString()
    }
}