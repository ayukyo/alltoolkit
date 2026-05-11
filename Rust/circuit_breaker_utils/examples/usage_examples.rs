//! 熔断器使用示例
//!
//! 展示熔断器在各种场景下的使用方法

use std::thread;
use std::time::Duration;

mod mod;
use mod::{CircuitBreaker, CircuitBreakerBuilder, CircuitState};

fn main() {
    println!("=== 熔断器 (Circuit Breaker) 使用示例 ===\n");
    
    // 示例1: 基本使用
    basic_usage();
    
    // 示例2: API调用保护
    api_call_protection();
    
    // 示例3: 数据库连接保护
    database_connection_protection();
    
    // 示例4: 使用构建器配置
    builder_pattern();
    
    // 示例5: 监控和统计
    monitoring_and_stats();
    
    // 示例6: 手动控制
    manual_control();
    
    // 示例7: 多个熔断器协作
    multiple_circuit_breakers();
}

/// 示例1: 基本使用
fn basic_usage() {
    println!("--- 示例1: 基本使用 ---");
    
    // 创建熔断器：连续5次失败触发熔断，连续3次成功恢复，熔断持续30秒
    let breaker = CircuitBreaker::new(5, 3, 30);
    
    println!("初始状态: {:?}", breaker.state());
    
    // 执行成功操作
    match breaker.call(|| {
        // 模拟可能失败的操作
        Ok::<String, String>("操作成功".to_string())
    }) {
        Ok(result) => println!("✓ {}", result),
        Err(e) => println!("✗ {}", e),
    }
    
    println!("当前状态: {:?}\n", breaker.state());
}

/// 示例2: API调用保护
fn api_call_protection() {
    println!("--- 示例2: API调用保护 ---");
    
    let breaker = CircuitBreaker::new(3, 2, 10);
    let mut call_count = 0;
    
    // 模拟一个不稳定的API
    let unstable_api = || -> Result<String, String> {
        call_count += 1;
        if call_count <= 5 {
            Err("API 服务不可用".to_string())
        } else {
            Ok("API 响应成功".to_string())
        }
    };
    
    // 尝试调用API
    for i in 1..=10 {
        match breaker.call(|| unstable_api()) {
            Ok(response) => println!("请求 {}: ✓ {}", i, response),
            Err(e) => println!("请求 {}: ✗ {}", i, e),
        }
        
        if breaker.state() == CircuitState::Open {
            println!("熔断器打开，等待恢复...");
            thread::sleep(Duration::from_millis(500));
        }
    }
    
    println!("最终状态: {:?}\n", breaker.state());
}

/// 示例3: 数据库连接保护
fn database_connection_protection() {
    println!("--- 示例3: 数据库连接保护 ---");
    
    let db_breaker = CircuitBreakerBuilder::new()
        .failure_threshold(3)
        .success_threshold(2)
        .timeout_secs(5)
        .half_open_max_calls(1)
        .build();
    
    println!("数据库熔断器配置:");
    println!("  - 失败阈值: 3次");
    println!("  - 成功阈值: 2次");
    println!("  - 熔断超时: 5秒");
    println!("  - 半开探测数: 1次\n");
    
    // 模拟数据库查询
    fn query_database(query: &str) -> Result<Vec<String>, String> {
        // 模拟查询逻辑
        if query.contains("error") {
            Err("数据库连接失败".to_string())
        } else {
            Ok(vec!["结果1".to_string(), "结果2".to_string()])
        }
    }
    
    // 执行查询
    let queries = vec!["SELECT * FROM users", "SELECT error", "SELECT * FROM products"];
    
    for query in queries {
        match db_breaker.call(|| query_database(query)) {
            Ok(results) => println!("查询 '{}': ✓ {:?}", query, results),
            Err(e) => println!("查询 '{}': ✗ {}", query, e),
        }
    }
    
    println!("\n数据库熔断器统计:");
    let stats = db_breaker.stats();
    println!("  - 总请求: {}", stats.total_requests);
    println!("  - 成功: {}", stats.successful_requests);
    println!("  - 失败: {}", stats.failed_requests);
    println!("  - 失败率: {:.1}%\n", db_breaker.failure_rate());
}

