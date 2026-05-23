# -*- coding: utf-8 -*-
"""
Text Chunker Utilities - 使用示例

展示各种分块策略的使用方法
"""

from mod import (
    TextChunker,
    SlidingWindowChunker,
    TokenAwareChunker,
    RecursiveChunker,
    ChunkStrategy,
    TextChunk,
    chunk_text,
    chunk_for_embedding,
    sliding_window_chunk,
    recursive_chunk
)


def print_chunks(chunks: list, title: str = "Chunks"):
    """打印分块结果"""
    print(f"\n{'='*60}")
    print(f"{title}")
    print(f"{'='*60}")
    print(f"总计 {len(chunks)} 个块\n")
    
    for i, chunk in enumerate(chunks):
        print(f"--- Chunk {i} ---")
        print(f"长度: {len(chunk)} 字符")
        print(f"位置: [{chunk.start_index}, {chunk.end_index}]")
        if chunk.metadata:
            print(f"元数据: {chunk.metadata}")
        preview = chunk.content[:100] + "..." if len(chunk.content) > 100 else chunk.content
        print(f"内容: {preview!r}")
        print()


def example_basic_chunking():
    """基本分块示例"""
    print("\n" + "="*60)
    print("基本分块示例")
    print("="*60)
    
    text = """
    人工智能（Artificial Intelligence，简称 AI）是计算机科学的一个分支，
    旨在创建能够执行通常需要人类智能的任务的系统。这些任务包括学习、推理、
    问题解决、感知、语言理解等。人工智能技术已经广泛应用于各个领域，
    包括医疗诊断、自动驾驶、金融分析、智能客服等。
    
    机器学习是人工智能的一个子领域，专注于开发能够从数据中学习的算法。
    深度学习是机器学习的一个分支，使用神经网络进行学习。这些技术正在
    彻底改变我们与技术互动的方式。
    """
    
    # 创建分块器
    chunker = TextChunker(
        strategy=ChunkStrategy.SMART,
        chunk_size=100,
        chunk_overlap=20
    )
    
    # 分块
    chunks = chunker.chunk(text)
    print_chunks(chunks, "智能分块结果")


def example_character_chunking():
    """按字符分块示例"""
    print("\n" + "="*60)
    print("按字符分块示例")
    print("="*60)
    
    text = "这是一段用于测试按字符分块的文本。" * 10
    
    chunker = TextChunker(
        strategy=ChunkStrategy.CHARACTER,
        chunk_size=50,
        chunk_overlap=10,
        respect_sentence_boundary=True
    )
    
    chunks = chunker.chunk(text)
    print_chunks(chunks, "字符分块结果（尊重句子边界）")


def example_word_chunking():
    """按单词分块示例"""
    print("\n" + "="*60)
    print("按单词分块示例")
    print("="*60)
    
    text = """
    Machine learning is a subset of artificial intelligence that enables 
    systems to learn and improve from experience without being explicitly 
    programmed. It focuses on developing computer programs that can access 
    data and use it to learn for themselves.
    """
    
    chunker = TextChunker(
        strategy=ChunkStrategy.WORD,
        chunk_size=15  # 每块约 15 个单词
    )
    
    chunks = chunker.chunk(text)
    print_chunks(chunks, "单词分块结果")


def example_sentence_chunking():
    """按句子分块示例"""
    print("\n" + "="*60)
    print("按句子分块示例")
    print("="*60)
    
    text = """
    人工智能正在改变世界。从自动驾驶汽车到智能家居，AI 技术无处不在。
    机器学习是 AI 的核心技术之一。它让计算机能够从数据中学习模式。
    深度学习是机器学习的子领域。它使用多层神经网络来处理复杂问题。
    自然语言处理让计算机能够理解人类语言。这项技术被广泛应用于翻译和语音识别。
    """
    
    chunker = TextChunker(
        strategy=ChunkStrategy.SENTENCE,
        chunk_size=50
    )
    
    chunks = chunker.chunk(text)
    print_chunks(chunks, "句子分块结果")


def example_paragraph_chunking():
    """按段落分块示例"""
    print("\n" + "="*60)
    print("按段落分块示例")
    print("="*60)
    
    text = """
    第一段：人工智能（AI）是计算机科学的一个分支，旨在创建智能机器。
    它是研究、开发用于模拟、延伸和扩展人的智能的理论、方法、技术及应用系统的一门新的技术科学。
    
    第二段：机器学习是实现人工智能的一种方法。它使用算法来解析数据，
    从中学习，然后对现实世界中的事件做出决策和预测。
    
    第三段：深度学习是机器学习的子集，它使用人工神经网络来模拟人脑的工作方式。
    深度学习已经在图像识别、语音识别和自然语言处理等领域取得了突破性进展。
    
    第四段：自然语言处理（NLP）是人工智能的重要分支，专注于让计算机理解、
    解释和生成人类语言。NLP 技术被广泛应用于搜索引擎、翻译系统和聊天机器人。
    """
    
    chunker = TextChunker(
        strategy=ChunkStrategy.PARAGRAPH,
        chunk_size=200
    )
    
    chunks = chunker.chunk(text)
    print_chunks(chunks, "段落分块结果")


