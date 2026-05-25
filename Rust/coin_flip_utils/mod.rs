//! 抛硬币模拟工具库 - 零外部依赖
//!
//! 提供完整的抛硬币模拟功能，包括单次抛掷、多次抛掷、概率统计分析
//! 支持自定义硬币、历史记录、统计可视化等功能

use std::time::{SystemTime, UNIX_EPOCH};

/// 硬币结果
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum CoinFace {
    /// 正面（通常为头像面）
    Heads,
    /// 反面（通常为数字/图案面）
    Tails,
}

impl CoinFace {
    /// 获取结果名称
    pub fn name(&self) -> &'static str {
        match self {
            CoinFace::Heads => "正面",
            CoinFace::Tails => "反面",
        }
    }

    /// 获取英文名称
    pub fn name_en(&self) -> &'static str {
        match self {
            CoinFace::Heads => "Heads",
            CoinFace::Tails => "Tails",
        }
    }

    /// 翻转到另一面
    pub fn flip(&self) -> CoinFace {
        match self {
            CoinFace::Heads => CoinFace::Tails,
            CoinFace::Tails => CoinFace::Heads,
        }
    }

    /// 从布尔值创建
    pub fn from_bool(value: bool) -> Self {
        if value { CoinFace::Heads } else { CoinFace::Tails }
    }

    /// 转换为布尔值（正面为 true）
    pub fn to_bool(&self) -> bool {
        matches!(self, CoinFace::Heads)
    }

    /// 从数字创建（偶数为正面，奇数为反面）
    pub fn from_number(n: u64) -> Self {
        CoinFace::from_bool(n % 2 == 0)
    }
}

impl std::fmt::Display for CoinFace {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{}", self.name())
    }
}

/// 自定义硬币
#[derive(Debug, Clone)]
pub struct Coin {
    /// 硬币名称
    pub name: String,
    /// 正面标签
    pub heads_label: String,
    /// 反面标签
    pub tails_label: String,
    /// 正面权重（0.0-1.0，默认 0.5 表示均匀硬币）
    pub bias: f64,
}

impl Coin {
    /// 创建标准硬币
    pub fn new(name: &str, heads_label: &str, tails_label: &str) -> Self {
        Coin {
            name: name.to_string(),
            heads_label: heads_label.to_string(),
            tails_label: tails_label.to_string(),
            bias: 0.5,
        }
    }

    /// 创建均匀的标准硬币
    pub fn fair() -> Self {
        Coin::new("标准硬币", "正面", "反面")
    }

    /// 创建有偏差的硬币
    pub fn biased(name: &str, heads_label: &str, tails_label: &str, bias: f64) -> Self {
        let bias = bias.clamp(0.0, 1.0);
        Coin {
            name: name.to_string(),
            heads_label: heads_label.to_string(),
            tails_label: tails_label.to_string(),
            bias,
        }
    }

    /// 创建人民币一元硬币
    pub fn rmb_1() -> Self {
        Coin::new("人民币一元", "国徽", "菊花")
    }

    /// 创建美元硬币
    pub fn usd_quarter() -> Self {
        Coin::new("美元25美分", "华盛顿", "鹰")
    }

    /// 创建欧元硬币
    pub fn eur_1() -> Self {
        Coin::new("欧元1元", "欧洲地图", "成员国图案")
    }

    /// 创建比特币
    pub fn bitcoin() -> Self {
        Coin::new("比特币", "₿", "白皮书")
    }

    /// 设置偏差
    pub fn with_bias(mut self, bias: f64) -> Self {
        self.bias = bias.clamp(0.0, 1.0);
        self
    }

    /// 获取正面标签
    pub fn label(&self, face: CoinFace) -> &str {
        match face {
            CoinFace::Heads => &self.heads_label,
            CoinFace::Tails => &self.tails_label,
        }
    }

    /// 检查是否为均匀硬币
    pub fn is_fair(&self) -> bool {
        (self.bias - 0.5).abs() < 1e-10
    }
}

