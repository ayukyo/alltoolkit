"""
Wavelet Utils - 小波变换工具模块

小波变换是一种强大的信号分析工具，可用于信号压缩、噪声滤波、特征提取等。
特点：
- 多分辨率分析：不同尺度下的信号特征
- 时频局部化：同时保留时间和频率信息
- 去相关性：有效压缩信号
- 快速算法：计算效率高

应用场景：
- 信号压缩与编码
- 噪声去除与信号增强
- 图像处理（边缘检测、去噪）
- 特征提取与模式识别
- 生物医学信号分析（ECG、EEG）
- 地震信号处理

零外部依赖，仅使用 Python 标准库。
"""

import math
from typing import List, Tuple, Optional, Dict, Any
from dataclasses import dataclass
from copy import deepcopy


@dataclass
class WaveletCoefficients:
    """小波变换系数结构"""
    approximation: List[float]      # 近似系数 (低频)
    details: List[List[float]]      # 各层细节系数 (高频)
    levels: int                     # 分解层数
    wavelet_type: str               # 小波类型
    
    def get_all_coefficients(self) -> List[float]:
        """获取所有系数的扁平列表"""
        result = self.approximation.copy()
        for detail in self.details:
            result.extend(detail)
        return result
    
    def get_total_coefficients(self) -> int:
        """获取总系数数量"""
        return len(self.approximation) + sum(len(d) for d in self.details)


class WaveletBase:
    """小波基类"""
    
    @staticmethod
    def haar() -> Tuple[List[float], List[float]]:
        """
        Haar 小波
        
        最简单的小波，适合入门理解和快速计算。
        分解滤波器: [1, 1] / sqrt(2) (低通), [1, -1] / sqrt(2) (高通)
        """
        scale = 1.0 / math.sqrt(2)
        return ([scale, scale], [scale, -scale])
    
    @staticmethod
    def daubechies2() -> Tuple[List[float], List[float]]:
        """
        Daubechies 2 (D2) 小波
        
        也称为 D4 (因为滤波器长度为4)。
        最短的正交小波，具有连续性。
        """
        # D2 滤波器系数
        h0 = (1 + math.sqrt(3)) / (4 * math.sqrt(2))
        h1 = (3 + math.sqrt(3)) / (4 * math.sqrt(2))
        h2 = (3 - math.sqrt(3)) / (4 * math.sqrt(2))
        h3 = (1 - math.sqrt(3)) / (4 * math.sqrt(2))
        
        low_pass = [h0, h1, h2, h3]
        # 高通滤波器由低通滤波器推导
        high_pass = [h3, -h2, h1, -h0]
        
        return (low_pass, high_pass)
    
    @staticmethod
    def daubechies4() -> Tuple[List[float], List[float]]:
        """
        Daubechies 4 (D4) 小波
        
        滤波器长度为8，更平滑的小波。
        """
        # D4 滤波器系数 (近似值)
        coeffs = [
            0.2303778133088964,
            0.7148465705529154,
            0.6308807679398587,
            -0.0279837694168599,
            -0.1870348117190911,
            0.0308413818355607,
            0.0328830116668852,
            -0.0105974017850690
        ]
        
        low_pass = coeffs.copy()
        # 高通滤波器: 交替符号反转
        high_pass = [
            -coeffs[7], coeffs[6], -coeffs[5], coeffs[4],
            -coeffs[3], coeffs[2], -coeffs[1], coeffs[0]
        ]
        
        return (low_pass, high_pass)
    
    @staticmethod
    def get_wavelet(name: str) -> Tuple[List[float], List[float]]:
        """
        获取指定小波的滤波器系数
        
        Args:
            name: 小波名称 ('haar', 'db2', 'db4')
            
        Returns:
            (低通滤波器, 高通滤波器)
        """
        wavelets = {
            'haar': WaveletBase.haar,
            'db1': WaveletBase.haar,
            'db2': WaveletBase.daubechies2,
            'db4': WaveletBase.daubechies4
        }
        
        if name.lower() not in wavelets:
            raise ValueError(f"不支持的小波类型: {name}. 可选: {list(wavelets.keys())}")
        
        return wavelets[name.lower()]()


