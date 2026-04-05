-- ============================================================================
-- SQL Math Utilities Module
-- Location: SQL/math_utils/mod.sql
-- Description: A comprehensive mathematical utility module for SQL providing common
--              mathematical functions, statistical calculations, and numeric operations.
--              Zero dependencies, uses only standard SQL.
-- ============================================================================

-- ============================================================================
-- Basic Mathematical Functions
-- ============================================================================

-- Calculate absolute value
-- Usage: SELECT math_abs(-5); -- Returns: 5
DELIMITER //
CREATE FUNCTION IF NOT EXISTS math_abs(val DECIMAL(38, 10))
RETURNS DECIMAL(38, 10)
DETERMINISTIC
NO SQL
BEGIN
    IF val < 0 THEN
        RETURN -val;
    END IF;
    RETURN val;
END //
DELIMITER ;

-- Calculate sign of a number (-1, 0, or 1)
-- Usage: SELECT math_sign(-5); -- Returns: -1
DELIMITER //
CREATE FUNCTION IF NOT EXISTS math_sign(val DECIMAL(38, 10))
RETURNS INT
DETERMINISTIC
NO SQL
BEGIN
    IF val > 0 THEN
        RETURN 1;
    ELSEIF val < 0 THEN
        RETURN -1;
    ELSE
        RETURN 0;
    END IF;
END //
DELIMITER ;

-- Calculate minimum of two values
-- Usage: SELECT math_min(5, 3); -- Returns: 3
DELIMITER //
CREATE FUNCTION IF NOT EXISTS math_min(a DECIMAL(38, 10), b DECIMAL(38, 10))
RETURNS DECIMAL(38, 10)
DETERMINISTIC
NO SQL
BEGIN
    IF a < b THEN
        RETURN a;
    END IF;
    RETURN b;
END //
DELIMITER ;

-- Calculate maximum of two values
-- Usage: SELECT math_max(5, 3); -- Returns: 5
DELIMITER //
CREATE FUNCTION IF NOT EXISTS math_max(a DECIMAL(38, 10), b DECIMAL(38, 10))
RETURNS DECIMAL(38, 10)
DETERMINISTIC
NO SQL
BEGIN
    IF a > b THEN
        RETURN a;
    END IF;
    RETURN b;
END //
DELIMITER ;

-- Clamp value between min and max
-- Usage: SELECT math_clamp(15, 0, 10); -- Returns: 10
DELIMITER //
CREATE FUNCTION IF NOT EXISTS math_clamp(val DECIMAL(38, 10), min_val DECIMAL(38, 10), max_val DECIMAL(38, 10))
RETURNS DECIMAL(38, 10)
DETERMINISTIC
NO SQL
BEGIN
    IF val < min_val THEN
        RETURN min_val;
    ELSEIF val > max_val THEN
        RETURN max_val;
    END IF;
    RETURN val;
END //
DELIMITER ;

-- ============================================================================
-- Rounding Functions
-- ============================================================================

-- Round to nearest integer
-- Usage: SELECT math_round(3.7); -- Returns: 4
DELIMITER //
CREATE FUNCTION IF NOT EXISTS math_round(val DECIMAL(38, 10))
RETURNS DECIMAL(38, 10)
DETERMINISTIC
NO SQL
BEGIN
    RETURN ROUND(val, 0);
END //
DELIMITER ;

-- Round to specific decimal places
-- Usage: SELECT math_round_to(3.14159, 2); -- Returns: 3.14
DELIMITER //
CREATE FUNCTION IF NOT EXISTS math_round_to(val DECIMAL(38, 10), places INT)
RETURNS DECIMAL(38, 10)
DETERMINISTIC
NO SQL
BEGIN
    RETURN ROUND(val, places);
END //
DELIMITER ;

-- Floor (round down)
-- Usage: SELECT math_floor(3.7); -- Returns: 3
DELIMITER //
CREATE FUNCTION IF NOT EXISTS math_floor(val DECIMAL(38, 10))
RETURNS DECIMAL(38, 10)
DETERMINISTIC
NO SQL
BEGIN
    RETURN FLOOR(val);
END //
DELIMITER ;

-- Ceiling (round up)
-- Usage: SELECT math_ceil(3.2); -- Returns: 4
DELIMITER //
CREATE FUNCTION IF NOT EXISTS math_ceil(val DECIMAL(38, 10))
RETURNS DECIMAL(38, 10)
DETERMINISTIC
NO SQL
BEGIN
    RETURN CEILING(val);
