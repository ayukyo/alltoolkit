//! Example: CLI tool using language_safety_matrix

use language_safety_matrix::{generate_matrix, LanguageSafetyProfile, SAFETY_AXES};

fn main() {
    let args: Vec<String> = std::env::args().collect();

    if args.len() == 1 || args[1] == "--help" {
        println!("🛡️ Language Safety Matrix");
        println!();
        println!("Usage:");
        println!("  language_safety_matrix <lang>        # Safety profile for one language");
        println!("  language_safety_matrix <lang1> <lang2> ...  # Compare multiple languages");
        println!("  language_safety_matrix --all           # All 8 languages in matrix");
        println!("  language_safety_matrix --axes        # List safety axes");
        return;
    }

    if args[1] == "--axes" {
        println!("Safety Axes ({} total):", SAFETY_AXES.len());
        for (i, axis) in SAFETY_AXES.iter().enumerate() {
            println!("  {}. {}", i + 1, axis);
        }
        return;
    }

    let languages: Vec<&str> = if args[1] == "--all" {
        vec!["Rust", "Go", "Swift", "Kotlin", "TypeScript", "JavaScript", "Java", "C/C++"]
    } else {
        args[1..].iter().map(|s| s.as_str()).collect()
    };

    if languages.len() == 1 {
        let profile = LanguageSafetyProfile::generate(languages[0]);
        println!("{}", profile.radar_chart());
    } else {
        // Comparative matrix
        let matrix = generate_matrix(&languages);

        println!("\n🛡️ Comparative Safety Matrix\n");
        println!("{:15}  {:>6}  {:>6}  {:>6}  {:>6}  {:>6}  {:>6}  {:>6}  {:>6}",
            "Language",
            SAFETY_AXES[0].split_whitespace().next().unwrap(),
            SAFETY_AXES[1].split_whitespace().next().unwrap(),
            SAFETY_AXES[2].split_whitespace().next().unwrap(),
            SAFETY_AXES[3].split_whitespace().next().unwrap(),
            SAFETY_AXES[4].split_whitespace().next().unwrap(),
            SAFETY_AXES[5].split_whitespace().next().unwrap(),
            SAFETY_AXES[6].split_whitespace().next().unwrap(),
            SAFETY_AXES[7].split_whitespace().next().unwrap(),
        );
        println!("{}", "-".repeat(120));

        for (lang, profile) in &matrix {
            let scores: Vec<String> = profile.axes.iter().map(|a| format!("{:>6.0}%", a.score * 100.0)).collect();
            println!(
                "{:15}  {}",
                lang,
                scores.join("  ")
            );
        }

        println!();
        println!("Overall Rankings:");
        let mut sorted: Vec<_> = matrix.iter().collect();
        sorted.sort_by(|a, b| b.1.overall_score.partial_cmp(&a.1.overall_score).unwrap());
        for (i, (lang, profile)) in sorted.iter().enumerate() {
            println!("  {}. {} — {:.0}% ({})", i + 1, lang, profile.overall_score * 100.0, profile.risk_profile);
        }
    }
}