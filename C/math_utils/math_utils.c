/**
 * @file math_utils.c
 * @brief C 语言数学工具库实现
 * @author AllToolkit
 * @version 1.0.0
 * @date 2026-05-24
 */

#include "math_utils.h"
#include <math.h>
#include <stdlib.h>
#include <string.h>

/* ==================== 基础运算 ==================== */

int clamp_int(int value, int min, int max) {
    if (value < min) return min;
    if (value > max) return max;
    return value;
}

double clamp_double(double value, double min, double max) {
    if (value < min) return min;
    if (value > max) return max;
    return value;
}

int max_int(int a, int b) {
    return (a > b) ? a : b;
}

int max_int_array(const int* arr, size_t size) {
    if (arr == NULL || size == 0) return 0;
    int max_val = arr[0];
    for (size_t i = 1; i < size; i++) {
        if (arr[i] > max_val) max_val = arr[i];
    }
    return max_val;
}

double max_double(double a, double b) {
    return (a > b) ? a : b;
}

double max_double_array(const double* arr, size_t size) {
    if (arr == NULL || size == 0) return 0.0;
    double max_val = arr[0];
    for (size_t i = 1; i < size; i++) {
        if (arr[i] > max_val) max_val = arr[i];
    }
    return max_val;
}

int min_int(int a, int b) {
    return (a < b) ? a : b;
}

int min_int_array(const int* arr, size_t size) {
    if (arr == NULL || size == 0) return 0;
    int min_val = arr[0];
    for (size_t i = 1; i < size; i++) {
        if (arr[i] < min_val) min_val = arr[i];
    }
    return min_val;
}

double min_double(double a, double b) {
    return (a < b) ? a : b;
}

double min_double_array(const double* arr, size_t size) {
    if (arr == NULL || size == 0) return 0.0;
    double min_val = arr[0];
    for (size_t i = 1; i < size; i++) {
        if (arr[i] < min_val) min_val = arr[i];
    }
    return min_val;
}

void swap_int(int* a, int* b) {
    if (a == NULL || b == NULL) return;
    int temp = *a;
    *a = *b;
    *b = temp;
}

void swap_double(double* a, double* b) {
    if (a == NULL || b == NULL) return;
    double temp = *a;
    *a = *b;
    *b = temp;
}

int abs_int(int value) {
    return (value < 0) ? -value : value;
}

double abs_double(double value) {
    return (value < 0.0) ? -value : value;
}

int sign_int(int value) {
    if (value > 0) return 1;
    if (value < 0) return -1;
    return 0;
}

int sign_double(double value) {
    if (value > 0.0) return 1;
    if (value < 0.0) return -1;
    return 0;
}

/* ==================== 幂与根运算 ==================== */

long long power_int(int base, unsigned int exp) {
    long long result = 1;
    long long b = base;
    while (exp > 0) {
        if (exp & 1) result *= b;
        b *= b;
        exp >>= 1;
    }
    return result;
}

unsigned int isqrt(unsigned int n) {
    if (n == 0) return 0;
    unsigned int x = n;
    unsigned int y = (x + 1) / 2;
    while (y < x) {
        x = y;
        y = (x + n / x) / 2;
    }
    return x;
}

bool is_perfect_square(unsigned int n) {
    unsigned int root = isqrt(n);
    return root * root == n;
}

/* ==================== 几何计算 ==================== */

double distance_2d(double x1, double y1, double x2, double y2) {
    double dx = x2 - x1;
    double dy = y2 - y1;
    return sqrt(dx * dx + dy * dy);
}

double distance_3d(double x1, double y1, double z1, double x2, double y2, double z2) {
    double dx = x2 - x1;
    double dy = y2 - y1;
    double dz = z2 - z1;
    return sqrt(dx * dx + dy * dy + dz * dz);
}

double circle_area(double radius) {
    return 3.14159265358979323846 * radius * radius;
}

double circle_circumference(double radius) {
    return 2.0 * 3.14159265358979323846 * radius;
}

double rectangle_area(double width, double height) {
    return width * height;
}

double rectangle_perimeter(double width, double height) {
    return 2.0 * (width + height);
}

double triangle_area(double a, double b, double c) {
    double s = (a + b + c) / 2.0;
    double inner = s * (s - a) * (s - b) * (s - c);
    if (inner <= 0) return 0.0;
    return sqrt(inner);
}

double sphere_volume(double radius) {
    return (4.0 / 3.0) * 3.14159265358979323846 * radius * radius * radius;
}

double sphere_surface_area(double radius) {
    return 4.0 * 3.14159265358979323846 * radius * radius;
}

/* ==================== 统计函数 ==================== */

long long sum_int_array(const int* arr, size_t size) {
    if (arr == NULL || size == 0) return 0;
    long long sum = 0;
    for (size_t i = 0; i < size; i++) {
        sum += arr[i];
    }
    return sum;
}

double sum_double_array(const double* arr, size_t size) {
    if (arr == NULL || size == 0) return 0.0;
    double sum = 0.0;
    for (size_t i = 0; i < size; i++) {
        sum += arr[i];
    }
    return sum;
}

