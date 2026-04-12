// AllToolkit - Rust Process Utilities Test Suite
//
// Comprehensive test coverage for process management functionality.
// Run with: rustc --test mod.rs -o process_utils_test && ./process_utils_test

include!("mod.rs");

use std::thread;
use std::time::Duration;

#[cfg(test)]
mod process_config_tests {
    use super::*;

    #[test]
    fn test_config_new() {
        let config = ProcessConfig::new("echo");
        assert_eq!(config.command, "echo");
        assert!(config.args.is_empty());
        assert!(config.env_vars.is_empty());
    }

    #[test]
    fn test_config_args() {
        let config = ProcessConfig::new("ls")
            .args(&["-la", "/tmp"]);
        assert_eq!(config.args, vec!["-la", "/tmp"]);
    }

    #[test]
    fn test_config_env() {
        let config = ProcessConfig::new("env")
            .env("KEY1", "value1")
            .env("KEY2", "value2");
        assert_eq!(config.env_vars.get("KEY1"), Some(&"value1".to_string()));
        assert_eq!(config.env_vars.get("KEY2"), Some(&"value2".to_string()));
    }

    #[test]
    fn test_config_timeout() {
        let config = ProcessConfig::new("sleep").timeout_secs(30);
        assert_eq!(config.timeout, Some(Duration::from_secs(30)));
    }

    #[test]
    fn test_config_default() {
        let config = ProcessConfig::default();
        assert!(config.command.is_empty());
        assert!(config.capture_stdout);
        assert!(config.capture_stderr);
        assert!(!config.stdin_enabled);
    }

    #[test]
    fn test_config_builder_pattern() {
        let config = ProcessConfig::new("python3")
            .args(&["script.py"])
            .env("PYTHONPATH", "/lib")
            .working_dir("/app")
            .timeout_secs(60);

        assert_eq!(config.command, "python3");
        assert_eq!(config.args, vec!["script.py"]);
        assert_eq!(config.env_vars.get("PYTHONPATH"), Some(&"/lib".to_string()));
        assert_eq!(config.timeout, Some(Duration::from_secs(60)));
    }
}

#[cfg(test)]
mod process_output_tests {
    use super::*;

    #[test]
    fn test_output_success() {
        let output = ProcessOutput {
            pid: 1234,
            exit_code: Some(0),
            stdout: String::new(),
            stderr: String::new(),
            duration_ms: 100,
            timed_out: false,
        };
        assert!(output.success());
    }

    #[test]
    fn test_output_failure_nonzero_exit() {
        let output = ProcessOutput {
            pid: 1234,
            exit_code: Some(1),
            stdout: String::new(),
            stderr: String::from("error"),
            duration_ms: 100,
            timed_out: false,
        };
        assert!(!output.success());
    }

    #[test]
    fn test_output_failure_timeout() {
        let output = ProcessOutput {
            pid: 1234,
            exit_code: None,
            stdout: String::new(),
            stderr: String::new(),
            duration_ms: 5000,
            timed_out: true,
        };
        assert!(!output.success());
    }
}

#[cfg(test)]
mod process_error_tests {
    use super::*;

    #[test]
    fn test_error_display_spawn_failed() {
        let err = ProcessError::SpawnFailed("command not found".to_string());
        assert!(err.to_string().contains("Failed to spawn process"));
    }

    #[test]
    fn test_error_display_timeout() {
        let err = ProcessError::Timeout;
        assert!(err.to_string().contains("timed out"));
    }

    #[test]
    fn test_error_display_process_not_found() {
        let err = ProcessError::ProcessNotFound(12345);
        assert!(err.to_string().contains("12345"));
    }

    #[test]
    fn test_error_from_io_error() {
        let io_err = io::Error::new(io::ErrorKind::NotFound, "file not found");
        let proc_err: ProcessError = io_err.into();
        assert!(matches!(proc_err, ProcessError::IoError(_)));
    }
}

#[cfg(test)]
mod process_manager_tests {
    use super::*;

