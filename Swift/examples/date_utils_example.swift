/**
 * AllToolkit - Swift DateUtils 使用示例
 *
 * 演示 DateUtils 扩展的各种功能用法
 *
 * 运行方式:
 * 1. 在 Xcode 中创建 Swift 项目
 * 2. 将 DateUtils.swift 和本文件添加到项目中
 * 3. 在需要时 import Foundation
 * 4. 直接调用 Date 的扩展方法
 */

import Foundation

// MARK: - 示例运行函数

func runDateUtilsExamples() {
    print("=== Swift DateUtils 使用示例 ===\n")
    
    let now = Date()
    print("当前时间: \(now)")
    print()
    
    // MARK: 格式化方法
    print("--- 格式化方法 ---")
    print("string() [默认]: \(now.string())")
    print("dateString(): \(now.dateString())")
    print("timeString(): \(now.timeString())")
    print("iso8601String(): \(now.iso8601String())")
    print("chineseDateString(): \(now.chineseDateString())")
    print()
    
    // MARK: 相对时间
    print("--- 相对时间 ---")
    let fiveMinutesAgo = now.addingMinutes(-5)
    let twoHoursAgo = now.addingHours(-2)
    let yesterday = now.addingDays(-1)
    let threeDaysAgo = now.addingDays(-3)
    
    print("5分钟前: \(fiveMinutesAgo.relativeTimeString())")
    print("2小时前: \(twoHoursAgo.relativeTimeString())")
    print("昨天: \(yesterday.relativeTimeString())")
    print("3天前: \(threeDaysAgo.relativeTimeString())")
    print()
    
    // MARK: 日期计算
    print("--- 日期计算 ---")
    print("当前: \(now.dateTimeString())")
    print("+1年: \(now.addingYears(1).dateTimeString())")
    print("+1月: \(now.addingMonths(1).dateTimeString())")
    print("+7天: \(now.addingDays(7).dateTimeString())")
    print("+2小时: \(now.addingHours(2).dateTimeString())")
    print("+30分钟: \(now.addingMinutes(30).dateTimeString())")
    print()
    
    // MARK: 日期比较
    print("--- 日期比较 ---")
    print("isToday: \(now.isToday)")
    print("isYesterday: \(yesterday.isYesterday)")
    print("isTomorrow: \(now.addingDays(1).isTomorrow)")
    print("isThisWeek: \(now.isThisWeek)")
    print("isThisMonth: \(now.isThisMonth)")
    print("isThisYear: \(now.isThisYear)")
    
    let startOfMonth = now.startOfMonth
    let endOfMonth = now.endOfMonth
    print("isBetween(月初, 月末): \(now.isBetween(startOfMonth, and: endOfMonth))")
    print()
    
    // MARK: 日期组件
    print("--- 日期组件 ---")
    print("year: \(now.year)")
    print("month: \(now.month)")
    print("day: \(now.day)")
    print("hour: \(now.hour)")
    print("minute: \(now.minute)")
    print("second: \(now.second)")
    print("weekday: \(now.weekday)")
    print("weekdayName: \(now.weekdayName)")
    print("weekdayNameEnglish: \(now.weekdayNameEnglish)")
    print()
    
    // MARK: 日期边界
    print("--- 日期边界 ---")
    print("startOfDay: \(now.startOfDay.dateTimeString())")
    print("endOfDay: \(now.endOfDay.dateTimeString())")
    print("startOfWeek: \(now.startOfWeek.dateTimeString())")
    print("endOfWeek: \(now.endOfWeek.dateTimeString())")
    print("startOfMonth: \(now.startOfMonth.dateString())")
    print("endOfMonth: \(now.endOfMonth.dateString())")
    print()
    
    // MARK: 日期差值
    print("--- 日期差值 ---")
    let nextWeek = now.addingDays(7)
    print("daysUntil(下周): \(now.daysUntil(nextWeek))")
    print("hoursUntil(明天): \(now.hoursUntil(now.addingDays(1)))")
    print("minutesUntil(1小时后): \(now.minutesUntil(now.addingHours(1)))")
    
    let birthDate = Date.from(year: 1990, month: 1, day: 1)!
    print("age(1990-01-01): \(birthDate.age)")
    print()
    
    // MARK: 字符串解析
    print("--- 字符串解析 ---")
    let dateString = "2024-03-15 14:30:00"
    if let parsedDate = Date.parse(dateString, format: Date.dateTimeFormat) {
        print("解析 '\(dateString)': \(parsedDate.chineseDateTimeString())")
    }
    
    let isoString = "2024-03-15T14:30:00.000+0800"
    if let parsedISO = Date.parseISO8601(isoString) {
        print("解析 ISO8601: \(parsedISO.dateTimeString())")
    }
    
    if let fromComponents = Date.from(year: 2024, month: 12, day: 25, hour: 10, minute: 0, second: 0) {
        print("fromComponents: \(fromComponents.chineseDateTimeString())")
    }
    print()
    
    // MARK: 时间戳
    print("--- 时间戳 ---")
    print("timestamp: \(now.timestamp)")
    print("timestampMilliseconds: \(now.timestampMilliseconds)")
    
    if let fromTimestamp = Date.fromTimestamp(now.timestamp) {
        print("fromTimestamp: \(fromTimestamp.dateTimeString())")
    }
    print()
    
    // MARK: 辅助方法
    print("--- 辅助方法 ---")
    print("daysInMonth: \(now.daysInMonth)")
    print("isLeapYear: \(now.isLeapYear)")
    print("isWeekend: \(now.isWeekend)")
    print("isWeekday: \(now.isWeekday)")
    print()
    
    print("=== 示例运行完成 ===")
}

// MARK: - 运行示例

runDateUtilsExamples()
