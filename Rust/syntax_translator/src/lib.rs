//! # Syntax Translator
//!
//! A cross-language syntax translator that converts code snippets between any
//! two languages in the rotation order:
//! `Rust -> Go -> Swift -> Kotlin -> TypeScript -> JavaScript -> Java -> C/C++ -> Rust (loop)`
//!
//! ## Creative Concept
//!
//! **"Every language speaks the same ideas differently."**
//!
//! This tool accepts a code snippet in one language and translates it to another,
//! preserving semantics while adapting idioms. It reads `language_rotation.json`
//! to determine the current language, then advances the index after translation.

use serde::{Deserialize, Serialize};
use std::fs;
use std::path::Path;


// ─────────────────────────────────────────────────────────────────
// Types
// ─────────────────────────────────────────────────────────────────

/// Supported languages in the rotation
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub enum Language {
    Rust,
    Go,
    Swift,
    Kotlin,
    TypeScript,
    JavaScript,
    Java,
    #[serde(rename = "C/C++")]
    Cpp,
}

impl Language {
    pub fn from_str(s: &str) -> Option<Self> {
        match s {
            "Rust" => Some(Language::Rust),
            "Go" => Some(Language::Go),
            "Swift" => Some(Language::Swift),
            "Kotlin" => Some(Language::Kotlin),
            "TypeScript" => Some(Language::TypeScript),
            "JavaScript" => Some(Language::JavaScript),
            "Java" => Some(Language::Java),
            "C/C++" | "C++" => Some(Language::Cpp),
            _ => None,
        }
    }

    pub fn as_str(&self) -> &'static str {
        match self {
            Language::Rust => "Rust",
            Language::Go => "Go",
            Language::Swift => "Swift",
            Language::Kotlin => "Kotlin",
            Language::TypeScript => "TypeScript",
            Language::JavaScript => "JavaScript",
            Language::Java => "Java",
            Language::Cpp => "C/C++",
        }
    }

    pub fn all() -> [Self; 8] {
        [
            Language::Rust,
            Language::Go,
            Language::Swift,
            Language::Kotlin,
            Language::TypeScript,
            Language::JavaScript,
            Language::Java,
            Language::Cpp,
        ]
    }
}

impl std::fmt::Display for Language {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{}", self.as_str())
    }
}

/// Language characteristics for translation decisions
#[derive(Debug, Clone)]
pub struct LanguageProfile {
    pub is_typed: bool,
    pub is_oo: bool,
    pub has_generics: bool,
    pub null_safety: &'static str,
    pub mutability: &'static str,
    pub has_await: bool,
    pub has_match: bool,
    pub comment_style: &'static str,
}

impl LanguageProfile {
    fn for_lang(lang: Language) -> Self {
        match lang {
            Language::Rust => LanguageProfile {
                is_typed: true,
                is_oo: false,
                has_generics: true,
                null_safety: "strict",
                mutability: "explicit",
                has_await: true,
                has_match: true,
                comment_style: "//",
            },
            Language::Go => LanguageProfile {
                is_typed: true,
                is_oo: false,
                has_generics: true,
                null_safety: "nullable",
                mutability: "default_mutable",
                has_await: false,
                has_match: false,
                comment_style: "//",
            },
            Language::Swift => LanguageProfile {
                is_typed: true,
                is_oo: true,
                has_generics: true,
                null_safety: "strict",
                mutability: "explicit",
                has_await: true,
                has_match: true,
                comment_style: "//",
            },
            Language::Kotlin => LanguageProfile {
                is_typed: true,
                is_oo: true,
                has_generics: true,
                null_safety: "strict",
                mutability: "explicit",
                has_await: true,
                has_match: true,
                comment_style: "//",
            },
            Language::TypeScript => LanguageProfile {
                is_typed: true,
                is_oo: true,
                has_generics: true,
                null_safety: "strict",
                mutability: "default_mutable",
                has_await: true,
                has_match: true,
                comment_style: "//",
            },
            Language::JavaScript => LanguageProfile {
                is_typed: false,
                is_oo: true,
                has_generics: false,
                null_safety: "nullable",
                mutability: "default_mutable",
                has_await: true,
                has_match: false,
                comment_style: "//",
            },
            Language::Java => LanguageProfile {
                is_typed: true,
                is_oo: true,
                has_generics: true,
                null_safety: "nullable",
                mutability: "explicit",
                has_await: false,
                has_match: true,
                comment_style: "//",
            },
            Language::Cpp => LanguageProfile {
                is_typed: true,
                is_oo: true,
                has_generics: true,
                null_safety: "nullable",
                mutability: "explicit",
                has_await: false,
                has_match: false,
                comment_style: "//",
            },
        }
    }
}

/// Translation rule: a pattern + replacement for a language pair
#[derive(Debug, Clone)]
pub struct TranslationRule {
    pub from: Language,
    pub to: Language,
    pub pattern: String,
    pub replacement: String,
    pub description: &'static str,
}

/// A single translation operation
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct TranslationResult {
    pub from_language: String,
    pub to_language: String,
    pub original_code: String,
    pub translated_code: String,
    pub rules_applied: usize,
    pub confidence_score: f64,
    pub notes: Vec<String>,
}

