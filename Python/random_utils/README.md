# Random Utils 🎲

**Python 随机工具模块 - 零依赖，生产就绪**

---

## 📖 概述

`random_utils` 是一个全面的 Python 随机工具模块，提供安全随机数生成、UUID、随机字符串、随机选择、洗牌、随机数据生成等功能。所有实现均使用 Python 标准库（`random`、`secrets`、`uuid` 等），零外部依赖。

### ✨ 特性

- **零依赖** - 仅使用 Python 标准库
- **加密安全** - 支持 `secrets` 模块的安全随机生成
- **多种类型** - 随机数、字符串、密码、UUID、日期时间等
- **随机数据** - 邮箱、电话、IP 地址、颜色等模拟数据
- **游戏工具** - 骰子、硬币、扑克牌
- **可重现** - 支持种子随机数生成器
- **类型安全** - 完整的类型注解
- **生产就绪** - 完整的错误处理和边界检查
- **全面测试** - 100+ 测试用例覆盖所有功能

---

## 📦 安装

无需安装！直接复制 `mod.py` 到你的项目即可使用。

```bash
# 从 AllToolkit 复制
cp AllToolkit/Python/random_utils/mod.py your_project/

# 或者克隆整个仓库
git clone https://github.com/ayukyo/alltoolkit.git
```

---

## 🚀 快速开始

```python
from mod import (
    random_string, random_password, random_uuid,
    random_int, random_choice, random_datetime,
    secure_random_bytes, random_token
)

# 随机字符串
print(random_string(16))
# 输出：aB3dE7fG9hJ2kL4m

# 随机密码
print(random_password(16))
# 输出：Kx9#mP2$vL5@nQ8w

# UUID
print(random_uuid())
# 输出：550e8400-e29b-41d4-a716-446655440000

# 安全随机字节
print(secure_random_bytes(16).hex())
# 输出：a1b2c3d4e5f6789012345678abcdef90

# 随机选择
print(random_choice(['apple', 'banana', 'cherry']))
# 输出：banana
```

---

## 📚 API 参考

### 安全随机生成

#### `secure_random_bytes(n)`

生成 n 个加密安全的随机字节。

```python
data = secure_random_bytes(16)
print(data.hex())
# 'a1b2c3d4e5f6789012345678abcdef90'
```

#### `secure_random_int(lower, upper)`

生成 [lower, upper] 范围内的加密安全随机整数。

```python
secure_random_int(1, 100)
# 42
```

#### `secure_random_float()`

生成 [0.0, 1.0) 范围内的加密安全随机浮点数。

```python
secure_random_float()
# 0.7234567890123456
```

#### `secure_random_choice(seq)`

从序列中加密安全地选择一个元素。

```python
secure_random_choice(['a', 'b', 'c'])
# 'b'
```

#### `secure_random_sample(seq, k)`

从序列中加密安全地选择 k 个唯一元素。

```python
secure_random_sample([1, 2, 3, 4, 5], 3)
# [3, 1, 5]
```

---

### 随机字符串生成

#### `random_string(length=16, charset=DEFAULT_CHARSET_ALPHANUMERIC, secure=True)`

生成指定长度的随机字符串。

```python
random_string(10)
# 'aB3dE7fG9h'

random_string(8, charset="abc")
# 'bacbcaba'

random_string(10, secure=False)  # 使用普通随机
# 'xY9zA2bC4d'
```

#### `random_password(length=16, use_lowercase=True, use_uppercase=True, use_digits=True, use_special=True, secure=True)`

生成随机密码。

```python
random_password(12)
# 'Kx9#mP2$vL5@'

random_password(16, use_special=False)
# 'aB3dE7fG9hJ2kL4m'

random_password(8, use_lowercase=False, use_uppercase=False)
# '37591824'
```

#### `random_token(length=32, url_safe=True)`

生成随机令牌（适合认证/验证）。

```python
random_token()
# 'xY9zA2bC4dEfGhIjKlMnOpQrStUvWx'

random_token(url_safe=False)
# 'a1b2c3d4e5f6789012345678abcdef90'
```

