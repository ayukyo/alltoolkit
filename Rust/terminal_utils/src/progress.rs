//! Progress bar utilities
//! 
//! Provides progress bar rendering for terminal output.

/// Progress bar characters
pub struct ProgressChars {
    pub filled: char,
    pub empty: char,
    pub start: char,
    pub end: char,
}

impl Default for ProgressChars {
    fn default() -> Self {
        Self {
            filled: '█',
            empty: '░',
            start: '[',
            end: ']',
        }
    }
}

impl ProgressChars {
    /// Classic ASCII style
    pub fn ascii() -> Self {
        Self {
            filled: '=',
            empty: '-',
            start: '[',
            end: ']',
        }
    }

    /// Block style with rounded corners
    pub fn blocks() -> Self {
        Self {
            filled: '■',
            empty: '□',
            start: '[',
            end: ']',
        }
    }

    /// Minimal style (no brackets)
    pub fn minimal() -> Self {
        Self {
            filled: '●',
            empty: '○',
            start: ' ',
            end: ' ',
        }
    }

    /// Dots style
    pub fn dots() -> Self {
        Self {
            filled: '⬤',
            empty: '⬢',
            start: ' ',
            end: ' ',
        }
    }

    /// Arrow style
    pub fn arrow() -> Self {
        Self {
            filled: '=',
            empty: ' ',
            start: '[',
            end: '>',
        }
    }
}

/// Create a progress bar string
/// 
/// # Arguments
/// * `current` - Current progress value
/// * `total` - Maximum value
/// * `width` - Width of the progress bar in characters
/// 
/// # Example
/// ```rust
/// use terminal_utils::progress;
/// let bar = progress::bar(50, 100, 20);
/// assert!(bar.contains("50%"));
/// ```
pub fn bar(current: u64, total: u64, width: usize) -> String {
    bar_with_chars(current, total, width, ProgressChars::default())
}

/// Create a progress bar with custom characters
/// 
/// # Arguments
/// * `current` - Current progress value
/// * `total` - Maximum value
/// * `width` - Width of the progress bar in characters
/// * `chars` - Custom progress characters
pub fn bar_with_chars(current: u64, total: u64, width: usize, chars: ProgressChars) -> String {
    let percentage = if total == 0 { 0.0 } else { (current as f64 / total as f64) * 100.0 };
    let filled_len = if total == 0 { 0 } else { 
        ((current as f64 / total as f64) * width as f64).round() as usize 
    };
    let filled_len = filled_len.min(width);
    let empty_len = width - filled_len;
    
    let filled: String = chars.filled.to_string().repeat(filled_len);
    let empty: String = chars.empty.to_string().repeat(empty_len);
    
    format!(
        "{}{}{}{} {:.0}%",
        chars.start, filled, empty, chars.end, percentage
    )
}

/// Create a progress bar with custom label
/// 
/// # Arguments
/// * `current` - Current progress value
/// * `total` - Maximum value
/// * `width` - Width of the progress bar in characters
/// * `label` - Label to show before the progress bar
pub fn bar_with_label(current: u64, total: u64, width: usize, label: &str) -> String {
    let bar_str = bar(current, total, width);
    format!("{} {}", label, bar_str)
}

/// Create a spinner animation frame
/// 
/// # Arguments
/// * `frame` - Current frame index
/// 
/// # Example
/// ```rust
/// use terminal_utils::progress;
/// let spinner = progress::spinner(0); // |
/// let spinner = progress::spinner(1); // /
/// ```
pub fn spinner(frame: usize) -> String {
    let frames = ['|', '/', '-', '\\'];
    frames[frame % frames.len()].to_string()
}

/// Spinner with dots style
pub fn spinner_dots(frame: usize) -> String {
    let frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"];
    frames[frame % frames.len()].to_string()
}

/// Spinner with moon style
pub fn spinner_moon(frame: usize) -> String {
    let frames = ["🌑", "🌒", "🌓", "🌔", "🌕", "🌖", "🌗", "🌘"];
    frames[frame % frames.len()].to_string()
}

/// Create a download-style progress bar
/// 
/// Shows downloaded size, total size, and speed
/// 
/// # Arguments
/// * `downloaded` - Bytes downloaded
/// * `total` - Total bytes
/// * `width` - Width of progress bar
/// * `speed_bps` - Speed in bytes per second
pub fn download_bar(downloaded: u64, total: u64, width: usize, speed_bps: u64) -> String {
    let percentage = if total == 0 { 0.0 } else { (downloaded as f64 / total as f64) * 100.0 };
    let filled_len = if total == 0 { 0 } else { 
        ((downloaded as f64 / total as f64) * width as f64).round() as usize 
    };
    let filled_len = filled_len.min(width);
    let empty_len = width - filled_len;
    
    let filled: String = "█".repeat(filled_len);
    let empty: String = "░".repeat(empty_len);
    
    let downloaded_str = format_bytes(downloaded);
    let total_str = format_bytes(total);
    let speed_str = format_bytes(speed_bps) + "/s";
    
    format!(
        "[{}{}] {:>8}/{:<8} {:>10} {:5.1}%",
        filled, empty, downloaded_str, total_str, speed_str, percentage
    )
}