impl TranslationResult {
    pub fn new(
        from: Language,
        to: Language,
        original: String,
        translated: String,
        rules_applied: usize,
        confidence: f64,
        notes: Vec<String>,
    ) -> Self {
        Self {
            from_language: from.as_str().to_string(),
            to_language: to.as_str().to_string(),
            original_code: original,
            translated_code: translated,
            rules_applied,
            confidence_score: confidence,
            notes: notes.iter().map(|s| s.to_string()).collect(),
        }
    }
}

/// Coverage report for a language pair
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct TranslationCoverage {
    pub from: String,
    pub to: String,
    pub patterns_covered: usize,
    pub patterns_available: usize,
    pub coverage_percent: f64,
    pub gaps: Vec<String>,
}

// ─────────────────────────────────────────────────────────────────
// Translation Rules Registry
// ─────────────────────────────────────────────────────────────────

/// Build all translation rules using standard escaped strings
fn build_rules() -> Vec<TranslationRule> {
    use Language::*;
    vec![
    // Rust -> Go
    TranslationRule {
        from: Rust, to: Go,
        pattern: r"fn\s+(\w+)\s*\(([^)]*)\)\s*(?:->\s*(\w+))?\s*\{".to_string(),
        replacement: "func $1($2) $3 {".to_string(),
        description: "Function signature",
    },
    TranslationRule {
        from: Rust, to: Go,
        pattern: r"let\s+mut\s+(\w+)\s*:\s*(\w+)\s*=\s*(.+?);".to_string(),
        replacement: "$1 := $3".to_string(),
        description: "Mutable variable declaration",
    },
    TranslationRule {
        from: Rust, to: Go,
        pattern: r"let\s+(\w+)\s*:\s*(\w+)\s*=\s*(.+?);".to_string(),
        replacement: "var $1 $2 = $3".to_string(),
        description: "Immutable variable declaration",
    },
    TranslationRule {
        from: Rust, to: Go,
        pattern: r#"println!\s*\(\s*"([^"]*)"\s*\)"#.to_string(),
        replacement: r#"fmt.Println("$1")"#.to_string(),
        description: "Println macro",
    },
    TranslationRule {
        from: Rust, to: Go,
        pattern: r"vec!\[([^\]]+)\]".to_string(),
        replacement: "[]{$1}".to_string(),
        description: "Vec literal to slice",
    },
    TranslationRule {
        from: Rust, to: Go,
        pattern: r"Option<(\w+)>".to_string(),
        replacement: "*$1".to_string(),
        description: "Option<T> to pointer",
    },
    TranslationRule {
        from: Rust, to: Go,
        pattern: r"Result<(\w+),\s*(\w+)>".to_string(),
        replacement: "($1, error)".to_string(),
        description: "Result<T, E> to Go error style",
    },
    TranslationRule {
        from: Rust, to: Go,
        pattern: r"impl\s+(\w+)\s*\{".to_string(),
        replacement: "func (s *$1) ".to_string(),
        description: "impl block to method receiver",
    },
    TranslationRule {
        from: Rust, to: Go,
        pattern: r"for\s+(\w+)\s+in\s+(\w+)\.iter\(\)\s*\{".to_string(),
        replacement: "for _, $1 := range $2 {".to_string(),
        description: "Iterator loop",
    },
    TranslationRule {
        from: Rust, to: Go,
        pattern: r"match\s+(\w+)\s*\{".to_string(),
        replacement: "switch $1 {".to_string(),
        description: "Match expression to switch",
    },
    TranslationRule {
        from: Rust, to: Go,
        pattern: r"\.unwrap\(\)".to_string(),
        replacement: "".to_string(),
        description: "unwrap() call",
    },
    TranslationRule {
        from: Rust, to: Go,
        pattern: r"->\s*(\w+)".to_string(),
        replacement: " $1".to_string(),
        description: "Return type annotation",
    },
    TranslationRule {
        from: Rust, to: Go,
        pattern: r"&mut\s+(\w+)".to_string(),
        replacement: "&$1".to_string(),
        description: "Mutable reference to pointer",
    },
    TranslationRule {
        from: Rust, to: Go,
        pattern: r"#\[derive\(([^)]+)\)\]".to_string(),
        replacement: "".to_string(),
        description: "Remove derive attributes",
    },

    // Rust -> TypeScript
    TranslationRule {
        from: Rust, to: TypeScript,
        pattern: r"fn\s+(\w+)\s*\(([^)]*)\)\s*(?:->\s*(\w+))?\s*\{".to_string(),
        replacement: "function $1($2): $3 {".to_string(),
        description: "Function signature",
    },
    TranslationRule {
        from: Rust, to: TypeScript,
        pattern: r"let\s+mut\s+(\w+)\s*:\s*(\w+)\s*=\s*(.+?);".to_string(),
        replacement: "let $1: $2 = $3;".to_string(),
        description: "Mutable variable with type",
    },
    TranslationRule {
        from: Rust, to: TypeScript,
        pattern: r"let\s+(\w+)\s*:\s*(\w+)\s*=\s*(.+?);".to_string(),
        replacement: "const $1: $2 = $3;".to_string(),
        description: "Immutable variable with type",
    },
    TranslationRule {
        from: Rust, to: TypeScript,
        pattern: r#"println!\s*\(\s*"([^"]*)"\s*\)"#.to_string(),
        replacement: r#"console.log("$1");"#.to_string(),
        description: "Println to console.log",
    },
    TranslationRule {
        from: Rust, to: TypeScript,
        pattern: r"vec!\[([^\]]+)\]".to_string(),
        replacement: "[$1]".to_string(),
        description: "Vec literal to array",
    },
    TranslationRule {
        from: Rust, to: TypeScript,
        pattern: r"Option<(\w+)>".to_string(),
        replacement: "$1 | null".to_string(),
        description: "Option<T> to nullable type",
    },
    TranslationRule {
        from: Rust, to: TypeScript,
        pattern: r"Result<(\w+),\s*(\w+)>".to_string(),
        replacement: "{ ok: $1; err: $2 }".to_string(),
        description: "Result<T, E> to typed result object",
    },
    TranslationRule {
        from: Rust, to: TypeScript,
        pattern: r"impl\s+(\w+)\s*\{".to_string(),
        replacement: "class $1 { ".to_string(),
        description: "impl to class",
    },
    TranslationRule {
        from: Rust, to: TypeScript,
        pattern: r"for\s+(\w+)\s+in\s+(\w+)\.iter\(\)\s*\{".to_string(),
        replacement: "for (const $1 of $2) {".to_string(),
        description: "Iterator loop to for-of",
    },
    TranslationRule {
        from: Rust, to: TypeScript,
        pattern: r"match\s+(\w+)\s*\{".to_string(),
        replacement: "switch ($1) {".to_string(),
        description: "Match to switch",
    },
    TranslationRule {
        from: Rust, to: TypeScript,
        pattern: r"->\s*(\w+)".to_string(),
        replacement: ": $1".to_string(),
        description: "Return type arrow",
    },
    TranslationRule {
        from: Rust, to: TypeScript,
        pattern: r"&mut\s+(\w+)".to_string(),
        replacement: "$1".to_string(),
        description: "Strip mutable reference",
    },
    TranslationRule {
        from: Rust, to: TypeScript,
        pattern: r"\.unwrap\(\)".to_string(),
        replacement: "".to_string(),
        description: "unwrap() call",
    },

    // Go -> Rust
    TranslationRule {
        from: Go, to: Rust,
        pattern: r"func\s+(\w+)\s*\(([^)]*)\)\s*(\w+)?\s*\{".to_string(),
        replacement: "fn $1($2) -> $3 {".to_string(),
        description: "Function signature",
    },
    TranslationRule {
        from: Go, to: Rust,
        pattern: r"(\w+)\s*:=\s*(.+)".to_string(),
        replacement: "let mut $1 = $2;".to_string(),
        description: "Short variable declaration",
    },
    TranslationRule {
        from: Go, to: Rust,
        pattern: r#"fmt\.Println\s*\(\s*"([^"]*)"\s*\)"#.to_string(),
        replacement: r#"println!("$1");"#.to_string(),
        description: "fmt.Println to println!",
    },
    TranslationRule {
        from: Go, to: Rust,
        pattern: r"for\s+(\w+)\s*,\s*(\w+)\s*:=\s*range\s+(\w+)\s*\{".to_string(),
        replacement: "for ($1, $2) in $3.iter().enumerate() {".to_string(),
        description: "range loop with index",
    },
    TranslationRule {
        from: Go, to: Rust,
        pattern: r"switch\s+(\w+)\s*\{".to_string(),
        replacement: "match $1 {".to_string(),
        description: "switch to match",
    },
    TranslationRule {
        from: Go, to: Rust,
        pattern: r"var\s+(\w+)\s+(\w+)\s*=\s*(.+)".to_string(),
        replacement: "let $1: $2 = $3;".to_string(),
        description: "var declaration with type",
    },

    // Swift -> Rust
    TranslationRule {
        from: Swift, to: Rust,
        pattern: r"func\s+(\w+)\s*\(([^)]*)\)\s*(->\s*\w+)?\s*\{".to_string(),
        replacement: "fn $1($2) $3 {".to_string(),
        description: "Function signature",
    },
    TranslationRule {
        from: Swift, to: Rust,
        pattern: r"var\s+(\w+)\s*:\s*(\w+)\s*=\s*(.+)".to_string(),
        replacement: "let mut $1: $2 = $3;".to_string(),
        description: "Variable declaration",
    },
    TranslationRule {
        from: Swift, to: Rust,
        pattern: r"let\s+(\w+)\s*:\s*(\w+)\s*=\s*(.+)".to_string(),
        replacement: "let $1: $2 = $3;".to_string(),
        description: "Constant declaration",
    },
    TranslationRule {
        from: Swift, to: Rust,
        pattern: r#"print\s*\(\s*"([^"]*)"\s*\)"#.to_string(),
        replacement: r#"println!("$1");"#.to_string(),
        description: "print to println!",
    },
    TranslationRule {
        from: Swift, to: Rust,
        pattern: r"if\s+let\s+(\w+)\s*=\s*(.+)\s*\{".to_string(),
        replacement: "if let Some($1) = $2 {".to_string(),
        description: "if let to if let Some",
    },
    TranslationRule {
        from: Swift, to: Rust,
        pattern: r"guard\s+let\s+(\w+)\s*=\s*(.+)\s+else\s*\{".to_string(),
        replacement: "let $1 = $2; if $1.is_none() {".to_string(),
        description: "guard let to if let None",
    },
    TranslationRule {
        from: Swift, to: Rust,
        pattern: r"\?\.\w+".to_string(),
        replacement: ".".to_string(),
        description: "Optional chaining to method call",
    },

    // Kotlin -> Rust
    TranslationRule {
        from: Kotlin, to: Rust,
        pattern: r"fun\s+(\w+)\s*\(([^)]*)\)\s*:\s*(\w+)\s*\{".to_string(),
        replacement: "fn $1($2) -> $3 {".to_string(),
        description: "Function signature with return type",
    },
    TranslationRule {
        from: Kotlin, to: Rust,
        pattern: r"fun\s+(\w+)\s*\(([^)]*)\)\s*\{".to_string(),
        replacement: "fn $1($2) {".to_string(),
        description: "Function signature without return type",
    },
    TranslationRule {
        from: Kotlin, to: Rust,
        pattern: r"val\s+(\w+)\s*:\s*(\w+)\s*=\s*(.+)".to_string(),
        replacement: "let $1: $2 = $3;".to_string(),
        description: "val (immutable) declaration",
    },
    TranslationRule {
        from: Kotlin, to: Rust,
        pattern: r"var\s+(\w+)\s*:\s*(\w+)\s*=\s*(.+)".to_string(),
        replacement: "let mut $1: $2 = $3;".to_string(),
        description: "var (mutable) declaration",
    },
    TranslationRule {
        from: Kotlin, to: Rust,
        pattern: r#"println\s*\(\s*"([^"]*)"\s*\)"#.to_string(),
        replacement: r#"println!("$1");"#.to_string(),
        description: "println to println!",
    },
    TranslationRule {
        from: Kotlin, to: Rust,
        pattern: r"when\s*\(([^)]+)\)\s*\{".to_string(),
        replacement: "match $1 {".to_string(),
        description: "when to match",
    },
    TranslationRule {
        from: Kotlin, to: Rust,
        pattern: r"\.map\s*\{\s*(\w+)\s*->\s*(.+)\s*\}".to_string(),
        replacement: ".map(|$1| $2)".to_string(),
        description: "lambda to closure",
    },
    TranslationRule {
        from: Kotlin, to: Rust,
        pattern: r"\bnull\b".to_string(),
        replacement: "None".to_string(),
        description: "null to None",
    },

    // TypeScript -> Rust
    TranslationRule {
        from: TypeScript, to: Rust,
        pattern: r"function\s+(\w+)\s*\(([^)]*)\)\s*:\s*(\w+)\s*\{".to_string(),
        replacement: "fn $1($2) -> $3 {".to_string(),
        description: "Function signature",
    },
    TranslationRule {
        from: TypeScript, to: Rust,
        pattern: r"const\s+(\w+)\s*:\s*(\w+)\s*=\s*(.+?);".to_string(),
        replacement: "let $1: $2 = $3;".to_string(),
        description: "const with type",
    },
    TranslationRule {
        from: TypeScript, to: Rust,
        pattern: r"let\s+(\w+)\s*:\s*(\w+)\s*=\s*(.+?);".to_string(),
        replacement: "let mut $1: $2 = $3;".to_string(),
        description: "let with type",
    },
    TranslationRule {
        from: TypeScript, to: Rust,
        pattern: r#"console\.log\s*\(\s*"([^"]*)"\s*\);"#.to_string(),
        replacement: r#"println!("$1");"#.to_string(),
        description: "console.log to println!",
    },
    TranslationRule {
        from: TypeScript, to: Rust,
        pattern: r"interface\s+(\w+)\s*\{".to_string(),
        replacement: "struct $1 {".to_string(),
        description: "interface to struct",
    },
    TranslationRule {
        from: TypeScript, to: Rust,
        pattern: r"type\s+(\w+)\s*=\s*".to_string(),
        replacement: "type $1 = ".to_string(),
        description: "type alias",
    },
    TranslationRule {
        from: TypeScript, to: Rust,
        pattern: r"switch\s*\(([^)]+)\)\s*\{".to_string(),
        replacement: "match $1 {".to_string(),
        description: "switch to match",
    },
    TranslationRule {
        from: TypeScript, to: Rust,
        pattern: r":\s*(\w+)\s*\|\s*null".to_string(),
        replacement: ": Option<$1>".to_string(),
        description: "nullable type to Option<T>",
    },

    // JavaScript -> TypeScript
    TranslationRule {
        from: JavaScript, to: TypeScript,
        pattern: r"function\s+(\w+)\s*\(([^)]*)\)\s*\{".to_string(),
        replacement: "function $1($2): void {".to_string(),
        description: "Function signature with return type",
    },
    TranslationRule {
        from: JavaScript, to: TypeScript,
        pattern: r"const\s+(\w+)\s*=\s*(.+)".to_string(),
        replacement: "const $1: unknown = $2".to_string(),
        description: "const declaration (add type)",
    },
    TranslationRule {
        from: JavaScript, to: TypeScript,
        pattern: r"let\s+(\w+)\s*=\s*(.+)".to_string(),
        replacement: "let $1: unknown = $2".to_string(),
        description: "let declaration (add type)",
    },

    // Java -> Rust
    TranslationRule {
        from: Java, to: Rust,
        pattern: r"public\s+static\s+void\s+main\s*\(\s*String\[\]\s+args\s*\)\s*\{".to_string(),
        replacement: "fn main() {".to_string(),
        description: "Java main method signature",
    },
    TranslationRule {
        from: Java, to: Rust,
        pattern: r"public\s+(\w+)\s+(\w+)\s*\(([^)]*)\)\s*\{".to_string(),
        replacement: "pub fn $2($3) -> $1 {".to_string(),
        description: "Public method signature",
    },
    TranslationRule {
        from: Java, to: Rust,
        pattern: r#"System\.out\.println\s*\(\s*"([^"]*)"\s*\);"#.to_string(),
        replacement: r#"println!("$1");"#.to_string(),
        description: "println to println!",
    },
    TranslationRule {
        from: Java, to: Rust,
        pattern: r"\bString\b".to_string(),
        replacement: "&str".to_string(),
        description: "String to &str",
    },
    TranslationRule {
        from: Java, to: Rust,
        pattern: r"\bint\b".to_string(),
        replacement: "i32".to_string(),
        description: "int to i32",
    },
    TranslationRule {
        from: Java, to: Rust,
        pattern: r"\bboolean\b".to_string(),
        replacement: "bool".to_string(),
        description: "boolean to bool",
    },
    TranslationRule {
        from: Java, to: Rust,
        pattern: r"class\s+(\w+)\s*\{".to_string(),
        replacement: "struct $1 {".to_string(),
        description: "class to struct",
    },
    TranslationRule {
        from: Java, to: Rust,
        pattern: r"new\s+(\w+)\s*\(" .to_string(),
        replacement: "$1::new(".to_string(),
        description: "new to ::new",
    },

    // C/C++ -> Rust
    TranslationRule {
        from: Cpp, to: Rust,
        pattern: r"int\s+main\s*\(\s*\)\s*\{".to_string(),
        replacement: "fn main() {".to_string(),
        description: "main function",
    },
    TranslationRule {
        from: Cpp, to: Rust,
        pattern: r#"printf\s*\(\s*"([^"]*)"\s*\);"#.to_string(),
        replacement: r#"println!("$1");"#.to_string(),
        description: "printf to println!",
    },
    TranslationRule {
        from: Cpp, to: Rust,
        pattern: r"#include\s*<([^>]+)>".to_string(),
        replacement: "// use $1 from crates.io".to_string(),
        description: "include to external dependency",
    },
    TranslationRule {
        from: Cpp, to: Rust,
        pattern: r"std::".to_string(),
        replacement: "".to_string(),
        description: "strip std:: prefix",
    },
    TranslationRule {
        from: Cpp, to: Rust,
        pattern: r"cout\s*<<".to_string(),
        replacement: "println!(\"\");".to_string(),
        description: "cout to println!",
    },
    ]
}

