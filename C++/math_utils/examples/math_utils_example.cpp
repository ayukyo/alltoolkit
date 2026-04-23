/**
 * @file math_utils_example.cpp
 * @brief math_utils 使用示例
 * @author AllToolkit
 * @date 2026-04-24
 *
 * 编译: g++ -std=c++17 -o math_utils_example math_utils_example.cpp
 * 运行: ./math_utils_example
 */

#include "math_utils.hpp"
#include <iomanip>
#include <iostream>

using namespace alltoolkit::math_utils;

int main() {
    std::cout << "\n========================================" << std::endl;
    std::cout << "  AllToolkit C++ Math Utils Examples   " << std::endl;
    std::cout << "========================================\n" << std::endl;
    
    // ============================================================================
    // 常量演示
    // ============================================================================
    std::cout << "--- Constants ---" << std::endl;
    std::cout << "PI = " << std::setprecision(10) << PI << std::endl;
    std::cout << "E = " << E << std::endl;
    std::cout << "Golden Ratio (PHI) = " << PHI << std::endl;
    std::cout << "SQRT2 = " << SQRT2 << std::endl;
    std::cout << std::endl;
    
    // ============================================================================
    // 基础数学运算示例
    // ============================================================================
    std::cout << "--- Basic Math Operations ---" << std::endl;
    
    // 绝对值
    std::cout << "abs(-42) = " << abs(-42) << std::endl;
    
    // Clamp
    std::cout << "clamp(150, 0, 100) = " << clamp(150, 0, 100) << std::endl;
    
    // 线性插值
    std::cout << "lerp(0, 100, 0.5) = " << lerp(0.0, 100.0, 0.5) << std::endl;
    
    // 平滑插值
    std::cout << "smoothstep(0, 1, 0.25) = " << smoothstep(0.0, 1.0, 0.25) << std::endl;
    
    // 平方和立方
    std::cout << "square(7) = " << square(7) << std::endl;
    std::cout << "cube(3) = " << cube(3) << std::endl;
    
    // 符号
    std::cout << "sign(-10) = " << sign(-10) << std::endl;
    std::cout << "sign(10) = " << sign(10) << std::endl;
    std::cout << std::endl;
    
    // ============================================================================
    // 统计计算示例
    // ============================================================================
    std::cout << "--- Statistics ---" << std::endl;
    
    Vector<double> scores = {85, 90, 78, 92, 88, 76, 95, 82};
    
    std::cout << "Scores: ";
    for (auto s : scores) std::cout << s << " ";
    std::cout << std::endl;
    
    std::cout << "Mean: " << mean(scores) << std::endl;
    std::cout << "Median: " << median(scores) << std::endl;
    std::cout << "Std Dev: " << stdDev(scores) << std::endl;
    std::cout << "Range: " << range(scores) << std::endl;
    std::cout << "Sum: " << sum(scores) << std::endl;
    std::cout << std::endl;
    
    // ============================================================================
    // 几何计算示例
    // ============================================================================
    std::cout << "--- Geometry ---" << std::endl;
    
    double radius = 5.0;
    std::cout << "Circle with radius " << radius << ":" << std::endl;
    std::cout << "  Area = " << circleArea(radius) << std::endl;
    std::cout << "  Circumference = " << circleCircumference(radius) << std::endl;
    
    std::cout << "Sphere with radius " << radius << ":" << std::endl;
    std::cout << "  Volume = " << sphereVolume(radius) << std::endl;
    std::cout << "  Surface Area = " << sphereSurfaceArea(radius) << std::endl;
    
    std::cout << "Triangle (3, 4, 5): Area = " << triangleArea(3.0, 4.0, 5.0) << std::endl;
    std::cout << std::endl;
    
    // ============================================================================
    // 数论示例
    // ============================================================================
    std::cout << "--- Number Theory ---" << std::endl;
    
    std::cout << "gcd(48, 18) = " << gcd(48, 18) << std::endl;
    std::cout << "lcm(4, 6) = " << lcm(4, 6) << std::endl;
    
    std::cout << "Is 17 prime? " << (isPrime(17) ? "Yes" : "No") << std::endl;
    std::cout << "Is 18 prime? " << (isPrime(18) ? "Yes" : "No") << std::endl;
    
    std::cout << "factorial(10) = " << factorial(10) << std::endl;
    std::cout << "combination(10, 5) = C(10, 5) = " << combination(10, 5) << std::endl;
    
    std::cout << "Fibonacci sequence (0-10): ";
    for (int i = 0; i <= 10; ++i) {
        std::cout << fibonacci(i) << " ";
    }
    std::cout << std::endl;
    
    std::cout << "Primes up to 20: ";
    auto primes = sieveOfEratosthenes(20);
    for (auto p : primes) std::cout << p << " ";
    std::cout << std::endl;
    std::cout << std::endl;
    
    // ============================================================================
    // 三角函数示例
    // ============================================================================
    std::cout << "--- Trigonometry ---" << std::endl;
    
    std::cout << "degToRad(90) = " << degToRad(90.0) << " radians" << std::endl;
    std::cout << "radToDeg(PI/2) = " << radToDeg(PI / 2) << " degrees" << std::endl;
    
    std::cout << "sec(0) = " << sec(0.0) << std::endl;
    std::cout << "cot(PI/4) = " << cot(PI / 4) << std::endl;
    std::cout << std::endl;
    
    // ============================================================================
    // 数值计算示例
    // ============================================================================
    std::cout << "--- Numerical Methods ---" << std::endl;
    
    // 牛顿法平方根
    std::cout << "sqrtNewton(2) = " << sqrtNewton(2.0) << std::endl;
    std::cout << "std::sqrt(2) = " << std::sqrt(2.0) << std::endl;
    
    // 数值积分示例
    auto f = [](double x) { return x * x; };
    std::cout << "Integral of x^2 from 0 to 1 (Simpson): " << simpsonIntegration(f, 0.0, 1.0) << std::endl;
    std::cout << "Exact value: 1/3 = " << 1.0/3.0 << std::endl;
    
    // 二分法求解方程
    auto g = [](double x) { return x * x - 2; };
    auto root = bisectionMethod(g, 0.0, 2.0);
    if (root) {
        std::cout << "Root of x^2 - 2 = 0: " << root.value() << std::endl;
        std::cout << "sqrt(2) = " << std::sqrt(2.0) << std::endl;
    }
    std::cout << std::endl;
    
    // ============================================================================
    // 向量操作示例
    // ============================================================================
    std::cout << "--- Vector Operations ---" << std::endl;
    
    Vector<double> a = {1, 2, 3};
    Vector<double> b = {4, 5, 6};
    
    std::cout << "Vector a: {1, 2, 3}" << std::endl;
    std::cout << "Vector b: {4, 5, 6}" << std::endl;
    
    auto sum = vectorAdd(a, b);
    std::cout << "a + b = {" << sum[0] << ", " << sum[1] << ", " << sum[2] << "}" << std::endl;
    
    std::cout << "a · b = " << dotProduct(a, b) << std::endl;
    
    Vector<double> c = {3, 4};
    std::cout << "Vector {3, 4} magnitude = " << vectorMagnitude(c) << std::endl;
    
    auto norm = vectorNormalize(c);
    std::cout << "Normalized: {" << norm[0] << ", " << norm[1] << "}" << std::endl;
    
    Vector<double> x = {1, 0, 0};
    Vector<double> y = {0, 1, 0};
    auto cross = crossProduct3D(x, y);
    std::cout << "{1,0,0} × {0,1,0} = {" << cross[0] << ", " << cross[1] << ", " << cross[2] << "}" << std::endl;
    std::cout << std::endl;
    
    // ============================================================================
    // 映射函数示例
    // ============================================================================
    std::cout << "--- Mapping Functions ---" << std::endl;
    
    // 范围映射
    std::cout << "mapRange(50, 0, 100, 0, 255) = " << mapRange(50.0, 0.0, 100.0, 0.0, 255.0) << std::endl;
    
    // 归一化
    std::cout << "normalize(75, 0, 100) = " << normalize(75.0, 0.0, 100.0) << std::endl;
    
    std::cout << "\n========================================" << std::endl;
    std::cout << "  Examples Complete                    " << std::endl;
    std::cout << "========================================\n" << std::endl;
    
    return 0;
}