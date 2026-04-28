# DateUtils - Java 日期时间工具类

零外部依赖的日期时间处理工具，提供全面的日期操作功能。

## 功能特性

### 📅 格式化与解析
- 多种预设格式（ISO、日期、时间、中文格式等）
- 自定义格式支持
- 自动格式检测解析
- 时区感知的格式化/解析

### 🔢 日期计算
- 加减天数、小时、分钟、秒
- 加减月份、年份、周
- 获取一天的开始/结束时间
- 获取周/月/年的开始日期

### 📊 日期提取
- 获取年、月、日、时、分、秒
- 获取星期几（名称和数字）
- 获取月份天数
- 判断闰年

### ⚖️ 日期比较
- 计算两个日期之间的天数、小时、分钟差
- 判断是否同一天
- 判断是否今天/昨天/明天
- 判断日期是否在范围内

### ⏰ 相对时间
- "刚刚"、"3分钟前"、"2天后"等友好描述
- 支持中英文

### 💼 工作日计算
- 计算两个日期之间的工作日数量
- 添加工作日（跳过周末）

### 🌍 时区转换
- 时区间的日期转换
- UTC 时间转换

### 🎂 年龄计算
- 根据出生日期计算年龄

## 使用示例

```java
import java.text.ParseException;
import java.util.Date;
import java.util.List;

public class Example {
    public static void main(String[] args) throws ParseException {
        Date now = new Date();
        
        // 格式化
        System.out.println(DateUtils.formatDate(now));       // 2024-01-15
        System.out.println(DateUtils.formatDateTime(now));   // 2024-01-15 10:30:00
        System.out.println(DateUtils.formatISO(now));        // 2024-01-15T10:30:00
        
        // 解析
        Date date = DateUtils.parse("2024-01-15", "yyyy-MM-dd");
        Date auto = DateUtils.parseAuto("2024-01-15 10:30:00");
        
        // 日期计算
        Date tomorrow = DateUtils.addDays(now, 1);
        Date nextMonth = DateUtils.addMonths(now, 1);
        Date startOfDay = DateUtils.startOfDay(now);
        Date endOfMonth = DateUtils.endOfMonth(now);
        
        // 日期提取
        int year = DateUtils.getYear(now);
        int month = DateUtils.getMonth(now);
        int day = DateUtils.getDay(now);
        String weekDay = DateUtils.getDayOfWeekName(now); // 周一
        
        // 日期比较
        long days = DateUtils.daysBetween(date1, date2);
        boolean sameDay = DateUtils.isSameDay(date1, date2);
        boolean isToday = DateUtils.isToday(date);
        
        // 相对时间
        String relative = DateUtils.relativeTime(date); // "3小时前"
        
        // 工作日
        int workdays = DateUtils.countWorkdays(start, end);
        Date plus5Workdays = DateUtils.addWorkdays(date, 5);
        
        // 时区
        Date utc = DateUtils.toUTC(now);
        Date local = DateUtils.fromUTC(utc);
        
        // 年龄
        int age = DateUtils.calculateAge(birthDate);
        
        // 时间戳
        long ts = DateUtils.currentTimestamp();
        Date fromTs = DateUtils.fromTimestamp(ts);
    }
}
```

## 编译和运行

```bash
# 编译
javac DateUtils.java DateUtilsTest.java

# 运行测试
java DateUtilsTest

# 使用示例
javac DateUtils.java Example.java
java Example
```

## 预设格式

| 格式常量 | 模式 | 示例 |
|---------|------|------|
| FORMAT_ISO | yyyy-MM-dd'T'HH:mm:ss | 2024-01-15T10:30:00 |
| FORMAT_ISO_WITH_TZ | yyyy-MM-dd'T'HH:mm:ssXXX | 2024-01-15T10:30:00+08:00 |
| FORMAT_DATE | yyyy-MM-dd | 2024-01-15 |
| FORMAT_DATETIME | yyyy-MM-dd HH:mm:ss | 2024-01-15 10:30:00 |
| FORMAT_TIME | HH:mm:ss | 10:30:00 |
| FORMAT_COMPACT | yyyyMMddHHmmss | 20240115103000 |
| FORMAT_CHINESE | yyyy年MM月dd日 HH:mm:ss | 2024年01月15日 10:30:00 |
| FORMAT_US | MMMM dd, yyyy | January 15, 2024 |

## 测试结果

```
========================================
DateUtils 单元测试
========================================

【格式化与解析测试】
  ✓ 格式化为 yyyy-MM-dd
  ✓ 格式化为ISO格式
  ✓ 解析日期字符串
  ✓ 自动解析日期格式
  ✓ 自动解析日期时间格式
  ✓ 安全解析无效日期返回null

【日期计算测试】
  ✓ 添加1天
  ✓ 添加2小时
  ✓ 添加30分钟
  ✓ 添加月份
  ✓ 添加-1天
  ✓ 一天开始
  ✓ 一天结束
  ✓ 结束 > 开始
  ✓ 月初日期为1
  ✓ 月末日期正确

【日期提取测试】
  ✓ 获取年份 >= 2024
  ✓ 获取月份 1-12
  ...

通过: 45 / 失败: 0
========================================
```

## 特点

- ✅ **零外部依赖** - 仅使用 Java 标准库
- ✅ **线程安全** - 无状态设计，每次调用创建新的 SimpleDateFormat
- ✅ **国际化支持** - 支持中英文相对时间描述
- ✅ **全面功能** - 覆盖日常开发中 90% 的日期操作需求

## 版本历史

- **v1.0** (2026-04-29) - 初始版本
  - 格式化与解析
  - 日期计算
  - 日期比较
  - 相对时间
  - 工作日计算
  - 时区转换
  - 年龄计算

## 许可证

MIT License