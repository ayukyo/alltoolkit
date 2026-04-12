// AllToolkit - Rust Process Utilities
//
// A zero-dependency, production-ready process management utility module.
// Supports process spawning, monitoring, resource tracking, and process tree operations.
//
// Author: AllToolkit
// License: MIT

use std::collections::HashMap;
use std::fs;
use std::io::Read;
use std::path::{Path, PathBuf};
use std::process::{Child, Command, Stdio};
use std::sync::{Arc, Mutex};
use std::thread;
use std::time::{Duration, Instant};

/// Result type for process operations
pub type ProcessResult<T> = Result<T, ProcessError>;

/// Error types for process operations
#[derive(Debug, Clone)]
pub enum ProcessError {
    SpawnFailed(String),
    IoError(String),
    Timeout,
    ProcessNotFound(u32),
    PermissionDenied(String),
    InvalidPid(u32),
    SignalFailed(String),
    ResourceLimit(String),
}

impl std::fmt::Display for ProcessError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            ProcessError::SpawnFailed(msg) => write!(f, "Failed to spawn process: {}", msg),
            ProcessError::IoError(msg) => write!(f, "IO error: {}", msg),
            ProcessError::Timeout => write!(f, "Operation timed out"),
            ProcessError::ProcessNotFound(pid) => write!(f, "Process not found: {}", pid),
            ProcessError::PermissionDenied(msg) => write!(f, "Permission denied: {}", msg),
            ProcessError::InvalidPid(pid) => write!(f, "Invalid PID: {}", pid),
            ProcessError::SignalFailed(msg) => write!(f, "Failed to send signal: {}", msg),
            ProcessError::ResourceLimit(msg) => write!(f, "Resource limit exceeded: {}", msg),
        }
    }
}

impl std::error::Error for ProcessError {}

impl From<std::io::Error> for ProcessError {
    fn from(err: std::io::Error) -> Self {
        ProcessError::IoError(err.to_string())
    }
}

/// Process configuration
#[derive(Debug, Clone)]
pub struct ProcessConfig {
    pub command: String,
    pub args: Vec<String>,
    pub env_vars: HashMap<String, String>,
    pub working_dir: Option<PathBuf>,
    pub capture_stdout: bool,
    pub capture_stderr: bool,
    pub stdin_enabled: bool,
    pub timeout: Option<Duration>,
    pub max_memory_mb: Option<u64>,
    pub cpu_limit: Option<f32>,
    pub user: Option<String>,
    pub group: Option<String>,
}

impl Default for ProcessConfig {
    fn default() -> Self {
        Self {
            command: String::new(),
            args: Vec::new(),
            env_vars: HashMap::new(),
            working_dir: None,
            capture_stdout: true,
            capture_stderr: true,
            stdin_enabled: false,
            timeout: None,
            max_memory_mb: None,
            cpu_limit: None,
            user: None,
            group: None,
        }
    }
}

impl ProcessConfig {
    pub fn new(command: &str) -> Self {
        Self {
            command: command.to_string(),
            ..Default::default()
        }
    }

    pub fn args<S: AsRef<str>>(mut self, args: &[S]) -> Self {
        self.args = args.iter().map(|s| s.as_ref().to_string()).collect();
        self
    }

    pub fn env(mut self, key: &str, value: &str) -> Self {
        self.env_vars.insert(key.to_string(), value.to_string());
        self
    }

    pub fn working_dir<P: AsRef<Path>>(mut self, path: P) -> Self {
        self.working_dir = Some(path.as_ref().to_path_buf());
        self
    }

    pub fn timeout_secs(mut self, secs: u64) -> Self {
        self.timeout = Some(Duration::from_secs(secs));
        self
    }

    pub fn build_command(&self) -> Command {
        let mut cmd = Command::new(&self.command);
        cmd.args(&self.args);

        for (key, value) in &self.env_vars {
            cmd.env(key, value);
        }

        if let Some(ref dir) = self.working_dir {
            cmd.current_dir(dir);
        }

        if self.capture_stdout {
            cmd.stdout(Stdio::piped());
        }
        if self.capture_stderr {
            cmd.stderr(Stdio::piped());
        }
        if self.stdin_enabled {
            cmd.stdin(Stdio::piped());
        }

        cmd
    }
}

