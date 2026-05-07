"""
Wordle 游戏辅助工具示例

演示如何使用 wordle_utils 进行：
- 单词过滤
- 最优猜测计算
- 自动求解
- 字母频率分析
"""

from wordle_utils import (
    WordleHelper,
    WordleSolver,
    filter_words,
    get_best_guess,
    calculate_letter_frequency,
    DEFAULT_WORDS
)


def demo_basic_filtering():
    """演示基本过滤功能"""
    print("=" * 60)
    print("基本过滤示例")
    print("=" * 60)
    
    helper = WordleHelper()
    print(f"词库大小: {len(helper.words)} 词\n")
    
    # 示例1: 已知正确位置的字母
    print("1. 已知第3位是 'a':")
    result = helper.filter_words(correct="..a..")
    print(f"   匹配词数: {len(result)}")
    print(f"   前10个: {result[:10]}\n")
    
    # 示例2: 已知存在但位置不对的字母
    print("2. 已知存在 'e' 但位置不对:")
    result = helper.filter_words(present="e", correct=".....")
    print(f"   匹配词数: {len(result)}")
    print(f"   前10个: {result[:10]}\n")
    
    # 示例3: 已知不存在的字母
    print("3. 不含 'xyz':")
    result = helper.filter_words(absent="xyz")
    print(f"   匹配词数: {len(result)}")
    print(f"   前10个: {result[:10]}\n")
    
    # 示例4: 组合过滤
    print("4. 组合过滤: 第3位 'a'，含 'e'，不含 'xyz':")
    result = helper.filter_words(
        correct="..a..",
        present="e",
        absent="xyz"
    )
    print(f"   匹配词数: {len(result)}")
    print(f"   结果: {result}\n")


def demo_best_guess():
    """演示最优猜测计算"""
    print("=" * 60)
    print("最优猜测示例")
    print("=" * 60)
    
    helper = WordleHelper()
    
    # 示例1: 使用不同方法获取最优猜测
    print("1. 不同方法的最优首词:")
    
    methods = ["frequency", "position", "entropy", "combined"]
    for method in methods:
        word, score = helper.get_best_guess(method=method)
        print(f"   {method:12s}: {word} (得分: {score:.4f})")
    
    print()
    
    # 示例2: 缩小候选后获取最优猜测
    print("2. 缩小候选后的最优猜测:")
    candidates = helper.filter_words(correct="..a..", present="e")
    word, score = helper.get_best_guess(candidates=candidates)
    print(f"   候选词数: {len(candidates)}")
    print(f"   最优猜测: {word} (得分: {score:.4f})")
    print(f"   前10候选: {candidates[:10]}\n")


def demo_frequency_analysis():
    """演示字母频率分析"""
    print("=" * 60)
    print("字母频率分析")
    print("=" * 60)
    
    helper = WordleHelper()
    
    # 字母频率
    freq = helper.letter_frequency
    print("1. 最常见的10个字母:")
    sorted_freq = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    for letter, f in sorted_freq[:10]:
        print(f"   {letter.upper()}: {f:.2%}")
    
    print()
    
    # 位置频率
    pos_freq = helper.position_frequency
    print("2. 各位置最常见的字母:")
    for i, pf in enumerate(pos_freq):
        best_letter = max(pf.items(), key=lambda x: x[1])
        print(f"   位置 {i+1}: {best_letter[0].upper()} ({best_letter[1]:.2%})")
    
    print()


def demo_feedback_analysis():
    """演示反馈分析"""
    print("=" * 60)
    print("反馈分析示例")
    print("=" * 60)
    
    helper = WordleHelper()
    
    # 示例: 分析 "crane" 的反馈 "yybgb"
    # y = 黄色（存在但位置错误）
    # g = 绿色（正确位置）
    # b = 灰色（不存在）
    guess = "crane"
    feedback = "yybgb"  # c黄, r黄, a灰, n绿, e绿
    
    print(f"猜测词: {guess}")
    print(f"反馈:   {feedback}")
    print("(y=黄色/存在位置错误, g=绿色/正确位置, b=灰色/不存在)\n")
    
    conditions = helper.analyze_feedback(guess, feedback)
    print("解析结果:")
    print(f"  正确位置: {conditions['pattern']}")
    print(f"  存在字母: {conditions['present']}")
    print(f"  不存在: {conditions['absent']}")
    
    # 应用过滤
    candidates = helper.filter_words(
        correct=conditions['pattern'],
        present=conditions['present'],
        absent=conditions['absent']
    )
    
    print(f"\n剩余候选词: {len(candidates)}")
    print(f"候选列表: {candidates[:20]}\n")


