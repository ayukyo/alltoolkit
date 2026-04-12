"""
Audio Utilities Module
音频处理工具函数库

Author: AllToolkit
Version: 1.0.0
"""

from .mod import (
    AudioInfo,
    AudioUtilsError,
    UnsupportedFormatError,
    InvalidAudioError,
    get_audio_info,
    read_audio,
    write_audio,
    adjust_volume,
    fade_in,
    fade_out,
    concatenate_audio,
    extract_segment,
    convert_to_mono,
    reverse_audio,
    generate_sine_wave,
    detect_silence,
    get_peak_amplitude,
    normalize_audio,
    create_tone,
    split_stereo,
)

__all__ = [
    'AudioInfo',
    'AudioUtilsError',
    'UnsupportedFormatError',
    'InvalidAudioError',
    'get_audio_info',
    'read_audio',
    'write_audio',
    'adjust_volume',
    'fade_in',
    'fade_out',
    'concatenate_audio',
    'extract_segment',
    'convert_to_mono',
    'reverse_audio',
    'generate_sine_wave',
    'detect_silence',
    'get_peak_amplitude',
    'normalize_audio',
    'create_tone',
    'split_stereo',
]

__version__ = '1.0.0'
