//! Language Safety Matrix — Memory & Type Safety Analysis Tool
//!
//! Generates a comparative safety matrix across programming languages,
//! analyzing dimensions like memory model, type safety, concurrency safety,
//! null safety, and overflow handling. Each language gets a multi-dimensional
//! safety profile that developers can use to reason about trust boundaries.
//!
//! # Creative Concept
//!
//! Every language makes a trade-off between safety and control. This tool
//! builds a safety radar chart (text-based) showing where each language
//! stands on 8 safety axes, helping developers choose languages that match
//! their risk tolerance and correctness requirements.
//!
//! Distinct from existing tools:
//! - language_sage: idioms, pro tips, pitfalls (learning-focused)
//! - language_archaeology: historical origins, design philosophy (history)
//! - language_probe: runtime availability, version, capabilities (runtime)
//! - language_mastery: XP/level progress tracking (gamification)
//! - language_compass: learning journey milestones (education path)
//! - language_rotator: round-robin scheduling with weights/cooldowns (orchestration)
//!
//! This tool is about SAFETY ANALYSIS — a technical comparison dimension.

use serde::{Deserialize, Serialize};
use std::collections::BTreeMap;

/// Safety axis name
pub type AxisName = &'static str;

/// Score on an axis (0.0 = none, 1.0 = full protection)
pub type SafetyScore = f64;

/// A single axis evaluation
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AxisResult {
    pub name: AxisName,
    pub score: SafetyScore,
    pub verdict: &'static str,
    pub detail: String,
}

/// Full safety profile for one language
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct LanguageSafetyProfile {
    pub language: String,
    pub axes: Vec<AxisResult>,
    pub overall_score: SafetyScore,
    pub risk_profile: &'static str,
}

/// The 8 safety axes
pub const SAFETY_AXES: &[AxisName] = &[
    "Memory Safety",
    "Type Safety",
    "Concurrency Safety",
    "Null Safety",
    "Overflow Safety",
    "Aliasing Safety",
    "Uninitialized Safety",
    "Escape Safety",
];

impl LanguageSafetyProfile {
    /// Generate a safety profile for a named language
    pub fn generate(language: &str) -> Self {
        match language {
            "Rust" => Self::rust(),
            "Go" => Self::go(),
            "Swift" => Self::swift(),
            "Kotlin" => Self::kotlin(),
            "TypeScript" => Self::typescript(),
            "JavaScript" => Self::javascript(),
            "Java" => Self::java(),
            "C/C++" | "C++" => Self::cpp(),
            "C" => Self::c(),
            other => Self::unknown(other),
        }
    }

    fn rust() -> Self {
        let axes = vec![
            AxisResult {
                name: "Memory Safety",
                score: 1.0,
                verdict: "✅ Full",
                detail: "Ownership + borrowing enforces exclusive access. No dangling pointers, no double-free, no use-after-free.".into(),
            },
            AxisResult {
                name: "Type Safety",
                score: 1.0,
                verdict: "✅ Full",
                detail: "Strong static typing with inference. No implicit casts between incompatible types.".into(),
            },
            AxisResult {
                name: "Concurrency Safety",
                score: 1.0,
                verdict: "✅ Full",
                detail: "Send/Sync traits encode thread safety in types. Data races are compile-time errors.".into(),
            },
            AxisResult {
                name: "Null Safety",
                score: 1.0,
                verdict: "✅ Full",
                detail: "Option<T> makes absence explicit. Match-based handling never panics on None.".into(),
            },
            AxisResult {
                name: "Overflow Safety",
                score: 0.9,
                verdict: "✅ Near-full",
                detail: "Checked arithmetic in debug (panic), wrapping in release. overflow-checks flag available.".into(),
            },
            AxisResult {
                name: "Aliasing Safety",
                score: 1.0,
                verdict: "✅ Full",
                detail: "Borrow checker enforces at most one mutable reference OR any number of shared references.".into(),
            },
            AxisResult {
                name: "Uninitialized Safety",
                score: 1.0,
                verdict: "✅ Full",
                detail: "Every variable must be initialized before use. No undefined states.".into(),
            },
            AxisResult {
                name: "Escape Safety",
                score: 1.0,
                verdict: "✅ Full",
                detail: "Lifetime annotations prove references don't outlive the data they point to.".into(),
            },
        ];
        let overall_score = axes.iter().map(|a| a.score).sum::<f64>() / axes.len() as f64;
        Self {
            language: "Rust".into(),
            axes,
            overall_score,
            risk_profile: "🛡️ Fort Knox — maximum safety with zero-cost abstractions",
        }
    }

