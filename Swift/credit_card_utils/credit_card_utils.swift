//
//  CreditCardUtils.swift
//  AllToolkit - Credit Card Validation and Formatting Utilities
//
//  Created by AllToolkit Auto Generator
//  Date: 2026-05-29
//
//  A comprehensive credit card validation, formatting, and identification toolkit.
//  Zero external dependencies - pure Swift implementation.
//

import Foundation

// MARK: - Credit Card Types

/// Supported credit card types
public enum CreditCardType: String, CaseIterable {
    case visa = "Visa"
    case mastercard = "MasterCard"
    case amex = "American Express"
    case discover = "Discover"
    case dinersClub = "Diners Club"
    case jcb = "JCB"
    case unionPay = "UnionPay"
    case maestro = "Maestro"
    case unknown = "Unknown"
    
    /// Card type display name
    public var displayName: String {
        return self.rawValue
    }
    
    /// Card number length range
    public var lengthRange: ClosedRange<Int> {
        switch self {
        case .visa: return 13...16
        case .mastercard: return 16...16
        case .amex: return 15...15
        case .discover: return 16...19
        case .dinersClub: return 14...19
        case .jcb: return 16...16
        case .unionPay: return 16...19
        case .maestro: return 12...19
        case .unknown: return 13...19
        }
    }
    
    /// CVV length for this card type
    public var cvvLength: Int {
        switch self {
        case .amex: return 4
        default: return 3
        }
    }
}

// MARK: - Credit Card Info

/// Credit card information container
public struct CreditCardInfo {
    public let type: CreditCardType
    public let isValid: Bool
    public let formattedNumber: String
    public let maskedNumber: String
    public let lastFourDigits: String
    public let issuer: String?
    public let isExpired: Bool?
    
    public init(
        type: CreditCardType,
        isValid: Bool,
        formattedNumber: String,
        maskedNumber: String,
        lastFourDigits: String,
        issuer: String? = nil,
        isExpired: Bool? = nil
    ) {
        self.type = type
        self.isValid = isValid
        self.formattedNumber = formattedNumber
        self.maskedNumber = maskedNumber
        self.lastFourDigits = lastFourDigits
        self.issuer = issuer
        self.isExpired = isExpired
    }
}

// MARK: - Validation Result

/// Detailed validation result
public struct ValidationResult {
    public let isValid: Bool
    public let errors: [ValidationError]
    public let warnings: [String]
    
    public init(isValid: Bool, errors: [ValidationError] = [], warnings: [String] = []) {
        self.isValid = isValid
        self.errors = errors
        self.warnings = warnings
    }
    
    public enum ValidationError: String {
        case emptyNumber = "Card number is empty"
        case invalidCharacters = "Card number contains invalid characters"
        case invalidLength = "Card number length is invalid for this card type"
        case luhnFailed = "Card number fails Luhn checksum validation"
        case unknownCardType = "Unknown card type"
        case expired = "Card has expired"
        case invalidExpiryFormat = "Invalid expiry date format"
        case invalidCVV = "Invalid CVV for this card type"
    }
}

// MARK: - Credit Card Utils

/// Main credit card utility class
public final class CreditCardUtils {
    
    // MARK: - Private Constants
    
    /// Card type detection patterns
    private static let cardPatterns: [(type: CreditCardType, pattern: String)] = [
        (.visa, "^4[0-9]{12}(?:[0-9]{3})?$"),
        (.mastercard, "^(?:5[1-5][0-9]{2}|2[2-7][0-9]{2})[0-9]{12}$"),
        (.amex, "^3[47][0-9]{13}$"),
        (.discover, "^6(?:011|5[0-9]{2})[0-9]{12}$"),
        (.dinersClub, "^3(?:0[0-5]|[68][0-9])[0-9]{11}$"),
        (.jcb, "^(?:2131|1800|35[0-9]{3})[0-9]{11}$"),
        (.unionPay, "^(62|81)[0-9]{14,17}$"),
        (.maestro, "^(5018|5020|5038|58[0-9]{2}|6304|6759|676[1-3]|060[0-9]{2})[0-9]{8,15}$")
    ]
    
