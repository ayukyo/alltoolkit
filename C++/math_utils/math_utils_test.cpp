/**
 * @file math_utils_test.cpp
 * @brief math_utils 测试文件
 * @author AllToolkit
 * @date 2026-04-24
 *
 * 编译: g++ -std=c++17 -o math_utils_test math_utils_test.cpp
 * 运行: ./math_utils_test
 */

#include "math_utils.hpp"
#include <cassert>
#include <cmath>
#include <iomanip>
#include <iostream>

using namespace alltoolkit::math_utils;

// 测试计数器
int testsPassed = 0;
int testsFailed = 0;

#define TEST(name) void test_##name()
#define RUN_TEST(name) do { \
    std::cout << "Running " << #name << "... "; \
    try { \
        test_##name(); \
        std::cout << "✓ PASSED" << std::endl; \
        testsPassed++; \
    } catch (const std::exception& e) { \
        std::cout << "✗ FAILED: " << e.what() << std::endl; \
        testsFailed++; \
    } catch (...) { \
        std::cout << "✗ FAILED: Unknown error" << std::endl; \
        testsFailed++; \
    } \
} while(0)

#define ASSERT_TRUE(expr) do { if (!(expr)) throw std::runtime_error("Assertion failed: " #expr); } while(0)
#define ASSERT_FALSE(expr) ASSERT_TRUE(!(expr))
#define ASSERT_EQ(a, b) do { if ((a) != (b)) throw std::runtime_error("Assertion failed: " #a " != " #b); } while(0)
#define ASSERT_NEAR(a, b, eps) do { if (std::abs((a) - (b)) > (eps)) throw std::runtime_error("Assertion failed: " #a " !≈ " #b); } while(0)

// ============================================================================
// 基础数学运算测试
// ============================================================================

TEST(basic_abs) {
    ASSERT_EQ(abs(-5), 5);
    ASSERT_EQ(abs(5), 5);
    ASSERT_EQ(abs(0), 0);
    ASSERT_NEAR(abs(-3.14), 3.14, 0.0001);
}

TEST(basic_max_min) {
    ASSERT_EQ(max(3, 5), 5);
    ASSERT_EQ(max(5, 3), 5);
    ASSERT_EQ(min(3, 5), 3);
    ASSERT_EQ(min(5, 3), 3);
}

TEST(basic_clamp) {
    ASSERT_EQ(clamp(5, 0, 10), 5);
    ASSERT_EQ(clamp(-5, 0, 10), 0);
    ASSERT_EQ(clamp(15, 0, 10), 10);
}

TEST(basic_lerp) {
    ASSERT_NEAR(lerp(0.0, 10.0, 0.5), 5.0, 0.0001);
    ASSERT_NEAR(lerp(0.0, 10.0, 0.0), 0.0, 0.0001);
    ASSERT_NEAR(lerp(0.0, 10.0, 1.0), 10.0, 0.0001);
}

TEST(basic_smoothstep) {
    ASSERT_NEAR(smoothstep(0.0, 1.0, 0.0), 0.0, 0.0001);
    ASSERT_NEAR(smoothstep(0.0, 1.0, 1.0), 1.0, 0.0001);
    ASSERT_NEAR(smoothstep(0.0, 1.0, 0.5), 0.5, 0.0001);
}

TEST(basic_square_cube) {
    ASSERT_EQ(square(5), 25);
    ASSERT_EQ(square(-3), 9);
    ASSERT_EQ(cube(2), 8);
    ASSERT_EQ(cube(-2), -8);
}

TEST(basic_power) {
    ASSERT_EQ(power(2, 3), 8);
    ASSERT_EQ(power(2, 0), 1);
    ASSERT_EQ(power(5, 2), 25);
    ASSERT_NEAR(power(2.0, -2), 0.25, 0.0001);
}

TEST(basic_sign) {
    ASSERT_EQ(sign(5), 1);
    ASSERT_EQ(sign(-5), -1);
    ASSERT_EQ(sign(0), 0);
}

TEST(basic_distance) {
    ASSERT_NEAR(distance(0.0, 0.0, 3.0, 4.0), 5.0, 0.0001);
    ASSERT_NEAR(distance(1.0, 1.0, 4.0, 5.0), 5.0, 0.0001);
}

TEST(basic_distance3d) {
    ASSERT_NEAR(distance3D(0.0, 0.0, 0.0, 1.0, 2.0, 2.0), 3.0, 0.0001);
}

