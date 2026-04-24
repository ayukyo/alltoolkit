/**
 * @file examples.c
 * @brief 位操作工具库示例
 * 
 * 编译: gcc -o examples examples.c bit_utils.c
 * 运行: ./examples
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "bit_utils.h"

/* ============================================================
 * 示例1: 基本位操作
 * ============================================================ */
void example_basic_operations(void) {
    printf("\n=== 示例1: 基本位操作 ===\n\n");
    
    uint64_t value = 0;
    
    /* 设置位 */
    value = bit_set(value, 0);    /* 设置第0位 */
    value = bit_set(value, 3);    /* 设置第3位 */
    value = bit_set(value, 7);    /* 设置第7位 */
    printf("设置位 0, 3, 7 后: 0x%llX (二进制: ", value);
    char buf[65];
    bit_to_string(value, buf, 8);
    printf("%s)\n", buf);
    
    /* 测试位 */
    printf("位0是否设置: %s\n", bit_test(value, 0) ? "是" : "否");
    printf("位1是否设置: %s\n", bit_test(value, 1) ? "是" : "否");
    printf("位3是否设置: %s\n", bit_test(value, 3) ? "是" : "否");
    
    /* 清除位 */
    value = bit_clear(value, 3);
    printf("\n清除位3后: 0x%llX (二进制: ", value);
    bit_to_string(value, buf, 8);
    printf("%s)\n", buf);
    
    /* 切换位 */
    value = bit_toggle(value, 0);  /* 0 -> 1 的翻转 */
    value = bit_toggle(value, 1);  /* 翻转未设置的位 */
    printf("切换位0和1后: 0x%llX (二进制: ", value);
    bit_to_string(value, buf, 8);
    printf("%s)\n", buf);
    
    /* 设置特定位为指定值 */
    value = bit_set_value(value, 5, true);
    printf("设置位5为1: 0x%llX\n", value);
}

/* ============================================================
 * 示例2: 位计数和奇偶校验
 * ============================================================ */
void example_bit_counting(void) {
    printf("\n=== 示例2: 位计数和奇偶校验 ===\n\n");
    
    uint64_t value = 0xABCD;  /* 1010101111001101 */
    
    char buf[65];
    bit_to_string(value, buf, 16);
    printf("值: 0x%llX (二进制: %s)\n", value, buf);
    
    printf("置位数量 (popcount): %d\n", bit_count(value));
    printf("清零位数量: %d\n", bit_count_zero(value));
    printf("奇偶校验: %s\n", bit_parity(value) ? "奇" : "偶");
    
    /* 实用场景: 计算网络掩码中的主机位数 */
    uint32_t subnet_mask = 0xFFFFFF00;  /* /24 子网 */
    uint8_t host_bits = bit_count_zero(subnet_mask);
    printf("\n子网掩码 0x%08X (/24)\n", subnet_mask);
    printf("主机位数: %d\n", host_bits);
    printf("可用主机数: %u\n", (1u << host_bits) - 2);  /* 减去网络地址和广播地址 */
}

/* ============================================================
 * 示例3: 位查找
 * ============================================================ */
void example_bit_finding(void) {
    printf("\n=== 示例3: 位查找 ===\n\n");
    
    uint64_t value = 0x10101010;  /* 二进制: ...00010000000100000001000000010000 */
    
    char buf[65];
    bit_to_string(value, buf, 32);
    printf("值: 0x%llX (二进制: %s)\n", value, buf);
    
    printf("最低有效位位置 (LSB): %d\n", bit_find_first_set(value));
    printf("最高有效位位置 (MSB): %d\n", bit_find_last_set(value));
    printf("最低清零位位置: %d\n", bit_find_first_zero(value));
    printf("最高清零位位置: %d\n", bit_find_last_zero(value));
    
    /* 实用场景: 找到空闲的位槽 */
    uint64_t slots = 0b10110111;  /* 位槽使用情况 */
    int8_t free_slot = bit_find_first_zero(slots);
    printf("\n位槽状态: ");
    bit_to_string(slots, buf, 8);
    printf("%s\n", buf);
    printf("找到空闲槽位: %d\n", free_slot);
}

/* ============================================================
 * 示例4: 位反转和旋转
 * ============================================================ */
