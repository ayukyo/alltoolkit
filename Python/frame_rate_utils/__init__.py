"""
Frame Rate Utils - 帧率计算工具
用于视频编辑、动画和游戏开发中的帧率相关计算

功能：
- 帧数 ↔ 时间转换
- 时间码生成和解析（HH:MM:SS:FF 格式）
- 帧率转换
- 下拉/上拉处理
- 常见帧率常量

零外部依赖，纯 Python 实现
"""

from .mod import (
    FrameRate,
    Timecode,
    FrameConverter,
    DropFrameCalculator,
    FRAME_RATE_PRESETS,
    frames_to_seconds,
    seconds_to_frames,
    frames_to_timecode,
    timecode_to_frames,
    timecode_to_seconds,
    seconds_to_timecode,
    convert_frame_rate,
    calculate_drop_frame_count,
    is_drop_frame_rate,
)

__all__ = [
    'FrameRate',
    'Timecode',
    'FrameConverter',
    'DropFrameCalculator',
    'FRAME_RATE_PRESETS',
    'frames_to_seconds',
    'seconds_to_frames',
    'frames_to_timecode',
    'timecode_to_frames',
    'timecode_to_seconds',
    'seconds_to_timecode',
    'convert_frame_rate',
    'calculate_drop_frame_count',
    'is_drop_frame_rate',
]

__version__ = '1.0.0'
__author__ = 'AllToolkit'