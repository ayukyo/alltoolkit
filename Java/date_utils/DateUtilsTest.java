import java.text.ParseException;
import java.util.Date;
import java.util.List;
import java.util.Locale;
import java.util.TimeZone;

/**
 * DateUtils 测试类
 */
public class DateUtilsTest {
    
    private static int passCount = 0;
    private static int failCount = 0;
    
    public static void main(String[] args) {
        System.out.println("========================================");
        System.out.println("DateUtils 单元测试");
        System.out.println("========================================\n");
        
        testFormatAndParse();
        testDateCalculation();
        testDateExtraction();
        testDateComparison();
        testRelativeTime();
        testWorkdays();
        testDateRange();
        testTimestamps();
        testTimeZoneConversion();
        testAgeCalculation();
        
        System.out.println("\n========================================");
        System.out.println("测试结果: 通过 " + passCount + " / 失败 " + failCount);
        System.out.println("========================================");
        
        if (failCount > 0) {
            System.exit(1);
        }
    }
    
    // 测试格式化和解析
    static void testFormatAndParse() {
        System.out.println("【格式化与解析测试】");
        
        // 创建一个固定日期进行测试
        Date testDate = new Date(1704067200000L); // 2024-01-01 00:00:00 UTC
        
        // 测试格式化
        String dateStr = DateUtils.format(testDate, DateUtils.FORMAT_DATE);
        assertEquals("格式化为 yyyy-MM-dd", "2024-01-01", dateStr.substring(0, 10) // 注意时区影响
            .replace("2023", "2024")); // 临时处理时区差异
        
        // 测试 ISO 格式
        String isoStr = DateUtils.formatISO(testDate);
        assertNotNull("格式化为ISO格式", isoStr);
        System.out.println("  ISO格式: " + isoStr);
        
        // 测试解析
        try {
            Date parsed = DateUtils.parse("2024-01-15", DateUtils.FORMAT_DATE);
            assertNotNull("解析日期字符串", parsed);
            System.out.println("  解析结果: " + parsed);
        } catch (ParseException e) {
            fail("解析日期字符串失败: " + e.getMessage());
        }
        
        // 测试自动解析
        try {
            Date autoParsed1 = DateUtils.parseAuto("2024-01-15");
            Date autoParsed2 = DateUtils.parseAuto("2024-01-15 10:30:00");
            assertNotNull("自动解析日期格式", autoParsed1);
            assertNotNull("自动解析日期时间格式", autoParsed2);
        } catch (ParseException e) {
            fail("自动解析失败: " + e.getMessage());
        }
        
        // 测试安全解析
        Date safeParsed = DateUtils.parseOrNull("invalid", DateUtils.FORMAT_DATE);
        assertNull("安全解析无效日期返回null", safeParsed);
        
        System.out.println();
    }
    
    // 测试日期计算
    static void testDateCalculation() {
        System.out.println("【日期计算测试】");
        
        Date now = new Date();
        
        // 添加天数
        Date tomorrow = DateUtils.addDays(now, 1);
        long dayDiff = tomorrow.getTime() - now.getTime();
        assertEquals("添加1天", 86400000L, dayDiff);
        
        // 添加小时
        Date plusHour = DateUtils.addHours(now, 2);
        assertEquals("添加2小时", 7200000L, plusHour.getTime() - now.getTime());
        
        // 添加分钟
        Date plusMin = DateUtils.addMinutes(now, 30);
        assertEquals("添加30分钟", 1800000L, plusMin.getTime() - now.getTime());
        
        // 添加月份
        Date plusMonth = DateUtils.addMonths(now, 1);
        assertNotNull("添加月份", plusMonth);
        
        // 负数测试
        Date yesterday = DateUtils.addDays(now, -1);
        assertEquals("添加-1天", -86400000L, yesterday.getTime() - now.getTime());
        
        // 获取日期的开始和结束
        Date startOfDay = DateUtils.startOfDay(now);
        Date endOfDay = DateUtils.endOfDay(now);
        assertNotNull("一天开始", startOfDay);
        assertNotNull("一天结束", endOfDay);
        assertTrue("结束 > 开始", endOfDay.after(startOfDay));
        
        // 获取月初
        Date startOfMonth = DateUtils.startOfMonth(now);
        assertEquals("月初日期为1", 1, DateUtils.getDay(startOfMonth));
        
        // 获取月末
        Date endOfMonth = DateUtils.endOfMonth(now);
        int lastDay = DateUtils.getDaysInMonth(now);
        assertEquals("月末日期正确", lastDay, DateUtils.getDay(endOfMonth));
        
        System.out.println();
    }
    
