//! Basic Usage Examples for Date Utilities
//!
//! Run with: cargo run --example basic_usage

use date_utils::{Date, parse_date, format_date, is_leap_year, days_in_month};

fn main() {
    println!("=== Date Utilities Basic Usage ===\n");

    // 1. 创建日期
    println!("1. 创建日期");
    let date = Date::new(2024, 3, 15).unwrap();
    println!("   手动创建：{}", date);
    
    let today = Date::today();
    println!("   今天：{}", today);
    println!();

    // 2. 解析日期
    println!("2. 解析日期");
    let formats = vec![
        "2024-03-15",
        "2024/03/15",
        "15-03-2024",
        "15/03/2024",
        "03-15-2024",
        "20240315",
    ];
    
    for fmt in formats {
        match parse_date(fmt) {
            Ok(d) => println!("   '{}' -> {}", fmt, d),
            Err(e) => println!("   '{}' -> 错误：{:?}", fmt, e),
        }
    }
    println!();

    // 3. 格式化日期
    println!("3. 格式化日期");
    let date = parse_date("2024-03-15").unwrap();
    let formats = vec![
        "YYYY-MM-DD",
        "MM/DD/YYYY",
        "DD/MM/YYYY",
        "MMMM D, YYYY",
        "EEEE, MMMM D, YYYY",
        "'Day ' DDD ' of year'",
    ];
    
    for fmt in formats {
        println!("   '{}' -> {}", fmt, format_date(&date, fmt));
    }
    println!();

    // 4. 获取日期信息
    println!("4. 获取日期信息");
    let date = parse_date("2024-03-15").unwrap();
    println!("   年份：{}", date.year());
    println!("   月份：{}", date.month());
    println!("   日期：{}", date.day());
    println!("   月份名：{}", date.month_enum().full_name());
    println!("   星期：{} ({})", date.weekday().short_name(), date.weekday().full_name());
    println!("   一年中的第几天：{}", date.day_of_year());
    println!("   是否闰年：{}", Date::is_leap_year(date.year()));
    println!("   本月天数：{}", date.days_in_current_month());
    println!();

    // 5. 工具函数
    println!("5. 工具函数");
    println!("   2024 是闰年吗？{}", is_leap_year(2024));
    println!("   2023 是闰年吗？{}", is_leap_year(2023));
    println!("   2024 年 2 月有{}天", days_in_month(2024, 2));
    println!("   2024 年 4 月有{}天", days_in_month(2024, 4));
    println!();

    // 6. 边界日期
    println!("6. 边界日期");
    let date = parse_date("2024-03-15").unwrap();
    println!("   原始日期：{}", date);
    println!("   月初：{}", date.first_day_of_month());
    println!("   月末：{}", date.last_day_of_month());
    println!("   年初：{}", date.first_day_of_year());
    println!("   年末：{}", date.last_day_of_year());
    println!();

    println!("=== 完成 ===");
}
