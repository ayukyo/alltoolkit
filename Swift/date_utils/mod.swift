/**
 * AllToolkit - Swift Date Utilities
 *
 * 通用日期时间工具类，提供常用的时间格式化、计算和转换功能。
 * 零依赖，仅使用 Swift 标准库 Foundation。
 * 支持 iOS 13.0+, macOS 10.15+, watchOS 6.0+, tvOS 13.0+
 *
 * @author AllToolkit
 * @version 1.0.0
 */

import Foundation

// MARK: - Date 扩展

public extension Date {
    
    // MARK: 常用格式化字符串
    
    /// ISO 8601 标准格式: "yyyy-MM-dd'T'HH:mm:ss.SSSZ"
    static let iso8601Format = "yyyy-MM-dd'T'HH:mm:ss.SSSZ"
    /// 标准日期格式: "yyyy-MM-dd"
    static let dateFormat = "yyyy-MM-dd"
    /// 标准时间格式: "HH:mm:ss"
    static let timeFormat = "HH:mm:ss"
    /// 标准日期时间格式: "yyyy-MM-dd HH:mm:ss"
    static let dateTimeFormat = "yyyy-MM-dd HH:mm:ss"
    /// 紧凑日期时间格式: "yyyyMMddHHmmss"
    static let compactFormat = "yyyyMMddHHmmss"
    /// 中文日期格式: "yyyy年MM月dd日"
    static let chineseDateFormat = "yyyy年MM月dd日"
    /// 中文日期时间格式: "yyyy年MM月dd日 HH:mm:ss"
    static let chineseDateTimeFormat = "yyyy年MM月dd日 HH:mm:ss"
    
    // MARK: 格式化方法
    
    /**
     * 将日期格式化为指定格式的字符串
     *
     * @param format 日期格式字符串，默认为 "yyyy-MM-dd HH:mm:ss"
     * @param locale 区域设置，默认为当前区域
     * @param timeZone 时区，默认为当前时区
     * @return 格式化后的日期字符串
     */
    func string(format: String = Date.dateTimeFormat, locale: Locale = .current, timeZone: TimeZone = .current) -> String {
        let formatter = DateFormatter()
        formatter.dateFormat = format
        formatter.locale = locale
        formatter.timeZone = timeZone
        return formatter.string(from: self)
    }
    
    /**
     * 格式化为 ISO 8601 字符串
     *
     * @return ISO 8601 格式字符串
     */
    func iso8601String() -> String {
        return string(format: Date.iso8601Format)
    }
    
    /**
     * 格式化为日期字符串 (yyyy-MM-dd)
     *
     * @return 日期字符串
     */
    func dateString() -> String {
        return string(format: Date.dateFormat)
    }
    
    /**
     * 格式化为时间字符串 (HH:mm:ss)
     *
     * @return 时间字符串
     */
    func timeString() -> String {
        return string(format: Date.timeFormat)
    }
    
    /**
     * 格式化为中文日期字符串
     *
     * @return 中文日期字符串
     */
    func chineseDateString() -> String {
        return string(format: Date.chineseDateFormat)
    }
    
    /**
     * 格式化为相对时间描述
     * 如: "刚刚", "5分钟前", "2小时前", "昨天", "3天前"
     *
     * @return 相对时间描述字符串
     */
    func relativeTimeString() -> String {
        let calendar = Calendar.current
        let now = Date()
        let components = calendar.dateComponents([.second, .minute, .hour, .day, .weekOfYear, .month, .year], from: self, to: now)
        
        if let year = components.year, year > 0 {
            return "\(year)年前"
        }
        if let month = components.month, month > 0 {
            return "\(month)个月前"
        }
        if let week = components.weekOfYear, week > 0 {
            return "\(week)周前"
        }
        if let day = components.day, day > 0 {
            if day == 1 {
                return "昨天"
            }
            return "\(day)天前"
        }
        if let hour = components.hour, hour > 0 {
            return "\(hour)小时前"
        }
        if let minute = components.minute, minute > 0 {
            return "\(minute)分钟前"
        }
        if let second = components.second, second > 30 {
            return "\(second)秒前"
        }
        return "刚刚"
    }
    
    // MARK: 日期计算
    
    /**
     * 添加指定数量的年
     *
     * @param years 年数，可为负数
     * @return 新的日期
     */
    func addingYears(_ years: Int) -> Date {
        return Calendar.current.date(byAdding: .year, value: years, to: self) ?? self
    }
    
    /**
     * 添加指定数量的月
     *
     * @param months 月数，可为负数
     * @return 新的日期
     */
    func addingMonths(_ months: Int) -> Date {
        return Calendar.current.date(byAdding: .month, value: months, to: self) ?? self
    }
    
