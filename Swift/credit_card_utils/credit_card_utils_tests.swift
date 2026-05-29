//
//  CreditCardUtilsTests.swift
//  AllToolkit - Credit Card Utilities Tests
//
//  Created by AllToolkit Auto Generator
//  Date: 2026-05-29
//

import Foundation
import XCTest

// For standalone compilation, include the main module
// @testable import CreditCardUtils

final class CreditCardUtilsTests: XCTestCase {
    
    // MARK: - Card Type Detection Tests
    
    func testVisaDetection() {
        XCTAssertEqual(CreditCardUtils.detectCardType("4000000000000001"), .visa)
        XCTAssertEqual(CreditCardUtils.detectCardType("4111111111111111"), .visa)
        XCTAssertEqual(CreditCardUtils.detectCardType("4012888888881881"), .visa)
        XCTAssertEqual(CreditCardUtils.detectCardType("4222222222222"), .visa)
    }
    
    func testMasterCardDetection() {
        XCTAssertEqual(CreditCardUtils.detectCardType("5100000000000000"), .mastercard)
        XCTAssertEqual(CreditCardUtils.detectCardType("5200000000000000"), .mastercard)
        XCTAssertEqual(CreditCardUtils.detectCardType("5300000000000000"), .mastercard)
        XCTAssertEqual(CreditCardUtils.detectCardType("5400000000000000"), .mastercard)
        XCTAssertEqual(CreditCardUtils.detectCardType("5500000000000000"), .mastercard)
        // 2-series MasterCard
        XCTAssertEqual(CreditCardUtils.detectCardType("2200000000000000"), .mastercard)
        XCTAssertEqual(CreditCardUtils.detectCardType("2720000000000000"), .mastercard)
    }
    
    func testAmexDetection() {
        XCTAssertEqual(CreditCardUtils.detectCardType("340000000000009"), .amex)
        XCTAssertEqual(CreditCardUtils.detectCardType("370000000000002"), .amex)
        XCTAssertEqual(CreditCardUtils.detectCardType("378282246310005"), .amex)
        XCTAssertEqual(CreditCardUtils.detectCardType("371449635398431"), .amex)
    }
    
    func testDiscoverDetection() {
        XCTAssertEqual(CreditCardUtils.detectCardType("6011000000000004"), .discover)
        XCTAssertEqual(CreditCardUtils.detectCardType("6011111111111117"), .discover)
        XCTAssertEqual(CreditCardUtils.detectCardType("6500000000000002"), .discover)
    }
    
    func testJCBDetection() {
        XCTAssertEqual(CreditCardUtils.detectCardType("3528000000000000"), .jcb)
        XCTAssertEqual(CreditCardUtils.detectCardType("3530111333300000"), .jcb)
    }
    
    func testDinersClubDetection() {
        XCTAssertEqual(CreditCardUtils.detectCardType("30000000000004"), .dinersClub)
        XCTAssertEqual(CreditCardUtils.detectCardType("30569300000000"), .dinersClub)
    }
    
    func testUnionPayDetection() {
        XCTAssertEqual(CreditCardUtils.detectCardType("6200000000000000"), .unionPay)
        XCTAssertEqual(CreditCardUtils.detectCardType("6221260000000000"), .unionPay)
    }
    
    func testMaestroDetection() {
        XCTAssertEqual(CreditCardUtils.detectCardType("501800000000"), .maestro)
        XCTAssertEqual(CreditCardUtils.detectCardType("6759000000000000"), .maestro)
    }
    
    func testUnknownCardDetection() {
        XCTAssertEqual(CreditCardUtils.detectCardType("0000000000000000"), .unknown)
        XCTAssertEqual(CreditCardUtils.detectCardType("1234567890123456"), .unknown)
    }
    
    func testCardTypeWithFormatting() {
        XCTAssertEqual(CreditCardUtils.detectCardType("4000-0000-0000-0001"), .visa)
        XCTAssertEqual(CreditCardUtils.detectCardType("4000 0000 0000 0001"), .visa)
        XCTAssertEqual(CreditCardUtils.detectCardType("4000 0000 0000 0001 "), .visa)
    }
    