class DiscreteWaveletTransform:
    """
    离散小波变换 (DWT)
    
    使用示例：
        >>> dwt = DiscreteWaveletTransform(wavelet='haar')
        >>> signal = [1, 2, 3, 4, 5, 6, 7, 8]
        >>> coeffs = dwt.decompose(signal, levels=3)
        >>> reconstructed = dwt.reconstruct(coeffs)
    """
    
    def __init__(self, wavelet: str = 'haar'):
        """
        初始化 DWT
        
        Args:
            wavelet: 小波类型 ('haar', 'db2', 'db4')
        """
        self._wavelet = wavelet.lower()
        self._low_pass, self._high_pass = WaveletBase.get_wavelet(self._wavelet)
        self._filter_len = len(self._low_pass)
    
    def _convolve_downsample(
        self, 
        signal: List[float], 
        filter: List[float]
    ) -> List[float]:
        """
        卷积并下采样（简化版）
        
        Args:
            signal: 输入信号
            filter: 滤波器系数
            
        Returns:
            下采样后的结果
        """
        n = len(signal)
        f_len = len(filter)
        
        result = []
        # 对于 Haar（长度为2），直接计算
        if f_len == 2:
            for i in range(0, n - 1, 2):
                val = signal[i] * filter[0] + signal[i + 1] * filter[1]
                result.append(val)
        else:
            # 对于其他滤波器，使用周期扩展
            for i in range(0, n, 2):
                val = 0.0
                for j in range(f_len):
                    idx = (i + j) % n
                    val += signal[idx] * filter[j]
                result.append(val)
        
        return result
    
    def _upsample_convolve(
        self, 
        coeffs: List[float], 
        filter: List[float],
        output_len: int
    ) -> List[float]:
        """
        上采样并卷积（简化版）
        
        Args:
            coeffs: 输入系数
            filter: 滤波器系数
            output_len: 输出长度
            
        Returns:
            上采样后的结果
        """
        f_len = len(filter)
        
        # 上采样：在每两个值之间插入0
        upsampled = []
        for c in coeffs:
            upsampled.append(c)
            upsampled.append(0.0)
        
        result = [0.0] * output_len
        
        # 对于 Haar（长度为2），简化计算
        if f_len == 2:
            for i in range(min(output_len, len(upsampled))):
                if i < len(upsampled):
                    result[i] = upsampled[i] * filter[0]
                if i + 1 < len(upsampled) and i + 1 < output_len:
                    result[i + 1] = upsampled[i] * filter[1]
        else:
            # 一般卷积
            for i in range(output_len):
                val = 0.0
                for j in range(f_len):
                    idx = i - j + f_len // 2 - 1
                    if 0 <= idx < len(upsampled):
                        val += upsampled[idx] * filter[j]
                result[i] = val
        
        return result
    
    def decompose(
        self, 
        signal: List[float], 
        levels: Optional[int] = None
    ) -> WaveletCoefficients:
        """
        多级小波分解
        
        Args:
            signal: 输入信号
            levels: 分解层数（默认为最大可能层数）
            
        Returns:
            WaveletCoefficients 结构
        """
        if len(signal) < 2:
            raise ValueError("信号长度必须至少为 2")
        
        # 计算最大分解层数
        max_levels = int(math.log2(len(signal)))
        if levels is None:
            levels = max_levels
        elif levels > max_levels:
            levels = max_levels
        
        approximation = signal.copy()
        details = []
        
        for level in range(levels):
            if len(approximation) < self._filter_len:
                break
            
            # 分解为近似和细节
            new_approx = self._convolve_downsample(approximation, self._low_pass)
            detail = self._convolve_downsample(approximation, self._high_pass)
            
            details.append(detail)
            approximation = new_approx
        
        return WaveletCoefficients(
            approximation=approximation,
            details=details,
            levels=len(details),
            wavelet_type=self._wavelet
        )
    
    def reconstruct(self, coeffs: WaveletCoefficients) -> List[float]:
        """
        小波重构
        
        Args:
            coeffs: 小波系数结构
            
        Returns:
            重构的信号
        """
        approximation = coeffs.approximation.copy()
        details = coeffs.details.copy()
        
        # Haar 小波完美重构
        if self._wavelet == 'haar' or self._wavelet == 'db1':
            # 从最低层开始重构
            for level in range(len(details) - 1, -1, -1):
                detail = details[level]
                
                # Haar 逆变换：完美重构公式
                # 前向变换: approx = (a+b)/sqrt(2), detail = (a-b)/sqrt(2)
                # 逆变换: a = (approx+detail)/sqrt(2), b = (approx-detail)/sqrt(2)
                result = []
                
                for i in range(len(approximation)):
                    if i < len(detail):
                        # 逆变换公式
                        val1 = (approximation[i] + detail[i]) / math.sqrt(2)
                        val2 = (approximation[i] - detail[i]) / math.sqrt(2)
                        result.append(val1)
                        result.append(val2)
                
                approximation = result
            
            return approximation
        else:
            # 其他小波使用通用重构
            for level in range(len(details) - 1, -1, -1):
                detail = details[level]
                
                prev_len = len(approximation) * 2
                
                approx_part = self._upsample_convolve(approximation, self._low_pass, prev_len)
                detail_part = self._upsample_convolve(detail, self._high_pass, prev_len)
                
                approximation = [
                    approx_part[i] + detail_part[i] 
                    for i in range(min(prev_len, len(approx_part), len(detail_part)))
                ]
            
            return approximation
    
    def get_wavelet_info(self) -> Dict[str, Any]:
        """获取小波信息"""
        return {
            'wavelet_type': self._wavelet,
            'filter_length': self._filter_len,
            'low_pass_filter': self._low_pass,
            'high_pass_filter': self._high_pass
        }