/// Process output
#[derive(Debug, Clone)]
pub struct ProcessOutput {
    pub pid: u32,
    pub exit_code: Option<i32>,
    pub stdout: String,
    pub stderr: String,
    pub duration_ms: u64,
    pub timed_out: bool,
}

impl ProcessOutput {
    pub fn success(&self) -> bool {
        self.exit_code == Some(0) && !self.timed_out
    }
}

/// Process information
#[derive(Debug, Clone)]
pub struct ProcessInfo {
    pub pid: u32,
    pub ppid: u32,
    pub name: String,
    pub command: String,
    pub status: String,
    pub cpu_percent: f32,
    pub memory_bytes: u64,
    pub start_time: u64,
    pub user: String,
    pub threads: u32,
}

/// Process manager for spawning and monitoring processes
pub struct ProcessManager {
    children: Arc<Mutex<HashMap<u32, Child>>>,
    outputs: Arc<Mutex<HashMap<u32, ProcessOutput>>>,
}

impl Default for ProcessManager {
    fn default() -> Self {
        Self::new()
    }
}

impl ProcessManager {
    pub fn new() -> Self {
        Self {
            children: Arc::new(Mutex::new(HashMap::new())),
            outputs: Arc::new(Mutex::new(HashMap::new())),
        }
    }

    /// Spawn a new process
    pub fn spawn(&self, config: &ProcessConfig) -> ProcessResult<u32> {
        let child = config
            .build_command()
            .spawn()
            .map_err(|e| ProcessError::SpawnFailed(e.to_string()))?;

        let pid = child.id();

        {
            let mut children = self.children.lock().unwrap();
            children.insert(pid, child);
        }

        Ok(pid)
    }

    /// Spawn and wait for process completion
    pub fn run(&self, config: &ProcessConfig) -> ProcessResult<ProcessOutput> {
        let start = Instant::now();
        
        let mut child = config
            .build_command()
            .spawn()
            .map_err(|e| ProcessError::SpawnFailed(e.to_string()))?;

        let pid = child.id();
        
        // Capture stdout and stderr before waiting
        let capture_stdout = config.capture_stdout;
        let capture_stderr = config.capture_stderr;
        
        let stdout_handle = if capture_stdout {
            child.stdout.take().map(|stdout| {
                thread::spawn(move || {
                    let mut buf = Vec::new();
                    let mut reader = stdout;
                    reader.read_to_end(&mut buf).ok();
                    String::from_utf8_lossy(&buf).to_string()
                })
            })
        } else {
            None
        };

        let stderr_handle = if capture_stderr {
            child.stderr.take().map(|stderr| {
                thread::spawn(move || {
                    let mut buf = Vec::new();
                    let mut reader = stderr;
                    reader.read_to_end(&mut buf).ok();
                    String::from_utf8_lossy(&buf).to_string()
                })
            })
        } else {
            None
        };

        // Wait for process with timeout
        let timed_out;
        let exit_code;

        if let Some(timeout) = config.timeout {
            let start_wait = Instant::now();
            loop {
                if start_wait.elapsed() > timeout {
                    child.kill().ok();
                    timed_out = true;
                    exit_code = None;
                    break;
                }

                match child.try_wait() {
                    Ok(Some(status)) => {
                        exit_code = status.code();
                        timed_out = false;
                        break;
                    }
                    Ok(None) => {
                        thread::sleep(Duration::from_millis(50));
                    }
                    Err(_) => {
                        exit_code = None;
                        timed_out = true;
                        break;
                    }
                }
            }
        } else {
            match child.wait() {
                Ok(status) => {
                    exit_code = status.code();
                    timed_out = false;
                }
                Err(_) => {
                    exit_code = None;
                    timed_out = false;
                }
            }
        }

        let duration_ms = start.elapsed().as_millis() as u64;

        // Collect output
        let stdout = stdout_handle
            .and_then(|h| h.join().ok())
            .unwrap_or_default();

        let stderr = stderr_handle
            .and_then(|h| h.join().ok())
            .unwrap_or_default();

        let output = ProcessOutput {
            pid,
            exit_code,
            stdout,
            stderr,
            duration_ms,
            timed_out,
        };

        {
            let mut outputs = self.outputs.lock().unwrap();
            outputs.insert(pid, output.clone());
        }

        Ok(output)
    }