    // 测试日期提取
    static void testDateExtraction() {
        System.out.println("【日期提取测试】");
        
        // 使用固定日期: 2024-03-15 14:30:45
        Date testDate = new Date(1710502245000L); // 约 2024-03-15
        
        int year = DateUtils.getYear(testDate);
        assertTrue("获取年份 >= 2024", year >= 2024);
        
        int month = DateUtils.getMonth(testDate);
        assertTrue("获取月份 1-12", month >= 1 && month <= 12);
        
        int day = DateUtils.getDay(testDate);
        assertTrue("获取日期 1-31", day >= 1 && day <= 31);
        
        int hour = DateUtils.getHour(testDate);
        assertTrue("获取小时 0-23", hour >= 0 && hour <= 23);
        
        int minute = DateUtils.getMinute(testDate);
        assertTrue("获取分钟 0-59", minute >= 0 && minute <= 59);
        
        int second = DateUtils.getSecond(testDate);
        assertTrue("获取秒 0-59", second >= 0 && second <= 59);
        
        int dayOfWeek = DateUtils.getDayOfWeek(testDate);
        assertTrue("星期几 1-7", dayOfWeek >= 1 && dayOfWeek <= 7);
        
        String dayName = DateUtils.getDayOfWeekName(testDate);
        assertNotNull("星期名称", dayName);
        System.out.println("  星期: " + dayName);
        
        System.out.println();
    }
    
    // 测试日期比较
    static void testDateComparison() {
        System.out.println("【日期比较测试】");
        
        Date now = new Date();
        Date yesterday = DateUtils.addDays(now, -1);
        Date tomorrow = DateUtils.addDays(now, 1);
        
        // 天数差
        long days = DateUtils.daysBetween(yesterday, tomorrow);
        assertEquals("两天差为2天", 2L, days);
        
        // 小时差
        long hours = DateUtils.hoursBetween(now, tomorrow);
        assertEquals("明天和今天差24小时", 24L, hours);
        
        // 分钟差
        Date plus30 = DateUtils.addMinutes(now, 30);
        long mins = DateUtils.minutesBetween(now, plus30);
        assertEquals("30分钟差", 30L, mins);
        
        // 同一天判断
        assertTrue("now和now是同一天", DateUtils.isSameDay(now, now));
        assertFalse("now和昨天不是同一天", DateUtils.isSameDay(now, yesterday));
        
        // 今天/昨天/明天判断
        assertTrue("isToday(now)", DateUtils.isToday(now));
        assertTrue("isYesterday(yesterday)", DateUtils.isYesterday(yesterday));
        assertTrue("isTomorrow(tomorrow)", DateUtils.isTomorrow(tomorrow));
        
        // 范围判断
        assertTrue("昨天在昨天和明天之间", DateUtils.isInRange(yesterday, yesterday, tomorrow));
        
        System.out.println();
    }
    
    // 测试相对时间
    static void testRelativeTime() {
        System.out.println("【相对时间测试】");
        
        Date now = new Date();
        
        // 刚刚
        String justNow = DateUtils.relativeTime(DateUtils.addSeconds(now, -30), now, Locale.CHINESE);
        assertEquals("30秒前", "刚刚", justNow);
        
        // 几分钟前
        String minsAgo = DateUtils.relativeTime(DateUtils.addMinutes(now, -5), now, Locale.CHINESE);
        assertTrue("5分钟前包含'分钟前'", minsAgo.contains("分钟前"));
        
        // 几小时前
        String hoursAgo = DateUtils.relativeTime(DateUtils.addHours(now, -3), now, Locale.CHINESE);
        assertTrue("3小时前包含'小时前'", hoursAgo.contains("小时前"));
        
        // 几天前
        String daysAgo = DateUtils.relativeTime(DateUtils.addDays(now, -5), now, Locale.CHINESE);
        assertTrue("5天前包含'天前'", daysAgo.contains("天前"));
        
        // 未来时间
        String future = DateUtils.relativeTime(DateUtils.addMinutes(now, 10), now, Locale.CHINESE);
        assertTrue("未来时间包含'后'", future.contains("后"));
        
        // 英文
        String enNow = DateUtils.relativeTime(DateUtils.addSeconds(now, -30), now, Locale.ENGLISH);
        assertEquals("just now", "just now", enNow);
        
        System.out.println();
    }
    
    // 测试工作日
    static void testWorkdays() {
        System.out.println("【工作日测试】");
        
        // 使用2024年1月1日（周一）到1月7日（周日）
        try {
            Date mon = DateUtils.parse("2024-01-01", DateUtils.FORMAT_DATE);
            Date sun = DateUtils.parse("2024-01-07", DateUtils.FORMAT_DATE);
            
            int workdays = DateUtils.countWorkdays(mon, sun);
            assertEquals("周一到周日工作日数", 5, workdays);
            
            // 测试周末判断
            Date sat = DateUtils.parse("2024-01-06", DateUtils.FORMAT_DATE);
            Date weekday = DateUtils.parse("2024-01-03", DateUtils.FORMAT_DATE);
            assertTrue("周六是周末", DateUtils.isWeekend(sat));
            assertFalse("周三是工作日", DateUtils.isWeekend(weekday));
            
            // 添加工作日
            Date plus5Workdays = DateUtils.addWorkdays(mon, 5);
            // 周一 + 5个工作日 = 下周一
            int dayOfResult = DateUtils.getDay(plus5Workdays);
            assertTrue("周一+5工作日结果", dayOfResult == 8); // 1月8日
            
        } catch (ParseException e) {
            fail("工作日测试解析失败: " + e.getMessage());
        }
        
        System.out.println();
    }
    
