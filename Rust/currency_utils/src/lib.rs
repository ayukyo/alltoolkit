//! # Currency Utils
//!
//! A comprehensive currency formatting and conversion utility library.
//! Supports 20+ major currencies with formatting, parsing, arithmetic, and conversion.
//! Zero external dependencies - uses only Rust standard library.
//!
//! ## Features
//!
//! - Format amounts with proper currency symbols and separators
//! - Parse currency strings like "$1,234.56" or "¥100,000"
//! - Convert between currencies using hardcoded exchange rates
//! - Currency arithmetic with proper rounding
//! - Support for 20+ major world currencies
//! - Customizable formatting options
//!
//! ## Example
//!
//! ```rust
//! use currency_utils::{Currency, CurrencyUtils};
//!
//! let utils = CurrencyUtils::new();
//!
//! // Format currency
//! let formatted = utils.format(1234.56, Currency::USD);
//! println!("{}", formatted); // "$1,234.56"
//!
//! // Convert between currencies
//! let eur = utils.convert(100.0, Currency::USD, Currency::EUR);
//! println!("$100 = €{:.2}", eur);
//! ```

use std::fmt;
use std::str::FromStr;

/// Currency code enumeration representing different world currencies
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub enum Currency {
    // Americas
    USD, // US Dollar
    CAD, // Canadian Dollar
    MXN, // Mexican Peso
    BRL, // Brazilian Real
    ARS, // Argentine Peso
    
    // Europe
    EUR, // Euro
    GBP, // British Pound
    CHF, // Swiss Franc
    SEK, // Swedish Krona
    NOK, // Norwegian Krone
    DKK, // Danish Krone
    RUB, // Russian Ruble
    PLN, // Polish Zloty
    
    // Asia
    CNY, // Chinese Yuan
    JPY, // Japanese Yen
    KRW, // South Korean Won
    INR, // Indian Rupee
    HKD, // Hong Kong Dollar
    SGD, // Singapore Dollar
    TWD, // Taiwan Dollar
    THB, // Thai Baht
}

