# Progress Utils


进度追踪工具模块

提供进度条、进度计算、时间估算等功能，零外部依赖。


## 功能

### 类

- **ProgressBar**: ASCII 进度条生成器

支持多种样式、时间估算、自定义格式。
  方法: render, update, set_progress, reset
- **ProgressTracker**: 高级进度追踪器

支持多阶段进度、子任务、回调等功能。
  方法: progress, percent, elapsed, eta, rate ... (13 个方法)
- **Spinner**: 终端旋转动画

用于不确定时间的等待过程。
  方法: update, start, stop
- **ETAEstimator**: ETA 估算器

基于历史数据估算剩余时间，使用指数加权移动平均。
  方法: update, estimate, get_rate, reset

### 函数

- **progress_bar(total, width, style**) - 创建进度条的快捷函数
- **track(iterable, total, description**, ...) - 跟踪可迭代对象的进度
- **format_duration(seconds**) - 格式化持续时间
- **format_rate(rate, unit**) - 格式化处理速率
- **render(self, current**) - 渲染进度条字符串
- **update(self, n**) - 更新进度
- **set_progress(self, current**) - 直接设置当前进度
- **reset(self**) - 重置进度条状态
- **progress(self**) - 当前进度（0-1）
- **percent(self**) - 当前百分比（0-100）

... 共 28 个函数

## 使用示例

```python
from mod import progress_bar

# 使用 progress_bar
result = progress_bar()
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
