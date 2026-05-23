# -*- coding: utf-8 -*-
"""
Text Chunker Utilities - 文本分块工具

提供多种文本分块策略，适用于 LLM 处理、向量嵌入、文档分割等场景。
支持按字符、单词、句子、段落分块，以及智能重叠分块。
零外部依赖，仅使用 Python 标准库。

Author: AllToolkit
Version: 1.0.0
"""

import re
from typing import List, Tuple, Optional, Callable, Iterator, Dict, Any
from dataclasses import dataclass, field
from enum import Enum
import unicodedata


class ChunkStrategy(Enum):
    """分块策略枚举"""
    CHARACTER = "character"       # 按字符数分块
    WORD = "word"                 # 按单词数分块
    SENTENCE = "sentence"         # 按句子分块
    PARAGRAPH = "paragraph"       # 按段落分块
    SMART = "smart"              # 智能分块（考虑多种边界）
    SEMANTIC = "semantic"        # 语义分块（尝试保持语义完整性）


@dataclass
class TextChunk:
    """文本块数据结构"""
    content: str                          # 块内容
    start_index: int                      # 起始位置（字符索引）
    end_index: int                        # 结束位置（字符索引）
    chunk_index: int                      # 块索引
    overlap_previous: int = 0             # 与前一块的重叠字符数
    overlap_next: int = 0                 # 与后一块的重叠字符数
    metadata: Dict[str, Any] = field(default_factory=dict)  # 元数据
    
    def __len__(self) -> int:
        """返回块长度"""
        return len(self.content)
    
    def __repr__(self) -> str:
        preview = self.content[:50] + "..." if len(self.content) > 50 else self.content
        return f"TextChunk({self.chunk_index}, len={len(self)}, content={preview!r})"