impl Currency {
    /// Get the ISO 4217 currency code
    pub fn code(&self) -> &'static str {
        match self {
            Currency::USD => "USD",
            Currency::CAD => "CAD",
            Currency::MXN => "MXN",
            Currency::BRL => "BRL",
            Currency::ARS => "ARS",
            Currency::EUR => "EUR",
            Currency::GBP => "GBP",
            Currency::CHF => "CHF",
            Currency::SEK => "SEK",
            Currency::NOK => "NOK",
            Currency::DKK => "DKK",
            Currency::RUB => "RUB",
            Currency::PLN => "PLN",
            Currency::CNY => "CNY",
            Currency::JPY => "JPY",
            Currency::KRW => "KRW",
            Currency::INR => "INR",
            Currency::HKD => "HKD",
            Currency::SGD => "SGD",
            Currency::TWD => "TWD",
            Currency::THB => "THB",
        }
    }

    /// Get the currency symbol
    pub fn symbol(&self) -> &'static str {
        match self {
            Currency::USD => "$",
            Currency::CAD => "C$",
            Currency::MXN => "Mex$",
            Currency::BRL => "R$",
            Currency::ARS => "$",
            Currency::EUR => "€",
            Currency::GBP => "£",
            Currency::CHF => "Fr",
            Currency::SEK => "kr",
            Currency::NOK => "kr",
            Currency::DKK => "kr",
            Currency::RUB => "₽",
            Currency::PLN => "zł",
            Currency::CNY => "¥",
            Currency::JPY => "¥",
            Currency::KRW => "₩",
            Currency::INR => "₹",
            Currency::HKD => "HK$",
            Currency::SGD => "S$",
            Currency::TWD => "NT$",
            Currency::THB => "฿",
        }
    }

    /// Get the full currency name
    pub fn name(&self) -> &'static str {
        match self {
            Currency::USD => "US Dollar",
            Currency::CAD => "Canadian Dollar",
            Currency::MXN => "Mexican Peso",
            Currency::BRL => "Brazilian Real",
            Currency::ARS => "Argentine Peso",
            Currency::EUR => "Euro",
            Currency::GBP => "British Pound",
            Currency::CHF => "Swiss Franc",
            Currency::SEK => "Swedish Krona",
            Currency::NOK => "Norwegian Krone",
            Currency::DKK => "Danish Krone",
            Currency::RUB => "Russian Ruble",
            Currency::PLN => "Polish Zloty",
            Currency::CNY => "Chinese Yuan",
            Currency::JPY => "Japanese Yen",
            Currency::KRW => "South Korean Won",
            Currency::INR => "Indian Rupee",
            Currency::HKD => "Hong Kong Dollar",
            Currency::SGD => "Singapore Dollar",
            Currency::TWD => "Taiwan Dollar",
            Currency::THB => "Thai Baht",
        }
    }

    /// Get the number of decimal places for this currency
    pub fn decimal_places(&self) -> u8 {
        match self {
            Currency::JPY => 0,
            Currency::KRW => 0,
            _ => 2,
        }
    }

    /// Get the decimal separator character
    pub fn decimal_separator(&self) -> char {
        match self {
            Currency::EUR => ',', // Most EU countries use comma
            Currency::CHF => '.', // Switzerland uses period
            Currency::SEK | Currency::NOK | Currency::DKK => ',',
            Currency::PLN => ',',
            Currency::RUB => ',',
            _ => '.',
        }
    }

    /// Get the thousands separator character
    pub fn thousands_separator(&self) -> char {
        match self {
            Currency::EUR => '.', // Most EU countries use period
            Currency::CHF => '\'',
            Currency::SEK | Currency::NOK | Currency::DKK => ' ',
            Currency::PLN => ' ',
            Currency::RUB => ' ',
            _ => ',',
        }
    }

    /// Check if symbol should be placed before the amount
    pub fn symbol_before(&self) -> bool {
        match self {
            Currency::EUR => false, // € is typically after in many EU countries
            Currency::SEK | Currency::NOK | Currency::DKK => false,
            Currency::PLN => false,
            Currency::THB => false,
            _ => true,
        }
    }

    /// Get all supported currencies
    pub fn all() -> Vec<Currency> {
        vec![
            Currency::USD,
            Currency::CAD,
            Currency::MXN,
            Currency::BRL,
            Currency::ARS,
            Currency::EUR,
            Currency::GBP,
            Currency::CHF,
            Currency::SEK,
            Currency::NOK,
            Currency::DKK,
            Currency::RUB,
            Currency::PLN,
            Currency::CNY,
            Currency::JPY,
            Currency::KRW,
            Currency::INR,
            Currency::HKD,
            Currency::SGD,
            Currency::TWD,
            Currency::THB,
        ]
    }

    /// Parse currency from code or symbol
    pub fn from_code_or_symbol(s: &str) -> Option<Currency> {
        let s = s.trim().to_uppercase();
        
        // Try by code first
        Currency::from_str(&s).ok().or_else(|| {
            // Try by symbol
            match s.as_str() {
                "$" | "DOLLAR" => Some(Currency::USD),
                "C$" => Some(Currency::CAD),
                "MEX$" => Some(Currency::MXN),
                "R$" => Some(Currency::BRL),
                "€" | "EUR" => Some(Currency::EUR),
                "£" | "GBP" => Some(Currency::GBP),
                "FR" | "CHF" => Some(Currency::CHF),
                "KR" => Some(Currency::SEK), // Default to SEK for kr
                "₽" => Some(Currency::RUB),
                "ZŁ" => Some(Currency::PLN),
                "¥" | "YUAN" => Some(Currency::CNY), // Default to CNY for ¥
                "₩" => Some(Currency::KRW),
                "₹" => Some(Currency::INR),
                "HK$" => Some(Currency::HKD),
                "S$" => Some(Currency::SGD),
                "NT$" => Some(Currency::TWD),
                "฿" => Some(Currency::THB),
                _ => None,
            }
        })
    }
}

impl fmt::Display for Currency {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{}", self.code())
    }
}

impl FromStr for Currency {
    type Err = CurrencyError;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let s = s.trim().to_uppercase();
        match s.as_str() {
            "USD" => Ok(Currency::USD),
            "CAD" => Ok(Currency::CAD),
            "MXN" => Ok(Currency::MXN),
            "BRL" => Ok(Currency::BRL),
            "ARS" => Ok(Currency::ARS),
            "EUR" => Ok(Currency::EUR),
            "GBP" => Ok(Currency::GBP),
            "CHF" => Ok(Currency::CHF),
            "SEK" => Ok(Currency::SEK),
            "NOK" => Ok(Currency::NOK),
            "DKK" => Ok(Currency::DKK),
            "RUB" => Ok(Currency::RUB),
            "PLN" => Ok(Currency::PLN),
            "CNY" | "RMB" => Ok(Currency::CNY),
            "JPY" => Ok(Currency::JPY),
            "KRW" => Ok(Currency::KRW),
            "INR" => Ok(Currency::INR),
            "HKD" => Ok(Currency::HKD),
            "SGD" => Ok(Currency::SGD),
            "TWD" => Ok(Currency::TWD),
            "THB" => Ok(Currency::THB),
            _ => Err(CurrencyError::InvalidCurrency(s)),
        }
    }
}

/// Money value with currency
#[derive(Debug, Clone, Copy)]
pub struct Money {
    pub amount: f64,
    pub currency: Currency,
}

impl Money {
    /// Create a new Money instance
    pub fn new(amount: f64, currency: Currency) -> Self {
        Self { amount, currency }
    }

    /// Create USD money
    pub fn usd(amount: f64) -> Self {
        Self::new(amount, Currency::USD)
    }

    /// Create EUR money
    pub fn eur(amount: f64) -> Self {
        Self::new(amount, Currency::EUR)
    }

