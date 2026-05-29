//
//  CreditCardUtils Examples.swift
//  AllToolkit - Credit Card Utilities Usage Examples
//
//  Created by AllToolkit Auto Generator
//  Date: 2026-05-29
//

import Foundation

// MARK: - Example Usage

func demonstrateCreditCardUtils() {
    print("=" * 60)
    print("CreditCardUtils - Usage Examples")
    print("=" * 60)
    print()
    
    // ========================================
    // 1. Card Type Detection
    // ========================================
    print("1️⃣  Card Type Detection")
    print("-" * 40)
    
    let cards = [
        ("Visa", "4242424242424242"),
        ("MasterCard", "5555555555554444"),
        ("American Express", "378282246310005"),
        ("Discover", "6011111111111117"),
        ("JCB", "3530111333300000"),
        ("Diners Club", "30569300000000"),
        ("UnionPay", "6221260000000000"),
        ("Unknown", "1234567890123456")
    ]
    
    for (name, number) in cards {
        let type = CreditCardUtils.detectCardType(number)
        print("  \(name.padRight(20)) -> \(type.displayName)")
    }
    print()
    
    // ========================================
    // 2. Validation
    // ========================================
    print("2️⃣  Validation")
    print("-" * 40)
    
    let validationExamples = [
        ("Valid Visa", "4242424242424242"),
        ("Invalid Luhn", "4242424242424241"),
        ("Too Short", "123456"),
        ("Empty", "")
    ]
    
    for (name, number) in validationExamples {
        let result = CreditCardUtils.validate(number)
        let status = result.isValid ? "✅ Valid" : "❌ Invalid"
        print("  \(name.padRight(20)) -> \(status)")
        if !result.errors.isEmpty {
            for error in result.errors {
                print("      ⚠️  \(error.rawValue)")
            }
        }
    }
    print()
    
    // ========================================
    // 3. Luhn Algorithm
    // ========================================
    print("3️⃣  Luhn Algorithm")
    print("-" * 40)
    
    let luhnExamples = [
        "4242424242424242",
        "5555555555554444",
        "378282246310005",
        "4242424242424241" // Invalid
    ]
    
    for number in luhnExamples {
        let passes = CreditCardUtils.luhnCheck(number)
        let checksum = CreditCardUtils.generateLuhnChecksum(String(number.dropLast()))
        print("  \(number) -> Luhn: \(passes ? "✅ Pass" : "❌ Fail") | Checksum digit: \(checksum ?? 0)")
    }
    print()
    
    // ========================================
    // 4. Formatting
    // ========================================
    print("4️⃣  Formatting")
    print("-" * 40)
    
    let formatExamples = [
        ("Visa", "4242424242424242"),
        ("Amex", "378282246310005"),
        ("MasterCard", "5555555555554444")
    ]
    
    for (name, number) in formatExamples {
        let formatted = CreditCardUtils.format(number)
        let withSpaces = CreditCardUtils.format(number, separator: " ")
        print("  \(name.padRight(15)) -> Default: \(formatted)")
        print("  \("".padRight(15))    Spaces:  \(withSpaces)")
    }
    print()
    
    // ========================================
    // 5. Masking
    // ========================================
    print("5️⃣  Masking")
    print("-" * 40)
    
    let cardNumber = "4242424242424242"
    
    print("  Original:     \(cardNumber)")
    print("  Default Mask:  \(CreditCardUtils.mask(cardNumber))")
    print("  Full Mask:    \(CreditCardUtils.mask(cardNumber, visiblePrefix: 0, visibleSuffix: 4))")
    print("  Custom Mask:  \(CreditCardUtils.mask(cardNumber, visiblePrefix: 4, visibleSuffix: 4, maskChar: "X"))")
    print("  Last 4:       \(CreditCardUtils.lastFour(cardNumber))")
    print("  First 6:      \(CreditCardUtils.firstSix(cardNumber))")
    print()
    
    // ========================================
    // 6. Issuer Detection
    // ========================================
    print("6️⃣  Issuer Detection")
    print("-" * 40)
    
    let issuerExamples = [
        "4000000000000000",
        "5100000000000000",
        "340000000000000",
        "6011000000000000",
        "6221260000000000"
    ]
    
    for number in issuerExamples {
        let issuer = CreditCardUtils.getIssuer(number) ?? "Unknown"
        print("  \(number) -> \(issuer)")
    }
    print()
    
    // ========================================
    // 7. Full Analysis
    // ========================================
    print("7️⃣  Full Analysis")
    print("-" * 40)
    
    let analysisCards = [
        "4242424242424242",
        "5555555555554444",
        "378282246310005"
    ]
    
    for number in analysisCards {
        let info = CreditCardUtils.analyze(number)
        print("  Card: \(number)")
        print("    Type:     \(info.type.displayName)")
        print("    Valid:    \(info.isValid ? "✅ Yes" : "❌ No")")
        print("    Formatted: \(info.formattedNumber)")
        print("    Masked:   \(info.maskedNumber)")
        print("    Last 4:   \(info.lastFourDigits)")
        print("    Issuer:   \(info.issuer ?? "Unknown")")
        print()
    }
    
    // ========================================
    // 8. Expiry Validation
    // ========================================
    print("8️⃣  Expiry Validation")
    print("-" * 40)
    
    let calendar = Calendar.current
    let currentYear = calendar.component(.year, from: Date())
    let currentMonth = calendar.component(.month, from: Date())
    
    // Future date (valid)
    let futureMonth = currentMonth == 12 ? 1 : currentMonth
    let futureYear = currentMonth == 12 ? currentYear + 2 : currentYear + 1
    let futureResult = CreditCardUtils.validateExpiry(month: futureMonth, year: futureYear)
    print("  Future Date (\(futureMonth)/\(futureYear)): \(futureResult.isValid ? "✅ Valid" : "❌ Invalid")")
    
    // Past date (expired)
    let pastMonth = currentMonth == 1 ? 12 : currentMonth - 1
    let pastYear = currentMonth == 1 ? currentYear - 1 : currentYear - 1
    let pastResult = CreditCardUtils.validateExpiry(month: pastMonth, year: pastYear)
    print("  Past Date (\(pastMonth)/\(pastYear)): \(pastResult.isValid ? "✅ Valid" : "❌ Expired")")
    print()
    
    // ========================================
    // 9. CVV Validation
    // ========================================
    print("9️⃣  CVV Validation")
    print("-" * 40)
    
    let cvvExamples: [(type: CreditCardType, cvv: String)] = [
        (.visa, "123"),
        (.visa, "1234"), // Wrong length
        (.amex, "1234"),
        (.amex, "123")   // Wrong length
    ]
    
    for example in cvvExamples {
        let result = CreditCardUtils.validateCVV(cvv: example.cvv, for: example.type)
        let status = result.isValid ? "✅ Valid" : "❌ Invalid"
        print("  \(example.type.displayName.padRight(20)) CVV: \(example.cvv.padRight(5)) -> \(status)")
    }
    print()
    
    // ========================================
    // 10. Test Number Generation
    // ========================================
    print("🔟 Test Number Generation")
    print("-" * 40)
    
    for type in [CreditCardType.visa, .mastercard, .amex, .discover, .jcb] {
        let testNumber = CreditCardUtils.generateTestNumber(for: type)
        let info = CreditCardUtils.analyze(testNumber)
        print("  \(type.displayName.padRight(20)) -> \(testNumber.padRight(20)) Valid: \(info.isValid ? "✅" : "❌")")
    }
    print()
    
    // ========================================
    // 11. String Extensions
    // ========================================
    print("1️⃣1️⃣  String Extensions")
    print("-" * 40)
    
    let card = "4242424242424242"
    
    print("  Card: \(card)")
    print("  isValidCreditCard:  \(card.isValidCreditCard)")
    print("  creditCardType:     \(card.creditCardType.displayName)")
    print("  formattedCreditCard: \(card.formattedCreditCard)")
    print("  maskedCreditCard:   \(card.maskedCreditCard)")
    print()
    
    // ========================================
    // 12. Complete Validation Example
    // ========================================
    print("1️⃣2️⃣  Complete Payment Validation")
    print("-" * 40)
    
    func validatePayment(cardNumber: String, expiryMonth: Int, expiryYear: Int, cvv: String) {
        print("  Validating payment details...")
        
        let result = CreditCardUtils.validateFull(
            cardNumber: cardNumber,
            expiryMonth: expiryMonth,
            expiryYear: expiryYear,
            cvv: cvv
        )
        
        if result.isValid {
            let info = CreditCardUtils.analyze(cardNumber)
            print("  ✅ Payment details valid!")
            print("     Card Type: \(info.type.displayName)")
            print("     Last 4: \(info.lastFourDigits)")
        } else {
            print("  ❌ Validation failed!")
            for error in result.errors {
                print("     - \(error.rawValue)")
            }
        }
        
        if !result.warnings.isEmpty {
            print("  ⚠️  Warnings:")
            for warning in result.warnings {
                print("     - \(warning)")
            }
        }
    }
    
    // Valid payment
    validatePayment(
        cardNumber: "4242424242424242",
        expiryMonth: 12,
        expiryYear: currentYear + 1,
        cvv: "123"
    )
    print()
    
    // Invalid payment
    validatePayment(
        cardNumber: "4242424242424241",
        expiryMonth: 1,
        expiryYear: 2020,
        cvv: "1234"
    )
    print()
    
    print("=" * 60)
    print("Examples completed!")
    print("=" * 60)
}

// Helper extension for string padding
extension String {
    func padRight(_ length: Int) -> String {
        return self.padding(toLength: length, withPad: " ", startingAt: 0)
    }
}

// Run the examples
// demonstrateCreditCardUtils()