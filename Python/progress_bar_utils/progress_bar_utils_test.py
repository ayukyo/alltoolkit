"""
Progress Bar Utils 测试套件

测试进度条的各项功能。
"""

import unittest
import time
import io
import threading
from mod import (
    ProgressBarStyle,
    ProgressBar,
    MultiProgressBar,
    SpinnerProgress,
    ProgressBarBuilder,
    progress,
    progress_range,
    progress_iter,
    create_progress_bar,
    timed_progress
)


class TestProgressBarStyle(unittest.TestCase):
    """ProgressBarStyle 测试"""
    
    def test_default_style(self):
        """测试默认样式"""
        style = ProgressBarStyle()
        self.assertEqual(style.filled, '█')
        self.assertEqual(style.empty, '░')
        self.assertEqual(style.length, 30)
        self.assertTrue(style.show_eta)
        self.assertTrue(style.show_rate)
    
    def test_classic_style(self):
        """测试经典样式"""
        style = ProgressBarStyle.classic()
        self.assertEqual(style.filled, '#')
        self.assertEqual(style.empty, '-')
        self.assertEqual(style.length, 40)
    
    def test_modern_style(self):
        """测试现代样式"""
        style = ProgressBarStyle.modern()
        self.assertEqual(style.filled, '█')
        self.assertEqual(style.empty, '░')
        self.assertEqual(style.length, 30)
    
    def test_minimal_style(self):
        """测试简约样式"""
        style = ProgressBarStyle.minimal()
        self.assertEqual(style.filled, '=')
        self.assertEqual(style.empty, ' ')
        self.assertEqual(style.length, 20)
        self.assertFalse(style.show_eta)
        self.assertFalse(style.show_rate)
    
    def test_blocks_style(self):
        """测试方块样式"""
        style = ProgressBarStyle.blocks()
        self.assertEqual(style.filled, '▓')
        self.assertEqual(style.empty, '░')
    
    def test_arrows_style(self):
        """测试箭头样式"""
        style = ProgressBarStyle.arrows()
        self.assertEqual(style.filled, '▶')
        self.assertEqual(style.empty, '▷')


class TestProgressBar(unittest.TestCase):
    """ProgressBar 测试"""
    
    def test_init(self):
        """测试初始化"""
        pb = ProgressBar(100, "测试")
        self.assertEqual(pb.total, 100)
        self.assertEqual(pb.current, 0)
        pb.close()
    
    def test_init_invalid_total(self):
        """测试无效总数"""
        with self.assertRaises(ValueError):
            ProgressBar(0)
        with self.assertRaises(ValueError):
            ProgressBar(-10)
    
    def test_update(self):
        """测试更新进度"""
        pb = ProgressBar(100)
        pb.update(10)
        self.assertEqual(pb.current, 10)
        pb.close()
    
    def test_update_multiple(self):
        """测试多次更新"""
        pb = ProgressBar(100)
        for i in range(10):
            pb.update(5)
        self.assertEqual(pb.current, 50)
        pb.close()
    
    def test_update_overflow(self):
        """测试更新溢出"""
        pb = ProgressBar(10)
        pb.update(20)  # 超过总数
        self.assertEqual(pb.current, 10)  # 最大为总数
        pb.close()
    
    def test_set_current(self):
        """测试直接设置进度"""
        pb = ProgressBar(100)
        pb.set_current(50)
        self.assertEqual(pb.current, 50)
        pb.close()
    
    def test_set_current_invalid(self):
        """测试设置无效进度"""
        pb = ProgressBar(100)
        pb.set_current(-10)  # 负数
        self.assertEqual(pb.current, 0)
        pb.set_current(200)  # 超过总数
        self.assertEqual(pb.current, 100)
        pb.close()
    
    def test_progress_percent(self):
        """测试进度计算"""
        pb = ProgressBar(200)
        pb.set_current(50)
        self.assertEqual(pb.progress, 0.25)
        self.assertEqual(pb.percent, 25.0)
        pb.close()
    
    def test_elapsed(self):
        """测试已用时间"""
        pb = ProgressBar(100)
        time.sleep(0.1)
        self.assertGreaterEqual(pb.elapsed, 0.1)
        pb.close()
    
    def test_eta(self):
        """测试预估时间"""
        pb = ProgressBar(100)
        self.assertIsNone(pb.eta)  # 还没开始
        
        pb.update(10)
        time.sleep(0.1)
        pb.update(10)
        self.assertIsNotNone(pb.eta)
        pb.close()
    
    def test_rate(self):
        """测试速率"""
        pb = ProgressBar(100)
        time.sleep(0.1)
        pb.update(10)
        self.assertIsNotNone(pb.rate)
        self.assertGreater(pb.rate, 0)
        pb.close()
    
    def test_context_manager(self):
        """测试上下文管理器"""
        with ProgressBar(100) as pb:
            pb.update(50)
            self.assertEqual(pb.current, 50)
        # 离开上下文后已关闭
    
    def test_close(self):
        """测试关闭"""
        pb = ProgressBar(100)
        pb.update(50)
        pb.close()
        
        # 关闭后更新无效
        pb.update(10)
        self.assertEqual(pb.current, 50)
    
    def test_reset(self):
        """测试重置"""
        pb = ProgressBar(100, "原描述")
        pb.update(50)
        
        pb.reset(total=200, desc="新描述")
        self.assertEqual(pb.current, 0)
        self.assertEqual(pb.total, 200)
        pb.close()
    
    def test_repr(self):
        """测试字符串表示"""
        pb = ProgressBar(100, "测试")
        repr_str = repr(pb)
        self.assertIn("ProgressBar", repr_str)
        self.assertIn("current=0", repr_str)
        self.assertIn("total=100", repr_str)
        pb.close()
    
    def test_with_custom_output(self):
        """测试自定义输出"""
        output = io.StringIO()
        pb = ProgressBar(10, file=output)
        pb.update(5)
        pb.close()
        
        output_str = output.getvalue()
        self.assertIn("5/10", output_str)
    
    def test_different_styles(self):
        """测试不同样式"""
        output = io.StringIO()
        
        # 经典样式
        pb = ProgressBar(10, style=ProgressBarStyle.classic(), file=output)
        pb.update(5)
        pb.close()
        self.assertIn("#", output.getvalue())
        
        # 简约样式
        output2 = io.StringIO()
        pb2 = ProgressBar(10, style=ProgressBarStyle.minimal(), file=output2)
        pb2.update(5)
        pb2.close()
        self.assertIn("=", output2.getvalue())