void example_reverse_rotate(void) {
    printf("\n=== 示例4: 位反转和旋转 ===\n\n");
    
    uint64_t value = 0x0F0F0F0F;
    char buf[65];
    
    printf("原值: 0x%llX\n", value);
    
    /* 位反转 */
    uint64_t reversed = bit_reverse(value);
    printf("反转后: 0x%llX\n", reversed);
    
    /* 反转指定位宽 */
    uint8_t byte_val = 0xF0;
    uint8_t byte_rev = (uint8_t)bit_reverse_n(byte_val, 8);
    printf("\n字节反转: 0x%02X -> 0x%02X\n", byte_val, byte_rev);
    
    /* 循环左移 */
    value = 0x12345678;
    printf("\n循环移位 (值: 0x%08llX):\n", value);
    for (int i = 0; i <= 8; i++) {
        uint64_t rotated = bit_rotate_left(value, i, 32);
        printf("  左移 %d 位: 0x%08llX\n", i, rotated);
    }
    
    /* 循环右移 */
    printf("\n循环右移 8 位: 0x%08llX\n", bit_rotate_right(value, 8, 32));
}

/* ============================================================
 * 示例5: 位掩码操作
 * ============================================================ */
void example_bit_masks(void) {
    printf("\n=== 示例5: 位掩码操作 ===\n\n");
    
    /* 生成掩码 */
    printf("低位掩码:\n");
    printf("  低4位: 0x%llX\n", bit_mask_low(4));
    printf("  低8位: 0x%llX\n", bit_mask_low(8));
    printf("  低16位: 0x%llX\n", bit_mask_low(16));
    
    printf("\n高位掩码:\n");
    printf("  高4位: 0x%llX\n", bit_mask_high(4));
    printf("  高8位: 0x%llX\n", bit_mask_high(8));
    
    printf("\n范围掩码:\n");
    printf("  位 4-7: 0x%llX\n", bit_mask_range(4, 7));
    printf("  位 8-15: 0x%llX\n", bit_mask_range(8, 15));
    
    /* 提取和插入 */
    uint64_t color = 0x00FF8000;  /* RGB: 绿色 */
    uint8_t green = (uint8_t)bit_extract(color, 8, 15);
    printf("\n从颜色 0x%06llX 提取绿色分量: 0x%02X (%d)\n", color, green, green);
    
    /* 插入新值 */
    uint64_t new_color = bit_insert(color, 0, 8, 15);  /* 绿色设为0 */
    new_color = bit_insert(new_color, 0xFF, 0, 7);     /* 红色设为255 */
    printf("修改后的颜色: 0x%06llX (红色分量: 0x%02X)\n", 
           new_color, (uint8_t)bit_extract(new_color, 0, 7));
}

/* ============================================================
 * 示例6: 字节序转换
 * ============================================================ */
void example_byte_order(void) {
    printf("\n=== 示例6: 字节序转换 ===\n\n");
    
    uint16_t val16 = 0x1234;
    uint32_t val32 = 0x12345678;
    uint64_t val64 = 0x0123456789ABCDEFULL;
    
    printf("16位转换:\n");
    printf("  原值: 0x%04X\n", val16);
    printf("  字节反转: 0x%04X\n", bit_swap16(val16));
    
    printf("\n32位转换:\n");
    printf("  原值: 0x%08X\n", val32);
    printf("  字节反转: 0x%08X\n", bit_swap32(val32));
    
    printf("\n64位转换:\n");
    printf("  原值: 0x%016llX\n", val64);
    printf("  字节反转: 0x%016llX\n", bit_swap64(val64));
    
    /* 网络编程示例 */
    printf("\n网络字节序转换:\n");
    uint32_t host_order = 0x00000001;
    uint32_t net_order = bit_le_to_be32(host_order);
    printf("  主机序 (小端): 0x%08X\n", host_order);
    printf("  网络序 (大端): 0x%08X\n", net_order);
    
    /* 检测当前系统字节序 */
    uint16_t test = 1;
    bool is_little_endian = *(uint8_t*)&test == 1;
    printf("\n当前系统: %s端\n", is_little_endian ? "小" : "大");
}

/* ============================================================
 * 示例7: 位字段操作
 * ============================================================ */