// ============================================================================
// 统计计算测试
// ============================================================================

TEST(stats_mean) {
    Vector<int> data1 = {1, 2, 3, 4, 5};
    ASSERT_NEAR(mean(data1), 3.0, 0.0001);
    
    Vector<int> empty;
    ASSERT_NEAR(mean(empty), 0.0, 0.0001);
    
    Vector<double> data2 = {1.5, 2.5, 3.5};
    ASSERT_NEAR(mean(data2), 2.5, 0.0001);
}

TEST(stats_median) {
    Vector<int> data1 = {1, 2, 3, 4, 5};
    ASSERT_NEAR(median(data1), 3.0, 0.0001);
    
    Vector<int> data2 = {1, 2, 3, 4};
    ASSERT_NEAR(median(data2), 2.5, 0.0001);
}

TEST(stats_variance) {
    Vector<double> data = {2.0, 4.0, 4.0, 4.0, 5.0, 5.0, 7.0, 9.0};
    ASSERT_NEAR(variance(data), 4.0, 0.0001);
}

TEST(stats_stddev) {
    Vector<double> data = {2.0, 4.0, 4.0, 4.0, 5.0, 5.0, 7.0, 9.0};
    ASSERT_NEAR(stdDev(data), 2.0, 0.0001);
}

TEST(stats_correlation) {
    Vector<double> x = {1, 2, 3, 4, 5};
    Vector<double> y = {2, 4, 6, 8, 10};
    ASSERT_NEAR(correlation(x, y), 1.0, 0.0001);  // 完全正相关
}

TEST(stats_sum_product) {
    Vector<int> data = {1, 2, 3, 4, 5};
    ASSERT_EQ(sum(data), 15);
    ASSERT_EQ(product(data), 120);
}

TEST(stats_range) {
    Vector<int> data = {1, 5, 3, 9, 2};
    ASSERT_EQ(range(data), 8);
}

// ============================================================================
// 几何计算测试
// ============================================================================

TEST(geo_circle) {
    ASSERT_NEAR(circleArea(1.0), PI, 0.0001);
    ASSERT_NEAR(circleCircumference(1.0), 2 * PI, 0.0001);
}

TEST(geo_rectangle) {
    ASSERT_EQ(rectangleArea(5, 3), 15);
    ASSERT_EQ(rectanglePerimeter(5, 3), 16);
}

TEST(geo_triangle) {
    ASSERT_NEAR(triangleArea(3.0, 4.0), 6.0, 0.0001);  // 底高公式
    ASSERT_NEAR(triangleArea(3.0, 4.0, 5.0), 6.0, 0.0001);  // 海伦公式
}

TEST(geo_sphere) {
    ASSERT_NEAR(sphereVolume(1.0), 4.0 * PI / 3.0, 0.0001);
    ASSERT_NEAR(sphereSurfaceArea(1.0), 4.0 * PI, 0.0001);
}

TEST(geo_cylinder) {
    ASSERT_NEAR(cylinderVolume(1.0, 1.0), PI, 0.0001);
}

TEST(geo_point_in_circle) {
    ASSERT_TRUE(pointInCircle(0.0, 0.0, 0.0, 0.0, 5.0));
    ASSERT_TRUE(pointInCircle(3.0, 4.0, 0.0, 0.0, 5.0));
    ASSERT_FALSE(pointInCircle(4.0, 4.0, 0.0, 0.0, 5.0));
}

TEST(geo_point_in_rect) {
    ASSERT_TRUE(pointInRect(5, 5, 0, 0, 10, 10));
    ASSERT_FALSE(pointInRect(15, 5, 0, 0, 10, 10));
}

// ============================================================================
// 数论函数测试
// ============================================================================

TEST(num_gcd_lcm) {
    ASSERT_EQ(gcd(12, 8), 4);
    ASSERT_EQ(gcd(17, 13), 1);
    ASSERT_EQ(lcm(4, 6), 12);
    ASSERT_EQ(lcm(3, 5), 15);
}

TEST(num_prime) {
    ASSERT_TRUE(isPrime(2));
    ASSERT_TRUE(isPrime(17));
    ASSERT_TRUE(isPrime(97));
    ASSERT_FALSE(isPrime(1));
    ASSERT_FALSE(isPrime(4));
    ASSERT_FALSE(isPrime(100));
}

