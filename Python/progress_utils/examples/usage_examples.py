"""
进度追踪工具使用示例
"""

import time
import sys
sys.path.insert(0, '..')

from progress_utils.mod import (
    ProgressBar,
    ProgressTracker,
    Spinner,
    ETAEstimator,
    progress_bar,
    track,
    format_duration,
    format_rate,
)


def example_basic_progress_bar():
    """基本进度条示例"""
    print("\n=== 基本进度条示例 ===\n")
    
    # 创建进度条
    bar = progress_bar(total=50, prefix='处理:', style='modern')
    
    # 模拟任务
    for i in range(50):
        time.sleep(0.02)
        bar.update()
    
    print("完成！")


def example_multiple_styles():
    """多种进度条样式示例"""
    print("\n=== 多种进度条样式 ===\n")
    
    styles = ['classic', 'modern', 'dots', 'arrows', 'blocks', 'minimal', 'fancy']
    
    for style in styles:
        print(f"\n样式: {style}")
        bar = ProgressBar(
            total=30,
            style=style,
            width=30,
            show_eta=False,
            prefix=f"[{style}] ",
        )
        
        for i in range(30):
            time.sleep(0.01)
            bar.update()


def example_track_iterator():
    """跟踪迭代器示例"""
    print("\n=== 跟踪迭代器示例 ===\n")
    
    # 处理列表
    items = ['apple', 'banana', 'cherry', 'date', 'elderberry', 'fig', 'grape']
    
    print("处理水果列表:")
    for item in track(items, description='处理中:'):
        time.sleep(0.1)
        print(f"\n  -> 已处理: {item}")
    
    print("\n所有项目处理完成！")


def example_progress_tracker():
    """高级进度追踪器示例"""
    print("\n=== 高级进度追踪器示例 ===\n")
    
    def on_update(current, total, progress):
        """更新回调"""
        pass  # 可以在这里做自定义处理
    
    def on_complete():
        """完成回调"""
        print("\n🎉 任务完成！")
    
    tracker = ProgressTracker(
        total=100,
        description='数据处理任务',
        on_update=on_update,
        on_complete=on_complete,
    )
    
    with tracker:
        # 第一阶段
        for i in range(25):
            time.sleep(0.01)
            tracker.update()
        tracker.milestone('数据读取完成')
        
        # 第二阶段
        for i in range(50):
            time.sleep(0.01)
            tracker.update()
        tracker.milestone('数据处理完成')
        
        # 第三阶段
        for i in range(25):
            time.sleep(0.01)
            tracker.update()
        tracker.milestone('数据写入完成')
    
    # 显示统计
    stats = tracker.get_stats()
    print(f"\n任务统计:")
    print(f"  总耗时: {format_duration(stats['elapsed'])}")
    print(f"  处理速率: {format_rate(stats['rate'])}")
    print(f"  里程碑: {stats['milestones']} 个")
    
    # 显示里程碑
    print("\n里程碑记录:")
    for m in tracker.get_milestones():
        print(f"  - {m['name']}: {m['progress']}%, 耗时 {format_duration(m['elapsed_from_start'])}")


def example_spinner():
    """旋转动画示例"""
    print("\n=== 旋转动画示例 ===\n")
    
    styles = ['dots', 'line', 'circle', 'ascii']
    
    for style in styles:
        print(f"样式: {style}")
        with Spinner(f"加载中 ({style})...", style=style) as spinner:
            for i in range(20):
                time.sleep(0.05)
                spinner.update(f"加载中 ({style})... {i+1}/20")
        print(f"完成 ({style})\n")


def example_eta_estimator():
    """ETA 估算器示例"""
    print("\n=== ETA 估算器示例 ===\n")
    
    total = 100
    estimator = ETAEstimator(alpha=0.3)
    
    bar = ProgressBar(
        total=total,
        prefix='处理:',
        style='modern',
        show_eta=False,  # 我们用自己的 ETA
    )
    
    for i in range(1, total + 1):
        # 模拟变化的工作速度
        time.sleep(0.01 + (i % 10) * 0.001)
        
        estimator.update(i)
        eta = estimator.estimate(total)
        rate = estimator.get_rate()
        
        bar.set_progress(i)
    
    print(f"\n最终速率: {format_rate(estimator.get_rate())}")


def example_nested_progress():
    """嵌套进度示例"""
    print("\n=== 嵌套进度示例 ===\n")
    
    outer_bar = ProgressBar(
        total=5,
        width=20,
        prefix='总任务:',
        style='modern',
    )
    
    for i in range(5):
        inner_bar = ProgressBar(
            total=10,
            width=15,
            prefix=f'  子任务 {i+1}:',
            style='dots',
            show_eta=False,
        )
        
        for j in range(10):
            time.sleep(0.03)
            inner_bar.update()
        
        outer_bar.update()


