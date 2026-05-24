/**
 * @file math_utils.h
 * @brief C 语言数学工具库 - 提供常用数学运算功能
 * @author AllToolkit
 * @version 1.0.0
 * @date 2026-05-24
 */

#ifndef MATH_UTILS_H
#define MATH_UTILS_H

#include <stddef.h>
#include <stdbool.h>

#ifdef __cplusplus
extern "C" {
#endif

/* ==================== 基础运算 ==================== */

/**
 * @brief 限制值在指定范围内
 */
int clamp_int(int value, int min, int max);
double clamp_double(double value, double min, double max);

/**
 * @brief 返回两个数中的最大值
 */
int max_int(int a, int b);
int max_int_array(const int* arr, size_t size);
double max_double(double a, double b);
double max_double_array(const double* arr, size_t size);

/**
 * @brief 返回两个数中的最小值
 */
int min_int(int a, int b);
int min_int_array(const int* arr, size_t size);
double min_double(double a, double b);
double min_double_array(const double* arr, size_t size);

/**
 * @brief 交换两个整数
 */
void swap_int(int* a, int* b);
void swap_double(double* a, double* b);

/**
 * @brief 计算绝对值
 */
int abs_int(int value);
double abs_double(double value);

/**
 * @brief 计算符号 (-1, 0, 1)
 */
int sign_int(int value);
int sign_double(double value);

/* ==================== 幂与根运算 ==================== */

/**
 * @brief 整数幂运算 (base^exp)
 */
long long power_int(int base, unsigned int exp);

/**
 * @brief 整数平方根 (向下取整)
 */
unsigned int isqrt(unsigned int n);

/**
 * @brief 检查是否为完全平方数
 */
bool is_perfect_square(unsigned int n);

/* ==================== 几何计算 ==================== */

/**
 * @brief 计算两点之间的距离
 */
double distance_2d(double x1, double y1, double x2, double y2);
double distance_3d(double x1, double y1, double z1, double x2, double y2, double z2);

/**
 * @brief 计算圆的面积和周长
 */
double circle_area(double radius);
double circle_circumference(double radius);

/**
 * @brief 计算矩形面积
 */
double rectangle_area(double width, double height);
double rectangle_perimeter(double width, double height);

/**
 * @brief 计算三角形面积 (海伦公式)
 */
double triangle_area(double a, double b, double c);

/**
 * @brief 计算球体体积和表面积
 */
double sphere_volume(double radius);
double sphere_surface_area(double radius);

/* ==================== 统计函数 ==================== */

/**
 * @brief 计算数组的和
 */
long long sum_int_array(const int* arr, size_t size);
double sum_double_array(const double* arr, size_t size);

/**
 * @brief 计算数组的平均值
 */
double mean_int_array(const int* arr, size_t size);
double mean_double_array(const double* arr, size_t size);

/**
 * @brief 计算数组的中位数
 */
double median_int_array(int* arr, size_t size);  /* 注意：会修改原数组 */
double median_double_array(double* arr, size_t size);  /* 注意：会修改原数组 */

/**
 * @brief 计算数组的方差
 */
double variance_int_array(const int* arr, size_t size);
double variance_double_array(const double* arr, size_t size);

/**
 * @brief 计算数组的标准差
 */
double std_dev_int_array(const int* arr, size_t size);
double std_dev_double_array(const double* arr, size_t size);

/* ==================== 数论函数 ==================== */

/**
 * @brief 检查是否为质数
 */
bool is_prime(unsigned int n);

/**
 * @brief 计算最大公约数
 */
unsigned int gcd(unsigned int a, unsigned int b);

/**
 * @brief 计算最小公倍数
 */
unsigned int lcm(unsigned int a, unsigned int b);

/**
 * @brief 计算阶乘
 */
unsigned long long factorial(unsigned int n);

/**
 * @brief 斐波那契数列第n项
 */
unsigned long long fibonacci(unsigned int n);

/**
 * @brief 模运算 (处理负数)
 */
int mod(int a, int b);

/**
 * @brief 模幂运算 (base^exp mod m)
 */
long long mod_power(long long base, long long exp, long long mod);

/* ==================== 数值检查 ==================== */

/**
 * @brief 检查是否为偶数
 */
bool is_even(int n);

/**
 * @brief 检查是否为奇数
 */
bool is_odd(int n);

/**
 * @brief 检查是否为2的幂
 */
bool is_power_of_two(unsigned int n);

/**
 * @brief 检查浮点数是否接近零
 */
bool is_near_zero(double value, double epsilon);

/**
 * @brief 检查两个浮点数是否近似相等
 */
bool is_approx_equal(double a, double b, double epsilon);

/* ==================== 范围与序列 ==================== */

/**
 * @brief 将值从一个范围映射到另一个范围
 */
double map_range(double value, double in_min, double in_max, double out_min, double out_max);

/**
 * @brief 线性插值
 */
double lerp(double a, double b, double t);

/**
 * @brief 生成范围内的整数序列
 */
void range_int(int* arr, size_t size, int start, int step);

/* ==================== 三角函数辅助 ==================== */

/**
 * @brief 角度转弧度
 */
double degrees_to_radians(double degrees);

/**
 * @brief 弧度转角度
 */
double radians_to_degrees(double radians);

#ifdef __cplusplus
}
#endif

#endif /* MATH_UTILS_H */