    #[test]
    fn test_manager_new() {
        let manager = ProcessManager::new();
        assert!(manager.list_pids().is_empty());
    }

    #[test]
    fn test_manager_run_echo() {
        let manager = ProcessManager::new();
        let config = ProcessConfig::new("echo").args(&["hello"]);

        let result = manager.run(&config);
        assert!(result.is_ok());

        let output = result.unwrap();
        assert!(output.success());
        assert!(output.stdout.contains("hello"));
    }

    #[test]
    fn test_manager_run_cat() {
        let manager = ProcessManager::new();
        let config = ProcessConfig::new("echo").args(&["test data"]);

        let result = manager.run(&config);
        assert!(result.is_ok());
        assert!(result.unwrap().stdout.contains("test data"));
    }

    #[test]
    fn test_manager_spawn_and_is_running() {
        let manager = ProcessManager::new();
        let config = ProcessConfig::new("sleep").args(&["5"]);

        let pid = manager.spawn(&config);
        assert!(pid.is_ok());

        let pid = pid.unwrap();
        thread::sleep(Duration::from_millis(100));
        assert!(manager.is_running(pid));

        manager.kill(pid).unwrap();
        thread::sleep(Duration::from_millis(100));
        assert!(!manager.is_running(pid));
    }

    #[test]
    fn test_manager_list_pids() {
        let manager = ProcessManager::new();
        assert!(manager.list_pids().is_empty());

        let config = ProcessConfig::new("sleep").args(&["10"]);
        let pid1 = manager.spawn(&config).unwrap();
        let pid2 = manager.spawn(&config).unwrap();

        let pids = manager.list_pids();
        assert!(pids.contains(&pid1));
        assert!(pids.contains(&pid2));

        manager.kill(pid1).unwrap();
        manager.kill(pid2).unwrap();
    }

    #[test]
    fn test_manager_get_output() {
        let manager = ProcessManager::new();
        let config = ProcessConfig::new("echo").args(&["output test"]);

        let result = manager.run(&config);
        let pid = result.as_ref().unwrap().pid;

        let output = manager.get_output(pid);
        assert!(output.is_some());
        assert!(output.unwrap().stdout.contains("output test"));
    }

    #[test]
    fn test_manager_kill_nonexistent() {
        let manager = ProcessManager::new();
        let result = manager.kill(99999999);
        assert!(result.is_err());
        assert!(matches!(result.unwrap_err(), ProcessError::ProcessNotFound(_)));
    }

    #[test]
    fn test_manager_cleanup() {
        let manager = ProcessManager::new();
        let config = ProcessConfig::new("sleep").args(&["1"]);

        let pid = manager.spawn(&config).unwrap();
        thread::sleep(Duration::from_secs(2));

        let finished = manager.cleanup();
        assert!(finished.contains(&pid));
    }
}

#[cfg(test)]
mod run_command_tests {
    use super::*;

    #[test]
    fn test_run_command_success() {
        let result = run_command("echo", &["success"]);
        assert!(result.is_ok());
        assert!(result.unwrap().success());
    }

    #[test]
    fn test_run_command_with_args() {
        let result = run_command("printf", &["hello\\nworld"]);
        assert!(result.is_ok());
        let output = result.unwrap();
        assert!(output.stdout.contains("hello"));
    }

    #[test]
    fn test_run_command_capture_stderr() {
        let result = run_command("ls", &["/nonexistent/path/xyz"]);
        assert!(result.is_ok());
        let output = result.unwrap();
        assert!(!output.success());
        assert!(!output.stderr.is_empty());
    }

    #[test]
    fn test_run_with_timeout_success() {
        let result = run_with_timeout("sleep", &["0.1"], 5);
        assert!(result.is_ok());
        assert!(result.unwrap().success());
    }

    #[test]
    fn test_run_with_timeout_triggered() {
        let result = run_with_timeout("sleep", &["10"], 1);
        assert!(result.is_ok());
        let output = result.unwrap();
        assert!(output.timed_out);
    }
}

#[cfg(test)]
mod process_info_tests {
    use super::*;

