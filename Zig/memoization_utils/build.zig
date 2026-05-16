const std = @import("std");

pub fn build(b: *std.Build) void {
    const target = b.standardTargetOptions(.{});
    const optimize = b.standardOptimizeOption(.{});

    // Module
    const memoization_module = b.addModule("memoization", .{
        .root_source_file = b.path("memoization.zig"),
        .target = target,
        .optimize = optimize,
    });

    // Tests
    const unit_tests = b.addTest(.{
        .root_source_file = b.path("memoization.zig"),
        .target = target,
        .optimize = optimize,
    });

    const run_unit_tests = b.addRunArtifact(unit_tests);
    const test_step = b.step("test", "Run unit tests");
    test_step.dependOn(&run_unit_tests.step);

    // Example
    const example_exe = b.addExecutable(.{
        .name = "memoization_example",
        .root_source_file = b.path("examples/example.zig"),
        .target = target,
        .optimize = optimize,
    });
    example_exe.root_module.addImport("memoization", memoization_module);
    b.installArtifact(example_exe);

    const run_example = b.addRunArtifact(example_exe);
    const example_step = b.step("example", "Run the example");
    example_step.dependOn(&run_example.step);

    // Benchmark
    const benchmark_exe = b.addExecutable(.{
        .name = "memoization_benchmark",
        .root_source_file = b.path("examples/benchmark.zig"),
        .target = target,
        .optimize = optimize,
    });
    benchmark_exe.root_module.addImport("memoization", memoization_module);
    b.installArtifact(benchmark_exe);

    const run_benchmark = b.addRunArtifact(benchmark_exe);
    const benchmark_step = b.step("benchmark", "Run benchmarks");
    benchmark_step.dependOn(&run_benchmark.step);
}