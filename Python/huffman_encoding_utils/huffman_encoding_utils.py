"""
Huffman Encoding Utils - 零依赖哈夫曼编码工具

功能:
- 基于字符频率构建哈夫曼树
- 文本编码与解码
- 压缩率计算与分析
- 二进制序列转换
- 树的可视化表示

作者: AllToolkit 自动生成
日期: 2026-04-28
"""

from collections import Counter
from typing import Dict, Optional, Tuple, List, Any
from dataclasses import dataclass
import heapq


@dataclass
class HuffmanNode:
    """哈夫曼树节点"""
    char: Optional[str]  # 字符，None表示内部节点
    freq: int  # 频率
    left: Optional['HuffmanNode'] = None
    right: Optional['HuffmanNode'] = None
    
    def __lt__(self, other: 'HuffmanNode') -> bool:
        """用于堆比较，频率低的优先"""
        return self.freq < other.freq
    
    def is_leaf(self) -> bool:
        """判断是否为叶子节点"""
        return self.left is None and self.right is None


class HuffmanEncoder:
    """哈夫曼编码器"""
    
    def __init__(self):
        self.root: Optional[HuffmanNode] = None
        self.codes: Dict[str, str] = {}
        self.reverse_codes: Dict[str, str] = {}
    
    def build_tree(self, text: str) -> HuffmanNode:
        """
        根据文本构建哈夫曼树
        
        Args:
            text: 输入文本
        
        Returns:
            哈夫曼树的根节点
        """
        if not text:
            raise ValueError("输入文本不能为空")
        
        # 统计字符频率
        freq = Counter(text)
        
        # 特殊情况：只有一种字符
        if len(freq) == 1:
            char = list(freq.keys())[0]
            self.root = HuffmanNode(char=None, freq=freq[char])
            self.root.left = HuffmanNode(char=char, freq=freq[char])
            self.codes = {char: '0'}
            self.reverse_codes = {'0': char}
            return self.root
        
        # 构建最小堆
        heap = [HuffmanNode(char=ch, freq=f) for ch, f in freq.items()]
        heapq.heapify(heap)
        
        # 构建哈夫曼树
        while len(heap) > 1:
            left = heapq.heappop(heap)
            right = heapq.heappop(heap)
            
            merged = HuffmanNode(
                char=None,
                freq=left.freq + right.freq,
                left=left,
                right=right
            )
            heapq.heappush(heap, merged)
        
        self.root = heap[0]
        
        # 生成编码表
        self.codes = {}
        self._generate_codes(self.root, "")
        self.reverse_codes = {v: k for k, v in self.codes.items()}
        
        return self.root
    
    def _generate_codes(self, node: Optional[HuffmanNode], code: str) -> None:
        """
        递归生成哈夫曼编码
        
        Args:
            node: 当前节点
            code: 当前编码前缀
        """
        if node is None:
            return
        
        if node.is_leaf():
            if node.char is not None:
                self.codes[node.char] = code if code else '0'
            return
        
        self._generate_codes(node.left, code + '0')
        self._generate_codes(node.right, code + '1')
    
    def encode(self, text: str) -> str:
        """
        编码文本为二进制字符串
        
        Args:
            text: 要编码的文本
        
        Returns:
            二进制编码字符串
        """
        if not self.codes:
            self.build_tree(text)
        
        return ''.join(self.codes.get(ch, '') for ch in text)
    
    def decode(self, encoded: str) -> str:
        """
        解码二进制字符串为原始文本
        
        Args:
            encoded: 二进制编码字符串
        
        Returns:
            解码后的原始文本
        """
        if self.root is None:
            raise ValueError("请先构建哈夫曼树")
        
        if not encoded:
            return ""
        
        result = []
        current = self.root
        
        for bit in encoded:
            if bit == '0':
                current = current.left
            else:
                current = current.right
            
            if current is None:
                raise ValueError("无效的编码序列")
            
            if current.is_leaf() and current.char is not None:
                result.append(current.char)
                current = self.root
        
        return ''.join(result)
    
    def get_frequency_table(self, text: str) -> Dict[str, Tuple[int, float]]:
        """
        获取字符频率表
        
        Args:
            text: 输入文本
        
        Returns:
            字符到(频率, 百分比)的映射
        """
        if not text:
            return {}
        
        freq = Counter(text)
        total = len(text)
        
        return {
            ch: (count, count / total * 100)
            for ch, count in freq.most_common()
        }
    
    def get_code_table(self) -> Dict[str, str]:
        """获取编码表"""
        return self.codes.copy()
    
    def calculate_compression_stats(self, text: str) -> Dict[str, Any]:
        """
        计算压缩统计信息
        
        Args:
            text: 原始文本
        
        Returns:
            包含压缩统计的字典
        """
        if not text:
            return {}
        
        if not self.codes:
            self.build_tree(text)
        
        encoded = self.encode(text)
        
        original_bits = len(text) * 8  # 假设原始为ASCII
        encoded_bits = len(encoded)
        
        # 计算平均编码长度
        freq = Counter(text)
        total = len(text)
        avg_length = sum(
            freq[ch] / total * len(self.codes[ch])
            for ch in freq
        )
        
        return {
            'original_size_bits': original_bits,
            'encoded_size_bits': encoded_bits,
            'compression_ratio': encoded_bits / original_bits if original_bits > 0 else 0,
            'space_saved_percent': (1 - encoded_bits / original_bits) * 100 if original_bits > 0 else 0,
            'average_code_length': avg_length,
            'unique_characters': len(freq),
            'code_table_size': len(self.codes)
        }
    
    def visualize_tree(self) -> str:
        """
        生成树的可视化字符串表示
        
        Returns:
            树的可视化字符串
        """
        if self.root is None:
            return "树未构建"
        
        lines = []
        self._visualize_node(self.root, "", True, lines)
        return '\n'.join(lines)
    
    def _visualize_node(
        self, 
        node: Optional[HuffmanNode], 
        prefix: str, 
        is_last: bool,
        lines: List[str]
    ) -> None:
        """递归生成节点可视化"""
        if node is None:
            return
        
        connector = "└── " if is_last else "├── "
        
        if node.is_leaf():
            char_repr = repr(node.char) if node.char else 'None'
            lines.append(f"{prefix}{connector}{char_repr} ({node.freq})")
        else:
            lines.append(f"{prefix}{connector}* ({node.freq})")
            
            extension = "    " if is_last else "│   "
            new_prefix = prefix + extension
            
            children = [n for n in [node.left, node.right] if n is not None]
            for i, child in enumerate(children):
                self._visualize_node(child, new_prefix, i == len(children) - 1, lines)
    
    def to_dict(self) -> Dict[str, Any]:
        """
        将编码器状态序列化为字典
        
        Returns:
            包含编码表和树结构的字典
        """
        return {
            'codes': self.codes,
            'reverse_codes': self.reverse_codes,
            'tree': self._node_to_dict(self.root) if self.root else None
        }
    
    def _node_to_dict(self, node: Optional[HuffmanNode]) -> Optional[Dict]:
        """将节点转换为字典"""
        if node is None:
            return None
        
        return {
            'char': node.char,
            'freq': node.freq,
            'left': self._node_to_dict(node.left),
            'right': self._node_to_dict(node.right)
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'HuffmanEncoder':
        """
        从字典恢复编码器状态
        
        Args:
            data: 序列化的编码器数据
        
        Returns:
            HuffmanEncoder实例
        """
        encoder = cls()
        encoder.codes = data.get('codes', {})
        encoder.reverse_codes = data.get('reverse_codes', {})
        encoder.root = cls._dict_to_node(data.get('tree'))
        return encoder
    
    @staticmethod
    def _dict_to_node(data: Optional[Dict]) -> Optional[HuffmanNode]:
        """从字典恢复节点"""
        if data is None:
            return None
        
        return HuffmanNode(
            char=data.get('char'),
            freq=data.get('freq', 0),
            left=HuffmanEncoder._dict_to_node(data.get('left')),
            right=HuffmanEncoder._dict_to_node(data.get('right'))
        )


def huffman_encode(text: str) -> Tuple[str, HuffmanEncoder]:
    """
    快捷编码函数
    
    Args:
        text: 要编码的文本
    
    Returns:
        (编码后的二进制字符串, 编码器实例)
    """
    encoder = HuffmanEncoder()
    encoded = encoder.encode(text)
    return encoded, encoder


def huffman_decode(encoded: str, encoder: HuffmanEncoder) -> str:
    """
    快捷解码函数
    
    Args:
        encoded: 二进制编码字符串
        encoder: 哈夫曼编码器
    
    Returns:
        解码后的文本
    """
    return encoder.decode(encoded)


def analyze_text(text: str) -> Dict[str, Any]:
    """
    分析文本的压缩潜力
    
    Args:
        text: 要分析的文本
    
    Returns:
        分析结果字典
    """
    encoder = HuffmanEncoder()
    encoder.build_tree(text)
    
    return {
        'text_length': len(text),
        'frequency_table': encoder.get_frequency_table(text),
        'code_table': encoder.get_code_table(),
        'compression_stats': encoder.calculate_compression_stats(text),
        'tree_visualization': encoder.visualize_tree()
    }


def compare_with_fixed_encoding(text: str) -> Dict[str, Any]:
    """
    比较哈夫曼编码与固定长度编码
    
    Args:
        text: 要比较的文本
    
    Returns:
        比较结果
    """
    encoder = HuffmanEncoder()
    encoder.build_tree(text)
    
    stats = encoder.calculate_compression_stats(text)
    
    # 固定长度编码需要 ceil(log2(unique_chars)) 位
    unique_chars = stats['unique_characters']
    import math
    fixed_bits_per_char = math.ceil(math.log2(unique_chars)) if unique_chars > 1 else 1
    
    fixed_total_bits = len(text) * fixed_bits_per_char
    
    return {
        'huffman_bits': stats['encoded_size_bits'],
        'fixed_bits': fixed_total_bits,
        'huffman_avg_length': stats['average_code_length'],
        'fixed_bits_per_char': fixed_bits_per_char,
        'huffman_savings_vs_fixed': (
            (fixed_total_bits - stats['encoded_size_bits']) / fixed_total_bits * 100
            if fixed_total_bits > 0 else 0
        )
    }


# 示例使用
if __name__ == "__main__":
    # 示例文本
    sample_text = "this is an example for huffman encoding"
    
    print("=" * 60)
    print("哈夫曼编码工具示例")
    print("=" * 60)
    
    # 创建编码器
    encoder = HuffmanEncoder()
    encoder.build_tree(sample_text)
    
    # 显示频率表
    print("\n字符频率表:")
    freq_table = encoder.get_frequency_table(sample_text)
    for ch, (count, percent) in list(freq_table.items())[:10]:
        print(f"  {repr(ch)}: {count}次 ({percent:.1f}%)")
    
    # 显示编码表
    print("\n编码表 (前10个):")
    codes = encoder.get_code_table()
    for ch, code in list(codes.items())[:10]:
        print(f"  {repr(ch)}: {code}")
    
    # 编码
    encoded = encoder.encode(sample_text)
    print(f"\n原始文本: {sample_text}")
    print(f"编码结果: {encoded[:50]}...")
    
    # 解码
    decoded = encoder.decode(encoded)
    print(f"解码结果: {decoded}")
    print(f"编码正确: {decoded == sample_text}")
    
    # 压缩统计
    stats = encoder.calculate_compression_stats(sample_text)
    print(f"\n压缩统计:")
    print(f"  原始大小: {stats['original_size_bits']} bits")
    print(f"  编码大小: {stats['encoded_size_bits']} bits")
    print(f"  压缩率: {stats['compression_ratio']:.3f}")
    print(f"  节省空间: {stats['space_saved_percent']:.1f}%")
    print(f"  平均编码长度: {stats['average_code_length']:.2f} bits/字符")
    
    # 可视化树
    print("\n哈夫曼树结构:")
    print(encoder.visualize_tree())