    /// Create CNY money
    pub fn cny(amount: f64) -> Self {
        Self::new(amount, Currency::CNY)
    }

    /// Create JPY money
    pub fn jpy(amount: f64) -> Self {
        Self::new(amount, Currency::JPY)
    }

    /// Create GBP money
    pub fn gbp(amount: f64) -> Self {
        Self::new(amount, Currency::GBP)
    }

    /// Format this money with default options
    pub fn format(&self) -> String {
        CurrencyUtils::new().format(self.amount, self.currency)
    }

    /// Convert to another currency
    pub fn convert_to(&self, target: Currency, utils: &CurrencyUtils) -> Self {
        let converted = utils.convert(self.amount, self.currency, target);
        Money::new(converted, target)
    }
}

impl fmt::Display for Money {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{}", self.format())
    }
}

impl FromStr for Money {
    type Err = CurrencyError;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        parse_money(s)
    }
}

/// Error types for currency operations
#[derive(Debug, Clone)]
pub enum CurrencyError {
    InvalidCurrency(String),
    ParseError(String),
    InvalidAmount(String),
    ConversionError(String),
}

impl fmt::Display for CurrencyError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            CurrencyError::InvalidCurrency(s) => write!(f, "Invalid currency: {}", s),
            CurrencyError::ParseError(s) => write!(f, "Failed to parse currency: {}", s),
            CurrencyError::InvalidAmount(s) => write!(f, "Invalid amount: {}", s),
            CurrencyError::ConversionError(s) => write!(f, "Conversion error: {}", s),
        }
    }
}

impl std::error::Error for CurrencyError {}

/// Format options for currency display
#[derive(Debug, Clone)]
pub struct FormatOptions {
    /// Include currency symbol
    pub include_symbol: bool,
    /// Include currency code
    pub include_code: bool,
    /// Use thousands separator
    pub use_thousands_separator: bool,
    /// Custom decimal places (overrides currency default)
    pub decimal_places: Option<u8>,
    /// Use parentheses for negative amounts
    pub parentheses_for_negative: bool,
}

impl Default for FormatOptions {
    fn default() -> Self {
        Self {
            include_symbol: true,
            include_code: false,
            use_thousands_separator: true,
            decimal_places: None,
            parentheses_for_negative: false,
        }
    }
}

impl FormatOptions {
    /// Create new format options with defaults
    pub fn new() -> Self {
        Self::default()
    }

    /// Set include_symbol option
    pub fn with_symbol(mut self, include: bool) -> Self {
        self.include_symbol = include;
        self
    }

    /// Set include_code option
    pub fn with_code(mut self, include: bool) -> Self {
        self.include_code = include;
        self
    }

    /// Set use_thousands_separator option
    pub fn with_thousands_separator(mut self, use_separator: bool) -> Self {
        self.use_thousands_separator = use_separator;
        self
    }

    /// Set custom decimal places
    pub fn with_decimal_places(mut self, places: u8) -> Self {
        self.decimal_places = Some(places);
        self
    }

    /// Set parentheses_for_negative option
    pub fn with_parentheses_for_negative(mut self, use_parentheses: bool) -> Self {
        self.parentheses_for_negative = use_parentheses;
        self
    }
}

/// Exchange rates relative to USD (approximate rates)
/// Note: These are hardcoded approximate rates for demonstration
/// In production, use real-time rates from an API
const EXCHANGE_RATES_USD: &[(Currency, f64)] = &[
    // Americas
    (Currency::USD, 1.0),
    (Currency::CAD, 1.36),
    (Currency::MXN, 17.15),
    (Currency::BRL, 4.97),
    (Currency::ARS, 350.0),
    // Europe
    (Currency::EUR, 0.92),
    (Currency::GBP, 0.79),
    (Currency::CHF, 0.88),
    (Currency::SEK, 10.42),
    (Currency::NOK, 10.67),
    (Currency::DKK, 6.87),
    (Currency::RUB, 92.0),
    (Currency::PLN, 3.98),
    // Asia
    (Currency::CNY, 7.24),
    (Currency::JPY, 149.50),
    (Currency::KRW, 1320.0),
    (Currency::INR, 83.12),
    (Currency::HKD, 7.82),
    (Currency::SGD, 1.34),
    (Currency::TWD, 31.85),
    (Currency::THB, 35.15),
];

/// Get exchange rate from USD
fn get_rate_from_usd(currency: Currency) -> f64 {
    EXCHANGE_RATES_USD
        .iter()
        .find(|(c, _)| *c == currency)
        .map(|(_, rate)| *rate)
        .unwrap_or(1.0)
}

/// Get exchange rate to USD
fn get_rate_to_usd(currency: Currency) -> f64 {
    1.0 / get_rate_from_usd(currency)
}

/// Main currency utilities struct
#[derive(Debug, Clone)]
pub struct CurrencyUtils {
    format_options: FormatOptions,
}

impl Default for CurrencyUtils {
    fn default() -> Self {
        Self::new()
    }
}