void example_bit_fields(void) {
    printf("\n=== 示例7: 位字段操作 ===\n\n");
    
    /* 模拟一个32位寄存器 */
    uint32_t control_reg = 0;
    
    /* 位 0: 使能位 */
    /* 位 1-2: 工作模式 (00=停止, 01=运行, 10=暂停, 11=复位) */
    /* 位 3-6: 预分频值 (0-15) */
    /* 位 7-15: 比较值 */
    /* 位 16-31: 计数器 */
    
    /* 设置使能位 */
    control_reg = (uint32_t)bit_set(control_reg, 0);
    printf("设置使能位: 0x%08X\n", control_reg);
    
    /* 设置工作模式为运行 (01) */
    control_reg = (uint32_t)bit_field_write(control_reg, 1, 1, 2);
    printf("设置工作模式=运行: 0x%08X\n", control_reg);
    
    /* 设置预分频值为 7 */
    control_reg = (uint32_t)bit_field_write(control_reg, 7, 3, 6);
    printf("设置预分频=7: 0x%08X\n", control_reg);
    
    /* 设置比较值为 255 */
    control_reg = (uint32_t)bit_field_write(control_reg, 255, 7, 15);
    printf("设置比较值=255: 0x%08X\n", control_reg);
    
    /* 读取各字段 */
    printf("\n读取寄存器字段:\n");
    printf("  使能: %d\n", bit_test(control_reg, 0));
    printf("  工作模式: %llu\n", bit_field_read(control_reg, 1, 2));
    printf("  预分频: %llu\n", bit_field_read(control_reg, 3, 6));
    printf("  比较值: %llu\n", bit_field_read(control_reg, 7, 15));
    printf("  计数器: %llu\n", bit_field_read(control_reg, 16, 31));
}

/* ============================================================
 * 示例8: 位向量
 * ============================================================ */
void example_bit_vector(void) {
    printf("\n=== 示例8: 位向量 ===\n\n");
    
    /* 创建一个1024位的位向量 */
    BitVector *bv = bit_vector_create(1024);
    if (!bv) {
        printf("创建位向量失败\n");
        return;
    }
    
    printf("创建了 %zu 位的位向量\n", bv->size);
    
    /* 设置一些位 */
    for (int i = 0; i < 1024; i += 100) {
        bit_vector_set(bv, i, true);
    }
    bit_vector_set(bv, 1023, true);  /* 最后一位 */
    
    printf("设置了位: 0, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1023\n");
    printf("置位数量: %zu\n", bit_vector_count(bv));
    
    /* 查找设置和未设置的位 */
    printf("\n查找:\n");
    for (int i = 0; i < 5; i++) {
        printf("  位 %d: %s\n", i, bit_vector_get(bv, i) ? "已设置" : "未设置");
    }
    printf("  位 100: %s\n", bit_vector_get(bv, 100) ? "已设置" : "未设置");
    printf("  位 1023: %s\n", bit_vector_get(bv, 1023) ? "已设置" : "未设置");
    
    /* 切换位 */
    int new_val = bit_vector_toggle(bv, 50);
    printf("\n切换位50: %d -> %d\n", new_val ^ 1, new_val);
    
    /* 扩展大小 */
    printf("\n扩展位向量到 2048 位\n");
    bit_vector_resize(bv, 2048);
    printf("新大小: %zu\n", bv->size);
    printf("新位置的值: %s\n", bit_vector_get(bv, 1500) ? "1" : "0");
    
    /* 填充所有位 */
    bit_vector_fill(bv, true);
    printf("填充后置位数量: %zu\n", bit_vector_count(bv));
    
    bit_vector_destroy(bv);
}

/* ============================================================
 * 示例9: 实用函数
 * ============================================================ */
