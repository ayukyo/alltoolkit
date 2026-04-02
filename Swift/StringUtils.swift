/**
 * AllToolkit - Swift String Utilities
 *
 * 通用字符串工具类，提供常用的字符串处理、验证和转换功能。
 * 零依赖，仅使用 Swift 标准库。
 * 支持 iOS 13.0+, macOS 10.15+, watchOS 6.0+, tvOS 13.0+
 *
 * @author AllToolkit
 * @version 1.0.0
 */

import Foundation

// MARK: - String 扩展

public extension String {
    
    // MARK: 空值检查
    
    /**
     * 检查字符串是否为空或仅包含空白字符
     *
     * @return true 如果字符串为空或仅包含空白字符
     */
    var isBlank: Bool {
        return trimmingCharacters(in: .whitespacesAndNewlines).isEmpty
    }
    
    /**
     * 检查字符串是否不为空且不只包含空白字符
     *
     * @return true 如果字符串有实际内容
     */
    var isNotBlank: Bool {
        return !isBlank
    }
    
    // MARK: 子串操作
    
    /**
     * 安全地获取子字符串
     *
     * @param start 起始索引（包含）
     * @param end 结束索引（不包含）
     * @return 子字符串，如果索引无效则返回空字符串
     */
    func substring(start: Int, end: Int) -> String {
        guard start >= 0, end <= count, start < end else { return "" }
        let startIndex = index(self.startIndex, offsetBy: start)
        let endIndex = index(self.startIndex, offsetBy: end)
        return String(self[startIndex..<endIndex])
    }
    
    /**
     * 安全地获取从指定位置开始的子字符串
     *
     * @param from 起始索引（包含）
     * @return 子字符串，如果索引无效则返回空字符串
     */
    func substring(from: Int) -> String {
        guard from >= 0, from < count else { return "" }
        let startIndex = index(self.startIndex, offsetBy: from)
        return String(self[startIndex...])
    }
    
    /**
     * 安全地获取从开始到指定位置的子字符串
     *
     * @param to 结束索引（不包含）
     * @return 子字符串，如果索引无效则返回空字符串
     */
    func substring(to: Int) -> String {
        guard to > 0, to <= count else { return "" }
        let endIndex = index(self.startIndex, offsetBy: to)
        return String(self[..<endIndex])
    }
    
    /**
     * 限制字符串长度，超出部分用指定后缀替换
     *
     * @param length 最大长度
     * @param suffix 超出部分替换的后缀，默认为 "..."
     * @return 截断后的字符串
     */
    func truncate(_ length: Int, suffix: String = "...") -> String {
        guard count > length else { return self }
        let endLength = length - suffix.count
        guard endLength > 0 else { return suffix }
        return substring(to: endLength) + suffix
    }
    
    // MARK: 空白处理
    
    /**
     * 去除字符串两端的空白字符
     *
     * @return 去除两端空白后的字符串
     */
    func trimmed() -> String {
        return trimmingCharacters(in: .whitespacesAndNewlines)
    }
    
    /**
     * 去除字符串中所有空白字符
     *
     * @return 去除所有空白后的字符串
     */
    func removeAllWhitespaces() -> String {
        return replacingOccurrences(of: "\\s+", with: "", options: .regularExpression)
    }
    
    /**
     * 将多个连续空白字符替换为单个空格
     *
     * @return 规范化空白后的字符串
     */
    func normalizeWhitespaces() -> String {
        return replacingOccurrences(of: "\\s+", with: " ", options: .regularExpression)
            .trimmed()
    }
    
    // MARK: 验证方法
    
    /**
     * 验证是否为有效的邮箱地址
     *
     * @return true 如果是有效的邮箱格式
     */
    var isValidEmail: Bool {
        let pattern = "^[A-Za-z0-9+_.-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$"
        return isMatch(pattern: pattern)
    }
    
    /**
     * 验证是否为有效的手机号码（中国大陆）
     *
     * @return true 如果是有效的手机号
     */
    var isValidChinesePhone: Bool {
        let pattern = "^1[3-9]\\d{9}$"
        return isMatch(pattern: pattern)
    }
    
    /**
     * 验证是否为有效的 URL
     *
     * @return true 如果是有效的 URL
     */
    var isValidURL: Bool {
        guard let url = URL(string: self) else { return false }
        return url.scheme != nil && url.host != nil
    }
    
    /**
     * 验证是否为纯数字
     *
     * @return true 如果字符串只包含数字
     */
    var isNumeric: Bool {
        return !isEmpty && allSatisfy { $0.isNumber }
    }
    
    /**
     * 验证是否为纯字母
     *
     * @return true 如果字符串只包含字母
     */
    var isAlphabetic: Bool {
        return !isEmpty && allSatisfy { $0.isLetter }
    }
    
