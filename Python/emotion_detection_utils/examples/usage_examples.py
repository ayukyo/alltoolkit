"""
情感检测工具使用示例

展示如何使用 emotion_detection_utils 进行文本情感分析。
"""

from emotion_detection_utils.mod import (
    EmotionDetector,
    Emotion,
    Sentiment,
    detect_emotion,
    get_sentiment,
    is_positive,
    is_negative
)


def example_basic_usage():
    """基本使用示例"""
    print("=" * 60)
    print("基本使用示例")
    print("=" * 60)
    
    # 创建检测器
    detector = EmotionDetector()
    
    # 检测中文文本
    texts = [
        "今天天气真好，心情特别愉快！",
        "我很伤心，失去了一位好朋友。",
        "这太让人气愤了，我非常生气！",
        "我有点害怕，不敢一个人走夜路。",
        "哇，真是太不可思议了！",
        "这东西太恶心了，让人作呕。"
    ]
    
    for text in texts:
        result = detector.detect(text)
        print(f"\n文本: {text}")
        print(f"  主导情感: {result.dominant_emotion.value}")
        print(f"  情感极性: {result.sentiment.value}")
        print(f"  置信度: {result.confidence:.3f}")
        print(f"  关键词: {result.keywords_found}")


def example_english_detection():
    """英文情感检测示例"""
    print("\n" + "=" * 60)
    print("英文情感检测示例")
    print("=" * 60)
    
    detector = EmotionDetector(language="en")
    
    texts = [
        "I am so happy today! It's wonderful!",
        "I feel really sad and lonely right now.",
        "This makes me so angry! I can't believe it!",
        "I'm afraid of what might happen next.",
        "Wow, this is absolutely amazing!",
        "This is disgusting and gross."
    ]
    
    for text in texts:
        result = detector.detect(text)
        print(f"\nText: {text}")
        print(f"  Dominant Emotion: {result.dominant_emotion.value}")
        print(f"  Sentiment: {result.sentiment.value}")
        print(f"  Confidence: {result.confidence:.3f}")


def example_batch_detection():
    """批量检测示例"""
    print("\n" + "=" * 60)
    print("批量检测示例")
    print("=" * 60)
    
    detector = EmotionDetector()
    
    # 批量检测评论
    comments = [
        "这个产品太棒了，非常满意！",
        "质量很差，完全不值这个价格。",
        "一般般，还可以接受。",
        "客服态度很好，物流也很快！",
        "收到货是坏的，太失望了。"
    ]
    
    results = detector.batch_detect(comments)
    
    print("\n评论情感分析结果:")
    print("-" * 60)
    for i, (comment, result) in enumerate(zip(comments, results), 1):
        print(f"{i}. {comment}")
        print(f"   情感: {result.dominant_emotion.value} | 极性: {result.sentiment.value} | 置信度: {result.confidence:.2f}")


def example_emotion_distribution():
    """情感分布分析示例"""
    print("\n" + "=" * 60)
    print("情感分布分析示例")
    print("=" * 60)
    
    detector = EmotionDetector()
    
    text = "今天虽然取得了一些成绩，但我还是很担心未来，同时也感到一丝失望。"
    distribution = detector.get_emotion_distribution(text)
    
    print(f"\n文本: {text}")
    print("\n情感分布:")
    for emotion, score in sorted(distribution.items(), key=lambda x: x[1], reverse=True):
        if score > 0:
            bar = "█" * int(score * 20)
            print(f"  {emotion:10s}: {score:.3f} {bar}")


def example_sentiment_score():
    """情感分数示例"""
    print("\n" + "=" * 60)
    print("情感分数示例")
    print("=" * 60)
    
    detector = EmotionDetector()
    
    texts = [
        "我非常非常开心，今天是最美好的一天！",
        "还行吧，没什么特别的。",
        "糟糕透了，我太失望了。"
    ]
    
    print("\n情感分数 (-1 到 1):")
    print("-" * 60)
    for text in texts:
        score = detector.get_sentiment_score(text)
        print(f"{text}")
        print(f"  分数: {score:+.3f} {'正面' if score > 0.2 else '负面' if score < -0.2 else '中性'}\n")


