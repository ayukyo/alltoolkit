-- ============================================================================
-- SQL Math Utilities Example
-- Location: SQL/examples/math_utils_example.sql
-- Description: Practical usage examples for math_utils module
-- ============================================================================

-- Example 1: Basic Mathematical Operations
-- =======================================

-- Calculate absolute values
SELECT 'Absolute Values:' AS section;
SELECT math_abs(-42) AS abs_negative, math_abs(42) AS abs_positive, math_abs(0) AS abs_zero;

-- Find min/max values
SELECT 'Min/Max:' AS section;
SELECT math_min(100, 50) AS minimum, math_max(100, 50) AS maximum;

-- Clamp values to a range
SELECT 'Clamping:' AS section;
SELECT 
    math_clamp(150, 0, 100) AS clamped_high,
    math_clamp(-50, 0, 100) AS clamped_low,
    math_clamp(75, 0, 100) AS within_range;

-- Example 2: Rounding Operations
-- ==============================

SELECT 'Rounding:' AS section;
SELECT 
    math_round(3.7) AS rounded,
    math_floor(3.7) AS floored,
    math_ceil(3.2) AS ceiled,
    math_round_to(3.14159, 2) AS to_2_decimals;

-- Example 3: Power and Roots
-- ==========================

SELECT 'Power and Roots:' AS section;
SELECT 
    math_pow(2, 10) AS two_to_ten,
    math_sqrt(144) AS square_root,
    math_cbrt(27) AS cube_root,
    math_nth_root(16, 4) AS fourth_root;

-- Example 4: Trigonometry
-- =======================

SELECT 'Trigonometry (degrees):' AS section;
SELECT 
    math_sin_deg(30) AS sin_30,
    math_cos_deg(60) AS cos_60,
    math_tan_deg(45) AS tan_45;

-- Convert between degrees and radians
SELECT 'Angle Conversions:' AS section;
SELECT 
    math_degrees_to_radians(180) AS rad_from_180_deg,
    math_radians_to_degrees(PI()) AS deg_from_pi_rad;

-- Example 5: Logarithms
-- =====================

SELECT 'Logarithms:' AS section;
SELECT 
    math_ln(2.718281828) AS natural_log,
    math_log10(1000) AS log_base_10,
    math_log(64, 2) AS log_base_2;

-- Example 6: Percentage Calculations
-- ==================================

-- Calculate what percentage a value is
SELECT 'Percentages:' AS section;
SELECT 
    math_percentage(25, 100) AS pct_25_of_100,
    math_pct_change(100, 150) AS pct_increase,
    math_pct_change(100, 75) AS pct_decrease;

-- Example 7: Number Theory
-- ========================

SELECT 'GCD and LCM:' AS section;
SELECT 
    math_gcd(48, 18) AS gcd_result,
    math_lcm(4, 6) AS lcm_result;

SELECT 'Prime Check:' AS section;
SELECT 
    math_is_prime(7) AS is_7_prime,
    math_is_prime(8) AS is_8_prime,
    math_is_prime(97) AS is_97_prime;

SELECT 'Perfect Square:' AS section;
SELECT 
    math_is_perfect_square(16) AS is_16_ps,
    math_is_perfect_square(20) AS is_20_ps;

-- Example 8: Distance Calculations
-- ================================

SELECT 'Distance Calculations:' AS section;
-- Distance from origin to point (3, 4) - should be 5
SELECT 
    math_distance_2d(0, 0, 3, 4) AS euclidean_distance,
    math_manhattan_distance(0, 0, 3, 4) AS manhattan_distance;

-- Example 9: Interpolation and Mapping
-- ===================================

SELECT 'Interpolation:' AS section;
-- Find value halfway between 0 and 100
SELECT math_lerp(0, 100, 0.5) AS halfway;

-- Map a value from one range to another
-- 5 in range [0, 10] maps to 50 in range [0, 100]
SELECT math_map(5, 0, 10, 0, 100) AS mapped_value;

-- Example 10: Statistical Functions
-- =================================

SELECT 'Statistics:' AS section;
SELECT 
    math_mean(10, 20) AS mean_of_2,
    math_mean3(10, 20, 30) AS mean_of_3,
    math_std_dev(10, 20) AS std_dev;

-- Example 11: Using in Queries
-- ============================

-- Create a sample table for demonstration
CREATE TABLE IF NOT EXISTS products (
    id INT PRIMARY KEY,
    name VARCHAR(100),
    price DECIMAL(10, 2),
    discount_percent DECIMAL(5, 2)
);

-- Insert sample data
INSERT INTO products (id, name, price, discount_percent) VALUES
(1, 'Laptop', 999.99, 15),
(2, 'Mouse', 29.99, 10),
(3, 'Keyboard', 79.99, 20),
(4, 'Monitor', 299.99, 0),
(5, 'Webcam', 49.99, 5);

-- Calculate discounted prices using math functions
SELECT 
    name,
    price AS original_price,
    discount_percent,
    math_round_to(price * (1 - discount_percent/100), 2) AS discounted_price,
    math_round_to(price * discount_percent/100, 2) AS savings
FROM products;

-- Clamp discounts to valid range (0-100%)
SELECT 
    name,
    price,
    math_clamp(discount_percent, 0, 100) AS valid_discount
FROM products;

-- Example 12: Random Number Generation
-- ====================================

SELECT 'Random Numbers:' AS section;
-- Generate 5 random integers between 1 and 100
SELECT math_random_int(1, 100) AS random_num FROM (SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5) AS t;

-- Example 13: Constants
-- ====================

SELECT 'Mathematical Constants:' AS section;
SELECT 
    math_pi() AS pi_value,
    math_e() AS e_value;

-- Example 14: Validation in Queries
-- =================================

SELECT 'Validation Examples:' AS section;
SELECT 
    id,
    price,
    CASE 
        WHEN math_is_even(id) THEN 'Even ID'
        ELSE 'Odd ID'
    END AS id_parity,
    CASE 
        WHEN price > 100 THEN 'Expensive'
        ELSE 'Affordable'
    END AS price_category
FROM products;

-- Cleanup
DROP TABLE IF EXISTS products;

-- ============================================================================
-- End of Examples
-- ============================================================================
SELECT 'Examples completed successfully!' AS status;