    // MARK: - Luhn Algorithm Tests
    
    func testLuhnValidCards() {
        // These are known valid test card numbers
        XCTAssertTrue(CreditCardUtils.luhnCheck("4000000000000002"))
        XCTAssertTrue(CreditCardUtils.luhnCheck("4242424242424242"))
        XCTAssertTrue(CreditCardUtils.luhnCheck("5555555555554444"))
        XCTAssertTrue(CreditCardUtils.luhnCheck("378282246310005"))
        XCTAssertTrue(CreditCardUtils.luhnCheck("6011111111111117"))
    }
    
    func testLuhnInvalidCards() {
        XCTAssertFalse(CreditCardUtils.luhnCheck("4000000000000001"))
        XCTAssertFalse(CreditCardUtils.luhnCheck("4242424242424241"))
        XCTAssertFalse(CreditCardUtils.luhnCheck("1234567890123456"))
    }
    
    func testLuhnChecksumGeneration() {
        XCTAssertEqual(CreditCardUtils.generateLuhnChecksum("400000000000000"), 2)
        XCTAssertEqual(CreditCardUtils.generateLuhnChecksum("424242424242424"), 2)
        XCTAssertEqual(CreditCardUtils.generateLuhnChecksum("555555555555444"), 4)
    }
    
    // MARK: - Validation Tests
    
    func testValidCardNumbers() {
        XCTAssertTrue(CreditCardUtils.isValid("4242424242424242"))
        XCTAssertTrue(CreditCardUtils.isValid("5555555555554444"))
        XCTAssertTrue(CreditCardUtils.isValid("378282246310005"))
        XCTAssertTrue(CreditCardUtils.isValid("6011111111111117"))
    }
    
    func testInvalidCardNumbers() {
        XCTAssertFalse(CreditCardUtils.isValid(""))
        XCTAssertFalse(CreditCardUtils.isValid("123456"))
        XCTAssertFalse(CreditCardUtils.isValid("4242424242424241"))
        XCTAssertFalse(CreditCardUtils.isValid("5555555555554443"))
    }
    
    func testValidationDetails() {
        let validResult = CreditCardUtils.validate("4242424242424242")
        XCTAssertTrue(validResult.isValid)
        XCTAssertTrue(validResult.errors.isEmpty)
        
        let invalidResult = CreditCardUtils.validate("")
        XCTAssertFalse(invalidResult.isValid)
        XCTAssertTrue(invalidResult.errors.contains(.emptyNumber))
        
        let luhnFailResult = CreditCardUtils.validate("4242424242424241")
        XCTAssertFalse(luhnFailResult.isValid)
        XCTAssertTrue(luhnFailResult.errors.contains(.luhnFailed))
    }
    
    func testValidationWithExpiry() {
        let calendar = Calendar.current
        let currentYear = calendar.component(.year, from: Date())
        let currentMonth = calendar.component(.month, from: Date())
        
        // Valid expiry (next month)
        let validMonth = currentMonth == 12 ? 1 : currentMonth + 1
        let validYear = currentMonth == 12 ? currentYear + 1 : currentYear
        let validExpiryResult = CreditCardUtils.validateExpiry(month: validMonth, year: validYear)
        XCTAssertTrue(validExpiryResult.isValid)
        
        // Expired (last month)
        let expiredMonth = currentMonth == 1 ? 12 : currentMonth - 1
        let expiredYear = currentMonth == 1 ? currentYear - 1 : currentYear
        let expiredResult = CreditCardUtils.validateExpiry(month: expiredMonth, year: expiredYear)
        XCTAssertFalse(expiredResult.isValid)
        XCTAssertTrue(expiredResult.errors.contains(.expired))
    }
    
