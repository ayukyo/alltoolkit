/**
 * @file math_utils_test.c
 * @brief C 语言数学工具库测试
 * @author AllToolkit
 * @version 1.0.0
 * @date 2026-05-24
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include "math_utils.h"

/* 测试计数器 */
static int tests_passed = 0;
static int tests_failed = 0;

/* 辅助测试宏 */
#define TEST(name) printf("  Testing %s... ", name)
#define PASS() do { printf("PASS\n"); tests_passed++; } while(0)
#define FAIL(msg, ...) do { printf("FAIL: " msg "\n", ##__VA_ARGS__); tests_failed++; } while(0)
#define ASSERT_TRUE(cond) if (cond) { PASS(); } else { FAIL("Expected true, got false"); }
#define ASSERT_FALSE(cond) if (!(cond)) { PASS(); } else { FAIL("Expected false, got true"); }
#define ASSERT_EQ_INT(expected, actual) \
    if ((expected) == (actual)) { PASS(); } else { FAIL("Expected %d, got %d", (expected), (actual)); }
#define ASSERT_EQ_LL(expected, actual) \
    if ((expected) == (actual)) { PASS(); } else { FAIL("Expected %lld, got %lld", (long long)(expected), (long long)(actual)); }
#define ASSERT_EQ_UINT(expected, actual) \
    if ((expected) == (actual)) { PASS(); } else { FAIL("Expected %u, got %u", (expected), (actual)); }
#define ASSERT_NEAR(expected, actual, eps) \
    if (fabs((expected) - (actual)) < (eps)) { PASS(); } else { FAIL("Expected %.6f, got %.6f", (expected), (actual)); }

/* ==================== 基础运算测试 ==================== */

void test_clamp(void) {
    printf("\n=== Clamp Tests ===\n");
    
    TEST("clamp_int normal range");
    ASSERT_EQ_INT(5, clamp_int(5, 0, 10));
    
    TEST("clamp_int below min");
    ASSERT_EQ_INT(0, clamp_int(-5, 0, 10));
    
    TEST("clamp_int above max");
    ASSERT_EQ_INT(10, clamp_int(15, 0, 10));
    
    TEST("clamp_double normal range");
    ASSERT_NEAR(5.5, clamp_double(5.5, 0.0, 10.0), 0.0001);
    
    TEST("clamp_double below min");
    ASSERT_NEAR(0.0, clamp_double(-5.0, 0.0, 10.0), 0.0001);
}

void test_max_min(void) {
    printf("\n=== Max/Min Tests ===\n");
    
    TEST("max_int");
    ASSERT_EQ_INT(10, max_int(10, 5));
    
    TEST("min_int");
    ASSERT_EQ_INT(5, min_int(10, 5));
    
    TEST("max_double");
    ASSERT_NEAR(10.5, max_double(10.5, 5.5), 0.0001);
    
    TEST("min_double");
    ASSERT_NEAR(5.5, min_double(10.5, 5.5), 0.0001);
    
    int arr1[] = {3, 1, 4, 1, 5, 9, 2, 6};
    TEST("max_int_array");
    ASSERT_EQ_INT(9, max_int_array(arr1, 8));
    
    TEST("min_int_array");
    ASSERT_EQ_INT(1, min_int_array(arr1, 8));
}

void test_swap_abs_sign(void) {
    printf("\n=== Swap/Abs/Sign Tests ===\n");
    
    int a = 5, b = 10;
    TEST("swap_int");
    swap_int(&a, &b);
    if (a == 10 && b == 5) { PASS(); } else { FAIL("Expected a=10, b=5, got a=%d, b=%d", a, b); }
    
    TEST("abs_int positive");
    ASSERT_EQ_INT(5, abs_int(5));
    
    TEST("abs_int negative");
    ASSERT_EQ_INT(5, abs_int(-5));
    
    TEST("abs_double positive");
    ASSERT_NEAR(5.5, abs_double(5.5), 0.0001);
    
    TEST("abs_double negative");
    ASSERT_NEAR(5.5, abs_double(-5.5), 0.0001);
    
    TEST("sign_int positive");
    ASSERT_EQ_INT(1, sign_int(10));
    
    TEST("sign_int negative");
    ASSERT_EQ_INT(-1, sign_int(-10));
    
    TEST("sign_int zero");
    ASSERT_EQ_INT(0, sign_int(0));
}

/* ==================== 幂与根运算测试 ==================== */

void test_power_sqrt(void) {
    printf("\n=== Power/Sqrt Tests ===\n");
    
    TEST("power_int 2^3");
    ASSERT_EQ_LL(8, power_int(2, 3));
    
    TEST("power_int 3^4");
    ASSERT_EQ_LL(81, power_int(3, 4));
    
    TEST("power_int 5^0");
    ASSERT_EQ_LL(1, power_int(5, 0));
    
    TEST("isqrt 16");
    ASSERT_EQ_UINT(4, isqrt(16));
    
    TEST("isqrt 17");
    ASSERT_EQ_UINT(4, isqrt(17));
    
    TEST("isqrt 15");
    ASSERT_EQ_UINT(3, isqrt(15));
    
    TEST("is_perfect_square 16");
    ASSERT_TRUE(is_perfect_square(16));
    
    TEST("is_perfect_square 17");
    ASSERT_FALSE(is_perfect_square(17));
}

