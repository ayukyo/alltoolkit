// AllToolkit Process Utils - Batch Processor Example
//
// This example demonstrates batch processing with parallel execution.
// Compile: rustc batch_processor.rs -o batch_processor
// Run: ./batch_processor

include!("../mod.rs");

/// Result of a batch job
#[derive(Debug, Clone)]
struct BatchResult {
    id: usize,
    command: String,
    success: bool,
    duration_ms: u64,
    output: String,
}

/// Batch processor for running multiple commands
struct BatchProcessor {
    max_concurrent: usize,
    results: Arc<Mutex<Vec<BatchResult>>>,
}

impl BatchProcessor {
    fn new(max_concurrent: usize) -> Self {
        Self {
            max_concurrent,
            results: Arc::new(Mutex::new(Vec::new())),
        }
    }

    /// Run a batch of commands with limited concurrency
    fn run_batch(&self, jobs: Vec<(usize, String, Vec<String>)>) -> Vec<BatchResult> {
        let mut handles = Vec::new();
        let mut active_count = 0;
        let mut job_iter = jobs.into_iter();

        loop {
            // Start new jobs if we have capacity
            while active_count < self.max_concurrent {
                if let Some((id, cmd, args)) = job_iter.next() {
                    let results = Arc::clone(&self.results);
                    
                    let handle = thread::spawn(move || {
                        let start = Instant::now();
                        
                        let config = ProcessConfig::new(&cmd)
                            .args(&args)
                            .timeout_secs(30);
                        
                        let manager = ProcessManager::new();
                        let result = manager.run(&config);
                        
                        let duration_ms = start.elapsed().as_millis() as u64;
                        
                        let batch_result = match result {
                            Ok(output) => BatchResult {
                                id,
                                command: format!("{} {}", cmd, args.join(" ")),
                                success: output.success(),
                                duration_ms,
                                output: if output.success() { 
                                    output.stdout 
                                } else { 
                                    output.stderr 
                                },
                            },
                            Err(e) => BatchResult {
                                id,
                                command: format!("{} {}", cmd, args.join(" ")),
                                success: false,
                                duration_ms,
                                output: e.to_string(),
                            },
                        };
                        
                        results.lock().unwrap().push(batch_result);
                    });
                    
                    handles.push(handle);
                    active_count += 1;
                } else {
                    break;
                }
            }

            // If no active jobs and no more to start, we're done
            if handles.is_empty() {
                break;
            }

            // Wait for one job to complete
            if let Some(pos) = handles.iter().position(|h| !h.is_finished()) {
                // All still running, wait a bit
                thread::sleep(Duration::from_millis(10));
            } else {
                // At least one finished, collect it
                if let Some(handle) = handles.pop() {
                    handle.join().ok();
                    active_count -= 1;
                }
            }
        }

        // Wait for all remaining handles
        for handle in handles {
            handle.join().ok();
        }

        let mut results = self.results.lock().unwrap();
        results.sort_by_key(|r| r.id);
        results.clone()
    }

    /// Print summary of results
    fn print_summary(&self, results: &[BatchResult]) {
        let total = results.len();
        let success = results.iter().filter(|r| r.success).count();
        let failed = total - success;
        let total_duration: u64 = results.iter().map(|r| r.duration_ms).sum();
        let avg_duration = total_duration / total as u64;

        println!("\n=== Batch Summary ===");
        println!("  Total jobs: {}", total);
        println!("  Successful: {}", success);
        println!("  Failed: {}", failed);
        println!("  Total time: {}ms", total_duration);
        println!("  Avg time: {}ms", avg_duration);
        println!();
    }
}

fn main() {
    println!("=== AllToolkit Process Utils - Batch Processor ===\n");

    let processor = BatchProcessor::new(3); // Max 3 concurrent jobs

    // Define batch jobs
    let jobs = vec![
        (1, "echo".to_string(), vec!["Job 1".to_string()]),
        (2, "echo".to_string(), vec!["Job 2".to_string()]),
        (3, "echo".to_string(), vec!["Job 3".to_string()]),
        (4, "echo".to_string(), vec!["Job 4".to_string()]),
        (5, "echo".to_string(), vec!["Job 5".to_string()]),
        (6, "sleep".to_string(), vec!["0.5".to_string()]),
        (7, "sleep".to_string(), vec!["0.3".to_string()]),
        (8, "date".to_string(), vec!["+%Y-%m-%d %H:%M:%S".to_string()]),
        (9, "uname".to_string(), vec!["-a".to_string()]),
        (10, "pwd".to_string(), vec![]),
    ];

    println!("Running {} batch jobs (max 3 concurrent)...\n", jobs.len());

    let start = Instant::now();
    let results = processor.run_batch(jobs);
    let total_duration = start.elapsed();

    // Print individual results
    println!("=== Job Results ===");
    for result in &results {
        let status = if result.success { "✓" } else { "✗" };
        println!("  {} Job {}: {} ({}ms)", 
                 status, result.id, result.command, result.duration_ms);
    }

    // Print summary
    processor.print_summary(&results);

    println!("Total batch time: {:?}", total_duration);
    println!();

    // Example 2: Processing files in batch
    println!("=== File Processing Example ===\n");

    let processor2 = BatchProcessor::new(2);

    // Simulate processing multiple files
    let file_jobs = vec![
        (1, "wc".to_string(), vec!["-l".to_string(), "/etc/passwd".to_string()]),
        (2, "head".to_string(), vec!["-3".to_string(), "/etc/hosts".to_string()]),
        (3, "cat".to_string(), vec!["/etc/hostname".to_string()]),
    ];

    println!("Processing files...\n");
    let file_results = processor2.run_batch(file_jobs);

    for result in &file_results {
        let status = if result.success { "✓" } else { "✗" };
        println!("  {} {}: {}", status, result.command, result.output.trim());
    }

    processor2.print_summary(&file_results);

    // Example 3: Error handling
    println!("=== Error Handling Example ===\n");

    let processor3 = BatchProcessor::new(2);

    let error_jobs = vec![
        (1, "echo".to_string(), vec!["Valid command".to_string()]),
        (2, "ls".to_string(), vec!["/nonexistent_path_xyz".to_string()]),
        (3, "false".to_string(), vec![]), // Command that always fails
        (4, "echo".to_string(), vec!["Another valid command".to_string()]),
    ];

    println!("Running jobs with some expected failures...\n");
    let error_results = processor3.run_batch(error_jobs);

    for result in &error_results {
        let status = if result.success { "✓" } else { "✗" };
        println!("  {} Job {}: {}", status, result.command, 
                 if result.success { "OK" } else { &result.output[..result.output.len().min(50)] });
    }

    processor3.print_summary(&error_results);

    println!("=== Batch Processor Complete ===");
}
