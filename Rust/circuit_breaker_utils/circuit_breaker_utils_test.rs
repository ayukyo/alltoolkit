//! 熔断器工具库测试
//!
//! 测试熔断器的各种场景和状态转换

use std::thread;
use std::time::Duration;

// 引入模块
mod mod;
use mod::{CircuitBreaker, CircuitBreakerBuilder, CircuitState, CircuitError, CircuitConfig};

#[test]
fn test_initial_state_is_closed() {
    let breaker = CircuitBreaker::new(5, 3, 30);
    assert_eq!(breaker.state(), CircuitState::Closed);
}

#[test]
fn test_successful_calls_keep_circuit_closed() {
    let breaker = CircuitBreaker::new(3, 2, 10);
    
    for i in 0..10 {
        let result = breaker.call(|| Ok::<_, String>(format!("success {}", i)));
        assert!(result.is_ok());
        assert_eq!(breaker.state(), CircuitState::Closed);
    }
}

#[test]
fn test_circuit_opens_after_failure_threshold() {
    let breaker = CircuitBreaker::new(3, 2, 10);
    
    // 3次失败应该触发熔断
    for i in 0..3 {
        let result = breaker.call(|| Err::<(), _>(format!("error {}", i)));
        assert!(matches!(result, Err(CircuitError::OperationError(_))));
    }
    
    assert_eq!(breaker.state(), CircuitState::Open);
}

#[test]
fn test_open_circuit_rejects_calls_immediately() {
    let breaker = CircuitBreaker::new(2, 2, 10);
    
    // 触发熔断
    for _ in 0..2 {
        let _ = breaker.call(|| Err::<(), _>("error"));
    }
    assert_eq!(breaker.state(), CircuitState::Open);
    
    // 后续调用应该被立即拒绝
    let result = breaker.call(|| {
        panic!("This should not be called!");
        Ok::<(), String>(())
    });
    
    assert!(matches!(result, Err(CircuitError::CircuitOpen)));
}

#[test]
fn test_circuit_transitions_to_half_open_after_timeout() {
    let breaker = CircuitBreaker::new(2, 2, 1);
    
    // 触发熔断
    for _ in 0..2 {
        let _ = breaker.call(|| Err::<(), _>("error"));
    }
    assert_eq!(breaker.state(), CircuitState::Open);
    
    // 等待超时
    thread::sleep(Duration::from_millis(1100));
    
    // 应该变为半开状态
    assert_eq!(breaker.state(), CircuitState::HalfOpen);
}

#[test]
fn test_half_open_to_closed_on_successes() {
    // 使用构建器设置更大的 half_open_max_calls
    let breaker = CircuitBreakerBuilder::new()
        .failure_threshold(2)
        .success_threshold(3)
        .timeout_secs(1)
        .half_open_max_calls(5)  // 允许5个探测请求
        .build();
    
    // 触发熔断
    for _ in 0..2 {
        let _ = breaker.call(|| Err::<(), _>("error"));
    }
    assert_eq!(breaker.state(), CircuitState::Open);
    
    // 等待超时
    thread::sleep(Duration::from_millis(1100));
    assert_eq!(breaker.state(), CircuitState::HalfOpen);
    
    // 连续成功达到阈值
    for _ in 0..3 {
        let result = breaker.call(|| Ok::<(), String>(()));
        assert!(result.is_ok());
    }
    
    // 应该回到关闭状态
    assert_eq!(breaker.state(), CircuitState::Closed);
}

#[test]
fn test_half_open_back_to_open_on_failure() {
    let breaker = CircuitBreaker::new(2, 2, 1);
    
    // 触发熔断
    for _ in 0..2 {
        let _ = breaker.call(|| Err::<(), _>("error"));
    }
    assert_eq!(breaker.state(), CircuitState::Open);
    
    // 等待超时
    thread::sleep(Duration::from_millis(1100));
    assert_eq!(breaker.state(), CircuitState::HalfOpen);
    
    // 半开状态下的失败应该重新打开熔断器
    let _ = breaker.call(|| Err::<(), String>("error"));
    assert_eq!(breaker.state(), CircuitState::Open);
}

#[test]
fn test_manual_trip_and_reset() {
    let breaker = CircuitBreaker::new(10, 5, 30);
    
    // 手动打开
    breaker.trip();
    assert_eq!(breaker.state(), CircuitState::Open);
    
    // 应该拒绝请求
    let result = breaker.call(|| Ok::<(), String>(()));
    assert!(matches!(result, Err(CircuitError::CircuitOpen)));
    
    // 手动关闭
    breaker.reset();
    assert_eq!(breaker.state(), CircuitState::Closed);
    
    // 应该允许请求
    let result = breaker.call(|| Ok::<(), String>(()));
    assert!(result.is_ok());
}