/// Format bytes to human-readable string
fn format_bytes(bytes: u64) -> String {
    const UNITS: [&str; 6] = ["B", "KB", "MB", "GB", "TB", "PB"];
    let mut size = bytes as f64;
    let mut unit_idx = 0;
    
    while size >= 1024.0 && unit_idx < UNITS.len() - 1 {
        size /= 1024.0;
        unit_idx += 1;
    }
    
    if unit_idx == 0 {
        format!("{} {}", bytes, UNITS[unit_idx])
    } else {
        format!("{:.1} {}", size, UNITS[unit_idx])
    }
}

/// Progress bar with elapsed time
/// 
/// # Arguments
/// * `current` - Current progress value
/// * `total` - Maximum value
/// * `width` - Width of progress bar
/// * `elapsed_secs` - Elapsed time in seconds
pub fn bar_with_time(current: u64, total: u64, width: usize, elapsed_secs: u64) -> String {
    let percentage = if total == 0 { 0.0 } else { (current as f64 / total as f64) * 100.0 };
    let filled_len = if total == 0 { 0 } else { 
        ((current as f64 / total as f64) * width as f64).round() as usize 
    };
    let filled_len = filled_len.min(width);
    let empty_len = width - filled_len;
    
    let filled: String = "█".repeat(filled_len);
    let empty: String = "░".repeat(empty_len);
    
    let eta = if current > 0 && total > current {
        let rate = current as f64 / elapsed_secs as f64;
        let remaining = (total - current) as f64;
        let eta_secs = (remaining / rate) as u64;
        format_time(eta_secs)
    } else {
        "--:--".to_string()
    };
    
    format!(
        "[{}{}] {:5.1}% Elapsed: {} ETA: {}",
        filled, empty, percentage, format_time(elapsed_secs), eta
    )
}

/// Format seconds to MM:SS or HH:MM:SS
fn format_time(secs: u64) -> String {
    let hours = secs / 3600;
    let mins = (secs % 3600) / 60;
    let secs = secs % 60;
    
    if hours > 0 {
        format!("{:02}:{:02}:{:02}", hours, mins, secs)
    } else {
        format!("{:02}:{:02}", mins, secs)
    }
}

/// Create a multi-progress container for parallel progress bars
pub struct MultiProgress {
    bars: Vec<(String, u64, u64)>,
    width: usize,
}

impl MultiProgress {
    pub fn new(width: usize) -> Self {
        Self {
            bars: Vec::new(),
            width,
        }
    }

    /// Add a progress bar
    pub fn add(&mut self, label: &str, current: u64, total: u64) {
        self.bars.push((label.to_string(), current, total));
    }

    /// Update a progress bar by index
    pub fn update(&mut self, index: usize, current: u64) {
        if index < self.bars.len() {
            self.bars[index].1 = current;
        }
    }

    /// Render all progress bars
    pub fn render(&self) -> String {
        self.bars
            .iter()
            .map(|(label, current, total)| bar_with_label(*current, *total, self.width, label))
            .collect::<Vec<_>>()
            .join("\n")
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_bar_zero() {
        let bar = bar(0, 100, 10);
        assert!(bar.contains("0%"));
    }

    #[test]
    fn test_bar_half() {
        let bar = bar(50, 100, 10);
        assert!(bar.contains("50%"));
    }

    #[test]
    fn test_bar_full() {
        let bar = bar(100, 100, 10);
        assert!(bar.contains("100%"));
    }

    #[test]
    fn test_bar_with_chars() {
        let chars = ProgressChars::ascii();
        let bar = bar_with_chars(50, 100, 10, chars);
        assert!(bar.contains("["));
        assert!(bar.contains("]"));
    }

    #[test]
    fn test_spinner() {
        assert_eq!(spinner(0), "|");
        assert_eq!(spinner(1), "/");
        assert_eq!(spinner(2), "-");
        assert_eq!(spinner(3), "\\");
        assert_eq!(spinner(4), "|"); // Wraps around
    }

    #[test]
    fn test_format_bytes() {
        assert_eq!(format_bytes(500), "500 B");
        assert_eq!(format_bytes(1024), "1.0 KB");
        assert_eq!(format_bytes(1536), "1.5 KB");
        assert_eq!(format_bytes(1048576), "1.0 MB");
    }

    #[test]
    fn test_format_time() {
        assert_eq!(format_time(65), "01:05");
        assert_eq!(format_time(3665), "01:01:05");
    }

    #[test]
    fn test_multi_progress() {
        let mut mp = MultiProgress::new(20);
        mp.add("Task 1", 50, 100);
        mp.add("Task 2", 25, 100);
        
        let rendered = mp.render();
        assert!(rendered.contains("Task 1"));
        assert!(rendered.contains("Task 2"));
    }
}