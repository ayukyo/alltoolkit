use syntax_translator::SyntaxTranslator;
use std::path::PathBuf;
use std::fs;

fn main() {
    let t = SyntaxTranslator::new();

    // Kotlin test
    let result = t.translate(r#"fun main() { println("hello") }"#, "Kotlin", "Rust").unwrap();
    println!("Kotlin -> Rust:");
    println!("  translated: {:?}", result.translated_code);
    println!("  rules_applied: {}", result.rules_applied);

    // Java test
    let result2 = t.translate("public static void main(String[] args) { System.out.println(\"hello\"); }", "Java", "Rust").unwrap();
    println!("\nJava -> Rust:");
    println!("  translated: {:?}", result2.translated_code);
    println!("  rules_applied: {}", result2.rules_applied);
}