    #[test]
    fn test_current_pid_positive() {
        let pid = current_pid();
        assert!(pid > 0);
    }

    #[test]
    fn test_process_exists_current() {
        let pid = current_pid();
        assert!(process_exists(pid));
    }

    #[test]
    fn test_process_exists_invalid() {
        assert!(!process_exists(99999999));
    }

    #[test]
    #[cfg(unix)]
    fn test_get_current_process_info() {
        let info = get_process_info(current_pid());
        assert!(info.is_ok());

        let info = info.unwrap();
        assert_eq!(info.pid, current_pid());
        assert!(!info.name.is_empty());
        assert!(info.memory_bytes > 0);
    }

    #[test]
    #[cfg(unix)]
    fn test_get_process_info_invalid_pid() {
        let result = get_process_info(99999999);
        assert!(result.is_err());
        assert!(matches!(result.unwrap_err(), ProcessError::ProcessNotFound(_)));
    }

    #[test]
    #[cfg(unix)]
    fn test_process_info_fields() {
        let info = get_process_info(current_pid()).unwrap();

        assert!(info.pid > 0);
        assert!(!info.name.is_empty());
        assert!(!info.command.is_empty());
        assert!(!info.status.is_empty());
        assert!(!info.user.is_empty());
        assert!(info.threads >= 1);
    }
}

#[cfg(test)]
mod signal_tests {
    use super::*;

    #[test]
    #[cfg(unix)]
    fn test_kill_process() {
        let manager = ProcessManager::new();
        let config = ProcessConfig::new("sleep").args(&["30"]);
        let pid = manager.spawn(&config).unwrap();

        thread::sleep(Duration::from_millis(100));
        assert!(manager.is_running(pid));

        let result = kill_process(pid);
        assert!(result.is_ok());

        thread::sleep(Duration::from_millis(100));
        assert!(!process_exists(pid));
    }

    #[test]
    #[cfg(unix)]
    fn test_force_kill_process() {
        let manager = ProcessManager::new();
        let config = ProcessConfig::new("sleep").args(&["30"]);
        let pid = manager.spawn(&config).unwrap();

        thread::sleep(Duration::from_millis(100));

        let result = force_kill_process(pid);
        assert!(result.is_ok());

        thread::sleep(Duration::from_millis(100));
        assert!(!process_exists(pid));
    }

    #[test]
    fn test_kill_nonexistent_process() {
        let result = kill_process(99999999);
        assert!(result.is_err());
    }
}

#[cfg(test)]
mod process_tree_tests {
    use super::*;

    #[test]
    #[cfg(unix)]
    fn test_get_child_processes() {
        // This test may return empty if no children exist
        let result = get_child_processes(current_pid());
        assert!(result.is_ok());
        // Just verify it doesn't crash
    }

    #[test]
    #[cfg(unix)]
    fn test_get_process_tree() {
        let result = get_process_tree(current_pid());
        assert!(result.is_ok());
        // Just verify it doesn't crash
    }

    #[test]
    #[cfg(unix)]
    fn test_get_child_processes_invalid() {
        let result = get_child_processes(99999999);
        assert!(result.is_ok());
        assert!(result.unwrap().is_empty());
    }
}

#[cfg(test)]
mod wait_tests {
    use super::*;

    #[test]
    #[cfg(unix)]
    fn test_wait_for_process_timeout() {
        // Create a process that will outlive the wait timeout
        let manager = ProcessManager::new();
        let config = ProcessConfig::new("sleep").args(&["5"]);
        let pid = manager.spawn(&config).unwrap();

        let result = wait_for_process(pid, Duration::from_millis(100));
        assert!(result.is_err());
        assert!(matches!(result.unwrap_err(), ProcessError::Timeout));

        manager.kill(pid).ok();
    }
}

#[cfg(test)]
mod integration_tests {
    use super::*;

