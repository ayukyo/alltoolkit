# Progress Bar Utils


Progress Bar Utils - 进度条工具集

提供终端进度条显示的实现，适用于：
- 命令行任务进度展示
- 文件下载/上传进度
- 数据处理进度
- 批量任务执行状态

特点：
- 零外部依赖（纯 Python 标准库）
- 支持多种进度条样式
- 支持多任务并行进度
- 支持自定义格式
- 支持预估剩余时间
- 线程安全


## 功能

### 类

- **ProgressBarStyle**: 进度条样式配置
  方法: classic, modern, minimal, blocks, arrows
- **ProgressBar**: 终端进度条

支持多种样式、预估时间、速率显示等功能。

示例:
    >>> # 基础用法
    >>> pb = ProgressBar(100, "下载文件")
    >>> for i in range(100):
    
  方法: current, total, progress, percent, elapsed ... (11 个方法)
- **MultiProgressBar**: 多任务并行进度条

同时显示多个任务的进度，适用于并发任务监控。

示例:
    >>> mpb = MultiProgressBar(3)
    >>> mpb
  方法: add_task, update, set_progress, remove_task, close
- **SpinnerProgress**: 旋转加载动画

适用于无法确定进度的长时间任务。

示例:
    >>> with SpinnerProgress("加载数据") as sp:
    
  方法: elapsed, start, stop
- **ProgressBarBuilder**: 进度条构建器

提供链式调用创建进度条。

示例:
    >>> pb = (ProgressBarBuilder()
    
  方法: total, desc, style, file, min_interval ... (6 个方法)

### 函数

- **progress(total, desc, style**) - 进度条上下文管理器
- **progress_range(start, stop, step**, ...) - 带进度条的 range 迭代器
- **progress_iter(iterable, desc, style**, ...) - 带进度条的迭代器
- **create_progress_bar(total, desc, style**) - 创建进度条的便捷函数
- **timed_progress(duration, desc, steps**) - 定时进度条
- **classic(cls**) - 经典样式
- **modern(cls**) - 现代样式
- **minimal(cls**) - 简约样式
- **blocks(cls**) - 方块样式
- **arrows(cls**) - 箭头样式

... 共 35 个函数

## 使用示例

```python
from mod import progress

# 使用 progress
result = progress()
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