class TextChunker:
    """
    文本分块器
    
    支持多种分块策略，可配置块大小、重叠大小等参数。
    """
    
    def __init__(
        self,
        strategy: ChunkStrategy = ChunkStrategy.SMART,
        chunk_size: int = 500,
        chunk_overlap: int = 50,
        separator: str = "\n\n",
        length_function: Optional[Callable[[str], int]] = None,
        keep_separator: bool = True,
        respect_sentence_boundary: bool = True,
        min_chunk_size: int = 50
    ):
        """
        初始化文本分块器
        
        Args:
            strategy: 分块策略
            chunk_size: 块大小（字符数或单词数，取决于策略）
            chunk_overlap: 块重叠大小
            separator: 分隔符（用于段落分块）
            length_function: 自定义长度计算函数
            keep_separator: 是否保留分隔符
            respect_sentence_boundary: 是否尊重句子边界
            min_chunk_size: 最小块大小
        """
        self.strategy = strategy
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.separator = separator
        self.length_function = length_function or len
        self.keep_separator = keep_separator
        self.respect_sentence_boundary = respect_sentence_boundary
        self.min_chunk_size = min_chunk_size
    
    def chunk(self, text: str) -> List[TextChunk]:
        """
        将文本分块
        
        Args:
            text: 要分块的文本
            
        Returns:
            文本块列表
        """
        if not text or not text.strip():
            return []
        
        strategy_map = {
            ChunkStrategy.CHARACTER: self._chunk_by_character,
            ChunkStrategy.WORD: self._chunk_by_word,
            ChunkStrategy.SENTENCE: self._chunk_by_sentence,
            ChunkStrategy.PARAGRAPH: self._chunk_by_paragraph,
            ChunkStrategy.SMART: self._chunk_smart,
            ChunkStrategy.SEMANTIC: self._chunk_semantic,
        }
        
        return strategy_map[self.strategy](text)
    
    def chunk_iter(self, text: str) -> Iterator[TextChunk]:
        """
        迭代器方式返回文本块
        
        Args:
            text: 要分块的文本
            
        Yields:
            文本块
        """
        yield from self.chunk(text)
    
    def _chunk_by_character(self, text: str) -> List[TextChunk]:
        """按字符数分块"""
        chunks = []
        start = 0
        chunk_index = 0
        
        while start < len(text):
            end = min(start + self.chunk_size, len(text))
            
            # 如果尊重句子边界且不是最后一块
            if self.respect_sentence_boundary and end < len(text):
                # 向后查找句子边界
                boundary = self._find_sentence_boundary(text, end, forward=True)
                if boundary > start:
                    end = boundary
            
            content = text[start:end].strip()
            if content and len(content) >= self.min_chunk_size:
                overlap_prev = min(self.chunk_overlap, start) if start > 0 else 0
                overlap_next = min(self.chunk_overlap, len(text) - end) if end < len(text) else 0
                
                chunks.append(TextChunk(
                    content=content,
                    start_index=start,
                    end_index=end,
                    chunk_index=chunk_index,
                    overlap_previous=overlap_prev,
                    overlap_next=overlap_next
                ))
                chunk_index += 1
            
            # 计算下一个起始位置（考虑重叠）
            start = max(start + 1, end - self.chunk_overlap)
        
        return chunks
    
    def _chunk_by_word(self, text: str) -> List[TextChunk]:
        """按单词数分块"""
        words = self._split_words(text)
        if not words:
            return []
        
        chunks = []
        chunk_index = 0
        
        i = 0
        while i < len(words):
            # 收集单词直到达到大小限制
            chunk_words = []
            char_count = 0
            start_pos = words[i][1]  # 起始字符位置
            
            while i < len(words) and len(chunk_words) < self.chunk_size:
                word, pos, word_len = words[i]
                chunk_words.append(word)
                char_count += word_len + 1  # +1 for space
                i += 1
            
            if chunk_words:
                end_pos = words[i-1][1] + words[i-1][2] if i > 0 else start_pos
                
                content = text[start_pos:end_pos].strip()
                if content and len(content) >= self.min_chunk_size:
                    overlap_prev = min(self.chunk_overlap, len(' '.join(chunk_words[:self.chunk_overlap//5]))) if chunks else 0
                    
                    chunks.append(TextChunk(
                        content=content,
                        start_index=start_pos,
                        end_index=end_pos,
                        chunk_index=chunk_index,
                        overlap_previous=overlap_prev
                    ))
                    chunk_index += 1
                
                # 回退以创建重叠
                if self.chunk_overlap > 0 and i < len(words):
                    i = max(0, i - self.chunk_overlap // 5)
        
        return chunks
    
    def _chunk_by_sentence(self, text: str) -> List[TextChunk]:
        """按句子分块"""
        sentences = self._split_sentences(text)
        if not sentences:
            return []
        
        chunks = []
        current_sentences = []
        current_length = 0
        chunk_index = 0
        start_index = 0
        
        for i, (sentence, start, end) in enumerate(sentences):
            sentence_len = self.length_function(sentence)
            
            if current_length + sentence_len > self.chunk_size and current_sentences:
                # 创建块
                content = ' '.join(current_sentences)
                chunks.append(TextChunk(
                    content=content,
                    start_index=start_index,
                    end_index=sentences[i-1][2] if i > 0 else end,
                    chunk_index=chunk_index,
                    metadata={'sentence_count': len(current_sentences)}
                ))
                chunk_index += 1
                
                # 开始新块（考虑重叠）
                if self.chunk_overlap > 0:
                    # 保留最后几个句子作为重叠
                    overlap_sentences = []
                    overlap_len = 0
                    for s in reversed(current_sentences):
                        s_len = self.length_function(s)
                        if overlap_len + s_len > self.chunk_overlap:
                            break
                        overlap_sentences.insert(0, s)
                        overlap_len += s_len
                    
                    current_sentences = overlap_sentences
                    current_length = overlap_len
                    if overlap_sentences:
                        start_index = sentences[i - len(overlap_sentences)][1]
                else:
                    current_sentences = []
                    current_length = 0
                    start_index = start
            
            current_sentences.append(sentence)
            current_length += sentence_len
        
        # 处理剩余的句子
        if current_sentences:
            content = ' '.join(current_sentences)
            chunks.append(TextChunk(
                content=content,
                start_index=start_index,
                end_index=sentences[-1][2],
                chunk_index=chunk_index,
                metadata={'sentence_count': len(current_sentences)}
            ))
        
        return chunks
    
    def _chunk_by_paragraph(self, text: str) -> List[TextChunk]:
        """按段落分块"""
        paragraphs = self._split_paragraphs(text)
        if not paragraphs:
            return []
        
        chunks = []
        current_paragraphs = []
        current_length = 0
        chunk_index = 0
        start_index = 0
        
        for i, (paragraph, start, end) in enumerate(paragraphs):
            para_len = self.length_function(paragraph)
            
            if current_length + para_len > self.chunk_size and current_paragraphs:
                # 创建块
                separator = self.separator if self.keep_separator else '\n\n'
                content = separator.join(current_paragraphs)
                chunks.append(TextChunk(
                    content=content,
                    start_index=start_index,
                    end_index=paragraphs[i-1][2] if i > 0 else end,
                    chunk_index=chunk_index,
                    metadata={'paragraph_count': len(current_paragraphs)}
                ))
                chunk_index += 1
                
                current_paragraphs = []
                current_length = 0
                start_index = start
            
            current_paragraphs.append(paragraph)
            current_length += para_len
        
        # 处理剩余的段落
        if current_paragraphs:
            separator = self.separator if self.keep_separator else '\n\n'
            content = separator.join(current_paragraphs)
            chunks.append(TextChunk(
                content=content,
                start_index=start_index,
                end_index=paragraphs[-1][2],
                chunk_index=chunk_index,
                metadata={'paragraph_count': len(current_paragraphs)}
            ))
        
        return chunks
    
    def _chunk_smart(self, text: str) -> List[TextChunk]:
        """
        智能分块
        
        综合考虑段落、句子边界，优先在自然边界处分块
        """
        paragraphs = self._split_paragraphs(text)
        if not paragraphs:
            return []
        
        chunks = []
        chunk_index = 0
        
        for paragraph, para_start, para_end in paragraphs:
            # 如果段落本身小于块大小，直接作为一个块
            if self.length_function(paragraph) <= self.chunk_size:
                if chunks and self.length_function(chunks[-1].content) + self.length_function(paragraph) <= self.chunk_size:
                    # 合并到上一个块
                    old_chunk = chunks[-1]
                    new_content = old_chunk.content + '\n\n' + paragraph
                    chunks[-1] = TextChunk(
                        content=new_content,
                        start_index=old_chunk.start_index,
                        end_index=para_end,
                        chunk_index=old_chunk.chunk_index,
                        metadata={**old_chunk.metadata, 'paragraph_count': old_chunk.metadata.get('paragraph_count', 1) + 1}
                    )
                else:
                    chunks.append(TextChunk(
                        content=paragraph,
                        start_index=para_start,
                        end_index=para_end,
                        chunk_index=chunk_index,
                        metadata={'paragraph_count': 1}
                    ))
                    chunk_index += 1
            else:
                # 段落太长，按句子分块
                sentences = self._split_sentences(paragraph)
                current_sentences = []
                current_length = 0
                current_start = para_start
                
                for sentence, sent_start, sent_end in sentences:
                    sent_len = self.length_function(sentence)
                    
                    if current_length + sent_len > self.chunk_size and current_sentences:
                        content = ' '.join(current_sentences)
                        chunks.append(TextChunk(
                            content=content,
                            start_index=current_start,
                            end_index=sentences[sentences.index((sentence, sent_start, sent_end)) - 1][2] if sentences.index((sentence, sent_start, sent_end)) > 0 else sent_end,
                            chunk_index=chunk_index,
                            metadata={'sentence_count': len(current_sentences)}
                        ))
                        chunk_index += 1
                        current_sentences = []
                        current_length = 0
                        current_start = sent_start
                    
                    current_sentences.append(sentence)
                    current_length += sent_len
                
                if current_sentences:
                    content = ' '.join(current_sentences)
                    chunks.append(TextChunk(
                        content=content,
                        start_index=current_start,
                        end_index=para_end,
                        chunk_index=chunk_index,
                        metadata={'sentence_count': len(current_sentences)}
                    ))
                    chunk_index += 1
        
        return chunks
    
    def _chunk_semantic(self, text: str) -> List[TextChunk]:
        """
        语义分块
        
        尝试在语义边界处分块，如标题、列表项、代码块等
        """
        # 首先识别语义边界
        boundaries = self._find_semantic_boundaries(text)
        
        if not boundaries:
            return self._chunk_smart(text)
        
        chunks = []
        chunk_index = 0
        
        for i, (start, end, boundary_type) in enumerate(boundaries):
            content = text[start:end].strip()
            
            if content and len(content) >= self.min_chunk_size:
                # 如果内容太大，继续分割
                if self.length_function(content) > self.chunk_size * 1.5:
                    sub_chunks = TextChunker(
                        strategy=ChunkStrategy.SMART,
                        chunk_size=self.chunk_size,
                        chunk_overlap=self.chunk_overlap
                    ).chunk(content)
                    
                    for sub_chunk in sub_chunks:
                        chunks.append(TextChunk(
                            content=sub_chunk.content,
                            start_index=start + sub_chunk.start_index,
                            end_index=start + sub_chunk.end_index,
                            chunk_index=chunk_index,
                            metadata={'semantic_type': boundary_type, **sub_chunk.metadata}
                        ))
                        chunk_index += 1
                else:
                    chunks.append(TextChunk(
                        content=content,
                        start_index=start,
                        end_index=end,
                        chunk_index=chunk_index,
                        metadata={'semantic_type': boundary_type}
                    ))
                    chunk_index += 1
        
        return chunks
    
    def _split_words(self, text: str) -> List[Tuple[str, int, int]]:
        """
        分割文本为单词，返回 (单词, 起始位置, 长度) 列表
        """
        words = []
        pattern = re.compile(r'\S+')
        
        for match in pattern.finditer(text):
            words.append((match.group(), match.start(), len(match.group())))
        
        return words
    
    def _split_sentences(self, text: str) -> List[Tuple[str, int, int]]:
        """
        分割文本为句子，返回 (句子, 起始位置, 结束位置) 列表
        
        支持中英文句子边界检测
        """
        sentences = []
        
        # 中文句子分隔符
        chinese_endings = r'[。！？；；…]+'
        # 英文句子分隔符
        english_endings = r'[.!?]+'
        # 合并分隔符模式
        pattern = re.compile(
            rf'[^。！？；…\.!?]+(?:{chinese_endings}|{english_endings}|\n+|$)',
            re.UNICODE
        )
        
        for match in pattern.finditer(text):
            sentence = match.group().strip()
            if sentence:
                sentences.append((sentence, match.start(), match.end()))
        
        return sentences
    
    def _split_paragraphs(self, text: str) -> List[Tuple[str, int, int]]:
        """
        分割文本为段落，返回 (段落, 起始位置, 结束位置) 列表
        """
        paragraphs = []
        
        # 按空行分割
        para_pattern = re.compile(r'[^\n]+(?:\n[^\n]+)*', re.MULTILINE)
        
        for match in para_pattern.finditer(text):
            paragraph = match.group().strip()
            if paragraph:
                paragraphs.append((paragraph, match.start(), match.end()))
        
        return paragraphs
    
    def _find_sentence_boundary(self, text: str, position: int, forward: bool = True) -> int:
        """
        查找最近的句子边界
        
        Args:
            text: 文本
            position: 起始位置
            forward: 是否向前查找
            
        Returns:
            句子边界位置
        """
        # 句子结束标记
        sentence_enders = '。！？.!?\n'
        
        if forward:
            for i in range(position, min(position + 200, len(text))):
                if text[i] in sentence_enders:
                    return i + 1
        else:
            for i in range(position, max(0, position - 200), -1):
                if text[i] in sentence_enders:
                    return i + 1
        
        return position
    
    def _find_semantic_boundaries(self, text: str) -> List[Tuple[int, int, str]]:
        """
        识别语义边界
        
        Returns:
            (起始位置, 结束位置, 边界类型) 列表
        """
        boundaries = []
        
        # 匹配 Markdown 标题
        header_pattern = re.compile(r'^#{1,6}\s+.+$', re.MULTILINE)
        
        # 匹配代码块
        code_pattern = re.compile(r'```[\s\S]*?```', re.MULTILINE)
        
        # 匹配列表
        list_pattern = re.compile(r'(?:^[\*\-\+]\s+.+$\n?)+', re.MULTILINE)
        
        # 匹配编号列表
        numbered_list_pattern = re.compile(r'(?:^\d+\.\s+.+$\n?)+', re.MULTILINE)
        
        # 标记所有匹配
        used_ranges = set()
        
        for match in header_pattern.finditer(text):
            start, end = match.start(), match.end()
            if not any(start < r_end and end > r_start for r_start, r_end in used_ranges):
                # 标题到下一个标题或文档结束
                next_match = header_pattern.search(text, end)
                block_end = next_match.start() if next_match else len(text)
                boundaries.append((start, block_end, 'header'))
                used_ranges.add((start, block_end))
        
        for match in code_pattern.finditer(text):
            start, end = match.start(), match.end()
            if not any(start < r_end and end > r_start for r_start, r_end in used_ranges):
                boundaries.append((start, end, 'code'))
                used_ranges.add((start, end))
        
        for match in list_pattern.finditer(text):
            start, end = match.start(), match.end()
            if not any(start < r_end and end > r_start for r_start, r_end in used_ranges):
                boundaries.append((start, end, 'list'))
                used_ranges.add((start, end))
        
        for match in numbered_list_pattern.finditer(text):
            start, end = match.start(), match.end()
            if not any(start < r_end and end > r_start for r_start, r_end in used_ranges):
                boundaries.append((start, end, 'numbered_list'))
                used_ranges.add((start, end))
        
        # 填充剩余文本
        boundaries.sort(key=lambda x: x[0])
        
        filled_boundaries = []
        last_end = 0
        
        for start, end, boundary_type in boundaries:
            if start > last_end:
                # 添加普通文本
                filled_boundaries.append((last_end, start, 'text'))
            filled_boundaries.append((start, end, boundary_type))
            last_end = end
        
        if last_end < len(text):
            filled_boundaries.append((last_end, len(text), 'text'))
        
        return filled_boundaries


class SlidingWindowChunker:
    """
    滑动窗口分块器
    
    使用滑动窗口方式分块，适用于向量嵌入场景
    """
    
    def __init__(
        self,
        window_size: int = 500,
        step_size: int = 250,
        length_function: Optional[Callable[[str], int]] = None
    ):
        """
        初始化滑动窗口分块器
        
        Args:
            window_size: 窗口大小（字符数）
            step_size: 步长（字符数）
            length_function: 自定义长度计算函数
        """
        self.window_size = window_size
        self.step_size = step_size
        self.length_function = length_function or len
    
    def chunk(self, text: str) -> List[TextChunk]:
        """
        滑动窗口分块
        
        Args:
            text: 要分块的文本
            
        Returns:
            文本块列表
        """
        if not text:
            return []
        
        chunks = []
        start = 0
        chunk_index = 0
        
        while start < len(text):
            end = min(start + self.window_size, len(text))
            content = text[start:end]
            
            chunks.append(TextChunk(
                content=content,
                start_index=start,
                end_index=end,
                chunk_index=chunk_index,
                overlap_previous=min(self.step_size, start) if start > 0 else 0,
                overlap_next=min(self.window_size - self.step_size, len(text) - end) if end < len(text) else 0
            ))
            
            chunk_index += 1
            start += self.step_size
            
            if start >= len(text):
                break
        
        return chunks


class TokenAwareChunker:
    """
    Token 感知分块器
    
    基于估算的 token 数量进行分块
    """
    
    def __init__(
        self,
        max_tokens: int = 512,
        overlap_tokens: int = 50,
        chars_per_token: float = 4.0,  # 估算：平均每个 token 约 4 个字符
        tokenizer: Optional[Callable[[str], int]] = None
    ):
        """
        初始化 Token 感知分块器
        
        Args:
            max_tokens: 每个 chunk 的最大 token 数
            overlap_tokens: 重叠 token 数
            chars_per_token: 每个 token 的平均字符数（用于估算）
            tokenizer: 自定义 tokenizer 函数，返回 token 数量
        """
        self.max_tokens = max_tokens
        self.overlap_tokens = overlap_tokens
        self.chars_per_token = chars_per_token
        self.tokenizer = tokenizer
    
    def count_tokens(self, text: str) -> int:
        """计算文本的 token 数量"""
        if self.tokenizer:
            return self.tokenizer(text)
        return int(len(text) / self.chars_per_token)
    
    def chunk(self, text: str) -> List[TextChunk]:
        """
        基于 token 数量分块
        
        Args:
            text: 要分块的文本
            
        Returns:
            文本块列表
        """
        if not text:
            return []
        
        # 首先估算整个文本的 token 数量
        total_tokens = self.count_tokens(text)
        
        if total_tokens <= self.max_tokens:
            return [TextChunk(
                content=text,
                start_index=0,
                end_index=len(text),
                chunk_index=0,
                metadata={'estimated_tokens': total_tokens}
            )]
        
        chunks = []
        sentences = self._split_sentences(text)
        
        current_chunk_sentences = []
        current_tokens = 0
        current_start = 0
        chunk_index = 0
        
        for sentence, start, end in sentences:
            sentence_tokens = self.count_tokens(sentence)
            
            # 如果单个句子就超过限制，需要进一步分割
            if sentence_tokens > self.max_tokens:
                # 先保存当前块
                if current_chunk_sentences:
                    content = ' '.join(current_chunk_sentences)
                    chunks.append(TextChunk(
                        content=content,
                        start_index=current_start,
                        end_index=start,
                        chunk_index=chunk_index,
                        metadata={'estimated_tokens': current_tokens}
                    ))
                    chunk_index += 1
                    current_chunk_sentences = []
                    current_tokens = 0
                
                # 分割长句子
                sub_chunks = self._split_long_sentence(sentence, start)
                for sub_content, sub_start, sub_end in sub_chunks:
                    chunks.append(TextChunk(
                        content=sub_content,
                        start_index=sub_start,
                        end_index=sub_end,
                        chunk_index=chunk_index,
                        metadata={'estimated_tokens': self.count_tokens(sub_content)}
                    ))
                    chunk_index += 1
                continue
            
            if current_tokens + sentence_tokens > self.max_tokens and current_chunk_sentences:
                # 保存当前块
                content = ' '.join(current_chunk_sentences)
                chunks.append(TextChunk(
                    content=content,
                    start_index=current_start,
                    end_index=end,
                    chunk_index=chunk_index,
                    metadata={'estimated_tokens': current_tokens}
                ))
                chunk_index += 1
                
                # 开始新块（考虑重叠）
                overlap_sentences = []
                overlap_tokens = 0
                for s in reversed(current_chunk_sentences):
                    s_tokens = self.count_tokens(s)
                    if overlap_tokens + s_tokens > self.overlap_tokens:
                        break
                    overlap_sentences.insert(0, s)
                    overlap_tokens += s_tokens
                
                if overlap_sentences:
                    current_chunk_sentences = overlap_sentences
                    current_tokens = overlap_tokens
                    current_start = sentences[sentences.index((sentence, start, end)) - len(overlap_sentences)][1] if sentences.index((sentence, start, end)) >= len(overlap_sentences) else start
                else:
                    current_chunk_sentences = []
                    current_tokens = 0
                    current_start = start
            
            if not current_chunk_sentences:
                current_start = start
            current_chunk_sentences.append(sentence)
            current_tokens += sentence_tokens
        
        # 保存剩余内容
        if current_chunk_sentences:
            content = ' '.join(current_chunk_sentences)
            chunks.append(TextChunk(
                content=content,
                start_index=current_start,
                end_index=len(text),
                chunk_index=chunk_index,
                metadata={'estimated_tokens': current_tokens}
            ))
        
        return chunks
    
    def _split_sentences(self, text: str) -> List[Tuple[str, int, int]]:
        """分割文本为句子"""
        sentences = []
        pattern = re.compile(r'[^。！？；…\.!?]+(?:[。！？；…\.!?]+|\n+|$)', re.UNICODE)
        
        for match in pattern.finditer(text):
            sentence = match.group().strip()
            if sentence:
                sentences.append((sentence, match.start(), match.end()))
        
        return sentences
    
    def _split_long_sentence(self, sentence: str, offset: int) -> List[Tuple[str, int, int]]:
        """分割长句子"""
        chunks = []
        chunk_size = int(self.max_tokens * self.chars_per_token)
        
        start = 0
        while start < len(sentence):
            end = min(start + chunk_size, len(sentence))
            
            # 尝试在词边界处分割
            if end < len(sentence):
                space_pos = sentence.rfind(' ', start, end)
                if space_pos > start:
                    end = space_pos
            
            content = sentence[start:end].strip()
            if content:
                chunks.append((content, offset + start, offset + end))
            
            start = end
        
        return chunks


class RecursiveChunker:
    """
    递归分块器
    
    按照分隔符优先级递归分割文本
    """
    
    def __init__(
        self,
        chunk_size: int = 500,
        chunk_overlap: int = 50,
        separators: Optional[List[str]] = None,
        keep_separator: bool = True
    ):
        """
        初始化递归分块器
        
        Args:
            chunk_size: 块大小
            chunk_overlap: 块重叠大小
            separators: 分隔符列表（按优先级排序）
            keep_separator: 是否保留分隔符
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.separators = separators or ["\n\n", "\n", ". ", " ", ""]
        self.keep_separator = keep_separator
    
    def chunk(self, text: str) -> List[TextChunk]:
        """
        递归分块
        
        Args:
            text: 要分块的文本
            
        Returns:
            文本块列表
        """
        return self._recursive_chunk(text, 0, len(text), 0)
    
    def _recursive_chunk(
        self, 
        text: str, 
        start: int, 
        end: int, 
        chunk_index: int
    ) -> List[TextChunk]:
        """递归分割文本"""
        content = text[start:end]
        
        if len(content) <= self.chunk_size:
            return [TextChunk(
                content=content.strip(),
                start_index=start,
                end_index=end,
                chunk_index=chunk_index
            )]
        
        # 尝试按分隔符分割
        for separator in self.separators:
            if separator and separator in content:
                parts = content.split(separator)
                chunks = []
                current_pos = start
                
                for i, part in enumerate(parts):
                    if not part:
                        current_pos += len(separator)
                        continue
                    
                    part_start = current_pos
                    part_end = current_pos + len(part)
                    
                    if self.keep_separator and i > 0:
                        part_start -= len(separator)
                        part = separator + part
                    
                    if len(part) > self.chunk_size:
                        # 递归分割
                        sub_chunks = self._recursive_chunk(
                            text, part_start, part_end, chunk_index + len(chunks)
                        )
                        chunks.extend(sub_chunks)
                    else:
                        chunks.append(TextChunk(
                            content=part.strip(),
                            start_index=part_start,
                            end_index=part_end,
                            chunk_index=chunk_index + len(chunks)
                        ))
                    
                    current_pos = part_end + len(separator)
                
                if chunks:
                    return self._merge_small_chunks(chunks)
        
        # 如果没有合适的分隔符，强制按字符分割
        return self._force_split(text, start, end, chunk_index)
    
    def _merge_small_chunks(self, chunks: List[TextChunk]) -> List[TextChunk]:
        """合并过小的块"""
        if not chunks:
            return chunks
        
        merged = []
        current_chunk = None
        
        for chunk in chunks:
            if current_chunk is None:
                current_chunk = chunk
            elif len(current_chunk.content) + len(chunk.content) <= self.chunk_size:
                # 合并
                current_chunk = TextChunk(
                    content=current_chunk.content + " " + chunk.content,
                    start_index=current_chunk.start_index,
                    end_index=chunk.end_index,
                    chunk_index=current_chunk.chunk_index
                )
            else:
                merged.append(current_chunk)
                current_chunk = chunk
        
        if current_chunk:
            merged.append(current_chunk)
        
        # 重新编号
        for i, chunk in enumerate(merged):
            merged[i] = TextChunk(
                content=chunk.content,
                start_index=chunk.start_index,
                end_index=chunk.end_index,
                chunk_index=i,
                metadata=chunk.metadata
            )
        
        return merged
    
    def _force_split(
        self, 
        text: str, 
        start: int, 
        end: int, 
        chunk_index: int
    ) -> List[TextChunk]:
        """强制按字符分割"""
        chunks = []
        pos = start
        local_index = chunk_index
        
        while pos < end:
            chunk_end = min(pos + self.chunk_size, end)
            content = text[pos:chunk_end]
            
            chunks.append(TextChunk(
                content=content.strip(),
                start_index=pos,
                end_index=chunk_end,
                chunk_index=local_index,
                overlap_previous=min(self.chunk_overlap, pos - start) if pos > start else 0
            ))
            
            pos = chunk_end - self.chunk_overlap
            local_index += 1
        
        return chunks


# ============================================================================
# 便捷函数
# ============================================================================

def chunk_text(
    text: str,
    strategy: str = "smart",
    chunk_size: int = 500,
    chunk_overlap: int = 50,
    **kwargs
) -> List[TextChunk]:
    """
    便捷函数：将文本分块
    
    Args:
        text: 要分块的文本
        strategy: 分块策略 ("character", "word", "sentence", "paragraph", "smart", "semantic")
        chunk_size: 块大小
        chunk_overlap: 块重叠大小
        **kwargs: 其他参数
        
    Returns:
        文本块列表
    """
    strategy_map = {
        "character": ChunkStrategy.CHARACTER,
        "word": ChunkStrategy.WORD,
        "sentence": ChunkStrategy.SENTENCE,
        "paragraph": ChunkStrategy.PARAGRAPH,
        "smart": ChunkStrategy.SMART,
        "semantic": ChunkStrategy.SEMANTIC,
    }
    
    chunker = TextChunker(
        strategy=strategy_map.get(strategy, ChunkStrategy.SMART),
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        **kwargs
    )
    
    return chunker.chunk(text)


def chunk_for_embedding(
    text: str,
    max_tokens: int = 512,
    overlap_tokens: int = 50
) -> List[TextChunk]:
    """
    便捷函数：为向量嵌入分块
    
    Args:
        text: 要分块的文本
        max_tokens: 每个 chunk 的最大 token 数
        overlap_tokens: 重叠 token 数
        
    Returns:
        文本块列表
    """
    chunker = TokenAwareChunker(
        max_tokens=max_tokens,
        overlap_tokens=overlap_tokens
    )
    
    return chunker.chunk(text)


def sliding_window_chunk(
    text: str,
    window_size: int = 500,
    step_size: int = 250
) -> List[TextChunk]:
    """
    便捷函数：滑动窗口分块
    
    Args:
        text: 要分块的文本
        window_size: 窗口大小
        step_size: 步长
        
    Returns:
        文本块列表
    """
    chunker = SlidingWindowChunker(
        window_size=window_size,
        step_size=step_size
    )
    
    return chunker.chunk(text)


def recursive_chunk(
    text: str,
    chunk_size: int = 500,
    chunk_overlap: int = 50,
    separators: Optional[List[str]] = None
) -> List[TextChunk]:
    """
    便捷函数：递归分块
    
    Args:
        text: 要分块的文本
        chunk_size: 块大小
        chunk_overlap: 块重叠大小
        separators: 分隔符列表
        
    Returns:
        文本块列表
    """
    chunker = RecursiveChunker(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=separators
    )
    
    return chunker.chunk(text)


# ============================================================================
# 模块元数据
# ============================================================================

__version__ = "1.0.0"
__author__ = "AllToolkit"
__all__ = [
    # 枚举
    'ChunkStrategy',
    
    # 数据类
    'TextChunk',
    
    # 分块器类
    'TextChunker',
    'SlidingWindowChunker',
    'TokenAwareChunker',
    'RecursiveChunker',
    
    # 便捷函数
    'chunk_text',
    'chunk_for_embedding',
    'sliding_window_chunk',
    'recursive_chunk',
]