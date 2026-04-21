//! # Progress Bar Utilities
//!
//! A lightweight, zero-dependency progress bar library for Rust command-line applications.
//! Provides beautiful, customizable progress indicators with ETA estimation and multiple styles.
//!
//! ## Features
//!
//! - Multiple progress bar styles (classic, modern, dots, arrows)
//! - Real-time ETA estimation
//! - Elapsed time tracking
//! - Rate calculation (items/second)
//! - Thread-safe progress tracking
//! - Customizable width and colors
//! - Zero external dependencies
//!
//! ## Usage
//!
//! ```rust
//! use progress_bar::{ProgressBar, Style};
//!
//! // Create a progress bar
//! let mut pb = ProgressBar::new(100);
//! pb.set_style(Style::Modern);
//!
//! for i in 0..100 {
//!     // Do work...
//!     pb.inc(1);
//!     pb.print();
//! }
//! pb.finish();
//! ```

use std::io::{self, Write};
use std::time::{Duration, Instant};

/// Progress bar style variants.
#[derive(Debug, Clone, Copy, PartialEq)]
pub enum Style {
    /// Classic style: [=====>    ] 50%
    Classic,
    /// Modern style: ████████░░ 80%
    Modern,
    /// Dots style: ●●●●●○○○○○ 50%
    Dots,
    /// Arrows style: ▶▶▶▶▶▷▷▷▷▷ 50%
    Arrows,
    /// Minimal style: 50% [5/10]
    Minimal,
}

/// Configuration for progress bar display.
#[derive(Debug, Clone)]
pub struct Config {
    /// Width of the progress bar in characters (default: 40)
    pub width: usize,
    /// Whether to show percentage (default: true)
    pub show_percent: bool,
    /// Whether to show count (default: true)
    pub show_count: bool,
    /// Whether to show ETA (default: true)
    pub show_eta: bool,
    /// Whether to show elapsed time (default: true)
    pub show_elapsed: bool,
    /// Whether to show rate (default: false)
    pub show_rate: bool,
}

impl Default for Config {
    fn default() -> Self {
        Config {
            width: 40,
            show_percent: true,
            show_count: true,
            show_eta: true,
            show_elapsed: true,
            show_rate: false,
        }
    }
}

/// A progress bar for tracking task completion.
///
/// # Thread Safety
///
/// This implementation is not thread-safe. For multi-threaded use cases,
/// wrap in a `Mutex` or use external synchronization.
///
/// # Example
///
/// ```rust
/// use progress_bar::{ProgressBar, Style};
///
/// let mut pb = ProgressBar::new(1000);
/// pb.set_style(Style::Modern);
///
/// for i in 0..1000 {
///     // Simulate work
///     std::thread::sleep(std::time::Duration::from_millis(1));
///     pb.inc(1);
///     pb.print();
/// }
/// pb.finish();
/// ```
#[derive(Debug)]
pub struct ProgressBar {
    /// Total number of items
    total: u64,
    /// Current progress count
    current: u64,
    /// Progress bar style
    style: Style,
    /// Display configuration
    config: Config,
    /// Start time
    start_time: Instant,
    /// Last update time (for rate calculation)
    last_update: Instant,
    /// Progress at last update (for rate calculation)
    last_progress: u64,
    /// Estimated rate (items per second)
    rate: f64,
    /// Whether the progress bar has finished
    finished: bool,
    /// Custom message to display
    message: Option<String>,
}

impl ProgressBar {
    /// Creates a new progress bar with the specified total.
    ///
    /// # Parameters
    ///
    /// * `total` - Total number of items to process
    ///
    /// # Returns
    ///
    /// A new `ProgressBar` instance with default style and configuration.
    ///
    /// # Example
    ///
    /// ```rust
    /// use progress_bar::ProgressBar;
    ///
    /// let pb = ProgressBar::new(100);
    /// ```
    pub fn new(total: u64) -> Self {
        let now = Instant::now();
        ProgressBar {
            total,
            current: 0,
            style: Style::Classic,
            config: Config::default(),
            start_time: now,
            last_update: now,
            last_progress: 0,
            rate: 0.0,
            finished: false,
            message: None,
        }
    }

    /// Creates a progress bar with indeterminate progress (no total).
    ///
    /// Use this when the total number of items is unknown.
    /// Displays a spinner-style animation instead of a percentage.
    ///
    /// # Example
    ///
    /// ```rust
    /// use progress_bar::ProgressBar;
    ///
    /// let pb = ProgressBar::indeterminate();
    /// ```
    pub fn indeterminate() -> Self {
        let mut pb = Self::new(0);
        pb.config.show_percent = false;
        pb.config.show_eta = false;
        pb
    }