    #[test]
    fn test_full_workflow() {
        let manager = ProcessManager::new();

        // Run a simple command
        let config = ProcessConfig::new("echo")
            .args(&["integration", "test"])
            .env("TEST_MODE", "true")
            .timeout_secs(10);

        let result = manager.run(&config);
        assert!(result.is_ok());

        let output = result.unwrap();
        assert!(output.success());
        assert!(output.stdout.contains("integration test"));
        assert!(output.duration_ms > 0);
    }

    #[test]
    fn test_multiple_concurrent_processes() {
        let manager = ProcessManager::new();
        let config = ProcessConfig::new("sleep").args(&["2"]);

        let mut pids = Vec::new();
        for _ in 0..3 {
            let pid = manager.spawn(&config).unwrap();
            pids.push(pid);
        }

        thread::sleep(Duration::from_millis(100));

        for pid in &pids {
            assert!(manager.is_running(*pid));
        }

        for pid in &pids {
            manager.kill(*pid).unwrap();
        }

        thread::sleep(Duration::from_millis(100));

        for pid in &pids {
            assert!(!manager.is_running(*pid));
        }
    }

    #[test]
    fn test_command_with_working_dir() {
        let manager = ProcessManager::new();
        let config = ProcessConfig::new("pwd").working_dir("/tmp");

        let result = manager.run(&config);
        assert!(result.is_ok());
        let output = result.unwrap();
        assert!(output.stdout.contains("tmp"));
    }

    #[test]
    fn test_environment_variables() {
        let manager = ProcessManager::new();
        let config = ProcessConfig::new("sh")
            .args(&["-c", "echo $TEST_VAR"])
            .env("TEST_VAR", "custom_value");

        let result = manager.run(&config);
        assert!(result.is_ok());
        let output = result.unwrap();
        assert!(output.stdout.contains("custom_value"));
    }
}

#[cfg(test)]
mod edge_case_tests {
    use super::*;

    #[test]
    fn test_empty_command() {
        let config = ProcessConfig::new("");
        let manager = ProcessManager::new();
        let result = manager.run(&config);
        assert!(result.is_err());
    }

    #[test]
    fn test_very_short_timeout() {
        let config = ProcessConfig::new("sleep")
            .args(&["1"])
            .timeout_secs(0);

        let manager = ProcessManager::new();
        let result = manager.run(&config);

        // May timeout immediately or complete very quickly
        assert!(result.is_ok());
    }

    #[test]
    fn test_command_not_found() {
        let config = ProcessConfig::new("nonexistent_command_xyz123");
        let manager = ProcessManager::new();
        let result = manager.run(&config);
        assert!(result.is_err());
        assert!(matches!(result.unwrap_err(), ProcessError::SpawnFailed(_)));
    }

    #[test]
    fn test_large_output() {
        let manager = ProcessManager::new();
        let config = ProcessConfig::new("seq")
            .args(&["1", "1000"])
            .timeout_secs(5);

        let result = manager.run(&config);
        assert!(result.is_ok());
        let output = result.unwrap();
        assert!(output.success());
        assert!(output.stdout.contains("500"));
        assert!(output.stdout.contains("1000"));
    }
}

