"""
进度追踪工具模块测试
"""

import io
import sys
import os
import time
import unittest
from unittest.mock import patch

# 添加模块路径
sys.path.insert(0, '..')

from mod import (
    ProgressBar,
    ProgressTracker,
    Spinner,
    ETAEstimator,
    progress_bar,
    track,
    format_duration,
    format_rate,
)


class TestProgressBar(unittest.TestCase):
    """ProgressBar 测试"""
    
    def test_basic_progress(self):
        """测试基本进度更新"""
        output = io.StringIO()
        bar = ProgressBar(total=10, output=output, show_eta=False)
        
        bar.update(1)
        self.assertEqual(bar.current, 1)
        
        bar.update(5)
        self.assertEqual(bar.current, 6)
        
        bar.update(10)  # 应该限制在 total
        self.assertEqual(bar.current, 10)
        self.assertTrue(bar._completed)
    
    def test_render_styles(self):
        """测试不同样式渲染"""
        styles = ['classic', 'modern', 'dots', 'arrows', 'blocks', 'minimal', 'fancy']
        
        for style in styles:
            bar = ProgressBar(total=100, style=style, show_eta=False, show_percent=False, show_count=False)
            bar.set_progress(50)
            rendered = bar.render()
            self.assertIn(bar.style['border'][0], rendered)
    
    def test_render_with_all_options(self):
        """测试所有显示选项"""
        output = io.StringIO()
        bar = ProgressBar(
            total=100,
            width=20,
            show_percent=True,
            show_eta=True,
            show_count=True,
            prefix='处理中:',
            suffix='...',
            output=output
        )
        bar.start_time = time.time()
        bar.set_progress(50)
        
        rendered = bar.render()
        self.assertIn('处理中:', rendered)
        self.assertIn('50.0%', rendered)
        self.assertIn('50/100', rendered)
        self.assertIn('ETA:', rendered)
        self.assertIn('...', rendered)
    
    def test_invalid_style(self):
        """测试无效样式"""
        with self.assertRaises(ValueError):
            ProgressBar(total=10, style='invalid_style')
    
    def test_invalid_total(self):
        """测试无效总数"""
        with self.assertRaises(ValueError):
            ProgressBar(total=0)
        with self.assertRaises(ValueError):
            ProgressBar(total=-1)
    
    def test_context_manager(self):
        """测试上下文管理器"""
        output = io.StringIO()
        with ProgressBar(total=10, output=output) as bar:
            bar.update(5)
            self.assertEqual(bar.current, 5)
        
        # 未完成时应该输出换行
    
    def test_set_progress(self):
        """测试直接设置进度"""
        output = io.StringIO()
        bar = ProgressBar(total=100, output=output)
        
        bar.set_progress(50)
        self.assertEqual(bar.current, 50)
        
        bar.set_progress(150)  # 应该限制在 total
        self.assertEqual(bar.current, 100)
        
        bar.set_progress(-10)  # 应该限制在 0
        self.assertEqual(bar.current, 0)
    
    def test_reset(self):
        """测试重置"""
        output = io.StringIO()
        bar = ProgressBar(total=100, output=output)
        bar.update(50)
        self.assertEqual(bar.current, 50)
        
        bar.reset()
        self.assertEqual(bar.current, 0)
        self.assertIsNone(bar.start_time)
        self.assertFalse(bar._completed)


class TestProgressBarStyles(unittest.TestCase):
    """进度条样式测试"""
    
    def test_classic_style(self):
        """测试 classic 样式"""
        bar = ProgressBar(total=100, style='classic', show_eta=False, show_percent=False, show_count=False)
        bar.set_progress(50)
        rendered = bar.render()
        self.assertIn('#', rendered)
        self.assertIn('-', rendered)
        self.assertIn('[', rendered)
    
    def test_modern_style(self):
        """测试 modern 样式"""
        bar = ProgressBar(total=100, style='modern', show_eta=False, show_percent=False, show_count=False)
        bar.set_progress(50)
        rendered = bar.render()
        self.assertIn('█', rendered)
        self.assertIn('░', rendered)
    
    def test_dots_style(self):
        """测试 dots 样式"""
        bar = ProgressBar(total=100, style='dots', show_eta=False, show_percent=False, show_count=False)
        bar.set_progress(50)
        rendered = bar.render()
        self.assertIn('●', rendered)
        self.assertIn('○', rendered)


