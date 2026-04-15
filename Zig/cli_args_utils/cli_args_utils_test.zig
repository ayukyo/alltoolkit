const std = @import("std");
const cli = @import("mod.zig");

test "CliParser - basic flag parsing" {
    const allocator = std.testing.allocator;

    var parser = cli.CliParser.init(allocator);
    defer parser.deinit();

    _ = try parser.addFlag("verbose", 'v', "verbose", "Enable verbose output");
    _ = try parser.addFlag("help", 'h', "help", "Show help");

    const argv = [_][]const u8{ "myprogram", "-v", "--help" };

    var result = try parser.parseFromSlice(&argv);
    defer result.deinit();

    try std.testing.expect(result.isPresent("verbose"));
    try std.testing.expect(result.isPresent("help"));
    try std.testing.expect(!result.isPresent("unknown"));
}

test "CliParser - short flags combined" {
    const allocator = std.testing.allocator;

    var parser = cli.CliParser.init(allocator);
    defer parser.deinit();

    _ = try parser.addFlag("verbose", 'v', "verbose", "Enable verbose output");
    _ = try parser.addFlag("all", 'a', "all", "Process all files");
    _ = try parser.addFlag("force", 'f', "force", "Force operation");

    const argv = [_][]const u8{ "myprogram", "-vaf" };

    var result = try parser.parseFromSlice(&argv);
    defer result.deinit();

    try std.testing.expect(result.isPresent("verbose"));
    try std.testing.expect(result.isPresent("all"));
    try std.testing.expect(result.isPresent("force"));
}

test "CliParser - option with value via space" {
    const allocator = std.testing.allocator;

    var parser = cli.CliParser.init(allocator);
    defer parser.deinit();

    _ = try parser.addOption("file", 'f', "file", "Input file", false, null);
    _ = try parser.addOption("output", 'o', "output", "Output file", false, "out.txt");

    const argv = [_][]const u8{ "myprogram", "-f", "input.txt", "--output", "result.txt" };

    var result = try parser.parseFromSlice(&argv);
    defer result.deinit();

    try std.testing.expect(result.isPresent("file"));
    try std.testing.expectEqualStrings("input.txt", result.getValue("file").?);

    try std.testing.expect(result.isPresent("output"));
    try std.testing.expectEqualStrings("result.txt", result.getValue("output").?);
}

test "CliParser - option with equals syntax" {
    const allocator = std.testing.allocator;

    var parser = cli.CliParser.init(allocator);
    defer parser.deinit();

    _ = try parser.addOption("name", 'n', "name", "Name value", false, null);
    _ = try parser.addOption("count", 'c', "count", "Count value", false, "1");

    const argv = [_][]const u8{ "myprogram", "--name=John", "--count=42" };

    var result = try parser.parseFromSlice(&argv);
    defer result.deinit();

    try std.testing.expect(result.isPresent("name"));
    try std.testing.expectEqualStrings("John", result.getValue("name").?);

    try std.testing.expect(result.isPresent("count"));
    try std.testing.expectEqualStrings("42", result.getValue("count").?);
}

test "CliParser - short option with attached value" {
    const allocator = std.testing.allocator;

    var parser = cli.CliParser.init(allocator);
    defer parser.deinit();

    _ = try parser.addOption("file", 'f', "file", "Input file", false, null);

    const argv = [_][]const u8{ "myprogram", "-finput.txt" };

    var result = try parser.parseFromSlice(&argv);
    defer result.deinit();

    try std.testing.expect(result.isPresent("file"));
    try std.testing.expectEqualStrings("input.txt", result.getValue("file").?);
}

test "CliParser - positional arguments" {
    const allocator = std.testing.allocator;

    var parser = cli.CliParser.init(allocator);
    defer parser.deinit();

    _ = try parser.addFlag("verbose", 'v', "verbose", "Enable verbose");

    const argv = [_][]const u8{ "myprogram", "-v", "file1.txt", "file2.txt", "file3.txt" };

    var result = try parser.parseFromSlice(&argv);
    defer result.deinit();

    try std.testing.expectEqual(@as(usize, 3), result.positional.items.len);
    try std.testing.expectEqualStrings("file1.txt", result.getPositional(0).?);
    try std.testing.expectEqualStrings("file2.txt", result.getPositional(1).?);
    try std.testing.expectEqualStrings("file3.txt", result.getPositional(2).?);
    try std.testing.expect(result.getPositional(3) == null);
}

