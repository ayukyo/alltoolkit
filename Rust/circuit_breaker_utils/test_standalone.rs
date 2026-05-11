// 独立测试文件 - 不依赖 Cargo
// 可以直接用 rustc 编译测试

mod mod;
use mod::{CircuitBreaker, CircuitBreakerBuilder, CircuitState, CircuitError};
use std::thread;
use std::time::Duration;

fn main() {
    println!("=== 熔断器独立测试 ===\n");
    
    // 测试1: 初始状态
    println!("测试1: 初始状态应该是 Closed");
    let breaker = CircuitBreaker::new(5, 3, 30);
    assert_eq!(breaker.state(), CircuitState::Closed);
    println!("✓ 通过\n");
    
    // 测试2: 成功调用保持关闭状态
    println!("测试2: 成功调用应该保持 Closed 状态");
    let breaker = CircuitBreaker::new(3, 2, 10);
    for i in 0..10 {
        let result = breaker.call(|| Ok::<_, String>(format!("success {}", i)));
        assert!(result.is_ok());
        assert_eq!(breaker.state(), CircuitState::Closed);
    }
    println!("✓ 通过\n");
    
    // 测试3: 失败阈值触发熔断
    println!("测试3: 连续失败应该触发熔断");
    let breaker = CircuitBreaker::new(3, 2, 1);
    for _ in 0..3 {
        let _ = breaker.call(|| Err::<(), _>("error".to_string()));
    }
    assert_eq!(breaker.state(), CircuitState::Open);
    println!("✓ 通过\n");
    
    // 测试4: 熔断状态拒绝请求
    println!("测试4: Open 状态应该立即拒绝请求");
    let breaker = CircuitBreaker::new(2, 2, 10);
    for _ in 0..2 {
        let _ = breaker.call(|| Err::<(), _>("error".to_string()));
    }
    assert_eq!(breaker.state(), CircuitState::Open);
    
    let result = breaker.call(|| Ok::<(), String>(()));
    assert!(matches!(result, Err(CircuitError::CircuitOpen)));
    println!("✓ 通过\n");
    
    // 测试5: 半开状态恢复
    println!("测试5: 半开状态应该能够恢复");
    let breaker = CircuitBreaker::new(2, 2, 1);
    for _ in 0..2 {
        let _ = breaker.call(|| Err::<(), _>("error".to_string()));
    }
    assert_eq!(breaker.state(), CircuitState::Open);
    
    thread::sleep(Duration::from_millis(1100));
    assert_eq!(breaker.state(), CircuitState::HalfOpen);
    
    for _ in 0..2 {
        let _ = breaker.call(|| Ok::<(), String>(()));
    }
    assert_eq!(breaker.state(), CircuitState::Closed);
    println!("✓ 通过\n");
    
    // 测试6: 手动控制
    println!("测试6: 手动控制");
    let breaker = CircuitBreaker::new(10, 5, 30);
    breaker.trip();
    assert_eq!(breaker.state(), CircuitState::Open);
    
    breaker.reset();
    assert_eq!(breaker.state(), CircuitState::Closed);
    println!("✓ 通过\n");
    
    // 测试7: 统计信息
    println!("测试7: 统计信息跟踪");
    let breaker = CircuitBreaker::new(10, 5, 30);
    for i in 0..10 {
        let _ = breaker.call(|| {
            if i < 4 {
                Err::<(), String>("error".to_string())
            } else {
                Ok(())
            }
        });
    }
    
    let stats = breaker.stats();
    assert_eq!(stats.total_requests, 10);
    assert_eq!(stats.failed_requests, 4);
    assert_eq!(stats.successful_requests, 6);
    println!("✓ 通过\n");
    
    // 测试8: 失败率和成功率
    println!("测试8: 失败率和成功率计算");
    assert_eq!(breaker.failure_rate(), 40.0);
    assert_eq!(breaker.success_rate(), 60.0);
    println!("✓ 通过\n");
    
    // 测试9: 构建器模式
    println!("测试9: 构建器模式");
    let breaker = CircuitBreakerBuilder::new()
        .failure_threshold(7)
        .success_threshold(4)
        .timeout_secs(15)
        .half_open_max_calls(3)
        .fail_fast_on_half_open(false)
        .build();
    
    let config = breaker.config();
    assert_eq!(config.failure_threshold, 7);
    assert_eq!(config.success_threshold, 4);
    assert_eq!(config.timeout_secs, 15);
    println!("✓ 通过\n");
    
    // 测试10: is_call_allowed
    println!("测试10: is_call_allowed 方法");
    let breaker = CircuitBreaker::new(2, 2, 1);
    assert!(breaker.is_call_allowed());
    
    for _ in 0..2 {
        let _ = breaker.call(|| Err::<(), _>("error".to_string()));
    }
    assert!(!breaker.is_call_allowed());
    
    thread::sleep(Duration::from_millis(1100));
    assert!(breaker.is_call_allowed());
    println!("✓ 通过\n");
    
    // 测试11: try_call
    println!("测试11: try_call 方法");
    let breaker = CircuitBreaker::new(2, 2, 10);
    
    let result = breaker.try_call(|| Ok::<i32, String>(42));
    assert!(result.is_some());
    assert_eq!(result.unwrap(), Ok(42));
    
    for _ in 0..2 {
        let _ = breaker.call(|| Err::<(), _>("error".to_string()));
    }
    
    let result = breaker.try_call(|| Ok::<i32, String>(42));
    assert!(result.is_none());
    println!("✓ 通过\n");
    
    // 测试12: 重置统计
    println!("测试12: reset_stats");
    let breaker = CircuitBreaker::new(10, 5, 30);
    for _ in 0..10 {
        let _ = breaker.call(|| Ok::<(), String>(()));
    }
    assert_eq!(breaker.stats().total_requests, 10);
    
    breaker.reset_stats();
    let stats = breaker.stats();
    assert_eq!(stats.total_requests, 0);
    assert_eq!(stats.successful_requests, 0);
    assert_eq!(stats.failed_requests, 0);
    println!("✓ 通过\n");
    
    println!("=== 所有测试通过! ✓ ===");
}