    /// Issuer identification numbers (IIN/BIN ranges)
    private static let issuerRanges: [(range: ClosedRange<Int>, issuer: String)] = [
        (400000...499999, "Visa"),
        (510000...559999, "MasterCard"),
        (222100...272099, "MasterCard"),
        (340000...349999, "American Express"),
        (370000...379999, "American Express"),
        (601100...601199, "Discover"),
        (622126...622925, "UnionPay"),
        (624000...626999, "UnionPay"),
        (628200...628899, "UnionPay")
    ]
    
    // MARK: - Card Type Detection
    
    /// Detect the credit card type from a card number
    /// - Parameter cardNumber: The card number to analyze
    /// - Returns: The detected card type
    public static func detectCardType(_ cardNumber: String) -> CreditCardType {
        let cleanNumber = sanitize(cardNumber)
        
        guard !cleanNumber.isEmpty else { return .unknown }
        
        for (type, pattern) in cardPatterns {
            if let regex = try? NSRegularExpression(pattern: pattern, options: []),
               regex.firstMatch(in: cleanNumber, options: [], range: NSRange(location: 0, length: cleanNumber.count)) != nil {
                return type
            }
        }
        
        return .unknown
    }
    
    // MARK: - Validation
    
    /// Validate a credit card number
    /// - Parameter cardNumber: The card number to validate
    /// - Returns: Whether the card number is valid
    public static func isValid(_ cardNumber: String) -> Bool {
        return validate(cardNumber).isValid
    }
    
    /// Validate a credit card number with detailed results
    /// - Parameter cardNumber: The card number to validate
    /// - Returns: Detailed validation result
    public static func validate(_ cardNumber: String) -> ValidationResult {
        var errors: [ValidationResult.ValidationError] = []
        var warnings: [String] = []
        
        let cleanNumber = sanitize(cardNumber)
        
        // Check empty
        guard !cleanNumber.isEmpty else {
            return ValidationResult(isValid: false, errors: [.emptyNumber])
        }
        
        // Check for non-numeric characters
        guard cleanNumber.allSatisfy({ $0.isNumber }) else {
            return ValidationResult(isValid: false, errors: [.invalidCharacters])
        }
        
        // Detect card type
        let cardType = detectCardType(cleanNumber)
        
        if cardType == .unknown {
            warnings.append("Card type could not be determined")
        }
        
        // Validate length
        let length = cleanNumber.count
        if !cardType.lengthRange.contains(length) {
            errors.append(.invalidLength)
        }
        
        // Luhn validation
        if !luhnCheck(cleanNumber) {
            errors.append(.luhnFailed)
        }
        
        return ValidationResult(
            isValid: errors.isEmpty,
            errors: errors,
            warnings: warnings
        )
    }
    
    /// Validate card number with expiry and CVV
    /// - Parameters:
    ///   - cardNumber: The card number
    ///   - expiryMonth: Expiry month (1-12)
    ///   - expiryYear: Expiry year (4 digits)
    ///   - cvv: CVV code
    /// - Returns: Detailed validation result
    public static func validateFull(
        cardNumber: String,
        expiryMonth: Int,
        expiryYear: Int,
        cvv: String
    ) -> ValidationResult {
        var errors: [ValidationResult.ValidationError] = []
        var warnings: [String] = []
        
        // Validate card number
        let numberValidation = validate(cardNumber)
        errors.append(contentsOf: numberValidation.errors)
        warnings.append(contentsOf: numberValidation.warnings)
        
        // Validate expiry
        let expiryValidation = validateExpiry(month: expiryMonth, year: expiryYear)
        errors.append(contentsOf: expiryValidation.errors)
        warnings.append(contentsOf: expiryValidation.warnings)
        
        // Validate CVV
        let cvvValidation = validateCVV(cvv: cvv, forCardNumber: cardNumber)
        errors.append(contentsOf: cvvValidation.errors)
        
        return ValidationResult(isValid: errors.isEmpty, errors: errors, warnings: warnings)
    }
    