#### `random_uuid(version=4)`

生成随机 UUID。

```python
random_uuid()  # version 4
# '550e8400-e29b-41d4-a716-446655440000'

random_uuid(version=1)  # version 1 (基于时间)
# 'c232ab28-9405-11ef-8e03-0242ac120002'
```

#### `random_slug(length=8, separator='-')`

生成随机 slug（URL 友好标识符）。

```python
random_slug()
# 'a1b2-c3d4-e5f6-g7h8-i9j0-k1l2-m3n4-o5p6'

random_slug(length=4, separator='_')
# 'abc1_def2_ghi3_jkl4'
```

---

### 随机数生成

#### `random_int(lower, upper, secure=False)`

生成 [lower, upper] 范围内的随机整数。

```python
random_int(1, 100)
# 42

random_int(1, 100, secure=True)
# 73
```

#### `random_float(lower=0.0, upper=1.0, secure=False)`

生成 [lower, upper) 范围内的随机浮点数。

```python
random_float()
# 0.7234567890123456

random_float(10.0, 20.0)
# 15.67890123456789
```

#### `random_gauss(mean=0.0, std=1.0)`

从高斯（正态）分布生成随机浮点数。

```python
random_gauss()
# -0.23456789012345678

random_gauss(mean=100, std=15)
# 98.76543210987654
```

#### `random_bool(probability=0.5)`

生成随机布尔值。

```python
random_bool()
# True

random_bool(0.9)  # 90% 概率为 True
# True

random_bool(0.0)  # 总是 False
# False
```

---

### 随机选择和洗牌

#### `random_choice(seq, secure=False)`

从序列中选择一个随机元素。

```python
random_choice([1, 2, 3, 4, 5])
# 3
```

#### `random_sample(seq, k, secure=False)`

从序列中选择 k 个唯一随机元素。

```python
random_sample([1, 2, 3, 4, 5, 6], 3)
# [4, 1, 6]
```

#### `random_shuffle(seq, secure=False)`

原地洗牌列表。

```python
items = [1, 2, 3, 4, 5]
random_shuffle(items)
print(items)
# [3, 1, 5, 2, 4]
```

#### `weighted_choice(items, weights)`

按权重选择随机元素。

```python
weighted_choice(['win', 'lose'], [0.9, 0.1])
# 'win' (90% 概率)
```

---

### 随机日期时间

#### `random_datetime(start=None, end=None)`

生成 start 和 end 之间的随机日期时间。

```python
from datetime import datetime

start = datetime(2020, 1, 1)
end = datetime(2025, 12, 31)
random_datetime(start, end)
# datetime(2023, 7, 15, 14, 30, 45)
```

#### `random_date(start_year=1970, end_year=None)`

生成随机日期。

```python
random_date(2000, 2020)
# datetime(2015, 6, 23, 10, 15, 30)
```

#### `random_time()`

生成一天中的随机时间。

```python
random_time()
# datetime(2000, 1, 1, 14, 30, 45)
```

---

### 随机数据生成

#### `random_email(domain="example.com")`

生成随机邮箱地址。

```python
random_email()
# 'abc123xyz@example.com'

random_email('company.com')
# 'user456@company.com'
```

#### `random_phone(country_code="+1", length=10)`

生成随机电话号码。

```python
random_phone()
# '+15551234567'

random_phone('+86', 11)
# '+8613800138000'
```

#### `random_ipv4(private=False)`

生成随机 IPv4 地址。

```python
random_ipv4()
# '203.45.67.89'

random_ipv4(private=True)
# '192.168.1.100'
```

#### `random_color(format='hex')`

生成随机颜色。

```python
random_color('hex')
# '#a1b2c3'

random_color('rgb')
# 'rgb(123, 45, 67)'

random_color('hsl')
# 'hsl(180, 50%, 60%)'
```

---

### 随机 ID 生成

#### `random_id(prefix="", length=12, separator="_", timestamp=False)`

生成随机唯一标识符。