/// 示例4: 使用构建器配置
fn builder_pattern() {
    println!("--- 示例4: 使用构建器配置 ---");
    
    // 使用构建器创建自定义配置的熔断器
    let breaker = CircuitBreakerBuilder::new()
        .failure_threshold(10)        // 连续10次失败触发熔断
        .success_threshold(5)         // 连续5次成功关闭熔断
        .timeout_secs(60)              // 熔断持续60秒
        .half_open_max_calls(3)        // 半开状态允许3个探测请求
        .fail_fast_on_half_open(true)  // 半开状态失败立即重新打开
        .build();
    
    println!("自定义配置:");
    let config = breaker.config();
    println!("  - 失败阈值: {}", config.failure_threshold);
    println!("  - 成功阈值: {}", config.success_threshold);
    println!("  - 熔断超时: {}秒", config.timeout_secs);
    println!("  - 半开探测数: {}", config.half_open_max_calls);
    println!("  - 半开快速失败: {}\n", config.fail_fast_on_half_open);
    
    // 执行一些操作
    for i in 0..5 {
        let _ = breaker.call(|| {
            if i % 2 == 0 {
                Err::<(), String>("偶数索引失败".to_string())
            } else {
                Ok(())
            }
        });
    }
    
    println!("执行5次操作后的统计:");
    println!("  - 成功率: {:.1}%\n", breaker.success_rate());
}

/// 示例5: 监控和统计
fn monitoring_and_stats() {
    println!("--- 示例5: 监控和统计 ---");
    
    let breaker = CircuitBreaker::new(5, 3, 30);
    
    // 执行一系列操作
    println!("执行操作序列: 成功, 成功, 失败, 成功, 失败, 失败, 失败, 失败, 失败");
    
    let results = vec![true, true, false, true, false, false, false, false, false];
    
    for (i, &success) in results.iter().enumerate() {
        let _ = breaker.call(|| {
            if success {
                Ok::<(), String>(())
            } else {
                Err("操作失败".to_string())
            }
        });
        
        println!("操作 {}: {} | 状态: {:?} | 失败率: {:.1}%",
            i + 1,
            if success { "成功" } else { "失败" },
            breaker.state(),
            breaker.failure_rate()
        );
    }
    
    println!("\n最终统计:");
    let stats = breaker.stats();
    println!("  - 总请求数: {}", stats.total_requests);
    println!("  - 成功请求: {}", stats.successful_requests);
    println!("  - 失败请求: {}", stats.failed_requests);
    println!("  - 连续失败: {}", stats.consecutive_failures);
    println!("  - 连续成功: {}", stats.consecutive_successes);
    println!("  - 状态转换次数: {}", stats.state_transitions);
    println!("  - 成功率: {:.1}%", breaker.success_rate());
    println!("  - 失败率: {:.1}%\n", breaker.failure_rate());
}

/// 示例6: 手动控制
fn manual_control() {
    println!("--- 示例6: 手动控制 ---");
    
    let breaker = CircuitBreaker::new(10, 5, 30);
    
    println!("初始状态: {:?}", breaker.state());
    
    // 手动触发熔断（例如在维护期间）
    println!("\n执行维护，手动打开熔断器...");
    breaker.trip();
    println!("当前状态: {:?}", breaker.state());
    
    // 尝试调用会被拒绝
    match breaker.call(|| Ok::<String, String>("这不会执行".to_string())) {
        Ok(_) => println!("✗ 不应该成功"),
        Err(_) => println!("✓ 请求被拒绝（熔断器打开）"),
    }
    
    // 维护完成后手动关闭
    println!("\n维护完成，手动关闭熔断器...");
    breaker.reset();
    println!("当前状态: {:?}", breaker.state());
    
    // 现在可以正常调用
    match breaker.call(|| Ok::<String, String>("操作成功".to_string())) {
        Ok(result) => println!("✓ {}", result),
        Err(_) => println!("✗ 不应该失败"),
    }
    
    // 重置统计
    println!("\n重置统计数据...");
    breaker.reset_stats();
    println!("总请求数: {} (应该为0)\n", breaker.stats().total_requests);
}

