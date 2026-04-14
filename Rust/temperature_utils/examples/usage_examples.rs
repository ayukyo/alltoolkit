//! Temperature Utils Usage Examples

use temperature_utils::{Temperature, TemperatureUnit, TemperatureUtils, format_temperature};

fn main() {
    println!("============================================================");
    println!("AllToolkit - Temperature Utils Examples (Rust)");
    println!("============================================================");

    // Create utility instance
    let utils = TemperatureUtils::new();

    // 1. Basic conversions
    println!("\n1. Basic Temperature Conversions");
    println!("----------------------------------------");

    let celsius = 25.0;
    println!("Celsius {:.1}°C converts to:", celsius);
    println!("  Fahrenheit: {:.2}°F", utils.celsius_to_fahrenheit(celsius));
    println!("  Kelvin:     {:.2}K", utils.celsius_to_kelvin(celsius));

    let fahrenheit = 98.6;
    println!("\nFahrenheit {:.1}°F converts to:", fahrenheit);
    println!("  Celsius: {:.2}°C", utils.fahrenheit_to_celsius(fahrenheit));
    println!("  Kelvin:  {:.2}K", utils.fahrenheit_to_kelvin(fahrenheit));

    let kelvin = 300.0;
    println!("\nKelvin {:.1}K converts to:", kelvin);
    println!("  Celsius:     {:.2}°C", utils.kelvin_to_celsius(kelvin));
    println!("  Fahrenheit: {:.2}°F", utils.kelvin_to_fahrenheit(kelvin));

    // 2. Convert to all units
    println!("\n2. Convert to All Units");
    println!("----------------------------------------");

    let all_temps = utils.convert_all(20.0, TemperatureUnit::Celsius);
    for (unit, value) in all_temps {
        println!("  {}: {:.2}{}", unit.name(), value, unit.symbol());
    }

    // 3. Temperature parsing
    println!("\n3. Parse Temperature Strings");
    println!("----------------------------------------");

    let temps_to_parse = vec!["25°C", "77°F", "300K", "-40°C"];
    for temp_str in temps_to_parse {
        let temp: Temperature = temp_str.parse().unwrap();
        println!("  '{}' → {} ({})", temp_str, temp, temp.unit.name());
    }

    // 4. Temperature struct
    println!("\n4. Temperature Struct");
    println!("----------------------------------------");

    let t1 = Temperature::from_celsius(25.0);
    let t2 = Temperature::from_fahrenheit(77.0);
    let t3 = Temperature::from_kelvin(300.0);

    println!("  t1: {}", t1);
    println!("  t2: {}", t2);
    println!("  t3: {}", t3);

    // Convert t1 to Fahrenheit
    let t1_f = t1.convert_to(TemperatureUnit::Fahrenheit, &utils);
    println!("  t1 converted to Fahrenheit: {}", t1_f);

    // 5. Temperature operations
    println!("\n5. Temperature Operations");
    println!("----------------------------------------");

    let t_a = Temperature::from_celsius(20.0);
    let t_b = Temperature::from_celsius(10.0);

    println!("  Temperature A: {}", t_a);
    println!("  Temperature B: {}", t_b);

    let sum = utils.add(t_a, t_b);
    let diff = utils.subtract(t_a, t_b);
    println!("  A + B = {}", sum);
    println!("  A - B = {}", diff);

    // Scale temperature
    let scaled = utils.scale(t_a, 2.0);
    println!("  A × 2 = {}", scaled);

    // 6. Average temperature
    println!("\n6. Average Temperature");
    println!("----------------------------------------");

    let temps = vec![
        Temperature::from_celsius(18.0),
        Temperature::from_celsius(22.0),
        Temperature::from_celsius(25.0),
        Temperature::from_fahrenheit(77.0), // ≈ 25°C
    ];

    println!("  Temperatures:");
    for temp in &temps {
        println!("    {}", temp);
    }

    let avg = utils.average(&temps, TemperatureUnit::Celsius);
    println!("  Average: {}", avg);

    // 7. State of matter
    println!("\n7. Water State of Matter");
    println!("----------------------------------------");

    let state_temps = vec![
        Temperature::from_celsius(-10.0),
        Temperature::from_celsius(25.0),
        Temperature::from_celsius(110.0),
    ];

    for temp in state_temps {
        println!("  {} → {}", temp, utils.state_of_matter(temp));
    }

    // 8. Comfort level
    println!("\n8. Comfort Level Assessment");
    println!("----------------------------------------");

    let comfort_temps = vec![10.0, 18.0, 22.0, 25.0, 28.0, 32.0];
    for temp in comfort_temps {
        let t = Temperature::from_celsius(temp);
        println!("  {} → {}", t, utils.comfort_level(t));
    }

    // 9. Temperature comparison
    println!("\n9. Temperature Comparison");
    println!("----------------------------------------");

    let t1 = Temperature::from_celsius(20.0);
    let t2 = Temperature::from_fahrenheit(68.0); // ≈ 20°C
    let t3 = Temperature::from_celsius(30.0);

    println!("  {} vs {}:", t1, t2);
    println!("    Equal? {}", utils.equal(t1, t2));

    println!("  {} vs {}:", t1, t3);
    println!("    Less than? {}", utils.less_than(t1, t3));
    println!("    Greater than? {}", utils.greater_than(t3, t1));

    // 10. Weather calculations
    println!("\n10. Weather Calculations");
    println!("----------------------------------------");

    // Wind chill
    let wind_chill = utils.wind_chill(-5.0, 15.0);
    println!("  Wind Chill: -5°C with 15 km/h wind = {:.1}°C", wind_chill);

    // Heat index
    let heat_index = utils.heat_index(32.0, 70.0);
    println!("  Heat Index: 32°C with 70% humidity = {:.1}°C", heat_index);

    // Dew point
    let dew_point = utils.dew_point(25.0, 60.0);
    println!("  Dew Point: 25°C with 60% humidity = {:.1}°C", dew_point);

    // 11. Temperature description
    println!("\n11. Temperature Description");
    println!("----------------------------------------");

    let desc_temps = vec![
        Temperature::from_celsius(-273.15),
        Temperature::from_celsius(-40.0),
        Temperature::from_celsius(0.0),
        Temperature::from_celsius(22.0),
        Temperature::from_celsius(37.0),
        Temperature::from_celsius(100.0),
        Temperature::from_celsius(500.0),
    ];

    for temp in &desc_temps {
        println!("  {}", utils.describe(*temp));
    }

    // 12. Historical scales
    println!("\n12. Historical Temperature Scales");
    println!("----------------------------------------");

    println!("  Water freezing point (0°C) in historical scales:");
    let freezing = utils.convert_all(0.0, TemperatureUnit::Celsius);
    for (unit, value) in freezing.iter().filter(|(u, _)| {
        *u == TemperatureUnit::Delisle || 
        *u == TemperatureUnit::Newton || 
        *u == TemperatureUnit::Reaumur || 
        *u == TemperatureUnit::Romer
    }) {
        println!("    {}: {:.2}{}", unit.name(), value, unit.symbol());
    }

    println!("\n  Water boiling point (100°C) in historical scales:");
    let boiling = utils.convert_all(100.0, TemperatureUnit::Celsius);
    for (unit, value) in boiling.iter().filter(|(u, _)| {
        *u == TemperatureUnit::Delisle || 
        *u == TemperatureUnit::Newton || 
        *u == TemperatureUnit::Reaumur || 
        *u == TemperatureUnit::Romer
    }) {
        println!("    {}: {:.2}{}", unit.name(), value, unit.symbol());
    }

    // 13. Precision control
    println!("\n13. Precision Control");
    println!("----------------------------------------");

    let utils_p4 = TemperatureUtils::with_precision(4);
    println!("  With precision 4: 37°C → {:.4}°F", utils_p4.celsius_to_fahrenheit(37.0));

    let utils_p0 = TemperatureUtils::with_precision(0);
    println!("  With precision 0: 37°C → {:.0}°F", utils_p0.celsius_to_fahrenheit(37.0));

    // 14. Formatting
    println!("\n14. Formatting");
    println!("----------------------------------------");

    println!("  format_temperature(25.5, Celsius, 1): {}", 
             format_temperature(25.5, TemperatureUnit::Celsius, 1));

    // 15. Freezing and boiling checks
    println!("\n15. Freezing and Boiling Checks");
    println!("----------------------------------------");

    let check_temps = vec![
        Temperature::from_celsius(-5.0),
        Temperature::from_celsius(25.0),
        Temperature::from_celsius(105.0),
    ];

    for temp in check_temps {
        println!("  {}:", temp);
        println!("    Below freezing? {}", utils.is_below_freezing(temp));
        println!("    Above boiling?  {}", utils.is_above_boiling(temp));
    }

    // 16. Absolute zero
    println!("\n16. Absolute Zero");
    println!("----------------------------------------");

    println!("  Absolute zero in all scales:");
    let absolute_zero = utils.convert_all(-273.15, TemperatureUnit::Celsius);
    for (unit, value) in absolute_zero {
        println!("    {}: {:.2}{}", unit.name(), value, unit.symbol());
    }

    println!("\n============================================================");
    println!("Examples complete!");
}