    /// Validate expiry date
    /// - Parameters:
    ///   - month: Month (1-12)
    ///   - year: Year (4 digits)
    /// - Returns: Validation result
    public static func validateExpiry(month: Int, year: Int) -> ValidationResult {
        var errors: [ValidationResult.ValidationError] = []
        var warnings: [String] = []
        
        // Validate month
        guard (1...12).contains(month) else {
            return ValidationResult(isValid: false, errors: [.invalidExpiryFormat])
        }
        
        // Get current date
        let calendar = Calendar.current
        let now = Date()
        let currentYear = calendar.component(.year, from: now)
        let currentMonth = calendar.component(.month, from: now)
        
        // Check if expired
        if year < currentYear || (year == currentYear && month < currentMonth) {
            errors.append(.expired)
        }
        
        // Warn if expiry is too far in future (likely error)
        if year > currentYear + 20 {
            warnings.append("Expiry date is more than 20 years in the future")
        }
        
        return ValidationResult(isValid: errors.isEmpty, errors: errors, warnings: warnings)
    }
    
    /// Validate CVV for a card type
    /// - Parameters:
    ///   - cvv: CVV code to validate
    ///   - forCardNumber: Card number to determine type
    /// - Returns: Validation result
    public static func validateCVV(cvv: String, forCardNumber cardNumber: String) -> ValidationResult {
        let cardType = detectCardType(cardNumber)
        return validateCVV(cvv: cvv, for: cardType)
    }
    
    /// Validate CVV for a card type
    /// - Parameters:
    ///   - cvv: CVV code to validate
    ///   - cardType: Card type
    /// - Returns: Validation result
    public static func validateCVV(cvv: String, for cardType: CreditCardType) -> ValidationResult {
        let cleanCVV = cvv.filter { $0.isNumber }
        let expectedLength = cardType.cvvLength
        
        guard cleanCVV.count == expectedLength else {
            return ValidationResult(isValid: false, errors: [.invalidCVV])
        }
        
        return ValidationResult(isValid: true)
    }
    
    // MARK: - Luhn Algorithm
    
    /// Perform Luhn algorithm validation
    /// - Parameter number: The card number to validate
    /// - Returns: Whether the number passes the Luhn check
    public static func luhnCheck(_ number: String) -> Bool {
        let cleanNumber = sanitize(number)
        
        guard cleanNumber.allSatisfy({ $0.isNumber }) else {
            return false
        }
        
        let digits = cleanNumber.compactMap { $0.wholeNumberValue }
        
        var sum = 0
        let parity = digits.count % 2
        
        for (index, digit) in digits.enumerated() {
            var value = digit
            
            if index % 2 == parity {
                value *= 2
                if value > 9 {
                    value -= 9
                }
            }
            
            sum += value
        }
        
        return sum % 10 == 0
    }
    
    /// Generate a valid Luhn checksum digit for a partial card number
    /// - Parameter partialNumber: The partial card number (without checksum)
    /// - Returns: The checksum digit, or nil if input is invalid
    public static func generateLuhnChecksum(_ partialNumber: String) -> Int? {
        let cleanNumber = sanitize(partialNumber)
        
        guard cleanNumber.allSatisfy({ $0.isNumber }) else {
            return nil
        }
        
        let digits = cleanNumber.compactMap { $0.wholeNumberValue }
        
        var sum = 0
        let parity = (digits.count + 1) % 2
        
        for (index, digit) in digits.enumerated() {
            var value = digit
            
            if index % 2 == parity {
                value *= 2
                if value > 9 {
                    value -= 9
                }
            }
            
            sum += value
        }
        
        return (10 - (sum % 10)) % 10
    }
    
    // MARK: - Formatting
    
    /// Format a card number with spaces
    /// - Parameter cardNumber: The card number to format
    /// - Returns: Formatted card number
    public static func format(_ cardNumber: String) -> String {
        let cleanNumber = sanitize(cardNumber)
        let cardType = detectCardType(cleanNumber)
        
        switch cardType {
        case .amex:
            // Amex: 4-6-5 format
            return formatWithPattern(cleanNumber, pattern: "****-******-*####")
        case .dinersClub:
            // Diners: 4-6-4 format
            return formatWithPattern(cleanNumber, pattern: "****-******-****")
        default:
            // Standard: 4-4-4-4 format
            return formatWithPattern(cleanNumber, pattern: "****-****-****-****")
        }
    }
    