impl Default for Coin {
    fn default() -> Self {
        Coin::fair()
    }
}

/// 简单伪随机数生成器（XorShift64）
#[derive(Debug, Clone)]
pub struct SimpleRng {
    state: u64,
}

impl SimpleRng {
    /// 从时间戳创建随机数生成器
    pub fn from_time() -> Self {
        let timestamp = SystemTime::now()
            .duration_since(UNIX_EPOCH)
            .unwrap_or_default()
            .as_nanos() as u64;
        Self::from_seed(timestamp)
    }

    /// 从种子创建随机数生成器
    pub fn from_seed(seed: u64) -> Self {
        let state = if seed == 0 { 1 } else { seed };
        SimpleRng { state }
    }

    /// 生成下一个随机数
    pub fn next_u64(&mut self) -> u64 {
        // XorShift64 算法
        let mut x = self.state;
        x ^= x << 13;
        x ^= x >> 7;
        x ^= x << 17;
        self.state = x;
        x
    }

    /// 生成 [0, 1) 范围的随机浮点数
    pub fn next_f64(&mut self) -> f64 {
        (self.next_u64() as f64) / (u64::MAX as f64)
    }

    /// 生成 [0, max) 范围的随机整数
    pub fn next_range(&mut self, max: u64) -> u64 {
        self.next_u64() % max
    }

    /// 根据概率生成布尔值
    pub fn next_bool_with_prob(&mut self, probability: f64) -> bool {
        self.next_f64() < probability
    }
}

/// 抛硬币结果
#[derive(Debug, Clone)]
pub struct FlipResult {
    /// 硬币面
    pub face: CoinFace,
    /// 硬币标签
    pub label: String,
    /// 抛掷序号
    pub index: usize,
}

impl FlipResult {
    fn new(face: CoinFace, coin: &Coin, index: usize) -> Self {
        FlipResult {
            face,
            label: coin.label(face).to_string(),
            index,
        }
    }
}

/// 多次抛掷统计
#[derive(Debug, Clone, Default)]
pub struct FlipStats {
    /// 正面次数
    pub heads_count: usize,
    /// 反面次数
    pub tails_count: usize,
    /// 总次数
    pub total_flips: usize,
    /// 结果序列
    pub sequence: Vec<CoinFace>,
}

impl FlipStats {
    /// 创建空统计
    pub fn new() -> Self {
        FlipStats::default()
    }

    /// 从序列创建统计
    pub fn from_sequence(sequence: Vec<CoinFace>) -> Self {
        let heads_count = sequence.iter().filter(|f| **f == CoinFace::Heads).count();
        let tails_count = sequence.len() - heads_count;
        FlipStats {
            heads_count,
            tails_count,
            total_flips: sequence.len(),
            sequence,
        }
    }

    /// 记录一次结果
    pub fn record(&mut self, face: CoinFace) {
        match face {
            CoinFace::Heads => self.heads_count += 1,
            CoinFace::Tails => self.tails_count += 1,
        }
        self.total_flips += 1;
        self.sequence.push(face);
    }

    /// 正面比例
    pub fn heads_ratio(&self) -> f64 {
        if self.total_flips == 0 {
            0.0
        } else {
            self.heads_count as f64 / self.total_flips as f64
        }
    }

    /// 反面比例
    pub fn tails_ratio(&self) -> f64 {
        if self.total_flips == 0 {
            0.0
        } else {
            self.tails_count as f64 / self.total_flips as f64
        }
    }

    /// 最长连续正面
    pub fn longest_heads_streak(&self) -> usize {
        self.longest_streak(CoinFace::Heads)
    }

    /// 最长连续反面
    pub fn longest_tails_streak(&self) -> usize {
        self.longest_streak(CoinFace::Tails)
    }