    /**
     * 添加指定数量的天
     *
     * @param days 天数，可为负数
     * @return 新的日期
     */
    func addingDays(_ days: Int) -> Date {
        return Calendar.current.date(byAdding: .day, value: days, to: self) ?? self
    }
    
    /**
     * 添加指定数量的小时
     *
     * @param hours 小时数，可为负数
     * @return 新的日期
     */
    func addingHours(_ hours: Int) -> Date {
        return Calendar.current.date(byAdding: .hour, value: hours, to: self) ?? self
    }
    
    /**
     * 添加指定数量的分钟
     *
     * @param minutes 分钟数，可为负数
     * @return 新的日期
     */
    func addingMinutes(_ minutes: Int) -> Date {
        return Calendar.current.date(byAdding: .minute, value: minutes, to: self) ?? self
    }
    
    /**
     * 添加指定数量的秒
     *
     * @param seconds 秒数，可为负数
     * @return 新的日期
     */
    func addingSeconds(_ seconds: Int) -> Date {
        return Calendar.current.date(byAdding: .second, value: seconds, to: self) ?? self
    }
    
    // MARK: 日期比较
    
    /**
     * 是否为同一天
     *
     * @param date 要比较的日期
     * @return true 如果是同一天
     */
    func isSameDay(as date: Date) -> Bool {
        return Calendar.current.isDate(self, inSameDayAs: date)
    }
    
    /**
     * 是否为今天
     *
     * @return true 如果是今天
     */
    var isToday: Bool {
        return Calendar.current.isDateInToday(self)
    }
    
    /**
     * 是否为昨天
     *
     * @return true 如果是昨天
     */
    var isYesterday: Bool {
        return Calendar.current.isDateInYesterday(self)
    }
    
    /**
     * 是否为明天
     *
     * @return true 如果是明天
     */
    var isTomorrow: Bool {
        return Calendar.current.isDateInTomorrow(self)
    }
    
    /**
     * 是否为本周
     *
     * @return true 如果在本周
     */
    var isThisWeek: Bool {
        return Calendar.current.isDate(self, equalTo: Date(), toGranularity: .weekOfYear)
    }
    
    /**
     * 是否为本月
     *
     * @return true 如果在本月
     */
    var isThisMonth: Bool {
        return Calendar.current.isDate(self, equalTo: Date(), toGranularity: .month)
    }
    
    /**
     * 是否为本年
     *
     * @return true 如果在本年
     */
    var isThisYear: Bool {
        return Calendar.current.isDate(self, equalTo: Date(), toGranularity: .year)
    }
    
    /**
     * 是否在两个日期之间（包含边界）
     *
     * @param startDate 开始日期
     * @param endDate 结束日期
     * @return true 如果在范围内
     */
    func isBetween(_ startDate: Date, and endDate: Date) -> Bool {
        return self >= startDate && self <= endDate
    }
    
    // MARK: 日期组件获取
    
    /**
     * 获取年份
     *
     * @return 年份
     */
    var year: Int {
        return Calendar.current.component(.year, from: self)
    }
    
    /**
     * 获取月份 (1-12)
     *
     * @return 月份
     */
    var month: Int {
        return Calendar.current.component(.month, from: self)
    }
    
    /**
     * 获取日期 (1-31)
     *
     * @return 日期
     */
    var day: Int {
        return Calendar.current.component(.day, from: self)
    }
    
    /**
     * 获取小时 (0-23)
     *
     * @return 小时
     */
    var hour: Int {
        return Calendar.current.component(.hour, from: self)
    }
    
    /**
     * 获取分钟 (0-59)
     *
     * @return 分钟
     */
    var minute: Int {
        return Calendar.current.component(.minute, from: self)
    }
    
    /**
     * 获取秒 (0-59)
     *
     * @return 秒
     */
    var second: Int {
        return Calendar.current.component(.second, from: self)
    }
    
    /**
     * 获取星期几 (1=周日, 2=周一, ..., 7=周六)
     *
     * @return 星期几
     */
    var weekday: Int {
        return Calendar.current.component(.weekday, from: self)
    }
    
    /**
     * 获取星期几的中文名称
     *
     * @return 星期几中文名称
     */
    var weekdayName: String {
        let names = ["", "周日", "周一", "周二", "周三", "周四", "周五", "周六"]
        return names[safe: weekday] ?? ""
    }
    
    /**
     * 获取星期几的英文名称
     *
     * @return 星期几英文名称
     */
    var weekday