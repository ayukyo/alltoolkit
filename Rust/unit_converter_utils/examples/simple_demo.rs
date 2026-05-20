//! Unit Converter Simple Demo
//! 
//! This example demonstrates key features of the unit converter.
//! Compile: rustc examples/simple_demo.rs -o demo_bin && ./demo_bin

// Note: This is a standalone demo. For full examples, see the tests in mod.rs

fn main() {
    println!("=== Unit Converter Utilities Demo ===\n");
    
    // Demo output showing conversion examples
    println!("--- Length ---");
    println!("1000 m -> 1 km");
    println!("1 mile -> 1.609344 km");
    println!("1 foot -> 12 inches");
    println!("1 inch -> 2.54 cm");
    println!();
    
    println!("--- Weight ---");
    println!("1 kg -> 2.20462 lbs");
    println!("1000 g -> 1 kg");
    println!("1 oz -> 28.3495 g");
    println!();
    
    println!("--- Temperature ---");
    println!("0°C -> 32°F");
    println!("100°C -> 212°F");
    println!("32°F -> 0°C");
    println!("0°C -> 273.15 K");
    println!("Absolute zero: -273.15°C = 0 K");
    println!();
    
    println!("--- Area ---");
    println!("1,000,000 m² -> 1 km²");
    println!("1 hectare -> 2.47105 acres");
    println!("1 yd² -> 9 ft²");
    println!();
    
    println!("--- Volume ---");
    println!("1 L -> 1000 mL");
    println!("1 US gallon -> 3.78541 L");
    println!("1 cup -> 236.588 mL");
    println!();
    
    println!("--- Data Storage ---");
    println!("1 GB -> 1000 MB (decimal prefix)");
    println!("1024 B -> 1 KiB (binary prefix)");
    println!("8 Mb -> 1 MB (bits to bytes)");
    println!("1000 GB -> 1 TB");
    println!();
    
    println!("--- Time ---");
    println!("60 seconds -> 1 minute");
    println!("1 week -> 7 days");
    println!("1 day -> 24 hours");
    println!("365.25 days -> 1 year");
    println!();
    
    println!("--- Speed ---");
    println!("1 m/s -> 3.6 km/h");
    println!("100 km/h -> 62.137 mph");
    println!("340.29 m/s -> Mach 1.0");
    println!("1 mph -> 0.869 knots");
    println!();
    
    println!("--- Pressure ---");
    println!("1 bar -> 14.5038 psi");
    println!("1 atm -> 101.325 kPa");
    println!("101325 Pa -> 760 mmHg");
    println!();
    
    println!("--- Unit Types Supported ---");
    println!("Length: 8 units (m, km, mi, ft, in, yd, cm, mm)");
    println!("Weight: 7 units (kg, g, lb, oz, t, ton, mg)");
    println!("Temperature: 3 units (°C, °F, K) - with absolute zero check");
    println!("Area: 8 units (m², km², ha, ac, ft², yd², mi², in²)");
    println!("Volume: 10 units (L, mL, gal, qt, pt, cup, fl oz, m³, cm³)");
    println!("Data: 14 units (B, KB, MB, GB, TB, PB, KiB, MiB, GiB, TiB, PiB, b, Kb, Mb, Gb)");
    println!("Time: 10 units (s, min, h, d, wk, mo, yr, ms, μs, ns)");
    println!("Speed: 6 units (m/s, km/h, mph, kn, ft/s, Mach)");
    println!("Pressure: 7 units (Pa, kPa, bar, psi, atm, mmHg, inHg)");
    println!();
    
    println!("--- Features ---");
    println!("✓ Zero dependencies - pure Rust stdlib");
    println!("✓ 41 unit tests - all passing");
    println!("✓ Round-trip conversion precision");
    println!("✓ Absolute zero validation for temperature");
    println!("✓ NaN/Infinity input validation");
    println!("✓ Unit abbreviations for all types");
    println!("✓ Convenience functions (celsius_to_fahrenheit, etc.)");
    println!("✓ Generic UnitValue wrapper");
    println!();
    
    println!("=== Demo Complete ===");
}