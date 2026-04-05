-- ============================================================================
-- SQL Math Utilities Test Suite
-- Location: SQL/math_utils/math_utils_test.sql
-- Description: Comprehensive tests for math_utils module
-- ============================================================================

-- Test Basic Functions
SELECT 'Testing math_abs' AS test;
SELECT math_abs(-5) = 5 AS test_abs_negative;
SELECT math_abs(5) = 5 AS test_abs_positive;
SELECT math_abs(0) = 0 AS test_abs_zero;

SELECT 'Testing math_sign' AS test;
SELECT math_sign(-5) = -1 AS test_sign_negative;
SELECT math_sign(5) = 1 AS test_sign_positive;
SELECT math_sign(0) = 0 AS test_sign_zero;

SELECT 'Testing math_min' AS test;
SELECT math_min(5, 3) = 3 AS test_min_basic;
SELECT math_min(-5, 3) = -5 AS test_min_negative;
SELECT math_min(5, 5) = 5 AS test_min_equal;

SELECT 'Testing math_max' AS test;
SELECT math_max(5, 3) = 5 AS test_max_basic;
SELECT math_max(-5, 3) = 3 AS test_max_negative;
SELECT math_max(5, 5) = 5 AS test_max_equal;

SELECT 'Testing math_clamp' AS test;
SELECT math_clamp(15, 0, 10) = 10 AS test_clamp_max;
SELECT math_clamp(-5, 0, 10) = 0 AS test_clamp_min;
SELECT math_clamp(5, 0, 10) = 5 AS test_clamp_within;

-- Test Rounding Functions
SELECT 'Testing math_round' AS test;
SELECT math_round(3.7) = 4 AS test_round_up;
SELECT math_round(3.2) = 3 AS test_round_down;
SELECT math_round(3.5) = 4 AS test_round_half;

SELECT 'Testing math_round_to' AS test;
SELECT math_round_to(3.14159, 2) = 3.14 AS test_round_to_2;
SELECT math_round_to(3.14159, 0) = 3 AS test_round_to_0;
SELECT math_round_to(3.14159, 4) = 3.1416 AS test_round_to_4;

SELECT 'Testing math_floor' AS test;
SELECT math_floor(3.7) = 3 AS test_floor_basic;
SELECT math_floor(-3.7) = -4 AS test_floor_negative;
SELECT math_floor(3) = 3 AS test_floor_integer;

SELECT 'Testing math_ceil' AS test;
SELECT math_ceil(3.2) = 4 AS test_ceil_basic;
SELECT math_ceil(-3.2) = -3 AS test_ceil_negative;
SELECT math_ceil(3) = 3 AS test_ceil_integer;

-- Test Power and Root Functions
SELECT 'Testing math_pow' AS test;
SELECT math_pow(2, 3) = 8 AS test_pow_basic;
SELECT math_pow(10, 0) = 1 AS test_pow_zero;
SELECT math_pow(2, -1) = 0.5 AS test_pow_negative;

SELECT 'Testing math_sqrt' AS test;
SELECT math_sqrt(16) = 4 AS test_sqrt_basic;
SELECT math_sqrt(0) = 0 AS test_sqrt_zero;
SELECT math_sqrt(2) > 1.4 AND math_sqrt(2) < 1.5 AS test_sqrt_irrational;

SELECT 'Testing math_cbrt' AS test;
SELECT math_cbrt(27) = 3 AS test_cbrt_basic;
SELECT math_cbrt(8) = 2 AS test_cbrt_8;
SELECT math_cbrt(-8) = -2 AS test_cbrt_negative;

SELECT 'Testing math_nth_root' AS test;
SELECT math_nth_root(16, 4) = 2 AS test_nth_root_4;
SELECT math_nth_root(32, 5) = 2 AS test_nth_root_5;
SELECT math_nth_root(81, 4) = 3 AS test_nth_root_3;

-- Test Trigonometric Functions
SELECT 'Testing math_degrees_to_radians' AS test;
SELECT ABS(math_degrees_to_radians(180) - PI()) < 0.0001 AS test_deg_to_rad;
SELECT ABS(math_degrees_to_radians(90) - PI()/2) < 0.0001 AS test_deg_to_rad_90;

SELECT 'Testing math_radians_to_degrees' AS test;
SELECT math_radians_to_degrees(PI()) = 180 AS test_rad_to_deg;
SELECT math_radians_to_degrees(PI()/2) = 90 AS test_rad_to_deg_90;

SELECT 'Testing math_sin_deg' AS test;
SELECT ABS(math_sin_deg(90) - 1) < 0.0001 AS test_sin_90;
SELECT ABS(math_sin_deg(0)) < 0.0001 AS test_sin_0;
SELECT ABS(math_sin_deg(30) - 0.5) < 0.0001 AS test_sin_30;

SELECT 'Testing math_cos_deg' AS test;
SELECT ABS(math_cos_deg(0) - 1) < 0.0001 AS test_cos_0;
SELECT ABS(math_cos_deg(90)) < 0.0001 AS test_cos_90;
SELECT ABS(math_cos_deg(60) - 0.5) < 0.0001 AS test_cos_60;

SELECT 'Testing math_tan_deg' AS test;
SELECT ABS(math_tan_deg(45) - 1) < 0.0001 AS test_tan_45;
SELECT ABS(math_tan_deg(0)) < 0.0001 AS test_tan_0;