    fn longest_streak(&self, target: CoinFace) -> usize {
        let mut max_streak = 0;
        let mut current_streak = 0;

        for face in &self.sequence {
            if *face == target {
                current_streak += 1;
                max_streak = max_streak.max(current_streak);
            } else {
                current_streak = 0;
            }
        }

        max_streak
    }

    /// 所有连续序列
    pub fn all_streaks(&self) -> Vec<(CoinFace, usize)> {
        let mut streaks = Vec::new();
        if self.sequence.is_empty() {
            return streaks;
        }

        let mut current_face = self.sequence[0];
        let mut current_length = 1;

        for face in self.sequence.iter().skip(1) {
            if *face == current_face {
                current_length += 1;
            } else {
                streaks.push((current_face, current_length));
                current_face = *face;
                current_length = 1;
            }
        }
        streaks.push((current_face, current_length));

        streaks
    }

    /// 生成可视化图表（ASCII）
    pub fn visualize(&self, width: usize) -> String {
        if self.total_flips == 0 {
            return "无数据".to_string();
        }

        let bar_width = width.saturating_sub(10);
        let heads_bar_len = (self.heads_ratio() * bar_width as f64) as usize;
        let tails_bar_len = bar_width - heads_bar_len;

        format!(
            "正面: {:>5} ({:>5.1}%) [{}{}]\n反面: {:>5} ({:>5.1}%) [{}{}]",
            self.heads_count,
            self.heads_ratio() * 100.0,
            "█".repeat(heads_bar_len),
            " ".repeat(tails_bar_len),
            self.tails_count,
            self.tails_ratio() * 100.0,
            "█".repeat(tails_bar_len),
            " ".repeat(heads_bar_len),
        )
    }

    /// 概率分析报告
    pub fn analyze(&self) -> String {
        if self.total_flips == 0 {
            return "暂无抛掷数据".to_string();
        }

        let expected_ratio = 0.5;
        let deviation = (self.heads_ratio() - expected_ratio).abs();
        let z_score = if self.total_flips > 0 {
            (self.heads_count as f64 - self.total_flips as f64 / 2.0)
                / (self.total_flips as f64 / 4.0).sqrt()
        } else {
            0.0
        };

        let mut report = format!(
            "=== 抛硬币统计分析 ===\n\
             总次数: {}\n\
             正面: {} ({:.2}%)\n\
             反面: {} ({:.2}%)\n\
             偏差: {:.4}\n\
             Z分数: {:.4}\n\
             最长正面连续: {}\n\
             最长反面连续: {}",
            self.total_flips,
            self.heads_count,
            self.heads_ratio() * 100.0,
            self.tails_count,
            self.tails_ratio() * 100.0,
            deviation,
            z_score,
            self.longest_heads_streak(),
            self.longest_tails_streak()
        );

        // 正态性检验（粗略）
        if self.total_flips >= 30 {
            let is_normal = z_score.abs() < 1.96;
            report.push_str(&format!(
                "\n均匀性检验: {}",
                if is_normal { "通过（95%置信度）" } else { "未通过（可能不均匀）" }
            ));
        } else {
            report.push_str("\n均匀性检验: 样本不足（需≥30次）");
        }

        report
    }
}

/// 抛硬币器
#[derive(Debug)]
pub struct CoinFlipper {
    coin: Coin,
    rng: SimpleRng,
    stats: FlipStats,
    history: Vec<FlipResult>,
}

impl CoinFlipper {
    /// 创建新的抛硬币器
    pub fn new(coin: Coin) -> Self {
        CoinFlipper {
            coin,
            rng: SimpleRng::from_time(),
            stats: FlipStats::new(),
            history: Vec::new(),
        }
    }

    /// 创建使用种子的抛硬币器（可重复）
    pub fn with_seed(coin: Coin, seed: u64) -> Self {
        CoinFlipper {
            coin,
            rng: SimpleRng::from_seed(seed),
            stats: FlipStats::new(),
            history: Vec::new(),
        }
    }