class TestTrack(unittest.TestCase):
    """track 函数测试"""
    
    def test_track_with_list(self):
        """测试跟踪列表"""
        items = list(range(5))
        result = list(track(items, description='处理:'))
        self.assertEqual(result, items)
    
    def test_track_with_range(self):
        """测试跟踪 range"""
        result = list(track(range(10), total=10, description='计数:'))
        self.assertEqual(len(result), 10)
    
    def test_track_unknown_length(self):
        """测试未知长度的迭代器"""
        def gen():
            yield 1
            yield 2
            yield 3
        
        result = list(track(gen()))
        self.assertEqual(result, [1, 2, 3])


class TestProgressTracker(unittest.TestCase):
    """ProgressTracker 测试"""
    
    def test_basic_tracking(self):
        """测试基本追踪"""
        tracker = ProgressTracker(total=100, description='测试任务')
        tracker.start()
        
        self.assertEqual(tracker.current, 0)
        self.assertEqual(tracker.progress, 0)
        self.assertEqual(tracker.percent, 0)
        
        tracker.update(25)
        self.assertEqual(tracker.current, 25)
        self.assertEqual(tracker.progress, 0.25)
        self.assertEqual(tracker.percent, 25)
        
        tracker.set_progress(50)
        self.assertEqual(tracker.current, 50)
    
    def test_completion(self):
        """测试完成状态"""
        tracker = ProgressTracker(total=10)
        
        completed_called = []
        def on_complete():
            completed_called.append(True)
        
        tracker.on_complete = on_complete
        tracker.start()
        tracker.update(10)
        
        self.assertTrue(tracker.is_complete)
        self.assertTrue(completed_called)
    
    def test_stats(self):
        """测试统计信息"""
        tracker = ProgressTracker(total=100, description='统计测试')
        tracker.start()
        tracker.update(50)
        
        stats = tracker.get_stats()
        self.assertEqual(stats['description'], '统计测试')
        self.assertEqual(stats['current'], 50)
        self.assertEqual(stats['total'], 100)
        self.assertEqual(stats['progress'], 0.5)
        self.assertEqual(stats['percent'], 50)
        self.assertIn('elapsed', stats)
        self.assertIn('eta', stats)
        self.assertIn('rate', stats)
    
    def test_milestones(self):
        """测试里程碑"""
        tracker = ProgressTracker(total=100)
        tracker.start()
        
        tracker.set_progress(25).milestone('第一阶段')
        tracker.set_progress(50).milestone('第二阶段')
        tracker.set_progress(100).milestone('完成')
        
        milestones = tracker.get_milestones()
        self.assertEqual(len(milestones), 3)
        self.assertEqual(milestones[0]['name'], '第一阶段')
        self.assertEqual(milestones[1]['name'], '第二阶段')
        self.assertEqual(milestones[2]['name'], '完成')
    
    def test_sub_tracker(self):
        """测试子追踪器"""
        tracker = ProgressTracker(total=100)
        sub = tracker.add_sub_tracker(50, '子任务')
        
        self.assertEqual(sub.total, 50)
        self.assertEqual(sub.description, '子任务')
    
    def test_context_manager(self):
        """测试上下文管理器"""
        with ProgressTracker(total=100) as tracker:
            tracker.update(50)
            self.assertEqual(tracker.current, 50)
            self.assertIsNotNone(tracker.start_time)


class TestSpinner(unittest.TestCase):
    """Spinner 测试"""
    
    def test_styles(self):
        """测试所有样式"""
        for style in Spinner.STYLES:
            output = io.StringIO()
            spinner = Spinner('加载中...', style=style, output=output)
            spinner.start()
            spinner.stop()
            self.assertIsNotNone(spinner.message)
    
    def test_invalid_style(self):
        """测试无效样式"""
        with self.assertRaises(ValueError):
            Spinner(style='invalid')
    
    def test_update_message(self):
        """测试更新消息"""
        output = io.StringIO()
        spinner = Spinner('初始消息', output=output)
        spinner.update('新消息')
        self.assertEqual(spinner.message, '新消息')
    
    def test_context_manager(self):
        """测试上下文管理器"""
        output = io.StringIO()
        with Spinner('加载中...', output=output) as spinner:
            self.assertTrue(spinner._active)
        self.assertFalse(spinner._active)


