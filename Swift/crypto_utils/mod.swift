import Foundation
import CryptoKit

public enum HashAlgorithm: String, CaseIterable {
    case md5 = "MD5"
    case sha1 = "SHA1"
    case sha256 = "SHA256"
    case sha384 = "SHA384"
    case sha512 = "SHA512"
}

public struct CryptoUtils {

    public static let lowercaseLetters = "abcdefghijklmnopqrstuvwxyz"
    public static let uppercaseLetters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    public static let digits = "0123456789"
    public static let specialCharacters = "!@#$%^&*()-_=+[]{}|;:,.<>?"
    public static let hexCharacters = "0123456789abcdef"
    public static let hexCharactersUpper = "0123456789ABCDEF"
    public static let urlSafeCharacters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_"
    public static let alphanumeric = lowercaseLetters + uppercaseLetters + digits
    public static let allCharacters = alphanumeric + specialCharacters

    // MARK: - Hash Functions

    public static func md5(_ input: String) -> String {
        guard let data = input.data(using: .utf8) else { return "" }
        let digest = Insecure.MD5.hash(data: data)
        return digest.map { String(format: "%02x", $0) }.joined()
    }

    public static func sha1(_ input: String) -> String {
        guard let data = input.data(using: .utf8) else { return "" }
        let digest = Insecure.SHA1.hash(data: data)
        return digest.map { String(format: "%02x", $0) }.joined()
    }

    public static func sha256(_ input: String) -> String {
        guard let data = input.data(using: .utf8) else { return "" }
        let digest = SHA256.hash(data: data)
        return digest.map { String(format: "%02x", $0) }.joined()
    }

    public static func sha384(_ input: String) -> String {
        guard let data = input.data(using: .utf8) else { return "" }
        let digest = SHA384.hash(data: data)
        return digest.map { String(format: "%02x", $0) }.joined()
    }

    public static func sha512(_ input: String) -> String {
        guard let data = input.data(using: .utf8) else { return "" }
        let digest = SHA512.hash(data: data)
        return digest.map { String(format: "%02x", $0) }.joined()
    }

    public static func hash(data: Data, algorithm: HashAlgorithm) -> String {
        switch algorithm {
        case .md5:
            return Insecure.MD5.hash(data: data).map { String(format: "%02x", $0) }.joined()
        case .sha1:
            return Insecure.SHA1.hash(data: data).map { String(format: "%02x", $0) }.joined()
        case .sha256:
            return SHA256.hash(data: data).map { String(format: "%02x", $0) }.joined()
        case .sha384:
            return SHA384.hash(data: data).map { String(format: "%02x", $0) }.joined()
        case .sha512:
            return SHA512.hash(data: data).map { String(format: "%02x", $0) }.joined()
        }
    }

    // MARK: - HMAC Functions

    public static func hmacSha256(message: String, key: String) -> String {
        guard let messageData = message.data(using: .utf8),
              let keyData = key.data(using: .utf8) else { return "" }
        let symmetricKey = SymmetricKey(data: keyData)
        let signature = HMAC<SHA256>.authenticationCode(for: messageData, using: symmetricKey)
        return signature.map { String(format: "%02x", $0) }.joined()
    }

    public static func hmacSha512(message: String, key: String) -> String {
        guard let messageData = message.data(using: .utf8),
              let keyData = key.data(using: .utf8) else { return "" }
        let symmetricKey = SymmetricKey(data: keyData)
        let signature = HMAC<SHA512>.authenticationCode(for: messageData, using: symmetricKey)
        return signature.map { String(format: "%02x", $0) }.joined()
    }

    public static func verifyHmacSha256(message: String, key: String, hmac: String) -> Bool {
        let computed = hmacSha256(message: message, key: key)
        return computed.lowercased() == hmac.lowercased()
    }

    // MARK: - Base64 Encoding

    public static func base64Encode(_ input: String) -> String {
        guard let data = input.data(using: .utf8) else { return "" }
        return data.base64EncodedString()
    }

    public static func base64Decode(_ input: String) -> String? {
        guard let data = Data(base64Encoded: input) else { return nil }
        return String(data: data, encoding: .utf8)
    }

    public static func base64UrlEncode(_ input: String, padding: Bool = true) -> String {
        guard let data = input.data(using: .utf8) else { return "" }
        var encoded = data.base64EncodedString()
            .replacingOccurrences(of: "+", with: "-")
            .replacingOccurrences(of: "/", with: "_")
        if !padding {
            encoded = encoded.replacingOccurrences(of: "=", with: "")
        }
        return encoded
    }

    public static func base64UrlDecode(_ input: String) -> String? {
        var base64 = input
            .replacingOccurrences(of: "-", with: "+")
            .replacingOccurrences(of: "_", with: "/")
        let padding = 4 - (base64.count % 4)
        if padding != 4 {
            base64 += String(repeating: "=", count: padding)
        }
        guard let data = Data(base64Encoded: base64) else { return nil }
        return String(data: data, encoding: .utf8)
    }

    public static func isValidBase64(_ input: String) -> Bool {
        let base64Regex = "^[A-Za-z0-9+/]*={0,2}$"
        guard let regex = try? NSRegularExpression(pattern: base64Regex) else { return false }
        let range = NSRange(location: 0, length: input.utf16.count)
        return regex.firstMatch(in: input, options: [], range: range) != nil && input.count % 4 == 0
    }