    /// Format with custom separator
    /// - Parameters:
    ///   - cardNumber: The card number
    ///   - separator: Separator character
    /// - Returns: Formatted card number
    public static func format(_ cardNumber: String, separator: Character) -> String {
        let cleanNumber = sanitize(cardNumber)
        let cardType = detectCardType(cleanNumber)
        
        var result = ""
        var index = 0
        
        let groupSizes: [Int]
        switch cardType {
        case .amex:
            groupSizes = [4, 6, 5]
        case .dinersClub:
            groupSizes = [4, 6, 4]
        default:
            groupSizes = [4, 4, 4, 4]
        }
        
        for size in groupSizes {
            let end = min(index + size, cleanNumber.count)
            if index < end {
                if !result.isEmpty {
                    result.append(separator)
                }
                let start = cleanNumber.index(cleanNumber.startIndex, offsetBy: index)
                let endIndex = cleanNumber.index(cleanNumber.startIndex, offsetBy: end)
                result += String(cleanNumber[start..<endIndex])
            }
            index = end
            if index >= cleanNumber.count { break }
        }
        
        // Add remaining digits if any
        if index < cleanNumber.count {
            let remaining = cleanNumber[cleanNumber.index(cleanNumber.startIndex, offsetBy: index)...]
            if !result.isEmpty {
                result.append(separator)
            }
            result += String(remaining)
        }
        
        return result
    }
    
    // MARK: - Masking
    
    /// Mask a card number (show first 6 and last 4 digits)
    /// - Parameter cardNumber: The card number to mask
    /// - Returns: Masked card number
    public static func mask(_ cardNumber: String) -> String {
        let cleanNumber = sanitize(cardNumber)
        
        guard cleanNumber.count >= 10 else {
            return String(repeating: "*", count: cleanNumber.count)
        }
        
        let firstSix = String(cleanNumber.prefix(6))
        let lastFour = String(cleanNumber.suffix(4))
        let middleCount = cleanNumber.count - 10
        
        return "\(firstSix)\(String(repeating: "*", count: middleCount))\(lastFour)"
    }
    
    /// Mask with custom visible ranges
    /// - Parameters:
    ///   - cardNumber: The card number
    ///   - visiblePrefix: Number of visible digits at start
    ///   - visibleSuffix: Number of visible digits at end
    ///   - maskChar: Character to use for masking
    /// - Returns: Masked card number
    public static func mask(
        _ cardNumber: String,
        visiblePrefix: Int = 6,
        visibleSuffix: Int = 4,
        maskChar: Character = "*"
    ) -> String {
        let cleanNumber = sanitize(cardNumber)
        
        let totalVisible = visiblePrefix + visibleSuffix
        guard cleanNumber.count > totalVisible else {
            return String(repeating: maskChar, count: cleanNumber.count)
        }
        
        let prefix = String(cleanNumber.prefix(visiblePrefix))
        let suffix = String(cleanNumber.suffix(visibleSuffix))
        let middleCount = cleanNumber.count - totalVisible
        
        return "\(prefix)\(String(repeating: String(maskChar), count: middleCount))\(suffix)"
    }
    
    /// Get last 4 digits
    /// - Parameter cardNumber: The card number
    /// - Returns: Last 4 digits, or all digits if less than 4
    public static func lastFour(_ cardNumber: String) -> String {
        let cleanNumber = sanitize(cardNumber)
        return String(cleanNumber.suffix(4))
    }
    
    /// Get first 6 digits (IIN/BIN)
    /// - Parameter cardNumber: The card number
    /// - Returns: First 6 digits, or all digits if less than 6
    public static func firstSix(_ cardNumber: String) -> String {
        let cleanNumber = sanitize(cardNumber)
        return String(cleanNumber.prefix(6))
    }
    
    // MARK: - Issuer Detection
    
    /// Get issuer from card number
    /// - Parameter cardNumber: The card number
    /// - Returns: Issuer name if known
    public static func getIssuer(_ cardNumber: String) -> String? {
        let cleanNumber = sanitize(cardNumber)
        
        guard cleanNumber.count >= 6,
              let iin = Int(String(cleanNumber.prefix(6))) else {
            return nil
        }
        
        for (range, issuer) in issuerRanges {
            if range.contains(iin) {
                return issuer
            }
        }
        
        return nil
    }
    
    // MARK: - Full Analysis
    