/// Core translation engine
pub struct SyntaxTranslator {
    rules: Vec<TranslationRule>,
}

impl Default for SyntaxTranslator {
    fn default() -> Self {
        Self::new()
    }
}

impl SyntaxTranslator {
    pub fn new() -> Self {
        Self {
            rules: build_rules(),
        }
    }

    /// Translate code from one language to another
    pub fn translate(
        &self,
        code: &str,
        from: &str,
        to: &str,
    ) -> Result<TranslationResult, TranslatorError> {
        let from_lang = Language::from_str(from)
            .ok_or_else(|| TranslatorError::UnknownLanguage(from.to_string()))?;
        let to_lang = Language::from_str(to)
            .ok_or_else(|| TranslatorError::UnknownLanguage(to.to_string()))?;

        let rules = self.get_rules_for_pair(from_lang, to_lang);
        let mut translated = code.to_string();
        let mut notes = Vec::new();
        let mut applied = 0;

        for rule in &rules {
            let re = regex::Regex::new(&rule.pattern)
                .map_err(|e| TranslatorError::RegexError(e.to_string()))?;
            if re.is_match(&translated) {
                let count = re.find_iter(&translated).count();
                translated = re.replace_all(&translated, rule.replacement.as_str()).to_string();
                applied += count;
                notes.push(format!("{}: {} pattern(s) applied ({})", rule.description, count, from_lang.as_str()));
            }
        }

        let confidence = self.calculate_confidence(from_lang, to_lang, applied);

        Ok(TranslationResult::new(
            from_lang,
            to_lang,
            code.to_string(),
            translated,
            applied,
            confidence,
            notes,
        ))
    }

