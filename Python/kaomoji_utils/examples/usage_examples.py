"""
Kaomoji Utils 使用示例

展示日式颜文字工具集的各种使用场景。
"""

from mod import (
    get_all_emotions,
    get_by_emotion,
    get_random,
    search,
    get_details,
    get_random_entry,
    count,
    count_total,
    happy, sad, love, angry, surprised, cute, shy, cat, bear, flower,
    HAPPY, SAD, LOVE, ANGRY, SURPRISED, CUTE, SHY, WINK, TABLE_FLIP, CAT, BEAR, FLOWER, FIGHT, MAGIC, RUN,
)


def example_basic_usage():
    """基本使用示例"""
    print("=" * 60)
    print("基本使用示例")
    print("=" * 60)
    
    # 获取随机颜文字
    print("\n🎲 获取随机颜文字:")
    print(f"  get_random() → {get_random()}")
    print(f"  get_random() → {get_random()}")
    print(f"  get_random() → {get_random()}")
    
    # 获取指定情绪的颜文字
    print("\n😊 获取开心颜文字:")
    happy_list = get_by_emotion("happy")
    for k in happy_list[:5]:
        print(f"  {k}")
    
    print("\n💔 获取伤心颜文字:")
    sad_list = get_by_emotion("sad")
    for k in sad_list[:5]:
        print(f"  {k}")
    
    # 获取所有情绪类别
    print("\n📋 所有情绪类别:")
    emotions = get_all_emotions()
    print(f"  {', '.join(emotions)}")


def example_search():
    """搜索功能示例"""
    print("\n" + "=" * 60)
    print("搜索功能示例")
    print("=" * 60)
    
    # 搜索关键词
    print("\n🔍 搜索 'love':")
    results = search("love")
    for k in results[:5]:
        print(f"  {k}")
    
    print("\n🔍 搜索 'cute':")
    results = search("cute")
    for k in results[:5]:
        print(f"  {k}")
    
    print("\n🔍 搜索 '猫' (中文描述):")
    results = search("猫")
    for k in results[:5]:
        print(f"  {k}")
    
    print("\n🔍 搜索 '♥' (颜文字中的字符):")
    results = search("♥")
    for k in results[:5]:
        print(f"  {k}")


def example_details():
    """详情功能示例"""
    print("\n" + "=" * 60)
    print("详情功能示例")
    print("=" * 60)
    
    # 获取颜文字详情
    print("\n📝 获取颜文字详情:")
    entry = get_details(HAPPY)
    print(f"  颜文字: {entry.kaomoji}")
    print(f"  情绪类别: {entry.emotion}")
    print(f"  关键词: {entry.keywords}")
    print(f"  描述: {entry.description}")
    
    # 获取随机条目
    print("\n🎲 获取随机条目:")
    entry = get_random_entry("cat")
    print(f"  颜文字: {entry.kaomoji}")
    print(f"  情绪类别: {entry.emotion}")
    print(f"  关键词: {entry.keywords}")
    print(f"  描述: {entry.description}")


def example_statistics():
    """统计功能示例"""
    print("\n" + "=" * 60)
    print("统计功能示例")
    print("=" * 60)
    
    # 统计总数
    print(f"\n📊 颜文字总数: {count_total()}")
    
    # 各类别统计
    print("\n📊 各类别数量:")
    counts = count()
    for emotion, cnt in sorted(counts.items()):
        print(f"  {emotion}: {cnt}")


def example_convenience_functions():
    """便捷函数示例"""
    print("\n" + "=" * 60)
    print("便捷函数示例")
    print("=" * 60)
    
    print("\n🎯 情绪快捷函数:")
    print(f"  happy()    → {happy()}")
    print(f"  sad()      → {sad()}")
    print(f"  love()     → {love()}")
    print(f"  angry()    → {angry()}")
    print(f"  surprised() → {surprised()}")
    print(f"  cute()     → {cute()}")
    print(f"  shy()      → {shy()}")
    print(f"  cat()      → {cat()}")
    print(f"  bear()     → {bear()}")
    print(f"  flower()   → {flower()}")


