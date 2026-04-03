/**
 * AllToolkit - Swift Date Utilities Test
 *
 * 日期时间工具类单元测试
 * 覆盖: 格式化、计算、比较、组件获取
 *
 * @author AllToolkit
 * @version 1.0.0
 */

import Foundation
import XCTest

@testable import DateUtils

class DateUtilsTest: XCTestCase {
    
    // MARK: - 格式化测试
    
    func testStringFormat() {
        let date = createDate(year: 2024, month: 1, day: 15, hour: 10, minute: 30, second: 0)
        let formatted = date.string(format: "yyyy-MM-dd HH:mm:ss")
        XCTAssertEqual(formatted, "2024-01-15 10:30:00")
    }
    
    func testISO8601String() {
        let date = createDate(year: 2024, month: 1, day: 15, hour: 10, minute: 30, second: 0)
        let isoString = date.iso8601String()
        XCTAssertTrue(isoString.contains("2024-01-15"))
    }
    
    func testDateString() {
        let date = createDate(year: 2024, month: 6, day: 20)
        XCTAssertEqual(date.dateString(), "2024-06-20")
    }
    
    func testTimeString() {
        let date = createDate(year: 2024, month: 1, day: 1, hour: 14, minute: 30, second: 45)
        XCTAssertEqual(date.timeString(), "14:30:45")
    }
    
    func testChineseDateString() {
        let date = createDate(year: 2024, month: 1, day: 15)
        XCTAssertEqual(date.chineseDateString(), "2024年01月15日")
    }
    
    // MARK: - 相对时间测试
    
    func testRelativeTimeJustNow() {
        let now = Date()
        let desc = now.relativeTimeString()
        XCTAssertEqual(desc, "刚刚")
    }
    
    func testRelativeTimeMinutesAgo() {
        let fiveMinutesAgo = Date().addingTimeInterval(-5 * 60)
        let desc = fiveMinutesAgo.relativeTimeString()
        XCTAssertEqual(desc, "5分钟前")
    }
    
    func testRelativeTimeHoursAgo() {
        let twoHoursAgo = Date().addingTimeInterval(-2 * 60 * 60)
        let desc = twoHoursAgo.relativeTimeString()
        XCTAssertEqual(desc, "2小时前")
    }
    
    func testRelativeTimeYesterday() {
        let yesterday = Date().addingTimeInterval(-24 * 60 * 60)
        let desc = yesterday.relativeTimeString()
        XCTAssertEqual(desc, "昨天")
    }
    
    func testRelativeTimeDaysAgo() {
        let threeDaysAgo = Date().addingTimeInterval(-3 * 24 * 60 * 60)
        let desc = threeDaysAgo.relativeTimeString()
        XCTAssertEqual(desc, "3天前")
    }
    
    // MARK: - 日期计算测试
    
    func testAddingDays() {
        let date = createDate(year: 2024, month: 1, day: 15)
        let newDate = date.addingDays(5)
        XCTAssertEqual(newDate.day, 20)
        XCTAssertEqual(newDate.month, 1)
    }
    
    func testAddingDaysNegative() {
        let date = createDate(year: 2024, month: 1, day: 15)
        let newDate = date.addingDays(-5)
        XCTAssertEqual(newDate.day, 10)
    }
    
    func testAddingMonths() {
        let date = createDate(year: 2024, month: 1, day: 15)
        let newDate = date.addingMonths(2)
        XCTAssertEqual(newDate.month, 3)
    }
    
    func testAddingMonthsCrossYear() {
        let date = createDate(year: 2024, month: 11, day: 15)
        let newDate = date.addingMonths(3)
        XCTAssertEqual(newDate.month, 2)
        XCTAssertEqual(newDate.year, 2025)
    }
    
    func testAddingYears() {
        let date = createDate(year: 2024, month: 6, day: 15)
        let newDate = date.addingYears(5)
        XCTAssertEqual(newDate.year, 2029)
    }
    
    func testAddingHours() {
        let date = createDate(year: 2024, month: 1, day: 1, hour: 10)
        let newDate = date.addingHours(5)
        XCTAssertEqual(newDate.hour, 15)
    }
    
