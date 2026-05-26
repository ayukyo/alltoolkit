"""
Riddle Utils 使用示例

演示谜语工具库的各种用法
"""

import sys
import os
from datetime import date

# 添加父目录到路径（mod.py 在上一级目录）
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    RiddleManager,
    Riddle,
    Hint,
    RiddleCategory,
    RiddleDifficulty,
    RiddleLanguage,
    RiddleGenerator,
    RiddleQuiz,
    get_random_riddle,
    get_daily_riddle,
    check_riddle_answer,
)


def example_basic_usage():
    """基本用法示例"""
    print("=" * 50)
    print("1. 基本用法示例")
    print("=" * 50)
    
    manager = RiddleManager()
    
    # 获取随机谜语
    riddle = manager.get_random()
    print(f"\n谜面：{riddle.question}")
    print(f"类别：{riddle.category.value}")
    print(f"难度：{riddle.difficulty.name}")
    print(f"语言：{riddle.language.value}")
    
    # 获取提示
    print("\n--- 提示系统 ---")
    for level in [1, 2, 3]:
        hint = manager.get_hint(riddle.id, level=level)
        if hint:
            print(f"提示 {hint.level}: {hint.content}")
    
    # 检查答案
    print("\n--- 答案验证 ---")
    test_answers = ["错误答案", riddle.answer]
    for answer in test_answers:
        is_correct, feedback = manager.check_answer(riddle.id, answer)
        print(f"答案 '{answer}': {feedback}")
    
    print(f"\n正确答案：{riddle.answer}")
    print(f"解释：{riddle.explanation}")


def example_category_filter():
    """按类别筛选示例"""
    print("\n" + "=" * 50)
    print("2. 按类别筛选示例")
    print("=" * 50)
    
    manager = RiddleManager()
    
    # 按类别获取谜语
    categories = [RiddleCategory.ANIMAL, RiddleCategory.CHARACTER, RiddleCategory.HUMOR]
    
    for category in categories:
        riddles = manager.get_by_category(category)
        print(f"\n{category.value} 类别谜语数量: {len(riddles)}")
        
        if riddles:
            r = riddles[0]
            print(f"  示例: {r.question[:50]}...")
            print(f"  答案: {r.answer}")


def example_difficulty_levels():
    """难度级别示例"""
    print("\n" + "=" * 50)
    print("3. 难度级别示例")
    print("=" * 50)
    
    manager = RiddleManager()
    
    # 按难度获取谜语
    for difficulty in RiddleDifficulty:
        riddles = manager.get_by_difficulty(difficulty)
        print(f"\n{difficulty.name} 难度谜语数量: {len(riddles)}")
        
        if riddles:
            r = riddles[0]
            print(f"  示例: {r.question[:50]}...")


def example_language_filter():
    """语言筛选示例"""
    print("\n" + "=" * 50)
    print("4. 语言筛选示例")
    print("=" * 50)
    
    manager = RiddleManager()
    
    # 中文谜语
    print("\n中文谜语示例:")
    zh_riddle = manager.get_random(language=RiddleLanguage.CHINESE)
    print(f"谜面：{zh_riddle.question}")
    print(f"答案：{zh_riddle.answer}")
    
    # 英文谜语
    print("\n英文谜语示例:")
    en_riddle = manager.get_random(language=RiddleLanguage.ENGLISH)
    print(f"谜面：{en_riddle.question}")
    print(f"答案：{en_riddle.answer}")
    
    # 测试英文答案验证（不区分大小写）
    is_correct, feedback = manager.check_answer(en_riddle.id, en_riddle.answer.upper())
    print(f"验证大写答案: {feedback}")


def example_daily_riddle():
    """每日谜语示例"""
    print("\n" + "=" * 50)
    print("5. 每日谜语示例")
    print("=" * 50)
    
    manager = RiddleManager()
    
    # 获取今天的谜语
    today_riddle = manager.get_daily_riddle()
    print(f"\n今日谜语 ({date.today()}):")
    print(f"谜面：{today_riddle.question}")
    print(f"类别：{today_riddle.category.value}")
    
    # 获取特定日期的谜语
    specific_date = date(2024, 1, 1)
    specific_riddle = manager.get_daily_riddle(specific_date)
    print(f"\n{specific_date} 的谜语:")
    print(f"谜面：{specific_riddle.question[:50]}...")