def example_multi_stage():
    """多阶段任务示例"""
    print("\n=== 多阶段任务示例 ===\n")
    
    total_stages = 3
    stage_progress = 0
    
    bar = ProgressBar(
        total=100,
        prefix='总进度:',
        style='blocks',
        suffix=f'(阶段 1/{total_stages})',
    )
    
    # 阶段 1: 数据读取 (0-30%)
    print("阶段 1: 数据读取")
    for i in range(30):
        time.sleep(0.02)
        bar.update()
    bar.suffix = f'(阶段 2/{total_stages})'
    
    # 阶段 2: 数据处理 (30-70%)
    print("阶段 2: 数据处理")
    for i in range(40):
        time.sleep(0.02)
        bar.update()
    bar.suffix = f'(阶段 3/{total_stages})'
    
    # 阶段 3: 数据写入 (70-100%)
    print("阶段 3: 数据写入")
    for i in range(30):
        time.sleep(0.02)
        bar.update()
    
    print("\n所有阶段完成！")


def example_rate_display():
    """速率显示示例"""
    print("\n=== 速率显示示例 ===\n")
    
    test_rates = [0.1, 0.5, 5, 50, 500, 5000, 50000, 500000]
    
    for rate in test_rates:
        print(f"速率 {rate:8.1f} 项/秒 -> {format_rate(rate)}")
    
    print("\n自定义单位:")
    for rate in [10, 100, 1000]:
        print(f"  {format_rate(rate, '条记录')}")


def example_duration_format():
    """持续时间格式化示例"""
    print("\n=== 持续时间格式化示例 ===\n")
    
    durations = [
        0.001,    # 1 毫秒
        0.5,      # 0.5 秒
        5,        # 5 秒
        30,       # 30 秒
        90,       # 1.5 分钟
        3600,     # 1 小时
        7325,     # 2 小时 2 分 5 秒
        86400,    # 1 天
        172800,   # 2 天
        31536000, # 1 年
    ]
    
    for d in durations:
        print(f"{d:10.0f} 秒 -> {format_duration(d)}")


def example_context_managers():
    """上下文管理器示例"""
    print("\n=== 上下文管理器示例 ===\n")
    
    # ProgressBar 作为上下文管理器
    print("使用 ProgressBar 上下文管理器:")
    with ProgressBar(total=20, prefix='处理:') as bar:
        for i in range(20):
            time.sleep(0.02)
            bar.update()
    
    print("\n使用 ProgressTracker 上下文管理器:")
    with ProgressTracker(total=50, description='追踪任务') as tracker:
        for i in range(50):
            time.sleep(0.01)
            tracker.update()
        print(f"  -> 完成，耗时: {format_duration(tracker.elapsed)}")
    
    print("\n使用 Spinner 上下文管理器:")
    with Spinner('加载配置...') as spinner:
        time.sleep(0.5)
        spinner.update('读取数据库...')
        time.sleep(0.5)
        spinner.update('初始化模块...')
        time.sleep(0.5)


def example_real_world():
    """真实场景示例"""
    print("\n=== 真实场景示例：文件处理模拟 ===\n")
    
    # 模拟处理多个文件
    files = ['doc1.txt', 'doc2.txt', 'report.pdf', 'data.csv', 'config.json']
    
    print("开始处理文件...\n")
    
    # 使用 track 自动跟踪
    processed = []
    for filename in track(files, description='处理文件:'):
        time.sleep(0.2)  # 模拟处理时间
        processed.append(filename)
        print(f"\n  ✓ 已完成: {filename}")
    
    print(f"\n所有 {len(processed)} 个文件处理完成！")
    
    # 使用 ProgressTracker 获取详细统计
    print("\n--- 详细处理报告 ---")
    
    with ProgressTracker(total=len(files), description='批量处理') as tracker:
        for f in files:
            time.sleep(0.1)
            tracker.update()
            tracker.milestone(f'已处理: {f}')
    
    stats = tracker.get_stats()
    print(f"总耗时: {format_duration(stats['elapsed'])}")
    print(f"平均速率: {format_rate(stats['rate'], '文件')}")


if __name__ == '__main__':
    print("=" * 50)
    print("进度追踪工具示例")
    print("=" * 50)
    
    example_basic_progress_bar()
    example_multiple_styles()
    example_track_iterator()
    example_progress_tracker()
    example_spinner()
    example_eta_estimator()
    example_nested_progress()
    example_multi_stage()
    example_rate_display()
    example_duration_format()
    example_context_managers()
    example_real_world()
    
    print("\n" + "=" * 50)
    print("所有示例完成！")
    print("=" * 50)