    /**
     * 验证是否为字母数字组合
     *
     * @return true 如果字符串只包含字母和数字
     */
    var isAlphanumeric: Bool {
        return !isEmpty && allSatisfy { $0.isLetter || $0.isNumber }
    }
    
    /**
     * 验证是否为有效的身份证号（中国大陆 18 位）
     *
     * @return true 如果是有效的身份证号
     */
    var isValidChineseIDCard: Bool {
        let pattern = "^[1-9]\\d{5}(18|19|20)\\d{2}(0[1-9]|1[0-2])(0[1-9]|[12]\\d|3[01])\\d{3}[\\dXx]$"
        guard isMatch(pattern: pattern) else { return false }
        return validateIDCardChecksum()
    }
    
    /**
     * 验证是否为有效的 IPv4 地址
     *
     * @return true 如果是有效的 IPv4 地址
     */
    var isValidIPv4: Bool {
        let parts = split(separator: ".")
        guard parts.count == 4 else { return false }
        return parts.allSatisfy { part in
            guard let num = Int(part), num >= 0, num <= 255 else { return false }
            return String(num) == part
        }
    }
    
    // MARK: 正则匹配
    
    /**
     * 检查字符串是否匹配正则表达式
     *
     * @param pattern 正则表达式模式
     * @return true 如果匹配成功
     */
    func isMatch(pattern: String) -> Bool {
        guard let regex = try? NSRegularExpression(pattern: pattern) else { return false }
        let range = NSRange(location: 0, length: utf16.count)
        return regex.firstMatch(in: self, options: [], range: range) != nil
    }
    
    /**
     * 提取所有匹配正则表达式的子串
     *
     * @param pattern 正则表达式模式
     * @return 匹配结果数组
     */
    func matches(pattern: String) -> [String] {
        guard let regex = try? NSRegularExpression(pattern: pattern) else { return [] }
        let range = NSRange(location: 0, length: utf16.count)
        let matches = regex.matches(in: self, options: [], range: range)
        return matches.compactMap { match in
            guard let range = Range(match.range, in: self) else { return nil }
            return String(self[range])
        }
    }
    
    /**
     * 提取第一个匹配正则表达式的子串
     *
     * @param pattern 正则表达式模式
     * @return 第一个匹配结果，如果没有则返回 nil
     */
    func firstMatch(pattern: String) -> String? {
        return matches(pattern: pattern).first
    }
    
    // MARK: 替换操作
    
    /**
     * 使用正则表达式替换匹配内容
     *
     * @param pattern 正则表达式模式
     * @param replacement 替换字符串
     * @return 替换后的字符串
     */
    func replacingMatches(pattern: String, with replacement: String) -> String {
        guard let regex = try? NSRegularExpression(pattern: pattern) else { return self }
        let range = NSRange(location: 0, length: utf16.count)
        return regex.stringByReplacingMatches(in: self, options: [], range: range, withTemplate: replacement)
    }
    
    /**
     * 移除 HTML 标签
     *
     * @return 去除 HTML 标签后的纯文本
     */
    func strippingHTML() -> String {
        return replacingMatches(pattern: "<[^>]+>", with: "")
    }
    
    // MARK: 编码/解码
    
    /**
     * URL 编码
     *
     * @param characterSet 允许的字符集，默认为 .urlQueryAllowed
     * @return URL 编码后的字符串
     */
    func urlEncoded(characterSet: CharacterSet = .urlQueryAllowed) -> String {
        return addingPercentEncoding(withAllowedCharacters: characterSet) ?? self
    }
    
    /**
     * URL 解码
     *
     * @return URL 解码后的字符串
     */
    func urlDecoded() -> String {
        return removingPercentEncoding ?? self
    }
    
    /**
     * Base64 编码
     *
     * @return Base64 编码后的字符串
     */
    func base64Encoded() -> String {
        return Data(utf8).base64EncodedString()
    }
    
    /**
     * Base64 解码
     *
     * @return Base64 解码后的字符串，失败返回 nil
     */
    func base64Decoded() -> String? {
        guard let data = Data(base64Encoded: self) else { return nil }
        return String(data: data, encoding: .utf8)
    }
    
    // MARK: 大小写转换
    
    /**
     * 转为驼峰命名（camelCase）
     * 如: "user_name" -> "userName", "User-Name" -> "userName"
     *
     * @return 驼峰命名字符串
     */
    func toCamelCase() -> String {
        let components = components(separatedBy: CharacterSet(charactersIn: "_- "))
        let first = components.first?.lowercased() ?? ""
        let rest = components.dropFirst().map { $0.prefix(1).uppercased() + $0.dropFirst().lowercased() }
        return first + rest.joined()
    }
    
    /**
     * 转为帕斯卡命名（PascalCase）
     * 如: "user_name" -> "UserName", "user-name" -> "UserName"
     *
     * @return 帕斯卡命名字符串
     */
    func toPascalCase() -> String {
        let components = components(separatedBy: CharacterSet(charactersIn: "_- "))
        return components
            .filter { !$0.isEmpty }
            .map { $0.prefix(1).uppercased() + $0.dropFirst().lowercased() }
            .joined()
    }
    
