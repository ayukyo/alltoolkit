const std = @import("std");
const cli = @import("../mod.zig");

pub fn main() !void {
    // This example demonstrates various ways to use the CLI argument parser

    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    defer _ = gpa.deinit();
    const allocator = gpa.allocator();

    // Example 1: Simple flag detection
    try simpleFlagExample(allocator);

    // Example 2: Full CLI parser with options
    try fullParserExample(allocator);

    // Example 3: Quick parsing for simple CLIs
    try quickParseExample(allocator);

    // Example 4: File processing CLI
    try fileProcessingExample(allocator);
}

/// Example 1: Simple flag detection using hasFlag
fn simpleFlagExample(allocator: std.mem.Allocator) !void {
    std.debug.print("\n=== Example 1: Simple Flag Detection ===\n", .{});

    // Simulated command line: myapp -v --output=result.txt input.txt
    const argv = [_][]const u8{ "myapp", "-v", "--output=result.txt", "input.txt" };

    // Check if flags are present
    const verbose = cli.hasFlag(&argv, 'v', "verbose");
    const help = cli.hasFlag(&argv, 'h', "help");

    std.debug.print("Verbose flag: {}\n", .{verbose});
    std.debug.print("Help flag: {}\n", .{help});

    // Count positional arguments
    const positional_count = cli.countPositionalArgs(&argv);
    std.debug.print("Number of positional args: {}\n", .{positional_count});

    // Get positional arguments
    var positional = try cli.getPositionalArgs(allocator, &argv);
    defer {
        for (positional) |arg| allocator.free(arg);
        allocator.free(positional);
    }

    std.debug.print("Positional arguments:\n", .{});
    for (positional, 0..) |arg, i| {
        std.debug.print("  [{}]: {s}\n", .{ i, arg });
    }
}

/// Example 2: Full CLI parser with all features
fn fullParserExample(allocator: std.mem.Allocator) !void {
    std.debug.print("\n=== Example 2: Full CLI Parser ===\n", .{});

    var parser = cli.CliParser.init(allocator);
    defer parser.deinit();

    // Configure the parser
    _ = parser.setProgramName("myapp");
    _ = parser.setDescription("A powerful CLI application for file processing");

    // Add flags (boolean options)
    _ = try parser.addFlag("verbose", 'v', "verbose", "Enable verbose output");
    _ = try parser.addFlag("force", 'f', "force", "Force overwrite existing files");
    _ = try parser.addFlag("dry-run", null, "dry-run", "Show what would be done without making changes");
    _ = try parser.addFlag("help", 'h', "help", "Show this help message");

    // Add options (with values)
    _ = try parser.addOption("output", 'o', "output", "Output directory", false, "./output");
    _ = try parser.addOption("format", 'F', "format", "Output format (json, csv, xml)", false, "json");
    _ = try parser.addOption("threads", 'j', "threads", "Number of threads to use", false, "4");
    _ = try parser.addOption("config", 'c', "config", "Configuration file", false, null);
    _ = try parser.addOption("input", 'i', "input", "Input file (required)", true, null);

    // Simulated command line
    const argv = [_][]const u8{
        "myapp",
        "-v",
        "--format=csv",
        "-j", "8",
        "-i", "data.txt",
        "extra1.txt",
        "extra2.txt",
    };

    // Parse arguments
    var result = try parser.parseFromSlice(&argv);
    defer result.deinit();

    // Generate and display help
    std.debug.print("\nHelp Text:\n", .{});
    std.debug.print("----------\n", .{});
    var help_buffer = std.ArrayList(u8).init(allocator);
    defer help_buffer.deinit();
    try parser.generateHelp(help_buffer.writer());
    std.debug.print("{s}\n", .{help_buffer.items});

    // Check parsed values
    std.debug.print("\nParsed Results:\n", .{});
    std.debug.print("----------------\n", .{});

    std.debug.print("Verbose: {}\n", .{result.isPresent("verbose")});
    std.debug.print("Force: {}\n", .{result.isPresent("force")});
    std.debug.print("Dry-run: {}\n", .{result.isPresent("dry-run")});
    std.debug.print("Format: {s}\n", .{result.getValue("format") orelse "not set"});
    std.debug.print("Threads: {s}\n", .{result.getValue("threads") orelse "not set"});
    std.debug.print("Output: {s}\n", .{result.getValue("output") orelse "not set"});
    std.debug.print("Input: {s}\n", .{result.getValue("input") orelse "not set"});

    std.debug.print("\nPositional arguments:\n", .{});
    for (result.positional.items, 0..) |arg, i| {
        std.debug.print("  [{}]: {s}\n", .{ i, arg });
    }
}

