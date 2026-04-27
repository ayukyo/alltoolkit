"""
Pipeline Utils 测试文件

测试覆盖：
- 所有步骤类的功能
- Pipeline 链式调用
- 惰性求值和立即求值
- 错误处理
- 并行处理
- 管道组合
- 便捷函数

作者: AllToolkit
日期: 2026-04-23
"""

import pytest
import time
from typing import List, Dict, Any
import sys
import os

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    Pipeline, PipelineBuilder, PipelineError, StepError,
    MapStep, FilterStep, ReduceStep, FlatMapStep, TakeStep, SkipStep,
    GroupByStep, SortStep, UniqueStep, ChunkStep, ZipStep, EnumerateStep,
    TapStep, BatchStep, ConditionalStep, TryCatchStep, ParallelMapStep,
    pipe, compose,
    create_filter_pipeline, create_map_pipeline, create_sort_pipeline,
    create_unique_pipeline, create_batch_pipeline
)


class TestMapStep:
    """测试 MapStep"""
    
    def test_basic_map(self):
        """测试基本映射"""
        step = MapStep(lambda x: x * 2)
        result = list(step.process([1, 2, 3]))
        assert result == [2, 4, 6]
    
    def test_map_with_name(self):
        """测试带名称的映射"""
        step = MapStep(lambda x: x.upper(), "ToUpper")
        assert step.name == "ToUpper"
        result = list(step.process(['a', 'b', 'c']))
        assert result == ['A', 'B', 'C']


class TestFilterStep:
    """测试 FilterStep"""
    
    def test_basic_filter(self):
        """测试基本过滤"""
        step = FilterStep(lambda x: x > 2)
        result = list(step.process([1, 2, 3, 4, 5]))
        assert result == [3, 4, 5]
    
    def test_filter_empty(self):
        """测试空结果"""
        step = FilterStep(lambda x: x > 100)
        result = list(step.process([1, 2, 3]))
        assert result == []


class TestReduceStep:
    """测试 ReduceStep"""
    
    def test_reduce_sum(self):
        """测试求和归约"""
        step = ReduceStep(lambda acc, x: acc + x, 0)
        result = step.process([1, 2, 3, 4, 5])
        assert result == 15
    
    def test_reduce_product(self):
        """测试求积归约"""
        step = ReduceStep(lambda acc, x: acc * x, 1)
        result = step.process([1, 2, 3, 4])
        assert result == 24
    
    def test_reduce_no_initial(self):
        """测试无初始值归约"""
        step = ReduceStep(lambda acc, x: acc + x)
        result = step.process([1, 2, 3])
        assert result == 6


class TestFlatMapStep:
    """测试 FlatMapStep"""
    
    def test_flat_map(self):
        """测试扁平映射"""
        step = FlatMapStep(lambda x: [x, x * 2])
        result = list(step.process([1, 2, 3]))
        assert result == [1, 2, 2, 4, 3, 6]
    
    def test_flat_map_empty(self):
        """测试空列表映射"""
        step = FlatMapStep(lambda x: [])
        result = list(step.process([1, 2, 3]))
        assert result == []


class TestTakeStep:
    """测试 TakeStep"""
    
    def test_take_basic(self):
        """测试取前N个"""
        step = TakeStep(3)
        result = list(step.process([1, 2, 3, 4, 5]))
        assert result == [1, 2, 3]
    
    def test_take_more_than_length(self):
        """测试取的数量超过长度"""
        step = TakeStep(10)
        result = list(step.process([1, 2, 3]))
        assert result == [1, 2, 3]


class TestSkipStep:
    """测试 SkipStep"""
    
    def test_skip_basic(self):
        """测试跳过前N个"""
        step = SkipStep(2)
        result = list(step.process([1, 2, 3, 4, 5]))
        assert result == [3, 4, 5]
    
    def test_skip_all(self):
        """测试跳过所有"""
        step = SkipStep(10)
        result = list(step.process([1, 2, 3]))
        assert result == []


class TestGroupByStep:
    """测试 GroupByStep"""
    
    def test_group_by_parity(self):
        """测试按奇偶分组"""
        step = GroupByStep(lambda x: x % 2)
        result = step.process([1, 2, 3, 4, 5])
        assert result[0] == [2, 4]
        assert result[1] == [1, 3, 5]
    
    def test_group_by_first_letter(self):
        """测试按首字母分组"""
        step = GroupByStep(lambda x: x[0])
        result = step.process(['apple', 'banana', 'apricot', 'cherry'])
        assert result['a'] == ['apple', 'apricot']
        assert result['b'] == ['banana']
        assert result['c'] == ['cherry']


