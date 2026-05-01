"""
Sentiment Utils - 使用示例

展示情感分析工具的各种用法。
"""

from sentiment_utils import (
    SentimentAnalyzer, SentimentPolarity,
    analyze_sentiment, get_sentiment_score, 
    is_positive_text, is_negative_text
)


def example_basic_analysis():
    """基本情感分析示例"""
    print("\n" + "=" * 60)
    print("示例 1: 基本情感分析")
    print("=" * 60)
    
    analyzer = SentimentAnalyzer()
    
    texts = [
        "这个产品非常好用，我很喜欢！",
        "服务态度太差了，非常失望。",
        "这个东西还行，凑合用吧。",
    ]
    
    for text in texts:
        result = analyzer.analyze(text)
        print(f"\n文本: {text}")
        print(f"  极性: {result.polarity.value}")
        print(f"  得分: {result.score}")
        print(f"  正面词: {result.positive_words}")
        print(f"  负面词: {result.negative_words}")
        print(f"  置信度: {result.confidence}")


def example_english_analysis():
    """英文情感分析示例"""
    print("\n" + "=" * 60)
    print("示例 2: 英文情感分析")
    print("=" * 60)
    
    analyzer = SentimentAnalyzer()
    
    texts = [
        "I love this product! It's amazing and wonderful!",
        "This is terrible. I hate it. Worst purchase ever.",
        "The quality is okay, nothing special.",
    ]
    
    for text in texts:
        result = analyzer.analyze(text)
        print(f"\nText: {text}")
        print(f"  Polarity: {result.polarity.value}")
        print(f"  Score: {result.score}")


def example_negation_handling():
    """否定词处理示例"""
    print("\n" + "=" * 60)
    print("示例 3: 否定词处理")
    print("=" * 60)
    
    analyzer = SentimentAnalyzer()
    
    pairs = [
        ("这个很好", "这个不好"),
        ("I like it", "I don't like it"),
        ("服务很好", "服务不好"),
        ("This is good", "This is not good"),
    ]
    
    for positive, negative in pairs:
        result_pos = analyzer.analyze(positive)
        result_neg = analyzer.analyze(negative)
        
        print(f"\n对比:")
        print(f"  '{positive}' → 得分: {result_pos.score:.2f}")
        print(f"  '{negative}' → 得分: {result_neg.score:.2f}")


def example_intensifier():
    """程度副词效果示例"""
    print("\n" + "=" * 60)
    print("示例 4: 程度副词效果")
    print("=" * 60)
    
    analyzer = SentimentAnalyzer()
    
    texts = [
        "这个好",
        "这个很好",
        "这个非常好",
        "这个特别好",
        "这个极其好",
    ]
    
    for text in texts:
        result = analyzer.analyze(text)
        print(f"'{text}' → 得分: {result.score:.2f}, 正面得分: {result.positive_score:.2f}")


def example_custom_dictionary():
    """自定义词典示例"""
    print("\n" + "=" * 60)
    print("示例 5: 自定义词典")
    print("=" * 60)
    
    # 添加自定义词汇
    custom_positive = {
        "牛牛牛": 1.0,
        "给力啊": 0.9,
        "真香": 0.8,
    }
    
    custom_negative = {
        "坑爹": 0.9,
        "辣鸡": 0.8,
        "智商税": 0.7,
    }
    
    analyzer = SentimentAnalyzer(
        custom_positive=custom_positive,
        custom_negative=custom_negative
    )
    
    texts = [
        "这个东西牛牛牛！",
        "真是坑爹！",
        "智商税产品！",
        "真香！",
    ]
    
    for text in texts:
        result = analyzer.analyze(text)
        print(f"\n'{text}'")
        print(f"  极性: {result.polarity.value}")
        print(f"  得分: {result.score}")


