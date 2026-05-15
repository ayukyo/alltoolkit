//! Currency Utils Usage Examples
//!
//! This example demonstrates various features of the currency_utils library.

use currency_utils::{Currency, CurrencyUtils, Money, FormatOptions};

fn main() {
    println!("=== Currency Utils Examples ===\n");

    // Create currency utility instance
    let utils = CurrencyUtils::new();

    // Example 1: Basic formatting
    println!("--- Basic Formatting ---");
    println!("$1,234.56 USD: {}", utils.format(1234.56, Currency::USD));
    println!("€1,234.56 EUR: {}", utils.format(1234.56, Currency::EUR));
    println!("¥1,234,567 JPY: {}", utils.format(1234567.0, Currency::JPY));
    println!("£1,234.56 GBP: {}", utils.format(1234.56, Currency::GBP));
    println!("₹1,234.56 INR: {}", utils.format(1234.56, Currency::INR));
    println!("₩1,234,567 KRW: {}", utils.format(1234567.0, Currency::KRW));
    println!();

    // Example 2: Money struct
    println!("--- Money Struct ---");
    let usd = Money::usd(100.0);
    let eur = Money::eur(92.0);
    let cny = Money::cny(724.0);
    let jpy = Money::jpy(14950.0);

    println!("USD: {}", usd);
    println!("EUR: {}", eur);
    println!("CNY: {}", cny);
    println!("JPY: {}", jpy);
    println!();

    // Example 3: Currency conversion
    println!("--- Currency Conversion ---");
    println!("$100 USD → EUR: {}", utils.convert_and_format(100.0, Currency::USD, Currency::EUR));
    println!("$100 USD → CNY: {}", utils.convert_and_format(100.0, Currency::USD, Currency::CNY));
    println!("$100 USD → JPY: {}", utils.convert_and_format(100.0, Currency::USD, Currency::JPY));
    println!("$100 USD → GBP: {}", utils.convert_and_format(100.0, Currency::USD, Currency::GBP));
    println!("$100 USD → KRW: {}", utils.convert_and_format(100.0, Currency::USD, Currency::KRW));
    println!("€100 EUR → USD: {}", utils.convert_and_format(100.0, Currency::EUR, Currency::USD));
    println!("¥1000 CNY → USD: {}", utils.convert_and_format(1000.0, Currency::CNY, Currency::USD));
    println!();

    // Example 4: Format options
    println!("--- Format Options ---");
    
    // Without symbol
    let options = FormatOptions::new().with_symbol(false);
    println!("No symbol: {}", utils.format_with_options(1234.56, Currency::USD, &options));
    
    // With currency code
    let options = FormatOptions::new().with_code(true);
    println!("With code: {}", utils.format_with_options(1234.56, Currency::USD, &options));
    
    // Without thousands separator
    let options = FormatOptions::new().with_thousands_separator(false);
    println!("No separator: {}", utils.format_with_options(1234567.89, Currency::USD, &options));
    
    // Parentheses for negative
    let options = FormatOptions::new().with_parentheses_for_negative(true);
    println!("Negative with parentheses: {}", utils.format_with_options(-1234.56, Currency::USD, &options));
    
    // Custom decimal places
    let options = FormatOptions::new().with_decimal_places(4);
    println!("4 decimal places: {}", utils.format_with_options(1234.5678, Currency::USD, &options));
    println!();

    // Example 5: Parsing currency strings
    println!("--- Parsing Currency Strings ---");
    let parsed: Money = "$1,234.56".parse().unwrap();
    println!("Parsed '$1,234.56': {} (amount: {}, currency: {})", parsed, parsed.amount, parsed.currency);
    
    let parsed: Money = "€500".parse().unwrap();
    println!("Parsed '€500': {} (amount: {}, currency: {})", parsed, parsed.amount, parsed.currency);
    
    let parsed: Money = "¥100,000".parse().unwrap();
    println!("Parsed '¥100,000': {} (amount: {}, currency: {})", parsed, parsed.amount, parsed.currency);
    
    let parsed: Money = "100 JPY".parse().unwrap();
    println!("Parsed '100 JPY': {} (amount: {}, currency: {})", parsed, parsed.amount, parsed.currency);
    println!();

    // Example 6: Money arithmetic
    println!("--- Money Arithmetic ---");
    let m1 = Money::usd(100.0);
    let m2 = Money::usd(50.0);
    
    println!("{} + {} = {}", m1, m2, utils.add(m1, m2));
    println!("{} - {} = {}", m1, m2, utils.subtract(m1, m2));
    println!("{} × 2 = {}", m1, utils.multiply(m1, 2.0));
    println!("{} ÷ 2 = {}", m1, utils.divide(m1, 2.0).unwrap());
    println!("10% of {} = {}", m1, utils.percentage(m1, 10.0));
    println!();

    // Example 7: Cross-currency arithmetic
    println!("--- Cross-Currency Arithmetic ---");
    let usd = Money::usd(100.0);
    let eur = Money::eur(92.0); // ≈ $100
    
    let sum = utils.add(usd, eur);
    println!("{} + {} = {} (≈ $200)", usd, eur, sum);
    
    let diff = utils.subtract(usd, eur);
    println!("{} - {} = {} (≈ $0)", usd, eur, diff);
    println!();

    // Example 8: Money comparison
    println!("--- Money Comparison ---");
    let m1 = Money::usd(100.0);
    let m2 = Money::usd(200.0);
    let m3 = Money::eur(92.0); // ≈ $100
    
    println!("{} < {}? {}", m1, m2, utils.less_than(m1, m2));
    println!("{} > {}? {}", m2, m1, utils.greater_than(m2, m1));
    println!("{} = {}? {} (cross-currency)", m1, m3, utils.equal(m1, m3));
    println!();

    // Example 9: Aggregation functions
    println!("--- Aggregation Functions ---");
    let amounts = [
        Money::usd(100.0),
        Money::usd(200.0),
        Money::usd(300.0),
    ];
    
    println!("Sum: {}", utils.sum(&amounts, Currency::USD));
    println!("Average: {}", utils.average(&amounts, Currency::USD).unwrap());
    println!("Min: {}", utils.min(&amounts).unwrap());
    println!("Max: {}", utils.max(&amounts).unwrap());
    println!();

    // Example 10: Rounding
    println!("--- Rounding ---");
    let money = Money::usd(123.456);
    println!("Original: {}", money);
    println!("Round: {}", utils.round(money));
    println!("Round up: {}", utils.round_up(money));
    println!("Round down: {}", utils.round_down(money));
    println!();

    // Example 11: Sign operations
    println!("--- Sign Operations ---");
    let positive = Money::usd(100.0);
    let negative = Money::usd(-100.0);
    let zero = Money::usd(0.0);
    
    println!("{} is positive? {}", positive, utils.is_positive(positive));
    println!("{} is negative? {}", negative, utils.is_negative(negative));
    println!("{} is zero? {}", zero, utils.is_zero(zero));
    println!("abs({}) = {}", negative, utils.abs(negative));
    println!("negate({}) = {}", positive, utils.negate(positive));
    println!();

    // Example 12: Format as words
    println!("--- Format as Words ---");
    println!("{}", utils.format_as_words(Money::usd(0.0)));
    println!("{}", utils.format_as_words(Money::usd(1.0)));
    println!("{}", utils.format_as_words(Money::usd(15.0)));
    println!("{}", utils.format_as_words(Money::usd(42.0)));
    println!("{}", utils.format_as_words(Money::usd(100.0)));
    println!("{}", utils.format_as_words(Money::usd(1234.56)));
    println!("{}", utils.format_as_words(Money::usd(1000000.0)));
    println!("{}", utils.format_as_words(Money::usd(1234567890.12)));
    println!();

    // Example 13: Currency information
    println!("--- Currency Information ---");
    for currency in [Currency::USD, Currency::EUR, Currency::JPY, Currency::GBP, Currency::CNY].iter() {
        println!("{}: {} ({}) - {} decimal places", 
            currency.code(), currency.name(), currency.symbol(), currency.decimal_places());
    }
    println!();

    // Example 14: Exchange rates
    println!("--- Exchange Rates (USD base) ---");
    println!("USD → EUR rate: {}", utils.get_exchange_rate(Currency::USD, Currency::EUR));
    println!("USD → CNY rate: {}", utils.get_exchange_rate(Currency::USD, Currency::CNY));
    println!("USD → JPY rate: {}", utils.get_exchange_rate(Currency::USD, Currency::JPY));
    println!("EUR → USD rate: {}", utils.get_exchange_rate(Currency::EUR, Currency::USD));
    println!();

    // Example 15: All supported currencies
    println!("--- All Supported Currencies ---");
    println!("Total: {} currencies", Currency::all().len());
    println!("Currencies: {:?}", Currency::all());
    println!();

    // Example 16: Large numbers
    println!("--- Large Numbers ---");
    println!("$1,234,567,890.12: {}", utils.format(1234567890.12, Currency::USD));
    println!("$1 trillion: {}", utils.format(1000000000000.0, Currency::USD));
    println!("¥100 billion: {}", utils.format(100000000000.0, Currency::JPY));
    println!();

    println!("=== All Examples Complete ===");
}