    func testCVVValidation() {
        // Visa/MasterCard - 3 digit CVV
        XCTAssertTrue(CreditCardUtils.validateCVV(cvv: "123", for: .visa).isValid)
        XCTAssertTrue(CreditCardUtils.validateCVV(cvv: "123", for: .mastercard).isValid)
        XCTAssertFalse(CreditCardUtils.validateCVV(cvv: "1234", for: .visa).isValid)
        
        // Amex - 4 digit CVV
        XCTAssertTrue(CreditCardUtils.validateCVV(cvv: "1234", for: .amex).isValid)
        XCTAssertFalse(CreditCardUtils.validateCVV(cvv: "123", for: .amex).isValid)
        
        // Invalid CVV
        XCTAssertFalse(CreditCardUtils.validateCVV(cvv: "12", for: .visa).isValid)
        XCTAssertFalse(CreditCardUtils.validateCVV(cvv: "abc", for: .visa).isValid)
    }
    
    func testFullValidation() {
        let calendar = Calendar.current
        let currentYear = calendar.component(.year, from: Date())
        
        let result = CreditCardUtils.validateFull(
            cardNumber: "4242424242424242",
            expiryMonth: 12,
            expiryYear: currentYear + 1,
            cvv: "123"
        )
        XCTAssertTrue(result.isValid)
        
        let invalidResult = CreditCardUtils.validateFull(
            cardNumber: "4242424242424241",
            expiryMonth: 12,
            expiryYear: currentYear + 1,
            cvv: "1234"
        )
        XCTAssertFalse(invalidResult.isValid)
        XCTAssertTrue(invalidResult.errors.contains(.luhnFailed))
        XCTAssertTrue(invalidResult.errors.contains(.invalidCVV))
    }
    
    // MARK: - Formatting Tests
    
    func testFormatVisa() {
        XCTAssertEqual(CreditCardUtils.format("4242424242424242"), "4242-4242-4242-4242")
        XCTAssertEqual(CreditCardUtils.format("424242424242424"), "4242-4242-4242-424")
    }
    
    func testFormatAmex() {
        XCTAssertEqual(CreditCardUtils.format("378282246310005"), "3782-822463-10005")
    }
    
    func testFormatWithCustomSeparator() {
        XCTAssertEqual(CreditCardUtils.format("4242424242424242", separator: " "), "4242 4242 4242 4242")
        XCTAssertEqual(CreditCardUtils.format("378282246310005", separator: "."), "3782.822463.10005")
    }
    
    func testFormatWithInputFormatting() {
        XCTAssertEqual(CreditCardUtils.format("4242-4242-4242-4242"), "4242-4242-4242-4242")
        XCTAssertEqual(CreditCardUtils.format("4242 4242 4242 4242"), "4242-4242-4242-4242")
    }
    
    // MARK: - Masking Tests
    
    func testMaskDefault() {
        XCTAssertEqual(CreditCardUtils.mask("4242424242424242"), "424242****4242")
        XCTAssertEqual(CreditCardUtils.mask("378282246310005"), "378282****10005")
    }
    
    func testMaskCustomVisibleRange() {
        XCTAssertEqual(
            CreditCardUtils.mask("4242424242424242", visiblePrefix: 4, visibleSuffix: 4),
            "4242********4242"
        )
        XCTAssertEqual(
            CreditCardUtils.mask("4242424242424242", visiblePrefix: 0, visibleSuffix: 4),
            "************4242"
        )
    }
    
    func testMaskWithCustomCharacter() {
        XCTAssertEqual(
            CreditCardUtils.mask("4242424242424242", maskChar: "X"),
            "424242XXXX4242"
        )
    }
    
    func testLastFour() {
        XCTAssertEqual(CreditCardUtils.lastFour("4242424242424242"), "4242")
        XCTAssertEqual(CreditCardUtils.lastFour("378282246310005"), "0005")
        XCTAssertEqual(CreditCardUtils.lastFour("123"), "123")
    }
    
    func testFirstSix() {
        XCTAssertEqual(CreditCardUtils.firstSix("4242424242424242"), "424242")
        XCTAssertEqual(CreditCardUtils.firstSix("12345"), "12345")
    }
    
    // MARK: - Issuer Detection Tests
    
