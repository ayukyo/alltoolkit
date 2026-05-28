#!/usr/bin/env python3
"""
Frame Rate Utils 使用示例

演示帧率计算工具的各种用法
"""

from fractions import Fraction
import sys
import os

# 确保能找到模块
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
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
    is_drop_frame_rate,
    calculate_drop_frame_count,
)


def print_section(title):
    """打印分隔线"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def example_basic_frame_rate():
    """示例：基本帧率操作"""
    print_section("基本帧率操作")
    
    # 创建帧率对象
    fps_30 = FrameRate(30)
    fps_24 = FrameRate(24)
    fps_2997 = FrameRate(Fraction(30000, 1001))  # 29.97fps (NTSC)
    
    print(f"帧率 30fps: {fps_30}")
    print(f"帧率 24fps: {fps_24}")
    print(f"帧率 29.97fps: {fps_2997}")
    
    # 帧率属性
    print(f"\n30fps 详细信息:")
    print(f"  - 浮点值: {fps_30.float_value}")
    print(f"  - 分数形式: {fps_30.fps}")
    print(f"  - 分子: {fps_30.numerator}")
    print(f"  - 分母: {fps_30.denominator}")
    print(f"  - 每帧时长: {fps_30.frame_duration} 秒")
    print(f"  - 每帧时长: {fps_30.frame_duration_ms:.4f} 毫秒")


def example_frames_time_conversion():
    """示例：帧数与时间转换"""
    print_section("帧数与时间转换")
    
    fps = FrameRate(30)
    
    # 帧数转秒数
    frames = 90
    seconds = fps.frames_to_seconds(frames)
    print(f"{frames} 帧 = {seconds} 秒 (30fps)")
    
    frames = 108000
    seconds = fps.frames_to_seconds(frames)
    print(f"{frames} 帧 = {seconds} 秒 = {seconds/3600} 小时 (30fps)")
    
    # 秒数转帧数
    seconds = 5.5
    frames = fps.seconds_to_frames(seconds)
    print(f"\n{seconds} 秒 = {frames} 帧 (30fps)")
    
    # 不同舍入方式
    seconds = 1.7
    frames_round = fps.seconds_to_frames(seconds, 'round')
    frames_floor = fps.seconds_to_frames(seconds, 'floor')
    frames_ceil = fps.seconds_to_frames(seconds, 'ceil')
    print(f"{seconds} 秒转帧数:")
    print(f"  - round: {frames_round}")
    print(f"  - floor: {frames_floor}")
    print(f"  - ceil: {frames_ceil}")


def example_timecode_operations():
    """示例：时间码操作"""
    print_section("时间码操作")
    
    # 从帧数创建时间码
    tc1 = Timecode.from_frames(90, 30)
    print(f"90 帧 (30fps): {tc1}")
    
    tc2 = Timecode.from_frames(108000, 30)  # 1 小时
    print(f"108000 帧 (30fps): {tc2}")
    
    # 从秒数创建时间码
    tc3 = Timecode.from_seconds(90.5, 30)
    print(f"90.5 秒 (30fps): {tc3}")
    
    # 从字符串解析时间码
    tc4 = Timecode.from_string("01:23:45:12", 30)
    print(f"解析 '01:23:45:12': {tc4}")
    print(f"  - 总帧数: {tc4.total_frames}")
    print(f"  - 总秒数: {tc4.total_seconds}")
    
    # 时间码运算
    tc_a = Timecode.from_string("00:00:30:00", 30)
    tc_b = Timecode.from_string("00:00:45:00", 30)
    tc_sum = tc_a + tc_b
    tc_diff = tc_b - tc_a
    print(f"\n时间码运算:")
    print(f"  {tc_a} + {tc_b} = {tc_sum}")
    print(f"  {tc_b} - {tc_a} = {tc_diff}")
    
    # 时间码比较
    print(f"\n时间码比较:")
    print(f"  {tc_a} < {tc_b}: {tc_a < tc_b}")
    print(f"  {tc_a} == {tc_a}: {tc_a == tc_a}")


def example_drop_frame():
    """示例：Drop-Frame 时间码"""
    print_section("Drop-Frame 时间码 (NTSC)")
    
    # Drop-frame 是 NTSC 视频的标准
    fps_df = FrameRate(FRAME_RATE_PRESETS['ntsc_df'], is_drop_frame=True)
    print(f"NTSC Drop-Frame: {fps_df}")
    
    # 判断是否为 drop-frame 帧率
    print(f"\n29.97fps 是 drop-frame 帧率: {is_drop_frame_rate(fps_df.fps)}")
    print(f"30fps 是 drop-frame 帧率: {is_drop_frame_rate(30)}")
    
    # Drop-frame 时间码使用分号分隔
    tc_df = Timecode.from_frames(108000, fps_df, is_drop_frame=True)
    print(f"\n108000 帧的 drop-frame 时间码: {tc_df}")
    
    # 比较 drop-frame 和 non-drop-frame
    fps_ndf = FrameRate(30, is_drop_frame=False)
    tc_ndf = Timecode.from_frames(108000, fps_ndf, is_drop_frame=False)
    print(f"108000 帧的 non-drop-frame 时间码: {tc_ndf}")
    
    # 计算丢帧数
    drop_count = calculate_drop_frame_count(108000)
    print(f"\n108000 帧的 drop-frame 丢帧数: {drop_count}")


def example_frame_rate_conversion():
    """示例：帧率转换"""
    print_section("帧率转换")
    
    # 24fps 电影转 30fps 视频
    frames_24 = 24  # 1 秒
    frames_30 = convert_frame_rate(frames_24, 24, 30)
    print(f"24fps 的 {frames_24} 帧 → 30fps 的 {frames_30} 帧")
    
    # 24fps 转换到 25fps (PAL)
    frames_24 = 240  # 10 秒
    frames_25 = convert_frame_rate(frames_24, 24, 25)
    print(f"24fps 的 {frames_24} 帧 → 25fps 的 {frames_25} 帧")
    
    # 分数帧率转换
    frames_23976 = 24
    frames_2997 = convert_frame_rate(
        frames_23976,
        Fraction(24000, 1001),  # 23.976fps
        Fraction(30000, 1001)   # 29.97fps
    )
    print(f"23.976fps 的 {frames_23976} 帧 → 29.97fps 的 {frames_2997} 帧")
    
    # 计算下拉参数
    pulldown = FrameConverter.calculate_pull_down()
    print(f"\n3:2 Pulldown 参数:")
    print(f"  - 源帧率: {pulldown['source_fps']} fps")
    print(f"  - 目标帧率: {pulldown['target_fps']:.2f} fps")
    print(f"  - 比例: {pulldown['ratio']:.2f}")
    print(f"  - 是 3:2 pulldown: {pulldown['is_32_pulldown']}")


def example_convenience_functions():
    """示例：便捷函数"""
    print_section("便捷函数")
    
    # 帧数转秒数
    seconds = frames_to_seconds(1500, 30)
    print(f"1500 帧 → {seconds} 秒 (30fps)")
    
    # 秒数转帧数
    frames = seconds_to_frames(50.5, 30)
    print(f"50.5 秒 → {frames} 帧 (30fps)")
    
    # 帧数转时间码
    tc = frames_to_timecode(5400, 30)  # 3 分钟
    print(f"5400 帧 → {tc} (30fps)")
    
    # 时间码转帧数
    frames = timecode_to_frames("00:03:00:00", 30)
    print(f"00:03:00:00 → {frames} 帧 (30fps)")
    
    # 时间码转秒数
    seconds = timecode_to_seconds("00:05:30:00", 30)
    print(f"00:05:30:00 → {seconds} 秒 (30fps)")
    
    # 秒数转时间码
    tc = seconds_to_timecode(330, 30)  # 5 分 30 秒
    print(f"330 秒 → {tc} (30fps)")


def example_frame_rate_presets():
    """示例：帧率预设"""
    print_section("帧率预设")
    
    print("常用帧率预设:")
    for name, fps in FRAME_RATE_PRESETS.items():
        fps_obj = FrameRate(fps)
        print(f"  {name:12s}: {fps_obj.float_value:8.4f} fps ({fps})")
    
    print("\n使用预设:")
    film_fps = FrameRate(FRAME_RATE_PRESETS['film'])
    print(f"电影帧率: {film_fps}")
    
    pal_fps = FrameRate(FRAME_RATE_PRESETS['pal'])
    print(f"PAL 帧率: {pal_fps}")
    
    ntsc_df = FrameRate(FRAME_RATE_PRESETS['ntsc_df'], is_drop_frame=True)
    print(f"NTSC Drop-Frame: {ntsc_df}")


def example_practical_use_cases():
    """示例：实际应用场景"""
    print_section("实际应用场景")
    
    # 场景1：计算视频总帧数
    print("场景1: 计算 10 分钟 30fps 视频的总帧数")
    duration_minutes = 10
    fps = 30
    total_frames = seconds_to_frames(duration_minutes * 60, fps)
    total_timecode = frames_to_timecode(total_frames, fps)
    print(f"  总帧数: {total_frames}")
    print(f"  时间码: {total_timecode}")
    
    # 场景2：计算时间差
    print("\n场景2: 计算两个时间点之间的帧数")
    start_tc = Timecode.from_string("00:01:30:00", 30)
    end_tc = Timecode.from_string("00:05:45:15", 30)
    duration = end_tc - start_tc
    print(f"  开始: {start_tc}")
    print(f"  结束: {end_tc}")
    print(f"  时长: {duration} ({duration.total_frames} 帧)")
    print(f"  秒数: {duration.total_seconds}")
    
    # 场景3：计算每帧时长
    print("\n场景3: 计算不同帧率的每帧时长")
    for fps_name, fps_value in [('film', 24), ('pal', 25), ('ntsc', 30), ('hfr', 60)]:
        fps = FrameRate(fps_value)
        print(f"  {fps_name}: 每帧 {fps.frame_duration_ms:.4f} ms")
    
    # 场景4：计算需要多少帧
    print("\n场景4: 计算特定时长需要的帧数")
    needed_duration = 2.5  # 秒
    for fps in [24, 25, 30, 50, 60]:
        frames = seconds_to_frames(needed_duration, fps)
        print(f"  {fps}fps: {frames} 帧")


def example_high_frame_rate():
    """示例：高帧率"""
    print_section("高帧率 (HFR)")
    
    # 48fps, 60fps, 120fps, 240fps
    hfr_fps_list = [
        ('48fps (HFR)', 48),
        ('60fps', 60),
        ('120fps (HFR)', 120),
        ('240fps (HFR)', 240),
    ]
    
    for name, fps_value in hfr_fps_list:
        fps = FrameRate(fps_value)
        tc_1min = Timecode.from_seconds(60, fps)
        tc_1hour = Timecode.from_seconds(3600, fps)
        
        print(f"\n{name}:")
        print(f"  每帧时长: {fps.frame_duration_ms:.4f} ms")
        print(f"  1 分钟帧数: {fps.seconds_to_frames(60)}")
        print(f"  1 小时帧数: {fps.seconds_to_frames(3600)}")
        print(f"  1 分钟时间码: {tc_1min}")
        print(f"  1 小时时间码: {tc_1hour}")


def main():
    """运行所有示例"""
    print("\n" + "=" * 60)
    print("  Frame Rate Utils 使用示例")
    print("=" * 60)
    
    example_basic_frame_rate()
    example_frames_time_conversion()
    example_timecode_operations()
    example_drop_frame()
    example_frame_rate_conversion()
    example_convenience_functions()
    example_frame_rate_presets()
    example_practical_use_cases()
    example_high_frame_rate()
    
    print("\n" + "=" * 60)
    print("  示例完成")
    print("=" * 60 + "\n")


if __name__ == '__main__':
    main()