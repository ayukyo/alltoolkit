/**
 * AllToolkit - Kotlin DateTime Utilities Test
 * 
 * 日期时间工具类单元测试
 * 覆盖正常场景、边界值、异常情况
 * 
 * @author AllToolkit
 * @version 1.0.0
 */

import org.junit.Test
import org.junit.Assert.*
import java.time.Instant
import java.time.LocalDateTime
import java.time.ZoneId

class DateTimeUtilsTest {

    @Test
    fun testCurrentTimeMillis() {
        val before = System.currentTimeMillis()
        val result = DateTimeUtils.currentTimeMillis()
        val after = System.currentTimeMillis()
        assertTrue(result >= before && result <= after)
    }

    @Test
    fun testCurrentTimeSeconds() {
        val millis = DateTimeUtils.currentTimeMillis()
        val seconds = DateTimeUtils.currentTimeSeconds()
        assertEquals(millis / 1000, seconds)
    }

    @Test
    fun testFormatTimestamp() {
        val timestamp = 1705315800000L
        val result = DateTimeUtils.format(timestamp, "yyyy-MM-dd HH:mm:ss")
        assertNotNull(result)
        assertTrue(result.contains("2024"))
    }

    @Test
    fun testParseToMillis() {
        val dateString = "2024-01-15 10:30:00"
        val result = DateTimeUtils.parseToMillis(dateString)
        assertNotNull(result)
        assertTrue(result!! > 0)
    }

    @Test
    fun testParseToMillisInvalidFormat() {
        val result = DateTimeUtils.parseToMillis("invalid-date")
        assertNull(result)
    }

    @Test
    fun testGetRelativeTimeDescJustNow() {
        val now = DateTimeUtils.currentTimeMillis()
        val result = DateTimeUtils.getRelativeTimeDesc(now)
        assertEquals("刚刚", result)
    }

    @Test
    fun testGetRelativeTimeDescMinutesAgo() {
        val fiveMinutesAgo = DateTimeUtils.currentTimeMillis() - 5 * 60 * 1000
        val result = DateTimeUtils.getRelativeTimeDesc(fiveMinutesAgo)
        assertEquals("5分钟前", result)
    }

    @Test
    fun testDaysBetween() {
        val start = DateTimeUtils.parseToMillis("2024-01-01 00:00:00")!!
        val end = DateTimeUtils.parseToMillis("2024-01-10 00:00:00")!!
        val result = DateTimeUtils.daysBetween(start, end)
        assertEquals(9, result)
    }

    @Test
    fun testIsLeapYear() {
        assertTrue(DateTimeUtils.isLeapYear(2024))
        assertFalse(DateTimeUtils.isLeapYear(2023))
        assertTrue(DateTimeUtils.isLeapYear(2000))
        assertFalse(DateTimeUtils.isLeapYear(1900))
    }

    @Test
    fun testGetDaysInMonth() {
        assertEquals(31, DateTimeUtils.getDaysInMonth(2024, 1))
        assertEquals(29, DateTimeUtils.getDaysInMonth(2024, 2)) // Leap year
        assertEquals(28, DateTimeUtils.getDaysInMonth(2023, 2)) // Non-leap year
        assertEquals(30, DateTimeUtils.getDaysInMonth(2024, 4))
    }

    @Test
    fun testAddDays() {
        val timestamp = DateTimeUtils.parseToMillis("2024-01-01 00:00:00")!!
        val result = DateTimeUtils.addDays(timestamp, 5)
        val formatted = DateTimeUtils.format(result, "yyyy-MM-dd")
        assertEquals("2024-01-06", formatted)
    }

    @Test
    fun testAddHours() {
        val timestamp = DateTimeUtils.parseToMillis("2024-01-01 00:00:00")!!
        val result = DateTimeUtils.addHours(timestamp, 5)
        val diff = (result - timestamp) / (60 * 60 * 1000)
        assertEquals(5, diff)
    }

    @Test
    fun testGetAge() {
        // Test with a birth date 25 years ago
        val birthYear = java.time.Year.now().value - 25
        val birthTimestamp = DateTimeUtils.parseToMillis("$birthYear-01-01 00:00:00")!!
        val age = DateTimeUtils.getAge(birthTimestamp)
        assertTrue(age >= 24 && age <= 25)
    }

    @Test
    fun testFormatDuration() {
        assertEquals("5秒", DateTimeUtils.formatDuration(5000))
        assertEquals("1分", DateTimeUtils.formatDuration(60000))
        assertEquals("1小时", DateTimeUtils.formatDuration(3600000))
        assertEquals("1天", DateTimeUtils.formatDuration(86400000))
    }

    @Test
    fun testFormatDurationShort() {
        assertEquals("00:05", DateTimeUtils.formatDurationShort(5000))
        assertEquals("01:00", DateTimeUtils.formatDurationShort(60000))
        assertEquals("01:00:00", DateTimeUtils.formatDurationShort(3600000))
    }

    @Test
    fun testSecondsToMillis() {
        assertEquals(5000, DateTimeUtils.secondsToMillis(5))
        assertEquals(0, DateTimeUtils.secondsToMillis(0))
    }

    @Test
    fun testMillisToSeconds() {
        assertEquals(5, DateTimeUtils.millisToSeconds(5000))
        assertEquals(0, DateTimeUtils.millisToSeconds(0))
    }

    @Test
    fun testIsWeekday() {
        // Monday, January 15, 2024
        val monday = DateTimeUtils.parseToMillis("2024-01-15 12:00:00")!!
        assertTrue(DateTimeUtils.isWeekday(monday))
        
        // Saturday, January 13, 2024
        val saturday = DateTimeUtils.parseToMillis("2024-01-13 12:00:00")!!
        assertFalse(DateTimeUtils.isWeekday(saturday))
    }

    @Test
    fun testIsWeekend() {
        // Saturday
        val saturday = DateTimeUtils.parseToMillis("2024-01-13 12:00:00")!!
        assertTrue(DateTimeUtils.isWeekend(saturday))
        
        // Monday
        val monday = DateTimeUtils.parseToMillis("2024-01-15 12:00:00")!!
        assertFalse(DateTimeUtils.isWeekend(monday))
    }

    @Test
    fun testGenerateTimeRanges() {
        val start = DateTimeUtils.parseToMillis("2024-01-01 00:00:00")!!
        val end = DateTimeUtils.parseToMillis("2024-01-01 01:00:00")!!
        val ranges = DateTimeUtils.generateTimeRanges(start, end, 15)
        
        assertEquals(5, ranges.size) // 00:00, 00:15, 00:30, 00:45, 01:00
        assertEquals(start, ranges[0])
    }
}
