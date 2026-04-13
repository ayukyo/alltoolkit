//! WCAG contrast checker example

use color_utils::{Color, ContrastLevel};

fn main() {
    println!("=== WCAG Contrast Checker ===\n");

    // Test cases for text/background combinations
    let test_cases = [
        // (foreground, background, description)
        ("#000000", "#FFFFFF", "Black on White"),
        ("#FFFFFF", "#000000", "White on Black"),
        ("#333333", "#FFFFFF", "Dark Gray on White"),
        ("#FF0000", "#FFFFFF", "Red on White"),
        ("#FF0000", "#000000", "Red on Black"),
        ("#777777", "#FFFFFF", "Medium Gray on White"),
        ("#3498db", "#FFFFFF", "Blue on White"),
        ("#3498db", "#2c3e50", "Blue on Dark Blue"),
        ("#e74c3c", "#2c3e50", "Red on Dark Blue"),
        ("#f1c40f", "#2c3e50", "Yellow on Dark Blue"),
    ];

    println!("{:<25} {:<12} {:<15} {:<12}", "Combination", "Ratio", "WCAG Level", "Passes AA?");
    println!("{}", "-".repeat(65));

    for (fg_hex, bg_hex, description) in test_cases {
        let fg = Color::from_hex(fg_hex).unwrap();
        let bg = Color::from_hex(bg_hex).unwrap();
        
        let ratio = fg.contrast_ratio(&bg);
        let level = fg.contrast_level(&bg);
        
        let passes_aa = matches!(level, ContrastLevel::AA | ContrastLevel::AAA);
        
        println!(
            "{:<25} {:>6.2}:1    {:<15} {}",
            description,
            ratio,
            level.to_string(),
            if passes_aa { "✓" } else { "✗" }
        );
    }

    // Interactive contrast requirements
    println!("\n--- WCAG Requirements ---");
    println!("AA:   4.5:1 for normal text, 3:1 for large text");
    println!("AAA:  7:1 for normal text, 4.5:1 for large text");
    println!("Large text: ≥18pt regular or ≥14pt bold");

    // Find a color that passes AA for a given background
    println!("\n--- Finding Accessible Colors ---");
    
    let background = Color::from_hex("#2c3e50").unwrap();
    println!("Background: {}", background.to_hex());
    
    println!("\nFinding text colors that pass AA (≥4.5:1):");
    
    // Test various shades of gray
    let mut found_colors = Vec::new();
    for gray in (0..=255).step_by(17) {
        let text_color = Color::rgb(gray, gray, gray);
        let ratio = text_color.contrast_ratio(&background);
        
        if ratio >= 4.5 {
            found_colors.push((gray, ratio, text_color));
        }
    }
    
    for (gray, ratio, color) in found_colors.iter().take(5) {
        println!("  Gray {:3}: {} ({:.2}:1)", gray, color.to_hex(), ratio);
    }
    
    println!("  ... and {} more valid options", found_colors.len().saturating_sub(5));

    // Demo: lighten/darken to meet contrast
    println!("\n--- Auto-adjust for Contrast ---");
    
    let mut text = Color::rgb(100, 100, 100);
    let bg = Color::rgb(200, 200, 200);
    
    println!("Initial text: {} on background: {}", text.to_hex(), bg.to_hex());
    println!("Initial contrast: {:.2}:1", text.contrast_ratio(&bg));
    
    // Lighten until we reach 4.5:1
    while text.contrast_ratio(&bg) < 4.5 {
        text = text.darken(5);
    }
    
    println!("Adjusted text: {}", text.to_hex());
    println!("Final contrast: {:.2}:1", text.contrast_ratio(&bg));
    println!("WCAG Level: {}", text.contrast_level(&bg));
}