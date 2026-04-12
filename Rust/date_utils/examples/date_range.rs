//! Date Range Examples for Date Utilities
//!
//! Run with: cargo run --example date_range

use date_utils::{parse_date, date_range, date_range_step, weekdays_in_range, weekends_in_range};

fn main() {
    println!("=== Date Range Examples ===\n");

    // 1. 基本日期范围
    println!("1. 基本日期范围");
    let start = parse_date("2024-01-01").unwrap();
    let end = parse_date("2024-01-10").unwrap();
    
    println!("   从 {} 到 {}", start, end);
    let range = date_range(&start, &end);
    println!("   共 {} 天:", range.len());
    for (i, date) in range.iter().enumerate() {
        if i < 5 {
            print!("   {} ", date);
        } else if i == 5 {
            print!("... ");
        }
    }
    println!();
    println!();

    // 2. 带步长的日期范围
    println!("2. 带步长的日期范围");
    let start = parse_date("2024-01-01").unwrap();
    let end = parse_date("2024-01-20").unwrap();
    
    println!("   从 {} 到 {}, 步长 3 天", start, end);
    let range = date_range_step(&start, &end, 3);
    println!("   共 {} 个日期:", range.len());
    for date in &range {
        print!("   {} ", date);
    }
    println!();
    println!();

    // 3. 工作日范围
    println!("3. 工作日范围 (周一至周五)");
    let start = parse_date("2024-01-01").unwrap(); // Monday
    let end = parse_date("2024-01-14").unwrap();   // Sunday (2 weeks)
    
    println!("   从 {} ({}) 到 {} ({})", 
             start, start.weekday().full_name(),
             end, end.weekday().full_name());
    
    let weekdays = weekdays_in_range(&start, &end);
    println!("   共 {} 个工作日:", weekdays.len());
    for date in &weekdays {
        print!("   {}({}) ", date, date.weekday().short_name());
    }
    println!();
    println!();

    // 4. 周末范围
    println!("4. 周末范围 (周六、周日)");
    let start = parse_date("2024-01-01").unwrap();
    let end = parse_date("2024-01-31").unwrap();
    
    println!("   从 {} 到 {}", start, end);
    
    let weekends = weekends_in_range(&start, &end);
    println!("   共 {} 个周末日:", weekends.len());
    for date in &weekends {
        print!("   {}({}) ", date, date.weekday().short_name());
    }
    println!();
    println!();

    // 5. 实际应用场景
    println!("5. 实际应用场景");
    
    // 项目排期
    println!("   📅 项目排期:");
    let project_start = parse_date("2024-03-01").unwrap();
    let project_end = parse_date("2024-03-31").unwrap();
    let workdays = weekdays_in_range(&project_start, &project_end);
    println!("      项目期间：{} 到 {}", project_start, project_end);
    println!("      工作日总数：{} 天", workdays.len());
    if let Some(first) = workdays.first() {
        println!("      第一个工作日：{} ({})", first, first.weekday().full_name());
    }
    if let Some(last) = workdays.last() {
        println!("      最后工作日：{} ({})", last, last.weekday().full_name());
    }
    println!();
    
    // 假期计算
    println!("   🏖️ 假期计算:");
    let vacation_start = parse_date("2024-07-01").unwrap();
    let vacation_end = parse_date("2024-07-14").unwrap();
    let vacation_days = date_range(&vacation_start, &vacation_end);
    let vacation_weekends = weekends_in_range(&vacation_start, &vacation_end);
    let vacation_workdays = vacation_days.len() - vacation_weekends.len();
    println!("      假期：{} 到 {}, 共 {} 天", 
             vacation_start, vacation_end, vacation_days.len());
    println!("      占用工作日：{} 天", vacation_workdays);
    println!("      包含周末：{} 天", vacation_weekends.len());
    println!();
    
    // 月度报告
    println!("   📊 月度报告:");
    let month_start = parse_date("2024-04-01").unwrap();
    let month_end = parse_date("2024-04-30").unwrap();
    let month_days = date_range(&month_start, &month_end);
    let month_weekdays = weekdays_in_range(&month_start, &month_end);
    let month_weekends = weekends_in_range(&month_start, &month_end);
    println!("      月份：{} 年 {} 月", month_start.year(), month_start.month());
    println!("      总天数：{}", month_days.len());
    println!("      工作日：{} 天", month_weekdays.len());
    println!("      周末：{} 天", month_weekends.len());
    println!();
    
    // 每周例会
    println!("   📆 每周例会安排:");
    let week_start = parse_date("2024-05-01").unwrap();
    let week_end = parse_date("2024-05-07").unwrap();
    let week_days = date_range(&week_start, &week_end);
    println!("      周次：{} 到 {}", week_start, week_end);
    for date in &week_days {
        let is_meeting_day = date.weekday().number() == 3; // Wednesday
        if is_meeting_day {
            println!("      ✅ {} ({}) - 例会日", date, date.weekday().full_name());
        }
    }
    println!();

    // 6. 生成日历
    println!("6. 生成月历视图:");
    let month_start = parse_date("2024-03-01").unwrap();
    let month_end = month_start.last_day_of_month();
    
    println!("   {} 年 {} 月", month_start.year(), month_start.month());
    println!("   -----------------------------");
    println!("   日  一  二  三  四  五  六");
    
    // 获取月初是星期几
    let first_weekday = month_start.weekday().number() as usize; // 1=Mon, 7=Sun
    let adjusted_first = if first_weekday == 7 { 0 } else { first_weekday };
    
    // 打印前导空格
    print!("   ");
    for _ in 0..adjusted_first {
        print!("    ");
    }
    
    // 打印日期
    let days = date_range(&month_start, &month_end);
    for date in &days {
        print!("{:3} ", date.day());
        if date.weekday().number() == 7 {
            println!();
            print!("   ");
        }
    }
    println!();
    println!();

    println!("=== 完成 ===");
}
