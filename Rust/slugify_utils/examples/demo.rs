//! Basic usage examples for slugify_utils

use std::collections::HashMap;

// Inline the module content (without doc comments for example purposes)
fn get_unicode_map() -> HashMap<char, &'static str> {
    let mut map = HashMap::new();
    map.insert('À', "A"); map.insert('Á', "A"); map.insert('Â', "A"); map.insert('Ã', "A");
    map.insert('Ä', "Ae"); map.insert('Å', "A"); map.insert('Æ', "Ae");
    map.insert('Ç', "C");
    map.insert('È', "E"); map.insert('É', "E"); map.insert('Ê', "E"); map.insert('Ë', "E");
    map.insert('Ì', "I"); map.insert('Í', "I"); map.insert('Î', "I"); map.insert('Ï', "I");
    map.insert('Ð', "D"); map.insert('Ñ', "N");
    map.insert('Ò', "O"); map.insert('Ó', "O"); map.insert('Ô', "O"); map.insert('Õ', "O");
    map.insert('Ö', "Oe"); map.insert('Ø', "O");
    map.insert('Ù', "U"); map.insert('Ú', "U"); map.insert('Û', "U"); map.insert('Ü', "Ue");
    map.insert('Ý', "Y"); map.insert('Þ', "Th"); map.insert('ß', "ss");
    map.insert('à', "a"); map.insert('á', "a"); map.insert('â', "a"); map.insert('ã', "a");
    map.insert('ä', "ae"); map.insert('å', "a"); map.insert('æ', "ae");
    map.insert('ç', "c");
    map.insert('è', "e"); map.insert('é', "e"); map.insert('ê', "e"); map.insert('ë', "e");
    map.insert('ì', "i"); map.insert('í', "i"); map.insert('î', "i"); map.insert('ï', "i");
    map.insert('ð', "d"); map.insert('ñ', "n");
    map.insert('ò', "o"); map.insert('ó', "o"); map.insert('ô', "o"); map.insert('õ', "o");
    map.insert('ö', "oe"); map.insert('ø', "o");
    map.insert('ù', "u"); map.insert('ú', "u"); map.insert('û', "u"); map.insert('ü', "ue");
    map.insert('ý', "y"); map.insert('þ', "th"); map.insert('ÿ', "y");
    // Cyrillic
    map.insert('а', "a"); map.insert('б', "b"); map.insert('в', "v"); map.insert('г', "g");
    map.insert('д', "d"); map.insert('е', "e"); map.insert('ё', "yo"); map.insert('ж', "zh");
    map.insert('з', "z"); map.insert('и', "i"); map.insert('й', "y"); map.insert('к', "k");
    map.insert('л', "l"); map.insert('м', "m"); map.insert('н', "n"); map.insert('о', "o");
    map.insert('п', "p"); map.insert('р', "r"); map.insert('с', "s"); map.insert('т', "t");
    map.insert('у', "u"); map.insert('ф', "f"); map.insert('х', "kh"); map.insert('ц', "ts");
    map.insert('ч', "ch"); map.insert('ш', "sh"); map.insert('щ', "shch");
    map.insert('ы', "y"); map.insert('э', "e"); map.insert('ю', "yu"); map.insert('я', "ya");
    map.insert('А', "A"); map.insert('Б', "B"); map.insert('В', "V"); map.insert('Г', "G");
    map.insert('Д', "D"); map.insert('Е', "E"); map.insert('Ё', "Yo"); map.insert('Ж', "Zh");
    map.insert('З', "Z"); map.insert('И', "I"); map.insert('Й', "Y"); map.insert('К', "K");
    map.insert('Л', "L"); map.insert('М', "M"); map.insert('Н', "N"); map.insert('О', "O");
    map.insert('П', "P"); map.insert('Р', "R"); map.insert('С', "S"); map.insert('Т', "T");
    map.insert('У', "U"); map.insert('Ф', "F"); map.insert('Х', "Kh"); map.insert('Ц', "Ts");
    map.insert('Ч', "Ch"); map.insert('Ш', "Sh"); map.insert('Щ', "Shch");
    map.insert('Ы', "Y"); map.insert('Э', "E"); map.insert('Ю', "Yu"); map.insert('Я', "Ya");
    // Greek
    map.insert('α', "a"); map.insert('β', "b"); map.insert('γ', "g"); map.insert('δ', "d");
    map.insert('ε', "e"); map.insert('ζ', "z"); map.insert('η', "i"); map.insert('θ', "th");
    map.insert('ι', "i"); map.insert('κ', "k"); map.insert('λ', "l"); map.insert('μ', "m");
    map.insert('ν', "n"); map.insert('ξ', "x"); map.insert('ο', "o"); map.insert('π', "p");
    map.insert('ρ', "r"); map.insert('σ', "s"); map.insert('ς', "s"); map.insert('τ', "t");
    map.insert('υ', "y"); map.insert('φ', "f"); map.insert('χ', "ch"); map.insert('ψ', "ps");
    map.insert('ω', "o");
    map.insert('ά', "a"); map.insert('έ', "e"); map.insert('ή', "i"); map.insert('ί', "i");
    map.insert('ό', "o"); map.insert('ύ', "y"); map.insert('ώ', "o");
    map.insert('Α', "A"); map.insert('Β', "B"); map.insert('Γ', "G"); map.insert('Δ', "D");
    map.insert('Ε', "E"); map.insert('Ζ', "Z"); map.insert('Η', "I"); map.insert('Θ', "Th");
    map.insert('Ι', "I"); map.insert('Κ', "K"); map.insert('Λ', "L"); map.insert('Μ', "M");
    map.insert('Ν', "N"); map.insert('Ξ', "X"); map.insert('Ο', "O"); map.insert('Π', "P");
    map.insert('Ρ', "R"); map.insert('Σ', "S"); map.insert('Τ', "T"); map.insert('Υ', "Y");
    map.insert('Φ', "F"); map.insert('Χ', "Ch"); map.insert('Ψ', "Ps"); map.insert('Ω', "O");
    // Symbols
    map.insert('$', "-dollar-"); map.insert('€', "-euro-"); map.insert('£', "-pound-");
    map.insert('¥', "-yen-"); map.insert('&', "-and-"); map.insert('@', "-at-");
    map.insert('#', "-hash-"); map.insert('%', "-percent-");
    map
}

