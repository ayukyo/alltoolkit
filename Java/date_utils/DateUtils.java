import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.Date;
import java.util.List;
import java.util.Locale;
import java.util.TimeZone;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * DateUtils - 零外部依赖的日期时间工具类
 * 
 * 功能：
 * - 日期格式化与解析
 * - 日期计算（加减天数、月份等）
 * - 日期比较与判断
 * - 相对时间计算（如"3天前"）
 * - 工作日计算
 * - 时区转换
 * 
 * @author AllToolkit
 * @version 1.0
 */
public class DateUtils {
    
    // 常用日期格式
    public static final String FORMAT_ISO = "yyyy-MM-dd'T'HH:mm:ss";
    public static final String FORMAT_ISO_WITH_TZ = "yyyy-MM-dd'T'HH:mm:ssXXX";
    public static final String FORMAT_DATE = "yyyy-MM-dd";
    public static final String FORMAT_DATETIME = "yyyy-MM-dd HH:mm:ss";
    public static final String FORMAT_TIME = "HH:mm:ss";
    public static final String FORMAT_COMPACT = "yyyyMMddHHmmss";
    public static final String FORMAT_CHINESE = "yyyy年MM月dd日 HH:mm:ss";
    public static final String FORMAT_US = "MMMM dd, yyyy";
    
    private static final long MILLIS_PER_SECOND = 1000L;
    private static final long MILLIS_PER_MINUTE = 60L * MILLIS_PER_SECOND;
    private static final long MILLIS_PER_HOUR = 60L * MILLIS_PER_MINUTE;
    private static final long MILLIS_PER_DAY = 24L * MILLIS_PER_HOUR;
    
    // ============ 格式化方法 ============
    
    /**
     * 格式化日期为字符串
     */
    public static String format(Date date, String pattern) {
        if (date == null || pattern == null) {
            return null;
        }
        SimpleDateFormat sdf = new SimpleDateFormat(pattern, Locale.getDefault());
        return sdf.format(date);
    }
    
    /**
     * 格式化日期为字符串（指定时区）
     */
    public static String format(Date date, String pattern, TimeZone timeZone) {
        if (date == null || pattern == null) {
            return null;
        }
        SimpleDateFormat sdf = new SimpleDateFormat(pattern, Locale.getDefault());
        sdf.setTimeZone(timeZone);
        return sdf.format(date);
    }
    
    /**
     * 格式化为ISO格式
     */
    public static String formatISO(Date date) {
        return format(date, FORMAT_ISO);
    }
    
    /**
     * 格式化为日期字符串（yyyy-MM-dd）
     */
    public static String formatDate(Date date) {
        return format(date, FORMAT_DATE);
    }
    
    /**
     * 格式化为日期时间字符串（yyyy-MM-dd HH:mm:ss）
     */
    public static String formatDateTime(Date date) {
        return format(date, FORMAT_DATETIME);
    }
    
    // ============ 解析方法 ============
    
    /**
     * 解析字符串为日期
     */
    public static Date parse(String dateStr, String pattern) throws ParseException {
        if (dateStr == null || pattern == null) {
            return null;
        }
        SimpleDateFormat sdf = new SimpleDateFormat(pattern, Locale.getDefault());
        sdf.setLenient(false);
        return sdf.parse(dateStr);
    }
    
    /**
     * 解析字符串为日期（指定时区）
     */
    public static Date parse(String dateStr, String pattern, TimeZone timeZone) throws ParseException {
        if (dateStr == null || pattern == null) {
            return null;
        }
        SimpleDateFormat sdf = new SimpleDateFormat(pattern, Locale.getDefault());
        sdf.setTimeZone(timeZone);
        sdf.setLenient(false);
        return sdf.parse(dateStr);
    }
    
    /**
     * 安全解析（解析失败返回null）
     */
    public static Date parseOrNull(String dateStr, String pattern) {
        try {
            return parse(dateStr, pattern);
        } catch (ParseException e) {
            return null;
        }
    }
    