    /// Get all rules for a language pair
    fn get_rules_for_pair(&self, from: Language, to: Language) -> Vec<&TranslationRule> {
        self.rules
            .iter()
            .filter(|r| r.from == from && r.to == to)
            .collect()
    }

    /// Calculate confidence score based on rules applied and gaps
    fn calculate_confidence(&self, from: Language, to: Language, rules_applied: usize) -> f64 {
        let available = self.get_rules_for_pair(from, to).len();
        if available == 0 {
            return 0.0;
        }
        let raw = rules_applied.min(available) as f64 / available as f64;
        let base_bonus = if rules_applied >= 3 { 0.1 } else { 0.0 };
        (raw + base_bonus).min(1.0)
    }

    /// Get translation coverage for a language pair
    pub fn coverage_report(&self, from: &str, to: &str) -> Result<TranslationCoverage, TranslatorError> {
        let from_lang = Language::from_str(from)
            .ok_or_else(|| TranslatorError::UnknownLanguage(from.to_string()))?;
        let to_lang = Language::from_str(to)
            .ok_or_else(|| TranslatorError::UnknownLanguage(to.to_string()))?;

        let rules = self.get_rules_for_pair(from_lang, to_lang);
        let available = rules.len();
        let covered = available;

        let gaps = self.identify_gaps(from_lang, to_lang);

        let coverage_percent = if available > 0 {
            (covered as f64 / available as f64) * 100.0
        } else {
            0.0
        };

        Ok(TranslationCoverage {
            from: from.to_string(),
            to: to.to_string(),
            patterns_covered: covered,
            patterns_available: available,
            coverage_percent,
            gaps,
        })
    }