def example_convenience_functions():
    """便捷函数示例"""
    print("\n" + "=" * 60)
    print("便捷函数示例")
    print("=" * 60)
    
    # 快速检测
    result = detect_emotion("太棒了！非常满意！")
    print(f"\n快速检测: {result.dominant_emotion.value} (置信度: {result.confidence:.2f})")
    
    # 快速获取极性
    sentiment = get_sentiment("我很伤心")
    print(f"快速极性: {sentiment}")
    
    # 快速判断正面
    positive_text = "这是一次非常愉快的体验"
    negative_text = "这是一次糟糕的体验"
    
    print(f"\n'{positive_text}' 是正面情感吗? {is_positive(positive_text)}")
    print(f"'{negative_text}' 是负面情感吗? {is_negative(negative_text)}")


def example_social_media_analysis():
    """社交媒体分析示例"""
    print("\n" + "=" * 60)
    print("社交媒体分析示例")
    print("=" * 60)
    
    detector = EmotionDetector()
    
    # 模拟社交媒体帖子
    posts = [
        {"user": "用户A", "content": "今天阳光明媚，心情特别好！😄"},
        {"user": "用户B", "content": "又是加班的一天，太累了...😔"},
        {"user": "用户C", "content": "新出的产品真的很惊艳，强烈推荐！👍"},
        {"user": "用户D", "content": "服务态度太差了，再也不来了！😤"},
        {"user": "用户E", "content": "刚刚看到了一个消息，震惊到我了！😲"},
    ]
    
    print("\n社交媒体情感分析:")
    print("-" * 60)
    
    positive_count = 0
    negative_count = 0
    neutral_count = 0
    
    for post in posts:
        result = detector.detect(post["content"])
        emoji = {
            Sentiment.POSITIVE: "😊",
            Sentiment.NEGATIVE: "😞",
            Sentiment.NEUTRAL: "😐"
        }[result.sentiment]
        
        print(f"{post['user']}: {post['content']}")
        print(f"  → {result.dominant_emotion.value} {emoji} (置信度: {result.confidence:.2f})")
        
        if result.sentiment == Sentiment.POSITIVE:
            positive_count += 1
        elif result.sentiment == Sentiment.NEGATIVE:
            negative_count += 1
        else:
            neutral_count += 1
    
    total = len(posts)
    print(f"\n统计: 正面 {positive_count/total*100:.0f}% | 负面 {negative_count/total*100:.0f}% | 中性 {neutral_count/total*100:.0f}%")


def example_customer_feedback_analysis():
    """客户反馈分析示例"""
    print("\n" + "=" * 60)
    print("客户反馈分析示例")
    print("=" * 60)
    
    detector = EmotionDetector()
    
    # 模拟客户反馈
    feedbacks = [
        "产品质量很好，物流速度快，非常满意！",
        "包装破损，产品有划痕，体验很差。",
        "一般般，没有想象中那么好。",
        "客服响应很及时，问题解决得很满意。",
        "价格偏贵，性价比不高。",
        "功能很强大，超出预期！",
    ]
    
    # 分析反馈
    positive_feedbacks = []
    negative_feedbacks = []
    neutral_feedbacks = []
    
    for feedback in feedbacks:
        if detector.is_positive(feedback, threshold=0.4):
            positive_feedbacks.append(feedback)
        elif detector.is_negative(feedback, threshold=0.4):
            negative_feedbacks.append(feedback)
        else:
            neutral_feedbacks.append(feedback)
    
    print("\n正面反馈:")
    for fb in positive_feedbacks:
        print(f"  ✓ {fb}")
    
    print("\n负面反馈:")
    for fb in negative_feedbacks:
        print(f"  ✗ {fb}")
    
    print("\n中性反馈:")
    for fb in neutral_feedbacks:
        print(f"  - {fb}")
    
    # 统计
    total = len(feedbacks)
    print(f"\n满意度分析:")
    print(f"  满意: {len(positive_feedbacks)/total*100:.1f}%")
    print(f"  不满意: {len(negative_feedbacks)/total*100:.1f}%")
    print(f"  一般: {len(neutral_feedbacks)/total*100:.1f}%")


def example_to_dict():
    """结果导出示例"""
    print("\n" + "=" * 60)
    print("结果导出示例")
    print("=" * 60)
    
    detector = EmotionDetector()
    result = detector.detect("我非常开心，今天是个好日子！")
    
    # 转换为字典
    result_dict = result.to_dict()
    
    print("\n检测结果（字典格式）:")
    import json
    print(json.dumps(result_dict, indent=2, ensure_ascii=False))


def main():
    """主函数"""
    example_basic_usage()
    example_english_detection()
    example_batch_detection()
    example_emotion_distribution()
    example_sentiment_score()
    example_convenience_functions()
    example_social_media_analysis()
    example_customer_feedback_analysis()
    example_to_dict()
    
    print("\n" + "=" * 60)
    print("示例运行完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()