    /**
     * 自动检测格式解析
     */
    public static Date parseAuto(String dateStr) throws ParseException {
        if (dateStr == null || dateStr.trim().isEmpty()) {
            return null;
        }
        
        String[] patterns = {
            FORMAT_ISO_WITH_TZ, FORMAT_ISO, FORMAT_DATETIME, 
            FORMAT_DATE, FORMAT_COMPACT, FORMAT_CHINESE, FORMAT_US
        };
        
        for (String pattern : patterns) {
            try {
                return parse(dateStr.trim(), pattern);
            } catch (ParseException ignored) {
            }
        }
        
        throw new ParseException("无法解析日期: " + dateStr, 0);
    }
    
    // ============ 日期计算方法 ============
    
    /**
     * 添加天数
     */
    public static Date addDays(Date date, int days) {
        return add(date, Calendar.DAY_OF_MONTH, days);
    }
    
    /**
     * 添加小时
     */
    public static Date addHours(Date date, int hours) {
        return add(date, Calendar.HOUR_OF_DAY, hours);
    }
    
    /**
     * 添加分钟
     */
    public static Date addMinutes(Date date, int minutes) {
        return add(date, Calendar.MINUTE, minutes);
    }
    
    /**
     * 添加秒
     */
    public static Date addSeconds(Date date, int seconds) {
        return add(date, Calendar.SECOND, seconds);
    }
    
    /**
     * 添加月份
     */
    public static Date addMonths(Date date, int months) {
        return add(date, Calendar.MONTH, months);
    }
    
    /**
     * 添加年份
     */
    public static Date addYears(Date date, int years) {
        return add(date, Calendar.YEAR, years);
    }
    
    /**
     * 添加周
     */
    public static Date addWeeks(Date date, int weeks) {
        return add(date, Calendar.WEEK_OF_YEAR, weeks);
    }
    
    private static Date add(Date date, int field, int amount) {
        if (date == null) {
            return null;
        }
        Calendar cal = Calendar.getInstance();
        cal.setTime(date);
        cal.add(field, amount);
        return cal.getTime();
    }
    
    // ============ 日期获取方法 ============
    
    /**
     * 获取今天的开始时间（00:00:00）
     */
    public static Date startOfDay(Date date) {
        if (date == null) {
            return null;
        }
        Calendar cal = Calendar.getInstance();
        cal.setTime(date);
        cal.set(Calendar.HOUR_OF_DAY, 0);
        cal.set(Calendar.MINUTE, 0);
        cal.set(Calendar.SECOND, 0);
        cal.set(Calendar.MILLISECOND, 0);
        return cal.getTime();
    }
    
    /**
     * 获取今天的结束时间（23:59:59）
     */
    public static Date endOfDay(Date date) {
        if (date == null) {
            return null;
        }
        Calendar cal = Calendar.getInstance();
        cal.setTime(date);
        cal.set(Calendar.HOUR_OF_DAY, 23);
        cal.set(Calendar.MINUTE, 59);
        cal.set(Calendar.SECOND, 59);
        cal.set(Calendar.MILLISECOND, 999);
        return cal.getTime();
    }
    
    /**
     * 获取本周第一天（周一）
     */
    public static Date startOfWeek(Date date) {
        if (date == null) {
            return null;
        }
        Calendar cal = Calendar.getInstance();
        cal.setTime(date);
        cal.setFirstDayOfWeek(Calendar.MONDAY);
        cal.set(Calendar.DAY_OF_WEEK, Calendar.MONDAY);
        return startOfDay(cal.getTime());
    }
    
    /**
     * 获取本月第一天
     */
    public static Date startOfMonth(Date date) {
        if (date == null) {
            return null;
        }
        Calendar cal = Calendar.getInstance();
        cal.setTime(date);
        cal.set(Calendar.DAY_OF_MONTH, 1);
        return startOfDay(cal.getTime());
    }
    
    /**
     * 获取本月最后一天
     */
    public static Date endOfMonth(Date date) {
        if (date == null) {
            return null;
        }
        Calendar cal = Calendar.getInstance();
        cal.setTime(date);
        cal.set(Calendar.DAY_OF_MONTH, cal.getActualMaximum(Calendar.DAY_OF_MONTH));
        return endOfDay(cal.getTime());
    }
    