#[test]
fn test_stats_tracking() {
    let breaker = CircuitBreaker::new(10, 5, 30);
    
    // 10个成功，5个失败
    for i in 0..15 {
        let _ = breaker.call(|| {
            if i < 10 {
                Ok::<(), String>(())
            } else {
                Err("error".to_string())
            }
        });
    }
    
    let stats = breaker.stats();
    assert_eq!(stats.total_requests, 15);
    assert_eq!(stats.successful_requests, 10);
    assert_eq!(stats.failed_requests, 5);
}

#[test]
fn test_failure_and_success_rates() {
    let breaker = CircuitBreaker::new(10, 5, 30);
    
    // 初始应该为0
    assert_eq!(breaker.failure_rate(), 0.0);
    assert_eq!(breaker.success_rate(), 0.0);
    
    // 4个失败，6个成功
    for i in 0..10 {
        let _ = breaker.call(|| {
            if i < 4 {
                Err::<(), String>("error".to_string())
            } else {
                Ok(())
            }
        });
    }
    
    // 失败率40%，成功率60%
    assert_eq!(breaker.failure_rate(), 40.0);
    assert_eq!(breaker.success_rate(), 60.0);
}

#[test]
fn test_consecutive_failure_counting() {
    let breaker = CircuitBreaker::new(10, 5, 30);
    
    // 交替成功和失败
    for i in 0..10 {
        let _ = breaker.call(|| {
            if i % 2 == 0 {
                Err::<(), String>("error".to_string())
            } else {
                Ok(())
            }
        });
    }
    
    let stats = breaker.stats();
    // 最后一次是失败的（索引9是奇数，所以是成功）
    // 等等，让我重新计算：
    // i=0 失败, i=1 成功, i=2 失败, i=3 成功...
    // 最后一次 i=9 是成功
    assert_eq!(stats.consecutive_failures, 0);
    assert_eq!(stats.consecutive_successes, 1);
}

#[test]
fn test_builder_pattern() {
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
    assert_eq!(config.half_open_max_calls, 3);
    assert!(!config.fail_fast_on_half_open);
}

#[test]
fn test_is_call_allowed() {
    let breaker = CircuitBreaker::new(2, 2, 1);
    
    // 初始允许
    assert!(breaker.is_call_allowed());
    
    // 触发熔断
    for _ in 0..2 {
        let _ = breaker.call(|| Err::<(), _>("error"));
    }
    
    // 不允许
    assert!(!breaker.is_call_allowed());
    
    // 等待超时
    thread::sleep(Duration::from_millis(1100));
    
    // 半开状态允许
    assert!(breaker.is_call_allowed());
}

#[test]
fn test_try_call_returns_none_when_open() {
    let breaker = CircuitBreaker::new(2, 2, 10);
    
    // 正常情况
    let result = breaker.try_call(|| Ok::<i32, String>(42));
    assert!(result.is_some());
    
    // 触发熔断
    for _ in 0..2 {
        let _ = breaker.call(|| Err::<(), _>("error"));
    }
    
    // 应该返回 None
    let result = breaker.try_call(|| {
        panic!("Should not be called");
        Ok::<i32, String>(42)
    });
    assert!(result.is_none());
}

#[test]
fn test_reset_stats() {
    let breaker = CircuitBreaker::new(10, 5, 30);
    
    // 执行一些操作
    for _ in 0..10 {
        let _ = breaker.call(|| Ok::<(), String>(()));
    }
    
    assert_eq!(breaker.stats().total_requests, 10);
    
    // 重置
    breaker.reset_stats();
    let stats = breaker.stats();
    assert_eq!(stats.total_requests, 0);
    assert_eq!(stats.successful_requests, 0);
    assert_eq!(stats.failed_requests, 0);
}

#[test]
fn test_state_transitions_count() {
    let breaker = CircuitBreaker::new(2, 2, 1);
    
    // 初始为0
    assert_eq!(breaker.stats().state_transitions, 0);
    
    // 触发熔断 (Closed -> Open)
    for _ in 0..2 {
        let _ = breaker.call(|| Err::<(), _>("error"));
    }
    assert_eq!(breaker.stats().state_transitions, 1);
    
    // 等待超时 (Open -> HalfOpen)
    thread::sleep(Duration::from_millis(1100));
    assert_eq!(breaker.state(), CircuitState::HalfOpen);
    assert_eq!(breaker.stats().state_transitions, 2);
    
    // 成功恢复 (HalfOpen -> Closed)
    for _ in 0..2 {
        let _ = breaker.call(|| Ok::<(), String>(()));
    }
    assert_eq!(breaker.stats().state_transitions, 3);
}

