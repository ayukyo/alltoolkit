//! Circuit Breaker Utils - 熔断器工具库
//! 
//! 提供熔断器模式的实现，用于防止级联故障、实现快速失败和自动恢复。
//! 
//! # 熔断器状态
//! 
//! - **Closed（关闭）**: 正常状态，请求正常执行
//! - **Open（打开）**: 熔断状态，请求直接失败，不执行实际操作
//! - **HalfOpen（半开）**: 恢复探测状态，允许部分请求通过以测试服务是否恢复
//! 
//! # 示例
//! 
//! ```rust
//! use circuit_breaker_utils::{CircuitBreaker, CircuitState};
//! 
//! // 创建熔断器
//! let mut breaker = CircuitBreaker::new(5, 10, 30);
//! 
//! // 执行受保护的函数
//! match breaker.call(|| {
//!     // 模拟可能失败的操作
//!     Ok::<_, String>("success")
//! }) {
//!     Ok(result) => println!("成功: {}", result),
//!     Err(e) => println!("失败: {}", e),
//! }
//! ```

use std::sync::{Arc, Mutex};
use std::time::{Duration, Instant};

/// 熔断器状态
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum CircuitState {
    /// 关闭状态 - 正常执行请求
    Closed,
    /// 打开状态 - 快速失败，不执行请求
    Open,
    /// 半开状态 - 允许探测请求
    HalfOpen,
}

/// 熔断器统计信息
#[derive(Debug, Clone)]
pub struct CircuitStats {
    /// 总请求数
    pub total_requests: u64,
    /// 成功请求数
    pub successful_requests: u64,
    /// 失败请求数
    pub failed_requests: u64,
    /// 连续失败数
    pub consecutive_failures: u64,
    /// 连续成功数
    pub consecutive_successes: u64,
    /// 最后失败时间
    pub last_failure_time: Option<Instant>,
    /// 最后成功时间
    pub last_success_time: Option<Instant>,
    /// 状态转换次数
    pub state_transitions: u64,
}

impl Default for CircuitStats {
    fn default() -> Self {
        Self {
            total_requests: 0,
            successful_requests: 0,
            failed_requests: 0,
            consecutive_failures: 0,
            consecutive_successes: 0,
            last_failure_time: None,
            last_success_time: None,
            state_transitions: 0,
        }
    }
}

/// 熔断器配置
#[derive(Debug, Clone)]
pub struct CircuitConfig {
    /// 触发熔断的连续失败阈值
    pub failure_threshold: u64,
    /// 熔断后重置的连续成功阈值
    pub success_threshold: u64,
    /// 熔断持续时间（秒）
    pub timeout_secs: u64,
    /// 半开状态下允许的探测请求数
    pub half_open_max_calls: u64,
    /// 是否在半开状态失败后立即打开
    pub fail_fast_on_half_open: bool,
}

impl Default for CircuitConfig {
    fn default() -> Self {
        Self {
            failure_threshold: 5,
            success_threshold: 3,
            timeout_secs: 30,
            half_open_max_calls: 1,
            fail_fast_on_half_open: true,
        }
    }
}

/// 熔断器错误类型
#[derive(Debug, Clone)]
pub enum CircuitError<E> {
    /// 熔断器打开，请求被拒绝
    CircuitOpen,
    /// 实际操作失败
    OperationError(E),
}

impl<E: std::fmt::Display> std::fmt::Display for CircuitError<E> {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            CircuitError::CircuitOpen => write!(f, "Circuit breaker is open"),
            CircuitError::OperationError(e) => write!(f, "Operation error: {}", e),
        }
    }
}

impl<E: std::fmt::Debug + std::fmt::Display> std::error::Error for CircuitError<E> {}

/// 熔断器内部状态
struct CircuitInner {
    state: CircuitState,
    config: CircuitConfig,
    stats: CircuitStats,
    opened_at: Option<Instant>,
    half_open_calls: u64,
}

/// 熔断器
#[derive(Clone)]
pub struct CircuitBreaker {
    inner: Arc<Mutex<CircuitInner>>,
}

impl CircuitBreaker {
    /// 创建新的熔断器
    /// 
    /// # 参数
    /// 
    /// - `failure_threshold`: 连续失败多少次后触发熔断
    /// - `success_threshold`: 半开状态下连续成功多少次后关闭熔断器
    /// - `timeout_secs`: 熔断持续时间（秒）
    pub fn new(failure_threshold: u64, success_threshold: u64, timeout_secs: u64) -> Self {
        Self::with_config(CircuitConfig {
            failure_threshold,
            success_threshold,
            timeout_secs,
            ..Default::default()
        })
    }

