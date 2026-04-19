const std = @import("std");

pub fn build(b: *std.Build) void {
    const target = b.standardTargetOptions(.{});
    const optimize = b.standardOptimizeOption(.{});

    // Module
    const pq_module = b.addModule("priority_queue", .{
        .root_source_file = b.path("src/priority_queue.zig"),
        .target = target,
        .optimize = optimize,
    });

    // Tests
    const unit_tests = b.addTest(.{
        .root_source_file = b.path("src/priority_queue.zig"),
        .target = target,
        .optimize = optimize,
    });

    const run_unit_tests = b.addRunArtifact(unit_tests);

    // Test step
    const test_step = b.step("test", "Run unit tests");
    test_step.dependOn(&run_unit_tests.step);

    // Example: Basic usage
    const example_basic = b.addExecutable(.{
        .name = "basic_example",
        .root_source_file = b.path("examples/basic.zig"),
        .target = target,
        .optimize = optimize,
    });
    example_basic.root_module.addImport("priority_queue", pq_module);

    const run_example_basic = b.addRunArtifact(example_basic);
    const example_basic_step = b.step("example-basic", "Run basic example");
    example_basic_step.dependOn(&run_example_basic.step);

    // Example: Task scheduler
    const example_scheduler = b.addExecutable(.{
        .name = "scheduler_example",
        .root_source_file = b.path("examples/scheduler.zig"),
        .target = target,
        .optimize = optimize,
    });
    example_scheduler.root_module.addImport("priority_queue", pq_module);

    const run_example_scheduler = b.addRunArtifact(example_scheduler);
    const example_scheduler_step = b.step("example-scheduler", "Run scheduler example");
    example_scheduler_step.dependOn(&run_example_scheduler.step);

    // Example: Dijkstra's algorithm helper
    const example_dijkstra = b.addExecutable(.{
        .name = "dijkstra_example",
        .root_source_file = b.path("examples/dijkstra.zig"),
        .target = target,
        .optimize = optimize,
    });
    example_dijkstra.root_module.addImport("priority_queue", pq_module);

    const run_example_dijkstra = b.addRunArtifact(example_dijkstra);
    const example_dijkstra_step = b.step("example-dijkstra", "Run Dijkstra example");
    example_dijkstra_step.dependOn(&run_example_dijkstra.step);
}