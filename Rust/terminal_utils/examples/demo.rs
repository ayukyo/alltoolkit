//! Terminal Utils Example
//! 
//! Demonstrates the various features of the terminal_utils library.

use terminal_utils::{color, style, cursor, screen, progress, align, table};

fn main() {
    println!("\n{}", style::bold("=== Terminal Utils Demo ===\n"));

    // Color examples
    demo_colors();
    
    // Style examples
    demo_styles();
    
    // Progress bar examples
    demo_progress();
    
    // Table examples
    demo_tables();
    
    // Alignment examples
    demo_alignment();
    
    println!("\n{}", color::green("Demo complete!"));
}

fn demo_colors() {
    println!("{}", style::bold("Colors:"));
    
    // Basic colors
    println!("  {} {} {} {} {} {} {} {}",
        color::black("black"),
        color::red("red"),
        color::green("green"),
        color::yellow("yellow"),
        color::blue("blue"),
        color::magenta("magenta"),
        color::cyan("cyan"),
        color::white("white"),
    );
    
    // Bright colors
    println!("  {} {} {} {} {} {} {} {}",
        color::bright_black("bright_black"),
        color::bright_red("bright_red"),
        color::bright_green("bright_green"),
        color::bright_yellow("bright_yellow"),
        color::bright_blue("bright_blue"),
        color::bright_magenta("bright_magenta"),
        color::bright_cyan("bright_cyan"),
        color::bright_white("bright_white"),
    );
    
    // RGB colors
    println!("  {}", color::colorize_rgb("Custom RGB Color", 255, 128, 0));
    
    println!();
}

fn demo_styles() {
    println!("{}", style::bold("Text Styles:"));
    
    println!("  {} {} {} {} {}",
        style::bold("bold"),
        style::italic("italic"),
        style::underline("underline"),
        style::strikethrough("strikethrough"),
        style::dim("dim"),
    );
    
    // Combined styles
    println!("  {}", style::combine("Bold + Italic + Red", &[
        style::BOLD,
        style::ITALIC,
        &color::fg(color::RED),
    ]));
    
    println!();
}

fn demo_progress() {
    println!("{}", style::bold("Progress Bars:"));
    
    // Standard progress bar
    println!("  Standard:");
    for i in [0, 25, 50, 75, 100] {
        println!("    {}", progress::bar(i, 100, 20));
    }
    
    // ASCII style
    println!("  ASCII:");
    for i in [0, 50, 100] {
        println!("    {}", progress::bar_with_chars(i, 100, 20, progress::ProgressChars::ascii()));
    }
    
    // Download style
    println!("  Download:");
    println!("    {}", progress::download_bar(52428800, 104857600, 20, 2097152));
    
    // Spinner
    println!("  Spinners:");
    for i in 0..4 {
        println!("    Frame {}: {}", i, progress::spinner(i));
    }
    
    // Moon spinner
    for i in 0..4 {
        println!("    Moon {}: {}", i, progress::spinner_moon(i));
    }
    
    println!();
}

fn demo_tables() {
    println!("{}", style::bold("Tables:"));
    
    // Simple table
    println!("  Standard table:");
    let output = table::simple(
        &["Name", "Age", "City"],
        &[
            &["Alice", "30", "New York"],
            &["Bob", "25", "Los Angeles"],
            &["Charlie", "35", "Chicago"],
        ],
    );
    for line in output.lines() {
        println!("    {}", line);
    }
    
    // ASCII table
    println!("\n  ASCII table:");
    let output = table::ascii_table(
        &["ID", "Status"],
        &[
            &["001", "Active"],
            &["002", "Inactive"],
        ],
    );
    for line in output.lines() {
        println!("    {}", line);
    }
    
    // Markdown table
    println!("\n  Markdown table:");
    let output = table::markdown_table(
        &["Language", "Year"],
        &[
            &["Rust", "2010"],
            &["Go", "2009"],
            &["Python", "1991"],
        ],
    );
    for line in output.lines() {
        println!("    {}", line);
    }
    
    // Styled table
    println!("\n  Styled table:");
    let styled_table = table::Table::new()
        .border(table::BorderStyle::rounded())
        .column("Feature")
        .column_with(table::Column::new("Status").align_right())
        .column_with(table::Column::new("Notes").align_center())
        .row(&["Colors", "✓", "8 basic + bright"])
        .row(&["Styles", "✓", "Bold, italic, etc."])
        .row(&["Tables", "✓", "Multiple styles"])
        .row(&["Progress", "✓", "Various types"])
        .render();
    for line in styled_table.lines() {
        println!("    {}", line);
    }
    
    println!();
}

fn demo_alignment() {
    println!("{}", style::bold("Text Alignment:"));
    
    let width = 30;
    let text = "Hello";
    
    println!("  Width: {} characters", width);
    println!("  Left:   |{}|", align::left(text, width));
    println!("  Right:  |{}|", align::right(text, width));
    println!("  Center: |{}|", align::center(text, width));
    
    // Truncate
    let long_text = "This is a very long text that needs truncation";
    println!("\n  Truncate test:");
    println!("    Original: {}", long_text);
    println!("    Truncated (20): {}", align::truncate(long_text, 20));
    
    // Distribute
    println!("\n  Distribute across width:");
    let distributed = align::distribute(&["Left", "Middle", "Right"], 40);
    println!("    |{}|", distributed);
    
    println!();
}

#[allow(dead_code)]
fn demo_cursor_screen() {
    // These are shown commented to avoid messing up the demo output
    
    // Cursor control
    // println!("Move cursor to row 5, col 10: {}", cursor::to_pos(5, 10));
    // println!("Move up 2 lines: {}", cursor::up(2));
    // println!("Save position: {}", cursor::save());
    // println!("Restore position: {}", cursor::restore());
    // println!("Hide cursor: {}", cursor::hide());
    // println!("Show cursor: {}", cursor::show());
    
    // Screen control
    // println!("Clear screen: {}", screen::clear_screen());
    // println!("Clear line: {}", screen::clear_line());
    // println!("Enter alt screen: {}", screen::enter_alt_screen());
    // println!("Exit alt screen: {}", screen::exit_alt_screen());
}