END //
DELIMITER ;

-- ============================================================================
-- Power and Root Functions
-- ============================================================================

-- Calculate power
-- Usage: SELECT math_pow(2, 3); -- Returns: 8
DELIMITER //
CREATE FUNCTION IF NOT EXISTS math_pow(base DECIMAL(38, 10), exponent DECIMAL(38, 10))
RETURNS DECIMAL(38, 10)
DETERMINISTIC
NO SQL
BEGIN
    RETURN POWER(base, exponent);
END //
DELIMITER ;

-- Calculate square root
-- Usage: SELECT math_sqrt(16); -- Returns: 4
DELIMITER //
CREATE FUNCTION IF NOT EXISTS math_sqrt(val DECIMAL(38, 10))
RETURNS DECIMAL(38, 10)
DETERMINISTIC
NO SQL
BEGIN
    RETURN SQRT(val);
END //
DELIMITER ;

-- Calculate cube root
-- Usage: SELECT math_cbrt(27); -- Returns: 3
DELIMITER //
CREATE FUNCTION IF NOT EXISTS math_cbrt(val DECIMAL(38, 10))
RETURNS DECIMAL(38, 10)
DETERMINISTIC
NO SQL
BEGIN
    RETURN POWER(val, 1.0 / 3.0);
END //
DELIMITER ;

-- Calculate nth root
-- Usage: SELECT math_nth_root(16, 4); -- Returns: 2
DELIMITER //
CREATE FUNCTION IF NOT EXISTS math_nth_root(val DECIMAL(38, 10), n INT)
RETURNS DECIMAL(38, 10)
DETERMINISTIC
NO SQL
BEGIN
    RETURN POWER(val, 1.0 / n);
END //
DELIMITER ;

-- ============================================================================
-- Trigonometric Functions
-- ============================================================================

-- Convert degrees to radians
-- Usage: SELECT math_degrees_to_radians(180); -- Returns: 3.14159...
DELIMITER //
CREATE FUNCTION IF NOT EXISTS math_degrees_to_radians(degrees DECIMAL(38, 10))
RETURNS DECIMAL(38, 10)
DETERMINISTIC
NO SQL
BEGIN
    RETURN degrees * PI() / 180.0;
END //
DELIMITER ;

-- Convert radians to degrees
-- Usage: SELECT math_radians_to_degrees(PI()); -- Returns: 180
DELIMITER //
CREATE FUNCTION IF NOT EXISTS math_radians_to_degrees(radians DECIMAL(38, 10))
RETURNS DECIMAL(38, 10)
DETERMINISTIC
NO SQL
BEGIN
    RETURN radians * 180.0 / PI();
END //
DELIMITER ;

-- Sine of angle in degrees
-- Usage: SELECT math_sin_deg(90); -- Returns: 1
DELIMITER //
CREATE FUNCTION IF NOT EXISTS math_sin_deg(degrees DECIMAL(38, 10))
RETURNS DECIMAL(38, 10)
DETERMINISTIC
NO SQL
BEGIN
    RETURN SIN(degrees * PI() / 180.0);
END //
DELIMITER ;

-- Cosine of angle in degrees
-- Usage: SELECT math_cos_deg(0); -- Returns: 1
DELIMITER //
CREATE FUNCTION IF NOT EXISTS math_cos_deg(degrees DECIMAL(38, 10))
RETURNS DECIMAL(38, 10)
DETERMINISTIC
NO SQL
BEGIN
    RETURN COS(degrees * PI() / 180.0);
END //
DELIMITER ;

-- Tangent of angle in degrees
-- Usage: SELECT math_tan_deg(45); -- Returns: 1
DELIMITER //
CREATE FUNCTION IF NOT EXISTS math_tan_deg(degrees DECIMAL(38, 10))
RETURNS DECIMAL(38, 10)
DETERMINISTIC
NO SQL
BEGIN
    RETURN TAN(degrees * PI() / 180.0);
END //
DELIMITER ;

-- ============================================================================
-- Logarithmic Functions
-- ============================================================================

-- Natural logarithm (base e)
-- Usage: SELECT math_ln(2.71828); -- Returns: ~1
DELIMITER //
CREATE FUNCTION IF NOT EXISTS math_ln(val DECIMAL(38, 10))
RETURNS DECIMAL(38, 10)
DETERMINISTIC
NO SQL
BEGIN
    RETURN LN(val);
