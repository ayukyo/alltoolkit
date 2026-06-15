# LIS Utils 📊

最长上升子序列工具，使用 O(n log n) 高效算法。

## 特性

- ✅ **O(n log n)** - Patience 排序算法
- ✅ **LIS 序列** - 返回实际最长上升子序列
- ✅ **LDS/LNDS** - 下降/非下降子序列
- ✅ **多 LIS** - 所有等长 LIS
- ✅ **零依赖** - 仅使用 Python 标准库

## 快速开始

```python
from lis_utils import lis_length, lis_sequence

# 长度
seq = [10, 9, 2, 5, 3, 7, 101, 18]
length = lis_length(seq)
print(length)  # 4 ([2, 5, 7, 101] 或 [2, 3, 7, 101])

# 序列
result = lis_sequence(seq)
print(result)  # [2, 5, 7, 101]
```

## API 参考

| 函数 | 说明 |
|------|------|
| `lis_length(seq)` | LIS 长度 |
| `lis_sequence(seq)` | LIS 序列 |
| `lds_length(seq)` | LDS 长度 |
| `lnds_length(seq)` | LNDS 长度 |
| `count_lis(seq)` | LIS 数量 |
