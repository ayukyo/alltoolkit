# matrix_utils - MATLAB 矩阵操作工具集

## 概述

`matrix_utils` 是一个全面的 MATLAB 矩阵操作工具集，提供常用的矩阵操作函数，零外部依赖。

## 功能列表

### 矩阵旋转
| 函数 | 描述 |
|------|------|
| `rotate90(A)` | 顺时针旋转90度 |
| `rotate180(A)` | 旋转180度 |
| `rotate270(A)` | 逆时针旋转90度 |

### 矩阵翻转
| 函数 | 描述 |
|------|------|
| `flip_horizontal(A)` | 水平翻转（左右镜像） |
| `flip_vertical(A)` | 垂直翻转（上下镜像） |

### 矩阵分块
| 函数 | 描述 |
|------|------|
| `block_split(A, block_size)` | 将矩阵分割成小块 |
| `block_merge(blocks)` | 将分块合并成完整矩阵 |

### 矩阵填充
| 函数 | 描述 |
|------|------|
| `pad_matrix(A, pad_size, ...)` | 矩阵填充，支持 constant/replicate/symmetric 模式 |

### 矩阵统计
| 函数 | 描述 |
|------|------|
| `matrix_stats(A)` | 计算矩阵统计信息（min, max, mean, median, std, var 等） |

### 矩阵切片
| 函数 | 描述 |
|------|------|
| `slice_extract(A, start_pos, slice_size)` | 提取矩阵切片 |
| `slice_insert(A, slice, start_pos)` | 插入切片到指定位置 |

### 矩阵卷积
| 函数 | 描述 |
|------|------|
| `convolve2d(A, kernel, ...)` | 二维卷积 |

### 滑动窗口
| 函数 | 描述 |
|------|------|
| `sliding_window(A, window_size, ...)` | 创建滑动窗口视图 |

### 对角线操作
| 函数 | 描述 |
|------|------|
| `diagonal(A, k)` | 提取对角线元素 |
| `diagonal_matrix(v, k)` | 从向量创建对角矩阵 |

### 矩阵运算
| 函数 | 描述 |
|------|------|
| `determinant(A)` | 计算行列式 |
| `inverse(A)` | 计算逆矩阵 |
| `pseudo_inverse(A)` | 计算伪逆（Moore-Penrose逆） |

### 矩阵分解
| 函数 | 描述 |
|------|------|
| `eigen(A)` | 特征值和特征向量 |
| `svd_decompose(A)` | 奇异值分解 |
| `qr_decompose(A)` | QR分解 |
| `lu_decompose(A)` | LU分解 |

### 矩阵属性
| 函数 | 描述 |
|------|------|
| `matrix_rank(A)` | 矩阵秩 |
| `matrix_norm(A, ...)` | 矩阵范数 |

### 矩阵创建
| 函数 | 描述 |
|------|------|
| `identity(n, m)` | 创建单位矩阵 |
| `zeros_matrix(m, n)` | 创建全零矩阵 |
| `ones_matrix(m, n)` | 创建全一矩阵 |
| `random_matrix(m, n, ...)` | 创建随机矩阵 |

### 其他
| 函数 | 描述 |
|------|------|
| `broadcast_add(A, v, dim)` | 广播加法 |
| `normalize(A, ...)` | 矩阵标准化（z-score/minmax） |
| `print_matrix(A, ...)` | 美化打印矩阵 |

## 使用示例

### 基本旋转和翻转

```matlab
% 创建测试矩阵
A = [1 2 3; 4 5 6];

% 顺时针旋转90度
B = matrix_utils.rotate90(A);
% B = [4 1; 5 2; 6 3]

% 水平翻转
B = matrix_utils.flip_horizontal(A);
% B = [3 2 1; 6 5 4]
```

### 矩阵分块

```matlab
% 分割4x4矩阵为2x2块
A = [1 2 3 4; 5 6 7 8; 9 10 11 12; 13 14 15 16];
blocks = matrix_utils.block_split(A, [2, 2]);

% 合并块
B = matrix_utils.block_merge(blocks);
```

### 矩阵填充

```matlab
A = [1 2; 3 4];

% 用0填充
B = matrix_utils.pad_matrix(A, [1, 1, 1, 1]);
% B = [0 0 0 0; 0 1 2 0; 0 3 4 0; 0 0 0 0]

% 复制边界填充
B = matrix_utils.pad_matrix(A, [1, 1, 1, 1], 'mode', 'replicate');
```

### 矩阵统计

```matlab
A = [1 2 3; 4 5 6];
stats = matrix_utils.matrix_stats(A);
fprintf('Min: %.2f, Max: %.2f, Mean: %.2f\n', stats.min, stats.max, stats.mean);
```

### 滑动窗口

```matlab
A = [1 2 3 4; 5 6 7 8; 9 10 11 12];
windows = matrix_utils.sliding_window(A, [2, 2]);
% 返回所有 2x2 的滑动窗口
```

### 矩阵分解

```matlab
A = [1 2 3; 4 5 6; 7 8 10];

% SVD分解
[U, S, V] = matrix_utils.svd_decompose(A);

% 特征值
[vals, vecs] = matrix_utils.eigen(A);
```

### 矩阵标准化

```matlab
A = [1 2 3; 4 5 6; 7 8 9];

% Z-score标准化
B = matrix_utils.normalize(A, 'method', 'zscore');

% MinMax标准化
B = matrix_utils.normalize(A, 'method', 'minmax');
```

## 运行测试

```matlab
% 在 MATLAB 中运行
cd MATLAB/matrix_utils
matrix_utils_test
```

## 依赖

- MATLAB R2016b 或更高版本
- 无外部依赖

## 版本历史

- v1.0.0 (2026-05-01): 初始版本，包含27个矩阵操作函数

## 作者

AllToolkit 自动生成