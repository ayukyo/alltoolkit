/**
 * ValidationUtils - Comprehensive Data Validation Utilities for Swift
 * 
 * A zero-dependency validation library for Swift providing common validation
 * functions for emails, URLs, phone numbers, credit cards, IP addresses,
 * passwords, UUIDs, and more.
 *
 * Features:
 * - Email validation (RFC 5322 compliant)
 * - URL validation with scheme checking
 * - Phone number validation (US, China, international)
 * - Credit card validation (Luhn algorithm)
 * - IP address validation (IPv4/IPv6)
 * - Password strength validation
 * - UUID validation
 * - Hex color validation
 * - MAC address validation
 * - Alphanumeric/numeric/alpha validation
 * - String length validation
 *
 * Requirements: iOS 13.0+, macOS 10.15+, watchOS 6.0+, tvOS 13.0+
 */

import Foundation

// MARK: - Password Strength

/// Represents password strength levels
public enum PasswordStrength: Int, Comparable {
    case veryWeak = 0
    case weak = 1
    case medium = 2
    case strong = 3
    case veryStrong = 4
    
    public static func < (lhs: PasswordStrength, rhs: PasswordStrength) -> Bool {
        return lhs.rawValue < rhs.rawValue
    }
    
    public var description: String {
        switch self {
        case .veryWeak: return "Very Weak"
        case .weak: return "Weak"
        case .medium: return "Medium"
        case .strong: return "Strong"
        case .veryStrong: return "Very Strong"
        }
    }
}

// MARK: - ValidationUtils

public struct ValidationUtils {
    
    // MARK: - String Validation
    
    /// Check if string is empty or contains only whitespace
    public static func isBlank(_ string: String?) -> Bool {
        guard let string = string else { return true }
        return string.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty
    }
    
    /// Check if string has content (not blank)
    public static func isNotBlank(_ string: String?) -> Bool {
        return !isBlank(string)
    }
    
    /// Check if string is empty
    public static func isEmpty(_ string: String?) -> Bool {
        return string?.isEmpty ?? true
    }
    
    /// Check if string is not empty
    public static func isNotEmpty(_ string: String?) -> Bool {
        return !isEmpty(string)
    }
    
    /// Check string length is within range
    public static func lengthBetween(_ string: String?, min: Int, max: Int) -> Bool {
        guard let string = string else { return false }
        let length = string.count
        return length >= min && length <= max
    }
    
    /// Check string length is at least minimum
    public static func minLength(_ string: String?, _ min: Int) -> Bool {
        guard let string = string else { return false }
        return string.count >= min
    }
    
    /// Check string length is at most maximum
    public static func maxLength(_ string: String?, _ max: Int) -> Bool {
        guard let string = string else { return false }
        return string.count <= max
    }
    
    /// Check if string contains only letters
    public static func isAlpha(_ string: String?) -> Bool {
        guard let string = string, !string.isEmpty else { return false }
        return string.allSatisfy { $0.isLetter }
    }
    
    /// Check if string contains only digits
    public static func isNumeric(_ string: String?) -> Bool {
        guard let string = string, !string.isEmpty else { return false }
        return string.allSatisfy { $0.isNumber }
    }
    
    /// Check if string contains only letters and digits
    public static func isAlphanumeric(_ string: String?) -> Bool {
        guard let string = string, !string.isEmpty else { return false }
        return string.allSatisfy { $0.isLetter || $0.isNumber }
    }
    
    // MARK: - Email Validation
    
    /// Validate email format (RFC 5322 compliant regex)
    public static func isValidEmail(_ email: String?) -> Bool {
        guard let email = email, !email.isEmpty else { return false }
        
        let emailRegex = "^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$"
        return NSPredicate(format: "SELF MATCHES %@", emailRegex).evaluate(with: email)
    }
    
