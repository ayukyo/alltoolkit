"""
进度条高级用法示例

展示 MultiProgressBar、迭代器工具、构建器等高级功能。
"""

import time
import threading
import random
from mod import (
    ProgressBar,
    ProgressBarStyle,
    MultiProgressBar,
    SpinnerProgress,
    ProgressBarBuilder,
    progress,
    progress_range,
    progress_iter,
    timed_progress
)


def multi_progress():
    """多任务并行进度条"""
    print("\n=== 多任务并行进度条 ===")
    
    mpb = MultiProgressBar()
    
    # 添加多个任务
    task1 = mpb.add_task("下载文件A", 100)
    task2 = mpb.add_task("下载文件B", 150)
    task3 = mpb.add_task("下载文件C", 80)
    
    # 模拟并行下载
    def download_task(task_id, total):
        for i in range(total):
            mpb.update(task_id)
            time.sleep(random.uniform(0.01, 0.03))
    
    threads = [
        threading.Thread(target=download_task, args=(task1, 100)),
        threading.Thread(target=download_task, args=(task2, 150)),
        threading.Thread(target=download_task, args=(task3, 80)),
    ]
    
    for t in threads:
        t.start()
    
    for t in threads:
        t.join()
    
    mpb.close()
    print("所有下载完成！")


def progress_range_example():
    """进度 range 迭代器"""
    print("\n=== progress_range 迭代器 ===")
    
    # 自动显示进度
    for i in progress_range(0, 100, desc="处理范围"):
        time.sleep(0.02)
    
    print("范围处理完成！")
    
    # 带步进的 range
    for i in progress_range(0, 100, step=5, desc="跳跃处理"):
        time.sleep(0.05)


def progress_iter_example():
    """进度迭代器"""
    print("\n=== progress_iter 迭代器 ===")
    
    # 迭代列表
    items = ["苹果", "香蕉", "橙子", "葡萄", "西瓜", "草莓", "蓝莓", "芒果"]
    
    for item in progress_iter(items, "处理水果"):
        print(f"\r处理: {item}")
        time.sleep(0.3)
    
    print("水果处理完成！")


def builder_example():
    """构建器链式调用"""
    print("\n=== 进度条构建器 ===")
    
    # 链式配置
    pb = (ProgressBarBuilder()
          .total(50)
          .desc("构建的任务")
          .style(ProgressBarStyle.minimal())
          .min_interval(0.01)
          .build())
    
    for i in range(50):
        pb.update()
        time.sleep(0.03)
    
    pb.close()


def timed_progress_example():
    """定时进度条"""
    print("\n=== 定时进度条 ===")
    
    # 在固定时间内完成进度
    timed_progress(3.0, "三秒任务", steps=30)
    
    print("定时任务完成！")


def concurrent_with_spinner():
    """并发任务与旋转动画"""
    print("\n=== 并发任务与旋转动画 ===")
    
    def background_task():
        time.sleep(3)
        return "数据加载完成"
    
    # 启动后台任务
    result = [None]
    thread = threading.Thread(target=lambda: result.__setitem__(0, background_task()))
    thread.start()
    
    # 显示旋转动画
    with SpinnerProgress("等待后台任务"):
        thread.join()
    
    print(f"结果: {result[0]}")


def file_processing():
    """文件处理示例"""
    print("\n=== 文件处理模拟 ===")
    
    # 模拟文件列表
    files = [
        "document1.txt",
        "document2.txt",
        "image1.png",
        "image2.jpg",
        "video1.mp4",
        "audio1.mp3",
        "archive1.zip",
        "config.ini",
    ]
    
    # 模拟不同大小的文件
    sizes = [random.randint(10, 100) for _ in files]
    
    with ProgressBar(len(files), "处理文件") as pb:
        for file, size in zip(files, sizes):
            time.sleep(size * 0.01)  # 模拟处理时间
            pb.update()
    
    print(f"处理了 {len(files)} 个文件")


def nested_progress():
    """嵌套进度条"""
    print("\n=== 嵌套进度条 ===")
    
    # 外层进度
    with ProgressBar(5, "批量任务") as outer_pb:
        for batch in range(5):
            # 内层进度
            with ProgressBar(20, f"批次 {batch + 1}") as inner_pb:
                for item in range(20):
                    time.sleep(0.01)
                    inner_pb.update()
            
            outer_pb.update()
    
    print("所有批次完成！")


def custom_style():
    """自定义样式"""
    print("\n=== 自定义样式 ===")
    
    # 创建自定义样式
    custom = ProgressBarStyle(
        filled='★',
        empty='☆',
        prefix='[进度] ',
        suffix=' 完成!',
        decimals=2,
        length=15,
        show_eta=True,
        show_rate=False,
        show_percent=True
    )
    
    pb = ProgressBar(100, "自定义任务", style=custom)
    
    for i in range(100):
        pb.update()
        time.sleep(0.02)
    
    pb.close()


def progress_with_error():
    """带错误处理的进度条"""
    print("\n=== 错误处理 ===")
    
    try:
        with ProgressBar(10, "可能失败的任务") as pb:
            for i in range(10):
                if i == 7:
                    raise ValueError("模拟错误！")
                pb.update()
                time.sleep(0.1)
    except ValueError as e:
        print(f"\n任务失败: {e}")
        print(f"已完成: {pb.current}/{pb.total}")


def rate_limited_update():
    """限制更新频率"""
    print("\n=== 限制更新频率 ===")
    
    # 设置最小更新间隔为 0.5 秒
    pb = ProgressBar(1000, "快速更新", min_update_interval=0.5)
    
    for i in range(1000):
        pb.update()
        time.sleep(0.001)  # 每次迭代很快
    
    # 但进度条只每隔 0.5 秒更新一次
    pb.close()
    print(f"总迭代: 1000, 实际刷新: ~{pb.elapsed / 0.5:.0f} 次")


def simulated_download():
    """模拟下载场景"""
    print("\n=== 模拟下载场景 ===")
    
    total_size = 1024 * 1024 * 10  # 10 MB
    
    with ProgressBar(100, "下载 10MB 文件") as pb:
        downloaded = 0
        
        while downloaded < total_size:
            # 模拟网络波动
            chunk = random.randint(50000, 200000)
            downloaded = min(downloaded + chunk, total_size)
            
            # 更新进度百分比
            progress_percent = int(downloaded / total_size * 100)
            pb.set_current(progress_percent)
            
            time.sleep(0.1)
    
    print("下载完成！")


if __name__ == "__main__":
    print("进度条工具集 - 高级用法示例")
    print("=" * 50)
    
    multi_progress()
    progress_range_example()
    progress_iter_example()
    builder_example()
    timed_progress_example()
    concurrent_with_spinner()
    file_processing()
    nested_progress()
    custom_style()
    progress_with_error()
    rate_limited_update()
    simulated_download()
    
    print("\n所有高级示例运行完成！")