def example_quiz_game():
    """问答游戏示例"""
    print("\n" + "=" * 50)
    print("6. 问答游戏示例")
    print("=" * 50)
    
    quiz = RiddleQuiz()
    
    # 开始三轮游戏
    print("\n开始谜语问答游戏！\n")
    
    for round_num in range(1, 4):
        print(f"--- 第 {round_num} 轮 ---")
        
        riddle = quiz.start_round()
        print(f"谜面：{riddle.question}")
        
        # 模拟玩家请求提示
        hint = quiz.get_hint()
        print(f"提示：{hint}")
        
        # 模拟玩家回答（这里使用正确答案演示）
        result = quiz.answer(riddle.answer)
        
        print(f"结果：{result['feedback']}")
        print(f"得分：{result['score']}")
        print(f"解释：{result['explanation']}")
        print()
    
    # 显示最终统计
    stats = quiz.get_stats()
    print("=" * 30)
    print("游戏统计")
    print("=" * 30)
    print(f"总轮数：{stats['rounds_played']}")
    print(f"正确数：{stats['correct_answers']}")
    print(f"总得分：{stats['total_score']}")
    print(f"正确率：{stats['accuracy']:.1%}")


def example_custom_riddle():
    """添加自定义谜语示例"""
    print("\n" + "=" * 50)
    print("7. 自定义谜语示例")
    print("=" * 50)
    
    manager = RiddleManager()
    
    # 创建自定义谜语
    custom_riddle = Riddle(
        id="custom_001",
        question="四四方方一座城，里面有灯外面明，到了晚上才出来，白天不见影无踪。",
        answer="窗户",
        category=RiddleCategory.DAILY,
        difficulty=RiddleDifficulty.MEDIUM,
        language=RiddleLanguage.CHINESE,
        hints=[
            Hint(1, "这是房子的一部分", "category"),
            Hint(2, "用来透光和通风", "description"),
            Hint(3, "两个字", "length"),
            Hint(4, "第一字是'窗'", "first_letter"),
            Hint(5, "晚上能看到外面", "description"),
        ],
        explanation="窗户是房子的一部分，白天可以采光，晚上可以看到外面的灯光。",
        tags=["房屋", "日常", "建筑"],
    )
    
    # 添加到管理器
    manager.add_riddle(custom_riddle)
    print(f"\n添加自定义谜语成功！")
    print(f"谜语总数：{manager.count()}")
    
    # 验证添加成功
    retrieved = manager.get_riddle("custom_001")
    print(f"\n检索验证：{retrieved.question}")
    print(f"答案：{retrieved.answer}")


def example_riddle_generator():
    """谜语生成器示例"""
    print("\n" + "=" * 50)
    print("8. 谜语生成器示例")
    print("=" * 50)
    
    generator = RiddleGenerator()
    
    # 生成物品谜语
    print("\n生成物品谜语：")
    features = {
        "missing": "脚",
        "ability": "报时",
        "cannot": "走",
        "category_hint": "这是日常用品",
        "first_letter": "钟",
        "explanation": "钟表能显示时间但不能走路。",
    }
    
    object_riddle = generator.generate_object_riddle("钟表", features)
    print(f"谜面：{object_riddle.question}")
    print(f"答案：{object_riddle.answer}")
    
    # 生成字谜
    print("\n生成字谜：")
    char_riddle = generator.generate_character_riddle(
        character="日",
        composition="太阳从地上升起",
        meaning="太阳",
    )
    print(f"谜面：{char_riddle.question}")
    print(f"答案：{char_riddle.answer}")
    print(f"解释：{char_riddle.explanation}")