    // MARK: - Hex Encoding

    public static func hexEncode(_ input: String) -> String {
        guard let data = input.data(using: .utf8) else { return "" }
        return data.map { String(format: "%02x", $0) }.joined()
    }

    public static func hexDecode(_ input: String) -> String? {
        var data = Data()
        var index = input.startIndex
        while index < input.endIndex {
            let nextIndex = input.index(index, offsetBy: 2, limitedBy: input.endIndex) ?? input.endIndex
            let byteString = String(input[index..<nextIndex])
            if let byte = UInt8(byteString, radix: 16) {
                data.append(byte)
            } else {
                return nil
            }
            index = nextIndex
        }
        return String(data: data, encoding: .utf8)
    }

    public static func isValidHex(_ input: String) -> Bool {
        let hexRegex = "^[0-9a-fA-F]+$"
        guard let regex = try? NSRegularExpression(pattern: hexRegex) else { return false }
        let range = NSRange(location: 0, length: input.utf16.count)
        return regex.firstMatch(in: input, options: [], range: range) != nil && input.count % 2 == 0
    }

    // MARK: - URL Encoding

    public static func urlEncode(_ input: String) -> String {
        return input.addingPercentEncoding(withAllowedCharacters: .urlQueryAllowed) ?? input
    }

    public static func urlDecode(_ input: String) -> String {
        return input.removingPercentEncoding ?? input
    }

    public static func urlEncodeComponent(_ input: String) -> String {
        var allowed = CharacterSet.urlQueryAllowed
        allowed.remove(charactersIn: "!*'();:@&=+$,/?%#[]")
        return input.addingPercentEncoding(withAllowedCharacters: allowed) ?? input
    }

    // MARK: - UUID Generation

    public static func uuid() -> String {
        return UUID().uuidString
    }

    public static func uuidUpper() -> String {
        return UUID().uuidString.uppercased()
    }

    public static func uuidSimple() -> String {
        return UUID().uuidString.replacingOccurrences(of: "-", with: "")
    }

    public static func isValidUuid(_ input: String) -> Bool {
        let uuidRegex = "^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$"
        guard let regex = try? NSRegularExpression(pattern: uuidRegex) else { return false }
        let range = NSRange(location: 0, length: input.utf16.count)
        return regex.firstMatch(in: input, options: [], range: range) != nil
    }

    // MARK: - Random Generation

    public static func randomString(length: Int, characters: String) -> String {
        guard length > 0, !characters.isEmpty else { return "" }
        var result = ""
        let chars = Array(characters)
        for _ in 0..<length {
            result.append(chars[Int.random(in: 0..<chars.count)])
        }
        return result
    }

    public static func randomAlphanumeric(length: Int) -> String {
        return randomString(length: length, characters: alphanumeric)
    }

    public static func randomNumeric(length: Int) -> String {
        return randomString(length: length, characters: digits)
    }

    public static func randomHex(length: Int) -> String {
        return randomString(length: length, characters: hexCharacters)
    }

    public static func randomPassword(length: Int) -> String {
        guard length >= 4 else { return "" }
        var password = ""
        password += randomString(length: 1, characters: lowercaseLetters)
        password += randomString(length: 1, characters: uppercaseLetters)
        password += randomString(length: 1, characters: digits)
        password += randomString(length: 1, characters: specialCharacters)
        if length > 4 {
            password += randomString(length: length - 4, characters: allCharacters)
        }
        return String(password.shuffled())
    }

    // MARK: - XOR Encryption

    public static func xorEncrypt(_ input: String, key: String) -> String {
        guard !key.isEmpty else { return input }
        let inputData = Array(input.utf8)
        let keyData = Array(key.utf8)
        var result = Data()
        for (i, byte) in inputData.enumerated() {
            result.append(byte ^ keyData[i % keyData.count])
        }
        return result.base64EncodedString()
    }

    public static func xorDecrypt(_ input: String, key: String) -> String? {
        guard !key.isEmpty else { return input }
        guard let data = Data(base64Encoded: input) else { return nil }
        let keyData = Array(key.utf8)
        var result = Data()
        for (i, byte) in data.enumerated() {
            result.append(byte ^ keyData[i % keyData.count])
        }
        return String(data: result, encoding: .utf8)
    }

    // MARK: - Validation

    public static func isValidMd5(_ input: String) -> Bool {
        return input.count == 32 && input.range(of: "^[0-9a-fA-F]{32}$", options: .regularExpression) != nil
    }

    public static func isValidSha1(_ input: String) -> Bool {
        return input.count == 40 && input.range(of: "^[0-9a-fA-F]{40}$", options: .regularExpression) != nil
    }

    public static func isValidSha256(_ input: String) -> Bool {
        return input.count == 64 && input.range(of: "^[0-9a-fA-F]{64}$", options: .regularExpression) != nil
    }

    public static func isValidHash(_ input: String, algorithm: HashAlgorithm) -> Bool {
        switch algorithm {
        case .md5:
            return isValidMd5(input)
        case .sha1:
            return isValidSha1(input)
        case .sha256:
            return isValidSha256(input)
        case .sha384:
            return input.count == 96 && input.range(of: "^[0-9a-fA-F]{96}$", options: .regularExpression) != nil
        case .sha512:
            return input.count == 128 && input.range(of: "^[0-9a-fA-F]{128}$", options: .regularExpression) != nil
        }
    }
}