impl CurrencyUtils {
    /// Create a new CurrencyUtils with default format options
    pub fn new() -> Self {
        Self {
            format_options: FormatOptions::default(),
        }
    }

    /// Create with custom format options
    pub fn with_options(options: FormatOptions) -> Self {
        Self {
            format_options: options,
        }
    }

    /// Set format options
    pub fn set_format_options(&mut self, options: FormatOptions) {
        self.format_options = options;
    }

    /// Format a currency amount
    pub fn format(&self, amount: f64, currency: Currency) -> String {
        self.format_with_options(amount, currency, &self.format_options)
    }

    /// Format with custom options
    pub fn format_with_options(&self, amount: f64, currency: Currency, options: &FormatOptions) -> String {
        let is_negative = amount < 0.0;
        let abs_amount = amount.abs();
        
        let decimal_places = options.decimal_places.unwrap_or_else(|| currency.decimal_places());
        let decimal_sep = currency.decimal_separator();
        let thousands_sep = currency.thousands_separator();

        // Format the number with proper decimal places
        let formatted_number = if options.use_thousands_separator {
            self.format_number_with_separators(abs_amount, decimal_places, decimal_sep, thousands_sep)
        } else {
            format!("{:.1$}", abs_amount, decimal_places as usize)
        };

        // Build the result string
        let mut result = String::new();

        if is_negative && options.parentheses_for_negative {
            result.push('(');
        } else if is_negative {
            result.push('-');
        }

        // Add symbol before or after
        if options.include_symbol && currency.symbol_before() {
            result.push_str(currency.symbol());
        }

        result.push_str(&formatted_number);

        if options.include_symbol && !currency.symbol_before() {
            result.push(' ');
            result.push_str(currency.symbol());
        }

        if options.include_code {
            result.push_str(" ");
            result.push_str(currency.code());
        }

        if is_negative && options.parentheses_for_negative {
            result.push(')');
        }

        result
    }

    /// Format number with thousands separators
    fn format_number_with_separators(&self, amount: f64, decimal_places: u8, decimal_sep: char, thousands_sep: char) -> String {
        let scaled = amount * 10_f64.powi(decimal_places as i32);
        let rounded = scaled.round() as i64;
        let pow_factor = 10_i64.pow(decimal_places as u32);
        let int_part = rounded / pow_factor;
        let dec_part = (rounded % pow_factor).abs();

        // Format integer part with thousands separators
        let int_str = int_part.to_string();
        let mut formatted_int = String::new();
        
        for (i, c) in int_str.chars().rev().enumerate() {
            if i > 0 && i % 3 == 0 {
                formatted_int.push(thousands_sep);
            }
            formatted_int.push(c);
        }
        
        let formatted_int: String = formatted_int.chars().rev().collect();

        if decimal_places > 0 {
            format!("{}{}{:0width$}", formatted_int, decimal_sep, dec_part, width = decimal_places as usize)
        } else {
            formatted_int
        }
    }

    /// Convert amount from one currency to another
    pub fn convert(&self, amount: f64, from: Currency, to: Currency) -> f64 {
        if from == to {
            return amount;
        }

        // Convert to USD first, then to target currency
        let usd_amount = amount * get_rate_to_usd(from);
        usd_amount * get_rate_from_usd(to)
    }

    /// Convert and format in one step
    pub fn convert_and_format(&self, amount: f64, from: Currency, to: Currency) -> String {
        let converted = self.convert(amount, from, to);
        self.format(converted, to)
    }

    /// Parse a currency string like "$1,234.56" or "€500"
    pub fn parse(&self, s: &str) -> Result<Money, CurrencyError> {
        parse_money(s)
    }

    /// Add two money values (returns result in first currency)
    pub fn add(&self, m1: Money, m2: Money) -> Money {
        let m2_converted = m2.convert_to(m1.currency, self);
        Money::new(m1.amount + m2_converted.amount, m1.currency)
    }

    /// Subtract money values (returns result in first currency)
    pub fn subtract(&self, m1: Money, m2: Money) -> Money {
        let m2_converted = m2.convert_to(m1.currency, self);
        Money::new(m1.amount - m2_converted.amount, m1.currency)
    }

    /// Multiply money by a factor
    pub fn multiply(&self, money: Money, factor: f64) -> Money {
        Money::new(money.amount * factor, money.currency)
    }

    /// Divide money by a factor
    pub fn divide(&self, money: Money, divisor: f64) -> Result<Money, CurrencyError> {
        if divisor == 0.0 {
            return Err(CurrencyError::InvalidAmount("Division by zero".to_string()));
        }
        Ok(Money::new(money.amount / divisor, money.currency))
    }

    /// Calculate percentage of money
    pub fn percentage(&self, money: Money, percent: f64) -> Money {
        Money::new(money.amount * percent / 100.0, money.currency)
    }

