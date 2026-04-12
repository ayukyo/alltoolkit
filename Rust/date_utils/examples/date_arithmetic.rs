//! Date Arithmetic Examples for Date Utilities
//!
//! Run with: cargo run --example date_arithmetic

use date_utils::{Date, parse_date};

fn main() {
    println!("=== Date Arithmetic Examples ===\n");

    // 1. 加减天数
    println!("1. 加减天数");
    let base = parse_date("2024-01-15").unwrap();
    println!("   基准日期：{}", base);
    println!("   +10 天：{}", base.add_days(10));
    println!("   +30 天：{}", base.add_days(30));
    println!("   +365 天：{}", base.add_days(365));
    println!("   -10 天：{}", base.subtract_days(10));
    println!("   -30 天：{}", base.subtract_days(30));
    
    // 使用运算符
    println!("   使用运算符 base + 15: {}", base + 15);
    println!("   使用运算符 base - 15: {}", base - 15);
    println!();

    // 2. 加减月份
    println!("2. 加减月份");
    let base = parse_date("2024-01-31").unwrap();
    println!("   基准日期：{} (1 月 31 日)", base);
    println!("   +1 个月：{} (自动调整为 2 月 29 日)", base.add_months(1));
    println!("   +2 个月：{}", base.add_months(2));
    println!("   +12 个月：{}", base.add_months(12));
    println!("   -1 个月：{}", base.subtract_months(1));
    
    // 跨年份
    let base = parse_date("2024-10-15").unwrap();
    println!("   基准日期：{}", base);
    println!("   +5 个月：{} (跨年)", base.add_months(5));
    println!("   -12 个月：{}", base.subtract_months(12));
    println!();

    // 3. 加减年份
    println!("3. 加减年份");
    let base = parse_date("2024-02-29").unwrap();
    println!("   基准日期：{} (闰年 2 月 29 日)", base);
    println!("   +1 年：{} (非闰年，调整为 28 日)", base.add_years(1));
    println!("   +4 年：{}", base.add_years(4));
    println!("   -1 年：{}", base.subtract_years(1));
    
    let base = parse_date("2024-03-15").unwrap();
    println!("   基准日期：{}", base);
    println!("   +10 年：{}", base.add_years(10));
    println!("   -10 年：{}", base.subtract_years(10));
    println!();

    // 4. 日期差
    println!("4. 日期差");
    let date1 = parse_date("2024-01-01").unwrap();
    let date2 = parse_date("2024-12-31").unwrap();
    println!("   从 {} 到 {}", date1, date2);
    println!("   相差 {} 天", date1.days_difference(&date2));
    println!("   使用运算符 date2 - date1 = {}", date2 - date1);
    
    let date1 = parse_date("2023-12-31").unwrap();
    let date2 = parse_date("2024-01-01").unwrap();
    println!("   跨年：{} 到 {} = {} 天", date1, date2, date2 - date1);
    println!();

    // 5. 日期比较
    println!("5. 日期比较");
    let past = parse_date("2024-01-01").unwrap();
    let present = parse_date("2024-06-15").unwrap();
    let future = parse_date("2024-12-31").unwrap();
    
    println!("   past: {}, present: {}, future: {}", past, present, future);
    println!("   past < present: {}", past.is_before(&present));
    println!("   future > present: {}", future.is_after(&present));
    println!("   present 在 [past, future] 之间：{}", present.is_between(&past, &future));
    println!("   past == present: {}", past.is_equal(&present));
    println!();

    // 6. 实际应用场景
    println!("6. 实际应用场景");
    
    // 计算到期日
    let loan_date = parse_date("2024-01-15").unwrap();
    let due_date = loan_date.add_days(30);
    println!("   借款日期：{}, 30 天后到期：{}", loan_date, due_date);
    
    // 计算年龄
    let birth = parse_date("1990-06-15").unwrap();
    let today = Date::today();
    let age_days = birth.days_difference(&today);
    let age_years = age_days / 365;
    println!("   出生日期：{}, 今天：{}, 大约 {} 岁", birth, today, age_years);
    
    // 计算项目周期
    let project_start = parse_date("2024-03-01").unwrap();
    let project_end = parse_date("2024-08-31").unwrap();
    let duration = project_end - project_start;
    println!("   项目从 {} 到 {}, 共 {} 天 (约 {} 周)", 
             project_start, project_end, duration, duration / 7);
    
    // 试用期计算
    let hire_date = parse_date("2024-01-01").unwrap();
    let probation_end = hire_date.add_months(3);
    println!("   入职日期：{}, 试用期结束：{}", hire_date, probation_end);
    
    println!();
    println!("=== 完成 ===");
}
