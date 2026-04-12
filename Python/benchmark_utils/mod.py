"""
AllToolkit - Python Benchmark Utilities

A zero-dependency, production-ready benchmarking and performance measurement module.
Supports timing, statistical analysis, comparison, and report generation.

Author: AllToolkit
License: MIT
"""

import time
import statistics
import functools
import threading
import json
import os
from typing import Optional, Any, Dict, List, Callable, Tuple, Union, TypeVar
from dataclasses import dataclass, field
from contextlib import contextmanager
from datetime import datetime
from collections import defaultdict


T = TypeVar('T')


@dataclass
class BenchmarkResult:
    """Represents the result of a single benchmark run."""
    name: str
    iterations: int
    times: List[float] = field(default_factory=list)
    total_time: float = 0.0
    avg_time: float = 0.0
    min_time: float = float('inf')
    max_time: float = 0.0
    median_time: float = 0.0
    std_dev: float = 0.0
    variance: float = 0.0
    ops_per_sec: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def calculate_stats(self) -> None:
        """Calculate statistical measures from timing data."""
        if not self.times:
            return
        
        self.total_time = sum(self.times)
        self.avg_time = self.total_time / len(self.times)
        self.min_time = min(self.times)
        self.max_time = max(self.times)
        self.median_time = statistics.median(self.times)
        
        if len(self.times) > 1:
            self.std_dev = statistics.stdev(self.times)
            self.variance = statistics.variance(self.times)
        else:
            self.std_dev = 0.0
            self.variance = 0.0
        
        self.ops_per_sec = self.iterations / self.total_time if self.total_time > 0 else 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert result to dictionary."""
        return {
            'name': self.name,
            'iterations': self.iterations,
            'total_time': self.total_time,
            'avg_time': self.avg_time,
            'min_time': self.min_time,
            'max_time': self.max_time,
            'median_time': self.median_time,
            'std_dev': self.std_dev,
            'variance': self.variance,
            'ops_per_sec': self.ops_per_sec,
            'metadata': self.metadata,
        }
    
    def __str__(self) -> str:
        return (
            f"BenchmarkResult({self.name}: "
            f"avg={self.avg_time*1000:.3f}ms, "
            f"min={self.min_time*1000:.3f}ms, "
            f"max={self.max_time*1000:.3f}ms, "
            f"ops/s={self.ops_per_sec:.2f})"
        )


@dataclass
class BenchmarkComparison:
    """Represents comparison between multiple benchmarks."""
    results: List[BenchmarkResult] = field(default_factory=list)
    baseline: Optional[str] = None
    
    def add_result(self, result: BenchmarkResult) -> None:
        """Add a benchmark result to comparison."""
        self.results.append(result)
    
    def set_baseline(self, name: str) -> None:
        """Set the baseline for comparison."""
        self.baseline = name
    
    def get_relative_performance(self) -> Dict[str, float]:
        """Get performance relative to baseline."""
        if not self.baseline or not self.results:
            return {}
        
        baseline_result = next(
            (r for r in self.results if r.name == self.baseline), 
            None
        )
        if not baseline_result or baseline_result.avg_time == 0:
            return {}
        
        relative = {}
        for result in self.results:
            if result.avg_time > 0:
                relative[result.name] = baseline_result.avg_time / result.avg_time
        return relative
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert comparison to dictionary."""
        return {
            'baseline': self.baseline,
            'results': [r.to_dict() for r in self.results],
            'relative_performance': self.get_relative_performance(),
        }


class Timer:
    """High-resolution timer for precise measurements."""
    
    def __init__(self):
        self._start: Optional[float] = None
        self._end: Optional[float] = None
        self._elapsed: float = 0.0
    
    def start(self) -> 'Timer':
        """Start the timer."""
        self._start = time.perf_counter()
        self._end = None
        self._elapsed = 0.0
        return self
    
    def stop(self) -> 'Timer':
        """Stop the timer."""
        if self._start is not None:
            self._end = time.perf_counter()
            self._elapsed = self._end - self._start
        return self
    
    @property
    def elapsed(self) -> float:
        """Get elapsed time in seconds."""
        if self._start is None:
            return 0.0
        if self._end is None:
            return time.perf_counter() - self._start
        return self._elapsed
    
    @property
    def elapsed_ms(self) -> float:
        """Get elapsed time in milliseconds."""
        return self.elapsed * 1000
    
    def __enter__(self) -> 'Timer':
        return self.start()
    
    def __exit__(self, *args) -> None:
        self.stop()