    /// Compare two money values
    pub fn compare(&self, m1: Money, m2: Money) -> std::cmp::Ordering {
        let m2_converted = m2.convert_to(m1.currency, self);
        m1.amount.partial_cmp(&m2_converted.amount).unwrap_or(std::cmp::Ordering::Equal)
    }

    /// Check if two money values are equal
    pub fn equal(&self, m1: Money, m2: Money) -> bool {
        self.compare(m1, m2) == std::cmp::Ordering::Equal
    }

    /// Check if m1 is less than m2
    pub fn less_than(&self, m1: Money, m2: Money) -> bool {
        self.compare(m1, m2) == std::cmp::Ordering::Less
    }

    /// Check if m1 is greater than m2
    pub fn greater_than(&self, m1: Money, m2: Money) -> bool {
        self.compare(m1, m2) == std::cmp::Ordering::Greater
    }

    /// Calculate sum of multiple money values (returns in specified currency)
    pub fn sum(&self, amounts: &[Money], result_currency: Currency) -> Money {
        let total: f64 = amounts
            .iter()
            .map(|m| m.convert_to(result_currency, self).amount)
            .sum();
        Money::new(total, result_currency)
    }

    /// Calculate average of multiple money values
    pub fn average(&self, amounts: &[Money], result_currency: Currency) -> Option<Money> {
        if amounts.is_empty() {
            return None;
        }
        let sum = self.sum(amounts, result_currency);
        Some(Money::new(sum.amount / amounts.len() as f64, result_currency))
    }

    /// Find minimum
    pub fn min(&self, amounts: &[Money]) -> Option<Money> {
        amounts.iter().min_by(|a, b| self.compare(**a, **b)).copied()
    }

    /// Find maximum
    pub fn max(&self, amounts: &[Money]) -> Option<Money> {
        amounts.iter().max_by(|a, b| self.compare(**a, **b)).copied()
    }

    /// Round to currency's decimal places
    pub fn round(&self, money: Money) -> Money {
        let places = money.currency.decimal_places();
        let factor = 10_f64.powi(places as i32);
        Money::new((money.amount * factor).round() / factor, money.currency)
    }

    /// Round up to currency's decimal places
    pub fn round_up(&self, money: Money) -> Money {
        let places = money.currency.decimal_places();
        let factor = 10_f64.powi(places as i32);
        Money::new((money.amount * factor).ceil() / factor, money.currency)
    }

    /// Round down to currency's decimal places
    pub fn round_down(&self, money: Money) -> Money {
        let places = money.currency.decimal_places();
        let factor = 10_f64.powi(places as i32);
        Money::new((money.amount * factor).floor() / factor, money.currency)
    }

    /// Check if amount is zero
    pub fn is_zero(&self, money: Money) -> bool {
        money.amount == 0.0
    }

    /// Check if amount is positive
    pub fn is_positive(&self, money: Money) -> bool {
        money.amount > 0.0
    }

    /// Check if amount is negative
    pub fn is_negative(&self, money: Money) -> bool {
        money.amount < 0.0
    }

    /// Get absolute value
    pub fn abs(&self, money: Money) -> Money {
        Money::new(money.amount.abs(), money.currency)
    }

    /// Negate
    pub fn negate(&self, money: Money) -> Money {
        Money::new(-money.amount, money.currency)
    }

    /// Get all supported currencies with their current rates
    pub fn get_all_rates(&self) -> Vec<(Currency, f64)> {
        EXCHANGE_RATES_USD.to_vec()
    }

    /// Get exchange rate between two currencies
    pub fn get_exchange_rate(&self, from: Currency, to: Currency) -> f64 {
        get_rate_to_usd(from) * get_rate_from_usd(to)
    }

    /// Format amount as words (English)
    pub fn format_as_words(&self, money: Money) -> String {
        let amount = money.amount;
        let currency = money.currency;
        
        let int_part = amount.trunc().abs() as i64;
        let dec_part = ((amount.fract().abs() * 100.0).round()) as i64;
        
        let int_words = self.number_to_words(int_part);
        let currency_name = if int_part == 1 { currency.name().replace("Dollar", "Dollar") } else { format!("{}s", currency.name()) };
        
        if currency.decimal_places() == 0 {
            return format!("{} {}", int_words, currency_name);
        }
        
        let cent_name = if dec_part == 1 { "cent" } else { "cents" };
        
        if dec_part == 0 {
            format!("{} {}", int_words, currency_name)
        } else {
            format!("{} {} and {} {}", int_words, currency_name, dec_part, cent_name)
        }
    }