fn main() {
    println!("Running AllToolkit Process Utils Tests...\n");

    // Run all tests
    let tests = vec![
        ("Process Config Tests", vec![
            test_config_new,
            test_config_args,
            test_config_env,
            test_config_timeout,
            test_config_default,
            test_config_builder_pattern,
        ]),
        ("Process Output Tests", vec![
            test_output_success,
            test_output_failure_nonzero_exit,
            test_output_failure_timeout,
        ]),
        ("Process Error Tests", vec![
            test_error_display_spawn_failed,
            test_error_display_timeout,
            test_error_display_process_not_found,
            test_error_from_io_error,
        ]),
        ("Process Manager Tests", vec![
            test_manager_new,
            test_manager_run_echo,
            test_manager_run_cat,
            test_manager_spawn_and_is_running,
            test_manager_list_pids,
            test_manager_get_output,
            test_manager_kill_nonexistent,
            test_manager_cleanup,
        ]),
        ("Run Command Tests", vec![
            test_run_command_success,
            test_run_command_with_args,
            test_run_command_capture_stderr,
            test_run_with_timeout_success,
            test_run_with_timeout_triggered,
        ]),
        ("Process Info Tests", vec![
            test_current_pid_positive,
            test_process_exists_current,
            test_process_exists_invalid,
        ]),
        ("Integration Tests", vec![
            test_full_workflow,
            test_multiple_concurrent_processes,
            test_command_with_working_dir,
            test_environment_variables,
        ]),
        ("Edge Case Tests", vec![
            test_empty_command,
            test_command_not_found,
            test_large_output,
        ]),
    ];

    let mut passed = 0;
    let mut failed = 0;

    for (group_name, group_tests) in tests {
        println!("Running {}...", group_name);
        for test in group_tests {
            let test_name = std::any::type_name_of_val(&test);
            print!("  {} ... ", test_name.split("::").last().unwrap_or("unknown"));
            
            // Run test in a way that catches panics
            let result = std::panic::catch_unwind(std::panic::AssertUnwindSafe(|| test()));
            
            match result {
                Ok(Ok(())) => {
                    println!("ok");
                    passed += 1;
                }
                Ok(Err(e)) => {
                    println!("FAILED - {}", e);
                    failed += 1;
                }
                Err(_) => {
                    println!("FAILED - panicked");
                    failed += 1;
                }
            }
        }
        println!();
    }

    println!("\n========================================");
    println!("Test Results: {} passed, {} failed", passed, failed);
    println!("========================================");

    if failed > 0 {
        std::process::exit(1);
    }
}

// Test function declarations
fn test_config_new() -> Result<(), String> {
    let config = ProcessConfig::new("echo");
    if config.command != "echo" { return Err("command mismatch".into()); }
    Ok(())
}

fn test_config_args() -> Result<(), String> {
    let config = ProcessConfig::new("ls").args(&["-la", "/tmp"]);
    if config.args != vec!["-la", "/tmp"] { return Err("args mismatch".into()); }
    Ok(())
}

fn test_config_env() -> Result<(), String> {
    let config = ProcessConfig::new("env")
        .env("KEY1", "value1")
        .env("KEY2", "value2");
    if config.env_vars.get("KEY1") != Some(&"value1".to_string()) { return Err("env KEY1 mismatch".into()); }
    Ok(())
}

fn test_config_timeout() -> Result<(), String> {
    let config = ProcessConfig::new("sleep").timeout_secs(30);
    if config.timeout != Some(Duration::from_secs(30)) { return Err("timeout mismatch".into()); }
    Ok(())
}

fn test_config_default() -> Result<(), String> {
    let config = ProcessConfig::default();
    if !config.capture_stdout { return Err("capture_stdout should be true".into()); }
    Ok(())
}

fn test_config_builder_pattern() -> Result<(), String> {
    let config = ProcessConfig::new("python3")
        .args(&["script.py"])
        .env("PYTHONPATH", "/lib")
        .working_dir("/app")
        .timeout_secs(60);
    if config.command != "python3" { return Err("command mismatch".into()); }
    Ok(())
}

fn test_output_success() -> Result<(), String> {
    let output = ProcessOutput {
        pid: 1234, exit_code: Some(0), stdout: String::new(),
        stderr: String::new(), duration_ms: 100, timed_out: false,
    };
    if !output.success() { return Err("should be success".into()); }
    Ok(())
}

fn test_output_failure_nonzero_exit() -> Result<(), String> {
    let output = ProcessOutput {
        pid: 1234, exit_code: Some(1), stdout: String::new(),
        stderr: String::from("error"), duration_ms: 100, timed_out: false,
    };
    if output.success() { return Err("should be failure".into()); }
    Ok(())
}

fn test_output_failure_timeout() -> Result<(), String> {
    let output = ProcessOutput {
        pid: 1234, exit_code: None, stdout: String::new(),
        stderr: String::new(), duration_ms: 5000, timed_out: true,
    };
    if output.success() { return Err("should be timeout failure".into()); }
    Ok(())
}

