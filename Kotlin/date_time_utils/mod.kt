/**
 * AllToolkit - Kotlin DateTime Utilities
 * 
 * 通用日期时间工具类，提供常用的时间格式化、计算和转换功能。
 * 零依赖，仅使用 Kotlin 标准库。
 *
 * @author AllToolkit
 * @version 1.0.0
 */

import java.time.*
import java.time.format.DateTimeFormatter
import java.time.temporal.ChronoUnit
import java.util.*

/**
 * 日期时间工具对象
 */
object DateTimeUtils {

    /**
     * 标准日期时间格式
     */
    const val FORMAT_DATETIME = "yyyy-MM-dd HH:mm:ss"
    const val FORMAT_DATE = "yyyy-MM-dd"
    const val FORMAT_TIME = "HH:mm:ss"
    const val FORMAT_ISO8601 = "yyyy-MM-dd'T'HH:mm:ss'Z'"
    const val FORMAT_COMPACT = "yyyyMMddHHmmss"

    /**
     * 获取当前时间戳（毫秒）
     *
     * @return 当前时间的毫秒时间戳
     */
    fun currentTimeMillis(): Long = System.currentTimeMillis()

    /**
     * 获取当前时间戳（秒）
     *
     * @return 当前时间的秒级时间戳
     */
    fun currentTimeSeconds(): Long = System.currentTimeMillis() / 1000

    /**
     * 格式化日期时间为字符串
     *
     * @param timestamp 毫秒时间戳
     * @param pattern 日期格式，默认为 "yyyy-MM-dd HH:mm:ss"
     * @return 格式化后的日期字符串
     */
    fun format(timestamp: Long, pattern: String = FORMAT_DATETIME): String {
        return format(Instant.ofEpochMilli(timestamp), pattern)
    }

    /**
     * 格式化 Instant 为字符串
     *
     * @param instant Instant 对象
     * @param pattern 日期格式
     * @param zoneId 时区，默认为系统默认时区
     * @return 格式化后的日期字符串
     */
    fun format(
        instant: Instant,
        pattern: String = FORMAT_DATETIME,
        zoneId: ZoneId = ZoneId.systemDefault()
    ): String {
        val formatter = DateTimeFormatter.ofPattern(pattern)
        return instant.atZone(zoneId).format(formatter)
    }

    /**
     * 格式化 LocalDateTime 为字符串
     *
     * @param localDateTime LocalDateTime 对象
     * @param pattern 日期格式
     * @return 格式化后的日期字符串
     */
    fun format(localDateTime: LocalDateTime, pattern: String = FORMAT_DATETIME): String {
        val formatter = DateTimeFormatter.ofPattern(pattern)
        return localDateTime.format(formatter)
    }

    /**
     * 解析日期字符串为时间戳
     *
     * @param dateString 日期字符串
     * @param pattern 日期格式
     * @return 毫秒时间戳，解析失败返回 null
     */
    fun parseToMillis(dateString: String, pattern: String = FORMAT_DATETIME): Long? {
        return try {
            val formatter = DateTimeFormatter.ofPattern(pattern)
            val localDateTime = LocalDateTime.parse(dateString, formatter)
            localDateTime.atZone(ZoneId.systemDefault()).toInstant().toEpochMilli()
        } catch (e: Exception) {
            null
        }
    }

    /**
     * 解析日期字符串为 LocalDateTime
     *
     * @param dateString 日期字符串
     * @param pattern 日期格式
     * @return LocalDateTime 对象，解析失败返回 null
     */
    fun parseToLocalDateTime(dateString: String, pattern: String = FORMAT_DATETIME): LocalDateTime? {
        return try {
            val formatter = DateTimeFormatter.ofPattern(pattern)
            LocalDateTime.parse(dateString, formatter)
        } catch (e: Exception) {
            null
        }
    }

