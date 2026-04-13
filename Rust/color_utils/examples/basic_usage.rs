//! Basic usage examples for color_utils

use color_utils::Color;

fn main() {
    println!("=== Color Utils - Basic Usage Examples ===\n");

    // Creating colors from different color spaces
    println!("--- Creating Colors ---");
    
    // RGB
    let red = Color::rgb(255, 0, 0);
    println!("RGB Red: {}", red);
    
    // RGBA
    let transparent_blue = Color::rgba(0, 0, 255, 128);
    println!("RGBA Blue (50% alpha): rgba({}, {}, {}, {})", 
        transparent_blue.red(),
        transparent_blue.green(),
        transparent_blue.blue(),
        transparent_blue.alpha()
    );
    
    // HSL (Hue: 0-360, Saturation: 0-100, Lightness: 0-100)
    let green = Color::hsl(120, 100, 50);
    println!("HSL Green (120°, 100%, 50%): {}", green);
    
    // HSV (Hue: 0-360, Saturation: 0-100, Value: 0-100)
    let blue = Color::hsv(240, 100, 100);
    println!("HSV Blue (240°, 100%, 100%): {}", blue);
    
    // CMYK (Cyan: 0-100, Magenta: 0-100, Yellow: 0-100, Key: 0-100)
    let cyan = Color::cmyk(100, 0, 0, 0);
    println!("CMYK Cyan (100%, 0%, 0%, 0%): {}", cyan);
    
    // HEX
    let orange = Color::from_hex("#FF8040").unwrap();
    println!("HEX Orange (#FF8040): {}", orange);

    println!("\n--- Converting Colors ---");
    
    // Convert to different formats
    let color = Color::rgb(255, 128, 64);
    println!("Original: {}", color);
    
    // To HEX
    println!("HEX: {}", color.to_hex());
    
    // To HSL
    let (h, s, l) = color.to_hsl();
    println!("HSL: h={}, s={}%, l={}%", h, s, l);
    
    // To HSV
    let (h, s, v) = color.to_hsv();
    println!("HSV: h={}, s={}%, v={}%", h, s, v);
    
    // To CMYK
    let (c, m, y, k) = color.to_cmyk();
    println!("CMYK: c={}%, m={}%, y={}%, k={}%", c, m, y, k);

    println!("\n--- Color Properties ---");
    
    let light_color = Color::rgb(230, 230, 230);
    let dark_color = Color::rgb(30, 30, 30);
    
    println!("Is {} light? {}", light_color.to_hex(), light_color.is_light());
    println!("Is {} dark? {}", dark_color.to_hex(), dark_color.is_dark());
    println!("{} luminance: {:.4}", light_color.to_hex(), light_color.luminance());
    println!("{} luminance: {:.4}", dark_color.to_hex(), dark_color.luminance());

    println!("\n--- Contrast Checking (WCAG) ---");
    
    let text = Color::rgb(0, 0, 0);
    let background = Color::rgb(255, 255, 255);
    
    let ratio = text.contrast_ratio(&background);
    let level = text.contrast_level(&background);
    
    println!("Contrast ratio: {:.2}:1", ratio);
    println!("WCAG Level: {}", level);

    println!("\n--- Color Manipulation ---");
    
    let base = Color::rgb(128, 64, 32);
    
    // Lighten
    println!("Original: {}", base.to_hex());
    println!("Lightened by 20%: {}", base.lighten(20).to_hex());
    println!("Darkened by 20%: {}", base.darken(20).to_hex());
    
    // Saturate/Desaturate
    println!("Saturated by 30%: {}", base.saturate(30).to_hex());
    println!("Desaturated by 30%: {}", base.desaturate(30).to_hex());
    
    // Grayscale
    println!("Grayscale: {}", base.grayscale().to_hex());
    
    // Invert
    println!("Inverted: {}", base.invert().to_hex());
    
    // Complementary
    println!("Complementary: {}", base.complementary().to_hex());
    
    // Mix colors
    let other = Color::rgb(32, 128, 255);
    println!("Mixed with {}: {}", other.to_hex(), base.mix(&other, 0.5).to_hex());

    println!("\n--- Named Colors ---");
    
    let named_colors = [
        Color::rgb(255, 0, 0),
        Color::rgb(0, 255, 0),
        Color::rgb(0, 0, 255),
        Color::rgb(255, 165, 0),
        Color::rgb(255, 192, 203),
    ];
    
    for color in named_colors {
        if let Some(name) = color.name() {
            println!("{} = {}", color.to_hex(), name);
        }
    }

    println!("\n--- Parsing HEX Strings ---");
    
    let hex_inputs = ["#F00", "#FF0000", "#ff0000", "FF0000", "#FF000080"];
    
    for hex in hex_inputs {
        match Color::from_hex(hex) {
            Ok(color) => println!("'{}' -> {} (alpha: {})", hex, color.to_hex(), color.alpha()),
            Err(e) => println!("'{}' -> Error: {}", hex, e),
        }
    }
}