void example_utilities(void) {
    printf("\n=== 示例9: 实用函数 ===\n\n");
    
    /* 2的幂检测 */
    printf("2的幂检测:\n");
    uint64_t test_vals[] = {0, 1, 2, 3, 4, 5, 8, 16, 1023, 1024, 1025};
    for (int i = 0; i < 11; i++) {
        printf("  %llu: %s\n", test_vals[i], 
               bit_is_power_of_two(test_vals[i]) ? "是2的幂" : "不是2的幂");
    }
    
    /* 取整到最近的2的幂 */
    printf("\n取整到最近的2的幂:\n");
    uint64_t vals[] = {5, 100, 1000, 10000};
    for (int i = 0; i < 4; i++) {
        printf("  %llu: 上取整=%llu, 下取整=%llu\n", 
               vals[i],
               bit_next_power_of_two(vals[i]),
               bit_prev_power_of_two(vals[i]));
    }
    
    /* 计算位宽 */
    printf("\n位宽计算:\n");
    printf("  0 -> %d 位\n", bit_width(0));
    printf("  1 -> %d 位\n", bit_width(1));
    printf("  7 -> %d 位\n", bit_width(7));
    printf("  8 -> %d 位\n", bit_width(8));
    printf("  255 -> %d 位\n", bit_width(255));
    printf("  256 -> %d 位\n", bit_width(256));
    
    /* Gray码转换 */
    printf("\nGray码转换:\n");
    printf("  二进制 -> Gray码:\n");
    char bin_buf[17], gray_buf[17];
    for (int i = 0; i <= 15; i++) {
        bit_to_string(i, bin_buf, 4);
        bit_to_string(bit_binary_to_gray(i), gray_buf, 4);
        printf("    %2d (%s) -> Gray: %2d (%s)\n", 
               i, bin_buf, (int)bit_binary_to_gray(i), gray_buf);
    }
    
    /* 字符串转换 */
    printf("\n字符串转换:\n");
    char buf[65];
    bit_to_string(0xDEADBEEF, buf, 32);
    printf("  0xDEADBEEF -> %s\n", buf);
    
    uint64_t parsed;
    bit_from_string("11011110101011011011111011101111", &parsed);
    printf("  11011110101011011011111011101111 -> 0x%llX\n", parsed);
}

/* ============================================================
 * 示例10: 综合应用 - 权限系统
 * ============================================================ */
void example_permission_system(void) {
    printf("\n=== 示例10: 综合应用 - 权限系统 ===\n\n");
    
    /* 定义权限位 */
    #define PERM_READ      (1ULL << 0)
    #define PERM_WRITE     (1ULL << 1)
    #define PERM_EXECUTE   (1ULL << 2)
    #define PERM_DELETE    (1ULL << 3)
    #define PERM_ADMIN     (1ULL << 4)
    #define PERM_SHARE     (1ULL << 5)
    
    /* 初始权限: 读取和执行 */
    uint64_t permissions = PERM_READ | PERM_EXECUTE;
    char buf[65];
    
    bit_to_string(permissions, buf, 8);
    printf("初始权限: 0x%02X (%s)\n", (uint8_t)permissions, buf);
    printf("  读取: %s\n", bit_test(permissions, 0) ? "允许" : "禁止");
    printf("  写入: %s\n", bit_test(permissions, 1) ? "允许" : "禁止");
    printf("  执行: %s\n", bit_test(permissions, 2) ? "允许" : "禁止");
    
    /* 授予写入权限 */
    permissions = bit_set(permissions, 1);
    printf("\n授予写入权限后:\n");
    printf("  写入: %s\n", bit_test(permissions, 1) ? "允许" : "禁止");
    
    /* 授予管理员权限 */
    permissions = bit_set(permissions, 4);
    printf("\n授予管理员权限后:\n");
    printf("  管理员: %s\n", bit_test(permissions, 4) ? "允许" : "禁止");
    
    /* 检查是否有管理员权限 */
    if (bit_test(permissions, 4)) {
        printf("\n管理员模式 - 授予所有权限\n");
        permissions = bit_mask_low(6);  /* 所有6个权限 */
    }
    
    printf("\n最终权限: 0x%02X\n", (uint8_t)permissions);
    printf("权限数量: %d\n", bit_count(permissions));
    
    /* 撤销删除权限 */
    permissions = bit_clear(permissions, 3);
    printf("\n撤销删除权限后:\n");
    printf("  删除: %s\n", bit_test(permissions, 3) ? "允许" : "禁止");
    
    #undef PERM_READ
    #undef PERM_WRITE
    #undef PERM_EXECUTE
    #undef PERM_DELETE
    #undef PERM_ADMIN
    #undef PERM_SHARE
}

/* ============================================================
 * 主函数
 * ============================================================ */
int main(void) {
    printf("\n");
    printf("╔════════════════════════════════════════╗\n");
    printf("║     Bit Utils - 位操作工具库示例      ║\n");
    printf("╚════════════════════════════════════════╝\n");
    
    example_basic_operations();
    example_bit_counting();
    example_bit_finding();
    example_reverse_rotate();
    example_bit_masks();
    example_byte_order();
    example_bit_fields();
    example_bit_vector();
    example_utilities();
    example_permission_system();
    
    printf("\n所有示例运行完成！\n\n");
    return 0;
}