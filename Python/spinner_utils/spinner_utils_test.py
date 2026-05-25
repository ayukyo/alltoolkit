#!/usr/bin/env python3
"""
Terminal Spinner Utils 测试套件

测试覆盖：
- 基本动画功能
- 多种样式
- 颜色支持
- 进度显示
- 时间显示
- 迭代器包装
- 装饰器功能
- 多任务管理
"""

import time
import sys
import io
import threading

import sys
import os

# Ensure the module directory is in sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    Spinner,
    spinner,
    spin,
    SpinnerIterator,
    MultiSpinner,
    animated_wait,
    list_styles,
    preview_styles,
    SPINNER_FRAMES,
    ANSI_COLORS,
    ANSI_RESET
)


class TestSpinnerBasics(unittest.TestCase):
    """测试 Spinner 基本功能"""
    
    def test_spinner_creation(self):
        """测试 Spinner 创建"""
        s = Spinner("Test message")
        self.assertEqual(s.message, "Test message")
        self.assertFalse(s._running)
    
    def test_spinner_with_style(self):
        """测试不同样式"""
        for style in ['dots', 'arrow', 'line', 'pulse']:
            s = Spinner(style=style)
            self.assertEqual(s.frames, SPINNER_FRAMES[style])
    
    def test_spinner_with_invalid_style(self):
        """测试无效样式使用默认值"""
        s = Spinner(style='invalid_style_name')
        self.assertEqual(s.frames, SPINNER_FRAMES['dots'])
    
    def test_spinner_with_custom_frames(self):
        """测试自定义帧"""
        custom_frames = ['a', 'b', 'c']
        s = Spinner(frames=custom_frames)
        self.assertEqual(s.frames, custom_frames)
    
    def test_spinner_with_color(self):
        """测试颜色设置"""
        s = Spinner(color='green')
        self.assertEqual(s.color_code, ANSI_COLORS['green'])
        self.assertEqual(s.color_reset, ANSI_RESET)
    
    def test_spinner_with_invalid_color(self):
        """测试无效颜色"""
        s = Spinner(color='invalid')
        self.assertEqual(s.color_code, '')
    
    def test_spinner_start_stop(self):
        """测试启动和停止"""
        s = Spinner("Test")
        s.start()
        self.assertTrue(s._running)
        self.assertIsNotNone(s._thread)
        time.sleep(0.3)  # 让动画运行一会儿
        s.stop()
        self.assertFalse(s._running)
    
    def test_spinner_context_manager(self):
        """测试上下文管理器"""
        with Spinner("Test") as s:
            self.assertTrue(s._running)
        self.assertFalse(s._running)
    
    def test_spinner_context_manager_exception(self):
        """测试上下文管理器异常处理"""
        try:
            with Spinner("Test") as s:
                raise ValueError("Test error")
        except ValueError:
            pass
        self.assertFalse(s._running)


class TestSpinnerUpdate(unittest.TestCase):
    """测试 Spinner 更新功能"""
    
    def test_update_message(self):
        """测试更新消息"""
        s = Spinner("Original")
        s.update("New message")
        self.assertEqual(s.message, "New message")
    
    def test_set_progress(self):
        """测试设置进度"""
        s = Spinner(show_progress=True)
        s.set_progress(0.5)
        self.assertEqual(s._progress, 0.5)
    
    def test_set_progress_bounds(self):
        """测试进度边界"""
        s = Spinner(show_progress=True)
        s.set_progress(-0.5)
        self.assertEqual(s._progress, 0.0)
        s.set_progress(1.5)
        self.assertEqual(s._progress, 1.0)


class TestSpinnerHelpers(unittest.TestCase):
    """测试辅助函数"""
    
    def test_spinner_context(self):
        """测试 spinner 上下文管理器"""
        with spinner("Loading...") as s:
            self.assertTrue(s._running)
        self.assertFalse(s._running)
    
    def test_spin_decorator(self):
        """测试 spin 装饰器"""
        @spin("Working...")
        def test_func():
            time.sleep(0.2)
            return "success"
        
        result = test_func()
        self.assertEqual(result, "success")
    
    def test_spin_decorator_exception(self):
        """测试 spin 装饰器异常处理"""
        @spin("Failing...")
        def failing_func():
            raise RuntimeError("Test error")
        
        with self.assertRaises(RuntimeError):
            failing_func()
    
    def test_list_styles(self):
        """测试列出样式"""
        styles = list_styles()
        self.assertIsInstance(styles, list)
        self.assertIn('dots', styles)
        self.assertIn('arrow', styles)
    
    def test_animated_wait(self):
        """测试动画等待"""
        start = time.time()
        animated_wait(0.5, "Waiting", style='dots')
        elapsed = time.time() - start
        self.assertGreaterEqual(elapsed, 0.5)


class TestSpinnerIterator(unittest.TestCase):
    """测试 SpinnerIterator"""
    
    def test_iterator_basic(self):
        """测试基本迭代"""
        items = [1, 2, 3, 4, 5]
        results = []
        
        for item in SpinnerIterator(items, "Processing"):
            results.append(item)
        
        self.assertEqual(results, items)
    
    def test_iterator_with_known_length(self):
        """测试已知长度的迭代"""
        items = list(range(10))
        results = []
        
        for item in SpinnerIterator(items, "Processing"):
            results.append(item)
        
        self.assertEqual(results, items)
    
    def test_iterator_empty(self):
        """测试空迭代"""
        items = []
        results = []
        
        for item in SpinnerIterator(items, "Processing"):
            results.append(item)
        
        self.assertEqual(results, [])


