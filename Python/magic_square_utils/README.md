# Magic Square Utils 🔮

魔方阵工具集 - 提供完整的魔方阵生成、验证和变换功能。

## 功能特性

- **魔方阵验证** - 行/列/对角线和相等检查
- **奇数阶生成** - Siamese 方法
- **双偶数阶生成** - Strachey 方法
- **单偶数阶生成** - Conway 方法
- **魔方常数计算** - 自动计算常数
- **魔方阵变换** - 旋转、镜像
- **泛对角线魔方阵** - Pandiagonal 支持
- **素数魔方阵** - 素数元素生成

## 快速开始

```python
from magic_square_utils.mod import generate_magic_square, is_magic_square, magic_constant

# 生成 3阶魔方阵
square = generate_magic_square(3)
print(square)
# [[8, 1, 6],
#  [3, 5, 7],
#  [4, 9, 2]]

# 验证是否为魔方阵
valid = is_magic_square(square)
print(valid)  # True

# 计算魔方常数
constant = magic_constant(3)
print(f"3阶魔方常数: {constant}")  # 15
```

## 核心函数

### generate_magic_square(n)

```python
from magic_square_utils.mod import generate_magic_square

# 奇数阶 (3, 5, 7, ...)
square = generate_magic_square(5)

# 双偶数阶 (4, 8, 12, ...)
square = generate_magic_square(4)

# 单偶数阶 (6, 10, 14, ...)
square = generate_magic_square(6)
```

### is_magic_square(square)

```python
from magic_square_utils.mod import is_magic_square

square = [[8, 1, 6], [3, 5, 7], [4, 9, 2]]
valid = is_magic_square(square)  # True

# 验证泛对角线魔方阵
valid = is_magic_square(square, check_pandiagonal=True)
```

### magic_constant(n)

```python
from magic_square_utils.mod import magic_constant

# 魔方常数 = n × (n² + 1) ÷ 2
print(magic_constant(3))  # 15
print(magic_constant(4))  # 34
print(magic_constant(5))  # 65
```

## 魔方阵变换

```python
from magic_square_utils.mod import rotate_magic_square, mirror_magic_square

square = generate_magic_square(3)

# 旋转 90°
rotated = rotate_magic_square(square, angle=90)

# 镜像（水平）
mirrored = mirror_magic_square(square, axis='horizontal')
```

## 生成方法

| 阶数类型 | 方法 | 示例阶数 |
|----------|------|----------|
| 奇数阶 | Siamese | 3, 5, 7, 9 |
| 双偶数阶 | Strachey | 4, 8, 12 |
| 单偶数阶 | Conway | 6, 10, 14 |

## 泛对角线魔方阵

```python
from magic_square_utils.mod import generate_pandiagonal_magic_square

# 泛对角线魔方阵：所有对角线（包括断裂对角线）的和都相等
square = generate_pandiagonal_magic_square(5)
```

## 素数魔方阵

```python
from magic_square_utils.mod import generate_prime_magic_square

# 使用素数生成魔方阵
square = generate_prime_magic_square(3)
# 所有元素都是素数
```

## 魔方常数公式

```
M(n) = n × (n² + 1) / 2
```

| 阶数 | 魔方常数 |
|------|----------|
| 3 | 15 |
| 4 | 34 |
| 5 | 65 |
| 6 | 111 |
| 7 | 175 |
| 8 | 260 |

## 测试

```bash
python Python/magic_square_utils/magic_square_utils_test.py
```

## 许可证

MIT License