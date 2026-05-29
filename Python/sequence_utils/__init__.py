"""
Sequence Utilities - 序列分析工具模块

提供全面的序列分析和处理功能。
"""

from .mod import (
    # 异常类
    SequenceError,
    EmptySequenceError,
    InvalidSequenceError,
    
    # 统计分析
    mean,
    median,
    mode,
    variance,
    std_dev,
    skewness,
    kurtosis,
    quantile,
    quartiles,
    iqr,
    range_value,
    coefficient_of_variation,
    descriptive_stats,
    
    # 序列变换
    normalize,
    standardize,
    differentiate,
    cumulative_sum,
    cumulative_product,
    exponential_smoothing,
    moving_average,
    log_transform,
    power_transform,
    box_cox_transform,
    
    # 序列生成器
    arange,
    linspace,
    logspace,
    geometric_sequence,
    fibonacci,
    tribonacci,
    lucas_numbers,
    prime_numbers,
    triangular_numbers,
    square_numbers,
    cube_numbers,
    factorial_sequence,
    
    # 滑动窗口操作
    sliding_window,
    rolling_max,
    rolling_min,
    rolling_sum,
    rolling_std,
    
    # 插值与填充
    linear_interpolate,
    fill_missing,
    
    # 重采样
    downsample,
    upsample,
    
    # 序列操作
    reverse,
    shuffle,
    sample,
    split,
    chunk,
    flatten,
    unique,
    difference,
    intersection,
    union,
    
    # 异常值检测
    zscore_outliers,
    iqr_outliers,
    remove_outliers,
    
    # 趋势与周期检测
    is_monotonic,
    is_increasing,
    is_decreasing,
    trend_direction,
    find_peaks,
    find_valleys,
    detect_seasonality,
    
    # 自相关与滞后
    autocorrelation,
    autocorrelation_function,
    lag,
    lead,
    
    # 序列相似度
    euclidean_distance,
    manhattan_distance,
    cosine_similarity,
    pearson_correlation,
    spearman_correlation,
    dtw_distance,
    
    # 实用工具
    apply,
    filter_seq,
    reduce_seq,
    compose,
    
    # 常量
    GOLDEN_RATIO,
    EULER_NUMBER,
    PI,
    golden_sequence,
)

__all__ = [
    # 异常类
    'SequenceError',
    'EmptySequenceError',
    'InvalidSequenceError',
    
    # 统计分析
    'mean',
    'median',
    'mode',
    'variance',
    'std_dev',
    'skewness',
    'kurtosis',
    'quantile',
    'quartiles',
    'iqr',
    'range_value',
    'coefficient_of_variation',
    'descriptive_stats',
    
    # 序列变换
    'normalize',
    'standardize',
    'differentiate',
    'cumulative_sum',
    'cumulative_product',
    'exponential_smoothing',
    'moving_average',
    'log_transform',
    'power_transform',
    'box_cox_transform',
    
    # 序列生成器
    'arange',
    'linspace',
    'logspace',
    'geometric_sequence',
    'fibonacci',
    'tribonacci',
    'lucas_numbers',
    'prime_numbers',
    'triangular_numbers',
    'square_numbers',
    'cube_numbers',
    'factorial_sequence',
    
    # 滑动窗口操作
    'sliding_window',
    'rolling_max',
    'rolling_min',
    'rolling_sum',
    'rolling_std',
    
    # 插值与填充
    'linear_interpolate',
    'fill_missing',
    
    # 重采样
    'downsample',
    'upsample',
    
    # 序列操作
    'reverse',
    'shuffle',
    'sample',
    'split',
    'chunk',
    'flatten',
    'unique',
    'difference',
    'intersection',
    'union',
    
    # 异常值检测
    'zscore_outliers',
    'iqr_outliers',
    'remove_outliers',
    
    # 趋势与周期检测
    'is_monotonic',
    'is_increasing',
    'is_decreasing',
    'trend_direction',
    'find_peaks',
    'find_valleys',
    'detect_seasonality',
    
    # 自相关与滞后
    'autocorrelation',
    'autocorrelation_function',
    'lag',
    'lead',
    
    # 序列相似度
    'euclidean_distance',
    'manhattan_distance',
    'cosine_similarity',
    'pearson_correlation',
    'spearman_correlation',
    'dtw_distance',
    
    # 实用工具
    'apply',
    'filter_seq',
    'reduce_seq',
    'compose',
    
    # 常量
    'GOLDEN_RATIO',
    'EULER_NUMBER',
    'PI',
    'golden_sequence',
]

__version__ = '1.0.0'