def example_batch_analysis():
    """批量分析示例"""
    print("\n" + "=" * 60)
    print("示例 6: 批量分析")
    print("=" * 60)
    
    analyzer = SentimentAnalyzer()
    
    # 模拟商品评论
    comments = [
        "质量很好，物流也快，非常满意！",
        "一般般吧，没什么特别的。",
        "太差了，退货了，浪费钱。",
        "性价比很高，推荐购买！",
        "做工粗糙，不值这个价。",
        "颜色和图片不符，失望。",
        "很好很好，下次还来！",
        "勉强能用，凑合吧。",
    ]
    
    results = analyzer.analyze_batch(comments)
    
    # 统计
    positive_count = sum(1 for r in results if r.polarity == SentimentPolarity.POSITIVE)
    negative_count = sum(1 for r in results if r.polarity == SentimentPolarity.NEGATIVE)
    neutral_count = sum(1 for r in results if r.polarity == SentimentPolarity.NEUTRAL)
    avg_score = sum(r.score for r in results) / len(results)
    
    print(f"\n共 {len(comments)} 条评论:")
    print(f"  正面: {positive_count} 条 ({positive_count/len(comments)*100:.1f}%)")
    print(f"  中性: {neutral_count} 条 ({neutral_count/len(comments)*100:.1f}%)")
    print(f"  负面: {negative_count} 条 ({negative_count/len(comments)*100:.1f}%)")
    print(f"  平均得分: {avg_score:.2f}")
    
    print("\n详细分析:")
    for i, (comment, result) in enumerate(zip(comments, results), 1):
        emoji = "😊" if result.polarity == SentimentPolarity.POSITIVE else \
                "😞" if result.polarity == SentimentPolarity.NEGATIVE else "😐"
        print(f"  {i}. [{emoji}] {comment[:20]}... 得分: {result.score:.2f}")


def example_sentiment_comparison():
    """情感比较示例"""
    print("\n" + "=" * 60)
    print("示例 7: 情感比较")
    print("=" * 60)
    
    analyzer = SentimentAnalyzer()
    
    products = [
        ("产品A", "质量很好，价格实惠，物流超快！"),
        ("产品B", "还行，能用，没什么特别的。"),
        ("产品C", "太差了，做工粗糙，不推荐购买。"),
    ]
    
    # 按情感得分排序
    ranked = sorted(
        [(name, text, analyzer.get_score(text)) for name, text in products],
        key=lambda x: x[2],
        reverse=True
    )
    
    print("\n产品评价排名（按情感得分）:")
    for i, (name, text, score) in enumerate(ranked, 1):
        print(f"  {i}. {name}: 得分 {score:.2f}")
        print(f"     评价: {text}")


def example_quick_functions():
    """便捷函数示例"""
    print("\n" + "=" * 60)
    print("示例 8: 便捷函数")
    print("=" * 60)
    
    texts = [
        "这个产品非常好！",
        "这个产品太差了！",
        "一般般吧。",
    ]
    
    print("\n快捷判断:")
    for text in texts:
        score = get_sentiment_score(text)
        is_pos = is_positive_text(text)
        is_neg = is_negative_text(text)
        
        status = "正面" if is_pos else "负面" if is_neg else "中性"
        print(f"  '{text}' → {status} (得分: {score:.2f})")


def example_extract_words():
    """提取情感词示例"""
    print("\n" + "=" * 60)
    print("示例 8: 提取情感词")
    print("=" * 60)
    
    analyzer = SentimentAnalyzer()
    
    text = "这个产品质量很好，价格实惠，物流超快，但是客服态度很差，让人失望。"
    
    positive, negative = analyzer.get_sentiment_words(text)
    
    print(f"\n文本: {text}")
    print(f"正面词: {positive}")
    print(f"负面词: {negative}")


if __name__ == "__main__":
    example_basic_analysis()
    example_english_analysis()
    example_negation_handling()
    example_intensifier()
    example_custom_dictionary()
    example_batch_analysis()
    example_sentiment_comparison()
    example_quick_functions()
    example_extract_words()
    
    print("\n" + "=" * 60)
    print("所有示例运行完成！")
    print("=" * 60)