class TestSortStep:
    """测试 SortStep"""
    
    def test_sort_ascending(self):
        """测试升序排序"""
        step = SortStep()
        result = step.process([3, 1, 4, 1, 5, 9, 2, 6])
        assert result == [1, 1, 2, 3, 4, 5, 6, 9]
    
    def test_sort_descending(self):
        """测试降序排序"""
        step = SortStep(reverse=True)
        result = step.process([3, 1, 4, 1, 5])
        assert result == [5, 4, 3, 1, 1]
    
    def test_sort_with_key(self):
        """测试按键排序"""
        step = SortStep(key=lambda x: x[1])
        result = step.process([('a', 3), ('b', 1), ('c', 2)])
        assert result == [('b', 1), ('c', 2), ('a', 3)]


class TestUniqueStep:
    """测试 UniqueStep"""
    
    def test_unique_basic(self):
        """测试基本去重"""
        step = UniqueStep()
        result = list(step.process([1, 2, 2, 3, 3, 3, 4]))
        assert result == [1, 2, 3, 4]
    
    def test_unique_with_key(self):
        """测试按键去重"""
        step = UniqueStep(key=lambda x: x[0])
        result = list(step.process([('a', 1), ('a', 2), ('b', 3)]))
        assert result == [('a', 1), ('b', 3)]


class TestChunkStep:
    """测试 ChunkStep"""
    
    def test_chunk_basic(self):
        """测试基本分块"""
        step = ChunkStep(3)
        result = list(step.process([1, 2, 3, 4, 5, 6, 7]))
        assert result == [[1, 2, 3], [4, 5, 6], [7]]
    
    def test_chunk_exact(self):
        """测试正好分块"""
        step = ChunkStep(2)
        result = list(step.process([1, 2, 3, 4]))
        assert result == [[1, 2], [3, 4]]
    
    def test_chunk_invalid_size(self):
        """测试无效块大小"""
        with pytest.raises(ValueError):
            ChunkStep(0)


class TestZipStep:
    """测试 ZipStep"""
    
    def test_zip_basic(self):
        """测试基本配对"""
        step = ZipStep(['a', 'b', 'c'])
        result = list(step.process([1, 2, 3]))
        assert result == [(1, 'a'), (2, 'b'), (3, 'c')]
    
    def test_zip_different_length(self):
        """测试不同长度配对"""
        step = ZipStep(['a', 'b'])
        result = list(step.process([1, 2, 3]))
        assert result == [(1, 'a'), (2, 'b')]


class TestEnumerateStep:
    """测试 EnumerateStep"""
    
    def test_enumerate_default(self):
        """测试默认枚举"""
        step = EnumerateStep()
        result = list(step.process(['a', 'b', 'c']))
        assert result == [(0, 'a'), (1, 'b'), (2, 'c')]
    
    def test_enumerate_custom_start(self):
        """测试自定义起始索引"""
        step = EnumerateStep(start=1)
        result = list(step.process(['a', 'b', 'c']))
        assert result == [(1, 'a'), (2, 'b'), (3, 'c')]


class TestTapStep:
    """测试 TapStep"""
    
    def test_tap_no_modification(self):
        """测试旁路操作不修改数据"""
        collected = []
        step = TapStep(lambda x: collected.append(x * 2))
        result = list(step.process([1, 2, 3]))
        assert result == [1, 2, 3]
        assert collected == [2, 4, 6]


class TestBatchStep:
    """测试 BatchStep"""
    
    def test_batch_basic(self):
        """测试基本批量处理"""
        def double_batch(items):
            return [x * 2 for x in items]
        
        step = BatchStep(double_batch, batch_size=2)
        result = list(step.process([1, 2, 3, 4, 5]))
        assert result == [2, 4, 6, 8, 10]


class TestConditionalStep:
    """测试 ConditionalStep"""
    
    def test_conditional_basic(self):
        """测试条件分支"""
        step = ConditionalStep(
            condition=lambda x: x % 2 == 0,
            true_step=lambda x: x * 2,
            false_step=lambda x: x * 3
        )
        result = list(step.process([1, 2, 3, 4]))
        assert result == [3, 4, 9, 8]