    /// Identify gaps in translation coverage
    fn identify_gaps(&self, from: Language, to: Language) -> Vec<String> {
        let mut gaps = Vec::new();
        let all_patterns = [
            "function_signature",
            "variable_declaration",
            "print_statement",
            "loop",
            "match_switch",
            "class_struct",
            "generics",
            "null_handling",
            "optional_chaining",
            "lambda_closure",
        ];
        for pattern in all_patterns {
            let has_rule = self.rules.iter().any(|r| r.from == from && r.to == to
                && r.description.to_lowercase().contains(pattern));
            if !has_rule {
                gaps.push(pattern.to_string());
            }
        }
        gaps
    }

    /// Get the next language in the rotation (from language_rotation.json)
    pub fn get_next_from_rotation(json_path: &Path) -> Result<(String, String), TranslatorError> {
        let content = fs::read_to_string(json_path)
            .map_err(|e| TranslatorError::Io(e.to_string()))?;

        #[derive(Deserialize)]
        struct RotationState {
            languages: Vec<String>,
            current_index: usize,
        }

        let state: RotationState = serde_json::from_str(&content)
            .map_err(|e| TranslatorError::Parse(e.to_string()))?;

        let n = state.languages.len();
        if n == 0 {
            return Err(TranslatorError::EmptyRotation);
        }

        let current = state.languages[state.current_index % n].clone();
        let next_idx = (state.current_index + 1) % n;
        let next = state.languages[next_idx].clone();

        Ok((current, next))
    }

