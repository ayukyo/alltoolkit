"""
Pipeline Utils 使用示例

展示数据处理管道的各种用法：
1. 基础链式操作
2. 数据过滤和转换
3. 分组和聚合
4. 批量处理
5. 并行处理
6. 错误处理
7. 管道组合
8. 实际应用场景

作者: AllToolkit
日期: 2026-04-23
"""

import sys
import os
import time

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from pipeline_utils.mod import (
    Pipeline, PipelineBuilder,
    pipe, compose,
    create_filter_pipeline, create_map_pipeline
)


def section(title: str):
    """打印分节标题"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")


def example_basic_chain():
    """示例1: 基础链式操作"""
    section("1. 基础链式操作")
    
    # 简单的映射-过滤链
    result = (
        Pipeline([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        .map(lambda x: x * 2)
        .filter(lambda x: x > 10)
        .to_list()
    )
    print(f"映射后过滤: {result}")
    
    # 带取和跳过
    result = (
        Pipeline(range(1, 21))
        .map(lambda x: x ** 2)
        .skip(5)
        .take(5)
        .to_list()
    )
    print(f"跳过前5个，取后5个平方数: {result}")


def example_filter_transform():
    """示例2: 数据过滤和转换"""
    section("2. 数据过滤和转换")
    
    # 处理用户数据
    users = [
        {"name": "Alice", "age": 25, "city": "Beijing"},
        {"name": "Bob", "age": 30, "city": "Shanghai"},
        {"name": "Charlie", "age": 25, "city": "Beijing"},
        {"name": "Diana", "age": 35, "city": "Guangzhou"},
        {"name": "Eve", "age": 30, "city": "Shanghai"},
    ]
    
    # 筛选北京的用户，提取名字
    beijing_names = (
        Pipeline(users)
        .filter(lambda u: u["city"] == "Beijing")
        .map(lambda u: u["name"])
        .to_list()
    )
    print(f"北京的用户: {beijing_names}")
    
    # 按年龄分组
    by_age = (
        Pipeline(users)
        .group_by(lambda u: u["age"])
        .run()
    )
    print(f"\n按年龄分组:")
    for age, group in sorted(by_age.items()):
        names = [u["name"] for u in group]
        print(f"  {age}岁: {names}")


def example_aggregation():
    """示例3: 分组和聚合"""
    section("3. 分组和聚合")
    
    # 销售数据
    sales = [
        {"product": "A", "region": "North", "amount": 100},
        {"product": "B", "region": "North", "amount": 200},
        {"product": "A", "region": "South", "amount": 150},
        {"product": "B", "region": "South", "amount": 250},
        {"product": "A", "region": "North", "amount": 180},
        {"product": "C", "region": "East", "amount": 300},
    ]
    
    # 按区域分组统计
    print("按区域统计销售额:")
    region_sales = (
        Pipeline(sales)
        .group_by(lambda s: s["region"])
        .run()
    )
    for region, items in sorted(region_sales.items()):
        total = sum(s["amount"] for s in items)
        print(f"  {region}: {total}")
    
    # 计算总销售额
    total = Pipeline(sales).map(lambda s: s["amount"]).sum()
    print(f"\n总销售额: {total}")
    
    # 找出销售额最高的产品
    top_product = (
        Pipeline(sales)
        .group_by(lambda s: s["product"])
        .run()
    )
    product_totals = {
        p: sum(s["amount"] for s in items)
        for p, items in top_product.items()
    }
    print(f"\n产品销售额: {product_totals}")


def example_batch_processing():
    """示例4: 批量处理"""
    section("4. 批量处理")
    
    # 模拟批量API调用
    def batch_api_call(items):
        """模拟批量API调用"""
        print(f"  处理批次: {items}")
        return [f"processed_{x}" for x in items]
    
    result = (
        Pipeline(range(1, 11))
        .batch(batch_api_call, batch_size=3)
        .to_list()
    )
    print(f"\n批量处理结果: {result}")
    
    # 分块处理
    print("\n分块示例:")
    chunks = (
        Pipeline(range(1, 10))
        .chunk(3)
        .to_list()
    )
    print(f"每3个一组: {chunks}")


def example_parallel_processing():
    """示例5: 并行处理"""
    section("5. 并行处理")
    
    def slow_operation(x):
        """模拟耗时操作"""
        time.sleep(0.1)
        return x ** 2
    
    # 串行处理
    start = time.time()
    result = (
        Pipeline(range(1, 6))
        .map(slow_operation)
        .to_list()
    )
    serial_time = time.time() - start
    print(f"串行处理结果: {result}, 耗时: {serial_time:.2f}s")
    
    # 并行处理
    start = time.time()
    result = (
        Pipeline(range(1, 6))
        .parallel_map(slow_operation, max_workers=5)
        .to_list()
    )
    parallel_time = time.time() - start
    print(f"并行处理结果: {result}, 耗时: {parallel_time:.2f}s")
    print(f"加速比: {serial_time/parallel_time:.2f}x")


def example_error_handling():
    """示例6: 错误处理"""
    section("6. 错误处理")
    
    def risky_divide(x):
        if x == 0:
            raise ValueError("不能除以零")
        return 100 / x
    
    # 带错误处理
    result = (
        Pipeline([10, 5, 0, 2, 0, 4])
        .try_catch(
            risky_divide,
            on_error=lambda x, e: f"Error({x})"
        )
        .to_list()
    )
    print(f"带错误处理的结果: {result}")
    
    # 条件分支
    result = (
        Pipeline([-3, -2, -1, 0, 1, 2, 3])
        .conditional(
            condition=lambda x: x >= 0,
            true_func=lambda x: f"positive({x})",
            false_func=lambda x: f"negative({abs(x)})"
        )
        .to_list()
    )
    print(f"条件分支结果: {result}")


def example_pipeline_composition():
    """示例7: 管道组合"""
    section("7. 管道组合")
    
    # 定义可复用的管道
    filter_even = Pipeline().filter(lambda x: x % 2 == 0)
    double = Pipeline().map(lambda x: x * 2)
    top_five = Pipeline().take(5)
    
    # 组合管道
    combined = filter_even.compose(double).compose(top_five)
    result = list(combined.run(range(1, 20)))
    print(f"过滤偶数 -> 翻倍 -> 取前5: {result}")
    
    # 使用 | 操作符
    combined2 = filter_even | double | top_five
    result2 = list(combined2.run(range(1, 20)))
    print(f"使用 | 操作符: {result2}")
    
    # 使用构建器
    builder = (
        PipelineBuilder()
        .filter(lambda x: x % 2 == 0)
        .map(lambda x: x * 2)
        .take(5)
    )
    
    pipeline1 = builder.build(range(1, 20))
    pipeline2 = builder.build(range(50, 70))
    
    print(f"\n构建器复用1: {list(pipeline1.run())}")
    print(f"构建器复用2: {list(pipeline2.run())}")


def example_text_processing():
    """示例8: 文本处理"""
    section("8. 文本处理")
    
    text = """
    Python is a programming language.
    It is widely used for web development.
    Python is also popular in data science.
    Many developers love Python.
    """
    
    # 词频统计
    word_freq = (
        Pipeline(text.split())
        .map(lambda w: w.lower().strip(".,!?"))
        .filter(lambda w: len(w) > 2)
        .group_by(lambda w: w)
        .run()
    )
    
    # 排序显示
    sorted_words = sorted(
        [(word, len(items)) for word, items in word_freq.items()],
        key=lambda x: x[1],
        reverse=True
    )
    
    print("词频统计:")
    for word, count in sorted_words[:10]:
        print(f"  {word}: {count}")


def example_data_cleaning():
    """示例9: 数据清洗"""
    section("9. 数据清洗")
    
    raw_data = [
        "  Alice  ",
        "",
        "Bob",
        "  ",
        "CHARLIE",
        "diana",
        None,
        "Eve  ",
    ]
    
    # 清洗流程：去除None -> strip -> 过滤空 -> 统一大小写
    cleaned = (
        Pipeline(raw_data)
        .filter(lambda x: x is not None)
        .map(lambda x: x.strip())
        .filter(lambda x: len(x) > 0)
        .map(lambda x: x.title())
        .unique()
        .sort()
        .to_list()
    )
    print(f"原始数据: {raw_data}")
    print(f"清洗后: {cleaned}")


def example_enumerate_and_zip():
    """示例10: 枚举和配对"""
    section("10. 枚举和配对")
    
    # 枚举
    result = (
        Pipeline(['a', 'b', 'c', 'd'])
        .enumerate(start=1)
        .to_list()
    )
    print(f"枚举: {result}")
    
    # 配对
    names = ['Alice', 'Bob', 'Charlie']
    scores = [85, 92, 78]
    result = (
        Pipeline(names)
        .zip_with(scores)
        .to_list()
    )
    print(f"配对: {result}")


def example_termination_operations():
    """示例11: 终止操作"""
    section("11. 终止操作")
    
    data = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
    
    print(f"数据: {data}")
    
    # 聚合统计
    pipeline = Pipeline(data)
    print(f"  数量: {pipeline.clone().count()}")
    print(f"  总和: {pipeline.clone().sum()}")
    print(f"  最小: {pipeline.clone().min()}")
    print(f"  最大: {pipeline.clone().max()}")
    print(f"  第一个: {pipeline.clone().first()}")
    print(f"  最后一个: {pipeline.clone().last()}")
    
    # 条件检查
    print(f"\n条件检查:")
    print(f"  是否有大于5的数: {Pipeline(data).any(lambda x: x > 5)}")
    print(f"  是否都大于0: {Pipeline(data).all(lambda x: x > 0)}")
    
    # 排序后去重
    unique_sorted = (
        Pipeline(data)
        .unique()
        .sort()
        .to_list()
    )
    print(f"\n去重排序: {unique_sorted}")


def example_functional_utils():
    """示例12: 函数式工具"""
    section("12. 函数式工具")
    
    # pipe: 从左到右
    calc = pipe(
        lambda x: x + 1,
        lambda x: x * 2,
        lambda x: x - 3
    )
    print(f"pipe(5) -> ((5+1)*2)-3 = {calc(5)}")
    
    # compose: 从右到左
    calc2 = compose(
        lambda x: x - 3,
        lambda x: x * 2,
        lambda x: x + 1
    )
    print(f"compose(5) -> ((5+1)*2)-3 = {calc2(5)}")


def example_tap_debugging():
    """示例13: 使用tap调试"""
    section("13. 使用tap调试")
    
    print("调试管道中间状态:")
    result = (
        Pipeline(range(1, 6))
        .tap(lambda x: print(f"  原始: {x}"))
        .map(lambda x: x * 2)
        .tap(lambda x: print(f"  翻倍后: {x}"))
        .filter(lambda x: x > 4)
        .tap(lambda x: print(f"  过滤后: {x}"))
        .to_list()
    )
    print(f"最终结果: {result}")


def example_flat_map():
    """示例14: 扁平映射"""
    section("14. 扁平映射")
    
    # 展开嵌套列表
    nested = [[1, 2], [3, 4, 5], [6], [7, 8, 9]]
    result = (
        Pipeline(nested)
        .flat_map(lambda x: x)
        .to_list()
    )
    print(f"展开嵌套列表: {result}")
    
    # 生成序列
    result = (
        Pipeline([1, 2, 3])
        .flat_map(lambda x: [x, x * 10])
        .to_list()
    )
    print(f"生成序列: {result}")


def main():
    """运行所有示例"""
    example_basic_chain()
    example_filter_transform()
    example_aggregation()
    example_batch_processing()
    example_parallel_processing()
    example_error_handling()
    example_pipeline_composition()
    example_text_processing()
    example_data_cleaning()
    example_enumerate_and_zip()
    example_termination_operations()
    example_functional_utils()
    example_tap_debugging()
    example_flat_map()
    
    print("\n" + "="*60)
    print("  所有示例完成!")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()