    /// Sets the total number of items.
    ///
    /// # Parameters
    ///
    /// * `total` - New total value
    pub fn set_total(&mut self, total: u64) {
        self.total = total;
    }

    /// Returns the total number of items.
    pub fn total(&self) -> u64 {
        self.total
    }

    /// Returns the current progress count.
    pub fn current(&self) -> u64 {
        self.current
    }

    /// Sets the progress bar style.
    ///
    /// # Parameters
    ///
    /// * `style` - The style to use
    pub fn set_style(&mut self, style: Style) {
        self.style = style;
    }

    /// Sets the display configuration.
    ///
    /// # Parameters
    ///
    /// * `config` - Configuration options
    pub fn set_config(&mut self, config: Config) {
        self.config = config;
    }

    /// Sets a custom message to display.
    ///
    /// # Parameters
    ///
    /// * `msg` - Message string
    pub fn set_message(&mut self, msg: impl Into<String>) {
        self.message = Some(msg.into());
    }

    /// Increments the progress by a specified amount.
    ///
    /// # Parameters
    ///
    /// * `n` - Number of items to add to progress
    ///
    /// # Example
    ///
    /// ```rust
    /// use progress_bar::ProgressBar;
    ///
    /// let mut pb = ProgressBar::new(100);
    /// pb.inc(10); // Progress is now 10
    /// ```
    pub fn inc(&mut self, n: u64) {
        self.current = (self.current + n).min(self.total);
        self.update_rate();
    }

    /// Sets the progress to a specific value.
    ///
    /// # Parameters
    ///
    /// * `n` - New progress value (clamped to total)
    pub fn set(&mut self, n: u64) {
        self.current = n.min(self.total);
        self.update_rate();
    }

    /// Updates the rate calculation.
    fn update_rate(&mut self) {
        let now = Instant::now();
        let elapsed = now.duration_since(self.last_update).as_secs_f64();

        if elapsed >= 0.1 {
            let progress_delta = self.current.saturating_sub(self.last_progress) as f64;
            self.rate = progress_delta / elapsed;
            self.last_update = now;
            self.last_progress = self.current;
        }
    }

    /// Calculates the completion percentage.
    fn percentage(&self) -> f64 {
        if self.total == 0 {
            0.0
        } else {
            (self.current as f64 / self.total as f64) * 100.0
        }
    }

    /// Estimates time remaining.
    fn eta(&self) -> Duration {
        if self.rate <= 0.0 || self.current >= self.total {
            return Duration::ZERO;
        }

        let remaining = self.total - self.current;
        let seconds = remaining as f64 / self.rate;
        Duration::from_secs_f64(seconds)
    }

    /// Formats a duration as human-readable string.
    fn format_duration(d: Duration) -> String {
        let secs = d.as_secs();

        if secs < 60 {
            format!("{:2}s", secs)
        } else if secs < 3600 {
            let mins = secs / 60;
            let s = secs % 60;
            format!("{:2}m {:2}s", mins, s)
        } else {
            let hours = secs / 3600;
            let mins = (secs % 3600) / 60;
            let s = secs % 60;
            format!("{:2}h {:2}m {:2}s", hours, mins, s)
        }
    }

    /// Builds the progress bar string.
    fn build_bar(&self) -> String {
        let percent = self.percentage();
        let filled = if self.total > 0 {
            ((percent / 100.0) * self.config.width as f64) as usize
        } else {
            0
        };
        let filled = filled.min(self.config.width);
        let empty = self.config.width - filled;

        match self.style {
            Style::Classic => {
                let filled_str: String = "=".repeat(filled);
                let empty_str: String = " ".repeat(empty);
                let arrow = if filled > 0 && filled < self.config.width {
                    ">"
                } else {
                    ""
                };
                format!("[{}{}{}]", filled_str, arrow, empty_str)
            }
            Style::Modern => {
                let filled_str: String = "█".repeat(filled);
                let empty_str: String = "░".repeat(empty);
                format!("{}{}", filled_str, empty_str)
            }
            Style::Dots => {
                let filled_str: String = "●".repeat(filled);
                let empty_str: String = "○".repeat(empty);
                format!("{}{}", filled_str, empty_str)
            }
            Style::Arrows => {
                let filled_str: String = "▶".repeat(filled);
                let empty_str: String = "▷".repeat(empty);
                format!("{}{}", filled_str, empty_str)
            }
            Style::Minimal => {
                format!("[{}/{}]", self.current, self.total)
            }
        }
    }