    /// Convert number to words (supports up to trillions)
    fn number_to_words(&self, num: i64) -> String {
        if num == 0 {
            return "zero".to_string();
        }

        let ones = ["", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine",
                    "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen",
                    "seventeen", "eighteen", "nineteen"];
        let tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"];

        fn convert_hundreds(n: i64, ones: &[&str], tens: &[&str]) -> String {
            if n == 0 {
                return String::new();
            }
            
            let mut result = String::new();
            
            if n >= 100 {
                result.push_str(ones[(n / 100) as usize]);
                result.push_str(" hundred");
                if n % 100 > 0 {
                    result.push_str(" ");
                }
            }
            
            let remainder = n % 100;
            if remainder > 0 {
                if remainder < 20 {
                    result.push_str(ones[remainder as usize]);
                } else {
                    result.push_str(tens[(remainder / 10) as usize]);
                    if remainder % 10 > 0 {
                        result.push_str("-");
                        result.push_str(ones[(remainder % 10) as usize]);
                    }
                }
            }
            
            result
        }

        let mut result = String::new();
        let mut remaining = num;

        // Billions
        if remaining >= 1_000_000_000 {
            let billions = remaining / 1_000_000_000;
            result.push_str(&convert_hundreds(billions, &ones, &tens));
            result.push_str(" billion");
            remaining %= 1_000_000_000;
            if remaining > 0 {
                result.push_str(" ");
            }
        }

        // Millions
        if remaining >= 1_000_000 {
            let millions = remaining / 1_000_000;
            result.push_str(&convert_hundreds(millions, &ones, &tens));
            result.push_str(" million");
            remaining %= 1_000_000;
            if remaining > 0 {
                result.push_str(" ");
            }
        }

        // Thousands
        if remaining >= 1_000 {
            let thousands = remaining / 1_000;
            result.push_str(&convert_hundreds(thousands, &ones, &tens));
            result.push_str(" thousand");
            remaining %= 1_000;
            if remaining > 0 {
                result.push_str(" ");
            }
        }

        // Remaining
        if remaining > 0 {
            result.push_str(&convert_hundreds(remaining, &ones, &tens));
        }

        result
    }
}

/// Parse a money string like "$1,234.56" or "€500"
pub fn parse_money(s: &str) -> Result<Money, CurrencyError> {
    let s = s.trim();
    
    // Try to extract currency and amount
    let mut currency: Option<Currency> = None;
    let mut amount_str = String::new();
    
    // Check for currency symbols at start
    for curr in Currency::all() {
        let symbol = curr.symbol();
        if s.starts_with(symbol) {
            currency = Some(curr);
            amount_str = s[symbol.len()..].to_string();
            break;
        }
    }
    
    // If no symbol found, try to find currency code
    if currency.is_none() {
        // Check for code at end (e.g., "100 USD")
        for curr in Currency::all() {
            if s.ends_with(curr.code()) {
                currency = Some(curr);
                amount_str = s[..s.len() - curr.code().len()].to_string();
                break;
            }
        }
    }
    
    // If still no currency, default to USD
    if currency.is_none() {
        amount_str = s.to_string();
        currency = Some(Currency::USD);
    }
    
    // Clean up the amount string
    let clean_amount: String = amount_str
        .chars()
        .filter(|c| c.is_ascii_digit() || *c == '.' || *c == '-' || *c == ',')
        .collect();
    
    // Remove thousands separators (commas)
    let clean_amount = clean_amount.replace(",", "");
    
    let amount: f64 = clean_amount
        .parse()
        .map_err(|_| CurrencyError::ParseError(s.to_string()))?;
    
    Ok(Money::new(amount, currency.unwrap()))
}

/// Check if a string is a valid currency
pub fn is_valid_currency(s: &str) -> bool {
    Currency::from_str(s).is_ok()
}

/// Get all supported currencies
pub fn get_supported_currencies() -> Vec<Currency> {
    Currency::all()
}

#[cfg(test)]
mod tests {
    use super::*;

    const EPSILON: f64 = 0.01;

    fn approx_eq(a: f64, b: f64) -> bool {
        (a - b).abs() < EPSILON
    }

    #[test]
    fn test_currency_properties() {
        assert_eq!(Currency::USD.code(), "USD");
        assert_eq!(Currency::USD.symbol(), "$");
        assert_eq!(Currency::USD.name(), "US Dollar");
        assert_eq!(Currency::USD.decimal_places(), 2);
        
        assert_eq!(Currency::JPY.decimal_places(), 0);
        assert_eq!(Currency::KRW.decimal_places(), 0);
    }

    #[test]
    fn test_format_usd() {
        let utils = CurrencyUtils::new();
        
        assert_eq!(utils.format(1234.56, Currency::USD), "$1,234.56");
        assert_eq!(utils.format(0.0, Currency::USD), "$0.00");
        assert_eq!(utils.format(-1234.56, Currency::USD), "-$1,234.56");
    }

    #[test]
    fn test_format_jpy() {
        let utils = CurrencyUtils::new();
        
        // JPY has no decimal places
        let formatted = utils.format(1234567.0, Currency::JPY);
        assert!(formatted.contains("1,234,567"));
        assert!(formatted.contains("¥"));
    }

    #[test]
    fn test_format_eur() {
        let utils = CurrencyUtils::new();
        
        // EUR uses comma as decimal separator
        let formatted = utils.format(1234.56, Currency::EUR);
        assert!(formatted.contains("1.234,56") || formatted.contains("1234,56"));
    }