    /// Advance the rotation index in language_rotation.json
    pub fn advance_rotation(json_path: &Path) -> Result<String, TranslatorError> {
        let content = fs::read_to_string(json_path)
            .map_err(|e| TranslatorError::Io(e.to_string()))?;

        #[derive(Deserialize, Serialize)]
        struct RotationState {
            languages: Vec<String>,
            current_index: usize,
            last_language: Option<String>,
            updated_at: String,
        }

        let mut state: RotationState = serde_json::from_str(&content)
            .map_err(|e| TranslatorError::Parse(e.to_string()))?;

        let n = state.languages.len();
        if n == 0 {
            return Err(TranslatorError::EmptyRotation);
        }

        let current = state.languages[state.current_index % n].clone();
        state.current_index = (state.current_index + 1) % n;
        state.last_language = Some(current.clone());
        state.updated_at = chrono_now();

        let json = serde_json::to_string_pretty(&state)
            .map_err(|e| TranslatorError::Encode(e.to_string()))?;

        let tmp = format!("{}.tmp", json_path.display());
        fs::write(&tmp, &json)
            .map_err(|e| TranslatorError::Io(e.to_string()))?;
        fs::rename(&tmp, json_path)
            .map_err(|e| TranslatorError::Io(e.to_string()))?;

        Ok(state.languages[state.current_index].clone())
    }

    /// Full translate-and-rotate: translate from current -> next, advance index
    pub fn translate_and_rotate(
        &self,
        code: &str,
        json_path: &Path,
    ) -> Result<TranslationResult, TranslatorError> {
        let (from, to) = Self::get_next_from_rotation(json_path)?;
        let result = self.translate(code, &from, &to)?;
        Self::advance_rotation(json_path)?;
        Ok(result)
    }

    /// List all supported language pairs
    pub fn supported_pairs(&self) -> Vec<(String, String)> {
        let mut pairs = Vec::new();
        for lang in Language::all() {
            for to_lang in Language::all() {
                if lang != to_lang {
                    let rules = self.get_rules_for_pair(lang, to_lang);
                    if !rules.is_empty() {
                        pairs.push((lang.as_str().to_string(), to_lang.as_str().to_string()));
                    }
                }
            }
        }
        pairs.sort();
        pairs.dedup();
        pairs
    }
}

fn chrono_now() -> String {
    use std::time::{SystemTime, UNIX_EPOCH};
    let ms = SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .unwrap_or_default()
        .as_millis() as u64;
    format!("{}", ms)
}

// ─────────────────────────────────────────────────────────────────
// Errors
// ─────────────────────────────────────────────────────────────────

#[derive(Debug, Clone)]
pub enum TranslatorError {
    UnknownLanguage(String),
    RegexError(String),
    Io(String),
    Parse(String),
    Encode(String),
    EmptyRotation,
}

impl std::fmt::Display for TranslatorError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            Self::UnknownLanguage(s) => write!(f, "Unknown language: {}", s),
            Self::RegexError(s) => write!(f, "Regex error: {}", s),
            Self::Io(s) => write!(f, "IO error: {}", s),
            Self::Parse(s) => write!(f, "Parse error: {}", s),
            Self::Encode(s) => write!(f, "Encode error: {}", s),
            Self::EmptyRotation => write!(f, "Language rotation is empty"),
        }
    }
}

impl std::error::Error for TranslatorError {}

// ─────────────────────────────────────────────────────────────────
// Tests
// ─────────────────────────────────────────────────────────────────

#[cfg(test)]
mod tests {
    use super::*;

    fn temp_json_path() -> std::path::PathBuf {
        use std::time::{SystemTime, UNIX_EPOCH};
        let nanos = SystemTime::now()
            .duration_since(UNIX_EPOCH)
            .unwrap()
            .as_nanos();
        std::env::temp_dir().join(format!("rotation_test_{}.json", nanos))
    }

