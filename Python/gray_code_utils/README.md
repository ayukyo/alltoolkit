# Gray Code Utils


gray_code_utils/mod.py - Gray码工具集
零外部依赖，纯Python标准库实现

功能：
- 二进制Gray码生成（n位Gray码序列）
- 十进制转Gray码、Gray码转十进制
- 二进制转Gray码、Gray码转二进制
- 循环Gray码检测
- Gray码距离计算（相邻码距离）
- n维Gray码生成（用于多维空间遍历）
- Johnson计数器Gray码
- Gray码排序
- Gray码汉明重量
- 实际应用：位置编码器模拟、汉诺塔解法生成


## 功能

### 函数

- **binary_to_gray(binary**) - 将二进制数转换为Gray码
- **gray_to_binary(gray**) - 将Gray码转换为二进制数
- **decimal_to_gray(n**) - 将十进制数转换为Gray码（binary_to_gray的别名）
- **gray_to_decimal(gray**) - 将Gray码转换为十进制数（gray_to_binary的别名）
- **binary_to_gray_bits(bits**) - 将二进制位列表转换为Gray码位列表
- **gray_bits_to_binary(gray_bits**) - 将Gray码位列表转换为二进制位列表
- **generate_gray_codes(n**) - 生成n位Gray码序列
- **generate_gray_codes_iterative(n**) - 迭代方式生成n位Gray码序列
- **gray_code_generator(n**) - 生成n位Gray码的生成器（节省内存）
- **generate_gray_codes_binary(n**) - 生成n位Gray码序列（二进制字符串表示）

... 共 34 个函数

## 使用示例

```python
from mod import binary_to_gray

# 使用 binary_to_gray
result = binary_to_gray()
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