TEST(num_factorial) {
    ASSERT_EQ(factorial(0), 1ULL);
    ASSERT_EQ(factorial(1), 1ULL);
    ASSERT_EQ(factorial(5), 120ULL);
    ASSERT_EQ(factorial(10), 3628800ULL);
}

TEST(num_permutation_combination) {
    ASSERT_EQ(permutation(5, 3), 60ULL);
    ASSERT_EQ(permutation(4, 2), 12ULL);
    ASSERT_EQ(combination(5, 3), 10ULL);
    ASSERT_EQ(combination(10, 5), 252ULL);
}

TEST(num_fibonacci) {
    ASSERT_EQ(fibonacci(0), 0ULL);
    ASSERT_EQ(fibonacci(1), 1ULL);
    ASSERT_EQ(fibonacci(10), 55ULL);
    ASSERT_EQ(fibonacci(20), 6765ULL);
}

TEST(num_sieve) {
    auto primes = sieveOfEratosthenes(30);
    Vector<int> expected = {2, 3, 5, 7, 11, 13, 17, 19, 23, 29};
    ASSERT_TRUE(primes == expected);
}

// ============================================================================
// 三角函数测试
// ============================================================================

TEST(trig_deg_rad) {
    ASSERT_NEAR(degToRad(180.0), PI, 0.0001);
    ASSERT_NEAR(radToDeg(PI), 180.0, 0.0001);
}

TEST(trig_safe_functions) {
    ASSERT_NEAR(safeAsin(1.5), PI / 2, 0.0001);  // 应该被限制
    ASSERT_NEAR(safeAcos(1.5), 0.0, 0.0001);    // 应该被限制
}

TEST(trig_hyperbolic) {
    // sec, csc, cot 测试
    ASSERT_NEAR(sec(0.0), 1.0, 0.0001);
    ASSERT_NEAR(csc(PI / 2), 1.0, 0.0001);
    ASSERT_NEAR(cot(PI / 4), 1.0, 0.0001);
}

// ============================================================================
// 数值计算测试
// ============================================================================

TEST(num_sqrt_newton) {
    ASSERT_NEAR(sqrtNewton(4.0), 2.0, 0.0001);
    ASSERT_NEAR(sqrtNewton(9.0), 3.0, 0.0001);
    ASSERT_NEAR(sqrtNewton(2.0), std::sqrt(2.0), 0.0001);
}

TEST(num_bisection) {
    // 求解 x^2 - 4 = 0 在 [0, 3] 范围内的根
    auto root = bisectionMethod([](double x) { return x * x - 4; }, 0.0, 3.0);
    ASSERT_TRUE(root.has_value());
    ASSERT_NEAR(root.value(), 2.0, 0.001);
}

TEST(num_integration) {
    // 积分 x^2 在 [0, 1] 上，结果应为 1/3
    auto f = [](double x) { return x * x; };
    ASSERT_NEAR(trapezoidalIntegration(f, 0.0, 1.0), 1.0 / 3.0, 0.001);
    ASSERT_NEAR(simpsonIntegration(f, 0.0, 1.0), 1.0 / 3.0, 0.0001);
}

// ============================================================================
// 向量操作测试
// ============================================================================

TEST(vec_add_sub) {
    Vector<double> a = {1, 2, 3};
    Vector<double> b = {4, 5, 6};
    
    auto sum = vectorAdd(a, b);
    ASSERT_TRUE(sum == Vector<double>({5, 7, 9}));
    
    auto diff = vectorSub(a, b);
    ASSERT_TRUE(diff == Vector<double>({-3, -3, -3}));
}

TEST(vec_scale) {
    Vector<double> v = {1, 2, 3};
    auto scaled = vectorScale(v, 2.0);
    ASSERT_TRUE(scaled == Vector<double>({2, 4, 6}));
}

TEST(vec_dot) {
    Vector<double> a = {1, 2, 3};
    Vector<double> b = {4, 5, 6};
    ASSERT_EQ(dotProduct(a, b), 32);
}

TEST(vec_magnitude_normalize) {
    Vector<double> v = {3, 4};
    ASSERT_NEAR(vectorMagnitude(v), 5.0, 0.0001);
    
    auto normalized = vectorNormalize(v);
    ASSERT_NEAR(vectorMagnitude(normalized), 1.0, 0.0001);
}

TEST(vec_cross) {
    Vector<double> a = {1, 0, 0};
    Vector<double> b = {0, 1, 0};
    auto cross = crossProduct3D(a, b);
    ASSERT_NEAR(cross[0], 0.0, 0.0001);
    ASSERT_NEAR(cross[1], 0.0, 0.0001);
    ASSERT_NEAR(cross[2], 1.0, 0.0001);
}