    func testIssuerDetection() {
        XCTAssertEqual(CreditCardUtils.getIssuer("4000000000000000"), "Visa")
        XCTAssertEqual(CreditCardUtils.getIssuer("5100000000000000"), "MasterCard")
        XCTAssertEqual(CreditCardUtils.getIssuer("340000000000000"), "American Express")
        XCTAssertEqual(CreditCardUtils.getIssuer("6011000000000000"), "Discover")
        XCTAssertEqual(CreditCardUtils.getIssuer("6221260000000000"), "UnionPay")
    }
    
    // MARK: - Analysis Tests
    
    func testAnalyzeVisa() {
        let info = CreditCardUtils.analyze("4242424242424242")
        
        XCTAssertEqual(info.type, .visa)
        XCTAssertTrue(info.isValid)
        XCTAssertEqual(info.formattedNumber, "4242-4242-4242-4242")
        XCTAssertEqual(info.maskedNumber, "424242****4242")
        XCTAssertEqual(info.lastFourDigits, "4242")
        XCTAssertEqual(info.issuer, "Visa")
    }
    
    func testAnalyzeAmex() {
        let info = CreditCardUtils.analyze("378282246310005")
        
        XCTAssertEqual(info.type, .amex)
        XCTAssertTrue(info.isValid)
        XCTAssertEqual(info.formattedNumber, "3782-822463-10005")
        XCTAssertEqual(info.lastFourDigits, "0005")
    }
    
    func testAnalyzeWithExpiry() {
        let calendar = Calendar.current
        let currentYear = calendar.component(.year, from: Date())
        
        // Not expired
        let validInfo = CreditCardUtils.analyzeWithExpiry(
            "4242424242424242",
            expiryMonth: 12,
            expiryYear: currentYear + 1
        )
        XCTAssertTrue(validInfo.isValid)
        XCTAssertFalse(validInfo.isExpired!)
        
        // Expired
        let expiredInfo = CreditCardUtils.analyzeWithExpiry(
            "4242424242424242",
            expiryMonth: 1,
            expiryYear: currentYear - 1
        )
        XCTAssertFalse(expiredInfo.isValid)
        XCTAssertTrue(expiredInfo.isExpired!)
    }
    
    // MARK: - Test Number Generation Tests
    
    func testGenerateTestNumbers() {
        for type in [CreditCardType.visa, .mastercard, .amex, .discover] {
            let testNumber = CreditCardUtils.generateTestNumber(for: type)
            XCTAssertFalse(testNumber.isEmpty, "Generated number for \(type) should not be empty")
            XCTAssertEqual(CreditCardUtils.detectCardType(testNumber), type, "Generated number should match \(type) type")
            XCTAssertTrue(CreditCardUtils.luhnCheck(testNumber), "Generated \(type) number should pass Luhn check")
            XCTAssertTrue(CreditCardUtils.isValid(testNumber), "Generated \(type) number should be valid")
        }
    }
    
    // MARK: - String Extension Tests
    
    func testStringExtensions() {
        // Valid card
        let validCard = "4242424242424242"
        XCTAssertTrue(validCard.isValidCreditCard)
        XCTAssertEqual(validCard.creditCardType, .visa)
        XCTAssertEqual(validCard.formattedCreditCard, "4242-4242-4242-4242")
        XCTAssertEqual(validCard.maskedCreditCard, "424242****4242")
        
        // Invalid card
        let invalidCard = "123456"
        XCTAssertFalse(invalidCard.isValidCreditCard)
    }
    
    // MARK: - Sanitize Tests
    
    func testSanitize() {
        XCTAssertEqual(CreditCardUtils.sanitize("4242-4242-4242-4242"), "4242424242424242")
        XCTAssertEqual(CreditCardUtils.sanitize("4242 4242 4242 4242"), "4242424242424242")
        XCTAssertEqual(CreditCardUtils.sanitize("4242 4242-4242 4242"), "4242424242424242")
        XCTAssertEqual(CreditCardUtils.sanitize(" 4242424242424242 "), "4242424242424242")
        XCTAssertEqual(CreditCardUtils.sanitize("abcd4242424242424242efgh"), "4242424242424242")
    }
    
    // MARK: - Card Type Properties Tests
    