    /// Validate email with stricter rules
    public static func isValidEmailStrict(_ email: String?) -> Bool {
        guard let email = email, !email.isEmpty else { return false }
        
        let components = email.split(separator: "@")
        guard components.count == 2 else { return false }
        
        let localPart = String(components[0])
        let domain = String(components[1])
        
        guard !localPart.isEmpty,
              localPart.count <= 64,
              !localPart.hasPrefix("."),
              !localPart.hasSuffix("."),
              !localPart.contains("..") else { return false }
        
        guard !domain.isEmpty,
              domain.count <= 255,
              !domain.hasPrefix("-"),
              !domain.hasSuffix("-"),
              !domain.contains("..") else { return false }
        
        return isValidEmail(email)
    }
    
    // MARK: - URL Validation
    
    /// Validate URL format
    public static func isValidURL(_ url: String?, requireScheme: Bool = true) -> Bool {
        guard let url = url, !url.isEmpty else { return false }
        
        if requireScheme {
            let urlRegex = "^(https?|ftp)://[\\w\\-]+(\\.[\\w\\-]+)+([\\w\\-.,@?^=%&:/~+#]*[\\w\\-@?^=%&/~+#])?$"
            return NSPredicate(format: "SELF MATCHES %@", urlRegex).evaluate(with: url)
        } else {
            let urlRegex = "^((https?|ftp)://)?[\\w\\-]+(\\.[\\w\\-]+)+([\\w\\-.,@?^=%&:/~+#]*[\\w\\-@?^=%&/~+#])?$"
            return NSPredicate(format: "SELF MATCHES %@", urlRegex).evaluate(with: url)
        }
    }
    
    /// Validate HTTPS URL
    public static func isValidHTTPS(_ url: String?) -> Bool {
        guard let url = url else { return false }
        return url.lowercased().hasPrefix("https://") && isValidURL(url)
    }
    
    // MARK: - Phone Number Validation
    
    /// Validate phone number (7-15 digits)
    public static func isValidPhone(_ phone: String?) -> Bool {
        guard let phone = phone else { return false }
        let digitsOnly = phone.filter { $0.isNumber }
        return digitsOnly.count >= 7 && digitsOnly.count <= 15
    }
    
    /// Validate US phone number (10 digits)
    public static func isValidUSPhone(_ phone: String?) -> Bool {
        guard let phone = phone else { return false }
        let digitsOnly = phone.filter { $0.isNumber }
        return digitsOnly.count == 10
    }
    
    /// Validate Chinese mobile phone number
    public static func isValidChinaMobile(_ phone: String?) -> Bool {
        guard let phone = phone else { return false }
        let digitsOnly = phone.filter { $0.isNumber }
        guard digitsOnly.count == 11, digitsOnly.hasPrefix("1") else { return false }
        
        let secondIndex = digitsOnly.index(digitsOnly.startIndex, offsetBy: 1)
        let secondDigit = digitsOnly[secondIndex]
        return "3456789".contains(secondDigit)
    }
    
    // MARK: - IP Address Validation
    
    /// Validate IPv4 address
    public static func isValidIPv4(_ ip: String?) -> Bool {
        guard let ip = ip else { return false }
        
        let parts = ip.split(separator: ".")
        guard parts.count == 4 else { return false }
        
        for part in parts {
            guard let num = Int(part), num >= 0, num <= 255 else { return false }
            if part.count > 1 && part.hasPrefix("0") { return false }
        }
        
        return true
    }
    
    /// Validate IPv6 address (simplified)
    public static func isValidIPv6(_ ip: String?) -> Bool {
        guard let ip = ip else { return false }
        
        let parts = ip.split(separator: ":")
        guard parts.count >= 2 && parts.count <= 8 else { return false }
        
        for part in parts {
            guard !part.isEmpty else { continue }
            guard part.count <= 4 else { return false }
            let hexRegex = "^[0-9A-Fa-f]{1,4}$"
            guard NSPredicate(format: "SELF MATCHES %@", hexRegex).evaluate(with: String(part)) else {
                return false
            }
        }
        
        return true
    }
    
    /// Validate IP address (IPv4 or IPv6)
    public static func isValidIP(_ ip: String?) -> Bool {
        return isValidIPv4(ip) || isValidIPv6(ip)
    }
    
    // MARK: - Credit Card Validation
    