class TestMultiSpinner(unittest.TestCase):
    """测试 MultiSpinner"""
    
    def test_add_task(self):
        """测试添加任务"""
        ms = MultiSpinner()
        idx = ms.add("Task 1", 'dots')
        self.assertEqual(idx, 0)
        self.assertEqual(len(ms.tasks), 1)
    
    def test_multiple_tasks(self):
        """测试多任务"""
        ms = MultiSpinner()
        ms.add("Task 1")
        ms.add("Task 2")
        ms.add("Task 3")
        self.assertEqual(len(ms.tasks), 3)
    
    def test_complete_task(self):
        """测试完成任务"""
        ms = MultiSpinner()
        idx = ms.add("Task 1")
        ms.complete(idx, success=True)
        self.assertTrue(ms.tasks[idx]['completed'])
        self.assertTrue(ms.tasks[idx]['success'])
    
    def test_complete_task_failure(self):
        """测试失败任务"""
        ms = MultiSpinner()
        idx = ms.add("Task 1")
        ms.complete(idx, success=False, message="Failed")
        self.assertTrue(ms.tasks[idx]['completed'])
        self.assertFalse(ms.tasks[idx]['success'])
        self.assertEqual(ms.tasks[idx]['message'], "Failed")
    
    def test_context_manager(self):
        """测试上下文管理器"""
        with MultiSpinner() as ms:
            self.assertTrue(ms._running)
            ms.add("Task 1")
        self.assertFalse(ms._running)


class TestSpinnerStyles(unittest.TestCase):
    """测试所有动画样式"""
    
    def test_all_styles_have_frames(self):
        """测试所有样式都有帧"""
        for style, frames in SPINNER_FRAMES.items():
            self.assertIsInstance(frames, list)
            self.assertGreater(len(frames), 0)
    
    def test_all_styles_work(self):
        """测试所有样式都能正常工作"""
        for style in SPINNER_FRAMES.keys():
            s = Spinner(style=style)
            s.start()
            time.sleep(0.2)
            s.stop()
            # 没有异常即通过


class TestSpinnerColors(unittest.TestCase):
    """测试颜色功能"""
    
    def test_all_colors(self):
        """测试所有颜色"""
        for color in ['black', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white']:
            s = Spinner(color=color)
            self.assertEqual(s.color_code, ANSI_COLORS[color])
    
    def test_bright_colors(self):
        """测试亮色"""
        for color in ['bright_red', 'bright_green', 'bright_blue']:
            s = Spinner(color=color)
            self.assertEqual(s.color_code, ANSI_COLORS[color])


class TestOutput(unittest.TestCase):
    """测试输出功能"""
    
    def test_custom_output(self):
        """测试自定义输出流"""
        output = io.StringIO()
        s = Spinner("Test", output=output)
        s.start()
        time.sleep(0.2)
        s.stop()
        
        content = output.getvalue()
        # 应该有一些输出
        self.assertGreater(len(content), 0)


class TestIntegration(unittest.TestCase):
    """集成测试"""
    
    def test_full_workflow(self):
        """测试完整工作流程"""
        with Spinner("Loading...", style='dots', color='cyan', show_elapsed=True) as s:
            for i in range(5):
                time.sleep(0.1)
                s.update(f"Step {i+1}/5")
                s.set_progress((i + 1) / 5)
    
    def test_concurrent_spinners(self):
        """测试并发 Spinner（不同场景）"""
        results = []
        
        def run_spinner(name):
            with Spinner(f"Task {name}", style='dots'):
                time.sleep(0.3)
            results.append(name)
        
        threads = [
            threading.Thread(target=run_spinner, args=(i,))
            for i in range(3)
        ]
        
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        self.assertEqual(len(results), 3)


def run_tests():
    """运行所有测试"""
    # 创建测试套件
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # 添加测试类
    suite.addTests(loader.loadTestsFromTestCase(TestSpinnerBasics))
    suite.addTests(loader.loadTestsFromTestCase(TestSpinnerUpdate))
    suite.addTests(loader.loadTestsFromTestCase(TestSpinnerHelpers))
    suite.addTests(loader.loadTestsFromTestCase(TestSpinnerIterator))
    suite.addTests(loader.loadTestsFromTestCase(TestMultiSpinner))
    suite.addTests(loader.loadTestsFromTestCase(TestSpinnerStyles))
    suite.addTests(loader.loadTestsFromTestCase(TestSpinnerColors))
    suite.addTests(loader.loadTestsFromTestCase(TestOutput))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    print("=" * 60)
    print("Terminal Spinner Utils Test Suite")
    print("=" * 60)
    print()
    
    success = run_tests()
    
    print()
    print("=" * 60)
    if success:
        print("All tests passed! ✓")
    else:
        print("Some tests failed! ✗")
    print("=" * 60)
    
    sys.exit(0 if success else 1)