END //
DELIMITER ;

-- Logarithm base 10
-- Usage: SELECT math_log10(100); -- Returns: 2
DELIMITER //
CREATE FUNCTION IF NOT EXISTS math_log10(val DECIMAL(38, 10))
RETURNS DECIMAL(38, 10)
DETERMINISTIC
NO SQL
BEGIN
    RETURN LOG10(val);
END //
DELIMITER ;

-- Logarithm with custom base
-- Usage: SELECT math_log(8, 2); -- Returns: 3
DELIMITER //
CREATE FUNCTION IF NOT EXISTS math_log(val DECIMAL(38, 10), base DECIMAL(38, 10))
RETURNS DECIMAL(38, 10)
DETERMINISTIC
NO SQL
BEGIN
    RETURN LN(val) / LN(base);
END //
DELIMITER ;

-- ============================================================================
-- Percentage and Ratio Functions
-- ============================================================================

-- Calculate percentage
-- Usage: SELECT math_percentage(25, 100); -- Returns: 25 (25% of 100)
DELIMITER //
CREATE FUNCTION IF NOT EXISTS math_percentage(part DECIMAL(38, 10), whole DECIMAL(38, 10))
RETURNS DECIMAL(38, 10)
DETERMINISTIC
NO SQL
BEGIN
    IF whole = 0 THEN
        RETURN 0;
    END IF;
    RETURN (part / whole) * 100;
END //
DELIMITER ;

-- Calculate percentage change
-- Usage: SELECT math_pct_change(100, 125); -- Returns: 25 (25% increase)
DELIMITER //
CREATE FUNCTION IF NOT EXISTS math_pct_change(old_val DECIMAL(38, 10), new_val DECIMAL(38, 10))
RETURNS DECIMAL(38, 10)
DETERMINISTIC
NO SQL
BEGIN
    IF old_val = 0 THEN
        RETURN 0;
    END IF;
    RETURN ((new_val - old_val) / old_val) * 100;
END //
DELIMITER ;

-- Calculate what percentage a value is of another
-- Usage: SELECT math_pct_of(50, 200); -- Returns: 25 (50 is 25% of 200)
DELIMITER //
CREATE FUNCTION IF NOT EXISTS math_pct_of(val DECIMAL(38, 10), total DECIMAL(38, 10))
RETURNS DECIMAL(38, 10)
DETERMINISTIC
NO SQL
BEGIN
    IF total = 0 THEN
        RETURN 0;
    END IF;
    RETURN (val / total) * 100;
END //
DELIMITER ;

-- ============================================================================
-- GCD and LCM Functions
-- ============================================================================

-- Calculate GCD (Greatest Common Divisor) using Euclidean algorithm
-- Usage: SELECT math_gcd(48, 18); -- Returns: 6
DELIMITER //
CREATE FUNCTION IF NOT EXISTS math_gcd(a INT, b INT)
RETURNS INT
DETERMINISTIC
NO SQL
BEGIN
    DECLARE temp INT;
    SET a = ABS(a);
    SET b = ABS(b);
    WHILE b != 0 DO
        SET temp = b;
        SET b = a MOD b;
        SET a = temp;
    END WHILE;
    RETURN a;
END //
DELIMITER ;

-- Calculate LCM (Least Common Multiple)
-- Usage: SELECT math_lcm(4, 6); -- Returns: 12
DELIMITER //
CREATE FUNCTION IF NOT EXISTS math_lcm(a INT, b INT)
RETURNS INT
DETERMINISTIC
NO SQL
BEGIN
    IF a = 0 OR b = 0 THEN
        RETURN 0;
    END IF;
    RETURN ABS(a * b) / math_gcd(a, b);
END //
DELIMITER ;

-- ============================================================================
-- Random Number Functions
-- ============================================================================

-- Generate random integer between min and max (inclusive)
-- Usage: SELECT math_random_int(1, 100); -- Returns: random number between 1 and 100
DELIMITER //
CREATE FUNCTION IF NOT EXISTS math_random_int(min_val INT, max_val INT)
RETURNS INT
NOT DETERMINISTIC
NO SQL
BEGIN
    RETURN FLOOR(min_val + (RAND() * (max_val - min_val + 1)));
END //
DELIMITER ;

