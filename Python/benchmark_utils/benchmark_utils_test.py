"""
AllToolkit - Python Benchmark Utilities Test Suite

Comprehensive tests for benchmark_utils module.
Run with: python benchmark_utils_test.py
"""

import unittest
import time
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    Timer,
    BenchmarkResult,
    BenchmarkComparison,
    BenchmarkRunner,
    PerformanceProfiler,
    benchmark,
    measure_time,
    measure_time_silent,
    time_func,
    compare_implementations,
    sleep_benchmark,
)


class TestTimer(unittest.TestCase):
    """Tests for Timer class."""
    
    def test_timer_basic(self):
        """Test basic timer functionality."""
        timer = Timer()
        self.assertEqual(timer.elapsed, 0.0)
        
        timer.start()
        time.sleep(0.01)  # Sleep 10ms
        timer.stop()
        
        self.assertGreater(timer.elapsed, 0.009)
        self.assertLess(timer.elapsed, 0.05)
    
    def test_timer_context_manager(self):
        """Test timer as context manager."""
        with Timer() as timer:
            time.sleep(0.01)
        
        self.assertGreater(timer.elapsed, 0.009)
        self.assertLess(timer.elapsed, 0.05)
    
    def test_timer_elapsed_ms(self):
        """Test elapsed_ms property."""
        with Timer() as timer:
            time.sleep(0.01)
        
        self.assertGreater(timer.elapsed_ms, 9.0)
        self.assertLess(timer.elapsed_ms, 50.0)
    
    def test_timer_running(self):
        """Test timer while still running."""
        timer = Timer()
        timer.start()
        time.sleep(0.01)
        
        # Should return elapsed time even without stop()
        self.assertGreater(timer.elapsed, 0.009)


class TestBenchmarkResult(unittest.TestCase):
    """Tests for BenchmarkResult class."""
    
    def test_result_creation(self):
        """Test basic result creation."""
        result = BenchmarkResult(
            name="test",
            iterations=100,
            times=[0.001, 0.002, 0.003],
        )
        result.calculate_stats()
        
        self.assertEqual(result.name, "test")
        self.assertEqual(result.iterations, 100)
        self.assertAlmostEqual(result.avg_time, 0.002, places=4)
        self.assertAlmostEqual(result.min_time, 0.001, places=4)
        self.assertAlmostEqual(result.max_time, 0.003, places=4)
    
    def test_result_stats_calculation(self):
        """Test statistical calculations."""
        result = BenchmarkResult(
            name="stats_test",
            iterations=10,
            times=[0.001] * 10,  # All same values
        )
        result.calculate_stats()
        
        self.assertAlmostEqual(result.total_time, 0.01, places=6)
        self.assertAlmostEqual(result.avg_time, 0.001, places=6)
        self.assertEqual(result.std_dev, 0.0)
        self.assertEqual(result.variance, 0.0)
    
    def test_result_ops_per_sec(self):
        """Test operations per second calculation."""
        result = BenchmarkResult(
            name="ops_test",
            iterations=1000,
            times=[0.001] * 1000,  # 1ms each = 1 second total
        )
        result.calculate_stats()
        
        self.assertAlmostEqual(result.ops_per_sec, 1000.0, places=1)
    
    def test_result_to_dict(self):
        """Test conversion to dictionary."""
        result = BenchmarkResult(
            name="dict_test",
            iterations=100,
            times=[0.001, 0.002],
            metadata={'key': 'value'},
        )
        result.calculate_stats()
        
        d = result.to_dict()
        self.assertEqual(d['name'], 'dict_test')
        self.assertEqual(d['iterations'], 100)
        self.assertEqual(d['metadata'], {'key': 'value'})
        self.assertIn('avg_time', d)
    
    def test_result_string_representation(self):
        """Test string representation."""
        result = BenchmarkResult(
            name="str_test",
            iterations=100,
            times=[0.001, 0.002, 0.003],
        )
        result.calculate_stats()
        
        str_repr = str(result)
        self.assertIn("str_test", str_repr)
        self.assertIn("avg=", str_repr)
        self.assertIn("ops/s=", str_repr)