    /**
     * 获取本年第一天
     */
    public static Date startOfYear(Date date) {
        if (date == null) {
            return null;
        }
        Calendar cal = Calendar.getInstance();
        cal.setTime(date);
        cal.set(Calendar.MONTH, Calendar.JANUARY);
        cal.set(Calendar.DAY_OF_MONTH, 1);
        return startOfDay(cal.getTime());
    }
    
    /**
     * 获取年份
     */
    public static int getYear(Date date) {
        return getField(date, Calendar.YEAR);
    }
    
    /**
     * 获取月份（1-12）
     */
    public static int getMonth(Date date) {
        return getField(date, Calendar.MONTH) + 1;
    }
    
    /**
     * 获取日
     */
    public static int getDay(Date date) {
        return getField(date, Calendar.DAY_OF_MONTH);
    }
    
    /**
     * 获取小时
     */
    public static int getHour(Date date) {
        return getField(date, Calendar.HOUR_OF_DAY);
    }
    
    /**
     * 获取分钟
     */
    public static int getMinute(Date date) {
        return getField(date, Calendar.MINUTE);
    }
    
    /**
     * 获取秒
     */
    public static int getSecond(Date date) {
        return getField(date, Calendar.SECOND);
    }
    
    /**
     * 获取星期几（1-7，周一为1）
     */
    public static int getDayOfWeek(Date date) {
        int day = getField(date, Calendar.DAY_OF_WEEK);
        return day == Calendar.SUNDAY ? 7 : day - 1;
    }
    
    /**
     * 获取星期名称
     */
    public static String getDayOfWeekName(Date date) {
        String[] names = {"周一", "周二", "周三", "周四", "周五", "周六", "周日"};
        return names[getDayOfWeek(date) - 1];
    }
    
    private static int getField(Date date, int field) {
        if (date == null) {
            throw new IllegalArgumentException("Date cannot be null");
        }
        Calendar cal = Calendar.getInstance();
        cal.setTime(date);
        return cal.get(field);
    }
    
    // ============ 日期比较方法 ============
    
    /**
     * 计算两个日期之间的天数差
     */
    public static long daysBetween(Date start, Date end) {
        if (start == null || end == null) {
            throw new IllegalArgumentException("Dates cannot be null");
        }
        Date startDay = startOfDay(start);
        Date endDay = startOfDay(end);
        return (endDay.getTime() - startDay.getTime()) / MILLIS_PER_DAY;
    }
    
    /**
     * 计算两个日期之间的小时差
     */
    public static long hoursBetween(Date start, Date end) {
        if (start == null || end == null) {
            throw new IllegalArgumentException("Dates cannot be null");
        }
        return (end.getTime() - start.getTime()) / MILLIS_PER_HOUR;
    }
    
    /**
     * 计算两个日期之间的分钟差
     */
    public static long minutesBetween(Date start, Date end) {
        if (start == null || end == null) {
            throw new IllegalArgumentException("Dates cannot be null");
        }
        return (end.getTime() - start.getTime()) / MILLIS_PER_MINUTE;
    }
    
    /**
     * 比较两个日期是否同一天
     */
    public static boolean isSameDay(Date date1, Date date2) {
        if (date1 == null || date2 == null) {
            return false;
        }
        return formatDate(date1).equals(formatDate(date2));
    }
    
    /**
     * 判断是否为今天
     */
    public static boolean isToday(Date date) {
        return isSameDay(date, new Date());
    }
    
    /**
     * 判断是否为昨天
     */
    public static boolean isYesterday(Date date) {
        if (date == null) {
            return false;
        }
        return isSameDay(date, addDays(new Date(), -1));
    }
    
    /**
     * 判断是否为明天
     */
    public static boolean isTomorrow(Date date) {
        if (date == null) {
            return false;
        }
        return isSameDay(date, addDays(new Date(), 1));
    }
    
    /**
     * 判断日期是否在范围内
     */
    public static boolean isInRange(Date date, Date start, Date end) {
        if (date == null || start == null || end == null) {
            return false;
        }
        return !date.before(start) && !date.after(end);
    }
    