class TestMultiProgressBar(unittest.TestCase):
    """MultiProgressBar 测试"""
    
    def test_add_task(self):
        """测试添加任务"""
        mpb = MultiProgressBar()
        task_id = mpb.add_task("任务A", 100)
        self.assertEqual(task_id, 0)
        mpb.close()
    
    def test_add_multiple_tasks(self):
        """测试添加多个任务"""
        mpb = MultiProgressBar()
        id1 = mpb.add_task("任务A", 100)
        id2 = mpb.add_task("任务B", 200)
        id3 = mpb.add_task("任务C", 150)
        
        self.assertEqual(id1, 0)
        self.assertEqual(id2, 1)
        self.assertEqual(id3, 2)
        mpb.close()
    
    def test_update_task(self):
        """测试更新任务"""
        output = io.StringIO()
        mpb = MultiProgressBar(file=output)
        
        task_id = mpb.add_task("任务A", 100)
        mpb.update(task_id, 50)
        mpb.close()
        
        self.assertIn("50/100", output.getvalue())
    
    def test_set_progress(self):
        """测试设置进度"""
        output = io.StringIO()
        mpb = MultiProgressBar(file=output)
        
        task_id = mpb.add_task("任务A", 100)
        mpb.set_progress(task_id, 75)
        mpb.close()
        
        self.assertIn("75/100", output.getvalue())
    
    def test_remove_task(self):
        """测试移除任务"""
        mpb = MultiProgressBar()
        task_id = mpb.add_task("任务A", 100)
        mpb.remove_task(task_id)
        mpb.close()
    
    def test_context_manager(self):
        """测试上下文管理器"""
        with MultiProgressBar() as mpb:
            task_id = mpb.add_task("任务A", 100)
            mpb.update(task_id, 50)


class TestSpinnerProgress(unittest.TestCase):
    """SpinnerProgress 测试"""
    
    def test_start_stop(self):
        """测试启动和停止"""
        output = io.StringIO()
        sp = SpinnerProgress("加载中", file=output, use_unicode=False)
        
        sp.start()
        time.sleep(0.3)  # 让动画运行
        sp.stop()
        
        output_str = output.getvalue()
        self.assertIn("加载中", output_str)
    
    def test_context_manager(self):
        """测试上下文管理器"""
        output = io.StringIO()
        
        with SpinnerProgress("处理中", file=output, use_unicode=False):
            time.sleep(0.2)
        
        output_str = output.getvalue()
        self.assertIn("处理中", output_str)
    
    def test_elapsed(self):
        """测试已用时间"""
        sp = SpinnerProgress()
        sp.start()
        time.sleep(0.2)
        self.assertGreaterEqual(sp.elapsed, 0.2)
        sp.stop()
    
    def test_custom_message(self):
        """测试自定义完成消息"""
        output = io.StringIO()
        sp = SpinnerProgress("加载中", file=output, use_unicode=False)
        sp.start()
        time.sleep(0.2)
        sp.stop("完成！")
        
        output_str = output.getvalue()
        self.assertIn("完成！", output_str)


class TestProgressBarBuilder(unittest.TestCase):
    """ProgressBarBuilder 测试"""
    
    def test_build(self):
        """测试构建进度条"""
        output = io.StringIO()
        pb = (ProgressBarBuilder()
              .total(100)
              .desc("测试任务")
              .style(ProgressBarStyle.minimal())
              .file(output)
              .min_interval(0.01)
              .build())
        
        self.assertEqual(pb.total, 100)
        pb.update(10)
        pb.close()
        
        output_str = output.getvalue()
        self.assertIn("测试任务", output_str)
        self.assertIn("10/100", output_str)


