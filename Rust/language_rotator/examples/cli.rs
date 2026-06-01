//! Example: CLI tool using language_rotator

use language_rotator::{LanguageEntry, LanguageRotator};
use std::env;

fn main() {
    let args: Vec<String> = env::args().collect();

    if args.len() == 1 || args[1] == "help" {
        println!("Usage: language_rotator <json_path> [--status|--history|--force <lang>]");
        return;
    }

    let path = &args[1];
    let mut rotator = LanguageRotator::load(path).expect("Failed to load rotator state");

    if args.len() > 2 {
        match args[2].as_str() {
            "--status" => {
                println!("Current index: {}", rotator.current_index());
                println!("Languages:");
                for (i, lang) in rotator.languages().iter().enumerate() {
                    println!(
                        "  [{}] {} (weight={}, uses={})",
                        i, lang.name, lang.weight, lang.use_count
                    );
                }
                return;
            }
            "--history" => {
                for event in rotator.history() {
                    println!("  {} at {} (forced={})", event.language, event.timestamp, event.was_forced);
                }
                return;
            }
            "--force" => {
                if args.len() < 4 {
                    println!("--force requires a language name");
                    return;
                }
                let lang = &args[3];
                match rotator.force_select(lang) {
                    Ok(sel) => println!("Forced: {} (index={})", sel.language, sel.index),
                    Err(e) => {
                        eprintln!("Error: {}", e);
                        std::process::exit(1);
                    }
                }
            }
            _ => {
                eprintln!("Unknown option: {}", args[2]);
                std::process::exit(1);
            }
        }
    } else {
        match rotator.select() {
            Ok(sel) => {
                println!(
                    "Selected: {} (index={}, rotation_index={}, weight={})",
                    sel.language, sel.index, sel.rotation_index, sel.weight
                );
            }
            Err(e) => {
                eprintln!("Selection error: {}", e);
                std::process::exit(1);
            }
        }
    }

    rotator.save(path).expect("Failed to save rotator state");
}