class WaveletPacketTransform:
    """
    小波包变换
    
    不仅分解近似系数，也分解细节系数，提供更精细的时频分析。
    
    使用示例：
        >>> wpt = WaveletPacketTransform(wavelet='haar')
        >>> signal = [1, 2, 3, 4, 5, 6, 7, 8]
        >>> tree = wpt.decompose(signal, levels=3)
        >>> best_basis = wpt.find_best_basis(tree)
    """
    
    def __init__(self, wavelet: str = 'haar'):
        """初始化小波包变换"""
        self._wavelet = wavelet.lower()
        self._low_pass, self._high_pass = WaveletBase.get_wavelet(self._wavelet)
        self._filter_len = len(self._low_pass)
    
    def _decompose_node(self, data: List[float]) -> Tuple[List[float], List[float]]:
        """分解单个节点"""
        # 简化的分解（类似DWT的单级分解）
        approx = []
        detail = []
        
        for i in range(0, len(data) - 1, 2):
            if i + 1 < len(data):
                # Haar 简化版本
                approx.append((data[i] + data[i+1]) / math.sqrt(2))
                detail.append((data[i] - data[i+1]) / math.sqrt(2))
        
        return approx, detail
    
    def decompose(
        self, 
        signal: List[float], 
        levels: int = 3
    ) -> Dict[str, List[float]]:
        """
        小波包分解
        
        Args:
            signal: 输入信号
            levels: 分解层数
            
        Returns:
            小波包树（字典形式），键为节点路径（如 'aaa', 'aad', 'ada' 等）
        """
        tree = {'': signal.copy()}
        
        for level in range(levels):
            new_nodes = {}
            for path, data in tree.items():
                if len(path) == level and len(data) >= 2:
                    approx, detail = self._decompose_node(data)
                    new_nodes[path + 'a'] = approx  # 近似
                    new_nodes[path + 'd'] = detail  # 细节
            
            tree.update(new_nodes)
        
        return tree
    
    def reconstruct_node(
        self, 
        tree: Dict[str, List[float]], 
        path: str = ''
    ) -> List[float]:
        """
        从指定节点重构
        
        Args:
            tree: 小波包树
            path: 节点路径
            
        Returns:
            重构的信号
        """
        if path not in tree:
            raise ValueError(f"节点路径 '{path}' 不存在")
        
        data = tree[path]
        
        # 如果是叶节点，直接返回
        if path + 'a' not in tree or path + 'd' not in tree:
            return data
        
        # 递归重构
        approx = self.reconstruct_node(tree, path + 'a')
        detail = self.reconstruct_node(tree, path + 'd')
        
        # 合并（逆变换）
        result = []
        for i in range(len(approx)):
            if i < len(detail):
                result.append((approx[i] + detail[i]) / math.sqrt(2))
                result.append((approx[i] - detail[i]) / math.sqrt(2))
        
        return result
    
    def find_best_basis(
        self, 
        tree: Dict[str, List[float]], 
        cost_func: str = 'entropy'
    ) -> List[str]:
        """
        寻找最佳基
        
        Args:
            tree: 小波包树
            cost_func: 成本函数 ('entropy', 'threshold', 'energy')
            
        Returns:
            最佳基节点列表
        """
        def entropy(data: List[float]) -> float:
            """香农熵"""
            if not data:
                return 0.0
            total = sum(abs(x) for x in data)
            if total == 0:
                return 0.0
            e = 0.0
            for x in data:
                p = abs(x) / total
                if p > 0:
                    e -= p * math.log2(p)
            return e
        
        def threshold_cost(data: List[float], threshold: float = 0.1) -> float:
            """阈值成本：超过阈值的系数数量"""
            return sum(1 for x in data if abs(x) > threshold)
        
        def energy(data: List[float]) -> float:
            """能量成本"""
            return sum(x*x for x in data)
        
        cost_functions = {
            'entropy': entropy,
            'threshold': threshold_cost,
            'energy': energy
        }
        
        if cost_func not in cost_functions:
            raise ValueError(f"不支持的成本函数: {cost_func}")
        
        cost_fn = cost_functions[cost_func]
        
        # 计算每个节点的成本
        costs = {path: cost_fn(data) for path, data in tree.items()}
        
        # 寻找最佳基（简化版：选择叶节点中成本最小的）
        leaf_nodes = [
            path for path in tree.keys()
            if path + 'a' not in tree or path + 'd' not in tree
        ]
        
        # 按成本排序
        sorted_leaves = sorted(leaf_nodes, key=lambda p: costs.get(p, float('inf')))
        
        return sorted_leaves


