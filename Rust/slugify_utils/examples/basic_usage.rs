//! Basic usage examples for slugify_utils

fn main() {
    println!("=== Slugify Utils Examples ===\n");
    
    // Basic slugification
    println!("1. Basic slugification:");
    println!("   'Hello World' -> '{}'", slugify("Hello World"));
    println!("   'Hello, World!' -> '{}'", slugify("Hello, World!"));
    println!("   '  Multiple   Spaces  ' -> '{}'", slugify("  Multiple   Spaces  "));
    println!();
    
    // Unicode transliteration
    println!("2. Unicode transliteration:");
    println!("   'Café' -> '{}'", slugify("Café"));
    println!("   'München' -> '{}'", slugify("München"));
    println!("   'naïve' -> '{}'", slugify("naïve"));
    println!("   'Привет мир' -> '{}'", slugify("Привет мир"));
    println!("   'Αθήνα' -> '{}'", slugify("Αθήνα"));
    println!();
    
    // Special characters
    println!("3. Special characters:");
    println!("   'Hello@World' -> '{}'", slugify("Hello@World"));
    println!("   '100% Pure' -> '{}'", slugify("100% Pure"));
    println!("   '$50 discount' -> '{}'", slugify("$50 discount"));
    println!("   '€100 price' -> '{}'", slugify("€100 price"));
    println!();
    
    // Custom options
    println!("4. Custom options:");
    let underscore_sep = SlugifyOptions::new().separator('_');
    println!("   Underscore separator: '{}'", slugify_with_options("Hello World", underscore_sep));
    
    let preserve_case = SlugifyOptions::new().lowercase(false);
    println!("   Preserve case: '{}'", slugify_with_options("Hello World", preserve_case));
    
    let with_max_len = SlugifyOptions::new().max_length(15);
    println!("   Max length 15: '{}'", slugify_with_options("Hello Beautiful Amazing World", with_max_len));
    
    let no_transliterate = SlugifyOptions::new().transliterate(false);
    println!("   No transliterate: '{}'", slugify_with_options("Hello World Test", no_transliterate));
    println!();
    
    // With ID
    println!("5. Slug with ID:");
    println!("   ('My Blog Post', 123) -> '{}'", slugify_with_id("My Blog Post", 123));
    println!("   ('', 456) -> '{}'", slugify_with_id("", 456));
    println!();
    
    // Validation
    println!("6. Validation:");
    println!("   'hello-world' is valid: {}", is_valid_slug("hello-world"));
    println!("   'Hello_World' is valid: {}", is_valid_slug("Hello_World"));
    println!("   '-invalid' is valid: {}", is_valid_slug("-invalid"));
    println!();
    
    // Unslugify
    println!("7. Unslugify:");
    println!("   'hello-world' -> '{}'", unslugify("hello-world"));
    println!("   'my-blog-post-123' -> '{}'", unslugify("my-blog-post-123"));
    println!();
    
    // Truncate
    println!("8. Truncate:");
    println!("   'hello-world-from-rust' (max 10) -> '{}'", 
        truncate_slug("hello-world-from-rust", 10));
}

mod slugify_utils {
    include!("../mod.rs");
}

use slugify_utils::*;