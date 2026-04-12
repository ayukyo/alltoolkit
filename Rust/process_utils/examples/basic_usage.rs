// AllToolkit Process Utils - Basic Usage Example
//
// This example demonstrates the fundamental usage of the process utilities.
// Compile: rustc basic_usage.rs -o basic_usage
// Run: ./basic_usage

// Include the process_utils module
include!("../mod.rs");

fn main() {
    println!("=== AllToolkit Process Utils - Basic Usage ===\n");

    // Example 1: Simple command execution
    println!("1. Running a simple command:");
    println!("   Command: echo 'Hello, World!'");
    
    let result = run_command("echo", &["Hello, World!"]);
    match result {
        Ok(output) => {
            println!("   Exit code: {:?}", output.exit_code);
            println!("   Output: {}", output.stdout.trim());
            println!("   Duration: {}ms\n", output.duration_ms);
        }
        Err(e) => println!("   Error: {}\n", e),
    }

    // Example 2: Command with timeout
    println!("2. Running command with timeout:");
    println!("   Command: sleep 0.5 (timeout: 5s)");
    
    let result = run_with_timeout("sleep", &["0.5"], 5);
    match result {
        Ok(output) => {
            println!("   Success: {}", output.success());
            println!("   Timed out: {}", output.timed_out);
            println!("   Duration: {}ms\n", output.duration_ms);
        }
        Err(e) => println!("   Error: {}\n", e),
    }

    // Example 3: Using ProcessManager for multiple processes
    println!("3. Managing multiple processes:");
    
    let manager = ProcessManager::new();
    
    // Spawn several background processes
    let config = ProcessConfig::new("sleep").args(&["3"]);
    
    let pid1 = manager.spawn(&config).expect("Failed to spawn process 1");
    let pid2 = manager.spawn(&config).expect("Failed to spawn process 2");
    let pid3 = manager.spawn(&config).expect("Failed to spawn process 3");
    
    println!("   Spawned processes: {}, {}, {}", pid1, pid2, pid3);
    println!("   All running: {}, {}, {}", 
             manager.is_running(pid1),
             manager.is_running(pid2),
             manager.is_running(pid3));
    
    // Wait a bit and check again
    thread::sleep(Duration::from_millis(500));
    println!("   After 500ms - Still running: {}, {}, {}", 
             manager.is_running(pid1),
             manager.is_running(pid2),
             manager.is_running(pid3));
    
    // Kill one process
    manager.kill(pid2).expect("Failed to kill process 2");
    println!("   Killed process 2");
    thread::sleep(Duration::from_millis(100));
    println!("   Status: {}, {}, {}\n", 
             manager.is_running(pid1),
             manager.is_running(pid2),
             manager.is_running(pid3));

    // Clean up remaining processes
    manager.kill(pid1).ok();
    manager.kill(pid3).ok();

    // Example 4: Process with environment variables
    println!("4. Running command with environment variables:");
    println!("   Command: env (with custom vars)");
    
    let config = ProcessConfig::new("env")
        .env("APP_NAME", "MyApp")
        .env("APP_VERSION", "1.0.0")
        .env("DEBUG", "true");
    
    let manager = ProcessManager::new();
    match manager.run(&config) {
        Ok(output) => {
            println!("   Output contains custom env vars:");
            for line in output.stdout.lines() {
                if line.starts_with("APP_") || line.starts_with("DEBUG") {
                    println!("     {}", line);
                }
            }
            println!();
        }
        Err(e) => println!("   Error: {}\n", e),
    }

    // Example 5: Get current process info
    println!("5. Getting current process information:");
    
    let pid = current_pid();
    println!("   Current PID: {}", pid);
    
    #[cfg(unix)]
    {
        if let Ok(info) = get_process_info(pid) {
            println!("   Process name: {}", info.name);
            println!("   Status: {}", info.status);
            println!("   Memory: {} KB", info.memory_bytes / 1024);
            println!("   Threads: {}", info.threads);
        }
    }
    #[cfg(not(unix))]
    {
        println!("   Process info only available on Unix systems");
    }
    println!();

    // Example 6: Process tree
    println!("6. Getting child processes:");
    
    #[cfg(unix)]
    {
        match get_child_processes(pid) {
            Ok(children) => {
                if children.is_empty() {
                    println!("   No child processes");
                } else {
                    println!("   Child PIDs: {:?}", children);
                }
            }
            Err(e) => println!("   Error: {}", e),
        }
    }
    #[cfg(not(unix))]
    {
        println!("   Child processes only available on Unix systems");
    }
    println!();

    // Example 7: Command with working directory
    println!("7. Running command with specific working directory:");
    println!("   Command: pwd (in /tmp)");
    
    let config = ProcessConfig::new("pwd").working_dir("/tmp");
    let manager = ProcessManager::new();
    match manager.run(&config) {
        Ok(output) => {
            println!("   Working directory: {}", output.stdout.trim());
        }
        Err(e) => println!("   Error: {}", e),
    }
    println!();

    // Example 8: Capturing stderr
    println!("8. Capturing stderr output:");
    println!("   Command: ls /nonexistent_path");
    
    let result = run_command("ls", &["/nonexistent_path_xyz123"]);
    match result {
        Ok(output) => {
            println!("   Exit code: {:?}", output.exit_code);
            println!("   Stderr: {}", output.stderr.trim());
        }
        Err(e) => println!("   Error: {}", e),
    }
    println!();

    println!("=== Examples Complete ===");
}