    /// 使用配置创建熔断器
    pub fn with_config(config: CircuitConfig) -> Self {
        Self {
            inner: Arc::new(Mutex::new(CircuitInner {
                state: CircuitState::Closed,
                config,
                stats: CircuitStats::default(),
                opened_at: None,
                half_open_calls: 0,
            })),
        }
    }

    /// 获取当前状态
    pub fn state(&self) -> CircuitState {
        let mut inner = self.inner.lock().unwrap();
        self.check_state_transition(&mut inner);
        inner.state
    }

    /// 获取统计信息
    pub fn stats(&self) -> CircuitStats {
        let inner = self.inner.lock().unwrap();
        inner.stats.clone()
    }

    /// 检查并更新状态转换
    fn check_state_transition(&self, inner: &mut CircuitInner) {
        if inner.state == CircuitState::Open {
            if let Some(opened_at) = inner.opened_at {
                let elapsed = opened_at.elapsed();
                let timeout = Duration::from_secs(inner.config.timeout_secs);
                if elapsed >= timeout {
                    inner.state = CircuitState::HalfOpen;
                    inner.half_open_calls = 0;
                    inner.stats.state_transitions += 1;
                }
            }
        }
    }

    /// 记录成功
    fn record_success(&self, inner: &mut CircuitInner) {
        inner.stats.total_requests += 1;
        inner.stats.successful_requests += 1;
        inner.stats.consecutive_failures = 0;
        inner.stats.consecutive_successes += 1;
        inner.stats.last_success_time = Some(Instant::now());

        match inner.state {
            CircuitState::HalfOpen => {
                inner.half_open_calls += 1;
                if inner.stats.consecutive_successes >= inner.config.success_threshold {
                    inner.state = CircuitState::Closed;
                    inner.stats.state_transitions += 1;
                }
            }
            CircuitState::Closed => {
                // 已经是关闭状态，无需操作
            }
            CircuitState::Open => {
                // 不应该在 Open 状态下记录成功，但如果发生了，忽略
            }
        }
    }

    /// 记录失败
    fn record_failure(&self, inner: &mut CircuitInner) {
        inner.stats.total_requests += 1;
        inner.stats.failed_requests += 1;
        inner.stats.consecutive_failures += 1;
        inner.stats.consecutive_successes = 0;
        inner.stats.last_failure_time = Some(Instant::now());

        match inner.state {
            CircuitState::Closed => {
                if inner.stats.consecutive_failures >= inner.config.failure_threshold {
                    inner.state = CircuitState::Open;
                    inner.opened_at = Some(Instant::now());
                    inner.stats.state_transitions += 1;
                }
            }
            CircuitState::HalfOpen => {
                if inner.config.fail_fast_on_half_open {
                    inner.state = CircuitState::Open;
                    inner.opened_at = Some(Instant::now());
                    inner.stats.state_transitions += 1;
                } else {
                    inner.half_open_calls += 1;
                    if inner.half_open_calls >= inner.config.half_open_max_calls {
                        inner.state = CircuitState::Open;
                        inner.opened_at = Some(Instant::now());
                        inner.stats.state_transitions += 1;
                    }
                }
            }
            CircuitState::Open => {
                // 已经是打开状态，更新时间戳
                inner.opened_at = Some(Instant::now());
            }
        }
    }

    /// 执行受保护的函数
    /// 
    /// # 返回值
    /// 
    /// - `Ok(T)`: 操作成功
    /// - `Err(CircuitError::CircuitOpen)`: 熔断器打开，请求被拒绝
    /// - `Err(CircuitError::OperationError(E))`: 操作失败
    pub fn call<T, E, F>(&self, f: F) -> Result<T, CircuitError<E>>
    where
        F: FnOnce() -> Result<T, E>,
    {
        let mut inner = self.inner.lock().unwrap();
        self.check_state_transition(&mut inner);

        match inner.state {
            CircuitState::Open => {
                Err(CircuitError::CircuitOpen)
            }
            CircuitState::HalfOpen => {
                // 在半开状态下，限制探测请求数量
                if inner.half_open_calls >= inner.config.half_open_max_calls {
                    drop(inner);
                    return Err(CircuitError::CircuitOpen);
                }
                drop(inner);
                
                match f() {
                    Ok(result) => {
                        let mut inner = self.inner.lock().unwrap();
                        self.record_success(&mut inner);
                        Ok(result)
                    }
                    Err(e) => {
                        let mut inner = self.inner.lock().unwrap();
                        self.record_failure(&mut inner);
                        Err(CircuitError::OperationError(e))
                    }
                }
            }
            CircuitState::Closed => {
                drop(inner);
                
                match f() {
                    Ok(result) => {
                        let mut inner = self.inner.lock().unwrap();
                        self.record_success(&mut inner);
                        Ok(result)
                    }
                    Err(e) => {
                        let mut inner = self.inner.lock().unwrap();
                        self.record_failure(&mut inner);
                        Err(CircuitError::OperationError(e))
                    }
                }
            }
        }
    }

