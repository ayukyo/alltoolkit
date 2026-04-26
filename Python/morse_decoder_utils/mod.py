"""
Morse Code Decoder Utils - Morse码解码工具

功能：
1. 文本 Morse 码解码（支持多种分隔符格式）
2. 音频信号解码（通过波形分析）
3. 自动速率检测
4. 噪声过滤
5. 信号质量分析

零外部依赖，纯 Python 实现
"""

import re
import math
from typing import List, Tuple, Optional, Dict
from collections import Counter


# 国际 Morse 码对照表（解码用）
MORSE_TO_CHAR = {
    '.-': 'A', '-...': 'B', '-.-.': 'C', '-..': 'D', '.': 'E',
    '..-.': 'F', '--.': 'G', '....': 'H', '..': 'I', '.---': 'J',
    '-.-': 'K', '.-..': 'L', '--': 'M', '-.': 'N', '---': 'O',
    '.--.': 'P', '--.-': 'Q', '.-.': 'R', '...': 'S', '-': 'T',
    '..-': 'U', '...-': 'V', '.--': 'W', '-..-': 'X', '-.--': 'Y',
    '--..': 'Z',
    '-----': '0', '.----': '1', '..---': '2', '...--': '3', '....-': '4',
    '.....': '5', '-....': '6', '--...': '7', '---..': '8', '----.': '9',
    '.-.-.-': '.', '--..--': ',', '..--..': '?', '.----.': "'",
    '-.-.--': '!', '-..-.': '/', '-.--.': '(', '-.--.-': ')',
    '.-...': '&', '---...': ':', '-.-.-.': ';', '-...-': '=',
    '.-.-.': '+', '-....-': '-', '..--.-': '_', '.-..-.': '"',
    '...-..-': '$', '.--.-.': '@',
    # 扩展符号
    '.-.-': 'Ä', '.--.-': 'Á', '..-..': 'É', '--.--': 'Ñ',
    '---.': 'Ö', '...-.': 'É', '..--.': 'Ü',
}

# 数字莫尔斯码
NUMBERS_MORSE = {
    '-----': '0', '.----': '1', '..---': '2', '...--': '3', '....-': '4',
    '.....': '5', '-....': '6', '--...': '7', '---..': '8', '----.': '9',
}


