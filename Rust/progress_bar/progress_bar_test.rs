//! Progress Bar Test Suite
//!
//! Comprehensive tests for progress bar functionality.

// Note: These tests verify the public API of the progress bar module.
// Run with: rustc --test progress_bar_test.rs -L ../ && ./progress_bar_test

// Re-export functions for standalone test file
mod progress_bar {
    use std::io::{self, Write};
    use std::time::{Duration, Instant};

    #[derive(Debug, Clone, Copy, PartialEq)]
    pub enum Style {
        Classic,
        Modern,
        Dots,
        Arrows,
        Minimal,
    }

    #[derive(Debug, Clone)]
    pub struct Config {
        pub width: usize,
        pub show_percent: bool,
        pub show_count: bool,
        pub show_eta: bool,
        pub show_elapsed: bool,
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

    pub struct ProgressBar {
        total: u64,
        current: u64,
        style: Style,
        config: Config,
        start_time: Instant,
        last_update: Instant,
        last_progress: u64,
        rate: f64,
        finished: bool,
        message: Option<String>,
    }

    impl ProgressBar {
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

        pub fn indeterminate() -> Self {
            let mut pb = Self::new(0);
            pb.config.show_percent = false;
            pb.config.show_eta = false;
            pb
        }

        pub fn set_total(&mut self, total: u64) {
            self.total = total;
        }

        pub fn total(&self) -> u64 {
            self.total
        }

        pub fn current(&self) -> u64 {
            self.current
        }

        pub fn set_style(&mut self, style: Style) {
            self.style = style;
        }

        pub fn set_config(&mut self, config: Config) {
            self.config = config;
        }

        pub fn set_message(&mut self, msg: impl Into<String>) {
            self.message = Some(msg.into());
        }

        pub fn inc(&mut self, n: u64) {
            self.current = (self.current + n).min(self.total);
            self.update_rate();
        }

        pub fn set(&mut self, n: u64) {
            self.current = n.min(self.total);
            self.update_rate();
        }

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

        fn percentage(&self) -> f64 {
            if self.total == 0 {
                0.0
            } else {
                (self.current as f64 / self.total as f64) * 100.0
            }
        }

        fn eta(&self) -> Duration {
            if self.rate <= 0.0 || self.current >= self.total {
                return Duration::ZERO;
            }
            let remaining = self.total - self.current;
            let seconds = remaining as f64 / self.rate;
            Duration::from_secs_f64(seconds)
        }

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

        fn build_spinner(&self) -> String {
            let spinners = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"];
            let idx = (self.current % spinners.len() as u64) as usize;
            spinners[idx].to_string()
        }

        pub fn render(&self) -> String {
            let mut parts = Vec::new();
            if let Some(ref msg) = self.message {
                parts.push(format!("{} ", msg));
            }
            if self.total == 0 {
                parts.push(self.build_spinner());
                parts.push(" Working...".to_string());
            } else {
                parts.push(self.build_bar());
                if self.config.show_percent {
                    parts.push(format!(" {:5.1}%", self.percentage()));
                }
                if self.config.show_count {
                    parts.push(format!(" [{}/{}]", self.current, self.total));
                }
            }
            if self.config.show_elapsed {
                let elapsed = self.start_time.elapsed();
                parts.push(format!(" elapsed: {}", Self::format_duration(elapsed)));
            }
            if self.config.show_eta && self.total > 0 && self.current < self.total {
                let eta = self.eta();
                if eta > Duration::ZERO {
                    parts.push(format!(" ETA: {}", Self::format_duration(eta)));
                }
            }
            if self.config.show_rate && self.rate > 0.0 {
                parts.push(format!(" ({:.1}/s)", self.rate));
            }
            parts.join("")
        }

        pub fn print(&self) {
            if self.finished {
                return;
            }
            let output = self.render();
            print!("\r{}", " ".repeat(80));
            print!("\r{}", output);
            let _ = io::stdout().flush();
        }

        pub fn finish(&mut self) {
            self.finished = true;
            self.current = self.total;
            println!();
        }

        pub fn finish_with_message(&mut self, msg: &str) {
            self.finished = true;
            self.current = self.total;
            let elapsed = self.start_time.elapsed();
            println!("\r{} ✓ ({})", msg, Self::format_duration(elapsed));
        }

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
                println!();
            }
        }
    }
}

use progress_bar::{Config, ProgressBar, Style};
use std::time::Duration;

// ============ Creation Tests ============

#[test]
fn test_new_progress_bar() {
    let pb = ProgressBar::new(100);
    assert_eq!(pb.total(), 100);
    assert_eq!(pb.current(), 0);
}

#[test]
fn test_indeterminate_progress_bar() {
    let pb = ProgressBar::indeterminate();
    assert_eq!(pb.total(), 0);
}

#[test]
fn test_zero_total() {
    let pb = ProgressBar::new(0);
    assert_eq!(pb.total(), 0);
    assert_eq!(pb.current(), 0);
}