/* ==================== 几何计算测试 ==================== */

void test_geometry(void) {
    printf("\n=== Geometry Tests ===\n");
    
    TEST("distance_2d (0,0) to (3,4)");
    ASSERT_NEAR(5.0, distance_2d(0, 0, 3, 4), 0.0001);
    
    TEST("distance_3d (0,0,0) to (1,2,2)");
    ASSERT_NEAR(3.0, distance_3d(0, 0, 0, 1, 2, 2), 0.0001);
    
    TEST("circle_area r=1");
    ASSERT_NEAR(3.14159265358979, circle_area(1.0), 0.0001);
    
    TEST("circle_circumference r=1");
    ASSERT_NEAR(6.28318530717959, circle_circumference(1.0), 0.0001);
    
    TEST("rectangle_area 3x4");
    ASSERT_NEAR(12.0, rectangle_area(3.0, 4.0), 0.0001);
    
    TEST("rectangle_perimeter 3x4");
    ASSERT_NEAR(14.0, rectangle_perimeter(3.0, 4.0), 0.0001);
    
    TEST("triangle_area 3-4-5");
    ASSERT_NEAR(6.0, triangle_area(3.0, 4.0, 5.0), 0.0001);
    
    TEST("sphere_volume r=1");
    ASSERT_NEAR(4.18879020478639, sphere_volume(1.0), 0.0001);
    
    TEST("sphere_surface_area r=1");
    ASSERT_NEAR(12.5663706143592, sphere_surface_area(1.0), 0.0001);
}

/* ==================== 统计函数测试 ==================== */

void test_statistics(void) {
    printf("\n=== Statistics Tests ===\n");
    
    int arr1[] = {1, 2, 3, 4, 5};
    TEST("sum_int_array");
    ASSERT_EQ_LL(15, sum_int_array(arr1, 5));
    
    TEST("mean_int_array");
    ASSERT_NEAR(3.0, mean_int_array(arr1, 5), 0.0001);
    
    int arr2[] = {1, 2, 3, 4, 5};
    TEST("median_int_array odd");
    ASSERT_NEAR(3.0, median_int_array(arr2, 5), 0.0001);
    
    int arr3[] = {1, 2, 3, 4, 5, 6};
    TEST("median_int_array even");
    ASSERT_NEAR(3.5, median_int_array(arr3, 6), 0.0001);
    
    int arr4[] = {2, 4, 4, 4, 5, 5, 7, 9};
    TEST("variance_int_array");
    ASSERT_NEAR(4.0, variance_int_array(arr4, 8), 0.0001);
    
    TEST("std_dev_int_array");
    ASSERT_NEAR(2.0, std_dev_int_array(arr4, 8), 0.0001);
}

/* ==================== 数论函数测试 ==================== */

void test_number_theory(void) {
    printf("\n=== Number Theory Tests ===\n");
    
    TEST("is_prime 2");
    ASSERT_TRUE(is_prime(2));
    
    TEST("is_prime 17");
    ASSERT_TRUE(is_prime(17));
    
    TEST("is_prime 18");
    ASSERT_FALSE(is_prime(18));
    
    TEST("is_prime 1");
    ASSERT_FALSE(is_prime(1));
    
    TEST("gcd 48, 18");
    ASSERT_EQ_UINT(6, gcd(48, 18));
    
    TEST("gcd 17, 23");
    ASSERT_EQ_UINT(1, gcd(17, 23));
    
    TEST("lcm 4, 6");
    ASSERT_EQ_UINT(12, lcm(4, 6));
    
    TEST("factorial 5");
    ASSERT_EQ_LL(120, factorial(5));
    
    TEST("factorial 0");
    ASSERT_EQ_LL(1, factorial(0));
    
    TEST("fibonacci 10");
    ASSERT_EQ_LL(55, fibonacci(10));
    
    TEST("fibonacci 0");
    ASSERT_EQ_LL(0, fibonacci(0));
    
    TEST("fibonacci 1");
    ASSERT_EQ_LL(1, fibonacci(1));
    
    TEST("mod -7, 5");
    ASSERT_EQ_INT(3, mod(-7, 5));
    
    TEST("mod 7, 5");
    ASSERT_EQ_INT(2, mod(7, 5));
    
    TEST("mod_power 2^10 mod 1000");
    ASSERT_EQ_LL(24, mod_power(2, 10, 1000));
}

/* ==================== 数值检查测试 ==================== */