TEST(vec_angle) {
    Vector<double> a = {1, 0, 0};
    Vector<double> b = {0, 1, 0};
    ASSERT_NEAR(vectorAngle(a, b), PI / 2, 0.0001);
}

// ============================================================================
// 比较和映射函数测试
// ============================================================================

TEST(compare_approx) {
    ASSERT_TRUE(approxEqual(1.0, 1.0 + 1e-10));
    ASSERT_FALSE(approxEqual(1.0, 1.001));
    ASSERT_TRUE(isZero(1e-15));
    ASSERT_FALSE(isZero(0.001));
    ASSERT_TRUE(inRange(5, 0, 10));
    ASSERT_FALSE(inRange(15, 0, 10));
}

TEST(map_range) {
    ASSERT_NEAR(mapRange(5.0, 0.0, 10.0, 0.0, 100.0), 50.0, 0.0001);
    ASSERT_NEAR(normalize(50.0, 0.0, 100.0), 0.5, 0.0001);
}

// ============================================================================
// 主函数
// ============================================================================

int main() {
    std::cout << "\n========================================" << std::endl;
    std::cout << "  AllToolkit C++ Math Utils Test Suite  " << std::endl;
    std::cout << "========================================\n" << std::endl;
    
    // 基础数学运算测试
    std::cout << "--- Basic Math Operations ---" << std::endl;
    RUN_TEST(basic_abs);
    RUN_TEST(basic_max_min);
    RUN_TEST(basic_clamp);
    RUN_TEST(basic_lerp);
    RUN_TEST(basic_smoothstep);
    RUN_TEST(basic_square_cube);
    RUN_TEST(basic_power);
    RUN_TEST(basic_sign);
    RUN_TEST(basic_distance);
    RUN_TEST(basic_distance3d);
    
    // 统计计算测试
    std::cout << "\n--- Statistics ---" << std::endl;
    RUN_TEST(stats_mean);
    RUN_TEST(stats_median);
    RUN_TEST(stats_variance);
    RUN_TEST(stats_stddev);
    RUN_TEST(stats_correlation);
    RUN_TEST(stats_sum_product);
    RUN_TEST(stats_range);
    
    // 几何计算测试
    std::cout << "\n--- Geometry ---" << std::endl;
    RUN_TEST(geo_circle);
    RUN_TEST(geo_rectangle);
    RUN_TEST(geo_triangle);
    RUN_TEST(geo_sphere);
    RUN_TEST(geo_cylinder);
    RUN_TEST(geo_point_in_circle);
    RUN_TEST(geo_point_in_rect);
    
    // 数论函数测试
    std::cout << "\n--- Number Theory ---" << std::endl;
    RUN_TEST(num_gcd_lcm);
    RUN_TEST(num_prime);
    RUN_TEST(num_factorial);
    RUN_TEST(num_permutation_combination);
    RUN_TEST(num_fibonacci);
    RUN_TEST(num_sieve);
    
    // 三角函数测试
    std::cout << "\n--- Trigonometry ---" << std::endl;
    RUN_TEST(trig_deg_rad);
    RUN_TEST(trig_safe_functions);
    RUN_TEST(trig_hyperbolic);
    
    // 数值计算测试
    std::cout << "\n--- Numerical Methods ---" << std::endl;
    RUN_TEST(num_sqrt_newton);
    RUN_TEST(num_bisection);
    RUN_TEST(num_integration);
    
    // 向量操作测试
    std::cout << "\n--- Vector Operations ---" << std::endl;
    RUN_TEST(vec_add_sub);
    RUN_TEST(vec_scale);
    RUN_TEST(vec_dot);
    RUN_TEST(vec_magnitude_normalize);
    RUN_TEST(vec_cross);
    RUN_TEST(vec_angle);
    
    // 比较和映射函数测试
    std::cout << "\n--- Comparison & Mapping ---" << std::endl;
    RUN_TEST(compare_approx);
    RUN_TEST(map_range);
    
    // 输出结果
    std::cout << "\n========================================" << std::endl;
    std::cout << "  Results: " << testsPassed << " passed, " << testsFailed << " failed" << std::endl;
    std::cout << "========================================\n" << std::endl;
    
    return testsFailed > 0 ? 1 : 0;
}