    /// 尝试执行，不阻塞
    /// 
    /// 如果熔断器打开，立即返回 None，不执行函数
    pub fn try_call<T, E, F>(&self, f: F) -> Option<Result<T, E>>
    where
        F: FnOnce() -> Result<T, E>,
    {
        let mut inner = self.inner.lock().unwrap();
        self.check_state_transition(&mut inner);

        match inner.state {
            CircuitState::Open => None,
            CircuitState::HalfOpen => {
                if inner.half_open_calls >= inner.config.half_open_max_calls {
                    return None;
                }
                drop(inner);
                
                let result = f();
                let mut inner = self.inner.lock().unwrap();
                match &result {
                    Ok(_) => self.record_success(&mut inner),
                    Err(_) => self.record_failure(&mut inner),
                }
                Some(result)
            }
            CircuitState::Closed => {
                drop(inner);
                let result = f();
                let mut inner = self.inner.lock().unwrap();
                match &result {
                    Ok(_) => self.record_success(&mut inner),
                    Err(_) => self.record_failure(&mut inner),
                }
                Some(result)
            }
        }
    }

    /// 手动打开熔断器
    pub fn trip(&self) {
        let mut inner = self.inner.lock().unwrap();
        inner.state = CircuitState::Open;
        inner.opened_at = Some(Instant::now());
        inner.stats.state_transitions += 1;
    }

    /// 手动关闭熔断器
    pub fn reset(&self) {
        let mut inner = self.inner.lock().unwrap();
        inner.state = CircuitState::Closed;
        inner.opened_at = None;
        inner.half_open_calls = 0;
        inner.stats.consecutive_failures = 0;
        inner.stats.consecutive_successes = 0;
        inner.stats.state_transitions += 1;
    }

    /// 重置统计信息
    pub fn reset_stats(&self) {
        let mut inner = self.inner.lock().unwrap();
        inner.stats = CircuitStats::default();
    }

    /// 检查是否允许请求
    pub fn is_call_allowed(&self) -> bool {
        let mut inner = self.inner.lock().unwrap();
        self.check_state_transition(&mut inner);
        
        match inner.state {
            CircuitState::Closed => true,
            CircuitState::HalfOpen => {
                inner.half_open_calls < inner.config.half_open_max_calls
            }
            CircuitState::Open => false,
        }
    }

    /// 获取配置
    pub fn config(&self) -> CircuitConfig {
        let inner = self.inner.lock().unwrap();
        inner.config.clone()
    }

    /// 更新配置
    pub fn set_config(&self, config: CircuitConfig) {
        let mut inner = self.inner.lock().unwrap();
        inner.config = config;
    }

    /// 获取失败率（百分比）
    pub fn failure_rate(&self) -> f64 {
        let inner = self.inner.lock().unwrap();
        if inner.stats.total_requests == 0 {
            return 0.0;
        }
        (inner.stats.failed_requests as f64 / inner.stats.total_requests as f64) * 100.0
    }

    /// 获取成功率（百分比）
    pub fn success_rate(&self) -> f64 {
        let inner = self.inner.lock().unwrap();
        if inner.stats.total_requests == 0 {
            return 0.0;
        }
        (inner.stats.successful_requests as f64 / inner.stats.total_requests as f64) * 100.0
    }
}

/// 熔断器构建器
pub struct CircuitBreakerBuilder {
    config: CircuitConfig,
}

impl CircuitBreakerBuilder {
    pub fn new() -> Self {
        Self {
            config: CircuitConfig::default(),
        }
    }