    fn go() -> Self {
        let axes = vec![
            AxisResult {
                name: "Memory Safety",
                score: 0.95,
                verdict: "✅ Near-full",
                detail: "GC eliminates heap dangling pointers. Stack-allocated slices are bounds-checked.".into(),
            },
            AxisResult {
                name: "Type Safety",
                score: 0.85,
                verdict: "⚠️ Mostly",
                detail: "Strong static typing. However, interface{} erases type info (requires type assertions).".into(),
            },
            AxisResult {
                name: "Concurrency Safety",
                score: 0.8,
                verdict: "⚠️ CSP helps, but...",
                detail: "Channels prevent shared-memory concurrency, but shared maps/slices across goroutines cause races.".into(),
            },
            AxisResult {
                name: "Null Safety",
                score: 0.7,
                verdict: "⚠️ Partial",
                detail: "nil is a valid zero value for pointers/interfaces. No null pointer exceptions but silent failures possible.".into(),
            },
            AxisResult {
                name: "Overflow Safety",
                score: 0.7,
                verdict: "⚠️ Silent wrap",
                detail: "Integer overflow wraps silently in Go 1.17+. Must use big.Int or manually check.".into(),
            },
            AxisResult {
                name: "Aliasing Safety",
                score: 0.6,
                verdict: "⚠️ Shared aliasing allowed",
                detail: "Slices are reference types — two slices can share the same underlying array.".into(),
            },
            AxisResult {
                name: "Uninitialized Safety",
                score: 0.9,
                verdict: "✅ Mostly",
                detail: "Zero values for all types, but zero value of sync.Mutex is locked (a footgun).".into(),
            },
            AxisResult {
                name: "Escape Safety",
                score: 0.8,
                verdict: "⚠️ Escape analysis exists",
                detail: "Compiler decides heap vs stack via escape analysis, but this is opaque to the programmer.".into(),
            },
        ];
        let overall_score = axes.iter().map(|a| a.score).sum::<f64>() / axes.len() as f64;
        Self {
            language: "Go".into(),
            axes,
            overall_score,
            risk_profile: "🛡️ Strong — GC-protected but some sharp edges",
        }
    }

    fn swift() -> Self {
        let axes = vec![
            AxisResult {
                name: "Memory Safety",
                score: 0.95,
                verdict: "✅ Near-full",
                detail: "ARC (Automatic Reference Counting) prevents leaks. Retain cycles require weak/unowned breaks.".into(),
            },
            AxisResult {
                name: "Type Safety",
                score: 1.0,
                verdict: "✅ Full",
                detail: "Protocol-oriented type system with generics, associated types, and protocol compositions.".into(),
            },
            AxisResult {
                name: "Concurrency Safety",
                score: 0.85,
                verdict: "⚠️ Actor model in Swift 5.5+",
                detail: "Actors isolate mutable state. async/await with task groups. Older code relies on Serial DispatchQueue.".into(),
            },
            AxisResult {
                name: "Null Safety",
                score: 1.0,
                verdict: "✅ Full",
                detail: "Optional<T> (like Rust's Option) makes nil explicit. Optional chaining and nil-coalescing operators.".into(),
            },
            AxisResult {
                name: "Overflow Safety",
                score: 0.7,
                verdict: "⚠️ Traps in debug",
                detail: "+ & - overflow traps in debug, wraps in release. .addingReportingOverflow() available.".into(),
            },
            AxisResult {
                name: "Aliasing Safety",
                score: 0.75,
                verdict: "⚠️ Class vs struct distinction",
                detail: "Classes allow shared mutable state (aliasing). Structs are value types (copied).".into(),
            },
            AxisResult {
                name: "Uninitialized Safety",
                score: 0.9,
                verdict: "✅ Mostly",
                detail: "Optional properties can be uninitialized. let must be initialized before use.".into(),
            },
            AxisResult {
                name: "Escape Safety",
                score: 0.85,
                verdict: "⚠️ Closures capture by capture list",
                detail: "Closures are reference types. Must use [weak self] or [unowned self] to avoid retain cycles.".into(),
            },
        ];
        let overall_score = axes.iter().map(|a| a.score).sum::<f64>() / axes.len() as f64;
        Self {
            language: "Swift".into(),
            axes,
            overall_score,
            risk_profile: "🛡️ Strong — value types + optionals, minor ARC footguns",
        }
    }