```python
random_id("user")
# 'user_abc123def456'

random_id("order", timestamp=True)
# 'order_1703275200000_xyz789'
```

#### `random_correlation_id()`

生成随机关联/追踪 ID。

```python
random_correlation_id()
# 'corr-550e8400-e29b-41d4-a716-446655440000'
```

#### `random_request_id()`

生成随机请求 ID。

```python
random_request_id()
# 'req-a1b2c3d4e5f67890'
```

---

### 种子随机数

#### `SeededRandom(seed)`

可重现的随机数生成器。

```python
rng = SeededRandom(42)
print(rng.random_string(10))
# 'xY9zA2bC4d'

rng2 = SeededRandom(42)
print(rng2.random_string(10))
# 'xY9zA2bC4d' (相同结果!)

rng.random_int(1, 100)
# 82

rng.random_choice(['a', 'b', 'c'])
# 'b'

rng.random_shuffle([1, 2, 3, 4, 5])
# [3, 1, 5, 2, 4]
```

---

### 数学工具

#### `random_point_2d(min_x, max_x, min_y, max_y)`

生成随机 2D 点。

```python
random_point_2d()
# (0.543, 0.876)

random_point_2d(0, 100, 0, 100)
# (45.67, 89.12)
```

#### `random_point_3d(min_x, max_x, min_y, max_y, min_z, max_z)`

生成随机 3D 点。

```python
random_point_3d()
# (0.543, 0.876, 0.234)
```

#### `random_vector(length, min_val, max_val)`

生成随机向量。

```python
random_vector(3)
# [0.123, -0.456, 0.789]
```

#### `random_matrix(rows, cols, min_val, max_val)`

生成随机矩阵。

```python
random_matrix(2, 3)
# [[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]]
```

---

### 游戏工具

#### `roll_dice(sides=6, count=1)`

掷骰子。

```python
roll_dice(6, 2)  # 2d6
# [4, 3]

roll_dice(20, 1)  # 1d20
# [17]
```

#### `roll_d20()`

掷 20 面骰子（D&D 风格）。

```python
roll_d20()
# 17
```

#### `coin_flip()`

抛硬币。

```python
coin_flip()
# 'heads' 或 'tails'
```

#### `draw_card(deck_type='standard')`

从牌组中抽牌。

```python
draw_card()
# 'A♠'

draw_card('short')  # 短牌组 (32 张)
# 'K♥'
```

---

## 📝 示例

查看 `examples/` 目录获取更多使用示例：

- `basic_usage.py` - 基本用法示例
- `secure_tokens.py` - 安全令牌生成
- `test_data.py` - 测试数据生成
- `games.py` - 游戏工具示例

---

## 🧪 运行测试

```bash
cd random_utils
python random_utils_test.py
```

测试覆盖：
- 安全随机生成
- 随机字符串和密码
- 随机数生成
- 选择和洗牌
- 日期时间生成
- 数据生成（邮箱、电话、IP、颜色）
- ID 生成
- 种子随机数
- 数学工具
- 游戏工具
- 错误处理
- 唯一性验证

---

## 🔒 安全注意事项

1. **加密安全**：对于安全敏感的应用（密码、令牌、密钥），使用 `secure=True` 参数或 `secure_*` 函数。

2. **密码生成**：`random_password` 使用加密安全随机（默认），适合生成临时密码或 API 密钥。

3. **UUID**：`random_uuid()` 使用 `uuid.uuid4()`，适合生成唯一标识符。

4. **可重现性**：使用 `SeededRandom` 进行测试或需要可重现结果的场景。不要用于安全用途。

5. **随机性质量**：
   - 安全用途：使用 `secrets` 模块（`secure_*` 函数）
   - 一般用途：使用 `random` 模块（默认函数）
   - 测试/调试：使用 `SeededRandom`

---

## 📊 性能提示

- `secure_*` 函数比非安全版本慢，但对安全至关重要
- 批量生成时，预分配列表比追加更高效
- `SeededRandom` 比普通 `random` 稍慢，但提供可重现性

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

## 📄 许可证

MIT License