    /**
     * 获取相对时间描述（如：3分钟前、2小时前、昨天等）
     *
     * @param timestamp 毫秒时间戳
     * @return 相对时间描述字符串
     */
    fun getRelativeTimeDesc(timestamp: Long): String {
        val now = currentTimeMillis()
        val diff = now - timestamp
        
        return when {
            diff < 0 -> "未来"
            diff < 60_000 -> "刚刚"
            diff < 3_600_000 -> "${diff / 60_000}分钟前"
            diff < 86_400_000 -> "${diff / 3_600_000}小时前"
            diff < 172_800_000 -> "昨天"
            diff < 604_800_000 -> "${diff / 86_400_000}天前"
            diff < 2_592_000_000 -> "${diff / 604_800_000}周前"
            diff < 31_536_000_000 -> "${diff / 2_592_000_000}个月前"
            else -> "${diff / 31_536_000_000}年前"
        }
    }

    /**
     * 计算两个时间戳之间的天数差
     *
     * @param startTimestamp 开始时间戳（毫秒）
     * @param endTimestamp 结束时间戳（毫秒）
     * @return 天数差（绝对值）
     */
    fun daysBetween(startTimestamp: Long, endTimestamp: Long): Long {
        val start = Instant.ofEpochMilli(startTimestamp).atZone(ZoneId.systemDefault()).toLocalDate()
        val end = Instant.ofEpochMilli(endTimestamp).atZone(ZoneId.systemDefault()).toLocalDate()
        return ChronoUnit.DAYS.between(start, end).let { kotlin.math.abs(it) }
    }

    /**
     * 计算两个时间戳之间的小时差
     *
     * @param startTimestamp 开始时间戳（毫秒）
     * @param endTimestamp 结束时间戳（毫秒）
     * @return 小时差（绝对值）
     */
    fun hoursBetween(startTimestamp: Long, endTimestamp: Long): Long {
        return kotlin.math.abs(endTimestamp - startTimestamp) / 3_600_000
    }

    /**
     * 判断是否为今天
     *
     * @param timestamp 毫秒时间戳
     * @return 是否为今天
     */
    fun isToday(timestamp: Long): Boolean {
        val target = Instant.ofEpochMilli(timestamp).atZone(ZoneId.systemDefault()).toLocalDate()
        val today = LocalDate.now()
        return target == today
    }

    /**
     * 判断是否为昨天
     *
     * @param timestamp 毫秒时间戳
     * @return 是否为昨天
     */
    fun isYesterday(timestamp: Long): Boolean {
        val target = Instant.ofEpochMilli(timestamp).atZone(ZoneId.systemDefault()).toLocalDate()
        val yesterday = LocalDate.now().minusDays(1)
        return target == yesterday
    }

    /**
     * 判断是否为本周
     *
     * @param timestamp 毫秒时间戳
     * @return 是否为本周
     */
    fun isThisWeek(timestamp: Long): Boolean {
        val target = Instant.ofEpochMilli(timestamp).atZone(ZoneId.systemDefault()).toLocalDate()
        val today = LocalDate.now()
        val weekStart = today.minusDays(today.dayOfWeek.value.toLong() - 1)
        val weekEnd = weekStart.plusDays(6)
        return !target.isBefore(weekStart) && !target.isAfter(weekEnd)
    }

    /**
     * 判断是否为闰年
     *
     * @param year 年份
     * @return 是否为闰年
     */
    fun isLeapYear(year: Int): Boolean {
        return Year.of(year).isLeap
    }

    /**
     * 获取某月的天数
     *
     * @param year 年份
     * @param month 月份（1-12）
     * @return 该月的天数
     */
    fun getDaysInMonth(year: Int, month: Int): Int {
        return YearMonth.of(year, month).lengthOfMonth()
    }

    /**
     * 获取当天的开始时间戳（00:00:00）
     *
     * @param timestamp 任意时间戳，默认为当前时间
     * @return 当天开始的时间戳（毫秒）
     */
    fun getStartOfDay(timestamp: Long = currentTimeMillis()): Long {
        return Instant.ofEpochMilli(timestamp)
            .atZone(ZoneId.systemDefault())
            .toLocalDate()
            .atStartOfDay(ZoneId.systemDefault())
            .toInstant()
            .toEpochMilli()
    }

