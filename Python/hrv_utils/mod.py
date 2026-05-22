"""
HRV (Heart Rate Variability) - 心率变异性分析工具

心率变异性是连续心跳间隔时间的变化程度，是评估自律神经系统功能
和心血管健康的重要指标。本模块提供完整的 HRV 分析功能。

核心功能:
1. 时域分析 - SDNN, RMSSD, pNN50, NN50 等
2. 频域分析 - VLF, LF, HF 功率及比率
3. 非线性分析 - Poincaré 图, SD1, SD2, ApEn
4. 健康评估 - 压力指数, 恢复状态, 心脏年龄
5. 异常检测 - 心律不齐识别

参考标准:
- Task Force of ESC/NASPE (1996)
- 获取 RR 间期数据后可直接分析
"""

import math
from typing import List, Tuple, Optional, Dict, Any
from collections import deque
from dataclasses import dataclass


# ============================================================================
# 数据结构定义
# ============================================================================

@dataclass
class TimeDomainMetrics:
    """时域分析指标"""
    # 基础统计
    mean_nn: float  # 平均 NN 间期 (ms)
    sdnn: float  # NN 间期标准差 (ms)
    nn_count: int  # 有效心跳数
    
    # 差分指标
    rmssd: float  # 相邻 NN 间期差值的均方根 (ms)
    nn50: int  # 相邻 NN 间期差值超过 50ms 的数量
    pnn50: float  # NN50 占总数的百分比 (%)
    
    # 其他
    sdann: Optional[float] = None  # 5分钟均值的标准差
    sdnn_index: Optional[float] = None  # 5分钟标准差的均值


@dataclass
class FrequencyDomainMetrics:
    """频域分析指标"""
    # 功率谱密度 (ms²)
    total_power: float  # 总功率
    vlf: float  # 极低频功率 (0.0033-0.04 Hz)
    lf: float  # 低频功率 (0.04-0.15 Hz)
    hf: float  # 高频功率 (0.15-0.4 Hz)
    
    # 标准化单位 (n.u.)
    lf_nu: float  # 标准化低频功率
    hf_nu: float  # 标准化高频功率
    
    # 比率
    lf_hf_ratio: float  # LF/HF 比率


@dataclass
class NonlinearMetrics:
    """非线性分析指标"""
    # Poincaré 图指标
    sd1: float  # 短期变异性 (ms)
    sd2: float  # 长期变异性 (ms)
    sd1_sd2_ratio: float  # SD1/SD2 比率
    
    # 熵指标
    apen: Optional[float] = None  # 近似熵
    sampen: Optional[float] = None  # 样本熵
    
    # 分形维数
    dfa_alpha1: Optional[float] = None  # 短期 DFA
    dfa_alpha2: Optional[float] = None  # 长期 DFA


@dataclass
class HealthAssessment:
    """健康评估结果"""
    stress_index: float  # 压力指数 (0-100)
    stress_level: str  # 压力等级描述
    recovery_status: str  # 恢复状态
    autonomic_balance: str  # 自律神经平衡状态
    hrv_age: Optional[int] = None  # 心脏年龄估计
    recommendations: List[str] = None  # 建议列表
    
    def __post_init__(self):
        if self.recommendations is None:
            self.recommendations = []


@dataclass
class ArrhythmiaDetection:
    """心律异常检测结果"""
    has_arrhythmia: bool  # 是否检测到异常
    ectopic_beats: int  # 异位搏动数量
    missed_beats: int  # 漏搏数量
    short_intervals: int  # 短间期数量
    long_intervals: int  # 长间期数量
    irregularity_score: float  # 不规则指数 (0-1)
    details: List[Dict[str, Any]]  # 详细异常列表


# ============================================================================
# 数据预处理
# ============================================================================