def demo_game_solver():
    """演示游戏求解器"""
    print("=" * 60)
    print("自动求解示例")
    print("=" * 60)
    
    solver = WordleSolver()
    
    # 示例1: 自动求解一个词
    print("1. 自动求解 'apple':")
    success, attempts, history = solver.auto_solve("apple", verbose=True)
    
    print(f"\n结果: {'成功' if success else '失败'}")
    print(f"尝试次数: {attempts}")
    print(f"历史记录: {len(history)} 条\n")
    
    # 示例2: 求解另一个词
    print("2. 自动求解 'dream':")
    success, attempts, history = solver.auto_solve("dream", verbose=True)
    print(f"\n结果: {'成功' if success else '失败'}\n")


def demo_interactive_game():
    """演示交互式游戏"""
    print("=" * 60)
    print("交互式游戏模拟")
    print("=" * 60)
    
    helper = WordleHelper()
    history = []
    
    # 模拟游戏过程
    print("模拟一个 Wordle 游戏过程:\n")
    
    # 第1步: 获取首词
    first_guess, _ = helper.get_best_guess()
    print(f"第1次猜测: {first_guess}")
    
    # 假设答案是 "flame"，模拟反馈
    answer = "flame"
    feedback = helper._get_pattern(first_guess, answer)
    feedback_display = feedback.replace('2', '🟩').replace('1', '🟨').replace('0', '⬜')
    print(f"反馈: {feedback_display}")
    history.append((first_guess, feedback))
    
    # 第2步: 根据反馈获取下一个猜测
    guess, candidates, count = helper.suggest_next_guess(history)
    print(f"\n第2次猜测: {guess}")
    print(f"剩余候选: {count} 词")
    
    feedback = helper._get_pattern(guess, answer)
    feedback_display = feedback.replace('2', '🟩').replace('1', '🟨').replace('0', '⬜')
    print(f"反馈: {feedback_display}")
    history.append((guess, feedback))
    
    # 继续...
    for i in range(3, 7):
        guess, candidates, count = helper.suggest_next_guess(history)
        if not guess:
            print("无法找到候选词!")
            break
        
        print(f"\n第{i}次猜测: {guess}")
        print(f"剩余候选: {count} 词")
        
        feedback = helper._get_pattern(guess, answer)
        feedback_display = feedback.replace('2', '🟩').replace('1', '🟨').replace('0', '⬜')
        print(f"反馈: {feedback_display}")
        
        if feedback == "22222":
            print(f"\n🎉 成功！用了 {i} 次猜中！")
            break
        
        history.append((guess, feedback))
    else:
        print(f"\n未能在6次内猜中。答案是: {answer}")


def demo_convenience_functions():
    """演示便捷函数"""
    print("=" * 60)
    print("便捷函数示例")
    print("=" * 60)
    
    # filter_words
    print("1. filter_words() - 快速过滤:")
    result = filter_words(correct="..a..", present="e", absent="xyz")
    print(f"   匹配词数: {len(result)}")
    print(f"   前5个: {result[:5]}\n")
    
    # get_best_guess
    print("2. get_best_guess() - 获取最优猜测:")
    word, score = get_best_guess()
    print(f"   推荐: {word} (得分: {score:.4f})\n")
    
    # calculate_letter_frequency
    print("3. calculate_letter_frequency() - 计算字母频率:")
    freq = calculate_letter_frequency()
    sorted_freq = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    print(f"   最常见字母: {', '.join([f'{l}({f:.1%})' for l, f in sorted_freq[:5]])}\n")


def demo_custom_wordlist():
    """演示自定义词库"""
    print("=" * 60)
    print("自定义词库示例")
    print("=" * 60)
    
    # 使用自定义词库
    custom_words = [
        "apple", "beach", "crane", "dream", "eagle",
        "flame", "grape", "house", "ivory", "jolly",
        "knife", "lemon", "magic", "night", "ocean",
        "piano", "queen", "robot", "storm", "tiger"
    ]
    
    helper = WordleHelper(custom_words)
    print(f"自定义词库大小: {len(helper.words)} 词\n")
    
    print("1. 过滤示例:")
    result = helper.filter_words(present="a")
    print(f"   含 'a' 的词: {result}\n")
    
    print("2. 最优猜测:")
    word, score = helper.get_best_guess()
    print(f"   推荐: {word} (得分: {score:.4f})\n")
    
    print("3. 自动求解 'magic':")
    solver = WordleSolver(custom_words)
    solver.auto_solve("magic", verbose=True)


def main():
    """运行所有示例"""
    print("\n" + "🎯" * 20)
    print("Wordle 游戏辅助工具 - 功能演示")
    print("🎯" * 20 + "\n")
    
    demo_basic_filtering()
    demo_best_guess()
    demo_frequency_analysis()
    demo_feedback_analysis()
    demo_game_solver()
    demo_interactive_game()
    demo_convenience_functions()
    demo_custom_wordlist()
    
    print("\n" + "=" * 60)
    print("演示完成!")
    print("=" * 60)


if __name__ == "__main__":
    main()