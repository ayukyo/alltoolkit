# Pipeline Utils


Pipeline Utils - 数据处理管道工具包

提供可组合的数据处理管道，零外部依赖，仅使用 Python 标准库。

功能:
- Pipeline: 链式数据处理管道
- Step: 单个处理步骤（支持 map/filter/reduce/flat_map/group_by 等）
- 条件分支和错误处理
- 惰性求值支持
- 并行处理支持
- 管道组合和复用
- 内置常用步骤工厂

作者: AllToolkit
日期: 2026-04-23


## 功能

### 类

- **PipelineError**: 管道处理错误
- **StepError**: 步骤执行错误
- **ValidationError**: 验证错误
- **BaseStep**: 基础步骤类
  方法: name, process
- **MapStep**: 映射步骤 - 对每个元素应用函数
  方法: process
- **FilterStep**: 过滤步骤 - 筛选满足条件的元素
  方法: process
- **ReduceStep**: 归约步骤 - 将序列归约为单个值
  方法: process
- **FlatMapStep**: 扁平映射步骤 - 映射后展平
  方法: process
- **TakeStep**: 取前N个元素
  方法: process
- **SkipStep**: 跳过前N个元素
  方法: process
- **GroupByStep**: 分组步骤
  方法: process
- **SortStep**: 排序步骤
  方法: process
- **UniqueStep**: 去重步骤
  方法: process
- **ChunkStep**: 分块步骤 - 将序列分成固定大小的块
  方法: process
- **ZipStep**: 配对步骤 - 与另一序列配对
  方法: process
- **EnumerateStep**: 枚举步骤 - 添加索引
  方法: process
- **TapStep**: 旁路步骤 - 对每个元素执行操作但不修改数据
  方法: process
- **BatchStep**: 批量处理步骤 - 累积后批量处理
  方法: process
- **ConditionalStep**: 条件分支步骤
  方法: process
- **TryCatchStep**: 错误捕获步骤
  方法: process
- **ParallelMapStep**: 并行映射步骤 - 使用线程池并行处理
  方法: process
- **Pipeline**: 数据处理管道 - 支持链式组合多个处理步骤。

特性:
- 链式调用，声明式构建
- 惰性求值（默认）
- 支持并行处理
- 可组合和复用
- 支持错误处理

示例:
    >>> # 基础管道
    >>> result = (
    
  方法: map, filter, reduce, flat_map, take ... (34 个方法)
- **PipelineBuilder**: 管道构建器 - 用于创建可复用的管道模板。

示例:
    >>> # 创建管道模板
    >>> builder = PipelineBuilder()
    >>> builder
  方法: map, filter, reduce, flat_map, take ... (12 个方法)

### 函数

- **create_filter_pipeline(predicate**) - 创建过滤管道
- **create_map_pipeline(func**) - 创建映射管道
- **create_sort_pipeline(key, reverse**) - 创建排序管道
- **create_unique_pipeline(key**) - 创建去重管道
- **create_batch_pipeline(batch_func, batch_size**) - 创建批量处理管道
- **pipe(**) - 函数管道 - 从左到右依次应用函数。
- **compose(**) - 函数组合 - 从右到左依次应用函数。
- **name(self**)
- **process(self, data**)
- **process(self, data**)

... 共 74 个函数

## 使用示例

```python
from mod import create_filter_pipeline

# 使用 create_filter_pipeline
result = create_filter_pipeline()
```

## 测试

运行测试：

```bash
python *_test.py
```

## 文件结构

```
{module_name}/
├── mod.py              # 主模块
├── *_test.py           # 测试文件
├── README.md           # 本文档
└── examples/           # 示例代码
    └── usage_examples.py
```

---

**Last updated**: 2026-04-28