    /**
     * 判断是否为周末
     */
    public static boolean isWeekend(Date date) {
        int dayOfWeek = getDayOfWeek(date);
        return dayOfWeek == 6 || dayOfWeek == 7;
    }
    
    /**
     * 判断是否为工作日（周一到周五）
     */
    public static boolean isWeekday(Date date) {
        return !isWeekend(date);
    }
    
    /**
     * 判断是否为闰年
     */
    public static boolean isLeapYear(Date date) {
        int year = getYear(date);
        return (year % 4 == 0 && year % 100 != 0) || (year % 400 == 0);
    }
    
    /**
     * 获取某月的天数
     */
    public static int getDaysInMonth(Date date) {
        if (date == null) {
            throw new IllegalArgumentException("Date cannot be null");
        }
        Calendar cal = Calendar.getInstance();
        cal.setTime(date);
        return cal.getActualMaximum(Calendar.DAY_OF_MONTH);
    }
    
    // ============ 相对时间方法 ============
    
    /**
     * 获取相对时间描述（如"3分钟前"、"2天后"）
     */
    public static String relativeTime(Date date) {
        return relativeTime(date, new Date(), Locale.CHINESE);
    }
    
    /**
     * 获取相对时间描述（指定当前时间）
     */
    public static String relativeTime(Date date, Date now, Locale locale) {
        if (date == null || now == null) {
            return "";
        }
        
        long diffMs = now.getTime() - date.getTime();
        boolean isFuture = diffMs < 0;
        diffMs = Math.abs(diffMs);
        
        long seconds = diffMs / MILLIS_PER_SECOND;
        long minutes = diffMs / MILLIS_PER_MINUTE;
        long hours = diffMs / MILLIS_PER_HOUR;
        long days = diffMs / MILLIS_PER_DAY;
        long months = days / 30;
        long years = days / 365;
        
        boolean isChinese = locale != null && locale.getLanguage().equals("zh");
        
        if (isFuture) {
            if (seconds < 60) {
                return isChinese ? "即将" : "in a moment";
            } else if (minutes < 60) {
                return isChinese ? minutes + "分钟后" : "in " + minutes + " minutes";
            } else if (hours < 24) {
                return isChinese ? hours + "小时后" : "in " + hours + " hours";
            } else if (days < 30) {
                return isChinese ? days + "天后" : "in " + days + " days";
            } else if (months < 12) {
                return isChinese ? months + "个月后" : "in " + months + " months";
            } else {
                return isChinese ? years + "年后" : "in " + years + " years";
            }
        } else {
            if (seconds < 60) {
                return isChinese ? "刚刚" : "just now";
            } else if (minutes < 60) {
                return isChinese ? minutes + "分钟前" : minutes + " minutes ago";
            } else if (hours < 24) {
                return isChinese ? hours + "小时前" : hours + " hours ago";
            } else if (days < 30) {
                return isChinese ? days + "天前" : days + " days ago";
            } else if (months < 12) {
                return isChinese ? months + "个月前" : months + " months ago";
            } else {
                return isChinese ? years + "年前" : years + " years ago";
            }
        }
    }
    
    // ============ 工作日计算 ============
    
    /**
     * 计算工作日数量（跳过周末）
     */
    public static int countWorkdays(Date start, Date end) {
        if (start == null || end == null) {
            return 0;
        }
        
        // 确保 start <= end
        Date s = start.before(end) ? start : end;
        Date e = start.before(end) ? end : start;
        
        int workdays = 0;
        Calendar cal = Calendar.getInstance();
        cal.setTime(s);
        
        while (!cal.getTime().after(e)) {
            if (isWeekday(cal.getTime())) {
                workdays++;
            }
            cal.add(Calendar.DAY_OF_MONTH, 1);
        }
        
        return workdays;
    }
    