/// Example 3: Quick parsing for simple CLIs
fn quickParseExample(allocator: std.mem.Allocator) !void {
    std.debug.print("\n=== Example 3: Quick Parse ===\n", .{});

    // Simulated command line: myapp --name=Alice --verbose --count=42 file.txt
    const argv = [_][]const u8{ "myapp", "--name=Alice", "--verbose", "--count=42", "file.txt" };

    // Quick parse returns a simple map
    var result = try cli.parseSimple(allocator, &argv);
    defer {
        var iter = result.iterator();
        while (iter.next()) |entry| {
            if (entry.value_ptr.*) |v| allocator.free(v);
            allocator.free(entry.key_ptr.*);
        }
        result.deinit();
    }

    std.debug.print("Parsed key-value pairs:\n", .{});
    var iter = result.iterator();
    while (iter.next()) |entry| {
        if (entry.value_ptr.*) |v| {
            std.debug.print("  {s} = {s}\n", .{ entry.key_ptr.*, v });
        } else {
            std.debug.print("  {s} = (flag)\n", .{entry.key_ptr.*});
        }
    }
}

/// Example 4: Real-world file processing CLI
fn fileProcessingExample(allocator: std.mem.Allocator) !void {
    std.debug.print("\n=== Example 4: File Processing CLI ===\n", .{});

    var parser = cli.CliParser.init(allocator);
    defer parser.deinit();

    _ = parser.setProgramName("fileproc");
    _ = parser.setDescription("Process and transform files");

    // Boolean flags
    _ = try parser.addFlag("verbose", 'v', "verbose", "Enable verbose output");
    _ = try parser.addFlag("quiet", 'q', "quiet", "Suppress all output");
    _ = try parser.addFlag("recursive", 'r', "recursive", "Process directories recursively");
    _ = try parser.addFlag("backup", 'b', "backup", "Create backup before processing");
    _ = try parser.addFlag("help", 'h', "help", "Show help");

    // Options with values
    _ = try parser.addOption("output", 'o', "output", "Output directory", false, ".");
    _ = try parser.addOption("suffix", 's', "suffix", "File suffix to process", false, ".txt");
    _ = try parser.addOption("encoding", 'e', "encoding", "File encoding", false, "utf-8");
    _ = try parser.addOption("max-size", 'm', "max-size", "Maximum file size (MB)", false, "100");

    // Simulated complex command line
    const argv = [_][]const u8{
        "fileproc",
        "-vrb",
        "--output=./processed",
        "--suffix=.log",
        "file1.txt",
        "file2.txt",
        "file3.txt",
    };

    var result = try parser.parseFromSlice(&argv);
    defer result.deinit();

    std.debug.print("Configuration:\n", .{});
    std.debug.print("  Verbose: {}\n", .{result.isPresent("verbose")});
    std.debug.print("  Quiet: {}\n", .{result.isPresent("quiet")});
    std.debug.print("  Recursive: {}\n", .{result.isPresent("recursive")});
    std.debug.print("  Backup: {}\n", .{result.isPresent("backup")});
    std.debug.print("  Output directory: {s}\n", .{result.getValue("output") orelse "."});
    std.debug.print("  File suffix: {s}\n", .{result.getValue("suffix") orelse ".txt"});
    std.debug.print("  Encoding: {s}\n", .{result.getValue("encoding") orelse "utf-8"});
    std.debug.print("  Max size: {s} MB\n", .{result.getValue("max-size") orelse "100"});

    std.debug.print("\nFiles to process ({}):\n", .{result.positional.items.len});
    for (result.positional.items, 0..) |file, i| {
        std.debug.print("  {}. {s}\n", .{ i + 1, file });
    }

    // Show how to access values in real application
    std.debug.print("\n--- Real application logic would go here ---\n", .{});
    std.debug.print("Processing files with encoding={s}...\n", .{result.getValue("encoding") orelse "utf-8"});

    if (result.isPresent("backup")) {
        std.debug.print("Creating backups...\n", .{});
    }

    for (result.positional.items) |file| {
        if (result.isPresent("verbose")) {
            std.debug.print("Processing: {s}\n", .{file});
        }
        // Actual file processing would happen here
    }

    std.debug.print("Done!\n", .{});
}

// Run this example with:
// zig run examples/usage_examples.zig