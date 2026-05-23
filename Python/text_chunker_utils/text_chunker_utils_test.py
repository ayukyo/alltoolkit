# -*- coding: utf-8 -*-
"""
Text Chunker Utilities - 测试模块

测试所有分块策略和功能
"""

import unittest
from mod import (
    TextChunker,
    SlidingWindowChunker,
    TokenAwareChunker,
    RecursiveChunker,
    TextChunk,
    ChunkStrategy,
    chunk_text,
    chunk_for_embedding,
    sliding_window_chunk,
    recursive_chunk
)


class TestTextChunk(unittest.TestCase):
    """TextChunk 数据类测试"""
    
    def test_basic_properties(self):
        """测试基本属性"""
        chunk = TextChunk(
            content="Hello World",
            start_index=0,
            end_index=11,
            chunk_index=0
        )
        
        self.assertEqual(chunk.content, "Hello World")
        self.assertEqual(chunk.start_index, 0)
        self.assertEqual(chunk.end_index, 11)
        self.assertEqual(chunk.chunk_index, 0)
        self.assertEqual(len(chunk), 11)
    
    def test_with_metadata(self):
        """测试带元数据"""
        chunk = TextChunk(
            content="Test",
            start_index=0,
            end_index=4,
            chunk_index=0,
            overlap_previous=10,
            overlap_next=5,
            metadata={"sentence_count": 3}
        )
        
        self.assertEqual(chunk.overlap_previous, 10)
        self.assertEqual(chunk.overlap_next, 5)
        self.assertEqual(chunk.metadata["sentence_count"], 3)
    
    def test_repr(self):
        """测试字符串表示"""
        chunk = TextChunk(
            content="A" * 100,
            start_index=0,
            end_index=100,
            chunk_index=0
        )
        
        repr_str = repr(chunk)
        self.assertIn("TextChunk", repr_str)
        self.assertIn("len=100", repr_str)


class TestTextChunker(unittest.TestCase):
    """TextChunker 测试"""
    
    def setUp(self):
        """测试前准备"""
        self.short_text = "Hello World"
        self.long_text = " ".join(["word"] * 1000)
        self.paragraphs_text = """第一段内容。这是一些测试文本。
        
第二段内容。包含更多文本。
        
第三段内容。用于测试段落分块。"""
    
    def test_chunk_empty_text(self):
        """测试空文本"""
        chunker = TextChunker()
        self.assertEqual(chunker.chunk(""), [])
        self.assertEqual(chunker.chunk("   "), [])
        self.assertEqual(chunker.chunk(None), [])
    
    def test_chunk_short_text(self):
        """测试短文本"""
        chunker = TextChunker(chunk_size=100)
        chunks = chunker.chunk(self.short_text)
        
        self.assertEqual(len(chunks), 1)
        self.assertEqual(chunks[0].content, self.short_text)
    
    def test_chunk_by_character(self):
        """测试按字符分块"""
        chunker = TextChunker(
            strategy=ChunkStrategy.CHARACTER,
            chunk_size=50,
            chunk_overlap=10
        )
        chunks = chunker.chunk(self.long_text)
        
        self.assertTrue(len(chunks) > 1)
        for chunk in chunks:
            self.assertGreater(len(chunk.content), 0)
    
    def test_chunk_by_word(self):
        """测试按单词分块"""
        chunker = TextChunker(
            strategy=ChunkStrategy.WORD,
            chunk_size=10  # 10 words per chunk
        )
        chunks = chunker.chunk(self.long_text)
        
        self.assertTrue(len(chunks) > 1)
        for chunk in chunks:
            # 每个块应该约 10 个单词
            word_count = len(chunk.content.split())
            self.assertLessEqual(word_count, 15)  # 允许一些波动
    
    def test_chunk_by_sentence(self):
        """测试按句子分块"""
        text = "第一句话。第二句话。第三句话。第四句话。第五句话。"
        chunker = TextChunker(
            strategy=ChunkStrategy.SENTENCE,
            chunk_size=20  # 小块大小触发多块
        )
        chunks = chunker.chunk(text)
        
        self.assertTrue(len(chunks) >= 1)
        for chunk in chunks:
            self.assertGreater(len(chunk.content), 0)
    
    def test_chunk_by_paragraph(self):
        """测试按段落分块"""
        chunker = TextChunker(
            strategy=ChunkStrategy.PARAGRAPH,
            chunk_size=100
        )
        chunks = chunker.chunk(self.paragraphs_text)
        
        self.assertTrue(len(chunks) >= 1)
        for chunk in chunks:
            self.assertGreater(len(chunk.content), 0)
    
    def test_chunk_smart(self):
        """测试智能分块"""
        chunker = TextChunker(
            strategy=ChunkStrategy.SMART,
            chunk_size=100
        )
        chunks = chunker.chunk(self.paragraphs_text)
        
        self.assertTrue(len(chunks) >= 1)
        for chunk in chunks:
            self.assertGreater(len(chunk.content), 0)
    
    def test_chunk_semantic(self):
        """测试语义分块"""
        text = """# 标题一
        
这是第一段内容。

```python
print("Hello")
```

- 列表项一
- 列表项二

1. 编号项一
2. 编号项二"""
        
        chunker = TextChunker(
            strategy=ChunkStrategy.SEMANTIC,
            chunk_size=500
        )
        chunks = chunker.chunk(text)
        
        self.assertTrue(len(chunks) >= 1)
        for chunk in chunks:
            self.assertGreater(len(chunk.content), 0)
    
    def test_chunk_iter(self):
        """测试迭代器方式"""
        chunker = TextChunker(chunk_size=50)
        chunks = list(chunker.chunk_iter(self.long_text))
        
        self.assertTrue(len(chunks) > 1)
    
    def test_custom_length_function(self):
        """测试自定义长度函数"""
        def count_words(text):
            return len(text.split())
        
        chunker = TextChunker(
            strategy=ChunkStrategy.CHARACTER,
            chunk_size=10,
            length_function=count_words
        )
        chunks = chunker.chunk(self.long_text)
        
        self.assertTrue(len(chunks) >= 1)
    
    def test_respect_sentence_boundary(self):
        """测试句子边界尊重"""
        text = "第一句话。第二句话。第三句话。"
        chunker = TextChunker(
            strategy=ChunkStrategy.CHARACTER,
            chunk_size=10,
            respect_sentence_boundary=True
        )
        chunks = chunker.chunk(text)
        
        # 检查块边界是否在句子结束处
        for chunk in chunks:
            content = chunk.content
            # 每个块应该以句子结束符结尾（除了可能的最后一个）
            if chunk.chunk_index < len(chunks) - 1:
                self.assertTrue(
                    content.endswith('。') or content.endswith('！') or content.endswith('？'),
                    f"Chunk should end with sentence marker: {content}"
                )
    
    def test_min_chunk_size(self):
        """测试最小块大小"""
        chunker = TextChunker(
            chunk_size=100,
            min_chunk_size=20
        )
        chunks = chunker.chunk(self.short_text)
        
        for chunk in chunks:
            self.assertGreaterEqual(len(chunk.content), 20)