def preprocess_rr_intervals(
    rr_intervals: List[float],
    artifact_threshold: float = 0.2,
    min_rr: float = 300,
    max_rr: float = 2000,
    interpolate: bool = True
) -> Tuple[List[float], List[int]]:
    """
    预处理 RR 间期数据，去除伪影和异常值
    
    Args:
        rr_intervals: RR 间期列表 (ms)
        artifact_threshold: 伪影检测阈值 (相对变化比例)
        min_rr: 最小有效 RR 间期 (ms)
        max_rr: 最大有效 RR 间期 (ms)
        interpolate: 是否对缺失值进行插值
    
    Returns:
        (清理后的 RR 间期列表, 异常值索引列表)
    
    Example:
        >>> rr = [800, 810, 400, 820, 830]  # 400 是异常值
        >>> clean_rr, artifacts = preprocess_rr_intervals(rr)
        >>> len(artifacts) > 0
        True
    """
    if len(rr_intervals) < 3:
        return rr_intervals.copy(), []
    
    clean_rr = rr_intervals.copy()
    artifacts = []
    
    # 计算中位数作为参考
    sorted_rr = sorted(rr_intervals)
    n = len(sorted_rr)
    median_rr = sorted_rr[n // 2] if n % 2 else (sorted_rr[n//2-1] + sorted_rr[n//2]) / 2
    
    # 第一遍：检测异常值
    for i, rr in enumerate(rr_intervals):
        is_artifact = False
        
        # 生理范围检查
        if rr < min_rr or rr > max_rr:
            is_artifact = True
        
        # 相邻间期变化检查
        if i > 0 and not is_artifact:
            prev_rr = clean_rr[i - 1]
            if prev_rr is not None and prev_rr > 0:
                change = abs(rr - prev_rr) / prev_rr
                if change > artifact_threshold:
                    is_artifact = True
        
        if is_artifact:
            artifacts.append(i)
            clean_rr[i] = None  # 标记为待处理
    
    # 第二遍：处理异常值
    if interpolate and artifacts:
        result = []
        for i, rr in enumerate(clean_rr):
            if rr is None:
                # 线性插值
                prev_idx = i - 1
                next_idx = i + 1
                while prev_idx >= 0 and clean_rr[prev_idx] is None:
                    prev_idx -= 1
                while next_idx < len(clean_rr) and clean_rr[next_idx] is None:
                    next_idx += 1
                
                if prev_idx >= 0 and next_idx < len(clean_rr):
                    # 线性插值
                    prev_rr = clean_rr[prev_idx]
                    next_rr = clean_rr[next_idx]
                    weight = (i - prev_idx) / (next_idx - prev_idx)
                    result.append(prev_rr + weight * (next_rr - prev_rr))
                elif prev_idx >= 0:
                    result.append(clean_rr[prev_idx])
                elif next_idx < len(clean_rr):
                    result.append(clean_rr[next_idx])
                else:
                    result.append(median_rr)
            else:
                result.append(rr)
        clean_rr = result
    
    # 过滤掉 None 值
    clean_rr = [rr for rr in clean_rr if rr is not None and rr > 0]
    
    return clean_rr, artifacts


def interpolate_rr_to_uniform(
    rr_intervals: List[float],
    target_rate: float = 4.0
) -> List[float]:
    """
    将不均匀的 RR 间期插值为均匀采样
    
    Args:
        rr_intervals: RR 间期列表 (ms)
        target_rate: 目标采样率 (Hz)
    
    Returns:
        均匀采样的心率值列表
    
    Example:
        >>> rr = [800, 810, 820, 815]
        >>> uniform = interpolate_rr_to_uniform(rr, target_rate=4.0)
    """
    if len(rr_intervals) < 2:
        return rr_intervals.copy()
    
    # 计算累积时间
    times = [0]
    for rr in rr_intervals:
        times.append(times[-1] + rr / 1000.0)  # 转换为秒
    
    # 目标采样间隔
    sample_interval = 1.0 / target_rate
    total_time = times[-1]
    
    # 计算每个时间点的瞬时心率
    inst_hr = []
    for rr in rr_intervals:
        inst_hr.append(60000.0 / rr)  # bpm
    
    # 插值
    result = []
    t = 0
    rr_idx = 0
    
    while t <= total_time and rr_idx < len(rr_intervals):
        # 找到当前时间对应的 RR 间期
        while rr_idx < len(times) - 1 and times[rr_idx + 1] < t:
            rr_idx += 1
        
        if rr_idx < len(inst_hr):
            # 线性插值
            if rr_idx < len(times) - 1 and times[rr_idx + 1] > times[rr_idx]:
                alpha = (t - times[rr_idx]) / (times[rr_idx + 1] - times[rr_idx])
                hr = inst_hr[rr_idx] * (1 - alpha)
                if rr_idx + 1 < len(inst_hr):
                    hr += inst_hr[rr_idx + 1] * alpha
                result.append(hr)
            else:
                result.append(inst_hr[rr_idx] if rr_idx < len(inst_hr) else inst_hr[-1])
        
        t += sample_interval
    
    return result


# ============================================================================
# 时域分析
# ============================================================================

def calculate_time_domain_metrics(
    nn_intervals: List[float],
    segment_duration: int = 300  # 5分钟，单位秒
) -> TimeDomainMetrics:
    """
    计算时域 HRV 指标
    
    Args:
        nn_intervals: NN 间期列表 (ms)
        segment_duration: 分段时长 (秒)，用于计算 SDANN
    
    Returns:
        TimeDomainMetrics 对象
    
    Example:
        >>> nn = [800, 810, 795, 820, 815, 805, 825]
        >>> metrics = calculate_time_domain_metrics(nn)
        >>> metrics.sdnn > 0
        True
    """
    if len(nn_intervals) < 2:
        return TimeDomainMetrics(
            mean_nn=0, sdnn=0, nn_count=len(nn_intervals),
            rmssd=0, nn50=0, pnn50=0
        )
    
    n = len(nn_intervals)
    
    # 计算均值
    mean_nn = sum(nn_intervals) / n
    
    # 计算 SDNN
    variance = sum((x - mean_nn) ** 2 for x in nn_intervals) / n
    sdnn = math.sqrt(variance)
    
    # 计算差分序列
    diffs = []
    for i in range(1, n):
        diffs.append(abs(nn_intervals[i] - nn_intervals[i - 1]))
    
    # 计算 RMSSD
    if diffs:
        rmssd = math.sqrt(sum(d ** 2 for d in diffs) / len(diffs))
    else:
        rmssd = 0
    
    # 计算 NN50 和 pNN50
    nn50 = sum(1 for d in diffs if d > 50)
    pnn50 = (nn50 / len(diffs) * 100) if diffs else 0
    
    # 计算 SDANN 和 SDNN Index (需要足够长的数据)
    sdann = None
    sdnn_index = None
    
    # 估算总时长
    total_time = sum(nn_intervals) / 1000.0  # 秒
    
    if total_time >= segment_duration:
        # 分段计算
        segment_means = []
        segment_sds = []
        current_segment = []
        current_time = 0
        
        for nn in nn_intervals:
            current_segment.append(nn)
            current_time += nn / 1000.0
            
            if current_time >= segment_duration:
                if len(current_segment) > 1:
                    seg_mean = sum(current_segment) / len(current_segment)
                    segment_means.append(seg_mean)
                    
                    seg_var = sum((x - seg_mean) ** 2 for x in current_segment) / len(current_segment)
                    segment_sds.append(math.sqrt(seg_var))
                
                current_segment = []
                current_time = 0
        
        if len(segment_means) > 1:
            sdann = math.sqrt(sum((x - sum(segment_means)/len(segment_means)) ** 2 
                                  for x in segment_means) / len(segment_means))
        
        if segment_sds:
            sdnn_index = sum(segment_sds) / len(segment_sds)
    
    return TimeDomainMetrics(
        mean_nn=mean_nn,
        sdnn=sdnn,
        nn_count=n,
        rmssd=rmssd,
        nn50=nn50,
        pnn50=pnn50,
        sdann=sdann,
        sdnn_index=sdnn_index
    )


# ============================================================================
# 频域分析
# ============================================================================

def _welch_psd(
    data: List[float],
    sample_rate: float,
    nperseg: int = 256
) -> Tuple[List[float], List[float]]:
    """
    使用 Welch 方法计算功率谱密度 (简化版)
    
    零外部依赖的 PSD 估计实现。
    """
    if len(data) < nperseg:
        nperseg = len(data)
    
    # 汉宁窗
    window = [0.5 * (1 - math.cos(2 * math.pi * i / (nperseg - 1))) 
              for i in range(nperseg)]
    
    # 重叠 50%
    noverlap = nperseg // 2
    step = nperseg - noverlap
    
    # 计算分段数
    n_segments = (len(data) - noverlap) // step
    
    if n_segments < 1:
        n_segments = 1
    
    # 频率分辨率
    freq_resolution = sample_rate / nperseg
    n_freqs = nperseg // 2 + 1
    
    # 初始化 PSD 累加器
    psd_sum = [0.0] * n_freqs
    
    for seg in range(n_segments):
        start = seg * step
        end = start + nperseg
        
        if end > len(data):
            break
        
        # 提取段并加窗
        segment = [data[start + i] * window[i] for i in range(nperseg)]
        
        # 去均值
        seg_mean = sum(segment) / nperseg
        segment = [x - seg_mean for x in segment]
        
        # 计算 FFT (使用 Cooley-Tukey 算法)
        fft_result = _fft(segment)
        
        # 计算功率谱
        window_power = sum(w ** 2 for w in window) / nperseg
        
        for i in range(n_freqs):
            power = (fft_result[i].real ** 2 + fft_result[i].imag ** 2) / (sample_rate * window_power)
            psd_sum[i] += power
    
    # 平均
    psd = [p / n_segments for p in psd_sum]
    
    # 频率轴
    freqs = [i * freq_resolution for i in range(n_freqs)]
    
    return freqs, psd


def _fft(x: List[float]) -> List[complex]:
    """
    快速傅里叶变换 (Cooley-Tukey 算法)
    """
    n = len(x)
    
    # 补零到 2 的幂次
    n_fft = 1
    while n_fft < n:
        n_fft *= 2
    
    x_padded = x + [0] * (n_fft - n)
    
    # 位反转排序
    result = [complex(v, 0) for v in x_padded]
    
    # FFT
    size = 2
    while size <= n_fft:
        half = size // 2
        for i in range(0, n_fft, size):
            for j in range(half):
                k = i + j + half
                t = complex(math.cos(-2 * math.pi * j / size),
                           math.sin(-2 * math.pi * j / size)) * result[k]
                result[k] = result[i + j] - t
                result[i + j] = result[i + j] + t
        size *= 2
    
    return result[:n]


def calculate_frequency_domain_metrics(
    nn_intervals: List[float],
    sample_rate: float = 4.0,
    method: str = 'welch'
) -> FrequencyDomainMetrics:
    """
    计算频域 HRV 指标
    
    Args:
        nn_intervals: NN 间期列表 (ms)
        sample_rate: 重采样率 (Hz)
        method: PSD 估计方法 ('welch')
    
    Returns:
        FrequencyDomainMetrics 对象
    
    Example:
        >>> nn = [800, 810, 795, 820, 815, 805, 825, 810, 790, 800]
        >>> metrics = calculate_frequency_domain_metrics(nn)
        >>> metrics.lf_hf_ratio > 0
        True
    """
    if len(nn_intervals) < 10:
        # 数据不足，返回默认值
        return FrequencyDomainMetrics(
            total_power=0, vlf=0, lf=0, hf=0,
            lf_nu=0, hf_nu=0, lf_hf_ratio=0
        )
    
    # 插值到均匀采样
    hr_signal = interpolate_rr_to_uniform(nn_intervals, sample_rate)
    
    if len(hr_signal) < 64:
        return FrequencyDomainMetrics(
            total_power=0, vlf=0, lf=0, hf=0,
            lf_nu=0, hf_nu=0, lf_hf_ratio=0
        )
    
    # 计算 PSD
    freqs, psd = _welch_psd(hr_signal, sample_rate)
    
    # 频带定义 (Hz)
    VLF_BAND = (0.0033, 0.04)
    LF_BAND = (0.04, 0.15)
    HF_BAND = (0.15, 0.4)
    
    # 计算各频带功率
    def band_power(low: float, high: float) -> float:
        power = 0
        for i, f in enumerate(freqs):
            if low <= f < high:
                power += psd[i]
        return power
    
    vlf_power = band_power(*VLF_BAND)
    lf_power = band_power(*LF_BAND)
    hf_power = band_power(*HF_BAND)
    total_power = vlf_power + lf_power + hf_power
    
    # 标准化功率
    lf_hf_sum = lf_power + hf_power
    if lf_hf_sum > 0:
        lf_nu = lf_power / lf_hf_sum * 100
        hf_nu = hf_power / lf_hf_sum * 100
    else:
        lf_nu = 0
        hf_nu = 0
    
    # LF/HF 比率
    lf_hf_ratio = lf_power / hf_power if hf_power > 0 else 0
    
    return FrequencyDomainMetrics(
        total_power=total_power,
        vlf=vlf_power,
        lf=lf_power,
        hf=hf_power,
        lf_nu=lf_nu,
        hf_nu=hf_nu,
        lf_hf_ratio=lf_hf_ratio
    )


# ============================================================================
# 非线性分析
# ============================================================================

def calculate_nonlinear_metrics(
    nn_intervals: List[float]
) -> NonlinearMetrics:
    """
    计算非线性 HRV 指标
    
    Args:
        nn_intervals: NN 间期列表 (ms)
    
    Returns:
        NonlinearMetrics 对象
    
    Example:
        >>> nn = [800, 810, 795, 820, 815, 805, 825, 810]
        >>> metrics = calculate_nonlinear_metrics(nn)
        >>> metrics.sd1 > 0
        True
    """
    n = len(nn_intervals)
    
    if n < 4:
        return NonlinearMetrics(
            sd1=0, sd2=0, sd1_sd2_ratio=0,
            apen=None, sampen=None
        )
    
    # ========== Poincaré 图分析 ==========
    # SD1 和 SD2 计算
    # SD1 = 短期变异性 (垂直于恒等线方向)
    # SD2 = 长期变异性 (沿恒等线方向)
    
    # 计算差分序列
    diffs = [nn_intervals[i + 1] - nn_intervals[i] for i in range(n - 1)]
    
    # 计算均值
    mean_nn = sum(nn_intervals) / n
    
    # SD1: 差分的标准差 / sqrt(2)
    if diffs:
        diff_var = sum((d - sum(diffs)/len(diffs)) ** 2 for d in diffs) / len(diffs)
        sd1 = math.sqrt(diff_var) / math.sqrt(2)
    else:
        sd1 = 0
    
    # SD2: 沿恒等线方向的标准差
    # SD2² = 2 * SDNN² - SD1²
    variance = sum((x - mean_nn) ** 2 for x in nn_intervals) / n
    sdnn = math.sqrt(variance)
    
    # 确保 SD2 计算
    sd2_squared = 2 * sdnn ** 2 - sd1 ** 2
    if sd2_squared > 0:
        sd2 = math.sqrt(sd2_squared)
    else:
        # 回退到 SDNN 作为 SD2 的近似
        sd2 = sdnn * math.sqrt(2)
    
    # SD2 应至少等于 SD1 (生理学合理性)
    sd2 = max(sd2, sd1)
    
    sd1_sd2_ratio = sd1 / sd2 if sd2 > 0 else 0
    
    # ========== 近似熵 (ApEn) ==========
    apen = _calculate_approximate_entropy(nn_intervals, m=2, r=0.2)
    
    # ========== 样本熵 (SampEn) ==========
    sampen = _calculate_sample_entropy(nn_intervals, m=2, r=0.2)
    
    return NonlinearMetrics(
        sd1=sd1,
        sd2=sd2,
        sd1_sd2_ratio=sd1_sd2_ratio,
        apen=apen,
        sampen=sampen
    )


def _calculate_approximate_entropy(
    data: List[float],
    m: int = 2,
    r: float = 0.2
) -> Optional[float]:
    """
    计算近似熵
    
    Args:
        data: 数据序列
        m: 嵌入维度
        r: 容差 (相对于标准差)
    """
    n = len(data)
    
    if n < m + 2:
        return None
    
    # 计算容差阈值
    mean_val = sum(data) / n
    variance = sum((x - mean_val) ** 2 for x in data) / n
    sd = math.sqrt(variance)
    threshold = r * sd
    
    if threshold == 0:
        return None
    
    def _max_dist(x1: List[float], x2: List[float]) -> float:
        return max(abs(a - b) for a, b in zip(x1, x2))
    
    def _phi(m_val: int) -> float:
        patterns = []
        for i in range(n - m_val + 1):
            patterns.append(data[i:i + m_val])
        
        c = []
        for i, pattern in enumerate(patterns):
            count = sum(1 for other in patterns 
                       if _max_dist(pattern, other) <= threshold)
            c.append(count / (n - m_val + 1))
        
        return sum(math.log(ci) for ci in c if ci > 0) / (n - m_val + 1)
    
    try:
        return _phi(m) - _phi(m + 1)
    except (ValueError, ZeroDivisionError):
        return None


def _calculate_sample_entropy(
    data: List[float],
    m: int = 2,
    r: float = 0.2
) -> Optional[float]:
    """
    计算样本熵
    
    Args:
        data: 数据序列
        m: 嵌入维度
        r: 容差 (相对于标准差)
    """
    n = len(data)
    
    if n < m + 2:
        return None
    
    # 计算容差阈值
    mean_val = sum(data) / n
    variance = sum((x - mean_val) ** 2 for x in data) / n
    sd = math.sqrt(variance)
    threshold = r * sd
    
    if threshold == 0:
        return None
    
    def _max_dist(x1: List[float], x2: List[float]) -> float:
        return max(abs(a - b) for a, b in zip(x1, x2))
    
    def _count_matches(m_val: int) -> int:
        patterns = []
        for i in range(n - m_val + 1):
            patterns.append((data[i:i + m_val], i))
        
        count = 0
        for i in range(len(patterns)):
            for j in range(i + 1, len(patterns)):
                if _max_dist(patterns[i][0], patterns[j][0]) <= threshold:
                    count += 1
        
        return count
    
    try:
        a = _count_matches(m)
        b = _count_matches(m + 1)
        
        if a == 0 or b == 0:
            return None
        
        return -math.log(b / a)
    except (ValueError, ZeroDivisionError):
        return None


# ============================================================================
# 心律异常检测
# ============================================================================

def detect_arrhythmias(
    nn_intervals: List[float],
    ectopic_threshold: float = 0.2,
    pause_threshold: float = 1.5
) -> ArrhythmiaDetection:
    """
    检测心律异常
    
    Args:
        nn_intervals: NN 间期列表 (ms)
        ectopic_threshold: 异位搏动检测阈值 (相对变化)
        pause_threshold: 暂停检测阈值 (相对于平均 RR)
    
    Returns:
        ArrhythmiaDetection 对象
    
    Example:
        >>> nn = [800, 400, 810, 795, 2000, 820, 815]
        >>> detection = detect_arrhythmias(nn)
        >>> detection.has_arrhythmia
        True
    """
    n = len(nn_intervals)
    
    if n < 3:
        return ArrhythmiaDetection(
            has_arrhythmia=False,
            ectopic_beats=0, missed_beats=0,
            short_intervals=0, long_intervals=0,
            irregularity_score=0, details=[]
        )
    
    # 计算参考值
    sorted_rr = sorted(nn_intervals)
    median_rr = sorted_rr[n // 2] if n % 2 else (sorted_rr[n//2-1] + sorted_rr[n//2]) / 2
    
    ectopic_beats = 0
    missed_beats = 0
    short_intervals = 0
    long_intervals = 0
    details = []
    
    # 检测短间期 (可能的 PAC - 房性早搏)
    short_threshold = median_rr * (1 - ectopic_threshold)
    # 检测长间期 (可能的暂停或 PVC 代偿间歇)
    long_threshold = median_rr * (1 + ectopic_threshold)
    # 检测严重长间期 (可能的漏搏)
    pause_threshold_value = median_rr * pause_threshold
    
    for i, rr in enumerate(nn_intervals):
        if rr < short_threshold:
            short_intervals += 1
            details.append({
                'type': 'short_interval',
                'index': i,
                'value': rr,
                'expected': median_rr
            })
            
            # 检查是否是异位搏动 (短间期后跟长间期)
            if i + 1 < n:
                next_rr = nn_intervals[i + 1]
                if next_rr > long_threshold:
                    ectopic_beats += 1
                    details.append({
                        'type': 'ectopic_beat',
                        'index': i,
                        'short_rr': rr,
                        'compensatory_rr': next_rr
                    })
        
        elif rr > pause_threshold_value:
            missed_beats += 1
            details.append({
                'type': 'missed_beat',
                'index': i,
                'value': rr,
                'expected': median_rr
            })
        
        elif rr > long_threshold:
            long_intervals += 1
            details.append({
                'type': 'long_interval',
                'index': i,
                'value': rr,
                'expected': median_rr
            })
    
    # 计算不规则指数
    if n > 1:
        diffs = [abs(nn_intervals[i + 1] - nn_intervals[i]) for i in range(n - 1)]
        mean_diff = sum(diffs) / len(diffs)
        irregularity_score = min(1.0, mean_diff / median_rr)
    else:
        irregularity_score = 0
    
    has_arrhythmia = (
        ectopic_beats > 0 or 
        missed_beats > 0 or 
        irregularity_score > 0.2 or
        short_intervals + long_intervals > n * 0.1
    )
    
    return ArrhythmiaDetection(
        has_arrhythmia=has_arrhythmia,
        ectopic_beats=ectopic_beats,
        missed_beats=missed_beats,
        short_intervals=short_intervals,
        long_intervals=long_intervals,
        irregularity_score=irregularity_score,
        details=details
    )


# ============================================================================
# 健康评估
# ============================================================================

def assess_health_status(
    time_metrics: TimeDomainMetrics,
    freq_metrics: Optional[FrequencyDomainMetrics] = None,
    nonlinear_metrics: Optional[NonlinearMetrics] = None,
    age: Optional[int] = None
) -> HealthAssessment:
    """
    综合健康状态评估
    
    Args:
        time_metrics: 时域指标
        freq_metrics: 频域指标 (可选)
        nonlinear_metrics: 非线性指标 (可选)
        age: 年龄 (可选，用于估算心脏年龄)
    
    Returns:
        HealthAssessment 对象
    
    Example:
        >>> nn = [800, 810, 795, 820, 815, 805, 825, 810, 790, 800,
        ...       805, 815, 790, 810, 805]
        >>> time_m = calculate_time_domain_metrics(nn)
        >>> assessment = assess_health_status(time_m)
        >>> assessment.stress_level in ['低', '中等', '高', '很高']
        True
    """
    # ========== 压力指数计算 ==========
    # 基于 RMSSD 和 pNN50 (副交感神经活动指标)
    # 低 RMSSD = 高压力
    
    # RMSSD 正常范围参考 (ms)
    # < 20: 非常低 (高压力)
    # 20-50: 低
    # 50-100: 正常
    # > 100: 高 (可能过度恢复)
    
    rmssd_score = 0
    if time_metrics.rmssd < 20:
        rmssd_score = 100  # 高压力
    elif time_metrics.rmssd < 50:
        rmssd_score = 70 + (50 - time_metrics.rmssd)  # 70-90
    elif time_metrics.rmssd < 100:
        rmssd_score = 30 + (100 - time_metrics.rmssd) * 0.4  # 30-50
    else:
        rmssd_score = max(10, 30 - (time_metrics.rmssd - 100) * 0.2)  # 低压力
    
    # pNN50 贡献
    pnn50_score = max(0, 50 - time_metrics.pnn50)  # 低 pNN50 = 高压力
    
    # SDNN 贡献 (整体变异性)
    sdnn_score = max(0, 80 - time_metrics.sdnn)  # 低 SDNN = 可能压力
    
    # 综合压力指数
    stress_index = (rmssd_score * 0.5 + pnn50_score * 0.3 + sdnn_score * 0.2)
    stress_index = min(100, max(0, stress_index))
    
    # 频域指标贡献
    if freq_metrics:
        # 低 LF/HF 比率 = 副交感主导 = 放松
        # 高 LF/HF 比率 = 交感主导 = 压力
        if freq_metrics.lf_hf_ratio > 4:
            stress_index = min(100, stress_index + 15)
        elif freq_metrics.lf_hf_ratio > 2:
            stress_index = min(100, stress_index + 5)
        elif freq_metrics.lf_hf_ratio < 0.5:
            stress_index = max(0, stress_index - 10)
    
    # 非线性指标贡献
    if nonlinear_metrics:
        # 低 SD1/SD2 比率 = 低短期变异性 = 压力
        if nonlinear_metrics.sd1_sd2_ratio < 0.2:
            stress_index = min(100, stress_index + 10)
    
    # 压力等级
    if stress_index < 25:
        stress_level = '低'
    elif stress_index < 50:
        stress_level = '中等'
    elif stress_index < 75:
        stress_level = '高'
    else:
        stress_level = '很高'
    
    # ========== 恢复状态评估 ==========
    # 基于 HRV 整体水平
    
    if time_metrics.rmssd > 80 and time_metrics.sdnn > 100:
        recovery_status = '优秀恢复'
    elif time_metrics.rmssd > 50 and time_metrics.sdnn > 50:
        recovery_status = '良好恢复'
    elif time_metrics.rmssd > 30 and time_metrics.sdnn > 30:
        recovery_status = '一般恢复'
    else:
        recovery_status = '恢复不足'
    
    # ========== 自律神经平衡 ==========
    if freq_metrics:
        if freq_metrics.lf_hf_ratio < 0.5:
            autonomic_balance = '副交感神经主导 (深度放松)'
        elif freq_metrics.lf_hf_ratio < 1.0:
            autonomic_balance = '副交感神经略占优势'
        elif freq_metrics.lf_hf_ratio < 2.0:
            autonomic_balance = '自律神经平衡'
        elif freq_metrics.lf_hf_ratio < 4.0:
            autonomic_balance = '交感神经略占优势'
        else:
            autonomic_balance = '交感神经主导 (应激状态)'
    else:
        if time_metrics.rmssd > 60:
            autonomic_balance = '副交感神经活跃'
        elif time_metrics.rmssd > 30:
            autonomic_balance = '自律神经相对平衡'
        else:
            autonomic_balance = '交感神经活跃'
    
    # ========== 心脏年龄估算 ==========
    hrv_age = None
    if age:
        # 基于 SDNN 的心脏年龄估算
        # 年龄-SDNN 参考关系 (简化)
        sdnn = time_metrics.sdnn
        
        # 年龄对应的 SDNN 参考值
        age_sdnn_map = {
            20: 65, 25: 60, 30: 55, 35: 50, 40: 45,
            45: 40, 50: 35, 55: 30, 60: 25, 65: 20, 70: 15
        }
        
        # 找到实际 SDNN 对应的年龄
        for a, ref_sdnn in age_sdnn_map.items():
            if sdnn >= ref_sdnn:
                hrv_age = a
                break
        else:
            hrv_age = 75
        
        # 微调
        if hrv_age < age - 10:
            hrv_age = max(20, age - 15)
        elif hrv_age > age + 10:
            hrv_age = min(80, age + 10)
    
    # ========== 建议生成 ==========
    recommendations = []
    
    if stress_index > 70:
        recommendations.append('建议进行深呼吸或冥想练习以缓解压力')
        recommendations.append('考虑减少咖啡因摄入')
    
    if time_metrics.rmssd < 30:
        recommendations.append('副交感神经活动较低，建议保证充足睡眠')
        recommendations.append('适度有氧运动有助于提高 HRV')
    
    if freq_metrics and freq_metrics.lf_hf_ratio > 3:
        recommendations.append('交感神经活动较高，建议放松活动如瑜伽、太极')
    
    if recovery_status == '恢复不足':
        recommendations.append('身体恢复不足，建议调整训练强度或休息')
    
    if hrv_age and age and hrv_age > age + 5:
        recommendations.append(f'心脏年龄 ({hrv_age}岁) 高于实际年龄，建议改善生活方式')
    
    if not recommendations:
        recommendations.append('HRV 指标良好，继续保持健康生活方式')
    
    return HealthAssessment(
        stress_index=round(stress_index, 1),
        stress_level=stress_level,
        recovery_status=recovery_status,
        autonomic_balance=autonomic_balance,
        hrv_age=hrv_age,
        recommendations=recommendations
    )


# ============================================================================
# 综合分析
# ============================================================================

def analyze_hrv(
    rr_intervals: List[float],
    age: Optional[int] = None,
    preprocess: bool = True,
    include_frequency: bool = True,
    include_nonlinear: bool = True
) -> Dict[str, Any]:
    """
    HRV 综合分析 - 一站式分析函数
    
    Args:
        rr_intervals: RR 间期列表 (ms)
        age: 年龄 (可选)
        preprocess: 是否预处理数据
        include_frequency: 是否包含频域分析
        include_nonlinear: 是否包含非线性分析
    
    Returns:
        包含所有分析结果的字典
    
    Example:
        >>> rr = [800, 810, 795, 820, 815, 805, 825, 810, 790, 800,
        ...       805, 815, 790, 810, 805, 820, 795, 810, 805, 815]
        >>> result = analyze_hrv(rr, age=30)
        >>> 'time_domain' in result
        True
    """
    # 预处理
    if preprocess:
        clean_rr, artifacts = preprocess_rr_intervals(rr_intervals)
    else:
        clean_rr = rr_intervals.copy()
        artifacts = []
    
    # 时域分析
    time_metrics = calculate_time_domain_metrics(clean_rr)
    
    # 频域分析
    freq_metrics = None
    if include_frequency:
        freq_metrics = calculate_frequency_domain_metrics(clean_rr)
    
    # 非线性分析
    nonlinear_metrics = None
    if include_nonlinear:
        nonlinear_metrics = calculate_nonlinear_metrics(clean_rr)
    
    # 心律异常检测
    arrhythmia = detect_arrhythmias(clean_rr)
    
    # 健康评估
    health = assess_health_status(
        time_metrics, freq_metrics, nonlinear_metrics, age
    )
    
    return {
        'time_domain': {
            'mean_nn': round(time_metrics.mean_nn, 2),
            'sdnn': round(time_metrics.sdnn, 2),
            'rmssd': round(time_metrics.rmssd, 2),
            'nn50': time_metrics.nn50,
            'pnn50': round(time_metrics.pnn50, 2),
            'sdann': round(time_metrics.sdann, 2) if time_metrics.sdann else None,
            'sdnn_index': round(time_metrics.sdnn_index, 2) if time_metrics.sdnn_index else None,
            'nn_count': time_metrics.nn_count
        },
        'frequency_domain': {
            'total_power': round(freq_metrics.total_power, 4) if freq_metrics else None,
            'vlf': round(freq_metrics.vlf, 4) if freq_metrics else None,
            'lf': round(freq_metrics.lf, 4) if freq_metrics else None,
            'hf': round(freq_metrics.hf, 4) if freq_metrics else None,
            'lf_nu': round(freq_metrics.lf_nu, 2) if freq_metrics else None,
            'hf_nu': round(freq_metrics.hf_nu, 2) if freq_metrics else None,
            'lf_hf_ratio': round(freq_metrics.lf_hf_ratio, 2) if freq_metrics else None
        } if freq_metrics else None,
        'nonlinear': {
            'sd1': round(nonlinear_metrics.sd1, 2),
            'sd2': round(nonlinear_metrics.sd2, 2),
            'sd1_sd2_ratio': round(nonlinear_metrics.sd1_sd2_ratio, 4),
            'apen': round(nonlinear_metrics.apen, 4) if nonlinear_metrics.apen else None,
            'sampen': round(nonlinear_metrics.sampen, 4) if nonlinear_metrics.sampen else None
        } if nonlinear_metrics else None,
        'arrhythmia': {
            'has_arrhythmia': arrhythmia.has_arrhythmia,
            'ectopic_beats': arrhythmia.ectopic_beats,
            'missed_beats': arrhythmia.missed_beats,
            'irregularity_score': round(arrhythmia.irregularity_score, 4)
        },
        'health_assessment': {
            'stress_index': health.stress_index,
            'stress_level': health.stress_level,
            'recovery_status': health.recovery_status,
            'autonomic_balance': health.autonomic_balance,
            'hrv_age': health.hrv_age,
            'recommendations': health.recommendations
        },
        'metadata': {
            'input_count': len(rr_intervals),
            'valid_count': len(clean_rr),
            'artifact_count': len(artifacts),
            'artifact_indices': artifacts[:10]  # 只返回前10个
        }
    }


def get_hrv_summary(rr_intervals: List[float], age: Optional[int] = None) -> str:
    """
    获取 HRV 分析文本摘要
    
    Args:
        rr_intervals: RR 间期列表 (ms)
        age: 年龄 (可选)
    
    Returns:
        分析结果文本摘要
    
    Example:
        >>> rr = [800, 810, 795, 820, 815, 805, 825, 810]
        >>> summary = get_hrv_summary(rr)
        >>> 'HRV' in summary
        True
    """
    result = analyze_hrv(rr_intervals, age=age)
    
    lines = [
        "=" * 50,
        "HRV (心率变异性) 分析报告",
        "=" * 50,
        "",
        "【时域分析】",
        f"  平均 NN 间期: {result['time_domain']['mean_nn']:.1f} ms",
        f"  SDNN: {result['time_domain']['sdnn']:.2f} ms",
        f"  RMSSD: {result['time_domain']['rmssd']:.2f} ms",
        f"  pNN50: {result['time_domain']['pnn50']:.1f}%",
        ""
    ]
    
    if result['frequency_domain']:
        lines.extend([
            "【频域分析】",
            f"  总功率: {result['frequency_domain']['total_power']:.2f} ms²",
            f"  LF 功率: {result['frequency_domain']['lf']:.2f} ms²",
            f"  HF 功率: {result['frequency_domain']['hf']:.2f} ms²",
            f"  LF/HF 比率: {result['frequency_domain']['lf_hf_ratio']:.2f}",
            ""
        ])
    
    if result['nonlinear']:
        lines.extend([
            "【非线性分析】",
            f"  SD1: {result['nonlinear']['sd1']:.2f} ms",
            f"  SD2: {result['nonlinear']['sd2']:.2f} ms",
            f"  SD1/SD2: {result['nonlinear']['sd1_sd2_ratio']:.4f}",
            ""
        ])
    
    lines.extend([
        "【健康评估】",
        f"  压力指数: {result['health_assessment']['stress_index']}/100 ({result['health_assessment']['stress_level']})",
        f"  恢复状态: {result['health_assessment']['recovery_status']}",
        f"  自律神经: {result['health_assessment']['autonomic_balance']}"
    ])
    
    if result['health_assessment']['hrv_age']:
        lines.append(f"  心脏年龄: {result['health_assessment']['hrv_age']} 岁")
    
    lines.append("")
    
    if result['arrhythmia']['has_arrhythmia']:
        lines.extend([
            "【⚠ 心律异常检测】",
            f"  检测到异常: 异位搏动 {result['arrhythmia']['ectopic_beats']} 次, "
            f"漏搏 {result['arrhythmia']['missed_beats']} 次",
            f"  不规则指数: {result['arrhythmia']['irregularity_score']:.2%}",
            ""
        ])
    
    lines.extend([
        "【建议】",
        *result['health_assessment']['recommendations']
    ])
    
    return "\n".join(lines)


# ============================================================================
# 便捷函数
# ============================================================================

def calculate_stress_index(rr_intervals: List[float]) -> float:
    """
    快速计算压力指数 (0-100)
    
    Args:
        rr_intervals: RR 间期列表 (ms)
    
    Returns:
        压力指数 (0-100, 越高表示压力越大)
    """
    time_metrics = calculate_time_domain_metrics(rr_intervals)
    health = assess_health_status(time_metrics)
    return health.stress_index


def calculate_recovery_score(rr_intervals: List[float]) -> float:
    """
    快速计算恢复分数 (0-100)
    
    Args:
        rr_intervals: RR 间期列表 (ms)
    
    Returns:
        恢复分数 (0-100, 越高表示恢复越好)
    """
    time_metrics = calculate_time_domain_metrics(rr_intervals)
    
    # 基于 RMSSD 和 SDNN 计算恢复分数
    rmssd_score = min(100, time_metrics.rmssd * 1.2)
    sdnn_score = min(100, time_metrics.sdnn)
    
    return round((rmssd_score * 0.6 + sdnn_score * 0.4), 1)


def check_readiness(rr_intervals: List[float]) -> Dict[str, Any]:
    """
    快速检查训练准备状态
    
    Args:
        rr_intervals: RR 间期列表 (ms)
    
    Returns:
        准备状态评估结果
    
    Example:
        >>> rr = [800, 810, 795, 820, 815, 805, 825, 810]
        >>> status = check_readiness(rr)
        >>> 'ready' in status
        True
    """
    time_metrics = calculate_time_domain_metrics(rr_intervals)
    
    # 基准值 (使用之前测量或群体平均值)
    # 这里使用简化方法
    
    # RMSSD 变化评估
    rmssd = time_metrics.rmssd
    
    if rmssd > 80:
        readiness = '高'
        score = 90
        color = 'green'
    elif rmssd > 50:
        readiness = '中等'
        score = 70
        color = 'yellow'
    elif rmssd > 30:
        readiness = '较低'
        score = 50
        color = 'orange'
    else:
        readiness = '低'
        score = 30
        color = 'red'
    
    # 检查心律异常
    arrhythmia = detect_arrhythmias(rr_intervals)
    
    if arrhythmia.has_arrhythmia:
        score = max(20, score - 20)
        readiness = '需要休息'
        color = 'red'
    
    return {
        'ready': score >= 50,
        'readiness_score': score,
        'readiness_level': readiness,
        'color': color,
        'rmssd': round(rmssd, 2),
        'sdnn': round(time_metrics.sdnn, 2),
        'warning': '检测到心律异常，建议休息' if arrhythmia.has_arrhythmia else None
    }