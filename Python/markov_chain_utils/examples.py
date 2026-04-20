"""
Markov Chain Utils 使用示例

演示各个模块的核心功能
"""

from markov_chain_utils import (
    MarkovChain,
    MarkovTextGenerator,
    SequencePredictor,
    TransitionMatrix
)


def example_markov_chain():
    """马尔可夫链基础示例"""
    print("=" * 50)
    print("MarkovChain 基础示例")
    print("=" * 50)
    
    # 创建一阶马尔可夫链
    mc = MarkovChain(order=1)
    
    # 训练：天气序列 (S=晴天, R=雨天, C=多云)
    weather_sequence = ['S', 'S', 'S', 'R', 'S', 'C', 'S', 'S', 'R', 'R', 
                        'S', 'S', 'C', 'S', 'R', 'S', 'S', 'S', 'R', 'S']
    
    mc.train(weather_sequence)
    
    print(f"\n模型信息: {mc}")
    print(f"状态数量: {mc.num_states}")
    print(f"所有状态: {mc.states}")
    
    # 获取转移概率
    print("\n转移概率:")
    print(f"  P(S|S) = {mc.get_transition_probability(('S',), 'S'):.2f}")
    print(f"  P(R|S) = {mc.get_transition_probability(('S',), 'R'):.2f}")
    print(f"  P(S|R) = {mc.get_transition_probability(('R',), 'S'):.2f}")
    
    # 预测下一个状态
    print("\n预测:")
    print(f"  晴天后的预测: {mc.predict_next(('S',))}")
    print(f"  雨天后的预测: {mc.predict_next(('R',))}")
    
    # 可能的下一状态
    print("\n晴天后可能的下一状态:")
    for state, prob in mc.get_possible_next_states(('S',)):
        print(f"  {state}: {prob:.2%}")
    
    # 生成序列
    print("\n生成天气序列 (10步):")
    generated = mc.generate(start=('S',), steps=10)
    print(f"  {' -> '.join(generated)}")


def example_markov_chain_higher_order():
    """高阶马尔可夫链示例"""
    print("\n" + "=" * 50)
    print("高阶马尔可夫链示例")
    print("=" * 50)
    
    # 二阶马尔可夫链
    mc = MarkovChain(order=2)
    
    # 音符序列 (简化)
    notes = ['C', 'D', 'E', 'F', 'G', 'A', 'G', 'F', 'E', 'D', 'C',
             'C', 'D', 'E', 'F', 'G', 'A', 'G', 'F', 'E', 'D', 'C']
    
    mc.train(notes)
    
    print(f"\n模型: {mc}")
    
    # 生成旋律
    print("\n生成旋律:")
    melody = mc.generate(start=('C', 'D'), steps=15)
    print(f"  {' '.join(melody)}")


def example_text_generator():
    """文本生成器示例"""
    print("\n" + "=" * 50)
    print("MarkovTextGenerator 文本生成示例")
    print("=" * 50)
    
    # 创建单词级生成器
    gen = MarkovTextGenerator(order=2, mode='word')
    
    # 训练文本
    training_text = """
    The quick brown fox jumps over the lazy dog.
    The lazy dog sleeps all day in the warm sun.
    A quick fox runs through the green forest.
    The brown dog plays happily in the park.
    Quick animals run fast in the wild forest.
    The fox is a clever animal in the wild.
    """
    
    gen.train(training_text)
    
    print(f"\n生成器: {gen}")
    print(f"词汇表大小: {gen.vocabulary_size}")
    
    # 生成文本
    print("\n生成句子:")
    for i in range(3):
        sentence = gen.generate_sentence(max_length=15)
        print(f"  {i+1}. {sentence}")
    
    # 续写预测
    print("\n'The quick' 的可能续写:")
    continuations = gen.get_continuations("The quick", top_n=5)
    for word, prob in continuations:
        print(f"  '{word}': {prob:.2%}")
    
    # 不同温度的生成
    print("\n不同温度生成:")
    for temp in [0, 0.5, 1.0, 1.5]:
        text = gen.generate(start="The fox", max_length=8, temperature=temp)
        print(f"  温度 {temp}: {text}")


def example_char_level_generator():
    """字符级生成示例"""
    print("\n" + "=" * 50)
    print("字符级文本生成示例")
    print("=" * 50)
    
    gen = MarkovTextGenerator(order=4, mode='char')
    
    # 训练
    gen.train("hello world hello python hello markov")
    
    print(f"\n生成器: {gen}")
    
    # 生成
    print("\n生成文本:")
    for i in range(3):
        text = gen.generate(start="hell", max_length=20)
        print(f"  {i+1}. {text}")


def example_sequence_predictor():
    """序列预测器示例"""
    print("\n" + "=" * 50)
    print("SequencePredictor 序列预测示例")
    print("=" * 50)
    
    sp = SequencePredictor(order=2)
    
    # 训练数据：网页访问序列
    pages = ['home', 'products', 'cart', 'checkout', 'home',
             'products', 'detail', 'cart', 'checkout', 'home',
             'products', 'cart', 'detail', 'checkout']
    
    sp.train(pages)
    
    print(f"\n预测器: {sp}")
    
    # 预测下一页
    contexts = [
        ['home', 'products'],
        ['products', 'cart'],
        ['cart', 'checkout'],
    ]
    
    print("\n页面预测:")
    for ctx in contexts:
        pred, prob = sp.predict_with_probability(ctx)
        print(f"  {ctx} -> {pred} (置信度: {prob:.2%})")
    
    # 概率分布
    print("\n'home', 'products' 后的页面分布:")
    dist = sp.predict_distribution(['home', 'products'], top_n=5)
    for page, prob in dist:
        print(f"  {page}: {prob:.2%}")
    
    # 多步预测
    print("\n多步预测 (从 'home' 开始):")
    sequence = sp.predict_sequence(['home', 'products'], steps=3)
    print(f"  {' -> '.join(sequence)}")


