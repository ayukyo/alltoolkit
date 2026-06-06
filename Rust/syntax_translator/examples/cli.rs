//! CLI tool for syntax_translator
//!
//! Usage:
//!   cargo run --example cli <json_path> <code> <from_lang> <to_lang>
//!   cargo run --example cli <json_path> --status
//!   cargo run --example cli <json_path> --coverage <from_lang> <to_lang>

use syntax_translator::{SyntaxTranslator, Language};
use std::env;
use std::fs;

fn main() {
    let args: Vec<String> = env::args().collect();

    if args.len() < 2 {
        println!("Usage:");
        println!("  cargo run --example cli <json_path> <code> <from_lang> <to_lang>");
        println!("  cargo run --example cli <json_path> --status");
        println!("  cargo run --example cli <json_path> --coverage <from_lang> <to_lang>");
        println!("  cargo run --example cli <json_path> --rotate <code>");
        return;
    }

    let json_path = std::path::Path::new(&args[1]);
    let translator = SyntaxTranslator::new();

    if args.len() == 2 || (args.len() == 3 && args[2] == "--status") {
        // Show rotation status
        match SyntaxTranslator::get_next_from_rotation(json_path) {
            Ok((current, next)) => {
                println!("Current language: {}", current);
                println!("Next language:    {}", next);
                println!();
                println!("Supported language pairs:");
                for pair in translator.supported_pairs() {
                    println!("  {} -> {}", pair.0, pair.1);
                }
            }
            Err(e) => {
                eprintln!("Error: {}", e);
                std::process::exit(1);
            }
        }
    } else if args.len() >= 4 && args[2] == "--coverage" {
        let from = &args[3];
        let to = if args.len() > 4 { &args[4] } else { "" };
        match translator.coverage_report(from, to) {
            Ok(cov) => {
                println!("Coverage: {} -> {}", cov.from, cov.to);
                println!("  Patterns: {}/{}", cov.patterns_covered, cov.patterns_available);
                println!("  {:.0}% coverage", cov.coverage_percent);
                if !cov.gaps.is_empty() {
                    println!("  Gaps: {}", cov.gaps.join(", "));
                }
            }
            Err(e) => {
                eprintln!("Error: {}", e);
                std::process::exit(1);
            }
        }
    } else if args.len() >= 4 && args[2] == "--rotate" {
        let code = &args[3];
        match translator.translate_and_rotate(code, json_path) {
            Ok(result) => {
                println!("Translation: {} -> {}", result.from_language, result.to_language);
                println!("Confidence: {:.0}%", result.confidence_score * 100.0);
                println!("Rules applied: {}", result.rules_applied);
                println!();
                println!("{}", result.translated_code);
                println!();
                println!("Updated language_rotation.json (index advanced)");
            }
            Err(e) => {
                eprintln!("Error: {}", e);
                std::process::exit(1);
            }
        }
    } else if args.len() >= 5 {
        let code = &args[2];
        let from = &args[3];
        let to = &args[4];
        match translator.translate(code, from, to) {
            Ok(result) => {
                println!("Translation: {} -> {}", result.from_language, result.to_language);
                println!("Confidence: {:.0}%", result.confidence_score * 100.0);
                println!("Rules applied: {}", result.rules_applied);
                if !result.notes.is_empty() {
                    println!("Notes:");
                    for note in &result.notes {
                        println!("  - {}", note);
                    }
                }
                println!();
                println!("{}", result.translated_code);
            }
            Err(e) => {
                eprintln!("Error: {}", e);
                std::process::exit(1);
            }
        }
    } else {
        println!("Usage:");
        println!("  cargo run --example cli <json_path> <code> <from_lang> <to_lang>");
        println!("  cargo run --example cli <json_path> --status");
        println!("  cargo run --example cli <json_path> --coverage <from_lang> <to_lang>");
        println!("  cargo run --example cli <json_path> --rotate <code>");
    }
}