class TestTryCatchStep:
    """测试 TryCatchStep"""
    
    def test_try_catch_no_error(self):
        """测试无错误"""
        step = TryCatchStep(lambda x: x * 2)
        result = list(step.process([1, 2, 3]))
        assert result == [2, 4, 6]
    
    def test_try_catch_with_error_handler(self):
        """测试有错误处理器"""
        def risky(x):
            if x == 0:
                raise ValueError("zero")
            return 10 // x
        
        step = TryCatchStep(risky, on_error=lambda x, e: -1)
        result = list(step.process([1, 2, 0, 4]))
        assert result == [10, 5, -1, 2]
    
    def test_try_catch_no_error_handler(self):
        """测试无错误处理器时抛出异常"""
        def risky(x):
            if x == 0:
                raise ValueError("zero")
            return x
        
        step = TryCatchStep(risky)
        with pytest.raises(StepError):
            list(step.process([1, 0, 2]))


class TestParallelMapStep:
    """测试 ParallelMapStep"""
    
    def test_parallel_map_basic(self):
        """测试基本并行映射"""
        def slow_double(x):
            time.sleep(0.01)
            return x * 2
        
        step = ParallelMapStep(slow_double, max_workers=4)
        result = list(step.process([1, 2, 3, 4]))
        assert sorted(result) == [2, 4, 6, 8]


