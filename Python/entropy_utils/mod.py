#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Python Entropy Utilities
熵计算工具模块 - 用于信息熵、数据熵、密码学熵等计算

@module: entropy_utils
@author: AllToolkit Contributors
@license: MIT
@version: 1.0.0

功能列表:
- Shannon熵: 计算数据序列的香农熵
- 密码熵: 计算密码的信息熵和安全强度
- 数据压缩熵: 分析数据的可压缩性
- 条件熵: 计算条件熵和互信息
- 相对熵: 计算KL散度
- 交叉熵: 用于机器学习损失函数
- 文件熵: 计算文件的熵值
- 字符串熵: 分析字符串的随机性

使用示例:
    from entropy_utils.mod import EntropyUtils, PasswordEntropy
    
    # 计算字符串的香农熵
    entropy = EntropyUtils.shannon_entropy("hello world")
    print(f"Shannon entropy: {entropy:.4f} bits/char")
    
    # 分析密码强度
    analyzer = PasswordEntropy()
    result = analyzer.analyze("MyP@ssw0rd123!")
    print(f"Password entropy: {result['entropy']:.2f} bits")
"""

import math
from collections import Counter
from typing import Dict, List, Tuple, Optional, Union, Any
from dataclasses import dataclass


class EntropyUtils:
    """熵计算工具集"""
    
    @staticmethod
    def shannon_entropy(data: Union[str, bytes, List[Any]]) -> float:
        """
        计算香农熵
        
        香农熵衡量数据的不确定性或信息量。
        H(X) = -Σ p(x) * log2(p(x))
        
        Args:
            data: 输入数据（字符串、字节或列表）
            
        Returns:
            香农熵值（bits/符号）
            
        Examples:
            >>> EntropyUtils.shannon_entropy("aaa")
            0.0
            >>> EntropyUtils.shannon_entropy("abc")
            1.584962500721156
        """
        if not data:
            return 0.0
        
        # 计算频率分布
        counter = Counter(data)
        total = len(data)
        
        # 计算熵
        entropy = 0.0
        for count in counter.values():
            if count > 0:
                probability = count / total
                entropy -= probability * math.log2(probability)
        
        return entropy
    
    @staticmethod
    def shannon_entropy_normalized(data: Union[str, bytes, List[Any]]) -> float:
        """
        计算归一化香农熵
        
        将熵值归一化到 [0, 1] 范围，便于比较不同大小的数据。
        
        Args:
            data: 输入数据
            
        Returns:
            归一化熵值 [0, 1]
        """
        if not data:
            return 0.0
        
        # 原始熵
        entropy = EntropyUtils.shannon_entropy(data)
        
        # 最大可能熵
        unique_count = len(set(data))
        if unique_count <= 1:
            return 0.0
        
        max_entropy = math.log2(unique_count)
        
        return entropy / max_entropy if max_entropy > 0 else 0.0
    
    @staticmethod
    def renyi_entropy(data: Union[str, bytes, List[Any]], alpha: float = 2.0) -> float:
        """
        计算Rényi熵
        
        Rényi熵是香农熵的推广，由参数alpha控制。
        alpha=1时等于香农熵，alpha=0时等于log(字符集大小)，alpha=2时为碰撞熵。
        
        H_α(X) = 1/(1-α) * log2(Σ p(x)^α)
        
        Args:
            data: 输入数据
            alpha: Rényi熵参数，默认为2（碰撞熵）
            
        Returns:
            Rényi熵值
        """
        if not data:
            return 0.0
        
        if alpha == 1.0:
            # alpha=1时极限等于香农熵
            return EntropyUtils.shannon_entropy(data)
        
        counter = Counter(data)
        total = len(data)
        
        # 计算 Σ p(x)^α
        sum_prob_alpha = 0.0
        for count in counter.values():
            probability = count / total
            sum_prob_alpha += probability ** alpha
        
        # H_α = 1/(1-α) * log2(sum)
        if sum_prob_alpha <= 0:
            return 0.0
        
        return math.log2(sum_prob_alpha) / (1 - alpha)
    
    @staticmethod
    def min_entropy(data: Union[str, bytes, List[Any]]) -> float:
        """
        计算最小熵
        
        最小熵是最保守的熵度量，等于 -log2(max p(x))
        常用于密码学和随机数生成器评估。
        
        Args:
            data: 输入数据
            
        Returns:
            最小熵值
        """
        if not data:
            return 0.0
        
        counter = Counter(data)
        total = len(data)
        
        # 找最大概率
        max_probability = max(count / total for count in counter.values())
        
        if max_probability <= 0:
            return 0.0
        
        return -math.log2(max_probability)
    
    @staticmethod
    def gini_impurity(data: Union[str, bytes, List[Any]]) -> float:
        """
        计算基尼不纯度
        
        基尼不纯度衡量数据集的不确定性，常用于决策树。
        Gini = 1 - Σ p(x)^2
        
        Args:
            data: 输入数据
            
        Returns:
            基尼不纯度 [0, 1]
        """
        if not data:
            return 0.0
        
        counter = Counter(data)
        total = len(data)
        
        # 计算 Σ p(x)^2
        sum_prob_squared = sum((count / total) ** 2 for count in counter.values())
        
        return 1 - sum_prob_squared
    
    @staticmethod
    def kl_divergence(p: Dict[Any, float], q: Dict[Any, float]) -> float:
        """
        计算KL散度（相对熵）
        
        D_KL(P||Q) = Σ p(x) * log2(p(x)/q(x))
        
        衡量分布P相对于分布Q的差异。
        
        Args:
            p: 第一个概率分布
            q: 第二个概率分布
            
        Returns:
            KL散度值（非负）
            
        Raises:
            ValueError: 如果分布无效
        """
        # 获取所有可能的符号
        all_keys = set(p.keys()) | set(q.keys())
        
        divergence = 0.0
        for key in all_keys:
            p_val = p.get(key, 0.0)
            q_val = q.get(key, 0.0)
            
            if p_val > 0:
                if q_val <= 0:
                    raise ValueError(f"分布Q中符号{key}的概率为0，但分布P中该符号概率为{p_val}")
                divergence += p_val * math.log2(p_val / q_val)
        
        return divergence
    
    @staticmethod
    def cross_entropy(p: Dict[Any, float], q: Dict[Any, float]) -> float:
        """
        计算交叉熵
        
        H(P, Q) = -Σ p(x) * log2(q(x))
        
        用于机器学习中衡量预测分布与真实分布的差异。
        
        Args:
            p: 真实概率分布
            q: 预测概率分布
            
        Returns:
            交叉熵值
        """
        all_keys = set(p.keys()) | set(q.keys())
        
        ce = 0.0
        for key in all_keys:
            p_val = p.get(key, 0.0)
            q_val = q.get(key, 1e-10)  # 避免log(0)
            
            if p_val > 0:
                ce -= p_val * math.log2(q_val)
        
        return ce
    
    @staticmethod
    def mutual_information(x: List[Any], y: List[Any]) -> float:
        """
        计算互信息
        
        I(X;Y) = H(X) + H(Y) - H(X,Y)
        
        衡量两个变量之间的相互依赖程度。
        
        Args:
            x: 第一个变量
            y: 第二个变量
            
        Returns:
            互信息值
        """
        if len(x) != len(y):
            raise ValueError("两个变量长度必须相同")
        
        if not x:
            return 0.0
        
        # 计算边缘熵
        h_x = EntropyUtils.shannon_entropy(x)
        h_y = EntropyUtils.shannon_entropy(y)
        
        # 计算联合熵
        joint = list(zip(x, y))
        h_xy = EntropyUtils.shannon_entropy(joint)
        
        return h_x + h_y - h_xy
    
    @staticmethod
    def joint_entropy(x: List[Any], y: List[Any]) -> float:
        """
        计算联合熵
        
        H(X,Y) = -Σ p(x,y) * log2(p(x,y))
        
        Args:
            x: 第一个变量
            y: 第二个变量
            
        Returns:
            联合熵值
        """
        if len(x) != len(y):
            raise ValueError("两个变量长度必须相同")
        
        if not x:
            return 0.0
        
        joint = list(zip(x, y))
        return EntropyUtils.shannon_entropy(joint)
    
    @staticmethod
    def conditional_entropy(x: List[Any], y: List[Any]) -> float:
        """
        计算条件熵
        
        H(X|Y) = H(X,Y) - H(Y)
        
        衡量已知Y的情况下X的不确定性。
        
        Args:
            x: 目标变量
            y: 条件变量
            
        Returns:
            条件熵值
        """
        if len(x) != len(y):
            raise ValueError("两个变量长度必须相同")
        
        if not x:
            return 0.0
        
        h_xy = EntropyUtils.joint_entropy(x, y)
        h_y = EntropyUtils.shannon_entropy(y)
        
        return h_xy - h_y
    
    @staticmethod
    def file_entropy(filepath: str, chunk_size: int = 8192) -> float:
        """
        计算文件的字节熵
        
        Args:
            filepath: 文件路径
            chunk_size: 读取块大小
            
        Returns:
            文件的字节熵值
        """
        byte_counter: Counter = Counter()
        total_bytes = 0
        
        with open(filepath, 'rb') as f:
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                byte_counter.update(chunk)
                total_bytes += len(chunk)
        
        if total_bytes == 0:
            return 0.0
        
        # 计算熵
        entropy = 0.0
        for count in byte_counter.values():
            if count > 0:
                probability = count / total_bytes
                entropy -= probability * math.log2(probability)
        
        return entropy
    
    @staticmethod
    def compression_potential(data: Union[str, bytes]) -> float:
        """
        评估数据的压缩潜力
        
        基于熵值评估数据的可压缩性。
        返回值越高，压缩效果越好。
        
        Args:
            data: 输入数据
            
        Returns:
            压缩潜力 [0, 1]，1表示最容易压缩
        """
        if not data:
            return 0.0
        
        if isinstance(data, str):
            # 字符串：最大熵为 log2(字符集大小)
            charset_size = len(set(data))
            # 对于单一字符，压缩潜力最高（1.0）
            if charset_size <= 1:
                return 1.0
            max_entropy = math.log2(charset_size)
        else:
            # 字节：最大熵为 8
            charset_size = len(set(data))
            if charset_size <= 1:
                return 1.0
            max_entropy = 8.0
        
        actual_entropy = EntropyUtils.shannon_entropy(data)
        
        if max_entropy <= 0:
            return 0.0
        
        # 归一化：熵越低，压缩潜力越高
        return 1 - (actual_entropy / max_entropy) if max_entropy > 0 else 0.0
    
    @staticmethod
    def randomness_score(data: Union[str, bytes, List[Any]]) -> float:
        """
        计算随机性得分
        
        基于多个指标评估数据的随机性程度。
        
        Args:
            data: 输入数据
            
        Returns:
            随机性得分 [0, 1]，1表示最随机
        """
        if not data:
            return 0.0
        
        # 1. 归一化香农熵
        entropy_score = EntropyUtils.shannon_entropy_normalized(data)
        
        # 2. 符号分布均匀度
        counter = Counter(data)
        unique = len(counter)
        total = len(data)
        expected_freq = total / unique if unique > 0 else 0
        
        uniformity = 0.0
        if expected_freq > 0:
            variance = sum((count - expected_freq) ** 2 for count in counter.values()) / unique
            uniformity = 1 - min(variance / (expected_freq ** 2), 1) if expected_freq > 0 else 0
        
        # 3. 序列独立性（简单的游程检验）
        if len(data) > 1:
            runs = 1
            for i in range(1, len(data)):
                if data[i] != data[i-1]:
                    runs += 1
            expected_runs = 1 + (total - 1) * (unique - 1) / unique if unique > 1 else 1
            runs_score = min(runs / expected_runs, 1) if expected_runs > 0 else 0
        else:
            runs_score = 0.5
        
        # 综合得分
        return (entropy_score * 0.5 + uniformity * 0.3 + runs_score * 0.2)
    
    @staticmethod
    def analyze_distribution(data: Union[str, bytes, List[Any]]) -> Dict[str, Any]:
        """
        分析数据的分布特征
        
        Args:
            data: 输入数据
            
        Returns:
            包含各种熵度量的字典
        """
        if not data:
            return {
                'shannon_entropy': 0,
                'min_entropy': 0,
                'max_entropy': 0,
                'normalized_entropy': 0,
                'gini_impurity': 0,
                'unique_count': 0,
                'total_count': 0,
                'compression_potential': 0,
                'randomness_score': 0
            }
        
        shannon = EntropyUtils.shannon_entropy(data)
        min_ent = EntropyUtils.min_entropy(data)
        gini = EntropyUtils.gini_impurity(data)
        
        unique_count = len(set(data))
        total_count = len(data)
        
        # 最大可能熵
        if isinstance(data, (str, bytes)):
            max_ent = math.log2(unique_count) if unique_count > 1 else 0
        else:
            max_ent = math.log2(unique_count) if unique_count > 1 else 0
        
        return {
            'shannon_entropy': round(shannon, 6),
            'min_entropy': round(min_ent, 6),
            'max_entropy': round(max_ent, 6),
            'normalized_entropy': round(shannon / max_ent, 6) if max_ent > 0 else 0,
            'gini_impurity': round(gini, 6),
            'unique_count': unique_count,
            'total_count': total_count,
            'compression_potential': round(EntropyUtils.compression_potential(data), 6),
            'randomness_score': round(EntropyUtils.randomness_score(data), 6),
            'top_symbols': Counter(data).most_common(5)
        }


@dataclass
class PasswordAnalysis:
    """密码分析结果"""
    password: str
    length: int
    entropy: float
    entropy_per_char: float
    charset_size: int
    has_lowercase: bool
    has_uppercase: bool
    has_digits: bool
    has_special: bool
    has_unicode: bool
    is_common: bool
    strength: str
    crack_time_estimate: str
    suggestions: List[str]


class PasswordEntropy:
    """密码熵分析器"""
    
    # 常见密码列表（示例）
    COMMON_PASSWORDS = {
        'password', '123456', '12345678', 'qwerty', 'abc123',
        'monkey', '1234567', 'letmein', 'trustno1', 'dragon',
        'baseball', 'iloveyou', 'master', 'sunshine', 'ashley',
        'bailey', 'passw0rd', 'shadow', '123123', '654321',
        'superman', 'qazwsx', 'michael', 'football', 'password1',
        'password123', 'admin', 'welcome', 'login', 'starwars'
    }
    
    # 字符集定义
    LOWERCASE = set('abcdefghijklmnopqrstuvwxyz')
    UPPERCASE = set('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    DIGITS = set('0123456789')
    SPECIAL = set('!@#$%^&*()_+-=[]{}|;:\'",.<>?/~`')
    
    # 键盘模式
    KEYBOARD_PATTERNS = [
        'qwerty', 'asdfgh', 'zxcvbn', 'qwertyuiop', 'asdfghjkl',
        'zxcvbnm', '1234567890', '!@#$%^&*()'
    ]
    
    def __init__(self, custom_common_passwords: Optional[set] = None):
        """
        初始化密码熵分析器
        
        Args:
            custom_common_passwords: 自定义常见密码集合
        """
        if custom_common_passwords:
            self.common_passwords = self.COMMON_PASSWORDS | custom_common_passwords
        else:
            self.common_passwords = self.COMMON_PASSWORDS
    
    def calculate_charset_size(self, password: str) -> int:
        """
        计算密码使用的字符集大小
        
        Args:
            password: 密码字符串
            
        Returns:
            字符集大小
        """
        chars = set(password)
        charset_size = 0
        
        if chars & self.LOWERCASE:
            charset_size += 26
        if chars & self.UPPERCASE:
            charset_size += 26
        if chars & self.DIGITS:
            charset_size += 10
        if chars & self.SPECIAL:
            charset_size += 32
        
        # 检查其他Unicode字符
        remaining = chars - self.LOWERCASE - self.UPPERCASE - self.DIGITS - self.SPECIAL
        if remaining:
            charset_size += len(remaining)
        
        return max(charset_size, 1)
    
    def calculate_entropy(self, password: str) -> float:
        """
        计算密码熵
        
        熵 = length * log2(charset_size)
        
        Args:
            password: 密码字符串
            
        Returns:
            熵值（bits）
        """
        if not password:
            return 0.0
        
        charset_size = self.calculate_charset_size(password)
        length = len(password)
        
        return length * math.log2(charset_size)
    
    def estimate_crack_time(self, entropy: float, guesses_per_second: float = 1e10) -> str:
        """
        估算破解时间
        
        Args:
            entropy: 密码熵值
            guesses_per_second: 每秒猜测次数（默认100亿次）
            
        Returns:
            人类可读的时间估计
        """
        if entropy <= 0:
            return "瞬间"
        
        # 平均需要尝试 2^(entropy-1) 次
        total_guesses = 2 ** entropy / 2
        seconds = total_guesses / guesses_per_second
        
        if seconds < 1:
            return "瞬间"
        elif seconds < 60:
            return f"{seconds:.1f} 秒"
        elif seconds < 3600:
            return f"{seconds/60:.1f} 分钟"
        elif seconds < 86400:
            return f"{seconds/3600:.1f} 小时"
        elif seconds < 31536000:
            return f"{seconds/86400:.1f} 天"
        elif seconds < 31536000 * 100:
            return f"{seconds/31536000:.1f} 年"
        elif seconds < 31536000 * 1000000:
            return f"{seconds/31536000:.0f} 年"
        else:
            return "宇宙年龄级别"
    
    def check_patterns(self, password: str) -> List[str]:
        """
        检查密码中的弱模式
        
        Args:
            password: 密码字符串
            
        Returns:
            发现的模式列表
        """
        patterns = []
        lower = password.lower()
        
        # 检查键盘模式
        for pattern in self.KEYBOARD_PATTERNS:
            if pattern in lower:
                patterns.append(f"键盘模式: {pattern}")
        
        # 检查连续数字
        for i in range(len(password) - 2):
            if password[i:i+3].isdigit():
                if ord(password[i+1]) - ord(password[i]) == 1 and \
                   ord(password[i+2]) - ord(password[i+1]) == 1:
                    patterns.append("连续数字序列")
                    break
        
        # 检查重复字符
        for i in range(len(password) - 2):
            if password[i] == password[i+1] == password[i+2]:
                patterns.append("重复字符")
                break
        
        return patterns
    
    def generate_suggestions(self, password: str, analysis: dict) -> List[str]:
        """
        生成密码改进建议
        
        Args:
            password: 密码字符串
            analysis: 分析结果
            
        Returns:
            建议列表
        """
        suggestions = []
        
        if analysis['length'] < 8:
            suggestions.append("增加密码长度（至少8个字符）")
        
        if not analysis['has_lowercase']:
            suggestions.append("添加小写字母")
        
        if not analysis['has_uppercase']:
            suggestions.append("添加大写字母")
        
        if not analysis['has_digits']:
            suggestions.append("添加数字")
        
        if not analysis['has_special']:
            suggestions.append("添加特殊字符")
        
        if analysis['is_common']:
            suggestions.append("避免使用常见密码")
        
        patterns = self.check_patterns(password)
        if patterns:
            suggestions.append("避免使用可预测的模式")
        
        if analysis['entropy'] < 40:
            suggestions.append("熵值过低，考虑使用更复杂的密码")
        
        return suggestions
    
    def analyze(self, password: str) -> PasswordAnalysis:
        """
        全面分析密码强度
        
        Args:
            password: 密码字符串
            
        Returns:
            PasswordAnalysis 对象
        """
        chars = set(password)
        length = len(password)
        
        # 字符集检测
        has_lower = bool(chars & self.LOWERCASE)
        has_upper = bool(chars & self.UPPERCASE)
        has_digits = bool(chars & self.DIGITS)
        has_special = bool(chars & self.SPECIAL)
        has_unicode = bool(chars - self.LOWERCASE - self.UPPERCASE - 
                          self.DIGITS - self.SPECIAL)
        
        # 是否为常见密码
        is_common = password.lower() in self.common_passwords
        
        # 计算熵
        entropy = self.calculate_entropy(password)
        entropy_per_char = entropy / length if length > 0 else 0
        
        # 强度评级
        if entropy < 28:
            strength = "非常弱"
        elif entropy < 36:
            strength = "弱"
        elif entropy < 60:
            strength = "中等"
        elif entropy < 80:
            strength = "强"
        else:
            strength = "非常强"
        
        # 估算破解时间
        crack_time = self.estimate_crack_time(entropy)
        
        # 分析字典
        analysis_dict = {
            'length': length,
            'entropy': entropy,
            'has_lowercase': has_lower,
            'has_uppercase': has_upper,
            'has_digits': has_digits,
            'has_special': has_special,
            'is_common': is_common
        }
        
        # 生成建议
        suggestions = self.generate_suggestions(password, analysis_dict)
        
        return PasswordAnalysis(
            password='*' * length,  # 隐藏密码
            length=length,
            entropy=round(entropy, 2),
            entropy_per_char=round(entropy_per_char, 2),
            charset_size=self.calculate_charset_size(password),
            has_lowercase=has_lower,
            has_uppercase=has_upper,
            has_digits=has_digits,
            has_special=has_special,
            has_unicode=has_unicode,
            is_common=is_common,
            strength=strength,
            crack_time_estimate=crack_time,
            suggestions=suggestions
        )


class DataEntropyAnalyzer:
    """数据熵分析器"""
    
    def __init__(self, window_size: int = 256):
        """
        初始化分析器
        
        Args:
            window_size: 滑动窗口大小
        """
        self.window_size = window_size
    
    def analyze_sequence(self, data: Union[str, bytes, List[Any]]) -> Dict[str, Any]:
        """
        分析序列数据的熵特征
        
        Args:
            data: 输入数据
            
        Returns:
            分析结果字典
        """
        if not data:
            return {'error': '空数据'}
        
        # 基本统计
        counter = Counter(data)
        unique = len(counter)
        total = len(data)
        
        # 熵计算
        shannon = EntropyUtils.shannon_entropy(data)
        min_ent = EntropyUtils.min_entropy(data)
        renyi_2 = EntropyUtils.renyi_entropy(data, 2)
        gini = EntropyUtils.gini_impurity(data)
        
        # 最大可能熵
        max_entropy = math.log2(unique) if unique > 1 else 0
        
        return {
            'length': total,
            'unique_symbols': unique,
            'symbol_diversity': unique / min(total, 256),  # 相对于256的多样性
            'shannon_entropy': round(shannon, 4),
            'min_entropy': round(min_ent, 4),
            'renyi_entropy_alpha2': round(renyi_2, 4),
            'gini_impurity': round(gini, 4),
            'max_possible_entropy': round(max_entropy, 4),
            'entropy_efficiency': round(shannon / max_entropy * 100, 2) if max_entropy > 0 else 0,
            'compression_potential': round(EntropyUtils.compression_potential(data), 4),
            'randomness_score': round(EntropyUtils.randomness_score(data), 4),
            'top_5_symbols': counter.most_common(5)
        }
    
    def sliding_window_entropy(self, data: Union[str, bytes], 
                               step: int = 1) -> List[Tuple[int, float]]:
        """
        计算滑动窗口熵
        
        Args:
            data: 输入数据
            step: 滑动步长
            
        Returns:
            (位置, 熵值) 列表
        """
        if isinstance(data, str):
            data = data.encode('utf-8')
        
        results = []
        for i in range(0, len(data) - self.window_size + 1, step):
            window = data[i:i + self.window_size]
            entropy = EntropyUtils.shannon_entropy(window)
            results.append((i, entropy))
        
        return results
    
    def find_high_entropy_regions(self, data: Union[str, bytes], 
                                   threshold: float = 7.0,
                                   min_length: int = 64) -> List[Tuple[int, int, float]]:
        """
        找出高熵区域
        
        Args:
            data: 输入数据
            threshold: 熵阈值
            min_length: 最小区域长度
            
        Returns:
            [(起始位置, 结束位置, 平均熵), ...]
        """
        if isinstance(data, str):
            data = data.encode('utf-8')
        
        high_entropy_regions = []
        start = None
        
        for i in range(0, len(data) - self.window_size + 1):
            window = data[i:i + self.window_size]
            entropy = EntropyUtils.shannon_entropy(window)
            
            if entropy >= threshold:
                if start is None:
                    start = i
            else:
                if start is not None:
                    end = i + self.window_size - 1
                    if end - start >= min_length:
                        # 计算平均熵
                        region = data[start:end]
                        avg_entropy = EntropyUtils.shannon_entropy(region)
                        high_entropy_regions.append((start, end, round(avg_entropy, 4)))
                    start = None
        
        # 处理结尾区域
        if start is not None:
            end = len(data)
            region = data[start:end]
            avg_entropy = EntropyUtils.shannon_entropy(region)
            high_entropy_regions.append((start, end, round(avg_entropy, 4)))
        
        return high_entropy_regions


# 便捷函数
def shannon_entropy(data: Union[str, bytes, List[Any]]) -> float:
    """计算香农熵的便捷函数"""
    return EntropyUtils.shannon_entropy(data)


def analyze_password(password: str) -> PasswordAnalysis:
    """分析密码的便捷函数"""
    return PasswordEntropy().analyze(password)


def entropy_report(data: Union[str, bytes, List[Any]]) -> Dict[str, Any]:
    """生成熵分析报告的便捷函数"""
    return EntropyUtils.analyze_distribution(data)


if __name__ == "__main__":
    print("=" * 60)
    print("熵计算工具模块演示")
    print("=" * 60)
    
    # 1. 香农熵
    print("\n【1. 香农熵计算】")
    test_strings = ["aaaaaa", "abcdef", "Hello, World!", "密码测试123!@#"]
    for s in test_strings:
        entropy = EntropyUtils.shannon_entropy(s)
        print(f"  '{s}': {entropy:.4f} bits/char")
    
    # 2. 密码分析
    print("\n【2. 密码强度分析】")
    analyzer = PasswordEntropy()
    passwords = ["123456", "password", "MyP@ssw0rd!", "Tr0ub4dor&3"]
    for pwd in passwords:
        result = analyzer.analyze(pwd)
        print(f"  '{pwd}':")
        print(f"    熵值: {result.entropy} bits")
        print(f"    强度: {result.strength}")
        print(f"    破解时间: {result.crack_time_estimate}")
    
    # 3. 数据分布分析
    print("\n【3. 数据分布分析】")
    data = "The quick brown fox jumps over the lazy dog"
    analysis = EntropyUtils.analyze_distribution(data)
    print(f"  数据: '{data}'")
    print(f"  香农熵: {analysis['shannon_entropy']}")
    print(f"  最小熵: {analysis['min_entropy']}")
    print(f"  基尼不纯度: {analysis['gini_impurity']}")
    print(f"  压缩潜力: {analysis['compression_potential']}")
    print(f"  随机性得分: {analysis['randomness_score']}")
    
    # 4. 互信息
    print("\n【4. 互信息计算】")
    x = [1, 1, 2, 2, 3, 3, 4, 4]
    y = [1, 2, 1, 2, 3, 4, 3, 4]
    mi = EntropyUtils.mutual_information(x, y)
    print(f"  变量X: {x}")
    print(f"  变量Y: {y}")
    print(f"  互信息: {mi:.4f} bits")
    
    # 5. KL散度
    print("\n【5. KL散度计算】")
    p = {'A': 0.5, 'B': 0.3, 'C': 0.2}
    q = {'A': 0.4, 'B': 0.4, 'C': 0.2}
    kl = EntropyUtils.kl_divergence(p, q)
    print(f"  分布P: {p}")
    print(f"  分布Q: {q}")
    print(f"  KL(P||Q): {kl:.4f}")
    
    # 6. Rényi熵
    print("\n【6. Rényi熵计算】")
    data = "aabbcc"
    for alpha in [0, 0.5, 1, 2, 3]:
        if alpha == 1:
            entropy = EntropyUtils.shannon_entropy(data)
        else:
            entropy = EntropyUtils.renyi_entropy(data, alpha)
        print(f"  α={alpha}: {entropy:.4f} bits")
    
    print("\n" + "=" * 60)
    print("演示完成")
    print("=" * 60)