#[test]
fn test_different_error_types() {
    let breaker = CircuitBreaker::new(3, 2, 10);
    
    // 使用 i32 作为错误类型
    let result = breaker.call(|| Err::<(), i32>(404));
    assert!(matches!(result, Err(CircuitError::OperationError(404))));
    
    // 使用自定义错误类型
    #[derive(Debug)]
    enum MyError {
        NetworkError,
        TimeoutError,
    }
    
    impl std::fmt::Display for MyError {
        fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
            match self {
                MyError::NetworkError => write!(f, "Network error"),
                MyError::TimeoutError => write!(f, "Timeout error"),
            }
        }
    }
    
    let result = breaker.call(|| Err::<(), MyError>(MyError::NetworkError));
    assert!(matches!(result, Err(CircuitError::OperationError(MyError::NetworkError))));
}

#[test]
fn test_concurrent_access() {
    use std::sync::Arc;
    use std::thread as std_thread;
    
    let breaker = Arc::new(CircuitBreaker::new(100, 50, 10));
    let mut handles = vec![];
    
    // 多个线程并发访问
    for _ in 0..10 {
        let breaker = Arc::clone(&breaker);
        handles.push(std_thread::spawn(move || {
            for i in 0..100 {
                let result = breaker.call(|| {
                    if i % 10 == 0 {
                        Err::<(), String>("error".to_string())
                    } else {
                        Ok(())
                    }
                });
                let _ = result;
            }
        }));
    }
    
    for handle in handles {
        handle.join().unwrap();
    }
    
    // 应该有1000个请求
    assert_eq!(breaker.stats().total_requests, 1000);
}

#[test]
fn test_config_update() {
    let breaker = CircuitBreaker::new(5, 3, 30);
    
    // 更新配置
    breaker.set_config(CircuitConfig {
        failure_threshold: 10,
        success_threshold: 5,
        timeout_secs: 60,
        half_open_max_calls: 2,
        fail_fast_on_half_open: true,
    });
    
    let config = breaker.config();
    assert_eq!(config.failure_threshold, 10);
    assert_eq!(config.success_threshold, 5);
    assert_eq!(config.timeout_secs, 60);
}

#[test]
fn test_last_failure_and_success_times() {
    let breaker = CircuitBreaker::new(10, 5, 30);
    
    // 初始应该为 None
    assert!(breaker.stats().last_success_time.is_none());
    assert!(breaker.stats().last_failure_time.is_none());
    
    // 执行成功
    let _ = breaker.call(|| Ok::<(), String>(()));
    assert!(breaker.stats().last_success_time.is_some());
    
    // 执行失败
    let _ = breaker.call(|| Err::<(), String>("error".to_string()));
    assert!(breaker.stats().last_failure_time.is_some());
}

fn main() {
    println!("运行熔断器工具库测试...");
    
    // 运行所有测试
    test_initial_state_is_closed();
    println!("✓ 初始状态测试通过");
    
    test_successful_calls_keep_circuit_closed();
    println!("✓ 成功调用保持关闭状态测试通过");
    
    test_circuit_opens_after_failure_threshold();
    println!("✓ 失败阈值触发熔断测试通过");
    
    test_open_circuit_rejects_calls_immediately();
    println!("✓ 熔断状态立即拒绝请求测试通过");
    
    test_circuit_transitions_to_half_open_after_timeout();
    println!("✓ 超时后转为半开状态测试通过");
    
    test_half_open_to_closed_on_successes();
    println!("✓ 半开状态成功恢复测试通过");
    
    test_half_open_back_to_open_on_failure();
    println!("✓ 半开状态失败重新熔断测试通过");
    
    test_manual_trip_and_reset();
    println!("✓ 手动控制测试通过");
    
    test_stats_tracking();
    println!("✓ 统计跟踪测试通过");
    
    test_failure_and_success_rates();
    println!("✓ 失败率和成功率计算测试通过");
    
    test_builder_pattern();
    println!("✓ 构建器模式测试通过");
    
    test_is_call_allowed();
    println!("✓ is_call_allowed 测试通过");
    
    test_try_call_returns_none_when_open();
    println!("✓ try_call 测试通过");
    
    test_reset_stats();
    println!("✓ 重置统计测试通过");
    
    test_state_transitions_count();
    println!("✓ 状态转换计数测试通过");
    
    test_concurrent_access();
    println!("✓ 并发访问测试通过");
    
    test_last_failure_and_success_times();
    println!("✓ 最后失败/成功时间测试通过");
    
    println!("\n所有测试通过! ✓");
}