double mean_int_array(const int* arr, size_t size) {
    if (arr == NULL || size == 0) return 0.0;
    return (double)sum_int_array(arr, size) / (double)size;
}

double mean_double_array(const double* arr, size_t size) {
    if (arr == NULL || size == 0) return 0.0;
    return sum_double_array(arr, size) / (double)size;
}

/* 辅助函数：比较整数 */
static int compare_int(const void* a, const void* b) {
    return (*(int*)a - *(int*)b);
}

/* 辅助函数：比较浮点数 */
static int compare_double(const void* a, const void* b) {
    double diff = *(double*)a - *(double*)b;
    if (diff < 0) return -1;
    if (diff > 0) return 1;
    return 0;
}

double median_int_array(int* arr, size_t size) {
    if (arr == NULL || size == 0) return 0.0;
    qsort(arr, size, sizeof(int), compare_int);
    if (size % 2 == 0) {
        return (arr[size / 2 - 1] + arr[size / 2]) / 2.0;
    } else {
        return (double)arr[size / 2];
    }
}

double median_double_array(double* arr, size_t size) {
    if (arr == NULL || size == 0) return 0.0;
    qsort(arr, size, sizeof(double), compare_double);
    if (size % 2 == 0) {
        return (arr[size / 2 - 1] + arr[size / 2]) / 2.0;
    } else {
        return arr[size / 2];
    }
}

double variance_int_array(const int* arr, size_t size) {
    if (arr == NULL || size == 0) return 0.0;
    double mean = mean_int_array(arr, size);
    double variance = 0.0;
    for (size_t i = 0; i < size; i++) {
        double diff = arr[i] - mean;
        variance += diff * diff;
    }
    return variance / (double)size;
}

double variance_double_array(const double* arr, size_t size) {
    if (arr == NULL || size == 0) return 0.0;
    double mean = mean_double_array(arr, size);
    double variance = 0.0;
    for (size_t i = 0; i < size; i++) {
        double diff = arr[i] - mean;
        variance += diff * diff;
    }
    return variance / (double)size;
}

double std_dev_int_array(const int* arr, size_t size) {
    return sqrt(variance_int_array(arr, size));
}

double std_dev_double_array(const double* arr, size_t size) {
    return sqrt(variance_double_array(arr, size));
}

/* ==================== 数论函数 ==================== */

bool is_prime(unsigned int n) {
    if (n < 2) return false;
    if (n == 2) return true;
    if (n % 2 == 0) return false;
    for (unsigned int i = 3; i * i <= n; i += 2) {
        if (n % i == 0) return false;
    }
    return true;
}

unsigned int gcd(unsigned int a, unsigned int b) {
    while (b != 0) {
        unsigned int temp = b;
        b = a % b;
        a = temp;
    }
    return a;
}

unsigned int lcm(unsigned int a, unsigned int b) {
    if (a == 0 || b == 0) return 0;
    return (a / gcd(a, b)) * b;
}

unsigned long long factorial(unsigned int n) {
    if (n > 20) return 0;  /* 溢出保护 */
    unsigned long long result = 1;
    for (unsigned int i = 2; i <= n; i++) {
        result *= i;
    }
    return result;
}

unsigned long long fibonacci(unsigned int n) {
    if (n == 0) return 0;
    if (n == 1 || n == 2) return 1;
    
    unsigned long long prev = 1, curr = 1;
    for (unsigned int i = 3; i <= n; i++) {
        unsigned long long next = prev + curr;
        prev = curr;
        curr = next;
    }
    return curr;
}

int mod(int a, int b) {
    if (b == 0) return 0;
    int r = a % b;
    return (r < 0) ? r + b : r;
}

long long mod_power(long long base, long long exp, long long m) {
    if (m == 0) return 0;
    long long result = 1;
    base = base % m;
    if (base < 0) base += m;
    while (exp > 0) {
        if (exp & 1) {
            result = (result * base) % m;
        }
        exp >>= 1;
        base = (base * base) % m;
    }
    return result;
}

/* ==================== 数值检查 ==================== */

bool is_even(int n) {
    return (n & 1) == 0;
}

bool is_odd(int n) {
    return (n & 1) != 0;
}

bool is_power_of_two(unsigned int n) {
    return n != 0 && (n & (n - 1)) == 0;
}

bool is_near_zero(double value, double epsilon) {
    return value > -epsilon && value < epsilon;
}

bool is_approx_equal(double a, double b, double epsilon) {
    return is_near_zero(a - b, epsilon);
}

/* ==================== 范围与序列 ==================== */

double map_range(double value, double in_min, double in_max, double out_min, double out_max) {
    if (in_max == in_min) return out_min;
    return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}

double lerp(double a, double b, double t) {
    return a + t * (b - a);
}

void range_int(int* arr, size_t size, int start, int step) {
    if (arr == NULL) return;
    for (size_t i = 0; i < size; i++) {
        arr[i] = start + (int)i * step;
    }
}

/* ==================== 三角函数辅助 ==================== */

double degrees_to_radians(double degrees) {
    return degrees * 3.14159265358979323846 / 180.0;
}

double radians_to_degrees(double radians) {
    return radians * 180.0 / 3.14159265358979323846;
}