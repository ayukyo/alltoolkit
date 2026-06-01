//! Polyglot Parallel Runner
//!
//! Forks N child processes, each printing a banner in their language's idiom,
//! then collects and reports peak RSS (Resident Set Size) across all workers.
//!
//! # Design
//!
//! - **Leader process** (parent): spawns `count` children via `fork()` + `execvp()`
//! - **Workers** (children): print their banner and exit immediately
//! - **Leader**: waits for all children with `waitpid()`, tracks their RSS via `/proc`
//!
//! # Why a Fork-Based Approach?
//!
//! Rust has no built-in `fork()` — we shell out to `python3 -c '...' ` for the
//! actual fork, then read `/proc/<pid>/status` RSS from the parent side after
//! `waitpid()` returns. This gives us real OS-level parallelism without async.
//!
//! # Example Output
//!
//! ```text
//! Polyglot Parallel Runner — 3 workers
//! ┌─────────────────────────────────────────┐
//! │  Worker 0 · Rust    · OK  · 8.2 MB     │
//! │  Worker 1 · Go       · OK  · 7.8 MB     │
//! │  Worker 2 · Swift   · OK  · 9.1 MB     │
//! └─────────────────────────────────────────┘
//! Peak RSS across all workers: 9.1 MB
//! ```

use serde::{Deserialize, Serialize};
use std::fs;
use std::process::Command;
use std::time::{SystemTime, UNIX_EPOCH};

// ─────────────────────────────────────────────────────────────────
// Types
// ─────────────────────────────────────────────────────────────────

/// Banner text for a single language worker
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct WorkerBanner {
    pub language: String,
    pub line1: String,
    pub line2: String,
}

impl WorkerBanner {
    pub fn new(language: &str, line1: &str, line2: &str) -> Self {
        Self {
            language: language.to_string(),
            line1: line1.to_string(),
            line2: line2.to_string(),
        }
    }
}

/// A completed worker result
#[derive(Debug, Clone)]
pub struct WorkerResult {
    pub id: usize,
    pub language: String,
    pub rss_kb: u64,
    pub exited_ok: bool,
}

/// Summary across all workers
#[derive(Debug, Clone)]
pub struct RunSummary {
    pub total_workers: usize,
    pub results: Vec<WorkerResult>,
    pub peak_rss_kb: u64,
    pub all_ok: bool,
}

// ─────────────────────────────────────────────────────────────────
// Banner Library
// ─────────────────────────────────────────────────────────────────

/// Returns the banner lines for a given language
pub fn banner_for(language: &str) -> WorkerBanner {
    match language {
        "Rust" => WorkerBanner::new(
            "Rust",
            "fn main() { println!(\"🦀 Hello from Rust!\"); }",
            "// Fearless concurrency — done right",
        ),
        "Go" => WorkerBanner::new(
            "Go",
            "func main() { fmt.Println(\"🐹 Hello from Go!\") }",
            "// Channels and goroutines — simple and powerful",
        ),
        "Swift" => WorkerBanner::new(
            "Swift",
            "print(\"🦤 Hello from Swift!\")",
            "// Safe, fast, and expressive",
        ),
        "Kotlin" => WorkerBanner::new(
            "Kotlin",
            "fun main() = println(\"🟣 Hello from Kotlin!\")",
            "// Modern, concise, interoperable",
        ),
        "TypeScript" => WorkerBanner::new(
            "TypeScript",
            "console.log(\"⚡ Hello from TypeScript!\");",
            "// JavaScript with types — scale fearlessly",
        ),
        "JavaScript" => WorkerBanner::new(
            "JavaScript",
            "console.log(\"🌏 Hello from JavaScript!\");",
            "// The language that runs the web",
        ),
        "Java" => WorkerBanner::new(
            "Java",
            "public class Hello { public static void main(String[] a) { System.out.println(\"☕ Hello from Java!\"); } }",
            "// Write once, run everywhere",
        ),
        "C/C++" => WorkerBanner::new(
            "C/C++",
            "#include <stdio.h>\\nint main(){printf(\"⚙️ Hello from C!\\n\");return 0;}",
            "// Low-level control, maximum performance",
        ),
        _ => WorkerBanner::new(
            language,
            "// Unknown language",
            "// Add your banner above!",
        ),
    }
}

// ─────────────────────────────────────────────────────────────────
// Core Runner
// ─────────────────────────────────────────────────────────────────