class TestSlidingWindowChunker(unittest.TestCase):
    """SlidingWindowChunker 测试"""
    
    def test_sliding_window(self):
        """测试滑动窗口分块"""
        text = "A" * 100
        chunker = SlidingWindowChunker(
            window_size=30,
            step_size=10
        )
        chunks = chunker.chunk(text)
        
        self.assertTrue(len(chunks) > 1)
        
        # 检查窗口大小
        for chunk in chunks:
            self.assertLessEqual(len(chunk.content), 30)
        
        # 检查重叠
        if len(chunks) >= 2:
            self.assertGreater(chunks[1].overlap_previous, 0)
    
    def test_sliding_window_empty(self):
        """测试空文本"""
        chunker = SlidingWindowChunker()
        self.assertEqual(chunker.chunk(""), [])


class TestTokenAwareChunker(unittest.TestCase):
    """TokenAwareChunker 测试"""
    
    def test_token_aware_chunking(self):
        """测试 Token 感知分块"""
        text = " ".join(["word"] * 100)
        chunker = TokenAwareChunker(
            max_tokens=10,  # 约 40 字符
            chars_per_token=4.0
        )
        chunks = chunker.chunk(text)
        
        self.assertTrue(len(chunks) >= 1)
        for chunk in chunks:
            estimated_tokens = chunk.metadata.get('estimated_tokens', 0)
            self.assertGreater(estimated_tokens, 0)
    
    def test_custom_tokenizer(self):
        """测试自定义 tokenizer"""
        def custom_tokenizer(text):
            # 简单的按空格分割
            return len(text.split())
        
        text = "word " * 100
        chunker = TokenAwareChunker(
            max_tokens=10,
            tokenizer=custom_tokenizer
        )
        chunks = chunker.chunk(text)
        
        self.assertTrue(len(chunks) >= 1)
    
    def test_count_tokens(self):
        """测试 token 计数"""
        chunker = TokenAwareChunker(chars_per_token=4.0)
        
        # 100 字符应该约 25 tokens
        tokens = chunker.count_tokens("A" * 100)
        self.assertEqual(tokens, 25)


class TestRecursiveChunker(unittest.TestCase):
    """RecursiveChunker 测试"""
    
    def test_recursive_chunking(self):
        """测试递归分块"""
        text = "段落一。\n\n段落二。\n\n段落三。"
        chunker = RecursiveChunker(
            chunk_size=20,
            chunk_overlap=5
        )
        chunks = chunker.chunk(text)
        
        self.assertTrue(len(chunks) >= 1)
        for chunk in chunks:
            self.assertGreater(len(chunk.content), 0)
    
    def test_custom_separators(self):
        """测试自定义分隔符"""
        text = "A|B|C|D|E"
        chunker = RecursiveChunker(
            chunk_size=5,
            separators=["|", ""]
        )
        chunks = chunker.chunk(text)
        
        self.assertTrue(len(chunks) >= 1)