    /**
     * 转为蛇形命名（snake_case）
     * 如: "UserName" -> "user_name", "userName" -> "user_name"
     *
     * @return 蛇形命名字符串
     */
    func toSnakeCase() -> String {
        let pattern = "([a-z0-9])([A-Z])"
        let result = replacingMatches(pattern: pattern, with: "$1_$2")
        return result.lowercased().replacingOccurrences(of: "-", with: "_")
    }
    
    /**
     * 转为短横线命名（kebab-case）
     * 如: "UserName" -> "user-name", "user_name" -> "user-name"
     *
     * @return 短横线命名字符串
     */
    func toKebabCase() -> String {
        return toSnakeCase().replacingOccurrences(of: "_", with: "-")
    }
    
    // MARK: 其他工具方法
    
    /**
     * 重复字符串指定次数
     *
     * @param count 重复次数
     * @return 重复后的字符串
     */
    func repeated(_ count: Int) -> String {
        guard count > 0 else { return "" }
        return String(repeating: self, count: count)
    }
    
    /**
     * 在左侧填充字符至指定长度
     *
     * @param length 目标长度
     * @param character 填充字符，默认为空格
     * @return 填充后的字符串
     */
    func leftPadded(to length: Int, with character: Character = " ") -> String {
        guard count < length else { return self }
        let padding = String(repeating: character, count: length - count)
        return padding + self
    }
    
    /**
     * 在右侧填充字符至指定长度
     *
     * @param length 目标长度
     * @param character 填充字符，默认为空格
     * @return 填充后的字符串
     */
    func rightPadded(to length: Int, with character: Character = " ") -> String {
        guard count < length else { return self }
        let padding = String(repeating: character, count: length - count)
        return self + padding
    }
    
    /**
     * 计算字符串的 MD5 哈希值
     *
     * @return MD5 哈希字符串（小写）
     */
    func md5() -> String {
        let data = Data(utf8)
        var digest = [UInt8](repeating: 0, count: Int(CC_MD5_DIGEST_LENGTH))
        data.withUnsafeBytes { bytes in
            _ = CC_MD5(bytes.baseAddress, CC_LONG(data.count), &digest)
        }
        return digest.map { String(format: "%02x", $0) }.joined()
    }
    
    /**
     * 计算字符串的 SHA256 哈希值
     *
     * @return SHA256 哈希字符串（小写）
     */
    func sha256() -> String {
        let data = Data(utf8)
        var digest = [UInt8](repeating: 0, count: Int(CC_SHA256_DIGEST_LENGTH))
        data.withUnsafeBytes { bytes in
            _ = CC_SHA256(bytes.baseAddress, CC_LONG(data.count), &digest)
        }
        return digest.map { String(format: "%02x", $0) }.joined()
    }
    
    /**
     * 反转字符串
     *
     * @return 反转后的字符串
     */
    func reversed() -> String {
        return String(self.reversed())
    }
    
    /**
     * 检查是否包含子串（不区分大小写）
     *
     * @param substring 要查找的子串
     * @return true 如果包含
     */
    func containsCaseInsensitive(_ substring: String) -> Bool {
        return lowercased().contains(substring.lowercased())
    }
    
    /**
     * 安全地转换为 Int
     *
     * @return Int 值，转换失败返回 nil
     */
    func toInt() -> Int? {
        return Int(self)
    }
    
    /**
     * 安全地转换为 Double
     *
     * @return Double 值，转换失败返回 nil
     */
    func toDouble() -> Double? {
        return Double(self)
    }
    
    /**
     * 安全地转换为 Bool
     * 支持: "true", "yes", "1", "false", "no", "0"
     *
     * @return Bool 值，转换失败返回 nil
     */
    func toBool() -> Bool? {
        let lower = lowercased()
        if ["true", "yes", "1"].contains(lower) { return true }
        if ["false", "no", "0"].contains(lower) { return false }
        return nil
    }
    
    // MARK: 私有方法
    
    /**
     * 验证身份证校验码
     *
     * @return true 如果校验码正确
     */
    private func validateIDCardChecksum() -> Bool {
        let weights = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
        let checkCodes = ["1", "0", "X", "9", "8", "7", "6", "5", "4", "3", "2"]
        
        let idString = uppercased()
        guard idString.count == 18 else { return false }
        
        var sum = 0
        for i in 0..<17 {
            guard let digit = Int(String(idString[idString.index(idString.startIndex, offsetBy: i)])),
                  digit >= 0 && digit <= 9 else { return false }
            sum += digit * weights[i]
        }
        
        let checkCode = checkCodes[sum % 11]
        let lastChar = String(idString[idString.index(idString.startIndex, offsetBy: 17)])
        return lastChar == checkCode
    }
}

