#!/usr/bin/env python3
"""
基本使用示例
演示 Spinner 的基本用法
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import time
from mod import Spinner, spinner, spin


def example_basic():
    """基本使用"""
    print("基本使用示例:")
    print("-" * 40)
    
    # 使用上下文管理器
    with Spinner("加载中..."):
        time.sleep(2)
    
    print("完成！\n")


def example_manual():
    """手动控制"""
    print("手动控制示例:")
    print("-" * 40)
    
    s = Spinner("处理数据...")
    s.start()
    time.sleep(2)
    s.stop(success=True)
    
    print()


def example_different_styles():
    """不同样式"""
    print("不同动画样式示例:")
    print("-" * 40)
    
    styles = ['dots', 'arrow', 'line', 'pulse', 'moon', 'hearts']
    
    for style in styles:
        with Spinner(f"使用 {style} 样式", style=style):
            time.sleep(1)
        print()  # 换行


def example_with_color():
    """颜色支持"""
    print("颜色支持示例:")
    print("-" * 40)
    
    colors = ['red', 'green', 'yellow', 'blue', 'magenta', 'cyan']
    
    for color in colors:
        with Spinner(f"{color} 颜色", color=color):
            time.sleep(0.8)
        print()


def example_with_elapsed_time():
    """显示已用时间"""
    print("显示已用时间示例:")
    print("-" * 40)
    
    with Spinner("计算中...", show_elapsed=True):
        time.sleep(3)
    
    print()


def example_with_progress():
    """显示进度"""
    print("显示进度示例:")
    print("-" * 40)
    
    s = Spinner("处理任务...", show_progress=True)
    s.start()
    
    for i in range(10):
        time.sleep(0.3)
        s.set_progress((i + 1) / 10)
    
    s.stop(success=True, message="处理完成！")
    print()


def example_update_message():
    """动态更新消息"""
    print("动态更新消息示例:")
    print("-" * 40)
    
    stages = [
        "初始化...",
        "加载配置...",
        "连接服务器...",
        "获取数据...",
        "处理数据...",
        "保存结果...",
    ]
    
    with Spinner("准备中...") as s:
        for stage in stages:
            s.update(stage)
            time.sleep(0.5)
    
    print()


def example_context_manager():
    """快捷上下文管理器"""
    print("快捷上下文管理器示例:")
    print("-" * 40)
    
    with spinner("下载文件...", style='earth', color='green'):
        time.sleep(2)
    
    print()


def example_decorator():
    """装饰器"""
    print("装饰器示例:")
    print("-" * 40)
    
    @spin("执行任务...", style='clock')
    def long_running_task():
        time.sleep(2)
        return "成功！"
    
    result = long_running_task()
    print(f"结果: {result}\n")


def example_custom_frames():
    """自定义动画帧"""
    print("自定义动画帧示例:")
    print("-" * 40)
    
    # 使用 emoji 作为动画帧
    frames = ['😺', '😸', '😹', '😻', '😼', '😽']
    
    with Spinner("喵喵加载中...", frames=frames):
        time.sleep(3)
    
    print()


def main():
    print("=" * 50)
    print("Terminal Spinner Utils - 基本使用示例")
    print("=" * 50)
    print()
    
    example_basic()
    example_manual()
    example_different_styles()
    example_with_color()
    example_with_elapsed_time()
    example_with_progress()
    example_update_message()
    example_context_manager()
    example_decorator()
    example_custom_frames()
    
    print("=" * 50)
    print("所有示例完成！")
    print("=" * 50)


if __name__ == "__main__":
    main()