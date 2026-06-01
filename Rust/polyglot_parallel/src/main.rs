//! Binary entry point for polyglot_parallel
//!
//! Loads language_rotation.json, picks the current language (Rust this run),
//! runs the parallel banner worker, advances the index (next = Go), saves.

use polyglot_parallel::{run_parallel, load_rotation_state, save_rotation_state,
    current_language, advance_index};

fn main() {
    // 1. Load rotation state
    let mut state = match load_rotation_state() {
        Ok(s) => s,
        Err(e) => {
            eprintln!("ERROR loading {}: {}", "/home/admin/.openclaw/workspace/AllToolkit/language_rotation.json", e);
            std::process::exit(1);
        }
    };

    // 2. Determine current language (must be Rust per cron spec)
    let lang = match current_language(&state) {
        Some(l) => l,
        None => {
            eprintln!("ERROR: No languages in rotation state");
            std::process::exit(1);
        }
    };

    println!("[polyglot_parallel] Current language: {}", lang);

    // 3. Run parallel workers
    let languages = state.languages.clone();
    let summary = run_parallel(languages.len(), &languages);

    // 4. Display results
    println!("{}", summary.display());

    // 5. Advance index (next run selects Go)
    let prev_index = state.current_index;
    advance_index(&mut state);
    println!("[polyglot_parallel] Advanced index {} -> {} (next: {:?})",
             prev_index, state.current_index,
             state.languages.get(state.current_index));

    // 6. Save updated state
    if let Err(e) = save_rotation_state(&state) {
        eprintln!("ERROR saving state: {}", e);
        std::process::exit(1);
    }

    println!("[polyglot_parallel] State saved. Rotation: {} -> {}",
             lang, state.languages.get(state.current_index).unwrap_or(&"<none>".to_string()));
}