    /// Get complete card information
    /// - Parameter cardNumber: The card number
    /// - Returns: CreditCardInfo with all details
    public static func analyze(_ cardNumber: String) -> CreditCardInfo {
        let cleanNumber = sanitize(cardNumber)
        let cardType = detectCardType(cleanNumber)
        let valid = isValid(cleanNumber)
        let formatted = format(cleanNumber)
        let masked = mask(cleanNumber)
        let lastFour = lastFour(cleanNumber)
        let issuer = getIssuer(cleanNumber)
        
        return CreditCardInfo(
            type: cardType,
            isValid: valid,
            formattedNumber: formatted,
            maskedNumber: masked,
            lastFourDigits: lastFour,
            issuer: issuer
        )
    }
    
    /// Analyze with expiry information
    /// - Parameters:
    ///   - cardNumber: The card number
    ///   - expiryMonth: Expiry month
    ///   - expiryYear: Expiry year
    /// - Returns: CreditCardInfo with expiry status
    public static func analyzeWithExpiry(
        _ cardNumber: String,
        expiryMonth: Int,
        expiryYear: Int
    ) -> CreditCardInfo {
        var info = analyze(cardNumber)
        let expiryValidation = validateExpiry(month: expiryMonth, year: expiryYear)
        
        return CreditCardInfo(
            type: info.type,
            isValid: info.isValid && expiryValidation.isValid,
            formattedNumber: info.formattedNumber,
            maskedNumber: info.maskedNumber,
            lastFourDigits: info.lastFourDigits,
            issuer: info.issuer,
            isExpired: expiryValidation.errors.contains(.expired)
        )
    }
    
    // MARK: - Generation (for testing)
    
    /// Generate a test card number for a specific type
    /// - Parameter type: The card type
    /// - Returns: A valid test card number
    public static func generateTestNumber(for type: CreditCardType) -> String {
        // Test card prefixes for each type
        let prefixes: [CreditCardType: [String]] = [
            .visa: ["4000000000000", "400000000000000"],
            .mastercard: ["5100000000000000", "5200000000000000", "5500000000000000", "2200000000000000"],
            .amex: ["34000000000000", "37000000000000"],
            .discover: ["601100000000000"],
            .dinersClub: ["30000000000000"],
            .jcb: ["3528000000000000"],
            .unionPay: ["6200000000000000"],
            .maestro: ["501800000000"]
        ]
        
        guard let availablePrefixes = prefixes[type], let prefix = availablePrefixes.first else {
            return ""
        }
        
        // Pad to target length - 1 (checksum digit will be added)
        let targetLength = type.lengthRange.lowerBound
        var number = prefix
        
        while number.count < targetLength - 1 {
            number += String(Int.random(in: 0...9))
        }
        
        // Calculate and append checksum
        if let checksum = generateLuhnChecksum(number) {
            number += String(checksum)
        }
        
        return number
    }
    
    // MARK: - Helper Methods
    
    /// Sanitize a card number (remove non-numeric characters)
    /// - Parameter cardNumber: Input card number
    /// - Returns: Clean numeric string
    public static func sanitize(_ cardNumber: String) -> String {
        return cardNumber.filter { $0.isNumber }
    }
    
    /// Format number with pattern
    private static func formatWithPattern(_ number: String, pattern: String) -> String {
        var result = ""
        var numberIndex = number.startIndex
        
        for char in pattern {
            if char == "*" || char == "#" {
                if numberIndex < number.endIndex {
                    result.append(char == "#" ? number[numberIndex] : "*")
                    numberIndex = number.index(after: numberIndex)
                }
            } else {
                result.append(char)
            }
        }
        
        return result
    }
}

// MARK: - Convenience Extensions

public extension String {
    /// Check if string is a valid credit card number
    var isValidCreditCard: Bool {
        return CreditCardUtils.isValid(self)
    }
    
    /// Get credit card type from string
    var creditCardType: CreditCardType {
        return CreditCardUtils.detectCardType(self)
    }
    
    /// Format as credit card number
    var formattedCreditCard: String {
        return CreditCardUtils.format(self)
    }
    
    /// Mask credit card number
    var maskedCreditCard: String {
        return CreditCardUtils.mask(self)
    }
}