    func testCardTypeLengthRange() {
        XCTAssertEqual(CreditCardType.visa.lengthRange, 13...16)
        XCTAssertEqual(CreditCardType.mastercard.lengthRange, 16...16)
        XCTAssertEqual(CreditCardType.amex.lengthRange, 15...15)
        XCTAssertEqual(CreditCardType.discover.lengthRange, 16...19)
    }
    
    func testCardTypeCVVLength() {
        XCTAssertEqual(CreditCardType.visa.cvvLength, 3)
        XCTAssertEqual(CreditCardType.mastercard.cvvLength, 3)
        XCTAssertEqual(CreditCardType.amex.cvvLength, 4)
        XCTAssertEqual(CreditCardType.discover.cvvLength, 3)
    }
    
    // MARK: - Edge Case Tests
    
    func testEmptyCardNumber() {
        XCTAssertFalse(CreditCardUtils.isValid(""))
        XCTAssertEqual(CreditCardUtils.detectCardType(""), .unknown)
        XCTAssertEqual(CreditCardUtils.format(""), "")
        XCTAssertEqual(CreditCardUtils.mask(""), "")
    }
    
    func testShortCardNumber() {
        XCTAssertFalse(CreditCardUtils.isValid("123"))
        XCTAssertEqual(CreditCardUtils.lastFour("123"), "123")
        XCTAssertEqual(CreditCardUtils.mask("123"), "***")
    }
    
    func testLongCardNumber() {
        let longNumber = "4242424242424242424242424242"
        XCTAssertFalse(CreditCardUtils.isValid(longNumber)) // Too long
        XCTAssertEqual(CreditCardUtils.lastFour(longNumber), "2424")
    }
    
    func testNonNumericInput() {
        XCTAssertFalse(CreditCardUtils.isValid("abcd-efgh-ijkl-mnop"))
        XCTAssertFalse(CreditCardUtils.isValid(" Visa 4242 "))
        
        let sanitized = CreditCardUtils.sanitize("a4b2c4d2e4f2g4h2i4j2k4l2m4n2o4")
        XCTAssertEqual(sanitized, "4242424242424242")
        XCTAssertTrue(CreditCardUtils.isValid(sanitized))
    }
    
    // MARK: - Performance Tests
    
    func testValidationPerformance() {
        // Test that validation is fast enough for real-time use
        measure {
            for _ in 0..<1000 {
                _ = CreditCardUtils.isValid("4242424242424242")
            }
        }
    }
    
    func testTypeDetectionPerformance() {
        measure {
            for _ in 0..<1000 {
                _ = CreditCardUtils.detectCardType("4242424242424242")
            }
        }
    }
}

// MARK: - Test Runner

#if DEBUG
func runAllTests() {
    // This function can be called to run tests without XCTest framework
    print("Running CreditCardUtils Tests...")
    
    let tests = CreditCardUtilsTests()
    
    // Run a selection of key tests
    do {
        try tests.testVisaDetection()
        print("✅ Visa Detection - PASSED")
    } catch {
        print("❌ Visa Detection - FAILED")
    }
    
    do {
        try tests.testLuhnValidCards()
        print("✅ Luhn Valid Cards - PASSED")
    } catch {
        print("❌ Luhn Valid Cards - FAILED")
    }
    
    do {
        try tests.testValidCardNumbers()
        print("✅ Valid Card Numbers - PASSED")
    } catch {
        print("❌ Valid Card Numbers - FAILED")
    }
    
    do {
        try tests.testFormatVisa()
        print("✅ Format Visa - PASSED")
    } catch {
        print("❌ Format Visa - FAILED")
    }
    
    do {
        try tests.testMaskDefault()
        print("✅ Mask Default - PASSED")
    } catch {
        print("❌ Mask Default - FAILED")
    }
    
    do {
        try tests.testAnalyzeVisa()
        print("✅ Analyze Visa - PASSED")
    } catch {
        print("❌ Analyze Visa - FAILED")
    }
    
    do {
        try tests.testGenerateTestNumbers()
        print("✅ Generate Test Numbers - PASSED")
    } catch {
        print("❌ Generate Test Numbers - FAILED")
    }
    
    print("\nAll tests completed!")
}
#endif