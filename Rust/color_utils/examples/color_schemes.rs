//! Color scheme generation examples

use color_utils::Color;

fn main() {
    println!("=== Color Scheme Generator ===\n");

    let base_color = Color::rgb(255, 128, 64);
    println!("Base Color: {}\n", base_color.to_hex());

    // Triadic Color Scheme
    println!("--- Triadic Scheme (120° apart) ---");
    let triadic = base_color.triadic();
    for (i, color) in triadic.iter().enumerate() {
        let (h, s, l) = color.to_hsl();
        println!("  Color {}: {} (HSL: {}°, {}%, {}%)", 
            i + 1, color.to_hex(), h, s, l);
    }

    // Analogous Color Scheme
    println!("\n--- Analogous Scheme (30° apart) ---");
    let analogous = base_color.analogous();
    for (i, color) in analogous.iter().enumerate() {
        let (h, s, l) = color.to_hsl();
        println!("  Color {}: {} (HSL: {}°, {}%, {}%)", 
            i + 1, color.to_hex(), h, s, l);
    }

    // Split-Complementary Color Scheme
    println!("\n--- Split-Complementary Scheme ---");
    let split = base_color.split_complementary();
    for (i, color) in split.iter().enumerate() {
        let (h, s, l) = color.to_hsl();
        println!("  Color {}: {} (HSL: {}°, {}%, {}%)", 
            i + 1, color.to_hex(), h, s, l);
    }

    // Complementary Color
    println!("\n--- Complementary Color ---");
    let complementary = base_color.complementary();
    println!("  Base: {} -> Complementary: {}", 
        base_color.to_hex(), complementary.to_hex());

    // Generate a gradient
    println!("\n--- 10-Step Gradient (Base to Complementary) ---");
    for i in 0..=10 {
        let weight = i as f64 / 10.0;
        let color = base_color.mix(&complementary, weight);
        println!("  Step {:2}: {}", i, color.to_hex());
    }

    // Generate tints and shades
    println!("\n--- Tints (Lighter) ---");
    for i in 1..=5 {
        let lightened = base_color.lighten(i * 15);
        println!("  +{}%: {}", i * 15, lightened.to_hex());
    }

    println!("\n--- Shades (Darker) ---");
    for i in 1..=5 {
        let darkened = base_color.darken(i * 15);
        println!("  -{}%: {}", i * 15, darkened.to_hex());
    }

    // Generate saturation variations
    println!("\n--- Saturation Variations ---");
    let saturated = base_color.saturate(50);
    let desaturated = base_color.desaturate(50);
    let grayscale = base_color.grayscale();
    
    println!("  Original:     {}", base_color.to_hex());
    println!("  +50% Sat:     {}", saturated.to_hex());
    println!("  -50% Sat:     {}", desaturated.to_hex());
    println!("  Grayscale:    {}", grayscale.to_hex());
}