    /// 创建标准抛硬币器
    pub fn fair() -> Self {
        CoinFlipper::new(Coin::fair())
    }

    /// 创建有偏差的抛硬币器
    pub fn biased(bias: f64) -> Self {
        CoinFlipper::new(Coin::fair().with_bias(bias))
    }

    /// 获取硬币引用
    pub fn coin(&self) -> &Coin {
        &self.coin
    }

    /// 获取统计引用
    pub fn stats(&self) -> &FlipStats {
        &self.stats
    }

    /// 获取历史记录
    pub fn history(&self) -> &[FlipResult] {
        &self.history
    }

    /// 抛一次硬币
    pub fn flip(&mut self) -> FlipResult {
        let index = self.stats.total_flips;
        let is_heads = self.rng.next_bool_with_prob(self.coin.bias);
        let face = if is_heads { CoinFace::Heads } else { CoinFace::Tails };

        self.stats.record(face);

        let result = FlipResult::new(face, &self.coin, index);
        self.history.push(result.clone());

        result
    }

    /// 抛多次硬币
    pub fn flip_n(&mut self, n: usize) -> Vec<FlipResult> {
        (0..n).map(|_| self.flip()).collect()
    }

    /// 快速抛多次（不保存历史）
    pub fn flip_n_fast(&mut self, n: usize) -> FlipStats {
        let mut stats = FlipStats::new();
        for _ in 0..n {
            let is_heads = self.rng.next_bool_with_prob(self.coin.bias);
            let face = if is_heads { CoinFace::Heads } else { CoinFace::Tails };
            stats.record(face);
        }
        stats
    }

    /// 重置统计和历史
    pub fn reset(&mut self) {
        self.stats = FlipStats::new();
        self.history.clear();
    }

    /// 设置新种子
    pub fn set_seed(&mut self, seed: u64) {
        self.rng = SimpleRng::from_seed(seed);
    }

    /// 重新设置硬币
    pub fn set_coin(&mut self, coin: Coin) {
        self.coin = coin;
    }
}

/// 全局单次抛硬币（使用时间种子）
pub fn flip() -> CoinFace {
    flip_with_coin(&Coin::fair())
}

/// 使用指定硬币抛一次
pub fn flip_with_coin(coin: &Coin) -> CoinFace {
    let mut rng = SimpleRng::from_time();
    if rng.next_bool_with_prob(coin.bias) {
        CoinFace::Heads
    } else {
        CoinFace::Tails
    }
}

/// 抛多次硬币并返回统计
pub fn flip_n(n: usize) -> FlipStats {
    flip_n_with_coin(n, &Coin::fair())
}

/// 使用指定硬币抛多次
pub fn flip_n_with_coin(n: usize, coin: &Coin) -> FlipStats {
    let mut flipper = CoinFlipper::new(coin.clone());
    flipper.flip_n_fast(n)
}

/// 抛硬币决断（帮助做决定）
pub fn decide(question: &str) -> String {
    let result = flip();
    format!(
        "🪙 问题: {}\n   结果: {}\n   建议: {}",
        question,
        result.name(),
        if result == CoinFace::Heads { "去做吧！" } else { "再考虑考虑..." }
    )
}

/// 三次抛硬币（三局两胜）
pub fn best_of_three() -> CoinFace {
    let mut flipper = CoinFlipper::fair();
    let mut heads_wins = 0;
    let mut tails_wins = 0;

    for _ in 0..3 {
        match flipper.flip().face {
            CoinFace::Heads => heads_wins += 1,
            CoinFace::Tails => tails_wins += 1,
        }
        if heads_wins >= 2 {
            return CoinFace::Heads;
        }
        if tails_wins >= 2 {
            return CoinFace::Tails;
        }
    }

    // 如果2:1，返回多的那个
    if heads_wins > tails_wins {
        CoinFace::Heads
    } else {
        CoinFace::Tails
    }
}

