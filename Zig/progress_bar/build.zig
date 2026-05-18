const std = @import("std");

pub fn build(b: *std.Build) void {
    const target = b.standardTargetOptions(.{});
    const optimize = b.standardOptimizeOption(.{});

    // Module
    const mod = b.addModule("progress_bar", .{
        .root_source_file = b.path("progress_bar.zig"),
        .target = target,
        .optimize = optimize,
    });

    // Tests
    const tests = b.addTest(.{
        .root_source_file = b.path("progress_bar.zig"),
        .target = target,
        .optimize = optimize,
    });
    const run_tests = b.addRunArtifact(tests);

    const test_step = b.step("test", "Run unit tests");
    test_step.dependOn(&run_tests.step);

    // Example
    const example = b.addExecutable(.{
        .name = "progress_bar_example",
        .root_source_file = b.path("example.zig"),
        .target = target,
        .optimize = optimize,
    });
    example.root_module.addImport("progress_bar", mod);

    const run_example = b.addRunArtifact(example);
    const example_step = b.step("example", "Run example");
    example_step.dependOn(&run_example.step);
}