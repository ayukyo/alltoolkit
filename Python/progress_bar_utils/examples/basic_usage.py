"""
进度条基础用法示例

展示 ProgressBar 的基本功能和使用方式。
"""

import time
from mod import (
    ProgressBar,
    ProgressBarStyle,
    progress,
    create_progress_bar,
    SpinnerProgress
)


def basic_progress():
    """基础进度条使用"""
    print("\n=== 基础进度条 ===")
    
    # 创建进度条
    pb = ProgressBar(100, "下载文件")
    
    # 更新进度
    for i in range(100):
        pb.update()
        time.sleep(0.02)
    
    # 关闭进度条
    pb.close()
    print("下载完成！")


def context_manager():
    """使用上下文管理器"""
    print("\n=== 上下文管理器 ===")
    
    # 自动管理生命周期
    with ProgressBar(50, "处理数据") as pb:
        for i in range(50):
            pb.update()
            time.sleep(0.03)
    # 自动关闭


def progress_helper():
    """使用 progress 便捷函数"""
    print("\n=== progress 便捷函数 ===")
    
    with progress(80, "备份文件") as pb:
        for i in range(80):
            pb.update()
            time.sleep(0.02)


def different_styles():
    """不同样式展示"""
    print("\n=== 不同样式 ===")
    
    styles = [
        ("经典样式", ProgressBarStyle.classic()),
        ("现代样式", ProgressBarStyle.modern()),
        ("简约样式", ProgressBarStyle.minimal()),
        ("方块样式", ProgressBarStyle.blocks()),
        ("箭头样式", ProgressBarStyle.arrows()),
    ]
    
    for name, style in styles:
        print(f"\n{name}:")
        pb = ProgressBar(30, name, style=style)
        for i in range(30):
            pb.update()
            time.sleep(0.05)
        pb.close()


def create_by_name():
    """通过名称创建进度条"""
    print("\n=== 通过名称创建 ===")
    
    style_names = ["classic", "modern", "minimal", "blocks", "arrows"]
    
    for style_name in style_names:
        pb = create_progress_bar(20, f"{style_name}样式", style_name)
        for i in range(20):
            pb.update()
            time.sleep(0.04)
        pb.close()


def spinner_example():
    """旋转加载动画"""
    print("\n=== 旋转加载动画 ===")
    
    # 使用 Unicode 字符
    with SpinnerProgress("加载数据", use_unicode=True):
        time.sleep(2)
    
    # 使用 ASCII 字符
    with SpinnerProgress("处理请求", use_unicode=False):
        time.sleep(1.5)
    
    # 自定义完成消息
    sp = SpinnerProgress("验证文件", use_unicode=True)
    sp.start()
    time.sleep(1)
    sp.stop("✓ 验证成功！")


def batch_processing():
    """批量处理示例"""
    print("\n=== 批量处理 ===")
    
    items = list(range(100))
    
    with ProgressBar(len(items), "批量处理") as pb:
        for item in items:
            # 处理每个项目
            time.sleep(0.01)
            pb.update()


def eta_and_rate():
    """预估时间和速率显示"""
    print("\n=== ETA 和速率 ===")
    
    pb = ProgressBar(200, "传输数据")
    
    for i in range(200):
        pb.update()
        time.sleep(0.015)
        
        # 每 50 步显示详细信息
        if i % 50 == 0 and pb.eta is not None:
            # 这些信息已经显示在进度条中
            pass
    
    pb.close()
    
    print(f"总用时: {pb.elapsed:.2f} 秒")
    print(f"平均速率: {pb.rate:.2f} 项/秒")


def reset_example():
    """重置进度条"""
    print("\n=== 重置进度条 ===")
    
    pb = ProgressBar(100, "第一阶段")
    
    # 第一阶段
    for i in range(100):
        pb.update()
        time.sleep(0.01)
    
    print("第一阶段完成！")
    
    # 重置为第二阶段
    pb.reset(total=50, desc="第二阶段")
    
    for i in range(50):
        pb.update()
        time.sleep(0.02)
    
    pb.close()
    print("第二阶段完成！")


def multiple_updates():
    """批量更新"""
    print("\n=== 批量更新 ===")
    
    pb = ProgressBar(100, "快速处理")
    
    # 每次更新多个
    for i in range(10):
        pb.update(10)  # 每次增加 10
        time.sleep(0.1)
    
    pb.close()


def set_current_example():
    """直接设置进度"""
    print("\n=== 直接设置进度 ===")
    
    pb = ProgressBar(100, "跳跃进度")
    
    pb.set_current(25)
    time.sleep(0.5)
    
    pb.set_current(50)
    time.sleep(0.5)
    
    pb.set_current(75)
    time.sleep(0.5)
    
    pb.set_current(100)
    time.sleep(0.1)
    
    pb.close()


if __name__ == "__main__":
    print("进度条工具集 - 基础用法示例")
    print("=" * 50)
    
    basic_progress()
    context_manager()
    progress_helper()
    different_styles()
    create_by_name()
    spinner_example()
    batch_processing()
    eta_and_rate()
    reset_example()
    multiple_updates()
    set_current_example()
    
    print("\n所有示例运行完成！")