class TestUtilityFunctions(unittest.TestCase):
    """工具函数测试"""
    
    def test_progress_context(self):
        """测试进度上下文管理器"""
        output = io.StringIO()
        
        with progress(10, "处理", style=ProgressBarStyle.minimal()) as pb:
            pb._file = output
            for i in range(10):
                pb.update()
        
        self.assertEqual(pb.current, 10)
    
    def test_progress_range(self):
        """测试进度 range"""
        output = io.StringIO()
        result = []
        
        for i in progress_range(0, 5, desc="计数"):
            result.append(i)
        
        self.assertEqual(result, [0, 1, 2, 3, 4])
    
    def test_progress_range_with_step(self):
        """测试带步进的进度 range"""
        result = list(progress_range(0, 10, step=2))
        self.assertEqual(result, [0, 2, 4, 6, 8])
    
    def test_progress_iter(self):
        """测试进度迭代器"""
        items = [1, 2, 3, 4, 5]
        result = []
        
        for item in progress_iter(items):
            result.append(item)
        
        self.assertEqual(result, items)
    
    def test_progress_iter_with_total(self):
        """测试带总数的进度迭代器"""
        items = [1, 2, 3, 4, 5]
        result = list(progress_iter(items, total=5))
        self.assertEqual(result, items)
    
    def test_create_progress_bar(self):
        """测试创建进度条便捷函数"""
        pb = create_progress_bar(100, "测试", "classic")
        self.assertEqual(pb.total, 100)
        pb.close()
        
        pb2 = create_progress_bar(100, "测试", "modern")
        self.assertEqual(pb2.total, 100)
        pb2.close()
        
        pb3 = create_progress_bar(100, "测试", "minimal")
        self.assertEqual(pb3.total, 100)
        pb3.close()
    
    def test_timed_progress(self):
        """测试定时进度条"""
        start = time.time()
        timed_progress(0.5, "测试", steps=10)
        elapsed = time.time() - start
        
        # 应该大约 0.5 秒
        self.assertGreaterEqual(elapsed, 0.4)
        self.assertLess(elapsed, 1.0)


class TestThreadSafety(unittest.TestCase):
    """线程安全测试"""
    
    def test_concurrent_update(self):
        """测试并发更新"""
        pb = ProgressBar(1000, min_update_interval=0)
        
        def update_many(start, count):
            for _ in range(count):
                pb.update()
        
        threads = [
            threading.Thread(target=update_many, args=(i * 100, 100))
            for i in range(10)
        ]
        
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        self.assertEqual(pb.current, 1000)
        pb.close()
    
    def test_multi_progress_concurrent(self):
        """测试多进度条并发更新"""
        mpb = MultiProgressBar()
        
        task_ids = [mpb.add_task(f"任务{i}", 100) for i in range(5)]
        
        def update_task(task_id):
            for _ in range(100):
                mpb.update(task_id)
                time.sleep(0.001)
        
        threads = [
            threading.Thread(target=update_task, args=(tid,))
            for tid in task_ids
        ]
        
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        mpb.close()


class TestEdgeCases(unittest.TestCase):
    """边界情况测试"""
    
    def test_single_item(self):
        """测试单项进度"""
        output = io.StringIO()
        pb = ProgressBar(1, file=output)
        pb.update()
        pb.close()
        
        self.assertIn("1/1", output.getvalue())
    
    def test_large_total(self):
        """测试大总数"""
        output = io.StringIO()
        pb = ProgressBar(10000000, file=output)
        pb.update(10000000)
        pb.close()
        
        self.assertIn("10000000", output.getvalue())
    
    def test_unicode_description(self):
        """测试 Unicode 描述"""
        output = io.StringIO()
        pb = ProgressBar(100, "处理文件 📁", file=output)
        pb.update(50)
        pb.close()
        
        self.assertIn("处理文件 📁", output.getvalue())
    
    def test_empty_description(self):
        """测试空描述"""
        output = io.StringIO()
        pb = ProgressBar(100, "", file=output)
        pb.update(50)
        pb.close()
        
        self.assertIn("50/100", output.getvalue())
    
    def test_update_after_close(self):
        """测试关闭后更新"""
        output = io.StringIO()
        pb = ProgressBar(100, file=output)
        pb.update(50)
        pb.close()
        
        output_str = output.getvalue()
        pb.update(30)
        
        # 更新无效，仍然是 50
        self.assertEqual(pb.current, 50)
    
    def test_reset_after_close(self):
        """测试关闭后重置"""
        pb = ProgressBar(100)
        pb.update(50)
        pb.close()
        
        # 重置应该可以重新使用
        pb.reset(total=200)
        self.assertEqual(pb.current, 0)
        self.assertEqual(pb.total, 200)
        pb.close()


if __name__ == "__main__":
    unittest.main(verbosity=2)