def example_constants():
    """常量使用示例"""
    print("\n" + "=" * 60)
    print("常量使用示例")
    print("=" * 60)
    
    print("\n📌 预定义常量:")
    print(f"  HAPPY      = {HAPPY}")
    print(f"  SAD        = {SAD}")
    print(f"  LOVE       = {LOVE}")
    print(f"  ANGRY      = {ANGRY}")
    print(f"  SURPRISED  = {SURPRISED}")
    print(f"  CUTE       = {CUTE}")
    print(f"  SHY        = {SHY}")
    print(f"  WINK       = {WINK}")
    print(f"  TABLE_FLIP = {TABLE_FLIP}")
    print(f"  CAT        = {CAT}")
    print(f"  BEAR       = {BEAR}")
    print(f"  FLOWER     = {FLOWER}")
    print(f"  FIGHT      = {FIGHT}")
    print(f"  MAGIC      = {MAGIC}")
    print(f"  RUN        = {RUN}")


def example_practical_usage():
    """实际应用示例"""
    print("\n" + "=" * 60)
    print("实际应用示例")
    print("=" * 60)
    
    # 模拟聊天场景
    print("\n💬 聊天场景示例:")
    
    print("\n  用户: '我今天好开心啊！'")
    print(f"  AI: '太棒了！{happy()} 真为你感到高兴！'")
    
    print("\n  用户: '我的猫咪不见了...' ")
    print(f"  AI: '噢，太遗憾了... {sad()} 希望你能找到它'")
    
    print("\n  用户: '我爱你'")
    print(f"  AI: '{love()} 我也爱你！'")
    
    print("\n  用户: '有人偷了我的午餐！'")
    print(f"  AI: '{angry()} 这太过分了！'")
    
    print("\n  用户: '看这个视频！'")
    print(f"  AI: '{surprised()} 哇，太神奇了！'")
    
    # 表情装饰
    print("\n✨ 表情装饰示例:")
    print(f"  '{cute()} 欢迎来到我的博客！'")
    print(f"  '今日心情: {happy()}'")
    print(f"  '推荐阅读 {flower()}'")
    
    # 社交媒体
    print("\n📱 社交媒体示例:")
    print(f"  微博: '早安！{happy()} {flower()}'")
    print(f"  Twitter: 'Good morning! {happy()}'")
    print(f"  朋友圈: '今天天气真好 {cute()} {flower()}'")


def example_creative_usage():
    """创意使用示例"""
    print("\n" + "=" * 60)
    print("创意使用示例")
    print("=" * 60)
    
    # 情绪变化
    print("\n🎭 情绪变化场景:")
    emotions = ["happy", "love", "shy", "happy", "excited"]
    for emotion in emotions:
        print(f"  {get_random(emotion)}")
    
    # 颜文字组合
    print("\n🎨 颜文字组合:")
    print(f"  {cat()} {bear()} {flower()}")
    print(f"  {HAPPY} {love()} {CUTE}")
    
    # 特殊场景
    print("\n🎉 特殊场景:")
    print(f"  掀桌: {TABLE_FLIP}")
    print(f"  打架: {FIGHT}")
    print(f"  魔法: {MAGIC}")
    print(f"  逃跑: {RUN}")
    
    # 表达式组合
    print("\n📝 表达式组合:")
    print(f"  '{love()} 我喜欢你 {shy()}'")
    print(f"  '{angry()} 你骗我！{TABLE_FLIP}'")
    print(f"  '{happy()} {cat()} 今天好开心！'")


def example_all_emotions():
    """展示所有情绪类别"""
    print("\n" + "=" * 60)
    print("所有情绪类别展示")
    print("=" * 60)
    
    for emotion in get_all_emotions():
        print(f"\n【{emotion}】")
        kaomoji_list = get_by_emotion(emotion)
        # 显示前3个
        for k in kaomoji_list[:3]:
            print(f"  {k}")
        if len(kaomoji_list) > 3:
            print(f"  ... 还有 {len(kaomoji_list) - 3} 个")


def main():
    """运行所有示例"""
    example_basic_usage()
    example_search()
    example_details()
    example_statistics()
    example_convenience_functions()
    example_constants()
    example_practical_usage()
    example_creative_usage()
    example_all_emotions()
    
    print("\n" + "=" * 60)
    print("示例结束")
    print("=" * 60)


if __name__ == "__main__":
    main()