/// 幸运抛硬币（连续指定次数相同结果算赢）
pub fn lucky_flip(streak_required: usize) -> Option<(CoinFace, usize)> {
    if streak_required == 0 {
        return None;
    }

    let mut flipper = CoinFlipper::fair();
    let mut current_face = flipper.flip().face;
    let mut streak = 1;

    while streak < streak_required {
        let result = flipper.flip().face;
        if result == current_face {
            streak += 1;
        } else {
            current_face = result;
            streak = 1;
        }

        // 防止无限循环（最多尝试10000次）
        if flipper.stats().total_flips > 10000 {
            return None;
        }
    }

    Some((current_face, flipper.stats().total_flips))
}

/// 模拟蒙特卡洛实验
pub fn monte_carlo(n: usize) -> MonteCarloResult {
    let mut flipper = CoinFlipper::fair();
    let stats = flipper.flip_n_fast(n);

    MonteCarloResult {
        sample_size: n,
        heads_ratio: stats.heads_ratio(),
        deviation_from_expected: (stats.heads_ratio() - 0.5).abs(),
        longest_heads_streak: stats.longest_heads_streak(),
        longest_tails_streak: stats.longest_tails_streak(),
    }
}

/// 蒙特卡洛实验结果
#[derive(Debug, Clone)]
pub struct MonteCarloResult {
    /// 样本大小
    pub sample_size: usize,
    /// 正面比例
    pub heads_ratio: f64,
    /// 与期望值的偏差
    pub deviation_from_expected: f64,
    /// 最长正面连续
    pub longest_heads_streak: usize,
    /// 最长反面连续
    pub longest_tails_streak: usize,
}

