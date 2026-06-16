//! Example: generate an epic saga for each language in rotation
//!
//! Run with: cargo run --example example

use polyglot_epic_saga::{EpicSaga, Language};
use rand::SeedableRng;

fn main() {
    let mut rng = rand::rngs::StdRng::from_entropy();

    println!("Generating sagas for all 8 languages in rotation order...\n");

    for lang in Language::all() {
        let saga = EpicSaga::generate(lang, &mut rng);
        println!("{}", saga.render_text());
        println!("\n---\n");
    }

    println!("All sagas displayed. Rotation index unchanged (generate() doesn't advance it).");
    println!("Use run_cycle() to generate AND advance the rotation.");
}
