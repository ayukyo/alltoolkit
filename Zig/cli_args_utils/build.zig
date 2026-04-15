const std = @import("std");

pub fn build(b: *std.Build) void {
    const target = b.standardTargetOptions(.{});
    const optimize = b.standardOptimizeOption(.{});

    // Module for external use
    _ = b.addModule("cli_args_utils", .{
        .root_source_file = b.path("mod.zig"),
        .target = target,
        .optimize = optimize,
    });

    // Tests
    const unit_tests = b.addTest(.{
        .root_source_file = b.path("cli_args_utils_test.zig"),
        .target = target,
        .optimize = optimize,
    });

    const run_unit_tests = b.addRunArtifact(unit_tests);

    const test_step = b.step("test", "Run unit tests");
    test_step.dependOn(&run_unit_tests.step);

    // Example executable
    const example_exe = b.addExecutable(.{
        .name = "cli_example",
        .root_source_file = b.path("examples/usage_examples.zig"),
        .target = target,
        .optimize = optimize,
    });

    const run_example = b.addRunArtifact(example_exe);

    const example_step = b.step("example", "Run the example program");
    example_step.dependOn(&run_example.step);
}