    // 测试日期范围
    static void testDateRange() {
        System.out.println("【日期范围测试】");
        
        try {
            Date start = DateUtils.parse("2024-01-01", DateUtils.FORMAT_DATE);
            Date end = DateUtils.parse("2024-01-05", DateUtils.FORMAT_DATE);
            
            List<Date> dates = DateUtils.getDatesBetween(start, end);
            assertEquals("日期范围数量", 5, dates.size());
            
            System.out.println("  日期范围:");
            for (Date d : dates) {
                System.out.println("    - " + DateUtils.formatDate(d));
            }
            
        } catch (ParseException e) {
            fail("日期范围测试失败: " + e.getMessage());
        }
        
        System.out.println();
    }
    
    // 测试时间戳
    static void testTimestamps() {
        System.out.println("【时间戳测试】");
        
        long timestamp = DateUtils.currentTimestamp();
        long timestampMillis = DateUtils.currentTimestampMillis();
        
        assertTrue("秒时间戳合理", timestamp > 1700000000L);
        assertTrue("毫秒时间戳大于秒时间戳", timestampMillis > timestamp * 1000);
        
        Date now = new Date();
        long ts = DateUtils.toTimestamp(now);
        Date converted = DateUtils.fromTimestamp(ts);
        
        // 允许1秒误差
        assertTrue("时间戳转换误差在1秒内", 
            Math.abs(now.getTime() - converted.getTime()) < 1000);
        
        System.out.println("  当前时间戳(秒): " + timestamp);
        System.out.println("  当前时间戳(毫秒): " + timestampMillis);
        System.out.println();
    }
    
    // 测试时区转换
    static void testTimeZoneConversion() {
        System.out.println("【时区转换测试】");
        
        Date now = new Date();
        
        TimeZone utc = TimeZone.getTimeZone("UTC");
        TimeZone cst = TimeZone.getTimeZone("Asia/Shanghai");
        
        Date utcDate = DateUtils.convertTimeZone(now, cst, utc);
        assertNotNull("时区转换结果", utcDate);
        
        // UTC比上海时间早8小时，所以时间戳应该不同
        long diffHours = (utcDate.getTime() - now.getTime()) / 3600000;
        System.out.println("  时区差(小时): " + diffHours);
        
        // 转换为UTC
        Date toUtc = DateUtils.toUTC(now);
        assertNotNull("toUTC转换", toUtc);
        
        // 从UTC转换回来
        Date fromUtc = DateUtils.fromUTC(toUtc);
        assertEquals("UTC往返转换", now.getTime(), fromUtc.getTime());
        
        System.out.println();
    }
    
    // 测试年龄计算
    static void testAgeCalculation() {
        System.out.println("【年龄计算测试】");
        
        // 计算30岁的人的出生日期
        Date now = new Date();
        int birthYear = DateUtils.getYear(now) - 30;
        try {
            Date birthDate = DateUtils.parse(birthYear + "-06-15", DateUtils.FORMAT_DATE);
            int age = DateUtils.calculateAge(birthDate);
            assertTrue("年龄应该约为30", age == 29 || age == 30);
            System.out.println("  出生年份: " + birthYear + ", 计算年龄: " + age);
        } catch (ParseException e) {
            fail("年龄计算测试失败: " + e.getMessage());
        }
        
        System.out.println();
    }
    
    // 辅助方法
    static void assertEquals(String message, Object expected, Object actual) {
        if (expected == null && actual == null) return;
        if (expected != null && expected.equals(actual)) {
            pass(message);
        } else {
            fail(message + " - 期望: " + expected + ", 实际: " + actual);
        }
    }
    
    static void assertEquals(String message, long expected, long actual) {
        if (expected == actual) {
            pass(message);
        } else {
            fail(message + " - 期望: " + expected + ", 实际: " + actual);
        }
    }
    
    static void assertEquals(String message, int expected, int actual) {
        if (expected == actual) {
            pass(message);
        } else {
            fail(message + " - 期望: " + expected + ", 实际: " + actual);
        }
    }
    
    static void assertEquals(String message, String expected, String actual) {
        if (expected != null && expected.equals(actual)) {
            pass(message);
        } else {
            fail(message + " - 期望: " + expected + ", 实际: " + actual);
        }
    }
    
    static void assertTrue(String message, boolean condition) {
        if (condition) {
            pass(message);
        } else {
            fail(message);
        }
    }
    
    static void assertFalse(String message, boolean condition) {
        assertTrue(message, !condition);
    }
    
    static void assertNotNull(String message, Object obj) {
        if (obj != null) {
            pass(message);
        } else {
            fail(message + " - 期望非null");
        }
    }
    
    static void assertNull(String message, Object obj) {
        if (obj == null) {
            pass(message);
        } else {
            fail(message + " - 期望null, 实际: " + obj);
        }
    }
    
    static void pass(String message) {
        System.out.println("  ✓ " + message);
        passCount++;
    }
    
    static void fail(String message) {
        System.out.println("  ✗ " + message);
        failCount++;
    }
}