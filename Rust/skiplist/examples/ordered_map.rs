//! Ordered Map usage example

use skiplist::SkipList;

fn main() {
    println!("=== SkipList as Ordered Map Example ===\n");

    // SkipList can be used as an ordered map
    // Keys are automatically sorted
    let mut map: SkipList<String, i32> = SkipList::new();

    // Insert city populations (unordered)
    println!("--- Inserting city populations (unordered) ---");
    map.insert("Tokyo".to_string(), 37_400_000);
    map.insert("New York".to_string(), 8_400_000);
    map.insert("London".to_string(), 9_000_000);
    map.insert("Beijing".to_string(), 21_500_000);
    map.insert("Shanghai".to_string(), 28_500_000);
    map.insert("Paris".to_string(), 2_100_000);
    map.insert("Delhi".to_string(), 32_900_000);
    map.insert("Mumbai".to_string(), 21_000_000);

    println!("Inserted 8 cities");

    // Keys are automatically sorted alphabetically
    println!("\n--- Cities in alphabetical order ---");
    for (city, population) in map.iter() {
        println!("  {}: {} residents", city, population);
    }

    // Access specific city
    println!("\n--- Accessing specific cities ---");
    println!("Tokyo population: {:?}", map.get(&"Tokyo".to_string()));
    println!("Paris population: {:?}", map.get(&"Paris".to_string()));
    println!("Sydney population: {:?}", map.get(&"Sydney".to_string())); // Not found

    // First and last (alphabetically)
    println!("\n--- First and last (alphabetically) ---");
    if let Some((first_city, pop)) = map.first_key_value() {
        println!("First city: {} (population: {})", first_city, pop);
    }
    if let Some((last_city, pop)) = map.last_key_value() {
        println!("Last city: {} (population: {})", last_city, pop);
    }

    // Range of cities
    println!("\n--- Cities from 'L' to 'S' ---");
    let range = map.range("London".to_string().."Shanghai".to_string());
    for (city, population) in range {
        println!("  {}: {} residents", city, population);
    }

    // Update population
    println!("\n--- Updating population ---");
    let old = map.insert("Tokyo".to_string(), 38_000_000);
    println!("Tokyo population updated: {} -> {}", old.unwrap(), 38_000_000);

    // Remove a city
    println!("\n--- Removing Paris ---");
    let removed = map.remove(&"Paris".to_string());
    println!("Removed Paris with population: {}", removed.unwrap());
    println!("Remaining cities: {}", map.len());

    // Build from iterator
    println!("\n--- Building from iterator ---");
    let countries: SkipList<String, String> = [
        ("Japan", "Asia"),
        ("France", "Europe"),
        ("Brazil", "South America"),
        ("Canada", "North America"),
        ("Australia", "Oceania"),
    ]
        .into_iter()
        .map(|(k, v)| (k.to_string(), v.to_string()))
        .collect();

    println!("Countries:");
    for (country, region) in countries.iter() {
        println!("  {} -> {}", country, region);
    }

    // Clone the map
    println!("\n--- Cloning the map ---");
    let cloned = map.clone();
    println!("Original has {} cities", map.len());
    println!("Clone has {} cities", cloned.len());
    println!("Clone first city: {:?}", cloned.first_key_value());

    // Modify original, clone stays independent
    map.remove(&"Beijing".to_string());
    println!("\nAfter removing Beijing from original:");
    println!("  Original: {} cities", map.len());
    println!("  Clone: {} cities", cloned.len());

    println!("\n=== Example Complete ===");
}