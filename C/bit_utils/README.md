# Bit Utils - C 位操作工具库

完整的位操作工具库，提供丰富的位操作功能，零外部依赖。

## 功能概览

### 基本位操作
- `bit_set` - 设置位（置1）
- `bit_clear` - 清除位（置0）
- `bit_toggle` - 切换位（翻转）
- `bit_test` - 测试位是否为1
- `bit_set_value` - 设置位为指定值

### 位计数
- `bit_count` - 计算置位数量（popcount/汉明重量）
- `bit_count_zero` - 计算清零位数量
- `bit_parity` - 计算奇偶校验位

### 位查找
- `bit_find_first_set` - 查找最低有效位位置（LSB）
- `bit_find_last_set` - 查找最高有效位位置（MSB）
- `bit_find_first_zero` - 查找最低清零位位置
- `bit_find_last_zero` - 查找最高清零位位置

### 位反转和旋转
- `bit_reverse` - 反转所有位
- `bit_reverse_n` - 反转指定宽度位
- `bit_rotate_left` - 循环左移
- `bit_rotate_right` - 循环右移

### 位掩码
- `bit_mask_low` - 生成低位掩码
- `bit_mask_high` - 生成高位掩码
- `bit_mask_range` - 生成范围掩码
- `bit_extract` - 提取位范围
- `bit_insert` - 插入值到位范围

### 字节序转换
- `bit_swap16/32/64` - 反转字节序
- `bit_le_to_be16/32/64` - 小端到大端
- `bit_be_to_le16/32/64` - 大端到小端

### 位字段操作
- `bit_field_read` - 读取位字段
- `bit_field_write` - 写入位字段

### 位向量
- `bit_vector_create` - 创建位向量
- `bit_vector_destroy` - 销毁位向量
- `bit_vector_get/set/toggle` - 位操作
- `bit_vector_fill` - 填充所有位
- `bit_vector_count` - 计算置位数量
- `bit_vector_resize` - 调整大小

### 实用函数
- `bit_is_power_of_two` - 判断是否为2的幂
- `bit_next_power_of_two` - 向上取整到最近的2的幂
- `bit_prev_power_of_two` - 向下取整到最近的2的幂
- `bit_width` - 计算有效位数宽度
- `bit_binary_to_gray` - 二进制转Gray码
- `bit_gray_to_binary` - Gray码转二进制
- `bit_to_string` - 位转字符串
- `bit_from_string` - 字符串转位

## 编译

```bash
# 编译所有
make all

# 编译并运行测试
make test

# 编译并运行示例
make examples

# 清理
make clean
```

## 使用方法

```c
#include "bit_utils.h"

int main() {
    uint64_t value = 0;
    
    // 设置位
    value = bit_set(value, 0);   // 设置第0位 -> 1
    value = bit_set(value, 3);   // 设置第3位 -> 0b1001
    
    // 测试位
    if (bit_test(value, 0)) {
        printf("第0位已设置\n");
    }
    
    // 计算置位数量
    printf("置位数量: %d\n", bit_count(value));
    
    // 位反转
    uint64_t reversed = bit_reverse(value);
    
    // 创建位向量
    BitVector *bv = bit_vector_create(1024);
    bit_vector_set(bv, 0, true);
    bit_vector_set(bv, 100, true);
    printf("置位数量: %zu\n", bit_vector_count(bv));
    bit_vector_destroy(bv);
    
    return 0;
}
```

## 测试

包含 46 个单元测试，覆盖所有功能模块：

- 基本位操作测试
- 位计数测试
- 位查找测试
- 位反转和旋转测试
- 位掩码测试
- 字节序转换测试
- 位字段操作测试
- 位向量测试
- 实用函数测试

## 示例

包含 10 个完整示例：

1. 基本位操作演示
2. 位计数和奇偶校验
3. 位查找应用
4. 位反转和旋转
5. 位掩码操作
6. 字节序转换
7. 位字段操作（寄存器模拟）
8. 位向量使用
9. 实用函数展示
10. 综合应用 - 权限系统

## 文件结构

```
bit_utils/
├── bit_utils.h      # 头文件
├── bit_utils.c      # 实现文件
├── test_bit_utils.c # 测试文件
├── examples.c       # 示例文件
├── Makefile         # 构建文件
└── README.md        # 说明文档
```

## 特性

- **零外部依赖**: 纯 C 标准库实现
- **跨平台**: 支持 Linux/Windows/Mac
- **高性能**: 使用高效算法（Brian Kernighan、分治法等）
- **完整测试**: 46 个单元测试
- **丰富示例**: 10 个完整使用示例
- **C99 支持**: 兼容 C99 及以上标准

## 作者

AllToolkit - 2026-04-24