    fn kotlin() -> Self {
        let axes = vec![
            AxisResult {
                name: "Memory Safety",
                score: 0.95,
                verdict: "✅ Near-full",
                detail: "JVM GC handles heap. Kotlin cannot allocate arbitrary memory. Primitive types on stack.".into(),
            },
            AxisResult {
                name: "Type Safety",
                score: 0.9,
                verdict: "✅ Strong",
                detail: "Non-nullable types by default, sealed classes, reified generics (in inline functions).".into(),
            },
            AxisResult {
                name: "Concurrency Safety",
                score: 0.65,
                verdict: "⚠️ Coroutines help but...",
                detail: "Coroutines are structured but shared mutable state still requires explicit synchronization.".into(),
            },
            AxisResult {
                name: "Null Safety",
                score: 1.0,
                verdict: "✅ Full",
                detail: "Non-nullable types by default. ? suffix for nullable. Elvis operator for safe defaults.".into(),
            },
            AxisResult {
                name: "Overflow Safety",
                score: 0.7,
                verdict: "⚠️ JVM-based",
                detail: "Inherits JVM overflow semantics: throws ArithmeticException on overflow in some contexts.".into(),
            },
            AxisResult {
                name: "Aliasing Safety",
                score: 0.6,
                verdict: "⚠️ Reference types alias",
                detail: "Classes are references (aliased). data classes / value classes help. Collections alias.".into(),
            },
            AxisResult {
                name: "Uninitialized Safety",
                score: 0.8,
                verdict: "⚠️ lateinit + notNull",
                detail: "var can be uninitialized with lateinit var or delegates.notNull(). Throws if accessed early.".into(),
            },
            AxisResult {
                name: "Escape Safety",
                score: 0.7,
                verdict: "⚠️ JVM escape analysis basic",
                detail: "Escape analysis is JVM-level and limited. Stack allocation only for simple cases.".into(),
            },
        ];
        let overall_score = axes.iter().map(|a| a.score).sum::<f64>() / axes.len() as f64;
        Self {
            language: "Kotlin".into(),
            axes,
            overall_score,
            risk_profile: "🛡️ Strong null safety, JVM safety net, coroutine footguns",
        }
    }

    fn typescript() -> Self {
        let axes = vec![
            AxisResult {
                name: "Memory Safety",
                score: 0.85,
                verdict: "⚠️ GC-managed but...",
                detail: "JS runtime GC. No manual memory errors. Phantom reference leaks possible.".into(),
            },
            AxisResult {
                name: "Type Safety",
                score: 0.85,
                verdict: "⚠️ Gradual typing",
                detail: "TypeScript adds static types, but any cast bypasses checks. Structural typing is flexible.".into(),
            },
            AxisResult {
                name: "Concurrency Safety",
                score: 0.6,
                verdict: "⚠️ Event loop limits",
                detail: "Single-threaded event loop prevents low-level races. Shared DOM state = footguns.".into(),
            },
            AxisResult {
                name: "Null Safety",
                score: 0.6,
                verdict: "⚠️ undefined vs null",
                detail: "Both undefined and null exist. Optional chaining helps. strictNullChecks helps a lot.".into(),
            },
            AxisResult {
                name: "Overflow Safety",
                score: 0.5,
                verdict: "❌ IEEE-754 NaN/Inf",
                detail: "All numbers are IEEE-754 doubles. 1e309 = Infinity, no overflow exception. NaN propagation.".into(),
            },
            AxisResult {
                name: "Aliasing Safety",
                score: 0.5,
                verdict: "⚠️ Objects are refs",
                detail: "Objects, arrays, functions are reference types. Destructuring makes copies of primitives.".into(),
            },
            AxisResult {
                name: "Uninitialized Safety",
                score: 0.7,
                verdict: "⚠️ hoisting + TDZ",
                detail: "var hoisting causes subtle bugs. let/const in TDZ (temporal dead zone) until initialized.".into(),
            },
            AxisResult {
                name: "Escape Safety",
                score: 0.85,
                verdict: "✅ Sandbox limits escape",
                detail: "Browser sandbox prevents arbitrary OS access. Node.js has module boundary discipline.".into(),
            },
        ];
        let overall_score = axes.iter().map(|a| a.score).sum::<f64>() / axes.len() as f64;
        Self {
            language: "TypeScript".into(),
            axes,
            overall_score,
            risk_profile: "⚠️ Moderate — runtime duck typing, JS heritage",
        }
    }