def example_smart_chunking():
    """智能分块示例"""
    print("\n" + "="*60)
    print("智能分块示例")
    print("="*60)
    
    text = """
    # 人工智能导论
    
    人工智能（Artificial Intelligence，简称 AI）是计算机科学的一个分支。
    它旨在创建能够执行通常需要人类智能的任务的系统。
    
    ## 机器学习
    
    机器学习是人工智能的核心技术。它包括：
    - 监督学习
    - 无监督学习
    - 强化学习
    
    ## 深度学习
    
    深度学习使用神经网络处理复杂问题。
    
    ```python
    import torch
    model = torch.nn.Linear(10, 1)
    ```
    
    深度学习已经在多个领域取得突破。
    """
    
    chunker = TextChunker(
        strategy=ChunkStrategy.SMART,
        chunk_size=100
    )
    
    chunks = chunker.chunk(text)
    print_chunks(chunks, "智能分块结果")


def example_semantic_chunking():
    """语义分块示例"""
    print("\n" + "="*60)
    print("语义分块示例")
    print("="*60)
    
    text = """
    # 第一章：简介
    
    这是简介部分的内容。
    
    ## 1.1 背景
    
    背景内容介绍。
    
    # 第二章：方法论
    
    这是方法论部分。
    
    ```python
    def train_model(data):
        # 训练模型的代码
        return model
    ```
    
    - 第一步：数据预处理
    - 第二步：特征提取
    - 第三步：模型训练
    
    1. 数据收集
    2. 数据清洗
    3. 模型评估
    """
    
    chunker = TextChunker(
        strategy=ChunkStrategy.SEMANTIC,
        chunk_size=100
    )
    
    chunks = chunker.chunk(text)
    print_chunks(chunks, "语义分块结果")


def example_sliding_window():
    """滑动窗口分块示例"""
    print("\n" + "="*60)
    print("滑动窗口分块示例")
    print("="*60)
    
    text = "这是一段用于测试滑动窗口分块的文本。" * 20
    
    chunker = SlidingWindowChunker(
        window_size=50,
        step_size=25
    )
    
    chunks = chunker.chunk(text)
    print_chunks(chunks, "滑动窗口分块结果")
    
    # 显示重叠
    print("重叠分析：")
    for i, chunk in enumerate(chunks):
        if i > 0:
            print(f"  Chunk {i} 与前一块重叠: {chunk.overlap_previous} 字符")
        if i < len(chunks) - 1:
            print(f"  Chunk {i} 与后一块重叠: {chunk.overlap_next} 字符")


def example_token_aware():
    """Token 感知分块示例"""
    print("\n" + "="*60)
    print("Token 感知分块示例")
    print("="*60)
    
    text = """
    人工智能（AI）是计算机科学的一个分支，旨在创建智能机器。
    机器学习是 AI 的核心技术，它使用算法来解析数据、学习模式，
    并做出决策。深度学习是机器学习的子集，使用神经网络模拟人脑。
    自然语言处理让计算机能够理解人类语言，广泛应用于翻译和对话系统。
    """
    
    chunker = TokenAwareChunker(
        max_tokens=50,  # 每块最多 50 个 token
        overlap_tokens=10,  # 重叠 10 个 token
        chars_per_token=2.0  # 中文约 2 字符/token
    )
    
    chunks = chunker.chunk(text)
    print_chunks(chunks, "Token 感知分块结果")
    
    # 显示 token 估算
    print("Token 估算：")
    for chunk in chunks:
        tokens = chunk.metadata.get('estimated_tokens', 0)
        print(f"  Chunk {chunk.chunk_index}: 约 {tokens} tokens")


def example_recursive():
    """递归分块示例"""
    print("\n" + "="*60)
    print("递归分块示例")
    print("="*60)
    
    text = """
    第一节：介绍
    
    这是介绍部分的内容。包含一些基本信息。
    
    第二节：详细说明
    
    这里是详细说明的内容。
    包含更多的细节描述。
    
    第三节：总结
    
    这是总结部分。回顾了前面介绍的内容。
    """
    
    chunker = RecursiveChunker(
        chunk_size=50,
        chunk_overlap=10,
        separators=["\n\n", "\n", "。", ""]
    )
    
    chunks = chunker.chunk(text)
    print_chunks(chunks, "递归分块结果")


def example_convenience_functions():
    """便捷函数示例"""
    print("\n" + "="*60)
    print("便捷函数示例")
    print("="*60)
    
    text = "这是一段测试文本。" * 50
    
    # 1. 基本分块
    print("\n1. chunk_text() - 基本分块")
    chunks = chunk_text(text, strategy="smart", chunk_size=50)
    print(f"   生成 {len(chunks)} 个块")
    
    # 2. 嵌入分块
    print("\n2. chunk_for_embedding() - 为嵌入分块")
    chunks = chunk_for_embedding(text, max_tokens=100)
    print(f"   生成 {len(chunks)} 个块")
    
    # 3. 滑动窗口
    print("\n3. sliding_window_chunk() - 滑动窗口")
    chunks = sliding_window_chunk(text, window_size=50, step_size=25)
    print(f"   生成 {len(chunks)} 个块")
    
    # 4. 递归分块
    print("\n4. recursive_chunk() - 递归分块")
    chunks = recursive_chunk(text, chunk_size=50)
    print(f"   生成 {len(chunks)} 个块")