-- Test Logarithmic Functions
SELECT 'Testing math_ln' AS test;
SELECT ABS(math_ln(2.718281828) - 1) < 0.001 AS test_ln_e;
SELECT math_ln(1) = 0 AS test_ln_1;

SELECT 'Testing math_log10' AS test;
SELECT math_log10(100) = 2 AS test_log10_100;
SELECT math_log10(1000) = 3 AS test_log10_1000;
SELECT math_log10(1) = 0 AS test_log10_1;

SELECT 'Testing math_log' AS test;
SELECT math_log(8, 2) = 3 AS test_log_base2;
SELECT math_log(27, 3) = 3 AS test_log_base3;
SELECT math_log(100, 10) = 2 AS test_log_base10;

-- Test Percentage Functions
SELECT 'Testing math_percentage' AS test;
SELECT math_percentage(25, 100) = 25 AS test_pct_basic;
SELECT math_percentage(50, 200) = 25 AS test_pct_50of200;
SELECT math_percentage(0, 100) = 0 AS test_pct_zero;

SELECT 'Testing math_pct_change' AS test;
SELECT math_pct_change(100, 125) = 25 AS test_pct_change_increase;
SELECT math_pct_change(100, 75) = -25 AS test_pct_change_decrease;
SELECT math_pct_change(100, 100) = 0 AS test_pct_change_same;

SELECT 'Testing math_pct_of' AS test;
SELECT math_pct_of(50, 200) = 25 AS test_pct_of_basic;
SELECT math_pct_of(100, 100) = 100 AS test_pct_of_full;

-- Test GCD and LCM
SELECT 'Testing math_gcd' AS test;
SELECT math_gcd(48, 18) = 6 AS test_gcd_basic;
SELECT math_gcd(54, 24) = 6 AS test_gcd_54_24;
SELECT math_gcd(7, 5) = 1 AS test_gcd_coprime;
SELECT math_gcd(-48, 18) = 6 AS test_gcd_negative;

SELECT 'Testing math_lcm' AS test;
SELECT math_lcm(4, 6) = 12 AS test_lcm_basic;
SELECT math_lcm(21, 6) = 42 AS test_lcm_21_6;
SELECT math_lcm(0, 5) = 0 AS test_lcm_zero;

-- Test Validation Functions
SELECT 'Testing math_is_even' AS test;
SELECT math_is_even(4) = 1 AS test_even_true;
SELECT math_is_even(5) = 0 AS test_even_false;
SELECT math_is_even(0) = 1 AS test_even_zero;

SELECT 'Testing math_is_odd' AS test;
SELECT math_is_odd(5) = 1 AS test_odd_true;
SELECT math_is_odd(4) = 0 AS test_odd_false;
SELECT math_is_odd(0) = 0 AS test_odd_zero;

SELECT 'Testing math_is_prime' AS test;
SELECT math_is_prime(7) = 1 AS test_prime_7;
SELECT math_is_prime(4) = 0 AS test_prime_4;
SELECT math_is_prime(1) = 0 AS test_prime_1;
SELECT math_is_prime(2) = 1 AS test_prime_2;

SELECT 'Testing math_is_perfect_square' AS test;
SELECT math_is_perfect_square(16) = 1 AS test_ps_16;
SELECT math_is_perfect_square(25) = 1 AS test_ps_25;
SELECT math_is_perfect_square(26) = 0 AS test_ps_26;

-- Test Distance Functions
SELECT 'Testing math_distance_2d' AS test;
SELECT math_distance_2d(0, 0, 3, 4) = 5 AS test_dist_3_4_5;
SELECT math_distance_2d(0, 0, 0, 0) = 0 AS test_dist_zero;
SELECT math_distance_2d(1, 1, 4, 5) = 5 AS test_dist_1_1_4_5;

SELECT 'Testing math_manhattan_distance' AS test;
SELECT math_manhattan_distance(0, 0, 3, 4) = 7 AS test_manhattan_3_4;
SELECT math_manhattan_distance(1, 1, 4, 5) = 7 AS test_manhattan_1_1;

-- Test Statistical Functions
SELECT 'Testing math_mean' AS test;
SELECT math_mean(10, 20) = 15 AS test_mean_2;
SELECT math_mean(0, 0) = 0 AS test_mean_zero;

SELECT 'Testing math_mean3' AS test;
SELECT math_mean3(10, 20, 30) = 20 AS test_mean3_basic;
SELECT math_mean3(5, 5, 5) = 5 AS test_mean3_same;

-- Test Interpolation Functions
SELECT 'Testing math_lerp' AS test;
SELECT math_lerp(0, 100, 0.5) = 50 AS test_lerp_half;
SELECT math_lerp(0, 100, 0) = 0 AS test_lerp_start;
SELECT math_lerp(0, 100, 1) = 100 AS test_lerp_end;

SELECT 'Testing math_map' AS test;
SELECT math_map(5, 0, 10, 0, 100) = 50 AS test_map_basic;
SELECT math_map(0, 0, 10, 0, 100) = 0 AS test_map_min;
SELECT math_map(10, 0, 10, 0, 100) = 100 AS test_map_max;

-- Test Constants
SELECT 'Testing math_pi' AS test;
SELECT ABS(math_pi() - 3.141592653589793) < 0.0000001 AS test_pi;

SELECT 'Testing math_e' AS test;
SELECT ABS(math_e() - 2.718281828459045) < 0.0000001 AS test_e;

-- ============================================================================
-- Test Summary
-- ============================================================================
SELECT 'All tests completed!' AS summary;