    fn javascript() -> Self {
        let axes = vec![
            AxisResult {
                name: "Memory Safety",
                score: 0.8,
                verdict: "⚠️ GC, but leaks exist",
                detail: "JS GC prevents manual dangling pointers. Closure memory leaks from retained references.".into(),
            },
            AxisResult {
                name: "Type Safety",
                score: 0.3,
                verdict: "❌ None (dynamic)",
                detail: "Pure dynamic typing. typeof is unreliable. No compile-time checks whatsoever.".into(),
            },
            AxisResult {
                name: "Concurrency Safety",
                score: 0.6,
                verdict: "⚠️ Event loop limits",
                detail: "Single-threaded loop avoids shared-memory races. Web Workers are isolated.".into(),
            },
            AxisResult {
                name: "Null Safety",
                score: 0.5,
                verdict: "⚠️ undefined/null chaos",
                detail: "Both exist with subtly different semantics. == null catches both but == undefined only undefined.".into(),
            },
            AxisResult {
                name: "Overflow Safety",
                score: 0.4,
                verdict: "❌ IEEE-754 only",
                detail: "No integer type. Numbers silently become Infinity or NaN on overflow. No integer math safety.".into(),
            },
            AxisResult {
                name: "Aliasing Safety",
                score: 0.4,
                verdict: "❌ Reference chaos",
                detail: "Objects are mutable references. spread [...] makes shallow copies only. Deep aliasing common.".into(),
            },
            AxisResult {
                name: "Uninitialized Safety",
                score: 0.5,
                verdict: "⚠️ hoisting mess",
                detail: "var hoisted to function scope with undefined value. Access before declaration = undefined (not error).".into(),
            },
            AxisResult {
                name: "Escape Safety",
                score: 0.85,
                verdict: "✅ Sandbox",
                detail: "Browser sandbox prevents OS access. CSP limits code injection. Node.js needs discipline.".into(),
            },
        ];
        let overall_score = axes.iter().map(|a| a.score).sum::<f64>() / axes.len() as f64;
        Self {
            language: "JavaScript".into(),
            axes,
            overall_score,
            risk_profile: "☠️ High risk — pure dynamic typing, JS legacy quirks",
        }
    }

    fn java() -> Self {
        let axes = vec![
            AxisResult {
                name: "Memory Safety",
                score: 0.95,
                verdict: "✅ Near-full",
                detail: "JVM GC. No direct pointer arithmetic. Array bounds checked. Heap-only allocation.".into(),
            },
            AxisResult {
                name: "Type Safety",
                score: 0.9,
                verdict: "✅ Strong static",
                detail: "Strong static typing with generics. Type erasure is a limitation for reflection.".into(),
            },
            AxisResult {
                name: "Concurrency Safety",
                score: 0.6,
                verdict: "⚠️ synchronized + volatile",
                detail: "Built-in monitors but race conditions on shared mutable state are a persistent Java problem.".into(),
            },
            AxisResult {
                name: "Null Safety",
                score: 0.3,
                verdict: "❌ NullPointerException",
                detail: "null is a valid value for any reference type. NPE is the billion-dollar mistake, confirmed.".into(),
            },
            AxisResult {
                name: "Overflow Safety",
                score: 0.7,
                verdict: "⚠️ Checked vs unchecked",
                detail: "Checked exceptions force handling for overflow (IOException etc). Arithmetic overflow unchecked.".into(),
            },
            AxisResult {
                name: "Aliasing Safety",
                score: 0.5,
                verdict: "⚠️ Reference semantics",
                detail: "Objects aliased via references. Collections store references. Immutable wrappers available.".into(),
            },
            AxisResult {
                name: "Uninitialized Safety",
                score: 0.7,
                verdict: "⚠️ Fields zero-initialized",
                detail: "Instance fields get zero/false/null defaults. Static fields same. Local vars must be initialized.".into(),
            },
            AxisResult {
                name: "Escape Safety",
                score: 0.7,
                verdict: "⚠️ JVM sandbox model",
                detail: "SecurityManager deprecated. Module system (Java 9+) provides encapsulation.".into(),
            },
        ];
        let overall_score = axes.iter().map(|a| a.score).sum::<f64>() / axes.len() as f64;
        Self {
            language: "Java".into(),
            axes,
            overall_score,
            risk_profile: "🛡️ JVM safety net, but NPE is endemic",
        }
    }