// ============ Progress Tests ============

#[test]
fn test_increment() {
    let mut pb = ProgressBar::new(100);
    pb.inc(1);
    assert_eq!(pb.current(), 1);
}

#[test]
fn test_increment_multiple() {
    let mut pb = ProgressBar::new(100);
    pb.inc(10);
    assert_eq!(pb.current(), 10);
    pb.inc(20);
    assert_eq!(pb.current(), 30);
}

#[test]
fn test_increment_overflow() {
    let mut pb = ProgressBar::new(100);
    pb.inc(150); // Should clamp to total
    assert_eq!(pb.current(), 100);
}

#[test]
fn test_set_progress() {
    let mut pb = ProgressBar::new(100);
    pb.set(50);
    assert_eq!(pb.current(), 50);
}

#[test]
fn test_set_progress_overflow() {
    let mut pb = ProgressBar::new(100);
    pb.set(200); // Should clamp to total
    assert_eq!(pb.current(), 100);
}

#[test]
fn test_set_total() {
    let mut pb = ProgressBar::new(100);
    pb.set_total(200);
    assert_eq!(pb.total(), 200);
}

// ============ Style Tests ============

#[test]
fn test_classic_style() {
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
    let rendered = pb.render();
    assert!(rendered.contains('['));
    assert!(rendered.contains(']'));
    assert!(rendered.contains('='));
}

#[test]
fn test_modern_style() {
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
    let rendered = pb.render();
    assert!(rendered.contains('█'));
    assert!(rendered.contains('░'));
}

#[test]
fn test_dots_style() {
    let mut pb = ProgressBar::new(10);
    pb.set_style(Style::Dots);
    pb.set_config(Config {
        width: 10,
        show_percent: false,
        show_count: false,
        show_eta: false,
        show_elapsed: false,
        show_rate: false,
    });
    pb.inc(5);
    let rendered = pb.render();
    assert!(rendered.contains('●'));
    assert!(rendered.contains('○'));
}

#[test]
fn test_arrows_style() {
    let mut pb = ProgressBar::new(10);
    pb.set_style(Style::Arrows);
    pb.set_config(Config {
        width: 10,
        show_percent: false,
        show_count: false,
        show_eta: false,
        show_elapsed: false,
        show_rate: false,
    });
    pb.inc(5);
    let rendered = pb.render();
    assert!(rendered.contains('▶'));
    assert!(rendered.contains('▷'));
}

#[test]
fn test_minimal_style() {
    let mut pb = ProgressBar::new(100);
    pb.set_style(Style::Minimal);
    pb.set_config(Config {
        width: 10,
        show_percent: false,
        show_count: false,
        show_eta: false,
        show_elapsed: false,
        show_rate: false,
    });
    pb.inc(50);
    let rendered = pb.render();
    assert!(rendered.contains("[50/100]"));
}

// ============ Configuration Tests ============

#[test]
fn test_show_percent() {
    let mut pb = ProgressBar::new(100);
    pb.set_config(Config {
        width: 10,
        show_percent: true,
        show_count: false,
        show_eta: false,
        show_elapsed: false,
        show_rate: false,
    });
    pb.inc(50);
    let rendered = pb.render();
    assert!(rendered.contains("50.0%"));
}

#[test]
fn test_show_count() {
    let mut pb = ProgressBar::new(100);
    pb.set_config(Config {
        width: 10,
        show_percent: false,
        show_count: true,
        show_eta: false,
        show_elapsed: false,
        show_rate: false,
    });
    pb.inc(50);
    let rendered = pb.render();
    assert!(rendered.contains("[50/100]"));
}

#[test]
fn test_hide_elapsed() {
    let mut pb = ProgressBar::new(100);
    pb.set_config(Config {
        width: 10,
        show_percent: false,
        show_count: false,
        show_eta: false,
        show_elapsed: false,
        show_rate: false,
    });
    pb.inc(50);
    let rendered = pb.render();
    assert!(!rendered.contains("elapsed"));
}

#[test]
fn test_custom_width() {
    let mut pb = ProgressBar::new(10);
    pb.set_style(Style::Modern);
    pb.set_config(Config {
        width: 20,
        show_percent: false,
        show_count: false,
        show_eta: false,
        show_elapsed: false,
        show_rate: false,
    });
    pb.inc(5);
    let rendered = pb.render();
    // Should have 10 filled and 10 empty characters
    let filled_count = rendered.chars().filter(|&c| c == '█').count();
    let empty_count = rendered.chars().filter(|&c| c == '░').count();
    assert_eq!(filled_count, 10);
    assert_eq!(empty_count, 10);
}

// ============ Message Tests ============

#[test]
fn test_message() {
    let mut pb = ProgressBar::new(100);
    pb.set_message("Processing");
    let rendered = pb.render();
    assert!(rendered.starts_with("Processing"));
}