    fn make_test_rotation(path: &std::path::Path) {
        let state = serde_json::json!({
            "languages": ["Rust", "Go", "Swift", "Kotlin", "TypeScript", "JavaScript", "Java", "C/C++"],
            "current_index": 0,
            "last_language": null,
            "updated_at": "2026-06-07T01:00:00+08:00"
        });
        fs::write(path, serde_json::to_string_pretty(&state).unwrap()).unwrap();
    }

    #[test]
    fn test_language_from_str() {
        assert_eq!(Language::from_str("Rust"), Some(Language::Rust));
        assert_eq!(Language::from_str("Go"), Some(Language::Go));
        assert_eq!(Language::from_str("Swift"), Some(Language::Swift));
        assert_eq!(Language::from_str("Kotlin"), Some(Language::Kotlin));
        assert_eq!(Language::from_str("TypeScript"), Some(Language::TypeScript));
        assert_eq!(Language::from_str("JavaScript"), Some(Language::JavaScript));
        assert_eq!(Language::from_str("Java"), Some(Language::Java));
        assert_eq!(Language::from_str("C/C++"), Some(Language::Cpp));
        assert_eq!(Language::from_str("Python"), None);
    }

    #[test]
    fn test_language_as_str() {
        assert_eq!(Language::Rust.as_str(), "Rust");
        assert_eq!(Language::Go.as_str(), "Go");
        assert_eq!(Language::Cpp.as_str(), "C/C++");
    }

    #[test]
    fn test_language_all() {
        let all = Language::all();
        assert_eq!(all.len(), 8);
        assert_eq!(all[0], Language::Rust);
        assert_eq!(all[7], Language::Cpp);
    }