-- Generate random decimal between 0 and 1
-- Usage: SELECT math_random(); -- Returns: random decimal 0-1
DELIMITER //
CREATE FUNCTION IF NOT EXISTS math_random()
RETURNS DECIMAL(38, 10)
NOT DETERMINISTIC
NO SQL
BEGIN
    RETURN RAND();
END //
DELIMITER ;

-- ============================================================================
-- Validation Functions
-- ============================================================================

-- Check if number is even
-- Usage: SELECT math_is_even(4); -- Returns: 1 (true)
DELIMITER //
CREATE FUNCTION IF NOT EXISTS math_is_even(n INT)
RETURNS BOOLEAN
DETERMINISTIC
NO SQL
BEGIN
    RETURN n MOD 2 = 0;
END //
DELIMITER ;

-- Check if number is odd
-- Usage: SELECT math_is_odd(5); -- Returns: 1 (true)
DELIMITER //
CREATE FUNCTION IF NOT EXISTS math_is_odd(n INT)
RETURNS BOOLEAN
DETERMINISTIC
NO SQL
BEGIN
    RETURN n MOD 2 != 0;
END //
DELIMITER ;

-- Check if number is prime
-- Usage: SELECT math_is_prime(7); -- Returns: 1 (true)
DELIMITER //
CREATE FUNCTION IF NOT EXISTS math_is_prime(n INT)
RETURNS BOOLEAN
DETERMINISTIC
NO SQL
BEGIN
    DECLARE i INT DEFAULT 2;
    IF n <= 1 THEN
        RETURN FALSE;
    END IF;
    IF n = 2 THEN
        RETURN TRUE;
    END IF;
    IF n MOD 2 = 0 THEN
        RETURN FALSE;
    END IF;
    SET i = 3;
    WHILE i * i <= n DO
        IF n MOD i = 0 THEN
            RETURN FALSE;
        END IF;
        SET i = i + 2;
    END WHILE;
    RETURN TRUE;
END //
DELIMITER ;

-- Check if number is perfect square
-- Usage: SELECT math_is_perfect_square(16); -- Returns: 1 (true)
DELIMITER //
CREATE FUNCTION IF NOT EXISTS math_is_perfect_square(n INT)
RETURNS BOOLEAN
DETERMINISTIC
NO SQL
BEGIN
    DECLARE root INT;
    SET root = FLOOR(SQRT(n));
    RETURN root * root = n;
END //
DELIMITER ;

-- ============================================================================
-- Number Formatting Functions
-- ============================================================================

-- Format number with thousands separator
-- Usage: SELECT math_format_number(1234567.89); -- Returns: '1,234,567.89'
DELIMITER //
CREATE FUNCTION IF NOT EXISTS math_format_number(n DECIMAL(38, 10))
RETURNS VARCHAR(50)
DETERMINISTIC
NO SQL
BEGIN
    RETURN FORMAT(n, 0);
END //
DELIMITER ;

-- Format as currency
-- Usage: SELECT math_format_currency(1234.5); -- Returns: '$1,234.50'
DELIMITER //
CREATE FUNCTION IF NOT EXISTS math_format_currency(amount DECIMAL(38, 10), currency_symbol VARCHAR(10))
RETURNS VARCHAR(50)
DETERMINISTIC
NO SQL
BEGIN
    IF currency_symbol IS NULL THEN
        SET currency_symbol = '$';
    END IF;
    RETURN CONCAT(currency_symbol, FORMAT(amount, 2));
END //
DELIMITER ;

-- ============================================================================
-- Distance Functions
-- ============================================================================

-- Calculate Euclidean distance between two points in 2D
-- Usage: SELECT math_distance_2d(0, 0, 3, 4); -- Returns: 5
DELIMITER //
CREATE FUNCTION IF NOT EXISTS math_distance_2d(x1 DECIMAL(38, 10), y1 DECIMAL(38, 10), x2 DECIMAL(38, 10), y2 DECIMAL(38, 10))
RETURNS DECIMAL(38, 10)
DETERMINISTIC
NO SQL
BEGIN
    RETURN SQRT(POWER(x2 - x1, 2) + POWER(y2 - y1, 2));
END //
DELIMITER ;

-- Calculate Manhattan distance between two points
-- Usage: SELECT math_manhattan_distance(0, 0, 3, 4); -- Returns: 7
DELIMITER //
CREATE FUNCTION IF NOT EXISTS math_manhattan_distance(x1 DECIMAL(38, 10), y1 DECIMAL(38, 10), x2 DECIMAL(38, 10), y2 DECIMAL(38, 10))
RETURNS DECIMAL(38, 10)
DETERMINISTIC
NO SQL
BEGIN
    RETURN ABS(x2 - x1) + ABS(y2 - y1);