#[test]
fn test_message_with_emoji() {
    let mut pb = ProgressBar::new(100);
    pb.set_message("📁 Loading files");
    let rendered = pb.render();
    assert!(rendered.starts_with("📁 Loading files"));
}

// ============ Finish Tests ============

#[test]
fn test_finish() {
    let mut pb = ProgressBar::new(100);
    pb.inc(50);
    pb.finish();
    assert!(pb.finished);
    assert_eq!(pb.current(), 100);
}

#[test]
fn test_finish_with_message() {
    let mut pb = ProgressBar::new(100);
    pb.inc(50);
    pb.finish_with_message("Complete");
    assert!(pb.finished);
    assert_eq!(pb.current(), 100);
}

// ============ Reset Tests ============

#[test]
fn test_reset() {
    let mut pb = ProgressBar::new(100);
    pb.inc(50);
    pb.finish();
    pb.reset();
    assert_eq!(pb.current(), 0);
    assert!(!pb.finished);
}

// ============ Duration Format Tests ============

#[test]
fn test_format_duration_seconds() {
    use progress_bar::ProgressBar;
    // Test via render output
    let pb = ProgressBar::new(1);
    let result = ProgressBar::format_duration(Duration::from_secs(5));
    assert_eq!(result, " 5s");
}

#[test]
fn test_format_duration_minutes() {
    let result = ProgressBar::format_duration(Duration::from_secs(65));
    assert_eq!(result, " 1m  5s");
}

#[test]
fn test_format_duration_hours() {
    let result = ProgressBar::format_duration(Duration::from_secs(3665));
    assert_eq!(result, " 1h  1m  5s");
}

// ============ Percentage Tests ============

#[test]
fn test_percentage_zero() {
    let pb = ProgressBar::new(100);
    // Percentage is not directly accessible, test via render
    let mut pb = ProgressBar::new(100);
    pb.set_config(Config {
        width: 10,
        show_percent: true,
        show_count: false,
        show_eta: false,
        show_elapsed: false,
        show_rate: false,
    });
    let rendered = pb.render();
    assert!(rendered.contains("0.0%"));
}

#[test]
fn test_percentage_half() {
    let mut pb = ProgressBar::new(100);
    pb.set_config(Config {
        width: 10,
        show_percent: true,
        show_count: false,
        show_eta: false,
        show_elapsed: false,
        show_rate: false,
    });
    pb.inc(50);
    let rendered = pb.render();
    assert!(rendered.contains("50.0%"));
}

#[test]
fn test_percentage_complete() {
    let mut pb = ProgressBar::new(100);
    pb.set_config(Config {
        width: 10,
        show_percent: true,
        show_count: false,
        show_eta: false,
        show_elapsed: false,
        show_rate: false,
    });
    pb.inc(100);
    let rendered = pb.render();
    assert!(rendered.contains("100.0%"));
}

// ============ Edge Cases ============

#[test]
fn test_single_item() {
    let mut pb = ProgressBar::new(1);
    pb.inc(1);
    assert_eq!(pb.current(), 1);
    pb.finish();
    assert!(pb.finished);
}

#[test]
fn test_large_total() {
    let mut pb = ProgressBar::new(1_000_000_000);
    pb.inc(500_000_000);
    assert_eq!(pb.current(), 500_000_000);
}

#[test]
fn test_increment_zero() {
    let mut pb = ProgressBar::new(100);
    pb.inc(0);
    assert_eq!(pb.current(), 0);
}

// ============ Integration Tests ============

#[test]
fn test_full_workflow() {
    let mut pb = ProgressBar::new(100);
    pb.set_style(Style::Modern);
    pb.set_message("Processing items");

    // Simulate work
    for i in 1..=100 {
        pb.set(i);
    }

    assert_eq!(pb.current(), 100);
    pb.finish();
    assert!(pb.finished);
}

#[test]
fn test_reuse_after_reset() {
    let mut pb = ProgressBar::new(50);

    // First run
    for i in 1..=50 {
        pb.set(i);
    }
    pb.finish();

    // Reset and run again
    pb.reset();
    pb.set_total(100);

    for i in 1..=100 {
        pb.set(i);
    }
    pb.finish();

    assert_eq!(pb.current(), 100);
}

// ============ Render Tests ============

#[test]
fn test_render_contains_bar() {
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
    let rendered = pb.render();
    // Should have 5 '=' characters and spaces
    assert!(rendered.contains("====="));
}

#[test]
fn test_render_empty_progress() {
    let pb = ProgressBar::new(100);
    let rendered = pb.render();
    // Should not panic and should contain bar brackets
    assert!(rendered.contains('['));
    assert!(rendered.contains(']'));
}

#[test]
fn test_render_full_progress() {
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
    pb.inc(10);
    let rendered = pb.render();
    // Should be all filled
    let filled_count = rendered.chars().filter(|&c| c == '█').count();
    assert_eq!(filled_count, 10);
}