class TestBenchmarkComparison(unittest.TestCase):
    """Tests for BenchmarkComparison class."""
    
    def test_add_result(self):
        """Test adding results to comparison."""
        comparison = BenchmarkComparison()
        result = BenchmarkResult(name="test", iterations=100, times=[0.001])
        result.calculate_stats()
        
        comparison.add_result(result)
        self.assertEqual(len(comparison.results), 1)
    
    def test_relative_performance(self):
        """Test relative performance calculation."""
        comparison = BenchmarkComparison()
        
        # Baseline: 0.002s avg
        baseline = BenchmarkResult(name="baseline", iterations=100, times=[0.002] * 10)
        baseline.calculate_stats()
        
        # Faster: 0.001s avg (2x faster)
        faster = BenchmarkResult(name="faster", iterations=100, times=[0.001] * 10)
        faster.calculate_stats()
        
        comparison.add_result(baseline)
        comparison.add_result(faster)
        comparison.set_baseline("baseline")
        
        relative = comparison.get_relative_performance()
        self.assertAlmostEqual(relative["faster"], 2.0, places=1)
    
    def test_comparison_to_dict(self):
        """Test comparison to dictionary."""
        comparison = BenchmarkComparison()
        result = BenchmarkResult(name="test", iterations=100, times=[0.001])
        result.calculate_stats()
        comparison.add_result(result)
        
        d = comparison.to_dict()
        self.assertIn('results', d)
        self.assertIn('relative_performance', d)


class TestBenchmarkRunner(unittest.TestCase):
    """Tests for BenchmarkRunner class."""
    
    def test_run_basic(self):
        """Test basic benchmark run."""
        runner = BenchmarkRunner(warmup_iterations=1, verbose=False)
        
        def simple_func():
            return 42
        
        result = runner.run("simple", simple_func, iterations=10)
        
        self.assertEqual(result.name, "simple")
        self.assertEqual(result.iterations, 10)
        self.assertGreater(result.avg_time, 0)
    
    def test_run_with_args(self):
        """Test benchmark with function arguments."""
        runner = BenchmarkRunner(warmup_iterations=1, verbose=False)
        
        def add_func(a, b):
            return a + b
        
        result = runner.run(
            "add", 
            add_func, 
            iterations=100,
            args=(5, 3),
        )
        
        self.assertEqual(result.name, "add")
        self.assertGreater(result.avg_time, 0)
    
    def test_run_with_kwargs(self):
        """Test benchmark with keyword arguments."""
        runner = BenchmarkRunner(warmup_iterations=1, verbose=False)
        
        def multiply_func(a, b=1):
            return a * b
        
        result = runner.run(
            "multiply",
            multiply_func,
            iterations=100,
            args=(5,),
            kwargs={'b': 3},
        )
        
        self.assertEqual(result.name, "multiply")
    
    def test_run_comparison(self):
        """Test running multiple benchmarks for comparison."""
        runner = BenchmarkRunner(warmup_iterations=1, verbose=False)
        
        def slow_func():
            time.sleep(0.001)
        
        def fast_func():
            pass
        
        comparison = runner.run_comparison({
            'slow': slow_func,
            'fast': fast_func,
        }, iterations=10)
        
        self.assertEqual(len(comparison.results), 2)
        self.assertGreater(
            comparison.results[0].avg_time,
            comparison.results[1].avg_time,
        )
    
    def test_get_result(self):
        """Test retrieving specific result."""
        runner = BenchmarkRunner(warmup_iterations=1, verbose=False)
        runner.run("test", lambda: None, iterations=10)
        
        result = runner.get_result("test")
        self.assertIsNotNone(result)
        self.assertEqual(result.name, "test")
    
    def test_clear_results(self):
        """Test clearing results."""
        runner = BenchmarkRunner(warmup_iterations=1, verbose=False)
        runner.run("test", lambda: None, iterations=10)
        
        runner.clear()
        self.assertEqual(len(runner.get_all_results()), 0)


class TestDecorators(unittest.TestCase):
    """Tests for benchmark decorators."""
    
    def test_benchmark_decorator(self):
        """Test benchmark decorator."""
        @benchmark(name="decorated_test", iterations=10, warmup=1)
        def test_func():
            return 42
        
        # Call the function
        result = test_func()
        self.assertEqual(result, 42)
        
        # Check benchmark result is available
        bench_result = test_func.benchmark_result()
        self.assertIsNotNone(bench_result)
        self.assertEqual(bench_result.name, "decorated_test")
    
    def test_measure_time_context(self):
        """Test measure_time context manager."""
        with measure_time("test_op") as timer:
            time.sleep(0.01)
        
        self.assertGreater(timer.elapsed, 0.009)
    
    def test_measure_time_silent(self):
        """Test silent measure_time context manager."""
        with measure_time_silent() as timer:
            time.sleep(0.01)
        
        self.assertGreater(timer.elapsed, 0.009)