    /// Kill a process by PID
    pub fn kill(&self, pid: u32) -> ProcessResult<()> {
        let mut children = self.children.lock().unwrap();

        if let Some(mut child) = children.remove(&pid) {
            child.kill().map_err(|e| ProcessError::SignalFailed(e.to_string()))?;
            child.wait().ok();
            Ok(())
        } else {
            Err(ProcessError::ProcessNotFound(pid))
        }
    }

    /// Check if a process is still running
    pub fn is_running(&self, pid: u32) -> bool {
        let mut children = self.children.lock().unwrap();

        if let Some(child) = children.get_mut(&pid) {
            return child.try_wait().map(|s| s.is_none()).unwrap_or(false);
        }

        // Check system-wide using /proc on Unix
        #[cfg(unix)]
        {
            Path::new(&format!("/proc/{}", pid)).exists()
        }
        #[cfg(not(unix))]
        {
            false
        }
    }

    /// Get process output
    pub fn get_output(&self, pid: u32) -> Option<ProcessOutput> {
        let outputs = self.outputs.lock().unwrap();
        outputs.get(&pid).cloned()
    }

    /// Get all managed PIDs
    pub fn list_pids(&self) -> Vec<u32> {
        let children = self.children.lock().unwrap();
        children.keys().cloned().collect()
    }

    /// Clean up finished processes
    pub fn cleanup(&self) -> Vec<u32> {
        let mut children = self.children.lock().unwrap();
        let mut finished = Vec::new();

        children.retain(|pid, child| {
            match child.try_wait() {
                Ok(Some(_)) => {
                    finished.push(*pid);
                    false
                }
                _ => true,
            }
        });

        finished
    }
}

/// Get process information by PID (Unix only)
#[cfg(unix)]
pub fn get_process_info(pid: u32) -> ProcessResult<ProcessInfo> {
    let proc_path = format!("/proc/{}", pid);

    if !Path::new(&proc_path).exists() {
        return Err(ProcessError::ProcessNotFound(pid));
    }

    // Read status
    let status_path = format!("{}/status", proc_path);
    let status_content = fs::read_to_string(&status_path)
        .map_err(|_| ProcessError::ProcessNotFound(pid))?;

    let mut name = String::new();
    let mut ppid: u32 = 0;
    let mut uid: u32 = 0;
    let mut vm_rss: u64 = 0;
    let mut threads: u32 = 1;

    for line in status_content.lines() {
        if let Some((key, value)) = line.split_once(':') {
            let value = value.trim();
            match key {
                "Name" => name = value.to_string(),
                "PPid" => ppid = value.parse().unwrap_or(0),
                "Uid" => {
                    uid = value.split_whitespace().next().unwrap_or("0").parse().unwrap_or(0)
                }
                "VmRSS" => {
                    vm_rss = value
                        .split_whitespace()
                        .next()
                        .unwrap_or("0")
                        .parse::<u64>()
                        .unwrap_or(0)
                        * 1024
                }
                "Threads" => threads = value.parse().unwrap_or(1),
                _ => {}
            }
        }
    }

    // Read command line
    let cmdline_path = format!("{}/cmdline", proc_path);
    let command = fs::read_to_string(&cmdline_path)
        .map(|s| s.replace('\0', " ").trim().to_string())
        .unwrap_or_else(|_| name.clone());

    // Read stat for more info
    let stat_path = format!("{}/stat", proc_path);
    let stat_content = fs::read_to_string(&stat_path).unwrap_or_default();
    let stat_parts: Vec<&str> = stat_content.split_whitespace().collect();

    let state = if stat_parts.len() > 2 {
        match stat_parts[2] {
            "R" => "running",
            "S" => "sleeping",
            "D" => "disk_sleep",
            "Z" => "zombie",
            "T" => "stopped",
            _ => "unknown",
        }
    } else {
        "unknown"
    };

    let start_time = if stat_parts.len() > 21 {
        stat_parts[21].parse().unwrap_or(0)
    } else {
        0
    };

    let user = format!("{}", uid);

    Ok(ProcessInfo {
        pid,
        ppid,
        name,
        command,
        status: state.to_string(),
        cpu_percent: 0.0,
        memory_bytes: vm_rss,
        start_time,
        user,
        threads,
    })
}