class TestETAEstimator(unittest.TestCase):
    """ETAEstimator 测试"""
    
    def test_basic_estimation(self):
        """测试基本估算"""
        estimator = ETAEstimator()
        
        # 模拟进度更新
        for i in range(1, 11):
            time.sleep(0.01)  # 小延迟
            estimator.update(i)
        
        # 估算剩余时间
        eta = estimator.estimate(100)
        self.assertGreater(eta, 0)
    
    def test_rate_calculation(self):
        """测试速率计算"""
        estimator = ETAEstimator(alpha=1.0)  # 使用即时速率
        
        # 需要多次更新才能计算速率
        for i in range(1, 11):
            time.sleep(0.01)  # 小延迟
            estimator.update(i)
        
        rate = estimator.get_rate()
        self.assertGreater(rate, 0)
    
    def test_reset(self):
        """测试重置"""
        estimator = ETAEstimator()
        
        # 需要多次更新才能产生有效速率
        for i in range(1, 11):
            time.sleep(0.01)
            estimator.update(i)
        
        self.assertGreater(estimator.get_rate(), 0)
        
        estimator.reset()
        self.assertEqual(estimator.get_rate(), 0)


class TestUtilityFunctions(unittest.TestCase):
    """工具函数测试"""
    
    def test_progress_bar_function(self):
        """测试 progress_bar 快捷函数"""
        bar = progress_bar(100, width=20, style='classic', prefix='Progress:')
        self.assertEqual(bar.total, 100)
        self.assertEqual(bar.width, 20)
        self.assertEqual(bar.style['filled'], '#')
    
    def test_format_duration(self):
        """测试持续时间格式化"""
        # 秒
        self.assertIn('秒', format_duration(0.5))
        self.assertIn('秒', format_duration(5))
        
        # 分钟
        result = format_duration(120)
        self.assertIn('分钟', result)
        
        # 小时
        result = format_duration(7200)
        self.assertIn('小时', result)
        
        # 天
        result = format_duration(172800)
        self.assertIn('天', result)
        
        # 负数
        self.assertEqual(format_duration(-1), "未知")
    
    def test_format_rate(self):
        """测试速率格式化"""
        self.assertIn('/秒', format_rate(0.5))
        self.assertIn('/秒', format_rate(5))
        self.assertIn('/秒', format_rate(100))
        self.assertIn('k', format_rate(1500))
        self.assertIn('M', format_rate(1500000))
        self.assertEqual(format_rate(0), '0 项/秒')
        
        # 自定义单位
        self.assertIn('个', format_rate(10, '个'))


class TestProgressBarRender(unittest.TestCase):
    """ProgressBar 渲染细节测试"""
    
    def test_render_zero_progress(self):
        """测试零进度渲染"""
        bar = ProgressBar(
            total=100,
            show_eta=False,
            show_percent=True,
            show_count=True
        )
        rendered = bar.render(0)
        self.assertIn('0.0%', rendered)
        self.assertIn('0/100', rendered)
    
    def test_render_full_progress(self):
        """测试完整进度渲染"""
        bar = ProgressBar(
            total=100,
            show_eta=False,
            show_percent=True,
            show_count=True
        )
        rendered = bar.render(100)
        self.assertIn('100.0%', rendered)
        self.assertIn('100/100', rendered)
    
    def test_format_time(self):
        """测试时间格式化"""
        bar = ProgressBar(total=100)
        
        # 秒
        self.assertEqual(bar._format_time(30), '30s')
        
        # 分钟:秒
        self.assertEqual(bar._format_time(90), '1:30')
        
        # 小时:分钟:秒
        self.assertEqual(bar._format_time(3661), '1:01:01')
        
        # 无效值
        self.assertEqual(bar._format_time(-1), '--:--:--')
        self.assertEqual(bar._format_time(float('inf')), '--:--:--')
    
    def test_calculate_eta(self):
        """测试 ETA 计算"""
        bar = ProgressBar(total=100)
        
        # 进度为 0
        eta = bar._calculate_eta(10, 0)
        self.assertEqual(eta, float('inf'))
        
        # 进度为 1
        eta = bar._calculate_eta(10, 1)
        self.assertEqual(eta, 0)
        
        # 正常进度
        eta = bar._calculate_eta(10, 0.5)
        self.assertEqual(eta, 10)  # 剩余 50% 需要 10 秒


if __name__ == '__main__':
    unittest.main(verbosity=2)