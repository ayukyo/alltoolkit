/**
 * AllToolkit - Kotlin DateTimeUtils 使用示例
 *
 * 演示 DateTimeUtils 的各种功能用法
 */

fun main() {
    println("=== DateTimeUtils 使用示例 ===\n")
    
    // 1. 获取当前时间戳
    println("1. 获取当前时间戳")
    val currentMillis = DateTimeUtils.currentTimeMillis()
    val currentSeconds = DateTimeUtils.currentTimeSeconds()
    println("   当前毫秒时间戳: $currentMillis")
    println("   当前秒级时间戳: $currentSeconds")
    println()
    
    // 2. 格式化时间
    println("2. 格式化时间")
    println("   默认格式: ${DateTimeUtils.format(currentMillis)}")
    println("   日期格式: ${DateTimeUtils.format(currentMillis, DateTimeUtils.FORMAT_DATE)}")
    println("   时间格式: ${DateTimeUtils.format(currentMillis, DateTimeUtils.FORMAT_TIME)}")
    println("   ISO8601:  ${DateTimeUtils.format(currentMillis, DateTimeUtils.FORMAT_ISO8601)}")
    println("   紧凑格式: ${DateTimeUtils.format(currentMillis, DateTimeUtils.FORMAT_COMPACT)}")
    println()
    
    // 3. 解析时间字符串
    println("3. 解析时间字符串")
    val dateString = "2024-03-15 14:30:00"
    val parsedMillis = DateTimeUtils.parseToMillis(dateString)
    println("   解析 '$dateString' -> $parsedMillis")
    println("   验证: ${DateTimeUtils.format(parsedMillis ?: 0)}")
    println()
    
    // 4. 相对时间描述
    println("4. 相对时间描述")
    val now = DateTimeUtils.currentTimeMillis()
    println("   刚刚: ${DateTimeUtils.getRelativeTimeDesc(now)}")
    println("   5分钟前: ${DateTimeUtils.getRelativeTimeDesc(now - 5 * 60 * 1000)}")
    println("   2小时前: ${DateTimeUtils.getRelativeTimeDesc(now - 2 * 60 * 60 * 1000)}")
    println("   昨天: ${DateTimeUtils.getRelativeTimeDesc(now - 25 * 60 * 60 * 1000)}")
    println("   3天前: ${DateTimeUtils.getRelativeTimeDesc(now - 3 * 24 * 60 * 60 * 1000)}")
    println()
    
    // 5. 时间计算
    println("5. 时间计算")
    val yesterday = DateTimeUtils.addDays(now, -1)
    val tomorrow = DateTimeUtils.addDays(now, 1)
    val nextHour = DateTimeUtils.addHours(now, 1)
    println("   昨天: ${DateTimeUtils.format(yesterday)}")
    println("   明天: ${DateTimeUtils.format(tomorrow)}")
    println("   1小时后: ${DateTimeUtils.format(nextHour, DateTimeUtils.FORMAT_TIME)}")
    println()
    
    // 6. 日期判断
    println("6. 日期判断")
    println("   当前是今天: ${DateTimeUtils.isToday(now)}")
    println("   昨天是今天: ${DateTimeUtils.isToday(yesterday)}")
    println("   昨天是昨天: ${DateTimeUtils.isYesterday(yesterday)}")
    println("   当前是本周: ${DateTimeUtils.isThisWeek(now)}")
    println("   当前是工作日: ${DateTimeUtils.isWeekday(now)}")
    println("   当前是周末: ${DateTimeUtils.isWeekend(now)}")
    println("   今天是星期: ${DateTimeUtils.getWeekDay(now)}")
    println()
    
    // 7. 日期间隔
    println("7. 日期间隔")
    val startTime = DateTimeUtils.parseToMillis("2024-01-01 00:00:00") ?: 0
    val endTime = DateTimeUtils.parseToMillis("2024-03-15 12:00:00") ?: 0
    println("   从 2024-01-01 到 2024-03-15")
    println("   相差天数: ${DateTimeUtils.daysBetween(startTime, endTime)}")
    println("   相差小时: ${DateTimeUtils.hoursBetween(startTime, endTime)}")
    println()
    
    // 8. 获取当天开始/结束
    println("8. 获取当天范围")
    val startOfDay = DateTimeUtils.getStartOfDay()
    val endOfDay = DateTimeUtils.getEndOfDay()
    println("   今天开始: ${DateTimeUtils.format(startOfDay)}")
    println("   今天结束: ${DateTimeUtils.format(endOfDay)}")
    println()
    
    // 9. 闰年和月份天数
    println("9. 闰年和月份天数")
    println("   2024年是闰年: ${DateTimeUtils.isLeapYear(2024)}")
    println("   2023年是闰年: ${DateTimeUtils.isLeapYear(2023)}")
    println("   2024年2月天数: ${DateTimeUtils.getDaysInMonth(2024, 2)}")
    println("   2024年3月天数: ${DateTimeUtils.getDaysInMonth(2024, 3)}")
    println()
    
    // 10. 时长格式化
    println("10. 时长格式化")
    val duration1 = 3661000L  // 1小时1分1秒
    val duration2 = 90061000L // 25小时1分1秒
    println("   ${duration1}ms = ${DateTimeUtils.formatDuration(duration1)}")
    println("   ${duration2}ms = ${DateTimeUtils.formatDuration(duration2)}")
    println("   ${duration1}ms = ${DateTimeUtils.formatDurationShort(duration1)}")
    println("   ${duration2}ms = ${DateTimeUtils.formatDurationShort(duration2)}")
    println()
    
    // 11. 友好日期显示
    println("11. 友好日期显示")
    println("   当前: ${DateTimeUtils.getFriendlyDate(now)}")
    println("   昨天: ${DateTimeUtils.getFriendlyDate(yesterday)}")
    println("   3天前: ${DateTimeUtils.getFriendlyDate(DateTimeUtils.addDays(now, -3))}")
    println()
    
    // 12. 时间范围生成
    println("12. 时间范围生成（每30分钟一个点）")
    val ranges = DateTimeUtils.generateTimeRanges(
        DateTimeUtils.getStartOfDay(),
        DateTimeUtils.getEndOfDay(),
        30
    )
    println("   今天共生成 ${ranges.size} 个时间点")
    println("   前5个: ${ranges.take(5).map { DateTimeUtils.format(it, DateTimeUtils.FORMAT_TIME) }}")
    println()
    
    // 13. 年龄计算
    println("13. 年龄计算")
    val birthDate = DateTimeUtils.parseToMillis("1990-05-20 00:00:00") ?: 0
    println("   出生日期: ${DateTimeUtils.format(birthDate)}")
    println("   年龄: ${DateTimeUtils.getAge(birthDate)} 岁")
    println()
    
    // 14. 月份第一天/最后一天
    println("14. 月份边界")
    val firstDay = DateTimeUtils.getFirstDayOfMonth(2024, 2)
    val lastDay = DateTimeUtils.getLastDayOfMonth(2024, 2)
    println("   2024年2月第一天: ${DateTimeUtils.format(firstDay)}")
    println("   2024年2月最后一天: ${DateTimeUtils.format(lastDay)}")
    println()
    
    println("=== 示例结束 ===")
}