#[cfg(not(unix))]
pub fn get_process_info(pid: u32) -> ProcessResult<ProcessInfo> {
    Err(ProcessError::IoError(
        "Process info not implemented for this platform".to_string(),
    ))
}

/// Check if a process exists
#[cfg(unix)]
pub fn process_exists(pid: u32) -> bool {
    Path::new(&format!("/proc/{}", pid)).exists()
}

#[cfg(not(unix))]
pub fn process_exists(pid: u32) -> bool {
    false
}

/// Get current process PID
pub fn current_pid() -> u32 {
    std::process::id()
}

/// Get current process info
pub fn current_process_info() -> ProcessResult<ProcessInfo> {
    get_process_info(current_pid())
}

/// Kill a process by PID (Unix only)
#[cfg(unix)]
pub fn kill_process(pid: u32) -> ProcessResult<()> {
    Command::new("kill")
        .arg("-TERM")
        .arg(pid.to_string())
        .output()
        .map_err(|e| ProcessError::SignalFailed(e.to_string()))?;
    
    Ok(())
}

#[cfg(not(unix))]
pub fn kill_process(pid: u32) -> ProcessResult<()> {
    Err(ProcessError::IoError(
        "Process kill not implemented for this platform".to_string(),
    ))
}

/// Force kill a process by PID (Unix only)
#[cfg(unix)]
pub fn force_kill_process(pid: u32) -> ProcessResult<()> {
    Command::new("kill")
        .arg("-KILL")
        .arg(pid.to_string())
        .output()
        .map_err(|e| ProcessError::SignalFailed(e.to_string()))?;
    
    Ok(())
}

#[cfg(not(unix))]
pub fn force_kill_process(pid: u32) -> ProcessResult<()> {
    Err(ProcessError::IoError(
        "Process force kill not implemented for this platform".to_string(),
    ))
}

/// Get child processes of a given PID (Unix only)
#[cfg(unix)]
pub fn get_child_processes(pid: u32) -> ProcessResult<Vec<u32>> {
    let mut children = Vec::new();

    if let Ok(entries) = fs::read_dir("/proc") {
        for entry in entries.flatten() {
            if let Ok(name) = entry.file_name().into_string() {
                if let Ok(child_pid) = name.parse::<u32>() {
                    if let Ok(info) = get_process_info(child_pid) {
                        if info.ppid == pid {
                            children.push(child_pid);
                        }
                    }
                }
            }
        }
    }

    Ok(children)
}

#[cfg(not(unix))]
pub fn get_child_processes(pid: u32) -> ProcessResult<Vec<u32>> {
    Err(ProcessError::IoError(
        "Child processes not implemented for this platform".to_string(),
    ))
}

/// Get process tree (all descendants)
#[cfg(unix)]
pub fn get_process_tree(pid: u32) -> ProcessResult<Vec<u32>> {
    let mut tree = Vec::new();
    let mut queue = vec![pid];

    while let Some(current) = queue.pop() {
        if let Ok(children) = get_child_processes(current) {
            for child in children {
                tree.push(child);
                queue.push(child);
            }
        }
    }

    Ok(tree)
}

#[cfg(not(unix))]
pub fn get_process_tree(pid: u32) -> ProcessResult<Vec<u32>> {
    Err(ProcessError::IoError(
        "Process tree not implemented for this platform".to_string(),
    ))
}