    /// 设置失败阈值
    pub fn failure_threshold(mut self, threshold: u64) -> Self {
        self.config.failure_threshold = threshold;
        self
    }

    /// 设置成功阈值
    pub fn success_threshold(mut self, threshold: u64) -> Self {
        self.config.success_threshold = threshold;
        self
    }

    /// 设置熔断超时时间（秒）
    pub fn timeout_secs(mut self, secs: u64) -> Self {
        self.config.timeout_secs = secs;
        self
    }

    /// 设置半开状态最大探测数
    pub fn half_open_max_calls(mut self, max_calls: u64) -> Self {
        self.config.half_open_max_calls = max_calls;
        self
    }

    /// 设置半开状态失败是否立即打开
    pub fn fail_fast_on_half_open(mut self, fail_fast: bool) -> Self {
        self.config.fail_fast_on_half_open = fail_fast;
        self
    }

    /// 构建熔断器
    pub fn build(self) -> CircuitBreaker {
        CircuitBreaker::with_config(self.config)
    }
}

impl Default for CircuitBreakerBuilder {
    fn default() -> Self {
        Self::new()
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::thread;
    use std::time::Duration;

    #[test]
    fn test_circuit_breaker_closed_state() {
        let breaker = CircuitBreaker::new(5, 3, 30);
        
        // 初始状态应该是关闭的
        assert_eq!(breaker.state(), CircuitState::Closed);
        
        // 执行成功的操作
        for i in 0..10 {
            let result = breaker.call(|| Ok::<_, String>(i));
            assert!(result.is_ok());
        }
        
        // 状态应该保持关闭
        assert_eq!(breaker.state(), CircuitState::Closed);
        
        // 检查统计
        let stats = breaker.stats();
        assert_eq!(stats.successful_requests, 10);
        assert_eq!(stats.failed_requests, 0);
    }

    #[test]
    fn test_circuit_breaker_opens_on_failures() {
        let breaker = CircuitBreaker::new(3, 2, 1);
        
        // 触发熔断
        for _ in 0..3 {
            let _ = breaker.call(|| Err::<(), _>("error".to_string()));
        }
        
        // 状态应该打开
        assert_eq!(breaker.state(), CircuitState::Open);
        
        // 后续请求应该被拒绝
        let result = breaker.call(|| Ok::<(), String>(()));
        assert!(matches!(result, Err(CircuitError::CircuitOpen)));
    }

    #[test]
    fn test_circuit_breaker_half_open_recovery() {
        // 使用构建器设置更大的 half_open_max_calls
        let breaker = CircuitBreakerBuilder::new()
            .failure_threshold(2)
            .success_threshold(2)
            .timeout_secs(1)
            .half_open_max_calls(3)  // 允许3个探测请求
            .build();
        
        // 触发熔断
        for _ in 0..2 {
            let _ = breaker.call(|| Err::<(), _>("error".to_string()));
        }
        assert_eq!(breaker.state(), CircuitState::Open);
        
        // 等待超时
        thread::sleep(Duration::from_millis(1100));
        
        // 状态应该变为半开
        assert_eq!(breaker.state(), CircuitState::HalfOpen);
        
        // 成功的请求应该让熔断器关闭
        for _ in 0..2 {
            let _ = breaker.call(|| Ok::<(), String>(()));
        }
        assert_eq!(breaker.state(), CircuitState::Closed);
    }

    #[test]
    fn test_circuit_breaker_half_open_failure() {
        let breaker = CircuitBreaker::new(2, 2, 1);
        
        // 触发熔断
        for _ in 0..2 {
            let _ = breaker.call(|| Err::<(), _>("error".to_string()));
        }
        assert_eq!(breaker.state(), CircuitState::Open);
        
        // 等待超时
        thread::sleep(Duration::from_millis(1100));
        assert_eq!(breaker.state(), CircuitState::HalfOpen);
        
        // 半开状态下的失败应该立即重新打开
        let _ = breaker.call(|| Err::<(), String>("error".to_string()));
        assert_eq!(breaker.state(), CircuitState::Open);
    }

    #[test]
    fn test_circuit_breaker_manual_control() {
        let breaker = CircuitBreaker::new(10, 5, 30);
        
        // 手动打开
        breaker.trip();
        assert_eq!(breaker.state(), CircuitState::Open);
        
        // 手动关闭
        breaker.reset();
        assert_eq!(breaker.state(), CircuitState::Closed);
    }

    #[test]
    fn test_circuit_breaker_stats() {
        let breaker = CircuitBreaker::new(10, 5, 30);
        
        // 执行一些操作
        for i in 0..10 {
            let _ = breaker.call(|| {
                if i % 3 == 0 {
                    Err::<(), _>("error".to_string())
                } else {
                    Ok(())
                }
            });
        }
        
        let stats = breaker.stats();
        assert_eq!(stats.total_requests, 10);
        // 0, 3, 6, 9 是失败的
        assert_eq!(stats.failed_requests, 4);
        assert_eq!(stats.successful_requests, 6);
    }

    #[test]
    fn test_circuit_breaker_builder() {
        let breaker = CircuitBreakerBuilder::new()
            .failure_threshold(3)
            .success_threshold(2)
            .timeout_secs(10)
            .half_open_max_calls(2)
            .fail_fast_on_half_open(false)
            .build();
        
        let config = breaker.config();
        assert_eq!(config.failure_threshold, 3);
        assert_eq!(config.success_threshold, 2);
        assert_eq!(config.timeout_secs, 10);
        assert_eq!(config.half_open_max_calls, 2);
        assert!(!config.fail_fast_on_half_open);
    }

    #[test]
    fn test_is_call_allowed() {
        let breaker = CircuitBreaker::new(2, 2, 1);
        
        // 初始状态允许调用
        assert!(breaker.is_call_allowed());
        
        // 触发熔断
        for _ in 0..2 {
            let _ = breaker.call(|| Err::<(), _>("error".to_string()));
        }
        
        // 不允许调用
        assert!(!breaker.is_call_allowed());
        
        // 等待超时
        thread::sleep(Duration::from_millis(1100));
        
        // 允许调用（半开状态）
        assert!(breaker.is_call_allowed());
    }

    #[test]
    fn test_failure_and_success_rates() {
        let breaker = CircuitBreaker::new(10, 5, 30);
        
        // 没有请求时
        assert_eq!(breaker.failure_rate(), 0.0);
        assert_eq!(breaker.success_rate(), 0.0);
        
        // 10 个请求，4 个失败
        for i in 0..10 {
            let _ = breaker.call(|| {
                if i < 4 {
                    Err::<(), _>("error".to_string())
                } else {
                    Ok(())
                }
            });
        }
        
        // 失败率 40%，成功率 60%
        assert_eq!(breaker.failure_rate(), 40.0);
        assert_eq!(breaker.success_rate(), 60.0);
    }

    #[test]
    fn test_consecutive_counters() {
        let breaker = CircuitBreaker::new(10, 5, 30);
        
        // 连续成功
        for _ in 0..5 {
            let _ = breaker.call(|| Ok::<(), String>(()));
        }
        let stats = breaker.stats();
        assert_eq!(stats.consecutive_successes, 5);
        assert_eq!(stats.consecutive_failures, 0);
        
        // 连续失败
        for _ in 0..3 {
            let _ = breaker.call(|| Err::<(), _>("error".to_string()));
        }
        let stats = breaker.stats();
        assert_eq!(stats.consecutive_failures, 3);
        assert_eq!(stats.consecutive_successes, 0);
    }

    #[test]
    fn test_try_call() {
        let breaker = CircuitBreaker::new(2, 2, 1);
        
        // 正常情况
        let result = breaker.try_call(|| Ok::<i32, String>(42));
        assert!(result.is_some());
        assert_eq!(result.unwrap(), Ok(42));
        
        // 触发熔断
        for _ in 0..2 {
            let _ = breaker.call(|| Err::<(), _>("error".to_string()));
        }
        
        // 应该返回 None
        let result = breaker.try_call(|| Ok::<i32, String>(42));
        assert!(result.is_none());
    }

    #[test]
    fn test_reset_stats() {
        let breaker = CircuitBreaker::new(10, 5, 30);
        
        // 执行一些操作
        for _ in 0..5 {
            let _ = breaker.call(|| Ok::<(), String>(()));
        }
        for _ in 0..3 {
            let _ = breaker.call(|| Err::<(), _>("error".to_string()));
        }
        
        // 验证统计
        let stats = breaker.stats();
        assert_eq!(stats.total_requests, 8);
        
        // 重置统计
        breaker.reset_stats();
        let stats = breaker.stats();
        assert_eq!(stats.total_requests, 0);
        assert_eq!(stats.successful_requests, 0);
        assert_eq!(stats.failed_requests, 0);
    }
}