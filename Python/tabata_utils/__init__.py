"""
Tabata Utilities - Tabata 高强度间歇训练工具

提供完整的 Tabata 训练支持，零外部依赖。

主要组件：
- TabataTimer: 训练计时器
- TabataPresets: 预设训练方案
- TabataBuilder: 自定义训练构建器
- TabataCalculator: 训练计算工具
- TabataFormatter: 格式化输出工具
"""

from .mod import (
    # 类型
    PhaseType,
    TabataRound,
    TabataSession,
    SessionStats,
    
    # 核心类
    TabataTimer,
    TabataPresets,
    TabataBuilder,
    TabataFormatter,
    TabataCalculator,
    
    # 便捷函数
    create_tabata,
    get_preset,
    list_presets,
)

__all__ = [
    'PhaseType',
    'TabataRound',
    'TabataSession',
    'SessionStats',
    'TabataTimer',
    'TabataPresets',
    'TabataBuilder',
    'TabataFormatter',
    'TabataCalculator',
    'create_tabata',
    'get_preset',
    'list_presets',
]

__version__ = '1.0.0'
__author__ = 'AllToolkit'