impl MonteCarloResult {
    /// 格式化报告
    pub fn report(&self) -> String {
        format!(
            "=== 蒙特卡洛模拟 ===\n\
             样本量: {}\n\
             正面比例: {:.4} (期望: 0.5000)\n\
             偏差: {:.6}\n\
             最长正面连续: {}\n\
             最长反面连续: {}",
            self.sample_size,
            self.heads_ratio,
            self.deviation_from_expected,
            self.longest_heads_streak,
            self.longest_tails_streak
        )
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_coin_face_flip() {
        assert_eq!(CoinFace::Heads.flip(), CoinFace::Tails);
        assert_eq!(CoinFace::Tails.flip(), CoinFace::Heads);
    }

    #[test]
    fn test_coin_face_bool() {
        assert_eq!(CoinFace::from_bool(true), CoinFace::Heads);
        assert_eq!(CoinFace::from_bool(false), CoinFace::Tails);
        assert!(CoinFace::Heads.to_bool());
        assert!(!CoinFace::Tails.to_bool());
    }

    #[test]
    fn test_coin_face_from_number() {
        assert_eq!(CoinFace::from_number(0), CoinFace::Heads); // 偶数
        assert_eq!(CoinFace::from_number(1), CoinFace::Tails); // 奇数
        assert_eq!(CoinFace::from_number(2), CoinFace::Heads);
        assert_eq!(CoinFace::from_number(3), CoinFace::Tails);
    }

    #[test]
    fn test_coin_creation() {
        let coin = Coin::fair();
        assert!(coin.is_fair());
        assert_eq!(coin.name, "标准硬币");
        assert_eq!(coin.heads_label, "正面");
        assert_eq!(coin.tails_label, "反面");
    }

    #[test]
    fn test_biased_coin() {
        let coin = Coin::biased("作弊硬币", "赢", "输", 0.8);
        assert_eq!(coin.bias, 0.8);
        assert!(!coin.is_fair());
    }

    #[test]
    fn test_coin_with_bias() {
        let coin = Coin::fair().with_bias(0.3);
        assert_eq!(coin.bias, 0.3);
    }

    #[test]
    fn test_coin_labels() {
        let coin = Coin::rmb_1();
        assert_eq!(coin.label(CoinFace::Heads), "国徽");
        assert_eq!(coin.label(CoinFace::Tails), "菊花");
    }

    #[test]
    fn test_simple_rng_reproducible() {
        let mut rng1 = SimpleRng::from_seed(12345);
        let mut rng2 = SimpleRng::from_seed(12345);

        for _ in 0..10 {
            assert_eq!(rng1.next_u64(), rng2.next_u64());
        }
    }

    #[test]
    fn test_simple_rng_range() {
        let mut rng = SimpleRng::from_seed(42);
        for _ in 0..100 {
            let val = rng.next_range(10);
            assert!(val < 10);
        }
    }

    #[test]
    fn test_simple_rng_probability() {
        let mut rng = SimpleRng::from_seed(42);
        let mut heads = 0;
        let trials = 10000;
        for _ in 0..trials {
            if rng.next_bool_with_prob(0.5) {
                heads += 1;
            }
        }
        let ratio = heads as f64 / trials as f64;
        // 应该接近 0.5，允许 5% 的偏差
        assert!((ratio - 0.5).abs() < 0.05);
    }

    #[test]
    fn test_flipper_basic() {
        let mut flipper = CoinFlipper::fair();
        let result = flipper.flip();
        assert!(result.face == CoinFace::Heads || result.face == CoinFace::Tails);
        assert_eq!(result.index, 0);
        assert_eq!(flipper.stats().total_flips, 1);
    }

    #[test]
    fn test_flipper_multiple() {
        let mut flipper = CoinFlipper::fair();
        let results = flipper.flip_n(100);
        assert_eq!(results.len(), 100);
        assert_eq!(flipper.stats().total_flips, 100);
    }

    #[test]
    fn test_flipper_biased() {
        let coin = Coin::fair().with_bias(1.0); // 总是正面
        let mut flipper = CoinFlipper::with_seed(coin, 42);

        for _ in 0..100 {
            let result = flipper.flip();
            assert_eq!(result.face, CoinFace::Heads);
        }
    }

    #[test]
    fn test_flipper_reproducible() {
        let coin = Coin::fair();

        let mut flipper1 = CoinFlipper::with_seed(coin.clone(), 12345);
        let results1: Vec<_> = flipper1.flip_n(10).iter().map(|r| r.face).collect();

        let mut flipper2 = CoinFlipper::with_seed(coin, 12345);
        let results2: Vec<_> = flipper2.flip_n(10).iter().map(|r| r.face).collect();

        assert_eq!(results1, results2);
    }

    #[test]
    fn test_flip_stats() {
        let mut stats = FlipStats::new();
        stats.record(CoinFace::Heads);
        stats.record(CoinFace::Heads);
        stats.record(CoinFace::Tails);

        assert_eq!(stats.heads_count, 2);
        assert_eq!(stats.tails_count, 1);
        assert_eq!(stats.total_flips, 3);
        assert!((stats.heads_ratio() - 0.6666).abs() < 0.01);
    }

    #[test]
    fn test_flip_stats_streaks() {
        let sequence = vec![
            CoinFace::Heads, CoinFace::Heads, CoinFace::Heads,
            CoinFace::Tails, CoinFace::Tails,
            CoinFace::Heads,
        ];
        let stats = FlipStats::from_sequence(sequence);

        assert_eq!(stats.longest_heads_streak(), 3);
        assert_eq!(stats.longest_tails_streak(), 2);
    }

    #[test]
    fn test_flip_stats_all_streaks() {
        let sequence = vec![
            CoinFace::Heads, CoinFace::Heads,
            CoinFace::Tails,
            CoinFace::Heads, CoinFace::Heads, CoinFace::Heads,
        ];
        let stats = FlipStats::from_sequence(sequence);
        let streaks = stats.all_streaks();

        assert_eq!(streaks, vec![
            (CoinFace::Heads, 2),
            (CoinFace::Tails, 1),
            (CoinFace::Heads, 3),
        ]);
    }

    #[test]
    fn test_flip_stats_visualize() {
        let mut stats = FlipStats::new();
        for _ in 0..50 {
            stats.record(CoinFace::Heads);
        }
        for _ in 0..50 {
            stats.record(CoinFace::Tails);
        }

        let visual = stats.visualize(50);
        assert!(visual.contains("正面"));
        assert!(visual.contains("反面"));
        assert!(visual.contains("50"));
    }

    #[test]
    fn test_flip_stats_analyze() {
        let mut stats = FlipStats::new();
        for _ in 0..50 {
            stats.record(CoinFace::Heads);
        }
        for _ in 0..50 {
            stats.record(CoinFace::Tails);
        }

        let report = stats.analyze();
        assert!(report.contains("总次数: 100"));
        assert!(report.contains("均匀性检验"));
    }

    #[test]
    fn test_global_flip() {
        let result = flip();
        assert!(result == CoinFace::Heads || result == CoinFace::Tails);
    }

    #[test]
    fn test_global_flip_n() {
        let stats = flip_n(1000);
        assert_eq!(stats.total_flips, 1000);
        // 正面比例应该在 0.4 到 0.6 之间（统计规律）
        assert!(stats.heads_ratio() > 0.4 && stats.heads_ratio() < 0.6);
    }

    #[test]
    fn test_best_of_three() {
        let winner = best_of_three();
        assert!(winner == CoinFace::Heads || winner == CoinFace::Tails);
    }

    #[test]
    fn test_decide() {
        let result = decide("今天去跑步吗？");
        assert!(result.contains("今天去跑步吗？"));
        assert!(result.contains("结果:"));
    }

    #[test]
    fn test_lucky_flip_impossible() {
        // 连续10次相同几乎不可能在10000次内完成
        let result = lucky_flip(100);
        assert!(result.is_none());
    }

    #[test]
    fn test_lucky_flip_possible() {
        // 连续2次相同很容易
        let result = lucky_flip(2);
        assert!(result.is_some());
        let (face, count) = result.unwrap();
        assert!(face == CoinFace::Heads || face == CoinFace::Tails);
        assert!(count >= 2);
    }

    #[test]
    fn test_monte_carlo() {
        let result = monte_carlo(10000);
        assert_eq!(result.sample_size, 10000);
        // 大数定律：正面比例应该接近 0.5
        assert!((result.heads_ratio - 0.5).abs() < 0.05);
    }

    #[test]
    fn test_monte_carlo_report() {
        let result = monte_carlo(1000);
        let report = result.report();
        assert!(report.contains("蒙特卡洛模拟"));
        assert!(report.contains("样本量: 1000"));
    }

    #[test]
    fn test_flip_n_fast() {
        let mut flipper = CoinFlipper::fair();
        let stats = flipper.flip_n_fast(10000);
        assert_eq!(stats.total_flips, 10000);
        // 大数定律
        assert!((stats.heads_ratio() - 0.5).abs() < 0.05);
    }

    #[test]
    fn test_flipper_reset() {
        let mut flipper = CoinFlipper::fair();
        flipper.flip_n(100);
        assert_eq!(flipper.stats().total_flips, 100);

        flipper.reset();
        assert_eq!(flipper.stats().total_flips, 0);
        assert!(flipper.history().is_empty());
    }

    #[test]
    fn test_history_tracking() {
        let mut flipper = CoinFlipper::with_seed(Coin::fair(), 42);
        flipper.flip_n(5);

        assert_eq!(flipper.history().len(), 5);
        for (i, result) in flipper.history().iter().enumerate() {
            assert_eq!(result.index, i);
        }
    }

    #[test]
    fn test_predefined_coins() {
        assert_eq!(Coin::rmb_1().name, "人民币一元");
        assert_eq!(Coin::usd_quarter().name, "美元25美分");
        assert_eq!(Coin::eur_1().name, "欧元1元");
        assert_eq!(Coin::bitcoin().name, "比特币");
    }
}