test "CliParser - mixed options and positionals" {
    const allocator = std.testing.allocator;

    var parser = cli.CliParser.init(allocator);
    defer parser.deinit();

    _ = try parser.addOption("output", 'o', "output", "Output file", false, null);
    _ = try parser.addFlag("verbose", 'v', "verbose", "Verbose mode");

    const argv = [_][]const u8{ "myprogram", "input1.txt", "-v", "input2.txt", "-o", "out.txt", "input3.txt" };

    var result = try parser.parseFromSlice(&argv);
    defer result.deinit();

    try std.testing.expect(result.isPresent("verbose"));
    try std.testing.expectEqualStrings("out.txt", result.getValue("output").?);
    try std.testing.expectEqual(@as(usize, 3), result.positional.items.len);
}

test "CliParser - default values" {
    const allocator = std.testing.allocator;

    var parser = cli.CliParser.init(allocator);
    defer parser.deinit();

    _ = try parser.addOption("port", 'p', "port", "Port number", false, "8080");
    _ = try parser.addOption("host", 'H', "host", "Host address", false, "localhost");
    _ = try parser.addOption("timeout", 't', "timeout", "Timeout in seconds", false, "30");

    const argv = [_][]const u8{ "myprogram", "--port", "3000" };

    var result = try parser.parseFromSlice(&argv);
    defer result.deinit();

    try std.testing.expect(result.isPresent("port"));
    try std.testing.expectEqualStrings("3000", result.getValue("port").?);

    // Check defaults
    try std.testing.expect(!result.isPresent("host"));
    try std.testing.expectEqualStrings("localhost", result.getValue("host").?);

    try std.testing.expect(!result.isPresent("timeout"));
    try std.testing.expectEqualStrings("30", result.getValue("timeout").?);
}

test "CliParser - only positional arguments" {
    const allocator = std.testing.allocator;

    var parser = cli.CliParser.init(allocator);
    defer parser.deinit();

    // No flags/options defined

    const argv = [_][]const u8{ "myprogram", "arg1", "arg2", "arg3" };

    var result = try parser.parseFromSlice(&argv);
    defer result.deinit();

    try std.testing.expectEqual(@as(usize, 3), result.positional.items.len);
}

test "CliParser - empty arguments" {
    const allocator = std.testing.allocator;

    var parser = cli.CliParser.init(allocator);
    defer parser.deinit();

    _ = try parser.addFlag("help", 'h', "help", "Show help");

    const argv = [_][]const u8{ "myprogram" };

    var result = try parser.parseFromSlice(&argv);
    defer result.deinit();

    try std.testing.expect(!result.isPresent("help"));
    try std.testing.expectEqual(@as(usize, 0), result.positional.items.len);
}

test "CliParser - long option only (no short)" {
    const allocator = std.testing.allocator;

    var parser = cli.CliParser.init(allocator);
    defer parser.deinit();

    _ = try parser.addOption("config", null, "config", "Config file", false, null);
    _ = try parser.addFlag("dry-run", null, "dry-run", "Dry run mode");

    const argv = [_][]const u8{ "myprogram", "--config", "settings.json", "--dry-run" };

    var result = try parser.parseFromSlice(&argv);
    defer result.deinit();

    try std.testing.expect(result.isPresent("config"));
    try std.testing.expectEqualStrings("settings.json", result.getValue("config").?);
    try std.testing.expect(result.isPresent("dry-run"));
}

test "CliParser - short option only (no long)" {
    const allocator = std.testing.allocator;

    var parser = cli.CliParser.init(allocator);
    defer parser.deinit();

    _ = try parser.addOption("file", 'f', null, "Input file", false, null);
    _ = try parser.addFlag("verbose", 'v', null, "Verbose mode");

    const argv = [_][]const u8{ "myprogram", "-f", "data.txt", "-v" };

    var result = try parser.parseFromSlice(&argv);
    defer result.deinit();

    try std.testing.expect(result.isPresent("file"));
    try std.testing.expectEqualStrings("data.txt", result.getValue("file").?);
    try std.testing.expect(result.isPresent("verbose"));
}