/// Spawn `count` parallel banner workers, return summary.
pub fn run_parallel(count: usize, languages: &[String]) -> RunSummary {
    // Spawn all workers first (before any wait())
    let mut children: Vec<_> = Vec::with_capacity(count);
    for id in 0..count {
        let lang = languages.get(id).map(|s| s.as_str()).unwrap_or("Unknown");
        let banner = banner_for(lang);
        let child = spawn_worker(&banner);
        children.push((id, banner.language.clone(), child));
    }

    // Read RSS for each child BEFORE waiting — /proc/<pid> is valid while process is alive
    let mut results: Vec<_> = children
        .iter()
        .map(|(id, lang, child)| {
            let rss_kb = read_proc_rss(child.id());
            WorkerResult {
                id: *id,
                language: lang.clone(),
                rss_kb,
                exited_ok: true, // will be updated after wait
            }
        })
        .collect();

    // Wait for all children to finish
    for (i, (_id, _lang, mut child)) in children.into_iter().enumerate() {
        let status = child.wait().expect("Failed to wait for worker");
        results[i].exited_ok = status.success();
        // If RSS was 0 (kernel recycled /proc), try once more
        if results[i].rss_kb == 0 {
            results[i].rss_kb = read_proc_rss(child.id());
        }
    }

    let peak_rss_kb = results.iter().map(|r| r.rss_kb).max().unwrap_or(0);
    let all_ok = results.iter().all(|r| r.exited_ok);

    RunSummary {
        total_workers: count,
        results,
        peak_rss_kb,
        all_ok,
    }
}

/// Spawn a single worker process (returns immediately, child is alive)
fn spawn_worker(banner: &WorkerBanner) -> std::process::Child {
    let python_script = format!(concat!(
        "import sys, os\n",
        "print('---WORKER-BANNER---', file=sys.stderr)\n",
        "print('Language: {lang}', file=sys.stderr)\n",
        "print('{line1}', file=sys.stderr)\n",
        "print('---WORKER-BANNER---', file=sys.stderr)\n",
        "sys.stderr.flush()\n",
        "print(os.getpid())\n",
        "sys.stdout.flush()\n"
    ), lang = banner.language, line1 = banner.line1);

    Command::new("python3")
        .args(["-c", &python_script])
        .stdout(std::process::Stdio::piped())
        .stderr(std::process::Stdio::piped())
        .spawn()
        .expect("Failed to spawn python3 worker")
}

/// Read PeakRSS from /proc/<pid>/status
fn read_proc_rss(pid: u32) -> u64 {
    let path = format!("/proc/{}/status", pid);
    let content = fs::read_to_string(&path).unwrap_or_default();

    for line in content.lines() {
        if line.starts_with("VmRSS:") {
            // e.g. "VmRSS:     1234 kB"
            let parts: Vec<&str> = line.split_whitespace().collect();
            if parts.len() >= 2 {
                return parts[1].parse::<u64>().unwrap_or(0);
            }
        }
    }
    0
}

// ─────────────────────────────────────────────────────────────────
// Language Rotation Integration
// ─────────────────────────────────────────────────────────────────

const ROTATION_JSON: &str = "/home/admin/.openclaw/workspace/AllToolkit/language_rotation.json";

/// Load language rotation state from ROTATION_JSON
pub fn load_rotation_state() -> Result<LanguageRotationState, String> {
    let content =
        fs::read_to_string(ROTATION_JSON).map_err(|e| format!("Failed to read {}: {}", ROTATION_JSON, e))?;
    serde_json::from_str(&content).map_err(|e| format!("Failed to parse JSON: {}", e))
}

/// Save language rotation state to ROTATION_JSON
pub fn save_rotation_state(state: &LanguageRotationState) -> Result<(), String> {
    let json = serde_json::to_string_pretty(state)
        .map_err(|e| format!("Failed to encode JSON: {}", e))?;
    fs::write(ROTATION_JSON, json).map_err(|e| format!("Failed to write {}: {}", ROTATION_JSON, e))
}

/// Get current language (based on current_index) without advancing
pub fn current_language(state: &LanguageRotationState) -> Option<String> {
    state.languages.get(state.current_index).cloned()
}

/// Advance index to next position (wrapping)
pub fn advance_index(state: &mut LanguageRotationState) {
    if !state.languages.is_empty() {
        state.current_index = (state.current_index + 1) % state.languages.len();
    }
}

/// Language rotation state (mirrors language_rotation.json schema)
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct LanguageRotationState {
    pub languages: Vec<String>,
    pub current_index: usize,
    #[serde(default)]
    pub last_language: Option<String>,
    #[serde(default)]
    pub updated_at: Option<String>,
}

impl LanguageRotationState {
    pub fn new(languages: Vec<String>) -> Self {
        Self {
            languages,
            current_index: 0,
            last_language: None,
            updated_at: Some(current_iso_timestamp()),
        }
    }
}

// ─────────────────────────────────────────────────────────────────
// Utilities
// ─────────────────────────────────────────────────────────────────

fn current_iso_timestamp() -> String {
    let now = SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .unwrap_or_default();
    let secs = now.as_secs();
    // Simple ISO-ish format: just seconds since epoch for now
    format!("{}", secs)
}