fn slugify(input: &str) -> String {
    let unicode_map = get_unicode_map();
    let mut result = String::new();
    let mut prev_sep = false;
    
    for ch in input.chars() {
        if ch.is_whitespace() || ch == '_' {
            if !prev_sep && !result.is_empty() {
                result.push('-');
                prev_sep = true;
            }
            continue;
        }
        
        let processed = if let Some(rep) = unicode_map.get(&ch) {
            rep.to_string()
        } else if ch.is_ascii() {
            ch.to_string()
        } else {
            continue;
        };
        
        for pch in processed.chars() {
            if pch.is_alphanumeric() {
                result.push(pch.to_lowercase().next().unwrap_or(pch));
                prev_sep = false;
            } else if pch == '-' {
                if !prev_sep && !result.is_empty() {
                    result.push('-');
                    prev_sep = true;
                }
            }
        }
    }
    
    if result.ends_with('-') { result.pop(); }
    result
}

fn main() {
    println!("=== Slugify Utils Examples ===\n");
    
    println!("1. Basic slugification:");
    println!("   'Hello World' -> '{}'", slugify("Hello World"));
    println!("   'Hello, World!' -> '{}'", slugify("Hello, World!"));
    println!();
    
    println!("2. Unicode transliteration:");
    println!("   'Café' -> '{}'", slugify("Café"));
    println!("   'München' -> '{}'", slugify("München"));
    println!("   'Привет мир' -> '{}'", slugify("Привет мир"));
    println!("   'Αθήνα' -> '{}'", slugify("Αθήνα"));
    println!();
    
    println!("3. Special characters:");
    println!("   'Hello@World' -> '{}'", slugify("Hello@World"));
    println!("   '$50 discount' -> '{}'", slugify("$50 discount"));
    println!("   '€100 price' -> '{}'", slugify("€100 price"));
    println!();
    
    println!("4. Multiple spaces:");
    println!("   'Hello    World' -> '{}'", slugify("Hello    World"));
}