class TestPipeline:
    """测试 Pipeline"""
    
    def test_basic_chain(self):
        """测试基本链式调用"""
        result = (
            Pipeline([1, 2, 3, 4, 5])
            .map(lambda x: x * 2)
            .filter(lambda x: x > 4)
            .to_list()
        )
        assert result == [6, 8, 10]
    
    def test_map_filter_reduce(self):
        """测试映射过滤归约"""
        result = (
            Pipeline([1, 2, 3, 4, 5])
            .map(lambda x: x * 2)
            .filter(lambda x: x > 4)
            .reduce(lambda acc, x: acc + x, 0)
            .run()
        )
        assert result == 24  # 6 + 8 + 10
    
    def test_take_skip(self):
        """测试取和跳过"""
        result = (
            Pipeline([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
            .skip(2)
            .take(5)
            .to_list()
        )
        assert result == [3, 4, 5, 6, 7]
    
    def test_sort_unique(self):
        """测试排序和去重"""
        result = (
            Pipeline([3, 1, 2, 3, 2, 1, 4])
            .unique()
            .sort()
            .to_list()
        )
        assert result == [1, 2, 3, 4]
    
    def test_flat_map(self):
        """测试扁平映射"""
        result = (
            Pipeline([[1, 2], [3, 4], [5]])
            .flat_map(lambda x: x)
            .to_list()
        )
        assert result == [1, 2, 3, 4, 5]
    
    def test_group_by(self):
        """测试分组"""
        result = (
            Pipeline([1, 2, 3, 4, 5, 6])
            .group_by(lambda x: x % 2)
            .run()
        )
        assert result[0] == [2, 4, 6]
        assert result[1] == [1, 3, 5]
    
    def test_chunk(self):
        """测试分块"""
        result = (
            Pipeline([1, 2, 3, 4, 5, 6, 7])
            .chunk(3)
            .to_list()
        )
        assert result == [[1, 2, 3], [4, 5, 6], [7]]
    
    def test_enumerate(self):
        """测试枚举"""
        result = (
            Pipeline(['a', 'b', 'c'])
            .enumerate(start=1)
            .to_list()
        )
        assert result == [(1, 'a'), (2, 'b'), (3, 'c')]
    
    def test_zip_with(self):
        """测试配对"""
        result = (
            Pipeline([1, 2, 3])
            .zip_with(['a', 'b', 'c'])
            .to_list()
        )
        assert result == [(1, 'a'), (2, 'b'), (3, 'c')]
    
    def test_tap(self):
        """测试旁路操作"""
        collected = []
        result = (
            Pipeline([1, 2, 3])
            .tap(lambda x: collected.append(x * 2))
            .map(lambda x: x * 3)
            .to_list()
        )
        assert result == [3, 6, 9]
        assert collected == [2, 4, 6]
    
    def test_conditional(self):
        """测试条件分支"""
        result = (
            Pipeline([1, 2, 3, 4, 5])
            .conditional(
                condition=lambda x: x % 2 == 0,
                true_func=lambda x: f"even:{x}",
                false_func=lambda x: f"odd:{x}"
            )
            .to_list()
        )
        assert result == ["odd:1", "even:2", "odd:3", "even:4", "odd:5"]
    
    def test_lazy_vs_eager(self):
        """测试惰性和立即求值"""
        # 惰性求值
        lazy_pipeline = Pipeline([1, 2, 3]).map(lambda x: x * 2).lazy()
        lazy_result = lazy_pipeline.run()
        assert hasattr(lazy_result, '__iter__') and not isinstance(lazy_result, list)
        
        # 立即求值
        eager_pipeline = Pipeline([1, 2, 3]).map(lambda x: x * 2).eager()
        eager_result = eager_pipeline.run()
        assert isinstance(eager_result, list)
    
    def test_terminal_operations(self):
        """测试终止操作"""
        pipeline = Pipeline([1, 2, 3, 4, 5]).map(lambda x: x * 2)
        
        # to_list
        assert pipeline.clone().to_list() == [2, 4, 6, 8, 10]
        
        # first
        assert pipeline.clone().first() == 2
        
        # last
        assert pipeline.clone().last() == 10
        
        # count
        assert pipeline.clone().count() == 5
        
        # sum
        assert pipeline.clone().sum() == 30
        
        # min/max
        assert pipeline.clone().min() == 2
        assert pipeline.clone().max() == 10
    
    def test_any_all(self):
        """测试any和all"""
        # any
        assert Pipeline([1, 2, 3]).any(lambda x: x > 2)
        assert not Pipeline([1, 2, 3]).any(lambda x: x > 10)
        
        # all
        assert Pipeline([2, 4, 6]).all(lambda x: x % 2 == 0)
        assert not Pipeline([1, 2, 3]).all(lambda x: x > 1)
    
    def test_for_each(self):
        """测试for_each"""
        collected = []
        Pipeline([1, 2, 3]).for_each(lambda x: collected.append(x * 2))
        assert collected == [2, 4, 6]
    
    def test_iteration(self):
        """测试迭代器协议"""
        result = []
        for item in Pipeline([1, 2, 3]).map(lambda x: x * 2):
            result.append(item)
        assert result == [2, 4, 6]
    
    def test_run_with_source(self):
        """测试run方法传入数据源"""
        pipeline = Pipeline().map(lambda x: x * 2).filter(lambda x: x > 4)
        result = pipeline.run([1, 2, 3, 4, 5])
        assert list(result) == [6, 8, 10]
    
    def test_no_source_error(self):
        """测试没有数据源时报错"""
        pipeline = Pipeline().map(lambda x: x * 2)
        with pytest.raises(PipelineError):
            pipeline.run()
    
    def test_compose(self):
        """测试管道组合"""
        p1 = Pipeline().map(lambda x: x * 2)
        p2 = Pipeline().filter(lambda x: x > 5)
        combined = p1.compose(p2)
        result = combined.run([1, 2, 3, 4, 5])
        assert list(result) == [6, 8, 10]
    
    def test_or_operator(self):
        """测试|操作符"""
        p1 = Pipeline().map(lambda x: x * 2)
        p2 = Pipeline().filter(lambda x: x > 5)
        combined = p1 | p2
        result = combined.run([1, 2, 3, 4, 5])
        assert list(result) == [6, 8, 10]
    
    def test_clone(self):
        """测试克隆"""
        original = Pipeline([1, 2, 3]).map(lambda x: x * 2)
        cloned = original.clone()
        
        # 修改克隆不应影响原始
        cloned._steps.append(FilterStep(lambda x: x > 4))
        
        assert len(original._steps) == 1
        assert len(cloned._steps) == 2
    
    def test_repr(self):
        """测试字符串表示"""
        pipeline = Pipeline().map(lambda x: x).filter(lambda x: True)
        repr_str = repr(pipeline)
        assert "Map" in repr_str
        assert "Filter" in repr_str


class TestPipelineBuilder:
    """测试 PipelineBuilder"""
    
    def test_build(self):
        """测试构建管道"""
        builder = (
            PipelineBuilder()
            .map(lambda x: x * 2)
            .filter(lambda x: x > 4)
            .take(3)
        )
        pipeline = builder.build([1, 2, 3, 4, 5, 6, 7])
        result = list(pipeline.run())
        assert result == [6, 8, 10]
    
    def test_reuse_builder(self):
        """测试复用构建器"""
        builder = PipelineBuilder().map(lambda x: x * 2)
        
        pipeline1 = builder.build([1, 2, 3])
        pipeline2 = builder.build([4, 5, 6])
        
        assert list(pipeline1.run()) == [2, 4, 6]
        assert list(pipeline2.run()) == [8, 10, 12]


class TestConvenienceFunctions:
    """测试便捷函数"""
    
    def test_pipe(self):
        """测试pipe函数"""
        result = pipe(
            lambda x: x + 1,
            lambda x: x * 2,
            lambda x: x - 3
        )(5)
        assert result == 9  # ((5 + 1) * 2) - 3 = 9
    
    def test_compose(self):
        """测试compose函数"""
        result = compose(
            lambda x: x - 3,
            lambda x: x * 2,
            lambda x: x + 1
        )(5)
        assert result == 9  # ((5 + 1) * 2) - 3 = 9
    
    def test_create_filter_pipeline(self):
        """测试创建过滤管道"""
        pipeline = create_filter_pipeline(lambda x: x > 2)
        result = list(pipeline.run([1, 2, 3, 4, 5]))
        assert result == [3, 4, 5]
    
    def test_create_map_pipeline(self):
        """测试创建映射管道"""
        pipeline = create_map_pipeline(lambda x: x * 2)
        result = list(pipeline.run([1, 2, 3]))
        assert result == [2, 4, 6]
    
    def test_create_sort_pipeline(self):
        """测试创建排序管道"""
        pipeline = create_sort_pipeline()
        result = pipeline.run([3, 1, 2])
        assert result == [1, 2, 3]
    
    def test_create_unique_pipeline(self):
        """测试创建去重管道"""
        pipeline = create_unique_pipeline()
        result = list(pipeline.run([1, 2, 2, 3, 3, 3]))
        assert result == [1, 2, 3]
    
    def test_create_batch_pipeline(self):
        """测试创建批量处理管道"""
        def double_batch(items):
            return [x * 2 for x in items]
        
        pipeline = create_batch_pipeline(double_batch, batch_size=2)
        result = list(pipeline.run([1, 2, 3, 4]))
        assert result == [2, 4, 6, 8]


class TestComplexScenarios:
    """测试复杂场景"""
    
    def test_data_processing_pipeline(self):
        """测试数据处理管道"""
        data = [
            {"name": "Alice", "age": 25, "score": 85},
            {"name": "Bob", "age": 30, "score": 92},
            {"name": "Charlie", "age": 25, "score": 78},
            {"name": "Diana", "age": 35, "score": 95},
            {"name": "Eve", "age": 30, "score": 88},
        ]
        
        # 找出分数大于80的人，按年龄分组
        result = (
            Pipeline(data)
            .filter(lambda x: x["score"] > 80)
            .sort(key=lambda x: x["score"], reverse=True)
            .group_by(lambda x: x["age"])
            .run()
        )
        
        assert len(result[25]) == 1  # Alice
        assert len(result[30]) == 2  # Bob, Eve
        assert len(result[35]) == 1  # Diana
    
    def test_text_processing(self):
        """测试文本处理"""
        text = "Hello World Python Pipeline Utils"
        
        words = (
            Pipeline(text.split())
            .map(lambda x: x.lower())
            .filter(lambda x: len(x) > 5)
            .sort()
            .to_list()
        )
        
        assert words == ["pipeline", "python"]
    
    def test_chained_pipelines(self):
        """测试链式管道"""
        # 第一阶段：过滤和映射
        stage1 = Pipeline().filter(lambda x: x % 2 == 0).map(lambda x: x * 2)
        
        # 第二阶段：取和排序
        stage2 = Pipeline().take(5).sort(reverse=True)
        
        # 组合
        combined = stage1.compose(stage2)
        result = list(combined.run(range(1, 15)))
        assert result == [20, 16, 12, 8, 4]
    
    def test_error_recovery(self):
        """测试错误恢复"""
        def safe_divide(x):
            return 100 / x
        
        result = (
            Pipeline([1, 2, 0, 4, 5])
            .try_catch(safe_divide, on_error=lambda x, e: -1)
            .to_list()
        )
        
        assert result == [100.0, 50.0, -1, 25.0, 20.0]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])