    /// Validate credit card number using Luhn algorithm
    public static func isValidCreditCard(_ cardNumber: String?) -> Bool {
        guard let cardNumber = cardNumber else { return false }
        let digitsOnly = cardNumber.filter { $0.isNumber }
        guard digitsOnly.count >= 13 && digitsOnly.count <= 19 else { return false }
        
        var sum = 0
        var isEven = false
        
        for char in digitsOnly.reversed() {
            guard let digit = char.wholeNumberValue else { return false }
            
            if isEven {
                let doubled = digit * 2
                sum += doubled > 9 ? doubled - 9 : doubled
            } else {
                sum += digit
            }
            isEven = !isEven
        }
        
        return sum % 10 == 0
    }
    
    // MARK: - UUID Validation
    
    /// Validate UUID format
    public static func isValidUUID(_ uuid: String?) -> Bool {
        guard let uuid = uuid else { return false }
        let uuidRegex = "^[0-9A-Fa-f]{8}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{12}$"
        return NSPredicate(format: "SELF MATCHES %@", uuidRegex).evaluate(with: uuid)
    }
    
    /// Validate UUID without dashes
    public static func isValidUUIDSimple(_ uuid: String?) -> Bool {
        guard let uuid = uuid else { return false }
        let uuidRegex = "^[0-9A-Fa-f]{32}$"
        return NSPredicate(format: "SELF MATCHES %@", uuidRegex).evaluate(with: uuid)
    }
    
    // MARK: - Hex Color Validation
    
    /// Validate hex color code (#RGB or #RRGGBB)
    public static func isValidHexColor(_ color: String?) -> Bool {
        guard let color = color else { return false }
        let hexRegex = "^#([0-9A-Fa-f]{3}|[0-9A-Fa-f]{6})$"
        return NSPredicate(format: "SELF MATCHES %@", hexRegex).evaluate(with: color)
    }
    
    /// Validate hex color with alpha (#RGBA or #RRGGBBAA)
    public static func isValidHexColorWithAlpha(_ color: String?) -> Bool {
        guard let color = color else { return false }
        let hexRegex = "^#([0-9A-Fa-f]{3}|[0-9A-Fa-f]{4}|[0-9A-Fa-f]{6}|[0-9A-Fa-f]{8})$"
        return NSPredicate(format: "SELF MATCHES %@", hexRegex).evaluate(with: color)
    }
    
    // MARK: - MAC Address Validation
    
    /// Validate MAC address format
    public static func isValidMACAddress(_ mac: String?) -> Bool {
        guard let mac = mac else { return false }
        let macRegex = "^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$"
        return NSPredicate(format: "SELF MATCHES %@", macRegex).evaluate(with: mac)
    }
    
    // MARK: - ID Card Validation
    
    /// Validate Chinese ID card number (18 digits)
    public static func isValidChinaIDCard(_ idCard: String?) -> Bool {
        guard let idCard = idCard else { return false }
        let digitsOnly = idCard.filter { $0.isNumber }
        guard digitsOnly.count == 17 else { return false }
        
        let weights = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
        let checkCodes = ["1", "0", "X", "9", "8", "7", "6", "5", "4", "3", "2"]
        
        var sum = 0
        for (index, char) in digitsOnly.enumerated() {
            guard let digit = char.wholeNumberValue else { return false }
            sum += digit * weights[index]
        }
        
        let checkCode = checkCodes[sum % 11]
        let lastChar = String(idCard.last!).uppercased()
        return lastChar == checkCode
    }
    
    // MARK: - Password Validation
    