    fn cpp() -> Self {
        let axes = vec![
            AxisResult {
                name: "Memory Safety",
                score: 0.2,
                verdict: "❌ Dangerous",
                detail: "Manual heap management. dangling pointers, double-free, use-after-free all possible.".into(),
            },
            AxisResult {
                name: "Type Safety",
                score: 0.5,
                verdict: "⚠️ Limited",
                detail: "Implicit conversions, reinterpret_cast, void*. noexcept is not enforced at compile time.".into(),
            },
            AxisResult {
                name: "Concurrency Safety",
                score: 0.3,
                verdict: "❌ Manual",
                detail: "std::thread, mutex, atomic — all manual. Data races are UB. No type-level thread safety.".into(),
            },
            AxisResult {
                name: "Null Safety",
                score: 0.2,
                verdict: "❌ Raw pointers nullable",
                detail: "Raw pointers can be null. nullptr introduced but doesn't prevent dereference bugs.".into(),
            },
            AxisResult {
                name: "Overflow Safety",
                score: 0.2,
                verdict: "❌ Undefined behavior",
                detail: "Signed integer overflow = UB. Unsigned wraps. sanitizer required to detect.".into(),
            },
            AxisResult {
                name: "Aliasing Safety",
                score: 0.2,
                verdict: "❌ UB aliasing rules",
                detail: "Strict aliasing rule is easily violated. memset on wrong type = UB. Optimization hazards.".into(),
            },
            AxisResult {
                name: "Uninitialized Safety",
                score: 0.2,
                verdict: "❌ Uninitialized reads UB",
                detail: "Reading uninitialized memory of non-trivial type is UB. Members not auto-initialized.".into(),
            },
            AxisResult {
                name: "Escape Safety",
                score: 0.4,
                verdict: "⚠️ manual, sanitizers help",
                detail: "AddressSanitizer, MemorySanitizer, UBSan detect issues. No runtime sandbox by default.".into(),
            },
        ];
        let overall_score = axes.iter().map(|a| a.score).sum::<f64>() / axes.len() as f64;
        Self {
            language: "C/C++".into(),
            axes,
            overall_score,
            risk_profile: "☠️ Maximum control, minimum safety net — requires rigorous tooling",
        }
    }

    fn c() -> Self {
        let mut profile = Self::cpp();
        profile.language = "C".into();
        profile.overall_score = profile.axes.iter().map(|a| a.score).sum::<f64>() / profile.axes.len() as f64;
        profile.risk_profile = "☠️ Bare metal — no safety net whatsoever";
        profile
    }

    fn unknown(language: &str) -> Self {
        let axes = SAFETY_AXES
            .iter()
            .map(|&name| AxisResult {
                name,
                score: 0.0,
                verdict: "❓ Unknown",
                detail: format!("No safety data for language: {}", language),
            })
            .collect();
        Self {
            language: language.into(),
            axes,
            overall_score: 0.0,
            risk_profile: "❓ Unknown",
        }
    }

    /// Render a text-based radar chart for this profile
    pub fn radar_chart(&self) -> String {
        let mut lines = vec![format!("\n🛡️ Safety Radar: {} ({:.0}% overall)\n", self.language, self.overall_score * 100.0)];

        // Find max detail length for alignment
        let max_detail_len = self.axes.iter().map(|a| a.detail.len()).max().unwrap_or(0).min(60);
        let bar_width = 20_usize;

        for axis in &self.axes {
            let filled = (axis.score * bar_width as f64).round() as usize;
            let empty = bar_width - filled;
            let bar = format!("{}{}", "█".repeat(filled), "░".repeat(empty));
            let detail = if axis.detail.len() > max_detail_len {
                format!("{}...", &axis.detail[..max_detail_len - 3])
            } else {
                axis.detail.clone()
            };
            lines.push(format!(
                "  {:20} [{}] {:4.0}%  {}",
                axis.name, bar, axis.score * 100.0, detail
            ));
        }
        lines.push(format!("\n  Risk Profile: {}", self.risk_profile));
        lines.join("\n")
    }
}

/// Generate a comparative matrix for multiple languages
pub fn generate_matrix(languages: &[&str]) -> BTreeMap<String, LanguageSafetyProfile> {
    languages
        .iter()
        .map(|&lang| {
            let profile = LanguageSafetyProfile::generate(lang);
            (lang.to_string(), profile)
        })
        .collect()
}

