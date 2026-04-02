/// Example usage of math_utils module
///
/// Run with: rustc --edition 2021 example_math_utils.rs -L . && ./example_math_utils

mod math_utils;

use math_utils::*;

fn main() {
    println!("=== AllToolkit Math Utilities Demo ===\n");

    // 1. Clamp - limit values to a range
    println!("1. Clamp:");
    let raw_value = 150.0;
    let clamped = clamp(raw_value, 0.0, 100.0);
    println!("   clamp({}, 0, 100) = {}", raw_value, clamped);
    println!("   clamp({}, 0, 100) = {}", -10.0, clamp(-10.0, 0.0, 100.0));
    println!();

    // 2. Lerp - linear interpolation
    println!("2. Linear Interpolation (Lerp):");
    let start = 0.0;
    let end = 100.0;
    println!("   lerp({}, {}, 0.0) = {}", start, end, lerp(start, end, 0.0));
    println!("   lerp({}, {}, 0.5) = {}", start, end, lerp(start, end, 0.5));
    println!("   lerp({}, {}, 1.0) = {}", start, end, lerp(start, end, 1.0));
    println!();

    // 3. Map Range - convert between ranges
    println!("3. Map Range:");
    let celsius = map_range(98.6, 32.0, 212.0, 0.0, 100.0);
    println!("   98.6F in Celsius = {:.1}°C", celsius);
    let percent = map_range(7.5, 0.0, 10.0, 0.0, 100.0);
    println!("   7.5/10 as percentage = {:.0}%", percent);
    println!();

    // 4. Approximate Equality
    println!("4. Approximate Equality:");
    println!("   approx_eq(0.1 + 0.2, 0.3, 1e-10) = {}", approx_eq(0.1 + 0.2, 0.3, 1e-10));
    println!("   approx_eq(1.0, 1.001, 0.01) = {}", approx_eq(1.0, 1.001, 0.01));
    println!();

    // 5. Rounding
    println!("5. Round to Decimal Places:");
    let pi = 3.14159265359;
    println!("   round_to(PI, 2) = {}", round_to(pi, 2));
    println!("   round_to(PI, 4) = {}", round_to(pi, 4));
    println!();

    // 6. Statistical Functions
    println!("6. Statistics:");
    let data = [12.0, 15.0, 18.0, 21.0, 24.0];
    println!("   Data: {:?}", data);
    println!("   Mean = {:.1}", mean(&data).unwrap());
    println!("   Median = {:.1}", median(&data).unwrap());
    let (min, max) = min_max(&data).unwrap();
    println!("   Min = {:.1}, Max = {:.1}", min, max);
    println!("   Std Dev = {:.2}", std_dev(&data).unwrap());
    println!();

    // 7. Number Theory
    println!("7. Number Theory:");
    println!("   factorial(5) = {}", factorial(5));
    println!("   is_prime(17) = {}", is_prime(17));
    println!("   is_prime(18) = {}", is_prime(18));
    println!("   gcd(48, 18) = {}", gcd(48, 18));
    println!("   lcm(4, 6) = {}", lcm(4, 6));
    println!();

    // 8. Angle Conversions
    println!("8. Angle Conversions:");
    println!("   90 degrees = {:.4} radians", to_radians(90.0));
    println!("   PI radians = {:.1} degrees", to_degrees(std::f64::consts::PI));
    println!("   450 degrees normalized to [0,360) = {}", normalize_angle_360(450.0));
    println!("   270 degrees normalized to [-180,180) = {}", normalize_angle_180(270.0));
    println!();

    // 9. Distance Calculations
    println!("9. Distance Calculations:");
    let d2d = distance_2d(0.0, 0.0, 3.0, 4.0);
    println!("   Distance 2D (0,0) to (3,4) = {}", d2d);
    let d3d = distance_3d(0.0, 0.0, 0.0, 1.0, 1.0, 1.0);
    println!("   Distance 3D (0,0,0) to (1,1,1) = {:.4}", d3d);
    println!();

    // 10. Formatting
    println!("10. Number Formatting:");
    println!("   format_with_commas(1234567) = {}", format_with_commas(1234567));
    println!("   format_with_commas(-9999999) = {}", format_with_commas(-9999999));
    println!();

    println!("=== Demo Complete ===");
}