END //
DELIMITER ;

-- ============================================================================
-- Statistical Functions (for single values/rows)
-- ============================================================================

-- Calculate mean of two values
-- Usage: SELECT math_mean(10, 20); -- Returns: 15
DELIMITER //
CREATE FUNCTION IF NOT EXISTS math_mean(a DECIMAL(38, 10), b DECIMAL(38, 10))
RETURNS DECIMAL(38, 10)
DETERMINISTIC
NO SQL
BEGIN
    RETURN (a + b) / 2;
END //
DELIMITER ;

-- Calculate mean of three values
-- Usage: SELECT math_mean3(10, 20, 30); -- Returns: 20
DELIMITER //
CREATE FUNCTION IF NOT EXISTS math_mean3(a DECIMAL(38, 10), b DECIMAL(38, 10), c DECIMAL(38, 10))
RETURNS DECIMAL(38, 10)
DETERMINISTIC
NO SQL
BEGIN
    RETURN (a + b + c) / 3;
END //
DELIMITER ;

-- Calculate variance of two values
-- Usage: SELECT math_variance(10, 20); -- Returns: 25
DELIMITER //
CREATE FUNCTION IF NOT EXISTS math_variance(a DECIMAL(38, 10), b DECIMAL(38, 10))
RETURNS DECIMAL(38, 10)
DETERMINISTIC
NO SQL
BEGIN
    DECLARE m DECIMAL(38, 10);
    SET m = (a + b) / 2;
    RETURN ((POWER(a - m, 2) + POWER(b - m, 2)) / 2);
END //
DELIMITER ;

-- Calculate standard deviation of two values
-- Usage: SELECT math_std_dev(10, 20); -- Returns: 5
DELIMITER //
CREATE FUNCTION IF NOT EXISTS math_std_dev(a DECIMAL(38, 10), b DECIMAL(38, 10))
RETURNS DECIMAL(38, 10)
DETERMINISTIC
NO SQL
BEGIN
    RETURN SQRT(math_variance(a, b));
END //
DELIMITER ;

-- ============================================================================
-- Linear Interpolation
-- ============================================================================

-- Linear interpolation between two values
-- Usage: SELECT math_lerp(0, 100, 0.5); -- Returns: 50
DELIMITER //
CREATE FUNCTION IF NOT EXISTS math_lerp(a DECIMAL(38, 10), b DECIMAL(38, 10), t DECIMAL(38, 10))
RETURNS DECIMAL(38, 10)
DETERMINISTIC
NO SQL
BEGIN
    RETURN a + (b - a) * t;
END //
DELIMITER ;

-- Map a value from one range to another
-- Usage: SELECT math_map(5, 0, 10, 0, 100); -- Returns: 50
DELIMITER //
CREATE FUNCTION IF NOT EXISTS math_map(val DECIMAL(38, 10), in_min DECIMAL(38, 10), in_max DECIMAL(38, 10), out_min DECIMAL(38, 10), out_max DECIMAL(38, 10))
RETURNS DECIMAL(38, 10)
DETERMINISTIC
NO SQL
BEGIN
    IF in_max = in_min THEN
        RETURN out_min;
    END IF;
    RETURN out_min + (val - in_min) * (out_max - out_min) / (in_max - in_min);
END //
DELIMITER ;

-- ============================================================================
-- Constants Functions
-- ============================================================================

-- Get PI value
-- Usage: SELECT math_pi(); -- Returns: 3.141592653589793
DELIMITER //
CREATE FUNCTION IF NOT EXISTS math_pi()
RETURNS DECIMAL(38, 15)
DETERMINISTIC
NO SQL
BEGIN
    RETURN 3.14159265358979323846;
END //
DELIMITER ;

-- Get E value (Euler's number)
-- Usage: SELECT math_e(); -- Returns: 2.718281828459045
DELIMITER //
CREATE FUNCTION IF NOT EXISTS math_e()
RETURNS DECIMAL(38, 15)
DETERMINISTIC
NO SQL
BEGIN
    RETURN 2.71828182845904523536;
END //
DELIMITER ;

-- ============================================================================
-- Module Complete
-- ============================================================================