def example_search():
    """搜索示例"""
    print("\n" + "=" * 50)
    print("9. 搜索谜语示例")
    print("=" * 50)
    
    manager = RiddleManager()
    
    # 搜索关键词
    keywords = ["西瓜", "动物", "clock"]
    
    for keyword in keywords:
        results = manager.search(keyword)
        print(f"\n搜索 '{keyword}' 找到 {len(results)} 个结果：")
        for r in results[:3]:  # 只显示前3个
            print(f"  - {r.question[:40]}...")
            print(f"    答案：{r.answer}")


def example_statistics():
    """统计信息示例"""
    print("\n" + "=" * 50)
    print("10. 统计信息示例")
    print("=" * 50)
    
    manager = RiddleManager()
    
    print(f"\n谜语总数：{manager.count()}")
    
    # 按类别统计
    print("\n类别分布：")
    category_counts = manager.count_by_category()
    for category, count in category_counts.items():
        print(f"  {category.value}: {count}")
    
    # 可用类别
    print(f"\n可用类别：{[c.value for c in manager.get_categories()]}")
    
    # 可用难度
    print(f"\n可用难度：{[d.name for d in manager.get_difficulties()]}")
    
    # 可用语言
    print(f"\n可用语言：{[l.value for l in manager.get_languages()]}")


def example_convenience_functions():
    """便捷函数示例"""
    print("\n" + "=" * 50)
    print("11. 便捷函数示例")
    print("=" * 50)
    
    # 快速获取随机谜语
    print("\n使用 get_random_riddle()：")
    riddle = get_random_riddle()
    print(f"谜面：{riddle.question[:50]}...")
    print(f"答案：{riddle.answer}")
    
    # 带参数获取
    print("\n带参数获取：")
    riddle = get_random_riddle(difficulty=1, language="zh")  # 简单中文谜语
    print(f"谜面：{riddle.question}")
    
    # 获取每日谜语
    print("\n使用 get_daily_riddle()：")
    daily = get_daily_riddle()
    print(f"谜面：{daily.question[:50]}...")
    
    # 快速检查答案
    manager = RiddleManager()
    test_riddle = manager.get_random()
    print("\n使用 check_riddle_answer()：")
    is_correct, feedback = check_riddle_answer(test_riddle.id, test_riddle.answer)
    print(f"答案 '{test_riddle.answer}': {feedback}")


def example_answer_validation():
    """答案验证详细示例"""
    print("\n" + "=" * 50)
    print("12. 答案验证详细示例")
    print("=" * 50)
    
    manager = RiddleManager()
    riddle = manager.get_riddle("zh_obj_001")  # 答案是"西瓜"
    
    print(f"\n谜面：{riddle.question}")
    print(f"正确答案：{riddle.answer}")
    
    test_cases = [
        ("西瓜", "完全正确"),
        ("西 瓜", "带空格"),
        ("西瓜！", "带标点"),
        ("大西瓜", "不正确但有相似"),
        ("苹果", "完全错误"),
    ]
    
    print("\n答案验证测试：")
    for answer, description in test_cases:
        is_correct, feedback = manager.check_answer(riddle.id, answer)
        status = "✅" if is_correct else "❌"
        print(f"{status} '{answer}' ({description}): {feedback}")


def main():
    """运行所有示例"""
    print("╔" + "═" * 48 + "╗")
    print("║" + " " * 12 + "谜语工具库 (riddle_utils)" + " " * 12 + "║")
    print("║" + " " * 48 + "║")
    print("║" + " " * 15 + "使用示例演示" + " " * 15 + "║")
    print("╚" + "═" * 48 + "╝")
    
    example_basic_usage()
    example_category_filter()
    example_difficulty_levels()
    example_language_filter()
    example_daily_riddle()
    example_quiz_game()
    example_custom_riddle()
    example_riddle_generator()
    example_search()
    example_statistics()
    example_convenience_functions()
    example_answer_validation()
    
    print("\n" + "=" * 50)
    print("所有示例演示完成！")
    print("=" * 50)


if __name__ == "__main__":
    main()