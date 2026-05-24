/**
 * @file example.c
 * @brief Math Utils 使用示例
 * @author AllToolkit
 * @version 1.0.0
 * @date 2026-05-24
 * 
 * 编译命令:
 *   gcc -o example example.c math_utils.c -lm
 * 
 * 运行:
 *   ./example
 */

#include <stdio.h>
#include <string.h>
#include "math_utils.h"

int main(void) {
    printf("========================================\n");
    printf("     Math Utils 使用示例\n");
    printf("========================================\n\n");
    
    /* ==================== 基础运算 ==================== */
    printf("【基础运算】\n");
    printf("----------------------------------------\n");
    
    /* Clamp 限制范围 */
    int value = 15;
    printf("clamp_int(%d, 0, 10) = %d\n", value, clamp_int(value, 0, 10));
    
    /* 最大最小值 */
    printf("max_int(10, 20) = %d\n", max_int(10, 20));
    printf("min_int(10, 20) = %d\n", min_int(10, 20));
    
    /* 数组统计 */
    int arr[] = {3, 1, 4, 1, 5, 9, 2, 6, 5, 3};
    size_t arr_size = sizeof(arr) / sizeof(arr[0]);
    printf("数组: [3, 1, 4, 1, 5, 9, 2, 6, 5, 3]\n");
    printf("  最大值: %d\n", max_int_array(arr, arr_size));
    printf("  最小值: %d\n", min_int_array(arr, arr_size));
    printf("  总和: %lld\n", sum_int_array(arr, arr_size));
    printf("  平均值: %.2f\n", mean_int_array(arr, arr_size));
    
    /* 绝对值和符号 */
    printf("abs_int(-42) = %d\n", abs_int(-42));
    printf("sign_int(-42) = %d\n", sign_int(-42));
    printf("\n");
    
    /* ==================== 幂与根运算 ==================== */
    printf("【幂与根运算】\n");
    printf("----------------------------------------\n");
    
    printf("power_int(2, 10) = %lld\n", power_int(2, 10));
    printf("isqrt(100) = %u\n", isqrt(100));
    printf("isqrt(99) = %u\n", isqrt(99));
    printf("is_perfect_square(144) = %s\n", 
           is_perfect_square(144) ? "true" : "false");
    printf("is_perfect_square(145) = %s\n", 
           is_perfect_square(145) ? "true" : "false");
    printf("\n");
    
    /* ==================== 几何计算 ==================== */
    printf("【几何计算】\n");
    printf("----------------------------------------\n");
    
    printf("两点距离 (0,0) 到 (3,4) = %.2f\n", distance_2d(0, 0, 3, 4));
    printf("圆面积 (r=5) = %.2f\n", circle_area(5));
    printf("圆周长 (r=5) = %.2f\n", circle_circumference(5));
    printf("矩形面积 (4x5) = %.2f\n", rectangle_area(4, 5));
    printf("三角形面积 (边 3-4-5) = %.2f\n", triangle_area(3, 4, 5));
    printf("球体体积 (r=3) = %.2f\n", sphere_volume(3));
    printf("\n");
    
    /* ==================== 统计函数 ==================== */
    printf("【统计函数】\n");
    printf("----------------------------------------\n");
    
    int scores[] = {85, 92, 78, 95, 88, 73, 91, 67, 82, 90};
    size_t scores_size = sizeof(scores) / sizeof(scores[0]);
    
    printf("成绩: [85, 92, 78, 95, 88, 73, 91, 67, 82, 90]\n");
    printf("  平均分: %.2f\n", mean_int_array(scores, scores_size));
    printf("  标准差: %.2f\n", std_dev_int_array(scores, scores_size));
    
    /* 注意：median 函数会修改原数组，所以复制一份 */
    int scores_copy[10];
    memcpy(scores_copy, scores, sizeof(scores));
    printf("  中位数: %.2f\n", median_int_array(scores_copy, scores_size));
    printf("\n");
    
    /* ==================== 数论函数 ==================== */
    printf("【数论函数】\n");
    printf("----------------------------------------\n");
    
    printf("质数检查:\n");
    for (int i = 2; i <= 20; i++) {
        if (is_prime(i)) {
            printf("  %d 是质数\n", i);
        }
    }
    
    printf("\ngcd(48, 18) = %u\n", gcd(48, 18));
    printf("lcm(12, 18) = %u\n", lcm(12, 18));
    
    printf("\n阶乘:\n");
    for (int i = 0; i <= 10; i++) {
        printf("  %d! = %llu\n", i, factorial(i));
    }
    
    printf("\n斐波那契数列前 15 项:\n  ");
    for (int i = 0; i < 15; i++) {
        printf("%llu ", fibonacci(i));
    }
    printf("\n");
    
    printf("\n模运算:\n");
    printf("  mod(-7, 5) = %d\n", mod(-7, 5));
    printf("  mod_power(3, 7, 13) = %lld\n", mod_power(3, 7, 13));
    printf("\n");
    
    /* ==================== 数值检查 ==================== */
    printf("【数值检查】\n");
    printf("----------------------------------------\n");
    
    printf("奇偶检查:\n");
    printf("  is_even(42) = %s\n", is_even(42) ? "true" : "false");
    printf("  is_odd(42) = %s\n", is_odd(42) ? "true" : "false");
    
    printf("\n2的幂检查:\n");
    for (int i = 1; i <= 16; i++) {
        if (is_power_of_two(i)) {
            printf("  %d 是 2 的幂\n", i);
        }
    }
    
    printf("\n浮点数比较:\n");
    printf("  is_approx_equal(1.0, 1.0001, 0.01) = %s\n",
           is_approx_equal(1.0, 1.0001, 0.01) ? "true" : "false");
    printf("\n");
    
    /* ==================== 范围映射与插值 ==================== */
    printf("【范围映射与插值】\n");
    printf("----------------------------------------\n");
    
    printf("将温度从摄氏度映射到华氏度:\n");
    double celsius[] = {0, 25, 37, 100};
    for (int i = 0; i < 4; i++) {
        double fahrenheit = map_range(celsius[i], 0, 100, 32, 212);
        printf("  %.0f°C = %.1f°F\n", celsius[i], fahrenheit);
    }
    
    printf("\n线性插值 (从 0 到 100):\n");
    double t_values[] = {0.0, 0.25, 0.5, 0.75, 1.0};
    for (int i = 0; i < 5; i++) {
        printf("  t=%.2f: %.1f\n", t_values[i], lerp(0, 100, t_values[i]));
    }
    
    printf("\n生成等差数列:\n");
    int sequence[10];
    range_int(sequence, 10, 0, 5);
    printf("  ");
    for (int i = 0; i < 10; i++) {
        printf("%d ", sequence[i]);
    }
    printf("\n\n");
    
    /* ==================== 角度转换 ==================== */
    printf("【角度转换】\n");
    printf("----------------------------------------\n");
    
    double angles[] = {0, 45, 90, 180, 270, 360};
    printf("度数 -> 弧度:\n");
    for (int i = 0; i < 6; i++) {
        printf("  %.0f° = %.4f rad\n", angles[i], degrees_to_radians(angles[i]));
    }
    printf("\n");
    
    printf("========================================\n");
    printf("        示例演示完成\n");
    printf("========================================\n");
    
    return 0;
}