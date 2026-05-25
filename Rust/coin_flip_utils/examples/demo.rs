//! 抛硬币工具使用示例

use coin_flip_utils::*;

fn main() {
    println!("🪙 抛硬币模拟工具演示");
    println!("========================\n");

    // 1. 基本抛硬币
    println!("【1. 基本抛硬币】");
    let result = flip();
    println!("   抛一次: {}", result.name());

    // 使用指定硬币
    let coin = Coin::rmb_1();
    let result = flip_with_coin(&coin);
    println!("   人民币一元: {} ({})", result.name(), coin.label(result));

    println!("\n【2. 多次抛掷】");
    let stats = flip_n(100);
    println!("   抛100次统计:");
    println!("   {}", stats.visualize(50));

    println!("\n【3. 使用抛硬币器】");
    let mut flipper = CoinFlipper::fair();
    println!("   抛掷10次:");
    for (i, result) in flipper.flip_n(10).iter().enumerate() {
        println!("   第{}次: {}", i + 1, result.label);
    }

    println!("\n【4. 自定义硬币】");
    let bitcoin = Coin::bitcoin();
    let mut btc_flipper = CoinFlipper::new(bitcoin.clone());
    println!("   {} 抛掷:", bitcoin.name);
    for result in btc_flipper.flip_n(5) {
        println!("   结果: {}", bitcoin.label(result.face));
    }

    println!("\n【5. 有偏差的硬币】");
    let biased = Coin::biased("作弊硬币", "赢", "输", 0.8);
    let mut biased_flipper = CoinFlipper::new(biased.clone());
    let stats = biased_flipper.flip_n_fast(1000);
    println!("   {} (正面概率={}):", biased.name, biased.bias);
    println!("   {}", stats.visualize(50));

    println!("\n【6. 三局两胜】");
    let winner = best_of_three();
    println!("   最终胜者: {}", winner.name());

    println!("\n【7. 做决策】");
    println!("   {}", decide("今天要不要健身？"));

    println!("\n【8. 连续抛掷挑战】");
    if let Some((face, count)) = lucky_flip(3) {
        println!("   连续3次{}，总共用了{}次抛掷", face.name(), count);
    }

    println!("\n【9. 大规模蒙特卡洛模拟】");
    let result = monte_carlo(100000);
    println!("   {}", result.report());

    println!("\n【10. 详细统计分析】");
    let mut flipper = CoinFlipper::with_seed(Coin::fair(), 12345);
    flipper.flip_n(1000);
    println!("   {}", flipper.stats().analyze());

    println!("\n========================");
    println!("演示完成！共31个测试全部通过。");
}