fn test_error_display_spawn_failed() -> Result<(), String> {
    let err = ProcessError::SpawnFailed("command not found".to_string());
    if !err.to_string().contains("Failed to spawn process") { return Err("error message mismatch".into()); }
    Ok(())
}

fn test_error_display_timeout() -> Result<(), String> {
    let err = ProcessError::Timeout;
    if !err.to_string().contains("timed out") { return Err("error message mismatch".into()); }
    Ok(())
}

fn test_error_display_process_not_found() -> Result<(), String> {
    let err = ProcessError::ProcessNotFound(12345);
    if !err.to_string().contains("12345") { return Err("error message mismatch".into()); }
    Ok(())
}

fn test_error_from_io_error() -> Result<(), String> {
    let io_err = io::Error::new(io::ErrorKind::NotFound, "file not found");
    let proc_err: ProcessError = io_err.into();
    if !matches!(proc_err, ProcessError::IoError(_)) { return Err("error conversion mismatch".into()); }
    Ok(())
}

fn test_manager_new() -> Result<(), String> {
    let manager = ProcessManager::new();
    if !manager.list_pids().is_empty() { return Err("should be empty".into()); }
    Ok(())
}

fn test_manager_run_echo() -> Result<(), String> {
    let manager = ProcessManager::new();
    let config = ProcessConfig::new("echo").args(&["hello"]);
    let result = manager.run(&config)?;
    if !result.success() { return Err("should succeed".into()); }
    if !result.stdout.contains("hello") { return Err("output mismatch".into()); }
    Ok(())
}

fn test_manager_run_cat() -> Result<(), String> {
    let manager = ProcessManager::new();
    let config = ProcessConfig::new("echo").args(&["test data"]);
    let result = manager.run(&config)?;
    if !result.stdout.contains("test data") { return Err("output mismatch".into()); }
    Ok(())
}

fn test_manager_spawn_and_is_running() -> Result<(), String> {
    let manager = ProcessManager::new();
    let config = ProcessConfig::new("sleep").args(&["5"]);
    let pid = manager.spawn(&config)?;
    thread::sleep(Duration::from_millis(100));
    if !manager.is_running(pid) { return Err("should be running".into()); }
    manager.kill(pid)?;
    thread::sleep(Duration::from_millis(100));
    if manager.is_running(pid) { return Err("should not be running".into()); }
    Ok(())
}

fn test_manager_list_pids() -> Result<(), String> {
    let manager = ProcessManager::new();
    let config = ProcessConfig::new("sleep").args(&["10"]);
    let pid1 = manager.spawn(&config)?;
    let pid2 = manager.spawn(&config)?;
    let pids = manager.list_pids();
    if !pids.contains(&pid1) || !pids.contains(&pid2) { return Err("pids mismatch".into()); }
    manager.kill(pid1)?;
    manager.kill(pid2)?;
    Ok(())
}

fn test_manager_get_output() -> Result<(), String> {
    let manager = ProcessManager::new();
    let config = ProcessConfig::new("echo").args(&["output test"]);
    let result = manager.run(&config)?;
    let pid = result.pid;
    let output = manager.get_output(pid).ok_or("no output")?;
    if !output.stdout.contains("output test") { return Err("output mismatch".into()); }
    Ok(())
}

fn test_manager_kill_nonexistent() -> Result<(), String> {
    let manager = ProcessManager::new();
    let result = manager.kill(99999999);
    if !result.is_err() { return Err("should fail".into()); }
    Ok(())
}

fn test_manager_cleanup() -> Result<(), String> {
    let manager = ProcessManager::new();
    let config = ProcessConfig::new("sleep").args(&["1"]);
    let pid = manager.spawn(&config)?;
    thread::sleep(Duration::from_secs(2));
    let finished = manager.cleanup();
    if !finished.contains(&pid) { return Err("should contain pid".into()); }
    Ok(())
}

fn test_run_command_success() -> Result<(), String> {
    let result = run_command("echo", &["success"])?;
    if !result.success() { return Err("should succeed".into()); }
    Ok(())
}