    func testAddingMinutes() {
        let date = createDate(year: 2024, month: 1, day: 1, hour: 10, minute: 30)
        let newDate = date.addingMinutes(45)
        XCTAssertEqual(newDate.minute, 15)
        XCTAssertEqual(newDate.hour, 11)
    }
    
    // MARK: - 日期比较测试
    
    func testIsSameDay() {
        let date1 = createDate(year: 2024, month: 1, day: 15, hour: 10)
        let date2 = createDate(year: 2024, month: 1, day: 15, hour: 20)
        XCTAssertTrue(date1.isSameDay(as: date2))
    }
    
    func testIsNotSameDay() {
        let date1 = createDate(year: 2024, month: 1, day: 15)
        let date2 = createDate(year: 2024, month: 1, day: 16)
        XCTAssertFalse(date1.isSameDay(as: date2))
    }
    
    func testIsToday() {
        let today = Date()
        XCTAssertTrue(today.isToday)
    }
    
    func testIsYesterday() {
        let yesterday = Date().addingDays(-1)
        XCTAssertTrue(yesterday.isYesterday)
    }
    
    func testIsTomorrow() {
        let tomorrow = Date().addingDays(1)
        XCTAssertTrue(tomorrow.isTomorrow)
    }
    
    func testIsBetween() {
        let start = createDate(year: 2024, month: 1, day: 1)
        let end = createDate(year: 2024, month: 1, day: 31)
        let middle = createDate(year: 2024, month: 1, day: 15)
        XCTAssertTrue(middle.isBetween(start, and: end))
    }
    
    func testIsBetweenInclusive() {
        let start = createDate(year: 2024, month: 1, day: 15)
        let end = createDate(year: 2024, month: 1, day: 20)
        XCTAssertTrue(start.isBetween(start, and: end))
        XCTAssertTrue(end.isBetween(start, and: end))
    }
    
    // MARK: - 日期组件测试
    
    func testYear() {
        let date = createDate(year: 2024, month: 6, day: 15)
        XCTAssertEqual(date.year, 2024)
    }
    
    func testMonth() {
        let date = createDate(year: 2024, month: 6, day: 15)
        XCTAssertEqual(date.month, 6)
    }
    
    func testDay() {
        let date = createDate(year: 2024, month: 6, day: 15)
        XCTAssertEqual(date.day, 15)
    }
    
    func testHour() {
        let date = createDate(year: 2024, month: 1, day: 1, hour: 14)
        XCTAssertEqual(date.hour, 14)
    }
    
    func testMinute() {
        let date = createDate(year: 2024, month: 1, day: 1, minute: 30)
        XCTAssertEqual(date.minute, 30)
    }
    
    func testSecond() {
        let date = createDate(year: 2024, month: 1, day: 1, second: 45)
        XCTAssertEqual(date.second, 45)
    }
    
    func testWeekday() {
        // 2024-01-15 is Monday (2 in Calendar's weekday: 1=Sunday, 2=Monday)
        let date = createDate(year: 2024, month: 1, day: 15)
        XCTAssertEqual(date.weekday, 2)
    }
    
    func testWeekdayName() {
        let monday = createDate(year: 2024, month: 1, day: 15)
        XCTAssertEqual(monday.weekdayName, "周一")
    }
    
    // MARK: - 时间戳测试
    
    func testTimestamp() {
        let date = Date()
        let timestamp = date.timestamp()
        let expected = Int(date.timeIntervalSince1970)
        XCTAssertEqual(timestamp, expected)
    }
    
    func testTimestampMilliseconds() {
        let date = Date()
        let timestampMs = date.timestampMilliseconds()
        let expected = Int(date.timeIntervalSince1970 * 1000)
        XCTAssertEqual(timestampMs, expected)
    }
    
    // MARK: - 日期边界测试
    
    func testStartOfDay() {
        let date = createDate(year: 2024, month: 6, day: 15, hour: 14, minute: 30)
        let start = date.startOfDay
        XCTAssertEqual(start.hour, 0)
        XCTAssertEqual(start.minute, 0)
        XCTAssertEqual(start.second, 0)
        XCTAssertEqual(start.day, 15)
    }
    
    func testEndOfDay() {
        let date = createDate(year: 2024, month: 6, day: 15, hour: 14, minute: 30)
        let end = date.endOfDay
        XCTAssertEqual(end.hour, 23)
        XCTAssertEqual(end.minute, 59)
        XCTAssertEqual(end.second, 59)
    }
    