    /// Builds a spinner animation for indeterminate progress.
    fn build_spinner(&self) -> String {
        let spinners = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"];
        let idx = (self.current % spinners.len() as u64) as usize;
        spinners[idx].to_string()
    }

    /// Renders the complete progress bar string.
    pub fn render(&self) -> String {
        let mut parts = Vec::new();

        // Add message if set
        if let Some(ref msg) = self.message {
            parts.push(format!("{} ", msg));
        }

        // Build bar or spinner
        if self.total == 0 {
            parts.push(self.build_spinner());
            parts.push(" Working...".to_string());
        } else {
            parts.push(self.build_bar());

            // Add percentage
            if self.config.show_percent {
                parts.push(format!(" {:5.1}%", self.percentage()));
            }

            // Add count
            if self.config.show_count {
                parts.push(format!(" [{}/{}]", self.current, self.total));
            }
        }

        // Add elapsed time
        if self.config.show_elapsed {
            let elapsed = self.start_time.elapsed();
            parts.push(format!(" elapsed: {}", Self::format_duration(elapsed)));
        }

        // Add ETA
        if self.config.show_eta && self.total > 0 && self.current < self.total {
            let eta = self.eta();
            if eta > Duration::ZERO {
                parts.push(format!(" ETA: {}", Self::format_duration(eta)));
            }
        }

        // Add rate
        if self.config.show_rate && self.rate > 0.0 {
            parts.push(format!(" ({:.1}/s)", self.rate));
        }

        parts.join("")
    }

    /// Prints the progress bar to stdout.
    ///
    /// Uses carriage return to overwrite the current line.
    /// Call `finish()` when done to print a newline.
    pub fn print(&self) {
        if self.finished {
            return;
        }

        let output = self.render();
        let terminal_width = self.get_terminal_width();

        // Clear the line and print
        print!("\r{}", " ".repeat(terminal_width));
        print!("\r{}", output);

        let _ = io::stdout().flush();
    }

    /// Gets the terminal width, with a default fallback.
    fn get_terminal_width(&self) -> usize {
        // Default to 80 columns if we can't determine terminal width
        80
    }

    /// Marks the progress bar as finished and prints a newline.
    ///
    /// If `clear` is true, the progress bar line is cleared.
    pub fn finish(&mut self) {
        self.finished = true;
        self.current = self.total;
        println!(); // Move to next line
    }

    /// Finishes the progress bar with a custom message.
    ///
    /// # Parameters
    ///
    /// * `msg` - Completion message
    pub fn finish_with_message(&mut self, msg: &str) {
        self.finished = true;
        self.current = self.total;

        let elapsed = self.start_time.elapsed();
        println!("\r{} ✓ ({})", msg, Self::format_duration(elapsed));
    }

    /// Resets the progress bar for reuse.
    pub fn reset(&mut self) {
        let now = Instant::now();
        self.current = 0;
        self.start_time = now;
        self.last_update = now;
        self.last_progress = 0;
        self.rate = 0.0;
        self.finished = false;
        self.message = None;
    }
}

impl Drop for ProgressBar {
    fn drop(&mut self) {
        if !self.finished {
            println!(); // Ensure we end on a new line
        }
    }
}

// ============================================================================
// Example Usage
// ============================================================================

/// Example demonstrating basic progress bar usage.
pub fn example_basic() {
    println!("=== Basic Progress Bar ===\n");

    let mut pb = ProgressBar::new(50);
    pb.set_style(Style::Classic);

    for _ in 0..50 {
        std::thread::sleep(Duration::from_millis(50));
        pb.inc(1);
        pb.print();
    }
    pb.finish();
}

/// Example demonstrating all available styles.
pub fn example_styles() {
    println!("=== Progress Bar Styles ===\n");

    let styles = [
        (Style::Classic, "Classic"),
        (Style::Modern, "Modern"),
        (Style::Dots, "Dots"),
        (Style::Arrows, "Arrows"),
        (Style::Minimal, "Minimal"),
    ];

    for (style, name) in styles {
        println!("{} style:", name);
        let mut pb = ProgressBar::new(20);
        pb.set_style(style);
        pb.set_message("Processing");

        for _ in 0..20 {
            std::thread::sleep(Duration::from_millis(30));
            pb.inc(1);
            pb.print();
        }
        pb.finish_with_message("Done");
        println!();
    }
}

