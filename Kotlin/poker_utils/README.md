# Poker Utils - 扑克牌工具模块

[English](#english) | [中文](#中文)

---

## 中文

### 概述

扑克牌工具模块，提供完整的扑克牌操作功能，包括牌组管理、发牌、牌型评估、手牌比较和概率计算。

### 功能特性

#### 🃏 牌组操作
- 创建标准52张牌组
- Fisher-Yates 洗牌算法（支持种子）
- 发牌（支持任意手牌数量）
- 德州扑克专用发牌

#### 📊 牌型评估
支持所有标准扑克牌型：
1. 高牌 (High Card)
2. 一对 (One Pair)
3. 两对 (Two Pair)
4. 三条 (Three of a Kind)
5. 顺子 (Straight)
6. 同花 (Flush)
7. 葫芦 (Full House)
8. 四条 (Four of a Kind)
9. 同花顺 (Straight Flush)
10. 皇家同花顺 (Royal Flush)

#### 🎮 游戏功能
- 手牌比较和赢家判定
- 德州扑克完整局模拟
- 多牌型最佳组合选择（7张选5张）

#### 📈 概率计算
- 出牌概率计算
- 底池赔率计算
- 跟注决策辅助

### 安装

将 `poker_utils.kt` 复制到您的项目中即可使用。

### 快速开始

```kotlin
import poker_utils.*

fun main() {
    // 创建并洗牌
    val deck = shuffleDeck(createDeck())
    
    // 德州扑克发牌
    val (hands, remaining) = dealTexasHoldem(deck, numPlayers = 4)
    
    // 评估牌型
    val cards = parseCards("♠A ♥A ♦A ♣K ♠K")
    val eval = evaluateHand(cards)
    println(eval.describe())  // 葫芦 (Full House)
    
    // 模拟游戏
    val result = simulateTexasHoldem(numPlayers = 4)
    println(result.describe())
}
```

### API 参考

#### 数据类型

```kotlin
// 花色
enum class Suit {
    SPADES,    // ♠ 黑桃
    HEARTS,    // ♥ 红心
    DIAMONDS,  // ♦ 方块
    CLUBS      // ♣ 梅花
}

// 点数 (2-10, J, Q, K, A)
enum class Rank {
    TWO, THREE, FOUR, FIVE, SIX, SEVEN, EIGHT, NINE, TEN,
    JACK, QUEEN, KING, ACE
}

// 扑克牌
data class Card(val suit: Suit, val rank: Rank)

// 牌型
enum class HandRank {
    HIGH_CARD, ONE_PAIR, TWO_PAIR, THREE_OF_A_KIND,
    STRAIGHT, FLUSH, FULL_HOUSE, FOUR_OF_A_KIND,
    STRAIGHT_FLUSH, ROYAL_FLUSH
}

// 评估结果
data class HandEvaluation(
    val rank: HandRank,
    val kickers: List<Int>,
    val cards: List<Card>
)
```

#### 核心函数

```kotlin
// 牌组操作
fun createDeck(): List<Card>
fun shuffleDeck(deck: List<Card>, seed: Long? = null): List<Card>
fun dealCards(deck: List<Card>, numHands: Int, cardsPerHand: Int): Pair<List<List<Card>>, List<Card>>
fun dealTexasHoldem(deck: List<Card>, numPlayers: Int): Pair<List<List<Card>>, List<Card>>

// 牌型评估
fun evaluateHand(cards: List<Card>): HandEvaluation

// 手牌比较
fun compareHands(hand1: List<Card>, hand2: List<Card>): Int
fun findWinners(hands: Map<String, List<Card>>): List<Pair<String, HandEvaluation>>

// 概率计算
fun calculateOutsProbability(outs: Int, remainingCards: Int = 47): Double
fun calculatePotOdds(potSize: Double, callAmount: Double): Double
fun shouldCall(outs: Int, potOdds: Double): Boolean

// 游戏模拟
fun simulateTexasHoldem(numPlayers: Int, seed: Long? = null): GameResult

// 解析工具
fun parseCard(str: String): Card?
fun parseCards(str: String): List<Card>
fun cardsHash(cards: List<Card>): String
```

### 使用示例

#### 1. 评估牌型

```kotlin
// 一对
val pair = parseCards("♠A ♥A ♦K ♣Q ♠J")
println(evaluateHand(pair).describe())  // 一对 (One Pair)

// 同花顺
val straightFlush = parseCards("♠5 ♠6 ♠7 ♠8 ♠9")
println(evaluateHand(straightFlush).describe())  // 同花顺 (Straight Flush)

// 皇家同花顺
val royal = parseCards("♠10 ♠J ♠Q ♠K ♠A")
println(evaluateHand(royal).describe())  // 皇家同花顺 (Royal Flush)
```

#### 2. 德州扑克模拟

```kotlin
val result = simulateTexasHoldem(numPlayers = 4, seed = 12345)

// 输出结果
println(result.describe())

// 获取公共牌
val flop = result.flop      // 翻牌（3张）
val turn = result.turn      // 转牌（1张）
val river = result.river    // 河牌（1张）

// 评估每个玩家的最终牌型
result.hands.forEachIndexed { i, hand ->
    val allCards = hand + result.communityCards
    val eval = evaluateHand(allCards)
    println("玩家${i + 1}: ${eval.describe()}")
}
```

#### 3. 手牌比较

```kotlin
val players = mapOf(
    "Alice" to parseCards("♠A ♥A ♦K ♣Q ♠J"),    // 一对A
    "Bob" to parseCards("♠K ♥K ♦K ♣Q ♠J"),      // 三条K
    "Charlie" to parseCards("♠A ♥A ♦A ♣Q ♠J")   // 三条A
)

val winners = findWinners(players)
// 获胜者: Charlie (三条 A)
```

#### 4. 概率计算

```kotlin
// 同花听牌场景
val outs = 9  // 剩余同花牌
val prob = calculateOutsProbability(outs)
println("成功概率: ${(prob * 100).format(1)}%")

// 底池赔率
val potOdds = calculatePotOdds(potSize = 100.0, callAmount = 20.0)
println("底池赔率: ${potOdds}:1")

// 是否值得跟注
if (shouldCall(outs, potOdds)) {
    println("建议跟注")
} else {
    println("建议弃牌")
}
```

### 测试

运行测试套件：

```bash
kotlinc poker_utils.kt poker_utils_test.kt -include-runtime -d poker_test.jar
java -jar poker_test.jar
```

### 许可证

MIT License

---

## English

### Overview

A comprehensive poker utility module providing card deck management, dealing, hand evaluation, hand comparison, and probability calculations.

### Features

#### 🃏 Deck Operations
- Create standard 52-card deck
- Fisher-Yates shuffle algorithm (seedable)
- Deal cards (any number of hands)
- Texas Hold'em specific dealing

#### 📊 Hand Evaluation
Supports all standard poker hands:
1. High Card
2. One Pair
3. Two Pair
4. Three of a Kind
5. Straight
6. Flush
7. Full House
8. Four of a Kind
9. Straight Flush
10. Royal Flush

#### 🎮 Game Features
- Hand comparison and winner determination
- Complete Texas Hold'em simulation
- Best 5-card selection from 7 cards

#### 📈 Probability Calculations
- Outs probability calculation
- Pot odds calculation
- Call/fold decision helper

### Installation

Copy `poker_utils.kt` to your project.

### Quick Start

```kotlin
import poker_utils.*

fun main() {
    // Create and shuffle deck
    val deck = shuffleDeck(createDeck())
    
    // Deal Texas Hold'em
    val (hands, remaining) = dealTexasHoldem(deck, numPlayers = 4)
    
    // Evaluate hand
    val cards = parseCards("♠A ♥A ♦A ♣K ♠K")
    val eval = evaluateHand(cards)
    println(eval.describe())  // Full House
    
    // Simulate game
    val result = simulateTexasHoldem(numPlayers = 4)
    println(result.describe())
}
```

### API Reference

See Chinese section above for complete API documentation.

### License

MIT License