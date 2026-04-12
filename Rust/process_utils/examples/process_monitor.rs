// AllToolkit Process Utils - Process Monitor Example
//
// This example demonstrates process monitoring and management capabilities.
// Compile: rustc process_monitor.rs -o process_monitor
// Run: ./process_monitor

include!("../mod.rs");

/// Simple process monitor that tracks multiple processes
struct Monitor {
    manager: ProcessManager,
    processes: HashMap<u32, ProcessRecord>,
}

struct ProcessRecord {
    name: String,
    started_at: Instant,
    config: ProcessConfig,
}

impl Monitor {
    fn new() -> Self {
        Self {
            manager: ProcessManager::new(),
            processes: HashMap::new(),
        }
    }

    fn spawn(&mut self, name: &str, config: ProcessConfig) -> Result<u32, ProcessError> {
        let pid = self.manager.spawn(&config)?;
        
        self.processes.insert(pid, ProcessRecord {
            name: name.to_string(),
            started_at: Instant::now(),
            config,
        });
        
        Ok(pid)
    }

    fn status(&self) {
        println!("\n=== Process Status ===");
        
        for (pid, record) in &self.processes {
            let running = self.manager.is_running(*pid);
            let elapsed = record.started_at.elapsed();
            
            let status = if running { "Running" } else { "Finished" };
            println!("  [{}] {} (PID: {}) - {} for {:?}", 
                     status, record.name, pid, status, elapsed);
        }
        println!();
    }

    fn cleanup(&mut self) -> Vec<u32> {
        let finished = self.manager.cleanup();
        
        for pid in &finished {
            self.processes.remove(pid);
        }
        
        finished
    }

    fn kill_all(&mut self) {
        let pids: Vec<u32> = self.processes.keys().cloned().collect();
        
        for pid in pids {
            if let Err(e) = self.manager.kill(pid) {
                println!("  Failed to kill PID {}: {}", pid, e);
            } else {
                println!("  Killed PID {}", pid);
            }
        }
        
        self.processes.clear();
    }
}

fn main() {
    println!("=== AllToolkit Process Utils - Process Monitor ===\n");

    let mut monitor = Monitor::new();

    // Spawn several worker processes
    println!("Spawning worker processes...\n");

    // Worker 1: A short task
    let config1 = ProcessConfig::new("sleep").args(&["2"]);
    monitor.spawn("Short Worker", config1).expect("Failed to spawn worker 1");

    // Worker 2: A medium task
    let config2 = ProcessConfig::new("sleep").args(&["5"]);
    monitor.spawn("Medium Worker", config2).expect("Failed to spawn worker 2");

    // Worker 3: A longer task
    let config3 = ProcessConfig::new("sleep").args(&["10"]);
    monitor.spawn("Long Worker", config3).expect("Failed to spawn worker 3");

    // Worker 4: A computation task
    let config4 = ProcessConfig::new("sh")
        .args(&["-c", "for i in $(seq 1 5); do echo \"Iteration $i\"; sleep 1; done"]);
    monitor.spawn("Computation Worker", config4).expect("Failed to spawn worker 4");

    // Initial status
    monitor.status();

    // Monitor loop
    println!("Monitoring processes (checking every second)...\n");
    
    let max_duration = Duration::from_secs(12);
    let start = Instant::now();

    while start.elapsed() < max_duration {
        thread::sleep(Duration::from_secs(1));
        
        // Clean up finished processes
        let finished = monitor.cleanup();
        if !finished.is_empty() {
            println!("  ✓ Finished processes: {:?}", finished);
        }

        // Show status
        monitor.status();

        // Check if all done
        if monitor.processes.is_empty() {
            println!("All processes completed!\n");
            break;
        }
    }

    // If any processes are still running, terminate them
    if !monitor.processes.is_empty() {
        println!("Terminating remaining processes...\n");
        monitor.kill_all();
    }

    // Demonstrate process info
    println!("=== System Process Information ===\n");
    
    let current_pid = current_pid();
    println!("Current process: PID {}", current_pid);
    
    #[cfg(unix)]
    {
        if let Ok(info) = get_process_info(current_pid) {
            println!("  Name: {}", info.name);
            println!("  Status: {}", info.status);
            println!("  Memory: {} KB", info.memory_bytes / 1024);
            println!("  Threads: {}", info.threads);
            println!("  Parent PID: {}", info.ppid);
        }
        
        // Show process tree info
        println!("\nProcess tree:");
        match get_process_tree(current_pid) {
            Ok(tree) => {
                if tree.is_empty() {
                    println!("  No child processes");
                } else {
                    println!("  Child processes: {:?}", tree);
                }
            }
            Err(e) => println!("  Error: {}", e),
        }
    }
    #[cfg(not(unix))]
    {
        println!("Process info only available on Unix systems");
    }

    println!("\n=== Monitor Complete ===");
}
