/**
 * @file bit_utils.h
 * @brief 位操作工具库 - 提供完整的位操作功能
 * @author AllToolkit
 * @date 2026-04-24
 * 
 * 零外部依赖，纯 C 标准库实现
 * 支持 C99 及以上标准
 */

#ifndef BIT_UTILS_H
#define BIT_UTILS_H

#include <stdint.h>
#include <stdbool.h>
#include <stddef.h>

#ifdef __cplusplus
extern "C" {
#endif

/* ============================================================
 * 基本位操作
 * ============================================================ */

/**
 * @brief 设置指定位置的位（置1）
 * @param value 原始值
 * @param bit 位位置（0-基于最低位）
 * @return 设置后的值
 */
uint64_t bit_set(uint64_t value, uint8_t bit);

/**
 * @brief 清除指定位置的位（置0）
 * @param value 原始值
 * @param bit 位位置
 * @return 清除后的值
 */
uint64_t bit_clear(uint64_t value, uint8_t bit);

/**
 * @brief 切换指定位置的位（翻转）
 * @param value 原始值
 * @param bit 位位置
 * @return 切换后的值
 */
uint64_t bit_toggle(uint64_t value, uint8_t bit);

/**
 * @brief 测试指定位是否为1
 * @param value 原始值
 * @param bit 位位置
 * @return true 如果位为1，false 如果位为0
 */
bool bit_test(uint64_t value, uint8_t bit);

/**
 * @brief 设置指定位为指定值
 * @param value 原始值
 * @param bit 位位置
 * @param set_value 要设置的值（true=1, false=0）
 * @return 修改后的值
 */
uint64_t bit_set_value(uint64_t value, uint8_t bit, bool set_value);

/* ============================================================
 * 位计数
 * ============================================================ */

/**
 * @brief 计算置位数量（popcount/汉明重量）
 * @param value 输入值
 * @return 置位数量
 */
uint8_t bit_count(uint64_t value);

/**
 * @brief 计算清零位数量
 * @param value 输入值
 * @return 清零位数量
 */
uint8_t bit_count_zero(uint64_t value);

/**
 * @brief 计算奇偶校验位
 * @param value 输入值
 * @return true 表示奇数个1，false 表示偶数个1
 */
bool bit_parity(uint64_t value);

/* ============================================================
 * 位查找
 * ============================================================ */

/**
 * @brief 查找最低有效位的位置（LSB）
 * @param value 输入值
 * @return LSB位置（0-63），如果value为0返回-1
 */
int8_t bit_find_first_set(uint64_t value);

/**
 * @brief 查找最高有效位的位置（MSB）
 * @param value 输入值
 * @return MSB位置（0-63），如果value为0返回-1
 */
int8_t bit_find_last_set(uint64_t value);

/**
 * @brief 查找最低清零位的位置
 * @param value 输入值
 * @return 最低清零位位置，如果全为1返回-1
 */
int8_t bit_find_first_zero(uint64_t value);

/**
 * @brief 查找最高清零位的位置
 * @param value 输入值
 * @return 最高清零位位置，如果全为1返回-1
 */
int8_t bit_find_last_zero(uint64_t value);

/* ============================================================
 * 位反转和旋转
 * ============================================================ */

/**
 * @brief 反转所有位
 * @param value 输入值
 * @return 位反转后的值
 */
uint64_t bit_reverse(uint64_t value);

/**
 * @brief 反转指定宽度的位
 * @param value 输入值
 * @param width 位宽度（1-64）
 * @return 反转后的值（仅低width位有效）
 */
uint64_t bit_reverse_n(uint64_t value, uint8_t width);

/**
 * @brief 左旋转
 * @param value 输入值
 * @param shift 旋转位数
 * @param width 数据宽度（1-64）
 * @return 旋转后的值
 */
uint64_t bit_rotate_left(uint64_t value, uint8_t shift, uint8_t width);

/**
 * @brief 右旋转
 * @param value 输入值
 * @param shift 旋转位数
 * @param width 数据宽度（1-64）
 * @return 旋转后的值
 */
uint64_t bit_rotate_right(uint64_t value, uint8_t shift, uint8_t width);

/* ============================================================
 * 位掩码
 * ============================================================ */

/**
 * @brief 生成低位掩码（低n位全为1）
 * @param n 位数
 * @return 掩码值
 */
uint64_t bit_mask_low(uint8_t n);

/**
 * @brief 生成高位掩码（高n位全为1）
 * @param n 位数
 * @return 掩码值
 */
uint64_t bit_mask_high(uint8_t n);

/**
 * @brief 生成范围掩码（从start到end的位全为1）
 * @param start 起始位（包含）
 * @param end 结束位（包含）
 * @return 掩码值
 */
uint64_t bit_mask_range(uint8_t start, uint8_t end);

/**
 * @brief 提取指定位范围
 * @param value 输入值
 * @param start 起始位
 * @param end 结束位
 * @return 提取的值
 */
uint64_t bit_extract(uint64_t value, uint8_t start, uint8_t end);

/**
 * @brief 插入值到位范围
 * @param value 目标值
 * @param insert 要插入的值
 * @param start 起始位
 * @param end 结束位
 * @return 插入后的值
 */
uint64_t bit_insert(uint64_t value, uint64_t insert, uint8_t start, uint8_t end);

/* ============================================================
 * 字节序转换
 * ============================================================ */

/**
 * @brief 反转字节序
 * @param value 输入值
 * @return 字节反转后的值
 */
uint16_t bit_swap16(uint16_t value);
uint32_t bit_swap32(uint32_t value);
uint64_t bit_swap64(uint64_t value);

/**
 * @brief 小端到大端转换
 */
uint16_t bit_le_to_be16(uint16_t value);
uint32_t bit_le_to_be32(uint32_t value);
uint64_t bit_le_to_be64(uint64_t value);

/**
 * @brief 大端到小端转换
 */
uint16_t bit_be_to_le16(uint16_t value);
uint32_t bit_be_to_le32(uint32_t value);
uint64_t bit_be_to_le64(uint64_t value);

/* ============================================================
 * 位字段操作
 * ============================================================ */

/**
 * @brief 读取位字段
 * @param value 源值
 * @param offset 位偏移
 * @param width 字段宽度
 * @return 字段值
 */
uint64_t bit_field_read(uint64_t value, uint8_t offset, uint8_t width);

/**
 * @brief 写入位字段
 * @param value 目标值
 * @param field_val 字段值
 * @param offset 位偏移
 * @param width 字段宽度
 * @return 写入后的值
 */
uint64_t bit_field_write(uint64_t value, uint64_t field_val, uint8_t offset, uint8_t width);

/* ============================================================
 * 位向量操作
 * ============================================================ */

/**
 * @brief 位向量结构
 */
typedef struct {
    uint8_t *data;      /**< 数据存储 */
    size_t size;        /**< 位数 */
    size_t capacity;    /**< 字节容量 */
} BitVector;

/**
 * @brief 创建位向量
 * @param size 位数
 * @return 位向量指针，失败返回NULL
 */
BitVector* bit_vector_create(size_t size);

/**
 * @brief 销毁位向量
 * @param bv 位向量指针
 */
void bit_vector_destroy(BitVector *bv);

/**
 * @brief 获取位
 * @param bv 位向量指针
 * @param index 位索引
 * @return 位值（0或1），失败返回-1
 */
int bit_vector_get(const BitVector *bv, size_t index);

/**
 * @brief 设置位
 * @param bv 位向量指针
 * @param index 位索引
 * @param value 位值（0或1）
 * @return 成功返回0，失败返回-1
 */
int bit_vector_set(BitVector *bv, size_t index, bool value);

/**
 * @brief 切换位
 * @param bv 位向量指针
 * @param index 位索引
 * @return 切换后的位值
 */
int bit_vector_toggle(BitVector *bv, size_t index);

/**
 * @brief 填充所有位
 * @param bv 位向量指针
 * @param value 填充值
 */
void bit_vector_fill(BitVector *bv, bool value);

/**
 * @brief 计算置位数量
 * @param bv 位向量指针
 * @return 置位数量
 */
size_t bit_vector_count(const BitVector *bv);

/**
 * @brief 调整大小
 * @param bv 位向量指针
 * @param new_size 新大小
 * @return 成功返回0，失败返回-1
 */
int bit_vector_resize(BitVector *bv, size_t new_size);

/* ============================================================
 * 实用函数
 * ============================================================ */

/**
 * @brief 判断是否为2的幂
 * @param value 输入值
 * @return true 如果是2的幂
 */
bool bit_is_power_of_two(uint64_t value);

/**
 * @brief 向上取整到最近的2的幂
 * @param value 输入值
 * @return 大于等于value的最小2的幂
 */
uint64_t bit_next_power_of_two(uint64_t value);

/**
 * @brief 向下取整到最近的2的幂
 * @param value 输入值
 * @return 小于等于value的最大2的幂
 */
uint64_t bit_prev_power_of_two(uint64_t value);

/**
 * @brief 计算值的有效位数宽度
 * @param value 输入值
 * @return 有效位数
 */
uint8_t bit_width(uint64_t value);

/**
 * @brief Gray码转换：二进制 -> Gray码
 * @param value 二进制值
 * @return Gray码值
 */
uint64_t bit_binary_to_gray(uint64_t value);

/**
 * @brief Gray码转换：Gray码 -> 二进制
 * @param gray Gray码值
 * @return 二进制值
 */
uint64_t bit_gray_to_binary(uint64_t gray);

/**
 * @brief 将位转换为字符串
 * @param value 输入值
 * @param buffer 输出缓冲区（至少65字节）
 * @param width 显示宽度（1-64）
 * @return 缓冲区指针
 */
char* bit_to_string(uint64_t value, char *buffer, uint8_t width);

/**
 * @brief 从字符串解析位
 * @param str 输入字符串
 * @param value 输出值指针
 * @return 成功返回0，失败返回-1
 */
int bit_from_string(const char *str, uint64_t *value);

#ifdef __cplusplus
}
#endif

#endif /* BIT_UTILS_H */