    /**
     * 添加工作日
     */
    public static Date addWorkdays(Date date, int workdays) {
        if (date == null || workdays == 0) {
            return date;
        }
        
        Calendar cal = Calendar.getInstance();
        cal.setTime(date);
        int direction = workdays > 0 ? 1 : -1;
        int remaining = Math.abs(workdays);
        
        while (remaining > 0) {
            cal.add(Calendar.DAY_OF_MONTH, direction);
            if (isWeekday(cal.getTime())) {
                remaining--;
            }
        }
        
        return cal.getTime();
    }
    
    // ============ 年龄计算 ============
    
    /**
     * 计算年龄
     */
    public static int calculateAge(Date birthDate) {
        return calculateAge(birthDate, new Date());
    }
    
    /**
     * 计算年龄（指定日期）
     */
    public static int calculateAge(Date birthDate, Date currentDate) {
        if (birthDate == null || currentDate == null) {
            throw new IllegalArgumentException("Dates cannot be null");
        }
        
        Calendar birth = Calendar.getInstance();
        birth.setTime(birthDate);
        Calendar current = Calendar.getInstance();
        current.setTime(currentDate);
        
        int age = current.get(Calendar.YEAR) - birth.get(Calendar.YEAR);
        
        if (current.get(Calendar.DAY_OF_YEAR) < birth.get(Calendar.DAY_OF_YEAR)) {
            age--;
        }
        
        return age;
    }
    
    // ============ 时区转换 ============
    
    /**
     * 转换时区
     */
    public static Date convertTimeZone(Date date, TimeZone fromTz, TimeZone toTz) {
        if (date == null) {
            return null;
        }
        long time = date.getTime();
        long offset = toTz.getOffset(time) - fromTz.getOffset(time);
        return new Date(time + offset);
    }
    
    /**
     * 转换为UTC时间
     */
    public static Date toUTC(Date date) {
        return convertTimeZone(date, TimeZone.getDefault(), TimeZone.getTimeZone("UTC"));
    }
    
    /**
     * 从UTC时间转换
     */
    public static Date fromUTC(Date date) {
        return convertTimeZone(date, TimeZone.getTimeZone("UTC"), TimeZone.getDefault());
    }
    
    // ============ 日期范围 ============
    
    /**
     * 获取两个日期之间的所有日期
     */
    public static List<Date> getDatesBetween(Date start, Date end) {
        List<Date> dates = new ArrayList<>();
        if (start == null || end == null) {
            return dates;
        }
        
        Date s = start.before(end) ? start : end;
        Date e = start.before(end) ? end : start;
        
        Calendar cal = Calendar.getInstance();
        cal.setTime(startOfDay(s));
        Date endDate = startOfDay(e);
        
        while (!cal.getTime().after(endDate)) {
            dates.add(cal.getTime());
            cal.add(Calendar.DAY_OF_MONTH, 1);
        }
        
        return dates;
    }
    
    // ============ 时间戳方法 ============
    
    /**
     * 获取当前时间戳（秒）
     */
    public static long currentTimestamp() {
        return System.currentTimeMillis() / 1000;
    }
    
    /**
     * 获取当前时间戳（毫秒）
     */
    public static long currentTimestampMillis() {
        return System.currentTimeMillis();
    }
    
    /**
     * 时间戳转Date（秒）
     */
    public static Date fromTimestamp(long timestamp) {
        return new Date(timestamp * 1000);
    }
    
    /**
     * 时间戳转Date（毫秒）
     */
    public static Date fromTimestampMillis(long timestamp) {
        return new Date(timestamp);
    }
    
    /**
     * Date转时间戳（秒）
     */
    public static long toTimestamp(Date date) {
        return date == null ? 0 : date.getTime() / 1000;
    }
    
    // ============ 当前时间快捷方法 ============
    
    /**
     * 获取当前日期
     */
    public static Date now() {
        return new Date();
    }
    
    /**
     * 获取今天开始
     */
    public static Date today() {
        return startOfDay(new Date());
    }
    
    /**
     * 获取明天开始
     */
    public static Date tomorrow() {
        return startOfDay(addDays(new Date(), 1));
    }
    
    /**
     * 获取昨天开始
     */
    public static Date yesterday() {
        return startOfDay(addDays(new Date(), -1));
    }
}