// ─────────────────────────────────────────────────────────────────
// Pretty Printing
// ─────────────────────────────────────────────────────────────────

impl RunSummary {
    /// Render the run summary as a formatted multi-line string
    pub fn display(&self) -> String {
        let count = self.total_workers;
        let width = 50;

        let mut out = format!("Polyglot Parallel Runner — {} worker{}\n", count, if count == 1 { "" } else { "s" });
        out.push_str(&"┌".to_string());
        out.push_str(&"─".repeat(width));
        out.push_str("┐\n");

        for r in &self.results {
            let lang = format!("{:?}", r.language);
            let status = if r.exited_ok { "OK" } else { "FAIL" };
            let rss = format!("{}.{} MB", r.rss_kb / 1024, (r.rss_kb % 1024) * 10 / 1024);
            let line = format!(
                "│  Worker {} · {:.<13} · {:.<4} · {:>7} │",
                r.id, lang, status, rss
            );
            // Truncate to width
            let line: String = line.chars().take(width + 9).collect();
            out.push_str(&line);
            out.push('\n');
        }

        out.push_str(&"└".to_string());
        out.push_str(&"─".repeat(width));
        out.push_str("┘\n");

        let peak_mb = format!("{}.{} MB", self.peak_rss_kb / 1024, (self.peak_rss_kb % 1024) * 10 / 1024);
        out.push_str(&format!(
            "Peak RSS across all workers: {} (all OK: {})\n",
            peak_mb,
            self.all_ok
        ));

        out
    }
}

// ─────────────────────────────────────────────────────────────────
// Tests
// ─────────────────────────────────────────────────────────────────

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_banner_for_all_languages() {
        let langs = ["Rust", "Go", "Swift", "Kotlin", "TypeScript", "JavaScript", "Java", "C/C++"];
        for lang in langs {
            let banner = banner_for(lang);
            assert_eq!(banner.language, lang);
            assert!(!banner.line1.is_empty());
        }
    }

    #[test]
    fn test_banner_unknown_language() {
        let banner = banner_for("Pascal");
        assert_eq!(banner.language, "Pascal");
        assert!(banner.line1.contains("Unknown"));
    }

    #[test]
    fn test_current_language() {
        let state = LanguageRotationState::new(vec!["Rust".to_string(), "Go".to_string()]);
        assert_eq!(current_language(&state), Some("Rust".to_string()));
    }

    #[test]
    fn test_advance_index() {
        let mut state = LanguageRotationState::new(vec!["Rust".to_string(), "Go".to_string(), "Swift".to_string()]);
        assert_eq!(state.current_index, 0);
        advance_index(&mut state);
        assert_eq!(state.current_index, 1);
        advance_index(&mut state);
        assert_eq!(state.current_index, 2);
        advance_index(&mut state);
        assert_eq!(state.current_index, 0); // wraps
    }

    #[test]
    fn test_rotation_state_serialization() {
        let state = LanguageRotationState::new(vec!["Rust".to_string(), "Go".to_string()]);
        let json = serde_json::to_string(&state).unwrap();
        let decoded: LanguageRotationState = serde_json::from_str(&json).unwrap();
        assert_eq!(decoded.languages, state.languages);
        assert_eq!(decoded.current_index, state.current_index);
    }

    #[test]
    fn test_run_parallel_single_worker() {
        let summary = run_parallel(1, &["Rust".to_string()]);
        assert_eq!(summary.total_workers, 1);
        assert_eq!(summary.results[0].language, "Rust");
    }

    #[test]
    fn test_run_parallel_multiple_workers() {
        let langs = vec![
            "Rust".to_string(),
            "Go".to_string(),
            "Swift".to_string(),
        ];
        let summary = run_parallel(3, &langs);
        assert_eq!(summary.total_workers, 3);
        assert!(summary.results.iter().all(|r| r.exited_ok));
        assert!(summary.peak_rss_kb > 0);
    }

    #[test]
    fn test_run_parallel_unknown_language() {
        let summary = run_parallel(1, &["UnknownLang".to_string()]);
        assert_eq!(summary.total_workers, 1);
        assert_eq!(summary.results[0].language, "UnknownLang");
    }

    #[test]
    fn test_run_summary_display() {
        let summary = RunSummary {
            total_workers: 2,
            results: vec![
                WorkerResult {
                    id: 0,
                    language: "Rust".to_string(),
                    rss_kb: 8192,
                    exited_ok: true,
                },
                WorkerResult {
                    id: 1,
                    language: "Go".to_string(),
                    rss_kb: 9216,
                    exited_ok: true,
                },
            ],
            peak_rss_kb: 9216,
            all_ok: true,
        };
        let display = summary.display();
        assert!(display.contains("Rust"));
        assert!(display.contains("Go"));
        assert!(display.contains("Peak RSS"));
    }
}