def example_llm_application():
    """LLM 应用示例"""
    print("\n" + "="*60)
    print("LLM 应用示例 - 长文档处理")
    print("="*60)
    
    # 模拟一篇长文章
    article = """
    # 人工智能的未来发展
    
    人工智能（AI）正在快速发展，并在各个领域产生深远影响。
    本文将探讨 AI 的未来发展趋势和潜在挑战。
    
    ## 技术发展趋势
    
    ### 大语言模型
    
    大语言模型（LLM）如 GPT 系列、Claude、Gemini 等正在改变人机交互方式。
    这些模型能够理解复杂语境、生成高质量文本，并执行多种任务。
    
    ### 多模态 AI
    
    多模态 AI 能够同时处理文本、图像、音频等多种类型的输入。
    这使得 AI 能够更全面地理解世界并进行交互。
    
    ### AI Agent
    
    AI Agent 是能够自主执行任务的智能体。
    它们可以规划、推理、使用工具，并与环境交互。
    
    ## 应用领域
    
    ### 医疗健康
    
    AI 在医疗诊断、药物研发、个性化治疗等方面展现出巨大潜力。
    深度学习算法能够分析医学影像，辅助医生诊断疾病。
    
    ### 金融科技
    
    AI 被广泛应用于风险评估、欺诈检测、智能投顾等领域。
    机器学习模型能够分析海量数据，发现潜在风险和机会。
    
    ### 自动驾驶
    
    自动驾驶技术是 AI 的一个重要应用领域。
    计算机视觉和深度学习使得汽车能够感知环境并做出决策。
    
    ## 挑战与展望
    
    ### 伦理问题
    
    AI 的发展带来了诸多伦理挑战，包括隐私保护、算法偏见、就业影响等。
    如何确保 AI 的发展造福全人类是一个重要课题。
    
    ### 技术挑战
    
    当前的 AI 技术仍存在局限性，如可解释性、安全性、通用性等问题。
    研究人员正在努力解决这些挑战，推动 AI 技术进步。
    
    ## 结论
    
    AI 的未来充满机遇和挑战。通过负责任的发展和应用，
    AI 有望为人类社会带来深远影响，推动科技进步和社会发展。
    """
    
    # 为 LLM 处理分块
    print("方案一：智能分块（推荐）")
    chunker = TextChunker(
        strategy=ChunkStrategy.SMART,
        chunk_size=200,
        chunk_overlap=30
    )
    chunks = chunker.chunk(article)
    print(f"  生成 {len(chunks)} 个块")
    for i, chunk in enumerate(chunks):
        print(f"  Chunk {i}: {len(chunk)} 字符")
    
    print("\n方案二：Token 感知分块（用于嵌入）")
    chunker2 = TokenAwareChunker(
        max_tokens=200,
        overlap_tokens=30,
        chars_per_token=2.0
    )
    chunks2 = chunker2.chunk(article)
    print(f"  生成 {len(chunks2)} 个块")
    
    print("\n方案三：语义分块（保持结构）")
    chunker3 = TextChunker(
        strategy=ChunkStrategy.SEMANTIC,
        chunk_size=300
    )
    chunks3 = chunker3.chunk(article)
    print(f"  生成 {len(chunks3)} 个块")
    for i, chunk in enumerate(chunks3):
        semantic_type = chunk.metadata.get('semantic_type', 'text')
        print(f"  Chunk {i}: {semantic_type}, {len(chunk)} 字符")


def example_custom_length_function():
    """自定义长度函数示例"""
    print("\n" + "="*60)
    print("自定义长度函数示例")
    print("="*60)
    
    text = "这是一段用于测试自定义长度函数的文本。" * 20
    
    # 使用单词计数作为长度
    def count_words(t):
        return len(t.split())
    
    chunker = TextChunker(
        strategy=ChunkStrategy.CHARACTER,
        chunk_size=10,  # 10 个单词
        length_function=count_words
    )
    
    chunks = chunker.chunk(text)
    print_chunks(chunks, "按单词数分块结果")


def main():
    """运行所有示例"""
    print("\n" + "="*70)
    print(" Text Chunker Utilities - 使用示例")
    print("="*70)
    
    example_basic_chunking()
    example_character_chunking()
    example_word_chunking()
    example_sentence_chunking()
    example_paragraph_chunking()
    example_smart_chunking()
    example_semantic_chunking()
    example_sliding_window()
    example_token_aware()
    example_recursive()
    example_convenience_functions()
    example_llm_application()
    example_custom_length_function()
    
    print("\n" + "="*70)
    print(" 所有示例完成！")
    print("="*70)


if __name__ == "__main__":
    main()