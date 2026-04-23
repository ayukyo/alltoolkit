/**
 * @file math_utils.hpp
 * @brief C++ 数学工具库 - 零依赖、现代 C++17 实现
 * @author AllToolkit
 * @version 1.0.0
 * @date 2026-04-24
 *
 * 提供 40+ 个常用数学函数，涵盖：
 * - 基础数学运算（Basic Math）
 * - 统计计算（Statistics）
 * - 几何计算（Geometry）
 * - 数论函数（Number Theory）
 * - 三角函数扩展（Trigonometry）
 * - 数值计算（Numerical Methods）
 * - 向量/矩阵基础（Vector/Matrix Basics）
 * - 随机数辅助（Random Helpers）
 */

#ifndef ALLTOOLKIT_MATH_UTILS_HPP
#define ALLTOOLKIT_MATH_UTILS_HPP

#include <algorithm>
#include <cmath>
#include <limits>
#include <map>
#include <numeric>
#include <optional>
#include <stdexcept>
#include <type_traits>
#include <vector>

namespace alltoolkit {

/**
 * @brief 数学工具命名空间
 */
namespace math_utils {

// ============================================================================
// 常量定义
// ============================================================================

constexpr double PI = 3.14159265358979323846;
constexpr double E = 2.71828182845904523536;
constexpr double PHI = 1.61803398874989484820;  // 黄金比例
constexpr double SQRT2 = 1.41421356237309504880;
constexpr double SQRT3 = 1.73205080756887729352;
constexpr double LN2 = 0.69314718055994530942;
constexpr double LN10 = 2.30258509299404568402;
constexpr double DEG_TO_RAD = PI / 180.0;
constexpr double RAD_TO_DEG = 180.0 / PI;

// ============================================================================
// 类型别名
// ============================================================================

template <typename T>
using Vector = std::vector<T>;

// ============================================================================
// 类型判断辅助
// ============================================================================

template <typename T>
inline constexpr bool is_floating_point_v = std::is_floating_point_v<T>;

template <typename T>
inline constexpr bool is_integral_v = std::is_integral_v<T>;

template <typename T>
inline constexpr bool is_arithmetic_v = std::is_arithmetic_v<T>;

// ============================================================================
// 基础数学运算 (Basic Math Operations)
// ============================================================================

/**
 * @brief 计算绝对值
 * @param value 输入值
 * @return 绝对值
 */
template <typename T>
[[nodiscard]] inline constexpr T abs(T value) noexcept {
    return value < T(0) ? -value : value;
}

/**
 * @brief 计算两数中的最大值
 */
template <typename T>
[[nodiscard]] inline constexpr T max(T a, T b) noexcept {
    return a > b ? a : b;
}

/**
 * @brief 计算两数中的最小值
 */
template <typename T>
[[nodiscard]] inline constexpr T min(T a, T b) noexcept {
    return a < b ? a : b;
}

/**
 * @brief 将值限制在指定范围内
 * @param value 输入值
 * @param low 下界
 * @param high 上界
 * @return 限制后的值
 */
template <typename T>
[[nodiscard]] inline constexpr T clamp(T value, T low, T high) noexcept {
    return value < low ? low : (value > high ? high : value);
}

/**
 * @brief 线性插值
 * @param a 起始值
 * @param b 结束值
 * @param t 插值因子 [0, 1]
 * @return 插值结果
 */
template <typename T>
[[nodiscard]] inline constexpr T lerp(T a, T b, T t) noexcept {
    return a + t * (b - a);
}

/**
 * @brief 平滑插值（SmoothStep）
 * @param edge0 下边界
 * @param edge1 上边界
 * @param x 输入值
 * @return 平滑插值结果 [0, 1]
 */
template <typename T>
[[nodiscard]] inline T smoothstep(T edge0, T edge1, T x) noexcept {
    T t = clamp((x - edge0) / (edge1 - edge0), T(0), T(1));
    return t * t * (T(3) - T(2) * t);
}

/**
 * @brief 计算平方
 */
template <typename T>
[[nodiscard]] inline constexpr T square(T value) noexcept {
    return value * value;
}

/**
 * @brief 计算立方
 */
template <typename T>
[[nodiscard]] inline constexpr T cube(T value) noexcept {
    return value * value * value;
}

/**
 * @brief 计算整数幂
 * @param base 底数
 * @param exp 指数（非负整数）
 * @return 幂运算结果
 */
template <typename T>
[[nodiscard]] inline T power(T base, int exp) noexcept {
    if (exp < 0) return T(1) / power(base, -exp);
    T result = T(1);
    while (exp > 0) {
        if (exp & 1) result *= base;
        base *= base;
        exp >>= 1;
    }
    return result;
}

/**
 * @brief 计算符号 (-1, 0, 1)
 */
template <typename T>
[[nodiscard]] inline constexpr int sign(T value) noexcept {
    return (T(0) < value) - (value < T(0));
}

/**
 * @brief 计算两点之间的距离
 */
template <typename T>
[[nodiscard]] inline T distance(T x1, T y1, T x2, T y2) noexcept {
    return std::sqrt(square(x2 - x1) + square(y2 - y1));
}

/**
 * @brief 计算两点之间的距离（3D）
 */
template <typename T>
[[nodiscard]] inline T distance3D(T x1, T y1, T z1, T x2, T y2, T z2) noexcept {
    return std::sqrt(square(x2 - x1) + square(y2 - y1) + square(z2 - z1));
}

// ============================================================================
// 统计计算 (Statistics)
// ============================================================================

/**
 * @brief 计算平均值
 * @param data 数据容器
 * @return 平均值（空容器返回 0）
 */
template <typename T>
[[nodiscard]] inline double mean(const Vector<T>& data) noexcept {
    if (data.empty()) return 0.0;
    double sum = std::accumulate(data.begin(), data.end(), 0.0);
    return sum / static_cast<double>(data.size());
}

/**
 * @brief 计算中位数
 * @param data 数据容器（会被修改）
 * @return 中位数
 */
template <typename T>
[[nodiscard]] inline double median(Vector<T>& data) {
    if (data.empty()) {
        throw std::invalid_argument("Cannot compute median of empty data");
    }
    size_t n = data.size();
    std::sort(data.begin(), data.end());
    if (n % 2 == 0) {
        return (static_cast<double>(data[n/2 - 1]) + static_cast<double>(data[n/2])) / 2.0;
    } else {
        return static_cast<double>(data[n/2]);
    }
}

/**
 * @brief 计算中位数（常量版本，不修改原数据）
 */
template <typename T>
[[nodiscard]] inline double median(const Vector<T>& data) {
    Vector<T> copy = data;
    return median(copy);
}

/**
 * @brief 计算方差（总体方差）
 * @param data 数据容器
 * @return 方差
 */
template <typename T>
[[nodiscard]] inline double variance(const Vector<T>& data) noexcept {
    if (data.size() < 2) return 0.0;
    double m = mean(data);
    double sum = 0.0;
    for (const auto& val : data) {
        sum += square(static_cast<double>(val) - m);
    }
    return sum / static_cast<double>(data.size());
}

/**
 * @brief 计算样本方差
 * @param data 数据容器
 * @return 样本方差
 */
template <typename T>
[[nodiscard]] inline double sampleVariance(const Vector<T>& data) noexcept {
    if (data.size() < 2) return 0.0;
    double m = mean(data);
    double sum = 0.0;
    for (const auto& val : data) {
        sum += square(static_cast<double>(val) - m);
    }
    return sum / static_cast<double>(data.size() - 1);
}

/**
 * @brief 计算标准差
 */
template <typename T>
[[nodiscard]] inline double stdDev(const Vector<T>& data) noexcept {
    return std::sqrt(variance(data));
}

/**
 * @brief 计算样本标准差
 */
template <typename T>
[[nodiscard]] inline double sampleStdDev(const Vector<T>& data) noexcept {
    return std::sqrt(sampleVariance(data));
}

/**
 * @brief 计算协方差
 */
template <typename T>
[[nodiscard]] inline double covariance(const Vector<T>& x, const Vector<T>& y) {
    if (x.size() != y.size() || x.size() < 2) {
        throw std::invalid_argument("Vectors must have same size and at least 2 elements");
    }
    double mx = mean(x);
    double my = mean(y);
    double sum = 0.0;
    for (size_t i = 0; i < x.size(); ++i) {
        sum += (static_cast<double>(x[i]) - mx) * (static_cast<double>(y[i]) - my);
    }
    return sum / static_cast<double>(x.size() - 1);
}

/**
 * @brief 计算皮尔逊相关系数
 */
template <typename T>
[[nodiscard]] inline double correlation(const Vector<T>& x, const Vector<T>& y) {
    if (x.size() != y.size() || x.size() < 2) {
        throw std::invalid_argument("Vectors must have same size and at least 2 elements");
    }
    double sx = sampleStdDev(x);
    double sy = sampleStdDev(y);
    if (sx < 1e-10 || sy < 1e-10) return 0.0;
    return covariance(x, y) / (sx * sy);
}

/**
 * @brief 计算众数
 */
template <typename T>
[[nodiscard]] inline Vector<T> mode(const Vector<T>& data) {
    if (data.empty()) return {};
    
    std::map<T, size_t> freq;
    for (const auto& val : data) {
        freq[val]++;
    }
    
    size_t maxCount = 0;
    for (const auto& [val, count] : freq) {
        maxCount = max(maxCount, count);
    }
    
    Vector<T> result;
    for (const auto& [val, count] : freq) {
        if (count == maxCount) {
            result.push_back(val);
        }
    }
    return result;
}

/**
 * @brief 计算范围（极差）
 */
template <typename T>
[[nodiscard]] inline T range(const Vector<T>& data) {
    if (data.empty()) {
        throw std::invalid_argument("Cannot compute range of empty data");
    }
    auto [minIt, maxIt] = std::minmax_element(data.begin(), data.end());
    return *maxIt - *minIt;
}

/**
 * @brief 计算数据总和
 */
template <typename T>
[[nodiscard]] inline T sum(const Vector<T>& data) noexcept {
    return std::accumulate(data.begin(), data.end(), T(0));
}

/**
 * @brief 计算数据乘积
 */
template <typename T>
[[nodiscard]] inline T product(const Vector<T>& data) noexcept {
    if (data.empty()) return T(1);
    return std::accumulate(data.begin(), data.end(), T(1), std::multiplies<T>());
}

// ============================================================================
// 几何计算 (Geometry)
// ============================================================================

/**
 * @brief 计算圆的面积
 */
template <typename T>
[[nodiscard]] inline constexpr T circleArea(T radius) noexcept {
    return static_cast<T>(PI) * radius * radius;
}

/**
 * @brief 计算圆的周长
 */
template <typename T>
[[nodiscard]] inline constexpr T circleCircumference(T radius) noexcept {
    return static_cast<T>(2) * static_cast<T>(PI) * radius;
}

/**
 * @brief 计算矩形面积
 */
template <typename T>
[[nodiscard]] inline constexpr T rectangleArea(T width, T height) noexcept {
    return width * height;
}

/**
 * @brief 计算矩形周长
 */
template <typename T>
[[nodiscard]] inline constexpr T rectanglePerimeter(T width, T height) noexcept {
    return T(2) * (width + height);
}

/**
 * @brief 计算三角形面积（海伦公式）
 */
template <typename T>
[[nodiscard]] inline T triangleArea(T a, T b, T c) {
    T s = (a + b + c) / T(2);
    return std::sqrt(s * (s - a) * (s - b) * (s - c));
}

/**
 * @brief 计算三角形面积（底高公式）
 */
template <typename T>
[[nodiscard]] inline constexpr T triangleArea(T base, T height) noexcept {
    return base * height / T(2);
}

/**
 * @brief 计算球体体积
 */
template <typename T>
[[nodiscard]] inline constexpr T sphereVolume(T radius) noexcept {
    return (T(4) / T(3)) * static_cast<T>(PI) * radius * radius * radius;
}

/**
 * @brief 计算球体表面积
 */
template <typename T>
[[nodiscard]] inline constexpr T sphereSurfaceArea(T radius) noexcept {
    return T(4) * static_cast<T>(PI) * radius * radius;
}

/**
 * @brief 计算圆柱体体积
 */
template <typename T>
[[nodiscard]] inline constexpr T cylinderVolume(T radius, T height) noexcept {
    return static_cast<T>(PI) * radius * radius * height;
}

/**
 * @brief 判断点是否在圆内
 */
template <typename T>
[[nodiscard]] inline bool pointInCircle(T px, T py, T cx, T cy, T radius) noexcept {
    return distance(px, py, cx, cy) <= radius;
}

/**
 * @brief 判断点是否在矩形内
 */
template <typename T>
[[nodiscard]] inline constexpr bool pointInRect(T px, T py, T rx, T ry, T width, T height) noexcept {
    return px >= rx && px <= rx + width && py >= ry && py <= ry + height;
}

// ============================================================================
// 数论函数 (Number Theory)
// ============================================================================

/**
 * @brief 计算最大公约数
 */
template <typename T>
[[nodiscard]] inline constexpr T gcd(T a, T b) noexcept {
    while (b != T(0)) {
        T temp = b;
        b = a % b;
        a = temp;
    }
    return a;
}

/**
 * @brief 计算最小公倍数
 */
template <typename T>
[[nodiscard]] inline constexpr T lcm(T a, T b) noexcept {
    if (a == T(0) || b == T(0)) return T(0);
    return (a / gcd(a, b)) * b;
}

/**
 * @brief 判断是否为素数
 */
[[nodiscard]] inline bool isPrime(int n) noexcept {
    if (n < 2) return false;
    if (n == 2) return true;
    if (n % 2 == 0) return false;
    for (int i = 3; i * i <= n; i += 2) {
        if (n % i == 0) return false;
    }
    return true;
}

/**
 * @brief 获取所有小于等于 n 的素数
 */
[[nodiscard]] inline Vector<int> sieveOfEratosthenes(int n) {
    if (n < 2) return {};
    
    Vector<bool> isPrimeVec(n + 1, true);
    isPrimeVec[0] = isPrimeVec[1] = false;
    
    for (int i = 2; i * i <= n; ++i) {
        if (isPrimeVec[i]) {
            for (int j = i * i; j <= n; j += i) {
                isPrimeVec[j] = false;
            }
        }
    }
    
    Vector<int> primes;
    for (int i = 2; i <= n; ++i) {
        if (isPrimeVec[i]) {
            primes.push_back(i);
        }
    }
    return primes;
}

/**
 * @brief 计算阶乘
 */
[[nodiscard]] inline unsigned long long factorial(int n) noexcept {
    if (n < 0) return 0;
    if (n <= 1) return 1;
    unsigned long long result = 1;
    for (int i = 2; i <= n; ++i) {
        result *= i;
    }
    return result;
}

/**
 * @brief 计算排列数 A(n, k)
 */
[[nodiscard]] inline unsigned long long permutation(int n, int k) noexcept {
    if (k < 0 || k > n) return 0;
    unsigned long long result = 1;
    for (int i = 0; i < k; ++i) {
        result *= (n - i);
    }
    return result;
}

/**
 * @brief 计算组合数 C(n, k)
 */
[[nodiscard]] inline unsigned long long combination(int n, int k) noexcept {
    if (k < 0 || k > n) return 0;
    if (k == 0 || k == n) return 1;
    k = min(k, n - k);
    unsigned long long result = 1;
    for (int i = 0; i < k; ++i) {
        result *= (n - i);
        result /= (i + 1);
    }
    return result;
}

/**
 * @brief 计算斐波那契数列第 n 项
 */
[[nodiscard]] inline unsigned long long fibonacci(int n) noexcept {
    if (n < 0) return 0;
    if (n <= 1) return static_cast<unsigned long long>(n);
    
    unsigned long long a = 0, b = 1;
    for (int i = 2; i <= n; ++i) {
        unsigned long long temp = a + b;
        a = b;
        b = temp;
    }
    return b;
}

// ============================================================================
// 三角函数扩展 (Extended Trigonometry)
// ============================================================================

/**
 * @brief 角度转弧度
 */
template <typename T>
[[nodiscard]] inline constexpr T degToRad(T degrees) noexcept {
    return degrees * static_cast<T>(DEG_TO_RAD);
}

/**
 * @brief 弧度转角度
 */
template <typename T>
[[nodiscard]] inline constexpr T radToDeg(T radians) noexcept {
    return radians * static_cast<T>(RAD_TO_DEG);
}

/**
 * @brief 安全的反正弦函数（值会被限制在 [-1, 1]）
 */
template <typename T>
[[nodiscard]] inline T safeAsin(T value) noexcept {
    return std::asin(clamp(value, T(-1), T(1)));
}

/**
 * @brief 安全的反余弦函数（值会被限制在 [-1, 1]）
 */
template <typename T>
[[nodiscard]] inline T safeAcos(T value) noexcept {
    return std::acos(clamp(value, T(-1), T(1)));
}

/**
 * @brief 计算正割 sec(x) = 1/cos(x)
 */
template <typename T>
[[nodiscard]] inline T sec(T radians) {
    T c = std::cos(radians);
    if (std::abs(c) < std::numeric_limits<T>::epsilon()) {
        throw std::overflow_error("secant undefined at this angle");
    }
    return T(1) / c;
}

/**
 * @brief 计算余割 csc(x) = 1/sin(x)
 */
template <typename T>
[[nodiscard]] inline T csc(T radians) {
    T s = std::sin(radians);
    if (std::abs(s) < std::numeric_limits<T>::epsilon()) {
        throw std::overflow_error("cosecant undefined at this angle");
    }
    return T(1) / s;
}

/**
 * @brief 计算余切 cot(x) = cos(x)/sin(x)
 */
template <typename T>
[[nodiscard]] inline T cot(T radians) {
    T s = std::sin(radians);
    if (std::abs(s) < std::numeric_limits<T>::epsilon()) {
        throw std::overflow_error("cotangent undefined at this angle");
    }
    return std::cos(radians) / s;
}

// ============================================================================
// 数值计算 (Numerical Methods)
// ============================================================================

/**
 * @brief 牛顿法求平方根
 */
template <typename T>
[[nodiscard]] inline T sqrtNewton(T value, int iterations = 20) noexcept {
    if (value < T(0)) return std::numeric_limits<T>::quiet_NaN();
    if (value == T(0)) return T(0);
    
    T x = value / T(2);
    for (int i = 0; i < iterations; ++i) {
        x = (x + value / x) / T(2);
    }
    return x;
}

/**
 * @brief 二分法求方程的根
 * @param f 函数
 * @param a 区间左端点
 * @param b 区间右端点
 * @param tolerance 容差
 * @param maxIterations 最大迭代次数
 * @return 根（如果存在）
 */
template <typename T, typename Func>
[[nodiscard]] inline std::optional<T> bisectionMethod(Func f, T a, T b, T tolerance = T(1e-10), int maxIterations = 100) {
    T fa = f(a);
    T fb = f(b);
    
    if (fa * fb > T(0)) return std::nullopt;
    
    for (int i = 0; i < maxIterations; ++i) {
        T c = (a + b) / T(2);
        T fc = f(c);
        
        if (std::abs(fc) < tolerance || (b - a) / T(2) < tolerance) {
            return c;
        }
        
        if (fa * fc < T(0)) {
            b = c;
            fb = fc;
        } else {
            a = c;
            fa = fc;
        }
    }
    return (a + b) / T(2);
}

/**
 * @brief 数值积分（梯形法则）
 */
template <typename T, typename Func>
[[nodiscard]] inline T trapezoidalIntegration(Func f, T a, T b, int n = 1000) {
    T h = (b - a) / n;
    T sum = (f(a) + f(b)) / T(2);
    
    for (int i = 1; i < n; ++i) {
        sum += f(a + i * h);
    }
    
    return sum * h;
}

/**
 * @brief 数值积分（辛普森法则）
 */
template <typename T, typename Func>
[[nodiscard]] inline T simpsonIntegration(Func f, T a, T b, int n = 1000) {
    if (n % 2 != 0) n++;
    T h = (b - a) / n;
    T sum = f(a) + f(b);
    
    for (int i = 1; i < n; ++i) {
        T coef = (i % 2 == 0) ? T(2) : T(4);
        sum += coef * f(a + i * h);
    }
    
    return sum * h / T(3);
}

// ============================================================================
// 向量基础操作 (Basic Vector Operations)
// ============================================================================

/**
 * @brief 向量加法
 */
template <typename T>
[[nodiscard]] inline Vector<T> vectorAdd(const Vector<T>& a, const Vector<T>& b) {
    if (a.size() != b.size()) {
        throw std::invalid_argument("Vectors must have the same size");
    }
    Vector<T> result(a.size());
    for (size_t i = 0; i < a.size(); ++i) {
        result[i] = a[i] + b[i];
    }
    return result;
}

/**
 * @brief 向量减法
 */
template <typename T>
[[nodiscard]] inline Vector<T> vectorSub(const Vector<T>& a, const Vector<T>& b) {
    if (a.size() != b.size()) {
        throw std::invalid_argument("Vectors must have the same size");
    }
    Vector<T> result(a.size());
    for (size_t i = 0; i < a.size(); ++i) {
        result[i] = a[i] - b[i];
    }
    return result;
}

/**
 * @brief 向量标量乘法
 */
template <typename T>
[[nodiscard]] inline Vector<T> vectorScale(const Vector<T>& v, T scalar) {
    Vector<T> result(v.size());
    for (size_t i = 0; i < v.size(); ++i) {
        result[i] = v[i] * scalar;
    }
    return result;
}

/**
 * @brief 向量点积
 */
template <typename T>
[[nodiscard]] inline T dotProduct(const Vector<T>& a, const Vector<T>& b) {
    if (a.size() != b.size()) {
        throw std::invalid_argument("Vectors must have the same size");
    }
    T result = T(0);
    for (size_t i = 0; i < a.size(); ++i) {
        result += a[i] * b[i];
    }
    return result;
}

/**
 * @brief 向量模长
 */
template <typename T>
[[nodiscard]] inline double vectorMagnitude(const Vector<T>& v) {
    return std::sqrt(static_cast<double>(dotProduct(v, v)));
}

/**
 * @brief 向量归一化
 */
template <typename T>
[[nodiscard]] inline Vector<double> vectorNormalize(const Vector<T>& v) {
    double mag = vectorMagnitude(v);
    if (mag < 1e-10) {
        throw std::invalid_argument("Cannot normalize zero vector");
    }
    Vector<double> result(v.size());
    for (size_t i = 0; i < v.size(); ++i) {
        result[i] = static_cast<double>(v[i]) / mag;
    }
    return result;
}

/**
 * @brief 3D 向量叉积
 */
template <typename T>
[[nodiscard]] inline Vector<T> crossProduct3D(const Vector<T>& a, const Vector<T>& b) {
    if (a.size() != 3 || b.size() != 3) {
        throw std::invalid_argument("Cross product requires 3D vectors");
    }
    return {
        a[1] * b[2] - a[2] * b[1],
        a[2] * b[0] - a[0] * b[2],
        a[0] * b[1] - a[1] * b[0]
    };
}

/**
 * @brief 向量夹角（弧度）
 */
template <typename T>
[[nodiscard]] inline double vectorAngle(const Vector<T>& a, const Vector<T>& b) {
    double dot = static_cast<double>(dotProduct(a, b));
    double magA = vectorMagnitude(a);
    double magB = vectorMagnitude(b);
    if (magA < 1e-10 || magB < 1e-10) {
        throw std::invalid_argument("Cannot compute angle with zero vector");
    }
    return safeAcos(dot / (magA * magB));
}

// ============================================================================
// 比较函数 (Comparison)
// ============================================================================

/**
 * @brief 判断两个浮点数是否近似相等
 */
template <typename T>
[[nodiscard]] inline bool approxEqual(T a, T b, T epsilon = T(1e-9)) noexcept {
    if constexpr (is_floating_point_v<T>) {
        return std::abs(a - b) < epsilon;
    } else {
        return a == b;
    }
}

/**
 * @brief 判断浮点数是否为零
 */
template <typename T>
[[nodiscard]] inline bool isZero(T value, T epsilon = T(1e-9)) noexcept {
    return std::abs(value) < epsilon;
}

/**
 * @brief 判断值是否在范围内
 */
template <typename T>
[[nodiscard]] inline constexpr bool inRange(T value, T low, T high) noexcept {
    return value >= low && value <= high;
}

// ============================================================================
// 映射函数 (Mapping Functions)
// ============================================================================

/**
 * @brief 将值从一个范围映射到另一个范围
 * @param value 输入值
 * @param inMin 输入范围最小值
 * @param inMax 输入范围最大值
 * @param outMin 输出范围最小值
 * @param outMax 输出范围最大值
 * @return 映射后的值
 */
template <typename T>
[[nodiscard]] inline T mapRange(T value, T inMin, T inMax, T outMin, T outMax) noexcept {
    return outMin + (value - inMin) * (outMax - outMin) / (inMax - inMin);
}

/**
 * @brief 将值归一化到 [0, 1]
 */
template <typename T>
[[nodiscard]] inline T normalize(T value, T minVal, T maxVal) noexcept {
    return (value - minVal) / (maxVal - minVal);
}

} // namespace math_utils

} // namespace alltoolkit

#endif // ALLTOOLKIT_MATH_UTILS_HPP