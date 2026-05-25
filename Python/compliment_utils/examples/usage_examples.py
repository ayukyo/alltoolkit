"""
Compliment Utils 使用示例

演示称赞生成工具的各种用法
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    ComplimentUtils,
    ComplimentCategory,
    ComplimentStrength,
    Language,
    get_compliment,
    get_personalized_compliment,
    get_daily_compliment,
    get_motivational_compliment,
    get_batch_compliments,
    random_compliment,
)


def example_basic_compliment():
    """示例：基本称赞获取"""
    print("\n" + "=" * 50)
    print("示例：基本称赞获取")
    print("=" * 50)
    
    # 随机称赞
    print("\n随机称赞：")
    print(random_compliment())
    
    # 使用类方法获取
    print("\n使用类方法获取称赞：")
    print(ComplimentUtils.get_compliment())


def example_category_compliments():
    """示例：按类别获取称赞"""
    print("\n" + "=" * 50)
    print("示例：按类别获取称赞")
    print("=" * 50)
    
    categories = ComplimentUtils.get_categories(Language.CHINESE)
    
    for category in categories:
        compliment = ComplimentUtils.get_compliment(
            category=ComplimentCategory(category),
            language=Language.CHINESE,
        )
        print(f"\n【{category}】：{compliment}")


def example_strength_compliments():
    """示例：按强度获取称赞"""
    print("\n" + "=" * 50)
    print("示例：按强度获取称赞")
    print("=" * 50)
    
    for strength in [ComplimentStrength.LIGHT, ComplimentStrength.MEDIUM, ComplimentStrength.STRONG]:
        compliment = ComplimentUtils.get_compliment(
            strength=strength,
            category=ComplimentCategory.WORK,
            language=Language.CHINESE,
        )
        print(f"\n【{strength.value}】：{compliment}")


def example_language_compliments():
    """示例：多语言称赞"""
    print("\n" + "=" * 50)
    print("示例：多语言称赞")
    print("=" * 50)
    
    # 中文称赞
    print("\n中文称赞：")
    for i in range(3):
        print(f"  {i+1}. {ComplimentUtils.get_compliment(language=Language.CHINESE)}")
    
    # 英文称赞
    print("\n英文称赞：")
    for i in range(3):
        print(f"  {i+1}. {ComplimentUtils.get_compliment(language=Language.ENGLISH)}")


def example_personalized_compliments():
    """示例：个性化称赞"""
    print("\n" + "=" * 50)
    print("示例：个性化称赞")
    print("=" * 50)
    
    names = ["小明", "小红", "张三", "李四"]
    
    print("\n中文个性化称赞：")
    for name in names:
        compliment = ComplimentUtils.get_personalized_compliment(
            name=name,
            language=Language.CHINESE,
        )
        print(f"  → {compliment}")
    
    print("\n英文个性化称赞：")
    for name in ["John", "Sarah", "Mike", "Emma"]:
        compliment = ComplimentUtils.get_personalized_compliment(
            name=name,
            language=Language.ENGLISH,
        )
        print(f"  → {compliment}")


def example_context_compliments():
    """示例：根据上下文获取称赞"""
    print("\n" + "=" * 50)
    print("示例：根据上下文获取称赞")
    print("=" * 50)
    
    contexts = [
        "完成了项目开发",
        "帮助同事解决了问题",
        "设计出了新的方案",
        "每天坚持锻炼",
        "获得了比赛第一名",
    ]
    
    for context in contexts:
        compliment = ComplimentUtils.get_compliment_for_context(context)
        print(f"\n上下文：{context}")
        print(f"称赞：{compliment}")


def example_batch_compliments():
    """示例：批量获取称赞"""
    print("\n" + "=" * 50)
    print("示例：批量获取称赞")
    print("=" * 50)
    
    # 获取5条不重复的称赞
    print("\n获取5条不重复的称赞：")
    compliments = ComplimentUtils.get_batch_compliments(count=5, unique=True)
    for i, compliment in enumerate(compliments, 1):
        print(f"  {i}. {compliment}")
    
    # 获取特定类别的批量称赞
    print("\n获取3条工作相关的称赞：")
    compliments = ComplimentUtils.get_batch_compliments(
        count=3,
        category=ComplimentCategory.WORK,
    )
    for i, compliment in enumerate(compliments, 1):
        print(f"  {i}. {compliment}")


def example_daily_compliment():
    """示例：每日称赞"""
    print("\n" + "=" * 50)
    print("示例：每日称赞")
    print("=" * 50)
    
    print("\n中文每日称赞：")
    print(ComplimentUtils.get_daily_compliment(Language.CHINESE))
    
    print("\n英文每日称赞：")
    print(ComplimentUtils.get_daily_compliment(Language.ENGLISH))


def example_motivational_compliment():
    """示例：激励性称赞"""
    print("\n" + "=" * 50)
    print("示例：激励性称赞")
    print("=" * 50)
    
    print("\n适合用于激励的场景：")
    for i in range(3):
        compliment = ComplimentUtils.get_motivational_compliment(Language.CHINESE)
        print(f"  {i+1}. {compliment}")


def example_with_prefix_suffix():
    """示例：带前缀和后缀的称赞"""
    print("\n" + "=" * 50)
    print("示例：带前缀和后缀的称赞")
    print("=" * 50)
    
    print("\n只带前缀：")
    compliment = ComplimentUtils.get_compliment(include_prefix=True, include_suffix=False)
    print(f"  {compliment}")
    
    print("\n只带后缀：")
    compliment = ComplimentUtils.get_compliment(include_prefix=False, include_suffix=True)
    print(f"  {compliment}")
    
    print("\n带前缀和后缀：")
    compliment = ComplimentUtils.get_compliment(include_prefix=True, include_suffix=True)
    print(f"  {compliment}")


def example_convenience_functions():
    """示例：便捷函数使用"""
    print("\n" + "=" * 50)
    print("示例：便捷函数使用")
    print("=" * 50)
    
    # 使用便捷函数
    print("\n使用 get_compliment()：")
    print(get_compliment())
    
    print("\n使用 get_compliment(category='工作')：")
    print(get_compliment(category="工作"))
    
    print("\n使用 get_compliment(strength='强力', language='zh')：")
    print(get_compliment(strength="强力", language="zh"))
    
    print("\n使用 get_personalized_compliment('小明')：")
    print(get_personalized_compliment("小明"))
    
    print("\n使用 get_batch_compliments(5)：")
    compliments = get_batch_compliments(5)
    for i, c in enumerate(compliments, 1):
        print(f"  {i}. {c}")


def example_statistics():
    """示例：统计信息"""
    print("\n" + "=" * 50)
    print("示例：统计信息")
    print("=" * 50)
    
    # 获取称赞总数
    total = ComplimentUtils.get_compliment_count()
    print(f"\n称赞语总数：{total}")
    
    # 获取各类别称赞数量
    print("\n各类别称赞数量：")
    for category in ComplimentCategory:
        count = ComplimentUtils.get_compliment_count(category=category)
        print(f"  {category.value}: {count}条")
    
    # 获取可用类别
    print("\n可用类别列表：")
    categories = ComplimentUtils.get_categories(Language.CHINESE)
    print(f"  {', '.join(categories)}")
    
    # 获取可用强度
    print("\n可用强度列表：")
    strengths = ComplimentUtils.get_strengths(Language.CHINESE)
    print(f"  {', '.join(strengths)}")


def example_special_scenario():
    """示例：特殊场景应用"""
    print("\n" + "=" * 50)
    print("示例：特殊场景应用")
    print("=" * 50)
    
    # 面试场景 - 称赞候选人的能力
    print("\n【面试场景】称赞候选人：")
    compliment = ComplimentUtils.get_compliment(
        category=ComplimentCategory.SKILL,
        strength=ComplimentStrength.MEDIUM,
        include_prefix=True,
    )
    print(f"  {compliment}")
    
    # 团队建设 - 称赞团队协作
    print("\n【团队建设】称赞团队精神：")
    compliment = ComplimentUtils.get_compliment(
        category=ComplimentCategory.FRIENDSHIP,
        strength=ComplimentStrength.STRONG,
        include_prefix=True,
        include_suffix=True,
    )
    print(f"  {compliment}")
    
    # 每日鼓励 - 用于自动化提醒
    print("\n【每日鼓励】自动化提醒内容：")
    compliment = get_motivational_compliment()
    print(f"  {compliment}")
    
    # 礼貌开场 - 用于邮件或消息开头
    print("\n【礼貌开场】邮件开头称赞：")
    compliment = ComplimentUtils.get_compliment(
        category=ComplimentCategory.GENERAL,
        strength=ComplimentStrength.LIGHT,
        include_prefix=False,
    )
    print(f"  {compliment}")


def main():
    """运行所有示例"""
    print("\n" + "=" * 60)
    print(" Compliment Utils - 称赞生成工具使用示例")
    print("=" * 60)
    
    example_basic_compliment()
    example_category_compliments()
    example_strength_compliments()
    example_language_compliments()
    example_personalized_compliments()
    example_context_compliments()
    example_batch_compliments()
    example_daily_compliment()
    example_motivational_compliment()
    example_with_prefix_suffix()
    example_convenience_functions()
    example_statistics()
    example_special_scenario()
    
    print("\n" + "=" * 60)
    print(" 示例演示完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()