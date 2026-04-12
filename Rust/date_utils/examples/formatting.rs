//! Date Formatting Examples for Date Utilities
//!
//! Run with: cargo run --example formatting

use date_utils::{parse_date, format_date};

fn main() {
    println!("=== Date Formatting Examples ===\n");

    let date = parse_date("2024-03-15").unwrap();
    println!("基准日期：{} ({})\n", date, date.weekday().full_name());

    // 1. 常见日期格式
    println!("1. 常见日期格式");
    let formats = vec![
        ("ISO 8601", "YYYY-MM-DD"),
        ("美国格式", "MM/DD/YYYY"),
        ("欧洲格式", "DD/MM/YYYY"),
        ("中国格式", "YYYY 年 MM 月 DD 日"),
        ("日本格式", "YYYY/MM/DD"),
        ("紧凑格式", "YYYYMMDD"),
    ];
    
    for (name, fmt) in &formats {
        println!("   {}: {}", name, format_date(&date, fmt));
    }
    println!();

    // 2. 带月份名称
    println!("2. 带月份名称");
    let formats = vec![
        ("短月份", "MMM DD, YYYY"),
        ("长月份", "MMMM DD, YYYY"),
        ("仅月份", "MMMM YYYY"),
        ("月年缩写", "MMM YYYY"),
    ];
    
    for (name, fmt) in &formats {
        println!("   {}: {}", name, format_date(&date, fmt));
    }
    println!();

    // 3. 带星期名称
    println!("3. 带星期名称");
    let formats = vec![
        ("短星期", "EEE, MMM DD"),
        ("长星期", "EEEE, MMMM DD"),
        ("完整格式", "EEEE, MMMM DD, YYYY"),
        ("仅星期", "EEEE"),
    ];
    
    for (name, fmt) in &formats {
        println!("   {}: {}", name, format_date(&date, fmt));
    }
    println!();

    // 4. 一年中的第几天
    println!("4. 一年中的第几天");
    let formats = vec![
        ("第几天", "'Day ' D ' of ' YYYY"),
        ("序号格式", "DD/DDD YYYY"),
    ];
    
    for (name, fmt) in &formats {
        println!("   {}: {}", name, format_date(&date, fmt));
    }
    println!();

    // 5. 自定义格式
    println!("5. 自定义/创意格式");
    let formats = vec![
        ("文件命名", "report_YYYYMMDD"),
        ("日志格式", "[YYYY-MM-DD]"),
        ("显示格式", "今天是：EEEE (MMM D)"),
        ("长句格式", "MMMM D, YYYY is a EEEE"),
        ("技术格式", "YYYY.DDD"),
    ];
    
    for (name, fmt) in &formats {
        println!("   {}: {}", name, format_date(&date, fmt));
    }
    println!();

    // 6. 不同日期的格式展示
    println!("6. 不同日期的格式展示");
    let dates = vec![
        parse_date("2024-01-01").unwrap(),
        parse_date("2024-06-15").unwrap(),
        parse_date("2024-12-25").unwrap(),
        parse_date("2024-02-29").unwrap(),
    ];
    
    let fmt = "EEEE, MMMM D, YYYY";
    for date in &dates {
        println!("   {}: {}", date, format_date(date, fmt));
    }
    println!();

    // 7. 格式模板应用
    println!("7. 格式模板应用");
    
    // 生日卡片
    let birthday = parse_date("1990-06-15").unwrap();
    println!("   🎂 生日卡片:");
    println!("      格式：'生日快乐！你出生于 EEEE, MMMM D, YYYY'");
    println!("      输出：'生日快乐！你出生于 {}'\n", 
             format_date(&birthday, "EEEE, MMMM D, YYYY"));
    
    // 会议邀请
    let meeting = parse_date("2024-04-20").unwrap();
    println!("   📅 会议邀请:");
    println!("      格式：'会议时间：YYYY-MM-DD EEEE HH:MM'");
    println!("      输出：'会议时间：{} {} 14:00'\n", 
             format_date(&meeting, "YYYY-MM-DD"),
             format_date(&meeting, "EEEE"));
    
    // 发票日期
    let invoice = parse_date("2024-03-01").unwrap();
    println!("   📄 发票日期:");
    println!("      格式：'Invoice Date: MMM D, YYYY'");
    println!("      输出：'Invoice Date: {}'\n", 
             format_date(&invoice, "MMM D, YYYY"));
    
    // 新闻标题
    let news_date = parse_date("2024-07-04").unwrap();
    println!("   📰 新闻标题:");
    println!("      格式：'MMMM D, YYYY - 重大新闻发布'");
    println!("      输出：'{} - 重大新闻发布'\n", 
             format_date(&news_date, "MMMM D, YYYY"));
    
    // 证书日期
    let cert_date = parse_date("2024-05-15").unwrap();
    println!("   🏆 证书日期:");
    println!("      格式：'授予日期：YYYY 年 MM 月 DD 日'");
    println!("      输出：'授予日期：{}'\n", 
             format_date(&cert_date, "YYYY 年 MM 月 DD 日"));

    // 8. 格式字符参考
    println!("8. 格式字符参考表:");
    println!("   ┌─────────┬────────────────────────────┬──────────────┐");
    println!("   │ 格式符  │ 描述                       │ 示例         │");
    println!("   ├─────────┼────────────────────────────┼──────────────┤");
    println!("   │ YYYY    │ 四位数年份                 │ 2024         │");
    println!("   │ YY      │ 两位数年份                 │ 24           │");
    println!("   │ MM      │ 两位数月份                 │ 03           │");
    println!("   │ M       │ 一位数月份                 │ 3            │");
    println!("   │ DD      │ 两位数日期                 │ 15           │");
    println!("   │ D       │ 一位数日期                 │ 15           │");
    println!("   │ MMMM    │ 完整月份名                 │ March        │");
    println!("   │ MMM     │ 缩写月份名                 │ Mar          │");
    println!("   │ EEEE    │ 完整星期名                 │ Friday       │");
    println!("   │ EEE     │ 缩写星期名                 │ Fri          │");
    println!("   │ D       │ 一年中的第几天             │ 75           │");
    println!("   │ W       │ 星期几 (1-7)               │ 5            │");
    println!("   └─────────┴────────────────────────────┴──────────────┘");
    println!();

    println!("=== 完成 ===");
}