/// 示例7: 多个熔断器协作
fn multiple_circuit_breakers() {
    println!("--- 示例7: 多个熔断器协作 ---");
    
    // 为不同的服务创建独立的熔断器
    let api_breaker = CircuitBreaker::new(3, 2, 10);
    let db_breaker = CircuitBreaker::new(5, 3, 20);
    let cache_breaker = CircuitBreaker::new(10, 5, 15);
    
    println!("创建三个服务的熔断器:");
    println!("  - API服务: 失败阈值3, 成功阈值2, 超时10秒");
    println!("  - 数据库: 失败阈值5, 成功阈值3, 超时20秒");
    println!("  - 缓存: 失败阈值10, 成功阈值5, 超时15秒\n");
    
    // 模拟服务调用
    fn call_api() -> Result<String, String> {
        Ok("API响应".to_string())
    }
    
    fn query_db() -> Result<String, String> {
        Err("数据库超时".to_string())
    }
    
    fn get_cache() -> Result<String, String> {
        Ok("缓存命中".to_string())
    }
    
    // 使用各个熔断器保护服务调用
    let api_result = api_breaker.call(call_api);
    let db_result = db_breaker.call(query_db);
    let cache_result = cache_breaker.call(get_cache);
    
    println!("服务调用结果:");
    println!("  - API: {:?}", api_result);
    println!("  - 数据库: {:?}", db_result);
    println!("  - 缓存: {:?}", cache_result);
    
    println!("\n各服务熔断器状态:");
    println!("  - API: {:?}", api_breaker.state());
    println!("  - 数据库: {:?}", db_breaker.state());
    println!("  - 缓存: {:?}", cache_breaker.state());
    
    println!("\n=== 所有示例完成 ===");
}

/// 实际应用场景示例
#[allow(dead_code)]
fn real_world_example() {
    // 在实际应用中，可以这样使用熔断器：
    
    // 1. 作为全局单例
    /*
    lazy_static! {
        static ref API_BREAKER: CircuitBreaker = CircuitBreaker::new(5, 3, 30);
    }
    
    fn make_api_request(endpoint: &str) -> Result<String, String> {
        API_BREAKER.call(|| {
            // 实际的HTTP请求
            let response = http_client.get(endpoint)?;
            Ok(response.body)
        })
    }
    */
    
    // 2. 在Web服务器中间件中使用
    /*
    fn circuit_breaker_middleware(breaker: Arc<CircuitBreaker>) -> impl Middleware {
        move |req, next| {
            if !breaker.is_call_allowed() {
                return Err(ServiceUnavailable);
            }
            breaker.call(|| next(req))
        }
    }
    */
    
    // 3. 结合重试机制
    /*
    fn call_with_retry<F, T, E>(breaker: &CircuitBreaker, mut f: F, max_retries: u32) -> Result<T, E>
    where
        F: FnMut() -> Result<T, E>,
    {
        let mut retries = 0;
        loop {
            match breaker.call(&mut f) {
                Ok(result) => return Ok(result),
                Err(CircuitError::CircuitOpen) => {
                    return Err(/* circuit open error */);
                }
                Err(CircuitError::OperationError(e)) => {
                    retries += 1;
                    if retries >= max_retries {
                        return Err(e);
                    }
                    thread::sleep(Duration::from_millis(100));
                }
            }
        }
    }
    */
}