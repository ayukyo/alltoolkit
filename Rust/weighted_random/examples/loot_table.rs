//! Game loot table example using weighted_random
//!
//! Run with: cargo run --example loot_table

use weighted_random::{Selector, WeightedItem};

/// Represents a loot item in a game
#[derive(Debug, Clone)]
struct LootItem {
    name: String,
    rarity: Rarity,
    value: usize,
}

#[derive(Debug, Clone, Copy, PartialEq)]
enum Rarity {
    Common,
    Uncommon,
    Rare,
    Epic,
    Legendary,
}

impl std::fmt::Display for Rarity {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Rarity::Common => write!(f, "Common"),
            Rarity::Uncommon => write!(f, "Uncommon"),
            Rarity::Rare => write!(f, "Rare"),
            Rarity::Epic => write!(f, "Epic"),
            Rarity::Legendary => write!(f, "Legendary"),
        }
    }
}

impl LootItem {
    fn new(name: &str, rarity: Rarity, value: usize) -> Self {
        Self {
            name: name.to_string(),
            rarity,
            value,
        }
    }
}

fn main() {
    println!("=== Game Loot Table System ===\n");

    monster_drops();
    chest_loot();
    gacha_system();
    crafting_drops();
}

fn monster_drops() {
    println!("--- Example 1: Monster Drop Table ---\n");

    let dragon_drops = vec![
        WeightedItem::new(LootItem::new("Dragon Scale", Rarity::Rare, 100), 15.0),
        WeightedItem::new(LootItem::new("Dragon Bone", Rarity::Rare, 80), 15.0),
        WeightedItem::new(LootItem::new("Dragon Tooth", Rarity::Epic, 200), 5.0),
        WeightedItem::new(LootItem::new("Dragon Heart", Rarity::Legendary, 1000), 1.0),
        WeightedItem::new(LootItem::new("Gold Coins", Rarity::Common, 50), 30.0),
        WeightedItem::new(LootItem::new("Trash", Rarity::Common, 1), 34.0),
    ];

    let selector = Selector::new(dragon_drops).unwrap();

    println!("Dragon drop probabilities:");
    println!("  Legendary: ~1% (Dragon Heart)");
    println!("  Epic: ~5% (Dragon Tooth)");
    println!("  Rare: ~30% (Dragon Scale/Bone)");
    println!("  Common: ~64% (Gold/Trash)");

    println!("\nDefeating dragon 20 times...");
    let mut total_gold = 0;
    let mut rarity_counts: std::collections::HashMap<Rarity, usize> = std::collections::HashMap::new();

    for i in 1..=20 {
        let drop = selector.select();
        total_gold += drop.value;
        *rarity_counts.entry(drop.rarity).or_insert(0) += 1;

        println!("  Kill {}: {} [{}] - {} gold", i, drop.name, drop.rarity, drop.value);
    }

    println!("\nSummary:");
    println!("  Total gold earned: {}", total_gold);
    println!("  Rarity distribution:");
    for rarity in [Rarity::Legendary, Rarity::Epic, Rarity::Rare, Rarity::Common] {
        let count = rarity_counts.get(&rarity).unwrap_or(&0);
        println!("    {}: {} items", rarity, count);
    }
    println!();
}

fn chest_loot() {
    println!("--- Example 2: Treasure Chest Loot ---\n");

    let wooden_chest = vec![
        WeightedItem::new(LootItem::new("Wooden Sword", Rarity::Common, 10), 40.0),
        WeightedItem::new(LootItem::new("Minor Health Potion", Rarity::Common, 5), 30.0),
        WeightedItem::new(LootItem::new("Iron Ring", Rarity::Uncommon, 25), 20.0),
        WeightedItem::new(LootItem::new("Silver Coins", Rarity::Common, 15), 10.0),
    ];

    let golden_chest = vec![
        WeightedItem::new(LootItem::new("Magic Sword", Rarity::Epic, 500), 10.0),
        WeightedItem::new(LootItem::new("Enchanted Shield", Rarity::Rare, 200), 25.0),
        WeightedItem::new(LootItem::new("Ancient Scroll", Rarity::Rare, 150), 25.0),
        WeightedItem::new(LootItem::new("Diamond Ring", Rarity::Epic, 400), 10.0),
        WeightedItem::new(LootItem::new("Gold Coins (100)", Rarity::Uncommon, 100), 30.0),
    ];

    println!("Opening 5 wooden chests:");
    let wooden_selector = Selector::new(wooden_chest).unwrap();
    for i in 1..=5 {
        let item = wooden_selector.select();
        println!("  Chest {}: {} [{}]", i, item.name, item.rarity);
    }

    println!("\nOpening 3 golden chests:");
    let golden_selector = Selector::new(golden_chest).unwrap();
    for i in 1..=3 {
        let item = golden_selector.select();
        println!("  Chest {}: {} [{}]", i, item.name, item.rarity);
    }
    println!();
}

fn gacha_system() {
    println!("--- Example 3: Gacha/Roll System ---\n");

    let gacha_pool = vec![
        WeightedItem::new("SSR: Legendary Hero", 0.5),
        WeightedItem::new("SR: Epic Warrior", 5.0),
        WeightedItem::new("R: Rare Mage", 15.0),
        WeightedItem::new("N: Common Soldier", 79.5),
    ];

    let selector = Selector::new(gacha_pool).unwrap();

    println!("Gacha rates:");
    println!("  SSR (0.5%): Legendary Hero");
    println!("  SR (5%): Epic Warrior");
    println!("  R (15%): Rare Mage");
    println!("  N (79.5%): Common Soldier");

    println!("\nRolling 10 times:");
    for i in 1..=10 {
        let result = selector.select();
        let stars = if result.starts_with("SSR") { "★★★★★" }
                    else if result.starts_with("SR") { "★★★★" }
                    else if result.starts_with("R") { "★★★" }
                    else { "★★" };
        let name = result.split(": ").nth(1).unwrap_or(result);
        println!("  Roll {}: {} {}", i, stars, name);
    }

    println!("\nSimulating 1000 rolls for SSR hit rate:");
    let mut ssr_count = 0;
    for _ in 0..1000 {
        if selector.select().starts_with("SSR") {
            ssr_count += 1;
        }
    }
    println!("  SSR obtained: {} times ({:.2}%)", ssr_count, ssr_count as f64 / 1000.0 * 100.0);
    println!("  (Expected: ~0.5% = ~5 SSRs)");
    println!();
}

fn crafting_drops() {
    println!("--- Example 4: Crafting Material Drops ---\n");

    let mining_table = vec![
        WeightedItem::new("Iron Ore", 40.0),
        WeightedItem::new("Copper Ore", 30.0),
        WeightedItem::new("Silver Ore", 15.0),
        WeightedItem::new("Gold Ore", 10.0),
        WeightedItem::new("Diamond", 5.0),
    ];

    let selector = Selector::new(mining_table).unwrap();

    println!("Mining 20 times:");
    let mut materials: std::collections::HashMap<&str, usize> = std::collections::HashMap::new();

    for _ in 0..20 {
        let material = selector.select();
        *materials.entry(material).or_insert(0) += 1;
    }

    println!("Materials collected:");
    for (material, count) in &materials {
        println!("  {}: {} units", material, count);
    }
    println!();
}