    /**
     * 获取当天的结束时间戳（23:59:59.999）
     *
     * @param timestamp 任意时间戳，默认为当前时间
     * @return 当天结束的时间戳（毫秒）
     */
    fun getEndOfDay(timestamp: Long = currentTimeMillis()): Long {
        return Instant.ofEpochMilli(timestamp)
            .atZone(ZoneId.systemDefault())
            .toLocalDate()
            .plusDays(1)
            .atStartOfDay(ZoneId.systemDefault())
            .toInstant()
            .toEpochMilli() - 1
    }

    /**
     * 添加天数
     *
     * @param timestamp 基准时间戳
     * @param days 要添加的天数（可为负数）
     * @return 新的时间戳
     */
    fun addDays(timestamp: Long, days: Int): Long {
        return Instant.ofEpochMilli(timestamp)
            .atZone(ZoneId.systemDefault())
            .plusDays(days.toLong())
            .toInstant()
            .toEpochMilli()
    }

    /**
     * 添加小时数
     *
     * @param timestamp 基准时间戳
     * @param hours 要添加的小时数（可为负数）
     * @return 新的时间戳
     */
    fun addHours(timestamp: Long, hours: Int): Long {
        return timestamp + hours * 3_600_000L
    }

    /**
     * 添加分钟数
     *
     * @param timestamp 基准时间戳
     * @param minutes 要添加的分钟数（可为负数）
     * @return 新的时间戳
     */
    fun addMinutes(timestamp: Long, minutes: Int): Long {
        return timestamp + minutes * 60_000L
    }

    /**
     * 将秒级时间戳转换为毫秒级
     *
     * @param seconds 秒级时间戳
     * @return 毫秒级时间戳
     */
    fun secondsToMillis(seconds: Long): Long = seconds * 1000

    /**
     * 将毫秒级时间戳转换为秒级
     *
     * @param millis 毫秒级时间戳
     * @return 秒级时间戳
     */
    fun millisToSeconds(millis: Long): Long = millis / 1000

    /**
     * 获取年龄
     *
     * @param birthTimestamp 出生日期时间戳（毫秒）
     * @return 年龄（周岁）
     */
    fun getAge(birthTimestamp: Long): Int {
        val birthDate = Instant.ofEpochMilli(birthTimestamp)
            .atZone(ZoneId.systemDefault())
            .toLocalDate()
        val now = LocalDate.now()
        return Period.between(birthDate, now).years
    }

    /**
     * 获取指定月份的第一天时间戳
     *
     * @param year 年份
     * @param month 月份（1-12）
     * @return 该月第一天 00:00:00 的时间戳
     */
    fun getFirstDayOfMonth(year: Int, month: Int): Long {
        return YearMonth.of(year, month)
            .atDay(1)
            .atStartOfDay(ZoneId.systemDefault())
            .toInstant()
            .toEpochMilli()
    }

    /**
     * 获取指定月份的最后一天时间戳
     *
     * @param year 年份
     * @param month 月份（1-12）
     * @return 该月最后一天 23:59:59.999 的时间戳
     */
    fun getLastDayOfMonth(year: Int, month: Int): Long {
        return YearMonth.of(year, month)
            .atEndOfMonth()
            .plusDays(1)
            .atStartOfDay(ZoneId.systemDefault())
            .toInstant()
            .toEpochMilli() - 1
    }

    /**
     * 获取当前是星期几（中文）
     *
     * @param timestamp 时间戳，默认为当前时间
     * @return 星期几（一、二、三、四、五、六、日）
     */
    fun getWeekDay(timestamp: Long = currentTimeMillis()): String {
        val dayOfWeek = Instant.ofEpochMilli(timestamp)
            .atZone(ZoneId.systemDefault())
            .dayOfWeek
        return when (dayOfWeek) {
            DayOfWeek.MONDAY -> "一"
            DayOfWeek.TUESDAY -> "二"
            DayOfWeek.WEDNESDAY -> "三"
            DayOfWeek.THURSDAY -> "四"
            DayOfWeek.FRIDAY -> "五"
            DayOfWeek.SATURDAY -> "六"
            DayOfWeek.SUNDAY -> "日"
        }
    }