class BenchmarkRunner:
    """Main benchmark runner with comprehensive features."""
    
    def __init__(self, warmup_iterations: int = 1, verbose: bool = True):
        self.warmup_iterations = warmup_iterations
        self.verbose = verbose
        self._results: Dict[str, BenchmarkResult] = {}
        self._lock = threading.Lock()
        self._current_benchmark: Optional[str] = None
    
    def run(
        self,
        name: str,
        func: Callable[..., Any],
        iterations: int = 1000,
        args: Tuple = (),
        kwargs: Optional[Dict] = None,
        warmup: Optional[int] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> BenchmarkResult:
        """
        Run a benchmark for the given function.
        
        Args:
            name: Name of the benchmark
            func: Function to benchmark
            iterations: Number of iterations to run
            args: Arguments to pass to function
            kwargs: Keyword arguments to pass to function
            warmup: Number of warmup iterations (overrides default)
            metadata: Additional metadata to store
        
        Returns:
            BenchmarkResult with timing statistics
        """
        kwargs = kwargs or {}
        warmup_count = warmup if warmup is not None else self.warmup_iterations
        
        # Warmup phase
        for _ in range(warmup_count):
            func(*args, **kwargs)
        
        # Benchmark phase
        times: List[float] = []
        for _ in range(iterations):
            with Timer() as timer:
                func(*args, **kwargs)
            times.append(timer.elapsed)
        
        # Create result
        result = BenchmarkResult(
            name=name,
            iterations=iterations,
            times=times,
            metadata=metadata or {},
        )
        result.calculate_stats()
        
        # Store result
        with self._lock:
            self._results[name] = result
        
        if self.verbose:
            print(f"✓ {name}: avg={result.avg_time*1000:.3f}ms, "
                  f"ops/s={result.ops_per_sec:.2f}")
        
        return result
    
    def run_comparison(
        self,
        benchmarks: Dict[str, Callable[..., Any]],
        iterations: int = 1000,
        args: Tuple = (),
        kwargs: Optional[Dict] = None,
    ) -> BenchmarkComparison:
        """
        Run multiple benchmarks and compare them.
        
        Args:
            benchmarks: Dict mapping names to functions
            iterations: Number of iterations per benchmark
            args: Arguments to pass to all functions
            kwargs: Keyword arguments to pass to all functions
        
        Returns:
            BenchmarkComparison with all results
        """
        comparison = BenchmarkComparison()
        
        for name, func in benchmarks.items():
            result = self.run(name, func, iterations, args, kwargs)
            comparison.add_result(result)
        
        return comparison
    
    def get_result(self, name: str) -> Optional[BenchmarkResult]:
        """Get a specific benchmark result by name."""
        return self._results.get(name)
    
    def get_all_results(self) -> Dict[str, BenchmarkResult]:
        """Get all benchmark results."""
        return self._results.copy()
    
    def export_json(self, filepath: str) -> None:
        """Export results to JSON file."""
        data = {
            'timestamp': datetime.now().isoformat(),
            'results': {name: r.to_dict() for name, r in self._results.items()},
        }
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
    
    def export_markdown(self, filepath: str) -> None:
        """Export results to Markdown file."""
        lines = [
            "# Benchmark Results",
            "",
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "## Summary",
            "",
            "| Benchmark | Iterations | Avg (ms) | Min (ms) | Max (ms) | Ops/sec |",
            "|-----------|------------|----------|----------|----------|---------|",
        ]
        
        for result in self._results.values():
            lines.append(
                f"| {result.name} | {result.iterations} | "
                f"{result.avg_time*1000:.3f} | {result.min_time*1000:.3f} | "
                f"{result.max_time*1000:.3f} | {result.ops_per_sec:.2f} |"
            )
        
        with open(filepath, 'w') as f:
            f.write('\n'.join(lines))
    
    def clear(self) -> None:
        """Clear all stored results."""
        self._results.clear()


def benchmark(
    name: Optional[str] = None,
    iterations: int = 1000,
    warmup: int = 1,
    runner: Optional[BenchmarkRunner] = None,
) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """
    Decorator to benchmark a function.
    
    Args:
        name: Name for the benchmark (defaults to function name)
        iterations: Number of iterations
        warmup: Number of warmup iterations
        runner: BenchmarkRunner instance (creates one if not provided)
    
    Returns:
        Decorated function
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        benchmark_name = name or func.__name__
        _runner = runner or BenchmarkRunner(warmup_iterations=warmup, verbose=False)
        _result: Optional[BenchmarkResult] = None
        
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> T:
            nonlocal _result
            if _result is None:
                _result = _runner.run(
                    benchmark_name,
                    func,
                    iterations=iterations,
                    args=args,
                    kwargs=kwargs,
                )
            return func(*args, **kwargs)
        
        wrapper.benchmark_result = lambda: _result  # type: ignore
        wrapper.benchmark_runner = _runner  # type: ignore
        
        return wrapper
    
    return decorator


@contextmanager
def measure_time(name: str = "Operation") -> Timer:
    """
    Context manager to measure execution time.
    
    Args:
        name: Name of the operation being measured
    
    Yields:
        Timer instance with elapsed time
    """
    timer = Timer()
    with timer:
        yield timer
    if timer.elapsed > 0.001:  # Only print if > 1ms
        print(f"⏱ {name}: {timer.elapsed_ms:.3f}ms")


@contextmanager
def measure_time_silent() -> Timer:
    """
    Silent context manager to measure execution time without printing.
    
    Yields:
        Timer instance with elapsed time
    """
    timer = Timer()
    with timer:
        yield timer


def time_func(
    func: Callable[..., T],
    iterations: int = 1,
    print_result: bool = True,
) -> Tuple[T, float]:
    """
    Time a single function call (or multiple iterations).
    
    Args:
        func: Function to time
        iterations: Number of iterations
        print_result: Whether to print timing info
    
    Returns:
        Tuple of (result, total_time_seconds)
    """
    result = None
    with measure_time_silent() as timer:
        for _ in range(iterations):
            result = func()
    
    elapsed = timer.elapsed
    if print_result:
        print(f"⏱ {func.__name__}: {elapsed*1000:.3f}ms "
              f"({'x' + str(iterations) if iterations > 1 else '1x'})")
    
    return result, elapsed


class PerformanceProfiler:
    """Simple profiler for tracking function call performance over time."""
    
    def __init__(self):
        self._calls: Dict[str, List[float]] = defaultdict(list)
        self._lock = threading.Lock()
    
    def profile(
        self,
        name: Optional[str] = None,
    ) -> Callable[[Callable[..., T]], Callable[..., T]]:
        """
        Decorator to profile function calls.
        
        Args:
            name: Name for profiling (defaults to function name)
        
        Returns:
            Decorated function
        """
        def decorator(func: Callable[..., T]) -> Callable[..., T]:
            profile_name = name or func.__name__
            
            @functools.wraps(func)
            def wrapper(*args, **kwargs) -> T:
                with measure_time_silent() as timer:
                    result = func(*args, **kwargs)
                
                with self._lock:
                    self._calls[profile_name].append(timer.elapsed)
                
                return result
            
            return wrapper
        
        return decorator
    
    def get_stats(self, name: str) -> Optional[Dict[str, float]]:
        """Get statistics for a profiled function."""
        with self._lock:
            times = self._calls.get(name, [])
        
        if not times:
            return None
        
        return {
            'count': len(times),
            'total': sum(times),
            'avg': statistics.mean(times),
            'min': min(times),
            'max': max(times),
            'median': statistics.median(times),
            'std_dev': statistics.stdev(times) if len(times) > 1 else 0.0,
        }
    
    def get_all_stats(self) -> Dict[str, Dict[str, float]]:
        """Get statistics for all profiled functions."""
        result = {}
        for name in self._calls.keys():
            stats = self.get_stats(name)
            if stats is not None:
                result[name] = stats
        return result
    
    def clear(self, name: Optional[str] = None) -> None:
        """Clear profiling data."""
        with self._lock:
            if name:
                self._calls.pop(name, None)
            else:
                self._calls.clear()


def compare_implementations(
    implementations: Dict[str, Callable[..., Any]],
    test_data: Any = None,
    iterations: int = 100,
) -> BenchmarkComparison:
    """
    Convenience function to compare multiple implementations.
    
    Args:
        implementations: Dict mapping names to implementation functions
        test_data: Test data to pass to each implementation
        iterations: Number of iterations per implementation
    
    Returns:
        BenchmarkComparison with results
    """
    runner = BenchmarkRunner(warmup_iterations=3, verbose=True)
    
    if test_data is not None:
        comparison = runner.run_comparison(
            implementations,
            iterations=iterations,
            args=(test_data,) if not isinstance(test_data, tuple) else test_data,
        )
    else:
        comparison = runner.run_comparison(
            implementations,
            iterations=iterations,
        )
    
    return comparison


# Utility functions for common benchmarking scenarios

def benchmark_memory(func: Callable[..., Any], iterations: int = 10) -> Dict[str, Any]:
    """
    Benchmark memory usage of a function (if tracemalloc available).
    
    Args:
        func: Function to benchmark
        iterations: Number of iterations
    
    Returns:
        Dict with memory statistics
    """
    try:
        import tracemalloc
        tracemalloc.start()
        
        for _ in range(iterations):
            func()
        
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        return {
            'current_mb': current / 1024 / 1024,
            'peak_mb': peak / 1024 / 1024,
            'iterations': iterations,
        }
    except ImportError:
        return {'error': 'tracemalloc not available'}


def sleep_benchmark(milliseconds: float) -> None:
    """
    Utility function for testing - sleeps for specified milliseconds.
    
    Args:
        milliseconds: Time to sleep in milliseconds
    """
    time.sleep(milliseconds / 1000.0)