    #[test]
    fn test_format_options() {
        let utils = CurrencyUtils::new();
        
        // Without symbol
        let options = FormatOptions::new().with_symbol(false);
        let formatted = utils.format_with_options(1234.56, Currency::USD, &options);
        assert_eq!(formatted, "1,234.56");
        
        // With code
        let options = FormatOptions::new().with_code(true);
        let formatted = utils.format_with_options(1234.56, Currency::USD, &options);
        assert!(formatted.contains("USD"));
        
        // Without thousands separator
        let options = FormatOptions::new().with_thousands_separator(false);
        let formatted = utils.format_with_options(1234.56, Currency::USD, &options);
        assert_eq!(formatted, "$1234.56");
        
        // Parentheses for negative
        let options = FormatOptions::new().with_parentheses_for_negative(true);
        let formatted = utils.format_with_options(-1234.56, Currency::USD, &options);
        assert!(formatted.starts_with("($") && formatted.ends_with(")"));
    }

    #[test]
    fn test_convert_usd_to_eur() {
        let utils = CurrencyUtils::new();
        
        // $100 should convert to approximately €92
        let eur = utils.convert(100.0, Currency::USD, Currency::EUR);
        assert!(approx_eq(eur, 92.0));
    }

    #[test]
    fn test_convert_usd_to_cny() {
        let utils = CurrencyUtils::new();
        
        // $100 should convert to approximately ¥724
        let cny = utils.convert(100.0, Currency::USD, Currency::CNY);
        assert!(approx_eq(cny, 724.0));
    }

    #[test]
    fn test_convert_jpy_to_usd() {
        let utils = CurrencyUtils::new();
        
        // ¥14950 should convert to approximately $100
        let usd = utils.convert(14950.0, Currency::JPY, Currency::USD);
        assert!(approx_eq(usd, 100.0));
    }

    #[test]
    fn test_convert_same_currency() {
        let utils = CurrencyUtils::new();
        
        // Same currency should return same amount
        let result = utils.convert(100.0, Currency::USD, Currency::USD);
        assert_eq!(result, 100.0);
    }

    #[test]
    fn test_parse_usd() {
        let money: Money = "$1,234.56".parse().unwrap();
        assert_eq!(money.amount, 1234.56);
        assert_eq!(money.currency, Currency::USD);
    }

    #[test]
    fn test_parse_eur() {
        let money: Money = "€500".parse().unwrap();
        assert_eq!(money.amount, 500.0);
        assert_eq!(money.currency, Currency::EUR);
    }

    #[test]
    fn test_parse_with_code() {
        let money: Money = "100 JPY".parse().unwrap();
        assert_eq!(money.amount, 100.0);
        assert_eq!(money.currency, Currency::JPY);
    }

    #[test]
    fn test_parse_negative() {
        let money: Money = "-$500".parse().unwrap();
        assert_eq!(money.amount, -500.0);
        assert_eq!(money.currency, Currency::USD);
    }

    #[test]
    fn test_money_creation() {
        let usd = Money::usd(100.0);
        assert_eq!(usd.amount, 100.0);
        assert_eq!(usd.currency, Currency::USD);
        
        let eur = Money::eur(100.0);
        assert_eq!(eur.currency, Currency::EUR);
        
        let cny = Money::cny(100.0);
        assert_eq!(cny.currency, Currency::CNY);
    }

    #[test]
    fn test_money_arithmetic() {
        let utils = CurrencyUtils::new();
        
        let m1 = Money::usd(100.0);
        let m2 = Money::usd(50.0);
        
        let sum = utils.add(m1, m2);
        assert_eq!(sum.amount, 150.0);
        
        let diff = utils.subtract(m1, m2);
        assert_eq!(diff.amount, 50.0);
        
        let doubled = utils.multiply(m1, 2.0);
        assert_eq!(doubled.amount, 200.0);
        
        let half = utils.divide(m1, 2.0).unwrap();
        assert_eq!(half.amount, 50.0);
    }

    #[test]
    fn test_money_cross_currency_arithmetic() {
        let utils = CurrencyUtils::new();
        
        let usd = Money::usd(100.0);
        let eur = Money::eur(92.0); // ≈ $100
        
        let sum = utils.add(usd, eur);
        assert_eq!(sum.currency, Currency::USD);
        assert!(sum.amount > 190.0); // Should be ~$200
    }

    #[test]
    fn test_money_comparison() {
        let utils = CurrencyUtils::new();
        
        let m1 = Money::usd(100.0);
        let m2 = Money::usd(200.0);
        let m3 = Money::usd(100.0);
        
        assert!(utils.less_than(m1, m2));
        assert!(utils.greater_than(m2, m1));
        assert!(utils.equal(m1, m3));
    }