/// Wait for a process to complete with timeout (Unix only)
#[cfg(unix)]
pub fn wait_for_process(pid: u32, timeout: Duration) -> ProcessResult<Option<i32>> {
    let start = Instant::now();

    loop {
        if !process_exists(pid) {
            return Ok(None);
        }

        if start.elapsed() > timeout {
            return Err(ProcessError::Timeout);
        }

        thread::sleep(Duration::from_millis(100));
    }
}

#[cfg(not(unix))]
pub fn wait_for_process(pid: u32, timeout: Duration) -> ProcessResult<Option<i32>> {
    Err(ProcessError::IoError(
        "Wait for process not implemented for this platform".to_string(),
    ))
}

/// Run a command and capture output (convenience function)
pub fn run_command(cmd: &str, args: &[&str]) -> ProcessResult<ProcessOutput> {
    let config = ProcessConfig::new(cmd).args(args).timeout_secs(60);
    let manager = ProcessManager::new();
    manager.run(&config)
}

/// Run a command with timeout
pub fn run_with_timeout(cmd: &str, args: &[&str], timeout_secs: u64) -> ProcessResult<ProcessOutput> {
    let config = ProcessConfig::new(cmd)
        .args(args)
        .timeout_secs(timeout_secs);
    let manager = ProcessManager::new();
    manager.run(&config)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_process_config_builder() {
        let config = ProcessConfig::new("echo")
            .args(&["hello", "world"])
            .env("TEST_VAR", "test_value")
            .timeout_secs(30);

        assert_eq!(config.command, "echo");
        assert_eq!(config.args, vec!["hello", "world"]);
        assert_eq!(config.env_vars.get("TEST_VAR"), Some(&"test_value".to_string()));
        assert_eq!(config.timeout, Some(Duration::from_secs(30)));
    }

    #[test]
    fn test_run_command_echo() {
        let result = run_command("echo", &["hello"]);
        assert!(result.is_ok());
        let output = result.unwrap();
        assert!(output.success());
        assert!(output.stdout.contains("hello"));
    }

    #[test]
    fn test_run_command_with_timeout() {
        let result = run_with_timeout("sleep", &["0.1"], 5);
        assert!(result.is_ok());
        assert!(result.unwrap().success());
    }

    #[test]
    fn test_process_manager_spawn_and_kill() {
        let manager = ProcessManager::new();
        let config = ProcessConfig::new("sleep").args(&["10"]);

        let pid = manager.spawn(&config);
        assert!(pid.is_ok());

        let pid = pid.unwrap();
        assert!(manager.is_running(pid));

        let kill_result = manager.kill(pid);
        assert!(kill_result.is_ok());

        thread::sleep(Duration::from_millis(100));
        assert!(!manager.is_running(pid));
    }

    #[test]
    fn test_current_pid() {
        let pid = current_pid();
        assert!(pid > 0);
    }

    #[test]
    fn test_process_exists() {
        assert!(process_exists(current_pid()));
        assert!(!process_exists(99999999));
    }

    #[test]
    fn test_process_output() {
        let config = ProcessConfig::new("echo")
            .args(&["test output"])
            .timeout_secs(5);

        let manager = ProcessManager::new();
        let result = manager.run(&config);

        assert!(result.is_ok());
        let output = result.unwrap();
        assert!(output.success());
        assert!(output.stdout.contains("test output"));
    }

    #[test]
    #[cfg(unix)]
    fn test_get_process_info() {
        let info = get_process_info(current_pid());
        assert!(info.is_ok());

        let info = info.unwrap();
        assert_eq!(info.pid, current_pid());
        assert!(!info.name.is_empty());
    }

    #[test]
    fn test_process_config_defaults() {
        let config = ProcessConfig::default();
        assert!(config.args.is_empty());
        assert!(config.env_vars.is_empty());
        assert!(config.working_dir.is_none());
        assert!(config.timeout.is_none());
        assert!(config.capture_stdout);
        assert!(config.capture_stderr);
    }
}