    func testStartOfMonth() {
        let date = createDate(year: 2024, month: 6, day: 15)
        let start = date.startOfMonth
        XCTAssertEqual(start.day, 1)
        XCTAssertEqual(start.month, 6)
    }
    
    func testEndOfMonth() {
        let date = createDate(year: 2024, month: 6, day: 15)
        let end = date.endOfMonth
        XCTAssertEqual(end.day, 30)
        XCTAssertEqual(end.month, 6)
    }
    
    func testEndOfMonthFebruaryLeap() {
        let date = createDate(year: 2024, month: 2, day: 15)
        let end = date.endOfMonth
        XCTAssertEqual(end.day, 29)
    }
    
    func testEndOfMonthFebruaryNonLeap() {
        let date = createDate(year: 2023, month: 2, day: 15)
        let end = date.endOfMonth
        XCTAssertEqual(end.day, 28)
    }
    
    // MARK: - 日期差值测试
    
    func testDaysSince() {
        let date1 = createDate(year: 2024, month: 1, day: 15)
        let date2 = createDate(year: 2024, month: 1, day: 20)
        let days = date2.days(since: date1)
        XCTAssertEqual(days, 5)
    }
    
    func testHoursSince() {
        let date1 = createDate(year: 2024, month: 1, day: 15, hour: 10)
        let date2 = createDate(year: 2024, month: 1, day: 15, hour: 15)
        let hours = date2.hours(since: date1)
        XCTAssertEqual(hours, 5)
    }
    
    func testMinutesSince() {
        let date1 = createDate(year: 2024, month: 1, day: 15, hour: 10, minute: 0)
        let date2 = createDate(year: 2024, month: 1, day: 15, hour: 10, minute: 45)
        let minutes = date2.minutes(since: date1)
        XCTAssertEqual(minutes, 45)
    }
    
    // MARK: - 特殊日期判断测试
    
    func testIsWeekend() {
        // 2024-01-13 is Saturday
        let saturday = createDate(year: 2024, month: 1, day: 13)
        XCTAssertTrue(saturday.isWeekend)
        
        // 2024-01-15 is Monday
        let monday = createDate(year: 2024, month: 1, day: 15)
        XCTAssertFalse(monday.isWeekend)
    }
    
    func testIsWeekday() {
        // 2024-01-15 is Monday
        let monday = createDate(year: 2024, month: 1, day: 15)
        XCTAssertTrue(monday.isWeekday)
        
        // 2024-01-13 is Saturday
        let saturday = createDate(year: 2024, month: 1, day: 13)
        XCTAssertFalse(saturday.isWeekday)
    }
    
    func testIsLeapYear() {
        let leapYear = createDate(year: 2024, month: 1, day: 1)
        XCTAssertTrue(leapYear.isLeapYear)
        
        let nonLeapYear = createDate(year: 2023, month: 1, day: 1)
        XCTAssertFalse(nonLeapYear.isLeapYear)
    }
    
    func testDaysInMonth() {
        let january = createDate(year: 2024, month: 1, day: 1)
        XCTAssertEqual(january.daysInMonth, 31)
        
        let april = createDate(year: 2024, month: 4, day: 1)
        XCTAssertEqual(april.daysInMonth, 30)
        
        let februaryLeap = createDate(year: 2024, month: 2, day: 1)
        XCTAssertEqual(februaryLeap.daysInMonth, 29)
        
        let februaryNonLeap = createDate(year: 2023, month: 2, day: 1)
        XCTAssertEqual(februaryNonLeap.daysInMonth, 28)
    }
    
    // MARK: - 年龄计算测试
    
    func testAge() {
        let birthDate = createDate(year: 2000, month: 1, day: 1)
        let age = birthDate.age()
        XCTAssertTrue(age >= 24)
    }
    
    // MARK: - 辅助方法
    
    private func createDate(year: Int, month: Int, day: Int, 
                           hour: Int = 0, minute: Int = 0, second: Int = 0) -> Date {
        var components = DateComponents()
        components.year = year
        components.month = month
        components.day = day
        components.hour = hour
        components.minute = minute
        components.second = second
        return Calendar.current.date(from: components)!
    }
}