class TestConvenienceFunctions(unittest.TestCase):
    """便捷函数测试"""
    
    def test_chunk_text(self):
        """测试 chunk_text 函数"""
        text = "这是一段测试文本。" * 50
        chunks = chunk_text(
            text,
            strategy="smart",
            chunk_size=50,
            chunk_overlap=10
        )
        
        self.assertTrue(len(chunks) >= 1)
    
    def test_chunk_for_embedding(self):
        """测试 chunk_for_embedding 函数"""
        text = " ".join(["word"] * 100)
        chunks = chunk_for_embedding(
            text,
            max_tokens=20,
            overlap_tokens=5
        )
        
        self.assertTrue(len(chunks) >= 1)
    
    def test_sliding_window_chunk(self):
        """测试 sliding_window_chunk 函数"""
        text = "A" * 100
        chunks = sliding_window_chunk(
            text,
            window_size=30,
            step_size=15
        )
        
        self.assertTrue(len(chunks) > 1)
    
    def test_recursive_chunk(self):
        """测试 recursive_chunk 函数"""
        text = "段落一。\n\n段落二。\n\n段落三。"
        chunks = recursive_chunk(
            text,
            chunk_size=20,
            chunk_overlap=5
        )
        
        self.assertTrue(len(chunks) >= 1)


class TestEdgeCases(unittest.TestCase):
    """边界情况测试"""
    
    def test_single_character(self):
        """测试单字符文本"""
        chunker = TextChunker(chunk_size=10)
        chunks = chunker.chunk("A")
        
        self.assertEqual(len(chunks), 1)
        self.assertEqual(chunks[0].content, "A")
    
    def test_exact_chunk_size(self):
        """测试恰好等于块大小"""
        chunker = TextChunker(chunk_size=10, chunk_overlap=0)
        chunks = chunker.chunk("A" * 10)
        
        self.assertEqual(len(chunks), 1)
    
    def test_unicode_text(self):
        """测试 Unicode 文本"""
        text = "你好世界！这是中文测试。日本語テストもします。한국어도 테스트합니다。"
        chunker = TextChunker(chunk_size=20)
        chunks = chunker.chunk(text)
        
        self.assertTrue(len(chunks) >= 1)
        for chunk in chunks:
            self.assertGreater(len(chunk.content), 0)
    
    def test_mixed_language(self):
        """测试混合语言"""
        text = "Hello world! 你好世界！Hola mundo! こんにちは世界!"
        chunker = TextChunker(chunk_size=20)
        chunks = chunker.chunk(text)
        
        self.assertTrue(len(chunks) >= 1)
    
    def test_code_blocks(self):
        """测试代码块"""
        text = """这是一段代码：

```python
def hello():
    print("Hello, World!")
    return 42
```

代码结束。"""
        
        chunker = TextChunker(
            strategy=ChunkStrategy.SEMANTIC,
            chunk_size=100
        )
        chunks = chunker.chunk(text)
        
        self.assertTrue(len(chunks) >= 1)
    
    def test_markdown_headers(self):
        """测试 Markdown 标题"""
        text = """# 主标题

## 子标题一

内容一。

## 子标题二

内容二。"""
        
        chunker = TextChunker(
            strategy=ChunkStrategy.SEMANTIC,
            chunk_size=50
        )
        chunks = chunker.chunk(text)
        
        self.assertTrue(len(chunks) >= 1)
    
    def test_large_overlap(self):
        """测试大重叠"""
        chunker = TextChunker(
            chunk_size=50,
            chunk_overlap=40
        )
        chunks = chunker.chunk("A" * 200)
        
        self.assertTrue(len(chunks) >= 1)
    
    def test_very_small_chunks(self):
        """测试非常小的块"""
        chunker = TextChunker(
            chunk_size=5,
            min_chunk_size=1
        )
        chunks = chunker.chunk("ABCDEFGHIJ")
        
        self.assertTrue(len(chunks) >= 1)


class TestChunkStrategy(unittest.TestCase):
    """ChunkStrategy 枚举测试"""
    
    def test_enum_values(self):
        """测试枚举值"""
        self.assertEqual(ChunkStrategy.CHARACTER.value, "character")
        self.assertEqual(ChunkStrategy.WORD.value, "word")
        self.assertEqual(ChunkStrategy.SENTENCE.value, "sentence")
        self.assertEqual(ChunkStrategy.PARAGRAPH.value, "paragraph")
        self.assertEqual(ChunkStrategy.SMART.value, "smart")
        self.assertEqual(ChunkStrategy.SEMANTIC.value, "semantic")


if __name__ == '__main__':
    unittest.main()