class MorseDecoder:
    """Morse码解码器"""
    
    def __init__(self, dot_threshold: float = 0.3):
        """
        初始化解码器
        
        Args:
            dot_threshold: 点划判断阈值（相对于单位时间的比例）
        """
        self.dot_threshold = dot_threshold
        self.stats = {
            'decoded_chars': 0,
            'unknown_chars': 0,
            'signal_quality': 1.0
        }
    
    def decode_text(self, morse: str, 
                    char_sep: str = ' ',
                    word_sep: str = ' / ') -> Tuple[str, Dict]:
        """
        解码文本形式的 Morse 码
        
        Args:
            morse: Morse 码字符串
            char_sep: 字符分隔符（默认空格）
            word_sep: 单词分隔符（默认 ' / '）
        
        Returns:
            (解码后的文本, 统计信息)
        """
        if not morse or not morse.strip():
            return '', {'decoded_chars': 0, 'unknown_chars': 0, 'signal_quality': 1.0}
        
        # 标准化输入
        morse = morse.strip()
        
        # 替换单词分隔符为统一格式
        morse = morse.replace(word_sep, '   ')
        morse = morse.replace('  ', '   ')  # 双空格也视为单词分隔
        
        words = []
        word_parts = morse.split('   ')
        total_chars = 0
        unknown_chars = 0
        
        for word_morse in word_parts:
            if not word_morse.strip():
                continue
            
            chars = []
            char_parts = word_morse.split(char_sep)
            
            for char_morse in char_parts:
                char_morse = char_morse.strip()
                if not char_morse:
                    continue
                
                # 标准化：只保留点和划
                normalized = self._normalize_morse(char_morse)
                
                if normalized in MORSE_TO_CHAR:
                    chars.append(MORSE_TO_CHAR[normalized])
                    total_chars += 1
                else:
                    # 尝试纠错
                    corrected = self._try_correct(normalized)
                    if corrected:
                        chars.append(corrected)
                        total_chars += 1
                    else:
                        chars.append('?')
                        total_chars += 1
                        unknown_chars += 1
            
            if chars:
                words.append(''.join(chars))
        
        # 计算信号质量
        quality = 1.0 - (unknown_chars / total_chars if total_chars > 0 else 0)
        
        stats = {
            'decoded_chars': total_chars,
            'unknown_chars': unknown_chars,
            'signal_quality': quality
        }
        
        self.stats = stats
        return ' '.join(words), stats
    
    def _normalize_morse(self, morse: str) -> str:
        """标准化 Morse 码符号"""
        # 将各种表示统一为 . 和 -
        normalized = morse.upper()
        # Unicode 点符号
        normalized = normalized.replace('•', '.').replace('●', '.')
        normalized = normalized.replace('·', '.').replace('•', '.')
        # Unicode 划符号（包括各种横线）
        normalized = normalized.replace('—', '-')  # em dash
        normalized = normalized.replace('–', '-')  # en dash
        normalized = normalized.replace('−', '-')  # minus sign
        normalized = normalized.replace('―', '-')  # horizontal bar
        normalized = normalized.replace('_', '-')  # underscore
        # 过滤非法字符，只保留点和划
        return re.sub(r'[^.\-]', '', normalized)
    
    def _try_correct(self, morse: str) -> Optional[str]:
        """尝试纠错未知的 Morse 码"""
        if not morse:
            return None
        
        # 尝试反转点划
        inverted = ''.join('.' if c == '-' else '-' for c in morse)
        if inverted in MORSE_TO_CHAR:
            return MORSE_TO_CHAR[inverted]
        
        # 尝试添加/删除一个符号
        for i in range(len(morse) + 1):
            # 添加
            for sym in '.-':
                new_morse = morse[:i] + sym + morse[i:]
                if new_morse in MORSE_TO_CHAR:
                    return MORSE_TO_CHAR[new_morse]
        
        for i in range(len(morse)):
            new_morse = morse[:i] + morse[i+1:]
            if new_morse in MORSE_TO_CHAR:
                return MORSE_TO_CHAR[new_morse]
        
        return None
    
    def decode_signal(self, signal: List[float], 
                       sample_rate: float = 1000.0,
                       threshold: Optional[float] = None) -> Tuple[str, Dict]:
        """
        从信号序列解码 Morse 码
        
        Args:
            signal: 信号强度列表（0-1 或 0-255）
            sample_rate: 采样率（Hz）
            threshold: 信号阈值（自动计算如果 None）
        
        Returns:
            (解码后的文本, 详细统计)
        """
        if not signal:
            return '', {'error': 'Empty signal'}
        
        # 标准化信号
        signal = self._normalize_signal(signal)
        
        # 计算阈值
        if threshold is None:
            threshold = self._auto_threshold(signal)
        
        # 二值化
        binary = [1 if s >= threshold else 0 for s in signal]
        
        # 检测边缘
        edges = self._detect_edges(binary)
        
        # 计算单位时间
        unit_time = self._estimate_unit_time(edges, sample_rate)
        
        # 解码
        morse_text = self._edges_to_morse(edges, unit_time, sample_rate)
        
        # 解码 Morse 码文本
        text, stats = self.decode_text(morse_text)
        
        # 添加信号分析统计
        stats.update({
            'sample_count': len(signal),
            'sample_rate': sample_rate,
            'unit_time_ms': unit_time * 1000,
            'threshold': threshold,
            'signal_duration_s': len(signal) / sample_rate
        })
        
        return text, stats
    
    def _normalize_signal(self, signal: List[float]) -> List[float]:
        """标准化信号到 0-1 范围"""
        if not signal:
            return []
        
        min_val = min(signal)
        max_val = max(signal)
        
        if max_val == min_val:
            return [0.5] * len(signal)
        
        return [(s - min_val) / (max_val - min_val) for s in signal]
    
    def _auto_threshold(self, signal: List[float]) -> float:
        """自动计算信号阈值（使用 Otsu 方法）"""
        if not signal:
            return 0.5
        
        # 创建直方图
        hist = Counter(int(s * 255) for s in signal)
        total = len(signal)
        
        best_threshold = 128
        best_variance = 0
        
        for t in range(1, 256):
            # 类内方差
            w0 = sum(hist.get(i, 0) for i in range(t)) / total
            w1 = sum(hist.get(i, 0) for i in range(t, 256)) / total
            
            if w0 == 0 or w1 == 0:
                continue
            
            m0 = sum(i * hist.get(i, 0) for i in range(t)) / (w0 * total)
            m1 = sum(i * hist.get(i, 0) for i in range(t, 256)) / (w1 * total)
            
            variance = w0 * w1 * (m0 - m1) ** 2
            
            if variance > best_variance:
                best_variance = variance
                best_threshold = t
        
        return best_threshold / 255.0
    
    def _detect_edges(self, binary: List[int]) -> List[Tuple[int, int]]:
        """
        检测信号边缘
        
        Returns:
            [(开始位置, 结束位置), ...] 高电平段列表
        """
        edges = []
        in_high = False
        start = 0
        
        for i, val in enumerate(binary):
            if val == 1 and not in_high:
                in_high = True
                start = i
            elif val == 0 and in_high:
                in_high = False
                edges.append((start, i))
        
        # 处理最后一个高电平
        if in_high:
            edges.append((start, len(binary)))
        
        return edges
    
    def _estimate_unit_time(self, edges: List[Tuple[int, int]], 
                            sample_rate: float) -> float:
        """估算单位时间（点的持续时间）"""
        if not edges:
            return 0.1  # 默认 100ms
        
        # 收集所有高电平和低电平持续时间
        durations = []
        for start, end in edges:
            durations.append((end - start) / sample_rate)
        
        # 添加低电平持续时间
        for i in range(len(edges) - 1):
            gap = (edges[i+1][0] - edges[i][1]) / sample_rate
            durations.append(gap)
        
        if not durations:
            return 0.1
        
        # 使用聚类找到短、中、长三类持续时间
        # 点 = 短，划 = 长（3倍点），字符间隙 = 点，单词间隙 = 7倍点
        sorted_durations = sorted(durations)
        
        # 使用最小的非零持续时间作为点的估计
        min_durations = sorted_durations[:max(1, len(sorted_durations) // 3)]
        unit_time = sum(min_durations) / len(min_durations) if min_durations else 0.1
        
        return max(unit_time, 0.01)  # 最小 10ms
    
    def _edges_to_morse(self, edges: List[Tuple[int, int]], 
                        unit_time: float,
                        sample_rate: float) -> str:
        """将边缘转换为 Morse 码文本"""
        if not edges:
            return ''
        
        morse_chars = []
        
        for i, (start, end) in enumerate(edges):
            duration = (end - start) / sample_rate
            
            # 判断点或划
            if duration < unit_time * 2:
                morse_chars.append('.')
            else:
                morse_chars.append('-')
            
            # 检查间隙
            if i < len(edges) - 1:
                gap = (edges[i+1][0] - end) / sample_rate
                
                if gap > unit_time * 5:
                    # 单词分隔
                    morse_chars.append('   ')
                elif gap > unit_time * 2:
                    # 字符分隔
                    morse_chars.append(' ')
        
        return ''.join(morse_chars)
    
    def analyze_signal_quality(self, signal: List[float],
                                sample_rate: float = 1000.0) -> Dict:
        """
        分析信号质量
        
        Returns:
            信号质量分析结果
        """
        if not signal:
            return {'quality': 0, 'error': 'Empty signal'}
        
        signal = self._normalize_signal(signal)
        threshold = self._auto_threshold(signal)
        
        # 计算信噪比估计
        high_samples = [s for s in signal if s >= threshold]
        low_samples = [s for s in signal if s < threshold]
        
        if not high_samples or not low_samples:
            return {
                'quality': 0.5,
                'threshold': threshold,
                'high_mean': sum(high_samples) / len(high_samples) if high_samples else 0,
                'low_mean': sum(low_samples) / len(low_samples) if low_samples else 0,
                'signal_ratio': len(high_samples) / len(signal)
            }
        
        high_mean = sum(high_samples) / len(high_samples)
        low_mean = sum(low_samples) / len(low_samples)
        
        # 简单的信噪比估计
        snr = (high_mean - low_mean) / max(0.01, low_mean)
        
        # 转换为质量分数（0-1）
        quality = min(1.0, snr / 3.0)
        
        # 检测稳定性
        high_std = math.sqrt(sum((s - high_mean)**2 for s in high_samples) / len(high_samples))
        low_std = math.sqrt(sum((s - low_mean)**2 for s in low_samples) / len(low_samples))
        stability = 1.0 - min(1.0, (high_std + low_std) / 2)
        
        return {
            'quality': quality * stability,
            'snr_estimate': snr,
            'threshold': threshold,
            'high_mean': high_mean,
            'high_std': high_std,
            'low_mean': low_mean,
            'low_std': low_std,
            'signal_ratio': len(high_samples) / len(signal),
            'stability': stability,
            'sample_count': len(signal),
            'duration_s': len(signal) / sample_rate
        }


def decode_morse(morse: str, char_sep: str = ' ', word_sep: str = ' / ') -> str:
    """
    快速解码 Morse 码文本的便捷函数
    
    Args:
        morse: Morse 码字符串
        char_sep: 字符分隔符
        word_sep: 单词分隔符
    
    Returns:
        解码后的文本
    """
    decoder = MorseDecoder()
    text, _ = decoder.decode_text(morse, char_sep, word_sep)
    return text


def decode_signal(signal: List[float], 
                  sample_rate: float = 1000.0,
                  threshold: Optional[float] = None) -> str:
    """
    快速解码信号的便捷函数
    
    Args:
        signal: 信号强度列表
        sample_rate: 采样率
        threshold: 信号阈值
    
    Returns:
        解码后的文本
    """
    decoder = MorseDecoder()
    text, _ = decoder.decode_signal(signal, sample_rate, threshold)
    return text


def analyze_signal(signal: List[float], sample_rate: float = 1000.0) -> Dict:
    """
    分析信号质量的便捷函数
    
    Args:
        signal: 信号强度列表
        sample_rate: 采样率
    
    Returns:
        信号质量分析结果
    """
    decoder = MorseDecoder()
    return decoder.analyze_signal_quality(signal, sample_rate)


# 常用 Morse 码短语
COMMON_PHRASES = {
    '... --- ...': 'SOS',
    '.- .-.. .-..': 'ALL',
    '-.-- . ...': 'YES',
    '-. ---': 'NO',
    '.-- .- .. -': 'WAIT',
    '--. ---': 'GO',
    '.... . .-.. .--.': 'HELP',
    '.-- .-': 'WE',
    '.. ...': 'IS',
    '- .... . .-. .': 'THERE',
    '.- -. -.-- --- -. .': 'ANYONE',
}


def quick_decode(morse: str) -> str:
    """
    快速解码，优先使用常用短语
    
    Args:
        morse: Morse 码字符串
    
    Returns:
        解码后的文本
    """
    normalized = ' '.join(morse.split())  # 标准化空白
    
    if normalized in COMMON_PHRASES:
        return COMMON_PHRASES[normalized]
    
    return decode_morse(morse)


# 导出
__all__ = [
    'MorseDecoder',
    'MORSE_TO_CHAR',
    'decode_morse',
    'decode_signal',
    'analyze_signal',
    'quick_decode',
    'COMMON_PHRASES',
]