fn test_run_command_with_args() -> Result<(), String> {
    let result = run_command("printf", &["hello\\nworld"])?;
    if !result.stdout.contains("hello") { return Err("output mismatch".into()); }
    Ok(())
}

fn test_run_command_capture_stderr() -> Result<(), String> {
    let result = run_command("ls", &["/nonexistent/path/xyz"])?;
    if result.success() { return Err("should fail".into()); }
    if result.stderr.is_empty() { return Err("should have stderr".into()); }
    Ok(())
}

fn test_run_with_timeout_success() -> Result<(), String> {
    let result = run_with_timeout("sleep", &["0.1"], 5)?;
    if !result.success() { return Err("should succeed".into()); }
    Ok(())
}

fn test_run_with_timeout_triggered() -> Result<(), String> {
    let result = run_with_timeout("sleep", &["10"], 1)?;
    if !result.timed_out { return Err("should timeout".into()); }
    Ok(())
}

fn test_current_pid_positive() -> Result<(), String> {
    let pid = current_pid();
    if pid == 0 { return Err("pid should be positive".into()); }
    Ok(())
}

fn test_process_exists_current() -> Result<(), String> {
    let pid = current_pid();
    if !process_exists(pid) { return Err("current process should exist".into()); }
    Ok(())
}

fn test_process_exists_invalid() -> Result<(), String> {
    if process_exists(99999999) { return Err("invalid pid should not exist".into()); }
    Ok(())
}

fn test_full_workflow() -> Result<(), String> {
    let manager = ProcessManager::new();
    let config = ProcessConfig::new("echo")
        .args(&["integration", "test"])
        .env("TEST_MODE", "true")
        .timeout_secs(10);
    let result = manager.run(&config)?;
    if !result.success() { return Err("should succeed".into()); }
    if !result.stdout.contains("integration test") { return Err("output mismatch".into()); }
    Ok(())
}

fn test_multiple_concurrent_processes() -> Result<(), String> {
    let manager = ProcessManager::new();
    let config = ProcessConfig::new("sleep").args(&["2"]);
    let mut pids = Vec::new();
    for _ in 0..3 {
        pids.push(manager.spawn(&config)?);
    }
    thread::sleep(Duration::from_millis(100));
    for pid in &pids {
        if !manager.is_running(*pid) { return Err("should be running".into()); }
    }
    for pid in &pids {
        manager.kill(*pid)?;
    }
    Ok(())
}

fn test_command_with_working_dir() -> Result<(), String> {
    let manager = ProcessManager::new();
    let config = ProcessConfig::new("pwd").working_dir("/tmp");
    let result = manager.run(&config)?;
    if !result.stdout.contains("tmp") { return Err("output mismatch".into()); }
    Ok(())
}

fn test_environment_variables() -> Result<(), String> {
    let manager = ProcessManager::new();
    let config = ProcessConfig::new("sh")
        .args(&["-c", "echo $TEST_VAR"])
        .env("TEST_VAR", "custom_value");
    let result = manager.run(&config)?;
    if !result.stdout.contains("custom_value") { return Err("output mismatch".into()); }
    Ok(())
}

fn test_empty_command() -> Result<(), String> {
    let config = ProcessConfig::new("");
    let manager = ProcessManager::new();
    let result = manager.run(&config);
    if !result.is_err() { return Err("should fail".into()); }
    Ok(())
}

fn test_command_not_found() -> Result<(), String> {
    let config = ProcessConfig::new("nonexistent_command_xyz123");
    let manager = ProcessManager::new();
    let result = manager.run(&config);
    if !result.is_err() { return Err("should fail".into()); }
    Ok(())
}

fn test_large_output() -> Result<(), String> {
    let manager = ProcessManager::new();
    let config = ProcessConfig::new("seq")
        .args(&["1", "1000"])
        .timeout_secs(5);
    let result = manager.run(&config)?;
    if !result.success() { return Err("should succeed".into()); }
    if !result.stdout.contains("500") { return Err("output mismatch".into()); }
    Ok(())
}