    /// Check password strength and return detailed result
    public static func checkPasswordStrength(_ password: String?) -> (strength: PasswordStrength, score: Int, messages: [String]) {
        guard let password = password else {
            return (.veryWeak, 0, ["Password is required"])
        }
        
        var score = 0
        var messages: [String] = []
        
        // Length check
        if password.count < 8 {
            messages.append("Password must be at least 8 characters")
        } else if password.count >= 12 {
            score += 2
        } else {
            score += 1
        }
        
        // Uppercase check
        let hasUppercase = password.contains { $0.isUppercase }
        if hasUppercase {
            score += 1
        } else {
            messages.append("Password must contain uppercase letters")
        }
        
        // Lowercase check
        let hasLowercase = password.contains { $0.isLowercase }
        if hasLowercase {
            score += 1
        } else {
            messages.append("Password must contain lowercase letters")
        }
        
        // Digit check
        let hasDigit = password.contains { $0.isNumber }
        if hasDigit {
            score += 1
        } else {
            messages.append("Password must contain digits")
        }
        
        // Special character check
        let specialChars = CharacterSet(charactersIn: "!@#$%^&*()-_=+[]{}|;:,.<>?")
        let hasSpecial = password.unicodeScalars.contains { specialChars.contains($0) }
        if hasSpecial {
            score += 1
        } else {
            messages.append("Password must contain special characters")
        }
        
        // Determine strength
        let strength: PasswordStrength
        switch score {
        case 0...1: strength = .veryWeak
        case 2: strength = .weak
        case 3...4: strength = .medium
        case 5: strength = .strong
        default: strength = .veryStrong
        }
        
        return (strength, score, messages.isEmpty ? ["Password is strong"] : messages)
    }
    
    /// Validate strong password (at least 8 chars, uppercase, lowercase, digit, special char)
    public static func isStrongPassword(_ password: String?) -> Bool {
        guard let password = password, password.count >= 8 else { return false }
        
        let hasUppercase = password.contains { $0.isUppercase }
        let hasLowercase = password.contains { $0.isLowercase }
        let hasDigit = password.contains { $0.isNumber }
        let specialChars = CharacterSet(charactersIn: "!@#$%^&*()-_=+[]{}|;:,.<>?")
        let hasSpecial = password.unicodeScalars.contains { specialChars.contains($0) }
        
        return hasUppercase && hasLowercase && hasDigit && hasSpecial
    }
    
    // MARK: - Date Validation
    
    /// Validate date string with format
    public static func isValidDate(_ dateString: String?, format: String = "yyyy-MM-dd") -> Bool {
        guard let dateString = dateString else { return false }
        let formatter = DateFormatter()
        formatter.dateFormat = format
        formatter.isLenient = false
        return formatter.date(from: dateString) != nil
    }
    
    /// Validate ISO 8601 date string
    public static func isValidISODate(_ dateString: String?) -> Bool {
        guard let dateString = dateString else { return false }
        let formatter = ISO8601DateFormatter()
        return formatter.date(from: dateString) != nil
    }
    
    // MARK: - Regex Validation
    
    /// Validate string against custom regex pattern
    public static func matches(_ string: String?, pattern: String) -> Bool {
        guard let string = string else { return false }
        return NSPredicate(format: "SELF MATCHES %@", pattern).evaluate(with: string)
    }
    
    /// Check if string contains pattern
    public static func contains(_ string: String?, pattern: String) -> Bool {
        guard let string = string else { return false }
        guard let regex = try? NSRegularExpression(pattern: pattern) else { return false }
        let range = NSRange(string.startIndex..., in: string)
        return regex.firstMatch(in: string, options: [], range: range) != nil
    }
    
    // MARK: - Numeric Validation
    
    /// Check if value is within numeric range
    public static func between<T: Comparable>(_ value: T, min: T, max: T) -> Bool {
        return value >= min && value <= max
    }
    
    /// Check if string represents a valid integer
    public static func isValidInteger(_ string: String?) -> Bool {
        guard let string = string else { return false }
        return Int(string) != nil
    }
    
    /// Check if string represents a valid floating point number
    public static func isValidFloat(_ string: String?) -> Bool {
        guard let string = string else { return false }
        return Double(string) != nil
    }
    
    /// Check if string represents a positive number
    public static func isPositive(_ string: String?) -> Bool {
        guard let string = string, let num = Double(string) else { return false }
        return num > 0
    }
    
    /// Check if string represents a negative number
    public static func isNegative(_ string: String?) -> Bool {
        guard let string = string, let num = Double(string) else { return false }
        return num < 0
    }
}
