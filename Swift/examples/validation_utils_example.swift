import Foundation

// Example 1: String Validation
print("=== String Validation ===")
let userInput = "   "
if ValidationUtils.isBlank(userInput) {
    print("Input is required!")
}

let username = "john_doe"
if ValidationUtils.lengthBetween(username, min: 3, max: 20) {
    print("Username '\(username)' length is valid")
}

let code = "ABC123"
if ValidationUtils.isAlphanumeric(code) {
    print("'\(code)' is alphanumeric")
}

// Example 2: Email Validation
print("\n=== Email Validation ===")
let emails = ["user@example.com", "invalid.email", "@nodomain.com"]
for email in emails {
    let isValid = ValidationUtils.isValidEmail(email)
    print("\(email): \(isValid ? "Valid" : "Invalid")")
}

// Example 3: URL Validation
print("\n=== URL Validation ===")
let urls = ["https://www.example.com", "example.com", "not a url"]
for url in urls {
    let isValid = ValidationUtils.isValidURL(url)
    let isValidNoScheme = ValidationUtils.isValidURL(url, requireScheme: false)
    print("\(url): strict=\(isValid), relaxed=\(isValidNoScheme)")
}

// Example 4: Phone Number Validation
print("\n=== Phone Number Validation ===")
print("US phone '1234567890': \(ValidationUtils.isValidUSPhone("1234567890") ? "Valid" : "Invalid")")
print("China mobile '13800138000': \(ValidationUtils.isValidChinaMobile("13800138000") ? "Valid" : "Invalid")")

// Example 5: IP Address Validation
print("\n=== IP Address Validation ===")
let ips = ["192.168.1.1", "256.1.1.1", "::1"]
for ip in ips {
    let isV4 = ValidationUtils.isValidIPv4(ip)
    let isV6 = ValidationUtils.isValidIPv6(ip)
    print("\(ip): IPv4=\(isV4), IPv6=\(isV6)")
}

// Example 6: Credit Card Validation
print("\n=== Credit Card Validation ===")
let cards = [
    ("4532015112830366", "Visa"),
    ("5425233430109903", "Mastercard"),
    ("4532015112830367", "Invalid")
]
for (card, type) in cards {
    let isValid = ValidationUtils.isValidCreditCard(card)
    print("\(type): \(isValid ? "Valid" : "Invalid")")
}

// Example 7: UUID Validation
print("\n=== UUID Validation ===")
let uuid = "550e8400-e29b-41d4-a716-446655440000"
print("Standard UUID '\(uuid)': \(ValidationUtils.isValidUUID(uuid) ? "Valid" : "Invalid")")

// Example 8: Password Strength
print("\n=== Password Strength ===")
let passwords = ["StrongP@ss123", "weak", "nouppercase123!"]
for password in passwords {
    let strength = ValidationUtils.checkPasswordStrength(password)
    print("'\(password)': \(strength.strength.description)")
}

// Example 9: Hex Color Validation
print("\n=== Hex Color Validation ===")
let colors = ["#FF5733", "#F53", "#GG5733"]
for color in colors {
    let isValid = ValidationUtils.isValidHexColor(color)
    print("\(color): \(isValid ? "Valid" : "Invalid")")
}

// Example 10: MAC Address Validation
print("\n=== MAC Address Validation ===")
let mac = "00:1A:2B:3C:4D:5E"
print("MAC '\(mac)': \(ValidationUtils.isValidMACAddress(mac) ? "Valid" : "Invalid")")

// Example 11: Date Validation
print("\n=== Date Validation ===")
let dates = ["2024-03-15", "2024-13-15"]
for date in dates {
    let isValid = ValidationUtils.isValidDate(date)
    print("\(date): \(isValid ? "Valid" : "Invalid")")
}

// Example 12: Numeric Validation
print("\n=== Numeric Validation ===")
print("Is '123' an integer? \(ValidationUtils.isValidInteger("123"))")
print("Is '3.14' a float? \(ValidationUtils.isValidFloat("3.14"))")
print("Is 5 between 1 and 10? \(ValidationUtils.between(5, min: 1, max: 10))")

print("\nAll examples completed!")