test "parseSimple - basic usage" {
    const allocator = std.testing.allocator;

    const argv = [_][]const u8{ "prog", "--name=Alice", "--verbose", "-d", "directory" };

    var result = try cli.parseSimple(allocator, &argv);
    defer {
        var iter = result.iterator();
        while (iter.next()) |entry| {
            if (entry.value_ptr.*) |v| allocator.free(v);
            allocator.free(entry.key_ptr.*);
        }
        result.deinit();
    }

    try std.testing.expectEqualStrings("Alice", result.get("name").?.?);
    try std.testing.expect(result.get("verbose").? == null);
    try std.testing.expect(result.get("d") != null);
}

test "parseSimple - equals syntax" {
    const allocator = std.testing.allocator;

    const argv = [_][]const u8{ "prog", "--key1=value1", "--key2=value with spaces" };

    var result = try cli.parseSimple(allocator, &argv);
    defer {
        var iter = result.iterator();
        while (iter.next()) |entry| {
            if (entry.value_ptr.*) |v| allocator.free(v);
            allocator.free(entry.key_ptr.*);
        }
        result.deinit();
    }

    try std.testing.expectEqualStrings("value1", result.get("key1").?.?);
    try std.testing.expectEqualStrings("value with spaces", result.get("key2").?.?);
}

test "hasFlag - detect flags" {
    const argv = [_][]const u8{ "prog", "-v", "--verbose", "--help" };

    try std.testing.expect(cli.hasFlag(&argv, 'v', null));
    try std.testing.expect(cli.hasFlag(&argv, null, "verbose"));
    try std.testing.expect(cli.hasFlag(&argv, 'h', "help"));
    try std.testing.expect(!cli.hasFlag(&argv, 'q', null));
    try std.testing.expect(!cli.hasFlag(&argv, null, "quiet"));
}

test "hasFlag - with both short and long" {
    const argv1 = [_][]const u8{ "prog", "-v" };
    const argv2 = [_][]const u8{ "prog", "--verbose" };

    try std.testing.expect(cli.hasFlag(&argv1, 'v', "verbose"));
    try std.testing.expect(cli.hasFlag(&argv2, 'v', "verbose"));
    try std.testing.expect(!cli.hasFlag(&argv1, 'q', "quiet"));
}

test "countPositionalArgs - count non-flag arguments" {
    const argv1 = [_][]const u8{ "prog", "file1.txt", "file2.txt" };
    try std.testing.expectEqual(@as(usize, 2), cli.countPositionalArgs(&argv1));

    const argv2 = [_][]const u8{ "prog", "-v", "file.txt", "--output=out.txt" };
    try std.testing.expectEqual(@as(usize, 1), cli.countPositionalArgs(&argv2));

    const argv3 = [_][]const u8{ "prog", "-v", "--help" };
    try std.testing.expectEqual(@as(usize, 0), cli.countPositionalArgs(&argv3));
}

test "getPositionalArgs - extract positional args" {
    const allocator = std.testing.allocator;

    const argv = [_][]const u8{ "prog", "-v", "file1.txt", "--output=out.txt", "file2.txt" };

    const positional = try cli.getPositionalArgs(allocator, &argv);
    defer {
        for (positional) |arg| {
            allocator.free(arg);
        }
        allocator.free(positional);
    }

    try std.testing.expectEqual(@as(usize, 2), positional.len);
    try std.testing.expectEqualStrings("file1.txt", positional[0]);
    try std.testing.expectEqualStrings("file2.txt", positional[1]);
}

test "CliParser - generate help" {
    const allocator = std.testing.allocator;

    var parser = cli.CliParser.init(allocator);
    defer parser.deinit();

    _ = parser.setProgramName("myapp");
    _ = try parser.addFlag("verbose", 'v', "verbose", "Enable verbose output");
    _ = try parser.addFlag("help", 'h', "help", "Show this help message");
    _ = try parser.addOption("file", 'f', "file", "Input file", true, null);
    _ = try parser.addOption("output", 'o', "output", "Output file", false, "output.txt");
    _ = try parser.addOption("count", 'c', "count", "Number of iterations", false, "10");

    var buffer = std.ArrayList(u8).init(allocator);
    defer buffer.deinit();

    try parser.generateHelp(buffer.writer());

    const help_text = buffer.items;
    try std.testing.expect(std.mem.indexOf(u8, help_text, "myapp") != null);
    try std.testing.expect(std.mem.indexOf(u8, help_text, "verbose") != null);
    try std.testing.expect(std.mem.indexOf(u8, help_text, "[required]") != null);
    try std.testing.expect(std.mem.indexOf(u8, help_text, "(default: output.txt)") != null);
}