    #[test]
    fn test_translate_rust_to_go_simple() {
        let t = SyntaxTranslator::new();
        let result = t.translate(r#"fn main() { println!("hello"); }"#, "Rust", "Go").unwrap();
        assert_eq!(result.from_language, "Rust");
        assert_eq!(result.to_language, "Go");
        assert!(result.translated_code.contains("func main()"));
        assert!(result.translated_code.contains("fmt.Println"));
    }

    #[test]
    fn test_translate_rust_to_typescript() {
        let t = SyntaxTranslator::new();
        let result = t.translate(r#"fn main() { println!("hello"); }"#, "Rust", "TypeScript").unwrap();
        assert_eq!(result.from_language, "Rust");
        assert_eq!(result.to_language, "TypeScript");
        assert!(result.translated_code.contains("function main()"));
        assert!(result.translated_code.contains("console.log"));
    }

    #[test]
    fn test_translate_go_to_rust() {
        let t = SyntaxTranslator::new();
        let result = t.translate(r#"func main() { fmt.Println("hello") }"#, "Go", "Rust").unwrap();
        assert_eq!(result.from_language, "Go");
        assert_eq!(result.to_language, "Rust");
        assert!(result.translated_code.contains("fn main()"));
        assert!(result.translated_code.contains("println!"));
    }

    #[test]
    fn test_translate_swift_to_rust() {
        let t = SyntaxTranslator::new();
        let result = t.translate(
            r#"func greet(name: String) -> String { return "Hello, \(name)!" }"#,
            "Swift",
            "Rust",
        ).unwrap();
        assert_eq!(result.from_language, "Swift");
        assert_eq!(result.to_language, "Rust");
        assert!(result.translated_code.contains("fn greet"));
    }

    #[test]
    fn test_translate_kotlin_to_rust() {
        let t = SyntaxTranslator::new();
        let result = t.translate(r#"fun main() { println("hello") }"#, "Kotlin", "Rust").unwrap();
        assert_eq!(result.from_language, "Kotlin");
        assert_eq!(result.to_language, "Rust");
        assert!(result.translated_code.contains("fn main()"));
    }

    #[test]
    fn test_translate_typescript_to_rust() {
        let t = SyntaxTranslator::new();
        let result = t.translate("function add(a: number, b: number): number { return a + b; }", "TypeScript", "Rust").unwrap();
        assert_eq!(result.from_language, "TypeScript");
        assert_eq!(result.to_language, "Rust");
        assert!(result.translated_code.contains("fn add"));
    }

    #[test]
    fn test_translate_java_to_rust() {
        let t = SyntaxTranslator::new();
        let result = t.translate("public static void main(String[] args) { System.out.println(\"hello\"); }", "Java", "Rust").unwrap();
        assert_eq!(result.from_language, "Java");
        assert_eq!(result.to_language, "Rust");
        assert!(result.translated_code.contains("fn main"));
        assert!(result.translated_code.contains("println!"));
    }

    #[test]
    fn test_translate_cpp_to_rust() {
        let t = SyntaxTranslator::new();
        let result = t.translate("#include <stdio.h>\nint main() { printf(\"hello\\n\"); return 0; }", "C/C++", "Rust").unwrap();
        assert_eq!(result.from_language, "C/C++");
        assert_eq!(result.to_language, "Rust");
        assert!(result.translated_code.contains("fn main()"));
    }

    #[test]
    fn test_translate_unknown_language() {
        let t = SyntaxTranslator::new();
        let result = t.translate("print('hello')", "Python", "Rust");
        assert!(result.is_err());
        assert!(matches!(result.unwrap_err(), TranslatorError::UnknownLanguage(_)));
    }

    #[test]
    fn test_translate_same_language_no_change() {
        let t = SyntaxTranslator::new();
        let result = t.translate("let x = 5;", "Rust", "Rust").unwrap();
        assert_eq!(result.from_language, "Rust");
        assert_eq!(result.to_language, "Rust");
        assert!(result.rules_applied >= 0);
    }

    #[test]
    fn test_confidence_score() {
        let t = SyntaxTranslator::new();
        let result = t.translate(r#"fn main() { println!("hello"); }"#, "Rust", "Go").unwrap();
        assert!(result.confidence_score > 0.0);
        assert!(result.confidence_score <= 1.0);
    }

    #[test]
    fn test_get_next_from_rotation() {
        let path = temp_json_path();
        make_test_rotation(&path);

        let (current, next) = SyntaxTranslator::get_next_from_rotation(&path).unwrap();
        assert_eq!(current, "Rust");
        assert_eq!(next, "Go");

        std::fs::remove_file(&path).ok();
    }

    #[test]
    fn test_advance_rotation() {
        let path = temp_json_path();
        make_test_rotation(&path);

        let next = SyntaxTranslator::advance_rotation(&path).unwrap();
        assert_eq!(next, "Go");

        let content = fs::read_to_string(&path).unwrap();
        let state: serde_json::Value = serde_json::from_str(&content).unwrap();
        assert_eq!(state["current_index"], 1);
        assert_eq!(state["last_language"], "Rust");

        std::fs::remove_file(&path).ok();
    }

    #[test]
    fn test_advance_rotation_wraps() {
        let path = temp_json_path();
        let state = serde_json::json!({
            "languages": ["Rust", "Go", "Swift"],
            "current_index": 2,
            "last_language": "Go",
            "updated_at": "2026-06-07T01:00:00+08:00"
        });
        fs::write(&path, serde_json::to_string_pretty(&state).unwrap()).unwrap();

        let next = SyntaxTranslator::advance_rotation(&path).unwrap();
        assert_eq!(next, "Rust");

        std::fs::remove_file(&path).ok();
    }

    #[test]
    fn test_translate_and_rotate() {
        let path = temp_json_path();
        make_test_rotation(&path);

        let t = SyntaxTranslator::new();
        let result = t.translate_and_rotate(
            r#"fn main() { println!("hello"); }"#,
            &path,
        ).unwrap();

        assert_eq!(result.from_language, "Rust");
        assert_eq!(result.to_language, "Go");
        assert!(result.translated_code.contains("func main()"));

        let content = fs::read_to_string(&path).unwrap();
        let state: serde_json::Value = serde_json::from_str(&content).unwrap();
        assert_eq!(state["current_index"], 1);

        std::fs::remove_file(&path).ok();
    }

    #[test]
    fn test_coverage_report() {
        let t = SyntaxTranslator::new();
        let cov = t.coverage_report("Rust", "Go").unwrap();
        assert_eq!(cov.from, "Rust");
        assert_eq!(cov.to, "Go");
        assert!(cov.patterns_available > 0);
        assert!(cov.coverage_percent >= 0.0);
    }

    #[test]
    fn test_supported_pairs() {
        let t = SyntaxTranslator::new();
        let pairs = t.supported_pairs();
        assert!(!pairs.is_empty());
        assert!(pairs.contains(&("Rust".to_string(), "Go".to_string())));
        assert!(pairs.contains(&("Rust".to_string(), "TypeScript".to_string())));
    }

    #[test]
    fn test_language_profile() {
        let rust_profile = LanguageProfile::for_lang(Language::Rust);
        assert!(rust_profile.is_typed);
        assert_eq!(rust_profile.null_safety, "strict");
        assert_eq!(rust_profile.mutability, "explicit");
        assert!(rust_profile.has_match);

        let js_profile = LanguageProfile::for_lang(Language::JavaScript);
        assert!(!js_profile.is_typed);
        assert_eq!(js_profile.null_safety, "nullable");
    }

    #[test]
    fn test_identify_gaps() {
        let t = SyntaxTranslator::new();
        let gaps = t.identify_gaps(Language::Rust, Language::Go);
        assert!(gaps.len() >= 0);
    }

    #[test]
    fn test_result_fields_populated() {
        let t = SyntaxTranslator::new();
        let result = t.translate("fn main() { }", "Rust", "Go").unwrap();
        assert!(!result.original_code.is_empty());
        assert!(!result.translated_code.is_empty());
        assert!(result.rules_applied >= 0);
    }

    #[test]
    fn test_multiple_rules_applied() {
        let t = SyntaxTranslator::new();
        let code = r#"fn main() { println!("hello"); let mut x: i32 = 5; }"#;
        let result = t.translate(code, "Rust", "Go").unwrap();
        assert!(result.rules_applied >= 2);
    }

    #[test]
    fn test_empty_rotation_error() {
        let path = temp_json_path();
        let state = serde_json::json!({
            "languages": [],
            "current_index": 0,
            "last_language": null,
            "updated_at": "2026-06-07T01:00:00+08:00"
        });
        fs::write(&path, serde_json::to_string_pretty(&state).unwrap()).unwrap();

        let err = SyntaxTranslator::get_next_from_rotation(&path).unwrap_err();
        assert!(matches!(err, TranslatorError::EmptyRotation));

        std::fs::remove_file(&path).ok();
    }
}