class TestTimeFunc(unittest.TestCase):
    """Tests for time_func utility."""
    
    def test_time_func_basic(self):
        """Test basic time_func."""
        def test_func():
            time.sleep(0.01)
            return "done"
        
        result, elapsed = time_func(test_func, print_result=False)
        
        self.assertEqual(result, "done")
        self.assertGreater(elapsed, 0.009)
    
    def test_time_func_iterations(self):
        """Test time_func with multiple iterations."""
        counter = {'count': 0}
        
        def increment():
            counter['count'] += 1
        
        _, elapsed = time_func(increment, iterations=5, print_result=False)
        
        self.assertEqual(counter['count'], 5)
        self.assertGreater(elapsed, 0)


class TestPerformanceProfiler(unittest.TestCase):
    """Tests for PerformanceProfiler class."""
    
    def test_profile_decorator(self):
        """Test profile decorator."""
        profiler = PerformanceProfiler()
        
        @profiler.profile(name="profiled_func")
        def test_func():
            time.sleep(0.001)
        
        # Call multiple times
        for _ in range(5):
            test_func()
        
        stats = profiler.get_stats("profiled_func")
        self.assertIsNotNone(stats)
        self.assertEqual(stats['count'], 5)
        self.assertGreater(stats['avg'], 0.0009)
    
    def test_get_all_stats(self):
        """Test getting all stats."""
        profiler = PerformanceProfiler()
        
        @profiler.profile(name="func1")
        def func1():
            pass
        
        @profiler.profile(name="func2")
        def func2():
            pass
        
        func1()
        func2()
        
        all_stats = profiler.get_all_stats()
        self.assertIn("func1", all_stats)
        self.assertIn("func2", all_stats)
    
    def test_clear_profiler(self):
        """Test clearing profiler data."""
        profiler = PerformanceProfiler()
        
        @profiler.profile(name="to_clear")
        def test_func():
            pass
        
        test_func()
        
        profiler.clear("to_clear")
        stats = profiler.get_stats("to_clear")
        self.assertIsNone(stats)


class TestCompareImplementations(unittest.TestCase):
    """Tests for compare_implementations utility."""
    
    def test_compare_basic(self):
        """Test comparing implementations."""
        def impl1():
            return sum(range(100))
        
        def impl2():
            total = 0
            for i in range(100):
                total += i
            return total
        
        comparison = compare_implementations(
            {'impl1': impl1, 'impl2': impl2},
            iterations=10,
        )
        
        self.assertEqual(len(comparison.results), 2)


class TestUtilityFunctions(unittest.TestCase):
    """Tests for utility functions."""
    
    def test_sleep_benchmark(self):
        """Test sleep benchmark utility."""
        start = time.time()
        sleep_benchmark(50)  # Sleep 50ms
        elapsed = time.time() - start
        
        self.assertGreater(elapsed, 0.045)
        self.assertLess(elapsed, 0.1)


class TestThreadSafety(unittest.TestCase):
    """Tests for thread safety."""
    
    def test_runner_thread_safety(self):
        """Test BenchmarkRunner thread safety."""
        import threading
        
        runner = BenchmarkRunner(warmup_iterations=1, verbose=False)
        errors = []
        
        def run_benchmark(name):
            try:
                def func():
                    pass
                runner.run(name, func, iterations=10)
            except Exception as e:
                errors.append(e)
        
        threads = []
        for i in range(5):
            t = threading.Thread(target=run_benchmark, args=(f"bench_{i}",))
            threads.append(t)
            t.start()
        
        for t in threads:
            t.join()
        
        self.assertEqual(len(errors), 0)
        self.assertEqual(len(runner.get_all_results()), 5)


class TestEdgeCases(unittest.TestCase):
    """Tests for edge cases."""
    
    def test_empty_times(self):
        """Test result with no times."""
        result = BenchmarkResult(name="empty", iterations=0, times=[])
        result.calculate_stats()
        
        self.assertEqual(result.total_time, 0)
        self.assertEqual(result.avg_time, 0)
        self.assertEqual(result.ops_per_sec, 0)
    
    def test_single_iteration(self):
        """Test result with single iteration."""
        result = BenchmarkResult(name="single", iterations=1, times=[0.001])
        result.calculate_stats()
        
        self.assertEqual(result.std_dev, 0.0)
        self.assertEqual(result.variance, 0.0)
    
    def test_very_fast_function(self):
        """Test benchmarking very fast function."""
        runner = BenchmarkRunner(warmup_iterations=1, verbose=False)
        
        def instant():
            return None
        
        result = runner.run("instant", instant, iterations=10000)
        
        self.assertGreater(result.iterations, 0)
        # Even instant functions take some time


def run_tests():
    """Run all tests and print summary."""
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(sys.modules[__name__])
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print("\n" + "="*60)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success: {result.wasSuccessful()}")
    print("="*60)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
