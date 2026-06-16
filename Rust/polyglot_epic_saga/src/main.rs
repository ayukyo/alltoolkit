//! Binary entry point for polyglot_epic_saga
//!
//! Usage:
//!     cargo run [-- <rotation_json>]
//!
//! Environment:
//!     WORKSPACE_ROOT  Root workspace directory (default: /home/admin/.openclaw/workspace)

use polyglot_epic_saga::run_cycle_with_log;
use rand::SeedableRng;
use std::env;
use std::path::PathBuf;

const DEFAULT_WORKSPACE: &str = "/home/admin/.openclaw/workspace";

fn main() {
    let args: Vec<String> = env::args().collect();

    let workspace = PathBuf::from(
        env::var("WORKSPACE_ROOT").unwrap_or_else(|_| DEFAULT_WORKSPACE.to_string()),
    );

    let rotation_path = args
        .get(1)
        .map(PathBuf::from)
        .unwrap_or_else(|| workspace.join("language_rotation.json"));
    let log_path = workspace.join("polyglot_epic_saga_log.json");

    let mut rng = rand::rngs::StdRng::from_entropy();

    match run_cycle_with_log(&rotation_path, &log_path, &mut rng) {
        Ok(ref saga) => {
            let lang = saga.language.clone();
            println!("{}", saga.render_text());
            println!("\n✅ Saga generated for {} and rotation advanced.", lang);
        }
        Err(e) => {
            eprintln!("Error: {}", e);
            std::process::exit(1);
        }
    }
}