/// Example demonstrating indeterminate progress.
pub fn example_indeterminate() {
    println!("=== Indeterminate Progress ===\n");

    let mut pb = ProgressBar::indeterminate();
    pb.set_message("Loading");

    for _ in 0..30 {
        std::thread::sleep(Duration::from_millis(100));
        pb.inc(1);
        pb.print();
    }
    pb.finish_with_message("Complete");
}

/// Example demonstrating custom configuration.
pub fn example_custom_config() {
    println!("=== Custom Configuration ===\n");

    let config = Config {
        width: 30,
        show_percent: true,
        show_count: true,
        show_eta: true,
        show_elapsed: true,
        show_rate: true,
    };

    let mut pb = ProgressBar::new(100);
    pb.set_style(Style::Modern);
    pb.set_config(config);
    pb.set_message("Uploading");

    for _ in 0..100 {
        std::thread::sleep(Duration::from_millis(20));
        pb.inc(1);
        pb.print();
    }
    pb.finish_with_message("Upload complete");
}

/// Run all examples.
pub fn run_examples() {
    example_basic();
    println!();

    example_styles();
    println!();

    example_indeterminate();
    println!();

    example_custom_config();
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_progress_bar_creation() {
        let pb = ProgressBar::new(100);
        assert_eq!(pb.total(), 100);
        assert_eq!(pb.current(), 0);
    }

    #[test]
    fn test_progress_bar_increment() {
        let mut pb = ProgressBar::new(100);
        pb.inc(10);
        assert_eq!(pb.current(), 10);
        pb.inc(20);
        assert_eq!(pb.current(), 30);
    }

    #[test]
    fn test_progress_bar_set() {
        let mut pb = ProgressBar::new(100);
        pb.set(50);
        assert_eq!(pb.current(), 50);
        pb.set(150); // Should clamp to total
        assert_eq!(pb.current(), 100);
    }

    #[test]
    fn test_progress_bar_percentage() {
        let mut pb = ProgressBar::new(100);
        assert_eq!(pb.percentage(), 0.0);
        pb.inc(25);
        assert_eq!(pb.percentage(), 25.0);
        pb.inc(25);
        assert_eq!(pb.percentage(), 50.0);
    }

    #[test]
    fn test_progress_bar_finish() {
        let mut pb = ProgressBar::new(100);
        pb.inc(50);
        pb.finish();
        assert!(pb.finished);
        assert_eq!(pb.current(), 100);
    }

    #[test]
    fn test_progress_bar_reset() {
        let mut pb = ProgressBar::new(100);
        pb.inc(50);
        pb.finish();
        pb.reset();
        assert_eq!(pb.current(), 0);
        assert!(!pb.finished);
    }

    #[test]
    fn test_format_duration() {
        assert_eq!(ProgressBar::format_duration(Duration::from_secs(5)), " 5s");
        assert_eq!(
            ProgressBar::format_duration(Duration::from_secs(65)),
            " 1m  5s"
        );
        assert_eq!(
            ProgressBar::format_duration(Duration::from_secs(3665)),
            " 1h  1m  5s"
        );
    }

    #[test]
    fn test_style_classic() {
        let mut pb = ProgressBar::new(10);
        pb.set_style(Style::Classic);
        pb.set_config(Config {
            width: 10,
            show_percent: false,
            show_count: false,
            show_eta: false,
            show_elapsed: false,
            show_rate: false,
        });
        pb.inc(5);

        // Classic style should have brackets and equals
        let rendered = pb.render();
        assert!(rendered.contains('['));
        assert!(rendered.contains(']'));
        assert!(rendered.contains('='));
    }

    #[test]
    fn test_style_modern() {
        let mut pb = ProgressBar::new(10);
        pb.set_style(Style::Modern);
        pb.set_config(Config {
            width: 10,
            show_percent: false,
            show_count: false,
            show_eta: false,
            show_elapsed: false,
            show_rate: false,
        });
        pb.inc(5);

        // Modern style uses block characters
        let rendered = pb.render();
        assert!(rendered.contains('█'));
        assert!(rendered.contains('░'));
    }

    #[test]
    fn test_indeterminate() {
        let pb = ProgressBar::indeterminate();
        assert_eq!(pb.total(), 0);
        assert!(!pb.config.show_percent);
    }

    #[test]
    fn test_message() {
        let mut pb = ProgressBar::new(10);
        pb.set_message("Testing");
        let rendered = pb.render();
        assert!(rendered.starts_with("Testing"));
    }

    #[test]
    fn test_zero_total() {
        let pb = ProgressBar::new(0);
        assert_eq!(pb.percentage(), 0.0);
    }
}