def example_anomaly_detection():
    """异常检测示例"""
    print("\n" + "=" * 50)
    print("异常检测示例")
    print("=" * 50)
    
    sp = SequencePredictor(order=2)
    
    # 正常用户行为模式
    normal_patterns = [
        ['login', 'view', 'edit', 'save', 'logout'],
        ['login', 'view', 'view', 'edit', 'logout'],
        ['login', 'view', 'edit', 'edit', 'save', 'logout'],
        ['login', 'view', 'view', 'view', 'logout'],
    ]
    
    for pattern in normal_patterns:
        sp.train(pattern)
    
    print(f"预测器: {sp}")
    
    # 检测异常序列
    test_sequences = [
        (['login', 'view', 'edit', 'delete', 'logout'], "包含罕见操作"),
        (['login', 'delete', 'delete', 'logout'], "异常频繁删除"),
        (['login', 'view', 'edit', 'save', 'logout'], "正常模式"),
    ]
    
    print("\n异常检测结果:")
    for seq, desc in test_sequences:
        anomalies = sp.detect_anomaly(seq, threshold=0.2)
        status = "异常" if anomalies else "正常"
        print(f"  {desc}: {status}")
        if anomalies:
            for pos, val, prob in anomalies:
                print(f"    位置 {pos}: '{val}' (概率: {prob:.2%})")


def example_transition_matrix():
    """转移矩阵示例"""
    print("\n" + "=" * 50)
    print("TransitionMatrix 转移矩阵示例")
    print("=" * 50)
    
    tm = TransitionMatrix()
    
    # 添加页面跳转数据
    transitions = [
        ('home', 'products'),
        ('home', 'products'),
        ('home', 'about'),
        ('products', 'detail'),
        ('products', 'detail'),
        ('products', 'cart'),
        ('detail', 'cart'),
        ('detail', 'cart'),
        ('detail', 'cart'),
        ('cart', 'checkout'),
        ('cart', 'products'),
        ('checkout', 'home'),
        ('checkout', 'checkout'),
    ]
    
    for from_state, to_state in transitions:
        tm.add_transition(from_state, to_state)
    
    print(f"\n矩阵: {tm}")
    print(f"状态数: {tm.num_states}")
    print(f"转移总数: {tm.num_transitions}")
    
    # 查看各状态的转移概率
    print("\n转移概率分布:")
    for state in sorted(tm.states):
        row = tm.get_row(state)
        if row:
            print(f"  从 {state}:")
            for to_state, prob in sorted(row.items(), key=lambda x: -x[1]):
                print(f"    -> {to_state}: {prob:.1%}")
    
    # 稳态分布
    print("\n稳态分布:")
    stationary = tm.get_stationary_distribution()
    for state, prob in sorted(stationary.items(), key=lambda x: -x[1]):
        print(f"  {state}: {prob:.2%}")
    
    # 吸收态
    absorbing = tm.get_absorbing_states()
    if absorbing:
        print(f"\n吸收态: {absorbing}")
    
    # 互通类
    classes = tm.get_communicating_classes()
    print(f"\n互通类: {classes}")


def example_frequency_analysis():
    """频繁模式分析示例"""
    print("\n" + "=" * 50)
    print("频繁模式分析示例")
    print("=" * 50)
    
    sp = SequencePredictor(order=2)
    
    # 电商用户行为数据
    behaviors = ['view', 'click', 'view', 'click', 'buy', 'view', 
                 'click', 'buy', 'view', 'click', 'view', 'click', 'buy']
    
    sp.train(behaviors)
    
    print(f"预测器: {sp}")
    
    # 获取频繁模式
    patterns = sp.get_frequent_patterns(min_count=2)
    
    print("\n频繁模式 (出现 >= 2 次):")
    for context, next_val, count in patterns[:5]:
        print(f"  {context} -> {next_val}: {count} 次")


def example_paragraph_generation():
    """段落生成示例"""
    print("\n" + "=" * 50)
    print("段落生成示例")
    print("=" * 50)
    
    gen = MarkovTextGenerator(order=2, mode='word')
    
    # 训练文本（简化的新闻语料）
    news_text = """
    The economy grew significantly this quarter. Stock markets reached new highs.
    Technology companies reported strong earnings. Investors remain optimistic.
    The central bank announced new policies. Economic indicators show growth.
    Technology sector leads the market growth this year.
    """
    
    gen.train(news_text)
    
    print(f"生成器: {gen}")
    
    # 生成段落
    print("\n生成的段落:")
    paragraph = gen.generate_paragraph(num_sentences=3, max_length_per_sentence=10)
    print(f"  {paragraph}")


if __name__ == '__main__':
    # 运行所有示例
    example_markov_chain()
    example_markov_chain_higher_order()
    example_text_generator()
    example_char_level_generator()
    example_sequence_predictor()
    example_anomaly_detection()
    example_transition_matrix()
    example_frequency_analysis()
    example_paragraph_generation()
    
    print("\n" + "=" * 50)
    print("示例运行完成!")
    print("=" * 50)