test "CliParser - complex real-world scenario" {
    const allocator = std.testing.allocator;

    var parser = cli.CliParser.init(allocator);
    defer parser.deinit();

    _ = parser.setProgramName("file-processor");
    _ = parser.setDescription("Process files with various options");
    _ = try parser.addFlag("verbose", 'v', "verbose", "Enable verbose output");
    _ = try parser.addFlag("dry-run", 'd', "dry-run", "Show what would be done without making changes");
    _ = try parser.addFlag("force", 'f', "force", "Force overwrite existing files");
    _ = try parser.addOption("output", 'o', "output", "Output directory", false, "./output");
    _ = try parser.addOption("format", null, "format", "Output format (json, csv, xml)", false, "json");
    _ = try parser.addOption("threads", 'j', "threads", "Number of threads", false, "4");

    const argv = [_][]const u8{
        "file-processor",
        "-v",
        "--format=csv",
        "-j", "8",
        "input1.txt",
        "input2.txt",
        "input3.txt",
    };

    var result = try parser.parseFromSlice(&argv);
    defer result.deinit();

    // Check flags
    try std.testing.expect(result.isPresent("verbose"));
    try std.testing.expect(!result.isPresent("dry-run"));
    try std.testing.expect(!result.isPresent("force"));

    // Check options
    try std.testing.expectEqualStrings("csv", result.getValue("format").?);
    try std.testing.expectEqualStrings("8", result.getValue("threads").?);
    try std.testing.expectEqualStrings("./output", result.getValue("output").?); // default

    // Check positional
    try std.testing.expectEqual(@as(usize, 3), result.positional.items.len);
    try std.testing.expectEqualStrings("input1.txt", result.getPositional(0).?);
    try std.testing.expectEqualStrings("input2.txt", result.getPositional(1).?);
    try std.testing.expectEqualStrings("input3.txt", result.getPositional(2).?);
}

test "CliParser - multiple values same option" {
    const allocator = std.testing.allocator;

    var parser = cli.CliParser.init(allocator);
    defer parser.deinit();

    _ = try parser.addOption("include", 'I', "include", "Include path", false, null);

    const argv = [_][]const u8{ "myprogram", "-I", "/usr/include", "-I", "/usr/local/include" };

    var result = try parser.parseFromSlice(&argv);
    defer result.deinit();

    // Note: This tests that the last value wins (common behavior)
    try std.testing.expect(result.isPresent("include"));
    try std.testing.expectEqualStrings("/usr/local/include", result.getValue("include").?);
}

test "CliParser - dashes in values" {
    const allocator = std.testing.allocator;

    var parser = cli.CliParser.init(allocator);
    defer parser.deinit();

    _ = try parser.addOption("date", 'd', "date", "Date value", false, null);
    _ = try parser.addOption("name", 'n', "name", "Name value", false, null);

    const argv = [_][]const u8{ "myprogram", "--date=2024-01-15", "--name=some-name" };

    var result = try parser.parseFromSlice(&argv);
    defer result.deinit();

    try std.testing.expectEqualStrings("2024-01-15", result.getValue("date").?);
    try std.testing.expectEqualStrings("some-name", result.getValue("name").?);
}

test "CliParser - get with default fallback" {
    const allocator = std.testing.allocator;

    var parser = cli.CliParser.init(allocator);
    defer parser.deinit();

    _ = try parser.addOption("port", 'p', "port", "Port number", false, "8080");

    const argv = [_][]const u8{ "myprogram" };

    var result = try parser.parseFromSlice(&argv);
    defer result.deinit();

    // getValue returns the default
    try std.testing.expectEqualStrings("8080", result.getValue("port").?);
    // But isPresent should be false
    try std.testing.expect(!result.isPresent("port"));
}