    #[test]
    fn test_money_aggregation() {
        let utils = CurrencyUtils::new();
        
        let amounts = [
            Money::usd(100.0),
            Money::usd(200.0),
            Money::usd(300.0),
        ];
        
        let sum = utils.sum(&amounts, Currency::USD);
        assert_eq!(sum.amount, 600.0);
        
        let avg = utils.average(&amounts, Currency::USD).unwrap();
        assert_eq!(avg.amount, 200.0);
        
        let min = utils.min(&amounts).unwrap();
        assert_eq!(min.amount, 100.0);
        
        let max = utils.max(&amounts).unwrap();
        assert_eq!(max.amount, 300.0);
    }

    #[test]
    fn test_money_rounding() {
        let utils = CurrencyUtils::new();
        
        let money = Money::usd(123.456);
        let rounded = utils.round(money);
        assert_eq!(rounded.amount, 123.46);
        
        let rounded_up = utils.round_up(money);
        assert_eq!(rounded_up.amount, 123.46);
        
        let rounded_down = utils.round_down(money);
        assert_eq!(rounded_down.amount, 123.45);
    }

    #[test]
    fn test_money_sign_checks() {
        let utils = CurrencyUtils::new();
        
        assert!(utils.is_positive(Money::usd(100.0)));
        assert!(utils.is_negative(Money::usd(-100.0)));
        assert!(utils.is_zero(Money::usd(0.0)));
    }

    #[test]
    fn test_money_abs_negate() {
        let utils = CurrencyUtils::new();
        
        let negative = Money::usd(-100.0);
        let positive = utils.abs(negative);
        assert_eq!(positive.amount, 100.0);
        
        let negated = utils.negate(Money::usd(100.0));
        assert_eq!(negated.amount, -100.0);
    }

    #[test]
    fn test_percentage() {
        let utils = CurrencyUtils::new();
        
        let money = Money::usd(200.0);
        let ten_percent = utils.percentage(money, 10.0);
        assert_eq!(ten_percent.amount, 20.0);
    }

    #[test]
    fn test_format_as_words() {
        let utils = CurrencyUtils::new();
        
        let money = Money::usd(123.45);
        let words = utils.format_as_words(money);
        assert!(words.contains("one hundred twenty-three"));
        assert!(words.contains("Dollar"));
        assert!(words.contains("cent"));
        
        let zero = Money::usd(0.0);
        let words = utils.format_as_words(zero);
        assert!(words.contains("zero"));
    }

    #[test]
    fn test_number_to_words() {
        let utils = CurrencyUtils::new();
        
        assert_eq!(utils.number_to_words(0), "zero");
        assert_eq!(utils.number_to_words(1), "one");
        assert_eq!(utils.number_to_words(15), "fifteen");
        assert_eq!(utils.number_to_words(42), "forty-two");
        assert_eq!(utils.number_to_words(100), "one hundred");
        assert_eq!(utils.number_to_words(123), "one hundred twenty-three");
        assert_eq!(utils.number_to_words(1000), "one thousand");
        assert_eq!(utils.number_to_words(1234), "one thousand two hundred thirty-four");
        assert_eq!(utils.number_to_words(1000000), "one million");
        assert_eq!(utils.number_to_words(1000000000), "one billion");
    }

    #[test]
    fn test_get_exchange_rate() {
        let utils = CurrencyUtils::new();
        
        let rate = utils.get_exchange_rate(Currency::USD, Currency::EUR);
        assert!(approx_eq(rate, 0.92));
        
        let rate_inverse = utils.get_exchange_rate(Currency::EUR, Currency::USD);
        assert!(approx_eq(rate_inverse, 1.0 / 0.92));
    }

    #[test]
    fn test_all_currencies() {
        let all = Currency::all();
        assert_eq!(all.len(), 21);
    }

    #[test]
    fn test_currency_from_code_or_symbol() {
        assert_eq!(Currency::from_code_or_symbol("USD"), Some(Currency::USD));
        assert_eq!(Currency::from_code_or_symbol("$"), Some(Currency::USD));
        assert_eq!(Currency::from_code_or_symbol("EUR"), Some(Currency::EUR));
        assert_eq!(Currency::from_code_or_symbol("€"), Some(Currency::EUR));
        assert_eq!(Currency::from_code_or_symbol("invalid"), None);
    }

    #[test]
    fn test_convert_and_format() {
        let utils = CurrencyUtils::new();
        
        let result = utils.convert_and_format(100.0, Currency::USD, Currency::EUR);
        assert!(result.contains("€") || result.contains("EUR"));
    }

    #[test]
    fn test_large_numbers() {
        let utils = CurrencyUtils::new();
        
        let formatted = utils.format(1234567890.12, Currency::USD);
        assert!(formatted.contains("1,234,567,890"));
        
        let words = utils.format_as_words(Money::usd(1234567890.0));
        assert!(words.contains("billion"));
    }

    #[test]
    fn test_japanese_yen_formatting() {
        let utils = CurrencyUtils::new();
        
        // JPY has no decimal places
        let jpy = Money::jpy(12345.0);
        let formatted = jpy.format();
        assert!(formatted.contains("12,345"));
        assert!(!formatted.contains(".")); // No decimal point
    }
}