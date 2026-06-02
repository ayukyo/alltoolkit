//! Binary entry point for language_probe
//!
//! Loads language_rotation.json, probes all language runtimes in parallel,
//! displays the capability matrix, advances the index (next = Go), saves.
//!
//! Supports --force-rust to force-select Rust for this run (used when cron
//! specifies Rust as the mandatory selection for this cycle).

use language_probe::{
    load_rotation_state, save_rotation_state, current_language, advance_index,
    probe_all,
};

fn main() {
    let force_rust = std::env::args().any(|a| a == "--force-rust");

    // 1. Load rotation state
    let mut state = match load_rotation_state() {
        Ok(s) => s,
        Err(e) => {
            eprintln!("ERROR loading {}: {}", "/home/admin/.openclaw/workspace/AllToolkit/language_rotation.json", e);
            std::process::exit(1);
        }
    };

    // 2. Determine current language
    let current_lang = if force_rust {
        println!("[language_probe] 🔒 Force-rust mode: locking to Rust (index 0)");
        "Rust".to_string()
    } else {
        match current_language(&state) {
            Some(l) => l,
            None => {
                eprintln!("ERROR: No languages in rotation state");
                std::process::exit(1);
            }
        }
    };

    println!("[language_probe] Current language: {} (rotation index: {})", current_lang, state.current_index);
    println!();

    // 3. Probe all languages in parallel
    let (_, summary) = probe_all(&state.languages);

    // 4. Display capability matrix
    println!("{}", summary.display());

    // 5. Advance index (next run selects next language)
    let prev_index = state.current_index;
    let prev_lang = current_lang.clone();
    advance_index(&mut state);
    let next_lang = state.languages.get(state.current_index).cloned().unwrap_or_default();

    if force_rust {
        // Reset to index 1 (Go) so next cycle picks up from where it left off
        state.current_index = 1;
        println!("[language_probe] ✅ Force-rust: Rotated {} → Go (index reset to 1 for next cycle)", prev_lang);
    } else {
        println!("[language_probe] ✅ Rotated index {} → {} (next: {})", prev_index, state.current_index, next_lang);
    }

    // 6. Save updated state
    if let Err(e) = save_rotation_state(&state) {
        eprintln!("ERROR saving state: {}", e);
        std::process::exit(1);
    }

    println!("[language_probe] ✅ State saved to language_rotation.json");
    println!("[language_probe] ✅ Next scheduled language: {}", state.languages.get(state.current_index).unwrap_or(&"<none>".to_string()));
}
