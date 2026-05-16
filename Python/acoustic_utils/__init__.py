"""
Acoustic Utilities - 声学计算工具模块

提供全面的声学和声音计算功能，零外部依赖。

功能:
- 分贝计算 (功率、强度、压力)
- 声级转换
- 频率加权滤波 (A, B, C, D 权重)
- 房间声学 (RT60, 房间模式)
- 声音传播 (距离衰减)
- 多普勒效应计算
- 波长和频率转换
- 响度转换 (phon, sone)
- 噪声准则计算
- 噪声剂量和暴露评估
"""

from .mod import (
    # Constants
    SPEED_OF_SOUND_20C,
    REFERENCE_SOUND_PRESSURE,
    REFERENCE_SOUND_INTENSITY,
    REFERENCE_SOUND_POWER,
    REFERENCE_DISTANCE,
    
    # Enums
    FrequencyWeighting,
    RoomType,
    
    # Data Classes
    SoundLevel,
    RoomAcoustics,
    
    # Core Decibel Functions
    db_from_power,
    db_from_intensity,
    db_from_pressure,
    power_from_db,
    intensity_from_db,
    pressure_from_db,
    
    # Sound Level Operations
    add_decibels,
    subtract_decibels,
    average_decibels,
    decibel_difference,
    
    # Distance Attenuation
    distance_attenuation,
    sound_level_at_distance,
    distance_from_sound_level,
    
    # Wavelength and Frequency
    wavelength,
    frequency_from_wavelength,
    speed_of_sound,
    
    # Doppler Effect
    doppler_frequency,
    doppler_shift,
    
    # Frequency Weighting
    a_weighting,
    c_weighting,
    apply_weighting,
    
    # Loudness Conversions
    phon_to_sone,
    sone_to_phon,
    db_to_phon,
    
    # Room Acoustics
    sabine_rt60,
    eyring_rt60,
    room_modes,
    critical_distance,
    recommended_rt60,
    
    # Noise Criteria
    noise_criteria,
    
    # Sound Exposure and Dose
    sound_exposure_level,
    equivalent_continuous_level,
    noise_dose,
    time_weighted_average,
    
    # Utility Functions
    db_to_linear,
    linear_to_db,
    db_gain,
    amplitude_ratio_db,
    sound_power_level,
    sound_intensity_level,
    hearing_threshold_shift,
    
    # Main Class
    AcousticUtils,
    
    # Convenience Functions
    calculate_rt60,
    sound_level_summary,
)

__all__ = [
    # Constants
    'SPEED_OF_SOUND_20C',
    'REFERENCE_SOUND_PRESSURE',
    'REFERENCE_SOUND_INTENSITY',
    'REFERENCE_SOUND_POWER',
    'REFERENCE_DISTANCE',
    
    # Enums
    'FrequencyWeighting',
    'RoomType',
    
    # Data Classes
    'SoundLevel',
    'RoomAcoustics',
    
    # Core Decibel Functions
    'db_from_power',
    'db_from_intensity',
    'db_from_pressure',
    'power_from_db',
    'intensity_from_db',
    'pressure_from_db',
    
    # Sound Level Operations
    'add_decibels',
    'subtract_decibels',
    'average_decibels',
    'decibel_difference',
    
    # Distance Attenuation
    'distance_attenuation',
    'sound_level_at_distance',
    'distance_from_sound_level',
    
    # Wavelength and Frequency
    'wavelength',
    'frequency_from_wavelength',
    'speed_of_sound',
    
    # Doppler Effect
    'doppler_frequency',
    'doppler_shift',
    
    # Frequency Weighting
    'a_weighting',
    'c_weighting',
    'apply_weighting',
    
    # Loudness Conversions
    'phon_to_sone',
    'sone_to_phon',
    'db_to_phon',
    
    # Room Acoustics
    'sabine_rt60',
    'eyring_rt60',
    'room_modes',
    'critical_distance',
    'recommended_rt60',
    
    # Noise Criteria
    'noise_criteria',
    
    # Sound Exposure and Dose
    'sound_exposure_level',
    'equivalent_continuous_level',
    'noise_dose',
    'time_weighted_average',
    
    # Utility Functions
    'db_to_linear',
    'linear_to_db',
    'db_gain',
    'amplitude_ratio_db',
    'sound_power_level',
    'sound_intensity_level',
    'hearing_threshold_shift',
    
    # Main Class
    'AcousticUtils',
    
    # Convenience Functions
    'calculate_rt60',
    'sound_level_summary',
]