class WaveletDenoiser:
    """
    小波去噪
    
    使用小波变换进行信号去噪，基于阈值方法。
    
    使用示例：
        >>> denoiser = WaveletDenoiser(wavelet='haar', threshold_method='soft')
        >>> noisy_signal = [1.5, 2.3, 2.8, 4.1, ...]
        >>> clean_signal = denoiser.denoise(noisy_signal)
    """
    
    def __init__(
        self, 
        wavelet: str = 'haar',
        threshold_method: str = 'soft',
        threshold_mode: str = 'universal'
    ):
        """
        初始化去噪器
        
        Args:
            wavelet: 小波类型
            threshold_method: 阈值方法 ('soft', 'hard')
            threshold_mode: 阈值模式 ('universal', 'adaptive', 'manual')
        """
        self._dwt = DiscreteWaveletTransform(wavelet)
        self._threshold_method = threshold_method.lower()
        self._threshold_mode = threshold_mode.lower()
    
    def _calculate_threshold(self, details: List[List[float]]) -> List[float]:
        """
        计算阈值
        
        Args:
            details: 各层细节系数
            
        Returns:
            各层的阈值
        """
        thresholds = []
        
        for detail in details:
            if self._threshold_mode == 'universal':
                # Universal 阈值: σ * sqrt(2 * log(n))
                n = len(detail)
                if n == 0:
                    thresholds.append(0.0)
                    continue
                
                # 估计噪声标准差（使用 MAD）
                median = sorted(abs(x) for x in detail)[n // 2] if n > 0 else 0
                sigma = median / 0.6745  # MAD 估计
                
                threshold = sigma * math.sqrt(2 * math.log(n)) if n > 1 else 0
                thresholds.append(threshold)
                
            elif self._threshold_mode == 'adaptive':
                # Adaptive 阈值（SureShrink）
                n = len(detail)
                if n == 0:
                    thresholds.append(0.0)
                    continue
                
                sigma = self._estimate_sigma(detail)
                threshold = min(
                    sigma * math.sqrt(2 * math.log(n)),
                    self._sure_threshold(detail, sigma)
                )
                thresholds.append(threshold)
                
            else:
                # Manual 模式使用默认值
                thresholds.append(0.5)
        
        return thresholds
    
    def _estimate_sigma(self, data: List[float]) -> float:
        """估计噪声标准差"""
        if not data:
            return 0.0
        median = sorted(abs(x) for x in data)[len(data) // 2]
        return median / 0.6745
    
    def _sure_threshold(self, data: List[float], sigma: float) -> float:
        """SURE 阈值估计"""
        n = len(data)
        if n == 0:
            return 0.0
        
        # Stein's Unbiased Risk Estimate
        sorted_data = sorted(abs(x) for x in data)
        
        min_risk = float('inf')
        best_t = 0
        
        for k, x in enumerate(sorted_data):
            t = x
            risk = (n - 2*k + sum(1 for d in sorted_data[:k] if d < t)) * sigma**2 / n
            if risk < min_risk:
                min_risk = risk
                best_t = t
        
        return best_t
    
    def _apply_threshold(
        self, 
        value: float, 
        threshold: float
    ) -> float:
        """
        应用阈值
        
        Args:
            value: 系数值
            threshold: 阈值
            
        Returns:
            处理后的值
        """
        abs_val = abs(value)
        
        if abs_val <= threshold:
            return 0.0
        
        if self._threshold_method == 'soft':
            # 软阈值：收缩
            sign = 1 if value >= 0 else -1
            return sign * (abs_val - threshold)
        else:
            # 硬阈值：保留或置零
            return value
    
    def denoise(
        self, 
        signal: List[float],
        levels: Optional[int] = None,
        manual_threshold: Optional[float] = None
    ) -> List[float]:
        """
        信号去噪
        
        Args:
            signal: 含噪信号
            levels: 分解层数
            manual_threshold: 手动阈值（threshold_mode='manual' 时使用）
            
        Returns:
            去噪后的信号
        """
        # 分解
        coeffs = self._dwt.decompose(signal, levels)
        
        # 计算阈值
        if self._threshold_mode == 'manual' and manual_threshold is not None:
            thresholds = [manual_threshold] * len(coeffs.details)
        else:
            thresholds = self._calculate_threshold(coeffs.details)
        
        # 应用阈值到细节系数
        denoised_details = []
        for i, detail in enumerate(coeffs.details):
            threshold = thresholds[i] if i < len(thresholds) else 0
            denoised = [
                self._apply_threshold(x, threshold) 
                for x in detail
            ]
            denoised_details.append(denoised)
        
        # 创建新的系数结构
        denoised_coeffs = WaveletCoefficients(
            approximation=coeffs.approximation,
            details=denoised_details,
            levels=coeffs.levels,
            wavelet_type=coeffs.wavelet_type
        )
        
        # 重构
        return self._dwt.reconstruct(denoised_coeffs)
    
    def get_noise_estimate(self, signal: List[float]) -> float:
        """
        估计噪声水平
        
        Args:
            signal: 含噪信号
            
        Returns:
            噪声标准差估计
        """
        coeffs = self._dwt.decompose(signal, levels=1)
        if not coeffs.details:
            return 0.0
        
        # 使用最精细层的细节系数估计噪声
        finest_detail = coeffs.details[0]
        return self._estimate_sigma(finest_detail)


class WaveletEnergyAnalyzer:
    """
    小波能量分析器
    
    分析信号在不同频带的能量分布。
    
    使用示例：
        >>> analyzer = WaveletEnergyAnalyzer(wavelet='haar')
        >>> signal = [1, 2, 3, 4, 5, 6, 7, 8]
        >>> energy_dist = analyzer.analyze_energy_distribution(signal)
    """
    
    def __init__(self, wavelet: str = 'haar'):
        """初始化分析器"""
        self._dwt = DiscreteWaveletTransform(wavelet)
    
    def analyze_energy_distribution(
        self, 
        signal: List[float],
        levels: Optional[int] = None
    ) -> Dict[str, float]:
        """
        分析能量分布
        
        Args:
            signal: 输入信号
            levels: 分解层数
            
        Returns:
            各频带的能量百分比
        """
        coeffs = self._dwt.decompose(signal, levels)
        
        # 计算各部分能量
        approx_energy = sum(x*x for x in coeffs.approximation)
        
        detail_energies = []
        for detail in coeffs.details:
            energy = sum(x*x for x in detail)
            detail_energies.append(energy)
        
        total_energy = approx_energy + sum(detail_energies)
        
        if total_energy == 0:
            return {'approximation': 0.0, 'total_energy': 0.0, 'details': {}}
        
        # 计算百分比
        result = {
            'approximation': approx_energy / total_energy,
            'total_energy': total_energy,
            'details': {}
        }
        
        for i, energy in enumerate(detail_energies):
            level_name = f'level_{i+1}'
            result['details'][level_name] = energy / total_energy
        
        return result
    
    def get_frequency_bands(
        self, 
        signal_length: int,
        levels: int
    ) -> List[Tuple[float, float]]:
        """
        计算各层对应的频带
        
        Args:
            signal_length: 信号长度
            levels: 分解层数
            
        Returns:
            各层的频带范围 (low, high)
        """
        # 假设采样率为1，实际应用中需要调整
        nyquist = 0.5  # Nyquist频率
        
        bands = []
        for level in range(levels):
            low = 0
            high = nyquist / (2 ** level)
            bands.append((low, high))
        
        # 近似系数对应的频带
        approx_band = (0, nyquist / (2 ** levels))
        
        return bands, approx_band
    
    def detect_anomalies(
        self, 
        signal: List[float],
        threshold_ratio: float = 2.0
    ) -> List[int]:
        """
        基于能量检测异常
        
        Args:
            signal: 输入信号
            threshold_ratio: 异常阈值比率
            
        Returns:
            异常位置索引列表
        """
        coeffs = self._dwt.decompose(signal, levels=1)
        
        if not coeffs.details:
            return []
        
        # 使用最精细层细节系数检测异常
        finest_detail = coeffs.details[0]
        
        # 计算平均能量
        avg_energy = sum(x*x for x in finest_detail) / len(finest_detail)
        threshold = avg_energy * threshold_ratio
        
        # 找出超过阈值的点
        anomalies = []
        for i, val in enumerate(finest_detail):
            if val*val > threshold:
                # 映射回原始信号位置
                original_pos = i * 2
                if original_pos < len(signal):
                    anomalies.append(original_pos)
        
        return anomalies


# 便捷函数
def dwt_decompose(
    signal: List[float],
    wavelet: str = 'haar',
    levels: Optional[int] = None
) -> WaveletCoefficients:
    """
    快速 DWT 分解
    
    Args:
        signal: 输入信号
        wavelet: 小波类型
        levels: 分解层数
        
    Returns:
        小波系数
    """
    dwt = DiscreteWaveletTransform(wavelet)
    return dwt.decompose(signal, levels)


def dwt_reconstruct(coeffs: WaveletCoefficients, wavelet: str = 'haar') -> List[float]:
    """
    快速 DWT 重构
    
    Args:
        coeffs: 小波系数
        wavelet: 小波类型
        
    Returns:
        重构信号
    """
    dwt = DiscreteWaveletTransform(wavelet)
    return dwt.reconstruct(coeffs)


def denoise_signal(
    signal: List[float],
    wavelet: str = 'haar',
    method: str = 'soft'
) -> List[float]:
    """
    快速小波去噪
    
    Args:
        signal: 含噪信号
        wavelet: 小波类型
        method: 阈值方法
        
    Returns:
        去噪信号
    """
    denoiser = WaveletDenoiser(wavelet, threshold_method=method)
    return denoiser.denoise(signal)


def analyze_energy(
    signal: List[float],
    wavelet: str = 'haar'
) -> Dict[str, float]:
    """
    快速能量分析
    
    Args:
        signal: 输入信号
        wavelet: 小波类型
        
    Returns:
        能量分布
    """
    analyzer = WaveletEnergyAnalyzer(wavelet)
    return analyzer.analyze_energy_distribution(signal)


if __name__ == "__main__":
    # 简单演示
    print("=== Wavelet Utils 演示 ===")
    
    # 创建测试信号
    signal = [1, 2, 3, 4, 5, 6, 7, 8]
    print(f"原始信号: {signal}")
    
    # DWT 分解与重构
    dwt = DiscreteWaveletTransform('haar')
    coeffs = dwt.decompose(signal, levels=3)
    print(f"\n分解结果:")
    print(f"  近似系数: {coeffs.approximation}")
    for i, detail in enumerate(coeffs.details):
        print(f"  第{i+1}层细节: {detail}")
    
    reconstructed = dwt.reconstruct(coeffs)
    print(f"\n重构信号: {[round(x, 4) for x in reconstructed]}")
    
    # 去噪演示
    noisy_signal = [s + 0.5 * (math.sin(s) + 0.3) for s in signal]
    denoiser = WaveletDenoiser('haar', 'soft')
    clean = denoiser.denoise(noisy_signal)
    print(f"\n去噪演示:")
    print(f"  含噪信号: {[round(x, 2) for x in noisy_signal]}")
    print(f"  去噪后: {[round(x, 2) for x in clean]}")
    
    # 能量分析
    analyzer = WaveletEnergyAnalyzer('haar')
    energy = analyzer.analyze_energy_distribution(signal)
    print(f"\n能量分析:")
    print(f"  总能量: {energy['total_energy']}")
    print(f"  近似系数占比: {energy['approximation']:.2%}")
    for level, pct in energy['details'].items():
        print(f"  {level}: {pct:.2%}")