/// Compare two languages side-by-side on an axis
pub fn compare_on_axis(profile_a: &LanguageSafetyProfile, profile_b: &LanguageSafetyProfile, axis: AxisName) -> (&'static str, f64, f64) {
    let score_a = profile_a.axes.iter().find(|a| a.name == axis).map(|a| a.score).unwrap_or(0.0);
    let score_b = profile_b.axes.iter().find(|a| a.name == axis).map(|a| a.score).unwrap_or(0.0);
    (axis, score_a, score_b)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_rust_profile() {
        let profile = LanguageSafetyProfile::generate("Rust");
        assert_eq!(profile.language, "Rust");
        assert_eq!(profile.axes.len(), 8);
        // Rust scores 1.0 on most axes
        let memory_score = profile.axes.iter().find(|a| a.name == "Memory Safety").unwrap().score;
        assert_eq!(memory_score, 1.0);
        assert!(profile.overall_score > 0.95);
    }

    #[test]
    fn test_all_languages_known() {
        for lang in ["Rust", "Go", "Swift", "Kotlin", "TypeScript", "JavaScript", "Java", "C/C++"] {
            let profile = LanguageSafetyProfile::generate(lang);
            assert_eq!(profile.axes.len(), 8);
            assert!(profile.overall_score >= 0.0);
            assert!(profile.overall_score <= 1.0);
        }
    }

    #[test]
    fn test_unknown_language() {
        let profile = LanguageSafetyProfile::generate("Brainfuck");
        assert_eq!(profile.language, "Brainfuck");
        assert_eq!(profile.overall_score, 0.0);
        assert_eq!(profile.risk_profile, "❓ Unknown");
    }

    #[test]
    fn test_cpp_high_risk() {
        let profile = LanguageSafetyProfile::generate("C/C++");
        // C/C++ should have low overall score
        assert!(profile.overall_score < 0.4);
    }

    #[test]
    fn test_compare_on_axis() {
        let rust = LanguageSafetyProfile::generate("Rust");
        let js = LanguageSafetyProfile::generate("JavaScript");
        let axis_name = "Memory Safety";
        let (_, rust_score, js_score) = compare_on_axis(&rust, &js, axis_name);
        assert!(rust_score > js_score);
    }

    #[test]
    fn test_radar_chart_contains_language() {
        let profile = LanguageSafetyProfile::generate("Go");
        let chart = profile.radar_chart();
        assert!(chart.contains("Go"));
        assert!(chart.contains("Safety Radar"));
    }

    #[test]
    fn test_generate_matrix() {
        let matrix = generate_matrix(&["Rust", "Go", "JavaScript"]);
        assert_eq!(matrix.len(), 3);
        assert!(matrix.contains_key("Rust"));
        assert!(matrix.contains_key("Go"));
        assert!(matrix.contains_key("JavaScript"));
    }

    #[test]
    fn test_null_safety_ordering() {
        // Null safety should be: Rust=1.0, Kotlin=1.0, Swift=1.0, TypeScript=0.6, JavaScript=0.5, Java=0.3, C/C++=0.2
        let langs = ["Rust", "Kotlin", "Java"];
        let scores: Vec<SafetyScore> = langs
            .iter()
            .map(|&l| {
                LanguageSafetyProfile::generate(l)
                    .axes
                    .iter()
                    .find(|a| a.name == "Null Safety")
                    .unwrap()
                    .score
            })
            .collect();
        assert!(scores[0] >= scores[1]); // Rust >= Kotlin
        assert!(scores[1] > scores[2]);   // Kotlin > Java
    }

    #[test]
    fn test_axis_scores_bounded() {
        for lang in ["Rust", "Go", "Swift", "Kotlin", "TypeScript", "JavaScript", "Java", "C/C++"] {
            let profile = LanguageSafetyProfile::generate(lang);
            for axis in &profile.axes {
                assert!(axis.score >= 0.0 && axis.score <= 1.0, "Score out of bounds for {} on {}", lang, axis.name);
            }
        }
    }

    #[test]
    fn test_safety_axes_count() {
        assert_eq!(SAFETY_AXES.len(), 8);
        assert!(SAFETY_AXES.contains(&"Memory Safety"));
        assert!(SAFETY_AXES.contains(&"Type Safety"));
        assert!(SAFETY_AXES.contains(&"Concurrency Safety"));
        assert!(SAFETY_AXES.contains(&"Null Safety"));
        assert!(SAFETY_AXES.contains(&"Overflow Safety"));
        assert!(SAFETY_AXES.contains(&"Aliasing Safety"));
        assert!(SAFETY_AXES.contains(&"Uninitialized Safety"));
        assert!(SAFETY_AXES.contains(&"Escape Safety"));
    }
}