void test_checks(void) {
    printf("\n=== Number Check Tests ===\n");
    
    TEST("is_even 4");
    ASSERT_TRUE(is_even(4));
    
    TEST("is_even 5");
    ASSERT_FALSE(is_even(5));
    
    TEST("is_odd 5");
    ASSERT_TRUE(is_odd(5));
    
    TEST("is_power_of_two 8");
    ASSERT_TRUE(is_power_of_two(8));
    
    TEST("is_power_of_two 7");
    ASSERT_FALSE(is_power_of_two(7));
    
    TEST("is_near_zero 0.00001");
    ASSERT_TRUE(is_near_zero(0.00001, 0.001));
    
    TEST("is_near_zero 0.1");
    ASSERT_FALSE(is_near_zero(0.1, 0.001));
    
    TEST("is_approx_equal 1.0, 1.00001");
    ASSERT_TRUE(is_approx_equal(1.0, 1.00001, 0.001));
}

/* ==================== 范围与序列测试 ==================== */

void test_range_lerp(void) {
    printf("\n=== Range/Lerp Tests ===\n");
    
    TEST("map_range 5 from [0,10] to [0,100]");
    ASSERT_NEAR(50.0, map_range(5.0, 0.0, 10.0, 0.0, 100.0), 0.0001);
    
    TEST("map_range 0 from [0,100] to [0,255]");
    ASSERT_NEAR(0.0, map_range(0.0, 0.0, 100.0, 0.0, 255.0), 0.0001);
    
    TEST("map_range 50 from [0,100] to [0,255]");
    ASSERT_NEAR(127.5, map_range(50.0, 0.0, 100.0, 0.0, 255.0), 0.0001);
    
    TEST("lerp 0 to 10, t=0.5");
    ASSERT_NEAR(5.0, lerp(0.0, 10.0, 0.5), 0.0001);
    
    TEST("lerp 0 to 10, t=0");
    ASSERT_NEAR(0.0, lerp(0.0, 10.0, 0.0), 0.0001);
    
    TEST("lerp 0 to 10, t=1");
    ASSERT_NEAR(10.0, lerp(0.0, 10.0, 1.0), 0.0001);
    
    int range_arr[5];
    range_int(range_arr, 5, 0, 2);
    TEST("range_int start=0, step=2");
    if (range_arr[0] == 0 && range_arr[1] == 2 && range_arr[2] == 4 && 
        range_arr[3] == 6 && range_arr[4] == 8) {
        PASS();
    } else {
        FAIL("Expected [0,2,4,6,8]");
    }
}

/* ==================== 三角函数辅助测试 ==================== */

void test_angle_conversion(void) {
    printf("\n=== Angle Conversion Tests ===\n");
    
    TEST("degrees_to_radians 180");
    ASSERT_NEAR(3.14159265358979, degrees_to_radians(180.0), 0.0001);
    
    TEST("degrees_to_radians 90");
    ASSERT_NEAR(1.57079632679490, degrees_to_radians(90.0), 0.0001);
    
    TEST("radians_to_degrees pi");
    ASSERT_NEAR(180.0, radians_to_degrees(3.14159265358979), 0.0001);
    
    TEST("radians_to_degrees pi/2");
    ASSERT_NEAR(90.0, radians_to_degrees(1.57079632679490), 0.0001);
}

/* ==================== 边界情况测试 ==================== */

void test_edge_cases(void) {
    printf("\n=== Edge Case Tests ===\n");
    
    TEST("factorial 20 (max safe)");
    ASSERT_EQ_LL(2432902008176640000ULL, factorial(20));
    
    int single[] = {42};
    TEST("max_int_array single element");
    ASSERT_EQ_INT(42, max_int_array(single, 1));
    
    TEST("min_int_array single element");
    ASSERT_EQ_INT(42, min_int_array(single, 1));
    
    TEST("sum_int_array single element");
    ASSERT_EQ_LL(42, sum_int_array(single, 1));
    
    TEST("gcd 0, 5");
    ASSERT_EQ_UINT(5, gcd(0, 5));
    
    TEST("gcd 5, 0");
    ASSERT_EQ_UINT(5, gcd(5, 0));
    
    TEST("lcm 0, 5");
    ASSERT_EQ_UINT(0, lcm(0, 5));
    
    int neg_arr[] = {-5, -3, -1, -10};
    TEST("max_int_array with negatives");
    ASSERT_EQ_INT(-1, max_int_array(neg_arr, 4));
    
    TEST("min_int_array with negatives");
    ASSERT_EQ_INT(-10, min_int_array(neg_arr, 4));
}

/* ==================== 主函数 ==================== */

int main(void) {
    printf("========================================\n");
    printf("     Math Utils Library Test Suite\n");
    printf("========================================\n");
    
    test_clamp();
    test_max_min();
    test_swap_abs_sign();
    test_power_sqrt();
    test_geometry();
    test_statistics();
    test_number_theory();
    test_checks();
    test_range_lerp();
    test_angle_conversion();
    test_edge_cases();
    
    printf("\n========================================\n");
    printf("           Test Results\n");
    printf("========================================\n");
    printf("  Passed: %d\n", tests_passed);
    printf("  Failed: %d\n", tests_failed);
    printf("  Total:  %d\n", tests_passed + tests_failed);
    printf("========================================\n");
    
    return (tests_failed > 0) ? 1 : 0;
}