    /**
     * 判断是否为工作日（周一到周五）
     *
     * @param timestamp 时间戳，默认为当前时间
     * @return 是否为工作日
     */
    fun isWeekday(timestamp: Long = currentTimeMillis()): Boolean {
        val dayOfWeek = Instant.ofEpochMilli(timestamp)
            .atZone(ZoneId.systemDefault())
            .dayOfWeek
        return dayOfWeek != DayOfWeek.SATURDAY && dayOfWeek != DayOfWeek.SUNDAY
    }

    /**
     * 判断是否为周末
     *
     * @param timestamp 时间戳，默认为当前时间
     * @return 是否为周末
     */
    fun isWeekend(timestamp: Long = currentTimeMillis()): Boolean {
        val dayOfWeek = Instant.ofEpochMilli(timestamp)
            .atZone(ZoneId.systemDefault())
            .dayOfWeek
        return dayOfWeek == DayOfWeek.SATURDAY || dayOfWeek == DayOfWeek.SUNDAY
    }

    /**
     * 格式化时长（毫秒转换为可读格式）
     *
     * @param durationMillis 时长（毫秒）
     * @return 格式化后的时长字符串，如 "1天2小时3分4秒"
     */
    fun formatDuration(durationMillis: Long): String {
        if (durationMillis < 0) return "0秒"
        
        val seconds = durationMillis / 1000
        val minutes = seconds / 60
        val hours = minutes / 60
        val days = hours / 24
        
        val sb = StringBuilder()
        if (days > 0) sb.append("${days}天")
        if (hours % 24 > 0) sb.append("${hours % 24}小时")
        if (minutes % 60 > 0) sb.append("${minutes % 60}分")
        if (seconds % 60 > 0 || sb.isEmpty()) sb.append("${seconds % 60}秒")
        
        return sb.toString()
    }

    /**
     * 格式化时长为简短格式
     *
     * @param durationMillis 时长（毫秒）
     * @return 格式化后的时长字符串，如 "02:30:45"
     */
    fun formatDurationShort(durationMillis: Long): String {
        val totalSeconds = durationMillis / 1000
        val hours = totalSeconds / 3600
        val minutes = (totalSeconds % 3600) / 60
        val seconds = totalSeconds % 60
        
        return if (hours > 0) {
            String.format("%02d:%02d:%02d", hours, minutes, seconds)
        } else {
            String.format("%02d:%02d", minutes, seconds)
        }
    }

    /**
     * 获取友好的日期显示
     *
     * @param timestamp 时间戳
     * @return 友好的日期字符串，如 "今天 14:30"、"昨天 09:15"、"2024-01-15"
     */
    fun getFriendlyDate(timestamp: Long): String {
        return when {
            isToday(timestamp) -> "今天 ${format(timestamp, FORMAT_TIME)}"
            isYesterday(timestamp) -> "昨天 ${format(timestamp, FORMAT_TIME)}"
            else -> format(timestamp, FORMAT_DATE)
        }
    }

    /**
     * 生成时间范围列表（用于统计等场景）
     *
     * @param startTimestamp 开始时间戳
     * @param endTimestamp 结束时间戳
     * @param intervalMinutes 间隔分钟数
     * @return 时间戳列表
     */
    fun generateTimeRanges(
        startTimestamp: Long,
        endTimestamp: Long,
        intervalMinutes: Int
    ): List<Long> {
        val ranges = mutableListOf<Long>()
        var current = startTimestamp
        val intervalMillis = intervalMinutes * 60_000L
        
        while (current <= endTimestamp) {
            ranges.add(current)
            current += intervalMillis
        }
        
        return ranges
    }
}